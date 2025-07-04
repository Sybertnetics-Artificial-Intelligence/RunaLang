# Runa Comprehensive Grammar Rules
# Complete EBNF grammar for universal language translation

# =============================================================================
# Top-Level Structure
# =============================================================================

program                 ::= (statement | declaration | ai_annotation)* EOF

# =============================================================================
# Statements
# =============================================================================

statement              ::= simple_statement
                        | compound_statement
                        | flow_control_statement
                        | error_handling_statement
                        | concurrency_statement
                        | memory_statement

simple_statement       ::= let_statement
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
                        | await_statement
                        | send_statement

compound_statement     ::= if_statement
                        | unless_statement
                        | when_statement
                        | match_statement
                        | switch_statement
                        | for_loop
                        | while_loop
                        | do_while_loop
                        | repeat_loop
                        | infinite_loop
                        | async_block
                        | atomic_block
                        | lock_statement
                        | with_statement

# =============================================================================
# Variable Declarations and Assignments
# =============================================================================

let_statement          ::= "Let" identifier type_annotation? "be" expression
                        | "Let" pattern "be" expression

define_statement       ::= "Define" identifier type_annotation? "as" expression
                        | "Define" "constant" identifier type_annotation? "as" expression

set_statement          ::= "Set" assignable "to" expression

assignable             ::= identifier
                        | member_access
                        | index_access

type_annotation        ::= "(" type_expression ")"

# =============================================================================
# Type Expressions
# =============================================================================

type_expression        ::= basic_type
                        | generic_type
                        | union_type
                        | intersection_type
                        | function_type
                        | optional_type
                        | array_type
                        | tuple_type
                        | record_type
                        | type_identifier

basic_type             ::= "Integer" | "Float" | "String" | "Boolean" 
                        | "Character" | "Byte" | "Any" | "Void" | "Never"

generic_type           ::= type_identifier "[" type_list "]"

union_type             ::= type_expression ("OR" type_expression)+

intersection_type      ::= type_expression ("AND" type_expression)+

function_type          ::= "Function" "[" type_list "," type_expression "]"

optional_type          ::= "Optional" "[" type_expression "]"

array_type             ::= "Array" "[" type_expression ("," expression)? "]"

tuple_type             ::= "Tuple" "[" type_list "]"

record_type            ::= "Record" "with" ":" INDENT record_fields DEDENT

record_fields          ::= (identifier "as" type_expression)+

type_list              ::= type_expression ("," type_expression)*

# =============================================================================
# Control Flow Statements
# =============================================================================

if_statement           ::= "If" expression ":" block 
                          ("Otherwise" "if" expression ":" block)*
                          ("Otherwise" ":" block)?

unless_statement       ::= "Unless" expression ":" block

when_statement         ::= "When" expression ":" block

match_statement        ::= "Match" expression ":" INDENT match_cases DEDENT

match_cases            ::= match_case+

match_case             ::= "When" pattern guard? ":" block

guard                  ::= "where" expression

switch_statement       ::= "Switch" expression ":" INDENT switch_cases DEDENT

switch_cases           ::= switch_case+ default_case?

switch_case            ::= "Case" expression ":" block fallthrough?

default_case           ::= "Default" ":" block

fallthrough            ::= "Fallthrough"

# =============================================================================
# Loop Statements
# =============================================================================

for_loop               ::= for_each_loop | for_range_loop

for_each_loop          ::= "For" "each" identifier "in" expression ":" block

for_range_loop         ::= "For" identifier "from" expression "to" expression 
                          ("by" expression)? ":" block

while_loop             ::= "While" expression ":" block

do_while_loop          ::= "Do" ":" block "While" expression

repeat_loop            ::= "Repeat" expression "times" ":" block

infinite_loop          ::= "Loop" "forever" ":" block

# =============================================================================
# Pattern Matching
# =============================================================================

pattern                ::= literal_pattern
                        | identifier_pattern
                        | wildcard_pattern
                        | list_pattern
                        | tuple_pattern
                        | record_pattern
                        | type_pattern
                        | or_pattern
                        | as_pattern

literal_pattern        ::= literal

identifier_pattern     ::= identifier

wildcard_pattern       ::= "_"

list_pattern           ::= "[" pattern_list "]"
                        | "[" pattern_list "," "..." identifier? "]"
                        | "list" "containing" pattern_list

tuple_pattern          ::= "(" pattern_list ")"

record_pattern         ::= "{" record_pattern_fields "}"
                        | "dictionary" "with" ":" INDENT record_pattern_fields DEDENT

record_pattern_fields  ::= (identifier "as" pattern ("," | NEWLINE))*

type_pattern           ::= pattern "of" "type" type_expression

or_pattern             ::= pattern ("|" pattern)+

as_pattern             ::= pattern "as" identifier

pattern_list           ::= pattern ("," pattern)*

# =============================================================================
# Expressions
# =============================================================================

expression             ::= ternary_expression

ternary_expression     ::= or_expression ("if" or_expression "else" or_expression)?

or_expression          ::= and_expression ("or" and_expression)*

and_expression         ::= not_expression ("and" not_expression)*

not_expression         ::= "not" not_expression | comparison_expression

comparison_expression  ::= additive_expression (comparison_op additive_expression)*

comparison_op          ::= "is" "equal" "to"
                        | "is" "not" "equal" "to"
                        | "is" "greater" "than"
                        | "is" "less" "than"
                        | "is" "greater" "than" "or" "equal" "to"
                        | "is" "less" "than" "or" "equal" "to"
                        | "contains"
                        | "is" "in"
                        | "is" "of" "type"

additive_expression    ::= multiplicative_expression (additive_op multiplicative_expression)*

additive_op            ::= "plus" | "minus" | "concatenated" "with"

multiplicative_expression ::= unary_expression (multiplicative_op unary_expression)*

multiplicative_op      ::= "multiplied" "by" | "divided" "by" | "modulo"

unary_expression       ::= unary_op unary_expression | power_expression

unary_op               ::= "negative" | "positive" | "bitwise" "not"

power_expression       ::= postfix_expression ("to" "the" "power" "of" postfix_expression)*

postfix_expression     ::= primary_expression postfix_op*

postfix_op             ::= member_access
                        | index_access  
                        | slice_access
                        | function_call
                        | type_cast

primary_expression     ::= literal
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

# =============================================================================
# Access Operations
# =============================================================================

member_access          ::= "." identifier

index_access           ::= "[" expression "]"
                        | "at" "index" expression

slice_access           ::= "[" expression? ":" expression? (":" expression)? "]"

# =============================================================================
# Function Calls
# =============================================================================

function_call          ::= "(" argument_list ")"
                        | "with" named_arguments

argument_list          ::= (argument ("," argument)*)?

argument               ::= expression
                        | "..." expression

named_arguments        ::= named_argument (("and" | ",") named_argument)*
                        | ":" INDENT (named_argument NEWLINE)* DEDENT

named_argument         ::= identifier "as" expression

# =============================================================================
# Type Operations
# =============================================================================

type_cast              ::= "as" type_expression

typeof_expression      ::= "type" "of" expression

sizeof_expression      ::= "size" "of" type_expression

new_expression         ::= "New" type_expression ("with" named_arguments)?

# =============================================================================
# Literals
# =============================================================================

literal                ::= number_literal
                        | string_literal
                        | boolean_literal
                        | null_literal
                        | list_literal
                        | dictionary_literal
                        | tuple_literal
                        | set_literal

number_literal         ::= integer_literal | float_literal

integer_literal        ::= DIGIT+ type_suffix?

float_literal          ::= DIGIT+ "." DIGIT+ type_suffix?

type_suffix            ::= "L" | "U" | "F" | "D"

string_literal         ::= string_prefix? (QUOTE string_content QUOTE | APOSTROPHE string_content APOSTROPHE)

string_prefix          ::= "r" | "u" | "b" | "f"

boolean_literal        ::= "true" | "false"

null_literal           ::= "null" | "none" | "nil" | "undefined"

list_literal           ::= "[" expression_list "]"
                        | "list" "containing" expression_list

dictionary_literal     ::= "{" key_value_pairs "}"
                        | "dictionary" "with" ":" INDENT dict_