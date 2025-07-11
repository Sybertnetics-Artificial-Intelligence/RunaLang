"""
SmartPy AST Nodes

Abstract Syntax Tree nodes for SmartPy - a Python-based smart contract language for Tezos.
SmartPy provides Python syntax for writing smart contracts that compile to Michelson.
"""

from typing import List, Optional, Any, Dict, Union
from dataclasses import dataclass
from enum import Enum

from runa.ast.base import ASTNode, SourceInfo


class SmartPyVisibility(Enum):
    """Visibility levels for SmartPy elements."""
    PUBLIC = "public"
    PRIVATE = "private"


class SmartPyType(Enum):
    """SmartPy built-in types."""
    INT = "int"
    NAT = "nat" 
    STRING = "string"
    BYTES = "bytes"
    BOOL = "bool"
    UNIT = "unit"
    ADDRESS = "address"
    TIMESTAMP = "timestamp"
    MUTEZ = "mutez"
    KEY = "key"
    KEY_HASH = "key_hash"
    SIGNATURE = "signature"
    CHAIN_ID = "chain_id"
    LIST = "list"
    SET = "set"
    MAP = "map"
    BIG_MAP = "big_map"
    RECORD = "record"
    VARIANT = "variant"
    OPTION = "option"
    CONTRACT = "contract"
    OPERATION = "operation"
    LAMBDA = "lambda"


@dataclass
class SmartPyNode(ASTNode):
    """Base class for all SmartPy AST nodes."""
    source_info: Optional[SourceInfo] = None


# Type nodes
@dataclass 
class SmartPyTypeAnnotation(SmartPyNode):
    """Base class for type annotations."""
    pass


@dataclass
class SmartPyPrimitiveType(SmartPyTypeAnnotation):
    """Primitive type annotation."""
    type_name: SmartPyType


@dataclass
class SmartPyListType(SmartPyTypeAnnotation):
    """List type annotation: list[element_type]."""
    element_type: SmartPyTypeAnnotation


@dataclass
class SmartPyMapType(SmartPyTypeAnnotation):
    """Map type annotation: map[key_type, value_type]."""
    key_type: SmartPyTypeAnnotation
    value_type: SmartPyTypeAnnotation


@dataclass
class SmartPyBigMapType(SmartPyTypeAnnotation):
    """BigMap type annotation: big_map[key_type, value_type]."""
    key_type: SmartPyTypeAnnotation
    value_type: SmartPyTypeAnnotation


@dataclass
class SmartPySetType(SmartPyTypeAnnotation):
    """Set type annotation: set[element_type]."""
    element_type: SmartPyTypeAnnotation


@dataclass
class SmartPyOptionType(SmartPyTypeAnnotation):
    """Option type annotation: option[inner_type]."""
    inner_type: SmartPyTypeAnnotation


@dataclass
class SmartPyRecordType(SmartPyTypeAnnotation):
    """Record type annotation with named fields."""
    fields: Dict[str, SmartPyTypeAnnotation]


@dataclass
class SmartPyVariantType(SmartPyTypeAnnotation):
    """Variant type annotation."""
    variants: Dict[str, Optional[SmartPyTypeAnnotation]]


@dataclass
class SmartPyContractType(SmartPyTypeAnnotation):
    """Contract type annotation."""
    parameter_type: SmartPyTypeAnnotation


@dataclass
class SmartPyLambdaType(SmartPyTypeAnnotation):
    """Lambda type annotation."""
    param_type: SmartPyTypeAnnotation
    return_type: SmartPyTypeAnnotation


# Expression nodes
@dataclass
class SmartPyExpression(SmartPyNode):
    """Base class for expressions."""
    pass


@dataclass
class SmartPyLiteral(SmartPyExpression):
    """Literal value expression."""
    value: Any
    type_hint: Optional[SmartPyTypeAnnotation] = None


@dataclass
class SmartPyIdentifier(SmartPyExpression):
    """Identifier expression."""
    name: str


@dataclass
class SmartPyBinaryOp(SmartPyExpression):
    """Binary operation expression."""
    left: SmartPyExpression
    operator: str
    right: SmartPyExpression


@dataclass
class SmartPyUnaryOp(SmartPyExpression):
    """Unary operation expression."""
    operator: str
    operand: SmartPyExpression


@dataclass
class SmartPyFunctionCall(SmartPyExpression):
    """Function call expression."""
    function: SmartPyExpression
    args: List[SmartPyExpression]
    keywords: Dict[str, SmartPyExpression]


@dataclass
class SmartPyAttributeAccess(SmartPyExpression):
    """Attribute access expression: obj.attr."""
    object: SmartPyExpression
    attribute: str


@dataclass
class SmartPyIndexAccess(SmartPyExpression):
    """Index access expression: obj[index]."""
    object: SmartPyExpression
    index: SmartPyExpression


@dataclass
class SmartPySlice(SmartPyExpression):
    """Slice expression: obj[start:end]."""
    object: SmartPyExpression
    start: Optional[SmartPyExpression]
    end: Optional[SmartPyExpression]
    step: Optional[SmartPyExpression]


@dataclass
class SmartPyConditional(SmartPyExpression):
    """Conditional expression: a if condition else b."""
    test: SmartPyExpression
    if_true: SmartPyExpression
    if_false: SmartPyExpression


@dataclass
class SmartPyLambda(SmartPyExpression):
    """Lambda expression."""
    parameters: List[str]
    body: SmartPyExpression


@dataclass
class SmartPyListLiteral(SmartPyExpression):
    """List literal expression."""
    elements: List[SmartPyExpression]


@dataclass
class SmartPyMapLiteral(SmartPyExpression):
    """Map literal expression."""
    pairs: List[tuple[SmartPyExpression, SmartPyExpression]]


@dataclass
class SmartPySetLiteral(SmartPyExpression):
    """Set literal expression."""
    elements: List[SmartPyExpression]


@dataclass
class SmartPyRecordLiteral(SmartPyExpression):
    """Record literal expression."""
    fields: Dict[str, SmartPyExpression]


@dataclass
class SmartPyVariantLiteral(SmartPyExpression):
    """Variant literal expression."""
    constructor: str
    value: Optional[SmartPyExpression]


# SmartPy built-in expressions
@dataclass
class SmartPySender(SmartPyExpression):
    """sp.sender expression."""
    pass


@dataclass
class SmartPyAmount(SmartPyExpression):
    """sp.amount expression."""
    pass


@dataclass
class SmartPyBalance(SmartPyExpression):
    """sp.balance expression."""
    pass


@dataclass
class SmartPyNow(SmartPyExpression):
    """sp.now expression."""
    pass


@dataclass
class SmartPyLevel(SmartPyExpression):
    """sp.level expression."""
    pass


@dataclass
class SmartPyChainId(SmartPyExpression):
    """sp.chain_id expression."""
    pass


@dataclass
class SmartPySelfAddress(SmartPyExpression):
    """sp.self_address expression."""
    pass


@dataclass
class SmartPySource(SmartPyExpression):
    """sp.source expression."""
    pass


# Statement nodes
@dataclass
class SmartPyStatement(SmartPyNode):
    """Base class for statements."""
    pass


@dataclass
class SmartPyAssignment(SmartPyStatement):
    """Assignment statement."""
    target: SmartPyExpression
    value: SmartPyExpression


@dataclass
class SmartPyAugmentedAssignment(SmartPyStatement):
    """Augmented assignment statement (+=, -=, etc.)."""
    target: SmartPyExpression
    operator: str
    value: SmartPyExpression


@dataclass
class SmartPyExpressionStatement(SmartPyStatement):
    """Expression used as statement."""
    expression: SmartPyExpression


@dataclass
class SmartPyBlock(SmartPyStatement):
    """Block of statements."""
    statements: List[SmartPyStatement]


@dataclass
class SmartPyIf(SmartPyStatement):
    """If statement."""
    test: SmartPyExpression
    body: List[SmartPyStatement]
    orelse: List[SmartPyStatement]


@dataclass
class SmartPyFor(SmartPyStatement):
    """For loop statement."""
    target: str
    iter: SmartPyExpression
    body: List[SmartPyStatement]


@dataclass
class SmartPyWhile(SmartPyStatement):
    """While loop statement."""
    test: SmartPyExpression
    body: List[SmartPyStatement]


@dataclass
class SmartPyReturn(SmartPyStatement):
    """Return statement."""
    value: Optional[SmartPyExpression]


@dataclass
class SmartPyBreak(SmartPyStatement):
    """Break statement."""
    pass


@dataclass
class SmartPyContinue(SmartPyStatement):
    """Continue statement."""
    pass


# SmartPy specific statements
@dataclass
class SmartPyVerify(SmartPyStatement):
    """sp.verify() statement."""
    condition: SmartPyExpression
    message: Optional[SmartPyExpression] = None


@dataclass
class SmartPyFailwith(SmartPyStatement):
    """sp.failwith() statement."""
    value: SmartPyExpression


@dataclass
class SmartPyResult(SmartPyStatement):
    """sp.result() statement."""
    value: SmartPyExpression


@dataclass
class SmartPyTransfer(SmartPyStatement):
    """sp.transfer() statement."""
    arg: SmartPyExpression
    amount: SmartPyExpression
    destination: SmartPyExpression


@dataclass
class SmartPySetDelegate(SmartPyStatement):
    """sp.set_delegate() statement."""
    delegate: SmartPyExpression


@dataclass
class SmartPyCreateContract(SmartPyStatement):
    """sp.create_contract() statement."""
    contract: SmartPyExpression
    storage: SmartPyExpression
    amount: SmartPyExpression


# Control flow statements specific to SmartPy
@dataclass
class SmartPySpIf(SmartPyStatement):
    """sp.if statement."""
    condition: SmartPyExpression
    body: List[SmartPyStatement]
    else_body: Optional[List[SmartPyStatement]] = None


@dataclass
class SmartPySpFor(SmartPyStatement):
    """sp.for statement."""
    variable: str
    iterable: SmartPyExpression
    body: List[SmartPyStatement]


@dataclass
class SmartPySpWhile(SmartPyStatement):
    """sp.while statement."""
    condition: SmartPyExpression
    body: List[SmartPyStatement]


# Pattern matching
@dataclass
class SmartPyPattern(SmartPyNode):
    """Base class for patterns."""
    pass


@dataclass
class SmartPyWildcardPattern(SmartPyPattern):
    """Wildcard pattern (_)."""
    pass


@dataclass
class SmartPyVariablePattern(SmartPyPattern):
    """Variable pattern."""
    name: str


@dataclass
class SmartPyLiteralPattern(SmartPyPattern):
    """Literal pattern."""
    value: Any


@dataclass
class SmartPyRecordPattern(SmartPyPattern):
    """Record pattern."""
    fields: Dict[str, SmartPyPattern]


@dataclass
class SmartPyVariantPattern(SmartPyPattern):
    """Variant pattern."""
    constructor: str
    pattern: Optional[SmartPyPattern]


@dataclass
class SmartPyMatch(SmartPyStatement):
    """Match statement."""
    value: SmartPyExpression
    cases: List[tuple[SmartPyPattern, List[SmartPyStatement]]]


# Declaration nodes
@dataclass
class SmartPyDeclaration(SmartPyNode):
    """Base class for declarations."""
    pass


@dataclass
class SmartPyFunctionDef(SmartPyDeclaration):
    """Function definition."""
    name: str
    parameters: List[str]
    body: List[SmartPyStatement]
    decorators: List[str]
    return_type: Optional[SmartPyTypeAnnotation] = None


@dataclass
class SmartPyMethodDef(SmartPyDeclaration):
    """Method definition (part of a contract)."""
    name: str
    parameters: List[str]
    body: List[SmartPyStatement]
    decorators: List[str]
    is_entry_point: bool = False
    return_type: Optional[SmartPyTypeAnnotation] = None


@dataclass
class SmartPyContractDef(SmartPyDeclaration):
    """Smart contract definition."""
    name: str
    base_classes: List[str]
    methods: List[SmartPyMethodDef]
    entry_points: List[SmartPyMethodDef]
    init_method: Optional[SmartPyMethodDef]


@dataclass
class SmartPyImport(SmartPyDeclaration):
    """Import declaration."""
    module: str
    alias: Optional[str] = None
    names: Optional[List[str]] = None


@dataclass
class SmartPyVariableDef(SmartPyDeclaration):
    """Variable definition."""
    name: str
    value: SmartPyExpression
    type_hint: Optional[SmartPyTypeAnnotation] = None


# Test nodes
@dataclass
class SmartPyTestDef(SmartPyDeclaration):
    """Test definition."""
    name: str
    body: List[SmartPyStatement]


@dataclass
class SmartPyScenario(SmartPyStatement):
    """Test scenario."""
    name: str
    statements: List[SmartPyStatement]


@dataclass
class SmartPyContractCall(SmartPyStatement):
    """Contract method call in test."""
    contract: SmartPyExpression
    method: str
    args: List[SmartPyExpression]
    keywords: Dict[str, SmartPyExpression]
    run_params: Optional[Dict[str, Any]] = None


# Module and program structure
@dataclass
class SmartPyModule(SmartPyNode):
    """SmartPy module containing declarations."""
    declarations: List[SmartPyDeclaration]
    imports: List[SmartPyImport]


@dataclass
class SmartPyProgram(SmartPyNode):
    """Complete SmartPy program."""
    modules: List[SmartPyModule]
    main_module: SmartPyModule


# Storage initialization
@dataclass
class SmartPyStorageInit(SmartPyStatement):
    """Storage initialization statement: self.init(...)."""
    fields: Dict[str, SmartPyExpression]


# Special SmartPy constructs
@dataclass
class SmartPyRange(SmartPyExpression):
    """sp.range() expression."""
    start: SmartPyExpression
    stop: SmartPyExpression
    step: Optional[SmartPyExpression] = None


@dataclass
class SmartPyLen(SmartPyExpression):
    """sp.len() expression."""
    value: SmartPyExpression


@dataclass
class SmartPySize(SmartPyExpression):
    """sp.size() expression."""
    value: SmartPyExpression


@dataclass
class SmartPySum(SmartPyExpression):
    """sp.sum() expression."""
    iterable: SmartPyExpression


@dataclass
class SmartPyAbs(SmartPyExpression):
    """sp.abs() expression."""
    value: SmartPyExpression


@dataclass
class SmartPyMin(SmartPyExpression):
    """sp.min() expression."""
    values: List[SmartPyExpression]


@dataclass
class SmartPyMax(SmartPyExpression):
    """sp.max() expression."""
    values: List[SmartPyExpression]


@dataclass
class SmartPySlice(SmartPyExpression):
    """sp.slice() expression."""
    value: SmartPyExpression
    start: SmartPyExpression
    length: SmartPyExpression


@dataclass
class SmartPyConcat(SmartPyExpression):
    """sp.concat() expression."""
    values: List[SmartPyExpression]


@dataclass
class SmartPyPack(SmartPyExpression):
    """sp.pack() expression."""
    value: SmartPyExpression


@dataclass
class SmartPyUnpack(SmartPyExpression):
    """sp.unpack() expression."""
    value: SmartPyExpression
    type_hint: SmartPyTypeAnnotation


@dataclass
class SmartPyBlake2b(SmartPyExpression):
    """sp.blake2b() expression."""
    value: SmartPyExpression


@dataclass
class SmartPySha256(SmartPyExpression):
    """sp.sha256() expression."""
    value: SmartPyExpression


@dataclass
class SmartPySha512(SmartPyExpression):
    """sp.sha512() expression."""
    value: SmartPyExpression


@dataclass
class SmartPyCheckSignature(SmartPyExpression):
    """sp.check_signature() expression."""
    public_key: SmartPyExpression
    signature: SmartPyExpression
    message: SmartPyExpression


# Type constructors as expressions
@dataclass
class SmartPyTypeConstructor(SmartPyExpression):
    """Type constructor expression."""
    type_name: str
    value: SmartPyExpression


@dataclass
class SmartPyMapConstructor(SmartPyExpression):
    """Map constructor: sp.map()."""
    pairs: List[tuple[SmartPyExpression, SmartPyExpression]]
    key_type: Optional[SmartPyTypeAnnotation] = None
    value_type: Optional[SmartPyTypeAnnotation] = None


@dataclass
class SmartPyBigMapConstructor(SmartPyExpression):
    """BigMap constructor: sp.big_map()."""
    pairs: List[tuple[SmartPyExpression, SmartPyExpression]]
    key_type: Optional[SmartPyTypeAnnotation] = None
    value_type: Optional[SmartPyTypeAnnotation] = None


@dataclass
class SmartPySetConstructor(SmartPyExpression):
    """Set constructor: sp.set()."""
    elements: List[SmartPyExpression]
    element_type: Optional[SmartPyTypeAnnotation] = None


@dataclass
class SmartPyRecordConstructor(SmartPyExpression):
    """Record constructor: sp.record()."""
    fields: Dict[str, SmartPyExpression]


@dataclass 
class SmartPyVariantConstructor(SmartPyExpression):
    """Variant constructor: sp.variant()."""
    constructor: str
    value: Optional[SmartPyExpression] = None


# Data access patterns
@dataclass
class SmartPyDataAccess(SmartPyExpression):
    """self.data access expression."""
    pass


@dataclass
class SmartPyParamsAccess(SmartPyExpression):
    """params access expression."""
    pass 