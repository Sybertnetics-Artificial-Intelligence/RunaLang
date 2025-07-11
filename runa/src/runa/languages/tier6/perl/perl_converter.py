"""
Perl Converter for Runa Universal Translation Platform
Handles bidirectional conversion between Runa AST and Perl AST

This converter supports Perl's powerful text processing capabilities,
flexible syntax, and unique features like:
- Context-sensitive operations (scalar vs list context)
- Regular expressions with advanced pattern matching
- References and complex data structures
- TMTOWTDI (There's More Than One Way To Do It) philosophy
- Special variables and magic handling
- Object-oriented features through blessing
"""

from typing import List, Optional, Dict, Any, Union
import logging
from dataclasses import dataclass, field

from .perl_ast import *
from ...core.ast_base import ASTNode
from ...core.converter_base import BaseConverter, ConversionError
from ...shared.type_system import TypeSystem, Type

logger = logging.getLogger(__name__)

@dataclass
class PerlConversionContext:
    """Context for Perl conversion operations"""
    current_package: Optional[str] = None
    use_statements: List[str] = field(default_factory=list)
    subroutines: Dict[str, PerlSubroutineDeclaration] = field(default_factory=dict)
    variables: Dict[str, PerlVariable] = field(default_factory=dict)
    context_type: str = "void"  # void, scalar, list
    in_regex: bool = False
    regex_flags: str = ""
    text_processing_mode: bool = True
    
class PerlConverter(BaseConverter):
    """Converter between Runa AST and Perl AST"""
    
    def __init__(self):
        super().__init__()
        self.context = PerlConversionContext()
        self.type_system = TypeSystem()
        
        # Perl-specific type mappings
        self.perl_type_map = {
            "String": "scalar",
            "Integer": "scalar", 
            "Float": "scalar",
            "Boolean": "scalar",
            "Array": "array",
            "List": "array",
            "Dictionary": "hash",
            "Hash": "hash",
            "Function": "subroutine",
            "Regex": "regex",
            "FileHandle": "filehandle"
        }
        
        # Perl operators mapping
        self.perl_operators = {
            "+": "+", "-": "-", "*": "*", "/": "/", "%": "%",
            "**": "**", "++": "++", "--": "--",
            "==": "==", "!=": "!=", "<": "<", ">": ">",
            "<=": "<=", ">=": ">=", "<=>": "<=>",
            "eq": "eq", "ne": "ne", "lt": "lt", "gt": "gt",
            "le": "le", "ge": "ge", "cmp": "cmp",
            "&&": "&&", "||": "||", "!": "!",
            "and": "and", "or": "or", "not": "not", "xor": "xor",
            ".": ".", "x": "x", "=~": "=~", "!~": "!~",
            "=": "=", "+=": "+=", "-=": "-=", ".=": ".=",
            ">>": ">>", "<<": "<<", "&": "&", "|": "|", "^": "^"
        }
        
    def runa_to_perl(self, runa_node: ASTNode) -> PerlNode:
        """Convert Runa AST node to Perl AST node"""
        try:
            node_type = getattr(runa_node, 'node_type', type(runa_node).__name__)
            
            conversion_method = f"_convert_{node_type.lower()}_to_perl"
            if hasattr(self, conversion_method):
                return getattr(self, conversion_method)(runa_node)
            else:
                return self._convert_generic_to_perl(runa_node)
                
        except Exception as e:
            logger.error(f"Error converting Runa to Perl: {e}")
            raise ConversionError(f"Failed to convert {type(runa_node).__name__} to Perl: {e}")
    
    def perl_to_runa(self, perl_node: PerlNode) -> ASTNode:
        """Convert Perl AST node to Runa AST node"""
        try:
            node_type = perl_node.node_type.value
            
            conversion_method = f"_convert_{node_type.lower()}_to_runa"
            if hasattr(self, conversion_method):
                return getattr(self, conversion_method)(perl_node)
            else:
                return self._convert_generic_to_runa(perl_node)
                
        except Exception as e:
            logger.error(f"Error converting Perl to Runa: {e}")
            raise ConversionError(f"Failed to convert {perl_node.node_type} to Runa: {e}")
    
    # Runa to Perl conversions
    
    def _convert_program_to_perl(self, runa_node) -> PerlProgram:
        """Convert Runa program to Perl program"""
        statements = []
        packages = []
        use_statements = []
        
        # Add common use statements for text processing
        if self.context.text_processing_mode:
            use_statements.append(PerlUseStatement(module_name="strict"))
            use_statements.append(PerlUseStatement(module_name="warnings"))
            use_statements.append(PerlUseStatement(module_name="utf8"))
        
        for stmt in getattr(runa_node, 'statements', []):
            perl_stmt = self.runa_to_perl(stmt)
            if isinstance(perl_stmt, PerlPackage):
                packages.append(perl_stmt)
            elif isinstance(perl_stmt, PerlUseStatement):
                use_statements.append(perl_stmt)
            else:
                statements.append(perl_stmt)
        
        return PerlProgram(
            statements=statements,
            packages=packages,
            use_statements=use_statements,
            shebang="#!/usr/bin/perl"
        )
    
    def _convert_variable_declaration_to_perl(self, runa_node) -> PerlVariable:
        """Convert Runa variable declaration to Perl variable"""
        var_name = getattr(runa_node, 'name', 'var')
        var_type = getattr(runa_node, 'type', 'scalar')
        
        # Determine Perl variable type based on Runa type
        if var_type in ['Array', 'List']:
            return PerlArrayVariable(name=var_name, package=self.context.current_package)
        elif var_type in ['Dictionary', 'Hash']:
            return PerlHashVariable(name=var_name, package=self.context.current_package)
        else:
            return PerlScalarVariable(name=var_name, package=self.context.current_package)
    
    def _convert_function_declaration_to_perl(self, runa_node) -> PerlSubroutineDeclaration:
        """Convert Runa function to Perl subroutine"""
        name = getattr(runa_node, 'name', 'func')
        params = [param.name for param in getattr(runa_node, 'parameters', [])]
        body = [self.runa_to_perl(stmt) for stmt in getattr(runa_node, 'body', [])]
        
        return PerlSubroutineDeclaration(
            name=name,
            parameters=params,
            body=body
        )
    
    def _convert_if_statement_to_perl(self, runa_node) -> PerlIfStatement:
        """Convert Runa if statement to Perl if statement"""
        condition = self.runa_to_perl(getattr(runa_node, 'condition'))
        then_block = [self.runa_to_perl(stmt) for stmt in getattr(runa_node, 'then_block', [])]
        else_block = [self.runa_to_perl(stmt) for stmt in getattr(runa_node, 'else_block', [])]
        
        return PerlIfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def _convert_while_loop_to_perl(self, runa_node) -> PerlWhileLoop:
        """Convert Runa while loop to Perl while loop"""
        condition = self.runa_to_perl(getattr(runa_node, 'condition'))
        body = [self.runa_to_perl(stmt) for stmt in getattr(runa_node, 'body', [])]
        
        return PerlWhileLoop(condition=condition, body=body)
    
    def _convert_for_loop_to_perl(self, runa_node) -> Union[PerlForLoop, PerlForeachLoop]:
        """Convert Runa for loop to Perl for/foreach loop"""
        # Check if it's a foreach-style loop
        if hasattr(runa_node, 'iterable'):
            variable = None
            if hasattr(runa_node, 'variable'):
                variable = self.runa_to_perl(runa_node.variable)
            
            iterable = self.runa_to_perl(runa_node.iterable)
            body = [self.runa_to_perl(stmt) for stmt in getattr(runa_node, 'body', [])]
            
            return PerlForeachLoop(
                variable=variable,
                iterable=iterable,
                body=body
            )
        else:
            # C-style for loop
            init = self.runa_to_perl(getattr(runa_node, 'initialization', None)) if hasattr(runa_node, 'initialization') else None
            condition = self.runa_to_perl(getattr(runa_node, 'condition', None)) if hasattr(runa_node, 'condition') else None
            increment = self.runa_to_perl(getattr(runa_node, 'increment', None)) if hasattr(runa_node, 'increment') else None
            body = [self.runa_to_perl(stmt) for stmt in getattr(runa_node, 'body', [])]
            
            return PerlForLoop(
                initialization=init,
                condition=condition,
                increment=increment,
                body=body
            )
    
    def _convert_assignment_to_perl(self, runa_node) -> PerlAssignment:
        """Convert Runa assignment to Perl assignment"""
        left = self.runa_to_perl(getattr(runa_node, 'left'))
        right = self.runa_to_perl(getattr(runa_node, 'right'))
        operator = getattr(runa_node, 'operator', '=')
        
        # Map Runa operators to Perl operators
        perl_operator = self.perl_operators.get(operator, operator)
        
        return PerlAssignment(left=left, right=right, operator=perl_operator)
    
    def _convert_binary_operation_to_perl(self, runa_node) -> PerlBinaryOperation:
        """Convert Runa binary operation to Perl binary operation"""
        left = self.runa_to_perl(getattr(runa_node, 'left'))
        right = self.runa_to_perl(getattr(runa_node, 'right'))
        operator = getattr(runa_node, 'operator', '+')
        
        # Handle string operations specially in Perl
        perl_operator = self.perl_operators.get(operator, operator)
        
        return PerlBinaryOperation(left=left, right=right, operator=perl_operator)
    
    def _convert_string_literal_to_perl(self, runa_node) -> PerlStringLiteral:
        """Convert Runa string literal to Perl string literal"""
        value = getattr(runa_node, 'value', '')
        
        # Check if string contains variable interpolation patterns
        if '$' in value or '@' in value:
            return PerlStringLiteral(value=value, quote_type="double")
        else:
            return PerlStringLiteral(value=value, quote_type="single")
    
    def _convert_regex_literal_to_perl(self, runa_node) -> PerlRegexLiteral:
        """Convert Runa regex to Perl regex literal"""
        pattern = getattr(runa_node, 'pattern', '')
        flags = getattr(runa_node, 'flags', '')
        
        return PerlRegexLiteral(pattern=pattern, flags=flags)
    
    def _convert_array_literal_to_perl(self, runa_node) -> PerlArrayLiteral:
        """Convert Runa array literal to Perl array literal"""
        elements = [self.runa_to_perl(elem) for elem in getattr(runa_node, 'elements', [])]
        return PerlArrayLiteral(elements=elements)
    
    def _convert_dictionary_literal_to_perl(self, runa_node) -> PerlHashLiteral:
        """Convert Runa dictionary to Perl hash literal"""
        pairs = []
        items = getattr(runa_node, 'items', [])
        
        for item in items:
            key = self.runa_to_perl(getattr(item, 'key'))
            value = self.runa_to_perl(getattr(item, 'value'))
            pairs.append(PerlHashPair(key=key, value=value))
        
        return PerlHashLiteral(pairs=pairs)
    
    # Perl to Runa conversions
    
    def _convert_program_to_runa(self, perl_node: PerlProgram):
        """Convert Perl program to Runa program"""
        from ...core.ast_base import Program
        
        statements = []
        for stmt in perl_node.statements:
            runa_stmt = self.perl_to_runa(stmt)
            statements.append(runa_stmt)
        
        return Program(statements=statements)
    
    def _convert_scalar_variable_to_runa(self, perl_node: PerlScalarVariable):
        """Convert Perl scalar variable to Runa variable"""
        from ...core.ast_base import VariableReference
        return VariableReference(name=perl_node.name)
    
    def _convert_array_variable_to_runa(self, perl_node: PerlArrayVariable):
        """Convert Perl array variable to Runa array variable"""
        from ...core.ast_base import VariableReference
        return VariableReference(name=perl_node.name)
    
    def _convert_hash_variable_to_runa(self, perl_node: PerlHashVariable):
        """Convert Perl hash variable to Runa dictionary variable"""
        from ...core.ast_base import VariableReference
        return VariableReference(name=perl_node.name)
    
    def _convert_subroutine_declaration_to_runa(self, perl_node: PerlSubroutineDeclaration):
        """Convert Perl subroutine to Runa function"""
        from ...core.ast_base import FunctionDeclaration, Parameter
        
        parameters = [Parameter(name=param) for param in perl_node.parameters]
        body = [self.perl_to_runa(stmt) for stmt in perl_node.body]
        
        return FunctionDeclaration(
            name=perl_node.name,
            parameters=parameters,
            body=body
        )
    
    def _convert_if_statement_to_runa(self, perl_node: PerlIfStatement):
        """Convert Perl if statement to Runa if statement"""
        from ...core.ast_base import IfStatement
        
        condition = self.perl_to_runa(perl_node.condition)
        then_block = [self.perl_to_runa(stmt) for stmt in perl_node.then_block]
        else_block = [self.perl_to_runa(stmt) for stmt in perl_node.else_block]
        
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def _convert_while_loop_to_runa(self, perl_node: PerlWhileLoop):
        """Convert Perl while loop to Runa while loop"""
        from ...core.ast_base import WhileLoop
        
        condition = self.perl_to_runa(perl_node.condition)
        body = [self.perl_to_runa(stmt) for stmt in perl_node.body]
        
        return WhileLoop(condition=condition, body=body)
    
    def _convert_foreach_loop_to_runa(self, perl_node: PerlForeachLoop):
        """Convert Perl foreach loop to Runa for loop"""
        from ...core.ast_base import ForLoop
        
        variable = self.perl_to_runa(perl_node.variable) if perl_node.variable else None
        iterable = self.perl_to_runa(perl_node.iterable)
        body = [self.perl_to_runa(stmt) for stmt in perl_node.body]
        
        return ForLoop(
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def _convert_assignment_to_runa(self, perl_node: PerlAssignment):
        """Convert Perl assignment to Runa assignment"""
        from ...core.ast_base import Assignment
        
        left = self.perl_to_runa(perl_node.left)
        right = self.perl_to_runa(perl_node.right)
        
        return Assignment(left=left, right=right, operator=perl_node.operator)
    
    def _convert_binary_operation_to_runa(self, perl_node: PerlBinaryOperation):
        """Convert Perl binary operation to Runa binary operation"""
        from ...core.ast_base import BinaryOperation
        
        left = self.perl_to_runa(perl_node.left)
        right = self.perl_to_runa(perl_node.right)
        
        return BinaryOperation(left=left, right=right, operator=perl_node.operator)
    
    def _convert_string_literal_to_runa(self, perl_node: PerlStringLiteral):
        """Convert Perl string literal to Runa string literal"""
        from ...core.ast_base import StringLiteral
        return StringLiteral(value=perl_node.value)
    
    def _convert_numeric_literal_to_runa(self, perl_node: PerlNumericLiteral):
        """Convert Perl numeric literal to Runa numeric literal"""
        from ...core.ast_base import NumericLiteral
        return NumericLiteral(value=perl_node.value)
    
    def _convert_regex_literal_to_runa(self, perl_node: PerlRegexLiteral):
        """Convert Perl regex literal to Runa regex literal"""
        from ...core.ast_base import RegexLiteral
        return RegexLiteral(pattern=perl_node.pattern, flags=perl_node.flags)
    
    def _convert_array_literal_to_runa(self, perl_node: PerlArrayLiteral):
        """Convert Perl array literal to Runa array literal"""
        from ...core.ast_base import ArrayLiteral
        
        elements = [self.perl_to_runa(elem) for elem in perl_node.elements]
        return ArrayLiteral(elements=elements)
    
    def _convert_hash_literal_to_runa(self, perl_node: PerlHashLiteral):
        """Convert Perl hash literal to Runa dictionary literal"""
        from ...core.ast_base import DictionaryLiteral, KeyValuePair
        
        items = []
        for pair in perl_node.pairs:
            key = self.perl_to_runa(pair.key)
            value = self.perl_to_runa(pair.value)
            items.append(KeyValuePair(key=key, value=value))
        
        return DictionaryLiteral(items=items)
    
    # Text processing specific conversions
    
    def _convert_regex_match_to_runa(self, perl_node: PerlRegexMatch):
        """Convert Perl regex match to Runa match operation"""
        from ...core.ast_base import FunctionCall
        
        string = self.perl_to_runa(perl_node.string)
        pattern = self.perl_to_runa(perl_node.pattern)
        
        # Convert to Runa function call for regex matching
        return FunctionCall(
            name="match_regex",
            arguments=[string, pattern]
        )
    
    def _convert_regex_substitution_to_runa(self, perl_node: PerlRegexSubstitution):
        """Convert Perl regex substitution to Runa function call"""
        from ...core.ast_base import FunctionCall, StringLiteral
        
        string = self.perl_to_runa(perl_node.string)
        pattern = StringLiteral(value=perl_node.pattern)
        replacement = StringLiteral(value=perl_node.replacement)
        
        return FunctionCall(
            name="substitute_regex",
            arguments=[string, pattern, replacement]
        )
    
    def _convert_print_statement_to_runa(self, perl_node: PerlPrintStatement):
        """Convert Perl print to Runa print function call"""
        from ...core.ast_base import FunctionCall
        
        arguments = [self.perl_to_runa(arg) for arg in perl_node.arguments]
        
        return FunctionCall(name="print", arguments=arguments)
    
    # Generic conversion fallbacks
    
    def _convert_generic_to_perl(self, runa_node) -> PerlNode:
        """Generic conversion from Runa to Perl"""
        # Create a basic Perl identifier for unknown nodes
        node_name = type(runa_node).__name__.lower()
        return PerlIdentifier(name=node_name)
    
    def _convert_generic_to_runa(self, perl_node: PerlNode):
        """Generic conversion from Perl to Runa"""
        from ...core.ast_base import Identifier
        # Create a basic Runa identifier for unknown nodes
        return Identifier(name=str(perl_node.node_type.value))
    
    # Utility methods
    
    def set_context(self, context_type: str):
        """Set the conversion context (void, scalar, list)"""
        self.context.context_type = context_type
    
    def enable_text_processing_mode(self):
        """Enable enhanced text processing features"""
        self.context.text_processing_mode = True
    
    def add_use_statement(self, module: str):
        """Add a use statement to the conversion context"""
        self.context.use_statements.append(module)
    
    def get_perl_type(self, runa_type: str) -> str:
        """Get Perl type for Runa type"""
        return self.perl_type_map.get(runa_type, "scalar") 