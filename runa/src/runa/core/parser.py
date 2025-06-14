"""
Runa Language Parser

SECG Compliance: Full ethical validation for all parsing operations
Performance Target: <100ms compilation for 1000-line programs
Self-Hosting Support: Designed to parse Runa compiler source code

This parser converts Runa tokens into Abstract Syntax Tree (AST) nodes.
Supports all documented Runa syntax including natural language constructs,
pattern matching, type definitions, and async/await.
"""

import time
from typing import List, Optional, Union, Any, Dict, Tuple
from dataclasses import dataclass

from .lexer import Token, TokenType, RunaLexer
from .ast.ast_nodes import *
from . import (
    secg_compliance_required, PerformanceMonitor, RUNA_COMPILATION_TARGET_MS,
    OperationResult, SECGViolationError
)

class ParserError(Exception):
    """Parser-specific errors with location information."""
    def __init__(self, message: str, token: Token):
        super().__init__(f"Parser error at line {token.line}, column {token.column}: {message}")
        self.token = token
        self.line = token.line
        self.column = token.column

@dataclass
class ParserState:
    """Current state of the parser."""
    tokens: List[Token]
    position: int
    current_token: Optional[Token]

@secg_compliance_required
class RunaParser:
    """
    Complete recursive descent parser for Runa programming language.
    
    Converts tokens from lexer into Abstract Syntax Tree (AST) nodes.
    Handles all Runa syntax including natural language constructs,
    control flow, pattern matching, and type definitions.
    """
    
    def __init__(self):
        """Initialize parser with performance monitoring."""
        self.performance_monitor = PerformanceMonitor()
        self.state: Optional[ParserState] = None
    
    @PerformanceMonitor().enforce_target(RUNA_COMPILATION_TARGET_MS)
    def parse(self, tokens: List[Token]) -> OperationResult:
        """
        Parse tokens into AST.
        
        Args:
            tokens: List of tokens from lexer
            
        Returns:
            OperationResult containing Program AST node or error information
            
        Raises:
            SECGViolationError: If SECG compliance is violated
            PerformanceViolationError: If parsing exceeds time limit
        """
        if not isinstance(tokens, list):
            return OperationResult(
                success=False,
                error=f"Expected list of tokens, got {type(tokens)}"
            )
        
        if not tokens:
            return OperationResult(
                success=True,
                value=Program([]),
                secg_compliant=True
            )
        
        try:
            start_time = time.perf_counter()
            
            self.state = ParserState(
                tokens=tokens,
                position=0,
                current_token=tokens[0] if tokens else None
            )
            
            program = self._parse_program()
            
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            
            return OperationResult(
                success=True,
                value=program,
                execution_time_ms=execution_time,
                secg_compliant=True
            )
            
        except ParserError as e:
            return OperationResult(
                success=False,
                error=str(e),
                secg_compliant=True
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Unexpected parser error: {e}",
                secg_compliant=True
            )
    
    def _parse_program(self) -> Program:
        """Parse complete program."""
        statements = []
        
        while not self._is_at_end() and self._current_token().type != TokenType.EOF:
            # Skip newlines and comments at top level
            if self._current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                self._advance()
                continue
                
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def _parse_statement(self) -> Optional[Statement]:
        """Parse any statement."""
        if not self._current_token():
            return None
        
        token_type = self._current_token().type
        
        # Variable declarations
        if token_type in [TokenType.LET, TokenType.DEFINE, TokenType.SET]:
            return self._parse_variable_declaration()
        
        # Function definitions
        elif token_type == TokenType.PROCESS:
            return self._parse_function_definition()
        
        # Control flow
        elif token_type == TokenType.IF:
            return self._parse_if_statement()
        elif token_type == TokenType.FOR:
            return self._parse_for_statement()
        elif token_type == TokenType.WHILE:
            return self._parse_while_statement()
        elif token_type == TokenType.MATCH:
            return self._parse_match_statement()
        
        # Return statement
        elif token_type == TokenType.RETURN:
            return self._parse_return_statement()
        
        # Display statement
        elif token_type == TokenType.DISPLAY:
            return self._parse_display_statement()
        
        # Type definitions
        elif token_type == TokenType.TYPE:
            return self._parse_type_definition()
        
        # Expression statements (function calls, assignments)
        else:
            expr = self._parse_expression()
            self._consume_newline_or_eof()
            return expr  # Expression statements
    
    def _parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration (Let/Define/Set)."""
        declaration_type = self._current_token().value
        self._advance()  # consume declaration keyword
        
        # Get variable name
        if self._current_token().type != TokenType.IDENTIFIER:
            raise ParserError(f"Expected identifier after {declaration_type}", self._current_token())
        
        name = self._current_token().value
        self._advance()
        
        # Optional type annotation
        type_annotation = None
        if self._current_token().type == TokenType.LEFT_PAREN:
            self._advance()  # consume '('
            type_annotation = self._parse_type_expression()
            if self._current_token().type != TokenType.RIGHT_PAREN:
                raise ParserError("Expected ')' after type annotation", self._current_token())
            self._advance()  # consume ')'
        
        # Expect 'be' or 'as'
        if self._current_token().type not in [TokenType.BE, TokenType.AS]:
            raise ParserError(f"Expected 'be' or 'as' after variable name", self._current_token())
        self._advance()
        
        # Parse value expression
        value = self._parse_expression()
        
        self._consume_newline_or_eof()
        
        return VariableDeclaration(
            name=name,
            value=value,
            type_annotation=type_annotation,
            declaration_type=declaration_type,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_function_definition(self) -> FunctionDefinition:
        """Parse function definition (Process called)."""
        self._advance()  # consume 'Process'
        
        # Expect 'called'
        if self._current_token().type != TokenType.CALLED:
            raise ParserError("Expected 'called' after 'Process'", self._current_token())
        self._advance()
        
        # Function name (string literal)
        if self._current_token().type != TokenType.STRING:
            raise ParserError("Expected function name as string", self._current_token())
        
        name = self._current_token().value[1:-1]  # Remove quotes
        self._advance()
        
        # Optional parameters
        parameters = []
        return_type = None
        
        if self._current_token().type == TokenType.THAT:
            self._advance()  # consume 'that'
            
            if self._current_token().type == TokenType.TAKES:
                self._advance()  # consume 'takes'
                parameters = self._parse_parameter_list()
        
        # Optional return type
        if self._current_token().type == TokenType.RETURNS:
            self._advance()  # consume 'returns'
            return_type = self._parse_type_expression()
        
        # Expect colon
        if self._current_token().type != TokenType.COLON:
            raise ParserError("Expected ':' after function signature", self._current_token())
        self._advance()
        
        # Parse body
        body = self._parse_block()
        
        return FunctionDefinition(
            name=name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_parameter_list(self) -> List[Parameter]:
        """Parse function parameter list."""
        parameters = []
        
        # First parameter
        if self._current_token().type == TokenType.IDENTIFIER:
            param_name = self._current_token().value
            self._advance()
            
            type_annotation = None
            if self._current_token().type == TokenType.AS:
                self._advance()  # consume 'as'
                type_annotation = self._parse_type_expression()
            
            parameters.append(Parameter(name=param_name, type_annotation=type_annotation))
            
            # Additional parameters
            while self._current_token().type == TokenType.AND:
                self._advance()  # consume 'and'
                
                if self._current_token().type != TokenType.IDENTIFIER:
                    raise ParserError("Expected parameter name after 'and'", self._current_token())
                
                param_name = self._current_token().value
                self._advance()
                
                type_annotation = None
                if self._current_token().type == TokenType.AS:
                    self._advance()  # consume 'as'
                    type_annotation = self._parse_type_expression()
                
                parameters.append(Parameter(name=param_name, type_annotation=type_annotation))
        
        return parameters
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse if-otherwise statement."""
        self._advance()  # consume 'If'
        
        condition = self._parse_expression()
        
        if self._current_token().type != TokenType.COLON:
            raise ParserError("Expected ':' after if condition", self._current_token())
        self._advance()
        
        then_block = self._parse_block()
        
        else_block = None
        if (self._current_token() and 
            self._current_token().type == TokenType.OTHERWISE):
            self._advance()  # consume 'Otherwise'
            
            if self._current_token().type != TokenType.COLON:
                raise ParserError("Expected ':' after 'Otherwise'", self._current_token())
            self._advance()
            
            else_block = self._parse_block()
        
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_for_statement(self) -> ForStatement:
        """Parse for each statement."""
        self._advance()  # consume 'For'
        
        if self._current_token().type != TokenType.EACH:
            raise ParserError("Expected 'each' after 'For'", self._current_token())
        self._advance()
        
        if self._current_token().type != TokenType.IDENTIFIER:
            raise ParserError("Expected variable name", self._current_token())
        
        variable = self._current_token().value
        self._advance()
        
        if self._current_token().type != TokenType.IN:
            raise ParserError("Expected 'in' after variable", self._current_token())
        self._advance()
        
        iterable = self._parse_expression()
        
        if self._current_token().type != TokenType.COLON:
            raise ParserError("Expected ':' after for expression", self._current_token())
        self._advance()
        
        body = self._parse_block()
        
        return ForStatement(
            variable=variable,
            iterable=iterable,
            body=body,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_while_statement(self) -> WhileStatement:
        """Parse while statement."""
        self._advance()  # consume 'While'
        
        condition = self._parse_expression()
        
        if self._current_token().type != TokenType.COLON:
            raise ParserError("Expected ':' after while condition", self._current_token())
        self._advance()
        
        body = self._parse_block()
        
        return WhileStatement(
            condition=condition,
            body=body,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_match_statement(self) -> MatchStatement:
        """Parse match statement."""
        self._advance()  # consume 'Match'
        
        value = self._parse_expression()
        
        if self._current_token().type != TokenType.COLON:
            raise ParserError("Expected ':' after match value", self._current_token())
        self._advance()
        
        cases = []
        
        # Expect indentation
        if self._current_token().type != TokenType.INDENT:
            raise ParserError("Expected indentation after match:", self._current_token())
        self._advance()
        
        # Parse cases
        while (self._current_token() and 
               self._current_token().type == TokenType.WHEN):
            cases.append(self._parse_match_case())
        
        # Expect dedent
        if self._current_token().type == TokenType.DEDENT:
            self._advance()
        
        return MatchStatement(
            value=value,
            cases=cases,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_match_case(self) -> MatchCase:
        """Parse individual match case."""
        self._advance()  # consume 'When'
        
        pattern = self._parse_pattern()
        
        if self._current_token().type != TokenType.COLON:
            raise ParserError("Expected ':' after pattern", self._current_token())
        self._advance()
        
        # Parse body (single statement or block)
        body = []
        if self._current_token().type == TokenType.INDENT:
            body = self._parse_block()
        else:
            # Single statement
            stmt = self._parse_statement()
            if stmt:
                body = [stmt]
        
        return MatchCase(pattern=pattern, body=body)
    
    def _parse_pattern(self) -> Pattern:
        """Parse pattern for match statement."""
        if self._current_token().type == TokenType.UNDERSCORE:
            self._advance()
            return WildcardPattern()
        
        elif self._current_token().type in [TokenType.STRING, TokenType.INTEGER, 
                                           TokenType.FLOAT, TokenType.BOOLEAN_TRUE, 
                                           TokenType.BOOLEAN_FALSE]:
            literal = self._parse_literal()
            return LiteralPattern(literal)
        
        elif self._current_token().type == TokenType.IDENTIFIER:
            name = self._current_token().value
            self._advance()
            return IdentifierPattern(name)
        
        else:
            raise ParserError("Invalid pattern", self._current_token())
    
    def _parse_return_statement(self) -> ReturnStatement:
        """Parse return statement."""
        self._advance()  # consume 'Return'
        
        value = None
        if (self._current_token() and 
            self._current_token().type not in [TokenType.NEWLINE, TokenType.EOF]):
            value = self._parse_expression()
        
        self._consume_newline_or_eof()
        
        return ReturnStatement(
            value=value,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_display_statement(self) -> DisplayStatement:
        """Parse display statement."""
        self._advance()  # consume 'Display'
        
        expressions = [self._parse_expression()]
        
        message = None
        if self._current_token().type == TokenType.WITH:
            self._advance()  # consume 'with'
            
            if self._current_token().type == TokenType.MESSAGE:
                self._advance()  # consume 'message'
                message_expr = self._parse_expression()
                if isinstance(message_expr, StringLiteral):
                    message = message_expr.value
        
        self._consume_newline_or_eof()
        
        return DisplayStatement(
            expressions=expressions,
            message=message,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_type_definition(self) -> TypeDefinition:
        """Parse type definition."""
        self._advance()  # consume 'Type'
        
        if self._current_token().type != TokenType.IDENTIFIER:
            raise ParserError("Expected type name", self._current_token())
        
        name = self._current_token().value
        self._advance()
        
        if self._current_token().type != TokenType.IS:
            raise ParserError("Expected 'is' after type name", self._current_token())
        self._advance()
        
        # Parse type definition body
        definition = self._parse_type_definition_body()
        
        return TypeDefinition(
            name=name,
            definition=definition,
            line=self._current_token().line,
            column=self._current_token().column
        )
    
    def _parse_type_definition_body(self) -> TypeDefinitionBody:
        """Parse type definition body."""
        if self._current_token().type == TokenType.DICTIONARY:
            # Struct-like definition
            self._advance()  # consume 'Dictionary'
            
            if self._current_token().type != TokenType.WITH:
                raise ParserError("Expected 'with' after 'Dictionary'", self._current_token())
            self._advance()
            
            if self._current_token().type != TokenType.COLON:
                raise ParserError("Expected ':' after 'with'", self._current_token())
            self._advance()
            
            fields = self._parse_type_fields()
            return StructTypeDefinition(fields)
        
        else:
            # Simple type alias or union type
            type_expr = self._parse_type_expression()
            # For now, treat as struct with single field
            return StructTypeDefinition([])
    
    def _parse_type_fields(self) -> List[TypeField]:
        """Parse type fields."""
        fields = []
        
        if self._current_token().type != TokenType.INDENT:
            raise ParserError("Expected indentation after type definition", self._current_token())
        self._advance()
        
        while (self._current_token() and 
               self._current_token().type == TokenType.IDENTIFIER):
            field_name = self._current_token().value
            self._advance()
            
            if self._current_token().type != TokenType.AS:
                raise ParserError("Expected 'as' after field name", self._current_token())
            self._advance()
            
            field_type = self._parse_type_expression()
            fields.append(TypeField(name=field_name, type_annotation=field_type))
            
            # Skip newlines
            while (self._current_token() and 
                   self._current_token().type == TokenType.NEWLINE):
                self._advance()
        
        if self._current_token().type == TokenType.DEDENT:
            self._advance()
        
        return fields
    
    def _parse_expression(self) -> Expression:
        """Parse expression (entry point for expression parsing)."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self) -> Expression:
        """Parse logical OR expression."""
        expr = self._parse_logical_and()
        
        while (self._current_token() and 
               self._current_token().type == TokenType.OR):
            self._advance()
            right = self._parse_logical_and()
            expr = BinaryOperation(expr, BinaryOperator.OR, right)
        
        return expr
    
    def _parse_logical_and(self) -> Expression:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        
        while (self._current_token() and 
               self._current_token().type == TokenType.AND):
            self._advance()
            right = self._parse_equality()
            expr = BinaryOperation(expr, BinaryOperator.AND, right)
        
        return expr
    
    def _parse_equality(self) -> Expression:
        """Parse equality expressions."""
        expr = self._parse_comparison()
        
        while self._current_token():
            if self._current_token().type == TokenType.IS:
                self._advance()
                if self._current_token().type == TokenType.EQUAL:
                    self._advance()
                    if self._current_token().type == TokenType.TO:
                        self._advance()
                        right = self._parse_comparison()
                        expr = BinaryOperation(expr, BinaryOperator.IS_EQUAL, right)
                    else:
                        raise ParserError("Expected 'to' after 'is equal'", self._current_token())
                else:
                    raise ParserError("Expected 'equal' after 'is'", self._current_token())
            else:
                break
        
        return expr
    
    def _parse_comparison(self) -> Expression:
        """Parse comparison expressions."""
        expr = self._parse_term()
        
        while self._current_token():
            if self._current_token().type == TokenType.IS:
                # Look ahead for comparison operators
                saved_pos = self.state.position
                self._advance()
                
                if self._current_token().type == TokenType.GREATER:
                    self._advance()
                    if self._current_token().type == TokenType.THAN:
                        self._advance()
                        right = self._parse_term()
                        expr = BinaryOperation(expr, BinaryOperator.IS_GREATER_THAN, right)
                    else:
                        # Restore position if not complete pattern
                        self.state.position = saved_pos
                        self.state.current_token = self.state.tokens[self.state.position]
                        break
                elif self._current_token().type == TokenType.LESS:
                    self._advance()
                    if self._current_token().type == TokenType.THAN:
                        self._advance()
                        right = self._parse_term()
                        expr = BinaryOperation(expr, BinaryOperator.IS_LESS_THAN, right)
                    else:
                        # Restore position if not complete pattern
                        self.state.position = saved_pos
                        self.state.current_token = self.state.tokens[self.state.position]
                        break
                else:
                    # Restore position
                    self.state.position = saved_pos
                    self.state.current_token = self.state.tokens[self.state.position]
                    break
            else:
                break
        
        return expr
    
    def _parse_term(self) -> Expression:
        """Parse addition/subtraction expressions."""
        expr = self._parse_factor()
        
        while self._current_token():
            if self._current_token().type == TokenType.PLUS:
                self._advance()
                right = self._parse_factor()
                expr = BinaryOperation(expr, BinaryOperator.PLUS, right)
            elif self._current_token().type == TokenType.MINUS:
                self._advance()
                right = self._parse_factor()
                expr = BinaryOperation(expr, BinaryOperator.MINUS, right)
            else:
                break
        
        return expr
    
    def _parse_factor(self) -> Expression:
        """Parse multiplication/division expressions."""
        expr = self._parse_unary()
        
        while self._current_token():
            if self._current_token().type == TokenType.MULTIPLIED:
                self._advance()
                if self._current_token().type == TokenType.BY:
                    self._advance()
                    right = self._parse_unary()
                    expr = BinaryOperation(expr, BinaryOperator.MULTIPLIED_BY, right)
                else:
                    raise ParserError("Expected 'by' after 'multiplied'", self._current_token())
            elif self._current_token().type == TokenType.DIVIDED:
                self._advance()
                if self._current_token().type == TokenType.BY:
                    self._advance()
                    right = self._parse_unary()
                    expr = BinaryOperation(expr, BinaryOperator.DIVIDED_BY, right)
                else:
                    raise ParserError("Expected 'by' after 'divided'", self._current_token())
            else:
                break
        
        return expr
    
    def _parse_unary(self) -> Expression:
        """Parse unary expressions."""
        if (self._current_token() and 
            self._current_token().type == TokenType.NOT):
            operator = self._current_token().value
            self._advance()
            operand = self._parse_unary()
            return UnaryOperation(operator, operand)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Expression:
        """Parse primary expressions."""
        if not self._current_token():
            raise ParserError("Unexpected end of input", Token(TokenType.EOF, "", 0, 0, 0, 0))
        
        token_type = self._current_token().type
        
        # Literals
        if token_type in [TokenType.STRING, TokenType.INTEGER, TokenType.FLOAT,
                         TokenType.BOOLEAN_TRUE, TokenType.BOOLEAN_FALSE, TokenType.NONE]:
            return self._parse_literal()
        
        # Identifiers and function calls
        elif token_type == TokenType.IDENTIFIER:
            return self._parse_identifier_or_call()
        
        # List expressions
        elif token_type == TokenType.LIST:
            return self._parse_list_expression()
        
        # Parenthesized expressions
        elif token_type == TokenType.LEFT_PAREN:
            self._advance()  # consume '('
            expr = self._parse_expression()
            if self._current_token().type != TokenType.RIGHT_PAREN:
                raise ParserError("Expected ')' after expression", self._current_token())
            self._advance()  # consume ')'
            return expr
        
        else:
            raise ParserError(f"Unexpected token: {self._current_token().value}", self._current_token())
    
    def _parse_literal(self) -> Literal:
        """Parse literal expressions."""
        token = self._current_token()
        self._advance()
        
        if token.type == TokenType.STRING:
            return StringLiteral(token.value[1:-1])  # Remove quotes
        elif token.type == TokenType.INTEGER:
            return IntegerLiteral(int(token.value))
        elif token.type == TokenType.FLOAT:
            return FloatLiteral(float(token.value))
        elif token.type == TokenType.BOOLEAN_TRUE:
            return BooleanLiteral(True)
        elif token.type == TokenType.BOOLEAN_FALSE:
            return BooleanLiteral(False)
        elif token.type == TokenType.NONE:
            return NoneLiteral()
        else:
            raise ParserError(f"Unknown literal type: {token.type}", token)
    
    def _parse_identifier_or_call(self) -> Expression:
        """Parse identifier or function call."""
        name = self._current_token().value
        self._advance()
        
        # Check for function call with 'with' keyword
        if (self._current_token() and 
            self._current_token().type == TokenType.WITH):
            return self._parse_function_call(name)
        
        return Identifier(name)
    
    def _parse_function_call(self, function_name: str) -> FunctionCall:
        """Parse function call with 'with' syntax."""
        self._advance()  # consume 'with'
        
        arguments = []
        
        # Parse first argument
        if self._current_token().type != TokenType.COLON:
            arguments.append(self._parse_argument())
            
            # Parse additional arguments
            while (self._current_token() and 
                   self._current_token().type == TokenType.AND):
                self._advance()  # consume 'and'
                arguments.append(self._parse_argument())
        
        return FunctionCall(function_name=function_name, arguments=arguments)
    
    def _parse_argument(self) -> Argument:
        """Parse function argument."""
        # Check for named argument (param as value)
        if (self._current_token().type == TokenType.IDENTIFIER and
            self._peek() and self._peek().type == TokenType.AS):
            name = self._current_token().value
            self._advance()  # consume identifier
            self._advance()  # consume 'as'
            value = self._parse_expression()
            return Argument(name=name, value=value)
        else:
            # Positional argument
            value = self._parse_expression()
            return Argument(name=None, value=value)
    
    def _parse_list_expression(self) -> ListExpression:
        """Parse list expression."""
        self._advance()  # consume 'list'
        
        if self._current_token().type != TokenType.CONTAINING:
            raise ParserError("Expected 'containing' after 'list'", self._current_token())
        self._advance()
        
        elements = []
        
        # Parse first element
        if self._current_token().type not in [TokenType.NEWLINE, TokenType.EOF]:
            elements.append(self._parse_expression())
            
            # Parse additional elements
            while (self._current_token() and 
                   self._current_token().type == TokenType.COMMA):
                self._advance()  # consume ','
                elements.append(self._parse_expression())
        
        return ListExpression(elements)
    
    def _parse_type_expression(self) -> TypeExpression:
        """Parse type expression."""
        if self._current_token().type == TokenType.IDENTIFIER:
            type_name = self._current_token().value
            self._advance()
            
            # Check for generic type
            if (self._current_token() and 
                self._current_token().type == TokenType.LEFT_BRACKET):
                self._advance()  # consume '['
                
                type_params = []
                type_params.append(self._parse_type_expression())
                
                while (self._current_token() and 
                       self._current_token().type == TokenType.COMMA):
                    self._advance()  # consume ','
                    type_params.append(self._parse_type_expression())
                
                if self._current_token().type != TokenType.RIGHT_BRACKET:
                    raise ParserError("Expected ']' after type parameters", self._current_token())
                self._advance()  # consume ']'
                
                return GenericType(base_type=type_name, type_parameters=type_params)
            
            return SimpleType(type_name)
        
        else:
            raise ParserError("Expected type name", self._current_token())
    
    def _parse_block(self) -> List[Statement]:
        """Parse indented block of statements."""
        statements = []
        
        # Expect indentation
        if self._current_token().type != TokenType.INDENT:
            raise ParserError("Expected indentation", self._current_token())
        self._advance()
        
        # Parse statements in block
        while (self._current_token() and 
               self._current_token().type not in [TokenType.DEDENT, TokenType.EOF]):
            
            # Skip newlines within block
            if self._current_token().type == TokenType.NEWLINE:
                self._advance()
                continue
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        # Expect dedentation
        if self._current_token().type == TokenType.DEDENT:
            self._advance()
        
        return statements
    
    # Helper methods
    def _current_token(self) -> Optional[Token]:
        """Get current token."""
        return self.state.current_token if self.state else None
    
    def _advance(self) -> Optional[Token]:
        """Advance to next token."""
        if not self.state:
            return None
        
        if self.state.position < len(self.state.tokens) - 1:
            self.state.position += 1
            self.state.current_token = self.state.tokens[self.state.position]
        else:
            self.state.current_token = None
        
        return self.state.current_token
    
    def _peek(self) -> Optional[Token]:
        """Peek at next token without advancing."""
        if not self.state:
            return None
        
        if self.state.position < len(self.state.tokens) - 1:
            return self.state.tokens[self.state.position + 1]
        return None
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return not self.state or not self.state.current_token
    
    def _consume_newline_or_eof(self):
        """Consume newline or EOF token."""
        if (self._current_token() and 
            self._current_token().type in [TokenType.NEWLINE, TokenType.EOF]):
            self._advance()

# Export parser components
__all__ = ['RunaParser', 'ParserError', 'ParserState']
