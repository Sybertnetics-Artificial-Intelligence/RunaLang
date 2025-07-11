#!/usr/bin/env python3
"""
Elixir Toolchain Module

This module provides a complete toolchain for the Elixir programming language,
including:
- Mix build tool integration
- Elixir compiler (elixirc) integration
- REPL (IEx) support
- OTP application management
- Testing with ExUnit
- Dependency management with Hex
- Phoenix framework support
- GenServer and supervisor patterns
"""

import os
import subprocess
import tempfile
import json
from typing import Dict, List, Optional, Tuple, Any, Union
from pathlib import Path
from dataclasses import dataclass, field

from ...core.base_components import BaseToolchain, ToolchainConfig, CompilationResult
from .elixir_ast import ElixirProgram, ElixirNode
from .elixir_parser import parse_elixir
from .elixir_converter import elixir_to_runa, runa_to_elixir
from .elixir_generator import generate_elixir_code, ElixirCodeStyle

@dataclass
class ElixirCompileOptions:
    """Configuration options for Elixir compilation."""
    output_dir: Optional[str] = None
    warnings_as_errors: bool = False
    debug_info: bool = True
    optimize: bool = False
    verbose: bool = False
    no_warn_undefined: bool = False
    docs: bool = True
    compile_deps: bool = True
    env: str = "dev"  # dev, test, prod

@dataclass
class MixProjectConfig:
    """Configuration for Mix project structure."""
    app_name: str = "my_app"
    version: str = "0.1.0"
    elixir_version: str = "~> 1.14"
    deps: List[Dict[str, Any]] = field(default_factory=list)
    aliases: Dict[str, str] = field(default_factory=dict)
    start_permanent: bool = False
    umbrella: bool = False

@dataclass 
class ElixirToolchainConfig(ToolchainConfig):
    """Configuration for Elixir toolchain."""
    elixir_path: str = "elixir"
    elixirc_path: str = "elixirc"
    mix_path: str = "mix"
    iex_path: str = "iex"
    compile_options: ElixirCompileOptions = field(default_factory=ElixirCompileOptions)
    mix_config: MixProjectConfig = field(default_factory=MixProjectConfig)
    code_style: ElixirCodeStyle = field(default_factory=ElixirCodeStyle)
    
    # Phoenix support
    phoenix_enabled: bool = False
    phoenix_version: str = "~> 1.7.0"
    
    # LiveView support
    liveview_enabled: bool = False
    liveview_version: str = "~> 0.19.0"
    
    # Database support
    ecto_enabled: bool = False
    ecto_version: str = "~> 3.10"
    database_adapter: str = "postgres"  # postgres, mysql, sqlite

class ElixirToolchain(BaseToolchain):
    """Complete Elixir language toolchain."""
    
    def __init__(self, config: Optional[ElixirToolchainConfig] = None):
        super().__init__()
        self.config = config or ElixirToolchainConfig()
        self.language = "elixir"
        self.version = self._get_elixir_version()
        
        # Verify tools are available
        self._verify_installation()
    
    def _get_elixir_version(self) -> str:
        """Get the installed Elixir version."""
        try:
            result = subprocess.run(
                [self.config.elixir_path, "--version"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # Parse version from output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('Elixir'):
                        return line.split()[1]
            return "unknown"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return "unknown"
    
    def _verify_installation(self):
        """Verify that required Elixir tools are installed."""
        tools = [
            (self.config.elixir_path, "Elixir"),
            (self.config.elixirc_path, "Elixir Compiler"),
            (self.config.mix_path, "Mix Build Tool"),
            (self.config.iex_path, "IEx REPL")
        ]
        
        missing_tools = []
        for tool_path, tool_name in tools:
            try:
                result = subprocess.run(
                    [tool_path, "--version"],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode != 0:
                    missing_tools.append(tool_name)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_tools.append(tool_name)
        
        if missing_tools:
            raise RuntimeError(f"Missing Elixir tools: {', '.join(missing_tools)}")
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ElixirProgram:
        """Parse Elixir source code."""
        try:
            return parse_elixir(source_code)
        except Exception as e:
            raise SyntaxError(f"Failed to parse Elixir code: {e}")
    
    def convert_to_runa(self, elixir_ast: ElixirNode):
        """Convert Elixir AST to Runa Universal AST."""
        return elixir_to_runa(elixir_ast)
    
    def convert_from_runa(self, runa_ast):
        """Convert Runa Universal AST to Elixir AST."""
        return runa_to_elixir(runa_ast)
    
    def generate_code(self, elixir_ast: ElixirNode) -> str:
        """Generate Elixir code from AST."""
        return generate_elixir_code(elixir_ast, self.config.code_style)
    
    def validate_syntax(self, source_code: str) -> Tuple[bool, Optional[str]]:
        """Validate Elixir syntax without execution."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ex', delete=False) as f:
            f.write(source_code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                [self.config.elixirc_path, "--no-compile", temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr
        
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return False, str(e)
        finally:
            os.unlink(temp_file)
    
    def compile_file(self, source_file: str, output_dir: Optional[str] = None) -> CompilationResult:
        """Compile a single Elixir file."""
        if not os.path.exists(source_file):
            return CompilationResult(
                success=False,
                exit_code=1,
                output="",
                error=f"Source file not found: {source_file}",
                output_files=[]
            )
        
        compile_output_dir = output_dir or self.config.compile_options.output_dir or os.path.dirname(source_file)
        
        # Build compilation command
        cmd = [self.config.elixirc_path]
        
        if compile_output_dir:
            cmd.extend(["-o", compile_output_dir])
        
        if self.config.compile_options.warnings_as_errors:
            cmd.append("--warnings-as-errors")
        
        if not self.config.compile_options.debug_info:
            cmd.append("--no-debug-info")
        
        if self.config.compile_options.verbose:
            cmd.append("--verbose")
        
        if self.config.compile_options.no_warn_undefined:
            cmd.append("--no-warn-undefined")
        
        cmd.append(source_file)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Find output files (BEAM files)
            output_files = []
            if result.returncode == 0 and compile_output_dir:
                for file in os.listdir(compile_output_dir):
                    if file.endswith('.beam'):
                        output_files.append(os.path.join(compile_output_dir, file))
            
            return CompilationResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                output=result.stdout,
                error=result.stderr,
                output_files=output_files
            )
        
        except subprocess.TimeoutExpired:
            return CompilationResult(
                success=False,
                exit_code=124,
                output="",
                error="Compilation timed out",
                output_files=[]
            )
        except Exception as e:
            return CompilationResult(
                success=False,
                exit_code=1,
                output="",
                error=str(e),
                output_files=[]
            )
    
    def compile_project(self, project_dir: str) -> CompilationResult:
        """Compile an entire Mix project."""
        if not os.path.exists(os.path.join(project_dir, "mix.exs")):
            return CompilationResult(
                success=False,
                exit_code=1,
                output="",
                error="No mix.exs file found in project directory",
                output_files=[]
            )
        
        # Set environment
        env = os.environ.copy()
        env["MIX_ENV"] = self.config.compile_options.env
        
        # Build compilation command
        cmd = [self.config.mix_path, "compile"]
        
        if self.config.compile_options.warnings_as_errors:
            cmd.append("--warnings-as-errors")
        
        if self.config.compile_options.verbose:
            cmd.append("--verbose")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=project_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=300
            )
            
            # Find output files
            output_files = []
            build_dir = os.path.join(project_dir, "_build", self.config.compile_options.env, "lib")
            if os.path.exists(build_dir):
                for root, dirs, files in os.walk(build_dir):
                    for file in files:
                        if file.endswith('.beam'):
                            output_files.append(os.path.join(root, file))
            
            return CompilationResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                output=result.stdout,
                error=result.stderr,
                output_files=output_files
            )
        
        except subprocess.TimeoutExpired:
            return CompilationResult(
                success=False,
                exit_code=124,
                output="",
                error="Project compilation timed out",
                output_files=[]
            )
        except Exception as e:
            return CompilationResult(
                success=False,
                exit_code=1,
                output="",
                error=str(e),
                output_files=[]
            )
    
    def run_script(self, script_content: str, args: Optional[List[str]] = None) -> Tuple[int, str, str]:
        """Run Elixir script content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.exs', delete=False) as f:
            f.write(script_content)
            temp_file = f.name
        
        try:
            cmd = [self.config.elixir_path, temp_file]
            if args:
                cmd.extend(args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.returncode, result.stdout, result.stderr
        
        except subprocess.TimeoutExpired:
            return 124, "", "Script execution timed out"
        except Exception as e:
            return 1, "", str(e)
        finally:
            os.unlink(temp_file)
    
    def start_repl(self) -> subprocess.Popen:
        """Start an interactive Elixir REPL (IEx)."""
        return subprocess.Popen(
            [self.config.iex_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def create_mix_project(self, project_name: str, project_dir: str, 
                          template: str = "default") -> bool:
        """Create a new Mix project."""
        try:
            # Determine project template
            cmd = [self.config.mix_path, "new", project_name]
            
            if template == "phoenix":
                cmd = [self.config.mix_path, "phx.new", project_name]
            elif template == "umbrella":
                cmd.extend(["--umbrella"])
            elif template == "library":
                cmd.extend(["--module", project_name.title()])
            
            # Add optional flags
            if template != "phoenix":
                cmd.extend(["--app", project_name.lower()])
            
            result = subprocess.run(
                cmd,
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                # Update project configuration if needed
                self._update_mix_project(os.path.join(project_dir, project_name))
                return True
            else:
                print(f"Failed to create project: {result.stderr}")
                return False
        
        except Exception as e:
            print(f"Error creating project: {e}")
            return False
    
    def _update_mix_project(self, project_path: str):
        """Update mix.exs with configured dependencies and settings."""
        mix_file = os.path.join(project_path, "mix.exs")
        if not os.path.exists(mix_file):
            return
        
        # Add Phoenix dependency if enabled
        if self.config.phoenix_enabled:
            self.config.mix_config.deps.append({
                "phoenix": self.config.phoenix_version
            })
        
        # Add LiveView dependency if enabled
        if self.config.liveview_enabled:
            self.config.mix_config.deps.append({
                "phoenix_live_view": self.config.liveview_version
            })
        
        # Add Ecto dependency if enabled
        if self.config.ecto_enabled:
            self.config.mix_config.deps.append({
                "ecto_sql": self.config.ecto_version
            })
            
            if self.config.database_adapter == "postgres":
                self.config.mix_config.deps.append({"postgrex": ">= 0.0.0"})
            elif self.config.database_adapter == "mysql":
                self.config.mix_config.deps.append({"myxql": ">= 0.0.0"})
            elif self.config.database_adapter == "sqlite":
                self.config.mix_config.deps.append({"ecto_sqlite3": ">= 0.0.0"})
    
    def run_tests(self, project_dir: str, test_pattern: Optional[str] = None) -> Tuple[int, str, str]:
        """Run ExUnit tests for a project."""
        if not os.path.exists(os.path.join(project_dir, "mix.exs")):
            return 1, "", "No mix.exs file found in project directory"
        
        # Set test environment
        env = os.environ.copy()
        env["MIX_ENV"] = "test"
        
        cmd = [self.config.mix_path, "test"]
        
        if test_pattern:
            cmd.append(test_pattern)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=project_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=300
            )
            
            return result.returncode, result.stdout, result.stderr
        
        except subprocess.TimeoutExpired:
            return 124, "", "Test execution timed out"
        except Exception as e:
            return 1, "", str(e)
    
    def get_dependencies(self, project_dir: str) -> List[Dict[str, Any]]:
        """Get project dependencies from mix.exs."""
        try:
            result = subprocess.run(
                [self.config.mix_path, "deps"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse dependencies from output
                deps = []
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('*'):
                        # Parse dependency line
                        parts = line.split()
                        if len(parts) >= 3:
                            deps.append({
                                "name": parts[1],
                                "version": parts[2],
                                "status": "available" if "*" in parts[0] else "missing"
                            })
                return deps
            else:
                return []
        
        except Exception:
            return []
    
    def format_code(self, source_code: str) -> str:
        """Format Elixir code using mix format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ex', delete=False) as f:
            f.write(source_code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                [self.config.mix_path, "format", temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                with open(temp_file, 'r') as f:
                    return f.read()
            else:
                return source_code  # Return original if formatting fails
        
        except Exception:
            return source_code
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def analyze_code(self, source_code: str) -> Dict[str, Any]:
        """Analyze Elixir code for potential issues."""
        # Use Credo for static analysis if available
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ex', delete=False) as f:
            f.write(source_code)
            temp_file = f.name
        
        try:
            # Try to run credo
            result = subprocess.run(
                [self.config.mix_path, "credo", "--format", "json", temp_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                # Fallback to basic syntax validation
                is_valid, error = self.validate_syntax(source_code)
                return {
                    "issues": [] if is_valid else [{"message": error, "severity": "error"}],
                    "summary": {"total": 0 if is_valid else 1}
                }
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            # Fallback to syntax validation
            is_valid, error = self.validate_syntax(source_code)
            return {
                "issues": [] if is_valid else [{"message": error, "severity": "error"}],
                "summary": {"total": 0 if is_valid else 1}
            }
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def get_project_info(self, project_dir: str) -> Dict[str, Any]:
        """Get information about a Mix project."""
        try:
            result = subprocess.run(
                [self.config.mix_path, "compile", "--verbose"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Get dependency tree
            deps_result = subprocess.run(
                [self.config.mix_path, "deps.tree"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "compilation_info": result.stdout if result.returncode == 0 else result.stderr,
                "dependency_tree": deps_result.stdout if deps_result.returncode == 0 else "",
                "elixir_version": self.version,
                "mix_env": os.environ.get("MIX_ENV", "dev")
            }
        
        except Exception as e:
            return {"error": str(e)}

# Convenience functions

def create_elixir_toolchain(config: Optional[Dict[str, Any]] = None) -> ElixirToolchain:
    """Create an Elixir toolchain with optional configuration."""
    if config:
        toolchain_config = ElixirToolchainConfig(**config)
        return ElixirToolchain(toolchain_config)
    else:
        return ElixirToolchain()

def compile_elixir_file(file_path: str, output_path: Optional[str] = None) -> CompilationResult:
    """Compile a single Elixir file."""
    toolchain = ElixirToolchain()
    return toolchain.compile_file(file_path, output_path)

def run_elixir_script(script_content: str, args: Optional[List[str]] = None) -> Tuple[int, str, str]:
    """Run Elixir script content."""
    toolchain = ElixirToolchain()
    return toolchain.run_script(script_content, args) 