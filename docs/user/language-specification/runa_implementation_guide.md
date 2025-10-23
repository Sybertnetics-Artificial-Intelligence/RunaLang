# Runa Implementation Guide
*Complete Guide for Language Implementers and Tool Builders*

**Last Updated**: 2025-10-19
**Implementation Status**: Canon Mode fully specified, Developer Mode planned, Viewer Mode planned

## Overview

This implementation guide provides comprehensive instructions for building Runa language processors, including compilers, interpreters, transpilers, and development tools. It covers the complete implementation pipeline from lexical analysis through code generation and runtime support.

**IMPORTANT**: Runa supports multiple syntax modes (Canon, Developer, Viewer). This guide focuses on implementing **Canon Mode** as the primary syntax. Developer Mode (symbolic operators) and Viewer Mode (natural language display) are planned future additions.

## Syntax Modes

Runa implements a triple syntax architecture to serve different audiences and use cases:

### Canon Mode (Primary Implementation Target)
- **Status**: Fully specified and ready for implementation
- **Characteristics**:
  - Natural language operators: `multiplied by`, `is equal to`, `is greater than`
  - Multi-word identifiers: `user name`, `total count`, `maximum retry limit`
  - Explicit block terminators: `End Process`, `End Type`, `End If`
  - Standard Runa keywords: `Process`, `Type`, `Let`, `Set`
- **Purpose**:
  - Primary mode for human-readable code
  - Optimal for AI code generation and comprehension
  - Default mode for all Runa source files
- **Implementation Priority**: **Implement this mode FIRST**

### Developer Mode (Future)
- **Status**: Planned, not yet implemented
- **Characteristics**:
  - Symbolic operators: `*`, `==`, `>`
  - Same keywords as Canon mode (keywords don't change between modes)
  - Same block terminators as Canon mode
  - Familiar to programmers from other languages
- **Purpose**:
  - Efficient input for experienced developers
  - Optional alternative to Canon Mode
- **Implementation Note**: Developer Mode will auto-translate to Canon during parsing

### Viewer Mode (Future)
- **Status**: Planned, not yet implemented
- **Characteristics**:
  - Full natural language sentences
  - Educational context and explanations
  - Read-only display mode
- **Purpose**:
  - Documentation generation
  - Code review by non-programmers
  - Educational materials
- **Implementation Note**: Post-processing layer on top of Canon/Developer AST

### Mode Consistency Rules

1. **Keywords are identical** across Canon and Developer modes
2. **Only operators differ** between Canon and Developer modes
3. **Block terminators are required** in both Canon and Developer modes
4. **Viewer mode is generated**, not parsed

For detailed syntax mode specifications, see the main language specification.

## Key Syntax Patterns (Canon Mode)

This section highlights critical syntax patterns that implementers must understand for Canon Mode.

### Constructor Syntax

Runa uses explicit constructor syntax to create new object instances:

```runa
Note: Basic constructor (no field initialization)
Let user be a value of type User

Note: Constructor with field initialization
Let point be a value of type Point with x as 10, y as 20

Note: Complex constructor
Let config be a value of type Configuration with
    debug_mode as true,
    log_level as "INFO",
    max_retries as 5

Note: Shortened form (optional)
Let settings be of type Settings with timeout as 30
```

**Important**: The pattern `a value of type TypeName` is REQUIRED for constructors. This disambiguates object creation from function calls.

### Multi-Word Identifiers (Encasing Keyword Pairs)

Runa supports natural multi-word variable names captured between keyword boundaries:

```runa
Note: Multi-word variable declarations
Let user input value be 42
Let maximum retry count be 3
Let total calculation result be sum

Note: Multi-word variable assignment
Set total calculation result to new_sum
Set user input value to user_input_value plus 1

Note: "Last occurrence wins" for ambiguous cases
Let to be or not to be be "that is the question"
Note: Variable name is "to be or not to be", value is the string
```

### Imperative Statement Patterns

Canon Mode includes natural imperative statements for common mutations:

```runa
Note: Compound assignment statements
Increase count by 1
Decrease health points by damage amount
Multiply total price by tax rate
Divide total cost by number of items

Note: These are equivalent to:
Set count to count gets increased by 1
Set health points to health points gets decreased by damage amount
Set total price to total price gets multiplied by tax rate
Set total cost to total cost gets divided by number of items
```

### Block Terminators

**CRITICAL**: All block structures in Runa MUST end with explicit `End` keywords:

```runa
Note: Function blocks
Process called "calculate_area" that takes radius as Float returns Float:
    Return 3.14159 multiplied by radius multiplied by radius
End Process

Note: Type blocks
Type called "Point":
    Field x as Float
    Field y as Float
End Type

Note: Conditional blocks
If value is greater than 10:
    Display "Large value"
Otherwise if value is greater than 5:
    Display "Medium value"
Otherwise:
    Display "Small value"
End If

Note: Loop blocks
For each item in items:
    Display item
End For

While counter is less than limit:
    Increase counter by 1
End While
```

### Natural Language Operators

Canon Mode uses natural language for ALL operators:

```runa
Note: Arithmetic
Let result be a plus b
Let product be width multiplied by height
Let quotient be total divided by count
Let remainder be value modulo by 10
Let power be base to the power of exponent

Note: Comparison
If score is greater than 90:
    Display "Excellent"
End If

If age is less than or equal to 18:
    Display "Minor"
End If

If status is equal to "active":
    Display "Running"
End If

Note: Logical
If is_valid and is_complete:
    Process the data
End If

If is_error or is_warning:
    Log the message
End If

Note: String operations
Let full_name be first_name joined with " " joined with last_name
```

## Architecture Overview

### Core Components

1. **Lexer** - Tokenizes Runa source code (Canon Mode natural language syntax)
2. **Parser** - Builds Abstract Syntax Tree (AST) from token stream
3. **Semantic Analyzer** - Performs type checking and semantic validation
4. **IR Generator** - Converts AST to intermediate representation
5. **Runtime** - Executes compiled bytecode or generates target code
6. **Standard Library** - Provides essential functions and types (14-tier architecture)
7. **Formatter** - Pretty-prints Runa code in canonical style

### Language Keywords vs Standard Library

Runa distinguishes between **language keywords** and **standard library functions**:

#### Language Keywords (Built into Runtime)
```runa
Display "Hello World"     Note: Language construct
Let x be 42              Note: Language construct
length of list_var       Note: Language construct
```

#### Standard Library Functions (Callable)
```runa
sort_list with list as numbers                    Note: Function call
filter_list with list as data and predicate as f  Note: Function call
map_list with list as items and function as g     Note: Function call
```

## Implementation Architecture

### Core Components

```
Runa Implementation Pipeline:

Source Code
    ↓
Lexical Analysis (Tokenizer)
    ↓
Syntax Analysis (Parser)
    ↓
Semantic Analysis (Type Checker)
    ↓
Intermediate Representation (IR)
    ↓
Optimization Passes
    ↓
Code Generation (Target Language)
    ↓
Runtime Library Integration
    ↓
Target Executable/Script
```

### Module Structure

Based on the v0.0.8.5 bootstrap implementation:

```
runa/bootstrap/v0.0.8.5/
├── compiler/
│   ├── frontend/           # Lexical analysis, parsing, AST generation
│   ├── middle/             # Semantic analysis, type checking, IR
│   ├── backend/            # Code generation
│   │   ├── bytecode_gen/   # Bytecode generation
│   │   ├── machine_code/   # Native code generation
│   │   └── syscalls/       # System call interfaces
│   ├── internal/           # Compiler internals
│   ├── services/           # Compiler services
│   ├── tools/              # Compiler-specific tools
│   ├── testing/            # Compiler tests
│   └── driver/             # Compiler driver/CLI
├── runtime/
│   ├── core/               # Core runtime functionality
│   ├── core_asm/           # Assembly-level runtime support
│   ├── concurrency/        # Concurrency primitives
│   ├── io/                 # I/O operations
│   ├── aott/               # Ahead-of-time translation
│   ├── integration/        # External integrations
│   ├── services/           # Runtime services
│   └── tools/              # Runtime tools
├── dev_tools/              # Development tools (LSP, debugger, formatter)
├── docs/                   # Documentation
└── tests/                  # Integration and system tests
```

## Phase 1: Lexical Analysis

### Token Definition

The Runa compiler is self-hosted (written in Runa). Token definitions are found in `compiler/frontend/lexer/token.runa`:

```runa
Note: Token type enumeration for Canon Mode
Type called "TokenType":
    Note: Literal types
    Case LITERAL_INTEGER
    Case LITERAL_FLOAT
    Case LITERAL_STRING
    Case LITERAL_BOOLEAN
    Case LITERAL_NULL

    Note: Identifiers
    Case IDENTIFIER
    Case MULTI_WORD_IDENTIFIER

    Note: Keywords
    Case KEYWORD_LET
    Case KEYWORD_DEFINE
    Case KEYWORD_SET
    Case KEYWORD_IF
    Case KEYWORD_OTHERWISE
    Case KEYWORD_UNLESS
    Case KEYWORD_WHEN
    Case KEYWORD_MATCH
    Case KEYWORD_PROCESS
    Case KEYWORD_TYPE
    Case KEYWORD_RETURN
    Case KEYWORD_END
    Note: ... (all other keywords)

    Note: Canon Mode natural language operators
    Case OPERATOR_PLUS
    Case OPERATOR_MINUS
    Case OPERATOR_MULTIPLIED_BY
    Case OPERATOR_DIVIDED_BY
    Case OPERATOR_MODULO_BY
    Case OPERATOR_IS_EQUAL_TO
    Case OPERATOR_IS_NOT_EQUAL_TO
    Case OPERATOR_IS_GREATER_THAN
    Case OPERATOR_IS_LESS_THAN
    Note: ... (all other operators)

    Note: Punctuation
    Case PUNCT_COLON
    Case PUNCT_COMMA
    Case PUNCT_SEMICOLON
    Case PUNCT_LPAREN
    Case PUNCT_RPAREN
    Case PUNCT_LBRACKET
    Case PUNCT_RBRACKET
    Case PUNCT_LBRACE
    Case PUNCT_RBRACE

    Note: Special tokens
    Case SPECIAL_INDENT
    Case SPECIAL_DEDENT
    Case SPECIAL_NEWLINE
    Case SPECIAL_EOF

    Note: AI Annotations
    Case ANNOTATION_REASONING
    Case ANNOTATION_END_REASONING
    Case ANNOTATION_IMPLEMENTATION
    Case ANNOTATION_END_IMPLEMENTATION
    Note: ... (all other annotation tokens)
End Type

Note: Token structure with location information
Type called "Token":
    Field token_type as TokenType
    Field value as String
    Field line as Integer
    Field column as Integer
    Field position as Integer
    Field length as Integer
End Type
```

### Enhanced Lexer Implementation

The Runa lexer has been enhanced with production-grade performance optimizations, advanced error recovery, and comprehensive edge case handling.

#### Key Enhancements

**Performance Optimizations:**
- **Streaming Mode**: Automatically activates for files larger than 1MB
- **Chunked Processing**: 8KB chunks for efficient memory usage
- **Buffer Optimization**: Increased buffer size to 8KB for better throughput
- **Lookahead Enhancement**: Increased to 20 tokens for complex multi-word constructs
- **Memory Management**: Token pooling, string sharing, automatic cleanup

**Advanced Error Recovery:**
- **Multiple Recovery Strategies**: Skip to newline, whitespace, identifier, operator, string start, comment start
- **Context-Aware Recovery**: Intelligent recovery based on context
- **Recovery Confidence**: Scoring for recovery strategy effectiveness
- **Enhanced Error Reporting**: Detailed error messages with suggestions

**Edge Case Handling:**
- **Extended String Support**: Up to 50KB strings with enhanced Unicode
- **Complex Number Formats**: Support for large numbers (200+ digits) with underscore separators
- **Multi-word Constructs**: Support for constructs up to 8 words with case-insensitive matching
- **Deep Indentation**: Robust handling of complex indentation patterns

#### Implementation Example

```runa
Note: Enhanced Lexer Usage
Let source be "Let x be 42\nIf x is greater than 10:\n    Display \"Large number\""
Let tokens be tokenize with source_code as source and file_path as "test.runa"

Note: Performance monitoring
Let metrics be get_lexer_performance_metrics with lexer as lexer
Display "Tokens Generated: " plus metrics.tokens_generated
Display "Multi-word Matches: " plus metrics.multi_word_matches
Display "Error Recoveries: " plus metrics.error_recoveries
Display "Processing Time: " plus metrics.processing_time_ms plus "ms"

Note: Memory usage tracking
Let memory_usage be get_lexer_memory_usage with lexer as lexer
Display "Memory Usage: " plus memory_usage.current_memory_kb plus "KB"
```

#### Error Recovery Example

```runa
Note: Malformed source with error recovery
Let malformed_source be "Let x be \"Hello World\nLet y be 42"
Let tokens be tokenize with source_code as malformed_source and file_path as "malformed.runa"

Note: Lexer recovers and continues processing
Return length of tokens is greater than 0 and
       tokens at index (length of tokens minus 1).type is equal to EOF
```

#### Configuration Options

```runa
Note: Lexer configuration
Let lexer_config be dictionary containing:
    "max_string_length" as 50000
    "max_number_length" as 200
    "max_unicode_escapes" as 100
    "max_underscores" as 50
    "max_phrase_length" as 8
    "streaming_threshold" as 1000000
    "chunk_size" as 8192
    "max_lookahead" as 20
    "max_recovery_depth" as 10
```

#### Performance Benchmarks

- **Small Files (<1KB)**: <1ms processing time
- **Medium Files (1-100KB)**: 1-10ms processing time
- **Large Files (100KB-1MB)**: 10-100ms processing time
- **Very Large Files (>1MB)**: 100ms+ with streaming mode

#### Runa Lexer Implementation

The actual lexer is implemented in `compiler/frontend/lexer/lexer.runa`:

```runa
Note: Runa Lexer - Tokenizes Canon Mode source code
Type called "Lexer":
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]  # Track indentation levels
        
        # Canon Mode natural language operators
        self.multi_word_patterns = [
            (r'multiplied\s+by', TokenType.MULTIPLIED_BY),
            (r'divided\s+by', TokenType.DIVIDED_BY),
            (r'plus', TokenType.PLUS),
            (r'minus', TokenType.MINUS),
            (r'modulo\s+by', TokenType.MODULO_BY),
            (r'is\s+equal\s+to', TokenType.IS_EQUAL_TO),
            (r'is\s+not\s+equal\s+to', TokenType.IS_NOT_EQUAL_TO),
            (r'is\s+greater\s+than\s+or\s+equal\s+to', TokenType.IS_GREATER_THAN_OR_EQUAL_TO),
            (r'is\s+less\s+than\s+or\s+equal\s+to', TokenType.IS_LESS_THAN_OR_EQUAL_TO),
            (r'is\s+greater\s+than', TokenType.IS_GREATER_THAN),
            (r'is\s+less\s+than', TokenType.IS_LESS_THAN),
            (r'joined\s+with', TokenType.JOINED_WITH),
            (r'to\s+the\s+power\s+of', TokenType.TO_THE_POWER_OF),
            (r'gets\s+increased\s+by', TokenType.GETS_INCREASED_BY),
            (r'gets\s+decreased\s+by', TokenType.GETS_DECREASED_BY),
            (r'gets\s+multiplied\s+by', TokenType.GETS_MULTIPLIED_BY),
            (r'gets\s+divided\s+by', TokenType.GETS_DIVIDED_BY),
            # ... add all multi-word operators
        ]
        
        # Keyword mapping
        self.keywords = {
            'Let': TokenType.LET,
            'Define': TokenType.DEFINE,
            'Set': TokenType.SET,
            'If': TokenType.IF,
            'Otherwise': TokenType.OTHERWISE,
            'Unless': TokenType.UNLESS,
            'When': TokenType.WHEN,
            'Match': TokenType.MATCH,
            'Process': TokenType.PROCESS,
            'Type': TokenType.TYPE,
            'Return': TokenType.RETURN,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
            'null': TokenType.NULL,
            'none': TokenType.NULL,
            'nil': TokenType.NULL,
            # ... add all keywords
        }

    def tokenize(self) -> List[Token]:
        while not self._at_end():
            self._scan_token()
        
        # Add final DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self._add_token(TokenType.DEDENT)
        
        self._add_token(TokenType.EOF)
        return self.tokens
    
    def _scan_token(self):
        # Handle indentation at start of line
        if self.column == 1:
            self._handle_indentation()
        
        char = self._advance()
        
        # Whitespace (but not newlines - those are significant)
        if char in ' \t':
            return
        
        # Newlines
        if char == '\n':
            self._add_token(TokenType.NEWLINE)
            self.line += 1
            self.column = 1
            return
        
        # Comments
        if char == 'N' and self._match_word('Note:'):
            self._scan_comment()
            return
        
        # String literals
        if char in '"\'':
            self._scan_string(char)
            return
        
        # Numbers
        if char.isdigit():
            self._scan_number()
            return
        
        # Multi-word operators and identifiers
        if char.isalpha() or char == '_':
            self._scan_identifier_or_operator()
            return
        
        # Single-character tokens
        single_chars = {
            ':': TokenType.COLON,
            ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '@': None,  # Handle annotations separately
        }
        
        if char in single_chars:
            if char == '@':
                self._scan_annotation()
            else:
                self._add_token(single_chars[char])
            return
        
        # Unknown character
        raise LexError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
    
    def _handle_indentation(self):
        """Handle Python-style indentation"""
        indent_level = 0
        start_pos = self.position
        
        # Count leading whitespace
        while not self._at_end() and self._peek() in ' \t':
            if self._peek() == ' ':
                indent_level += 1
            elif self._peek() == '\t':
                indent_level += 8  # Tab = 8 spaces
            self._advance()
        
        # Skip empty lines
        if self._peek() == '\n':
            return
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # Increased indentation
            self.indent_stack.append(indent_level)
            self._add_token(TokenType.INDENT)
        elif indent_level < current_indent:
            # Decreased indentation
            while len(self.indent_stack) > 1 and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                self._add_token(TokenType.DEDENT)
            
            if self.indent_stack[-1] != indent_level:
                raise LexError(f"Indentation error at line {self.line}")
    
    def _scan_identifier_or_operator(self):
        """Scan multi-word identifiers and operators"""
        start = self.position - 1
        
        # Try to match multi-word operators first
        for pattern, token_type in self.multi_word_patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            match = regex.match(self.text, start)
            if match:
                self.position = start + len(match.group())
                self.column += len(match.group()) - 1
                self._add_token(token_type, match.group())
                return
        
        # Scan identifier (potentially multi-word)
        words = []
        word_start = start
        
        while True:
            # Scan current word
            while (not self._at_end() and 
                   (self._peek().isalnum() or self._peek() == '_')):
                self._advance()
            
            words.append(self.text[word_start:self.position])
            
            # Check if next token is a space followed by another identifier
            if (not self._at_end() and self._peek() == ' ' and
                self.position + 1 < len(self.text) and
                self.text[self.position + 1].isalpha()):
                
                # Look ahead to see if this continues the identifier
                next_space = self.text.find(' ', self.position + 1)
                next_non_alpha = self.position + 1
                while (next_non_alpha < len(self.text) and 
                       self.text[next_non_alpha].isalnum()):
                    next_non_alpha += 1
                
                # If the next word is not a keyword, include it in identifier
                next_word = self.text[self.position + 1:next_non_alpha]
                if next_word not in self.keywords:
                    self._advance()  # Skip space
                    word_start = self.position
                    continue
            
            break
        
        # Create the identifier/keyword token
        full_identifier = ' '.join(words)
        
        # Check if it's a keyword
        token_type = self.keywords.get(words[0], TokenType.IDENTIFIER)
        if len(words) > 1:
            token_type = TokenType.MULTI_WORD_IDENTIFIER
        
        self._add_token(token_type, full_identifier)
    
    def _scan_string(self, quote_char: str):
        """Scan string literals with support for raw and f-strings"""
        string_start = self.position - 1
        
        # Check for string prefixes (r, f, etc.)
        prefix = ''
        if string_start > 0:
            possible_prefix = self.text[string_start - 1]
            if possible_prefix in 'rfRF':
                prefix = possible_prefix.lower()
        
        content = ''
        while not self._at_end() and self._peek() != quote_char:
            if self._peek() == '\\' and prefix != 'r':  # No escapes in raw strings
                self._advance()  # Skip backslash
                if not self._at_end():
                    escape_char = self._advance()
                    content += self._process_escape(escape_char)
            else:
                content += self._advance()
        
        if self._at_end():
            raise LexError(f"Unterminated string at line {self.line}")
        
        self._advance()  # Consume closing quote
        
        # Handle f-string interpolation
        if prefix == 'f':
            self._add_token(TokenType.STRING, self._process_f_string(content))
        else:
            self._add_token(TokenType.STRING, content)
    
    def _scan_annotation(self):
        """Scan AI annotation tokens"""
        start = self.position - 1
        
        # Match annotation patterns
        annotation_patterns = {
            r'@Reasoning:': TokenType.AT_REASONING,
            r'@End_Reasoning': TokenType.AT_END_REASONING,
            r'@Implementation:': TokenType.AT_IMPLEMENTATION,
            r'@End_Implementation': TokenType.AT_END_IMPLEMENTATION,
            r'@Task:': TokenType.AT_TASK,
            r'@End_Task': TokenType.AT_END_TASK,
            # ... add all annotation patterns
        }
        
        for pattern, token_type in annotation_patterns.items():
            regex = re.compile(pattern)
            match = regex.match(self.text, start)
            if match:
                self.position = start + len(match.group())
                self.column += len(match.group()) - 1
                self._add_token(token_type, match.group())
                return
        
        # If no annotation pattern matched, treat as regular @
        self._add_token(TokenType.AT, '@')
```

## Phase 2: Syntax Analysis

### AST Node Hierarchy

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Union
from dataclasses import dataclass

class ASTNode(ABC):
    """Base class for all AST nodes"""
    line: int
    column: int

class Expression(ASTNode):
    """Base class for expressions"""
    pass

class Statement(ASTNode):
    """Base class for statements"""
    pass

class Declaration(ASTNode):
    """Base class for declarations"""
    pass

# Literal expressions
@dataclass
class LiteralExpression(Expression):
    value: Any
    literal_type: str  # "integer", "float", "string", "boolean", "null"

@dataclass
class IdentifierExpression(Expression):
    name: str
    is_multi_word: bool = False

# Binary and unary expressions
@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression

# Function calls
@dataclass
class FunctionCall(Expression):
    function: Expression
    arguments: List['Argument']

@dataclass
class Argument:
    name: Optional[str]  # None for positional args
    value: Expression
    is_spread: bool = False

# Statements
@dataclass
class LetStatement(Statement):
    pattern: 'Pattern'
    type_annotation: Optional['TypeExpression']
    value: Expression

@dataclass
class SetStatement(Statement):
    target: Expression
    value: Expression

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_block: List[Statement]
    elif_clauses: List['ElifClause']
    else_block: Optional[List[Statement]]

@dataclass
class ElifClause:
    condition: Expression
    block: List[Statement]

# Pattern matching
@dataclass
class MatchStatement(Statement):
    expression: Expression
    cases: List['MatchCase']

@dataclass
class MatchCase:
    pattern: 'Pattern'
    guard: Optional[Expression]
    block: List[Statement]

# Patterns
class Pattern(ASTNode):
    pass

@dataclass
class IdentifierPattern(Pattern):
    name: str

@dataclass
class LiteralPattern(Pattern):
    value: Any

@dataclass
class WildcardPattern(Pattern):
    pass

@dataclass
class ListPattern(Pattern):
    elements: List[Pattern]
    rest_pattern: Optional[str] = None

@dataclass
class RecordPattern(Pattern):
    fields: List['FieldPattern']

@dataclass
class FieldPattern:
    name: str
    pattern: Pattern

# Type expressions
class TypeExpression(ASTNode):
    pass

@dataclass
class BasicType(TypeExpression):
    name: str

@dataclass
class GenericType(TypeExpression):
    base: TypeExpression
    parameters: List[TypeExpression]

@dataclass
class UnionType(TypeExpression):
    types: List[TypeExpression]

@dataclass
class FunctionType(TypeExpression):
    parameters: List[TypeExpression]
    return_type: TypeExpression

# Declarations
@dataclass
class FunctionDefinition(Declaration):
    name: str
    generic_params: List[str]
    parameters: List['Parameter']
    return_type: Optional[TypeExpression]
    body: List[Statement]
    is_async: bool = False

@dataclass
class Parameter:
    name: str
    type_annotation: Optional[TypeExpression]
    default_value: Optional[Expression]

@dataclass
class TypeDefinition(Declaration):
    name: str
    generic_params: List[str]
    definition: Union['RecordDefinition', 'ADTDefinition', 'TypeAlias']

# AI Annotations
@dataclass
class ReasoningAnnotation(ASTNode):
    content: str

@dataclass
class ImplementationAnnotation(ASTNode):
    content: str

@dataclass
class TaskAnnotation(ASTNode):
    objective: str
    constraints: List[str]
    input_format: str
    output_format: str
    target_language: str
    priority: str
```

### Parser Implementation

```python
from typing import List, Optional, Union

class RunaParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> List[Union[Declaration, Statement]]:
        """Parse the token stream into an AST"""
        nodes = []
        
        while not self._at_end():
            if self._check_annotation():
                nodes.append(self._parse_annotation())
            elif self._check_declaration():
                nodes.append(self._parse_declaration())
            else:
                nodes.append(self._parse_statement())
        
        return nodes
    
    def _parse_declaration(self) -> Declaration:
        """Parse top-level declarations"""
        if self._match(TokenType.PROCESS):
            return self._parse_function_definition()
        elif self._match(TokenType.TYPE):
            return self._parse_type_definition()
        elif self._match(TokenType.IMPORT):
            return self._parse_import_statement()
        else:
            raise ParseError(f"Expected declaration at line {self._peek().line}")
    
    def _parse_function_definition(self) -> FunctionDefinition:
        """Parse function (process) definition"""
        is_async = False
        if self._previous().type == TokenType.ASYNC:
            is_async = True
            self._consume(TokenType.PROCESS, "Expected 'Process' after 'Async'")
        
        self._consume(TokenType.CALLED, "Expected 'called' after 'Process'")
        
        name_token = self._consume(TokenType.STRING, "Expected function name")
        name = name_token.value
        
        # Generic parameters
        generic_params = []
        if self._match(TokenType.LBRACKET):
            generic_params = self._parse_generic_parameters()
            self._consume(TokenType.RBRACKET, "Expected ']' after generic parameters")
        
        # Parameters
        parameters = []
        if self._match(TokenType.THAT, TokenType.TAKES):
            parameters = self._parse_parameter_list()
        
        # Return type
        return_type = None
        if self._match(TokenType.RETURNS):
            return_type = self._parse_type_expression()
        
        self._consume(TokenType.COLON, "Expected ':' before function body")
        
        # Function body
        body = self._parse_block()
        
        return FunctionDefinition(
            name=name,
            generic_params=generic_params,
            parameters=parameters,
            return_type=return_type,
            body=body,
            is_async=is_async,
            line=name_token.line,
            column=name_token.column
        )
    
    def _parse_statement(self) -> Statement:
        """Parse statements"""
        if self._match(TokenType.LET):
            return self._parse_let_statement()
        elif self._match(TokenType.SET):
            return self._parse_set_statement()
        elif self._match(TokenType.IF):
            return self._parse_if_statement()
        elif self._match(TokenType.MATCH):
            return self._parse_match_statement()
        elif self._match(TokenType.FOR):
            return self._parse_for_statement()
        elif self._match(TokenType.WHILE):
            return self._parse_while_statement()
        elif self._match(TokenType.RETURN):
            return self._parse_return_statement()
        else:
            # Expression statement
            expr = self._parse_expression()
            return ExpressionStatement(expr, expr.line, expr.column)
    
    def _parse_expression(self) -> Expression:
        """Parse expressions with proper precedence"""
        return self._parse_ternary()
    
    def _parse_ternary(self) -> Expression:
        """Parse ternary conditional expressions"""
        expr = self._parse_or()
        
        if self._match(TokenType.IF):
            condition = self._parse_or()
            self._consume(TokenType.ELSE, "Expected 'else' in ternary expression")
            else_expr = self._parse_ternary()
            return TernaryExpression(expr, condition, else_expr, expr.line, expr.column)
        
        return expr
    
    def _parse_or(self) -> Expression:
        """Parse logical OR expressions"""
        expr = self._parse_and()
        
        while self._match(TokenType.OR):
            operator = self._previous().value
            right = self._parse_and()
            expr = BinaryExpression(expr, operator, right, expr.line, expr.column)
        
        return expr
    
    def _parse_and(self) -> Expression:
        """Parse logical AND expressions"""
        expr = self._parse_equality()
        
        while self._match(TokenType.AND):
            operator = self._previous().value
            right = self._parse_equality()
            expr = BinaryExpression(expr, operator, right, expr.line, expr.column)
        
        return expr
    
    def _parse_equality(self) -> Expression:
        """Parse equality and comparison expressions"""
        expr = self._parse_addition()
        
        while self._match(TokenType.IS_EQUAL_TO, TokenType.IS_NOT_EQUAL_TO,
                           TokenType.IS_GREATER_THAN, TokenType.IS_LESS_THAN,
                           TokenType.IS_GREATER_THAN_OR_EQUAL_TO,
                           TokenType.IS_LESS_THAN_OR_EQUAL_TO):
            operator = self._previous().value
            right = self._parse_addition()
            expr = BinaryExpression(expr, operator, right, expr.line, expr.column)
        
        return expr
    
    def _parse_addition(self) -> Expression:
        """Parse addition and subtraction"""
        expr = self._parse_multiplication()
        
        while self._match(TokenType.PLUS, TokenType.MINUS, TokenType.JOINED_WITH):
            operator = self._previous().value
            right = self._parse_multiplication()
            expr = BinaryExpression(expr, operator, right, expr.line, expr.column)
        
        return expr
    
    def _parse_multiplication(self) -> Expression:
        """Parse multiplication, division, and modulo"""
        expr = self._parse_unary()
        
        while self._match(TokenType.MULTIPLIED_BY, TokenType.DIVIDED_BY, TokenType.MODULO):
            operator = self._previous().value
            right = self._parse_unary()
            expr = BinaryExpression(expr, operator, right, expr.line, expr.column)
        
        return expr
    
    def _parse_unary(self) -> Expression:
        """Parse unary expressions"""
        if self._match(TokenType.NOT, TokenType.NEGATIVE, TokenType.POSITIVE):
            operator = self._previous().value
            expr = self._parse_unary()
            return UnaryExpression(operator, expr, self._previous().line, self._previous().column)
        
        return self._parse_power()
    
    def _parse_power(self) -> Expression:
        """Parse power expressions"""
        expr = self._parse_postfix()
        
        if self._match(TokenType.TO_THE_POWER_OF):
            operator = self._previous().value
            right = self._parse_unary()  # Right associative
            expr = BinaryExpression(expr, operator, right, expr.line, expr.column)
        
        return expr
    
    def _parse_postfix(self) -> Expression:
        """Parse postfix expressions (member access, indexing, calls)"""
        expr = self._parse_primary()
        
        while True:
            if self._match(TokenType.DOT):
                name = self._consume(TokenType.IDENTIFIER, "Expected property name").value
                expr = MemberAccess(expr, name, expr.line, expr.column)
            elif self._match(TokenType.LBRACKET):
                index = self._parse_expression()
                self._consume(TokenType.RBRACKET, "Expected ']'")
                expr = IndexAccess(expr, index, expr.line, expr.column)
            elif self._match(TokenType.LPAREN):
                args = self._parse_argument_list()
                self._consume(TokenType.RPAREN, "Expected ')'")
                expr = FunctionCall(expr, args, expr.line, expr.column)
            elif self._match(TokenType.WITH):
                args = self._parse_named_arguments()
                expr = FunctionCall(expr, args, expr.line, expr.column)
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> Expression:
        """Parse primary expressions"""
        if self._match(TokenType.INTEGER):
            return LiteralExpression(self._previous().value, "integer", 
                                   self._previous().line, self._previous().column)
        
        if self._match(TokenType.FLOAT):
            return LiteralExpression(self._previous().value, "float",
                                   self._previous().line, self._previous().column)
        
        if self._match(TokenType.STRING):
            return LiteralExpression(self._previous().value, "string",
                                   self._previous().line, self._previous().column)
        
        if self._match(TokenType.BOOLEAN):
            value = self._previous().value == "true"
            return LiteralExpression(value, "boolean",
                                   self._previous().line, self._previous().column)
        
        if self._match(TokenType.NULL):
            return LiteralExpression(None, "null",
                                   self._previous().line, self._previous().column)
        
        if self._match(TokenType.IDENTIFIER, TokenType.MULTI_WORD_IDENTIFIER):
            name = self._previous().value
            is_multi_word = self._previous().type == TokenType.MULTI_WORD_IDENTIFIER
            return IdentifierExpression(name, is_multi_word,
                                      self._previous().line, self._previous().column)
        
        if self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        if self._match(TokenType.LBRACKET):
            return self._parse_list_literal()
        
        if self._match(TokenType.LBRACE):
            return self._parse_dictionary_literal()
        
        raise ParseError(f"Unexpected token {self._peek().type} at line {self._peek().line}")
```

## Phase 3: Semantic Analysis

### Symbol Table Implementation

```python
from typing import Dict, Optional, Any, List
from enum import Enum

class SymbolType(Enum):
    VARIABLE = "variable"
    FUNCTION = "function"
    TYPE = "type"
    MODULE = "module"

@dataclass
class Symbol:
    name: str
    symbol_type: SymbolType
    data_type: Optional['Type']
    value: Optional[Any]
    is_mutable: bool
    is_exported: bool
    definition_location: tuple  # (line, column)

class SymbolTable:
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
        self.children: List['SymbolTable'] = []
    
    def define(self, symbol: Symbol) -> bool:
        """Define a new symbol in this scope"""
        if symbol.name in self.symbols:
            return False  # Symbol already exists
        
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope and parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        
        if self.parent:
            return self.parent.lookup(name)
        
        return None
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up a symbol only in this scope"""
        return self.symbols.get(name)
    
    def create_child_scope(self) -> 'SymbolTable':
        """Create a new child scope"""
        child = SymbolTable(parent=self)
        self.children.append(child)
        return child
```

### Type System Implementation

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class Type(ABC):
    """Base class for all types"""
    
    @abstractmethod
    def is_assignable_to(self, other: 'Type') -> bool:
        """Check if this type can be assigned to another type"""
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        """Get string representation of type"""
        pass

class BasicType(Type):
    def __init__(self, name: str):
        self.name = name
    
    def is_assignable_to(self, other: Type) -> bool:
        if isinstance(other, BasicType):
            return self.name == other.name
        if isinstance(other, UnionType):
            return any(self.is_assignable_to(t) for t in other.types)
        return False
    
    def to_string(self) -> str:
        return self.name

class GenericType(Type):
    def __init__(self, base: Type, parameters: List[Type]):
        self.base = base
        self.parameters = parameters
    
    def is_assignable_to(self, other: Type) -> bool:
        if isinstance(other, GenericType):
            if not self.base.is_assignable_to(other.base):
                return False
            if len(self.parameters) != len(other.parameters):
                return False
            return all(p1.is_assignable_to(p2) 
                      for p1, p2 in zip(self.parameters, other.parameters))
        return False
    
    def to_string(self) -> str:
        params = ", ".join(p.to_string() for p in self.parameters)
        return f"{self.base.to_string()}[{params}]"

class UnionType(Type):
    def __init__(self, types: List[Type]):
        self.types = types
    
    def is_assignable_to(self, other: Type) -> bool:
        if isinstance(other, UnionType):
            return all(any(t1.is_assignable_to(t2) for t2 in other.types) 
                      for t1 in self.types)
        return all(t.is_assignable_to(other) for t in self.types)
    
    def to_string(self) -> str:
        return " OR ".join(t.to_string() for t in self.types)

class FunctionType(Type):
    def __init__(self, parameters: List[Type], return_type: Type):
        self.parameters = parameters
        self.return_type = return_type
    
    def is_assignable_to(self, other: Type) -> bool:
        if isinstance(other, FunctionType):
            # Contravariant in parameters, covariant in return type
            if len(self.parameters) != len(other.parameters):
                return False
            
            # Parameters are contravariant
            params_compatible = all(
                other_param.is_assignable_to(self_param)
                for self_param, other_param in zip(self.parameters, other.parameters)
            )
            
            # Return type is covariant
            return_compatible = self.return_type.is_assignable_to(other.return_type)
            
            return params_compatible and return_compatible
        return False
    
    def to_string(self) -> str:
        params = ", ".join(p.to_string() for p in self.parameters)
        return f"Function[{params}, {self.return_type.to_string()}]"

# Type inference engine
class TypeInferenceEngine:
    def __init__(self):
        self.constraints: List['TypeConstraint'] = []
        self.type_variables: Dict[str, Type] = {}
    
    def infer_expression_type(self, expr: Expression, 
                            symbol_table: SymbolTable) -> Type:
        """Infer the type of an expression"""
        if isinstance(expr, LiteralExpression):
            return self._infer_literal_type(expr)
        elif isinstance(expr, IdentifierExpression):
            return self._infer_identifier_type(expr, symbol_table)
        elif isinstance(expr, BinaryExpression):
            return self._infer_binary_expression_type(expr, symbol_table)
        elif isinstance(expr, FunctionCall):
            return self._infer_function_call_type(expr, symbol_table)
        else:
            raise TypeError(f"Cannot infer type for expression: {type(expr)}")
    
    def _infer_literal_type(self, expr: LiteralExpression) -> Type:
        """Infer type from literal values"""
        type_map = {
            "integer": BasicType("Integer"),
            "float": BasicType("Float"),
            "string": BasicType("String"),
            "boolean": BasicType("Boolean"),
            "null": BasicType("None")
        }
        return type_map[expr.literal_type]
    
    def _infer_binary_expression_type(self, expr: BinaryExpression, 
                                    symbol_table: SymbolTable) -> Type:
        """Infer type of binary expressions"""
        left_type = self.infer_expression_type(expr.left, symbol_table)
        right_type = self.infer_expression_type(expr.right, symbol_table)
        
        # Type rules for different operators
        if expr.operator in ["plus", "minus", "multiplied by", "divided by"]:
            if (left_type.is_assignable_to(BasicType("Integer")) and
                right_type.is_assignable_to(BasicType("Integer"))):
                return BasicType("Integer")
            elif (left_type.is_assignable_to(BasicType("Float")) or
                  right_type.is_assignable_to(BasicType("Float"))):
                return BasicType("Float")
        
        elif expr.operator in ["is equal to", "is not equal to", 
                             "is greater than", "is less than"]:
            return BasicType("Boolean")
        
        elif expr.operator == "joined with":
            return BasicType("String")
        
        raise TypeError(f"Invalid types for operator {expr.operator}: "
                       f"{left_type.to_string()} and {right_type.to_string()}")
```

### Semantic Analyzer

```python
class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.type_inference = TypeInferenceEngine()
        self.errors: List[str] = []
    
    def analyze(self, nodes: List[Union[Declaration, Statement]]) -> bool:
        """Perform semantic analysis on AST nodes"""
        # First pass: collect all declarations
        for node in nodes:
            if isinstance(node, Declaration):
                self._collect_declaration(node)
        
        # Second pass: analyze all nodes
        for node in nodes:
            self._analyze_node(node)
        
        return len(self.errors) == 0
    
    def _analyze_node(self, node: ASTNode):
        """Analyze individual AST nodes"""
        if isinstance(node, LetStatement):
            self._analyze_let_statement(node)
        elif isinstance(node, SetStatement):
            self._analyze_set_statement(node)
        elif isinstance(node, FunctionDefinition):
            self._analyze_function_definition(node)
        elif isinstance(node, IfStatement):
            self._analyze_if_statement(node)
        elif isinstance(node, Expression):
            self._analyze_expression(node)
        # ... handle other node types
    
    def _analyze_let_statement(self, stmt: LetStatement):
        """Analyze let statements"""
        # Infer type from value
        value_type = self.type_inference.infer_expression_type(
            stmt.value, self.current_scope)
        
        # Check type annotation if present
        if stmt.type_annotation:
            declared_type = self._resolve_type_expression(stmt.type_annotation)
            if not value_type.is_assignable_to(declared_type):
                self.errors.append(
                    f"Type mismatch at line {stmt.line}: "
                    f"Cannot assign {value_type.to_string()} to "
                    f"{declared_type.to_string()}")
                return
            value_type = declared_type
        
        # Define symbol
        if isinstance(stmt.pattern, IdentifierPattern):
            symbol = Symbol(
                name=stmt.pattern.name,
                symbol_type=SymbolType.VARIABLE,
                data_type=value_type,
                value=None,
                is_mutable=True,
                is_exported=False,
                definition_location=(stmt.line, stmt.column)
            )
            
            if not self.current_scope.define(symbol):
                self.errors.append(
                    f"Symbol '{stmt.pattern.name}' already defined at line {stmt.line}")
    
    def _analyze_function_definition(self, func: FunctionDefinition):
        """Analyze function definitions"""
        # Create new scope for function
        func_scope = self.current_scope.create_child_scope()
        old_scope = self.current_scope
        self.current_scope = func_scope
        
        try:
            # Add parameters to scope
            param_types = []
            for param in func.parameters:
                param_type = self._resolve_type_expression(param.type_annotation) \
                    if param.type_annotation else BasicType("Any")
                param_types.append(param_type)
                
                symbol = Symbol(
                    name=param.name,
                    symbol_type=SymbolType.VARIABLE,
                    data_type=param_type,
                    value=None,
                    is_mutable=True,
                    is_exported=False,
                    definition_location=(func.line, func.column)
                )
                self.current_scope.define(symbol)
            
            # Analyze function body
            for stmt in func.body:
                self._analyze_node(stmt)
            
            # Create function type
            return_type = self._resolve_type_expression(func.return_type) \
                if func.return_type else BasicType("Void")
            func_type = FunctionType(param_types, return_type)
            
            # Add function to parent scope
            func_symbol = Symbol(
                name=func.name,
                symbol_type=SymbolType.FUNCTION,
                data_type=func_type,
                value=None,
                is_mutable=False,
                is_exported=False,
                definition_location=(func.line, func.column)
            )
            old_scope.define(func_symbol)
            
        finally:
            self.current_scope = old_scope
```

## Phase 4: Code Generation

### Multi-Target Code Generator

```python
from abc import ABC, abstractmethod

class CodeGenerator(ABC):
    """Base class for target language code generators"""
    
    @abstractmethod
    def generate_program(self, nodes: List[ASTNode]) -> str:
        pass
    
    @abstractmethod
    def generate_expression(self, expr: Expression) -> str:
        pass
    
    @abstractmethod
    def generate_statement(self, stmt: Statement) -> str:
        pass

class PythonCodeGenerator(CodeGenerator):
    def __init__(self):
        self.indent_level = 0
        self.output = []
    
    def generate_program(self, nodes: List[ASTNode]) -> str:
        """Generate complete Python program"""
        self.output = []
        
        # Add imports
        self.output.append("# Generated by Runa compiler")
        self.output.append("from typing import *")
        self.output.append("from runa_runtime import *")
        self.output.append("")
        
        # Generate all nodes
        for node in nodes:
            if isinstance(node, Declaration):
                self.output.append(self.generate_declaration(node))
            elif isinstance(node, Statement):
                self.output.append(self.generate_statement(node))
            self.output.append("")
        
        return "\n".join(self.output)
    
    def generate_expression(self, expr: Expression) -> str:
        """Generate Python expression"""
        if isinstance(expr, LiteralExpression):
            return self._generate_literal(expr)
        elif isinstance(expr, IdentifierExpression):
            return self._generate_identifier(expr)
        elif isinstance(expr, BinaryExpression):
            return self._generate_binary_expression(expr)
        elif isinstance(expr, FunctionCall):
            return self._generate_function_call(expr)
        else:
            raise CodeGenError(f"Unsupported expression type: {type(expr)}")
    
    def _generate_literal(self, expr: LiteralExpression) -> str:
        """Generate Python literals"""
        if expr.literal_type == "string":
            return f'"{expr.value}"'
        elif expr.literal_type == "integer":
            return str(expr.value)
        elif expr.literal_type == "float":
            return str(expr.value)
        elif expr.literal_type == "boolean":
            return "True" if expr.value else "False"
        elif expr.literal_type == "null":
            return "None"
        else:
            raise CodeGenError(f"Unknown literal type: {expr.literal_type}")
    
    def _generate_identifier(self, expr: IdentifierExpression) -> str:
        """Generate Python identifier"""
        if expr.is_multi_word:
            # Convert multi-word identifier to snake_case
            return expr.name.lower().replace(" ", "_")
        return expr.name
    
    def _generate_binary_expression(self, expr: BinaryExpression) -> str:
        """Generate Python binary expressions"""
        left = self.generate_expression(expr.left)
        right = self.generate_expression(expr.right)
        
        # Map Runa Canon Mode operators to Python operators
        operator_map = {
            # Arithmetic operators (Canon Mode)
            "plus": "+",
            "minus": "-",
            "multiplied by": "*",
            "divided by": "/",
            "modulo": "%",
            "modulo by": "%",
            "to the power of": "**",

            # Comparison operators (Canon Mode)
            "is equal to": "==",
            "is not equal to": "!=",
            "is greater than": ">",
            "is less than": "<",
            "is greater than or equal to": ">=",
            "is less than or equal to": "<=",

            # Logical operators
            "and": "and",
            "or": "or",
            "not": "not",

            # String operators
            "joined with": "+"
        }
        
        python_op = operator_map.get(expr.operator)
        if python_op:
            return f"({left} {python_op} {right})"
        else:
            raise CodeGenError(f"Unsupported operator: {expr.operator}")
    
    def generate_statement(self, stmt: Statement) -> str:
        """Generate Python statement"""
        if isinstance(stmt, LetStatement):
            return self._generate_let_statement(stmt)
        elif isinstance(stmt, SetStatement):
            return self._generate_set_statement(stmt)
        elif isinstance(stmt, IfStatement):
            return self._generate_if_statement(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self._generate_return_statement(stmt)
        else:
            raise CodeGenError(f"Unsupported statement type: {type(stmt)}")
    
    def _generate_let_statement(self, stmt: LetStatement) -> str:
        """Generate Python variable declaration"""
        if isinstance(stmt.pattern, IdentifierPattern):
            var_name = self._generate_identifier(
                IdentifierExpression(stmt.pattern.name, False, 0, 0))
            value = self.generate_expression(stmt.value)
            return f"{self._indent()}{var_name} = {value}"
        else:
            raise CodeGenError("Only identifier patterns supported currently")
    
    def _generate_if_statement(self, stmt: IfStatement) -> str:
        """Generate Python if statement"""
        condition = self.generate_expression(stmt.condition)
        result = [f"{self._indent()}if {condition}:"]
        
        self.indent_level += 1
        for s in stmt.then_block:
            result.append(self.generate_statement(s))
        self.indent_level -= 1
        
        for elif_clause in stmt.elif_clauses:
            elif_condition = self.generate_expression(elif_clause.condition)
            result.append(f"{self._indent()}elif {elif_condition}:")
            self.indent_level += 1
            for s in elif_clause.block:
                result.append(self.generate_statement(s))
            self.indent_level -= 1
        
        if stmt.else_block:
            result.append(f"{self._indent()}else:")
            self.indent_level += 1
            for s in stmt.else_block:
                result.append(self.generate_statement(s))
            self.indent_level -= 1
        
        return "\n".join(result)
    
    def _indent(self) -> str:
        """Generate indentation"""
        return "    " * self.indent_level

class JavaScriptCodeGenerator(CodeGenerator):
    """JavaScript code generator"""
    
    def generate_program(self, nodes: List[ASTNode]) -> str:
        """Generate JavaScript program"""
        output = []
        
        # Add header
        output.append("// Generated by Runa compiler")
        output.append("const { RunaRuntime } = require('runa-runtime');")
        output.append("")
        
        # Generate nodes
        for node in nodes:
            if isinstance(node, FunctionDefinition):
                output.append(self._generate_js_function(node))
            # ... handle other nodes
        
        return "\n".join(output)
    
    def _generate_js_function(self, func: FunctionDefinition) -> str:
        """Generate JavaScript function"""
        params = ", ".join(p.name for p in func.parameters)
        
        if func.is_async:
            result = [f"async function {func.name}({params}) {{"]
        else:
            result = [f"function {func.name}({params}) {{"]
        
        # Generate body
        for stmt in func.body:
            result.append(f"    {self.generate_statement(stmt)}")
        
        result.append("}")
        return "\n".join(result)
    
    def generate_expression(self, expr: Expression) -> str:
        """Generate JavaScript expression"""
        if isinstance(expr, BinaryExpression):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            
            # JavaScript operator mapping
            js_operators = {
                "plus": "+",
                "minus": "-",
                "multiplied by": "*",
                "divided by": "/",
                "is equal to": "===",
                "joined with": "+"
            }
            
            op = js_operators.get(expr.operator, expr.operator)
            return f"({left} {op} {right})"
        
        # ... handle other expressions
        return str(expr)
    
    def generate_statement(self, stmt: Statement) -> str:
        """Generate JavaScript statement"""
        if isinstance(stmt, LetStatement):
            pattern = stmt.pattern
            if isinstance(pattern, IdentifierPattern):
                value = self.generate_expression(stmt.value)
                return f"let {pattern.name} = {value};"
        
        # ... handle other statements
        return str(stmt)
```

## Phase 5: Runtime Library

### Core Runtime Support

```python
# runa_runtime.py - Runtime support for generated code

from typing import Any, Dict, List, Optional, Union, Callable
import asyncio
import json

class RunaRuntime:
    """Core runtime support for Runa programs"""
    
    @staticmethod
    def runa_display(*args, **kwargs):
        """Implementation of Runa's Display statement"""
        message = kwargs.get('message', '')
        if args:
            if message:
                print(*args, message)
            else:
                print(*args)
        elif message:
            print(message)
    
    @staticmethod
    def runa_input(prompt: str = "") -> str:
        """Implementation of Runa's input function"""
        return input(prompt)
    
    @staticmethod
    def runa_length(obj: Any) -> int:
        """Implementation of Runa's length function"""
        if hasattr(obj, '__len__'):
            return len(obj)
        else:
            raise TypeError(f"Object of type {type(obj)} has no length")
    
    @staticmethod
    def runa_list_containing(*items) -> List[Any]:
        """Implementation of 'list containing' syntax"""
        return list(items)
    
    @staticmethod
    def runa_dictionary_with(**kwargs) -> Dict[str, Any]:
        """Implementation of 'dictionary with' syntax"""
        return dict(kwargs)
    
    @staticmethod
    def runa_add_to(container: List[Any], item: Any) -> None:
        """Implementation of 'Add X to Y' syntax"""
        container.append(item)
    
    @staticmethod
    def runa_map(items: List[Any], func: Callable) -> List[Any]:
        """Implementation of Map function"""
        return [func(item) for item in items]
    
    @staticmethod
    def runa_filter(items: List[Any], predicate: Callable) -> List[Any]:
        """Implementation of Filter function"""
        return [item for item in items if predicate(item)]
    
    @staticmethod
    def runa_reduce(items: List[Any], func: Callable, initial: Any = None) -> Any:
        """Implementation of Reduce function"""
        from functools import reduce
        if initial is not None:
            return reduce(func, items, initial)
        else:
            return reduce(func, items)

# Type system support
class RunaType:
    """Base class for Runa runtime types"""
    pass

class RunaOptional(RunaType):
    """Runtime representation of Optional types"""
    def __init__(self, value: Any):
        self.value = value
    
    def is_some(self) -> bool:
        return self.value is not None
    
    def is_none(self) -> bool:
        return self.value is None
    
    def unwrap(self) -> Any:
        if self.value is None:
            raise RuntimeError("Cannot unwrap None value")
        return self.value

# Pattern matching support
class RunaPatternMatcher:
    """Runtime support for pattern matching"""
    
    @staticmethod
    def match_literal(value: Any, pattern: Any) -> bool:
        """Match literal patterns"""
        return value == pattern
    
    @staticmethod
    def match_list(value: List[Any], patterns: List[Any]) -> Optional[Dict[str, Any]]:
        """Match list patterns"""
        if not isinstance(value, list):
            return None
        
        if len(value) != len(patterns):
            return None
        
        bindings = {}
        for i, (v, p) in enumerate(zip(value, patterns)):
            if isinstance(p, str) and p.startswith('_'):
                bindings[p[1:]] = v  # Bind variable
            elif v != p:
                return None
        
        return bindings
    
    @staticmethod
    def match_dict(value: Dict[str, Any], pattern: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Match dictionary patterns"""
        if not isinstance(value, dict):
            return None
        
        bindings = {}
        for key, pattern_value in pattern.items():
            if key not in value:
                return None
            
            if isinstance(pattern_value, str) and pattern_value.startswith('_'):
                bindings[pattern_value[1:]] = value[key]
            elif value[key] != pattern_value:
                return None
        
        return bindings

# Async support
class RunaAsyncRuntime:
    """Async runtime support"""
    
    @staticmethod
    async def runa_spawn(func: Callable, *args, **kwargs):
        """Spawn an async task"""
        return asyncio.create_task(func(*args, **kwargs))
    
    @staticmethod
    async def runa_await(awaitable):
        """Await an async operation"""
        return await awaitable
    
    @staticmethod
    def runa_run_async(func: Callable, *args, **kwargs):
        """Run an async function"""
        return asyncio.run(func(*args, **kwargs))

# Error handling support
class RunaError(Exception):
    """Base class for Runa runtime errors"""
    pass

class RunaTypeError(RunaError):
    """Runa type error"""
    pass

class RunaValueError(RunaError):
    """Runa value error"""
    pass

# Export all runtime components
__all__ = [
    'RunaRuntime', 'RunaType', 'RunaOptional', 'RunaPatternMatcher',
    'RunaAsyncRuntime', 'RunaError', 'RunaTypeError', 'RunaValueError'
]
```

## Phase 6: Development Tools

### Language Server Protocol Implementation

```python
# runa_lsp.py - Language Server Protocol implementation

import json
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class Position:
    line: int
    character: int

@dataclass
class Range:
    start: Position
    end: Position

@dataclass
class Diagnostic:
    range: Range
    message: str
    severity: int  # 1=Error, 2=Warning, 3=Info, 4=Hint
    source: str = "runa"

class RunaLanguageServer:
    """Language Server Protocol implementation for Runa"""
    
    def __init__(self):
        self.documents: Dict[str, str] = {}
        self.lexer = RunaLexer("")
        self.parser = RunaParser([])
        self.analyzer = SemanticAnalyzer()
    
    def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "capabilities": {
                "textDocumentSync": 1,  # Full sync
                "completionProvider": {
                    "triggerCharacters": [" ", "."]
                },
                "hoverProvider": True,
                "definitionProvider": True,
                "diagnosticsProvider": True,
                "documentFormattingProvider": True,
                "renameProvider": True
            }
        }
    
    def did_open(self, params: Dict[str, Any]):
        """Handle document open"""
        uri = params["textDocument"]["uri"]
        text = params["textDocument"]["text"]
        self.documents[uri] = text
        self._validate_document(uri)
    
    def did_change(self, params: Dict[str, Any]):
        """Handle document change"""
        uri = params["textDocument"]["uri"]
        changes = params["contentChanges"]
        
        # Apply changes (assuming full sync for simplicity)
        if changes:
            self.documents[uri] = changes[0]["text"]
        
        self._validate_document(uri)
    
    def _validate_document(self, uri: str):
        """Validate document and send diagnostics"""
        text = self.documents[uri]
        diagnostics = []
        
        try:
            # Tokenize
            self.lexer = RunaLexer(text)
            tokens = self.lexer.tokenize()
            
            # Parse
            self.parser = RunaParser(tokens)
            ast = self.parser.parse()
            
            # Semantic analysis
            self.analyzer = SemanticAnalyzer()
            success = self.analyzer.analyze(ast)
            
            if not success:
                for error in self.analyzer.errors:
                    # Parse error message for location
                    # This is simplified - real implementation would track locations
                    diagnostic = Diagnostic(
                        range=Range(Position(0, 0), Position(0, 10)),
                        message=error,
                        severity=1
                    )
                    diagnostics.append(diagnostic)
        
        except Exception as e:
            diagnostic = Diagnostic(
                range=Range(Position(0, 0), Position(0, 10)),
                message=str(e),
                severity=1
            )
            diagnostics.append(diagnostic)
        
        # Send diagnostics
        self._send_diagnostics(uri, diagnostics)
    
    def completion(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle completion request"""
        uri = params["textDocument"]["uri"]
        position = params["position"]
        
        # Get completion items based on context
        completions = []
        
        # Add keyword completions
        keywords = ["Let", "Define", "Set", "If", "Otherwise", "Process", "Type"]
        for keyword in keywords:
            completions.append({
                "label": keyword,
                "kind": 14,  # Keyword
                "detail": f"Runa keyword: {keyword}"
            })
        
        # Add function completions based on scope
        # This would be more sophisticated in a real implementation
        
        return {"items": completions}
    
    def hover(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle hover request"""
        uri = params["textDocument"]["uri"]
        position = params["position"]
        
        # Find symbol at position and provide hover info
        # This is simplified - real implementation would use AST
        
        return {
            "contents": {
                "kind": "markdown",
                "value": "Runa identifier or expression"
            }
        }
    
    def formatting(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle document formatting"""
        uri = params["textDocument"]["uri"]
        text = self.documents[uri]
        
        # Format the document
        formatted = self._format_code(text)
        
        # Return text edit to replace entire document
        return [{
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": text.count('\n'), "character": 0}
            },
            "newText": formatted
        }]
    
    def _format_code(self, text: str) -> str:
        """Format Runa code"""
        try:
            lexer = RunaLexer(text)
            tokens = lexer.tokenize()
            formatter = RunaFormatter()
            return formatter.format(tokens)
        except:
            return text  # Return original on error
    
    def _send_diagnostics(self, uri: str, diagnostics: List[Diagnostic]):
        """Send diagnostics to client"""
        # Convert diagnostics to LSP format
        lsp_diagnostics = []
        for diag in diagnostics:
            lsp_diagnostics.append({
                "range": {
                    "start": {"line": diag.range.start.line, "character": diag.range.start.character},
                    "end": {"line": diag.range.end.line, "character": diag.range.end.character}
                },
                "message": diag.message,
                "severity": diag.severity,
                "source": diag.source
            })
        
        # Send notification (simplified - real implementation would use JSON-RPC)
        notification = {
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": lsp_diagnostics
            }
        }
        print(json.dumps(notification))

class RunaFormatter:
    """Code formatter for Runa"""
    
    def format(self, tokens: List[Token]) -> str:
        """Format tokens into well-formatted code"""
        output = []
        indent_level = 0
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == TokenType.INDENT:
                indent_level += 1
            elif token.type == TokenType.DEDENT:
                indent_level -= 1
            elif token.type == TokenType.NEWLINE:
                output.append('\n')
                # Add indentation for next line
                if i + 1 < len(tokens) and tokens[i + 1].type not in [TokenType.DEDENT, TokenType.EOF]:
                    output.append('    ' * indent_level)
            elif token.type == TokenType.COLON:
                output.append(':')
                # Add space after colon if not followed by newline
                if i + 1 < len(tokens) and tokens[i + 1].type != TokenType.NEWLINE:
                    output.append(' ')
            else:
                output.append(str(token.value))
                # Add space after token if needed
                if (i + 1 < len(tokens) and 
                    tokens[i + 1].type not in [TokenType.COLON, TokenType.NEWLINE, TokenType.COMMA]):
                    output.append(' ')
            
            i += 1
        
        return ''.join(output)
```

## Implementation Best Practices

### 1. Error Handling Strategy

```python
class RunaCompilerError(Exception):
    """Base class for compiler errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"{message} at line {line}, column {column}")

class LexError(RunaCompilerError):
    """Lexical analysis error"""
    pass

class ParseError(RunaCompilerError):
    """Parse error"""
    pass

class SemanticError(RunaCompilerError):
    """Semantic analysis error"""
    pass

class CodeGenError(RunaCompilerError):
    """Code generation error"""
    pass
```

### 2. Testing Framework

```python
import unittest
from typing import List

class RunaCompilerTests(unittest.TestCase):
    """Test suite for Runa compiler"""
    
    def setUp(self):
        self.lexer = RunaLexer("")
        self.parser = RunaParser([])
        self.analyzer = SemanticAnalyzer()
    
    def test_basic_lexing(self):
        """Test basic tokenization"""
        code = 'Let x be 42'
        self.lexer = RunaLexer(code)
        tokens = self.lexer.tokenize()
        
        expected_types = [TokenType.LET, TokenType.IDENTIFIER, 
                         TokenType.BE, TokenType.INTEGER, TokenType.EOF]
        actual_types = [token.type for token in tokens]
        
        self.assertEqual(expected_types, actual_types)
    
    def test_multi_word_operators(self):
        """Test multi-word operator recognition"""
        code = 'If x is greater than 5:'
        self.lexer = RunaLexer(code)
        tokens = self.lexer.tokenize()
        
        self.assertIn(TokenType.IS_GREATER_THAN, [t.type for t in tokens])
    
    def test_function_parsing(self):
        """Test function definition parsing"""
        code = '''
Process called "add" that takes a as Integer and b as Integer returns Integer:
    Return a plus b
End Process
'''
        self.lexer = RunaLexer(code)
        tokens = self.lexer.tokenize()
        self.parser = RunaParser(tokens)
        ast = self.parser.parse()
        
        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], FunctionDefinition)
        self.assertEqual(ast[0].name, "add")
    
    def test_type_checking(self):
        """Test type checking"""
        code = '''
Let x be 42
Let y be "hello"
Set x to y
'''
        # This should produce a type error
        success = self._compile_and_analyze(code)
        self.assertFalse(success)
        self.assertTrue(len(self.analyzer.errors) > 0)
    
    def _compile_and_analyze(self, code: str) -> bool:
        """Helper method to compile and analyze code"""
        try:
            self.lexer = RunaLexer(code)
            tokens = self.lexer.tokenize()
            self.parser = RunaParser(tokens)
            ast = self.parser.parse()
            self.analyzer = SemanticAnalyzer()
            return self.analyzer.analyze(ast)
        except Exception:
            return False

if __name__ == '__main__':
    unittest.main()
```

### 3. Performance Optimization

```python
class CompilerOptimizations:
    """Optimization passes for the compiler"""
    
    @staticmethod
    def dead_code_elimination(ast: List[ASTNode]) -> List[ASTNode]:
        """Remove unreachable code"""
        # Implementation for dead code elimination
        pass
    
    @staticmethod
    def constant_folding(ast: List[ASTNode]) -> List[ASTNode]:
        """Fold constant expressions at compile time"""
        # Implementation for constant folding
        pass
    
    @staticmethod
    def inline_functions(ast: List[ASTNode]) -> List[ASTNode]:
        """Inline small functions"""
        # Implementation for function inlining
        pass
```

## Phase 7: Advanced Compiler Implementation

### Code Generation Strategies

#### Multi-Target Code Generation

```python
class TargetLanguageRegistry:
    """Registry for target language code generators"""
    
    def __init__(self):
        self.generators = {}
        self.target_configs = {}
    
    def register_target(self, language: str, generator_class: type, config: dict):
        """Register a new target language"""
        self.generators[language] = generator_class
        self.target_configs[language] = config
    
    def generate_code(self, ast: List[ASTNode], target: str) -> str:
        """Generate code for specified target language"""
        if target not in self.generators:
            raise UnsupportedTargetError(f"Target {target} not supported")
        
        generator = self.generators[target]()
        return generator.generate_program(ast)

# Target-specific optimizations
class TargetSpecificOptimizations:
    
    @staticmethod
    def optimize_for_python(ast: List[ASTNode]) -> List[ASTNode]:
        """Python-specific optimizations"""
        # List comprehension optimization
        # Dictionary comprehension optimization
        # Generator expression optimization
        return ast
    
    @staticmethod
    def optimize_for_javascript(ast: List[ASTNode]) -> List[ASTNode]:
        """JavaScript-specific optimizations"""
        # Prototype chain optimization
        # Closure optimization
        # Promise/async optimization
        return ast
    
    @staticmethod
    def optimize_for_cpp(ast: List[ASTNode]) -> List[ASTNode]:
        """C++ specific optimizations"""
        # RAII optimization
        # Template instantiation optimization
        # Move semantics optimization
        return ast
```

#### Template-Based Code Generation

```python
class TemplateCodeGenerator:
    """Template-based code generation system"""
    
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.templates = {}
        self.load_templates()
    
    def load_templates(self):
        """Load code generation templates"""
        for target in ["python", "javascript", "java", "cpp"]:
            template_path = f"{self.template_dir}/{target}"
            self.templates[target] = self.load_target_templates(template_path)
    
    def generate_function(self, func: FunctionDefinition, target: str) -> str:
        """Generate function code using templates"""
        template = self.templates[target]["function"]
        
        context = {
            "name": func.name,
            "parameters": self.format_parameters(func.parameters, target),
            "return_type": self.format_type(func.return_type, target),
            "body": self.generate_statements(func.body, target),
            "is_async": func.is_async
        }
        
        return template.render(context)
    
    def generate_type_definition(self, type_def: TypeDefinition, target: str) -> str:
        """Generate type definition using templates"""
        if isinstance(type_def.definition, RecordDefinition):
            template = self.templates[target]["class"]
        elif isinstance(type_def.definition, ADTDefinition):
            template = self.templates[target]["enum"]
        else:
            template = self.templates[target]["typedef"]
        
        context = {
            "name": type_def.name,
            "fields": self.format_fields(type_def.definition, target),
            "methods": self.format_methods(type_def.definition, target)
        }
        
        return template.render(context)
```

### Optimization Passes and Techniques

#### Control Flow Analysis

```python
class ControlFlowAnalyzer:
    """Analyze control flow for optimization"""
    
    def __init__(self):
        self.basic_blocks = []
        self.cfg = {}  # Control Flow Graph
    
    def analyze_function(self, func: FunctionDefinition) -> 'ControlFlowGraph':
        """Build control flow graph for function"""
        self.basic_blocks = self.identify_basic_blocks(func.body)
        self.cfg = self.build_cfg(self.basic_blocks)
        return ControlFlowGraph(self.basic_blocks, self.cfg)
    
    def identify_basic_blocks(self, statements: List[Statement]) -> List['BasicBlock']:
        """Identify basic blocks in statement list"""
        blocks = []
        current_block = []
        
        for stmt in statements:
            current_block.append(stmt)
            
            # Block ends at control flow statements
            if isinstance(stmt, (ReturnStatement, BreakStatement, 
                               ContinueStatement, ThrowStatement)):
                blocks.append(BasicBlock(current_block))
                current_block = []
            elif isinstance(stmt, (IfStatement, MatchStatement, 
                                 ForLoop, WhileLoop)):
                blocks.append(BasicBlock(current_block))
                current_block = []
                # Recursively analyze nested blocks
                for nested_block in self.get_nested_blocks(stmt):
                    blocks.extend(self.identify_basic_blocks(nested_block))
        
        if current_block:
            blocks.append(BasicBlock(current_block))
        
        return blocks
    
    def optimize_control_flow(self, cfg: 'ControlFlowGraph') -> 'ControlFlowGraph':
        """Optimize control flow graph"""
        # Dead code elimination
        cfg = self.eliminate_dead_blocks(cfg)
        
        # Branch optimization
        cfg = self.optimize_branches(cfg)
        
        # Loop optimization
        cfg = self.optimize_loops(cfg)
        
        return cfg

class DataFlowAnalyzer:
    """Analyze data flow for optimization"""
    
    def __init__(self):
        self.def_use_chains = {}
        self.live_variables = {}
    
    def analyze_reaching_definitions(self, cfg: 'ControlFlowGraph'):
        """Analyze reaching definitions"""
        # Implement reaching definitions analysis
        pass
    
    def analyze_live_variables(self, cfg: 'ControlFlowGraph'):
        """Analyze live variables"""
        # Implement live variable analysis
        pass
    
    def optimize_register_allocation(self, cfg: 'ControlFlowGraph'):
        """Optimize register allocation using graph coloring"""
        # Build interference graph
        # Apply graph coloring algorithm
        # Assign registers/stack slots
        pass
```

#### Advanced Optimizations

```python
class AdvancedOptimizations:
    """Advanced compiler optimizations"""
    
    @staticmethod
    def scalar_replacement_of_aggregates(ast: List[ASTNode]) -> List[ASTNode]:
        """Replace aggregate types with scalars where possible"""
        # Identify aggregates that can be replaced
        # Replace with individual scalar variables
        # Update all references
        return ast
    
    @staticmethod
    def loop_invariant_code_motion(ast: List[ASTNode]) -> List[ASTNode]:
        """Move loop-invariant code outside loops"""
        # Identify loop-invariant expressions
        # Move to loop preheader
        # Update variable definitions
        return ast
    
    @staticmethod
    def function_inlining(ast: List[ASTNode]) -> List[ASTNode]:
        """Inline small functions at call sites"""
        # Identify candidates for inlining
        # Perform inlining transformation
        # Update variable scoping
        return ast
    
    @staticmethod
    def tail_call_optimization(ast: List[ASTNode]) -> List[ASTNode]:
        """Optimize tail calls to iterations"""
        # Identify tail recursive calls
        # Transform to iterative form
        # Eliminate stack frame allocation
        return ast
    
    @staticmethod
    def devirtualization(ast: List[ASTNode]) -> List[ASTNode]:
        """Replace virtual calls with direct calls where possible"""
        # Analyze type hierarchy
        # Identify monomorphic call sites
        # Replace with direct calls
        return ast
```

### Error Reporting Mechanisms

#### Diagnostic System

```python
@dataclass
class Diagnostic:
    """Compiler diagnostic message"""
    level: DiagnosticLevel  # Error, Warning, Info, Hint
    message: str
    location: SourceLocation
    code: str  # Error code (e.g., "E001")
    suggestions: List[str]
    related_diagnostics: List['Diagnostic']

class DiagnosticEngine:
    """Engine for collecting and reporting diagnostics"""
    
    def __init__(self):
        self.diagnostics = []
        self.error_count = 0
        self.warning_count = 0
        self.max_errors = 100
    
    def report_error(self, message: str, location: SourceLocation, 
                    code: str = "", suggestions: List[str] = None):
        """Report a compilation error"""
        diag = Diagnostic(
            level=DiagnosticLevel.ERROR,
            message=message,
            location=location,
            code=code,
            suggestions=suggestions or [],
            related_diagnostics=[]
        )
        
        self.diagnostics.append(diag)
        self.error_count += 1
        
        if self.error_count >= self.max_errors:
            raise TooManyErrorsException()
    
    def report_warning(self, message: str, location: SourceLocation, 
                      code: str = "", suggestions: List[str] = None):
        """Report a compilation warning"""
        diag = Diagnostic(
            level=DiagnosticLevel.WARNING,
            message=message,
            location=location,
            code=code,
            suggestions=suggestions or [],
            related_diagnostics=[]
        )
        
        self.diagnostics.append(diag)
        self.warning_count += 1
    
    def format_diagnostics(self) -> str:
        """Format diagnostics for display"""
        output = []
        
        for diag in self.diagnostics:
            # Format diagnostic with source context
            formatted = self.format_diagnostic(diag)
            output.append(formatted)
        
        # Add summary
        output.append(f"\n{self.error_count} errors, {self.warning_count} warnings")
        
        return "\n".join(output)
    
    def format_diagnostic(self, diag: Diagnostic) -> str:
        """Format a single diagnostic"""
        # Load source file and extract relevant lines
        source_lines = self.load_source_context(diag.location)
        
        lines = []
        
        # Header with file:line:column
        header = f"{diag.location.file}:{diag.location.line}:{diag.location.column}"
        level_str = diag.level.name.lower()
        lines.append(f"{header}: {level_str}: {diag.message}")
        
        if diag.code:
            lines[-1] += f" [{diag.code}]"
        
        # Source context
        lines.extend(self.format_source_context(source_lines, diag.location))
        
        # Suggestions
        for suggestion in diag.suggestions:
            lines.append(f"  help: {suggestion}")
        
        return "\n".join(lines)
    
    def format_source_context(self, source_lines: List[str], 
                            location: SourceLocation) -> List[str]:
        """Format source code context with highlighting"""
        lines = []
        
        # Show 2 lines before and after
        start_line = max(0, location.line - 3)
        end_line = min(len(source_lines), location.line + 2)
        
        for i in range(start_line, end_line):
            line_num = i + 1
            source_line = source_lines[i]
            
            # Line number and source
            lines.append(f"{line_num:4} | {source_line}")
            
            # Highlight error location
            if line_num == location.line:
                pointer = " " * (6 + location.column) + "^"
                if location.length > 1:
                    pointer += "~" * (location.length - 1)
                lines.append(pointer)
        
        return lines
```

### Build System Integration

#### Build Configuration

```python
class BuildConfig:
    """Build configuration for Runa projects"""
    
    def __init__(self, config_file: str):
        self.config = self.load_config(config_file)
        self.validate_config()
    
    def load_config(self, config_file: str) -> dict:
        """Load build configuration from file"""
        # Support multiple formats: TOML, JSON, YAML
        if config_file.endswith('.toml'):
            return self.load_toml(config_file)
        elif config_file.endswith('.json'):
            return self.load_json(config_file)
        elif config_file.endswith('.yaml'):
            return self.load_yaml(config_file)
        else:
            raise UnsupportedConfigError(f"Unsupported config format: {config_file}")

# Example runa.toml
"""
[package]
name = "my-runa-project"
version = "1.0.0"
authors = ["Developer <dev@example.com>"]
description = "A Runa project"

[build]
target_language = "python"
optimization_level = 2
debug = false
output_dir = "build/"

[targets]
python = { version = "3.9", stdlib = "full" }
javascript = { version = "es2020", runtime = "node" }
java = { version = "11", framework = "spring" }

[dependencies]
http = "1.0"
json = "2.1"
math = { version = "3.0", features = ["statistics"] }

[dev-dependencies]
testing = "1.5"
profiling = "0.8"

[scripts]
build = "runa build --release"
test = "runa test --verbose"
deploy = ["runa build --release", "runa deploy --target production"]
"""

class BuildSystem:
    """Integrated build system for Runa projects"""
    
    def __init__(self, config: BuildConfig):
        self.config = config
        self.dependency_resolver = DependencyResolver()
        self.compiler = RunaCompiler()
    
    def build_project(self) -> BuildResult:
        """Build the entire project"""
        try:
            # Resolve dependencies
            dependencies = self.dependency_resolver.resolve(self.config.dependencies)
            
            # Compile source files
            compilation_result = self.compile_sources()
            
            # Link dependencies
            linked_result = self.link_dependencies(compilation_result, dependencies)
            
            # Generate output
            output = self.generate_output(linked_result)
            
            return BuildResult(success=True, output=output)
            
        except BuildError as e:
            return BuildResult(success=False, error=str(e))
    
    def compile_sources(self) -> CompilationResult:
        """Compile all source files"""
        source_files = self.discover_source_files()
        compiled_modules = []
        
        for source_file in source_files:
            try:
                module = self.compiler.compile_file(source_file)
                compiled_modules.append(module)
            except CompilationError as e:
                raise BuildError(f"Failed to compile {source_file}: {e}")
        
        return CompilationResult(modules=compiled_modules)
    
    def incremental_build(self, changed_files: List[str]) -> BuildResult:
        """Perform incremental build for changed files"""
        # Build dependency graph
        dep_graph = self.build_dependency_graph()
        
        # Find files that need recompilation
        files_to_compile = self.find_affected_files(changed_files, dep_graph)
        
        # Compile only affected files
        for file in files_to_compile:
            self.compiler.compile_file(file)
        
        # Update build artifacts
        return self.update_build_artifacts(files_to_compile)
```

## Phase 8: Advanced Language Features

### Metaprogramming and Compile-Time Execution

#### Macro System

```python
class MacroProcessor:
    """Runa macro processing system"""
    
    def __init__(self):
        self.macros = {}
        self.expansion_stack = []
    
    def define_macro(self, name: str, parameters: List[str], 
                    body: List[ASTNode], is_syntax: bool = False):
        """Define a new macro"""
        macro = Macro(name, parameters, body, is_syntax)
        self.macros[name] = macro
    
    def expand_macro(self, call: MacroCall, context: MacroContext) -> List[ASTNode]:
        """Expand a macro call"""
        if call.name not in self.macros:
            raise UndefinedMacroError(f"Macro {call.name} not defined")
        
        # Prevent infinite recursion
        if call.name in self.expansion_stack:
            raise MacroRecursionError(f"Recursive macro expansion: {call.name}")
        
        macro = self.macros[call.name]
        self.expansion_stack.append(call.name)
        
        try:
            # Bind arguments to parameters
            bindings = self.bind_arguments(macro.parameters, call.arguments)
            
            # Expand macro body with substitutions
            expanded = self.substitute_body(macro.body, bindings, context)
            
            return expanded
        finally:
            self.expansion_stack.pop()

# Macro definition syntax in Runa
"""
# Function-like macro
Macro called "assert_not_null" that takes expr:
    If expr is None:
        Throw ValueError with message "Expression cannot be null"

# Syntax macro for custom control structures
Syntax Macro called "unless" that takes condition and body:
    If not condition:
        body

# Compile-time code generation macro
Compile Time Macro called "generate_getters" that takes type_def:
    For each field in type_def.fields:
        Generate Process called f"get_{field.name}" returns field.type:
            Return self.field.name
"""
```

#### Compile-Time Execution

```python
class CompileTimeExecutor:
    """Execute Runa code at compile time"""
    
    def __init__(self):
        self.compile_time_env = CompileTimeEnvironment()
        self.interpreter = RunaInterpreter()
    
    def execute_compile_time_block(self, block: CompileTimeBlock) -> Any:
        """Execute a compile-time code block"""
        # Set up compile-time environment
        old_env = self.interpreter.environment
        self.interpreter.environment = self.compile_time_env
        
        try:
            # Execute the block
            result = self.interpreter.execute_statements(block.statements)
            return result
        finally:
            # Restore runtime environment
            self.interpreter.environment = old_env
    
    def evaluate_compile_time_expression(self, expr: Expression) -> Any:
        """Evaluate an expression at compile time"""
        if isinstance(expr, LiteralExpression):
            return expr.value
        elif isinstance(expr, BinaryExpression):
            left = self.evaluate_compile_time_expression(expr.left)
            right = self.evaluate_compile_time_expression(expr.right)
            return self.apply_operator(expr.operator, left, right)
        # ... handle other expression types
        
    def generate_code_from_template(self, template: CodeTemplate, 
                                  context: dict) -> List[ASTNode]:
        """Generate code from template with context"""
        # Template expansion with variable substitution
        # Type-safe code generation
        # AST node creation
        pass
```

### Reflection and Introspection

```python
class ReflectionSystem:
    """Runtime reflection and introspection"""
    
    def __init__(self):
        self.type_registry = TypeRegistry()
        self.function_registry = FunctionRegistry()
    
    def get_type_info(self, obj: Any) -> TypeInfo:
        """Get type information for an object"""
        obj_type = type(obj)
        return self.type_registry.get_type_info(obj_type)
    
    def get_function_info(self, func: Callable) -> FunctionInfo:
        """Get function metadata"""
        return self.function_registry.get_function_info(func)
    
    def invoke_function(self, func_name: str, args: List[Any], 
                       kwargs: dict = None) -> Any:
        """Dynamically invoke a function by name"""
        func_info = self.function_registry.lookup(func_name)
        if not func_info:
            raise FunctionNotFoundError(f"Function {func_name} not found")
        
        # Type check arguments
        self.validate_arguments(func_info, args, kwargs or {})
        
        # Invoke function
        return func_info.function(*args, **(kwargs or {}))

# Reflection usage in Runa
"""
# Get type information
Let user_type be type of user
Display "Type name: " with message user_type.name
Display "Fields: " with message user_type.fields

# Dynamic function invocation
Let function_name be "calculate_tax"
Let args be list containing income, tax_rate
Let result be invoke function_name with args as args

# Iterate over object fields
For each field in reflect on user:
    Display field.name with message ": " with message field.value
"""
```

### Conditional Compilation

```python
class ConditionalCompiler:
    """Handle conditional compilation directives"""
    
    def __init__(self):
        self.defines = {}
        self.target_features = set()
    
    def set_define(self, name: str, value: Any = True):
        """Set a compilation define"""
        self.defines[name] = value
    
    def process_conditional_block(self, block: ConditionalBlock) -> List[ASTNode]:
        """Process conditional compilation block"""
        for condition, statements in block.conditions:
            if self.evaluate_condition(condition):
                return statements
        
        # No condition matched, return else block if present
        return block.else_statements or []
    
    def evaluate_condition(self, condition: Expression) -> bool:
        """Evaluate a conditional compilation expression"""
        if isinstance(condition, IdentifierExpression):
            return condition.name in self.defines
        elif isinstance(condition, BinaryExpression):
            if condition.operator == "and":
                return (self.evaluate_condition(condition.left) and 
                       self.evaluate_condition(condition.right))
            elif condition.operator == "or":
                return (self.evaluate_condition(condition.left) or 
                       self.evaluate_condition(condition.right))
        # ... handle other condition types

# Conditional compilation syntax in Runa
"""
# Feature-based compilation
When feature "async_support":
    Async Process called "async_function":
        Note: Async implementation
    End Process
End When
Otherwise:
    Process called "async_function":
        Note: Synchronous fallback
    End Process
End Otherwise

# Target-based compilation
When target "web":
    Import "web_utilities" as web_utilities
End When
When target "desktop":
    Import "desktop_utilities" as desktop_utilities
End When

# Debug vs Release
When build_mode "debug":
    Process called "debug_log" that takes message as String:
        Display "[DEBUG] " joined with message
    End Process
End When
When build_mode "release":
    Process called "debug_log" that takes message as String:
        Note: No-op in release builds
        Pass
    End Process
End When

# Version-based compilation
When version >= "2.0":
    # Use new API
    Let result be new_api_function()
Otherwise:
    # Use legacy API
    Let result be legacy_api_function()
"""
```

## Phase 9: Development Tool Integration

### Language Server Protocol (LSP) Specification

```python
class RunaLanguageServer:
    """Complete LSP implementation for Runa"""
    
    def __init__(self):
        self.workspace = Workspace()
        self.compiler = RunaCompiler()
        self.symbol_index = SymbolIndex()
        self.diagnostic_engine = DiagnosticEngine()
    
    # LSP Lifecycle
    def initialize(self, params: InitializeParams) -> InitializeResult:
        """Initialize the language server"""
        capabilities = ServerCapabilities(
            text_document_sync=TextDocumentSyncKind.INCREMENTAL,
            completion_provider=CompletionOptions(
                trigger_characters=[" ", ".", "@"],
                resolve_provider=True
            ),
            hover_provider=True,
            signature_help_provider=SignatureHelpOptions(
                trigger_characters=["(", ","]
            ),
            definition_provider=True,
            references_provider=True,
            document_highlight_provider=True,
            document_symbol_provider=True,
            workspace_symbol_provider=True,
            code_action_provider=True,
            code_lens_provider=CodeLensOptions(resolve_provider=True),
            document_formatting_provider=True,
            document_range_formatting_provider=True,
            document_on_type_formatting_provider=DocumentOnTypeFormattingOptions(
                first_trigger_character=":",
                more_trigger_character=["\n"]
            ),
            rename_provider=RenameOptions(prepare_provider=True),
            folding_range_provider=True,
            execute_command_provider=ExecuteCommandOptions(
                commands=["runa.compile", "runa.test", "runa.format"]
            ),
            semantic_tokens_provider=SemanticTokensOptions(
                legend=self.get_semantic_tokens_legend(),
                range=True,
                full=SemanticTokensFullOptions(delta=True)
            ),
            inlay_hint_provider=True,
            diagnostic_provider=DiagnosticOptions(
                identifier="runa",
                inter_file_dependencies=True,
                workspace_diagnostics=True
            )
        )
        
        return InitializeResult(capabilities=capabilities)
    
    # Text Document Synchronization
    def did_open(self, params: DidOpenTextDocumentParams):
        """Handle document open"""
        uri = params.text_document.uri
        text = params.text_document.text
        
        # Parse and analyze document
        self.workspace.add_document(uri, text)
        self.update_diagnostics(uri)
        self.update_symbol_index(uri)
    
    def did_change(self, params: DidChangeTextDocumentParams):
        """Handle document changes"""
        uri = params.text_document.uri
        
        # Apply incremental changes
        for change in params.content_changes:
            self.workspace.apply_change(uri, change)
        
        # Re-analyze document
        self.update_diagnostics(uri)
        self.update_symbol_index(uri)
    
    # Language Features
    def completion(self, params: CompletionParams) -> CompletionList:
        """Provide code completion"""
        uri = params.text_document.uri
        position = params.position
        
        # Get completion context
        document = self.workspace.get_document(uri)
        context = self.get_completion_context(document, position)
        
        # Generate completions based on context
        items = []
        
        # Keyword completions
        items.extend(self.get_keyword_completions(context))
        
        # Symbol completions
        items.extend(self.get_symbol_completions(context))
        
        # Snippet completions
        items.extend(self.get_snippet_completions(context))
        
        # Annotation completions
        items.extend(self.get_annotation_completions(context))
        
        return CompletionList(is_incomplete=False, items=items)
    
    def hover(self, params: HoverParams) -> Optional[Hover]:
        """Provide hover information"""
        uri = params.text_document.uri
        position = params.position
        
        # Find symbol at position
        symbol = self.symbol_index.find_symbol_at_position(uri, position)
        if not symbol:
            return None
        
        # Generate hover content
        content = self.generate_hover_content(symbol)
        
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.MARKDOWN,
                value=content
            ),
            range=symbol.range
        )
    
    def signature_help(self, params: SignatureHelpParams) -> Optional[SignatureHelp]:
        """Provide signature help for function calls"""
        uri = params.text_document.uri
        position = params.position
        
        # Find function call context
        call_context = self.find_function_call_context(uri, position)
        if not call_context:
            return None
        
        # Get function signatures
        signatures = self.get_function_signatures(call_context.function_name)
        
        # Determine active signature and parameter
        active_signature = self.determine_active_signature(signatures, call_context)
        active_parameter = self.determine_active_parameter(call_context)
        
        return SignatureHelp(
            signatures=signatures,
            active_signature=active_signature,
            active_parameter=active_parameter
        )
    
    def definition(self, params: DefinitionParams) -> Optional[List[Location]]:
        """Go to definition"""
        uri = params.text_document.uri
        position = params.position
        
        # Find symbol at position
        symbol = self.symbol_index.find_symbol_at_position(uri, position)
        if not symbol:
            return None
        
        # Find definition location
        definition = self.symbol_index.find_definition(symbol)
        if not definition:
            return None
        
        return [Location(uri=definition.uri, range=definition.range)]
    
    def references(self, params: ReferenceParams) -> Optional[List[Location]]:
        """Find all references"""
        uri = params.text_document.uri
        position = params.position
        
        # Find symbol at position
        symbol = self.symbol_index.find_symbol_at_position(uri, position)
        if not symbol:
            return None
        
        # Find all references
        references = self.symbol_index.find_references(symbol)
        
        # Include declaration if requested
        if params.context.include_declaration:
            definition = self.symbol_index.find_definition(symbol)
            if definition:
                references.insert(0, definition)
        
        return [Location(uri=ref.uri, range=ref.range) for ref in references]
    
    def document_symbol(self, params: DocumentSymbolParams) -> List[DocumentSymbol]:
        """Get document outline"""
        uri = params.text_document.uri
        
        # Parse document and extract symbols
        document = self.workspace.get_document(uri)
        ast = self.compiler.parse(document.text)
        
        return self.extract_document_symbols(ast)
    
    def code_action(self, params: CodeActionParams) -> List[CodeAction]:
        """Provide code actions"""
        uri = params.text_document.uri
        range = params.range
        context = params.context
        
        actions = []
        
        # Quick fixes for diagnostics
        for diagnostic in context.diagnostics:
            quick_fixes = self.generate_quick_fixes(diagnostic)
            actions.extend(quick_fixes)
        
        # Refactoring actions
        refactoring_actions = self.generate_refactoring_actions(uri, range)
        actions.extend(refactoring_actions)
        
        return actions
    
    def formatting(self, params: DocumentFormattingParams) -> List[TextEdit]:
        """Format entire document"""
        uri = params.text_document.uri
        document = self.workspace.get_document(uri)
        
        # Format the document
        formatter = RunaFormatter()
        formatted_text = formatter.format(document.text)
        
        # Return single text edit that replaces entire document
        return [TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=document.line_count, character=0)
            ),
            new_text=formatted_text
        )]
    
    def semantic_tokens_full(self, params: SemanticTokensParams) -> SemanticTokens:
        """Provide semantic highlighting"""
        uri = params.text_document.uri
        document = self.workspace.get_document(uri)
        
        # Tokenize and classify
        tokenizer = SemanticTokenizer()
        tokens = tokenizer.tokenize(document.text)
        
        # Encode tokens for LSP
        encoded_tokens = self.encode_semantic_tokens(tokens)
        
        return SemanticTokens(data=encoded_tokens)
```

### Debugger Interface and Protocol

```python
class RunaDebugAdapter:
    """Debug Adapter Protocol implementation for Runa"""
    
    def __init__(self):
        self.debugger = RunaDebugger()
        self.breakpoints = {}
        self.stack_frames = []
        self.variables = {}
    
    def initialize(self, args: InitializeRequestArguments) -> Capabilities:
        """Initialize debug adapter"""
        return Capabilities(
            supports_configuration_done_request=True,
            supports_function_breakpoints=True,
            supports_conditional_breakpoints=True,
            supports_hit_conditional_breakpoints=True,
            supports_evaluate_for_hovers=True,
            supports_step_back=False,
            supports_set_variable=True,
            supports_restart_frame=True,
            supports_goto_targets=True,
            supports_step_in_targets=True,
            supports_completions_request=True,
            completion_trigger_characters=["."],
            supports_modules_request=True,
            additional_module_columns=[],
            supported_checksum_algorithms=[],
            supports_restart_request=True,
            supports_exception_options=True,
            supports_value_formatting_options=True,
            supports_exception_info_request=True,
            support_terminate_debuggee=True,
            supports_delayed_stack_trace_loading=True,
            supports_loaded_sources_request=True,
            supports_log_points=True,
            supports_terminate_threads_request=True,
            supports_set_expression=True,
            supports_terminate_request=True,
            supports_data_breakpoints=False,
            supports_read_memory_request=False,
            supports_disassemble_request=True,
            supports_cancel_request=True,
            supports_breakpoint_locations_request=True,
            supports_clipboard_context=True
        )
    
    def launch(self, args: LaunchRequestArguments):
        """Launch Runa program for debugging"""
        # Start the Runa program with debugging enabled
        self.debugger.launch_program(
            program=args.program,
            args=args.args or [],
            cwd=args.cwd,
            env=args.env or {},
            stop_on_entry=args.stop_on_entry or False
        )
    
    def set_breakpoints(self, args: SetBreakpointsArguments) -> SetBreakpointsResponse:
        """Set breakpoints in source file"""
        source = args.source
        requested_breakpoints = args.breakpoints or []
        
        # Clear existing breakpoints for this file
        if source.path in self.breakpoints:
            for bp in self.breakpoints[source.path]:
                self.debugger.remove_breakpoint(bp.id)
        
        # Set new breakpoints
        actual_breakpoints = []
        for req_bp in requested_breakpoints:
            bp = self.debugger.set_breakpoint(
                file=source.path,
                line=req_bp.line,
                condition=req_bp.condition,
                hit_condition=req_bp.hit_condition,
                log_message=req_bp.log_message
            )
            
            actual_breakpoints.append(Breakpoint(
                id=bp.id,
                verified=bp.verified,
                line=bp.line,
                column=bp.column,
                source=source
            ))
        
        self.breakpoints[source.path] = actual_breakpoints
        return SetBreakpointsResponse(breakpoints=actual_breakpoints)
    
    def continue_(self, args: ContinueArguments) -> ContinueResponse:
        """Continue execution"""
        thread_id = args.thread_id
        all_threads_continued = self.debugger.continue_execution(thread_id)
        return ContinueResponse(all_threads_continued=all_threads_continued)
    
    def step_in(self, args: StepInArguments):
        """Step into function calls"""
        thread_id = args.thread_id
        target_id = args.target_id
        self.debugger.step_in(thread_id, target_id)
    
    def step_out(self, args: StepOutArguments):
        """Step out of current function"""
        thread_id = args.thread_id
        self.debugger.step_out(thread_id)
    
    def step_over(self, args: NextArguments):
        """Step over to next line"""
        thread_id = args.thread_id
        self.debugger.step_over(thread_id)
    
    def stack_trace(self, args: StackTraceArguments) -> StackTraceResponse:
        """Get stack trace"""
        thread_id = args.thread_id
        start_frame = args.start_frame or 0
        levels = args.levels or 20
        
        frames = self.debugger.get_stack_trace(thread_id, start_frame, levels)
        
        stack_frames = []
        for i, frame in enumerate(frames):
            stack_frames.append(StackFrame(
                id=frame.id,
                name=frame.function_name,
                source=Source(
                    name=frame.source_file,
                    path=frame.source_path
                ),
                line=frame.line,
                column=frame.column,
                end_line=frame.end_line,
                end_column=frame.end_column
            ))
        
        return StackTraceResponse(
            stack_frames=stack_frames,
            total_frames=len(frames)
        )
    
    def scopes(self, args: ScopesArguments) -> ScopesResponse:
        """Get variable scopes for stack frame"""
        frame_id = args.frame_id
        
        scopes = []
        
        # Local variables scope
        local_vars = self.debugger.get_local_variables(frame_id)
        if local_vars:
            scopes.append(Scope(
                name="Locals",
                variables_reference=self.create_variable_reference(local_vars),
                expensive=False
            ))
        
        # Global variables scope
        global_vars = self.debugger.get_global_variables(frame_id)
        if global_vars:
            scopes.append(Scope(
                name="Globals",
                variables_reference=self.create_variable_reference(global_vars),
                expensive=True
            ))
        
        return ScopesResponse(scopes=scopes)
    
    def variables(self, args: VariablesArguments) -> VariablesResponse:
        """Get variables for a scope"""
        variables_reference = args.variables_reference
        
        if variables_reference not in self.variables:
            return VariablesResponse(variables=[])
        
        var_data = self.variables[variables_reference]
        variables = []
        
        for name, value in var_data.items():
            variables.append(Variable(
                name=name,
                value=self.format_value(value),
                type=self.get_type_name(value),
                variables_reference=self.get_child_reference(value),
                evaluate_name=name
            ))
        
        return VariablesResponse(variables=variables)
    
    def evaluate(self, args: EvaluateArguments) -> EvaluateResponse:
        """Evaluate expression in current context"""
        expression = args.expression
        frame_id = args.frame_id
        context = args.context
        
        try:
            # Evaluate expression in debugger context
            result = self.debugger.evaluate_expression(expression, frame_id)
            
            return EvaluateResponse(
                result=self.format_value(result),
                type=self.get_type_name(result),
                variables_reference=self.get_child_reference(result)
            )
        except Exception as e:
            raise Exception(f"Failed to evaluate '{expression}': {str(e)}")
```

### Package Manager Specification

```python
class RunaPackageManager:
    """Package manager for Runa packages"""
    
    def __init__(self, registry_url: str = "https://packages.runa-lang.org"):
        self.registry_url = registry_url
        self.local_registry = LocalPackageRegistry()
        self.dependency_resolver = DependencyResolver()
        self.cache = PackageCache()
    
    def install_package(self, package_spec: str, version: str = "latest") -> InstallResult:
        """Install a package and its dependencies"""
        try:
            # Parse package specification
            package_info = self.parse_package_spec(package_spec, version)
            
            # Resolve dependencies
            dependency_tree = self.dependency_resolver.resolve(package_info)
            
            # Download and install packages
            installed_packages = []
            for pkg in dependency_tree:
                if not self.local_registry.is_installed(pkg.name, pkg.version):
                    self.download_and_install(pkg)
                    installed_packages.append(pkg)
            
            # Update project dependencies
            self.update_project_dependencies(package_info)
            
            return InstallResult(
                success=True,
                installed_packages=installed_packages
            )
            
        except PackageError as e:
            return InstallResult(success=False, error=str(e))
    
    def publish_package(self, package_dir: str) -> PublishResult:
        """Publish a package to the registry"""
        try:
            # Validate package structure
            self.validate_package_structure(package_dir)
            
            # Build package
            build_result = self.build_package(package_dir)
            if not build_result.success:
                raise PackageError(f"Build failed: {build_result.error}")
            
            # Create package archive
            archive_path = self.create_package_archive(package_dir)
            
            # Upload to registry
            upload_result = self.upload_to_registry(archive_path)
            
            return PublishResult(
                success=True,
                package_url=upload_result.url,
                version=upload_result.version
            )
            
        except PackageError as e:
            return PublishResult(success=False, error=str(e))
    
    def search_packages(self, query: str) -> List[PackageInfo]:
        """Search for packages in the registry"""
        response = self.query_registry("search", {"q": query})
        return [PackageInfo.from_dict(pkg) for pkg in response["packages"]]
    
    def update_dependencies(self) -> UpdateResult:
        """Update all project dependencies"""
        project_config = self.load_project_config()
        current_deps = project_config.dependencies
        
        # Check for updates
        updates_available = []
        for dep_name, dep_version in current_deps.items():
            latest_version = self.get_latest_version(dep_name)
            if self.is_newer_version(latest_version, dep_version):
                updates_available.append((dep_name, dep_version, latest_version))
        
        # Apply updates
        updated_packages = []
        for dep_name, old_version, new_version in updates_available:
            self.install_package(dep_name, new_version)
            updated_packages.append((dep_name, old_version, new_version))
        
        return UpdateResult(
            success=True,
            updated_packages=updated_packages
        )

# Package.toml structure
"""
[package]
name = "json-parser"
version = "1.2.3"
description = "Fast JSON parser for Runa"
authors = ["Jane Developer <jane@example.com>"]
license = "MIT"
repository = "https://github.com/user/json-parser"
homepage = "https://json-parser.runa-lang.org"
documentation = "https://docs.json-parser.runa-lang.org"
readme = "README.md"
keywords = ["json", "parser", "serialization"]
categories = ["parsing", "data-structures"]

[dependencies]
string-utils = "2.1"
error-handling = { version = "1.5", features = ["stack-traces"] }
benchmark = { version = "0.3", optional = true }

[dev-dependencies]
testing = "1.8"
profiling = "0.9"

[features]
default = ["fast-parsing"]
fast-parsing = []
pretty-printing = ["string-utils/formatting"]
benchmarks = ["benchmark"]

[targets]
python = { min_version = "3.8" }
javascript = { environments = ["node", "browser"] }
java = { min_version = "11" }

[build]
exclude = ["tests/", "benchmarks/", "*.tmp"]
include = ["src/", "README.md", "LICENSE"]

[scripts]
test = "runa test"
benchmark = "runa run benchmarks/ --feature benchmarks"
docs = "runa doc --output docs/"
"""
```

This comprehensive enhancement completes all the critical missing components in the Runa documentation, providing implementers with detailed specifications for runtime environments, FFI, compiler implementation, advanced language features, and development tooling.