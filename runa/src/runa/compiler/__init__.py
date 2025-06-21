"""
Runa Compiler Package

Complete compilation pipeline from source code to executable bytecode.
Supports universal translation and AI-to-AI communication patterns.
"""

from .lexer import RunaLexer as Lexer, Token, TokenType
from .parser import (
    RunaParser as Parser, ASTNode, Program, Statement, Expression,
    VariableDeclaration, FunctionDeclaration, Identifier, Literal,
    BinaryExpression, CallExpression, IfStatement, ForStatement,
    WhileStatement, ReturnStatement, TypeAnnotation, Parameter
)
from .semantic_analyzer import SemanticAnalyzer, TypeChecker, Symbol, TypeInfo
from .bytecode_generator import BytecodeGenerator, Opcode
from .hybrid_compiler import HybridCompiler
from .universal_translator import UniversalTranslator

from ..runtime import RunaRuntime, get_runtime
from ..vm import RunaVM, get_vm
from ..error_handler import RunaError, RunaCompilationError
from ..performance_monitor import PerformanceMonitor

import time
from typing import Any, Dict, List, Optional, Union


class Compiler:
    """
    Complete Runa compiler with integrated runtime and virtual machine.
    
    Provides end-to-end compilation from Runa source code to execution,
    with performance monitoring and AI-specific optimizations.
    """
    
    def __init__(self, optimize: bool = True, debug: bool = False):
        self.semantic_analyzer = SemanticAnalyzer()
        self.bytecode_generator = BytecodeGenerator()
        self.hybrid_compiler = HybridCompiler()
        self.runtime = get_runtime()
        self.vm = get_vm()
        self.performance_monitor = PerformanceMonitor()
        self.optimize = optimize
        self.debug = debug
        self.compilation_count = 0
        self.total_compilation_time = 0.0
        self.total_execution_time = 0.0
        self.universal_translator = UniversalTranslator()
    
    def compile(self, source_code: str, program_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Compile Runa source code to bytecode.
        
        Args:
            source_code: Runa source code as string
            program_id: Optional program identifier
            
        Returns:
            Dictionary containing compilation results and metadata
        """
        start_time = time.time()
        
        try:
            # Phase 1: Lexical Analysis
            lex_start = time.time()
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            lex_time = time.time() - lex_start
            
            if self.debug:
                print(f"Lexical analysis completed in {lex_time:.4f}s")
                print(f"Generated {len(tokens)} tokens")
            
            # Phase 2: Parsing
            parse_start = time.time()
            parser = Parser(tokens)
            ast = parser.parse()
            parse_time = time.time() - parse_start
            
            if self.debug:
                print(f"Parsing completed in {parse_time:.4f}s")
                print(f"AST has {self._count_nodes(ast)} nodes")
            
            # Phase 3: Semantic Analysis
            semantic_start = time.time()
            semantic_result = self.semantic_analyzer.analyze(ast)
            semantic_time = time.time() - semantic_start
            
            if self.debug:
                print(f"Semantic analysis completed in {semantic_time:.4f}s")
                print(f"Symbol table has {len(semantic_result['symbol_table'].symbols)} symbols")
            
            # Phase 4: Bytecode Generation
            bytecode_start = time.time()
            bytecode = self.bytecode_generator.generate(ast, semantic_result)
            bytecode_time = time.time() - bytecode_start
            
            if self.debug:
                print(f"Bytecode generation completed in {bytecode_time:.4f}s")
                print(f"Generated {len(bytecode)} instructions")
            
            # Compilation completed
            compilation_time = time.time() - start_time
            self.compilation_count += 1
            self.total_compilation_time += compilation_time
            
            # Performance monitoring
            self.performance_monitor.record_operation(
                "compilation", compilation_time,
                {
                    "program_id": program_id or "unknown",
                    "source_length": len(source_code),
                    "token_count": len(tokens),
                    "instruction_count": len(bytecode),
                    "optimize": self.optimize
                }
            )
            
            # Check performance targets
            if compilation_time > 0.1:  # 100ms target
                self.performance_monitor.record_warning(
                    f"Compilation time {compilation_time:.4f}s exceeds 100ms target"
                )
            
            result = {
                "success": True,
                "program_id": program_id or f"program_{int(time.time())}",
                "bytecode": bytecode,
                "ast": ast,
                "semantic_result": semantic_result,
                "tokens": tokens,
                "performance": {
                    "total_compilation_time": compilation_time,
                    "lexical_analysis_time": lex_time,
                    "parsing_time": parse_time,
                    "semantic_analysis_time": semantic_time,
                    "bytecode_generation_time": bytecode_time,
                    "instructions_per_second": len(bytecode) / compilation_time if compilation_time > 0 else 0
                },
                "statistics": {
                    "source_length": len(source_code),
                    "token_count": len(tokens),
                    "ast_node_count": self._count_nodes(ast),
                    "instruction_count": len(bytecode),
                    "symbol_count": len(semantic_result['symbol_table'].symbols)
                }
            }
            
            return result
        
        except Exception as e:
            compilation_time = time.time() - start_time
            self.performance_monitor.record_error(f"Compilation failed: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "program_id": program_id or f"program_{int(time.time())}",
                "performance": {
                    "total_compilation_time": compilation_time
                }
            }
    
    def compile_and_execute(self, source_code: str, program_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Compile and execute Runa source code in one operation.
        
        Args:
            source_code: Runa source code as string
            program_id: Optional program identifier
            
        Returns:
            Dictionary containing compilation and execution results
        """
        # Compile
        compilation_result = self.compile(source_code, program_id)
        
        if not compilation_result["success"]:
            return compilation_result
        
        # Execute
        execution_start = time.time()
        try:
            result = self.vm.execute(compilation_result["bytecode"], program_id)
            execution_time = time.time() - execution_start
            
            self.total_execution_time += execution_time
            
            # Get VM statistics
            vm_stats = self.vm.get_stats()
            
            execution_result = {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "vm_stats": vm_stats,
                "output": self.runtime.get_output()
            }
            
            # Performance monitoring
            self.performance_monitor.record_operation(
                "execution", execution_time,
                {
                    "program_id": program_id or "unknown",
                    "instruction_count": len(compilation_result["bytecode"]),
                    "result_type": type(result).__name__
                }
            )
            
        except Exception as e:
            execution_time = time.time() - execution_start
            self.performance_monitor.record_error(f"Execution failed: {e}")
            
            execution_result = {
                "success": False,
                "error": str(e),
                "execution_time": execution_time
            }
        
        # Combine results
        combined_result = {
            **compilation_result,
            "execution": execution_result
        }
        
        return combined_result
    
    def compile_file(self, file_path: str, program_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Compile Runa source code from a file.
        
        Args:
            file_path: Path to Runa source file
            program_id: Optional program identifier
            
        Returns:
            Dictionary containing compilation results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            return self.compile(source_code, program_id or file_path)
        
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "program_id": program_id or file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading file: {e}",
                "program_id": program_id or file_path
            }
    
    def compile_and_execute_file(self, file_path: str, program_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Compile and execute Runa source code from a file.
        
        Args:
            file_path: Path to Runa source file
            program_id: Optional program identifier
            
        Returns:
            Dictionary containing compilation and execution results
        """
        compilation_result = self.compile_file(file_path, program_id)
        
        if not compilation_result["success"]:
            return compilation_result
        
        return self.compile_and_execute(compilation_result.get("source_code", ""), program_id)
    
    def get_compilation_stats(self) -> Dict[str, Any]:
        """Get compilation statistics."""
        return {
            "compilation_count": self.compilation_count,
            "total_compilation_time": self.total_compilation_time,
            "total_execution_time": self.total_execution_time,
            "average_compilation_time": self.total_compilation_time / self.compilation_count if self.compilation_count > 0 else 0,
            "performance_stats": self.performance_monitor.get_stats(),
            "vm_stats": self.vm.get_stats(),
            "runtime_stats": self.runtime.get_memory_stats()
        }
    
    def reset(self) -> None:
        """Reset compiler state and statistics."""
        self.compilation_count = 0
        self.total_compilation_time = 0.0
        self.total_execution_time = 0.0
        self.performance_monitor.reset()
        self.vm.reset()
        self.runtime.cleanup()
    
    def _count_nodes(self, node: ASTNode) -> int:
        """Count nodes in AST recursively."""
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count
    
    def validate_compilation_target(self, compilation_time: float) -> bool:
        """Validate that compilation meets performance targets."""
        return compilation_time < 0.1  # 100ms target
    
    def optimize_for_ai(self) -> None:
        """Apply AI-specific optimizations to the compiler."""
        self.vm.optimize_for_ai()
        # Additional AI-specific compiler optimizations would go here

    def generate_cpp(self, source_code: str) -> str:
        """Generate C++ code from Runa source using the universal translator."""
        result = self.universal_translator.translate(source_code, target_language="cpp")
        if not result.success or not result.translated_code:
            raise RuntimeError(f"C++ code generation failed: {result.error_message}")
        return result.translated_code


# Convenience functions for common operations

def compile_runa(source_code: str, optimize: bool = True, debug: bool = False) -> Dict[str, Any]:
    """Compile Runa source code with default settings."""
    compiler = Compiler(optimize=optimize, debug=debug)
    return compiler.compile(source_code)


def execute_runa(source_code: str, optimize: bool = True, debug: bool = False) -> Dict[str, Any]:
    """Compile and execute Runa source code with default settings."""
    compiler = Compiler(optimize=optimize, debug=debug)
    return compiler.compile_and_execute(source_code)


def compile_file_runa(file_path: str, optimize: bool = True, debug: bool = False) -> Dict[str, Any]:
    """Compile Runa source file with default settings."""
    compiler = Compiler(optimize=optimize, debug=debug)
    return compiler.compile_file(file_path)


def execute_file_runa(file_path: str, optimize: bool = True, debug: bool = False) -> Dict[str, Any]:
    """Compile and execute Runa source file with default settings."""
    compiler = Compiler(optimize=optimize, debug=debug)
    return compiler.compile_and_execute_file(file_path)


# Export main classes and functions
__all__ = [
    'Compiler',
    'Lexer',
    'Parser', 
    'SemanticAnalyzer',
    'BytecodeGenerator',
    'HybridCompiler',
    'RunaRuntime',
    'RunaVM',
    'compile_runa',
    'execute_runa',
    'compile_file_runa',
    'execute_file_runa'
] 