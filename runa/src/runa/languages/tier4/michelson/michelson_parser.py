"""
Michelson Parser for the stack-based smart contract language on Tezos.

This module provides lexical analysis and parsing capabilities for Michelson,
supporting the complete stack-based syntax and smart contract structure.
"""

import re
from typing import List, Optional, Union, Dict, Any
from enum import Enum
from .michelson_ast import *


class TokenType(Enum):
    """Token types for Michelson lexical analysis."""
    # Literals
    INTEGER = "INTEGER"
    STRING = "STRING"
    BYTES = "BYTES"
    
    # Keywords
    PARAMETER = "parameter"
    STORAGE = "storage"
    CODE = "code"
    
    # Instructions
    INSTRUCTION = "INSTRUCTION"
    
    # Types
    TYPE = "TYPE"
    
    # Delimiters
    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    SEMICOLON = ";"
    
    # Annotations
    TYPE_ANNOTATION = "TYPE_ANNOTATION"      # :annotation
    VARIABLE_ANNOTATION = "VARIABLE_ANNOTATION"  # @annotation  
    FIELD_ANNOTATION = "FIELD_ANNOTATION"   # %annotation
    ENTRYPOINT_ANNOTATION = "ENTRYPOINT_ANNOTATION"  # &annotation
    
    # Special
    IDENTIFIER = "IDENTIFIER"
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    WHITESPACE = "WHITESPACE"
    
    # Macro names
    MACRO = "MACRO"


class Token:
    """Represents a token in Michelson source code."""
    
    def __init__(self, type_: TokenType, value: str, line: int = 1, column: int = 1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"


class MichelsonLexer:
    """Lexer for Michelson language."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Michelson instruction set
        self.instructions = {
            # Stack operations
            "DROP", "DUP", "SWAP", "DIG", "DUG", "PUSH",
            # Arithmetic
            "ADD", "SUB", "MUL", "DIV", "MOD", "ABS", "NEG",
            "LSL", "LSR", "OR", "AND", "XOR", "NOT",
            # Comparison
            "COMPARE", "EQ", "NEQ", "LT", "GT", "LE", "GE",
            # Control flow
            "IF", "IF_NONE", "IF_LEFT", "IF_CONS", "LOOP", "LOOP_LEFT", "ITER", "MAP",
            # Data operations
            "PAIR", "UNPAIR", "CAR", "CDR", "LEFT", "RIGHT", "SOME", "NONE", "UNIT",
            # List operations
            "CONS", "NIL", "SIZE",
            # Set operations  
            "EMPTY_SET", "MEM", "UPDATE",
            # Map operations
            "EMPTY_MAP", "GET",
            # String operations
            "CONCAT", "SLICE",
            # Crypto operations
            "PACK", "UNPACK", "BLAKE2B", "SHA256", "SHA512", "HASH_KEY", "CHECK_SIGNATURE",
            # Blockchain operations
            "NOW", "AMOUNT", "BALANCE", "SENDER", "SOURCE", "ADDRESS", "CONTRACT",
            "TRANSFER_TOKENS", "CREATE_CONTRACT", "IMPLICIT_ACCOUNT", "SET_DELEGATE",
            # Domain-specific
            "SELF", "CHAIN_ID", "TOTAL_VOTING_POWER", "VOTING_POWER", "KECCAK", "SHA3", "PAIRING_CHECK",
            # Exception handling
            "FAILWITH", "NEVER"
        }
        
        # Michelson types
        self.types = {
            "unit", "int", "nat", "string", "bytes", "bool", "mutez", "tez",
            "address", "key", "key_hash", "signature", "timestamp", "chain_id",
            "operation", "contract", "pair", "or", "option", "list", "set", 
            "map", "big_map", "lambda"
        }
        
        # Common macros
        self.macros = {
            "ASSERT", "ASSERT_EQ", "ASSERT_NEQ", "ASSERT_LT", "ASSERT_LE", 
            "ASSERT_GT", "ASSERT_GE", "ASSERT_CMPEQ", "ASSERT_CMPNEQ",
            "ASSERT_CMPLE", "ASSERT_CMPLT", "ASSERT_CMPGE", "ASSERT_CMPGT",
            "FAIL", "ASSERT_NONE", "ASSERT_SOME", "ASSERT_LEFT", "ASSERT_RIGHT"
        }
    
    def error(self, message: str):
        """Raise a lexer error with position information."""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def current_char(self) -> Optional[str]:
        """Get current character or None if at end."""
        return self.source[self.position] if self.position < len(self.source) else None
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character with offset."""
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else None
    
    def advance(self):
        """Advance position and update line/column."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def read_string(self) -> str:
        """Read a string literal."""
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == quote_char:
                    value += quote_char
                else:
                    value += escape_char or ""
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() != quote_char:
            self.error(f"Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return value
    
    def read_bytes(self) -> str:
        """Read a bytes literal (0x...)."""
        value = ""
        self.advance()  # Skip '0'
        self.advance()  # Skip 'x'
        
        while self.current_char() and self.current_char() in "0123456789abcdefABCDEF":
            value += self.current_char()
            self.advance()
        
        return "0x" + value
    
    def read_number(self) -> str:
        """Read a number literal."""
        value = ""
        
        # Handle negative numbers
        if self.current_char() == '-':
            value += '-'
            self.advance()
        
        while self.current_char() and self.current_char().isdigit():
            value += self.current_char()
            self.advance()
        
        return value
    
    def read_identifier(self) -> str:
        """Read an identifier or keyword."""
        value = ""
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in "_")):
            value += self.current_char()
            self.advance()
        
        return value
    
    def read_annotation(self) -> tuple:
        """Read an annotation (starts with @, %, :, or &)."""
        annotation_type = self.current_char()
        self.advance()
        
        name = ""
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in "_")):
            name += self.current_char()
            self.advance()
        
        if annotation_type == '@':
            return TokenType.VARIABLE_ANNOTATION, f"@{name}"
        elif annotation_type == '%':
            return TokenType.FIELD_ANNOTATION, f"%{name}"
        elif annotation_type == ':':
            return TokenType.TYPE_ANNOTATION, f":{name}"
        elif annotation_type == '&':
            return TokenType.ENTRYPOINT_ANNOTATION, f"&{name}"
    
    def read_comment(self) -> str:
        """Read a comment (# to end of line)."""
        value = ""
        self.advance()  # Skip '#'
        
        while self.current_char() and self.current_char() != '\n':
            value += self.current_char()
            self.advance()
        
        return value
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        self.tokens = []
        
        while self.position < len(self.source):
            char = self.current_char()
            
            if char is None:
                break
            
            # Skip whitespace
            if char.isspace():
                self.skip_whitespace()
                continue
            
            # Comments
            if char == '#':
                comment_value = self.read_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment_value, self.line, self.column))
                continue
            
            # String literals
            if char in ['"', "'"]:
                string_value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, string_value, self.line, self.column))
                continue
            
            # Bytes literals
            if char == '0' and self.peek_char() == 'x':
                bytes_value = self.read_bytes()
                self.tokens.append(Token(TokenType.BYTES, bytes_value, self.line, self.column))
                continue
            
            # Numbers
            if char.isdigit() or (char == '-' and self.peek_char() and self.peek_char().isdigit()):
                number_value = self.read_number()
                self.tokens.append(Token(TokenType.INTEGER, number_value, self.line, self.column))
                continue
            
            # Annotations
            if char in '@%:&':
                annotation_type, annotation_value = self.read_annotation()
                self.tokens.append(Token(annotation_type, annotation_value, self.line, self.column))
                continue
            
            # Single-character tokens
            if char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, self.line, self.column))
                self.advance()
                continue
            
            if char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, self.line, self.column))
                self.advance()
                continue
            
            if char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, self.line, self.column))
                self.advance()
                continue
            
            if char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, self.line, self.column))
                self.advance()
                continue
            
            if char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, char, self.line, self.column))
                self.advance()
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                identifier = self.read_identifier()
                
                # Check if it's a keyword
                if identifier in ["parameter", "storage", "code"]:
                    self.tokens.append(Token(TokenType.PARAMETER if identifier == "parameter" 
                                           else TokenType.STORAGE if identifier == "storage"
                                           else TokenType.CODE, identifier, self.line, self.column))
                elif identifier in self.instructions:
                    self.tokens.append(Token(TokenType.INSTRUCTION, identifier, self.line, self.column))
                elif identifier in self.types:
                    self.tokens.append(Token(TokenType.TYPE, identifier, self.line, self.column))
                elif identifier in self.macros:
                    self.tokens.append(Token(TokenType.MACRO, identifier, self.line, self.column))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, identifier, self.line, self.column))
                continue
            
            # Unknown character
            self.error(f"Unknown character: '{char}'")
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens


class MichelsonParser:
    """Parser for Michelson language."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, message: str):
        """Raise a parser error with position information."""
        token = self.current_token
        raise SyntaxError(f"Parser error at line {token.line}, column {token.column}: {message}")
    
    def advance(self):
        """Advance to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type and advance."""
        if not self.current_token or self.current_token.type != token_type:
            self.error(f"Expected {token_type.value}, got {self.current_token.type.value if self.current_token else 'EOF'}")
        
        token = self.current_token
        self.advance()
        return token
    
    def match(self, token_type: TokenType) -> bool:
        """Check if current token matches type without advancing."""
        return self.current_token and self.current_token.type == token_type
    
    def skip_comments_and_semicolons(self):
        """Skip comments and semicolons."""
        while self.current_token and self.current_token.type in [TokenType.COMMENT, TokenType.SEMICOLON]:
            self.advance()
    
    def parse_type(self) -> MichelsonType_Node:
        """Parse a Michelson type."""
        self.skip_comments_and_semicolons()
        
        if self.match(TokenType.LPAREN):
            self.advance()  # Skip '('
            
            # Parse compound type
            type_token = self.expect(TokenType.TYPE)
            type_enum = MichelsonType(type_token.value)
            
            args = []
            while not self.match(TokenType.RPAREN):
                self.skip_comments_and_semicolons()
                args.append(self.parse_type())
                self.skip_comments_and_semicolons()
            
            self.expect(TokenType.RPAREN)
            return MichelsonType_Node(type_enum, args)
        
        elif self.match(TokenType.TYPE):
            type_token = self.advance_and_return()
            type_enum = MichelsonType(type_token.value)
            return MichelsonType_Node(type_enum)
        
        else:
            self.error(f"Expected type, got {self.current_token.type.value}")
    
    def advance_and_return(self) -> Token:
        """Advance and return the previous token."""
        token = self.current_token
        self.advance()
        return token
    
    def parse_literal(self) -> MichelsonLiteral:
        """Parse a literal value."""
        if self.match(TokenType.INTEGER):
            token = self.advance_and_return()
            return MichelsonLiteral(int(token.value), MichelsonType.INT)
        
        elif self.match(TokenType.STRING):
            token = self.advance_and_return()
            return MichelsonLiteral(token.value, MichelsonType.STRING)
        
        elif self.match(TokenType.BYTES):
            token = self.advance_and_return()
            return MichelsonLiteral(token.value, MichelsonType.BYTES)
        
        else:
            self.error(f"Expected literal, got {self.current_token.type.value}")
    
    def parse_instruction(self) -> MichelsonInstruction_Node:
        """Parse a Michelson instruction."""
        self.skip_comments_and_semicolons()
        
        if self.match(TokenType.INSTRUCTION):
            instruction_token = self.advance_and_return()
            instruction_enum = MichelsonInstruction(instruction_token.value)
            
            args = []
            
            # Parse instruction arguments
            while (self.current_token and 
                   self.current_token.type not in [TokenType.RBRACE, TokenType.SEMICOLON, 
                                                  TokenType.EOF, TokenType.INSTRUCTION]):
                self.skip_comments_and_semicolons()
                
                if self.match(TokenType.TYPE) or self.match(TokenType.LPAREN):
                    args.append(self.parse_type())
                elif self.match(TokenType.INTEGER) or self.match(TokenType.STRING) or self.match(TokenType.BYTES):
                    args.append(self.parse_literal())
                elif self.match(TokenType.LBRACE):
                    args.append(self.parse_instruction_sequence())
                else:
                    break
            
            return MichelsonInstruction_Node(instruction_enum, args)
        
        elif self.match(TokenType.MACRO):
            macro_token = self.advance_and_return()
            # Treat macros as special instructions for now
            return MichelsonInstruction_Node(MichelsonInstruction.FAILWITH, [MichelsonLiteral(macro_token.value)])
        
        else:
            self.error(f"Expected instruction, got {self.current_token.type.value}")
    
    def parse_instruction_sequence(self) -> MichelsonSequence:
        """Parse a sequence of instructions in braces."""
        self.expect(TokenType.LBRACE)
        
        instructions = []
        while not self.match(TokenType.RBRACE):
            self.skip_comments_and_semicolons()
            if self.match(TokenType.RBRACE):
                break
            instructions.append(self.parse_instruction())
            self.skip_comments_and_semicolons()
        
        self.expect(TokenType.RBRACE)
        return MichelsonSequence(instructions)
    
    def parse_contract(self) -> MichelsonContract:
        """Parse a complete Michelson contract."""
        self.skip_comments_and_semicolons()
        
        # Parse parameter
        self.expect(TokenType.PARAMETER)
        parameter_type = self.parse_type()
        self.skip_comments_and_semicolons()
        
        # Parse storage
        self.expect(TokenType.STORAGE)
        storage_type = self.parse_type()
        self.skip_comments_and_semicolons()
        
        # Parse code
        self.expect(TokenType.CODE)
        code = self.parse_instruction_sequence()
        
        return MichelsonContract(parameter_type, storage_type, code)
    
    def parse(self) -> MichelsonContract:
        """Parse the tokens into a Michelson AST."""
        try:
            contract = self.parse_contract()
            
            # Ensure we've consumed all tokens
            self.skip_comments_and_semicolons()
            if not self.match(TokenType.EOF):
                self.error("Expected end of input")
            
            return contract
        
        except Exception as e:
            raise SyntaxError(f"Failed to parse Michelson contract: {str(e)}")


def parse_michelson(source: str) -> MichelsonContract:
    """Parse Michelson source code into an AST."""
    lexer = MichelsonLexer(source)
    tokens = lexer.tokenize()
    
    # Filter out whitespace tokens
    filtered_tokens = [token for token in tokens if token.type != TokenType.WHITESPACE]
    
    parser = MichelsonParser(filtered_tokens)
    return parser.parse()


def parse_michelson_expression(source: str) -> MichelsonASTNode:
    """Parse a single Michelson expression."""
    lexer = MichelsonLexer(source)
    tokens = lexer.tokenize()
    
    # Filter out whitespace tokens
    filtered_tokens = [token for token in tokens if token.type != TokenType.WHITESPACE]
    
    parser = MichelsonParser(filtered_tokens)
    
    # Try to parse as instruction first
    try:
        return parser.parse_instruction()
    except:
        # Try to parse as type
        try:
            parser.position = 0
            parser.current_token = filtered_tokens[0] if filtered_tokens else None
            return parser.parse_type()
        except:
            # Try to parse as literal
            parser.position = 0
            parser.current_token = filtered_tokens[0] if filtered_tokens else None
            return parser.parse_literal() 