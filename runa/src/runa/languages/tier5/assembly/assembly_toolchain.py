"""
Assembly Toolchain - Build system integration and development tools for Assembly.

This module provides comprehensive toolchain support for Assembly language development,
including assemblers, linkers, debuggers, and build system integration.
"""

import os
import subprocess
import platform
import shutil
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path
import json

from runa.core.toolchain import BaseToolchain, BuildResult, ToolchainError


@dataclass
class AssemblyToolchainConfig:
    """Configuration for Assembly toolchain."""
    target_architecture: str = "x64"  # x86, x64, arm, arm64, riscv, mips, powerpc
    assembler: str = "nasm"  # nasm, gas, masm, yasm, fasm
    linker: str = "ld"  # ld, gold, lld, link
    format: str = "elf64"  # elf32, elf64, pe32, pe64, macho32, macho64
    optimization_level: str = "O0"  # O0, O1, O2, O3, Os, Oz
    debug_info: bool = True
    include_paths: List[str] = None
    library_paths: List[str] = None
    libraries: List[str] = None
    defines: Dict[str, str] = None
    output_dir: str = "build"
    executable_name: str = "program"
    enable_warnings: bool = True
    treat_warnings_as_errors: bool = False
    verbose: bool = False


class AssemblyToolchain(BaseToolchain):
    """Assembly language toolchain implementation."""
    
    def __init__(self, config: Optional[AssemblyToolchainConfig] = None):
        super().__init__()
        self.config = config or AssemblyToolchainConfig()
        self.build_cache: Dict[str, Any] = {}
        self.available_tools: Dict[str, str] = {}
        self._detect_available_tools()
    
    def _detect_available_tools(self) -> None:
        """Detect available Assembly tools on the system."""
        tools_to_detect = [
            # Assemblers
            "nasm", "gas", "as", "yasm", "fasm", "masm", "tasm",
            # Linkers
            "ld", "ld.gold", "ld.lld", "link",
            # Debuggers
            "gdb", "lldb", "x64dbg", "windbg",
            # Disassemblers
            "objdump", "ndisasm", "dumpbin",
            # Other tools
            "objcopy", "strip", "nm", "readelf", "file", "hexdump"
        ]
        
        for tool in tools_to_detect:
            path = shutil.which(tool)
            if path:
                self.available_tools[tool] = path
    
    def get_available_tools(self) -> Dict[str, str]:
        """Get dictionary of available tools and their paths."""
        return self.available_tools.copy()
    
    def validate_config(self) -> List[str]:
        """Validate toolchain configuration."""
        issues = []
        
        # Check if required assembler is available
        if self.config.assembler not in self.available_tools:
            issues.append(f"Assembler '{self.config.assembler}' not found")
        
        # Check if linker is available
        if self.config.linker not in self.available_tools:
            issues.append(f"Linker '{self.config.linker}' not found")
        
        # Validate architecture
        valid_architectures = ["x86", "x64", "arm", "arm64", "riscv", "mips", "powerpc"]
        if self.config.target_architecture not in valid_architectures:
            issues.append(f"Unsupported architecture: {self.config.target_architecture}")
        
        # Validate format
        valid_formats = ["elf32", "elf64", "pe32", "pe64", "macho32", "macho64", "bin", "coff"]
        if self.config.format not in valid_formats:
            issues.append(f"Unsupported format: {self.config.format}")
        
        # Check include paths
        if self.config.include_paths:
            for path in self.config.include_paths:
                if not os.path.exists(path):
                    issues.append(f"Include path does not exist: {path}")
        
        # Check library paths
        if self.config.library_paths:
            for path in self.config.library_paths:
                if not os.path.exists(path):
                    issues.append(f"Library path does not exist: {path}")
        
        return issues
    
    def build(self, source_files: List[str], output_path: Optional[str] = None) -> BuildResult:
        """Build Assembly source files."""
        try:
            # Validate configuration
            config_issues = self.validate_config()
            if config_issues:
                return BuildResult(
                    success=False,
                    errors=config_issues,
                    warnings=[],
                    output_files=[],
                    metadata={"toolchain": "assembly"}
                )
            
            # Prepare build directory
            build_dir = Path(self.config.output_dir)
            build_dir.mkdir(exist_ok=True)
            
            # Assemble source files
            object_files = []
            all_errors = []
            all_warnings = []
            
            for source_file in source_files:
                obj_file = self._assemble_file(source_file, build_dir)
                if obj_file:
                    object_files.append(obj_file)
                else:
                    all_errors.append(f"Failed to assemble {source_file}")
            
            if not object_files:
                return BuildResult(
                    success=False,
                    errors=all_errors,
                    warnings=all_warnings,
                    output_files=[],
                    metadata={"toolchain": "assembly"}
                )
            
            # Link object files
            executable_path = output_path or str(build_dir / self.config.executable_name)
            link_result = self._link_files(object_files, executable_path)
            
            if link_result:
                return BuildResult(
                    success=True,
                    errors=all_errors,
                    warnings=all_warnings,
                    output_files=[executable_path],
                    metadata={
                        "toolchain": "assembly",
                        "assembler": self.config.assembler,
                        "linker": self.config.linker,
                        "architecture": self.config.target_architecture,
                        "format": self.config.format
                    }
                )
            else:
                all_errors.append("Linking failed")
                return BuildResult(
                    success=False,
                    errors=all_errors,
                    warnings=all_warnings,
                    output_files=object_files,
                    metadata={"toolchain": "assembly"}
                )
        
        except Exception as e:
            return BuildResult(
                success=False,
                errors=[f"Build error: {str(e)}"],
                warnings=[],
                output_files=[],
                metadata={"toolchain": "assembly"}
            )
    
    def _assemble_file(self, source_file: str, build_dir: Path) -> Optional[str]:
        """Assemble a single source file."""
        try:
            source_path = Path(source_file)
            obj_file = build_dir / f"{source_path.stem}.o"
            
            # Build assembler command
            cmd = self._build_assembler_command(source_file, str(obj_file))
            
            if self.config.verbose:
                print(f"Assembling: {' '.join(cmd)}")
            
            # Run assembler
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=build_dir
            )
            
            if result.returncode == 0:
                return str(obj_file)
            else:
                print(f"Assembly failed for {source_file}:")
                print(result.stderr)
                return None
        
        except Exception as e:
            print(f"Error assembling {source_file}: {str(e)}")
            return None
    
    def _build_assembler_command(self, source_file: str, output_file: str) -> List[str]:
        """Build assembler command line."""
        assembler = self.config.assembler
        cmd = [assembler]
        
        if assembler == "nasm":
            cmd.extend(["-f", self._get_nasm_format()])
            if self.config.debug_info:
                cmd.append("-g")
            if self.config.include_paths:
                for path in self.config.include_paths:
                    cmd.extend(["-I", path])
            if self.config.defines:
                for name, value in self.config.defines.items():
                    cmd.extend(["-D", f"{name}={value}"])
            cmd.extend(["-o", output_file, source_file])
        
        elif assembler in ["gas", "as"]:
            cmd.extend(["--" + self._get_gas_arch()])
            if self.config.debug_info:
                cmd.append("-g")
            if self.config.enable_warnings:
                cmd.append("-W")
            if self.config.include_paths:
                for path in self.config.include_paths:
                    cmd.extend(["-I", path])
            cmd.extend(["-o", output_file, source_file])
        
        elif assembler == "yasm":
            cmd.extend(["-f", self._get_yasm_format()])
            if self.config.debug_info:
                cmd.append("-g", "dwarf2")
            if self.config.include_paths:
                for path in self.config.include_paths:
                    cmd.extend(["-I", path])
            cmd.extend(["-o", output_file, source_file])
        
        elif assembler == "fasm":
            # FASM has different syntax
            cmd.extend([source_file, output_file])
        
        elif assembler == "masm":
            cmd.extend(["/c"])  # Compile only
            if self.config.debug_info:
                cmd.append("/Zi")
            cmd.extend(["/Fo" + output_file, source_file])
        
        else:
            # Generic assembler
            cmd.extend(["-o", output_file, source_file])
        
        return cmd
    
    def _link_files(self, object_files: List[str], output_file: str) -> bool:
        """Link object files into executable."""
        try:
            cmd = self._build_linker_command(object_files, output_file)
            
            if self.config.verbose:
                print(f"Linking: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True
            else:
                print(f"Linking failed:")
                print(result.stderr)
                return False
        
        except Exception as e:
            print(f"Error linking: {str(e)}")
            return False
    
    def _build_linker_command(self, object_files: List[str], output_file: str) -> List[str]:
        """Build linker command line."""
        linker = self.config.linker
        cmd = [linker]
        
        if linker == "ld":
            # Entry point
            if self.config.target_architecture in ["x86", "x64"]:
                cmd.extend(["-e", "_start"])
            elif self.config.target_architecture in ["arm", "arm64"]:
                cmd.extend(["-e", "_start"])
            
            # Output file
            cmd.extend(["-o", output_file])
            
            # Library paths
            if self.config.library_paths:
                for path in self.config.library_paths:
                    cmd.extend(["-L", path])
            
            # Libraries
            if self.config.libraries:
                for lib in self.config.libraries:
                    cmd.extend(["-l", lib])
            
            # Object files
            cmd.extend(object_files)
        
        elif linker == "gold" or linker == "ld.gold":
            cmd = ["ld.gold"]
            cmd.extend(["-o", output_file])
            cmd.extend(object_files)
        
        elif linker == "lld" or linker == "ld.lld":
            cmd = ["ld.lld"]
            cmd.extend(["-o", output_file])
            cmd.extend(object_files)
        
        elif linker == "link":  # Microsoft linker
            cmd.extend(["/OUT:" + output_file])
            if self.config.debug_info:
                cmd.append("/DEBUG")
            cmd.extend(object_files)
        
        else:
            # Generic linker
            cmd.extend(["-o", output_file])
            cmd.extend(object_files)
        
        return cmd
    
    def run(self, executable_path: str, args: List[str] = None) -> subprocess.CompletedProcess:
        """Run the compiled executable."""
        cmd = [executable_path]
        if args:
            cmd.extend(args)
        
        return subprocess.run(cmd, capture_output=True, text=True)
    
    def debug(self, executable_path: str, debugger: Optional[str] = None) -> bool:
        """Launch debugger for the executable."""
        if not debugger:
            # Auto-detect debugger
            if "gdb" in self.available_tools:
                debugger = "gdb"
            elif "lldb" in self.available_tools:
                debugger = "lldb"
            else:
                print("No debugger available")
                return False
        
        try:
            if debugger == "gdb":
                subprocess.run([debugger, executable_path])
            elif debugger == "lldb":
                subprocess.run([debugger, executable_path])
            else:
                subprocess.run([debugger, executable_path])
            return True
        except Exception as e:
            print(f"Error launching debugger: {str(e)}")
            return False
    
    def disassemble(self, file_path: str, output_file: Optional[str] = None) -> bool:
        """Disassemble binary file."""
        if "objdump" in self.available_tools:
            cmd = ["objdump", "-d", file_path]
        elif "ndisasm" in self.available_tools:
            cmd = ["ndisasm", "-b", "64" if "64" in self.config.format else "32", file_path]
        else:
            print("No disassembler available")
            return False
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
            else:
                print(result.stdout)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error disassembling: {str(e)}")
            return False
    
    def analyze_binary(self, file_path: str) -> Dict[str, Any]:
        """Analyze binary file and return metadata."""
        info = {
            "file_path": file_path,
            "exists": os.path.exists(file_path),
            "size": 0,
            "architecture": "unknown",
            "format": "unknown",
            "sections": [],
            "symbols": [],
            "dependencies": []
        }
        
        if not info["exists"]:
            return info
        
        info["size"] = os.path.getsize(file_path)
        
        # Use file command to get basic info
        if "file" in self.available_tools:
            try:
                result = subprocess.run(
                    ["file", file_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    file_info = result.stdout.strip()
                    if "x86-64" in file_info:
                        info["architecture"] = "x64"
                    elif "i386" in file_info:
                        info["architecture"] = "x86"
                    elif "ARM" in file_info:
                        info["architecture"] = "arm"
                    
                    if "ELF" in file_info:
                        info["format"] = "elf"
                    elif "PE32" in file_info:
                        info["format"] = "pe"
                    elif "Mach-O" in file_info:
                        info["format"] = "macho"
            except:
                pass
        
        # Use readelf for ELF files
        if "readelf" in self.available_tools and info["format"] == "elf":
            try:
                # Get sections
                result = subprocess.run(
                    ["readelf", "-S", file_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    # Parse section headers (simplified)
                    for line in result.stdout.split('\n'):
                        if line.strip().startswith('[') and ']' in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                section_name = parts[1]
                                info["sections"].append(section_name)
                
                # Get symbols
                result = subprocess.run(
                    ["readelf", "-s", file_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    # Parse symbol table (simplified)
                    for line in result.stdout.split('\n'):
                        parts = line.split()
                        if len(parts) >= 8 and parts[0].isdigit():
                            symbol_name = parts[7]
                            if symbol_name and symbol_name != "UND":
                                info["symbols"].append(symbol_name)
            except:
                pass
        
        # Use objdump for additional info
        if "objdump" in self.available_tools:
            try:
                # Get dynamic dependencies
                result = subprocess.run(
                    ["objdump", "-p", file_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if "NEEDED" in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                dependency = parts[1]
                                info["dependencies"].append(dependency)
            except:
                pass
        
        return info
    
    def create_project(self, project_name: str, project_dir: str) -> bool:
        """Create a new Assembly project."""
        try:
            project_path = Path(project_dir) / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create directory structure
            (project_path / "src").mkdir(exist_ok=True)
            (project_path / "include").mkdir(exist_ok=True)
            (project_path / "build").mkdir(exist_ok=True)
            (project_path / "docs").mkdir(exist_ok=True)
            
            # Create main.asm
            main_asm = project_path / "src" / "main.asm"
            with open(main_asm, 'w') as f:
                f.write(self._get_template_main_asm())
            
            # Create Makefile
            makefile = project_path / "Makefile"
            with open(makefile, 'w') as f:
                f.write(self._get_template_makefile(project_name))
            
            # Create README
            readme = project_path / "README.md"
            with open(readme, 'w') as f:
                f.write(self._get_template_readme(project_name))
            
            # Create .gitignore
            gitignore = project_path / ".gitignore"
            with open(gitignore, 'w') as f:
                f.write(self._get_template_gitignore())
            
            return True
        
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False
    
    def _get_nasm_format(self) -> str:
        """Get NASM format string."""
        format_map = {
            "elf32": "elf32",
            "elf64": "elf64", 
            "pe32": "win32",
            "pe64": "win64",
            "macho32": "macho32",
            "macho64": "macho64",
            "bin": "bin"
        }
        return format_map.get(self.config.format, "elf64")
    
    def _get_gas_arch(self) -> str:
        """Get GAS architecture string."""
        arch_map = {
            "x86": "32",
            "x64": "64",
            "arm": "32",
            "arm64": "64"
        }
        return arch_map.get(self.config.target_architecture, "64")
    
    def _get_yasm_format(self) -> str:
        """Get YASM format string."""
        return self._get_nasm_format()  # YASM uses same formats as NASM
    
    def _get_template_main_asm(self) -> str:
        """Get template main.asm file."""
        if self.config.target_architecture == "x64":
            return '''section .data
    msg db 'Hello, World!', 0xA, 0
    msg_len equ $ - msg

section .text
    global _start

_start:
    ; write system call
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    mov rsi, msg        ; message
    mov rdx, msg_len    ; message length
    syscall

    ; exit system call
    mov rax, 60         ; sys_exit
    mov rdi, 0          ; exit status
    syscall
'''
        else:
            return '''; Assembly program template
; Architecture: ''' + self.config.target_architecture + '''

section .data
    ; Data section

section .text
    global _start

_start:
    ; Program entry point
    
    ; Exit
    mov eax, 1
    int 0x80
'''
    
    def _get_template_makefile(self, project_name: str) -> str:
        """Get template Makefile."""
        return f'''# Makefile for {project_name}

ASM = {self.config.assembler}
LD = {self.config.linker}
FORMAT = {self._get_nasm_format()}

SRCDIR = src
BUILDDIR = build
SOURCES = $(wildcard $(SRCDIR)/*.asm)
OBJECTS = $(SOURCES:$(SRCDIR)/%.asm=$(BUILDDIR)/%.o)
TARGET = $(BUILDDIR)/{project_name}

.PHONY: all clean run debug

all: $(TARGET)

$(TARGET): $(OBJECTS) | $(BUILDDIR)
\t$(LD) -o $@ $^

$(BUILDDIR)/%.o: $(SRCDIR)/%.asm | $(BUILDDIR)
\t$(ASM) -f $(FORMAT) -o $@ $<

$(BUILDDIR):
\tmkdir -p $(BUILDDIR)

clean:
\trm -rf $(BUILDDIR)

run: $(TARGET)
\t./$(TARGET)

debug: $(TARGET)
\tgdb ./$(TARGET)

install: $(TARGET)
\tcp $(TARGET) /usr/local/bin/

.PHONY: help
help:
\t@echo "Available targets:"
\t@echo "  all     - Build the project"
\t@echo "  clean   - Remove build files"  
\t@echo "  run     - Run the executable"
\t@echo "  debug   - Debug with GDB"
\t@echo "  install - Install to system"
\t@echo "  help    - Show this help"
'''
    
    def _get_template_readme(self, project_name: str) -> str:
        """Get template README.md."""
        return f'''# {project_name}

Assembly language project.

## Building

```bash
make
```

## Running

```bash
make run
```

## Debugging

```bash
make debug
```

## Architecture

Target: {self.config.target_architecture}
Format: {self.config.format}
Assembler: {self.config.assembler}

## Project Structure

- `src/` - Source files
- `include/` - Header files
- `build/` - Build output
- `docs/` - Documentation
'''
    
    def _get_template_gitignore(self) -> str:
        """Get template .gitignore."""
        return '''# Build output
build/
*.o
*.obj
*.exe
*.bin
*.elf
*.out

# Debug files
*.pdb
*.dSYM/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
''' 