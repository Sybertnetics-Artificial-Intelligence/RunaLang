#!/usr/bin/env python3
"""
Shell Script Parser and Lexer

Comprehensive shell script parsing implementation supporting POSIX shell,
Bash, and modern shell features with error recovery.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .shell_ast import *


class ShellTokenType(Enum):
    """Shell token types."""
    # Literals and identifiers
    WORD = auto()
    STRING = auto()
    NUMBER = auto()
    VARIABLE = auto()
    
    # Operators
    PIPE = auto()
    AND = auto()
    OR = auto()
    SEMICOLON = auto()
    AMPERSAND = auto()
    
    # Redirections
    REDIRECT_OUT = auto()
    REDIRECT_APPEND = auto()
    REDIRECT_IN = auto()
    REDIRECT_HERE_DOC = auto()
    REDIRECT_HERE_STRING = auto()
    REDIRECT_ERR = auto()
    REDIRECT_BOTH = auto()
    
    # Parentheses and brackets
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    
    # Keywords
    IF = auto()
    THEN = auto()
    ELSE = auto()
    ELIF = auto()
    FI = auto()
    CASE = auto()
    ESAC = auto()
    FOR = auto()
    WHILE = auto()
    UNTIL = auto()
    DO = auto()
    DONE = auto()
    FUNCTION = auto()
    IN = auto()
    
    # Special
    ASSIGNMENT = auto()
    EXPANSION = auto()
    COMMAND_SUBSTITUTION = auto()
    ARITHMETIC_EXPANSION = auto()
    COMMENT = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class ShellToken:
    """Shell token."""
    type: ShellTokenType
    value: str
    line: int
    column: int


class ShellLexer:
    """Shell lexer for tokenizing shell scripts."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset lexer state."""
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.pos = 0
        self.text = ""
        self.in_string = False
        self.string_delimiter = ""
    
    def tokenize(self, text: str) -> List[ShellToken]:
        """Tokenize shell script text."""
        self.reset()
        self.text = text
        
        while self.pos < len(self.text):
            if self._is_whitespace() and not self.in_string:
                self._skip_whitespace()
            elif self._match('\n'):
                self._add_token(ShellTokenType.NEWLINE, '\n')
                self._advance()
            elif self._match('#') and not self.in_string:
                self._tokenize_comment()
            elif self._match_string_start():
                self._tokenize_string()
            elif self._match('$'):
                self._tokenize_expansion()
            elif self._match('|'):
                if self._peek(1) == '|':
                    self._advance()
                    self._advance()
                    self._add_token(ShellTokenType.OR, '||')
                else:
                    self._advance()
                    self._add_token(ShellTokenType.PIPE, '|')
            elif self._match('&'):
                if self._peek(1) == '&':
                    self._advance()
                    self._advance()
                    self._add_token(ShellTokenType.AND, '&&')
                elif self._peek(1) == '>':
                    self._advance()
                    self._advance()
                    self._add_token(ShellTokenType.REDIRECT_BOTH, '&>')
                else:
                    self._advance()
                    self._add_token(ShellTokenType.AMPERSAND, '&')
            elif self._match('>'):
                if self._peek(1) == '>':
                    self._advance()
                    self._advance()
                    self._add_token(ShellTokenType.REDIRECT_APPEND, '>>')
                else:
                    self._advance()
                    self._add_token(ShellTokenType.REDIRECT_OUT, '>')
            elif self._match('<'):
                if self._peek(1) == '<':
                    if self._peek(2) == '<':
                        self._advance()
                        self._advance()
                        self._advance()
                        self._add_token(ShellTokenType.REDIRECT_HERE_STRING, '<<<')
                    else:
                        self._advance()
                        self._advance()
                        self._add_token(ShellTokenType.REDIRECT_HERE_DOC, '<<')
                else:
                    self._advance()
                    self._add_token(ShellTokenType.REDIRECT_IN, '<')
            elif self._match('2>'):
                if self._peek(2) == '>':
                    self._advance()
                    self._advance()
                    self._advance()
                    self._add_token(ShellTokenType.REDIRECT_ERR, '2>>')
                else:
                    self._advance()
                    self._advance()
                    self._add_token(ShellTokenType.REDIRECT_ERR, '2>')
            elif self._match(';'):
                self._advance()
                self._add_token(ShellTokenType.SEMICOLON, ';')
            elif self._match('('):
                self._advance()
                self._add_token(ShellTokenType.LEFT_PAREN, '(')
            elif self._match(')'):
                self._advance()
                self._add_token(ShellTokenType.RIGHT_PAREN, ')')
            elif self._match('['):
                self._advance()
                self._add_token(ShellTokenType.LEFT_BRACKET, '[')
            elif self._match(']'):
                self._advance()
                self._add_token(ShellTokenType.RIGHT_BRACKET, ']')
            elif self._match('{'):
                self._advance()
                self._add_token(ShellTokenType.LEFT_BRACE, '{')
            elif self._match('}'):
                self._advance()
                self._add_token(ShellTokenType.RIGHT_BRACE, '}')
            elif self._is_word_start():
                self._tokenize_word()
            else:
                self._advance()  # Skip unknown characters
        
        self._add_token(ShellTokenType.EOF, '')
        return self.tokens
    
    def _peek(self, offset: int = 0) -> str:
        """Peek at character at current position + offset."""
        pos = self.pos + offset
        return self.text[pos] if pos < len(self.text) else ''
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            if char == '\n':
                self.current_line += 1
                self.current_column = 1
            else:
                self.current_column += 1
            return char
        return ''
    
    def _match(self, pattern: str) -> bool:
        """Check if text at current position matches pattern."""
        return self.text[self.pos:self.pos + len(pattern)] == pattern
    
    def _is_whitespace(self) -> bool:
        """Check if current character is whitespace (excluding newline)."""
        return self.pos < len(self.text) and self.text[self.pos] in ' \t'
    
    def _is_word_start(self) -> bool:
        """Check if current character can start a word."""
        char = self._peek()
        return char.isalnum() or char in '_-./~'
    
    def _is_word_char(self) -> bool:
        """Check if current character can be part of a word."""
        char = self._peek()
        return char.isalnum() or char in '_-./~=:'
    
    def _match_string_start(self) -> bool:
        """Check if at start of string."""
        return self._peek() in ('"', "'")
    
    def _skip_whitespace(self):
        """Skip whitespace characters (excluding newline)."""
        while self._is_whitespace():
            self._advance()
    
    def _tokenize_comment(self):
        """Tokenize shell comment."""
        self._advance()  # Skip #
        
        comment_text = ""
        while self.pos < len(self.text) and self._peek() != '\n':
            comment_text += self._advance()
        
        self._add_token(ShellTokenType.COMMENT, comment_text)
    
    def _tokenize_string(self):
        """Tokenize string literal."""
        quote_char = self._advance()  # Get quote character
        string_value = ""
        
        while self.pos < len(self.text):
            char = self._peek()
            if char == quote_char:
                self._advance()  # Skip closing quote
                break
            elif char == '\\' and quote_char == '"':
                self._advance()  # Skip escape character
                escaped = self._advance()
                if escaped == 'n':
                    string_value += '\n'
                elif escaped == 't':
                    string_value += '\t'
                elif escaped == 'r':
                    string_value += '\r'
                elif escaped == '\\':
                    string_value += '\\'
                elif escaped == '"':
                    string_value += '"'
                elif escaped == '$':
                    string_value += '$'
                else:
                    string_value += escaped
            else:
                string_value += self._advance()
        
        self._add_token(ShellTokenType.STRING, string_value)
    
    def _tokenize_expansion(self):
        """Tokenize shell expansion."""
        self._advance()  # Skip $
        
        if self._match('('):
            # Command substitution or arithmetic expansion
            if self._peek(1) == '(':
                # Arithmetic expansion $((expr))
                self._advance()  # Skip first (
                self._advance()  # Skip second (
                
                expr = ""
                paren_count = 2
                while self.pos < len(self.text) and paren_count > 0:
                    char = self._advance()
                    if char == '(':
                        paren_count += 1
                        expr += char
                    elif char == ')':
                        paren_count -= 1
                        if paren_count > 0:
                            expr += char
                    else:
                        expr += char
                
                self._add_token(ShellTokenType.ARITHMETIC_EXPANSION, expr)
            else:
                # Command substitution $(cmd)
                self._advance()  # Skip (
                
                cmd = ""
                paren_count = 1
                while self.pos < len(self.text) and paren_count > 0:
                    char = self._advance()
                    if char == '(':
                        paren_count += 1
                        cmd += char
                    elif char == ')':
                        paren_count -= 1
                        if paren_count > 0:
                            cmd += char
                    else:
                        cmd += char
                
                self._add_token(ShellTokenType.COMMAND_SUBSTITUTION, cmd)
        
        elif self._match('{'):
            # Parameter expansion ${var}
            self._advance()  # Skip {
            
            expansion = ""
            while self.pos < len(self.text) and self._peek() != '}':
                expansion += self._advance()
            
            if self._peek() == '}':
                self._advance()  # Skip }
            
            self._add_token(ShellTokenType.EXPANSION, expansion)
        
        else:
            # Simple variable $var
            var_name = ""
            while self._is_word_char():
                var_name += self._advance()
            
            self._add_token(ShellTokenType.VARIABLE, var_name)
    
    def _tokenize_word(self):
        """Tokenize word or keyword."""
        word = ""
        
        # Check for assignment (word=value)
        start_pos = self.pos
        temp_word = ""
        while self._is_word_char() or self._peek() == '=':
            temp_word += self._advance()
        
        if '=' in temp_word and not temp_word.startswith('='):
            # This is an assignment
            self._add_token(ShellTokenType.ASSIGNMENT, temp_word)
            return
        
        # Reset position and parse as regular word
        self.pos = start_pos
        
        while self._is_word_char():
            word += self._advance()
        
        # Check if word is a keyword
        keywords = {
            'if': ShellTokenType.IF,
            'then': ShellTokenType.THEN,
            'else': ShellTokenType.ELSE,
            'elif': ShellTokenType.ELIF,
            'fi': ShellTokenType.FI,
            'case': ShellTokenType.CASE,
            'esac': ShellTokenType.ESAC,
            'for': ShellTokenType.FOR,
            'while': ShellTokenType.WHILE,
            'until': ShellTokenType.UNTIL,
            'do': ShellTokenType.DO,
            'done': ShellTokenType.DONE,
            'function': ShellTokenType.FUNCTION,
            'in': ShellTokenType.IN
        }
        
        token_type = keywords.get(word, ShellTokenType.WORD)
        self._add_token(token_type, word)
    
    def _add_token(self, token_type: ShellTokenType, value: str):
        """Add token to list."""
        self.tokens.append(ShellToken(
            type=token_type,
            value=value,
            line=self.current_line,
            column=self.current_column
        ))


class ShellParser:
    """Shell script parser."""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
    
    def parse(self, text: str) -> ShellScript:
        """Parse shell script text into AST."""
        try:
            lexer = ShellLexer()
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            
            return self._parse_script()
            
        except Exception as e:
            self.logger.error(f"Shell parsing failed: {e}")
            raise RuntimeError(f"Failed to parse shell script: {e}")
    
    def _current_token(self) -> ShellToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ShellToken(ShellTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> ShellToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: ShellTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _match_value(self, value: str) -> bool:
        """Check if current token has specific value."""
        return self._current_token().value == value
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(ShellTokenType.EOF)
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match(ShellTokenType.NEWLINE):
            self._advance()
    
    def _parse_script(self) -> ShellScript:
        """Parse shell script."""
        script = ShellScript()
        
        # Check for shebang
        if self.tokens and self.tokens[0].value.startswith('#!'):
            script.shebang = self.tokens[0].value
            self._advance()
        
        self._skip_newlines()
        
        while not self._is_at_end():
            self._skip_newlines()
            
            if self._is_at_end():
                break
            
            if self._match(ShellTokenType.COMMENT):
                comment = self._parse_comment()
                script.add_comment(comment)
            elif self._match(ShellTokenType.FUNCTION):
                function = self._parse_function_definition()
                if function:
                    script.add_function(function)
            else:
                statement = self._parse_statement()
                if statement:
                    script.add_statement(statement)
            
            self._skip_newlines()
        
        return script
    
    def _parse_statement(self) -> Optional[ShellStatement]:
        """Parse shell statement."""
        if self._match(ShellTokenType.IF):
            return self._parse_if_statement()
        elif self._match(ShellTokenType.CASE):
            return self._parse_case_statement()
        elif self._match(ShellTokenType.FOR):
            return self._parse_for_loop()
        elif self._match(ShellTokenType.WHILE):
            return self._parse_while_loop()
        elif self._match(ShellTokenType.UNTIL):
            return self._parse_until_loop()
        elif self._match(ShellTokenType.ASSIGNMENT):
            return self._parse_assignment()
        elif self._match(ShellTokenType.LEFT_PAREN):
            return self._parse_subshell()
        elif self._match(ShellTokenType.LEFT_BRACE):
            return self._parse_command_group()
        else:
            return self._parse_pipeline()
    
    def _parse_pipeline(self) -> Optional[ShellStatement]:
        """Parse pipeline or simple command."""
        commands = []
        negated = False
        
        # Check for negation
        if self._match_value('!'):
            negated = True
            self._advance()
        
        # Parse first command
        command = self._parse_simple_command()
        if not command:
            return None
        
        commands.append(command)
        
        # Parse additional commands in pipeline
        while self._match(ShellTokenType.PIPE):
            self._advance()  # consume |
            cmd = self._parse_simple_command()
            if cmd:
                commands.append(cmd)
        
        if len(commands) == 1:
            return commands[0]
        else:
            pipeline = ShellPipeline(commands=commands, negated=negated)
            return pipeline
    
    def _parse_simple_command(self) -> Optional[ShellCommand]:
        """Parse simple command."""
        command_parts = []
        redirections = []
        environment = {}
        
        # Parse command and arguments
        while self._match(ShellTokenType.WORD, ShellTokenType.STRING, ShellTokenType.VARIABLE):
            if self._match(ShellTokenType.ASSIGNMENT):
                # Environment variable
                assignment = self._advance().value
                if '=' in assignment:
                    var, val = assignment.split('=', 1)
                    environment[var] = val
            else:
                command_parts.append(self._advance().value)
        
        # Parse redirections
        while self._match(ShellTokenType.REDIRECT_OUT, ShellTokenType.REDIRECT_APPEND,
                          ShellTokenType.REDIRECT_IN, ShellTokenType.REDIRECT_HERE_DOC,
                          ShellTokenType.REDIRECT_HERE_STRING, ShellTokenType.REDIRECT_ERR,
                          ShellTokenType.REDIRECT_BOTH):
            redirection = self._parse_redirection()
            if redirection:
                redirections.append(redirection)
        
        if not command_parts:
            return None
        
        command = ShellCommand(
            command=command_parts[0],
            arguments=command_parts[1:],
            redirections=redirections,
            environment=environment
        )
        
        # Check for background execution
        if self._match(ShellTokenType.AMPERSAND):
            command.background = True
            self._advance()
        
        return command
    
    def _parse_redirection(self) -> Optional[ShellRedirection]:
        """Parse redirection."""
        if not self._match(ShellTokenType.REDIRECT_OUT, ShellTokenType.REDIRECT_APPEND,
                          ShellTokenType.REDIRECT_IN, ShellTokenType.REDIRECT_HERE_DOC,
                          ShellTokenType.REDIRECT_HERE_STRING, ShellTokenType.REDIRECT_ERR,
                          ShellTokenType.REDIRECT_BOTH):
            return None
        
        redirect_token = self._advance()
        
        # Get target
        if self._match(ShellTokenType.WORD, ShellTokenType.STRING):
            target = self._advance().value
        else:
            return None
        
        redirection_type_map = {
            ShellTokenType.REDIRECT_OUT: ">",
            ShellTokenType.REDIRECT_APPEND: ">>",
            ShellTokenType.REDIRECT_IN: "<",
            ShellTokenType.REDIRECT_HERE_DOC: "<<",
            ShellTokenType.REDIRECT_HERE_STRING: "<<<",
            ShellTokenType.REDIRECT_ERR: "2>",
            ShellTokenType.REDIRECT_BOTH: "&>"
        }
        
        redirection_type = redirection_type_map.get(redirect_token.type, ">")
        
        return ShellRedirection(
            redirection_type=redirection_type,
            target=target,
            here_document=redirect_token.type == ShellTokenType.REDIRECT_HERE_DOC,
            here_string=redirect_token.type == ShellTokenType.REDIRECT_HERE_STRING
        )
    
    def _parse_if_statement(self) -> Optional[ShellConditional]:
        """Parse if statement."""
        self._advance()  # consume 'if'
        
        # Parse condition
        condition_parts = []
        while not self._match(ShellTokenType.THEN, ShellTokenType.NEWLINE, ShellTokenType.EOF):
            condition_parts.append(self._advance().value)
        
        condition = " ".join(condition_parts)
        
        if not self._match(ShellTokenType.THEN):
            return None
        
        self._advance()  # consume 'then'
        self._skip_newlines()
        
        # Parse then body
        then_body = []
        while not self._match(ShellTokenType.ELSE, ShellTokenType.ELIF, ShellTokenType.FI, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                then_body.append(stmt)
            else:
                break
        
        # Parse elif clauses
        elif_clauses = []
        while self._match(ShellTokenType.ELIF):
            self._advance()  # consume 'elif'
            
            elif_condition_parts = []
            while not self._match(ShellTokenType.THEN, ShellTokenType.NEWLINE, ShellTokenType.EOF):
                elif_condition_parts.append(self._advance().value)
            
            elif_condition = " ".join(elif_condition_parts)
            
            if not self._match(ShellTokenType.THEN):
                break
            
            self._advance()  # consume 'then'
            self._skip_newlines()
            
            elif_body = []
            while not self._match(ShellTokenType.ELSE, ShellTokenType.ELIF, ShellTokenType.FI, ShellTokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    elif_body.append(stmt)
                else:
                    break
            
            elif_clauses.append((elif_condition, elif_body))
        
        # Parse else body
        else_body = []
        if self._match(ShellTokenType.ELSE):
            self._advance()  # consume 'else'
            self._skip_newlines()
            
            while not self._match(ShellTokenType.FI, ShellTokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    else_body.append(stmt)
                else:
                    break
        
        if self._match(ShellTokenType.FI):
            self._advance()  # consume 'fi'
        
        conditional = ShellConditional(
            conditional_type="if",
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            elif_clauses=elif_clauses
        )
        
        return conditional
    
    def _parse_case_statement(self) -> Optional[ShellConditional]:
        """Parse case statement."""
        self._advance()  # consume 'case'
        
        # Parse expression
        if not self._match(ShellTokenType.WORD, ShellTokenType.VARIABLE):
            return None
        
        expression = self._advance().value
        
        if not self._match(ShellTokenType.IN):
            return None
        
        self._advance()  # consume 'in'
        self._skip_newlines()
        
        # Parse case patterns
        case_patterns = []
        while not self._match(ShellTokenType.ESAC, ShellTokenType.EOF):
            # Parse pattern
            pattern_parts = []
            while not self._match(ShellTokenType.RIGHT_PAREN, ShellTokenType.NEWLINE, ShellTokenType.EOF):
                pattern_parts.append(self._advance().value)
            
            if not pattern_parts:
                break
            
            pattern = " ".join(pattern_parts)
            
            if self._match(ShellTokenType.RIGHT_PAREN):
                self._advance()  # consume ')'
            
            self._skip_newlines()
            
            # Parse statements
            statements = []
            while not self._match(ShellTokenType.SEMICOLON, ShellTokenType.ESAC, ShellTokenType.EOF):
                if self._match_value(';;'):
                    break
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
                else:
                    break
            
            case_patterns.append((pattern, statements))
            
            # Skip ;; if present
            if self._match_value(';;'):
                self._advance()
                self._advance()
            
            self._skip_newlines()
        
        if self._match(ShellTokenType.ESAC):
            self._advance()  # consume 'esac'
        
        conditional = ShellConditional(
            conditional_type="case",
            condition=expression,
            case_patterns=case_patterns
        )
        
        return conditional
    
    def _parse_for_loop(self) -> Optional[ShellLoop]:
        """Parse for loop."""
        self._advance()  # consume 'for'
        
        # Parse variable
        if not self._match(ShellTokenType.WORD):
            return None
        
        variable = self._advance().value
        
        # Parse 'in' clause
        iterable = ""
        if self._match(ShellTokenType.IN):
            self._advance()  # consume 'in'
            
            iterable_parts = []
            while not self._match(ShellTokenType.DO, ShellTokenType.NEWLINE, ShellTokenType.EOF):
                iterable_parts.append(self._advance().value)
            
            iterable = " ".join(iterable_parts)
        
        if not self._match(ShellTokenType.DO):
            return None
        
        self._advance()  # consume 'do'
        self._skip_newlines()
        
        # Parse loop body
        body = []
        while not self._match(ShellTokenType.DONE, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if self._match(ShellTokenType.DONE):
            self._advance()  # consume 'done'
        
        loop = ShellLoop(
            loop_type="for",
            condition=f"{variable} in {iterable}",
            variable=variable,
            iterable=iterable,
            body=body
        )
        
        return loop
    
    def _parse_while_loop(self) -> Optional[ShellLoop]:
        """Parse while loop."""
        self._advance()  # consume 'while'
        
        # Parse condition
        condition_parts = []
        while not self._match(ShellTokenType.DO, ShellTokenType.NEWLINE, ShellTokenType.EOF):
            condition_parts.append(self._advance().value)
        
        condition = " ".join(condition_parts)
        
        if not self._match(ShellTokenType.DO):
            return None
        
        self._advance()  # consume 'do'
        self._skip_newlines()
        
        # Parse loop body
        body = []
        while not self._match(ShellTokenType.DONE, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if self._match(ShellTokenType.DONE):
            self._advance()  # consume 'done'
        
        loop = ShellLoop(
            loop_type="while",
            condition=condition,
            body=body
        )
        
        return loop
    
    def _parse_until_loop(self) -> Optional[ShellLoop]:
        """Parse until loop."""
        self._advance()  # consume 'until'
        
        # Parse condition
        condition_parts = []
        while not self._match(ShellTokenType.DO, ShellTokenType.NEWLINE, ShellTokenType.EOF):
            condition_parts.append(self._advance().value)
        
        condition = " ".join(condition_parts)
        
        if not self._match(ShellTokenType.DO):
            return None
        
        self._advance()  # consume 'do'
        self._skip_newlines()
        
        # Parse loop body
        body = []
        while not self._match(ShellTokenType.DONE, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if self._match(ShellTokenType.DONE):
            self._advance()  # consume 'done'
        
        loop = ShellLoop(
            loop_type="until",
            condition=condition,
            body=body
        )
        
        return loop
    
    def _parse_function_definition(self) -> Optional[ShellFunctionDefinition]:
        """Parse function definition."""
        self._advance()  # consume 'function'
        
        # Parse function name
        if not self._match(ShellTokenType.WORD):
            return None
        
        name = self._advance().value
        
        # Skip optional parentheses
        if self._match(ShellTokenType.LEFT_PAREN):
            self._advance()
            if self._match(ShellTokenType.RIGHT_PAREN):
                self._advance()
        
        # Parse function body
        if not self._match(ShellTokenType.LEFT_BRACE):
            return None
        
        self._advance()  # consume '{'
        self._skip_newlines()
        
        body = []
        while not self._match(ShellTokenType.RIGHT_BRACE, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if self._match(ShellTokenType.RIGHT_BRACE):
            self._advance()  # consume '}'
        
        function = ShellFunctionDefinition(name=name, body=body)
        return function
    
    def _parse_assignment(self) -> Optional[ShellVariableAssignment]:
        """Parse variable assignment."""
        if not self._match(ShellTokenType.ASSIGNMENT):
            return None
        
        assignment_text = self._advance().value
        
        if '=' not in assignment_text:
            return None
        
        variable, value = assignment_text.split('=', 1)
        
        # Check for export, readonly, local prefixes
        export = False
        readonly = False
        local = False
        
        if variable.startswith('export '):
            export = True
            variable = variable[7:]
        elif variable.startswith('readonly '):
            readonly = True
            variable = variable[9:]
        elif variable.startswith('local '):
            local = True
            variable = variable[6:]
        
        assignment = ShellVariableAssignment(
            variable=variable,
            value=value,
            export=export,
            readonly=readonly,
            local=local
        )
        
        return assignment
    
    def _parse_subshell(self) -> Optional[ShellCompoundCommand]:
        """Parse subshell command."""
        self._advance()  # consume '('
        
        body = []
        while not self._match(ShellTokenType.RIGHT_PAREN, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if self._match(ShellTokenType.RIGHT_PAREN):
            self._advance()  # consume ')'
        
        compound = ShellCompoundCommand(command_type="subshell", body=body)
        return compound
    
    def _parse_command_group(self) -> Optional[ShellCompoundCommand]:
        """Parse command group."""
        self._advance()  # consume '{'
        self._skip_newlines()
        
        body = []
        while not self._match(ShellTokenType.RIGHT_BRACE, ShellTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if self._match(ShellTokenType.RIGHT_BRACE):
            self._advance()  # consume '}'
        
        compound = ShellCompoundCommand(command_type="group", body=body)
        return compound
    
    def _parse_comment(self) -> ShellComment:
        """Parse comment."""
        comment_token = self._advance()
        return ShellComment(text=comment_token.value)


# Convenience functions
def parse_shell(text: str) -> ShellScript:
    """Parse shell script text into AST."""
    parser = ShellParser()
    return parser.parse(text)


def parse_shell_file(file_path: str) -> ShellScript:
    """Parse shell script file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_shell(f.read())


def parse_shell_command(command_line: str) -> Optional[ShellCommand]:
    """Parse single shell command."""
    try:
        script = parse_shell(command_line)
        if script.statements and isinstance(script.statements[0], ShellCommand):
            return script.statements[0]
        return None
    except:
        return None


def validate_shell_syntax(text: str) -> Tuple[bool, Optional[str]]:
    """Validate shell script syntax."""
    try:
        parse_shell(text)
        return True, None
    except Exception as e:
        return False, str(e)


def extract_shell_commands(text: str) -> List[str]:
    """Extract all commands from shell script."""
    try:
        script = parse_shell(text)
        commands = []
        
        def extract_commands_from_statements(statements):
            for stmt in statements:
                if isinstance(stmt, ShellCommand):
                    commands.append(stmt.command)
                elif isinstance(stmt, ShellPipeline):
                    for cmd in stmt.commands:
                        commands.append(cmd.command)
                elif isinstance(stmt, (ShellConditional, ShellLoop, ShellFunctionDefinition)):
                    if hasattr(stmt, 'body'):
                        extract_commands_from_statements(stmt.body)
                    if hasattr(stmt, 'then_body'):
                        extract_commands_from_statements(stmt.then_body)
                    if hasattr(stmt, 'else_body'):
                        extract_commands_from_statements(stmt.else_body)
        
        extract_commands_from_statements(script.statements)
        return commands
    except:
        return []


def extract_shell_variables(text: str) -> List[str]:
    """Extract all variable names from shell script."""
    try:
        script = parse_shell(text)
        variables = set()
        
        def extract_vars_from_statements(statements):
            for stmt in statements:
                if isinstance(stmt, ShellVariableAssignment):
                    variables.add(stmt.variable)
                elif hasattr(stmt, 'body'):
                    extract_vars_from_statements(stmt.body)
                elif hasattr(stmt, 'then_body'):
                    extract_vars_from_statements(stmt.then_body)
                elif hasattr(stmt, 'else_body'):
                    extract_vars_from_statements(stmt.else_body)
        
        extract_vars_from_statements(script.statements)
        return list(variables)
    except:
        return []


def minify_shell_simple(text: str) -> str:
    """Simple shell script minification."""
    try:
        script = parse_shell(text)
        from .shell_generator import generate_shell_code, ShellCodeStyle
        return generate_shell_code(script, ShellCodeStyle.MINIFIED)
    except:
        # Fallback: simple regex-based minification
        import re
        minified = re.sub(r'#.*$', '', text, flags=re.MULTILINE)  # Remove comments
        minified = re.sub(r'\n\s*\n', '\n', minified)  # Remove empty lines
        minified = re.sub(r'^\s+', '', minified, flags=re.MULTILINE)  # Remove leading whitespace
        return minified.strip()


def prettify_shell_simple(text: str) -> str:
    """Simple shell script prettification."""
    try:
        script = parse_shell(text)
        from .shell_generator import generate_shell_code, ShellCodeStyle
        return generate_shell_code(script, ShellCodeStyle.PRETTY)
    except:
        return text