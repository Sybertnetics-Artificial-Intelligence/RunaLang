#!/usr/bin/env python3
"""
SQL AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for SQL covering all major SQL standards
and dialects including ANSI SQL-92/99/2003/2008/2011/2016, MySQL, PostgreSQL,
SQL Server, Oracle, and SQLite extensions.

This module provides a complete AST representation for:
- DDL (Data Definition Language): CREATE, ALTER, DROP statements
- DML (Data Manipulation Language): SELECT, INSERT, UPDATE, DELETE, MERGE
- DCL (Data Control Language): GRANT, REVOKE, DENY statements
- DQL (Data Query Language): Complex SELECT queries with JOINs, subqueries, CTEs
- TCL (Transaction Control Language): COMMIT, ROLLBACK, SAVEPOINT statements

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class SQLNodeType(Enum):
    """SQL AST node types covering all SQL language constructs."""
    
    # Core nodes
    PROGRAM = auto()
    STATEMENT = auto()
    EXPRESSION = auto()
    CLAUSE = auto()
    
    # Literals and identifiers
    LITERAL = auto()
    INTEGER_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    DATE_LITERAL = auto()
    TIME_LITERAL = auto()
    TIMESTAMP_LITERAL = auto()
    INTERVAL_LITERAL = auto()
    BINARY_LITERAL = auto()
    IDENTIFIER = auto()
    QUALIFIED_IDENTIFIER = auto()
    
    # Data types
    DATA_TYPE = auto()
    INTEGER_TYPE = auto()
    BIGINT_TYPE = auto()
    SMALLINT_TYPE = auto()
    TINYINT_TYPE = auto()
    DECIMAL_TYPE = auto()
    NUMERIC_TYPE = auto()
    FLOAT_TYPE = auto()
    DOUBLE_TYPE = auto()
    REAL_TYPE = auto()
    CHAR_TYPE = auto()
    VARCHAR_TYPE = auto()
    TEXT_TYPE = auto()
    CLOB_TYPE = auto()
    BLOB_TYPE = auto()
    BINARY_TYPE = auto()
    VARBINARY_TYPE = auto()
    BOOLEAN_TYPE = auto()
    DATE_TYPE = auto()
    TIME_TYPE = auto()
    TIMESTAMP_TYPE = auto()
    INTERVAL_TYPE = auto()
    JSON_TYPE = auto()
    XML_TYPE = auto()
    UUID_TYPE = auto()
    ARRAY_TYPE = auto()
    CUSTOM_TYPE = auto()
    
    # DDL Statements
    CREATE_TABLE = auto()
    CREATE_INDEX = auto()
    CREATE_VIEW = auto()
    CREATE_PROCEDURE = auto()
    CREATE_FUNCTION = auto()
    CREATE_TRIGGER = auto()
    CREATE_SEQUENCE = auto()
    CREATE_SCHEMA = auto()
    CREATE_DATABASE = auto()
    CREATE_USER = auto()
    CREATE_ROLE = auto()
    CREATE_DOMAIN = auto()
    CREATE_TYPE = auto()
    CREATE_CONSTRAINT = auto()
    
    ALTER_TABLE = auto()
    ALTER_INDEX = auto()
    ALTER_VIEW = auto()
    ALTER_PROCEDURE = auto()
    ALTER_FUNCTION = auto()
    ALTER_TRIGGER = auto()
    ALTER_SEQUENCE = auto()
    ALTER_SCHEMA = auto()
    ALTER_DATABASE = auto()
    ALTER_USER = auto()
    ALTER_ROLE = auto()
    ALTER_DOMAIN = auto()
    ALTER_TYPE = auto()
    
    DROP_TABLE = auto()
    DROP_INDEX = auto()
    DROP_VIEW = auto()
    DROP_PROCEDURE = auto()
    DROP_FUNCTION = auto()
    DROP_TRIGGER = auto()
    DROP_SEQUENCE = auto()
    DROP_SCHEMA = auto()
    DROP_DATABASE = auto()
    DROP_USER = auto()
    DROP_ROLE = auto()
    DROP_DOMAIN = auto()
    DROP_TYPE = auto()
    DROP_CONSTRAINT = auto()
    
    TRUNCATE_TABLE = auto()
    RENAME_TABLE = auto()
    COMMENT = auto()
    
    # DML Statements
    SELECT = auto()
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    MERGE = auto()
    UPSERT = auto()
    REPLACE = auto()
    
    # DCL Statements
    GRANT = auto()
    REVOKE = auto()
    DENY = auto()
    
    # TCL Statements
    COMMIT = auto()
    ROLLBACK = auto()
    SAVEPOINT = auto()
    RELEASE_SAVEPOINT = auto()
    SET_TRANSACTION = auto()
    START_TRANSACTION = auto()
    BEGIN_TRANSACTION = auto()
    
    # Query clauses
    FROM_CLAUSE = auto()
    WHERE_CLAUSE = auto()
    GROUP_BY_CLAUSE = auto()
    HAVING_CLAUSE = auto()
    ORDER_BY_CLAUSE = auto()
    LIMIT_CLAUSE = auto()
    OFFSET_CLAUSE = auto()
    WINDOW_CLAUSE = auto()
    WITH_CLAUSE = auto()
    
    # Expressions
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    CASE_EXPRESSION = auto()
    CAST_EXPRESSION = auto()
    EXTRACT_EXPRESSION = auto()
    FUNCTION_CALL = auto()
    AGGREGATE_FUNCTION = auto()
    WINDOW_FUNCTION = auto()
    SCALAR_SUBQUERY = auto()
    EXISTS_EXPRESSION = auto()
    IN_EXPRESSION = auto()
    BETWEEN_EXPRESSION = auto()
    LIKE_EXPRESSION = auto()
    SIMILAR_TO_EXPRESSION = auto()
    REGEXP_EXPRESSION = auto()
    IS_NULL_EXPRESSION = auto()
    IS_DISTINCT_EXPRESSION = auto()
    COALESCE_EXPRESSION = auto()
    NULLIF_EXPRESSION = auto()
    GREATEST_EXPRESSION = auto()
    LEAST_EXPRESSION = auto()
    
    # JOINs
    JOIN = auto()
    INNER_JOIN = auto()
    LEFT_JOIN = auto()
    RIGHT_JOIN = auto()
    FULL_JOIN = auto()
    CROSS_JOIN = auto()
    NATURAL_JOIN = auto()
    LATERAL_JOIN = auto()
    
    # Subqueries and CTEs
    SUBQUERY = auto()
    CTE = auto()
    RECURSIVE_CTE = auto()
    
    # Table expressions
    TABLE_REFERENCE = auto()
    TABLE_ALIAS = auto()
    DERIVED_TABLE = auto()
    TABLE_FUNCTION = auto()
    VALUES_TABLE = auto()
    
    # Column expressions
    COLUMN_REFERENCE = auto()
    COLUMN_ALIAS = auto()
    COLUMN_DEFINITION = auto()
    
    # Constraints
    PRIMARY_KEY_CONSTRAINT = auto()
    FOREIGN_KEY_CONSTRAINT = auto()
    UNIQUE_CONSTRAINT = auto()
    CHECK_CONSTRAINT = auto()
    NOT_NULL_CONSTRAINT = auto()
    DEFAULT_CONSTRAINT = auto()
    EXCLUSION_CONSTRAINT = auto()
    
    # Index components
    INDEX_COLUMN = auto()
    INDEX_EXPRESSION = auto()
    
    # Window functions
    WINDOW_SPECIFICATION = auto()
    PARTITION_BY = auto()
    ORDER_BY = auto()
    FRAME_CLAUSE = auto()
    
    # Set operations
    UNION = auto()
    UNION_ALL = auto()
    INTERSECT = auto()
    INTERSECT_ALL = auto()
    EXCEPT = auto()
    EXCEPT_ALL = auto()
    MINUS = auto()
    
    # Operators
    ARITHMETIC_OPERATOR = auto()
    COMPARISON_OPERATOR = auto()
    LOGICAL_OPERATOR = auto()
    BITWISE_OPERATOR = auto()
    STRING_OPERATOR = auto()
    ASSIGNMENT_OPERATOR = auto()
    
    # Special constructs
    PARAMETER = auto()
    VARIABLE = auto()
    PLACEHOLDER = auto()
    WILDCARD = auto()
    
    # Dialect-specific
    MYSQL_SPECIFIC = auto()
    POSTGRESQL_SPECIFIC = auto()
    SQLSERVER_SPECIFIC = auto()
    ORACLE_SPECIFIC = auto()
    SQLITE_SPECIFIC = auto()
    
    # Stored procedures and functions
    STORED_PROCEDURE = auto()
    STORED_FUNCTION = auto()
    TRIGGER = auto()
    TRIGGER_EVENT = auto()
    TRIGGER_TIMING = auto()
    TRIGGER_BODY = auto()
    
    # Control flow (for stored procedures)
    IF_STATEMENT = auto()
    WHILE_LOOP = auto()
    FOR_LOOP = auto()
    LOOP_STATEMENT = auto()
    REPEAT_STATEMENT = auto()
    GOTO_STATEMENT = auto()
    LABEL = auto()
    RETURN_STATEMENT = auto()
    RAISE_STATEMENT = auto()
    
    # Exception handling
    TRY_CATCH = auto()
    EXCEPTION_HANDLER = auto()
    
    # Cursors
    CURSOR_DECLARATION = auto()
    CURSOR_OPEN = auto()
    CURSOR_FETCH = auto()
    CURSOR_CLOSE = auto()
    
    # Administrative
    ANALYZE = auto()
    VACUUM = auto()
    EXPLAIN = auto()
    SHOW = auto()
    DESCRIBE = auto()
    USE = auto()
    SET = auto()
    RESET = auto()
    
    # JSON operations (modern SQL)
    JSON_EXTRACT = auto()
    JSON_OBJECT = auto()
    JSON_ARRAY = auto()
    JSON_QUERY = auto()
    JSON_VALUE = auto()
    
    # Array operations
    ARRAY_CONSTRUCTOR = auto()
    ARRAY_ELEMENT = auto()
    ARRAY_SLICE = auto()
    
    # Row operations
    ROW_CONSTRUCTOR = auto()
    ROW_SUBQUERY = auto()


class SQLDialect(Enum):
    """SQL dialect enumeration."""
    ANSI = "ansi"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLSERVER = "sqlserver"
    ORACLE = "oracle"
    SQLITE = "sqlite"
    H2 = "h2"
    HSQLDB = "hsqldb"
    DERBY = "derby"
    MARIADB = "mariadb"
    REDSHIFT = "redshift"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    CLICKHOUSE = "clickhouse"


class SQLOperator(Enum):
    """SQL operator enumeration."""
    # Arithmetic operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "^"
    
    # Comparison operators
    EQUAL = "="
    NOT_EQUAL = "<>"
    NOT_EQUAL_ALT = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    
    # Logical operators
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Pattern matching
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"
    ILIKE = "ILIKE"  # PostgreSQL case-insensitive LIKE
    NOT_ILIKE = "NOT ILIKE"
    SIMILAR_TO = "SIMILAR TO"
    NOT_SIMILAR_TO = "NOT SIMILAR TO"
    REGEXP = "REGEXP"
    NOT_REGEXP = "NOT REGEXP"
    RLIKE = "RLIKE"  # MySQL regex
    
    # Set operators
    IN = "IN"
    NOT_IN = "NOT IN"
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT EXISTS"
    
    # Range operators
    BETWEEN = "BETWEEN"
    NOT_BETWEEN = "NOT BETWEEN"
    
    # Null operators
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"
    
    # String concatenation
    CONCAT = "||"
    CONCAT_MYSQL = "CONCAT"
    
    # Bitwise operators
    BITWISE_AND = "&"
    BITWISE_OR = "|"
    BITWISE_XOR = "^"
    BITWISE_NOT = "~"
    BITWISE_SHIFT_LEFT = "<<"
    BITWISE_SHIFT_RIGHT = ">>"
    
    # Assignment
    ASSIGN = ":="
    
    # JSON operators (PostgreSQL)
    JSON_EXTRACT = "->"
    JSON_EXTRACT_TEXT = "->>"
    JSON_PATH = "#>"
    JSON_PATH_TEXT = "#>>"
    JSON_CONTAINS = "@>"
    JSON_CONTAINED = "<@"
    JSON_EXISTS = "?"
    JSON_EXISTS_ANY = "?|"
    JSON_EXISTS_ALL = "?&"
    
    # Array operators (PostgreSQL)
    ARRAY_CONTAINS = "@>"
    ARRAY_CONTAINED = "<@"
    ARRAY_OVERLAP = "&&"
    ARRAY_CONCAT = "||"
    ARRAY_ELEMENT = "[]"


class JoinType(Enum):
    """SQL JOIN type enumeration."""
    INNER = "INNER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    FULL = "FULL"
    CROSS = "CROSS"
    NATURAL = "NATURAL"
    LATERAL = "LATERAL"


class ConstraintType(Enum):
    """SQL constraint type enumeration."""
    PRIMARY_KEY = "PRIMARY KEY"
    FOREIGN_KEY = "FOREIGN KEY"
    UNIQUE = "UNIQUE"
    CHECK = "CHECK"
    NOT_NULL = "NOT NULL"
    DEFAULT = "DEFAULT"
    EXCLUSION = "EXCLUSION"


class WindowFrameType(Enum):
    """SQL window frame type enumeration."""
    ROWS = "ROWS"
    RANGE = "RANGE"
    GROUPS = "GROUPS"


class WindowFrameBound(Enum):
    """SQL window frame bound enumeration."""
    UNBOUNDED_PRECEDING = "UNBOUNDED PRECEDING"
    CURRENT_ROW = "CURRENT ROW"
    UNBOUNDED_FOLLOWING = "UNBOUNDED FOLLOWING"
    PRECEDING = "PRECEDING"
    FOLLOWING = "FOLLOWING"


@dataclass
class SQLNode(ABC):
    """Base class for all SQL AST nodes."""
    node_type: SQLNodeType
    line: int = 0
    column: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept visitor pattern."""
        pass
    
    @property
    def children(self) -> List['SQLNode']:
        """Get child nodes."""
        return []


@dataclass
class SQLProgram(SQLNode):
    """Root node representing a complete SQL program."""
    statements: List['SQLStatement'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.PROGRAM
    
    def accept(self, visitor):
        return visitor.visit_program(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.statements


@dataclass
class SQLStatement(SQLNode):
    """Base class for all SQL statements."""
    pass


@dataclass
class SQLExpression(SQLNode):
    """Base class for all SQL expressions."""
    pass


@dataclass
class SQLClause(SQLNode):
    """Base class for all SQL clauses."""
    pass


# Literal nodes
@dataclass
class SQLLiteral(SQLExpression):
    """Base class for SQL literals."""
    value: Any
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class SQLIntegerLiteral(SQLLiteral):
    """SQL integer literal."""
    value: int
    
    def __post_init__(self):
        self.node_type = SQLNodeType.INTEGER_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_integer_literal(self)


@dataclass
class SQLFloatLiteral(SQLLiteral):
    """SQL float literal."""
    value: float
    
    def __post_init__(self):
        self.node_type = SQLNodeType.FLOAT_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_float_literal(self)


@dataclass
class SQLStringLiteral(SQLLiteral):
    """SQL string literal."""
    value: str
    quote_char: str = "'"
    
    def __post_init__(self):
        self.node_type = SQLNodeType.STRING_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)


@dataclass
class SQLBooleanLiteral(SQLLiteral):
    """SQL boolean literal."""
    value: bool
    
    def __post_init__(self):
        self.node_type = SQLNodeType.BOOLEAN_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)


@dataclass
class SQLNullLiteral(SQLLiteral):
    """SQL NULL literal."""
    value: None = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.NULL_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_null_literal(self)


@dataclass
class SQLDateLiteral(SQLLiteral):
    """SQL date literal."""
    value: str
    
    def __post_init__(self):
        self.node_type = SQLNodeType.DATE_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_date_literal(self)


@dataclass
class SQLTimeLiteral(SQLLiteral):
    """SQL time literal."""
    value: str
    
    def __post_init__(self):
        self.node_type = SQLNodeType.TIME_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_time_literal(self)


@dataclass
class SQLTimestampLiteral(SQLLiteral):
    """SQL timestamp literal."""
    value: str
    
    def __post_init__(self):
        self.node_type = SQLNodeType.TIMESTAMP_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_timestamp_literal(self)


@dataclass
class SQLIntervalLiteral(SQLLiteral):
    """SQL interval literal."""
    value: str
    unit: str
    
    def __post_init__(self):
        self.node_type = SQLNodeType.INTERVAL_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_interval_literal(self)


# Identifier nodes
@dataclass
class SQLIdentifier(SQLExpression):
    """SQL identifier."""
    name: str
    quoted: bool = False
    quote_char: str = '"'
    
    def __post_init__(self):
        self.node_type = SQLNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class SQLQualifiedIdentifier(SQLExpression):
    """SQL qualified identifier (schema.table.column)."""
    parts: List[str]
    quoted: List[bool] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.QUALIFIED_IDENTIFIER
        if not self.quoted:
            self.quoted = [False] * len(self.parts)
    
    def accept(self, visitor):
        return visitor.visit_qualified_identifier(self)


# Data type nodes
@dataclass
class SQLDataType(SQLNode):
    """Base class for SQL data types."""
    name: str
    parameters: List[Union[int, str]] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.DATA_TYPE
    
    def accept(self, visitor):
        return visitor.visit_data_type(self)


@dataclass
class SQLIntegerType(SQLDataType):
    """SQL integer type."""
    size: Optional[int] = None
    unsigned: bool = False
    
    def __post_init__(self):
        self.node_type = SQLNodeType.INTEGER_TYPE
        self.name = "INTEGER"
    
    def accept(self, visitor):
        return visitor.visit_integer_type(self)


@dataclass
class SQLVarcharType(SQLDataType):
    """SQL VARCHAR type."""
    length: Optional[int] = None
    charset: Optional[str] = None
    collation: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.VARCHAR_TYPE
        self.name = "VARCHAR"
    
    def accept(self, visitor):
        return visitor.visit_varchar_type(self)


@dataclass
class SQLDecimalType(SQLDataType):
    """SQL DECIMAL type."""
    precision: Optional[int] = None
    scale: Optional[int] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.DECIMAL_TYPE
        self.name = "DECIMAL"
    
    def accept(self, visitor):
        return visitor.visit_decimal_type(self)


@dataclass
class SQLArrayType(SQLDataType):
    """SQL array type."""
    element_type: SQLDataType
    dimensions: Optional[int] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.ARRAY_TYPE
        self.name = "ARRAY"
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.element_type]


# Expression nodes
@dataclass
class SQLBinaryExpression(SQLExpression):
    """SQL binary expression."""
    left: SQLExpression
    operator: SQLOperator
    right: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.BINARY_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.left, self.right]


@dataclass
class SQLUnaryExpression(SQLExpression):
    """SQL unary expression."""
    operator: SQLOperator
    operand: SQLExpression
    prefix: bool = True
    
    def __post_init__(self):
        self.node_type = SQLNodeType.UNARY_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.operand]


@dataclass
class SQLFunctionCall(SQLExpression):
    """SQL function call."""
    name: str
    arguments: List[SQLExpression] = field(default_factory=list)
    distinct: bool = False
    window: Optional['SQLWindowSpecification'] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.FUNCTION_CALL
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = self.arguments.copy()
        if self.window:
            children.append(self.window)
        return children


@dataclass
class SQLCaseExpression(SQLExpression):
    """SQL CASE expression."""
    expression: Optional[SQLExpression] = None  # For simple CASE
    when_clauses: List[Tuple[SQLExpression, SQLExpression]] = field(default_factory=list)
    else_clause: Optional[SQLExpression] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.CASE_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_case_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = []
        if self.expression:
            children.append(self.expression)
        for when_expr, then_expr in self.when_clauses:
            children.extend([when_expr, then_expr])
        if self.else_clause:
            children.append(self.else_clause)
        return children


@dataclass
class SQLCastExpression(SQLExpression):
    """SQL CAST expression."""
    expression: SQLExpression
    target_type: SQLDataType
    
    def __post_init__(self):
        self.node_type = SQLNodeType.CAST_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_cast_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.expression, self.target_type]


@dataclass
class SQLSubquery(SQLExpression):
    """SQL subquery."""
    query: 'SQLSelectStatement'
    
    def __post_init__(self):
        self.node_type = SQLNodeType.SUBQUERY
    
    def accept(self, visitor):
        return visitor.visit_subquery(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.query]


@dataclass
class SQLColumnReference(SQLExpression):
    """SQL column reference."""
    table: Optional[str] = None
    column: str = ""
    schema: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.COLUMN_REFERENCE
    
    def accept(self, visitor):
        return visitor.visit_column_reference(self)


@dataclass
class SQLInExpression(SQLExpression):
    """SQL IN expression."""
    expression: SQLExpression
    values: List[SQLExpression]
    negated: bool = False
    
    def __post_init__(self):
        self.node_type = SQLNodeType.IN_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_in_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.expression] + self.values


@dataclass
class SQLBetweenExpression(SQLExpression):
    """SQL BETWEEN expression."""
    expression: SQLExpression
    lower_bound: SQLExpression
    upper_bound: SQLExpression
    negated: bool = False
    
    def __post_init__(self):
        self.node_type = SQLNodeType.BETWEEN_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_between_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.expression, self.lower_bound, self.upper_bound]


@dataclass
class SQLLikeExpression(SQLExpression):
    """SQL LIKE expression."""
    expression: SQLExpression
    pattern: SQLExpression
    escape: Optional[SQLExpression] = None
    negated: bool = False
    case_insensitive: bool = False  # ILIKE
    
    def __post_init__(self):
        self.node_type = SQLNodeType.LIKE_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_like_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.expression, self.pattern]
        if self.escape:
            children.append(self.escape)
        return children


@dataclass
class SQLExistsExpression(SQLExpression):
    """SQL EXISTS expression."""
    subquery: SQLSubquery
    negated: bool = False
    
    def __post_init__(self):
        self.node_type = SQLNodeType.EXISTS_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_exists_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.subquery]


# Statement nodes
@dataclass
class SQLSelectStatement(SQLStatement):
    """SQL SELECT statement."""
    select_list: List[SQLExpression] = field(default_factory=list)
    from_clause: Optional['SQLFromClause'] = None
    where_clause: Optional['SQLWhereClause'] = None
    group_by_clause: Optional['SQLGroupByClause'] = None
    having_clause: Optional['SQLHavingClause'] = None
    order_by_clause: Optional['SQLOrderByClause'] = None
    limit_clause: Optional['SQLLimitClause'] = None
    offset_clause: Optional['SQLOffsetClause'] = None
    with_clause: Optional['SQLWithClause'] = None
    distinct: bool = False
    distinct_on: List[SQLExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.SELECT
    
    def accept(self, visitor):
        return visitor.visit_select_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = self.select_list.copy()
        if self.from_clause:
            children.append(self.from_clause)
        if self.where_clause:
            children.append(self.where_clause)
        if self.group_by_clause:
            children.append(self.group_by_clause)
        if self.having_clause:
            children.append(self.having_clause)
        if self.order_by_clause:
            children.append(self.order_by_clause)
        if self.limit_clause:
            children.append(self.limit_clause)
        if self.offset_clause:
            children.append(self.offset_clause)
        if self.with_clause:
            children.append(self.with_clause)
        children.extend(self.distinct_on)
        return children


@dataclass
class SQLInsertStatement(SQLStatement):
    """SQL INSERT statement."""
    table: SQLIdentifier
    columns: List[SQLIdentifier] = field(default_factory=list)
    values: List[List[SQLExpression]] = field(default_factory=list)
    select_query: Optional[SQLSelectStatement] = None
    on_conflict_action: Optional[str] = None
    returning: List[SQLExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.INSERT
    
    def accept(self, visitor):
        return visitor.visit_insert_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.table] + self.columns
        for value_list in self.values:
            children.extend(value_list)
        if self.select_query:
            children.append(self.select_query)
        children.extend(self.returning)
        return children


@dataclass
class SQLUpdateStatement(SQLStatement):
    """SQL UPDATE statement."""
    table: SQLIdentifier
    set_clauses: List[Tuple[SQLIdentifier, SQLExpression]] = field(default_factory=list)
    from_clause: Optional['SQLFromClause'] = None
    where_clause: Optional['SQLWhereClause'] = None
    returning: List[SQLExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.UPDATE
    
    def accept(self, visitor):
        return visitor.visit_update_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.table]
        for column, value in self.set_clauses:
            children.extend([column, value])
        if self.from_clause:
            children.append(self.from_clause)
        if self.where_clause:
            children.append(self.where_clause)
        children.extend(self.returning)
        return children


@dataclass
class SQLDeleteStatement(SQLStatement):
    """SQL DELETE statement."""
    table: SQLIdentifier
    where_clause: Optional['SQLWhereClause'] = None
    returning: List[SQLExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.DELETE
    
    def accept(self, visitor):
        return visitor.visit_delete_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.table]
        if self.where_clause:
            children.append(self.where_clause)
        children.extend(self.returning)
        return children


@dataclass
class SQLCreateTableStatement(SQLStatement):
    """SQL CREATE TABLE statement."""
    table_name: SQLIdentifier
    columns: List['SQLColumnDefinition'] = field(default_factory=list)
    constraints: List['SQLConstraint'] = field(default_factory=list)
    temporary: bool = False
    if_not_exists: bool = False
    as_query: Optional[SQLSelectStatement] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.CREATE_TABLE
    
    def accept(self, visitor):
        return visitor.visit_create_table_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.table_name] + self.columns + self.constraints
        if self.as_query:
            children.append(self.as_query)
        return children


@dataclass
class SQLDropTableStatement(SQLStatement):
    """SQL DROP TABLE statement."""
    table_names: List[SQLIdentifier]
    if_exists: bool = False
    cascade: bool = False
    
    def __post_init__(self):
        self.node_type = SQLNodeType.DROP_TABLE
    
    def accept(self, visitor):
        return visitor.visit_drop_table_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.table_names


@dataclass
class SQLAlterTableStatement(SQLStatement):
    """SQL ALTER TABLE statement."""
    table_name: SQLIdentifier
    actions: List['SQLAlterTableAction'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.ALTER_TABLE
    
    def accept(self, visitor):
        return visitor.visit_alter_table_statement(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.table_name] + self.actions


# Clause nodes
@dataclass
class SQLFromClause(SQLClause):
    """SQL FROM clause."""
    table_references: List['SQLTableReference'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.FROM_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_from_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.table_references


@dataclass
class SQLWhereClause(SQLClause):
    """SQL WHERE clause."""
    condition: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.WHERE_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_where_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.condition]


@dataclass
class SQLGroupByClause(SQLClause):
    """SQL GROUP BY clause."""
    expressions: List[SQLExpression]
    
    def __post_init__(self):
        self.node_type = SQLNodeType.GROUP_BY_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_group_by_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.expressions


@dataclass
class SQLHavingClause(SQLClause):
    """SQL HAVING clause."""
    condition: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.HAVING_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_having_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.condition]


@dataclass
class SQLOrderByClause(SQLClause):
    """SQL ORDER BY clause."""
    expressions: List['SQLOrderByExpression']
    
    def __post_init__(self):
        self.node_type = SQLNodeType.ORDER_BY_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_order_by_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.expressions


@dataclass
class SQLOrderByExpression(SQLExpression):
    """SQL ORDER BY expression."""
    expression: SQLExpression
    ascending: bool = True
    nulls_first: Optional[bool] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.ORDER_BY
    
    def accept(self, visitor):
        return visitor.visit_order_by_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.expression]


@dataclass
class SQLLimitClause(SQLClause):
    """SQL LIMIT clause."""
    count: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.LIMIT_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_limit_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.count]


@dataclass
class SQLOffsetClause(SQLClause):
    """SQL OFFSET clause."""
    count: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.OFFSET_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_offset_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.count]


@dataclass
class SQLWithClause(SQLClause):
    """SQL WITH clause (Common Table Expressions)."""
    cte_list: List['SQLCommonTableExpression']
    recursive: bool = False
    
    def __post_init__(self):
        self.node_type = SQLNodeType.WITH_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_with_clause(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.cte_list


@dataclass
class SQLCommonTableExpression(SQLNode):
    """SQL Common Table Expression."""
    name: SQLIdentifier
    columns: List[SQLIdentifier] = field(default_factory=list)
    query: SQLSelectStatement = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.CTE
    
    def accept(self, visitor):
        return visitor.visit_common_table_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.name] + self.columns + [self.query]


# Table reference nodes
@dataclass
class SQLTableReference(SQLNode):
    """Base class for table references."""
    alias: Optional[SQLIdentifier] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.TABLE_REFERENCE
    
    def accept(self, visitor):
        return visitor.visit_table_reference(self)


@dataclass
class SQLTableName(SQLTableReference):
    """Simple table name reference."""
    name: SQLIdentifier
    
    def accept(self, visitor):
        return visitor.visit_table_name(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.name]
        if self.alias:
            children.append(self.alias)
        return children


@dataclass
class SQLJoin(SQLTableReference):
    """SQL JOIN operation."""
    join_type: JoinType
    left: SQLTableReference
    right: SQLTableReference
    condition: Optional[SQLExpression] = None
    using_columns: List[SQLIdentifier] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.JOIN
    
    def accept(self, visitor):
        return visitor.visit_join(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.left, self.right]
        if self.condition:
            children.append(self.condition)
        children.extend(self.using_columns)
        return children


@dataclass
class SQLDerivedTable(SQLTableReference):
    """Derived table (subquery in FROM clause)."""
    query: SQLSelectStatement
    
    def accept(self, visitor):
        return visitor.visit_derived_table(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.query]
        if self.alias:
            children.append(self.alias)
        return children


# Column definition and constraints
@dataclass
class SQLColumnDefinition(SQLNode):
    """SQL column definition."""
    name: SQLIdentifier
    data_type: SQLDataType
    constraints: List['SQLConstraint'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.COLUMN_DEFINITION
    
    def accept(self, visitor):
        return visitor.visit_column_definition(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.name, self.data_type] + self.constraints


@dataclass
class SQLConstraint(SQLNode):
    """Base class for SQL constraints."""
    constraint_type: ConstraintType
    name: Optional[SQLIdentifier] = None
    
    def accept(self, visitor):
        return visitor.visit_constraint(self)


@dataclass
class SQLPrimaryKeyConstraint(SQLConstraint):
    """SQL PRIMARY KEY constraint."""
    columns: List[SQLIdentifier] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.PRIMARY_KEY_CONSTRAINT
        self.constraint_type = ConstraintType.PRIMARY_KEY
    
    def accept(self, visitor):
        return visitor.visit_primary_key_constraint(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = self.columns.copy()
        if self.name:
            children.append(self.name)
        return children


@dataclass
class SQLForeignKeyConstraint(SQLConstraint):
    """SQL FOREIGN KEY constraint."""
    columns: List[SQLIdentifier] = field(default_factory=list)
    referenced_table: SQLIdentifier = None
    referenced_columns: List[SQLIdentifier] = field(default_factory=list)
    on_delete: Optional[str] = None
    on_update: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.FOREIGN_KEY_CONSTRAINT
        self.constraint_type = ConstraintType.FOREIGN_KEY
    
    def accept(self, visitor):
        return visitor.visit_foreign_key_constraint(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = self.columns.copy()
        if self.name:
            children.append(self.name)
        if self.referenced_table:
            children.append(self.referenced_table)
        children.extend(self.referenced_columns)
        return children


@dataclass
class SQLUniqueConstraint(SQLConstraint):
    """SQL UNIQUE constraint."""
    columns: List[SQLIdentifier] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.UNIQUE_CONSTRAINT
        self.constraint_type = ConstraintType.UNIQUE
    
    def accept(self, visitor):
        return visitor.visit_unique_constraint(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = self.columns.copy()
        if self.name:
            children.append(self.name)
        return children


@dataclass
class SQLCheckConstraint(SQLConstraint):
    """SQL CHECK constraint."""
    condition: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.CHECK_CONSTRAINT
        self.constraint_type = ConstraintType.CHECK
    
    def accept(self, visitor):
        return visitor.visit_check_constraint(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.condition]
        if self.name:
            children.append(self.name)
        return children


@dataclass
class SQLDefaultConstraint(SQLConstraint):
    """SQL DEFAULT constraint."""
    value: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.DEFAULT_CONSTRAINT
        self.constraint_type = ConstraintType.DEFAULT
    
    def accept(self, visitor):
        return visitor.visit_default_constraint(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.value]
        if self.name:
            children.append(self.name)
        return children


# Window function nodes
@dataclass
class SQLWindowSpecification(SQLNode):
    """SQL window specification."""
    partition_by: List[SQLExpression] = field(default_factory=list)
    order_by: List[SQLOrderByExpression] = field(default_factory=list)
    frame_clause: Optional['SQLFrameClause'] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.WINDOW_SPECIFICATION
    
    def accept(self, visitor):
        return visitor.visit_window_specification(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = self.partition_by + self.order_by
        if self.frame_clause:
            children.append(self.frame_clause)
        return children


@dataclass
class SQLFrameClause(SQLNode):
    """SQL frame clause for window functions."""
    frame_type: WindowFrameType
    start_bound: WindowFrameBound
    end_bound: Optional[WindowFrameBound] = None
    
    def __post_init__(self):
        self.node_type = SQLNodeType.FRAME_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_frame_clause(self)


# Set operation nodes
@dataclass
class SQLSetOperation(SQLStatement):
    """SQL set operation (UNION, INTERSECT, EXCEPT)."""
    left: SQLSelectStatement
    right: SQLSelectStatement
    operation: str
    all_modifier: bool = False
    
    def __post_init__(self):
        if self.operation.upper() == "UNION":
            self.node_type = SQLNodeType.UNION_ALL if self.all_modifier else SQLNodeType.UNION
        elif self.operation.upper() == "INTERSECT":
            self.node_type = SQLNodeType.INTERSECT_ALL if self.all_modifier else SQLNodeType.INTERSECT
        elif self.operation.upper() == "EXCEPT":
            self.node_type = SQLNodeType.EXCEPT_ALL if self.all_modifier else SQLNodeType.EXCEPT
    
    def accept(self, visitor):
        return visitor.visit_set_operation(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.left, self.right]


# Alter table actions
@dataclass
class SQLAlterTableAction(SQLNode):
    """Base class for ALTER TABLE actions."""
    pass


@dataclass
class SQLAddColumnAction(SQLAlterTableAction):
    """ALTER TABLE ADD COLUMN action."""
    column: SQLColumnDefinition
    
    def accept(self, visitor):
        return visitor.visit_add_column_action(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.column]


@dataclass
class SQLDropColumnAction(SQLAlterTableAction):
    """ALTER TABLE DROP COLUMN action."""
    column_name: SQLIdentifier
    if_exists: bool = False
    cascade: bool = False
    
    def accept(self, visitor):
        return visitor.visit_drop_column_action(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.column_name]


@dataclass
class SQLAlterColumnAction(SQLAlterTableAction):
    """ALTER TABLE ALTER COLUMN action."""
    column_name: SQLIdentifier
    new_data_type: Optional[SQLDataType] = None
    set_default: Optional[SQLExpression] = None
    drop_default: bool = False
    set_not_null: bool = False
    drop_not_null: bool = False
    
    def accept(self, visitor):
        return visitor.visit_alter_column_action(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = [self.column_name]
        if self.new_data_type:
            children.append(self.new_data_type)
        if self.set_default:
            children.append(self.set_default)
        return children


@dataclass
class SQLAddConstraintAction(SQLAlterTableAction):
    """ALTER TABLE ADD CONSTRAINT action."""
    constraint: SQLConstraint
    
    def accept(self, visitor):
        return visitor.visit_add_constraint_action(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.constraint]


@dataclass
class SQLDropConstraintAction(SQLAlterTableAction):
    """ALTER TABLE DROP CONSTRAINT action."""
    constraint_name: SQLIdentifier
    if_exists: bool = False
    cascade: bool = False
    
    def accept(self, visitor):
        return visitor.visit_drop_constraint_action(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.constraint_name]


# JSON operations (modern SQL features)
@dataclass
class SQLJSONExtractExpression(SQLExpression):
    """SQL JSON extract expression."""
    json_expression: SQLExpression
    path: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.JSON_EXTRACT
    
    def accept(self, visitor):
        return visitor.visit_json_extract_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.json_expression, self.path]


@dataclass
class SQLJSONObjectExpression(SQLExpression):
    """SQL JSON object construction."""
    key_value_pairs: List[Tuple[SQLExpression, SQLExpression]] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.JSON_OBJECT
    
    def accept(self, visitor):
        return visitor.visit_json_object_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        children = []
        for key, value in self.key_value_pairs:
            children.extend([key, value])
        return children


@dataclass
class SQLJSONArrayExpression(SQLExpression):
    """SQL JSON array construction."""
    elements: List[SQLExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.JSON_ARRAY
    
    def accept(self, visitor):
        return visitor.visit_json_array_expression(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.elements


# Array operations
@dataclass
class SQLArrayConstructor(SQLExpression):
    """SQL array constructor."""
    elements: List[SQLExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = SQLNodeType.ARRAY_CONSTRUCTOR
    
    def accept(self, visitor):
        return visitor.visit_array_constructor(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return self.elements


@dataclass
class SQLArrayElement(SQLExpression):
    """SQL array element access."""
    array_expression: SQLExpression
    index: SQLExpression
    
    def __post_init__(self):
        self.node_type = SQLNodeType.ARRAY_ELEMENT
    
    def accept(self, visitor):
        return visitor.visit_array_element(self)
    
    @property
    def children(self) -> List[SQLNode]:
        return [self.array_expression, self.index]


# Visitor pattern interface
class SQLVisitor(ABC):
    """Abstract base class for SQL AST visitors."""
    
    @abstractmethod
    def visit_program(self, node: SQLProgram):
        pass
    
    @abstractmethod
    def visit_select_statement(self, node: SQLSelectStatement):
        pass
    
    @abstractmethod
    def visit_insert_statement(self, node: SQLInsertStatement):
        pass
    
    @abstractmethod
    def visit_update_statement(self, node: SQLUpdateStatement):
        pass
    
    @abstractmethod
    def visit_delete_statement(self, node: SQLDeleteStatement):
        pass
    
    @abstractmethod
    def visit_create_table_statement(self, node: SQLCreateTableStatement):
        pass
    
    @abstractmethod
    def visit_drop_table_statement(self, node: SQLDropTableStatement):
        pass
    
    @abstractmethod
    def visit_alter_table_statement(self, node: SQLAlterTableStatement):
        pass
    
    @abstractmethod
    def visit_binary_expression(self, node: SQLBinaryExpression):
        pass
    
    @abstractmethod
    def visit_unary_expression(self, node: SQLUnaryExpression):
        pass
    
    @abstractmethod
    def visit_function_call(self, node: SQLFunctionCall):
        pass
    
    @abstractmethod
    def visit_case_expression(self, node: SQLCaseExpression):
        pass
    
    @abstractmethod
    def visit_cast_expression(self, node: SQLCastExpression):
        pass
    
    @abstractmethod
    def visit_subquery(self, node: SQLSubquery):
        pass
    
    @abstractmethod
    def visit_column_reference(self, node: SQLColumnReference):
        pass
    
    @abstractmethod
    def visit_identifier(self, node: SQLIdentifier):
        pass
    
    @abstractmethod
    def visit_qualified_identifier(self, node: SQLQualifiedIdentifier):
        pass
    
    @abstractmethod
    def visit_literal(self, node: SQLLiteral):
        pass
    
    @abstractmethod
    def visit_data_type(self, node: SQLDataType):
        pass
    
    @abstractmethod
    def visit_constraint(self, node: SQLConstraint):
        pass
    
    @abstractmethod
    def visit_from_clause(self, node: SQLFromClause):
        pass
    
    @abstractmethod
    def visit_where_clause(self, node: SQLWhereClause):
        pass
    
    @abstractmethod
    def visit_group_by_clause(self, node: SQLGroupByClause):
        pass
    
    @abstractmethod
    def visit_having_clause(self, node: SQLHavingClause):
        pass
    
    @abstractmethod
    def visit_order_by_clause(self, node: SQLOrderByClause):
        pass
    
    @abstractmethod
    def visit_limit_clause(self, node: SQLLimitClause):
        pass
    
    @abstractmethod
    def visit_offset_clause(self, node: SQLOffsetClause):
        pass
    
    @abstractmethod
    def visit_with_clause(self, node: SQLWithClause):
        pass
    
    @abstractmethod
    def visit_join(self, node: SQLJoin):
        pass
    
    @abstractmethod
    def visit_table_reference(self, node: SQLTableReference):
        pass
    
    @abstractmethod
    def visit_column_definition(self, node: SQLColumnDefinition):
        pass
    
    @abstractmethod
    def visit_window_specification(self, node: SQLWindowSpecification):
        pass
    
    @abstractmethod
    def visit_set_operation(self, node: SQLSetOperation):
        pass
    
    # Additional visit methods for specific node types
    def visit_integer_literal(self, node: SQLIntegerLiteral):
        return self.visit_literal(node)
    
    def visit_float_literal(self, node: SQLFloatLiteral):
        return self.visit_literal(node)
    
    def visit_string_literal(self, node: SQLStringLiteral):
        return self.visit_literal(node)
    
    def visit_boolean_literal(self, node: SQLBooleanLiteral):
        return self.visit_literal(node)
    
    def visit_null_literal(self, node: SQLNullLiteral):
        return self.visit_literal(node)
    
    def visit_date_literal(self, node: SQLDateLiteral):
        return self.visit_literal(node)
    
    def visit_time_literal(self, node: SQLTimeLiteral):
        return self.visit_literal(node)
    
    def visit_timestamp_literal(self, node: SQLTimestampLiteral):
        return self.visit_literal(node)
    
    def visit_interval_literal(self, node: SQLIntervalLiteral):
        return self.visit_literal(node)
    
    def visit_integer_type(self, node: SQLIntegerType):
        return self.visit_data_type(node)
    
    def visit_varchar_type(self, node: SQLVarcharType):
        return self.visit_data_type(node)
    
    def visit_decimal_type(self, node: SQLDecimalType):
        return self.visit_data_type(node)
    
    def visit_array_type(self, node: SQLArrayType):
        return self.visit_data_type(node)
    
    def visit_primary_key_constraint(self, node: SQLPrimaryKeyConstraint):
        return self.visit_constraint(node)
    
    def visit_foreign_key_constraint(self, node: SQLForeignKeyConstraint):
        return self.visit_constraint(node)
    
    def visit_unique_constraint(self, node: SQLUniqueConstraint):
        return self.visit_constraint(node)
    
    def visit_check_constraint(self, node: SQLCheckConstraint):
        return self.visit_constraint(node)
    
    def visit_default_constraint(self, node: SQLDefaultConstraint):
        return self.visit_constraint(node)
    
    def visit_in_expression(self, node: SQLInExpression):
        return self.visit_binary_expression(node)
    
    def visit_between_expression(self, node: SQLBetweenExpression):
        return self.visit_binary_expression(node)
    
    def visit_like_expression(self, node: SQLLikeExpression):
        return self.visit_binary_expression(node)
    
    def visit_exists_expression(self, node: SQLExistsExpression):
        return self.visit_unary_expression(node)
    
    def visit_order_by_expression(self, node: SQLOrderByExpression):
        return self.visit_literal(node)
    
    def visit_common_table_expression(self, node: SQLCommonTableExpression):
        return self.visit_literal(node)
    
    def visit_table_name(self, node: SQLTableName):
        return self.visit_table_reference(node)
    
    def visit_derived_table(self, node: SQLDerivedTable):
        return self.visit_table_reference(node)
    
    def visit_frame_clause(self, node: SQLFrameClause):
        return self.visit_literal(node)
    
    def visit_add_column_action(self, node: SQLAddColumnAction):
        return self.visit_literal(node)
    
    def visit_drop_column_action(self, node: SQLDropColumnAction):
        return self.visit_literal(node)
    
    def visit_alter_column_action(self, node: SQLAlterColumnAction):
        return self.visit_literal(node)
    
    def visit_add_constraint_action(self, node: SQLAddConstraintAction):
        return self.visit_literal(node)
    
    def visit_drop_constraint_action(self, node: SQLDropConstraintAction):
        return self.visit_literal(node)
    
    def visit_json_extract_expression(self, node: SQLJSONExtractExpression):
        return self.visit_binary_expression(node)
    
    def visit_json_object_expression(self, node: SQLJSONObjectExpression):
        return self.visit_function_call(node)
    
    def visit_json_array_expression(self, node: SQLJSONArrayExpression):
        return self.visit_function_call(node)
    
    def visit_array_constructor(self, node: SQLArrayConstructor):
        return self.visit_function_call(node)
    
    def visit_array_element(self, node: SQLArrayElement):
        return self.visit_binary_expression(node)