"""
Tcl Parser for Runa Universal Translation Platform
Parses Tcl (Tool Command Language) source code

Key features:
- Command-based syntax parsing
- Variable, command, and backslash substitutions
- String and list processing
- Control structures and procedures
- Everything-is-a-string philosophy
- Flexible word parsing with quotes and braces
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass
import logging

from .tcl_ast import *

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Base parse error class."""
    pass

class TclTokenType(Enum):
    """Tcl token types"""
    # Basic tokens
    WORD = "WORD"
    QUOTED_WORD = "QUOTED_WORD"
    BRACED_WORD = "BRACED_WORD"
    VARIABLE = "VARIABLE"
    COMMAND_SUB = "COMMAND_SUB"
    
    # Separators
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    SEMICOLON = "SEMICOLON"
    
    # Comments
    COMMENT = "COMMENT"
    
    # Special characters
    DOLLAR = "$"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    QUOTE = '"'
    BACKSLASH = "\\"
    
    # End of file
    EOF = "EOF"

@dataclass
class TclToken:
    """Tcl token with type, value, and location"""
    type: TclTokenType
    value: str
    line: int
    column: int

class TclLexer:
    """Tcl lexer supporting flexible word parsing and substitutions"""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[TclToken] = []
        
    def tokenize(self) -> List[TclToken]:
        """Tokenize Tcl source code"""
        while self.position < len(self.source):
            if self._at_end():
                break
                
            char = self._current_char()
            
            # Skip whitespace (except newlines)
            if char in ' \t\r':
                self._skip_whitespace()
                continue
            
            # Handle newlines (command separators)
            elif char == '\n':
                self._add_token(TclTokenType.NEWLINE, '\n')
                self._advance()
                continue
            
            # Handle semicolons (command separators)
            elif char == ';':
                self._add_token(TclTokenType.SEMICOLON, ';')
                self._advance()
                continue
            
            # Handle comments
            elif char == '#':
                self._parse_comment()
                continue
            
            # Handle quoted strings
            elif char == '"':
                self._parse_quoted_string()
                continue
            
            # Handle braced strings
            elif char == '{':
                self._parse_braced_string()
                continue
            
            # Handle variable substitution
            elif char == '$':
                self._parse_variable()
                continue
            
            # Handle command substitution
            elif char == '[':
                self._parse_command_substitution()
                continue
            
            # Handle backslash escapes
            elif char == '\\':
                self._parse_backslash_escape()
                continue
            
            # Handle regular words
            else:
                self._parse_word()
                continue
        
        self._add_token(TclTokenType.EOF, "")
        return self.tokens
    
    def _current_char(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def _peek_char(self, offset: int = 1) -> str:
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def _advance(self) -> str:
        char = self._current_char()
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _at_end(self) -> bool:
        return self.position >= len(self.source)
    
    def _skip_whitespace(self):
        while self._current_char() in ' \t\r':
            self._advance()
    
    def _parse_comment(self):
        """Parse Tcl comment"""
        start_pos = self.position
        value = ""
        
        self._advance()  # Skip #
        
        while self._current_char() not in ['\n', '\0']:
            value += self._advance()
        
        self._add_token(TclTokenType.COMMENT, value)
    
    def _parse_quoted_string(self):
        """Parse quoted string with substitutions"""
        start_pos = self.position
        value = ""
        
        self._advance()  # Skip opening quote
        
        while self._current_char() not in ['"', '\0']:
            char = self._current_char()
            
            if char == '\\':
                # Handle escape sequences
                self._advance()
                next_char = self._current_char()
                if next_char in '"\\$[]{}':
                    value += next_char
                    self._advance()
                elif next_char == 'n':
                    value += '\n'
                    self._advance()
                elif next_char == 't':
                    value += '\t'
                    self._advance()
                elif next_char == 'r':
                    value += '\r'
                    self._advance()
                else:
                    value += '\\'
                    if not self._at_end():
                        value += self._advance()
            else:
                value += self._advance()
        
        if self._current_char() == '"':
            self._advance()  # Skip closing quote
        
        self._add_token(TclTokenType.QUOTED_WORD, value)
    
    def _parse_braced_string(self):
        """Parse braced string (no substitutions)"""
        start_pos = self.position
        value = ""
        brace_count = 0
        
        self._advance()  # Skip opening brace
        brace_count = 1
        
        while brace_count > 0 and not self._at_end():
            char = self._current_char()
            
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            
            if brace_count > 0:
                value += self._advance()
            else:
                self._advance()  # Skip closing brace
        
        self._add_token(TclTokenType.BRACED_WORD, value)
    
    def _parse_variable(self):
        """Parse variable substitution"""
        start_pos = self.position
        
        self._advance()  # Skip $
        
        if self._current_char() == '{':
            # ${variable} form
            self._advance()  # Skip {
            value = ""
            while self._current_char() not in ['}', '\0']:
                value += self._advance()
            if self._current_char() == '}':
                self._advance()  # Skip }
        else:
            # $variable form
            value = ""
            while (self._current_char().isalnum() or 
                   self._current_char() in '_:'):
                value += self._advance()
        
        self._add_token(TclTokenType.VARIABLE, value)
    
    def _parse_command_substitution(self):
        """Parse command substitution"""
        start_pos = self.position
        value = ""
        bracket_count = 0
        
        self._advance()  # Skip [
        bracket_count = 1
        
        while bracket_count > 0 and not self._at_end():
            char = self._current_char()
            
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
            
            if bracket_count > 0:
                value += self._advance()
            else:
                self._advance()  # Skip ]
        
        self._add_token(TclTokenType.COMMAND_SUB, value)
    
    def _parse_backslash_escape(self):
        """Parse backslash escape sequence"""
        start_pos = self.position
        
        self._advance()  # Skip backslash
        
        if not self._at_end():
            escaped_char = self._advance()
            
            # Handle common escape sequences
            if escaped_char == 'n':
                value = '\n'
            elif escaped_char == 't':
                value = '\t'
            elif escaped_char == 'r':
                value = '\r'
            elif escaped_char == '\\':
                value = '\\'
            elif escaped_char == ' ':
                value = ' '
            elif escaped_char == '\n':
                value = ' '  # Line continuation
            else:
                value = escaped_char
            
            self._add_token(TclTokenType.WORD, value)
    
    def _parse_word(self):
        """Parse regular word"""
        value = ""
        
        while (not self._at_end() and 
               self._current_char() not in ' \t\r\n;#"{}[]$\\'):
            value += self._advance()
        
        if value:
            self._add_token(TclTokenType.WORD, value)
    
    def _add_token(self, token_type: TclTokenType, value: str):
        token = TclToken(token_type, value, self.line, self.column - len(value))
        self.tokens.append(token)

class TclParseError(ParseError):
    """Tcl-specific parse error"""
    pass

class TclParser(BaseParser):
    """Tcl parser supporting command-based syntax and substitutions"""
    
    def __init__(self, tokens: Optional[List[TclToken]] = None):
        super().__init__()
        self.tokens = tokens or []
        self.current = 0
        
    def parse(self, source: str) -> TclScript:
        """Parse Tcl source code"""
        try:
            lexer = TclLexer(source)
            self.tokens = lexer.tokenize()
            self.current = 0
            
            return self.parse_script()
            
        except Exception as e:
            logger.error(f"Tcl parse error: {e}")
            raise TclParseError(f"Failed to parse Tcl code: {e}")
    
    def current_token(self) -> TclToken:
        """Get current token"""
        if self.current >= len(self.tokens):
            return TclToken(TclTokenType.EOF, "", 0, 0)
        return self.tokens[self.current]
    
    def advance(self) -> TclToken:
        """Advance to next token"""
        token = self.current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def match(self, *token_types: TclTokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token().type in token_types
    
    def consume(self, token_type: TclTokenType) -> TclToken:
        """Consume token of expected type"""
        if self.match(token_type):
            return self.advance()
        
        current = self.current_token()
        raise TclParseError(f"Expected {token_type}, got {current.type} at line {current.line}")
    
    def parse_script(self) -> TclScript:
        """Parse a Tcl script"""
        commands = []
        
        while not self.match(TclTokenType.EOF):
            # Skip command separators and comments
            if self.match(TclTokenType.NEWLINE, TclTokenType.SEMICOLON, TclTokenType.COMMENT):
                self.advance()
                continue
            
            # Parse command
            command = self.parse_command()
            if command:
                commands.append(command)
        
        return TclScript(commands=commands)
    
    def parse_command(self) -> Optional[TclCommand]:
        """Parse a Tcl command"""
        if self.match(TclTokenType.EOF, TclTokenType.NEWLINE, TclTokenType.SEMICOLON):
            return None
        
        # Get command name
        command_name_word = self.parse_word()
        if not command_name_word:
            return None
        
        command_name = self._word_to_string(command_name_word)
        
        # Parse arguments
        arguments = []
        while (not self.match(TclTokenType.EOF, TclTokenType.NEWLINE, 
                             TclTokenType.SEMICOLON, TclTokenType.COMMENT)):
            arg = self.parse_word()
            if arg:
                arguments.append(arg)
            else:
                break
        
        # Handle special command types
        if command_name in ['if', 'while', 'for', 'foreach', 'switch', 'proc']:
            return self._parse_special_command(command_name, arguments)
        else:
            return TclCommand(command_name=command_name, arguments=arguments)
    
    def parse_word(self) -> Optional[TclWord]:
        """Parse a Tcl word"""
        if self.match(TclTokenType.WORD):
            token = self.advance()
            return TclWord(content=token.value)
        
        elif self.match(TclTokenType.QUOTED_WORD):
            token = self.advance()
            return TclWord(content=token.value, is_quoted=True)
        
        elif self.match(TclTokenType.BRACED_WORD):
            token = self.advance()
            return TclWord(content=token.value, is_braced=True)
        
        elif self.match(TclTokenType.VARIABLE):
            token = self.advance()
            var_sub = TclVariableSubstitution(variable_name=token.value)
            return TclWord(content=[var_sub])
        
        elif self.match(TclTokenType.COMMAND_SUB):
            token = self.advance()
            # Parse the command inside the substitution
            sub_parser = TclParser()
            sub_script = sub_parser.parse(token.value)
            if sub_script.commands:
                cmd_sub = TclCommandSubstitution(command=sub_script.commands[0])
                return TclWord(content=[cmd_sub])
        
        return None
    
    def _parse_special_command(self, command_name: str, arguments: List[TclWord]) -> TclCommand:
        """Parse special Tcl commands with specific syntax"""
        
        if command_name == "if":
            return self._parse_if_command(arguments)
        elif command_name == "while":
            return self._parse_while_command(arguments)
        elif command_name == "for":
            return self._parse_for_command(arguments)
        elif command_name == "foreach":
            return self._parse_foreach_command(arguments)
        elif command_name == "proc":
            return self._parse_proc_command(arguments)
        else:
            # Default to regular command
            return TclCommand(command_name=command_name, arguments=arguments)
    
    def _parse_if_command(self, arguments: List[TclWord]) -> TclIf:
        """Parse if command"""
        if len(arguments) < 2:
            raise TclParseError("if command requires at least condition and then body")
        
        condition = arguments[0]
        then_body = self._parse_script_from_word(arguments[1])
        
        # Handle elseif and else clauses
        elseif_clauses = []
        else_body = None
        
        i = 2
        while i < len(arguments):
            if i + 1 < len(arguments) and self._word_to_string(arguments[i]) == "elseif":
                elseif_condition = arguments[i + 1]
                elseif_body = self._parse_script_from_word(arguments[i + 2]) if i + 2 < len(arguments) else TclScript()
                elseif_clauses.append(TclElseIf(condition=elseif_condition, body=elseif_body))
                i += 3
            elif self._word_to_string(arguments[i]) == "else":
                else_body = self._parse_script_from_word(arguments[i + 1]) if i + 1 < len(arguments) else TclScript()
                break
            else:
                i += 1
        
        return TclIf(
            condition=condition,
            then_body=then_body,
            elseif_clauses=elseif_clauses,
            else_body=else_body
        )
    
    def _parse_while_command(self, arguments: List[TclWord]) -> TclWhile:
        """Parse while command"""
        if len(arguments) < 2:
            raise TclParseError("while command requires condition and body")
        
        condition = arguments[0]
        body = self._parse_script_from_word(arguments[1])
        
        return TclWhile(condition=condition, body=body)
    
    def _parse_for_command(self, arguments: List[TclWord]) -> TclFor:
        """Parse for command"""
        if len(arguments) < 4:
            raise TclParseError("for command requires init, condition, increment, and body")
        
        init = self._parse_script_from_word(arguments[0])
        condition = arguments[1]
        increment = self._parse_script_from_word(arguments[2])
        body = self._parse_script_from_word(arguments[3])
        
        return TclFor(
            init=init,
            condition=condition,
            increment=increment,
            body=body
        )
    
    def _parse_foreach_command(self, arguments: List[TclWord]) -> TclForeach:
        """Parse foreach command"""
        if len(arguments) < 3:
            raise TclParseError("foreach command requires variable, list, and body")
        
        variable = self._word_to_string(arguments[0])
        list_expr = arguments[1]
        body = self._parse_script_from_word(arguments[2])
        
        return TclForeach(
            variables=[variable],
            list_expr=list_expr,
            body=body
        )
    
    def _parse_proc_command(self, arguments: List[TclWord]) -> TclProc:
        """Parse proc command"""
        if len(arguments) < 3:
            raise TclParseError("proc command requires name, parameters, and body")
        
        name = self._word_to_string(arguments[0])
        
        # Parse parameter list
        param_list_str = self._word_to_string(arguments[1])
        parameters = param_list_str.split() if param_list_str else []
        
        body = self._parse_script_from_word(arguments[2])
        
        return TclProc(name=name, parameters=parameters, body=body)
    
    def _parse_script_from_word(self, word: TclWord) -> TclScript:
        """Parse a script from a word (typically braced)"""
        content = self._word_to_string(word)
        sub_parser = TclParser()
        return sub_parser.parse(content)
    
    def _word_to_string(self, word: TclWord) -> str:
        """Convert a word to string"""
        if isinstance(word.content, str):
            return word.content
        elif isinstance(word.content, list):
            # Handle substitutions - simplified for now
            result = ""
            for item in word.content:
                if isinstance(item, str):
                    result += item
                elif isinstance(item, TclVariableSubstitution):
                    result += f"${item.variable_name}"
                elif isinstance(item, TclCommandSubstitution):
                    result += "[command]"  # Simplified
            return result
        else:
            return str(word.content) 