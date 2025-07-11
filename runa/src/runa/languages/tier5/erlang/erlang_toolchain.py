#!/usr/bin/env python3
"""
Erlang Toolchain

Complete toolchain for Erlang language support in Runa.
"""

import os
import subprocess
import tempfile
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field

from ...shared.base_toolchain import BaseToolchain, ToolchainConfig, CompilationResult
from ....core.error_handler import ErrorHandler, RunaError

from .erlang_ast import ErlangNode, ErlangProgram
from .erlang_parser import parse_erlang, parse_erlang_expression
from .erlang_converter import ErlangToRunaConverter, RunaToErlangConverter, erlang_to_runa, runa_to_erlang
from .erlang_generator import ErlangCodeGenerator, generate_erlang_code


@dataclass
class ErlangToolchainConfig(ToolchainConfig):
    """Erlang-specific toolchain configuration."""
    erlang_compiler: str = "erlc"
    erlang_interpreter: str = "erl"
    format_on_generate: bool = True
    indent_size: int = 4
    enable_syntax_check: bool = True
    enable_semantic_check: bool = True
    output_format: str = "beam"  # "beam", "erl"


class ErlangToolchain(BaseToolchain):
    """Complete Erlang language toolchain."""
    
    def __init__(self, config: Optional[ErlangToolchainConfig] = None):
        super().__init__()
        self.config = config or ErlangToolchainConfig()
        self.error_handler = ErrorHandler()
        
        # Components
        self.converter_to_runa = ErlangToRunaConverter()
        self.converter_from_runa = RunaToErlangConverter()
        self.generator = ErlangCodeGenerator(self.config.indent_size)
        
        # Runtime state
        self.runtime_available = self._check_runtime()
        self.temp_files: List[str] = []
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ErlangProgram:
        """Parse Erlang source code into AST."""
        try:
            return parse_erlang(source_code)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Erlang parsing failed: {e}", "PARSE_ERROR", file_path)
            )
            raise
    
    def parse_expression(self, expression: str) -> ErlangNode:
        """Parse single Erlang expression."""
        try:
            return parse_erlang_expression(expression)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Erlang expression parsing failed: {e}", "PARSE_ERROR")
            )
            raise
    
    def convert_to_runa(self, erlang_ast: ErlangNode):
        """Convert Erlang AST to Runa universal AST."""
        try:
            return self.converter_to_runa.convert(erlang_ast)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Erlang to Runa conversion failed: {e}", "CONVERSION_ERROR")
            )
            raise
    
    def convert_from_runa(self, runa_ast):
        """Convert Runa universal AST to Erlang AST."""
        try:
            return self.converter_from_runa.convert(runa_ast)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Runa to Erlang conversion failed: {e}", "CONVERSION_ERROR")
            )
            raise
    
    def generate(self, erlang_ast: ErlangNode) -> str:
        """Generate Erlang code from AST."""
        try:
            return self.generator.generate(erlang_ast)
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Erlang code generation failed: {e}", "GENERATION_ERROR")
            )
            raise
    
    def validate(self, erlang_ast: ErlangNode, source_code: Optional[str] = None) -> List[str]:
        """Validate Erlang AST and optionally source code."""
        issues = []
        
        try:
            if self.config.enable_syntax_check:
                issues.extend(self._validate_syntax(erlang_ast))
            
            if self.config.enable_semantic_check:
                issues.extend(self._validate_semantics(erlang_ast))
            
        except Exception as e:
            issues.append(f"Validation error: {e}")
        
        return issues
    
    def compile(self, source_code: str, output_path: Optional[str] = None) -> CompilationResult:
        """Compile Erlang source code."""
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
            
            # Compile with Erlang compiler if needed
            compiled_output = None
            if self.config.output_format == "beam" and self.runtime_available:
                compiled_output = self._compile_with_erlc(generated_code, output_path)
            
            return CompilationResult(
                success=True,
                output_path=compiled_output or output_path,
                errors=[],
                warnings=[i for i in issues if "warning" in i.lower()],
                metadata={
                    'language': 'erlang',
                    'format': self.config.output_format
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
        """Execute Erlang source code."""
        if not self.runtime_available:
            raise RuntimeError("Erlang runtime not available")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.erl', delete=False) as f:
            f.write(source_code)
            temp_file = f.name
        
        self.temp_files.append(temp_file)
        
        try:
            # Compile first
            cmd = [self.config.erlang_compiler, temp_file]
            compile_process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if compile_process.returncode != 0:
                return compile_process.returncode, "", compile_process.stderr
            
            # Execute
            module_name = os.path.basename(temp_file).replace('.erl', '')
            cmd = [self.config.erlang_interpreter, "-noshell", "-s", module_name, "start", "-s", "init", "stop"]
            if args:
                cmd.extend(args)
            
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return process.returncode, process.stdout, process.stderr
            
        except subprocess.TimeoutExpired:
            return 1, "", "Execution timed out"
        except Exception as e:
            return 1, "", f"Execution failed: {e}"
        finally:
            # Clean up
            for ext in ['.erl', '.beam']:
                try:
                    file_to_remove = temp_file.replace('.erl', ext)
                    os.unlink(file_to_remove)
                except:
                    pass
            try:
                self.temp_files.remove(temp_file)
            except:
                pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get toolchain information."""
        return {
            'name': 'Erlang',
            'version': '1.0.0',
            'tier': 5,
            'features': [
                'Actor model',
                'Pattern matching',
                'Functional programming',
                'Distributed systems',
                'Fault tolerance',
                'Hot code swapping',
                'Concurrency'
            ],
            'file_extensions': ['.erl', '.hrl'],
            'compiler': self.config.erlang_compiler,
            'interpreter': self.config.erlang_interpreter,
            'runtime_available': self.runtime_available
        }
    
    def cleanup(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        self.temp_files.clear()
    
    # Private methods
    def _check_runtime(self) -> bool:
        """Check if Erlang runtime is available."""
        try:
            result = subprocess.run(
                [self.config.erlang_compiler, "-help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _validate_syntax(self, ast: ErlangNode) -> List[str]:
        """Validate Erlang syntax."""
        issues = []
        try:
            # Try to regenerate code
            code = self.generate(ast)
            # Try to re-parse
            reparsed = self.parse(code)
        except Exception as e:
            issues.append(f"Syntax error: {e}")
        return issues
    
    def _validate_semantics(self, ast: ErlangNode) -> List[str]:
        """Validate Erlang semantics."""
        issues = []
        # Add semantic validation here
        return issues
    
    def _compile_with_erlc(self, source_code: str, output_path: Optional[str] = None) -> Optional[str]:
        """Compile with erlc."""
        if not self.runtime_available:
            return None
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.erl', delete=False) as f:
                f.write(source_code)
                temp_file = f.name
            
            cmd = [self.config.erlang_compiler, temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                beam_file = temp_file.replace('.erl', '.beam')
                if output_path and output_path.endswith('.beam'):
                    os.rename(beam_file, output_path)
                    return output_path
                return beam_file
            else:
                raise RuntimeError(f"Compilation failed: {result.stderr}")
        
        except Exception as e:
            self.error_handler.handle_error(
                RunaError(f"Erlang compilation failed: {e}", "COMPILATION_ERROR")
            )
            return None


# Convenience functions
def create_erlang_toolchain(config: Optional[Dict[str, Any]] = None) -> ErlangToolchain:
    """Create Erlang toolchain."""
    if config:
        toolchain_config = ErlangToolchainConfig(**config)
    else:
        toolchain_config = ErlangToolchainConfig()
    
    return ErlangToolchain(toolchain_config)


def compile_erlang_file(file_path: str, output_path: Optional[str] = None) -> CompilationResult:
    """Compile Erlang file."""
    toolchain = create_erlang_toolchain()
    
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        if output_path is None:
            output_path = file_path.replace('.erl', '.beam')
        
        return toolchain.compile(source_code, output_path)
    
    except Exception as e:
        return CompilationResult(
            success=False,
            output_path=None,
            errors=[f"Failed to compile {file_path}: {e}"],
            warnings=[]
        )


def run_erlang_file(file_path: str, args: Optional[List[str]] = None) -> Tuple[int, str, str]:
    """Run Erlang file."""
    toolchain = create_erlang_toolchain()
    
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        return toolchain.execute(source_code, args)
    
    except Exception as e:
        return 1, "", f"Failed to run {file_path}: {e}" 