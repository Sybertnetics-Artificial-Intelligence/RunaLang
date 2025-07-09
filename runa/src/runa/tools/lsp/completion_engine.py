"""
Runa Completion Engine

Advanced auto-completion and IntelliSense for Runa programming language.
"""

import re
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from .compiler.lexer import RunaLexer
from .compiler.parser import RunaParser
from .compiler.ast_nodes import *


class CompletionItemKind(Enum):
    TEXT = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    FIELD = 5
    VARIABLE = 6
    CLASS = 7
    INTERFACE = 8
    MODULE = 9
    PROPERTY = 10
    UNIT = 11
    VALUE = 12
    ENUM = 13
    KEYWORD = 14
    SNIPPET = 15
    COLOR = 16
    FILE = 17
    REFERENCE = 18


@dataclass
class CompletionItem:
    """Represents a completion suggestion."""
    label: str
    kind: CompletionItemKind
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None
    filter_text: Optional[str] = None
    sort_text: Optional[str] = None
    priority: int = 50  # Higher = better


@dataclass
class Symbol:
    """Represents a symbol in the code."""
    name: str
    kind: str
    type_info: Optional[str] = None
    scope: str = "local"
    line: int = 0
    column: int = 0
    documentation: Optional[str] = None


class ScopeContext:
    """Tracks scope and variable context."""
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # Stack of scopes
        self.current_function: Optional[str] = None
        self.current_class: Optional[str] = None
        self.current_module: Optional[str] = None
        
    def enter_scope(self):
        """Enter a new scope."""
        self.scopes.append({})
    
    def exit_scope(self):
        """Exit current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def add_symbol(self, symbol: Symbol):
        """Add symbol to current scope."""
        self.scopes[-1][symbol.name] = symbol
    
    def find_symbol(self, name: str) -> Optional[Symbol]:
        """Find symbol in current scope chain."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols from all scopes."""
        symbols = []
        for scope in self.scopes:
            symbols.extend(scope.values())
        return symbols


class RunaCompletionEngine:
    """Main completion engine for Runa."""
    
    def __init__(self):
        self.lexer = RunaLexer()
        self.parser = RunaParser()
        
        # Built-in completions
        self.keywords = self._get_keywords()
        self.builtin_functions = self._get_builtin_functions()
        self.builtin_types = self._get_builtin_types()
        self.stdlib_modules = self._get_stdlib_modules()
        
        # Context tracking
        self.scope_context = ScopeContext()
    
    def _get_keywords(self) -> List[CompletionItem]:
        """Get keyword completions."""
        keywords = [
            ("function", "Define a function", "function ${1:name}(${2:params}):\n    ${3:body}\nend"),
            ("let", "Declare a variable", "let ${1:name} = ${2:value}"),
            ("if", "Conditional statement", "if ${1:condition}:\n    ${2:body}\nend"),
            ("else", "Alternative condition", "else:\n    ${1:body}"),
            ("for", "For loop", "for ${1:item} in ${2:collection}:\n    ${3:body}\nend"),
            ("while", "While loop", "while ${1:condition}:\n    ${2:body}\nend"),
            ("match", "Pattern matching", "match ${1:expression}:\n    case ${2:pattern}:\n        ${3:body}\nend"),
            ("try", "Error handling", "try:\n    ${1:body}\ncatch ${2:error}:\n    ${3:handler}\nend"),
            ("async", "Async function", "async function ${1:name}(${2:params}):\n    ${3:body}\nend"),
            ("import", "Import module", "import ${1:module}"),
            ("export", "Export declaration", "export ${1:declaration}"),
            ("return", "Return value", "return ${1:value}"),
            ("break", "Break from loop", "break"),
            ("continue", "Continue loop", "continue"),
            ("true", "Boolean true", "true"),
            ("false", "Boolean false", "false"),
            ("null", "Null value", "null"),
            ("and", "Logical AND", "and"),
            ("or", "Logical OR", "or"),
            ("not", "Logical NOT", "not"),
            ("in", "Membership test", "in"),
            ("is", "Identity test", "is"),
            ("end", "End block", "end")
        ]
        
        return [
            CompletionItem(
                label=keyword,
                kind=CompletionItemKind.KEYWORD,
                detail=f"Runa keyword: {keyword}",
                documentation=description,
                insert_text=snippet,
                priority=80
            )
            for keyword, description, snippet in keywords
        ]
    
    def _get_builtin_functions(self) -> List[CompletionItem]:
        """Get built-in function completions."""
        functions = [
            ("print", "Print to console", "print(${1:message})", "Print a message to the console"),
            ("input", "Get user input", "input(${1:prompt})", "Get input from the user"),
            ("length", "Get length", "length(${1:collection})", "Get the length of a collection or string"),
            ("type", "Get type", "type(${1:value})", "Get the type of a value"),
            ("convert", "Convert type", "convert(${1:value}, ${2:target_type})", "Convert a value to a different type"),
            ("parse", "Parse string", "parse(${1:string}, ${2:format})", "Parse a string into a structured value"),
            ("format", "Format value", "format(${1:value}, ${2:template})", "Format a value using a template"),
            ("range", "Create range", "range(${1:start}, ${2:end})", "Create a range of numbers"),
            ("enumerate", "Enumerate items", "enumerate(${1:collection})", "Get indexed items from a collection"),
            ("zip", "Zip collections", "zip(${1:collection1}, ${2:collection2})", "Combine multiple collections"),
            ("map", "Map function", "map(${1:function}, ${2:collection})", "Apply function to each item"),
            ("filter", "Filter items", "filter(${1:predicate}, ${2:collection})", "Filter items based on condition"),
            ("reduce", "Reduce collection", "reduce(${1:function}, ${2:collection})", "Reduce collection to single value"),
            ("sort", "Sort collection", "sort(${1:collection})", "Sort items in a collection"),
            ("reverse", "Reverse collection", "reverse(${1:collection})", "Reverse order of items"),
            ("split", "Split string", "split(${1:string}, ${2:delimiter})", "Split string by delimiter"),
            ("join", "Join strings", "join(${1:strings}, ${2:separator})", "Join strings with separator"),
            ("replace", "Replace in string", "replace(${1:string}, ${2:old}, ${3:new})", "Replace text in string"),
            ("contains", "Check contains", "contains(${1:collection}, ${2:item})", "Check if collection contains item"),
            ("starts_with", "Check prefix", "starts_with(${1:string}, ${2:prefix})", "Check if string starts with prefix"),
            ("ends_with", "Check suffix", "ends_with(${1:string}, ${2:suffix})", "Check if string ends with suffix"),
            ("uppercase", "Convert to uppercase", "uppercase(${1:string})", "Convert string to uppercase"),
            ("lowercase", "Convert to lowercase", "lowercase(${1:string})", "Convert string to lowercase"),
            ("trim", "Trim whitespace", "trim(${1:string})", "Remove whitespace from string")
        ]
        
        return [
            CompletionItem(
                label=func,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Built-in function: {func}",
                documentation=description,
                insert_text=snippet,
                priority=70
            )
            for func, detail, snippet, description in functions
        ]
    
    def _get_builtin_types(self) -> List[CompletionItem]:
        """Get built-in type completions."""
        types = [
            ("number", "Numeric type", "Any numeric value (integer or decimal)"),
            ("string", "Text type", "Sequence of characters"),
            ("boolean", "Boolean type", "True or false value"),
            ("list", "List type", "Ordered collection of items"),
            ("dictionary", "Dictionary type", "Key-value mapping"),
            ("function", "Function type", "Callable function"),
            ("optional", "Optional type", "Value that may be null"),
            ("union", "Union type", "One of multiple possible types"),
            ("intersection", "Intersection type", "Combination of multiple types"),
            ("any", "Any type", "Any value type"),
            ("void", "Void type", "No return value")
        ]
        
        return [
            CompletionItem(
                label=type_name,
                kind=CompletionItemKind.CLASS,
                detail=f"Built-in type: {type_name}",
                documentation=description,
                priority=60
            )
            for type_name, detail, description in types
        ]
    
    def _get_stdlib_modules(self) -> List[CompletionItem]:
        """Get standard library module completions."""
        modules = [
            ("math", "Mathematical functions and constants"),
            ("string", "String manipulation functions"),
            ("file", "File system operations"),
            ("network", "Network and HTTP operations"),
            ("time", "Date and time operations"),
            ("json", "JSON parsing and serialization"),
            ("collections", "Collection manipulation functions")
        ]
        
        return [
            CompletionItem(
                label=module,
                kind=CompletionItemKind.MODULE,
                detail=f"Standard library: {module}",
                documentation=description,
                insert_text=f"import {module}",
                priority=65
            )
            for module, description in modules
        ]
    
    def analyze_context(self, text: str, line: int, column: int) -> Dict:
        """Analyze the context at the given position."""
        lines = text.split('\n')
        current_line = lines[line] if line < len(lines) else ""
        
        # Get text before cursor
        text_before_cursor = current_line[:column]
        
        # Determine context type
        context = {
            'type': 'general',
            'in_string': False,
            'in_comment': False,
            'after_dot': False,
            'after_import': False,
            'after_from': False,
            'in_function_call': False,
            'in_type_annotation': False,
            'prefix': '',
            'surrounding_text': current_line
        }
        
        # Check if in string
        string_count = text_before_cursor.count('"') + text_before_cursor.count("'")
        context['in_string'] = string_count % 2 == 1
        
        # Check if in comment
        context['in_comment'] = '#' in text_before_cursor and not context['in_string']
        
        if context['in_string'] or context['in_comment']:
            return context
        
        # Check for dot access
        context['after_dot'] = text_before_cursor.rstrip().endswith('.')
        
        # Check for import context
        import_match = re.search(r'\b(import|from)\s+(\w*)?$', text_before_cursor)
        if import_match:
            context['after_import'] = import_match.group(1) == 'import'
            context['after_from'] = import_match.group(1) == 'from'
        
        # Check for function call context
        paren_depth = text_before_cursor.count('(') - text_before_cursor.count(')')
        context['in_function_call'] = paren_depth > 0
        
        # Check for type annotation context
        context['in_type_annotation'] = ':' in text_before_cursor and not context['in_function_call']
        
        # Extract prefix (word being typed)
        word_match = re.search(r'\b(\w+)$', text_before_cursor)
        if word_match:
            context['prefix'] = word_match.group(1)
        
        return context
    
    def get_completions(self, text: str, line: int, column: int) -> List[CompletionItem]:
        """Get completion suggestions for the given position."""
        context = self.analyze_context(text, line, column)
        
        # Don't complete in strings or comments
        if context['in_string'] or context['in_comment']:
            return []
        
        completions = []
        
        # Context-specific completions
        if context['after_import'] or context['after_from']:
            completions.extend(self.stdlib_modules)
        elif context['after_dot']:
            completions.extend(self._get_member_completions(text, line, column))
        elif context['in_type_annotation']:
            completions.extend(self.builtin_types)
        else:
            # General completions
            completions.extend(self.keywords)
            completions.extend(self.builtin_functions)
            completions.extend(self.builtin_types)
            completions.extend(self._get_variable_completions())
            completions.extend(self._get_function_completions())
        
        # Filter by prefix
        prefix = context['prefix'].lower()
        if prefix:
            completions = [
                comp for comp in completions
                if comp.label.lower().startswith(prefix)
            ]
        
        # Sort by priority and label
        completions.sort(key=lambda x: (-x.priority, x.label))
        
        return completions
    
    def _get_member_completions(self, text: str, line: int, column: int) -> List[CompletionItem]:
        """Get member access completions (after dot)."""
        # This would require more sophisticated analysis
        # For now, return common string/list methods
        common_methods = [
            CompletionItem("length", CompletionItemKind.PROPERTY, "Get length", "Number of items"),
            CompletionItem("append", CompletionItemKind.METHOD, "Add item", "append(${1:item})"),
            CompletionItem("remove", CompletionItemKind.METHOD, "Remove item", "remove(${1:item})"),
            CompletionItem("contains", CompletionItemKind.METHOD, "Check contains", "contains(${1:item})"),
            CompletionItem("sort", CompletionItemKind.METHOD, "Sort items", "sort()"),
            CompletionItem("reverse", CompletionItemKind.METHOD, "Reverse order", "reverse()"),
            CompletionItem("split", CompletionItemKind.METHOD, "Split string", "split(${1:delimiter})"),
            CompletionItem("replace", CompletionItemKind.METHOD, "Replace text", "replace(${1:old}, ${2:new})"),
            CompletionItem("uppercase", CompletionItemKind.METHOD, "To uppercase", "uppercase()"),
            CompletionItem("lowercase", CompletionItemKind.METHOD, "To lowercase", "lowercase()"),
            CompletionItem("trim", CompletionItemKind.METHOD, "Trim whitespace", "trim()")
        ]
        return common_methods
    
    def _get_variable_completions(self) -> List[CompletionItem]:
        """Get variable completions from current scope."""
        symbols = self.scope_context.get_all_symbols()
        return [
            CompletionItem(
                label=symbol.name,
                kind=CompletionItemKind.VARIABLE,
                detail=f"Variable: {symbol.type_info or 'unknown'}",
                documentation=symbol.documentation,
                priority=90
            )
            for symbol in symbols
            if symbol.kind == "variable"
        ]
    
    def _get_function_completions(self) -> List[CompletionItem]:
        """Get user-defined function completions."""
        symbols = self.scope_context.get_all_symbols()
        return [
            CompletionItem(
                label=symbol.name,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Function: {symbol.type_info or 'unknown'}",
                documentation=symbol.documentation,
                insert_text=f"{symbol.name}(${{1:args}})",
                priority=85
            )
            for symbol in symbols
            if symbol.kind == "function"
        ]
    
    def update_symbols(self, text: str):
        """Update symbol table from source code."""
        try:
            # Reset scope context
            self.scope_context = ScopeContext()
            
            # Parse and extract symbols
            tokens = self.lexer.tokenize(text)
            ast = self.parser.parse(tokens)
            
            # Simple symbol extraction (would need more sophisticated AST walking)
            self._extract_symbols_from_ast(ast)
            
        except Exception:
            # If parsing fails, continue with existing symbols
            pass
    
    def _extract_symbols_from_ast(self, node):
        """Extract symbols from AST node."""
        if isinstance(node, ProcessDefinition):
            symbol = Symbol(
                name=node.name,
                kind="function",
                type_info=f"function({', '.join(p.name for p in node.parameters)})",
                documentation=getattr(node, 'docstring', None)
            )
            self.scope_context.add_symbol(symbol)
        
        elif isinstance(node, (LetStatement, DefineStatement)):
            symbol = Symbol(
                name=node.identifier,
                kind="variable",
                type_info=str(node.type_annotation) if node.type_annotation else None
            )
            self.scope_context.add_symbol(symbol)
        
        # Recursively process child nodes
        if hasattr(node, '__dict__'):
            for attr_value in node.__dict__.values():
                if isinstance(attr_value, list):
                    for item in attr_value:
                        if hasattr(item, '__dict__'):
                            self._extract_symbols_from_ast(item)
                elif hasattr(attr_value, '__dict__'):
                    self._extract_symbols_from_ast(attr_value)
    
    def get_function_signature_help(self, text: str, line: int, column: int) -> Optional[Dict]:
        """Get function signature help for current position."""
        lines = text.split('\n')
        current_line = lines[line] if line < len(lines) else ""
        text_before_cursor = current_line[:column]
        
        # Find function call
        func_match = re.search(r'(\w+)\s*\([^)]*$', text_before_cursor)
        if not func_match:
            return None
        
        func_name = func_match.group(1)
        
        # Get signature for built-in functions
        builtin_signatures = {
            'print': {
                'label': 'print(message: string)',
                'documentation': 'Print a message to the console',
                'parameters': [{'label': 'message', 'documentation': 'The message to print'}]
            },
            'length': {
                'label': 'length(collection: list|string)',
                'documentation': 'Get the length of a collection or string',
                'parameters': [{'label': 'collection', 'documentation': 'The collection or string'}]
            },
            'map': {
                'label': 'map(function: function, collection: list)',
                'documentation': 'Apply function to each item in collection',
                'parameters': [
                    {'label': 'function', 'documentation': 'Function to apply'},
                    {'label': 'collection', 'documentation': 'Collection to process'}
                ]
            }
        }
        
        return builtin_signatures.get(func_name)
    
    def get_hover_info(self, text: str, line: int, column: int) -> Optional[str]:
        """Get hover information for symbol at position."""
        lines = text.split('\n')
        current_line = lines[line] if line < len(lines) else ""
        
        # Extract word at position
        start = column
        end = column
        
        while start > 0 and (current_line[start - 1].isalnum() or current_line[start - 1] == '_'):
            start -= 1
        
        while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
            end += 1
        
        if start == end:
            return None
        
        word = current_line[start:end]
        
        # Check built-in functions
        builtin_docs = {
            'print': 'Print a message to the console\n\n**Syntax:** `print(message)`',
            'length': 'Get the length of a collection or string\n\n**Syntax:** `length(collection)`',
            'map': 'Apply a function to each item in a collection\n\n**Syntax:** `map(function, collection)`',
            'filter': 'Filter items based on a condition\n\n**Syntax:** `filter(predicate, collection)`',
            'if': 'Conditional execution based on a boolean expression',
            'for': 'Iterate over items in a collection',
            'function': 'Define a reusable block of code with parameters'
        }
        
        if word in builtin_docs:
            return builtin_docs[word]
        
        # Check user-defined symbols
        symbol = self.scope_context.find_symbol(word)
        if symbol:
            return f"**{symbol.name}** ({symbol.kind})\n\n{symbol.documentation or 'User-defined symbol'}"
        
        return None