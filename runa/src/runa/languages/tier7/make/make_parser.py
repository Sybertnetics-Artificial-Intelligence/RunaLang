#!/usr/bin/env python3
"""
Make Parser - Comprehensive parser for Make (GNU Make/POSIX Make)

Features:
- Complete Makefile syntax parsing
- Rules and targets (including pattern rules)
- Variables (all assignment types: =, :=, ?=, +=, !=)
- Functions (built-in and user-defined)
- Conditionals (ifeq, ifneq, ifdef, ifndef)
- Includes and directives
- Comments and whitespace handling
- Error recovery and reporting
"""

import re
from typing import List, Optional, Dict, Any, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass
from .make_ast import *

class TokenType(Enum):
    """Make token types"""
    # Literals
    IDENTIFIER = auto()
    TEXT = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Operators and symbols
    EQUALS = auto()           # =
    COLON_EQUALS = auto()     # :=
    QUESTION_EQUALS = auto()  # ?=
    PLUS_EQUALS = auto()      # +=
    EXCLAIM_EQUALS = auto()   # !=
    COLON = auto()           # :
    DOUBLE_COLON = auto()    # ::
    SEMICOLON = auto()       # ;
    PIPE = auto()            # |
    DOLLAR = auto()          # $
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    COMMA = auto()           # ,
    AT = auto()              # @
    MINUS = auto()           # -
    PLUS = auto()            # +
    PERCENT = auto()         # %
    
    # Special characters
    TAB = auto()
    NEWLINE = auto()
    SPACE = auto()
    BACKSLASH = auto()
    
    # Keywords and directives
    INCLUDE = auto()
    SINCLUDE = auto()        # -include
    VPATH = auto()
    EXPORT = auto()
    UNEXPORT = auto()
    OVERRIDE = auto()
    PRIVATE = auto()
    DEFINE = auto()
    ENDEF = auto()
    
    # Conditionals
    IFEQ = auto()
    IFNEQ = auto()
    IFDEF = auto()
    IFNDEF = auto()
    ELSE = auto()
    ENDIF = auto()
    
    # Special targets
    PHONY = auto()
    SUFFIXES = auto()
    PRECIOUS = auto()
    INTERMEDIATE = auto()
    SECONDARY = auto()
    DELETE_ON_ERROR = auto()
    
    # Built-in functions
    SUBST = auto()
    PATSUBST = auto()
    WILDCARD = auto()
    SHELL = auto()
    STRIP = auto()
    FINDSTRING = auto()
    FILTER = auto()
    FILTER_OUT = auto()
    SORT = auto()
    WORD = auto()
    WORDS = auto()
    WORDLIST = auto()
    FIRSTWORD = auto()
    LASTWORD = auto()
    DIR = auto()
    NOTDIR = auto()
    SUFFIX = auto()
    BASENAME = auto()
    ADDSUFFIX = auto()
    ADDPREFIX = auto()
    JOIN = auto()
    REALPATH = auto()
    ABSPATH = auto()
    
    # Comments
    COMMENT = auto()
    
    # End of file
    EOF = auto()

@dataclass
class Token:
    """Make token"""
    type: TokenType
    value: str
    line: int = 1
    column: int = 1
    
class MakeLexer:
    """Lexer for Make files"""
    
    # Keywords mapping
    KEYWORDS = {
        'include': TokenType.INCLUDE,
        '-include': TokenType.SINCLUDE,
        'vpath': TokenType.VPATH,
        'VPATH': TokenType.VPATH,
        'export': TokenType.EXPORT,
        'unexport': TokenType.UNEXPORT,
        'override': TokenType.OVERRIDE,
        'private': TokenType.PRIVATE,
        'define': TokenType.DEFINE,
        'endef': TokenType.ENDEF,
        'ifeq': TokenType.IFEQ,
        'ifneq': TokenType.IFNEQ,
        'ifdef': TokenType.IFDEF,
        'ifndef': TokenType.IFNDEF,
        'else': TokenType.ELSE,
        'endif': TokenType.ENDIF,
        '.PHONY': TokenType.PHONY,
        '.SUFFIXES': TokenType.SUFFIXES,
        '.PRECIOUS': TokenType.PRECIOUS,
        '.INTERMEDIATE': TokenType.INTERMEDIATE,
        '.SECONDARY': TokenType.SECONDARY,
        '.DELETE_ON_ERROR': TokenType.DELETE_ON_ERROR,
        # Built-in functions
        'subst': TokenType.SUBST,
        'patsubst': TokenType.PATSUBST,
        'wildcard': TokenType.WILDCARD,
        'shell': TokenType.SHELL,
        'strip': TokenType.STRIP,
        'findstring': TokenType.FINDSTRING,
        'filter': TokenType.FILTER,
        'filter-out': TokenType.FILTER_OUT,
        'sort': TokenType.SORT,
        'word': TokenType.WORD,
        'words': TokenType.WORDS,
        'wordlist': TokenType.WORDLIST,
        'firstword': TokenType.FIRSTWORD,
        'lastword': TokenType.LASTWORD,
        'dir': TokenType.DIR,
        'notdir': TokenType.NOTDIR,
        'suffix': TokenType.SUFFIX,
        'basename': TokenType.BASENAME,
        'addsuffix': TokenType.ADDSUFFIX,
        'addprefix': TokenType.ADDPREFIX,
        'join': TokenType.JOIN,
        'realpath': TokenType.REALPATH,
        'abspath': TokenType.ABSPATH,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def error(self, message: str) -> None:
        """Report lexer error"""
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {message}")
        
    def peek(self, offset: int = 0) -> str:
        """Peek at character at current position + offset"""
        pos = self.pos + offset
        return self.source[pos] if pos < len(self.source) else ''
        
    def advance(self) -> str:
        """Advance and return current character"""
        if self.pos >= len(self.source):
            return ''
            
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char
        
    def skip_whitespace(self, skip_newlines: bool = False) -> None:
        """Skip whitespace characters"""
        while self.pos < len(self.source):
            char = self.peek()
            if char in ' \t' or (skip_newlines and char == '\n'):
                self.advance()
            else:
                break
                
    def read_string(self, quote: str) -> str:
        """Read quoted string"""
        value = ''
        self.advance()  # Skip opening quote
        
        while self.pos < len(self.source):
            char = self.peek()
            if char == quote:
                self.advance()  # Skip closing quote
                break
            elif char == '\\':
                self.advance()  # Skip backslash
                escaped = self.advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == '\\':
                    value += '\\'
                elif escaped == quote:
                    value += quote
                else:
                    value += escaped
            else:
                value += self.advance()
                
        return value
        
    def read_identifier(self) -> str:
        """Read identifier or keyword"""
        value = ''
        
        while self.pos < len(self.source):
            char = self.peek()
            if char.isalnum() or char in '_.-':
                value += self.advance()
            else:
                break
                
        return value
        
    def read_variable_reference(self) -> Token:
        """Read variable reference like $(VAR) or ${VAR}"""
        start_line, start_col = self.line, self.column
        self.advance()  # Skip $
        
        if self.peek() == '(':
            self.advance()  # Skip (
            bracket_style = "$()"
            end_char = ')'
        elif self.peek() == '{':
            self.advance()  # Skip {
            bracket_style = "${}"
            end_char = '}'
        else:
            # Single character automatic variable like $@, $<
            char = self.advance()
            return Token(TokenType.IDENTIFIER, f"${char}", start_line, start_col)
            
        # Read variable name
        name = ''
        while self.pos < len(self.source) and self.peek() != end_char:
            name += self.advance()
            
        if self.pos < len(self.source):
            self.advance()  # Skip closing bracket
            
        return Token(TokenType.IDENTIFIER, f"${bracket_style[1]}{name}{end_char}", start_line, start_col)
        
    def read_comment(self) -> str:
        """Read comment to end of line"""
        value = ''
        self.advance()  # Skip #
        
        while self.pos < len(self.source):
            char = self.peek()
            if char == '\n':
                break
            value += self.advance()
            
        return value.strip()
        
    def read_text_until(self, delimiters: str) -> str:
        """Read text until delimiter"""
        value = ''
        
        while self.pos < len(self.source):
            char = self.peek()
            if char in delimiters:
                break
            elif char == '\\' and self.peek(1) in delimiters:
                self.advance()  # Skip backslash
                value += self.advance()  # Add escaped delimiter
            else:
                value += self.advance()
                
        return value.strip()
        
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source"""
        self.tokens = []
        
        while self.pos < len(self.source):
            start_line, start_col = self.line, self.column
            char = self.peek()
            
            # Skip spaces (but not tabs at line start - those are significant)
            if char == ' ':
                self.skip_whitespace()
                continue
                
            # Newlines
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, self.advance(), start_line, start_col))
                
            # Tabs (significant for commands)
            elif char == '\t':
                self.tokens.append(Token(TokenType.TAB, self.advance(), start_line, start_col))
                
            # Comments
            elif char == '#':
                comment = self.read_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment, start_line, start_col))
                
            # Variable references
            elif char == '$':
                token = self.read_variable_reference()
                self.tokens.append(token)
                
            # Operators
            elif char == ':':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.COLON_EQUALS, ':=', start_line, start_col))
                elif self.peek(1) == ':':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.DOUBLE_COLON, '::', start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.COLON, self.advance(), start_line, start_col))
                    
            elif char == '=':
                self.tokens.append(Token(TokenType.EQUALS, self.advance(), start_line, start_col))
                
            elif char == '?':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.QUESTION_EQUALS, '?=', start_line, start_col))
                else:
                    text = self.read_text_until(' \t\n:=')
                    self.tokens.append(Token(TokenType.TEXT, char + text, start_line, start_col))
                    
            elif char == '+':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.PLUS_EQUALS, '+=', start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.PLUS, self.advance(), start_line, start_col))
                    
            elif char == '!':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.EXCLAIM_EQUALS, '!=', start_line, start_col))
                else:
                    text = self.read_text_until(' \t\n:=')
                    self.tokens.append(Token(TokenType.TEXT, char + text, start_line, start_col))
                    
            # Other symbols
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, self.advance(), start_line, start_col))
            elif char == '|':
                self.tokens.append(Token(TokenType.PIPE, self.advance(), start_line, start_col))
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, self.advance(), start_line, start_col))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, self.advance(), start_line, start_col))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, self.advance(), start_line, start_col))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, self.advance(), start_line, start_col))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, self.advance(), start_line, start_col))
            elif char == '@':
                self.tokens.append(Token(TokenType.AT, self.advance(), start_line, start_col))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, self.advance(), start_line, start_col))
            elif char == '%':
                self.tokens.append(Token(TokenType.PERCENT, self.advance(), start_line, start_col))
            elif char == '\\':
                self.tokens.append(Token(TokenType.BACKSLASH, self.advance(), start_line, start_col))
                
            # Quoted strings
            elif char in '"\'':
                string_value = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, string_value, start_line, start_col))
                
            # Numbers
            elif char.isdigit():
                number = self.read_identifier()  # Numbers can have dots
                self.tokens.append(Token(TokenType.NUMBER, number, start_line, start_col))
                
            # Identifiers and keywords
            elif char.isalpha() or char in '_.':
                identifier = self.read_identifier()
                token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, identifier, start_line, start_col))
                
            # Default: treat as text
            else:
                text = self.read_text_until(' \t\n:=;|(){},-@+%\\')
                if text:
                    self.tokens.append(Token(TokenType.TEXT, char + text, start_line, start_col))
                else:
                    self.advance()  # Skip single character
                    
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

class MakeParser:
    """Parser for Make files"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, '', 1, 1)
        
    def error(self, message: str) -> None:
        """Report parser error"""
        token = self.current_token
        raise SyntaxError(f"Line {token.line}, Column {token.column}: {message}")
        
    def peek(self, offset: int = 0) -> Token:
        """Peek at token at current position + offset"""
        pos = self.pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else Token(TokenType.EOF, '', 1, 1)
        
    def advance(self) -> Token:
        """Advance to next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return self.current_token
        
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token.type in token_types
        
    def consume(self, token_type: TokenType, message: str = None) -> Token:
        """Consume token of given type or error"""
        if self.current_token.type != token_type:
            msg = message or f"Expected {token_type}, got {self.current_token.type}"
            self.error(msg)
        token = self.current_token
        self.advance()
        return token
        
    def skip_newlines(self) -> None:
        """Skip newline tokens"""
        while self.match(TokenType.NEWLINE):
            self.advance()
            
    def is_at_line_start(self) -> bool:
        """Check if we're at the start of a line (after newlines)"""
        # Look back to see if previous token was newline or we're at start
        return self.pos == 0 or self.tokens[self.pos - 1].type == TokenType.NEWLINE
        
    def parse_makefile(self) -> MakeFile:
        """Parse complete makefile"""
        statements = []
        
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            try:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            except SyntaxError:
                # Skip to next line on error
                while not self.match(TokenType.NEWLINE, TokenType.EOF):
                    self.advance()
                if self.match(TokenType.NEWLINE):
                    self.advance()
                    
            self.skip_newlines()
            
        return MakeFile(statements=statements)
        
    def parse_statement(self) -> Optional[MakeStatement]:
        """Parse a top-level statement"""
        # Skip leading tabs/spaces
        while self.match(TokenType.TAB, TokenType.SPACE):
            self.advance()
            
        if self.match(TokenType.COMMENT):
            return self.parse_comment()
        elif self.match(TokenType.INCLUDE, TokenType.SINCLUDE):
            return self.parse_include()
        elif self.match(TokenType.VPATH):
            return self.parse_vpath()
        elif self.match(TokenType.EXPORT, TokenType.UNEXPORT):
            return self.parse_export()
        elif self.match(TokenType.DEFINE):
            return self.parse_define()
        elif self.match(TokenType.IFEQ, TokenType.IFNEQ, TokenType.IFDEF, TokenType.IFNDEF):
            return self.parse_conditional()
        elif self.match(TokenType.OVERRIDE):
            return self.parse_override()
        elif self.match(TokenType.PRIVATE):
            return self.parse_private()
        elif self.is_rule_or_assignment():
            return self.parse_rule_or_assignment()
        else:
            # Skip unknown tokens
            self.advance()
            return None
            
    def is_rule_or_assignment(self) -> bool:
        """Check if this looks like a rule or variable assignment"""
        # Look ahead for : or = indicators
        saved_pos = self.pos
        
        # Skip to find : or =
        while (not self.match(TokenType.EOF, TokenType.NEWLINE) and 
               not self.match(TokenType.COLON, TokenType.DOUBLE_COLON, 
                             TokenType.EQUALS, TokenType.COLON_EQUALS,
                             TokenType.QUESTION_EQUALS, TokenType.PLUS_EQUALS,
                             TokenType.EXCLAIM_EQUALS)):
            self.advance()
            
        is_rule_or_assign = self.match(TokenType.COLON, TokenType.DOUBLE_COLON, 
                                      TokenType.EQUALS, TokenType.COLON_EQUALS,
                                      TokenType.QUESTION_EQUALS, TokenType.PLUS_EQUALS,
                                      TokenType.EXCLAIM_EQUALS)
        
        # Restore position
        self.pos = saved_pos
        self.current_token = self.tokens[self.pos]
        
        return is_rule_or_assign
        
    def parse_rule_or_assignment(self) -> MakeStatement:
        """Parse rule or variable assignment"""
        # Read target/variable name
        name_parts = []
        
        while (not self.match(TokenType.EOF, TokenType.NEWLINE) and 
               not self.match(TokenType.COLON, TokenType.DOUBLE_COLON,
                             TokenType.EQUALS, TokenType.COLON_EQUALS,
                             TokenType.QUESTION_EQUALS, TokenType.PLUS_EQUALS,
                             TokenType.EXCLAIM_EQUALS)):
            if self.match(TokenType.IDENTIFIER, TokenType.TEXT, TokenType.NUMBER):
                name_parts.append(self.current_token.value)
                self.advance()
            else:
                self.advance()
                
        name = ' '.join(name_parts).strip()
        
        # Check what follows
        if self.match(TokenType.COLON, TokenType.DOUBLE_COLON):
            return self.parse_rule(name)
        elif self.match(TokenType.EQUALS, TokenType.COLON_EQUALS,
                        TokenType.QUESTION_EQUALS, TokenType.PLUS_EQUALS,
                        TokenType.EXCLAIM_EQUALS):
            return self.parse_assignment(name)
        else:
            self.error("Expected : or = after target/variable name")
            
    def parse_rule(self, target_name: str) -> MakeRule:
        """Parse a rule"""
        is_double_colon = self.match(TokenType.DOUBLE_COLON)
        self.advance()  # Skip : or ::
        
        # Parse dependencies
        dependencies = []
        order_only_deps = []
        in_order_only = False
        
        while not self.match(TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.EOF):
            if self.match(TokenType.PIPE):
                in_order_only = True
                self.advance()
            elif self.match(TokenType.IDENTIFIER, TokenType.TEXT, TokenType.NUMBER):
                dep = self.current_token.value
                if in_order_only:
                    order_only_deps.append(dep)
                else:
                    dependencies.append(dep)
                self.advance()
            else:
                self.advance()
                
        # Parse commands (after semicolon or on following lines with tabs)
        commands = []
        
        if self.match(TokenType.SEMICOLON):
            self.advance()
            # Command on same line
            cmd_parts = []
            while not self.match(TokenType.NEWLINE, TokenType.EOF):
                cmd_parts.append(self.current_token.value)
                self.advance()
            if cmd_parts:
                commands.append(MakeCommand(' '.join(cmd_parts)))
                
        if self.match(TokenType.NEWLINE):
            self.advance()
            
        # Commands on following lines starting with tab
        while self.match(TokenType.TAB):
            self.advance()  # Skip tab
            
            # Check for command prefixes
            is_silent = False
            ignore_errors = False
            always_execute = False
            
            if self.match(TokenType.AT):
                is_silent = True
                self.advance()
            if self.match(TokenType.MINUS):
                ignore_errors = True
                self.advance()
            if self.match(TokenType.PLUS):
                always_execute = True
                self.advance()
                
            # Read command
            cmd_parts = []
            while not self.match(TokenType.NEWLINE, TokenType.EOF):
                cmd_parts.append(self.current_token.value)
                self.advance()
                
            if cmd_parts:
                cmd = MakeCommand(
                    command_line=' '.join(cmd_parts),
                    is_silent=is_silent,
                    ignore_errors=ignore_errors,
                    always_execute=always_execute
                )
                commands.append(cmd)
                
            if self.match(TokenType.NEWLINE):
                self.advance()
            else:
                break
                
        return MakeRule(
            targets=[target_name],
            dependencies=dependencies,
            order_only_deps=order_only_deps,
            commands=commands,
            is_double_colon=is_double_colon,
            is_pattern_rule='%' in target_name
        )
        
    def parse_assignment(self, var_name: str) -> MakeVariable:
        """Parse variable assignment"""
        assignment_type = self.current_token.value
        self.advance()
        
        # Read value
        value_parts = []
        while not self.match(TokenType.NEWLINE, TokenType.EOF):
            value_parts.append(self.current_token.value)
            self.advance()
            
        value_text = ' '.join(value_parts).strip()
        value = TextLiteral(value_text) if value_text else TextLiteral("")
        
        return MakeVariable(
            name=var_name,
            value=value,
            assignment_type=assignment_type
        )
        
    def parse_comment(self) -> MakeComment:
        """Parse comment"""
        text = self.current_token.value
        self.advance()
        return MakeComment(text=text)
        
    def parse_include(self) -> MakeInclude:
        """Parse include directive"""
        is_optional = self.match(TokenType.SINCLUDE)
        self.advance()
        
        filenames = []
        while not self.match(TokenType.NEWLINE, TokenType.EOF):
            if self.match(TokenType.IDENTIFIER, TokenType.TEXT, TokenType.STRING):
                filenames.append(self.current_token.value)
            self.advance()
            
        return MakeInclude(filenames=filenames, is_optional=is_optional)
        
    def parse_vpath(self) -> VPathDirective:
        """Parse VPATH directive"""
        self.advance()  # Skip 'vpath' or 'VPATH'
        
        # For vpath, next might be pattern
        pattern = None
        directories = []
        
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            # First argument could be pattern (for vpath) or directory
            if self.match(TokenType.IDENTIFIER, TokenType.TEXT):
                first_arg = self.current_token.value
                self.advance()
                
                # If there's more, first_arg is pattern
                if not self.match(TokenType.NEWLINE, TokenType.EOF):
                    pattern = first_arg
                    while not self.match(TokenType.NEWLINE, TokenType.EOF):
                        if self.match(TokenType.IDENTIFIER, TokenType.TEXT):
                            directories.append(self.current_token.value)
                        self.advance()
                else:
                    directories.append(first_arg)
                    
        return VPathDirective(pattern=pattern, directories=directories)
        
    def parse_export(self) -> ExportDirective:
        """Parse export/unexport directive"""
        is_unexport = self.match(TokenType.UNEXPORT)
        self.advance()
        
        variables = []
        while not self.match(TokenType.NEWLINE, TokenType.EOF):
            if self.match(TokenType.IDENTIFIER, TokenType.TEXT):
                variables.append(self.current_token.value)
            self.advance()
            
        return ExportDirective(variables=variables, is_unexport=is_unexport)
        
    def parse_define(self) -> UserDefinedFunction:
        """Parse define/endef block"""
        self.advance()  # Skip 'define'
        
        # Get function name
        name = ""
        if self.match(TokenType.IDENTIFIER, TokenType.TEXT):
            name = self.current_token.value
            self.advance()
            
        if self.match(TokenType.NEWLINE):
            self.advance()
            
        # Parse body until endef
        body = []
        while not self.match(TokenType.ENDEF, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            elif self.match(TokenType.NEWLINE):
                self.advance()
            else:
                self.advance()
                
        if self.match(TokenType.ENDEF):
            self.advance()
            
        return UserDefinedFunction(name=name, body=body)
        
    def parse_conditional(self) -> MakeConditional:
        """Parse conditional block"""
        condition_type = self.current_token.value
        self.advance()
        
        # Parse condition arguments
        condition_args = []
        while not self.match(TokenType.NEWLINE, TokenType.EOF):
            condition_args.append(self.current_token.value)
            self.advance()
            
        condition = TextLiteral(' '.join(condition_args))
        
        if self.match(TokenType.NEWLINE):
            self.advance()
            
        # Parse then statements
        then_statements = []
        while (not self.match(TokenType.ELSE, TokenType.ENDIF, TokenType.EOF)):
            stmt = self.parse_statement()
            if stmt:
                then_statements.append(stmt)
            elif self.match(TokenType.NEWLINE):
                self.advance()
            else:
                self.advance()
                
        # Parse else statements
        else_statements = []
        if self.match(TokenType.ELSE):
            self.advance()
            if self.match(TokenType.NEWLINE):
                self.advance()
                
            while not self.match(TokenType.ENDIF, TokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    else_statements.append(stmt)
                elif self.match(TokenType.NEWLINE):
                    self.advance()
                else:
                    self.advance()
                    
        if self.match(TokenType.ENDIF):
            self.advance()
            
        return MakeConditional(
            condition_type=condition_type,
            condition=condition,
            then_statements=then_statements,
            else_statements=else_statements
        )
        
    def parse_override(self) -> MakeVariable:
        """Parse override directive"""
        self.advance()  # Skip 'override'
        
        # This should be followed by a variable assignment
        var = self.parse_rule_or_assignment()
        if isinstance(var, MakeVariable):
            var.is_override = True
            return var
        else:
            self.error("Expected variable assignment after override")
            
    def parse_private(self) -> MakeVariable:
        """Parse private directive"""
        self.advance()  # Skip 'private'
        
        # This should be followed by a variable assignment
        var = self.parse_rule_or_assignment()
        if isinstance(var, MakeVariable):
            var.is_private = True
            return var
        else:
            self.error("Expected variable assignment after private")

# Main parsing functions

def parse_make(source: str) -> MakeFile:
    """Parse Make source code into AST"""
    try:
        lexer = MakeLexer(source)
        tokens = lexer.tokenize()
        
        parser = MakeParser(tokens)
        ast = parser.parse_makefile()
        
        return ast
        
    except Exception as e:
        raise SyntaxError(f"Make parsing failed: {str(e)}")

# Export main components
__all__ = [
    'TokenType', 'Token', 'MakeLexer', 'MakeParser', 'parse_make'
] 