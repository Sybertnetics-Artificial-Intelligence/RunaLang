#!/usr/bin/env python3
"""
CMake Parser Implementation

Complete parser for CMake build files including:
- CMakeLists.txt files with commands and targets
- Variables and property management
- Control flow statements
- Modern CMake target-based syntax
"""

import re
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .cmake_ast import *


class TokenType(Enum):
    """Token types for CMake lexer."""
    # Literals and identifiers
    IDENTIFIER = auto()
    STRING_LITERAL = auto()
    QUOTED_ARGUMENT = auto()
    BRACKET_ARGUMENT = auto()
    VARIABLE_REF = auto()
    GENERATOR_EXPR = auto()
    
    # Delimiters
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    
    # Special
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()


@dataclass
class Token:
    """Represents a token in CMake source."""
    type: TokenType
    value: str
    line: int
    column: int


class CMakeLexer:
    """Lexer for CMake files."""
    
    def __init__(self, source: str, file_path: Optional[str] = None):
        self.source = source
        self.file_path = file_path
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source."""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
                
            char = self.source[self.position]
            
            if char == '\n':
                self._add_token(TokenType.NEWLINE, char)
                self._advance()
            elif char == '#':
                self._handle_comment()
            elif char == '"':
                self._handle_quoted_string()
            elif char == '$':
                self._handle_variable_or_generator()
            elif char == '[':
                if self._peek() == '[' or self._peek() == '=':
                    self._handle_bracket_argument()
                else:
                    self._handle_identifier()
            elif char == '(':
                self._add_token(TokenType.LPAREN, char)
                self._advance()
            elif char == ')':
                self._add_token(TokenType.RPAREN, char)
                self._advance()
            elif char.isalnum() or char in '_.-+/:':
                self._handle_identifier()
            else:
                self._advance()  # Skip unknown characters
        
        self._add_token(TokenType.EOF, "")
        return self.tokens
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return '\0'
    
    def _peek(self, offset: int = 1) -> str:
        """Peek at character at current position + offset."""
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else '\0'
    
    def _add_token(self, token_type: TokenType, value: str):
        """Add a token to the tokens list."""
        token = Token(token_type, value, self.line, self.column - len(value))
        self.tokens.append(token)
    
    def _skip_whitespace(self):
        """Skip whitespace characters except newlines."""
        while (self.position < len(self.source) and 
               self.source[self.position] in ' \t\r'):
            self._advance()
    
    def _handle_comment(self):
        """Handle comment line."""
        start = self.position
        while (self.position < len(self.source) and 
               self.source[self.position] != '\n'):
            self._advance()
        
        comment_text = self.source[start:self.position]
        self._add_token(TokenType.COMMENT, comment_text)
    
    def _handle_quoted_string(self):
        """Handle quoted string."""
        start = self.position
        self._advance()  # consume opening quote
        
        while (self.position < len(self.source) and 
               self.source[self.position] != '"'):
            if self.source[self.position] == '\\':
                self._advance()  # skip escape character
            self._advance()
        
        if self.position < len(self.source):
            self._advance()  # consume closing quote
        
        quoted_str = self.source[start:self.position]
        self._add_token(TokenType.QUOTED_ARGUMENT, quoted_str)
    
    def _handle_variable_or_generator(self):
        """Handle variable reference ${VAR} or generator expression $<...>."""
        start = self.position
        self._advance()  # consume $
        
        if self.position < len(self.source):
            if self.source[self.position] == '{':
                # Variable reference ${VAR}
                self._advance()  # consume {
                while (self.position < len(self.source) and 
                       self.source[self.position] != '}'):
                    self._advance()
                if self.position < len(self.source):
                    self._advance()  # consume }
                
                var_ref = self.source[start:self.position]
                self._add_token(TokenType.VARIABLE_REF, var_ref)
            elif self.source[self.position] == '<':
                # Generator expression $<...>
                self._advance()  # consume <
                bracket_count = 1
                while self.position < len(self.source) and bracket_count > 0:
                    if self.source[self.position] == '<':
                        bracket_count += 1
                    elif self.source[self.position] == '>':
                        bracket_count -= 1
                    self._advance()
                
                gen_expr = self.source[start:self.position]
                self._add_token(TokenType.GENERATOR_EXPR, gen_expr)
            else:
                # Just a $ character
                self._add_token(TokenType.IDENTIFIER, '$')
    
    def _handle_bracket_argument(self):
        """Handle bracket argument [[...]]."""
        start = self.position
        
        # Count = signs for bracket level
        self._advance()  # consume [
        level = 0
        while (self.position < len(self.source) and 
               self.source[self.position] == '='):
            level += 1
            self._advance()
        
        if self.position < len(self.source) and self.source[self.position] == '[':
            self._advance()  # consume second [
            
            # Find closing bracket with same level
            while self.position < len(self.source):
                if self.source[self.position] == ']':
                    close_level = 0
                    temp_pos = self.position + 1
                    while (temp_pos < len(self.source) and 
                           self.source[temp_pos] == '='):
                        close_level += 1
                        temp_pos += 1
                    
                    if (temp_pos < len(self.source) and 
                        self.source[temp_pos] == ']' and 
                        close_level == level):
                        # Found matching closing bracket
                        self.position = temp_pos + 1
                        self.column += close_level + 2
                        break
                
                self._advance()
        
        bracket_arg = self.source[start:self.position]
        self._add_token(TokenType.BRACKET_ARGUMENT, bracket_arg)
    
    def _handle_identifier(self):
        """Handle identifiers and unquoted arguments."""
        start = self.position
        
        while (self.position < len(self.source) and 
               not self.source[self.position].isspace() and
               self.source[self.position] not in '()#"'):
            self._advance()
        
        identifier = self.source[start:self.position]
        self._add_token(TokenType.IDENTIFIER, identifier)


class CMakeParser:
    """Parser for CMake files."""
    
    def __init__(self, tokens: List[Token], file_path: Optional[str] = None):
        self.tokens = tokens
        self.file_path = file_path
        self.position = 0
        self.current_token = tokens[0] if tokens else None
        
    def parse(self) -> CMakeFile:
        """Parse tokens into CMake AST."""
        statements = []
        cmake_minimum_required = None
        project_name = None
        
        self._skip_newlines()
        while self.current_token and not self._match(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
                
                # Extract metadata
                if isinstance(stmt, CommandInvocation):
                    if stmt.command_name.lower() == "cmake_minimum_required":
                        cmake_minimum_required = self._extract_version(stmt)
                    elif stmt.command_name.lower() == "project":
                        project_name = self._extract_project_name(stmt)
            
            self._skip_newlines()
        
        return CMakeFile(
            file_path=self.file_path or "CMakeLists.txt",
            statements=statements,
            cmake_minimum_required=cmake_minimum_required,
            project_name=project_name
        )
    
    def _advance(self) -> Optional[Token]:
        """Advance to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
        return self.current_token
    
    def _match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token and self.current_token.type in token_types
    
    def _consume(self, token_type: TokenType) -> Token:
        """Consume token of expected type."""
        if not self.current_token or self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")
        token = self.current_token
        self._advance()
        return token
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match(TokenType.NEWLINE, TokenType.COMMENT):
            self._advance()
    
    def _parse_statement(self) -> Optional[CMakeStatement]:
        """Parse a statement."""
        if self._match(TokenType.IDENTIFIER):
            return self._parse_command_invocation()
        elif self._match(TokenType.COMMENT):
            self._advance()  # Skip comments
            return None
        else:
            self._advance()  # Skip unknown tokens
            return None
    
    def _parse_command_invocation(self) -> CommandInvocation:
        """Parse a command invocation."""
        command_token = self._consume(TokenType.IDENTIFIER)
        command_name = command_token.value.lower()
        
        self._consume(TokenType.LPAREN)
        
        arguments = []
        while not self._match(TokenType.RPAREN, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.COMMENT):
                self._advance()
                continue
            
            arg = self._parse_argument()
            if arg:
                arguments.append(arg)
        
        self._consume(TokenType.RPAREN)
        
        # Create specific command types for common commands
        if command_name == "project":
            return self._create_project_command(arguments)
        elif command_name == "add_executable":
            return self._create_add_executable(arguments)
        elif command_name == "add_library":
            return self._create_add_library(arguments)
        elif command_name == "target_link_libraries":
            return self._create_target_link_libraries(arguments)
        elif command_name == "set":
            return self._create_set_command(arguments)
        elif command_name == "find_package":
            return self._create_find_package(arguments)
        else:
            return CommandInvocation(command_name=command_name, arguments=arguments)
    
    def _parse_argument(self) -> Optional[CMakeExpression]:
        """Parse a command argument."""
        if self._match(TokenType.IDENTIFIER):
            value = self.current_token.value
            self._advance()
            return StringLiteral(value)
        elif self._match(TokenType.QUOTED_ARGUMENT):
            value = self.current_token.value
            self._advance()
            return QuotedArgument(value.strip('"'))
        elif self._match(TokenType.BRACKET_ARGUMENT):
            value = self.current_token.value
            self._advance()
            return BracketArgument(value)
        elif self._match(TokenType.VARIABLE_REF):
            value = self.current_token.value
            self._advance()
            # Extract variable name from ${VAR}
            var_name = value[2:-1] if value.startswith('${') and value.endswith('}') else value
            return VariableRef(var_name)
        elif self._match(TokenType.GENERATOR_EXPR):
            value = self.current_token.value
            self._advance()
            return GeneratorExpr(value)
        else:
            self._advance()  # Skip unknown tokens
            return None
    
    def _create_project_command(self, arguments: List[CMakeExpression]) -> ProjectCommand:
        """Create a project command from arguments."""
        if not arguments:
            return ProjectCommand(name="")
        
        name = self._extract_string_value(arguments[0])
        version = None
        languages = []
        
        # Parse remaining arguments (simplified)
        for i, arg in enumerate(arguments[1:], 1):
            arg_str = self._extract_string_value(arg).upper()
            if arg_str == "VERSION" and i + 1 < len(arguments):
                version = self._extract_string_value(arguments[i + 1])
            elif arg_str in ["C", "CXX", "FORTRAN", "JAVA", "CUDA", "OBJC", "OBJCXX"]:
                languages.append(arg_str)
        
        return ProjectCommand(name=name, version=version, languages=languages)
    
    def _create_add_executable(self, arguments: List[CMakeExpression]) -> AddExecutable:
        """Create an add_executable command from arguments."""
        if not arguments:
            return AddExecutable(name="")
        
        name = self._extract_string_value(arguments[0])
        sources = []
        
        for arg in arguments[1:]:
            arg_str = self._extract_string_value(arg)
            if arg_str not in ["WIN32", "MACOSX_BUNDLE", "EXCLUDE_FROM_ALL"]:
                sources.append(arg_str)
        
        return AddExecutable(name=name, sources=sources)
    
    def _create_add_library(self, arguments: List[CMakeExpression]) -> AddLibrary:
        """Create an add_library command from arguments."""
        if not arguments:
            return AddLibrary(name="")
        
        name = self._extract_string_value(arguments[0])
        library_type = "STATIC"
        sources = []
        
        for arg in arguments[1:]:
            arg_str = self._extract_string_value(arg).upper()
            if arg_str in ["STATIC", "SHARED", "MODULE", "INTERFACE", "OBJECT"]:
                library_type = arg_str
            elif arg_str not in ["EXCLUDE_FROM_ALL"]:
                sources.append(self._extract_string_value(arg))
        
        return AddLibrary(name=name, library_type=library_type, sources=sources)
    
    def _create_target_link_libraries(self, arguments: List[CMakeExpression]) -> TargetLinkLibraries:
        """Create a target_link_libraries command from arguments."""
        if not arguments:
            return TargetLinkLibraries(target="")
        
        target = self._extract_string_value(arguments[0])
        scope = "PUBLIC"
        libraries = []
        
        for arg in arguments[1:]:
            arg_str = self._extract_string_value(arg).upper()
            if arg_str in ["PUBLIC", "PRIVATE", "INTERFACE"]:
                scope = arg_str
            else:
                libraries.append(self._extract_string_value(arg))
        
        return TargetLinkLibraries(target=target, scope=scope, libraries=libraries)
    
    def _create_set_command(self, arguments: List[CMakeExpression]) -> SetCommand:
        """Create a set command from arguments."""
        if not arguments:
            return SetCommand(variable="", value="")
        
        variable = self._extract_string_value(arguments[0])
        
        if len(arguments) == 1:
            return SetCommand(variable=variable, value="")
        elif len(arguments) == 2:
            value = self._extract_string_value(arguments[1])
            return SetCommand(variable=variable, value=value)
        else:
            # Multiple values - create list
            values = [self._extract_string_value(arg) for arg in arguments[1:]]
            return SetCommand(variable=variable, value=values)
    
    def _create_find_package(self, arguments: List[CMakeExpression]) -> FindPackage:
        """Create a find_package command from arguments."""
        if not arguments:
            return FindPackage(package_name="")
        
        package_name = self._extract_string_value(arguments[0])
        version = None
        required = False
        quiet = False
        components = []
        
        for arg in arguments[1:]:
            arg_str = self._extract_string_value(arg).upper()
            if arg_str == "REQUIRED":
                required = True
            elif arg_str == "QUIET":
                quiet = True
            elif arg_str == "COMPONENTS":
                # Remaining arguments are components
                break
            elif not arg_str.startswith(("CONFIG", "MODULE", "NO_")):
                if not version and re.match(r'^\d+(\.\d+)*$', arg_str):
                    version = arg_str
                else:
                    components.append(arg_str)
        
        return FindPackage(
            package_name=package_name,
            version=version,
            required=required,
            quiet=quiet,
            components=components
        )
    
    def _extract_string_value(self, expr: CMakeExpression) -> str:
        """Extract string value from expression."""
        if isinstance(expr, StringLiteral):
            return expr.value
        elif isinstance(expr, QuotedArgument):
            return expr.content
        elif isinstance(expr, BracketArgument):
            return expr.content
        elif isinstance(expr, VariableRef):
            return f"${{{expr.variable}}}"
        elif isinstance(expr, GeneratorExpr):
            return expr.expression
        else:
            return str(expr)
    
    def _extract_version(self, stmt: CommandInvocation) -> Optional[str]:
        """Extract version from cmake_minimum_required command."""
        for i, arg in enumerate(stmt.arguments):
            if self._extract_string_value(arg).upper() == "VERSION" and i + 1 < len(stmt.arguments):
                return self._extract_string_value(stmt.arguments[i + 1])
        return None
    
    def _extract_project_name(self, stmt: CommandInvocation) -> Optional[str]:
        """Extract project name from project command."""
        if stmt.arguments:
            return self._extract_string_value(stmt.arguments[0])
        return None


# Public API functions
def parse_cmake(source: str, file_path: Optional[str] = None) -> CMakeFile:
    """Parse CMake source code into AST."""
    lexer = CMakeLexer(source, file_path)
    tokens = lexer.tokenize()
    parser = CMakeParser(tokens, file_path)
    return parser.parse()


# Export classes and functions
__all__ = ['CMakeLexer', 'CMakeParser', 'parse_cmake', 'Token', 'TokenType'] 