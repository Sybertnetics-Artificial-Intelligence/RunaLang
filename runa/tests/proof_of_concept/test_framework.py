"""
Runa Proof of Concept Test Framework
===================================

This framework orchestrates comprehensive tests that showcase Runa's capabilities
across all languages. It accepts test cases provided by the user and runs them
through the complete translation pipeline with full artifact capture.

Features:
- Complete pipeline integration (7 stages)
- Cross-language translation testing
- Round-trip verification
- Semantic preservation analysis
- Performance benchmarking
- Detailed output capture and organization
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import time
import logging
import traceback
from datetime import datetime
import sys
import os

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from runa.core.pipeline import TranslationPipeline, PipelineStage, TranslationResult
from runa.core.verification import VerificationResult


class TestComplexity(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXTREME = "extreme"
    BREAKING = "breaking"


class TestType(Enum):
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    ROUNDTRIP = "roundtrip"
    CROSS_LANGUAGE = "cross_language"
    CROSS_DOMAIN = "cross_domain"
    FEATURE_SHOWCASE = "feature_showcase"
    EDGE_CASE = "edge_case"
    PERFORMANCE = "performance"


@dataclass
class TestCase:
    """A comprehensive test case definition."""
    name: str
    description: str
    complexity: TestComplexity
    test_type: TestType
    source_language: str
    target_languages: List[str]
    source_code: str
    expected_behavior: str
    known_issues: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    expected_runa: Optional[str] = None


@dataclass
class TestExecution:
    """Results from executing a single test case."""
    test_case: TestCase
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = False
    error_message: Optional[str] = None
    
    # Pipeline results for each target language
    translation_results: Dict[str, TranslationResult] = field(default_factory=dict)
    
    # Captured artifacts (saved to files)
    artifacts: Dict[str, str] = field(default_factory=dict)
    
    # Performance metrics
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Verification results
    verification_results: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_ms(self) -> float:
        """Calculate test duration in milliseconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of test execution."""
        return {
            "name": self.test_case.name,
            "success": self.success,
            "duration_ms": self.duration_ms,
            "source_language": self.test_case.source_language,
            "target_languages": list(self.translation_results.keys()),
            "successful_translations": [
                lang for lang, result in self.translation_results.items() 
                if result.success
            ],
            "failed_translations": [
                lang for lang, result in self.translation_results.items() 
                if not result.success
            ],
            "error_message": self.error_message,
            "artifacts_count": len(self.artifacts),
            "complexity": self.test_case.complexity.value,
            "test_type": self.test_case.test_type.value
        }


class ProofOfConceptTestFramework:
    """Main test framework for proof of concept demonstrations."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize the test framework."""
        self.output_dir = output_dir or Path(__file__).parent / "outputs"
        self.reports_dir = Path(__file__).parent / "reports"
        
        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize pipeline
        self.pipeline = TranslationPipeline()
        
        # Test execution tracking
        self.executions: List[TestExecution] = []
        
        # Setup logging
        self._setup_logging()
        
        # Initialize language toolchains
        self._initialize_toolchains()
    
    def _setup_logging(self):
        """Setup comprehensive logging."""
        log_file = self.reports_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Test framework initialized. Logs: {log_file}")
    
    def _initialize_toolchains(self):
        """Initialize and register all available language toolchains."""
        self.logger.info("Initializing language toolchains...")
        
        # This will be implemented to auto-discover and register all available toolchains
        # For now, we'll track which languages are available
        self.available_languages = set()
        
        try:
            # Try to register common Tier 1 languages
            self._try_register_language("python")
            self._try_register_language("javascript")
            self._try_register_language("typescript")
            self._try_register_language("java")
            self._try_register_language("csharp")
            self._try_register_language("cpp")
            self._try_register_language("sql")
            self._try_register_language("runa")
            
        except Exception as e:
            self.logger.warning(f"Error during toolchain initialization: {e}")
        
        self.logger.info(f"Available languages: {sorted(self.available_languages)}")
    
    def _try_register_language(self, language: str):
        """Try to register a specific language toolchain."""
        try:
            # This will be implemented to actually register the toolchains
            # For now, we'll just track available languages
            self.available_languages.add(language)
            self.logger.debug(f"Language {language} marked as available")
        except Exception as e:
            self.logger.warning(f"Failed to register {language}: {e}")
    
    def execute_test_case(self, test_case: TestCase) -> TestExecution:
        """Execute a single comprehensive test case."""
        execution = TestExecution(
            test_case=test_case,
            start_time=datetime.now()
        )
        
        self.logger.info(f"🔄 Executing test: {test_case.name}")
        self.logger.info(f"   Source: {test_case.source_language}")
        self.logger.info(f"   Targets: {', '.join(test_case.target_languages)}")
        self.logger.info(f"   Complexity: {test_case.complexity.value}")
        
        try:
            # Create test-specific output directory
            test_output_dir = self._create_test_output_dir(test_case)
            
            # Save original source code
            source_file = test_output_dir / f"01_source.{self._get_file_extension(test_case.source_language)}"
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(test_case.source_code)
            execution.artifacts["source_code"] = str(source_file)
            
            # Execute translation for each target language
            for target_lang in test_case.target_languages:
                self.logger.info(f"   🔄 Translating to {target_lang}...")
                
                try:
                    # Execute translation through pipeline
                    translation_start = time.time()
                    
                    result = self.pipeline.translate(
                        source_code=test_case.source_code,
                        source_language=test_case.source_language,
                        target_language=target_lang,
                        file_path=f"test_{test_case.name}",
                        verify_round_trip=test_case.test_type == TestType.ROUNDTRIP
                    )
                    
                    translation_time = (time.time() - translation_start) * 1000
                    execution.performance_metrics[f"{target_lang}_translation_ms"] = translation_time
                    execution.translation_results[target_lang] = result
                    
                    # Save all pipeline artifacts
                    self._save_pipeline_artifacts(test_case, target_lang, result, test_output_dir)
                    
                    if result.success:
                        self.logger.info(f"   ✅ {target_lang} translation successful ({translation_time:.1f}ms)")
                    else:
                        self.logger.warning(f"   ❌ {target_lang} translation failed: {result.error_message}")
                
                except Exception as e:
                    self.logger.error(f"   ❌ {target_lang} translation error: {e}")
                    execution.translation_results[target_lang] = TranslationResult(
                        success=False,
                        source_language=test_case.source_language,
                        target_language=target_lang,
                        source_code=test_case.source_code,
                        error_message=str(e)
                    )
            
            # Perform additional verification if requested
            if test_case.test_type == TestType.ROUNDTRIP:
                execution.verification_results.update(
                    self._perform_roundtrip_verification(test_case, execution)
                )
            
            # Calculate overall success
            successful_translations = sum(1 for r in execution.translation_results.values() if r.success)
            total_translations = len(execution.translation_results)
            execution.success = successful_translations > 0  # At least one successful translation
            
            # Generate test summary
            summary = self._generate_test_summary(execution)
            summary_file = test_output_dir / "test_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, default=str)
            execution.artifacts["summary"] = str(summary_file)
            
            self.logger.info(f"   🎉 Test completed: {successful_translations}/{total_translations} translations successful")
            
        except Exception as e:
            execution.success = False
            execution.error_message = str(e)
            self.logger.error(f"   ❌ Test execution failed: {e}")
            self.logger.debug(traceback.format_exc())
        
        finally:
            execution.end_time = datetime.now()
            self.executions.append(execution)
        
        return execution
    
    def execute_test_batch(self, test_cases: List[TestCase]) -> List[TestExecution]:
        """Execute a batch of test cases."""
        self.logger.info(f"🚀 Starting batch execution of {len(test_cases)} test cases")
        
        batch_start = time.time()
        executions = []
        
        for i, test_case in enumerate(test_cases, 1):
            self.logger.info(f"📋 Test {i}/{len(test_cases)}: {test_case.name}")
            
            execution = self.execute_test_case(test_case)
            executions.append(execution)
            
            # Brief pause between tests
            time.sleep(0.1)
        
        batch_time = (time.time() - batch_start) / 60  # minutes
        self.logger.info(f"🏁 Batch execution completed in {batch_time:.2f} minutes")
        
        # Generate batch report
        self._generate_batch_report(executions)
        
        return executions
    
    def _create_test_output_dir(self, test_case: TestCase) -> Path:
        """Create output directory for a specific test."""
        # Organize by tier and language
        tier = self._get_language_tier(test_case.source_language)
        test_dir = self.output_dir / tier / test_case.source_language / test_case.name
        test_dir.mkdir(parents=True, exist_ok=True)
        return test_dir
    
    def _get_language_tier(self, language: str) -> str:
        """Get the tier directory for a language."""
        tier1 = ["python", "javascript", "typescript", "java", "csharp", "cpp", "sql"]
        tier2 = ["go", "rust", "kotlin", "swift", "scala", "php", "webassembly"]
        tier3 = ["html", "css", "json", "yaml", "xml", "shell", "lua", "toml", "ini", "hcl", "assemblyscript"]
        
        if language in tier1:
            return "tier1"
        elif language in tier2:
            return "tier2"
        elif language in tier3:
            return "tier3"
        elif language == "runa":
            return "tier1"  # Runa is core, put in tier1
        else:
            return "tier4"  # Default for other languages
    
    def _get_file_extension(self, language: str) -> str:
        """Get appropriate file extension for a language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "csharp": "cs",
            "cpp": "cpp",
            "sql": "sql",
            "runa": "runa",
            "go": "go",
            "rust": "rs",
            "kotlin": "kt",
            "swift": "swift",
            "php": "php",
            "html": "html",
            "css": "css",
            "json": "json",
            "yaml": "yaml",
            "xml": "xml",
            "shell": "sh"
        }
        return extensions.get(language, "txt")
    
    def _save_pipeline_artifacts(self, test_case: TestCase, target_lang: str, 
                                result: TranslationResult, output_dir: Path):
        """Save all pipeline artifacts for detailed analysis."""
        try:
            base_name = f"{target_lang}_"
            
            # Save each checkpoint
            for i, checkpoint in enumerate(result.checkpoints, 2):
                stage_name = checkpoint.stage.name.lower()
                
                if checkpoint.is_code():
                    # Save code content
                    if checkpoint.stage == PipelineStage.RUNA_CODE:
                        filename = f"{base_name}04_runa_code.runa"
                    elif checkpoint.stage == PipelineStage.TARGET_CODE:
                        ext = self._get_file_extension(target_lang)
                        filename = f"{base_name}07_target_code.{ext}"
                    else:
                        filename = f"{base_name}{i:02d}_{stage_name}.txt"
                    
                    file_path = output_dir / filename
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(checkpoint.content)
                
                elif checkpoint.is_ast():
                    # Save AST as JSON
                    if checkpoint.stage == PipelineStage.SOURCE_AST:
                        filename = f"{base_name}02_source_ast.json"
                    elif checkpoint.stage == PipelineStage.RUNA_AST_CHECKPOINT_1:
                        filename = f"{base_name}03_runa_ast_1.json"
                    elif checkpoint.stage == PipelineStage.RUNA_AST_CHECKPOINT_2:
                        filename = f"{base_name}05_runa_ast_2.json"
                    elif checkpoint.stage == PipelineStage.TARGET_AST:
                        filename = f"{base_name}06_target_ast.json"
                    else:
                        filename = f"{base_name}{i:02d}_{stage_name}_ast.json"
                    
                    file_path = output_dir / filename
                    with open(file_path, 'w', encoding='utf-8') as f:
                        # Serialize AST (this will need proper AST serialization)
                        ast_data = {
                            "type": checkpoint.content.__class__.__name__,
                            "stage": stage_name,
                            "metadata": checkpoint.metadata,
                            "timestamp": checkpoint.timestamp.isoformat()
                        }
                        json.dump(ast_data, f, indent=2, default=str)
            
            # Save translation metadata
            metadata_file = output_dir / f"{base_name}translation_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                metadata = {
                    "success": result.success,
                    "source_language": result.source_language,
                    "target_language": result.target_language,
                    "total_time_ms": result.total_time_ms,
                    "confidence_score": result.confidence_score,
                    "error_message": result.error_message,
                    "checkpoints_count": len(result.checkpoints),
                    "verification_results": {
                        k: {
                            "is_identical": v.is_identical,
                            "differences_count": len(v.differences),
                            "confidence": v.confidence
                        }
                        for k, v in result.verification_results.items()
                    }
                }
                json.dump(metadata, f, indent=2, default=str)
        
        except Exception as e:
            self.logger.warning(f"Failed to save artifacts for {target_lang}: {e}")
    
    def _perform_roundtrip_verification(self, test_case: TestCase, 
                                      execution: TestExecution) -> Dict[str, Any]:
        """Perform comprehensive round-trip verification."""
        verification_results = {}
        
        try:
            # Check if we have successful translations
            successful_translations = [
                (lang, result) for lang, result in execution.translation_results.items()
                if result.success
            ]
            
            if not successful_translations:
                return {"error": "No successful translations for round-trip verification"}
            
            # Perform round-trip through Runa for each successful translation
            for target_lang, translation_result in successful_translations:
                if translation_result.target_code:
                    try:
                        # Translate back to original language through Runa
                        roundtrip_result = self.pipeline.translate(
                            source_code=translation_result.target_code,
                            source_language=target_lang,
                            target_language=test_case.source_language,
                            verify_round_trip=True
                        )
                        
                        verification_results[f"{target_lang}_roundtrip"] = {
                            "success": roundtrip_result.success,
                            "semantic_preservation": roundtrip_result.confidence_score,
                            "error_message": roundtrip_result.error_message
                        }
                        
                    except Exception as e:
                        verification_results[f"{target_lang}_roundtrip"] = {
                            "success": False,
                            "error": str(e)
                        }
        
        except Exception as e:
            verification_results["verification_error"] = str(e)
        
        return verification_results
    
    def _generate_test_summary(self, execution: TestExecution) -> Dict[str, Any]:
        """Generate comprehensive test summary."""
        return {
            "test_case": {
                "name": execution.test_case.name,
                "description": execution.test_case.description,
                "complexity": execution.test_case.complexity.value,
                "test_type": execution.test_case.test_type.value,
                "source_language": execution.test_case.source_language,
                "target_languages": execution.test_case.target_languages,
                "expected_behavior": execution.test_case.expected_behavior,
                "known_issues": execution.test_case.known_issues,
                "metadata": execution.test_case.metadata
            },
            "execution": {
                "start_time": execution.start_time.isoformat(),
                "end_time": execution.end_time.isoformat() if execution.end_time else None,
                "duration_ms": execution.duration_ms,
                "success": execution.success,
                "error_message": execution.error_message
            },
            "translation_results": {
                lang: {
                    "success": result.success,
                    "total_time_ms": result.total_time_ms,
                    "confidence_score": result.confidence_score,
                    "checkpoints_count": len(result.checkpoints),
                    "error_message": result.error_message
                }
                for lang, result in execution.translation_results.items()
            },
            "performance_metrics": execution.performance_metrics,
            "verification_results": execution.verification_results,
            "artifacts": execution.artifacts
        }
    
    def _generate_batch_report(self, executions: List[TestExecution]):
        """Generate comprehensive batch execution report."""
        report_file = self.reports_dir / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Calculate statistics
        total_tests = len(executions)
        successful_tests = sum(1 for e in executions if e.success)
        total_translations = sum(len(e.translation_results) for e in executions)
        successful_translations = sum(
            sum(1 for r in e.translation_results.values() if r.success)
            for e in executions
        )
        
        # Group by complexity and type
        by_complexity = {}
        by_type = {}
        by_source_lang = {}
        
        for execution in executions:
            tc = execution.test_case
            
            by_complexity.setdefault(tc.complexity.value, []).append(execution)
            by_type.setdefault(tc.test_type.value, []).append(execution)
            by_source_lang.setdefault(tc.source_language, []).append(execution)
        
        # Generate report
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "framework_version": "1.0.0",
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
                "total_translations": total_translations,
                "successful_translations": successful_translations,
                "translation_success_rate": successful_translations / total_translations if total_translations > 0 else 0
            },
            "statistics": {
                "by_complexity": {
                    complexity: {
                        "count": len(execs),
                        "success_rate": sum(1 for e in execs if e.success) / len(execs) if execs else 0
                    }
                    for complexity, execs in by_complexity.items()
                },
                "by_test_type": {
                    test_type: {
                        "count": len(execs),
                        "success_rate": sum(1 for e in execs if e.success) / len(execs) if execs else 0
                    }
                    for test_type, execs in by_type.items()
                },
                "by_source_language": {
                    lang: {
                        "count": len(execs),
                        "success_rate": sum(1 for e in execs if e.success) / len(execs) if execs else 0
                    }
                    for lang, execs in by_source_lang.items()
                }
            },
            "test_summaries": [execution.get_summary() for execution in executions]
        }
        
        # Save report
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"📊 Batch report saved: {report_file}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("🎯 PROOF OF CONCEPT TEST RESULTS SUMMARY")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Successful Tests: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
        print(f"Total Translations: {total_translations}")
        print(f"Successful Translations: {successful_translations} ({successful_translations/total_translations*100:.1f}%)")
        print("\nResults by Complexity:")
        for complexity, stats in report["statistics"]["by_complexity"].items():
            print(f"  {complexity}: {stats['count']} tests, {stats['success_rate']*100:.1f}% success")
        print("\nResults by Source Language:")
        for lang, stats in report["statistics"]["by_source_language"].items():
            print(f"  {lang}: {stats['count']} tests, {stats['success_rate']*100:.1f}% success")
        print("="*60)


def accept_user_test_cases(test_cases: List[TestCase]) -> List[TestExecution]:
    """
    Main entry point for user-provided test cases.
    
    This function accepts test cases provided by the user and executes them
    through the comprehensive proof of concept test framework.
    """
    framework = ProofOfConceptTestFramework()
    return framework.execute_test_batch(test_cases)