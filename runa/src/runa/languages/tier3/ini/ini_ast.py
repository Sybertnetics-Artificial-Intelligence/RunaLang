#!/usr/bin/env python3
"""
INI AST - Abstract Syntax Tree for INI Configuration Files

Provides comprehensive AST node definitions for INI files including:
- Section headers with hierarchical organization
- Key-value pairs with various data types
- Comments and documentation
- Multi-line values and string handling
- Case sensitivity options
- Different delimiter styles (= vs :)
- Environment variable interpolation
- Include file directives

Supports standard INI, Windows INI, and extended INI formats.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass


class ININode(ABC):
    """Base class for all INI AST nodes"""
    
    def __init__(self, location: Optional[Dict[str, Any]] = None):
        self.location = location or {}
        self.parent: Optional['ININode'] = None
        self.children: List['ININode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'INIVisitor') -> Any:
        """Accept visitor pattern implementation"""
        pass
    
    def add_child(self, child: 'ININode') -> None:
        """Add child node"""
        if child:
            child.parent = self
            self.children.append(child)


class INIValueType(Enum):
    """INI value types"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    LIST = "list"
    MULTILINE = "multiline"


class INIDelimiterType(Enum):
    """INI key-value delimiter types"""
    EQUALS = "="
    COLON = ":"
    SPACE = " "


class INICommentStyle(Enum):
    """INI comment styles"""
    SEMICOLON = ";"
    HASH = "#"


# Base INI Elements
@dataclass
class INIValue(ININode):
    """INI value with type information"""
    value: Any
    value_type: INIValueType
    raw_text: str
    is_quoted: bool = False
    quote_style: str = '"'
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_value(self)


@dataclass
class INIKey(ININode):
    """INI key"""
    name: str
    is_case_sensitive: bool = True
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_key(self)


@dataclass
class INIKeyValuePair(ININode):
    """INI key-value pair"""
    key: INIKey
    value: INIValue
    delimiter: INIDelimiterType = INIDelimiterType.EQUALS
    inline_comment: Optional['INIComment'] = None
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_key_value_pair(self)


@dataclass
class INISection(ININode):
    """INI section with header and entries"""
    name: str
    entries: List[Union[INIKeyValuePair, 'INIComment', 'INISubSection']]
    is_case_sensitive: bool = True
    is_root: bool = False  # True for implicit root section
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_section(self)
    
    def get_entry(self, key: str) -> Optional[INIKeyValuePair]:
        """Get entry by key name"""
        search_key = key if self.is_case_sensitive else key.lower()
        
        for entry in self.entries:
            if isinstance(entry, INIKeyValuePair):
                entry_key = entry.key.name
                if not self.is_case_sensitive:
                    entry_key = entry_key.lower()
                if entry_key == search_key:
                    return entry
        return None
    
    def add_entry(self, entry: Union[INIKeyValuePair, 'INIComment']) -> None:
        """Add entry to section"""
        self.entries.append(entry)
        self.add_child(entry)


@dataclass
class INISubSection(ININode):
    """INI subsection (nested section)"""
    name: str
    parent_section: str
    entries: List[Union[INIKeyValuePair, 'INIComment']]
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_subsection(self)


@dataclass
class INIComment(ININode):
    """INI comment"""
    text: str
    style: INICommentStyle = INICommentStyle.SEMICOLON
    is_inline: bool = False
    is_documentation: bool = False
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_comment(self)


@dataclass
class INIInterpolation(ININode):
    """INI variable interpolation (e.g., ${VAR} or %(var)s)"""
    variable_name: str
    default_value: Optional[str] = None
    format_style: str = "${}"  # ${}, %(...)s, or %{...}
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_interpolation(self)


@dataclass
class INIInclude(ININode):
    """INI include directive"""
    file_path: str
    is_optional: bool = False
    relative_to_current: bool = True
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_include(self)


@dataclass
class INIConfiguration(ININode):
    """Complete INI configuration file"""
    sections: List[INISection]
    global_entries: List[Union[INIKeyValuePair, INIComment, INIInclude]]  # Entries before any section
    filename: Optional[str] = None
    encoding: str = "utf-8"
    case_sensitive: bool = True
    allow_multiline: bool = True
    comment_prefixes: List[str] = None
    delimiters: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.comment_prefixes is None:
            self.comment_prefixes = [';', '#']
        if self.delimiters is None:
            self.delimiters = ['=', ':']
        if self.metadata is None:
            self.metadata = {}
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_configuration(self)
    
    def get_section(self, name: str) -> Optional[INISection]:
        """Get section by name"""
        search_name = name if self.case_sensitive else name.lower()
        
        for section in self.sections:
            section_name = section.name
            if not self.case_sensitive:
                section_name = section_name.lower()
            if section_name == search_name:
                return section
        return None
    
    def add_section(self, section: INISection) -> None:
        """Add section to configuration"""
        self.sections.append(section)
        self.add_child(section)
    
    def get_value(self, section_name: str, key_name: str) -> Optional[Any]:
        """Get value by section and key"""
        section = self.get_section(section_name)
        if section:
            entry = section.get_entry(key_name)
            if entry:
                return entry.value.value
        return None
    
    def set_value(self, section_name: str, key_name: str, value: Any) -> None:
        """Set value by section and key"""
        section = self.get_section(section_name)
        if not section:
            section = INISection(
                name=section_name,
                entries=[],
                is_case_sensitive=self.case_sensitive
            )
            self.add_section(section)
        
        entry = section.get_entry(key_name)
        if entry:
            entry.value.value = value
            entry.value.raw_text = str(value)
        else:
            key = INIKey(key_name, self.case_sensitive)
            value_node = INIValue(
                value=value,
                value_type=self._infer_value_type(value),
                raw_text=str(value)
            )
            new_entry = INIKeyValuePair(key, value_node)
            section.add_entry(new_entry)
    
    def _infer_value_type(self, value: Any) -> INIValueType:
        """Infer INI value type from Python value"""
        if isinstance(value, bool):
            return INIValueType.BOOLEAN
        elif isinstance(value, (int, float)):
            return INIValueType.NUMBER
        elif isinstance(value, list):
            return INIValueType.LIST
        elif isinstance(value, str) and '\n' in value:
            return INIValueType.MULTILINE
        else:
            return INIValueType.STRING


# Extended INI Elements
@dataclass
class INIArray(ININode):
    """INI array value (comma-separated or multi-line)"""
    elements: List[INIValue]
    is_multiline: bool = False
    separator: str = ","
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_array(self)


@dataclass
class INIConditional(ININode):
    """INI conditional section or entry"""
    condition: str
    true_entries: List[Union[INIKeyValuePair, INISection]]
    false_entries: List[Union[INIKeyValuePair, INISection]] = None
    
    def __post_init__(self):
        if self.false_entries is None:
            self.false_entries = []
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_conditional(self)


@dataclass
class INILoop(ININode):
    """INI loop construct for generating multiple entries"""
    variable: str
    iterable: List[str]
    template_entries: List[Union[INIKeyValuePair, INISection]]
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_loop(self)


@dataclass
class INIMacro(ININode):
    """INI macro definition"""
    name: str
    parameters: List[str]
    body: List[Union[INIKeyValuePair, INISection]]
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_macro(self)


@dataclass
class INIMacroCall(ININode):
    """INI macro invocation"""
    macro_name: str
    arguments: Dict[str, Any]
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_macro_call(self)


# Special INI Formats
@dataclass
class WindowsINISection(INISection):
    """Windows INI section with specific behaviors"""
    is_system: bool = False
    registry_path: Optional[str] = None
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_windows_section(self)


@dataclass
class GitConfigSection(INISection):
    """Git config section with subsection support"""
    subsection: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        """Get full section name including subsection"""
        if self.subsection:
            return f"{self.name} \"{self.subsection}\""
        return self.name
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_git_section(self)


@dataclass
class SystemdConfigSection(INISection):
    """Systemd configuration section"""
    unit_type: Optional[str] = None
    
    def accept(self, visitor: 'INIVisitor') -> Any:
        return visitor.visit_systemd_section(self)


# Visitor Pattern
class INIVisitor(ABC):
    """Abstract visitor for INI AST traversal"""
    
    @abstractmethod
    def visit_configuration(self, node: INIConfiguration) -> Any:
        pass
    
    @abstractmethod
    def visit_section(self, node: INISection) -> Any:
        pass
    
    @abstractmethod
    def visit_subsection(self, node: INISubSection) -> Any:
        pass
    
    @abstractmethod
    def visit_key_value_pair(self, node: INIKeyValuePair) -> Any:
        pass
    
    @abstractmethod
    def visit_key(self, node: INIKey) -> Any:
        pass
    
    @abstractmethod
    def visit_value(self, node: INIValue) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: INIComment) -> Any:
        pass
    
    @abstractmethod
    def visit_interpolation(self, node: INIInterpolation) -> Any:
        pass
    
    @abstractmethod
    def visit_include(self, node: INIInclude) -> Any:
        pass
    
    @abstractmethod
    def visit_array(self, node: INIArray) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional(self, node: INIConditional) -> Any:
        pass
    
    @abstractmethod
    def visit_loop(self, node: INILoop) -> Any:
        pass
    
    @abstractmethod
    def visit_macro(self, node: INIMacro) -> Any:
        pass
    
    @abstractmethod
    def visit_macro_call(self, node: INIMacroCall) -> Any:
        pass
    
    @abstractmethod
    def visit_windows_section(self, node: WindowsINISection) -> Any:
        pass
    
    @abstractmethod
    def visit_git_section(self, node: GitConfigSection) -> Any:
        pass
    
    @abstractmethod
    def visit_systemd_section(self, node: SystemdConfigSection) -> Any:
        pass


class INIBaseVisitor(INIVisitor):
    """Base visitor with default implementations"""
    
    def visit_configuration(self, node: INIConfiguration) -> Any:
        for entry in node.global_entries:
            entry.accept(self)
        for section in node.sections:
            section.accept(self)
    
    def visit_section(self, node: INISection) -> Any:
        for entry in node.entries:
            entry.accept(self)
    
    def visit_subsection(self, node: INISubSection) -> Any:
        for entry in node.entries:
            entry.accept(self)
    
    def visit_key_value_pair(self, node: INIKeyValuePair) -> Any:
        node.key.accept(self)
        node.value.accept(self)
        if node.inline_comment:
            node.inline_comment.accept(self)
    
    def visit_key(self, node: INIKey) -> Any:
        pass
    
    def visit_value(self, node: INIValue) -> Any:
        pass
    
    def visit_comment(self, node: INIComment) -> Any:
        pass
    
    def visit_interpolation(self, node: INIInterpolation) -> Any:
        pass
    
    def visit_include(self, node: INIInclude) -> Any:
        pass
    
    def visit_array(self, node: INIArray) -> Any:
        for element in node.elements:
            element.accept(self)
    
    def visit_conditional(self, node: INIConditional) -> Any:
        for entry in node.true_entries:
            entry.accept(self)
        for entry in node.false_entries:
            entry.accept(self)
    
    def visit_loop(self, node: INILoop) -> Any:
        for entry in node.template_entries:
            entry.accept(self)
    
    def visit_macro(self, node: INIMacro) -> Any:
        for entry in node.body:
            entry.accept(self)
    
    def visit_macro_call(self, node: INIMacroCall) -> Any:
        pass
    
    def visit_windows_section(self, node: WindowsINISection) -> Any:
        self.visit_section(node)
    
    def visit_git_section(self, node: GitConfigSection) -> Any:
        self.visit_section(node)
    
    def visit_systemd_section(self, node: SystemdConfigSection) -> Any:
        self.visit_section(node)


# Utility Functions
def create_ini_value(value: Any, raw_text: Optional[str] = None) -> INIValue:
    """Create INI value from Python value"""
    if raw_text is None:
        raw_text = str(value)
    
    if isinstance(value, bool):
        return INIValue(value, INIValueType.BOOLEAN, raw_text)
    elif isinstance(value, (int, float)):
        return INIValue(value, INIValueType.NUMBER, raw_text)
    elif isinstance(value, list):
        return INIValue(value, INIValueType.LIST, raw_text)
    elif isinstance(value, str) and '\n' in value:
        return INIValue(value, INIValueType.MULTILINE, raw_text)
    else:
        return INIValue(value, INIValueType.STRING, raw_text)


def create_ini_section(name: str, case_sensitive: bool = True) -> INISection:
    """Create INI section"""
    return INISection(
        name=name,
        entries=[],
        is_case_sensitive=case_sensitive
    )


def create_ini_configuration(case_sensitive: bool = True) -> INIConfiguration:
    """Create empty INI configuration"""
    return INIConfiguration(
        sections=[],
        global_entries=[],
        case_sensitive=case_sensitive
    )


# Common INI Formats
INI_FORMATS = {
    "standard": {
        "case_sensitive": False,
        "comment_prefixes": [';', '#'],
        "delimiters": ['=', ':'],
        "allow_multiline": True,
        "interpolation": False
    },
    "windows": {
        "case_sensitive": False,
        "comment_prefixes": [';'],
        "delimiters": ['='],
        "allow_multiline": False,
        "interpolation": False
    },
    "git": {
        "case_sensitive": True,
        "comment_prefixes": ['#', ';'],
        "delimiters": ['='],
        "allow_multiline": True,
        "interpolation": False,
        "subsections": True
    },
    "systemd": {
        "case_sensitive": True,
        "comment_prefixes": ['#'],
        "delimiters": ['='],
        "allow_multiline": True,
        "interpolation": True
    },
    "python": {
        "case_sensitive": True,
        "comment_prefixes": ['#'],
        "delimiters": ['=', ':'],
        "allow_multiline": True,
        "interpolation": True,
        "interpolation_style": "%(...)s"
    }
} 