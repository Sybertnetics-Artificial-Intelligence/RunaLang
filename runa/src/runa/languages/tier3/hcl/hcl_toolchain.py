#!/usr/bin/env python3
"""
HCL Toolchain - Complete HCL and Terraform Toolchain Integration

Provides comprehensive HCL toolchain capabilities including:
- HCL parsing, validation, and formatting
- Terraform CLI integration and workflow
- Configuration analysis and linting
- Provider and module management
- Plan generation and validation
- Round-trip translation verification
- Infrastructure deployment (dry-run mode)
- Configuration optimization and refactoring

Supports HCL 1.0/2.0 and Terraform 0.12+ workflows.
"""

import os
import json
import subprocess
import tempfile
import shutil
from typing import List, Dict, Optional, Any, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from .hcl_ast import *
from .hcl_parser import parse_hcl, HCLLexer, HCLParser
from .hcl_converter import hcl_to_runa, runa_to_hcl, HCLToRunaConverter, RunaToHCLConverter
from .hcl_generator import generate_hcl, HCLCodeGenerator, HCLFormatStyle, HCLGeneratorConfig


class HCLValidationLevel(Enum):
    """HCL validation levels"""
    SYNTAX = "syntax"           # Basic syntax validation
    SEMANTIC = "semantic"       # Semantic validation with type checking
    TERRAFORM = "terraform"     # Terraform-specific validation
    COMPLETE = "complete"       # Full validation with provider schemas


class TerraformCommand(Enum):
    """Terraform CLI commands"""
    INIT = "init"
    PLAN = "plan"
    APPLY = "apply"
    DESTROY = "destroy"
    VALIDATE = "validate"
    FORMAT = "fmt"
    IMPORT = "import"
    REFRESH = "refresh"
    OUTPUT = "output"
    WORKSPACE = "workspace"
    PROVIDERS = "providers"


@dataclass
class HCLDiagnostic:
    """HCL diagnostic message"""
    level: str  # "error", "warning", "info"
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class TerraformPlan:
    """Terraform plan result"""
    resources_to_add: List[Dict[str, Any]]
    resources_to_change: List[Dict[str, Any]]
    resources_to_destroy: List[Dict[str, Any]]
    output_changes: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    success: bool


@dataclass
class HCLToolchainConfig:
    """Configuration for HCL toolchain"""
    terraform_version: str = "1.0"
    terraform_path: str = "terraform"
    validation_level: HCLValidationLevel = HCLValidationLevel.SEMANTIC
    auto_format: bool = True
    auto_init: bool = True
    dry_run_only: bool = True  # Safety: never actually apply changes
    workspace: str = "default"
    
    # Provider configuration
    provider_cache_dir: Optional[str] = None
    provider_mirror_url: Optional[str] = None
    
    # Validation options
    check_provider_schemas: bool = True
    check_module_dependencies: bool = True
    check_variable_usage: bool = True
    check_resource_references: bool = True
    
    # Formatting options
    format_style: HCLFormatStyle = HCLFormatStyle.TERRAFORM
    sort_attributes: bool = True
    align_attributes: bool = True


class HCLToolchain:
    """Complete HCL and Terraform toolchain"""
    
    def __init__(self, config: Optional[HCLToolchainConfig] = None):
        self.config = config or HCLToolchainConfig()
        self.terraform_available = self._check_terraform_availability()
        self.working_directory: Optional[str] = None
        self.provider_schemas: Dict[str, Any] = {}
        self.module_cache: Dict[str, Any] = {}
        
        # Built-in HCL validators
        self.builtin_functions = HCL_BUILTIN_FUNCTIONS
        self.terraform_blocks = HCL_BLOCK_TYPES
    
    def parse_hcl_file(self, file_path: str) -> Tuple[Optional[HCLConfiguration], List[HCLDiagnostic]]:
        """Parse HCL file and return AST with diagnostics"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse HCL
            ast = parse_hcl(content, file_path)
            
            # Validate based on configuration
            validation_diagnostics = self._validate_ast(ast, file_path)
            diagnostics.extend(validation_diagnostics)
            
            return ast, diagnostics
            
        except FileNotFoundError:
            diagnostics.append(HCLDiagnostic(
                level="error",
                message=f"File not found: {file_path}",
                file=file_path
            ))
            return None, diagnostics
            
        except Exception as e:
            diagnostics.append(HCLDiagnostic(
                level="error",
                message=f"Parse error: {str(e)}",
                file=file_path
            ))
            return None, diagnostics
    
    def parse_hcl_directory(self, directory: str) -> Tuple[List[HCLConfiguration], List[HCLDiagnostic]]:
        """Parse all HCL files in directory"""
        configurations = []
        all_diagnostics = []
        
        hcl_files = []
        for ext in ['.hcl', '.tf', '.tfvars']:
            hcl_files.extend(Path(directory).glob(f'**/*{ext}'))
        
        for file_path in hcl_files:
            ast, diagnostics = self.parse_hcl_file(str(file_path))
            if ast:
                configurations.append(ast)
            all_diagnostics.extend(diagnostics)
        
        return configurations, all_diagnostics
    
    def validate_configuration(self, config: HCLConfiguration, file_path: Optional[str] = None) -> List[HCLDiagnostic]:
        """Validate HCL configuration"""
        return self._validate_ast(config, file_path)
    
    def format_hcl_file(self, file_path: str, in_place: bool = False) -> Tuple[str, List[HCLDiagnostic]]:
        """Format HCL file"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse and format
            ast = parse_hcl(content, file_path)
            generator_config = HCLGeneratorConfig(
                style=self.config.format_style,
                sort_attributes=self.config.sort_attributes,
                align_attributes=self.config.align_attributes
            )
            generator = HCLCodeGenerator(generator_config)
            formatted_content = generator.generate(ast)
            
            if in_place:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                diagnostics.append(HCLDiagnostic(
                    level="info",
                    message=f"Formatted file: {file_path}",
                    file=file_path
                ))
            
            return formatted_content, diagnostics
            
        except Exception as e:
            diagnostics.append(HCLDiagnostic(
                level="error",
                message=f"Format error: {str(e)}",
                file=file_path
            ))
            return "", diagnostics
    
    def terraform_init(self, directory: str) -> Tuple[bool, List[HCLDiagnostic]]:
        """Initialize Terraform configuration"""
        if not self.terraform_available:
            return False, [HCLDiagnostic(
                level="error",
                message="Terraform CLI not available"
            )]
        
        try:
            result = subprocess.run(
                [self.config.terraform_path, "init"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            diagnostics = self._parse_terraform_output(result.stdout, result.stderr)
            return result.returncode == 0, diagnostics
            
        except subprocess.TimeoutExpired:
            return False, [HCLDiagnostic(
                level="error",
                message="Terraform init timed out"
            )]
        except Exception as e:
            return False, [HCLDiagnostic(
                level="error",
                message=f"Terraform init failed: {str(e)}"
            )]
    
    def terraform_validate(self, directory: str) -> Tuple[bool, List[HCLDiagnostic]]:
        """Validate Terraform configuration"""
        if not self.terraform_available:
            return False, [HCLDiagnostic(
                level="error",
                message="Terraform CLI not available"
            )]
        
        try:
            # Ensure initialized
            if self.config.auto_init:
                init_success, _ = self.terraform_init(directory)
                if not init_success:
                    return False, [HCLDiagnostic(
                        level="error",
                        message="Failed to initialize Terraform"
                    )]
            
            result = subprocess.run(
                [self.config.terraform_path, "validate", "-json"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            diagnostics = []
            
            if result.stdout:
                try:
                    validation_result = json.loads(result.stdout)
                    if not validation_result.get("valid", False):
                        for diag in validation_result.get("diagnostics", []):
                            diagnostics.append(HCLDiagnostic(
                                level=diag.get("severity", "error"),
                                message=diag.get("summary", "Unknown error"),
                                file=diag.get("range", {}).get("filename"),
                                line=diag.get("range", {}).get("start", {}).get("line"),
                                column=diag.get("range", {}).get("start", {}).get("column")
                            ))
                except json.JSONDecodeError:
                    diagnostics.extend(self._parse_terraform_output(result.stdout, result.stderr))
            
            return result.returncode == 0, diagnostics
            
        except Exception as e:
            return False, [HCLDiagnostic(
                level="error",
                message=f"Terraform validate failed: {str(e)}"
            )]
    
    def terraform_plan(self, directory: str, var_files: Optional[List[str]] = None) -> Tuple[Optional[TerraformPlan], List[HCLDiagnostic]]:
        """Generate Terraform plan"""
        if not self.terraform_available:
            return None, [HCLDiagnostic(
                level="error",
                message="Terraform CLI not available"
            )]
        
        try:
            # Build command
            cmd = [self.config.terraform_path, "plan", "-json", "-no-color"]
            
            if var_files:
                for var_file in var_files:
                    cmd.extend(["-var-file", var_file])
            
            result = subprocess.run(
                cmd,
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            diagnostics = []
            plan = None
            
            if result.stdout:
                try:
                    # Parse JSON output line by line
                    resources_to_add = []
                    resources_to_change = []
                    resources_to_destroy = []
                    output_changes = {}
                    warnings = []
                    errors = []
                    
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            try:
                                json_line = json.loads(line)
                                msg_type = json_line.get("type")
                                
                                if msg_type == "diagnostic":
                                    diag = json_line.get("diagnostic", {})
                                    diagnostics.append(HCLDiagnostic(
                                        level=diag.get("severity", "info"),
                                        message=diag.get("summary", ""),
                                        file=diag.get("range", {}).get("filename"),
                                        line=diag.get("range", {}).get("start", {}).get("line")
                                    ))
                                
                                elif msg_type == "resource_drift":
                                    # Handle resource changes
                                    change = json_line.get("change", {})
                                    if change.get("action") == "create":
                                        resources_to_add.append(change)
                                    elif change.get("action") == "update":
                                        resources_to_change.append(change)
                                    elif change.get("action") == "delete":
                                        resources_to_destroy.append(change)
                                
                            except json.JSONDecodeError:
                                continue
                    
                    plan = TerraformPlan(
                        resources_to_add=resources_to_add,
                        resources_to_change=resources_to_change,
                        resources_to_destroy=resources_to_destroy,
                        output_changes=output_changes,
                        warnings=warnings,
                        errors=errors,
                        success=result.returncode == 0
                    )
                    
                except Exception as e:
                    diagnostics.append(HCLDiagnostic(
                        level="error",
                        message=f"Failed to parse plan output: {str(e)}"
                    ))
            
            return plan, diagnostics
            
        except Exception as e:
            return None, [HCLDiagnostic(
                level="error",
                message=f"Terraform plan failed: {str(e)}"
            )]
    
    def terraform_format(self, directory: str) -> Tuple[bool, List[HCLDiagnostic]]:
        """Format Terraform files"""
        if not self.terraform_available:
            return False, [HCLDiagnostic(
                level="error",
                message="Terraform CLI not available"
            )]
        
        try:
            result = subprocess.run(
                [self.config.terraform_path, "fmt", "-recursive"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            diagnostics = self._parse_terraform_output(result.stdout, result.stderr)
            return result.returncode == 0, diagnostics
            
        except Exception as e:
            return False, [HCLDiagnostic(
                level="error",
                message=f"Terraform format failed: {str(e)}"
            )]
    
    def hcl_to_runa_convert(self, hcl_config: HCLConfiguration) -> Any:
        """Convert HCL configuration to Runa AST"""
        converter = HCLToRunaConverter()
        return converter.convert(hcl_config)
    
    def runa_to_hcl_convert(self, runa_module: Any) -> HCLConfiguration:
        """Convert Runa AST to HCL configuration"""
        converter = RunaToHCLConverter()
        return converter.convert(runa_module)
    
    def round_trip_verify(self, file_path: str) -> Tuple[bool, List[HCLDiagnostic]]:
        """Verify round-trip conversion HCL → Runa → HCL"""
        diagnostics = []
        
        try:
            # Parse original HCL
            original_ast, parse_diagnostics = self.parse_hcl_file(file_path)
            diagnostics.extend(parse_diagnostics)
            
            if not original_ast:
                return False, diagnostics
            
            # Convert to Runa
            runa_ast = self.hcl_to_runa_convert(original_ast)
            
            # Convert back to HCL
            converted_ast = self.runa_to_hcl_convert(runa_ast)
            
            # Generate both versions and compare
            generator = HCLCodeGenerator()
            original_code = generator.generate(original_ast)
            converted_code = generator.generate(converted_ast)
            
            # Normalize and compare
            if self._normalize_hcl_code(original_code) == self._normalize_hcl_code(converted_code):
                diagnostics.append(HCLDiagnostic(
                    level="info",
                    message="Round-trip conversion successful",
                    file=file_path
                ))
                return True, diagnostics
            else:
                diagnostics.append(HCLDiagnostic(
                    level="warning",
                    message="Round-trip conversion produced different output",
                    file=file_path,
                    suggestion="Check for semantic equivalence"
                ))
                return False, diagnostics
                
        except Exception as e:
            diagnostics.append(HCLDiagnostic(
                level="error",
                message=f"Round-trip verification failed: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def analyze_configuration(self, directory: str) -> Dict[str, Any]:
        """Analyze HCL configuration for insights"""
        analysis = {
            "files": [],
            "blocks": {"total": 0, "by_type": {}},
            "resources": [],
            "data_sources": [],
            "variables": [],
            "outputs": [],
            "providers": [],
            "modules": [],
            "complexity_score": 0,
            "recommendations": []
        }
        
        configs, diagnostics = self.parse_hcl_directory(directory)
        
        for config in configs:
            for item in config.body:
                if isinstance(item, HCLBlock):
                    analysis["blocks"]["total"] += 1
                    block_type = item.type
                    analysis["blocks"]["by_type"][block_type] = \
                        analysis["blocks"]["by_type"].get(block_type, 0) + 1
                    
                    if isinstance(item, HCLResource):
                        analysis["resources"].append({
                            "type": item.type,
                            "name": item.name,
                            "provider": item.provider,
                            "has_count": item.count is not None,
                            "has_for_each": item.for_each is not None
                        })
                    elif isinstance(item, HCLDataSource):
                        analysis["data_sources"].append({
                            "type": item.type,
                            "name": item.name
                        })
                    elif isinstance(item, HCLVariable):
                        analysis["variables"].append({
                            "name": item.name,
                            "has_default": item.default is not None,
                            "sensitive": item.sensitive
                        })
                    elif isinstance(item, HCLOutput):
                        analysis["outputs"].append({
                            "name": item.name,
                            "sensitive": item.sensitive
                        })
                    elif isinstance(item, HCLProvider):
                        analysis["providers"].append({
                            "name": item.name,
                            "alias": item.alias
                        })
                    elif isinstance(item, HCLModule):
                        analysis["modules"].append({
                            "name": item.name,
                            "source": item.source
                        })
        
        # Calculate complexity score
        analysis["complexity_score"] = self._calculate_complexity_score(analysis)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def lint_configuration(self, directory: str) -> List[HCLDiagnostic]:
        """Lint HCL configuration for best practices"""
        diagnostics = []
        configs, parse_diagnostics = self.parse_hcl_directory(directory)
        diagnostics.extend(parse_diagnostics)
        
        for config in configs:
            diagnostics.extend(self._lint_configuration(config))
        
        return diagnostics
    
    # Private helper methods
    def _check_terraform_availability(self) -> bool:
        """Check if Terraform CLI is available"""
        try:
            result = subprocess.run(
                [self.config.terraform_path, "version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _validate_ast(self, ast: HCLConfiguration, file_path: Optional[str] = None) -> List[HCLDiagnostic]:
        """Validate HCL AST"""
        diagnostics = []
        
        if self.config.validation_level in [HCLValidationLevel.SYNTAX, HCLValidationLevel.SEMANTIC]:
            diagnostics.extend(self._validate_syntax(ast, file_path))
        
        if self.config.validation_level in [HCLValidationLevel.SEMANTIC, HCLValidationLevel.TERRAFORM]:
            diagnostics.extend(self._validate_semantics(ast, file_path))
        
        if self.config.validation_level in [HCLValidationLevel.TERRAFORM, HCLValidationLevel.COMPLETE]:
            diagnostics.extend(self._validate_terraform(ast, file_path))
        
        return diagnostics
    
    def _validate_syntax(self, ast: HCLConfiguration, file_path: Optional[str] = None) -> List[HCLDiagnostic]:
        """Basic syntax validation"""
        diagnostics = []
        
        for item in ast.body:
            if isinstance(item, HCLBlock):
                # Check for required labels
                if item.type == "resource" and len(item.labels) != 2:
                    diagnostics.append(HCLDiagnostic(
                        level="error",
                        message="Resource blocks require exactly 2 labels (type and name)",
                        file=file_path
                    ))
                elif item.type == "variable" and len(item.labels) != 1:
                    diagnostics.append(HCLDiagnostic(
                        level="error",
                        message="Variable blocks require exactly 1 label (name)",
                        file=file_path
                    ))
        
        return diagnostics
    
    def _validate_semantics(self, ast: HCLConfiguration, file_path: Optional[str] = None) -> List[HCLDiagnostic]:
        """Semantic validation"""
        diagnostics = []
        
        # Track variable definitions and references
        defined_variables = set()
        referenced_variables = set()
        
        for item in ast.body:
            if isinstance(item, HCLVariable):
                defined_variables.add(item.name)
        
        # Find variable references (simplified)
        for item in ast.body:
            if isinstance(item, HCLBlock):
                self._find_variable_references(item, referenced_variables)
        
        # Check for undefined variables
        for var in referenced_variables:
            if var not in defined_variables:
                diagnostics.append(HCLDiagnostic(
                    level="warning",
                    message=f"Reference to undefined variable: {var}",
                    file=file_path
                ))
        
        return diagnostics
    
    def _validate_terraform(self, ast: HCLConfiguration, file_path: Optional[str] = None) -> List[HCLDiagnostic]:
        """Terraform-specific validation"""
        diagnostics = []
        
        # Check for required provider configurations
        used_providers = set()
        configured_providers = set()
        
        for item in ast.body:
            if isinstance(item, HCLResource):
                provider = item.type.split('_')[0]
                used_providers.add(provider)
            elif isinstance(item, HCLProvider):
                configured_providers.add(item.name)
        
        for provider in used_providers:
            if provider not in configured_providers:
                diagnostics.append(HCLDiagnostic(
                    level="warning",
                    message=f"Provider '{provider}' used but not configured",
                    file=file_path,
                    suggestion=f"Add a provider \"{provider}\" block"
                ))
        
        return diagnostics
    
    def _find_variable_references(self, node: HCLNode, references: set) -> None:
        """Find variable references in AST (simplified)"""
        if isinstance(node, HCLIdentifier) and node.name.startswith('var.'):
            var_name = node.name[4:]  # Remove 'var.' prefix
            references.add(var_name)
        
        # Recursively check children
        for child in getattr(node, 'children', []):
            self._find_variable_references(child, references)
    
    def _parse_terraform_output(self, stdout: str, stderr: str) -> List[HCLDiagnostic]:
        """Parse Terraform command output into diagnostics"""
        diagnostics = []
        
        # Parse stderr for errors
        if stderr:
            for line in stderr.split('\n'):
                if line.strip():
                    diagnostics.append(HCLDiagnostic(
                        level="error",
                        message=line.strip()
                    ))
        
        # Parse stdout for info
        if stdout:
            for line in stdout.split('\n'):
                if line.strip():
                    diagnostics.append(HCLDiagnostic(
                        level="info",
                        message=line.strip()
                    ))
        
        return diagnostics
    
    def _normalize_hcl_code(self, code: str) -> str:
        """Normalize HCL code for comparison"""
        # Remove comments and normalize whitespace
        lines = []
        for line in code.split('\n'):
            line = line.split('#')[0].strip()  # Remove comments
            if line:
                lines.append(line)
        
        return '\n'.join(lines)
    
    def _calculate_complexity_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate configuration complexity score"""
        score = 0
        score += len(analysis["resources"]) * 2
        score += len(analysis["data_sources"]) * 1
        score += len(analysis["modules"]) * 3
        score += len(analysis["variables"])
        score += len(analysis["outputs"])
        
        # Add complexity for dynamic blocks
        for resource in analysis["resources"]:
            if resource["has_count"] or resource["has_for_each"]:
                score += 2
        
        return score
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate configuration recommendations"""
        recommendations = []
        
        if len(analysis["variables"]) == 0:
            recommendations.append("Consider using variables for configurable values")
        
        if len(analysis["outputs"]) == 0 and len(analysis["resources"]) > 0:
            recommendations.append("Consider adding outputs for important resource attributes")
        
        if analysis["complexity_score"] > 50:
            recommendations.append("Configuration complexity is high - consider splitting into modules")
        
        provider_count = len(set(r["type"].split('_')[0] for r in analysis["resources"]))
        if provider_count > 3:
            recommendations.append("Multiple providers detected - ensure proper provider configuration")
        
        return recommendations
    
    def _lint_configuration(self, config: HCLConfiguration) -> List[HCLDiagnostic]:
        """Lint configuration for best practices"""
        diagnostics = []
        
        for item in config.body:
            if isinstance(item, HCLVariable):
                if not item.description:
                    diagnostics.append(HCLDiagnostic(
                        level="warning",
                        message=f"Variable '{item.name}' missing description",
                        suggestion="Add description for documentation"
                    ))
            
            elif isinstance(item, HCLOutput):
                if not item.description:
                    diagnostics.append(HCLDiagnostic(
                        level="warning",
                        message=f"Output '{item.name}' missing description",
                        suggestion="Add description for documentation"
                    ))
            
            elif isinstance(item, HCLResource):
                # Check for hardcoded values
                for body_item in item.body:
                    if isinstance(body_item, HCLAttribute):
                        if isinstance(body_item.value, HCLString):
                            # Check for potential secrets
                            if any(keyword in body_item.name.lower() 
                                  for keyword in ['password', 'secret', 'key', 'token']):
                                diagnostics.append(HCLDiagnostic(
                                    level="warning",
                                    message=f"Potential secret in resource '{item.name}' attribute '{body_item.name}'",
                                    suggestion="Consider using variables or external data sources"
                                ))
        
        return diagnostics


# Convenience functions
def parse_hcl_code(code: str, filename: Optional[str] = None) -> HCLConfiguration:
    """Parse HCL code string"""
    return parse_hcl(code, filename)


def generate_hcl_code(ast: HCLConfiguration, style: HCLFormatStyle = HCLFormatStyle.STANDARD) -> str:
    """Generate HCL code from AST"""
    return generate_hcl(ast, style)


def hcl_round_trip_verify(code: str) -> bool:
    """Verify HCL round-trip conversion"""
    toolchain = HCLToolchain()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tf', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        success, _ = toolchain.round_trip_verify(temp_file)
        return success
    finally:
        os.unlink(temp_file)


def hcl_to_runa_translate(hcl_config: HCLConfiguration) -> Any:
    """Translate HCL to Runa AST"""
    toolchain = HCLToolchain()
    return toolchain.hcl_to_runa_convert(hcl_config)


def runa_to_hcl_translate(runa_module: Any) -> HCLConfiguration:
    """Translate Runa AST to HCL"""
    toolchain = HCLToolchain()
    return toolchain.runa_to_hcl_convert(runa_module) 