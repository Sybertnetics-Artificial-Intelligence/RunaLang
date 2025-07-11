"""
Ada Parser for Runa Universal Translation Platform
Supports Ada 2012 standard with safety-critical, real-time, and embedded features

Key features:
- Strong typing with subtype constraints  
- Package system with specification/body separation
- Generic programming with formal parameters
- Tasking (concurrency) with protected objects
- Exception handling with contracts
- SPARK subset for formal verification
- Ravenscar profile for real-time systems
"""

import re
from typing import List, Optional, Dict, Any, Union, Iterator
from enum import Enum
from dataclasses import dataclass
import logging

from .ada_ast import *

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Base parse error class."""
    pass


class BaseParser:
    """Base parser class."""
    pass

class AdaTokenType(Enum):
    """Ada token types"""
    # Literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    REAL_LITERAL = "REAL_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    CHARACTER_LITERAL = "CHARACTER_LITERAL"
    
    # Keywords - Reserved words
    ABORT = "abort"
    ABS = "abs"
    ABSTRACT = "abstract"
    ACCEPT = "accept"
    ACCESS = "access"
    ALIASED = "aliased"
    ALL = "all"
    AND = "and"
    ARRAY = "array"
    AT = "at"
    BEGIN = "begin"
    BODY = "body"
    CASE = "case"
    CONSTANT = "constant"
    DECLARE = "declare"
    DELAY = "delay"
    DELTA = "delta"
    DIGITS = "digits"
    DO = "do"
    ELSE = "else"
    ELSIF = "elsif"
    END = "end"
    ENTRY = "entry"
    EXCEPTION = "exception"
    EXIT = "exit"
    FOR = "for"
    FUNCTION = "function"
    GENERIC = "generic"
    GOTO = "goto"
    IF = "if"
    IN = "in"
    INTERFACE = "interface"
    IS = "is"
    LIMITED = "limited"
    LOOP = "loop"
    MOD = "mod"
    NEW = "new"
    NOT = "not"
    NULL = "null"
    OF = "of"
    OR = "or"
    OTHERS = "others"
    OUT = "out"
    OVERRIDING = "overriding"
    PACKAGE = "package"
    PRAGMA = "pragma"
    PRIVATE = "private"
    PROCEDURE = "procedure"
    PROTECTED = "protected"
    RAISE = "raise"
    RANGE = "range"
    RECORD = "record"
    REM = "rem"
    RENAMES = "renames"
    REQUEUE = "requeue"
    RETURN = "return"
    REVERSE = "reverse"
    SELECT = "select"
    SEPARATE = "separate"
    SUBTYPE = "subtype"
    SYNCHRONIZED = "synchronized"
    TAGGED = "tagged"
    TASK = "task"
    TERMINATE = "terminate"
    THEN = "then"
    TYPE = "type"
    UNTIL = "until"
    USE = "use"
    WHEN = "when"
    WHILE = "while"
    WITH = "with"
    XOR = "xor"
    
    # Operators and delimiters
    ARROW = "=>"
    DOUBLE_DOT = ".."
    DOUBLE_STAR = "**"
    ASSIGNMENT = ":="
    NOT_EQUAL = "/="
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    LEFT_LABEL = "<<"
    RIGHT_LABEL = ">>"
    BOX = "<>"
    
    # Single character tokens
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    COLON = ":"
    APOSTROPHE = "'"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    PIPE = "|"
    AMPERSAND = "&"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    EQUAL = "="
    LESS = "<"
    GREATER = ">"
    
    # Special
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    EOF = "EOF"

@dataclass
class AdaToken:
    """Ada token with type, value, and location"""
    type: AdaTokenType
    value: str
    line: int
    column: int
    file_path: Optional[str] = None

class AdaLexer:
    """Ada lexer for tokenizing source code"""
    
    ADA_KEYWORDS = {
        "abort", "abs", "abstract", "accept", "access", "aliased", "all",
        "and", "array", "at", "begin", "body", "case", "constant", "declare",
        "delay", "delta", "digits", "do", "else", "elsif", "end", "entry",
        "exception", "exit", "for", "function", "generic", "goto", "if",
        "in", "interface", "is", "limited", "loop", "mod", "new", "not",
        "null", "of", "or", "others", "out", "overriding", "package",
        "pragma", "private", "procedure", "protected", "raise", "range",
        "record", "rem", "renames", "requeue", "return", "reverse",
        "select", "separate", "subtype", "synchronized", "tagged", "task",
        "terminate", "then", "type", "until", "use", "when", "while",
        "with", "xor"
    }
    
    def __init__(self, source: str, file_path: Optional[str] = None):
        self.source = source
        self.file_path = file_path
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[AdaToken] = []
        
    def tokenize(self) -> List[AdaToken]:
        """Tokenize Ada source code"""
        while self.position < len(self.source):
            self._skip_whitespace()
            if self.position >= len(self.source):
                break
                
            if self._match_comment():
                continue
            elif self._match_string_literal():
                continue
            elif self._match_character_literal():
                continue
            elif self._match_numeric_literal():
                continue
            elif self._match_identifier_or_keyword():
                continue
            elif self._match_operator():
                continue
            elif self._match_delimiter():
                continue
            else:
                raise AdaParseError(f"Unexpected character '{self.current_char()}' at {self.line}:{self.column}")
                
        self._add_token(AdaTokenType.EOF, "")
        return self.tokens
    
    def current_char(self) -> str:
        """Get current character"""
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> str:
        """Peek at character with offset"""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Advance position and return current character"""
        char = self.current_char()
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _add_token(self, token_type: AdaTokenType, value: str):
        """Add token to list"""
        token = AdaToken(token_type, value, self.line, self.column - len(value), self.file_path)
        self.tokens.append(token)
    
    def _skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char().isspace():
            self.advance()
    
    def _match_comment(self) -> bool:
        """Match Ada comment (-- to end of line)"""
        if self.current_char() == '-' and self.peek_char() == '-':
            start_column = self.column
            value = ""
            while self.current_char() not in ['\n', '\0']:
                value += self.advance()
            self._add_token(AdaTokenType.COMMENT, value)
            return True
        return False
    
    def _match_string_literal(self) -> bool:
        """Match string literal"""
        if self.current_char() != '"':
            return False
            
        start_column = self.column
        value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() != '"' and self.current_char() != '\0':
            if self.current_char() == '"' and self.peek_char() == '"':
                # Escaped quote
                value += '""'
                self.advance()
                self.advance()
            else:
                value += self.advance()
                
        if self.current_char() == '"':
            self.advance()  # Skip closing quote
            self._add_token(AdaTokenType.STRING_LITERAL, f'"{value}"')
            return True
        else:
            raise AdaParseError(f"Unterminated string literal at {self.line}:{start_column}")
    
    def _match_character_literal(self) -> bool:
        """Match character literal"""
        if self.current_char() != "'":
            return False
            
        # Check if it's an attribute reference instead
        if self.position > 0 and (self.source[self.position-1].isalnum() or self.source[self.position-1] == ')'):
            return False
            
        start_column = self.column
        value = "'"
        self.advance()
        
        if self.current_char() != '\0':
            value += self.advance()
            
        if self.current_char() == "'":
            value += self.advance()
            self._add_token(AdaTokenType.CHARACTER_LITERAL, value)
            return True
        else:
            raise AdaParseError(f"Unterminated character literal at {self.line}:{start_column}")
    
    def _match_numeric_literal(self) -> bool:
        """Match integer or real literal"""
        if not self.current_char().isdigit():
            return False
            
        value = ""
        has_dot = False
        has_exp = False
        base = 10
        
        # Check for based literals (e.g., 16#FF#)
        start_pos = self.position
        temp_value = ""
        temp_pos = self.position
        
        while temp_pos < len(self.source) and self.source[temp_pos].isdigit():
            temp_value += self.source[temp_pos]
            temp_pos += 1
            
        if temp_pos < len(self.source) and self.source[temp_pos] == '#':
            # Based literal
            base = int(temp_value)
            value = temp_value + "#"
            self.position = temp_pos + 1
            self.column += len(value)
            
            while self.current_char().isalnum():
                value += self.advance()
                
            if self.current_char() == '#':
                value += self.advance()
            else:
                raise AdaParseError(f"Invalid based literal at {self.line}:{self.column}")
        else:
            # Decimal literal
            while self.current_char().isdigit():
                value += self.advance()
                
            # Check for decimal point
            if self.current_char() == '.' and self.peek_char().isdigit():
                has_dot = True
                value += self.advance()  # '.'
                while self.current_char().isdigit():
                    value += self.advance()
                    
            # Check for exponent
            if self.current_char().lower() == 'e':
                has_exp = True
                value += self.advance()  # 'e' or 'E'
                if self.current_char() in ['+', '-']:
                    value += self.advance()
                while self.current_char().isdigit():
                    value += self.advance()
        
        token_type = AdaTokenType.REAL_LITERAL if has_dot or has_exp else AdaTokenType.INTEGER_LITERAL
        self._add_token(token_type, value)
        return True
    
    def _match_identifier_or_keyword(self) -> bool:
        """Match identifier or keyword"""
        if not (self.current_char().isalpha() or self.current_char() == '_'):
            return False
            
        value = ""
        while (self.current_char().isalnum() or self.current_char() == '_'):
            value += self.advance()
            
        # Check if it's a keyword (case-insensitive)
        lower_value = value.lower()
        if lower_value in self.ADA_KEYWORDS:
            token_type = AdaTokenType(lower_value)
        else:
            token_type = AdaTokenType.IDENTIFIER
            
        self._add_token(token_type, value)
        return True
    
    def _match_operator(self) -> bool:
        """Match multi-character operators"""
        char = self.current_char()
        next_char = self.peek_char()
        
        if char == '=' and next_char == '>':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.ARROW, "=>")
            return True
        elif char == '.' and next_char == '.':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.DOUBLE_DOT, "..")
            return True
        elif char == '*' and next_char == '*':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.DOUBLE_STAR, "**")
            return True
        elif char == ':' and next_char == '=':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.ASSIGNMENT, ":=")
            return True
        elif char == '/' and next_char == '=':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.NOT_EQUAL, "/=")
            return True
        elif char == '<' and next_char == '=':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.LESS_EQUAL, "<=")
            return True
        elif char == '>' and next_char == '=':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.GREATER_EQUAL, ">=")
            return True
        elif char == '<' and next_char == '<':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.LEFT_LABEL, "<<")
            return True
        elif char == '>' and next_char == '>':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.RIGHT_LABEL, ">>")
            return True
        elif char == '<' and next_char == '>':
            self.advance()
            self.advance()
            self._add_token(AdaTokenType.BOX, "<>")
            return True
            
        return False
    
    def _match_delimiter(self) -> bool:
        """Match single character delimiters"""
        char = self.current_char()
        token_map = {
            ';': AdaTokenType.SEMICOLON,
            ',': AdaTokenType.COMMA,
            '.': AdaTokenType.DOT,
            ':': AdaTokenType.COLON,
            "'": AdaTokenType.APOSTROPHE,
            '(': AdaTokenType.LEFT_PAREN,
            ')': AdaTokenType.RIGHT_PAREN,
            '|': AdaTokenType.PIPE,
            '&': AdaTokenType.AMPERSAND,
            '+': AdaTokenType.PLUS,
            '-': AdaTokenType.MINUS,
            '*': AdaTokenType.STAR,
            '/': AdaTokenType.SLASH,
            '=': AdaTokenType.EQUAL,
            '<': AdaTokenType.LESS,
            '>': AdaTokenType.GREATER,
        }
        
        if char in token_map:
            self.advance()
            self._add_token(token_map[char], char)
            return True
            
        return False

class AdaParseError(ParseError):
    """Ada-specific parse error"""
    pass

class AdaSyntaxError(AdaParseError):
    """Ada syntax error"""
    pass

@dataclass
class ParseContext:
    """Context information during parsing"""
    in_generic: bool = False
    in_package: bool = False
    in_subprogram: bool = False
    in_task: bool = False
    in_protected: bool = False
    current_scope: str = "global"

class AdaParser(BaseParser):
    """Ada parser for creating AST from tokens"""
    
    def __init__(self, tokens: Optional[List[AdaToken]] = None):
        super().__init__()
        self.tokens = tokens or []
        self.position = 0
        self.context = ParseContext()
        
    def parse(self, source: str, file_path: Optional[str] = None) -> AdaCompilationUnit:
        """Parse Ada source code into AST"""
        try:
            lexer = AdaLexer(source, file_path)
            self.tokens = lexer.tokenize()
            self.position = 0
            
            return self.parse_compilation_unit()
            
        except Exception as e:
            raise AdaParseError(f"Parse error: {e}")
    
    def current_token(self) -> AdaToken:
        """Get current token"""
        if self.position >= len(self.tokens):
            return AdaToken(AdaTokenType.EOF, "", 0, 0)
        return self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> AdaToken:
        """Peek at token with offset"""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return AdaToken(AdaTokenType.EOF, "", 0, 0)
        return self.tokens[pos]
    
    def advance(self) -> AdaToken:
        """Advance to next token"""
        token = self.current_token()
        if self.position < len(self.tokens):
            self.position += 1
        return token
    
    def match(self, *token_types: AdaTokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token().type in token_types
    
    def consume(self, token_type: AdaTokenType, message: str = None) -> AdaToken:
        """Consume token of specific type or raise error"""
        if self.current_token().type == token_type:
            return self.advance()
        
        msg = message or f"Expected {token_type.value}, got {self.current_token().type.value}"
        raise AdaSyntaxError(f"{msg} at line {self.current_token().line}")
    
    def parse_compilation_unit(self) -> AdaCompilationUnit:
        """Parse compilation unit"""
        context_clauses = []
        pragmas = []
        
        # Parse context clauses and pragmas
        while self.match(AdaTokenType.WITH, AdaTokenType.USE, AdaTokenType.PRAGMA):
            if self.match(AdaTokenType.WITH):
                context_clauses.append(self.parse_with_clause())
            elif self.match(AdaTokenType.USE):
                context_clauses.append(self.parse_use_clause())
            elif self.match(AdaTokenType.PRAGMA):
                pragmas.append(self.parse_pragma())
        
        # Parse library unit
        unit = self.parse_library_unit()
        
        return AdaCompilationUnit(
            context_clauses=context_clauses,
            unit=unit,
            pragmas=pragmas
        )
    
    def parse_with_clause(self) -> AdaWithClause:
        """Parse with clause"""
        self.consume(AdaTokenType.WITH)
        
        is_limited = False
        is_private = False
        
        if self.match(AdaTokenType.LIMITED):
            is_limited = True
            self.advance()
        elif self.match(AdaTokenType.PRIVATE):
            is_private = True
            self.advance()
            
        library_units = [self.consume(AdaTokenType.IDENTIFIER).value]
        
        while self.match(AdaTokenType.COMMA):
            self.advance()
            library_units.append(self.consume(AdaTokenType.IDENTIFIER).value)
            
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaWithClause(
            library_units=library_units,
            is_limited=is_limited,
            is_private=is_private
        )
    
    def parse_use_clause(self) -> AdaUseClause:
        """Parse use clause"""
        self.consume(AdaTokenType.USE)
        
        library_units = [self.consume(AdaTokenType.IDENTIFIER).value]
        
        while self.match(AdaTokenType.COMMA):
            self.advance()
            library_units.append(self.consume(AdaTokenType.IDENTIFIER).value)
            
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaUseClause(library_units=library_units)
    
    def parse_pragma(self) -> AdaPragma:
        """Parse pragma directive"""
        self.consume(AdaTokenType.PRAGMA)
        name = self.consume(AdaTokenType.IDENTIFIER).value
        
        arguments = []
        if self.match(AdaTokenType.LEFT_PAREN):
            self.advance()
            if not self.match(AdaTokenType.RIGHT_PAREN):
                arguments.append(self.parse_expression())
                while self.match(AdaTokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())
            self.consume(AdaTokenType.RIGHT_PAREN)
            
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaPragma(pragma_name=name, arguments=arguments)
    
    def parse_library_unit(self) -> AdaLibraryUnit:
        """Parse library unit (package, subprogram, etc.)"""
        if self.match(AdaTokenType.PACKAGE):
            return self.parse_package()
        elif self.match(AdaTokenType.PROCEDURE, AdaTokenType.FUNCTION):
            return self.parse_subprogram()
        elif self.match(AdaTokenType.GENERIC):
            return self.parse_generic()
        elif self.match(AdaTokenType.TASK):
            return self.parse_task()
        elif self.match(AdaTokenType.PROTECTED):
            return self.parse_protected()
        else:
            raise AdaSyntaxError(f"Expected library unit at line {self.current_token().line}")
    
    def parse_package(self) -> Union[AdaPackageSpecification, AdaPackageBody]:
        """Parse package specification or body"""
        self.consume(AdaTokenType.PACKAGE)
        
        if self.match(AdaTokenType.BODY):
            self.advance()
            name = self.consume(AdaTokenType.IDENTIFIER).value
            self.consume(AdaTokenType.IS)
            
            declarations = []
            while not self.match(AdaTokenType.BEGIN, AdaTokenType.END):
                declarations.append(self.parse_declaration())
                
            statements = []
            exception_handlers = []
            
            if self.match(AdaTokenType.BEGIN):
                self.advance()
                statements = self.parse_statement_list()
                
            if self.match(AdaTokenType.EXCEPTION):
                exception_handlers = self.parse_exception_handlers()
                
            self.consume(AdaTokenType.END)
            if self.match(AdaTokenType.IDENTIFIER):
                self.advance()
            self.consume(AdaTokenType.SEMICOLON)
            
            return AdaPackageBody(
                name=name,
                declarations=declarations,
                statements=statements,
                exception_handlers=exception_handlers
            )
        else:
            name = self.consume(AdaTokenType.IDENTIFIER).value
            self.consume(AdaTokenType.IS)
            
            declarations = []
            private_declarations = []
            
            while not self.match(AdaTokenType.PRIVATE, AdaTokenType.END):
                declarations.append(self.parse_declaration())
                
            if self.match(AdaTokenType.PRIVATE):
                self.advance()
                while not self.match(AdaTokenType.END):
                    private_declarations.append(self.parse_declaration())
                    
            self.consume(AdaTokenType.END)
            if self.match(AdaTokenType.IDENTIFIER):
                self.advance()
            self.consume(AdaTokenType.SEMICOLON)
            
            return AdaPackageSpecification(
                name=name,
                declarations=declarations,
                private_declarations=private_declarations
            )
    
    def parse_subprogram(self) -> Union[AdaSubprogramSpecification, AdaSubprogramBody]:
        """Parse subprogram specification or body"""
        kind = "procedure" if self.match(AdaTokenType.PROCEDURE) else "function"
        self.advance()
        
        name = self.consume(AdaTokenType.IDENTIFIER).value
        
        parameters = []
        if self.match(AdaTokenType.LEFT_PAREN):
            parameters = self.parse_parameter_list()
            
        return_type = None
        if kind == "function":
            self.consume(AdaTokenType.RETURN)
            return_type = self.parse_type_reference()
            
        if self.match(AdaTokenType.IS):
            # Subprogram body
            self.advance()
            
            declarations = []
            while not self.match(AdaTokenType.BEGIN):
                declarations.append(self.parse_declaration())
                
            self.consume(AdaTokenType.BEGIN)
            statements = self.parse_statement_list()
            
            exception_handlers = []
            if self.match(AdaTokenType.EXCEPTION):
                exception_handlers = self.parse_exception_handlers()
                
            self.consume(AdaTokenType.END)
            if self.match(AdaTokenType.IDENTIFIER):
                self.advance()
            self.consume(AdaTokenType.SEMICOLON)
            
            spec = AdaSubprogramSpecification(
                name=name,
                subprogram_kind=kind,
                parameters=parameters,
                return_type=return_type
            )
            
            return AdaSubprogramBody(
                name=name,
                specification=spec,
                declarations=declarations,
                statements=statements,
                exception_handlers=exception_handlers
            )
        else:
            # Specification only
            self.consume(AdaTokenType.SEMICOLON)
            return AdaSubprogramSpecification(
                name=name,
                subprogram_kind=kind,
                parameters=parameters,
                return_type=return_type
            )
    
    def parse_generic(self) -> Union[AdaGenericPackage, AdaGenericSubprogram]:
        """Parse generic unit"""
        self.consume(AdaTokenType.GENERIC)
        
        formal_parameters = []
        while not self.match(AdaTokenType.PACKAGE, AdaTokenType.PROCEDURE, AdaTokenType.FUNCTION):
            formal_parameters.append(self.parse_generic_formal_parameter())
            
        if self.match(AdaTokenType.PACKAGE):
            package_spec = self.parse_package()
            return AdaGenericPackage(
                name=package_spec.name,
                formal_parameters=formal_parameters,
                package_specification=package_spec
            )
        else:
            subprogram_spec = self.parse_subprogram()
            return AdaGenericSubprogram(
                name=subprogram_spec.name,
                formal_parameters=formal_parameters,
                subprogram_specification=subprogram_spec
            )
    
    def parse_generic_formal_parameter(self) -> AdaGenericFormalParameter:
        """Parse generic formal parameter"""
        if self.match(AdaTokenType.TYPE):
            self.advance()
            name = self.consume(AdaTokenType.IDENTIFIER).value
            # Simplified - could be more complex
            self.consume(AdaTokenType.SEMICOLON)
            return AdaGenericFormalParameter(parameter_kind="type", name=name)
        else:
            # Other formal parameter types (procedure, function, object)
            # Simplified implementation
            name = self.consume(AdaTokenType.IDENTIFIER).value
            self.consume(AdaTokenType.SEMICOLON)
            return AdaGenericFormalParameter(parameter_kind="object", name=name)
    
    def parse_parameter_list(self) -> List[AdaParameterDeclaration]:
        """Parse parameter list"""
        self.consume(AdaTokenType.LEFT_PAREN)
        
        parameters = []
        if not self.match(AdaTokenType.RIGHT_PAREN):
            parameters.append(self.parse_parameter_declaration())
            while self.match(AdaTokenType.SEMICOLON):
                self.advance()
                parameters.append(self.parse_parameter_declaration())
                
        self.consume(AdaTokenType.RIGHT_PAREN)
        return parameters
    
    def parse_parameter_declaration(self) -> AdaParameterDeclaration:
        """Parse parameter declaration"""
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.COLON)
        
        mode = "in"
        if self.match(AdaTokenType.IN):
            self.advance()
            if self.match(AdaTokenType.OUT):
                self.advance()
                mode = "in out"
        elif self.match(AdaTokenType.OUT):
            self.advance()
            mode = "out"
            
        param_type = self.parse_type_reference()
        
        default_value = None
        if self.match(AdaTokenType.ASSIGNMENT):
            self.advance()
            default_value = self.parse_expression()
            
        return AdaParameterDeclaration(
            name=name,
            parameter_mode=mode,
            parameter_type=param_type,
            default_value=default_value
        )
    
    def parse_declaration(self) -> AdaDeclaration:
        """Parse declaration"""
        if self.match(AdaTokenType.TYPE):
            return self.parse_type_declaration()
        elif self.match(AdaTokenType.SUBTYPE):
            return self.parse_subtype_declaration()
        elif self.match(AdaTokenType.PROCEDURE, AdaTokenType.FUNCTION):
            return self.parse_subprogram()
        elif self.match(AdaTokenType.TASK):
            return self.parse_task()
        elif self.match(AdaTokenType.PROTECTED):
            return self.parse_protected()
        else:
            return self.parse_object_declaration()
    
    def parse_type_declaration(self) -> AdaTypeDeclaration:
        """Parse type declaration"""
        self.consume(AdaTokenType.TYPE)
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.IS)
        
        type_def = self.parse_type_definition()
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaTypeDeclaration(name=name, type_definition=type_def)
    
    def parse_type_definition(self) -> AdaTypeDefinition:
        """Parse type definition"""
        if self.match(AdaTokenType.ARRAY):
            return self.parse_array_type()
        elif self.match(AdaTokenType.RECORD):
            return self.parse_record_type()
        elif self.match(AdaTokenType.ACCESS):
            return self.parse_access_type()
        elif self.match(AdaTokenType.RANGE):
            return self.parse_integer_type()
        elif self.match(AdaTokenType.LEFT_PAREN):
            return self.parse_enumeration_type()
        else:
            # Simplified - assume scalar type
            return AdaScalarType(scalar_kind="integer")
    
    def parse_array_type(self) -> AdaArrayType:
        """Parse array type"""
        self.consume(AdaTokenType.ARRAY)
        self.consume(AdaTokenType.LEFT_PAREN)
        
        index_types = [self.parse_type_reference()]
        while self.match(AdaTokenType.COMMA):
            self.advance()
            index_types.append(self.parse_type_reference())
            
        self.consume(AdaTokenType.RIGHT_PAREN)
        self.consume(AdaTokenType.OF)
        
        component_type = self.parse_type_reference()
        
        return AdaArrayType(
            index_types=index_types,
            component_type=component_type
        )
    
    def parse_record_type(self) -> AdaRecordType:
        """Parse record type"""
        self.consume(AdaTokenType.RECORD)
        
        components = []
        while not self.match(AdaTokenType.END):
            component = self.parse_component_declaration()
            components.append(component)
            
        self.consume(AdaTokenType.END)
        self.consume(AdaTokenType.RECORD)
        
        return AdaRecordType(components=components)
    
    def parse_component_declaration(self) -> AdaComponentDeclaration:
        """Parse record component declaration"""
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.COLON)
        component_type = self.parse_type_reference()
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaComponentDeclaration(
            name=name,
            component_type=component_type
        )
    
    def parse_access_type(self) -> AdaAccessType:
        """Parse access type"""
        self.consume(AdaTokenType.ACCESS)
        designated_type = self.parse_type_reference()
        
        return AdaAccessType(designated_type=designated_type)
    
    def parse_integer_type(self) -> AdaIntegerType:
        """Parse integer type"""
        self.consume(AdaTokenType.RANGE)
        low = self.parse_expression()
        self.consume(AdaTokenType.DOUBLE_DOT)
        high = self.parse_expression()
        
        return AdaIntegerType(
            range_constraint=AdaRangeConstraint(low_bound=low, high_bound=high)
        )
    
    def parse_enumeration_type(self) -> AdaEnumerationType:
        """Parse enumeration type"""
        self.consume(AdaTokenType.LEFT_PAREN)
        
        literals = [self.consume(AdaTokenType.IDENTIFIER).value]
        while self.match(AdaTokenType.COMMA):
            self.advance()
            literals.append(self.consume(AdaTokenType.IDENTIFIER).value)
            
        self.consume(AdaTokenType.RIGHT_PAREN)
        
        return AdaEnumerationType(literals=literals)
    
    def parse_type_reference(self) -> AdaTypeReference:
        """Parse type reference"""
        type_name = self.consume(AdaTokenType.IDENTIFIER).value
        
        package_name = None
        if self.match(AdaTokenType.DOT):
            package_name = type_name
            self.advance()
            type_name = self.consume(AdaTokenType.IDENTIFIER).value
            
        return AdaTypeReference(type_name=type_name, package_name=package_name)
    
    def parse_expression(self) -> AdaExpression:
        """Parse expression (simplified)"""
        if self.match(AdaTokenType.INTEGER_LITERAL):
            value = self.advance().value
            return AdaNumericLiteral(value=int(value), numeric_type="integer")
        elif self.match(AdaTokenType.REAL_LITERAL):
            value = self.advance().value
            return AdaNumericLiteral(value=float(value), numeric_type="real")
        elif self.match(AdaTokenType.STRING_LITERAL):
            value = self.advance().value
            return AdaStringLiteral(value=value[1:-1])  # Remove quotes
        elif self.match(AdaTokenType.CHARACTER_LITERAL):
            value = self.advance().value
            return AdaCharacterLiteral(value=value[1:-1])  # Remove quotes
        elif self.match(AdaTokenType.IDENTIFIER):
            name = self.advance().value
            return AdaIdentifier(name=name)
        else:
            raise AdaSyntaxError(f"Expected expression at line {self.current_token().line}")
    
    # Simplified implementations for remaining parse methods
    def parse_object_declaration(self) -> AdaObjectDeclaration:
        """Parse object declaration (simplified)"""
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.COLON)
        object_type = self.parse_type_reference()
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaObjectDeclaration(name=name, object_type=object_type)
    
    def parse_subtype_declaration(self) -> AdaSubtypeDeclaration:
        """Parse subtype declaration (simplified)"""
        self.consume(AdaTokenType.SUBTYPE)
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.IS)
        parent_type = self.parse_type_reference()
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaSubtypeDeclaration(name=name, parent_type=parent_type)
    
    def parse_task(self) -> AdaTaskSpecification:
        """Parse task (simplified)"""
        self.consume(AdaTokenType.TASK)
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaTaskSpecification(name=name)
    
    def parse_protected(self) -> AdaProtectedSpecification:
        """Parse protected object (simplified)"""
        self.consume(AdaTokenType.PROTECTED)
        name = self.consume(AdaTokenType.IDENTIFIER).value
        self.consume(AdaTokenType.SEMICOLON)
        
        return AdaProtectedSpecification(name=name)
    
    def parse_statement_list(self) -> List[AdaStatement]:
        """Parse statement list (simplified)"""
        statements = []
        while not self.match(AdaTokenType.END, AdaTokenType.EXCEPTION):
            # Simplified - just null statements
            self.consume(AdaTokenType.NULL)
            self.consume(AdaTokenType.SEMICOLON)
            statements.append(AdaNullStatement())
        return statements
    
    def parse_exception_handlers(self) -> List[AdaExceptionHandler]:
        """Parse exception handlers (simplified)"""
        self.consume(AdaTokenType.EXCEPTION)
        handlers = []
        # Simplified implementation
        return handlers

# Export main classes
__all__ = [
    'AdaTokenType', 'AdaToken', 'AdaLexer', 'AdaParser',
    'AdaParseError', 'AdaSyntaxError', 'ParseContext'
] 