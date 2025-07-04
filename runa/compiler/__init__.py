"""
Runa Compiler Package

This package provides the complete compilation pipeline for the Runa programming language:
1. Lexical analysis (tokenization) of natural language syntax
2. Syntactic analysis (parsing) into Abstract Syntax Tree (AST)
3. Semantic analysis with type checking and symbol table management
4. Intermediate representation (IR) generation
5. Code generation for target languages (starting with Python)

The compiler follows a traditional multi-pass architecture with clean separation
of concerns between each compilation phase.
"""

# Core compilation components
from .lexer import RunaLexer
from .parser import RunaParser
from .semantic import SemanticAnalyzer, analyze_semantics, SemanticError
from .tokens import TokenType, Token
from .ast_nodes import *

# New IR and code generation components
from .ir import *
from .ast_to_ir import ast_to_ir, ASTToIRVisitor
from .codegen import PythonCodeGenerator
from .codegen.python_generator import generate_python

# High-level compilation API
def compile_runa_to_python(source_code: str) -> str:
    """
    Complete compilation pipeline: Runa source → Python code
    
    Args:
        source_code: Runa source code as string
        
    Returns:
        Generated Python code as string
        
    Raises:
        Various compilation errors if the source is invalid
    """
    # Phase 1: Lexical analysis
    lexer = RunaLexer(source_code)
    tokens = lexer.tokenize()
    
    # Phase 2: Syntactic analysis
    parser = RunaParser(tokens)
    ast = parser.parse()
    
    # Phase 3: Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Phase 4: IR generation
    ir_module = ast_to_ir(ast)
    
    # Phase 5: Python code generation
    python_code = generate_python(ir_module)
    
    return python_code

def parse_runa_source(source_code: str) -> Program:
    """
    Parse Runa source code into AST (original function, preserved for compatibility)
    
    Args:
        source_code: Runa source code as string
        
    Returns:
        Program AST node
    """
    lexer = RunaLexer(source_code)
    tokens = lexer.tokenize()
    parser = RunaParser(tokens)
    return parser.parse()

def compile_runa_to_ir(source_code: str) -> IRModule:
    """
    Compile Runa source to intermediate representation
    
    Args:
        source_code: Runa source code as string
        
    Returns:
        IR module
    """
    ast = parse_runa_source(source_code)
    
    # Run semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate IR
    return ast_to_ir(ast)

# Export key classes and functions
__all__ = [
    # Core compilation
    'RunaLexer', 'RunaParser', 'SemanticAnalyzer', 'analyze_semantics', 'SemanticError',
    'TokenType', 'Token',
    
    # AST nodes (star import from ast_nodes)
    'Program', 'Statement', 'Expression', 'Declaration',
    'LetStatement', 'SetStatement', 'IfStatement', 'DisplayStatement',
    'IntegerLiteral', 'StringLiteral', 'BooleanLiteral', 'Identifier',
    'BinaryExpression', 'FunctionCall',
    
    # IR components
    'IRModule', 'IRFunction', 'IRBasicBlock', 'IRInstruction',
    'IRVariable', 'IRTemporary', 'IRConstant', 'IRTypes',
    'ast_to_ir', 'ASTToIRVisitor',
    
    # Code generation
    'PythonCodeGenerator', 'generate_python',
    
    # High-level API
    'compile_runa_to_python', 'parse_runa_source', 'compile_runa_to_ir'
] 