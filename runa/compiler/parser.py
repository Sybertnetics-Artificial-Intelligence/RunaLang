"""
Runa Parser

Recursive descent parser for the Runa natural language syntax.
Transforms tokens into an Abstract Syntax Tree (AST) following the 
Runa Formal Grammar Specifications exactly.
"""

from typing import List, Optional, Union, Any
from .tokens import Token, TokenType
from .lexer import RunaLexer
from .ast_nodes import *

class ParseError(Exception):
    """Exception raised for parsing errors."""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse error at line {token.line}, column {token.column}: {message}")

class RunaParser:
    """
    Recursive descent parser for Runa natural language syntax.
    
    Parses according to the Runa Formal Grammar Specifications:
    - Natural language keywords and operators
    - Multi-word constructs
    - Indentation-based scoping
    - All language constructs from the grammar
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors: List[ParseError] = []
    
    def current_token(self) -> Token:
        """Get the current token."""
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current]
    
    def peek_token(self, offset: int = 1) -> Token:
        """Peek at a token ahead by offset positions."""
        pos = self.current + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Advance to the next token and return the previous one."""
        token = self.current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token().type in token_types
    
    def consume(self, token_type: TokenType, message: str = None) -> Token:
        """Consume a token of the given type or raise an error."""
        if self.match(token_type):
            return self.advance()
        
        if message is None:
            message = f"Expected {token_type.name}"
        
        error = ParseError(message, self.current_token())
        self.errors.append(error)
        raise error
    
    def synchronize(self):
        """Synchronize after a parse error by advancing to the next statement."""
        self.advance()
        
        while not self.match(TokenType.EOF):
            if self.tokens[self.current - 1].type == TokenType.NEWLINE:
                return
            
            if self.match(TokenType.LET, TokenType.DEFINE, TokenType.SET,
                         TokenType.IF, TokenType.OTHERWISE, TokenType.WHILE,
                         TokenType.FOR, TokenType.PROCESS, TokenType.RETURN):
                return
            
            self.advance()
    
    def parse(self) -> Program:
        """Parse the entire program and return the AST."""
        statements = []
        self.errors = [] # Reset errors at the start of a new parse

        while not self.match(TokenType.EOF):
            # Skip any leading newlines or indentation tokens
            while self.match(TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT):
                self.advance()

            if self.match(TokenType.EOF):
                break # Re-check for EOF after skipping newlines

            try:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                # If we are not at the end of the file and got no statement, it's an error.
                elif not self.match(TokenType.EOF):
                    raise ParseError(
                        f"Invalid syntax at line {self.current_token().line}. Expected a valid statement.",
                        self.current_token()
                    )
            except ParseError as e:
                self.errors.append(e)
                # For this phase, we will stop at the first error to ensure tests are strict.
                # In the future, we could implement synchronization here.
                raise e
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[Statement]:
        """Parse a statement according to the grammar."""
        # Skip leading newlines
        while self.match(TokenType.NEWLINE):
            self.advance()
        
        if self.match(TokenType.EOF):
            return None
        
        # Variable declarations and process definitions starting with 'Define'
        if self.match(TokenType.LET):
            return self.parse_let_statement()
        elif self.match(TokenType.DEFINE):
            # Peek ahead to detect 'Define process' (where 'process' may be IDENTIFIER)
            next_tok = self.peek_token()
            if next_tok.type == TokenType.PROCESS or (next_tok.type == TokenType.IDENTIFIER and next_tok.value.lower() == 'process'):
                return self.parse_process_definition()
            else:
                return self.parse_define_statement()
        elif self.match(TokenType.SET):
            return self.parse_set_statement()
        
        # Control flow
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.UNLESS):
            return self.parse_unless_statement()
        elif self.match(TokenType.WHEN):
            return self.parse_when_statement()
        elif self.match(TokenType.MATCH):
            return self.parse_match_statement()
        
        # Loops
        elif self.match(TokenType.FOR):
            return self.parse_for_loop()
        elif self.match(TokenType.WHILE):
            return self.parse_while_loop()
        elif self.match(TokenType.DO):
            return self.parse_do_while_loop()
        elif self.match(TokenType.REPEAT):
            return self.parse_repeat_loop()
        
        # Function/Process definition
        elif self.match(TokenType.PROCESS):
            return self.parse_process_definition()
        
        # Control flow statements
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.BREAK):
            self.advance()
            return BreakStatement()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            return ContinueStatement()
        
        # I/O statements
        elif self.match(TokenType.DISPLAY):
            return self.parse_display_statement()
        
        # Type definitions
        elif self.match(TokenType.TYPE):
            return self.parse_type_definition()
        
        # Expression statement
        else:
            expr = self.parse_expression()
            if not expr:
                # If we couldn't parse an expression here, it's a syntax error
                # unless it's just the end of the file.
                if not self.match(TokenType.EOF):
                    raise ParseError(
                        f"Invalid syntax. Expected a statement or expression, but found '{self.current_token().value}'.",
                        self.current_token()
                    )
                return None  # Legitimate end of file
            return ExpressionStatement(expr)
    
    def parse_let_statement(self) -> LetStatement:
        """Parse: Let identifier [type_annotation] be expression"""
        self.consume(TokenType.LET)
        
        # Parse identifier (could be multi-word)
        identifier_token = self.consume(TokenType.IDENTIFIER, "Expected identifier after 'Let'")
        identifier_parts = [identifier_token.value]
        
        # Handle multi-word identifiers
        while self.match(TokenType.IDENTIFIER):
            identifier_parts.append(self.advance().value)
        
        identifier = " ".join(identifier_parts)
        
        # Optional type annotation: (Type)
        type_annotation = None
        if self.match(TokenType.LPAREN):
            type_annotation = self.parse_type_annotation()
        
        # Consume 'be'
        self.consume(TokenType.BE, "Expected 'be' in let statement")
        
        # Parse value expression
        value = self.parse_expression()
        if not value:
            raise ParseError("Incomplete statement: expected expression after 'be'", self.current_token())
        
        return LetStatement(identifier, type_annotation, value)
    
    def parse_define_statement(self) -> DefineStatement:
        """Parse: Define [constant] identifier [type_annotation] as expression"""
        self.consume(TokenType.DEFINE)
        
        # Check for 'constant' keyword
        is_constant = False
        if self.match(TokenType.CONSTANT):
            is_constant = True
            self.advance()
        
        # Parse identifier (could be multi-word)
        identifier_token = self.consume(TokenType.IDENTIFIER, "Expected identifier after 'Define'")
        identifier_parts = [identifier_token.value]
        
        # Handle multi-word identifiers
        while self.match(TokenType.IDENTIFIER):
            identifier_parts.append(self.advance().value)
        
        identifier = " ".join(identifier_parts)
        
        # Optional type annotation
        type_annotation = None
        if self.match(TokenType.LPAREN):
            type_annotation = self.parse_type_annotation()
        
        # Consume 'as'
        self.consume(TokenType.AS, "Expected 'as' in define statement")
        
        # Parse value expression
        value = self.parse_expression()
        if not value:
            raise ParseError("Incomplete statement: expected expression after 'as'", self.current_token())
        
        return DefineStatement(identifier, type_annotation, value, is_constant)
    
    def parse_set_statement(self) -> SetStatement:
        """Parse: Set target to expression"""
        self.consume(TokenType.SET)
        
        # Parse target (identifier, member access, or index access)
        target = self.parse_assignable()
        
        # Consume 'to'
        self.consume(TokenType.TO, "Expected 'to' in set statement")
        
        # Parse value expression
        value = self.parse_expression()
        if not value:
            raise ParseError("Incomplete statement: expected expression after 'to'", self.current_token())
        
        return SetStatement(target, value)
    
    def parse_assignable(self) -> Expression:
        """Parse an assignable expression (identifier, member access, index access)."""
        expr = self.parse_primary()
        
        # Handle multi-word identifiers
        if isinstance(expr, Identifier) and self.match(TokenType.IDENTIFIER):
            parts = [expr.name]
            while self.match(TokenType.IDENTIFIER):
                parts.append(self.advance().value)
            expr = Identifier(" ".join(parts))
        
        while True:
            if self.match(TokenType.DOT):
                self.advance()
                member_token = self.consume(TokenType.IDENTIFIER, "Expected member name after '.'")
                expr = MemberAccess(expr, member_token.value)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexAccess(expr, index)
            else:
                break
        
        return expr
    
    def parse_if_statement(self) -> IfStatement:
        """Parse: If condition: block [Otherwise if condition: block]* [Otherwise: block]?"""
        self.consume(TokenType.IF)
        
        # Parse condition
        condition = self.parse_expression()
        
        # Consume ':'
        self.consume(TokenType.COLON, "Expected ':' after if condition")
        
        # Parse then block
        then_block = self.parse_block()
        
        # Parse elif clauses
        elif_clauses = []
        while self.match(TokenType.OTHERWISE) and self.peek_token().type == TokenType.IF:
            self.advance()  # consume 'Otherwise'
            self.advance()  # consume 'if'
            
            elif_condition = self.parse_expression()
            self.consume(TokenType.COLON, "Expected ':' after elif condition")
            elif_block = self.parse_block()
            
            elif_clauses.append((elif_condition, elif_block))
        
        # Parse else block
        else_block = None
        if self.match(TokenType.OTHERWISE):
            self.advance()
            self.consume(TokenType.COLON, "Expected ':' after 'Otherwise'")
            else_block = self.parse_block()
        
        return IfStatement(condition, then_block, elif_clauses, else_block)
    
    def parse_unless_statement(self) -> UnlessStatement:
        """Parse: Unless condition: block"""
        self.consume(TokenType.UNLESS)
        condition = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':' after unless condition")
        block = self.parse_block()
        
        return UnlessStatement(condition, block)
    
    def parse_when_statement(self) -> WhenStatement:
        """Parse: When condition: block"""
        self.consume(TokenType.WHEN)
        condition = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':' after when condition")
        block = self.parse_block()
        
        return WhenStatement(condition, block)
    
    def parse_display_statement(self) -> DisplayStatement:
        """Parse: Display expression [with message expression]?"""
        self.consume(TokenType.DISPLAY)
        
        # Parse main expression - use primary to avoid consuming WITH token
        value = self.parse_primary()
        
        # Handle multi-word identifiers manually
        if isinstance(value, Identifier) and self.match(TokenType.IDENTIFIER):
            parts = [value.name]
            while self.match(TokenType.IDENTIFIER):
                parts.append(self.advance().value)
            value = Identifier(" ".join(parts))
        
        # Optional 'with message' clause
        prefix = None
        if self.match(TokenType.WITH):
            # Check if this is "with message" or a function call
            if self.peek_token().type == TokenType.MESSAGE:
                self.advance()  # consume 'with'
                self.advance()  # consume 'message'
                prefix = self.parse_expression()
            else:
                # This is a function call like "Display value with param as x"
                # Re-parse as function call
                function_call = self.parse_function_call(value)
                return ExpressionStatement(function_call)
        
        return DisplayStatement(value, prefix)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse: Return [expression]?"""
        self.consume(TokenType.RETURN)
        
        # Optional return value
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            value = self.parse_expression()
        
        return ReturnStatement(value)
    
    def parse_block(self) -> List[Statement]:
        """Parse an indented block of statements."""
        statements = []
        
        # Expect newline and indent
        if self.match(TokenType.NEWLINE):
            self.advance()
        
        if not self.match(TokenType.INDENT):
            # Single statement on same line
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            return statements
        
        self.advance()  # consume INDENT
        
        # Parse statements until DEDENT
        while not self.match(TokenType.DEDENT, TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                self.advance()
                continue
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_expression(self) -> Expression:
        """Parse an expression with operator precedence."""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> Expression:
        """Parse logical OR expression."""
        expr = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            operator = BinaryOperator.OR
            self.advance()
            right = self.parse_logical_and()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def parse_logical_and(self) -> Expression:
        """Parse logical AND expression."""
        expr = self.parse_equality()
        
        while self.match(TokenType.AND):
            operator = BinaryOperator.AND
            self.advance()
            right = self.parse_equality()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def parse_equality(self) -> Expression:
        """Parse equality comparison."""
        expr = self.parse_comparison()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            if self.match(TokenType.EQUALS):
                operator = BinaryOperator.EQUALS
            else:
                operator = BinaryOperator.NOT_EQUALS
            
            self.advance()
            right = self.parse_comparison()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def parse_comparison(self) -> Expression:
        """Parse comparison operators."""
        expr = self.parse_term()
        
        while self.match(TokenType.GREATER_THAN, TokenType.LESS_THAN,
                         TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            if self.match(TokenType.GREATER_THAN):
                operator = BinaryOperator.GREATER_THAN
            elif self.match(TokenType.LESS_THAN):
                operator = BinaryOperator.LESS_THAN
            elif self.match(TokenType.GREATER_EQUAL):
                operator = BinaryOperator.GREATER_EQUAL
            else:
                operator = BinaryOperator.LESS_EQUAL
            
            self.advance()
            right = self.parse_term()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def parse_term(self) -> Expression:
        """Parse addition and subtraction."""
        expr = self.parse_factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            if self.match(TokenType.PLUS):
                operator = BinaryOperator.PLUS
            else:
                operator = BinaryOperator.MINUS
            
            self.advance()
            right = self.parse_factor()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def parse_factor(self) -> Expression:
        """Parse multiplication, division, and modulo."""
        expr = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            if self.match(TokenType.MULTIPLY):
                operator = BinaryOperator.MULTIPLY
            elif self.match(TokenType.DIVIDE):
                operator = BinaryOperator.DIVIDE
            else:
                operator = BinaryOperator.MODULO
            
            self.advance()
            right = self.parse_unary()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def parse_unary(self) -> Expression:
        """Parse unary expressions."""
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.advance().value
            operand = self.parse_unary()
            return UnaryExpression(operator, operand)
        
        return self.parse_call()
    
    def parse_call(self) -> Expression:
        """Parse function calls and member access."""
        expr = self.parse_primary()
        
        # Handle multi-word identifiers for function calls
        # If we have an identifier followed by more identifiers, combine them
        if isinstance(expr, Identifier) and self.match(TokenType.IDENTIFIER):
            # Combine multiple identifiers into a single multi-word identifier
            parts = [expr.name]
            while self.match(TokenType.IDENTIFIER):
                parts.append(self.advance().value)
            expr = Identifier(" ".join(parts))
        
        while True:
            if self.match(TokenType.WITH):
                # Function call: function_name with args
                expr = self.parse_function_call(expr)
            elif self.match(TokenType.DOT):
                # Member access: object.member
                self.advance()
                member_token = self.consume(TokenType.IDENTIFIER, "Expected member name after '.'")
                expr = MemberAccess(expr, member_token.value)
            elif self.match(TokenType.LBRACKET):
                # Index access: object[index]
                self.advance()
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexAccess(expr, index)
            else:
                break
        
        return expr
    
    def parse_argument_value(self) -> Expression:
        """Parse an argument value, stopping at AND tokens."""
        # Parse expression but stop at AND (which is used to separate arguments)
        # This is similar to parse_expression but with lower precedence for AND
        return self.parse_equality()  # Parse up to equality, skip logical operators
    
    def parse_function_call(self, function_expr: Expression) -> FunctionCall:
        """Parse function call arguments after 'with'."""
        self.consume(TokenType.WITH)
        
        # Extract function name
        if not isinstance(function_expr, Identifier):
            raise ParseError("Function calls must use an identifier", self.current_token())
        function_name = function_expr.name
        
        arguments = []
        
        # Handle indented block for arguments
        if self.match(TokenType.COLON):
            self.consume(TokenType.COLON)
            if not self.match(TokenType.NEWLINE):
                raise ParseError("Expected a newline after ':' in function call", self.current_token())
            self.consume(TokenType.NEWLINE)
            
            self.consume(TokenType.INDENT, "Expected indented block for arguments")
            
            while not self.match(TokenType.DEDENT):
                # Skip any blank lines
                if self.match(TokenType.NEWLINE):
                    self.advance()
                    continue

                # Parse multi-word parameter name
                param_name_parts = [self.consume(TokenType.IDENTIFIER, "Expected parameter name").value]
                while self.match(TokenType.IDENTIFIER):
                    param_name_parts.append(self.advance().value)
                param_name = " ".join(param_name_parts)

                self.consume(TokenType.AS, f"Expected 'as' after parameter name '{param_name}'")
                
                value = self.parse_expression()
                if not value:
                    raise ParseError(f"Expected expression for parameter '{param_name}'", self.current_token())
                
                arguments.append((param_name, value))

                # Arguments in a block must be on separate lines
                if not self.match(TokenType.NEWLINE, TokenType.DEDENT, TokenType.EOF):
                    raise ParseError("Expected newline after argument in block", self.current_token())
                if self.match(TokenType.NEWLINE):
                    self.advance()

            self.consume(TokenType.DEDENT, "Expected dedent to end argument block")

        # Handle single line arguments: param as value and param2 as value2
        else:
            while not self.match(TokenType.NEWLINE, TokenType.EOF):
                # Parse multi-word parameter name
                param_name_parts = [self.consume(TokenType.IDENTIFIER, "Expected parameter name").value]
                while self.match(TokenType.IDENTIFIER):
                    param_name_parts.append(self.advance().value)
                param_name = " ".join(param_name_parts)

                self.consume(TokenType.AS, f"Expected 'as' after parameter name '{param_name}'")
                
                # Use specific argument value parser that stops at AND
                value = self.parse_argument_value()
                if not value:
                    raise ParseError(f"Expected expression for parameter '{param_name}'", self.current_token())
                
                arguments.append((param_name, value))
                
                # Check for 'and' to continue with more arguments
                if self.match(TokenType.AND):
                    self.advance()
                    continue
                else:
                    break
        
        return FunctionCall(function_name, arguments)
    
    def parse_primary(self) -> Expression:
        """Parse primary expressions (literals, identifiers, parentheses)."""
        if self.match(TokenType.EOF):
            raise ParseError("Unexpected end of file, expected an expression.", self.current_token())

        # Literals
        if self.match(TokenType.INTEGER):
            return IntegerLiteral(self.advance().value)
        
        if self.match(TokenType.FLOAT):
            return FloatLiteral(self.advance().value)
        
        if self.match(TokenType.STRING):
            return StringLiteral(self.advance().value)
        
        if self.match(TokenType.BOOLEAN):
            return BooleanLiteral(self.advance().value)
        
        # Identifier
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.advance().value)
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        # List literal: list containing elements  
        if self.match(TokenType.LIST):
            return self.parse_list_literal()
        
        raise ParseError(f"Unexpected token: {self.current_token().value}", self.current_token())
    
    def parse_list_literal(self) -> ListLiteral:
        """Parse: list containing element1, element2, ..."""
        # The lexer gives us "list containing" as a single LIST token
        self.consume(TokenType.LIST)
        
        elements = []
        
        while not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.COLON):
            elements.append(self.parse_expression())
            
            if self.match(TokenType.COMMA):
                self.advance()
            else:
                break
        
        return ListLiteral(elements)
    
    def parse_type_annotation(self) -> TypeExpression:
        """Parse a type annotation: (Type)"""
        self.consume(TokenType.LPAREN)
        
        # Basic types
        if self.match(TokenType.INTEGER_TYPE):
            self.advance()
            type_expr = BasicType("Integer")
        elif self.match(TokenType.FLOAT_TYPE):
            self.advance()
            type_expr = BasicType("Float")
        elif self.match(TokenType.STRING_TYPE):
            self.advance()
            type_expr = BasicType("String")
        elif self.match(TokenType.BOOLEAN_TYPE):
            self.advance()
            type_expr = BasicType("Boolean")
        else:
            # For now, treat any identifier as a type
            type_token = self.consume(TokenType.IDENTIFIER, "Expected type name")
            type_expr = BasicType(type_token.value)
        
        self.consume(TokenType.RPAREN, "Expected ')' after type annotation")
        return type_expr
    
    def parse_process_definition(self) -> ProcessDefinition:
        """Parse process definition statement."""
        # Syntax: Define process <name> [with param1 [and param2 ...]]:
        self.consume(TokenType.DEFINE)
        process_token = None
        if self.match(TokenType.PROCESS):
            process_token = self.advance()
        elif self.match(TokenType.IDENTIFIER) and self.current_token().value.lower() == 'process':
            process_token = self.advance()
        else:
            raise ParseError("Expected 'process' after 'Define'", self.current_token())

        # Parse process name (could be multi-word) until we hit 'with' or ':'
        name_parts = []
        while not self.match(TokenType.WITH, TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
            if self.match(TokenType.IDENTIFIER, TokenType.STRING):
                name_parts.append(self.advance().value)
            else:
                break
        if not name_parts:
            raise ParseError("Expected process name", self.current_token())
        process_name = " ".join(name_parts)

        parameters: List[Parameter] = []

        # Parse parameter list if present
        if self.match(TokenType.WITH):
            self.advance()  # consume WITH
            while not self.match(TokenType.COLON):
                param_token = self.consume(TokenType.IDENTIFIER, "Expected parameter name")
                param_name = param_token.value
                # For now we do not support type annotations within parameter list
                parameters.append(Parameter(param_name))
                # Handle 'and' between parameters
                if self.match(TokenType.AND):
                    self.advance()
                    continue
                else:
                    break

        # Expect ':' then block
        self.consume(TokenType.COLON, "Expected ':' after process signature")
        body_block = self.parse_block()

        return ProcessDefinition(process_name, parameters, None, body_block)
    
    def parse_for_loop(self) -> Statement:
        """Parse for-each and for-range loops."""
        for_token = self.consume(TokenType.FOR)

        # Support lexer combining 'For each' into single FOR token
        is_for_each_combined = for_token.value.lower().startswith("for each")

        # For each loop: For each item in iterable:
        if is_for_each_combined or self.match(TokenType.EACH):
            if not is_for_each_combined:
                self.advance()  # consume EACH
            var_token = self.consume(TokenType.IDENTIFIER, "Expected loop variable after 'each'")
            variable_name = var_token.value
            self.consume(TokenType.IN, "Expected 'in' after loop variable")
            iterable = self.parse_expression()
            self.consume(TokenType.COLON, "Expected ':' after iterable expression")
            block = self.parse_block()
            return ForEachLoop(variable_name, iterable, block)

        # Otherwise for-range loop: For i from start to end [step step_expr]:
        var_token = self.consume(TokenType.IDENTIFIER, "Expected loop variable after 'For'")
        variable_name = var_token.value
        self.consume(TokenType.FROM, "Expected 'from' in for-range loop")
        start_expr = self.parse_expression()
        self.consume(TokenType.TO, "Expected 'to' in for-range loop")
        end_expr = self.parse_expression()
        step_expr = None
        if self.match(TokenType.STEP):
            self.advance()
            step_expr = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':' after range expression")
        block = self.parse_block()
        return ForRangeLoop(variable_name, start_expr, end_expr, step_expr, block)
    
    def parse_while_loop(self) -> WhileLoop:
        """Parse: While condition: block"""
        self.consume(TokenType.WHILE)
        condition = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':' after while condition")
        block = self.parse_block()
        return WhileLoop(condition, block)
    
    def parse_do_while_loop(self) -> DoWhileLoop:
        """Parse do-while loop - placeholder for now."""
        raise ParseError("Do-while loops not yet implemented", self.current_token())
    
    def parse_repeat_loop(self) -> RepeatLoop:
        """Parse repeat loop - placeholder for now."""
        raise ParseError("Repeat loops not yet implemented", self.current_token())
    
    def parse_match_statement(self) -> MatchStatement:
        """Parse match statement - placeholder for now."""
        raise ParseError("Match statements not yet implemented", self.current_token())
    
    def parse_type_definition(self) -> TypeDefinition:
        """Parse type definition - placeholder for now."""
        raise ParseError("Type definitions not yet implemented", self.current_token())

def parse_runa_source(source: str) -> Program:
    """Convenience function to parse Runa source code."""
    lexer = RunaLexer(source)
    tokens = lexer.tokenize()
    parser = RunaParser(tokens)
    
    program = parser.parse()
    
    # If there were parse errors, raise the first one
    if parser.errors:
        raise parser.errors[0]
    
    return program 