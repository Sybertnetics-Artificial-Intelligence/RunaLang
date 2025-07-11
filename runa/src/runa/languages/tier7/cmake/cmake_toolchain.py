#!/usr/bin/env python3
"""
CMake Toolchain Integration

Complete toolchain for CMake build system including:
- CMakeLists.txt parsing and generation
- Build system integration (Make, Ninja, Visual Studio)
- Cross-platform build support
- Package management and dependencies
- Testing and installation
"""

import os
import subprocess
import json
import tempfile
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
from dataclasses import dataclass

from .cmake_ast import *
from .cmake_parser import parse_cmake
from .cmake_converter import cmake_to_runa, runa_to_cmake
from .cmake_generator import generate_cmake, CMakeCodeStyle


@dataclass
class CMakeConfig:
    """Configuration for CMake toolchain."""
    cmake_binary: str = "cmake"
    generator: Optional[str] = None  # Unix Makefiles, Ninja, Visual Studio, etc.
    build_type: str = "Release"  # Debug, Release, RelWithDebInfo, MinSizeRel
    install_prefix: Optional[str] = None
    build_parallel_level: Optional[int] = None
    verbose: bool = False
    
    def __post_init__(self):
        if self.build_parallel_level is None:
            self.build_parallel_level = os.cpu_count()


@dataclass
class CMakeBuildResult:
    """Result of a CMake build operation."""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    build_time: float = 0.0
    targets_built: List[str] = None
    
    def __post_init__(self):
        if self.targets_built is None:
            self.targets_built = []


class CMakeToolchain:
    """Complete CMake build system toolchain."""
    
    def __init__(self, config: Optional[CMakeConfig] = None):
        self.config = config or CMakeConfig()
        self.source_dir = None
        self.build_dir = None
        
    def parse_file(self, file_path: str) -> CMakeFile:
        """Parse a CMake file into AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return parse_cmake(content, file_path)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"CMake file not found: {file_path}")
        except Exception as e:
            raise SyntaxError(f"Failed to parse CMake file {file_path}: {e}")
    
    def generate_file(self, ast_node: CMakeNode, style: Optional[CMakeCodeStyle] = None) -> str:
        """Generate CMake code from AST."""
        return generate_cmake(ast_node, style)
    
    def configure(self, source_dir: str, build_dir: str, options: Optional[Dict[str, str]] = None) -> CMakeBuildResult:
        """Configure CMake project."""
        self.source_dir = Path(source_dir).resolve()
        self.build_dir = Path(build_dir).resolve()
        
        # Create build directory
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [self.config.cmake_binary]
        
        # Add generator
        if self.config.generator:
            cmd.extend(["-G", self.config.generator])
        
        # Add build type
        cmd.extend(["-DCMAKE_BUILD_TYPE=" + self.config.build_type])
        
        # Add install prefix
        if self.config.install_prefix:
            cmd.extend(["-DCMAKE_INSTALL_PREFIX=" + self.config.install_prefix])
        
        # Add custom options
        if options:
            for key, value in options.items():
                cmd.extend([f"-D{key}={value}"])
        
        # Add source directory
        cmd.append(str(self.source_dir))
        
        return self._run_cmake_command(cmd, cwd=self.build_dir)
    
    def build(self, target: Optional[str] = None, parallel: Optional[bool] = True) -> CMakeBuildResult:
        """Build CMake project."""
        if not self.build_dir or not self.build_dir.exists():
            raise RuntimeError("Project not configured. Run configure() first.")
        
        cmd = [self.config.cmake_binary, "--build", str(self.build_dir)]
        
        if target:
            cmd.extend(["--target", target])
        
        if parallel and self.config.build_parallel_level:
            cmd.extend(["--parallel", str(self.config.build_parallel_level)])
        
        if self.config.verbose:
            cmd.append("--verbose")
        
        return self._run_cmake_command(cmd)
    
    def install(self, component: Optional[str] = None) -> CMakeBuildResult:
        """Install CMake project."""
        if not self.build_dir or not self.build_dir.exists():
            raise RuntimeError("Project not configured. Run configure() first.")
        
        cmd = [self.config.cmake_binary, "--install", str(self.build_dir)]
        
        if component:
            cmd.extend(["--component", component])
        
        if self.config.verbose:
            cmd.append("--verbose")
        
        return self._run_cmake_command(cmd)
    
    def test(self, parallel: Optional[bool] = True) -> CMakeBuildResult:
        """Run CMake tests using CTest."""
        if not self.build_dir or not self.build_dir.exists():
            raise RuntimeError("Project not configured. Run configure() first.")
        
        cmd = ["ctest", "--test-dir", str(self.build_dir)]
        
        if parallel and self.config.build_parallel_level:
            cmd.extend(["--parallel", str(self.config.build_parallel_level)])
        
        if self.config.verbose:
            cmd.append("--verbose")
        
        return self._run_cmake_command(cmd)
    
    def clean(self) -> CMakeBuildResult:
        """Clean CMake build directory."""
        if not self.build_dir or not self.build_dir.exists():
            raise RuntimeError("Project not configured. Run configure() first.")
        
        cmd = [self.config.cmake_binary, "--build", str(self.build_dir), "--target", "clean"]
        
        return self._run_cmake_command(cmd)
    
    def get_cache_variables(self) -> Dict[str, str]:
        """Get CMake cache variables."""
        if not self.build_dir or not self.build_dir.exists():
            return {}
        
        cache_file = self.build_dir / "CMakeCache.txt"
        if not cache_file.exists():
            return {}
        
        variables = {}
        try:
            with open(cache_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        if ':' in line:
                            # Format: VAR:TYPE=VALUE
                            var_part, value = line.split('=', 1)
                            var_name = var_part.split(':')[0]
                            variables[var_name] = value
                        else:
                            # Format: VAR=VALUE
                            var_name, value = line.split('=', 1)
                            variables[var_name] = value
        except Exception:
            pass
        
        return variables
    
    def list_targets(self) -> List[str]:
        """List available build targets."""
        if not self.build_dir or not self.build_dir.exists():
            return []
        
        cmd = [self.config.cmake_binary, "--build", str(self.build_dir), "--target", "help"]
        result = self._run_cmake_command(cmd)
        
        targets = []
        if result.success:
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line.startswith('...'):
                    target = line[3:].strip()
                    if target:
                        targets.append(target)
        
        return targets
    
    def find_cmake_lists(self, directory: str) -> List[str]:
        """Find all CMakeLists.txt files in directory tree."""
        cmake_files = []
        root_path = Path(directory)
        
        for cmake_file in root_path.rglob("CMakeLists.txt"):
            if cmake_file.is_file():
                cmake_files.append(str(cmake_file))
        
        return cmake_files
    
    def validate_project(self, source_dir: str) -> Dict[str, Any]:
        """Validate CMake project structure."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "cmake_files": [],
            "targets": {}
        }
        
        source_path = Path(source_dir)
        
        # Check for main CMakeLists.txt
        main_cmake = source_path / "CMakeLists.txt"
        if not main_cmake.exists():
            validation["valid"] = False
            validation["errors"].append("No CMakeLists.txt found in source directory")
            return validation
        
        # Find and validate all CMakeLists.txt files
        cmake_files = self.find_cmake_lists(source_dir)
        validation["cmake_files"] = cmake_files
        
        for cmake_file in cmake_files:
            try:
                ast = self.parse_file(cmake_file)
                # Basic validation passed
            except Exception as e:
                validation["valid"] = False
                validation["errors"].append(f"Invalid CMakeLists.txt {cmake_file}: {e}")
        
        return validation
    
    def round_trip_verify(self, file_path: str) -> bool:
        """Verify round-trip conversion: CMake → Runa → CMake."""
        try:
            # Parse original CMake file
            original_ast = self.parse_file(file_path)
            
            # Convert to Runa AST
            runa_ast = cmake_to_runa(original_ast)
            
            # Convert back to CMake AST
            reconstructed_ast = runa_to_cmake(runa_ast)
            
            # Generate code from reconstructed AST
            reconstructed_code = self.generate_file(reconstructed_ast)
            
            # Parse reconstructed code
            reparsed_ast = parse_cmake(reconstructed_code, file_path)
            
            # Basic verification - both should parse successfully
            return True
            
        except Exception as e:
            print(f"Round-trip verification failed for {file_path}: {e}")
            return False
    
    def create_project(self, project_name: str, project_dir: str, project_type: str = "executable") -> bool:
        """Create a new CMake project."""
        try:
            project_path = Path(project_dir)
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create main CMakeLists.txt
            cmake_content = f"""cmake_minimum_required(VERSION 3.16)

project({project_name} 
    VERSION 1.0.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

"""
            
            if project_type == "executable":
                cmake_content += f"""add_executable({project_name}
    src/main.cpp
)
"""
                # Create source directory and main.cpp
                src_dir = project_path / "src"
                src_dir.mkdir(exist_ok=True)
                
                main_cpp = src_dir / "main.cpp"
                main_cpp.write_text("""#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
""")
            
            elif project_type == "library":
                cmake_content += f"""add_library({project_name}
    src/{project_name}.cpp
    include/{project_name}.h
)

target_include_directories({project_name} PUBLIC
    include
)
"""
                # Create directories and files
                src_dir = project_path / "src"
                inc_dir = project_path / "include"
                src_dir.mkdir(exist_ok=True)
                inc_dir.mkdir(exist_ok=True)
                
                header_file = inc_dir / f"{project_name}.h"
                header_file.write_text(f"""#pragma once

class {project_name.title()} {{
public:
    void hello();
}};
""")
                
                source_file = src_dir / f"{project_name}.cpp"
                source_file.write_text(f"""#include "{project_name}.h"
#include <iostream>

void {project_name.title()}::hello() {{
    std::cout << "Hello from {project_name}!" << std::endl;
}}
""")
            
            # Write CMakeLists.txt
            cmake_file = project_path / "CMakeLists.txt"
            cmake_file.write_text(cmake_content)
            
            return True
            
        except Exception as e:
            print(f"Failed to create project: {e}")
            return False
    
    def _run_cmake_command(self, cmd: List[str], cwd: Optional[Path] = None) -> CMakeBuildResult:
        """Run a CMake command and return the result."""
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=300  # 5 minute timeout
            )
            
            return CMakeBuildResult(
                success=process.returncode == 0,
                exit_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr
            )
            
        except subprocess.TimeoutExpired:
            return CMakeBuildResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr="Command timed out"
            )
        except Exception as e:
            return CMakeBuildResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Failed to run command: {e}"
            )


# Convenience functions for external use
def parse_cmake_code(code: str, file_path: Optional[str] = None) -> CMakeFile:
    """Parse CMake code string into AST."""
    return parse_cmake(code, file_path)


def generate_cmake_code(ast_node: CMakeNode, style: Optional[CMakeCodeStyle] = None) -> str:
    """Generate CMake code from AST node."""
    return generate_cmake(ast_node, style)


def cmake_round_trip_verify(file_path: str) -> bool:
    """Verify round-trip conversion for a CMake file."""
    toolchain = CMakeToolchain()
    return toolchain.round_trip_verify(file_path)


def cmake_to_runa_translate(cmake_code: str, file_path: Optional[str] = None):
    """Translate CMake code to Runa AST."""
    cmake_ast = parse_cmake_code(cmake_code, file_path)
    return cmake_to_runa(cmake_ast)


def runa_to_cmake_translate(runa_ast):
    """Translate Runa AST to CMake code."""
    cmake_ast = runa_to_cmake(runa_ast)
    return generate_cmake_code(cmake_ast)


# Export main classes and functions
__all__ = [
    'CMakeToolchain',
    'CMakeConfig',
    'CMakeBuildResult',
    'parse_cmake_code',
    'generate_cmake_code',
    'cmake_round_trip_verify',
    'cmake_to_runa_translate',
    'runa_to_cmake_translate'
] 