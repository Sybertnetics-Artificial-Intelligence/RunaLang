"""
LIGO Language Support

High-level smart contract language for Tezos blockchain that compiles to optimized Michelson.
Supports both JsLIGO (JavaScript-like) and CameLIGO (OCaml-like) syntaxes.

Features:
- Two syntax variants: JsLIGO and CameLIGO
- Strong type system with inference
- Functional programming constructs
- Pattern matching and variants
- Native Tezos operations
- Gas optimization
- Formal verification support

Usage:
    from runa.languages.tier4.ligo import toolchain
    
    # Parse LIGO code
    ast = toolchain.parse_string(ligo_code)
    
    # Convert between syntaxes
    cameligo_code = toolchain.translate_code(jsligo_code, LIGOSyntax.CAMELIGO)
    
    # Compile to Michelson
    result = toolchain.compile_contract("contract.jsligo")
    
    # Analyze gas usage
    analysis = toolchain.analyze_gas_usage(ligo_code)
"""

from typing import Dict, List, Optional, Union, Any
from pathlib import Path

# Import core components
from .ligo_ast import *
from .ligo_parser import LIGOParser, LIGOLexer
from .ligo_converter import LIGOToRunaConverter, RunaToLIGOConverter, ligo_to_runa, runa_to_ligo
from .ligo_generator import LIGOGenerator, generate_ligo_code, format_ligo_code
from .ligo_toolchain import LIGOToolchain

# Import main toolchain instance
from .ligo_toolchain import toolchain


class LIGOLanguageProxy:
    """
    Proxy class providing convenient access to all LIGO functionality.
    Follows the standardized interface pattern for Runa language support.
    """
    
    def __init__(self):
        self._toolchain = None
        self._jsligo_toolchain = None
        self._cameligo_toolchain = None
    
    @property
    def toolchain(self) -> LIGOToolchain:
        """Get the default LIGO toolchain (JsLIGO syntax)."""
        if self._toolchain is None:
            self._toolchain = LIGOToolchain(LIGOSyntax.JSLIGO)
        return self._toolchain
    
    @property
    def jsligo(self) -> LIGOToolchain:
        """Get JsLIGO-specific toolchain."""
        if self._jsligo_toolchain is None:
            self._jsligo_toolchain = LIGOToolchain(LIGOSyntax.JSLIGO)
        return self._jsligo_toolchain
    
    @property
    def cameligo(self) -> LIGOToolchain:
        """Get CameLIGO-specific toolchain."""
        if self._cameligo_toolchain is None:
            self._cameligo_toolchain = LIGOToolchain(LIGOSyntax.CAMELIGO)
        return self._cameligo_toolchain
    
    # Core parsing and generation
    def parse(self, code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO, 
              filename: Optional[str] = None) -> LIGOProgram:
        """Parse LIGO code with specified syntax."""
        tc = self._get_toolchain(syntax)
        return tc.parse_string(code, filename)
    
    def parse_file(self, file_path: Union[str, Path], 
                   syntax: Optional[LIGOSyntax] = None) -> LIGOProgram:
        """Parse LIGO file, auto-detecting syntax if not specified."""
        path = Path(file_path)
        
        if syntax is None:
            # Auto-detect syntax from file extension
            if path.suffix == '.jsligo':
                syntax = LIGOSyntax.JSLIGO
            elif path.suffix == '.mligo':
                syntax = LIGOSyntax.CAMELIGO
            else:
                syntax = LIGOSyntax.JSLIGO  # Default
        
        tc = self._get_toolchain(syntax)
        return tc.parse_file(file_path)
    
    def generate(self, ast: LIGONode, syntax: LIGOSyntax = LIGOSyntax.JSLIGO,
                format_output: bool = True) -> str:
        """Generate LIGO code from AST."""
        tc = self._get_toolchain(syntax)
        return tc.generate_code(ast, format_output)
    
    def format_code(self, code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> str:
        """Format LIGO code with proper indentation."""
        return format_ligo_code(code, syntax)
    
    # AST conversion
    def to_runa(self, ligo_ast: LIGONode, 
                syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> Any:  # RunaNode
        """Convert LIGO AST to Runa AST."""
        tc = self._get_toolchain(syntax)
        return tc.to_runa_ast(ligo_ast)
    
    def from_runa(self, runa_ast: Any,  # RunaNode
                  syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> LIGONode:
        """Convert Runa AST to LIGO AST."""
        tc = self._get_toolchain(syntax)
        return tc.from_runa_ast(runa_ast)
    
    # Code translation
    def translate_syntax(self, code: str, from_syntax: LIGOSyntax, 
                        to_syntax: LIGOSyntax) -> str:
        """Translate between JsLIGO and CameLIGO syntaxes."""
        tc = self._get_toolchain(from_syntax)
        return tc.translate_code(code, to_syntax)
    
    def jsligo_to_cameligo(self, jsligo_code: str) -> str:
        """Convert JsLIGO code to CameLIGO."""
        return self.translate_syntax(jsligo_code, LIGOSyntax.JSLIGO, LIGOSyntax.CAMELIGO)
    
    def cameligo_to_jsligo(self, cameligo_code: str) -> str:
        """Convert CameLIGO code to JsLIGO."""
        return self.translate_syntax(cameligo_code, LIGOSyntax.CAMELIGO, LIGOSyntax.JSLIGO)
    
    # Validation and analysis
    def validate(self, code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> Any:  # ValidationResult
        """Validate LIGO syntax and semantics."""
        tc = self._get_toolchain(syntax)
        return tc.validate_syntax(code)
    
    def analyze_gas(self, code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> Dict[str, Any]:
        """Analyze gas usage and provide optimization suggestions."""
        tc = self._get_toolchain(syntax)
        return tc.analyze_gas_usage(code)
    
    def optimize(self, code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> str:
        """Apply optimizations to LIGO code."""
        tc = self._get_toolchain(syntax)
        return tc.optimize_code(code)
    
    # Compilation and deployment
    def compile_contract(self, source_file: Union[str, Path],
                        output_dir: Optional[Union[str, Path]] = None,
                        syntax: Optional[LIGOSyntax] = None) -> Dict[str, Any]:
        """Compile LIGO contract to Michelson."""
        if syntax is None:
            # Auto-detect from file extension
            path = Path(source_file)
            syntax = LIGOSyntax.JSLIGO if path.suffix == '.jsligo' else LIGOSyntax.CAMELIGO
        
        tc = self._get_toolchain(syntax)
        return tc.compile_contract(source_file, output_dir)
    
    def generate_deployment_script(self, contract_file: Union[str, Path],
                                 storage_params: Dict[str, Any],
                                 syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> str:
        """Generate deployment script for Tezos."""
        tc = self._get_toolchain(syntax)
        return tc.generate_deployment_script(contract_file, storage_params)
    
    # Testing
    def run_tests(self, test_file: Union[str, Path],
                  syntax: Optional[LIGOSyntax] = None) -> Any:  # TestResult
        """Run LIGO tests."""
        if syntax is None:
            # Auto-detect from file extension
            path = Path(test_file)
            syntax = LIGOSyntax.JSLIGO if path.suffix == '.jsligo' else LIGOSyntax.CAMELIGO
        
        tc = self._get_toolchain(syntax)
        return tc.run_tests(test_file)
    
    # Utility methods
    def get_syntax_info(self, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> Dict[str, Any]:
        """Get information about syntax features."""
        tc = self._get_toolchain(syntax)
        return tc.get_syntax_info()
    
    def detect_syntax(self, code: str) -> LIGOSyntax:
        """Detect LIGO syntax from code content."""
        # Simple heuristics
        if 'const ' in code and '=>' in code and '{' in code:
            return LIGOSyntax.JSLIGO
        elif 'let ' in code and ' -> ' in code:
            return LIGOSyntax.CAMELIGO
        else:
            return LIGOSyntax.JSLIGO  # Default
    
    def _get_toolchain(self, syntax: LIGOSyntax) -> LIGOToolchain:
        """Get appropriate toolchain for syntax."""
        if syntax == LIGOSyntax.JSLIGO:
            return self.jsligo
        else:
            return self.cameligo
    
    # AST node creation helpers
    def create_literal(self, value: Any, literal_type: Optional[str] = None) -> LIGOLiteral:
        """Create a LIGO literal node."""
        return LIGOLiteral(value=value, literal_type=literal_type)
    
    def create_identifier(self, name: str) -> LIGOIdentifier:
        """Create a LIGO identifier node."""
        return LIGOIdentifier(name=name)
    
    def create_function_call(self, function: LIGONode, 
                           arguments: List[LIGONode]) -> LIGOFunctionCall:
        """Create a LIGO function call node."""
        return LIGOFunctionCall(function=function, arguments=arguments)
    
    def create_binary_op(self, left: LIGONode, operator: str, 
                        right: LIGONode) -> LIGOBinaryOp:
        """Create a LIGO binary operation node."""
        return LIGOBinaryOp(left=left, operator=operator, right=right)
    
    def create_record_type(self, fields: List[Tuple[str, LIGOType]]) -> LIGORecordType:
        """Create a LIGO record type."""
        field_nodes = []
        for name, type_annotation in fields:
            field_nodes.append(LIGORecordField(name=name, type_annotation=type_annotation))
        return LIGORecordType(fields=field_nodes)
    
    def create_function_decl(self, name: str, parameters: List[LIGOParameter],
                           return_type: Optional[LIGOType] = None,
                           body: List[LIGONode] = None) -> LIGOFunctionDecl:
        """Create a LIGO function declaration."""
        return LIGOFunctionDecl(
            name=name,
            parameters=parameters,
            return_type=return_type,
            body=body or [],
            visibility=LIGOVisibility.PUBLIC
        )
    
    # Smart contract specific helpers
    def create_contract(self, storage_type: Optional[LIGOType] = None,
                       entrypoints: List[LIGOEntrypoint] = None) -> LIGOContractDecl:
        """Create a LIGO contract declaration."""
        return LIGOContractDecl(
            name="Contract",
            storage_type=storage_type,
            entrypoints=entrypoints or []
        )
    
    def create_entrypoint(self, name: str, param_type: Optional[LIGOType] = None,
                         body: List[LIGONode] = None) -> LIGOEntrypoint:
        """Create a LIGO entrypoint."""
        return LIGOEntrypoint(
            name=name,
            param_type=param_type,
            body=body or []
        )


# Create the main proxy instance
language = LIGOLanguageProxy()

# Convenience exports for direct access
parse = language.parse
parse_file = language.parse_file
generate = language.generate
format_code = language.format_code
validate = language.validate
compile_contract = language.compile_contract

# Export main components
__all__ = [
    # Main interface
    "language",
    "toolchain",
    
    # Convenience functions
    "parse",
    "parse_file", 
    "generate",
    "format_code",
    "validate",
    "compile_contract",
    
    # Core classes
    "LIGOToolchain",
    "LIGOParser",
    "LIGOLexer",
    "LIGOGenerator",
    "LIGOToRunaConverter",
    "RunaToLIGOConverter",
    
    # AST nodes
    "LIGONode",
    "LIGOProgram",
    "LIGOFunctionDecl",
    "LIGOVariableDecl",
    "LIGOTypeDecl",
    "LIGOContractDecl",
    "LIGOEntrypoint",
    "LIGOLiteral",
    "LIGOIdentifier",
    "LIGOBinaryOp",
    "LIGOUnaryOp",
    "LIGOFunctionCall",
    "LIGOConditional",
    "LIGOLambda",
    
    # Types
    "LIGOType",
    "LIGOPrimitiveType",
    "LIGORecordType", 
    "LIGOVariantType",
    "LIGOListType",
    "LIGOMapType",
    "LIGOOptionType",
    "LIGOTupleType",
    "LIGOFunctionType",
    
    # Enums
    "LIGOSyntax",
    "LIGOVisibility",
    
    # Utility functions
    "ligo_to_runa",
    "runa_to_ligo", 
    "generate_ligo_code",
    "format_ligo_code"
]

# Metadata
__version__ = "1.0.0"
__author__ = "Runa Development Team"
__description__ = "LIGO smart contract language support for Runa"
__language__ = "LIGO"
__tier__ = 4
__syntax_variants__ = ["JsLIGO", "CameLIGO"]
__file_extensions__ = [".jsligo", ".mligo"]
__blockchain__ = "Tezos"
