"""LLVM IR Toolchain - Build system integration and development tools for LLVM IR."""

import os
import subprocess
import shutil
import tempfile
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from runa.core.toolchain import BaseToolchain, BuildResult, ToolchainError


@dataclass
class LLVMIRToolchainConfig:
    """Configuration for LLVM IR toolchain."""
    llvm_version: str = "15"
    target_triple: str = "x86_64-unknown-linux-gnu"
    optimization_level: str = "O0"  # O0, O1, O2, O3, Os, Oz
    output_format: str = "executable"  # executable, object, bitcode, assembly
    debug_info: bool = True
    use_lto: bool = False
    use_pgo: bool = False
    sanitizers: List[str] = None
    output_dir: str = "build"
    verbose: bool = False


class LLVMIRToolchain(BaseToolchain):
    """LLVM IR language toolchain implementation."""
    
    def __init__(self, config: Optional[LLVMIRToolchainConfig] = None):
        super().__init__()
        self.config = config or LLVMIRToolchainConfig()
        self.available_tools: Dict[str, str] = {}
        self._detect_llvm_tools()
    
    def _detect_llvm_tools(self) -> None:
        """Detect available LLVM tools."""
        tools_to_detect = [
            "llvm-as", "llvm-dis", "llvm-link", "llvm-opt", "llc",
            "lli", "llvm-objdump", "llvm-nm", "llvm-readobj",
            "clang", "clang++", "lld", "opt"
        ]
        
        for tool in tools_to_detect:
            # Try with version suffix first
            versioned_tool = f"{tool}-{self.config.llvm_version}"
            path = shutil.which(versioned_tool)
            if path:
                self.available_tools[tool] = path
            else:
                # Try without version
                path = shutil.which(tool)
                if path:
                    self.available_tools[tool] = path
    
    def get_available_tools(self) -> Dict[str, str]:
        """Get available LLVM tools."""
        return self.available_tools.copy()
    
    def validate_config(self) -> List[str]:
        """Validate toolchain configuration."""
        issues = []
        
        # Check required tools
        required_tools = ["llvm-as", "llc"]
        for tool in required_tools:
            if tool not in self.available_tools:
                issues.append(f"Required tool '{tool}' not found")
        
        # Validate optimization level
        valid_opts = ["O0", "O1", "O2", "O3", "Os", "Oz"]
        if self.config.optimization_level not in valid_opts:
            issues.append(f"Invalid optimization level: {self.config.optimization_level}")
        
        # Validate output format
        valid_formats = ["executable", "object", "bitcode", "assembly"]
        if self.config.output_format not in valid_formats:
            issues.append(f"Invalid output format: {self.config.output_format}")
        
        return issues
    
    def build(self, source_files: List[str], output_path: Optional[str] = None) -> BuildResult:
        """Build LLVM IR source files."""
        try:
            # Validate configuration
            config_issues = self.validate_config()
            if config_issues:
                return BuildResult(
                    success=False,
                    errors=config_issues,
                    warnings=[],
                    output_files=[],
                    metadata={"toolchain": "llvm_ir"}
                )
            
            # Prepare build directory
            build_dir = Path(self.config.output_dir)
            build_dir.mkdir(exist_ok=True)
            
            all_errors = []
            all_warnings = []
            intermediate_files = []
            
            # Process each source file
            for source_file in source_files:
                # Convert LLVM IR to bitcode
                bc_file = self._assemble_ir(source_file, build_dir)
                if bc_file:
                    intermediate_files.append(bc_file)
                else:
                    all_errors.append(f"Failed to assemble {source_file}")
            
            if not intermediate_files:
                return BuildResult(
                    success=False,
                    errors=all_errors,
                    warnings=all_warnings,
                    output_files=[],
                    metadata={"toolchain": "llvm_ir"}
                )
            
            # Link bitcode files if multiple
            if len(intermediate_files) > 1:
                linked_bc = self._link_bitcode(intermediate_files, build_dir)
                if linked_bc:
                    final_bc = linked_bc
                else:
                    all_errors.append("Failed to link bitcode files")
                    return BuildResult(
                        success=False,
                        errors=all_errors,
                        warnings=all_warnings,
                        output_files=intermediate_files,
                        metadata={"toolchain": "llvm_ir"}
                    )
            else:
                final_bc = intermediate_files[0]
            
            # Optimize if requested
            if self.config.optimization_level != "O0":
                optimized_bc = self._optimize_bitcode(final_bc, build_dir)
                if optimized_bc:
                    final_bc = optimized_bc
            
            # Generate final output
            output_file = output_path or str(build_dir / "program")
            
            if self.config.output_format == "bitcode":
                final_output = final_bc
            elif self.config.output_format == "assembly":
                final_output = self._generate_assembly(final_bc, build_dir)
            elif self.config.output_format == "object":
                final_output = self._generate_object(final_bc, build_dir)
            else:  # executable
                final_output = self._generate_executable(final_bc, output_file)
            
            if final_output:
                return BuildResult(
                    success=True,
                    errors=all_errors,
                    warnings=all_warnings,
                    output_files=[final_output],
                    metadata={
                        "toolchain": "llvm_ir",
                        "optimization": self.config.optimization_level,
                        "target_triple": self.config.target_triple,
                        "output_format": self.config.output_format
                    }
                )
            else:
                all_errors.append("Failed to generate final output")
                return BuildResult(
                    success=False,
                    errors=all_errors,
                    warnings=all_warnings,
                    output_files=[final_bc] if final_bc else [],
                    metadata={"toolchain": "llvm_ir"}
                )
        
        except Exception as e:
            return BuildResult(
                success=False,
                errors=[f"Build error: {str(e)}"],
                warnings=[],
                output_files=[],
                metadata={"toolchain": "llvm_ir"}
            )
    
    def _assemble_ir(self, source_file: str, build_dir: Path) -> Optional[str]:
        """Assemble LLVM IR to bitcode."""
        if "llvm-as" not in self.available_tools:
            return None
        
        try:
            source_path = Path(source_file)
            bc_file = build_dir / f"{source_path.stem}.bc"
            
            cmd = [
                self.available_tools["llvm-as"],
                "-o", str(bc_file),
                source_file
            ]
            
            if self.config.verbose:
                print(f"Assembling: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return str(bc_file)
            else:
                print(f"Assembly failed: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error assembling {source_file}: {str(e)}")
            return None
    
    def _link_bitcode(self, bc_files: List[str], build_dir: Path) -> Optional[str]:
        """Link multiple bitcode files."""
        if "llvm-link" not in self.available_tools:
            return None
        
        try:
            linked_bc = build_dir / "linked.bc"
            
            cmd = [
                self.available_tools["llvm-link"],
                "-o", str(linked_bc)
            ] + bc_files
            
            if self.config.verbose:
                print(f"Linking: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return str(linked_bc)
            else:
                print(f"Linking failed: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error linking bitcode: {str(e)}")
            return None
    
    def _optimize_bitcode(self, bc_file: str, build_dir: Path) -> Optional[str]:
        """Optimize bitcode using opt."""
        if "opt" not in self.available_tools:
            return bc_file  # Return unoptimized if opt not available
        
        try:
            optimized_bc = build_dir / "optimized.bc"
            
            cmd = [
                self.available_tools["opt"],
                f"-{self.config.optimization_level}",
                "-o", str(optimized_bc),
                bc_file
            ]
            
            if self.config.verbose:
                print(f"Optimizing: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return str(optimized_bc)
            else:
                print(f"Optimization failed: {result.stderr}")
                return bc_file  # Return unoptimized
        
        except Exception as e:
            print(f"Error optimizing {bc_file}: {str(e)}")
            return bc_file
    
    def _generate_assembly(self, bc_file: str, build_dir: Path) -> Optional[str]:
        """Generate assembly from bitcode."""
        if "llc" not in self.available_tools:
            return None
        
        try:
            asm_file = build_dir / "program.s"
            
            cmd = [
                self.available_tools["llc"],
                "-o", str(asm_file),
                bc_file
            ]
            
            if self.config.verbose:
                print(f"Generating assembly: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return str(asm_file)
            else:
                print(f"Assembly generation failed: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error generating assembly: {str(e)}")
            return None
    
    def _generate_object(self, bc_file: str, build_dir: Path) -> Optional[str]:
        """Generate object file from bitcode."""
        if "llc" not in self.available_tools:
            return None
        
        try:
            obj_file = build_dir / "program.o"
            
            cmd = [
                self.available_tools["llc"],
                "-filetype=obj",
                "-o", str(obj_file),
                bc_file
            ]
            
            if self.config.verbose:
                print(f"Generating object: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return str(obj_file)
            else:
                print(f"Object generation failed: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error generating object: {str(e)}")
            return None
    
    def _generate_executable(self, bc_file: str, output_file: str) -> Optional[str]:
        """Generate executable from bitcode."""
        # Try clang first, then llc + system linker
        if "clang" in self.available_tools:
            return self._generate_executable_clang(bc_file, output_file)
        else:
            return self._generate_executable_llc(bc_file, output_file)
    
    def _generate_executable_clang(self, bc_file: str, output_file: str) -> Optional[str]:
        """Generate executable using clang."""
        try:
            cmd = [
                self.available_tools["clang"],
                "-o", output_file,
                bc_file
            ]
            
            if self.config.debug_info:
                cmd.append("-g")
            
            if self.config.verbose:
                print(f"Generating executable: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return output_file
            else:
                print(f"Executable generation failed: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error generating executable: {str(e)}")
            return None
    
    def _generate_executable_llc(self, bc_file: str, output_file: str) -> Optional[str]:
        """Generate executable using llc + system linker."""
        # Generate object file first
        build_dir = Path(bc_file).parent
        obj_file = self._generate_object(bc_file, build_dir)
        
        if not obj_file:
            return None
        
        # Link with system linker
        try:
            cmd = ["gcc", "-o", output_file, obj_file]
            
            if self.config.debug_info:
                cmd.append("-g")
            
            if self.config.verbose:
                print(f"Linking executable: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return output_file
            else:
                print(f"Linking failed: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error linking executable: {str(e)}")
            return None
    
    def run(self, executable_path: str, args: List[str] = None) -> subprocess.CompletedProcess:
        """Run compiled executable or interpret bitcode."""
        if executable_path.endswith('.bc') and "lli" in self.available_tools:
            # Interpret bitcode with lli
            cmd = [self.available_tools["lli"], executable_path]
            if args:
                cmd.extend(args)
        else:
            # Run native executable
            cmd = [executable_path]
            if args:
                cmd.extend(args)
        
        return subprocess.run(cmd, capture_output=True, text=True)
    
    def disassemble(self, bc_file: str, output_file: Optional[str] = None) -> bool:
        """Disassemble bitcode to LLVM IR."""
        if "llvm-dis" not in self.available_tools:
            return False
        
        try:
            cmd = [self.available_tools["llvm-dis"]]
            
            if output_file:
                cmd.extend(["-o", output_file])
            
            cmd.append(bc_file)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if not output_file:
                    print(result.stdout)
                return True
            else:
                print(f"Disassembly failed: {result.stderr}")
                return False
        
        except Exception as e:
            print(f"Error disassembling: {str(e)}")
            return False
    
    def analyze_bitcode(self, bc_file: str) -> Dict[str, Any]:
        """Analyze bitcode file."""
        info = {
            "file_path": bc_file,
            "exists": os.path.exists(bc_file),
            "size": 0,
            "functions": [],
            "globals": [],
            "metadata": {}
        }
        
        if not info["exists"]:
            return info
        
        info["size"] = os.path.getsize(bc_file)
        
        # Use llvm-nm to get symbols
        if "llvm-nm" in self.available_tools:
            try:
                result = subprocess.run(
                    [self.available_tools["llvm-nm"], bc_file],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        parts = line.split()
                        if len(parts) >= 3:
                            symbol_type = parts[1]
                            symbol_name = parts[2]
                            
                            if symbol_type in ['T', 't']:  # Text (function)
                                info["functions"].append(symbol_name)
                            elif symbol_type in ['D', 'd', 'B', 'b']:  # Data/BSS
                                info["globals"].append(symbol_name)
            except:
                pass
        
        return info


# Utility functions
def create_llvm_ir_toolchain(config: Optional[LLVMIRToolchainConfig] = None) -> LLVMIRToolchain:
    """Create LLVM IR toolchain."""
    return LLVMIRToolchain(config)


def build_llvm_ir_project(source_files: List[str], config: Optional[LLVMIRToolchainConfig] = None, output_path: Optional[str] = None) -> BuildResult:
    """Build LLVM IR project."""
    toolchain = create_llvm_ir_toolchain(config)
    return toolchain.build(source_files, output_path)


def run_llvm_ir_executable(executable_path: str, args: List[str] = None, config: Optional[LLVMIRToolchainConfig] = None) -> subprocess.CompletedProcess:
    """Run LLVM IR executable."""
    toolchain = create_llvm_ir_toolchain(config)
    return toolchain.run(executable_path, args)


def debug_llvm_ir_executable(executable_path: str, config: Optional[LLVMIRToolchainConfig] = None) -> bool:
    """Debug LLVM IR executable."""
    # Launch with gdb or lldb
    debuggers = ["gdb", "lldb"]
    
    for debugger in debuggers:
        if shutil.which(debugger):
            try:
                subprocess.run([debugger, executable_path])
                return True
            except:
                continue
    
    print("No debugger available")
    return False 