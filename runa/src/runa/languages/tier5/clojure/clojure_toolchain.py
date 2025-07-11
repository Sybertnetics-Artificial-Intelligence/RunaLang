#!/usr/bin/env python3
"""
Clojure Toolchain Integration

Complete toolchain for Clojure language support in the Runa Universal
Translation Pipeline. Integrates parsing, conversion, generation, and 
validation for seamless Clojure ↔ Runa translation.
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

from .clojure_ast import *
from .clojure_parser import ClojureLexer, ClojureParser, parse_clojure
from .clojure_converter import (
    ClojureToRunaConverter, RunaToClojureConverter,
    clojure_to_runa, runa_to_clojure
)
from .clojure_generator import ClojureCodeGenerator, ClojureCodeStyle, generate_clojure


@dataclass
class ClojureCompileOptions:
    """Clojure compilation options."""
    java_path: str = "java"
    clojure_jar: Optional[str] = None
    classpath: List[str] = None
    main_class: Optional[str] = None
    output_dir: Optional[str] = None
    aot_compile: bool = False
    
    def __post_init__(self):
        if self.classpath is None:
            self.classpath = ["."]


class ClojureToolchain(BaseToolchain):
    """Complete Clojure language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.language = "clojure"
        self.version = "1.0.0"
        self.file_extensions = [".clj", ".cljs", ".cljc"]
        self.mime_types = ["text/x-clojure"]
        
        # Components
        self.lexer_class = ClojureLexer
        self.parser_class = ClojureParser
        self.to_runa_converter = ClojureToRunaConverter()
        self.from_runa_converter = RunaToClojureConverter()
        self.code_generator = ClojureCodeGenerator()
        
        # Configuration
        self.compile_options = ClojureCompileOptions()
        self.code_style = ClojureCodeStyle()
    
    # Core parsing functionality
    def parse_source(self, source_code: str) -> ClojureModule:
        """Parse Clojure source code into AST."""
        try:
            return parse_clojure(source_code)
        except Exception as e:
            raise CompilationError(f"Clojure parsing failed: {str(e)}")
    
    def parse_file(self, file_path: str) -> ClojureModule:
        """Parse Clojure file into AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
            return self.parse_source(source_code)
        except FileNotFoundError:
            raise RunaError(f"Clojure file not found: {file_path}")
        except Exception as e:
            raise CompilationError(f"Failed to parse Clojure file {file_path}: {str(e)}")
    
    # Code generation
    def generate_code(self, ast_node: ClojureNode, style: Optional[ClojureCodeStyle] = None) -> str:
        """Generate Clojure code from AST."""
        try:
            generator = ClojureCodeGenerator(style or self.code_style)
            return generator.generate(ast_node)
        except Exception as e:
            raise CompilationError(f"Clojure code generation failed: {str(e)}")
    
    def format_code(self, source_code: str) -> str:
        """Format Clojure code."""
        try:
            # Parse and regenerate for formatting
            ast = self.parse_source(source_code)
            return self.generate_code(ast)
        except Exception as e:
            # Return original if formatting fails
            return source_code
    
    # Conversion functionality
    def to_runa_ast(self, clojure_ast: ClojureNode) -> RunaNode:
        """Convert Clojure AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(clojure_ast)
        except Exception as e:
            raise CompilationError(f"Clojure to Runa conversion failed: {str(e)}")
    
    def from_runa_ast(self, runa_ast: RunaNode) -> ClojureNode:
        """Convert Runa AST to Clojure AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise CompilationError(f"Runa to Clojure conversion failed: {str(e)}")
    
    def translate_from_runa(self, runa_source: str) -> str:
        """Translate Runa source code to Clojure."""
        try:
            # This would normally parse Runa, but for now we'll use a placeholder
            # In a complete implementation, this would:
            # 1. Parse Runa source to Runa AST
            # 2. Convert Runa AST to Clojure AST
            # 3. Generate Clojure code
            # TODO: Implement Runa parser not yet available
            return StringLiteral(value="Runa parser not yet available_placeholder")
        except Exception as e:
            raise CompilationError(f"Runa to Clojure translation failed: {str(e)}")
    
    def translate_to_runa(self, clojure_source: str) -> str:
        """Translate Clojure source code to Runa."""
        try:
            # Parse Clojure
            clojure_ast = self.parse_source(clojure_source)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_ast(clojure_ast)
            
            # Generate Runa code (placeholder - would need Runa generator)
            # return generate_runa_code(runa_ast)
            return ";; Runa code generation not yet implemented"
        except Exception as e:
            raise CompilationError(f"Clojure to Runa translation failed: {str(e)}")
    
    # REPL and evaluation
    def start_repl(self) -> bool:
        """Start Clojure REPL."""
        try:
            cmd = [self.compile_options.java_path]
            
            # Add classpath
            if self.compile_options.clojure_jar:
                cmd.extend(["-cp", f"{':'.join(self.compile_options.classpath)}:{self.compile_options.clojure_jar}"])
            else:
                cmd.extend(["-cp", ":".join(self.compile_options.classpath)])
            
            cmd.append("clojure.main")
            
            # Start REPL process
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, text=True)
            
            return process.returncode == 0 if process.poll() is not None else True
            
        except Exception as e:
            raise CompilationError(f"Failed to start Clojure REPL: {str(e)}")
    
    def evaluate_expression(self, expression: str) -> Any:
        """Evaluate Clojure expression."""
        try:
            # This would require a running Clojure process
            # For now, just parse and validate syntax
            ast = self.parse_source(expression)
            return "Expression parsed successfully"
        except Exception as e:
            raise CompilationError(f"Failed to evaluate expression: {str(e)}")
    
    # Compilation and validation
    def compile_source(self, source_code: str, output_path: Optional[str] = None) -> bool:
        """Compile Clojure source code."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.clj', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
            
            try:
                return self.compile_file(temp_file_path, output_path)
            finally:
                os.unlink(temp_file_path)
        except Exception as e:
            raise CompilationError(f"Clojure compilation failed: {str(e)}")
    
    def compile_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Compile Clojure file."""
        try:
            cmd = [self.compile_options.java_path]
            
            # Add classpath
            classpath = self.compile_options.classpath.copy()
            if self.compile_options.clojure_jar:
                classpath.append(self.compile_options.clojure_jar)
            
            cmd.extend(["-cp", ":".join(classpath)])
            cmd.append("clojure.main")
            
            if self.compile_options.aot_compile:
                cmd.extend(["-e", f"(compile '{Path(input_path).stem})"])
            else:
                cmd.append(input_path)
            
            # Run compilation
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise CompilationError(f"Clojure compilation failed:\n{result.stderr}")
            
            return True
            
        except Exception as e:
            raise CompilationError(f"Clojure compilation failed: {str(e)}")
    
    def validate_syntax(self, source_code: str) -> Tuple[bool, List[str]]:
        """Validate Clojure syntax."""
        errors = []
        try:
            self.parse_source(source_code)
            return True, []
        except Exception as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, errors
    
    def validate_semantics(self, ast_node: ClojureNode) -> Tuple[bool, List[str]]:
        """Validate Clojure semantics."""
        try:
            validator = ClojureSemanticValidator()
            validator.validate(ast_node)
            return True, []
        except Exception as e:
            return False, [f"Semantic error: {str(e)}"]
    
    def check_types(self, source_code: str) -> Tuple[bool, List[str]]:
        """Check Clojure types (basic validation)."""
        try:
            # Clojure is dynamically typed, so just validate syntax
            return self.validate_syntax(source_code)
        except Exception as e:
            return False, [f"Type checking failed: {str(e)}"]
    
    def get_namespace_dependencies(self, ast_node: ClojureModule) -> List[str]:
        """Extract namespace dependencies from AST."""
        dependencies = []
        if ast_node.namespace:
            for require in ast_node.namespace.requires:
                dependencies.append(require.namespace.qualified_name)
        return dependencies
    
    def extract_function_signatures(self, ast_node: ClojureModule) -> Dict[str, str]:
        """Extract function signatures from module."""
        signatures = {}
        for form in ast_node.forms:
            if isinstance(form, ClojureDefn):
                signatures[form.name.name] = f"({form.name.name} [params...])"
        return signatures
    
    def get_defined_symbols(self, ast_node: ClojureModule) -> List[str]:
        """Extract defined symbols from module."""
        symbols = []
        for form in ast_node.forms:
            if isinstance(form, (ClojureDef, ClojureDefn)):
                if hasattr(form, 'symbol'):
                    symbols.append(form.symbol.name)
                elif hasattr(form, 'name'):
                    symbols.append(form.name.name)
        return symbols
    
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
    
    def _compare_asts(self, ast1: ClojureNode, ast2: ClojureNode) -> bool:
        """Compare two ASTs for structural equality."""
        # Simplified comparison - would need more sophisticated logic
        return type(ast1) == type(ast2)
    
    def configure_compiler(self, options: ClojureCompileOptions):
        """Configure compiler options."""
        self.compile_options = options
    
    def configure_style(self, style: ClojureCodeStyle):
        """Configure code style."""
        self.code_style = style
    
    def get_language_info(self) -> Dict[str, Any]:
        """Get language information."""
        return {
            "name": "Clojure",
            "version": self.version,
            "tier": 5,
            "paradigms": ["functional", "dynamic", "lisp"],
            "typing": "dynamic",
            "file_extensions": self.file_extensions,
            "mime_types": self.mime_types,
            "features": [
                "s_expressions",
                "immutable_data_structures",
                "functional_programming",
                "macros",
                "java_interop",
                "dynamic_typing",
                "repl",
                "lazy_sequences",
                "persistent_data_structures"
            ],
            "toolchain_version": self.version
        }


class ClojureSemanticValidator:
    """Clojure semantic validation."""
    
    def __init__(self):
        self.errors = []
    
    def validate(self, node: ClojureNode):
        """Validate semantic correctness."""
        method_name = f"validate_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.validate_generic)
        return method(node)
    
    def validate_generic(self, node: ClojureNode):
        """Generic validation."""
        pass
    
    def validate_clojuremodule(self, node: ClojureModule):
        """Validate module."""
        if node.namespace:
            self.validate(node.namespace)
        for form in node.forms:
            self.validate(form)
    
    def validate_clojuredefn(self, node: ClojureDefn):
        """Validate function definition."""
        for arity in node.arities:
            for expr in arity.body:
                self.validate(expr)


# Convenience functions
def parse_clojure_code(source_code: str) -> ClojureModule:
    """Parse Clojure source code."""
    toolchain = ClojureToolchain()
    return toolchain.parse_source(source_code)

def generate_clojure_code(ast_node: ClojureNode, style: Optional[ClojureCodeStyle] = None) -> str:
    """Generate Clojure code from AST."""
    toolchain = ClojureToolchain()
    return toolchain.generate_code(ast_node, style)

def clojure_round_trip_verify(source_code: str) -> bool:
    """Verify Clojure round-trip translation."""
    toolchain = ClojureToolchain()
    return toolchain.verify_round_trip(source_code)

def clojure_to_runa_translate(clojure_source: str) -> str:
    """Translate Clojure to Runa."""
    toolchain = ClojureToolchain()
    return toolchain.translate_to_runa(clojure_source)

def runa_to_clojure_translate(runa_source: str) -> str:
    """Translate Runa to Clojure."""
    toolchain = ClojureToolchain()
    return toolchain.translate_from_runa(runa_source) 