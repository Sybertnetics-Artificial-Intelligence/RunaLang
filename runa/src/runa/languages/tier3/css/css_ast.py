#!/usr/bin/env python3
"""
CSS AST Node Definitions

Complete CSS Abstract Syntax Tree node definitions for the Runa
universal translation system supporting CSS3 specification.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class CssNodeType(Enum):
    """CSS node types."""
    STYLESHEET = "stylesheet"
    RULE = "rule"
    SELECTOR = "selector"
    DECLARATION = "declaration"
    AT_RULE = "at_rule"
    COMMENT = "comment"
    MEDIA_QUERY = "media_query"


class CssVisitor(ABC):
    """Visitor interface for CSS AST nodes."""
    
    @abstractmethod
    def visit_css_stylesheet(self, node: 'CssStylesheet'): pass
    
    @abstractmethod
    def visit_css_rule(self, node: 'CssRule'): pass
    
    @abstractmethod
    def visit_css_selector(self, node: 'CssSelector'): pass
    
    @abstractmethod
    def visit_css_declaration(self, node: 'CssDeclaration'): pass
    
    @abstractmethod
    def visit_css_at_rule(self, node: 'CssAtRule'): pass
    
    @abstractmethod
    def visit_css_comment(self, node: 'CssComment'): pass
    
    @abstractmethod
    def visit_css_media_query(self, node: 'CssMediaQuery'): pass


class CssNode(ABC):
    """Base class for all CSS AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: CssVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class CssStylesheet(CssNode):
    """CSS stylesheet root."""
    rules: List['CssRule'] = field(default_factory=list)
    at_rules: List['CssAtRule'] = field(default_factory=list)
    comments: List['CssComment'] = field(default_factory=list)
    charset: Optional[str] = None
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_stylesheet(self)
    
    def add_rule(self, rule: 'CssRule'):
        """Add a CSS rule."""
        self.rules.append(rule)
    
    def add_at_rule(self, at_rule: 'CssAtRule'):
        """Add an at-rule."""
        self.at_rules.append(at_rule)
    
    def add_comment(self, comment: 'CssComment'):
        """Add a comment."""
        self.comments.append(comment)
    
    def find_rules_by_selector(self, selector_text: str) -> List['CssRule']:
        """Find rules that match a selector."""
        matching_rules = []
        for rule in self.rules:
            for selector in rule.selectors:
                if selector_text in selector.text:
                    matching_rules.append(rule)
                    break
        return matching_rules
    
    def find_declarations_by_property(self, property_name: str) -> List['CssDeclaration']:
        """Find all declarations with a specific property."""
        declarations = []
        for rule in self.rules:
            for decl in rule.declarations:
                if decl.property == property_name:
                    declarations.append(decl)
        return declarations


@dataclass
class CssRule(CssNode):
    """CSS rule (selector + declarations)."""
    selectors: List['CssSelector'] = field(default_factory=list)
    declarations: List['CssDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_rule(self)
    
    def add_selector(self, selector: 'CssSelector'):
        """Add a selector."""
        self.selectors.append(selector)
    
    def add_declaration(self, declaration: 'CssDeclaration'):
        """Add a declaration."""
        self.declarations.append(declaration)
    
    def get_selector_text(self) -> str:
        """Get combined selector text."""
        return ", ".join(selector.text for selector in self.selectors)
    
    def find_declaration(self, property_name: str) -> Optional['CssDeclaration']:
        """Find declaration by property name."""
        for decl in self.declarations:
            if decl.property == property_name:
                return decl
        return None


@dataclass
class CssSelector(CssNode):
    """CSS selector."""
    text: str
    specificity: Optional[Tuple[int, int, int, int]] = None  # (style, id, class, element)
    pseudo_elements: List[str] = field(default_factory=list)
    pseudo_classes: List[str] = field(default_factory=list)
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_selector(self)
    
    def calculate_specificity(self):
        """Calculate CSS specificity."""
        style = 0  # inline styles (not applicable here)
        ids = self.text.count('#')
        classes = self.text.count('.') + self.text.count('[') + len(self.pseudo_classes)
        elements = len([part for part in self.text.split() if part and not part.startswith(('.', '#', ':'))])
        
        self.specificity = (style, ids, classes, elements)
        return self.specificity
    
    @property
    def is_universal(self) -> bool:
        """Check if this is a universal selector."""
        return self.text.strip() == '*'
    
    @property
    def is_element(self) -> bool:
        """Check if this is an element selector."""
        return self.text.isalpha() and not self.text.startswith(('.', '#', ':'))
    
    @property
    def is_class(self) -> bool:
        """Check if this is a class selector."""
        return self.text.startswith('.')
    
    @property
    def is_id(self) -> bool:
        """Check if this is an ID selector."""
        return self.text.startswith('#')


@dataclass
class CssDeclaration(CssNode):
    """CSS declaration (property: value)."""
    property: str
    value: str
    important: bool = False
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_declaration(self)
    
    @property
    def full_value(self) -> str:
        """Get value with !important if applicable."""
        if self.important:
            return f"{self.value} !important"
        return self.value
    
    def parse_value_parts(self) -> List[str]:
        """Parse value into parts (space-separated)."""
        return self.value.split()
    
    def is_shorthand_property(self) -> bool:
        """Check if this is a shorthand property."""
        shorthand_props = {
            'margin', 'padding', 'border', 'font', 'background', 'outline',
            'border-radius', 'border-width', 'border-style', 'border-color'
        }
        return self.property in shorthand_props


@dataclass
class CssAtRule(CssNode):
    """CSS at-rule (@media, @import, etc.)."""
    name: str
    params: str = ""
    rules: List[CssRule] = field(default_factory=list)
    declarations: List[CssDeclaration] = field(default_factory=list)
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_at_rule(self)
    
    @property
    def is_media_query(self) -> bool:
        """Check if this is a media query."""
        return self.name == "media"
    
    @property
    def is_import(self) -> bool:
        """Check if this is an import rule."""
        return self.name == "import"
    
    @property
    def is_keyframes(self) -> bool:
        """Check if this is a keyframes rule."""
        return self.name in ("keyframes", "-webkit-keyframes", "-moz-keyframes")
    
    @property
    def is_font_face(self) -> bool:
        """Check if this is a font-face rule."""
        return self.name == "font-face"


@dataclass
class CssComment(CssNode):
    """CSS comment."""
    text: str
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_comment(self)


@dataclass
class CssMediaQuery(CssNode):
    """CSS media query."""
    media_type: str = "all"
    features: List[str] = field(default_factory=list)
    
    def accept(self, visitor: CssVisitor) -> Any:
        return visitor.visit_css_media_query(self)
    
    def to_string(self) -> str:
        """Convert to media query string."""
        if not self.features:
            return self.media_type
        
        features_str = " and ".join(self.features)
        if self.media_type == "all":
            return features_str
        return f"{self.media_type} and {features_str}"


# CSS Value Types
@dataclass
class CssValue:
    """CSS value with type information."""
    value: str
    unit: Optional[str] = None
    type: str = "unknown"  # color, length, percentage, number, string, etc.
    
    def is_color(self) -> bool:
        """Check if value is a color."""
        return self.type == "color" or self.value.startswith(('#', 'rgb', 'hsl', 'hwb'))
    
    def is_length(self) -> bool:
        """Check if value is a length."""
        return self.unit in ('px', 'em', 'rem', 'vh', 'vw', 'pt', 'pc', 'in', 'cm', 'mm')
    
    def is_percentage(self) -> bool:
        """Check if value is a percentage."""
        return self.unit == '%'
    
    def is_number(self) -> bool:
        """Check if value is a number."""
        return self.type == "number" and not self.unit


# CSS Property Categories
CSS_LAYOUT_PROPERTIES = {
    'display', 'position', 'top', 'right', 'bottom', 'left', 'z-index',
    'float', 'clear', 'width', 'height', 'max-width', 'max-height',
    'min-width', 'min-height', 'margin', 'padding', 'box-sizing'
}

CSS_TEXT_PROPERTIES = {
    'font-family', 'font-size', 'font-weight', 'font-style', 'font-variant',
    'line-height', 'text-align', 'text-decoration', 'text-transform',
    'letter-spacing', 'word-spacing', 'white-space', 'color'
}

CSS_BACKGROUND_PROPERTIES = {
    'background', 'background-color', 'background-image', 'background-repeat',
    'background-position', 'background-size', 'background-attachment'
}

CSS_BORDER_PROPERTIES = {
    'border', 'border-width', 'border-style', 'border-color', 'border-radius',
    'border-top', 'border-right', 'border-bottom', 'border-left'
}

CSS_ANIMATION_PROPERTIES = {
    'animation', 'animation-name', 'animation-duration', 'animation-timing-function',
    'animation-delay', 'animation-iteration-count', 'animation-direction',
    'transition', 'transform'
}


# Utility functions
def create_css_stylesheet() -> CssStylesheet:
    """Create an empty CSS stylesheet."""
    return CssStylesheet()


def create_css_rule(selectors: List[str] = None, declarations: Dict[str, str] = None) -> CssRule:
    """Create a CSS rule."""
    rule = CssRule()
    
    if selectors:
        for selector_text in selectors:
            rule.add_selector(CssSelector(text=selector_text))
    
    if declarations:
        for prop, value in declarations.items():
            # Check for !important
            important = False
            if value.endswith(' !important'):
                value = value[:-11].strip()
                important = True
            
            rule.add_declaration(CssDeclaration(property=prop, value=value, important=important))
    
    return rule


def create_css_selector(text: str) -> CssSelector:
    """Create a CSS selector."""
    selector = CssSelector(text=text.strip())
    selector.calculate_specificity()
    return selector


def create_css_declaration(property: str, value: str, important: bool = False) -> CssDeclaration:
    """Create a CSS declaration."""
    return CssDeclaration(property=property.strip(), value=value.strip(), important=important)


def create_css_at_rule(name: str, params: str = "", rules: List[CssRule] = None) -> CssAtRule:
    """Create a CSS at-rule."""
    return CssAtRule(name=name, params=params, rules=rules or [])


def create_css_comment(text: str) -> CssComment:
    """Create a CSS comment."""
    return CssComment(text=text.strip())


def parse_css_value(value_str: str) -> CssValue:
    """Parse CSS value and determine type."""
    value_str = value_str.strip()
    
    # Check for colors
    if value_str.startswith('#') or value_str.startswith('rgb') or value_str.startswith('hsl'):
        return CssValue(value=value_str, type="color")
    
    # Check for named colors
    named_colors = {
        'red', 'green', 'blue', 'black', 'white', 'gray', 'transparent',
        'inherit', 'initial', 'currentColor'
    }
    if value_str.lower() in named_colors:
        return CssValue(value=value_str, type="color")
    
    # Check for lengths/numbers with units
    import re
    unit_pattern = r'^(-?\d*\.?\d+)(px|em|rem|vh|vw|pt|pc|in|cm|mm|%|deg|rad|turn|s|ms)?$'
    match = re.match(unit_pattern, value_str)
    
    if match:
        number_part = match.group(1)
        unit_part = match.group(2)
        
        if unit_part == '%':
            return CssValue(value=number_part, unit=unit_part, type="percentage")
        elif unit_part in ('px', 'em', 'rem', 'vh', 'vw', 'pt', 'pc', 'in', 'cm', 'mm'):
            return CssValue(value=number_part, unit=unit_part, type="length")
        elif unit_part in ('deg', 'rad', 'turn'):
            return CssValue(value=number_part, unit=unit_part, type="angle")
        elif unit_part in ('s', 'ms'):
            return CssValue(value=number_part, unit=unit_part, type="time")
        elif not unit_part:
            return CssValue(value=number_part, type="number")
    
    # Default to string
    return CssValue(value=value_str, type="string")


def normalize_css_property(property: str) -> str:
    """Normalize CSS property name."""
    return property.lower().strip()


def normalize_css_value(value: str) -> str:
    """Normalize CSS value."""
    return ' '.join(value.split())


def is_css_shorthand_property(property: str) -> bool:
    """Check if property is a shorthand property."""
    shorthand_props = {
        'margin', 'padding', 'border', 'font', 'background', 'outline',
        'border-radius', 'border-width', 'border-style', 'border-color',
        'animation', 'transition', 'flex', 'grid-area'
    }
    return property in shorthand_props


def expand_css_shorthand(property: str, value: str) -> Dict[str, str]:
    """Expand shorthand property to individual properties."""
    parts = value.split()
    
    if property == 'margin' or property == 'padding':
        if len(parts) == 1:
            return {
                f"{property}-top": parts[0],
                f"{property}-right": parts[0],
                f"{property}-bottom": parts[0],
                f"{property}-left": parts[0]
            }
        elif len(parts) == 2:
            return {
                f"{property}-top": parts[0],
                f"{property}-right": parts[1],
                f"{property}-bottom": parts[0],
                f"{property}-left": parts[1]
            }
        elif len(parts) == 4:
            return {
                f"{property}-top": parts[0],
                f"{property}-right": parts[1],
                f"{property}-bottom": parts[2],
                f"{property}-left": parts[3]
            }
    
    # For other shorthands, return as-is for now
    return {property: value}


def get_css_property_category(property: str) -> str:
    """Get category of CSS property."""
    if property in CSS_LAYOUT_PROPERTIES:
        return "layout"
    elif property in CSS_TEXT_PROPERTIES:
        return "text"
    elif property in CSS_BACKGROUND_PROPERTIES:
        return "background"
    elif property in CSS_BORDER_PROPERTIES:
        return "border"
    elif property in CSS_ANIMATION_PROPERTIES:
        return "animation"
    else:
        return "other"


def css_to_dict(stylesheet: CssStylesheet) -> Dict[str, Any]:
    """Convert CSS stylesheet to dictionary representation."""
    result = {
        "type": "stylesheet",
        "rules": []
    }
    
    if stylesheet.charset:
        result["charset"] = stylesheet.charset
    
    # Add rules
    for rule in stylesheet.rules:
        rule_dict = {
            "type": "rule",
            "selectors": [sel.text for sel in rule.selectors],
            "declarations": []
        }
        
        for decl in rule.declarations:
            decl_dict = {
                "property": decl.property,
                "value": decl.value
            }
            if decl.important:
                decl_dict["important"] = True
            
            rule_dict["declarations"].append(decl_dict)
        
        result["rules"].append(rule_dict)
    
    # Add at-rules
    if stylesheet.at_rules:
        result["at_rules"] = []
        for at_rule in stylesheet.at_rules:
            at_rule_dict = {
                "type": "at_rule",
                "name": at_rule.name,
                "params": at_rule.params
            }
            if at_rule.rules:
                at_rule_dict["rules"] = [css_to_dict(CssStylesheet(rules=[r])) for r in at_rule.rules]
            
            result["at_rules"].append(at_rule_dict)
    
    return result


def dict_to_css(data: Dict[str, Any]) -> CssStylesheet:
    """Convert dictionary to CSS stylesheet."""
    stylesheet = CssStylesheet()
    
    if "charset" in data:
        stylesheet.charset = data["charset"]
    
    # Process rules
    for rule_data in data.get("rules", []):
        rule = CssRule()
        
        # Add selectors
        for selector_text in rule_data.get("selectors", []):
            rule.add_selector(CssSelector(text=selector_text))
        
        # Add declarations
        for decl_data in rule_data.get("declarations", []):
            declaration = CssDeclaration(
                property=decl_data["property"],
                value=decl_data["value"],
                important=decl_data.get("important", False)
            )
            rule.add_declaration(declaration)
        
        stylesheet.add_rule(rule)
    
    return stylesheet


# Extended visitor for additional functionality
class CssVisitorExtended(CssVisitor):
    """Extended visitor with additional methods."""
    pass