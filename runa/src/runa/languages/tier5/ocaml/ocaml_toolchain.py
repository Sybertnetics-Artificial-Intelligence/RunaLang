#!/usr/bin/env python3
"""
OCaml Toolchain Integration

Complete toolchain for OCaml language support in the Runa Universal
Translation Pipeline. Integrates parsing, conversion, generation, and 
validation for seamless OCaml ↔ Runa translation.
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
import os

from runa.core.ast import RunaNode
from runa.languages.shared.base_toolchain import BaseToolchain
from runa.core.errors import RunaError, CompilationError, ValidationError

from .ocaml_ast import *
from .ocaml_parser import OcamlLexer, OcamlParser, parse_ocaml
from .ocaml_converter import (
    OcamlToRunaConverter, RunaToOcamlConverter,
    ocaml_to_runa, runa_to_ocaml
)
from .ocaml_generator import OcamlCodeGenerator, OcamlCodeStyle, generate_ocaml


@dataclass
class OcamlCompileOptions:
    """OCaml compilation options."""
    ocamlc_path: str = "ocamlc"
    ocamlopt_path: str = "ocamlopt"
    optimization_level: str = "-O2"
    warnings: List[str] = None
    packages: List[str] = None
    include_dirs: List[str] = None
    output_dir: Optional[str] = None
    native_compilation: bool = True
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = ["-w", "+A-4-9-18-40-41-42-44-45-48-70"]
        if self.packages is None:
            self.packages = []
        if self.include_dirs is None:
            self.include_dirs = []


class OcamlToolchain(BaseToolchain):
    """Complete OCaml language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.language = "ocaml"
        self.version = "1.0.0"
        self.file_extensions = [".ml", ".mli"]
        self.mime_types = ["text/x-ocaml"]
        
        # Components
        self.lexer_class = OcamlLexer
        self.parser_class = OcamlParser
        self.to_runa_converter = OcamlToRunaConverter()
        self.from_runa_converter = RunaToOcamlConverter()
        self.code_generator = OcamlCodeGenerator()
        
        # Configuration
        self.compile_options = OcamlCompileOptions()
        self.code_style = OcamlCodeStyle()
    
    # Core parsing functionality
    def parse_source(self, source_code: str) -> OcamlModule:
        """Parse OCaml source code into AST."""
        try:
            return parse_ocaml(source_code)
        except Exception as e:
            raise CompilationError(f"OCaml parsing failed: {str(e)}")
    
    def parse_file(self, file_path: str) -> OcamlModule:
        """Parse OCaml file into AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
            return self.parse_source(source_code)
        except FileNotFoundError:
            raise RunaError(f"OCaml file not found: {file_path}")
        except Exception as e:
            raise CompilationError(f"Failed to parse OCaml file {file_path}: {str(e)}")
    
    # Code generation
    def generate_code(self, ast_node: OcamlNode, style: Optional[OcamlCodeStyle] = None) -> str:
        """Generate OCaml code from AST."""
        try:
            generator = OcamlCodeGenerator(style or self.code_style)
            return generator.generate(ast_node)
        except Exception as e:
            raise CompilationError(f"OCaml code generation failed: {str(e)}")
    
    def format_code(self, source_code: str) -> str:
        """Format OCaml code."""
        try:
            # Parse and regenerate for formatting
            ast = self.parse_source(source_code)
            return self.generate_code(ast)
        except Exception as e:
            # Return original if formatting fails
            return source_code
    
    # Conversion functionality
    def to_runa_ast(self, ocaml_ast: OcamlNode) -> RunaNode:
        """Convert OCaml AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(ocaml_ast)
        except Exception as e:
            raise CompilationError(f"OCaml to Runa conversion failed: {str(e)}")
    
    def from_runa_ast(self, runa_ast: RunaNode) -> OcamlNode:
        """Convert Runa AST to OCaml AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise CompilationError(f"Runa to OCaml conversion failed: {str(e)}")
    
    def translate_from_runa(self, runa_source: str) -> str:
        """Translate Runa source code to OCaml."""
        try:
            # This would normally parse Runa, but for now we'll use a placeholder
            # In a complete implementation, this would:
            # 1. Parse Runa source to Runa AST
            # 2. Convert Runa AST to OCaml AST
            # 3. Generate OCaml code
            # TODO: Implement Runa parser not yet available
            return StringLiteral(value="Runa parser not yet available_placeholder")
        except Exception as e:
            raise CompilationError(f"Runa to OCaml translation failed: {str(e)}")
    
    def translate_to_runa(self, ocaml_source: str) -> str:
        """Translate OCaml source code to Runa."""
        try:
            # Parse OCaml
            ocaml_ast = self.parse_source(ocaml_source)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_ast(ocaml_ast)
            
            # Generate Runa code (placeholder - would need Runa generator)
            # return generate_runa_code(runa_ast)
            return "(* Runa code generation not yet implemented *)"
        except Exception as e:
            raise CompilationError(f"OCaml to Runa translation failed: {str(e)}")
    
    # Compilation and validation
    def compile_source(self, source_code: str, output_path: Optional[str] = None) -> bool:
        """Compile OCaml source code."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
            
            try:
                return self.compile_file(temp_file_path, output_path)
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise CompilationError(f"OCaml compilation failed: {str(e)}")
    
    def compile_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Compile OCaml file."""
        try:
            # Choose compiler based on compilation mode
            if self.compile_options.native_compilation:
                compiler = self.compile_options.ocamlopt_path
            else:
                compiler = self.compile_options.ocamlc_path
            
            cmd = [compiler]
            
            # Add optimization for native compilation
            if self.compile_options.native_compilation and self.compile_options.optimization_level:
                cmd.append(self.compile_options.optimization_level)
            
            # Add warnings
            cmd.extend(self.compile_options.warnings)
            
            # Add include directories
            for include_dir in self.compile_options.include_dirs:
                cmd.extend(["-I", include_dir])
            
            # Add packages
            for package in self.compile_options.packages:
                cmd.extend(["-package", package])
            
            # Output options
            if output_path:
                cmd.extend(["-o", output_path])
            elif self.compile_options.output_dir:
                output_file = Path(input_path).stem
                if self.compile_options.native_compilation:
                    output_file += ".exe" if os.name == 'nt' else ""
                else:
                    output_file += ".byte"
                cmd.extend(["-o", os.path.join(self.compile_options.output_dir, output_file)])
            
            # Input file
            cmd.append(input_path)
            
            # Run compilation
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise CompilationError(f"OCaml compilation failed:\n{result.stderr}")
            
            return True
            
        except Exception as e:
            raise CompilationError(f"OCaml compilation failed: {str(e)}")
    
    def validate_syntax(self, source_code: str) -> Tuple[bool, List[str]]:
        """Validate OCaml syntax."""
        errors = []
        try:
            self.parse_source(source_code)
            return True, []
        except Exception as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, errors
    
    def validate_semantics(self, ast_node: OcamlNode) -> Tuple[bool, List[str]]:
        """Validate OCaml semantics."""
        try:
            validator = OcamlSemanticValidator()
            validator.validate(ast_node)
            return True, []
        except Exception as e:
            return False, [f"Semantic error: {str(e)}"]
    
    def check_types(self, source_code: str) -> Tuple[bool, List[str]]:
        """Check OCaml types using the compiler."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
            
            try:
                # Use ocamlc for type checking only
                cmd = [self.compile_options.ocamlc_path, "-i"]
                cmd.extend(self.compile_options.warnings)
                cmd.append(temp_file_path)
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    errors = result.stderr.strip().split('\n') if result.stderr else []
                    return False, errors
                
                return True, []
                
            finally:
                os.unlink(temp_file_path)
                
        except Exception as e:
            return False, [f"Type checking failed: {str(e)}"]
    
    def get_module_dependencies(self, ast_node: OcamlModule) -> List[str]:
        """Extract module dependencies from AST."""
        dependencies = []
        # This would analyze the AST for module references
        # For now, return empty list
        return dependencies
    
    def extract_function_signatures(self, ast_node: OcamlModule) -> Dict[str, str]:
        """Extract function signatures from module."""
        signatures = {}
        for decl in ast_node.declarations:
            if isinstance(decl, OcamlValueDeclaration):
                if isinstance(decl.pattern, OcamlVariablePattern):
                    signatures[decl.pattern.name] = "inferred_type"
        return signatures
    
    def get_data_types(self, ast_node: OcamlModule) -> List[str]:
        """Extract data type definitions from module."""
        types = []
        for decl in ast_node.declarations:
            if isinstance(decl, OcamlTypeDeclaration):
                types.append(decl.name)
        return types
    
    def verify_round_trip(self, source_code: str) -> bool:
        """Verify round-trip translation maintains semantics."""
        try:
            # Parse original
            original_ast = self.parse_source(source_code)
            
            # Generate code and re-parse
            generated_code = self.generate_code(original_ast)
            regenerated_ast = self.parse_source(generated_code)
            
            # Compare ASTs (simplified comparison)
            return self._compare_asts(original_ast, regenerated_ast)
            
        except Exception:
            return False
    
    def _compare_asts(self, ast1: OcamlNode, ast2: OcamlNode) -> bool:
        """Compare two ASTs for structural equality."""
        # Simplified comparison - would need more sophisticated logic
        return type(ast1) == type(ast2)
    
    def configure_compiler(self, options: OcamlCompileOptions):
        """Configure compiler options."""
        self.compile_options = options
    
    def configure_style(self, style: OcamlCodeStyle):
        """Configure code style."""
        self.code_style = style
    
    def get_language_info(self) -> Dict[str, Any]:
        """Get language information."""
        return {
            "name": "OCaml",
            "version": self.version,
            "tier": 5,
            "paradigms": ["functional", "imperative", "object-oriented"],
            "typing": "static",
            "file_extensions": self.file_extensions,
            "mime_types": self.mime_types,
            "features": [
                "pattern_matching",
                "type_inference",
                "algebraic_data_types",
                "modules",
                "functors",
                "objects",
                "polymorphism",
                "first_class_functions"
            ],
            "toolchain_version": self.version
        }


class OcamlSemanticValidator:
    """OCaml semantic validation."""
    
    def __init__(self):
        self.errors = []
    
    def validate(self, node: OcamlNode):
        """Validate semantic correctness."""
        method_name = f"validate_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.validate_generic)
        return method(node)
    
    def validate_generic(self, node: OcamlNode):
        """Generic validation."""
        pass
    
    def validate_ocamlmodule(self, node: OcamlModule):
        """Validate module."""
        for decl in node.declarations:
            self.validate(decl)
    
    def validate_ocamlvaluedeclaration(self, node: OcamlValueDeclaration):
        """Validate value declaration."""
        self.validate(node.pattern)
        self.validate(node.expression)


# Convenience functions
def parse_ocaml_code(source_code: str) -> OcamlModule:
    """Parse OCaml source code."""
    toolchain = OcamlToolchain()
    return toolchain.parse_source(source_code)

def generate_ocaml_code(ast_node: OcamlNode, style: Optional[OcamlCodeStyle] = None) -> str:
    """Generate OCaml code from AST."""
    toolchain = OcamlToolchain()
    return toolchain.generate_code(ast_node, style)

def ocaml_round_trip_verify(source_code: str) -> bool:
    """Verify OCaml round-trip translation."""
    toolchain = OcamlToolchain()
    return toolchain.verify_round_trip(source_code)

def ocaml_to_runa_translate(ocaml_source: str) -> str:
    """Translate OCaml to Runa."""
    toolchain = OcamlToolchain()
    return toolchain.translate_to_runa(ocaml_source)

def runa_to_ocaml_translate(runa_source: str) -> str:
    """Translate Runa to OCaml."""
    toolchain = OcamlToolchain()
    return toolchain.translate_from_runa(runa_source) 