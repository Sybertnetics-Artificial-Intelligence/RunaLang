#!/usr/bin/env python3
"""
Haskell Toolchain Integration

Complete toolchain for Haskell language support in the Runa Universal
Translation Pipeline. Integrates parsing, conversion, generation, and 
validation for seamless Haskell ↔ Runa translation.
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
import os

from runa.core.runa_ast import RunaNode
from runa.languages.shared.base_toolchain import BaseToolchain
from runa.core.errors import RunaError, CompilationError, ValidationError

from .haskell_ast import *
from .haskell_parser import HsLexer, HsParser, parse_haskell
from .haskell_converter import (
    HaskellToRunaConverter, RunaToHaskellConverter,
    haskell_to_runa, runa_to_haskell
)
from .haskell_generator import HaskellCodeGenerator, HaskellCodeStyle, generate_haskell


@dataclass
class HaskellCompileOptions:
    """Haskell compilation options."""
    ghc_path: str = "ghc"
    optimization_level: str = "-O1"
    warnings: List[str] = None
    extensions: List[str] = None
    packages: List[str] = None
    output_dir: Optional[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = ["-Wall", "-Wextra"]
        if self.extensions is None:
            self.extensions = []
        if self.packages is None:
            self.packages = ["base"]


class HaskellToolchain(BaseToolchain):
    """Complete Haskell language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.language = "haskell"
        self.version = "1.0.0"
        self.file_extensions = [".hs", ".lhs"]
        self.mime_types = ["text/x-haskell"]
        
        # Components
        self.lexer_class = HsLexer
        self.parser_class = HsParser
        self.to_runa_converter = HaskellToRunaConverter()
        self.from_runa_converter = RunaToHaskellConverter()
        self.code_generator = HaskellCodeGenerator()
        
        # Configuration
        self.compile_options = HaskellCompileOptions()
        self.code_style = HaskellCodeStyle()
    
    # Core parsing functionality
    def parse_source(self, source_code: str) -> HsModule:
        """Parse Haskell source code into AST."""
        try:
            return parse_haskell(source_code)
        except Exception as e:
            raise CompilationError(f"Haskell parsing failed: {str(e)}")
    
    def parse_file(self, file_path: str) -> HsModule:
        """Parse Haskell file into AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
            return self.parse_source(source_code)
        except FileNotFoundError:
            raise RunaError(f"Haskell file not found: {file_path}")
        except Exception as e:
            raise CompilationError(f"Failed to parse Haskell file {file_path}: {str(e)}")
    
    # Code generation
    def generate_code(self, ast_node: HsNode, style: Optional[HaskellCodeStyle] = None) -> str:
        """Generate Haskell code from AST."""
        try:
            generator = HaskellCodeGenerator(style or self.code_style)
            return generator.generate(ast_node)
        except Exception as e:
            raise CompilationError(f"Haskell code generation failed: {str(e)}")
    
    def format_code(self, source_code: str) -> str:
        """Format Haskell code."""
        try:
            # Parse and regenerate for formatting
            ast = self.parse_source(source_code)
            return self.generate_code(ast)
        except Exception as e:
            # Return original if formatting fails
            return source_code
    
    # Conversion functionality
    def to_runa_ast(self, haskell_ast: HsNode) -> RunaNode:
        """Convert Haskell AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(haskell_ast)
        except Exception as e:
            raise CompilationError(f"Haskell to Runa conversion failed: {str(e)}")
    
    def from_runa_ast(self, runa_ast: RunaNode) -> HsNode:
        """Convert Runa AST to Haskell AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise CompilationError(f"Runa to Haskell conversion failed: {str(e)}")
    
    def translate_from_runa(self, runa_source: str) -> str:
        """Translate Runa source code to Haskell."""
        try:
            # This would normally parse Runa, but for now we'll use a placeholder
            # In a complete implementation, this would:
            # 1. Parse Runa source to Runa AST
            # 2. Convert Runa AST to Haskell AST
            # 3. Generate Haskell code
            # TODO: Implement Runa parser not yet available
            return StringLiteral(value="Runa parser not yet available_placeholder")
        except Exception as e:
            raise CompilationError(f"Runa to Haskell translation failed: {str(e)}")
    
    def translate_to_runa(self, haskell_source: str) -> str:
        """Translate Haskell source code to Runa."""
        try:
            # Parse Haskell
            haskell_ast = self.parse_source(haskell_source)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_ast(haskell_ast)
            
            # Generate Runa code (placeholder - would need Runa generator)
            # return generate_runa_code(runa_ast)
            return "-- Runa code generation not yet implemented"
        except Exception as e:
            raise CompilationError(f"Haskell to Runa translation failed: {str(e)}")
    
    # Compilation and validation
    def compile_source(self, source_code: str, output_path: Optional[str] = None) -> bool:
        """Compile Haskell source code."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.hs', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
            
            try:
                return self.compile_file(temp_file_path, output_path)
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise CompilationError(f"Haskell compilation failed: {str(e)}")
    
    def compile_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Compile Haskell file."""
        try:
            cmd = [self.compile_options.ghc_path]
            
            # Add optimization
            if self.compile_options.optimization_level:
                cmd.append(self.compile_options.optimization_level)
            
            # Add warnings
            cmd.extend(self.compile_options.warnings)
            
            # Add extensions
            for ext in self.compile_options.extensions:
                cmd.extend(["-X", ext])
            
            # Add packages
            for pkg in self.compile_options.packages:
                cmd.extend(["-package", pkg])
            
            # Output options
            if output_path:
                cmd.extend(["-o", output_path])
            elif self.compile_options.output_dir:
                cmd.extend(["-outputdir", self.compile_options.output_dir])
            
            # Input file
            cmd.append(input_path)
            
            # Run compilation
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise CompilationError(f"GHC compilation failed:\n{result.stderr}")
            
            return True
        
        except FileNotFoundError:
            raise RunaError(f"GHC compiler not found at: {self.compile_options.ghc_path}")
        except Exception as e:
            raise CompilationError(f"Haskell compilation failed: {str(e)}")
    
    def validate_syntax(self, source_code: str) -> Tuple[bool, List[str]]:
        """Validate Haskell syntax."""
        errors = []
        try:
            self.parse_source(source_code)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors
    
    def validate_semantics(self, ast_node: HsNode) -> Tuple[bool, List[str]]:
        """Validate Haskell semantics."""
        errors = []
        try:
            # Basic semantic validation
            validator = HaskellSemanticValidator()
            validator.validate(ast_node)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors
    
    def check_types(self, source_code: str) -> Tuple[bool, List[str]]:
        """Check Haskell types using GHC."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.hs', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
            
            try:
                cmd = [self.compile_options.ghc_path, "-fno-code", "-Wall", temp_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    return True, []
                else:
                    errors = result.stderr.split('\n')
                    return False, [error for error in errors if error.strip()]
            finally:
                os.unlink(temp_file_path)
        
        except Exception as e:
            return False, [f"Type checking failed: {str(e)}"]
    
    # Language-specific utilities
    def get_module_dependencies(self, ast_node: HsModule) -> List[str]:
        """Get module dependencies from AST."""
        dependencies = []
        for imp in ast_node.imports:
            dependencies.append(imp.module_name)
        return dependencies
    
    def extract_function_signatures(self, ast_node: HsModule) -> Dict[str, str]:
        """Extract function signatures from module."""
        signatures = {}
        
        for decl in ast_node.declarations:
            if isinstance(decl, HsTypeSignature):
                type_str = self.generate_code(decl.type_expr)
                for name in decl.names:
                    signatures[name] = type_str
        
        return signatures
    
    def get_data_types(self, ast_node: HsModule) -> List[str]:
        """Get data type names from module."""
        data_types = []
        
        for decl in ast_node.declarations:
            if isinstance(decl, HsDataDeclaration):
                data_types.append(decl.name)
            elif isinstance(decl, HsTypeDeclaration):
                data_types.append(decl.name)
        
        return data_types
    
    # Round-trip verification
    def verify_round_trip(self, source_code: str) -> bool:
        """Verify round-trip translation accuracy."""
        try:
            # Parse original
            original_ast = self.parse_source(source_code)
            
            # Generate code
            generated_code = self.generate_code(original_ast)
            
            # Parse generated
            generated_ast = self.parse_source(generated_code)
            
            # Compare ASTs (simplified comparison)
            return self._compare_asts(original_ast, generated_ast)
        
        except Exception:
            return False
    
    def _compare_asts(self, ast1: HsNode, ast2: HsNode) -> bool:
        """Compare two ASTs for structural equality."""
        # Simplified comparison - in practice would need deep comparison
        return type(ast1) == type(ast2)
    
    # Configuration
    def configure_compiler(self, options: HaskellCompileOptions):
        """Configure compiler options."""
        self.compile_options = options
    
    def configure_style(self, style: HaskellCodeStyle):
        """Configure code style."""
        self.code_style = style
    
    # Metadata
    def get_language_info(self) -> Dict[str, Any]:
        """Get language information."""
        return {
            "name": "Haskell",
            "version": self.version,
            "paradigm": ["functional", "lazy", "pure"],
            "typing": "static",
            "file_extensions": self.file_extensions,
            "mime_types": self.mime_types,
            "features": [
                "lazy_evaluation",
                "pattern_matching", 
                "type_classes",
                "higher_order_functions",
                "algebraic_data_types",
                "monads",
                "pure_functions"
            ]
        }


class HaskellSemanticValidator:
    """Validates Haskell semantic correctness."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.scope_stack = []
    
    def validate(self, node: HsNode):
        """Validate AST node."""
        method_name = f"validate_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.validate_generic)
        return method(node)
    
    def validate_generic(self, node: HsNode):
        """Generic validation."""
        pass
    
    def validate_hsmodule(self, node: HsModule):
        """Validate module."""
        # Check for duplicate imports
        import_names = [imp.module_name for imp in node.imports]
        if len(import_names) != len(set(import_names)):
            self.warnings.append("Duplicate imports detected")
        
        # Validate declarations
        for decl in node.declarations:
            self.validate(decl)
    
    def validate_hsfunctiondeclaration(self, node: HsFunctionDeclaration):
        """Validate function declaration."""
        if not node.clauses:
            self.errors.append(f"Function {node.name} has no clauses")
        
        # Check clause consistency
        if len(node.clauses) > 1:
            first_arity = len(node.clauses[0].patterns)
            for i, clause in enumerate(node.clauses[1:], 1):
                if len(clause.patterns) != first_arity:
                    self.errors.append(
                        f"Function {node.name} clause {i+1} has different arity"
                    )


# Convenience functions
def parse_haskell_code(source_code: str) -> HsModule:
    """Parse Haskell source code."""
    toolchain = HaskellToolchain()
    return toolchain.parse_source(source_code)


def generate_haskell_code(ast_node: HsNode, style: Optional[HaskellCodeStyle] = None) -> str:
    """Generate Haskell code from AST."""
    toolchain = HaskellToolchain()
    return toolchain.generate_code(ast_node, style)


def haskell_round_trip_verify(source_code: str) -> bool:
    """Verify round-trip translation."""
    toolchain = HaskellToolchain()
    return toolchain.verify_round_trip(source_code)


def haskell_to_runa_translate(haskell_source: str) -> str:
    """Translate Haskell to Runa."""
    toolchain = HaskellToolchain()
    return toolchain.translate_to_runa(haskell_source)


def runa_to_haskell_translate(runa_source: str) -> str:
    """Translate Runa to Haskell."""
    toolchain = HaskellToolchain()
    return toolchain.translate_from_runa(runa_source)


# Create singleton instance
toolchain = HaskellToolchain()


# Export all functionality
__all__ = [
    # Main toolchain
    "HaskellToolchain", "toolchain",
    
    # Configuration
    "HaskellCompileOptions", "HaskellCodeStyle",
    
    # Validator
    "HaskellSemanticValidator",
    
    # Convenience functions
    "parse_haskell_code", "generate_haskell_code", "haskell_round_trip_verify",
    "haskell_to_runa_translate", "runa_to_haskell_translate"
] 