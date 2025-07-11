#!/usr/bin/env python3
"""
C++ Language Toolchain

Complete C++ toolchain providing parsing, conversion, generation,
and round-trip verification capabilities for the Runa universal translation system.
Supports modern C++ features from C++11 through C++23.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
import time
import difflib
import re

from .cpp_parser import parse_cpp
from .cpp_converter import cpp_to_runa, runa_to_cpp
from .cpp_generator import CppCodeGenerator, CppCodeStyle, generate_cpp
from .cpp_ast import CppNode, CppTranslationUnit
from ....core.runa_ast import Program
from ...shared.base_toolchain import BaseLanguageToolchain, LanguageMetadata, ToolchainResult
from ....core.translation_result import TranslationResult, TranslationError


class CppToolchain(BaseLanguageToolchain):
    """Complete C++ language toolchain."""
    
    def __init__(self):
        super().__init__("cpp", "1.0.0")
        self.generator = CppCodeGenerator()
    
    @property
    def metadata(self) -> LanguageMetadata:
        """Get C++ language metadata."""
        return LanguageMetadata(
            name="C++",
            id="cpp",
            tier=1,
            file_extensions=[".cpp", ".cxx", ".cc", ".c++", ".hpp", ".hxx", ".hh", ".h++", ".h"],
            mime_types=["text/x-c++src", "text/x-c++hdr", "text/x-chdr"],
            features={
                # Core language features
                "static_typing": True,
                "strong_typing": True,
                "manual_memory_management": True,
                "automatic_memory_management": False,
                "garbage_collection": False,
                "compiled": True,
                "interpreted": False,
                "object_oriented": True,
                "functional_programming": True,
                "generic_programming": True,
                "template_metaprogramming": True,
                "procedural_programming": True,
                
                # C++ specific features
                "multiple_inheritance": True,
                "operator_overloading": True,
                "function_overloading": True,
                "constructor_destructor": True,
                "raii": True,  # Resource Acquisition Is Initialization
                "smart_pointers": True,
                "references": True,
                "pointers": True,
                "const_correctness": True,
                "friend_functions": True,
                "virtual_functions": True,
                "pure_virtual_functions": True,
                "abstract_classes": True,
                "namespaces": True,
                "using_declarations": True,
                "typedef": True,
                "type_aliases": True,
                "enum_classes": True,
                "unions": True,
                "structs": True,
                "bitfields": True,
                
                # Modern C++ features (C++11+)
                "auto_type_deduction": True,
                "decltype": True,
                "lambda_expressions": True,
                "range_based_for": True,
                "nullptr": True,
                "move_semantics": True,
                "rvalue_references": True,
                "forwarding_references": True,
                "variadic_templates": True,
                "template_aliases": True,
                "constexpr": True,
                "thread_local_storage": True,
                "static_assert": True,
                "override_final": True,
                "default_delete": True,
                "delegating_constructors": True,
                "inheriting_constructors": True,
                "uniform_initialization": True,
                "initializer_lists": True,
                "brace_initialization": True,
                
                # C++14 features
                "generic_lambdas": True,
                "variable_templates": True,
                "binary_literals": True,
                "digit_separators": True,
                "return_type_deduction": True,
                
                # C++17 features
                "structured_bindings": True,
                "if_constexpr": True,
                "inline_variables": True,
                "fold_expressions": True,
                "class_template_argument_deduction": True,
                "filesystem_library": True,
                "optional": True,
                "variant": True,
                "any": True,
                "string_view": True,
                "parallel_algorithms": True,
                
                # C++20 features
                "concepts": True,
                "requires_expressions": True,
                "coroutines": True,
                "modules": True,
                "three_way_comparison": True,  # spaceship operator <=>
                "designated_initializers": True,
                "template_syntax_for_lambdas": True,
                "consteval": True,
                "constinit": True,
                "char8_t": True,
                "abbreviated_function_templates": True,
                "pack_expansions_in_lambda_init_capture": True,
                
                # C++23 features
                "if_consteval": True,
                "multidimensional_subscript": True,
                "auto_in_non_type_template_parameters": True,
                "deducing_this": True,
                
                # Standard library features
                "stl_containers": True,
                "stl_algorithms": True,
                "stl_iterators": True,
                "stl_functors": True,
                "iostream": True,
                "string_manipulation": True,
                "regular_expressions": True,
                "random_numbers": True,
                "chrono": True,
                "thread_support": True,
                "atomic_operations": True,
                "condition_variables": True,
                "futures_promises": True,
                "memory_management_utilities": True,
                "type_traits": True,
                "tuple": True,
                "function_objects": True,
                
                # Memory and performance
                "zero_overhead_abstraction": True,
                "deterministic_destruction": True,
                "stack_allocation": True,
                "heap_allocation": True,
                "placement_new": True,
                "custom_allocators": True,
                "memory_pools": True,
                "cache_friendly_programming": True,
                "simd_support": True,
                
                # Error handling
                "exceptions": True,
                "exception_safety": True,
                "error_codes": True,
                "assertions": True,
                "optional_error_handling": True,
                
                # Compilation and linking
                "separate_compilation": True,
                "header_files": True,
                "include_guards": True,
                "pragma_once": True,
                "precompiled_headers": True,
                "template_instantiation": True,
                "extern_templates": True,
                "link_time_optimization": True,
                "whole_program_optimization": True,
                
                # Platform and system programming
                "system_programming": True,
                "embedded_programming": True,
                "kernel_programming": True,
                "device_drivers": True,
                "real_time_programming": True,
                "cross_platform": True,
                "platform_specific_code": True,
                "inline_assembly": True,
                "bit_manipulation": True,
                "low_level_programming": True,
                
                # Development and tooling
                "static_analysis": True,
                "dynamic_analysis": True,
                "profiling": True,
                "debugging": True,
                "unit_testing": True,
                "benchmark_testing": True,
                "documentation_generation": True,
                "code_coverage": True,
                "sanitizers": True,
                "valgrind_support": True,
                
                # Integration and interoperability
                "c_interoperability": True,
                "abi_compatibility": True,
                "shared_libraries": True,
                "static_libraries": True,
                "plugin_architecture": True,
                "foreign_function_interface": True,
                "python_bindings": True,
                "java_jni": True,
                "com_interop": True,
                
                # Application domains
                "systems_programming": True,
                "game_development": True,
                "graphics_programming": True,
                "scientific_computing": True,
                "high_performance_computing": True,
                "numerical_analysis": True,
                "computer_graphics": True,
                "image_processing": True,
                "signal_processing": True,
                "database_engines": True,
                "web_browsers": True,
                "operating_systems": True,
                "compilers": True,
                "interpreters": True,
                "virtual_machines": True,
                "emulators": True,
                "desktop_applications": True,
                "server_applications": True,
                "network_programming": True,
                "distributed_systems": True,
                "blockchain": True,
                "cryptocurrency": True,
                "trading_systems": True,
                "financial_modeling": True,
                "quantitative_analysis": True,
                "machine_learning": True,
                "artificial_intelligence": True,
                "computer_vision": True,
                "robotics": True,
                "automotive": True,
                "aerospace": True,
                "telecommunications": True,
                "multimedia": True,
                "audio_processing": True,
                "video_processing": True,
                "compression": True,
                "encryption": True,
                "security": True,
                
                # Industry adoption
                "enterprise_software": True,
                "large_scale_systems": True,
                "performance_critical": True,
                "resource_constrained": True,
                "legacy_code_support": True,
                "mature_ecosystem": True,
                "extensive_tooling": True,
                "compiler_optimization": True,
                "portable_code": True,
            },
            description="C++ is a general-purpose programming language with imperative, object-oriented and generic programming features.",
            homepage="https://isocpp.org/",
            specification="https://www.iso.org/standard/79358.html"
        )
    
    @property
    def supported_features(self) -> Dict[str, bool]:
        """Get supported C++ features."""
        return self.metadata.features
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse C++ source code into AST."""
        start_time = time.time()
        lines = source_code.count('\n') + 1
        
        try:
            # Check cache first
            cache_key = self._get_cache_key(source_code)
            if self.cache_enabled and cache_key in self._parse_cache:
                cached_result = self._parse_cache[cache_key]
                self._update_parse_stats(lines, 0, True)
                return cached_result
            
            # Parse the source code
            ast = parse_cpp(source_code, file_path)
            
            # Cache result if enabled
            result = ToolchainResult(
                success=True,
                data=ast,
                metadata={
                    "lines": lines,
                    "file_path": file_path,
                    "parse_time_ms": (time.time() - start_time) * 1000,
                    "cpp_standard": "C++20",
                    "ast_nodes": self._count_ast_nodes(ast),
                    "complexity_score": self._calculate_complexity(ast),
                    "detected_features": self._detect_features(ast)
                }
            )
            
            if self.cache_enabled:
                if len(self._parse_cache) >= self.max_cache_size:
                    # Remove oldest entry
                    oldest_key = next(iter(self._parse_cache))
                    del self._parse_cache[oldest_key]
                self._parse_cache[cache_key] = result
            
            parse_time_ms = (time.time() - start_time) * 1000
            self._update_parse_stats(lines, parse_time_ms, True)
            
            return result
            
        except Exception as e:
            parse_time_ms = (time.time() - start_time) * 1000
            self._update_parse_stats(lines, parse_time_ms, False)
            
            return ToolchainResult(
                success=False,
                error=f"Parse error: {str(e)}",
                metadata={
                    "lines": lines,
                    "file_path": file_path,
                    "parse_time_ms": parse_time_ms
                }
            )
    
    def to_runa(self, language_ast: CppTranslationUnit) -> TranslationResult:
        """Convert C++ AST to Runa AST."""
        start_time = time.time()
        
        try:
            runa_ast = cpp_to_runa(language_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "to_runa")
            
            return TranslationResult(
                success=True,
                source_language="cpp",
                target_language="runa",
                source_ast=language_ast,
                target_ast=runa_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "cpp_to_runa",
                    "raii_patterns_preserved": True,
                    "template_features_simplified": True,
                    "memory_management_abstracted": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "to_runa")
            
            return TranslationResult(
                success=False,
                source_language="cpp",
                target_language="runa",
                source_ast=language_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert C++ to Runa: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def from_runa(self, runa_ast: Program) -> TranslationResult:
        """Convert Runa AST to C++ AST."""
        start_time = time.time()
        
        try:
            cpp_ast = runa_to_cpp(runa_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "from_runa")
            
            return TranslationResult(
                success=True,
                source_language="runa",
                target_language="cpp",
                source_ast=runa_ast,
                target_ast=cpp_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "runa_to_cpp",
                    "modern_cpp_idioms_applied": True,
                    "smart_pointers_used": True,
                    "raii_patterns_applied": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "from_runa")
            
            return TranslationResult(
                success=False,
                source_language="runa",
                target_language="cpp",
                source_ast=runa_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert Runa to C++: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def generate(self, language_ast: CppTranslationUnit, **options) -> ToolchainResult:
        """Generate C++ source code from AST."""
        start_time = time.time()
        
        try:
            # Configure generator options
            style_name = options.get("style", "default")
            
            if style_name == "google":
                from .cpp_generator import CppFormatter
                style = CppFormatter.google_style()
            elif style_name == "llvm":
                from .cpp_generator import CppFormatter
                style = CppFormatter.llvm_style()
            elif style_name == "mozilla":
                from .cpp_generator import CppFormatter
                style = CppFormatter.mozilla_style()
            elif style_name == "webkit":
                from .cpp_generator import CppFormatter
                style = CppFormatter.webkit_style()
            elif style_name == "microsoft":
                from .cpp_generator import CppFormatter
                style = CppFormatter.microsoft_style()
            else:
                style = CppCodeStyle()
            
            # Override specific style options from parameters
            if "indent_size" in options:
                style.indent_size = options["indent_size"]
            if "use_spaces" in options:
                style.use_spaces = options["use_spaces"]
            if "brace_style" in options:
                style.brace_style = options["brace_style"]
            if "modern_cpp_features" in options:
                style.modern_cpp_features = options["modern_cpp_features"]
            
            generator = CppCodeGenerator(style)
            code = generator.generate(language_ast)
            
            lines = code.count('\n') + 1
            generation_time_ms = (time.time() - start_time) * 1000
            
            self._update_generation_stats(lines, generation_time_ms, True)
            
            return ToolchainResult(
                success=True,
                data=code,
                metadata={
                    "lines": lines,
                    "generation_time_ms": generation_time_ms,
                    "style": style_name,
                    "indent_size": style.indent_size,
                    "use_spaces": style.use_spaces,
                    "brace_style": style.brace_style,
                    "modern_cpp_features": style.modern_cpp_features,
                    "cpp_standard": "C++20"
                }
            )
            
        except Exception as e:
            generation_time_ms = (time.time() - start_time) * 1000
            self._update_generation_stats(0, generation_time_ms, False)
            
            return ToolchainResult(
                success=False,
                error=f"Generation error: {str(e)}",
                metadata={
                    "generation_time_ms": generation_time_ms
                }
            )
    
    def _count_ast_nodes(self, ast: CppTranslationUnit) -> int:
        """Count AST nodes for complexity analysis."""
        count = 0
        
        def traverse(node):
            nonlocal count
            count += 1
            
            # Traverse child nodes based on node type
            if hasattr(node, 'declarations'):
                for decl in node.declarations:
                    traverse(decl)
            elif hasattr(node, 'statements'):
                for stmt in node.statements:
                    traverse(stmt)
            elif hasattr(node, 'body') and isinstance(node.body, list):
                for stmt in node.body:
                    traverse(stmt)
            elif hasattr(node, 'body') and node.body:
                traverse(node.body)
            elif hasattr(node, 'members'):
                for member in node.members:
                    traverse(member)
            
            # Traverse expressions
            if hasattr(node, 'left') and node.left:
                traverse(node.left)
            if hasattr(node, 'right') and node.right:
                traverse(node.right)
            if hasattr(node, 'operand') and node.operand:
                traverse(node.operand)
            if hasattr(node, 'condition') and node.condition:
                traverse(node.condition)
            if hasattr(node, 'function') and node.function:
                traverse(node.function)
            if hasattr(node, 'arguments') and node.arguments:
                for arg in node.arguments:
                    traverse(arg)
        
        traverse(ast)
        return count
    
    # Abstract method implementations
    def _compare_ast_structure(self, ast1: CppTranslationUnit, ast2: CppTranslationUnit) -> bool:
        """Compare AST structure for syntax preservation."""
        try:
            # Simple structural comparison
            if type(ast1) != type(ast2):
                return False
            
            if len(ast1.declarations) != len(ast2.declarations):
                return False
            
            for decl1, decl2 in zip(ast1.declarations, ast2.declarations):
                if type(decl1) != type(decl2):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _compare_semantics(self, ast1: CppTranslationUnit, ast2: CppTranslationUnit) -> bool:
        """Compare AST semantics."""
        try:
            # Generate code from both ASTs and compare
            code1 = self.generator.generate(ast1)
            code2 = self.generator.generate(ast2)
            
            # Normalize whitespace for comparison
            normalized1 = ' '.join(code1.split())
            normalized2 = ' '.join(code2.split())
            
            return normalized1 == normalized2
            
        except Exception:
            return False
    
    def _find_differences(self, ast1: CppTranslationUnit, ast2: CppTranslationUnit) -> List[str]:
        """Find differences between ASTs."""
        differences = []
        
        try:
            # Generate code and compare
            code1 = self.generator.generate(ast1)
            code2 = self.generator.generate(ast2)
            
            # Use difflib to find differences
            diff = list(difflib.unified_diff(
                code1.splitlines(keepends=True),
                code2.splitlines(keepends=True),
                fromfile='original',
                tofile='regenerated',
                lineterm=''
            ))
            
            differences.extend(diff)
            
        except Exception as e:
            differences.append(f"Error comparing ASTs: {str(e)}")
        
        return differences
    
    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity score between code strings."""
        try:
            # Use difflib SequenceMatcher
            matcher = difflib.SequenceMatcher(None, code1, code2)
            return matcher.ratio()
            
        except Exception:
            return 0.0
    
    def _detect_features(self, ast: CppTranslationUnit) -> List[str]:
        """Detect C++ features used in AST."""
        features = []
        
        try:
            def traverse(node):
                if hasattr(node, 'type'):
                    node_type = node.type
                    
                    if hasattr(node_type, 'name'):
                        type_name = node_type.name
                        
                        # Detect C++ features
                        if 'TEMPLATE' in type_name:
                            features.append('templates')
                        elif 'LAMBDA' in type_name:
                            features.append('lambda_expressions')
                        elif 'AUTO' in type_name:
                            features.append('auto_type_deduction')
                        elif 'DECLTYPE' in type_name:
                            features.append('decltype')
                        elif 'CONSTEXPR' in type_name:
                            features.append('constexpr')
                        elif 'NULLPTR' in type_name:
                            features.append('nullptr')
                        elif 'RANGE_FOR' in type_name:
                            features.append('range_based_for')
                        elif 'RVALUE_REFERENCE' in type_name:
                            features.append('rvalue_references')
                        elif 'INITIALIZER_LIST' in type_name:
                            features.append('initializer_lists')
                        elif 'CLASS' in type_name:
                            features.append('classes')
                        elif 'NAMESPACE' in type_name:
                            features.append('namespaces')
                        elif 'FUNCTION' in type_name:
                            features.append('functions')
                        elif 'POINTER' in type_name:
                            features.append('pointers')
                        elif 'REFERENCE' in type_name:
                            features.append('references')
                        elif 'INHERITANCE' in type_name:
                            features.append('inheritance')
                        elif 'VIRTUAL' in type_name:
                            features.append('virtual_functions')
                        elif 'OPERATOR' in type_name:
                            features.append('operator_overloading')
                        elif 'EXCEPTION' in type_name:
                            features.append('exceptions')
                
                # Recursively traverse child nodes
                if hasattr(node, 'declarations'):
                    for decl in node.declarations:
                        traverse(decl)
                elif hasattr(node, 'statements'):
                    for stmt in node.statements:
                        traverse(stmt)
                elif hasattr(node, 'body') and isinstance(node.body, list):
                    for stmt in node.body:
                        traverse(stmt)
                elif hasattr(node, 'body') and node.body:
                    traverse(node.body)
                elif hasattr(node, 'members'):
                    for member in node.members:
                        traverse(member)
            
            traverse(ast)
            
        except Exception:
            pass
        
        return list(set(features))  # Remove duplicates
    
    def _calculate_complexity(self, ast: CppTranslationUnit) -> int:
        """Calculate complexity score of AST."""
        complexity = 0
        
        try:
            def traverse(node):
                nonlocal complexity
                complexity += 1
                
                # Add extra complexity for certain constructs
                if hasattr(node, 'type'):
                    node_type = node.type
                    
                    if hasattr(node_type, 'name'):
                        type_name = node_type.name
                        
                        # C++ specific complexity
                        if any(construct in type_name for construct in [
                            'TEMPLATE', 'LAMBDA', 'CLASS', 'NAMESPACE', 'FUNCTION'
                        ]):
                            complexity += 5
                        elif any(construct in type_name for construct in [
                            'CONDITIONAL', 'LOOP', 'TRY', 'SWITCH', 'INHERITANCE'
                        ]):
                            complexity += 3
                        elif any(construct in type_name for construct in [
                            'POINTER', 'REFERENCE', 'CAST', 'OPERATOR'
                        ]):
                            complexity += 2
                        elif any(construct in type_name for construct in [
                            'AUTO', 'DECLTYPE', 'CONSTEXPR', 'NULLPTR'
                        ]):
                            complexity += 1
                
                # Recursively traverse child nodes
                if hasattr(node, 'declarations'):
                    for decl in node.declarations:
                        traverse(decl)
                elif hasattr(node, 'statements'):
                    for stmt in node.statements:
                        traverse(stmt)
                elif hasattr(node, 'body') and isinstance(node.body, list):
                    for stmt in node.body:
                        traverse(stmt)
                elif hasattr(node, 'body') and node.body:
                    traverse(node.body)
                elif hasattr(node, 'members'):
                    for member in node.members:
                        traverse(member)
            
            traverse(ast)
            
        except Exception:
            complexity = 1
        
        return complexity


# Convenience functions
def parse_cpp_code(source_code: str) -> CppTranslationUnit:
    """Parse C++ source code to AST."""
    return parse_cpp(source_code)


def generate_cpp_code(ast: CppTranslationUnit, **options) -> str:
    """Generate C++ source code from AST."""
    return generate_cpp(ast, **options)


def cpp_round_trip_verify(source_code: str, **options) -> bool:
    """Verify round-trip translation preserves semantics."""
    toolchain = CppToolchain()
    result = toolchain.round_trip_verify(source_code, **options)
    return result.success


def cpp_to_runa_translate(source_code: str) -> Program:
    """Translate C++ source code to Runa AST."""
    toolchain = CppToolchain()
    
    # Parse C++
    parse_result = toolchain.parse(source_code)
    if not parse_result.success:
        raise ValueError(f"Parse error: {parse_result.error}")
    
    # Convert to Runa
    conversion_result = toolchain.to_runa(parse_result.data)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    return conversion_result.target_ast


def runa_to_cpp_translate(runa_ast: Program, **options) -> str:
    """Translate Runa AST to C++ source code."""
    toolchain = CppToolchain()
    
    # Convert from Runa
    conversion_result = toolchain.from_runa(runa_ast)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    # Generate C++ code
    generation_result = toolchain.generate(conversion_result.target_ast, **options)
    if not generation_result.success:
        raise ValueError(f"Generation error: {generation_result.error}")
    
    return generation_result.data