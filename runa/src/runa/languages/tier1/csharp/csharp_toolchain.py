"""
C# Language Toolchain Integration

This module provides the complete C# toolchain integration for the Runa universal translation platform.
It extends the BaseLanguageToolchain to provide C#-specific functionality including compilation,
round-trip verification, performance optimization, and caching.

Author: Sybertnetics AI Solutions
License: MIT
"""

import time
from typing import Dict, List, Optional, Any, Tuple, Union
from pathlib import Path
import hashlib
import json
import logging
from dataclasses import dataclass, field
from enum import Enum

from ..base_toolchain import BaseLanguageToolchain, TranslationResult, LanguageFeature
from .csharp_ast import (
    CSharpNode, CSharpProgram, CSharpNamespace, CSharpClass, CSharpMethod,
    CSharpProperty, CSharpField, CSharpParameter, CSharpType, CSharpExpression,
    CSharpStatement, CSharpDeclaration, CSharpModifier, CSharpAccessModifier,
    CSharpAttribute, CSharpGenericParameter, CSharpConstraint, CSharpLiteral,
    CSharpIdentifier, CSharpBinaryExpression, CSharpUnaryExpression,
    CSharpMemberAccess, CSharpMethodCall, CSharpNewExpression, CSharpArrayAccess,
    CSharpCastExpression, CSharpConditionalExpression, CSharpLambdaExpression,
    CSharpAnonymousObject, CSharpQueryExpression, CSharpAwaitExpression,
    CSharpNullableType, CSharpTupleType, CSharpRecordDeclaration,
    CSharpSwitchExpression, CSharpPatternMatching, CSharpInterpolatedString,
    CSharpRangeExpression, CSharpIndexExpression, CSharpWithExpression,
    CSharpTopLevelStatement, CSharpGlobalUsing, CSharpFileScoped,
    CSharpInitOnlyProperty, CSharpRecordPattern, CSharpListPattern
)
from .csharp_parser import CSharpLexer, CSharpParser
from .csharp_converter import CSharpToRunaConverter, RunaToCSharpConverter
from .csharp_generator import CSharpCodeGenerator, CSharpCodeStyle


class CSharpVersion(Enum):
    """C# language version enumeration."""
    CSHARP_1_0 = "1.0"
    CSHARP_1_2 = "1.2"
    CSHARP_2_0 = "2.0"
    CSHARP_3_0 = "3.0"
    CSHARP_4_0 = "4.0"
    CSHARP_5_0 = "5.0"
    CSHARP_6_0 = "6.0"
    CSHARP_7_0 = "7.0"
    CSHARP_7_1 = "7.1"
    CSHARP_7_2 = "7.2"
    CSHARP_7_3 = "7.3"
    CSHARP_8_0 = "8.0"
    CSHARP_9_0 = "9.0"
    CSHARP_10_0 = "10.0"
    CSHARP_11_0 = "11.0"
    CSHARP_12_0 = "12.0"
    LATEST = "latest"


class CSharpFramework(Enum):
    """C# framework target enumeration."""
    NET_FRAMEWORK_2_0 = "net20"
    NET_FRAMEWORK_3_5 = "net35"
    NET_FRAMEWORK_4_0 = "net40"
    NET_FRAMEWORK_4_5 = "net45"
    NET_FRAMEWORK_4_6 = "net46"
    NET_FRAMEWORK_4_7 = "net47"
    NET_FRAMEWORK_4_8 = "net48"
    NET_CORE_1_0 = "netcoreapp1.0"
    NET_CORE_1_1 = "netcoreapp1.1"
    NET_CORE_2_0 = "netcoreapp2.0"
    NET_CORE_2_1 = "netcoreapp2.1"
    NET_CORE_2_2 = "netcoreapp2.2"
    NET_CORE_3_0 = "netcoreapp3.0"
    NET_CORE_3_1 = "netcoreapp3.1"
    NET_5_0 = "net5.0"
    NET_6_0 = "net6.0"
    NET_7_0 = "net7.0"
    NET_8_0 = "net8.0"
    NET_9_0 = "net9.0"
    NET_STANDARD_1_0 = "netstandard1.0"
    NET_STANDARD_1_1 = "netstandard1.1"
    NET_STANDARD_1_2 = "netstandard1.2"
    NET_STANDARD_1_3 = "netstandard1.3"
    NET_STANDARD_1_4 = "netstandard1.4"
    NET_STANDARD_1_5 = "netstandard1.5"
    NET_STANDARD_1_6 = "netstandard1.6"
    NET_STANDARD_2_0 = "netstandard2.0"
    NET_STANDARD_2_1 = "netstandard2.1"


@dataclass
class CSharpCompilerOptions:
    """C# compiler configuration options."""
    version: CSharpVersion = CSharpVersion.LATEST
    framework: CSharpFramework = CSharpFramework.NET_8_0
    nullable_enabled: bool = True
    implicit_usings: bool = True
    file_scoped_namespaces: bool = True
    top_level_statements: bool = False
    global_using_directives: bool = True
    treat_warnings_as_errors: bool = False
    warning_level: int = 4
    optimize: bool = True
    debug: bool = False
    unsafe_code: bool = False
    checked_arithmetic: bool = False
    define_constants: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    output_type: str = "exe"  # exe, library, winexe, module
    platform: str = "AnyCPU"  # AnyCPU, x86, x64, ARM, ARM64


@dataclass
class CSharpPerformanceMetrics:
    """C#-specific performance metrics."""
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


class CSharpToolchain(BaseLanguageToolchain):
    """
    Complete C# language toolchain implementation.
    
    This class provides comprehensive C# language support including:
    - Modern C# syntax (C# 1.0 through C# 12.0)
    - Multiple .NET framework targets
    - Advanced language features (nullable reference types, pattern matching, records)
    - Performance optimization and caching
    - Round-trip translation verification
    - Comprehensive error handling and diagnostics
    """

    def __init__(self, 
                 compiler_options: Optional[CSharpCompilerOptions] = None,
                 code_style: CSharpCodeStyle = CSharpCodeStyle.MICROSOFT,
                 enable_caching: bool = True,
                 cache_directory: Optional[str] = None,
                 performance_logging: bool = False):
        """
        Initialize the C# toolchain.
        
        Args:
            compiler_options: C# compiler configuration options
            code_style: Code formatting style preference
            enable_caching: Enable AST and translation caching
            cache_directory: Custom cache directory path
            performance_logging: Enable detailed performance logging
        """
        super().__init__(
            language_name="C#",
            language_version="12.0",
            file_extension=".cs",
            supports_compilation=True,
            supports_interpretation=False
        )
        
        self.compiler_options = compiler_options or CSharpCompilerOptions()
        self.code_style = code_style
        self.enable_caching = enable_caching
        self.cache_directory = Path(cache_directory) if cache_directory else Path.home() / ".runa_cache" / "csharp"
        self.performance_logging = performance_logging
        
        # Initialize components
        self.lexer = CSharpLexer()
        self.parser = CSharpParser()
        self.to_runa_converter = CSharpToRunaConverter()
        self.from_runa_converter = RunaToCSharpConverter()
        self.generator = CSharpCodeGenerator(style=code_style)
        
        # Performance tracking
        self.metrics = CSharpPerformanceMetrics()
        self.logger = logging.getLogger(__name__)
        
        # Cache management
        self.ast_cache: Dict[str, CSharpNode] = {}
        self.translation_cache: Dict[str, str] = {}
        
        # Initialize cache directory
        if self.enable_caching:
            self.cache_directory.mkdir(parents=True, exist_ok=True)
        
        # Setup supported features
        self._setup_supported_features()
        
        self.logger.info(f"C# toolchain initialized with {self.compiler_options.version.value} targeting {self.compiler_options.framework.value}")

    def _setup_supported_features(self) -> None:
        """Setup the list of supported C# language features."""
        self.supported_features = {
            LanguageFeature.CLASSES: True,
            LanguageFeature.INTERFACES: True,
            LanguageFeature.INHERITANCE: True,
            LanguageFeature.POLYMORPHISM: True,
            LanguageFeature.GENERICS: True,
            LanguageFeature.LAMBDAS: True,
            LanguageFeature.CLOSURES: True,
            LanguageFeature.ASYNC_AWAIT: True,
            LanguageFeature.PATTERN_MATCHING: True,
            LanguageFeature.NULLABLE_TYPES: True,
            LanguageFeature.RECORDS: True,
            LanguageFeature.TUPLES: True,
            LanguageFeature.PROPERTIES: True,
            LanguageFeature.EVENTS: True,
            LanguageFeature.DELEGATES: True,
            LanguageFeature.ATTRIBUTES: True,
            LanguageFeature.REFLECTION: True,
            LanguageFeature.LINQ: True,
            LanguageFeature.EXCEPTION_HANDLING: True,
            LanguageFeature.MEMORY_MANAGEMENT: False,  # Garbage collected
            LanguageFeature.OPERATOR_OVERLOADING: True,
            LanguageFeature.INDEXERS: True,
            LanguageFeature.DESTRUCTORS: True,
            LanguageFeature.NAMESPACES: True,
            LanguageFeature.ASSEMBLIES: True,
            LanguageFeature.UNSAFE_CODE: True,
            LanguageFeature.PARTIAL_CLASSES: True,
            LanguageFeature.EXTENSION_METHODS: True,
            LanguageFeature.ANONYMOUS_TYPES: True,
            LanguageFeature.DYNAMIC_TYPING: True,
            LanguageFeature.COVARIANCE_CONTRAVARIANCE: True,
            LanguageFeature.NULLABLE_REFERENCE_TYPES: True,
            LanguageFeature.SWITCH_EXPRESSIONS: True,
            LanguageFeature.USING_DECLARATIONS: True,
            LanguageFeature.READONLY_MEMBERS: True,
            LanguageFeature.DEFAULT_INTERFACE_METHODS: True,
            LanguageFeature.RANGES_INDICES: True,
            LanguageFeature.NULL_COALESCING_ASSIGNMENT: True,
            LanguageFeature.STATIC_LOCAL_FUNCTIONS: True,
            LanguageFeature.INIT_ONLY_PROPERTIES: True,
            LanguageFeature.RECORD_TYPES: True,
            LanguageFeature.TOP_LEVEL_STATEMENTS: True,
            LanguageFeature.GLOBAL_USING_DIRECTIVES: True,
            LanguageFeature.FILE_SCOPED_NAMESPACES: True,
            LanguageFeature.GENERIC_ATTRIBUTES: True,
            LanguageFeature.STATIC_ABSTRACT_INTERFACE_MEMBERS: True,
            LanguageFeature.REQUIRED_MEMBERS: True,
            LanguageFeature.UTF8_STRING_LITERALS: True,
            LanguageFeature.NEWLINES_IN_STRING_INTERPOLATION: True,
            LanguageFeature.LIST_PATTERNS: True,
            LanguageFeature.SLICE_PATTERNS: True,
            LanguageFeature.PRIMARY_CONSTRUCTORS: True,
            LanguageFeature.COLLECTION_EXPRESSIONS: True,
            LanguageFeature.INLINE_ARRAYS: True,
            LanguageFeature.LAMBDA_DEFAULT_PARAMETERS: True,
            LanguageFeature.ALIAS_ANY_TYPE: True,
            LanguageFeature.EXPERIMENTAL_ATTRIBUTE: True
        }

    def parse_code(self, code: str) -> CSharpNode:
        """
        Parse C# source code into an AST.
        
        Args:
            code: C# source code string
            
        Returns:
            CSharpNode: Root AST node
            
        Raises:
            SyntaxError: If parsing fails
        """
        start_time = time.time()
        
        try:
            # Check cache first
            if self.enable_caching:
                code_hash = hashlib.sha256(code.encode()).hexdigest()
                if code_hash in self.ast_cache:
                    self.metrics.cache_hits += 1
                    self.logger.debug(f"AST cache hit for hash {code_hash[:8]}")
                    return self.ast_cache[code_hash]
                self.metrics.cache_misses += 1
            
            # Tokenize
            lexing_start = time.time()
            tokens = self.lexer.tokenize(code)
            self.metrics.lexing_time = time.time() - lexing_start
            
            # Parse
            parsing_start = time.time()
            ast = self.parser.parse(tokens)
            self.metrics.parsing_time = time.time() - parsing_start
            
            # Count nodes for metrics
            self.metrics.ast_node_count = self._count_ast_nodes(ast)
            
            # Cache result
            if self.enable_caching:
                self.ast_cache[code_hash] = ast
                self._save_ast_cache(code_hash, ast)
            
            self.metrics.total_translation_time = time.time() - start_time
            
            if self.performance_logging:
                self.logger.info(f"Parsed C# code in {self.metrics.total_translation_time:.3f}s "
                               f"({self.metrics.ast_node_count} nodes)")
            
            return ast
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"C# parsing failed: {e}")
            raise SyntaxError(f"Failed to parse C# code: {e}")

    def generate_code(self, ast: CSharpNode) -> str:
        """
        Generate C# source code from an AST.
        
        Args:
            ast: C# AST root node
            
        Returns:
            str: Generated C# source code
        """
        start_time = time.time()
        
        try:
            # Generate code
            code = self.generator.generate(ast)
            
            # Update metrics
            self.metrics.code_generation_time = time.time() - start_time
            self.metrics.generated_lines = len(code.splitlines())
            
            if self.performance_logging:
                self.logger.info(f"Generated C# code in {self.metrics.code_generation_time:.3f}s "
                               f"({self.metrics.generated_lines} lines)")
            
            return code
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"C# code generation failed: {e}")
            raise RuntimeError(f"Failed to generate C# code: {e}")

    def translate_from_runa(self, runa_ast: Any) -> TranslationResult:
        """
        Translate from Runa AST to C# code.
        
        Args:
            runa_ast: Runa AST node
            
        Returns:
            TranslationResult: Translation result with C# code and metadata
        """
        start_time = time.time()
        
        try:
            # Convert Runa AST to C# AST
            csharp_ast = self.from_runa_converter.convert(runa_ast)
            
            # Generate C# code
            code = self.generate_code(csharp_ast)
            
            # Create result
            result = TranslationResult(
                code=code,
                language=self.language_name,
                success=True,
                ast=csharp_ast,
                execution_time=time.time() - start_time,
                warnings=[],
                errors=[],
                metadata={
                    "csharp_version": self.compiler_options.version.value,
                    "framework": self.compiler_options.framework.value,
                    "nullable_enabled": self.compiler_options.nullable_enabled,
                    "file_scoped_namespaces": self.compiler_options.file_scoped_namespaces,
                    "code_style": self.code_style.value,
                    "ast_node_count": self.metrics.ast_node_count,
                    "generated_lines": self.metrics.generated_lines
                }
            )
            
            if self.performance_logging:
                self.logger.info(f"Translated from Runa to C# in {result.execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Translation from Runa to C# failed: {e}")
            
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
        Translate C# code to Runa AST.
        
        Args:
            code: C# source code
            
        Returns:
            TranslationResult: Translation result with Runa AST and metadata
        """
        start_time = time.time()
        
        try:
            # Parse C# code
            csharp_ast = self.parse_code(code)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_converter.convert(csharp_ast)
            
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
                    "csharp_version": self.compiler_options.version.value,
                    "ast_node_count": self.metrics.ast_node_count,
                    "conversion_time": time.time() - start_time
                }
            )
            
            if self.performance_logging:
                self.logger.info(f"Translated from C# to Runa in {result.execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            self.metrics.compilation_errors += 1
            self.logger.error(f"Translation from C# to Runa failed: {e}")
            
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
            original_code: Original C# source code
            tolerance: Semantic similarity tolerance (0.0 to 1.0)
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (success, verification_details)
        """
        start_time = time.time()
        
        try:
            # Original -> Runa -> C#
            runa_result = self.translate_to_runa(original_code)
            if not runa_result.success:
                return False, {
                    "error": "Failed to translate to Runa",
                    "runa_errors": runa_result.errors
                }
            
            csharp_result = self.translate_from_runa(runa_result.ast)
            if not csharp_result.success:
                return False, {
                    "error": "Failed to translate from Runa",
                    "csharp_errors": csharp_result.errors
                }
            
            # Compare original and round-trip code
            similarity = self._calculate_semantic_similarity(original_code, csharp_result.code)
            
            verification_details = {
                "round_trip_time": time.time() - start_time,
                "semantic_similarity": similarity,
                "tolerance": tolerance,
                "original_lines": len(original_code.splitlines()),
                "round_trip_lines": len(csharp_result.code.splitlines()),
                "original_ast_nodes": self._count_ast_nodes(self.parse_code(original_code)),
                "round_trip_ast_nodes": self._count_ast_nodes(csharp_result.ast),
                "passed": similarity >= tolerance
            }
            
            if self.performance_logging:
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
            "version": self.compiler_options.version.value,
            "framework": self.compiler_options.framework.value,
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
                "compilation_errors": self.metrics.compilation_errors
            },
            "cache_stats": {
                "enabled": self.enable_caching,
                "directory": str(self.cache_directory),
                "ast_cache_size": len(self.ast_cache),
                "translation_cache_size": len(self.translation_cache)
            },
            "compiler_options": {
                "version": self.compiler_options.version.value,
                "framework": self.compiler_options.framework.value,
                "nullable_enabled": self.compiler_options.nullable_enabled,
                "implicit_usings": self.compiler_options.implicit_usings,
                "file_scoped_namespaces": self.compiler_options.file_scoped_namespaces,
                "top_level_statements": self.compiler_options.top_level_statements,
                "optimize": self.compiler_options.optimize,
                "debug": self.compiler_options.debug
            }
        }

    def clear_cache(self) -> None:
        """Clear all caches."""
        self.ast_cache.clear()
        self.translation_cache.clear()
        
        if self.enable_caching and self.cache_directory.exists():
            import shutil
            shutil.rmtree(self.cache_directory)
            self.cache_directory.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("C# toolchain cache cleared")

    def optimize_for_target(self, target_framework: CSharpFramework) -> None:
        """
        Optimize toolchain for specific target framework.
        
        Args:
            target_framework: Target .NET framework
        """
        self.compiler_options.framework = target_framework
        
        # Adjust language features based on framework
        if target_framework in [CSharpFramework.NET_FRAMEWORK_2_0, CSharpFramework.NET_FRAMEWORK_3_5]:
            self.compiler_options.nullable_enabled = False
            self.compiler_options.implicit_usings = False
            self.compiler_options.file_scoped_namespaces = False
            self.compiler_options.top_level_statements = False
            self.compiler_options.global_using_directives = False
        elif target_framework in [CSharpFramework.NET_FRAMEWORK_4_0, CSharpFramework.NET_FRAMEWORK_4_5]:
            self.compiler_options.nullable_enabled = False
            self.compiler_options.file_scoped_namespaces = False
            self.compiler_options.top_level_statements = False
        elif target_framework in [CSharpFramework.NET_CORE_1_0, CSharpFramework.NET_CORE_2_0]:
            self.compiler_options.nullable_enabled = False
            self.compiler_options.file_scoped_namespaces = False
            self.compiler_options.top_level_statements = False
        
        self.logger.info(f"Optimized C# toolchain for {target_framework.value}")

    def _count_ast_nodes(self, node: CSharpNode) -> int:
        """Count the total number of AST nodes."""
        if not node:
            return 0
        
        count = 1
        for child in node.children if hasattr(node, 'children') else []:
            count += self._count_ast_nodes(child)
        
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

    def _save_ast_cache(self, code_hash: str, ast: CSharpNode) -> None:
        """Save AST to persistent cache."""
        if not self.enable_caching:
            return
        
        try:
            cache_file = self.cache_directory / f"{code_hash}.json"
            # In a real implementation, we'd serialize the AST properly
            # For now, we'll just store a placeholder
            with open(cache_file, 'w') as f:
                json.dump({"hash": code_hash, "timestamp": time.time()}, f)
        except Exception as e:
            self.logger.warning(f"Failed to save AST cache: {e}")

    def _load_ast_cache(self, code_hash: str) -> Optional[CSharpNode]:
        """Load AST from persistent cache."""
        if not self.enable_caching:
            return None
        
        try:
            cache_file = self.cache_directory / f"{code_hash}.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                # In a real implementation, we'd deserialize the AST properly
                # For now, we'll return None to indicate cache miss
                return None
        except Exception as e:
            self.logger.warning(f"Failed to load AST cache: {e}")
        
        return None