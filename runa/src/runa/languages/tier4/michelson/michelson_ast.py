"""
Michelson AST definitions for the stack-based smart contract language on Tezos.

This module provides comprehensive Abstract Syntax Tree node definitions for Michelson,
covering stack operations, data types, instructions, and smart contract structures.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod


class MichelsonType(Enum):
    """Michelson primitive types."""
    UNIT = "unit"
    INT = "int"
    NAT = "nat"  
    STRING = "string"
    BYTES = "bytes"
    BOOL = "bool"
    MUTEZ = "mutez"
    TEZ = "tez"
    ADDRESS = "address"
    KEY = "key"
    KEY_HASH = "key_hash"
    SIGNATURE = "signature"
    TIMESTAMP = "timestamp"
    CHAIN_ID = "chain_id"
    OPERATION = "operation"
    CONTRACT = "contract"
    PAIR = "pair"
    OR = "or"
    OPTION = "option"
    LIST = "list"
    SET = "set"
    MAP = "map"
    BIG_MAP = "big_map"
    LAMBDA = "lambda"


class MichelsonInstruction(Enum):
    """Michelson stack instructions."""
    # Stack operations
    DROP = "DROP"
    DUP = "DUP"
    SWAP = "SWAP"
    DIG = "DIG"
    DUG = "DUG"
    PUSH = "PUSH"
    
    # Arithmetic operations
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    ABS = "ABS"
    NEG = "NEG"
    LSL = "LSL"
    LSR = "LSR"
    OR = "OR"
    AND = "AND"
    XOR = "XOR"
    NOT = "NOT"
    
    # Comparison operations
    COMPARE = "COMPARE"
    EQ = "EQ"
    NEQ = "NEQ"
    LT = "LT"
    GT = "GT"
    LE = "LE"
    GE = "GE"
    
    # Control structures
    IF = "IF"
    IF_NONE = "IF_NONE"
    IF_LEFT = "IF_LEFT"
    IF_CONS = "IF_CONS"
    LOOP = "LOOP"
    LOOP_LEFT = "LOOP_LEFT"
    ITER = "ITER"
    MAP = "MAP"
    
    # Data operations
    PAIR = "PAIR"
    UNPAIR = "UNPAIR"
    CAR = "CAR"
    CDR = "CDR"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    SOME = "SOME"
    NONE = "NONE"
    UNIT = "UNIT"
    
    # List operations
    CONS = "CONS"
    NIL = "NIL"
    SIZE = "SIZE"
    
    # Set operations
    EMPTY_SET = "EMPTY_SET"
    MEM = "MEM"
    UPDATE = "UPDATE"
    
    # Map operations
    EMPTY_MAP = "EMPTY_MAP"
    GET = "GET"
    
    # String operations
    CONCAT = "CONCAT"
    SLICE = "SLICE"
    
    # Cryptographic operations
    PACK = "PACK"
    UNPACK = "UNPACK"
    BLAKE2B = "BLAKE2B"
    SHA256 = "SHA256"
    SHA512 = "SHA512"
    HASH_KEY = "HASH_KEY"
    CHECK_SIGNATURE = "CHECK_SIGNATURE"
    
    # Blockchain operations
    NOW = "NOW"
    AMOUNT = "AMOUNT"
    BALANCE = "BALANCE"
    SENDER = "SENDER"
    SOURCE = "SOURCE"
    ADDRESS = "ADDRESS"
    CONTRACT = "CONTRACT"
    TRANSFER_TOKENS = "TRANSFER_TOKENS"
    CREATE_CONTRACT = "CREATE_CONTRACT"
    IMPLICIT_ACCOUNT = "IMPLICIT_ACCOUNT"
    SET_DELEGATE = "SET_DELEGATE"
    
    # Domain-specific operations
    SELF = "SELF"
    CHAIN_ID = "CHAIN_ID"
    TOTAL_VOTING_POWER = "TOTAL_VOTING_POWER"
    VOTING_POWER = "VOTING_POWER"
    KECCAK = "KECCAK"
    SHA3 = "SHA3"
    PAIRING_CHECK = "PAIRING_CHECK"
    
    # Exception handling
    FAILWITH = "FAILWITH"
    NEVER = "NEVER"


class MichelsonComparable(Enum):
    """Michelson comparable types for sets and map keys."""
    UNIT = "unit"
    BOOL = "bool"
    INT = "int"
    NAT = "nat"
    STRING = "string"
    BYTES = "bytes"
    MUTEZ = "mutez"
    KEY_HASH = "key_hash"
    TIMESTAMP = "timestamp"
    ADDRESS = "address"
    CHAIN_ID = "chain_id"


class MichelsonNode(ABC):
    """Base class for all Michelson AST nodes."""
    
    def __init__(self, position: Optional[tuple] = None):
        self.position = position
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"


class MichelsonType_Node(MichelsonNode):
    """Represents a Michelson type."""
    
    def __init__(self, type_name: MichelsonType, args: Optional[List['MichelsonType_Node']] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.type_name = type_name
        self.args = args or []
    
    def accept(self, visitor):
        return visitor.visit_michelson_type(self)
    
    def __repr__(self):
        if self.args:
            args_str = " ".join(str(arg) for arg in self.args)
            return f"({self.type_name.value} {args_str})"
        return self.type_name.value


class MichelsonLiteral(MichelsonNode):
    """Represents a Michelson literal value."""
    
    def __init__(self, value: Any, type_hint: Optional[MichelsonType] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.value = value
        self.type_hint = type_hint
    
    def accept(self, visitor):
        return visitor.visit_michelson_literal(self)
    
    def __repr__(self):
        return f"MichelsonLiteral({self.value})"


class MichelsonInstruction_Node(MichelsonNode):
    """Represents a Michelson instruction."""
    
    def __init__(self, instruction: MichelsonInstruction, 
                 args: Optional[List[Union['MichelsonInstruction_Node', MichelsonLiteral, 'MichelsonType_Node']]] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.instruction = instruction
        self.args = args or []
    
    def accept(self, visitor):
        return visitor.visit_michelson_instruction(self)
    
    def __repr__(self):
        if self.args:
            args_str = " ".join(str(arg) for arg in self.args)
            return f"{self.instruction.value} {args_str}"
        return self.instruction.value


class MichelsonSequence(MichelsonNode):
    """Represents a sequence of Michelson instructions."""
    
    def __init__(self, instructions: List[MichelsonInstruction_Node],
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.instructions = instructions
    
    def accept(self, visitor):
        return visitor.visit_michelson_sequence(self)
    
    def __repr__(self):
        return f"MichelsonSequence({len(self.instructions)} instructions)"


class MichelsonPair(MichelsonNode):
    """Represents a Michelson pair."""
    
    def __init__(self, left: MichelsonNode, right: MichelsonNode,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.left = left
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_michelson_pair(self)
    
    def __repr__(self):
        return f"Pair({self.left}, {self.right})"


class MichelsonLeft(MichelsonNode):
    """Represents a Michelson Left variant."""
    
    def __init__(self, value: MichelsonNode, position: Optional[tuple] = None):
        super().__init__(position)
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_michelson_left(self)


class MichelsonRight(MichelsonNode):
    """Represents a Michelson Right variant."""
    
    def __init__(self, value: MichelsonNode, position: Optional[tuple] = None):
        super().__init__(position)
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_michelson_right(self)


class MichelsonSome(MichelsonNode):
    """Represents a Michelson Some option."""
    
    def __init__(self, value: MichelsonNode, position: Optional[tuple] = None):
        super().__init__(position)
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_michelson_some(self)


class MichelsonNone(MichelsonNode):
    """Represents a Michelson None option."""
    
    def __init__(self, type_annotation: MichelsonType_Node, position: Optional[tuple] = None):
        super().__init__(position)
        self.type_annotation = type_annotation
    
    def accept(self, visitor):
        return visitor.visit_michelson_none(self)


class MichelsonList(MichelsonNode):
    """Represents a Michelson list."""
    
    def __init__(self, elements: List[MichelsonNode], 
                 element_type: Optional[MichelsonType_Node] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.elements = elements
        self.element_type = element_type
    
    def accept(self, visitor):
        return visitor.visit_michelson_list(self)


class MichelsonSet(MichelsonNode):
    """Represents a Michelson set."""
    
    def __init__(self, elements: List[MichelsonNode],
                 element_type: Optional[MichelsonType_Node] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.elements = elements
        self.element_type = element_type
    
    def accept(self, visitor):
        return visitor.visit_michelson_set(self)


class MichelsonMap(MichelsonNode):
    """Represents a Michelson map."""
    
    def __init__(self, entries: List[MichelsonPair],
                 key_type: Optional[MichelsonType_Node] = None,
                 value_type: Optional[MichelsonType_Node] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.entries = entries
        self.key_type = key_type
        self.value_type = value_type
    
    def accept(self, visitor):
        return visitor.visit_michelson_map(self)


class MichelsonLambda(MichelsonNode):
    """Represents a Michelson lambda function."""
    
    def __init__(self, param_type: MichelsonType_Node, return_type: MichelsonType_Node,
                 body: MichelsonSequence, position: Optional[tuple] = None):
        super().__init__(position)
        self.param_type = param_type
        self.return_type = return_type
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_michelson_lambda(self)


class MichelsonContract(MichelsonNode):
    """Represents a Michelson smart contract."""
    
    def __init__(self, parameter_type: MichelsonType_Node, storage_type: MichelsonType_Node,
                 code: MichelsonSequence, position: Optional[tuple] = None):
        super().__init__(position)
        self.parameter_type = parameter_type
        self.storage_type = storage_type
        self.code = code
    
    def accept(self, visitor):
        return visitor.visit_michelson_contract(self)
    
    def __repr__(self):
        return f"MichelsonContract(param: {self.parameter_type}, storage: {self.storage_type})"


class MichelsonConditional(MichelsonNode):
    """Represents a Michelson conditional (IF, IF_NONE, etc.)."""
    
    def __init__(self, condition_type: MichelsonInstruction, 
                 then_branch: MichelsonSequence,
                 else_branch: MichelsonSequence,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.condition_type = condition_type
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def accept(self, visitor):
        return visitor.visit_michelson_conditional(self)


class MichelsonLoop(MichelsonNode):
    """Represents a Michelson loop (LOOP, LOOP_LEFT, ITER, MAP)."""
    
    def __init__(self, loop_type: MichelsonInstruction, body: MichelsonSequence,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.loop_type = loop_type
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_michelson_loop(self)


class MichelsonAnnotation(MichelsonNode):
    """Represents a Michelson annotation."""
    
    def __init__(self, annotation_type: str, name: str, position: Optional[tuple] = None):
        super().__init__(position)
        self.annotation_type = annotation_type  # @, %, :, &
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_michelson_annotation(self)
    
    def __repr__(self):
        return f"{self.annotation_type}{self.name}"


class MichelsonMacro(MichelsonNode):
    """Represents a Michelson macro expansion."""
    
    def __init__(self, macro_name: str, args: List[MichelsonNode],
                 expanded: Optional[MichelsonSequence] = None,
                 position: Optional[tuple] = None):
        super().__init__(position)
        self.macro_name = macro_name
        self.args = args
        self.expanded = expanded
    
    def accept(self, visitor):
        return visitor.visit_michelson_macro(self)


# Visitor interface for traversing Michelson AST
class MichelsonVisitor(ABC):
    """Abstract visitor for Michelson AST nodes."""
    
    @abstractmethod
    def visit_michelson_type(self, node: MichelsonType_Node): pass
    
    @abstractmethod
    def visit_michelson_literal(self, node: MichelsonLiteral): pass
    
    @abstractmethod
    def visit_michelson_instruction(self, node: MichelsonInstruction_Node): pass
    
    @abstractmethod
    def visit_michelson_sequence(self, node: MichelsonSequence): pass
    
    @abstractmethod
    def visit_michelson_pair(self, node: MichelsonPair): pass
    
    @abstractmethod
    def visit_michelson_left(self, node: MichelsonLeft): pass
    
    @abstractmethod
    def visit_michelson_right(self, node: MichelsonRight): pass
    
    @abstractmethod
    def visit_michelson_some(self, node: MichelsonSome): pass
    
    @abstractmethod
    def visit_michelson_none(self, node: MichelsonNone): pass
    
    @abstractmethod
    def visit_michelson_list(self, node: MichelsonList): pass
    
    @abstractmethod
    def visit_michelson_set(self, node: MichelsonSet): pass
    
    @abstractmethod
    def visit_michelson_map(self, node: MichelsonMap): pass
    
    @abstractmethod
    def visit_michelson_lambda(self, node: MichelsonLambda): pass
    
    @abstractmethod
    def visit_michelson_contract(self, node: MichelsonContract): pass
    
    @abstractmethod
    def visit_michelson_conditional(self, node: MichelsonConditional): pass
    
    @abstractmethod
    def visit_michelson_loop(self, node: MichelsonLoop): pass
    
    @abstractmethod
    def visit_michelson_annotation(self, node: MichelsonAnnotation): pass
    
    @abstractmethod
    def visit_michelson_macro(self, node: MichelsonMacro): pass


# Type aliases for convenience
MichelsonASTNode = Union[
    MichelsonType_Node, MichelsonLiteral, MichelsonInstruction_Node, MichelsonSequence,
    MichelsonPair, MichelsonLeft, MichelsonRight, MichelsonSome, MichelsonNone,
    MichelsonList, MichelsonSet, MichelsonMap, MichelsonLambda, MichelsonContract,
    MichelsonConditional, MichelsonLoop, MichelsonAnnotation, MichelsonMacro
] 