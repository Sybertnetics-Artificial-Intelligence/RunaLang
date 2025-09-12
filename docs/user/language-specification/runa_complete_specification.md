# Runa Programming Language: Complete Specification
*Version 2.2 - AI-First Programming Language with Multiple Syntax Modes*

**Last Updated**: 2025-09-11  
**Implementation Status**: Canon/Developer modes complete, Viewer mode planned

## Table of Contents

1. [Language Overview](#language-overview)
2. [Syntax Modes](#syntax-modes)
3. [Lexical Structure](#lexical-structure)
4. [Syntax and Grammar](#syntax-and-grammar)
5. [Type System](#type-system)
6. [Semantic Analysis Rules](#semantic-analysis-rules)
7. [Memory Management](#memory-management)
8. [Module System](#module-system)
9. [Error Handling](#error-handling)
10. [Concurrency Model](#concurrency-model)
11. [AI Notation System](#ai-notation-system)
12. [Foreign Function Interface](#foreign-function-interface)
13. [Standard Library](#standard-library)
14. [Runtime Environment](#runtime-environment)
15. [Language Feature Extensions](#language-feature-extensions)

---

## Language Overview

### Design Philosophy

Runa is a revolutionary programming language designed to bridge human thought patterns with machine execution. Named after Norse runes that encoded knowledge and meaning, Runa features pseudocode-like syntax that resembles natural language while maintaining the precision needed for computational execution.

### Core Design Principles

- **Human-Readable**: Syntax that mirrors natural language for intuitive understanding
- **AI-First**: Built specifically for AI-assisted development and code generation
- **Symbol Enforcement**: Mathematical symbols restricted to mathematical contexts only
- **Type-Safe**: Strong static typing with inference to prevent errors
- **Memory-Safe**: Automatic memory management with hybrid ARC/GC system
- **Modular**: Comprehensive module system for large-scale development
- **Universal**: Designed for translation to any target programming language

### Key Features

- Natural language syntax with minimal punctuation
- Mathematical symbol enforcement with context validation
- Automatic symbol-to-word conversion during formatting
- Advanced type system with generics and algebraic data types
- Hybrid memory management combining ARC and garbage collection
- Comprehensive error handling with exceptions and result types
- Module system with dependency management and versioning
- AI notation annotations for enhanced code documentation and reasoning
- Actor-based concurrency model
- Foreign function interface for native library integration

---

## Syntax Modes

Runa implements a triple syntax architecture to serve different audiences and use cases:

### Canon Mode (Default)
- **Status**: Fully implemented
- Natural language operators: `multiplied by`, `is equal to`
- Standard Runa keywords: `Process`, `Type`, `Public`, `Private`
- Designed for clarity and AI comprehension
- Primary mode for documentation and teaching

### Developer Mode
- **Status**: Fully implemented
- Symbolic operators: `*`, `==`
- Same keywords as Canon mode (keywords don't change)
- Familiar to programmers from other languages
- Efficient for experienced developers

### Viewer Mode (Planned)
- **Status**: Not yet implemented
- **Purpose**: Read-only natural language display for non-technical stakeholders
- **Characteristics**:
  - Full natural language sentences
  - Educational context and explanations
  - AI-readable format for verification systems
  - Pattern-based transformation from compiled AST
- **Use Cases**:
  - Documentation generation
  - Code review by non-programmers
  - AI system verification (for AI that cannot parse programmatic languages)
  - Educational materials and tutorials
- **Implementation Strategy**:
  - Post-processing layer on tokenized Canon/Developer output
  - No separate lexer/parser required
  - Cache generated viewer displays for performance

### Mode Consistency
- **Keywords remain constant** across Canon and Developer modes
- **Only operators change** between Canon and Developer modes
- **Viewer mode** transforms entire code structure to natural language
- See [Syntax Modes Specification](runa_syntax_modes.md) for complete details

---

## Lexical Structure

### Whitespace and Control Tokens

```ebnf
NEWLINE               ::= platform-agnostic newline character
INDENT                ::= increase in indentation level
DEDENT                ::= decrease in indentation level
EOF                   ::= end of file token
```

### Identifiers and Keywords

```ebnf
identifier            ::= /[a-zA-Z_][a-zA-Z0-9_]*/
multi_word_identifier ::= identifier (SPACE identifier)*
```

Identifier semantics (mode-scoped):

1. Identifiers are case-sensitive in all modes.
2. Canon (writeable): preserves author-provided spacing and underscores; multi-word identifiers are valid (e.g., `user name`).
3. Developer (writeable): translates spaces to underscores during parsing/formatting, and preserves existing underscores (e.g., `user name` ↔ `user_name`).
4. Viewer (read-only): displays underscores as spaces for readability.
5. Cross-mode translation: Developer ↔ Canon round-trips preserve identifier semantics and intent; Canon defaults to spaces when translating back.

**Reserved Keywords**: Let, Define, Set, If, Otherwise, Unless, When, Match, Process, Type, Import, Export, Try, Catch, Finally, For, While, Loop, Return, Yield, Break, Continue, Throw, Assert, Display, Delete, Await, Send, Receive, Spawn, New, Static, Public, Private, Async, External, Protocol

### Literals

#### Numeric Literals

```ebnf
number_literal        ::= float_literal | integer_literal

integer_literal       ::= decimal_int | hex_int | binary_int | octal_int
decimal_int           ::= /[0-9][0-9_]*/
hex_int               ::= /0x[0-9a-fA-F][0-9a-fA-F_]*/
binary_int            ::= /0b[01][01_]*/
octal_int             ::= /0o[0-7][0-7_]*/

float_literal         ::= /[0-9][0-9_]*\.[0-9_]+/
```

#### String Literals

```ebnf
string_literal        ::= normal_string | raw_string | formatted_string

normal_string         ::= /"([^"\\]|\\.)*" | '([^'\\]|\\.)*'/
raw_string            ::= /r"[\s\S]*?" | r'[\s\S]*?'/
formatted_string      ::= /f"([^"\\]|\\.|{[^}]+})*" | f'([^'\\]|\\.|{[^}]+})*'/
```

**Escape Sequences**: `\n` (newline), `\t` (tab), `\r` (carriage return), `\\` (backslash), `\"` (double quote), `\'` (single quote), `\u{...}` (Unicode)

#### Boolean and Null Literals

```ebnf
boolean_literal       ::= "true" | "false"
null_literal          ::= "null" | "none" | "nil"
```

### Comments

```ebnf
comment               ::= single_line_comment | block_comment
single_line_comment   ::= "Note:" /.*/ NEWLINE
block_comment         ::= "Note:" NEWLINE comment_block ":End Note" NEWLINE
comment_block         ::= (/.*/ NEWLINE)*
```

Runa supports both single-line and block-style comments for documentation and code annotation.

- **Single-line comment:**
  ```runa
  Note: This is a single-line comment
  ```
- **Block/multi-line comment:**
  ```runa
  Note:
  This is a multi-line comment or documentation block.
  You can write as many lines as needed.
  :End Note
  ```
- The block starts with `Note:` on its own line and ends with `:End Note` on its own line.
- No need to prefix each line inside the block.

This convention ensures comments are readable, natural, and easy for both humans and tools to parse.

---

## Syntax and Grammar
### Syntax Modes (Normative)

- Canon (writeable): canonical natural syntax; avoids mathematical symbols outside mathematical contexts.
- Developer (writeable): technical shorthand; permits mathematical symbols in mathematical contexts; auto-translates to Canon during parsing.
- Viewer (read-only): natural-language display for comprehension; not writeable; generated from Canon/Developer.

Unless stated otherwise, examples in this specification are Canon.

### Program Structure

```ebnf
program               ::= (declaration | statement | ai_annotation)* EOF

declaration           ::= function_definition
                        | type_definition
                        | import_statement
                        | export_declaration

statement             ::= simple_statement
                        | compound_statement
                        | flow_control_statement
                        | error_handling_statement
                        | concurrency_statement
                        | memory_statement
```

### Variable Declarations and Assignments

#### Revolutionary Encasing Keyword Pairs

Runa supports natural multi-word variable names through encasing keyword pairs. Variable names can contain spaces and are captured between keyword boundaries:

```ebnf
let_statement         ::= "Let" encased_identifier type_annotation? "be" expression
                        | "Let" pattern "be" expression

encased_identifier    ::= word+ (captured until "be")
set_statement         ::= "Set" encased_identifier "to" expression
```

**Examples:**
```runa
Note: Multi-word variable names
Let user input value be 42
Let maximum retry count be 3
Set total calculation result to sum

Note: "Last occurrence wins" rule for ambiguous cases
Let x be y be 5  Note: Variable is "x be y", value is 5
```

**Standard Declaration Forms:**

```ebnf
let_statement         ::= "Let" identifier type_annotation? "be" expression
                        | "Let" pattern "be" expression

define_statement      ::= "Define" identifier type_annotation? "as" expression
                        | "Constant" identifier "as" type_expression "is" expression

set_statement         ::= "Set" assignable "to" expression

assignable            ::= identifier | member_access | index_access

type_annotation       ::= "(" type_expression ")"
```

#### Examples

```runa
Note: Variable declarations (mutable)
Let count be 0
Let name be "Alice"
Let user be User()

Note: Constant declarations (immutable)
Constant PI as Float is 3.14159
Constant MAX_SIZE as Integer is 1000
Constant APP_NAME as String is "MyApplication"

Note: Variable assignment (mutation)
Set count to count plus 1
Set user.name to "Bob"
```

### Object Creation and Constructors

Runa provides an explicit and unambiguous syntax for object creation that clearly distinguishes constructors from other expressions.

#### Constructor Syntax

```ebnf
constructor_expression ::= "a" "value" "of" "type" type_identifier constructor_fields?
                         | "of" "type" type_identifier constructor_fields?  // Shortened form

constructor_fields     ::= "with" field_initializers

field_initializers     ::= field_initializer ("and" field_initializer)*
                         | field_initializer ("," field_initializer)*

field_initializer      ::= identifier "as" expression
```

#### Rationale

The `a value of type` pattern provides complete disambiguation between:
- Object construction (creating new instances)
- Function calls (invoking processes)
- Simple variable assignments
- Expression evaluations

This syntax is:
1. **Completely unambiguous**: The parser immediately recognizes the pattern
2. **Self-documenting**: Reads as natural English
3. **AI-friendly**: Easy for language models to generate and parse
4. **Philosophically aligned**: Prioritizes clarity over brevity

#### Examples

```runa
Note: Default constructor (no field initialization)
Let args be a value of type CommandLineArgs

Note: Constructor with field initialization
Let point be a value of type Point with x as 10 and y as 20

Note: Complex type construction
Let user be a value of type User with
    name as "Alice",
    age as 30,
    email as "alice@example.com"

Note: Shortened form (optional)
Let config be of type Configuration with debug as true

Note: Contrast with function calls
Let result be calculate with radius as 5        Note: Function call
Let circle be a value of type Circle with radius as 5  Note: Constructor
```

#### Type Resolution

When the compiler encounters `a value of type TypeName`, it:
1. Verifies that `TypeName` is a valid type in scope
2. Generates or calls the appropriate constructor function
3. Allocates memory for the new instance
4. Initializes fields (if provided) or sets defaults
5. Returns a reference to the newly created instance

#### Default Field Values

If fields are not specified in the constructor:
- Numeric types default to 0
- Boolean types default to false  
- String types default to ""
- Reference types default to null/None
- Collections default to empty

```runa
Note: These are equivalent
Let config1 be a value of type Config
Let config2 be a value of type Config with
    debug as false,
    verbosity as 0,
    output_file as ""
```

### Imperative Statement Patterns

Runa supports natural language imperative statements for common operations:

#### Compound Assignment Statements

These statements modify variables in place using natural English:

```ebnf
increase_statement    ::= "Increase" encased_identifier "by" expression
decrease_statement    ::= "Decrease" encased_identifier "by" expression
multiply_statement    ::= "Multiply" encased_identifier "by" expression
divide_statement      ::= "Divide" encased_identifier "by" expression
```

**Examples:**
```runa
Note: Imperative compound assignments
Increase count by 1
Decrease health points by damage
Multiply price by discount factor
Divide total cost by number of items

Note: These are equivalent to:
Set count to count gets increased by 1
Set health points to health points gets decreased by damage
Set price to price gets multiplied by discount factor
Set total cost to total cost gets divided by number of items
```

### Control Structures

```ebnf
if_statement          ::= "If" expression ":" block 
                         ("Otherwise" "if" expression ":" block)*
                         ("Otherwise" ":" block)? "End" "If"

unless_statement      ::= "Unless" expression ":" block "End" "Unless"

when_statement        ::= "When" expression ":" block "End" "When"

match_statement       ::= "Match" expression ":" INDENT match_cases DEDENT "End" "Match"

match_cases           ::= match_case+
match_case            ::= "When" pattern guard? ":" block
guard                 ::= "where" expression

for_loop              ::= for_each_loop | for_range_loop
for_each_loop         ::= "For" "each" identifier "in" expression ":" block "End" "For"
for_range_loop        ::= "For" identifier "from" expression "to" expression 
                         ("by" expression)? ":" block "End" "For"

while_loop            ::= "While" expression ":" block "End" "While"
do_while_loop         ::= "Do" ":" block "While" expression "End" "Do"
repeat_loop           ::= "Repeat" expression "times" ":" block "End" "Repeat"
infinite_loop         ::= "Loop" "forever" ":" block "End" "Loop"
```

### Function Definitions

```ebnf
function_definition   ::= "Async"? "Process" "called" string_literal
                         ("that" "takes" parameter_list)?
                         ("returns" type_expression)?
                         ":" block "End" "Process"

parameter_list        ::= parameter (("and" | ",") parameter)*
parameter             ::= identifier ("as" type_expression)? ("defaults" "to" expression)?
```

### Type Definitions

```ebnf
type_definition       ::= "Type" identifier generic_params? "is" type_body

generic_params        ::= "[" identifier ("," identifier)* "]"

type_body             ::= record_definition | adt_definition | type_alias

record_definition     ::= "Dictionary" "with" inheritance_clause? protocol_conformance_clause? ":"
                         INDENT (field_declaration | method_definition | static_member_definition)+ DEDENT "End" "Type"

adt_definition        ::= ":" INDENT ("|" adt_variant)+ DEDENT "End" "Type"
adt_variant           ::= identifier ("with" variant_fields)? NEWLINE

type_alias            ::= type_expression
```

### Pattern Matching

```ebnf
pattern               ::= literal_pattern
                        | identifier_pattern
                        | wildcard_pattern
                        | list_pattern
                        | tuple_pattern
                        | record_pattern
                        | type_pattern
                        | or_pattern
                        | as_pattern

literal_pattern       ::= literal
identifier_pattern    ::= identifier
wildcard_pattern      ::= "_"
list_pattern          ::= "[" pattern_list "]"
                        | "list" "containing" pattern_list
tuple_pattern         ::= "(" pattern_list ")"
record_pattern        ::= "{" record_pattern_fields "}"
                        | "dictionary" "with" ":" INDENT record_pattern_fields DEDENT
type_pattern          ::= pattern "of" "type" type_expression
or_pattern            ::= pattern ("|" pattern)+
as_pattern            ::= pattern "as" identifier
```

### Expressions

```ebnf
expression            ::= ternary_expression

ternary_expression    ::= or_expression ("If" or_expression "Otherwise" or_expression)?

or_expression         ::= and_expression ("or" and_expression)*

and_expression        ::= not_expression ("and" not_expression)*

not_expression        ::= "not" not_expression | comparison_expression

comparison_expression ::= additive_expression (comparison_op additive_expression)*

comparison_op         ::= "equals"
                        | "is" "equal" "to"
                        | "does" "not" "equal"
                        | "is" "not" "equal" "to"
                        | "is" "greater" "than"
                        | "is" "less" "than"
                        | "is" "greater" "than" "or" "equal" "to"
                        | "is" "less" "than" "or" "equal" "to"
                        | "contains"
                        | "is" "in"
                        | "is" "of" "type"

additive_expression   ::= multiplicative_expression (additive_op multiplicative_expression)*

additive_op           ::= "plus" | "minus" | "joined" "with"

multiplicative_expression ::= unary_expression (multiplicative_op unary_expression)*

multiplicative_op     ::= "multiplied" "by" | "divided" "by" | "modulo"

unary_expression      ::= unary_op unary_expression | power_expression

unary_op              ::= "negative" | "positive" | "bitwise" "not"

power_expression      ::= postfix_expression ("to" "the" "power" "of" postfix_expression)*

postfix_expression    ::= primary_expression postfix_op*

postfix_op            ::= member_access | index_access | slice_access | function_call | type_cast

primary_expression    ::= literal
                        | identifier
                        | "(" expression ")"
                        | lambda_expression
                        | list_comprehension
                        | new_expression
                        | await_expression
                        | receive_expression
                        | spawn_expression
                        | typeof_expression
                        | sizeof_expression
```

### Field and Method Access (Mode-Scoped)

Runa supports both natural language and technical syntax for accessing fields and methods. Usage is scoped by mode:

- Canon: use natural phrases like "the name of user" and "the area of circle".
- Developer: may use dot notation (e.g., `user.name`, `circle.area`) as a technical shorthand.
- Viewer: displays natural phrases; dot notation is not shown.

#### Field Access

**Natural Language Syntax (Recommended for Basic/Intermediate Examples):**
```runa
Let radius be the radius of circle
Let name be the name of user
Let width be the width of rectangle
Let value be the value of counter
```

**Developer Mode Technical Syntax:**
```runa
Let radius be circle.radius
Let name be user.name
Let width be rectangle.width
Let value be counter.value
```

#### Method Access

**Natural Language Syntax (Recommended for Basic/Intermediate Examples):**
```runa
Let area be the area of circle
Let magnitude be the magnitude of complex_number
Let result be the output of process with input as value
Let sum be the sum of a and b
```

**Technical Syntax (For Advanced/Backend Development):**
```runa
Let area be circle.area
Let magnitude be complex_number.magnitude
Let result be process with self as value
Let sum be add with a as a and b as b
```

#### Collection Access (Mode-Scoped)

**Developer Mode Bracket Notation (Dictionaries and Lists):**
```runa
Let value be my_dict["key"]
Let item be my_list[0]
Let element be array at index 5
Let value2 be my_dict at key "id"
```

**Canon/Viewer Natural Language for Collections:**
```runa
Let value be the value of my_dict at key
Let item be the first item of my_list
Let element be the element of array at index 5
```

#### Type Definitions with Methods

```runa
Type called "Circle":
    radius as Float

    Process called "area" returns Float:
        Return 3.14159 multiplied by the radius of self to the power of 2
        Note: Or: Return 3.14159 multiplied by self.radius to the power of 2

    Process called "circumference" returns Float:
        Return 2 multiplied by 3.14159 multiplied by the radius of self
        Note: Or: Return 2 multiplied by 3.14159 multiplied by self.radius
```

#### Usage Guidelines

1. **Basic and Intermediate Examples**: Use natural language syntax for better readability and accessibility
2. **Advanced/Backend Development**: Use technical syntax for efficiency and familiarity
3. **Documentation**: Always provide natural language examples first, with technical syntax as alternatives
4. **Consistency**: Choose one style per project or module for consistency

### Function Calls Without Parentheses

Runa supports natural function invocation without parentheses in Canon mode. The lexer uses context to determine if an identifier is a function call:

#### Context-Based Recognition

When the lexer encounters an identifier that matches a known function name, it treats it as a function call:

```runa
Note: Zero-argument functions
Let time be current timestamp      Note: Calls current_timestamp()
Let area be calculate area         Note: Calls calculate_area()

Note: Functions with arguments use "with" or "given"
Let result be calculate area with radius
Let sum be add numbers with first and second
Let output be process data given input
```

#### Parentheses in Developer Mode

Developer mode may use traditional parentheses:

```runa
Let time be current_timestamp()
Let area be calculate_area(radius)
Let sum be add_numbers(first, second)
```

#### Disambiguation Rules

1. **Known Functions**: If identifier matches a function in scope, treat as call
2. **With/Given Keywords**: Presence of "with" or "given" indicates function call with arguments
3. **Parentheses**: Always indicates function call regardless of mode
4. **Context**: Parser uses surrounding context to resolve ambiguity

#### Examples by Audience

**For Non-Developers/Domain Experts:**
```runa
Let user_name be the name of current_user
Let account_balance be the balance of user_account
Let transaction_count be the count of transactions
Let is_active be the status of user_account
```

**For Experienced Developers:**
```runa
Let user_name be current_user.name
Let account_balance be user_account.balance
Let transaction_count be transactions.count
Let is_active be user_account.status
```

**For AI/Advanced Development:**
```runa
Let result be process_data with input as data and config as settings
Let output be neural_network.forward with input as features
Let gradient be loss_function.backward with prediction as pred and target as target
```

---

## Type System

### Basic Types

```runa
Type Any                     Note: Any value
Type Integer                 Note: Whole numbers (e.g., 1, -5, 42)
Type Float                   Note: Floating-point numbers (e.g., 3.14, -0.5)
Type Boolean                 Note: Boolean values (true, false)
Type String                  Note: Text strings (e.g., "Hello")
Type None                    Note: The unit type, represented by None
```

### Collection Types

```runa
Type List[T]                 Note: List of elements of type T
Type Dictionary[K, V]        Note: Dictionary with keys of type K and values of type V
Type Set[T]                  Note: Set of elements of type T
Type Tuple[T1, T2, ...]      Note: Tuple with elements of specified types
```

### Function Types

```runa
Type Function[T1, T2, ..., R]  Note: Function taking arguments of types T1, T2, ... and returning type R
```

### Type Expressions

```ebnf
type_expression       ::= basic_type
                        | generic_type
                        | union_type
                        | intersection_type
                        | function_type
                        | optional_type
                        | array_type
                        | tuple_type
                        | record_type
                        | type_identifier

basic_type            ::= "Integer" | "Float" | "String" | "Boolean" 
                        | "Character" | "Byte" | "Any" | "Void" | "Never"

generic_type          ::= type_identifier "[" type_list "]"

union_type            ::= type_expression ("OR" type_expression)+

intersection_type     ::= type_expression ("AND" type_expression)+

function_type         ::= "Function" "[" type_list "," type_expression "]"

optional_type         ::= "Optional" "[" type_expression "]"
```

### Type Inference

Runa's type inference system reduces the need for explicit annotations:

```runa
Note: Type is inferred as Dictionary[String, Integer]
Let scores be dictionary containing:
    "Alice" as 95
    "Bob" as 87
    "Charlie" as 92

Note: Return type is inferred as the same type as 'value'
Process called "double" that takes value:
    Return value multiplied by 2

Note: Types are propagated through expressions
Let numbers be list containing 1, 2, 3
Let doubled be Map over numbers using double
Note: doubled is inferred as List[Integer]
```

### Generic Types

```runa
Note: Generic identity function
Process called "identity"[T] that takes value as T returns T:
    Return value

Note: Generic pair type
Type called "Pair"[A, B]:
    first as A
    second as B

Note: Create a pair
Let point be Pair[Integer, Integer] with:
    first as 10
    second as 20
```

### Union Types

```runa
Type Result is Integer OR String

Process called "safe_divide" that takes a as Integer and b as Integer returns Result:
    If b is equal to 0:
        Return "Cannot divide by zero"
    Otherwise:
        Return a divided by b
```

### Algebraic Data Types

```runa
Note: Sum type (variant)
Type Shape is
    | Circle with radius as Float
    | Rectangle with width as Float and height as Float
    | Triangle with base as Float and height as Float

Note: Create shapes
Let circle be Shape.Circle with radius as 5.0
Let rectangle be Shape.Rectangle with width as 4.0 and height as 3.0

Note: Calculate area based on shape type
Process called "calculate_area" that takes shape as Shape returns Float:
    Match shape:
        When Circle with radius as r:
            Return 3.14159 multiplied by r multiplied by r
        When Rectangle with width as w and height as h:
            Return w multiplied by h
        When Triangle with base as b and height as h:
            Return 0.5 multiplied by b multiplied by h
```

---

## Semantic Analysis Rules

### Symbol Table Management

1. **Scope Hierarchy**: Global → Module → Function → Block
2. **Name Resolution**: Inner scopes shadow outer scopes
3. **Forward Declarations**: Allowed for mutually recursive functions
4. **Circular Dependencies**: Detected and reported as errors

### Type Checking Rules

1. **Assignment Compatibility**: Strict type checking with coercion rules
2. **Function Call Validation**: Parameter count and type matching
3. **Return Type Consistency**: All return paths must match declared type
4. **Generic Instantiation**: Type parameter substitution and constraint checking

### Advanced Features

#### Generics and Type Constraints

```runa
Note: Constrain to types that support comparison
Process called "max"[T: Comparable] that takes a as T and b as T returns T:
    If a is greater than b:
        Return a
    Otherwise:
        Return b

Note: Multiple constraints
Process called "sort_and_display"[T: Comparable + Serializable] that takes items as List[T]:
    Let sorted_items be sort items
    For each item in sorted_items:
        Display item.to_string()

Note: Where clauses for complex constraints
Process called "process_collection"[T, U] that takes input as T returns U
    where T implements Iterable[U] and U implements Comparable[U]:
    Let sorted_items be sort input
    Return first item from sorted_items
```

#### Closure Capture Rules

1. **By Value**: Immutable captures for basic types
2. **By Reference**: Mutable captures for complex types
3. **Lifetime Analysis**: Ensures captured variables outlive closures
4. **Move Semantics**: Ownership transfer for unique resources

```runa
Note: Capture by value (immutable)
Let counter be 0
Let increment_func be lambda: counter plus 1  Note: counter captured by value

Note: Capture by reference (mutable)
Let mutable_state be mutable dictionary
Let modifier_func be lambda x: Set mutable_state["count"] to x  Note: mutable capture

Note: Move capture (ownership transfer)
Let large_data be create_large_dataset()
Let processor_func be move lambda: process_data(large_data)  Note: large_data moved
```

#### Shadowing Rules

1. **Variable Shadowing**: Inner scope variables hide outer scope
2. **Function Overloading**: Not allowed - use different names
3. **Type Shadowing**: Inner type definitions hide outer ones
4. **Import Shadowing**: Imported names can be shadowed by local definitions

### Edge Cases and Error Conditions

#### Type System Edge Cases

```runa
Note: Recursive type definitions
Type Node[T] is Record with:
    value as T
    children as List[Node[T]]  Note: Self-referential type

Note: Mutually recursive types
Type Tree is Record with:
    root as TreeNode

Type TreeNode is Record with:
    tree as Tree  Note: Mutually recursive
    value as Integer

Note: Generic type bounds checking
Process called "constrained_function"[T: Numeric + Comparable] that takes x as T:
    Note: T must implement both Numeric and Comparable
    If x is greater than zero():
        Return x.sqrt()  Note: Valid: T implements Numeric
    Return zero()  Note: Error detection: ensure zero() returns T

Note: Type inference limits
Let ambiguous_value be None  Note: Error: cannot infer type
Let explicit_value be None as Optional[String]  Note: OK: explicit type
```

#### Scope Resolution Edge Cases

```runa
Note: Complex nested scoping
Let global_var be "global"

Process called "outer_function":
    Let outer_var be "outer"
    
    Process called "inner_function":
        Let inner_var be "inner"
        Note: Can access: inner_var, outer_var, global_var
        
        If condition:
            Let block_var be "block"
            Note: Can access: block_var, inner_var, outer_var, global_var
            
            Process called "nested_function":
                Note: Can access: inner_var, outer_var, global_var
                Note: Cannot access: block_var (different block scope)
                Display outer_var  Note: Valid
                Display block_var  Note: Error: not in scope

Note: Forward reference resolution
Process called "function_a":
    Return function_b()  Note: Forward reference - OK

Process called "function_b":
    Return "result"

Note: Circular function dependency (allowed)
Process called "is_even" that takes n as Integer returns Boolean:
    If n is equal to 0:
        Return True
    Return is_odd(n minus 1)

Process called "is_odd" that takes n as Integer returns Boolean:
    If n is equal to 0:
        Return False
    Return is_even(n minus 1)
```

#### Generic Instantiation Edge Cases

```runa
Note: Higher-kinded type instantiation
Type Container[F[_], T] is Record with:
    data as F[T]

Note: F must be a type constructor (List, Optional, etc.)
Let list_container be Container[List, String] with data as ["a", "b", "c"]
Let optional_container be Container[Optional, Integer] with data as Some(42)

Note: Generic constraint satisfaction
Process called "generic_processor"[T: Serializable + Clone] that takes items as List[T]:
    Note: T must satisfy both constraints
    Let cloned_items be items.map(lambda x: x.clone())  Note: Uses Clone
    Let serialized be cloned_items.map(lambda x: x.serialize())  Note: Uses Serializable
    Return serialized

Note: Type parameter variance
Type Producer[+T] is Record with:  Note: Covariant in T
    produce as Process[] returns T

Type Consumer[-T] is Record with:  Note: Contravariant in T
    consume as Process[T] returns Unit

Type Processor[T] is Record with:  Note: Invariant in T
    process as Process[T] returns T
```

#### Pattern Matching Exhaustiveness

```runa
Note: Exhaustiveness checking for ADTs
Type Color is ADT with:
    Red
    Green
    Blue

Process called "color_to_string" that takes color as Color returns String:
    Match color:
        When Red:
            Return "red"
        When Green:
            Return "green"
        Note: Error: missing Blue case - non-exhaustive pattern

Note: Guard clause reachability
Process called "classify_number" that takes n as Integer returns String:
    Match n:
        When x where x is greater than 0:
            Return "positive"
        When x where x is less than 0:
            Return "negative"
        When 0:
            Return "zero"
        When x where x is greater than 5:  Note: Error: unreachable pattern
            Return "large positive"

Note: Nested pattern completeness
Type Result[T, E] is ADT with:
    Ok(value as T)
    Error(error as E)

Process called "unwrap_result" that takes result as Result[String, Integer]:
    Match result:
        When Ok(value) where length of value is greater than 0:
            Return value
        When Ok(value):  Note: Handles empty strings
            Return "empty"
        When Error(code) where code is less than 100:
            Return "minor error"
        Note: Error: missing Error case for code >= 100
```

#### Memory Safety Analysis

```runa
Note: Lifetime analysis for references
Process called "get_reference" that takes data as List[String] returns Reference[String]:
    If length of data is greater than 0:
        Return reference to data[0]  Note: Valid: data outlives return
    Otherwise:
        Let local_string be "temp"
        Return reference to local_string  Note: Error: local_string doesn't outlive return

Note: Ownership transfer validation
Process called "transfer_ownership" that takes data as List[String]):
    Let processor be create_data_processor()
    processor.take_ownership(data)  Note: data ownership transferred
    Display length of data  Note: Error: data no longer owned

Note: Mutable aliasing prevention
Process called "prevent_aliasing" that takes data as mutable List[String]):
    Let mutable_ref1 be mutable reference to data
    Let mutable_ref2 be mutable reference to data  Note: Error: multiple mutable references
    
    Note: Alternative: exclusive access pattern
    With exclusive_access to data as exclusive_data:
        Note: Only exclusive_data can modify during this block
        Add "new item" to exclusive_data
```

#### Control Flow Analysis

```runa
Note: Unreachable code detection
Process called "unreachable_example" that takes x as Integer:
    If x is greater than 0:
        Return "positive"
    Otherwise:
        Return "non-positive"
    Display "This will never execute"  Note: Error: unreachable code

Note: Definite assignment analysis
Process called "assignment_analysis" that takes condition as Boolean returns String:
    Let result as String  Note: Declared but not initialized
    
    If condition:
        Set result to "true case"
    Note: Error: result may not be initialized in all paths
    Return result

Note: Corrected version
Process called "correct_assignment" that takes condition as Boolean returns String:
    Let result as String
    
    If condition:
        Set result to "true case"
    Otherwise:
        Set result to "false case"
    Note: OK: result definitely assigned in all paths
    Return result

Note: Return path analysis
Process called "return_analysis" that takes x as Integer returns String:
    If x is greater than 0:
        Return "positive"
    If x is less than 0:
        Return "negative"
    Note: Error: missing return for x == 0 case

Note: Loop analysis for definite assignment
Process called "loop_assignment" that takes items as List[String]) returns String:
    Let result as String
    
    For each item in items:
        Set result to item
        Break
    Note: Error: result may not be assigned if items is empty
    Return result
```

#### Recursive Type and Function Analysis

```runa
# Tail recursion optimization detection
Process called "tail_recursive_factorial" that takes n as Integer and acc as Integer returns Integer:
    If n is less than or equal to 1:
        Return acc
    Return tail_recursive_factorial(n minus 1, acc multiplied by n)  Note: Tail call

Process called "non_tail_recursive_factorial" that takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    Return n multiplied by non_tail_recursive_factorial(n minus 1)  Note: Not tail call

# Infinite recursion detection (static analysis)
Process called "infinite_recursion" that takes x as Integer returns Integer:
    Return infinite_recursion(x)  Note: Warning: potential infinite recursion

# Mutual recursion depth analysis
Process called "deep_mutual_recursion_a" that takes depth as Integer:
    If depth is greater than 1000:  Note: Stack overflow protection
        Throw StackOverflowError with message "Recursion too deep"
    Return deep_mutual_recursion_b(depth plus 1)

Process called "deep_mutual_recursion_b" that takes depth as Integer:
    Return deep_mutual_recursion_a(depth plus 1)
```

#### Module System Edge Cases

```runa
Note: Circular import detection
Note: File: module_a.runa
Import module "module_b"  Note: Creates circular dependency

Export Process called "function_a":
    Return module_b.function_b()

Note: File: module_b.runa  
Import module "module_a"  Note: Error: circular import detected

Export Process called "function_b":
    Return module_a.function_a()

Note: Re-export analysis
Note: File: core.runa
Export Process called "core_function":
    Return "core"

Note: File: utils.runa
Import { core_function } from module "core"
Export core_function  Note: Re-export

Note: File: main.runa
Import { core_function } from module "utils"  Note: Valid: transitively imported

Note: Name collision resolution
Import { function_name } from module "module_a"
Import { function_name } from module "module_b"  Note: Error: name collision

Note: Resolution with aliasing
Import { function_name as function_a } from module "module_a"
Import { function_name as function_b } from module "module_b"  Note: OK: aliased
```

---

## Memory Management

### Hybrid Memory Management Model

Runa employs a sophisticated hybrid memory management system:

1. **Automatic Reference Counting (ARC)** for deterministic deallocation
2. **Cycle-breaking Garbage Collector** for handling reference cycles
3. **Stack allocation** for small, short-lived objects
4. **Region-based allocation** for batch operations

### Memory Safety Guarantees

1. **No Null Pointer Dereferences**: Optional types enforce null checking
2. **No Buffer Overflows**: Array bounds checking
3. **No Use-After-Free**: Ownership tracking and lifetime analysis
4. **No Double-Free**: Automatic memory management prevents manual errors

### Resource Management

#### Automatic Resource Management (RAII)

```runa
With open_file("data.txt") as file:
    Let content be file.read_all()
    Display content
Note: File is automatically closed here
Note: File is automatically closed here
```

#### Manual Memory Control (Advanced)

```runa
@Resource_Constraints:
    memory_limit: "512MB"
    optimize_for: "memory"
@End_Resource_Constraints

Process called "large_computation" that takes data:
    Note: Memory usage is tracked and limited
    Let result be process_data with data as data
    Return result
```

---

## Module System

### Module Structure

Every Runa file is implicitly a module. Modules can export declarations and import from other modules.

```runa
Note: geometry.runa
Export Constant PI as Float is 3.14159

Export Type called "Circle":
    radius as Float

    Process called "area" returns Float:
        Return PI multiplied by self.radius to the power of 2

Note: Private function - not exported
Process called "internal_helper":
    Note: Implementation
```

### Import System

```ebnf
import_statement      ::= "Import" "Module" string_literal "as" identifier
                        | "Import" "{" import_list "}" "from" "Module" string_literal
                        | "Import" import_list "from" identifier

import_list           ::= identifier ("as" identifier)? ("," identifier ("as" identifier)?)*
```

```runa
Note: Import entire module (canonical form)
Import Module "geometry" as geometry
Let c be New Circle from geometry with radius as 10

Note: Import specific items
Import { PI, Circle } from Module "geometry"
Let c2 be New Circle with radius as 5

Note: Using member access operators
Let area be area of circle
Let pi_value be PI from Math
```

### Package Management and Versioning

#### Semantic Versioning System

```runa
Note: Package.toml - Package manifest file
[package]
name = "data_processor"
version = "2.1.3"                Note: Major.Minor.Patch
description = "High-performance data processing library"
authors = ["Developer <dev@example.com>"]
license = "MIT"
repository = "https://github.com/user/data-processor"
homepage = "https://data-processor.example.com"
documentation = "https://docs.data-processor.example.com"
readme = "README.md"
keywords = ["data", "processing", "analytics"]
categories = ["data-structures", "algorithms"]
edition = "2024"                 Note: Runa language edition

[dependencies]
Note: Version specifications
math_utils = "1.2.3"            Note: Exact version
string_tools = "^2.1.0"         Note: Compatible version (2.1.0 <= version < 3.0.0)
network_lib = "~1.4.5"          Note: Tilde version (1.4.5 <= version < 1.5.0)
logging = { version = "3.0", features = ["async", "json"] }
crypto = { version = "1.0", optional = true }

Note: Development dependencies
testing = { version = "2.0", dev = true }
benchmarks = { version = "1.0", dev = true }

Note: Platform-specific dependencies
[dependencies.windows]
windows_api = "0.48"

[dependencies.unix]
libc = "0.2"

[features]
default = ["compression", "validation"]
compression = ["crypto"]
validation = ["string_tools/validation"]
async_support = ["network_lib/async"]
crypto_features = ["crypto"]

[build]
exclude = ["tests/", "benchmarks/", "*.tmp"]
include = ["src/", "README.md", "LICENSE", "Package.toml"]
```

#### Version Compatibility and Resolution

```runa
Note: Version constraint resolution algorithm
Process called "resolve_dependencies" that takes packages as List[PackageSpec] returns DependencyGraph:
    Let dependency_graph be create_dependency_graph()
    Let resolved_versions be Dictionary[String, Version]
    
    Note: Phase 1: Collect all dependencies and their constraints
    For each package in packages:
        Let constraints be collect_version_constraints(package)
        dependency_graph.add_constraints(constraints)
    
    Note: Phase 2: Resolve version conflicts
    For each package_name in dependency_graph.get_package_names():
        Let version_constraints be dependency_graph.get_constraints(package_name)
        Let compatible_version be find_compatible_version(version_constraints)
        
        If compatible_version is None:
            Throw DependencyResolutionError with:
                message: "Cannot resolve compatible version for package"
                package: package_name
                constraints: version_constraints
        
        Set resolved_versions[package_name] to compatible_version
    
    Return create_resolved_graph(resolved_versions)

# Version compatibility checking
Process called "is_compatible" that takes version as Version and constraint as VersionConstraint returns Boolean:
    Match constraint.type:
        When "exact":
            Return version equals constraint.version
        When "caret":  Note: ^1.2.3 allows >=1.2.3 and <2.0.0
            Return version is greater than or equal to constraint.version and
                   version.major equals constraint.version.major
        When "tilde":  Note: ~1.2.3 allows >=1.2.3 and <1.3.0  
            Return version is greater than or equal to constraint.version and
                   version.major equals constraint.version.major and
                   version.minor equals constraint.version.minor
        When "range":  Note: 1.0.0 - 2.0.0
            Return version is greater than or equal to constraint.min_version and
                   version is less than or equal to constraint.max_version
```

#### Circular Dependency Detection and Resolution

```runa
Note: Advanced circular dependency detection
Type DependencyNode is Record with:
    module_name as String
    dependencies as List[String]
    state as DependencyState  Note: Unvisited, Visiting, Visited

Type DependencyState is ADT with:
    Unvisited
    Visiting
    Visited

Process called "detect_circular_dependencies" that takes modules as List[Module] returns List[CircularDependency]:
    Let dependency_graph be build_dependency_graph(modules)
    Let circular_dependencies be List[CircularDependency]
    Let node_states be Dictionary[String, DependencyState]
    
    Note: Initialize all nodes as unvisited
    For each module in modules:
        Set node_states[module.name] to DependencyState.Unvisited
    
    Note: Depth-first search to detect cycles
    For each module in modules:
        If node_states[module.name] is equal to DependencyState.Unvisited:
            Let cycle be detect_cycle_from_node(module.name, dependency_graph, node_states)
            If cycle is not None:
                Add cycle to circular_dependencies
    
    Return circular_dependencies

Process called "detect_cycle_from_node" that takes node_name as String and graph as DependencyGraph and states as Dictionary[String, DependencyState] returns Optional[CircularDependency]:
    Set states[node_name] to DependencyState.Visiting
    
    For each dependency in graph.get_dependencies(node_name):
        Match states[dependency]:
            When DependencyState.Visiting:
                Note: Found a cycle - trace back to find complete cycle
                Return trace_cycle_path(dependency, node_name, graph)
            When DependencyState.Unvisited:
                Let nested_cycle be detect_cycle_from_node(dependency, graph, states)
                If nested_cycle is not None:
                    Return nested_cycle
    
    Set states[node_name] to DependencyState.Visited
    Return None

Note: Circular dependency resolution strategies
Type CircularDependencyResolution is ADT with:
    InterfaceExtraction      Note: Extract common interface
    DependencyInversion      Note: Invert dependency direction
    MediatorPattern         Note: Introduce mediator module
    LazyInitialization     Note: Use lazy loading
    WeakReferences          Note: Use weak references for cycles

Process called "resolve_circular_dependency" that takes cycle as CircularDependency returns ResolutionPlan:
    Let analysis be analyze_dependency_cycle(cycle)
    
    Match analysis.cycle_type:
        When "interface_cycle":
            Return create_interface_extraction_plan(cycle)
        When "initialization_cycle":
            Return create_lazy_initialization_plan(cycle)
        When "mutual_reference_cycle":
            Return create_weak_reference_plan(cycle)
        When "complex_cycle":
            Return create_mediator_pattern_plan(cycle)

Note: Example: Interface extraction for circular dependencies
Note: Before resolution (circular):
Note: File: user.runa
Import module "order"
Type User is Record with:
    orders as List[order.Order]  Note: Circular dependency

Note: File: order.runa  
Import module "user"
Type Order is Record with:
    user as user.User           Note: Circular dependency

Note: After resolution (interface extraction):
Note: File: user_interface.runa
Type UserInterface is Protocol with:
    Process get_id returns String
    Process get_name returns String

Note: File: order_interface.runa
Type OrderInterface is Protocol with:
    Process get_id returns String
    Process get_total returns Float

Note: File: user.runa
Import module "user_interface"
Import module "order_interface"
Type User is Record with:
    orders as List[order_interface.OrderInterface]
    Process implements user_interface.UserInterface

Note: File: order.runa
Import module "user_interface" 
Import module "order_interface"
Type Order is Record with:
    user as user_interface.UserInterface
    Process implements order_interface.OrderInterface
```

#### Module Initialization and Loading

```runa
Note: Module initialization phases
Type InitializationPhase is ADT with:
    Discovery       Note: Find and catalog modules
    Parsing         Note: Parse module syntax
    Dependency      Note: Resolve dependencies  
    TypeChecking    Note: Perform semantic analysis
    Initialization  Note: Execute module initialization code
    Registration    Note: Register exports in global namespace

Process called "initialize_module_system" that takes entry_point as String returns ModuleSystem:
    Let module_system be create_module_system()
    
    Note: Phase 1: Discovery
    Let discovered_modules be discover_modules_from_entry_point(entry_point)
    module_system.register_discovered_modules(discovered_modules)
    
    Note: Phase 2: Dependency analysis
    Let dependency_graph be build_module_dependency_graph(discovered_modules)
    Let circular_dependencies be detect_circular_dependencies(discovered_modules)
    
    If length of circular_dependencies is greater than 0:
        Throw CircularDependencyError with:
            message: "Circular dependencies detected"
            cycles: circular_dependencies
            resolution_suggestions: suggest_resolution_strategies(circular_dependencies)
    
    Note: Phase 3: Topological sort for initialization order
    Let initialization_order be topological_sort(dependency_graph)
    
    Note: Phase 4: Initialize modules in dependency order
    For each module_name in initialization_order:
        Let module be module_system.get_module(module_name)
        initialize_module(module, module_system)
    
    Return module_system

Note: Lazy module loading for performance
Process called "lazy_load_module" that takes module_name as String returns LazyModule:
    Return LazyModule with:
        name as module_name
        load_function as lambda: load_and_compile_module(module_name)
        cached_module as None
        
        Process called "get_module":
            If self.cached_module is None:
                Set self.cached_module to self.load_function()
            Return self.cached_module

Note: Module hot-reloading for development
Process called "enable_hot_reloading" that takes module_system as ModuleSystem:
    Let file_watcher be create_file_watcher()
    
    For each module in module_system.get_all_modules():
        file_watcher.watch_file with:
            file_path: module.source_file_path
            on_change: lambda: reload_module(module.name, module_system)
    
    file_watcher.start_watching()

Process called "reload_module" that takes module_name as String and system as ModuleSystem:
    Note: Identify modules that depend on the changed module
    Let dependent_modules be system.get_dependent_modules(module_name)
    
    Note: Reload in reverse dependency order
    Let reload_order be reverse_topological_sort(dependent_modules)
    
    For each dependent_module in reload_order:
        system.invalidate_module(dependent_module)
        system.reload_module(dependent_module)
    
    Display "Reloaded modules:" with message reload_order
```

#### Advanced Module Features

```runa
Note: Conditional module loading
Note: File: platform_specific.runa
When target_platform is "windows":
    Import module "windows_implementation" as impl
When target_platform is "linux":
    Import module "linux_implementation" as impl
When target_platform is "macos":
    Import module "macos_implementation" as impl
Otherwise:
    Import module "generic_implementation" as impl

Export impl.primary_function
Export impl.PlatformSpecificType

Note: Feature-gated modules
When feature_enabled("advanced_crypto"):
    Import module "advanced_crypto" as crypto
Otherwise:
    Import module "basic_crypto" as crypto

Export crypto.encrypt
Export crypto.decrypt

Note: Dynamic module loading
Process called "load_plugin" that takes plugin_name as String returns Optional[Module]:
    Try:
        Let plugin_path be resolve_plugin_path(plugin_name)
        Let plugin_module be load_module_from_path(plugin_path)
        
        Note: Validate plugin interface
        If not plugin_module.implements("PluginInterface"):
            Throw PluginValidationError with:
                message: "Plugin does not implement required interface"
                plugin: plugin_name
                expected_interface: "PluginInterface"
        
        Return Some(plugin_module)
    Catch err (ModuleLoadError):
        Display "Failed to load plugin:" with message plugin_name
        Return None

Note: Module sandboxing and security
Process called "create_sandboxed_module" that takes module_path as String returns SandboxedModule:
    Return SandboxedModule with:
        module_path as module_path
        permissions as SandboxPermissions with:
            file_access as ["read_only", module_path]
            network_access as "none"
            system_calls as "restricted"
            memory_limit as "64MB"
            execution_timeout as "30 seconds"
        
        Process called "execute_in_sandbox" that takes function_name as String and args as List[Any]:
            With security_context(self.permissions):
                Let module be load_module(self.module_path)
                Return module.call_function(function_name, args)

Note: Module metadata and reflection
Process called "get_module_metadata" that takes module as Module returns ModuleMetadata:
    Return ModuleMetadata with:
        name as module.name
        version as module.version
        exports as module.get_exported_symbols()
        imports as module.get_imported_modules()
        types as module.get_defined_types()
        functions as module.get_defined_functions()
        dependencies as module.get_dependencies()
        source_location as module.source_file_path
        compile_time as module.compilation_timestamp
        checksum as module.content_hash
```

### Export System

```runa
Note: Basic exports
Export function_definition
Export type_definition  
Export let_statement
Export define_statement

Note: Selective exports with visibility control
Export Public type UserAccount
Export Internal type DatabaseConnection  Note: Only visible to same package
Export Private helper_function           Note: Only visible to same module

Note: Re-exports and module composition
Import { external_function, ExternalType } from module "external_library"
Export external_function                 Note: Re-export imported function
Export ExternalType as LocalType         Note: Re-export with alias

Note: Conditional exports
When feature_enabled("debugging"):
    Export debug_utilities
    Export internal_state_inspector

When build_mode is "development":
    Export test_helpers
    Export mock_implementations
```

---

## Error Handling

### Exception Hierarchy

```runa
Type called "Error":
    message as String
    stack_trace as List[String]

Type called "RuntimeError" inherits from Error
Type called "TypeError" inherits from Error
Type called "ValueError" inherits from Error
Type called "FileNotFoundError" inherits from Error
Type called "NetworkError" inherits from Error
```

### Try-Catch-Finally

```ebnf
try_catch_statement   ::= "Try" ":" block
                         ("Catch" identifier? type_annotation? ":" block)+
                         ("Finally" ":" block)?
```

```runa
Try:
    Let content be read_file("config.json")
    Display "Configuration loaded"
Catch err (FileNotFoundError):
    Display "Error: Configuration file not found at " with message err.path
Catch err (Error):
    Display "An unknown error occurred: " with message err.message
Finally:
    Display "Cleanup completed"
```

### Result Types

```runa
Type Result[T, E] is T OR E

Process called "safe_operation" that takes value returns Result[Integer, String]:
    If value is greater than 0:
        Return value multiplied by 2
    Otherwise:
        Return "Invalid input: value must be positive"
```

### Async Error Handling

```runa
Async Process called "fetch_data" that takes url:
    Try:
        Let response be await http_get with url as url
        Return response
    Catch err (NetworkError):
        Display "Network error: " with message err.message
        Return None
```

---

## Concurrency Model

### Actor Model Implementation

Runa's concurrency is built on the Actor Model, providing safe, message-passing concurrency.

#### Async Processes (Actors)

```runa
Async Process called "counter_actor":
    Let count be 0
    Loop forever:
        Let message be Receive
        Match message:
            When "increment":
                Set count to count plus 1
            When "get_count":
                Display f"Count is {count}"
            When "shutdown":
                Break
```

#### Process Communication

```ebnf
spawn_expression      ::= "Spawn" function_call
send_statement        ::= "Send" expression "to" expression
receive_expression    ::= "Receive" ("from" expression)? ("timeout" expression)?
```

```runa
Note: Start the counter actor
Let counter_id be Spawn counter_actor()

Note: Send messages to it
Send "increment" to counter_id
Send "increment" to counter_id
Send "get_count" to counter_id
```

### Parallel Processing

```runa
@Execution_Model:
    mode: "parallel"
    concurrency: "thread_pool"
    max_workers: 8
@End_Execution_Model

Process called "parallel_map" that takes data and transform_func:
    Note: Automatically parallelized by runtime
    Let results be Map over data using transform_func
    Return results
```

### Synchronization Primitives

```runa
Note: Atomic operations
Let shared_counter be Atomic(0)
Set shared_counter to shared_counter plus 1

Note: Channels for communication
Let channel be Channel[String](capacity: 10)
Send "message" to channel
Let message be Receive from channel
```

---

## AI Notation System

Runa includes a comprehensive annotation system for AI-assisted development, enabling enhanced code documentation, reasoning, and intelligent code analysis.

Note: Bootstrap Compiler Conformance
The current bootstrap implementation routes the following annotation blocks as first-class statements: @Reasoning, @Implementation, @Uncertainty, @Request_Clarification, @KnowledgeReference, @TestCases, @Resource_Constraints, @Security_Scope, @Execution_Model, @Performance_Hints, @Progress, @Feedback, @Translation_Note, and @Error_Handling. Additional specified blocks (@Task, @Requirements, @Verify, @Request, @Context, @Collaboration, @Iteration, @Clarification) are recognized by the lexer and annotation type system and will be fully routed by the parser in a subsequent update. Keep using them for forward compatibility.

### Semantic Annotations

#### Reasoning Blocks

```runa
@Reasoning:
    The quicksort algorithm is preferred over merge sort in this case because:
    1. We have a small dataset that fits in memory
    2. The partial ordering of the data suggests good pivot selection
    3. The implementation is simpler and requires less additional memory
@End_Reasoning

Process called "sort_data" that takes data:
    Note: Implementation follows
```

#### Implementation Blocks

```runa
@Implementation:
    Process called "binary_search" that takes array and target:
        Let low be 0
        Let high be length of array minus 1
        
        While low is less than or equal to high:
            Let mid be (low plus high) divided by 2
            If array at index mid is equal to target:
                Return mid
            Otherwise if array at index mid is less than target:
                Set low to mid plus 1
            Otherwise:
                Set high to mid minus 1
        
        Return -1
@End_Implementation
```

### Uncertainty Representation

```runa
Process called "choose_sorting_algorithm" that takes data and size:
    If size is less than 100:
        Return ?[InsertionSort, BubbleSort, QuickSort] with confidence 0.8
    Otherwise if size is less than 10000:
        Return QuickSort with data as data
    Otherwise:
        Return ?MergeSort with data as data  Note: Lower confidence in this choice
```

### Knowledge References

```runa
@KnowledgeReference:
    concept: "Transformer Architecture"
    reference_id: "arxiv:1706.03762"
    version: "as of 2023-10"
@End_KnowledgeReference

Process called "build_transformer_model" that takes input_dim and output_dim:
    Note: Implementation based on the referenced paper
```

### Task Specifications

```runa
@Task:
    objective: "Create a web scraper for financial data"
    constraints: ["Must respect robots.txt", "Rate-limited to 1 request/second"]
    input_format: "URL list"
    output_format: "CSV with date, price, volume columns"
    target_language: "Python"
    priority: "Efficiency"
@End_Task

Process called "scrape_financial_data" that takes urls:
    Note: Implementation following the specifications
```

### Verification Framework

```runa
@Verify:
    Assert mean is greater than or equal to minimum value in data
    Assert mean is less than or equal to maximum value in data
    Assert standard_deviation is greater than or equal to 0
@End_Verify

Process called "calculate_statistics" that takes data:
    Note: Statistical calculations with built-in verification
```

### Resource and Security Traits

```runa
@Resource_Constraints:
    memory_limit: "512MB"
    cpu_limit: "4 cores"
    execution_timeout: "60 seconds"
    optimize_for: "speed"
    max_iterations: 50000
@End_Resource_Constraints

@Security_Scope:
    capabilities: ["file.read", "math.compute", "memory.local"]
    forbidden: ["net.access", "file.write", "system.execute"]
    sandbox_level: "strict"
    data_access: "read_only"
@End_Security_Scope

Process called "process_large_dataset" that takes data:
    Note: Compiler will enforce constraints and capabilities
    Let results be process_data with data as data
    Return results
```

---

## Foreign Function Interface

### External Function Declaration

```ebnf
external_function_declaration ::= "External" "Process" "called" identifier
                                 ("that" "takes" parameter_list)?
                                 ("returns" type_expression)?
                                 "from" "library" string_literal
                                 ("aliased" "as" string_literal)?
                                 ("convention" calling_convention)?
                                 ("unsafe")?

calling_convention            ::= "c" | "stdcall" | "fastcall" | "cdecl" | "syscall"
```

### Basic FFI Usage

```runa
Note: Import the 'sqrt' function from the standard C math library
External Process called "c_sqrt"
    that takes x (Float)
    returns Float
    from library "m"
    aliased as "sqrt"
    convention cdecl

Let result be c_sqrt(16.0)
Display f"The square root from C is {result}"  Note: Output: 4.0
```

### Advanced FFI Features

#### Struct Marshaling

```runa
Note: Define a C-compatible struct
Type Point is C_Struct with:
    x as Float
    y as Float
    layout packed

Note: Import function that takes struct by value
External Process called "distance_to_origin"
    that takes point as Point
    returns Float
    from library "geometry"
    convention c

Note: Import function that takes struct by pointer
External Process called "move_point"
    that takes point_ptr as Pointer[Point] and dx as Float and dy as Float
    from library "geometry"
    convention c
    unsafe
```

#### Array and Buffer Handling

```runa
Note: Fixed-size arrays
Type FloatArray10 is C_Array[Float, 10]

External Process called "process_array"
    that takes data as FloatArray10
    returns Float
    from library "math_utils"

Note: Dynamic arrays with explicit size
External Process called "sum_array"
    that takes data as Pointer[Float] and size as Integer
    returns Float
    from library "math_utils"
    unsafe

Note: Usage with safety checks
Process called "safe_sum_array" that takes values as List[Float] returns Float:
    Let size be length of values
    With array_ptr as allocate_array(values):
        Return sum_array with data as array_ptr and size as size
```

#### Callback Functions

```runa
Note: Define callback type
Type CompareCallback is C_Function[Integer, Pointer[Any], Pointer[Any]]

Note: Import function that takes callback
External Process called "qsort"
    that takes base as Pointer[Any] and count as Integer and size as Integer and compare as CompareCallback
    from library "c"
    convention c
    unsafe

Note: Implement callback in Runa
Process called "compare_integers" that takes a_ptr as Pointer[Any] and b_ptr as Pointer[Any] returns Integer:
    Let a be dereference a_ptr as Integer
    Let b be dereference b_ptr as Integer
    If a is less than b:
        Return -1
    Otherwise if a is greater than b:
        Return 1
    Otherwise:
        Return 0
```

### C Calling Conventions

#### Convention Specifications

```
C Convention (default):
- Arguments passed in: RDI, RSI, RDX, RCX, R8, R9, then stack
- Return value in: RAX (integers), XMM0 (floats)
- Caller cleans up stack
- Red zone: 128 bytes below RSP

Stdcall Convention (Windows):
- Arguments pushed right-to-left on stack
- Callee cleans up stack
- Return value in EAX/RAX
- Used by Windows API functions

Fastcall Convention:
- First two arguments in ECX, EDX
- Remaining arguments on stack
- Callee cleans up stack
- Optimized for speed

Syscall Convention:
- Arguments in: RAX, RDI, RSI, RDX, R10, R8, R9
- System call number in RAX
- Return value in RAX
- Used for kernel system calls
```

### Library Linking Mechanisms

#### Static Linking

```runa
Note: Link static library at compile time
External Process called "static_function"
    from library "libstatic.a"
    link_type static

Note: Specify library search paths
Set library_path to list containing "/usr/local/lib", "/opt/lib"
```

#### Dynamic Linking

```runa
Note: Load shared library at runtime
External Process called "dynamic_function"
    from library "libdynamic.so"
    link_type dynamic
    lazy_load true

Note: Handle loading failures
Try:
    Let result be dynamic_function with arg as value
Catch library_error:
    Display "Failed to load library: " with message library_error.message
```

#### Platform-Specific Libraries

```runa
Note: Platform-specific library selection
When running on "windows":
    External Process called "platform_function"
        from library "platform.dll"
When running on "linux":
    External Process called "platform_function"
        from library "libplatform.so"
When running on "macos":
    External Process called "platform_function"
        from library "libplatform.dylib"
```

### Comprehensive Type Marshaling

#### Primitive Type Mapping

```
Runa Type     → C Type           → Description
─────────────────────────────────────────────────
Integer       → int64_t          → 64-bit signed integer
Float         → double           → 64-bit IEEE 754 float
Boolean       → bool             → 8-bit boolean (0/1)
Character     → char             → 8-bit character
String        → const char*      → UTF-8 null-terminated string
Byte          → uint8_t          → 8-bit unsigned integer

Pointer[T]    → T*               → Pointer to type T
Array[T, N]   → T[N]             → Fixed-size array
Buffer[T]     → T*               → Dynamic buffer
Void          → void             → No return value
```

#### Complex Type Marshaling

```runa
Note: Optional types become nullable pointers
Type OptionalInt is Integer OR None
Note: Marshals to: int64_t* (NULL for None)

Note: Union types require manual handling
Type IntOrFloat is Integer OR Float
Note: Requires explicit variant handling in FFI

Note: String marshaling options
External Process called "string_function"
    that takes text as String[utf8]        Note: UTF-8 encoding
    Note: that takes text as String[utf16]     Note: UTF-16 encoding  
    Note: that takes text as String[ascii]     Note: ASCII encoding
    from library "text_lib"
```

#### Memory Management in FFI

```runa
Note: Automatic memory management
External Process called "get_string"
    returns String[owned]    Note: Runa takes ownership, will free
    from library "string_lib"

External Process called "borrow_string"
    returns String[borrowed] Note: C retains ownership, Runa won't free
    from library "string_lib"

Note: Manual memory management
External Process called "allocate_buffer"
    that takes size as Integer
    returns Pointer[Byte][allocated]  Note: Must be manually freed
    from library "memory_lib"
    unsafe

External Process called "free_buffer"
    that takes ptr as Pointer[Byte]
    from library "memory_lib"
    unsafe

Note: RAII wrapper for safe usage
Process called "with_buffer"[T] that takes size as Integer and action as Function[Pointer[Byte], T] returns T:
    Let buffer be allocate_buffer with size as size
    Try:
        Return action with ptr as buffer
    Finally:
        free_buffer with ptr as buffer
```

### Platform-Specific Considerations

#### Windows Considerations

```runa
Note: Wide string support for Windows API
Type WideString is String[utf16]

External Process called "MessageBoxW"
    that takes hwnd as Pointer[Void] and text as WideString and caption as WideString and type as Integer
    returns Integer
    from library "user32.dll"
    convention stdcall

Note: COM interface support
Type IUnknown is COM_Interface with:
    QueryInterface as Function[Pointer[Void], Pointer[Pointer[Void]], Integer]
    AddRef as Function[Integer]
    Release as Function[Integer]
```

#### Unix/Linux Considerations

```runa
Note: POSIX function support
External Process called "pthread_create"
    that takes thread as Pointer[Pointer[Void]] and attr as Pointer[Void] and start_routine as Function[Pointer[Void], Pointer[Void]] and arg as Pointer[Void]
    returns Integer
    from library "pthread"
    convention c

Note: File descriptor handling
Type FileDescriptor is Integer[resource]  Note: Automatically closed on scope exit

External Process called "open"
    that takes pathname as String and flags as Integer
    returns FileDescriptor[checked]  Note: Returns error on failure
    from library "c"
```

#### macOS Considerations

```runa
Note: Objective-C bridge support
Type NSString is ObjC_Class

External Process called "NSStringFromClass"
    that takes cls as ObjC_Class
    returns NSString
    from library "Foundation"
    convention objc

Note: Framework loading
External Process called "framework_function"
    from framework "CoreFoundation"
    convention c
```

### Error Handling in FFI

#### Error Code Handling

```runa
Note: Function that returns error codes
External Process called "risky_operation"
    that takes input as Integer
    returns Integer[error_code]  Note: Special error code type
    from library "unsafe_lib"

Process called "safe_risky_operation" that takes input as Integer returns Result[Integer, String]:
    Let result be risky_operation with input as input
    Match result:
        When error_code 0:
            Return Success with value as result
        When error_code -1:
            Return Failure with error as "Invalid input"
        When error_code -2:
            Return Failure with error as "Operation failed"
        When _:
            Return Failure with error as f"Unknown error: {result}"
```

#### Exception Safety

```runa
Note: C functions that might call back into Runa
External Process called "callback_user"
    that takes callback as Function[Integer, Integer]
    from library "callback_lib"
    exception_safe  Note: Handles Runa exceptions

Note: Callback that might throw
Process called "throwing_callback" that takes value as Integer returns Integer:
    If value is less than 0:
        Throw ValueError with message "Negative input not allowed"
    Return value multiplied by 2

Note: Safe usage
Try:
    Let result be callback_user with callback as throwing_callback
    Display "Result: " with message result
Catch callback_error:
    Display "Callback error: " with message callback_error.message
```

### FFI Best Practices

#### Safety Guidelines

```runa
Note: 1. Always validate pointers before dereferencing
Process called "safe_dereference"[T] that takes ptr as Pointer[T] returns Optional[T]:
    If ptr is null:
        Return None
    Return Some with value as (dereference ptr)

Note: 2. Use RAII for resource management
Process called "with_file" that takes filename as String and mode as String and action as Function[Pointer[File], Any]:
    Let file_ptr be fopen with filename as filename and mode as mode
    If file_ptr is null:
        Throw FileError with message "Could not open file"
    Try:
        Return action with file as file_ptr
    Finally:
        fclose with file as file_ptr

Note: 3. Validate string encodings
Process called "safe_string_pass" that takes text as String returns String:
    If not is_valid_utf8(text):
        Throw EncodingError with message "Invalid UTF-8 string"
    Return c_function_expecting_utf8 with text as text
```

### Safety Considerations

#### Memory Safety

1. **Pointer Validation**: Always check for null pointers before dereferencing
2. **Buffer Bounds**: Validate array bounds when passing buffers to C
3. **Ownership Tracking**: Clear ownership semantics for allocated memory
4. **Lifetime Management**: Ensure C pointers don't outlive Runa objects

#### Type Safety

1. **ABI Compatibility**: Ensure struct layouts match C expectations
2. **Calling Convention**: Use correct calling convention for target platform
3. **Type Size Validation**: Verify type sizes match across language boundaries
4. **Endianness Handling**: Consider byte order for binary data exchange

#### Threading Safety

1. **Thread Local Storage**: Handle TLS differences between languages
2. **Lock Ordering**: Avoid deadlocks when crossing language boundaries
3. **Signal Safety**: Be careful with signal handlers in mixed code
4. **Exception Propagation**: Handle exceptions across language boundaries safely

---

## Standard Library

### Core Collections

```runa
Note: List operations
Let numbers be list containing 1, 2, 3, 4, 5
Let doubled be Map over numbers using lambda x: x multiplied by 2
Let evens be Filter numbers where lambda x: x modulo 2 equals 0
Let sum be Reduce numbers using lambda acc and x: acc plus x

Note: Dictionary operations
Let user be dictionary with:
    "name" as "Alice"
    "age" as 30
    "email" as "alice@example.com"

Note: String operations
Let greeting be "Hello, " joined with user["name"]
Let length be length of greeting
Let uppercase be greeting converted to uppercase
```

### Operators

Within the triple-syntax system, operators have dual forms (natural and symbolic) with **mathematical symbol enforcement** — symbols are restricted to mathematical contexts only.

#### Mathematical Symbol Enforcement

**IMPORTANT**: Mathematical symbols (`+`, `-`, `*`, `/`, `%`, `**`, `<`, `>`, `<=`, `>=`, `!=`, `==`) are **ONLY** permitted in mathematical contexts. The compiler enforces this restriction.

**Valid Mathematical Contexts**:
- Arithmetic expressions with numeric operands
- Mathematical comparisons between numbers
- Mathematical operations in expressions

**Invalid Non-Mathematical Contexts**:
- String operations (use "joined with")
- Boolean logic (use "and", "or", "not")
- Assignment operations (use "be", "as", "to")

#### Arithmetic Operators
Both forms supported (symbols restricted to mathematical contexts):

- `+` ↔ `plus` (mathematical only)
- `-` ↔ `minus` (mathematical only)
- `*` ↔ `multiplied by` (mathematical only)
- `/` ↔ `divided by` (mathematical only)
- `%` ↔ `modulo` (mathematical only)
- `**` ↔ `to the power of` (mathematical only)

#### Comparison Operators
Both forms supported (symbols restricted to mathematical contexts):

- `<` ↔ `is less than` (mathematical comparison only)
- `>` ↔ `is greater than` (mathematical comparison only)
- `<=` ↔ `is less than or equal to` (mathematical comparison only)
- `>=` ↔ `is greater than or equal to` (mathematical comparison only)
- `!=` ↔ `is not equal to` (mathematical comparison only)
- `==` ↔ `is equal to` (mathematical comparison only)
- `=` ↔ `equals` (assignment only)

#### Equality Operators
Runa provides a dual-syntax approach for equality that balances natural language readability with technical efficiency:

**Canonical Natural Language Syntax (Recommended):**
- `is equal to` - The primary operator for non-mathematical equality comparisons
- Example: `If name is equal to "Admin"` or `If the day is equal to "Monday"`

**Technical Shorthand (Alternative):**
- `equals` - Concise, functionally identical alternative for experienced developers
- Example: `If name is equal to "Admin"` or `If the day is equal to "Monday"`

Both operators produce identical results and can be used interchangeably. The canonical syntax emphasizes natural language readability, while the technical shorthand provides conciseness for rapid development.

#### Identity and Type Operators
The `is` keyword is reserved exclusively for identity, type, and state checks. It does **not** perform general value equality comparisons.

**Identity Checks:**
- `is None` - Check if a value is the null reference
- `is empty` - Check if a collection or string is empty
- `is null` - Alternative null check (synonym for `is None`)

**Type Checks:**
- `is of type String` - Check if a value is of a specific type
- `is of type Integer` - Type validation for integers
- `is of type Boolean` - Boolean type checking

**State Checks:**
- `is empty` - Check if a collection has no elements
- `is valid` - Check if a value is in a valid state
- `is ready` - Check if a resource is ready for use

**Important:** The `is` operator performs reference equality and type checking, not value equality. For value comparisons, use `is equal to` or `equals`.

#### Compound Assignment Operators

Runa provides natural language forms for compound assignments that modify variables in place:

**Infix Forms (modify and return new value):**
- `+=` ↔ `gets increased by` - Increases the variable by a value
- `-=` ↔ `gets decreased by` - Decreases the variable by a value
- `*=` ↔ `gets multiplied by` - Multiplies the variable by a value
- `/=` ↔ `gets divided by` - Divides the variable by a value

**Imperative Statement Forms (also available):**
- `Increase <variable> by <value>` - Equivalent to variable += value
- `Decrease <variable> by <value>` - Equivalent to variable -= value
- `Multiply <variable> by <value>` - Equivalent to variable *= value
- `Divide <variable> by <value>` - Equivalent to variable /= value

Examples:
```runa
Note: Infix forms
Set count to count gets increased by 1
Set total to total gets multiplied by tax_rate

Note: Imperative forms
Increase count by 1
Decrease health by damage
Multiply price by discount_factor
Divide total by num_items
```

#### Member Access Operators

Runa provides two natural language forms for member access, both equivalent to the dot operator:

- `.` ↔ `of` - Suggests possession or property
- `.` ↔ `from` - Suggests source or origin

Examples:
```runa
Note: Using 'of' for properties
Let area be area of circle
Let name be name of student

Note: Using 'from' for module/namespace access
Let pi be PI from Math
Let list be List from collections

Note: Symbol form in developer mode
Let area be circle.area
Let pi be Math.PI
```

#### Range Operators

Runa provides natural language forms for creating ranges:

- `..` ↔ `through` - Creates a range excluding the end value
- `..=` ↔ `up to and including` - Creates a range including the end value

Examples:
```runa
Note: Exclusive range (1, 2, 3, 4)
For i in 1 through 5:
    Display i
End For

Note: Inclusive range (1, 2, 3, 4, 5)
For i in 1 up to and including 5:
    Display i
End For
```

#### Index Access Operator

For array and dictionary indexing:

- `[]` ↔ `at` - Accesses element at index or key

Examples:
```runa
Note: Array indexing
Let first be array at 0
Let last be array at (length of array) minus 1

Note: Dictionary access
Let value be config at "setting"
Let user be users at user_id

Note: Symbol form in developer mode
Let first be array[0]
Let value be config["setting"]
```

#### Operator Type Classifications

- **Mathematical**: `+`, `-`, `*`, `/`, `%`, `**`, `plus`, `minus`, `multiplied by`, `divided by`, `modulo`, `to the power of`
- **Mathematical Comparison**: `<`, `>`, `<=`, `>=`, `!=`, `==`, `is greater than`, `is less than`, `is greater than or equal to`, `is less than or equal to`, `is not equal to`, `is equal to`
- **Compound Assignment**: `+=`, `-=`, `*=`, `/=`, `gets increased by`, `gets decreased by`, `gets multiplied by`, `gets divided by`
- **Member Access**: `.`, `of`, `from`
- **Range**: `..`, `..=`, `through`, `up to and including`
- **Index Access**: `[]`, `at`
- **Equality Comparison**: `is equal to`, `equals`, `contains`, `is in`
- **Identity and Type**: `is of type`, `is None`, `is empty`, `is null`, `is valid`, `is ready`
- **Bitwise**: `bitwise and`, `bitwise or`, `bitwise xor`, `bitwise not`, `shifted left by`, `shifted right by`
- **Logical**: `and`, `or`, `not`, `logical and`, `logical or`, `logical not`
- **String**: `joined with`

### Mathematical Operations

```runa
Note: Mathematical symbols ONLY in mathematical contexts
Let total be price + tax                    Note: Valid - mathematical context
Let total be price plus tax                 Note: Always valid - natural language
Let discount be price * 0.1                 Note: Valid - mathematical context  
Let discount be price multiplied by 0.1     Note: Always valid - natural language
Let average be sum / count                  Note: Valid - mathematical context
Let average be sum divided by count         Note: Always valid - natural language

Note: Advanced math
Let sqrt_value be sqrt(16.0)
Let power_value be 2 to the power of 8
Let sin_value be sin(3.14159 / 2)           Note: Valid - mathematical context
Let sin_value be sin(3.14159 divided by 2)  Note: Always valid - natural language

Note: NON-mathematical contexts must use natural language
Let full_name be first_name joined with " " joined with last_name
Note: Using + for strings would be INVALID
```

### Symbol-to-Word Conversion

The formatter automatically converts mathematical symbols to natural language unless configured otherwise:

```runa
Note: Formatter conversion rules
+ → plus
- → minus
* → multiplied by
/ → divided by
<= → is less than or equal to
>= → is greater than or equal to
!= → is not equal to
== → is equal to
= → equals
```

### I/O Operations

```runa
Note: File operations
Let content be read file "data.txt"
Write content to file "output.txt"
Let exists be file exists "config.json"

Note: Console I/O
Let user_input be input with prompt "Enter your name: "
Display "Hello, " with message user_input

Note: Network operations
Let response be http get with url "https://api.example.com/data"
Let json_data be parse json from response
```

### Time and Date

```runa
Let current_time be current timestamp
Let formatted_date be format time current_time as "YYYY-MM-DD"
Let tomorrow be current_time plus 1 day
```

---

## Runtime Environment

### Execution Model (AOTT - All-of-The-Time)

Runa uses the AOTT execution architecture as the single execution model. Transpilation or compilation are implementation strategies, whereas execution semantics are defined by AOTT’s tiered system:

1. Tier 0: Lightning Interpreter (fast startup, profiling hooks)
2. Tier 1: Smart Bytecode Execution (inline caching, basic optimizations)
3. Tier 2: Basic Native Execution (LLVM-based, code caching)
4. Tier 3: Optimized Native Execution (aggressive optimizations)
5. Tier 4: Speculative Execution (validated speculation with deoptimization)

See `docs/plans/RUNA_AOTT_ARCHITECTURE_PLAN.md` for authoritative architecture details.

### Bytecode and Engines in AOTT

#### Bytecode Format Specification

```
Runa Bytecode Format (.rbc):

Header (16 bytes):
  Magic Number: 0x52554E41 ("RUNA")
  Version: 2 bytes (major.minor)
  Flags: 2 bytes (optimization level, debug info)
  Constant Pool Size: 4 bytes
  Code Section Size: 4 bytes

Constant Pool:
  Entry Count: 4 bytes
  Entries: Variable length
    Type Tag: 1 byte (0x01=Integer, 0x02=Float, 0x03=String, 0x04=Function)
    Data: Variable length based on type

Code Section:
  Instruction Count: 4 bytes
  Instructions: Variable length
    Opcode: 1 byte
    Operands: 0-3 bytes depending on instruction
```

#### Instruction Set Architecture

```
Core Instructions (32 opcodes):
  0x00: NOP           - No operation
  0x01: LOAD_CONST    - Load constant from pool
  0x02: LOAD_LOCAL    - Load local variable
  0x03: STORE_LOCAL   - Store to local variable
  0x04: LOAD_GLOBAL   - Load global variable
  0x05: STORE_GLOBAL  - Store to global variable
  
Arithmetic Operations:
  0x10: ADD           - Add top two stack values
  0x11: SUB           - Subtract top two stack values
  0x12: MUL           - Multiply top two stack values
  0x13: DIV           - Divide top two stack values
  0x14: MOD           - Modulo operation
  0x15: POW           - Power operation
  
Control Flow:
  0x20: JUMP          - Unconditional jump
  0x21: JUMP_IF_TRUE  - Jump if top of stack is true
  0x22: JUMP_IF_FALSE - Jump if top of stack is false
  0x23: CALL          - Function call
  0x24: RETURN        - Return from function
  
Memory Operations:
  0x30: NEW_LIST      - Create new list
  0x31: NEW_DICT      - Create new dictionary
  0x32: GET_INDEX     - Get item by index
  0x33: SET_INDEX     - Set item by index
  0x34: GET_ATTR      - Get object attribute
  0x35: SET_ATTR      - Set object attribute
```

### Memory Management System

#### Hybrid ARC/GC Implementation

```
Memory Layout:
┌─────────────────┐
│   Stack         │ ← Local variables, function calls
├─────────────────┤
│   Young Gen     │ ← Short-lived objects (ARC)
├─────────────────┤
│   Old Gen       │ ← Long-lived objects (Mark & Sweep)
├─────────────────┤
│   Large Objects │ ← Objects > 64KB
└─────────────────┘

Reference Counting (ARC):
- Immediate deallocation for non-cyclic references
- Fast allocation/deallocation for temporary objects
- Zero-cost for single-ownership scenarios

Garbage Collection:
- Generational collection for cycle breaking
- Mark & Sweep for old generation
- Concurrent collection to minimize pauses
- Write barriers for generational integrity
```

#### Memory Allocation Strategy

```
Small Objects (< 256 bytes):
  - Pool allocator with size classes
  - Thread-local allocation buffers
  - Bump pointer allocation within pools

Medium Objects (256B - 64KB):
  - Best-fit allocator with coalescing
  - Segregated free lists by size
  - Lazy coalescing to reduce fragmentation

Large Objects (> 64KB):
  - Direct system allocation (mmap/VirtualAlloc)
  - Out-of-line metadata storage
  - Immediate deallocation when unreferenced
```

### Thread Scheduler and Concurrency Runtime

#### Actor-Based Concurrency

```
Scheduler Architecture:
┌─────────────────┐
│  Work Stealing  │ ← Thread pool with work stealing
│  Thread Pool    │
├─────────────────┤
│  Actor System   │ ← Message-based actor runtime
├─────────────────┤
│  Message Queues │ ← Lock-free MPSC queues
└─────────────────┘

Actor Lifecycle:
1. Spawn: Create actor and allocate resources
2. Schedule: Add to runnable queue
3. Execute: Process messages until queue empty
4. Park: Remove from scheduler when idle
5. Terminate: Clean up resources and notify dependents
```

#### Message Passing Implementation

```
Message Format:
┌─────────────────┐
│ Sender ID       │ 4 bytes
├─────────────────┤
│ Receiver ID     │ 4 bytes
├─────────────────┤
│ Message Type    │ 2 bytes
├─────────────────┤
│ Data Length     │ 4 bytes
├─────────────────┤
│ Payload         │ Variable
└─────────────────┘

Queue Implementation:
- Lock-free Multiple Producer Single Consumer (MPSC)
- Batch message processing to reduce context switches
- Priority lanes for urgent messages
- Backpressure handling for queue overflow
```

### Exception Handling Runtime

#### Exception Object Layout

```
Exception Structure:
┌─────────────────┐
│ Exception Type  │ 4 bytes (type ID)
├─────────────────┤
│ Message Ptr     │ 8 bytes (string pointer)
├─────────────────┤
│ Stack Trace Ptr │ 8 bytes (trace array pointer)
├─────────────────┤
│ Cause Ptr       │ 8 bytes (nested exception)
├─────────────────┤
│ Custom Data     │ Variable (exception-specific)
└─────────────────┘

Stack Unwinding:
1. Exception thrown sets unwinding flag
2. Each function checks flag on return
3. Destructors called for local objects
4. Stack frames deallocated
5. Exception handler located and called
```

#### Exception Propagation

```
Try-Catch Implementation:
- Exception tables map PC ranges to handlers
- Stack unwinding preserves exception object
- Handler matching by type hierarchy
- Finally blocks executed during unwinding
- Exception re-throwing preserves original stack trace
```

### Debugging Infrastructure

#### Debug Information Format

```
Debug Info Sections:
.debug_info:     Type information and variable metadata
.debug_line:     Source line to bytecode mapping
.debug_frame:    Stack frame unwinding information
.debug_ranges:   Code ranges for optimization boundaries

Symbol Table Format:
┌─────────────────┐
│ Symbol Name     │ Variable length string
├─────────────────┤
│ Symbol Type     │ 1 byte (var/func/type)
├─────────────────┤
│ Scope Start     │ 4 bytes (bytecode offset)
├─────────────────┤
│ Scope End       │ 4 bytes (bytecode offset)
├─────────────────┤
│ Type Info       │ 4 bytes (type table index)
└─────────────────┘
```

#### Debugger Protocol

```
Debug Commands:
- BREAK_SET <file:line>     Set breakpoint
- BREAK_CLEAR <id>          Clear breakpoint
- STEP_INTO                 Step into function calls
- STEP_OVER                 Step over function calls
- STEP_OUT                  Step out of current function
- CONTINUE                  Resume execution
- EVAL <expression>         Evaluate expression in current context
- STACK_TRACE               Get current call stack
- VAR_LIST                  List variables in current scope
- VAR_GET <name>            Get variable value
- VAR_SET <name> <value>    Set variable value
```

### Platform Integration

```runa
Note: Platform-specific code
When running on "windows":
    Let path_separator be "\\"
    Let executable_extension be ".exe"
    Let library_extension be ".dll"
When running on "unix":
    Let path_separator be "/"
    Let executable_extension be ""
    Let library_extension be ".so"
When running on "macos":
    Let path_separator be "/"
    Let executable_extension be ""
    Let library_extension be ".dylib"

Note: Environment variables
Let home_directory be environment variable "HOME"
Let debug_mode be environment variable "DEBUG" defaults to "false"
Let runa_path be environment variable "RUNA_PATH" defaults to "/usr/local/lib/runa"
```

### Performance Characteristics

#### Compilation Performance

```
Compilation Pipeline Performance:
- Lexical Analysis: ~1M lines/second
- Syntax Analysis: ~500K lines/second
- Semantic Analysis: ~200K lines/second
- Code Generation: ~100K lines/second
- Optimization: ~50K lines/second

Incremental Compilation:
- Only recompile changed modules and dependents
- Dependency graph caching
- Parallel compilation of independent modules
- Hot reloading in development mode
```

#### Runtime Performance (AOTT)

```
Execution Performance Targets:
- Startup Time: < 50ms for typical applications
- Memory Overhead: < 10MB base runtime
- GC Pause Time: < 10ms for 95th percentile
- Function Call Overhead: < 5ns for direct calls
- Message Passing: < 100ns per message

Optimization Characteristics under AOTT:
- Tier promotion based on profiles
- Devirtualization of polymorphic calls
- Dead code elimination
- Constant folding and propagation
- Speculative optimization with guard validation and deoptimization
```

---

## Language Feature Extensions

### Pattern Matching (Advanced)

```runa
Note: Destructuring with guards
Match user_data:
    When { "type": "admin", "permissions": perms } where length of perms is greater than 5:
        Display "Super admin detected"
    When { "type": user_type, "name": name } where name starts with "test":
        Display "Test user: " with message name
    When _:
        Display "Regular user"
```

### Functional Programming

#### Pipeline Operator

```runa
Let result be input_data
    |> validate_data
    |> transform_data
    |> filter_valid_items
    |> calculate_results
```

#### Higher-Order Functions

```runa
Note: Currying and partial application
Let add be lambda x: lambda y: x plus y
Let add_five be add(5)
Let result be add_five(10)  Note: Result is 15

Note: Function composition
Let process_pipeline be compose(
    validate_data,
    transform_data,
    save_results
)
```

### Asynchronous Programming

```runa
Note: Async/await with error handling
Async Process called "fetch_multiple_urls" that takes urls:
    Let results be list containing
    
    For each url in urls:
        Try:
            Let response be await http_get with url as url
            Add response to results
        Catch err (NetworkError):
            Add None to results
    
    Return results

Note: Concurrent execution
Let futures be list containing
For each url in urls:
    Add (Spawn fetch_data with url as url) to futures

Let results be await all futures
```

### Metaprogramming and Macro System

#### Compile-Time Code Generation

```runa
Note: Derive common functionality
@Derive(Clone, Debug, PartialEq, Hash)
Type User is Record with:
    id as Integer
    name as String
    email as String

Note: Template-based code generation
@Template("crud_operations")
Type UserRepository is with entity_type as User

Note: Custom attribute macros
@Validate_Fields(required=["name", "email"], max_length={"name": 50})
Type CreateUserRequest is Record with:
    name as String
    email as String
    age as Optional(Integer)
```

#### Macro Definition and Usage

```runa
Note: Define macro for logging
Macro called "debug_log" that takes message and variables:
    If compilation_mode is "debug":
        Return Display "[DEBUG]" with message message with " - " with variables
    Otherwise:
        Return Note: No-op in release mode

Note: Use macro
debug_log("Processing user", {user_id: user.id, timestamp: now()})

Note: Macro with multiple statements
Macro called "time_execution" that takes block:
    Return:
        Let start_time be current_timestamp()
        Let result be block
        Let end_time be current_timestamp()
        Let duration be end_time minus start_time
        Display "Execution time:" with duration with "ms"
        Return result

Note: Usage with block
Let result be time_execution:
    expensive_calculation()
    process_data()
    save_results()
```

#### Compile-Time Evaluation

```runa
Note: Compile-time constants
Const PI be 3.14159265359
Const MAX_USERS be 1000
Const BUILD_VERSION be compile_time_eval(read_version_from_file())

Note: Compile-time expressions
Let buffer_size be compile_time_eval(MAX_USERS multiplied by 8)
```

### Reflection and Introspection

#### Type Reflection

```runa
Note: Type information at runtime
Let user_type be typeof(User)
Display "Type name:" with user_type.name
Display "Fields:" with user_type.fields

Note: Field introspection
For each field in user_type.fields:
    Display "Field:" with field.name with "Type:" with field.type

Note: Method introspection
For each method in user_type.methods:
    Display "Method:" with method.name with "Parameters:" with method.parameters
```

#### Dynamic Type Operations

```runa
Note: Create instances dynamically
Let user_class be get_type_by_name("User")
Let user_instance be user_class.create_instance()
user_instance.set_field("name", "John Doe")
user_instance.set_field("age", 30)

Note: Call methods dynamically
Let method be user_class.get_method("validate")
Let is_valid be method.invoke(user_instance)

Note: Check type relationships
If user_instance.is_instance_of(Person):
    Display "User is a Person"

If user_class.implements_interface(Serializable):
    Let json_data be user_instance.to_json()
```

#### Attribute and Annotation Reflection

```runa
Note: Query attributes
Let validation_attrs be user_type.get_attributes("Validate")
For each attr in validation_attrs:
    Let rules be attr.get_parameter("rules")
    apply_validation_rules(user_instance, rules)

Note: Code generation metadata
Let generated_methods be user_type.get_generated_methods()
For each method in generated_methods:
    Display "Generated method:" with method.name
```

### Conditional Compilation

#### Platform-Specific Code

```runa
Note: Conditional compilation directives
@If(target_platform == "windows")
Process called "get_system_info":
    Import "windows.system" as sys
    Return sys.get_windows_info()

@ElseIf(target_platform == "linux")
Process called "get_system_info":
    Import "posix.system" as sys
    Return sys.get_unix_info()

@Else
Process called "get_system_info":
    Return "Unknown platform"
@EndIf

Note: Feature flags
@If(feature_enabled("advanced_logging"))
Process called "log_detailed_info" that takes data:
    Note: Detailed logging implementation
    log_with_stack_trace(data)
    log_performance_metrics(data)
@Else
Process called "log_detailed_info" that takes data:
    Note: Simple logging fallback
    Display data
@EndIf
```

#### Environment-Based Configuration

```runa
Note: Development vs Production
@If(build_mode == "development")
Const API_BASE_URL be "http://localhost:3000"
Const DEBUG_ENABLED be True
Const LOG_LEVEL be "DEBUG"

@ElseIf(build_mode == "staging")
Const API_BASE_URL be "https://staging.api.example.com"
Const DEBUG_ENABLED be True
Const LOG_LEVEL be "INFO"

@Else
Const API_BASE_URL be "https://api.example.com"
Const DEBUG_ENABLED be False
Const LOG_LEVEL be "ERROR"
@EndIf

Note: Target language specific implementations
@If(target_language == "python")
Process called "parallel_map" that takes func and iterable:
    Import "multiprocessing" as mp
    With mp.Pool() as pool:
        Return pool.map(func, iterable)

@ElseIf(target_language == "javascript")
Process called "parallel_map" that takes func and iterable:
    Return Promise.all(iterable.map(func))

@ElseIf(target_language == "java")
Process called "parallel_map" that takes func and iterable:
    Return iterable.parallelStream().map(func).collect(toList())
@EndIf
```

#### Version-Based Features

```runa
Note: API version compatibility
@If(api_version >= "2.0")
Type UserRequest is Record with:
    id as UUID
    name as String
    email as Email
    preferences as UserPreferences

@Else
Type UserRequest is Record with:
    id as Integer
    name as String
    email as String
@EndIf

Note: Language feature detection
@If(supports_async_await)
Async Process called "fetch_data" that takes url:
    Return await http_client.get(url)

@Else
Process called "fetch_data" that takes url:
    Return http_client.get_sync(url)
@EndIf
```

### Advanced Functional Programming

#### Monads and Effect Systems

```runa
Note: Maybe/Option monad
Type Maybe(T) is ADT with:
    Some(value as T)
    None

Note: Result type for error handling
Type Result(T, E) is ADT with:
    Ok(value as T)
    Error(error as E)

Note: Monad operations
Process called "bind" that takes maybe and func:
    Match maybe:
        When Some(value):
            Return func(value)
        When None:
            Return None

Note: Do notation for monadic composition
Do:
    Let user be get_user(user_id)?
    Let profile be get_profile(user.profile_id)?
    Let settings be get_settings(profile.settings_id)?
    Return settings.theme
```

#### Type-Level Programming

```runa
Note: Generic constraints with type-level predicates
Process called "sort_collection" that takes collection where T implements Comparable(T):
    Note: Type system ensures T can be compared
    Return collection.sort()

Note: Associated types and type families
Protocol Iterable(T) with:
    Type Item
    Process iterate returns Iterator(Item)

Note: Higher-kinded types
Type Functor(F) is Protocol with:
    Process map that takes func and fa returns F(B) where fa is F(A) and func is A -> B
```

---

## Implementation Notes

### Compiler Architecture

1. **Lexical Analysis**: Tokenization with multi-word identifier support
2. **Syntax Analysis**: Recursive descent parser with error recovery
3. **Semantic Analysis**: Type checking, symbol resolution, constraint verification
4. **Code Generation**: Target-language specific code generators
5. **Optimization**: Dead code elimination, constant folding, inlining

### Target Language Support

- **Tier 1**: Python, JavaScript, TypeScript, Java, C++, C#, SQL
- **Tier 2**: Go, Rust, Kotlin, Swift, PHP, Scala, WebAssembly
- **Tier 3**: CSS, HTML, JSON, YAML, XML, TOML, Shell, Lua
- **Tier 4**: Solidity, Move, GraphQL, Julia, R, MATLAB
- **Tier 5**: Haskell, OCaml, Clojure, Erlang, Elixir, Assembly, LLVM IR
- **Tier 6**: COBOL, Fortran, Ada, Perl, TCL, Visual Basic, Objective-C
- **Tier 7**: CUDA, OpenCL, CMake, Make, Nix, Bazel

### Development Phases

1. **Phase 1**: Core language design (✅ Completed)
2. **Phase 2**: Basic implementation with self-hosting (✅ Current)
3. **Phase 3**: Advanced features and tooling (🔄 In Progress)
4. **Phase 4**: AI integration and knowledge systems (✅ Completed)
5. **Phase 5**: Production optimization and ecosystem (✅ Completed)

---

## Conclusion

Runa represents a paradigm shift in programming language design, prioritizing human readability while maintaining computational precision. Its AI-first design philosophy, comprehensive type system, and universal translation capabilities make it an ideal bridge between human reasoning and machine execution.

The language's unique combination of natural syntax, modern programming features, and specialized AI notation constructs positions it as a powerful tool for the next generation of software development, particularly in AI-assisted environments where enhanced code documentation and reasoning capabilities enable more effective collaboration.

This specification serves as the definitive reference for Runa language implementers, tool developers, and programmers working within the Runa ecosystem.






---

## Implementation Notes

### Collection Literals and Comprehensions

Runa supports both static and dynamic (comprehension-based) collection literals.

#### Static Literals (Human-Friendly)
```runa
Let s be set containing 1, 2, 3
Let d be dictionary with:
    "a" as 1
    "b" as 2
Let l be list containing 1, 2, 3
```

#### Dynamic Literals (Comprehensions)
You can construct collections programmatically using comprehensions inside literals:
```runa
Let s be set containing x for each x in values
Let d be dictionary with:
    k as v for each (k, v) in pairs
Let l be list containing f(x) for each x in data if x is greater than 0
```
- The comprehension syntax allows you to build collections from other collections, filter, and transform data naturally.

#### Programmatic Helpers (For AI and Advanced Use)
For more complex or dynamic cases, use stdlib helpers:
```runa
Let s be from_list with elements as values
Let d be from_pairs with pairs as key_value_pairs
```
- These helpers are especially useful for AI-generated code or when the construction logic is not easily expressed as a comprehension.

#### Rationale
- **Literals** are preferred for static and human-written code.
- **Comprehensions** make literals dynamic and programmatic, bridging the gap for AI and advanced users.
- **Helpers** provide additional flexibility for cases where comprehensions are not sufficient.

> **Note:** Runa distinguishes between `Set` (the assignment keyword) and `set` (the collection type/literal). The parser uses context to resolve ambiguity.

### Collection Literals

```ebnf
list_literal          ::= "list" "containing" list_elements
list_elements         ::= expression ("," expression)*
                        | expression "for" identifier "in" expression ("if" expression)?

set_literal           ::= "set" "containing" set_elements
set_elements          ::= expression ("," expression)*
                        | expression "for" identifier "in" expression ("if" expression)?

dictionary_literal    ::= "dictionary" "with" ":" INDENT dict_entries DEDENT
                        | "dictionary" "with" dict_comprehension

dict_entries          ::= dict_entry (NEWLINE dict_entry)*
dict_entry            ::= expression "as" expression
dict_comprehension    ::= identifier "as" expression "for" "(" identifier "," identifier ")" "in" expression ("if" expression)?
```

**Examples:**
```runa
Let l be list containing 1, 2, 3
Let l2 be list containing x for each x in values if x is greater than 0

Let s be set containing 1, 2, 3
Let s2 be set containing x for each x in values

Let d be dictionary with:
    "a" as 1
    "b" as 2

Let d2 be dictionary with k as v for (k, v) in pairs if v is not None
```

--- Idiomatic Assignment and Process Call Styles in Runa ---

## Supported Idioms

### 1. Explicit Assignment (Default)
Use for clarity and in libraries/core logic.
```runa
Let result be pop with heap as h
```

### 2. Context Block Idiom (NEW)
Use for repeated operations on the same object or in scripts.
```runa
With heap as h:
    Let first be pop
    Let second be pop
```
Within the block, any process that can take a `heap` argument will use `h` as the default unless overridden.

### 3. Imperative Assignment (PLANNED)
Command-like, for scripting or AI-generated code. Not yet implemented.
```runa
Pop with heap as h and set as first
```

## Style Guidelines
- Use explicit assignment in libraries and when clarity is paramount.
- Use context blocks in scripts or when working with a current context.
- Use imperative assignment in scripts or for command-like code (future).

## Tooling: Linting and Formatting for Idiom Consistency
- Projects should choose a preferred idiom and enforce it with a linter/formatter.
- The linter should warn about mixing idioms inappropriately.
- The formatter should auto-format code to a consistent style.

## Future Expansion
- As the language matures, additional idioms may be added. All new idioms will be documented with grammar, examples, and style guidelines.

## Bracket Indexing (Mode-Scoped)

Developer mode supports bracket indexing for lists, dictionaries, and other indexable types. In Canon and Viewer, prefer natural forms like "at index" and "at key". Bracket indexing is equivalent to calling the appropriate process (e.g., get_at_index, get_value).

Examples (Developer mode):

    Let first be numbers[0]
    Let value be dict["key"]
    Let char be text[5]

Bracket indexing is concise and idiomatic for programmatic code in Developer mode. For Canon or AI-focused readability, prefer process calls or natural language.

Note: Mode guidance — Canon uses natural syntax; Developer may use dot notation; Viewer displays natural descriptions.

## Context Management Protocol (Standard Library)

Runa supports robust, idiomatic context management for both synchronous and asynchronous resources via the following protocols:

```runa
Protocol ContextManager defines:
    Process called "enter_context" returns Any
    Process called "exit_context" returns None

Protocol AsyncContextManager defines:
    Async Process called "enter_async_context" returns Any
    Async Process called "exit_async_context" returns None
```

Any type implementing these protocols can be used with the `With` statement for resource management. For asynchronous context management, use an `Async:` block with `With` inside.

### Example: Synchronous Lock Context
```runa
Let lock be create_lock
With enter_context with lock as lock_resource:
    Note: Critical section
    Display "Lock acquired!"
    Let released be release_lock with lock as lock_resource
```

### Example: Asynchronous Lock Context
```runa
Async:
    Let lock be create_lock
    With enter_async_context with lock as lock_resource:
        Note: Async critical section
        Display "Async lock acquired!"
        Let released be release_lock with lock as lock_resource
```

### Example: Using Helper Processes
```runa
With acquire_lock as lock:
    Display "Lock acquired via helper!"

Async:
    With acquire_lock_async as lock:
        Display "Async lock acquired via helper!"
```

#### Rationale
- The protocol is extensible: any user-defined type can implement `enter_context`/`exit_context` or their async variants.
- This design matches the ergonomics of Python's `with`/`async with` and Rust's RAII/context traits, but is fully idiomatic to Runa.
- For async context management, use `Async:` blocks with `With` inside, as `AsyncWith` is not yet a language keyword.
- All error handling is explicit: if a resource cannot be acquired or released, an exception is thrown.

See also: [Async Module Standard Library Documentation](../standard-library/async_module.md)