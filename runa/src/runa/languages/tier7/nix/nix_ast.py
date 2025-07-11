#!/usr/bin/env python3
"""
Nix AST - Abstract Syntax Tree for Nix Expression Language

Comprehensive AST representation supporting:
- Functional expressions (functions, applications, closures)
- Attribute sets and attribute access
- Lists and list operations
- String interpolations and literals
- Derivations and package definitions
- Let expressions and variable bindings
- Conditionals and pattern matching
- Import and include system
- Built-in functions and operators
- Lazy evaluation constructs
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Base AST Node Classes

@dataclass
class NixNode(ABC):
    """Base class for all Nix AST nodes"""
    line_number: int = 0
    column_number: int = 0
    source_file: Optional[str] = None
    
    @abstractmethod
    def accept(self, visitor: 'NixVisitor') -> Any:
        """Accept visitor for traversal"""
        pass

@dataclass 
class NixExpression(NixNode):
    """Base class for Nix expressions"""
    pass

@dataclass
class NixStatement(NixNode): 
    """Base class for Nix statements"""
    pass

# Core AST Node Types

@dataclass
class NixFile(NixNode):
    """Root node representing a complete Nix file"""
    expression: NixExpression
    imports: List['ImportExpression'] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_nix_file(self)

# Literals and Basic Types

@dataclass
class StringLiteral(NixExpression):
    """String literal with interpolation support"""
    value: str
    has_interpolation: bool = False
    interpolated_parts: List[NixExpression] = field(default_factory=list)
    quote_style: str = '"'  # ", '', or ''
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_string_literal(self)

@dataclass
class IntegerLiteral(NixExpression):
    """Integer literal"""
    value: int
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_integer_literal(self)

@dataclass
class FloatLiteral(NixExpression):
    """Float literal"""
    value: float
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_float_literal(self)

@dataclass
class BooleanLiteral(NixExpression):
    """Boolean literal"""
    value: bool
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_boolean_literal(self)

@dataclass
class NullLiteral(NixExpression):
    """Null literal"""
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_null_literal(self)

@dataclass
class PathLiteral(NixExpression):
    """Path literal"""
    value: str
    is_absolute: bool = False
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_path_literal(self)

# Identifiers and Variables

@dataclass
class Identifier(NixExpression):
    """Variable identifier"""
    name: str
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_identifier(self)

# Attribute Sets

@dataclass
class AttributeSet(NixExpression):
    """Attribute set { a = 1; b = 2; }"""
    attributes: List['AttributeBinding'] = field(default_factory=list)
    is_recursive: bool = False  # rec { ... }
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_attribute_set(self)

@dataclass
class AttributeBinding(NixNode):
    """Attribute binding inside attribute set"""
    path: List[str]  # For nested attributes like a.b.c
    value: NixExpression
    is_inherit: bool = False
    inherit_source: Optional[NixExpression] = None  # For inherit (source) attr;
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_attribute_binding(self)

@dataclass
class AttributeAccess(NixExpression):
    """Attribute access expr.attr or expr."attr\""""
    expression: NixExpression
    attribute: Union[str, NixExpression]
    has_default: bool = False
    default_value: Optional[NixExpression] = None  # For expr.attr or default
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_attribute_access(self)

# Lists

@dataclass
class ListExpression(NixExpression):
    """List expression [ a b c ]"""
    elements: List[NixExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_list_expression(self)

# Functions

@dataclass
class FunctionExpression(NixExpression):
    """Function expression arg: body or { args }: body"""
    parameter: Union[str, 'FunctionParameters']
    body: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_function_expression(self)

@dataclass
class FunctionParameters(NixNode):
    """Function parameters for destructuring { a, b ? default, ... }"""
    parameters: Dict[str, Optional[NixExpression]] = field(default_factory=dict)  # name -> default
    has_ellipsis: bool = False  # ...
    at_pattern: Optional[str] = None  # @ name for the whole argument
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_function_parameters(self)

@dataclass
class FunctionApplication(NixExpression):
    """Function application func arg"""
    function: NixExpression
    argument: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_function_application(self)

# Let Expressions

@dataclass
class LetExpression(NixExpression):
    """Let expression let bindings in expr"""
    bindings: List[AttributeBinding] = field(default_factory=list)
    body: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_let_expression(self)

# Conditionals

@dataclass
class ConditionalExpression(NixExpression):
    """Conditional expression if cond then expr1 else expr2"""
    condition: NixExpression
    then_expr: NixExpression
    else_expr: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_conditional_expression(self)

# Binary Operations

@dataclass
class BinaryOperation(NixExpression):
    """Binary operation expr1 op expr2"""
    left: NixExpression
    operator: str
    right: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_binary_operation(self)

# Unary Operations

@dataclass
class UnaryOperation(NixExpression):
    """Unary operation !expr or -expr"""
    operator: str
    operand: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_unary_operation(self)

# With Expression

@dataclass
class WithExpression(NixExpression):
    """With expression with expr1; expr2"""
    namespace: NixExpression
    body: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_with_expression(self)

# Assert Expression

@dataclass
class AssertExpression(NixExpression):
    """Assert expression assert condition; expr"""
    condition: NixExpression
    body: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_assert_expression(self)

# Import and Include

@dataclass
class ImportExpression(NixExpression):
    """Import expression import path"""
    path: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_import_expression(self)

# Derivations and Packages

@dataclass
class DerivationExpression(NixExpression):
    """Derivation expression (special attribute set for builds)"""
    attributes: List[AttributeBinding] = field(default_factory=list)
    name: Optional[str] = None
    system: Optional[str] = None
    builder: Optional[NixExpression] = None
    build_inputs: List[NixExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_derivation_expression(self)

# Built-in Functions

@dataclass
class BuiltinFunction(NixExpression):
    """Built-in function reference"""
    name: str
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_builtin_function(self)

# String Interpolation

@dataclass
class StringInterpolation(NixExpression):
    """String interpolation ${expr}"""
    expression: NixExpression
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_string_interpolation(self)

# Comments

@dataclass
class Comment(NixNode):
    """Comment in Nix code"""
    text: str
    is_block: bool = False  # /* */ vs #
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_comment(self)

# Advanced Constructs

@dataclass
class PackageExpression(NixExpression):
    """Package expression with metadata"""
    name: str
    version: Optional[str] = None
    derivation: DerivationExpression
    meta: Optional[AttributeSet] = None
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_package_expression(self)

@dataclass
class OverrideExpression(NixExpression):
    """Package override expression pkg.override { ... }"""
    package: NixExpression
    overrides: AttributeSet
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_override_expression(self)

@dataclass
class CallPackageExpression(NixExpression):
    """callPackage expression for Nixpkgs"""
    package_path: NixExpression
    arguments: Optional[AttributeSet] = None
    
    def accept(self, visitor: 'NixVisitor') -> Any:
        return visitor.visit_call_package_expression(self)

# Visitor Pattern

class NixVisitor(ABC):
    """Abstract visitor for Nix AST traversal"""
    
    @abstractmethod
    def visit_nix_file(self, node: NixFile) -> Any:
        pass
    
    @abstractmethod
    def visit_string_literal(self, node: StringLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_integer_literal(self, node: IntegerLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_float_literal(self, node: FloatLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_null_literal(self, node: NullLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_path_literal(self, node: PathLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute_set(self, node: AttributeSet) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute_binding(self, node: AttributeBinding) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute_access(self, node: AttributeAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_list_expression(self, node: ListExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_function_expression(self, node: FunctionExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_function_parameters(self, node: FunctionParameters) -> Any:
        pass
    
    @abstractmethod
    def visit_function_application(self, node: FunctionApplication) -> Any:
        pass
    
    @abstractmethod
    def visit_let_expression(self, node: LetExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional_expression(self, node: ConditionalExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_operation(self, node: BinaryOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_operation(self, node: UnaryOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_with_expression(self, node: WithExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_assert_expression(self, node: AssertExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_import_expression(self, node: ImportExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_derivation_expression(self, node: DerivationExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_builtin_function(self, node: BuiltinFunction) -> Any:
        pass
    
    @abstractmethod
    def visit_string_interpolation(self, node: StringInterpolation) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: Comment) -> Any:
        pass
    
    @abstractmethod
    def visit_package_expression(self, node: PackageExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_override_expression(self, node: OverrideExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_call_package_expression(self, node: CallPackageExpression) -> Any:
        pass

# Utility Functions

def create_simple_attribute_set(attributes: Dict[str, NixExpression]) -> AttributeSet:
    """Create simple attribute set from dict"""
    bindings = []
    for name, value in attributes.items():
        binding = AttributeBinding(path=[name], value=value)
        bindings.append(binding)
    return AttributeSet(attributes=bindings)

def create_function(param_name: str, body: NixExpression) -> FunctionExpression:
    """Create simple function"""
    return FunctionExpression(parameter=param_name, body=body)

def create_function_call(func: NixExpression, arg: NixExpression) -> FunctionApplication:
    """Create function application"""
    return FunctionApplication(function=func, argument=arg)

def create_let_binding(name: str, value: NixExpression) -> AttributeBinding:
    """Create let binding"""
    return AttributeBinding(path=[name], value=value)

def create_derivation(name: str, builder: str, **kwargs) -> DerivationExpression:
    """Create basic derivation"""
    attrs = [
        AttributeBinding(path=["name"], value=StringLiteral(name)),
        AttributeBinding(path=["builder"], value=StringLiteral(builder))
    ]
    
    for key, value in kwargs.items():
        if isinstance(value, str):
            value = StringLiteral(value)
        attrs.append(AttributeBinding(path=[key], value=value))
    
    return DerivationExpression(attributes=attrs, name=name, builder=StringLiteral(builder))

# AST Builder for common patterns
class NixASTBuilder:
    """Builder for constructing Nix AST nodes"""
    
    def __init__(self):
        self.expression = None
        
    def string(self, value: str) -> 'NixASTBuilder':
        """Add string literal"""
        self.expression = StringLiteral(value)
        return self
        
    def integer(self, value: int) -> 'NixASTBuilder':
        """Add integer literal"""
        self.expression = IntegerLiteral(value)
        return self
        
    def boolean(self, value: bool) -> 'NixASTBuilder':
        """Add boolean literal"""
        self.expression = BooleanLiteral(value)
        return self
        
    def identifier(self, name: str) -> 'NixASTBuilder':
        """Add identifier"""
        self.expression = Identifier(name)
        return self
        
    def attribute_set(self, **attributes) -> 'NixASTBuilder':
        """Add attribute set"""
        self.expression = create_simple_attribute_set({
            k: StringLiteral(v) if isinstance(v, str) else v 
            for k, v in attributes.items()
        })
        return self
        
    def list_expr(self, *elements) -> 'NixASTBuilder':
        """Add list expression"""
        nix_elements = []
        for elem in elements:
            if isinstance(elem, str):
                nix_elements.append(StringLiteral(elem))
            elif isinstance(elem, NixExpression):
                nix_elements.append(elem)
            else:
                nix_elements.append(StringLiteral(str(elem)))
        self.expression = ListExpression(nix_elements)
        return self
        
    def function(self, param: str, body: NixExpression) -> 'NixASTBuilder':
        """Add function"""
        self.expression = create_function(param, body)
        return self
        
    def build(self) -> NixExpression:
        """Build the final expression"""
        return self.expression or NullLiteral()

# Built-in function names for reference
BUILTIN_FUNCTIONS = {
    # Type checking
    'isAttrs', 'isBool', 'isFloat', 'isFunction', 'isInt', 'isList', 'isNull', 'isString',
    
    # List operations
    'length', 'head', 'tail', 'elem', 'filter', 'map', 'sort', 'reverse', 'unique',
    'concatLists', 'listToAttrs', 'genList', 'range', 'partition',
    
    # String operations
    'toString', 'stringLength', 'substring', 'split', 'concatStringsSep', 'replaceStrings',
    'hasPrefix', 'hasSuffix', 'removePrefix', 'removeSuffix', 'trim', 'toLower', 'toUpper',
    
    # Attribute set operations
    'attrNames', 'attrValues', 'hasAttr', 'getAttr', 'removeAttrs', 'intersectAttrs',
    'catAttrs', 'mapAttrs', 'mapAttrsToList', 'filterAttrs', 'foldAttrs',
    
    # File operations
    'readFile', 'readDir', 'pathExists', 'baseNameOf', 'dirOf', 'import',
    
    # Derivation operations
    'derivation', 'derivationStrict', 'placeholder',
    
    # Math operations
    'add', 'sub', 'mul', 'div', 'lessThan', 'floor', 'ceil',
    
    # Misc
    'abort', 'throw', 'trace', 'seq', 'deepSeq', 'tryEval', 'typeOf'
}

# Export main classes
__all__ = [
    # Base classes
    'NixNode', 'NixExpression', 'NixStatement', 'NixVisitor',
    
    # Core nodes
    'NixFile', 'Identifier',
    
    # Literals
    'StringLiteral', 'IntegerLiteral', 'FloatLiteral', 'BooleanLiteral', 'NullLiteral', 'PathLiteral',
    
    # Complex expressions
    'AttributeSet', 'AttributeBinding', 'AttributeAccess', 'ListExpression',
    'FunctionExpression', 'FunctionParameters', 'FunctionApplication',
    'LetExpression', 'ConditionalExpression', 'BinaryOperation', 'UnaryOperation',
    'WithExpression', 'AssertExpression', 'ImportExpression',
    'DerivationExpression', 'BuiltinFunction', 'StringInterpolation',
    'PackageExpression', 'OverrideExpression', 'CallPackageExpression',
    
    # Comments
    'Comment',
    
    # Utilities
    'create_simple_attribute_set', 'create_function', 'create_function_call',
    'create_let_binding', 'create_derivation', 'NixASTBuilder',
    'BUILTIN_FUNCTIONS'
] 