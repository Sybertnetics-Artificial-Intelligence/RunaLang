"""
Runa Language Server Protocol (LSP) Implementation

Provides language server capabilities for Runa IDE integration.
"""

import asyncio
import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlparse, unquote

from .compiler.lexer import RunaLexer
from .compiler.parser import RunaParser
from .compiler.semantic import SemanticAnalyzer
from .compiler.ast_nodes import *


class Position:
    """LSP Position representation."""
    def __init__(self, line: int, character: int):
        self.line = line
        self.character = character
    
    def to_dict(self):
        return {"line": self.line, "character": self.character}


class Range:
    """LSP Range representation."""
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end
    
    def to_dict(self):
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}


class Location:
    """LSP Location representation."""
    def __init__(self, uri: str, range: Range):
        self.uri = uri
        self.range = range
    
    def to_dict(self):
        return {"uri": self.uri, "range": self.range.to_dict()}


class Diagnostic:
    """LSP Diagnostic representation."""
    def __init__(self, range: Range, message: str, severity: int = 1, source: str = "runa"):
        self.range = range
        self.message = message
        self.severity = severity  # 1=Error, 2=Warning, 3=Information, 4=Hint
        self.source = source
    
    def to_dict(self):
        return {
            "range": self.range.to_dict(),
            "message": self.message,
            "severity": self.severity,
            "source": self.source
        }


class CompletionItem:
    """LSP CompletionItem representation."""
    def __init__(self, label: str, kind: int, detail: str = None, documentation: str = None):
        self.label = label
        self.kind = kind  # 1=Text, 3=Function, 6=Variable, 7=Class, etc.
        self.detail = detail
        self.documentation = documentation
    
    def to_dict(self):
        item = {"label": self.label, "kind": self.kind}
        if self.detail:
            item["detail"] = self.detail
        if self.documentation:
            item["documentation"] = self.documentation
        return item


class RunaLanguageServer:
    """Main Language Server for Runa."""
    
    def __init__(self):
        self.documents: Dict[str, str] = {}
        self.diagnostics: Dict[str, List[Diagnostic]] = {}
        self.lexer = RunaLexer()
        self.parser = RunaParser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.logger = logging.getLogger(__name__)
        
        # Built-in keywords and functions for completion
        self.keywords = [
            "let", "define", "function", "if", "else", "while", "for", "in", "return",
            "true", "false", "null", "and", "or", "not", "try", "catch", "finally",
            "throw", "async", "await", "import", "export", "from", "as", "match",
            "case", "when", "delete", "own", "shared", "borrowed", "send", "receive",
            "atomic", "lock", "unlock", "process", "module"
        ]
        
        self.builtin_functions = [
            "print", "input", "length", "type", "convert", "parse", "format",
            "range", "enumerate", "zip", "map", "filter", "reduce", "sort",
            "reverse", "split", "join", "replace", "contains", "starts_with",
            "ends_with", "uppercase", "lowercase", "trim"
        ]
        
        self.builtin_types = [
            "number", "string", "boolean", "list", "dictionary", "function",
            "optional", "union", "intersection", "any", "void"
        ]
    
    def uri_to_path(self, uri: str) -> str:
        """Convert URI to file path."""
        parsed = urlparse(uri)
        return unquote(parsed.path)
    
    def path_to_uri(self, path: str) -> str:
        """Convert file path to URI."""
        return f"file://{path}"
    
    def get_line_character_from_offset(self, text: str, offset: int) -> Tuple[int, int]:
        """Convert text offset to line/character position."""
        lines = text[:offset].split('\n')
        line = len(lines) - 1
        character = len(lines[-1]) if lines else 0
        return line, character
    
    def get_offset_from_line_character(self, text: str, line: int, character: int) -> int:
        """Convert line/character position to text offset."""
        lines = text.split('\n')
        offset = sum(len(lines[i]) + 1 for i in range(line))
        return offset + character
    
    def analyze_document(self, uri: str, text: str) -> List[Diagnostic]:
        """Analyze document and return diagnostics."""
        diagnostics = []
        
        if not text.strip():
            return diagnostics
        
        try:
            # Initialize lexer with text
            self.lexer.reset_state()
            tokens = self.lexer.tokenize(text)
            
            # Parse with proper error handling
            try:
                ast = self.parser.parse(tokens)
                
                # Semantic analysis with context
                try:
                    self.semantic_analyzer.reset()
                    self.semantic_analyzer.analyze(ast)
                    
                    # Check for semantic warnings
                    warnings = self.semantic_analyzer.get_warnings()
                    for warning in warnings:
                        diagnostic = self._create_diagnostic_from_warning(warning)
                        diagnostics.append(diagnostic)
                        
                except Exception as semantic_error:
                    diagnostic = self._create_diagnostic_from_error(
                        semantic_error, "semantic", text
                    )
                    diagnostics.append(diagnostic)
                    
            except Exception as parse_error:
                diagnostic = self._create_diagnostic_from_error(
                    parse_error, "syntax", text
                )
                diagnostics.append(diagnostic)
                
        except Exception as lex_error:
            diagnostic = self._create_diagnostic_from_error(
                lex_error, "lexical", text
            )
            diagnostics.append(diagnostic)
        
        return diagnostics
    
    def _create_diagnostic_from_error(self, error: Exception, error_type: str, text: str) -> Diagnostic:
        """Create diagnostic from error with proper positioning."""
        error_msg = str(error)
        
        # Extract line/column from error if available
        line, character = 0, 0
        
        # Try different ways to extract position
        if hasattr(error, 'line') and hasattr(error, 'column'):
            line = max(0, error.line - 1)  # LSP uses 0-based lines
            character = max(0, error.column - 1)
        elif hasattr(error, 'lineno'):
            line = max(0, error.lineno - 1)
            character = getattr(error, 'offset', 0) or 0
        else:
            # Try to parse from error message
            line_match = re.search(r'line (\d+)', error_msg, re.IGNORECASE)
            if line_match:
                line = max(0, int(line_match.group(1)) - 1)
            
            col_match = re.search(r'column (\d+)', error_msg, re.IGNORECASE)
            if col_match:
                character = max(0, int(col_match.group(1)) - 1)
        
        # Validate position against text
        lines = text.split('\n')
        if line >= len(lines):
            line = len(lines) - 1
        
        if line >= 0 and character >= len(lines[line]):
            character = len(lines[line])
        
        # Create range
        start_pos = Position(line, character)
        end_pos = Position(line, min(character + 20, len(lines[line]) if line < len(lines) else 0))
        diagnostic_range = Range(start_pos, end_pos)
        
        # Determine severity based on error type
        severity = 1  # Error
        if error_type == "semantic" and "warning" in error_msg.lower():
            severity = 2  # Warning
        
        return Diagnostic(
            range=diagnostic_range,
            message=f"{error_type.capitalize()} error: {error_msg}",
            severity=severity,
            source="runa"
        )
    
    def _create_diagnostic_from_warning(self, warning: Dict) -> Diagnostic:
        """Create diagnostic from semantic warning."""
        line = warning.get('line', 0)
        character = warning.get('column', 0)
        message = warning.get('message', 'Unknown warning')
        
        start_pos = Position(line, character)
        end_pos = Position(line, character + warning.get('length', 10))
        diagnostic_range = Range(start_pos, end_pos)
        
        return Diagnostic(
            range=diagnostic_range,
            message=message,
            severity=2,  # Warning
            source="runa"
        )
    
    def get_completions(self, uri: str, line: int, character: int) -> List[CompletionItem]:
        """Get completion suggestions for position."""
        completions = []
        
        # Add keywords
        for keyword in self.keywords:
            completions.append(CompletionItem(
                label=keyword,
                kind=14,  # Keyword
                detail=f"Runa keyword: {keyword}",
                documentation=f"The '{keyword}' keyword"
            ))
        
        # Add built-in functions
        for func in self.builtin_functions:
            completions.append(CompletionItem(
                label=func,
                kind=3,  # Function
                detail=f"Built-in function: {func}",
                documentation=f"Built-in Runa function: {func}"
            ))
        
        # Add built-in types
        for type_name in self.builtin_types:
            completions.append(CompletionItem(
                label=type_name,
                kind=7,  # Class (type)
                detail=f"Built-in type: {type_name}",
                documentation=f"Built-in Runa type: {type_name}"
            ))
        
        # TODO: Add context-aware completions based on current scope
        # This would require parsing the document and analyzing the AST
        
        return completions
    
    def get_hover_info(self, uri: str, line: int, character: int) -> Optional[str]:
        """Get hover information for position."""
        text = self.documents.get(uri, "")
        lines = text.split('\n')
        
        if line >= len(lines):
            return None
        
        current_line = lines[line]
        if character >= len(current_line):
            return None
        
        # Simple word extraction for hover
        word_start = character
        word_end = character
        
        # Find word boundaries
        while word_start > 0 and current_line[word_start - 1].isalnum():
            word_start -= 1
        
        while word_end < len(current_line) and current_line[word_end].isalnum():
            word_end += 1
        
        word = current_line[word_start:word_end]
        
        if word in self.keywords:
            return f"**{word}** - Runa keyword"
        elif word in self.builtin_functions:
            return f"**{word}** - Built-in function"
        elif word in self.builtin_types:
            return f"**{word}** - Built-in type"
        
        return None
    
    def format_document(self, uri: str) -> List[Dict]:
        """Format document and return text edits."""
        text = self.documents.get(uri, "")
        
        # Simple formatting rules
        lines = text.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Handle indentation
            if stripped.endswith(':'):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped in ['end', 'finally', 'else', 'case']:
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('    ' * indent_level + stripped)
            else:
                formatted_lines.append('    ' * indent_level + stripped)
        
        formatted_text = '\n'.join(formatted_lines)
        
        # Return full document replacement
        return [{
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": len(lines), "character": 0}
            },
            "newText": formatted_text
        }]
    
    async def handle_request(self, request: Dict) -> Optional[Dict]:
        """Handle LSP request."""
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return {
                    "id": request_id,
                    "result": {
                        "capabilities": {
                            "textDocumentSync": 1,  # Full sync
                            "hoverProvider": True,
                            "completionProvider": {
                                "resolveProvider": False,
                                "triggerCharacters": [".", " "]
                            },
                            "documentFormattingProvider": True,
                            "documentRangeFormattingProvider": True,
                            "diagnosticProvider": True
                        }
                    }
                }
            
            elif method == "textDocument/didOpen":
                uri = params["textDocument"]["uri"]
                text = params["textDocument"]["text"]
                self.documents[uri] = text
                
                # Analyze and send diagnostics
                diagnostics = self.analyze_document(uri, text)
                self.diagnostics[uri] = diagnostics
                
                # Send diagnostics notification
                return {
                    "method": "textDocument/publishDiagnostics",
                    "params": {
                        "uri": uri,
                        "diagnostics": [d.to_dict() for d in diagnostics]
                    }
                }
            
            elif method == "textDocument/didChange":
                uri = params["textDocument"]["uri"]
                changes = params["contentChanges"]
                
                # Apply changes (assuming full document sync)
                if changes:
                    self.documents[uri] = changes[0]["text"]
                    
                    # Re-analyze and send diagnostics
                    diagnostics = self.analyze_document(uri, self.documents[uri])
                    self.diagnostics[uri] = diagnostics
                    
                    return {
                        "method": "textDocument/publishDiagnostics",
                        "params": {
                            "uri": uri,
                            "diagnostics": [d.to_dict() for d in diagnostics]
                        }
                    }
            
            elif method == "textDocument/completion":
                uri = params["textDocument"]["uri"]
                position = params["position"]
                
                completions = self.get_completions(
                    uri, position["line"], position["character"]
                )
                
                return {
                    "id": request_id,
                    "result": {
                        "isIncomplete": False,
                        "items": [c.to_dict() for c in completions]
                    }
                }
            
            elif method == "textDocument/hover":
                uri = params["textDocument"]["uri"]
                position = params["position"]
                
                hover_info = self.get_hover_info(
                    uri, position["line"], position["character"]
                )
                
                if hover_info:
                    return {
                        "id": request_id,
                        "result": {
                            "contents": {
                                "kind": "markdown",
                                "value": hover_info
                            }
                        }
                    }
                else:
                    return {"id": request_id, "result": None}
            
            elif method == "textDocument/formatting":
                uri = params["textDocument"]["uri"]
                text_edits = self.format_document(uri)
                
                return {
                    "id": request_id,
                    "result": text_edits
                }
            
            elif method == "shutdown":
                return {"id": request_id, "result": None}
            
            elif method == "exit":
                return None
            
            else:
                # Method not found
                return {
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    }
                }
        
        except Exception as e:
            self.logger.error(f"Error handling request: {e}")
            return {
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def start_server(self, reader, writer):
        """Start the LSP server."""
        while True:
            try:
                # Read Content-Length header
                content_length = None
                while True:
                    line = await reader.readline()
                    if not line:
                        return
                    
                    line = line.decode('utf-8').strip()
                    if line.startswith('Content-Length:'):
                        content_length = int(line.split(':')[1].strip())
                    elif line == '':
                        break
                
                if content_length is None:
                    continue
                
                # Read content
                content = await reader.read(content_length)
                request = json.loads(content.decode('utf-8'))
                
                # Handle request
                response = await self.handle_request(request)
                
                if response:
                    # Send response
                    response_json = json.dumps(response)
                    response_bytes = response_json.encode('utf-8')
                    
                    header = f"Content-Length: {len(response_bytes)}\r\n\r\n"
                    writer.write(header.encode('utf-8'))
                    writer.write(response_bytes)
                    await writer.drain()
            
            except Exception as e:
                self.logger.error(f"Server error: {e}")
                break


def main():
    """Main entry point for the LSP server."""
    logging.basicConfig(level=logging.INFO)
    
    async def handle_client(reader, writer):
        server = RunaLanguageServer()
        await server.start_server(reader, writer)
    
    server = asyncio.start_server(handle_client, 'localhost', 8080)
    
    print("Runa Language Server started on localhost:8080")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    loop.run_forever()


if __name__ == "__main__":
    main()