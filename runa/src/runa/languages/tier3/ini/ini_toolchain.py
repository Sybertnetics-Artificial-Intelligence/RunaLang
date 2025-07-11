#!/usr/bin/env python3
"""
INI Toolchain - Complete INI Configuration Toolchain Integration

Provides comprehensive INI toolchain capabilities including:
- INI parsing, validation, and formatting
- Configuration file type detection and optimization
- Schema validation for known INI formats
- Configuration analysis and linting
- Round-trip translation verification
- Integration with common tools (git config, systemd, etc.)
- Configuration migration and transformation
- Multi-format INI support (Windows, Git, systemd, etc.)

Supports standard INI, Windows INI, Git config, systemd units, and custom formats.
"""

import os
import json
import subprocess
import tempfile
import configparser
import shutil
from typing import List, Dict, Optional, Any, Union, Tuple, Set
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
import re

from .ini_ast import *
from .ini_parser import INIParser, INILexer
from .ini_converter import ini_to_runa, runa_to_ini, INIToRunaConverter, RunaToINIConverter
from .ini_generator import generate_ini, INICodeGenerator, INIFormatStyle, INIGeneratorConfig


class INIValidationLevel(Enum):
    """INI validation levels"""
    SYNTAX = "syntax"           # Basic syntax validation
    SEMANTIC = "semantic"       # Semantic validation with type checking
    SCHEMA = "schema"           # Schema-based validation for known formats
    COMPLETE = "complete"       # Full validation with external tool integration


class INIFormatType(Enum):
    """INI format types for tool integration"""
    STANDARD = "standard"       # Standard INI format
    WINDOWS = "windows"         # Windows INI/registry format
    GIT_CONFIG = "git"         # Git configuration format
    SYSTEMD = "systemd"        # Systemd unit files
    PYTHON_CONFIG = "python"   # Python configparser format
    MYSQL_CONFIG = "mysql"     # MySQL configuration
    PHP_INI = "php"           # PHP configuration
    CUSTOM = "custom"          # Custom format


@dataclass
class INIDiagnostic:
    """INI diagnostic message"""
    level: str  # "error", "warning", "info"
    message: str
    file: Optional[str] = None
    section: Optional[str] = None
    key: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class INIAnalysisResult:
    """INI configuration analysis result"""
    format_type: INIFormatType
    sections: List[str]
    total_keys: int
    complexity_score: int
    recommendations: List[str]
    warnings: List[str]
    statistics: Dict[str, Any]


@dataclass
class INIToolchainConfig:
    """Configuration for INI toolchain"""
    validation_level: INIValidationLevel = INIValidationLevel.SEMANTIC
    auto_format: bool = True
    detect_format: bool = True
    case_sensitive: bool = True
    
    # Format detection options
    format_type: Optional[INIFormatType] = None
    allow_multiline: bool = True
    allow_interpolation: bool = True
    
    # Validation options
    check_references: bool = True
    check_types: bool = True
    check_duplicates: bool = True
    check_encoding: bool = True
    
    # Tool integration
    git_config_validation: bool = True
    systemd_validation: bool = True
    windows_compatibility: bool = False
    
    # Formatting options
    format_style: INIFormatStyle = INIFormatStyle.STANDARD
    sort_sections: bool = False
    sort_keys: bool = False
    align_values: bool = True


class INIToolchain:
    """Complete INI configuration toolchain"""
    
    def __init__(self, config: Optional[INIToolchainConfig] = None):
        self.config = config or INIToolchainConfig()
        self.git_available = self._check_git_availability()
        self.systemctl_available = self._check_systemctl_availability()
        self.working_directory: Optional[str] = None
        
        # Format schemas and patterns
        self.format_schemas = self._load_format_schemas()
        self.format_patterns = self._load_format_patterns()
        
        # Built-in validators
        self.reserved_sections = self._get_reserved_sections()
        self.known_keys = self._get_known_keys()
    
    def parse_ini_file(self, file_path: str) -> Tuple[Optional[INIConfiguration], List[INIDiagnostic]]:
        """Parse INI file and return AST with diagnostics"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Detect format if needed
            format_type = self._detect_format(content, file_path) if self.config.detect_format else None
            
            # Parse INI
            parser = INIParser()
            ast = parser.parse(content, file_path)
            
            # Validate based on configuration
            validation_diagnostics = self._validate_ast(ast, file_path, format_type)
            diagnostics.extend(validation_diagnostics)
            
            return ast, diagnostics
            
        except FileNotFoundError:
            diagnostics.append(INIDiagnostic(
                level="error",
                message=f"File not found: {file_path}",
                file=file_path
            ))
            return None, diagnostics
            
        except Exception as e:
            diagnostics.append(INIDiagnostic(
                level="error",
                message=f"Parse error: {str(e)}",
                file=file_path
            ))
            return None, diagnostics
    
    def parse_ini_directory(self, directory: str) -> Tuple[List[INIConfiguration], List[INIDiagnostic]]:
        """Parse all INI files in directory"""
        configurations = []
        all_diagnostics = []
        
        ini_patterns = ['*.ini', '*.cfg', '*.conf', '*.config', '.gitconfig', '*.service', '*.timer']
        ini_files = []
        
        for pattern in ini_patterns:
            ini_files.extend(Path(directory).glob(f'**/{pattern}'))
        
        for file_path in ini_files:
            ast, diagnostics = self.parse_ini_file(str(file_path))
            if ast:
                configurations.append(ast)
            all_diagnostics.extend(diagnostics)
        
        return configurations, all_diagnostics
    
    def validate_configuration(self, config: INIConfiguration, file_path: Optional[str] = None) -> List[INIDiagnostic]:
        """Validate INI configuration"""
        format_type = self._detect_format_from_ast(config) if self.config.detect_format else None
        return self._validate_ast(config, file_path, format_type)
    
    def format_ini_file(self, file_path: str, in_place: bool = False) -> Tuple[str, List[INIDiagnostic]]:
        """Format INI file"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse and format
            parser = INIParser()
            ast = parser.parse(content, file_path)
            
            # Determine format style
            format_style = self._determine_format_style(ast, file_path)
            
            generator_config = INIGeneratorConfig(
                style=format_style,
                sort_sections=self.config.sort_sections,
                sort_keys=self.config.sort_keys,
                align_values=self.config.align_values
            )
            
            generator = INICodeGenerator(generator_config)
            formatted_content = generator.generate(ast)
            
            if in_place:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                diagnostics.append(INIDiagnostic(
                    level="info",
                    message=f"Formatted file: {file_path}",
                    file=file_path
                ))
            
            return formatted_content, diagnostics
            
        except Exception as e:
            diagnostics.append(INIDiagnostic(
                level="error",
                message=f"Formatting error: {str(e)}",
                file=file_path
            ))
            return "", diagnostics
    
    def git_config_validate(self, file_path: str) -> Tuple[bool, List[INIDiagnostic]]:
        """Validate git config file using git config command"""
        diagnostics = []
        
        if not self.git_available:
            diagnostics.append(INIDiagnostic(
                level="warning",
                message="Git not available for validation",
                file=file_path
            ))
            return False, diagnostics
        
        try:
            # Use git config to validate
            result = subprocess.run(
                ['git', 'config', '--file', file_path, '--list'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                diagnostics.append(INIDiagnostic(
                    level="info",
                    message="Git config validation successful",
                    file=file_path
                ))
                return True, diagnostics
            else:
                diagnostics.append(INIDiagnostic(
                    level="error",
                    message=f"Git config validation failed: {result.stderr}",
                    file=file_path
                ))
                return False, diagnostics
                
        except subprocess.TimeoutExpired:
            diagnostics.append(INIDiagnostic(
                level="error",
                message="Git config validation timed out",
                file=file_path
            ))
            return False, diagnostics
        except Exception as e:
            diagnostics.append(INIDiagnostic(
                level="error",
                message=f"Git config validation error: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def systemd_validate(self, file_path: str) -> Tuple[bool, List[INIDiagnostic]]:
        """Validate systemd unit file"""
        diagnostics = []
        
        if not self.systemctl_available:
            diagnostics.append(INIDiagnostic(
                level="warning",
                message="systemctl not available for validation",
                file=file_path
            ))
            return False, diagnostics
        
        try:
            # Use systemd-analyze to validate unit file
            result = subprocess.run(
                ['systemd-analyze', 'verify', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                diagnostics.append(INIDiagnostic(
                    level="info",
                    message="Systemd unit validation successful",
                    file=file_path
                ))
                return True, diagnostics
            else:
                # Parse systemd errors
                for line in result.stderr.split('\n'):
                    if line.strip():
                        diagnostics.append(INIDiagnostic(
                            level="error",
                            message=line.strip(),
                            file=file_path
                        ))
                return False, diagnostics
                
        except subprocess.TimeoutExpired:
            diagnostics.append(INIDiagnostic(
                level="error",
                message="Systemd validation timed out",
                file=file_path
            ))
            return False, diagnostics
        except Exception as e:
            diagnostics.append(INIDiagnostic(
                level="error",
                message=f"Systemd validation error: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def ini_to_runa_convert(self, ini_config: INIConfiguration) -> Any:
        """Convert INI to Runa AST"""
        converter = INIToRunaConverter()
        return converter.convert(ini_config)
    
    def runa_to_ini_convert(self, runa_module: Any) -> INIConfiguration:
        """Convert Runa AST to INI"""
        converter = RunaToINIConverter()
        return converter.convert(runa_module)
    
    def round_trip_verify(self, file_path: str) -> Tuple[bool, List[INIDiagnostic]]:
        """Verify round-trip conversion preserves semantics"""
        diagnostics = []
        
        try:
            # Parse original
            original_ast, parse_diagnostics = self.parse_ini_file(file_path)
            diagnostics.extend(parse_diagnostics)
            
            if not original_ast:
                return False, diagnostics
            
            # Convert to Runa and back
            runa_ast = self.ini_to_runa_convert(original_ast)
            converted_ast = self.runa_to_ini_convert(runa_ast)
            
            # Generate both versions
            generator_config = INIGeneratorConfig(style=INIFormatStyle.STANDARD)
            generator = INICodeGenerator(generator_config)
            
            original_code = generator.generate(original_ast)
            converted_code = generator.generate(converted_ast)
            
            # Normalize for comparison
            original_normalized = self._normalize_ini_code(original_code)
            converted_normalized = self._normalize_ini_code(converted_code)
            
            if original_normalized == converted_normalized:
                diagnostics.append(INIDiagnostic(
                    level="info",
                    message="Round-trip verification successful",
                    file=file_path
                ))
                return True, diagnostics
            else:
                diagnostics.append(INIDiagnostic(
                    level="warning",
                    message="Round-trip verification shows differences",
                    file=file_path,
                    suggestion="Check for lossy conversion in complex constructs"
                ))
                return False, diagnostics
                
        except Exception as e:
            diagnostics.append(INIDiagnostic(
                level="error",
                message=f"Round-trip verification error: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def analyze_configuration(self, file_path: str) -> INIAnalysisResult:
        """Analyze INI configuration for insights and recommendations"""
        ast, _ = self.parse_ini_file(file_path)
        
        if not ast:
            return INIAnalysisResult(
                format_type=INIFormatType.STANDARD,
                sections=[],
                total_keys=0,
                complexity_score=0,
                recommendations=["File could not be parsed"],
                warnings=["Parse errors present"],
                statistics={}
            )
        
        # Analyze structure
        sections = [s.name for s in ast.sections]
        total_keys = sum(len([e for e in s.entries if isinstance(e, INIKeyValuePair)]) 
                        for s in ast.sections)
        
        # Detect format
        format_type = self._detect_format_from_ast(ast)
        
        # Calculate complexity
        complexity_score = self._calculate_complexity_score(ast)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(ast)
        
        # Collect warnings
        warnings = self._collect_warnings(ast)
        
        # Compile statistics
        statistics = {
            "sections": len(sections),
            "total_keys": total_keys,
            "global_keys": len([e for e in ast.global_entries if isinstance(e, INIKeyValuePair)]),
            "comments": sum(len([e for e in s.entries if isinstance(e, INIComment)]) 
                          for s in ast.sections),
            "includes": len([e for e in ast.global_entries if isinstance(e, INIInclude)]),
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
        }
        
        return INIAnalysisResult(
            format_type=format_type,
            sections=sections,
            total_keys=total_keys,
            complexity_score=complexity_score,
            recommendations=recommendations,
            warnings=warnings,
            statistics=statistics
        )
    
    def lint_configuration(self, file_path: str) -> List[INIDiagnostic]:
        """Lint INI configuration for best practices"""
        ast, parse_diagnostics = self.parse_ini_file(file_path)
        
        if not ast:
            return parse_diagnostics
        
        lint_diagnostics = self._lint_configuration(ast, file_path)
        return parse_diagnostics + lint_diagnostics
    
    def _check_git_availability(self) -> bool:
        """Check if git command is available"""
        try:
            subprocess.run(['git', '--version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _check_systemctl_availability(self) -> bool:
        """Check if systemctl command is available"""
        try:
            subprocess.run(['systemctl', '--version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _validate_ast(self, ast: INIConfiguration, file_path: Optional[str] = None, 
                     format_type: Optional[INIFormatType] = None) -> List[INIDiagnostic]:
        """Validate INI AST based on configuration level"""
        diagnostics = []
        
        if self.config.validation_level.value in ["syntax", "semantic", "schema", "complete"]:
            diagnostics.extend(self._validate_syntax(ast, file_path))
        
        if self.config.validation_level.value in ["semantic", "schema", "complete"]:
            diagnostics.extend(self._validate_semantics(ast, file_path))
        
        if self.config.validation_level.value in ["schema", "complete"]:
            diagnostics.extend(self._validate_schema(ast, file_path, format_type))
        
        if self.config.validation_level.value == "complete":
            diagnostics.extend(self._validate_external_tools(ast, file_path, format_type))
        
        return diagnostics
    
    def _validate_syntax(self, ast: INIConfiguration, file_path: Optional[str] = None) -> List[INIDiagnostic]:
        """Validate basic syntax"""
        diagnostics = []
        
        # Check for duplicate sections
        if self.config.check_duplicates:
            section_names = [s.name for s in ast.sections]
            duplicates = [name for name in section_names if section_names.count(name) > 1]
            for dup in set(duplicates):
                diagnostics.append(INIDiagnostic(
                    level="error",
                    message=f"Duplicate section: [{dup}]",
                    file=file_path,
                    section=dup,
                    code="DUPLICATE_SECTION"
                ))
        
        # Check for empty sections
        for section in ast.sections:
            if not section.entries:
                diagnostics.append(INIDiagnostic(
                    level="warning",
                    message=f"Empty section: [{section.name}]",
                    file=file_path,
                    section=section.name,
                    code="EMPTY_SECTION",
                    suggestion="Consider removing empty sections or adding content"
                ))
        
        return diagnostics
    
    def _validate_semantics(self, ast: INIConfiguration, file_path: Optional[str] = None) -> List[INIDiagnostic]:
        """Validate semantic correctness"""
        diagnostics = []
        
        # Check for duplicate keys within sections
        if self.config.check_duplicates:
            for section in ast.sections:
                key_names = []
                for entry in section.entries:
                    if isinstance(entry, INIKeyValuePair):
                        key_names.append(entry.key.name)
                
                duplicates = [name for name in key_names if key_names.count(name) > 1]
                for dup in set(duplicates):
                    diagnostics.append(INIDiagnostic(
                        level="error",
                        message=f"Duplicate key in section [{section.name}]: {dup}",
                        file=file_path,
                        section=section.name,
                        key=dup,
                        code="DUPLICATE_KEY"
                    ))
        
        # Type checking
        if self.config.check_types:
            diagnostics.extend(self._validate_types(ast, file_path))
        
        return diagnostics
    
    def _validate_schema(self, ast: INIConfiguration, file_path: Optional[str] = None,
                        format_type: Optional[INIFormatType] = None) -> List[INIDiagnostic]:
        """Validate against format-specific schemas"""
        diagnostics = []
        
        if not format_type:
            return diagnostics
        
        schema = self.format_schemas.get(format_type)
        if not schema:
            return diagnostics
        
        # Validate required sections
        required_sections = schema.get("required_sections", [])
        present_sections = [s.name for s in ast.sections]
        
        for required in required_sections:
            if required not in present_sections:
                diagnostics.append(INIDiagnostic(
                    level="error",
                    message=f"Missing required section: [{required}]",
                    file=file_path,
                    code="MISSING_REQUIRED_SECTION"
                ))
        
        return diagnostics
    
    def _validate_external_tools(self, ast: INIConfiguration, file_path: Optional[str] = None,
                               format_type: Optional[INIFormatType] = None) -> List[INIDiagnostic]:
        """Validate using external tools"""
        diagnostics = []
        
        if not file_path:
            return diagnostics
        
        # Git config validation
        if (format_type == INIFormatType.GIT_CONFIG and 
            self.config.git_config_validation and 
            self.git_available):
            _, git_diagnostics = self.git_config_validate(file_path)
            diagnostics.extend(git_diagnostics)
        
        # Systemd validation
        if (format_type == INIFormatType.SYSTEMD and 
            self.config.systemd_validation and 
            self.systemctl_available):
            _, systemd_diagnostics = self.systemd_validate(file_path)
            diagnostics.extend(systemd_diagnostics)
        
        return diagnostics
    
    def _validate_types(self, ast: INIConfiguration, file_path: Optional[str] = None) -> List[INIDiagnostic]:
        """Validate value types"""
        diagnostics = []
        
        for section in ast.sections:
            for entry in section.entries:
                if isinstance(entry, INIKeyValuePair):
                    value = entry.value
                    
                    # Check for type consistency
                    if value.value_type == INIValueType.NUMBER:
                        try:
                            float(value.value)
                        except ValueError:
                            diagnostics.append(INIDiagnostic(
                                level="error",
                                message=f"Invalid number value: {value.value}",
                                file=file_path,
                                section=section.name,
                                key=entry.key.name,
                                code="INVALID_NUMBER"
                            ))
                    
                    elif value.value_type == INIValueType.BOOLEAN:
                        if str(value.value).lower() not in ["true", "false", "yes", "no", "1", "0", "on", "off"]:
                            diagnostics.append(INIDiagnostic(
                                level="warning",
                                message=f"Unusual boolean value: {value.value}",
                                file=file_path,
                                section=section.name,
                                key=entry.key.name,
                                code="UNUSUAL_BOOLEAN",
                                suggestion="Use standard boolean values (true/false, yes/no, 1/0)"
                            ))
        
        return diagnostics
    
    def _detect_format(self, content: str, file_path: str) -> INIFormatType:
        """Detect INI format type from content and filename"""
        filename = Path(file_path).name.lower()
        
        # File extension based detection
        if filename.endswith('.service') or filename.endswith('.timer') or filename.endswith('.target'):
            return INIFormatType.SYSTEMD
        elif filename == '.gitconfig' or filename.endswith('.gitconfig'):
            return INIFormatType.GIT_CONFIG
        elif filename.endswith('.ini') and ('windows' in content.lower() or 'registry' in content.lower()):
            return INIFormatType.WINDOWS
        elif filename.endswith('.conf') and 'mysql' in content.lower():
            return INIFormatType.MYSQL_CONFIG
        elif filename == 'php.ini':
            return INIFormatType.PHP_INI
        
        # Content-based detection
        if '[Unit]' in content and '[Service]' in content:
            return INIFormatType.SYSTEMD
        elif '[user]' in content and '[core]' in content:
            return INIFormatType.GIT_CONFIG
        elif '[mysqld]' in content or '[client]' in content:
            return INIFormatType.MYSQL_CONFIG
        
        return INIFormatType.STANDARD
    
    def _detect_format_from_ast(self, ast: INIConfiguration) -> INIFormatType:
        """Detect format from AST structure"""
        section_names = [s.name.lower() for s in ast.sections]
        
        # Systemd detection
        systemd_sections = ['unit', 'service', 'timer', 'socket', 'install']
        if any(s in section_names for s in systemd_sections):
            return INIFormatType.SYSTEMD
        
        # Git config detection
        git_sections = ['user', 'core', 'remote', 'branch', 'alias']
        if any(s in section_names for s in git_sections):
            return INIFormatType.GIT_CONFIG
        
        # MySQL detection
        mysql_sections = ['mysqld', 'client', 'mysql']
        if any(s in section_names for s in mysql_sections):
            return INIFormatType.MYSQL_CONFIG
        
        return INIFormatType.STANDARD
    
    def _determine_format_style(self, ast: INIConfiguration, file_path: str) -> INIFormatStyle:
        """Determine appropriate format style for file"""
        format_type = self._detect_format_from_ast(ast)
        
        if format_type == INIFormatType.SYSTEMD:
            return INIFormatStyle.SYSTEMD
        elif format_type == INIFormatType.GIT_CONFIG:
            return INIFormatStyle.GIT_CONFIG
        elif format_type == INIFormatType.WINDOWS:
            return INIFormatStyle.WINDOWS
        else:
            return self.config.format_style
    
    def _calculate_complexity_score(self, ast: INIConfiguration) -> int:
        """Calculate configuration complexity score"""
        score = 0
        
        # Base complexity from structure
        score += len(ast.sections) * 2
        score += len(ast.global_entries)
        
        for section in ast.sections:
            score += len(section.entries)
            
            # Additional complexity for special constructs
            for entry in section.entries:
                if isinstance(entry, INIKeyValuePair):
                    if entry.value.value_type == INIValueType.LIST:
                        score += 2
                    elif entry.value.value_type == INIValueType.MULTILINE:
                        score += 3
        
        return score
    
    def _generate_recommendations(self, ast: INIConfiguration) -> List[str]:
        """Generate configuration recommendations"""
        recommendations = []
        
        # Check for organization
        if len(ast.sections) > 10:
            recommendations.append("Consider organizing sections into separate files")
        
        # Check for documentation
        comment_count = sum(len([e for e in s.entries if isinstance(e, INIComment)]) 
                          for s in ast.sections)
        total_entries = sum(len(s.entries) for s in ast.sections)
        
        if total_entries > 20 and comment_count < total_entries * 0.1:
            recommendations.append("Consider adding more comments for documentation")
        
        # Check for empty values
        for section in ast.sections:
            for entry in section.entries:
                if isinstance(entry, INIKeyValuePair) and not entry.value.value:
                    recommendations.append(f"Consider removing empty value in section [{section.name}], key {entry.key.name}")
        
        return recommendations
    
    def _collect_warnings(self, ast: INIConfiguration) -> List[str]:
        """Collect potential warnings"""
        warnings = []
        
        # Long section names
        for section in ast.sections:
            if len(section.name) > 50:
                warnings.append(f"Very long section name: [{section.name}]")
        
        # Many sections
        if len(ast.sections) > 20:
            warnings.append("Configuration has many sections, consider splitting")
        
        return warnings
    
    def _lint_configuration(self, ast: INIConfiguration, file_path: str) -> List[INIDiagnostic]:
        """Lint configuration for best practices"""
        diagnostics = []
        
        # Check naming conventions
        for section in ast.sections:
            if ' ' in section.name and not isinstance(section, GitConfigSection):
                diagnostics.append(INIDiagnostic(
                    level="warning",
                    message=f"Section name contains spaces: [{section.name}]",
                    file=file_path,
                    section=section.name,
                    code="SECTION_SPACING",
                    suggestion="Consider using underscores or hyphens instead of spaces"
                ))
            
            for entry in section.entries:
                if isinstance(entry, INIKeyValuePair):
                    if ' ' in entry.key.name:
                        diagnostics.append(INIDiagnostic(
                            level="warning",
                            message=f"Key name contains spaces: {entry.key.name}",
                            file=file_path,
                            section=section.name,
                            key=entry.key.name,
                            code="KEY_SPACING",
                            suggestion="Consider using underscores or hyphens"
                        ))
        
        # Check for common mistakes
        for section in ast.sections:
            for entry in section.entries:
                if isinstance(entry, INIKeyValuePair):
                    key_lower = entry.key.name.lower()
                    value_str = str(entry.value.value).lower()
                    
                    # Check for path issues
                    if 'path' in key_lower and '\\' in value_str and os.name != 'nt':
                        diagnostics.append(INIDiagnostic(
                            level="warning",
                            message=f"Windows-style path on non-Windows system: {entry.value.value}",
                            file=file_path,
                            section=section.name,
                            key=entry.key.name,
                            code="PLATFORM_PATH",
                            suggestion="Use forward slashes for cross-platform compatibility"
                        ))
        
        return diagnostics
    
    def _normalize_ini_code(self, code: str) -> str:
        """Normalize INI code for comparison"""
        lines = []
        for line in code.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith(';'):
                # Normalize whitespace around delimiters
                if '=' in line:
                    key, value = line.split('=', 1)
                    line = f"{key.strip()}={value.strip()}"
                lines.append(line)
        return '\n'.join(sorted(lines))
    
    def _load_format_schemas(self) -> Dict[INIFormatType, Dict[str, Any]]:
        """Load format-specific schemas"""
        schemas = {}
        
        # Systemd schema
        schemas[INIFormatType.SYSTEMD] = {
            "required_sections": ["Unit"],
            "optional_sections": ["Service", "Install", "Timer", "Socket"],
            "section_keys": {
                "Unit": ["Description", "After", "Requires"],
                "Service": ["Type", "ExecStart"],
                "Install": ["WantedBy"]
            }
        }
        
        # Git config schema
        schemas[INIFormatType.GIT_CONFIG] = {
            "optional_sections": ["user", "core", "remote", "branch", "alias"],
            "section_keys": {
                "user": ["name", "email"],
                "core": ["editor", "autocrlf", "filemode"],
                "remote": ["url", "fetch"]
            }
        }
        
        return schemas
    
    def _load_format_patterns(self) -> Dict[INIFormatType, Dict[str, Any]]:
        """Load format-specific patterns"""
        return {
            INIFormatType.SYSTEMD: {
                "comment_prefix": "#",
                "case_sensitive": True,
                "allow_subsections": False
            },
            INIFormatType.GIT_CONFIG: {
                "comment_prefix": "#",
                "case_sensitive": False,
                "allow_subsections": True
            },
            INIFormatType.WINDOWS: {
                "comment_prefix": ";",
                "case_sensitive": False,
                "allow_subsections": False
            }
        }
    
    def _get_reserved_sections(self) -> Set[str]:
        """Get reserved section names"""
        return {
            # Systemd
            "Unit", "Service", "Install", "Timer", "Socket", "Mount", "Automount",
            # Git
            "user", "core", "remote", "branch", "alias", "push", "pull", "merge",
            # MySQL
            "mysqld", "client", "mysql", "mysqldump", "mysqlimport"
        }
    
    def _get_known_keys(self) -> Dict[str, Set[str]]:
        """Get known keys for sections"""
        return {
            "Unit": {"Description", "After", "Before", "Requires", "Wants"},
            "Service": {"Type", "ExecStart", "ExecStop", "User", "Group", "WorkingDirectory"},
            "Install": {"WantedBy", "RequiredBy", "Also"},
            "user": {"name", "email", "signingkey"},
            "core": {"editor", "autocrlf", "filemode", "ignorecase"}
        }


def parse_ini_code(code: str, filename: Optional[str] = None) -> INIConfiguration:
    """Parse INI code string"""
    parser = INIParser()
    return parser.parse(code, filename)


def generate_ini_code(ast: INIConfiguration, style: INIFormatStyle = INIFormatStyle.STANDARD) -> str:
    """Generate INI code from AST"""
    generator_config = INIGeneratorConfig(style=style)
    generator = INICodeGenerator(generator_config)
    return generator.generate(ast)


def ini_round_trip_verify(code: str) -> bool:
    """Verify INI round-trip conversion"""
    try:
        # Parse original
        parser = INIParser()
        original_ast = parser.parse(code)
        
        # Generate and re-parse
        generator_config = INIGeneratorConfig(style=INIFormatStyle.STANDARD)
        generator = INICodeGenerator(generator_config)
        generated_code = generator.generate(original_ast)
        regenerated_ast = parser.parse(generated_code)
        
        # Compare normalized versions
        toolchain = INIToolchain()
        original_normalized = toolchain._normalize_ini_code(generator.generate(original_ast))
        regenerated_normalized = toolchain._normalize_ini_code(generator.generate(regenerated_ast))
        
        return original_normalized == regenerated_normalized
    except:
        return False


def ini_to_runa_translate(ini_config: INIConfiguration) -> Any:
    """Translate INI to Runa AST"""
    converter = INIToRunaConverter()
    return converter.convert(ini_config)


def runa_to_ini_translate(runa_module: Any) -> INIConfiguration:
    """Translate Runa AST to INI"""
    converter = RunaToINIConverter()
    return converter.convert(runa_module) 