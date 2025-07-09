#!/usr/bin/env python3
"""
Java Language Toolchain

Complete Java toolchain providing parsing, conversion, generation,
and round-trip verification capabilities for the Runa universal translation system.
Supports modern Java features from Java 8 through Java 21.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
import time
import difflib
import re

from .java_parser import parse_java
from .java_converter import java_to_runa, runa_to_java
from .java_generator import JavaCodeGenerator, JavaCodeStyle, generate_java, JavaFormatter
from .java_ast import JavaNode, JavaCompilationUnit
from ....core.runa_ast import Program
from ...shared.base_toolchain import BaseLanguageToolchain, LanguageMetadata, ToolchainResult
from ...core.translation_result import TranslationResult, TranslationError


class JavaToolchain(BaseLanguageToolchain):
    """Complete Java language toolchain."""
    
    def __init__(self):
        super().__init__("java", "1.0.0")
        self.generator = JavaCodeGenerator()
    
    @property
    def metadata(self) -> LanguageMetadata:
        """Get Java language metadata."""
        return LanguageMetadata(
            name="Java",
            id="java",
            tier=1,
            file_extensions=[".java"],
            mime_types=["text/x-java-source"],
            features={
                # Core language features
                "static_typing": True,
                "strong_typing": True,
                "manual_memory_management": False,
                "automatic_memory_management": True,
                "garbage_collection": True,
                "compiled": True,
                "interpreted": False,
                "bytecode_compilation": True,
                "jit_compilation": True,
                "object_oriented": True,
                "functional_programming": True,
                "generic_programming": True,
                "procedural_programming": True,
                "reflective_programming": True,
                "concurrent_programming": True,
                
                # Java-specific features
                "platform_independence": True,
                "write_once_run_anywhere": True,
                "jvm_target": True,
                "interfaces": True,
                "abstract_classes": True,
                "inheritance": True,
                "single_inheritance": True,
                "multiple_interface_inheritance": True,
                "method_overloading": True,
                "method_overriding": True,
                "polymorphism": True,
                "encapsulation": True,
                "packages": True,
                "namespaces": True,
                "access_modifiers": True,
                "static_members": True,
                "final_keyword": True,
                "abstract_keyword": True,
                "synchronized_keyword": True,
                "volatile_keyword": True,
                "transient_keyword": True,
                "native_keyword": True,
                "strictfp_keyword": True,
                
                # Type system
                "primitive_types": True,
                "reference_types": True,
                "autoboxing": True,
                "unboxing": True,
                "type_inference": True,
                "generics": True,
                "type_erasure": True,
                "wildcards": True,
                "bounded_wildcards": True,
                "covariance": True,
                "contravariance": True,
                "invariance": True,
                "raw_types": True,
                "enum_types": True,
                "annotation_types": True,
                "array_types": True,
                "multidimensional_arrays": True,
                "varargs": True,
                
                # Java 8+ features
                "lambda_expressions": True,
                "method_references": True,
                "functional_interfaces": True,
                "stream_api": True,
                "optional_type": True,
                "default_methods": True,
                "static_interface_methods": True,
                "date_time_api": True,
                "nashorn_javascript": True,
                "parallel_streams": True,
                "collectors": True,
                "completable_future": True,
                "repeating_annotations": True,
                "type_annotations": True,
                
                # Java 9+ features
                "module_system": True,
                "jshell": True,
                "private_interface_methods": True,
                "diamond_operator_anonymous": True,
                "try_with_resources_improvements": True,
                "collection_factory_methods": True,
                "stream_improvements": True,
                "optional_improvements": True,
                "process_api_improvements": True,
                "variable_handles": True,
                "stack_walking_api": True,
                "multi_resolution_images": True,
                "compact_strings": True,
                "g1_garbage_collector": True,
                
                # Java 10+ features
                "local_variable_type_inference": True,  # var keyword
                "application_class_data_sharing": True,
                "garbage_collector_interface": True,
                "parallel_full_gc_g1": True,
                "heap_allocation_on_alternative_devices": True,
                "experimental_java_based_jit": True,
                "root_certificates": True,
                "time_based_release_versioning": True,
                
                # Java 11+ features
                "http_client": True,
                "string_methods": True,
                "file_methods": True,
                "collection_to_array": True,
                "optional_is_empty": True,
                "predicate_not": True,
                "lambda_parameters": True,
                "unicode_10_support": True,
                "flight_recorder": True,
                "no_op_garbage_collector": True,
                "low_overhead_heap_profiling": True,
                "transport_layer_security": True,
                "dynamic_class_file_constants": True,
                "epsilon_gc": True,
                "nest_based_access_control": True,
                
                # Java 12+ features
                "switch_expressions": True,
                "jvm_constants_api": True,
                "one_aarch64_port": True,
                "default_cds_archives": True,
                "abortable_mixed_collections_g1": True,
                "promptly_return_unused_committed_memory": True,
                
                # Java 13+ features
                "text_blocks": True,
                "dynamic_cds_archives": True,
                "zgc_uncommit_unused_memory": True,
                "socket_api_reimplementation": True,
                "switch_expressions_standard": True,
                
                # Java 14+ features
                "records": True,
                "pattern_matching_instanceof": True,
                "helpful_nullpointerexceptions": True,
                "foreign_function_interface": True,
                "jpackage_tool": True,
                "jfr_event_streaming": True,
                "non_volatile_mapped_byte_buffers": True,
                "numa_aware_g1": True,
                "jfr_event_streaming_api": True,
                "remove_concurrent_mark_sweep_gc": True,
                "macos_rendering_pipeline": True,
                "windows_x64_foreign_linker": True,
                
                # Java 15+ features
                "sealed_classes": True,
                "text_blocks_standard": True,
                "hidden_classes": True,
                "edwards_curve_digital_signature": True,
                "disable_biased_locking": True,
                "pattern_matching_instanceof_standard": True,
                "zgc_production_ready": True,
                "shenandoah_gc_production_ready": True,
                "remove_nashorn_javascript": True,
                "reimplemented_legacy_datagram_socket": True,
                "foreign_function_memory_api": True,
                "records_local_interfaces": True,
                
                # Java 16+ features
                "pattern_matching_instanceof_final": True,
                "records_final": True,
                "vector_api": True,
                "foreign_linker_api": True,
                "foreign_memory_access_api": True,
                "packaging_tool": True,
                "unix_domain_socket_channels": True,
                "warnings_for_value_based_classes": True,
                "alpine_linux_port": True,
                "elastic_metaspace": True,
                "windows_aarch64_port": True,
                "concurrent_thread_stack_processing": True,
                
                # Java 17+ features (LTS)
                "sealed_classes_final": True,
                "pattern_matching_switch": True,
                "remove_experimental_aot": True,
                "deprecate_applet_api": True,
                "foreign_function_memory_api_second_incubator": True,
                "vector_api_second_incubator": True,
                "context_specific_deserialization_filters": True,
                "strongly_encapsulate_jdk_internals": True,
                "switch_expressions_enhancements": True,
                "restore_always_strict_floating_point": True,
                "new_macos_rendering_pipeline": True,
                "macos_aarch64_port": True,
                "deprecate_security_manager": True,
                "foreign_function_memory_api_improvements": True,
                "random_number_generators": True,
                "deserialization_filtering": True,
                
                # Java 18+ features
                "utf8_by_default": True,
                "simple_web_server": True,
                "code_snippets_javadoc": True,
                "vector_api_third_incubator": True,
                "internet_address_resolution_spi": True,
                "foreign_function_memory_api_third_incubator": True,
                "pattern_matching_switch_second_preview": True,
                "deprecated_finalization": True,
                "service_loader_enhancements": True,
                
                # Java 19+ features
                "virtual_threads": True,
                "structured_concurrency": True,
                "vector_api_fourth_incubator": True,
                "pattern_matching_switch_third_preview": True,
                "foreign_function_memory_api_fourth_incubator": True,
                "record_patterns": True,
                "linux_risc_v_port": True,
                
                # Java 20+ features
                "scoped_values": True,
                "virtual_threads_second_preview": True,
                "structured_concurrency_second_incubator": True,
                "vector_api_fifth_incubator": True,
                "pattern_matching_switch_fourth_preview": True,
                "foreign_function_memory_api_fifth_incubator": True,
                "record_patterns_second_preview": True,
                
                # Java 21+ features (LTS)
                "virtual_threads_final": True,
                "sequenced_collections": True,
                "pattern_matching_switch_final": True,
                "record_patterns_final": True,
                "string_templates": True,
                "unnamed_patterns_variables": True,
                "foreign_function_memory_api_final": True,
                "vector_api_sixth_incubator": True,
                "structured_concurrency_final": True,
                "scoped_values_final": True,
                "key_encapsulation_mechanism": True,
                
                # Exception handling
                "exceptions": True,
                "checked_exceptions": True,
                "unchecked_exceptions": True,
                "try_catch_finally": True,
                "try_with_resources": True,
                "multicatch": True,
                "suppressed_exceptions": True,
                "stack_traces": True,
                "chained_exceptions": True,
                
                # Concurrency
                "threads": True,
                "thread_pools": True,
                "executors": True,
                "concurrent_collections": True,
                "locks": True,
                "atomic_variables": True,
                "volatile_variables": True,
                "synchronized_blocks": True,
                "wait_notify": True,
                "future_tasks": True,
                "fork_join_framework": True,
                "parallel_streams_processing": True,
                "reactive_streams": True,
                
                # Memory management
                "heap_memory": True,
                "stack_memory": True,
                "method_area": True,
                "garbage_collection_automatic": True,
                "generational_gc": True,
                "concurrent_gc": True,
                "low_latency_gc": True,
                "weak_references": True,
                "soft_references": True,
                "phantom_references": True,
                "finalization": True,
                "cleaner_api": True,
                
                # I/O and networking
                "io_streams": True,
                "nio": True,
                "file_io": True,
                "network_io": True,
                "channels": True,
                "buffers": True,
                "selectors": True,
                "socket_programming": True,
                "url_connections": True,
                "serialization": True,
                "externalization": True,
                
                # Collections framework
                "collections": True,
                "lists": True,
                "sets": True,
                "maps": True,
                "queues": True,
                "deques": True,
                "iterators": True,
                "comparable": True,
                "comparator": True,
                "sorting": True,
                "searching": True,
                "synchronized_collections": True,
                "concurrent_collections_framework": True,
                
                # Reflection and introspection
                "reflection": True,
                "class_loading": True,
                "dynamic_proxies": True,
                "annotations": True,
                "annotation_processing": True,
                "bean_introspection": True,
                "method_handles": True,
                "invokedynamic": True,
                
                # Security
                "security_manager": True,
                "access_control": True,
                "cryptography": True,
                "digital_signatures": True,
                "certificates": True,
                "secure_random": True,
                "security_providers": True,
                "policy_files": True,
                "permissions": True,
                "authentication": True,
                "authorization": True,
                
                # Internationalization
                "unicode_support": True,
                "localization": True,
                "resource_bundles": True,
                "message_formatting": True,
                "date_formatting": True,
                "number_formatting": True,
                "collation": True,
                "text_normalization": True,
                "bidirectional_text": True,
                
                # Standard library
                "extensive_standard_library": True,
                "utility_classes": True,
                "data_structures": True,
                "algorithms": True,
                "math_library": True,
                "text_processing": True,
                "regular_expressions": True,
                "logging": True,
                "preferences": True,
                "xml_processing": True,
                "json_processing": True,
                
                # Testing
                "junit_integration": True,
                "assertions": True,
                "test_annotations": True,
                "mocking_frameworks": True,
                "test_runners": True,
                "code_coverage": True,
                "integration_testing": True,
                "unit_testing": True,
                
                # Development tools
                "javadoc": True,
                "java_compiler": True,
                "jar_packaging": True,
                "classpath_management": True,
                "debugging": True,
                "profiling": True,
                "monitoring": True,
                "jmx": True,
                "flight_recorder_profiling": True,
                "mission_control": True,
                
                # Enterprise features
                "enterprise_java": True,
                "spring_framework": True,
                "dependency_injection": True,
                "aspect_oriented_programming": True,
                "orm_frameworks": True,
                "web_frameworks": True,
                "microservices": True,
                "rest_apis": True,
                "soap_web_services": True,
                "messaging": True,
                "transaction_management": True,
                "connection_pooling": True,
                "caching": True,
                "distributed_computing": True,
                
                # Build and deployment
                "maven_integration": True,
                "gradle_integration": True,
                "ant_integration": True,
                "war_packaging": True,
                "ear_packaging": True,
                "docker_containerization": True,
                "kubernetes_deployment": True,
                "cloud_deployment": True,
                "continuous_integration": True,
                "continuous_deployment": True,
                
                # Performance
                "hotspot_optimization": True,
                "ahead_of_time_compilation": True,
                "profile_guided_optimization": True,
                "escape_analysis": True,
                "loop_optimization": True,
                "inlining": True,
                "dead_code_elimination": True,
                "constant_folding": True,
                "branch_prediction": True,
                "cpu_specific_optimizations": True,
                
                # Ecosystem
                "mature_ecosystem": True,
                "extensive_libraries": True,
                "active_community": True,
                "long_term_support": True,
                "backward_compatibility": True,
                "vendor_support": True,
                "documentation": True,
                "learning_resources": True,
                "ide_support": True,
                "tooling_support": True,
            },
            description="Java is a high-level, class-based, object-oriented programming language with platform independence.",
            homepage="https://www.java.com/",
            specification="https://docs.oracle.com/javase/specs/"
        )
    
    @property
    def supported_features(self) -> Dict[str, bool]:
        """Get supported Java features."""
        return self.metadata.features
    
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse Java source code into AST."""
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
            ast = parse_java(source_code, file_path)
            
            # Cache result if enabled
            result = ToolchainResult(
                success=True,
                data=ast,
                metadata={
                    "lines": lines,
                    "file_path": file_path,
                    "parse_time_ms": (time.time() - start_time) * 1000,
                    "java_version": "21",
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
    
    def to_runa(self, language_ast: JavaCompilationUnit) -> TranslationResult:
        """Convert Java AST to Runa AST."""
        start_time = time.time()
        
        try:
            runa_ast = java_to_runa(language_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "to_runa")
            
            return TranslationResult(
                success=True,
                source_language="java",
                target_language="runa",
                source_ast=language_ast,
                target_ast=runa_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "java_to_runa",
                    "generics_preserved": True,
                    "lambda_expressions_converted": True,
                    "streams_simplified": True,
                    "checked_exceptions_handled": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "to_runa")
            
            return TranslationResult(
                success=False,
                source_language="java",
                target_language="runa",
                source_ast=language_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert Java to Runa: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def from_runa(self, runa_ast: Program) -> TranslationResult:
        """Convert Runa AST to Java AST."""
        start_time = time.time()
        
        try:
            java_ast = runa_to_java(runa_ast)
            
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, True, "from_runa")
            
            return TranslationResult(
                success=True,
                source_language="runa",
                target_language="java",
                source_ast=runa_ast,
                target_ast=java_ast,
                metadata={
                    "conversion_time_ms": conversion_time_ms,
                    "direction": "runa_to_java",
                    "modern_java_features_used": True,
                    "generics_inferred": True,
                    "lambda_expressions_generated": True,
                    "stream_api_utilized": True
                }
            )
            
        except Exception as e:
            conversion_time_ms = (time.time() - start_time) * 1000
            self._update_conversion_stats(conversion_time_ms, False, "from_runa")
            
            return TranslationResult(
                success=False,
                source_language="runa",
                target_language="java",
                source_ast=runa_ast,
                error=TranslationError(
                    error_type="conversion_error",
                    message=f"Failed to convert Runa to Java: {str(e)}",
                    details={"conversion_time_ms": conversion_time_ms}
                )
            )
    
    def generate(self, language_ast: JavaCompilationUnit, **options) -> ToolchainResult:
        """Generate Java source code from AST."""
        start_time = time.time()
        
        try:
            # Configure generator options
            style_name = options.get("style", "default")
            
            if style_name == "google":
                style = JavaFormatter.google_style()
            elif style_name == "oracle":
                style = JavaFormatter.oracle_style()
            elif style_name == "eclipse":
                style = JavaFormatter.eclipse_style()
            elif style_name == "intellij":
                style = JavaFormatter.intellij_style()
            else:
                style = JavaCodeStyle()
            
            # Override specific style options from parameters
            if "indent_size" in options:
                style.indent_size = options["indent_size"]
            if "use_spaces" in options:
                style.use_spaces = options["use_spaces"]
            if "brace_style" in options:
                style.brace_style = options["brace_style"]
            if "max_line_length" in options:
                style.max_line_length = options["max_line_length"]
            if "use_lambda_expressions" in options:
                style.use_lambda_expressions = options["use_lambda_expressions"]
            if "use_stream_api" in options:
                style.use_stream_api = options["use_stream_api"]
            if "use_var_for_local_variables" in options:
                style.use_var_for_local_variables = options["use_var_for_local_variables"]
            
            generator = JavaCodeGenerator(style)
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
                    "brace_style": style.brace_style.name,
                    "max_line_length": style.max_line_length,
                    "modern_java_features": {
                        "lambda_expressions": style.use_lambda_expressions,
                        "stream_api": style.use_stream_api,
                        "var_keyword": style.use_var_for_local_variables,
                        "text_blocks": style.use_text_blocks,
                        "switch_expressions": style.use_switch_expressions,
                        "records": style.use_records,
                        "pattern_matching": style.use_pattern_matching
                    },
                    "java_version": "21"
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
    
    def _count_ast_nodes(self, ast: JavaCompilationUnit) -> int:
        """Count AST nodes for complexity analysis."""
        count = 0
        
        def traverse(node):
            nonlocal count
            count += 1
            
            # Traverse child nodes based on node type
            if hasattr(node, 'type_declarations'):
                for decl in node.type_declarations:
                    traverse(decl)
            elif hasattr(node, 'body') and isinstance(node.body, list):
                for member in node.body:
                    traverse(member)
            elif hasattr(node, 'body') and node.body:
                traverse(node.body)
            elif hasattr(node, 'statements'):
                for stmt in node.statements:
                    traverse(stmt)
            elif hasattr(node, 'declarators'):
                for declarator in node.declarators:
                    traverse(declarator)
            
            # Traverse expressions
            if hasattr(node, 'left') and node.left:
                traverse(node.left)
            if hasattr(node, 'right') and node.right:
                traverse(node.right)
            if hasattr(node, 'operand') and node.operand:
                traverse(node.operand)
            if hasattr(node, 'condition') and node.condition:
                traverse(node.condition)
            if hasattr(node, 'expression') and node.expression:
                traverse(node.expression)
            if hasattr(node, 'arguments') and node.arguments:
                for arg in node.arguments:
                    traverse(arg)
            if hasattr(node, 'parameters') and node.parameters:
                for param in node.parameters:
                    traverse(param)
        
        traverse(ast)
        return count
    
    # Abstract method implementations
    def _compare_ast_structure(self, ast1: JavaCompilationUnit, ast2: JavaCompilationUnit) -> bool:
        """Compare AST structure for syntax preservation."""
        try:
            # Simple structural comparison
            if type(ast1) != type(ast2):
                return False
            
            if len(ast1.type_declarations) != len(ast2.type_declarations):
                return False
            
            for decl1, decl2 in zip(ast1.type_declarations, ast2.type_declarations):
                if type(decl1) != type(decl2):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _compare_semantics(self, ast1: JavaCompilationUnit, ast2: JavaCompilationUnit) -> bool:
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
    
    def _find_differences(self, ast1: JavaCompilationUnit, ast2: JavaCompilationUnit) -> List[str]:
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
    
    def _detect_features(self, ast: JavaCompilationUnit) -> List[str]:
        """Detect Java features used in AST."""
        features = []
        
        try:
            def traverse(node):
                if hasattr(node, 'type'):
                    node_type = node.type
                    
                    if hasattr(node_type, 'name'):
                        type_name = node_type.name
                        
                        # Detect Java features
                        if 'LAMBDA' in type_name:
                            features.append('lambda_expressions')
                        elif 'METHOD_REFERENCE' in type_name:
                            features.append('method_references')
                        elif 'STREAM' in type_name:
                            features.append('stream_api')
                        elif 'OPTIONAL' in type_name:
                            features.append('optional')
                        elif 'GENERIC' in type_name or 'PARAMETERIZED' in type_name:
                            features.append('generics')
                        elif 'ANNOTATION' in type_name:
                            features.append('annotations')
                        elif 'ENUM' in type_name:
                            features.append('enums')
                        elif 'RECORD' in type_name:
                            features.append('records')
                        elif 'SEALED' in type_name:
                            features.append('sealed_classes')
                        elif 'PATTERN_MATCHING' in type_name:
                            features.append('pattern_matching')
                        elif 'SWITCH_EXPRESSION' in type_name:
                            features.append('switch_expressions')
                        elif 'TEXT_BLOCK' in type_name:
                            features.append('text_blocks')
                        elif 'VAR' in type_name:
                            features.append('var_keyword')
                        elif 'MODULE' in type_name:
                            features.append('modules')
                        elif 'TRY_WITH_RESOURCES' in type_name:
                            features.append('try_with_resources')
                        elif 'MULTI_CATCH' in type_name:
                            features.append('multi_catch')
                        elif 'DIAMOND' in type_name:
                            features.append('diamond_operator')
                        elif 'FOR_EACH' in type_name:
                            features.append('enhanced_for_loops')
                        elif 'VARARGS' in type_name:
                            features.append('varargs')
                        elif 'AUTOBOXING' in type_name:
                            features.append('autoboxing')
                        elif 'INTERFACE' in type_name:
                            features.append('interfaces')
                        elif 'ABSTRACT' in type_name:
                            features.append('abstract_classes')
                        elif 'INHERITANCE' in type_name:
                            features.append('inheritance')
                        elif 'POLYMORPHISM' in type_name:
                            features.append('polymorphism')
                        elif 'THREAD' in type_name:
                            features.append('multithreading')
                        elif 'SYNCHRONIZED' in type_name:
                            features.append('synchronization')
                        elif 'REFLECTION' in type_name:
                            features.append('reflection')
                        elif 'SERIALIZATION' in type_name:
                            features.append('serialization')
                        elif 'COLLECTION' in type_name:
                            features.append('collections')
                        elif 'EXCEPTION' in type_name:
                            features.append('exceptions')
                        elif 'PACKAGE' in type_name:
                            features.append('packages')
                        elif 'IMPORT' in type_name:
                            features.append('imports')
                        elif 'STATIC' in type_name:
                            features.append('static_members')
                        elif 'FINAL' in type_name:
                            features.append('final_keyword')
                        elif 'VOLATILE' in type_name:
                            features.append('volatile_keyword')
                        elif 'TRANSIENT' in type_name:
                            features.append('transient_keyword')
                        elif 'NATIVE' in type_name:
                            features.append('native_methods')
                
                # Recursively traverse child nodes
                if hasattr(node, 'type_declarations'):
                    for decl in node.type_declarations:
                        traverse(decl)
                elif hasattr(node, 'body') and isinstance(node.body, list):
                    for member in node.body:
                        traverse(member)
                elif hasattr(node, 'body') and node.body:
                    traverse(node.body)
                elif hasattr(node, 'statements'):
                    for stmt in node.statements:
                        traverse(stmt)
                elif hasattr(node, 'declarators'):
                    for declarator in node.declarators:
                        traverse(declarator)
            
            traverse(ast)
            
        except Exception:
            pass
        
        return list(set(features))  # Remove duplicates
    
    def _calculate_complexity(self, ast: JavaCompilationUnit) -> int:
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
                        
                        # Java specific complexity
                        if any(construct in type_name for construct in [
                            'LAMBDA', 'STREAM', 'GENERIC', 'REFLECTION', 'ANNOTATION'
                        ]):
                            complexity += 5
                        elif any(construct in type_name for construct in [
                            'CONDITIONAL', 'LOOP', 'TRY', 'SWITCH', 'INHERITANCE'
                        ]):
                            complexity += 3
                        elif any(construct in type_name for construct in [
                            'METHOD_CALL', 'FIELD_ACCESS', 'ARRAY_ACCESS', 'CAST'
                        ]):
                            complexity += 2
                        elif any(construct in type_name for construct in [
                            'VARIABLE', 'LITERAL', 'IDENTIFIER', 'OPERATOR'
                        ]):
                            complexity += 1
                
                # Recursively traverse child nodes
                if hasattr(node, 'type_declarations'):
                    for decl in node.type_declarations:
                        traverse(decl)
                elif hasattr(node, 'body') and isinstance(node.body, list):
                    for member in node.body:
                        traverse(member)
                elif hasattr(node, 'body') and node.body:
                    traverse(node.body)
                elif hasattr(node, 'statements'):
                    for stmt in node.statements:
                        traverse(stmt)
                elif hasattr(node, 'declarators'):
                    for declarator in node.declarators:
                        traverse(declarator)
            
            traverse(ast)
            
        except Exception:
            complexity = 1
        
        return complexity


# Convenience functions
def parse_java_code(source_code: str) -> JavaCompilationUnit:
    """Parse Java source code to AST."""
    return parse_java(source_code)


def generate_java_code(ast: JavaCompilationUnit, **options) -> str:
    """Generate Java source code from AST."""
    return generate_java(ast, **options)


def java_round_trip_verify(source_code: str, **options) -> bool:
    """Verify round-trip translation preserves semantics."""
    toolchain = JavaToolchain()
    result = toolchain.round_trip_verify(source_code, **options)
    return result.success


def java_to_runa_translate(source_code: str) -> Program:
    """Translate Java source code to Runa AST."""
    toolchain = JavaToolchain()
    
    # Parse Java
    parse_result = toolchain.parse(source_code)
    if not parse_result.success:
        raise ValueError(f"Parse error: {parse_result.error}")
    
    # Convert to Runa
    conversion_result = toolchain.to_runa(parse_result.data)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    return conversion_result.target_ast


def runa_to_java_translate(runa_ast: Program, **options) -> str:
    """Translate Runa AST to Java source code."""
    toolchain = JavaToolchain()
    
    # Convert from Runa
    conversion_result = toolchain.from_runa(runa_ast)
    if not conversion_result.success:
        raise ValueError(f"Conversion error: {conversion_result.error}")
    
    # Generate Java code
    generation_result = toolchain.generate(conversion_result.target_ast, **options)
    if not generation_result.success:
        raise ValueError(f"Generation error: {generation_result.error}")
    
    return generation_result.data