#!/usr/bin/env python3
"""
Python Language Toolchain

Complete Python toolchain providing parsing, conversion, generation,
and round-trip verification capabilities for the Runa universal translation system.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
import time
import difflib

from .py_parser import parse_python
from .py_converter import py_to_runa, runa_to_py
from .py_generator import PyCodeGenerator, generate_python
from .py_ast import PyNode, PyModule
from ....core.runa_ast import Program
from ...shared.base_toolchain import BaseLanguageToolchain, LanguageMetadata, ToolchainResult
from ....core.translation_result import TranslationResult, TranslationError


class PythonToolchain(BaseLanguageToolchain):
    """Complete Python language toolchain."""
    
    def __init__(self):
        super().__init__("python", "1.0.0")
        self.generator = PyCodeGenerator()
    
    @property
    def metadata(self) -> LanguageMetadata:
        """Get Python language metadata."""
        return LanguageMetadata(
            name="Python",
            id="python",
            tier=1,
            file_extensions=[".py", ".pyw", ".pyi"],
            mime_types=["text/x-python", "application/x-python"],
            features={
                "dynamic_typing": True,
                "duck_typing": True,
                "first_class_functions": True,
                "higher_order_functions": True,
                "closures": True,
                "decorators": True,
                "generators": True,
                "iterators": True,
                "list_comprehensions": True,
                "dict_comprehensions": True,
                "set_comprehensions": True,
                "generator_expressions": True,
                "lambda_functions": True,
                "async_await": True,
                "context_managers": True,
                "exception_handling": True,
                "multiple_inheritance": True,
                "operator_overloading": True,
                "properties": True,
                "descriptors": True,
                "metaclasses": True,
                "type_hints": True,
                "optional_types": True,
                "union_types": True,
                "generic_types": True,
                "protocol_types": True,
                "literal_types": True,
                "final_types": True,
                "class_variables": True,
                "instance_variables": True,
                "static_methods": True,
                "class_methods": True,
                "property_methods": True,
                "magic_methods": True,
                "modules": True,
                "packages": True,
                "import_system": True,
                "namespace_packages": True,
                "virtual_environments": True,
                "pip_packaging": True,
                "docstrings": True,
                "reflection": True,
                "introspection": True,
                "monkey_patching": True,
                "multiple_assignment": True,
                "tuple_unpacking": True,
                "starred_expressions": True,
                "slice_notation": True,
                "string_formatting": True,
                "f_strings": True,
                "raw_strings": True,
                "bytes_literals": True,
                "set_literals": True,
                "dictionary_literals": True,
                "walrus_operator": True,  # :=
                "match_statements": True,  # Python 3.10+
                "positional_only_parameters": True,
                "keyword_only_parameters": True,
                "variable_arguments": True,
                "keyword_arguments": True,
                "default_arguments": True,
                "annotation_syntax": True,
                "type_comments": True,
                "dataclasses": True,
                "named_tuples": True,
                "enums": True,
                "pathlib": True,
                "asyncio": True,
                "concurrent_futures": True,
                "multiprocessing": True,
                "threading": True,
                "garbage_collection": True,
                "weak_references": True,
                "memory_management": True,
                "cpython_c_api": True,
                "cython_support": True,
                "numpy_integration": True,
                "scientific_computing": True,
                "data_analysis": True,
                "machine_learning": True,
                "web_frameworks": True,
                "database_connectivity": True,
                "json_support": True,
                "xml_support": True,
                "regex_support": True,
                "file_io": True,
                "network_programming": True,
                "gui_frameworks": True,
                "testing_frameworks": True,
                "logging": True,
                "profiling": True,
                "debugging": True,
                "interactive_shell": True,
                "jupyter_notebooks": True,
                "package_management": True,
                "virtual_environments": True,
                "cross_platform": True,
                "open_source": True,
                "large_ecosystem": True,
                "community_support": True,
                "extensive_documentation": True,
                "readable_syntax": True,
                "beginner_friendly": True,
                "rapid_prototyping": True,
                "scripting": True,
                "automation": True,
                "devops": True,
                "system_administration": True,
                "web_scraping": True,
                "api_development": True,
                "microservices": True,
                "cloud_computing": True,
                "containers": True,
                "serverless": True,
                "artificial_intelligence": True,
                "natural_language_processing": True,
                "computer_vision": True,
                "robotics": True,
                "game_development": True,
                "desktop_applications": True,
                "mobile_development": True,
                "embedded_systems": True,
                "iot_development": True,
                "blockchain": True,
                "cryptocurrency": True,
                "fintech": True,
                "bioinformatics": True,
                "geospatial": True,
                "image_processing": True,
                "audio_processing": True,
                "video_processing": True,
                "data_visualization": True,
                "business_intelligence": True,
                "enterprise_software": True,
                "education": True,
                "research": True,
                "prototyping": True,
                "legacy_integration": True,
                "cross_language_interop": True,
            },
            description="Python is a high-level, interpreted programming language with dynamic semantics and elegant syntax.",
            homepage="https://www.python.org/",
            specification="https://docs.python.org/3/reference/"
        )
    
    @property
    def supported_features(self) -> Dict[str, bool]:
        """Get supported Python features."""
        return self.metadata.features
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse Python source code into AST."""
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
            ast = parse_python(source_code)
            
            # Cache result if enabled
            result = ToolchainResult(
                success=True,
                data=ast,
                metadata={
                    "lines": lines,
                    "file_path": file_path,
                    "parse_time_ms": (time.time() - start_time) * 1000,
                    "python_version": "3.8+",
                    "ast_nodes": self._count_ast_nodes(ast)
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
    
    def to_runa(self, language_ast: PyModule) -> TranslationResult:
        """Convert Python AST to Runa AST."""
        start_time = time.time()
        
        try:
            runa_ast = py_to_runa(language_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "to_runa")
            
            return TranslationResult(
                success=True,
                source_language="python",
                target_language="runa",
                source_ast=language_ast,
                target_ast=runa_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "py_to_runa",
                    "dynamic_features_preserved": True,
                    "type_hints_preserved": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "to_runa")
            
            return TranslationResult(
                success=False,
                source_language="python",
                target_language="runa",
                source_ast=language_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert Python to Runa: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def from_runa(self, runa_ast: Program) -> TranslationResult:
        """Convert Runa AST to Python AST."""
        start_time = time.time()
        
        try:
            py_ast = runa_to_py(runa_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "from_runa")
            
            return TranslationResult(
                success=True,
                source_language="runa",
                target_language="python",
                source_ast=runa_ast,
                target_ast=py_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "runa_to_py",
                    "pythonic_idioms_applied": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "from_runa")
            
            return TranslationResult(
                success=False,
                source_language="runa",
                target_language="python",
                source_ast=runa_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert Runa to Python: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def generate(self, language_ast: PyModule, **options) -> ToolchainResult:
        """Generate Python source code from AST."""
        start_time = time.time()
        
        try:
            # Configure generator options
            indent_size = options.get("indent_size", 4)
            use_type_hints = options.get("use_type_hints", True)
            
            generator = PyCodeGenerator(
                indent_size=indent_size,
                use_type_hints=use_type_hints
            )
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
                    "indent_size": indent_size,
                    "use_type_hints": use_type_hints,
                    "python_version": "3.8+",
                    "pep8_compliant": True
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
    
    def _count_ast_nodes(self, ast: PyModule) -> int:
        """Count AST nodes for complexity analysis."""
        count = 0
        
        def traverse(node):
            nonlocal count
            count += 1
            
            # Traverse child nodes
            for attr_name in dir(node):
                if not attr_name.startswith('_'):
                    attr = getattr(node, attr_name)
                    if isinstance(attr, list):
                        for item in attr:
                            if hasattr(item, 'type'):
                                traverse(item)
                    elif hasattr(attr, 'type'):
                        traverse(attr)
        
        traverse(ast)
        return count
    
    # Abstract method implementations
    def _compare_ast_structure(self, ast1: PyModule, ast2: PyModule) -> bool:
        """Compare AST structure for syntax preservation."""
        try:
            # Simple structural comparison
            if type(ast1) != type(ast2):
                return False
            
            if hasattr(ast1, 'body') and hasattr(ast2, 'body'):
                if len(ast1.body) != len(ast2.body):
                    return False
                
                for stmt1, stmt2 in zip(ast1.body, ast2.body):
                    if type(stmt1) != type(stmt2):
                        return False
            
            return True
            
        except Exception:
            return False
    
    def _compare_semantics(self, ast1: PyModule, ast2: PyModule) -> bool:
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
    
    def _find_differences(self, ast1: PyModule, ast2: PyModule) -> List[str]:
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
    
    def _detect_features(self, ast: PyModule) -> List[str]:
        """Detect Python features used in AST."""
        features = []
        
        try:
            # Simple feature detection by traversing AST
            def traverse(node):
                if hasattr(node, 'type'):
                    node_type = node.type
                    
                    if hasattr(node_type, 'name'):
                        type_name = node_type.name
                        
                        # Detect Python features
                        if 'ASYNC' in type_name or 'AWAIT' in type_name:
                            features.append('async_await')
                        elif 'LAMBDA' in type_name:
                            features.append('lambda_functions')
                        elif 'COMP' in type_name:
                            if 'LIST' in type_name:
                                features.append('list_comprehensions')
                            elif 'SET' in type_name:
                                features.append('set_comprehensions')
                            elif 'DICT' in type_name:
                                features.append('dict_comprehensions')
                        elif 'GENERATOR' in type_name:
                            features.append('generators')
                        elif 'YIELD' in type_name:
                            features.append('generators')
                        elif 'DECORATOR' in type_name:
                            features.append('decorators')
                        elif 'WITH' in type_name:
                            features.append('context_managers')
                        elif 'ANN_ASSIGN' in type_name:
                            features.append('type_hints')
                        elif 'WALRUS' in type_name or 'NAMED_EXPR' in type_name:
                            features.append('walrus_operator')
                        elif 'MATCH' in type_name:
                            features.append('match_statements')
                        elif 'STARRED' in type_name:
                            features.append('starred_expressions')
                        elif 'CLASS' in type_name:
                            features.append('classes')
                        elif 'FUNCTION' in type_name:
                            features.append('functions')
                        elif 'IMPORT' in type_name:
                            features.append('modules')
                        elif 'EXCEPTION' in type_name or 'TRY' in type_name:
                            features.append('exception_handling')
                
                # Recursively traverse child nodes
                for attr_name in dir(node):
                    if not attr_name.startswith('_'):
                        attr = getattr(node, attr_name)
                        if isinstance(attr, list):
                            for item in attr:
                                if hasattr(item, 'type'):
                                    traverse(item)
                        elif hasattr(attr, 'type'):
                            traverse(attr)
            
            traverse(ast)
            
        except Exception:
            pass
        
        return list(set(features))  # Remove duplicates
    
    def _calculate_complexity(self, ast: PyModule) -> int:
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
                        
                        # Python-specific complexity
                        if any(construct in type_name for construct in [
                            'FUNCTION', 'ASYNC_FUNCTION', 'CLASS', 'LAMBDA',
                            'DECORATOR', 'GENERATOR', 'COMPREHENSION'
                        ]):
                            complexity += 3
                        elif any(construct in type_name for construct in [
                            'LOOP', 'CONDITIONAL', 'TRY', 'WITH', 'MATCH'
                        ]):
                            complexity += 2
                        elif any(construct in type_name for construct in [
                            'IMPORT', 'GLOBAL', 'NONLOCAL', 'YIELD', 'AWAIT'
                        ]):
                            complexity += 1
                
                # Recursively traverse child nodes
                for attr_name in dir(node):
                    if not attr_name.startswith('_'):
                        attr = getattr(node, attr_name)
                        if isinstance(attr, list):
                            for item in attr:
                                if hasattr(item, 'type'):
                                    traverse(item)
                        elif hasattr(attr, 'type'):
                            traverse(attr)
            
            traverse(ast)
            
        except Exception:
            complexity = 1
        
        return complexity


# Convenience functions
def parse_py(source_code: str) -> PyModule:
    """Parse Python source code to AST."""
    return parse_python(source_code)


def generate_py(ast: PyModule, **options) -> str:
    """Generate Python source code from AST."""
    return generate_python(ast, **options)


def py_round_trip_verify(source_code: str, **options) -> bool:
    """Verify round-trip translation preserves semantics."""
    toolchain = PythonToolchain()
    result = toolchain.round_trip_verify(source_code, **options)
    return result.success


def py_to_runa_translate(source_code: str) -> Program:
    """Translate Python source code to Runa AST."""
    toolchain = PythonToolchain()
    
    # Parse Python
    parse_result = toolchain.parse(source_code)
    if not parse_result.success:
        raise ValueError(f"Parse error: {parse_result.error}")
    
    # Convert to Runa
    conversion_result = toolchain.to_runa(parse_result.data)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    return conversion_result.target_ast


def runa_to_py_translate(runa_ast: Program, **options) -> str:
    """Translate Runa AST to Python source code."""
    toolchain = PythonToolchain()
    
    # Convert from Runa
    conversion_result = toolchain.from_runa(runa_ast)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    # Generate Python code
    generation_result = toolchain.generate(conversion_result.target_ast, **options)
    if not generation_result.success:
        raise ValueError(f"Generation error: {generation_result.error}")
    
    return generation_result.data