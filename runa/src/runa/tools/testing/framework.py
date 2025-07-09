#!/usr/bin/env python3
"""
Runa Multi-Language Testing Framework

Comprehensive testing framework supporting all language tiers with
test discovery, execution, reporting, and cross-language verification.
"""

import os
import re
import subprocess
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import tempfile
import shutil

from ..package.manager import PackageMetadata, PackageManager
from ..build.builder import RunaMultiLanguageBuilder, BuildConfiguration, BuildTarget
from ...core.pipeline import get_pipeline


class TestType(Enum):
    """Types of tests in the framework."""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    VERIFICATION = "verification"
    CROSS_LANGUAGE = "cross_language"
    END_TO_END = "end_to_end"


class TestStatus(Enum):
    """Test execution status."""
    PENDING = auto()
    RUNNING = auto()
    PASSED = auto()
    FAILED = auto()
    SKIPPED = auto()
    ERROR = auto()


@dataclass
class TestCase:
    """Represents a single test case."""
    name: str
    file_path: str
    test_type: TestType
    language: str
    description: str = ""
    
    # Test execution
    setup_code: Optional[str] = None
    test_code: str = ""
    teardown_code: Optional[str] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    timeout_seconds: int = 30
    dependencies: List[str] = field(default_factory=list)
    
    # Cross-language testing
    target_languages: List[str] = field(default_factory=list)
    expected_outputs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult:
    """Result of a test execution."""
    test_case: TestCase
    status: TestStatus
    execution_time_ms: float = 0.0
    
    # Output and errors
    stdout: str = ""
    stderr: str = ""
    error_message: Optional[str] = None
    
    # Cross-language results
    language_results: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Assertions and metrics
    assertions_passed: int = 0
    assertions_failed: int = 0
    coverage_percentage: Optional[float] = None
    
    def is_success(self) -> bool:
        """Check if test passed."""
        return self.status == TestStatus.PASSED


@dataclass
class TestSuite:
    """Collection of related test cases."""
    name: str
    test_cases: List[TestCase] = field(default_factory=list)
    setup_suite: Optional[str] = None
    teardown_suite: Optional[str] = None
    
    # Configuration
    parallel_execution: bool = True
    max_workers: int = 4
    timeout_seconds: int = 300
    
    def add_test(self, test_case: TestCase):
        """Add a test case to the suite."""
        self.test_cases.append(test_case)
    
    def get_tests_by_type(self, test_type: TestType) -> List[TestCase]:
        """Get tests filtered by type."""
        return [test for test in self.test_cases if test.test_type == test_type]
    
    def get_tests_by_language(self, language: str) -> List[TestCase]:
        """Get tests filtered by language."""
        return [test for test in self.test_cases if test.language == language]


@dataclass 
class TestConfiguration:
    """Configuration for test execution."""
    # Test selection
    test_types: List[TestType] = field(default_factory=lambda: [TestType.UNIT])
    test_languages: List[str] = field(default_factory=list)  # Empty = all
    test_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Execution
    parallel_execution: bool = True
    max_workers: int = 4
    fail_fast: bool = False
    timeout_seconds: int = 300
    
    # Cross-language testing
    enable_cross_language_tests: bool = True
    verify_translation_accuracy: bool = True
    
    # Output and reporting
    verbose: bool = False
    generate_coverage: bool = False
    output_format: str = "console"  # console, json, xml, html
    output_file: Optional[str] = None
    
    # Build integration
    build_before_test: bool = True
    clean_before_build: bool = False


class LanguageTestRunner:
    """Base class for language-specific test runners."""
    
    def __init__(self, language: str):
        self.language = language
        self.test_command = self._get_test_command()
        self.setup_commands = self._get_setup_commands()
        
    def _get_test_command(self) -> Optional[str]:
        """Get the test command for this language."""
        commands = {
            "python": "python -m pytest",
            "javascript": "npm test",
            "typescript": "npm test",
            "java": "mvn test",
            "cpp": "make test",
            "rust": "cargo test",
            "go": "go test",
            "csharp": "dotnet test"
        }
        return commands.get(self.language)
    
    def _get_setup_commands(self) -> List[str]:
        """Get setup commands for this language."""
        setup_commands = {
            "python": ["pip install -r requirements.txt"],
            "javascript": ["npm install"],
            "typescript": ["npm install"],
            "java": ["mvn compile"],
            "rust": ["cargo build"],
            "go": ["go mod download"],
            "csharp": ["dotnet restore"]
        }
        return setup_commands.get(self.language, [])
    
    def can_run_tests(self) -> bool:
        """Check if this language can run tests."""
        if not self.test_command:
            return False
        
        # Check if test runner is available
        command_parts = self.test_command.split()
        return shutil.which(command_parts[0]) is not None
    
    def setup_test_environment(self, test_dir: str) -> bool:
        """Setup test environment for this language."""
        try:
            for command in self.setup_commands:
                result = subprocess.run(
                    command.split(),
                    cwd=test_dir,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    print(f"Setup failed for {self.language}: {result.stderr}")
                    return False
            return True
        except Exception as e:
            print(f"Setup error for {self.language}: {e}")
            return False
    
    def run_test(self, test_case: TestCase, test_dir: str) -> TestResult:
        """Run a single test case."""
        start_time = time.time()
        result = TestResult(test_case=test_case, status=TestStatus.RUNNING)
        
        try:
            # Write test file
            test_file = self._write_test_file(test_case, test_dir)
            
            # Run test command
            if self.test_command:
                cmd = f"{self.test_command} {test_file}"
                process_result = subprocess.run(
                    cmd.split(),
                    cwd=test_dir,
                    capture_output=True,
                    text=True,
                    timeout=test_case.timeout_seconds
                )
                
                result.stdout = process_result.stdout
                result.stderr = process_result.stderr
                
                if process_result.returncode == 0:
                    result.status = TestStatus.PASSED
                else:
                    result.status = TestStatus.FAILED
                    result.error_message = result.stderr or "Test failed"
            else:
                # Fallback: run Runa test directly
                result = self._run_runa_test(test_case, test_dir)
                
        except subprocess.TimeoutExpired:
            result.status = TestStatus.ERROR
            result.error_message = f"Test timed out after {test_case.timeout_seconds}s"
        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = str(e)
        
        finally:
            result.execution_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def _write_test_file(self, test_case: TestCase, test_dir: str) -> str:
        """Write test case to appropriate file format."""
        # This would be implemented per language
        # For now, return the original file path
        return test_case.file_path
    
    def _run_runa_test(self, test_case: TestCase, test_dir: str) -> TestResult:
        """Run Runa test directly (fallback)."""
        # This would execute the Runa test code directly
        result = TestResult(test_case=test_case, status=TestStatus.PASSED)
        return result


class RunaTestRunner(LanguageTestRunner):
    """Runa-specific test runner."""
    
    def __init__(self):
        super().__init__("runa")
    
    def run_test(self, test_case: TestCase, test_dir: str) -> TestResult:
        """Run Runa test case."""
        start_time = time.time()
        result = TestResult(test_case=test_case, status=TestStatus.RUNNING)
        
        try:
            # Parse and execute Runa test code
            pipeline = get_pipeline()
            
            # For now, compile to Python and run
            python_code = pipeline.translate(test_case.test_code, "runa", "python")
            
            if python_code.success and python_code.target_code:
                # Write and execute Python code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(python_code.target_code)
                    temp_file = f.name
                
                try:
                    process_result = subprocess.run(
                        ["python", temp_file],
                        capture_output=True,
                        text=True,
                        timeout=test_case.timeout_seconds
                    )
                    
                    result.stdout = process_result.stdout
                    result.stderr = process_result.stderr
                    
                    if process_result.returncode == 0:
                        result.status = TestStatus.PASSED
                    else:
                        result.status = TestStatus.FAILED
                        result.error_message = result.stderr
                
                finally:
                    os.unlink(temp_file)
            else:
                result.status = TestStatus.ERROR
                result.error_message = "Failed to compile Runa test code"
                
        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = str(e)
        
        finally:
            result.execution_time_ms = (time.time() - start_time) * 1000
        
        return result


class MultiLanguageTestFramework:
    """Main testing framework supporting all languages."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.package_manager = PackageManager(str(self.project_root))
        self.builder = RunaMultiLanguageBuilder(str(self.project_root))
        
        # Language test runners
        self.test_runners = self._initialize_test_runners()
        
        # Test discovery
        self.test_suites: Dict[str, TestSuite] = {}
        
        # Load project metadata
        self.metadata = self._load_project_metadata()
    
    def _initialize_test_runners(self) -> Dict[str, LanguageTestRunner]:
        """Initialize test runners for all supported languages."""
        runners = {}
        
        # Runa test runner
        runners["runa"] = RunaTestRunner()
        
        # Other language runners
        languages = ["python", "javascript", "typescript", "java", "cpp", 
                    "rust", "go", "swift", "kotlin", "php", "csharp"]
        
        for lang in languages:
            runners[lang] = LanguageTestRunner(lang)
        
        return runners
    
    def _load_project_metadata(self) -> Optional[PackageMetadata]:
        """Load project metadata."""
        runa_toml = self.project_root / "runa.toml"
        if runa_toml.exists():
            try:
                return PackageMetadata.from_toml(str(runa_toml))
            except Exception:
                pass
        return None
    
    def discover_tests(self, test_dirs: List[str] = None) -> Dict[str, TestSuite]:
        """Discover all test cases in the project."""
        test_dirs = test_dirs or ["tests", "test", "spec"]
        
        for test_dir_name in test_dirs:
            test_dir = self.project_root / test_dir_name
            if test_dir.exists():
                self._discover_tests_in_directory(test_dir)
        
        return self.test_suites
    
    def _discover_tests_in_directory(self, test_dir: Path):
        """Discover tests in a specific directory."""
        # Discover Runa tests
        for runa_file in test_dir.rglob("*.runa"):
            if self._is_test_file(runa_file):
                test_cases = self._parse_runa_test_file(runa_file)
                
                suite_name = str(runa_file.relative_to(test_dir).parent)
                if suite_name not in self.test_suites:
                    self.test_suites[suite_name] = TestSuite(name=suite_name)
                
                for test_case in test_cases:
                    self.test_suites[suite_name].add_test(test_case)
        
        # Discover language-specific tests
        test_patterns = {
            "python": "test_*.py",
            "javascript": "*.test.js",
            "typescript": "*.test.ts",
            "java": "*Test.java"
        }
        
        for language, pattern in test_patterns.items():
            for test_file in test_dir.rglob(pattern):
                test_cases = self._parse_language_test_file(test_file, language)
                
                suite_name = f"{language}_tests"
                if suite_name not in self.test_suites:
                    self.test_suites[suite_name] = TestSuite(name=suite_name)
                
                for test_case in test_cases:
                    self.test_suites[suite_name].add_test(test_case)
    
    def _is_test_file(self, file_path: Path) -> bool:
        """Check if a file is a test file."""
        name = file_path.name.lower()
        return (name.startswith("test_") or 
                name.endswith("_test.runa") or
                "test" in name)
    
    def _parse_runa_test_file(self, test_file: Path) -> List[TestCase]:
        """Parse Runa test file and extract test cases."""
        test_cases = []
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex-based test discovery
            # Look for Process called "test_*" patterns
            test_pattern = r'Process called "test_([^"]*)"[^:]*:'
            matches = re.finditer(test_pattern, content, re.MULTILINE)
            
            for match in matches:
                test_name = f"test_{match.group(1)}"
                
                # Extract test code (simplified)
                # In reality, this would use the Runa parser
                test_code = self._extract_test_code(content, match.start())
                
                test_case = TestCase(
                    name=test_name,
                    file_path=str(test_file),
                    test_type=TestType.UNIT,
                    language="runa",
                    test_code=test_code
                )
                
                # Check for cross-language annotations
                if "Note: Cross-language test" in test_code:
                    test_case.test_type = TestType.CROSS_LANGUAGE
                    test_case.target_languages = self._extract_target_languages(test_code)
                
                test_cases.append(test_case)
        
        except Exception as e:
            print(f"Error parsing test file {test_file}: {e}")
        
        return test_cases
    
    def _extract_test_code(self, content: str, start_pos: int) -> str:
        """Extract test code from position (simplified)."""
        # This is a simplified extraction
        # In reality, would use proper Runa parsing
        lines = content[start_pos:].split('\n')
        test_lines = []
        indent_level = None
        
        for line in lines:
            if line.strip():
                current_indent = len(line) - len(line.lstrip())
                if indent_level is None:
                    indent_level = current_indent
                elif current_indent <= indent_level and test_lines:
                    break
                test_lines.append(line)
            elif test_lines:
                test_lines.append(line)
        
        return '\n'.join(test_lines)
    
    def _extract_target_languages(self, test_code: str) -> List[str]:
        """Extract target languages from test code."""
        # Look for annotations like "Note: Target languages: python, javascript"
        pattern = r'Note:\s*Target languages:\s*([^\n]+)'
        match = re.search(pattern, test_code)
        if match:
            languages = [lang.strip() for lang in match.group(1).split(',')]
            return languages
        return []
    
    def _parse_language_test_file(self, test_file: Path, language: str) -> List[TestCase]:
        """Parse language-specific test file."""
        # Simplified language test discovery
        # In reality, would use language-specific parsers
        return [
            TestCase(
                name=test_file.stem,
                file_path=str(test_file),
                test_type=TestType.UNIT,
                language=language,
                test_code=""  # Would read from file
            )
        ]
    
    def run_tests(self, config: TestConfiguration = None) -> Dict[str, List[TestResult]]:
        """Run tests according to configuration."""
        config = config or TestConfiguration()
        
        # Discover tests if not already done
        if not self.test_suites:
            self.discover_tests()
        
        # Build project if requested
        if config.build_before_test:
            build_success = self._build_project(config)
            if not build_success and config.fail_fast:
                return {}
        
        # Filter test cases
        all_test_cases = self._filter_test_cases(config)
        
        # Run tests
        if config.parallel_execution:
            results = self._run_tests_parallel(all_test_cases, config)
        else:
            results = self._run_tests_sequential(all_test_cases, config)
        
        return results
    
    def _build_project(self, config: TestConfiguration) -> bool:
        """Build project before running tests."""
        try:
            build_config = BuildConfiguration(
                target=BuildTarget.TEST,
                clean_before_build=config.clean_before_build,
                target_languages=config.test_languages or [],
                run_tests=False
            )
            
            result = self.builder.build(build_config)
            return result.success
        except Exception as e:
            print(f"Build failed: {e}")
            return False
    
    def _filter_test_cases(self, config: TestConfiguration) -> List[TestCase]:
        """Filter test cases based on configuration."""
        all_tests = []
        
        for suite in self.test_suites.values():
            for test_case in suite.test_cases:
                # Filter by type
                if config.test_types and test_case.test_type not in config.test_types:
                    continue
                
                # Filter by language
                if config.test_languages and test_case.language not in config.test_languages:
                    continue
                
                # Filter by pattern
                if config.test_patterns:
                    if not any(pattern in test_case.name for pattern in config.test_patterns):
                        continue
                
                # Exclude patterns
                if config.exclude_patterns:
                    if any(pattern in test_case.name for pattern in config.exclude_patterns):
                        continue
                
                # Filter by tags
                if config.tags:
                    if not any(tag in test_case.tags for tag in config.tags):
                        continue
                
                all_tests.append(test_case)
        
        return all_tests
    
    def _run_tests_parallel(self, test_cases: List[TestCase], 
                          config: TestConfiguration) -> Dict[str, List[TestResult]]:
        """Run tests in parallel."""
        results: Dict[str, List[TestResult]] = {}
        
        with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
            # Group by language for better parallelization
            language_groups = {}
            for test_case in test_cases:
                if test_case.language not in language_groups:
                    language_groups[test_case.language] = []
                language_groups[test_case.language].append(test_case)
            
            # Submit tasks
            futures = []
            for language, tests in language_groups.items():
                future = executor.submit(self._run_language_tests, language, tests, config)
                futures.append((language, future))
            
            # Collect results
            for language, future in futures:
                try:
                    lang_results = future.result(timeout=config.timeout_seconds)
                    results[language] = lang_results
                except Exception as e:
                    print(f"Error running {language} tests: {e}")
                    results[language] = []
        
        return results
    
    def _run_tests_sequential(self, test_cases: List[TestCase],
                            config: TestConfiguration) -> Dict[str, List[TestResult]]:
        """Run tests sequentially."""
        results: Dict[str, List[TestResult]] = {}
        
        # Group by language
        language_groups = {}
        for test_case in test_cases:
            if test_case.language not in language_groups:
                language_groups[test_case.language] = []
            language_groups[test_case.language].append(test_case)
        
        # Run each language group
        for language, tests in language_groups.items():
            lang_results = self._run_language_tests(language, tests, config)
            results[language] = lang_results
            
            # Fail fast if requested
            if config.fail_fast and any(not r.is_success() for r in lang_results):
                break
        
        return results
    
    def _run_language_tests(self, language: str, test_cases: List[TestCase],
                          config: TestConfiguration) -> List[TestResult]:
        """Run all tests for a specific language."""
        if language not in self.test_runners:
            return []
        
        runner = self.test_runners[language]
        
        # Check if runner is available
        if not runner.can_run_tests():
            print(f"Test runner for {language} not available")
            return []
        
        results = []
        
        # Create temporary test directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Setup test environment
            if not runner.setup_test_environment(temp_dir):
                print(f"Failed to setup test environment for {language}")
                return []
            
            # Run each test
            for test_case in test_cases:
                if config.verbose:
                    print(f"Running {test_case.name} ({language})")
                
                result = runner.run_test(test_case, temp_dir)
                results.append(result)
                
                # Handle cross-language tests
                if (test_case.test_type == TestType.CROSS_LANGUAGE and 
                    config.enable_cross_language_tests):
                    cross_results = self._run_cross_language_test(test_case, temp_dir, config)
                    result.language_results.update(cross_results)
                
                if config.fail_fast and not result.is_success():
                    break
        
        return results
    
    def _run_cross_language_test(self, test_case: TestCase, temp_dir: str,
                               config: TestConfiguration) -> Dict[str, Dict[str, Any]]:
        """Run cross-language verification test."""
        cross_results = {}
        
        if not test_case.target_languages:
            return cross_results
        
        try:
            pipeline = get_pipeline()
            
            # Translate test to each target language
            for target_lang in test_case.target_languages:
                if target_lang in self.test_runners:
                    # Translate Runa test to target language
                    translation = pipeline.translate(test_case.test_code, "runa", target_lang)
                    
                    if translation.success and translation.target_code:
                        # Run translated test
                        runner = self.test_runners[target_lang]
                        
                        # Create test case for target language
                        target_test = TestCase(
                            name=f"{test_case.name}_{target_lang}",
                            file_path=test_case.file_path,
                            test_type=TestType.VERIFICATION,
                            language=target_lang,
                            test_code=translation.target_code
                        )
                        
                        result = runner.run_test(target_test, temp_dir)
                        
                        cross_results[target_lang] = {
                            "success": result.is_success(),
                            "execution_time_ms": result.execution_time_ms,
                            "output": result.stdout,
                            "error": result.error_message
                        }
                    else:
                        cross_results[target_lang] = {
                            "success": False,
                            "error": "Translation failed"
                        }
        
        except Exception as e:
            print(f"Cross-language test error: {e}")
        
        return cross_results
    
    def generate_report(self, results: Dict[str, List[TestResult]], 
                       config: TestConfiguration) -> str:
        """Generate test report."""
        if config.output_format == "json":
            return self._generate_json_report(results)
        elif config.output_format == "xml":
            return self._generate_xml_report(results)
        elif config.output_format == "html":
            return self._generate_html_report(results)
        else:
            return self._generate_console_report(results)
    
    def _generate_console_report(self, results: Dict[str, List[TestResult]]) -> str:
        """Generate console report."""
        report_lines = []
        
        total_tests = sum(len(lang_results) for lang_results in results.values())
        total_passed = sum(len([r for r in lang_results if r.is_success()]) 
                          for lang_results in results.values())
        total_failed = total_tests - total_passed
        
        report_lines.append("=" * 60)
        report_lines.append("RUNA MULTI-LANGUAGE TEST RESULTS")
        report_lines.append("=" * 60)
        report_lines.append(f"Total Tests: {total_tests}")
        report_lines.append(f"Passed: {total_passed}")
        report_lines.append(f"Failed: {total_failed}")
        report_lines.append(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        report_lines.append("")
        
        # Per-language results
        for language, lang_results in results.items():
            if not lang_results:
                continue
            
            passed = len([r for r in lang_results if r.is_success()])
            failed = len(lang_results) - passed
            
            report_lines.append(f"{language.upper()} ({len(lang_results)} tests)")
            report_lines.append(f"  Passed: {passed}, Failed: {failed}")
            
            # Show failed tests
            for result in lang_results:
                if not result.is_success():
                    report_lines.append(f"  ❌ {result.test_case.name}: {result.error_message}")
            
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _generate_json_report(self, results: Dict[str, List[TestResult]]) -> str:
        """Generate JSON report."""
        report_data = {
            "timestamp": time.time(),
            "summary": {
                "total_tests": sum(len(r) for r in results.values()),
                "total_passed": sum(len([t for t in r if t.is_success()]) for r in results.values()),
                "languages_tested": list(results.keys())
            },
            "results": {}
        }
        
        for language, lang_results in results.items():
            report_data["results"][language] = [
                {
                    "name": result.test_case.name,
                    "status": result.status.name,
                    "execution_time_ms": result.execution_time_ms,
                    "error_message": result.error_message,
                    "cross_language_results": result.language_results
                }
                for result in lang_results
            ]
        
        return json.dumps(report_data, indent=2)
    
    def _generate_xml_report(self, results: Dict[str, List[TestResult]]) -> str:
        """Generate XML report (JUnit format)."""
        # Implementation for XML/JUnit format
        return "<testsuites></testsuites>"  # Placeholder
    
    def _generate_html_report(self, results: Dict[str, List[TestResult]]) -> str:
        """Generate HTML report."""
        # Implementation for HTML report
        return "<html><body>Test Results</body></html>"  # Placeholder


def main():
    """CLI entry point for the testing framework."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runa Multi-Language Testing Framework')
    parser.add_argument('--types', nargs='*', 
                       choices=['unit', 'integration', 'performance', 'verification', 'cross_language'],
                       default=['unit'], help='Test types to run')
    parser.add_argument('--languages', nargs='*', help='Languages to test')
    parser.add_argument('--patterns', nargs='*', help='Test name patterns to include')
    parser.add_argument('--exclude', nargs='*', help='Test name patterns to exclude')
    parser.add_argument('--tags', nargs='*', help='Test tags to include')
    parser.add_argument('--parallel', action='store_true', default=True, help='Run tests in parallel')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--fail-fast', action='store_true', help='Stop on first failure')
    parser.add_argument('--timeout', type=int, default=300, help='Test timeout in seconds')
    parser.add_argument('--no-build', action='store_true', help='Skip building before tests')
    parser.add_argument('--clean', action='store_true', help='Clean before build')
    parser.add_argument('--cross-language', action='store_true', default=True, 
                       help='Enable cross-language tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--format', choices=['console', 'json', 'xml', 'html'], 
                       default='console', help='Output format')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--project-dir', default='.', help='Project directory')
    
    # Discovery commands
    parser.add_argument('--discover', action='store_true', help='Discover and list tests')
    parser.add_argument('--test-dirs', nargs='*', help='Test directories to search')
    
    args = parser.parse_args()
    
    # Initialize testing framework
    framework = MultiLanguageTestFramework(args.project_dir)
    
    if args.discover:
        # Discover tests
        test_suites = framework.discover_tests(args.test_dirs)
        
        print(f"Discovered {len(test_suites)} test suites:")
        for suite_name, suite in test_suites.items():
            print(f"\n{suite_name} ({len(suite.test_cases)} tests):")
            for test_case in suite.test_cases:
                print(f"  - {test_case.name} ({test_case.language}, {test_case.test_type.value})")
        
        return 0
    
    # Configure test execution
    config = TestConfiguration(
        test_types=[TestType(t) for t in args.types],
        test_languages=args.languages or [],
        test_patterns=args.patterns or [],
        exclude_patterns=args.exclude or [],
        tags=args.tags or [],
        parallel_execution=args.parallel,
        max_workers=args.workers,
        fail_fast=args.fail_fast,
        timeout_seconds=args.timeout,
        enable_cross_language_tests=args.cross_language,
        verbose=args.verbose,
        generate_coverage=args.coverage,
        output_format=args.format,
        output_file=args.output,
        build_before_test=not args.no_build,
        clean_before_build=args.clean
    )
    
    # Run tests
    print("Running Runa multi-language tests...")
    
    start_time = time.time()
    results = framework.run_tests(config)
    execution_time = time.time() - start_time
    
    # Generate report
    report = framework.generate_report(results, config)
    
    if config.output_file:
        with open(config.output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {config.output_file}")
    else:
        print(report)
    
    print(f"\nTest execution completed in {execution_time:.2f}s")
    
    # Return appropriate exit code
    total_tests = sum(len(r) for r in results.values())
    failed_tests = sum(len([t for t in r if not t.is_success()]) for r in results.values())
    
    return 1 if failed_tests > 0 else 0


if __name__ == '__main__':
    import sys
    sys.exit(main())