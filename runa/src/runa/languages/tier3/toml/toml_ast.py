#!/usr/bin/env python3
"""
TOML AST - Abstract Syntax Tree for TOML (Tom's Obvious Minimal Language)

Provides comprehensive AST node definitions for TOML including:
- Basic values: strings, integers, floats, booleans, dates/times
- Collections: arrays and tables (including inline tables)
- Table structure with dotted keys and table arrays
- Comments and documentation
- Different string types (basic, multi-line, literal)
- Date/time formats (RFC 3339)

Supports TOML v1.0.0 specification.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, date, time


class TOMLNode(ABC):
    """Base class for all TOML AST nodes"""
    
    def __init__(self, location: Optional[Dict[str, Any]] = None):
        self.location = location or {}
        self.parent: Optional['TOMLNode'] = None
        self.children: List['TOMLNode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        """Accept visitor pattern implementation"""
        pass
    
    def add_child(self, child: 'TOMLNode') -> None:
        """Add child node"""
        if child:
            child.parent = self
            self.children.append(child)


class TOMLExpression(TOMLNode):
    """Base class for all TOML expressions"""
    pass


class TOMLValue(TOMLExpression):
    """Base class for TOML values"""
    pass


class TOMLStatement(TOMLNode):
    """Base class for TOML statements"""
    pass


class TOMLType(Enum):
    """TOML value types"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    ARRAY = "array"
    TABLE = "table"
    INLINE_TABLE = "inline_table"


class TOMLStringType(Enum):
    """TOML string types"""
    BASIC = "basic"              # "string"
    MULTILINE_BASIC = "multiline_basic"  # """string"""
    LITERAL = "literal"          # 'string'
    MULTILINE_LITERAL = "multiline_literal"  # '''string'''


# Basic Values
@dataclass
class TOMLString(TOMLValue):
    """TOML string value"""
    value: str
    string_type: TOMLStringType = TOMLStringType.BASIC
    raw_value: Optional[str] = None  # Original unprocessed string
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_string(self)


@dataclass
class TOMLInteger(TOMLValue):
    """TOML integer value"""
    value: int
    raw_text: str  # Original text (may include underscores, hex, oct, bin)
    base: int = 10  # 10, 16, 8, or 2
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_integer(self)


@dataclass
class TOMLFloat(TOMLValue):
    """TOML float value"""
    value: float
    raw_text: str  # Original text (may include underscores, scientific notation)
    is_inf: bool = False
    is_nan: bool = False
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_float(self)


@dataclass
class TOMLBoolean(TOMLValue):
    """TOML boolean value"""
    value: bool
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_boolean(self)


@dataclass
class TOMLDateTime(TOMLValue):
    """TOML date-time value"""
    value: datetime
    raw_text: str
    has_timezone: bool = True
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_datetime(self)


@dataclass
class TOMLDate(TOMLValue):
    """TOML date value"""
    value: date
    raw_text: str
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_date(self)


@dataclass
class TOMLTime(TOMLValue):
    """TOML time value"""
    value: time
    raw_text: str
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_time(self)


# Collections
@dataclass
class TOMLArray(TOMLValue):
    """TOML array value"""
    elements: List[TOMLValue]
    is_multiline: bool = False
    trailing_comma: bool = False
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_array(self)


@dataclass
class TOMLInlineTable(TOMLValue):
    """TOML inline table value"""
    pairs: List[tuple[str, TOMLValue]]  # (key, value) pairs
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_inline_table(self)


# Key Path
@dataclass
class TOMLKey(TOMLNode):
    """TOML key (possibly dotted)"""
    parts: List[str]  # ['a', 'b', 'c'] for a.b.c
    is_quoted: List[bool]  # Whether each part is quoted
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_key(self)
    
    @property
    def dotted_key(self) -> str:
        """Get the dotted key representation"""
        return '.'.join(self.parts)


# Statements
@dataclass
class TOMLKeyValue(TOMLStatement):
    """TOML key-value assignment"""
    key: TOMLKey
    value: TOMLValue
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_key_value(self)


@dataclass
class TOMLTable(TOMLStatement):
    """TOML table header [table.name]"""
    key: TOMLKey
    is_array_table: bool = False  # True for [[table]], False for [table]
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_table(self)


@dataclass
class TOMLComment(TOMLNode):
    """TOML comment"""
    text: str
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_comment(self)


@dataclass
class TOMLDocument(TOMLNode):
    """Complete TOML document"""
    items: List[Union[TOMLKeyValue, TOMLTable, TOMLComment]]
    filename: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def accept(self, visitor: 'TOMLVisitor') -> Any:
        return visitor.visit_document(self)


# Visitor Pattern
class TOMLVisitor(ABC):
    """Abstract visitor for TOML AST nodes"""
    
    @abstractmethod
    def visit_document(self, node: TOMLDocument) -> Any:
        pass
    
    @abstractmethod
    def visit_key_value(self, node: TOMLKeyValue) -> Any:
        pass
    
    @abstractmethod
    def visit_table(self, node: TOMLTable) -> Any:
        pass
    
    @abstractmethod
    def visit_key(self, node: TOMLKey) -> Any:
        pass
    
    @abstractmethod
    def visit_string(self, node: TOMLString) -> Any:
        pass
    
    @abstractmethod
    def visit_integer(self, node: TOMLInteger) -> Any:
        pass
    
    @abstractmethod
    def visit_float(self, node: TOMLFloat) -> Any:
        pass
    
    @abstractmethod
    def visit_boolean(self, node: TOMLBoolean) -> Any:
        pass
    
    @abstractmethod
    def visit_datetime(self, node: TOMLDateTime) -> Any:
        pass
    
    @abstractmethod
    def visit_date(self, node: TOMLDate) -> Any:
        pass
    
    @abstractmethod
    def visit_time(self, node: TOMLTime) -> Any:
        pass
    
    @abstractmethod
    def visit_array(self, node: TOMLArray) -> Any:
        pass
    
    @abstractmethod
    def visit_inline_table(self, node: TOMLInlineTable) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: TOMLComment) -> Any:
        pass


class TOMLBaseVisitor(TOMLVisitor):
    """Base visitor with default implementations"""
    
    def visit_document(self, node: TOMLDocument) -> Any:
        for item in node.items:
            item.accept(self)
    
    def visit_key_value(self, node: TOMLKeyValue) -> Any:
        node.key.accept(self)
        node.value.accept(self)
    
    def visit_table(self, node: TOMLTable) -> Any:
        node.key.accept(self)
    
    def visit_key(self, node: TOMLKey) -> Any:
        pass
    
    def visit_string(self, node: TOMLString) -> Any:
        pass
    
    def visit_integer(self, node: TOMLInteger) -> Any:
        pass
    
    def visit_float(self, node: TOMLFloat) -> Any:
        pass
    
    def visit_boolean(self, node: TOMLBoolean) -> Any:
        pass
    
    def visit_datetime(self, node: TOMLDateTime) -> Any:
        pass
    
    def visit_date(self, node: TOMLDate) -> Any:
        pass
    
    def visit_time(self, node: TOMLTime) -> Any:
        pass
    
    def visit_array(self, node: TOMLArray) -> Any:
        for element in node.elements:
            element.accept(self)
    
    def visit_inline_table(self, node: TOMLInlineTable) -> Any:
        for key, value in node.pairs:
            value.accept(self)
    
    def visit_comment(self, node: TOMLComment) -> Any:
        pass


# Helper functions for creating AST nodes
def create_string(value: str, string_type: TOMLStringType = TOMLStringType.BASIC) -> TOMLString:
    """Create a TOML string node"""
    return TOMLString(value=value, string_type=string_type)


def create_integer(value: int, raw_text: Optional[str] = None, base: int = 10) -> TOMLInteger:
    """Create a TOML integer node"""
    if raw_text is None:
        raw_text = str(value)
    return TOMLInteger(value=value, raw_text=raw_text, base=base)


def create_float(value: float, raw_text: Optional[str] = None) -> TOMLFloat:
    """Create a TOML float node"""
    if raw_text is None:
        raw_text = str(value)
    return TOMLFloat(value=value, raw_text=raw_text)


def create_boolean(value: bool) -> TOMLBoolean:
    """Create a TOML boolean node"""
    return TOMLBoolean(value=value)


def create_array(elements: List[TOMLValue], is_multiline: bool = False) -> TOMLArray:
    """Create a TOML array node"""
    return TOMLArray(elements=elements, is_multiline=is_multiline)


def create_inline_table(pairs: List[tuple[str, TOMLValue]]) -> TOMLInlineTable:
    """Create a TOML inline table node"""
    return TOMLInlineTable(pairs=pairs)


def create_key(key_string: str, is_quoted: bool = False) -> TOMLKey:
    """Create a TOML key from a string (handles dotted keys)"""
    if '.' in key_string and not is_quoted:
        parts = key_string.split('.')
        is_quoted_list = [False] * len(parts)
    else:
        parts = [key_string]
        is_quoted_list = [is_quoted]
    
    return TOMLKey(parts=parts, is_quoted=is_quoted_list)


def create_key_value(key_string: str, value: TOMLValue) -> TOMLKeyValue:
    """Create a TOML key-value pair"""
    key = create_key(key_string)
    return TOMLKeyValue(key=key, value=value)


def create_table(table_name: str, is_array_table: bool = False) -> TOMLTable:
    """Create a TOML table header"""
    key = create_key(table_name)
    return TOMLTable(key=key, is_array_table=is_array_table)


def create_comment(text: str) -> TOMLComment:
    """Create a TOML comment"""
    return TOMLComment(text=text)


def create_document(items: List[Union[TOMLKeyValue, TOMLTable, TOMLComment]], 
                   filename: Optional[str] = None) -> TOMLDocument:
    """Create a TOML document"""
    return TOMLDocument(items=items, filename=filename)


# Constants for TOML specification compliance
TOML_VERSION = "1.0.0"
TOML_SPEC_URL = "https://toml.io/en/v1.0.0"

# Maximum values per TOML spec
MAX_INTEGER_VALUE = 2**63 - 1
MIN_INTEGER_VALUE = -(2**63)

# Reserved key names that should be handled carefully
RESERVED_KEYWORDS = set()  # TOML doesn't have reserved keywords like programming languages 