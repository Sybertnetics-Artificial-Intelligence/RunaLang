#!/usr/bin/env python3
"""
Assembly Parser Module

This module provides comprehensive parsing capabilities for Assembly language,
supporting multiple architectures and all major syntax constructs including:
- Multiple instruction sets (x86, x64, ARM, RISC-V)
- Registers and memory addressing modes
- Labels, symbols, and directives
- Immediate values and expressions
- Sections and program structure
- Comments and preprocessor directives
"""

import re
from enum import Enum
from typing import List, Optional, Union, Dict, Any, Tuple
from .assembly_ast import *

class AssemblyTokenType(Enum):
    # Instructions
    INSTRUCTION = "INSTRUCTION"
    
    # Operands
    REGISTER = "REGISTER"
    IMMEDIATE = "IMMEDIATE"
    MEMORY_OPEN = "MEMORY_OPEN"      # [
    MEMORY_CLOSE = "MEMORY_CLOSE"    # ]
    
    # Identifiers and labels
    IDENTIFIER = "IDENTIFIER"
    LABEL = "LABEL"
    
    # Directives
    DIRECTIVE = "DIRECTIVE"
    
    # Operators and punctuation
    COMMA = "COMMA"                  # ,
    COLON = "COLON"                  # :
    PLUS = "PLUS"                    # +
    MINUS = "MINUS"                  # -
    MULTIPLY = "MULTIPLY"            # *
    DOLLAR = "DOLLAR"                # $ (immediate prefix)
    PERCENT = "PERCENT"              # % (register prefix)
    AT = "AT"                        # @ (symbol)
    
    # Numbers and strings
    NUMBER = "NUMBER"
    HEX_NUMBER = "HEX_NUMBER"
    BINARY_NUMBER = "BINARY_NUMBER"
    OCTAL_NUMBER = "OCTAL_NUMBER"
    STRING = "STRING"
    CHARACTER = "CHARACTER"
    
    # Comments
    COMMENT = "COMMENT"
    
    # Special tokens
    NEWLINE = "NEWLINE"
    EOF = "EOF"

class AssemblyToken:
    """Represents a token in Assembly source code."""
    
    def __init__(self, token_type: AssemblyTokenType, value: str, line: int = 0, column: int = 0):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.value}, {self.value!r}, {self.line}:{self.column})"

class AssemblyLexer:
    """Lexical analyzer for Assembly language."""
    
    def __init__(self, source: str, architecture: AssemblyArchitecture = AssemblyArchitecture.X86):
        self.source = source
        self.architecture = architecture
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Architecture-specific register sets
        self.register_patterns = self._get_register_patterns()
        self.instruction_patterns = self._get_instruction_patterns()
    
    def _get_register_patterns(self) -> Dict[str, str]:
        """Get register patterns for the current architecture."""
        patterns = {}
        
        if self.architecture in [AssemblyArchitecture.X86, AssemblyArchitecture.X64]:
            # x86/x64 registers
            patterns.update({
                # 32-bit general purpose
                r'eax|ebx|ecx|edx|esi|edi|esp|ebp': 'GENERAL_32',
                # 16-bit general purpose
                r'ax|bx|cx|dx|si|di|sp|bp': 'GENERAL_16',
                # 8-bit general purpose
                r'al|ah|bl|bh|cl|ch|dl|dh': 'GENERAL_8',
                # Segment registers
                r'cs|ds|es|fs|gs|ss': 'SEGMENT',
            })
            
            if self.architecture == AssemblyArchitecture.X64:
                # 64-bit registers
                patterns[r'rax|rbx|rcx|rdx|rsi|rdi|rsp|rbp|r8|r9|r10|r11|r12|r13|r14|r15'] = 'GENERAL_64'
        
        elif self.architecture in [AssemblyArchitecture.ARM, AssemblyArchitecture.ARM64]:
            # ARM registers
            patterns.update({
                r'r[0-9]|r1[0-5]': 'GENERAL',
                r'sp|lr|pc|cpsr': 'SPECIAL',
            })
        
        return patterns
    
    def _get_instruction_patterns(self) -> Dict[str, InstructionType]:
        """Get instruction patterns for the current architecture."""
        instructions = {}
        
        # Common instructions across architectures
        common = {
            'mov': InstructionType.MOV,
            'add': InstructionType.ADD,
            'sub': InstructionType.SUB,
            'mul': InstructionType.MUL,
            'div': InstructionType.DIV,
            'and': InstructionType.AND,
            'or': InstructionType.OR,
            'xor': InstructionType.XOR,
            'not': InstructionType.NOT,
            'cmp': InstructionType.CMP,
            'test': InstructionType.TEST,
            'jmp': InstructionType.JMP,
            'call': InstructionType.CALL,
            'ret': InstructionType.RET,
            'push': InstructionType.PUSH,
            'pop': InstructionType.POP,
            'nop': InstructionType.NOP,
        }
        
        instructions.update(common)
        
        if self.architecture in [AssemblyArchitecture.X86, AssemblyArchitecture.X64]:
            # x86-specific instructions
            x86_specific = {
                'lea': InstructionType.LEA,
                'inc': InstructionType.INC,
                'dec': InstructionType.DEC,
                'neg': InstructionType.NEG,
                'shl': InstructionType.SHL,
                'shr': InstructionType.SHR,
                'jz': InstructionType.JZ,
                'jnz': InstructionType.JNZ,
                'je': InstructionType.JE,
                'jne': InstructionType.JNE,
                'jl': InstructionType.JL,
                'jg': InstructionType.JG,
                'int': InstructionType.INT,
            }
            instructions.update(x86_specific)
        
        return instructions
    
    def current_char(self) -> Optional[str]:
        """Get the current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        """Move to the next character."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace characters except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_comment(self) -> AssemblyToken:
        """Read a comment."""
        start_column = self.column
        comment_text = ""
        
        # Skip comment indicator
        if self.current_char() == ';':
            self.advance()
        elif self.current_char() == '#':
            self.advance()
        elif self.current_char() == '/' and self.peek_char() == '/':
            self.advance()
            self.advance()
        
        # Read comment content
        while self.current_char() and self.current_char() != '\n':
            comment_text += self.current_char()
            self.advance()
        
        return AssemblyToken(AssemblyTokenType.COMMENT, comment_text.strip(), self.line, start_column)
    
    def read_string(self, quote_char: str) -> AssemblyToken:
        """Read a string literal."""
        start_column = self.column
        value = ""
        
        # Skip opening quote
        self.advance()
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
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
                        value += escape_char
                    self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        # Skip closing quote
        if self.current_char() == quote_char:
            self.advance()
        
        return AssemblyToken(AssemblyTokenType.STRING, value, self.line, start_column)
    
    def read_number(self) -> AssemblyToken:
        """Read a number (decimal, hex, binary, octal)."""
        start_column = self.column
        value = ""
        token_type = AssemblyTokenType.NUMBER
        
        # Check for hex (0x or 0X)
        if self.current_char() == '0' and self.peek_char() and self.peek_char().lower() == 'x':
            token_type = AssemblyTokenType.HEX_NUMBER
            value += self.current_char()
            self.advance()
            value += self.current_char()
            self.advance()
            
            while self.current_char() and self.current_char().lower() in '0123456789abcdef':
                value += self.current_char()
                self.advance()
        
        # Check for binary (0b or 0B)
        elif self.current_char() == '0' and self.peek_char() and self.peek_char().lower() == 'b':
            token_type = AssemblyTokenType.BINARY_NUMBER
            value += self.current_char()
            self.advance()
            value += self.current_char()
            self.advance()
            
            while self.current_char() and self.current_char() in '01':
                value += self.current_char()
                self.advance()
        
        # Check for octal (starting with 0)
        elif self.current_char() == '0' and self.peek_char() and self.peek_char().isdigit():
            token_type = AssemblyTokenType.OCTAL_NUMBER
            while self.current_char() and self.current_char() in '01234567':
                value += self.current_char()
                self.advance()
        
        # Regular decimal number
        else:
            while self.current_char() and self.current_char().isdigit():
                value += self.current_char()
                self.advance()
        
        return AssemblyToken(token_type, value, self.line, start_column)
    
    def read_identifier(self) -> AssemblyToken:
        """Read an identifier, register, or instruction."""
        start_column = self.column
        value = ""
        
        # Read identifier characters
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in '_.')):
            value += self.current_char()
            self.advance()
        
        value_lower = value.lower()
        
        # Check if it's an instruction
        if value_lower in self.instruction_patterns:
            return AssemblyToken(AssemblyTokenType.INSTRUCTION, value_lower, self.line, start_column)
        
        # Check if it's a register
        for pattern, reg_type in self.register_patterns.items():
            if re.match(f'^{pattern}$', value_lower):
                return AssemblyToken(AssemblyTokenType.REGISTER, value_lower, self.line, start_column)
        
        # Check if it's a directive (starts with .)
        if value.startswith('.'):
            return AssemblyToken(AssemblyTokenType.DIRECTIVE, value, self.line, start_column)
        
        # Default to identifier
        return AssemblyToken(AssemblyTokenType.IDENTIFIER, value, self.line, start_column)
    
    def tokenize(self) -> List[AssemblyToken]:
        """Tokenize the source code."""
        self.tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            
            # Comments
            if char == ';' or char == '#':
                self.tokens.append(self.read_comment())
            elif char == '/' and self.peek_char() == '/':
                self.tokens.append(self.read_comment())
            
            # Newlines
            elif char == '\n':
                self.tokens.append(AssemblyToken(AssemblyTokenType.NEWLINE, char, self.line, self.column))
                self.advance()
            
            # Strings
            elif char in '"\'':
                self.tokens.append(self.read_string(char))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Identifiers, instructions, registers
            elif char.isalpha() or char == '_' or char == '.':
                self.tokens.append(self.read_identifier())
            
            # Operators and punctuation
            elif char == ',':
                self.tokens.append(AssemblyToken(AssemblyTokenType.COMMA, char, self.line, self.column))
                self.advance()
            elif char == ':':
                self.tokens.append(AssemblyToken(AssemblyTokenType.COLON, char, self.line, self.column))
                self.advance()
            elif char == '[':
                self.tokens.append(AssemblyToken(AssemblyTokenType.MEMORY_OPEN, char, self.line, self.column))
                self.advance()
            elif char == ']':
                self.tokens.append(AssemblyToken(AssemblyTokenType.MEMORY_CLOSE, char, self.line, self.column))
                self.advance()
            elif char == '+':
                self.tokens.append(AssemblyToken(AssemblyTokenType.PLUS, char, self.line, self.column))
                self.advance()
            elif char == '-':
                self.tokens.append(AssemblyToken(AssemblyTokenType.MINUS, char, self.line, self.column))
                self.advance()
            elif char == '*':
                self.tokens.append(AssemblyToken(AssemblyTokenType.MULTIPLY, char, self.line, self.column))
                self.advance()
            elif char == '$':
                self.tokens.append(AssemblyToken(AssemblyTokenType.DOLLAR, char, self.line, self.column))
                self.advance()
            elif char == '%':
                self.tokens.append(AssemblyToken(AssemblyTokenType.PERCENT, char, self.line, self.column))
                self.advance()
            elif char == '@':
                self.tokens.append(AssemblyToken(AssemblyTokenType.AT, char, self.line, self.column))
                self.advance()
            else:
                # Unknown character, skip it
                self.advance()
        
        self.tokens.append(AssemblyToken(AssemblyTokenType.EOF, '', self.line, self.column))
        return self.tokens

class AssemblyParser:
    """Parser for Assembly language."""
    
    def __init__(self, tokens: List[AssemblyToken], architecture: AssemblyArchitecture = AssemblyArchitecture.X86):
        self.tokens = tokens
        self.architecture = architecture
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        """Move to the next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> Optional[AssemblyToken]:
        """Peek at a token ahead."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def expect_token(self, token_type: AssemblyTokenType) -> AssemblyToken:
        """Expect a specific token type."""
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type.value}, got {self.current_token.type.value}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.current_token and self.current_token.type == AssemblyTokenType.NEWLINE:
            self.advance()
    
    def parse_register(self) -> AssemblyRegister:
        """Parse a register operand."""
        token = self.expect_token(AssemblyTokenType.REGISTER)
        
        # Determine register size based on name
        size = self._get_register_size(token.value)
        
        return AssemblyRegister(
            name=token.value,
            size=size,
            architecture=self.architecture,
            line_number=token.line,
            column_number=token.column
        )
    
    def _get_register_size(self, register_name: str) -> DataSize:
        """Get the size of a register based on its name."""
        reg_lower = register_name.lower()
        
        if self.architecture in [AssemblyArchitecture.X86, AssemblyArchitecture.X64]:
            # x86/x64 register sizes
            if reg_lower in ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh']:
                return DataSize.BYTE
            elif reg_lower in ['ax', 'bx', 'cx', 'dx', 'si', 'di', 'sp', 'bp']:
                return DataSize.WORD
            elif reg_lower in ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp']:
                return DataSize.DWORD
            elif reg_lower in ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rsp', 'rbp'] or reg_lower.startswith('r'):
                return DataSize.QWORD
        
        elif self.architecture in [AssemblyArchitecture.ARM, AssemblyArchitecture.ARM64]:
            # ARM register sizes
            if self.architecture == AssemblyArchitecture.ARM64:
                return DataSize.QWORD
            else:
                return DataSize.DWORD
        
        return DataSize.DWORD  # Default
    
    def parse_immediate(self) -> AssemblyImmediate:
        """Parse an immediate value."""
        # Handle optional $ prefix
        if self.current_token.type == AssemblyTokenType.DOLLAR:
            self.advance()
        
        value = None
        size = None
        
        if self.current_token.type == AssemblyTokenType.NUMBER:
            value = int(self.current_token.value)
        elif self.current_token.type == AssemblyTokenType.HEX_NUMBER:
            value = int(self.current_token.value, 16)
        elif self.current_token.type == AssemblyTokenType.BINARY_NUMBER:
            value = int(self.current_token.value, 2)
        elif self.current_token.type == AssemblyTokenType.OCTAL_NUMBER:
            value = int(self.current_token.value, 8)
        elif self.current_token.type == AssemblyTokenType.IDENTIFIER:
            value = self.current_token.value  # Symbol reference
        else:
            raise SyntaxError(f"Expected immediate value, got {self.current_token.type.value}")
        
        token = self.current_token
        self.advance()
        
        return AssemblyImmediate(
            value=value,
            size=size,
            line_number=token.line,
            column_number=token.column
        )
    
    def parse_memory(self) -> AssemblyMemory:
        """Parse a memory operand [base + index*scale + displacement]."""
        self.expect_token(AssemblyTokenType.MEMORY_OPEN)
        
        base = None
        index = None
        scale = None
        displacement = None
        
        # Parse memory expression
        while self.current_token.type != AssemblyTokenType.MEMORY_CLOSE:
            if self.current_token.type == AssemblyTokenType.REGISTER:
                reg = self.parse_register()
                if base is None:
                    base = reg
                else:
                    index = reg
            
            elif self.current_token.type in [AssemblyTokenType.NUMBER, AssemblyTokenType.HEX_NUMBER]:
                # Could be scale or displacement
                num_value = int(self.current_token.value, 16 if self.current_token.type == AssemblyTokenType.HEX_NUMBER else 10)
                
                # Check if this is a scale factor (after *)
                prev_token = self.tokens[self.position - 1] if self.position > 0 else None
                if prev_token and prev_token.type == AssemblyTokenType.MULTIPLY:
                    scale = num_value
                else:
                    displacement = num_value
                
                self.advance()
            
            elif self.current_token.type == AssemblyTokenType.IDENTIFIER:
                # Symbol as displacement
                displacement = self.current_token.value
                self.advance()
            
            elif self.current_token.type in [AssemblyTokenType.PLUS, AssemblyTokenType.MINUS, AssemblyTokenType.MULTIPLY]:
                self.advance()  # Skip operator
            
            else:
                break
        
        self.expect_token(AssemblyTokenType.MEMORY_CLOSE)
        
        return AssemblyMemory(
            base=base,
            index=index,
            scale=scale,
            displacement=displacement
        )
    
    def parse_operand(self) -> AssemblyOperand:
        """Parse an operand (register, immediate, memory, or label reference)."""
        if self.current_token.type == AssemblyTokenType.REGISTER:
            return self.parse_register()
        
        elif self.current_token.type == AssemblyTokenType.MEMORY_OPEN:
            return self.parse_memory()
        
        elif self.current_token.type in [
            AssemblyTokenType.NUMBER, AssemblyTokenType.HEX_NUMBER,
            AssemblyTokenType.BINARY_NUMBER, AssemblyTokenType.OCTAL_NUMBER,
            AssemblyTokenType.DOLLAR
        ]:
            return self.parse_immediate()
        
        elif self.current_token.type == AssemblyTokenType.IDENTIFIER:
            # Label reference
            name = self.current_token.value
            self.advance()
            return AssemblyLabelRef(name=name)
        
        else:
            raise SyntaxError(f"Expected operand, got {self.current_token.type.value}")
    
    def parse_instruction(self) -> AssemblyInstruction:
        """Parse an instruction."""
        instruction_token = self.expect_token(AssemblyTokenType.INSTRUCTION)
        mnemonic = instruction_token.value
        
        # Parse operands
        operands = []
        if self.current_token.type != AssemblyTokenType.NEWLINE and self.current_token.type != AssemblyTokenType.EOF:
            operands.append(self.parse_operand())
            
            while self.current_token.type == AssemblyTokenType.COMMA:
                self.advance()  # Skip comma
                operands.append(self.parse_operand())
        
        # Create specific instruction types based on mnemonic
        if mnemonic == 'mov' and len(operands) == 2:
            return AssemblyMoveInstruction(
                destination=operands[0],
                source=operands[1],
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
        
        elif mnemonic in ['add', 'sub', 'mul', 'div', 'inc', 'dec'] and len(operands) >= 1:
            instruction_type = {
                'add': InstructionType.ADD,
                'sub': InstructionType.SUB,
                'mul': InstructionType.MUL,
                'div': InstructionType.DIV,
                'inc': InstructionType.INC,
                'dec': InstructionType.DEC,
            }[mnemonic]
            
            return AssemblyArithmeticInstruction(
                operation=instruction_type,
                destination=operands[0],
                source=operands[1] if len(operands) > 1 else None,
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
        
        elif mnemonic.startswith('j') and len(operands) == 1:
            jump_type = {
                'jmp': InstructionType.JMP,
                'jz': InstructionType.JZ,
                'jnz': InstructionType.JNZ,
                'je': InstructionType.JE,
                'jne': InstructionType.JNE,
            }.get(mnemonic, InstructionType.JMP)
            
            return AssemblyJumpInstruction(
                jump_type=jump_type,
                target=operands[0],
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
        
        elif mnemonic == 'call' and len(operands) == 1:
            return AssemblyCallInstruction(
                target=operands[0],
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
        
        elif mnemonic in ['push', 'pop'] and len(operands) == 1:
            return AssemblyStackInstruction(
                operation=InstructionType.PUSH if mnemonic == 'push' else InstructionType.POP,
                operand=operands[0],
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
        
        elif mnemonic == 'cmp' and len(operands) == 2:
            return AssemblyCompareInstruction(
                left=operands[0],
                right=operands[1],
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
        
        else:
            # Generic instruction
            return AssemblyGenericInstruction(
                mnemonic=mnemonic,
                operands=operands,
                line_number=instruction_token.line,
                column_number=instruction_token.column
            )
    
    def parse_label(self) -> AssemblyLabel:
        """Parse a label definition."""
        name_token = self.expect_token(AssemblyTokenType.IDENTIFIER)
        self.expect_token(AssemblyTokenType.COLON)
        
        return AssemblyLabel(
            name=name_token.value,
            line_number=name_token.line,
            column_number=name_token.column
        )
    
    def parse_directive(self) -> AssemblyDirective:
        """Parse an assembler directive."""
        directive_token = self.expect_token(AssemblyTokenType.DIRECTIVE)
        
        # Parse directive arguments
        arguments = []
        while (self.current_token.type not in [AssemblyTokenType.NEWLINE, AssemblyTokenType.EOF] and
               self.current_token.type != AssemblyTokenType.COMMENT):
            
            if self.current_token.type == AssemblyTokenType.STRING:
                arguments.append(self.current_token.value)
                self.advance()
            elif self.current_token.type == AssemblyTokenType.IDENTIFIER:
                arguments.append(self.current_token.value)
                self.advance()
            elif self.current_token.type in [AssemblyTokenType.NUMBER, AssemblyTokenType.HEX_NUMBER]:
                arguments.append(self.current_token.value)
                self.advance()
            elif self.current_token.type == AssemblyTokenType.COMMA:
                self.advance()  # Skip comma
            else:
                break
        
        return AssemblyDirective(
            name=directive_token.value,
            arguments=arguments,
            line_number=directive_token.line,
            column_number=directive_token.column
        )
    
    def parse_statement(self) -> Optional[AssemblyNode]:
        """Parse a statement (instruction, label, directive, or comment)."""
        self.skip_newlines()
        
        if not self.current_token or self.current_token.type == AssemblyTokenType.EOF:
            return None
        
        # Check for label
        if (self.current_token.type == AssemblyTokenType.IDENTIFIER and
            self.peek_token() and self.peek_token().type == AssemblyTokenType.COLON):
            return self.parse_label()
        
        # Check for directive
        elif self.current_token.type == AssemblyTokenType.DIRECTIVE:
            return self.parse_directive()
        
        # Check for instruction
        elif self.current_token.type == AssemblyTokenType.INSTRUCTION:
            return self.parse_instruction()
        
        # Check for comment
        elif self.current_token.type == AssemblyTokenType.COMMENT:
            comment = AssemblyComment(
                text=self.current_token.value,
                line_number=self.current_token.line,
                column_number=self.current_token.column
            )
            self.advance()
            return comment
        
        else:
            # Skip unknown tokens
            self.advance()
            return None
    
    def parse_program(self) -> AssemblyProgram:
        """Parse a complete Assembly program."""
        statements = []
        sections = []
        current_section = None
        
        while self.current_token and self.current_token.type != AssemblyTokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                # Check for section directives
                if isinstance(stmt, AssemblyDirective) and stmt.name in ['.text', '.data', '.bss']:
                    if current_section:
                        sections.append(current_section)
                    
                    current_section = AssemblySection(
                        name=stmt.name,
                        attributes=[],
                        content=[]
                    )
                elif current_section:
                    current_section.content.append(stmt)
                else:
                    statements.append(stmt)
            
            self.skip_newlines()
        
        # Add final section
        if current_section:
            sections.append(current_section)
        
        return AssemblyProgram(
            architecture=self.architecture,
            sections=sections,
            global_statements=statements
        )

def parse_assembly(source_code: str, architecture: AssemblyArchitecture = AssemblyArchitecture.X86) -> AssemblyProgram:
    """Parse Assembly source code into an AST."""
    lexer = AssemblyLexer(source_code, architecture)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing (keep them in AST)
    # tokens = [token for token in tokens if token.type != AssemblyTokenType.COMMENT]
    
    parser = AssemblyParser(tokens, architecture)
    return parser.parse_program()

def parse_assembly_instruction(source_code: str, architecture: AssemblyArchitecture = AssemblyArchitecture.X86) -> AssemblyInstruction:
    """Parse a single Assembly instruction."""
    lexer = AssemblyLexer(source_code, architecture)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing
    tokens = [token for token in tokens if token.type != AssemblyTokenType.COMMENT]
    
    parser = AssemblyParser(tokens, architecture)
    return parser.parse_instruction() 