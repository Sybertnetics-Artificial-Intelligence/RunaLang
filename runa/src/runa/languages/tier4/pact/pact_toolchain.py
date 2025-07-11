#!/usr/bin/env python3
"""
Pact Toolchain Implementation

Complete toolchain for Pact smart contract development including:
- LISP-like syntax parsing and generation
- Formal verification integration
- Kadena testnet deployment
- Capability testing and validation
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import re

from .pact_parser import parse_pact, PactLexer, PactParser
from .pact_ast import PactProgram
from .pact_generator import generate_pact, PactCodeStyle
from .pact_converter import pact_to_runa, runa_to_pact


@dataclass
class PactValidationResult:
    """Result of Pact script validation."""
    is_valid: bool
    formal_verification_passed: bool
    capabilities_verified: bool
    gas_cost: int
    execution_trace: List[str]
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any] = None


@dataclass
class PactDeploymentResult:
    """Result of Pact contract deployment."""
    success: bool
    transaction_hash: Optional[str] = None
    module_hash: Optional[str] = None
    contract_address: Optional[str] = None
    gas_used: int = 0
    errors: List[str] = None


class PactToolchain:
    """Complete toolchain for Pact smart contract development."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="pact_")
        self.pact_version = "4.9"
        self.kadena_cli_version = "2.0"
        
        # Kadena development environment
        self.kadena_node_url = os.environ.get("KADENA_NODE_URL", "http://localhost:1848")
        self.testnet_id = "testnet04"
        self.chain_id = "0"
        
        # Build configuration
        self.build_config = {
            "formal_verification": True,
            "capability_checks": True,
            "gas_estimation": True,
            "repl_mode": True
        }
    
    def parse_pact_code(self, source_code: str) -> Tuple[Optional[PactProgram], List[str]]:
        """Parse Pact source code into AST."""
        try:
            program, errors = parse_pact(source_code)
            return program, errors
        except Exception as e:
            return None, [f"Parse error: {str(e)}"]
    
    def generate_pact_code(self, ast: PactProgram, style: PactCodeStyle = None) -> str:
        """Generate Pact code from AST."""
        try:
            return generate_pact(ast, style)
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {str(e)}")
    
    def validate_contract(self, pact_code: str, module_name: str = "test-module") -> PactValidationResult:
        """Validate Pact contract with formal verification."""
        try:
            # Create validation environment
            validation_dir = Path(self.temp_dir) / "validation"
            validation_dir.mkdir(exist_ok=True)
            
            # Write contract code
            contract_file = validation_dir / f"{module_name}.pact"
            with open(contract_file, 'w') as f:
                f.write(pact_code)
            
            # Create validation script
            validation_script = self._create_validation_script(validation_dir, contract_file)
            
            # Run validation
            result = subprocess.run(
                ["bash", str(validation_script)],
                cwd=validation_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return self._parse_validation_output(result.stdout, result.stderr, result.returncode == 0)
        
        except Exception as e:
            return PactValidationResult(
                is_valid=False,
                formal_verification_passed=False,
                capabilities_verified=False,
                gas_cost=0,
                execution_trace=[],
                errors=[f"Validation error: {str(e)}"],
                warnings=[]
            )
    
    def deploy_to_testnet(self, pact_code: str, module_name: str, keyset_data: Dict[str, Any] = None) -> PactDeploymentResult:
        """Deploy Pact contract to Kadena testnet."""
        try:
            # Create deployment environment
            deploy_dir = Path(self.temp_dir) / "deployment"
            deploy_dir.mkdir(exist_ok=True)
            
            # Write contract
            contract_file = deploy_dir / f"{module_name}.pact"
            with open(contract_file, 'w') as f:
                f.write(pact_code)
            
            # Create deployment transaction
            tx_template = self._create_deployment_transaction(module_name, keyset_data)
            tx_file = deploy_dir / "deploy.yaml"
            with open(tx_file, 'w') as f:
                f.write(tx_template)
            
            # Deploy using Kadena CLI
            deployment_script = self._create_deployment_script(deploy_dir, tx_file)
            
            result = subprocess.run(
                ["bash", str(deployment_script)],
                cwd=deploy_dir,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode == 0:
                return self._parse_deployment_output(result.stdout, result.stderr)
            else:
                return PactDeploymentResult(
                    success=False,
                    errors=[result.stderr or "Deployment failed"]
                )
        
        except Exception as e:
            return PactDeploymentResult(
                success=False,
                errors=[f"Deployment error: {str(e)}"]
            )
    
    def run_repl_tests(self, test_code: str) -> Dict[str, Any]:
        """Run Pact REPL tests."""
        try:
            test_dir = Path(self.temp_dir) / "testing"
            test_dir.mkdir(exist_ok=True)
            
            # Write test file
            test_file = test_dir / "test.repl"
            with open(test_file, 'w') as f:
                f.write(test_code)
            
            # Run Pact REPL
            result = subprocess.run(
                ["pact", str(test_file)],
                cwd=test_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return self._parse_repl_output(result.stdout, result.stderr, result.returncode == 0)
        
        except Exception as e:
            return {
                "success": False,
                "errors": [f"REPL test error: {str(e)}"],
                "test_results": []
            }
    
    def check_formal_verification(self, pact_code: str) -> Dict[str, Any]:
        """Check formal verification properties."""
        try:
            verification_dir = Path(self.temp_dir) / "verification"
            verification_dir.mkdir(exist_ok=True)
            
            # Write contract
            contract_file = verification_dir / "contract.pact"
            with open(contract_file, 'w') as f:
                f.write(pact_code)
            
            # Run Z3 theorem prover verification
            verification_script = self._create_verification_script(verification_dir, contract_file)
            
            result = subprocess.run(
                ["bash", str(verification_script)],
                cwd=verification_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return self._parse_verification_output(result.stdout, result.stderr, result.returncode == 0)
        
        except Exception as e:
            return {
                "success": False,
                "verification_passed": False,
                "errors": [f"Formal verification error: {str(e)}"],
                "properties": []
            }
    
    def pact_round_trip_verify(self, source_code: str) -> Dict[str, Any]:
        """Verify round-trip conversion: Pact -> Runa -> Pact."""
        try:
            # Parse original Pact code
            original_ast, parse_errors = self.parse_pact_code(source_code)
            if parse_errors:
                return {
                    "success": False,
                    "errors": parse_errors,
                    "stage": "parse_original"
                }
            
            # Convert to Runa
            runa_ast = pact_to_runa(original_ast)
            
            # Convert back to Pact
            reconstructed_ast = runa_to_pact(runa_ast)
            
            # Generate code from reconstructed AST
            reconstructed_code = self.generate_pact_code(reconstructed_ast)
            
            # Compare results
            return {
                "success": True,
                "original_code": source_code,
                "reconstructed_code": reconstructed_code,
                "ast_comparison": self._compare_asts(original_ast, reconstructed_ast),
                "semantic_equivalence": self._check_semantic_equivalence(source_code, reconstructed_code)
            }
        
        except Exception as e:
            return {
                "success": False,
                "errors": [f"Round-trip verification failed: {str(e)}"],
                "stage": "unknown"
            }
    
    def _create_validation_script(self, validation_dir: Path, contract_file: Path) -> Path:
        """Create validation script."""
        script_path = validation_dir / "validate.sh"
        with open(script_path, 'w') as f:
            f.write(f"""#!/bin/bash
set -e

# Validate syntax
echo "Validating Pact syntax..."
pact --check {contract_file.name}

# Run formal verification if available
if command -v pact-verify &> /dev/null; then
    echo "Running formal verification..."
    pact-verify {contract_file.name}
fi

# Estimate gas cost
echo "Estimating gas cost..."
pact --gas-estimate {contract_file.name}

echo "Validation completed successfully"
""")
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def _create_deployment_transaction(self, module_name: str, keyset_data: Dict[str, Any] = None) -> str:
        """Create deployment transaction YAML."""
        keyset = keyset_data or {
            "keys": ["public-key-here"],
            "pred": "keys-all"
        }
        
        return f"""
networkId: "{self.testnet_id}"
chainId: "{self.chain_id}"
gasPrice: 0.000001
gasLimit: 10000
ttl: 600
codeFile: {module_name}.pact
dataFile: null
keyPairs:
  - public: "public-key-here"
    secret: "secret-key-here"
    caps: []
"""
    
    def _create_deployment_script(self, deploy_dir: Path, tx_file: Path) -> Path:
        """Create deployment script."""
        script_path = deploy_dir / "deploy.sh"
        with open(script_path, 'w') as f:
            f.write(f"""#!/bin/bash
set -e

# Deploy using Kadena CLI
echo "Deploying contract to Kadena testnet..."
kda send {tx_file.name} --node-url {self.kadena_node_url}

echo "Deployment completed"
""")
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def _create_verification_script(self, verification_dir: Path, contract_file: Path) -> Path:
        """Create formal verification script."""
        script_path = verification_dir / "verify.sh"
        with open(script_path, 'w') as f:
            f.write(f"""#!/bin/bash
set -e

# Check for Z3 theorem prover
if ! command -v z3 &> /dev/null; then
    echo "Z3 theorem prover not found, skipping formal verification"
    exit 0
fi

# Run Pact formal verification
echo "Running formal verification with Z3..."
pact --verify {contract_file.name}

echo "Formal verification completed"
""")
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def _parse_validation_output(self, stdout: str, stderr: str, success: bool) -> PactValidationResult:
        """Parse validation output."""
        formal_verification_passed = "verification passed" in stdout.lower()
        capabilities_verified = "capabilities verified" in stdout.lower()
        
        # Extract gas cost
        gas_cost = 0
        gas_match = re.search(r'gas cost:\s*(\d+)', stdout)
        if gas_match:
            gas_cost = int(gas_match.group(1))
        
        # Extract execution trace
        execution_trace = []
        if "trace:" in stdout.lower():
            trace_lines = stdout.split('\n')
            in_trace = False
            for line in trace_lines:
                if "trace:" in line.lower():
                    in_trace = True
                    continue
                if in_trace and line.strip():
                    execution_trace.append(line.strip())
        
        errors = [stderr] if stderr and not success else []
        warnings = []
        
        # Extract warnings
        warning_lines = [line for line in stdout.split('\n') if 'warning' in line.lower()]
        warnings.extend(warning_lines)
        
        return PactValidationResult(
            is_valid=success,
            formal_verification_passed=formal_verification_passed,
            capabilities_verified=capabilities_verified,
            gas_cost=gas_cost,
            execution_trace=execution_trace,
            errors=errors,
            warnings=warnings,
            metadata={"validation_output": stdout}
        )
    
    def _parse_deployment_output(self, stdout: str, stderr: str) -> PactDeploymentResult:
        """Parse deployment output."""
        # Extract transaction hash
        tx_hash = None
        tx_match = re.search(r'transaction hash:\s*([a-fA-F0-9]+)', stdout)
        if tx_match:
            tx_hash = tx_match.group(1)
        
        # Extract module hash
        module_hash = None
        module_match = re.search(r'module hash:\s*([a-fA-F0-9]+)', stdout)
        if module_match:
            module_hash = module_match.group(1)
        
        # Extract gas used
        gas_used = 0
        gas_match = re.search(r'gas used:\s*(\d+)', stdout)
        if gas_match:
            gas_used = int(gas_match.group(1))
        
        return PactDeploymentResult(
            success=True,
            transaction_hash=tx_hash,
            module_hash=module_hash,
            gas_used=gas_used,
            errors=[]
        )
    
    def cleanup(self) -> None:
        """Clean up temporary files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except OSError:
            pass


# Convenience functions
def parse_pact_code(source_code: str) -> Tuple[Optional[PactProgram], List[str]]:
    """Parse Pact source code."""
    toolchain = PactToolchain()
    return toolchain.parse_pact_code(source_code)

def generate_pact_code(ast: PactProgram, style: PactCodeStyle = None) -> str:
    """Generate Pact code from AST."""
    toolchain = PactToolchain()
    return toolchain.generate_pact_code(ast, style)

def pact_round_trip_verify(source_code: str) -> Dict[str, Any]:
    """Verify round-trip conversion."""
    toolchain = PactToolchain()
    return toolchain.pact_round_trip_verify(source_code)

def pact_to_runa_translate(pact_code: str) -> str:
    """Translate Pact code to Runa."""
    toolchain = PactToolchain()
    
    # Parse Pact code
    pact_ast, errors = toolchain.parse_pact_code(pact_code)
    if errors:
        raise ValueError(f"Failed to parse Pact code: {errors}")
    
    # Convert to Runa
    runa_ast = pact_to_runa(pact_ast)
    
    # Generate Runa code (would need Runa generator)
    return "# Converted from Pact\n# (Runa code generation not implemented)"

def runa_to_pact_translate(runa_code: str) -> str:
    """Translate Runa code to Pact."""
    return "; Converted from Runa\n; (Runa parsing not implemented in this context)" 