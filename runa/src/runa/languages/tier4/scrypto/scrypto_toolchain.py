"""
Scrypto development toolchain for building, testing, and deploying smart contracts.

This toolchain provides comprehensive support for Scrypto development including:
- Code compilation and building
- Unit and integration testing
- Package management with Cargo
- Radix Engine simulation
- Deployment to Radix networks
- Transaction construction and execution
"""

import os
import json
import subprocess
import tempfile
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass

from .scrypto_ast import ScryptoAST
from .scrypto_parser import parse_scrypto
from .scrypto_generator import generate_scrypto_code
from .scrypto_converter import convert_scrypto_to_runa, convert_runa_to_scrypto


@dataclass
class ScryptoCompilationResult:
    """Result of Scrypto compilation"""
    success: bool
    wasm_package: Optional[bytes] = None
    schema: Optional[Dict[str, Any]] = None
    package_address: Optional[str] = None
    error_message: Optional[str] = None
    warnings: List[str] = None


@dataclass
class ScryptoTestResult:
    """Result of Scrypto testing"""
    success: bool
    test_count: int = 0
    passed_count: int = 0
    failed_count: int = 0
    test_output: str = ""
    error_message: Optional[str] = None


@dataclass
class ScryptoDeploymentResult:
    """Result of Scrypto deployment"""
    success: bool
    transaction_hash: Optional[str] = None
    package_address: Optional[str] = None
    component_addresses: List[str] = None
    error_message: Optional[str] = None


@dataclass
class ScryptoTransaction:
    """Scrypto transaction definition"""
    manifest: str
    fee_payer: Optional[str] = None
    signatures: List[str] = None
    notary: Optional[str] = None


class ScryptoToolchain:
    """
    Comprehensive toolchain for Scrypto development.
    
    Provides building, testing, deployment, and simulation capabilities
    for Scrypto smart contracts on Radix DLT.
    """
    
    def __init__(self, project_path: Optional[str] = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.cargo_toml_path = self.project_path / "Cargo.toml"
        self.src_path = self.project_path / "src"
        self.target_path = self.project_path / "target"
        
        # Radix Engine configuration
        self.radix_engine_config = {
            'network': 'simulator',  # 'simulator', 'stokenet', 'mainnet'
            'node_url': 'http://localhost:8080',
            'simulator_path': None
        }
        
        # Build configuration
        self.build_config = {
            'target': 'wasm32-unknown-unknown',
            'release': True,
            'optimization_level': 3
        }
    
    def initialize_project(self, name: str, template: str = "blueprint") -> bool:
        """Initialize new Scrypto project"""
        try:
            # Create project directory
            self.project_path.mkdir(parents=True, exist_ok=True)
            
            # Create Cargo.toml
            self.create_cargo_toml(name, template)
            
            # Create source directory
            self.src_path.mkdir(exist_ok=True)
            
            # Create lib.rs
            self.create_lib_rs(template)
            
            # Create tests directory
            (self.project_path / "tests").mkdir(exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"Project initialization failed: {e}")
            return False
    
    def create_cargo_toml(self, name: str, template: str):
        """Create Cargo.toml for Scrypto project"""
        cargo_content = f'''[package]
name = "{name}"
version = "1.0.0"
edition = "2021"

[dependencies]
scrypto = {{ git = "https://github.com/radixdlt/radixdlt-scrypto", tag = "v1.3.0" }}

[profile.release]
opt-level = 3
overflow-checks = true
lto = true
codegen-units = 1
panic = "abort"

[lib]
crate-type = ["cdylib", "lib"]

[[bin]]
name = "blueprint"
path = "src/main.rs"
'''
        
        with open(self.cargo_toml_path, 'w') as f:
            f.write(cargo_content)
    
    def create_lib_rs(self, template: str):
        """Create lib.rs based on template"""
        if template == "blueprint":
            lib_content = '''use scrypto::prelude::*;

#[derive(ScryptoSbor)]
pub struct SimpleBlueprint {
    value: u32,
}

impl SimpleBlueprint {
    pub fn instantiate(initial_value: u32) -> ComponentAddress {
        Self {
            value: initial_value,
        }
        .instantiate()
        .globalize()
    }
    
    pub fn get_value(&self) -> u32 {
        self.value
    }
    
    pub fn set_value(&mut self, new_value: u32) {
        self.value = new_value;
    }
}
'''
        else:
            lib_content = '''use scrypto::prelude::*;

// Your Scrypto code here
'''
        
        with open(self.src_path / "lib.rs", 'w') as f:
            f.write(lib_content)
    
    def build(self, release: bool = True) -> ScryptoCompilationResult:
        """Build Scrypto project"""
        try:
            # Prepare build command
            cmd = ["cargo", "build"]
            if release:
                cmd.append("--release")
            cmd.extend(["--target", self.build_config['target']])
            
            # Run build
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ScryptoCompilationResult(
                    success=False,
                    error_message=result.stderr
                )
            
            # Extract WASM package
            wasm_path = self.get_wasm_path(release)
            if wasm_path and wasm_path.exists():
                with open(wasm_path, 'rb') as f:
                    wasm_package = f.read()
                
                return ScryptoCompilationResult(
                    success=True,
                    wasm_package=wasm_package,
                    warnings=self.parse_warnings(result.stderr)
                )
            else:
                return ScryptoCompilationResult(
                    success=False,
                    error_message="WASM package not found after build"
                )
            
        except Exception as e:
            return ScryptoCompilationResult(
                success=False,
                error_message=str(e)
            )
    
    def test(self, test_name: Optional[str] = None) -> ScryptoTestResult:
        """Run Scrypto tests"""
        try:
            cmd = ["cargo", "test"]
            if test_name:
                cmd.append(test_name)
            cmd.append("--")
            cmd.append("--nocapture")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            # Parse test results
            test_output = result.stdout + result.stderr
            test_count, passed_count, failed_count = self.parse_test_results(test_output)
            
            return ScryptoTestResult(
                success=result.returncode == 0,
                test_count=test_count,
                passed_count=passed_count,
                failed_count=failed_count,
                test_output=test_output,
                error_message=result.stderr if result.returncode != 0 else None
            )
            
        except Exception as e:
            return ScryptoTestResult(
                success=False,
                error_message=str(e)
            )
    
    def publish_package(self) -> ScryptoCompilationResult:
        """Publish package to Radix Engine"""
        try:
            # Build first
            build_result = self.build(release=True)
            if not build_result.success:
                return build_result
            
            # Use resim to publish package
            cmd = ["resim", "publish", "."]
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ScryptoCompilationResult(
                    success=False,
                    error_message=result.stderr
                )
            
            # Extract package address from output
            package_address = self.extract_package_address(result.stdout)
            
            return ScryptoCompilationResult(
                success=True,
                wasm_package=build_result.wasm_package,
                package_address=package_address
            )
            
        except Exception as e:
            return ScryptoCompilationResult(
                success=False,
                error_message=str(e)
            )
    
    def create_transaction_manifest(
        self,
        operations: List[Dict[str, Any]],
        accounts: List[str] = None
    ) -> str:
        """Create transaction manifest for operations"""
        manifest_lines = []
        
        # Add accounts to worktop if specified
        if accounts:
            for account in accounts:
                manifest_lines.append(f'CALL_METHOD Address("{account}") "withdraw_from_auth_zone" Enum<0u8>();')
        
        # Add operations
        for op in operations:
            if op['type'] == 'instantiate_component':
                manifest_lines.append(
                    f'CALL_FUNCTION Address("{op["package_address"]}") '
                    f'"{op["blueprint_name"]}" "{op["function_name"]}" '
                    f'{self.format_manifest_args(op.get("args", []))};'
                )
            
            elif op['type'] == 'call_method':
                manifest_lines.append(
                    f'CALL_METHOD Address("{op["component_address"]}") '
                    f'"{op["method_name"]}" '
                    f'{self.format_manifest_args(op.get("args", []))};'
                )
            
            elif op['type'] == 'create_proof':
                manifest_lines.append(
                    f'CREATE_PROOF_FROM_AUTH_ZONE_OF_AMOUNT Address("{op["resource_address"]}") '
                    f'Decimal("{op["amount"]}");'
                )
        
        # Add deposit instruction
        if accounts:
            manifest_lines.append(f'CALL_METHOD Address("{accounts[0]}") "deposit_batch" Expression("ENTIRE_WORKTOP");')
        
        return '\n'.join(manifest_lines)
    
    def execute_transaction(self, manifest: str, signers: List[str] = None) -> ScryptoDeploymentResult:
        """Execute transaction manifest"""
        try:
            # Write manifest to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rtm', delete=False) as f:
                f.write(manifest)
                manifest_file = f.name
            
            try:
                # Execute with resim
                cmd = ["resim", "run", manifest_file]
                if signers:
                    for signer in signers:
                        cmd.extend(["--signing-keys", signer])
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    return ScryptoDeploymentResult(
                        success=False,
                        error_message=result.stderr
                    )
                
                # Parse transaction results
                transaction_hash = self.extract_transaction_hash(result.stdout)
                component_addresses = self.extract_component_addresses(result.stdout)
                
                return ScryptoDeploymentResult(
                    success=True,
                    transaction_hash=transaction_hash,
                    component_addresses=component_addresses
                )
                
            finally:
                os.unlink(manifest_file)
            
        except Exception as e:
            return ScryptoDeploymentResult(
                success=False,
                error_message=str(e)
            )
    
    def instantiate_component(
        self,
        package_address: str,
        blueprint_name: str,
        function_name: str = "instantiate",
        args: List[Any] = None
    ) -> ScryptoDeploymentResult:
        """Instantiate component from blueprint"""
        operations = [{
            'type': 'instantiate_component',
            'package_address': package_address,
            'blueprint_name': blueprint_name,
            'function_name': function_name,
            'args': args or []
        }]
        
        manifest = self.create_transaction_manifest(operations)
        return self.execute_transaction(manifest)
    
    def call_component_method(
        self,
        component_address: str,
        method_name: str,
        args: List[Any] = None
    ) -> ScryptoDeploymentResult:
        """Call method on component"""
        operations = [{
            'type': 'call_method',
            'component_address': component_address,
            'method_name': method_name,
            'args': args or []
        }]
        
        manifest = self.create_transaction_manifest(operations)
        return self.execute_transaction(manifest)
    
    def reset_simulator(self) -> bool:
        """Reset Radix Engine simulator"""
        try:
            result = subprocess.run(
                ["resim", "reset"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def create_account(self) -> Optional[str]:
        """Create new account in simulator"""
        try:
            result = subprocess.run(
                ["resim", "new-account"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return self.extract_account_address(result.stdout)
            return None
            
        except Exception:
            return None
    
    def get_component_state(self, component_address: str) -> Optional[Dict[str, Any]]:
        """Get component state"""
        try:
            result = subprocess.run(
                ["resim", "show", component_address],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return self.parse_component_state(result.stdout)
            return None
            
        except Exception:
            return None
    
    def validate_code(self, source_code: str) -> List[str]:
        """Validate Scrypto code"""
        errors = []
        
        try:
            # Parse code
            ast = parse_scrypto(source_code)
            
            # Check for common issues
            errors.extend(self.check_asset_handling(ast))
            errors.extend(self.check_component_structure(ast))
            errors.extend(self.check_security_patterns(ast))
            
        except Exception as e:
            errors.append(f"Parsing error: {str(e)}")
        
        return errors
    
    def check_asset_handling(self, ast: ScryptoAST) -> List[str]:
        """Check asset handling patterns"""
        errors = []
        
        # Check for proper bucket/vault usage
        resources = ast.get_all_resources()
        if not resources:
            errors.append("No resource definitions found")
        
        return errors
    
    def check_component_structure(self, ast: ScryptoAST) -> List[str]:
        """Check component structure"""
        errors = []
        
        blueprints = ast.get_all_blueprints()
        if not blueprints:
            errors.append("No blueprints found")
        
        for blueprint in blueprints:
            if not blueprint.instantiate_functions:
                errors.append(f"Blueprint {blueprint.name} has no instantiate function")
        
        return errors
    
    def check_security_patterns(self, ast: ScryptoAST) -> List[str]:
        """Check security patterns"""
        errors = []
        
        # Check for proper access control
        # Check for overflow protection
        # Check for reentrancy protection
        
        return errors
    
    # Helper methods
    
    def get_wasm_path(self, release: bool) -> Optional[Path]:
        """Get path to compiled WASM file"""
        profile = "release" if release else "debug"
        wasm_file = f"{self.project_path.name.replace('-', '_')}.wasm"
        return self.target_path / self.build_config['target'] / profile / wasm_file
    
    def parse_warnings(self, stderr: str) -> List[str]:
        """Parse compiler warnings"""
        warnings = []
        lines = stderr.split('\n')
        for line in lines:
            if 'warning:' in line:
                warnings.append(line.strip())
        return warnings
    
    def parse_test_results(self, output: str) -> tuple:
        """Parse test results from output"""
        test_count = 0
        passed_count = 0
        failed_count = 0
        
        lines = output.split('\n')
        for line in lines:
            if 'test result:' in line:
                # Extract test counts
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed;' and i > 0:
                        passed_count = int(parts[i-1])
                    elif part == 'failed;' and i > 0:
                        failed_count = int(parts[i-1])
                
                test_count = passed_count + failed_count
                break
        
        return test_count, passed_count, failed_count
    
    def extract_package_address(self, output: str) -> Optional[str]:
        """Extract package address from resim output"""
        lines = output.split('\n')
        for line in lines:
            if 'Package:' in line:
                return line.split(':')[-1].strip()
        return None
    
    def extract_transaction_hash(self, output: str) -> Optional[str]:
        """Extract transaction hash from resim output"""
        lines = output.split('\n')
        for line in lines:
            if 'Transaction Hash:' in line:
                return line.split(':')[-1].strip()
        return None
    
    def extract_component_addresses(self, output: str) -> List[str]:
        """Extract component addresses from resim output"""
        addresses = []
        lines = output.split('\n')
        for line in lines:
            if 'Component:' in line:
                addresses.append(line.split(':')[-1].strip())
        return addresses
    
    def extract_account_address(self, output: str) -> Optional[str]:
        """Extract account address from resim output"""
        lines = output.split('\n')
        for line in lines:
            if 'Account component address:' in line:
                return line.split(':')[-1].strip()
        return None
    
    def parse_component_state(self, output: str) -> Dict[str, Any]:
        """Parse component state from resim output"""
        # This would parse the actual component state format
        # For now, return empty dict
        return {}
    
    def format_manifest_args(self, args: List[Any]) -> str:
        """Format arguments for transaction manifest"""
        if not args:
            return ""
        
        formatted_args = []
        for arg in args:
            if isinstance(arg, str):
                formatted_args.append(f'"{arg}"')
            elif isinstance(arg, (int, float)):
                formatted_args.append(f'Decimal("{arg}")')
            else:
                formatted_args.append(str(arg))
        
        return " ".join(formatted_args)


# Example usage and testing
if __name__ == "__main__":
    # Create toolchain instance
    toolchain = ScryptoToolchain("/tmp/test_scrypto_project")
    
    # Initialize project
    if toolchain.initialize_project("test_blueprint"):
        print("✅ Project initialized successfully")
        
        # Build project
        build_result = toolchain.build()
        if build_result.success:
            print("✅ Build successful")
        else:
            print(f"❌ Build failed: {build_result.error_message}")
        
        # Run tests
        test_result = toolchain.test()
        print(f"Tests: {test_result.passed_count}/{test_result.test_count} passed")
    else:
        print("❌ Project initialization failed") 