#!/usr/bin/env python3
"""
SQL ↔ Runa Bidirectional Converter

Converts between SQL AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.

This module handles conversion between:
- SQL schema definitions ↔ Runa data structures
- SQL queries ↔ Runa data processing logic
- SQL constraints ↔ Runa validation rules
- SQL functions ↔ Runa procedures

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
import logging

from .sql_ast import *

# Import Runa AST nodes
from ....core.runa_ast import *


class SQLToRunaConverter:
    """
    Converts SQL AST to Runa AST.
    
    This converter transforms SQL constructs into their Runa equivalents:
    - Tables become data structures
    - Queries become data processing logic
    - Constraints become validation rules
    - Stored procedures become process definitions
    """
    
    def __init__(self):
        """Initialize the SQL to Runa converter."""
        self.logger = logging.getLogger(__name__)
        self.schema_context = {}  # Track table schemas
        self.type_mapping = self._build_type_mapping()
        self.operator_mapping = self._build_operator_mapping()
        self.function_mapping = self._build_function_mapping()
        self.current_scope = []  # Track current scope for variable resolution
    
    def _build_type_mapping(self) -> Dict[str, str]:
        """Build mapping from SQL types to Runa types."""
        return {
            # Integer types
            'INTEGER': 'Integer',
            'INT': 'Integer',
            'BIGINT': 'BigInteger',
            'SMALLINT': 'SmallInteger',
            'TINYINT': 'TinyInteger',
            
            # Floating point types
            'DECIMAL': 'Decimal',
            'NUMERIC': 'Decimal',
            'FLOAT': 'Float',
            'DOUBLE': 'Float',
            'REAL': 'Float',
            
            # String types
            'CHAR': 'String',
            'VARCHAR': 'String',
            'TEXT': 'String',
            'CLOB': 'String',
            
            # Binary types
            'BINARY': 'Bytes',
            'VARBINARY': 'Bytes',
            'BLOB': 'Bytes',
            
            # Date/time types
            'DATE': 'Date',
            'TIME': 'Time',
            'TIMESTAMP': 'DateTime',
            'INTERVAL': 'Duration',
            
            # Boolean type
            'BOOLEAN': 'Boolean',
            
            # JSON type
            'JSON': 'Json',
            
            # Array type
            'ARRAY': 'List',
            
            # UUID type
            'UUID': 'UUID',
        }
    
    def _build_operator_mapping(self) -> Dict[SQLOperator, BinaryOperator]:
        """Build mapping from SQL operators to Runa operators."""
        return {
            SQLOperator.PLUS: BinaryOperator.PLUS,
            SQLOperator.MINUS: BinaryOperator.MINUS,
            SQLOperator.MULTIPLY: BinaryOperator.MULTIPLY,
            SQLOperator.DIVIDE: BinaryOperator.DIVIDE,
            SQLOperator.MODULO: BinaryOperator.MODULO,
            SQLOperator.POWER: BinaryOperator.POWER,
            SQLOperator.EQUAL: BinaryOperator.EQUALS,
            SQLOperator.NOT_EQUAL: BinaryOperator.NOT_EQUALS,
            SQLOperator.GREATER_THAN: BinaryOperator.GREATER_THAN,
            SQLOperator.LESS_THAN: BinaryOperator.LESS_THAN,
            SQLOperator.GREATER_EQUAL: BinaryOperator.GREATER_EQUAL,
            SQLOperator.LESS_EQUAL: BinaryOperator.LESS_EQUAL,
            SQLOperator.AND: BinaryOperator.AND,
            SQLOperator.OR: BinaryOperator.OR,
            SQLOperator.CONCAT: BinaryOperator.FOLLOWED_BY,
        }
    
    def _build_function_mapping(self) -> Dict[str, str]:
        """Build mapping from SQL functions to Runa functions."""
        return {
            # Aggregate functions
            'COUNT': 'Count',
            'SUM': 'Sum',
            'AVG': 'Average',
            'MIN': 'Minimum',
            'MAX': 'Maximum',
            'STDDEV': 'StandardDeviation',
            'VARIANCE': 'Variance',
            
            # String functions
            'UPPER': 'ToUpperCase',
            'LOWER': 'ToLowerCase',
            'LENGTH': 'Length',
            'SUBSTRING': 'Substring',
            'TRIM': 'Trim',
            'LTRIM': 'TrimLeft',
            'RTRIM': 'TrimRight',
            'CONCAT': 'Concatenate',
            'REPLACE': 'Replace',
            'SPLIT': 'Split',
            
            # Date/time functions
            'NOW': 'CurrentDateTime',
            'CURRENT_DATE': 'CurrentDate',
            'CURRENT_TIME': 'CurrentTime',
            'CURRENT_TIMESTAMP': 'CurrentDateTime',
            'EXTRACT': 'ExtractDatePart',
            'DATE_ADD': 'AddToDate',
            'DATE_SUB': 'SubtractFromDate',
            'DATE_DIFF': 'DateDifference',
            
            # Math functions
            'ABS': 'Absolute',
            'CEIL': 'Ceiling',
            'FLOOR': 'Floor',
            'ROUND': 'Round',
            'SQRT': 'SquareRoot',
            'POWER': 'Power',
            'MOD': 'Modulo',
            'RANDOM': 'Random',
            
            # Conditional functions
            'CASE': 'ConditionalExpression',
            'COALESCE': 'FirstNonNull',
            'NULLIF': 'NullIf',
            'GREATEST': 'Maximum',
            'LEAST': 'Minimum',
            
            # Type conversion
            'CAST': 'ConvertTo',
            'CONVERT': 'ConvertTo',
            
            # JSON functions
            'JSON_EXTRACT': 'ExtractFromJson',
            'JSON_OBJECT': 'CreateJsonObject',
            'JSON_ARRAY': 'CreateJsonArray',
            'JSON_VALID': 'IsValidJson',
            
            # Array functions
            'ARRAY_LENGTH': 'ArrayLength',
            'ARRAY_CONTAINS': 'ArrayContains',
            'ARRAY_SLICE': 'ArraySlice',
            'ARRAY_APPEND': 'ArrayAppend',
            'ARRAY_PREPEND': 'ArrayPrepend',
        }
    
    def convert(self, sql_ast: SQLProgram) -> Program:
        """
        Convert SQL program to Runa program.
        
        Args:
            sql_ast: SQL AST to convert
            
        Returns:
            Program: Runa AST
        """
        statements = []
        
        # Process each SQL statement
        for stmt in sql_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements=statements)
    
    def convert_statement(self, stmt: SQLStatement) -> Union[Statement, List[Statement], None]:
        """Convert SQL statement to Runa statement(s)."""
        if isinstance(stmt, SQLSelectStatement):
            return self._convert_select_statement(stmt)
        elif isinstance(stmt, SQLInsertStatement):
            return self._convert_insert_statement(stmt)
        elif isinstance(stmt, SQLUpdateStatement):
            return self._convert_update_statement(stmt)
        elif isinstance(stmt, SQLDeleteStatement):
            return self._convert_delete_statement(stmt)
        elif isinstance(stmt, SQLCreateTableStatement):
            return self._convert_create_table_statement(stmt)
        elif isinstance(stmt, SQLDropTableStatement):
            return self._convert_drop_table_statement(stmt)
        elif isinstance(stmt, SQLAlterTableStatement):
            return self._convert_alter_table_statement(stmt)
        else:
            self.logger.warning(f"Unsupported SQL statement type: {type(stmt)}")
            return None
    
    def _convert_select_statement(self, stmt: SQLSelectStatement) -> List[Statement]:
        """Convert SELECT statement to Runa data processing logic."""
        statements = []
        
        # Create a process for the SELECT operation
        process_name = f"Query_{id(stmt)}"
        
        # Convert WHERE clause to filter condition
        filter_condition = None
        if stmt.where_clause:
            filter_condition = self.convert_expression(stmt.where_clause.condition)
        
        # Convert ORDER BY clause
        sort_expressions = []
        if stmt.order_by_clause:
            for order_expr in stmt.order_by_clause.expressions:
                sort_expr = self.convert_expression(order_expr.expression)
                sort_expressions.append(sort_expr)
        
        # Convert GROUP BY clause
        group_expressions = []
        if stmt.group_by_clause:
            for group_expr in stmt.group_by_clause.expressions:
                group_expr_converted = self.convert_expression(group_expr)
                group_expressions.append(group_expr_converted)
        
        # Convert HAVING clause
        having_condition = None
        if stmt.having_clause:
            having_condition = self.convert_expression(stmt.having_clause.condition)
        
        # Convert LIMIT clause
        limit_value = None
        if stmt.limit_clause:
            limit_value = self.convert_expression(stmt.limit_clause.count)
        
        # Convert select list
        select_expressions = []
        for expr in stmt.select_list:
            converted_expr = self.convert_expression(expr)
            select_expressions.append(converted_expr)
        
        # Create a process definition that represents the query
        process_body = []
        
        # Add data source processing
        if stmt.from_clause:
            for table_ref in stmt.from_clause.table_references:
                table_stmt = self._convert_table_reference(table_ref)
                if table_stmt:
                    process_body.append(table_stmt)
        
        # Add filtering
        if filter_condition:
            filter_stmt = LetStatement(
                identifier="filtered_data",
                value=FunctionCall(
                    function_name="Filter",
                    arguments=[("condition", filter_condition)]
                )
            )
            process_body.append(filter_stmt)
        
        # Add grouping
        if group_expressions:
            group_stmt = LetStatement(
                identifier="grouped_data",
                value=FunctionCall(
                    function_name="GroupBy",
                    arguments=[("expressions", ListLiteral(elements=group_expressions))]
                )
            )
            process_body.append(group_stmt)
        
        # Add having filter
        if having_condition:
            having_stmt = LetStatement(
                identifier="having_filtered_data",
                value=FunctionCall(
                    function_name="Filter",
                    arguments=[("condition", having_condition)]
                )
            )
            process_body.append(having_stmt)
        
        # Add sorting
        if sort_expressions:
            sort_stmt = LetStatement(
                identifier="sorted_data",
                value=FunctionCall(
                    function_name="SortBy",
                    arguments=[("expressions", ListLiteral(elements=sort_expressions))]
                )
            )
            process_body.append(sort_stmt)
        
        # Add projection
        if select_expressions:
            project_stmt = LetStatement(
                identifier="projected_data",
                value=FunctionCall(
                    function_name="Select",
                    arguments=[("expressions", ListLiteral(elements=select_expressions))]
                )
            )
            process_body.append(project_stmt)
        
        # Add limit
        if limit_value:
            limit_stmt = LetStatement(
                identifier="limited_data",
                value=FunctionCall(
                    function_name="Limit",
                    arguments=[("count", limit_value)]
                )
            )
            process_body.append(limit_stmt)
        
        # Return the result
        return_stmt = ReturnStatement(
            value=Identifier(name="limited_data") if limit_value else
                  Identifier(name="projected_data") if select_expressions else
                  Identifier(name="sorted_data") if sort_expressions else
                  Identifier(name="having_filtered_data") if having_condition else
                  Identifier(name="grouped_data") if group_expressions else
                  Identifier(name="filtered_data") if filter_condition else
                  Identifier(name="source_data")
        )
        process_body.append(return_stmt)
        
        # Create the process definition
        process = ProcessDeclaration(
            name=process_name,
            body=BlockStatement(statements=process_body),
            parameters=[],
            return_type=GenericType(base_type="List", type_args=[BasicType(name="Record")])
        )
        
        statements.append(process)
        
        return statements
    
    def _convert_insert_statement(self, stmt: SQLInsertStatement) -> List[Statement]:
        """Convert INSERT statement to Runa data insertion logic."""
        statements = []
        
        # Create a process for the INSERT operation
        process_name = f"Insert_{stmt.table.name}"
        
        # Create record construction
        record_fields = []
        
        if stmt.columns and stmt.values:
            # Handle explicit column specification
            for i, column in enumerate(stmt.columns):
                if i < len(stmt.values[0]):  # Use first value row
                    field_value = self.convert_expression(stmt.values[0][i])
                    record_fields.append((column.name, field_value))
        
        # Create record creation
        record_expr = DictionaryLiteral(
            pairs=[(StringLiteral(value=name), value) for name, value in record_fields]
        )
        
        # Create insertion logic
        insert_stmt = LetStatement(
            identifier="new_record",
            value=record_expr
        )
        statements.append(insert_stmt)
        
        # Create table insertion call
        table_insert = ExpressionStatement(
            expression=FunctionCall(
                function_name="InsertIntoTable",
                arguments=[
                    ("table", StringLiteral(value=stmt.table.name)),
                    ("record", Identifier(name="new_record"))
                ]
            )
        )
        statements.append(table_insert)
        
        return statements
    
    def _convert_update_statement(self, stmt: SQLUpdateStatement) -> List[Statement]:
        """Convert UPDATE statement to Runa data update logic."""
        statements = []
        
        # Create update logic
        update_fields = []
        for column, value in stmt.set_clauses:
            field_value = self.convert_expression(value)
            update_fields.append((column.name, field_value))
        
        # Create update record
        update_record = DictionaryLiteral(
            pairs=[(StringLiteral(value=name), value) for name, value in update_fields]
        )
        
        # Create where condition
        where_condition = None
        if stmt.where_clause:
            where_condition = self.convert_expression(stmt.where_clause.condition)
        
        # Create update call
        update_call = ExpressionStatement(
            expression=FunctionCall(
                function_name="UpdateTable",
                arguments=[
                    ("table", StringLiteral(value=stmt.table.name)),
                    ("updates", update_record),
                    ("condition", where_condition if where_condition else BooleanLiteral(value=True))
                ]
            )
        )
        statements.append(update_call)
        
        return statements
    
    def _convert_delete_statement(self, stmt: SQLDeleteStatement) -> List[Statement]:
        """Convert DELETE statement to Runa data deletion logic."""
        statements = []
        
        # Create where condition
        where_condition = None
        if stmt.where_clause:
            where_condition = self.convert_expression(stmt.where_clause.condition)
        
        # Create delete call
        delete_call = ExpressionStatement(
            expression=FunctionCall(
                function_name="DeleteFromTable",
                arguments=[
                    ("table", StringLiteral(value=stmt.table.name)),
                    ("condition", where_condition if where_condition else BooleanLiteral(value=True))
                ]
            )
        )
        statements.append(delete_call)
        
        return statements
    
    def _convert_create_table_statement(self, stmt: SQLCreateTableStatement) -> List[Statement]:
        """Convert CREATE TABLE statement to Runa structure definition."""
        statements = []
        
        # Create field definitions
        fields = []
        for column in stmt.columns:
            field_type = self._convert_data_type(column.data_type)
            
            # Handle constraints
            is_optional = True
            default_value = None
            
            for constraint in column.constraints:
                if constraint.constraint_type == ConstraintType.NOT_NULL:
                    is_optional = False
                elif constraint.constraint_type == ConstraintType.DEFAULT:
                    default_value = self.convert_expression(constraint.value)
            
            # Make type optional if nullable
            if is_optional and not isinstance(field_type, OptionalType):
                field_type = OptionalType(inner_type=field_type)
            
            field_def = FieldDefinition(
                name=column.name.name,
                type=field_type,
                default_value=default_value,
                is_required=not is_optional
            )
            fields.append(field_def)
        
        # Create structure definition
        struct_def = StructDefinition(
            name=stmt.table_name.name,
            fields=fields,
            is_data_structure=True
        )
        statements.append(struct_def)
        
        # Create table schema definition
        table_schema = LetStatement(
            identifier=f"{stmt.table_name.name}_schema",
            value=FunctionCall(
                function_name="CreateTableSchema",
                arguments=[
                    ("name", StringLiteral(value=stmt.table_name.name)),
                    ("structure", Identifier(name=stmt.table_name.name))
                ]
            )
        )
        statements.append(table_schema)
        
        # Store schema in context
        self.schema_context[stmt.table_name.name] = {
            'columns': {col.name.name: col for col in stmt.columns},
            'constraints': stmt.constraints
        }
        
        return statements
    
    def _convert_drop_table_statement(self, stmt: SQLDropTableStatement) -> List[Statement]:
        """Convert DROP TABLE statement to Runa table removal logic."""
        statements = []
        
        for table_name in stmt.table_names:
            drop_call = ExpressionStatement(
                expression=FunctionCall(
                    function_name="DropTable",
                    arguments=[("table", StringLiteral(value=table_name.name))]
                )
            )
            statements.append(drop_call)
            
            # Remove from schema context
            if table_name.name in self.schema_context:
                del self.schema_context[table_name.name]
        
        return statements
    
    def _convert_alter_table_statement(self, stmt: SQLAlterTableStatement) -> List[Statement]:
        """Convert ALTER TABLE statement to Runa table modification logic."""
        statements = []
        
        for action in stmt.actions:
            if isinstance(action, SQLAddColumnAction):
                # Add column
                add_call = ExpressionStatement(
                    expression=FunctionCall(
                        function_name="AddColumn",
                        arguments=[
                            ("table", StringLiteral(value=stmt.table_name.name)),
                            ("column", StringLiteral(value=action.column.name.name)),
                            ("type", StringLiteral(value=self._convert_data_type(action.column.data_type).name))
                        ]
                    )
                )
                statements.append(add_call)
            
            elif isinstance(action, SQLDropColumnAction):
                # Drop column
                drop_call = ExpressionStatement(
                    expression=FunctionCall(
                        function_name="DropColumn",
                        arguments=[
                            ("table", StringLiteral(value=stmt.table_name.name)),
                            ("column", StringLiteral(value=action.column_name.name))
                        ]
                    )
                )
                statements.append(drop_call)
        
        return statements
    
    def _convert_table_reference(self, table_ref: SQLTableReference) -> Optional[Statement]:
        """Convert table reference to Runa data source."""
        if isinstance(table_ref, SQLTableName):
            return LetStatement(
                identifier="source_data",
                value=FunctionCall(
                    function_name="LoadTable",
                    arguments=[("table", StringLiteral(value=table_ref.name.name))]
                )
            )
        elif isinstance(table_ref, SQLJoin):
            # Handle JOIN operations
            left_data = self._convert_table_reference(table_ref.left)
            right_data = self._convert_table_reference(table_ref.right)
            
            join_condition = None
            if table_ref.condition:
                join_condition = self.convert_expression(table_ref.condition)
            
            # Create join operation
            join_call = FunctionCall(
                function_name=f"{table_ref.join_type.value}Join",
                arguments=[
                    ("left", Identifier(name="left_data")),
                    ("right", Identifier(name="right_data")),
                    ("condition", join_condition if join_condition else BooleanLiteral(value=True))
                ]
            )
            
            return LetStatement(
                identifier="joined_data",
                value=join_call
            )
        elif isinstance(table_ref, SQLDerivedTable):
            # Handle subquery
            subquery_statements = self._convert_select_statement(table_ref.query)
            # Return the last statement which should be the process
            return subquery_statements[-1] if subquery_statements else None
        
        return None
    
    def convert_expression(self, expr: SQLExpression) -> Expression:
        """Convert SQL expression to Runa expression."""
        if isinstance(expr, SQLIntegerLiteral):
            return IntegerLiteral(value=expr.value)
        elif isinstance(expr, SQLFloatLiteral):
            return FloatLiteral(value=expr.value)
        elif isinstance(expr, SQLStringLiteral):
            return StringLiteral(value=expr.value)
        elif isinstance(expr, SQLBooleanLiteral):
            return BooleanLiteral(value=expr.value)
        elif isinstance(expr, SQLNullLiteral):
            return Identifier(name="null")
        elif isinstance(expr, SQLColumnReference):
            if expr.table:
                return MemberAccess(
                    object=Identifier(name=expr.table),
                    member=expr.column
                )
            else:
                return Identifier(name=expr.column)
        elif isinstance(expr, SQLBinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, SQLUnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, SQLFunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, SQLCaseExpression):
            return self._convert_case_expression(expr)
        elif isinstance(expr, SQLCastExpression):
            return self._convert_cast_expression(expr)
        elif isinstance(expr, SQLSubquery):
            # Convert subquery to a process call
            subquery_statements = self._convert_select_statement(expr.query)
            if subquery_statements:
                process_name = subquery_statements[-1].name
                return FunctionCall(
                    function_name=process_name,
                    arguments=[]
                )
            return Identifier(name="subquery_result")
        elif isinstance(expr, SQLInExpression):
            return self._convert_in_expression(expr)
        elif isinstance(expr, SQLBetweenExpression):
            return self._convert_between_expression(expr)
        elif isinstance(expr, SQLLikeExpression):
            return self._convert_like_expression(expr)
        elif isinstance(expr, SQLExistsExpression):
            return self._convert_exists_expression(expr)
        else:
            self.logger.warning(f"Unsupported SQL expression type: {type(expr)}")
            return Identifier(name="unsupported_expression")
    
    def _convert_binary_expression(self, expr: SQLBinaryExpression) -> Expression:
        """Convert SQL binary expression to Runa binary expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        runa_operator = self.operator_mapping.get(expr.operator, BinaryOperator.EQUALS)
        
        return BinaryExpression(
            left=left,
            operator=runa_operator,
            right=right
        )
    
    def _convert_unary_expression(self, expr: SQLUnaryExpression) -> Expression:
        """Convert SQL unary expression to Runa unary expression."""
        operand = self.convert_expression(expr.operand)
        
        operator_str = "not" if expr.operator == SQLOperator.NOT else str(expr.operator.value)
        
        return UnaryExpression(
            operator=operator_str,
            operand=operand
        )
    
    def _convert_function_call(self, expr: SQLFunctionCall) -> Expression:
        """Convert SQL function call to Runa function call."""
        function_name = self.function_mapping.get(expr.name.upper(), expr.name)
        
        arguments = []
        for i, arg in enumerate(expr.arguments):
            converted_arg = self.convert_expression(arg)
            arguments.append((f"arg{i}", converted_arg))
        
        return FunctionCall(
            function_name=function_name,
            arguments=arguments
        )
    
    def _convert_case_expression(self, expr: SQLCaseExpression) -> Expression:
        """Convert SQL CASE expression to Runa conditional expression."""
        conditions = []
        values = []
        
        for when_expr, then_expr in expr.when_clauses:
            condition = self.convert_expression(when_expr)
            value = self.convert_expression(then_expr)
            conditions.append(condition)
            values.append(value)
        
        else_value = None
        if expr.else_clause:
            else_value = self.convert_expression(expr.else_clause)
        
        # Create nested conditional expression
        result = else_value if else_value else Identifier(name="null")
        
        for condition, value in zip(reversed(conditions), reversed(values)):
            result = ConditionalExpression(
                condition=condition,
                true_expression=value,
                false_expression=result
            )
        
        return result
    
    def _convert_cast_expression(self, expr: SQLCastExpression) -> Expression:
        """Convert SQL CAST expression to Runa type conversion."""
        source_expr = self.convert_expression(expr.expression)
        target_type = self._convert_data_type(expr.target_type)
        
        return FunctionCall(
            function_name="ConvertTo",
            arguments=[
                ("value", source_expr),
                ("type", StringLiteral(value=target_type.name))
            ]
        )
    
    def _convert_in_expression(self, expr: SQLInExpression) -> Expression:
        """Convert SQL IN expression to Runa contains check."""
        value_expr = self.convert_expression(expr.expression)
        
        if len(expr.values) == 1 and isinstance(expr.values[0], SQLSubquery):
            # Subquery IN
            subquery_result = self.convert_expression(expr.values[0])
            return FunctionCall(
                function_name="Contains",
                arguments=[
                    ("collection", subquery_result),
                    ("value", value_expr)
                ]
            )
        else:
            # Value list IN
            value_list = ListLiteral(elements=[self.convert_expression(v) for v in expr.values])
            return FunctionCall(
                function_name="Contains",
                arguments=[
                    ("collection", value_list),
                    ("value", value_expr)
                ]
            )
    
    def _convert_between_expression(self, expr: SQLBetweenExpression) -> Expression:
        """Convert SQL BETWEEN expression to Runa range check."""
        value_expr = self.convert_expression(expr.expression)
        lower_expr = self.convert_expression(expr.lower_bound)
        upper_expr = self.convert_expression(expr.upper_bound)
        
        # Create: value >= lower AND value <= upper
        lower_check = BinaryExpression(
            left=value_expr,
            operator=BinaryOperator.GREATER_EQUAL,
            right=lower_expr
        )
        
        upper_check = BinaryExpression(
            left=value_expr,
            operator=BinaryOperator.LESS_EQUAL,
            right=upper_expr
        )
        
        return BinaryExpression(
            left=lower_check,
            operator=BinaryOperator.AND,
            right=upper_check
        )
    
    def _convert_like_expression(self, expr: SQLLikeExpression) -> Expression:
        """Convert SQL LIKE expression to Runa pattern matching."""
        value_expr = self.convert_expression(expr.expression)
        pattern_expr = self.convert_expression(expr.pattern)
        
        function_name = "MatchesPattern"
        if expr.case_insensitive:
            function_name = "MatchesPatternIgnoreCase"
        
        return FunctionCall(
            function_name=function_name,
            arguments=[
                ("value", value_expr),
                ("pattern", pattern_expr)
            ]
        )
    
    def _convert_exists_expression(self, expr: SQLExistsExpression) -> Expression:
        """Convert SQL EXISTS expression to Runa existence check."""
        subquery_result = self.convert_expression(expr.subquery)
        
        return FunctionCall(
            function_name="HasAnyResults",
            arguments=[("query", subquery_result)]
        )
    
    def _convert_data_type(self, data_type: SQLDataType) -> TypeExpression:
        """Convert SQL data type to Runa type expression."""
        if isinstance(data_type, SQLIntegerType):
            return BasicType(name="Integer")
        elif isinstance(data_type, SQLVarcharType):
            return BasicType(name="String")
        elif isinstance(data_type, SQLDecimalType):
            return BasicType(name="Decimal")
        elif isinstance(data_type, SQLArrayType):
            element_type = self._convert_data_type(data_type.element_type)
            return GenericType(base_type="List", type_args=[element_type])
        else:
            # Generic type mapping
            runa_type = self.type_mapping.get(data_type.name.upper(), data_type.name)
            return BasicType(name=runa_type)


class RunaToSQLConverter:
    """
    Converts Runa AST to SQL AST.
    
    This converter transforms Runa constructs into their SQL equivalents:
    - Data structures become tables
    - Data processing logic becomes queries
    - Validation rules become constraints
    - Process definitions become stored procedures
    """
    
    def __init__(self, dialect: SQLDialect = SQLDialect.ANSI):
        """Initialize the Runa to SQL converter."""
        self.dialect = dialect
        self.logger = logging.getLogger(__name__)
        self.type_mapping = self._build_type_mapping()
        self.operator_mapping = self._build_operator_mapping()
        self.function_mapping = self._build_function_mapping()
        self.current_tables = {}  # Track table schemas
        self.query_counter = 0
    
    def _build_type_mapping(self) -> Dict[str, str]:
        """Build mapping from Runa types to SQL types."""
        return {
            'Integer': 'INTEGER',
            'BigInteger': 'BIGINT',
            'SmallInteger': 'SMALLINT',
            'TinyInteger': 'TINYINT',
            'Decimal': 'DECIMAL',
            'Float': 'FLOAT',
            'String': 'VARCHAR',
            'Bytes': 'VARBINARY',
            'Date': 'DATE',
            'Time': 'TIME',
            'DateTime': 'TIMESTAMP',
            'Duration': 'INTERVAL',
            'Boolean': 'BOOLEAN',
            'Json': 'JSON',
            'UUID': 'UUID',
        }
    
    def _build_operator_mapping(self) -> Dict[BinaryOperator, SQLOperator]:
        """Build mapping from Runa operators to SQL operators."""
        return {
            BinaryOperator.PLUS: SQLOperator.PLUS,
            BinaryOperator.MINUS: SQLOperator.MINUS,
            BinaryOperator.MULTIPLY: SQLOperator.MULTIPLY,
            BinaryOperator.DIVIDE: SQLOperator.DIVIDE,
            BinaryOperator.MODULO: SQLOperator.MODULO,
            BinaryOperator.POWER: SQLOperator.POWER,
            BinaryOperator.EQUALS: SQLOperator.EQUAL,
            BinaryOperator.NOT_EQUALS: SQLOperator.NOT_EQUAL,
            BinaryOperator.GREATER_THAN: SQLOperator.GREATER_THAN,
            BinaryOperator.LESS_THAN: SQLOperator.LESS_THAN,
            BinaryOperator.GREATER_EQUAL: SQLOperator.GREATER_EQUAL,
            BinaryOperator.LESS_EQUAL: SQLOperator.LESS_EQUAL,
            BinaryOperator.AND: SQLOperator.AND,
            BinaryOperator.OR: SQLOperator.OR,
            BinaryOperator.FOLLOWED_BY: SQLOperator.CONCAT,
        }
    
    def _build_function_mapping(self) -> Dict[str, str]:
        """Build mapping from Runa functions to SQL functions."""
        return {
            'Count': 'COUNT',
            'Sum': 'SUM',
            'Average': 'AVG',
            'Minimum': 'MIN',
            'Maximum': 'MAX',
            'StandardDeviation': 'STDDEV',
            'Variance': 'VARIANCE',
            'ToUpperCase': 'UPPER',
            'ToLowerCase': 'LOWER',
            'Length': 'LENGTH',
            'Substring': 'SUBSTRING',
            'Trim': 'TRIM',
            'TrimLeft': 'LTRIM',
            'TrimRight': 'RTRIM',
            'Concatenate': 'CONCAT',
            'Replace': 'REPLACE',
            'Split': 'SPLIT',
            'CurrentDateTime': 'NOW',
            'CurrentDate': 'CURRENT_DATE',
            'CurrentTime': 'CURRENT_TIME',
            'ExtractDatePart': 'EXTRACT',
            'AddToDate': 'DATE_ADD',
            'SubtractFromDate': 'DATE_SUB',
            'DateDifference': 'DATE_DIFF',
            'Absolute': 'ABS',
            'Ceiling': 'CEIL',
            'Floor': 'FLOOR',
            'Round': 'ROUND',
            'SquareRoot': 'SQRT',
            'Power': 'POWER',
            'Modulo': 'MOD',
            'Random': 'RANDOM',
            'FirstNonNull': 'COALESCE',
            'NullIf': 'NULLIF',
            'ConvertTo': 'CAST',
            'ExtractFromJson': 'JSON_EXTRACT',
            'CreateJsonObject': 'JSON_OBJECT',
            'CreateJsonArray': 'JSON_ARRAY',
            'IsValidJson': 'JSON_VALID',
            'ArrayLength': 'ARRAY_LENGTH',
            'ArrayContains': 'ARRAY_CONTAINS',
            'ArraySlice': 'ARRAY_SLICE',
            'ArrayAppend': 'ARRAY_APPEND',
            'ArrayPrepend': 'ARRAY_PREPEND',
        }
    
    def convert(self, runa_ast: Program) -> SQLProgram:
        """
        Convert Runa program to SQL program.
        
        Args:
            runa_ast: Runa AST to convert
            
        Returns:
            SQLProgram: SQL AST
        """
        statements = []
        
        # Process each Runa statement
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return SQLProgram(statements=statements)
    
    def convert_statement(self, stmt: Statement) -> Union[SQLStatement, List[SQLStatement], None]:
        """Convert Runa statement to SQL statement(s)."""
        if isinstance(stmt, StructDefinition):
            return self._convert_struct_definition(stmt)
        elif isinstance(stmt, ProcessDeclaration):
            return self._convert_process_declaration(stmt)
        elif isinstance(stmt, ExpressionStatement):
            return self._convert_expression_statement(stmt)
        else:
            self.logger.warning(f"Unsupported Runa statement type: {type(stmt)}")
            return None
    
    def _convert_struct_definition(self, stmt: StructDefinition) -> SQLCreateTableStatement:
        """Convert Runa struct definition to SQL CREATE TABLE."""
        columns = []
        constraints = []
        
        for field in stmt.fields:
            # Convert field type
            sql_type = self._convert_type_expression(field.type)
            
            # Create column definition
            column_constraints = []
            
            # Handle NOT NULL constraint
            if field.is_required:
                column_constraints.append(
                    SQLConstraint(constraint_type=ConstraintType.NOT_NULL)
                )
            
            # Handle DEFAULT constraint
            if field.default_value:
                default_expr = self.convert_expression(field.default_value)
                column_constraints.append(
                    SQLDefaultConstraint(value=default_expr)
                )
            
            column_def = SQLColumnDefinition(
                name=SQLIdentifier(name=field.name),
                data_type=sql_type,
                constraints=column_constraints
            )
            columns.append(column_def)
        
        # Store table schema
        self.current_tables[stmt.name] = {
            'columns': {field.name: field for field in stmt.fields}
        }
        
        return SQLCreateTableStatement(
            table_name=SQLIdentifier(name=stmt.name),
            columns=columns,
            constraints=constraints
        )
    
    def _convert_process_declaration(self, stmt: ProcessDeclaration) -> Union[SQLStatement, List[SQLStatement]]:
        """Convert Runa process declaration to SQL query or stored procedure."""
        # Detect query-like processes first
        if self._is_query_process(stmt):
            return self._convert_query_process(stmt)
        # Otherwise convert to stored procedure
        return self._convert_stored_procedure(stmt)

    def _is_query_process(self, stmt: ProcessDeclaration) -> bool:
        """Check if a process is a query-like operation."""
        # Simple heuristic: if it has a return statement and uses data operations
        if not stmt.body or not isinstance(stmt.body, BlockStatement):
            return False
        
        has_return = any(isinstance(s, ReturnStatement) for s in stmt.body.statements)
        has_data_ops = any(
            isinstance(s, LetStatement) and isinstance(s.value, FunctionCall) and
            s.value.function_name in ['Filter', 'GroupBy', 'SortBy', 'Select', 'Join']
            for s in stmt.body.statements
        )
        
        return has_return and has_data_ops
    
    def _convert_query_process(self, stmt: ProcessDeclaration) -> SQLSelectStatement:
        """Convert query-like process to SELECT statement."""
        select_list = [SQLColumnReference(column="*")]  # Default to SELECT *
        from_clause = None
        where_clause = None
        group_by_clause = None
        having_clause = None
        order_by_clause = None
        limit_clause = None
        
        if isinstance(stmt.body, BlockStatement):
            for s in stmt.body.statements:
                if isinstance(s, LetStatement) and isinstance(s.value, FunctionCall):
                    func_call = s.value
                    
                    if func_call.function_name == "LoadTable":
                        # FROM clause
                        table_name = None
                        for arg_name, arg_value in func_call.arguments:
                            if arg_name == "table" and isinstance(arg_value, StringLiteral):
                                table_name = arg_value.value
                                break
                        
                        if table_name:
                            table_ref = SQLTableName(name=SQLIdentifier(name=table_name))
                            from_clause = SQLFromClause(table_references=[table_ref])
                    
                    elif func_call.function_name == "Filter":
                        # WHERE clause
                        for arg_name, arg_value in func_call.arguments:
                            if arg_name == "condition":
                                condition = self.convert_expression(arg_value)
                                where_clause = SQLWhereClause(condition=condition)
                                break
                    
                    elif func_call.function_name == "GroupBy":
                        # GROUP BY clause
                        for arg_name, arg_value in func_call.arguments:
                            if arg_name == "expressions" and isinstance(arg_value, ListLiteral):
                                group_exprs = [self.convert_expression(e) for e in arg_value.elements]
                                group_by_clause = SQLGroupByClause(expressions=group_exprs)
                                break
                    
                    elif func_call.function_name == "SortBy":
                        # ORDER BY clause
                        for arg_name, arg_value in func_call.arguments:
                            if arg_name == "expressions" and isinstance(arg_value, ListLiteral):
                                order_exprs = []
                                for e in arg_value.elements:
                                    converted_expr = self.convert_expression(e)
                                    order_expr = SQLOrderByExpression(expression=converted_expr)
                                    order_exprs.append(order_expr)
                                order_by_clause = SQLOrderByClause(expressions=order_exprs)
                                break
                    
                    elif func_call.function_name == "Select":
                        # SELECT clause
                        for arg_name, arg_value in func_call.arguments:
                            if arg_name == "expressions" and isinstance(arg_value, ListLiteral):
                                select_list = [self.convert_expression(e) for e in arg_value.elements]
                                break
                    
                    elif func_call.function_name == "Limit":
                        # LIMIT clause
                        for arg_name, arg_value in func_call.arguments:
                            if arg_name == "count":
                                count_expr = self.convert_expression(arg_value)
                                limit_clause = SQLLimitClause(count=count_expr)
                                break
        
        return SQLSelectStatement(
            select_list=select_list,
            from_clause=from_clause,
            where_clause=where_clause,
            group_by_clause=group_by_clause,
            having_clause=having_clause,
            order_by_clause=order_by_clause,
            limit_clause=limit_clause
        )
    
    def _convert_stored_procedure(self, stmt: ProcessDeclaration) -> SQLCreateProcedureStatement:
        """Convert a Runa ProcessDeclaration into a SQL stored procedure."""
        # Parameters
        parameters: List[SQLParameter] = []
        for param in stmt.parameters:
            sql_type = self._convert_type_expression(param.type_annotation) if param.type_annotation else SQLVarcharType()
            direction = self._get_parameter_direction(param)
            param_name = SQLIdentifier(name=param.name)
            parameters.append(SQLParameter(name=param_name, data_type=sql_type, direction=direction))

        # Convert body statements to SQL
        body_sql: List[SQLStatement] = []
        if isinstance(stmt.body, BlockStatement):
            for s in stmt.body.statements:
                converted = self.convert_statement(s)
                if converted:
                    if isinstance(converted, list):
                        body_sql.extend(converted)
                    else:
                        body_sql.append(converted)

        proc_stmt = SQLCreateProcedureStatement(
            name=SQLIdentifier(name=stmt.name),
            parameters=parameters,
            body=body_sql,
            return_type=None  # Runa processes can have return; we may map later
        )
        return proc_stmt

    def _get_parameter_direction(self, param: 'Parameter') -> str:
        """
        Determine parameter direction (IN/OUT/INOUT) from annotations or naming conventions.
        
        Args:
            param: Function parameter to analyze
            
        Returns:
            Parameter direction as string: "IN", "OUT", or "INOUT"
        """
        # Check for explicit annotations first
        if hasattr(param, 'annotations') and param.annotations:
            for annotation in param.annotations:
                if hasattr(annotation, 'name'):
                    if annotation.name.lower() in ['out', 'output']:
                        return "OUT"
                    elif annotation.name.lower() in ['inout', 'in_out', 'bidirectional']:
                        return "INOUT"
        
        # Check parameter name for conventions
        param_name = param.name.lower()
        if param_name.startswith('out_') or param_name.endswith('_out'):
            return "OUT"
        elif param_name.startswith('inout_') or param_name.endswith('_inout'):
            return "INOUT"
        elif 'result' in param_name or 'output' in param_name:
            return "OUT"
        
        # Check type annotation for direction hints
        if hasattr(param, 'type_annotation') and param.type_annotation:
            type_str = str(param.type_annotation).lower()
            if 'output' in type_str or 'result' in type_str:
                return "OUT"
            elif 'inout' in type_str or 'bidirectional' in type_str:
                return "INOUT"
        
        # Default to IN parameter
        return "IN"

    # Helper to convert Runa TypeExpression to SQLDataType
    def _convert_type_expression(self, type_expr: TypeExpression) -> SQLDataType:
        if isinstance(type_expr, BasicType):
            mapping = {
                "Integer": SQLIntegerType(),
                "Float": SQLFloatType(),
                "String": SQLVarcharType(length=255),
                "Boolean": SQLBooleanType(),
            }
            return mapping.get(type_expr.name, SQLVarcharType(length=255))
        # Fallback
        return SQLVarcharType(length=255)
    
    def _convert_expression_statement(self, stmt: ExpressionStatement) -> Optional[SQLStatement]:
        """Convert Runa expression statement to SQL statement."""
        if isinstance(stmt.expression, FunctionCall):
            func_call = stmt.expression
            
            if func_call.function_name == "InsertIntoTable":
                return self._convert_insert_function(func_call)
            elif func_call.function_name == "UpdateTable":
                return self._convert_update_function(func_call)
            elif func_call.function_name == "DeleteFromTable":
                return self._convert_delete_function(func_call)
            elif func_call.function_name == "DropTable":
                return self._convert_drop_table_function(func_call)
        
        return None
    
    def _convert_insert_function(self, func_call: FunctionCall) -> SQLInsertStatement:
        """Convert InsertIntoTable function to INSERT statement."""
        table_name = None
        record_data = None
        
        for arg_name, arg_value in func_call.arguments:
            if arg_name == "table" and isinstance(arg_value, StringLiteral):
                table_name = arg_value.value
            elif arg_name == "record" and isinstance(arg_value, (DictionaryLiteral, Identifier)):
                record_data = arg_value
        
        if not table_name:
            return None
        
        # Convert record to column values
        columns = []
        values = []
        
        if isinstance(record_data, DictionaryLiteral):
            for key_expr, value_expr in record_data.pairs:
                if isinstance(key_expr, StringLiteral):
                    columns.append(SQLIdentifier(name=key_expr.value))
                    values.append(self.convert_expression(value_expr))
        
        return SQLInsertStatement(
            table=SQLIdentifier(name=table_name),
            columns=columns,
            values=[values] if values else []
        )
    
    def _convert_update_function(self, func_call: FunctionCall) -> SQLUpdateStatement:
        """Convert UpdateTable function to UPDATE statement."""
        table_name = None
        updates = None
        condition = None
        
        for arg_name, arg_value in func_call.arguments:
            if arg_name == "table" and isinstance(arg_value, StringLiteral):
                table_name = arg_value.value
            elif arg_name == "updates":
                updates = arg_value
            elif arg_name == "condition":
                condition = arg_value
        
        if not table_name:
            return None
        
        # Convert updates to SET clauses
        set_clauses = []
        if isinstance(updates, DictionaryLiteral):
            for key_expr, value_expr in updates.pairs:
                if isinstance(key_expr, StringLiteral):
                    column = SQLIdentifier(name=key_expr.value)
                    value = self.convert_expression(value_expr)
                    set_clauses.append((column, value))
        
        # Convert condition to WHERE clause
        where_clause = None
        if condition and not (isinstance(condition, BooleanLiteral) and condition.value):
            where_condition = self.convert_expression(condition)
            where_clause = SQLWhereClause(condition=where_condition)
        
        return SQLUpdateStatement(
            table=SQLIdentifier(name=table_name),
            set_clauses=set_clauses,
            where_clause=where_clause
        )
    
    def _convert_delete_function(self, func_call: FunctionCall) -> SQLDeleteStatement:
        """Convert DeleteFromTable function to DELETE statement."""
        table_name = None
        condition = None
        
        for arg_name, arg_value in func_call.arguments:
            if arg_name == "table" and isinstance(arg_value, StringLiteral):
                table_name = arg_value.value
            elif arg_name == "condition":
                condition = arg_value
        
        if not table_name:
            return None
        
        # Convert condition to WHERE clause
        where_clause = None
        if condition and not (isinstance(condition, BooleanLiteral) and condition.value):
            where_condition = self.convert_expression(condition)
            where_clause = SQLWhereClause(condition=where_condition)
        
        return SQLDeleteStatement(
            table=SQLIdentifier(name=table_name),
            where_clause=where_clause
        )
    
    def _convert_drop_table_function(self, func_call: FunctionCall) -> SQLDropTableStatement:
        """Convert DropTable function to DROP TABLE statement."""
        table_name = None
        
        for arg_name, arg_value in func_call.arguments:
            if arg_name == "table" and isinstance(arg_value, StringLiteral):
                table_name = arg_value.value
                break
        
        if not table_name:
            return None
        
        return SQLDropTableStatement(
            table_names=[SQLIdentifier(name=table_name)]
        )
    
    def convert_expression(self, expr: Expression) -> SQLExpression:
        """Convert Runa expression to SQL expression."""
        if isinstance(expr, IntegerLiteral):
            return SQLIntegerLiteral(value=expr.value)
        elif isinstance(expr, FloatLiteral):
            return SQLFloatLiteral(value=expr.value)
        elif isinstance(expr, StringLiteral):
            return SQLStringLiteral(value=expr.value)
        elif isinstance(expr, BooleanLiteral):
            return SQLBooleanLiteral(value=expr.value)
        elif isinstance(expr, Identifier):
            if expr.name == "null":
                return SQLNullLiteral()
            else:
                return SQLColumnReference(column=expr.name)
        elif isinstance(expr, MemberAccess):
            if isinstance(expr.object, Identifier):
                return SQLColumnReference(table=expr.object.name, column=expr.member)
            else:
                # Complex member access
                return SQLColumnReference(column=expr.member)
        elif isinstance(expr, BinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, UnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, ConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list_literal(expr)
        else:
            self.logger.warning(f"Unsupported Runa expression type: {type(expr)}")
            return SQLColumnReference(column="unsupported_expression")
    
    def _convert_binary_expression(self, expr: BinaryExpression) -> SQLExpression:
        """Convert Runa binary expression to SQL binary expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        sql_operator = self.operator_mapping.get(expr.operator, SQLOperator.EQUAL)
        
        return SQLBinaryExpression(
            left=left,
            operator=sql_operator,
            right=right
        )
    
    def _convert_unary_expression(self, expr: UnaryExpression) -> SQLExpression:
        """Convert Runa unary expression to SQL unary expression."""
        operand = self.convert_expression(expr.operand)
        
        if expr.operator == "not":
            sql_operator = SQLOperator.NOT
        else:
            sql_operator = SQLOperator.PLUS  # Default
        
        return SQLUnaryExpression(
            operator=sql_operator,
            operand=operand
        )
    
    def _convert_function_call(self, expr: FunctionCall) -> SQLExpression:
        """Convert Runa function call to SQL function call."""
        sql_function_name = self.function_mapping.get(expr.function_name, expr.function_name)
        
        arguments = []
        for arg_name, arg_value in expr.arguments:
            converted_arg = self.convert_expression(arg_value)
            arguments.append(converted_arg)
        
        return SQLFunctionCall(
            name=sql_function_name,
            arguments=arguments
        )
    
    def _convert_conditional_expression(self, expr: ConditionalExpression) -> SQLExpression:
        """Convert Runa conditional expression to SQL CASE expression."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.true_expression)
        false_expr = self.convert_expression(expr.false_expression)
        
        return SQLCaseExpression(
            expression=None,  # Searched CASE
            when_clauses=[(condition, true_expr)],
            else_clause=false_expr
        )
    
    def _convert_list_literal(self, expr: ListLiteral) -> SQLExpression:
        """Convert Runa list literal to SQL array or values list."""
        elements = [self.convert_expression(e) for e in expr.elements]
        
        if self.dialect in [SQLDialect.POSTGRESQL, SQLDialect.MYSQL]:
            # Use ARRAY constructor
            return SQLArrayConstructor(elements=elements)
        else:
            # Use VALUES clause or function call
            return SQLFunctionCall(
                name="VALUES",
                arguments=elements
            )


def sql_to_runa(sql_ast) -> 'Program':
    """Convert SQL AST to Runa AST."""
    converter = SQLToRunaConverter()
    return converter.convert(sql_ast)


def runa_to_sql(runa_ast: 'Program'):
    """Convert Runa AST to SQL AST."""
    converter = RunaToSQLConverter()
    return converter.convert(runa_ast)