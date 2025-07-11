#!/usr/bin/env python3
"""
COBOL AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for COBOL covering COBOL-85 and later standards
including all four divisions (IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE), fixed format,
record-oriented data structures, and mainframe business system features.

This module provides complete AST representation for:
- COBOL program structure (four divisions)
- Fixed format with column positions (7-72)
- Data definitions with PICTURE clauses
- File processing (sequential, indexed, relative)
- Record-oriented data structures
- Business arithmetic and decimal operations
- Structured programming constructs
- SQL integration (EXEC SQL)
- Copy books and includes
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class COBOLNodeType(Enum):
    """COBOL-specific AST node types."""
    # Program structure
    PROGRAM = auto()
    IDENTIFICATION_DIVISION = auto()
    ENVIRONMENT_DIVISION = auto()
    DATA_DIVISION = auto()
    PROCEDURE_DIVISION = auto()
    
    # Data definitions
    FILE_SECTION = auto()
    WORKING_STORAGE_SECTION = auto()
    LINKAGE_SECTION = auto()
    LOCAL_STORAGE_SECTION = auto()
    FILE_DESCRIPTION = auto()
    DATA_DESCRIPTION = auto()
    
    # Statements
    MOVE_STATEMENT = auto()
    ADD_STATEMENT = auto()
    SUBTRACT_STATEMENT = auto()
    MULTIPLY_STATEMENT = auto()
    DIVIDE_STATEMENT = auto()
    COMPUTE_STATEMENT = auto()
    IF_STATEMENT = auto()
    PERFORM_STATEMENT = auto()
    CALL_STATEMENT = auto()
    READ_STATEMENT = auto()
    WRITE_STATEMENT = auto()
    OPEN_STATEMENT = auto()
    CLOSE_STATEMENT = auto()
    ACCEPT_STATEMENT = auto()
    DISPLAY_STATEMENT = auto()
    STOP_STATEMENT = auto()
    GOBACK_STATEMENT = auto()
    SORT_STATEMENT = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL = auto()
    ARITHMETIC_EXPRESSION = auto()
    CONDITION = auto()
    
    # Special constructs
    PICTURE_CLAUSE = auto()
    OCCURS_CLAUSE = auto()
    REDEFINES_CLAUSE = auto()
    VALUE_CLAUSE = auto()
    COPY_STATEMENT = auto()
    EXEC_SQL = auto()


class COBOLDataType(Enum):
    """COBOL data types."""
    ALPHABETIC = "A"
    NUMERIC = "9"
    ALPHANUMERIC = "X"
    NUMERIC_EDITED = "Z"
    ALPHANUMERIC_EDITED = "B"
    NATIONAL = "N"
    BINARY = "BINARY"
    PACKED_DECIMAL = "COMP-3"
    FLOATING_POINT = "COMP-1"
    DOUBLE_PRECISION = "COMP-2"


class COBOLUsage(Enum):
    """COBOL USAGE clause values."""
    DISPLAY = "DISPLAY"
    COMPUTATIONAL = "COMP"
    COMPUTATIONAL_1 = "COMP-1"
    COMPUTATIONAL_2 = "COMP-2"
    COMPUTATIONAL_3 = "COMP-3"
    COMPUTATIONAL_4 = "COMP-4"
    COMPUTATIONAL_5 = "COMP-5"
    BINARY = "BINARY"
    PACKED_DECIMAL = "PACKED-DECIMAL"
    INDEX = "INDEX"
    POINTER = "POINTER"
    NATIONAL = "NATIONAL"


class COBOLAccessMode(Enum):
    """File access modes."""
    SEQUENTIAL = "SEQUENTIAL"
    RANDOM = "RANDOM"
    DYNAMIC = "DYNAMIC"


class COBOLOrganization(Enum):
    """File organization types."""
    SEQUENTIAL = "SEQUENTIAL"
    INDEXED = "INDEXED"
    RELATIVE = "RELATIVE"


@dataclass
class COBOLNode(ASTNode):
    """Base class for all COBOL AST nodes."""
    cobol_node_type: COBOLNodeType = COBOLNodeType.PROGRAM
    line_number: int = 0
    sequence_number: str = ""  # Columns 1-6
    indicator: str = " "       # Column 7 (space, *, /, etc.)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class COBOLProgram(COBOLNode):
    """Complete COBOL program"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.PROGRAM
    identification_division: 'COBOLIdentificationDivision' = None
    environment_division: Optional['COBOLEnvironmentDivision'] = None
    data_division: Optional['COBOLDataDivision'] = None
    procedure_division: Optional['COBOLProcedureDivision'] = None
    nested_programs: List['COBOLProgram'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_program(self)


@dataclass
class COBOLIdentificationDivision(COBOLNode):
    """IDENTIFICATION DIVISION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.IDENTIFICATION_DIVISION
    program_id: str = ""
    author: str = ""
    installation: str = ""
    date_written: str = ""
    date_compiled: str = ""
    security: str = ""
    remarks: str = ""
    
    def accept(self, visitor):
        return visitor.visit_cobol_identification_division(self)


@dataclass
class COBOLEnvironmentDivision(COBOLNode):
    """ENVIRONMENT DIVISION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.ENVIRONMENT_DIVISION
    configuration_section: Optional['COBOLConfigurationSection'] = None
    input_output_section: Optional['COBOLInputOutputSection'] = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_environment_division(self)


@dataclass
class COBOLConfigurationSection(COBOLNode):
    """CONFIGURATION SECTION"""
    source_computer: str = ""
    object_computer: str = ""
    special_names: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_configuration_section(self)


@dataclass
class COBOLInputOutputSection(COBOLNode):
    """INPUT-OUTPUT SECTION"""
    file_control: List['COBOLFileControlEntry'] = field(default_factory=list)
    io_control: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_input_output_section(self)


@dataclass
class COBOLFileControlEntry(COBOLNode):
    """File control entry"""
    file_name: str = ""
    assign_clause: str = ""
    organization: COBOLOrganization = COBOLOrganization.SEQUENTIAL
    access_mode: COBOLAccessMode = COBOLAccessMode.SEQUENTIAL
    record_key: str = ""
    alternate_keys: List[str] = field(default_factory=list)
    file_status: str = ""
    
    def accept(self, visitor):
        return visitor.visit_cobol_file_control_entry(self)


@dataclass
class COBOLDataDivision(COBOLNode):
    """DATA DIVISION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.DATA_DIVISION
    file_section: Optional['COBOLFileSection'] = None
    working_storage_section: Optional['COBOLWorkingStorageSection'] = None
    linkage_section: Optional['COBOLLinkageSection'] = None
    local_storage_section: Optional['COBOLLocalStorageSection'] = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_data_division(self)


@dataclass
class COBOLFileSection(COBOLNode):
    """FILE SECTION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.FILE_SECTION
    file_descriptions: List['COBOLFileDescription'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_file_section(self)


@dataclass
class COBOLWorkingStorageSection(COBOLNode):
    """WORKING-STORAGE SECTION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.WORKING_STORAGE_SECTION
    data_descriptions: List['COBOLDataDescription'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_working_storage_section(self)


@dataclass
class COBOLLinkageSection(COBOLNode):
    """LINKAGE SECTION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.LINKAGE_SECTION
    data_descriptions: List['COBOLDataDescription'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_linkage_section(self)


@dataclass
class COBOLLocalStorageSection(COBOLNode):
    """LOCAL-STORAGE SECTION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.LOCAL_STORAGE_SECTION
    data_descriptions: List['COBOLDataDescription'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_local_storage_section(self)


@dataclass
class COBOLProcedureDivision(COBOLNode):
    """PROCEDURE DIVISION"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.PROCEDURE_DIVISION
    using_clause: List[str] = field(default_factory=list)
    returning_clause: str = ""
    statements: List['COBOLStatement'] = field(default_factory=list)
    paragraphs: List['COBOLParagraph'] = field(default_factory=list)
    sections: List['COBOLSection'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_procedure_division(self)


@dataclass
class COBOLParagraph(COBOLNode):
    """COBOL paragraph"""
    name: str = ""
    statements: List['COBOLStatement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_paragraph(self)


@dataclass
class COBOLSection(COBOLNode):
    """COBOL section"""
    name: str = ""
    paragraphs: List[COBOLParagraph] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_section(self)


# ============================================================================
# Data Descriptions
# ============================================================================

@dataclass
class COBOLFileDescription(COBOLNode):
    """File Description (FD)"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.FILE_DESCRIPTION
    file_name: str = ""
    is_external: bool = False
    is_global: bool = False
    block_contains: str = ""
    record_contains: str = ""
    label_records: str = ""
    value_of: str = ""
    data_records: List[str] = field(default_factory=list)
    record_descriptions: List['COBOLDataDescription'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_file_description(self)


@dataclass
class COBOLDataDescription(COBOLNode):
    """Data Description Entry (01-49, 66, 77, 88)"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.DATA_DESCRIPTION
    level_number: int = 1
    data_name: str = ""
    filler: bool = False
    picture_clause: Optional['COBOLPictureClause'] = None
    usage_clause: Optional[COBOLUsage] = None
    value_clause: Optional['COBOLValueClause'] = None
    occurs_clause: Optional['COBOLOccursClause'] = None
    redefines_clause: Optional['COBOLRedefinesClause'] = None
    is_external: bool = False
    is_global: bool = False
    is_justified: bool = False
    is_synchronized: bool = False
    is_blank_when_zero: bool = False
    sign_clause: str = ""  # LEADING, TRAILING, SEPARATE
    subordinate_items: List['COBOLDataDescription'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_data_description(self)


@dataclass
class COBOLPictureClause(COBOLNode):
    """PICTURE clause"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.PICTURE_CLAUSE
    picture_string: str = ""
    data_type: COBOLDataType = COBOLDataType.ALPHANUMERIC
    length: int = 0
    decimal_positions: int = 0
    
    def accept(self, visitor):
        return visitor.visit_cobol_picture_clause(self)


@dataclass
class COBOLValueClause(COBOLNode):
    """VALUE clause"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.VALUE_CLAUSE
    literal_value: Any = None
    figurative_constant: str = ""  # ZERO, SPACE, HIGH-VALUE, etc.
    
    def accept(self, visitor):
        return visitor.visit_cobol_value_clause(self)


@dataclass
class COBOLOccursClause(COBOLNode):
    """OCCURS clause"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.OCCURS_CLAUSE
    minimum_times: int = 1
    maximum_times: Optional[int] = None
    depending_on: str = ""
    indexed_by: List[str] = field(default_factory=list)
    ascending_keys: List[str] = field(default_factory=list)
    descending_keys: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_occurs_clause(self)


@dataclass
class COBOLRedefinesClause(COBOLNode):
    """REDEFINES clause"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.REDEFINES_CLAUSE
    redefined_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_cobol_redefines_clause(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class COBOLStatement(COBOLNode):
    """Base class for COBOL statements"""
    pass


@dataclass
class COBOLMoveStatement(COBOLStatement):
    """MOVE statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.MOVE_STATEMENT
    source: 'COBOLExpression' = None
    destinations: List['COBOLExpression'] = field(default_factory=list)
    is_corresponding: bool = False
    
    def accept(self, visitor):
        return visitor.visit_cobol_move_statement(self)


@dataclass
class COBOLAddStatement(COBOLStatement):
    """ADD statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.ADD_STATEMENT
    operands: List['COBOLExpression'] = field(default_factory=list)
    to_variables: List['COBOLExpression'] = field(default_factory=list)
    giving_variable: Optional['COBOLExpression'] = None
    is_corresponding: bool = False
    on_size_error: List[COBOLStatement] = field(default_factory=list)
    not_on_size_error: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_add_statement(self)


@dataclass
class COBOLSubtractStatement(COBOLStatement):
    """SUBTRACT statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.SUBTRACT_STATEMENT
    operands: List['COBOLExpression'] = field(default_factory=list)
    from_variables: List['COBOLExpression'] = field(default_factory=list)
    giving_variable: Optional['COBOLExpression'] = None
    is_corresponding: bool = False
    on_size_error: List[COBOLStatement] = field(default_factory=list)
    not_on_size_error: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_subtract_statement(self)


@dataclass
class COBOLMultiplyStatement(COBOLStatement):
    """MULTIPLY statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.MULTIPLY_STATEMENT
    multiplicand: 'COBOLExpression' = None
    multiplier: 'COBOLExpression' = None
    giving_variable: Optional['COBOLExpression'] = None
    on_size_error: List[COBOLStatement] = field(default_factory=list)
    not_on_size_error: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_multiply_statement(self)


@dataclass
class COBOLDivideStatement(COBOLStatement):
    """DIVIDE statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.DIVIDE_STATEMENT
    dividend: 'COBOLExpression' = None
    divisor: 'COBOLExpression' = None
    quotient: Optional['COBOLExpression'] = None
    remainder: Optional['COBOLExpression'] = None
    giving_variable: Optional['COBOLExpression'] = None
    on_size_error: List[COBOLStatement] = field(default_factory=list)
    not_on_size_error: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_divide_statement(self)


@dataclass
class COBOLComputeStatement(COBOLStatement):
    """COMPUTE statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.COMPUTE_STATEMENT
    result_variables: List['COBOLExpression'] = field(default_factory=list)
    arithmetic_expression: 'COBOLArithmeticExpression' = None
    on_size_error: List[COBOLStatement] = field(default_factory=list)
    not_on_size_error: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_compute_statement(self)


@dataclass
class COBOLIfStatement(COBOLStatement):
    """IF statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.IF_STATEMENT
    condition: 'COBOLCondition' = None
    then_statements: List[COBOLStatement] = field(default_factory=list)
    else_statements: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_if_statement(self)


@dataclass
class COBOLPerformStatement(COBOLStatement):
    """PERFORM statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.PERFORM_STATEMENT
    procedure_name: str = ""
    through_procedure: str = ""
    times_expression: Optional['COBOLExpression'] = None
    until_condition: Optional['COBOLCondition'] = None
    varying_clause: Optional['COBOLVaryingClause'] = None
    inline_statements: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_perform_statement(self)


@dataclass
class COBOLVaryingClause(COBOLNode):
    """VARYING clause for PERFORM"""
    identifier: str = ""
    from_value: 'COBOLExpression' = None
    by_value: 'COBOLExpression' = None
    until_condition: 'COBOLCondition' = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_varying_clause(self)


@dataclass
class COBOLCallStatement(COBOLStatement):
    """CALL statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.CALL_STATEMENT
    program_name: 'COBOLExpression' = None
    using_parameters: List['COBOLUsingParameter'] = field(default_factory=list)
    returning_parameter: Optional['COBOLExpression'] = None
    on_overflow: List[COBOLStatement] = field(default_factory=list)
    on_exception: List[COBOLStatement] = field(default_factory=list)
    not_on_exception: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_call_statement(self)


@dataclass
class COBOLUsingParameter(COBOLNode):
    """Parameter for CALL statement"""
    parameter: 'COBOLExpression' = None
    by_reference: bool = True
    by_content: bool = False
    by_value: bool = False
    
    def accept(self, visitor):
        return visitor.visit_cobol_using_parameter(self)


@dataclass
class COBOLReadStatement(COBOLStatement):
    """READ statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.READ_STATEMENT
    file_name: str = ""
    record_name: str = ""
    key_name: str = ""
    into_identifier: str = ""
    at_end: List[COBOLStatement] = field(default_factory=list)
    not_at_end: List[COBOLStatement] = field(default_factory=list)
    invalid_key: List[COBOLStatement] = field(default_factory=list)
    not_invalid_key: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_read_statement(self)


@dataclass
class COBOLWriteStatement(COBOLStatement):
    """WRITE statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.WRITE_STATEMENT
    record_name: str = ""
    from_identifier: str = ""
    advancing_clause: str = ""
    at_end_of_page: List[COBOLStatement] = field(default_factory=list)
    not_at_end_of_page: List[COBOLStatement] = field(default_factory=list)
    invalid_key: List[COBOLStatement] = field(default_factory=list)
    not_invalid_key: List[COBOLStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_write_statement(self)


@dataclass
class COBOLDisplayStatement(COBOLStatement):
    """DISPLAY statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.DISPLAY_STATEMENT
    items: List['COBOLExpression'] = field(default_factory=list)
    upon_device: str = ""
    with_no_advancing: bool = False
    
    def accept(self, visitor):
        return visitor.visit_cobol_display_statement(self)


@dataclass
class COBOLAcceptStatement(COBOLStatement):
    """ACCEPT statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.ACCEPT_STATEMENT
    identifier: str = ""
    from_device: str = ""
    
    def accept(self, visitor):
        return visitor.visit_cobol_accept_statement(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class COBOLExpression(COBOLNode):
    """Base class for COBOL expressions"""
    pass


@dataclass
class COBOLIdentifier(COBOLExpression):
    """COBOL identifier"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.IDENTIFIER
    name: str = ""
    subscripts: List['COBOLExpression'] = field(default_factory=list)
    reference_modification: Optional['COBOLReferenceModification'] = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_identifier(self)


@dataclass
class COBOLReferenceModification(COBOLNode):
    """Reference modification (substring)"""
    start_position: 'COBOLExpression' = None
    length: Optional['COBOLExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_reference_modification(self)


@dataclass
class COBOLLiteral(COBOLExpression):
    """COBOL literal"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.LITERAL
    value: Any = None
    is_numeric: bool = False
    is_alphanumeric: bool = False
    is_national: bool = False
    is_figurative: bool = False
    
    def accept(self, visitor):
        return visitor.visit_cobol_literal(self)


@dataclass
class COBOLArithmeticExpression(COBOLExpression):
    """Arithmetic expression"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.ARITHMETIC_EXPRESSION
    left: COBOLExpression = None
    operator: str = ""  # +, -, *, /, **
    right: COBOLExpression = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_arithmetic_expression(self)


@dataclass
class COBOLCondition(COBOLExpression):
    """COBOL condition"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.CONDITION
    left: COBOLExpression = None
    operator: str = ""  # =, NOT =, <, >, <=, >=
    right: COBOLExpression = None
    logical_operator: str = ""  # AND, OR
    next_condition: Optional['COBOLCondition'] = None
    
    def accept(self, visitor):
        return visitor.visit_cobol_condition(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class COBOLCopyStatement(COBOLNode):
    """COPY statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.COPY_STATEMENT
    copy_book_name: str = ""
    library_name: str = ""
    replacing_clauses: List['COBOLReplacingClause'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_cobol_copy_statement(self)


@dataclass
class COBOLReplacingClause(COBOLNode):
    """REPLACING clause for COPY"""
    old_text: str = ""
    new_text: str = ""
    
    def accept(self, visitor):
        return visitor.visit_cobol_replacing_clause(self)


@dataclass
class COBOLExecSQL(COBOLNode):
    """EXEC SQL statement"""
    cobol_node_type: COBOLNodeType = COBOLNodeType.EXEC_SQL
    sql_statement: str = ""
    
    def accept(self, visitor):
        return visitor.visit_cobol_exec_sql(self)


# ============================================================================
# Factory Functions
# ============================================================================

def create_cobol_program(program_id: str) -> COBOLProgram:
    """Create a COBOL program with basic structure."""
    return COBOLProgram(
        identification_division=COBOLIdentificationDivision(program_id=program_id)
    )

def create_cobol_data_item(level: int, name: str, picture: str = None) -> COBOLDataDescription:
    """Create a COBOL data description entry."""
    item = COBOLDataDescription(level_number=level, data_name=name)
    if picture:
        item.picture_clause = COBOLPictureClause(picture_string=picture)
    return item

def create_cobol_move(source: Any, destination: str) -> COBOLMoveStatement:
    """Create a MOVE statement."""
    if isinstance(source, str):
        source_expr = COBOLLiteral(value=source, is_alphanumeric=True)
    else:
        source_expr = COBOLIdentifier(name=str(source))
    
    dest_expr = COBOLIdentifier(name=destination)
    return COBOLMoveStatement(source=source_expr, destinations=[dest_expr])

def create_cobol_display(*items) -> COBOLDisplayStatement:
    """Create a DISPLAY statement."""
    display_items = []
    for item in items:
        if isinstance(item, str):
            display_items.append(COBOLLiteral(value=item, is_alphanumeric=True))
        else:
            display_items.append(COBOLIdentifier(name=str(item)))
    
    return COBOLDisplayStatement(items=display_items) 