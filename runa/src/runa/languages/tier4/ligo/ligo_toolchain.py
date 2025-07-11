"""
LIGO Language Toolchain

Integrated toolchain for LIGO language support including parsing, AST conversion,
code generation, validation, and smart contract deployment utilities.
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Union, Any, Tuple
from pathlib import Path

from runa.ast.base import RunaNode
from runa.tools.validation import ValidationResult, ValidationError
from runa.tools.testing import TestResult, TestCase

from .ligo_ast import *
from .ligo_parser import LIGOParser, LIGOLexer
from .ligo_converter import LIGOToRunaConverter, RunaToLIGOConverter
from .ligo_generator import LIGOGenerator, generate_ligo_code


class LIGOToolchain:
    """Comprehensive LIGO language toolchain."""
    
    def __init__(self, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO):
        self.syntax_style = syntax_style
        self.parser = LIGOParser(syntax_style)
        self.lexer = LIGOLexer(syntax_style)
        self.to_runa_converter = LIGOToRunaConverter(syntax_style)
        self.from_runa_converter = RunaToLIGOConverter(syntax_style)
        self.generator = LIGOGenerator(syntax_style)
        
        # Compilation and deployment settings
        self.compile_options = {
            'protocol': 'PtNairob',  # Latest Tezos protocol
            'warn_unused_recursion': True,
            'no_warn': [],
            'syntax': 'jsligo' if syntax_style == LIGOSyntax.JSLIGO else 'cameligo'
        }
        
        self.network_config = {
            'rpc_endpoint': 'https://mainnet.api.tez.ie',
            'testnet_endpoint': 'https://ghostnet.api.tez.ie',
            'gas_limit': 1040000,
            'storage_limit': 60000
        }
    
    # Core parsing and generation
    def parse_file(self, file_path: Union[str, Path]) -> LIGOProgram:
        """Parse a LIGO file and return the AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            return self.parse_string(source_code, str(file_path))
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except UnicodeDecodeError:
            raise ValueError(f"Unable to decode file: {file_path}")
    
    def parse_string(self, source_code: str, filename: Optional[str] = None) -> LIGOProgram:
        """Parse LIGO source code string and return the AST."""
        try:
            # Tokenize
            tokens = self.lexer.tokenize(source_code)
            
            # Parse
            ast = self.parser.parse(tokens, filename)
            
            if not isinstance(ast, LIGOProgram):
                # Wrap in program if needed
                ast = LIGOProgram(
                    name=filename or "anonymous",
                    declarations=[ast] if ast else [],
                    syntax_style=self.syntax_style
                )
            
            return ast
        except Exception as e:
            raise ValueError(f"Parse error: {str(e)}")
    
    def generate_code(self, ast: LIGONode, format_output: bool = True) -> str:
        """Generate LIGO source code from AST."""
        try:
            code = self.generator.generate(ast)
            
            if format_output:
                code = self.format_code(code)
            
            return code
        except Exception as e:
            raise ValueError(f"Code generation error: {str(e)}")
    
    def format_code(self, code: str) -> str:
        """Format LIGO code with proper indentation."""
        from .ligo_generator import format_ligo_code
        return format_ligo_code(code, self.syntax_style)
    
    # AST conversion
    def to_runa_ast(self, ligo_ast: LIGONode) -> RunaNode:
        """Convert LIGO AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(ligo_ast)
        except Exception as e:
            raise ValueError(f"LIGO to Runa conversion error: {str(e)}")
    
    def from_runa_ast(self, runa_ast: RunaNode) -> LIGONode:
        """Convert Runa AST to LIGO AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise ValueError(f"Runa to LIGO conversion error: {str(e)}")
    
    # Full pipeline operations
    def runa_to_ligo(self, runa_code: str) -> str:
        """Convert Runa code to LIGO code."""
        # This would need the Runa parser, which we'll assume is available
        # For now, we'll create a placeholder
        # TODO: Implement Runa parser integration needed
            return StringLiteral(value="Runa parser integration needed_placeholder")
    
    def ligo_to_runa(self, ligo_code: str) -> str:
        """Convert LIGO code to Runa code."""
        # Parse LIGO
        ligo_ast = self.parse_string(ligo_code)
        
        # Convert to Runa AST
        runa_ast = self.to_runa_ast(ligo_ast)
        
        # Generate Runa code (would need Runa generator)
        # For now, return string representation
        return str(runa_ast)
    
    def translate_code(self, source_code: str, target_syntax: LIGOSyntax) -> str:
        """Translate between JsLIGO and CameLIGO syntaxes."""
        if target_syntax == self.syntax_style:
            return source_code
        
        # Parse with current syntax
        ast = self.parse_string(source_code)
        
        # Generate with target syntax
        target_generator = LIGOGenerator(target_syntax)
        return target_generator.generate(ast)
    
    # Validation and analysis
    def validate_syntax(self, source_code: str) -> ValidationResult:
        """Validate LIGO syntax."""
        errors = []
        warnings = []
        
        try:
            # Try to parse
            ast = self.parse_string(source_code)
            
            # Basic semantic checks
            semantic_errors = self._check_semantics(ast)
            errors.extend(semantic_errors)
            
        except Exception as e:
            errors.append(ValidationError(
                message=str(e),
                line=0,
                column=0,
                severity="error"
            ))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _check_semantics(self, ast: LIGOProgram) -> List[ValidationError]:
        """Perform basic semantic analysis."""
        errors = []
        
        # Check for duplicate declarations
        declared_names = set()
        for decl in ast.declarations:
            if hasattr(decl, 'name'):
                if decl.name in declared_names:
                    errors.append(ValidationError(
                        message=f"Duplicate declaration: {decl.name}",
                        line=getattr(decl.source_info, 'line', 0) if decl.source_info else 0,
                        column=getattr(decl.source_info, 'column', 0) if decl.source_info else 0,
                        severity="error"
                    ))
                declared_names.add(decl.name)
        
        return errors
    
    def analyze_gas_usage(self, source_code: str) -> Dict[str, Any]:
        """Analyze estimated gas usage for LIGO contract."""
        ast = self.parse_string(source_code)
        
        # Basic gas estimation heuristics
        gas_estimate = 0
        complexity_factors = {
            'function_calls': 0,
            'loop_iterations': 0,
            'storage_operations': 0,
            'map_operations': 0
        }
        
        # Traverse AST and count operations
        self._analyze_gas_recursive(ast, complexity_factors)
        
        # Calculate estimate
        gas_estimate = (
            complexity_factors['function_calls'] * 100 +
            complexity_factors['loop_iterations'] * 500 +
            complexity_factors['storage_operations'] * 1000 +
            complexity_factors['map_operations'] * 200
        )
        
        return {
            'estimated_gas': gas_estimate,
            'complexity_factors': complexity_factors,
            'optimization_suggestions': self._get_gas_optimizations(complexity_factors)
        }
    
    def _analyze_gas_recursive(self, node: LIGONode, factors: Dict[str, int]):
        """Recursively analyze gas usage in AST."""
        if isinstance(node, LIGOFunctionCall):
            factors['function_calls'] += 1
        elif isinstance(node, LIGOMapAccess):
            factors['map_operations'] += 1
        
        # Recursively check child nodes
        for attr_name in dir(node):
            if not attr_name.startswith('_'):
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, LIGONode):
                    self._analyze_gas_recursive(attr_value, factors)
                elif isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, LIGONode):
                            self._analyze_gas_recursive(item, factors)
    
    def _get_gas_optimizations(self, factors: Dict[str, int]) -> List[str]:
        """Get gas optimization suggestions."""
        suggestions = []
        
        if factors['map_operations'] > 10:
            suggestions.append("Consider using big_map for large datasets")
        
        if factors['function_calls'] > 20:
            suggestions.append("Consider inlining small functions")
        
        if factors['storage_operations'] > 5:
            suggestions.append("Batch storage operations when possible")
        
        return suggestions
    
    # Compilation and deployment
    def compile_contract(self, source_file: Union[str, Path], 
                        output_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """Compile LIGO contract to Michelson."""
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise ValueError(f"Source file not found: {source_file}")
        
        if output_dir is None:
            output_dir = source_path.parent / "build"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Compile to Michelson
        michelson_file = output_dir / f"{source_path.stem}.tz"
        
        try:
            # Use LIGO compiler if available
            result = self._run_ligo_compiler(source_path, michelson_file)
            
            return {
                'success': True,
                'michelson_file': str(michelson_file),
                'output': result.get('output', ''),
                'warnings': result.get('warnings', [])
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'michelson_file': None
            }
    
    def _run_ligo_compiler(self, source_file: Path, output_file: Path) -> Dict[str, Any]:
        """Run the LIGO compiler."""
        cmd = [
            'ligo', 'compile', 'contract',
            str(source_file),
            '--syntax', self.compile_options['syntax'],
            '--protocol', self.compile_options['protocol']
        ]
        
        if self.compile_options.get('warn_unused_recursion'):
            cmd.append('--warn-unused-recursion')
        
        for warning in self.compile_options.get('no_warn', []):
            cmd.extend(['--no-warn', warning])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Write output to file
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                
                return {
                    'output': result.stdout,
                    'warnings': result.stderr.split('\n') if result.stderr else []
                }
            else:
                raise RuntimeError(f"Compilation failed: {result.stderr}")
        
        except FileNotFoundError:
            raise RuntimeError("LIGO compiler not found. Please install LIGO.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Compilation timed out")
    
    def generate_deployment_script(self, contract_file: Union[str, Path],
                                 storage_params: Dict[str, Any]) -> str:
        """Generate deployment script for Tezos."""
        template = f'''#!/bin/bash

# LIGO Contract Deployment Script
# Generated automatically by Runa LIGO Toolchain

CONTRACT_FILE="{contract_file}"
NETWORK="ghostnet"  # Change to mainnet for production
RPC_ENDPOINT="{self.network_config['testnet_endpoint']}"

# Compile contract
echo "Compiling contract..."
ligo compile contract $CONTRACT_FILE --syntax {self.compile_options['syntax']} > contract.tz

# Compile initial storage
echo "Compiling initial storage..."
echo '{self._format_storage_params(storage_params)}' > storage.ligo
ligo compile storage storage.ligo '{self._format_storage_params(storage_params)}' --syntax {self.compile_options['syntax']} > storage.tz

# Deploy using Tezos client
echo "Deploying to $NETWORK..."
tezos-client --endpoint $RPC_ENDPOINT originate contract my_contract \\
    transferring 0 from $SOURCE_ACCOUNT \\
    running contract.tz \\
    --init "$(cat storage.tz)" \\
    --gas-limit {self.network_config['gas_limit']} \\
    --storage-limit {self.network_config['storage_limit']} \\
    --burn-cap 10

echo "Deployment complete!"
'''
        return template
    
    def _format_storage_params(self, params: Dict[str, Any]) -> str:
        """Format storage parameters for LIGO."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            return str(params).replace("'", '"')
        else:
            # CameLIGO format
            formatted = []
            for key, value in params.items():
                if isinstance(value, str):
                    formatted.append(f'{key} = "{value}"')
                else:
                    formatted.append(f'{key} = {value}')
            return '{' + '; '.join(formatted) + '}'
    
    # Testing support
    def run_tests(self, test_file: Union[str, Path]) -> TestResult:
        """Run LIGO tests."""
        test_path = Path(test_file)
        
        if not test_path.exists():
            raise ValueError(f"Test file not found: {test_file}")
        
        try:
            # Run LIGO test command
            cmd = [
                'ligo', 'run', 'test',
                str(test_path),
                '--syntax', self.compile_options['syntax']
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse test results
            passed = result.returncode == 0
            output = result.stdout + result.stderr
            
            return TestResult(
                passed=passed,
                output=output,
                test_cases=self._parse_test_output(output)
            )
        
        except FileNotFoundError:
            raise RuntimeError("LIGO compiler not found for testing")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Test execution timed out")
    
    def _parse_test_output(self, output: str) -> List[TestCase]:
        """Parse LIGO test output into test cases."""
        test_cases = []
        lines = output.split('\n')
        
        current_test = None
        for line in lines:
            if 'test_' in line and ('passed' in line or 'failed' in line):
                if current_test:
                    test_cases.append(current_test)
                
                test_name = line.split()[0] if line.split() else "unknown"
                passed = 'passed' in line.lower()
                
                current_test = TestCase(
                    name=test_name,
                    passed=passed,
                    output=line
                )
        
        if current_test:
            test_cases.append(current_test)
        
        return test_cases
    
    # Utility methods
    def get_syntax_info(self) -> Dict[str, Any]:
        """Get information about the current syntax style."""
        return {
            'syntax': self.syntax_style.value,
            'file_extension': '.jsligo' if self.syntax_style == LIGOSyntax.JSLIGO else '.mligo',
            'features': {
                'javascript_like': self.syntax_style == LIGOSyntax.JSLIGO,
                'functional': True,
                'type_safe': True,
                'smart_contracts': True
            }
        }
    
    def optimize_code(self, source_code: str) -> str:
        """Apply basic optimizations to LIGO code."""
        ast = self.parse_string(source_code)
        
        # Apply optimizations
        optimized_ast = self._apply_optimizations(ast)
        
        # Generate optimized code
        return self.generate_code(optimized_ast)
    
    def _apply_optimizations(self, ast: LIGOProgram) -> LIGOProgram:
        """Apply AST-level optimizations."""
        # Placeholder for optimization logic
        # Could include:
        # - Constant folding
        # - Dead code elimination  
        # - Function inlining for small functions
        # - Loop unrolling
        return ast


# Create toolchain instance
toolchain = LIGOToolchain()

# Convenience functions
def parse_ligo(code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> LIGOProgram:
    """Parse LIGO code with specified syntax."""
    tc = LIGOToolchain(syntax)
    return tc.parse_string(code)

def generate_ligo(ast: LIGONode, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> str:
    """Generate LIGO code with specified syntax."""
    tc = LIGOToolchain(syntax)
    return tc.generate_code(ast)

def translate_syntax(code: str, from_syntax: LIGOSyntax, to_syntax: LIGOSyntax) -> str:
    """Translate between LIGO syntaxes."""
    tc = LIGOToolchain(from_syntax)
    return tc.translate_code(code, to_syntax)

def validate_ligo(code: str, syntax: LIGOSyntax = LIGOSyntax.JSLIGO) -> ValidationResult:
    """Validate LIGO code."""
    tc = LIGOToolchain(syntax)
    return tc.validate_syntax(code) 