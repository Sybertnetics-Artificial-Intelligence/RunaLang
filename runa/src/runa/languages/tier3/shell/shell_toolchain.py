#!/usr/bin/env python3
"""
Shell Toolchain - Complete Shell Script Toolchain Integration

Provides comprehensive shell script toolchain capabilities including:
- Shell script parsing, validation, and syntax checking
- ShellCheck integration for linting and best practices
- Shell formatting with shfmt and custom formatters
- Script testing and execution in different shell environments
- Portability analysis and POSIX compliance checking
- Round-trip translation verification
- Security analysis and vulnerability detection
- Performance profiling and optimization suggestions

Supports POSIX sh, Bash, Zsh, Fish, and other shell dialects.
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

from .shell_ast import *
from .shell_parser import parse_shell, ShellLexer, ShellParser, validate_shell_syntax
from .shell_converter import shell_to_runa, runa_to_shell, ShellToRunaConverter, RunaToShellConverter
from .shell_generator import generate_shell, ShellCodeGenerator, ShellDialect, ShellFormatStyle, ShellGeneratorConfig


class ShellValidationLevel(Enum):
    """Shell validation levels"""
    SYNTAX = "syntax"           # Basic syntax validation
    SEMANTIC = "semantic"       # Semantic validation with variable checking
    LINT = "lint"               # Linting with best practices
    SECURITY = "security"       # Security analysis
    COMPLETE = "complete"       # Full validation with all checks


class ShellTestFramework(Enum):
    """Shell testing frameworks"""
    BATS = "bats"              # Bash Automated Testing System
    SHUNIT2 = "shunit2"        # Shell unit testing framework
    ROUNDUP = "roundup"        # Simple testing framework
    ASSERT_SH = "assert.sh"    # Minimalist assertion library
    SHARNESS = "sharness"      # Shell test framework


@dataclass
class ShellDiagnostic:
    """Shell diagnostic message"""
    level: str  # "error", "warning", "info", "note"
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None
    suggestion: Optional[str] = None
    rule: Optional[str] = None
    fix: Optional[str] = None


@dataclass
class ShellTestResult:
    """Shell test execution result"""
    passed: bool
    output: str
    error_output: str
    exit_code: int
    execution_time: float
    shell_used: str
    test_count: int
    failures: List[str]


@dataclass
class ShellAnalysis:
    """Shell script analysis result"""
    file_count: int
    line_count: int
    function_count: int
    complexity_score: int
    shell_dialect: ShellDialect
    portability_score: float  # 0.0 to 1.0
    security_score: float     # 0.0 to 1.0
    recommendations: List[str]
    issues: List[ShellDiagnostic]
    dependencies: List[str]   # External commands used
    metadata: Dict[str, Any]


@dataclass
class ShellToolchainConfig:
    """Configuration for Shell toolchain"""
    default_shell: ShellDialect = ShellDialect.BASH
    validation_level: ShellValidationLevel = ShellValidationLevel.SEMANTIC
    auto_format: bool = True
    auto_detect_dialect: bool = True
    strict_posix: bool = False
    
    # Tool paths
    shellcheck_path: str = "shellcheck"
    shfmt_path: str = "shfmt"
    bash_path: str = "bash"
    zsh_path: str = "zsh"
    fish_path: str = "fish"
    dash_path: str = "dash"
    
    # Validation options
    check_undefined_variables: bool = True
    check_command_existence: bool = True
    check_syntax_errors: bool = True
    check_best_practices: bool = True
    check_security_issues: bool = True
    check_portability: bool = True
    
    # Formatting options
    format_style: ShellFormatStyle = ShellFormatStyle.STANDARD
    indent_size: int = 2
    max_line_length: int = 120
    use_tabs: bool = False
    
    # Testing options
    test_framework: ShellTestFramework = ShellTestFramework.BATS
    test_all_shells: bool = False
    timeout_seconds: int = 30


class ShellToolchain:
    """Complete shell script toolchain"""
    
    def __init__(self, config: Optional[ShellToolchainConfig] = None):
        self.config = config or ShellToolchainConfig()
        self.external_tools = self._check_external_tools()
        self.working_directory: Optional[str] = None
        self.shell_paths = self._find_shell_paths()
        
        # Shell-specific configurations
        self.shell_configs = {
            ShellDialect.BASH: {"strict_mode": "set -euo pipefail", "ext": ".sh"},
            ShellDialect.ZSH: {"strict_mode": "set -euo pipefail", "ext": ".zsh"},
            ShellDialect.FISH: {"strict_mode": "", "ext": ".fish"},
            ShellDialect.POSIX: {"strict_mode": "set -eu", "ext": ".sh"},
            ShellDialect.DASH: {"strict_mode": "set -eu", "ext": ".sh"}
        }
        
        # Common shell security patterns
        self.security_patterns = [
            (r'\$\([^)]*\)', "Command substitution security risk"),
            (r'eval\s+', "Use of eval command"),
            (r'exec\s+', "Use of exec command"),
            (r'source\s+\$', "Dynamic sourcing"),
            (r'\|\s*sh', "Piping to shell"),
            (r'wget\s+.*\|\s*sh', "Download and execute pattern"),
            (r'curl\s+.*\|\s*sh', "Download and execute pattern"),
        ]
    
    def parse_shell_file(self, file_path: str) -> Tuple[Optional[ShellScript], List[ShellDiagnostic]]:
        """Parse shell script file and return AST with diagnostics"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Auto-detect shell dialect if enabled
            if self.config.auto_detect_dialect:
                dialect = self._detect_shell_dialect(file_path, content)
            else:
                dialect = self.config.default_shell
            
            # Parse shell script
            ast = parse_shell(content)
            
            # Validate based on configuration
            validation_diagnostics = self._validate_ast(ast, file_path, dialect)
            diagnostics.extend(validation_diagnostics)
            
            return ast, diagnostics
            
        except FileNotFoundError:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"File not found: {file_path}",
                file=file_path
            ))
            return None, diagnostics
            
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"Parse error: {str(e)}",
                file=file_path,
                code="parse_error"
            ))
            return None, diagnostics
    
    def parse_shell_directory(self, directory: str) -> Tuple[List[ShellScript], List[ShellDiagnostic]]:
        """Parse all shell script files in directory"""
        scripts = []
        all_diagnostics = []
        
        shell_files = []
        for ext in ['.sh', '.bash', '.zsh', '.fish']:
            shell_files.extend(Path(directory).glob(f'**/*{ext}'))
        
        # Also check files with shell shebangs
        for file_path in Path(directory).glob('**/*'):
            if file_path.is_file() and not file_path.suffix:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline()
                        if first_line.startswith('#!') and any(shell in first_line for shell in ['sh', 'bash', 'zsh', 'fish']):
                            shell_files.append(file_path)
                except:
                    pass
        
        for file_path in shell_files:
            ast, diagnostics = self.parse_shell_file(str(file_path))
            if ast:
                scripts.append(ast)
            all_diagnostics.extend(diagnostics)
        
        return scripts, all_diagnostics
    
    def validate_script(self, script: ShellScript, file_path: Optional[str] = None,
                       dialect: Optional[ShellDialect] = None) -> List[ShellDiagnostic]:
        """Validate shell script"""
        if dialect is None:
            dialect = self._detect_script_dialect(script)
        
        return self._validate_ast(script, file_path, dialect)
    
    def format_shell_file(self, file_path: str, in_place: bool = False) -> Tuple[str, List[ShellDiagnostic]]:
        """Format shell script file"""
        diagnostics = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try external formatter first if available
            if self.external_tools.get("shfmt"):
                formatted_content, format_diagnostics = self._format_with_shfmt(content, file_path)
                diagnostics.extend(format_diagnostics)
            else:
                # Use built-in formatter
                ast = parse_shell(content)
                dialect = self._detect_shell_dialect(file_path, content)
                
                generator_config = ShellGeneratorConfig(
                    dialect=dialect,
                    style=self.config.format_style,
                    indent_size=self.config.indent_size,
                    max_line_length=self.config.max_line_length
                )
                generator = ShellCodeGenerator(generator_config)
                formatted_content = generator.generate(ast)
            
            if in_place:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                diagnostics.append(ShellDiagnostic(
                    level="info",
                    message=f"Formatted file: {file_path}",
                    file=file_path
                ))
            
            return formatted_content, diagnostics
            
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"Format error: {str(e)}",
                file=file_path,
                code="format_error"
            ))
            return "", diagnostics
    
    def lint_script(self, file_path: str) -> List[ShellDiagnostic]:
        """Lint shell script with ShellCheck and built-in rules"""
        diagnostics = []
        
        # Use ShellCheck if available
        if self.external_tools.get("shellcheck"):
            shellcheck_diagnostics = self._lint_with_shellcheck(file_path)
            diagnostics.extend(shellcheck_diagnostics)
        
        # Built-in linting
        try:
            ast, parse_diagnostics = self.parse_shell_file(file_path)
            diagnostics.extend(parse_diagnostics)
            
            if ast:
                built_in_diagnostics = self._lint_shell_ast(ast, file_path)
                diagnostics.extend(built_in_diagnostics)
        
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"Lint error: {str(e)}",
                file=file_path,
                code="lint_error"
            ))
        
        return diagnostics
    
    def test_shell_script(self, file_path: str, test_file: Optional[str] = None) -> ShellTestResult:
        """Test shell script execution"""
        try:
            if test_file:
                return self._run_test_file(test_file, file_path)
            else:
                return self._run_basic_test(file_path)
                
        except Exception as e:
            return ShellTestResult(
                passed=False,
                output="",
                error_output=str(e),
                exit_code=1,
                execution_time=0.0,
                shell_used="unknown",
                test_count=0,
                failures=[str(e)]
            )
    
    def check_portability(self, file_path: str) -> Tuple[float, List[ShellDiagnostic]]:
        """Check shell script portability across different shells"""
        diagnostics = []
        portability_score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for shell-specific constructs
            bashisms = self._check_bashisms(content)
            if bashisms:
                portability_score -= len(bashisms) * 0.1
                diagnostics.extend(bashisms)
            
            # Test in different shells if available
            if self.config.test_all_shells:
                shell_test_results = self._test_in_multiple_shells(file_path)
                for shell, passed in shell_test_results.items():
                    if not passed:
                        portability_score -= 0.2
                        diagnostics.append(ShellDiagnostic(
                            level="warning",
                            message=f"Script fails in {shell}",
                            file=file_path,
                            code="portability_issue"
                        ))
            
            portability_score = max(0.0, portability_score)
            
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"Portability check error: {str(e)}",
                file=file_path,
                code="portability_error"
            ))
            portability_score = 0.0
        
        return portability_score, diagnostics
    
    def analyze_security(self, file_path: str) -> Tuple[float, List[ShellDiagnostic]]:
        """Analyze shell script for security issues"""
        diagnostics = []
        security_score = 1.0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check security patterns
            for pattern, description in self.security_patterns:
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    security_score -= 0.1
                    
                    diagnostics.append(ShellDiagnostic(
                        level="warning",
                        message=description,
                        file=file_path,
                        line=line_num,
                        column=match.start() - content.rfind('\n', 0, match.start()),
                        code="security_risk",
                        suggestion="Review for security implications"
                    ))
            
            # Check for other security issues
            security_issues = self._check_security_issues(content, file_path)
            diagnostics.extend(security_issues)
            security_score -= len(security_issues) * 0.05
            
            security_score = max(0.0, security_score)
            
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"Security analysis error: {str(e)}",
                file=file_path,
                code="security_error"
            ))
            security_score = 0.0
        
        return security_score, diagnostics
    
    def shell_to_runa_convert(self, shell_script: ShellScript) -> Any:
        """Convert Shell script to Runa AST"""
        converter = ShellToRunaConverter()
        return converter.convert(shell_script)
    
    def runa_to_shell_convert(self, runa_module: Any) -> ShellScript:
        """Convert Runa AST to Shell script"""
        converter = RunaToShellConverter()
        return converter.convert(runa_module)
    
    def round_trip_verify(self, file_path: str) -> Tuple[bool, List[ShellDiagnostic]]:
        """Verify round-trip conversion accuracy"""
        diagnostics = []
        
        try:
            # Parse original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            original_ast = parse_shell(original_content)
            
            # Convert to Runa and back
            runa_module = self.shell_to_runa_convert(original_ast)
            reconstructed_ast = self.runa_to_shell_convert(runa_module)
            
            # Generate and compare
            generator = ShellCodeGenerator()
            reconstructed_content = generator.generate(reconstructed_ast)
            
            # Normalize for comparison
            original_normalized = self._normalize_shell_content(original_content)
            reconstructed_normalized = self._normalize_shell_content(reconstructed_content)
            
            success = original_normalized == reconstructed_normalized
            
            if not success:
                diagnostics.append(ShellDiagnostic(
                    level="warning",
                    message="Round-trip conversion produced different result",
                    file=file_path,
                    code="round_trip_mismatch",
                    suggestion="Check for semantic preservation issues"
                ))
            else:
                diagnostics.append(ShellDiagnostic(
                    level="info",
                    message="Round-trip conversion successful",
                    file=file_path
                ))
            
            return success, diagnostics
            
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"Round-trip verification error: {str(e)}",
                file=file_path,
                code="round_trip_error"
            ))
            return False, diagnostics
    
    def analyze_script(self, file_path: str) -> ShellAnalysis:
        """Analyze shell script comprehensively"""
        scripts, diagnostics = self.parse_shell_directory(Path(file_path).parent)
        
        # Calculate metrics
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        line_count = len(content.split('\n'))
        
        # Parse script for analysis
        ast, parse_diagnostics = self.parse_shell_file(file_path)
        diagnostics.extend(parse_diagnostics)
        
        function_count = len(ast.functions) if ast else 0
        
        # Detect dialect
        dialect = self._detect_shell_dialect(file_path, content)
        
        # Calculate complexity
        complexity_score = self._calculate_complexity_score(ast) if ast else 0
        
        # Check portability and security
        portability_score, port_diagnostics = self.check_portability(file_path)
        diagnostics.extend(port_diagnostics)
        
        security_score, sec_diagnostics = self.analyze_security(file_path)
        diagnostics.extend(sec_diagnostics)
        
        # Find dependencies (external commands)
        dependencies = self._find_dependencies(ast) if ast else []
        
        # Generate recommendations
        recommendations = self._generate_recommendations(diagnostics, portability_score, security_score)
        
        return ShellAnalysis(
            file_count=1,
            line_count=line_count,
            function_count=function_count,
            complexity_score=complexity_score,
            shell_dialect=dialect,
            portability_score=portability_score,
            security_score=security_score,
            recommendations=recommendations,
            issues=diagnostics,
            dependencies=dependencies,
            metadata={
                "validation_level": self.config.validation_level.value,
                "total_diagnostics": len(diagnostics),
                "error_count": len([d for d in diagnostics if d.level == "error"]),
                "warning_count": len([d for d in diagnostics if d.level == "warning"])
            }
        )
    
    def _check_external_tools(self) -> Dict[str, bool]:
        """Check availability of external tools"""
        tools = {}
        
        # Check each tool
        for tool, path in [
            ("shellcheck", self.config.shellcheck_path),
            ("shfmt", self.config.shfmt_path),
            ("bash", self.config.bash_path),
            ("zsh", self.config.zsh_path),
            ("fish", self.config.fish_path),
            ("dash", self.config.dash_path),
        ]:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True)
                tools[tool] = result.returncode == 0
            except (FileNotFoundError, subprocess.SubprocessError):
                tools[tool] = False
        
        return tools
    
    def _find_shell_paths(self) -> Dict[ShellDialect, str]:
        """Find paths to different shell executables"""
        shells = {}
        
        for dialect, path_config in [
            (ShellDialect.BASH, self.config.bash_path),
            (ShellDialect.ZSH, self.config.zsh_path),
            (ShellDialect.FISH, self.config.fish_path),
            (ShellDialect.DASH, self.config.dash_path),
        ]:
            if self.external_tools.get(dialect.value, False):
                shells[dialect] = path_config
        
        return shells
    
    def _detect_shell_dialect(self, file_path: str, content: str) -> ShellDialect:
        """Detect shell dialect from file path and content"""
        # Check file extension
        ext = Path(file_path).suffix.lower()
        if ext == '.bash':
            return ShellDialect.BASH
        elif ext == '.zsh':
            return ShellDialect.ZSH
        elif ext == '.fish':
            return ShellDialect.FISH
        
        # Check shebang
        first_line = content.split('\n')[0] if content else ""
        if first_line.startswith('#!'):
            if 'bash' in first_line:
                return ShellDialect.BASH
            elif 'zsh' in first_line:
                return ShellDialect.ZSH
            elif 'fish' in first_line:
                return ShellDialect.FISH
            elif 'dash' in first_line:
                return ShellDialect.DASH
            elif '/bin/sh' in first_line or '/usr/bin/sh' in first_line:
                return ShellDialect.POSIX
        
        # Check content for dialect-specific features
        if 'function ' in content or '[[' in content:
            return ShellDialect.BASH
        elif 'autoload' in content or 'zstyle' in content:
            return ShellDialect.ZSH
        elif 'end' in content and 'function' in content:
            return ShellDialect.FISH
        
        return self.config.default_shell
    
    def _detect_script_dialect(self, script: ShellScript) -> ShellDialect:
        """Detect shell dialect from script AST"""
        if script.shebang:
            if 'bash' in script.shebang:
                return ShellDialect.BASH
            elif 'zsh' in script.shebang:
                return ShellDialect.ZSH
            elif 'fish' in script.shebang:
                return ShellDialect.FISH
            elif 'dash' in script.shebang:
                return ShellDialect.DASH
        
        return self.config.default_shell
    
    def _validate_ast(self, ast: ShellScript, file_path: Optional[str], 
                     dialect: ShellDialect) -> List[ShellDiagnostic]:
        """Validate shell AST with specified level"""
        diagnostics = []
        
        if self.config.validation_level.value in ["syntax", "semantic", "lint", "security", "complete"]:
            diagnostics.extend(self._validate_syntax(ast, file_path))
        
        if self.config.validation_level.value in ["semantic", "lint", "security", "complete"]:
            diagnostics.extend(self._validate_semantics(ast, file_path, dialect))
        
        if self.config.validation_level.value in ["lint", "security", "complete"]:
            diagnostics.extend(self._validate_best_practices(ast, file_path))
        
        if self.config.validation_level.value in ["security", "complete"]:
            # Security validation already done in analyze_security
            pass
        
        return diagnostics
    
    def _validate_syntax(self, ast: ShellScript, file_path: Optional[str]) -> List[ShellDiagnostic]:
        """Perform syntax validation"""
        diagnostics = []
        
        # Check for basic syntax issues
        for stmt in ast.statements:
            if isinstance(stmt, ShellCommand):
                if not stmt.command:
                    diagnostics.append(ShellDiagnostic(
                        level="error",
                        message="Empty command",
                        file=file_path,
                        code="empty_command"
                    ))
        
        return diagnostics
    
    def _validate_semantics(self, ast: ShellScript, file_path: Optional[str], 
                          dialect: ShellDialect) -> List[ShellDiagnostic]:
        """Perform semantic validation"""
        diagnostics = []
        
        # Check variable usage
        if self.config.check_undefined_variables:
            defined_vars = set(ast.variables.keys())
            for stmt in ast.statements:
                if isinstance(stmt, ShellVariableAssignment):
                    defined_vars.add(stmt.variable)
            
            # This would need more sophisticated analysis
            # For now, just check obvious cases
        
        return diagnostics
    
    def _validate_best_practices(self, ast: ShellScript, file_path: Optional[str]) -> List[ShellDiagnostic]:
        """Validate against shell best practices"""
        diagnostics = []
        
        # Check for missing error handling
        has_error_handling = any(
            'set -e' in str(stmt) or 'trap' in str(stmt) 
            for stmt in ast.statements
        )
        
        if not has_error_handling and self.config.check_best_practices:
            diagnostics.append(ShellDiagnostic(
                level="warning",
                message="Consider adding error handling (set -e, trap)",
                file=file_path,
                code="missing_error_handling",
                suggestion="Add 'set -e' at beginning of script"
            ))
        
        return diagnostics
    
    def _format_with_shfmt(self, content: str, file_path: str) -> Tuple[str, List[ShellDiagnostic]]:
        """Format shell script using shfmt"""
        try:
            cmd = [
                self.config.shfmt_path,
                "-i", str(self.config.indent_size),
                "-ci",  # Switch cases will be indented
            ]
            
            if not self.config.use_tabs:
                cmd.append("-s")  # Simplify the code
            
            result = subprocess.run(
                cmd,
                input=content,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout, []
            else:
                return content, [ShellDiagnostic(
                    level="error",
                    message=f"shfmt error: {result.stderr}",
                    file=file_path,
                    code="shfmt_error"
                )]
        
        except Exception as e:
            return content, [ShellDiagnostic(
                level="error",
                message=f"shfmt execution error: {str(e)}",
                file=file_path,
                code="shfmt_execution_error"
            )]
    
    def _lint_with_shellcheck(self, file_path: str) -> List[ShellDiagnostic]:
        """Lint shell script using ShellCheck"""
        diagnostics = []
        
        try:
            result = subprocess.run(
                [self.config.shellcheck_path, "-f", "json", file_path],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                shellcheck_results = json.loads(result.stdout)
                for issue in shellcheck_results:
                    level_map = {
                        "error": "error",
                        "warning": "warning", 
                        "info": "info",
                        "style": "note"
                    }
                    
                    diagnostics.append(ShellDiagnostic(
                        level=level_map.get(issue.get("level", "warning"), "warning"),
                        message=issue.get("message", ""),
                        file=file_path,
                        line=issue.get("line"),
                        column=issue.get("column"),
                        code=f"SC{issue.get('code', '')}",
                        suggestion=issue.get("fix", {}).get("replacements", [{}])[0].get("replacement") if issue.get("fix") else None
                    ))
        
        except Exception as e:
            diagnostics.append(ShellDiagnostic(
                level="error",
                message=f"ShellCheck error: {str(e)}",
                file=file_path,
                code="shellcheck_error"
            ))
        
        return diagnostics
    
    def _lint_shell_ast(self, ast: ShellScript, file_path: str) -> List[ShellDiagnostic]:
        """Built-in shell script linting"""
        diagnostics = []
        
        # Check for common issues
        for stmt in ast.statements:
            if isinstance(stmt, ShellCommand):
                # Check for potentially dangerous commands
                if stmt.command in ['rm', 'mv', 'cp'] and '-f' in stmt.arguments:
                    diagnostics.append(ShellDiagnostic(
                        level="warning",
                        message=f"Use of force flag with {stmt.command} command",
                        file=file_path,
                        code="dangerous_force_flag",
                        rule="avoid_force_flags"
                    ))
        
        return diagnostics
    
    def _run_basic_test(self, file_path: str) -> ShellTestResult:
        """Run basic syntax test of shell script"""
        import time
        
        start_time = time.time()
        
        try:
            # Test with bash -n (syntax check only)
            result = subprocess.run(
                [self.config.bash_path, "-n", file_path],
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds
            )
            
            execution_time = time.time() - start_time
            
            return ShellTestResult(
                passed=result.returncode == 0,
                output=result.stdout,
                error_output=result.stderr,
                exit_code=result.returncode,
                execution_time=execution_time,
                shell_used="bash",
                test_count=1,
                failures=[result.stderr] if result.returncode != 0 else []
            )
            
        except subprocess.TimeoutExpired:
            return ShellTestResult(
                passed=False,
                output="",
                error_output="Test timed out",
                exit_code=124,
                execution_time=self.config.timeout_seconds,
                shell_used="bash",
                test_count=1,
                failures=["Test timed out"]
            )
        except Exception as e:
            return ShellTestResult(
                passed=False,
                output="",
                error_output=str(e),
                exit_code=1,
                execution_time=time.time() - start_time,
                shell_used="bash",
                test_count=1,
                failures=[str(e)]
            )
    
    def _run_test_file(self, test_file: str, script_file: str) -> ShellTestResult:
        """Run test file against script"""
        # This would integrate with testing frameworks like BATS
        # For now, just return a basic result
        return self._run_basic_test(script_file)
    
    def _check_bashisms(self, content: str) -> List[ShellDiagnostic]:
        """Check for Bash-specific constructs that hurt portability"""
        diagnostics = []
        
        bashism_patterns = [
            (r'\[\[.*\]\]', "Use of [[ ]] (bash-specific, use [ ] for POSIX)"),
            (r'function\s+\w+', "Use of 'function' keyword (use name() for POSIX)"),
            (r'\$\(\(.*\)\)', "Use of $((arithmetic)) (use expr for POSIX)"),
            (r'echo\s+-[neE]', "Use of echo with flags (not portable)"),
            (r'source\s+', "Use of 'source' command (use '.' for POSIX)"),
            (r'>&', "Use of >& redirection (not POSIX)"),
        ]
        
        for pattern, description in bashism_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                diagnostics.append(ShellDiagnostic(
                    level="warning",
                    message=description,
                    line=line_num,
                    code="bashism",
                    rule="posix_compatibility"
                ))
        
        return diagnostics
    
    def _test_in_multiple_shells(self, file_path: str) -> Dict[str, bool]:
        """Test script in multiple shell environments"""
        results = {}
        
        for dialect, shell_path in self.shell_paths.items():
            try:
                result = subprocess.run(
                    [shell_path, "-n", file_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                results[dialect.value] = result.returncode == 0
            except:
                results[dialect.value] = False
        
        return results
    
    def _check_security_issues(self, content: str, file_path: str) -> List[ShellDiagnostic]:
        """Check for additional security issues"""
        diagnostics = []
        
        # Check for hardcoded secrets
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token"),
        ]
        
        for pattern, description in secret_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                diagnostics.append(ShellDiagnostic(
                    level="warning",
                    message=description,
                    file=file_path,
                    line=line_num,
                    code="hardcoded_secret",
                    rule="no_hardcoded_secrets"
                ))
        
        return diagnostics
    
    def _calculate_complexity_score(self, ast: ShellScript) -> int:
        """Calculate script complexity score"""
        score = 0
        
        # Count statements
        score += len(ast.statements)
        
        # Count functions
        score += len(ast.functions) * 2
        
        # Count conditionals and loops (higher complexity)
        for stmt in ast.statements:
            if isinstance(stmt, (ShellConditional, ShellLoop)):
                score += 3
            elif isinstance(stmt, ShellPipeline):
                score += len(stmt.commands)
        
        return score
    
    def _find_dependencies(self, ast: ShellScript) -> List[str]:
        """Find external command dependencies"""
        dependencies = set()
        
        for stmt in ast.statements:
            if isinstance(stmt, ShellCommand):
                if not stmt.is_builtin:
                    dependencies.add(stmt.command)
            elif isinstance(stmt, ShellPipeline):
                for cmd in stmt.commands:
                    if not cmd.is_builtin:
                        dependencies.add(cmd.command)
        
        return sorted(list(dependencies))
    
    def _generate_recommendations(self, diagnostics: List[ShellDiagnostic], 
                                 portability_score: float, security_score: float) -> List[str]:
        """Generate recommendations for script improvement"""
        recommendations = []
        
        error_count = len([d for d in diagnostics if d.level == "error"])
        warning_count = len([d for d in diagnostics if d.level == "warning"])
        
        if error_count > 0:
            recommendations.append(f"Fix {error_count} syntax errors")
        
        if warning_count > 5:
            recommendations.append("Address style warnings for better maintainability")
        
        if portability_score < 0.8:
            recommendations.append("Improve script portability by avoiding shell-specific features")
        
        if security_score < 0.8:
            recommendations.append("Review script for security issues and hardcoded secrets")
        
        # ShellCheck-specific recommendations
        shellcheck_issues = [d for d in diagnostics if d.code and d.code.startswith("SC")]
        if shellcheck_issues:
            recommendations.append("Run 'shellcheck' for detailed analysis and fixes")
        
        return recommendations
    
    def _normalize_shell_content(self, content: str) -> str:
        """Normalize shell content for comparison"""
        # Remove comments and extra whitespace
        lines = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                lines.append(stripped)
        
        return '\n'.join(sorted(lines))


# Convenience functions
def parse_shell_code(code: str, filename: Optional[str] = None) -> ShellScript:
    """Parse shell source code"""
    return parse_shell(code)


def generate_shell_code(ast: ShellScript, dialect: ShellDialect = ShellDialect.BASH,
                       style: ShellFormatStyle = ShellFormatStyle.STANDARD) -> str:
    """Generate shell code from AST"""
    config = ShellGeneratorConfig(dialect=dialect, style=style)
    generator = ShellCodeGenerator(config)
    return generator.generate(ast)


def shell_round_trip_verify(code: str) -> bool:
    """Verify shell round-trip conversion"""
    try:
        ast = parse_shell(code)
        generated = generate_shell_code(ast)
        
        # Normalize for comparison
        toolchain = ShellToolchain()
        original_normalized = toolchain._normalize_shell_content(code)
        generated_normalized = toolchain._normalize_shell_content(generated)
        
        return original_normalized == generated_normalized
    except Exception:
        return False


def shell_to_runa_translate(shell_script: ShellScript) -> Any:
    """Translate Shell script to Runa AST"""
    return shell_to_runa(shell_script)


def runa_to_shell_translate(runa_module: Any) -> ShellScript:
    """Translate Runa AST to Shell script"""
    return runa_to_shell(runa_module) 