"""
Scilla Abstract Syntax Tree (AST) Implementation

Scilla is a smart contract programming language developed for Zilliqa blockchain.
This module provides comprehensive AST nodes for Scilla's functional programming
paradigm with emphasis on safety, gas-bounded execution, and formal verification.

Key Features:
- Type safety with dependent types
- Pattern matching and algebraic data types  
- Immutable state transitions
- Gas-bounded computation
- Built-in library support
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum, auto


class ScillaPrimitiveType(Enum):
    """Scilla primitive types"""
    UINT32 = "Uint32"
    UINT64 = "Uint64" 
    UINT128 = "Uint128"
    UINT256 = "Uint256"
    INT32 = "Int32"
    INT64 = "Int64"
    INT128 = "Int128"
    INT256 = "Int256"
    STRING = "String"
    BYSTR = "ByStr"
    BYSTRX = "ByStrX"
    BNUM = "BNum"
    MESSAGE = "Message"
    EVENT = "Event"
    EXCEPTION = "Exception"


class ScillaFieldType(Enum):
    """Scilla contract field mutability"""
    IMMUTABLE = "immutable"
    MUTABLE = "mutable"


class ScillaVisibility(Enum):
    """Scilla contract element visibility"""
    PUBLIC = "public"
    PRIVATE = "private"


class ScillaTransitionType(Enum):
    """Scilla transition types"""
    TRANSITION = "transition"
    PROCEDURE = "procedure"


@dataclass
class ScillaNode:
    """Base class for all Scilla AST nodes"""
    line: Optional[int] = None
    column: Optional[int] = None
    
    def accept(self, visitor):
        """Visitor pattern implementation"""
        method_name = f"visit_{self.__class__.__name__}"
        visitor_method = getattr(visitor, method_name, None)
        if visitor_method:
            return visitor_method(self)
        else:
            return getattr(visitor, "generic_visit", lambda x: None)(self)


# Type Nodes
@dataclass
class ScillaPrimitive(ScillaNode):
    """Primitive type node"""
    type: ScillaPrimitiveType


@dataclass
class ScillaMapType(ScillaNode):
    """Map type: Map KeyType ValueType"""
    key_type: 'ScillaType'
    value_type: 'ScillaType'


@dataclass
class ScillaListType(ScillaNode):
    """List type: List ElementType"""
    element_type: 'ScillaType'


@dataclass
class ScillaOptionType(ScillaNode):
    """Option type: Option ElementType"""
    element_type: 'ScillaType'


@dataclass
class ScillaPairType(ScillaNode):
    """Pair type: Pair FirstType SecondType"""
    first_type: 'ScillaType'
    second_type: 'ScillaType'


@dataclass
class ScillaCustomType(ScillaNode):
    """Custom/user-defined type"""
    name: str
    type_args: List['ScillaType'] = field(default_factory=list)


@dataclass
class ScillaFunctionType(ScillaNode):
    """Function type: arg_types -> return_type"""
    arg_types: List['ScillaType']
    return_type: 'ScillaType'


ScillaType = Union[
    ScillaPrimitive, ScillaMapType, ScillaListType, ScillaOptionType,
    ScillaPairType, ScillaCustomType, ScillaFunctionType
]


# Literal Nodes
@dataclass
class ScillaIntLiteral(ScillaNode):
    """Integer literal"""
    value: str
    type_hint: Optional[ScillaPrimitiveType] = None


@dataclass
class ScillaStringLiteral(ScillaNode):
    """String literal"""
    value: str


@dataclass
class ScillaBoolLiteral(ScillaNode):
    """Boolean literal"""
    value: bool


@dataclass
class ScillaByStrLiteral(ScillaNode):
    """Byte string literal"""
    value: str  # Hex string
    width: Optional[int] = None  # For ByStrX


@dataclass
class ScillaAddressLiteral(ScillaNode):
    """Address literal (0x...)"""
    value: str


# Pattern Nodes
@dataclass
class ScillaWildcardPattern(ScillaNode):
    """Wildcard pattern: _"""
    pass


@dataclass
class ScillaVariablePattern(ScillaNode):
    """Variable pattern"""
    name: str


@dataclass
class ScillaConstructorPattern(ScillaNode):
    """Constructor pattern: Cons args"""
    constructor: str
    args: List['ScillaPattern']


@dataclass
class ScillaLiteralPattern(ScillaNode):
    """Literal pattern"""
    literal: Union[ScillaIntLiteral, ScillaStringLiteral, ScillaBoolLiteral]


ScillaPattern = Union[
    ScillaWildcardPattern, ScillaVariablePattern, 
    ScillaConstructorPattern, ScillaLiteralPattern
]


# Expression Nodes
@dataclass
class ScillaIdentifier(ScillaNode):
    """Variable identifier"""
    name: str


@dataclass
class ScillaLiteral(ScillaNode):
    """Literal expression"""
    literal: Union[ScillaIntLiteral, ScillaStringLiteral, ScillaBoolLiteral, 
                   ScillaByStrLiteral, ScillaAddressLiteral]


@dataclass
class ScillaApplication(ScillaNode):
    """Function application: func args"""
    function: 'ScillaExpression'
    args: List['ScillaExpression']


@dataclass
class ScillaBuiltinCall(ScillaNode):
    """Built-in function call"""
    builtin: str
    args: List['ScillaExpression']
    type_args: List[ScillaType] = field(default_factory=list)


@dataclass
class ScillaLet(ScillaNode):
    """Let binding: let x = e1 in e2"""
    bindings: List[tuple]  # [(pattern, expr), ...]
    body: 'ScillaExpression'


@dataclass
class ScillaMatch(ScillaNode):
    """Pattern matching: match expr with pattern => expr | ..."""
    expr: 'ScillaExpression'
    branches: List[tuple]  # [(pattern, expr), ...]


@dataclass
class ScillaConstructor(ScillaNode):
    """Constructor application: {Cons arg1 arg2}"""
    name: str
    args: List['ScillaExpression']


@dataclass
class ScillaMapAccess(ScillaNode):
    """Map access: map[key]"""
    map_expr: 'ScillaExpression'
    key: 'ScillaExpression'


@dataclass
class ScillaFieldAccess(ScillaNode):
    """Field access for contracts"""
    field: str


@dataclass
class ScillaMessageConstruction(ScillaNode):
    """Message construction: {_tag: ".."; _recipient: ...; ...}"""
    fields: Dict[str, 'ScillaExpression']


@dataclass
class ScillaEventConstruction(ScillaNode):
    """Event construction"""
    name: str
    params: Dict[str, 'ScillaExpression']


@dataclass
class ScillaLambda(ScillaNode):
    """Lambda expression: fun (x : T) => expr"""
    params: List[tuple]  # [(name, type), ...]
    body: 'ScillaExpression'


@dataclass
class ScillaTFun(ScillaNode):
    """Type abstraction: tfun 'A => expr"""
    type_vars: List[str]
    body: 'ScillaExpression'


@dataclass
class ScillaTApp(ScillaNode):
    """Type application: expr @T"""
    expr: 'ScillaExpression'
    type_args: List[ScillaType]


ScillaExpression = Union[
    ScillaIdentifier, ScillaLiteral, ScillaApplication, ScillaBuiltinCall,
    ScillaLet, ScillaMatch, ScillaConstructor, ScillaMapAccess, ScillaFieldAccess,
    ScillaMessageConstruction, ScillaEventConstruction, ScillaLambda, 
    ScillaTFun, ScillaTApp
]


# Statement Nodes
@dataclass
class ScillaLoad(ScillaNode):
    """Load statement: x <- f"""
    var: str
    field: str


@dataclass
class ScillaStore(ScillaNode):
    """Store statement: f := expr"""
    field: str
    value: ScillaExpression


@dataclass
class ScillaBind(ScillaNode):
    """Bind statement: x = expr"""
    var: str
    value: ScillaExpression


@dataclass
class ScillaMapUpdate(ScillaNode):
    """Map update: map[key] := value"""
    map_name: str
    key: ScillaExpression
    value: ScillaExpression


@dataclass
class ScillaMapDelete(ScillaNode):
    """Map delete: delete map[key]"""
    map_name: str
    key: ScillaExpression


@dataclass
class ScillaSend(ScillaNode):
    """Send statement: send msgs"""
    messages: ScillaExpression


@dataclass
class ScillaEvent(ScillaNode):
    """Event emission: event e"""
    event: ScillaExpression


@dataclass
class ScillaThrow(ScillaNode):
    """Throw exception: throw exc"""
    exception: ScillaExpression


@dataclass
class ScillaAccept(ScillaNode):
    """Accept payment"""
    pass


@dataclass
class ScillaMatchStmt(ScillaNode):
    """Match statement"""
    expr: ScillaExpression
    branches: List[tuple]  # [(pattern, statements), ...]


ScillaStatement = Union[
    ScillaLoad, ScillaStore, ScillaBind, ScillaMapUpdate, ScillaMapDelete,
    ScillaSend, ScillaEvent, ScillaThrow, ScillaAccept, ScillaMatchStmt
]


# Declaration Nodes
@dataclass
class ScillaTypeParameter(ScillaNode):
    """Type parameter: 'A"""
    name: str


@dataclass
class ScillaParameter(ScillaNode):
    """Function/transition parameter"""
    name: str
    type: ScillaType


@dataclass
class ScillaLibraryFunction(ScillaNode):
    """Library function definition"""
    name: str
    type_params: List[ScillaTypeParameter]
    params: List[ScillaParameter]
    return_type: ScillaType
    body: ScillaExpression


@dataclass
class ScillaADTConstructor(ScillaNode):
    """ADT constructor"""
    name: str
    arg_types: List[ScillaType]


@dataclass
class ScillaADTDeclaration(ScillaNode):
    """Algebraic Data Type declaration"""
    name: str
    type_params: List[ScillaTypeParameter]
    constructors: List[ScillaADTConstructor]


@dataclass
class ScillaFieldDeclaration(ScillaNode):
    """Contract field declaration"""
    name: str
    type: ScillaType
    mutability: ScillaFieldType
    init_value: Optional[ScillaExpression] = None


@dataclass
class ScillaTransition(ScillaNode):
    """Contract transition"""
    name: str
    params: List[ScillaParameter]
    statements: List[ScillaStatement]
    transition_type: ScillaTransitionType = ScillaTransitionType.TRANSITION


@dataclass
class ScillaProcedure(ScillaNode):
    """Contract procedure"""
    name: str
    params: List[ScillaParameter]
    statements: List[ScillaStatement]


# Top-level Nodes
@dataclass
class ScillaImport(ScillaNode):
    """Import statement"""
    module: str
    items: Optional[List[str]] = None  # None means import all


@dataclass
class ScillaLibrary(ScillaNode):
    """Library declaration"""
    name: str
    imports: List[ScillaImport]
    type_declarations: List[ScillaADTDeclaration]
    function_declarations: List[ScillaLibraryFunction]


@dataclass
class ScillaContract(ScillaNode):
    """Contract declaration"""
    name: str
    library: Optional[ScillaLibrary]
    imports: List[ScillaImport]
    type_params: List[ScillaTypeParameter]
    immutable_params: List[ScillaParameter]
    fields: List[ScillaFieldDeclaration]
    transitions: List[ScillaTransition]
    procedures: List[ScillaProcedure]


@dataclass
class ScillaProgram(ScillaNode):
    """Complete Scilla program"""
    scilla_version: str
    libraries: List[ScillaLibrary]
    contract: ScillaContract
    
    
# Utility Classes
@dataclass
class ScillaContractMetadata(ScillaNode):
    """Contract metadata for deployment"""
    gas_limit: Optional[int] = None
    gas_price: Optional[int] = None
    version: Optional[str] = None
    author: Optional[str] = None


@dataclass
class ScillaAnnotation(ScillaNode):
    """Annotation for formal verification"""
    name: str
    properties: Dict[str, Any]


# Expression Utilities
def create_scilla_builtin_call(name: str, args: List[ScillaExpression], 
                              type_args: List[ScillaType] = None) -> ScillaBuiltinCall:
    """Helper to create built-in function calls"""
    return ScillaBuiltinCall(
        builtin=name,
        args=args,
        type_args=type_args or []
    )


def create_scilla_map_type(key_type: ScillaType, value_type: ScillaType) -> ScillaMapType:
    """Helper to create map types"""
    return ScillaMapType(key_type=key_type, value_type=value_type)


def create_scilla_uint_type(width: int) -> ScillaPrimitive:
    """Helper to create uint types"""
    type_map = {
        32: ScillaPrimitiveType.UINT32,
        64: ScillaPrimitiveType.UINT64,
        128: ScillaPrimitiveType.UINT128,
        256: ScillaPrimitiveType.UINT256
    }
    return ScillaPrimitive(type=type_map[width]) 