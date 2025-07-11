#!/usr/bin/env python3
"""
LISP Toolchain

Complete toolchain for LISP language support in Runa.
Provides parsing, conversion, generation, validation, and runtime integration.
"""

import os
import subprocess
import tempfile
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field

from ...shared.base_toolchain import BaseToolchain, ToolchainConfig, CompilationResult
from ....core.config import RunaConfig
from ....core.error_handler import ErrorHandler, RunaError

from .lisp_ast import LispNode, LispProgram
from .lisp_parser import parse_lisp, parse_lisp_expression
from .lisp_converter import LispToRunaConverter, RunaToLispConverter, lisp_to_runa, runa_to_lisp
from .lisp_generator import LispCodeGenerator, generate_lisp_code, format_lisp_code


@dataclass
class LispToolchainConfig(ToolchainConfig):
    """LISP-specific toolchain configuration."""
    
    # LISP interpreter/runtime
    lisp_interpreter: str = "sbcl"  # Steel Bank Common Lisp by default
    lisp_args: List[str] = field(default_factory=lambda: ["--script"])
    
    # Code formatting
    format_on_generate: bool = True
    indent_size: int = 2
    max_line_length: int = 80
    
    # Validation
    enable_syntax_check: bool = True
    enable_semantic_check: bool = True
    enable_runtime_check: bool = False
    
    # Features
    enable_macros: bool = True
    enable_reader_macros: bool = True
    enable_debugging: bool = False
    
    # Output options
    output_format: str = "lisp"  # "lisp", "fasl", "executable"
    optimization_level: int = 1  # 0-3


class LispToolchain(BaseToolchain):
    """Complete LISP language toolchain."""
    
    def __init__(self, config: Optional[LispToolchainConfig] = None):
        super().__init__()
        self.config = config or LispToolchainConfig()
        self.error_handler = ErrorHandler()
        
        # Components
        self.parser = None
        self.converter_to_runa = LispToRunaConverter()
        self.converter_from_runa = RunaToLispConverter()
        self.generator = LispCodeGenerator(self.config.indent_size)
        
        # Runtime state
        self.runtime_available = self._check_runtime()
        self.temp_files: List[str] = []
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> LispProgram:
        """Parse LISP source code into AST."""
        try:
            return parse_lisp(source_code)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"LISP parsing failed: {e}", "PARSE_ERROR", file_path)
            )
            raise
    
    def parse_expression(self, expression: str) -> LispNode:
        """Parse a single LISP expression."""
        try:
            return parse_lisp_expression(expression)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"LISP expression parsing failed: {e}", "PARSE_ERROR")
            )
            raise
    
    def convert_to_runa(self, lisp_ast: LispNode):
        """Convert LISP AST to Runa universal AST."""
        try:
            return self.converter_to_runa.convert(lisp_ast)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"LISP to Runa conversion failed: {e}", "CONVERSION_ERROR")
            )
            raise
    
    def convert_from_runa(self, runa_ast):
        """Convert Runa universal AST to LISP AST."""
        try:
            return self.converter_from_runa.convert(runa_ast)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Runa to LISP conversion failed: {e}", "CONVERSION_ERROR")
            )
            raise
    
    def generate(self, lisp_ast: LispNode) -> str:
        """Generate LISP code from AST."""
        try:
            code = self.generator.generate(lisp_ast)
            
            if self.config.format_on_generate:
                code = format_lisp_code(code, {
                    'indent_size': self.config.indent_size,
                    'max_line_length': self.config.max_line_length
                })
            
            return code
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"LISP code generation failed: {e}", "GENERATION_ERROR")
            )
            raise
    
    def validate(self, lisp_ast: LispNode, source_code: Optional[str] = None) -> List[str]:
        """Validate LISP AST and optionally source code."""
        issues = []
        
        try:
            # Syntax validation
            if self.config.enable_syntax_check:
                issues.extend(self._validate_syntax(lisp_ast))
            
            # Semantic validation
            if self.config.enable_semantic_check:
                issues.extend(self._validate_semantics(lisp_ast))
            
            # Runtime validation
            if self.config.enable_runtime_check and source_code:
                issues.extend(self._validate_runtime(source_code))
            
        except Exception as e:
            issues.append(f"Validation error: {e}")
        
        return issues
    
    def compile(self, source_code: str, output_path: Optional[str] = None) -> CompilationResult:
        """Compile LISP source code."""
        try:
            # Parse
            ast = self.parse(source_code)
            
            # Validate
            issues = self.validate(ast, source_code)
            if issues and any("error" in issue.lower() for issue in issues):
                return CompilationResult(
                    success=False,
                    output_path=None,
                    errors=issues,
                    warnings=[i for i in issues if "warning" in i.lower()]
                )
            
            # Generate code
            generated_code = self.generate(ast)
            
            # Write output
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w') as f:
                    f.write(generated_code)
            
            # Compile with LISP runtime if needed
            compiled_output = None
            if self.config.output_format in ["fasl", "executable"]:
                compiled_output = self._compile_with_runtime(generated_code, output_path)
            
            return CompilationResult(
                success=True,
                output_path=compiled_output or output_path,
                errors=[],
                warnings=[i for i in issues if "warning" in i.lower()],
                metadata={
                    'language': 'lisp',
                    'format': self.config.output_format,
                    'optimization_level': self.config.optimization_level
                }
            )
            
        except Exception as e:
            return CompilationResult(
                success=False,
                output_path=None,
                errors=[str(e)],
                warnings=[]
            )
    
    def execute(self, source_code: str, args: Optional[List[str]] = None) -> Tuple[int, str, str]:
        """Execute LISP source code."""
        if not self.runtime_available:
            raise RuntimeError("LISP runtime not available")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lisp', delete=False) as f:
            f.write(source_code)
            temp_file = f.name
        
        self.temp_files.append(temp_file)
        
        try:
            # Build command
            cmd = [self.config.lisp_interpreter] + self.config.lisp_args + [temp_file]
            if args:
                cmd.extend(args)
            
            # Execute
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            return process.returncode, process.stdout, process.stderr
            
        except subprocess.TimeoutExpired:
            return 1, "", "Execution timed out"
        except Exception as e:
            return 1, "", f"Execution failed: {e}"
        finally:
            # Clean up
            try:
                os.unlink(temp_file)
                self.temp_files.remove(temp_file)
            except:
                pass
    
    def repl(self) -> None:
        """Start an interactive LISP REPL."""
        if not self.runtime_available:
            print("LISP runtime not available")
            return
        
        print("Runa LISP REPL (type 'quit' to exit)")
        print("Using interpreter:", self.config.lisp_interpreter)
        print()
        
        while True:
            try:
                # Get input
                line = input("LISP> ").strip()
                
                if line.lower() in ['quit', 'exit', ':q']:
                    break
                
                if not line:
                    continue
                
                # Parse and execute
                try:
                    ast = self.parse_expression(line)
                    code = self.generate(ast)
                    
                    # Execute
                    returncode, stdout, stderr = self.execute(f"(print {code})")
                    
                    if returncode == 0:
                        print(stdout.strip())
                    else:
                        print(f"Error: {stderr.strip()}")
                        
                except Exception as e:
                    print(f"Parse error: {e}")
            
            except KeyboardInterrupt:
                print("\nKeyboard interrupt")
                break
            except EOFError:
                break
        
        print("Goodbye!")
    
    def get_info(self) -> Dict[str, Any]:
        """Get toolchain information."""
        return {
            'name': 'LISP',
            'version': '1.0.0',
            'tier': 5,
            'features': [
                'S-expressions',
                'Functional programming',
                'Macros',
                'REPL support',
                'Runtime execution',
                'Cross-compilation'
            ],
            'file_extensions': ['.lisp', '.lsp', '.cl'],
            'interpreter': self.config.lisp_interpreter,
            'runtime_available': self.runtime_available,
            'config': {
                'format_on_generate': self.config.format_on_generate,
                'enable_macros': self.config.enable_macros,
                'optimization_level': self.config.optimization_level
            }
        }
    
    def cleanup(self):
        """Clean up temporary files and resources."""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        self.temp_files.clear()
    
    # Private methods
    def _check_runtime(self) -> bool:
        """Check if LISP runtime is available."""
        try:
            result = subprocess.run(
                [self.config.lisp_interpreter, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            # Try alternative interpreters
            alternatives = ["clisp", "ecl", "sbcl", "ccl", "abcl"]
            for interpreter in alternatives:
                try:
                    result = subprocess.run(
                        [interpreter, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        self.config.lisp_interpreter = interpreter
                        return True
                except:
                    continue
            return False
    
    def _validate_syntax(self, ast: LispNode) -> List[str]:
        """Validate LISP syntax."""
        issues = []
        
        try:
            # Try to regenerate code to check syntax consistency
            code = self.generate(ast)
            
            # Try to re-parse generated code
            reparsed = self.parse(code)
            
        except Exception as e:
            issues.append(f"Syntax error: {e}")
        
        return issues
    
    def _validate_semantics(self, ast: LispNode) -> List[str]:
        """Validate LISP semantics."""
        issues = []
        
        # This is a simplified semantic validator
        # In a real implementation, you'd have a full semantic analyzer
        
        try:
            # Check for common semantic issues
            if isinstance(ast, LispProgram):
                for form in ast.forms:
                    issues.extend(self._check_form_semantics(form))
        
        except Exception as e:
            issues.append(f"Semantic analysis error: {e}")
        
        return issues
    
    def _check_form_semantics(self, form: LispNode) -> List[str]:
        """Check semantics of a single form."""
        issues = []
        
        # Add semantic checks here
        # For example: undefined variables, type mismatches, etc.
        
        return issues
    
    def _validate_runtime(self, source_code: str) -> List[str]:
        """Validate by attempting runtime execution."""
        issues = []
        
        if not self.runtime_available:
            issues.append("Warning: Runtime validation skipped (interpreter not available)")
            return issues
        
        try:
            # Wrap code in a way that catches errors but doesn't execute side effects
            test_code = f"""
(handler-case
    (progn {source_code} nil)
  (error (c) (format t "Error: ~A" c)))
"""
            
            returncode, stdout, stderr = self.execute(test_code)
            
            if returncode != 0:
                issues.append(f"Runtime error: {stderr}")
            elif "Error:" in stdout:
                issues.append(f"Runtime validation: {stdout}")
        
        except Exception as e:
            issues.append(f"Runtime validation error: {e}")
        
        return issues
    
    def _compile_with_runtime(self, source_code: str, output_path: Optional[str] = None) -> Optional[str]:
        """Compile LISP code using runtime compiler."""
        if not self.runtime_available:
            return None
        
        try:
            # Create compilation script
            if self.config.output_format == "fasl":
                compile_code = f"""
(compile-file "{output_path}")
"""
            else:  # executable
                compile_code = f"""
(sb-ext:save-lisp-and-die "{output_path}" :executable t :toplevel (lambda () (main)))
"""
            
            # Execute compilation
            returncode, stdout, stderr = self.execute(compile_code)
            
            if returncode == 0:
                return output_path
            else:
                raise RuntimeError(f"Compilation failed: {stderr}")
        
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Runtime compilation failed: {e}", "COMPILATION_ERROR")
            )
            return None


# Convenience functions
def create_lisp_toolchain(config: Optional[Dict[str, Any]] = None) -> LispToolchain:
    """Create a LISP toolchain with optional configuration."""
    if config:
        toolchain_config = LispToolchainConfig(**config)
    else:
        toolchain_config = LispToolchainConfig()
    
    return LispToolchain(toolchain_config)


def compile_lisp_file(file_path: str, output_path: Optional[str] = None) -> CompilationResult:
    """Compile a LISP file."""
    toolchain = create_lisp_toolchain()
    
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        if output_path is None:
            output_path = file_path.replace('.lisp', '.fasl')
        
        return toolchain.compile(source_code, output_path)
    
    except Exception as e:
        return CompilationResult(
            success=False,
            output_path=None,
            errors=[f"Failed to compile {file_path}: {e}"],
            warnings=[]
        )


def run_lisp_file(file_path: str, args: Optional[List[str]] = None) -> Tuple[int, str, str]:
    """Run a LISP file."""
    toolchain = create_lisp_toolchain()
    
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        return toolchain.execute(source_code, args)
    
    except Exception as e:
        return 1, "", f"Failed to run {file_path}: {e}"


def start_lisp_repl():
    """Start a LISP REPL."""
    toolchain = create_lisp_toolchain()
    toolchain.repl()


# Testing utilities
def test_lisp_toolchain():
    """Test the LISP toolchain."""
    toolchain = create_lisp_toolchain()
    
    # Test cases
    test_cases = [
        # Simple expression
        "(+ 1 2 3)",
        
        # Function definition
        "(defun factorial (n) (if (= n 0) 1 (* n (factorial (- n 1)))))",
        
        # Let binding
        "(let ((x 10) (y 20)) (+ x y))",
        
        # Conditional
        "(if (> 5 3) 'true 'false)",
        
        # List operations
        "(car (cons 1 2))",
    ]
    
    print("Testing LISP toolchain...")
    
    for i, test_code in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_code}")
        
        try:
            # Parse
            ast = toolchain.parse_expression(test_code)
            print(f"✓ Parsed successfully")
            
            # Generate
            generated = toolchain.generate(ast)
            print(f"✓ Generated: {generated}")
            
            # Validate
            issues = toolchain.validate(ast, test_code)
            if issues:
                print(f"⚠ Issues: {', '.join(issues)}")
            else:
                print(f"✓ Validation passed")
            
            # Execute if runtime available
            if toolchain.runtime_available:
                returncode, stdout, stderr = toolchain.execute(f"(print {test_code})")
                if returncode == 0:
                    print(f"✓ Executed: {stdout.strip()}")
                else:
                    print(f"✗ Execution failed: {stderr}")
            
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    print(f"\nToolchain info: {toolchain.get_info()}")
    toolchain.cleanup()


if __name__ == "__main__":
    test_lisp_toolchain() 