#!/usr/bin/env python3
"""
Matlab Toolchain Integration

Complete toolchain for Matlab language support in the Runa Universal Translation Pipeline.
Integrates parsing, AST conversion, and code generation for bidirectional Matlab ↔ Runa translation.
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from pathlib import Path

from .matlab_ast import *
from .matlab_parser import MatlabLexer, MatlabParser, parse_matlab_source
from .matlab_converter import MatlabToRunaConverter, RunaToMatlabConverter
from .matlab_generator import MatlabCodeGenerator, generate_matlab_code
from ....core.runa_ast import *
from ....core.base_components import BaseToolchain
from ....core.translation_result import TranslationResult


class MatlabToolchain(BaseToolchain):
    """Matlab language toolchain for the Runa Universal Translation Pipeline."""
    
    def __init__(self):
        super().__init__("matlab", "4.0")
        self.file_extensions = [".m", ".mlx"]
        self.matlab_to_runa_converter = MatlabToRunaConverter()
        self.runa_to_matlab_converter = RunaToMatlabConverter()
        self.code_generator = MatlabCodeGenerator()
        
    def get_language_info(self) -> Dict[str, Any]:
        """Get information about the Matlab language."""
        return {
            "name": "Matlab",
            "version": "R2024a",
            "tier": 4,
            "description": "Technical computing language for scientific applications",
            "features": [
                "Matrix and array operations",
                "Vectorized computations", 
                "Object-oriented programming",
                "Function handles and anonymous functions",
                "Toolboxes for specialized domains",
                "Live scripts and interactive development",
                "Scientific visualization",
                "Signal processing and control systems",
                "Machine learning and deep learning",
                "Parallel and distributed computing"
            ],
            "paradigms": [
                "procedural",
                "object-oriented", 
                "functional",
                "array-oriented",
                "scientific-computing"
            ],
            "typing": "dynamic",
            "execution": "interpreted",
            "primary_use_cases": [
                "Scientific computing and analysis",
                "Engineering simulations",
                "Data analysis and visualization", 
                "Algorithm development",
                "Control system design",
                "Signal and image processing",
                "Financial modeling",
                "Machine learning research"
            ]
        }
    
    def can_handle_file(self, file_path: str) -> bool:
        """Check if this toolchain can handle the given file."""
        path = Path(file_path)
        return path.suffix.lower() in self.file_extensions
    
    def parse_source(self, source_code: str, file_path: Optional[str] = None) -> TranslationResult:
        """Parse Matlab source code into AST."""
        try:
            # Tokenize and parse
            lexer = MatlabLexer(source_code)
            tokens = lexer.tokenize()
            
            # Filter comments for parsing
            parsing_tokens = [t for t in tokens if t.type not in [MatlabTokenType.COMMENT, MatlabTokenType.BLOCK_COMMENT]]
            
            parser = MatlabParser(parsing_tokens)
            
            # Determine file type and parse accordingly
            if file_path:
                path = Path(file_path)
                if path.suffix == ".mlx":
                    # Live script - would need special handling
                    ast = parser.parse_script()
                elif "classdef" in source_code:
                    # Class file
                    class_decl = parser.parse_statement()
                    ast = MatlabClassFile(class_declaration=class_decl)
                elif source_code.strip().startswith("function"):
                    # Function file
                    func_decl = parser.parse_statement()
                    ast = MatlabFunctionFile(main_function=func_decl)
                else:
                    # Script file
                    ast = parser.parse_script()
            else:
                # Default to script
                ast = parser.parse_script()
            
            return TranslationResult(
                success=True,
                ast=ast,
                source_language="matlab",
                target_language="matlab",
                metadata={
                    "file_path": file_path,
                    "file_type": self._determine_file_type(source_code),
                    "tokens_count": len(tokens),
                    "parsing_tokens_count": len(parsing_tokens)
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                error=f"Matlab parsing failed: {str(e)}",
                source_language="matlab", 
                target_language="matlab"
            )
    
    def _determine_file_type(self, source_code: str) -> str:
        """Determine the type of Matlab file from source code."""
        source_stripped = source_code.strip()
        
        if source_stripped.startswith("classdef"):
            return "class"
        elif source_stripped.startswith("function"):
            return "function"
        elif "%% " in source_code:  # Live script sections
            return "live_script"
        else:
            return "script"
    
    def to_runa_ast(self, matlab_ast: MatlabNode) -> TranslationResult:
        """Convert Matlab AST to Runa AST."""
        try:
            if isinstance(matlab_ast, MatlabScript):
                runa_ast = self.matlab_to_runa_converter.convert_script(matlab_ast)
            elif isinstance(matlab_ast, MatlabFunctionFile):
                # Convert main function to Runa program
                if matlab_ast.main_function:
                    func_node = self.matlab_to_runa_converter.convert_statement(matlab_ast.main_function)
                    runa_ast = ProgramNode(statements=[func_node] if func_node else [])
                else:
                    runa_ast = ProgramNode(statements=[])
            elif isinstance(matlab_ast, MatlabClassFile):
                # Convert class to Runa program
                if matlab_ast.class_declaration:
                    class_node = self.matlab_to_runa_converter.convert_statement(matlab_ast.class_declaration)
                    runa_ast = ProgramNode(statements=[class_node] if class_node else [])
                else:
                    runa_ast = ProgramNode(statements=[])
            elif isinstance(matlab_ast, MatlabProgram):
                # Convert each file and combine
                all_statements = []
                for file_node in matlab_ast.files:
                    file_result = self.to_runa_ast(file_node)
                    if file_result.success and hasattr(file_result.ast, 'statements'):
                        all_statements.extend(file_result.ast.statements)
                runa_ast = ProgramNode(statements=all_statements)
            else:
                # Single statement/expression
                runa_node = self.matlab_to_runa_converter.convert_statement(matlab_ast)
                runa_ast = ProgramNode(statements=[runa_node] if runa_node else [])
            
            return TranslationResult(
                success=True,
                ast=runa_ast,
                source_language="matlab",
                target_language="runa",
                metadata={
                    "conversion_type": "matlab_to_runa",
                    "original_ast_type": type(matlab_ast).__name__
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                error=f"Matlab to Runa conversion failed: {str(e)}",
                source_language="matlab",
                target_language="runa"
            )
    
    def from_runa_ast(self, runa_ast: ASTNode) -> TranslationResult:
        """Convert Runa AST to Matlab AST."""
        try:
            if isinstance(runa_ast, ProgramNode):
                matlab_ast = self.runa_to_matlab_converter.convert_program(runa_ast)
            else:
                # Single node - wrap in script
                matlab_stmt = self.runa_to_matlab_converter.convert_statement(runa_ast)
                matlab_ast = MatlabScript(statements=[matlab_stmt] if matlab_stmt else [])
            
            return TranslationResult(
                success=True,
                ast=matlab_ast,
                source_language="runa",
                target_language="matlab",
                metadata={
                    "conversion_type": "runa_to_matlab",
                    "original_ast_type": type(runa_ast).__name__
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                error=f"Runa to Matlab conversion failed: {str(e)}",
                source_language="runa",
                target_language="matlab"
            )
    
    def generate_code(self, matlab_ast: MatlabNode, format_options: Optional[Dict[str, Any]] = None) -> TranslationResult:
        """Generate Matlab source code from AST."""
        try:
            options = format_options or {}
            indent_size = options.get("indent_size", 4)
            
            generator = MatlabCodeGenerator(indent_size)
            code = generator.generate(matlab_ast)
            
            return TranslationResult(
                success=True,
                code=code,
                source_language="matlab",
                target_language="matlab",
                metadata={
                    "generation_options": options,
                    "code_length": len(code),
                    "line_count": len(code.splitlines())
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                error=f"Matlab code generation failed: {str(e)}",
                source_language="matlab",
                target_language="matlab"
            )
    
    def translate_to_runa(self, source_code: str, file_path: Optional[str] = None) -> TranslationResult:
        """Complete translation from Matlab source to Runa AST."""
        # Parse Matlab source
        parse_result = self.parse_source(source_code, file_path)
        if not parse_result.success:
            return parse_result
        
        # Convert to Runa AST
        return self.to_runa_ast(parse_result.ast)
    
    def translate_from_runa(self, runa_ast: ASTNode, format_options: Optional[Dict[str, Any]] = None) -> TranslationResult:
        """Complete translation from Runa AST to Matlab source."""
        # Convert to Matlab AST
        convert_result = self.from_runa_ast(runa_ast)
        if not convert_result.success:
            return convert_result
        
        # Generate Matlab code
        return self.generate_code(convert_result.ast, format_options)
    
    def validate_ast(self, ast: MatlabNode) -> List[str]:
        """Validate Matlab AST structure."""
        errors = []
        
        try:
            self._validate_node(ast, errors)
        except Exception as e:
            errors.append(f"AST validation error: {str(e)}")
        
        return errors
    
    def _validate_node(self, node: MatlabNode, errors: List[str]) -> None:
        """Recursively validate AST node."""
        if isinstance(node, MatlabFunctionDeclaration):
            if not node.name:
                errors.append("Function declaration missing name")
            
            # Validate parameters
            for param in node.input_parameters + node.output_parameters:
                if not param or not param.isidentifier():
                    errors.append(f"Invalid parameter name: {param}")
            
            # Validate body
            for stmt in node.body:
                self._validate_node(stmt, errors)
                
        elif isinstance(node, MatlabClassDeclaration):
            if not node.name:
                errors.append("Class declaration missing name")
            
            # Validate superclasses
            for superclass in node.superclasses:
                if not superclass or not superclass.isidentifier():
                    errors.append(f"Invalid superclass name: {superclass}")
            
            # Validate properties and methods
            for props_block in node.properties_blocks:
                for prop in props_block.properties:
                    if not prop.name or not prop.name.isidentifier():
                        errors.append(f"Invalid property name: {prop.name}")
            
            for methods_block in node.methods_blocks:
                for method in methods_block.methods:
                    self._validate_node(method, errors)
                    
        elif isinstance(node, MatlabIfStatement):
            if not node.condition:
                errors.append("If statement missing condition")
            
            # Validate bodies
            for stmt in node.then_body + node.else_body:
                self._validate_node(stmt, errors)
            
            for elseif in node.elseif_clauses:
                if not elseif.condition:
                    errors.append("Elseif clause missing condition")
                for stmt in elseif.body:
                    self._validate_node(stmt, errors)
                    
        elif isinstance(node, MatlabForLoop):
            if not node.variable:
                errors.append("For loop missing variable")
            if not node.iterable:
                errors.append("For loop missing iterable")
            
            for stmt in node.body:
                self._validate_node(stmt, errors)
                
        elif isinstance(node, MatlabWhileLoop):
            if not node.condition:
                errors.append("While loop missing condition")
            
            for stmt in node.body:
                self._validate_node(stmt, errors)
                
        elif isinstance(node, MatlabAssignmentExpression):
            if not node.targets:
                errors.append("Assignment missing targets")
            if not node.value:
                errors.append("Assignment missing value")
                
        elif isinstance(node, MatlabBinaryExpression):
            if not node.left or not node.right:
                errors.append("Binary expression missing operands")
            if not node.operator:
                errors.append("Binary expression missing operator")
                
        elif isinstance(node, MatlabFunctionCall):
            if not node.function:
                errors.append("Function call missing function")
                
        # Add more validation as needed
    
    def get_optimization_suggestions(self, matlab_ast: MatlabNode) -> List[str]:
        """Get optimization suggestions for Matlab code."""
        suggestions = []
        
        # Analyze AST for optimization opportunities
        if isinstance(matlab_ast, MatlabScript):
            suggestions.extend(self._analyze_script_optimizations(matlab_ast))
        elif isinstance(matlab_ast, MatlabFunctionDeclaration):
            suggestions.extend(self._analyze_function_optimizations(matlab_ast))
        elif isinstance(matlab_ast, MatlabClassDeclaration):
            suggestions.extend(self._analyze_class_optimizations(matlab_ast))
        
        return suggestions
    
    def _analyze_script_optimizations(self, script: MatlabScript) -> List[str]:
        """Analyze script for optimization opportunities."""
        suggestions = []
        
        # Check for repeated computations
        assignments = [stmt for stmt in script.statements if isinstance(stmt, MatlabAssignmentExpression)]
        if len(assignments) > 10:
            suggestions.append("Consider organizing code into functions for better modularity")
        
        # Check for loop vectorization opportunities
        for stmt in script.statements:
            if isinstance(stmt, MatlabForLoop):
                suggestions.append("Consider vectorizing loops for better performance")
        
        return suggestions
    
    def _analyze_function_optimizations(self, function: MatlabFunctionDeclaration) -> List[str]:
        """Analyze function for optimization opportunities."""
        suggestions = []
        
        # Check function complexity
        if len(function.body) > 50:
            suggestions.append("Consider breaking down large function into smaller functions")
        
        # Check for nested loops
        nested_loops = self._count_nested_loops(function.body)
        if nested_loops > 2:
            suggestions.append("Consider optimizing nested loops with vectorization")
        
        return suggestions
    
    def _analyze_class_optimizations(self, class_decl: MatlabClassDeclaration) -> List[str]:
        """Analyze class for optimization opportunities."""
        suggestions = []
        
        # Check number of methods
        total_methods = sum(len(block.methods) for block in class_decl.methods_blocks)
        if total_methods > 20:
            suggestions.append("Consider using composition or breaking class into smaller classes")
        
        # Check for property access patterns
        total_properties = sum(len(block.properties) for block in class_decl.properties_blocks)
        if total_properties > 15:
            suggestions.append("Consider organizing properties into logical groups")
        
        return suggestions
    
    def _count_nested_loops(self, statements: List[MatlabNode]) -> int:
        """Count maximum nesting level of loops."""
        max_nesting = 0
        
        def count_nesting(stmts: List[MatlabNode], current_level: int = 0) -> int:
            max_level = current_level
            
            for stmt in stmts:
                if isinstance(stmt, (MatlabForLoop, MatlabWhileLoop)):
                    level = count_nesting(stmt.body, current_level + 1)
                    max_level = max(max_level, level)
                elif isinstance(stmt, MatlabIfStatement):
                    level = max(
                        count_nesting(stmt.then_body, current_level),
                        count_nesting(stmt.else_body, current_level)
                    )
                    for elseif in stmt.elseif_clauses:
                        level = max(level, count_nesting(elseif.body, current_level))
                    max_level = max(max_level, level)
            
            return max_level
        
        return count_nesting(statements)
    
    def get_language_specific_features(self) -> Dict[str, Any]:
        """Get Matlab-specific language features."""
        return {
            "matrix_operations": {
                "element_wise": [".*", "./", ".^", ".\\"],
                "matrix_operations": ["*", "/", "^", "\\"],
                "transpose": ["'", ".'"],
                "concatenation": ["[", ";", ","]
            },
            "indexing": {
                "array_indexing": "A(i,j)",
                "cell_indexing": "C{i,j}",
                "logical_indexing": "A(A > 0)",
                "linear_indexing": "A(5)"
            },
            "function_features": {
                "multiple_outputs": "[a, b] = func()",
                "variable_arguments": "varargin, varargout",
                "nested_functions": True,
                "anonymous_functions": "@(x) x^2",
                "function_handles": "@functionName"
            },
            "class_features": {
                "properties": ["Constant", "Dependent", "Access"],
                "methods": ["Static", "Abstract", "Access"],
                "events": True,
                "inheritance": "single and multiple",
                "packages": "+packageName"
            },
            "special_constructs": {
                "try_catch": True,
                "switch_case": True,
                "global_persistent": True,
                "command_syntax": True,
                "live_scripts": True
            }
        }


# Factory function
def create_matlab_toolchain() -> MatlabToolchain:
    """Create and return a Matlab toolchain instance."""
    return MatlabToolchain() 