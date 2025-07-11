#!/usr/bin/env python3
"""
AssemblyScript AST Node Definitions

Complete AssemblyScript Abstract Syntax Tree node definitions for the Runa
universal translation system supporting AssemblyScript specification.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class AsNodeType(Enum):
    """AssemblyScript node types."""
    PROGRAM = "program"
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = "interface"
    VARIABLE = "variable"
    EXPRESSION = "expression"
    STATEMENT = "statement"
    TYPE = "type"
    IMPORT = "import"
    EXPORT = "export"


class AsVisitor(ABC):
    """Visitor interface for AssemblyScript AST nodes."""
    
    @abstractmethod
    def visit_as_program(self, node: 'AsProgram'): pass
    
    @abstractmethod
    def visit_as_function(self, node: 'AsFunction'): pass
    
    @abstractmethod
    def visit_as_class(self, node: 'AsClass'): pass
    
    @abstractmethod
    def visit_as_interface(self, node: 'AsInterface'): pass
    
    @abstractmethod
    def visit_as_variable_declaration(self, node: 'AsVariableDeclaration'): pass
    
    @abstractmethod
    def visit_as_expression(self, node: 'AsExpression'): pass
    
    @abstractmethod
    def visit_as_statement(self, node: 'AsStatement'): pass
    
    @abstractmethod
    def visit_as_type(self, node: 'AsType'): pass
    
    @abstractmethod
    def visit_as_import(self, node: 'AsImport'): pass
    
    @abstractmethod
    def visit_as_export(self, node: 'AsExport'): pass


class AsNode(ABC):
    """Base class for all AssemblyScript AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: AsVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AsProgram(AsNode):
    """AssemblyScript program (top-level module)."""
    statements: List['AsStatement'] = field(default_factory=list)
    imports: List['AsImport'] = field(default_factory=list)
    exports: List['AsExport'] = field(default_factory=list)
    module_name: Optional[str] = None
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_program(self)


@dataclass
class AsType(AsNode):
    """AssemblyScript type annotation."""
    name: str
    generic_args: List['AsType'] = field(default_factory=list)
    is_nullable: bool = False
    is_array: bool = False
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_type(self)
    
    @property
    def full_name(self) -> str:
        """Get full type name including generics."""
        base = self.name
        
        if self.generic_args:
            args = ", ".join(arg.full_name for arg in self.generic_args)
            base = f"{base}<{args}>"
        
        if self.is_array:
            base = f"{base}[]"
        
        if self.is_nullable:
            base = f"{base} | null"
        
        return base


@dataclass 
class AsStatement(AsNode):
    """Base class for AssemblyScript statements."""
    pass


@dataclass
class AsExpression(AsNode):
    """Base class for AssemblyScript expressions."""
    result_type: Optional[AsType] = None
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_expression(self)


@dataclass
class AsFunction(AsStatement):
    """AssemblyScript function declaration."""
    name: str
    parameters: List['AsParameter'] = field(default_factory=list)
    return_type: Optional[AsType] = None
    body: List[AsStatement] = field(default_factory=list)
    is_export: bool = False
    is_inline: bool = False
    is_operator: bool = False
    generic_params: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_function(self)


@dataclass
class AsParameter:
    """AssemblyScript function parameter."""
    name: str
    param_type: AsType
    default_value: Optional[AsExpression] = None
    is_optional: bool = False
    is_rest: bool = False


@dataclass
class AsClass(AsStatement):
    """AssemblyScript class declaration."""
    name: str
    super_class: Optional[str] = None
    implements: List[str] = field(default_factory=list)
    members: List['AsClassMember'] = field(default_factory=list)
    generic_params: List[str] = field(default_factory=list)
    is_export: bool = False
    is_abstract: bool = False
    decorators: List[str] = field(default_factory=list)
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_class(self)


@dataclass
class AsInterface(AsStatement):
    """AssemblyScript interface declaration."""
    name: str
    extends: List[str] = field(default_factory=list)
    members: List['AsInterfaceMember'] = field(default_factory=list)
    generic_params: List[str] = field(default_factory=list)
    is_export: bool = False
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_interface(self)


@dataclass
class AsClassMember:
    """AssemblyScript class member."""
    name: str
    member_type: str  # "field", "method", "getter", "setter", "constructor"
    access_modifier: str = "public"  # "public", "private", "protected"
    is_static: bool = False
    is_readonly: bool = False
    is_abstract: bool = False
    field_type: Optional[AsType] = None
    method: Optional[AsFunction] = None
    initial_value: Optional[AsExpression] = None


@dataclass
class AsInterfaceMember:
    """AssemblyScript interface member."""
    name: str
    member_type: str  # "method", "property"
    signature_type: Optional[AsType] = None
    method_params: List[AsParameter] = field(default_factory=list)
    return_type: Optional[AsType] = None


@dataclass
class AsVariableDeclaration(AsStatement):
    """AssemblyScript variable declaration."""
    name: str
    var_type: Optional[AsType] = None
    initial_value: Optional[AsExpression] = None
    is_const: bool = False
    is_let: bool = True
    is_export: bool = False
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_variable_declaration(self)


@dataclass
class AsBlock(AsStatement):
    """AssemblyScript block statement."""
    statements: List[AsStatement] = field(default_factory=list)


@dataclass
class AsIfStatement(AsStatement):
    """AssemblyScript if statement."""
    condition: AsExpression
    then_statement: AsStatement
    else_statement: Optional[AsStatement] = None


@dataclass
class AsWhileStatement(AsStatement):
    """AssemblyScript while statement."""
    condition: AsExpression
    body: AsStatement


@dataclass
class AsForStatement(AsStatement):
    """AssemblyScript for statement."""
    init: Optional[AsStatement] = None
    condition: Optional[AsExpression] = None
    update: Optional[AsExpression] = None
    body: AsStatement = None


@dataclass
class AsReturnStatement(AsStatement):
    """AssemblyScript return statement."""
    value: Optional[AsExpression] = None


@dataclass
class AsExpressionStatement(AsStatement):
    """AssemblyScript expression statement."""
    expression: AsExpression


# Expressions
@dataclass
class AsLiteral(AsExpression):
    """AssemblyScript literal expression."""
    value: Any
    literal_type: str  # "number", "string", "boolean", "null"


@dataclass
class AsIdentifier(AsExpression):
    """AssemblyScript identifier expression."""
    name: str


@dataclass
class AsBinaryExpression(AsExpression):
    """AssemblyScript binary expression."""
    left: AsExpression
    operator: str
    right: AsExpression


@dataclass
class AsUnaryExpression(AsExpression):
    """AssemblyScript unary expression."""
    operator: str
    operand: AsExpression
    is_prefix: bool = True


@dataclass
class AsCallExpression(AsExpression):
    """AssemblyScript function call expression."""
    function: AsExpression
    arguments: List[AsExpression] = field(default_factory=list)
    type_arguments: List[AsType] = field(default_factory=list)


@dataclass
class AsMemberExpression(AsExpression):
    """AssemblyScript member access expression."""
    object: AsExpression
    property: AsExpression
    computed: bool = False  # obj[prop] vs obj.prop


@dataclass
class AsArrayExpression(AsExpression):
    """AssemblyScript array literal expression."""
    elements: List[Optional[AsExpression]] = field(default_factory=list)


@dataclass
class AsObjectExpression(AsExpression):
    """AssemblyScript object literal expression."""
    properties: List['AsProperty'] = field(default_factory=list)


@dataclass
class AsProperty:
    """AssemblyScript object property."""
    key: AsExpression
    value: AsExpression
    computed: bool = False
    shorthand: bool = False


@dataclass
class AsNewExpression(AsExpression):
    """AssemblyScript new expression."""
    constructor: AsExpression
    arguments: List[AsExpression] = field(default_factory=list)
    type_arguments: List[AsType] = field(default_factory=list)


@dataclass
class AsImport(AsStatement):
    """AssemblyScript import statement."""
    source: str
    specifiers: List['AsImportSpecifier'] = field(default_factory=list)
    import_type: str = "default"  # "default", "namespace", "named"
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_import(self)


@dataclass
class AsImportSpecifier:
    """AssemblyScript import specifier."""
    imported: str
    local: Optional[str] = None


@dataclass
class AsExport(AsStatement):
    """AssemblyScript export statement."""
    declaration: Optional[AsStatement] = None
    specifiers: List['AsExportSpecifier'] = field(default_factory=list)
    source: Optional[str] = None
    export_type: str = "named"  # "named", "default", "all"
    
    def accept(self, visitor: AsVisitor) -> Any:
        return visitor.visit_as_export(self)


@dataclass
class AsExportSpecifier:
    """AssemblyScript export specifier."""
    local: str
    exported: Optional[str] = None


# AssemblyScript built-in types
AS_BUILTIN_TYPES = {
    # Integer types
    'i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64',
    'isize', 'usize',
    
    # Floating point types
    'f32', 'f64',
    
    # Other types
    'bool', 'void', 'never',
    
    # Reference types
    'string', 'String',
    
    # Array types
    'Array', 'Int8Array', 'Uint8Array', 'Int16Array', 'Uint16Array',
    'Int32Array', 'Uint32Array', 'Float32Array', 'Float64Array',
    
    # Map and Set
    'Map', 'Set',
    
    # Memory types
    'ArrayBuffer', 'DataView'
}


# Utility functions
def create_as_program(statements: List[AsStatement] = None) -> AsProgram:
    """Create an AssemblyScript program."""
    return AsProgram(statements=statements or [])


def create_as_function(name: str,
                      parameters: List[AsParameter] = None,
                      return_type: AsType = None,
                      body: List[AsStatement] = None) -> AsFunction:
    """Create an AssemblyScript function."""
    return AsFunction(
        name=name,
        parameters=parameters or [],
        return_type=return_type,
        body=body or []
    )


def create_as_class(name: str,
                   super_class: str = None,
                   members: List[AsClassMember] = None) -> AsClass:
    """Create an AssemblyScript class."""
    return AsClass(
        name=name,
        super_class=super_class,
        members=members or []
    )


def create_as_variable(name: str,
                      var_type: AsType = None,
                      initial_value: AsExpression = None,
                      is_const: bool = False) -> AsVariableDeclaration:
    """Create an AssemblyScript variable declaration."""
    return AsVariableDeclaration(
        name=name,
        var_type=var_type,
        initial_value=initial_value,
        is_const=is_const,
        is_let=not is_const
    )


def create_as_type(name: str,
                  generic_args: List[AsType] = None,
                  is_nullable: bool = False,
                  is_array: bool = False) -> AsType:
    """Create an AssemblyScript type."""
    return AsType(
        name=name,
        generic_args=generic_args or [],
        is_nullable=is_nullable,
        is_array=is_array
    )


def create_as_literal(value: Any, literal_type: str = None) -> AsLiteral:
    """Create an AssemblyScript literal."""
    if literal_type is None:
        if isinstance(value, bool):
            literal_type = "boolean"
        elif isinstance(value, (int, float)):
            literal_type = "number"
        elif isinstance(value, str):
            literal_type = "string"
        elif value is None:
            literal_type = "null"
        else:
            literal_type = "unknown"
    
    return AsLiteral(value=value, literal_type=literal_type)


def create_as_identifier(name: str) -> AsIdentifier:
    """Create an AssemblyScript identifier."""
    return AsIdentifier(name=name)


def create_as_binary_expression(left: AsExpression,
                               operator: str,
                               right: AsExpression) -> AsBinaryExpression:
    """Create an AssemblyScript binary expression."""
    return AsBinaryExpression(left=left, operator=operator, right=right)


def create_as_call_expression(function: AsExpression,
                            arguments: List[AsExpression] = None) -> AsCallExpression:
    """Create an AssemblyScript call expression."""
    return AsCallExpression(function=function, arguments=arguments or [])


def is_as_builtin_type(type_name: str) -> bool:
    """Check if type is a built-in AssemblyScript type."""
    return type_name in AS_BUILTIN_TYPES


def get_as_numeric_types() -> List[str]:
    """Get all numeric types in AssemblyScript."""
    return ['i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'f32', 'f64', 'isize', 'usize']


def get_as_integer_types() -> List[str]:
    """Get all integer types in AssemblyScript."""
    return ['i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'isize', 'usize']


def get_as_float_types() -> List[str]:
    """Get all floating point types in AssemblyScript."""
    return ['f32', 'f64']


def infer_as_type_from_value(value: Any) -> AsType:
    """Infer AssemblyScript type from a value."""
    if isinstance(value, bool):
        return create_as_type("bool")
    elif isinstance(value, int):
        # Default to i32 for integers
        return create_as_type("i32")
    elif isinstance(value, float):
        # Default to f64 for floats
        return create_as_type("f64")
    elif isinstance(value, str):
        return create_as_type("string")
    elif value is None:
        return create_as_type("void")
    else:
        return create_as_type("unknown")


def as_type_to_string(as_type: AsType) -> str:
    """Convert AsType to string representation."""
    return as_type.full_name


def string_to_as_type(type_str: str) -> AsType:
    """Parse string representation to AsType."""
    # Simplified parsing - handles basic types
    type_str = type_str.strip()
    
    # Handle nullable types
    is_nullable = False
    if " | null" in type_str:
        type_str = type_str.replace(" | null", "")
        is_nullable = True
    
    # Handle array types
    is_array = False
    if type_str.endswith("[]"):
        type_str = type_str[:-2]
        is_array = True
    
    # Handle generic types (simplified)
    generic_args = []
    if "<" in type_str and type_str.endswith(">"):
        base_type = type_str[:type_str.index("<")]
        # Simplified - doesn't handle nested generics properly
        args_str = type_str[type_str.index("<") + 1:-1]
        if args_str:
            generic_args = [string_to_as_type(arg.strip()) for arg in args_str.split(",")]
        type_str = base_type
    
    return AsType(
        name=type_str,
        generic_args=generic_args,
        is_nullable=is_nullable,
        is_array=is_array
    )


def find_as_function_by_name(program: AsProgram, name: str) -> Optional[AsFunction]:
    """Find function by name in program."""
    for stmt in program.statements:
        if isinstance(stmt, AsFunction) and stmt.name == name:
            return stmt
    return None


def find_as_class_by_name(program: AsProgram, name: str) -> Optional[AsClass]:
    """Find class by name in program."""
    for stmt in program.statements:
        if isinstance(stmt, AsClass) and stmt.name == name:
            return stmt
    return None


def get_as_exports(program: AsProgram) -> List[str]:
    """Get all exported names from program."""
    exports = []
    
    # Direct exports
    for export in program.exports:
        if export.declaration:
            if isinstance(export.declaration, (AsFunction, AsClass, AsVariableDeclaration)):
                exports.append(export.declaration.name)
        
        for spec in export.specifiers:
            exports.append(spec.exported or spec.local)
    
    # Exported declarations
    for stmt in program.statements:
        if isinstance(stmt, (AsFunction, AsClass, AsVariableDeclaration)) and stmt.is_export:
            exports.append(stmt.name)
    
    return exports


# Extended visitor for additional functionality
class AsVisitorExtended(AsVisitor):
    """Extended visitor with additional methods."""
    pass