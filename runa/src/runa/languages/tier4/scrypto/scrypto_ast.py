"""
Abstract Syntax Tree definitions for Scrypto - Radix DLT's asset-oriented smart contract language.

Scrypto is built on Rust and introduces asset-oriented programming concepts including:
- Components (smart contracts) instantiated from Blueprints
- Native Resources (tokens, NFTs) managed by Radix Engine
- Buckets and Vaults for asset handling
- Badge-based authentication
- SBOR encoding for data serialization
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class ScryptoASTNodeType(Enum):
    """Types of nodes in Scrypto AST"""
    # Core language constructs
    PROGRAM = "program"
    BLUEPRINT = "blueprint"
    COMPONENT = "component"
    PACKAGE = "package"
    
    # Asset-oriented constructs
    RESOURCE = "resource"
    BUCKET = "bucket"
    VAULT = "vault"
    BADGE = "badge"
    
    # Functions and methods
    FUNCTION = "function"
    METHOD = "method"
    INSTANTIATE = "instantiate"
    
    # Types and data
    STRUCT = "struct"
    ENUM = "enum"
    TYPE_ANNOTATION = "type_annotation"
    
    # Expressions and statements
    EXPRESSION = "expression"
    STATEMENT = "statement"
    BLOCK = "block"
    
    # Rust-based constructs
    IMPL_BLOCK = "impl_block"
    TRAIT_DEF = "trait_def"
    USE_STATEMENT = "use_statement"
    
    # Scrypto-specific
    RADIX_ENGINE_CALL = "radix_engine_call"
    SBOR_ENCODING = "sbor_encoding"
    COMPONENT_STATE = "component_state"


class ScryptoResourceType(Enum):
    """Types of resources in Scrypto"""
    FUNGIBLE = "fungible"
    NON_FUNGIBLE = "non_fungible"
    BADGE = "badge"


class ScryptoAccessRule(Enum):
    """Access rules for Scrypto components and resources"""
    ALLOW_ALL = "allow_all"
    DENY_ALL = "deny_all"
    REQUIRE_BADGE = "require_badge"
    REQUIRE_SIGNATURE = "require_signature"


@dataclass
class ScryptoASTNode:
    """Base class for all Scrypto AST nodes"""
    node_type: ScryptoASTNodeType
    line: int = 0
    column: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScryptoProgram(ScryptoASTNode):
    """Root node representing a complete Scrypto program/package"""
    packages: List['ScryptoPackage'] = field(default_factory=list)
    use_statements: List['ScryptoUseStatement'] = field(default_factory=list)
    cargo_toml: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.PROGRAM


@dataclass
class ScryptoPackage(ScryptoASTNode):
    """Scrypto package containing multiple blueprints"""
    name: str
    version: str
    blueprints: List['ScryptoBlueprint'] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.PACKAGE


@dataclass
class ScryptoBlueprint(ScryptoASTNode):
    """Blueprint definition - template for creating components"""
    name: str
    state_struct: 'ScryptoStruct'
    methods: List['ScryptoMethod'] = field(default_factory=list)
    instantiate_functions: List['ScryptoFunction'] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    doc_comment: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.BLUEPRINT


@dataclass
class ScryptoComponent(ScryptoASTNode):
    """Component instance with state and behavior"""
    blueprint_name: str
    component_address: Optional[str] = None
    state: Dict[str, Any] = field(default_factory=dict)
    vaults: List['ScryptoVault'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.COMPONENT


@dataclass
class ScryptoResource(ScryptoASTNode):
    """Resource definition (tokens, NFTs, badges)"""
    name: str
    resource_type: ScryptoResourceType
    total_supply: Optional[str] = None
    divisibility: Optional[int] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    access_rules: Dict[str, ScryptoAccessRule] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.RESOURCE


@dataclass
class ScryptoBucket(ScryptoASTNode):
    """Temporary container for resources during transaction execution"""
    name: str
    resource_address: str
    amount: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.BUCKET


@dataclass
class ScryptoVault(ScryptoASTNode):
    """Persistent storage for resources within components"""
    name: str
    resource_address: str
    access_rules: Dict[str, ScryptoAccessRule] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.VAULT


@dataclass
class ScryptoBadge(ScryptoASTNode):
    """Badge resource for authentication and authorization"""
    name: str
    badge_type: str
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.BADGE


@dataclass
class ScryptoFunction(ScryptoASTNode):
    """Function definition"""
    name: str
    parameters: List['ScryptoParameter'] = field(default_factory=list)
    return_type: Optional['ScryptoType'] = None
    body: 'ScryptoBlock'
    visibility: str = "pub"
    is_instantiate: bool = False
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.FUNCTION


@dataclass
class ScryptoMethod(ScryptoASTNode):
    """Method definition for blueprint components"""
    name: str
    parameters: List['ScryptoParameter'] = field(default_factory=list)
    return_type: Optional['ScryptoType'] = None
    body: 'ScryptoBlock'
    visibility: str = "pub"
    is_mutable: bool = False
    access_rule: Optional[ScryptoAccessRule] = None
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.METHOD


@dataclass
class ScryptoParameter(ScryptoASTNode):
    """Function/method parameter"""
    name: str
    param_type: 'ScryptoType'
    is_mutable: bool = False
    default_value: Optional['ScryptoExpression'] = None


@dataclass
class ScryptoType(ScryptoASTNode):
    """Type annotation"""
    name: str
    generics: List['ScryptoType'] = field(default_factory=list)
    is_reference: bool = False
    is_mutable: bool = False
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.TYPE_ANNOTATION


@dataclass
class ScryptoStruct(ScryptoASTNode):
    """Struct definition"""
    name: str
    fields: List['ScryptoStructField'] = field(default_factory=list)
    derives: List[str] = field(default_factory=list)
    doc_comment: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.STRUCT


@dataclass
class ScryptoStructField(ScryptoASTNode):
    """Struct field definition"""
    name: str
    field_type: ScryptoType
    visibility: str = "pub"
    doc_comment: Optional[str] = None


@dataclass
class ScryptoEnum(ScryptoASTNode):
    """Enum definition"""
    name: str
    variants: List['ScryptoEnumVariant'] = field(default_factory=list)
    derives: List[str] = field(default_factory=list)
    doc_comment: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.ENUM


@dataclass
class ScryptoEnumVariant(ScryptoASTNode):
    """Enum variant"""
    name: str
    fields: List[ScryptoType] = field(default_factory=list)
    discriminant: Optional[int] = None


@dataclass
class ScryptoBlock(ScryptoASTNode):
    """Block of statements"""
    statements: List['ScryptoStatement'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.BLOCK


@dataclass
class ScryptoStatement(ScryptoASTNode):
    """Base class for statements"""
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.STATEMENT


@dataclass
class ScryptoLetStatement(ScryptoStatement):
    """Variable declaration/assignment"""
    name: str
    type_annotation: Optional[ScryptoType] = None
    value: Optional['ScryptoExpression'] = None
    is_mutable: bool = False


@dataclass
class ScryptoReturnStatement(ScryptoStatement):
    """Return statement"""
    value: Optional['ScryptoExpression'] = None


@dataclass
class ScryptoExpressionStatement(ScryptoStatement):
    """Expression used as statement"""
    expression: 'ScryptoExpression'


@dataclass
class ScryptoExpression(ScryptoASTNode):
    """Base class for expressions"""
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.EXPRESSION


@dataclass
class ScryptoLiteralExpression(ScryptoExpression):
    """Literal value expression"""
    value: Any
    literal_type: str  # "string", "integer", "decimal", "boolean", etc.


@dataclass
class ScryptoIdentifierExpression(ScryptoExpression):
    """Variable or identifier reference"""
    name: str


@dataclass
class ScryptoMethodCallExpression(ScryptoExpression):
    """Method call expression"""
    receiver: ScryptoExpression
    method_name: str
    arguments: List[ScryptoExpression] = field(default_factory=list)


@dataclass
class ScryptoFunctionCallExpression(ScryptoExpression):
    """Function call expression"""
    function_name: str
    arguments: List[ScryptoExpression] = field(default_factory=list)


@dataclass
class ScryptoRadixEngineCallExpression(ScryptoExpression):
    """Radix Engine specific API call"""
    api_name: str  # e.g., "ResourceManager", "ComponentManager"
    method_name: str
    arguments: List[ScryptoExpression] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = ScryptoASTNodeType.RADIX_ENGINE_CALL


@dataclass
class ScryptoResourceManagerCall(ScryptoExpression):
    """Resource Manager API calls"""
    operation: str  # "create_fungible_resource", "create_non_fungible_resource", etc.
    parameters: Dict[str, ScryptoExpression] = field(default_factory=dict)


@dataclass
class ScryptoBucketExpression(ScryptoExpression):
    """Bucket manipulation expression"""
    operation: str  # "take", "put", "amount", "resource_address"
    bucket: ScryptoExpression
    amount: Optional[ScryptoExpression] = None


@dataclass
class ScryptoVaultExpression(ScryptoExpression):
    """Vault manipulation expression"""
    operation: str  # "take", "put", "amount", "resource_address"
    vault: ScryptoExpression
    amount: Optional[ScryptoExpression] = None


@dataclass
class ScryptoComponentCallExpression(ScryptoExpression):
    """Component method call"""
    component_address: str
    method_name: str
    arguments: List[ScryptoExpression] = field(default_factory=list)


@dataclass
class ScryptoStructExpression(ScryptoExpression):
    """Struct instantiation"""
    struct_name: str
    fields: Dict[str, ScryptoExpression] = field(default_factory=dict)


@dataclass
class ScryptoFieldAccessExpression(ScryptoExpression):
    """Field access expression"""
    receiver: ScryptoExpression
    field_name: str


@dataclass
class ScryptoTupleExpression(ScryptoExpression):
    """Tuple expression"""
    elements: List[ScryptoExpression] = field(default_factory=list)


@dataclass
class ScryptoArrayExpression(ScryptoExpression):
    """Array/vector expression"""
    elements: List[ScryptoExpression] = field(default_factory=list)


@dataclass
class ScryptoIfExpression(ScryptoExpression):
    """If expression"""
    condition: ScryptoExpression
    then_block: ScryptoBlock
    else_block: Optional[ScryptoBlock] = None


@dataclass
class ScryptoMatchExpression(ScryptoExpression):
    """Match expression"""
    expression: ScryptoExpression
    arms: List['ScryptoMatchArm'] = field(default_factory=list)


@dataclass
class ScryptoMatchArm(ScryptoASTNode):
    """Match arm"""
    pattern: str
    guard: Optional[ScryptoExpression] = None
    body: ScryptoExpression


@dataclass
class ScryptoImplBlock(ScryptoASTNode):
    """Implementation block"""
    target_type: str
    trait_name: Optional[str] = None
    methods: List[ScryptoMethod] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.IMPL_BLOCK


@dataclass
class ScryptoUseStatement(ScryptoASTNode):
    """Use/import statement"""
    path: str
    alias: Optional[str] = None
    is_glob: bool = False
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.USE_STATEMENT


@dataclass
class ScryptoAttribute(ScryptoASTNode):
    """Attribute annotation (e.g., #[derive(ScryptoEncode, ScryptoDecode)])"""
    name: str
    arguments: List[str] = field(default_factory=list)


@dataclass
class ScryptoMacroCall(ScryptoExpression):
    """Macro call expression"""
    macro_name: str
    arguments: List[str] = field(default_factory=list)


@dataclass
class ScryptoComponentState(ScryptoASTNode):
    """Component state representation"""
    fields: Dict[str, Any] = field(default_factory=dict)
    vaults: Dict[str, str] = field(default_factory=dict)  # vault_name -> resource_address
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.COMPONENT_STATE


@dataclass
class ScryptoSborEncoding(ScryptoASTNode):
    """SBOR encoding specification"""
    data: Any
    encoding_type: str = "ScryptoEncode"
    
    def __post_init__(self):
        self.node_type = ScryptoASTNodeType.SBOR_ENCODING


# Built-in Scrypto types and constants
SCRYPTO_BUILTIN_TYPES = {
    # Primitive types
    "bool", "u8", "u16", "u32", "u64", "u128", "i8", "i16", "i32", "i64", "i128",
    "f32", "f64", "char", "str", "String",
    
    # Scrypto-specific types
    "ComponentAddress", "ResourceAddress", "PackageAddress", "GlobalAddress",
    "Bucket", "Vault", "Proof", "NonFungibleLocalId", "NonFungibleGlobalId",
    "Decimal", "PreciseDecimal", "Hash", "PublicKey", "Signature",
    
    # Collections
    "Vec", "HashMap", "BTreeMap", "HashSet", "BTreeSet", "Option", "Result",
    
    # Radix Engine types
    "ResourceManager", "ComponentManager", "PackageManager", "AuthZone",
    "Clock", "EpochManager", "Worktop"
}

SCRYPTO_BUILTIN_FUNCTIONS = {
    # Resource creation
    "create_fungible_resource", "create_non_fungible_resource",
    "create_fungible_resource_with_initial_supply",
    
    # Component management
    "instantiate_component", "get_component_address",
    
    # Bucket operations
    "take_from_worktop", "put_into_worktop", "create_bucket",
    
    # Vault operations
    "create_vault", "put", "take", "take_all",
    
    # Authentication
    "create_proof", "create_proof_from_auth_zone", "push_to_auth_zone",
    
    # Utilities
    "info!", "debug!", "error!", "assert!", "panic!"
}

class ScryptoAST:
    """
    Main AST class for Scrypto language representation.
    
    Provides utilities for working with Scrypto AST nodes and
    validating asset-oriented programming constructs.
    """
    
    def __init__(self, root: ScryptoProgram):
        self.root = root
    
    def get_all_blueprints(self) -> List[ScryptoBlueprint]:
        """Get all blueprints across all packages"""
        blueprints = []
        for package in self.root.packages:
            blueprints.extend(package.blueprints)
        return blueprints
    
    def get_all_resources(self) -> List[ScryptoResource]:
        """Get all resource definitions"""
        resources = []
        
        def collect_resources(node):
            if isinstance(node, ScryptoResource):
                resources.append(node)
            elif hasattr(node, '__dict__'):
                for value in node.__dict__.values():
                    if isinstance(value, list):
                        for item in value:
                            if hasattr(item, '__dict__'):
                                collect_resources(item)
                    elif hasattr(value, '__dict__'):
                        collect_resources(value)
        
        collect_resources(self.root)
        return resources
    
    def validate_asset_flow(self) -> List[str]:
        """Validate asset flow consistency (buckets/vaults)"""
        errors = []
        # Implementation would check bucket/vault operations
        # for consistency and asset conservation
        return errors
    
    def get_component_dependencies(self) -> Dict[str, List[str]]:
        """Get component dependencies for deployment ordering"""
        dependencies = {}
        # Implementation would analyze component instantiation dependencies
        return dependencies 