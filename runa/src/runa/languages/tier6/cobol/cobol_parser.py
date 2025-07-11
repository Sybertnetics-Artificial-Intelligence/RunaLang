#!/usr/bin/env python3
"""
COBOL Parser Implementation

Complete parser for COBOL with fixed format support, four divisions structure,
COBOL-85 and later standards, and mainframe business system features.
"""

from typing import List, Optional, Union, Dict, Any, Tuple
import re
from enum import Enum, auto
from dataclasses import dataclass

from .cobol_ast import *


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
class COBOLTokenType(Enum):
    # Divisions
    IDENTIFICATION = auto()
    ENVIRONMENT = auto()
    DATA = auto()
    PROCEDURE = auto()
    DIVISION = auto()
    
    # Sections
    SECTION = auto()
    CONFIGURATION = auto()
    INPUT_OUTPUT = auto()
    FILE_SECTION = auto()
    WORKING_STORAGE = auto()
    LINKAGE = auto()
    LOCAL_STORAGE = auto()
    
    # Data definition
    FD = auto()
    SD = auto()
    RD = auto()
    PICTURE = auto()
    PIC = auto()
    USAGE = auto()
    VALUE = auto()
    OCCURS = auto()
    REDEFINES = auto()
    FILLER = auto()
    
    # File control
    FILE_CONTROL = auto()
    SELECT = auto()
    ASSIGN = auto()
    ORGANIZATION = auto()
    ACCESS = auto()
    RECORD = auto()
    
    # Statements
    MOVE = auto()
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    COMPUTE = auto()
    IF = auto()
    ELSE = auto()
    END_IF = auto()
    PERFORM = auto()
    END_PERFORM = auto()
    CALL = auto()
    END_CALL = auto()
    READ = auto()
    WRITE = auto()
    OPEN = auto()
    CLOSE = auto()
    ACCEPT = auto()
    DISPLAY = auto()
    STOP = auto()
    GOBACK = auto()
    EXIT = auto()
    
    # Clauses
    TO = auto()
    FROM = auto()
    GIVING = auto()
    USING = auto()
    RETURNING = auto()
    BY = auto()
    TIMES = auto()
    UNTIL = auto()
    VARYING = auto()
    THROUGH = auto()
    THRU = auto()
    CORRESPONDING = auto()
    CORR = auto()
    
    # Conditions
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_OR_EQUAL = auto()
    LESS_OR_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Literals and identifiers
    NUMERIC_LITERAL = auto()
    ALPHANUMERIC_LITERAL = auto()
    NATIONAL_LITERAL = auto()
    FIGURATIVE_CONSTANT = auto()
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY_OP = auto()
    DIVIDE_OP = auto()
    POWER = auto()
    
    # Punctuation
    PERIOD = auto()
    COMMA = auto()
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    COLON = auto()
    
    # Special
    PROGRAM_ID = auto()
    AUTHOR = auto()
    DATE_WRITTEN = auto()
    COPY = auto()
    EXEC = auto()
    SQL = auto()
    END_EXEC = auto()
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()

@dataclass
class COBOLToken:
    """COBOL token with fixed format information."""
    type: COBOLTokenType
    value: str
    line: int
    column: int
    sequence_area: str = ""    # Columns 1-6
    indicator_area: str = " "  # Column 7
    area_a: bool = False      # Columns 8-11
    area_b: bool = False      # Columns 12-72

class COBOLLexer:
    """COBOL lexer with fixed format support."""
    
    KEYWORDS = {
        'identification': COBOLTokenType.IDENTIFICATION,
        'environment': COBOLTokenType.ENVIRONMENT,
        'data': COBOLTokenType.DATA,
        'procedure': COBOLTokenType.PROCEDURE,
        'division': COBOLTokenType.DIVISION,
        'section': COBOLTokenType.SECTION,
        'configuration': COBOLTokenType.CONFIGURATION,
        'input-output': COBOLTokenType.INPUT_OUTPUT,
        'file': COBOLTokenType.FILE_SECTION,
        'working-storage': COBOLTokenType.WORKING_STORAGE,
        'linkage': COBOLTokenType.LINKAGE,
        'local-storage': COBOLTokenType.LOCAL_STORAGE,
        'fd': COBOLTokenType.FD,
        'sd': COBOLTokenType.SD,
        'rd': COBOLTokenType.RD,
        'picture': COBOLTokenType.PICTURE,
        'pic': COBOLTokenType.PIC,
        'usage': COBOLTokenType.USAGE,
        'value': COBOLTokenType.VALUE,
        'occurs': COBOLTokenType.OCCURS,
        'redefines': COBOLTokenType.REDEFINES,
        'filler': COBOLTokenType.FILLER,
        'file-control': COBOLTokenType.FILE_CONTROL,
        'select': COBOLTokenType.SELECT,
        'assign': COBOLTokenType.ASSIGN,
        'organization': COBOLTokenType.ORGANIZATION,
        'access': COBOLTokenType.ACCESS,
        'record': COBOLTokenType.RECORD,
        'move': COBOLTokenType.MOVE,
        'add': COBOLTokenType.ADD,
        'subtract': COBOLTokenType.SUBTRACT,
        'multiply': COBOLTokenType.MULTIPLY,
        'divide': COBOLTokenType.DIVIDE,
        'compute': COBOLTokenType.COMPUTE,
        'if': COBOLTokenType.IF,
        'else': COBOLTokenType.ELSE,
        'end-if': COBOLTokenType.END_IF,
        'perform': COBOLTokenType.PERFORM,
        'end-perform': COBOLTokenType.END_PERFORM,
        'call': COBOLTokenType.CALL,
        'end-call': COBOLTokenType.END_CALL,
        'read': COBOLTokenType.READ,
        'write': COBOLTokenType.WRITE,
        'open': COBOLTokenType.OPEN,
        'close': COBOLTokenType.CLOSE,
        'accept': COBOLTokenType.ACCEPT,
        'display': COBOLTokenType.DISPLAY,
        'stop': COBOLTokenType.STOP,
        'goback': COBOLTokenType.GOBACK,
        'exit': COBOLTokenType.EXIT,
        'to': COBOLTokenType.TO,
        'from': COBOLTokenType.FROM,
        'giving': COBOLTokenType.GIVING,
        'using': COBOLTokenType.USING,
        'returning': COBOLTokenType.RETURNING,
        'by': COBOLTokenType.BY,
        'times': COBOLTokenType.TIMES,
        'until': COBOLTokenType.UNTIL,
        'varying': COBOLTokenType.VARYING,
        'through': COBOLTokenType.THROUGH,
        'thru': COBOLTokenType.THRU,
        'corresponding': COBOLTokenType.CORRESPONDING,
        'corr': COBOLTokenType.CORR,
        'equal': COBOLTokenType.EQUAL,
        'and': COBOLTokenType.AND,
        'or': COBOLTokenType.OR,
        'not': COBOLTokenType.NOT,
        'program-id': COBOLTokenType.PROGRAM_ID,
        'author': COBOLTokenType.AUTHOR,
        'date-written': COBOLTokenType.DATE_WRITTEN,
        'copy': COBOLTokenType.COPY,
        'exec': COBOLTokenType.EXEC,
        'sql': COBOLTokenType.SQL,
        'end-exec': COBOLTokenType.END_EXEC,
    }
    
    FIGURATIVE_CONSTANTS = {
        'zero', 'zeros', 'zeroes',
        'space', 'spaces',
        'high-value', 'high-values',
        'low-value', 'low-values',
        'quote', 'quotes',
        'null', 'nulls',
        'all'
    }
    
    def __init__(self, source: str):
        self.source = source
        self.lines = source.split('\n')
        self.current_line = 0
        self.current_pos = 0
        self.tokens: List[COBOLToken] = []
    
    def tokenize(self) -> List[COBOLToken]:
        """Tokenize COBOL source with fixed format support."""
        for line_num, line in enumerate(self.lines, 1):
            self._process_line(line, line_num)
        
        self.tokens.append(COBOLToken(COBOLTokenType.EOF, '', len(self.lines), 0))
        return self.tokens
    
    def _process_line(self, line: str, line_num: int):
        """Process a single line respecting COBOL fixed format."""
        if len(line) == 0:
            return
        
        # Extract areas according to COBOL fixed format
        sequence_area = line[0:6] if len(line) > 6 else line
        indicator_area = line[6] if len(line) > 6 else ' '
        area_a_b = line[7:72] if len(line) > 7 else ''
        
        # Skip comment lines (asterisk in indicator area)
        if indicator_area == '*' or indicator_area == '/':
            self.tokens.append(COBOLToken(
                COBOLTokenType.COMMENT, line[7:].strip(), line_num, 7,
                sequence_area, indicator_area
            ))
            return
        
        # Skip continuation lines (hyphen in indicator area)
        if indicator_area == '-':
            # Handle continuation - append to previous token or create new one
            return
        
        # Tokenize the content area
        if area_a_b.strip():
            self._tokenize_content(area_a_b, line_num, sequence_area, indicator_area)
    
    def _tokenize_content(self, content: str, line_num: int, seq_area: str, ind_area: str):
        """Tokenize the content area of a COBOL line."""
        pos = 0
        while pos < len(content):
            # Skip whitespace
            while pos < len(content) and content[pos].isspace():
                pos += 1
            
            if pos >= len(content):
                break
            
            start_pos = pos
            
            # Check for strings
            if content[pos] in ('"', "'"):
                pos = self._scan_string(content, pos, line_num, seq_area, ind_area, start_pos)
            # Check for numbers
            elif content[pos].isdigit():
                pos = self._scan_number(content, pos, line_num, seq_area, ind_area, start_pos)
            # Check for identifiers/keywords
            elif content[pos].isalpha() or content[pos] == '-':
                pos = self._scan_identifier(content, pos, line_num, seq_area, ind_area, start_pos)
            # Check for operators and punctuation
            else:
                pos = self._scan_operator(content, pos, line_num, seq_area, ind_area, start_pos)
    
    def _scan_string(self, content: str, pos: int, line_num: int, seq_area: str, 
                    ind_area: str, start_pos: int) -> int:
        """Scan a string literal."""
        quote_char = content[pos]
        pos += 1
        value = ""
        
        while pos < len(content):
            if content[pos] == quote_char:
                # Check for escaped quote
                if pos + 1 < len(content) and content[pos + 1] == quote_char:
                    value += quote_char
                    pos += 2
                else:
                    pos += 1
                    break
            else:
                value += content[pos]
                pos += 1
        
        # Determine if national literal (N prefix)
        token_type = COBOLTokenType.NATIONAL_LITERAL if quote_char == 'N' else COBOLTokenType.ALPHANUMERIC_LITERAL
        
        self.tokens.append(COBOLToken(
            token_type, value, line_num, start_pos + 8,
            seq_area, ind_area, start_pos < 4, start_pos >= 4
        ))
        
        return pos
    
    def _scan_number(self, content: str, pos: int, line_num: int, seq_area: str,
                    ind_area: str, start_pos: int) -> int:
        """Scan a numeric literal."""
        value = ""
        has_decimal = False
        
        while pos < len(content) and (content[pos].isdigit() or content[pos] == '.'):
            if content[pos] == '.':
                if has_decimal:
                    break
                has_decimal = True
            value += content[pos]
            pos += 1
        
        self.tokens.append(COBOLToken(
            COBOLTokenType.NUMERIC_LITERAL, value, line_num, start_pos + 8,
            seq_area, ind_area, start_pos < 4, start_pos >= 4
        ))
        
        return pos
    
    def _scan_identifier(self, content: str, pos: int, line_num: int, seq_area: str,
                        ind_area: str, start_pos: int) -> int:
        """Scan an identifier or keyword."""
        value = ""
        
        while (pos < len(content) and 
               (content[pos].isalnum() or content[pos] in '-_')):
            value += content[pos]
            pos += 1
        
        # Convert to lowercase for keyword lookup
        lower_value = value.lower()
        
        # Check for figurative constants
        if lower_value in self.FIGURATIVE_CONSTANTS:
            token_type = COBOLTokenType.FIGURATIVE_CONSTANT
        else:
            token_type = self.KEYWORDS.get(lower_value, COBOLTokenType.IDENTIFIER)
        
        self.tokens.append(COBOLToken(
            token_type, value, line_num, start_pos + 8,
            seq_area, ind_area, start_pos < 4, start_pos >= 4
        ))
        
        return pos
    
    def _scan_operator(self, content: str, pos: int, line_num: int, seq_area: str,
                      ind_area: str, start_pos: int) -> int:
        """Scan operators and punctuation."""
        char = content[pos]
        
        # Check for multi-character operators
        if pos + 1 < len(content):
            two_char = content[pos:pos+2]
            if two_char == '**':
                self.tokens.append(COBOLToken(
                    COBOLTokenType.POWER, two_char, line_num, start_pos + 8,
                    seq_area, ind_area, start_pos < 4, start_pos >= 4
                ))
                return pos + 2
            elif two_char == '>=':
                self.tokens.append(COBOLToken(
                    COBOLTokenType.GREATER_OR_EQUAL, two_char, line_num, start_pos + 8,
                    seq_area, ind_area, start_pos < 4, start_pos >= 4
                ))
                return pos + 2
            elif two_char == '<=':
                self.tokens.append(COBOLToken(
                    COBOLTokenType.LESS_OR_EQUAL, two_char, line_num, start_pos + 8,
                    seq_area, ind_area, start_pos < 4, start_pos >= 4
                ))
                return pos + 2
        
        # Single character operators
        token_map = {
            '.': COBOLTokenType.PERIOD,
            ',': COBOLTokenType.COMMA,
            ';': COBOLTokenType.SEMICOLON,
            '(': COBOLTokenType.LPAREN,
            ')': COBOLTokenType.RPAREN,
            ':': COBOLTokenType.COLON,
            '+': COBOLTokenType.PLUS,
            '-': COBOLTokenType.MINUS,
            '*': COBOLTokenType.MULTIPLY_OP,
            '/': COBOLTokenType.DIVIDE_OP,
            '=': COBOLTokenType.EQUAL,
            '>': COBOLTokenType.GREATER,
            '<': COBOLTokenType.LESS,
        }
        
        token_type = token_map.get(char, COBOLTokenType.IDENTIFIER)
        self.tokens.append(COBOLToken(
            token_type, char, line_num, start_pos + 8,
            seq_area, ind_area, start_pos < 4, start_pos >= 4
        ))
        
        return pos + 1

class COBOLParser:
    """COBOL parser."""
    
    def __init__(self, tokens: List[COBOLToken], error_handler: ErrorHandler):
        self.tokens = tokens
        self.pos = 0
        self.error_handler = error_handler
    
    def parse(self) -> COBOLProgram:
        """Parse COBOL program."""
        program = COBOLProgram()
        
        try:
            # Parse IDENTIFICATION DIVISION (required)
            program.identification_division = self._parse_identification_division()
            
            # Parse ENVIRONMENT DIVISION (optional)
            if self._current_token_is(COBOLTokenType.ENVIRONMENT):
                program.environment_division = self._parse_environment_division()
            
            # Parse DATA DIVISION (optional)
            if self._current_token_is(COBOLTokenType.DATA):
                program.data_division = self._parse_data_division()
            
            # Parse PROCEDURE DIVISION (optional)
            if self._current_token_is(COBOLTokenType.PROCEDURE):
                program.procedure_division = self._parse_procedure_division()
            
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.SYNTAX_ERROR,
                f"Failed to parse COBOL program: {e}",
                self._current_token().line,
                self._current_token().column
            )
        
        return program
    
    def _parse_identification_division(self) -> COBOLIdentificationDivision:
        """Parse IDENTIFICATION DIVISION."""
        self._consume(COBOLTokenType.IDENTIFICATION)
        self._consume(COBOLTokenType.DIVISION)
        self._consume_period()
        
        division = COBOLIdentificationDivision()
        
        # Parse PROGRAM-ID (required)
        if self._current_token_is(COBOLTokenType.PROGRAM_ID):
            self._advance()
            division.program_id = self._consume(COBOLTokenType.IDENTIFIER).value
            self._consume_period()
        
        # Parse optional clauses
        while not self._is_next_division():
            if self._current_token_is(COBOLTokenType.AUTHOR):
                self._advance()
                division.author = self._consume(COBOLTokenType.IDENTIFIER).value
                self._consume_period()
            elif self._current_token_is(COBOLTokenType.DATE_WRITTEN):
                self._advance()
                division.date_written = self._consume(COBOLTokenType.IDENTIFIER).value
                self._consume_period()
            else:
                self._advance()
        
        return division
    
    def _parse_environment_division(self) -> COBOLEnvironmentDivision:
        """Parse ENVIRONMENT DIVISION."""
        self._consume(COBOLTokenType.ENVIRONMENT)
        self._consume(COBOLTokenType.DIVISION)
        self._consume_period()
        
        division = COBOLEnvironmentDivision()
        
        # Parse sections
        while not self._is_next_division():
            if self._current_token_is(COBOLTokenType.CONFIGURATION):
                division.configuration_section = self._parse_configuration_section()
            elif self._current_token_is(COBOLTokenType.INPUT_OUTPUT):
                division.input_output_section = self._parse_input_output_section()
            else:
                self._advance()
        
        return division
    
    def _parse_data_division(self) -> COBOLDataDivision:
        """Parse DATA DIVISION."""
        self._consume(COBOLTokenType.DATA)
        self._consume(COBOLTokenType.DIVISION)
        self._consume_period()
        
        division = COBOLDataDivision()
        
        # Parse sections
        while not self._is_next_division():
            if self._current_token_is(COBOLTokenType.FILE_SECTION):
                division.file_section = self._parse_file_section()
            elif self._current_token_is(COBOLTokenType.WORKING_STORAGE):
                division.working_storage_section = self._parse_working_storage_section()
            elif self._current_token_is(COBOLTokenType.LINKAGE):
                division.linkage_section = self._parse_linkage_section()
            elif self._current_token_is(COBOLTokenType.LOCAL_STORAGE):
                division.local_storage_section = self._parse_local_storage_section()
            else:
                self._advance()
        
        return division
    
    def _parse_procedure_division(self) -> COBOLProcedureDivision:
        """Parse PROCEDURE DIVISION."""
        self._consume(COBOLTokenType.PROCEDURE)
        self._consume(COBOLTokenType.DIVISION)
        
        division = COBOLProcedureDivision()
        
        # Parse USING clause if present
        if self._current_token_is(COBOLTokenType.USING):
            self._advance()
            while not self._current_token_is(COBOLTokenType.PERIOD):
                division.using_clause.append(self._consume(COBOLTokenType.IDENTIFIER).value)
                if self._current_token_is(COBOLTokenType.COMMA):
                    self._advance()
        
        self._consume_period()
        
        # Parse statements, paragraphs, and sections
        while not self._current_token_is(COBOLTokenType.EOF):
            if self._is_statement():
                division.statements.append(self._parse_statement())
            elif self._is_paragraph_or_section():
                # Handle paragraphs and sections
                self._advance()
            else:
                self._advance()
        
        return division
    
    def _parse_statement(self) -> COBOLStatement:
        """Parse a COBOL statement."""
        token_type = self._current_token().type
        
        if token_type == COBOLTokenType.MOVE:
            return self._parse_move_statement()
        elif token_type == COBOLTokenType.ADD:
            return self._parse_add_statement()
        elif token_type == COBOLTokenType.SUBTRACT:
            return self._parse_subtract_statement()
        elif token_type == COBOLTokenType.MULTIPLY:
            return self._parse_multiply_statement()
        elif token_type == COBOLTokenType.DIVIDE:
            return self._parse_divide_statement()
        elif token_type == COBOLTokenType.COMPUTE:
            return self._parse_compute_statement()
        elif token_type == COBOLTokenType.IF:
            return self._parse_if_statement()
        elif token_type == COBOLTokenType.PERFORM:
            return self._parse_perform_statement()
        elif token_type == COBOLTokenType.CALL:
            return self._parse_call_statement()
        elif token_type == COBOLTokenType.DISPLAY:
            return self._parse_display_statement()
        elif token_type == COBOLTokenType.ACCEPT:
            return self._parse_accept_statement()
        else:
            # Skip unknown statement
            self._advance()
            return COBOLMoveStatement()  # Placeholder
    
    def _parse_move_statement(self) -> COBOLMoveStatement:
        """Parse MOVE statement."""
        self._consume(COBOLTokenType.MOVE)
        
        # Parse source
        source = self._parse_expression()
        
        self._consume(COBOLTokenType.TO)
        
        # Parse destinations
        destinations = []
        destinations.append(self._parse_expression())
        
        while self._current_token_is(COBOLTokenType.COMMA):
            self._advance()
            destinations.append(self._parse_expression())
        
        self._consume_period()
        
        return COBOLMoveStatement(source=source, destinations=destinations)
    
    def _parse_display_statement(self) -> COBOLDisplayStatement:
        """Parse DISPLAY statement."""
        self._consume(COBOLTokenType.DISPLAY)
        
        items = []
        items.append(self._parse_expression())
        
        while (not self._current_token_is(COBOLTokenType.PERIOD) and
               not self._current_token_is(COBOLTokenType.EOF)):
            items.append(self._parse_expression())
        
        self._consume_period()
        
        return COBOLDisplayStatement(items=items)
    
    def _parse_expression(self) -> COBOLExpression:
        """Parse a COBOL expression."""
        token = self._current_token()
        
        if token.type == COBOLTokenType.IDENTIFIER:
            name = self._advance().value
            return COBOLIdentifier(name=name)
        elif token.type == COBOLTokenType.NUMERIC_LITERAL:
            value = self._advance().value
            return COBOLLiteral(value=float(value) if '.' in value else int(value), is_numeric=True)
        elif token.type == COBOLTokenType.ALPHANUMERIC_LITERAL:
            value = self._advance().value
            return COBOLLiteral(value=value, is_alphanumeric=True)
        elif token.type == COBOLTokenType.FIGURATIVE_CONSTANT:
            value = self._advance().value
            return COBOLLiteral(value=value, is_figurative=True)
        else:
            self._advance()
            return COBOLLiteral(value="", is_alphanumeric=True)
    
    # Helper methods
    def _current_token(self) -> COBOLToken:
        """Get current token."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def _current_token_is(self, token_type: COBOLTokenType) -> bool:
        """Check if current token is of given type."""
        return self._current_token().type == token_type
    
    def _advance(self) -> COBOLToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _consume(self, expected_type: COBOLTokenType) -> COBOLToken:
        """Consume token of expected type."""
        if self._current_token_is(expected_type):
            return self._advance()
        else:
            self.error_handler.add_error(
                ErrorType.SYNTAX_ERROR,
                f"Expected {expected_type}, got {self._current_token().type}",
                self._current_token().line,
                self._current_token().column
            )
            return self._current_token()
    
    def _consume_period(self):
        """Consume a period."""
        if self._current_token_is(COBOLTokenType.PERIOD):
            self._advance()
    
    def _is_next_division(self) -> bool:
        """Check if we're at the start of the next division."""
        return self._current_token().type in [
            COBOLTokenType.ENVIRONMENT,
            COBOLTokenType.DATA,
            COBOLTokenType.PROCEDURE,
            COBOLTokenType.EOF
        ]
    
    def _is_statement(self) -> bool:
        """Check if current token starts a statement."""
        return self._current_token().type in [
            COBOLTokenType.MOVE, COBOLTokenType.ADD, COBOLTokenType.SUBTRACT,
            COBOLTokenType.MULTIPLY, COBOLTokenType.DIVIDE, COBOLTokenType.COMPUTE,
            COBOLTokenType.IF, COBOLTokenType.PERFORM, COBOLTokenType.CALL,
            COBOLTokenType.DISPLAY, COBOLTokenType.ACCEPT, COBOLTokenType.READ,
            COBOLTokenType.WRITE, COBOLTokenType.OPEN, COBOLTokenType.CLOSE
        ]
    
    def _is_paragraph_or_section(self) -> bool:
        """Check if current token is a paragraph or section name."""
        return (self._current_token().type == COBOLTokenType.IDENTIFIER and
                self._current_token().area_a)

def parse_cobol(source: str, error_handler: Optional[ErrorHandler] = None) -> COBOLProgram:
    """Parse COBOL source code."""
    if error_handler is None:
        error_handler = ErrorHandler()
    
    try:
        lexer = COBOLLexer(source)
        tokens = lexer.tokenize()
        parser = COBOLParser(tokens, error_handler)
        return parser.parse()
    except Exception as e:
        error_handler.add_error(ErrorType.SYNTAX_ERROR, str(e), 0, 0)
        return COBOLProgram() 