"""
Abstract Syntax Tree (AST) module for the Runa programming language.

This module defines the Abstract Syntax Tree (AST) nodes that represent the
structure of Runa programs after parsing. These nodes are used for semantic
analysis, type checking, and code generation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Any, Union

from runa.src.lexer.tokens import Token


class NodeType(Enum):
    """Enum representing the different types of AST nodes."""
    
    # Program structure
    PROGRAM = auto()
    
    # Statements
    STATEMENT = auto()
    DECLARATION = auto()
    ASSIGNMENT = auto()
    IF_STATEMENT = auto()
    LOOP_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    FUNCTION_DEFINITION = auto()
    RETURN_STATEMENT = auto()
    DISPLAY_STATEMENT = auto()
    BLOCK = auto()
    IMPORT_STATEMENT = auto()
    TRY_CATCH_STATEMENT = auto()
    
    # Expressions
    EXPRESSION = auto()
    LITERAL = auto()
    STRING_LITERAL = auto()
    NUMBER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    IDENTIFIER = auto()
    BINARY_EXPRESSION = auto()
    FUNCTION_CALL = auto()
    LIST_EXPRESSION = auto()
    DICTIONARY_EXPRESSION = auto()
    INDEX_ACCESS = auto()
    MEMBER_ACCESS = auto()
    
    # Types
    TYPE_ANNOTATION = auto()


@dataclass
class SourceLocation:
    """
    Represents a location in the source code.
    
    This class is used to track the location of AST nodes in the source code
    for error reporting and debugging.
    
    Attributes:
        line: The line number (1-indexed)
        column: The column number (1-indexed)
        file: The filename
    """
    
    line: int
    column: int
    file: str = "<unknown>"
    
    def __str__(self) -> str:
        """Return a string representation of the source location."""
        return f"{self.file}:{self.line}:{self.column}"


class ASTNode(ABC):
    """
    Base class for all AST nodes.
    
    All AST nodes inherit from this class, which provides common functionality
    for traversing the tree and tracking source locations.
    
    Attributes:
        node_type: The type of node
        location: The source location of the node
    """
    
    def __init__(self, node_type: NodeType, location: Optional[SourceLocation] = None):
        """
        Initialize a new AST node.
        
        Args:
            node_type: The type of node
            location: The source location of the node (optional)
        """
        self.node_type = node_type
        self.location = location
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """
        Accept a visitor to process this node.
        
        This method implements the Visitor pattern, allowing operations to be
        performed on the AST without modifying the node classes.
        
        Args:
            visitor: The visitor to accept
            
        Returns:
            The result of the visitor's visit method for this node
        """
        pass
    
    def __str__(self) -> str:
        """Return a string representation of the node."""
        return f"{self.node_type.name}"


class ASTVisitor(ABC):
    """
    Base class for AST visitors.
    
    Visitors are used to traverse the AST and perform operations on the nodes
    without modifying the node classes.
    """
    
    @abstractmethod
    def visit_program(self, node: 'Program') -> Any:
        """Visit a Program node."""
        pass
    
    @abstractmethod
    def visit_block(self, node: 'Block') -> Any:
        """Visit a Block node."""
        pass
    
    @abstractmethod
    def visit_declaration(self, node: 'Declaration') -> Any:
        """Visit a Declaration node."""
        pass
    
    @abstractmethod
    def visit_assignment(self, node: 'Assignment') -> Any:
        """Visit an Assignment node."""
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: 'IfStatement') -> Any:
        """Visit an IfStatement node."""
        pass
    
    @abstractmethod
    def visit_loop_statement(self, node: 'LoopStatement') -> Any:
        """Visit a LoopStatement node."""
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: 'WhileStatement') -> Any:
        """Visit a WhileStatement node."""
        pass
    
    @abstractmethod
    def visit_function_definition(self, node: 'FunctionDefinition') -> Any:
        """Visit a FunctionDefinition node."""
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: 'ReturnStatement') -> Any:
        """Visit a ReturnStatement node."""
        pass
    
    @abstractmethod
    def visit_display_statement(self, node: 'DisplayStatement') -> Any:
        """Visit a DisplayStatement node."""
        pass
    
    @abstractmethod
    def visit_import_statement(self, node: 'ImportStatement') -> Any:
        """Visit an ImportStatement node."""
        pass
    
    @abstractmethod
    def visit_try_catch_statement(self, node: 'TryCatchStatement') -> Any:
        """Visit a TryCatchStatement node."""
        pass
    
    @abstractmethod
    def visit_literal(self, node: 'Literal') -> Any:
        """Visit a Literal node."""
        pass
    
    @abstractmethod
    def visit_identifier(self, node: 'Identifier') -> Any:
        """Visit an Identifier node."""
        pass
    
    @abstractmethod
    def visit_binary_expression(self, node: 'BinaryExpression') -> Any:
        """Visit a BinaryExpression node."""
        pass
    
    @abstractmethod
    def visit_function_call(self, node: 'FunctionCall') -> Any:
        """Visit a FunctionCall node."""
        pass
    
    @abstractmethod
    def visit_list_expression(self, node: 'ListExpression') -> Any:
        """Visit a ListExpression node."""
        pass
    
    @abstractmethod
    def visit_dictionary_expression(self, node: 'DictionaryExpression') -> Any:
        """Visit a DictionaryExpression node."""
        pass
    
    @abstractmethod
    def visit_index_access(self, node: 'IndexAccess') -> Any:
        """Visit an IndexAccess node."""
        pass
    
    @abstractmethod
    def visit_member_access(self, node: 'MemberAccess') -> Any:
        """Visit a MemberAccess node."""
        pass
    
    @abstractmethod
    def visit_type_annotation(self, node: 'TypeAnnotation') -> Any:
        """Visit a TypeAnnotation node."""
        pass


# Program structure nodes

@dataclass
class Program(ASTNode):
    """
    Represents a Runa program.
    
    This is the root node of the AST for a Runa program.
    
    Attributes:
        statements: The list of top-level statements in the program
    """
    
    statements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, statements: List[ASTNode], location: Optional[SourceLocation] = None):
        """
        Initialize a new Program node.
        
        Args:
            statements: The list of top-level statements in the program
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.PROGRAM, location)
        self.statements = statements
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_program(self)


@dataclass
class Block(ASTNode):
    """
    Represents a block of statements.
    
    A block is a sequence of statements enclosed in indentation or braces.
    
    Attributes:
        statements: The list of statements in the block
    """
    
    statements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, statements: List[ASTNode], location: Optional[SourceLocation] = None):
        """
        Initialize a new Block node.
        
        Args:
            statements: The list of statements in the block
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.BLOCK, location)
        self.statements = statements
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_block(self)


# Type annotation node

@dataclass
class TypeAnnotation(ASTNode):
    """
    Represents a type annotation.
    
    Type annotations are used to specify the type of a variable or function.
    
    Attributes:
        type_name: The name of the type
    """
    
    type_name: str
    
    def __init__(self, type_name: str, location: Optional[SourceLocation] = None):
        """
        Initialize a new TypeAnnotation node.
        
        Args:
            type_name: The name of the type
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TYPE_ANNOTATION, location)
        self.type_name = type_name
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_type_annotation(self)


# Statement nodes

@dataclass
class Declaration(ASTNode):
    """
    Represents a variable declaration.
    
    A declaration introduces a new variable with an optional type and initial value.
    
    Attributes:
        name: The name of the variable
        type_annotation: The optional type annotation
        value: The initial value expression
    """
    
    name: str
    value: ASTNode
    type_annotation: Optional[TypeAnnotation] = None
    
    def __init__(
        self, 
        name: str, 
        value: ASTNode, 
        type_annotation: Optional[TypeAnnotation] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new Declaration node.
        
        Args:
            name: The name of the variable
            value: The initial value expression
            type_annotation: The optional type annotation
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.DECLARATION, location)
        self.name = name
        self.value = value
        self.type_annotation = type_annotation
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_declaration(self)


@dataclass
class Assignment(ASTNode):
    """
    Represents a variable assignment.
    
    An assignment updates the value of an existing variable.
    
    Attributes:
        name: The name of the variable
        value: The new value expression
    """
    
    name: str
    value: ASTNode
    
    def __init__(self, name: str, value: ASTNode, location: Optional[SourceLocation] = None):
        """
        Initialize a new Assignment node.
        
        Args:
            name: The name of the variable
            value: The new value expression
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.ASSIGNMENT, location)
        self.name = name
        self.value = value
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_assignment(self)


# This is just the foundation for the AST module. Additional node classes and
# functionality will be implemented in the AST node hierarchy files. 