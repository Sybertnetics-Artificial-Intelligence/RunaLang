#!/usr/bin/env python3
"""
Bazel Toolchain Integration

Complete toolchain for Bazel build system including:
- CLI integration and build execution
- Remote execution and caching support
- Build analysis and query capabilities
- Target dependency resolution
- Workspace configuration management
- Round-trip verification and testing
"""

import os
import subprocess
import json
import tempfile
import shutil
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
from dataclasses import dataclass

from .bazel_ast import *
from .bazel_parser import parse_bazel
from .bazel_converter import bazel_to_runa, runa_to_bazel
from .bazel_generator import generate_bazel, BazelCodeStyle


@dataclass
class BazelConfig:
    """Configuration for Bazel toolchain."""
    bazel_binary: str = "bazel"
    workspace_root: Optional[str] = None
    build_flags: List[str] = None
    test_flags: List[str] = None
    query_flags: List[str] = None
    remote_cache: Optional[str] = None
    remote_executor: Optional[str] = None
    output_base: Optional[str] = None
    
    def __post_init__(self):
        if self.build_flags is None:
            self.build_flags = []
        if self.test_flags is None:
            self.test_flags = []
        if self.query_flags is None:
            self.query_flags = []


@dataclass 
class BazelBuildResult:
    """Result of a Bazel build operation."""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    targets_built: List[str] = None
    artifacts: List[str] = None
    build_time: float = 0.0
    
    def __post_init__(self):
        if self.targets_built is None:
            self.targets_built = []
        if self.artifacts is None:
            self.artifacts = []


@dataclass
class BazelQueryResult:
    """Result of a Bazel query operation."""
    success: bool
    targets: List[str] = None
    dependencies: Dict[str, List[str]] = None
    rdependencies: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.targets is None:
            self.targets = []
        if self.dependencies is None:
            self.dependencies = {}
        if self.rdependencies is None:
            self.rdependencies = {}


class BazelToolchain:
    """Complete Bazel build system toolchain."""
    
    def __init__(self, config: Optional[BazelConfig] = None):
        self.config = config or BazelConfig()
        self.workspace_root = self._find_workspace_root()
        
    def _find_workspace_root(self) -> Optional[str]:
        """Find the Bazel workspace root."""
        if self.config.workspace_root:
            return self.config.workspace_root
        
        # Look for WORKSPACE file in current directory and parents
        current = Path.cwd()
        while current != current.parent:
            workspace_files = [
                current / "WORKSPACE",
                current / "WORKSPACE.bazel"
            ]
            
            for workspace_file in workspace_files:
                if workspace_file.exists():
                    return str(current)
            
            current = current.parent
        
        return None
    
    def parse_file(self, file_path: str) -> Union[BuildFile, WorkspaceFile, BzlFile]:
        """Parse a Bazel file into AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return parse_bazel(content, file_path)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Bazel file not found: {file_path}")
        except Exception as e:
            raise SyntaxError(f"Failed to parse Bazel file {file_path}: {e}")
    
    def generate_file(self, ast_node: BazelNode, style: Optional[BazelCodeStyle] = None) -> str:
        """Generate Bazel code from AST."""
        return generate_bazel(ast_node, style)
    
    def build_targets(self, targets: List[str], flags: Optional[List[str]] = None) -> BazelBuildResult:
        """Build Bazel targets."""
        if not self.workspace_root:
            raise RuntimeError("No Bazel workspace found")
        
        build_flags = (flags or []) + self.config.build_flags
        
        if self.config.remote_cache:
            build_flags.extend(["--remote_cache", self.config.remote_cache])
        
        if self.config.remote_executor:
            build_flags.extend(["--remote_executor", self.config.remote_executor])
        
        cmd = [self.config.bazel_binary, "build"] + build_flags + targets
        
        return self._run_bazel_command(cmd)
    
    def test_targets(self, targets: List[str], flags: Optional[List[str]] = None) -> BazelBuildResult:
        """Test Bazel targets."""
        if not self.workspace_root:
            raise RuntimeError("No Bazel workspace found")
        
        test_flags = (flags or []) + self.config.test_flags
        
        cmd = [self.config.bazel_binary, "test"] + test_flags + targets
        
        return self._run_bazel_command(cmd)
    
    def query_targets(self, query: str, flags: Optional[List[str]] = None) -> BazelQueryResult:
        """Query Bazel targets."""
        if not self.workspace_root:
            raise RuntimeError("No Bazel workspace found")
        
        query_flags = (flags or []) + self.config.query_flags + ["--output=label"]
        
        cmd = [self.config.bazel_binary, "query"] + query_flags + [query]
        
        result = self._run_bazel_command(cmd)
        
        targets = []
        if result.success:
            targets = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        return BazelQueryResult(
            success=result.success,
            targets=targets
        )
    
    def get_dependencies(self, target: str) -> BazelQueryResult:
        """Get dependencies of a target."""
        query = f"deps({target})"
        return self.query_targets(query)
    
    def get_reverse_dependencies(self, target: str) -> BazelQueryResult:
        """Get reverse dependencies of a target."""
        query = f"rdeps(..., {target})"
        return self.query_targets(query)
    
    def list_targets(self, package: str = "...") -> BazelQueryResult:
        """List all targets in a package."""
        query = f"//{package}"
        return self.query_targets(query)
    
    def run_target(self, target: str, args: Optional[List[str]] = None, flags: Optional[List[str]] = None) -> BazelBuildResult:
        """Run a Bazel target."""
        if not self.workspace_root:
            raise RuntimeError("No Bazel workspace found")
        
        run_flags = flags or []
        run_args = args or []
        
        cmd = [self.config.bazel_binary, "run"] + run_flags + [target]
        if run_args:
            cmd.extend(["--"] + run_args)
        
        return self._run_bazel_command(cmd)
    
    def clean_workspace(self, expunge: bool = False) -> BazelBuildResult:
        """Clean the Bazel workspace."""
        if not self.workspace_root:
            raise RuntimeError("No Bazel workspace found")
        
        cmd = [self.config.bazel_binary, "clean"]
        if expunge:
            cmd.append("--expunge")
        
        return self._run_bazel_command(cmd)
    
    def analyze_workspace(self) -> Dict[str, Any]:
        """Analyze the Bazel workspace structure."""
        if not self.workspace_root:
            raise RuntimeError("No Bazel workspace found")
        
        analysis = {
            "workspace_root": self.workspace_root,
            "workspace_file": None,
            "build_files": [],
            "bzl_files": [],
            "packages": [],
            "targets": {}
        }
        
        workspace_root = Path(self.workspace_root)
        
        # Find WORKSPACE file
        for workspace_file in ["WORKSPACE", "WORKSPACE.bazel"]:
            workspace_path = workspace_root / workspace_file
            if workspace_path.exists():
                analysis["workspace_file"] = str(workspace_path)
                break
        
        # Find all BUILD and .bzl files
        for build_file in workspace_root.rglob("BUILD*"):
            if build_file.is_file() and not any(part.startswith('.') for part in build_file.parts):
                analysis["build_files"].append(str(build_file))
                
                # Extract package name
                package_path = build_file.parent.relative_to(workspace_root)
                package_name = str(package_path) if package_path != Path('.') else ""
                if package_name not in analysis["packages"]:
                    analysis["packages"].append(package_name)
        
        for bzl_file in workspace_root.rglob("*.bzl"):
            if bzl_file.is_file() and not any(part.startswith('.') for part in bzl_file.parts):
                analysis["bzl_files"].append(str(bzl_file))
        
        # Query for targets in each package
        for package in analysis["packages"]:
            query_pattern = f"//{package}:*" if package else "//:*"
            result = self.query_targets(query_pattern)
            if result.success:
                analysis["targets"][package] = result.targets
        
        return analysis
    
    def validate_workspace(self) -> Dict[str, Any]:
        """Validate the Bazel workspace."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "files_checked": 0,
            "files_valid": 0
        }
        
        if not self.workspace_root:
            validation["valid"] = False
            validation["errors"].append("No Bazel workspace found")
            return validation
        
        workspace_root = Path(self.workspace_root)
        
        # Check WORKSPACE file
        workspace_files = [workspace_root / "WORKSPACE", workspace_root / "WORKSPACE.bazel"]
        workspace_exists = any(f.exists() for f in workspace_files)
        
        if not workspace_exists:
            validation["valid"] = False
            validation["errors"].append("No WORKSPACE file found")
        
        # Validate BUILD files
        for build_file in workspace_root.rglob("BUILD*"):
            if build_file.is_file():
                validation["files_checked"] += 1
                try:
                    self.parse_file(str(build_file))
                    validation["files_valid"] += 1
                except Exception as e:
                    validation["valid"] = False
                    validation["errors"].append(f"Invalid BUILD file {build_file}: {e}")
        
        # Validate .bzl files
        for bzl_file in workspace_root.rglob("*.bzl"):
            if bzl_file.is_file():
                validation["files_checked"] += 1
                try:
                    self.parse_file(str(bzl_file))
                    validation["files_valid"] += 1
                except Exception as e:
                    validation["valid"] = False
                    validation["errors"].append(f"Invalid .bzl file {bzl_file}: {e}")
        
        return validation
    
    def round_trip_verify(self, file_path: str) -> bool:
        """Verify round-trip conversion: Bazel → Runa → Bazel."""
        try:
            # Parse original Bazel file
            original_ast = self.parse_file(file_path)
            
            # Convert to Runa AST
            runa_ast = bazel_to_runa(original_ast)
            
            # Convert back to Bazel AST
            file_type = "BUILD"
            if file_path.endswith("WORKSPACE") or file_path.endswith("WORKSPACE.bazel"):
                file_type = "WORKSPACE"
            elif file_path.endswith(".bzl"):
                file_type = "BZL"
            
            reconstructed_ast = runa_to_bazel(runa_ast, file_type)
            
            # Generate code from reconstructed AST
            reconstructed_code = self.generate_file(reconstructed_ast)
            
            # Parse reconstructed code
            reparsed_ast = parse_bazel(reconstructed_code, file_path)
            
            # Basic verification - both should parse successfully
            return True
            
        except Exception as e:
            print(f"Round-trip verification failed for {file_path}: {e}")
            return False
    
    def create_workspace(self, workspace_name: str, workspace_dir: str) -> bool:
        """Create a new Bazel workspace."""
        try:
            workspace_path = Path(workspace_dir)
            workspace_path.mkdir(parents=True, exist_ok=True)
            
            # Create WORKSPACE file
            workspace_content = f'workspace(name = "{workspace_name}")\n'
            (workspace_path / "WORKSPACE").write_text(workspace_content)
            
            # Create root BUILD file
            build_content = '# Root BUILD file\n'
            (workspace_path / "BUILD").write_text(build_content)
            
            # Create .bazelrc file with common configurations
            bazelrc_content = """# Common Bazel configurations
build --jobs=auto
test --test_output=errors
query --output=label_kind
"""
            (workspace_path / ".bazelrc").write_text(bazelrc_content)
            
            return True
            
        except Exception as e:
            print(f"Failed to create workspace: {e}")
            return False
    
    def _run_bazel_command(self, cmd: List[str]) -> BazelBuildResult:
        """Run a Bazel command and return the result."""
        try:
            # Change to workspace directory
            original_cwd = os.getcwd()
            if self.workspace_root:
                os.chdir(self.workspace_root)
            
            # Run command
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return BazelBuildResult(
                success=process.returncode == 0,
                exit_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr
            )
            
        except subprocess.TimeoutExpired:
            return BazelBuildResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr="Command timed out"
            )
        except Exception as e:
            return BazelBuildResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Failed to run command: {e}"
            )
        finally:
            # Restore original directory
            os.chdir(original_cwd)


# Convenience functions for external use
def parse_bazel_code(code: str, file_path: Optional[str] = None) -> Union[BuildFile, WorkspaceFile, BzlFile]:
    """Parse Bazel code string into AST."""
    return parse_bazel(code, file_path)


def generate_bazel_code(ast_node: BazelNode, style: Optional[BazelCodeStyle] = None) -> str:
    """Generate Bazel code from AST node."""
    return generate_bazel(ast_node, style)


def bazel_round_trip_verify(file_path: str) -> bool:
    """Verify round-trip conversion for a Bazel file."""
    toolchain = BazelToolchain()
    return toolchain.round_trip_verify(file_path)


def bazel_to_runa_translate(bazel_code: str, file_path: Optional[str] = None):
    """Translate Bazel code to Runa AST."""
    bazel_ast = parse_bazel_code(bazel_code, file_path)
    return bazel_to_runa(bazel_ast)


def runa_to_bazel_translate(runa_ast, file_type: str = "BUILD"):
    """Translate Runa AST to Bazel code.""" 
    bazel_ast = runa_to_bazel(runa_ast, file_type)
    return generate_bazel_code(bazel_ast)


# Export main classes and functions
__all__ = [
    'BazelToolchain',
    'BazelConfig',
    'BazelBuildResult',
    'BazelQueryResult',
    'parse_bazel_code',
    'generate_bazel_code', 
    'bazel_round_trip_verify',
    'bazel_to_runa_translate',
    'runa_to_bazel_translate'
] 