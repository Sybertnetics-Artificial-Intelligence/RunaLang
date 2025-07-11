#!/usr/bin/env python3
"""
YAML AST Node Definitions

Complete YAML Abstract Syntax Tree node definitions for the Runa
universal translation system supporting YAML 1.2 specification.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class YamlValueType(Enum):
    """YAML value types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    NULL = "null"
    MAPPING = "mapping"
    SEQUENCE = "sequence"
    BINARY = "binary"
    TIMESTAMP = "timestamp"


class YamlScalarStyle(Enum):
    """YAML scalar presentation styles."""
    PLAIN = "plain"
    SINGLE_QUOTED = "single_quoted"
    DOUBLE_QUOTED = "double_quoted"
    LITERAL = "literal"           # |
    FOLDED = "folded"            # >


class YamlMappingStyle(Enum):
    """YAML mapping presentation styles."""
    BLOCK = "block"
    FLOW = "flow"


class YamlSequenceStyle(Enum):
    """YAML sequence presentation styles."""
    BLOCK = "block"
    FLOW = "flow"


class YamlVisitor(ABC):
    """Visitor interface for YAML AST nodes."""
    
    @abstractmethod
    def visit_yaml_document(self, node: 'YamlDocument'): pass
    
    @abstractmethod
    def visit_yaml_mapping(self, node: 'YamlMapping'): pass
    
    @abstractmethod
    def visit_yaml_sequence(self, node: 'YamlSequence'): pass
    
    @abstractmethod
    def visit_yaml_scalar(self, node: 'YamlScalar'): pass
    
    @abstractmethod
    def visit_yaml_mapping_item(self, node: 'YamlMappingItem'): pass
    
    @abstractmethod
    def visit_yaml_alias(self, node: 'YamlAlias'): pass
    
    @abstractmethod
    def visit_yaml_anchor(self, node: 'YamlAnchor'): pass


class YamlNode(ABC):
    """Base class for all YAML AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: YamlVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class YamlValue(YamlNode):
    """Base class for YAML values."""
    pass


@dataclass
class YamlDocument(YamlNode):
    """YAML document."""
    content: YamlValue
    directives: List['YamlDirective'] = field(default_factory=list)
    explicit_start: bool = False
    explicit_end: bool = False
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_document(self)


@dataclass
class YamlDirective(YamlNode):
    """YAML directive (%YAML, %TAG)."""
    name: str
    parameters: List[str] = field(default_factory=list)
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_directive(self)


@dataclass
class YamlStream(YamlNode):
    """YAML stream containing multiple documents."""
    documents: List[YamlDocument] = field(default_factory=list)
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_stream(self)


@dataclass
class YamlMapping(YamlValue):
    """YAML mapping (key-value pairs)."""
    items: List['YamlMappingItem'] = field(default_factory=list)
    style: YamlMappingStyle = YamlMappingStyle.BLOCK
    tag: Optional[str] = None
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_mapping(self)
    
    def get_item(self, key: Any) -> Optional['YamlMappingItem']:
        """Get mapping item by key."""
        for item in self.items:
            if self._keys_equal(item.key, key):
                return item
        return None
    
    def add_item(self, key: YamlValue, value: YamlValue) -> 'YamlMappingItem':
        """Add a new mapping item."""
        item = YamlMappingItem(key=key, value=value)
        self.items.append(item)
        return item
    
    def remove_item(self, key: Any) -> bool:
        """Remove mapping item by key."""
        for i, item in enumerate(self.items):
            if self._keys_equal(item.key, key):
                del self.items[i]
                return True
        return False
    
    def _keys_equal(self, node_key: YamlValue, search_key: Any) -> bool:
        """Check if keys are equal."""
        if isinstance(node_key, YamlScalar):
            return node_key.value == search_key
        return str(node_key) == str(search_key)


@dataclass
class YamlSequence(YamlValue):
    """YAML sequence (array)."""
    items: List[YamlValue] = field(default_factory=list)
    style: YamlSequenceStyle = YamlSequenceStyle.BLOCK
    tag: Optional[str] = None
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_sequence(self)
    
    def add_item(self, value: YamlValue):
        """Add item to sequence."""
        self.items.append(value)
    
    def remove_item(self, index: int) -> bool:
        """Remove item by index."""
        if 0 <= index < len(self.items):
            del self.items[index]
            return True
        return False
    
    def get_item(self, index: int) -> Optional[YamlValue]:
        """Get item by index."""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None


@dataclass
class YamlMappingItem(YamlNode):
    """YAML mapping item (key-value pair)."""
    key: YamlValue
    value: YamlValue
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_mapping_item(self)


@dataclass
class YamlScalar(YamlValue):
    """YAML scalar value."""
    value: Any
    style: YamlScalarStyle = YamlScalarStyle.PLAIN
    tag: Optional[str] = None
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_scalar(self)
    
    @property
    def yaml_type(self) -> YamlValueType:
        """Get YAML type of scalar."""
        if self.value is None:
            return YamlValueType.NULL
        elif isinstance(self.value, bool):
            return YamlValueType.BOOLEAN
        elif isinstance(self.value, int):
            return YamlValueType.INTEGER
        elif isinstance(self.value, float):
            return YamlValueType.FLOAT
        elif isinstance(self.value, str):
            return YamlValueType.STRING
        elif isinstance(self.value, bytes):
            return YamlValueType.BINARY
        else:
            return YamlValueType.STRING


@dataclass
class YamlAlias(YamlValue):
    """YAML alias reference (*alias)."""
    name: str
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_alias(self)


@dataclass
class YamlAnchor(YamlNode):
    """YAML anchor definition (&anchor)."""
    name: str
    value: YamlValue
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_anchor(self)


@dataclass
class YamlComment(YamlNode):
    """YAML comment."""
    text: str
    inline: bool = False
    
    def accept(self, visitor: YamlVisitor) -> Any:
        return visitor.visit_yaml_comment(self)


# Utility functions
def create_yaml_document(content: YamlValue, 
                        explicit_start: bool = False,
                        explicit_end: bool = False) -> YamlDocument:
    """Create a YAML document."""
    return YamlDocument(
        content=content,
        explicit_start=explicit_start,
        explicit_end=explicit_end
    )


def create_yaml_mapping(items: List[YamlMappingItem] = None,
                       style: YamlMappingStyle = YamlMappingStyle.BLOCK) -> YamlMapping:
    """Create a YAML mapping."""
    return YamlMapping(items=items or [], style=style)


def create_yaml_sequence(items: List[YamlValue] = None,
                        style: YamlSequenceStyle = YamlSequenceStyle.BLOCK) -> YamlSequence:
    """Create a YAML sequence."""
    return YamlSequence(items=items or [], style=style)


def create_yaml_mapping_item(key: YamlValue, value: YamlValue) -> YamlMappingItem:
    """Create a YAML mapping item."""
    return YamlMappingItem(key=key, value=value)


def create_yaml_scalar(value: Any, 
                      style: YamlScalarStyle = YamlScalarStyle.PLAIN,
                      tag: str = None) -> YamlScalar:
    """Create a YAML scalar."""
    return YamlScalar(value=value, style=style, tag=tag)


def create_yaml_string(value: str, 
                      style: YamlScalarStyle = YamlScalarStyle.PLAIN) -> YamlScalar:
    """Create a YAML string scalar."""
    return YamlScalar(value=value, style=style)


def create_yaml_integer(value: int) -> YamlScalar:
    """Create a YAML integer scalar."""
    return YamlScalar(value=value)


def create_yaml_float(value: float) -> YamlScalar:
    """Create a YAML float scalar."""
    return YamlScalar(value=value)


def create_yaml_boolean(value: bool) -> YamlScalar:
    """Create a YAML boolean scalar."""
    return YamlScalar(value=value)


def create_yaml_null() -> YamlScalar:
    """Create a YAML null scalar."""
    return YamlScalar(value=None)


def create_yaml_alias(name: str) -> YamlAlias:
    """Create a YAML alias."""
    return YamlAlias(name=name)


def create_yaml_anchor(name: str, value: YamlValue) -> YamlAnchor:
    """Create a YAML anchor."""
    return YamlAnchor(name=name, value=value)


def yaml_value_from_python(value: Any) -> YamlValue:
    """Convert Python value to YAML AST node."""
    if value is None:
        return YamlScalar(value=None)
    elif isinstance(value, bool):
        return YamlScalar(value=value)
    elif isinstance(value, (int, float)):
        return YamlScalar(value=value)
    elif isinstance(value, str):
        return YamlScalar(value=value)
    elif isinstance(value, bytes):
        return YamlScalar(value=value)
    elif isinstance(value, dict):
        items = []
        for k, v in value.items():
            key_node = yaml_value_from_python(k)
            value_node = yaml_value_from_python(v)
            items.append(YamlMappingItem(key=key_node, value=value_node))
        return YamlMapping(items=items)
    elif isinstance(value, (list, tuple)):
        items = [yaml_value_from_python(item) for item in value]
        return YamlSequence(items=items)
    else:
        # Convert unknown types to string
        return YamlScalar(value=str(value))


def yaml_value_to_python(node: YamlValue) -> Any:
    """Convert YAML AST node to Python value."""
    if isinstance(node, YamlScalar):
        return node.value
    elif isinstance(node, YamlMapping):
        result = {}
        for item in node.items:
            key = yaml_value_to_python(item.key)
            value = yaml_value_to_python(item.value)
            result[key] = value
        return result
    elif isinstance(node, YamlSequence):
        return [yaml_value_to_python(item) for item in node.items]
    elif isinstance(node, YamlAlias):
        # Aliases need to be resolved in context
        return f"*{node.name}"
    else:
        return None


def infer_yaml_type(value: Any) -> YamlValueType:
    """Infer YAML type from Python value."""
    if value is None:
        return YamlValueType.NULL
    elif isinstance(value, bool):
        return YamlValueType.BOOLEAN
    elif isinstance(value, int):
        return YamlValueType.INTEGER
    elif isinstance(value, float):
        return YamlValueType.FLOAT
    elif isinstance(value, str):
        return YamlValueType.STRING
    elif isinstance(value, bytes):
        return YamlValueType.BINARY
    elif isinstance(value, dict):
        return YamlValueType.MAPPING
    elif isinstance(value, (list, tuple)):
        return YamlValueType.SEQUENCE
    else:
        return YamlValueType.STRING


def validate_yaml_structure(node: YamlValue) -> bool:
    """Validate YAML structure."""
    try:
        if isinstance(node, YamlScalar):
            return True
        elif isinstance(node, YamlMapping):
            # Validate all items
            for item in node.items:
                if not validate_yaml_structure(item.key):
                    return False
                if not validate_yaml_structure(item.value):
                    return False
            return True
        elif isinstance(node, YamlSequence):
            # Validate all items
            return all(validate_yaml_structure(item) for item in node.items)
        elif isinstance(node, (YamlAlias, YamlAnchor)):
            return True
        else:
            return False
    except:
        return False


def find_yaml_path(root: YamlValue, path: str) -> Optional[YamlValue]:
    """Find value at YAML path (dot notation)."""
    if not path:
        return root
    
    parts = path.split('.')
    current = root
    
    for part in parts:
        if isinstance(current, YamlMapping):
            item = current.get_item(part)
            if item:
                current = item.value
            else:
                return None
        elif isinstance(current, YamlSequence):
            try:
                index = int(part)
                current = current.get_item(index)
                if current is None:
                    return None
            except ValueError:
                return None
        else:
            return None
    
    return current


def deep_copy_yaml_value(node: YamlValue) -> YamlValue:
    """Deep copy a YAML value."""
    if isinstance(node, YamlScalar):
        return YamlScalar(value=node.value, style=node.style, tag=node.tag)
    elif isinstance(node, YamlMapping):
        items = []
        for item in node.items:
            items.append(YamlMappingItem(
                key=deep_copy_yaml_value(item.key),
                value=deep_copy_yaml_value(item.value)
            ))
        return YamlMapping(items=items, style=node.style, tag=node.tag)
    elif isinstance(node, YamlSequence):
        items = [deep_copy_yaml_value(item) for item in node.items]
        return YamlSequence(items=items, style=node.style, tag=node.tag)
    elif isinstance(node, YamlAlias):
        return YamlAlias(name=node.name)
    else:
        return YamlScalar(value=None)


def merge_yaml_mappings(mapping1: YamlMapping, mapping2: YamlMapping) -> YamlMapping:
    """Merge two YAML mappings."""
    result = deep_copy_yaml_value(mapping1)
    
    for item in mapping2.items:
        existing_item = result.get_item(yaml_value_to_python(item.key))
        if existing_item:
            # If both are mappings, merge recursively
            if (isinstance(existing_item.value, YamlMapping) and 
                isinstance(item.value, YamlMapping)):
                existing_item.value = merge_yaml_mappings(existing_item.value, item.value)
            else:
                # Otherwise, replace
                existing_item.value = deep_copy_yaml_value(item.value)
        else:
            # Add new item
            result.add_item(
                deep_copy_yaml_value(item.key),
                deep_copy_yaml_value(item.value)
            )
    
    return result


# Extended visitor for additional node types
class YamlVisitorExtended(YamlVisitor):
    """Extended visitor with additional node types."""
    
    def visit_yaml_directive(self, node: YamlDirective): pass
    def visit_yaml_stream(self, node: YamlStream): pass
    def visit_yaml_comment(self, node: YamlComment): pass