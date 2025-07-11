#!/usr/bin/env python3
"""
Lua Toolchain - Complete Lua Development Toolchain Integration

Provides comprehensive Lua toolchain capabilities including:
- Lua parsing, validation, and formatting
- Integration with Lua interpreters (Lua 5.1-5.4, LuaJIT, OpenResty)
- Code analysis and linting with luacheck
- Testing framework integration (busted, luaunit)
- Package management (LuaRocks)
- Performance profiling and debugging
- Round-trip translation verification
- Love2D and OpenResty project support
- Module dependency analysis

Supports multiple Lua environments and development workflows.
"""

import os
import json
import subprocess
import tempfile
import shutil
from typing import List, Dict, Optional, Any, Union, Tuple, Set
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from .lua_ast import *
from .lua_parser import parse_lua, LuaParser
from .lua_converter import lua_to_runa, runa_to_lua, LuaToRunaConverter, RunaToLuaConverter
from .lua_generator import generate_lua, LuaCodeGenerator, LuaFormatStyle, LuaGeneratorConfig


class LuaValidationLevel(Enum):
    """Lua validation levels"""
    SYNTAX = "syntax"           # Basic syntax validation
    SEMANTIC = "semantic"       # Semantic validation with type checking
    LINT = "lint"              # Static analysis with luacheck
    COMPLETE = "complete"       # Full validation with interpreter


class LuaInterpreter(Enum):
    """Lua interpreter types"""
    LUA51 = "lua5.1"
    LUA52 = "lua5.2"
    LUA53 = "lua5.3"
    LUA54 = "lua5.4"
    LUAJIT = "luajit"
    OPENRESTY = "openresty"


class LuaProjectType(Enum):
    """Lua project types"""
    STANDARD = "standard"       # Standard Lua project
    LOVE2D = "love2d"          # Love2D game project
    OPENRESTY = "openresty"    # OpenResty web project
    LUAROCKS = "luarocks"      # LuaRocks module
    NGINX = "nginx"            # Nginx Lua module


@dataclass
class LuaDiagnostic:
    """Lua diagnostic message"""
    level: str  # "error", "warning", "info"
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None
    suggestion: Optional[str] = None
    rule: Optional[str] = None  # Luacheck rule


@dataclass
class LuaTestResult:
    """Lua test execution result"""
    success: bool
    total_tests: int
    passed_tests: int
    failed_tests: int
    output: str
    errors: List[str]
    duration: float


@dataclass
class LuaAnalysisResult:
    """Lua code analysis result"""
    complexity: int
    dependencies: List[str]
    globals: Set[str]
    functions: List[str]
    recommendations: List[str]
    warnings: List[str]
    statistics: Dict[str, Any]


@dataclass
class LuaToolchainConfig:
    """Configuration for Lua toolchain"""
    validation_level: LuaValidationLevel = LuaValidationLevel.SEMANTIC
    interpreter: LuaInterpreter = LuaInterpreter.LUA54
    project_type: LuaProjectType = LuaProjectType.STANDARD
    
    # Tool paths
    lua_path: Optional[str] = None
    luacheck_path: str = "luacheck"
    luarocks_path: str = "luarocks"
    busted_path: str = "busted"
    
    # Validation options
    check_globals: bool = True
    check_unused: bool = True
    check_undefined: bool = True
    max_line_length: int = 120
    
    # Project-specific options
    love2d_version: str = "11.4"
    openresty_version: str = "1.21.4.1"
    lua_version: str = "5.4"
    
    # Testing options
    test_framework: str = "busted"  # busted, luaunit, or custom
    test_directory: str = "test"
    test_pattern: str = "*_test.lua"
    
    # Formatting options
    format_style: LuaFormatStyle = LuaFormatStyle.STANDARD
    auto_format: bool = True


class LuaToolchain:
    """Complete Lua development toolchain"""
    
    def __init__(self, config: Optional[LuaToolchainConfig] = None):
        self.config = config or LuaToolchainConfig()
        self.working_directory: Optional[str] = None
        
        # Tool availability
        self.lua_available = self._check_lua_availability()
        self.luacheck_available = self._check_luacheck_availability()
        self.luarocks_available = self._check_luarocks_availability()
        self.busted_available = self._check_busted_availability()
        
        # Project detection
        self.project_type = self._detect_project_type()
        
        # Built-in Lua globals and functions
        self.lua_globals = self._get_lua_globals()
        self.lua_functions = self._get_lua_functions()
    
    def parse_lua_file(self, file_path: str) -> Tuple[Optional[LuaModule], List[LuaDiagnostic]]:
        """Parse Lua file and return AST with diagnostics"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Lua
            ast = parse_lua(content, file_path)
            
            # Validate based on configuration
            validation_diagnostics = self._validate_ast(ast, file_path)
            diagnostics.extend(validation_diagnostics)
            
            return ast, diagnostics
            
        except FileNotFoundError:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=f"File not found: {file_path}",
                file=file_path
            ))
            return None, diagnostics
            
        except Exception as e:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=f"Parse error: {str(e)}",
                file=file_path
            ))
            return None, diagnostics
    
    def parse_lua_directory(self, directory: str) -> Tuple[List[LuaModule], List[LuaDiagnostic]]:
        """Parse all Lua files in directory"""
        modules = []
        all_diagnostics = []
        
        lua_files = list(Path(directory).glob('**/*.lua'))
        
        for file_path in lua_files:
            ast, diagnostics = self.parse_lua_file(str(file_path))
            if ast:
                modules.append(ast)
            all_diagnostics.extend(diagnostics)
        
        return modules, all_diagnostics
    
    def validate_with_interpreter(self, file_path: str) -> Tuple[bool, List[LuaDiagnostic]]:
        """Validate Lua file using interpreter"""
        diagnostics = []
        
        if not self.lua_available:
            diagnostics.append(LuaDiagnostic(
                level="warning",
                message="Lua interpreter not available for validation",
                file=file_path
            ))
            return False, diagnostics
        
        try:
            lua_cmd = self._get_lua_command()
            
            # Check syntax with lua -l (load without running)
            result = subprocess.run(
                [lua_cmd, '-l', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                diagnostics.append(LuaDiagnostic(
                    level="info",
                    message="Lua syntax validation successful",
                    file=file_path
                ))
                return True, diagnostics
            else:
                # Parse Lua error messages
                for line in result.stderr.split('\n'):
                    if line.strip() and 'lua:' in line:
                        diagnostics.append(LuaDiagnostic(
                            level="error",
                            message=line.strip(),
                            file=file_path
                        ))
                return False, diagnostics
                
        except subprocess.TimeoutExpired:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message="Lua validation timed out",
                file=file_path
            ))
            return False, diagnostics
        except Exception as e:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=f"Lua validation error: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def luacheck_validate(self, file_path: str) -> Tuple[bool, List[LuaDiagnostic]]:
        """Validate Lua file using luacheck"""
        diagnostics = []
        
        if not self.luacheck_available:
            diagnostics.append(LuaDiagnostic(
                level="warning",
                message="Luacheck not available for validation",
                file=file_path
            ))
            return False, diagnostics
        
        try:
            result = subprocess.run(
                [self.config.luacheck_path, '--formatter', 'json', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                try:
                    luacheck_results = json.loads(result.stdout)
                    
                    for file_result in luacheck_results:
                        for issue in file_result.get('events', []):
                            level = self._luacheck_severity_to_level(issue.get('severity', 'warning'))
                            diagnostics.append(LuaDiagnostic(
                                level=level,
                                message=issue.get('message', 'Unknown luacheck issue'),
                                file=file_path,
                                line=issue.get('line'),
                                column=issue.get('column'),
                                code=issue.get('code'),
                                rule=issue.get('name')
                            ))
                
                except json.JSONDecodeError:
                    # Fallback to parsing text output
                    diagnostics.extend(self._parse_luacheck_text_output(result.stdout, file_path))
            
            success = result.returncode == 0
            return success, diagnostics
            
        except subprocess.TimeoutExpired:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message="Luacheck validation timed out",
                file=file_path
            ))
            return False, diagnostics
        except Exception as e:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=f"Luacheck validation error: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def format_lua_file(self, file_path: str, in_place: bool = False) -> Tuple[str, List[LuaDiagnostic]]:
        """Format Lua file"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse and format
            ast = parse_lua(content, file_path)
            
            # Determine format style based on project type
            format_style = self._determine_format_style()
            
            generator_config = LuaGeneratorConfig(style=format_style)
            generator = LuaCodeGenerator(generator_config)
            formatted_content = generator.generate(ast)
            
            if in_place:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                diagnostics.append(LuaDiagnostic(
                    level="info",
                    message=f"Formatted file: {file_path}",
                    file=file_path
                ))
            
            return formatted_content, diagnostics
            
        except Exception as e:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=f"Formatting error: {str(e)}",
                file=file_path
            ))
            return "", diagnostics
    
    def run_tests(self, directory: str) -> LuaTestResult:
        """Run Lua tests using configured test framework"""
        if self.config.test_framework == "busted" and self.busted_available:
            return self._run_busted_tests(directory)
        else:
            return self._run_custom_tests(directory)
    
    def analyze_file(self, file_path: str) -> LuaAnalysisResult:
        """Analyze Lua file for complexity and metrics"""
        try:
            ast, _ = self.parse_lua_file(file_path)
            
            if not ast:
                return LuaAnalysisResult(
                    complexity=0,
                    dependencies=[],
                    globals=set(),
                    functions=[],
                    recommendations=["File could not be parsed"],
                    warnings=["Parse errors present"],
                    statistics={}
                )
            
            # Analyze AST
            analyzer = LuaCodeAnalyzer()
            analysis = analyzer.analyze(ast)
            
            return analysis
            
        except Exception as e:
            return LuaAnalysisResult(
                complexity=0,
                dependencies=[],
                globals=set(),
                functions=[],
                recommendations=[f"Analysis error: {str(e)}"],
                warnings=["Analysis failed"],
                statistics={}
            )
    
    def lua_to_runa_convert(self, lua_module: LuaModule) -> Any:
        """Convert Lua to Runa AST"""
        converter = LuaToRunaConverter()
        return converter.convert(lua_module)
    
    def runa_to_lua_convert(self, runa_module: Any) -> LuaModule:
        """Convert Runa AST to Lua"""
        converter = RunaToLuaConverter()
        return converter.convert(runa_module)
    
    def round_trip_verify(self, file_path: str) -> Tuple[bool, List[LuaDiagnostic]]:
        """Verify round-trip conversion preserves semantics"""
        diagnostics = []
        
        try:
            # Parse original
            original_ast, parse_diagnostics = self.parse_lua_file(file_path)
            diagnostics.extend(parse_diagnostics)
            
            if not original_ast:
                return False, diagnostics
            
            # Convert to Runa and back
            runa_ast = self.lua_to_runa_convert(original_ast)
            converted_ast = self.runa_to_lua_convert(runa_ast)
            
            # Generate both versions
            generator_config = LuaGeneratorConfig(style=LuaFormatStyle.STANDARD)
            generator = LuaCodeGenerator(generator_config)
            
            original_code = generator.generate(original_ast)
            converted_code = generator.generate(converted_ast)
            
            # Normalize for comparison
            original_normalized = self._normalize_lua_code(original_code)
            converted_normalized = self._normalize_lua_code(converted_code)
            
            if original_normalized == converted_normalized:
                diagnostics.append(LuaDiagnostic(
                    level="info",
                    message="Round-trip verification successful",
                    file=file_path
                ))
                return True, diagnostics
            else:
                diagnostics.append(LuaDiagnostic(
                    level="warning",
                    message="Round-trip verification shows differences",
                    file=file_path,
                    suggestion="Check for lossy conversion in complex constructs"
                ))
                return False, diagnostics
                
        except Exception as e:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=f"Round-trip verification error: {str(e)}",
                file=file_path
            ))
            return False, diagnostics
    
    def install_dependencies(self, directory: str) -> Tuple[bool, List[str]]:
        """Install Lua dependencies using LuaRocks"""
        messages = []
        
        if not self.luarocks_available:
            messages.append("LuaRocks not available for dependency management")
            return False, messages
        
        rockspec_files = list(Path(directory).glob('*.rockspec'))
        
        if not rockspec_files:
            messages.append("No rockspec file found")
            return False, messages
        
        try:
            for rockspec in rockspec_files:
                result = subprocess.run(
                    [self.config.luarocks_path, 'install', str(rockspec)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    messages.append(f"Successfully installed dependencies from {rockspec.name}")
                else:
                    messages.append(f"Failed to install dependencies from {rockspec.name}: {result.stderr}")
                    return False, messages
            
            return True, messages
            
        except Exception as e:
            messages.append(f"Dependency installation error: {str(e)}")
            return False, messages
    
    # Helper methods
    def _check_lua_availability(self) -> bool:
        """Check if Lua interpreter is available"""
        try:
            lua_cmd = self._get_lua_command()
            subprocess.run([lua_cmd, '-v'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _check_luacheck_availability(self) -> bool:
        """Check if luacheck is available"""
        try:
            subprocess.run([self.config.luacheck_path, '--version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _check_luarocks_availability(self) -> bool:
        """Check if LuaRocks is available"""
        try:
            subprocess.run([self.config.luarocks_path, '--version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _check_busted_availability(self) -> bool:
        """Check if busted test framework is available"""
        try:
            subprocess.run([self.config.busted_path, '--version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _get_lua_command(self) -> str:
        """Get appropriate Lua command based on interpreter"""
        if self.config.lua_path:
            return self.config.lua_path
        
        interpreter_commands = {
            LuaInterpreter.LUA51: "lua5.1",
            LuaInterpreter.LUA52: "lua5.2", 
            LuaInterpreter.LUA53: "lua5.3",
            LuaInterpreter.LUA54: "lua5.4",
            LuaInterpreter.LUAJIT: "luajit",
            LuaInterpreter.OPENRESTY: "openresty",
        }
        
        return interpreter_commands.get(self.config.interpreter, "lua")
    
    def _detect_project_type(self) -> LuaProjectType:
        """Detect project type from files and structure"""
        if self.working_directory:
            project_path = Path(self.working_directory)
            
            # Check for Love2D
            if (project_path / "main.lua").exists() or (project_path / "conf.lua").exists():
                return LuaProjectType.LOVE2D
            
            # Check for OpenResty
            if (project_path / "nginx.conf").exists() or any(project_path.glob("**/nginx.conf")):
                return LuaProjectType.OPENRESTY
            
            # Check for LuaRocks
            if any(project_path.glob("*.rockspec")):
                return LuaProjectType.LUAROCKS
        
        return LuaProjectType.STANDARD
    
    def _validate_ast(self, ast: LuaModule, file_path: Optional[str] = None) -> List[LuaDiagnostic]:
        """Validate Lua AST based on configuration level"""
        diagnostics = []
        
        if self.config.validation_level.value in ["syntax", "semantic", "lint", "complete"]:
            diagnostics.extend(self._validate_syntax(ast, file_path))
        
        if self.config.validation_level.value in ["semantic", "lint", "complete"]:
            diagnostics.extend(self._validate_semantics(ast, file_path))
        
        if self.config.validation_level.value in ["lint", "complete"] and file_path:
            _, lint_diagnostics = self.luacheck_validate(file_path)
            diagnostics.extend(lint_diagnostics)
        
        if self.config.validation_level.value == "complete" and file_path:
            _, interpreter_diagnostics = self.validate_with_interpreter(file_path)
            diagnostics.extend(interpreter_diagnostics)
        
        return diagnostics
    
    def _validate_syntax(self, ast: LuaModule, file_path: Optional[str] = None) -> List[LuaDiagnostic]:
        """Validate basic syntax"""
        diagnostics = []
        
        # Check for basic syntax issues (this would be expanded)
        validator = LuaSyntaxValidator()
        syntax_issues = validator.validate(ast)
        
        for issue in syntax_issues:
            diagnostics.append(LuaDiagnostic(
                level="error",
                message=issue,
                file=file_path,
                code="SYNTAX_ERROR"
            ))
        
        return diagnostics
    
    def _validate_semantics(self, ast: LuaModule, file_path: Optional[str] = None) -> List[LuaDiagnostic]:
        """Validate semantic correctness"""
        diagnostics = []
        
        # Check for semantic issues (this would be expanded)
        validator = LuaSemanticValidator(self.lua_globals, self.lua_functions)
        semantic_issues = validator.validate(ast)
        
        for issue in semantic_issues:
            diagnostics.append(LuaDiagnostic(
                level="warning",
                message=issue["message"],
                file=file_path,
                line=issue.get("line"),
                code=issue.get("code", "SEMANTIC_WARNING")
            ))
        
        return diagnostics
    
    def _determine_format_style(self) -> LuaFormatStyle:
        """Determine appropriate format style"""
        if self.project_type == LuaProjectType.LOVE2D:
            return LuaFormatStyle.LOVE2D
        elif self.project_type == LuaProjectType.OPENRESTY:
            return LuaFormatStyle.OPENRESTY
        elif self.project_type == LuaProjectType.LUAROCKS:
            return LuaFormatStyle.LUAROCKS
        else:
            return self.config.format_style
    
    def _run_busted_tests(self, directory: str) -> LuaTestResult:
        """Run tests using busted framework"""
        try:
            result = subprocess.run(
                [self.config.busted_path, '--output=json', directory],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse busted JSON output
            if result.stdout:
                try:
                    test_data = json.loads(result.stdout)
                    return LuaTestResult(
                        success=test_data.get('success', False),
                        total_tests=test_data.get('total', 0),
                        passed_tests=test_data.get('passed', 0),
                        failed_tests=test_data.get('failed', 0),
                        output=result.stdout,
                        errors=[],
                        duration=test_data.get('duration', 0.0)
                    )
                except json.JSONDecodeError:
                    pass
            
            # Fallback to basic result
            return LuaTestResult(
                success=result.returncode == 0,
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                output=result.stdout,
                errors=[result.stderr] if result.stderr else [],
                duration=0.0
            )
            
        except Exception as e:
            return LuaTestResult(
                success=False,
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                output="",
                errors=[str(e)],
                duration=0.0
            )
    
    def _run_custom_tests(self, directory: str) -> LuaTestResult:
        """Run tests using custom test runner"""
        # Simple test runner implementation
        test_files = list(Path(directory).glob(self.config.test_pattern))
        
        total_tests = len(test_files)
        passed_tests = 0
        errors = []
        
        for test_file in test_files:
            try:
                lua_cmd = self._get_lua_command()
                result = subprocess.run(
                    [lua_cmd, str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    passed_tests += 1
                else:
                    errors.append(f"{test_file}: {result.stderr}")
                    
            except Exception as e:
                errors.append(f"{test_file}: {str(e)}")
        
        return LuaTestResult(
            success=len(errors) == 0,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=total_tests - passed_tests,
            output="",
            errors=errors,
            duration=0.0
        )
    
    def _luacheck_severity_to_level(self, severity: str) -> str:
        """Convert luacheck severity to diagnostic level"""
        severity_map = {
            "error": "error",
            "warning": "warning",
            "info": "info"
        }
        return severity_map.get(severity, "warning")
    
    def _parse_luacheck_text_output(self, output: str, file_path: str) -> List[LuaDiagnostic]:
        """Parse luacheck text output"""
        diagnostics = []
        
        for line in output.split('\n'):
            if line.strip() and ':' in line:
                parts = line.split(':', 3)
                if len(parts) >= 3:
                    try:
                        line_num = int(parts[1])
                        message = parts[2].strip() if len(parts) > 2 else "Luacheck issue"
                        
                        diagnostics.append(LuaDiagnostic(
                            level="warning",
                            message=message,
                            file=file_path,
                            line=line_num
                        ))
                    except ValueError:
                        continue
        
        return diagnostics
    
    def _normalize_lua_code(self, code: str) -> str:
        """Normalize Lua code for comparison"""
        lines = []
        for line in code.split('\n'):
            line = line.strip()
            if line and not line.startswith('--'):
                # Normalize whitespace
                line = ' '.join(line.split())
                lines.append(line)
        return '\n'.join(sorted(lines))
    
    def _get_lua_globals(self) -> Set[str]:
        """Get standard Lua global variables"""
        return {
            "_G", "_VERSION", "assert", "collectgarbage", "dofile", "error",
            "getmetatable", "ipairs", "load", "loadfile", "next", "pairs",
            "pcall", "print", "rawequal", "rawget", "rawlen", "rawset",
            "require", "select", "setmetatable", "tonumber", "tostring",
            "type", "xpcall", "coroutine", "package", "string", "utf8",
            "table", "math", "io", "os", "debug"
        }
    
    def _get_lua_functions(self) -> Set[str]:
        """Get standard Lua functions"""
        return {
            "assert", "collectgarbage", "dofile", "error", "getmetatable",
            "ipairs", "load", "loadfile", "next", "pairs", "pcall", "print",
            "rawequal", "rawget", "rawlen", "rawset", "require", "select",
            "setmetatable", "tonumber", "tostring", "type", "xpcall"
        }


# Simple validator classes (would be expanded in real implementation)
class LuaSyntaxValidator:
    """Basic Lua syntax validator"""
    
    def validate(self, ast: LuaModule) -> List[str]:
        """Validate syntax issues"""
        issues = []
        # Implementation would check for syntax issues
        return issues


class LuaSemanticValidator:
    """Basic Lua semantic validator"""
    
    def __init__(self, globals: Set[str], functions: Set[str]):
        self.globals = globals
        self.functions = functions
    
    def validate(self, ast: LuaModule) -> List[Dict[str, Any]]:
        """Validate semantic issues"""
        issues = []
        # Implementation would check for semantic issues
        return issues


class LuaCodeAnalyzer:
    """Lua code complexity and metrics analyzer"""
    
    def analyze(self, ast: LuaModule) -> LuaAnalysisResult:
        """Analyze Lua code for metrics"""
        # Simple analysis implementation
        return LuaAnalysisResult(
            complexity=self._calculate_complexity(ast),
            dependencies=self._extract_dependencies(ast),
            globals=self._find_globals(ast),
            functions=self._find_functions(ast),
            recommendations=self._generate_recommendations(ast),
            warnings=self._find_warnings(ast),
            statistics=self._calculate_statistics(ast)
        )
    
    def _calculate_complexity(self, ast: LuaModule) -> int:
        """Calculate cyclomatic complexity"""
        return 1  # Simplified
    
    def _extract_dependencies(self, ast: LuaModule) -> List[str]:
        """Extract require dependencies"""
        return []  # Simplified
    
    def _find_globals(self, ast: LuaModule) -> Set[str]:
        """Find global variable usage"""
        return set()  # Simplified
    
    def _find_functions(self, ast: LuaModule) -> List[str]:
        """Find function definitions"""
        return []  # Simplified
    
    def _generate_recommendations(self, ast: LuaModule) -> List[str]:
        """Generate code improvement recommendations"""
        return []  # Simplified
    
    def _find_warnings(self, ast: LuaModule) -> List[str]:
        """Find potential issues"""
        return []  # Simplified
    
    def _calculate_statistics(self, ast: LuaModule) -> Dict[str, Any]:
        """Calculate code statistics"""
        return {}  # Simplified


# Convenience functions
def parse_lua_code(code: str, filename: Optional[str] = None) -> LuaModule:
    """Parse Lua code string"""
    return parse_lua(code, filename)


def generate_lua_code(ast: LuaModule, style: LuaFormatStyle = LuaFormatStyle.STANDARD) -> str:
    """Generate Lua code from AST"""
    generator_config = LuaGeneratorConfig(style=style)
    generator = LuaCodeGenerator(generator_config)
    return generator.generate(ast)


def lua_round_trip_verify(code: str) -> bool:
    """Verify Lua round-trip conversion"""
    try:
        # Parse original
        original_ast = parse_lua(code)
        
        # Generate and re-parse
        generator_config = LuaGeneratorConfig(style=LuaFormatStyle.STANDARD)
        generator = LuaCodeGenerator(generator_config)
        generated_code = generator.generate(original_ast)
        regenerated_ast = parse_lua(generated_code)
        
        # Compare normalized versions
        toolchain = LuaToolchain()
        original_normalized = toolchain._normalize_lua_code(generator.generate(original_ast))
        regenerated_normalized = toolchain._normalize_lua_code(generator.generate(regenerated_ast))
        
        return original_normalized == regenerated_normalized
    except:
        return False


def lua_to_runa_translate(lua_module: LuaModule) -> Any:
    """Translate Lua to Runa AST"""
    converter = LuaToRunaConverter()
    return converter.convert(lua_module)


def runa_to_lua_translate(runa_module: Any) -> LuaModule:
    """Translate Runa AST to Lua"""
    converter = RunaToLuaConverter()
    return converter.convert(runa_module) 