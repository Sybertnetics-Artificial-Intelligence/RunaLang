#!/usr/bin/env python3
"""
HTML AST Node Definitions

Complete HTML Abstract Syntax Tree node definitions for the Runa
universal translation system supporting HTML5 specification.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class HtmlNodeType(Enum):
    """HTML node types."""
    DOCUMENT = "document"
    ELEMENT = "element"
    TEXT = "text"
    COMMENT = "comment"
    DOCTYPE = "doctype"
    CDATA = "cdata"  # For XML-style CDATA sections


class HtmlVisitor(ABC):
    """Visitor interface for HTML AST nodes."""
    
    @abstractmethod
    def visit_html_document(self, node: 'HtmlDocument'): pass
    
    @abstractmethod
    def visit_html_element(self, node: 'HtmlElement'): pass
    
    @abstractmethod
    def visit_html_text(self, node: 'HtmlText'): pass
    
    @abstractmethod
    def visit_html_comment(self, node: 'HtmlComment'): pass
    
    @abstractmethod
    def visit_html_doctype(self, node: 'HtmlDoctype'): pass
    
    @abstractmethod
    def visit_html_attribute(self, node: 'HtmlAttribute'): pass


class HtmlNode(ABC):
    """Base class for all HTML AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: HtmlVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class HtmlDocument(HtmlNode):
    """HTML document root."""
    doctype: Optional['HtmlDoctype'] = None
    root_element: Optional['HtmlElement'] = None
    comments: List['HtmlComment'] = field(default_factory=list)
    language: str = "en"
    encoding: str = "UTF-8"
    
    def accept(self, visitor: HtmlVisitor) -> Any:
        return visitor.visit_html_document(self)


@dataclass
class HtmlElement(HtmlNode):
    """HTML element."""
    tag_name: str
    attributes: Dict[str, 'HtmlAttribute'] = field(default_factory=dict)
    children: List[HtmlNode] = field(default_factory=list)
    is_self_closing: bool = False
    is_void_element: bool = False  # HTML5 void elements like <br>, <img>
    
    def accept(self, visitor: HtmlVisitor) -> Any:
        return visitor.visit_html_element(self)
    
    @property
    def is_empty(self) -> bool:
        """Check if element has no content."""
        return not self.children or all(
            isinstance(child, HtmlText) and not child.content.strip()
            for child in self.children
        )
    
    def get_attribute(self, name: str) -> Optional['HtmlAttribute']:
        """Get attribute by name."""
        return self.attributes.get(name.lower())
    
    def set_attribute(self, name: str, value: str = ""):
        """Set attribute value."""
        self.attributes[name.lower()] = HtmlAttribute(name=name.lower(), value=value)
    
    def remove_attribute(self, name: str) -> bool:
        """Remove attribute by name."""
        name_lower = name.lower()
        if name_lower in self.attributes:
            del self.attributes[name_lower]
            return True
        return False
    
    def has_attribute(self, name: str) -> bool:
        """Check if element has attribute."""
        return name.lower() in self.attributes
    
    def add_child(self, child: HtmlNode):
        """Add child node."""
        self.children.append(child)
    
    def remove_child(self, child: HtmlNode) -> bool:
        """Remove child node."""
        if child in self.children:
            self.children.remove(child)
            return True
        return False
    
    def get_text_content(self) -> str:
        """Get all text content from this element and its children."""
        text_parts = []
        for child in self.children:
            if isinstance(child, HtmlText):
                text_parts.append(child.content)
            elif isinstance(child, HtmlElement):
                text_parts.append(child.get_text_content())
        return ''.join(text_parts)
    
    def find_children_by_tag(self, tag_name: str) -> List['HtmlElement']:
        """Find direct children with specified tag name."""
        return [
            child for child in self.children 
            if isinstance(child, HtmlElement) and child.tag_name.lower() == tag_name.lower()
        ]
    
    def find_descendants_by_tag(self, tag_name: str) -> List['HtmlElement']:
        """Find all descendants with specified tag name."""
        descendants = []
        for child in self.children:
            if isinstance(child, HtmlElement):
                if child.tag_name.lower() == tag_name.lower():
                    descendants.append(child)
                descendants.extend(child.find_descendants_by_tag(tag_name))
        return descendants
    
    def find_by_id(self, element_id: str) -> Optional['HtmlElement']:
        """Find element by ID."""
        id_attr = self.get_attribute("id")
        if id_attr and id_attr.value == element_id:
            return self
        
        for child in self.children:
            if isinstance(child, HtmlElement):
                result = child.find_by_id(element_id)
                if result:
                    return result
        
        return None
    
    def find_by_class(self, class_name: str) -> List['HtmlElement']:
        """Find elements by class name."""
        results = []
        class_attr = self.get_attribute("class")
        
        if class_attr and class_name in class_attr.value.split():
            results.append(self)
        
        for child in self.children:
            if isinstance(child, HtmlElement):
                results.extend(child.find_by_class(class_name))
        
        return results


@dataclass
class HtmlAttribute(HtmlNode):
    """HTML attribute."""
    name: str
    value: str = ""
    is_boolean: bool = False  # For attributes like 'disabled', 'checked'
    
    def accept(self, visitor: HtmlVisitor) -> Any:
        return visitor.visit_html_attribute(self)
    
    @property
    def normalized_name(self) -> str:
        """Get normalized attribute name (lowercase)."""
        return self.name.lower()


@dataclass
class HtmlText(HtmlNode):
    """HTML text content."""
    content: str
    is_whitespace_only: bool = field(init=False)
    preserve_whitespace: bool = False
    
    def __post_init__(self):
        self.is_whitespace_only = self.content.isspace() if self.content else True
    
    def accept(self, visitor: HtmlVisitor) -> Any:
        return visitor.visit_html_text(self)


@dataclass
class HtmlComment(HtmlNode):
    """HTML comment."""
    content: str
    
    def accept(self, visitor: HtmlVisitor) -> Any:
        return visitor.visit_html_comment(self)


@dataclass
class HtmlDoctype(HtmlNode):
    """HTML DOCTYPE declaration."""
    doctype_string: str = "html"  # For HTML5: "html"
    
    def accept(self, visitor: HtmlVisitor) -> Any:
        return visitor.visit_html_doctype(self)
    
    @property
    def is_html5(self) -> bool:
        """Check if this is HTML5 doctype."""
        return self.doctype_string.lower() == "html"


# HTML5 void elements that cannot have content
HTML5_VOID_ELEMENTS: Set[str] = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
}

# HTML5 block-level elements
HTML5_BLOCK_ELEMENTS: Set[str] = {
    'address', 'article', 'aside', 'blockquote', 'details', 'dialog', 'dd', 'div',
    'dl', 'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav', 'ol',
    'p', 'pre', 'section', 'table', 'ul'
}

# HTML5 inline elements
HTML5_INLINE_ELEMENTS: Set[str] = {
    'a', 'abbr', 'acronym', 'b', 'bdi', 'bdo', 'big', 'br', 'button', 'cite',
    'code', 'dfn', 'em', 'i', 'img', 'input', 'kbd', 'label', 'map', 'mark',
    'meter', 'noscript', 'object', 'output', 'progress', 'q', 'ruby', 's', 'samp',
    'script', 'select', 'small', 'span', 'strong', 'sub', 'sup', 'textarea',
    'time', 'tt', 'u', 'var', 'wbr'
}


# Utility functions
def create_html_document(root_element: HtmlElement = None,
                        doctype: str = "html",
                        language: str = "en",
                        encoding: str = "UTF-8") -> HtmlDocument:
    """Create an HTML document."""
    return HtmlDocument(
        doctype=HtmlDoctype(doctype),
        root_element=root_element,
        language=language,
        encoding=encoding
    )


def create_html_element(tag_name: str,
                       attributes: Dict[str, str] = None,
                       content: str = None,
                       children: List[HtmlNode] = None) -> HtmlElement:
    """Create an HTML element."""
    tag_lower = tag_name.lower()
    element = HtmlElement(
        tag_name=tag_lower,
        is_void_element=tag_lower in HTML5_VOID_ELEMENTS
    )
    
    if attributes:
        for name, value in attributes.items():
            element.set_attribute(name, value)
    
    if content:
        element.add_child(HtmlText(content=content))
    
    if children:
        for child in children:
            element.add_child(child)
    
    return element


def create_html_text(content: str, preserve_whitespace: bool = False) -> HtmlText:
    """Create HTML text content."""
    return HtmlText(content=content, preserve_whitespace=preserve_whitespace)


def create_html_comment(content: str) -> HtmlComment:
    """Create HTML comment."""
    return HtmlComment(content=content)


def create_html_doctype(doctype_string: str = "html") -> HtmlDoctype:
    """Create HTML DOCTYPE declaration."""
    return HtmlDoctype(doctype_string=doctype_string)


def html_escape(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;'
    }
    
    result = text
    for char, escape in replacements.items():
        result = result.replace(char, escape)
    
    return result


def html_unescape(text: str) -> str:
    """Unescape HTML special characters."""
    if not text:
        return ""
    
    replacements = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#x27;': "'",
        '&#39;': "'",
        '&apos;': "'"
    }
    
    result = text
    for escape, char in replacements.items():
        result = result.replace(escape, char)
    
    return result


def is_valid_html_tag_name(name: str) -> bool:
    """Validate HTML tag name."""
    if not name:
        return False
    
    # HTML tag names must start with a letter
    if not name[0].isalpha():
        return False
    
    # Remaining characters must be letters, digits, or hyphens
    for char in name[1:]:
        if not (char.isalnum() or char == '-'):
            return False
    
    return True


def is_valid_html_attribute_name(name: str) -> bool:
    """Validate HTML attribute name."""
    if not name:
        return False
    
    # HTML attribute names are case-insensitive and can contain various characters
    invalid_chars = set(' \t\n\r\f"\'>/=')
    return not any(char in invalid_chars for char in name)


def find_html_element_by_path(root: HtmlElement, path: str) -> Optional[HtmlElement]:
    """Find element by CSS-like path (simplified)."""
    if not path:
        return root
    
    parts = path.strip().split(' ')
    current = root
    
    for part in parts:
        if not part:
            continue
        
        # Simple tag name matching
        found = False
        for child in current.children:
            if isinstance(child, HtmlElement) and child.tag_name.lower() == part.lower():
                current = child
                found = True
                break
        
        if not found:
            return None
    
    return current


def html_to_dict(element: HtmlElement) -> Dict[str, Any]:
    """Convert HTML element to dictionary representation."""
    result = {
        'tag': element.tag_name
    }
    
    # Add attributes
    if element.attributes:
        result['attributes'] = {name: attr.value for name, attr in element.attributes.items()}
    
    # Process children
    children_data = []
    text_content = ""
    
    for child in element.children:
        if isinstance(child, HtmlText):
            text_content += child.content
        elif isinstance(child, HtmlElement):
            children_data.append(html_to_dict(child))
        elif isinstance(child, HtmlComment):
            children_data.append({'type': 'comment', 'content': child.content})
    
    # Add text content if present
    text_content = text_content.strip()
    if text_content:
        if children_data:
            result['text'] = text_content
        else:
            # Element has only text content
            result['content'] = text_content
    
    # Add children
    if children_data:
        result['children'] = children_data
    
    return result


def dict_to_html(data: Dict[str, Any]) -> HtmlElement:
    """Convert dictionary to HTML element."""
    tag_name = data.get('tag', 'div')
    element = create_html_element(tag_name)
    
    # Handle attributes
    if 'attributes' in data:
        for attr_name, attr_value in data['attributes'].items():
            element.set_attribute(attr_name, str(attr_value))
    
    # Handle text content
    if 'content' in data:
        element.add_child(create_html_text(str(data['content'])))
    elif 'text' in data:
        element.add_child(create_html_text(str(data['text'])))
    
    # Handle children
    if 'children' in data:
        for child_data in data['children']:
            if isinstance(child_data, dict):
                if child_data.get('type') == 'comment':
                    element.add_child(create_html_comment(child_data.get('content', '')))
                else:
                    element.add_child(dict_to_html(child_data))
    
    return element


def deep_copy_html_element(element: HtmlElement) -> HtmlElement:
    """Deep copy an HTML element."""
    new_element = HtmlElement(
        tag_name=element.tag_name,
        is_self_closing=element.is_self_closing,
        is_void_element=element.is_void_element
    )
    
    # Copy attributes
    for name, attr in element.attributes.items():
        new_element.attributes[name] = HtmlAttribute(
            name=attr.name,
            value=attr.value,
            is_boolean=attr.is_boolean
        )
    
    # Copy children
    for child in element.children:
        if isinstance(child, HtmlElement):
            new_element.add_child(deep_copy_html_element(child))
        elif isinstance(child, HtmlText):
            new_element.add_child(HtmlText(
                content=child.content,
                preserve_whitespace=child.preserve_whitespace
            ))
        elif isinstance(child, HtmlComment):
            new_element.add_child(HtmlComment(content=child.content))
    
    return new_element


# Extended visitor for additional functionality
class HtmlVisitorExtended(HtmlVisitor):
    """Extended visitor with additional methods."""
    pass