#!/usr/bin/env python3
"""
JSON AST Node Definitions

Complete JSON Abstract Syntax Tree node definitions for the Runa
universal translation system supporting JSON schema and extensions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class JsonValueType(Enum):
    """JSON value types."""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    NULL = "null"
    OBJECT = "object"
    ARRAY = "array"


class JsonVisitor(ABC):
    """Visitor interface for JSON AST nodes."""
    
    @abstractmethod
    def visit_json_document(self, node: 'JsonDocument'): pass
    
    @abstractmethod
    def visit_json_object(self, node: 'JsonObject'): pass
    
    @abstractmethod
    def visit_json_array(self, node: 'JsonArray'): pass
    
    @abstractmethod
    def visit_json_property(self, node: 'JsonProperty'): pass
    
    @abstractmethod
    def visit_json_string(self, node: 'JsonString'): pass
    
    @abstractmethod
    def visit_json_number(self, node: 'JsonNumber'): pass
    
    @abstractmethod
    def visit_json_boolean(self, node: 'JsonBoolean'): pass
    
    @abstractmethod
    def visit_json_null(self, node: 'JsonNull'): pass


class JsonNode(ABC):
    """Base class for all JSON AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: JsonVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class JsonValue(JsonNode):
    """Base class for JSON values."""
    pass


@dataclass
class JsonDocument(JsonNode):
    """JSON document root."""
    root: JsonValue
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_document(self)


@dataclass
class JsonObject(JsonValue):
    """JSON object."""
    properties: List['JsonProperty'] = field(default_factory=list)
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_object(self)
    
    def get_property(self, key: str) -> Optional['JsonProperty']:
        """Get property by key."""
        for prop in self.properties:
            if prop.key.value == key:
                return prop
        return None
    
    def add_property(self, key: str, value: JsonValue) -> 'JsonProperty':
        """Add a new property."""
        prop = JsonProperty(key=JsonString(value=key), value=value)
        self.properties.append(prop)
        return prop
    
    def remove_property(self, key: str) -> bool:
        """Remove property by key."""
        for i, prop in enumerate(self.properties):
            if prop.key.value == key:
                del self.properties[i]
                return True
        return False


@dataclass
class JsonArray(JsonValue):
    """JSON array."""
    elements: List[JsonValue] = field(default_factory=list)
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_array(self)
    
    def add_element(self, value: JsonValue):
        """Add element to array."""
        self.elements.append(value)
    
    def remove_element(self, index: int) -> bool:
        """Remove element by index."""
        if 0 <= index < len(self.elements):
            del self.elements[index]
            return True
        return False
    
    def get_element(self, index: int) -> Optional[JsonValue]:
        """Get element by index."""
        if 0 <= index < len(self.elements):
            return self.elements[index]
        return None


@dataclass
class JsonProperty(JsonNode):
    """JSON object property."""
    key: 'JsonString'
    value: JsonValue
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_property(self)


@dataclass
class JsonString(JsonValue):
    """JSON string value."""
    value: str
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_string(self)


@dataclass
class JsonNumber(JsonValue):
    """JSON number value."""
    value: Union[int, float]
    is_integer: bool = field(init=False)
    
    def __post_init__(self):
        self.is_integer = isinstance(self.value, int)
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_number(self)


@dataclass
class JsonBoolean(JsonValue):
    """JSON boolean value."""
    value: bool
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_boolean(self)


@dataclass
class JsonNull(JsonValue):
    """JSON null value."""
    
    def accept(self, visitor: JsonVisitor) -> Any:
        return visitor.visit_json_null(self)


# JSON Schema support
@dataclass
class JsonSchema(JsonNode):
    """JSON Schema definition."""
    schema_type: str
    properties: Dict[str, 'JsonSchemaProperty'] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    additional_properties: bool = True
    title: Optional[str] = None
    description: Optional[str] = None
    
    def accept(self, visitor: JsonVisitor) -> Any:
        # Extended visitor would handle this
        return None


@dataclass
class JsonSchemaProperty(JsonNode):
    """JSON Schema property definition."""
    property_type: str
    format: Optional[str] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    enum: Optional[List[Any]] = None
    default: Optional[Any] = None
    description: Optional[str] = None
    
    def accept(self, visitor: JsonVisitor) -> Any:
        # Extended visitor would handle this
        return None


# Utility functions
def create_json_document(root: JsonValue) -> JsonDocument:
    """Create a JSON document."""
    return JsonDocument(root=root)


def create_json_object(properties: List[JsonProperty] = None) -> JsonObject:
    """Create a JSON object."""
    return JsonObject(properties=properties or [])


def create_json_array(elements: List[JsonValue] = None) -> JsonArray:
    """Create a JSON array."""
    return JsonArray(elements=elements or [])


def create_json_property(key: str, value: JsonValue) -> JsonProperty:
    """Create a JSON property."""
    return JsonProperty(key=JsonString(value=key), value=value)


def create_json_string(value: str) -> JsonString:
    """Create a JSON string."""
    return JsonString(value=value)


def create_json_number(value: Union[int, float]) -> JsonNumber:
    """Create a JSON number."""
    return JsonNumber(value=value)


def create_json_boolean(value: bool) -> JsonBoolean:
    """Create a JSON boolean."""
    return JsonBoolean(value=value)


def create_json_null() -> JsonNull:
    """Create a JSON null."""
    return JsonNull()


def json_value_from_python(value: Any) -> JsonValue:
    """Convert Python value to JSON AST node."""
    if value is None:
        return JsonNull()
    elif isinstance(value, bool):
        return JsonBoolean(value=value)
    elif isinstance(value, str):
        return JsonString(value=value)
    elif isinstance(value, (int, float)):
        return JsonNumber(value=value)
    elif isinstance(value, dict):
        properties = []
        for k, v in value.items():
            properties.append(JsonProperty(
                key=JsonString(value=str(k)),
                value=json_value_from_python(v)
            ))
        return JsonObject(properties=properties)
    elif isinstance(value, (list, tuple)):
        elements = [json_value_from_python(item) for item in value]
        return JsonArray(elements=elements)
    else:
        # Convert to string for unknown types
        return JsonString(value=str(value))


def json_value_to_python(node: JsonValue) -> Any:
    """Convert JSON AST node to Python value."""
    if isinstance(node, JsonNull):
        return None
    elif isinstance(node, JsonBoolean):
        return node.value
    elif isinstance(node, JsonString):
        return node.value
    elif isinstance(node, JsonNumber):
        return node.value
    elif isinstance(node, JsonObject):
        result = {}
        for prop in node.properties:
            result[prop.key.value] = json_value_to_python(prop.value)
        return result
    elif isinstance(node, JsonArray):
        return [json_value_to_python(element) for element in node.elements]
    else:
        return None


def get_json_type(node: JsonValue) -> JsonValueType:
    """Get JSON type of a value node."""
    if isinstance(node, JsonNull):
        return JsonValueType.NULL
    elif isinstance(node, JsonBoolean):
        return JsonValueType.BOOLEAN
    elif isinstance(node, JsonString):
        return JsonValueType.STRING
    elif isinstance(node, JsonNumber):
        return JsonValueType.NUMBER
    elif isinstance(node, JsonObject):
        return JsonValueType.OBJECT
    elif isinstance(node, JsonArray):
        return JsonValueType.ARRAY
    else:
        return JsonValueType.NULL


def validate_json_structure(node: JsonValue) -> bool:
    """Validate JSON structure."""
    try:
        if isinstance(node, (JsonString, JsonNumber, JsonBoolean, JsonNull)):
            return True
        elif isinstance(node, JsonObject):
            # Validate all properties
            for prop in node.properties:
                if not isinstance(prop.key, JsonString):
                    return False
                if not validate_json_structure(prop.value):
                    return False
            return True
        elif isinstance(node, JsonArray):
            # Validate all elements
            return all(validate_json_structure(elem) for elem in node.elements)
        else:
            return False
    except:
        return False


def find_json_path(root: JsonValue, path: str) -> Optional[JsonValue]:
    """Find value at JSON path (simplified JSONPath)."""
    if not path:
        return root
    
    parts = path.split('.')
    current = root
    
    for part in parts:
        if isinstance(current, JsonObject):
            prop = current.get_property(part)
            if prop:
                current = prop.value
            else:
                return None
        elif isinstance(current, JsonArray):
            try:
                index = int(part)
                current = current.get_element(index)
                if current is None:
                    return None
            except ValueError:
                return None
        else:
            return None
    
    return current


def deep_copy_json_value(node: JsonValue) -> JsonValue:
    """Deep copy a JSON value."""
    if isinstance(node, JsonNull):
        return JsonNull()
    elif isinstance(node, JsonBoolean):
        return JsonBoolean(value=node.value)
    elif isinstance(node, JsonString):
        return JsonString(value=node.value)
    elif isinstance(node, JsonNumber):
        return JsonNumber(value=node.value)
    elif isinstance(node, JsonObject):
        properties = []
        for prop in node.properties:
            properties.append(JsonProperty(
                key=JsonString(value=prop.key.value),
                value=deep_copy_json_value(prop.value)
            ))
        return JsonObject(properties=properties)
    elif isinstance(node, JsonArray):
        elements = [deep_copy_json_value(elem) for elem in node.elements]
        return JsonArray(elements=elements)
    else:
        return JsonNull()


def merge_json_objects(obj1: JsonObject, obj2: JsonObject) -> JsonObject:
    """Merge two JSON objects."""
    result = deep_copy_json_value(obj1)
    
    for prop in obj2.properties:
        existing_prop = result.get_property(prop.key.value)
        if existing_prop:
            # If both are objects, merge recursively
            if (isinstance(existing_prop.value, JsonObject) and 
                isinstance(prop.value, JsonObject)):
                existing_prop.value = merge_json_objects(existing_prop.value, prop.value)
            else:
                # Otherwise, replace
                existing_prop.value = deep_copy_json_value(prop.value)
        else:
            # Add new property
            result.add_property(prop.key.value, deep_copy_json_value(prop.value))
    
    return result