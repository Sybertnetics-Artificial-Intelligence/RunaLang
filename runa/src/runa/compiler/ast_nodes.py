"""
Runa AST Nodes - Natural Language Syntax Representation
======================================================

Represents Runa's natural language syntax as AST nodes:
- RunaDeclaration: "Let user name be \"Alex\""
- RunaAssignment: "Set user name to user name followed by \" Smith\""
- RunaFunctionCall: "Calculate Area with width as 5 and height as 10"
- RunaConditional: "If user age is greater than 21:"
- RunaLoop: "For each color in colors:"
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .ast_base import ASTNode, Statement, Expression, NodeType

# ============================================================================
# RUNA STATEMENT AST NODES
# ============================================================================

@dataclass
class RunaDeclaration(Statement):
    """AST node for Runa variable declarations."""
    variable_name: str
    type_annotation: Optional[str] = None  # Natural language type like "String"
    expression: str = ""  # Natural language expression like "width multiplied by height"
    inferred_type: Optional[str] = None
    
    def __init__(self, variable_name: str, expression: str, type_annotation: Optional[str] = None,
                 inferred_type: Optional[str] = None, line: int = 0, column: int = 0, 
                 source_file: Optional[str] = None):
        super().__init__(NodeType.VARIABLE_DECLARATION, line, column, source_file)
        self.variable_name = variable_name
        self.expression = expression
        self.type_annotation = type_annotation
        self.inferred_type = inferred_type
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if self.type_annotation:
            return f"Let {self.variable_name} ({self.type_annotation}) be {self.expression}"
        else:
            return f"Let {self.variable_name} be {self.expression}"


@dataclass
class RunaAssignment(Statement):
    """AST node for Runa assignments."""
    variable_name: str
    expression: str  # Natural language expression
    inferred_type: Optional[str] = None
    
    def __init__(self, variable_name: str, expression: str, inferred_type: Optional[str] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.ASSIGNMENT, line, column, source_file)
        self.variable_name = variable_name
        self.expression = expression
        self.inferred_type = inferred_type
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"Set {self.variable_name} to {self.expression}"


@dataclass
class RunaFunctionDeclaration(Statement):
    """AST node for Runa function declarations."""
    function_name: str
    parameters: List[str] = None  # Natural language parameter names
    return_type: Optional[str] = None  # Natural language return type
    body: List[str] = None  # Natural language body statements
    
    def __init__(self, function_name: str, parameters: Optional[List[str]] = None,
                 return_type: Optional[str] = None, body: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.FUNCTION_DECLARATION, line, column, source_file)
        self.function_name = function_name
        self.parameters = parameters or []
        self.return_type = return_type
        self.body = body or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        param_str = " and ".join(self.parameters) if self.parameters else "nothing"
        return_str = f" returns {self.return_type}" if self.return_type else ""
        return f"Process called \"{self.function_name}\" that takes {param_str}{return_str}:"


@dataclass
class RunaFunctionCall(Expression):
    """AST node for Runa function calls."""
    function_name: str
    arguments: Dict[str, str] = None  # Named arguments like {"width": "5", "height": "10"}
    
    def __init__(self, function_name: str, arguments: Optional[Dict[str, str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.FUNCTION_CALL, line, column, source_file)
        self.function_name = function_name
        self.arguments = arguments or {}
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if not self.arguments:
            return self.function_name
        
        arg_str = " and ".join([f"{key} as {value}" for key, value in self.arguments.items()])
        return f"{self.function_name} with {arg_str}"


@dataclass
class RunaConditional(Statement):
    """AST node for Runa conditional statements."""
    condition: str  # Natural language condition like "user age is greater than 21"
    then_body: List[str] = None  # Natural language statements
    else_body: List[str] = None  # Natural language statements
    elif_conditions: List[str] = None  # Natural language elif conditions
    elif_bodies: List[List[str]] = None  # Natural language elif bodies
    
    def __init__(self, condition: str, then_body: Optional[List[str]] = None,
                 else_body: Optional[List[str]] = None, elif_conditions: Optional[List[str]] = None,
                 elif_bodies: Optional[List[List[str]]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.CONDITIONAL, line, column, source_file)
        self.condition = condition
        self.then_body = then_body or []
        self.else_body = else_body or []
        self.elif_conditions = elif_conditions or []
        self.elif_bodies = elif_bodies or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        result = f"If {self.condition}:"
        
        # Add elif conditions
        for i, elif_condition in enumerate(self.elif_conditions):
            result += f"\nOtherwise if {elif_condition}:"
        
        # Add else
        if self.else_body:
            result += "\nOtherwise:"
        
        return result


@dataclass
class RunaLoop(Statement):
    """AST node for Runa for-each loops."""
    variable_name: str
    collection_expression: str  # Natural language collection expression
    body: List[str] = None  # Natural language body statements
    
    def __init__(self, variable_name: str, collection_expression: str,
                 body: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.LOOP, line, column, source_file)
        self.variable_name = variable_name
        self.collection_expression = collection_expression
        self.body = body or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"For each {self.variable_name} in {self.collection_expression}:"


@dataclass
class RunaWhileLoop(Statement):
    """AST node for Runa while loops."""
    condition: str  # Natural language condition
    body: List[str] = None  # Natural language body statements
    
    def __init__(self, condition: str, body: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.WHILE_LOOP, line, column, source_file)
        self.condition = condition
        self.body = body or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"While {self.condition}:"


@dataclass
class RunaPatternMatching(Statement):
    """AST node for Runa pattern matching."""
    expression: str  # Natural language expression to match
    cases: List['RunaPatternCase'] = None  # Pattern matching cases
    
    def __init__(self, expression: str, cases: Optional[List['RunaPatternCase']] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.PATTERN_MATCHING, line, column, source_file)
        self.expression = expression
        self.cases = cases or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"Match {self.expression}:"


@dataclass
class RunaPatternCase(ASTNode):
    """AST node for Runa pattern matching cases."""
    pattern: str  # Natural language pattern like "admin" or "user"
    guard: Optional[str] = None  # Natural language guard condition
    body: List[str] = None  # Natural language body statements
    
    def __init__(self, pattern: str, body: List[str], guard: Optional[str] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.PATTERN_MATCHING, line, column, source_file)
        self.pattern = pattern
        self.guard = guard
        self.body = body or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        result = f"When {self.pattern}"
        if self.guard:
            result += f" If {self.guard}"
        result += ":"
        return result


@dataclass
class RunaTypeDefinition(Statement):
    """AST node for Runa type definitions."""
    type_name: str
    type_expression: str  # Natural language type expression
    type_parameters: List[str] = None  # Generic type parameters
    
    def __init__(self, type_name: str, type_expression: str,
                 type_parameters: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.TYPE_DECLARATION, line, column, source_file)
        self.type_name = type_name
        self.type_expression = type_expression
        self.type_parameters = type_parameters or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        param_str = f"[{', '.join(self.type_parameters)}]" if self.type_parameters else ""
        return f"Type {self.type_name}{param_str} is {self.type_expression}"


# ============================================================================
# RUNA EXPRESSION AST NODES
# ============================================================================

@dataclass
class RunaArithmeticExpression(Expression):
    """AST node for Runa arithmetic expressions."""
    left_operand: str  # Natural language left operand
    operator: str  # Natural language operator like "multiplied by", "plus", "minus"
    right_operand: str  # Natural language right operand
    
    def __init__(self, left_operand: str, operator: str, right_operand: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.BINARY_EXPRESSION, line, column, source_file)
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"{self.left_operand} {self.operator} {self.right_operand}"


@dataclass
class RunaComparisonExpression(Expression):
    """AST node for Runa comparison expressions."""
    left_operand: str  # Natural language left operand
    operator: str  # Natural language operator like "is greater than", "is equal to"
    right_operand: str  # Natural language right operand
    
    def __init__(self, left_operand: str, operator: str, right_operand: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.BINARY_EXPRESSION, line, column, source_file)
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"{self.left_operand} {self.operator} {self.right_operand}"


@dataclass
class RunaStringConcatenation(Expression):
    """AST node for Runa string concatenation."""
    left_operand: str  # Natural language left operand
    right_operand: str  # Natural language right operand
    
    def __init__(self, left_operand: str, right_operand: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.BINARY_EXPRESSION, line, column, source_file)
        self.left_operand = left_operand
        self.right_operand = right_operand
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"{self.left_operand} followed by {self.right_operand}"


@dataclass
class RunaCollectionOperation(Expression):
    """AST node for Runa collection operations."""
    operation: str  # Natural language operation like "length of", "at index"
    collection: str  # Natural language collection expression
    index: Optional[str] = None  # Natural language index expression
    
    def __init__(self, operation: str, collection: str, index: Optional[str] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.COLLECTION_OPERATION, line, column, source_file)
        self.operation = operation
        self.collection = collection
        self.index = index
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if self.index:
            return f"{self.collection} {self.operation} {self.index}"
        else:
            return f"{self.operation} {self.collection}"


@dataclass
class RunaAggregationExpression(Expression):
    """AST node for Runa aggregation expressions."""
    operation: str  # Natural language operation like "the sum of all"
    variable: str  # Variable name in aggregation
    collection: str  # Natural language collection expression
    
    def __init__(self, operation: str, variable: str, collection: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.AGGREGATION_EXPRESSION, line, column, source_file)
        self.operation = operation
        self.variable = variable
        self.collection = collection
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"{self.operation} {self.variable} in {self.collection}"


@dataclass
class RunaLiteral(Expression):
    """AST node for Runa literals."""
    value: str  # Natural language literal value
    literal_type: str  # Type of literal: "string", "integer", "float", "boolean"
    
    def __init__(self, value: str, literal_type: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.LITERAL, line, column, source_file)
        self.value = value
        self.literal_type = literal_type
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return self.value


@dataclass
class RunaVariableReference(Expression):
    """AST node for Runa variable references."""
    variable_name: str  # Natural language variable name
    
    def __init__(self, variable_name: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.VARIABLE_REFERENCE, line, column, source_file)
        self.variable_name = variable_name
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return self.variable_name


@dataclass
class RunaListExpression(Expression):
    """AST node for Runa list expressions."""
    elements: List[str] = None  # Natural language list elements
    
    def __init__(self, elements: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.LIST_EXPRESSION, line, column, source_file)
        self.elements = elements or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if not self.elements:
            return "list containing"
        return f"list containing {', '.join(self.elements)}"


@dataclass
class RunaDictionaryExpression(Expression):
    """AST node for Runa dictionary expressions."""
    key_value_pairs: Dict[str, str] = None  # Natural language key-value pairs
    
    def __init__(self, key_value_pairs: Optional[Dict[str, str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.DICTIONARY_EXPRESSION, line, column, source_file)
        self.key_value_pairs = key_value_pairs or {}
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if not self.key_value_pairs:
            return "dictionary with:"
        
        pairs = [f"{key} as {value}" for key, value in self.key_value_pairs.items()]
        return f"dictionary with:\n" + "\n".join(pairs)


# ============================================================================
# RUNA CONTROL FLOW AST NODES
# ============================================================================

@dataclass
class RunaReturnStatement(Statement):
    """AST node for Runa return statements."""
    expression: str  # Natural language return expression
    
    def __init__(self, expression: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.RETURN_STATEMENT, line, column, source_file)
        self.expression = expression
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"Return {self.expression}"


@dataclass
class RunaDisplayStatement(Statement):
    """AST node for Runa display statements."""
    expression: str  # Natural language expression to display
    message: Optional[str] = None  # Optional natural language message
    
    def __init__(self, expression: str, message: Optional[str] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.DISPLAY_STATEMENT, line, column, source_file)
        self.expression = expression
        self.message = message
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if self.message:
            return f"Display {self.expression} with message {self.message}"
        else:
            return f"Display {self.expression}"


@dataclass
class RunaTryCatchStatement(Statement):
    """AST node for Runa try-catch statements."""
    try_body: List[str] = None  # Natural language try body
    catch_variable: str = ""  # Natural language catch variable name
    catch_body: List[str] = None  # Natural language catch body
    
    def __init__(self, try_body: Optional[List[str]] = None, catch_variable: str = "",
                 catch_body: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.TRY_CATCH_STATEMENT, line, column, source_file)
        self.try_body = try_body or []
        self.catch_variable = catch_variable
        self.catch_body = catch_body or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"Try:\nCatch {self.catch_variable}:"


@dataclass
class RunaImportStatement(Statement):
    """AST node for Runa import statements."""
    module_name: str  # Natural language module name
    alias: Optional[str] = None  # Optional alias
    
    def __init__(self, module_name: str, alias: Optional[str] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.IMPORT_STATEMENT, line, column, source_file)
        self.module_name = module_name
        self.alias = alias
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        if self.alias:
            return f"Import module {self.module_name} as {self.alias}"
        else:
            return f"Import module {self.module_name}"


# ============================================================================
# RUNA BLOCK AST NODES
# ============================================================================

@dataclass
class RunaBlock(Statement):
    """AST node for Runa code blocks."""
    statements: List[str] = None  # Natural language statements
    
    def __init__(self, statements: Optional[List[str]] = None,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.BLOCK, line, column, source_file)
        self.statements = statements or []
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return "\n".join(self.statements)


@dataclass
class RunaComment(Statement):
    """AST node for Runa comments."""
    comment_text: str  # Natural language comment text
    
    def __init__(self, comment_text: str,
                 line: int = 0, column: int = 0, source_file: Optional[str] = None):
        super().__init__(NodeType.COMMENT_LINE, line, column, source_file)
        self.comment_text = comment_text
    
    def to_runa_syntax(self) -> str:
        """Convert back to Runa syntax."""
        return f"# {self.comment_text}" 