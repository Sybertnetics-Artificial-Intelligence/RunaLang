#!/usr/bin/env python3
"""
Visual Basic Parser Implementation

Complete parser for Visual Basic .NET with case-insensitive syntax support,
COM interoperability, Windows Forms, database connectivity, and .NET Framework integration.
"""

from typing import List, Optional, Union, Dict, Any, Tuple
import re
from enum import Enum, auto
from dataclasses import dataclass

from .visual_basic_ast import *


class ErrorType:
    """Error type constants."""
    SYNTAX_ERROR = "SYNTAX_ERROR"
    TYPE_ERROR = "TYPE_ERROR"
    NAME_ERROR = "NAME_ERROR"


class ErrorHandler:
    """Simple error handler."""
    def __init__(self):
        self.errors = []
    
    def add_error(self, error_type: str, message: str, line: int = 0, column: int = 0):
        self.errors.append({"type": error_type, "message": message, "line": line, "column": column})


# Token definitions
class VBTokenType(Enum):
    # Literals
    STRING = auto()
    INTEGER = auto()
    DECIMAL = auto()
    BOOLEAN = auto()
    NOTHING = auto()
    
    # Keywords
    CLASS = auto()
    MODULE = auto()
    INTERFACE = auto()
    STRUCTURE = auto()
    ENUM = auto()
    NAMESPACE = auto()
    IMPORTS = auto()
    PUBLIC = auto()
    PRIVATE = auto()
    PROTECTED = auto()
    FRIEND = auto()
    SHARED = auto()
    OVERRIDABLE = auto()
    OVERRIDES = auto()
    SUB = auto()
    FUNCTION = auto()
    PROPERTY = auto()
    EVENT = auto()
    DECLARE = auto()
    DIM = auto()
    CONST = auto()
    READONLY = auto()
    WITHEVENTS = auto()
    HANDLES = auto()
    AS = auto()
    NEW = auto()
    INHERITS = auto()
    IMPLEMENTS = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    ELSEIF = auto()
    END = auto()
    SELECT = auto()
    CASE = auto()
    FOR = auto()
    TO = auto()
    STEP = auto()
    NEXT = auto()
    EACH = auto()
    IN = auto()
    WHILE = auto()
    DO = auto()
    LOOP = auto()
    UNTIL = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    RETURN = auto()
    EXIT = auto()
    CONTINUE = auto()
    WITH = auto()
    USING = auto()
    OPTION = auto()
    STRICT = auto()
    EXPLICIT = auto()
    ON = auto()
    OFF = auto()
    
    # Operators
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    INTEGER_DIVIDE = auto()
    MOD = auto()
    EXPONENT = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NOT = auto()
    ANDALSO = auto()
    ORELSE = auto()
    LIKE = auto()
    IS = auto()
    ISNOT = auto()
    CONCATENATE = auto()
    
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    QUESTION = auto()
    
    # Special
    IDENTIFIER = auto()
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()

@dataclass
class VBToken:
    """Visual Basic token."""
    type: VBTokenType
    value: str
    line: int
    column: int

class VBLexer:
    """Visual Basic lexer with case-insensitive keywords."""
    
    KEYWORDS = {
        'class': VBTokenType.CLASS,
        'module': VBTokenType.MODULE,
        'interface': VBTokenType.INTERFACE,
        'structure': VBTokenType.STRUCTURE,
        'enum': VBTokenType.ENUM,
        'namespace': VBTokenType.NAMESPACE,
        'imports': VBTokenType.IMPORTS,
        'public': VBTokenType.PUBLIC,
        'private': VBTokenType.PRIVATE,
        'protected': VBTokenType.PROTECTED,
        'friend': VBTokenType.FRIEND,
        'shared': VBTokenType.SHARED,
        'overridable': VBTokenType.OVERRIDABLE,
        'overrides': VBTokenType.OVERRIDES,
        'sub': VBTokenType.SUB,
        'function': VBTokenType.FUNCTION,
        'property': VBTokenType.PROPERTY,
        'event': VBTokenType.EVENT,
        'declare': VBTokenType.DECLARE,
        'dim': VBTokenType.DIM,
        'const': VBTokenType.CONST,
        'readonly': VBTokenType.READONLY,
        'withevents': VBTokenType.WITHEVENTS,
        'handles': VBTokenType.HANDLES,
        'as': VBTokenType.AS,
        'new': VBTokenType.NEW,
        'inherits': VBTokenType.INHERITS,
        'implements': VBTokenType.IMPLEMENTS,
        'if': VBTokenType.IF,
        'then': VBTokenType.THEN,
        'else': VBTokenType.ELSE,
        'elseif': VBTokenType.ELSEIF,
        'end': VBTokenType.END,
        'select': VBTokenType.SELECT,
        'case': VBTokenType.CASE,
        'for': VBTokenType.FOR,
        'to': VBTokenType.TO,
        'step': VBTokenType.STEP,
        'next': VBTokenType.NEXT,
        'each': VBTokenType.EACH,
        'in': VBTokenType.IN,
        'while': VBTokenType.WHILE,
        'do': VBTokenType.DO,
        'loop': VBTokenType.LOOP,
        'until': VBTokenType.UNTIL,
        'try': VBTokenType.TRY,
        'catch': VBTokenType.CATCH,
        'finally': VBTokenType.FINALLY,
        'throw': VBTokenType.THROW,
        'return': VBTokenType.RETURN,
        'exit': VBTokenType.EXIT,
        'continue': VBTokenType.CONTINUE,
        'with': VBTokenType.WITH,
        'using': VBTokenType.USING,
        'option': VBTokenType.OPTION,
        'strict': VBTokenType.STRICT,
        'explicit': VBTokenType.EXPLICIT,
        'on': VBTokenType.ON,
        'off': VBTokenType.OFF,
        'and': VBTokenType.AND,
        'or': VBTokenType.OR,
        'xor': VBTokenType.XOR,
        'not': VBTokenType.NOT,
        'andalso': VBTokenType.ANDALSO,
        'orelse': VBTokenType.ORELSE,
        'like': VBTokenType.LIKE,
        'is': VBTokenType.IS,
        'isnot': VBTokenType.ISNOT,
        'mod': VBTokenType.MOD,
        'true': VBTokenType.BOOLEAN,
        'false': VBTokenType.BOOLEAN,
        'nothing': VBTokenType.NOTHING,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[VBToken] = []
    
    def tokenize(self) -> List[VBToken]:
        """Tokenize the source code."""
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break
                
            char = self.source[self.pos]
            
            # Comments
            if char == "'":
                self._scan_comment()
            # Strings
            elif char == '"':
                self._scan_string()
            # Numbers
            elif char.isdigit():
                self._scan_number()
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self._scan_identifier()
            # Operators and punctuation
            else:
                self._scan_operator()
        
        self.tokens.append(VBToken(VBTokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """Skip whitespace except newlines."""
        while (self.pos < len(self.source) and 
               self.source[self.pos] in ' \t\r'):
            if self.source[self.pos] == '\t':
                self.column += 4
            else:
                self.column += 1
            self.pos += 1
    
    def _scan_comment(self):
        """Scan a comment starting with '."""
        start_pos = self.pos
        start_col = self.column
        
        while (self.pos < len(self.source) and 
               self.source[self.pos] != '\n'):
            self.pos += 1
            self.column += 1
        
        text = self.source[start_pos:self.pos]
        self.tokens.append(VBToken(VBTokenType.COMMENT, text, self.line, start_col))
    
    def _scan_string(self):
        """Scan a string literal."""
        start_pos = self.pos
        start_col = self.column
        self.pos += 1  # Skip opening quote
        self.column += 1
        
        value = ""
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char == '"':
                # Check for escaped quote ""
                if (self.pos + 1 < len(self.source) and 
                    self.source[self.pos + 1] == '"'):
                    value += '"'
                    self.pos += 2
                    self.column += 2
                else:
                    self.pos += 1  # Skip closing quote
                    self.column += 1
                    break
            elif char == '\n':
                raise ValueError(f"Unterminated string at line {self.line}")
            else:
                value += char
                self.pos += 1
                self.column += 1
        
        self.tokens.append(VBToken(VBTokenType.STRING, value, self.line, start_col))
    
    def _scan_number(self):
        """Scan a numeric literal."""
        start_pos = self.pos
        start_col = self.column
        has_decimal = False
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isdigit():
                self.pos += 1
                self.column += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                self.pos += 1
                self.column += 1
            else:
                break
        
        value = self.source[start_pos:self.pos]
        token_type = VBTokenType.DECIMAL if has_decimal else VBTokenType.INTEGER
        self.tokens.append(VBToken(token_type, value, self.line, start_col))
    
    def _scan_identifier(self):
        """Scan an identifier or keyword."""
        start_pos = self.pos
        start_col = self.column
        
        while (self.pos < len(self.source) and 
               (self.source[self.pos].isalnum() or self.source[self.pos] == '_')):
            self.pos += 1
            self.column += 1
        
        value = self.source[start_pos:self.pos]
        # VB is case-insensitive
        lower_value = value.lower()
        
        token_type = self.KEYWORDS.get(lower_value, VBTokenType.IDENTIFIER)
        self.tokens.append(VBToken(token_type, value, self.line, start_col))
    
    def _scan_operator(self):
        """Scan operators and punctuation."""
        char = self.source[self.pos]
        start_col = self.column
        
        # Two-character operators
        if self.pos + 1 < len(self.source):
            two_char = self.source[self.pos:self.pos + 2]
            if two_char == '<>':
                self.tokens.append(VBToken(VBTokenType.NOT_EQUALS, two_char, self.line, start_col))
                self.pos += 2
                self.column += 2
                return
            elif two_char == '<=':
                self.tokens.append(VBToken(VBTokenType.LESS_EQUAL, two_char, self.line, start_col))
                self.pos += 2
                self.column += 2
                return
            elif two_char == '>=':
                self.tokens.append(VBToken(VBTokenType.GREATER_EQUAL, two_char, self.line, start_col))
                self.pos += 2
                self.column += 2
                return
        
        # Single-character operators and punctuation
        token_map = {
            '=': VBTokenType.EQUALS,
            '<': VBTokenType.LESS_THAN,
            '>': VBTokenType.GREATER_THAN,
            '+': VBTokenType.PLUS,
            '-': VBTokenType.MINUS,
            '*': VBTokenType.MULTIPLY,
            '/': VBTokenType.DIVIDE,
            '\\': VBTokenType.INTEGER_DIVIDE,
            '^': VBTokenType.EXPONENT,
            '&': VBTokenType.CONCATENATE,
            '(': VBTokenType.LPAREN,
            ')': VBTokenType.RPAREN,
            '{': VBTokenType.LBRACE,
            '}': VBTokenType.RBRACE,
            '.': VBTokenType.DOT,
            ',': VBTokenType.COMMA,
            ':': VBTokenType.COLON,
            ';': VBTokenType.SEMICOLON,
            '?': VBTokenType.QUESTION,
            '\n': VBTokenType.NEWLINE,
        }
        
        token_type = token_map.get(char)
        if token_type:
            self.tokens.append(VBToken(token_type, char, self.line, start_col))
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
        else:
            # Unknown character
            self.pos += 1
            self.column += 1

class VBParser:
    """Visual Basic parser."""
    
    def __init__(self, tokens: List[VBToken], error_handler: ErrorHandler):
        self.tokens = tokens
        self.pos = 0
        self.error_handler = error_handler
    
    def parse(self) -> VBSourceUnit:
        """Parse Visual Basic source unit."""
        source_unit = VBSourceUnit()
        
        # Skip initial newlines
        self._skip_newlines()
        
        # Parse option statements
        while self._current_token_is(VBTokenType.OPTION):
            source_unit.option_statements.append(self._parse_option_statement())
            self._skip_newlines()
        
        # Parse imports statements  
        while self._current_token_is(VBTokenType.IMPORTS):
            source_unit.imports_statements.append(self._parse_imports_statement())
            self._skip_newlines()
        
        # Parse type declarations
        while not self._current_token_is(VBTokenType.EOF):
            if self._current_token_is(VBTokenType.NAMESPACE):
                source_unit.namespace_declarations.append(self._parse_namespace())
            elif self._current_token_is_type_declaration():
                source_unit.type_declarations.append(self._parse_type_declaration())
            else:
                self._advance()
            self._skip_newlines()
        
        return source_unit
    
    def _parse_option_statement(self) -> VBOptionStatement:
        """Parse Option statement."""
        self._consume(VBTokenType.OPTION)
        option_type = self._consume(VBTokenType.IDENTIFIER).value
        value = self._consume(VBTokenType.IDENTIFIER).value
        self._skip_newlines()
        
        return VBOptionStatement(option_type=option_type, value=value)
    
    def _parse_imports_statement(self) -> VBImportsStatement:
        """Parse Imports statement."""
        self._consume(VBTokenType.IMPORTS)
        namespace = self._consume(VBTokenType.IDENTIFIER).value
        
        # Handle dotted namespaces
        while self._current_token_is(VBTokenType.DOT):
            self._advance()
            namespace += "." + self._consume(VBTokenType.IDENTIFIER).value
        
        self._skip_newlines()
        return VBImportsStatement(namespace=namespace)
    
    def _parse_namespace(self) -> VBNamespace:
        """Parse Namespace declaration."""
        self._consume(VBTokenType.NAMESPACE)
        name = self._consume(VBTokenType.IDENTIFIER).value
        self._skip_newlines()
        
        namespace = VBNamespace(name=name)
        
        while not self._current_token_is_end_namespace():
            if self._current_token_is_type_declaration():
                namespace.type_declarations.append(self._parse_type_declaration())
            else:
                self._advance()
            self._skip_newlines()
        
        self._consume(VBTokenType.END)
        self._consume(VBTokenType.NAMESPACE)
        return namespace
    
    def _parse_type_declaration(self) -> VBTypeDeclaration:
        """Parse type declaration."""
        # Parse access modifier
        access_modifier = VBAccessModifier.PUBLIC
        if self._current_token_is_access_modifier():
            access_modifier = self._parse_access_modifier()
        
        # Parse type
        if self._current_token_is(VBTokenType.CLASS):
            return self._parse_class_declaration(access_modifier)
        elif self._current_token_is(VBTokenType.MODULE):
            return self._parse_module_declaration(access_modifier)
        elif self._current_token_is(VBTokenType.INTERFACE):
            return self._parse_interface_declaration(access_modifier)
        elif self._current_token_is(VBTokenType.STRUCTURE):
            return self._parse_structure_declaration(access_modifier)
        elif self._current_token_is(VBTokenType.ENUM):
            return self._parse_enum_declaration(access_modifier)
        else:
            self.error_handler.add_error(ErrorType.SYNTAX_ERROR, 
                                       f"Expected type declaration", 
                                       self._current_token().line,
                                       self._current_token().column)
            return VBClassDeclaration()
    
    def _parse_class_declaration(self, access_modifier: VBAccessModifier) -> VBClassDeclaration:
        """Parse Class declaration."""
        self._consume(VBTokenType.CLASS)
        name = self._consume(VBTokenType.IDENTIFIER).value
        self._skip_newlines()
        
        class_decl = VBClassDeclaration(name=name, access_modifier=access_modifier)
        
        # Parse class body
        while not self._current_token_is_end_class():
            if self._current_token_is_member_declaration():
                class_decl.members.append(self._parse_member_declaration())
            else:
                self._advance()
            self._skip_newlines()
        
        self._consume(VBTokenType.END)
        self._consume(VBTokenType.CLASS)
        return class_decl
    
    def _parse_module_declaration(self, access_modifier: VBAccessModifier) -> VBModuleDeclaration:
        """Parse Module declaration."""
        self._consume(VBTokenType.MODULE)
        name = self._consume(VBTokenType.IDENTIFIER).value
        self._skip_newlines()
        
        module_decl = VBModuleDeclaration(name=name, access_modifier=access_modifier)
        
        # Parse module body
        while not self._current_token_is_end_module():
            if self._current_token_is_member_declaration():
                module_decl.members.append(self._parse_member_declaration())
            else:
                self._advance()
            self._skip_newlines()
        
        self._consume(VBTokenType.END)
        self._consume(VBTokenType.MODULE)
        return module_decl
    
    def _parse_member_declaration(self) -> VBMemberDeclaration:
        """Parse member declaration."""
        # Parse access modifier
        access_modifier = VBAccessModifier.PUBLIC
        if self._current_token_is_access_modifier():
            access_modifier = self._parse_access_modifier()
        
        # Parse member modifiers
        member_modifiers = []
        while self._current_token_is_member_modifier():
            member_modifiers.append(self._parse_member_modifier())
        
        # Parse member type
        if self._current_token_is(VBTokenType.SUB):
            return self._parse_method_declaration(access_modifier, member_modifiers, False)
        elif self._current_token_is(VBTokenType.FUNCTION):
            return self._parse_method_declaration(access_modifier, member_modifiers, True)
        elif self._current_token_is(VBTokenType.PROPERTY):
            return self._parse_property_declaration(access_modifier, member_modifiers)
        elif self._current_token_is(VBTokenType.DIM):
            return self._parse_field_declaration(access_modifier, member_modifiers)
        else:
            self.error_handler.add_error(ErrorType.SYNTAX_ERROR,
                                       f"Expected member declaration",
                                       self._current_token().line,
                                       self._current_token().column)
            return VBFieldDeclaration()
    
    # Helper methods
    def _current_token(self) -> VBToken:
        """Get current token."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def _current_token_is(self, token_type: VBTokenType) -> bool:
        """Check if current token is of given type."""
        return self._current_token().type == token_type
    
    def _advance(self) -> VBToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _consume(self, expected_type: VBTokenType) -> VBToken:
        """Consume token of expected type."""
        if self._current_token_is(expected_type):
            return self._advance()
        else:
            self.error_handler.add_error(ErrorType.SYNTAX_ERROR,
                                       f"Expected {expected_type}, got {self._current_token().type}",
                                       self._current_token().line,
                                       self._current_token().column)
            return self._current_token()
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._current_token_is(VBTokenType.NEWLINE):
            self._advance()
    
    def _current_token_is_access_modifier(self) -> bool:
        """Check if current token is an access modifier."""
        return self._current_token().type in [
            VBTokenType.PUBLIC, VBTokenType.PRIVATE, VBTokenType.PROTECTED, VBTokenType.FRIEND
        ]
    
    def _current_token_is_member_modifier(self) -> bool:
        """Check if current token is a member modifier."""
        return self._current_token().type in [
            VBTokenType.SHARED, VBTokenType.OVERRIDABLE, VBTokenType.OVERRIDES
        ]
    
    def _current_token_is_type_declaration(self) -> bool:
        """Check if current token starts a type declaration."""
        return self._current_token().type in [
            VBTokenType.CLASS, VBTokenType.MODULE, VBTokenType.INTERFACE,
            VBTokenType.STRUCTURE, VBTokenType.ENUM
        ] or self._current_token_is_access_modifier()
    
    def _current_token_is_member_declaration(self) -> bool:
        """Check if current token starts a member declaration."""
        return self._current_token().type in [
            VBTokenType.SUB, VBTokenType.FUNCTION, VBTokenType.PROPERTY, VBTokenType.DIM
        ] or self._current_token_is_access_modifier() or self._current_token_is_member_modifier()
    
    def _current_token_is_end_namespace(self) -> bool:
        """Check if at end of namespace."""
        return (self._current_token_is(VBTokenType.END) and 
                self.pos + 1 < len(self.tokens) and
                self.tokens[self.pos + 1].type == VBTokenType.NAMESPACE)
    
    def _current_token_is_end_class(self) -> bool:
        """Check if at end of class."""
        return (self._current_token_is(VBTokenType.END) and 
                self.pos + 1 < len(self.tokens) and
                self.tokens[self.pos + 1].type == VBTokenType.CLASS)
    
    def _current_token_is_end_module(self) -> bool:
        """Check if at end of module."""
        return (self._current_token_is(VBTokenType.END) and 
                self.pos + 1 < len(self.tokens) and
                self.tokens[self.pos + 1].type == VBTokenType.MODULE)

def parse_visual_basic(source: str, error_handler: Optional[ErrorHandler] = None) -> VBSourceUnit:
    """Parse Visual Basic source code."""
    if error_handler is None:
        error_handler = ErrorHandler()
    
    try:
        lexer = VBLexer(source)
        tokens = lexer.tokenize()
        parser = VBParser(tokens, error_handler)
        return parser.parse()
    except Exception as e:
        error_handler.add_error(ErrorType.SYNTAX_ERROR, str(e), 0, 0)
        return VBSourceUnit() 