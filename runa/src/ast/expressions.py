"""
Expression nodes for the Runa abstract syntax tree.

This module defines the AST nodes that represent expressions in the Runa language.
Expressions are constructs that evaluate to a value.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union, Set

from runa.src.ast import ASTNode, ASTVisitor, NodeType, SourceLocation, TypeAnnotation
from runa.src.ast.nodes import Expression, Block, Parameter


@dataclass
class Expression(ASTNode):
    """Base class for all expression nodes."""
    
    def __init__(self, node_type: NodeType, location: Optional[SourceLocation] = None):
        """Initialize a new Expression node."""
        super().__init__(node_type, location)


@dataclass
class Literal(Expression):
    """
    Base class for literal values (strings, numbers, booleans, null).
    
    Attributes:
        value: The literal value
    """
    
    value: Any
    
    def __init__(self, node_type: NodeType, value: Any, location: Optional[SourceLocation] = None):
        """
        Initialize a new Literal node.
        
        Args:
            node_type: The specific type of literal (STRING_LITERAL, etc.)
            value: The literal value
            location: The source location of the node (optional)
        """
        super().__init__(node_type, location)
        self.value = value
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_literal(self)


@dataclass
class StringLiteral(Literal):
    """
    Represents a string literal.
    
    Attributes:
        value: The string value
    """
    
    def __init__(self, value: str, location: Optional[SourceLocation] = None):
        """
        Initialize a new StringLiteral node.
        
        Args:
            value: The string value
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.STRING_LITERAL, value, location)


@dataclass
class NumberLiteral(Literal):
    """
    Represents a number literal.
    
    Attributes:
        value: The numeric value (int or float)
    """
    
    def __init__(self, value: Union[int, float], location: Optional[SourceLocation] = None):
        """
        Initialize a new NumberLiteral node.
        
        Args:
            value: The numeric value (int or float)
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.NUMBER_LITERAL, value, location)


@dataclass
class BooleanLiteral(Literal):
    """
    Represents a boolean literal.
    
    Attributes:
        value: The boolean value
    """
    
    def __init__(self, value: bool, location: Optional[SourceLocation] = None):
        """
        Initialize a new BooleanLiteral node.
        
        Args:
            value: The boolean value
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.BOOLEAN_LITERAL, value, location)


@dataclass
class NullLiteral(Literal):
    """Represents a null literal."""
    
    def __init__(self, location: Optional[SourceLocation] = None):
        """
        Initialize a new NullLiteral node.
        
        Args:
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.NULL_LITERAL, None, location)


@dataclass
class Identifier(Expression):
    """
    Represents an identifier (variable name).
    
    Attributes:
        name: The name of the identifier
    """
    
    name: str
    
    def __init__(self, name: str, location: Optional[SourceLocation] = None):
        """
        Initialize a new Identifier node.
        
        Args:
            name: The name of the identifier
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.IDENTIFIER, location)
        self.name = name
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_identifier(self)


@dataclass
class BinaryExpression(Expression):
    """
    Represents a binary expression (e.g., a + b, x is greater than y).
    
    Attributes:
        left: The left operand
        operator: The operator
        right: The right operand
    """
    
    left: Expression
    operator: str
    right: Expression
    
    def __init__(
        self, 
        left: Expression, 
        operator: str, 
        right: Expression, 
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new BinaryExpression node.
        
        Args:
            left: The left operand
            operator: The operator
            right: The right operand
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.BINARY_EXPRESSION, location)
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_binary_expression(self)


@dataclass
class FunctionCall(Expression):
    """
    Represents a function call.
    
    Attributes:
        function: The function being called (an identifier)
        arguments: The arguments to the function
        named_arguments: Named arguments (keyword arguments)
    """
    
    function: Identifier
    arguments: List[Expression] = field(default_factory=list)
    named_arguments: Dict[str, Expression] = field(default_factory=dict)
    
    def __init__(
        self, 
        function: Identifier, 
        arguments: Optional[List[Expression]] = None,
        named_arguments: Optional[Dict[str, Expression]] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new FunctionCall node.
        
        Args:
            function: The function being called (an identifier)
            arguments: The arguments to the function
            named_arguments: Named arguments (keyword arguments)
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.FUNCTION_CALL, location)
        self.function = function
        self.arguments = arguments or []
        self.named_arguments = named_arguments or {}
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_function_call(self)


@dataclass
class ListExpression(Expression):
    """
    Represents a list expression (e.g., [1, 2, 3]).
    
    Attributes:
        elements: The elements of the list
    """
    
    elements: List[Expression] = field(default_factory=list)
    
    def __init__(
        self, 
        elements: Optional[List[Expression]] = None, 
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ListExpression node.
        
        Args:
            elements: The elements of the list
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.LIST_EXPRESSION, location)
        self.elements = elements or []
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_list_expression(self)


@dataclass
class DictionaryExpression(Expression):
    """
    Represents a dictionary expression (e.g., {"key": value}).
    
    Attributes:
        entries: The key-value pairs in the dictionary
    """
    
    entries: Dict[Expression, Expression] = field(default_factory=dict)
    
    def __init__(
        self, 
        entries: Optional[Dict[Expression, Expression]] = None, 
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new DictionaryExpression node.
        
        Args:
            entries: The key-value pairs in the dictionary
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.DICTIONARY_EXPRESSION, location)
        self.entries = entries or {}
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_dictionary_expression(self)


@dataclass
class IndexAccess(Expression):
    """
    Represents an index access expression (e.g., array[index]).
    
    Attributes:
        object: The object being indexed
        index: The index expression
    """
    
    object: Expression
    index: Expression
    
    def __init__(
        self, 
        object: Expression, 
        index: Expression, 
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new IndexAccess node.
        
        Args:
            object: The object being indexed
            index: The index expression
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.INDEX_ACCESS, location)
        self.object = object
        self.index = index
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_index_access(self)


@dataclass
class MemberAccess(Expression):
    """
    Represents a member access expression (e.g., object.member).
    
    Attributes:
        object: The object being accessed
        member: The member being accessed
    """
    
    object: Expression
    member: Identifier
    
    def __init__(
        self, 
        object: Expression, 
        member: Identifier, 
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new MemberAccess node.
        
        Args:
            object: The object being accessed
            member: The member being accessed
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MEMBER_ACCESS, location)
        self.object = object
        self.member = member
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_member_access(self)


@dataclass
class FunctionExpression(Expression):
    """
    Represents an anonymous function expression (closure).
    
    Attributes:
        parameters: The function parameters
        body: The function body
        return_type: The optional return type
        captured_variables: The variables captured from the outer scope
    """
    
    parameters: List[Parameter]
    body: Block
    return_type: Optional[TypeAnnotation] = None
    captured_variables: Set[str] = field(default_factory=set)
    
    def __init__(
        self,
        parameters: List[Parameter],
        body: Block,
        return_type: Optional[TypeAnnotation] = None,
        captured_variables: Optional[Set[str]] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new FunctionExpression node.
        
        Args:
            parameters: The function parameters
            body: The function body
            return_type: The optional return type
            captured_variables: The variables captured from the outer scope
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.FUNCTION_EXPRESSION, location)
        self.parameters = parameters
        self.body = body
        self.return_type = return_type
        self.captured_variables = captured_variables or set()
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_function_expression(self) 