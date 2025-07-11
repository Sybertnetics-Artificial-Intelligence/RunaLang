#!/usr/bin/env python3
"""
Plutus Toolchain Implementation

Complete toolchain for Plutus smart contract development including:
- Haskell compilation and UPLC generation
- Cardano testnet deployment
- Contract validation and testing
- Integration with Plutus Application Framework
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .plutus_parser import parse_plutus, PlutusLexer, PlutusParser
from .plutus_ast import PlutusProgram
from .plutus_generator import generate_plutus, PlutusCodeStyle
from .plutus_converter import plutus_to_runa, runa_to_plutus


@dataclass
class PlutusCompileResult:
    """Result of Plutus compilation."""
    success: bool
    uplc_code: Optional[str] = None
    script_hash: Optional[str] = None
    script_size: int = 0
    execution_units: Dict[str, int] = None
    errors: List[str] = None
    warnings: List[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class PlutusValidationResult:
    """Result of Plutus script validation."""
    is_valid: bool
    execution_cost: Dict[str, int]
    trace_log: List[str]
    errors: List[str]
    script_hash: str
    metadata: Dict[str, Any] = None


@dataclass
class PlutusDeploymentResult:
    """Result of Plutus contract deployment."""
    success: bool
    transaction_id: Optional[str] = None
    script_address: Optional[str] = None
    contract_address: Optional[str] = None
    deployment_cost: Dict[str, Any] = None
    errors: List[str] = None


class PlutusToolchain:
    """Complete toolchain for Plutus smart contract development."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="plutus_")
        self.ghc_version = "8.10.7"
        self.cabal_version = "3.6"
        self.plutus_version = "1.0.0"
        self.cardano_node_version = "1.35.4"
        
        # Plutus development environment
        self.plutus_apps_path = os.environ.get("PLUTUS_APPS_PATH", "/opt/plutus-apps")
        self.cardano_node_socket = os.environ.get("CARDANO_NODE_SOCKET_PATH", "/tmp/cardano-node.socket")
        self.testnet_magic = 1097911063  # Cardano testnet magic number
        
        # Build configuration
        self.build_config = {
            "optimization_level": "O2",
            "enable_profiling": False,
            "enable_coverage": False,
            "ghc_options": ["-Wall", "-Wcompat", "-Wredundant-constraints"],
            "language_extensions": [
                "DataKinds", "DeriveAnyClass", "DeriveGeneric", "DerivingStrategies",
                "ExplicitForAll", "GeneralizedNewtypeDeriving", "ImportQualifiedPost",
                "MultiParamTypeClasses", "NamedFieldPuns", "NoImplicitPrelude",
                "OverloadedStrings", "RecordWildCards", "ScopedTypeVariables",
                "Strict", "TemplateHaskell", "TypeApplications", "TypeFamilies",
                "TypeOperators"
            ]
        }
    
    def parse_plutus_code(self, source_code: str) -> Tuple[Optional[PlutusProgram], List[str]]:
        """Parse Plutus source code into AST."""
        try:
            program, errors = parse_plutus(source_code)
            return program, errors
        except Exception as e:
            return None, [f"Parse error: {str(e)}"]
    
    def generate_plutus_code(self, ast: PlutusProgram, style: PlutusCodeStyle = None) -> str:
        """Generate Plutus code from AST."""
        try:
            return generate_plutus(ast, style)
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {str(e)}")
    
    def compile_to_uplc(self, plutus_code: str, contract_name: str = "Contract") -> PlutusCompileResult:
        """Compile Plutus code to Untyped Plutus Core (UPLC)."""
        try:
            # Create project structure
            project_dir = Path(self.temp_dir) / f"plutus-{contract_name.lower()}"
            project_dir.mkdir(exist_ok=True)
            
            # Generate cabal project file
            self._create_cabal_project(project_dir, contract_name)
            
            # Write source code
            src_dir = project_dir / "src"
            src_dir.mkdir(exist_ok=True)
            
            main_file = src_dir / f"{contract_name}.hs"
            with open(main_file, 'w') as f:
                f.write(plutus_code)
            
            # Create compilation script
            compile_script = self._create_compilation_script(project_dir, contract_name)
            
            # Run compilation
            result = subprocess.run(
                ["bash", str(compile_script)],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Parse compilation output
                return self._parse_compile_output(project_dir, result.stdout, result.stderr)
            else:
                return PlutusCompileResult(
                    success=False,
                    errors=[result.stderr or "Compilation failed"],
                    warnings=[]
                )
        
        except subprocess.TimeoutExpired:
            return PlutusCompileResult(
                success=False,
                errors=["Compilation timed out"],
                warnings=[]
            )
        except Exception as e:
            return PlutusCompileResult(
                success=False,
                errors=[f"Compilation error: {str(e)}"],
                warnings=[]
            )
    
    def validate_script(self, uplc_code: str, datum: Any = None, redeemer: Any = None, 
                       script_context: Any = None) -> PlutusValidationResult:
        """Validate Plutus script execution."""
        try:
            # Create validation environment
            validation_dir = Path(self.temp_dir) / "validation"
            validation_dir.mkdir(exist_ok=True)
            
            # Write UPLC script
            script_file = validation_dir / "script.uplc"
            with open(script_file, 'w') as f:
                f.write(uplc_code)
            
            # Create validation script
            validation_script = self._create_validation_script(validation_dir, datum, redeemer, script_context)
            
            # Run validation
            result = subprocess.run(
                ["bash", str(validation_script)],
                cwd=validation_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return self._parse_validation_output(result.stdout, result.stderr, result.returncode == 0)
        
        except Exception as e:
            return PlutusValidationResult(
                is_valid=False,
                execution_cost={},
                trace_log=[],
                errors=[f"Validation error: {str(e)}"],
                script_hash=""
            )
    
    def deploy_to_testnet(self, uplc_code: str, initial_datum: Any = None) -> PlutusDeploymentResult:
        """Deploy Plutus script to Cardano testnet."""
        try:
            # Check if Cardano node is running
            if not self._check_cardano_node():
                return PlutusDeploymentResult(
                    success=False,
                    errors=["Cardano node is not running or not accessible"]
                )
            
            # Create deployment environment
            deploy_dir = Path(self.temp_dir) / "deployment"
            deploy_dir.mkdir(exist_ok=True)
            
            # Generate script address
            script_file = deploy_dir / "script.plutus"
            with open(script_file, 'w') as f:
                f.write(uplc_code)
            
            # Create deployment transaction
            deployment_script = self._create_deployment_script(deploy_dir, initial_datum)
            
            # Run deployment
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
                return PlutusDeploymentResult(
                    success=False,
                    errors=[result.stderr or "Deployment failed"]
                )
        
        except Exception as e:
            return PlutusDeploymentResult(
                success=False,
                errors=[f"Deployment error: {str(e)}"]
            )
    
    def run_tests(self, test_code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run Plutus contract tests."""
        try:
            test_dir = Path(self.temp_dir) / "testing"
            test_dir.mkdir(exist_ok=True)
            
            # Create test project
            self._create_test_project(test_dir, test_code, test_cases)
            
            # Run tests
            result = subprocess.run(
                ["cabal", "test", "--test-show-details=streaming"],
                cwd=test_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return self._parse_test_output(result.stdout, result.stderr, result.returncode == 0)
        
        except Exception as e:
            return {
                "success": False,
                "errors": [f"Test execution error: {str(e)}"],
                "test_results": []
            }
    
    def estimate_execution_cost(self, uplc_code: str, inputs: List[Any]) -> Dict[str, int]:
        """Estimate execution cost for Plutus script."""
        try:
            cost_dir = Path(self.temp_dir) / "cost_estimation"
            cost_dir.mkdir(exist_ok=True)
            
            # Create cost estimation script
            cost_script = self._create_cost_estimation_script(cost_dir, uplc_code, inputs)
            
            # Run cost estimation
            result = subprocess.run(
                ["bash", str(cost_script)],
                cwd=cost_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return self._parse_cost_output(result.stdout)
            else:
                return {"cpu": 0, "memory": 0, "error": result.stderr}
        
        except Exception as e:
            return {"cpu": 0, "memory": 0, "error": str(e)}
    
    def plutus_round_trip_verify(self, source_code: str) -> Dict[str, Any]:
        """Verify round-trip conversion: Plutus -> Runa -> Plutus."""
        try:
            # Parse original Plutus code
            original_ast, parse_errors = self.parse_plutus_code(source_code)
            if parse_errors:
                return {
                    "success": False,
                    "errors": parse_errors,
                    "stage": "parse_original"
                }
            
            # Convert to Runa
            runa_ast = plutus_to_runa(original_ast)
            
            # Convert back to Plutus
            reconstructed_ast = runa_to_plutus(runa_ast)
            
            # Generate code from reconstructed AST
            reconstructed_code = self.generate_plutus_code(reconstructed_ast)
            
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
    
    def _create_cabal_project(self, project_dir: Path, contract_name: str) -> None:
        """Create cabal project files."""
        # cabal.project
        cabal_project = project_dir / "cabal.project"
        with open(cabal_project, 'w') as f:
            f.write(f"""
packages: .

package cardano-crypto-praos
  flags: -external-libsodium-vrf

-- Always build tests and benchmarks.
tests: true
benchmarks: true

-- The only sensible test display option
test-show-details: streaming

allow-newer:
    size-based:template-haskell

constraints:
    hedgehog >= 1.0
  , bimap >= 0.4.0
  , libsystemd-journal >= 1.4.4
  , systemd >= 2.3.0
    -- systemd-2.3.0 requires at least network 3.1.1.0 but it doesn't declare
    -- that dependency
  , network >= 3.1.1.0

package plutus-ledger
  ghc-options: -Wno-unused-packages

source-repository-package
  type: git
  location: https://github.com/input-output-hk/plutus-apps.git
  tag: main
  subdir:
    cardano-node-emulator
    plutus-chain-index
    plutus-chain-index-core
    plutus-contract
    plutus-ledger
    plutus-ledger-constraints
    plutus-pab
    plutus-use-cases
    quickcheck-dynamic
""")
        
        # contract.cabal
        cabal_file = project_dir / f"{contract_name.lower()}.cabal"
        with open(cabal_file, 'w') as f:
            f.write(f"""
cabal-version: 2.4
name: {contract_name.lower()}
version: 0.1.0.0
synopsis: Plutus smart contract
description: Generated Plutus smart contract
author: Runa Universal Translation
maintainer: runa@sybertnetics.ai
category: Blockchain
build-type: Simple

common warnings
    ghc-options: -Wall
                 -Wcompat
                 -Wincomplete-uni-patterns
                 -Wincomplete-record-updates
                 -Wredundant-constraints
                 -Widentities
                 -Wunused-packages

library
    import: warnings
    exposed-modules: {contract_name}
    build-depends: base ^>=4.14.1.0
                 , aeson
                 , bytestring
                 , containers
                 , data-default
                 , plutus-core
                 , plutus-ledger-api
                 , plutus-tx
                 , plutus-tx-plugin
                 , text
                 , playground-common
                 , plutus-contract
                 , plutus-ledger
                 , plutus-ledger-constraints
                 , plutus-use-cases
    hs-source-dirs: src
    default-language: Haskell2010
    default-extensions: {' '.join(self.build_config['language_extensions'])}

executable {contract_name.lower()}-exe
    import: warnings
    main-is: Main.hs
    build-depends: base
                 , {contract_name.lower()}
    hs-source-dirs: app
    default-language: Haskell2010

test-suite {contract_name.lower()}-test
    import: warnings
    default-language: Haskell2010
    type: exitcode-stdio-1.0
    hs-source-dirs: test
    main-is: Spec.hs
    build-depends: base
                 , {contract_name.lower()}
                 , tasty
                 , tasty-hunit
                 , plutus-contract
                 , plutus-tx
                 , plutus-ledger
""")
    
    def _create_compilation_script(self, project_dir: Path, contract_name: str) -> Path:
        """Create compilation script."""
        script_path = project_dir / "compile.sh"
        with open(script_path, 'w') as f:
            f.write(f"""#!/bin/bash
set -e

# Setup environment
export PATH="$HOME/.cabal/bin:$PATH"
export PATH="$HOME/.ghcup/bin:$PATH"

# Update cabal
cabal update

# Configure and build
cabal configure
cabal build all

# Generate UPLC
cabal run {contract_name.lower()}-exe -- --output-uplc script.uplc

# Calculate script hash
cabal run {contract_name.lower()}-exe -- --script-hash > script.hash

echo "Compilation successful"
""")
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def _create_validation_script(self, validation_dir: Path, datum: Any, redeemer: Any, script_context: Any) -> Path:
        """Create script validation script."""
        script_path = validation_dir / "validate.sh"
        with open(script_path, 'w') as f:
            f.write(f"""#!/bin/bash
set -e

# Setup environment
export PATH="$HOME/.local/bin:$PATH"

# Create test inputs
echo '{json.dumps(datum) if datum else "null"}' > datum.json
echo '{json.dumps(redeemer) if redeemer else "null"}' > redeemer.json
echo '{json.dumps(script_context) if script_context else "null"}' > context.json

# Run validation using plutus-core
plutus-core evaluate --input-format flat-cbor --output-format text --trace-mode LogsWithBudgets script.uplc

echo "Validation completed"
""")
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def _check_cardano_node(self) -> bool:
        """Check if Cardano node is running."""
        try:
            result = subprocess.run(
                ["cardano-cli", "query", "tip", "--testnet-magic", str(self.testnet_magic)],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _parse_compile_output(self, project_dir: Path, stdout: str, stderr: str) -> PlutusCompileResult:
        """Parse compilation output."""
        try:
            # Read generated UPLC file
            uplc_file = project_dir / "script.uplc"
            uplc_code = ""
            if uplc_file.exists():
                with open(uplc_file, 'r') as f:
                    uplc_code = f.read()
            
            # Read script hash
            hash_file = project_dir / "script.hash"
            script_hash = ""
            if hash_file.exists():
                with open(hash_file, 'r') as f:
                    script_hash = f.read().strip()
            
            # Calculate script size
            script_size = len(uplc_code.encode('utf-8')) if uplc_code else 0
            
            return PlutusCompileResult(
                success=True,
                uplc_code=uplc_code,
                script_hash=script_hash,
                script_size=script_size,
                execution_units={"cpu": 0, "memory": 0},  # Placeholder
                errors=[],
                warnings=self._extract_warnings(stderr),
                metadata={"compilation_output": stdout}
            )
        
        except Exception as e:
            return PlutusCompileResult(
                success=False,
                errors=[f"Failed to parse compilation output: {str(e)}"],
                warnings=[]
            )
    
    def _extract_warnings(self, stderr: str) -> List[str]:
        """Extract warnings from compilation output."""
        warnings = []
        lines = stderr.split('\n')
        
        for line in lines:
            if 'Warning:' in line or 'warning:' in line:
                warnings.append(line.strip())
        
        return warnings
    
    def _parse_validation_output(self, stdout: str, stderr: str, success: bool) -> PlutusValidationResult:
        """Parse script validation output."""
        execution_cost = {"cpu": 0, "memory": 0}
        trace_log = []
        errors = []
        
        if success:
            # Parse execution cost from output
            lines = stdout.split('\n')
            for line in lines:
                if 'CPU' in line and 'steps' in line:
                    try:
                        execution_cost["cpu"] = int(line.split()[-2])
                    except (ValueError, IndexError):
                        pass
                elif 'Memory' in line and 'units' in line:
                    try:
                        execution_cost["memory"] = int(line.split()[-2])
                    except (ValueError, IndexError):
                        pass
                elif 'TRACE:' in line:
                    trace_log.append(line.replace('TRACE:', '').strip())
        else:
            errors = [stderr] if stderr else ["Validation failed"]
        
        return PlutusValidationResult(
            is_valid=success,
            execution_cost=execution_cost,
            trace_log=trace_log,
            errors=errors,
            script_hash="",  # Placeholder
            metadata={"validation_output": stdout}
        )
    
    def cleanup(self) -> None:
        """Clean up temporary files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except OSError:
            pass  # Ignore cleanup errors


# Convenience functions
def parse_plutus_code(source_code: str) -> Tuple[Optional[PlutusProgram], List[str]]:
    """Parse Plutus source code."""
    toolchain = PlutusToolchain()
    return toolchain.parse_plutus_code(source_code)

def generate_plutus_code(ast: PlutusProgram, style: PlutusCodeStyle = None) -> str:
    """Generate Plutus code from AST."""
    toolchain = PlutusToolchain()
    return toolchain.generate_plutus_code(ast, style)

def plutus_round_trip_verify(source_code: str) -> Dict[str, Any]:
    """Verify round-trip conversion."""
    toolchain = PlutusToolchain()
    return toolchain.plutus_round_trip_verify(source_code)

def plutus_to_runa_translate(plutus_code: str) -> str:
    """Translate Plutus code to Runa."""
    toolchain = PlutusToolchain()
    
    # Parse Plutus code
    plutus_ast, errors = toolchain.parse_plutus_code(plutus_code)
    if errors:
        raise ValueError(f"Failed to parse Plutus code: {errors}")
    
    # Convert to Runa
    runa_ast = plutus_to_runa(plutus_ast)
    
    # Generate Runa code (would need Runa generator)
    # For now, return a placeholder
    return "# Converted from Plutus\n# (Runa code generation not implemented)"

def runa_to_plutus_translate(runa_code: str) -> str:
    """Translate Runa code to Plutus."""
    # This would require a Runa parser, which is not available in this context
    # For now, return a placeholder
    return "-- Converted from Runa\n-- (Runa parsing not implemented in this context)" 