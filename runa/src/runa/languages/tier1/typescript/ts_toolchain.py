#!/usr/bin/env python3
"""
TypeScript Language Toolchain

Complete TypeScript toolchain providing parsing, conversion, generation,
and round-trip verification capabilities for the Runa universal translation system.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
import time
import difflib

from .ts_parser import parse_typescript
from .ts_converter import ts_to_runa, runa_to_ts
from .ts_generator import TSCodeGenerator, generate_typescript
from .ts_ast import TSNode, TSProgram
from ....core.runa_ast import Program
from ...shared.base_toolchain import BaseLanguageToolchain, LanguageMetadata, ToolchainResult
from ...core.translation_result import TranslationResult, TranslationError


class TypeScriptToolchain(BaseLanguageToolchain):
    """Complete TypeScript language toolchain."""
    
    def __init__(self):
        super().__init__("typescript", "1.0.0")
        self.generator = TSCodeGenerator()
    
    @property
    def metadata(self) -> LanguageMetadata:
        """Get TypeScript language metadata."""
        return LanguageMetadata(
            name="TypeScript",
            id="typescript",
            tier=1,
            file_extensions=[".ts", ".tsx", ".d.ts"],
            mime_types=["application/typescript", "text/typescript"],
            features={
                # JavaScript features
                "async_await": True,
                "arrow_functions": True,
                "classes": True,
                "destructuring": True,
                "generators": True,
                "modules": True,
                "template_literals": True,
                "promises": True,
                "spread_operator": True,
                "optional_chaining": True,
                "nullish_coalescing": True,
                "dynamic_imports": True,
                "bigint": True,
                "private_fields": True,
                "top_level_await": True,
                
                # TypeScript-specific features
                "type_annotations": True,
                "interfaces": True,
                "generics": True,
                "enums": True,
                "namespaces": True,
                "decorators": True,
                "type_guards": True,
                "mapped_types": True,
                "conditional_types": True,
                "utility_types": True,
                "declaration_merging": True,
                "module_augmentation": True,
                "abstract_classes": True,
                "access_modifiers": True,
                "readonly_properties": True,
                "optional_properties": True,
                "union_types": True,
                "intersection_types": True,
                "tuple_types": True,
                "literal_types": True,
                "index_signatures": True,
                "function_overloads": True,
                "type_assertions": True,
                "type_predicates": True,
                "keyof_operator": True,
                "typeof_operator": True,
                "indexed_access_types": True,
                "satisfies_operator": True,
            },
            description="TypeScript is a strongly typed programming language that builds on JavaScript by adding static type definitions.",
            homepage="https://www.typescriptlang.org/",
            specification="https://github.com/Microsoft/TypeScript/blob/main/doc/spec.md"
        )
    
    @property
    def supported_features(self) -> Dict[str, bool]:
        """Get supported TypeScript features."""
        return self.metadata.features
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse TypeScript source code into AST."""
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
            ast = parse_typescript(source_code)
            
            # Cache result if enabled
            result = ToolchainResult(
                success=True,
                data=ast,
                metadata={
                    "lines": lines,
                    "file_path": file_path,
                    "parse_time_ms": (time.time() - start_time) * 1000
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
    
    def to_runa(self, language_ast: TSProgram) -> TranslationResult:
        """Convert TypeScript AST to Runa AST."""
        start_time = time.time()
        
        try:
            runa_ast = ts_to_runa(language_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "to_runa")
            
            return TranslationResult(
                success=True,
                source_language="typescript",
                target_language="runa",
                source_ast=language_ast,
                target_ast=runa_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "ts_to_runa",
                    "type_information_preserved": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "to_runa")
            
            return TranslationResult(
                success=False,
                source_language="typescript",
                target_language="runa",
                source_ast=language_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert TypeScript to Runa: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def from_runa(self, runa_ast: Program) -> TranslationResult:
        """Convert Runa AST to TypeScript AST."""
        start_time = time.time()
        
        try:
            ts_ast = runa_to_ts(runa_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "from_runa")
            
            return TranslationResult(
                success=True,
                source_language="runa",
                target_language="typescript",
                source_ast=runa_ast,
                target_ast=ts_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "runa_to_ts",
                    "type_information_preserved": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "from_runa")
            
            return TranslationResult(
                success=False,
                source_language="runa",
                target_language="typescript",
                source_ast=runa_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert Runa to TypeScript: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def generate(self, language_ast: TSProgram, **options) -> ToolchainResult:
        """Generate TypeScript source code from AST."""
        start_time = time.time()
        
        try:
            # Configure generator options
            indent_size = options.get("indent_size", 2)
            use_semicolons = options.get("use_semicolons", True)
            use_trailing_comma = options.get("use_trailing_comma", True)
            style = options.get("style", "standard")
            minify = options.get("minify", False)
            
            # Generate code
            if minify:
                code = generate_typescript(language_ast, minify=True)
            else:
                generator = TSCodeGenerator(
                    indent_size=indent_size,
                    use_semicolons=use_semicolons,
                    use_trailing_comma=use_trailing_comma
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
                    "use_semicolons": use_semicolons,
                    "use_trailing_comma": use_trailing_comma,
                    "style": style,
                    "minified": minify
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
    
    # Abstract method implementations
    def _compare_ast_structure(self, ast1: TSProgram, ast2: TSProgram) -> bool:
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
    
    def _compare_semantics(self, ast1: TSProgram, ast2: TSProgram) -> bool:
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
    
    def _find_differences(self, ast1: TSProgram, ast2: TSProgram) -> List[str]:
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
    
    def _detect_features(self, ast: TSProgram) -> List[str]:
        """Detect TypeScript features used in AST."""
        features = []
        
        try:
            # Simple feature detection by traversing AST
            def traverse(node):
                if hasattr(node, 'type'):
                    node_type = node.type
                    
                    if hasattr(node_type, 'name'):
                        type_name = node_type.name
                        
                        # Detect TypeScript-specific features
                        if 'TYPE_ANNOTATION' in type_name:
                            features.append('type_annotations')
                        elif 'INTERFACE' in type_name:
                            features.append('interfaces')
                        elif 'ENUM' in type_name:
                            features.append('enums')
                        elif 'NAMESPACE' in type_name:
                            features.append('namespaces')
                        elif 'DECORATOR' in type_name:
                            features.append('decorators')
                        elif 'UNION_TYPE' in type_name:
                            features.append('union_types')
                        elif 'INTERSECTION_TYPE' in type_name:
                            features.append('intersection_types')
                        elif 'TUPLE_TYPE' in type_name:
                            features.append('tuple_types')
                        elif 'GENERIC' in type_name or 'TYPE_PARAMETER' in type_name:
                            features.append('generics')
                        elif 'MAPPED_TYPE' in type_name:
                            features.append('mapped_types')
                        elif 'CONDITIONAL_TYPE' in type_name:
                            features.append('conditional_types')
                        elif 'KEYOF' in type_name:
                            features.append('keyof_operator')
                        elif 'TYPEOF' in type_name:
                            features.append('typeof_operator')
                        elif 'TYPE_ASSERTION' in type_name:
                            features.append('type_assertions')
                        elif 'ABSTRACT' in type_name:
                            features.append('abstract_classes')
                        elif any(modifier in type_name for modifier in ['PRIVATE', 'PROTECTED', 'PUBLIC']):
                            features.append('access_modifiers')
                        elif 'READONLY' in type_name:
                            features.append('readonly_properties')
                        elif 'OPTIONAL' in type_name:
                            features.append('optional_properties')
                        elif 'SATISFIES' in type_name:
                            features.append('satisfies_operator')
                        
                        # Detect inherited JavaScript features
                        if 'ARROW_FUNCTION' in type_name:
                            features.append('arrow_functions')
                        elif 'ASYNC' in type_name or 'AWAIT' in type_name:
                            features.append('async_await')
                        elif 'CLASS' in type_name:
                            features.append('classes')
                        elif 'TEMPLATE' in type_name:
                            features.append('template_literals')
                        elif 'YIELD' in type_name:
                            features.append('generators')
                        elif 'IMPORT' in type_name or 'EXPORT' in type_name:
                            features.append('modules')
                
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
    
    def _calculate_complexity(self, ast: TSProgram) -> int:
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
                        
                        # TypeScript-specific complexity
                        if any(construct in type_name for construct in [
                            'GENERIC', 'INTERFACE', 'ENUM', 'NAMESPACE', 'DECORATOR',
                            'UNION_TYPE', 'INTERSECTION_TYPE', 'MAPPED_TYPE', 'CONDITIONAL_TYPE'
                        ]):
                            complexity += 3
                        elif any(construct in type_name for construct in [
                            'FUNCTION', 'CLASS', 'LOOP', 'CONDITIONAL', 'TRY'
                        ]):
                            complexity += 2
                        elif 'TYPE_ANNOTATION' in type_name:
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
def parse_ts(source_code: str) -> TSProgram:
    """Parse TypeScript source code to AST."""
    return parse_typescript(source_code)


def generate_ts(ast: TSProgram, **options) -> str:
    """Generate TypeScript source code from AST."""
    return generate_typescript(ast, **options)


def ts_round_trip_verify(source_code: str, **options) -> bool:
    """Verify round-trip translation preserves semantics."""
    toolchain = TypeScriptToolchain()
    result = toolchain.round_trip_verify(source_code, **options)
    return result.success


def ts_to_runa_translate(source_code: str) -> Program:
    """Translate TypeScript source code to Runa AST."""
    toolchain = TypeScriptToolchain()
    
    # Parse TypeScript
    parse_result = toolchain.parse(source_code)
    if not parse_result.success:
        raise ValueError(f"Parse error: {parse_result.error}")
    
    # Convert to Runa
    conversion_result = toolchain.to_runa(parse_result.data)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    return conversion_result.target_ast


def runa_to_ts_translate(runa_ast: Program, **options) -> str:
    """Translate Runa AST to TypeScript source code."""
    toolchain = TypeScriptToolchain()
    
    # Convert from Runa
    conversion_result = toolchain.from_runa(runa_ast)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    # Generate TypeScript code
    generation_result = toolchain.generate(conversion_result.target_ast, **options)
    if not generation_result.success:
        raise ValueError(f"Generation error: {generation_result.error}")
    
    return generation_result.data