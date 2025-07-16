# Runa Formal Grammar Specification
*Complete EBNF Grammar for Universal Language Translation*

## Overview

This document provides the complete Extended Backus-Naur Form (EBNF) grammar for the Runa programming language. This grammar serves as the authoritative specification for parser implementations and language tooling.

## Notation

- `::=` - Production rule
- `|` - Alternative
- `()` - Grouping
- `[]` - Optional
- `{}` - Zero or more repetitions
- `+` - One or more repetitions
- `*` - Zero or more repetitions
- `?` - Zero or one occurrence
- `"text"` - Terminal symbol (literal)
- `UPPERCASE` - Token/terminal defined elsewhere

## Lexical Structure

### Whitespace and Control

```ebnf
NEWLINE               ::= '\n' | '\r\n' | '\r'
INDENT                ::= increase in indentation level
DEDENT                ::= decrease in indentation level
WHITESPACE            ::= ' ' | '\t'
EOF                   ::= end of file
```

### Comments

```ebnf
comment               ::= "Note:" [^\n]* NEWLINE
```

### Identifiers

```ebnf
identifier            ::= letter (letter | digit | '_')*
multi_word_identifier ::= identifier (WHITESPACE identifier)*
letter                ::= [a-zA-Z_]
digit                 ::= [0-9]
```

### Keywords

```ebnf
keyword               ::= "Let" | "Define" | "Set" | "If" | "Otherwise" | "Unless"
                        | "When" | "Match" | "Process" | "Type" | "Import" | "Export"
                        | "Try" | "Catch" | "Finally" | "For" | "While" | "Loop"
                        | "Return" | "Yield" | "Break" | "Continue" | "Throw"
                        | "Assert" | "Display" | "Delete" | "Await" | "Send"
                        | "Receive" | "Spawn" | "New" | "Static" | "Public"
                        | "Private" | "Async" | "External" | "Protocol" | "With"
                        | "As" | "From" | "To" | "By" | "In" | "Of" | "And" | "Or"
                        | "Not" | "Is" | "Be" | "Plus" | "Minus" | "Times"
                        | "Multiplied" | "Divided" | "Modulo" | "Power" | "Equal"
                        | "Greater" | "Less" | "Than" | "Contains" | "True"
                        | "False" | "None" | "Null" | "Nil"
```

### Literals

```ebnf
literal               ::= number_literal | string_literal | boolean_literal | null_literal

number_literal        ::= integer_literal | float_literal

integer_literal       ::= decimal_int | hex_int | binary_int | octal_int
decimal_int           ::= digit+ ('_' digit+)*
hex_int               ::= '0x' hex_digit+ ('_' hex_digit+)*
binary_int            ::= '0b' binary_digit+ ('_' binary_digit+)*
octal_int             ::= '0o' octal_digit+ ('_' octal_digit+)*

hex_digit             ::= [0-9a-fA-F]
binary_digit          ::= [01]
octal_digit           ::= [0-7]

float_literal         ::= digit+ '.' digit+ ('_' digit+)*

string_literal        ::= normal_string | raw_string | formatted_string
normal_string         ::= '"' string_content '"' | "'" string_content "'"
raw_string            ::= 'r"' raw_string_content '"' | "r'" raw_string_content "'"
formatted_string      ::= 'f"' format_string_content '"' | "f'" format_string_content "'"

string_content        ::= (string_char | escape_sequence)*
raw_string_content    ::= [^"']* | [^']*
format_string_content ::= (string_char | escape_sequence | format_expression)*

string_char           ::= [^"'\\]
escape_sequence       ::= '\\' ('n' | 't' | 'r' | '\\' | '"' | "'" | unicode_escape)
unicode_escape        ::= 'u{' hex_digit+ '}'
format_expression     ::= '{' expression '}'

boolean_literal       ::= "true" | "false"
null_literal          ::= "null" | "none" | "nil"
```

## Top-Level Structure

```ebnf
program               ::= (declaration | statement | ai_annotation)* EOF

declaration           ::= function_definition
                        | type_definition
                        | import_statement
                        | export_declaration
                        | protocol_definition
                        | external_function_declaration

statement             ::= simple_statement | compound_statement

simple_statement      ::= let_statement
                        | define_statement
                        | set_statement
                        | expression_statement
                        | return_statement
                        | yield_statement
                        | break_statement
                        | continue_statement
                        | throw_statement
                        | assert_statement
                        | display_statement
                        | delete_statement
                        | send_statement

compound_statement    ::= if_statement
                        | unless_statement
                        | when_statement
                        | match_statement
                        | switch_statement
                        | for_loop
                        | while_loop
                        | do_while_loop
                        | repeat_loop
                        | infinite_loop
                        | try_catch_statement
                        | with_statement
                        | async_block
                        | atomic_block

block                 ::= ':' INDENT statement* DEDENT
```

## Variable Declarations and Assignments

```ebnf
let_statement         ::= "Let" (identifier | pattern) type_annotation? "be" expression

define_statement      ::= "Define" ["constant"] identifier type_annotation? "as" expression

set_statement         ::= "Set" assignable "to" expression

assignable            ::= identifier | member_access | index_access

type_annotation       ::= '(' type_expression ')'
```

## Type System

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

generic_type          ::= type_identifier '[' type_list ']'

union_type            ::= type_expression ("OR" type_expression)+

intersection_type     ::= type_expression ("AND" type_expression)+

function_type         ::= "Function" '[' type_list ',' type_expression ']'

optional_type         ::= "Optional" '[' type_expression ']'

array_type            ::= "Array" '[' type_expression (',' expression)? ']'

tuple_type            ::= "Tuple" '[' type_list ']'

record_type           ::= "Record" "with" ':' INDENT record_fields DEDENT

record_fields         ::= (identifier "as" type_expression NEWLINE)+

type_list             ::= type_expression (',' type_expression)*

type_identifier       ::= identifier
```

## Type Definitions

```ebnf
type_definition       ::= "Type" identifier generic_params? "is" type_body

generic_params        ::= '[' generic_param (',' generic_param)* ']'

generic_param         ::= identifier type_constraint?

type_constraint       ::= ':' type_expression

type_body             ::= record_definition | adt_definition | type_alias

record_definition     ::= "Dictionary" "with" inheritance_clause? protocol_conformance_clause? ':'
                         INDENT record_member* DEDENT

inheritance_clause    ::= "inherits" "from" type_identifier

protocol_conformance_clause ::= "conforms" "to" type_identifier (',' type_identifier)*

record_member         ::= field_declaration | method_definition | static_member_definition

field_declaration     ::= access_modifier? identifier "as" type_expression NEWLINE

method_definition     ::= access_modifier? function_definition

static_member_definition ::= "Static" (let_statement | define_statement | function_definition)

access_modifier       ::= "Public" | "Private"

adt_definition        ::= ':' INDENT ('|' adt_variant)+ DEDENT

adt_variant           ::= identifier ("with" variant_fields)? NEWLINE

variant_fields        ::= identifier "as" type_expression (("and" | ',') identifier "as" type_expression)*

type_alias            ::= type_expression

protocol_definition   ::= "Protocol" identifier "defines" ':' INDENT protocol_member+ DEDENT

protocol_member       ::= "Process" "called" identifier
                         ("that" "takes" parameter_list)?
                         ("returns" type_expression)? NEWLINE
```

## Function Definitions

```ebnf
function_definition   ::= "Async"? "Process" "called" identifier generic_params?
                         ("that" "takes" parameter_list)?
                         ("returns" type_expression)?
                         ':' block

parameter_list        ::= parameter (',' parameter)*

parameter             ::= identifier type_annotation? ("defaults" "to" expression)?

external_function_declaration ::= "External" "Process" "called" identifier
                                 ("that" "takes" parameter_list)?
                                 ("returns" type_expression)?
                                 "from" "library" string_literal
                                 ("aliased" "as" string_literal)?
```

## Control Flow Statements

```ebnf
if_statement          ::= "If" expression ':' block
                         ("Otherwise" "if" expression ':' block)*
                         ("Otherwise" ':' block)?

unless_statement      ::= "Unless" expression ':' block

when_statement        ::= "When" expression ':' block

match_statement       ::= "Match" expression ':' INDENT match_cases DEDENT

match_cases           ::= match_case+

match_case            ::= "When" pattern guard? ':' block

guard                 ::= "where" expression

switch_statement      ::= "Switch" expression ':' INDENT switch_cases DEDENT

switch_cases          ::= switch_case+ default_case?

switch_case           ::= "Case" expression ':' block fallthrough?

default_case          ::= "Default" ':' block

fallthrough           ::= "Fallthrough"
```

## Loop Statements

```ebnf
for_loop              ::= for_each_loop | for_range_loop

for_each_loop         ::= "For" "each" identifier "in" expression ':' block

for_range_loop        ::= "For" identifier "from" expression "to" expression
                         ("by" expression)? ':' block

while_loop            ::= "While" expression ':' block

do_while_loop         ::= "Do" ':' block "While" expression

repeat_loop           ::= "Repeat" expression "times" ':' block

infinite_loop         ::= "Loop" "forever" ':' block
```

## Pattern Matching

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

wildcard_pattern      ::= '_'

list_pattern          ::= '[' pattern_list? ']'
                        | '[' pattern_list ',' "..." identifier? ']'
                        | "list" "containing" pattern_list

tuple_pattern         ::= '(' pattern_list? ')'

record_pattern        ::= '{' record_pattern_fields? '}'
                        | "dictionary" "with" ':' INDENT record_pattern_fields DEDENT

record_pattern_fields ::= record_pattern_field (',' record_pattern_field | NEWLINE)*

record_pattern_field  ::= identifier "as" pattern

type_pattern          ::= pattern "of" "type" type_expression

or_pattern            ::= pattern ('|' pattern)+

as_pattern            ::= pattern "as" identifier

pattern_list          ::= pattern (',' pattern)*
```

## Expressions

```ebnf
expression            ::= ternary_expression

ternary_expression    ::= or_expression ("if" or_expression "else" or_expression)?

or_expression         ::= and_expression ("or" and_expression)*

and_expression        ::= not_expression ("and" not_expression)*

not_expression        ::= "not" not_expression | comparison_expression

comparison_expression ::= additive_expression (comparison_op additive_expression)*

comparison_op         ::= "is" "equal" "to"
                        | "is" "not" "equal" "to"
                        | "is" "greater" "than"
                        | "is" "less" "than"
                        | "is" "greater" "than" "or" "equal" "to"
                        | "is" "less" "than" "or" "equal" "to"
                        | "contains"
                        | "is" "in"
                        | "is" "of" "type"

additive_expression   ::= multiplicative_expression (additive_op multiplicative_expression)*

additive_op           ::= "plus" | "minus" | "concatenated" "with"

multiplicative_expression ::= unary_expression (multiplicative_op unary_expression)*

multiplicative_op     ::= "multiplied" "by" | "divided" "by" | "modulo"

unary_expression      ::= unary_op unary_expression | power_expression

unary_op              ::= "negative" | "positive" | "bitwise" "not"

power_expression      ::= postfix_expression ("to" "the" "power" "of" postfix_expression)*

postfix_expression    ::= primary_expression postfix_op*

postfix_op            ::= member_access
                        | index_access
                        | slice_access
                        | function_call
                        | type_cast

primary_expression    ::= literal
                        | identifier
                        | '(' expression ')'
                        | lambda_expression
                        | list_comprehension
                        | new_expression
                        | await_expression
                        | receive_expression
                        | spawn_expression
                        | typeof_expression
                        | sizeof_expression
                        | uncertainty_expression
```

## Access Operations

```ebnf
member_access         ::= '.' identifier
                        | natural_field_access
                        | natural_method_access

natural_field_access  ::= "the" identifier "of" expression

natural_method_access ::= "the" identifier "of" expression
                        | identifier "with" "self" "as" expression

index_access          ::= '[' expression ']'
                        | "at" "index" expression

slice_access          ::= '[' expression? ':' expression? (':' expression)? ']'
```

## Function Calls

```ebnf
function_call         ::= '(' argument_list? ')'
                        | "with" named_arguments

argument_list         ::= argument (',' argument)*

argument              ::= expression | "..." expression

named_arguments       ::= named_argument (("and" | ',') named_argument)*
                        | ':' INDENT (named_argument NEWLINE)* DEDENT

named_argument        ::= identifier "as" expression
```

## Advanced Expressions

```ebnf
lambda_expression     ::= "lambda" parameter_list? ':' expression

list_comprehension    ::= '[' expression "for" identifier "in" expression
                         ("if" expression)? ']'

new_expression        ::= "New" type_expression ("with" named_arguments)?

await_expression      ::= "await" expression

spawn_expression      ::= "Spawn" function_call

receive_expression    ::= "Receive" ("from" expression)? ("timeout" expression)?

typeof_expression     ::= "type" "of" expression

sizeof_expression     ::= "size" "of" type_expression

type_cast             ::= "as" type_expression

uncertainty_expression ::= '?' '[' expression_list ']' ("with" "confidence" expression)?
                          | '?' expression
```

## Error Handling

```ebnf
try_catch_statement   ::= "Try" ':' block
                         ("Catch" identifier? type_annotation? ':' block)+
                         ("Finally" ':' block)?

throw_statement       ::= "Throw" expression

assert_statement      ::= "Assert" expression ("with" "message" expression)?
```

## Resource Management

```ebnf
with_statement        ::= "With" expression "as" identifier ':' block

delete_statement      ::= "Delete" expression
```

## Module System

```ebnf
import_statement      ::= "Import" "module" string_literal ("as" identifier)?
                        | "Import" '{' import_list '}' "from" "module" string_literal

import_list           ::= import_item (',' import_item)*

import_item           ::= identifier ("as" identifier)?

export_declaration    ::= "Export" declaration
```

## Concurrency

```ebnf
send_statement        ::= "Send" expression "to" expression

async_block           ::= "Async" ':' block

atomic_block          ::= "Atomic" ':' block
```

## AI Annotations

```ebnf
ai_annotation         ::= reasoning_annotation
                        | implementation_annotation
                        | task_annotation
                        | knowledge_annotation
                        | verification_annotation
                        | resource_annotation
                        | security_annotation
                        | execution_annotation
                        | uncertainty_annotation
                        | progress_annotation
                        | translation_annotation
                        | error_handling_annotation

reasoning_annotation  ::= "@Reasoning:" annotation_content "@End_Reasoning"

implementation_annotation ::= "@Implementation:" annotation_content "@End_Implementation"

task_annotation       ::= "@Task:" structured_content "@End_Task"

knowledge_annotation  ::= "@KnowledgeReference:" structured_content "@End_KnowledgeReference"

verification_annotation ::= "@Verify:" assertion_list "@End_Verify"

resource_annotation   ::= "@Resource_Constraints:" constraint_list "@End_Resource_Constraints"

security_annotation   ::= "@Security_Scope:" capability_list "@End_Security_Scope"

execution_annotation  ::= "@Execution_Model:" execution_params "@End_Execution_Model"

uncertainty_annotation ::= "@Uncertainty:" uncertainty_content "@End_Uncertainty"

progress_annotation   ::= "@Progress:" progress_content "@End_Progress"

translation_annotation ::= "@Translation_Note:" translation_content "@End_Translation_Note"

error_handling_annotation ::= "@Error_Handling:" error_content "@End_Error_Handling"

annotation_content    ::= free_text
free_text             ::= [^@]* # Any text until next @ symbol
structured_content    ::= key_value_pairs
assertion_list        ::= (assertion NEWLINE)*
assertion             ::= "Assert" expression ("with" "message" expression)?
```

## Collection Literals

```ebnf
list_literal          ::= '[' expression_list? ']'
                        | "list" "containing" expression_list

dictionary_literal    ::= '{' key_value_pairs? '}'
                        | "dictionary" "with" ':' INDENT dict_entries DEDENT

tuple_literal         ::= '(' expression_list ')'

set_literal           ::= "set" "containing" expression_list

expression_list       ::= expression (',' expression)*

key_value_pairs       ::= key_value_pair (',' key_value_pair)*

key_value_pair        ::= expression ':' expression
                        | identifier "as" expression

dict_entries          ::= (dict_entry NEWLINE)*

dict_entry            ::= identifier "as" expression
```

## Operator Precedence (Highest to Lowest)

1. Primary expressions (literals, identifiers, parentheses)
2. Postfix operators (member access, indexing, function calls)
3. Unary operators (negative, positive, not)
4. Power operator (to the power of)
5. Multiplicative operators (multiplied by, divided by, modulo)
6. Additive operators (plus, minus, concatenated with)
7. Comparison operators (is equal to, is greater than, etc.)
8. Logical NOT (not)
9. Logical AND (and)
10. Logical OR (or)
11. Ternary conditional (if...else)
12. Assignment operators (be, as, to)

## Grammar Notes

### Multi-word Identifiers

Runa supports multi-word identifiers separated by spaces:
- `user name` is a valid identifier
- `account balance` is a valid identifier
- `final total` is a valid identifier

### Natural Language Operators

Operators use natural language constructs:
- Arithmetic: `plus`, `minus`, `multiplied by`, `divided by`
- Comparison: `is equal to`, `is greater than`, `is less than or equal to`
- Logical: `and`, `or`, `not`

### Indentation-Based Blocks

Runa uses Python-style indentation for block structure:
- `INDENT` token represents increased indentation
- `DEDENT` token represents decreased indentation
- Consistent indentation is required within blocks

### Context-Sensitive Parsing

Some constructs require context-sensitive parsing:
- Multi-word identifiers vs. separate tokens
- Natural language operators vs. individual words
- AI annotation blocks vs. regular comments

### Error Recovery

Parsers should implement error recovery strategies:
- Skip to next statement boundary on syntax errors
- Provide meaningful error messages for common mistakes
- Support partial parsing for IDE integration

## Implementation Considerations

### Lexer Requirements

1. **Multi-word Token Recognition**: Handle space-separated identifier components
2. **Keyword Disambiguation**: Distinguish keywords from identifiers in context
3. **Indentation Tracking**: Generate INDENT/DEDENT tokens based on whitespace
4. **String Interpolation**: Handle format expressions within f-strings

### Parser Requirements

1. **Recursive Descent**: Natural fit for Runa's grammar structure
2. **Operator Precedence**: Implement precedence climbing for expressions
3. **Error Recovery**: Graceful handling of syntax errors
4. **AST Generation**: Rich AST nodes with source location information

### Semantic Analysis

1. **Symbol Tables**: Nested scopes with proper shadowing rules
2. **Type Checking**: Strong static typing with inference
3. **Generic Resolution**: Type parameter substitution and constraint checking
4. **Pattern Exhaustiveness**: Ensure all match cases are covered

This grammar specification provides the complete formal definition of Runa's syntax and serves as the foundation for all language tooling and implementations.

# --- Context Block Idiom (NEW) ---

context_block ::= "With" identifier "as" identifier ":" block
block         ::= INDENT statement* DEDENT

# Example:
# With heap as h:
#     Let first be pop
#     Let second be pop

# --- Imperative Assignment Idiom (PLANNED) ---

imperative_assignment ::= process_call "and set as" identifier
process_call          ::= identifier "with" (identifier "as" expression) ( "and" identifier "as" expression )*

# Example:
# Pop with heap as h and set as first
#
# Note: Imperative assignment is planned for a future version. Parser support is not yet implemented.

# --- Bracket Indexing (NEW) ---

index_expression ::= primary_expression '[' expression ']'

# Example:
# Let x be l[0]
# Let y be d["key"]

# Bracket indexing is supported for lists, dictionaries, and other indexable types. It is equivalent to calling the appropriate process (e.g., get_at_index, get_value).