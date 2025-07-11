"""
SmartPy Language Toolchain

Integrated toolchain for SmartPy language support including parsing, AST conversion,
code generation, validation, and smart contract testing.
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Union, Any, Tuple
from pathlib import Path

from runa.ast.base import RunaNode
from runa.tools.validation import ValidationResult, ValidationError
from runa.tools.testing import TestResult, TestCase

from .smartpy_ast import *
from .smartpy_parser import SmartPyParser, SmartPyLexer
from .smartpy_converter import SmartPyToRunaConverter, RunaToSmartPyConverter
from .smartpy_generator import SmartPyGenerator, generate_smartpy_code


class SmartPyToolchain:
    """Comprehensive SmartPy language toolchain."""
    
    def __init__(self):
        self.parser = SmartPyParser()
        self.lexer = SmartPyLexer()
        self.to_runa_converter = SmartPyToRunaConverter()
        self.from_runa_converter = RunaToSmartPyConverter()
        self.generator = SmartPyGenerator()
        
        # SmartPy compilation settings
        self.compile_options = {
            'target': 'michelson',
            'protocol': 'PtNairob',
            'output_format': 'tz'
        }
        
        self.test_options = {
            'html_output': True,
            'verbose': True
        }
    
    # Core parsing and generation
    def parse_file(self, file_path: Union[str, Path]) -> SmartPyModule:
        """Parse a SmartPy file and return the AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            return self.parse_string(source_code, str(file_path))
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except UnicodeDecodeError:
            raise ValueError(f"Unable to decode file: {file_path}")
    
    def parse_string(self, source_code: str, filename: Optional[str] = None) -> SmartPyModule:
        """Parse SmartPy source code string and return the AST."""
        try:
            # Tokenize
            tokens = self.lexer.tokenize(source_code, filename or "unknown")
            
            # Parse
            ast = self.parser.parse(tokens, filename)
            
            return ast
        except Exception as e:
            raise ValueError(f"Parse error: {str(e)}")
    
    def generate_code(self, ast: SmartPyNode, format_output: bool = True) -> str:
        """Generate SmartPy source code from AST."""
        try:
            code = self.generator.generate(ast)
            
            if format_output:
                code = self.format_code(code)
            
            return code
        except Exception as e:
            raise ValueError(f"Code generation error: {str(e)}")
    
    def format_code(self, code: str) -> str:
        """Format SmartPy code with proper indentation."""
        # Basic formatting - could be enhanced with black or similar
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped:
                formatted_lines.append(stripped)
            else:
                formatted_lines.append('')
        
        return '\n'.join(formatted_lines)
    
    # AST conversion
    def to_runa_ast(self, smartpy_ast: SmartPyNode) -> RunaNode:
        """Convert SmartPy AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(smartpy_ast)
        except Exception as e:
            raise ValueError(f"SmartPy to Runa conversion error: {str(e)}")
    
    def from_runa_ast(self, runa_ast: RunaNode) -> SmartPyNode:
        """Convert Runa AST to SmartPy AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise ValueError(f"Runa to SmartPy conversion error: {str(e)}")
    
    # Full pipeline operations
    def runa_to_smartpy(self, runa_code: str) -> str:
        """Convert Runa code to SmartPy code."""
        # This would need the Runa parser, which we'll assume is available
        # For now, we'll create a placeholder
        # TODO: Implement Runa parser integration needed
            return StringLiteral(value="Runa parser integration needed_placeholder")
    
    def smartpy_to_runa(self, smartpy_code: str) -> str:
        """Convert SmartPy code to Runa code."""
        # Parse SmartPy
        smartpy_ast = self.parse_string(smartpy_code)
        
        # Convert to Runa AST
        runa_ast = self.to_runa_ast(smartpy_ast)
        
        # Generate Runa code (would need Runa generator)
        # For now, return string representation
        return str(runa_ast)
    
    # Validation and analysis
    def validate_syntax(self, source_code: str) -> ValidationResult:
        """Validate SmartPy syntax."""
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
    
    def _check_semantics(self, ast: SmartPyModule) -> List[ValidationError]:
        """Perform basic semantic analysis."""
        errors = []
        
        # Check for contracts inheriting from sp.Contract
        for decl in ast.declarations:
            if isinstance(decl, SmartPyContractDef):
                if "sp.Contract" not in decl.base_classes and "Contract" not in decl.base_classes:
                    errors.append(ValidationError(
                        message=f"Contract {decl.name} should inherit from sp.Contract",
                        line=getattr(decl.source_info, 'line', 0) if decl.source_info else 0,
                        column=getattr(decl.source_info, 'column', 0) if decl.source_info else 0,
                        severity="warning"
                    ))
                
                # Check for __init__ method
                if not decl.init_method:
                    errors.append(ValidationError(
                        message=f"Contract {decl.name} should have an __init__ method",
                        line=getattr(decl.source_info, 'line', 0) if decl.source_info else 0,
                        column=getattr(decl.source_info, 'column', 0) if decl.source_info else 0,
                        severity="warning"
                    ))
                
                # Check for entry points
                if not decl.entry_points:
                    errors.append(ValidationError(
                        message=f"Contract {decl.name} should have at least one entry point",
                        line=getattr(decl.source_info, 'line', 0) if decl.source_info else 0,
                        column=getattr(decl.source_info, 'column', 0) if decl.source_info else 0,
                        severity="warning"
                    ))
        
        return errors
    
    def analyze_gas_usage(self, source_code: str) -> Dict[str, Any]:
        """Analyze estimated gas usage for SmartPy contract."""
        ast = self.parse_string(source_code)
        
        # Basic gas estimation heuristics
        gas_estimate = 0
        complexity_factors = {
            'entry_points': 0,
            'function_calls': 0,
            'loop_iterations': 0,
            'storage_operations': 0,
            'map_operations': 0,
            'verify_calls': 0
        }
        
        # Traverse AST and count operations
        self._analyze_gas_recursive(ast, complexity_factors)
        
        # Calculate estimate
        gas_estimate = (
            complexity_factors['entry_points'] * 1000 +
            complexity_factors['function_calls'] * 100 +
            complexity_factors['loop_iterations'] * 500 +
            complexity_factors['storage_operations'] * 200 +
            complexity_factors['map_operations'] * 300 +
            complexity_factors['verify_calls'] * 50
        )
        
        return {
            'estimated_gas': gas_estimate,
            'complexity_factors': complexity_factors,
            'optimization_suggestions': self._get_gas_optimizations(complexity_factors)
        }
    
    def _analyze_gas_recursive(self, node: SmartPyNode, factors: Dict[str, int]):
        """Recursively analyze gas usage in AST."""
        if isinstance(node, SmartPyMethodDef) and node.is_entry_point:
            factors['entry_points'] += 1
        elif isinstance(node, SmartPyFunctionCall):
            factors['function_calls'] += 1
            # Check for specific SmartPy functions
            if isinstance(node.function, SmartPyAttributeAccess):
                if node.function.attribute in ['get', 'contains', 'update']:
                    factors['map_operations'] += 1
        elif isinstance(node, SmartPyVerify):
            factors['verify_calls'] += 1
        elif isinstance(node, SmartPyFor) or isinstance(node, SmartPyWhile):
            factors['loop_iterations'] += 1
        elif isinstance(node, SmartPyAssignment):
            if isinstance(node.target, SmartPyAttributeAccess):
                if hasattr(node.target.object, 'name') and node.target.object.name == 'self':
                    factors['storage_operations'] += 1
        
        # Recursively check child nodes
        for attr_name in dir(node):
            if not attr_name.startswith('_'):
                attr_value = getattr(node, attr_name)
                if isinstance(attr_value, SmartPyNode):
                    self._analyze_gas_recursive(attr_value, factors)
                elif isinstance(attr_value, list):
                    for item in attr_value:
                        if isinstance(item, SmartPyNode):
                            self._analyze_gas_recursive(item, factors)
    
    def _get_gas_optimizations(self, factors: Dict[str, int]) -> List[str]:
        """Get gas optimization suggestions."""
        suggestions = []
        
        if factors['map_operations'] > 10:
            suggestions.append("Consider using sp.big_map for large datasets")
        
        if factors['verify_calls'] > 5:
            suggestions.append("Consider combining multiple sp.verify calls")
        
        if factors['loop_iterations'] > 3:
            suggestions.append("Minimize loop operations to reduce gas costs")
        
        if factors['storage_operations'] > 10:
            suggestions.append("Batch storage operations when possible")
        
        return suggestions
    
    # Compilation and testing
    def compile_contract(self, source_file: Union[str, Path], 
                        output_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """Compile SmartPy contract to Michelson."""
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise ValueError(f"Source file not found: {source_file}")
        
        if output_dir is None:
            output_dir = source_path.parent / "build"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        try:
            # Try to use SmartPy CLI if available
            result = self._run_smartpy_compile(source_path, output_dir)
            
            return {
                'success': True,
                'output_dir': str(output_dir),
                'michelson_file': result.get('michelson_file'),
                'output': result.get('output', ''),
                'warnings': result.get('warnings', [])
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output_dir': str(output_dir)
            }
    
    def _run_smartpy_compile(self, source_file: Path, output_dir: Path) -> Dict[str, Any]:
        """Run SmartPy compiler."""
        cmd = [
            'SmartPy.sh', 'compile',
            str(source_file),
            str(output_dir),
            '--protocol', self.compile_options['protocol']
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Find generated Michelson file
                michelson_files = list(output_dir.glob("*.tz"))
                michelson_file = michelson_files[0] if michelson_files else None
                
                return {
                    'output': result.stdout,
                    'warnings': result.stderr.split('\n') if result.stderr else [],
                    'michelson_file': str(michelson_file) if michelson_file else None
                }
            else:
                raise RuntimeError(f"Compilation failed: {result.stderr}")
        
        except FileNotFoundError:
            raise RuntimeError("SmartPy CLI not found. Please install SmartPy.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Compilation timed out")
    
    def run_tests(self, source_file: Union[str, Path]) -> TestResult:
        """Run SmartPy tests."""
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise ValueError(f"Source file not found: {source_file}")
        
        try:
            # Try to run SmartPy test
            result = self._run_smartpy_test(source_path)
            
            passed = result['returncode'] == 0
            output = result['output']
            
            return TestResult(
                passed=passed,
                output=output,
                test_cases=self._parse_test_output(output)
            )
        
        except Exception as e:
            return TestResult(
                passed=False,
                output=str(e),
                test_cases=[]
            )
    
    def _run_smartpy_test(self, source_file: Path) -> Dict[str, Any]:
        """Run SmartPy test command."""
        cmd = [
            'SmartPy.sh', 'test',
            str(source_file),
            str(source_file.parent / "test_output")
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return {
                'returncode': result.returncode,
                'output': result.stdout + result.stderr
            }
        
        except FileNotFoundError:
            raise RuntimeError("SmartPy CLI not found for testing")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Test execution timed out")
    
    def _parse_test_output(self, output: str) -> List[TestCase]:
        """Parse SmartPy test output into test cases."""
        test_cases = []
        lines = output.split('\n')
        
        current_test = None
        for line in lines:
            if 'test' in line.lower() and ('passed' in line.lower() or 'failed' in line.lower()):
                if current_test:
                    test_cases.append(current_test)
                
                test_name = "test_function"  # SmartPy test names are generic
                passed = 'passed' in line.lower() or 'ok' in line.lower()
                
                current_test = TestCase(
                    name=test_name,
                    passed=passed,
                    output=line
                )
        
        if current_test:
            test_cases.append(current_test)
        
        return test_cases
    
    # Utility methods
    def get_language_info(self) -> Dict[str, Any]:
        """Get information about SmartPy language."""
        return {
            'name': 'SmartPy',
            'version': '1.0',
            'file_extension': '.py',
            'blockchain': 'Tezos',
            'target': 'Michelson',
            'features': {
                'python_syntax': True,
                'type_inference': True,
                'smart_contracts': True,
                'testing_framework': True,
                'formal_verification': False
            }
        }
    
    def create_contract_template(self, contract_name: str) -> str:
        """Create a SmartPy contract template."""
        template = f'''import smartpy as sp

class {contract_name}(sp.Contract):
    def __init__(self):
        self.init(
            # Define your storage here
            value=sp.int(0)
        )
    
    @sp.entry_point
    def set_value(self, params):
        sp.verify(params.value >= 0, "Value must be non-negative")
        self.data.value = params.value
    
    @sp.entry_point
    def get_value(self):
        sp.result(self.data.value)

@sp.add_test(name="Test {contract_name}")
def test():
    scenario = sp.test_scenario()
    
    # Create contract instance
    contract = {contract_name}()
    scenario += contract
    
    # Test setting value
    scenario += contract.set_value(value=42)
    
    # Verify storage
    scenario.verify(contract.data.value == 42)
'''
        return template


# Create toolchain instance
toolchain = SmartPyToolchain()

# Convenience functions
def parse_smartpy(code: str) -> SmartPyModule:
    """Parse SmartPy code."""
    return toolchain.parse_string(code)

def generate_smartpy(ast: SmartPyNode) -> str:
    """Generate SmartPy code."""
    return toolchain.generate_code(ast)

def validate_smartpy(code: str) -> ValidationResult:
    """Validate SmartPy code."""
    return toolchain.validate_syntax(code) 