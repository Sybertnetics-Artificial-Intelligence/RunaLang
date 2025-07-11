#!/usr/bin/env python3
"""
Kotlin Language Toolchain

Complete Kotlin toolchain integration for the Runa Universal Translation Platform.
Provides comprehensive Kotlin support including parsing, conversion, generation,
and validation with full support for modern Kotlin features.

This module coordinates:
- Kotlin parsing and lexical analysis
- Bidirectional conversion between Kotlin and Runa AST
- Kotlin code generation with multiple style options
- Coroutine and null safety support
- Performance optimization and analysis
- Round-trip translation verification

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import time
from pathlib import Path

# Import base toolchain
from ....languages.shared.base_toolchain import BaseLanguageToolchain

# Import Kotlin components
from .kotlin_parser import KotlinParser, KotlinLexer, KotlinParseError
from .kotlin_generator import KotlinCodeGenerator, KotlinCodeStyle, KotlinFormattingOptions
from .kotlin_converter import KotlinToRunaConverter, RunaToKotlinConverter
from .kotlin_ast import (
    KotlinProgram, KotlinStatement, KotlinExpression, KotlinNode,
    KotlinClassDeclaration, KotlinFunctionDeclaration, KotlinPropertyDeclaration,
    KotlinPackageDeclaration, KotlinImportDeclaration
)

# Import core AST
from ....core.runa_ast import (
    Program, Statement, Expression, ASTNode, TranslationMetadata, SourceLocation
)

# Import core components
from ....core.verification import VerificationResult, VerificationStatus
from ....core.translation_result import TranslationResult, TranslationStatus


class KotlinFeatureLevel(Enum):
    """Kotlin language feature levels."""
    KOTLIN_1_0 = "1.0"
    KOTLIN_1_1 = "1.1"
    KOTLIN_1_2 = "1.2"
    KOTLIN_1_3 = "1.3"
    KOTLIN_1_4 = "1.4"
    KOTLIN_1_5 = "1.5"
    KOTLIN_1_6 = "1.6"
    KOTLIN_1_7 = "1.7"
    KOTLIN_1_8 = "1.8"
    KOTLIN_1_9 = "1.9"
    LATEST = "latest"


class KotlinPlatform(Enum):
    """Kotlin target platforms."""
    JVM = "jvm"
    ANDROID = "android"
    JS = "js"
    NATIVE = "native"
    MULTIPLATFORM = "multiplatform"


class KotlinOptimizationLevel(Enum):
    """Kotlin optimization levels."""
    NONE = "none"
    BASIC = "basic"
    FULL = "full"
    AGGRESSIVE = "aggressive"


@dataclass
class KotlinToolchainOptions:
    """Kotlin toolchain configuration options."""
    # Language features
    feature_level: KotlinFeatureLevel = KotlinFeatureLevel.LATEST
    platform: KotlinPlatform = KotlinPlatform.JVM
    
    # Code generation
    code_style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS
    formatting_options: Optional[KotlinFormattingOptions] = None
    
    # Optimization
    optimization_level: KotlinOptimizationLevel = KotlinOptimizationLevel.BASIC
    enable_coroutines: bool = True
    enable_null_safety: bool = True
    enable_type_inference: bool = True
    
    # Analysis
    strict_mode: bool = False
    enable_warnings: bool = True
    treat_warnings_as_errors: bool = False
    
    # Performance
    enable_caching: bool = True
    cache_directory: Optional[str] = None
    performance_logging: bool = False
    
    # Advanced features
    enable_experimental_features: bool = False
    enable_inline_classes: bool = True
    enable_sealed_classes: bool = True
    enable_data_classes: bool = True
    enable_operator_overloading: bool = True
    enable_delegation: bool = True
    enable_destructuring: bool = True
    
    # JVM specific
    jvm_target: str = "1.8"
    enable_jvm_default: bool = True
    
    # JavaScript specific
    js_target: str = "es5"
    enable_js_modules: bool = True
    
    # Native specific
    native_target: str = "linux"
    enable_native_debug: bool = False


@dataclass
class KotlinPerformanceMetrics:
    """Kotlin-specific performance metrics."""
    lexing_time: float = 0.0
    parsing_time: float = 0.0
    semantic_analysis_time: float = 0.0
    code_generation_time: float = 0.0
    total_translation_time: float = 0.0
    ast_node_count: int = 0
    generated_lines: int = 0
    memory_usage: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    compilation_warnings: int = 0
    compilation_errors: int = 0
    coroutine_usage: int = 0
    nullable_type_usage: int = 0


class KotlinToolchain(BaseLanguageToolchain):
    """
    Complete Kotlin language toolchain implementation.
    
    This class provides comprehensive Kotlin language support including:
    - Modern Kotlin syntax (1.0 through latest)
    - Multiple platform targets (JVM, Android, JS, Native)
    - Coroutines and null safety
    - Advanced language features (sealed classes, data classes, etc.)
    - Performance optimization and caching
    - Round-trip translation verification
    """

    def __init__(self, options: Optional[KotlinToolchainOptions] = None):
        """
        Initialize the Kotlin toolchain.
        
        Args:
            options: Kotlin toolchain configuration options
        """
        super().__init__(
            language_name="Kotlin",
            language_version="1.9",
            file_extension=".kt",
            supports_compilation=True,
            supports_interpretation=False
        )
        
        self.options = options or KotlinToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.lexer = KotlinLexer()
        self.parser = KotlinParser()
        self.to_runa_converter = KotlinToRunaConverter()
        self.from_runa_converter = RunaToKotlinConverter()
        self.generator = KotlinCodeGenerator(style=self.options.code_style)
        
        # Performance tracking
        self.metrics = KotlinPerformanceMetrics()
        
        # Cache management
        self.ast_cache: Dict[str, KotlinNode] = {}
        self.translation_cache: Dict[str, str] = {}
        
        # Initialize cache directory
        if self.options.enable_caching:
            cache_dir = Path(self.options.cache_directory or Path.home() / ".runa_cache" / "kotlin")
            cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup supported features
        self._setup_supported_features()
        
        self.logger.info(f"Kotlin toolchain initialized with {self.options.feature_level.value} targeting {self.options.platform.value}")

    def _setup_supported_features(self) -> None:
        """Setup the list of supported Kotlin language features."""
        self.supported_features = {
            # Core language features
            "classes": True,
            "objects": True,
            "interfaces": True,
            "inheritance": True,
            "polymorphism": True,
            "generics": True,
            "lambdas": True,
            "higher_order_functions": True,
            "extension_functions": True,
            "infix_functions": True,
            "operator_overloading": self.options.enable_operator_overloading,
            "delegation": self.options.enable_delegation,
            "destructuring": self.options.enable_destructuring,
            
            # Modern features
            "coroutines": self.options.enable_coroutines,
            "null_safety": self.options.enable_null_safety,
            "type_inference": self.options.enable_type_inference,
            "data_classes": self.options.enable_data_classes,
            "sealed_classes": self.options.enable_sealed_classes,
            "inline_classes": self.options.enable_inline_classes,
            "enum_classes": True,
            "annotation_classes": True,
            
            # Control flow
            "when_expressions": True,
            "if_expressions": True,
            "try_expressions": True,
            "elvis_operator": True,
            "safe_call_operator": True,
            "not_null_assertion": True,
            
            # Collections
            "collections": True,
            "sequences": True,
            "ranges": True,
            "array_literals": True,
            
            # String features
            "string_templates": True,
            "raw_strings": True,
            "multiline_strings": True,
            
            # Advanced features
            "reflection": True,
            "annotations": True,
            "type_aliases": True,
            "contracts": self.options.feature_level != KotlinFeatureLevel.KOTLIN_1_0,
            "inline_functions": True,
            "reified_generics": True,
            
            # Platform specific
            "jvm_interop": self.options.platform in [KotlinPlatform.JVM, KotlinPlatform.ANDROID],
            "js_interop": self.options.platform == KotlinPlatform.JS,
            "native_interop": self.options.platform == KotlinPlatform.NATIVE,
            "multiplatform": self.options.platform == KotlinPlatform.MULTIPLATFORM,
            
            # Experimental features
            "experimental_features": self.options.enable_experimental_features,
            "unsigned_types": self.options.feature_level != KotlinFeatureLevel.KOTLIN_1_0,
            "context_receivers": self.options.enable_experimental_features,
            "value_classes": self.options.enable_experimental_features,
        }

    def parse_code(self, code: str) -> KotlinProgram:
        """
        Parse Kotlin source code into an AST.
        
        Args:
            code: Kotlin source code string
            
        Returns:
            KotlinProgram: Root AST node
            
        Raises:
            KotlinParseError: If parsing fails
        """
        start_time = time.time()
        
        try:
            # Check cache first
            if self.options.enable_caching:
                import hashlib
                code_hash = hashlib.sha256(code.encode()).hexdigest()
                if code_hash in self.ast_cache:
                    self.metrics.cache_hits += 1
                    self.logger.debug(f"AST cache hit for hash {code_hash[:8]}")
                    return self.ast_cache[code_hash]
                self.metrics.cache_misses += 1
            
            # Parse
            ast = self.parser.parse(code)
            
            # Count nodes for metrics
            self.metrics.ast_node_count = self._count_ast_nodes(ast)
            
            # Cache result
            if self.options.enable_caching:
                self.ast_cache[code_hash] = ast
            
            self.metrics.total_translation_time = time.time() - start_time
            
            if self.options.performance_logging:
                self.logger.info(f"Parsed Kotlin code in {self.metrics.total_translation_time:.3f}s "
                               f"({self.metrics.ast_node_count} nodes)")
            
            return ast
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Kotlin parsing failed: {e}")
            raise KotlinParseError(f"Failed to parse Kotlin code: {e}")

    def generate_code(self, ast: KotlinProgram) -> str:
        """
        Generate Kotlin source code from an AST.
        
        Args:
            ast: Kotlin AST root node
            
        Returns:
            str: Generated Kotlin source code
        """
        start_time = time.time()
        
        try:
            # Generate code
            code = self.generator.generate(ast)
            
            # Update metrics
            self.metrics.code_generation_time = time.time() - start_time
            self.metrics.generated_lines = len(code.splitlines())
            
            if self.options.performance_logging:
                self.logger.info(f"Generated Kotlin code in {self.metrics.code_generation_time:.3f}s "
                               f"({self.metrics.generated_lines} lines)")
            
            return code
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Kotlin code generation failed: {e}")
            raise RuntimeError(f"Failed to generate Kotlin code: {e}")

    def translate_from_runa(self, runa_ast: Program) -> TranslationResult:
        """
        Translate from Runa AST to Kotlin code.
        
        Args:
            runa_ast: Runa AST node
            
        Returns:
            TranslationResult: Translation result with Kotlin code and metadata
        """
        start_time = time.time()
        
        try:
            # Convert Runa AST to Kotlin AST
            kotlin_ast = self.from_runa_converter.convert(runa_ast)
            
            # Generate Kotlin code
            code = self.generate_code(kotlin_ast)
            
            # Create result
            result = TranslationResult(
                code=code,
                language=self.language_name,
                success=True,
                ast=kotlin_ast,
                execution_time=time.time() - start_time,
                warnings=[],
                errors=[],
                metadata={
                    "kotlin_version": self.options.feature_level.value,
                    "platform": self.options.platform.value,
                    "code_style": self.options.code_style.value,
                    "null_safety": self.options.enable_null_safety,
                    "coroutines": self.options.enable_coroutines,
                    "ast_node_count": self.metrics.ast_node_count,
                    "generated_lines": self.metrics.generated_lines,
                    "coroutine_usage": self.metrics.coroutine_usage,
                    "nullable_type_usage": self.metrics.nullable_type_usage
                }
            )
            
            if self.options.performance_logging:
                self.logger.info(f"Translated from Runa to Kotlin in {result.execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Translation from Runa to Kotlin failed: {e}")
            
            return TranslationResult(
                code="",
                language=self.language_name,
                success=False,
                ast=None,
                execution_time=time.time() - start_time,
                warnings=[],
                errors=[str(e)],
                metadata={}
            )

    def translate_to_runa(self, code: str) -> TranslationResult:
        """
        Translate Kotlin code to Runa AST.
        
        Args:
            code: Kotlin source code
            
        Returns:
            TranslationResult: Translation result with Runa AST and metadata
        """
        start_time = time.time()
        
        try:
            # Parse Kotlin code
            kotlin_ast = self.parse_code(code)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_converter.convert(kotlin_ast)
            
            # Create result
            result = TranslationResult(
                code="",  # Runa AST doesn't have code representation here
                language="Runa",
                success=True,
                ast=runa_ast,
                execution_time=time.time() - start_time,
                warnings=[],
                errors=[],
                metadata={
                    "source_language": self.language_name,
                    "kotlin_version": self.options.feature_level.value,
                    "platform": self.options.platform.value,
                    "ast_node_count": self.metrics.ast_node_count,
                    "conversion_time": time.time() - start_time,
                    "features_used": self._analyze_features_used(kotlin_ast)
                }
            )
            
            if self.options.performance_logging:
                self.logger.info(f"Translated from Kotlin to Runa in {result.execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Translation from Kotlin to Runa failed: {e}")
            
            return TranslationResult(
                code="",
                language="Runa",
                success=False,
                ast=None,
                execution_time=time.time() - start_time,
                warnings=[],
                errors=[str(e)],
                metadata={}
            )

    def verify_round_trip(self, original_code: str, tolerance: float = 0.95) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify round-trip translation integrity.
        
        Args:
            original_code: Original Kotlin source code
            tolerance: Semantic similarity tolerance (0.0 to 1.0)
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (success, verification_details)
        """
        start_time = time.time()
        
        try:
            # Original -> Runa -> Kotlin
            runa_result = self.translate_to_runa(original_code)
            if not runa_result.success:
                return False, {
                    "error": "Failed to translate to Runa",
                    "runa_errors": runa_result.errors
                }
            
            kotlin_result = self.translate_from_runa(runa_result.ast)
            if not kotlin_result.success:
                return False, {
                    "error": "Failed to translate from Runa",
                    "kotlin_errors": kotlin_result.errors
                }
            
            # Compare original and round-trip code
            similarity = self._calculate_semantic_similarity(original_code, kotlin_result.code)
            
            verification_details = {
                "round_trip_time": time.time() - start_time,
                "semantic_similarity": similarity,
                "tolerance": tolerance,
                "original_lines": len(original_code.splitlines()),
                "round_trip_lines": len(kotlin_result.code.splitlines()),
                "original_ast_nodes": self._count_ast_nodes(self.parse_code(original_code)),
                "round_trip_ast_nodes": self._count_ast_nodes(kotlin_result.ast),
                "features_preserved": self._compare_features(original_code, kotlin_result.code),
                "passed": similarity >= tolerance
            }
            
            if self.options.performance_logging:
                self.logger.info(f"Round-trip verification: {similarity:.3f} similarity "
                               f"({'PASS' if similarity >= tolerance else 'FAIL'})")
            
            return similarity >= tolerance, verification_details
            
        except Exception as e:
            self.logger.error(f"Round-trip verification failed: {e}")
            return False, {
                "error": str(e),
                "verification_time": time.time() - start_time
            }

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return {
            "language": self.language_name,
            "version": self.options.feature_level.value,
            "platform": self.options.platform.value,
            "metrics": {
                "lexing_time": self.metrics.lexing_time,
                "parsing_time": self.metrics.parsing_time,
                "semantic_analysis_time": self.metrics.semantic_analysis_time,
                "code_generation_time": self.metrics.code_generation_time,
                "total_translation_time": self.metrics.total_translation_time,
                "ast_node_count": self.metrics.ast_node_count,
                "generated_lines": self.metrics.generated_lines,
                "memory_usage": self.metrics.memory_usage,
                "cache_hits": self.metrics.cache_hits,
                "cache_misses": self.metrics.cache_misses,
                "compilation_warnings": self.metrics.compilation_warnings,
                "compilation_errors": self.metrics.compilation_errors,
                "coroutine_usage": self.metrics.coroutine_usage,
                "nullable_type_usage": self.metrics.nullable_type_usage
            },
            "cache_stats": {
                "enabled": self.options.enable_caching,
                "ast_cache_size": len(self.ast_cache),
                "translation_cache_size": len(self.translation_cache)
            },
            "configuration": {
                "feature_level": self.options.feature_level.value,
                "platform": self.options.platform.value,
                "code_style": self.options.code_style.value,
                "optimization_level": self.options.optimization_level.value,
                "null_safety": self.options.enable_null_safety,
                "coroutines": self.options.enable_coroutines,
                "type_inference": self.options.enable_type_inference,
                "experimental_features": self.options.enable_experimental_features
            }
        }

    def clear_cache(self) -> None:
        """Clear all caches."""
        self.ast_cache.clear()
        self.translation_cache.clear()
        
        if self.options.enable_caching and self.options.cache_directory:
            import shutil
            cache_dir = Path(self.options.cache_directory)
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Kotlin toolchain cache cleared")

    def optimize_for_platform(self, platform: KotlinPlatform) -> None:
        """
        Optimize toolchain for specific target platform.
        
        Args:
            platform: Target platform
        """
        self.options.platform = platform
        
        # Adjust features based on platform
        if platform == KotlinPlatform.ANDROID:
            self.options.jvm_target = "1.8"
            self.options.enable_coroutines = True
            self.options.enable_null_safety = True
            self.options.code_style = KotlinCodeStyle.ANDROID
        
        elif platform == KotlinPlatform.JS:
            self.options.js_target = "es5"
            self.options.enable_js_modules = True
            self.options.enable_coroutines = True
        
        elif platform == KotlinPlatform.NATIVE:
            self.options.native_target = "linux"
            self.options.enable_native_debug = True
            self.options.enable_coroutines = True
        
        elif platform == KotlinPlatform.MULTIPLATFORM:
            self.options.enable_coroutines = True
            self.options.enable_null_safety = True
            self.options.enable_experimental_features = True
        
        self.logger.info(f"Optimized Kotlin toolchain for {platform.value}")

    def _count_ast_nodes(self, node: KotlinNode) -> int:
        """Count the total number of AST nodes."""
        if not node:
            return 0
        
        count = 1
        # This would need to be implemented based on the actual AST structure
        # For now, return a placeholder
        return count

    def _calculate_semantic_similarity(self, code1: str, code2: str) -> float:
        """Calculate semantic similarity between two code strings."""
        # Simple similarity based on normalized structure
        # In a real implementation, this would use more sophisticated analysis
        
        # Remove whitespace and normalize
        normalized1 = ''.join(code1.split())
        normalized2 = ''.join(code2.split())
        
        if not normalized1 and not normalized2:
            return 1.0
        if not normalized1 or not normalized2:
            return 0.0
        
        # Calculate character-level similarity
        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()

    def _analyze_features_used(self, ast: KotlinProgram) -> Dict[str, bool]:
        """Analyze which Kotlin features are used in the AST."""
        features = {
            "classes": False,
            "objects": False,
            "data_classes": False,
            "sealed_classes": False,
            "inline_classes": False,
            "coroutines": False,
            "nullable_types": False,
            "lambdas": False,
            "extension_functions": False,
            "operator_overloading": False,
            "when_expressions": False,
            "string_templates": False,
            "destructuring": False,
            "delegation": False
        }
        
        # This would need to traverse the AST and detect feature usage
        # For now, return placeholder
        return features

    def _compare_features(self, original_code: str, round_trip_code: str) -> Dict[str, bool]:
        """Compare feature usage between original and round-trip code."""
        original_ast = self.parse_code(original_code)
        round_trip_ast = self.parse_code(round_trip_code)
        
        original_features = self._analyze_features_used(original_ast)
        round_trip_features = self._analyze_features_used(round_trip_ast)
        
        # Compare features
        preserved = {}
        for feature, used in original_features.items():
            preserved[feature] = used == round_trip_features.get(feature, False)
        
        return preserved


# Convenience functions
def create_kotlin_toolchain(
    feature_level: KotlinFeatureLevel = KotlinFeatureLevel.LATEST,
    platform: KotlinPlatform = KotlinPlatform.JVM,
    code_style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS,
    **kwargs
) -> KotlinToolchain:
    """Create a Kotlin toolchain with the specified configuration."""
    options = KotlinToolchainOptions(
        feature_level=feature_level,
        platform=platform,
        code_style=code_style,
        **kwargs
    )
    return KotlinToolchain(options)


def parse_kotlin_code(code: str) -> KotlinProgram:
    """Parse Kotlin code and return AST."""
    toolchain = KotlinToolchain()
    return toolchain.parse_code(code)


def generate_kotlin_code(ast: KotlinProgram, 
                        style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS) -> str:
    """Generate Kotlin code from AST."""
    generator = KotlinCodeGenerator(style)
    return generator.generate(ast)


def kotlin_to_runa(code: str) -> Program:
    """Convert Kotlin code to Runa AST."""
    toolchain = KotlinToolchain()
    result = toolchain.translate_to_runa(code)
    if not result.success:
        raise RuntimeError(f"Translation failed: {result.errors}")
    return result.ast


def runa_to_kotlin(runa_ast: Program, 
                  style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS) -> str:
    """Convert Runa AST to Kotlin code."""
    toolchain = KotlinToolchain(KotlinToolchainOptions(code_style=style))
    result = toolchain.translate_from_runa(runa_ast)
    if not result.success:
        raise RuntimeError(f"Translation failed: {result.errors}")
    return result.code


def verify_kotlin_round_trip(code: str, tolerance: float = 0.95) -> bool:
    """Verify round-trip translation of Kotlin code."""
    toolchain = KotlinToolchain()
    success, _ = toolchain.verify_round_trip(code, tolerance)
    return success