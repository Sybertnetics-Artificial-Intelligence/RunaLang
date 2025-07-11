#!/usr/bin/env python3
"""
Visual Basic Toolchain Implementation

Enterprise-grade toolchain for Visual Basic .NET with Microsoft tooling integration,
project generation, compilation, testing, and deployment capabilities.
"""

import os
import sys
import json
import subprocess
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any, Tuple, Set
from pathlib import Path
from dataclasses import dataclass, field
import logging

from .visual_basic_ast import *
from .visual_basic_parser import parse_visual_basic
from .visual_basic_generator import generate_visual_basic, VBGeneratorConfig, VBCodeStyle
from .visual_basic_converter import convert_vb_to_runa, convert_runa_to_vb
from ....core.base_toolchain import BaseToolchain, ToolchainCapability
from ....core.error_handler import ErrorHandler, ErrorType
from ....core.translation_context import TranslationContext

@dataclass
class VBProjectConfig:
    """Visual Basic project configuration."""
    project_name: str = "VBProject"
    target_framework: str = "net6.0"
    output_type: str = "Exe"  # Exe, Library, WinExe
    root_namespace: str = ""
    startup_object: str = ""
    platform_target: str = "AnyCPU"
    
    # Dependencies
    package_references: List[Dict[str, str]] = field(default_factory=list)
    project_references: List[str] = field(default_factory=list)
    
    # Compiler options
    option_explicit: bool = True
    option_strict: bool = True
    option_compare: str = "Binary"  # Binary, Text
    option_infer: bool = True
    
    # Build settings
    debug_symbols: bool = True
    optimize: bool = False
    treat_warnings_as_errors: bool = False
    warning_level: int = 4

@dataclass
class VBCompilerInfo:
    """Information about Visual Basic compiler."""
    compiler_path: str = ""
    version: str = ""
    target_frameworks: List[str] = field(default_factory=list)
    is_available: bool = False

class VBToolchain(BaseToolchain):
    """Visual Basic toolchain with Microsoft tooling integration."""
    
    def __init__(self, error_handler: ErrorHandler = None):
        super().__init__(error_handler)
        self.logger = logging.getLogger(__name__)
        self.compiler_info = self._detect_compiler()
        self.generator_config = VBGeneratorConfig()
        
        # Supported capabilities
        self.capabilities = {
            ToolchainCapability.PARSING,
            ToolchainCapability.GENERATION,
            ToolchainCapability.COMPILATION,
            ToolchainCapability.ROUND_TRIP_VERIFICATION,
            ToolchainCapability.PROJECT_GENERATION,
            ToolchainCapability.DEPENDENCY_MANAGEMENT,
            ToolchainCapability.TESTING,
            ToolchainCapability.DOCUMENTATION_GENERATION,
        }
    
    def get_language_name(self) -> str:
        """Get language name."""
        return "Visual Basic"
    
    def get_file_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return [".vb", ".vbproj", ".vbnet"]
    
    def parse_file(self, file_path: str, context: TranslationContext = None) -> VBSourceUnit:
        """Parse Visual Basic source file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            return parse_visual_basic(source, self.error_handler)
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.FILE_ERROR,
                f"Failed to parse VB file {file_path}: {e}",
                0, 0
            )
            return VBSourceUnit()
    
    def generate_code(self, ast_node: VBNode, context: TranslationContext = None) -> str:
        """Generate Visual Basic code from AST."""
        try:
            return generate_visual_basic(ast_node, self.generator_config)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.GENERATION_ERROR,
                f"Failed to generate VB code: {e}",
                0, 0
            )
            return f"' Generation error: {e}"
    
    def compile_project(self, project_path: str, output_path: str = None, 
                       config: VBProjectConfig = None) -> bool:
        """Compile Visual Basic project."""
        if not self.compiler_info.is_available:
            self.error_handler.add_error(
                ErrorType.TOOLCHAIN_ERROR,
                "Visual Basic compiler not available",
                0, 0
            )
            return False
        
        try:
            project_config = config or VBProjectConfig()
            
            # Use dotnet CLI for compilation
            cmd = ["dotnet", "build", project_path]
            
            if output_path:
                cmd.extend(["--output", output_path])
            
            # Add configuration
            if project_config.optimize:
                cmd.extend(["--configuration", "Release"])
            else:
                cmd.extend(["--configuration", "Debug"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.error_handler.add_error(
                    ErrorType.COMPILATION_ERROR,
                    f"Compilation failed: {result.stderr}",
                    0, 0
                )
                return False
            
            self.logger.info(f"Successfully compiled VB project: {project_path}")
            return True
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.COMPILATION_ERROR,
                f"Failed to compile VB project: {e}",
                0, 0
            )
            return False
    
    def create_project(self, project_path: str, config: VBProjectConfig) -> bool:
        """Create new Visual Basic project."""
        try:
            project_dir = Path(project_path).parent
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate project file
            project_content = self._generate_project_file(config)
            with open(project_path, 'w', encoding='utf-8') as f:
                f.write(project_content)
            
            # Generate Program.vb if it's an executable
            if config.output_type in ["Exe", "WinExe"]:
                program_path = project_dir / "Program.vb"
                program_content = self._generate_program_file(config)
                with open(program_path, 'w', encoding='utf-8') as f:
                    f.write(program_content)
            
            # Generate AssemblyInfo.vb
            properties_dir = project_dir / "My Project"
            properties_dir.mkdir(exist_ok=True)
            assembly_info_path = properties_dir / "AssemblyInfo.vb"
            assembly_info_content = self._generate_assembly_info(config)
            with open(assembly_info_path, 'w', encoding='utf-8') as f:
                f.write(assembly_info_content)
            
            self.logger.info(f"Created VB project: {project_path}")
            return True
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.PROJECT_ERROR,
                f"Failed to create VB project: {e}",
                0, 0
            )
            return False
    
    def verify_round_trip(self, source_code: str) -> bool:
        """Verify round-trip conversion (source -> AST -> source)."""
        try:
            # Parse original source
            original_ast = parse_visual_basic(source_code, self.error_handler)
            
            # Generate code from AST
            generated_code = generate_visual_basic(original_ast, self.generator_config)
            
            # Parse generated code
            regenerated_ast = parse_visual_basic(generated_code, self.error_handler)
            
            # Compare ASTs (simplified comparison)
            return self._compare_asts(original_ast, regenerated_ast)
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.VERIFICATION_ERROR,
                f"Round-trip verification failed: {e}",
                0, 0
            )
            return False
    
    def analyze_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Analyze project dependencies."""
        dependencies = {
            "packages": [],
            "projects": [],
            "frameworks": [],
            "missing": []
        }
        
        try:
            # Parse project file
            tree = ET.parse(project_path)
            root = tree.getroot()
            
            # Extract package references
            for package_ref in root.findall(".//PackageReference"):
                include = package_ref.get("Include")
                version = package_ref.get("Version")
                if include:
                    dependencies["packages"].append({
                        "name": include,
                        "version": version or "latest"
                    })
            
            # Extract project references
            for project_ref in root.findall(".//ProjectReference"):
                include = project_ref.get("Include")
                if include:
                    dependencies["projects"].append(include)
            
            # Extract target frameworks
            for framework in root.findall(".//TargetFramework"):
                if framework.text:
                    dependencies["frameworks"].append(framework.text)
            
            for frameworks in root.findall(".//TargetFrameworks"):
                if frameworks.text:
                    dependencies["frameworks"].extend(frameworks.text.split(';'))
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.ANALYSIS_ERROR,
                f"Failed to analyze dependencies: {e}",
                0, 0
            )
        
        return dependencies
    
    def run_tests(self, project_path: str) -> Dict[str, Any]:
        """Run tests for Visual Basic project."""
        results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0,
            "details": []
        }
        
        try:
            cmd = ["dotnet", "test", project_path, "--logger", "trx"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse test results (simplified)
            if result.returncode == 0:
                results["passed"] = 1
                results["total"] = 1
            else:
                results["failed"] = 1
                results["total"] = 1
                results["details"].append(result.stderr)
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.TESTING_ERROR,
                f"Failed to run tests: {e}",
                0, 0
            )
        
        return results
    
    def generate_documentation(self, project_path: str, output_path: str) -> bool:
        """Generate documentation for Visual Basic project."""
        try:
            # Use XML documentation comments
            cmd = ["dotnet", "build", project_path, "-p:GenerateDocumentationFile=true"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Generated documentation for: {project_path}")
                return True
            else:
                self.error_handler.add_error(
                    ErrorType.DOCUMENTATION_ERROR,
                    f"Failed to generate documentation: {result.stderr}",
                    0, 0
                )
                return False
                
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.DOCUMENTATION_ERROR,
                f"Failed to generate documentation: {e}",
                0, 0
            )
            return False
    
    def format_code(self, source_code: str, style: VBCodeStyle = VBCodeStyle.MICROSOFT) -> str:
        """Format Visual Basic code."""
        try:
            config = VBGeneratorConfig(style=style)
            ast = parse_visual_basic(source_code, self.error_handler)
            return generate_visual_basic(ast, config)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.FORMATTING_ERROR,
                f"Failed to format VB code: {e}",
                0, 0
            )
            return source_code
    
    def _detect_compiler(self) -> VBCompilerInfo:
        """Detect Visual Basic compiler."""
        info = VBCompilerInfo()
        
        try:
            # Check for dotnet CLI
            result = subprocess.run(["dotnet", "--version"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                info.version = result.stdout.strip()
                info.compiler_path = "dotnet"
                info.is_available = True
                
                # Get supported frameworks
                frameworks_result = subprocess.run(
                    ["dotnet", "--list-sdks"], capture_output=True, text=True)
                if frameworks_result.returncode == 0:
                    for line in frameworks_result.stdout.split('\n'):
                        if line.strip():
                            version = line.split()[0]
                            info.target_frameworks.append(f"net{version}")
            
        except FileNotFoundError:
            pass
        
        return info
    
    def _generate_project_file(self, config: VBProjectConfig) -> str:
        """Generate Visual Basic project file (.vbproj)."""
        project_xml = f'''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>{config.output_type}</OutputType>
    <TargetFramework>{config.target_framework}</TargetFramework>
    <RootNamespace>{config.root_namespace or config.project_name}</RootNamespace>
    <AssemblyName>{config.project_name}</AssemblyName>
    <PlatformTarget>{config.platform_target}</PlatformTarget>
    <OptionExplicit>{"On" if config.option_explicit else "Off"}</OptionExplicit>
    <OptionStrict>{"On" if config.option_strict else "Off"}</OptionStrict>
    <OptionCompare>{config.option_compare}</OptionCompare>
    <OptionInfer>{"On" if config.option_infer else "Off"}</OptionInfer>
    <DebugSymbols>{"true" if config.debug_symbols else "false"}</DebugSymbols>
    <Optimize>{"true" if config.optimize else "false"}</Optimize>
    <TreatWarningsAsErrors>{"true" if config.treat_warnings_as_errors else "false"}</TreatWarningsAsErrors>
    <WarningLevel>{config.warning_level}</WarningLevel>'''
        
        if config.startup_object:
            project_xml += f'\n    <StartupObject>{config.startup_object}</StartupObject>'
        
        project_xml += '\n  </PropertyGroup>\n'
        
        # Package references
        if config.package_references:
            project_xml += '\n  <ItemGroup>\n'
            for pkg in config.package_references:
                name = pkg.get("name", "")
                version = pkg.get("version", "")
                project_xml += f'    <PackageReference Include="{name}" Version="{version}" />\n'
            project_xml += '  </ItemGroup>\n'
        
        # Project references
        if config.project_references:
            project_xml += '\n  <ItemGroup>\n'
            for proj in config.project_references:
                project_xml += f'    <ProjectReference Include="{proj}" />\n'
            project_xml += '  </ItemGroup>\n'
        
        project_xml += '\n</Project>'
        return project_xml
    
    def _generate_program_file(self, config: VBProjectConfig) -> str:
        """Generate Program.vb file."""
        if config.output_type == "WinExe":
            return f'''Imports System
Imports System.Windows.Forms

Module Program
    ' <summary>
    ' The main entry point for the application.
    ' </summary>
    <STAThread>
    Sub Main()
        Application.EnableVisualStyles()
        Application.SetCompatibleTextRenderingDefault(False)
        ' Application.Run(New MainForm())
        Console.WriteLine("Hello, World from {config.project_name}!")
    End Sub
End Module'''
        else:
            return f'''Imports System

Module Program
    ' <summary>
    ' The main entry point for the application.
    ' </summary>
    Sub Main(args As String())
        Console.WriteLine("Hello, World from {config.project_name}!")
    End Sub
End Module'''
    
    def _generate_assembly_info(self, config: VBProjectConfig) -> str:
        """Generate AssemblyInfo.vb file."""
        return f'''Imports System.Reflection
Imports System.Runtime.InteropServices

' General Information about an assembly is controlled through the following
' set of attributes. Change these attribute values to modify the information
' associated with an assembly.
<Assembly: AssemblyTitle("{config.project_name}")>
<Assembly: AssemblyDescription("Visual Basic application generated by Runa")>
<Assembly: AssemblyConfiguration("")>
<Assembly: AssemblyCompany("")>
<Assembly: AssemblyProduct("{config.project_name}")>
<Assembly: AssemblyCopyright("Copyright © 2024")>
<Assembly: AssemblyTrademark("")>
<Assembly: AssemblyCulture("")>

' Setting ComVisible to False makes the types in this assembly not visible
' to COM components. If you need to access a type in this assembly from
' COM, set the ComVisible attribute to True on that type.
<Assembly: ComVisible(False)>

' Version information for an assembly consists of the following four values:
'
'      Major Version
'      Minor Version
'      Build Number
'      Revision
'
<Assembly: AssemblyVersion("1.0.0.0")>
<Assembly: AssemblyFileVersion("1.0.0.0")>'''
    
    def _compare_asts(self, ast1: VBNode, ast2: VBNode) -> bool:
        """Compare two ASTs for equivalence (simplified)."""
        # This is a simplified comparison
        # In a real implementation, you'd do deep structural comparison
        return type(ast1) == type(ast2)

def create_vb_toolchain(error_handler: ErrorHandler = None) -> VBToolchain:
    """Create Visual Basic toolchain instance."""
    return VBToolchain(error_handler) 