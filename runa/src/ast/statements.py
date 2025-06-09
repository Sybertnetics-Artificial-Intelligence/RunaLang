"""
Statement nodes for the Runa abstract syntax tree.

This module defines the AST nodes that represent statements in the Runa language.
Statements are constructs that represent actions and control flow.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from abc import ABC, abstractmethod
from enum import Enum, auto

from runa.src.ast import ASTNode, ASTVisitor, NodeType, SourceLocation, TypeAnnotation
from runa.src.ast.expressions import Expression, Identifier


@dataclass
class Statement(ASTNode):
    """Base class for all statement nodes."""
    
    def __init__(self, node_type: NodeType, location: Optional[SourceLocation] = None):
        """Initialize a new Statement node."""
        super().__init__(node_type, location)


@dataclass
class IfStatement(Statement):
    """
    Represents an if statement.
    
    Attributes:
        condition: The condition expression
        then_branch: The statements to execute if the condition is true
        else_if_branches: List of (condition, statements) for else-if branches
        else_branch: The statements to execute if the condition is false
    """
    
    condition: Expression
    then_branch: 'Block'
    else_if_branches: List[tuple[Expression, 'Block']] = field(default_factory=list)
    else_branch: Optional['Block'] = None
    
    def __init__(
        self,
        condition: Expression,
        then_branch: 'Block',
        else_if_branches: Optional[List[tuple[Expression, 'Block']]] = None,
        else_branch: Optional['Block'] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new IfStatement node.
        
        Args:
            condition: The condition expression
            then_branch: The statements to execute if the condition is true
            else_if_branches: List of (condition, statements) for else-if branches
            else_branch: The statements to execute if the condition is false
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.IF_STATEMENT, location)
        self.condition = condition
        self.then_branch = then_branch
        self.else_if_branches = else_if_branches or []
        self.else_branch = else_branch
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_if_statement(self)


@dataclass
class LoopStatement(Statement):
    """
    Represents a for-each loop statement.
    
    Attributes:
        variable: The loop variable identifier
        iterable: The iterable expression
        body: The loop body
    """
    
    variable: Identifier
    iterable: Expression
    body: 'Block'
    
    def __init__(
        self,
        variable: Identifier,
        iterable: Expression,
        body: 'Block',
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new LoopStatement node.
        
        Args:
            variable: The loop variable identifier
            iterable: The iterable expression
            body: The loop body
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.LOOP_STATEMENT, location)
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_loop_statement(self)


@dataclass
class WhileStatement(Statement):
    """
    Represents a while loop statement.
    
    Attributes:
        condition: The loop condition
        body: The loop body
    """
    
    condition: Expression
    body: 'Block'
    
    def __init__(
        self,
        condition: Expression,
        body: 'Block',
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new WhileStatement node.
        
        Args:
            condition: The loop condition
            body: The loop body
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.WHILE_STATEMENT, location)
        self.condition = condition
        self.body = body
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_while_statement(self)


@dataclass
class Parameter:
    """
    Represents a function parameter.
    
    Attributes:
        name: The parameter name
        type_annotation: The optional type annotation
    """
    
    name: str
    type_annotation: Optional[TypeAnnotation] = None


@dataclass
class FunctionDefinition(Statement):
    """
    Represents a function definition.
    
    Attributes:
        name: The function name
        parameters: The function parameters
        body: The function body
        return_type: The optional return type
    """
    
    name: str
    parameters: List[Parameter]
    body: 'Block'
    return_type: Optional[TypeAnnotation] = None
    
    def __init__(
        self,
        name: str,
        parameters: List[Parameter],
        body: 'Block',
        return_type: Optional[TypeAnnotation] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new FunctionDefinition node.
        
        Args:
            name: The function name
            parameters: The function parameters
            body: The function body
            return_type: The optional return type
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.FUNCTION_DEFINITION, location)
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_function_definition(self)


@dataclass
class ReturnStatement(Statement):
    """
    Represents a return statement.
    
    Attributes:
        value: The return value expression
    """
    
    value: Expression
    
    def __init__(self, value: Expression, location: Optional[SourceLocation] = None):
        """
        Initialize a new ReturnStatement node.
        
        Args:
            value: The return value expression
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.RETURN_STATEMENT, location)
        self.value = value
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_return_statement(self)


@dataclass
class DisplayStatement(Statement):
    """
    Represents a display statement.
    
    Attributes:
        value: The value to display
        message: The optional message to display with the value
    """
    
    value: Expression
    message: Optional[Expression] = None
    
    def __init__(
        self,
        value: Expression,
        message: Optional[Expression] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new DisplayStatement node.
        
        Args:
            value: The value to display
            message: The optional message to display with the value
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.DISPLAY_STATEMENT, location)
        self.value = value
        self.message = message
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_display_statement(self)


@dataclass
class ImportStatement(Statement):
    """
    Represents an import statement.
    
    Attributes:
        module: The module to import
        items: The items to import from the module
    """
    
    module: str
    items: List[str] = field(default_factory=list)
    
    def __init__(
        self,
        module: str,
        items: Optional[List[str]] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ImportStatement node.
        
        Args:
            module: The module to import
            items: The items to import from the module
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.IMPORT_STATEMENT, location)
        self.module = module
        self.items = items or []
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_import_statement(self)


@dataclass
class ExportStatement(Statement):
    """
    Represents an export statement.
    
    Attributes:
        items: The items to export from the module
    """
    
    items: List[str] = field(default_factory=list)
    
    def __init__(
        self,
        items: Optional[List[str]] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ExportStatement node.
        
        Args:
            items: The items to export from the module
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.EXPORT_STATEMENT, location)
        self.items = items or []
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_export_statement(self)


@dataclass
class TryCatchStatement(Statement):
    """
    Represents a try-catch statement.
    
    Attributes:
        try_block: The try block
        error_variable: The error variable name
        catch_block: The catch block
    """
    
    try_block: 'Block'
    error_variable: str
    catch_block: 'Block'
    
    def __init__(
        self,
        try_block: 'Block',
        error_variable: str,
        catch_block: 'Block',
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new TryCatchStatement node.
        
        Args:
            try_block: The try block
            error_variable: The error variable name
            catch_block: The catch block
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRY_CATCH_STATEMENT, location)
        self.try_block = try_block
        self.error_variable = error_variable
        self.catch_block = catch_block
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_try_catch_statement(self)


@dataclass
class Pattern(ABC):
    """
    Base class for all pattern matching patterns.
    
    Attributes:
        type: The type of the pattern
        location: The source location of the node
    """
    
    type: NodeType
    location: Optional[SourceLocation] = None
    
    def __init__(self, type: NodeType, location: Optional[SourceLocation] = None):
        """
        Initialize a new Pattern node.
        
        Args:
            type: The type of the pattern
            location: The source location of the node (optional)
        """
        self.type = type
        self.location = location
    
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        pass


@dataclass
class LiteralPattern(Pattern):
    """
    Represents a literal pattern in a match statement.
    
    Attributes:
        value: The literal value to match against
    """
    
    value: Expression
    
    def __init__(
        self,
        value: Expression,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new LiteralPattern node.
        
        Args:
            value: The literal value to match against
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.LITERAL_PATTERN, location)
        self.value = value
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_literal_pattern(self)


@dataclass
class VariablePattern(Pattern):
    """
    Represents a variable binding pattern in a match statement.
    
    Attributes:
        name: The name of the variable to bind
    """
    
    name: str
    
    def __init__(
        self,
        name: str,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new VariablePattern node.
        
        Args:
            name: The name of the variable to bind
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.VARIABLE_PATTERN, location)
        self.name = name
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_variable_pattern(self)


@dataclass
class WildcardPattern(Pattern):
    """
    Represents a wildcard pattern (_) in a match statement.
    """
    
    def __init__(
        self,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new WildcardPattern node.
        
        Args:
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.WILDCARD_PATTERN, location)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_wildcard_pattern(self)


@dataclass
class ListPattern(Pattern):
    """
    Represents a list pattern in a match statement.
    
    Attributes:
        elements: The patterns for list elements
        rest_variable: The optional variable to bind the rest of the list
    """
    
    elements: List[Pattern]
    rest_variable: Optional[str] = None
    
    def __init__(
        self,
        elements: List[Pattern],
        rest_variable: Optional[str] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ListPattern node.
        
        Args:
            elements: The patterns for list elements
            rest_variable: The optional variable to bind the rest of the list
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.LIST_PATTERN, location)
        self.elements = elements
        self.rest_variable = rest_variable
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_list_pattern(self)


@dataclass
class DictionaryPattern(Pattern):
    """
    Represents a dictionary pattern in a match statement.
    
    Attributes:
        pairs: The key-pattern pairs to match
    """
    
    pairs: Dict[str, Pattern]
    
    def __init__(
        self,
        pairs: Dict[str, Pattern],
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new DictionaryPattern node.
        
        Args:
            pairs: The key-pattern pairs to match
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.DICTIONARY_PATTERN, location)
        self.pairs = pairs
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_dictionary_pattern(self)


@dataclass
class TypePattern(Pattern):
    """
    Represents a type pattern in a match statement.
    
    Attributes:
        type_name: The name of the type to match against
        variable: The optional variable to bind the value
    """
    
    type_name: str
    variable: Optional[str] = None
    
    def __init__(
        self,
        type_name: str,
        variable: Optional[str] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new TypePattern node.
        
        Args:
            type_name: The name of the type to match against
            variable: The optional variable to bind the value
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TYPE_PATTERN, location)
        self.type_name = type_name
        self.variable = variable
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_type_pattern(self)


@dataclass
class MatchCase:
    """
    Represents a case in a match statement.
    
    Attributes:
        pattern: The pattern to match against
        guard: The optional guard expression
        body: The body to execute if the pattern matches
    """
    
    pattern: Pattern
    body: Block
    guard: Optional[Expression] = None
    
    def __init__(
        self,
        pattern: Pattern,
        body: Block,
        guard: Optional[Expression] = None
    ):
        """
        Initialize a new MatchCase node.
        
        Args:
            pattern: The pattern to match against
            body: The body to execute if the pattern matches
            guard: The optional guard expression
        """
        self.pattern = pattern
        self.body = body
        self.guard = guard


@dataclass
class MatchStatement(Statement):
    """
    Represents a match statement.
    
    Attributes:
        expression: The expression to match against
        cases: The match cases
    """
    
    expression: Expression
    cases: List[MatchCase]
    
    def __init__(
        self,
        expression: Expression,
        cases: List[MatchCase],
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new MatchStatement node.
        
        Args:
            expression: The expression to match against
            cases: The match cases
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MATCH_STATEMENT, location)
        self.expression = expression
        self.cases = cases
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_match_statement(self)


# Import Block to resolve circular dependency
from runa.src.ast import Block 