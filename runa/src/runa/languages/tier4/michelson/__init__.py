"""
Michelson Language Support for Runa Universal Translation Pipeline.

This module provides comprehensive support for the Michelson stack-based smart contract 
language used on the Tezos blockchain. Michelson is designed for formal verification
and features a strong type system with functional programming elements.

Features:
- Complete AST representation for stack operations
- Lexical analysis and parsing
- Bidirectional conversion with Runa AST
- Code generation with optimization
- Smart contract validation and testing
- Tezos blockchain integration
- Gas estimation and storage analysis

Author: Runa Development Team
License: MIT
"""

# Core imports
from .michelson_ast import *
from .michelson_parser import parse_michelson, parse_michelson_expression, MichelsonLexer, MichelsonParser
from .michelson_converter import michelson_to_runa, runa_to_michelson, MichelsonToRunaConverter, RunaToMichelsonConverter
from .michelson_generator import generate_michelson, generate_michelson_compact, MichelsonGenerator
from .michelson_toolchain import *

from typing import Dict, List, Optional, Any, Union
from ...runa_ast import RunaASTNode

# Language metadata
LANGUAGE_NAME = "Michelson"
LANGUAGE_VERSION = "1.0.0"
FILE_EXTENSIONS = [".tz", ".mtz"]
MIME_TYPES = ["text/x-michelson"]

# Language features
FEATURES = {
    "paradigm": "stack-based",
    "typing": "static",
    "platform": "tezos",
    "formal_verification": True,
    "gas_metering": True,
    "immutable": True,
    "blockchain": True,
    "smart_contracts": True
}

# Global toolchain instance
_toolchain: Optional[MichelsonToolchain] = None


def get_toolchain() -> MichelsonToolchain:
    """Get the global Michelson toolchain instance."""
    global _toolchain
    if _toolchain is None:
        _toolchain = MichelsonToolchain()
    return _toolchain


def set_toolchain_config(**kwargs):
    """Configure the global toolchain."""
    global _toolchain
    _toolchain = MichelsonToolchain(**kwargs)


# ============================================================================
# Standard Tier 1 Interface Implementation
# ============================================================================

def parse(source: str, **kwargs) -> MichelsonContract:
    """
    Parse Michelson source code into AST.
    
    Args:
        source: Michelson source code
        **kwargs: Additional parser options
        
    Returns:
        MichelsonContract: Parsed contract AST
        
    Raises:
        MichelsonToolchainError: If parsing fails
        
    Example:
        >>> contract = parse('parameter unit; storage unit; code { DROP; UNIT; NIL operation; PAIR }')
        >>> print(f"Contract has {len(contract.code.instructions)} instructions")
    """
    return get_toolchain().parse_from_source(source)


def parse_file(file_path: str, **kwargs) -> MichelsonContract:
    """
    Parse Michelson source file into AST.
    
    Args:
        file_path: Path to Michelson source file
        **kwargs: Additional parser options
        
    Returns:
        MichelsonContract: Parsed contract AST
        
    Raises:
        MichelsonToolchainError: If file not found or parsing fails
    """
    return get_toolchain().parse_from_file(file_path)


def generate(ast_node: MichelsonContract, **kwargs) -> str:
    """
    Generate Michelson source code from AST.
    
    Args:
        ast_node: Michelson contract AST
        **kwargs: Generation options (indent_size, optimize, add_comments)
        
    Returns:
        str: Generated Michelson source code
        
    Raises:
        MichelsonToolchainError: If generation fails
        
    Example:
        >>> source = generate(contract, indent_size=4, optimize=True)
        >>> print(source)
    """
    return get_toolchain().generate_source(ast_node)


def to_runa(michelson_ast: MichelsonContract) -> RunaASTNode:
    """
    Convert Michelson AST to Runa AST.
    
    Args:
        michelson_ast: Michelson contract AST
        
    Returns:
        RunaASTNode: Equivalent Runa AST
        
    Raises:
        MichelsonToolchainError: If conversion fails
    """
    return get_toolchain().convert_to_runa(michelson_ast)


def from_runa(runa_ast: RunaASTNode) -> MichelsonContract:
    """
    Convert Runa AST to Michelson AST.
    
    Args:
        runa_ast: Runa AST node
        
    Returns:
        MichelsonContract: Equivalent Michelson contract AST
        
    Raises:
        MichelsonToolchainError: If conversion fails
    """
    return get_toolchain().convert_from_runa(runa_ast)


def validate(ast_node: MichelsonContract, **kwargs) -> ValidationResult:
    """
    Validate Michelson contract AST.
    
    Args:
        ast_node: Michelson contract AST to validate
        **kwargs: Validation options (storage_value, etc.)
        
    Returns:
        ValidationResult: Validation results with errors/warnings
        
    Example:
        >>> result = validate(contract, storage_value="Unit")
        >>> if result.is_valid:
        ...     print(f"Contract valid, estimated gas: {result.gas_estimate}")
        >>> else:
        ...     print(f"Validation errors: {result.errors}")
    """
    storage_value = kwargs.get('storage_value')
    return get_toolchain().validate_contract(ast_node, storage_value)


def optimize(ast_node: MichelsonContract, **kwargs) -> MichelsonContract:
    """
    Apply optimizations to Michelson contract.
    
    Args:
        ast_node: Michelson contract AST to optimize
        **kwargs: Optimization options
        
    Returns:
        MichelsonContract: Optimized contract AST
    """
    return get_toolchain().optimize_contract(ast_node)


def format_code(source: str, **kwargs) -> str:
    """
    Format Michelson source code.
    
    Args:
        source: Michelson source code to format
        **kwargs: Formatting options (indent_size, etc.)
        
    Returns:
        str: Formatted Michelson source code
    """
    # Parse and regenerate for consistent formatting
    contract = parse(source)
    return generate(contract, **kwargs)


def get_language_info() -> Dict[str, Any]:
    """
    Get information about the Michelson language.
    
    Returns:
        Dict containing language metadata and features
    """
    return {
        "name": LANGUAGE_NAME,
        "version": LANGUAGE_VERSION,
        "extensions": FILE_EXTENSIONS,
        "mime_types": MIME_TYPES,
        "features": FEATURES,
        "description": "Stack-based smart contract language for Tezos blockchain",
        "paradigm": "functional, stack-based",
        "typing": "static, strong",
        "platform": "Tezos blockchain",
        "use_cases": [
            "Smart contracts",
            "DeFi protocols", 
            "NFT contracts",
            "Token contracts",
            "Governance contracts"
        ]
    }


# ============================================================================
# Extended Michelson-Specific Interface
# ============================================================================

def create_contract(parameter_type: str, storage_type: str, 
                   code_instructions: List[str]) -> MichelsonContract:
    """
    Create a Michelson contract from components.
    
    Args:
        parameter_type: Parameter type string
        storage_type: Storage type string  
        code_instructions: List of instruction strings
        
    Returns:
        MichelsonContract: Created contract AST
        
    Example:
        >>> contract = create_contract(
        ...     "unit", 
        ...     "int",
        ...     ["DROP", "PUSH int 42", "NIL operation", "PAIR"]
        ... )
    """
    # Build contract source and parse
    instructions = " ; ".join(code_instructions)
    source = f"""
parameter {parameter_type} ;
storage {storage_type} ;
code {{ {instructions} }}
"""
    return parse(source.strip())


def test_contract(contract: MichelsonContract, test_cases: List[Dict[str, Any]]) -> List[TestResult]:
    """
    Test Michelson contract with multiple test cases.
    
    Args:
        contract: Contract to test
        test_cases: List of test case dictionaries
        
    Returns:
        List[TestResult]: Test results
        
    Example:
        >>> results = test_contract(contract, [
        ...     {"name": "test1", "parameter": "Unit", "storage": "0", "expected": "42"}
        ... ])
    """
    return get_toolchain().test_contract(contract, test_cases)


def deploy_contract(contract: MichelsonContract, initial_storage: str,
                   sender_account: str, amount: str = "0") -> DeploymentResult:
    """
    Deploy contract to Tezos network.
    
    Args:
        contract: Contract to deploy
        initial_storage: Initial storage value
        sender_account: Sender account alias
        amount: Amount to transfer with deployment
        
    Returns:
        DeploymentResult: Deployment result
        
    Example:
        >>> result = deploy_contract(contract, "0", "alice", "1")
        >>> if result.success:
        ...     print(f"Deployed at: {result.contract_address}")
    """
    return get_toolchain().deploy_contract(contract, initial_storage, sender_account, amount)


def get_contract_info(contract: MichelsonContract) -> Dict[str, Any]:
    """
    Get detailed information about a contract.
    
    Args:
        contract: Contract to analyze
        
    Returns:
        Dict with contract information and analysis
    """
    return get_toolchain().get_contract_info(contract)


def create_deployment_package(contract: MichelsonContract, initial_storage: str,
                             metadata: Optional[ContractMetadata] = None) -> Dict[str, Any]:
    """
    Create a deployment package for the contract.
    
    Args:
        contract: Contract to package
        initial_storage: Initial storage value
        metadata: Optional contract metadata
        
    Returns:
        Dict containing deployment package
    """
    return get_toolchain().create_deployment_package(contract, initial_storage, metadata)


def analyze_gas_usage(contract: MichelsonContract, parameter: str = "Unit", 
                     storage: str = "Unit") -> Dict[str, Any]:
    """
    Analyze gas usage for contract execution.
    
    Args:
        contract: Contract to analyze
        parameter: Parameter value for analysis
        storage: Storage value for analysis
        
    Returns:
        Dict with gas analysis results
    """
    validation = validate(contract, storage_value=storage)
    
    return {
        "estimated_gas": validation.gas_estimate,
        "gas_limit_exceeded": (validation.gas_estimate or 0) > get_toolchain().settings['max_gas_limit'],
        "max_gas_limit": get_toolchain().settings['max_gas_limit'],
        "optimization_recommended": (validation.gas_estimate or 0) > 100000,
        "warnings": validation.warnings
    }


def compile_project(project_dir: str) -> Dict[str, Any]:
    """
    Compile an entire Michelson project.
    
    Args:
        project_dir: Directory containing Michelson files
        
    Returns:
        Dict with compilation results
    """
    return get_toolchain().compile_project(project_dir)


def lint_contract(contract: MichelsonContract) -> List[str]:
    """
    Lint a Michelson contract for best practices.
    
    Args:
        contract: Contract to lint
        
    Returns:
        List of linting suggestions
    """
    suggestions = []
    
    # Check for optimization opportunities
    opportunities = get_toolchain()._find_optimization_opportunities(contract)
    suggestions.extend([f"Optimization: {opp}" for opp in opportunities])
    
    # Check contract complexity
    complexity = get_toolchain()._calculate_complexity(contract)
    if complexity > 100:
        suggestions.append(f"High complexity score ({complexity}): Consider breaking into smaller contracts")
    
    # Check for common patterns
    instructions = contract.code.instructions
    
    # Look for missing error handling
    has_failwith = any(instr.instruction == MichelsonInstruction.FAILWITH for instr in instructions)
    if not has_failwith:
        suggestions.append("Consider adding error handling with FAILWITH instructions")
    
    # Look for gas-expensive operations
    expensive_ops = [MichelsonInstruction.BLAKE2B, MichelsonInstruction.SHA256, 
                     MichelsonInstruction.SHA512, MichelsonInstruction.PAIRING_CHECK]
    
    for instr in instructions:
        if instr.instruction in expensive_ops:
            suggestions.append(f"Gas-expensive operation detected: {instr.instruction.value}")
    
    return suggestions


def extract_entrypoints(contract: MichelsonContract) -> List[str]:
    """
    Extract entrypoint information from contract.
    
    Args:
        contract: Contract to analyze
        
    Returns:
        List of entrypoint names
    """
    # Simplified entrypoint extraction
    # In practice, would need more sophisticated analysis
    entrypoints = ["default"]
    
    # Look for IF_LEFT patterns which often indicate multiple entrypoints
    instructions = contract.code.instructions
    for instr in instructions:
        if instr.instruction == MichelsonInstruction.IF_LEFT:
            entrypoints.extend(["left_branch", "right_branch"])
    
    return entrypoints


def get_storage_schema(contract: MichelsonContract) -> Dict[str, Any]:
    """
    Get storage schema information.
    
    Args:
        contract: Contract to analyze
        
    Returns:
        Dict with storage schema details
    """
    storage_type = contract.storage_type
    
    def analyze_type(type_node: MichelsonType_Node) -> Dict[str, Any]:
        result = {
            "type": type_node.type_name.value,
            "args": []
        }
        
        if type_node.args:
            result["args"] = [analyze_type(arg) for arg in type_node.args]
        
        return result
    
    return {
        "storage_type": analyze_type(storage_type),
        "complexity": len(storage_type.args) if storage_type.args else 0,
        "contains_maps": any(arg.type_name in [MichelsonType.MAP, MichelsonType.BIG_MAP] 
                            for arg in (storage_type.args or [])),
        "estimated_size": get_toolchain().validate_contract(contract).storage_size
    }


# ============================================================================
# Convenience Functions and Aliases
# ============================================================================

# Aliases for common operations
compile_from_source = parse
compile_from_file = parse_file
generate_code = generate
convert_to_runa = to_runa
convert_from_runa = from_runa

# Type aliases for easier imports
MichelsonAST = MichelsonContract
MichelsonNode = MichelsonASTNode

__all__ = [
    # Core classes
    'MichelsonContract', 'MichelsonInstruction_Node', 'MichelsonType_Node',
    'MichelsonLiteral', 'MichelsonSequence', 'MichelsonToolchain',
    
    # Parser classes
    'MichelsonLexer', 'MichelsonParser',
    
    # Converter classes  
    'MichelsonToRunaConverter', 'RunaToMichelsonConverter',
    
    # Generator classes
    'MichelsonGenerator',
    
    # Result classes
    'ValidationResult', 'TestResult', 'DeploymentResult', 'ContractMetadata',
    
    # Standard interface functions
    'parse', 'parse_file', 'generate', 'to_runa', 'from_runa',
    'validate', 'optimize', 'format_code', 'get_language_info',
    
    # Extended interface functions
    'create_contract', 'test_contract', 'deploy_contract', 'get_contract_info',
    'create_deployment_package', 'analyze_gas_usage', 'compile_project',
    'lint_contract', 'extract_entrypoints', 'get_storage_schema',
    
    # Toolchain functions
    'get_toolchain', 'set_toolchain_config',
    
    # Convenience functions
    'parse_michelson', 'parse_michelson_expression', 'generate_michelson',
    'generate_michelson_compact', 'michelson_to_runa', 'runa_to_michelson',
    
    # Aliases
    'compile_from_source', 'compile_from_file', 'generate_code',
    'convert_to_runa', 'convert_from_runa', 'MichelsonAST', 'MichelsonNode',
    
    # Constants
    'LANGUAGE_NAME', 'LANGUAGE_VERSION', 'FILE_EXTENSIONS', 'MIME_TYPES', 'FEATURES'
]
