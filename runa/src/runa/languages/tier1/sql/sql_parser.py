#!/usr/bin/env python3
"""
SQL Parser and Lexer

Comprehensive SQL parsing implementation supporting multiple SQL dialects including
ANSI SQL-92/99/2003/2008/2011/2016, MySQL, PostgreSQL, SQL Server, Oracle, and SQLite.

This module provides:
- SQLToken: Token representation for SQL lexical elements
- SQLLexer: Tokenization of SQL source code
- SQLParser: Recursive descent parser for SQL statements
- Multi-dialect support with dialect-specific parsing rules
- Comprehensive error handling and recovery
- Support for complex SQL constructs including CTEs, window functions, and JSON operations

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import logging

from .sql_ast import *


class SQLTokenType(Enum):
    """SQL token types."""
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    DATE = auto()
    TIME = auto()
    TIMESTAMP = auto()
    INTERVAL = auto()
    BINARY = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    QUOTED_IDENTIFIER = auto()
    
    # Keywords - Core SQL
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    CREATE = auto()
    ALTER = auto()
    DROP = auto()
    TABLE = auto()
    INDEX = auto()
    VIEW = auto()
    PROCEDURE = auto()
    FUNCTION = auto()
    TRIGGER = auto()
    SCHEMA = auto()
    DATABASE = auto()
    
    # Keywords - Clauses
    GROUP = auto()
    BY = auto()
    HAVING = auto()
    ORDER = auto()
    LIMIT = auto()
    OFFSET = auto()
    WITH = auto()
    AS = auto()
    ON = auto()
    USING = auto()
    DISTINCT = auto()
    ALL = auto()
    INTO = auto()
    VALUES = auto()
    SET = auto()
    
    # Keywords - Joins
    JOIN = auto()
    INNER = auto()
    LEFT = auto()
    RIGHT = auto()
    FULL = auto()
    CROSS = auto()
    OUTER = auto()
    NATURAL = auto()
    LATERAL = auto()
    
    # Keywords - Data types
    INTEGER_TYPE = auto()
    BIGINT = auto()
    SMALLINT = auto()
    TINYINT = auto()
    DECIMAL = auto()
    NUMERIC = auto()
    FLOAT_TYPE = auto()
    DOUBLE = auto()
    REAL = auto()
    CHAR = auto()
    VARCHAR = auto()
    TEXT = auto()
    CLOB = auto()
    BLOB = auto()
    BINARY_TYPE = auto()
    VARBINARY = auto()
    BOOLEAN_TYPE = auto()
    DATE_TYPE = auto()
    TIME_TYPE = auto()
    TIMESTAMP_TYPE = auto()
    INTERVAL_TYPE = auto()
    JSON = auto()
    XML = auto()
    UUID = auto()
    ARRAY = auto()
    
    # Keywords - Constraints
    PRIMARY = auto()
    KEY = auto()
    FOREIGN = auto()
    UNIQUE = auto()
    CHECK = auto()
    NOT = auto()
    DEFAULT = auto()
    CONSTRAINT = auto()
    REFERENCES = auto()
    CASCADE = auto()
    RESTRICT = auto()
    
    # Keywords - Operators
    AND = auto()
    OR = auto()
    IN = auto()
    EXISTS = auto()
    BETWEEN = auto()
    LIKE = auto()
    ILIKE = auto()
    SIMILAR = auto()
    TO = auto()
    REGEXP = auto()
    RLIKE = auto()
    IS = auto()
    NULLS = auto()
    FIRST = auto()
    LAST = auto()
    
    # Keywords - Functions
    CASE = auto()
    WHEN = auto()
    THEN = auto()
    ELSE = auto()
    END = auto()
    CAST = auto()
    EXTRACT = auto()
    COALESCE = auto()
    NULLIF = auto()
    GREATEST = auto()
    LEAST = auto()
    
    # Keywords - Aggregates
    COUNT = auto()
    SUM = auto()
    AVG = auto()
    MIN = auto()
    MAX = auto()
    STDDEV = auto()
    VARIANCE = auto()
    
    # Keywords - Window functions
    OVER = auto()
    PARTITION = auto()
    WINDOW = auto()
    ROWS = auto()
    RANGE = auto()
    GROUPS = auto()
    UNBOUNDED = auto()
    PRECEDING = auto()
    FOLLOWING = auto()
    CURRENT = auto()
    ROW = auto()
    
    # Keywords - Set operations
    UNION = auto()
    INTERSECT = auto()
    EXCEPT = auto()
    MINUS = auto()
    
    # Keywords - Transactions
    COMMIT = auto()
    ROLLBACK = auto()
    SAVEPOINT = auto()
    RELEASE = auto()
    START = auto()
    BEGIN = auto()
    TRANSACTION = auto()
    
    # Keywords - Permissions
    GRANT = auto()
    REVOKE = auto()
    DENY = auto()
    PRIVILEGES = auto()
    ROLE = auto()
    USER = auto()
    
    # Keywords - Modifiers
    TEMPORARY = auto()
    TEMP = auto()
    IF = auto()
    ONLY = auto()
    REPLACE = auto()
    IGNORE = auto()
    
    # Keywords - Advanced
    RECURSIVE = auto()
    MATERIALIZED = auto()
    REFRESH = auto()
    CONCURRENTLY = auto()
    COLLATE = auto()
    SEQUENCE = auto()
    DOMAIN = auto()
    TYPE = auto()
    ENUM = auto()
    COMMENT = auto()
    ANALYZE = auto()
    VACUUM = auto()
    EXPLAIN = auto()
    SHOW = auto()
    DESCRIBE = auto()
    USE = auto()
    RESET = auto()
    
    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    MODULO = auto()        # %
    POWER = auto()         # ^
    EQUAL = auto()         # =
    NOT_EQUAL = auto()     # <> or !=
    LESS_THAN = auto()     # <
    GREATER_THAN = auto()  # >
    LESS_EQUAL = auto()    # <=
    GREATER_EQUAL = auto() # >=
    ASSIGNMENT = auto()    # :=
    
    # String operators
    CONCAT = auto()        # ||
    
    # Bitwise operators
    BITWISE_AND = auto()   # &
    BITWISE_OR = auto()    # |
    BITWISE_XOR = auto()   # ^
    BITWISE_NOT = auto()   # ~
    SHIFT_LEFT = auto()    # <<
    SHIFT_RIGHT = auto()   # >>
    
    # JSON operators (PostgreSQL)
    JSON_EXTRACT = auto()      # ->
    JSON_EXTRACT_TEXT = auto() # ->>
    JSON_PATH = auto()         # #>
    JSON_PATH_TEXT = auto()    # #>>
    JSON_CONTAINS = auto()     # @>
    JSON_CONTAINED = auto()    # <@
    JSON_EXISTS = auto()       # ?
    JSON_EXISTS_ANY = auto()   # ?|
    JSON_EXISTS_ALL = auto()   # ?&
    
    # Array operators
    ARRAY_CONTAINS = auto()    # @>
    ARRAY_CONTAINED = auto()   # <@
    ARRAY_OVERLAP = auto()     # &&
    ARRAY_CONCAT = auto()      # ||
    
    # Punctuation
    SEMICOLON = auto()     # ;
    COMMA = auto()         # ,
    DOT = auto()           # .
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    
    # Special
    PARAMETER = auto()     # ?
    NAMED_PARAMETER = auto() # :name or $1
    WILDCARD = auto()      # *
    PLACEHOLDER = auto()   # Placeholder for missing tokens
    
    # End of file
    EOF = auto()
    
    # Whitespace and comments (usually ignored)
    WHITESPACE = auto()
    COMMENT = auto()
    MULTILINE_COMMENT = auto()


@dataclass
class SQLToken:
    """SQL token representation."""
    type: SQLTokenType
    value: str
    line: int = 1
    column: int = 1
    length: int = 0
    
    def __post_init__(self):
        if self.length == 0:
            self.length = len(self.value)
    
    def __str__(self):
        return f"{self.type.name}({self.value!r})"
    
    def __repr__(self):
        return f"SQLToken({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class SQLLexer:
    """
    SQL lexer for tokenizing SQL source code.
    
    Supports multiple SQL dialects and provides comprehensive tokenization
    of SQL statements including keywords, operators, literals, and identifiers.
    """
    
    def __init__(self, dialect: SQLDialect = SQLDialect.ANSI):
        """
        Initialize the SQL lexer.
        
        Args:
            dialect: SQL dialect to use for parsing
        """
        self.dialect = dialect
        self.logger = logging.getLogger(__name__)
        
        # Token patterns
        self.token_patterns = self._build_token_patterns()
        
        # Keywords by dialect
        self.keywords = self._build_keywords()
        
        # Operator patterns
        self.operators = self._build_operators()
        
        # State tracking
        self.text = ""
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def _build_token_patterns(self) -> List[Tuple[str, SQLTokenType]]:
        """Build regex patterns for tokenization."""
        patterns = [
            # Multiline comments
            (r'/\*.*?\*/', SQLTokenType.MULTILINE_COMMENT),
            
            # Single line comments
            (r'--.*?$', SQLTokenType.COMMENT),
            (r'#.*?$', SQLTokenType.COMMENT),  # MySQL style
            
            # String literals
            (r"'(?:[^'\\]|\\.)*'", SQLTokenType.STRING),
            (r'"(?:[^"\\]|\\.)*"', SQLTokenType.QUOTED_IDENTIFIER),
            (r'`(?:[^`\\]|\\.)*`', SQLTokenType.QUOTED_IDENTIFIER),  # MySQL backticks
            
            # Numeric literals
            (r'\b\d+\.\d+([eE][+-]?\d+)?\b', SQLTokenType.FLOAT),
            (r'\b\d+[eE][+-]?\d+\b', SQLTokenType.FLOAT),
            (r'\b\d+\b', SQLTokenType.INTEGER),
            
            # Date/time literals
            (r"DATE\s*'[^']*'", SQLTokenType.DATE),
            (r"TIME\s*'[^']*'", SQLTokenType.TIME),
            (r"TIMESTAMP\s*'[^']*'", SQLTokenType.TIMESTAMP),
            (r"INTERVAL\s*'[^']*'", SQLTokenType.INTERVAL),
            
            # Binary literals
            (r"[xX]'[0-9a-fA-F]*'", SQLTokenType.BINARY),
            (r"0[xX][0-9a-fA-F]+", SQLTokenType.BINARY),
            
            # Multi-character operators
            (r'<>', SQLTokenType.NOT_EQUAL),
            (r'!=', SQLTokenType.NOT_EQUAL),
            (r'<=', SQLTokenType.LESS_EQUAL),
            (r'>=', SQLTokenType.GREATER_EQUAL),
            (r':=', SQLTokenType.ASSIGNMENT),
            (r'\|\|', SQLTokenType.CONCAT),
            (r'<<', SQLTokenType.SHIFT_LEFT),
            (r'>>', SQLTokenType.SHIFT_RIGHT),
            
            # JSON operators (PostgreSQL)
            (r'->', SQLTokenType.JSON_EXTRACT),
            (r'->>', SQLTokenType.JSON_EXTRACT_TEXT),
            (r'#>', SQLTokenType.JSON_PATH),
            (r'#>>', SQLTokenType.JSON_PATH_TEXT),
            (r'@>', SQLTokenType.JSON_CONTAINS),
            (r'<@', SQLTokenType.JSON_CONTAINED),
            (r'\?\|', SQLTokenType.JSON_EXISTS_ANY),
            (r'\?&', SQLTokenType.JSON_EXISTS_ALL),
            (r'\?', SQLTokenType.JSON_EXISTS),
            
            # Array operators
            (r'&&', SQLTokenType.ARRAY_OVERLAP),
            
            # Single-character operators
            (r'\+', SQLTokenType.PLUS),
            (r'-', SQLTokenType.MINUS),
            (r'\*', SQLTokenType.MULTIPLY),
            (r'/', SQLTokenType.DIVIDE),
            (r'%', SQLTokenType.MODULO),
            (r'\^', SQLTokenType.POWER),
            (r'=', SQLTokenType.EQUAL),
            (r'<', SQLTokenType.LESS_THAN),
            (r'>', SQLTokenType.GREATER_THAN),
            (r'&', SQLTokenType.BITWISE_AND),
            (r'\|', SQLTokenType.BITWISE_OR),
            (r'~', SQLTokenType.BITWISE_NOT),
            
            # Punctuation
            (r';', SQLTokenType.SEMICOLON),
            (r',', SQLTokenType.COMMA),
            (r'\.', SQLTokenType.DOT),
            (r'\(', SQLTokenType.LPAREN),
            (r'\)', SQLTokenType.RPAREN),
            (r'\[', SQLTokenType.LBRACKET),
            (r'\]', SQLTokenType.RBRACKET),
            (r'\{', SQLTokenType.LBRACE),
            (r'\}', SQLTokenType.RBRACE),
            
            # Parameters
            (r'\$\d+', SQLTokenType.NAMED_PARAMETER),  # PostgreSQL $1, $2, etc.
            (r':\w+', SQLTokenType.NAMED_PARAMETER),   # Oracle :name
            
            # Identifiers (must come after keywords)
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', SQLTokenType.IDENTIFIER),
            
            # Whitespace
            (r'\s+', SQLTokenType.WHITESPACE),
        ]
        
        return [(re.compile(pattern, re.MULTILINE | re.IGNORECASE), token_type) 
                for pattern, token_type in patterns]
    
    def _build_keywords(self) -> Dict[str, SQLTokenType]:
        """Build keyword mapping for the current dialect."""
        # Base ANSI SQL keywords
        keywords = {
            # Core statements
            'SELECT': SQLTokenType.SELECT,
            'FROM': SQLTokenType.FROM,
            'WHERE': SQLTokenType.WHERE,
            'INSERT': SQLTokenType.INSERT,
            'UPDATE': SQLTokenType.UPDATE,
            'DELETE': SQLTokenType.DELETE,
            'CREATE': SQLTokenType.CREATE,
            'ALTER': SQLTokenType.ALTER,
            'DROP': SQLTokenType.DROP,
            'TABLE': SQLTokenType.TABLE,
            'INDEX': SQLTokenType.INDEX,
            'VIEW': SQLTokenType.VIEW,
            'PROCEDURE': SQLTokenType.PROCEDURE,
            'FUNCTION': SQLTokenType.FUNCTION,
            'TRIGGER': SQLTokenType.TRIGGER,
            'SCHEMA': SQLTokenType.SCHEMA,
            'DATABASE': SQLTokenType.DATABASE,
            
            # Clauses
            'GROUP': SQLTokenType.GROUP,
            'BY': SQLTokenType.BY,
            'HAVING': SQLTokenType.HAVING,
            'ORDER': SQLTokenType.ORDER,
            'LIMIT': SQLTokenType.LIMIT,
            'OFFSET': SQLTokenType.OFFSET,
            'WITH': SQLTokenType.WITH,
            'AS': SQLTokenType.AS,
            'ON': SQLTokenType.ON,
            'USING': SQLTokenType.USING,
            'DISTINCT': SQLTokenType.DISTINCT,
            'ALL': SQLTokenType.ALL,
            'INTO': SQLTokenType.INTO,
            'VALUES': SQLTokenType.VALUES,
            'SET': SQLTokenType.SET,
            
            # Joins
            'JOIN': SQLTokenType.JOIN,
            'INNER': SQLTokenType.INNER,
            'LEFT': SQLTokenType.LEFT,
            'RIGHT': SQLTokenType.RIGHT,
            'FULL': SQLTokenType.FULL,
            'CROSS': SQLTokenType.CROSS,
            'OUTER': SQLTokenType.OUTER,
            'NATURAL': SQLTokenType.NATURAL,
            'LATERAL': SQLTokenType.LATERAL,
            
            # Data types
            'INTEGER': SQLTokenType.INTEGER_TYPE,
            'INT': SQLTokenType.INTEGER_TYPE,
            'BIGINT': SQLTokenType.BIGINT,
            'SMALLINT': SQLTokenType.SMALLINT,
            'TINYINT': SQLTokenType.TINYINT,
            'DECIMAL': SQLTokenType.DECIMAL,
            'NUMERIC': SQLTokenType.NUMERIC,
            'FLOAT': SQLTokenType.FLOAT_TYPE,
            'DOUBLE': SQLTokenType.DOUBLE,
            'REAL': SQLTokenType.REAL,
            'CHAR': SQLTokenType.CHAR,
            'VARCHAR': SQLTokenType.VARCHAR,
            'TEXT': SQLTokenType.TEXT,
            'CLOB': SQLTokenType.CLOB,
            'BLOB': SQLTokenType.BLOB,
            'BINARY': SQLTokenType.BINARY_TYPE,
            'VARBINARY': SQLTokenType.VARBINARY,
            'BOOLEAN': SQLTokenType.BOOLEAN_TYPE,
            'BOOL': SQLTokenType.BOOLEAN_TYPE,
            'DATE': SQLTokenType.DATE_TYPE,
            'TIME': SQLTokenType.TIME_TYPE,
            'TIMESTAMP': SQLTokenType.TIMESTAMP_TYPE,
            'INTERVAL': SQLTokenType.INTERVAL_TYPE,
            'JSON': SQLTokenType.JSON,
            'XML': SQLTokenType.XML,
            'UUID': SQLTokenType.UUID,
            'ARRAY': SQLTokenType.ARRAY,
            
            # Constraints
            'PRIMARY': SQLTokenType.PRIMARY,
            'KEY': SQLTokenType.KEY,
            'FOREIGN': SQLTokenType.FOREIGN,
            'UNIQUE': SQLTokenType.UNIQUE,
            'CHECK': SQLTokenType.CHECK,
            'NOT': SQLTokenType.NOT,
            'DEFAULT': SQLTokenType.DEFAULT,
            'CONSTRAINT': SQLTokenType.CONSTRAINT,
            'REFERENCES': SQLTokenType.REFERENCES,
            'CASCADE': SQLTokenType.CASCADE,
            'RESTRICT': SQLTokenType.RESTRICT,
            
            # Operators
            'AND': SQLTokenType.AND,
            'OR': SQLTokenType.OR,
            'IN': SQLTokenType.IN,
            'EXISTS': SQLTokenType.EXISTS,
            'BETWEEN': SQLTokenType.BETWEEN,
            'LIKE': SQLTokenType.LIKE,
            'ILIKE': SQLTokenType.ILIKE,
            'SIMILAR': SQLTokenType.SIMILAR,
            'TO': SQLTokenType.TO,
            'REGEXP': SQLTokenType.REGEXP,
            'RLIKE': SQLTokenType.RLIKE,
            'IS': SQLTokenType.IS,
            'NULLS': SQLTokenType.NULLS,
            'FIRST': SQLTokenType.FIRST,
            'LAST': SQLTokenType.LAST,
            
            # Literals
            'NULL': SQLTokenType.NULL,
            'TRUE': SQLTokenType.BOOLEAN,
            'FALSE': SQLTokenType.BOOLEAN,
            
            # Functions
            'CASE': SQLTokenType.CASE,
            'WHEN': SQLTokenType.WHEN,
            'THEN': SQLTokenType.THEN,
            'ELSE': SQLTokenType.ELSE,
            'END': SQLTokenType.END,
            'CAST': SQLTokenType.CAST,
            'EXTRACT': SQLTokenType.EXTRACT,
            'COALESCE': SQLTokenType.COALESCE,
            'NULLIF': SQLTokenType.NULLIF,
            'GREATEST': SQLTokenType.GREATEST,
            'LEAST': SQLTokenType.LEAST,
            
            # Aggregates
            'COUNT': SQLTokenType.COUNT,
            'SUM': SQLTokenType.SUM,
            'AVG': SQLTokenType.AVG,
            'MIN': SQLTokenType.MIN,
            'MAX': SQLTokenType.MAX,
            'STDDEV': SQLTokenType.STDDEV,
            'VARIANCE': SQLTokenType.VARIANCE,
            
            # Window functions
            'OVER': SQLTokenType.OVER,
            'PARTITION': SQLTokenType.PARTITION,
            'WINDOW': SQLTokenType.WINDOW,
            'ROWS': SQLTokenType.ROWS,
            'RANGE': SQLTokenType.RANGE,
            'GROUPS': SQLTokenType.GROUPS,
            'UNBOUNDED': SQLTokenType.UNBOUNDED,
            'PRECEDING': SQLTokenType.PRECEDING,
            'FOLLOWING': SQLTokenType.FOLLOWING,
            'CURRENT': SQLTokenType.CURRENT,
            'ROW': SQLTokenType.ROW,
            
            # Set operations
            'UNION': SQLTokenType.UNION,
            'INTERSECT': SQLTokenType.INTERSECT,
            'EXCEPT': SQLTokenType.EXCEPT,
            'MINUS': SQLTokenType.MINUS,
            
            # Transactions
            'COMMIT': SQLTokenType.COMMIT,
            'ROLLBACK': SQLTokenType.ROLLBACK,
            'SAVEPOINT': SQLTokenType.SAVEPOINT,
            'RELEASE': SQLTokenType.RELEASE,
            'START': SQLTokenType.START,
            'BEGIN': SQLTokenType.BEGIN,
            'TRANSACTION': SQLTokenType.TRANSACTION,
            
            # Permissions
            'GRANT': SQLTokenType.GRANT,
            'REVOKE': SQLTokenType.REVOKE,
            'DENY': SQLTokenType.DENY,
            'PRIVILEGES': SQLTokenType.PRIVILEGES,
            'ROLE': SQLTokenType.ROLE,
            'USER': SQLTokenType.USER,
            
            # Modifiers
            'TEMPORARY': SQLTokenType.TEMPORARY,
            'TEMP': SQLTokenType.TEMP,
            'IF': SQLTokenType.IF,
            'ONLY': SQLTokenType.ONLY,
            'REPLACE': SQLTokenType.REPLACE,
            'IGNORE': SQLTokenType.IGNORE,
            
            # Advanced
            'RECURSIVE': SQLTokenType.RECURSIVE,
            'MATERIALIZED': SQLTokenType.MATERIALIZED,
            'REFRESH': SQLTokenType.REFRESH,
            'CONCURRENTLY': SQLTokenType.CONCURRENTLY,
            'COLLATE': SQLTokenType.COLLATE,
            'SEQUENCE': SQLTokenType.SEQUENCE,
            'DOMAIN': SQLTokenType.DOMAIN,
            'TYPE': SQLTokenType.TYPE,
            'ENUM': SQLTokenType.ENUM,
            'COMMENT': SQLTokenType.COMMENT,
            'ANALYZE': SQLTokenType.ANALYZE,
            'VACUUM': SQLTokenType.VACUUM,
            'EXPLAIN': SQLTokenType.EXPLAIN,
            'SHOW': SQLTokenType.SHOW,
            'DESCRIBE': SQLTokenType.DESCRIBE,
            'USE': SQLTokenType.USE,
            'RESET': SQLTokenType.RESET,
        }
        
        # Dialect-specific keywords
        if self.dialect == SQLDialect.MYSQL:
            keywords.update({
                'AUTO_INCREMENT': SQLTokenType.IDENTIFIER,
                'UNSIGNED': SQLTokenType.IDENTIFIER,
                'ZEROFILL': SQLTokenType.IDENTIFIER,
                'ENGINE': SQLTokenType.IDENTIFIER,
                'CHARSET': SQLTokenType.IDENTIFIER,
                'COLLATION': SQLTokenType.IDENTIFIER,
                'LOCK': SQLTokenType.IDENTIFIER,
                'UNLOCK': SQLTokenType.IDENTIFIER,
                'TABLES': SQLTokenType.IDENTIFIER,
            })
        
        elif self.dialect == SQLDialect.POSTGRESQL:
            keywords.update({
                'SERIAL': SQLTokenType.IDENTIFIER,
                'BIGSERIAL': SQLTokenType.IDENTIFIER,
                'SMALLSERIAL': SQLTokenType.IDENTIFIER,
                'BYTEA': SQLTokenType.IDENTIFIER,
                'MONEY': SQLTokenType.IDENTIFIER,
                'INET': SQLTokenType.IDENTIFIER,
                'CIDR': SQLTokenType.IDENTIFIER,
                'MACADDR': SQLTokenType.IDENTIFIER,
                'TSQUERY': SQLTokenType.IDENTIFIER,
                'TSVECTOR': SQLTokenType.IDENTIFIER,
                'POINT': SQLTokenType.IDENTIFIER,
                'LINE': SQLTokenType.IDENTIFIER,
                'LSEG': SQLTokenType.IDENTIFIER,
                'BOX': SQLTokenType.IDENTIFIER,
                'PATH': SQLTokenType.IDENTIFIER,
                'POLYGON': SQLTokenType.IDENTIFIER,
                'CIRCLE': SQLTokenType.IDENTIFIER,
            })
        
        elif self.dialect == SQLDialect.SQLSERVER:
            keywords.update({
                'NCHAR': SQLTokenType.IDENTIFIER,
                'NVARCHAR': SQLTokenType.IDENTIFIER,
                'NTEXT': SQLTokenType.IDENTIFIER,
                'IDENTITY': SQLTokenType.IDENTIFIER,
                'UNIQUEIDENTIFIER': SQLTokenType.IDENTIFIER,
                'ROWVERSION': SQLTokenType.IDENTIFIER,
                'TIMESTAMP': SQLTokenType.IDENTIFIER,
                'MONEY': SQLTokenType.IDENTIFIER,
                'SMALLMONEY': SQLTokenType.IDENTIFIER,
                'GEOGRAPHY': SQLTokenType.IDENTIFIER,
                'GEOMETRY': SQLTokenType.IDENTIFIER,
                'HIERARCHYID': SQLTokenType.IDENTIFIER,
                'SQL_VARIANT': SQLTokenType.IDENTIFIER,
            })
        
        elif self.dialect == SQLDialect.ORACLE:
            keywords.update({
                'NUMBER': SQLTokenType.IDENTIFIER,
                'VARCHAR2': SQLTokenType.IDENTIFIER,
                'NVARCHAR2': SQLTokenType.IDENTIFIER,
                'CLOB': SQLTokenType.IDENTIFIER,
                'NCLOB': SQLTokenType.IDENTIFIER,
                'LONG': SQLTokenType.IDENTIFIER,
                'RAW': SQLTokenType.IDENTIFIER,
                'LONG_RAW': SQLTokenType.IDENTIFIER,
                'ROWID': SQLTokenType.IDENTIFIER,
                'UROWID': SQLTokenType.IDENTIFIER,
                'BFILE': SQLTokenType.IDENTIFIER,
                'XMLTYPE': SQLTokenType.IDENTIFIER,
                'CONNECT': SQLTokenType.IDENTIFIER,
                'PRIOR': SQLTokenType.IDENTIFIER,
                'LEVEL': SQLTokenType.IDENTIFIER,
                'ROWNUM': SQLTokenType.IDENTIFIER,
            })
        
        return keywords
    
    def _build_operators(self) -> Dict[str, SQLOperator]:
        """Build operator mapping."""
        return {
            '+': SQLOperator.PLUS,
            '-': SQLOperator.MINUS,
            '*': SQLOperator.MULTIPLY,
            '/': SQLOperator.DIVIDE,
            '%': SQLOperator.MODULO,
            '^': SQLOperator.POWER,
            '=': SQLOperator.EQUAL,
            '<>': SQLOperator.NOT_EQUAL,
            '!=': SQLOperator.NOT_EQUAL_ALT,
            '<': SQLOperator.LESS_THAN,
            '>': SQLOperator.GREATER_THAN,
            '<=': SQLOperator.LESS_EQUAL,
            '>=': SQLOperator.GREATER_EQUAL,
            '||': SQLOperator.CONCAT,
            '&': SQLOperator.BITWISE_AND,
            '|': SQLOperator.BITWISE_OR,
            '~': SQLOperator.BITWISE_NOT,
            '<<': SQLOperator.BITWISE_SHIFT_LEFT,
            '>>': SQLOperator.BITWISE_SHIFT_RIGHT,
            ':=': SQLOperator.ASSIGN,
            '->': SQLOperator.JSON_EXTRACT,
            '->>': SQLOperator.JSON_EXTRACT_TEXT,
            '#>': SQLOperator.JSON_PATH,
            '#>>': SQLOperator.JSON_PATH_TEXT,
            '@>': SQLOperator.JSON_CONTAINS,
            '<@': SQLOperator.JSON_CONTAINED,
            '?': SQLOperator.JSON_EXISTS,
            '?|': SQLOperator.JSON_EXISTS_ANY,
            '?&': SQLOperator.JSON_EXISTS_ALL,
            '&&': SQLOperator.ARRAY_OVERLAP,
        }
    
    def tokenize(self, text: str) -> List[SQLToken]:
        """
        Tokenize SQL source code.
        
        Args:
            text: SQL source code to tokenize
            
        Returns:
            List of SQL tokens
        """
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        while self.position < len(self.text):
            if not self._scan_token():
                # Skip unknown character
                self._advance()
        
        # Add EOF token
        self.tokens.append(SQLToken(SQLTokenType.EOF, '', self.line, self.column))
        
        # Filter out whitespace and comments unless needed
        filtered_tokens = []
        for token in self.tokens:
            if token.type not in [SQLTokenType.WHITESPACE, SQLTokenType.COMMENT, SQLTokenType.MULTILINE_COMMENT]:
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def _scan_token(self) -> bool:
        """Scan for the next token."""
        if self.position >= len(self.text):
            return False
        
        # Try each pattern
        for pattern, token_type in self.token_patterns:
            match = pattern.match(self.text, self.position)
            if match:
                value = match.group(0)
                
                # Handle keywords vs identifiers
                if token_type == SQLTokenType.IDENTIFIER:
                    upper_value = value.upper()
                    if upper_value in self.keywords:
                        token_type = self.keywords[upper_value]
                        # Special handling for boolean literals
                        if upper_value in ['TRUE', 'FALSE']:
                            token_type = SQLTokenType.BOOLEAN
                        elif upper_value == 'NULL':
                            token_type = SQLTokenType.NULL
                
                # Handle quoted identifiers
                elif token_type == SQLTokenType.QUOTED_IDENTIFIER:
                    # Remove quotes
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith('`') and value.endswith('`'):
                        value = value[1:-1]
                
                # Handle string literals
                elif token_type == SQLTokenType.STRING:
                    # Remove quotes and handle escape sequences
                    value = value[1:-1]  # Remove outer quotes
                    value = value.replace("''", "'")  # Handle escaped quotes
                
                # Create token
                token = SQLToken(
                    type=token_type,
                    value=value,
                    line=self.line,
                    column=self.column,
                    length=len(match.group(0))
                )
                
                self.tokens.append(token)
                
                # Update position
                self._advance(len(match.group(0)))
                
                return True
        
        return False
    
    def _advance(self, count: int = 1):
        """Advance position and update line/column tracking."""
        for _ in range(count):
            if self.position < len(self.text):
                if self.text[self.position] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.position += 1


class SQLParseError(Exception):
    """SQL parsing error."""
    
    def __init__(self, message: str, token: Optional[SQLToken] = None):
        super().__init__(message)
        self.token = token
        self.message = message
    
    def __str__(self):
        if self.token:
            return f"Parse error at line {self.token.line}, column {self.token.column}: {self.message}"
        return f"Parse error: {self.message}"


class SQLParser:
    """
    SQL parser using recursive descent parsing.
    
    Supports comprehensive SQL parsing including:
    - DDL statements (CREATE, ALTER, DROP)
    - DML statements (SELECT, INSERT, UPDATE, DELETE)
    - DCL statements (GRANT, REVOKE, DENY)
    - Complex queries with JOINs, subqueries, CTEs
    - Window functions and advanced SQL features
    """
    
    def __init__(self, dialect: SQLDialect = SQLDialect.ANSI):
        """
        Initialize the SQL parser.
        
        Args:
            dialect: SQL dialect to use for parsing
        """
        self.dialect = dialect
        self.lexer = SQLLexer(dialect)
        self.logger = logging.getLogger(__name__)
        
        # Parser state
        self.tokens = []
        self.current = 0
        self.errors = []
        
        # Operator precedence
        self.precedence = {
            SQLTokenType.OR: 1,
            SQLTokenType.AND: 2,
            SQLTokenType.NOT: 3,
            SQLTokenType.EQUAL: 4,
            SQLTokenType.NOT_EQUAL: 4,
            SQLTokenType.LESS_THAN: 4,
            SQLTokenType.GREATER_THAN: 4,
            SQLTokenType.LESS_EQUAL: 4,
            SQLTokenType.GREATER_EQUAL: 4,
            SQLTokenType.LIKE: 4,
            SQLTokenType.ILIKE: 4,
            SQLTokenType.IN: 4,
            SQLTokenType.EXISTS: 4,
            SQLTokenType.BETWEEN: 4,
            SQLTokenType.IS: 4,
            SQLTokenType.PLUS: 5,
            SQLTokenType.MINUS: 5,
            SQLTokenType.MULTIPLY: 6,
            SQLTokenType.DIVIDE: 6,
            SQLTokenType.MODULO: 6,
            SQLTokenType.POWER: 7,
            SQLTokenType.CONCAT: 5,
            SQLTokenType.BITWISE_AND: 3,
            SQLTokenType.BITWISE_OR: 2,
            SQLTokenType.BITWISE_XOR: 2,
            SQLTokenType.SHIFT_LEFT: 5,
            SQLTokenType.SHIFT_RIGHT: 5,
        }
    
    def parse(self, text: str) -> SQLProgram:
        """
        Parse SQL source code into an AST.
        
        Args:
            text: SQL source code to parse
            
        Returns:
            SQLProgram: Root AST node
            
        Raises:
            SQLParseError: If parsing fails
        """
        try:
            # Tokenize
            self.tokens = self.lexer.tokenize(text)
            self.current = 0
            self.errors = []
            
            # Parse program
            program = self._parse_program()
            
            if self.errors:
                error_msg = "; ".join(self.errors)
                raise SQLParseError(f"Parse errors: {error_msg}")
            
            return program
            
        except Exception as e:
            self.logger.error(f"SQL parsing failed: {e}")
            raise SQLParseError(f"Failed to parse SQL: {e}")
    
    def _parse_program(self) -> SQLProgram:
        """Parse a complete SQL program."""
        statements = []
        
        while not self._is_at_end():
            if self._check(SQLTokenType.SEMICOLON):
                self._advance()  # Skip empty statements
                continue
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            
            # Optional semicolon
            if self._check(SQLTokenType.SEMICOLON):
                self._advance()
        
        return SQLProgram(statements=statements)
    
    def _parse_statement(self) -> Optional[SQLStatement]:
        """Parse a SQL statement."""
        try:
            if self._check(SQLTokenType.SELECT):
                return self._parse_select_statement()
            elif self._check(SQLTokenType.INSERT):
                return self._parse_insert_statement()
            elif self._check(SQLTokenType.UPDATE):
                return self._parse_update_statement()
            elif self._check(SQLTokenType.DELETE):
                return self._parse_delete_statement()
            elif self._check(SQLTokenType.CREATE):
                return self._parse_create_statement()
            elif self._check(SQLTokenType.DROP):
                return self._parse_drop_statement()
            elif self._check(SQLTokenType.ALTER):
                return self._parse_alter_statement()
            elif self._check(SQLTokenType.WITH):
                return self._parse_with_statement()
            else:
                self._error(f"Unexpected token: {self._peek().value}")
                return None
                
        except SQLParseError as e:
            self.errors.append(str(e))
            self._synchronize()
            return None
    
    def _parse_select_statement(self) -> SQLSelectStatement:
        """Parse SELECT statement."""
        self._consume(SQLTokenType.SELECT, "Expected 'SELECT'")
        
        # Handle DISTINCT
        distinct = False
        distinct_on = []
        if self._check(SQLTokenType.DISTINCT):
            distinct = True
            self._advance()
            
            # PostgreSQL DISTINCT ON
            if self._check(SQLTokenType.LPAREN):
                self._advance()
                distinct_on.append(self._parse_expression())
                while self._check(SQLTokenType.COMMA):
                    self._advance()
                    distinct_on.append(self._parse_expression())
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        # Parse select list
        select_list = []
        if not self._check(SQLTokenType.FROM):
            select_list.append(self._parse_expression())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                select_list.append(self._parse_expression())
        
        # Parse FROM clause
        from_clause = None
        if self._check(SQLTokenType.FROM):
            from_clause = self._parse_from_clause()
        
        # Parse WHERE clause
        where_clause = None
        if self._check(SQLTokenType.WHERE):
            where_clause = self._parse_where_clause()
        
        # Parse GROUP BY clause
        group_by_clause = None
        if self._check(SQLTokenType.GROUP) and self._check_next(SQLTokenType.BY):
            group_by_clause = self._parse_group_by_clause()
        
        # Parse HAVING clause
        having_clause = None
        if self._check(SQLTokenType.HAVING):
            having_clause = self._parse_having_clause()
        
        # Parse ORDER BY clause
        order_by_clause = None
        if self._check(SQLTokenType.ORDER) and self._check_next(SQLTokenType.BY):
            order_by_clause = self._parse_order_by_clause()
        
        # Parse LIMIT clause
        limit_clause = None
        if self._check(SQLTokenType.LIMIT):
            limit_clause = self._parse_limit_clause()
        
        # Parse OFFSET clause
        offset_clause = None
        if self._check(SQLTokenType.OFFSET):
            offset_clause = self._parse_offset_clause()
        
        return SQLSelectStatement(
            select_list=select_list,
            from_clause=from_clause,
            where_clause=where_clause,
            group_by_clause=group_by_clause,
            having_clause=having_clause,
            order_by_clause=order_by_clause,
            limit_clause=limit_clause,
            offset_clause=offset_clause,
            distinct=distinct,
            distinct_on=distinct_on
        )
    
    def _parse_insert_statement(self) -> SQLInsertStatement:
        """Parse INSERT statement."""
        self._consume(SQLTokenType.INSERT, "Expected 'INSERT'")
        self._consume(SQLTokenType.INTO, "Expected 'INTO'")
        
        # Parse table name
        table = self._parse_identifier()
        
        # Parse column list
        columns = []
        if self._check(SQLTokenType.LPAREN):
            self._advance()
            columns.append(self._parse_identifier())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                columns.append(self._parse_identifier())
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        # Parse VALUES or SELECT
        values = []
        select_query = None
        
        if self._check(SQLTokenType.VALUES):
            self._advance()
            # Parse value lists
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            value_list = []
            value_list.append(self._parse_expression())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                value_list.append(self._parse_expression())
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            values.append(value_list)
            
            # Handle multiple value lists
            while self._check(SQLTokenType.COMMA):
                self._advance()
                self._consume(SQLTokenType.LPAREN, "Expected '('")
                value_list = []
                value_list.append(self._parse_expression())
                while self._check(SQLTokenType.COMMA):
                    self._advance()
                    value_list.append(self._parse_expression())
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
                values.append(value_list)
        
        elif self._check(SQLTokenType.SELECT):
            select_query = self._parse_select_statement()
        
        return SQLInsertStatement(
            table=table,
            columns=columns,
            values=values,
            select_query=select_query
        )
    
    def _parse_update_statement(self) -> SQLUpdateStatement:
        """Parse UPDATE statement."""
        self._consume(SQLTokenType.UPDATE, "Expected 'UPDATE'")
        
        # Parse table name
        table = self._parse_identifier()
        
        # Parse SET clause
        self._consume(SQLTokenType.SET, "Expected 'SET'")
        set_clauses = []
        
        column = self._parse_identifier()
        self._consume(SQLTokenType.EQUAL, "Expected '='")
        value = self._parse_expression()
        set_clauses.append((column, value))
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            column = self._parse_identifier()
            self._consume(SQLTokenType.EQUAL, "Expected '='")
            value = self._parse_expression()
            set_clauses.append((column, value))
        
        # Parse WHERE clause
        where_clause = None
        if self._check(SQLTokenType.WHERE):
            where_clause = self._parse_where_clause()
        
        return SQLUpdateStatement(
            table=table,
            set_clauses=set_clauses,
            where_clause=where_clause
        )
    
    def _parse_delete_statement(self) -> SQLDeleteStatement:
        """Parse DELETE statement."""
        self._consume(SQLTokenType.DELETE, "Expected 'DELETE'")
        self._consume(SQLTokenType.FROM, "Expected 'FROM'")
        
        # Parse table name
        table = self._parse_identifier()
        
        # Parse WHERE clause
        where_clause = None
        if self._check(SQLTokenType.WHERE):
            where_clause = self._parse_where_clause()
        
        return SQLDeleteStatement(
            table=table,
            where_clause=where_clause
        )
    
    def _parse_create_statement(self) -> SQLStatement:
        """Parse CREATE statement."""
        self._consume(SQLTokenType.CREATE, "Expected 'CREATE'")
        
        if self._check(SQLTokenType.TABLE):
            return self._parse_create_table_statement()
        else:
            self._error("Unsupported CREATE statement")
            return None
    
    def _parse_create_table_statement(self) -> SQLCreateTableStatement:
        """Parse CREATE TABLE statement."""
        self._consume(SQLTokenType.TABLE, "Expected 'TABLE'")
        
        # Handle IF NOT EXISTS
        if_not_exists = False
        if self._check(SQLTokenType.IF):
            self._advance()
            self._consume(SQLTokenType.NOT, "Expected 'NOT'")
            self._consume(SQLTokenType.EXISTS, "Expected 'EXISTS'")
            if_not_exists = True
        
        # Parse table name
        table_name = self._parse_identifier()
        
        # Parse column definitions
        columns = []
        constraints = []
        
        self._consume(SQLTokenType.LPAREN, "Expected '('")
        
        # Parse first column or constraint
        if self._check(SQLTokenType.CONSTRAINT):
            constraints.append(self._parse_constraint())
        else:
            columns.append(self._parse_column_definition())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            if self._check(SQLTokenType.CONSTRAINT):
                constraints.append(self._parse_constraint())
            else:
                columns.append(self._parse_column_definition())
        
        self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        return SQLCreateTableStatement(
            table_name=table_name,
            columns=columns,
            constraints=constraints,
            if_not_exists=if_not_exists
        )
    
    def _parse_drop_statement(self) -> SQLStatement:
        """Parse DROP statement."""
        self._consume(SQLTokenType.DROP, "Expected 'DROP'")
        
        if self._check(SQLTokenType.TABLE):
            return self._parse_drop_table_statement()
        else:
            self._error("Unsupported DROP statement")
            return None
    
    def _parse_drop_table_statement(self) -> SQLDropTableStatement:
        """Parse DROP TABLE statement."""
        self._consume(SQLTokenType.TABLE, "Expected 'TABLE'")
        
        # Handle IF EXISTS
        if_exists = False
        if self._check(SQLTokenType.IF):
            self._advance()
            self._consume(SQLTokenType.EXISTS, "Expected 'EXISTS'")
            if_exists = True
        
        # Parse table names
        table_names = []
        table_names.append(self._parse_identifier())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            table_names.append(self._parse_identifier())
        
        return SQLDropTableStatement(
            table_names=table_names,
            if_exists=if_exists
        )
    
    def _parse_alter_statement(self) -> SQLStatement:
        """Parse ALTER statement."""
        self._consume(SQLTokenType.ALTER, "Expected 'ALTER'")
        
        if self._check(SQLTokenType.TABLE):
            return self._parse_alter_table_statement()
        else:
            self._error("Unsupported ALTER statement")
            return None
    
    def _parse_alter_table_statement(self) -> SQLAlterTableStatement:
        """Parse ALTER TABLE statement."""
        self._consume(SQLTokenType.TABLE, "Expected 'TABLE'")
        
        # Parse table name
        table_name = self._parse_identifier()
        
        # Parse actions
        actions = []
        actions.append(self._parse_alter_table_action())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            actions.append(self._parse_alter_table_action())
        
        return SQLAlterTableStatement(
            table_name=table_name,
            actions=actions
        )
    
    def _parse_alter_table_action(self) -> SQLAlterTableAction:
        """Parse ALTER TABLE action."""
        if self._check(SQLTokenType.ADD):
            self._advance()
            if self._check(SQLTokenType.CONSTRAINT):
                constraint = self._parse_constraint()
                return SQLAddConstraintAction(constraint=constraint)
            else:
                column = self._parse_column_definition()
                return SQLAddColumnAction(column=column)
        
        elif self._check(SQLTokenType.DROP):
            self._advance()
            if self._check(SQLTokenType.CONSTRAINT):
                self._advance()
                constraint_name = self._parse_identifier()
                return SQLDropConstraintAction(constraint_name=constraint_name)
            else:
                column_name = self._parse_identifier()
                return SQLDropColumnAction(column_name=column_name)
        
        else:
            self._error("Unsupported ALTER TABLE action")
            return None
    
    def _parse_with_statement(self) -> SQLSelectStatement:
        """Parse WITH statement (CTE)."""
        with_clause = self._parse_with_clause()
        
        # Parse main query
        main_query = self._parse_select_statement()
        main_query.with_clause = with_clause
        
        return main_query
    
    def _parse_with_clause(self) -> SQLWithClause:
        """Parse WITH clause."""
        self._consume(SQLTokenType.WITH, "Expected 'WITH'")
        
        # Handle RECURSIVE
        recursive = False
        if self._check(SQLTokenType.RECURSIVE):
            recursive = True
            self._advance()
        
        # Parse CTEs
        cte_list = []
        cte_list.append(self._parse_cte())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            cte_list.append(self._parse_cte())
        
        return SQLWithClause(
            cte_list=cte_list,
            recursive=recursive
        )
    
    def _parse_cte(self) -> SQLCommonTableExpression:
        """Parse Common Table Expression."""
        # Parse CTE name
        name = self._parse_identifier()
        
        # Parse optional column list
        columns = []
        if self._check(SQLTokenType.LPAREN):
            self._advance()
            columns.append(self._parse_identifier())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                columns.append(self._parse_identifier())
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        # Parse AS
        self._consume(SQLTokenType.AS, "Expected 'AS'")
        
        # Parse query
        self._consume(SQLTokenType.LPAREN, "Expected '('")
        query = self._parse_select_statement()
        self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        return SQLCommonTableExpression(
            name=name,
            columns=columns,
            query=query
        )
    
    def _parse_from_clause(self) -> SQLFromClause:
        """Parse FROM clause."""
        self._consume(SQLTokenType.FROM, "Expected 'FROM'")
        
        table_references = []
        table_references.append(self._parse_table_reference())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            table_references.append(self._parse_table_reference())
        
        return SQLFromClause(table_references=table_references)
    
    def _parse_table_reference(self) -> SQLTableReference:
        """Parse table reference."""
        # Handle subquery
        if self._check(SQLTokenType.LPAREN):
            self._advance()
            query = self._parse_select_statement()
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            
            alias = None
            if self._check(SQLTokenType.AS):
                self._advance()
                alias = self._parse_identifier()
            elif self._check(SQLTokenType.IDENTIFIER):
                alias = self._parse_identifier()
            
            return SQLDerivedTable(query=query, alias=alias)
        
        # Parse table name
        table_name = self._parse_identifier()
        
        # Parse alias
        alias = None
        if self._check(SQLTokenType.AS):
            self._advance()
            alias = self._parse_identifier()
        elif self._check(SQLTokenType.IDENTIFIER):
            alias = self._parse_identifier()
        
        table_ref = SQLTableName(name=table_name, alias=alias)
        
        # Handle JOINs
        while self._check_join():
            table_ref = self._parse_join(table_ref)
        
        return table_ref
    
    def _parse_join(self, left: SQLTableReference) -> SQLJoin:
        """Parse JOIN operation."""
        join_type = JoinType.INNER
        
        if self._check(SQLTokenType.NATURAL):
            self._advance()
            join_type = JoinType.NATURAL
        elif self._check(SQLTokenType.CROSS):
            self._advance()
            join_type = JoinType.CROSS
        elif self._check(SQLTokenType.INNER):
            self._advance()
            join_type = JoinType.INNER
        elif self._check(SQLTokenType.LEFT):
            self._advance()
            join_type = JoinType.LEFT
            if self._check(SQLTokenType.OUTER):
                self._advance()
        elif self._check(SQLTokenType.RIGHT):
            self._advance()
            join_type = JoinType.RIGHT
            if self._check(SQLTokenType.OUTER):
                self._advance()
        elif self._check(SQLTokenType.FULL):
            self._advance()
            join_type = JoinType.FULL
            if self._check(SQLTokenType.OUTER):
                self._advance()
        
        self._consume(SQLTokenType.JOIN, "Expected 'JOIN'")
        
        # Parse right table reference
        right = self._parse_table_reference()
        
        # Parse join condition
        condition = None
        using_columns = []
        
        if self._check(SQLTokenType.ON):
            self._advance()
            condition = self._parse_expression()
        elif self._check(SQLTokenType.USING):
            self._advance()
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            using_columns.append(self._parse_identifier())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                using_columns.append(self._parse_identifier())
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        return SQLJoin(
            join_type=join_type,
            left=left,
            right=right,
            condition=condition,
            using_columns=using_columns
        )
    
    def _parse_where_clause(self) -> SQLWhereClause:
        """Parse WHERE clause."""
        self._consume(SQLTokenType.WHERE, "Expected 'WHERE'")
        condition = self._parse_expression()
        return SQLWhereClause(condition=condition)
    
    def _parse_group_by_clause(self) -> SQLGroupByClause:
        """Parse GROUP BY clause."""
        self._consume(SQLTokenType.GROUP, "Expected 'GROUP'")
        self._consume(SQLTokenType.BY, "Expected 'BY'")
        
        expressions = []
        expressions.append(self._parse_expression())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            expressions.append(self._parse_expression())
        
        return SQLGroupByClause(expressions=expressions)
    
    def _parse_having_clause(self) -> SQLHavingClause:
        """Parse HAVING clause."""
        self._consume(SQLTokenType.HAVING, "Expected 'HAVING'")
        condition = self._parse_expression()
        return SQLHavingClause(condition=condition)
    
    def _parse_order_by_clause(self) -> SQLOrderByClause:
        """Parse ORDER BY clause."""
        self._consume(SQLTokenType.ORDER, "Expected 'ORDER'")
        self._consume(SQLTokenType.BY, "Expected 'BY'")
        
        expressions = []
        expressions.append(self._parse_order_by_expression())
        
        while self._check(SQLTokenType.COMMA):
            self._advance()
            expressions.append(self._parse_order_by_expression())
        
        return SQLOrderByClause(expressions=expressions)
    
    def _parse_order_by_expression(self) -> SQLOrderByExpression:
        """Parse ORDER BY expression."""
        expression = self._parse_expression()
        
        ascending = True
        if self._check(SQLTokenType.IDENTIFIER):
            token = self._peek()
            if token.value.upper() == 'ASC':
                self._advance()
                ascending = True
            elif token.value.upper() == 'DESC':
                self._advance()
                ascending = False
        
        nulls_first = None
        if self._check(SQLTokenType.NULLS):
            self._advance()
            if self._check(SQLTokenType.FIRST):
                self._advance()
                nulls_first = True
            elif self._check(SQLTokenType.LAST):
                self._advance()
                nulls_first = False
        
        return SQLOrderByExpression(
            expression=expression,
            ascending=ascending,
            nulls_first=nulls_first
        )
    
    def _parse_limit_clause(self) -> SQLLimitClause:
        """Parse LIMIT clause."""
        self._consume(SQLTokenType.LIMIT, "Expected 'LIMIT'")
        count = self._parse_expression()
        return SQLLimitClause(count=count)
    
    def _parse_offset_clause(self) -> SQLOffsetClause:
        """Parse OFFSET clause."""
        self._consume(SQLTokenType.OFFSET, "Expected 'OFFSET'")
        count = self._parse_expression()
        return SQLOffsetClause(count=count)
    
    def _parse_expression(self) -> SQLExpression:
        """Parse expression with precedence."""
        return self._parse_or_expression()
    
    def _parse_or_expression(self) -> SQLExpression:
        """Parse OR expression."""
        expr = self._parse_and_expression()
        
        while self._check(SQLTokenType.OR):
            operator = self._advance()
            right = self._parse_and_expression()
            expr = SQLBinaryExpression(
                left=expr,
                operator=SQLOperator.OR,
                right=right
            )
        
        return expr
    
    def _parse_and_expression(self) -> SQLExpression:
        """Parse AND expression."""
        expr = self._parse_equality_expression()
        
        while self._check(SQLTokenType.AND):
            operator = self._advance()
            right = self._parse_equality_expression()
            expr = SQLBinaryExpression(
                left=expr,
                operator=SQLOperator.AND,
                right=right
            )
        
        return expr
    
    def _parse_equality_expression(self) -> SQLExpression:
        """Parse equality expression."""
        expr = self._parse_comparison_expression()
        
        while self._check(SQLTokenType.EQUAL, SQLTokenType.NOT_EQUAL):
            operator_token = self._advance()
            right = self._parse_comparison_expression()
            
            if operator_token.type == SQLTokenType.EQUAL:
                operator = SQLOperator.EQUAL
            else:
                operator = SQLOperator.NOT_EQUAL
            
            expr = SQLBinaryExpression(
                left=expr,
                operator=operator,
                right=right
            )
        
        return expr
    
    def _parse_comparison_expression(self) -> SQLExpression:
        """Parse comparison expression."""
        expr = self._parse_term_expression()
        
        while self._check(SQLTokenType.LESS_THAN, SQLTokenType.GREATER_THAN,
                          SQLTokenType.LESS_EQUAL, SQLTokenType.GREATER_EQUAL,
                          SQLTokenType.LIKE, SQLTokenType.ILIKE, SQLTokenType.IN,
                          SQLTokenType.BETWEEN, SQLTokenType.IS):
            
            if self._check(SQLTokenType.LIKE, SQLTokenType.ILIKE):
                operator_token = self._advance()
                pattern = self._parse_term_expression()
                
                # Handle ESCAPE
                escape = None
                if self._check(SQLTokenType.IDENTIFIER) and self._peek().value.upper() == 'ESCAPE':
                    self._advance()
                    escape = self._parse_term_expression()
                
                case_insensitive = operator_token.type == SQLTokenType.ILIKE
                expr = SQLLikeExpression(
                    expression=expr,
                    pattern=pattern,
                    escape=escape,
                    case_insensitive=case_insensitive
                )
            
            elif self._check(SQLTokenType.IN):
                self._advance()
                
                # Handle NOT IN
                negated = False
                if self._previous().type == SQLTokenType.NOT:
                    negated = True
                
                self._consume(SQLTokenType.LPAREN, "Expected '('")
                
                # Check for subquery
                if self._check(SQLTokenType.SELECT):
                    subquery = self._parse_select_statement()
                    self._consume(SQLTokenType.RPAREN, "Expected ')'")
                    expr = SQLInExpression(
                        expression=expr,
                        values=[SQLSubquery(query=subquery)],
                        negated=negated
                    )
                else:
                    # Value list
                    values = []
                    values.append(self._parse_expression())
                    while self._check(SQLTokenType.COMMA):
                        self._advance()
                        values.append(self._parse_expression())
                    self._consume(SQLTokenType.RPAREN, "Expected ')'")
                    
                    expr = SQLInExpression(
                        expression=expr,
                        values=values,
                        negated=negated
                    )
            
            elif self._check(SQLTokenType.BETWEEN):
                self._advance()
                
                # Handle NOT BETWEEN
                negated = False
                if self._previous().type == SQLTokenType.NOT:
                    negated = True
                
                lower_bound = self._parse_term_expression()
                self._consume(SQLTokenType.AND, "Expected 'AND'")
                upper_bound = self._parse_term_expression()
                
                expr = SQLBetweenExpression(
                    expression=expr,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    negated=negated
                )
            
            elif self._check(SQLTokenType.IS):
                self._advance()
                
                # Handle IS NULL, IS NOT NULL
                if self._check(SQLTokenType.NOT):
                    self._advance()
                    self._consume(SQLTokenType.NULL, "Expected 'NULL'")
                    expr = SQLUnaryExpression(
                        operator=SQLOperator.IS_NOT_NULL,
                        operand=expr
                    )
                elif self._check(SQLTokenType.NULL):
                    self._advance()
                    expr = SQLUnaryExpression(
                        operator=SQLOperator.IS_NULL,
                        operand=expr
                    )
                else:
                    right = self._parse_term_expression()
                    expr = SQLBinaryExpression(
                        left=expr,
                        operator=SQLOperator.EQUAL,
                        right=right
                    )
            
            else:
                operator_token = self._advance()
                right = self._parse_term_expression()
                
                operator_map = {
                    SQLTokenType.LESS_THAN: SQLOperator.LESS_THAN,
                    SQLTokenType.GREATER_THAN: SQLOperator.GREATER_THAN,
                    SQLTokenType.LESS_EQUAL: SQLOperator.LESS_EQUAL,
                    SQLTokenType.GREATER_EQUAL: SQLOperator.GREATER_EQUAL,
                }
                
                operator = operator_map.get(operator_token.type, SQLOperator.EQUAL)
                expr = SQLBinaryExpression(
                    left=expr,
                    operator=operator,
                    right=right
                )
        
        return expr
    
    def _parse_term_expression(self) -> SQLExpression:
        """Parse term expression."""
        expr = self._parse_factor_expression()
        
        while self._check(SQLTokenType.PLUS, SQLTokenType.MINUS, SQLTokenType.CONCAT):
            operator_token = self._advance()
            right = self._parse_factor_expression()
            
            operator_map = {
                SQLTokenType.PLUS: SQLOperator.PLUS,
                SQLTokenType.MINUS: SQLOperator.MINUS,
                SQLTokenType.CONCAT: SQLOperator.CONCAT,
            }
            
            operator = operator_map.get(operator_token.type, SQLOperator.PLUS)
            expr = SQLBinaryExpression(
                left=expr,
                operator=operator,
                right=right
            )
        
        return expr
    
    def _parse_factor_expression(self) -> SQLExpression:
        """Parse factor expression."""
        expr = self._parse_unary_expression()
        
        while self._check(SQLTokenType.MULTIPLY, SQLTokenType.DIVIDE, SQLTokenType.MODULO):
            operator_token = self._advance()
            right = self._parse_unary_expression()
            
            operator_map = {
                SQLTokenType.MULTIPLY: SQLOperator.MULTIPLY,
                SQLTokenType.DIVIDE: SQLOperator.DIVIDE,
                SQLTokenType.MODULO: SQLOperator.MODULO,
            }
            
            operator = operator_map.get(operator_token.type, SQLOperator.MULTIPLY)
            expr = SQLBinaryExpression(
                left=expr,
                operator=operator,
                right=right
            )
        
        return expr
    
    def _parse_unary_expression(self) -> SQLExpression:
        """Parse unary expression."""
        if self._check(SQLTokenType.NOT, SQLTokenType.PLUS, SQLTokenType.MINUS):
            operator_token = self._advance()
            operand = self._parse_unary_expression()
            
            operator_map = {
                SQLTokenType.NOT: SQLOperator.NOT,
                SQLTokenType.PLUS: SQLOperator.PLUS,
                SQLTokenType.MINUS: SQLOperator.MINUS,
            }
            
            operator = operator_map.get(operator_token.type, SQLOperator.NOT)
            return SQLUnaryExpression(
                operator=operator,
                operand=operand
            )
        
        return self._parse_primary_expression()
    
    def _parse_primary_expression(self) -> SQLExpression:
        """Parse primary expression."""
        # Handle literals
        if self._check(SQLTokenType.INTEGER):
            token = self._advance()
            return SQLIntegerLiteral(value=int(token.value))
        
        if self._check(SQLTokenType.FLOAT):
            token = self._advance()
            return SQLFloatLiteral(value=float(token.value))
        
        if self._check(SQLTokenType.STRING):
            token = self._advance()
            return SQLStringLiteral(value=token.value)
        
        if self._check(SQLTokenType.BOOLEAN):
            token = self._advance()
            return SQLBooleanLiteral(value=token.value.upper() == 'TRUE')
        
        if self._check(SQLTokenType.NULL):
            token = self._advance()
            return SQLNullLiteral()
        
        # Handle parenthesized expressions
        if self._check(SQLTokenType.LPAREN):
            self._advance()
            
            # Check for subquery
            if self._check(SQLTokenType.SELECT):
                query = self._parse_select_statement()
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
                return SQLSubquery(query=query)
            else:
                expr = self._parse_expression()
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
                return expr
        
        # Handle CASE expression
        if self._check(SQLTokenType.CASE):
            return self._parse_case_expression()
        
        # Handle CAST expression
        if self._check(SQLTokenType.CAST):
            return self._parse_cast_expression()
        
        # Handle EXISTS
        if self._check(SQLTokenType.EXISTS):
            self._advance()
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            query = self._parse_select_statement()
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            return SQLExistsExpression(subquery=SQLSubquery(query=query))
        
        # Handle function calls and identifiers
        if self._check(SQLTokenType.IDENTIFIER):
            name = self._advance().value
            
            # Check for function call
            if self._check(SQLTokenType.LPAREN):
                self._advance()
                
                # Handle empty argument list
                arguments = []
                if not self._check(SQLTokenType.RPAREN):
                    arguments.append(self._parse_expression())
                    while self._check(SQLTokenType.COMMA):
                        self._advance()
                        arguments.append(self._parse_expression())
                
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
                
                return SQLFunctionCall(name=name, arguments=arguments)
            
            # Handle column reference
            else:
                # Check for qualified identifier
                if self._check(SQLTokenType.DOT):
                    self._advance()
                    column = self._consume(SQLTokenType.IDENTIFIER, "Expected column name").value
                    return SQLColumnReference(table=name, column=column)
                else:
                    return SQLColumnReference(column=name)
        
        # Handle wildcard
        if self._check(SQLTokenType.MULTIPLY):
            self._advance()
            return SQLColumnReference(column="*")
        
        self._error(f"Unexpected token: {self._peek().value}")
        return None
    
    def _parse_case_expression(self) -> SQLCaseExpression:
        """Parse CASE expression."""
        self._consume(SQLTokenType.CASE, "Expected 'CASE'")
        
        # Handle simple vs searched CASE
        expression = None
        if not self._check(SQLTokenType.WHEN):
            expression = self._parse_expression()
        
        # Parse WHEN clauses
        when_clauses = []
        while self._check(SQLTokenType.WHEN):
            self._advance()
            when_expr = self._parse_expression()
            self._consume(SQLTokenType.THEN, "Expected 'THEN'")
            then_expr = self._parse_expression()
            when_clauses.append((when_expr, then_expr))
        
        # Parse ELSE clause
        else_clause = None
        if self._check(SQLTokenType.ELSE):
            self._advance()
            else_clause = self._parse_expression()
        
        self._consume(SQLTokenType.END, "Expected 'END'")
        
        return SQLCaseExpression(
            expression=expression,
            when_clauses=when_clauses,
            else_clause=else_clause
        )
    
    def _parse_cast_expression(self) -> SQLCastExpression:
        """Parse CAST expression."""
        self._consume(SQLTokenType.CAST, "Expected 'CAST'")
        self._consume(SQLTokenType.LPAREN, "Expected '('")
        
        expression = self._parse_expression()
        self._consume(SQLTokenType.AS, "Expected 'AS'")
        target_type = self._parse_data_type()
        
        self._consume(SQLTokenType.RPAREN, "Expected ')'")
        
        return SQLCastExpression(
            expression=expression,
            target_type=target_type
        )
    
    def _parse_data_type(self) -> SQLDataType:
        """Parse data type."""
        if self._check(SQLTokenType.INTEGER_TYPE):
            self._advance()
            return SQLIntegerType()
        
        elif self._check(SQLTokenType.VARCHAR):
            self._advance()
            length = None
            if self._check(SQLTokenType.LPAREN):
                self._advance()
                length_token = self._consume(SQLTokenType.INTEGER, "Expected integer")
                length = int(length_token.value)
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
            return SQLVarcharType(length=length)
        
        elif self._check(SQLTokenType.DECIMAL):
            self._advance()
            precision = None
            scale = None
            if self._check(SQLTokenType.LPAREN):
                self._advance()
                precision_token = self._consume(SQLTokenType.INTEGER, "Expected integer")
                precision = int(precision_token.value)
                if self._check(SQLTokenType.COMMA):
                    self._advance()
                    scale_token = self._consume(SQLTokenType.INTEGER, "Expected integer")
                    scale = int(scale_token.value)
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
            return SQLDecimalType(precision=precision, scale=scale)
        
        else:
            # Generic data type
            name_token = self._consume(SQLTokenType.IDENTIFIER, "Expected data type name")
            return SQLDataType(name=name_token.value)
    
    def _parse_identifier(self) -> SQLIdentifier:
        """Parse identifier."""
        if self._check(SQLTokenType.IDENTIFIER):
            token = self._advance()
            return SQLIdentifier(name=token.value)
        elif self._check(SQLTokenType.QUOTED_IDENTIFIER):
            token = self._advance()
            return SQLIdentifier(name=token.value, quoted=True)
        else:
            self._error("Expected identifier")
            return None
    
    def _parse_column_definition(self) -> SQLColumnDefinition:
        """Parse column definition."""
        name = self._parse_identifier()
        data_type = self._parse_data_type()
        
        # Parse constraints
        constraints = []
        while self._check_column_constraint():
            constraints.append(self._parse_column_constraint())
        
        return SQLColumnDefinition(
            name=name,
            data_type=data_type,
            constraints=constraints
        )
    
    def _parse_column_constraint(self) -> SQLConstraint:
        """Parse column constraint."""
        if self._check(SQLTokenType.NOT):
            self._advance()
            self._consume(SQLTokenType.NULL, "Expected 'NULL'")
            return SQLConstraint(constraint_type=ConstraintType.NOT_NULL)
        
        elif self._check(SQLTokenType.PRIMARY):
            self._advance()
            self._consume(SQLTokenType.KEY, "Expected 'KEY'")
            return SQLPrimaryKeyConstraint()
        
        elif self._check(SQLTokenType.UNIQUE):
            self._advance()
            return SQLUniqueConstraint()
        
        elif self._check(SQLTokenType.CHECK):
            self._advance()
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            condition = self._parse_expression()
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            return SQLCheckConstraint(condition=condition)
        
        elif self._check(SQLTokenType.DEFAULT):
            self._advance()
            value = self._parse_expression()
            return SQLDefaultConstraint(value=value)
        
        else:
            self._error("Expected constraint")
            return None
    
    def _parse_constraint(self) -> SQLConstraint:
        """Parse table constraint."""
        constraint_name = None
        if self._check(SQLTokenType.CONSTRAINT):
            self._advance()
            constraint_name = self._parse_identifier()
        
        if self._check(SQLTokenType.PRIMARY):
            self._advance()
            self._consume(SQLTokenType.KEY, "Expected 'KEY'")
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            
            columns = []
            columns.append(self._parse_identifier())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                columns.append(self._parse_identifier())
            
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            
            return SQLPrimaryKeyConstraint(columns=columns, name=constraint_name)
        
        elif self._check(SQLTokenType.FOREIGN):
            self._advance()
            self._consume(SQLTokenType.KEY, "Expected 'KEY'")
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            
            columns = []
            columns.append(self._parse_identifier())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                columns.append(self._parse_identifier())
            
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            self._consume(SQLTokenType.REFERENCES, "Expected 'REFERENCES'")
            
            referenced_table = self._parse_identifier()
            
            referenced_columns = []
            if self._check(SQLTokenType.LPAREN):
                self._advance()
                referenced_columns.append(self._parse_identifier())
                while self._check(SQLTokenType.COMMA):
                    self._advance()
                    referenced_columns.append(self._parse_identifier())
                self._consume(SQLTokenType.RPAREN, "Expected ')'")
            
            return SQLForeignKeyConstraint(
                columns=columns,
                referenced_table=referenced_table,
                referenced_columns=referenced_columns,
                name=constraint_name
            )
        
        elif self._check(SQLTokenType.UNIQUE):
            self._advance()
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            
            columns = []
            columns.append(self._parse_identifier())
            while self._check(SQLTokenType.COMMA):
                self._advance()
                columns.append(self._parse_identifier())
            
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            
            return SQLUniqueConstraint(columns=columns, name=constraint_name)
        
        elif self._check(SQLTokenType.CHECK):
            self._advance()
            self._consume(SQLTokenType.LPAREN, "Expected '('")
            condition = self._parse_expression()
            self._consume(SQLTokenType.RPAREN, "Expected ')'")
            return SQLCheckConstraint(condition=condition, name=constraint_name)
        
        else:
            self._error("Expected constraint")
            return None
    
    # Helper methods
    def _check(self, *token_types: SQLTokenType) -> bool:
        """Check if current token matches any of the given types."""
        if self._is_at_end():
            return False
        return self._peek().type in token_types
    
    def _check_next(self, token_type: SQLTokenType) -> bool:
        """Check if next token matches the given type."""
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type
    
    def _check_join(self) -> bool:
        """Check if current token starts a JOIN clause."""
        return self._check(
            SQLTokenType.JOIN, SQLTokenType.INNER, SQLTokenType.LEFT,
            SQLTokenType.RIGHT, SQLTokenType.FULL, SQLTokenType.CROSS,
            SQLTokenType.NATURAL, SQLTokenType.LATERAL
        )
    
    def _check_column_constraint(self) -> bool:
        """Check if current token starts a column constraint."""
        return self._check(
            SQLTokenType.NOT, SQLTokenType.PRIMARY, SQLTokenType.UNIQUE,
            SQLTokenType.CHECK, SQLTokenType.DEFAULT
        )
    
    def _advance(self) -> SQLToken:
        """Consume and return current token."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we're at the end of tokens."""
        return self._peek().type == SQLTokenType.EOF
    
    def _peek(self) -> SQLToken:
        """Return current token without consuming it."""
        return self.tokens[self.current]
    
    def _previous(self) -> SQLToken:
        """Return previous token."""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: SQLTokenType, message: str) -> SQLToken:
        """Consume token of expected type or raise error."""
        if self._check(token_type):
            return self._advance()
        
        current_token = self._peek()
        raise SQLParseError(f"{message}. Got {current_token.type.name}({current_token.value})", current_token)
    
    def _error(self, message: str):
        """Report parse error."""
        token = self._peek()
        error_msg = f"Parse error at line {token.line}, column {token.column}: {message}"
        self.logger.error(error_msg)
        raise SQLParseError(error_msg, token)
    
    def _synchronize(self):
        """Synchronize parser after error."""
        self._advance()
        
        while not self._is_at_end():
            if self._previous().type == SQLTokenType.SEMICOLON:
                return
            
            if self._peek().type in [
                SQLTokenType.SELECT, SQLTokenType.INSERT, SQLTokenType.UPDATE,
                SQLTokenType.DELETE, SQLTokenType.CREATE, SQLTokenType.ALTER,
                SQLTokenType.DROP, SQLTokenType.WITH
            ]:
                return
            
            self._advance()