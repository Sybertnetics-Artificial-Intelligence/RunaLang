"""
Ada AST (Abstract Syntax Tree) Implementation for Runa Universal Translation Platform

This module provides comprehensive AST node definitions for the Ada programming language,
supporting Ada 2012 standard with safety-critical, real-time, and embedded system features.

Ada is designed for safety-critical applications in defense, aerospace, transportation,
and industrial control systems where reliability and correctness are paramount.

Key Ada Features Supported:
- Strong static typing with subtype constraints
- Package system with specification and body separation
- Generic programming with formal parameters
- Tasking (concurrency) with protected objects and synchronization
- Exception handling with contract-based programming
- Representation clauses for low-level system programming
- Pragma directives for compiler control
- Attribute references and user-defined attributes
- Access types (pointers) with safety checks
- Variant records and discriminated types
- Real-time and embedded system constructs

Safety-Critical Features:
- SPARK subset for formal verification
- Ravenscar profile for deterministic real-time systems
- High Integrity restrictions
- Contract-based programming (preconditions, postconditions)
- Static analysis support
- Memory management without garbage collection
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum
import uuid

from ...core.ast_base import ASTNode

class AdaNodeType(Enum):
    """Ada-specific AST node types"""
    # Compilation units
    COMPILATION_UNIT = "compilation_unit"
    PACKAGE_SPECIFICATION = "package_specification"
    PACKAGE_BODY = "package_body"
    SUBPROGRAM_SPECIFICATION = "subprogram_specification"
    SUBPROGRAM_BODY = "subprogram_body"
    GENERIC_PACKAGE = "generic_package"
    GENERIC_SUBPROGRAM = "generic_subprogram"
    PACKAGE_INSTANTIATION = "package_instantiation"
    
    # Declarations
    TYPE_DECLARATION = "type_declaration"
    SUBTYPE_DECLARATION = "subtype_declaration"
    OBJECT_DECLARATION = "object_declaration"
    CONSTANT_DECLARATION = "constant_declaration"
    EXCEPTION_DECLARATION = "exception_declaration"
    RENAMING_DECLARATION = "renaming_declaration"
    USE_CLAUSE = "use_clause"
    WITH_CLAUSE = "with_clause"
    
    # Type definitions
    SCALAR_TYPE = "scalar_type"
    ARRAY_TYPE = "array_type"
    RECORD_TYPE = "record_type"
    ACCESS_TYPE = "access_type"
    ENUMERATION_TYPE = "enumeration_type"
    INTEGER_TYPE = "integer_type"
    REAL_TYPE = "real_type"
    PRIVATE_TYPE = "private_type"
    TAGGED_TYPE = "tagged_type"
    PROTECTED_TYPE = "protected_type"
    TASK_TYPE = "task_type"
    
    # Statements
    ASSIGNMENT_STATEMENT = "assignment_statement"
    PROCEDURE_CALL = "procedure_call"
    IF_STATEMENT = "if_statement"
    CASE_STATEMENT = "case_statement"
    LOOP_STATEMENT = "loop_statement"
    FOR_LOOP = "for_loop"
    WHILE_LOOP = "while_loop"
    EXIT_STATEMENT = "exit_statement"
    RETURN_STATEMENT = "return_statement"
    RAISE_STATEMENT = "raise_statement"
    NULL_STATEMENT = "null_statement"
    
    # Expressions
    FUNCTION_CALL = "function_call"
    ATTRIBUTE_REFERENCE = "attribute_reference"
    QUALIFIED_EXPRESSION = "qualified_expression"
    TYPE_CONVERSION = "type_conversion"
    ALLOCATOR = "allocator"
    AGGREGATE = "aggregate"
    
    # Tasking and concurrency
    TASK_SPECIFICATION = "task_specification"
    TASK_BODY = "task_body"
    PROTECTED_SPECIFICATION = "protected_specification"
    PROTECTED_BODY = "protected_body"
    ACCEPT_STATEMENT = "accept_statement"
    SELECT_STATEMENT = "select_statement"
    ENTRY_DECLARATION = "entry_declaration"
    ENTRY_CALL = "entry_call"
    
    # Exception handling
    EXCEPTION_HANDLER = "exception_handler"
    EXCEPTION_CHOICE = "exception_choice"
    
    # Representation and pragmas
    REPRESENTATION_CLAUSE = "representation_clause"
    PRAGMA = "pragma"
    ASPECT_SPECIFICATION = "aspect_specification"
    
    # Contracts and SPARK
    PRECONDITION = "precondition"
    POSTCONDITION = "postcondition"
    CONTRACT_CASE = "contract_case"
    GHOST_DECLARATION = "ghost_declaration"
    
    # Literals and identifiers
    NUMERIC_LITERAL = "numeric_literal"
    STRING_LITERAL = "string_literal"
    CHARACTER_LITERAL = "character_literal"
    IDENTIFIER = "identifier"
    OPERATOR_SYMBOL = "operator_symbol"

@dataclass
class AdaNode(ASTNode):
    """Base class for all Ada AST nodes"""
    node_type: AdaNodeType
    source_location: Optional[Dict[str, int]] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if self.node_id is None:
            self.node_id = str(uuid.uuid4())

@dataclass 
class AdaCompilationUnit(AdaNode):
    """Ada compilation unit (top-level program unit)"""
    context_clauses: List['AdaContextClause'] = field(default_factory=list)
    unit: 'AdaLibraryUnit'
    pragmas: List['AdaPragma'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.COMPILATION_UNIT

@dataclass
class AdaContextClause(AdaNode):
    """Context clause (with/use clauses)"""
    clause_type: str  # "with" or "use"
    library_units: List[str]
    is_private: bool = False
    is_limited: bool = False

@dataclass
class AdaWithClause(AdaContextClause):
    """With clause for importing library units"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.WITH_CLAUSE
        self.clause_type = "with"

@dataclass
class AdaUseClause(AdaContextClause):
    """Use clause for making names directly visible"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.USE_CLAUSE
        self.clause_type = "use"

@dataclass
class AdaLibraryUnit(AdaNode):
    """Base for library units (packages, subprograms)"""
    name: str
    is_private: bool = False

@dataclass
class AdaPackageSpecification(AdaLibraryUnit):
    """Ada package specification"""
    declarations: List['AdaDeclaration'] = field(default_factory=list)
    private_declarations: List['AdaDeclaration'] = field(default_factory=list)
    aspects: List['AdaAspectSpecification'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PACKAGE_SPECIFICATION

@dataclass
class AdaPackageBody(AdaLibraryUnit):
    """Ada package body"""
    declarations: List['AdaDeclaration'] = field(default_factory=list)
    statements: List['AdaStatement'] = field(default_factory=list)
    exception_handlers: List['AdaExceptionHandler'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PACKAGE_BODY

@dataclass
class AdaSubprogramSpecification(AdaLibraryUnit):
    """Ada subprogram specification (procedure/function)"""
    subprogram_kind: str  # "procedure" or "function"
    parameters: List['AdaParameterDeclaration'] = field(default_factory=list)
    return_type: Optional['AdaTypeReference'] = None
    aspects: List['AdaAspectSpecification'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.SUBPROGRAM_SPECIFICATION

@dataclass
class AdaSubprogramBody(AdaLibraryUnit):
    """Ada subprogram body"""
    specification: AdaSubprogramSpecification
    declarations: List['AdaDeclaration'] = field(default_factory=list)
    statements: List['AdaStatement'] = field(default_factory=list)
    exception_handlers: List['AdaExceptionHandler'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.SUBPROGRAM_BODY

@dataclass
class AdaGenericPackage(AdaLibraryUnit):
    """Generic package with formal parameters"""
    formal_parameters: List['AdaGenericFormalParameter'] = field(default_factory=list)
    package_specification: AdaPackageSpecification
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.GENERIC_PACKAGE

@dataclass
class AdaGenericSubprogram(AdaLibraryUnit):
    """Generic subprogram with formal parameters"""
    formal_parameters: List['AdaGenericFormalParameter'] = field(default_factory=list)
    subprogram_specification: AdaSubprogramSpecification
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.GENERIC_SUBPROGRAM

@dataclass
class AdaGenericFormalParameter(AdaNode):
    """Formal parameter in generic unit"""
    parameter_kind: str  # "type", "subprogram", "package", "object"
    name: str
    parameter_type: Optional['AdaTypeReference'] = None
    default_value: Optional['AdaExpression'] = None

@dataclass
class AdaPackageInstantiation(AdaLibraryUnit):
    """Instantiation of generic package"""
    generic_unit_name: str
    actual_parameters: List['AdaExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PACKAGE_INSTANTIATION

@dataclass
class AdaDeclaration(AdaNode):
    """Base class for all declarations"""
    name: str
    is_aliased: bool = False

@dataclass
class AdaTypeDeclaration(AdaDeclaration):
    """Type declaration"""
    type_definition: 'AdaTypeDefinition'
    discriminants: List['AdaDiscriminantSpecification'] = field(default_factory=list)
    aspects: List['AdaAspectSpecification'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.TYPE_DECLARATION

@dataclass
class AdaSubtypeDeclaration(AdaDeclaration):
    """Subtype declaration with constraints"""
    parent_type: 'AdaTypeReference'
    constraint: Optional['AdaConstraint'] = None
    aspects: List['AdaAspectSpecification'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.SUBTYPE_DECLARATION

@dataclass
class AdaObjectDeclaration(AdaDeclaration):
    """Object (variable) declaration"""
    object_type: 'AdaTypeReference'
    initial_value: Optional['AdaExpression'] = None
    is_constant: bool = False
    aspects: List['AdaAspectSpecification'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.OBJECT_DECLARATION

@dataclass
class AdaParameterDeclaration(AdaDeclaration):
    """Subprogram parameter declaration"""
    parameter_mode: str  # "in", "out", "in out"
    parameter_type: 'AdaTypeReference'
    default_value: Optional['AdaExpression'] = None

@dataclass
class AdaExceptionDeclaration(AdaDeclaration):
    """Exception declaration"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.EXCEPTION_DECLARATION

@dataclass
class AdaRenamingDeclaration(AdaDeclaration):
    """Renaming declaration"""
    renamed_entity: str
    entity_type: Optional['AdaTypeReference'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.RENAMING_DECLARATION

@dataclass
class AdaTypeDefinition(AdaNode):
    """Base class for type definitions"""
    pass

@dataclass
class AdaScalarType(AdaTypeDefinition):
    """Scalar type definition"""
    scalar_kind: str  # "integer", "real", "enumeration", "access"
    range_constraint: Optional['AdaRangeConstraint'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.SCALAR_TYPE

@dataclass
class AdaEnumerationType(AdaTypeDefinition):
    """Enumeration type definition"""
    literals: List[str]
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ENUMERATION_TYPE

@dataclass
class AdaIntegerType(AdaTypeDefinition):
    """Integer type definition"""
    range_constraint: 'AdaRangeConstraint'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.INTEGER_TYPE

@dataclass
class AdaRealType(AdaTypeDefinition):
    """Real (floating-point or fixed-point) type definition"""
    real_kind: str  # "floating" or "fixed"
    digits_constraint: Optional[int] = None
    range_constraint: Optional['AdaRangeConstraint'] = None
    delta_constraint: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.REAL_TYPE

@dataclass
class AdaArrayType(AdaTypeDefinition):
    """Array type definition"""
    index_types: List['AdaTypeReference']
    component_type: 'AdaTypeReference'
    is_unconstrained: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ARRAY_TYPE

@dataclass
class AdaRecordType(AdaTypeDefinition):
    """Record type definition"""
    components: List['AdaComponentDeclaration']
    variant_part: Optional['AdaVariantPart'] = None
    is_tagged: bool = False
    is_abstract: bool = False
    is_limited: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.RECORD_TYPE

@dataclass
class AdaComponentDeclaration(AdaDeclaration):
    """Record component declaration"""
    component_type: 'AdaTypeReference'
    default_value: Optional['AdaExpression'] = None

@dataclass
class AdaVariantPart(AdaNode):
    """Variant part of record type"""
    discriminant: str
    variants: List['AdaVariant']

@dataclass
class AdaVariant(AdaNode):
    """Single variant in variant part"""
    choices: List['AdaExpression']
    components: List[AdaComponentDeclaration]

@dataclass
class AdaAccessType(AdaTypeDefinition):
    """Access (pointer) type definition"""
    designated_type: 'AdaTypeReference'
    is_access_to_subprogram: bool = False
    is_access_to_constant: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ACCESS_TYPE

@dataclass
class AdaPrivateType(AdaTypeDefinition):
    """Private type definition"""
    is_tagged: bool = False
    is_limited: bool = False
    discriminants: List['AdaDiscriminantSpecification'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PRIVATE_TYPE

@dataclass
class AdaTaggedType(AdaTypeDefinition):
    """Tagged type definition (for OOP)"""
    parent_type: Optional['AdaTypeReference'] = None
    is_abstract: bool = False
    is_limited: bool = False
    record_definition: Optional[AdaRecordType] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.TAGGED_TYPE

@dataclass
class AdaProtectedType(AdaTypeDefinition):
    """Protected type definition (for synchronization)"""
    discriminants: List['AdaDiscriminantSpecification'] = field(default_factory=list)
    visible_declarations: List[AdaDeclaration] = field(default_factory=list)
    private_declarations: List[AdaDeclaration] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PROTECTED_TYPE

@dataclass
class AdaTaskType(AdaTypeDefinition):
    """Task type definition (for concurrency)"""
    discriminants: List['AdaDiscriminantSpecification'] = field(default_factory=list)
    entries: List['AdaEntryDeclaration'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.TASK_TYPE

@dataclass
class AdaDiscriminantSpecification(AdaNode):
    """Discriminant specification for discriminated types"""
    names: List[str]
    discriminant_type: 'AdaTypeReference'
    default_value: Optional['AdaExpression'] = None

@dataclass
class AdaConstraint(AdaNode):
    """Base class for constraints"""
    pass

@dataclass
class AdaRangeConstraint(AdaConstraint):
    """Range constraint for scalar types"""
    low_bound: 'AdaExpression'
    high_bound: 'AdaExpression'

@dataclass
class AdaIndexConstraint(AdaConstraint):
    """Index constraint for array types"""
    ranges: List[AdaRangeConstraint]

@dataclass
class AdaDiscriminantConstraint(AdaConstraint):
    """Discriminant constraint"""
    discriminant_associations: List['AdaDiscriminantAssociation']

@dataclass
class AdaDiscriminantAssociation(AdaNode):
    """Association in discriminant constraint"""
    discriminant_name: Optional[str] = None
    value: 'AdaExpression' = None

@dataclass
class AdaStatement(AdaNode):
    """Base class for all statements"""
    label: Optional[str] = None

@dataclass
class AdaAssignmentStatement(AdaStatement):
    """Assignment statement"""
    target: 'AdaExpression'
    value: 'AdaExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ASSIGNMENT_STATEMENT

@dataclass
class AdaProcedureCall(AdaStatement):
    """Procedure call statement"""
    procedure_name: str
    parameters: List['AdaParameterAssociation'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PROCEDURE_CALL

@dataclass
class AdaIfStatement(AdaStatement):
    """If statement with elsif and else parts"""
    condition: 'AdaExpression'
    then_statements: List[AdaStatement] = field(default_factory=list)
    elsif_parts: List['AdaElsifPart'] = field(default_factory=list)
    else_statements: List[AdaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.IF_STATEMENT

@dataclass
class AdaElsifPart(AdaNode):
    """Elsif part of if statement"""
    condition: 'AdaExpression'
    statements: List[AdaStatement] = field(default_factory=list)

@dataclass
class AdaCaseStatement(AdaStatement):
    """Case statement"""
    expression: 'AdaExpression'
    alternatives: List['AdaCaseAlternative'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.CASE_STATEMENT

@dataclass
class AdaCaseAlternative(AdaNode):
    """Case alternative"""
    choices: List['AdaExpression']  # Can include ranges
    statements: List[AdaStatement] = field(default_factory=list)

@dataclass
class AdaLoopStatement(AdaStatement):
    """Basic loop statement"""
    statements: List[AdaStatement] = field(default_factory=list)
    iteration_scheme: Optional['AdaIterationScheme'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.LOOP_STATEMENT

@dataclass
class AdaIterationScheme(AdaNode):
    """Iteration scheme for loops"""
    scheme_type: str  # "while", "for"

@dataclass
class AdaWhileLoop(AdaLoopStatement):
    """While loop statement"""
    condition: 'AdaExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.WHILE_LOOP

@dataclass
class AdaForLoop(AdaLoopStatement):
    """For loop statement"""
    loop_parameter: str
    discrete_range: 'AdaDiscreteRange'
    reverse: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.FOR_LOOP

@dataclass
class AdaDiscreteRange(AdaNode):
    """Discrete range for for loops"""
    range_type: str  # "range", "subtype"
    low_bound: Optional['AdaExpression'] = None
    high_bound: Optional['AdaExpression'] = None
    subtype_name: Optional[str] = None

@dataclass
class AdaExitStatement(AdaStatement):
    """Exit statement"""
    loop_name: Optional[str] = None
    condition: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.EXIT_STATEMENT

@dataclass
class AdaReturnStatement(AdaStatement):
    """Return statement"""
    return_value: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.RETURN_STATEMENT

@dataclass
class AdaRaiseStatement(AdaStatement):
    """Raise statement"""
    exception_name: Optional[str] = None
    message: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.RAISE_STATEMENT

@dataclass
class AdaNullStatement(AdaStatement):
    """Null statement"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.NULL_STATEMENT

@dataclass
class AdaExpression(AdaNode):
    """Base class for all expressions"""
    expression_type: Optional['AdaTypeReference'] = None

@dataclass
class AdaFunctionCall(AdaExpression):
    """Function call expression"""
    function_name: str
    parameters: List['AdaParameterAssociation'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.FUNCTION_CALL

@dataclass
class AdaParameterAssociation(AdaNode):
    """Parameter association in subprogram calls"""
    formal_parameter: Optional[str] = None  # None for positional
    actual_parameter: 'AdaExpression' = None

@dataclass
class AdaAttributeReference(AdaExpression):
    """Attribute reference (e.g., X'First, Y'Length)"""
    prefix: 'AdaExpression'
    attribute_name: str
    arguments: List['AdaExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ATTRIBUTE_REFERENCE

@dataclass
class AdaQualifiedExpression(AdaExpression):
    """Qualified expression with explicit type"""
    type_name: 'AdaTypeReference'
    expression: 'AdaExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.QUALIFIED_EXPRESSION

@dataclass
class AdaTypeConversion(AdaExpression):
    """Type conversion expression"""
    target_type: 'AdaTypeReference'
    expression: 'AdaExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.TYPE_CONVERSION

@dataclass
class AdaAllocator(AdaExpression):
    """Allocator expression (new)"""
    allocated_type: 'AdaTypeReference'
    initial_value: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ALLOCATOR

@dataclass
class AdaAggregate(AdaExpression):
    """Aggregate expression"""
    associations: List['AdaComponentAssociation'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.AGGREGATE

@dataclass
class AdaComponentAssociation(AdaNode):
    """Component association in aggregate"""
    choices: List['AdaExpression'] = field(default_factory=list)  # Empty for positional
    expression: 'AdaExpression' = None

@dataclass
class AdaLiteral(AdaExpression):
    """Base class for literals"""
    value: Any

@dataclass
class AdaNumericLiteral(AdaLiteral):
    """Numeric literal (integer or real)"""
    numeric_type: str  # "integer", "real"
    base: int = 10
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.NUMERIC_LITERAL

@dataclass
class AdaStringLiteral(AdaLiteral):
    """String literal"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.STRING_LITERAL

@dataclass
class AdaCharacterLiteral(AdaLiteral):
    """Character literal"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.CHARACTER_LITERAL

@dataclass
class AdaIdentifier(AdaExpression):
    """Identifier expression"""
    name: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.IDENTIFIER

@dataclass
class AdaOperatorSymbol(AdaExpression):
    """Operator symbol"""
    symbol: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.OPERATOR_SYMBOL

@dataclass
class AdaTypeReference(AdaNode):
    """Reference to a type"""
    type_name: str
    package_name: Optional[str] = None

# Tasking and concurrency constructs

@dataclass
class AdaTaskSpecification(AdaDeclaration):
    """Task specification"""
    discriminants: List[AdaDiscriminantSpecification] = field(default_factory=list)
    entries: List['AdaEntryDeclaration'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.TASK_SPECIFICATION

@dataclass
class AdaTaskBody(AdaDeclaration):
    """Task body"""
    declarations: List[AdaDeclaration] = field(default_factory=list)
    statements: List[AdaStatement] = field(default_factory=list)
    exception_handlers: List['AdaExceptionHandler'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.TASK_BODY

@dataclass
class AdaProtectedSpecification(AdaDeclaration):
    """Protected object specification"""
    discriminants: List[AdaDiscriminantSpecification] = field(default_factory=list)
    visible_declarations: List[AdaDeclaration] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PROTECTED_SPECIFICATION

@dataclass
class AdaProtectedBody(AdaDeclaration):
    """Protected object body"""
    declarations: List[AdaDeclaration] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PROTECTED_BODY

@dataclass
class AdaEntryDeclaration(AdaDeclaration):
    """Entry declaration for tasks and protected objects"""
    parameters: List[AdaParameterDeclaration] = field(default_factory=list)
    family_index: Optional['AdaDiscreteRange'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ENTRY_DECLARATION

@dataclass
class AdaAcceptStatement(AdaStatement):
    """Accept statement in task body"""
    entry_name: str
    formal_parameters: List[AdaParameterDeclaration] = field(default_factory=list)
    statements: List[AdaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ACCEPT_STATEMENT

@dataclass
class AdaSelectStatement(AdaStatement):
    """Select statement for concurrent operations"""
    alternatives: List['AdaSelectAlternative'] = field(default_factory=list)
    else_part: List[AdaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.SELECT_STATEMENT

@dataclass
class AdaSelectAlternative(AdaNode):
    """Alternative in select statement"""
    guard: Optional['AdaExpression'] = None
    statements: List[AdaStatement] = field(default_factory=list)

@dataclass
class AdaEntryCall(AdaStatement):
    """Entry call statement"""
    entry_name: str
    parameters: List[AdaParameterAssociation] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ENTRY_CALL

# Exception handling

@dataclass
class AdaExceptionHandler(AdaNode):
    """Exception handler"""
    exception_choices: List['AdaExceptionChoice'] = field(default_factory=list)
    statements: List[AdaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.EXCEPTION_HANDLER

@dataclass
class AdaExceptionChoice(AdaNode):
    """Exception choice in handler"""
    exception_name: Optional[str] = None  # None for "others"
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.EXCEPTION_CHOICE

# Representation and low-level features

@dataclass
class AdaRepresentationClause(AdaNode):
    """Representation clause for low-level control"""
    clause_type: str  # "record", "enumeration", "attribute_definition"
    type_name: str
    specification: Dict[str, Any]
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.REPRESENTATION_CLAUSE

@dataclass
class AdaPragma(AdaNode):
    """Pragma directive"""
    pragma_name: str
    arguments: List['AdaExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PRAGMA

@dataclass
class AdaAspectSpecification(AdaNode):
    """Aspect specification (Ada 2012)"""
    aspect_name: str
    aspect_value: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.ASPECT_SPECIFICATION

# Contract-based programming and SPARK

@dataclass
class AdaPrecondition(AdaNode):
    """Precondition contract"""
    condition: 'AdaExpression'
    message: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.PRECONDITION

@dataclass
class AdaPostcondition(AdaNode):
    """Postcondition contract"""
    condition: 'AdaExpression'
    message: Optional['AdaExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.POSTCONDITION

@dataclass
class AdaContractCase(AdaNode):
    """Contract case specification"""
    guard: 'AdaExpression'
    consequence: 'AdaExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.CONTRACT_CASE

@dataclass
class AdaGhostDeclaration(AdaDeclaration):
    """Ghost declaration for specification"""
    ghost_entity: AdaDeclaration
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = AdaNodeType.GHOST_DECLARATION

# Factory functions for common constructs

def create_ada_package(name: str, with_body: bool = True) -> Union[AdaPackageSpecification, tuple]:
    """Create Ada package specification and optionally body"""
    spec = AdaPackageSpecification(name=name)
    if with_body:
        body = AdaPackageBody(name=name)
        return spec, body
    return spec

def create_ada_procedure(name: str, parameters: List[AdaParameterDeclaration] = None) -> AdaSubprogramSpecification:
    """Create Ada procedure specification"""
    return AdaSubprogramSpecification(
        name=name,
        subprogram_kind="procedure",
        parameters=parameters or []
    )

def create_ada_function(name: str, return_type: AdaTypeReference, 
                       parameters: List[AdaParameterDeclaration] = None) -> AdaSubprogramSpecification:
    """Create Ada function specification"""
    return AdaSubprogramSpecification(
        name=name,
        subprogram_kind="function",
        return_type=return_type,
        parameters=parameters or []
    )

def create_ada_task(name: str, entries: List[AdaEntryDeclaration] = None) -> AdaTaskSpecification:
    """Create Ada task specification"""
    return AdaTaskSpecification(
        name=name,
        entries=entries or []
    )

def create_ada_protected_object(name: str) -> AdaProtectedSpecification:
    """Create Ada protected object specification"""
    return AdaProtectedSpecification(name=name)

# Export all public classes and functions
__all__ = [
    # Enums
    'AdaNodeType',
    
    # Base classes
    'AdaNode', 'AdaLibraryUnit', 'AdaDeclaration', 'AdaTypeDefinition',
    'AdaStatement', 'AdaExpression', 'AdaLiteral', 'AdaConstraint',
    
    # Compilation units
    'AdaCompilationUnit', 'AdaContextClause', 'AdaWithClause', 'AdaUseClause',
    
    # Program units
    'AdaPackageSpecification', 'AdaPackageBody', 'AdaSubprogramSpecification',
    'AdaSubprogramBody', 'AdaGenericPackage', 'AdaGenericSubprogram',
    'AdaPackageInstantiation', 'AdaGenericFormalParameter',
    
    # Declarations
    'AdaTypeDeclaration', 'AdaSubtypeDeclaration', 'AdaObjectDeclaration',
    'AdaParameterDeclaration', 'AdaExceptionDeclaration', 'AdaRenamingDeclaration',
    
    # Type definitions
    'AdaScalarType', 'AdaEnumerationType', 'AdaIntegerType', 'AdaRealType',
    'AdaArrayType', 'AdaRecordType', 'AdaAccessType', 'AdaPrivateType',
    'AdaTaggedType', 'AdaProtectedType', 'AdaTaskType',
    
    # Record components and variants
    'AdaComponentDeclaration', 'AdaVariantPart', 'AdaVariant',
    'AdaDiscriminantSpecification',
    
    # Constraints
    'AdaRangeConstraint', 'AdaIndexConstraint', 'AdaDiscriminantConstraint',
    'AdaDiscriminantAssociation',
    
    # Statements
    'AdaAssignmentStatement', 'AdaProcedureCall', 'AdaIfStatement', 
    'AdaCaseStatement', 'AdaLoopStatement', 'AdaWhileLoop', 'AdaForLoop',
    'AdaExitStatement', 'AdaReturnStatement', 'AdaRaiseStatement', 'AdaNullStatement',
    'AdaElsifPart', 'AdaCaseAlternative', 'AdaIterationScheme', 'AdaDiscreteRange',
    
    # Expressions
    'AdaFunctionCall', 'AdaAttributeReference', 'AdaQualifiedExpression',
    'AdaTypeConversion', 'AdaAllocator', 'AdaAggregate', 'AdaParameterAssociation',
    'AdaComponentAssociation',
    
    # Literals and identifiers
    'AdaNumericLiteral', 'AdaStringLiteral', 'AdaCharacterLiteral',
    'AdaIdentifier', 'AdaOperatorSymbol', 'AdaTypeReference',
    
    # Tasking
    'AdaTaskSpecification', 'AdaTaskBody', 'AdaProtectedSpecification',
    'AdaProtectedBody', 'AdaEntryDeclaration', 'AdaAcceptStatement',
    'AdaSelectStatement', 'AdaSelectAlternative', 'AdaEntryCall',
    
    # Exception handling
    'AdaExceptionHandler', 'AdaExceptionChoice',
    
    # Representation and pragmas
    'AdaRepresentationClause', 'AdaPragma', 'AdaAspectSpecification',
    
    # Contracts and SPARK
    'AdaPrecondition', 'AdaPostcondition', 'AdaContractCase', 'AdaGhostDeclaration',
    
    # Factory functions
    'create_ada_package', 'create_ada_procedure', 'create_ada_function',
    'create_ada_task', 'create_ada_protected_object'
] 