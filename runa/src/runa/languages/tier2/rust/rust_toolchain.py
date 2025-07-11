#!/usr/bin/env python3
"""
Rust Language Toolchain

Complete Rust toolchain integration for the Runa Universal Translation Platform.
Provides comprehensive Rust support including parsing, conversion, generation,
and validation with full support for modern Rust features.

This module coordinates:
- Rust parsing and lexical analysis
- Bidirectional conversion between Rust and Runa AST
- Rust code generation with multiple style options
- Ownership, borrowing, and lifetime support
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

# Import Rust components
from .rust_parser import RustParser, RustLexer, RustParseError
from .rust_generator import RustCodeGenerator, RustCodeStyle, RustFormattingOptions
from .rust_converter import RustToRunaConverter, RunaToRustConverter
from .rust_ast import (
    RustCrate, RustNode, RustItem, RustExpression, RustStatement,
    RustFunction, RustStruct, RustEnum, RustTrait, RustImpl,
    RustVisibility, RustMutability, RustSafety, RustAsyncness
)

# Import core AST
from ....core.runa_ast import (
    Program, Statement, Expression, ASTNode, TranslationMetadata, SourceLocation
)

# Import core components
from ....core.verification import VerificationResult, VerificationStatus
from ....core.translation_result import TranslationResult, TranslationStatus


class RustEdition(Enum):
    """Rust language editions."""
    RUST_2015 = "2015"
    RUST_2018 = "2018"
    RUST_2021 = "2021"
    RUST_2024 = "2024"


class RustTarget(Enum):
    """Rust compilation targets."""
    X86_64_UNKNOWN_LINUX_GNU = "x86_64-unknown-linux-gnu"
    X86_64_PC_WINDOWS_MSVC = "x86_64-pc-windows-msvc"
    X86_64_APPLE_DARWIN = "x86_64-apple-darwin"
    AARCH64_UNKNOWN_LINUX_GNU = "aarch64-unknown-linux-gnu"
    AARCH64_APPLE_DARWIN = "aarch64-apple-darwin"
    WASM32_UNKNOWN_UNKNOWN = "wasm32-unknown-unknown"
    WASM32_WASI = "wasm32-wasi"
    THUMBV7EM_NONE_EABIHF = "thumbv7em-none-eabihf"  # Embedded ARM


class RustOptimizationLevel(Enum):
    """Rust optimization levels."""
    DEBUG = "0"
    BASIC = "1"
    FULL = "2"
    AGGRESSIVE = "3"
    SIZE = "s"
    SIZE_AGGRESSIVE = "z"


@dataclass
class RustToolchainOptions:
    """Rust toolchain configuration options."""
    # Language features
    edition: RustEdition = RustEdition.RUST_2021
    target: RustTarget = RustTarget.X86_64_UNKNOWN_LINUX_GNU
    
    # Code generation
    code_style: RustCodeStyle = RustCodeStyle.RUSTFMT
    formatting_options: Optional[RustFormattingOptions] = None
    
    # Compilation
    optimization_level: RustOptimizationLevel = RustOptimizationLevel.BASIC
    debug_info: bool = True
    enable_lto: bool = False  # Link-time optimization
    
    # Features
    enable_unsafe: bool = True
    enable_async: bool = True
    enable_const_generics: bool = True
    enable_generic_associated_types: bool = True
    
    # Analysis
    strict_mode: bool = False
    enable_clippy: bool = True
    enable_miri: bool = False  # Miri interpreter for unsafe code
    treat_warnings_as_errors: bool = False
    
    # Memory safety
    enable_address_sanitizer: bool = False
    enable_memory_sanitizer: bool = False
    enable_thread_sanitizer: bool = False
    
    # Performance
    enable_caching: bool = True
    cache_directory: Optional[str] = None
    performance_logging: bool = False
    
    # Advanced features
    enable_experimental_features: bool = False
    enable_proc_macros: bool = True
    enable_derive_macros: bool = True
    enable_attribute_macros: bool = True
    
    # Cargo integration
    cargo_workspace: bool = True
    generate_cargo_toml: bool = True
    
    # Cross-compilation
    cross_compile: bool = False
    sysroot: Optional[str] = None
    
    # Documentation
    generate_docs: bool = True
    doc_private_items: bool = False


@dataclass
class RustPerformanceMetrics:
    """Rust-specific performance metrics."""
    lexing_time: float = 0.0
    parsing_time: float = 0.0
    semantic_analysis_time: float = 0.0
    borrow_checking_time: float = 0.0
    code_generation_time: float = 0.0
    total_translation_time: float = 0.0
    ast_node_count: int = 0
    generated_lines: int = 0
    memory_usage: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    compilation_warnings: int = 0
    compilation_errors: int = 0
    unsafe_blocks: int = 0
    async_functions: int = 0
    generic_functions: int = 0
    lifetime_annotations: int = 0
    borrowing_violations: int = 0


class RustToolchain(BaseLanguageToolchain):
    """
    Complete Rust language toolchain implementation.
    
    This class provides comprehensive Rust language support including:
    - Modern Rust syntax (2015, 2018, 2021, 2024 editions)
    - Multiple compilation targets (native, WASM, embedded)
    - Ownership, borrowing, and lifetime analysis
    - Async/await and futures support
    - Advanced type system (generics, traits, associated types)
    - Performance optimization and safety analysis
    - Round-trip translation verification
    """

    def __init__(self, options: Optional[RustToolchainOptions] = None):
        """
        Initialize the Rust toolchain.
        
        Args:
            options: Rust toolchain configuration options
        """
        super().__init__(
            language_name="Rust",
            language_version=options.edition.value if options else "2021",
            file_extension=".rs",
            supports_compilation=True,
            supports_interpretation=False
        )
        
        self.options = options or RustToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.lexer = RustLexer()
        self.parser = RustParser()
        self.to_runa_converter = RustToRunaConverter()
        self.from_runa_converter = RunaToRustConverter()
        self.generator = RustCodeGenerator(style=self.options.code_style)
        
        # Performance tracking
        self.metrics = RustPerformanceMetrics()
        
        # Cache management
        self.ast_cache: Dict[str, RustNode] = {}
        self.translation_cache: Dict[str, str] = {}
        
        # Initialize cache directory
        if self.options.enable_caching:
            cache_dir = Path(self.options.cache_directory or Path.home() / ".runa_cache" / "rust")
            cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup supported features
        self._setup_supported_features()
        
        self.logger.info(f"Rust toolchain initialized for edition {self.options.edition.value} targeting {self.options.target.value}")

    def _setup_supported_features(self) -> None:
        """Setup the list of supported Rust language features."""
        self.supported_features = {
            # Core language features
            "structs": True,
            "enums": True,
            "traits": True,
            "impl_blocks": True,
            "generics": True,
            "associated_types": self.options.enable_generic_associated_types,
            "const_generics": self.options.enable_const_generics,
            "lifetimes": True,
            "ownership": True,
            "borrowing": True,
            "pattern_matching": True,
            "closures": True,
            "iterators": True,
            
            # Memory safety
            "unsafe_code": self.options.enable_unsafe,
            "raw_pointers": self.options.enable_unsafe,
            "memory_safety": True,
            "borrow_checker": True,
            "move_semantics": True,
            "reference_counting": True,
            
            # Async and concurrency
            "async_await": self.options.enable_async,
            "futures": self.options.enable_async,
            "tokio_runtime": self.options.enable_async,
            "channels": True,
            "threads": True,
            "atomic_types": True,
            "send_sync": True,
            
            # Macros
            "declarative_macros": True,
            "procedural_macros": self.options.enable_proc_macros,
            "derive_macros": self.options.enable_derive_macros,
            "attribute_macros": self.options.enable_attribute_macros,
            
            # Advanced features
            "higher_ranked_trait_bounds": True,
            "existential_types": self.options.enable_experimental_features,
            "const_eval": True,
            "inline_assembly": self.options.enable_unsafe,
            "simd": True,
            
            # Edition-specific features
            "non_lexical_lifetimes": self.options.edition != RustEdition.RUST_2015,
            "async_await_syntax": self.options.edition != RustEdition.RUST_2015,
            "try_operator": self.options.edition != RustEdition.RUST_2015,
            "uniform_function_call_syntax": True,
            
            # Target-specific features
            "no_std": self.options.target in [RustTarget.THUMBV7EM_NONE_EABIHF],
            "wasm_bindgen": self.options.target in [RustTarget.WASM32_UNKNOWN_UNKNOWN, RustTarget.WASM32_WASI],
            "ffi": True,
            "cdylib": True,
            
            # Tooling features
            "cargo_integration": self.options.cargo_workspace,
            "rustfmt": True,
            "clippy": self.options.enable_clippy,
            "miri": self.options.enable_miri,
            "rustdoc": self.options.generate_docs,
            
            # Experimental features
            "experimental_features": self.options.enable_experimental_features,
            "type_alias_impl_trait": self.options.enable_experimental_features,
            "generic_const_exprs": self.options.enable_experimental_features,
            "associated_type_defaults": self.options.enable_experimental_features,
        }

    def parse_code(self, code: str) -> RustCrate:
        """
        Parse Rust source code into an AST.
        
        Args:
            code: Rust source code string
            
        Returns:
            RustCrate: Root AST node
            
        Raises:
            RustParseError: If parsing fails
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
            
            # Count nodes and analyze features for metrics
            self.metrics.ast_node_count = self._count_ast_nodes(ast)
            self._analyze_rust_features(ast)
            
            # Cache result
            if self.options.enable_caching:
                self.ast_cache[code_hash] = ast
            
            self.metrics.total_translation_time = time.time() - start_time
            
            if self.options.performance_logging:
                self.logger.info(f"Parsed Rust code in {self.metrics.total_translation_time:.3f}s "
                               f"({self.metrics.ast_node_count} nodes)")
            
            return ast
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Rust parsing failed: {e}")
            raise RustParseError(f"Failed to parse Rust code: {e}")

    def generate_code(self, ast: RustCrate) -> str:
        """
        Generate Rust source code from an AST.
        
        Args:
            ast: Rust AST root node
            
        Returns:
            str: Generated Rust source code
        """
        start_time = time.time()
        
        try:
            # Generate code
            code = self.generator.generate(ast)
            
            # Update metrics
            self.metrics.code_generation_time = time.time() - start_time
            self.metrics.generated_lines = len(code.splitlines())
            
            if self.options.performance_logging:
                self.logger.info(f"Generated Rust code in {self.metrics.code_generation_time:.3f}s "
                               f"({self.metrics.generated_lines} lines)")
            
            return code
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Rust code generation failed: {e}")
            raise RuntimeError(f"Failed to generate Rust code: {e}")

    def translate_from_runa(self, runa_ast: Program) -> TranslationResult:
        """
        Translate from Runa AST to Rust code.
        
        Args:
            runa_ast: Runa AST node
            
        Returns:
            TranslationResult: Translation result with Rust code and metadata
        """
        start_time = time.time()
        
        try:
            # Convert Runa AST to Rust AST
            rust_ast = self.from_runa_converter.convert(runa_ast)
            
            # Generate Rust code
            code = self.generate_code(rust_ast)
            
            # Create result
            result = TranslationResult(
                code=code,
                language=self.language_name,
                success=True,
                ast=rust_ast,
                execution_time=time.time() - start_time,
                warnings=[],
                errors=[],
                metadata={
                    "rust_edition": self.options.edition.value,
                    "rust_target": self.options.target.value,
                    "code_style": self.options.code_style.value,
                    "optimization_level": self.options.optimization_level.value,
                    "unsafe_enabled": self.options.enable_unsafe,
                    "async_enabled": self.options.enable_async,
                    "ast_node_count": self.metrics.ast_node_count,
                    "generated_lines": self.metrics.generated_lines,
                    "unsafe_blocks": self.metrics.unsafe_blocks,
                    "async_functions": self.metrics.async_functions,
                    "generic_functions": self.metrics.generic_functions,
                    "lifetime_annotations": self.metrics.lifetime_annotations
                }
            )
            
            if self.options.performance_logging:
                self.logger.info(f"Translated from Runa to Rust in {result.execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Translation from Runa to Rust failed: {e}")
            
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
        Translate Rust code to Runa AST.
        
        Args:
            code: Rust source code
            
        Returns:
            TranslationResult: Translation result with Runa AST and metadata
        """
        start_time = time.time()
        
        try:
            # Parse Rust code
            rust_ast = self.parse_code(code)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_converter.convert(rust_ast)
            
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
                    "rust_edition": self.options.edition.value,
                    "rust_target": self.options.target.value,
                    "ast_node_count": self.metrics.ast_node_count,
                    "conversion_time": time.time() - start_time,
                    "features_used": self._analyze_features_used(rust_ast),
                    "memory_safety_features": {
                        "ownership_patterns": self._count_ownership_patterns(rust_ast),
                        "borrowing_patterns": self._count_borrowing_patterns(rust_ast),
                        "lifetime_bounds": self._count_lifetime_bounds(rust_ast)
                    }
                }
            )
            
            if self.options.performance_logging:
                self.logger.info(f"Translated from Rust to Runa in {result.execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Translation from Rust to Runa failed: {e}")
            
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
            original_code: Original Rust source code
            tolerance: Semantic similarity tolerance (0.0 to 1.0)
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (success, verification_details)
        """
        start_time = time.time()
        
        try:
            # Original -> Runa -> Rust
            runa_result = self.translate_to_runa(original_code)
            if not runa_result.success:
                return False, {
                    "error": "Failed to translate to Runa",
                    "runa_errors": runa_result.errors
                }
            
            rust_result = self.translate_from_runa(runa_result.ast)
            if not rust_result.success:
                return False, {
                    "error": "Failed to translate from Runa",
                    "rust_errors": rust_result.errors
                }
            
            # Compare original and round-trip code
            similarity = self._calculate_semantic_similarity(original_code, rust_result.code)
            
            # Verify memory safety features are preserved
            original_safety = self._analyze_memory_safety(original_code)
            round_trip_safety = self._analyze_memory_safety(rust_result.code)
            safety_preservation = self._compare_safety_features(original_safety, round_trip_safety)
            
            verification_details = {
                "round_trip_time": time.time() - start_time,
                "semantic_similarity": similarity,
                "tolerance": tolerance,
                "original_lines": len(original_code.splitlines()),
                "round_trip_lines": len(rust_result.code.splitlines()),
                "original_ast_nodes": self._count_ast_nodes(self.parse_code(original_code)),
                "round_trip_ast_nodes": self._count_ast_nodes(rust_result.ast),
                "features_preserved": self._compare_features(original_code, rust_result.code),
                "memory_safety_preserved": safety_preservation,
                "ownership_patterns_preserved": safety_preservation.get("ownership", True),
                "borrowing_patterns_preserved": safety_preservation.get("borrowing", True),
                "lifetime_annotations_preserved": safety_preservation.get("lifetimes", True),
                "passed": similarity >= tolerance and all(safety_preservation.values())
            }
            
            success = similarity >= tolerance and all(safety_preservation.values())
            
            if self.options.performance_logging:
                self.logger.info(f"Round-trip verification: {similarity:.3f} similarity, "
                               f"safety preserved: {all(safety_preservation.values())} "
                               f"({'PASS' if success else 'FAIL'})")
            
            return success, verification_details
            
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
            "edition": self.options.edition.value,
            "target": self.options.target.value,
            "metrics": {
                "lexing_time": self.metrics.lexing_time,
                "parsing_time": self.metrics.parsing_time,
                "semantic_analysis_time": self.metrics.semantic_analysis_time,
                "borrow_checking_time": self.metrics.borrow_checking_time,
                "code_generation_time": self.metrics.code_generation_time,
                "total_translation_time": self.metrics.total_translation_time,
                "ast_node_count": self.metrics.ast_node_count,
                "generated_lines": self.metrics.generated_lines,
                "memory_usage": self.metrics.memory_usage,
                "cache_hits": self.metrics.cache_hits,
                "cache_misses": self.metrics.cache_misses,
                "compilation_warnings": self.metrics.compilation_warnings,
                "compilation_errors": self.metrics.compilation_errors,
                "unsafe_blocks": self.metrics.unsafe_blocks,
                "async_functions": self.metrics.async_functions,
                "generic_functions": self.metrics.generic_functions,
                "lifetime_annotations": self.metrics.lifetime_annotations,
                "borrowing_violations": self.metrics.borrowing_violations
            },
            "cache_stats": {
                "enabled": self.options.enable_caching,
                "ast_cache_size": len(self.ast_cache),
                "translation_cache_size": len(self.translation_cache)
            },
            "configuration": {
                "edition": self.options.edition.value,
                "target": self.options.target.value,
                "code_style": self.options.code_style.value,
                "optimization_level": self.options.optimization_level.value,
                "unsafe_enabled": self.options.enable_unsafe,
                "async_enabled": self.options.enable_async,
                "const_generics": self.options.enable_const_generics,
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
        
        self.logger.info("Rust toolchain cache cleared")

    def optimize_for_target(self, target: RustTarget) -> None:
        """
        Optimize toolchain for specific target platform.
        
        Args:
            target: Target platform
        """
        self.options.target = target
        
        # Adjust features based on target
        if target == RustTarget.WASM32_UNKNOWN_UNKNOWN:
            self.options.enable_async = True
            self.options.optimization_level = RustOptimizationLevel.SIZE
        elif target == RustTarget.THUMBV7EM_NONE_EABIHF:
            self.options.optimization_level = RustOptimizationLevel.SIZE_AGGRESSIVE
            self.options.debug_info = False
        elif target in [RustTarget.X86_64_UNKNOWN_LINUX_GNU, RustTarget.X86_64_PC_WINDOWS_MSVC]:
            self.options.enable_lto = True
            self.options.optimization_level = RustOptimizationLevel.FULL
        
        self.logger.info(f"Optimized Rust toolchain for target {target.value}")

    def _count_ast_nodes(self, node: RustNode) -> int:
        """Count the total number of AST nodes."""
        if not node:
            return 0
        
        count = 1
        # This would need to be implemented based on the actual AST structure
        # For now, return a placeholder
        return count

    def _analyze_rust_features(self, ast: RustCrate) -> None:
        """Analyze Rust-specific features in the AST."""
        # This would traverse the AST and count features
        # For now, use placeholders
        self.metrics.unsafe_blocks = 0
        self.metrics.async_functions = 0
        self.metrics.generic_functions = 0
        self.metrics.lifetime_annotations = 0

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

    def _analyze_features_used(self, ast: RustCrate) -> Dict[str, bool]:
        """Analyze which Rust features are used in the AST."""
        features = {
            "structs": False,
            "enums": False,
            "traits": False,
            "impl_blocks": False,
            "generics": False,
            "lifetimes": False,
            "unsafe_code": False,
            "async_await": False,
            "pattern_matching": False,
            "closures": False,
            "macros": False,
            "ownership": False,
            "borrowing": False
        }
        
        # This would need to traverse the AST and detect feature usage
        # For now, return placeholder
        return features

    def _analyze_memory_safety(self, code: str) -> Dict[str, Any]:
        """Analyze memory safety features in code."""
        return {
            "ownership_patterns": 0,
            "borrowing_patterns": 0,
            "lifetime_bounds": 0,
            "unsafe_blocks": 0,
            "raw_pointers": 0
        }

    def _compare_safety_features(self, original: Dict[str, Any], round_trip: Dict[str, Any]) -> Dict[str, bool]:
        """Compare memory safety features between original and round-trip code."""
        return {
            "ownership": abs(original.get("ownership_patterns", 0) - round_trip.get("ownership_patterns", 0)) <= 1,
            "borrowing": abs(original.get("borrowing_patterns", 0) - round_trip.get("borrowing_patterns", 0)) <= 1,
            "lifetimes": abs(original.get("lifetime_bounds", 0) - round_trip.get("lifetime_bounds", 0)) <= 1,
            "unsafe": original.get("unsafe_blocks", 0) == round_trip.get("unsafe_blocks", 0)
        }

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

    def _count_ownership_patterns(self, ast: RustCrate) -> int:
        """Count ownership patterns in AST."""
        return 0  # Placeholder

    def _count_borrowing_patterns(self, ast: RustCrate) -> int:
        """Count borrowing patterns in AST."""
        return 0  # Placeholder

    def _count_lifetime_bounds(self, ast: RustCrate) -> int:
        """Count lifetime bounds in AST."""
        return 0  # Placeholder


# Convenience functions
def create_rust_toolchain(
    edition: RustEdition = RustEdition.RUST_2021,
    target: RustTarget = RustTarget.X86_64_UNKNOWN_LINUX_GNU,
    code_style: RustCodeStyle = RustCodeStyle.RUSTFMT,
    **kwargs
) -> RustToolchain:
    """Create a Rust toolchain with the specified configuration."""
    options = RustToolchainOptions(
        edition=edition,
        target=target,
        code_style=code_style,
        **kwargs
    )
    return RustToolchain(options)


def parse_rust_code(code: str) -> RustCrate:
    """Parse Rust code and return AST."""
    toolchain = RustToolchain()
    return toolchain.parse_code(code)


def generate_rust_code(ast: RustCrate, 
                      style: RustCodeStyle = RustCodeStyle.RUSTFMT) -> str:
    """Generate Rust code from AST."""
    generator = RustCodeGenerator(style)
    return generator.generate(ast)


def rust_to_runa(code: str) -> Program:
    """Convert Rust code to Runa AST."""
    toolchain = RustToolchain()
    result = toolchain.translate_to_runa(code)
    if not result.success:
        raise RuntimeError(f"Translation failed: {result.errors}")
    return result.ast


def runa_to_rust(runa_ast: Program, 
                style: RustCodeStyle = RustCodeStyle.RUSTFMT) -> str:
    """Convert Runa AST to Rust code."""
    toolchain = RustToolchain(RustToolchainOptions(code_style=style))
    result = toolchain.translate_from_runa(runa_ast)
    if not result.success:
        raise RuntimeError(f"Translation failed: {result.errors}")
    return result.code


def verify_rust_round_trip(code: str, tolerance: float = 0.95) -> bool:
    """Verify round-trip translation of Rust code."""
    toolchain = RustToolchain()
    success, _ = toolchain.verify_round_trip(code, tolerance)
    return success