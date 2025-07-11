"""
Michelson Toolchain for complete smart contract development on Tezos.

This module provides a comprehensive toolchain for Michelson development,
including parsing, AST conversion, code generation, validation, and
Tezos blockchain integration.
"""

import os
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass

from .michelson_ast import *
from .michelson_parser import parse_michelson, parse_michelson_expression
from .michelson_converter import michelson_to_runa, runa_to_michelson
from .michelson_generator import generate_michelson, generate_michelson_compact
from ...runa_ast import RunaASTNode


class MichelsonToolchainError(Exception):
    """Exception raised by the Michelson toolchain."""
    pass


@dataclass
class ContractMetadata:
    """Metadata for a Michelson contract."""
    name: str
    description: str
    author: str
    version: str
    parameter_type: str
    storage_type: str
    entrypoints: List[str]
    gas_limit: Optional[int] = None
    storage_limit: Optional[int] = None


@dataclass
class ValidationResult:
    """Result of contract validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    gas_estimate: Optional[int] = None
    storage_size: Optional[int] = None


@dataclass
class TestResult:
    """Result of contract testing."""
    test_name: str
    passed: bool
    expected_output: Any
    actual_output: Any
    error_message: Optional[str] = None
    gas_used: Optional[int] = None


@dataclass
class DeploymentResult:
    """Result of contract deployment."""
    success: bool
    contract_address: Optional[str] = None
    operation_hash: Optional[str] = None
    error_message: Optional[str] = None
    gas_used: Optional[int] = None
    storage_size: Optional[int] = None


class MichelsonToolchain:
    """Complete toolchain for Michelson smart contract development."""
    
    def __init__(self, 
                 tezos_client_path: Optional[str] = None,
                 tezos_node_url: Optional[str] = None,
                 optimization_level: int = 1):
        """
        Initialize the Michelson toolchain.
        
        Args:
            tezos_client_path: Path to octez-client executable
            tezos_node_url: URL of Tezos node for deployment
            optimization_level: Code optimization level (0-3)
        """
        self.tezos_client_path = tezos_client_path or self._find_tezos_client()
        self.tezos_node_url = tezos_node_url or "http://localhost:8732"
        self.optimization_level = optimization_level
        
        # Compiler settings
        self.settings = {
            'indent_size': 2,
            'optimize': optimization_level > 0,
            'add_comments': True,
            'validate_types': True,
            'check_gas_limits': True,
            'max_gas_limit': 1040000,  # Tezos mainnet limit
            'max_storage_size': 60000   # 60KB storage limit
        }
        
        # Contract cache
        self._contract_cache: Dict[str, MichelsonContract] = {}
        self._validation_cache: Dict[str, ValidationResult] = {}
    
    def _find_tezos_client(self) -> Optional[str]:
        """Try to find octez-client in PATH."""
        for client_name in ['octez-client', 'tezos-client']:
            try:
                result = subprocess.run(['which', client_name], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                continue
        return None
    
    def parse_from_source(self, source: str) -> MichelsonContract:
        """Parse Michelson source code into AST."""
        try:
            contract = parse_michelson(source)
            
            # Cache the parsed contract
            source_hash = str(hash(source))
            self._contract_cache[source_hash] = contract
            
            return contract
        
        except Exception as e:
            raise MichelsonToolchainError(f"Failed to parse Michelson source: {str(e)}")
    
    def parse_from_file(self, file_path: str) -> MichelsonContract:
        """Parse Michelson contract from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            return self.parse_from_source(source)
        
        except FileNotFoundError:
            raise MichelsonToolchainError(f"Contract file not found: {file_path}")
        except Exception as e:
            raise MichelsonToolchainError(f"Failed to parse contract file: {str(e)}")
    
    def convert_to_runa(self, michelson_ast: MichelsonContract) -> RunaASTNode:
        """Convert Michelson AST to Runa AST."""
        try:
            return michelson_to_runa(michelson_ast)
        except Exception as e:
            raise MichelsonToolchainError(f"Failed to convert to Runa AST: {str(e)}")
    
    def convert_from_runa(self, runa_ast: RunaASTNode) -> MichelsonContract:
        """Convert Runa AST to Michelson AST."""
        try:
            result = runa_to_michelson(runa_ast)
            if isinstance(result, MichelsonContract):
                return result
            else:
                raise MichelsonToolchainError(f"Expected MichelsonContract, got {type(result)}")
        except Exception as e:
            raise MichelsonToolchainError(f"Failed to convert from Runa AST: {str(e)}")
    
    def generate_source(self, michelson_ast: MichelsonContract) -> str:
        """Generate Michelson source code from AST."""
        try:
            return generate_michelson(
                michelson_ast,
                indent_size=self.settings['indent_size'],
                optimize=self.settings['optimize'],
                add_comments=self.settings['add_comments']
            )
        except Exception as e:
            raise MichelsonToolchainError(f"Failed to generate Michelson source: {str(e)}")
    
    def validate_contract(self, contract: MichelsonContract, 
                         storage_value: Optional[str] = None) -> ValidationResult:
        """Validate a Michelson contract."""
        errors = []
        warnings = []
        
        try:
            # Generate source for validation
            source = self.generate_source(contract)
            
            # Check if we have cached validation result
            source_hash = str(hash(source))
            if source_hash in self._validation_cache:
                return self._validation_cache[source_hash]
            
            # Basic syntax validation
            try:
                self.parse_from_source(source)
            except Exception as e:
                errors.append(f"Syntax error: {str(e)}")
            
            # Type validation if enabled
            if self.settings['validate_types']:
                type_errors = self._validate_types(contract)
                errors.extend(type_errors)
            
            # Use octez-client for validation if available
            gas_estimate = None
            storage_size = None
            
            if self.tezos_client_path and not errors:
                validation_result = self._validate_with_tezos_client(source, storage_value)
                if validation_result:
                    client_errors, gas_estimate, storage_size = validation_result
                    errors.extend(client_errors)
            
            # Gas limit validation
            if (gas_estimate and self.settings['check_gas_limits'] and 
                gas_estimate > self.settings['max_gas_limit']):
                warnings.append(f"Gas estimate ({gas_estimate}) exceeds limit ({self.settings['max_gas_limit']})")
            
            # Storage size validation
            if (storage_size and storage_size > self.settings['max_storage_size']):
                warnings.append(f"Storage size ({storage_size}) exceeds limit ({self.settings['max_storage_size']})")
            
            result = ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                gas_estimate=gas_estimate,
                storage_size=storage_size
            )
            
            # Cache the result
            self._validation_cache[source_hash] = result
            return result
        
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation failed: {str(e)}"],
                warnings=[]
            )
    
    def _validate_types(self, contract: MichelsonContract) -> List[str]:
        """Perform type validation on contract."""
        errors = []
        
        # Check parameter type validity
        if not self._is_valid_type(contract.parameter_type):
            errors.append("Invalid parameter type")
        
        # Check storage type validity
        if not self._is_valid_type(contract.storage_type):
            errors.append("Invalid storage type")
        
        # TODO: Add more sophisticated type checking
        # - Stack type inference
        # - Instruction type compatibility
        # - Return type verification
        
        return errors
    
    def _is_valid_type(self, type_node: MichelsonType_Node) -> bool:
        """Check if a type is valid."""
        # Basic type validation
        if type_node.type_name in [MichelsonType.PAIR, MichelsonType.OR]:
            return len(type_node.args) >= 2
        elif type_node.type_name in [MichelsonType.OPTION, MichelsonType.LIST, MichelsonType.SET]:
            return len(type_node.args) == 1
        elif type_node.type_name in [MichelsonType.MAP, MichelsonType.BIG_MAP, MichelsonType.LAMBDA]:
            return len(type_node.args) == 2
        else:
            return True
    
    def _validate_with_tezos_client(self, source: str, 
                                   storage_value: Optional[str] = None) -> Optional[Tuple[List[str], Optional[int], Optional[int]]]:
        """Validate contract using octez-client."""
        if not self.tezos_client_path:
            return None
        
        try:
            # Create temporary file for contract
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tz', delete=False) as f:
                f.write(source)
                contract_file = f.name
            
            try:
                # Run typecheck command
                cmd = [self.tezos_client_path, 'typecheck', 'script', contract_file]
                
                if storage_value:
                    cmd.extend(['on', 'storage', storage_value])
                    cmd.extend(['and', 'input', 'Unit'])  # Default parameter
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                errors = []
                gas_estimate = None
                storage_size = None
                
                if result.returncode != 0:
                    error_output = result.stderr.strip()
                    if error_output:
                        errors.append(f"Tezos client error: {error_output}")
                else:
                    # Parse output for gas and storage information
                    output = result.stdout
                    gas_estimate = self._extract_gas_estimate(output)
                    storage_size = self._extract_storage_size(output)
                
                return errors, gas_estimate, storage_size
            
            finally:
                # Clean up temporary file
                os.unlink(contract_file)
        
        except subprocess.TimeoutExpired:
            return ["Validation timeout"], None, None
        except Exception as e:
            return [f"Validation error: {str(e)}"], None, None
    
    def _extract_gas_estimate(self, output: str) -> Optional[int]:
        """Extract gas estimate from octez-client output."""
        # Look for gas consumption patterns
        for line in output.split('\n'):
            if 'gas' in line.lower() and any(c.isdigit() for c in line):
                # Try to extract number from line
                import re
                numbers = re.findall(r'\d+', line)
                if numbers:
                    return int(numbers[0])
        return None
    
    def _extract_storage_size(self, output: str) -> Optional[int]:
        """Extract storage size from octez-client output."""
        # Look for storage size patterns
        for line in output.split('\n'):
            if 'storage' in line.lower() and 'size' in line.lower():
                import re
                numbers = re.findall(r'\d+', line)
                if numbers:
                    return int(numbers[0])
        return None
    
    def test_contract(self, contract: MichelsonContract, 
                     test_cases: List[Dict[str, Any]]) -> List[TestResult]:
        """Test contract with multiple test cases."""
        results = []
        
        for i, test_case in enumerate(test_cases):
            test_name = test_case.get('name', f'test_{i}')
            parameter = test_case.get('parameter', 'Unit')
            storage = test_case.get('storage', 'Unit')
            expected = test_case.get('expected', None)
            
            try:
                result = self._run_single_test(contract, parameter, storage, expected)
                result.test_name = test_name
                results.append(result)
            
            except Exception as e:
                results.append(TestResult(
                    test_name=test_name,
                    passed=False,
                    expected_output=expected,
                    actual_output=None,
                    error_message=str(e)
                ))
        
        return results
    
    def _run_single_test(self, contract: MichelsonContract, 
                        parameter: str, storage: str, 
                        expected: Any) -> TestResult:
        """Run a single test case."""
        if not self.tezos_client_path:
            raise MichelsonToolchainError("Tezos client not available for testing")
        
        # Generate contract source
        source = self.generate_source(contract)
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tz', delete=False) as f:
                f.write(source)
                contract_file = f.name
            
            try:
                # Run script with octez-client
                cmd = [
                    self.tezos_client_path, 'run', 'script', contract_file,
                    'on', 'storage', storage, 'and', 'input', parameter
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    return TestResult(
                        test_name="",
                        passed=False,
                        expected_output=expected,
                        actual_output=None,
                        error_message=result.stderr.strip()
                    )
                
                # Parse output
                output = result.stdout.strip()
                gas_used = self._extract_gas_estimate(output)
                
                # Compare with expected if provided
                passed = True
                if expected is not None:
                    passed = self._compare_outputs(output, expected)
                
                return TestResult(
                    test_name="",
                    passed=passed,
                    expected_output=expected,
                    actual_output=output,
                    gas_used=gas_used
                )
            
            finally:
                os.unlink(contract_file)
        
        except subprocess.TimeoutExpired:
            return TestResult(
                test_name="",
                passed=False,
                expected_output=expected,
                actual_output=None,
                error_message="Test timeout"
            )
    
    def _compare_outputs(self, actual: str, expected: Any) -> bool:
        """Compare actual output with expected result."""
        # Simplified comparison - in practice would need more sophisticated logic
        if isinstance(expected, str):
            return expected in actual
        elif isinstance(expected, dict):
            # Handle structured comparisons
            return all(str(v) in actual for v in expected.values())
        else:
            return str(expected) in actual
    
    def optimize_contract(self, contract: MichelsonContract) -> MichelsonContract:
        """Apply optimizations to a contract."""
        if self.optimization_level == 0:
            return contract
        
        # Generate source with optimizations
        source = generate_michelson(contract, optimize=True)
        
        # Parse back to get optimized AST
        return self.parse_from_source(source)
    
    def create_deployment_package(self, contract: MichelsonContract, 
                                 initial_storage: str,
                                 metadata: Optional[ContractMetadata] = None) -> Dict[str, Any]:
        """Create a deployment package for the contract."""
        package = {
            'contract_source': self.generate_source(contract),
            'initial_storage': initial_storage,
            'timestamp': str(datetime.now()),
            'toolchain_version': '1.0.0'
        }
        
        if metadata:
            package['metadata'] = {
                'name': metadata.name,
                'description': metadata.description,
                'author': metadata.author,
                'version': metadata.version,
                'parameter_type': metadata.parameter_type,
                'storage_type': metadata.storage_type,
                'entrypoints': metadata.entrypoints,
                'gas_limit': metadata.gas_limit,
                'storage_limit': metadata.storage_limit
            }
        
        # Add validation results
        validation = self.validate_contract(contract, initial_storage)
        package['validation'] = {
            'is_valid': validation.is_valid,
            'errors': validation.errors,
            'warnings': validation.warnings,
            'gas_estimate': validation.gas_estimate,
            'storage_size': validation.storage_size
        }
        
        return package
    
    def deploy_contract(self, contract: MichelsonContract,
                       initial_storage: str,
                       sender_account: str,
                       amount: str = "0") -> DeploymentResult:
        """Deploy contract to Tezos network."""
        if not self.tezos_client_path:
            return DeploymentResult(
                success=False,
                error_message="Tezos client not available for deployment"
            )
        
        try:
            # Validate before deployment
            validation = self.validate_contract(contract, initial_storage)
            if not validation.is_valid:
                return DeploymentResult(
                    success=False,
                    error_message=f"Contract validation failed: {'; '.join(validation.errors)}"
                )
            
            # Generate contract source
            source = self.generate_source(contract)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tz', delete=False) as f:
                f.write(source)
                contract_file = f.name
            
            try:
                # Deploy with octez-client
                cmd = [
                    self.tezos_client_path, 'originate', 'contract', 'deployed_contract',
                    'transferring', amount, 'from', sender_account,
                    'running', contract_file, '--init', initial_storage,
                    '--burn-cap', '10'  # Allow up to 10 tez burn for storage
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode != 0:
                    return DeploymentResult(
                        success=False,
                        error_message=result.stderr.strip()
                    )
                
                # Extract contract address and operation hash from output
                output = result.stdout
                contract_address = self._extract_contract_address(output)
                operation_hash = self._extract_operation_hash(output)
                gas_used = self._extract_gas_estimate(output)
                storage_size = self._extract_storage_size(output)
                
                return DeploymentResult(
                    success=True,
                    contract_address=contract_address,
                    operation_hash=operation_hash,
                    gas_used=gas_used,
                    storage_size=storage_size
                )
            
            finally:
                os.unlink(contract_file)
        
        except subprocess.TimeoutExpired:
            return DeploymentResult(
                success=False,
                error_message="Deployment timeout"
            )
        except Exception as e:
            return DeploymentResult(
                success=False,
                error_message=str(e)
            )
    
    def _extract_contract_address(self, output: str) -> Optional[str]:
        """Extract contract address from deployment output."""
        import re
        # Look for KT1 addresses
        match = re.search(r'KT1[A-Za-z0-9]{33}', output)
        return match.group(0) if match else None
    
    def _extract_operation_hash(self, output: str) -> Optional[str]:
        """Extract operation hash from deployment output."""
        import re
        # Look for operation hashes (typically starting with 'o')
        match = re.search(r'o[A-Za-z0-9]{50}', output)
        return match.group(0) if match else None
    
    def compile_project(self, project_dir: str) -> Dict[str, Any]:
        """Compile an entire Michelson project."""
        project_path = Path(project_dir)
        
        if not project_path.exists():
            raise MichelsonToolchainError(f"Project directory not found: {project_dir}")
        
        # Find all .tz files
        contract_files = list(project_path.glob("**/*.tz"))
        
        compilation_results = {}
        
        for contract_file in contract_files:
            try:
                contract = self.parse_from_file(str(contract_file))
                validation = self.validate_contract(contract)
                
                compilation_results[str(contract_file)] = {
                    'success': validation.is_valid,
                    'errors': validation.errors,
                    'warnings': validation.warnings,
                    'gas_estimate': validation.gas_estimate,
                    'storage_size': validation.storage_size
                }
            
            except Exception as e:
                compilation_results[str(contract_file)] = {
                    'success': False,
                    'errors': [str(e)],
                    'warnings': []
                }
        
        return {
            'project_dir': project_dir,
            'contracts': compilation_results,
            'total_contracts': len(contract_files),
            'successful': sum(1 for r in compilation_results.values() if r['success']),
            'failed': sum(1 for r in compilation_results.values() if not r['success'])
        }
    
    def get_contract_info(self, contract: MichelsonContract) -> Dict[str, Any]:
        """Get detailed information about a contract."""
        validation = self.validate_contract(contract)
        
        return {
            'parameter_type': self.generate_source(contract.parameter_type) if hasattr(contract.parameter_type, 'type_name') else str(contract.parameter_type),
            'storage_type': self.generate_source(contract.storage_type) if hasattr(contract.storage_type, 'type_name') else str(contract.storage_type),
            'instruction_count': len(contract.code.instructions),
            'validation': {
                'is_valid': validation.is_valid,
                'errors': validation.errors,
                'warnings': validation.warnings,
                'gas_estimate': validation.gas_estimate,
                'storage_size': validation.storage_size
            },
            'complexity_score': self._calculate_complexity(contract),
            'optimization_opportunities': self._find_optimization_opportunities(contract)
        }
    
    def _calculate_complexity(self, contract: MichelsonContract) -> int:
        """Calculate a complexity score for the contract."""
        score = 0
        
        # Base score from instruction count
        score += len(contract.code.instructions)
        
        # Add complexity for nested structures
        for instruction in contract.code.instructions:
            if hasattr(instruction, 'args') and instruction.args:
                for arg in instruction.args:
                    if isinstance(arg, MichelsonSequence):
                        score += len(arg.instructions) * 2  # Nested instructions are more complex
        
        return score
    
    def _find_optimization_opportunities(self, contract: MichelsonContract) -> List[str]:
        """Find potential optimization opportunities."""
        opportunities = []
        
        instructions = contract.code.instructions
        
        for i in range(len(instructions) - 1):
            current = instructions[i]
            next_instr = instructions[i + 1]
            
            # Look for common optimization patterns
            if (current.instruction == MichelsonInstruction.DUP and
                next_instr.instruction == MichelsonInstruction.DROP):
                opportunities.append(f"Remove redundant DUP/DROP at instruction {i}")
            
            elif (current.instruction == MichelsonInstruction.PUSH and
                  next_instr.instruction == MichelsonInstruction.DROP):
                opportunities.append(f"Remove redundant PUSH/DROP at instruction {i}")
        
        return opportunities


# Convenience functions for common operations
def parse_michelson_file(file_path: str) -> MichelsonContract:
    """Parse a Michelson contract file."""
    toolchain = MichelsonToolchain()
    return toolchain.parse_from_file(file_path)


def validate_michelson_file(file_path: str) -> ValidationResult:
    """Validate a Michelson contract file."""
    toolchain = MichelsonToolchain()
    contract = toolchain.parse_from_file(file_path)
    return toolchain.validate_contract(contract)


def compile_michelson_to_runa(michelson_source: str) -> RunaASTNode:
    """Compile Michelson source to Runa AST."""
    toolchain = MichelsonToolchain()
    contract = toolchain.parse_from_source(michelson_source)
    return toolchain.convert_to_runa(contract)


def compile_runa_to_michelson(runa_ast: RunaASTNode) -> str:
    """Compile Runa AST to Michelson source."""
    toolchain = MichelsonToolchain()
    contract = toolchain.convert_from_runa(runa_ast)
    return toolchain.generate_source(contract)


# Import datetime for timestamps
from datetime import datetime 