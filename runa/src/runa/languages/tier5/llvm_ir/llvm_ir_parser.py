"""
LLVM IR Parser - Parses LLVM Intermediate Representation source code.

This module provides parsing capabilities for LLVM IR syntax including
types, instructions, functions, basic blocks, and modules.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from .llvm_ir_ast import *


class LLVMIRTokenType(Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Identifiers
    GLOBAL_ID = "GLOBAL_ID"      # @global
    LOCAL_ID = "LOCAL_ID"        # %local
    LABEL_ID = "LABEL_ID"        # label:
    
    # Keywords
    DEFINE = "define"
    DECLARE = "declare"
    GLOBAL = "global"
    CONSTANT = "constant"
    TARGET = "target"
    DATALAYOUT = "datalayout"
    TRIPLE = "triple"
    
    # Types
    VOID = "void"
    I1 = "i1"
    I8 = "i8"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    FLOAT_TYPE = "float"
    DOUBLE = "double"
    LABEL = "label"
    
    # Instructions
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    UDIV = "udiv"
    SDIV = "sdiv"
    FDIV = "fdiv"
    ALLOCA = "alloca"
    LOAD = "load"
    STORE = "store"
    CALL = "call"
    RET = "ret"
    BR = "br"
    ICMP = "icmp"
    FCMP = "fcmp"
    PHI = "phi"
    
    # Operators
    EQUALS = "="
    COMMA = ","
    ASTERISK = "*"
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    
    # Special
    NULL = "null"
    UNDEF = "undef"
    POISON = "poison"
    TRUE = "true"
    FALSE = "false"
    
    # End
    EOF = "EOF"
    NEWLINE = "NEWLINE"


@dataclass
class LLVMIRToken:
    type: LLVMIRTokenType
    value: str
    line: int
    column: int


class LLVMIRSyntaxError(Exception):
    """LLVM IR syntax error exception."""
    
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Syntax error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column


class LLVMIRLexer:
    """LLVM IR lexer for tokenizing source code."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[LLVMIRToken] = []
        
        # Keywords mapping
        self.keywords = {
            "define": LLVMIRTokenType.DEFINE,
            "declare": LLVMIRTokenType.DECLARE,
            "global": LLVMIRTokenType.GLOBAL,
            "constant": LLVMIRTokenType.CONSTANT,
            "target": LLVMIRTokenType.TARGET,
            "datalayout": LLVMIRTokenType.DATALAYOUT,
            "triple": LLVMIRTokenType.TRIPLE,
            "void": LLVMIRTokenType.VOID,
            "i1": LLVMIRTokenType.I1,
            "i8": LLVMIRTokenType.I8,
            "i16": LLVMIRTokenType.I16,
            "i32": LLVMIRTokenType.I32,
            "i64": LLVMIRTokenType.I64,
            "float": LLVMIRTokenType.FLOAT_TYPE,
            "double": LLVMIRTokenType.DOUBLE,
            "label": LLVMIRTokenType.LABEL,
            "add": LLVMIRTokenType.ADD,
            "sub": LLVMIRTokenType.SUB,
            "mul": LLVMIRTokenType.MUL,
            "udiv": LLVMIRTokenType.UDIV,
            "sdiv": LLVMIRTokenType.SDIV,
            "fdiv": LLVMIRTokenType.FDIV,
            "alloca": LLVMIRTokenType.ALLOCA,
            "load": LLVMIRTokenType.LOAD,
            "store": LLVMIRTokenType.STORE,
            "call": LLVMIRTokenType.CALL,
            "ret": LLVMIRTokenType.RET,
            "br": LLVMIRTokenType.BR,
            "icmp": LLVMIRTokenType.ICMP,
            "fcmp": LLVMIRTokenType.FCMP,
            "phi": LLVMIRTokenType.PHI,
            "null": LLVMIRTokenType.NULL,
            "undef": LLVMIRTokenType.UNDEF,
            "poison": LLVMIRTokenType.POISON,
            "true": LLVMIRTokenType.TRUE,
            "false": LLVMIRTokenType.FALSE,
        }
    
    def tokenize(self) -> List[LLVMIRToken]:
        """Tokenize the source code."""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            char = self.source[self.position]
            
            if char == '\n':
                self._add_token(LLVMIRTokenType.NEWLINE, char)
                self._advance()
                self.line += 1
                self.column = 1
            elif char == ';':
                self._skip_comment()
            elif char == '"':
                self._read_string()
            elif char.isdigit() or (char == '-' and self._peek().isdigit()):
                self._read_number()
            elif char == '@':
                self._read_global_id()
            elif char == '%':
                self._read_local_id()
            elif char.isalpha() or char == '_':
                self._read_identifier()
            elif char == '=':
                self._add_token(LLVMIRTokenType.EQUALS, char)
                self._advance()
            elif char == ',':
                self._add_token(LLVMIRTokenType.COMMA, char)
                self._advance()
            elif char == '*':
                self._add_token(LLVMIRTokenType.ASTERISK, char)
                self._advance()
            elif char == '(':
                self._add_token(LLVMIRTokenType.LPAREN, char)
                self._advance()
            elif char == ')':
                self._add_token(LLVMIRTokenType.RPAREN, char)
                self._advance()
            elif char == '{':
                self._add_token(LLVMIRTokenType.LBRACE, char)
                self._advance()
            elif char == '}':
                self._add_token(LLVMIRTokenType.RBRACE, char)
                self._advance()
            elif char == '[':
                self._add_token(LLVMIRTokenType.LBRACKET, char)
                self._advance()
            elif char == ']':
                self._add_token(LLVMIRTokenType.RBRACKET, char)
                self._advance()
            else:
                raise LLVMIRSyntaxError(f"Unexpected character: {char}", self.line, self.column)
        
        self._add_token(LLVMIRTokenType.EOF, "")
        return self.tokens
    
    def _advance(self) -> str:
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            self.column += 1
            return char
        return ''
    
    def _peek(self, offset: int = 1) -> str:
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else ''
    
    def _skip_whitespace(self) -> None:
        while (self.position < len(self.source) and 
               self.source[self.position] in ' \t\r'):
            self._advance()
    
    def _skip_comment(self) -> None:
        while (self.position < len(self.source) and 
               self.source[self.position] != '\n'):
            self._advance()
    
    def _read_string(self) -> None:
        start_line = self.line
        start_column = self.column
        value = ""
        
        self._advance()  # Skip opening quote
        
        while (self.position < len(self.source) and 
               self.source[self.position] != '"'):
            char = self._advance()
            if char == '\\':
                # Handle escape sequences
                escaped = self._advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == '"':
                    value += '"'
                elif escaped == '\\':
                    value += '\\'
                else:
                    value += escaped
            else:
                value += char
        
        if self.position >= len(self.source):
            raise LLVMIRSyntaxError("Unterminated string", start_line, start_column)
        
        self._advance()  # Skip closing quote
        self._add_token(LLVMIRTokenType.STRING, value)
    
    def _read_number(self) -> None:
        value = ""
        
        # Handle negative numbers
        if self.source[self.position] == '-':
            value += self._advance()
        
        # Read integer part
        while (self.position < len(self.source) and 
               self.source[self.position].isdigit()):
            value += self._advance()
        
        # Check for float
        if (self.position < len(self.source) and 
            self.source[self.position] == '.' and
            self._peek().isdigit()):
            value += self._advance()  # decimal point
            
            while (self.position < len(self.source) and 
                   self.source[self.position].isdigit()):
                value += self._advance()
            
            self._add_token(LLVMIRTokenType.FLOAT, value)
        else:
            self._add_token(LLVMIRTokenType.INTEGER, value)
    
    def _read_global_id(self) -> None:
        value = self._advance()  # @
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or 
                self.source[self.position] in '_.:')):
            value += self._advance()
        
        self._add_token(LLVMIRTokenType.GLOBAL_ID, value)
    
    def _read_local_id(self) -> None:
        value = self._advance()  # %
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or 
                self.source[self.position] in '_.')):
            value += self._advance()
        
        self._add_token(LLVMIRTokenType.LOCAL_ID, value)
    
    def _read_identifier(self) -> None:
        value = ""
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or 
                self.source[self.position] == '_')):
            value += self._advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(value.lower(), LLVMIRTokenType.LABEL_ID)
        self._add_token(token_type, value)
    
    def _add_token(self, token_type: LLVMIRTokenType, value: str) -> None:
        token = LLVMIRToken(token_type, value, self.line, self.column - len(value))
        self.tokens.append(token)


class LLVMIRParser:
    """LLVM IR parser for creating AST from tokens."""
    
    def __init__(self, tokens: List[LLVMIRToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def parse(self) -> ModuleNode:
        """Parse tokens into LLVM IR module AST."""
        module = ModuleNode()
        
        while not self._is_at_end():
            if self._match(LLVMIRTokenType.NEWLINE):
                continue
            
            if self._match(LLVMIRTokenType.TARGET):
                self._parse_target_directive(module)
            elif self._match(LLVMIRTokenType.DEFINE):
                function = self._parse_function_definition()
                module.add_function(function)
            elif self._match(LLVMIRTokenType.DECLARE):
                function = self._parse_function_declaration()
                module.add_function(function)
            elif self._match(LLVMIRTokenType.GLOBAL_ID):
                global_var = self._parse_global_variable()
                module.add_global(global_var)
            else:
                self._advance()
        
        return module
    
    def _parse_target_directive(self, module: ModuleNode) -> None:
        """Parse target directive."""
        if self._match(LLVMIRTokenType.DATALAYOUT):
            self._consume(LLVMIRTokenType.EQUALS)
            layout = self._consume(LLVMIRTokenType.STRING).value
            module.data_layout = layout
        elif self._match(LLVMIRTokenType.TRIPLE):
            self._consume(LLVMIRTokenType.EQUALS)
            triple = self._consume(LLVMIRTokenType.STRING).value
            module.target_triple = triple
    
    def _parse_function_definition(self) -> FunctionNode:
        """Parse function definition."""
        # Get return type
        return_type = self._parse_type()
        
        # Get function name
        name_token = self._consume(LLVMIRTokenType.GLOBAL_ID)
        name = name_token.value[1:]  # Remove @
        
        # Parse parameters
        self._consume(LLVMIRTokenType.LPAREN)
        param_types = []
        
        while not self._check(LLVMIRTokenType.RPAREN):
            param_type = self._parse_type()
            param_types.append(param_type)
            
            if self._match(LLVMIRTokenType.LOCAL_ID):
                # Parameter name (ignore for now)
                pass
            
            if not self._check(LLVMIRTokenType.RPAREN):
                self._consume(LLVMIRTokenType.COMMA)
        
        self._consume(LLVMIRTokenType.RPAREN)
        
        # Create function type
        func_type = FunctionTypeNode(return_type, param_types)
        function = FunctionNode(name, func_type)
        
        # Parse function body
        if self._match(LLVMIRTokenType.LBRACE):
            while not self._check(LLVMIRTokenType.RBRACE):
                if self._match(LLVMIRTokenType.NEWLINE):
                    continue
                
                if self._check_label():
                    block = self._parse_basic_block()
                    function.add_basic_block(block)
                else:
                    self._advance()
            
            self._consume(LLVMIRTokenType.RBRACE)
        
        return function
    
    def _parse_function_declaration(self) -> FunctionNode:
        """Parse function declaration."""
        return_type = self._parse_type()
        name_token = self._consume(LLVMIRTokenType.GLOBAL_ID)
        name = name_token.value[1:]
        
        self._consume(LLVMIRTokenType.LPAREN)
        param_types = []
        
        while not self._check(LLVMIRTokenType.RPAREN):
            param_type = self._parse_type()
            param_types.append(param_type)
            
            if not self._check(LLVMIRTokenType.RPAREN):
                self._consume(LLVMIRTokenType.COMMA)
        
        self._consume(LLVMIRTokenType.RPAREN)
        
        func_type = FunctionTypeNode(return_type, param_types)
        return FunctionNode(name, func_type)
    
    def _parse_global_variable(self) -> GlobalVariableNode:
        """Parse global variable."""
        name_token = self._previous()
        name = name_token.value[1:]  # Remove @
        
        self._consume(LLVMIRTokenType.EQUALS)
        
        # Parse linkage/storage class
        linkage = "external"
        if self._match_any([LLVMIRTokenType.GLOBAL, LLVMIRTokenType.CONSTANT]):
            pass  # Use default linkage
        
        # Parse type
        var_type = self._parse_type()
        
        # Parse initializer
        initializer = None
        if not self._check(LLVMIRTokenType.NEWLINE) and not self._is_at_end():
            initializer = self._parse_constant()
        
        return GlobalVariableNode(name, var_type, initializer, linkage)
    
    def _parse_basic_block(self) -> BasicBlockNode:
        """Parse basic block."""
        # Parse label
        label_token = self._advance()
        label_name = label_token.value.rstrip(':')
        
        block = BasicBlockNode(label_name)
        
        # Parse instructions
        while (not self._is_at_end() and 
               not self._check(LLVMIRTokenType.RBRACE) and
               not self._check_label()):
            if self._match(LLVMIRTokenType.NEWLINE):
                continue
            
            instruction = self._parse_instruction()
            if instruction:
                block.add_instruction(instruction)
        
        return block
    
    def _parse_instruction(self) -> Optional[InstructionNode]:
        """Parse instruction."""
        # Check for assignment
        result_name = None
        if (self._check(LLVMIRTokenType.LOCAL_ID) and 
            self._peek_token(1).type == LLVMIRTokenType.EQUALS):
            result_name = self._advance().value[1:]  # Remove %
            self._consume(LLVMIRTokenType.EQUALS)
        
        # Parse instruction based on opcode
        if self._match(LLVMIRTokenType.ADD):
            return self._parse_binary_op("add", result_name)
        elif self._match(LLVMIRTokenType.SUB):
            return self._parse_binary_op("sub", result_name)
        elif self._match(LLVMIRTokenType.MUL):
            return self._parse_binary_op("mul", result_name)
        elif self._match(LLVMIRTokenType.ALLOCA):
            return self._parse_alloca(result_name)
        elif self._match(LLVMIRTokenType.LOAD):
            return self._parse_load(result_name)
        elif self._match(LLVMIRTokenType.STORE):
            return self._parse_store()
        elif self._match(LLVMIRTokenType.CALL):
            return self._parse_call(result_name)
        elif self._match(LLVMIRTokenType.RET):
            return self._parse_return()
        elif self._match(LLVMIRTokenType.BR):
            return self._parse_branch()
        else:
            # Skip unknown instruction
            self._advance()
            return None
    
    def _parse_binary_op(self, opcode: str, result_name: Optional[str]) -> InstructionNode:
        """Parse binary operation."""
        op_type = self._parse_type()
        left = self._parse_value()
        self._consume(LLVMIRTokenType.COMMA)
        right = self._parse_value()
        
        if opcode == "add":
            return AddNode(left, right, name=result_name)
        elif opcode == "sub":
            return SubNode(left, right, name=result_name)
        elif opcode == "mul":
            return MulNode(left, right, name=result_name)
        else:
            return BinaryOpNode(opcode, left, right, result_name)
    
    def _parse_alloca(self, result_name: Optional[str]) -> AllocaNode:
        """Parse alloca instruction."""
        allocated_type = self._parse_type()
        return AllocaNode(allocated_type, name=result_name)
    
    def _parse_load(self, result_name: Optional[str]) -> LoadNode:
        """Parse load instruction."""
        load_type = self._parse_type()
        self._consume(LLVMIRTokenType.COMMA)
        pointer = self._parse_value()
        return LoadNode(pointer, name=result_name)
    
    def _parse_store(self) -> StoreNode:
        """Parse store instruction."""
        value = self._parse_typed_value()
        self._consume(LLVMIRTokenType.COMMA)
        pointer = self._parse_value()
        return StoreNode(value, pointer)
    
    def _parse_call(self, result_name: Optional[str]) -> CallNode:
        """Parse call instruction."""
        func_type = self._parse_type()
        function = self._parse_value()
        
        self._consume(LLVMIRTokenType.LPAREN)
        arguments = []
        
        while not self._check(LLVMIRTokenType.RPAREN):
            arg = self._parse_typed_value()
            arguments.append(arg)
            
            if not self._check(LLVMIRTokenType.RPAREN):
                self._consume(LLVMIRTokenType.COMMA)
        
        self._consume(LLVMIRTokenType.RPAREN)
        
        return CallNode(function, arguments, name=result_name)
    
    def _parse_return(self) -> ReturnNode:
        """Parse return instruction."""
        if (not self._check(LLVMIRTokenType.NEWLINE) and 
            not self._is_at_end()):
            return_value = self._parse_typed_value()
            return ReturnNode(return_value)
        else:
            return ReturnNode()
    
    def _parse_branch(self) -> BranchNode:
        """Parse branch instruction."""
        if self._check(LLVMIRTokenType.I1):
            # Conditional branch
            condition = self._parse_typed_value()
            self._consume(LLVMIRTokenType.COMMA)
            self._consume(LLVMIRTokenType.LABEL)
            # Parse labels (simplified)
            return BranchNode(condition)
        else:
            # Unconditional branch
            self._consume(LLVMIRTokenType.LABEL)
            return BranchNode()
    
    def _parse_type(self) -> TypeNode:
        """Parse type."""
        if self._match(LLVMIRTokenType.VOID):
            return VoidTypeNode()
        elif self._match(LLVMIRTokenType.I1):
            return IntegerTypeNode(1)
        elif self._match(LLVMIRTokenType.I8):
            return IntegerTypeNode(8)
        elif self._match(LLVMIRTokenType.I16):
            return IntegerTypeNode(16)
        elif self._match(LLVMIRTokenType.I32):
            return IntegerTypeNode(32)
        elif self._match(LLVMIRTokenType.I64):
            return IntegerTypeNode(64)
        elif self._match(LLVMIRTokenType.FLOAT_TYPE):
            return FloatTypeNode("float")
        elif self._match(LLVMIRTokenType.DOUBLE):
            return FloatTypeNode("double")
        elif self._match(LLVMIRTokenType.LABEL):
            return LabelTypeNode()
        else:
            # Default to i32
            return IntegerTypeNode(32)
    
    def _parse_value(self) -> ValueNode:
        """Parse value."""
        if self._check(LLVMIRTokenType.LOCAL_ID):
            name = self._advance().value[1:]  # Remove %
            # Create a placeholder value
            return ArgumentNode(IntegerTypeNode(32), name)
        elif self._check(LLVMIRTokenType.GLOBAL_ID):
            name = self._advance().value[1:]  # Remove @
            # Create a placeholder global
            return GlobalVariableNode(name, IntegerTypeNode(32))
        elif self._check(LLVMIRTokenType.INTEGER):
            value = int(self._advance().value)
            return IntegerConstantNode(value, 32)
        elif self._check(LLVMIRTokenType.FLOAT):
            value = float(self._advance().value)
            return FloatConstantNode(value, "float")
        elif self._match(LLVMIRTokenType.TRUE):
            return BoolConstantNode(True)
        elif self._match(LLVMIRTokenType.FALSE):
            return BoolConstantNode(False)
        elif self._match(LLVMIRTokenType.NULL):
            return NullConstantNode(PointerTypeNode(IntegerTypeNode(8)))
        elif self._match(LLVMIRTokenType.UNDEF):
            return UndefConstantNode(IntegerTypeNode(32))
        else:
            # Default placeholder
            return IntegerConstantNode(0, 32)
    
    def _parse_typed_value(self) -> ValueNode:
        """Parse typed value (type value)."""
        value_type = self._parse_type()
        value = self._parse_value()
        value.value_type = value_type
        return value
    
    def _parse_constant(self) -> ConstantNode:
        """Parse constant value."""
        if self._check(LLVMIRTokenType.INTEGER):
            value = int(self._advance().value)
            return IntegerConstantNode(value, 32)
        elif self._check(LLVMIRTokenType.FLOAT):
            value = float(self._advance().value)
            return FloatConstantNode(value, "float")
        elif self._match(LLVMIRTokenType.NULL):
            return NullConstantNode(PointerTypeNode(IntegerTypeNode(8)))
        else:
            return IntegerConstantNode(0, 32)
    
    def _check_label(self) -> bool:
        """Check if current token is a label."""
        return (self._check(LLVMIRTokenType.LABEL_ID) or 
                (self.current_token and ':' in self.current_token.value))
    
    def _match(self, token_type: LLVMIRTokenType) -> bool:
        """Check and consume token type."""
        if self._check(token_type):
            self._advance()
            return True
        return False
    
    def _match_any(self, token_types: List[LLVMIRTokenType]) -> bool:
        """Check and consume any of the token types."""
        for token_type in token_types:
            if self._match(token_type):
                return True
        return False
    
    def _check(self, token_type: LLVMIRTokenType) -> bool:
        """Check current token type."""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type
    
    def _advance(self) -> LLVMIRToken:
        """Consume and return current token."""
        if not self._is_at_end():
            self.position += 1
            if self.position < len(self.tokens):
                self.current_token = self.tokens[self.position]
        return self._previous()
    
    def _previous(self) -> LLVMIRToken:
        """Get previous token."""
        return self.tokens[self.position - 1]
    
    def _peek_token(self, offset: int) -> Optional[LLVMIRToken]:
        """Peek ahead at token."""
        pos = self.position + offset
        return self.tokens[pos] if pos < len(self.tokens) else None
    
    def _consume(self, token_type: LLVMIRTokenType) -> LLVMIRToken:
        """Consume expected token type."""
        if self._check(token_type):
            return self._advance()
        
        current = self.current_token.type if self.current_token else "EOF"
        raise LLVMIRSyntaxError(
            f"Expected {token_type}, got {current}",
            self.current_token.line if self.current_token else 0,
            self.current_token.column if self.current_token else 0
        )
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return (self.current_token is None or 
                self.current_token.type == LLVMIRTokenType.EOF)


# Utility functions
def parse_llvm_ir_file(filename: str) -> ModuleNode:
    """Parse LLVM IR from file."""
    with open(filename, 'r') as f:
        source = f.read()
    return parse_llvm_ir_string(source)


def parse_llvm_ir_string(source: str) -> ModuleNode:
    """Parse LLVM IR from string."""
    lexer = LLVMIRLexer(source)
    tokens = lexer.tokenize()
    parser = LLVMIRParser(tokens)
    return parser.parse()


def create_llvm_ir_parser(source: str) -> LLVMIRParser:
    """Create LLVM IR parser."""
    lexer = LLVMIRLexer(source)
    tokens = lexer.tokenize()
    return LLVMIRParser(tokens)


def validate_llvm_ir_syntax(source: str) -> List[str]:
    """Validate LLVM IR syntax."""
    try:
        parse_llvm_ir_string(source)
        return []
    except LLVMIRSyntaxError as e:
        return [str(e)]
    except Exception as e:
        return [f"Parse error: {str(e)}"] 