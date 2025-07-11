#!/usr/bin/env python3
"""
Plutus AST Definitions

Comprehensive Abstract Syntax Tree representation for Cardano's Plutus smart contract language.
Plutus is a Haskell-based functional language that compiles to Untyped Plutus Core (UPLC).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum


class PlutusNodeType(Enum):
    """AST node types for Plutus language constructs."""
    # Core language constructs
    PROGRAM = "program"
    MODULE = "module"
    IMPORT = "import"
    EXPORT = "export"
    
    # Declarations
    VALUE_DECLARATION = "value_declaration"
    TYPE_DECLARATION = "type_declaration"
    DATA_DECLARATION = "data_declaration"
    NEWTYPE_DECLARATION = "newtype_declaration"
    CLASS_DECLARATION = "class_declaration"
    INSTANCE_DECLARATION = "instance_declaration"
    
    # Functions and bindings
    FUNCTION_DECLARATION = "function_declaration"
    LAMBDA_EXPRESSION = "lambda_expression"
    LET_BINDING = "let_binding"
    WHERE_CLAUSE = "where_clause"
    
    # Expressions
    VARIABLE_REFERENCE = "variable_reference"
    LITERAL = "literal"
    APPLICATION = "application"
    CONSTRUCTOR = "constructor"
    CASE_EXPRESSION = "case_expression"
    IF_EXPRESSION = "if_expression"
    DO_NOTATION = "do_notation"
    
    # Plutus-specific constructs
    VALIDATOR = "validator"
    MINTING_POLICY = "minting_policy"
    STAKE_VALIDATOR = "stake_validator"
    REDEEMER = "redeemer"
    DATUM = "datum"
    SCRIPT_CONTEXT = "script_context"
    BUILTIN_FUNCTION = "builtin_function"
    
    # UPLC constructs
    UPLC_TERM = "uplc_term"
    UPLC_VARIABLE = "uplc_variable"
    UPLC_LAMBDA = "uplc_lambda"
    UPLC_APPLICATION = "uplc_application"
    UPLC_CONSTANT = "uplc_constant"
    UPLC_BUILTIN = "uplc_builtin"
    UPLC_FORCE = "uplc_force"
    UPLC_DELAY = "uplc_delay"
    UPLC_ERROR = "uplc_error"
    
    # Types
    TYPE_SIGNATURE = "type_signature"
    TYPE_VARIABLE = "type_variable"
    TYPE_CONSTRUCTOR = "type_constructor"
    TYPE_APPLICATION = "type_application"
    FUNCTION_TYPE = "function_type"
    TUPLE_TYPE = "tuple_type"
    LIST_TYPE = "list_type"
    
    # Patterns
    PATTERN = "pattern"
    VARIABLE_PATTERN = "variable_pattern"
    CONSTRUCTOR_PATTERN = "constructor_pattern"
    LITERAL_PATTERN = "literal_pattern"
    WILDCARD_PATTERN = "wildcard_pattern"
    AS_PATTERN = "as_pattern"
    
    # Cardano-specific types
    UTXO = "utxo"
    TX_INPUT = "tx_input"
    TX_OUTPUT = "tx_output"
    VALUE = "value"
    POLICY_ID = "policy_id"
    ASSET_NAME = "asset_name"
    ADDRESS = "address"
    PUB_KEY_HASH = "pub_key_hash"
    SCRIPT_HASH = "script_hash"


@dataclass
class PlutusNode(ABC):
    """Base class for all Plutus AST nodes."""
    node_type: PlutusNodeType
    location: Optional[tuple] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


@dataclass
class PlutusExpression(PlutusNode):
    """Base class for Plutus expressions."""
    type_annotation: Optional['PlutusType'] = None


@dataclass
class PlutusStatement(PlutusNode):
    """Base class for Plutus statements."""
    pass


@dataclass
class PlutusDeclaration(PlutusNode):
    """Base class for Plutus declarations."""
    name: str
    export: bool = False


@dataclass
class PlutusType(PlutusNode):
    """Base class for Plutus types."""
    pass


# Core language constructs

@dataclass
class PlutusProgram(PlutusNode):
    """Root node representing a complete Plutus program."""
    modules: List['PlutusModule']
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.PROGRAM
    
    def accept(self, visitor):
        return visitor.visit_program(self)


@dataclass
class PlutusModule(PlutusNode):
    """Represents a Plutus module."""
    name: str
    imports: List['PlutusImport']
    exports: List['PlutusExport']
    declarations: List[PlutusDeclaration]
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.MODULE
    
    def accept(self, visitor):
        return visitor.visit_module(self)


@dataclass
class PlutusImport(PlutusNode):
    """Represents an import statement."""
    module_name: str
    qualified: bool = False
    alias: Optional[str] = None
    imports: Optional[List[str]] = None
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.IMPORT
    
    def accept(self, visitor):
        return visitor.visit_import(self)


@dataclass
class PlutusExport(PlutusNode):
    """Represents an export statement."""
    name: str
    export_type: str = "value"  # value, type, constructor
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.EXPORT
    
    def accept(self, visitor):
        return visitor.visit_export(self)


# Declarations

@dataclass
class PlutusValueDeclaration(PlutusDeclaration):
    """Represents a value declaration."""
    type_signature: Optional[PlutusType]
    expression: PlutusExpression
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.VALUE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_value_declaration(self)


@dataclass
class PlutusFunctionDeclaration(PlutusDeclaration):
    """Represents a function declaration."""
    parameters: List[str]
    type_signature: Optional[PlutusType]
    body: PlutusExpression
    where_clause: Optional['PlutusWhereClause'] = None
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.FUNCTION_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


@dataclass
class PlutusDataDeclaration(PlutusDeclaration):
    """Represents a data type declaration."""
    type_parameters: List[str]
    constructors: List['PlutusConstructor']
    deriving: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.DATA_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_data_declaration(self)


@dataclass
class PlutusNewtypeDeclaration(PlutusDeclaration):
    """Represents a newtype declaration."""
    type_parameters: List[str]
    constructor: 'PlutusConstructor'
    deriving: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.NEWTYPE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_newtype_declaration(self)


# Expressions

@dataclass
class PlutusVariableReference(PlutusExpression):
    """Represents a variable reference."""
    name: str
    qualified: bool = False
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.VARIABLE_REFERENCE
    
    def accept(self, visitor):
        return visitor.visit_variable_reference(self)


@dataclass
class PlutusLiteral(PlutusExpression):
    """Represents a literal value."""
    value: Any
    literal_type: str  # integer, string, char, rational, etc.
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class PlutusApplication(PlutusExpression):
    """Represents function application."""
    function: PlutusExpression
    arguments: List[PlutusExpression]
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.APPLICATION
    
    def accept(self, visitor):
        return visitor.visit_application(self)


@dataclass
class PlutusLambdaExpression(PlutusExpression):
    """Represents a lambda expression."""
    parameters: List[str]
    body: PlutusExpression
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.LAMBDA_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_lambda_expression(self)


@dataclass
class PlutusCaseExpression(PlutusExpression):
    """Represents a case expression."""
    expression: PlutusExpression
    alternatives: List['PlutusAlternative']
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.CASE_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_case_expression(self)


@dataclass
class PlutusIfExpression(PlutusExpression):
    """Represents an if-then-else expression."""
    condition: PlutusExpression
    then_expression: PlutusExpression
    else_expression: PlutusExpression
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.IF_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_if_expression(self)


@dataclass
class PlutusLetBinding(PlutusExpression):
    """Represents a let binding."""
    bindings: List['PlutusBinding']
    expression: PlutusExpression
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.LET_BINDING
    
    def accept(self, visitor):
        return visitor.visit_let_binding(self)


@dataclass
class PlutusDoNotation(PlutusExpression):
    """Represents do notation for monadic computations."""
    statements: List['PlutusDoStatement']
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.DO_NOTATION
    
    def accept(self, visitor):
        return visitor.visit_do_notation(self)


# Plutus-specific constructs

@dataclass
class PlutusValidator(PlutusDeclaration):
    """Represents a Plutus validator script."""
    validator_type: str  # spending, minting, staking, etc.
    parameters: List[str]
    body: PlutusExpression
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.VALIDATOR
    
    def accept(self, visitor):
        return visitor.visit_validator(self)


@dataclass
class PlutusMintingPolicy(PlutusDeclaration):
    """Represents a minting policy."""
    parameters: List[str]
    body: PlutusExpression
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.MINTING_POLICY
    
    def accept(self, visitor):
        return visitor.visit_minting_policy(self)


@dataclass
class PlutusBuiltinFunction(PlutusExpression):
    """Represents a Plutus builtin function."""
    name: str
    builtin_type: str
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.BUILTIN_FUNCTION
    
    def accept(self, visitor):
        return visitor.visit_builtin_function(self)


# UPLC constructs

@dataclass
class PlutusUPLCTerm(PlutusExpression):
    """Represents an Untyped Plutus Core term."""
    term_type: str
    term_data: Any
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.UPLC_TERM
    
    def accept(self, visitor):
        return visitor.visit_uplc_term(self)


@dataclass
class PlutusUPLCVariable(PlutusUPLCTerm):
    """Represents a UPLC variable with DeBruijn index."""
    debruijn_index: int
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.UPLC_VARIABLE
        self.term_type = "variable"
        self.term_data = self.debruijn_index


@dataclass
class PlutusUPLCLambda(PlutusUPLCTerm):
    """Represents a UPLC lambda abstraction."""
    parameter_name: str
    body: PlutusUPLCTerm
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.UPLC_LAMBDA
        self.term_type = "lambda"
        self.term_data = {"parameter": self.parameter_name, "body": self.body}


@dataclass
class PlutusUPLCApplication(PlutusUPLCTerm):
    """Represents a UPLC application."""
    function: PlutusUPLCTerm
    argument: PlutusUPLCTerm
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.UPLC_APPLICATION
        self.term_type = "application"
        self.term_data = {"function": self.function, "argument": self.argument}


@dataclass
class PlutusUPLCConstant(PlutusUPLCTerm):
    """Represents a UPLC constant."""
    constant_type: str
    value: Any
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.UPLC_CONSTANT
        self.term_type = "constant"
        self.term_data = {"type": self.constant_type, "value": self.value}


@dataclass
class PlutusUPLCBuiltin(PlutusUPLCTerm):
    """Represents a UPLC builtin function."""
    builtin_name: str
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.UPLC_BUILTIN
        self.term_type = "builtin"
        self.term_data = self.builtin_name


# Types

@dataclass
class PlutusTypeSignature(PlutusType):
    """Represents a type signature."""
    type_expression: PlutusType
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.TYPE_SIGNATURE
    
    def accept(self, visitor):
        return visitor.visit_type_signature(self)


@dataclass
class PlutusTypeVariable(PlutusType):
    """Represents a type variable."""
    name: str
    kind: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.TYPE_VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_type_variable(self)


@dataclass
class PlutusTypeConstructor(PlutusType):
    """Represents a type constructor."""
    name: str
    arguments: List[PlutusType] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.TYPE_CONSTRUCTOR
    
    def accept(self, visitor):
        return visitor.visit_type_constructor(self)


@dataclass
class PlutusFunctionType(PlutusType):
    """Represents a function type."""
    domain: PlutusType
    codomain: PlutusType
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.FUNCTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)


# Patterns

@dataclass
class PlutusPattern(PlutusNode):
    """Base class for patterns."""
    pass


@dataclass
class PlutusVariablePattern(PlutusPattern):
    """Represents a variable pattern."""
    name: str
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.VARIABLE_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_variable_pattern(self)


@dataclass
class PlutusConstructorPattern(PlutusPattern):
    """Represents a constructor pattern."""
    constructor: str
    patterns: List[PlutusPattern]
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.CONSTRUCTOR_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_constructor_pattern(self)


@dataclass
class PlutusLiteralPattern(PlutusPattern):
    """Represents a literal pattern."""
    value: Any
    literal_type: str
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.LITERAL_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_literal_pattern(self)


# Helper classes

@dataclass
class PlutusConstructor:
    """Represents a data constructor."""
    name: str
    fields: List[PlutusType]


@dataclass
class PlutusAlternative:
    """Represents a case alternative."""
    pattern: PlutusPattern
    expression: PlutusExpression


@dataclass
class PlutusBinding:
    """Represents a let binding."""
    name: str
    expression: PlutusExpression
    type_signature: Optional[PlutusType] = None


@dataclass
class PlutusDoStatement:
    """Represents a statement in do notation."""
    statement_type: str  # bind, let, expression
    content: Any


@dataclass
class PlutusWhereClause:
    """Represents a where clause."""
    bindings: List[PlutusBinding]
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.WHERE_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_where_clause(self)


# Cardano-specific types

@dataclass
class PlutusValue(PlutusExpression):
    """Represents a Cardano Value (ADA + native tokens)."""
    ada_amount: int
    tokens: Dict[str, Dict[str, int]] = field(default_factory=dict)  # {policy_id: {asset_name: amount}}
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.VALUE
    
    def accept(self, visitor):
        return visitor.visit_value(self)


@dataclass
class PlutusAddress(PlutusExpression):
    """Represents a Cardano address."""
    payment_credential: str
    staking_credential: Optional[str] = None
    network: str = "mainnet"
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.ADDRESS
    
    def accept(self, visitor):
        return visitor.visit_address(self)


@dataclass
class PlutusTxInput(PlutusExpression):
    """Represents a transaction input."""
    tx_id: str
    output_index: int
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.TX_INPUT
    
    def accept(self, visitor):
        return visitor.visit_tx_input(self)


@dataclass
class PlutusTxOutput(PlutusExpression):
    """Represents a transaction output."""
    address: PlutusAddress
    value: PlutusValue
    datum: Optional[PlutusExpression] = None
    reference_script: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PlutusNodeType.TX_OUTPUT
    
    def accept(self, visitor):
        return visitor.visit_tx_output(self)


# Visitor pattern interface
class PlutusASTVisitor(ABC):
    """Abstract base class for AST visitors."""
    
    @abstractmethod
    def visit_program(self, node: PlutusProgram):
        pass
    
    @abstractmethod
    def visit_module(self, node: PlutusModule):
        pass
    
    @abstractmethod
    def visit_function_declaration(self, node: PlutusFunctionDeclaration):
        pass
    
    @abstractmethod
    def visit_expression(self, node: PlutusExpression):
        pass 