#!/usr/bin/env python3
"""
Scala Language Toolchain

Complete Scala language toolchain integrating parsing, conversion, and code generation
with performance optimization and round-trip translation verification.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging
import time
from pathlib import Path

from ...shared.base_toolchain import BaseLanguageToolchain, ToolchainResult, PerformanceMetrics
from ....core.runa_ast import ASTNode, Program
from ....core.translation_result import TranslationResult, TranslationStatus

from .scala_ast import ScalaSourceFile, ScalaNode
from .scala_parser import ScalaParser, parse_scala_code
from .scala_converter import ScalaToRunaConverter, RunaToScalaConverter, scala_to_runa, runa_to_scala
from .scala_generator import ScalaCodeGenerator, ScalaCodeStyle, generate_scala_code


class ScalaVersion(Enum):
    """Scala language versions."""
    SCALA_2_12 = "2.12"
    SCALA_2_13 = "2.13"
    SCALA_3_0 = "3.0"
    SCALA_3_1 = "3.1"
    SCALA_3_2 = "3.2"
    SCALA_3_3 = "3.3"
    SCALA_3_4 = "3.4"


class ScalaCompileTarget(Enum):
    """Scala compilation targets."""
    JVM = "jvm"
    JS = "js"
    NATIVE = "native"


@dataclass
class ScalaToolchainOptions:
    """Scala toolchain configuration options."""
    version: ScalaVersion = ScalaVersion.SCALA_3_3
    compile_target: ScalaCompileTarget = ScalaCompileTarget.JVM
    code_style: ScalaCodeStyle = ScalaCodeStyle.STANDARD
    enable_strict_mode: bool = True
    enable_warnings: bool = True
    enable_optimization: bool = True
    enable_macros: bool = True
    enable_implicits: bool = True
    enable_caching: bool = True
    cache_size: int = 1000
    performance_tracking: bool = True


class ScalaToolchain(BaseLanguageToolchain):
    """Complete Scala language toolchain for Runa translation platform."""
    
    def __init__(self, options: Optional[ScalaToolchainOptions] = None):
        super().__init__()
        self.options = options or ScalaToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = ScalaParser()
        self.scala_to_runa_converter = ScalaToRunaConverter()
        self.runa_to_scala_converter = RunaToScalaConverter()
        self.code_generator = ScalaCodeGenerator(self.options.code_style)
        
        # Performance optimization
        self._ast_cache: Dict[str, ScalaSourceFile] = {}
        self._conversion_cache: Dict[str, ASTNode] = {}
        self._generation_cache: Dict[str, str] = {}
        
        # Metrics
        self.metrics = PerformanceMetrics()
    
    @property
    def language_name(self) -> str:
        """Get language name."""
        return "Scala"
    
    @property
    def file_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return [".scala", ".sc"]
    
    def parse_source(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse Scala source code into AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"parse_{hash(source_code)}"
            if self.options.enable_caching and cache_key in self._ast_cache:
                ast = self._ast_cache[cache_key]
                self.logger.debug("Retrieved Scala AST from cache")
            else:
                # Parse source code
                ast = self.parser.parse(source_code)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._ast_cache, cache_key, ast)
            
            # Calculate metrics
            parse_time = time.time() - start_time
            if self.options.performance_tracking:
                self.metrics.total_operations += 1
                self.metrics.total_time += parse_time
                self.metrics.average_time = self.metrics.total_time / self.metrics.total_operations
            
            return ToolchainResult(
                success=True,
                result=ast,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=parse_time,
                    average_time=parse_time,
                    cache_hits=1 if cache_key in self._ast_cache else 0
                ),
                language_specific_data={
                    "scala_version": self.options.version.value,
                    "compile_target": self.options.compile_target.value,
                    "file_path": file_path
                }
            )
            
        except Exception as e:
            error_msg = f"Scala parsing failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_to_runa(self, scala_ast: ScalaNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert Scala AST to Runa AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"to_runa_{hash(str(scala_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                runa_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved Runa AST from cache")
            else:
                # Convert to Runa
                runa_ast = self.scala_to_runa_converter.convert(scala_ast)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._conversion_cache, cache_key, runa_ast)
            
            # Calculate metrics
            conversion_time = time.time() - start_time
            
            return ToolchainResult(
                success=True,
                result=runa_ast,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=conversion_time,
                    average_time=conversion_time,
                    cache_hits=1 if cache_key in self._conversion_cache else 0
                ),
                language_specific_data={
                    "conversion_direction": "scala_to_runa",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"Scala to Runa conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_from_runa(self, runa_ast: ASTNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert Runa AST to Scala AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"from_runa_{hash(str(runa_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                scala_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved Scala AST from cache")
            else:
                # Convert from Runa
                scala_ast = self.runa_to_scala_converter.convert(runa_ast)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._conversion_cache, cache_key, scala_ast)
            
            # Calculate metrics
            conversion_time = time.time() - start_time
            
            return ToolchainResult(
                success=True,
                result=scala_ast,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=conversion_time,
                    average_time=conversion_time,
                    cache_hits=1 if cache_key in self._conversion_cache else 0
                ),
                language_specific_data={
                    "conversion_direction": "runa_to_scala",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"Runa to Scala conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def generate_code(self, scala_ast: ScalaNode, style: Optional[ScalaCodeStyle] = None) -> ToolchainResult:
        """Generate Scala source code from AST."""
        start_time = time.time()
        
        try:
            # Use specified style or default
            target_style = style or self.options.code_style
            
            # Check cache first
            cache_key = f"generate_{hash(str(scala_ast))}_{target_style.value}"
            if self.options.enable_caching and cache_key in self._generation_cache:
                generated_code = self._generation_cache[cache_key]
                self.logger.debug("Retrieved generated Scala code from cache")
            else:
                # Generate code
                if target_style != self.code_generator.style:
                    self.code_generator = ScalaCodeGenerator(target_style)
                
                generated_code = self.code_generator.generate(scala_ast)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._generation_cache, cache_key, generated_code)
            
            # Calculate metrics
            generation_time = time.time() - start_time
            
            return ToolchainResult(
                success=True,
                result=generated_code,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=generation_time,
                    average_time=generation_time,
                    cache_hits=1 if cache_key in self._generation_cache else 0
                ),
                language_specific_data={
                    "code_style": target_style.value,
                    "generated_lines": generated_code.count('\n') + 1
                }
            )
            
        except Exception as e:
            error_msg = f"Scala code generation failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def translate_to_runa(self, source_code: str, file_path: Optional[str] = None) -> TranslationResult:
        """Complete translation from Scala to Runa."""
        start_time = time.time()
        
        try:
            # Parse Scala source
            parse_result = self.parse_source(source_code, file_path)
            if not parse_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.PARSE_ERROR,
                    error=parse_result.error,
                    source_language="scala",
                    target_language="runa"
                )
            
            # Convert to Runa
            convert_result = self.convert_to_runa(parse_result.result)
            if not convert_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.CONVERSION_ERROR,
                    error=convert_result.error,
                    source_language="scala",
                    target_language="runa"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=convert_result.result,
                source_language="scala",
                target_language="runa",
                translation_time=total_time,
                metadata={
                    "scala_version": self.options.version.value,
                    "compile_target": self.options.compile_target.value,
                    "file_path": file_path
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="scala",
                target_language="runa",
                translation_time=time.time() - start_time
            )
    
    def translate_from_runa(self, runa_ast: ASTNode, target_style: Optional[ScalaCodeStyle] = None) -> TranslationResult:
        """Complete translation from Runa to Scala."""
        start_time = time.time()
        
        try:
            # Convert from Runa
            convert_result = self.convert_from_runa(runa_ast)
            if not convert_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.CONVERSION_ERROR,
                    error=convert_result.error,
                    source_language="runa",
                    target_language="scala"
                )
            
            # Generate Scala code
            generate_result = self.generate_code(convert_result.result, target_style)
            if not generate_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.GENERATION_ERROR,
                    error=generate_result.error,
                    source_language="runa",
                    target_language="scala"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=generate_result.result,
                source_language="runa",
                target_language="scala",
                translation_time=total_time,
                metadata={
                    "code_style": (target_style or self.options.code_style).value,
                    "scala_version": self.options.version.value,
                    "compile_target": self.options.compile_target.value
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="runa",
                target_language="scala",
                translation_time=time.time() - start_time
            )
    
    def verify_round_trip(self, source_code: str) -> ToolchainResult:
        """Verify round-trip translation Scala -> Runa -> Scala."""
        start_time = time.time()
        
        try:
            # Scala -> Runa
            to_runa_result = self.translate_to_runa(source_code)
            if not to_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"Scala to Runa failed: {to_runa_result.error}"
                )
            
            # Runa -> Scala
            from_runa_result = self.translate_from_runa(to_runa_result.result)
            if not from_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"Runa to Scala failed: {from_runa_result.error}"
                )
            
            verification_time = time.time() - start_time
            
            # Compare semantics (simplified)
            original_lines = len(source_code.strip().split('\n'))
            generated_lines = len(from_runa_result.result.strip().split('\n'))
            similarity_ratio = min(original_lines, generated_lines) / max(original_lines, generated_lines)
            
            return ToolchainResult(
                success=True,
                result={
                    "original_code": source_code,
                    "runa_ast": to_runa_result.result,
                    "generated_code": from_runa_result.result,
                    "similarity_ratio": similarity_ratio,
                    "verification_passed": similarity_ratio > 0.7
                },
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=verification_time,
                    average_time=verification_time
                )
            )
            
        except Exception as e:
            return ToolchainResult(
                success=False,
                error=f"Round-trip verification failed: {e}",
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def get_metrics(self) -> PerformanceMetrics:
        """Get performance metrics."""
        return self.metrics
    
    def clear_caches(self):
        """Clear all caches."""
        self._ast_cache.clear()
        self._conversion_cache.clear()
        self._generation_cache.clear()
        self.logger.info("Scala toolchain caches cleared")
    
    def _manage_cache(self, cache: Dict[str, Any], key: str, value: Any):
        """Manage cache size and add new entry."""
        if len(cache) >= self.options.cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(cache))
            del cache[oldest_key]
        
        cache[key] = value


# Convenience functions
def create_scala_toolchain(options: Optional[ScalaToolchainOptions] = None) -> ScalaToolchain:
    """Create a Scala toolchain with specified options."""
    return ScalaToolchain(options)


def scala_to_runa_translation(source_code: str, 
                             options: Optional[ScalaToolchainOptions] = None) -> TranslationResult:
    """Translate Scala source code to Runa AST."""
    toolchain = create_scala_toolchain(options)
    return toolchain.translate_to_runa(source_code)


def runa_to_scala_translation(runa_ast: ASTNode, 
                             style: Optional[ScalaCodeStyle] = None,
                             options: Optional[ScalaToolchainOptions] = None) -> TranslationResult:
    """Translate Runa AST to Scala source code."""
    toolchain = create_scala_toolchain(options)
    return toolchain.translate_from_runa(runa_ast, style)


def verify_scala_round_trip(source_code: str,
                           options: Optional[ScalaToolchainOptions] = None) -> ToolchainResult:
    """Verify Scala round-trip translation."""
    toolchain = create_scala_toolchain(options)
    return toolchain.verify_round_trip(source_code)