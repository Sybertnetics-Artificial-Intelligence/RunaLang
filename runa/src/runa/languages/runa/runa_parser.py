"""
Runa Parser

Recursive descent parser for the Runa natural language syntax.
Transforms tokens into an Abstract Syntax Tree (AST) following the 
Runa Formal Grammar Specifications exactly.

This parser now inherits from BaseLanguageParser and integrates with
the hub-and-spoke translation system.
"""

from typing import List, Optional, Union, Any
from runa.core.base_components import BaseLanguageParser, ParseError, LanguageInfo, LanguageTier
from runa.core.runa_ast import *
from .tokens import Token, TokenType
from .lexer import RunaLexer

# Define Runa language info
RUNA_LANGUAGE_INFO = LanguageInfo(
    name="runa",
    tier=LanguageTier.TIER1,
    file_extensions=[".runa"],
    mime_types=["text/x-runa"],
    description="Natural Language Programming Language",
    version="0.3.0",
    is_compiled=True,
    is_interpreted=True,
    has_static_typing=True,
    has_dynamic_typing=True,
    comment_patterns=[r"Note:\s*(.*)"],
    string_patterns=[r'"([^"\\\\]|\\\\.)*"', r"'([^'\\\\]|\\\\.)*'"],
    number_patterns=[r"\d+\.?\d*"],
    identifier_patterns=[r"[a-zA-Z_][a-zA-Z0-9_\s]*"]
)


class RunaParseError(ParseError):
    """Runa-specific parse error."""
    def __init__(self, message: str, token: Token):
        location = SourceLocation(
            file_path="",
            line=token.line,
            column=token.column
        )
        super().__init__(message, location)
        self.token = token


class RunaParser(BaseLanguageParser):
    """
    Recursive descent parser for Runa natural language syntax.
    
    Parses according to the Runa Formal Grammar Specifications:
    - Natural language keywords and operators
    - Multi-word constructs
    - Indentation-based scoping
    - All language constructs from the grammar
    """
    
    def __init__(self, tokens: List[Token] = None):
        super().__init__(RUNA_LANGUAGE_INFO)
        self.tokens = tokens or []
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
    
    def parse(self, source_code: str, file_path: str = "") -> ASTNode:
        """Parse Runa source code into AST - BaseLanguageParser interface."""
        self._current_file_path = file_path
        
        try:
            # Import lexer here to avoid circular imports
            from .lexer import RunaLexer
            
            # Tokenize source code
            lexer = RunaLexer(source_code)
            tokens = lexer.tokenize()
            
            # Create new parser instance with tokens
            parser = RunaParser(tokens)
            parser._current_file_path = file_path
            
            # Parse the program
            program = parser.parse_program()
            
            # Check for parse errors
            if parser.errors:
                raise parser.errors[0]
            
            return program
            
        except Exception as e:
            raise ParseError(f"Failed to parse Runa code: {e}", self.create_location(1, 1))
    
    def parse_program(self) -> Program:
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
        
        # Error handling
        elif self.match(TokenType.TRY):
            return self.parse_try_statement()
        elif self.match(TokenType.THROW):
            return self.parse_throw_statement()
        
        # Module system
        elif self.match(TokenType.IMPORT):
            return self.parse_import_statement()
        elif self.match(TokenType.EXPORT):
            return self.parse_export_statement()
        elif self.match(TokenType.MODULE):
            return self.parse_module_declaration()
        
        # Async/concurrency statements
        elif self.match(TokenType.ASYNC):
            return self.parse_async_process_definition()
        elif self.match(TokenType.SEND):
            return self.parse_send_statement()
        elif self.match(TokenType.ATOMIC):
            return self.parse_atomic_block()
        elif self.match(TokenType.LOCK):
            return self.parse_lock_statement()
        
        # Memory management
        elif self.match(TokenType.DELETE):
            return self.parse_delete_statement()
        elif self.match(TokenType.AT):
            return self.parse_annotated_declaration()
        
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
        # Allow certain keywords to be used as identifiers in this context
        if self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
            identifier_token = self.advance()
            identifier_parts = [identifier_token.value]
        else:
            raise ParseError("Expected identifier after 'Let'", self.current_token())
        
        # Handle multi-word identifiers
        while self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
        if isinstance(expr, Identifier) and self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
            parts = [expr.name]
            while self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
        
        # Handle multi-word identifiers manually, including MESSAGE tokens
        if isinstance(value, Identifier) and self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
            parts = [value.name]
            while self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
        elif self.match(TokenType.AWAIT):
            self.advance()  # consume AWAIT
            operand = self.parse_unary()
            return AwaitExpression(operand)
        
        return self.parse_call()
    
    def parse_call(self) -> Expression:
        """Parse function calls and member access."""
        expr = self.parse_primary()
        
        # Handle multi-word identifiers for function calls
        # If we have an identifier followed by more identifiers, combine them
        if isinstance(expr, Identifier) and self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
            # Combine multiple identifiers into a single multi-word identifier
            parts = [expr.name]
            while self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
                if self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
                    param_name_parts = [self.advance().value]
                else:
                    raise ParseError("Expected parameter name", self.current_token())
                while self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
                if self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
                    param_name_parts = [self.advance().value]
                else:
                    raise ParseError("Expected parameter name", self.current_token())
                while self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
        
        # Identifier (including MESSAGE when used as identifier)
        if self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
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
        type_expr = self.parse_type_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after type annotation")
        return type_expr
    
    def parse_type_expression(self) -> TypeExpression:
        """Parse a complete type expression including unions, intersections, generics."""
        return self.parse_union_type()
    
    def parse_union_type(self) -> TypeExpression:
        """Parse union types: Type1 OR Type2 OR Type3"""
        type_expr = self.parse_intersection_type()
        
        if self.match(TokenType.OR):
            types = [type_expr]
            while self.match(TokenType.OR):
                self.advance()  # consume OR
                types.append(self.parse_intersection_type())
            return UnionType(types)
        
        return type_expr
    
    def parse_intersection_type(self) -> TypeExpression:
        """Parse intersection types: Type1 AND Type2 AND Type3"""
        type_expr = self.parse_optional_type()
        
        if self.match(TokenType.AND):
            types = [type_expr]
            while self.match(TokenType.AND):
                self.advance()  # consume AND
                types.append(self.parse_optional_type())
            return IntersectionType(types)
        
        return type_expr
    
    def parse_optional_type(self) -> TypeExpression:
        """Parse optional types: Optional[Type] or Optional Type"""
        if self.match(TokenType.OPTIONAL):
            self.advance()  # consume OPTIONAL
            
            # Handle both Optional[Type] and Optional Type syntax
            if self.match(TokenType.LBRACKET):
                self.advance()  # consume [
                inner_type = self.parse_type_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after optional type parameter")
                return OptionalType(inner_type)
            else:
                # Optional Type (without brackets)
                inner_type = self.parse_primary_type()
                return OptionalType(inner_type)
        
        return self.parse_primary_type()
    
    def parse_primary_type(self) -> TypeExpression:
        """Parse primary types: basic types, generics, function types."""
        # Basic types
        if self.match(TokenType.INTEGER_TYPE):
            self.advance()
            return BasicType("Integer")
        elif self.match(TokenType.FLOAT_TYPE):
            self.advance()
            return BasicType("Float")
        elif self.match(TokenType.STRING_TYPE):
            self.advance()
            return BasicType("String")
        elif self.match(TokenType.BOOLEAN_TYPE):
            self.advance()
            return BasicType("Boolean")
        elif self.match(TokenType.ANY):
            self.advance()
            return BasicType("Any")
        elif self.match(TokenType.VOID):
            self.advance()
            return BasicType("Void")
        elif self.match(TokenType.NEVER):
            self.advance()
            return BasicType("Never")
        
        # Generic types: List, Dictionary, Array, etc.
        elif self.match(TokenType.LIST):
            return self.parse_generic_type("List")
        elif self.match(TokenType.DICTIONARY):
            return self.parse_generic_type("Dictionary")
        elif self.match(TokenType.ARRAY):
            return self.parse_generic_type("Array")
        elif self.match(TokenType.TUPLE):
            return self.parse_generic_type("Tuple")
        
        # Function types
        elif self.match(TokenType.FUNCTION):
            return self.parse_function_type()
        
        # Parenthesized type expression
        elif self.match(TokenType.LPAREN):
            self.advance()  # consume (
            type_expr = self.parse_type_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after type expression")
            return type_expr
        
        # Custom type identifier
        elif self.match(TokenType.IDENTIFIER):
            type_token = self.advance()
            base_type = type_token.value
            
            # Check for generic parameters
            if self.match(TokenType.LBRACKET):
                self.advance()  # consume [
                type_args = []
                
                if not self.match(TokenType.RBRACKET):
                    type_args.append(self.parse_type_expression())
                    
                    while self.match(TokenType.COMMA):
                        self.advance()  # consume ,
                        type_args.append(self.parse_type_expression())
                
                self.consume(TokenType.RBRACKET, "Expected ']' after generic type parameters")
                return GenericType(base_type, type_args)
            else:
                return BasicType(base_type)
        
        else:
            raise ParseError("Expected type expression", self.current_token())
    
    def parse_generic_type(self, base_type: str) -> GenericType:
        """Parse generic types like List[Integer] or Dictionary[String, Integer]"""
        self.advance()  # consume the base type token
        
        if self.match(TokenType.LBRACKET):
            self.advance()  # consume [
            type_args = []
            
            if not self.match(TokenType.RBRACKET):
                type_args.append(self.parse_type_expression())
                
                while self.match(TokenType.COMMA):
                    self.advance()  # consume ,
                    type_args.append(self.parse_type_expression())
            
            self.consume(TokenType.RBRACKET, "Expected ']' after generic type parameters")
            return GenericType(base_type, type_args)
        else:
            # Generic type without parameters (defaults to Any)
            return GenericType(base_type, [BasicType("Any")])
    
    def parse_function_type(self) -> FunctionType:
        """Parse function types: Function[Type1, Type2, ReturnType]"""
        self.advance()  # consume FUNCTION
        
        if self.match(TokenType.LBRACKET):
            self.advance()  # consume [
            
            param_types = []
            return_type = BasicType("Void")
            
            # Parse parameter types and return type
            if not self.match(TokenType.RBRACKET):
                # First type could be parameter or return type if only one
                first_type = self.parse_type_expression()
                
                if self.match(TokenType.COMMA):
                    # Multiple types - last one is return type
                    param_types.append(first_type)
                    
                    while self.match(TokenType.COMMA):
                        self.advance()  # consume ,
                        next_type = self.parse_type_expression()
                        
                        # If this is the last type, it's the return type
                        if self.peek_token().type == TokenType.RBRACKET:
                            return_type = next_type
                            break
                        else:
                            param_types.append(next_type)
                else:
                    # Single type - assume it's the return type with no parameters
                    return_type = first_type
            
            self.consume(TokenType.RBRACKET, "Expected ']' after function type parameters")
            return FunctionType(param_types, return_type)
        else:
            # Function without type parameters
            return FunctionType([], BasicType("Any"))
    
    def _parse_simple_type(self) -> TypeExpression:
        """Parse a simple type name without parentheses - delegated to parse_primary_type."""
        return self.parse_primary_type()
    
    def parse_process_definition(self) -> ProcessDefinition:
        """Parse process definition statement."""
        # Syntax: Process called "name" [that takes param1 as Type [and param2 as Type ...]] [returns Type]:
        self.consume(TokenType.PROCESS, "Expected 'Process'")
        self.consume(TokenType.CALLED, "Expected 'called' after 'Process'")
        
        # Parse process name (should be a string literal)
        if self.match(TokenType.STRING):
            process_name = self.advance().value.strip('"')
        else:
            raise ParseError("Expected process name as string literal after 'called'", self.current_token())

        parameters: List[Parameter] = []
        return_type = None

        # Parse parameter list if present: "that takes x as Integer and y as String"
        if self.match(TokenType.THAT):
            self.advance()  # consume THAT
            self.consume(TokenType.TAKES, "Expected 'takes' after 'that'")
            
            # Parse parameters
            while not self.match(TokenType.COLON, TokenType.RETURNS, TokenType.NEWLINE, TokenType.EOF):
                # Parse parameter name
                param_token = self.consume(TokenType.IDENTIFIER, "Expected parameter name")
                param_name = param_token.value
                
                # Parse optional type annotation: "as Type"
                param_type = None
                if self.match(TokenType.AS):
                    self.advance()  # consume AS
                    param_type = self._parse_simple_type()
                
                parameters.append(Parameter(param_name, param_type))
                
                # Handle 'and' between parameters
                if self.match(TokenType.AND):
                    self.advance()
                    continue
                else:
                    break
        
        # Parse optional return type: "returns Type"
        if self.match(TokenType.RETURNS):
            self.advance()  # consume RETURNS
            return_type = self._parse_simple_type()

        # Expect ':' then block
        self.consume(TokenType.COLON, "Expected ':' after process signature")
        body_block = self.parse_block()

        return ProcessDefinition(process_name, parameters, return_type, body_block)
    
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
        """Parse: Do: block While condition"""
        self.consume(TokenType.DO)
        self.consume(TokenType.COLON, "Expected ':' after 'Do'")
        block = self.parse_block()
        
        # Expect 'While' and condition
        self.consume(TokenType.WHILE, "Expected 'While' after do-block")
        condition = self.parse_expression()
        
        return DoWhileLoop(block, condition)
    
    def parse_repeat_loop(self) -> RepeatLoop:
        """Parse: Repeat count times: block"""
        self.consume(TokenType.REPEAT)
        
        # Parse count expression
        count = self.parse_expression()
        
        # Expect 'times'
        self.consume(TokenType.TIMES, "Expected 'times' after repeat count")
        self.consume(TokenType.COLON, "Expected ':' after 'times'")
        
        # Parse block
        block = self.parse_block()
        
        return RepeatLoop(count, block)
    
    def parse_match_statement(self) -> MatchStatement:
        """Parse: Match expression: cases"""
        self.consume(TokenType.MATCH)
        
        # Parse value expression to match against
        value = self.parse_expression()
        
        # Expect colon and block
        self.consume(TokenType.COLON, "Expected ':' after match expression")
        
        # Parse cases
        cases = []
        
        # Expect newline and indent for cases
        if self.match(TokenType.NEWLINE):
            self.advance()
        
        if not self.match(TokenType.INDENT):
            raise ParseError("Expected indented cases after match statement", self.current_token())
        
        self.advance()  # consume INDENT
        
        # Parse case clauses
        while not self.match(TokenType.DEDENT, TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                self.advance()
                continue
            
            # Parse case
            case = self.parse_match_case()
            cases.append(case)
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        if not cases:
            raise ParseError("Match statement must have at least one case", self.current_token())
        
        return MatchStatement(value, cases)
    
    def parse_match_case(self) -> MatchCase:
        """Parse: Case pattern [if guard]: block"""
        self.consume(TokenType.CASE, "Expected 'Case' in match statement")
        
        # Parse pattern
        pattern = self.parse_pattern()
        
        # Optional guard: if condition
        guard = None
        if self.match(TokenType.IF):
            self.advance()
            guard = self.parse_expression()
        
        # Expect colon and block
        self.consume(TokenType.COLON, "Expected ':' after case pattern")
        block = self.parse_block()
        
        return MatchCase(pattern, guard, block)
    
    def parse_pattern(self) -> Pattern:
        """Parse a pattern for pattern matching."""
        # Wildcard pattern: _
        if self.match(TokenType.WILDCARD):
            self.advance()
            return WildcardPattern()
        
        # List pattern: [pattern1, pattern2, ...]
        if self.match(TokenType.LBRACKET):
            return self.parse_list_pattern()
        
        # Try to parse as expression first (for literals)
        # Then determine if it's a literal or identifier pattern
        if self.match(TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.BOOLEAN):
            # Literal pattern
            literal = self.parse_primary()
            return LiteralPattern(literal)
        
        # Identifier pattern
        if self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
            identifier_token = self.advance()
            return IdentifierPattern(identifier_token.value)
        
        raise ParseError(f"Invalid pattern: {self.current_token().value}", self.current_token())
    
    def parse_list_pattern(self) -> ListPattern:
        """Parse: [pattern1, pattern2, ...rest]"""
        self.consume(TokenType.LBRACKET)
        
        elements = []
        rest = None
        
        # Empty list pattern
        if self.match(TokenType.RBRACKET):
            self.advance()
            return ListPattern(elements)
        
        while not self.match(TokenType.RBRACKET):
            # Check for rest pattern: ...name
            if self.match(TokenType.DOT):
                # Look for ...identifier
                if (self.peek_token().type == TokenType.DOT and 
                    self.peek_token(2).type == TokenType.DOT and
                    self.peek_token(3).type in [TokenType.IDENTIFIER, TokenType.MESSAGE]):
                    # Consume the three dots
                    self.advance()  # first dot
                    self.advance()  # second dot  
                    self.advance()  # third dot
                    rest_token = self.advance()  # identifier
                    rest = rest_token.value
                    break
                else:
                    # Regular pattern starting with dot - parse as normal
                    pattern = self.parse_pattern()
                    elements.append(pattern)
            else:
                pattern = self.parse_pattern()
                elements.append(pattern)
            
            # Handle comma separation
            if self.match(TokenType.COMMA):
                self.advance()
            elif not self.match(TokenType.RBRACKET):
                # If we don't see a comma or closing bracket, check for rest pattern
                if not (self.match(TokenType.DOT) and rest is None):
                    break
        
        self.consume(TokenType.RBRACKET, "Expected ']' after list pattern")
        return ListPattern(elements, rest)
    
    def parse_try_statement(self) -> TryStatement:
        """Parse: Try: block [Catch exception as name: block]* [Finally: block]?"""
        self.consume(TokenType.TRY)
        self.consume(TokenType.COLON, "Expected ':' after 'Try'")
        
        # Parse try block
        try_block = self.parse_block()
        
        # Parse catch clauses
        catch_clauses = []
        while self.match(TokenType.CATCH):
            catch_clause = self.parse_catch_clause()
            catch_clauses.append(catch_clause)
        
        # Parse optional finally block
        finally_block = None
        if self.match(TokenType.FINALLY):
            self.advance()
            self.consume(TokenType.COLON, "Expected ':' after 'Finally'")
            finally_block = self.parse_block()
        
        if not catch_clauses and not finally_block:
            raise ParseError("Try statement must have at least one catch or finally clause", self.current_token())
        
        return TryStatement(try_block, catch_clauses, finally_block)
    
    def parse_catch_clause(self) -> CatchClause:
        """Parse: Catch [ExceptionType] [as name]: block"""
        self.consume(TokenType.CATCH)
        
        exception_type = None
        exception_name = None
        
        # Check for 'as name' without exception type
        if self.match(TokenType.AS):
            self.advance()
            name_token = self.consume(TokenType.IDENTIFIER, "Expected exception name after 'as'")
            exception_name = name_token.value
        # Optional exception type
        elif self.match(TokenType.IDENTIFIER, TokenType.MESSAGE):
            # Try to parse as type
            type_token = self.advance()
            exception_type = BasicType(type_token.value)
            
            # Optional 'as name'
            if self.match(TokenType.AS):
                self.advance()
                name_token = self.consume(TokenType.IDENTIFIER, "Expected exception name after 'as'")
                exception_name = name_token.value
        
        self.consume(TokenType.COLON, "Expected ':' after catch clause")
        block = self.parse_block()
        
        return CatchClause(exception_type, exception_name, block)
    
    def parse_throw_statement(self) -> ThrowStatement:
        """Parse: Throw expression"""
        self.consume(TokenType.THROW)
        
        # Parse exception expression
        exception = self.parse_expression()
        if not exception:
            raise ParseError("Expected expression after 'Throw'", self.current_token())
        
        return ThrowStatement(exception)
    
    def parse_type_definition(self) -> TypeDefinition:
        """Parse type definition - placeholder for now."""
        raise ParseError("Type definitions not yet implemented", self.current_token())
    
    def parse_import_statement(self) -> ImportStatement:
        """Parse import statement: Import "module" [as alias] [exposing name1, name2]"""
        self.consume(TokenType.IMPORT)
        
        # Parse module path (string literal)
        module_token = self.consume(TokenType.STRING, "Expected module path as string literal")
        module_path = module_token.value.strip('"\'')
        
        alias = None
        imported_names = None
        
        # Check for alias: "as alias"
        if self.match(TokenType.AS):
            self.advance()  # consume AS
            alias_token = self.consume(TokenType.IDENTIFIER, "Expected alias name after 'as'")
            alias = alias_token.value
        
        # Check for selective imports: "exposing name1, name2"
        if self.match(TokenType.EXPOSING):
            self.advance()  # consume EXPOSING
            imported_names = []
            
            # Parse first name
            name_token = self.consume(TokenType.IDENTIFIER, "Expected name after 'exposing'")
            imported_names.append(name_token.value)
            
            # Parse additional names separated by commas
            while self.match(TokenType.COMMA):
                self.advance()  # consume COMMA
                name_token = self.consume(TokenType.IDENTIFIER, "Expected name after comma")
                imported_names.append(name_token.value)
        
        return ImportStatement(module_path, alias, imported_names)
    
    def parse_export_statement(self) -> ExportStatement:
        """Parse export statement: Export name1, name2 or Export all"""
        self.consume(TokenType.EXPORT)
        
        exported_names = None
        
        if self.match(TokenType.ALL):
            self.advance()  # consume ALL
            # exported_names stays None to indicate export all
        else:
            # Parse specific exports
            exported_names = []
            
            # Parse first name
            name_token = self.consume(TokenType.IDENTIFIER, "Expected name or 'all' after 'Export'")
            exported_names.append(name_token.value)
            
            # Parse additional names separated by commas
            while self.match(TokenType.COMMA):
                self.advance()  # consume COMMA
                name_token = self.consume(TokenType.IDENTIFIER, "Expected name after comma")
                exported_names.append(name_token.value)
        
        return ExportStatement(exported_names)
    
    def parse_module_declaration(self) -> ModuleDeclaration:
        """Parse module declaration: Module "name" with: body"""
        self.consume(TokenType.MODULE)
        
        # Parse module name (string literal)
        name_token = self.consume(TokenType.STRING, "Expected module name as string literal")
        module_name = name_token.value.strip('"\'')
        
        # Expect "with:"
        self.consume(TokenType.WITH, "Expected 'with' after module name")
        self.consume(TokenType.COLON, "Expected ':' after 'with'")
        
        # Parse module body
        body = self.parse_block()
        
        return ModuleDeclaration(module_name, body)
    
    def parse_async_process_definition(self) -> AsyncProcessDefinition:
        """Parse async process definition: Async Process called "name": body"""
        self.consume(TokenType.ASYNC)
        self.consume(TokenType.PROCESS, "Expected 'Process' after 'Async'")
        self.consume(TokenType.CALLED, "Expected 'called' after 'Process'")
        
        # Parse process name (string literal)
        if self.match(TokenType.STRING):
            process_name = self.advance().value.strip('"')
        else:
            raise ParseError("Expected process name as string literal after 'called'", self.current_token())

        parameters: List[Parameter] = []
        return_type = None

        # Parse parameter list if present
        if self.match(TokenType.THAT):
            self.advance()  # consume THAT
            self.consume(TokenType.TAKES, "Expected 'takes' after 'that'")
            
            # Parse parameters (same as regular process)
            while not self.match(TokenType.COLON, TokenType.RETURNS, TokenType.NEWLINE, TokenType.EOF):
                param_token = self.consume(TokenType.IDENTIFIER, "Expected parameter name")
                param_name = param_token.value
                
                param_type = None
                if self.match(TokenType.AS):
                    self.advance()  # consume AS
                    param_type = self._parse_simple_type()
                
                parameters.append(Parameter(param_name, param_type))
                
                if self.match(TokenType.AND):
                    self.advance()
                    continue
                else:
                    break
        
        # Parse optional return type
        if self.match(TokenType.RETURNS):
            self.advance()  # consume RETURNS
            return_type = self._parse_simple_type()

        # Expect ':' then block
        self.consume(TokenType.COLON, "Expected ':' after async process signature")
        body_block = self.parse_block()

        return AsyncProcessDefinition(process_name, parameters, return_type, body_block)
    
    def parse_send_statement(self) -> SendStatement:
        """Parse send statement: Send message to target"""
        self.consume(TokenType.SEND)
        
        # Parse message expression
        message = self.parse_expression()
        
        # Expect 'to'
        self.consume(TokenType.TO, "Expected 'to' after message in Send statement")
        
        # Parse target expression
        target = self.parse_expression()
        
        return SendStatement(message, target)
    
    def parse_atomic_block(self) -> AtomicBlock:
        """Parse atomic block: Atomic: body"""
        self.consume(TokenType.ATOMIC)
        self.consume(TokenType.COLON, "Expected ':' after 'Atomic'")
        
        # Parse atomic block body
        body = self.parse_block()
        
        return AtomicBlock(body)
    
    def parse_lock_statement(self) -> LockStatement:
        """Parse lock statement: Lock resource: body"""
        self.consume(TokenType.LOCK)
        
        # Parse resource expression
        resource = self.parse_expression()
        
        self.consume(TokenType.COLON, "Expected ':' after lock resource")
        
        # Parse lock body
        body = self.parse_block()
        
        return LockStatement(resource, body)
    
    def parse_delete_statement(self) -> DeleteStatement:
        """Parse delete statement: Delete resource"""
        self.consume(TokenType.DELETE)
        
        # Parse target expression
        target = self.parse_expression()
        
        return DeleteStatement(target)
    
    def parse_annotated_declaration(self) -> AnnotatedVariableDeclaration:
        """Parse annotated variable declaration: @owned Let x be 42"""
        # Parse memory annotations
        annotations = []
        
        while self.match(TokenType.AT):
            self.advance()  # consume @
            annotation = self.parse_memory_annotation()
            annotations.append(annotation)
        
        # Parse base declaration (Let or Define)
        if self.match(TokenType.LET):
            base_decl = self.parse_let_statement()
        elif self.match(TokenType.DEFINE):
            base_decl = self.parse_define_statement()
        else:
            raise ParseError("Expected variable declaration after memory annotations", self.current_token())
        
        return AnnotatedVariableDeclaration(base_decl, annotations)
    
    def parse_memory_annotation(self) -> MemoryAnnotation:
        """Parse memory annotation: owned, borrowed, shared, lifetime('a)"""
        if self.match(TokenType.OWNED):
            self.advance()
            return OwnershipAnnotation("owned")
        elif self.match(TokenType.BORROWED):
            self.advance()
            return OwnershipAnnotation("borrowed")
        elif self.match(TokenType.SHARED):
            self.advance()
            return OwnershipAnnotation("shared")
        elif self.match(TokenType.LIFETIME):
            self.advance()
            self.consume(TokenType.LPAREN, "Expected '(' after 'lifetime'")
            
            # Parse lifetime name (should be an identifier starting with apostrophe or just identifier)
            if self.match(TokenType.IDENTIFIER):
                lifetime_name = self.advance().value
            else:
                raise ParseError("Expected lifetime name after 'lifetime('", self.current_token())
            
            self.consume(TokenType.RPAREN, "Expected ')' after lifetime name")
            return LifetimeAnnotation(lifetime_name)
        else:
            raise ParseError("Expected memory annotation (owned, borrowed, shared, lifetime)", self.current_token())

def parse_runa_source(source: str) -> Program:
    """Convenience function to parse Runa source code."""
    from .lexer import RunaLexer
    
    lexer = RunaLexer(source)
    tokens = lexer.tokenize()
    parser = RunaParser(tokens)
    
    program = parser.parse_program()
    
    # If there were parse errors, raise the first one
    if parser.errors:
        raise parser.errors[0]
    
    return program 