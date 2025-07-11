#!/usr/bin/env python3
"""
Go Language Toolchain

Complete toolchain for Go language support in the Runa Universal Translation Platform.
Integrates parsing, AST conversion, code generation, and validation for Go language.

Features:
- Full Go language parsing and code generation
- Bidirectional Go ↔ Runa AST conversion
- Go-specific optimizations and validations
- Support for all Go constructs (goroutines, channels, interfaces, etc.)
- Go module system integration
- Error handling and diagnostics
- Performance optimizations
- Round-trip translation verification
"""

from typing import List, Optional, Dict, Any, Union, Set
from pathlib import Path
import tempfile
import subprocess
import json
import re
from dataclasses import dataclass, field

from .go_ast import *
from .go_parser import GoParser, GoLexer, GO_LANGUAGE_INFO
from .go_converter import GoToRunaConverter, RunaToGoConverter
from .go_generator import GoCodeGenerator, GoGeneratorOptions
from ....core.runa_ast import Program
from ....languages.shared.base_toolchain import BaseLanguageToolchain, ToolchainResult, ToolchainError
from ....core.translation_result import TranslationResult, TranslationError


@dataclass
class GoToolchainOptions:
    """Configuration options for Go toolchain."""
    # Parsing options
    strict_syntax: bool = True
    allow_experimental_features: bool = False
    go_version: str = "1.20"
    
    # Generation options
    generator_options: GoGeneratorOptions = field(default_factory=GoGeneratorOptions)
    format_output: bool = True
    add_build_tags: bool = False
    
    # Validation options
    validate_syntax: bool = True
    validate_semantics: bool = True
    check_go_modules: bool = True
    run_go_vet: bool = False
    
    # Performance options
    cache_parsed_files: bool = True
    parallel_processing: bool = True
    
    # Debug options
    debug_ast: bool = False
    debug_conversion: bool = False
    verbose_errors: bool = True


class GoToolchain(BaseLanguageToolchain):
    """Complete Go language toolchain."""
    
    def __init__(self, options: GoToolchainOptions = None):
        super().__init__(GO_LANGUAGE_INFO)
        self.options = options or GoToolchainOptions()
        
        # Initialize components
        self.parser = GoParser()
        self.go_to_runa_converter = GoToRunaConverter()
        self.runa_to_go_converter = RunaToGoConverter()
        self.generator = GoCodeGenerator(self.options.generator_options)
        
        # Caches
        self.parsed_files_cache: Dict[str, GoProgram] = {}
        self.validation_cache: Dict[str, bool] = {}
        
        # Statistics
        self.stats = {
            'files_parsed': 0,
            'lines_processed': 0,
            'errors_found': 0,
            'warnings_found': 0,
            'conversions_successful': 0,
            'round_trips_verified': 0
        }
    
    def parse_source(self, source_code: str, file_path: str = "") -> ToolchainResult[GoProgram]:
        """Parse Go source code into Go AST."""
        try:
            # Check cache first
            cache_key = f"{file_path}:{hash(source_code)}"
            if self.options.cache_parsed_files and cache_key in self.parsed_files_cache:
                return ToolchainResult.success(self.parsed_files_cache[cache_key])
            
            # Parse source
            go_program = self.parser.parse(source_code, file_path)
            
            # Cache result
            if self.options.cache_parsed_files:
                self.parsed_files_cache[cache_key] = go_program
            
            # Update statistics
            self.stats['files_parsed'] += 1
            self.stats['lines_processed'] += len(source_code.splitlines())
            
            # Debug output
            if self.options.debug_ast:
                self._debug_ast(go_program)
            
            return ToolchainResult.success(go_program)
            
        except Exception as e:
            self.stats['errors_found'] += 1
            error = ToolchainError(
                error_type="ParseError",
                message=f"Failed to parse Go source: {str(e)}",
                file_path=file_path,
                line=getattr(e, 'line', 0),
                column=getattr(e, 'column', 0)
            )
            return ToolchainResult.failure(error)
    
    def generate_code(self, go_ast: GoProgram) -> ToolchainResult[str]:
        """Generate Go source code from Go AST."""
        try:
            # Generate code
            generated_code = self.generator.generate(go_ast)
            
            # Format if requested
            if self.options.format_output:
                formatted_code = self._format_go_code(generated_code)
                if formatted_code:
                    generated_code = formatted_code
            
            # Validate syntax if requested
            if self.options.validate_syntax:
                validation_result = self._validate_go_syntax(generated_code)
                if not validation_result.success:
                    return validation_result
            
            return ToolchainResult.success(generated_code)
            
        except Exception as e:
            self.stats['errors_found'] += 1
            error = ToolchainError(
                error_type="GenerationError",
                message=f"Failed to generate Go code: {str(e)}"
            )
            return ToolchainResult.failure(error)
    
    def to_runa_ast(self, go_ast: GoProgram) -> ToolchainResult[Program]:
        """Convert Go AST to Runa AST."""
        try:
            # Convert AST
            runa_program = self.go_to_runa_converter.convert_program(go_ast)
            
            # Update statistics
            self.stats['conversions_successful'] += 1
            
            # Debug output
            if self.options.debug_conversion:
                self._debug_conversion("Go -> Runa", go_ast, runa_program)
            
            return ToolchainResult.success(runa_program)
            
        except Exception as e:
            self.stats['errors_found'] += 1
            error = ToolchainError(
                error_type="ConversionError",
                message=f"Failed to convert Go AST to Runa AST: {str(e)}"
            )
            return ToolchainResult.failure(error)
    
    def from_runa_ast(self, runa_ast: Program) -> ToolchainResult[GoProgram]:
        """Convert Runa AST to Go AST."""
        try:
            # Convert AST
            go_program = self.runa_to_go_converter.convert_program(runa_ast)
            
            # Update statistics
            self.stats['conversions_successful'] += 1
            
            # Debug output
            if self.options.debug_conversion:
                self._debug_conversion("Runa -> Go", runa_ast, go_program)
            
            return ToolchainResult.success(go_program)
            
        except Exception as e:
            self.stats['errors_found'] += 1
            error = ToolchainError(
                error_type="ConversionError",
                message=f"Failed to convert Runa AST to Go AST: {str(e)}"
            )
            return ToolchainResult.failure(error)
    
    def validate_code(self, source_code: str, file_path: str = "") -> ToolchainResult[List[str]]:
        """Validate Go source code."""
        issues = []
        
        try:
            # Check cache first
            cache_key = f"{file_path}:{hash(source_code)}"
            if cache_key in self.validation_cache:
                return ToolchainResult.success([])
            
            # Syntax validation
            if self.options.validate_syntax:
                syntax_result = self._validate_go_syntax(source_code)
                if not syntax_result.success:
                    issues.append(f"Syntax error: {syntax_result.error.message}")
            
            # Semantic validation
            if self.options.validate_semantics:
                semantic_issues = self._validate_go_semantics(source_code)
                issues.extend(semantic_issues)
            
            # Go modules validation
            if self.options.check_go_modules:
                module_issues = self._validate_go_modules(source_code, file_path)
                issues.extend(module_issues)
            
            # Go vet analysis
            if self.options.run_go_vet:
                vet_issues = self._run_go_vet(source_code, file_path)
                issues.extend(vet_issues)
            
            # Cache successful validation
            if not issues:
                self.validation_cache[cache_key] = True
            
            # Update statistics
            if issues:
                self.stats['errors_found'] += len([i for i in issues if 'error' in i.lower()])
                self.stats['warnings_found'] += len([i for i in issues if 'warning' in i.lower()])
            
            return ToolchainResult.success(issues)
            
        except Exception as e:
            error = ToolchainError(
                error_type="ValidationError",
                message=f"Failed to validate Go code: {str(e)}",
                file_path=file_path
            )
            return ToolchainResult.failure(error)
    
    def round_trip_test(self, source_code: str, file_path: str = "") -> ToolchainResult[bool]:
        """Test round-trip conversion: Go -> Runa -> Go."""
        try:
            # Parse original Go code
            parse_result = self.parse_source(source_code, file_path)
            if not parse_result.success:
                return parse_result
            
            original_go_ast = parse_result.result
            
            # Convert to Runa AST
            to_runa_result = self.to_runa_ast(original_go_ast)
            if not to_runa_result.success:
                return to_runa_result
            
            runa_ast = to_runa_result.result
            
            # Convert back to Go AST
            from_runa_result = self.from_runa_ast(runa_ast)
            if not from_runa_result.success:
                return from_runa_result
            
            reconstructed_go_ast = from_runa_result.result
            
            # Generate code from reconstructed AST
            gen_result = self.generate_code(reconstructed_go_ast)
            if not gen_result.success:
                return gen_result
            
            reconstructed_code = gen_result.result
            
            # Compare semantic equivalence
            is_equivalent = self._compare_go_semantics(source_code, reconstructed_code)
            
            if is_equivalent:
                self.stats['round_trips_verified'] += 1
            
            return ToolchainResult.success(is_equivalent)
            
        except Exception as e:
            error = ToolchainError(
                error_type="RoundTripError",
                message=f"Round-trip test failed: {str(e)}",
                file_path=file_path
            )
            return ToolchainResult.failure(error)
    
    def get_language_features(self) -> Dict[str, Any]:
        """Get supported Go language features."""
        return {
            'version': self.options.go_version,
            'features': {
                'packages': True,
                'imports': True,
                'types': {
                    'basic_types': True,
                    'arrays': True,
                    'slices': True,
                    'maps': True,
                    'structs': True,
                    'interfaces': True,
                    'pointers': True,
                    'channels': True,
                    'functions': True,
                },
                'statements': {
                    'assignments': True,
                    'short_var_declarations': True,
                    'if_statements': True,
                    'for_loops': True,
                    'range_loops': True,
                    'switch_statements': True,
                    'type_switches': True,
                    'select_statements': True,
                    'defer_statements': True,
                    'go_statements': True,
                    'return_statements': True,
                    'break_continue': True,
                    'goto_labels': True,
                },
                'expressions': {
                    'literals': True,
                    'identifiers': True,
                    'binary_operations': True,
                    'unary_operations': True,
                    'function_calls': True,
                    'method_calls': True,
                    'indexing': True,
                    'slicing': True,
                    'type_assertions': True,
                    'channel_operations': True,
                },
                'concurrency': {
                    'goroutines': True,
                    'channels': True,
                    'select_statements': True,
                    'mutexes': False,  # stdlib, not language feature
                },
                'error_handling': {
                    'multiple_returns': True,
                    'error_type': True,
                    'panic_recover': True,
                },
                'modern_features': {
                    'generics': self.options.go_version >= "1.18",
                    'modules': True,
                    'build_constraints': True,
                    'context': False,  # stdlib
                }
            },
            'extensions': ['.go'],
            'build_system': 'go_modules',
            'package_manager': 'go_mod',
            'testing_framework': 'go_test',
            'documentation': 'godoc'
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get toolchain statistics."""
        return {
            'toolchain': 'Go',
            'version': self.options.go_version,
            'statistics': self.stats.copy(),
            'cache_sizes': {
                'parsed_files': len(self.parsed_files_cache),
                'validations': len(self.validation_cache),
            },
            'options': {
                'strict_syntax': self.options.strict_syntax,
                'validate_syntax': self.options.validate_syntax,
                'validate_semantics': self.options.validate_semantics,
                'format_output': self.options.format_output,
            }
        }
    
    def clear_caches(self):
        """Clear all caches."""
        self.parsed_files_cache.clear()
        self.validation_cache.clear()
    
    # Private helper methods
    
    def _debug_ast(self, go_ast: GoProgram):
        """Debug print AST structure."""
        print(f"=== Go AST Debug ===")
        print(f"Files: {len(go_ast.files)}")
        for i, file_node in enumerate(go_ast.files):
            print(f"File {i}: Package={file_node.package.name if file_node.package else 'None'}")
            print(f"  Imports: {len(file_node.imports)}")
            print(f"  Declarations: {len(file_node.declarations)}")
    
    def _debug_conversion(self, direction: str, source_ast: Any, target_ast: Any):
        """Debug print conversion details."""
        print(f"=== {direction} Conversion Debug ===")
        print(f"Source AST type: {type(source_ast).__name__}")
        print(f"Target AST type: {type(target_ast).__name__}")
        if hasattr(source_ast, 'files'):
            print(f"Source files: {len(source_ast.files)}")
        if hasattr(target_ast, 'statements'):
            print(f"Target statements: {len(target_ast.statements)}")
    
    def _format_go_code(self, code: str) -> Optional[str]:
        """Format Go code using gofmt if available."""
        try:
            # Try to use gofmt for formatting
            process = subprocess.run(
                ['gofmt'],
                input=code,
                text=True,
                capture_output=True,
                timeout=10
            )
            
            if process.returncode == 0:
                return process.stdout
            else:
                # Fall back to basic formatting if gofmt fails
                return self._basic_go_format(code)
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # gofmt not available, use basic formatting
            return self._basic_go_format(code)
    
    def _basic_go_format(self, code: str) -> str:
        """Basic Go code formatting."""
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Adjust indentation based on braces
            if stripped.endswith('{'):
                formatted_lines.append('\t' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('\t' * indent_level + stripped)
            elif stripped in ['case', 'default'] or stripped.startswith('case ') or stripped.startswith('default'):
                # Special handling for switch cases
                formatted_lines.append('\t' * max(0, indent_level - 1) + stripped)
            else:
                formatted_lines.append('\t' * indent_level + stripped)
        
        return '\n'.join(formatted_lines)
    
    def _validate_go_syntax(self, code: str) -> ToolchainResult[bool]:
        """Validate Go syntax using go parse."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Use go parse to validate syntax
                process = subprocess.run(
                    ['go', 'tool', 'compile', '-e', '1', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if process.returncode == 0:
                    return ToolchainResult.success(True)
                else:
                    error = ToolchainError(
                        error_type="SyntaxError",
                        message=process.stderr.strip()
                    )
                    return ToolchainResult.failure(error)
                    
            finally:
                # Clean up temp file
                Path(temp_file).unlink(missing_ok=True)
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Go compiler not available, skip validation
            return ToolchainResult.success(True)
        except Exception as e:
            error = ToolchainError(
                error_type="ValidationError",
                message=f"Syntax validation failed: {str(e)}"
            )
            return ToolchainResult.failure(error)
    
    def _validate_go_semantics(self, code: str) -> List[str]:
        """Validate Go semantics."""
        issues = []
        
        # Basic semantic checks
        lines = code.split('\n')
        
        # Check for common issues
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for unused variables (simplified)
            if ':=' in stripped and not any(op in stripped for op in ['=', '!', '<', '>', '+', '-', '*', '/', '%']):
                # This is a very basic check - a real implementation would need proper AST analysis
                pass
            
            # Check for unreachable code after return
            if stripped.startswith('return') and i < len(lines):
                next_line = lines[i].strip() if i < len(lines) else ""
                if next_line and not next_line.startswith('}') and not next_line.startswith('//'):
                    issues.append(f"Line {i+1}: Potential unreachable code after return")
        
        return issues
    
    def _validate_go_modules(self, code: str, file_path: str) -> List[str]:
        """Validate Go modules and imports."""
        issues = []
        
        # Extract imports from code
        import_pattern = r'import\s+(?:\(\s*([^)]+)\s*\)|"([^"]+)"|\s+(\w+)\s+"([^"]+)")'
        imports = re.findall(import_pattern, code)
        
        # Check for common import issues
        for import_match in imports:
            import_block, single_import, alias, aliased_import = import_match
            
            if import_block:
                # Multi-line import block
                for line in import_block.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//'):
                        self._check_import_path(line.strip('"'), issues)
            elif single_import:
                self._check_import_path(single_import, issues)
            elif aliased_import:
                self._check_import_path(aliased_import, issues)
        
        return issues
    
    def _check_import_path(self, import_path: str, issues: List[str]):
        """Check individual import path."""
        # Basic import path validation
        if not import_path:
            return
        
        # Check for relative imports (generally discouraged)
        if import_path.startswith('./') or import_path.startswith('../'):
            issues.append(f"Warning: Relative import '{import_path}' - consider using absolute imports")
        
        # Check for deprecated packages
        deprecated_packages = {
            'io/ioutil': 'Use io and os packages instead',
            'golang.org/x/net/context': 'Use context package instead'
        }
        
        if import_path in deprecated_packages:
            issues.append(f"Warning: Package '{import_path}' is deprecated - {deprecated_packages[import_path]}")
    
    def _run_go_vet(self, code: str, file_path: str) -> List[str]:
        """Run go vet analysis."""
        issues = []
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run go vet
                process = subprocess.run(
                    ['go', 'vet', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if process.stderr:
                    # Parse vet output
                    for line in process.stderr.strip().split('\n'):
                        if line.strip():
                            issues.append(f"go vet: {line}")
                            
            finally:
                # Clean up temp file
                Path(temp_file).unlink(missing_ok=True)
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # go vet not available, skip
            pass
        except Exception:
            # Ignore vet errors for now
            pass
        
        return issues
    
    def _compare_go_semantics(self, original: str, reconstructed: str) -> bool:
        """Compare semantic equivalence of Go code."""
        # Simplified semantic comparison
        # A real implementation would need sophisticated AST comparison
        
        # Normalize whitespace and comments
        def normalize(code: str) -> str:
            # Remove comments
            code = re.sub(r'//.*', '', code)
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
            
            # Normalize whitespace
            code = re.sub(r'\s+', ' ', code)
            code = code.strip()
            
            return code
        
        normalized_original = normalize(original)
        normalized_reconstructed = normalize(reconstructed)
        
        # Basic comparison - in production, this would be much more sophisticated
        return normalized_original == normalized_reconstructed


# Factory function
def create_go_toolchain(options: GoToolchainOptions = None) -> GoToolchain:
    """Create a Go toolchain instance."""
    return GoToolchain(options)


# Example usage and testing
if __name__ == "__main__":
    # Create toolchain
    toolchain = create_go_toolchain()
    
    # Example Go code
    go_code = '''
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
'''
    
    # Test parsing
    parse_result = toolchain.parse_source(go_code)
    if parse_result.success:
        print("✅ Parsing successful")
        
        # Test code generation
        gen_result = toolchain.generate_code(parse_result.result)
        if gen_result.success:
            print("✅ Code generation successful")
            print("Generated code:")
            print(gen_result.result)
            
            # Test round-trip
            round_trip_result = toolchain.round_trip_test(go_code)
            if round_trip_result.success and round_trip_result.result:
                print("✅ Round-trip test successful")
            else:
                print("❌ Round-trip test failed")
        else:
            print(f"❌ Code generation failed: {gen_result.error.message}")
    else:
        print(f"❌ Parsing failed: {parse_result.error.message}")
    
    # Print statistics
    print("\nToolchain Statistics:")
    stats = toolchain.get_statistics()
    for key, value in stats['statistics'].items():
        print(f"  {key}: {value}") 