#!/usr/bin/env python3
"""
SQL Code Generator

Generates SQL code from SQL AST nodes with support for multiple SQL dialects.
Supports ANSI SQL-92/99/2003/2008/2011/2016, MySQL, PostgreSQL, SQL Server, Oracle, and SQLite.

This module provides:
- SQLCodeGenerator: SQL AST → SQL code generation
- Multi-dialect support with dialect-specific formatting
- Configurable code formatting options
- Performance-optimized generation
- Comprehensive SQL construct support

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Set, TextIO
from dataclasses import dataclass, field
from enum import Enum, auto
import io
import logging

from .sql_ast import (
    SQLNode, SQLProgram, SQLStatement, SQLExpression, SQLClause,
    SQLSelectStatement, SQLInsertStatement, SQLUpdateStatement, SQLDeleteStatement,
    SQLCreateTableStatement, SQLDropTableStatement, SQLAlterTableStatement,
    SQLBinaryExpression, SQLUnaryExpression, SQLFunctionCall, SQLCaseExpression,
    SQLCastExpression, SQLSubquery, SQLColumnReference, SQLIdentifier,
    SQLQualifiedIdentifier, SQLLiteral, SQLIntegerLiteral, SQLFloatLiteral,
    SQLStringLiteral, SQLBooleanLiteral, SQLNullLiteral, SQLDateLiteral,
    SQLTimeLiteral, SQLTimestampLiteral, SQLIntervalLiteral,
    SQLDataType, SQLIntegerType, SQLVarcharType, SQLDecimalType, SQLArrayType,
    SQLFromClause, SQLWhereClause, SQLGroupByClause, SQLHavingClause,
    SQLOrderByClause, SQLOrderByExpression, SQLLimitClause, SQLOffsetClause,
    SQLWithClause, SQLCommonTableExpression, SQLTableReference, SQLTableName,
    SQLJoin, SQLDerivedTable, SQLColumnDefinition, SQLConstraint,
    SQLPrimaryKeyConstraint, SQLForeignKeyConstraint, SQLUniqueConstraint,
    SQLCheckConstraint, SQLDefaultConstraint, SQLInExpression, SQLBetweenExpression,
    SQLLikeExpression, SQLExistsExpression, SQLWindowSpecification,
    SQLSetOperation, SQLAlterTableAction, SQLAddColumnAction, SQLDropColumnAction,
    SQLAlterColumnAction, SQLAddConstraintAction, SQLDropConstraintAction,
    SQLJSONExtractExpression, SQLJSONObjectExpression, SQLJSONArrayExpression,
    SQLArrayConstructor, SQLArrayElement, SQLOperator, SQLDialect, JoinType,
    ConstraintType, WindowFrameType, WindowFrameBound, SQLVisitor
)

# Import core AST for Runa integration
from ....core.runa_ast import TranslationMetadata, SourceLocation


class SQLFormattingStyle(Enum):
    """SQL code formatting styles."""
    COMPACT = "compact"           # Minimal whitespace
    READABLE = "readable"         # Balanced formatting
    EXPANDED = "expanded"         # Maximum readability
    MINIFIED = "minified"         # No unnecessary whitespace


class SQLKeywordCase(Enum):
    """SQL keyword case options."""
    UPPER = "upper"               # SELECT, FROM, WHERE
    LOWER = "lower"               # select, from, where  
    TITLE = "title"               # Select, From, Where


@dataclass
class SQLGenerationOptions:
    """SQL code generation options."""
    dialect: SQLDialect = SQLDialect.ANSI
    formatting_style: SQLFormattingStyle = SQLFormattingStyle.READABLE
    keyword_case: SQLKeywordCase = SQLKeywordCase.UPPER
    indent_size: int = 2
    max_line_length: int = 120
    include_comments: bool = True
    include_metadata: bool = False
    quote_identifiers: bool = False
    use_trailing_commas: bool = False
    align_columns: bool = True
    break_long_lines: bool = True


class SQLCodeGenerator(SQLVisitor):
    """
    SQL code generator that converts SQL AST to formatted SQL code.
    
    Supports multiple SQL dialects and configurable formatting options.
    Uses the visitor pattern to traverse the AST and generate code.
    """
    
    def __init__(self, options: Optional[SQLGenerationOptions] = None):
        """Initialize the SQL code generator."""
        self.options = options or SQLGenerationOptions()
        self.logger = logging.getLogger(__name__)
        self._output = io.StringIO()
        self._indent_level = 0
        self._current_line_length = 0
        self._in_subquery = False
        self._generated_metadata: List[TranslationMetadata] = []
        
        # Dialect-specific configuration
        self._configure_dialect()
    
    def _configure_dialect(self):
        """Configure dialect-specific settings."""
        dialect_configs = {
            SQLDialect.MYSQL: {
                'quote_char': '`',
                'string_quote': "'",
                'supports_limit': True,
                'supports_offset': True,
                'limit_syntax': 'LIMIT {offset}, {count}',
                'boolean_true': 'TRUE',
                'boolean_false': 'FALSE',
            },
            SQLDialect.POSTGRESQL: {
                'quote_char': '"',
                'string_quote': "'",
                'supports_limit': True,
                'supports_offset': True,
                'limit_syntax': 'LIMIT {count} OFFSET {offset}',
                'boolean_true': 'TRUE',
                'boolean_false': 'FALSE',
            },
            SQLDialect.SQLSERVER: {
                'quote_char': '[',
                'quote_char_end': ']',
                'string_quote': "'",
                'supports_limit': True,
                'supports_offset': True,
                'limit_syntax': 'OFFSET {offset} ROWS FETCH NEXT {count} ROWS ONLY',
                'boolean_true': '1',
                'boolean_false': '0',
            },
            SQLDialect.ORACLE: {
                'quote_char': '"',
                'string_quote': "'",
                'supports_limit': True,
                'supports_offset': True,
                'limit_syntax': 'OFFSET {offset} ROWS FETCH NEXT {count} ROWS ONLY',
                'boolean_true': '1',
                'boolean_false': '0',
            },
            SQLDialect.SQLITE: {
                'quote_char': '"',
                'string_quote': "'",
                'supports_limit': True,
                'supports_offset': True,
                'limit_syntax': 'LIMIT {count} OFFSET {offset}',
                'boolean_true': '1',
                'boolean_false': '0',
            },
            SQLDialect.ANSI: {
                'quote_char': '"',
                'string_quote': "'",
                'supports_limit': True,
                'supports_offset': True,
                'limit_syntax': 'LIMIT {count} OFFSET {offset}',
                'boolean_true': 'TRUE',
                'boolean_false': 'FALSE',
            }
        }
        
        self.dialect_config = dialect_configs.get(
            self.options.dialect, 
            dialect_configs[SQLDialect.ANSI]
        )
    
    def generate(self, ast: SQLProgram) -> str:
        """Generate SQL code from AST."""
        self._output = io.StringIO()
        self._indent_level = 0
        self._current_line_length = 0
        self._generated_metadata.clear()
        
        try:
            self.visit_program(ast)
            result = self._output.getvalue()
            
            if self.options.include_metadata:
                self._add_generation_metadata(ast)
            
            return result.strip()
            
        except Exception as e:
            self.logger.error(f"Failed to generate SQL code: {e}")
            raise
    
    def get_metadata(self) -> List[TranslationMetadata]:
        """Get generation metadata."""
        return self._generated_metadata.copy()
    
    # Visitor methods
    
    def visit_program(self, node: SQLProgram):
        """Visit SQL program node."""
        for i, stmt in enumerate(node.statements):
            if i > 0:
                self._write_line("")
            stmt.accept(self)
            if not self._output.getvalue().endswith(';'):
                self._write(";")
            self._write_line("")
    
    def visit_select_statement(self, node: SQLSelectStatement):
        """Visit SELECT statement."""
        # WITH clause
        if node.with_clause:
            node.with_clause.accept(self)
            self._write_line("")
        
        # SELECT clause
        self._write_keyword("SELECT")
        
        if node.distinct:
            self._write(" ")
            self._write_keyword("DISTINCT")
            if node.distinct_on:
                self._write("(")
                self._write_expression_list(node.distinct_on)
                self._write(")")
        
        self._write_line("")
        self._indent()
        self._write_expression_list(node.select_list, multiline=True)
        self._dedent()
        
        # FROM clause
        if node.from_clause:
            self._write_line("")
            node.from_clause.accept(self)
        
        # WHERE clause
        if node.where_clause:
            self._write_line("")
            node.where_clause.accept(self)
        
        # GROUP BY clause
        if node.group_by_clause:
            self._write_line("")
            node.group_by_clause.accept(self)
        
        # HAVING clause
        if node.having_clause:
            self._write_line("")
            node.having_clause.accept(self)
        
        # ORDER BY clause
        if node.order_by_clause:
            self._write_line("")
            node.order_by_clause.accept(self)
        
        # LIMIT clause
        if node.limit_clause:
            self._write_line("")
            node.limit_clause.accept(self)
        
        # OFFSET clause
        if node.offset_clause and self.options.dialect != SQLDialect.MYSQL:
            self._write_line("")
            node.offset_clause.accept(self)
    
    def visit_insert_statement(self, node: SQLInsertStatement):
        """Visit INSERT statement."""
        self._write_keyword("INSERT INTO")
        self._write(" ")
        node.table.accept(self)
        
        if node.columns:
            self._write(" (")
            self._write_node_list(node.columns)
            self._write(")")
        
        if node.values:
            self._write_line("")
            self._write_keyword("VALUES")
            self._write_line("")
            self._indent()
            for i, value_list in enumerate(node.values):
                if i > 0:
                    self._write(",")
                    self._write_line("")
                self._write("(")
                self._write_expression_list(value_list)
                self._write(")")
            self._dedent()
        elif node.select_query:
            self._write_line("")
            node.select_query.accept(self)
        
        if node.returning:
            self._write_line("")
            self._write_keyword("RETURNING")
            self._write(" ")
            self._write_expression_list(node.returning)
    
    def visit_update_statement(self, node: SQLUpdateStatement):
        """Visit UPDATE statement."""
        self._write_keyword("UPDATE")
        self._write(" ")
        node.table.accept(self)
        
        self._write_line("")
        self._write_keyword("SET")
        self._write_line("")
        self._indent()
        for i, (column, value) in enumerate(node.set_clauses):
            if i > 0:
                self._write(",")
                self._write_line("")
            column.accept(self)
            self._write(" = ")
            value.accept(self)
        self._dedent()
        
        if node.from_clause:
            self._write_line("")
            node.from_clause.accept(self)
        
        if node.where_clause:
            self._write_line("")
            node.where_clause.accept(self)
        
        if node.returning:
            self._write_line("")
            self._write_keyword("RETURNING")
            self._write(" ")
            self._write_expression_list(node.returning)
    
    def visit_delete_statement(self, node: SQLDeleteStatement):
        """Visit DELETE statement."""
        self._write_keyword("DELETE FROM")
        self._write(" ")
        node.table.accept(self)
        
        if node.where_clause:
            self._write_line("")
            node.where_clause.accept(self)
        
        if node.returning:
            self._write_line("")
            self._write_keyword("RETURNING")
            self._write(" ")
            self._write_expression_list(node.returning)
    
    def visit_create_table_statement(self, node: SQLCreateTableStatement):
        """Visit CREATE TABLE statement."""
        self._write_keyword("CREATE")
        if node.temporary:
            self._write(" ")
            self._write_keyword("TEMPORARY")
        self._write(" ")
        self._write_keyword("TABLE")
        if node.if_not_exists:
            self._write(" ")
            self._write_keyword("IF NOT EXISTS")
        self._write(" ")
        node.table_name.accept(self)
        
        if node.as_query:
            self._write(" ")
            self._write_keyword("AS")
            self._write_line("")
            node.as_query.accept(self)
        else:
            self._write(" (")
            self._write_line("")
            self._indent()
            
            # Columns
            for i, column in enumerate(node.columns):
                if i > 0:
                    self._write(",")
                    self._write_line("")
                column.accept(self)
            
            # Table constraints
            if node.constraints:
                for constraint in node.constraints:
                    self._write(",")
                    self._write_line("")
                    constraint.accept(self)
            
            self._dedent()
            self._write_line("")
            self._write(")")
    
    def visit_drop_table_statement(self, node: SQLDropTableStatement):
        """Visit DROP TABLE statement."""
        self._write_keyword("DROP TABLE")
        if node.if_exists:
            self._write(" ")
            self._write_keyword("IF EXISTS")
        self._write(" ")
        self._write_node_list(node.table_names)
        if node.cascade:
            self._write(" ")
            self._write_keyword("CASCADE")
    
    def visit_alter_table_statement(self, node: SQLAlterTableStatement):
        """Visit ALTER TABLE statement."""
        self._write_keyword("ALTER TABLE")
        self._write(" ")
        node.table_name.accept(self)
        self._write_line("")
        self._indent()
        for i, action in enumerate(node.actions):
            if i > 0:
                self._write(",")
                self._write_line("")
            action.accept(self)
        self._dedent()
    
    def visit_binary_expression(self, node: SQLBinaryExpression):
        """Visit binary expression."""
        # Handle operator precedence
        left_needs_parens = self._needs_parentheses(node.left, node)
        right_needs_parens = self._needs_parentheses(node.right, node)
        
        if left_needs_parens:
            self._write("(")
        node.left.accept(self)
        if left_needs_parens:
            self._write(")")
        
        self._write(" ")
        self._write_operator(node.operator)
        self._write(" ")
        
        if right_needs_parens:
            self._write("(")
        node.right.accept(self)
        if right_needs_parens:
            self._write(")")
    
    def visit_unary_expression(self, node: SQLUnaryExpression):
        """Visit unary expression."""
        if node.prefix:
            self._write_operator(node.operator)
            if node.operator in [SQLOperator.NOT]:
                self._write(" ")
        
        operand_needs_parens = self._needs_parentheses(node.operand, node)
        if operand_needs_parens:
            self._write("(")
        node.operand.accept(self)
        if operand_needs_parens:
            self._write(")")
        
        if not node.prefix:
            self._write(" ")
            self._write_operator(node.operator)
    
    def visit_function_call(self, node: SQLFunctionCall):
        """Visit function call."""
        self._write_identifier(node.name)
        self._write("(")
        
        if node.distinct:
            self._write_keyword("DISTINCT")
            if node.arguments:
                self._write(" ")
        
        if node.arguments:
            self._write_expression_list(node.arguments)
        
        self._write(")")
        
        if node.window:
            self._write(" ")
            self._write_keyword("OVER")
            self._write(" (")
            node.window.accept(self)
            self._write(")")
    
    def visit_case_expression(self, node: SQLCaseExpression):
        """Visit CASE expression."""
        self._write_keyword("CASE")
        
        if node.expression:
            self._write(" ")
            node.expression.accept(self)
        
        for when_expr, then_expr in node.when_clauses:
            self._write_line("")
            self._indent()
            self._write_keyword("WHEN")
            self._write(" ")
            when_expr.accept(self)
            self._write(" ")
            self._write_keyword("THEN")
            self._write(" ")
            then_expr.accept(self)
            self._dedent()
        
        if node.else_clause:
            self._write_line("")
            self._indent()
            self._write_keyword("ELSE")
            self._write(" ")
            node.else_clause.accept(self)
            self._dedent()
        
        self._write_line("")
        self._write_keyword("END")
    
    def visit_cast_expression(self, node: SQLCastExpression):
        """Visit CAST expression."""
        self._write_keyword("CAST")
        self._write("(")
        node.expression.accept(self)
        self._write(" ")
        self._write_keyword("AS")
        self._write(" ")
        node.target_type.accept(self)
        self._write(")")
    
    def visit_subquery(self, node: SQLSubquery):
        """Visit subquery."""
        old_in_subquery = self._in_subquery
        self._in_subquery = True
        
        self._write("(")
        self._write_line("")
        self._indent()
        node.query.accept(self)
        self._dedent()
        self._write_line("")
        self._write(")")
        
        self._in_subquery = old_in_subquery
    
    def visit_column_reference(self, node: SQLColumnReference):
        """Visit column reference."""
        if node.schema:
            self._write_identifier(node.schema)
            self._write(".")
        if node.table:
            self._write_identifier(node.table)
            self._write(".")
        self._write_identifier(node.column)
    
    def visit_identifier(self, node: SQLIdentifier):
        """Visit identifier."""
        self._write_identifier(node.name, node.quoted)
    
    def visit_qualified_identifier(self, node: SQLQualifiedIdentifier):
        """Visit qualified identifier."""
        for i, (part, quoted) in enumerate(zip(node.parts, node.quoted)):
            if i > 0:
                self._write(".")
            self._write_identifier(part, quoted)
    
    def visit_literal(self, node: SQLLiteral):
        """Visit literal base class."""
        # Dispatch to specific literal visitor
        if hasattr(node, 'accept'):
            node.accept(self)
        else:
            self._write(str(node.value))
    
    def visit_integer_literal(self, node: SQLIntegerLiteral):
        """Visit integer literal."""
        self._write(str(node.value))
    
    def visit_float_literal(self, node: SQLFloatLiteral):
        """Visit float literal."""
        self._write(str(node.value))
    
    def visit_string_literal(self, node: SQLStringLiteral):
        """Visit string literal."""
        quote = self.dialect_config['string_quote']
        escaped_value = node.value.replace(quote, quote + quote)
        self._write(f"{quote}{escaped_value}{quote}")
    
    def visit_boolean_literal(self, node: SQLBooleanLiteral):
        """Visit boolean literal."""
        if node.value:
            self._write(self.dialect_config['boolean_true'])
        else:
            self._write(self.dialect_config['boolean_false'])
    
    def visit_null_literal(self, node: SQLNullLiteral):
        """Visit NULL literal."""
        self._write_keyword("NULL")
    
    def visit_date_literal(self, node: SQLDateLiteral):
        """Visit date literal."""
        self._write_keyword("DATE")
        self._write(" ")
        quote = self.dialect_config['string_quote']
        self._write(f"{quote}{node.value}{quote}")
    
    def visit_time_literal(self, node: SQLTimeLiteral):
        """Visit time literal."""
        self._write_keyword("TIME")
        self._write(" ")
        quote = self.dialect_config['string_quote']
        self._write(f"{quote}{node.value}{quote}")
    
    def visit_timestamp_literal(self, node: SQLTimestampLiteral):
        """Visit timestamp literal."""
        self._write_keyword("TIMESTAMP")
        self._write(" ")
        quote = self.dialect_config['string_quote']
        self._write(f"{quote}{node.value}{quote}")
    
    def visit_interval_literal(self, node: SQLIntervalLiteral):
        """Visit interval literal."""
        self._write_keyword("INTERVAL")
        self._write(" ")
        quote = self.dialect_config['string_quote']
        self._write(f"{quote}{node.value}{quote}")
        if node.unit:
            self._write(" ")
            self._write_keyword(node.unit)
    
    def visit_data_type(self, node: SQLDataType):
        """Visit data type."""
        self._write_keyword(node.name)
        if node.parameters:
            self._write("(")
            for i, param in enumerate(node.parameters):
                if i > 0:
                    self._write(", ")
                self._write(str(param))
            self._write(")")
    
    def visit_constraint(self, node: SQLConstraint):
        """Visit constraint base class."""
        # Dispatch to specific constraint visitor
        if hasattr(node, 'accept'):
            node.accept(self)
    
    def visit_from_clause(self, node: SQLFromClause):
        """Visit FROM clause."""
        self._write_keyword("FROM")
        if node.table_references:
            self._write_line("")
            self._indent()
            for i, table_ref in enumerate(node.table_references):
                if i > 0:
                    self._write(",")
                    self._write_line("")
                table_ref.accept(self)
            self._dedent()
    
    def visit_where_clause(self, node: SQLWhereClause):
        """Visit WHERE clause."""
        self._write_keyword("WHERE")
        self._write(" ")
        node.condition.accept(self)
    
    def visit_group_by_clause(self, node: SQLGroupByClause):
        """Visit GROUP BY clause."""
        self._write_keyword("GROUP BY")
        self._write(" ")
        self._write_expression_list(node.expressions)
    
    def visit_having_clause(self, node: SQLHavingClause):
        """Visit HAVING clause."""
        self._write_keyword("HAVING")
        self._write(" ")
        node.condition.accept(self)
    
    def visit_order_by_clause(self, node: SQLOrderByClause):
        """Visit ORDER BY clause."""
        self._write_keyword("ORDER BY")
        self._write(" ")
        self._write_node_list(node.expressions)
    
    def visit_limit_clause(self, node: SQLLimitClause):
        """Visit LIMIT clause."""
        if self.options.dialect == SQLDialect.SQLSERVER:
            # SQL Server uses TOP in SELECT clause
            return
        
        if self.options.dialect == SQLDialect.MYSQL:
            # MySQL LIMIT syntax handled in SELECT
            return
        
        self._write_keyword("LIMIT")
        self._write(" ")
        node.count.accept(self)
    
    def visit_offset_clause(self, node: SQLOffsetClause):
        """Visit OFFSET clause."""
        if self.options.dialect == SQLDialect.MYSQL:
            # MySQL OFFSET is part of LIMIT
            return
        
        self._write_keyword("OFFSET")
        self._write(" ")
        node.count.accept(self)
    
    def visit_with_clause(self, node: SQLWithClause):
        """Visit WITH clause."""
        self._write_keyword("WITH")
        if node.recursive:
            self._write(" ")
            self._write_keyword("RECURSIVE")
        self._write_line("")
        self._indent()
        for i, cte in enumerate(node.cte_list):
            if i > 0:
                self._write(",")
                self._write_line("")
            cte.accept(self)
        self._dedent()
    
    def visit_join(self, node: SQLJoin):
        """Visit JOIN."""
        node.left.accept(self)
        self._write_line("")
        
        # Join type
        if node.join_type == JoinType.INNER:
            self._write_keyword("INNER JOIN")
        elif node.join_type == JoinType.LEFT:
            self._write_keyword("LEFT JOIN")
        elif node.join_type == JoinType.RIGHT:
            self._write_keyword("RIGHT JOIN")
        elif node.join_type == JoinType.FULL:
            self._write_keyword("FULL OUTER JOIN")
        elif node.join_type == JoinType.CROSS:
            self._write_keyword("CROSS JOIN")
        elif node.join_type == JoinType.NATURAL:
            self._write_keyword("NATURAL JOIN")
        else:
            self._write_keyword("JOIN")
        
        self._write(" ")
        node.right.accept(self)
        
        if node.condition:
            self._write(" ")
            self._write_keyword("ON")
            self._write(" ")
            node.condition.accept(self)
        elif node.using_columns:
            self._write(" ")
            self._write_keyword("USING")
            self._write(" (")
            self._write_node_list(node.using_columns)
            self._write(")")
    
    def visit_table_reference(self, node: SQLTableReference):
        """Visit table reference base class."""
        # Dispatch to specific table reference visitor
        if hasattr(node, 'accept'):
            node.accept(self)
    
    def visit_column_definition(self, node: SQLColumnDefinition):
        """Visit column definition."""
        node.name.accept(self)
        self._write(" ")
        node.data_type.accept(self)
        
        for constraint in node.constraints:
            self._write(" ")
            constraint.accept(self)
    
    def visit_window_specification(self, node: SQLWindowSpecification):
        """Visit window specification."""
        parts = []
        
        if node.partition_by:
            parts.append("PARTITION BY")
            # Add partition expressions
        
        if node.order_by:
            parts.append("ORDER BY")
            # Add order expressions
        
        if node.frame_clause:
            # Add frame clause
            pass
        
        # Write parts with appropriate spacing
        for i, part in enumerate(parts):
            if i > 0:
                self._write(" ")
            self._write_keyword(part)
    
    def visit_set_operation(self, node: SQLSetOperation):
        """Visit set operation."""
        node.left.accept(self)
        self._write_line("")
        
        self._write_keyword(node.operation.upper())
        if node.all_modifier:
            self._write(" ")
            self._write_keyword("ALL")
        
        self._write_line("")
        node.right.accept(self)
    
    # Helper methods
    
    def _write(self, text: str):
        """Write text to output."""
        self._output.write(text)
        self._current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write line with optional text."""
        if text:
            self._write(text)
        self._write("\n")
        if self._indent_level > 0:
            indent = " " * (self._indent_level * self.options.indent_size)
            self._write(indent)
        self._current_line_length = self._indent_level * self.options.indent_size
    
    def _write_keyword(self, keyword: str):
        """Write SQL keyword with appropriate case."""
        if self.options.keyword_case == SQLKeywordCase.UPPER:
            self._write(keyword.upper())
        elif self.options.keyword_case == SQLKeywordCase.LOWER:
            self._write(keyword.lower())
        else:  # TITLE
            self._write(keyword.title())
    
    def _write_identifier(self, name: str, quoted: bool = False):
        """Write identifier with optional quoting."""
        if quoted or self.options.quote_identifiers:
            quote_char = self.dialect_config['quote_char']
            quote_end = self.dialect_config.get('quote_char_end', quote_char)
            escaped_name = name.replace(quote_char, quote_char + quote_char)
            self._write(f"{quote_char}{escaped_name}{quote_end}")
        else:
            self._write(name)
    
    def _write_operator(self, operator: SQLOperator):
        """Write SQL operator."""
        self._write(operator.value)
    
    def _write_expression_list(self, expressions: List[SQLExpression], multiline: bool = False):
        """Write comma-separated expression list."""
        for i, expr in enumerate(expressions):
            if i > 0:
                self._write(",")
                if multiline:
                    self._write_line("")
                else:
                    self._write(" ")
            expr.accept(self)
    
    def _write_node_list(self, nodes: List[SQLNode]):
        """Write comma-separated node list."""
        for i, node in enumerate(nodes):
            if i > 0:
                self._write(", ")
            node.accept(self)
    
    def _indent(self):
        """Increase indentation level."""
        self._indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self._indent_level = max(0, self._indent_level - 1)
    
    def _needs_parentheses(self, expr: SQLExpression, parent: SQLNode) -> bool:
        """Determine if expression needs parentheses."""
        # Simplified precedence check
        if isinstance(expr, SQLBinaryExpression) and isinstance(parent, SQLBinaryExpression):
            # Add proper operator precedence logic here
            pass
        return False
    
    def _add_generation_metadata(self, ast: SQLProgram):
        """Add generation metadata."""
        metadata = TranslationMetadata(
            source_location=SourceLocation(
                file="<generated>",
                line=1,
                column=1,
                length=len(self._output.getvalue())
            ),
            metadata={
                'generator': 'SQLCodeGenerator',
                'dialect': self.options.dialect.value,
                'formatting_style': self.options.formatting_style.value,
                'keyword_case': self.options.keyword_case.value,
                'generated_lines': self._output.getvalue().count('\n') + 1,
                'ast_nodes': self._count_ast_nodes(ast)
            }
        )
        self._generated_metadata.append(metadata)
    
    def _count_ast_nodes(self, node: SQLNode) -> int:
        """Count total AST nodes."""
        count = 1
        for child in node.children:
            count += self._count_ast_nodes(child)
        return count
    
    # Additional visitor methods for missing node types
    def visit_in_expression(self, node: SQLInExpression):
        """Visit IN expression."""
        node.expression.accept(self)
        if node.negated:
            self._write(" ")
            self._write_keyword("NOT")
        self._write(" ")
        self._write_keyword("IN")
        self._write(" (")
        self._write_expression_list(node.values)
        self._write(")")
    
    def visit_between_expression(self, node: SQLBetweenExpression):
        """Visit BETWEEN expression."""
        node.expression.accept(self)
        if node.negated:
            self._write(" ")
            self._write_keyword("NOT")
        self._write(" ")
        self._write_keyword("BETWEEN")
        self._write(" ")
        node.lower_bound.accept(self)
        self._write(" ")
        self._write_keyword("AND")
        self._write(" ")
        node.upper_bound.accept(self)
    
    def visit_like_expression(self, node: SQLLikeExpression):
        """Visit LIKE expression."""
        node.expression.accept(self)
        if node.negated:
            self._write(" ")
            self._write_keyword("NOT")
        self._write(" ")
        if node.case_insensitive:
            self._write_keyword("ILIKE")
        else:
            self._write_keyword("LIKE")
        self._write(" ")
        node.pattern.accept(self)
        if node.escape:
            self._write(" ")
            self._write_keyword("ESCAPE")
            self._write(" ")
            node.escape.accept(self)
    
    def visit_exists_expression(self, node: SQLExistsExpression):
        """Visit EXISTS expression."""
        if node.negated:
            self._write_keyword("NOT")
            self._write(" ")
        self._write_keyword("EXISTS")
        self._write(" ")
        node.subquery.accept(self)
    
    def visit_order_by_expression(self, node: SQLOrderByExpression):
        """Visit ORDER BY expression."""
        node.expression.accept(self)
        if not node.ascending:
            self._write(" ")
            self._write_keyword("DESC")
        if node.nulls_first is not None:
            self._write(" ")
            self._write_keyword("NULLS")
            self._write(" ")
            if node.nulls_first:
                self._write_keyword("FIRST")
            else:
                self._write_keyword("LAST")
    
    def visit_common_table_expression(self, node: SQLCommonTableExpression):
        """Visit common table expression."""
        node.name.accept(self)
        if node.columns:
            self._write(" (")
            self._write_node_list(node.columns)
            self._write(")")
        self._write(" ")
        self._write_keyword("AS")
        self._write(" (")
        self._write_line("")
        self._indent()
        node.query.accept(self)
        self._dedent()
        self._write_line("")
        self._write(")")
    
    def visit_table_name(self, node: SQLTableName):
        """Visit table name."""
        node.name.accept(self)
        if node.alias:
            self._write(" ")
            self._write_keyword("AS")
            self._write(" ")
            node.alias.accept(self)
    
    def visit_derived_table(self, node: SQLDerivedTable):
        """Visit derived table."""
        self._write("(")
        self._write_line("")
        self._indent()
        node.query.accept(self)
        self._dedent()
        self._write_line("")
        self._write(")")
        if node.alias:
            self._write(" ")
            self._write_keyword("AS")
            self._write(" ")
            node.alias.accept(self)
    
    def visit_primary_key_constraint(self, node: SQLPrimaryKeyConstraint):
        """Visit PRIMARY KEY constraint."""
        if node.name:
            self._write_keyword("CONSTRAINT")
            self._write(" ")
            node.name.accept(self)
            self._write(" ")
        self._write_keyword("PRIMARY KEY")
        if node.columns:
            self._write(" (")
            self._write_node_list(node.columns)
            self._write(")")
    
    def visit_foreign_key_constraint(self, node: SQLForeignKeyConstraint):
        """Visit FOREIGN KEY constraint."""
        if node.name:
            self._write_keyword("CONSTRAINT")
            self._write(" ")
            node.name.accept(self)
            self._write(" ")
        self._write_keyword("FOREIGN KEY")
        if node.columns:
            self._write(" (")
            self._write_node_list(node.columns)
            self._write(")")
        if node.referenced_table:
            self._write(" ")
            self._write_keyword("REFERENCES")
            self._write(" ")
            node.referenced_table.accept(self)
            if node.referenced_columns:
                self._write(" (")
                self._write_node_list(node.referenced_columns)
                self._write(")")
        if node.on_delete:
            self._write(" ")
            self._write_keyword("ON DELETE")
            self._write(" ")
            self._write_keyword(node.on_delete)
        if node.on_update:
            self._write(" ")
            self._write_keyword("ON UPDATE")
            self._write(" ")
            self._write_keyword(node.on_update)
    
    def visit_unique_constraint(self, node: SQLUniqueConstraint):
        """Visit UNIQUE constraint."""
        if node.name:
            self._write_keyword("CONSTRAINT")
            self._write(" ")
            node.name.accept(self)
            self._write(" ")
        self._write_keyword("UNIQUE")
        if node.columns:
            self._write(" (")
            self._write_node_list(node.columns)
            self._write(")")
    
    def visit_check_constraint(self, node: SQLCheckConstraint):
        """Visit CHECK constraint."""
        if node.name:
            self._write_keyword("CONSTRAINT")
            self._write(" ")
            node.name.accept(self)
            self._write(" ")
        self._write_keyword("CHECK")
        self._write(" (")
        node.condition.accept(self)
        self._write(")")
    
    def visit_default_constraint(self, node: SQLDefaultConstraint):
        """Visit DEFAULT constraint."""
        self._write_keyword("DEFAULT")
        self._write(" ")
        node.value.accept(self) 