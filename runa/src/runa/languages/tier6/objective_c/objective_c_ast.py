#!/usr/bin/env python3
"""
Objective-C AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Objective-C covering all language features
including message passing syntax, memory management (ARC and manual), protocols,
categories, blocks, Foundation framework integration, and Apple ecosystem constructs.

This module provides complete AST representation for:
- Message passing: [object method:parameter]
- Memory management: ARC, manual retain/release, autorelease pools
- Foundation Framework: NSString, NSArray, NSDictionary, etc.
- Categories and Extensions: class method additions
- Protocols: Interface definitions and conformance
- Property Synthesis: @property, @synthesize, dot notation
- Blocks: Closure-like constructs with capture semantics
- Import system: #import and @import directives
- Preprocessor directives and macros
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class ObjCNodeType(Enum):
    """Objective-C-specific AST node types."""
    # Program structure
    SOURCE_UNIT = auto()
    IMPORT_DIRECTIVE = auto()
    PREPROCESSOR_DIRECTIVE = auto()
    
    # Classes and objects
    INTERFACE_DECLARATION = auto()
    IMPLEMENTATION = auto()
    PROTOCOL_DECLARATION = auto()
    CATEGORY_INTERFACE = auto()
    CATEGORY_IMPLEMENTATION = auto()
    CLASS_EXTENSION = auto()
    
    # Methods and properties
    METHOD_DECLARATION = auto()
    METHOD_IMPLEMENTATION = auto()
    PROPERTY_DECLARATION = auto()
    PROPERTY_SYNTHESIS = auto()
    IVAR_DECLARATION = auto()
    
    # Message passing
    MESSAGE_EXPRESSION = auto()
    SELECTOR = auto()
    KEYWORD_ARGUMENT = auto()
    
    # Blocks and closures
    BLOCK_EXPRESSION = auto()
    BLOCK_DECLARATION = auto()
    BLOCK_TYPE = auto()
    
    # Memory management
    AUTORELEASE_POOL = auto()
    RETAIN_EXPRESSION = auto()
    RELEASE_EXPRESSION = auto()
    AUTORELEASE_EXPRESSION = auto()
    
    # Types and declarations
    INSTANCE_TYPE = auto()
    ID_TYPE = auto()
    CLASS_TYPE = auto()
    PROTOCOL_TYPE = auto()
    POINTER_TYPE = auto()
    
    # Expressions
    SELF_EXPRESSION = auto()
    SUPER_EXPRESSION = auto()
    NIL_EXPRESSION = auto()
    BOOL_LITERAL = auto()
    STRING_LITERAL = auto()
    NUMBER_LITERAL = auto()
    ARRAY_LITERAL = auto()
    DICTIONARY_LITERAL = auto()
    
    # Statements
    SYNCHRONIZED_STATEMENT = auto()
    TRY_CATCH_STATEMENT = auto()
    THROW_STATEMENT = auto()
    
    # Preprocessor and attributes
    PRAGMA_DIRECTIVE = auto()
    ATTRIBUTE = auto()
    AVAILABILITY_ATTRIBUTE = auto()


class ObjCVisibility(Enum):
    """Objective-C visibility modifiers."""
    PUBLIC = "@public"
    PRIVATE = "@private"
    PROTECTED = "@protected"
    PACKAGE = "@package"


class ObjCPropertyAttribute(Enum):
    """Objective-C property attributes."""
    ATOMIC = "atomic"
    NONATOMIC = "nonatomic"
    STRONG = "strong"
    WEAK = "weak"
    COPY = "copy"
    ASSIGN = "assign"
    RETAIN = "retain"
    READONLY = "readonly"
    READWRITE = "readwrite"
    GETTER = "getter"
    SETTER = "setter"


class ObjCMemoryManagement(Enum):
    """Memory management modes."""
    ARC = "arc"
    MANUAL = "manual"
    GARBAGE_COLLECTION = "gc"  # Legacy


class ObjCMethodType(Enum):
    """Method types."""
    INSTANCE = "-"
    CLASS = "+"


@dataclass
class ObjCNode(ASTNode):
    """Base class for all Objective-C AST nodes."""
    objc_node_type: ObjCNodeType = ObjCNodeType.SOURCE_UNIT
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class ObjCSourceUnit(ObjCNode):
    """Objective-C source unit (file)"""
    objc_node_type: ObjCNodeType = ObjCNodeType.SOURCE_UNIT
    imports: List['ObjCImportDirective'] = field(default_factory=list)
    preprocessor_directives: List['ObjCPreprocessorDirective'] = field(default_factory=list)
    interfaces: List['ObjCInterfaceDeclaration'] = field(default_factory=list)
    implementations: List['ObjCImplementation'] = field(default_factory=list)
    protocols: List['ObjCProtocolDeclaration'] = field(default_factory=list)
    categories: List['ObjCCategoryInterface'] = field(default_factory=list)
    category_implementations: List['ObjCCategoryImplementation'] = field(default_factory=list)
    extensions: List['ObjCClassExtension'] = field(default_factory=list)
    functions: List['ObjCFunctionDeclaration'] = field(default_factory=list)
    variables: List['ObjCVariableDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_source_unit(self)


@dataclass
class ObjCImportDirective(ObjCNode):
    """Import directive: #import "Header.h" or @import Foundation;"""
    objc_node_type: ObjCNodeType = ObjCNodeType.IMPORT_DIRECTIVE
    is_framework_import: bool = False  # @import vs #import
    is_system_import: bool = False     # <> vs ""
    path: str = ""
    framework_name: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_objc_import_directive(self)


@dataclass
class ObjCPreprocessorDirective(ObjCNode):
    """Preprocessor directive: #define, #ifdef, etc."""
    objc_node_type: ObjCNodeType = ObjCNodeType.PREPROCESSOR_DIRECTIVE
    directive: str = ""  # define, ifdef, ifndef, endif, etc.
    content: str = ""
    
    def accept(self, visitor):
        return visitor.visit_objc_preprocessor_directive(self)


# ============================================================================
# Classes and Objects
# ============================================================================

@dataclass
class ObjCInterfaceDeclaration(ObjCNode):
    """Interface declaration: @interface MyClass : NSObject <Protocol> { ... }"""
    objc_node_type: ObjCNodeType = ObjCNodeType.INTERFACE_DECLARATION
    name: str = ""
    superclass: Optional[str] = None
    protocols: List[str] = field(default_factory=list)
    instance_variables: List['ObjCIvarDeclaration'] = field(default_factory=list)
    properties: List['ObjCPropertyDeclaration'] = field(default_factory=list)
    methods: List['ObjCMethodDeclaration'] = field(default_factory=list)
    is_forward_declaration: bool = False
    
    def accept(self, visitor):
        return visitor.visit_objc_interface_declaration(self)


@dataclass
class ObjCImplementation(ObjCNode):
    """Implementation: @implementation MyClass { ... } @end"""
    objc_node_type: ObjCNodeType = ObjCNodeType.IMPLEMENTATION
    name: str = ""
    instance_variables: List['ObjCIvarDeclaration'] = field(default_factory=list)
    properties: List['ObjCPropertySynthesis'] = field(default_factory=list)
    methods: List['ObjCMethodImplementation'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_implementation(self)


@dataclass
class ObjCProtocolDeclaration(ObjCNode):
    """Protocol declaration: @protocol MyProtocol <SuperProtocol> ... @end"""
    objc_node_type: ObjCNodeType = ObjCNodeType.PROTOCOL_DECLARATION
    name: str = ""
    protocols: List[str] = field(default_factory=list)  # Super protocols
    properties: List['ObjCPropertyDeclaration'] = field(default_factory=list)
    required_methods: List['ObjCMethodDeclaration'] = field(default_factory=list)
    optional_methods: List['ObjCMethodDeclaration'] = field(default_factory=list)
    is_forward_declaration: bool = False
    
    def accept(self, visitor):
        return visitor.visit_objc_protocol_declaration(self)


@dataclass
class ObjCCategoryInterface(ObjCNode):
    """Category interface: @interface MyClass (CategoryName) ... @end"""
    objc_node_type: ObjCNodeType = ObjCNodeType.CATEGORY_INTERFACE
    class_name: str = ""
    category_name: str = ""
    protocols: List[str] = field(default_factory=list)
    properties: List['ObjCPropertyDeclaration'] = field(default_factory=list)
    methods: List['ObjCMethodDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_category_interface(self)


@dataclass
class ObjCCategoryImplementation(ObjCNode):
    """Category implementation: @implementation MyClass (CategoryName) ... @end"""
    objc_node_type: ObjCNodeType = ObjCNodeType.CATEGORY_IMPLEMENTATION
    class_name: str = ""
    category_name: str = ""
    methods: List['ObjCMethodImplementation'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_category_implementation(self)


@dataclass
class ObjCClassExtension(ObjCNode):
    """Class extension: @interface MyClass () ... @end"""
    objc_node_type: ObjCNodeType = ObjCNodeType.CLASS_EXTENSION
    class_name: str = ""
    instance_variables: List['ObjCIvarDeclaration'] = field(default_factory=list)
    properties: List['ObjCPropertyDeclaration'] = field(default_factory=list)
    methods: List['ObjCMethodDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_class_extension(self)


# ============================================================================
# Methods and Properties
# ============================================================================

@dataclass
class ObjCMethodDeclaration(ObjCNode):
    """Method declaration: - (void)doSomething:(NSString *)param withFlag:(BOOL)flag;"""
    objc_node_type: ObjCNodeType = ObjCNodeType.METHOD_DECLARATION
    method_type: ObjCMethodType = ObjCMethodType.INSTANCE
    return_type: 'ObjCType' = None
    selector: 'ObjCSelector' = None
    parameters: List['ObjCParameter'] = field(default_factory=list)
    is_variadic: bool = False
    attributes: List['ObjCAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_method_declaration(self)


@dataclass
class ObjCMethodImplementation(ObjCNode):
    """Method implementation: - (void)doSomething:(NSString *)param { ... }"""
    objc_node_type: ObjCNodeType = ObjCNodeType.METHOD_IMPLEMENTATION
    method_type: ObjCMethodType = ObjCMethodType.INSTANCE
    return_type: 'ObjCType' = None
    selector: 'ObjCSelector' = None
    parameters: List['ObjCParameter'] = field(default_factory=list)
    body: List['ObjCStatement'] = field(default_factory=list)
    is_variadic: bool = False
    attributes: List['ObjCAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_method_implementation(self)


@dataclass
class ObjCSelector(ObjCNode):
    """Method selector: doSomething:withFlag:"""
    objc_node_type: ObjCNodeType = ObjCNodeType.SELECTOR
    parts: List[str] = field(default_factory=list)  # ["doSomething", "withFlag"]
    
    def get_selector_string(self) -> str:
        """Get the full selector string."""
        if not self.parts:
            return ""
        if len(self.parts) == 1 and not self.parts[0].endswith(':'):
            return self.parts[0]
        return ':'.join(self.parts) + ':'
    
    def accept(self, visitor):
        return visitor.visit_objc_selector(self)


@dataclass
class ObjCParameter(ObjCNode):
    """Method parameter: (NSString *)param"""
    type_annotation: 'ObjCType' = None
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_objc_parameter(self)


@dataclass
class ObjCPropertyDeclaration(ObjCNode):
    """Property declaration: @property (nonatomic, strong) NSString *name;"""
    objc_node_type: ObjCNodeType = ObjCNodeType.PROPERTY_DECLARATION
    type_annotation: 'ObjCType' = None
    name: str = ""
    attributes: List[ObjCPropertyAttribute] = field(default_factory=list)
    getter_name: Optional[str] = None
    setter_name: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_objc_property_declaration(self)


@dataclass
class ObjCPropertySynthesis(ObjCNode):
    """Property synthesis: @synthesize name = _name;"""
    objc_node_type: ObjCNodeType = ObjCNodeType.PROPERTY_SYNTHESIS
    property_name: str = ""
    ivar_name: Optional[str] = None  # If None, uses _propertyName
    is_dynamic: bool = False  # @dynamic vs @synthesize
    
    def accept(self, visitor):
        return visitor.visit_objc_property_synthesis(self)


@dataclass
class ObjCIvarDeclaration(ObjCNode):
    """Instance variable declaration: NSString *_name;"""
    objc_node_type: ObjCNodeType = ObjCNodeType.IVAR_DECLARATION
    type_annotation: 'ObjCType' = None
    name: str = ""
    visibility: ObjCVisibility = ObjCVisibility.PRIVATE
    initial_value: Optional['ObjCExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_objc_ivar_declaration(self)


# ============================================================================
# Message Passing and Expressions
# ============================================================================

@dataclass
class ObjCMessageExpression(ObjCNode):
    """Message expression: [object method:param withFlag:YES]"""
    objc_node_type: ObjCNodeType = ObjCNodeType.MESSAGE_EXPRESSION
    receiver: 'ObjCExpression' = None
    selector: ObjCSelector = None
    arguments: List['ObjCKeywordArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_message_expression(self)


@dataclass
class ObjCKeywordArgument(ObjCNode):
    """Keyword argument in message: withFlag:YES"""
    objc_node_type: ObjCNodeType = ObjCNodeType.KEYWORD_ARGUMENT
    keyword: str = ""  # "withFlag"
    expression: 'ObjCExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_objc_keyword_argument(self)


# ============================================================================
# Blocks and Closures
# ============================================================================

@dataclass
class ObjCBlockExpression(ObjCNode):
    """Block expression: ^(NSString *str) { return str.length; }"""
    objc_node_type: ObjCNodeType = ObjCNodeType.BLOCK_EXPRESSION
    parameters: List[ObjCParameter] = field(default_factory=list)
    return_type: Optional['ObjCType'] = None
    body: List['ObjCStatement'] = field(default_factory=list)
    captured_variables: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_block_expression(self)


@dataclass
class ObjCBlockDeclaration(ObjCNode):
    """Block variable declaration: void (^myBlock)(NSString *);"""
    objc_node_type: ObjCNodeType = ObjCNodeType.BLOCK_DECLARATION
    name: str = ""
    block_type: 'ObjCBlockType' = None
    initial_value: Optional[ObjCBlockExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_objc_block_declaration(self)


@dataclass
class ObjCBlockType(ObjCNode):
    """Block type: void (^)(NSString *)"""
    objc_node_type: ObjCNodeType = ObjCNodeType.BLOCK_TYPE
    return_type: 'ObjCType' = None
    parameter_types: List['ObjCType'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_block_type(self)


# ============================================================================
# Memory Management
# ============================================================================

@dataclass
class ObjCAutoreleasePool(ObjCNode):
    """Autorelease pool: @autoreleasepool { ... }"""
    objc_node_type: ObjCNodeType = ObjCNodeType.AUTORELEASE_POOL
    body: List['ObjCStatement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_autorelease_pool(self)


@dataclass
class ObjCRetainExpression(ObjCNode):
    """Retain expression: [object retain]"""
    objc_node_type: ObjCNodeType = ObjCNodeType.RETAIN_EXPRESSION
    expression: 'ObjCExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_objc_retain_expression(self)


@dataclass
class ObjCReleaseExpression(ObjCNode):
    """Release expression: [object release]"""
    objc_node_type: ObjCNodeType = ObjCNodeType.RELEASE_EXPRESSION
    expression: 'ObjCExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_objc_release_expression(self)


@dataclass
class ObjCAutoreleaseExpression(ObjCNode):
    """Autorelease expression: [object autorelease]"""
    objc_node_type: ObjCNodeType = ObjCNodeType.AUTORELEASE_EXPRESSION
    expression: 'ObjCExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_objc_autorelease_expression(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class ObjCType(ObjCNode):
    """Base class for Objective-C types."""
    pass


@dataclass
class ObjCInstanceType(ObjCType):
    """instancetype keyword"""
    objc_node_type: ObjCNodeType = ObjCNodeType.INSTANCE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_objc_instance_type(self)


@dataclass
class ObjCIdType(ObjCType):
    """id type"""
    objc_node_type: ObjCNodeType = ObjCNodeType.ID_TYPE
    protocols: List[str] = field(default_factory=list)  # id<Protocol>
    
    def accept(self, visitor):
        return visitor.visit_objc_id_type(self)


@dataclass
class ObjCClassType(ObjCType):
    """Class type"""
    objc_node_type: ObjCNodeType = ObjCNodeType.CLASS_TYPE
    class_name: str = ""
    protocols: List[str] = field(default_factory=list)  # ClassName<Protocol>
    
    def accept(self, visitor):
        return visitor.visit_objc_class_type(self)


@dataclass
class ObjCPointerType(ObjCType):
    """Pointer type: NSString *"""
    objc_node_type: ObjCNodeType = ObjCNodeType.POINTER_TYPE
    pointed_type: ObjCType = None
    is_const: bool = False
    
    def accept(self, visitor):
        return visitor.visit_objc_pointer_type(self)


@dataclass
class ObjCProtocolType(ObjCType):
    """Protocol type: id<MyProtocol>"""
    objc_node_type: ObjCNodeType = ObjCNodeType.PROTOCOL_TYPE
    protocol_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_objc_protocol_type(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class ObjCExpression(ObjCNode):
    """Base class for expressions."""
    pass


@dataclass
class ObjCSelfExpression(ObjCExpression):
    """self keyword"""
    objc_node_type: ObjCNodeType = ObjCNodeType.SELF_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_objc_self_expression(self)


@dataclass
class ObjCSuperExpression(ObjCExpression):
    """super keyword"""
    objc_node_type: ObjCNodeType = ObjCNodeType.SUPER_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_objc_super_expression(self)


@dataclass
class ObjCNilExpression(ObjCExpression):
    """nil keyword"""
    objc_node_type: ObjCNodeType = ObjCNodeType.NIL_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_objc_nil_expression(self)


@dataclass
class ObjCBoolLiteral(ObjCExpression):
    """Boolean literal: YES, NO"""
    objc_node_type: ObjCNodeType = ObjCNodeType.BOOL_LITERAL
    value: bool = False
    
    def accept(self, visitor):
        return visitor.visit_objc_bool_literal(self)


@dataclass
class ObjCStringLiteral(ObjCExpression):
    """String literal: @"Hello, World!" """
    objc_node_type: ObjCNodeType = ObjCNodeType.STRING_LITERAL
    value: str = ""
    is_nsstring: bool = True  # @"" vs regular C string
    
    def accept(self, visitor):
        return visitor.visit_objc_string_literal(self)


@dataclass
class ObjCNumberLiteral(ObjCExpression):
    """Number literal: @42, @3.14, @YES"""
    objc_node_type: ObjCNodeType = ObjCNodeType.NUMBER_LITERAL
    value: Union[int, float, bool] = 0
    is_nsnumber: bool = True  # @ prefix
    
    def accept(self, visitor):
        return visitor.visit_objc_number_literal(self)


@dataclass
class ObjCArrayLiteral(ObjCExpression):
    """Array literal: @[@"item1", @"item2"]"""
    objc_node_type: ObjCNodeType = ObjCNodeType.ARRAY_LITERAL
    elements: List[ObjCExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_array_literal(self)


@dataclass
class ObjCDictionaryLiteral(ObjCExpression):
    """Dictionary literal: @{@"key": @"value"}"""
    objc_node_type: ObjCNodeType = ObjCNodeType.DICTIONARY_LITERAL
    keys: List[ObjCExpression] = field(default_factory=list)
    values: List[ObjCExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_dictionary_literal(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class ObjCStatement(ObjCNode):
    """Base class for statements."""
    pass


@dataclass
class ObjCSynchronizedStatement(ObjCStatement):
    """Synchronized statement: @synchronized(object) { ... }"""
    objc_node_type: ObjCNodeType = ObjCNodeType.SYNCHRONIZED_STATEMENT
    expression: ObjCExpression = None
    body: List[ObjCStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_synchronized_statement(self)


@dataclass
class ObjCTryCatchStatement(ObjCStatement):
    """Try-catch statement: @try { ... } @catch(NSException *e) { ... } @finally { ... }"""
    objc_node_type: ObjCNodeType = ObjCNodeType.TRY_CATCH_STATEMENT
    try_body: List[ObjCStatement] = field(default_factory=list)
    catch_clauses: List['ObjCCatchClause'] = field(default_factory=list)
    finally_body: List[ObjCStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_try_catch_statement(self)


@dataclass
class ObjCCatchClause(ObjCNode):
    """Catch clause: @catch(NSException *e) { ... }"""
    exception_type: ObjCType = None
    exception_name: str = ""
    body: List[ObjCStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_catch_clause(self)


@dataclass
class ObjCThrowStatement(ObjCStatement):
    """Throw statement: @throw exception;"""
    objc_node_type: ObjCNodeType = ObjCNodeType.THROW_STATEMENT
    expression: ObjCExpression = None
    
    def accept(self, visitor):
        return visitor.visit_objc_throw_statement(self)


# ============================================================================
# Attributes and Preprocessor
# ============================================================================

@dataclass
class ObjCAttribute(ObjCNode):
    """Attribute: __attribute__((deprecated))"""
    objc_node_type: ObjCNodeType = ObjCNodeType.ATTRIBUTE
    name: str = ""
    arguments: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_objc_attribute(self)


@dataclass
class ObjCAvailabilityAttribute(ObjCNode):
    """Availability attribute: API_AVAILABLE(ios(10.0))"""
    objc_node_type: ObjCNodeType = ObjCNodeType.AVAILABILITY_ATTRIBUTE
    platform: str = ""  # ios, macos, watchos, tvos
    introduced: str = ""
    deprecated: str = ""
    obsoleted: str = ""
    message: str = ""
    
    def accept(self, visitor):
        return visitor.visit_objc_availability_attribute(self)


@dataclass
class ObjCPragmaDirective(ObjCNode):
    """Pragma directive: #pragma mark - Public Methods"""
    objc_node_type: ObjCNodeType = ObjCNodeType.PRAGMA_DIRECTIVE
    directive: str = ""
    content: str = ""
    
    def accept(self, visitor):
        return visitor.visit_objc_pragma_directive(self)


# ============================================================================
# Convenience Factory Functions
# ============================================================================

def create_objc_interface(name: str, superclass: str = None) -> ObjCInterfaceDeclaration:
    """Create an Objective-C interface declaration."""
    return ObjCInterfaceDeclaration(name=name, superclass=superclass)


def create_objc_implementation(name: str) -> ObjCImplementation:
    """Create an Objective-C implementation."""
    return ObjCImplementation(name=name)


def create_objc_protocol(name: str) -> ObjCProtocolDeclaration:
    """Create an Objective-C protocol declaration."""
    return ObjCProtocolDeclaration(name=name)


def create_objc_property(name: str, type_annotation: ObjCType, 
                        attributes: List[ObjCPropertyAttribute] = None) -> ObjCPropertyDeclaration:
    """Create an Objective-C property declaration."""
    return ObjCPropertyDeclaration(
        name=name, 
        type_annotation=type_annotation,
        attributes=attributes or []
    )


def create_objc_method_declaration(method_type: ObjCMethodType, selector: ObjCSelector,
                                 return_type: ObjCType = None,
                                 parameters: List[ObjCParameter] = None) -> ObjCMethodDeclaration:
    """Create an Objective-C method declaration."""
    return ObjCMethodDeclaration(
        method_type=method_type,
        selector=selector,
        return_type=return_type,
        parameters=parameters or []
    )


def create_objc_message_send(receiver: ObjCExpression, selector: ObjCSelector,
                           arguments: List[ObjCKeywordArgument] = None) -> ObjCMessageExpression:
    """Create an Objective-C message expression."""
    return ObjCMessageExpression(
        receiver=receiver,
        selector=selector,
        arguments=arguments or []
    )


def create_objc_block(parameters: List[ObjCParameter] = None,
                     return_type: ObjCType = None,
                     body: List[ObjCStatement] = None) -> ObjCBlockExpression:
    """Create an Objective-C block expression."""
    return ObjCBlockExpression(
        parameters=parameters or [],
        return_type=return_type,
        body=body or []
    )


def create_objc_nsstring_literal(value: str) -> ObjCStringLiteral:
    """Create an NSString literal."""
    return ObjCStringLiteral(value=value, is_nsstring=True)


def create_objc_nsnumber_literal(value: Union[int, float, bool]) -> ObjCNumberLiteral:
    """Create an NSNumber literal."""
    return ObjCNumberLiteral(value=value, is_nsnumber=True)


def create_objc_nsarray_literal(elements: List[ObjCExpression] = None) -> ObjCArrayLiteral:
    """Create an NSArray literal."""
    return ObjCArrayLiteral(elements=elements or []) 