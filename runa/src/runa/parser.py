"""
Recursive Descent Parser for Runa Programming Language.

This module implements a complete recursive descent parser that converts
tokenized Runa source code into an Abstract Syntax Tree (AST).

Features:
- Complete grammar implementation based on formal EBNF specification
- Error recovery mechanisms
- Source position tracking
- Natural language operator parsing
- AI/ML construct support
- Comprehensive error reporting
"""

from typing import List, Optional, Union, Dict, Any, Tuple
from dataclasses import dataclass

from .lexer import RunaLexer, Token, TokenType
from .ast_nodes import *
from .errors import (
    SourcePosition, RunaSyntaxError, ErrorReporter, syntax_error,
    ErrorSeverity
)


class ParseResult:
    """
    Result of parsing operation with error tracking.
    """
    def __init__(self, success: bool, node: Optional[ASTNode] = None, errors: Optional[List[RunaSyntaxError]] = None):
        self.success = success
        self.node = node
        self.errors = errors or []
    
    @staticmethod
    def success_result(node: ASTNode) -> 'ParseResult':
        """Create a successful parse result."""
        return ParseResult(True, node)
    
    @staticmethod
    def error_result(error: RunaSyntaxError) -> 'ParseResult':
        """Create an error parse result."""
        return ParseResult(False, None, [error])


class RunaParser:
    """
    Recursive descent parser for Runa programming language.
    
    Implements the complete formal grammar specification and provides
    comprehensive error handling and recovery mechanisms.
    """
    
    def __init__(self, tokens: List[Token], error_reporter: Optional[ErrorReporter] = None):
        """
        Initialize the parser with tokens.
        
        Args:
            tokens: List of tokens from the lexer
            error_reporter: Optional error reporter for centralized error handling
        """
        self.tokens = tokens
        self.current = 0
        self.errors: List[RunaSyntaxError] = []
        self.error_reporter = error_reporter or ErrorReporter()
        self.panic_mode = False
        
        # Track parsing context for better error messages
        self.parsing_context: List[str] = []
    
    # ========== UTILITY METHODS ==========
    
    def current_token(self) -> Token:
        """Get the current token."""
        if self.current >= len(self.tokens):
            return Token(
                type=TokenType.EOF,
                value="",
                line=self.tokens[-1].line if self.tokens else 1,
                column=self.tokens[-1].column if self.tokens else 1
            )
        return self.tokens[self.current]
    
    def peek(self, offset: int = 1) -> Token:
        """Peek at a token ahead of current position."""
        pos = self.current + offset
        if pos >= len(self.tokens):
            return Token(TokenType.EOF, "", 1, 1)
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Consume and return the current token."""
        token = self.current_token()
        if token.type != TokenType.EOF:
            self.current += 1
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token().type in token_types
    
    def check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type."""
        return self.current_token().type == token_type
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """
        Consume a token of the expected type or report an error.
        
        Returns:
            The consumed token if successful, or a dummy token if error.
        """
        if self.check(token_type):
            return self.advance()
        
        self.error(message)
        return Token(token_type, "", self.current_token().line, self.current_token().column)
    
    def error(self, message: str, token: Optional[Token] = None) -> None:
        """Report a parsing error."""
        error_token = token or self.current_token()
        context = " (in " + " -> ".join(self.parsing_context) + ")" if self.parsing_context else ""
        
        error = syntax_error(
            f"{message}{context}",
            SourcePosition(error_token.line, error_token.column, error_token.filename),
            f"Found '{error_token.value}' ({error_token.type.name})"
        )
        
        self.errors.append(error)
        self.error_reporter.add_error(error)
        
        if not self.panic_mode:
            self.panic_mode = True
    
    def synchronize(self) -> None:
        """
        Synchronize parser state after an error.
        
        Advances tokens until we reach a statement boundary
        or other recovery point.
        """
        self.panic_mode = False
        
        while not self.check(TokenType.EOF):
            # Skip to next statement-like token
            if self.current_token().type in [
                TokenType.LET, TokenType.DEFINE, TokenType.SET,
                TokenType.IF, TokenType.WHILE, TokenType.FOR,
                TokenType.PROCESS, TokenType.RETURN,
                TokenType.DISPLAY, TokenType.IMPORT,
                TokenType.TRY, TokenType.NEWLINE
            ]:
                return
            self.advance()
    
    def enter_context(self, context: str) -> None:
        """Enter a parsing context for better error messages."""
        self.parsing_context.append(context)
    
    def exit_context(self) -> None:
        """Exit the current parsing context."""
        if self.parsing_context:
            self.parsing_context.pop()
    
    # ========== MAIN PARSING METHODS ==========
    
    def parse(self) -> ParseResult:
        """
        Parse the tokens into an AST.
        
        Returns:
            ParseResult containing the AST or error information.
        """
        try:
            self.enter_context("program")
            statements = []
            
            while not self.check(TokenType.EOF):
                # Skip newlines at top level
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                
                stmt_result = self.parse_statement()
                if stmt_result.success and stmt_result.node:
                    statements.append(stmt_result.node)
                elif self.panic_mode:
                    self.synchronize()
            
            self.exit_context()
            
            program = Program(
                position=SourcePosition(1, 1),
                node_type=NodeType.PROGRAM,
                statements=statements
            )
            
            if self.errors:
                return ParseResult(False, program, self.errors)
            else:
                return ParseResult.success_result(program)
                
        except Exception as e:
            error = syntax_error(
                f"Unexpected parsing error: {str(e)}",
                SourcePosition(
                    self.current_token().line,
                    self.current_token().column
                )
            )
            return ParseResult.error_result(error)
    
    # ========== STATEMENT PARSING ==========
    
    def parse_statement(self) -> ParseResult:
        """Parse a single statement."""
        self.enter_context("statement")
        
        try:
            # Handle different statement types
            if self.match(TokenType.LET, TokenType.DEFINE):
                result = self.parse_declaration()
            elif self.match(TokenType.SET):
                result = self.parse_assignment()
            elif self.match(TokenType.DISPLAY):
                result = self.parse_display_statement()
            elif self.check(TokenType.COMMENT):
                result = self.parse_comment()
            else:
                # Try parsing as expression statement
                result = self.parse_expression_statement()
            
            self.exit_context()
            return result
            
        except Exception as e:
            self.error(f"Error parsing statement: {str(e)}")
            self.exit_context()
            return ParseResult.error_result(syntax_error(str(e), SourcePosition(1, 1)))
    
    def parse_declaration(self) -> ParseResult:
        """Parse variable declaration: 'Let x be 5' or 'Define name as "Alex"'"""
        self.enter_context("declaration")
        
        start_token = self.current_token()
        is_constant = self.match(TokenType.DEFINE)
        
        if is_constant:
            self.advance()  # consume 'define'
        else:
            self.advance()  # consume 'let'
        
        # Parse identifier
        if not self.check(TokenType.IDENTIFIER):
            self.error("Expected variable name after 'let' or 'define'")
            self.exit_context()
            return ParseResult.error_result(syntax_error("Expected identifier", SourcePosition(1, 1)))
        
        identifier = self.advance().value
        
        # Optional type annotation
        type_annotation = None
        if self.check(TokenType.LPAREN):
            type_result = self.parse_type_annotation()
            if type_result.success:
                type_annotation = type_result.node
        
        # Expect 'be' or 'as'
        if is_constant:
            self.consume(TokenType.AS, "Expected 'as' after constant name")
        else:
            self.consume(TokenType.BE, "Expected 'be' after variable name")
        
        # Parse initializer expression
        expr_result = self.parse_expression()
        if not expr_result.success:
            self.exit_context()
            return expr_result
        
        declaration = Declaration(
            position=SourcePosition(start_token.line, start_token.column),
            node_type=NodeType.DECLARATION,
            identifier=identifier,
            type_annotation=type_annotation,
            initializer=expr_result.node,
            is_constant=is_constant
        )
        
        self.exit_context()
        return ParseResult.success_result(declaration)
    
    def parse_assignment(self) -> ParseResult:
        """Parse assignment: 'Set x to 10'"""
        self.enter_context("assignment")
        
        start_token = self.advance()  # consume 'set'
        
        if not self.check(TokenType.IDENTIFIER):
            self.error("Expected variable name after 'set'")
            self.exit_context()
            return ParseResult.error_result(syntax_error("Expected identifier", SourcePosition(1, 1)))
        
        identifier = self.advance().value
        
        self.consume(TokenType.TO, "Expected 'to' after variable name in assignment")
        
        expr_result = self.parse_expression()
        if not expr_result.success:
            self.exit_context()
            return expr_result
        
        assignment = Assignment(
            position=SourcePosition(start_token.line, start_token.column),
            node_type=NodeType.ASSIGNMENT,
            identifier=identifier,
            value=expr_result.node
        )
        
        self.exit_context()
        return ParseResult.success_result(assignment)
    
    def parse_display_statement(self) -> ParseResult:
        """Parse display statement."""
        start_token = self.advance()  # consume 'display'
        
        expr_result = self.parse_expression()
        if not expr_result.success:
            return expr_result
        
        # Optional message
        message = None
        if self.match(TokenType.WITH):
            self.advance()  # consume 'with'
            # Look for message keyword or just take next expression
            if self.match(TokenType.WITH_MESSAGE):
                self.advance()
            
            message_result = self.parse_expression()
            if message_result.success:
                message = message_result.node
        
        display_stmt = DisplayStatement(
            position=SourcePosition(start_token.line, start_token.column),
            node_type=NodeType.DISPLAY_STATEMENT,
            expression=expr_result.node,
            message=message
        )
        
        return ParseResult.success_result(display_stmt)
    
    def parse_expression_statement(self) -> ParseResult:
        """Parse an expression as a statement."""
        expr_result = self.parse_expression()
        if not expr_result.success:
            return expr_result
        
        expr_stmt = ExpressionStatement(
            position=expr_result.node.position,
            node_type=NodeType.EXPRESSION_STATEMENT,
            expression=expr_result.node
        )
        
        return ParseResult.success_result(expr_stmt)
    
    def parse_comment(self) -> ParseResult:
        """Parse a comment."""
        token = self.advance()  # consume comment
        
        comment = Comment(
            position=SourcePosition(token.line, token.column),
            node_type=NodeType.COMMENT,
            text=token.value
        )
        
        return ParseResult.success_result(comment)
    
    # ========== EXPRESSION PARSING ==========
    
    def parse_expression(self) -> ParseResult:
        """Parse an expression (top level)."""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ParseResult:
        """Parse logical OR expressions."""
        left_result = self.parse_logical_and()
        if not left_result.success:
            return left_result
        
        while self.match(TokenType.OR):
            operator_token = self.advance()
            right_result = self.parse_logical_and()
            if not right_result.success:
                return right_result
            
            left_result = ParseResult.success_result(
                BinaryExpression(
                    position=SourcePosition(operator_token.line, operator_token.column),
                    node_type=NodeType.BINARY_EXPRESSION,
                    left=left_result.node,
                    operator=BinaryOperator.OR,
                    right=right_result.node
                )
            )
        
        return left_result
    
    def parse_logical_and(self) -> ParseResult:
        """Parse logical AND expressions."""
        left_result = self.parse_equality()
        if not left_result.success:
            return left_result
        
        while self.match(TokenType.AND):
            operator_token = self.advance()
            right_result = self.parse_equality()
            if not right_result.success:
                return right_result
            
            left_result = ParseResult.success_result(
                BinaryExpression(
                    position=SourcePosition(operator_token.line, operator_token.column),
                    node_type=NodeType.BINARY_EXPRESSION,
                    left=left_result.node,
                    operator=BinaryOperator.AND,
                    right=right_result.node
                )
            )
        
        return left_result
    
    def parse_equality(self) -> ParseResult:
        """Parse equality and comparison expressions."""
        left_result = self.parse_comparison()
        if not left_result.success:
            return left_result
        
        while True:
            if self.match(TokenType.IS):
                # Handle various "is" expressions
                is_token = self.advance()
                
                if self.match(TokenType.EQUAL):
                    self.advance()
                    if self.match(TokenType.TO):
                        self.advance()
                    operator = BinaryOperator.EQUALS
                
                elif self.match(TokenType.GREATER):
                    self.advance()
                    self.consume(TokenType.THAN, "Expected 'than' after 'is greater'")
                    operator = BinaryOperator.GREATER_THAN
                
                elif self.match(TokenType.LESS):
                    self.advance()
                    self.consume(TokenType.THAN, "Expected 'than' after 'is less'")
                    operator = BinaryOperator.LESS_THAN
                
                else:
                    self.error("Invalid comparison after 'is'")
                    return ParseResult.error_result(syntax_error("Invalid comparison", SourcePosition(1, 1)))
                
                right_result = self.parse_comparison()
                if not right_result.success:
                    return right_result
                
                left_result = ParseResult.success_result(
                    BinaryExpression(
                        position=SourcePosition(is_token.line, is_token.column),
                        node_type=NodeType.BINARY_EXPRESSION,
                        left=left_result.node,
                        operator=operator,
                        right=right_result.node
                    )
                )
            else:
                break
        
        return left_result
    
    def parse_comparison(self) -> ParseResult:
        """Parse comparison expressions."""
        return self.parse_term()
    
    def parse_term(self) -> ParseResult:
        """Parse addition and subtraction."""
        left_result = self.parse_factor()
        if not left_result.success:
            return left_result
        
        while True:
            if self.match(TokenType.PLUS):
                operator_token = self.advance()
                operator = BinaryOperator.ADD
            elif self.match(TokenType.MINUS):
                operator_token = self.advance()
                operator = BinaryOperator.SUBTRACT
            elif self.match(TokenType.FOLLOWED):
                operator_token = self.advance()
                if self.match(TokenType.BY):
                    self.advance()
                operator = BinaryOperator.CONCATENATE
            else:
                break
            
            right_result = self.parse_factor()
            if not right_result.success:
                return right_result
            
            left_result = ParseResult.success_result(
                BinaryExpression(
                    position=SourcePosition(operator_token.line, operator_token.column),
                    node_type=NodeType.BINARY_EXPRESSION,
                    left=left_result.node,
                    operator=operator,
                    right=right_result.node
                )
            )
        
        return left_result
    
    def parse_factor(self) -> ParseResult:
        """Parse multiplication and division."""
        left_result = self.parse_unary()
        if not left_result.success:
            return left_result
        
        while True:
            if self.match(TokenType.MULTIPLIED):
                operator_token = self.advance()
                self.consume(TokenType.BY, "Expected 'by' after 'multiplied'")
                operator = BinaryOperator.MULTIPLY
            elif self.match(TokenType.DIVIDED):
                operator_token = self.advance()
                self.consume(TokenType.BY, "Expected 'by' after 'divided'")
                operator = BinaryOperator.DIVIDE
            else:
                break
            
            right_result = self.parse_unary()
            if not right_result.success:
                return right_result
            
            left_result = ParseResult.success_result(
                BinaryExpression(
                    position=SourcePosition(operator_token.line, operator_token.column),
                    node_type=NodeType.BINARY_EXPRESSION,
                    left=left_result.node,
                    operator=operator,
                    right=right_result.node
                )
            )
        
        return left_result
    
    def parse_unary(self) -> ParseResult:
        """Parse unary expressions."""
        if self.match(TokenType.NOT):
            operator_token = self.advance()
            expr_result = self.parse_unary()
            if not expr_result.success:
                return expr_result
            
            return ParseResult.success_result(
                UnaryExpression(
                    position=SourcePosition(operator_token.line, operator_token.column),
                    node_type=NodeType.UNARY_EXPRESSION,
                    operator=UnaryOperator.NOT,
                    operand=expr_result.node
                )
            )
        
        return self.parse_primary()
    
    def parse_primary(self) -> ParseResult:
        """Parse primary expressions."""
        # Literals
        if self.match(TokenType.NUMBER):
            token = self.advance()
            value = float(token.value) if '.' in token.value else int(token.value)
            
            return ParseResult.success_result(
                Literal(
                    position=SourcePosition(token.line, token.column),
                    node_type=NodeType.LITERAL,
                    value=value,
                    literal_type="number"
                )
            )
        
        if self.match(TokenType.STRING):
            token = self.advance()
            value = token.value.strip('"\'')
            
            return ParseResult.success_result(
                Literal(
                    position=SourcePosition(token.line, token.column),
                    node_type=NodeType.LITERAL,
                    value=value,
                    literal_type="string"
                )
            )
        
        if self.match(TokenType.BOOLEAN):
            token = self.advance()
            value = token.value.lower() == "true"
            
            return ParseResult.success_result(
                Literal(
                    position=SourcePosition(token.line, token.column),
                    node_type=NodeType.LITERAL,
                    value=value,
                    literal_type="boolean"
                )
            )
        
        if self.match(TokenType.NULL):
            token = self.advance()
            
            return ParseResult.success_result(
                Literal(
                    position=SourcePosition(token.line, token.column),
                    node_type=NodeType.LITERAL,
                    value=None,
                    literal_type="null"
                )
            )
        
        # Identifiers and function calls
        if self.match(TokenType.IDENTIFIER):
            token = self.advance()
            
            # Check if this is a function call
            if self.match(TokenType.WITH):
                return self.parse_function_call(token.value, token)
            else:
                return ParseResult.success_result(
                    Identifier(
                        position=SourcePosition(token.line, token.column),
                        node_type=NodeType.IDENTIFIER,
                        name=token.value
                    )
                )
        
        # Parenthesized expressions
        if self.match(TokenType.LPAREN):
            self.advance()
            expr_result = self.parse_expression()
            if not expr_result.success:
                return expr_result
            
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr_result
        
        # List expressions
        if self.match(TokenType.LIST):
            return self.parse_list_expression()
        
        self.error(f"Unexpected token: {self.current_token().value}")
        return ParseResult.error_result(syntax_error("Unexpected token", SourcePosition(1, 1)))
    
    # ========== HELPER PARSING METHODS ==========
    
    def parse_type_annotation(self) -> ParseResult:
        """Parse type annotation: (type_name) or (type_name of other_type)"""
        start_token = self.consume(TokenType.LPAREN, "Expected '(' for type annotation")
        
        if not self.check(TokenType.IDENTIFIER):
            self.error("Expected type name in type annotation")
            return ParseResult.error_result(syntax_error("Expected type name", SourcePosition(1, 1)))
        
        type_name = self.advance().value
        
        # Handle generic types (e.g., "list of string")
        generic_args = None
        if self.match(TokenType.OF):
            self.advance()  # consume 'of'
            
            # Parse the generic argument type
            if self.check(TokenType.IDENTIFIER):
                arg_type_name = self.advance().value
                arg_type = TypeAnnotation(
                    position=SourcePosition(self.current_token().line, self.current_token().column),
                    node_type=NodeType.TYPE_ANNOTATION,
                    type_name=arg_type_name,
                    generic_args=None
                )
                generic_args = [arg_type]
        
        self.consume(TokenType.RPAREN, "Expected ')' after type annotation")
        
        type_annotation = TypeAnnotation(
            position=SourcePosition(start_token.line, start_token.column),
            node_type=NodeType.TYPE_ANNOTATION,
            type_name=type_name,
            generic_args=generic_args
        )
        
        return ParseResult.success_result(type_annotation)
    
    def parse_function_call(self, function_name: str, name_token: Token) -> ParseResult:
        """Parse function call with named arguments."""
        self.advance()  # consume 'with'
        
        arguments = []
        
        # Parse named arguments
        while True:
            if not self.check(TokenType.IDENTIFIER):
                break
            
            arg_name = self.advance().value
            self.consume(TokenType.AS, "Expected 'as' after argument name")
            
            value_result = self.parse_expression()
            if not value_result.success:
                return value_result
            
            arguments.append((arg_name, value_result.node))
            
            if not self.match(TokenType.AND):
                break
            self.advance()  # consume 'and'
        
        function_call = FunctionCall(
            position=SourcePosition(name_token.line, name_token.column),
            node_type=NodeType.FUNCTION_CALL,
            function_name=function_name,
            arguments=arguments,
            positional_args=[]
        )
        
        return ParseResult.success_result(function_call)
    
    def parse_list_expression(self) -> ParseResult:
        """Parse list expression: 'list containing 1, 2, 3'"""
        start_token = self.advance()  # consume 'list'
        self.consume(TokenType.CONTAINING, "Expected 'containing' after 'list'")
        
        elements = []
        
        # Parse list elements
        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.EOF):
            expr_result = self.parse_expression()
            if expr_result.success:
                elements.append(expr_result.node)
            
            while self.match(TokenType.COMMA):
                self.advance()  # consume ','
                
                expr_result = self.parse_expression()
                if expr_result.success:
                    elements.append(expr_result.node)
        
        list_expr = ListExpression(
            position=SourcePosition(start_token.line, start_token.column),
            node_type=NodeType.LIST_EXPRESSION,
            elements=elements
        )
        
        return ParseResult.success_result(list_expr)


# Export the main parser class
__all__ = ['RunaParser', 'ParseResult']
