#!/usr/bin/env python3
"""
Pact AST Definitions

Comprehensive Abstract Syntax Tree representation for Kadena's Pact smart contract language.
Pact is a LISP-like, human-readable language with formal verification and multi-sig support.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum


class PactNodeType(Enum):
    """AST node types for Pact language constructs."""
    # Core program structure
    PROGRAM = "program"
    MODULE = "module"
    CONTRACT = "contract"
    INTERFACE = "interface"
    
    # Declarations
    DEFUN = "defun"
    DEFPACT = "defpact"
    DEFSCHEMA = "defschema"
    DEFTABLE = "deftable"
    DEFCAP = "defcap"
    DEFCONST = "defconst"
    
    # Expressions
    LITERAL = "literal"
    VARIABLE = "variable"
    LIST = "list"
    FUNCTION_CALL = "function_call"
    LAMBDA = "lambda"
    LET = "let"
    BIND = "bind"
    IF = "if"
    COND = "cond"
    AND = "and"
    OR = "or"
    NOT = "not"
    TRY = "try"
    
    # Data structures
    OBJECT = "object"
    LIST_VALUE = "list_value"
    
    # Capabilities and authorization
    CAPABILITY = "capability"
    REQUIRE_CAPABILITY = "require_capability"
    COMPOSE_CAPABILITY = "compose_capability"
    INSTALL_CAPABILITY = "install_capability"
    WITH_CAPABILITY = "with_capability"
    
    # Database operations
    READ = "read"
    WRITE = "write"
    INSERT = "insert"
    UPDATE = "update"
    SELECT = "select"
    KEYS = "keys"
    KEYLOG = "keylog"
    TXLOG = "txlog"
    
    # Formal verification
    PROPERTY = "property"
    INVARIANT = "invariant"
    ENFORCE = "enforce"
    ENFORCE_ONE = "enforce_one"
    EXPECT_FAILURE = "expect_failure"
    
    # Pact transactions
    STEP = "step"
    STEP_WITH_ROLLBACK = "step_with_rollback"
    ROLLBACK = "rollback"
    CANCEL = "cancel"
    CONTINUE = "continue"
    
    # Keysets and governance
    KEYSET = "keyset"
    KEYSET_REF_GUARD = "keyset_ref_guard"
    DEFINE_KEYSET = "define_keyset"
    
    # Time and blocks
    CHAIN_TIME = "chain_time"
    BLOCK_HEIGHT = "block_height"
    BLOCK_TIME = "block_time"
    
    # Cryptography
    HASH = "hash"
    VERIFY_SPKI = "verify_spki"
    
    # Namespaces
    NAMESPACE = "namespace"
    DEFINE_NAMESPACE = "define_namespace"


@dataclass
class PactNode(ABC):
    """Base class for all Pact AST nodes."""
    node_type: PactNodeType
    line: int = 0
    column: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PactProgram(PactNode):
    """Root node representing a complete Pact program."""
    modules: List['PactModule']
    imports: List['PactImport'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = PactNodeType.PROGRAM


@dataclass
class PactModule(PactNode):
    """Pact module declaration."""
    name: str
    governance: Optional['PactExpression'] = None  # Governance capability
    declarations: List['PactDeclaration'] = field(default_factory=list)
    implements: List[str] = field(default_factory=list)  # Implemented interfaces
    blessed: List[str] = field(default_factory=list)  # Blessed hashes
    
    def __post_init__(self):
        self.node_type = PactNodeType.MODULE


@dataclass
class PactInterface(PactNode):
    """Pact interface declaration."""
    name: str
    declarations: List['PactDeclaration']
    
    def __post_init__(self):
        self.node_type = PactNodeType.INTERFACE


@dataclass
class PactImport(PactNode):
    """Module import."""
    module_name: str
    namespace: Optional[str] = None
    hash: Optional[str] = None


# Base classes for different types of nodes
@dataclass
class PactExpression(PactNode):
    """Base class for Pact expressions."""
    pass


@dataclass
class PactDeclaration(PactNode):
    """Base class for Pact declarations."""
    name: str


@dataclass
class PactStatement(PactNode):
    """Base class for Pact statements."""
    pass


@dataclass
class PactType(PactNode):
    """Pact type representation."""
    name: str
    args: List['PactType'] = field(default_factory=list)


# Expressions
@dataclass
class PactLiteral(PactExpression):
    """Literal value (number, string, boolean)."""
    value: Any
    literal_type: str  # "integer", "decimal", "string", "bool", "time"
    
    def __post_init__(self):
        self.node_type = PactNodeType.LITERAL


@dataclass
class PactVariable(PactExpression):
    """Variable reference."""
    name: str
    qualified: bool = False
    
    def __post_init__(self):
        self.node_type = PactNodeType.VARIABLE


@dataclass
class PactList(PactExpression):
    """List expression (function call or data list)."""
    elements: List[PactExpression]
    is_function_call: bool = True
    
    def __post_init__(self):
        self.node_type = PactNodeType.LIST


@dataclass
class PactFunctionCall(PactExpression):
    """Function call expression."""
    function: str
    arguments: List[PactExpression]
    
    def __post_init__(self):
        self.node_type = PactNodeType.FUNCTION_CALL


@dataclass
class PactLambda(PactExpression):
    """Lambda expression."""
    parameters: List[str]
    body: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.LAMBDA


@dataclass
class PactLet(PactExpression):
    """Let binding expression."""
    bindings: List['PactBinding']
    body: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.LET


@dataclass
class PactBind(PactExpression):
    """Bind expression for object destructuring."""
    object_expr: PactExpression
    bindings: Dict[str, str]  # field -> variable mapping
    body: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.BIND


@dataclass
class PactIf(PactExpression):
    """Conditional expression."""
    condition: PactExpression
    then_expr: PactExpression
    else_expr: Optional[PactExpression] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.IF


@dataclass
class PactCond(PactExpression):
    """Multi-way conditional expression."""
    clauses: List['PactCondClause']
    
    def __post_init__(self):
        self.node_type = PactNodeType.COND


@dataclass
class PactCondClause(PactNode):
    """Single clause in cond expression."""
    condition: PactExpression
    body: PactExpression


@dataclass
class PactObject(PactExpression):
    """Object literal."""
    fields: Dict[str, PactExpression]
    
    def __post_init__(self):
        self.node_type = PactNodeType.OBJECT


@dataclass
class PactListValue(PactExpression):
    """List literal value."""
    elements: List[PactExpression]
    
    def __post_init__(self):
        self.node_type = PactNodeType.LIST_VALUE


@dataclass
class PactTry(PactExpression):
    """Try-catch expression."""
    try_expr: PactExpression
    catch_expr: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.TRY


# Declarations
@dataclass
class PactDefun(PactDeclaration):
    """Function definition."""
    parameters: List['PactParameter']
    return_type: Optional[PactType] = None
    body: Optional[PactExpression] = None
    documentation: Optional[str] = None
    model: List[PactExpression] = field(default_factory=list)  # Formal verification model
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFUN


@dataclass
class PactDefpact(PactDeclaration):
    """Pact multi-step transaction definition."""
    parameters: List['PactParameter']
    return_type: Optional[PactType] = None
    steps: List['PactStep']
    documentation: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFPACT


@dataclass
class PactDefschema(PactDeclaration):
    """Schema definition."""
    fields: List['PactSchemaField']
    documentation: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFSCHEMA


@dataclass
class PactDeftable(PactDeclaration):
    """Table definition."""
    schema: str
    documentation: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFTABLE


@dataclass
class PactDefcap(PactDeclaration):
    """Capability definition."""
    parameters: List['PactParameter']
    body: Optional[PactExpression] = None
    documentation: Optional[str] = None
    managed: Optional[PactExpression] = None  # Managed capability parameter
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFCAP


@dataclass
class PactDefconst(PactDeclaration):
    """Constant definition."""
    value: PactExpression
    pact_type: Optional[PactType] = None
    documentation: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFCONST


# Supporting structures
@dataclass
class PactParameter(PactNode):
    """Function parameter."""
    name: str
    pact_type: Optional[PactType] = None


@dataclass
class PactSchemaField(PactNode):
    """Schema field definition."""
    name: str
    field_type: PactType
    optional: bool = False


@dataclass
class PactBinding(PactNode):
    """Variable binding in let expression."""
    variable: str
    value: PactExpression
    pact_type: Optional[PactType] = None


@dataclass
class PactStep(PactNode):
    """Step in a pact transaction."""
    body: PactExpression
    rollback: Optional[PactExpression] = None
    step_with_rollback: bool = False
    
    def __post_init__(self):
        if self.rollback:
            self.node_type = PactNodeType.STEP_WITH_ROLLBACK
        else:
            self.node_type = PactNodeType.STEP


# Capability system
@dataclass
class PactCapability(PactExpression):
    """Capability expression."""
    name: str
    arguments: List[PactExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = PactNodeType.CAPABILITY


@dataclass
class PactRequireCapability(PactExpression):
    """Require capability expression."""
    capability: PactCapability
    
    def __post_init__(self):
        self.node_type = PactNodeType.REQUIRE_CAPABILITY


@dataclass
class PactWithCapability(PactExpression):
    """With-capability expression."""
    capability: PactCapability
    body: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.WITH_CAPABILITY


# Database operations
@dataclass
class PactRead(PactExpression):
    """Database read operation."""
    table: str
    key: PactExpression
    columns: Optional[List[str]] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.READ


@dataclass
class PactWrite(PactExpression):
    """Database write operation."""
    table: str
    key: PactExpression
    object_expr: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.WRITE


@dataclass
class PactInsert(PactExpression):
    """Database insert operation."""
    table: str
    key: PactExpression
    object_expr: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.INSERT


@dataclass
class PactUpdate(PactExpression):
    """Database update operation."""
    table: str
    key: PactExpression
    object_expr: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.UPDATE


@dataclass
class PactSelect(PactExpression):
    """Database select operation."""
    table: str
    columns: Optional[List[str]] = None
    where_clause: Optional[PactExpression] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.SELECT


# Formal verification
@dataclass
class PactProperty(PactExpression):
    """Property for formal verification."""
    predicate: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.PROPERTY


@dataclass
class PactInvariant(PactExpression):
    """Invariant for formal verification."""
    predicate: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.INVARIANT


@dataclass
class PactEnforce(PactExpression):
    """Enforce assertion."""
    condition: PactExpression
    message: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = PactNodeType.ENFORCE


@dataclass
class PactEnforceOne(PactExpression):
    """Enforce one of several conditions."""
    message: str
    conditions: List[PactExpression]
    
    def __post_init__(self):
        self.node_type = PactNodeType.ENFORCE_ONE


# Keysets and authorization
@dataclass
class PactKeyset(PactExpression):
    """Keyset definition."""
    keys: List[str]
    predicate: str = "keys-all"  # keys-all, keys-any, keys-2, or custom function
    
    def __post_init__(self):
        self.node_type = PactNodeType.KEYSET


@dataclass
class PactKeysetRefGuard(PactExpression):
    """Keyset reference guard."""
    keyset_name: str
    
    def __post_init__(self):
        self.node_type = PactNodeType.KEYSET_REF_GUARD


@dataclass
class PactDefineKeyset(PactExpression):
    """Define keyset operation."""
    name: str
    keyset: PactKeyset
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFINE_KEYSET


# Time and blockchain operations
@dataclass
class PactChainTime(PactExpression):
    """Current chain time."""
    
    def __post_init__(self):
        self.node_type = PactNodeType.CHAIN_TIME


@dataclass
class PactBlockHeight(PactExpression):
    """Current block height."""
    
    def __post_init__(self):
        self.node_type = PactNodeType.BLOCK_HEIGHT


@dataclass
class PactBlockTime(PactExpression):
    """Current block time."""
    
    def __post_init__(self):
        self.node_type = PactNodeType.BLOCK_TIME


# Cryptographic operations
@dataclass
class PactHash(PactExpression):
    """Hash operation."""
    value: PactExpression
    algorithm: str = "sha256"  # sha256, sha512, keccak256, blake2b256
    
    def __post_init__(self):
        self.node_type = PactNodeType.HASH


@dataclass
class PactVerifySpki(PactExpression):
    """SPKI signature verification."""
    message: PactExpression
    signature: PactExpression
    public_key: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.VERIFY_SPKI


# Namespace operations
@dataclass
class PactNamespace(PactExpression):
    """Namespace declaration."""
    name: str
    guard: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.NAMESPACE


@dataclass
class PactDefineNamespace(PactExpression):
    """Define namespace operation."""
    name: str
    guard: PactExpression
    
    def __post_init__(self):
        self.node_type = PactNodeType.DEFINE_NAMESPACE


# Utility functions for AST construction
def create_pact_function_call(function_name: str, *args: PactExpression) -> PactFunctionCall:
    """Create a function call node."""
    return PactFunctionCall(function=function_name, arguments=list(args))


def create_pact_literal(value: Any) -> PactLiteral:
    """Create a literal node with appropriate type."""
    if isinstance(value, bool):
        return PactLiteral(value=value, literal_type="bool")
    elif isinstance(value, int):
        return PactLiteral(value=value, literal_type="integer")
    elif isinstance(value, float):
        return PactLiteral(value=value, literal_type="decimal")
    elif isinstance(value, str):
        return PactLiteral(value=value, literal_type="string")
    else:
        return PactLiteral(value=str(value), literal_type="string")


def create_pact_object(**fields) -> PactObject:
    """Create an object literal from keyword arguments."""
    pact_fields = {}
    for key, value in fields.items():
        if isinstance(value, PactExpression):
            pact_fields[key] = value
        else:
            pact_fields[key] = create_pact_literal(value)
    return PactObject(fields=pact_fields) 