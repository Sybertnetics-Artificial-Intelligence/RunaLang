"""
Compiler for the Runa programming language.

This module provides the main compiler functionality, integrating the lexer,
parser, and semantic analyzer components.
"""

from typing import List, Tuple, Optional, Dict, Any
import logging
from pathlib import Path

from runa.src.lexer.lexer import Lexer, LexerError
from runa.src.parser.parser import Parser, ParseError
from runa.src.ast import Program
from runa.src.semantic.analyzer import SemanticAnalyzer, SemanticError
from runa.src.semantic.types import TypeSystem
from runa.src.semantic.inference import TypeInferenceEngine


class CompilerError(Exception):
    """Base exception for compiler errors."""
    pass


class CompilationResult:
    """
    Result of a compilation process.
    
    Attributes:
        success: Whether the compilation was successful
        program: The AST of the compiled program (if successful)
        lexer_errors: List of lexer errors (if any)
        parser_errors: List of parser errors (if any)
        semantic_errors: List of semantic errors (if any)
        inferred_types: Dictionary of inferred types (if successful)
    """
    
    def __init__(
        self, 
        success: bool = False,
        program: Optional[Program] = None,
        lexer_errors: Optional[List[LexerError]] = None,
        parser_errors: Optional[List[ParseError]] = None,
        semantic_errors: Optional[List[SemanticError]] = None,
        inferred_types: Optional[Dict[str, str]] = None
    ):
        """Initialize a new CompilationResult."""
        self.success = success
        self.program = program
        self.lexer_errors = lexer_errors or []
        self.parser_errors = parser_errors or []
        self.semantic_errors = semantic_errors or []
        self.inferred_types = inferred_types or {}
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return bool(self.lexer_errors or self.parser_errors or self.semantic_errors)
    
    def error_count(self) -> int:
        """Get the total number of errors."""
        return len(self.lexer_errors) + len(self.parser_errors) + len(self.semantic_errors)
    
    def __str__(self) -> str:
        """Return a string representation of the compilation result."""
        if self.success:
            return f"Compilation successful, AST generated with {len(self.program.statements) if self.program else 0} statements"
        
        error_details = []
        if self.lexer_errors:
            error_details.append(f"{len(self.lexer_errors)} lexical errors")
        if self.parser_errors:
            error_details.append(f"{len(self.parser_errors)} syntax errors")
        if self.semantic_errors:
            error_details.append(f"{len(self.semantic_errors)} semantic errors")
        
        return f"Compilation failed with {', '.join(error_details)}"


class Compiler:
    """
    Compiler for the Runa programming language.
    
    This class orchestrates the compilation process, integrating the lexer,
    parser, and semantic analyzer.
    
    Attributes:
        type_system: The type system used for type checking
        inference_engine: The type inference engine
    """
    
    def __init__(self):
        """Initialize a new Compiler."""
        self.logger = logging.getLogger("runa.compiler")
        self.type_system = TypeSystem()
        self.inference_engine = TypeInferenceEngine(self.type_system)
    
    def compile_string(self, source: str) -> CompilationResult:
        """
        Compile a source string.
        
        Args:
            source: The source code to compile
            
        Returns:
            The compilation result
        """
        try:
            # Lexical analysis
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            if lexer.errors:
                self.logger.error(f"Lexical analysis failed with {len(lexer.errors)} errors")
                return CompilationResult(
                    success=False,
                    lexer_errors=lexer.errors
                )
            
            # Syntax analysis
            parser = Parser(tokens)
            program = parser.parse()
            
            if parser.errors:
                self.logger.error(f"Syntax analysis failed with {len(parser.errors)} errors")
                return CompilationResult(
                    success=False,
                    program=program,
                    parser_errors=parser.errors
                )
            
            # Type inference
            inferred_types = {}
            try:
                inferred_types = self.inference_engine.infer_program(program)
                self.logger.info(f"Type inference completed, inferred {len(inferred_types)} types")
            except Exception as e:
                self.logger.warning(f"Type inference failed: {str(e)}")
            
            # Semantic analysis
            analyzer = SemanticAnalyzer()
            semantic_errors = analyzer.analyze(program)
            
            if semantic_errors:
                self.logger.error(f"Semantic analysis failed with {len(semantic_errors)} errors")
                return CompilationResult(
                    success=False,
                    program=program,
                    semantic_errors=semantic_errors,
                    inferred_types=inferred_types
                )
            
            # All stages successful
            self.logger.info("Compilation successful")
            return CompilationResult(
                success=True,
                program=program,
                inferred_types=inferred_types
            )
        
        except Exception as e:
            self.logger.exception(f"Compilation failed with unexpected error: {str(e)}")
            return CompilationResult(success=False)
    
    def compile_file(self, file_path: str) -> CompilationResult:
        """
        Compile a source file.
        
        Args:
            file_path: The path to the source file
            
        Returns:
            The compilation result
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise CompilerError(f"File not found: {file_path}")
            
            with open(path, 'r') as file:
                source = file.read()
            
            return self.compile_string(source)
        
        except CompilerError as e:
            self.logger.error(str(e))
            return CompilationResult(success=False)
        
        except Exception as e:
            self.logger.exception(f"Error reading file {file_path}: {str(e)}")
            return CompilationResult(success=False) 