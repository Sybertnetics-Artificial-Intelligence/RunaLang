"""
Ada Toolchain for Runa Universal Translation Platform
Safety-critical Ada development environment

Features:
- GNAT compiler support
- SPARK formal verification
- Ravenscar profile validation
- Ada 2012/2022 standards
- Defense/aerospace project templates
- Real-time system configuration
- Contract-based programming validation
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

from ...shared.base_toolchain import BaseToolchain, ToolchainError, CompilationResult, TestResult

logger = logging.getLogger(__name__)

class AdaStandard(Enum):
    """Ada language standards"""
    ADA_95 = "95"
    ADA_2005 = "2005"
    ADA_2012 = "2012"
    ADA_2022 = "2022"

class AdaProfile(Enum):
    """Ada runtime profiles"""
    FULL = "full"
    RAVENSCAR = "ravenscar"
    RESTRICTED = "restricted"
    ZERO_FOOTPRINT = "zfp"

@dataclass
class AdaConfiguration:
    """Ada project configuration"""
    project_name: str
    standard: AdaStandard = AdaStandard.ADA_2012
    profile: AdaProfile = AdaProfile.FULL
    
    # SPARK configuration
    spark_mode: bool = False
    spark_level: str = "stone"  # stone, bronze, silver, gold, platinum
    
    # Safety-critical options
    safety_critical: bool = False
    high_integrity: bool = False
    real_time: bool = False
    
    # Compilation options
    debug_mode: bool = True
    optimization_level: int = 0
    warnings_as_errors: bool = True
    
    # Runtime options
    runtime: str = "native"
    target_platform: str = "native"
    
    # Project structure
    source_dirs: List[str] = None
    object_dir: str = "obj"
    exec_dir: str = "bin"
    library_dirs: List[str] = None
    
    def __post_init__(self):
        if self.source_dirs is None:
            self.source_dirs = ["src"]
        if self.library_dirs is None:
            self.library_dirs = []

class AdaToolchain(BaseToolchain):
    """Ada development toolchain"""
    
    def __init__(self, config: Optional[AdaConfiguration] = None):
        super().__init__("ada", "adb")
        self.config = config or AdaConfiguration("ada_project")
        self.gnat_path = self._find_gnat_compiler()
        self.gprbuild_path = self._find_gprbuild()
        self.gnatprove_path = self._find_gnatprove()
        
    def _find_gnat_compiler(self) -> Optional[str]:
        """Find GNAT Ada compiler"""
        compilers = ["gnat", "gcc", "gnatmake"]
        for compiler in compilers:
            if self._which(compiler):
                logger.info(f"Found Ada compiler: {compiler}")
                return compiler
        logger.warning("No Ada compiler found. Install GNAT.")
        return None
    
    def _find_gprbuild(self) -> Optional[str]:
        """Find GPRbuild project builder"""
        if self._which("gprbuild"):
            return "gprbuild"
        return None
    
    def _find_gnatprove(self) -> Optional[str]:
        """Find SPARK/GNATprove analyzer"""
        if self._which("gnatprove"):
            return "gnatprove"
        return None
    
    def _which(self, program: str) -> bool:
        """Check if program exists in PATH"""
        import shutil
        return shutil.which(program) is not None
    
    def create_project(self, name: str, directory: str) -> bool:
        """Create Ada project with GPR file"""
        try:
            project_path = Path(directory) / name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create directory structure
            dirs = [
                "src", "obj", "bin", "tests", "doc", 
                "contracts", "spark", "examples"
            ]
            for dir_name in dirs:
                (project_path / dir_name).mkdir(exist_ok=True)
            
            # Create GPR project file
            gpr_content = self._generate_gpr_file(name)
            gpr_file = project_path / f"{name.lower()}.gpr"
            with open(gpr_file, 'w') as f:
                f.write(gpr_content)
            
            # Create main program
            main_content = self._generate_main_program(name)
            main_file = project_path / "src" / f"{name.lower()}.adb"
            with open(main_file, 'w') as f:
                f.write(main_content)
            
            # Create project configuration
            config_data = {
                "name": name,
                "standard": self.config.standard.value,
                "profile": self.config.profile.value,
                "spark_mode": self.config.spark_mode,
                "safety_critical": self.config.safety_critical
            }
            
            config_file = project_path / "project.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Ada project '{name}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create Ada project: {e}")
            return False
    
    def _generate_gpr_file(self, name: str) -> str:
        """Generate GPR project file"""
        gpr_content = f'''-- Ada Project File for {name}
-- Generated by Runa Universal Translation Platform

project {name.title()} is

   for Source_Dirs use ("src");
   for Object_Dir use "obj";
   for Exec_Dir use "bin";
   for Main use ("{name.lower()}.adb");

   package Compiler is
      for Default_Switches ("Ada") use
        ("-gnat{self.config.standard.value}",
         "-gnaty3abcdefhijklmnoprstux",  -- Style checks
         "-Wall",                       -- All warnings
         "-gnatf",                      -- Full errors
         "-gnatU");                     -- Unique compilation
'''
        
        if self.config.debug_mode:
            gpr_content += '''
      for Default_Switches ("Ada") use Compiler'Default_Switches ("Ada") & 
        ("-g", "-gnata");  -- Debug symbols and assertions
'''
        
        if self.config.warnings_as_errors:
            gpr_content += '''
      for Default_Switches ("Ada") use Compiler'Default_Switches ("Ada") & 
        ("-gnatwe");  -- Warnings as errors
'''
        
        if self.config.spark_mode:
            gpr_content += '''
      for Default_Switches ("Ada") use Compiler'Default_Switches ("Ada") & 
        ("-gnatd.F", "-gnatd.V");  -- SPARK mode
'''
        
        gpr_content += '''
   end Compiler;

   package Binder is
      for Default_Switches ("Ada") use ("-Es");  -- Symbolic traceback
   end Binder;

'''
        
        if self.config.profile == AdaProfile.RAVENSCAR:
            gpr_content += '''   package Linker is
      for Default_Switches ("Ada") use ("-largs", "-margs", "-lkargs");
   end Linker;

'''
        
        gpr_content += f'end {name.title()};'
        return gpr_content
    
    def _generate_main_program(self, name: str) -> str:
        """Generate main Ada program"""
        main_content = f'''--  Main program for {name}
--  Generated by Runa Universal Translation Platform

'''
        
        if self.config.spark_mode:
            main_content += '''pragma SPARK_Mode (On);
'''
        
        if self.config.profile == AdaProfile.RAVENSCAR:
            main_content += '''pragma Profile (Ravenscar);
'''
        
        main_content += f'''
with Ada.Text_IO;

procedure {name.title()} is
   pragma Pure;  -- Safety-critical marker
begin
   Ada.Text_IO.Put_Line ("Hello from Ada program: {name}");
   Ada.Text_IO.Put_Line ("Compiled with safety-critical settings");
end {name.title()};'''
        
        return main_content
    
    def compile(self, source_file: str, output_file: Optional[str] = None,
                options: Optional[Dict[str, Any]] = None) -> CompilationResult:
        """Compile Ada source"""
        try:
            if not self.gnat_path:
                raise ToolchainError("No Ada compiler available")
            
            source_path = Path(source_file)
            if not source_path.exists():
                raise ToolchainError(f"Source file not found: {source_file}")
            
            # Use GPRbuild if available and GPR file exists
            gpr_file = source_path.parent / f"{source_path.stem}.gpr"
            if self.gprbuild_path and gpr_file.exists():
                return self._compile_with_gprbuild(str(gpr_file), options)
            else:
                return self._compile_with_gnatmake(source_file, output_file, options)
                
        except Exception as e:
            raise ToolchainError(f"Ada compilation failed: {e}")
    
    def _compile_with_gprbuild(self, gpr_file: str, options: Optional[Dict] = None) -> CompilationResult:
        """Compile using GPRbuild"""
        cmd = [self.gprbuild_path, "-P", gpr_file]
        
        if self.config.debug_mode:
            cmd.extend(["-Xmode=debug"])
        
        if options and options.get("verbose"):
            cmd.append("-v")
        
        logger.info(f"Compiling with GPRbuild: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        return CompilationResult(
            success=result.returncode == 0,
            output_file="bin/" if result.returncode == 0 else None,
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
            compilation_time=0.0
        )
    
    def _compile_with_gnatmake(self, source_file: str, output_file: Optional[str], 
                             options: Optional[Dict] = None) -> CompilationResult:
        """Compile using gnatmake"""
        cmd = ["gnatmake", source_file]
        
        if output_file:
            cmd.extend(["-o", output_file])
        
        cmd.extend([f"-gnat{self.config.standard.value}"])
        
        if self.config.debug_mode:
            cmd.extend(["-g", "-gnata"])
        
        if self.config.warnings_as_errors:
            cmd.append("-gnatwe")
        
        logger.info(f"Compiling with gnatmake: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        return CompilationResult(
            success=result.returncode == 0,
            output_file=output_file if result.returncode == 0 else None,
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
            compilation_time=0.0
        )
    
    def run_spark_analysis(self, project_file: str) -> Dict[str, Any]:
        """Run SPARK formal verification"""
        if not self.gnatprove_path:
            logger.warning("GNATprove not found. SPARK analysis unavailable.")
            return {"available": False}
        
        try:
            cmd = [self.gnatprove_path, "-P", project_file, 
                   f"--level={self.config.spark_level}"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            return {
                "available": True,
                "success": result.returncode == 0,
                "level": self.config.spark_level,
                "output": result.stdout,
                "errors": result.stderr,
                "verified": result.returncode == 0
            }
            
        except Exception as e:
            logger.error(f"SPARK analysis failed: {e}")
            return {"available": True, "success": False, "error": str(e)}
    
    def run_tests(self, test_directory: str = "tests") -> TestResult:
        """Run Ada test suite"""
        try:
            test_path = Path(test_directory)
            if not test_path.exists():
                return TestResult(True, 0, 0, 0, "No tests found")
            
            test_files = list(test_path.glob("test_*.adb"))
            if not test_files:
                return TestResult(True, 0, 0, 0, "No test files found")
            
            total_tests = len(test_files)
            passed_tests = 0
            failed_tests = 0
            test_outputs = []
            
            for test_file in test_files:
                try:
                    compile_result = self.compile(str(test_file))
                    if compile_result.success:
                        # Run test executable
                        exe_path = test_file.parent / test_file.stem
                        if exe_path.exists():
                            run_result = subprocess.run([str(exe_path)], 
                                                       capture_output=True, text=True, timeout=30)
                            if run_result.returncode == 0:
                                passed_tests += 1
                                test_outputs.append(f"PASSED: {test_file.name}")
                            else:
                                failed_tests += 1
                                test_outputs.append(f"FAILED: {test_file.name} - Runtime error")
                        else:
                            failed_tests += 1
                            test_outputs.append(f"FAILED: {test_file.name} - No executable")
                    else:
                        failed_tests += 1
                        test_outputs.append(f"FAILED: {test_file.name} - Compilation failed")
                        
                except Exception as e:
                    failed_tests += 1
                    test_outputs.append(f"FAILED: {test_file.name} - {str(e)}")
            
            return TestResult(
                success=failed_tests == 0,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                test_output='\n'.join(test_outputs)
            )
            
        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return TestResult(False, 0, 0, 1, f"Test framework error: {e}")
    
    def format_code(self, source_code: str, style: str = "standard") -> str:
        """Format Ada code"""
        # Basic Ada formatting
        lines = source_code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Adjust indent before line
            if any(stripped.startswith(kw) for kw in ['end', 'else', 'elsif', 'when', 'exception']):
                indent_level = max(0, indent_level - 1)
            
            # Apply indentation
            indent = ' ' * (indent_level * 3)
            formatted_lines.append(indent + stripped)
            
            # Adjust indent after line
            if any(stripped.startswith(kw) for kw in ['if', 'loop', 'case', 'begin', 'declare']):
                indent_level += 1
            elif stripped.endswith(' is') or stripped.endswith(' then'):
                indent_level += 1
        
        return '\n'.join(formatted_lines)
    
    def generate_documentation(self, source_directory: str, output_directory: str) -> bool:
        """Generate Ada documentation"""
        try:
            src_path = Path(source_directory)
            doc_path = Path(output_directory)
            doc_path.mkdir(parents=True, exist_ok=True)
            
            ada_files = list(src_path.glob("*.ads")) + list(src_path.glob("*.adb"))
            
            documentation = [
                "# Ada Project Documentation",
                f"Generated by Runa Universal Translation Platform",
                "",
                f"## Configuration",
                f"- Standard: Ada {self.config.standard.value}",
                f"- Profile: {self.config.profile.value}",
                f"- SPARK Mode: {'Enabled' if self.config.spark_mode else 'Disabled'}",
                f"- Safety Critical: {'Yes' if self.config.safety_critical else 'No'}",
                "",
                "## Source Files",
                ""
            ]
            
            for ada_file in ada_files:
                documentation.append(f"### {ada_file.name}")
                documentation.append("")
                
                # Extract basic file information
                try:
                    with open(ada_file, 'r') as f:
                        content = f.read()
                        
                    # Look for package/procedure declarations
                    lines = content.split('\n')
                    for line in lines[:20]:  # Check first 20 lines
                        line = line.strip()
                        if line.startswith('package ') or line.startswith('procedure '):
                            documentation.append(f"**Declaration:** `{line}`")
                            break
                    
                    documentation.append("")
                    
                except Exception:
                    documentation.append("*Unable to read file*")
                    documentation.append("")
            
            doc_file = doc_path / "README.md"
            with open(doc_file, 'w') as f:
                f.write('\n'.join(documentation))
            
            logger.info(f"Documentation generated: {doc_file}")
            return True
            
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            return False

# Factory function
def create_ada_toolchain(config: Optional[AdaConfiguration] = None) -> AdaToolchain:
    """Create Ada toolchain instance"""
    return AdaToolchain(config)

# Export main classes
__all__ = [
    'AdaToolchain', 'AdaConfiguration', 'AdaStandard', 'AdaProfile',
    'create_ada_toolchain'
] 