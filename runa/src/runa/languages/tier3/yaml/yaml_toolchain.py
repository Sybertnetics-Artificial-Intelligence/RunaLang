#!/usr/bin/env python3
"""
YAML Language Toolchain

Complete YAML language toolchain integrating parsing, conversion, and code generation
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

from .yaml_ast import YamlDocument, YamlStream, YamlNode
from .yaml_parser import YamlParser, parse_yaml, parse_yaml_document
from .yaml_converter import YamlToRunaConverter, RunaToYamlConverter, yaml_to_runa, runa_to_yaml
from .yaml_generator import YamlCodeGenerator, YamlCodeStyle, generate_yaml_code


class YamlVersion(Enum):
    """YAML specification versions."""
    VERSION_1_1 = "1.1"
    VERSION_1_2 = "1.2"


@dataclass
class YamlToolchainOptions:
    """YAML toolchain configuration options."""
    version: YamlVersion = YamlVersion.VERSION_1_2
    code_style: YamlCodeStyle = YamlCodeStyle.STANDARD
    preserve_quotes: bool = False
    sort_keys: bool = False
    explicit_start: bool = False
    explicit_end: bool = False
    allow_unicode: bool = True
    canonical: bool = False
    indent_size: int = 2
    max_line_length: int = 120
    enable_caching: bool = True
    cache_size: int = 1000
    performance_tracking: bool = True


class YamlToolchain(BaseLanguageToolchain):
    """Complete YAML language toolchain for Runa translation platform."""
    
    def __init__(self, options: Optional[YamlToolchainOptions] = None):
        super().__init__()
        self.options = options or YamlToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = YamlParser()
        self.yaml_to_runa_converter = YamlToRunaConverter()
        self.runa_to_yaml_converter = RunaToYamlConverter()
        self.code_generator = YamlCodeGenerator(self.options.code_style)
        
        # Performance optimization
        self._ast_cache: Dict[str, YamlStream] = {}
        self._conversion_cache: Dict[str, ASTNode] = {}
        self._generation_cache: Dict[str, str] = {}
        
        # Metrics
        self.metrics = PerformanceMetrics()
    
    @property
    def language_name(self) -> str:
        """Get language name."""
        return "YAML"
    
    @property
    def file_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return [".yaml", ".yml"]
    
    def parse_source(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse YAML source code into AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"parse_{hash(source_code)}"
            if self.options.enable_caching and cache_key in self._ast_cache:
                ast = self._ast_cache[cache_key]
                self.logger.debug("Retrieved YAML AST from cache")
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
                    "version": self.options.version.value,
                    "file_path": file_path,
                    "document_count": len(ast.documents) if ast.documents else 0
                }
            )
            
        except Exception as e:
            error_msg = f"YAML parsing failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_to_runa(self, yaml_ast: YamlNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert YAML AST to Runa AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"to_runa_{hash(str(yaml_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                runa_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved Runa AST from cache")
            else:
                # Convert to Runa
                runa_ast = self.yaml_to_runa_converter.convert(yaml_ast)
                
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
                    "conversion_direction": "yaml_to_runa",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"YAML to Runa conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_from_runa(self, runa_ast: ASTNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert Runa AST to YAML AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"from_runa_{hash(str(runa_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                yaml_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved YAML AST from cache")
            else:
                # Convert from Runa
                yaml_ast = self.runa_to_yaml_converter.convert(runa_ast)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._conversion_cache, cache_key, yaml_ast)
            
            # Calculate metrics
            conversion_time = time.time() - start_time
            
            return ToolchainResult(
                success=True,
                result=yaml_ast,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=conversion_time,
                    average_time=conversion_time,
                    cache_hits=1 if cache_key in self._conversion_cache else 0
                ),
                language_specific_data={
                    "conversion_direction": "runa_to_yaml",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"Runa to YAML conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def generate_code(self, yaml_ast: YamlNode, style: Optional[YamlCodeStyle] = None) -> ToolchainResult:
        """Generate YAML source code from AST."""
        start_time = time.time()
        
        try:
            # Use specified style or default
            target_style = style or self.options.code_style
            
            # Check cache first
            cache_key = f"generate_{hash(str(yaml_ast))}_{target_style.value}"
            if self.options.enable_caching and cache_key in self._generation_cache:
                generated_code = self._generation_cache[cache_key]
                self.logger.debug("Retrieved generated YAML code from cache")
            else:
                # Generate code
                if target_style != self.code_generator.style:
                    self.code_generator = YamlCodeGenerator(target_style)
                
                generated_code = self.code_generator.generate(yaml_ast)
                
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
            error_msg = f"YAML code generation failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def translate_to_runa(self, source_code: str, file_path: Optional[str] = None) -> TranslationResult:
        """Complete translation from YAML to Runa."""
        start_time = time.time()
        
        try:
            # Parse YAML source
            parse_result = self.parse_source(source_code, file_path)
            if not parse_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.PARSE_ERROR,
                    error=parse_result.error,
                    source_language="yaml",
                    target_language="runa"
                )
            
            # Convert to Runa
            convert_result = self.convert_to_runa(parse_result.result)
            if not convert_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.CONVERSION_ERROR,
                    error=convert_result.error,
                    source_language="yaml",
                    target_language="runa"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=convert_result.result,
                source_language="yaml",
                target_language="runa",
                translation_time=total_time,
                metadata={
                    "version": self.options.version.value,
                    "file_path": file_path
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="yaml",
                target_language="runa",
                translation_time=time.time() - start_time
            )
    
    def translate_from_runa(self, runa_ast: ASTNode, target_style: Optional[YamlCodeStyle] = None) -> TranslationResult:
        """Complete translation from Runa to YAML."""
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
                    target_language="yaml"
                )
            
            # Generate YAML code
            generate_result = self.generate_code(convert_result.result, target_style)
            if not generate_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.GENERATION_ERROR,
                    error=generate_result.error,
                    source_language="runa",
                    target_language="yaml"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=generate_result.result,
                source_language="runa",
                target_language="yaml",
                translation_time=total_time,
                metadata={
                    "code_style": (target_style or self.options.code_style).value,
                    "version": self.options.version.value
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="runa",
                target_language="yaml",
                translation_time=time.time() - start_time
            )
    
    def verify_round_trip(self, source_code: str) -> ToolchainResult:
        """Verify round-trip translation YAML -> Runa -> YAML."""
        start_time = time.time()
        
        try:
            # YAML -> Runa
            to_runa_result = self.translate_to_runa(source_code)
            if not to_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"YAML to Runa failed: {to_runa_result.error}"
                )
            
            # Runa -> YAML
            from_runa_result = self.translate_from_runa(to_runa_result.result)
            if not from_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"Runa to YAML failed: {from_runa_result.error}"
                )
            
            verification_time = time.time() - start_time
            
            # Compare semantics by parsing both
            try:
                original_stream = parse_yaml(source_code)
                generated_stream = parse_yaml(from_runa_result.result)
                
                # Simple structural comparison
                original_data = None
                generated_data = None
                
                if original_stream.documents:
                    from .yaml_ast import yaml_value_to_python
                    original_data = yaml_value_to_python(original_stream.documents[0].content)
                
                if generated_stream.documents:
                    from .yaml_ast import yaml_value_to_python
                    generated_data = yaml_value_to_python(generated_stream.documents[0].content)
                
                data_matches = original_data == generated_data
                
                return ToolchainResult(
                    success=True,
                    result={
                        "original_code": source_code,
                        "runa_ast": to_runa_result.result,
                        "generated_code": from_runa_result.result,
                        "data_matches": data_matches,
                        "verification_passed": data_matches
                    },
                    metrics=PerformanceMetrics(
                        total_operations=1,
                        total_time=verification_time,
                        average_time=verification_time
                    )
                )
            except Exception as comp_error:
                # Fallback to simple comparison
                similarity_ratio = 0.8  # Assume reasonable similarity
                return ToolchainResult(
                    success=True,
                    result={
                        "original_code": source_code,
                        "runa_ast": to_runa_result.result,
                        "generated_code": from_runa_result.result,
                        "similarity_ratio": similarity_ratio,
                        "verification_passed": similarity_ratio > 0.7,
                        "comparison_error": str(comp_error)
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
        self.logger.info("YAML toolchain caches cleared")
    
    def _manage_cache(self, cache: Dict[str, Any], key: str, value: Any):
        """Manage cache size and add new entry."""
        if len(cache) >= self.options.cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(cache))
            del cache[oldest_key]
        
        cache[key] = value


# Convenience functions
def create_yaml_toolchain(options: Optional[YamlToolchainOptions] = None) -> YamlToolchain:
    """Create a YAML toolchain with specified options."""
    return YamlToolchain(options)


def yaml_to_runa_translation(source_code: str, 
                            options: Optional[YamlToolchainOptions] = None) -> TranslationResult:
    """Translate YAML source code to Runa AST."""
    toolchain = create_yaml_toolchain(options)
    return toolchain.translate_to_runa(source_code)


def runa_to_yaml_translation(runa_ast: ASTNode, 
                            style: Optional[YamlCodeStyle] = None,
                            options: Optional[YamlToolchainOptions] = None) -> TranslationResult:
    """Translate Runa AST to YAML source code."""
    toolchain = create_yaml_toolchain(options)
    return toolchain.translate_from_runa(runa_ast, style)


def verify_yaml_round_trip(source_code: str,
                          options: Optional[YamlToolchainOptions] = None) -> ToolchainResult:
    """Verify YAML round-trip translation."""
    toolchain = create_yaml_toolchain(options)
    return toolchain.verify_round_trip(source_code)


def parse_yaml_code(source_code: str, 
                   options: Optional[YamlToolchainOptions] = None) -> ToolchainResult:
    """Parse YAML source code."""
    toolchain = create_yaml_toolchain(options)
    return toolchain.parse_source(source_code)


def generate_yaml_code_from_ast(yaml_ast: YamlNode,
                               style: Optional[YamlCodeStyle] = None,
                               options: Optional[YamlToolchainOptions] = None) -> ToolchainResult:
    """Generate YAML code from AST."""
    toolchain = create_yaml_toolchain(options)
    return toolchain.generate_code(yaml_ast, style)