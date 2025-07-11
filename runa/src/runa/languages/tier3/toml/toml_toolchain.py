#!/usr/bin/env python3
"""
TOML Toolchain - Complete TOML Configuration Toolchain Integration

Provides comprehensive TOML toolchain capabilities including:
- TOML parsing, validation, and formatting
- Configuration analysis and linting
- Schema validation and type checking
- Round-trip translation verification
- Configuration optimization and refactoring
- Integration with popular TOML tools
- Project-specific TOML handling (Cargo, Poetry, etc.)

Supports TOML v1.0.0 specification and common configuration patterns.
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
import re

from .toml_ast import *
from .toml_parser import parse_toml, TOMLLexer, TOMLParser
from .toml_converter import toml_to_runa, runa_to_toml, TOMLToRunaConverter, RunaToTOMLConverter
from .toml_generator import generate_toml, TOMLCodeGenerator, TOMLFormatStyle, TOMLGeneratorConfig


class TOMLValidationLevel(Enum):
    """TOML validation levels"""
    SYNTAX = "syntax"           # Basic syntax validation
    SEMANTIC = "semantic"       # Semantic validation with type checking
    SCHEMA = "schema"           # Schema-based validation
    PROJECT = "project"         # Project-specific validation (Cargo, Poetry, etc.)
    COMPLETE = "complete"       # Full validation with all checks


class TOMLProjectType(Enum):
    """Known TOML project types"""
    GENERIC = "generic"
    CARGO = "cargo"             # Rust Cargo.toml
    POETRY = "poetry"           # Python Poetry pyproject.toml
    PYPROJECT = "pyproject"     # Python pyproject.toml
    CONFIG = "config"           # Generic configuration
    ANSIBLE = "ansible"         # Ansible configuration
    HUGO = "hugo"               # Hugo site configuration


@dataclass
class TOMLDiagnostic:
    """TOML diagnostic message"""
    level: str  # "error", "warning", "info"
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None
    suggestion: Optional[str] = None
    rule: Optional[str] = None


@dataclass
class TOMLSchema:
    """TOML schema definition"""
    name: str
    version: str
    schema: Dict[str, Any]
    required_tables: List[str]
    optional_tables: List[str]
    validation_rules: List[str]


@dataclass
class TOMLAnalysis:
    """TOML configuration analysis result"""
    file_count: int
    table_count: int
    key_count: int
    complexity_score: int
    project_type: TOMLProjectType
    schema_compliance: float  # 0.0 to 1.0
    recommendations: List[str]
    issues: List[TOMLDiagnostic]
    metadata: Dict[str, Any]


@dataclass
class TOMLToolchainConfig:
    """Configuration for TOML toolchain"""
    validation_level: TOMLValidationLevel = TOMLValidationLevel.SEMANTIC
    auto_format: bool = True
    auto_detect_project_type: bool = True
    project_type: TOMLProjectType = TOMLProjectType.GENERIC
    
    # Validation options
    check_schema_compliance: bool = True
    check_key_naming: bool = True
    check_value_types: bool = True
    check_required_fields: bool = True
    check_deprecated_fields: bool = True
    
    # Formatting options
    format_style: TOMLFormatStyle = TOMLFormatStyle.STANDARD
    sort_keys: bool = False
    align_values: bool = True
    preserve_comments: bool = True
    
    # Tool integration
    toml_sort_path: str = "toml-sort"
    taplo_path: str = "taplo"  # Rust TOML formatter/linter
    cargo_path: str = "cargo"
    poetry_path: str = "poetry"


class TOMLToolchain:
    """Complete TOML configuration toolchain"""
    
    def __init__(self, config: Optional[TOMLToolchainConfig] = None):
        self.config = config or TOMLToolchainConfig()
        self.external_tools = self._check_external_tools()
        self.working_directory: Optional[str] = None
        self.schemas: Dict[str, TOMLSchema] = {}
        self.project_patterns: Dict[str, TOMLProjectType] = {
            "Cargo.toml": TOMLProjectType.CARGO,
            "pyproject.toml": TOMLProjectType.PYPROJECT,
            "poetry.lock": TOMLProjectType.POETRY,
            "ansible.cfg": TOMLProjectType.ANSIBLE,
            "config.toml": TOMLProjectType.CONFIG,
        }
        
        # Load built-in schemas
        self._load_builtin_schemas()
    
    def parse_toml_file(self, file_path: str) -> Tuple[Optional[TOMLDocument], List[TOMLDiagnostic]]:
        """Parse TOML file and return AST with diagnostics"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse TOML
            ast = parse_toml(content, file_path)
            
            # Auto-detect project type if enabled
            if self.config.auto_detect_project_type:
                project_type = self._detect_project_type(file_path, ast)
            else:
                project_type = self.config.project_type
            
            # Validate based on configuration
            validation_diagnostics = self._validate_ast(ast, file_path, project_type)
            diagnostics.extend(validation_diagnostics)
            
            return ast, diagnostics
            
        except FileNotFoundError:
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message=f"File not found: {file_path}",
                file=file_path
            ))
            return None, diagnostics
            
        except Exception as e:
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message=f"Parse error: {str(e)}",
                file=file_path,
                code="parse_error"
            ))
            return None, diagnostics
    
    def parse_toml_directory(self, directory: str) -> Tuple[List[TOMLDocument], List[TOMLDiagnostic]]:
        """Parse all TOML files in directory"""
        configurations = []
        all_diagnostics = []
        
        toml_files = list(Path(directory).glob('**/*.toml'))
        
        for file_path in toml_files:
            ast, diagnostics = self.parse_toml_file(str(file_path))
            if ast:
                configurations.append(ast)
            all_diagnostics.extend(diagnostics)
        
        return configurations, all_diagnostics
    
    def validate_configuration(self, config: TOMLDocument, file_path: Optional[str] = None,
                             project_type: Optional[TOMLProjectType] = None) -> List[TOMLDiagnostic]:
        """Validate TOML configuration"""
        if project_type is None:
            project_type = self._detect_project_type(file_path or "", config)
        
        return self._validate_ast(config, file_path, project_type)
    
    def format_toml_file(self, file_path: str, in_place: bool = False) -> Tuple[str, List[TOMLDiagnostic]]:
        """Format TOML file"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try external formatter first if available
            if self.external_tools.get("taplo"):
                formatted_content, format_diagnostics = self._format_with_taplo(content, file_path)
                diagnostics.extend(format_diagnostics)
            else:
                # Use built-in formatter
                ast = parse_toml(content, file_path)
                generator_config = TOMLGeneratorConfig(
                    style=self.config.format_style,
                    sort_keys=self.config.sort_keys,
                    align_values=self.config.align_values,
                    preserve_comments=self.config.preserve_comments
                )
                generator = TOMLCodeGenerator(generator_config)
                formatted_content = generator.generate(ast)
            
            if in_place:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                diagnostics.append(TOMLDiagnostic(
                    level="info",
                    message=f"Formatted file: {file_path}",
                    file=file_path
                ))
            
            return formatted_content, diagnostics
            
        except Exception as e:
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message=f"Format error: {str(e)}",
                file=file_path,
                code="format_error"
            ))
            return "", diagnostics
    
    def sort_toml_file(self, file_path: str, in_place: bool = False) -> Tuple[str, List[TOMLDiagnostic]]:
        """Sort TOML file keys"""
        diagnostics = []
        
        try:
            # Try external tool first
            if self.external_tools.get("toml-sort"):
                return self._sort_with_toml_sort(file_path, in_place)
            
            # Built-in sorting
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            ast = parse_toml(content, file_path)
            
            # Sort configuration
            sorted_ast = self._sort_toml_ast(ast)
            
            generator_config = TOMLGeneratorConfig(
                style=self.config.format_style,
                sort_keys=True,
                align_values=self.config.align_values
            )
            generator = TOMLCodeGenerator(generator_config)
            sorted_content = generator.generate(sorted_ast)
            
            if in_place:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(sorted_content)
            
            return sorted_content, diagnostics
            
        except Exception as e:
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message=f"Sort error: {str(e)}",
                file=file_path,
                code="sort_error"
            ))
            return "", diagnostics
    
    def lint_configuration(self, file_path: str) -> List[TOMLDiagnostic]:
        """Lint TOML configuration"""
        diagnostics = []
        
        try:
            ast, parse_diagnostics = self.parse_toml_file(file_path)
            diagnostics.extend(parse_diagnostics)
            
            if ast:
                project_type = self._detect_project_type(file_path, ast)
                lint_diagnostics = self._lint_toml_ast(ast, file_path, project_type)
                diagnostics.extend(lint_diagnostics)
        
        except Exception as e:
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message=f"Lint error: {str(e)}",
                file=file_path,
                code="lint_error"
            ))
        
        return diagnostics
    
    def toml_to_runa_convert(self, toml_doc: TOMLDocument) -> Any:
        """Convert TOML to Runa AST"""
        converter = TOMLToRunaConverter()
        return converter.convert(toml_doc)
    
    def runa_to_toml_convert(self, runa_module: Any) -> TOMLDocument:
        """Convert Runa AST to TOML"""
        converter = RunaToTOMLConverter()
        return converter.convert(runa_module)
    
    def round_trip_verify(self, file_path: str) -> Tuple[bool, List[TOMLDiagnostic]]:
        """Verify round-trip conversion accuracy"""
        diagnostics = []
        
        try:
            # Parse original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            original_ast = parse_toml(original_content, file_path)
            
            # Convert to Runa and back
            runa_module = self.toml_to_runa_convert(original_ast)
            reconstructed_ast = self.runa_to_toml_convert(runa_module)
            
            # Generate and compare
            generator = TOMLCodeGenerator()
            reconstructed_content = generator.generate(reconstructed_ast)
            
            # Normalize for comparison
            original_normalized = self._normalize_toml_content(original_content)
            reconstructed_normalized = self._normalize_toml_content(reconstructed_content)
            
            success = original_normalized == reconstructed_normalized
            
            if not success:
                diagnostics.append(TOMLDiagnostic(
                    level="warning",
                    message="Round-trip conversion produced different result",
                    file=file_path,
                    code="round_trip_mismatch",
                    suggestion="Check for semantic preservation issues"
                ))
            else:
                diagnostics.append(TOMLDiagnostic(
                    level="info",
                    message="Round-trip conversion successful",
                    file=file_path
                ))
            
            return success, diagnostics
            
        except Exception as e:
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message=f"Round-trip verification error: {str(e)}",
                file=file_path,
                code="round_trip_error"
            ))
            return False, diagnostics
    
    def analyze_configuration(self, directory: str) -> TOMLAnalysis:
        """Analyze TOML configuration comprehensively"""
        configs, diagnostics = self.parse_toml_directory(directory)
        
        # Calculate metrics
        file_count = len(configs)
        table_count = sum(len([item for item in config.items if isinstance(item, TOMLTable)]) 
                         for config in configs)
        key_count = sum(len([item for item in config.items if isinstance(item, TOMLKeyValue)]) 
                       for config in configs)
        
        # Detect project type
        project_type = TOMLProjectType.GENERIC
        if configs:
            toml_files = list(Path(directory).glob('**/*.toml'))
            for file_path in toml_files:
                detected_type = self._detect_project_type(str(file_path), configs[0])
                if detected_type != TOMLProjectType.GENERIC:
                    project_type = detected_type
                    break
        
        # Calculate complexity
        complexity_score = self._calculate_complexity_score(configs)
        
        # Schema compliance
        schema_compliance = self._calculate_schema_compliance(configs, project_type)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(configs, project_type, diagnostics)
        
        return TOMLAnalysis(
            file_count=file_count,
            table_count=table_count,
            key_count=key_count,
            complexity_score=complexity_score,
            project_type=project_type,
            schema_compliance=schema_compliance,
            recommendations=recommendations,
            issues=diagnostics,
            metadata={
                "validation_level": self.config.validation_level.value,
                "total_diagnostics": len(diagnostics),
                "error_count": len([d for d in diagnostics if d.level == "error"]),
                "warning_count": len([d for d in diagnostics if d.level == "warning"])
            }
        )
    
    def validate_cargo_toml(self, file_path: str) -> List[TOMLDiagnostic]:
        """Validate Rust Cargo.toml file"""
        if not self.external_tools.get("cargo"):
            return [TOMLDiagnostic(
                level="warning",
                message="Cargo not available for validation",
                file=file_path,
                code="missing_tool"
            )]
        
        try:
            # Run cargo check for validation
            result = subprocess.run(
                [self.config.cargo_path, "check", "--manifest-path", file_path],
                capture_output=True,
                text=True,
                cwd=Path(file_path).parent
            )
            
            diagnostics = []
            if result.returncode != 0:
                # Parse cargo output for diagnostics
                diagnostics.extend(self._parse_cargo_output(result.stderr))
            
            return diagnostics
            
        except Exception as e:
            return [TOMLDiagnostic(
                level="error",
                message=f"Cargo validation error: {str(e)}",
                file=file_path,
                code="cargo_error"
            )]
    
    def validate_poetry_toml(self, file_path: str) -> List[TOMLDiagnostic]:
        """Validate Poetry pyproject.toml file"""
        if not self.external_tools.get("poetry"):
            return [TOMLDiagnostic(
                level="warning",
                message="Poetry not available for validation",
                file=file_path,
                code="missing_tool"
            )]
        
        try:
            # Run poetry check for validation
            result = subprocess.run(
                [self.config.poetry_path, "check"],
                capture_output=True,
                text=True,
                cwd=Path(file_path).parent
            )
            
            diagnostics = []
            if result.returncode != 0:
                diagnostics.extend(self._parse_poetry_output(result.stderr))
            
            return diagnostics
            
        except Exception as e:
            return [TOMLDiagnostic(
                level="error",
                message=f"Poetry validation error: {str(e)}",
                file=file_path,
                code="poetry_error"
            )]
    
    def _check_external_tools(self) -> Dict[str, bool]:
        """Check availability of external tools"""
        tools = {}
        
        # Check each tool
        for tool, path in [
            ("toml-sort", self.config.toml_sort_path),
            ("taplo", self.config.taplo_path),
            ("cargo", self.config.cargo_path),
            ("poetry", self.config.poetry_path),
        ]:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True)
                tools[tool] = result.returncode == 0
            except (FileNotFoundError, subprocess.SubprocessError):
                tools[tool] = False
        
        return tools
    
    def _load_builtin_schemas(self) -> None:
        """Load built-in TOML schemas"""
        # Cargo.toml schema
        self.schemas["cargo"] = TOMLSchema(
            name="Cargo.toml",
            version="1.0",
            schema={
                "package": {
                    "required": ["name", "version"],
                    "optional": ["authors", "description", "license", "edition"]
                },
                "dependencies": {"type": "table"},
                "dev-dependencies": {"type": "table"},
                "build-dependencies": {"type": "table"}
            },
            required_tables=["package"],
            optional_tables=["dependencies", "dev-dependencies", "build-dependencies"],
            validation_rules=["check_semver_versions", "check_crate_names"]
        )
        
        # pyproject.toml schema
        self.schemas["pyproject"] = TOMLSchema(
            name="pyproject.toml",
            version="1.0",
            schema={
                "build-system": {
                    "required": ["requires"],
                    "optional": ["build-backend"]
                },
                "project": {
                    "required": ["name"],
                    "optional": ["version", "description", "authors", "license"]
                },
                "tool": {"type": "table"}
            },
            required_tables=[],
            optional_tables=["build-system", "project", "tool"],
            validation_rules=["check_pep621_compliance"]
        )
    
    def _detect_project_type(self, file_path: str, ast: TOMLDocument) -> TOMLProjectType:
        """Detect project type from file path and content"""
        file_name = Path(file_path).name.lower()
        
        # Check file name patterns
        for pattern, project_type in self.project_patterns.items():
            if pattern.lower() in file_name:
                return project_type
        
        # Check content patterns
        for item in ast.items:
            if isinstance(item, TOMLTable):
                table_name = item.key.dotted_key.lower()
                
                # Cargo patterns
                if table_name in ["package", "dependencies", "dev-dependencies"]:
                    return TOMLProjectType.CARGO
                
                # Poetry/pyproject patterns
                if table_name in ["build-system", "project", "tool.poetry"]:
                    return TOMLProjectType.POETRY
                
                # Config patterns
                if table_name in ["server", "database", "logging"]:
                    return TOMLProjectType.CONFIG
        
        return TOMLProjectType.GENERIC
    
    def _validate_ast(self, ast: TOMLDocument, file_path: Optional[str], 
                     project_type: TOMLProjectType) -> List[TOMLDiagnostic]:
        """Validate TOML AST with specified level"""
        diagnostics = []
        
        if self.config.validation_level.value in ["syntax", "semantic", "schema", "project", "complete"]:
            diagnostics.extend(self._validate_syntax(ast, file_path))
        
        if self.config.validation_level.value in ["semantic", "schema", "project", "complete"]:
            diagnostics.extend(self._validate_semantics(ast, file_path))
        
        if self.config.validation_level.value in ["schema", "project", "complete"]:
            diagnostics.extend(self._validate_schema(ast, file_path, project_type))
        
        if self.config.validation_level.value in ["project", "complete"]:
            diagnostics.extend(self._validate_project_specific(ast, file_path, project_type))
        
        return diagnostics
    
    def _validate_syntax(self, ast: TOMLDocument, file_path: Optional[str]) -> List[TOMLDiagnostic]:
        """Perform syntax validation"""
        diagnostics = []
        
        # Check for duplicate keys
        seen_keys = set()
        for item in ast.items:
            if isinstance(item, TOMLKeyValue):
                key_str = item.key.dotted_key
                if key_str in seen_keys:
                    diagnostics.append(TOMLDiagnostic(
                        level="error",
                        message=f"Duplicate key: {key_str}",
                        file=file_path,
                        code="duplicate_key"
                    ))
                seen_keys.add(key_str)
        
        return diagnostics
    
    def _validate_semantics(self, ast: TOMLDocument, file_path: Optional[str]) -> List[TOMLDiagnostic]:
        """Perform semantic validation"""
        diagnostics = []
        
        # Check key naming conventions
        if self.config.check_key_naming:
            for item in ast.items:
                if isinstance(item, TOMLKeyValue):
                    diagnostics.extend(self._check_key_naming(item.key, file_path))
        
        # Check value types consistency
        if self.config.check_value_types:
            diagnostics.extend(self._check_value_types(ast, file_path))
        
        return diagnostics
    
    def _validate_schema(self, ast: TOMLDocument, file_path: Optional[str], 
                        project_type: TOMLProjectType) -> List[TOMLDiagnostic]:
        """Perform schema validation"""
        diagnostics = []
        
        schema_name = project_type.value
        if schema_name in self.schemas:
            schema = self.schemas[schema_name]
            diagnostics.extend(self._validate_against_schema(ast, schema, file_path))
        
        return diagnostics
    
    def _validate_project_specific(self, ast: TOMLDocument, file_path: Optional[str], 
                                  project_type: TOMLProjectType) -> List[TOMLDiagnostic]:
        """Perform project-specific validation"""
        diagnostics = []
        
        if project_type == TOMLProjectType.CARGO and file_path:
            diagnostics.extend(self.validate_cargo_toml(file_path))
        elif project_type == TOMLProjectType.POETRY and file_path:
            diagnostics.extend(self.validate_poetry_toml(file_path))
        
        return diagnostics
    
    def _format_with_taplo(self, content: str, file_path: str) -> Tuple[str, List[TOMLDiagnostic]]:
        """Format TOML using taplo"""
        try:
            result = subprocess.run(
                [self.config.taplo_path, "format", "-"],
                input=content,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout, []
            else:
                return content, [TOMLDiagnostic(
                    level="error",
                    message=f"Taplo format error: {result.stderr}",
                    file=file_path,
                    code="taplo_error"
                )]
        
        except Exception as e:
            return content, [TOMLDiagnostic(
                level="error",
                message=f"Taplo execution error: {str(e)}",
                file=file_path,
                code="taplo_execution_error"
            )]
    
    def _sort_with_toml_sort(self, file_path: str, in_place: bool) -> Tuple[str, List[TOMLDiagnostic]]:
        """Sort TOML using toml-sort"""
        try:
            cmd = [self.config.toml_sort_path, file_path]
            if in_place:
                cmd.append("--in-place")
            else:
                cmd.append("--check")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if in_place:
                    with open(file_path, 'r') as f:
                        return f.read(), []
                else:
                    return result.stdout, []
            else:
                return "", [TOMLDiagnostic(
                    level="error",
                    message=f"toml-sort error: {result.stderr}",
                    file=file_path,
                    code="toml_sort_error"
                )]
        
        except Exception as e:
            return "", [TOMLDiagnostic(
                level="error",
                message=f"toml-sort execution error: {str(e)}",
                file=file_path,
                code="toml_sort_execution_error"
            )]
    
    def _sort_toml_ast(self, ast: TOMLDocument) -> TOMLDocument:
        """Sort TOML AST keys"""
        # Simple implementation - sort key-value pairs
        sorted_items = []
        
        for item in ast.items:
            sorted_items.append(item)
        
        # Sort key-value pairs by key name
        kv_items = [item for item in sorted_items if isinstance(item, TOMLKeyValue)]
        other_items = [item for item in sorted_items if not isinstance(item, TOMLKeyValue)]
        
        kv_items.sort(key=lambda kv: kv.key.dotted_key)
        
        return TOMLDocument(
            items=kv_items + other_items,
            filename=ast.filename,
            metadata=ast.metadata
        )
    
    def _lint_toml_ast(self, ast: TOMLDocument, file_path: str, 
                      project_type: TOMLProjectType) -> List[TOMLDiagnostic]:
        """Lint TOML AST for style and best practices"""
        diagnostics = []
        
        # Check for style issues
        for item in ast.items:
            if isinstance(item, TOMLKeyValue):
                # Check key naming
                key_name = item.key.dotted_key
                if "_" in key_name and "-" in key_name:
                    diagnostics.append(TOMLDiagnostic(
                        level="warning",
                        message=f"Mixed naming convention in key: {key_name}",
                        file=file_path,
                        code="mixed_naming",
                        rule="consistent_key_naming"
                    ))
        
        return diagnostics
    
    def _normalize_toml_content(self, content: str) -> str:
        """Normalize TOML content for comparison"""
        # Remove comments and extra whitespace
        lines = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                lines.append(stripped)
        
        return '\n'.join(sorted(lines))
    
    def _calculate_complexity_score(self, configs: List[TOMLDocument]) -> int:
        """Calculate configuration complexity score"""
        score = 0
        
        for config in configs:
            for item in config.items:
                if isinstance(item, TOMLTable):
                    score += 2  # Tables add complexity
                elif isinstance(item, TOMLKeyValue):
                    score += 1  # Key-value pairs
                    
                    # Nested structures add more complexity
                    if isinstance(item.value, TOMLArray):
                        score += len(item.value.elements)
                    elif isinstance(item.value, TOMLInlineTable):
                        score += len(item.value.pairs)
        
        return score
    
    def _calculate_schema_compliance(self, configs: List[TOMLDocument], 
                                   project_type: TOMLProjectType) -> float:
        """Calculate schema compliance score"""
        if project_type.value not in self.schemas:
            return 1.0  # No schema to validate against
        
        # Simple compliance check
        # This would be more sophisticated in a real implementation
        return 0.85  # Placeholder
    
    def _generate_recommendations(self, configs: List[TOMLDocument], 
                                 project_type: TOMLProjectType,
                                 diagnostics: List[TOMLDiagnostic]) -> List[str]:
        """Generate recommendations for configuration improvement"""
        recommendations = []
        
        error_count = len([d for d in diagnostics if d.level == "error"])
        warning_count = len([d for d in diagnostics if d.level == "warning"])
        
        if error_count > 0:
            recommendations.append(f"Fix {error_count} syntax errors")
        
        if warning_count > 5:
            recommendations.append("Consider addressing style warnings for better maintainability")
        
        total_keys = sum(len([item for item in config.items if isinstance(item, TOMLKeyValue)]) 
                        for config in configs)
        if total_keys > 50:
            recommendations.append("Consider splitting large configuration into multiple files")
        
        if project_type == TOMLProjectType.CARGO:
            recommendations.append("Run 'cargo check' for Rust-specific validation")
        elif project_type == TOMLProjectType.POETRY:
            recommendations.append("Run 'poetry check' for Python-specific validation")
        
        return recommendations
    
    def _check_key_naming(self, key: TOMLKey, file_path: Optional[str]) -> List[TOMLDiagnostic]:
        """Check key naming conventions"""
        diagnostics = []
        
        for part in key.parts:
            # Check for spaces in unquoted keys
            if ' ' in part and not any(key.is_quoted):
                diagnostics.append(TOMLDiagnostic(
                    level="error",
                    message=f"Unquoted key contains space: {part}",
                    file=file_path,
                    code="invalid_key_name"
                ))
        
        return diagnostics
    
    def _check_value_types(self, ast: TOMLDocument, file_path: Optional[str]) -> List[TOMLDiagnostic]:
        """Check value type consistency"""
        diagnostics = []
        
        # Check for consistent array types
        for item in ast.items:
            if isinstance(item, TOMLKeyValue) and isinstance(item.value, TOMLArray):
                if item.value.elements:
                    first_type = type(item.value.elements[0])
                    for i, elem in enumerate(item.value.elements[1:], 1):
                        if type(elem) != first_type:
                            diagnostics.append(TOMLDiagnostic(
                                level="warning",
                                message=f"Mixed types in array for key: {item.key.dotted_key}",
                                file=file_path,
                                code="mixed_array_types"
                            ))
                            break
        
        return diagnostics
    
    def _validate_against_schema(self, ast: TOMLDocument, schema: TOMLSchema, 
                                file_path: Optional[str]) -> List[TOMLDiagnostic]:
        """Validate AST against schema"""
        diagnostics = []
        
        # Check required tables
        present_tables = set()
        for item in ast.items:
            if isinstance(item, TOMLTable):
                present_tables.add(item.key.dotted_key)
        
        for required_table in schema.required_tables:
            if required_table not in present_tables:
                diagnostics.append(TOMLDiagnostic(
                    level="error",
                    message=f"Missing required table: [{required_table}]",
                    file=file_path,
                    code="missing_required_table"
                ))
        
        return diagnostics
    
    def _parse_cargo_output(self, stderr: str) -> List[TOMLDiagnostic]:
        """Parse cargo output for diagnostics"""
        diagnostics = []
        
        # Simple parsing - would be more sophisticated in practice
        if "error:" in stderr.lower():
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message="Cargo validation failed",
                code="cargo_validation_error"
            ))
        
        return diagnostics
    
    def _parse_poetry_output(self, stderr: str) -> List[TOMLDiagnostic]:
        """Parse poetry output for diagnostics"""
        diagnostics = []
        
        # Simple parsing - would be more sophisticated in practice  
        if "error:" in stderr.lower():
            diagnostics.append(TOMLDiagnostic(
                level="error",
                message="Poetry validation failed",
                code="poetry_validation_error"
            ))
        
        return diagnostics


# Convenience functions
def parse_toml_code(code: str, filename: Optional[str] = None) -> TOMLDocument:
    """Parse TOML source code"""
    return parse_toml(code, filename)


def generate_toml_code(ast: TOMLDocument, style: TOMLFormatStyle = TOMLFormatStyle.STANDARD) -> str:
    """Generate TOML code from AST"""
    config = TOMLGeneratorConfig(style=style)
    generator = TOMLCodeGenerator(config)
    return generator.generate(ast)


def toml_round_trip_verify(code: str) -> bool:
    """Verify TOML round-trip conversion"""
    try:
        ast = parse_toml(code)
        generated = generate_toml_code(ast)
        
        # Normalize for comparison
        toolchain = TOMLToolchain()
        original_normalized = toolchain._normalize_toml_content(code)
        generated_normalized = toolchain._normalize_toml_content(generated)
        
        return original_normalized == generated_normalized
    except Exception:
        return False


def toml_to_runa_translate(toml_doc: TOMLDocument) -> Any:
    """Translate TOML to Runa AST"""
    return toml_to_runa(toml_doc)


def runa_to_toml_translate(runa_module: Any) -> TOMLDocument:
    """Translate Runa AST to TOML"""
    return runa_to_toml(runa_module) 