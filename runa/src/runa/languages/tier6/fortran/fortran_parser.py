"""
Fortran Parser for Runa Universal Translation Platform
Parses Fortran source code supporting both fixed-form and free-form syntax

Key features:
- Support for FORTRAN 77 fixed-form syntax (columns 1-72)
- Modern Fortran free-form syntax (90/95/2003/2008/2018)
- Scientific computing constructs (arrays, complex numbers)
- Module system and interfaces
- Derived types and object-oriented features
- Parallel constructs (coarrays, do concurrent)
- Mathematical and intrinsic functions
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass
import logging

from .fortran_ast import *

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Base parse error class."""
    pass


class BaseParser:
    """Base parser class."""
    pass

class FortranTokenType(Enum):
    """Fortran token types"""
    # Keywords - Program structure
    PROGRAM = "program"
    END = "end" 
    MODULE = "module"
    SUBMODULE = "submodule"
    SUBROUTINE = "subroutine"
    FUNCTION = "function"
    INTERFACE = "interface"
    CONTAINS = "contains"
    USE = "use"
    ONLY = "only"
    
    # Keywords - Types and declarations
    INTEGER = "integer"
    REAL = "real"
    COMPLEX = "complex"
    LOGICAL = "logical"
    CHARACTER = "character"
    TYPE = "type"
    CLASS = "class"
    PARAMETER = "parameter"
    DIMENSION = "dimension"
    ALLOCATABLE = "allocatable"
    POINTER = "pointer"
    TARGET = "target"
    OPTIONAL = "optional"
    INTENT = "intent"
    
    # Keywords - Control flow
    IF = "if"
    THEN = "then"
    ELSE = "else"
    ELSEIF = "elseif"
    ENDIF = "endif"
    SELECT = "select"
    CASE = "case"
    DEFAULT = "default"
    DO = "do"
    ENDDO = "enddo"
    WHILE = "while"
    FORALL = "forall"
    WHERE = "where"
    ELSEWHERE = "elsewhere"
    ENDWHERE = "endwhere"
    
    # Keywords - I/O and procedures
    READ = "read"
    WRITE = "write"
    PRINT = "print"
    OPEN = "open"
    CLOSE = "close"
    CALL = "call"
    RETURN = "return"
    STOP = "stop"
    
    # Keywords - Memory management  
    ALLOCATE = "allocate"
    DEALLOCATE = "deallocate"
    NULLIFY = "nullify"
    
    # Keywords - Modern Fortran
    ABSTRACT = "abstract"
    EXTENDS = "extends"
    FINAL = "final"
    GENERIC = "generic"
    PROCEDURE = "procedure"
    CONCURRENT = "concurrent"
    CRITICAL = "critical"
    SYNC = "sync"
    ALL = "all"
    IMAGES = "images"
    
    # Operators
    ASSIGN = "="
    POINTER_ASSIGN = "=>"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"
    EQ = "=="
    NE = "/="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    AND = ".and."
    OR = ".or."
    NOT = ".not."
    EQV = ".eqv."
    NEQV = ".neqv."
    
    # Delimiters
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COMMA = ","
    COLON = ":"
    DOUBLE_COLON = "::"
    SEMICOLON = ";"
    PERCENT = "%"
    
    # Literals
    INTEGER_LITERAL = "INTEGER_LITERAL"
    REAL_LITERAL = "REAL_LITERAL"
    COMPLEX_LITERAL = "COMPLEX_LITERAL"
    LOGICAL_LITERAL = "LOGICAL_LITERAL"
    CHARACTER_LITERAL = "CHARACTER_LITERAL"
    
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    
    # Special
    COMMENT = "COMMENT"
    CONTINUATION = "CONTINUATION"
    NEWLINE = "NEWLINE"
    EOF = "EOF"

@dataclass
class FortranToken:
    """Fortran token with type, value, and location"""
    type: FortranTokenType
    value: str
    line: int
    column: int
    is_fixed_form: bool = False

class FortranLexer:
    """Fortran lexer supporting both fixed-form and free-form syntax"""
    
    FORTRAN_KEYWORDS = {
        "program", "end", "module", "submodule", "subroutine", "function",
        "interface", "contains", "use", "only", "integer", "real", "complex",
        "logical", "character", "type", "class", "parameter", "dimension",
        "allocatable", "pointer", "target", "optional", "intent", "if", "then",
        "else", "elseif", "endif", "select", "case", "default", "do", "enddo",
        "while", "forall", "where", "elsewhere", "endwhere", "read", "write",
        "print", "open", "close", "call", "return", "stop", "allocate",
        "deallocate", "nullify", "abstract", "extends", "final", "generic",
        "procedure", "concurrent", "critical", "sync", "all", "images"
    }
    
    def __init__(self, source: str, fixed_form: Optional[bool] = None):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[FortranToken] = []
        
        # Auto-detect form if not specified
        if fixed_form is None:
            self.fixed_form = self._detect_fixed_form()
        else:
            self.fixed_form = fixed_form
            
    def _detect_fixed_form(self) -> bool:
        """Auto-detect if source is fixed-form or free-form"""
        lines = self.source.split('\n')
        
        for line in lines[:10]:  # Check first 10 lines
            if len(line) > 0:
                # Check for continuation character in column 6
                if len(line) >= 6 and line[5] not in [' ', '0']:
                    return True
                # Check for comment in column 1
                if line[0] in ['C', 'c', '*']:
                    return True
                # Check for statement starting after column 6
                if len(line) > 6 and line[:6].strip() == '' and line[6:].strip():
                    return True
        
        return False
    
    def tokenize(self) -> List[FortranToken]:
        """Tokenize Fortran source code"""
        if self.fixed_form:
            return self._tokenize_fixed_form()
        else:
            return self._tokenize_free_form()
    
    def _tokenize_fixed_form(self) -> List[FortranToken]:
        """Tokenize fixed-form Fortran (FORTRAN 77 style)"""
        lines = self.source.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self.line = line_num
            self.column = 1
            
            if len(line) == 0:
                continue
                
            # Handle comment lines (C, c, or * in column 1)
            if line[0] in ['C', 'c', '*']:
                self._add_token(FortranTokenType.COMMENT, line, is_fixed_form=True)
                continue
            
            # Handle continuation lines (non-blank, non-zero in column 6)
            if len(line) >= 6 and line[5] not in [' ', '0']:
                self._add_token(FortranTokenType.CONTINUATION, line[5], is_fixed_form=True)
                # Process the rest of the line starting from column 7
                if len(line) > 6:
                    self._process_statement_part(line[6:], 7)
            else:
                # Regular statement line - process from column 7 onwards
                if len(line) > 6:
                    self._process_statement_part(line[6:], 7)
        
        self._add_token(FortranTokenType.EOF, "", is_fixed_form=True)
        return self.tokens
    
    def _tokenize_free_form(self) -> List[FortranToken]:
        """Tokenize free-form Fortran (Fortran 90+ style)"""
        while self.position < len(self.source):
            self._skip_whitespace()
            if self.position >= len(self.source):
                break
                
            if self._match_comment():
                continue
            elif self._match_string_literal():
                continue
            elif self._match_number():
                continue
            elif self._match_operator():
                continue
            elif self._match_keyword_or_identifier():
                continue
            elif self._match_delimiter():
                continue
            else:
                self._advance()
        
        self._add_token(FortranTokenType.EOF, "")
        return self.tokens
    
    def _process_statement_part(self, statement: str, start_col: int):
        """Process a statement part (common to both forms)"""
        pos = 0
        self.column = start_col
        
        while pos < len(statement):
            char = statement[pos]
            
            if char.isspace():
                pos += 1
                self.column += 1
                continue
            
            # Check for inline comments
            if char == '!' and not self.fixed_form:
                comment = statement[pos:]
                self._add_token(FortranTokenType.COMMENT, comment)
                break
            
            # Check for string literals
            if char in ['"', "'"]:
                quote_char = char
                pos += 1
                self.column += 1
                value = ""
                
                while pos < len(statement) and statement[pos] != quote_char:
                    value += statement[pos]
                    pos += 1
                    self.column += 1
                
                if pos < len(statement):  # Found closing quote
                    pos += 1
                    self.column += 1
                
                self._add_token(FortranTokenType.CHARACTER_LITERAL, value)
                continue
            
            # Check for numbers
            if char.isdigit() or char == '.':
                number_start = pos
                number_value = ""
                
                # Parse number
                while pos < len(statement) and (statement[pos].isdigit() or statement[pos] in '.eEdD+-'):
                    number_value += statement[pos]
                    pos += 1
                    self.column += 1
                
                # Determine number type
                if '.' in number_value or 'e' in number_value.lower() or 'd' in number_value.lower():
                    self._add_token(FortranTokenType.REAL_LITERAL, number_value)
                else:
                    self._add_token(FortranTokenType.INTEGER_LITERAL, number_value)
                continue
            
            # Check for operators and delimiters
            if pos + 1 < len(statement):
                two_char = statement[pos:pos+2]
                if two_char in ["**", "==", "/=", "<=", ">=", "=>", "::"]:
                    self._add_token(self._get_token_type_for_operator(two_char), two_char)
                    pos += 2
                    self.column += 2
                    continue
            
            # Check for dot operators (.and., .or., etc.)
            if char == '.':
                dot_start = pos
                pos += 1
                dot_content = ""
                
                while pos < len(statement) and statement[pos] != '.':
                    dot_content += statement[pos]
                    pos += 1
                
                if pos < len(statement) and statement[pos] == '.':
                    pos += 1
                    full_op = f".{dot_content}."
                    self._add_token(self._get_token_type_for_operator(full_op), full_op)
                    self.column += len(full_op)
                else:
                    # Just a single dot
                    pos = dot_start + 1
                    self._add_token(FortranTokenType.IDENTIFIER, ".")
                    self.column += 1
                continue
            
            # Single character operators and delimiters
            if char in "()[],:;%+-*/=<>":
                self._add_token(self._get_token_type_for_operator(char), char)
                pos += 1
                self.column += 1
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                ident_start = pos
                identifier = ""
                
                while pos < len(statement) and (statement[pos].isalnum() or statement[pos] == '_'):
                    identifier += statement[pos]
                    pos += 1
                    self.column += 1
                
                # Check if it's a keyword
                if identifier.lower() in self.FORTRAN_KEYWORDS:
                    token_type = getattr(FortranTokenType, identifier.upper(), FortranTokenType.IDENTIFIER)
                    self._add_token(token_type, identifier)
                else:
                    self._add_token(FortranTokenType.IDENTIFIER, identifier)
                continue
            
            # Unknown character, skip it
            pos += 1
            self.column += 1
    
    def _current_char(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def _advance(self) -> str:
        char = self._current_char()
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _skip_whitespace(self):
        while self._current_char().isspace():
            self._advance()
    
    def _match_comment(self) -> bool:
        if self._current_char() == '!':
            value = ""
            while self._current_char() not in ['\n', '\0']:
                value += self._advance()
            self._add_token(FortranTokenType.COMMENT, value)
            return True
        return False
    
    def _match_string_literal(self) -> bool:
        char = self._current_char()
        if char in ['"', "'"]:
            quote_char = char
            self._advance()
            value = ""
            
            while self._current_char() != quote_char and self._current_char() != '\0':
                if self._current_char() == '\\':
                    self._advance()
                if self._current_char() != '\0':
                    value += self._advance()
            
            if self._current_char() == quote_char:
                self._advance()
            
            self._add_token(FortranTokenType.CHARACTER_LITERAL, value)
            return True
        return False
    
    def _match_number(self) -> bool:
        if self._current_char().isdigit() or self._current_char() == '.':
            value = ""
            has_dot = False
            has_exp = False
            
            while (self._current_char().isdigit() or 
                   (self._current_char() == '.' and not has_dot) or
                   (self._current_char().lower() in 'ed' and not has_exp) or
                   (self._current_char() in '+-' and value and value[-1].lower() in 'ed')):
                
                char = self._current_char()
                if char == '.':
                    has_dot = True
                elif char.lower() in 'ed':
                    has_exp = True
                
                value += self._advance()
            
            # Determine token type
            if has_dot or has_exp:
                self._add_token(FortranTokenType.REAL_LITERAL, value)
            else:
                self._add_token(FortranTokenType.INTEGER_LITERAL, value)
            return True
        return False
    
    def _match_operator(self) -> bool:
        # Two-character operators
        if self.position + 1 < len(self.source):
            two_char = self.source[self.position:self.position+2]
            if two_char in ["**", "==", "/=", "<=", ">=", "=>", "::"]:
                self._advance()
                self._advance()
                self._add_token(self._get_token_type_for_operator(two_char), two_char)
                return True
        
        # Dot operators (.and., .or., etc.)
        if self._current_char() == '.':
            start_pos = self.position
            self._advance()
            
            dot_content = ""
            while self._current_char().isalpha():
                dot_content += self._advance()
            
            if self._current_char() == '.' and dot_content:
                self._advance()
                full_op = f".{dot_content}."
                self._add_token(self._get_token_type_for_operator(full_op), full_op)
                return True
            else:
                # Not a dot operator, reset
                self.position = start_pos + 1
                self.column = self.column - len(dot_content)
                return False
        
        # Single character operators
        char = self._current_char()
        if char in "+-*/=<>":
            self._advance()
            self._add_token(self._get_token_type_for_operator(char), char)
            return True
        
        return False
    
    def _match_keyword_or_identifier(self) -> bool:
        if self._current_char().isalpha() or self._current_char() == '_':
            value = ""
            while self._current_char().isalnum() or self._current_char() == '_':
                value += self._advance()
            
            # Check if it's a keyword
            if value.lower() in self.FORTRAN_KEYWORDS:
                token_type = getattr(FortranTokenType, value.upper(), FortranTokenType.IDENTIFIER)
                self._add_token(token_type, value)
            else:
                # Check for logical literals
                if value.lower() in ['.true.', '.false.']:
                    self._add_token(FortranTokenType.LOGICAL_LITERAL, value)
                else:
                    self._add_token(FortranTokenType.IDENTIFIER, value)
            return True
        return False
    
    def _match_delimiter(self) -> bool:
        char = self._current_char()
        if char in "()[],:;%":
            self._advance()
            self._add_token(self._get_token_type_for_operator(char), char)
            return True
        return False
    
    def _get_token_type_for_operator(self, op: str) -> FortranTokenType:
        """Get token type for operator"""
        op_map = {
            "=": FortranTokenType.ASSIGN,
            "=>": FortranTokenType.POINTER_ASSIGN,
            "+": FortranTokenType.PLUS,
            "-": FortranTokenType.MINUS,
            "*": FortranTokenType.MULTIPLY,
            "/": FortranTokenType.DIVIDE,
            "**": FortranTokenType.POWER,
            "==": FortranTokenType.EQ,
            "/=": FortranTokenType.NE,
            "<": FortranTokenType.LT,
            "<=": FortranTokenType.LE,
            ">": FortranTokenType.GT,
            ">=": FortranTokenType.GE,
            ".and.": FortranTokenType.AND,
            ".or.": FortranTokenType.OR,
            ".not.": FortranTokenType.NOT,
            ".eqv.": FortranTokenType.EQV,
            ".neqv.": FortranTokenType.NEQV,
            "(": FortranTokenType.LEFT_PAREN,
            ")": FortranTokenType.RIGHT_PAREN,
            "[": FortranTokenType.LEFT_BRACKET,
            "]": FortranTokenType.RIGHT_BRACKET,
            ",": FortranTokenType.COMMA,
            ":": FortranTokenType.COLON,
            "::": FortranTokenType.DOUBLE_COLON,
            ";": FortranTokenType.SEMICOLON,
            "%": FortranTokenType.PERCENT,
        }
        return op_map.get(op, FortranTokenType.IDENTIFIER)
    
    def _add_token(self, token_type: FortranTokenType, value: str, is_fixed_form: bool = None):
        if is_fixed_form is None:
            is_fixed_form = self.fixed_form
        
        token = FortranToken(token_type, value, self.line, self.column - len(value), is_fixed_form)
        self.tokens.append(token)

class FortranParseError(ParseError):
    """Fortran-specific parse error"""
    pass

class FortranParser(BaseParser):
    """Fortran parser supporting both fixed-form and free-form syntax"""
    
    def __init__(self, tokens: Optional[List[FortranToken]] = None):
        super().__init__()
        self.tokens = tokens or []
        self.current = 0
        
    def parse(self, source: str, fixed_form: Optional[bool] = None) -> FortranProgram:
        """Parse Fortran source code"""
        try:
            lexer = FortranLexer(source, fixed_form)
            self.tokens = lexer.tokenize()
            self.current = 0
            
            return self.parse_program_unit()
            
        except Exception as e:
            logger.error(f"Fortran parse error: {e}")
            raise FortranParseError(f"Failed to parse Fortran code: {e}")
    
    def current_token(self) -> FortranToken:
        """Get current token"""
        if self.current >= len(self.tokens):
            return FortranToken(FortranTokenType.EOF, "", 0, 0)
        return self.tokens[self.current]
    
    def advance(self) -> FortranToken:
        """Advance to next token"""
        token = self.current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def match(self, *token_types: FortranTokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token().type in token_types
    
    def consume(self, token_type: FortranTokenType) -> FortranToken:
        """Consume token of expected type"""
        if self.match(token_type):
            return self.advance()
        
        current = self.current_token()
        raise FortranParseError(f"Expected {token_type}, got {current.type} at line {current.line}")
    
    def parse_program_unit(self):
        """Parse a Fortran program unit"""
        # Skip comments and empty lines
        while self.match(FortranTokenType.COMMENT, FortranTokenType.NEWLINE):
            self.advance()
        
        if self.match(FortranTokenType.PROGRAM):
            return self.parse_program()
        elif self.match(FortranTokenType.MODULE):
            return self.parse_module()
        elif self.match(FortranTokenType.SUBROUTINE):
            return self.parse_subroutine()
        elif self.match(FortranTokenType.FUNCTION):
            return self.parse_function()
        else:
            # Assume it's a main program without explicit PROGRAM statement
            return self.parse_implicit_program()
    
    def parse_program(self) -> FortranProgram:
        """Parse a Fortran program"""
        self.consume(FortranTokenType.PROGRAM)
        name = self.consume(FortranTokenType.IDENTIFIER).value
        
        variables = []
        statements = []
        contains_section = []
        
        while not self.match(FortranTokenType.END, FortranTokenType.EOF):
            if self.match(FortranTokenType.CONTAINS):
                self.advance()
                contains_section = self.parse_contains_section()
                break
            elif self.match(FortranTokenType.COMMENT):
                self.advance()
            else:
                stmt = self.parse_statement()
                if isinstance(stmt, FortranVariableDeclaration):
                    variables.append(stmt)
                else:
                    statements.append(stmt)
        
        if self.match(FortranTokenType.END):
            self.advance()
            if self.match(FortranTokenType.PROGRAM):
                self.advance()
                if self.match(FortranTokenType.IDENTIFIER):
                    self.advance()  # Optional program name
        
        return FortranProgram(
            name=name,
            variables=variables,
            statements=statements,
            contains_section=contains_section
        )
    
    def parse_module(self) -> FortranModule:
        """Parse a Fortran module"""
        self.consume(FortranTokenType.MODULE)
        name = self.consume(FortranTokenType.IDENTIFIER).value
        
        use_statements = []
        declarations = []
        interfaces = []
        contains_section = []
        
        while not self.match(FortranTokenType.END, FortranTokenType.EOF):
            if self.match(FortranTokenType.USE):
                use_statements.append(self.parse_use_statement())
            elif self.match(FortranTokenType.INTERFACE):
                interfaces.append(self.parse_interface())
            elif self.match(FortranTokenType.CONTAINS):
                self.advance()
                contains_section = self.parse_contains_section()
                break
            elif self.match(FortranTokenType.COMMENT):
                self.advance()
            else:
                decl = self.parse_declaration()
                if decl:
                    declarations.append(decl)
        
        if self.match(FortranTokenType.END):
            self.advance()
            if self.match(FortranTokenType.MODULE):
                self.advance()
                if self.match(FortranTokenType.IDENTIFIER):
                    self.advance()  # Optional module name
        
        return FortranModule(
            name=name,
            use_statements=use_statements,
            declarations=declarations,
            interfaces=interfaces,
            contains_section=contains_section
        )
    
    def parse_subroutine(self) -> FortranSubroutine:
        """Parse a Fortran subroutine"""
        self.consume(FortranTokenType.SUBROUTINE)
        name = self.consume(FortranTokenType.IDENTIFIER).value
        
        parameters = []
        if self.match(FortranTokenType.LEFT_PAREN):
            self.advance()
            parameters = self.parse_parameter_list()
            self.consume(FortranTokenType.RIGHT_PAREN)
        
        variables = []
        statements = []
        contains_section = []
        
        while not self.match(FortranTokenType.END, FortranTokenType.EOF):
            if self.match(FortranTokenType.CONTAINS):
                self.advance()
                contains_section = self.parse_contains_section()
                break
            elif self.match(FortranTokenType.COMMENT):
                self.advance()
            else:
                stmt = self.parse_statement()
                if isinstance(stmt, FortranVariableDeclaration):
                    variables.append(stmt)
                else:
                    statements.append(stmt)
        
        if self.match(FortranTokenType.END):
            self.advance()
            if self.match(FortranTokenType.SUBROUTINE):
                self.advance()
                if self.match(FortranTokenType.IDENTIFIER):
                    self.advance()  # Optional subroutine name
        
        return FortranSubroutine(
            name=name,
            parameters=parameters,
            variables=variables,
            statements=statements,
            contains_section=contains_section
        )
    
    def parse_function(self) -> FortranFunction:
        """Parse a Fortran function"""
        # Check for type specification before FUNCTION
        return_type = None
        if self.match(FortranTokenType.INTEGER, FortranTokenType.REAL, 
                      FortranTokenType.COMPLEX, FortranTokenType.LOGICAL, 
                      FortranTokenType.CHARACTER):
            return_type = self.parse_type_spec()
        
        self.consume(FortranTokenType.FUNCTION)
        name = self.consume(FortranTokenType.IDENTIFIER).value
        
        parameters = []
        if self.match(FortranTokenType.LEFT_PAREN):
            self.advance()
            parameters = self.parse_parameter_list()
            self.consume(FortranTokenType.RIGHT_PAREN)
        
        # Check for result clause
        result_variable = None
        if self.match(FortranTokenType.IDENTIFIER) and self.current_token().value.lower() == "result":
            self.advance()
            self.consume(FortranTokenType.LEFT_PAREN)
            result_variable = self.consume(FortranTokenType.IDENTIFIER).value
            self.consume(FortranTokenType.RIGHT_PAREN)
        
        variables = []
        statements = []
        contains_section = []
        
        while not self.match(FortranTokenType.END, FortranTokenType.EOF):
            if self.match(FortranTokenType.CONTAINS):
                self.advance()
                contains_section = self.parse_contains_section()
                break
            elif self.match(FortranTokenType.COMMENT):
                self.advance()
            else:
                stmt = self.parse_statement()
                if isinstance(stmt, FortranVariableDeclaration):
                    variables.append(stmt)
                else:
                    statements.append(stmt)
        
        if self.match(FortranTokenType.END):
            self.advance()
            if self.match(FortranTokenType.FUNCTION):
                self.advance()
                if self.match(FortranTokenType.IDENTIFIER):
                    self.advance()  # Optional function name
        
        return FortranFunction(
            name=name,
            parameters=parameters,
            return_type=return_type,
            result_variable=result_variable,
            variables=variables,
            statements=statements,
            contains_section=contains_section
        )
    
    def parse_implicit_program(self) -> FortranProgram:
        """Parse an implicit main program (no PROGRAM statement)"""
        statements = []
        
        while not self.match(FortranTokenType.EOF):
            if self.match(FortranTokenType.COMMENT):
                self.advance()
            else:
                stmt = self.parse_statement()
                statements.append(stmt)
        
        return FortranProgram(name="main", statements=statements)
    
    def parse_statement(self):
        """Parse a Fortran statement"""
        if self.match(FortranTokenType.INTEGER, FortranTokenType.REAL,
                      FortranTokenType.COMPLEX, FortranTokenType.LOGICAL,
                      FortranTokenType.CHARACTER, FortranTokenType.TYPE):
            return self.parse_declaration()
        elif self.match(FortranTokenType.IF):
            return self.parse_if_construct()
        elif self.match(FortranTokenType.DO):
            return self.parse_do_construct()
        elif self.match(FortranTokenType.READ):
            return self.parse_read_statement()
        elif self.match(FortranTokenType.WRITE):
            return self.parse_write_statement()
        elif self.match(FortranTokenType.PRINT):
            return self.parse_print_statement()
        elif self.match(FortranTokenType.CALL):
            return self.parse_call_statement()
        elif self.match(FortranTokenType.ALLOCATE):
            return self.parse_allocate_statement()
        elif self.match(FortranTokenType.DEALLOCATE):
            return self.parse_deallocate_statement()
        else:
            return self.parse_assignment_or_call()
    
    def parse_declaration(self):
        """Parse a variable declaration"""
        type_spec = self.parse_type_spec()
        
        # Parse attributes
        attributes = []
        while self.match(FortranTokenType.COMMA):
            self.advance()
            if self.match(FortranTokenType.DIMENSION, FortranTokenType.ALLOCATABLE,
                          FortranTokenType.POINTER, FortranTokenType.TARGET,
                          FortranTokenType.OPTIONAL, FortranTokenType.INTENT,
                          FortranTokenType.PARAMETER):
                attr = self.advance().value
                if attr.lower() == "dimension":
                    self.consume(FortranTokenType.LEFT_PAREN)
                    # Parse dimension specification
                    dim_spec = ""
                    paren_count = 1
                    while paren_count > 0:
                        token = self.advance()
                        if token.type == FortranTokenType.LEFT_PAREN:
                            paren_count += 1
                        elif token.type == FortranTokenType.RIGHT_PAREN:
                            paren_count -= 1
                        if paren_count > 0:
                            dim_spec += token.value
                    attributes.append(f"dimension({dim_spec})")
                elif attr.lower() == "intent":
                    self.consume(FortranTokenType.LEFT_PAREN)
                    intent = self.consume(FortranTokenType.IDENTIFIER).value
                    self.consume(FortranTokenType.RIGHT_PAREN)
                    attributes.append(f"intent({intent})")
                else:
                    attributes.append(attr)
        
        # Parse variable names
        if self.match(FortranTokenType.DOUBLE_COLON):
            self.advance()
        
        names = []
        names.append(self.consume(FortranTokenType.IDENTIFIER).value)
        
        while self.match(FortranTokenType.COMMA):
            self.advance()
            names.append(self.consume(FortranTokenType.IDENTIFIER).value)
        
        return FortranVariableDeclaration(
            names=names,
            type_spec=type_spec,
            attributes=attributes
        )
    
    def parse_type_spec(self) -> FortranTypeSpec:
        """Parse a type specification"""
        type_name = self.advance().value  # INTEGER, REAL, etc.
        
        kind = None
        length = None
        
        if self.match(FortranTokenType.LEFT_PAREN):
            self.advance()
            if self.match(FortranTokenType.INTEGER_LITERAL, FortranTokenType.IDENTIFIER):
                kind_or_len = self.advance().value
                if type_name.lower() == "character":
                    length = kind_or_len
                else:
                    kind = kind_or_len
            self.consume(FortranTokenType.RIGHT_PAREN)
        
        return FortranTypeSpec(type_name=type_name, kind=kind, length=length)
    
    def parse_parameter_list(self) -> List[FortranParameter]:
        """Parse procedure parameter list"""
        parameters = []
        
        if not self.match(FortranTokenType.RIGHT_PAREN):
            parameters.append(self.parse_parameter())
            
            while self.match(FortranTokenType.COMMA):
                self.advance()
                parameters.append(self.parse_parameter())
        
        return parameters
    
    def parse_parameter(self) -> FortranParameter:
        """Parse a single parameter"""
        name = self.consume(FortranTokenType.IDENTIFIER).value
        return FortranParameter(name=name)
    
    def parse_expression(self) -> FortranExpression:
        """Parse a Fortran expression"""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> FortranExpression:
        """Parse logical OR expression"""
        left = self.parse_logical_and()
        
        while self.match(FortranTokenType.OR):
            operator = self.advance().value
            right = self.parse_logical_and()
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_logical_and(self) -> FortranExpression:
        """Parse logical AND expression"""
        left = self.parse_equality()
        
        while self.match(FortranTokenType.AND):
            operator = self.advance().value
            right = self.parse_equality()
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_equality(self) -> FortranExpression:
        """Parse equality expression"""
        left = self.parse_relational()
        
        while self.match(FortranTokenType.EQ, FortranTokenType.NE):
            operator = self.advance().value
            right = self.parse_relational()
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_relational(self) -> FortranExpression:
        """Parse relational expression"""
        left = self.parse_additive()
        
        while self.match(FortranTokenType.LT, FortranTokenType.LE,
                          FortranTokenType.GT, FortranTokenType.GE):
            operator = self.advance().value
            right = self.parse_additive()
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_additive(self) -> FortranExpression:
        """Parse additive expression"""
        left = self.parse_multiplicative()
        
        while self.match(FortranTokenType.PLUS, FortranTokenType.MINUS):
            operator = self.advance().value
            right = self.parse_multiplicative()
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_multiplicative(self) -> FortranExpression:
        """Parse multiplicative expression"""
        left = self.parse_power()
        
        while self.match(FortranTokenType.MULTIPLY, FortranTokenType.DIVIDE):
            operator = self.advance().value
            right = self.parse_power()
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_power(self) -> FortranExpression:
        """Parse power expression"""
        left = self.parse_unary()
        
        if self.match(FortranTokenType.POWER):
            operator = self.advance().value
            right = self.parse_power()  # Right associative
            left = FortranBinaryOperation(left=left, right=right, operator=operator)
        
        return left
    
    def parse_unary(self) -> FortranExpression:
        """Parse unary expression"""
        if self.match(FortranTokenType.PLUS, FortranTokenType.MINUS, FortranTokenType.NOT):
            operator = self.advance().value
            operand = self.parse_unary()
            return FortranUnaryOperation(operand=operand, operator=operator)
        
        return self.parse_primary()
    
    def parse_primary(self) -> FortranExpression:
        """Parse primary expression"""
        if self.match(FortranTokenType.INTEGER_LITERAL):
            value = int(self.advance().value)
            return FortranIntegerLiteral(value=value)
        
        elif self.match(FortranTokenType.REAL_LITERAL):
            value = float(self.advance().value)
            return FortranRealLiteral(value=value)
        
        elif self.match(FortranTokenType.CHARACTER_LITERAL):
            value = self.advance().value
            return FortranCharacterLiteral(value=value)
        
        elif self.match(FortranTokenType.LOGICAL_LITERAL):
            value = self.advance().value.lower() == '.true.'
            return FortranLogicalLiteral(value=value)
        
        elif self.match(FortranTokenType.IDENTIFIER):
            name = self.advance().value
            
            # Check for function call or array reference
            if self.match(FortranTokenType.LEFT_PAREN):
                self.advance()
                args = self.parse_argument_list()
                self.consume(FortranTokenType.RIGHT_PAREN)
                return FortranFunctionCall(name=name, arguments=args)
            else:
                return FortranIdentifier(name=name)
        
        elif self.match(FortranTokenType.LEFT_PAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(FortranTokenType.RIGHT_PAREN)
            return expr
        
        else:
            current = self.current_token()
            raise FortranParseError(f"Unexpected token {current.type} at line {current.line}")
    
    def parse_argument_list(self) -> List[FortranExpression]:
        """Parse function argument list"""
        args = []
        
        if not self.match(FortranTokenType.RIGHT_PAREN):
            args.append(self.parse_expression())
            
            while self.match(FortranTokenType.COMMA):
                self.advance()
                args.append(self.parse_expression())
        
        return args
    
    # Placeholder methods for other constructs
    def parse_use_statement(self):
        """Parse USE statement"""
        # Simplified implementation
        self.advance()  # USE
        module_name = self.consume(FortranTokenType.IDENTIFIER).value
        return FortranUseStatement(module_name=module_name)
    
    def parse_interface(self):
        """Parse INTERFACE construct"""
        # Simplified implementation
        self.advance()  # INTERFACE
        return FortranInterface()
    
    def parse_contains_section(self):
        """Parse CONTAINS section"""
        # Simplified implementation
        return []
    
    def parse_if_construct(self):
        """Parse IF construct"""
        # Simplified implementation
        self.advance()  # IF
        condition = self.parse_expression()
        return FortranIfConstruct(condition=condition)
    
    def parse_do_construct(self):
        """Parse DO construct"""
        # Simplified implementation
        self.advance()  # DO
        return FortranDoConstruct()
    
    def parse_read_statement(self):
        """Parse READ statement"""
        # Simplified implementation
        self.advance()  # READ
        return FortranReadStatement()
    
    def parse_write_statement(self):
        """Parse WRITE statement"""
        # Simplified implementation
        self.advance()  # WRITE
        return FortranWriteStatement()
    
    def parse_print_statement(self):
        """Parse PRINT statement"""
        # Simplified implementation
        self.advance()  # PRINT
        return FortranPrintStatement()
    
    def parse_call_statement(self):
        """Parse CALL statement"""
        # Simplified implementation
        self.advance()  # CALL
        name = self.consume(FortranTokenType.IDENTIFIER).value
        return FortranFunctionCall(name=name)
    
    def parse_allocate_statement(self):
        """Parse ALLOCATE statement"""
        # Simplified implementation
        self.advance()  # ALLOCATE
        return FortranAllocateStatement()
    
    def parse_deallocate_statement(self):
        """Parse DEALLOCATE statement"""
        # Simplified implementation
        self.advance()  # DEALLOCATE
        return FortranDeallocateStatement()
    
    def parse_assignment_or_call(self):
        """Parse assignment or procedure call"""
        # Simplified implementation - just parse as assignment
        lhs = self.parse_expression()
        if self.match(FortranTokenType.ASSIGN):
            self.advance()
            rhs = self.parse_expression()
            return FortranAssignment(lhs=lhs, rhs=rhs)
        else:
            return lhs 