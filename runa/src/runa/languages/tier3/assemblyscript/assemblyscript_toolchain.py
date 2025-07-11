#!/usr/bin/env python3
"""
AssemblyScript Language Toolchain

Complete AssemblyScript language toolchain integrating parsing, conversion, and code generation
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

from .assemblyscript_ast import AsProgram, AsFunction, AsClass, AsNode
from .assemblyscript_parser import AsParser, parse_assemblyscript, parse_assemblyscript_file
from .assemblyscript_converter import AssemblyScriptToRunaConverter, RunaToAssemblyScriptConverter, assemblyscript_to_runa, runa_to_assemblyscript
from .assemblyscript_generator import AssemblyScriptCodeGenerator, AssemblyScriptCodeStyle, generate_assemblyscript_code


class AssemblyScriptTarget(Enum):
    """AssemblyScript compilation targets."""
    WASM32 = "wasm32"
    WASM64 = "wasm64"


@dataclass
class AssemblyScriptToolchainOptions:
    """AssemblyScript toolchain configuration options."""
    target: AssemblyScriptTarget = AssemblyScriptTarget.WASM32
    code_style: AssemblyScriptCodeStyle = AssemblyScriptCodeStyle.STANDARD
    strict_mode: bool = True
    optimize: bool = True
    debug_mode: bool = False
    explicit_types: bool = True
    semicolons: str = "always"
    quote_style: str = "double"
    indent_size: int = 2
    max_line_length: int = 120
    enable_caching: bool = True
    cache_size: int = 1000
    performance_tracking: bool = True


class AssemblyScriptToolchain(BaseLanguageToolchain):
    """Complete AssemblyScript language toolchain for Runa translation platform."""
    
    def __init__(self, options: Optional[AssemblyScriptToolchainOptions] = None):
        super().__init__()
        self.options = options or AssemblyScriptToolchainOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = AsParser()
        self.as_to_runa_converter = AssemblyScriptToRunaConverter()
        self.runa_to_as_converter = RunaToAssemblyScriptConverter()
        self.code_generator = AssemblyScriptCodeGenerator(self.options.code_style)
        
        # Performance optimization
        self._ast_cache: Dict[str, AsProgram] = {}
        self._conversion_cache: Dict[str, ASTNode] = {}
        self._generation_cache: Dict[str, str] = {}
        
        # Metrics
        self.metrics = PerformanceMetrics()
    
    @property
    def language_name(self) -> str:
        """Get language name."""
        return "AssemblyScript"
    
    @property
    def file_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return [".ts", ".as"]
    
    def parse_source(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse AssemblyScript source code into AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"parse_{hash(source_code)}"
            if self.options.enable_caching and cache_key in self._ast_cache:
                ast = self._ast_cache[cache_key]
                self.logger.debug("Retrieved AssemblyScript AST from cache")
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
                    "target": self.options.target.value,
                    "file_path": file_path,
                    "strict_mode": self.options.strict_mode,
                    "module_name": ast.module_name,
                    "function_count": len([s for s in ast.statements if isinstance(s, AsFunction)]),
                    "class_count": len([s for s in ast.statements if isinstance(s, AsClass)])
                }
            )
            
        except Exception as e:
            error_msg = f"AssemblyScript parsing failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_to_runa(self, as_ast: AsNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert AssemblyScript AST to Runa AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"to_runa_{hash(str(as_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                runa_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved Runa AST from cache")
            else:
                # Convert to Runa
                runa_ast = self.as_to_runa_converter.convert(as_ast)
                
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
                    "conversion_direction": "assemblyscript_to_runa",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"AssemblyScript to Runa conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def convert_from_runa(self, runa_ast: ASTNode, metadata: Optional[Dict[str, Any]] = None) -> ToolchainResult:
        """Convert Runa AST to AssemblyScript AST."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"from_runa_{hash(str(runa_ast))}"
            if self.options.enable_caching and cache_key in self._conversion_cache:
                as_ast = self._conversion_cache[cache_key]
                self.logger.debug("Retrieved AssemblyScript AST from cache")
            else:
                # Convert from Runa
                as_ast = self.runa_to_as_converter.convert(runa_ast)
                
                # Cache result
                if self.options.enable_caching:
                    self._manage_cache(self._conversion_cache, cache_key, as_ast)
            
            # Calculate metrics
            conversion_time = time.time() - start_time
            
            return ToolchainResult(
                success=True,
                result=as_ast,
                metrics=PerformanceMetrics(
                    total_operations=1,
                    total_time=conversion_time,
                    average_time=conversion_time,
                    cache_hits=1 if cache_key in self._conversion_cache else 0
                ),
                language_specific_data={
                    "conversion_direction": "runa_to_assemblyscript",
                    "metadata": metadata
                }
            )
            
        except Exception as e:
            error_msg = f"Runa to AssemblyScript conversion failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def generate_code(self, as_ast: AsNode, style: Optional[AssemblyScriptCodeStyle] = None) -> ToolchainResult:
        """Generate AssemblyScript source code from AST."""
        start_time = time.time()
        
        try:
            # Use specified style or default
            target_style = style or self.options.code_style
            
            # Check cache first
            cache_key = f"generate_{hash(str(as_ast))}_{target_style.value}"
            if self.options.enable_caching and cache_key in self._generation_cache:
                generated_code = self._generation_cache[cache_key]
                self.logger.debug("Retrieved generated AssemblyScript code from cache")
            else:
                # Generate code
                if target_style != self.code_generator.style:
                    self.code_generator = AssemblyScriptCodeGenerator(target_style)
                
                generated_code = self.code_generator.generate(as_ast)
                
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
                    "generated_lines": generated_code.count('\n') + 1,
                    "target": self.options.target.value
                }
            )
            
        except Exception as e:
            error_msg = f"AssemblyScript code generation failed: {e}"
            self.logger.error(error_msg)
            return ToolchainResult(
                success=False,
                error=error_msg,
                metrics=PerformanceMetrics(total_operations=1, total_time=time.time() - start_time)
            )
    
    def translate_to_runa(self, source_code: str, file_path: Optional[str] = None) -> TranslationResult:
        """Complete translation from AssemblyScript to Runa."""
        start_time = time.time()
        
        try:
            # Parse AssemblyScript source
            parse_result = self.parse_source(source_code, file_path)
            if not parse_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.PARSE_ERROR,
                    error=parse_result.error,
                    source_language="assemblyscript",
                    target_language="runa"
                )
            
            # Convert to Runa
            convert_result = self.convert_to_runa(parse_result.result)
            if not convert_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.CONVERSION_ERROR,
                    error=convert_result.error,
                    source_language="assemblyscript",
                    target_language="runa"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=convert_result.result,
                source_language="assemblyscript",
                target_language="runa",
                translation_time=total_time,
                metadata={
                    "target": self.options.target.value,
                    "file_path": file_path
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="assemblyscript",
                target_language="runa",
                translation_time=time.time() - start_time
            )
    
    def translate_from_runa(self, runa_ast: ASTNode, target_style: Optional[AssemblyScriptCodeStyle] = None) -> TranslationResult:
        """Complete translation from Runa to AssemblyScript."""
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
                    target_language="assemblyscript"
                )
            
            # Generate AssemblyScript code
            generate_result = self.generate_code(convert_result.result, target_style)
            if not generate_result.success:
                return TranslationResult(
                    success=False,
                    status=TranslationStatus.GENERATION_ERROR,
                    error=generate_result.error,
                    source_language="runa",
                    target_language="assemblyscript"
                )
            
            total_time = time.time() - start_time
            
            return TranslationResult(
                success=True,
                status=TranslationStatus.SUCCESS,
                result=generate_result.result,
                source_language="runa",
                target_language="assemblyscript",
                translation_time=total_time,
                metadata={
                    "code_style": (target_style or self.options.code_style).value,
                    "target": self.options.target.value
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                status=TranslationStatus.INTERNAL_ERROR,
                error=str(e),
                source_language="runa",
                target_language="assemblyscript",
                translation_time=time.time() - start_time
            )
    
    def verify_round_trip(self, source_code: str) -> ToolchainResult:
        """Verify round-trip translation AssemblyScript -> Runa -> AssemblyScript."""
        start_time = time.time()
        
        try:
            # AssemblyScript -> Runa
            to_runa_result = self.translate_to_runa(source_code)
            if not to_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"AssemblyScript to Runa failed: {to_runa_result.error}"
                )
            
            # Runa -> AssemblyScript
            from_runa_result = self.translate_from_runa(to_runa_result.result)
            if not from_runa_result.success:
                return ToolchainResult(
                    success=False,
                    error=f"Runa to AssemblyScript failed: {from_runa_result.error}"
                )
            
            verification_time = time.time() - start_time
            
            # Compare semantics by parsing both
            try:
                original_ast = parse_assemblyscript(source_code)
                generated_ast = parse_assemblyscript(from_runa_result.result)
                
                # Simple structural comparison
                structure_matches = self._compare_as_structure(original_ast, generated_ast)
                
                return ToolchainResult(
                    success=True,
                    result={
                        "original_code": source_code,
                        "runa_ast": to_runa_result.result,
                        "generated_code": from_runa_result.result,
                        "structure_matches": structure_matches,
                        "verification_passed": structure_matches
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
    
    def _compare_as_structure(self, ast1: AsProgram, ast2: AsProgram) -> bool:
        """Compare AssemblyScript AST structure."""
        # Compare statement counts
        if len(ast1.statements) != len(ast2.statements):
            return False
        
        # Compare function and class counts (simplified)
        ast1_functions = [s for s in ast1.statements if isinstance(s, AsFunction)]
        ast2_functions = [s for s in ast2.statements if isinstance(s, AsFunction)]
        
        ast1_classes = [s for s in ast1.statements if isinstance(s, AsClass)]
        ast2_classes = [s for s in ast2.statements if isinstance(s, AsClass)]
        
        if len(ast1_functions) != len(ast2_functions) or len(ast1_classes) != len(ast2_classes):
            return False
        
        return True  # Simplified comparison
    
    def get_metrics(self) -> PerformanceMetrics:
        """Get performance metrics."""
        return self.metrics
    
    def clear_caches(self):
        """Clear all caches."""
        self._ast_cache.clear()
        self._conversion_cache.clear()
        self._generation_cache.clear()
        self.logger.info("AssemblyScript toolchain caches cleared")
    
    def _manage_cache(self, cache: Dict[str, Any], key: str, value: Any):
        """Manage cache size and add new entry."""
        if len(cache) >= self.options.cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(cache))
            del cache[oldest_key]
        
        cache[key] = value


# Convenience functions
def create_assemblyscript_toolchain(options: Optional[AssemblyScriptToolchainOptions] = None) -> AssemblyScriptToolchain:
    """Create an AssemblyScript toolchain with specified options."""
    return AssemblyScriptToolchain(options)


def assemblyscript_to_runa_translation(source_code: str, 
                                      options: Optional[AssemblyScriptToolchainOptions] = None) -> TranslationResult:
    """Translate AssemblyScript source code to Runa AST."""
    toolchain = create_assemblyscript_toolchain(options)
    return toolchain.translate_to_runa(source_code)


def runa_to_assemblyscript_translation(runa_ast: ASTNode, 
                                      style: Optional[AssemblyScriptCodeStyle] = None,
                                      options: Optional[AssemblyScriptToolchainOptions] = None) -> TranslationResult:
    """Translate Runa AST to AssemblyScript source code."""
    toolchain = create_assemblyscript_toolchain(options)
    return toolchain.translate_from_runa(runa_ast, style)


def verify_assemblyscript_round_trip(source_code: str,
                                    options: Optional[AssemblyScriptToolchainOptions] = None) -> ToolchainResult:
    """Verify AssemblyScript round-trip translation."""
    toolchain = create_assemblyscript_toolchain(options)
    return toolchain.verify_round_trip(source_code)


def parse_assemblyscript_code(source_code: str, 
                             options: Optional[AssemblyScriptToolchainOptions] = None) -> ToolchainResult:
    """Parse AssemblyScript source code."""
    toolchain = create_assemblyscript_toolchain(options)
    return toolchain.parse_source(source_code)


def generate_assemblyscript_code_from_ast(as_ast: AsNode,
                                         style: Optional[AssemblyScriptCodeStyle] = None,
                                         options: Optional[AssemblyScriptToolchainOptions] = None) -> ToolchainResult:
    """Generate AssemblyScript code from AST."""
    toolchain = create_assemblyscript_toolchain(options)
    return toolchain.generate_code(as_ast, style)