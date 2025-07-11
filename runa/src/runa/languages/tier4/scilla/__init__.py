"""
Scilla Language Implementation for Runa Universal Translation Pipeline

Scilla is a smart contract programming language developed for the Zilliqa blockchain.
This implementation provides complete support for functional programming constructs,
smart contract development, and type-safe code generation.

Language Features:
- Functional programming paradigm
- Pattern matching and algebraic data types
- Type safety with dependent types
- Gas-bounded computation model
- Smart contract structure (fields, transitions, procedures)
- Built-in formal verification support
- Message passing and event system

This module serves as the main entry point for all Scilla language operations
within the Runa ecosystem, providing seamless integration with the universal
translation pipeline.

Usage:
    from runa.languages.tier4.scilla import ScillaToolchain
    
    toolchain = ScillaToolchain()
    ast = toolchain.parse(scilla_code)
    runa_ast = toolchain.to_runa(ast) 
    regenerated = toolchain.generate(ast)
"""

# Core AST and language constructs
from .scilla_ast import (
    # Base node
    ScillaNode,
    
    # Enums
    ScillaPrimitiveType,
    ScillaFieldType,
    ScillaVisibility,
    ScillaTransitionType,
    
    # Type nodes
    ScillaPrimitive,
    ScillaMapType,
    ScillaListType,
    ScillaOptionType,
    ScillaPairType,
    ScillaCustomType,
    ScillaFunctionType,
    ScillaType,
    
    # Literal nodes
    ScillaIntLiteral,
    ScillaStringLiteral,
    ScillaBoolLiteral,
    ScillaByStrLiteral,
    ScillaAddressLiteral,
    
    # Pattern nodes
    ScillaWildcardPattern,
    ScillaVariablePattern,
    ScillaConstructorPattern,
    ScillaLiteralPattern,
    ScillaPattern,
    
    # Expression nodes
    ScillaIdentifier,
    ScillaLiteral,
    ScillaApplication,
    ScillaBuiltinCall,
    ScillaLet,
    ScillaMatch,
    ScillaConstructor,
    ScillaMapAccess,
    ScillaFieldAccess,
    ScillaMessageConstruction,
    ScillaEventConstruction,
    ScillaLambda,
    ScillaTFun,
    ScillaTApp,
    ScillaExpression,
    
    # Statement nodes
    ScillaLoad,
    ScillaStore,
    ScillaBind,
    ScillaMapUpdate,
    ScillaMapDelete,
    ScillaSend,
    ScillaEvent,
    ScillaThrow,
    ScillaAccept,
    ScillaMatchStmt,
    ScillaStatement,
    
    # Declaration nodes
    ScillaTypeParameter,
    ScillaParameter,
    ScillaLibraryFunction,
    ScillaADTConstructor,
    ScillaADTDeclaration,
    ScillaFieldDeclaration,
    ScillaTransition,
    ScillaProcedure,
    
    # Top-level nodes
    ScillaImport,
    ScillaLibrary,
    ScillaContract,
    ScillaProgram,
    
    # Utility classes
    ScillaContractMetadata,
    ScillaAnnotation,
    
    # Helper functions
    create_scilla_builtin_call,
    create_scilla_map_type,
    create_scilla_uint_type,
)

# Parser and lexer
from .scilla_parser import (
    ScillaTokenType,
    ScillaToken,
    ScillaLexer,
    ScillaParser,
    parse_scilla,
)

# AST converters
from .scilla_converter import (
    ScillaToRunaConverter,
    RunaToScillaConverter,
)

# Code generator
from .scilla_generator import (
    ScillaCodeGenerator,
    generate_scilla_code,
    format_scilla_code,
)

# Integrated toolchain
from .scilla_toolchain import (
    ScillaCompilationResult,
    ScillaDeploymentConfig,
    ScillaValidationResult,
    ScillaToolchain,
    create_scilla_toolchain,
    parse_scilla_file,
    compile_scilla_contract,
    validate_scilla_contract,
)

# Primary toolchain instance - main entry point
toolchain = ScillaToolchain()

# Proxy methods for common operations
def parse(source_code: str, file_path: str = None):
    """Parse Scilla source code into AST
    
    Args:
        source_code: Scilla source code string
        file_path: Optional file path for error reporting
        
    Returns:
        ScillaProgram: Parsed AST
        
    Raises:
        SyntaxError: If parsing fails
    """
    return toolchain.parse(source_code, file_path)


def generate(ast, format_output: bool = True, indent_size: int = 2):
    """Generate Scilla source code from AST
    
    Args:
        ast: ScillaProgram AST node
        format_output: Whether to format the output
        indent_size: Number of spaces for indentation
        
    Returns:
        str: Generated Scilla source code
        
    Raises:
        RuntimeError: If generation fails
    """
    return toolchain.generate(ast, format_output, indent_size)


def to_runa(scilla_ast):
    """Convert Scilla AST to Runa AST
    
    Args:
        scilla_ast: ScillaProgram AST node
        
    Returns:
        Node: Runa AST representation
        
    Raises:
        RuntimeError: If conversion fails
    """
    return toolchain.to_runa(scilla_ast)


def from_runa(runa_ast):
    """Convert Runa AST to Scilla AST
    
    Args:
        runa_ast: Runa Node AST
        
    Returns:
        ScillaProgram: Scilla AST representation
        
    Raises:
        RuntimeError: If conversion fails
    """
    return toolchain.from_runa(runa_ast)


def compile_contract(source_code: str, output_dir: str = None, optimization_level: int = 1):
    """Compile Scilla smart contract
    
    Args:
        source_code: Scilla source code
        output_dir: Optional output directory for artifacts
        optimization_level: Optimization level (0-3)
        
    Returns:
        ScillaCompilationResult: Compilation results
    """
    return toolchain.compile(source_code, output_dir, optimization_level)


def validate_contract(source_code: str):
    """Validate Scilla smart contract
    
    Args:
        source_code: Scilla source code
        
    Returns:
        ScillaValidationResult: Validation results with issues and suggestions
    """
    ast = toolchain.parse(source_code)
    return toolchain.validate_contract(ast)


def deploy_contract(contract_code: str, config: ScillaDeploymentConfig):
    """Deploy Scilla contract to Zilliqa network
    
    Args:
        contract_code: Scilla contract source code
        config: Deployment configuration
        
    Returns:
        dict: Deployment result with contract address and transaction details
    """
    return toolchain.deploy_contract(contract_code, config)


def create_contract_template(template_name: str, parameters: dict):
    """Create Scilla contract from template
    
    Args:
        template_name: Template name ('token', 'crowdsale', 'auction', etc.)
        parameters: Template parameters
        
    Returns:
        str: Generated contract source code
        
    Raises:
        ValueError: If template is unknown
    """
    return toolchain.create_contract_template(template_name, parameters)


def analyze_gas_usage(source_code: str):
    """Analyze gas usage patterns in Scilla contract
    
    Args:
        source_code: Scilla source code
        
    Returns:
        dict: Gas analysis with cost estimates and optimization suggestions
    """
    return toolchain.analyze_gas_usage(source_code)


# Language metadata
__language__ = "scilla"
__version__ = "1.0.0"
__author__ = "Runa Development Team"
__description__ = "Scilla smart contract language implementation for Zilliqa blockchain"

# Supported features
__features__ = [
    "smart_contracts",
    "functional_programming", 
    "pattern_matching",
    "type_safety",
    "formal_verification",
    "gas_optimization",
    "event_system",
    "message_passing",
    "algebraic_data_types",
    "dependent_types",
    "immutable_programming",
    "contract_deployment",
    "abi_generation",
    "bytecode_compilation"
]

# Export version for external use
__all__ = [
    # Core classes
    'ScillaNode', 'ScillaProgram', 'ScillaContract', 'ScillaTransition',
    'ScillaExpression', 'ScillaStatement', 'ScillaType',
    
    # Toolchain
    'ScillaToolchain', 'toolchain',
    
    # Main functions
    'parse', 'generate', 'to_runa', 'from_runa',
    'compile_contract', 'validate_contract', 'deploy_contract',
    'create_contract_template', 'analyze_gas_usage',
    
    # Results and configs
    'ScillaCompilationResult', 'ScillaValidationResult', 'ScillaDeploymentConfig',
    
    # Utilities
    'parse_scilla_file', 'compile_scilla_contract', 'validate_scilla_contract',
    
    # Metadata
    '__language__', '__version__', '__features__'
]
