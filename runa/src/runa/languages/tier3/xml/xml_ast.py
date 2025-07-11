#!/usr/bin/env python3
"""
XML AST Node Definitions

Complete XML Abstract Syntax Tree node definitions for the Runa
universal translation system supporting XML 1.0/1.1 specification.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class XmlNodeType(Enum):
    """XML node types."""
    ELEMENT = "element"
    TEXT = "text"
    COMMENT = "comment"
    CDATA = "cdata"
    PROCESSING_INSTRUCTION = "processing_instruction"
    DOCTYPE = "doctype"
    ENTITY_REFERENCE = "entity_reference"


class XmlVisitor(ABC):
    """Visitor interface for XML AST nodes."""
    
    @abstractmethod
    def visit_xml_document(self, node: 'XmlDocument'): pass
    
    @abstractmethod
    def visit_xml_element(self, node: 'XmlElement'): pass
    
    @abstractmethod
    def visit_xml_text(self, node: 'XmlText'): pass
    
    @abstractmethod
    def visit_xml_comment(self, node: 'XmlComment'): pass
    
    @abstractmethod
    def visit_xml_cdata(self, node: 'XmlCData'): pass
    
    @abstractmethod
    def visit_xml_processing_instruction(self, node: 'XmlProcessingInstruction'): pass
    
    @abstractmethod
    def visit_xml_doctype(self, node: 'XmlDoctype'): pass
    
    @abstractmethod
    def visit_xml_attribute(self, node: 'XmlAttribute'): pass


class XmlNode(ABC):
    """Base class for all XML AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: XmlVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class XmlDocument(XmlNode):
    """XML document root."""
    version: str = "1.0"
    encoding: str = "UTF-8"
    standalone: Optional[bool] = None
    doctype: Optional['XmlDoctype'] = None
    root_element: Optional['XmlElement'] = None
    processing_instructions: List['XmlProcessingInstruction'] = field(default_factory=list)
    comments: List['XmlComment'] = field(default_factory=list)
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_document(self)


@dataclass
class XmlElement(XmlNode):
    """XML element."""
    tag_name: str
    attributes: Dict[str, 'XmlAttribute'] = field(default_factory=dict)
    children: List[XmlNode] = field(default_factory=list)
    namespace_uri: Optional[str] = None
    namespace_prefix: Optional[str] = None
    is_self_closing: bool = False
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_element(self)
    
    @property
    def qualified_name(self) -> str:
        """Get qualified name with namespace prefix."""
        if self.namespace_prefix:
            return f"{self.namespace_prefix}:{self.tag_name}"
        return self.tag_name
    
    def get_attribute(self, name: str) -> Optional['XmlAttribute']:
        """Get attribute by name."""
        return self.attributes.get(name)
    
    def set_attribute(self, name: str, value: str, namespace_uri: str = None):
        """Set attribute value."""
        self.attributes[name] = XmlAttribute(name=name, value=value, namespace_uri=namespace_uri)
    
    def remove_attribute(self, name: str) -> bool:
        """Remove attribute by name."""
        if name in self.attributes:
            del self.attributes[name]
            return True
        return False
    
    def add_child(self, child: XmlNode):
        """Add child node."""
        self.children.append(child)
    
    def remove_child(self, child: XmlNode) -> bool:
        """Remove child node."""
        if child in self.children:
            self.children.remove(child)
            return True
        return False
    
    def get_text_content(self) -> str:
        """Get all text content from this element and its children."""
        text_parts = []
        for child in self.children:
            if isinstance(child, XmlText):
                text_parts.append(child.content)
            elif isinstance(child, XmlElement):
                text_parts.append(child.get_text_content())
        return ''.join(text_parts)
    
    def find_children_by_tag(self, tag_name: str) -> List['XmlElement']:
        """Find direct children with specified tag name."""
        return [child for child in self.children if isinstance(child, XmlElement) and child.tag_name == tag_name]
    
    def find_descendants_by_tag(self, tag_name: str) -> List['XmlElement']:
        """Find all descendants with specified tag name."""
        descendants = []
        for child in self.children:
            if isinstance(child, XmlElement):
                if child.tag_name == tag_name:
                    descendants.append(child)
                descendants.extend(child.find_descendants_by_tag(tag_name))
        return descendants


@dataclass
class XmlAttribute(XmlNode):
    """XML attribute."""
    name: str
    value: str
    namespace_uri: Optional[str] = None
    namespace_prefix: Optional[str] = None
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_attribute(self)
    
    @property
    def qualified_name(self) -> str:
        """Get qualified name with namespace prefix."""
        if self.namespace_prefix:
            return f"{self.namespace_prefix}:{self.name}"
        return self.name


@dataclass
class XmlText(XmlNode):
    """XML text content."""
    content: str
    is_whitespace_only: bool = field(init=False)
    
    def __post_init__(self):
        self.is_whitespace_only = self.content.isspace() if self.content else True
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_text(self)


@dataclass
class XmlComment(XmlNode):
    """XML comment."""
    content: str
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_comment(self)


@dataclass
class XmlCData(XmlNode):
    """XML CDATA section."""
    content: str
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_cdata(self)


@dataclass
class XmlProcessingInstruction(XmlNode):
    """XML processing instruction."""
    target: str
    data: str = ""
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_processing_instruction(self)


@dataclass
class XmlDoctype(XmlNode):
    """XML DOCTYPE declaration."""
    name: str
    external_id: Optional[str] = None
    system_id: Optional[str] = None
    internal_subset: Optional[str] = None
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_doctype(self)


@dataclass
class XmlEntityReference(XmlNode):
    """XML entity reference."""
    name: str
    
    def accept(self, visitor: XmlVisitor) -> Any:
        return visitor.visit_xml_entity_reference(self)


@dataclass
class XmlNamespace:
    """XML namespace declaration."""
    prefix: Optional[str]
    uri: str


# Utility functions
def create_xml_document(root_element: XmlElement = None,
                       version: str = "1.0",
                       encoding: str = "UTF-8",
                       standalone: bool = None) -> XmlDocument:
    """Create an XML document."""
    return XmlDocument(
        version=version,
        encoding=encoding,
        standalone=standalone,
        root_element=root_element
    )


def create_xml_element(tag_name: str,
                      attributes: Dict[str, str] = None,
                      namespace_prefix: str = None,
                      namespace_uri: str = None) -> XmlElement:
    """Create an XML element."""
    element = XmlElement(
        tag_name=tag_name,
        namespace_prefix=namespace_prefix,
        namespace_uri=namespace_uri
    )
    
    if attributes:
        for name, value in attributes.items():
            element.set_attribute(name, value)
    
    return element


def create_xml_text(content: str) -> XmlText:
    """Create XML text content."""
    return XmlText(content=content)


def create_xml_comment(content: str) -> XmlComment:
    """Create XML comment."""
    return XmlComment(content=content)


def create_xml_cdata(content: str) -> XmlCData:
    """Create XML CDATA section."""
    return XmlCData(content=content)


def create_xml_processing_instruction(target: str, data: str = "") -> XmlProcessingInstruction:
    """Create XML processing instruction."""
    return XmlProcessingInstruction(target=target, data=data)


def create_xml_doctype(name: str,
                      external_id: str = None,
                      system_id: str = None,
                      internal_subset: str = None) -> XmlDoctype:
    """Create XML DOCTYPE declaration."""
    return XmlDoctype(
        name=name,
        external_id=external_id,
        system_id=system_id,
        internal_subset=internal_subset
    )


def xml_escape(text: str) -> str:
    """Escape XML special characters."""
    if not text:
        return ""
    
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    
    result = text
    for char, escape in replacements.items():
        result = result.replace(char, escape)
    
    return result


def xml_unescape(text: str) -> str:
    """Unescape XML special characters."""
    if not text:
        return ""
    
    replacements = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'"
    }
    
    result = text
    for escape, char in replacements.items():
        result = result.replace(escape, char)
    
    return result


def validate_xml_name(name: str) -> bool:
    """Validate XML name according to XML specification."""
    if not name:
        return False
    
    # Simplified validation - first character must be letter or underscore
    if not (name[0].isalpha() or name[0] == '_'):
        return False
    
    # Remaining characters must be letters, digits, hyphens, periods, or underscores
    for char in name[1:]:
        if not (char.isalnum() or char in '-._'):
            return False
    
    return True


def find_xml_element_by_path(root: XmlElement, path: str) -> Optional[XmlElement]:
    """Find element by XPath-like path (simplified)."""
    if not path:
        return root
    
    parts = path.strip('/').split('/')
    current = root
    
    for part in parts:
        if not part:
            continue
        
        # Simple tag name matching
        found = False
        for child in current.children:
            if isinstance(child, XmlElement) and child.tag_name == part:
                current = child
                found = True
                break
        
        if not found:
            return None
    
    return current


def xml_to_dict(element: XmlElement) -> Dict[str, Any]:
    """Convert XML element to dictionary representation."""
    result = {}
    
    # Add attributes
    if element.attributes:
        result['@attributes'] = {name: attr.value for name, attr in element.attributes.items()}
    
    # Process children
    children_dict = {}
    text_content = ""
    
    for child in element.children:
        if isinstance(child, XmlText):
            text_content += child.content
        elif isinstance(child, XmlElement):
            child_dict = xml_to_dict(child)
            tag_name = child.tag_name
            
            if tag_name in children_dict:
                # Multiple children with same tag - convert to list
                if not isinstance(children_dict[tag_name], list):
                    children_dict[tag_name] = [children_dict[tag_name]]
                children_dict[tag_name].append(child_dict)
            else:
                children_dict[tag_name] = child_dict
        elif isinstance(child, XmlComment):
            # Store comments in special key
            if '@comments' not in result:
                result['@comments'] = []
            result['@comments'].append(child.content)
    
    # Add text content if present
    text_content = text_content.strip()
    if text_content:
        if children_dict:
            result['@text'] = text_content
        else:
            # Element has only text content
            return text_content
    
    # Add children
    result.update(children_dict)
    
    return result if result else None


def dict_to_xml(data: Dict[str, Any], root_tag: str = "root") -> XmlElement:
    """Convert dictionary to XML element."""
    element = create_xml_element(root_tag)
    
    for key, value in data.items():
        if key == '@attributes':
            # Handle attributes
            if isinstance(value, dict):
                for attr_name, attr_value in value.items():
                    element.set_attribute(attr_name, str(attr_value))
        elif key == '@text':
            # Handle text content
            element.add_child(create_xml_text(str(value)))
        elif key == '@comments':
            # Handle comments
            if isinstance(value, list):
                for comment in value:
                    element.add_child(create_xml_comment(str(comment)))
        elif isinstance(value, dict):
            # Nested element
            child_element = dict_to_xml(value, key)
            element.add_child(child_element)
        elif isinstance(value, list):
            # Multiple elements with same tag
            for item in value:
                if isinstance(item, dict):
                    child_element = dict_to_xml(item, key)
                    element.add_child(child_element)
                else:
                    child_element = create_xml_element(key)
                    child_element.add_child(create_xml_text(str(item)))
                    element.add_child(child_element)
        else:
            # Simple element with text content
            child_element = create_xml_element(key)
            child_element.add_child(create_xml_text(str(value)))
            element.add_child(child_element)
    
    return element


def deep_copy_xml_element(element: XmlElement) -> XmlElement:
    """Deep copy an XML element."""
    new_element = XmlElement(
        tag_name=element.tag_name,
        namespace_uri=element.namespace_uri,
        namespace_prefix=element.namespace_prefix,
        is_self_closing=element.is_self_closing
    )
    
    # Copy attributes
    for name, attr in element.attributes.items():
        new_element.attributes[name] = XmlAttribute(
            name=attr.name,
            value=attr.value,
            namespace_uri=attr.namespace_uri,
            namespace_prefix=attr.namespace_prefix
        )
    
    # Copy children
    for child in element.children:
        if isinstance(child, XmlElement):
            new_element.add_child(deep_copy_xml_element(child))
        elif isinstance(child, XmlText):
            new_element.add_child(XmlText(content=child.content))
        elif isinstance(child, XmlComment):
            new_element.add_child(XmlComment(content=child.content))
        elif isinstance(child, XmlCData):
            new_element.add_child(XmlCData(content=child.content))
    
    return new_element


# Extended visitor for additional node types
class XmlVisitorExtended(XmlVisitor):
    """Extended visitor with additional node types."""
    
    def visit_xml_entity_reference(self, node: XmlEntityReference): pass