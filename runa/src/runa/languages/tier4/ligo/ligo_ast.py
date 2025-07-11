"""
LIGO AST definitions for the high-level smart contract language on Tezos.

This module provides comprehensive Abstract Syntax Tree node definitions for LIGO,
supporting both JsLIGO and CameLIGO syntax variants, smart contract features,
and Tezos blockchain operations.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod


class LigoSyntax(Enum):
    """LIGO syntax variants."""
    JSLIGO = "jsligo"      # TypeScript/JavaScript inspired
    CAMELIGO = "cameligo"  # OCaml inspired


class LigoType(Enum):
    """LIGO primitive types."""
    UNIT = "unit"
    INT = "int"
    NAT = "nat"
    STRING = "string"
    BYTES = "bytes"
    BOOL = "bool"
    TEZ = "tez"
    MUTEZ = "mutez"
    ADDRESS = "address"
    KEY = "key"
    KEY_HASH = "key_hash"
    SIGNATURE = "signature"
    TIMESTAMP = "timestamp"
    CHAIN_ID = "chain_id"
    OPERATION = "operation"
    CONTRACT = "contract"
    
    # Composite types
    LIST = "list"
    SET = "set"
    MAP = "map"
    BIG_MAP = "big_map"
    OPTION = "option"
    RECORD = "record"
    VARIANT = "variant"
    TUPLE = "tuple"
    FUNCTION = "function"


class LigoOperator(Enum):
    """LIGO operators."""
    # Arithmetic
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "**"
    
    # Comparison
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # String/List
    CONCATENATE = "@"
    CONS = "::"
    
    # Assignment
    ASSIGN = "="


class LigoBuiltin(Enum):
    """LIGO built-in functions and operations."""
    # Tezos operations
    GET_AMOUNT = "Tezos.get_amount"
    GET_BALANCE = "Tezos.get_balance"
    GET_NOW = "Tezos.get_now"
    GET_SENDER = "Tezos.get_sender"
    GET_SOURCE = "Tezos.get_source"
    GET_SELF_ADDRESS = "Tezos.get_self_address"
    GET_CHAIN_ID = "Tezos.get_chain_id"
    GET_LEVEL = "Tezos.get_level"
    TRANSFER = "Tezos.transaction"
    SET_DELEGATE = "Tezos.set_delegate"
    CREATE_CONTRACT = "Tezos.create_contract"
    IMPLICIT_ACCOUNT = "Tezos.implicit_account"
    
    # Crypto operations
    PACK = "Bytes.pack"
    UNPACK = "Bytes.unpack"
    BLAKE2B = "Crypto.blake2b"
    SHA256 = "Crypto.sha256"
    SHA512 = "Crypto.sha512"
    HASH_KEY = "Crypto.hash_key"
    CHECK_SIGNATURE = "Crypto.check_signature"
    
    # Map operations
    MAP_FIND = "Map.find"
    MAP_FIND_OPT = "Map.find_opt"
    MAP_UPDATE = "Map.update"
    MAP_ADD = "Map.add"
    MAP_REMOVE = "Map.remove"
    MAP_MEM = "Map.mem"
    MAP_SIZE = "Map.size"
    MAP_LITERAL = "Map.literal"
    
    # List operations
    LIST_SIZE = "List.size"
    LIST_HEAD = "List.head"
    LIST_TAIL = "List.tail"
    LIST_MAP = "List.map"
    LIST_FOLD = "List.fold"
    LIST_ITER = "List.iter"
    
    # Set operations
    SET_ADD = "Set.add"
    SET_REMOVE = "Set.remove"
    SET_MEM = "Set.mem"
    SET_SIZE = "Set.size"
    SET_UPDATE = "Set.update"
    
    # Option operations
    OPTION_UNOPT = "Option.unopt"
    OPTION_IS_NONE = "Option.is_none"
    OPTION_IS_SOME = "Option.is_some"
    
    # Utility
    FAILWITH = "failwith"
    ASSERT = "assert"
    ABS = "abs"


class LigoNode(ABC):
    """Base class for all LIGO AST nodes."""
    
    def __init__(self, position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        self.position = position
        self.syntax = syntax or LigoSyntax.JSLIGO
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"


class LigoType_Node(LigoNode):
    """Represents a LIGO type."""
    
    def __init__(self, type_name: LigoType, args: Optional[List['LigoType_Node']] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.type_name = type_name
        self.args = args or []
    
    def accept(self, visitor):
        return visitor.visit_ligo_type(self)
    
    def __repr__(self):
        if self.args:
            args_str = ", ".join(str(arg) for arg in self.args)
            return f"{self.type_name.value}<{args_str}>"
        return self.type_name.value


class LigoLiteral(LigoNode):
    """Represents a LIGO literal value."""
    
    def __init__(self, value: Any, type_hint: Optional[LigoType] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.value = value
        self.type_hint = type_hint
    
    def accept(self, visitor):
        return visitor.visit_ligo_literal(self)
    
    def __repr__(self):
        return f"LigoLiteral({self.value})"


class LigoIdentifier(LigoNode):
    """Represents a LIGO identifier/variable reference."""
    
    def __init__(self, name: str, position: Optional[tuple] = None, 
                 syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_ligo_identifier(self)
    
    def __repr__(self):
        return f"LigoIdentifier({self.name})"


class LigoBinaryOperation(LigoNode):
    """Represents a LIGO binary operation."""
    
    def __init__(self, left: 'LigoExpression', operator: LigoOperator, 
                 right: 'LigoExpression', position: Optional[tuple] = None,
                 syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_ligo_binary_operation(self)


class LigoUnaryOperation(LigoNode):
    """Represents a LIGO unary operation."""
    
    def __init__(self, operator: LigoOperator, operand: 'LigoExpression',
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.operator = operator
        self.operand = operand
    
    def accept(self, visitor):
        return visitor.visit_ligo_unary_operation(self)


class LigoFunctionCall(LigoNode):
    """Represents a LIGO function call."""
    
    def __init__(self, function: 'LigoExpression', arguments: List['LigoExpression'],
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.function = function
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visit_ligo_function_call(self)


class LigoBuiltinCall(LigoNode):
    """Represents a LIGO built-in function call."""
    
    def __init__(self, builtin: LigoBuiltin, arguments: List['LigoExpression'],
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.builtin = builtin
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visit_ligo_builtin_call(self)


class LigoRecordAccess(LigoNode):
    """Represents record field access."""
    
    def __init__(self, record: 'LigoExpression', field: str,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.record = record
        self.field = field
    
    def accept(self, visitor):
        return visitor.visit_ligo_record_access(self)


class LigoTupleAccess(LigoNode):
    """Represents tuple element access."""
    
    def __init__(self, tuple_expr: 'LigoExpression', index: int,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.tuple_expr = tuple_expr
        self.index = index
    
    def accept(self, visitor):
        return visitor.visit_ligo_tuple_access(self)


class LigoListExpression(LigoNode):
    """Represents a LIGO list literal."""
    
    def __init__(self, elements: List['LigoExpression'], 
                 element_type: Optional[LigoType_Node] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.elements = elements
        self.element_type = element_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_list_expression(self)


class LigoSetExpression(LigoNode):
    """Represents a LIGO set literal."""
    
    def __init__(self, elements: List['LigoExpression'],
                 element_type: Optional[LigoType_Node] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.elements = elements
        self.element_type = element_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_set_expression(self)


class LigoMapEntry(LigoNode):
    """Represents a map entry (key-value pair)."""
    
    def __init__(self, key: 'LigoExpression', value: 'LigoExpression',
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.key = key
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_ligo_map_entry(self)


class LigoMapExpression(LigoNode):
    """Represents a LIGO map literal."""
    
    def __init__(self, entries: List[LigoMapEntry],
                 key_type: Optional[LigoType_Node] = None,
                 value_type: Optional[LigoType_Node] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.entries = entries
        self.key_type = key_type
        self.value_type = value_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_map_expression(self)


class LigoRecordField(LigoNode):
    """Represents a record field."""
    
    def __init__(self, name: str, value: 'LigoExpression',
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_ligo_record_field(self)


class LigoRecordExpression(LigoNode):
    """Represents a LIGO record literal."""
    
    def __init__(self, fields: List[LigoRecordField],
                 record_type: Optional[LigoType_Node] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.fields = fields
        self.record_type = record_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_record_expression(self)


class LigoTupleExpression(LigoNode):
    """Represents a LIGO tuple literal."""
    
    def __init__(self, elements: List['LigoExpression'],
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.elements = elements
    
    def accept(self, visitor):
        return visitor.visit_ligo_tuple_expression(self)


class LigoVariantExpression(LigoNode):
    """Represents a LIGO variant constructor."""
    
    def __init__(self, constructor: str, argument: Optional['LigoExpression'] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.constructor = constructor
        self.argument = argument
    
    def accept(self, visitor):
        return visitor.visit_ligo_variant_expression(self)


class LigoConditionalExpression(LigoNode):
    """Represents a LIGO conditional expression (ternary)."""
    
    def __init__(self, condition: 'LigoExpression', then_expr: 'LigoExpression',
                 else_expr: 'LigoExpression', position: Optional[tuple] = None,
                 syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr
    
    def accept(self, visitor):
        return visitor.visit_ligo_conditional_expression(self)


class LigoMatchPattern(LigoNode):
    """Represents a pattern in match expression."""
    
    def __init__(self, pattern: Union[str, 'LigoExpression'], 
                 variables: Optional[List[str]] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.pattern = pattern
        self.variables = variables or []
    
    def accept(self, visitor):
        return visitor.visit_ligo_match_pattern(self)


class LigoMatchCase(LigoNode):
    """Represents a case in match expression."""
    
    def __init__(self, pattern: LigoMatchPattern, expression: 'LigoExpression',
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.pattern = pattern
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_ligo_match_case(self)


class LigoMatchExpression(LigoNode):
    """Represents a LIGO match expression (pattern matching)."""
    
    def __init__(self, expression: 'LigoExpression', cases: List[LigoMatchCase],
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.expression = expression
        self.cases = cases
    
    def accept(self, visitor):
        return visitor.visit_ligo_match_expression(self)


class LigoLambdaExpression(LigoNode):
    """Represents a LIGO lambda function."""
    
    def __init__(self, parameters: List[str], body: 'LigoExpression',
                 param_types: Optional[List[LigoType_Node]] = None,
                 return_type: Optional[LigoType_Node] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.parameters = parameters
        self.body = body
        self.param_types = param_types or []
        self.return_type = return_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_lambda_expression(self)


# Statement nodes
class LigoParameter(LigoNode):
    """Represents a function parameter."""
    
    def __init__(self, name: str, param_type: LigoType_Node,
                 default_value: Optional['LigoExpression'] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.param_type = param_type
        self.default_value = default_value
    
    def accept(self, visitor):
        return visitor.visit_ligo_parameter(self)


class LigoTypeDeclaration(LigoNode):
    """Represents a LIGO type declaration."""
    
    def __init__(self, name: str, type_def: LigoType_Node, exported: bool = False,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.type_def = type_def
        self.exported = exported
    
    def accept(self, visitor):
        return visitor.visit_ligo_type_declaration(self)


class LigoRecordTypeField(LigoNode):
    """Represents a field in a record type."""
    
    def __init__(self, name: str, field_type: LigoType_Node,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.field_type = field_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_record_type_field(self)


class LigoRecordTypeDeclaration(LigoNode):
    """Represents a LIGO record type declaration."""
    
    def __init__(self, name: str, fields: List[LigoRecordTypeField], exported: bool = False,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.fields = fields
        self.exported = exported
    
    def accept(self, visitor):
        return visitor.visit_ligo_record_type_declaration(self)


class LigoVariantConstructor(LigoNode):
    """Represents a variant constructor."""
    
    def __init__(self, name: str, argument_type: Optional[LigoType_Node] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.argument_type = argument_type
    
    def accept(self, visitor):
        return visitor.visit_ligo_variant_constructor(self)


class LigoVariantTypeDeclaration(LigoNode):
    """Represents a LIGO variant type declaration."""
    
    def __init__(self, name: str, constructors: List[LigoVariantConstructor], 
                 exported: bool = False, position: Optional[tuple] = None, 
                 syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.constructors = constructors
        self.exported = exported
    
    def accept(self, visitor):
        return visitor.visit_ligo_variant_type_declaration(self)


class LigoVariableDeclaration(LigoNode):
    """Represents a LIGO variable declaration."""
    
    def __init__(self, name: str, var_type: Optional[LigoType_Node], 
                 initializer: Optional['LigoExpression'], mutable: bool = False,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.var_type = var_type
        self.initializer = initializer
        self.mutable = mutable
    
    def accept(self, visitor):
        return visitor.visit_ligo_variable_declaration(self)


class LigoFunctionDeclaration(LigoNode):
    """Represents a LIGO function declaration."""
    
    def __init__(self, name: str, parameters: List[LigoParameter], 
                 return_type: Optional[LigoType_Node], body: 'LigoStatement',
                 is_entry: bool = False, exported: bool = False,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.is_entry = is_entry
        self.exported = exported
    
    def accept(self, visitor):
        return visitor.visit_ligo_function_declaration(self)


class LigoExpressionStatement(LigoNode):
    """Represents an expression used as a statement."""
    
    def __init__(self, expression: 'LigoExpression',
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_ligo_expression_statement(self)


class LigoReturnStatement(LigoNode):
    """Represents a LIGO return statement."""
    
    def __init__(self, expression: Optional['LigoExpression'] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_ligo_return_statement(self)


class LigoBlockStatement(LigoNode):
    """Represents a LIGO block statement."""
    
    def __init__(self, statements: List['LigoStatement'],
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_ligo_block_statement(self)


class LigoIfStatement(LigoNode):
    """Represents a LIGO if statement."""
    
    def __init__(self, condition: 'LigoExpression', then_statement: 'LigoStatement',
                 else_statement: Optional['LigoStatement'] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement
    
    def accept(self, visitor):
        return visitor.visit_ligo_if_statement(self)


class LigoNamespace(LigoNode):
    """Represents a LIGO namespace/module."""
    
    def __init__(self, name: str, declarations: List['LigoDeclaration'],
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.name = name
        self.declarations = declarations
    
    def accept(self, visitor):
        return visitor.visit_ligo_namespace(self)


class LigoImport(LigoNode):
    """Represents a LIGO import statement."""
    
    def __init__(self, path: str, alias: Optional[str] = None,
                 position: Optional[tuple] = None, syntax: Optional[LigoSyntax] = None):
        super().__init__(position, syntax)
        self.path = path
        self.alias = alias
    
    def accept(self, visitor):
        return visitor.visit_ligo_import(self)


class LigoModule(LigoNode):
    """Represents a complete LIGO module/file."""
    
    def __init__(self, imports: List[LigoImport], declarations: List['LigoDeclaration'],
                 syntax: LigoSyntax = LigoSyntax.JSLIGO,
                 position: Optional[tuple] = None):
        super().__init__(position, syntax)
        self.imports = imports
        self.declarations = declarations
    
    def accept(self, visitor):
        return visitor.visit_ligo_module(self)
    
    def __repr__(self):
        return f"LigoModule({self.syntax.value}, {len(self.declarations)} declarations)"


# Visitor interface for traversing LIGO AST
class LigoVisitor(ABC):
    """Abstract visitor for LIGO AST nodes."""
    
    @abstractmethod
    def visit_ligo_type(self, node: LigoType_Node): pass
    
    @abstractmethod
    def visit_ligo_literal(self, node: LigoLiteral): pass
    
    @abstractmethod
    def visit_ligo_identifier(self, node: LigoIdentifier): pass
    
    @abstractmethod
    def visit_ligo_binary_operation(self, node: LigoBinaryOperation): pass
    
    @abstractmethod
    def visit_ligo_unary_operation(self, node: LigoUnaryOperation): pass
    
    @abstractmethod
    def visit_ligo_function_call(self, node: LigoFunctionCall): pass
    
    @abstractmethod
    def visit_ligo_builtin_call(self, node: LigoBuiltinCall): pass
    
    @abstractmethod
    def visit_ligo_record_access(self, node: LigoRecordAccess): pass
    
    @abstractmethod
    def visit_ligo_tuple_access(self, node: LigoTupleAccess): pass
    
    @abstractmethod
    def visit_ligo_list_expression(self, node: LigoListExpression): pass
    
    @abstractmethod
    def visit_ligo_set_expression(self, node: LigoSetExpression): pass
    
    @abstractmethod
    def visit_ligo_map_entry(self, node: LigoMapEntry): pass
    
    @abstractmethod
    def visit_ligo_map_expression(self, node: LigoMapExpression): pass
    
    @abstractmethod
    def visit_ligo_record_field(self, node: LigoRecordField): pass
    
    @abstractmethod
    def visit_ligo_record_expression(self, node: LigoRecordExpression): pass
    
    @abstractmethod
    def visit_ligo_tuple_expression(self, node: LigoTupleExpression): pass
    
    @abstractmethod
    def visit_ligo_variant_expression(self, node: LigoVariantExpression): pass
    
    @abstractmethod
    def visit_ligo_conditional_expression(self, node: LigoConditionalExpression): pass
    
    @abstractmethod
    def visit_ligo_match_pattern(self, node: LigoMatchPattern): pass
    
    @abstractmethod
    def visit_ligo_match_case(self, node: LigoMatchCase): pass
    
    @abstractmethod
    def visit_ligo_match_expression(self, node: LigoMatchExpression): pass
    
    @abstractmethod
    def visit_ligo_lambda_expression(self, node: LigoLambdaExpression): pass
    
    @abstractmethod
    def visit_ligo_parameter(self, node: LigoParameter): pass
    
    @abstractmethod
    def visit_ligo_type_declaration(self, node: LigoTypeDeclaration): pass
    
    @abstractmethod
    def visit_ligo_record_type_field(self, node: LigoRecordTypeField): pass
    
    @abstractmethod
    def visit_ligo_record_type_declaration(self, node: LigoRecordTypeDeclaration): pass
    
    @abstractmethod
    def visit_ligo_variant_constructor(self, node: LigoVariantConstructor): pass
    
    @abstractmethod
    def visit_ligo_variant_type_declaration(self, node: LigoVariantTypeDeclaration): pass
    
    @abstractmethod
    def visit_ligo_variable_declaration(self, node: LigoVariableDeclaration): pass
    
    @abstractmethod
    def visit_ligo_function_declaration(self, node: LigoFunctionDeclaration): pass
    
    @abstractmethod
    def visit_ligo_expression_statement(self, node: LigoExpressionStatement): pass
    
    @abstractmethod
    def visit_ligo_return_statement(self, node: LigoReturnStatement): pass
    
    @abstractmethod
    def visit_ligo_block_statement(self, node: LigoBlockStatement): pass
    
    @abstractmethod
    def visit_ligo_if_statement(self, node: LigoIfStatement): pass
    
    @abstractmethod
    def visit_ligo_namespace(self, node: LigoNamespace): pass
    
    @abstractmethod
    def visit_ligo_import(self, node: LigoImport): pass
    
    @abstractmethod
    def visit_ligo_module(self, node: LigoModule): pass


# Type aliases for convenience
LigoExpression = Union[
    LigoLiteral, LigoIdentifier, LigoBinaryOperation, LigoUnaryOperation,
    LigoFunctionCall, LigoBuiltinCall, LigoRecordAccess, LigoTupleAccess,
    LigoListExpression, LigoSetExpression, LigoMapExpression, LigoRecordExpression,
    LigoTupleExpression, LigoVariantExpression, LigoConditionalExpression,
    LigoMatchExpression, LigoLambdaExpression
]

LigoStatement = Union[
    LigoExpressionStatement, LigoReturnStatement, LigoBlockStatement, LigoIfStatement
]

LigoDeclaration = Union[
    LigoTypeDeclaration, LigoRecordTypeDeclaration, LigoVariantTypeDeclaration,
    LigoVariableDeclaration, LigoFunctionDeclaration, LigoNamespace
]

LigoASTNode = Union[LigoExpression, LigoStatement, LigoDeclaration, LigoModule] 