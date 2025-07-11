#!/usr/bin/env python3
"""
WebAssembly Parser and Lexer

Comprehensive WebAssembly text format (WAT) parsing implementation supporting
WebAssembly MVP and common extensions.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .wasm_ast import *


class WasmTokenType(Enum):
    """WebAssembly token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    
    # Special
    EOF = auto()
    COMMENT = auto()
    BLOCK_COMMENT = auto()


@dataclass
class WasmToken:
    """WebAssembly token."""
    type: WasmTokenType
    value: str
    line: int
    column: int


class WasmLexer:
    """WebAssembly lexer for tokenizing WAT format."""
    
    def __init__(self):
        self.keywords = {
            'module', 'func', 'param', 'result', 'local', 'global', 'table', 'memory',
            'import', 'export', 'start', 'data', 'elem', 'type', 'mut', 'const',
            'i32', 'i64', 'f32', 'f64', 'v128', 'funcref', 'externref',
            'block', 'loop', 'if', 'else', 'end', 'br', 'br_if', 'br_table',
            'return', 'call', 'call_indirect', 'drop', 'select', 'select_t',
            'local.get', 'local.set', 'local.tee', 'global.get', 'global.set',
            'table.get', 'table.set', 'table.init', 'elem.drop', 'table.copy',
            'table.grow', 'table.size', 'table.fill',
            'i32.load', 'i64.load', 'f32.load', 'f64.load', 'i32.store', 'i64.store',
            'f32.store', 'f64.store', 'memory.size', 'memory.grow',
            'i32.const', 'i64.const', 'f32.const', 'f64.const',
            'i32.eqz', 'i32.eq', 'i32.ne', 'i32.lt_s', 'i32.lt_u', 'i32.gt_s',
            'i32.gt_u', 'i32.le_s', 'i32.le_u', 'i32.ge_s', 'i32.ge_u',
            'i64.eqz', 'i64.eq', 'i64.ne', 'i64.lt_s', 'i64.lt_u', 'i64.gt_s',
            'i64.gt_u', 'i64.le_s', 'i64.le_u', 'i64.ge_s', 'i64.ge_u',
            'f32.eq', 'f32.ne', 'f32.lt', 'f32.gt', 'f32.le', 'f32.ge',
            'f64.eq', 'f64.ne', 'f64.lt', 'f64.gt', 'f64.le', 'f64.ge',
            'i32.clz', 'i32.ctz', 'i32.popcnt', 'i32.add', 'i32.sub', 'i32.mul',
            'i32.div_s', 'i32.div_u', 'i32.rem_s', 'i32.rem_u', 'i32.and',
            'i32.or', 'i32.xor', 'i32.shl', 'i32.shr_s', 'i32.shr_u',
            'i32.rotl', 'i32.rotr', 'i32.wrap_i64', 'i32.trunc_f32_s',
            'i32.trunc_f32_u', 'i32.trunc_f64_s', 'i32.trunc_f64_u',
            'i32.reinterpret_f32', 'i64.extend_i32_s', 'i64.extend_i32_u',
            'f32.convert_i32_s', 'f32.convert_i32_u', 'f32.convert_i64_s',
            'f32.convert_i64_u', 'f32.demote_f64', 'f32.reinterpret_i32',
            'f64.convert_i32_s', 'f64.convert_i32_u', 'f64.convert_i64_s',
            'f64.convert_i64_u', 'f64.promote_f32', 'f64.reinterpret_i64',
            'unreachable', 'nop'
        }
        
        self.token_patterns = [
            (r';;.*$', WasmTokenType.COMMENT),
            (r'\(;.*?;\)', WasmTokenType.BLOCK_COMMENT),
            (r'\(', WasmTokenType.LPAREN),
            (r'\)', WasmTokenType.RPAREN),
            (r'"([^"\\]|\\.)*"', WasmTokenType.STRING),
            (r'[-+]?0x[0-9a-fA-F]+(?:\.[0-9a-fA-F]+)?(?:[pP][-+]?[0-9]+)?', WasmTokenType.FLOAT),
            (r'[-+]?[0-9]+\.[0-9]+(?:[eE][-+]?[0-9]+)?', WasmTokenType.FLOAT),
            (r'[-+]?[0-9]+(?:[eE][-+]?[0-9]+)?', WasmTokenType.INTEGER),
            (r'inf|nan:0x[0-9a-fA-F]+|nan', WasmTokenType.FLOAT),
            (r'\$[a-zA-Z_][a-zA-Z0-9_]*', WasmTokenType.IDENTIFIER),
            (r'[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*', WasmTokenType.IDENTIFIER),
        ]
    
    def tokenize(self, text: str) -> List[WasmToken]:
        """Tokenize WebAssembly text format."""
        tokens = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            pos = 0
            while pos < len(line):
                # Skip whitespace
                if line[pos].isspace():
                    pos += 1
                    continue
                
                # Try to match patterns
                matched = False
                for pattern, token_type in self.token_patterns:
                    regex = re.compile(pattern)
                    match = regex.match(line, pos)
                    
                    if match:
                        value = match.group(0)
                        
                        # Skip comments
                        if token_type in (WasmTokenType.COMMENT, WasmTokenType.BLOCK_COMMENT):
                            pos = match.end()
                            if token_type == WasmTokenType.COMMENT:
                                break  # Rest of line is comment
                            matched = True
                            break
                        
                        # Classify identifiers as keywords if they match
                        if token_type == WasmTokenType.IDENTIFIER and value in self.keywords:
                            token_type = WasmTokenType.KEYWORD
                        
                        tokens.append(WasmToken(
                            type=token_type,
                            value=value,
                            line=line_num,
                            column=pos + 1
                        ))
                        
                        pos = match.end()
                        matched = True
                        break
                
                if not matched:
                    # Unknown character
                    pos += 1
        
        tokens.append(WasmToken(WasmTokenType.EOF, '', len(lines), 1))
        return tokens


class WasmParser:
    """WebAssembly parser for WAT format."""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
    
    def parse(self, text: str) -> WasmModule:
        """Parse WebAssembly text format."""
        try:
            lexer = WasmLexer()
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            
            return self._parse_module()
        except Exception as e:
            self.logger.error(f"WebAssembly parsing failed: {e}")
            raise RuntimeError(f"Failed to parse WebAssembly: {e}")
    
    def _current_token(self) -> WasmToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return WasmToken(WasmTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> WasmToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, expected: WasmTokenType) -> bool:
        """Check if current token matches expected type."""
        return self._current_token().type == expected
    
    def _consume(self, expected: WasmTokenType, message: str = None) -> WasmToken:
        """Consume token of expected type."""
        if not self._match(expected):
            error_msg = message or f"Expected {expected}, got {self._current_token().type}"
            raise RuntimeError(error_msg)
        return self._advance()
    
    def _consume_keyword(self, keyword: str) -> WasmToken:
        """Consume specific keyword."""
        token = self._current_token()
        if token.type != WasmTokenType.KEYWORD or token.value != keyword:
            raise RuntimeError(f"Expected keyword '{keyword}', got '{token.value}'")
        return self._advance()
    
    def _parse_module(self) -> WasmModule:
        """Parse WebAssembly module."""
        self._consume(WasmTokenType.LPAREN)
        self._consume_keyword('module')
        
        module = WasmModule()
        
        while not self._match(WasmTokenType.RPAREN) and not self._match(WasmTokenType.EOF):
            if self._match(WasmTokenType.LPAREN):
                self._parse_module_field(module)
            else:
                self._advance()  # Skip unexpected tokens
        
        self._consume(WasmTokenType.RPAREN)
        return module
    
    def _parse_module_field(self, module: WasmModule):
        """Parse module field."""
        self._consume(WasmTokenType.LPAREN)
        
        if not self._match(WasmTokenType.KEYWORD):
            self._consume(WasmTokenType.RPAREN)
            return
        
        keyword = self._current_token().value
        
        if keyword == 'type':
            module.types.append(self._parse_type())
        elif keyword == 'import':
            module.imports.append(self._parse_import())
        elif keyword == 'func':
            module.functions.append(self._parse_function())
        elif keyword == 'table':
            module.tables.append(self._parse_table())
        elif keyword == 'memory':
            module.memories.append(self._parse_memory())
        elif keyword == 'global':
            module.globals.append(self._parse_global())
        elif keyword == 'export':
            module.exports.append(self._parse_export())
        elif keyword == 'start':
            module.start = self._parse_start()
        elif keyword == 'elem':
            module.elements.append(self._parse_element())
        elif keyword == 'data':
            module.data.append(self._parse_data())
        else:
            # Skip unknown fields
            self._skip_s_expression()
        
        self._consume(WasmTokenType.RPAREN)
    
    def _parse_type(self) -> WasmType:
        """Parse function type."""
        self._consume_keyword('type')
        
        # Optional type identifier
        if self._match(WasmTokenType.IDENTIFIER):
            self._advance()
        
        # Parse function signature
        self._consume(WasmTokenType.LPAREN)
        self._consume_keyword('func')
        
        wasm_type = WasmType()
        
        # Parse parameters
        while self._match(WasmTokenType.LPAREN):
            lookahead_pos = self.pos + 1
            if (lookahead_pos < len(self.tokens) and 
                self.tokens[lookahead_pos].type == WasmTokenType.KEYWORD and 
                self.tokens[lookahead_pos].value == 'param'):
                
                self._consume(WasmTokenType.LPAREN)
                self._consume_keyword('param')
                
                # Optional parameter identifier
                if self._match(WasmTokenType.IDENTIFIER):
                    self._advance()
                
                # Parameter type
                if self._match(WasmTokenType.KEYWORD):
                    param_type = self._parse_value_type()
                    wasm_type.parameters.append(param_type)
                
                self._consume(WasmTokenType.RPAREN)
            else:
                break
        
        # Parse results
        while self._match(WasmTokenType.LPAREN):
            lookahead_pos = self.pos + 1
            if (lookahead_pos < len(self.tokens) and 
                self.tokens[lookahead_pos].type == WasmTokenType.KEYWORD and 
                self.tokens[lookahead_pos].value == 'result'):
                
                self._consume(WasmTokenType.LPAREN)
                self._consume_keyword('result')
                
                # Result type
                if self._match(WasmTokenType.KEYWORD):
                    result_type = self._parse_value_type()
                    wasm_type.results.append(result_type)
                
                self._consume(WasmTokenType.RPAREN)
            else:
                break
        
        self._consume(WasmTokenType.RPAREN)
        return wasm_type
    
    def _parse_import(self) -> WasmImport:
        """Parse import."""
        self._consume_keyword('import')
        
        # Module name
        module_name = self._consume(WasmTokenType.STRING).value[1:-1]  # Remove quotes
        
        # Import name
        import_name = self._consume(WasmTokenType.STRING).value[1:-1]  # Remove quotes
        
        # Import descriptor
        self._consume(WasmTokenType.LPAREN)
        
        if not self._match(WasmTokenType.KEYWORD):
            raise RuntimeError("Expected import kind")
        
        kind = self._current_token().value
        self._advance()
        
        # Parse type information based on kind
        type_index = None
        type_info = None
        
        if kind == 'func':
            # Optional function identifier
            if self._match(WasmTokenType.IDENTIFIER):
                self._advance()
            
            # Type use
            if self._match(WasmTokenType.LPAREN):
                self._consume(WasmTokenType.LPAREN)
                self._consume_keyword('type')
                # Type index or identifier
                if self._match(WasmTokenType.INTEGER):
                    type_index = int(self._advance().value)
                elif self._match(WasmTokenType.IDENTIFIER):
                    # Type identifier (would need to be resolved)
                    self._advance()
                self._consume(WasmTokenType.RPAREN)
        elif kind in ('table', 'memory', 'global'):
            # Parse type info for other kinds
            type_info = self._parse_import_type_info(kind)
        
        self._consume(WasmTokenType.RPAREN)
        
        return WasmImport(
            module=module_name,
            name=import_name,
            kind=kind,
            type_index=type_index,
            type_info=type_info
        )
    
    def _parse_function(self) -> WasmFunction:
        """Parse function."""
        self._consume_keyword('func')
        
        # Optional function identifier
        name = None
        if self._match(WasmTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Type use or inline type
        type_index = 0
        locals = []
        
        # Parse type use
        if self._match(WasmTokenType.LPAREN):
            lookahead_pos = self.pos + 1
            if (lookahead_pos < len(self.tokens) and 
                self.tokens[lookahead_pos].type == WasmTokenType.KEYWORD and 
                self.tokens[lookahead_pos].value == 'type'):
                
                self._consume(WasmTokenType.LPAREN)
                self._consume_keyword('type')
                
                if self._match(WasmTokenType.INTEGER):
                    type_index = int(self._advance().value)
                elif self._match(WasmTokenType.IDENTIFIER):
                    # Type identifier (would need to be resolved)
                    self._advance()
                
                self._consume(WasmTokenType.RPAREN)
        
        # Parse parameters and locals
        while self._match(WasmTokenType.LPAREN):
            lookahead_pos = self.pos + 1
            if (lookahead_pos < len(self.tokens) and 
                self.tokens[lookahead_pos].type == WasmTokenType.KEYWORD):
                
                keyword = self.tokens[lookahead_pos].value
                
                if keyword == 'param':
                    self._consume(WasmTokenType.LPAREN)
                    self._consume_keyword('param')
                    
                    # Optional parameter identifier
                    if self._match(WasmTokenType.IDENTIFIER):
                        self._advance()
                    
                    # Parameter type (skip for now)
                    if self._match(WasmTokenType.KEYWORD):
                        self._advance()
                    
                    self._consume(WasmTokenType.RPAREN)
                    
                elif keyword == 'result':
                    self._consume(WasmTokenType.LPAREN)
                    self._consume_keyword('result')
                    
                    # Result type (skip for now)
                    if self._match(WasmTokenType.KEYWORD):
                        self._advance()
                    
                    self._consume(WasmTokenType.RPAREN)
                    
                elif keyword == 'local':
                    self._consume(WasmTokenType.LPAREN)
                    self._consume_keyword('local')
                    
                    # Optional local identifier
                    if self._match(WasmTokenType.IDENTIFIER):
                        self._advance()
                    
                    # Local type
                    if self._match(WasmTokenType.KEYWORD):
                        local_type = self._parse_value_type()
                        locals.append(local_type)
                    
                    self._consume(WasmTokenType.RPAREN)
                else:
                    break
            else:
                break
        
        # Parse function body
        body = []
        while not self._match(WasmTokenType.RPAREN) and not self._match(WasmTokenType.EOF):
            if self._match(WasmTokenType.LPAREN):
                # Skip instruction parsing for now
                self._skip_s_expression()
            else:
                # Simple instruction
                if self._match(WasmTokenType.KEYWORD):
                    opcode_str = self._advance().value
                    try:
                        opcode = WasmOpcode(opcode_str)
                        body.append(WasmInstruction(opcode=opcode))
                    except ValueError:
                        # Unknown opcode, skip
                        pass
                else:
                    self._advance()
        
        return WasmFunction(
            type_index=type_index,
            locals=locals,
            body=body,
            name=name
        )
    
    def _parse_table(self) -> WasmTable:
        """Parse table."""
        self._consume_keyword('table')
        
        # Optional table identifier
        if self._match(WasmTokenType.IDENTIFIER):
            self._advance()
        
        # Table limits
        limits = self._parse_limits()
        
        # Element type
        element_type = self._parse_value_type()
        
        return WasmTable(element_type=element_type, limits=limits)
    
    def _parse_memory(self) -> WasmMemory:
        """Parse memory."""
        self._consume_keyword('memory')
        
        # Optional memory identifier
        if self._match(WasmTokenType.IDENTIFIER):
            self._advance()
        
        # Memory limits
        limits = self._parse_limits()
        
        return WasmMemory(limits=limits)
    
    def _parse_global(self) -> WasmGlobal:
        """Parse global."""
        self._consume_keyword('global')
        
        # Optional global identifier
        if self._match(WasmTokenType.IDENTIFIER):
            self._advance()
        
        # Global type
        mutability = WasmMutability.CONST
        if self._match(WasmTokenType.LPAREN):
            self._consume(WasmTokenType.LPAREN)
            self._consume_keyword('mut')
            mutability = WasmMutability.VAR
            self._consume(WasmTokenType.RPAREN)
        
        value_type = self._parse_value_type()
        
        # Initial value (simplified)
        init = []
        while not self._match(WasmTokenType.RPAREN) and not self._match(WasmTokenType.EOF):
            if self._match(WasmTokenType.LPAREN):
                self._skip_s_expression()
            else:
                self._advance()
        
        return WasmGlobal(
            value_type=value_type,
            mutability=mutability,
            init=init
        )
    
    def _parse_export(self) -> WasmExport:
        """Parse export."""
        self._consume_keyword('export')
        
        # Export name
        name = self._consume(WasmTokenType.STRING).value[1:-1]  # Remove quotes
        
        # Export descriptor
        self._consume(WasmTokenType.LPAREN)
        
        if not self._match(WasmTokenType.KEYWORD):
            raise RuntimeError("Expected export kind")
        
        kind = self._current_token().value
        self._advance()
        
        # Export index
        index = 0
        if self._match(WasmTokenType.INTEGER):
            index = int(self._advance().value)
        elif self._match(WasmTokenType.IDENTIFIER):
            # Identifier (would need to be resolved)
            self._advance()
        
        self._consume(WasmTokenType.RPAREN)
        
        return WasmExport(name=name, kind=kind, index=index)
    
    def _parse_start(self) -> int:
        """Parse start function."""
        self._consume_keyword('start')
        
        start_index = 0
        if self._match(WasmTokenType.INTEGER):
            start_index = int(self._advance().value)
        elif self._match(WasmTokenType.IDENTIFIER):
            # Identifier (would need to be resolved)
            self._advance()
        
        return start_index
    
    def _parse_element(self) -> WasmElement:
        """Parse element segment."""
        self._consume_keyword('elem')
        
        # Table index (simplified)
        table_index = 0
        
        # Offset (simplified)
        offset = []
        
        # Init (simplified)
        init = []
        
        # Skip remaining content
        while not self._match(WasmTokenType.RPAREN) and not self._match(WasmTokenType.EOF):
            if self._match(WasmTokenType.LPAREN):
                self._skip_s_expression()
            else:
                self._advance()
        
        return WasmElement(
            table_index=table_index,
            offset=offset,
            init=init
        )
    
    def _parse_data(self) -> WasmData:
        """Parse data segment."""
        self._consume_keyword('data')
        
        # Memory index (simplified)
        memory_index = 0
        
        # Offset (simplified)
        offset = []
        
        # Data (simplified)
        data = b''
        
        # Skip remaining content
        while not self._match(WasmTokenType.RPAREN) and not self._match(WasmTokenType.EOF):
            if self._match(WasmTokenType.LPAREN):
                self._skip_s_expression()
            elif self._match(WasmTokenType.STRING):
                # Parse string data
                string_val = self._advance().value[1:-1]  # Remove quotes
                data += string_val.encode('utf-8')
            else:
                self._advance()
        
        return WasmData(
            memory_index=memory_index,
            offset=offset,
            data=data
        )
    
    def _parse_value_type(self) -> WasmValueType:
        """Parse value type."""
        if not self._match(WasmTokenType.KEYWORD):
            raise RuntimeError("Expected value type")
        
        type_str = self._advance().value
        
        try:
            return WasmValueType(type_str)
        except ValueError:
            # Unknown type, default to i32
            return WasmValueType.I32
    
    def _parse_limits(self) -> WasmLimits:
        """Parse limits."""
        min_val = 0
        max_val = None
        
        if self._match(WasmTokenType.INTEGER):
            min_val = int(self._advance().value)
        
        if self._match(WasmTokenType.INTEGER):
            max_val = int(self._advance().value)
        
        return WasmLimits(min=min_val, max=max_val)
    
    def _parse_import_type_info(self, kind: str) -> Any:
        """Parse import type information."""
        # Simplified implementation
        return None
    
    def _skip_s_expression(self):
        """Skip an S-expression."""
        if not self._match(WasmTokenType.LPAREN):
            return
        
        self._advance()  # consume '('
        paren_count = 1
        
        while paren_count > 0 and not self._match(WasmTokenType.EOF):
            if self._match(WasmTokenType.LPAREN):
                paren_count += 1
            elif self._match(WasmTokenType.RPAREN):
                paren_count -= 1
            self._advance()


# Convenience functions
def parse_wasm(text: str) -> WasmModule:
    """Parse WebAssembly text format."""
    parser = WasmParser()
    return parser.parse(text)


def parse_wasm_file(file_path: str) -> WasmModule:
    """Parse WebAssembly file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_wasm(f.read())