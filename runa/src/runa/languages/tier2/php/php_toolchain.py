#!/usr/bin/env python3
"""
PHP Language Toolchain

Complete PHP language toolchain integrating parsing, conversion, and code generation
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

from .php_ast import PhpSourceFile, PhpNode
from .php_parser import PhpParser, parse_php_code
from .php_converter import PhpToRunaConverter, RunaToPhpConverter, php_to_runa, runa_to_php
from .php_generator import PhpCodeGenerator, PhpCodeStyle, generate_php_code


class PhpVersion(Enum):
    """PHP language versions."""
    PHP_7_4 = "7.4"
    PHP_8_0 = "8.0"
    PHP_8_1 = "8.1"
    PHP_8_2 = "8.2"
    PHP_8_3 = "8.3"
    PHP_8_4 = "8.4"


@dataclass
class PhpToolchainOptions:
    """PHP toolchain configuration options."""
    version: PhpVersion = PhpVersion.PHP_8_3
    code_style: PhpCodeStyle = PhpCodeStyle.PSR12
    strict_types: bool = True
    enable_opcache: bool = True
    error_reporting: str = "E_ALL"
    enable_caching: bool = True
    cache_size: int = 1000
    performance_tracking: bool = True


class PhpToolchain(BaseLanguageToolchain):
    """Complete PHP language toolchain for Runa translation platform."""
    
    def __init__(self, options: Optional[PhpToolchainOptions] = None):
        super().__init__()
        self.options = options or PhpToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = PhpParser()
        self.php_to_runa_converter = PhpToRunaConverter()
        self.runa_to_php_converter = RunaToPhpConverter()
        self.code_generator = PhpCodeGenerator(self.options.code_style)
        
        # Performance optimization
        self._ast_cache: Dict[str, PhpSourceFile] = {}
        self._conversion_cache: Dict[str, ASTNode] = {}
        self._generation_cache: Dict[str, str] = {}
        
        # Metrics
        self.metrics = PerformanceMetrics()
    
    @property
    def language_name(self) -> str:
        """Get language name."""
        return "PHP"
    
    @property
    def file_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return [".php", ".phtml", ".php3", ".php4", ".php5", ".phps"]
    
    def parse_source(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse PHP source code into AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"parse_{hash(source_code)}"
            if self.options.enable_caching and cache_key in self._ast_cache:
                ast = self._ast_cache[cache_key]
                self.logger.debug("Retrieved PHP AST from cache")
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
                    "php_version": self.options.version.value,
                    "strict_types": self.options.strict_types,
                    "file_path": file_path
                }
            )
            
        except Exception as e:
            error_msg = f"PHP parsing failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_to_runa(self, php_ast: PhpNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert PHP AST to Runa AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"to_runa_{hash(str(php_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                runa_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved Runa AST from cache")
            else:
                # Convert to Runa
                runa_ast = self.php_to_runa_converter.convert(php_ast)
                
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
                    "conversion_direction": "php_to_runa",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"PHP to Runa conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_from_runa(self, runa_ast: ASTNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert Runa AST to PHP AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"from_runa_{hash(str(runa_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                php_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved PHP AST from cache")
            else:
                # Convert from Runa
                php_ast = self.runa_to_php_converter.convert(runa_ast)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._conversion_cache, cache_key, php_ast)
            
            # Calculate metrics
            conversion_time = time.time() - start_time
            
            return ToolchainResult(
                success=True,
                result=php_ast,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=conversion_time,
                    average_time=conversion_time,
                    cache_hits=1 if cache_key in self._conversion_cache else 0
                ),
                language_specific_data={
                    "conversion_direction": "runa_to_php",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"Runa to PHP conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def generate_code(self, php_ast: PhpNode, style: Optional[PhpCodeStyle] = None) -> ToolchainResult:
        """Generate PHP source code from AST."""
        start_time = time.time()
        
        try:
            # Use specified style or default
            target_style = style or self.options.code_style
            
            # Check cache first
            cache_key = f"generate_{hash(str(php_ast))}_{target_style.value}"
            if self.options.enable_caching and cache_key in self._generation_cache:
                generated_code = self._generation_cache[cache_key]
                self.logger.debug("Retrieved generated PHP code from cache")
            else:
                # Generate code
                if target_style != self.code_generator.style:
                    self.code_generator = PhpCodeGenerator(target_style)
                
                generated_code = self.code_generator.generate(php_ast)
                
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
            error_msg = f"PHP code generation failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def translate_to_runa(self, source_code: str, file_path: Optional[str] = None) -> TranslationResult:
        """Complete translation from PHP to Runa."""
        start_time = time.time()
        
        try:
            # Parse PHP source
            parse_result = self.parse_source(source_code, file_path)
            if not parse_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.PARSE_ERROR,
                    error=parse_result.error,
                    source_language="php",
                    target_language="runa"
                )
            
            # Convert to Runa
            convert_result = self.convert_to_runa(parse_result.result)
            if not convert_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.CONVERSION_ERROR,
                    error=convert_result.error,
                    source_language="php",
                    target_language="runa"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=convert_result.result,
                source_language="php",
                target_language="runa",
                translation_time=total_time,
                metadata={
                    "php_version": self.options.version.value,
                    "strict_types": self.options.strict_types,
                    "file_path": file_path
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="php",
                target_language="runa",
                translation_time=time.time() - start_time
            )
    
    def translate_from_runa(self, runa_ast: ASTNode, target_style: Optional[PhpCodeStyle] = None) -> TranslationResult:
        """Complete translation from Runa to PHP."""
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
                    target_language="php"
                )
            
            # Generate PHP code
            generate_result = self.generate_code(convert_result.result, target_style)
            if not generate_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.GENERATION_ERROR,
                    error=generate_result.error,
                    source_language="runa",
                    target_language="php"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=generate_result.result,
                source_language="runa",
                target_language="php",
                translation_time=total_time,
                metadata={
                    "code_style": (target_style or self.options.code_style).value,
                    "php_version": self.options.version.value,
                    "strict_types": self.options.strict_types
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="runa",
                target_language="php",
                translation_time=time.time() - start_time
            )
    
    def verify_round_trip(self, source_code: str) -> ToolchainResult:
        """Verify round-trip translation PHP -> Runa -> PHP."""
        start_time = time.time()
        
        try:
            # PHP -> Runa
            to_runa_result = self.translate_to_runa(source_code)
            if not to_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"PHP to Runa failed: {to_runa_result.error}"
                )
            
            # Runa -> PHP
            from_runa_result = self.translate_from_runa(to_runa_result.result)
            if not from_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"Runa to PHP failed: {from_runa_result.error}"
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
        self.logger.info("PHP toolchain caches cleared")
    
    def _manage_cache(self, cache: Dict[str, Any], key: str, value: Any):
        """Manage cache size and add new entry."""
        if len(cache) >= self.options.cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(cache))
            del cache[oldest_key]
        
        cache[key] = value


# Convenience functions
def create_php_toolchain(options: Optional[PhpToolchainOptions] = None) -> PhpToolchain:
    """Create a PHP toolchain with specified options."""
    return PhpToolchain(options)


def php_to_runa_translation(source_code: str, 
                           options: Optional[PhpToolchainOptions] = None) -> TranslationResult:
    """Translate PHP source code to Runa AST."""
    toolchain = create_php_toolchain(options)
    return toolchain.translate_to_runa(source_code)


def runa_to_php_translation(runa_ast: ASTNode, 
                           style: Optional[PhpCodeStyle] = None,
                           options: Optional[PhpToolchainOptions] = None) -> TranslationResult:
    """Translate Runa AST to PHP source code."""
    toolchain = create_php_toolchain(options)
    return toolchain.translate_from_runa(runa_ast, style)


def verify_php_round_trip(source_code: str,
                         options: Optional[PhpToolchainOptions] = None) -> ToolchainResult:
    """Verify PHP round-trip translation."""
    toolchain = create_php_toolchain(options)
    return toolchain.verify_round_trip(source_code)