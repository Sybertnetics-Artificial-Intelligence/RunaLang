"""
Runa Compiler Package

High-performance universal programming language compiler with:
- Natural language understanding
- Vector-based semantic analysis
- Multi-pass optimization
- Performance monitoring
- <100ms compilation target
"""

from typing import Dict, Any, List, Optional, Tuple
from .lexer import RunaLexer as Lexer, Token, TokenType
from .parser import RunaParser as Parser, ASTNode, Program, Statement, Expression
from .semantic_analyzer import SemanticAnalyzer, SemanticError, TypeInfo, Symbol
from .bytecode_generator import BytecodeGenerator, BytecodeModule, Instruction, Opcode

__all__ = [
    # Lexer
    'Lexer',
    'Token', 
    'TokenType',
    
    # Parser
    'Parser',
    'ASTNode',
    'Program',
    'Statement',
    'Expression',
    
    # Semantic Analyzer
    'SemanticAnalyzer',
    'SemanticError',
    'TypeInfo',
    'Symbol',
    
    # Bytecode Generator
    'BytecodeGenerator',
    'BytecodeModule',
    'Instruction',
    'Opcode',
]


class Compiler:
    """
    Complete Runa compiler with all phases.
    
    Features:
    - Lexical analysis with natural language support
    - Recursive descent parsing with error recovery
    - Vector-based semantic analysis
    - Multi-pass bytecode generation with optimization
    - Performance monitoring and profiling
    - <100ms compilation target
    """
    
    def __init__(self):
        # Don't initialize lexer and parser here - they need source code
        self.semantic_analyzer = SemanticAnalyzer()
        self.bytecode_generator = BytecodeGenerator(self.semantic_analyzer)
        
        # Performance metrics
        self.compilation_time = 0.0
        self.phase_times = {}
    
    def compile(self, source_code: str) -> BytecodeModule:
        """
        Compile Runa source code to bytecode.
        
        Args:
            source_code: Runa source code as string
            
        Returns:
            BytecodeModule ready for execution
            
        Raises:
            Exception: If compilation fails
        """
        import time
        start_time = time.perf_counter()
        
        try:
            # Phase 1: Lexical Analysis
            phase_start = time.perf_counter()
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            self.phase_times['lexical_analysis'] = time.perf_counter() - phase_start
            
            # Phase 2: Parsing
            phase_start = time.perf_counter()
            parser = Parser(tokens)
            ast = parser.parse()
            self.phase_times['parsing'] = time.perf_counter() - phase_start
            
            # Phase 3: Semantic Analysis
            phase_start = time.perf_counter()
            semantic_success = self.semantic_analyzer.analyze(ast)
            self.phase_times['semantic_analysis'] = time.perf_counter() - phase_start
            
            if not semantic_success:
                errors = self.semantic_analyzer.get_errors()
                error_messages = [f"{error.message} at line {error.node.line}" for error in errors]
                raise Exception(f"Semantic analysis failed:\n" + "\n".join(error_messages))
            
            # Phase 4: Bytecode Generation
            phase_start = time.perf_counter()
            bytecode = self.bytecode_generator.generate(ast)
            self.phase_times['bytecode_generation'] = time.perf_counter() - phase_start
            
            # Update total compilation time
            self.compilation_time = time.perf_counter() - start_time
            
            return bytecode
            
        except Exception as e:
            self.compilation_time = time.perf_counter() - start_time
            raise Exception(f"Compilation failed: {e}")
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get detailed performance metrics for all compilation phases."""
        metrics = {
            'total_compilation_time_ms': self.compilation_time * 1000,
            'target_time_ms': 100.0,  # <100ms target
            'performance_ratio': (self.compilation_time * 1000) / 100.0,
        }
        
        # Add phase-specific metrics
        for phase, time_taken in self.phase_times.items():
            metrics[f'{phase}_time_ms'] = time_taken * 1000
        
        # Add bytecode generator metrics
        bc_metrics = self.bytecode_generator.get_performance_metrics()
        for key, value in bc_metrics.items():
            metrics[f'bytecode_{key}'] = value
        
        return metrics
    
    def validate_performance_target(self) -> bool:
        """Validate that compilation meets <100ms performance target."""
        return self.compilation_time * 1000 < 100.0 