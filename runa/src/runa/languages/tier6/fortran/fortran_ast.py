"""
Fortran AST (Abstract Syntax Tree) Implementation for Runa Universal Translation Platform

This module provides comprehensive AST node definitions for the Fortran programming language,
supporting both legacy FORTRAN 77 and modern Fortran (90/95/2003/2008/2018) features.

Fortran is the premier language for scientific and high-performance computing, featuring:
- Strong typing with precise numeric control
- Array-oriented programming with powerful intrinsics
- Mathematical and scientific function libraries
- Module system with interfaces and data encapsulation
- Parallel programming with coarrays and do concurrent
- Interoperability with C and other languages

Key Fortran Features Supported:
- Program units (programs, modules, subroutines, functions)
- Derived types with type-bound procedures
- Interfaces and abstract interfaces
- Generic procedures and operator overloading
- Array operations and array sections
- Pointer and allocatable variables
- Parameterized derived types
- Object-oriented programming features
- Parallel constructs (coarrays, do concurrent)
- Interoperability features

Scientific Computing Features:
- Intrinsic mathematical functions
- Array slicing and operations
- Complex number arithmetic
- Precision control (real kinds)
- Vector and matrix operations
- Elemental and pure procedures
- Numerical precision specifications
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum
import uuid

from ...core.ast_base import ASTNode

class FortranNodeType(Enum):
    """Fortran-specific AST node types"""
    # Program units
    PROGRAM = "program"
    MODULE = "module"
    SUBMODULE = "submodule"
    SUBROUTINE = "subroutine"
    FUNCTION = "function"
    BLOCK_DATA = "block_data"
    
    # Procedures and interfaces
    INTERFACE = "interface"
    ABSTRACT_INTERFACE = "abstract_interface"
    PROCEDURE = "procedure"
    GENERIC_INTERFACE = "generic_interface"
    
    # Declarations
    VARIABLE_DECLARATION = "variable_declaration"
    PARAMETER_DECLARATION = "parameter_declaration"
    TYPE_DECLARATION = "type_declaration"
    ENUM_DECLARATION = "enum_declaration"
    
    # Data types
    DERIVED_TYPE = "derived_type"
    TYPE_BOUND_PROCEDURE = "type_bound_procedure"
    COMPONENT_DECLARATION = "component_declaration"
    INTRINSIC_TYPE = "intrinsic_type"
    
    # Attributes
    INTENT_ATTRIBUTE = "intent_attribute"
    DIMENSION_ATTRIBUTE = "dimension_attribute"
    ALLOCATABLE_ATTRIBUTE = "allocatable_attribute"
    POINTER_ATTRIBUTE = "pointer_attribute"
    TARGET_ATTRIBUTE = "target_attribute"
    OPTIONAL_ATTRIBUTE = "optional_attribute"
    
    # Control structures
    IF_CONSTRUCT = "if_construct"
    CASE_CONSTRUCT = "case_construct"
    DO_CONSTRUCT = "do_construct"
    DO_CONCURRENT = "do_concurrent"
    WHERE_CONSTRUCT = "where_construct"
    FORALL_CONSTRUCT = "forall_construct"
    
    # Expressions
    ASSIGNMENT = "assignment"
    BINARY_OPERATION = "binary_operation"
    UNARY_OPERATION = "unary_operation"
    FUNCTION_CALL = "function_call"
    ARRAY_REFERENCE = "array_reference"
    STRUCTURE_COMPONENT = "structure_component"
    
    # Arrays
    ARRAY_CONSTRUCTOR = "array_constructor"
    ARRAY_SECTION = "array_section"
    IMPLIED_DO = "implied_do"
    
    # I/O statements
    READ_STATEMENT = "read_statement"
    WRITE_STATEMENT = "write_statement"
    PRINT_STATEMENT = "print_statement"
    OPEN_STATEMENT = "open_statement"
    CLOSE_STATEMENT = "close_statement"
    
    # Memory management
    ALLOCATE_STATEMENT = "allocate_statement"
    DEALLOCATE_STATEMENT = "deallocate_statement"
    NULLIFY_STATEMENT = "nullify_statement"
    
    # Parallel constructs
    COARRAY_REFERENCE = "coarray_reference"
    SYNC_ALL = "sync_all"
    SYNC_IMAGES = "sync_images"
    CRITICAL_CONSTRUCT = "critical_construct"
    
    # Literals and identifiers
    INTEGER_LITERAL = "integer_literal"
    REAL_LITERAL = "real_literal"
    COMPLEX_LITERAL = "complex_literal"
    LOGICAL_LITERAL = "logical_literal"
    CHARACTER_LITERAL = "character_literal"
    IDENTIFIER = "identifier"
    
    # Special constructs
    USE_STATEMENT = "use_statement"
    IMPORT_STATEMENT = "import_statement"
    COMMON_BLOCK = "common_block"
    EQUIVALENCE = "equivalence"
    NAMELIST = "namelist"

@dataclass
class FortranNode(ASTNode):
    """Base class for all Fortran AST nodes"""
    node_type: FortranNodeType
    source_location: Optional[Dict[str, int]] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if self.node_id is None:
            self.node_id = str(uuid.uuid4())

@dataclass
class FortranProgram(FortranNode):
    """Fortran program unit"""
    name: str
    variables: List['FortranVariableDeclaration'] = field(default_factory=list)
    statements: List['FortranStatement'] = field(default_factory=list)
    contains_section: List['FortranProcedure'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.PROGRAM

@dataclass
class FortranModule(FortranNode):
    """Fortran module"""
    name: str
    use_statements: List['FortranUseStatement'] = field(default_factory=list)
    implicit_statement: Optional['FortranImplicitStatement'] = None
    declarations: List['FortranDeclaration'] = field(default_factory=list)
    interfaces: List['FortranInterface'] = field(default_factory=list)
    contains_section: List['FortranProcedure'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.MODULE

@dataclass
class FortranSubmodule(FortranNode):
    """Fortran submodule"""
    name: str
    parent_name: str
    use_statements: List['FortranUseStatement'] = field(default_factory=list)
    declarations: List['FortranDeclaration'] = field(default_factory=list)
    contains_section: List['FortranProcedure'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.SUBMODULE

@dataclass
class FortranProcedure(FortranNode):
    """Base class for Fortran procedures"""
    name: str
    parameters: List['FortranParameter'] = field(default_factory=list)
    result_variable: Optional[str] = None
    attributes: List[str] = field(default_factory=list)
    variables: List['FortranVariableDeclaration'] = field(default_factory=list)
    statements: List['FortranStatement'] = field(default_factory=list)
    contains_section: List['FortranProcedure'] = field(default_factory=list)

@dataclass
class FortranSubroutine(FortranProcedure):
    """Fortran subroutine"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.SUBROUTINE

@dataclass
class FortranFunction(FortranProcedure):
    """Fortran function"""
    return_type: Optional['FortranTypeSpec'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.FUNCTION

@dataclass
class FortranInterface(FortranNode):
    """Fortran interface"""
    name: Optional[str] = None
    procedures: List[FortranProcedure] = field(default_factory=list)
    generic_spec: Optional[str] = None
    is_abstract: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.INTERFACE

@dataclass
class FortranTypeSpec(FortranNode):
    """Fortran type specification"""
    type_name: str
    kind: Optional[Union[int, str]] = None
    length: Optional[Union[int, str]] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.INTRINSIC_TYPE

@dataclass
class FortranDerivedType(FortranNode):
    """Fortran derived type"""
    name: str
    parameters: List['FortranTypeParameter'] = field(default_factory=list)
    parent_type: Optional[str] = None
    components: List['FortranComponentDeclaration'] = field(default_factory=list)
    type_bound_procedures: List['FortranTypeBoundProcedure'] = field(default_factory=list)
    is_abstract: bool = False
    is_sequence: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.DERIVED_TYPE

@dataclass
class FortranTypeParameter(FortranNode):
    """Fortran type parameter (for parameterized derived types)"""
    name: str
    kind: str  # "kind" or "len"
    default_value: Optional['FortranExpression'] = None

@dataclass
class FortranComponentDeclaration(FortranNode):
    """Fortran component declaration within derived type"""
    name: str
    type_spec: FortranTypeSpec
    attributes: List[str] = field(default_factory=list)
    initialization: Optional['FortranExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.COMPONENT_DECLARATION

@dataclass
class FortranTypeBoundProcedure(FortranNode):
    """Fortran type-bound procedure"""
    name: str
    procedure_name: str
    attributes: List[str] = field(default_factory=list)
    is_generic: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.TYPE_BOUND_PROCEDURE

@dataclass
class FortranParameter(FortranNode):
    """Fortran procedure parameter"""
    name: str
    type_spec: Optional[FortranTypeSpec] = None
    intent: Optional[str] = None  # "in", "out", "inout"
    attributes: List[str] = field(default_factory=list)

@dataclass
class FortranStatement(FortranNode):
    """Base class for Fortran statements"""
    pass

@dataclass
class FortranDeclaration(FortranStatement):
    """Base class for Fortran declarations"""
    pass

@dataclass
class FortranVariableDeclaration(FortranDeclaration):
    """Fortran variable declaration"""
    names: List[str]
    type_spec: FortranTypeSpec
    attributes: List[str] = field(default_factory=list)
    initialization: Optional['FortranExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.VARIABLE_DECLARATION

@dataclass
class FortranParameterDeclaration(FortranDeclaration):
    """Fortran parameter declaration (named constants)"""
    name: str
    type_spec: Optional[FortranTypeSpec] = None
    value: 'FortranExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.PARAMETER_DECLARATION

@dataclass
class FortranUseStatement(FortranStatement):
    """Fortran use statement"""
    module_name: str
    only_list: List[str] = field(default_factory=list)
    rename_list: List[tuple] = field(default_factory=list)
    nature: Optional[str] = None  # "intrinsic" or "non_intrinsic"
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.USE_STATEMENT

@dataclass
class FortranImplicitStatement(FortranStatement):
    """Fortran implicit statement"""
    implicit_spec: List[tuple] = field(default_factory=list)  # [(type, letter_ranges)]
    is_none: bool = False

@dataclass
class FortranExpression(FortranNode):
    """Base class for Fortran expressions"""
    pass

@dataclass
class FortranAssignment(FortranStatement):
    """Fortran assignment statement"""
    lhs: FortranExpression
    rhs: FortranExpression
    is_pointer_assignment: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.ASSIGNMENT

@dataclass
class FortranBinaryOperation(FortranExpression):
    """Fortran binary operation"""
    left: FortranExpression
    right: FortranExpression
    operator: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.BINARY_OPERATION

@dataclass
class FortranUnaryOperation(FortranExpression):
    """Fortran unary operation"""
    operand: FortranExpression
    operator: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.UNARY_OPERATION

@dataclass
class FortranFunctionCall(FortranExpression):
    """Fortran function call"""
    name: str
    arguments: List[FortranExpression] = field(default_factory=list)
    keyword_arguments: Dict[str, FortranExpression] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.FUNCTION_CALL

@dataclass
class FortranArrayReference(FortranExpression):
    """Fortran array reference"""
    array: FortranExpression
    indices: List[FortranExpression] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.ARRAY_REFERENCE

@dataclass
class FortranArraySection(FortranExpression):
    """Fortran array section"""
    array: FortranExpression
    section_subscripts: List['FortranSubscriptTriplet'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.ARRAY_SECTION

@dataclass
class FortranSubscriptTriplet(FortranNode):
    """Fortran subscript triplet (start:end:stride)"""
    start: Optional[FortranExpression] = None
    end: Optional[FortranExpression] = None
    stride: Optional[FortranExpression] = None

@dataclass
class FortranStructureComponent(FortranExpression):
    """Fortran structure component reference"""
    structure: FortranExpression
    component: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.STRUCTURE_COMPONENT

@dataclass
class FortranArrayConstructor(FortranExpression):
    """Fortran array constructor"""
    elements: List[FortranExpression] = field(default_factory=list)
    implied_do: Optional['FortranImpliedDo'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.ARRAY_CONSTRUCTOR

@dataclass
class FortranImpliedDo(FortranNode):
    """Fortran implied do construct"""
    expression: FortranExpression
    variable: str
    start: FortranExpression
    end: FortranExpression
    stride: Optional[FortranExpression] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.IMPLIED_DO

# Control constructs

@dataclass
class FortranIfConstruct(FortranStatement):
    """Fortran if construct"""
    condition: FortranExpression
    then_block: List[FortranStatement] = field(default_factory=list)
    elsif_blocks: List['FortranElsifBlock'] = field(default_factory=list)
    else_block: List[FortranStatement] = field(default_factory=list)
    construct_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.IF_CONSTRUCT

@dataclass
class FortranElsifBlock(FortranNode):
    """Fortran elsif block"""
    condition: FortranExpression
    statements: List[FortranStatement] = field(default_factory=list)

@dataclass
class FortranCaseConstruct(FortranStatement):
    """Fortran case construct"""
    expression: FortranExpression
    case_blocks: List['FortranCaseBlock'] = field(default_factory=list)
    default_block: List[FortranStatement] = field(default_factory=list)
    construct_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.CASE_CONSTRUCT

@dataclass
class FortranCaseBlock(FortranNode):
    """Fortran case block"""
    case_values: List[FortranExpression] = field(default_factory=list)
    statements: List[FortranStatement] = field(default_factory=list)

@dataclass
class FortranDoConstruct(FortranStatement):
    """Fortran do construct"""
    variable: Optional[str] = None
    start: Optional[FortranExpression] = None
    end: Optional[FortranExpression] = None
    step: Optional[FortranExpression] = None
    body: List[FortranStatement] = field(default_factory=list)
    construct_name: Optional[str] = None
    is_infinite: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.DO_CONSTRUCT

@dataclass
class FortranDoConcurrent(FortranStatement):
    """Fortran do concurrent construct"""
    concurrent_headers: List['FortranConcurrentHeader'] = field(default_factory=list)
    mask: Optional[FortranExpression] = None
    body: List[FortranStatement] = field(default_factory=list)
    construct_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.DO_CONCURRENT

@dataclass
class FortranConcurrentHeader(FortranNode):
    """Fortran concurrent header"""
    variable: str
    start: FortranExpression
    end: FortranExpression
    step: Optional[FortranExpression] = None

@dataclass
class FortranWhereConstruct(FortranStatement):
    """Fortran where construct"""
    mask: FortranExpression
    statements: List[FortranStatement] = field(default_factory=list)
    elsewhere_blocks: List['FortranElsewhereBlock'] = field(default_factory=list)
    construct_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.WHERE_CONSTRUCT

@dataclass
class FortranElsewhereBlock(FortranNode):
    """Fortran elsewhere block"""
    mask: Optional[FortranExpression] = None
    statements: List[FortranStatement] = field(default_factory=list)

# I/O statements

@dataclass
class FortranIOStatement(FortranStatement):
    """Base class for Fortran I/O statements"""
    unit: Optional[FortranExpression] = None
    format: Optional[FortranExpression] = None
    iostat: Optional[str] = None
    err: Optional[str] = None
    end: Optional[str] = None

@dataclass
class FortranReadStatement(FortranIOStatement):
    """Fortran read statement"""
    variables: List[FortranExpression] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.READ_STATEMENT

@dataclass
class FortranWriteStatement(FortranIOStatement):
    """Fortran write statement"""
    expressions: List[FortranExpression] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.WRITE_STATEMENT

@dataclass
class FortranPrintStatement(FortranStatement):
    """Fortran print statement"""
    format: Optional[FortranExpression] = None
    expressions: List[FortranExpression] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.PRINT_STATEMENT

# Memory management

@dataclass
class FortranAllocateStatement(FortranStatement):
    """Fortran allocate statement"""
    allocate_objects: List[FortranExpression] = field(default_factory=list)
    type_spec: Optional[FortranTypeSpec] = None
    stat: Optional[str] = None
    errmsg: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.ALLOCATE_STATEMENT

@dataclass
class FortranDeallocateStatement(FortranStatement):
    """Fortran deallocate statement"""
    deallocate_objects: List[FortranExpression] = field(default_factory=list)
    stat: Optional[str] = None
    errmsg: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.DEALLOCATE_STATEMENT

# Coarray constructs

@dataclass
class FortranCoarrayReference(FortranExpression):
    """Fortran coarray reference"""
    array: FortranExpression
    coindices: List[FortranExpression] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.COARRAY_REFERENCE

@dataclass
class FortranSyncAll(FortranStatement):
    """Fortran sync all statement"""
    stat: Optional[str] = None
    errmsg: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.SYNC_ALL

@dataclass
class FortranCriticalConstruct(FortranStatement):
    """Fortran critical construct"""
    statements: List[FortranStatement] = field(default_factory=list)
    construct_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.CRITICAL_CONSTRUCT

# Literals

@dataclass
class FortranIntegerLiteral(FortranExpression):
    """Fortran integer literal"""
    value: int
    kind: Optional[int] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.INTEGER_LITERAL

@dataclass
class FortranRealLiteral(FortranExpression):
    """Fortran real literal"""
    value: float
    kind: Optional[int] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.REAL_LITERAL

@dataclass
class FortranComplexLiteral(FortranExpression):
    """Fortran complex literal"""
    real_part: Union[int, float]
    imag_part: Union[int, float]
    kind: Optional[int] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.COMPLEX_LITERAL

@dataclass
class FortranLogicalLiteral(FortranExpression):
    """Fortran logical literal"""
    value: bool
    kind: Optional[int] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.LOGICAL_LITERAL

@dataclass
class FortranCharacterLiteral(FortranExpression):
    """Fortran character literal"""
    value: str
    kind: Optional[int] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.CHARACTER_LITERAL

@dataclass
class FortranIdentifier(FortranExpression):
    """Fortran identifier"""
    name: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = FortranNodeType.IDENTIFIER

# Utility functions for creating common Fortran constructs

def create_fortran_program(name: str) -> FortranProgram:
    """Create a Fortran program"""
    return FortranProgram(name=name)

def create_fortran_module(name: str) -> FortranModule:
    """Create a Fortran module"""
    return FortranModule(name=name)

def create_fortran_subroutine(name: str, parameters: List[FortranParameter] = None) -> FortranSubroutine:
    """Create a Fortran subroutine"""
    return FortranSubroutine(name=name, parameters=parameters or [])

def create_fortran_function(name: str, return_type: FortranTypeSpec = None, parameters: List[FortranParameter] = None) -> FortranFunction:
    """Create a Fortran function"""
    return FortranFunction(name=name, return_type=return_type, parameters=parameters or [])

def create_fortran_variable(names: List[str], type_name: str, kind: Optional[int] = None) -> FortranVariableDeclaration:
    """Create a Fortran variable declaration"""
    type_spec = FortranTypeSpec(type_name=type_name, kind=kind)
    return FortranVariableDeclaration(names=names, type_spec=type_spec)

def create_fortran_array(name: str, type_name: str, dimensions: List[str]) -> FortranVariableDeclaration:
    """Create a Fortran array declaration"""
    type_spec = FortranTypeSpec(type_name=type_name)
    return FortranVariableDeclaration(names=[name], type_spec=type_spec, attributes=[f"dimension({','.join(dimensions)})"])

def create_fortran_derived_type(name: str) -> FortranDerivedType:
    """Create a Fortran derived type"""
    return FortranDerivedType(name=name)

def create_fortran_do_loop(variable: str, start: int, end: int, step: int = 1) -> FortranDoConstruct:
    """Create a Fortran do loop"""
    return FortranDoConstruct(
        variable=variable,
        start=FortranIntegerLiteral(value=start),
        end=FortranIntegerLiteral(value=end),
        step=FortranIntegerLiteral(value=step) if step != 1 else None
    ) 