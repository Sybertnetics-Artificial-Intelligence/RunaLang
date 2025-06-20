"""
Runa Parser - Recursive Descent Parser Foundation

Implements the foundation for parsing Runa programming language with:
- Error recovery and source position tracking
- Comprehensive AST node hierarchy (30+ node types)
- Natural language-like syntax parsing
- AI-specific constructs support
"""

from typing import List, Optional, Any
from dataclasses import dataclass
from enum import Enum, auto

from .lexer import Token, TokenType, LexerError


class ParserError(Exception):
    """Parser-specific error with detailed context."""
    
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"ParserError at {token}: {message}")


class NodeType(Enum):
    """AST node types for comprehensive language support."""
    
    # Program Structure
    PROGRAM = auto()
    MODULE = auto()
    IMPORT = auto()
    EXPORT = auto()
    
    # Declarations
    VARIABLE_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    TYPE_DECLARATION = auto()
    CONSTANT_DECLARATION = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    IF_STATEMENT = auto()
    FOR_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    TRY_STATEMENT = auto()
    THROW_STATEMENT = auto()
    
    # Expressions
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    MEMBER_EXPRESSION = auto()
    ARRAY_EXPRESSION = auto()
    DICTIONARY_EXPRESSION = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    
    # AI-Specific Nodes
    REASONING_BLOCK = auto()
    IMPLEMENTATION_BLOCK = auto()
    VERIFICATION_BLOCK = auto()
    LLM_COMMUNICATION = auto()
    AI_AGENT_DEFINITION = auto()
    NEURAL_NETWORK_DEFINITION = auto()
    KNOWLEDGE_QUERY = auto()
    SELF_MODIFICATION = auto()
    
    # Type System
    TYPE_ANNOTATION = auto()
    GENERIC_TYPE = auto()
    UNION_TYPE = auto()
    INTERSECTION_TYPE = auto()
    FUNCTION_TYPE = auto()
    
    # Control Flow
    CONDITIONAL_EXPRESSION = auto()
    PATTERN_MATCHING = auto()
    GUARD_CLAUSE = auto()
    
    # Special Constructs
    UNCERTAINTY_EXPRESSION = auto()
    CONFIDENCE_EXPRESSION = auto()
    ANNOTATION = auto()


class ASTNode:
    """Base AST node with comprehensive metadata."""
    def __init__(self, node_type: NodeType, line: int, column: int, source_file: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_file = source_file
    
    def __str__(self) -> str:
        return f"{self.node_type.name}(line={self.line}, col={self.column})"


class Program:
    """Root program node."""
    def __init__(self, line: int, column: int, source_file: Optional[str] = None, statements: List['Statement'] = None):
        self.node_type = NodeType.PROGRAM
        self.line = line
        self.column = column
        self.source_file = source_file
        self.statements = statements if statements is not None else []


class Statement:
    """Base statement node."""
    def __init__(self, node_type: NodeType, line: int, column: int, source_file: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_file = source_file


class Expression:
    """Base expression node."""
    def __init__(self, node_type: NodeType, line: int, column: int, source_file: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_file = source_file


class VariableDeclaration(Statement):
    """Variable declaration statement."""
    def __init__(self, name: str, value: Optional[Expression], type_annotation: Optional['TypeAnnotation'], 
                 is_constant: bool, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.VARIABLE_DECLARATION, line, column, source_file)
        self.name = name
        self.value = value
        self.type_annotation = type_annotation
        self.is_constant = is_constant


class FunctionDeclaration(Statement):
    """Function declaration statement."""
    def __init__(self, name: str, parameters: List['Parameter'], return_type: Optional['TypeAnnotation'],
                 body: List[Statement], line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.FUNCTION_DECLARATION, line, column, source_file)
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body


class Parameter:
    """Function parameter."""
    def __init__(self, name: str, type_annotation: Optional['TypeAnnotation'] = None, 
                 default_value: Optional[Expression] = None):
        self.name = name
        self.type_annotation = type_annotation
        self.default_value = default_value


class IfStatement(Statement):
    """If statement with natural language syntax."""
    def __init__(self, condition: Expression, then_branch: List[Statement], 
                 else_branch: Optional[List[Statement]], line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.IF_STATEMENT, line, column, source_file)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class ForStatement(Statement):
    """For loop statement."""
    def __init__(self, iterator: Expression, variable: str, body: List[Statement],
                 line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.FOR_STATEMENT, line, column, source_file)
        self.iterator = iterator
        self.variable = variable
        self.body = body


class WhileStatement(Statement):
    """While loop statement."""
    def __init__(self, condition: Expression, body: List[Statement],
                 line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.WHILE_STATEMENT, line, column, source_file)
        self.condition = condition
        self.body = body


class ReturnStatement(Statement):
    """Return statement."""
    def __init__(self, value: Optional[Expression], line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.RETURN_STATEMENT, line, column, source_file)
        self.value = value


class BinaryExpression(Expression):
    """Binary expression."""
    def __init__(self, operator: str, left: Expression, right: Expression,
                 line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.BINARY_EXPRESSION, line, column, source_file)
        self.operator = operator
        self.left = left
        self.right = right


class CallExpression(Expression):
    """Function call expression."""
    def __init__(self, callee: Expression, arguments: List[Expression],
                 line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.CALL_EXPRESSION, line, column, source_file)
        self.callee = callee
        self.arguments = arguments


class Identifier(Expression):
    """Identifier expression."""
    def __init__(self, name: str, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.IDENTIFIER, line, column, source_file)
        self.name = name


class Literal(Expression):
    """Literal expression."""
    def __init__(self, value: Any, literal_type: str, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.LITERAL, line, column, source_file)
        self.value = value
        self.literal_type = literal_type


class TypeAnnotation(ASTNode):
    """Type annotation."""
    def __init__(self, type_name: str, line: int, column: int, source_file: Optional[str] = None,
                 generic_arguments: Optional[List['TypeAnnotation']] = None):
        super().__init__(NodeType.TYPE_ANNOTATION, line, column, source_file)
        self.type_name = type_name
        self.generic_arguments = generic_arguments


# AI-Specific AST Nodes

class ReasoningBlock(Statement):
    """AI reasoning block."""
    def __init__(self, content: str, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.REASONING_BLOCK, line, column, source_file)
        self.content = content


class ImplementationBlock(Statement):
    """AI implementation block."""
    def __init__(self, content: str, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.IMPLEMENTATION_BLOCK, line, column, source_file)
        self.content = content


class VerificationBlock(Statement):
    """AI verification block."""
    def __init__(self, content: str, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.VERIFICATION_BLOCK, line, column, source_file)
        self.content = content


class LLMCommunication(Statement):
    """LLM communication statement."""
    def __init__(self, target: str, context: str, task: str,
                 line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.LLM_COMMUNICATION, line, column, source_file)
        self.target = target
        self.context = context
        self.task = task


class RunaParser:
    """
    Recursive descent parser for Runa programming language.
    
    Features:
    - Comprehensive AST node hierarchy (30+ node types)
    - Error recovery and source position tracking
    - Natural language-like syntax parsing
    - AI-specific constructs support
    - Performance optimized for <100ms compilation target
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors: List[ParserError] = []
    
    def parse(self) -> Program:
        """
        Parse tokens into an AST.
        
        Returns:
            Program AST node
            
        Raises:
            ParserError: For parsing errors with detailed context
        """
        statements = []
        
        while not self.is_at_end():
            try:
                statement = self.parse_statement()
                if statement:
                    statements.append(statement)
            except ParserError as e:
                self.errors.append(e)
                self.synchronize()  # Error recovery
        
        if self.errors:
            raise ParserError(f"Parsing failed with {len(self.errors)} errors", self.peek())
        
        return Program(1, 1, statements=statements)
    
    def parse_statement(self) -> Optional[Statement]:
        """Parse a statement."""
        if self.match(TokenType.LET):
            return self.parse_variable_declaration()
        elif self.match(TokenType.DEFINE):
            return self.parse_define_statement()
        elif self.match(TokenType.SET):
            return self.parse_set_statement()
        elif self.match(TokenType.PROCESS):
            return self.parse_function_declaration()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.REASONING):
            return self.parse_reasoning_block()
        elif self.match(TokenType.IMPLEMENTATION):
            return self.parse_implementation_block()
        elif self.match(TokenType.VERIFY):
            return self.parse_verification_block()
        elif self.match(TokenType.SEND):
            return self.parse_llm_communication()
        else:
            # Try to parse as expression statement
            expr = self.parse_expression()
            if expr:
                return ExpressionStatement(expr, expr.line, expr.column, expr.source_file)
        
        return None
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration: 'Let name be value' or 'Let name as Type be value'."""
        line, column = self.peek().line, self.peek().column
        
        # Parse identifier
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        # Check for type annotation
        type_annotation = None
        if self.match(TokenType.AS):
            type_annotation = self.parse_type_annotation()
        
        # Expect 'be' or 'to'
        if not self.match(TokenType.BE, TokenType.TO):
            self.error("Expected 'be' or 'to' after variable name")
        
        # Parse value
        value = None
        if not self.check(TokenType.NEWLINE):
            value = self.parse_expression()
        
        return VariableDeclaration(name, value, type_annotation, False, line, column, value.source_file if value else None)
    
    def parse_define_statement(self) -> VariableDeclaration:
        """Parse define statement: 'Define name as Type containing value'."""
        line, column = self.peek().line, self.peek().column
        
        # Parse identifier
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        # Expect 'as'
        self.consume(TokenType.AS, "Expected 'as' after variable name")
        
        # Parse type
        type_annotation = self.parse_type_annotation()
        
        # Expect 'containing'
        self.consume(TokenType.CONTAINING, "Expected 'containing' after type")
        
        # Parse value
        value = self.parse_expression()
        
        return VariableDeclaration(name, value, type_annotation, True, line, column, value.source_file if value else None)
    
    def parse_set_statement(self) -> VariableDeclaration:
        """Parse set statement: 'Set name to value'."""
        line, column = self.peek().line, self.peek().column
        
        # Parse identifier
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        # Expect 'to'
        self.consume(TokenType.TO, "Expected 'to' after variable name")
        
        # Parse value
        value = self.parse_expression()
        
        return VariableDeclaration(name, value, None, False, line, column, value.source_file if value else None)
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration: 'Process called name that takes params: body'."""
        line, column = self.peek().line, self.peek().column
        
        # Expect 'called'
        self.consume(TokenType.CALLED, "Expected 'called' after 'Process'")
        
        # Parse function name
        name_token = self.consume(TokenType.STRING, "Expected function name in quotes")
        name = name_token.value.strip('"')
        
        # Expect 'that takes'
        self.consume(TokenType.THAT, "Expected 'that' after function name")
        self.consume(TokenType.TAKES, "Expected 'takes' after 'that'")
        
        # Parse parameters
        parameters = self.parse_parameters()
        
        # Expect colon
        self.consume(TokenType.COLON, "Expected ':' after parameters")
        
        # Parse function body
        body = self.parse_block()
        
        return FunctionDeclaration(name, parameters, None, body, line, column)
    
    def parse_parameters(self) -> List[Parameter]:
        """Parse function parameters."""
        parameters = []
        
        if self.check(TokenType.IDENTIFIER):
            while True:
                param_name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
                
                # Check for type annotation
                type_annotation = None
                if self.match(TokenType.AS):
                    type_annotation = self.parse_type_annotation()
                
                parameters.append(Parameter(param_name, type_annotation))
                
                if not self.match(TokenType.AND):
                    break
        
        return parameters
    
    def parse_type_annotation(self) -> TypeAnnotation:
        """Parse type annotation."""
        line, column = self.peek().line, self.peek().column
        
        if self.check(TokenType.TYPE_IDENTIFIER):
            type_name = self.consume(TokenType.TYPE_IDENTIFIER, "Expected type name").value
        elif self.check(TokenType.IDENTIFIER):
            type_name = self.consume(TokenType.IDENTIFIER, "Expected type name").value
        else:
            self.error("Expected type name")
            return None
        
        # Check for generic arguments
        generic_arguments = None
        if self.match(TokenType.LEFT_BRACKET):
            generic_arguments = []
            while not self.check(TokenType.RIGHT_BRACKET):
                generic_arguments.append(self.parse_type_annotation())
                if not self.match(TokenType.COMMA):
                    break
            self.consume(TokenType.RIGHT_BRACKET, "Expected ']' after generic arguments")
        
        return TypeAnnotation(type_name, line, column, generic_arguments=generic_arguments)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if statement: 'If condition: then_branch Otherwise: else_branch'."""
        line, column = self.peek().line, self.peek().column
        
        # Parse condition
        condition = self.parse_expression()
        
        # Expect colon
        self.consume(TokenType.COLON, "Expected ':' after condition")
        
        # Parse then branch
        then_branch = self.parse_block()
        
        # Check for else branch
        else_branch = None
        if self.match(TokenType.OTHERWISE):
            self.consume(TokenType.COLON, "Expected ':' after 'Otherwise'")
            else_branch = self.parse_block()
        
        return IfStatement(condition, then_branch, else_branch, line, column)
    
    def parse_for_statement(self) -> ForStatement:
        """Parse for statement: 'For each item in collection: body'."""
        line, column = self.peek().line, self.peek().column
        
        # Expect 'each'
        self.consume(TokenType.EACH, "Expected 'each' after 'For'")
        
        # Parse variable name
        variable = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        
        # Expect 'in'
        self.consume(TokenType.IN, "Expected 'in' after variable name")
        
        # Parse collection
        iterator = self.parse_expression()
        
        # Expect colon
        self.consume(TokenType.COLON, "Expected ':' after collection")
        
        # Parse body
        body = self.parse_block()
        
        return ForStatement(iterator, variable, body, line, column)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse while statement: 'While condition: body'."""
        line, column = self.peek().line, self.peek().column
        
        # Parse condition
        condition = self.parse_expression()
        
        # Expect colon
        self.consume(TokenType.COLON, "Expected ':' after condition")
        
        # Parse body
        body = self.parse_block()
        
        return WhileStatement(condition, body, line, column)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse return statement: 'Return value'."""
        line, column = self.peek().line, self.peek().column
        
        value = None
        if not self.check(TokenType.NEWLINE):
            value = self.parse_expression()
        
        return ReturnStatement(value, line, column)
    
    def parse_reasoning_block(self) -> ReasoningBlock:
        """Parse reasoning block: '@Reasoning: content @End_Reasoning'."""
        line, column = self.peek().line, self.peek().column
        
        content = self.parse_block_content()
        
        # Expect end marker
        self.consume(TokenType.END_REASONING, "Expected '@End_Reasoning'")
        
        return ReasoningBlock(content, line, column)
    
    def parse_implementation_block(self) -> ImplementationBlock:
        """Parse implementation block: '@Implementation: content @End_Implementation'."""
        line, column = self.peek().line, self.peek().column
        
        content = self.parse_block_content()
        
        # Expect end marker
        self.consume(TokenType.END_IMPLEMENTATION, "Expected '@End_Implementation'")
        
        return ImplementationBlock(content, line, column)
    
    def parse_verification_block(self) -> VerificationBlock:
        """Parse verification block: '@Verify: content @End_Verify'."""
        line, column = self.peek().line, self.peek().column
        
        content = self.parse_block_content()
        
        # Expect end marker
        self.consume(TokenType.END_VERIFY, "Expected '@End_Verify'")
        
        return VerificationBlock(content, line, column)
    
    def parse_llm_communication(self) -> LLMCommunication:
        """Parse LLM communication: 'Send to target with context: task'."""
        line, column = self.peek().line, self.peek().column
        
        # Expect 'to'
        self.consume(TokenType.TO, "Expected 'to' after 'Send'")
        
        # Parse target
        target = self.consume(TokenType.STRING, "Expected target name").value.strip('"')
        
        # Expect 'with context'
        self.consume(TokenType.WITH, "Expected 'with' after target")
        self.consume(TokenType.CONTEXT, "Expected 'context' after 'with'")
        
        # Parse context
        context = self.consume(TokenType.STRING, "Expected context").value.strip('"')
        
        # Expect colon
        self.consume(TokenType.COLON, "Expected ':' after context")
        
        # Parse task
        task = self.consume(TokenType.STRING, "Expected task").value.strip('"')
        
        return LLMCommunication(target, context, task, line, column)
    
    def parse_expression(self) -> Expression:
        """Parse an expression."""
        return self.parse_assignment()
    
    def parse_assignment(self) -> Expression:
        """Parse assignment expression."""
        expr = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            equals = self.previous()
            value = self.parse_assignment()
            
            if isinstance(expr, Identifier):
                # This is a valid assignment target
                return BinaryExpression("=", expr, value, expr.line, expr.column, expr.source_file)
            else:
                self.error("Invalid assignment target")
        
        return expr
    
    def parse_logical_or(self) -> Expression:
        """Parse logical OR expression."""
        expr = self.parse_logical_and()
        
        while self.match(TokenType.LOGICAL_OR):
            operator = self.previous().value
            right = self.parse_logical_and()
            expr = BinaryExpression(operator, expr, right, expr.line, expr.column, expr.source_file)
        
        return expr
    
    def parse_logical_and(self) -> Expression:
        """Parse logical AND expression."""
        expr = self.parse_equality()
        
        while self.match(TokenType.LOGICAL_AND):
            operator = self.previous().value
            right = self.parse_equality()
            expr = BinaryExpression(operator, expr, right, expr.line, expr.column, expr.source_file)
        
        return expr
    
    def parse_equality(self) -> Expression:
        """Parse equality expressions."""
        expr = self.parse_comparison()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.previous().value
            right = self.parse_comparison()
            expr = BinaryExpression(operator, expr, right, expr.line, expr.column, expr.source_file)
        
        return expr
    
    def parse_comparison(self) -> Expression:
        """Parse comparison expressions."""
        expr = self.parse_term()
        
        while self.match(TokenType.LESS_THAN, TokenType.LESS_EQUALS, 
                        TokenType.GREATER_THAN, TokenType.GREATER_EQUALS):
            operator = self.previous().value
            right = self.parse_term()
            expr = BinaryExpression(operator, expr, right, expr.line, expr.column, expr.source_file)
        
        return expr
    
    def parse_term(self) -> Expression:
        """Parse addition and subtraction."""
        expr = self.parse_factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().value
            right = self.parse_factor()
            expr = BinaryExpression(operator, expr, right, expr.line, expr.column, expr.source_file)
        
        return expr
    
    def parse_factor(self) -> Expression:
        """Parse multiplication and division."""
        expr = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.previous().value
            right = self.parse_unary()
            expr = BinaryExpression(operator, expr, right, expr.line, expr.column, expr.source_file)
        
        return expr
    
    def parse_unary(self) -> Expression:
        """Parse unary expressions."""
        if self.match(TokenType.LOGICAL_NOT, TokenType.MINUS, TokenType.BITWISE_NOT):
            operator = self.previous().value
            right = self.parse_unary()
            return UnaryExpression(operator, right, right.line, right.column, right.source_file)
        
        return self.parse_call()
    
    def parse_call(self) -> Expression:
        """Parse function calls."""
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expected property name after '.'")
                expr = MemberExpression(expr, name.value, expr.line, expr.column, expr.source_file)
            else:
                break
        
        return expr
    
    def finish_call(self, callee: Expression) -> CallExpression:
        """Finish parsing a function call."""
        arguments = []
        
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(self.parse_expression())
                if not self.match(TokenType.COMMA):
                    break
        
        paren = self.consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments")
        return CallExpression(callee, arguments, callee.line, callee.column, callee.source_file)
    
    def parse_primary(self) -> Expression:
        """Parse primary expressions."""
        if self.match(TokenType.TRUE):
            return Literal(True, "boolean", self.previous().line, self.previous().column, self.previous().source_file)
        if self.match(TokenType.FALSE):
            return Literal(False, "boolean", self.previous().line, self.previous().column, self.previous().source_file)
        if self.match(TokenType.NULL):
            return Literal(None, "null", self.previous().line, self.previous().column, self.previous().source_file)
        
        if self.match(TokenType.INTEGER):
            value = int(self.previous().value)
            return Literal(value, "integer", self.previous().line, self.previous().column, self.previous().source_file)
        
        if self.match(TokenType.FLOAT):
            value = float(self.previous().value)
            return Literal(value, "float", self.previous().line, self.previous().column, self.previous().source_file)
        
        if self.match(TokenType.STRING):
            value = self.previous().value.strip('"')
            return Literal(value, "string", self.previous().line, self.previous().column, self.previous().source_file)
        
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().value, self.previous().line, self.previous().column, self.previous().source_file)
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        
        self.error("Expected expression")
        return None
    
    def parse_block(self) -> List[Statement]:
        """Parse a block of statements."""
        statements = []
        
        # Expect indentation
        self.consume(TokenType.INDENT, "Expected indentation")
        
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        
        # Expect dedentation
        if self.check(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_block_content(self) -> str:
        """Parse content of a block (for AI blocks)."""
        content = []
        
        # Expect indentation
        self.consume(TokenType.INDENT, "Expected indentation")
        
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            token = self.advance()
            content.append(token.value)
        
        # Expect dedentation
        if self.check(TokenType.DEDENT):
            self.advance()
        
        return " ".join(content)
    
    # Parser utility methods
    
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False
    
    def check(self, type_: TokenType) -> bool:
        """Check if current token is of given type."""
        if self.is_at_end():
            return False
        return self.peek().type == type_
    
    def advance(self) -> Token:
        """Advance to next token."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of tokens."""
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        """Get current token without advancing."""
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        """Get previous token."""
        return self.tokens[self.current - 1]
    
    def consume(self, type_: TokenType, message: str) -> Token:
        """Consume token of expected type or error."""
        if self.check(type_):
            return self.advance()
        
        self.error(message)
        return None
    
    def error(self, message: str):
        """Report parsing error."""
        raise ParserError(message, self.peek())
    
    def synchronize(self):
        """Error recovery: skip tokens until we find a statement boundary."""
        self.advance()
        
        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE:
                return
            
            if self.peek().type in [
                TokenType.LET, TokenType.DEFINE, TokenType.SET, TokenType.PROCESS,
                TokenType.IF, TokenType.FOR, TokenType.WHILE, TokenType.RETURN,
                TokenType.REASONING, TokenType.IMPLEMENTATION, TokenType.VERIFY
            ]:
                return
            
            self.advance()


# Additional AST node classes for completeness

class ExpressionStatement(Statement):
    """Expression statement."""
    def __init__(self, expression: Expression, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.EXPRESSION_STATEMENT, line, column, source_file)
        self.expression = expression


class UnaryExpression(Expression):
    """Unary expression."""
    def __init__(self, operator: str, operand: Expression, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.UNARY_EXPRESSION, line, column, source_file)
        self.operator = operator
        self.operand = operand


class MemberExpression(Expression):
    """Member access expression."""
    def __init__(self, object: Expression, property: str, line: int, column: int, source_file: Optional[str] = None):
        super().__init__(NodeType.MEMBER_EXPRESSION, line, column, source_file)
        self.object = object
        self.property = property 