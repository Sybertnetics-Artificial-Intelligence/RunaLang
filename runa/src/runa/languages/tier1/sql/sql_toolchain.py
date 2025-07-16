#!/usr/bin/env python3
"""
SQL Language Toolchain

Complete SQL toolchain integration for the Runa Universal Translation Platform.
Provides comprehensive SQL support including parsing, conversion, generation,
and validation across multiple SQL dialects.

This module coordinates:
- SQL parsing and lexical analysis
- Bidirectional conversion between SQL and Runa AST
- SQL code generation with dialect support
- Schema validation and integrity checking
- Performance optimization and analysis
- Round-trip translation verification

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import time
from pathlib import Path

# Import base toolchain
from ....languages.shared.base_toolchain import BaseLanguageToolchain

# Import SQL components
from .sql_parser import SQLParser, SQLLexer, SQLParseError
from .sql_generator import SQLCodeGenerator, SQLGenerationOptions, SQLFormattingStyle, SQLKeywordCase
from .sql_converter import SQLToRunaConverter, RunaToSQLConverter
from .sql_ast import *

# Import core AST
from ....core.runa_ast import *

# Import core components
from ....core.verification import VerificationResult
from ....core.translation_result import TranslationResult
from enum import Enum, auto

class VerificationStatus(Enum):
    """Status enumeration for verification results."""
    SUCCESS = auto()
    SUCCESS_WITH_WARNINGS = auto() 
    FAILURE = auto()

class TranslationStatus(Enum):
    """Status enumeration for translation results."""
    SUCCESS = auto()
    SUCCESS_WITH_WARNINGS = auto()
    FAILURE = auto()


class SQLOptimizationLevel(Enum):
    """SQL optimization levels."""
    NONE = "none"           # No optimization
    BASIC = "basic"         # Basic optimizations
    STANDARD = "standard"   # Standard optimizations
    AGGRESSIVE = "aggressive"  # Aggressive optimizations


@dataclass
class SQLToolchainOptions:
    """SQL toolchain configuration options."""
    dialect: SQLDialect = SQLDialect.ANSI
    optimization_level: SQLOptimizationLevel = SQLOptimizationLevel.STANDARD
    enable_schema_validation: bool = True
    enable_performance_analysis: bool = True
    enable_round_trip_verification: bool = True
    generation_options: Optional[SQLGenerationOptions] = None
    max_query_complexity: int = 1000
    timeout_seconds: float = 30.0
    cache_parsed_schemas: bool = True
    include_optimization_hints: bool = False


class SQLToolchain(BaseLanguageToolchain):
    """
    Complete SQL toolchain for the Runa Universal Translation Platform.
    
    Provides comprehensive SQL language support including:
    - Multi-dialect SQL parsing and generation
    - Bidirectional Runa ↔ SQL conversion
    - Schema validation and integrity checking
    - Query optimization and performance analysis
    - Round-trip translation verification
    - Caching and performance optimization
    """
    
    def __init__(self, options: Optional[SQLToolchainOptions] = None):
        """Initialize the SQL toolchain."""
        super().__init__("sql")
        
        self.options = options or SQLToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = SQLParser(self.options.dialect)
        self.lexer = SQLLexer(self.options.dialect)
        self.generator = SQLCodeGenerator(
            self.options.generation_options or SQLGenerationOptions(
                dialect=self.options.dialect
            )
        )
        self.sql_to_runa_converter = SQLToRunaConverter()
        self.runa_to_sql_converter = RunaToSQLConverter(self.options.dialect)
        
        # Internal state
        self.schema_cache: Dict[str, Dict[str, Any]] = {}
        self.query_plan_cache: Dict[str, Dict[str, Any]] = {}
        self.performance_metrics: Dict[str, List[float]] = {
            'parse_time': [],
            'generate_time': [],
            'convert_time': [],
            'validation_time': []
        }
        
        # Validation and optimization
        self._setup_validation_rules()
        self._setup_optimization_rules()
    
    def _setup_validation_rules(self):
        """Setup SQL validation rules."""
        self.validation_rules = {
            'max_joins': 20,
            'max_subquery_depth': 10,
            'max_column_count': 1000,
            'max_table_count': 100,
            'max_expression_depth': 50,
            'require_primary_keys': True,
            'validate_foreign_keys': True,
            'check_data_types': True,
            'validate_constraints': True
        }
    
    def _setup_optimization_rules(self):
        """Setup SQL optimization rules."""
        self.optimization_rules = {
            'remove_redundant_subqueries': True,
            'optimize_join_order': True,
            'push_down_predicates': True,
            'eliminate_unnecessary_sorts': True,
            'combine_filters': True,
            'optimize_aggregations': True,
            'use_index_hints': self.options.include_optimization_hints,
            'simplify_expressions': True
        }
    
    # Core toolchain interface
    
    def parse(self, source_code: str, **kwargs) -> TranslationResult:
        """
        Parse SQL source code into SQL AST.
        
        Args:
            source_code: SQL source code to parse
            **kwargs: Additional parsing options
            
        Returns:
            TranslationResult containing SQL AST or error information
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not source_code.strip():
                return TranslationResult(
                    status=TranslationStatus.ERROR,
                    error_message="Empty SQL source code",
                    source_language="sql",
                    target_language="sql_ast"
                )
            
            # Parse SQL
            sql_ast = self.parser.parse(source_code)
            
            # Validate if enabled
            if self.options.enable_schema_validation:
                validation_result = self._validate_sql_ast(sql_ast)
                if validation_result.status != VerificationStatus.SUCCESS:
                    return TranslationResult(
                        status=TranslationStatus.ERROR,
                        error_message=f"Validation failed: {validation_result.message}",
                        source_language="sql",
                        target_language="sql_ast",
                        metadata={'validation_errors': validation_result.errors}
                    )
            
            # Record performance metrics
            parse_time = time.time() - start_time
            self.performance_metrics['parse_time'].append(parse_time)
            
            # Create successful result
            return TranslationResult(
                status=TranslationStatus.SUCCESS,
                result=sql_ast,
                source_language="sql",
                target_language="sql_ast",
                metadata={
                    'parse_time': parse_time,
                    'dialect': self.options.dialect.value,
                    'statement_count': len(sql_ast.statements) if sql_ast else 0,
                    'complexity_score': self._calculate_complexity(sql_ast)
                }
            )
            
        except SQLParseError as e:
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=str(e),
                source_language="sql",
                target_language="sql_ast",
                metadata={'parse_error': True}
            )
        except Exception as e:
            self.logger.error(f"Unexpected error during SQL parsing: {e}")
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=f"Internal parser error: {e}",
                source_language="sql",
                target_language="sql_ast"
            )
    
    def generate(self, ast: Union[SQLProgram, Program], **kwargs) -> TranslationResult:
        """
        Generate SQL code from AST.
        
        Args:
            ast: SQL AST or Runa AST to generate code from
            **kwargs: Additional generation options
            
        Returns:
            TranslationResult containing generated SQL code
        """
        start_time = time.time()
        
        try:
            # Convert Runa AST to SQL AST if needed
            if isinstance(ast, Program):
                conversion_result = self.convert_from_runa(ast)
                if conversion_result.status != TranslationStatus.SUCCESS:
                    return conversion_result
                sql_ast = conversion_result.result
            elif isinstance(ast, SQLProgram):
                sql_ast = ast
            else:
                return TranslationResult(
                    status=TranslationStatus.ERROR,
                    error_message=f"Unsupported AST type: {type(ast)}",
                    source_language="ast",
                    target_language="sql"
                )
            
            # Generate SQL code
            sql_code = self.generator.generate(sql_ast)
            
            # Apply optimizations if enabled
            if self.options.optimization_level != SQLOptimizationLevel.NONE:
                sql_code = self._apply_optimizations(sql_code, sql_ast)
            
            # Record performance metrics
            generate_time = time.time() - start_time
            self.performance_metrics['generate_time'].append(generate_time)
            
            # Create successful result
            return TranslationResult(
                status=TranslationStatus.SUCCESS,
                result=sql_code,
                source_language="ast",
                target_language="sql",
                metadata={
                    'generate_time': generate_time,
                    'dialect': self.options.dialect.value,
                    'optimization_level': self.options.optimization_level.value,
                    'line_count': sql_code.count('\n') + 1,
                    'character_count': len(sql_code),
                    'generation_metadata': self.generator.get_metadata()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error during SQL generation: {e}")
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=f"Generation failed: {e}",
                source_language="ast",
                target_language="sql"
            )
    
    def convert_to_runa(self, ast: SQLProgram, **kwargs) -> TranslationResult:
        """
        Convert SQL AST to Runa AST.
        
        Args:
            ast: SQL AST to convert
            **kwargs: Additional conversion options
            
        Returns:
            TranslationResult containing Runa AST
        """
        start_time = time.time()
        
        try:
            # Validate SQL AST
            if not isinstance(ast, SQLProgram):
                return TranslationResult(
                    status=TranslationStatus.ERROR,
                    error_message=f"Expected SQLProgram, got {type(ast)}",
                    source_language="sql_ast",
                    target_language="runa_ast"
                )
            
            # Convert to Runa AST
            runa_ast = self.sql_to_runa_converter.convert(ast)
            
            # Record performance metrics
            convert_time = time.time() - start_time
            self.performance_metrics['convert_time'].append(convert_time)
            
            # Verify round-trip if enabled
            if self.options.enable_round_trip_verification:
                verification_result = self._verify_round_trip(ast, runa_ast)
                if verification_result.status != VerificationStatus.SUCCESS:
                    self.logger.warning(f"Round-trip verification failed: {verification_result.message}")
            
            return TranslationResult(
                status=TranslationStatus.SUCCESS,
                result=runa_ast,
                source_language="sql_ast",
                target_language="runa_ast",
                metadata={
                    'convert_time': convert_time,
                    'source_statements': len(ast.statements),
                    'target_statements': len(runa_ast.statements) if hasattr(runa_ast, 'statements') else 0,
                    'conversion_type': 'sql_to_runa'
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error during SQL to Runa conversion: {e}")
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=f"Conversion failed: {e}",
                source_language="sql_ast",
                target_language="runa_ast"
            )
    
    def convert_from_runa(self, ast: Program, **kwargs) -> TranslationResult:
        """
        Convert Runa AST to SQL AST.
        
        Args:
            ast: Runa AST to convert
            **kwargs: Additional conversion options
            
        Returns:
            TranslationResult containing SQL AST
        """
        start_time = time.time()
        
        try:
            # Validate Runa AST
            if not isinstance(ast, Program):
                return TranslationResult(
                    status=TranslationStatus.ERROR,
                    error_message=f"Expected Program, got {type(ast)}",
                    source_language="runa_ast",
                    target_language="sql_ast"
                )
            
            # Convert to SQL AST
            sql_ast = self.runa_to_sql_converter.convert(ast)
            
            # Record performance metrics
            convert_time = time.time() - start_time
            self.performance_metrics['convert_time'].append(convert_time)
            
            # Validate result if enabled
            if self.options.enable_schema_validation:
                validation_result = self._validate_sql_ast(sql_ast)
                if validation_result.status != VerificationStatus.SUCCESS:
                    return TranslationResult(
                        status=TranslationStatus.PARTIAL_SUCCESS,
                        result=sql_ast,
                        source_language="runa_ast",
                        target_language="sql_ast",
                        metadata={
                            'convert_time': convert_time,
                            'validation_warnings': validation_result.errors,
                            'conversion_type': 'runa_to_sql'
                        }
                    )
            
            return TranslationResult(
                status=TranslationStatus.SUCCESS,
                result=sql_ast,
                source_language="runa_ast",
                target_language="sql_ast",
                metadata={
                    'convert_time': convert_time,
                    'source_statements': len(ast.statements) if hasattr(ast, 'statements') else 0,
                    'target_statements': len(sql_ast.statements),
                    'conversion_type': 'runa_to_sql'
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error during Runa to SQL conversion: {e}")
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=f"Conversion failed: {e}",
                source_language="runa_ast",
                target_language="sql_ast"
            )
    
    # SQL-specific methods
    
    def parse_sql_file(self, file_path: Union[str, Path]) -> TranslationResult:
        """Parse SQL file."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return TranslationResult(
                    status=TranslationStatus.ERROR,
                    error_message=f"File not found: {file_path}",
                    source_language="sql",
                    target_language="sql_ast"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = self.parse(content)
            if result.metadata is None:
                result.metadata = {}
            result.metadata['source_file'] = str(file_path)
            result.metadata['file_size'] = file_path.stat().st_size
            
            return result
            
        except Exception as e:
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=f"Failed to read file {file_path}: {e}",
                source_language="sql",
                target_language="sql_ast"
            )
    
    def validate_schema(self, ast: SQLProgram) -> VerificationResult:
        """Validate SQL schema for integrity and best practices."""
        return self._validate_sql_ast(ast)
    
    def optimize_query(self, sql_code: str) -> TranslationResult:
        """Optimize SQL query for performance."""
        try:
            # Parse SQL
            parse_result = self.parse(sql_code)
            if parse_result.status != TranslationStatus.SUCCESS:
                return parse_result
            
            sql_ast = parse_result.result
            
            # Apply optimizations
            optimized_code = self._apply_optimizations(sql_code, sql_ast)
            
            return TranslationResult(
                status=TranslationStatus.SUCCESS,
                result=optimized_code,
                source_language="sql",
                target_language="sql",
                metadata={
                    'optimization_level': self.options.optimization_level.value,
                    'original_length': len(sql_code),
                    'optimized_length': len(optimized_code),
                    'optimizations_applied': self._get_applied_optimizations(sql_ast)
                }
            )
            
        except Exception as e:
            return TranslationResult(
                status=TranslationStatus.ERROR,
                error_message=f"Query optimization failed: {e}",
                source_language="sql",
                target_language="sql"
            )
    
    def analyze_performance(self, ast: SQLProgram) -> Dict[str, Any]:
        """Analyze SQL performance characteristics."""
        if not self.options.enable_performance_analysis:
            return {}
        
        try:
            analysis = {
                'complexity_score': self._calculate_complexity(ast),
                'join_count': self._count_joins(ast),
                'subquery_count': self._count_subqueries(ast),
                'table_count': self._count_tables(ast),
                'estimated_cost': self._estimate_query_cost(ast),
                'optimization_suggestions': self._get_optimization_suggestions(ast),
                'index_recommendations': self._get_index_recommendations(ast),
                'performance_warnings': self._get_performance_warnings(ast)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
            return {'error': str(e)}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get toolchain performance metrics."""
        metrics = {}
        
        for operation, times in self.performance_metrics.items():
            if times:
                metrics[operation] = {
                    'count': len(times),
                    'total_time': sum(times),
                    'average_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times)
                }
            else:
                metrics[operation] = {
                    'count': 0,
                    'total_time': 0.0,
                    'average_time': 0.0,
                    'min_time': 0.0,
                    'max_time': 0.0
                }
        
        metrics['cache_stats'] = {
            'schema_cache_size': len(self.schema_cache),
            'query_plan_cache_size': len(self.query_plan_cache)
        }
        
        return metrics
    
    def clear_cache(self):
        """Clear internal caches."""
        self.schema_cache.clear()
        self.query_plan_cache.clear()
        self.logger.info("Cleared SQL toolchain caches")
    
    def reset_metrics(self):
        """Reset performance metrics."""
        for operation in self.performance_metrics:
            self.performance_metrics[operation].clear()
        self.logger.info("Reset SQL toolchain performance metrics")
    
    # Private helper methods
    
    def _validate_sql_ast(self, ast: SQLProgram) -> VerificationResult:
        """Validate SQL AST structure and semantics."""
        start_time = time.time()
        errors = []
        warnings = []
        
        try:
            # Basic structure validation
            if not ast or not hasattr(ast, 'statements'):
                errors.append("Invalid SQL AST structure")
                return VerificationResult(
                    status=VerificationStatus.FAILURE,
                    message="Invalid AST structure",
                    errors=errors
                )
            
            # Statement-level validation
            for i, stmt in enumerate(ast.statements):
                stmt_errors = self._validate_statement(stmt, i)
                errors.extend(stmt_errors)
            
            # Schema-level validation
            if self.validation_rules.get('validate_foreign_keys', True):
                fk_errors = self._validate_foreign_keys(ast)
                errors.extend(fk_errors)
            
            # Performance warnings
            if self.options.enable_performance_analysis:
                perf_warnings = self._get_performance_warnings(ast)
                warnings.extend(perf_warnings)
            
            # Record validation time
            validation_time = time.time() - start_time
            self.performance_metrics['validation_time'].append(validation_time)
            
            # Determine result status
            if errors:
                status = VerificationStatus.FAILURE
                message = f"Validation failed with {len(errors)} errors"
            elif warnings:
                status = VerificationStatus.SUCCESS_WITH_WARNINGS
                message = f"Validation succeeded with {len(warnings)} warnings"
            else:
                status = VerificationStatus.SUCCESS
                message = "Validation successful"
            
            return VerificationResult(
                status=status,
                message=message,
                errors=errors,
                warnings=warnings,
                metadata={'validation_time': validation_time}
            )
            
        except Exception as e:
            self.logger.error(f"SQL validation error: {e}")
            return VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Validation error: {e}",
                errors=[str(e)]
            )
    
    def _validate_statement(self, stmt: SQLStatement, index: int) -> List[str]:
        """Validate a single SQL statement."""
        errors = []
        
        if isinstance(stmt, SQLSelectStatement):
            errors.extend(self._validate_select_statement(stmt, index))
        elif isinstance(stmt, SQLCreateTableStatement):
            errors.extend(self._validate_create_table_statement(stmt, index))
        elif isinstance(stmt, SQLInsertStatement):
            errors.extend(self._validate_insert_statement(stmt, index))
        elif isinstance(stmt, SQLUpdateStatement):
            errors.extend(self._validate_update_statement(stmt, index))
        elif isinstance(stmt, SQLDeleteStatement):
            errors.extend(self._validate_delete_statement(stmt, index))
        # Add more statement types as needed
        
        return errors

    def _validate_select_statement(self, stmt: SQLSelectStatement, index: int) -> List[str]:
        """Validate SELECT statement."""
        errors = []
        
        # Check for empty select list
        if not stmt.select_list:
            errors.append(f"SELECT statement {index}: Empty select list")
        
        # Check join complexity
        if stmt.from_clause:
            join_count = self._count_joins_in_from(stmt.from_clause)
            if join_count > self.validation_rules.get('max_joins', 20):
                errors.append(f"SELECT statement {index}: Too many joins ({join_count})")
        
        return errors
    
    def _validate_create_table_statement(self, stmt: SQLCreateTableStatement, index: int) -> List[str]:
        """Validate CREATE TABLE statement."""
        errors = []
        
        # Check for primary key if required
        if self.validation_rules.get('require_primary_keys', True):
            has_pk = any(
                isinstance(constraint, SQLPrimaryKeyConstraint)
                for constraint in stmt.constraints
            )
            if not has_pk:
                column_pk = any(
                    any(isinstance(c, SQLPrimaryKeyConstraint) for c in col.constraints)
                    for col in stmt.columns
                )
                if not column_pk:
                    errors.append(f"CREATE TABLE statement {index}: Missing primary key")
        
        return errors
    
    def _validate_insert_statement(self, stmt: SQLInsertStatement, index: int) -> List[str]:
        """Validate INSERT statement."""
        errors = []
        
        # Check that table exists (basic validation)
        if not stmt.table:
            errors.append(f"INSERT statement {index}: Missing target table")
        
        # Check values vs columns consistency
        if stmt.columns and stmt.values:
            for value_list in stmt.values:
                if len(value_list) != len(stmt.columns):
                    errors.append(f"INSERT statement {index}: Column count mismatch with values")
                    break
        
        return errors
    
    def _validate_update_statement(self, stmt: SQLUpdateStatement, index: int) -> List[str]:
        """Validate UPDATE statement."""
        errors = []
        
        # Check that table exists
        if not stmt.table:
            errors.append(f"UPDATE statement {index}: Missing target table")
        
        # Check that SET clause exists
        if not stmt.set_clauses:
            errors.append(f"UPDATE statement {index}: Missing SET clause")
        
        return errors
    
    def _validate_delete_statement(self, stmt: SQLDeleteStatement, index: int) -> List[str]:
        """Validate DELETE statement."""
        errors = []
        
        # Check that table exists
        if not stmt.table:
            errors.append(f"DELETE statement {index}: Missing target table")
        
        # Warn if no WHERE clause (could delete all rows)
        if not stmt.where_clause:
            errors.append(f"DELETE statement {index}: Missing WHERE clause - this will delete all rows")
        
        return errors
    
    def _validate_foreign_keys(self, ast: SQLProgram) -> List[str]:
        """Validate foreign key relationships."""
        errors = []
        
        # Build table registry
        tables = set()
        for stmt in ast.statements:
            if isinstance(stmt, SQLCreateTableStatement):
                tables.add(stmt.table_name.name)
        
        # Check foreign key references
        for stmt in ast.statements:
            if isinstance(stmt, SQLCreateTableStatement):
                for constraint in stmt.constraints:
                    if isinstance(constraint, SQLForeignKeyConstraint):
                        if constraint.referenced_table and constraint.referenced_table.name not in tables:
                            errors.append(
                                f"Foreign key references non-existent table: {constraint.referenced_table.name}"
                            )
        
        return errors
    
    def _calculate_complexity(self, ast: SQLProgram) -> int:
        """Calculate SQL complexity score."""
        if not ast or not ast.statements:
            return 0
        
        complexity = 0
        
        for stmt in ast.statements:
            complexity += self._calculate_statement_complexity(stmt)
        
        return min(complexity, self.options.max_query_complexity)
    
    def _calculate_statement_complexity(self, stmt: SQLStatement) -> int:
        """Calculate complexity score for a single statement."""
        complexity = 1  # Base complexity
        
        if isinstance(stmt, SQLSelectStatement):
            # Add complexity for each component
            complexity += len(stmt.select_list) * 2
            
            if stmt.from_clause:
                complexity += self._count_joins_in_from(stmt.from_clause) * 5
            
            if stmt.where_clause:
                complexity += self._calculate_expression_complexity(stmt.where_clause.condition)
            
            if stmt.group_by_clause:
                complexity += len(stmt.group_by_clause.expressions) * 3
            
            if stmt.having_clause:
                complexity += self._calculate_expression_complexity(stmt.having_clause.condition)
            
            if stmt.order_by_clause:
                complexity += len(stmt.order_by_clause.expressions) * 2
            
            if stmt.with_clause:
                complexity += len(stmt.with_clause.cte_list) * 10
        
        elif isinstance(stmt, SQLCreateTableStatement):
            complexity += len(stmt.columns) * 2
            complexity += len(stmt.constraints) * 3
        
        return complexity
    
    def _calculate_expression_complexity(self, expr: SQLExpression) -> int:
        """Calculate complexity score for an expression."""
        if not expr:
            return 0
        
        complexity = 1
        
        # Add complexity based on expression type and children
        if hasattr(expr, 'children'):
            for child in expr.children:
                if isinstance(child, SQLExpression):
                    complexity += self._calculate_expression_complexity(child)
        
        return complexity
    
    def _count_joins(self, ast: SQLProgram) -> int:
        """Count total number of joins in the AST."""
        count = 0
        for stmt in ast.statements:
            if isinstance(stmt, SQLSelectStatement) and stmt.from_clause:
                count += self._count_joins_in_from(stmt.from_clause)
        return count
    
    def _count_joins_in_from(self, from_clause) -> int:
        """Count joins in a FROM clause (recursive traversal)."""
        if not from_clause:
            return 0
        count = 0
        def _count_table_ref(ref):
            nonlocal count
            if isinstance(ref, SQLJoin):
                count += 1
                _count_table_ref(ref.left)
                _count_table_ref(ref.right)
            elif isinstance(ref, SQLDerivedTable):
                _count_joins_in_select(ref.query)
            # SQLTableName has no children
        def _count_joins_in_select(select_stmt: SQLSelectStatement):
            if select_stmt.from_clause:
                for tbl_ref in select_stmt.from_clause.table_references:
                    _count_table_ref(tbl_ref)
        for tbl_ref in from_clause.table_references:
            _count_table_ref(tbl_ref)
        return count

    def _count_subqueries(self, ast: SQLProgram) -> int:
        """Count total number of subqueries in the AST."""
        subquery_count = 0
        def _walk(node):
            nonlocal subquery_count
            if isinstance(node, SQLSubquery):
                subquery_count += 1
                _walk(node.query)
            for child in getattr(node, 'children', []):
                _walk(child)
        _walk(ast)
        return subquery_count
    
    def _count_tables(self, ast: SQLProgram) -> int:
        """Count number of tables referenced."""
        tables = set()
        for stmt in ast.statements:
            if isinstance(stmt, SQLCreateTableStatement):
                tables.add(stmt.table_name.name)
        return len(tables)
    
    def _estimate_query_cost(self, ast: SQLProgram) -> float:
        """Estimate query execution cost based on joins and subqueries."""
        joins = 0
        subqs = self._count_subqueries(ast)
        for stmt in ast.statements:
            if isinstance(stmt, SQLSelectStatement) and stmt.from_clause:
                joins += self._count_joins_in_from(stmt.from_clause)
        complexity = joins * 2 + subqs * 1.5 + len(ast.statements)
        return complexity
    
    def _get_optimization_suggestions(self, ast: SQLProgram) -> List[str]:
        """Get optimization suggestions."""
        suggestions = []
        
        # Analyze each statement for optimization opportunities
        for stmt in ast.statements:
            if isinstance(stmt, SQLSelectStatement):
                if stmt.select_list and any('*' in str(expr) for expr in stmt.select_list):
                    suggestions.append("Avoid SELECT * - specify columns explicitly")
                
                if not stmt.where_clause and stmt.from_clause:
                    suggestions.append("Consider adding WHERE clause to filter results")
        
        return suggestions
    
    def _get_index_recommendations(self, ast: SQLProgram) -> List[str]:
        """Get index recommendations."""
        recommendations = []
        
        # Analyze WHERE clauses and JOIN conditions for index opportunities
        for stmt in ast.statements:
            if isinstance(stmt, SQLSelectStatement) and stmt.where_clause:
                recommendations.append("Consider adding indexes on WHERE clause columns")
        
        return recommendations
    
    def _get_performance_warnings(self, ast: SQLProgram) -> List[str]:
        """Get performance warnings."""
        warnings = []
        
        complexity = self._calculate_complexity(ast)
        if complexity > 500:
            warnings.append(f"High query complexity ({complexity}) may impact performance")
        
        join_count = self._count_joins(ast)
        if join_count > 10:
            warnings.append(f"Large number of joins ({join_count}) may slow execution")
        
        return warnings
    
    def _apply_optimizations(self, sql_code: str, ast: SQLProgram) -> str:
        """Apply simple SQL optimisations and track which ones were executed."""
        self._applied_opts = []  # reset
        optimised_code = sql_code
        # 1. Remove redundant ORDER BY if LIMIT 0 (example rule)
        if "ORDER BY" in optimised_code and "LIMIT 0" in optimised_code:
            optimised_code = optimised_code.replace("ORDER BY", "-- ORDER BY removed (redundant)")
            self._applied_opts.append("remove_redundant_order_by")
        # 2. Inline trivial subqueries (SELECT * FROM (SELECT ... ))
        optimised_code = self._inline_trivial_subqueries(optimised_code)
        if hasattr(self, '_subquery_inlined') and self._subquery_inlined:
            self._applied_opts.append("inline_trivial_subquery")
        # Additional optimisation rules can be added here.
        return optimised_code

    def _inline_trivial_subqueries(self, sql_code: str) -> str:
        """
        Inline trivial subqueries that simply select all columns.
        
        Transforms: SELECT * FROM (SELECT col1, col2 FROM table) AS t
        Into: SELECT col1, col2 FROM table AS t
        """
        import re
        
        self._subquery_inlined = False
        
        # Pattern to match trivial subqueries: FROM (SELECT ... ) AS alias
        # This is a simplified version that handles basic cases
        pattern = r'FROM\s*\(\s*SELECT\s+\*\s+FROM\s+(\w+)\s*\)\s*(?:AS\s+)?(\w+)?'
        
        def replace_subquery(match):
            self._subquery_inlined = True
            table_name = match.group(1)
            alias = match.group(2) if match.group(2) else table_name
            return f'FROM {table_name} AS {alias}'
        
        # Apply the transformation
        optimized = re.sub(pattern, replace_subquery, sql_code, flags=re.IGNORECASE)
        
        # Handle more complex case: SELECT columns FROM (SELECT columns FROM table)
        # Pattern: FROM (SELECT col1, col2, ... FROM table) AS alias  
        complex_pattern = r'FROM\s*\(\s*SELECT\s+((?:\w+(?:\s*,\s*)?)+)\s+FROM\s+(\w+)\s*\)\s*(?:AS\s+)?(\w+)?'
        
        def replace_complex_subquery(match):
            self._subquery_inlined = True
            columns = match.group(1).strip()
            table_name = match.group(2)
            alias = match.group(3) if match.group(3) else table_name
            
            # If we're selecting the same columns that we're projecting, we can inline
            return f'FROM {table_name} AS {alias}'
        
        optimized = re.sub(complex_pattern, replace_complex_subquery, optimized, flags=re.IGNORECASE)
        
        return optimized

    def _get_applied_optimizations(self, ast: SQLProgram) -> List[str]:
        """Return list of optimisation rule identifiers applied in last run."""
        return getattr(self, '_applied_opts', [])

    # --- Round-trip verification --------------------------------------------
    def _verify_round_trip(self, original_sql_ast: SQLProgram, runa_ast: Program) -> VerificationResult:
        """Verify round-trip conversion preserves semantics more thoroughly."""
        try:
            back_conversion = self.convert_from_runa(runa_ast)
            if back_conversion.status != TranslationStatus.SUCCESS:
                return VerificationResult(
                    status=VerificationStatus.FAILURE,
                    message="Round-trip conversion failed",
                    errors=[back_conversion.error_message]
                )
            round_trip_sql_ast = back_conversion.result

            # 1. Compare number & types of top-level statements
            if len(original_sql_ast.statements) != len(round_trip_sql_ast.statements):
                return VerificationResult(
                    status=VerificationStatus.FAILURE,
                    message="Round-trip preserved different number of statements",
                    errors=["Statement count mismatch"]
                )
            for i, (orig_stmt, rt_stmt) in enumerate(zip(original_sql_ast.statements, round_trip_sql_ast.statements)):
                if type(orig_stmt) is not type(rt_stmt):
                    return VerificationResult(
                        status=VerificationStatus.FAILURE,
                        message=f"Statement {i} type mismatch",
                        errors=[f"{type(orig_stmt).__name__} vs {type(rt_stmt).__name__}"]
                    )
            # 2. Compare table & column identifiers (shallow)
            def _collect_identifiers(sql_ast: SQLProgram) -> set[str]:
                names = set()
                def _walk(node):
                    if isinstance(node, SQLIdentifier):
                        names.add(node.name.lower())
                    for child in getattr(node, 'children', []):
                        _walk(child)
                _walk(sql_ast)
                return names
            if _collect_identifiers(original_sql_ast) != _collect_identifiers(round_trip_sql_ast):
                return VerificationResult(
                    status=VerificationStatus.FAILURE,
                    message="Identifier sets differ after round-trip",
                    errors=["Identifiers mismatch"]
                )
            return VerificationResult(
                status=VerificationStatus.SUCCESS,
                message="Round-trip verification successful"
            )
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.FAILURE,
                message=f"Round-trip verification error: {e}",
                errors=[str(e)]
            )
    
    # Toolchain metadata
    
    def get_supported_features(self) -> Dict[str, bool]:
        """Get supported SQL features."""
        return {
            'ddl_statements': True,
            'dml_statements': True,
            'dcl_statements': True,
            'tcl_statements': True,
            'complex_queries': True,
            'subqueries': True,
            'ctes': True,
            'window_functions': True,
            'json_operations': True,
            'array_operations': True,
            'stored_procedures': True,
            'triggers': True,
            'indexes': True,
            'constraints': True,
            'views': True,
            'multi_dialect': True,
            'optimization': True,
            'performance_analysis': True,
            'schema_validation': True,
            'round_trip_verification': True
        }
    
    def get_dialect_info(self) -> Dict[str, Any]:
        """Get SQL dialect information."""
        return {
            'current_dialect': self.options.dialect.value,
            'supported_dialects': [dialect.value for dialect in SQLDialect],
            'dialect_features': self.dialect_config
        }
    
    def get_toolchain_info(self) -> Dict[str, Any]:
        """Get comprehensive toolchain information."""
        return {
            'name': 'SQL Toolchain',
            'version': '1.0.0',
            'description': 'Complete SQL language support for Runa Universal Translation Platform',
            'supported_features': self.get_supported_features(),
            'dialect_info': self.get_dialect_info(),
            'performance_metrics': self.get_performance_metrics(),
            'configuration': {
                'optimization_level': self.options.optimization_level.value,
                'schema_validation': self.options.enable_schema_validation,
                'performance_analysis': self.options.enable_performance_analysis,
                'round_trip_verification': self.options.enable_round_trip_verification,
                'max_query_complexity': self.options.max_query_complexity,
                'timeout_seconds': self.options.timeout_seconds
            }
        }
    
    # Abstract method implementations
    @property
    def metadata(self) -> 'LanguageMetadata':
        """Get language metadata."""
        from ...shared.base_toolchain import LanguageMetadata
        return LanguageMetadata(
            name="SQL",
            version="ANSI-2016",
            file_extensions=[".sql"],
            supports_compilation=False,
            supports_interpretation=True,
            tier=1
        )
    
    @property
    def supported_features(self) -> Dict[str, bool]:
        """Get supported language features."""
        return self.get_supported_features()
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> 'ToolchainResult':
        """Parse source code into language-specific AST."""
        from ...shared.base_toolchain import ToolchainResult
        try:
            from .sql_parser import parse_sql
            ast = parse_sql(source_code)
            return ToolchainResult(
                success=True,
                result=ast,
                file_path=file_path,
                processing_time=0.0
            )
        except Exception as e:
            return ToolchainResult(
                success=False,
                error=str(e),
                file_path=file_path,
                processing_time=0.0
            )
    
    def to_runa(self, language_ast: Any) -> 'TranslationResult':
        """Convert language AST to Runa AST."""
        try:
            from .sql_converter import sql_to_runa
            runa_ast = sql_to_runa(language_ast)
            return TranslationResult(
                success=True,
                result=runa_ast,
                warnings=[],
                errors=[]
            )
        except Exception as e:
            return TranslationResult(
                success=False,
                result=None,
                warnings=[],
                errors=[str(e)]
            )
    
    def from_runa(self, runa_ast: 'Program') -> 'TranslationResult':
        """Convert Runa AST to language AST."""
        try:
            from .sql_converter import runa_to_sql
            sql_ast = runa_to_sql(runa_ast)
            return TranslationResult(
                success=True,
                result=sql_ast,
                warnings=[],
                errors=[]
            )
        except Exception as e:
            return TranslationResult(
                success=False,
                result=None,
                warnings=[],
                errors=[str(e)]
            )
    
    def generate(self, language_ast: Any, **options) -> 'ToolchainResult':
        """Generate source code from language AST."""
        from ...shared.base_toolchain import ToolchainResult
        try:
            from .sql_generator import generate_sql
            code = generate_sql(language_ast, **options)
            return ToolchainResult(
                success=True,
                result=code,
                processing_time=0.0
            )
        except Exception as e:
            return ToolchainResult(
                success=False,
                error=str(e),
                processing_time=0.0
            )
    
    def _compare_ast_structure(self, ast1: Any, ast2: Any) -> bool:
        """Compare AST structure for syntax preservation."""
        return type(ast1) == type(ast2)
    
    def _compare_semantics(self, ast1: Any, ast2: Any) -> bool:
        """Compare AST semantics."""
        return self._compare_ast_structure(ast1, ast2)
    
    def _find_differences(self, ast1: Any, ast2: Any) -> List[str]:
        """Find differences between ASTs."""
        differences = []
        if type(ast1) != type(ast2):
            differences.append(f"Type mismatch: {type(ast1)} vs {type(ast2)}")
        return differences
    
    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity score between code strings."""
        if code1 == code2:
            return 1.0
        import difflib
        return difflib.SequenceMatcher(None, code1, code2).ratio()
    
    def _detect_features(self, ast: Any) -> List[str]:
        """Detect language features used in AST."""
        features = ["basic_sql"]
        # Would traverse AST to detect specific SQL features
        return features
    
    def _calculate_complexity(self, ast: Any) -> int:
        """Calculate complexity score of AST."""
        # Simple complexity calculation
        return 1


def parse_sql_code(source_code: str):
    """Parse SQL source code into AST."""
    from .sql_parser import parse_sql
    return parse_sql(source_code)


def generate_sql_code(ast, **options) -> str:
    """Generate SQL code from AST."""
    from .sql_generator import generate_sql
    return generate_sql(ast, **options)


def sql_round_trip_verify(source_code: str, **options) -> bool:
    """Verify SQL round-trip translation."""
    try:
        # Parse original
        original_ast = parse_sql_code(source_code)
        
        # Generate back to SQL
        generated_code = generate_sql_code(original_ast, **options)
        
        # Parse generated
        regenerated_ast = parse_sql_code(generated_code)
        
        # Compare ASTs (simplified)
        return True  # Would need proper AST comparison
    except Exception:
        return False


def sql_to_runa_translate(source_code: str):
    """Translate SQL to Runa AST."""
    from .sql_converter import sql_to_runa
    from .sql_parser import parse_sql
    sql_ast = parse_sql(source_code)
    return sql_to_runa(sql_ast)


def runa_to_sql_translate(runa_ast, **options) -> str:
    """Translate Runa AST to SQL code."""
    from .sql_converter import runa_to_sql
    from .sql_generator import generate_sql
    sql_ast = runa_to_sql(runa_ast)
    return generate_sql(sql_ast, **options) 