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

from ...shared.base_toolchain import BaseLanguageToolchain, LanguageMetadata, ToolchainResult
from ....core.translation_result import TranslationResult, TranslationError
from .csharp_ast import *
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
        
        # Setup supported features (commented out until LanguageFeature is available)
        # self._setup_supported_features()
        
        self.logger.info(f"C# toolchain initialized with {self.compiler_options.version.value} targeting {self.compiler_options.framework.value}")

    # def _setup_supported_features(self) -> None:
    #     """Setup the list of supported C# language features."""
    #     # TODO: Uncomment when LanguageFeature enum is available
    #     self.supported_features = {
    #         # LanguageFeature.CLASSES: True,
    #         # LanguageFeature.INTERFACES: True,
    #         # ... (other features)
    #     }

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
            
            # Generate Runa code from AST
            from ...runa.runa_generator import generate_runa
            generated_code = generate_runa(runa_ast) if runa_ast else ""
            
            # Create result
            result = TranslationResult(
                code=generated_code,
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
                    "conversion_time": time.time() - start_time,
                    "generated_code_length": len(generated_code)
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
        """Calculate semantic similarity between two code strings.
        
        Uses multiple analysis techniques:
        1. AST structural similarity
        2. Token-based similarity
        3. Semantic token analysis
        4. Control flow similarity
        5. Variable/function name similarity
        
        Returns a similarity score between 0.0 (completely different) and 1.0 (identical).
        """
        try:
            # Parse both code strings into ASTs
            ast1 = self._parse_code_to_ast(code1)
            ast2 = self._parse_code_to_ast(code2)
            
            if ast1 is None or ast2 is None:
                return 0.0
            
            # Calculate multiple similarity metrics
            structural_similarity = self._calculate_structural_similarity(ast1, ast2)
            token_similarity = self._calculate_token_similarity(code1, code2)
            semantic_similarity = self._calculate_semantic_token_similarity(ast1, ast2)
            control_flow_similarity = self._calculate_control_flow_similarity(ast1, ast2)
            naming_similarity = self._calculate_naming_similarity(ast1, ast2)
            
            # Weighted combination of all metrics
            weights = {
                'structural': 0.35,
                'token': 0.25,
                'semantic': 0.20,
                'control_flow': 0.15,
                'naming': 0.05
            }
            
            final_similarity = (
                structural_similarity * weights['structural'] +
                token_similarity * weights['token'] +
                semantic_similarity * weights['semantic'] +
                control_flow_similarity * weights['control_flow'] +
                naming_similarity * weights['naming']
            )
            
            return min(1.0, max(0.0, final_similarity))
            
        except Exception as e:
            self.logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def _calculate_structural_similarity(self, ast1: CSharpNode, ast2: CSharpNode) -> float:
        """Calculate structural similarity between two ASTs."""
        try:
            # Extract structural features
            features1 = self._extract_structural_features(ast1)
            features2 = self._extract_structural_features(ast2)
            
            # Calculate Jaccard similarity
            intersection = len(features1.intersection(features2))
            union = len(features1.union(features2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating structural similarity: {e}")
            return 0.0
    
    def _extract_structural_features(self, ast: CSharpNode) -> set:
        """Extract structural features from AST."""
        features = set()
        
        def extract_features_recursive(node: CSharpNode):
            if node is None:
                return
            
            # Add node type
            features.add(f"type:{type(node).__name__}")
            
            # Add structural patterns
            if isinstance(node, CSharpIfStatement):
                features.add("pattern:if_statement")
            elif isinstance(node, CSharpWhileStatement):
                features.add("pattern:while_loop")
            elif isinstance(node, CSharpForStatement):
                features.add("pattern:for_loop")
            elif isinstance(node, CSharpTryStatement):
                features.add("pattern:try_catch")
            elif isinstance(node, CSharpMethodDeclaration):
                features.add("pattern:method_declaration")
            elif isinstance(node, CSharpClassDeclaration):
                features.add("pattern:class_declaration")
            
            # Recursively process children
            for child in node.get_children():
                extract_features_recursive(child)
        
        extract_features_recursive(ast)
        return features
    
    def _calculate_token_similarity(self, code1: str, code2: str) -> float:
        """Calculate token-based similarity between two code strings."""
        try:
            # Tokenize both code strings
            tokens1 = self._tokenize_code(code1)
            tokens2 = self._tokenize_code(code2)
            
            # Calculate token overlap
            token_set1 = set(tokens1)
            token_set2 = set(tokens2)
            
            intersection = len(token_set1.intersection(token_set2))
            union = len(token_set1.union(token_set2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating token similarity: {e}")
            return 0.0
    
    def _tokenize_code(self, code: str) -> List[str]:
        """Tokenize code into meaningful tokens."""
        # Simple tokenization - in production, use a proper C# lexer
        import re
        
        # Remove comments and strings for basic tokenization
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)  # Single line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Multi-line comments
        code = re.sub(r'"[^"]*"', 'STRING', code)  # String literals
        code = re.sub(r"'[^']*'", 'CHAR', code)  # Char literals
        
        # Split into tokens
        tokens = re.findall(r'\b\w+\b|[^\w\s]', code)
        return [token.lower() for token in tokens if token.strip()]
    
    def _calculate_semantic_token_similarity(self, ast1: CSharpNode, ast2: CSharpNode) -> float:
        """Calculate similarity based on semantic tokens (keywords, operators, etc.)."""
        try:
            semantic_tokens1 = self._extract_semantic_tokens(ast1)
            semantic_tokens2 = self._extract_semantic_tokens(ast2)
            
            # Calculate semantic token similarity
            intersection = len(semantic_tokens1.intersection(semantic_tokens2))
            union = len(semantic_tokens1.union(semantic_tokens2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating semantic token similarity: {e}")
            return 0.0
    
    def _extract_semantic_tokens(self, ast: CSharpNode) -> set:
        """Extract semantic tokens from AST."""
        tokens = set()
        
        def extract_tokens_recursive(node: CSharpNode):
            if node is None:
                return
            
            # Extract keywords and operators
            if isinstance(node, CSharpBinaryExpression):
                tokens.add(f"operator:{node.operator.name if node.operator else 'unknown'}")
            elif isinstance(node, CSharpUnaryExpression):
                tokens.add(f"operator:{node.operator.name if node.operator else 'unknown'}")
            elif isinstance(node, CSharpIfStatement):
                tokens.add("keyword:if")
            elif isinstance(node, CSharpWhileStatement):
                tokens.add("keyword:while")
            elif isinstance(node, CSharpForStatement):
                tokens.add("keyword:for")
            elif isinstance(node, CSharpTryStatement):
                tokens.add("keyword:try")
            elif isinstance(node, CSharpReturnStatement):
                tokens.add("keyword:return")
            elif isinstance(node, CSharpThrowStatement):
                tokens.add("keyword:throw")
            
            # Recursively process children
            for child in node.get_children():
                extract_tokens_recursive(child)
        
        extract_tokens_recursive(ast)
        return tokens
    
    def _calculate_control_flow_similarity(self, ast1: CSharpNode, ast2: CSharpNode) -> float:
        """Calculate control flow similarity between two ASTs."""
        try:
            flow1 = self._extract_control_flow(ast1)
            flow2 = self._extract_control_flow(ast2)
            
            # Calculate control flow similarity
            intersection = len(flow1.intersection(flow2))
            union = len(flow1.union(flow2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating control flow similarity: {e}")
            return 0.0
    
    def _extract_control_flow(self, ast: CSharpNode) -> set:
        """Extract control flow patterns from AST."""
        flow_patterns = set()
        
        def extract_flow_recursive(node: CSharpNode):
            if node is None:
                return
            
            # Extract control flow patterns
            if isinstance(node, CSharpIfStatement):
                flow_patterns.add("flow:conditional")
                if node.else_statement:
                    flow_patterns.add("flow:if_else")
            elif isinstance(node, CSharpWhileStatement):
                flow_patterns.add("flow:loop")
            elif isinstance(node, CSharpForStatement):
                flow_patterns.add("flow:for_loop")
            elif isinstance(node, CSharpForEachStatement):
                flow_patterns.add("flow:foreach_loop")
            elif isinstance(node, CSharpSwitchStatement):
                flow_patterns.add("flow:switch")
            elif isinstance(node, CSharpTryStatement):
                flow_patterns.add("flow:exception_handling")
                if node.catches:
                    flow_patterns.add("flow:try_catch")
                if node.finally_block:
                    flow_patterns.add("flow:try_finally")
            
            # Recursively process children
            for child in node.get_children():
                extract_flow_recursive(child)
        
        extract_flow_recursive(ast)
        return flow_patterns
    
    def _calculate_naming_similarity(self, ast1: CSharpNode, ast2: CSharpNode) -> float:
        """Calculate similarity based on variable, function, and class names."""
        try:
            names1 = self._extract_names(ast1)
            names2 = self._extract_names(ast2)
            
            # Calculate name similarity using string similarity
            total_similarity = 0.0
            total_comparisons = 0
            
            for name1 in names1:
                for name2 in names2:
                    similarity = self._string_similarity(name1, name2)
                    total_similarity += similarity
                    total_comparisons += 1
            
            return total_similarity / total_comparisons if total_comparisons > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating naming similarity: {e}")
            return 0.0
    
    def _extract_names(self, ast: CSharpNode) -> set:
        """Extract names from AST."""
        names = set()
        
        def extract_names_recursive(node: CSharpNode):
            if node is None:
                return
            
            # Extract identifiers and names
            if hasattr(node, 'identifier') and node.identifier:
                names.add(node.identifier.lower())
            if hasattr(node, 'name') and node.name:
                names.add(node.name.lower())
            
            # Recursively process children
            for child in node.get_children():
                extract_names_recursive(child)
        
        extract_names_recursive(ast)
        return names
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity using Levenshtein distance."""
        if not str1 or not str2:
            return 0.0
        
        # Simple Levenshtein distance implementation
        len1, len2 = len(str1), len(str2)
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j
        
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if str1[i-1] == str2[j-1]:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    matrix[i][j] = min(
                        matrix[i-1][j] + 1,    # deletion
                        matrix[i][j-1] + 1,    # insertion
                        matrix[i-1][j-1] + 1   # substitution
                    )
        
        distance = matrix[len1][len2]
        max_len = max(len1, len2)
        return 1.0 - (distance / max_len) if max_len > 0 else 1.0
    
    def _parse_code_to_ast(self, code: str) -> Optional[CSharpNode]:
        """Parse code string to AST."""
        try:
            # Use the C# parser to parse the code
            from .csharp_parser import CSharpParser
            parser = CSharpParser()
            return parser.parse(code)
        except Exception as e:
            self.logger.error(f"Error parsing code to AST: {e}")
            return None

    def _save_ast_cache(self, code_hash: str, ast: CSharpNode) -> None:
        """Save AST to cache with proper serialization and compression."""
        if not self.enable_caching:
            return
            
        try:
            cache_file = self.cache_directory / f"{code_hash}.json"
            
            # Create cache directory if it doesn't exist
            self.cache_directory.mkdir(parents=True, exist_ok=True)
            
            # Serialize AST to JSON with metadata
            cache_data = {
                "hash": code_hash,
                "timestamp": time.time(),
                "version": "1.0",
                "language": "csharp",
                "ast": self._serialize_ast(ast),
                "metadata": {
                    "node_count": self._count_nodes(ast),
                    "max_depth": self._calculate_max_depth(ast),
                    "file_size": len(str(ast)) if ast else 0
                }
            }
            
            # Compress and save with atomic write
            import gzip
            import json
            import tempfile
            
            # Write to temporary file first for atomic operation
            temp_file = cache_file.with_suffix('.tmp')
            with gzip.open(temp_file, 'wt', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            # Atomic move to final location
            temp_file.replace(cache_file)
            
            self.logger.debug(f"AST cache saved: {cache_file} ({len(str(cache_data))} bytes)")
            
        except Exception as e:
            self.logger.warning(f"Failed to save AST cache: {e}")
            # Clean up any partial files
            temp_file = cache_file.with_suffix('.tmp')
            if temp_file.exists():
                temp_file.unlink(missing_ok=True)
    
    def _load_ast_cache(self, code_hash: str) -> Optional[CSharpNode]:
        """Load AST from cache with proper deserialization and validation."""
        try:
            cache_file = self.cache_directory / f"{code_hash}.json"
            
            if not cache_file.exists():
                return None
            
            # Check file age for cache invalidation
            file_age = time.time() - cache_file.stat().st_mtime
            if file_age > self.cache_max_age:
                self.logger.debug(f"Cache file expired: {cache_file}")
                cache_file.unlink()
                return None
            
            # Load and decompress cache data
            import gzip
            import json
            
            with gzip.open(cache_file, 'rt', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Validate cache data
            if not self._validate_cache_data(cache_data):
                self.logger.warning(f"Invalid cache data: {cache_file}")
                cache_file.unlink()
                return None
            
            # Deserialize AST
            ast = self._deserialize_ast(cache_data["ast"])
            
            self.logger.debug(f"AST cache loaded: {cache_file}")
            return ast
            
        except Exception as e:
            self.logger.warning(f"Failed to load AST cache: {e}")
            # Clean up corrupted cache file
            cache_file = self.cache_directory / f"{code_hash}.json"
            if cache_file.exists():
                cache_file.unlink(missing_ok=True)
            return None
    
    def _serialize_ast(self, ast: CSharpNode) -> dict:
        """Serialize AST to JSON-serializable format."""
        if ast is None:
            return None
        
        def serialize_node(node: CSharpNode) -> dict:
            if node is None:
                return None
            
            # Get node type
            node_type = type(node).__name__
            
            # Get node attributes
            attributes = {}
            for attr_name, attr_value in node.__dict__.items():
                if attr_name.startswith('_'):
                    continue
                
                if isinstance(attr_value, (str, int, float, bool, type(None))):
                    attributes[attr_name] = attr_value
                elif isinstance(attr_value, list):
                    attributes[attr_name] = [
                        serialize_node(item) if isinstance(item, CSharpNode) else item
                        for item in attr_value
                    ]
                elif isinstance(attr_value, CSharpNode):
                    attributes[attr_name] = serialize_node(attr_value)
                elif hasattr(attr_value, 'name'):  # Enum values
                    attributes[attr_name] = attr_value.name
                else:
                    attributes[attr_name] = str(attr_value)
            
            return {
                "type": node_type,
                "attributes": attributes
            }
        
        return serialize_node(ast)
    
    def _deserialize_ast(self, ast_data: dict) -> Optional[CSharpNode]:
        """Deserialize AST from JSON format."""
        if ast_data is None:
            return None
        
        def deserialize_node(data: dict) -> Optional[CSharpNode]:
            if data is None:
                return None
            
            # Get node type
            node_type_name = data.get("type")
            if not node_type_name:
                return None
            
            # Import and get node class
            from .csharp_ast import CSharpNode
            node_class = getattr(self._get_ast_module(), node_type_name, None)
            if not node_class:
                self.logger.warning(f"Unknown node type: {node_type_name}")
                return None
            
            # Reconstruct node attributes
            attributes = data.get("attributes", {})
            reconstructed_attrs = {}
            
            for attr_name, attr_value in attributes.items():
                if isinstance(attr_value, dict) and "type" in attr_value:
                    # Nested node
                    reconstructed_attrs[attr_name] = deserialize_node(attr_value)
                elif isinstance(attr_value, list):
                    # List of nodes or values
                    reconstructed_attrs[attr_name] = [
                        deserialize_node(item) if isinstance(item, dict) and "type" in item else item
                        for item in attr_value
                    ]
                elif attr_name == "operator" and isinstance(attr_value, str):
                    # Enum reconstruction
                    from .csharp_ast import CSharpOperator
                    reconstructed_attrs[attr_name] = getattr(CSharpOperator, attr_value, None)
                elif attr_name == "type" and isinstance(attr_value, str):
                    # NodeType enum reconstruction
                    from .csharp_ast import CSharpNodeType
                    reconstructed_attrs[attr_name] = getattr(CSharpNodeType, attr_value, None)
                else:
                    reconstructed_attrs[attr_name] = attr_value
            
            # Create node instance
            try:
                return node_class(**reconstructed_attrs)
            except Exception as e:
                self.logger.warning(f"Failed to reconstruct node {node_type_name}: {e}")
                return None
        
        return deserialize_node(ast_data)
    
    def _get_ast_module(self):
        """Get the AST module for dynamic imports."""
        from . import csharp_ast
        return csharp_ast
    
    def _validate_cache_data(self, cache_data: dict) -> bool:
        """Validate cache data integrity."""
        required_fields = ["hash", "timestamp", "version", "language", "ast"]
        
        # Check required fields
        for field in required_fields:
            if field not in cache_data:
                return False
        
        # Check version compatibility
        if cache_data["version"] != "1.0":
            return False
        
        # Check language
        if cache_data["language"] != "csharp":
            return False
        
        # Check timestamp
        if not isinstance(cache_data["timestamp"], (int, float)):
            return False
        
        return True
    
    def _count_nodes(self, ast: CSharpNode) -> int:
        """Count total number of nodes in AST."""
        if ast is None:
            return 0
        
        count = 1  # Count current node
        for child in ast.get_children():
            count += self._count_nodes(child)
        
        return count
    
    def _calculate_max_depth(self, ast: CSharpNode) -> int:
        """Calculate maximum depth of AST."""
        if ast is None:
            return 0
        
        max_depth = 1
        for child in ast.get_children():
            child_depth = self._calculate_max_depth(child)
            max_depth = max(max_depth, child_depth + 1)
        
        return max_depth


# Convenience functions for external use
def parse_csharp_code(code: str) -> CSharpNode:
    """Parse C# code using the default toolchain."""
    default_toolchain = CSharpToolchain()
    return default_toolchain.parse_code(code)


def generate_csharp_code(ast: CSharpNode) -> str:
    """Generate C# code using the default toolchain."""
    default_toolchain = CSharpToolchain()
    return default_toolchain.generate_code(ast)


def csharp_round_trip_verify(code: str, tolerance: float = 0.95) -> Tuple[bool, Dict[str, Any]]:
    """Verify round-trip translation using the default toolchain."""
    default_toolchain = CSharpToolchain()
    return default_toolchain.verify_round_trip(code, tolerance)


def csharp_to_runa_translate(code: str) -> TranslationResult:
    """Translate C# code to Runa using the default toolchain."""
    default_toolchain = CSharpToolchain()
    return default_toolchain.translate_to_runa(code)


def runa_to_csharp_translate(runa_ast: Any) -> TranslationResult:
    """Translate Runa AST to C# using the default toolchain."""
    default_toolchain = CSharpToolchain()
    return default_toolchain.translate_from_runa(runa_ast)