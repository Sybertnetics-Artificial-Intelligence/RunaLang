.section .data
.globl PROGRAM_FUNCTIONS
PROGRAM_FUNCTIONS:    .quad 0
.globl PROGRAM_FUNCTION_COUNT
PROGRAM_FUNCTION_COUNT:    .quad 8
.globl PROGRAM_FUNCTION_CAPACITY
PROGRAM_FUNCTION_CAPACITY:    .quad 12
.globl PROGRAM_TYPES
PROGRAM_TYPES:    .quad 16
.globl PROGRAM_TYPE_COUNT
PROGRAM_TYPE_COUNT:    .quad 24
.globl PROGRAM_TYPE_CAPACITY
PROGRAM_TYPE_CAPACITY:    .quad 28
.globl PROGRAM_IMPORTS
PROGRAM_IMPORTS:    .quad 32
.globl PROGRAM_IMPORT_COUNT
PROGRAM_IMPORT_COUNT:    .quad 40
.globl PROGRAM_IMPORT_CAPACITY
PROGRAM_IMPORT_CAPACITY:    .quad 44
.globl PROGRAM_GLOBAL_VARS
PROGRAM_GLOBAL_VARS:    .quad 48
.globl PROGRAM_GLOBAL_COUNT
PROGRAM_GLOBAL_COUNT:    .quad 56
.globl PROGRAM_GLOBAL_CAPACITY
PROGRAM_GLOBAL_CAPACITY:    .quad 60
.globl EXPR_INTEGER
EXPR_INTEGER:    .quad 0
.globl EXPR_VARIABLE
EXPR_VARIABLE:    .quad 1
.globl EXPR_BINARY_OP
EXPR_BINARY_OP:    .quad 2
.globl EXPR_COMPARISON
EXPR_COMPARISON:    .quad 3
.globl EXPR_FUNCTION_CALL
EXPR_FUNCTION_CALL:    .quad 4
.globl EXPR_STRING_LITERAL
EXPR_STRING_LITERAL:    .quad 5
.globl EXPR_FIELD_ACCESS
EXPR_FIELD_ACCESS:    .quad 6
.globl EXPR_TYPE_NAME
EXPR_TYPE_NAME:    .quad 7
.globl EXPR_BUILTIN_CALL
EXPR_BUILTIN_CALL:    .quad 8
.globl EXPR_VARIANT_CONSTRUCTOR
EXPR_VARIANT_CONSTRUCTOR:    .quad 9
.globl EXPR_FUNCTION_POINTER
EXPR_FUNCTION_POINTER:    .quad 10
.globl EXPR_INDIRECT_CALL
EXPR_INDIRECT_CALL:    .quad 11
.globl EXPR_ARRAY_INDEX
EXPR_ARRAY_INDEX:    .quad 16
.globl EXPR_LIST_LITERAL
EXPR_LIST_LITERAL:    .quad 17
.globl EXPR_SET_LITERAL
EXPR_SET_LITERAL:    .quad 21
.globl EXPR_DICT_LITERAL
EXPR_DICT_LITERAL:    .quad 22
.globl EXPR_STRUCT_CONSTRUCTION
EXPR_STRUCT_CONSTRUCTION:    .quad 20
.globl EXPR_LAMBDA
EXPR_LAMBDA:    .quad 23
.globl EXPR_LAMBDA_CALL
EXPR_LAMBDA_CALL:    .quad 24
.globl EXPR_QUALIFIED_CALL
EXPR_QUALIFIED_CALL:    .quad 25
.globl STMT_LET
STMT_LET:    .quad 1
.globl STMT_SET
STMT_SET:    .quad 2
.globl STMT_RETURN
STMT_RETURN:    .quad 3
.globl STMT_PRINT
STMT_PRINT:    .quad 4
.globl STMT_IF
STMT_IF:    .quad 5
.globl STMT_WHILE
STMT_WHILE:    .quad 6
.globl STMT_EXPRESSION
STMT_EXPRESSION:    .quad 7
.globl STMT_MATCH
STMT_MATCH:    .quad 8
.globl STMT_BREAK
STMT_BREAK:    .quad 9
.globl STMT_CONTINUE
STMT_CONTINUE:    .quad 10
.globl STMT_FOR
STMT_FOR:    .quad 11
.globl STMT_FOR_EACH
STMT_FOR_EACH:    .quad 12
.globl STMT_IMPORT
STMT_IMPORT:    .quad 13
.globl STMT_INLINE_ASSEMBLY
STMT_INLINE_ASSEMBLY:    .quad 16
.globl STMT_COMPOUND_ASSIGN
STMT_COMPOUND_ASSIGN:    .quad 17
.globl STMT_MATCH_EXPR
STMT_MATCH_EXPR:    .quad 8
.globl STMT_MATCH_WHEN_CLAUSES
STMT_MATCH_WHEN_CLAUSES:    .quad 16
.globl STMT_MATCH_WHEN_COUNT
STMT_MATCH_WHEN_COUNT:    .quad 24
.globl WHEN_PATTERN_TYPE
WHEN_PATTERN_TYPE:    .quad 0
.globl WHEN_PATTERN_VALUE
WHEN_PATTERN_VALUE:    .quad 8
.globl WHEN_FIELD_BINDINGS
WHEN_FIELD_BINDINGS:    .quad 16
.globl WHEN_FIELD_COUNT
WHEN_FIELD_COUNT:    .quad 24
.globl WHEN_BODY_STMTS
WHEN_BODY_STMTS:    .quad 32
.globl WHEN_BODY_COUNT
WHEN_BODY_COUNT:    .quad 40
.globl PATTERN_LITERAL
PATTERN_LITERAL:    .quad 0
.globl PATTERN_VARIANT
PATTERN_VARIANT:    .quad 1
.globl PATTERN_WILDCARD
PATTERN_WILDCARD:    .quad 2
.globl PATTERN_TYPE
PATTERN_TYPE:    .quad 3
.globl TYPE_KIND_STRUCT
TYPE_KIND_STRUCT:    .quad 0
.globl TYPE_KIND_VARIANT
TYPE_KIND_VARIANT:    .quad 1
.globl TYPE_KIND_FUNCTION
TYPE_KIND_FUNCTION:    .quad 2
.globl TYPE_KIND_ARRAY
TYPE_KIND_ARRAY:    .quad 3
.globl TypeDefinition_SIZE
TypeDefinition_SIZE:    .quad 48
.globl TYPEDEFINITION_NAME_OFFSET
TYPEDEFINITION_NAME_OFFSET:    .quad 0
.globl TYPEDEFINITION_KIND_OFFSET
TYPEDEFINITION_KIND_OFFSET:    .quad 8
.globl TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET:    .quad 16
.globl TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET:    .quad 24
.globl TYPEDEFINITION_SIZE_OFFSET
TYPEDEFINITION_SIZE_OFFSET:    .quad 40
.globl TYPEDEFINITION_DATA_ARRAY_ELEMENT_TYPE_OFFSET
TYPEDEFINITION_DATA_ARRAY_ELEMENT_TYPE_OFFSET:    .quad 16
.globl TYPEDEFINITION_DATA_ARRAY_ELEMENT_SIZE_OFFSET
TYPEDEFINITION_DATA_ARRAY_ELEMENT_SIZE_OFFSET:    .quad 24
.globl TYPEDEFINITION_DATA_ARRAY_LENGTH_OFFSET
TYPEDEFINITION_DATA_ARRAY_LENGTH_OFFSET:    .quad 28
.globl TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET:    .quad 16
.globl TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET:    .quad 24
.globl TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET:    .quad 32
.globl TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET:    .quad 16
.globl TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET:    .quad 24
.globl TYPEFIELD_SIZE
TYPEFIELD_SIZE:    .quad 24
.globl TYPEFIELD_NAME_OFFSET
TYPEFIELD_NAME_OFFSET:    .quad 0
.globl TYPEFIELD_TYPE_OFFSET
TYPEFIELD_TYPE_OFFSET:    .quad 8
.globl TYPEFIELD_OFFSET_OFFSET
TYPEFIELD_OFFSET_OFFSET:    .quad 16
.globl TYPEFIELD_SIZE_OFFSET
TYPEFIELD_SIZE_OFFSET:    .quad 20
.globl VARIANT_SIZE
VARIANT_SIZE:    .quad 32
.globl VARIANT_NAME_OFFSET
VARIANT_NAME_OFFSET:    .quad 0
.globl VARIANT_FIELDS_OFFSET
VARIANT_FIELDS_OFFSET:    .quad 8
.globl VARIANT_FIELD_COUNT_OFFSET
VARIANT_FIELD_COUNT_OFFSET:    .quad 16
.globl VARIANT_TAG_OFFSET
VARIANT_TAG_OFFSET:    .quad 20
.globl PARSER_CURRENT_TOKEN_OFFSET
PARSER_CURRENT_TOKEN_OFFSET:    .quad 8
.globl PARSER_CURRENT_PROGRAM_OFFSET
PARSER_CURRENT_PROGRAM_OFFSET:    .quad 16
.globl EXPRESSION_TYPE_OFFSET
EXPRESSION_TYPE_OFFSET:    .quad 0
.globl SIZEOF_PARSER
SIZEOF_PARSER:    .quad 32
.globl SIZEOF_PROGRAM
SIZEOF_PROGRAM:    .quad 64
.globl PARSER_LEXER
PARSER_LEXER:    .quad 0
.globl PARSER_CURRENT_TOKEN
PARSER_CURRENT_TOKEN:    .quad 8
.globl PARSER_ARENA
PARSER_ARENA:    .quad 24
.globl TOKEN_TYPE_OFFSET
TOKEN_TYPE_OFFSET:    .quad 0
.globl TOKEN_VALUE_OFFSET
TOKEN_VALUE_OFFSET:    .quad 8
.globl TOKEN_LINE_OFFSET
TOKEN_LINE_OFFSET:    .quad 16
.globl EXPR_UNARY
EXPR_UNARY:    .quad 11
.globl EXPR_BINARY
EXPR_BINARY:    .quad 2
.globl EXPR_CALL
EXPR_CALL:    .quad 4
.globl EXPR_ARRAY_ACCESS
EXPR_ARRAY_ACCESS:    .quad 16
.globl EXPR_IDENTIFIER
EXPR_IDENTIFIER:    .quad 1
.globl STMT_TYPE
STMT_TYPE:    .quad 0
.globl STMT_LET_NAME
STMT_LET_NAME:    .quad 8
.globl STMT_LET_VALUE
STMT_LET_VALUE:    .quad 16
.globl STMT_LET_TYPE
STMT_LET_TYPE:    .quad 24
.globl STMT_SET_NAME
STMT_SET_NAME:    .quad 8
.globl STMT_SET_VALUE
STMT_SET_VALUE:    .quad 16
.globl STMT_IF_CONDITION
STMT_IF_CONDITION:    .quad 8
.globl STMT_IF_THEN_BODY
STMT_IF_THEN_BODY:    .quad 16
.globl STMT_IF_ELSE_BODY
STMT_IF_ELSE_BODY:    .quad 24
.globl STMT_WHILE_CONDITION
STMT_WHILE_CONDITION:    .quad 8
.globl STMT_WHILE_BODY
STMT_WHILE_BODY:    .quad 16
.globl STMT_FOR_VAR
STMT_FOR_VAR:    .quad 8
.globl STMT_FOR_START
STMT_FOR_START:    .quad 16
.globl STMT_FOR_END
STMT_FOR_END:    .quad 24
.globl STMT_FOR_BODY
STMT_FOR_BODY:    .quad 32
.globl STMT_RETURN_VALUE
STMT_RETURN_VALUE:    .quad 8
.globl STMT_EXPR_VALUE
STMT_EXPR_VALUE:    .quad 8
.globl EXPR_TYPE
EXPR_TYPE:    .quad 0
.globl EXPR_BINARY_LEFT
EXPR_BINARY_LEFT:    .quad 8
.globl EXPR_BINARY_RIGHT
EXPR_BINARY_RIGHT:    .quad 16
.globl EXPR_UNARY_OPERAND
EXPR_UNARY_OPERAND:    .quad 8
.globl EXPR_CALL_NAME
EXPR_CALL_NAME:    .quad 8
.globl EXPR_CALL_ARGS
EXPR_CALL_ARGS:    .quad 16
.globl EXPR_FIELD_OBJECT
EXPR_FIELD_OBJECT:    .quad 8
.globl EXPR_FIELD_NAME
EXPR_FIELD_NAME:    .quad 16
.globl EXPR_ARRAY_OBJECT
EXPR_ARRAY_OBJECT:    .quad 8
.globl EXPR_ARRAY_INDEX_OFFSET
EXPR_ARRAY_INDEX_OFFSET:    .quad 16
.globl EXPR_IDENTIFIER_NAME
EXPR_IDENTIFIER_NAME:    .quad 8
.globl EXPR_STRING_VALUE
EXPR_STRING_VALUE:    .quad 8
.globl TYPE_PRIMITIVE
TYPE_PRIMITIVE:    .quad 0
.globl TYPE_STRUCT
TYPE_STRUCT:    .quad 1
.globl TYPE_ARRAY
TYPE_ARRAY:    .quad 2
.globl TYPE_POINTER
TYPE_POINTER:    .quad 3
.globl TYPE_KIND
TYPE_KIND:    .quad 0
.globl TYPE_STRUCT_NAME
TYPE_STRUCT_NAME:    .quad 8
.globl TYPE_STRUCT_FIELDS
TYPE_STRUCT_FIELDS:    .quad 16
.globl TYPE_ARRAY_ELEMENT_TYPE
TYPE_ARRAY_ELEMENT_TYPE:    .quad 8
.globl TYPE_POINTER_TARGET_TYPE
TYPE_POINTER_TARGET_TYPE:    .quad 8
.globl FUNCTION_NAME
FUNCTION_NAME:    .quad 0
.globl FUNCTION_PARAMETERS
FUNCTION_PARAMETERS:    .quad 8
.globl FUNCTION_RETURN_TYPE
FUNCTION_RETURN_TYPE:    .quad 16
.globl FUNCTION_BODY
FUNCTION_BODY:    .quad 24

.text
print_string:
    pushq %rbp
    movq %rsp, %rbp

    # Calculate string length
    movq %rdi, %rsi  # Save string pointer
    movq %rdi, %rcx  # Counter for strlen
    xorq %rax, %rax  # Length accumulator
.strlen_loop:
    cmpb $0, (%rcx)
    je .strlen_done
    incq %rcx
    incq %rax
    jmp .strlen_loop
.strlen_done:

    # Call write syscall (sys_write = 1)
    movq $1, %rdi     # fd = stdout
    movq %rsi, %rsi   # buf = string pointer (already in rsi)
    movq %rax, %rdx   # count = string length
    movq $1, %rax     # syscall number for write
    syscall

    # Print newline
    movq $1, %rdi     # fd = stdout
    leaq .newline(%rip), %rsi  # newline string
    movq $1, %rdx     # count = 1
    movq $1, %rax     # syscall number for write
    syscall

    popq %rbp
    ret


print_integer:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp  # Space for string buffer (20 digits + null)

    # Convert integer to string
    movq %rdi, %rax  # integer value
    leaq -32(%rbp), %rsi  # buffer pointer
    addq $19, %rsi  # point to end of buffer (for reverse building)
    movb $0, (%rsi)  # null terminator
    decq %rsi

    # Handle zero case
    testq %rax, %rax
    jnz .convert_loop
    movb $48, (%rsi)  # '0' character
    jmp .convert_done

.convert_loop:
    testq %rax, %rax
    jz .convert_done
    movq %rax, %rcx
    movq $10, %rbx
    xorq %rdx, %rdx
    divq %rbx  # %rax = quotient, %rdx = remainder
    addq $48, %rdx  # convert remainder to ASCII
    movb %dl, (%rsi)  # store digit
    decq %rsi
    jmp .convert_loop

.convert_done:
    incq %rsi  # point to first character

    # Calculate string length
    movq %rsi, %rcx  # Counter for strlen
    xorq %rax, %rax  # Length accumulator
.int_strlen_loop:
    cmpb $0, (%rcx)
    je .int_strlen_done
    incq %rcx
    incq %rax
    jmp .int_strlen_loop
.int_strlen_done:

    # Call write syscall (sys_write = 1)
    movq $1, %rdi     # fd = stdout
    # %rsi already points to string
    movq %rax, %rdx   # count = string length
    movq $1, %rax     # syscall number for write
    syscall

    # Print newline
    movq $1, %rdi     # fd = stdout
    leaq .newline(%rip), %rsi  # newline string
    movq $1, %rdx     # count = 1
    movq $1, %rax     # syscall number for write
    syscall

    movq %rbp, %rsp
    popq %rbp
    ret


.section .rodata
.newline:
    .byte 10  # newline character
.STR0:    .string "string_concat"
.STR1:    .string "xor"
.STR2:    .string "list_get"
.STR3:    .string "[PARSER WARNING] Unexpected token after '.' at line "
.STR4:    .string "[PARSER ERROR] Module name must be a simple identifier"
.STR5:    .string "[PARSER ERROR] Expected 'index' or 'key' after 'at' at line "
.STR6:    .string "[PARSER ERROR] Expected 'than' after 'less' at line "
.STR7:    .string "[PARSER ERROR] Expected 'than' after 'greater' at line "
.STR8:    .string "null"
.STR9:    .string "Null"
.STR10:    .string "equals"
.STR11:    .string "does"
.STR12:    .string "equal"
.STR13:    .string "list_contains"
.STR14:    .string "dict_has_key"
.STR15:    .string "[PARSER ERROR] NULL parser in parser_parse_let_statement"
.STR16:    .string "[PARSER ERROR] Expected identifier after Let at line "
.STR17:    .string "[PARSER ERROR] parser became NULL before expression parsing in Let"
.STR18:    .string "Parser error: Expected operation after gets (got token "
.STR19:    .string ")"
.STR20:    .string "[PARSER ERROR] Expected token type "
.STR21:    .string ", got "
.STR22:    .string " at line "
.STR23:    .string "_"
.STR24:    .string "nothing"
.STR25:    .string "List"
.STR26:    .string "[PARSER ERROR] Expected 'as' in dictionary literal at line "
.STR27:    .string "Dictionary"
.STR28:    .string "Integer"
.STR29:    .string "Float"
.STR30:    .string "String"
.STR31:    .string "Boolean"
.STR32:    .string "Character"
.STR33:    .string "[PARSER ERROR] Null parser in parse_primary"
.STR34:    .string "[PARSER ERROR] Null current_token in parse_primary"
.STR35:    .string "size_of"
.STR36:    .string "list"
.STR37:    .string "dictionary"
.STR38:    .string "value"
.STR39:    .string "a"
.STR40:    .string "memory_get_pointer"
.STR41:    .string "memory_get_byte"
.STR42:    .string "[PARSER ERROR] Expected function name after $ at line "
.STR43:    .string "string_length"
.STR44:    .string "length"
.STR45:    .string "External"
.STR46:    .string "substring"
.STR47:    .string "string_substring"
.STR48:    .string "string"
.STR49:    .string "representation"
.STR50:    .string "int_to_string"
.STR51:    .string "[PARSER ERROR] Expected field name after 'the' at line "
.STR52:    .string "[PARSER ERROR] Expected 'of' after field name at line "
.STR53:    .string "an"
.STR54:    .string "[PARSER ERROR] Expected 'containing' after 'a list' at line "
.STR55:    .string "set"
.STR56:    .string "[PARSER ERROR] Expected 'containing' after 'a set' at line "
.STR57:    .string "[PARSER ERROR] Expected 'with' after struct type name at line "
.STR58:    .string "[PARSER ERROR] Expected field name at line "
.STR59:    .string "Array"
.STR60:    .string "[PARSER ERROR] Expected 'of' after 'an Array' at line "
.STR61:    .string "[PARSER ERROR] Expected integer size after 'an Array of' at line "
.STR62:    .string "[PARSER ERROR] Expected type name after array size at line "
.STR63:    .string "[PARSER ERROR] Array size mismatch: declared "
.STR64:    .string " but got "
.STR65:    .string " elements"
.STR66:    .string "[PARSER ERROR] Expected ':' after 'dictionary with' at line "
.STR67:    .string "[PARSER ERROR] Expected variant name after 'as'"
.STR68:    .string "[PARSER ERROR] Expected field name after 'with'"
.STR69:    .string "[PARSER ERROR] Expected ',' or ')' in function arguments at line "
.STR70:    .string "[PARSER ERROR] Expected integer after 'negative' at line "
.STR71:    .string "[PARSER ERROR] Expected parameter name after 'lambda'"
.STR72:    .string "[PARSER ERROR] Expected parameter name after comma"
.STR73:    .string "[PARSER ERROR] Expected ':' after lambda parameters"
.STR74:    .string "[PARSER ERROR] Expected integer or identifier at line "
.STR75:    .string "[PARSER ERROR] Display/Print is a statement and should not use parentheses. Use 'Display expression' not 'Display(expression)' at line "
.STR76:    .string "memory_set_pointer"
.STR77:    .string "memory_set_byte"
.STR78:    .string "Add"
.STR79:    .string "end"
.STR80:    .string "list_append"
.STR81:    .string "[PARSER WARNING] Expression statement (type="
.STR82:    .string ") - may not have intended effect"
.STR83:    .string "step"
.STR84:    .string "[PARSER ERROR] Expected 'type' keyword after 'of'"
.STR85:    .string "[PARSER ERROR] Expected type name after 'of Type'"
.STR86:    .string "[PARSER ERROR] Expected field name in When pattern"
.STR87:    .string "[PARSER ERROR] Expected binding name after 'as'"
.STR88:    .string "[WARNING] Match on type '"
.STR89:    .string "' is not exhaustive. Missing variants:"
.STR90:    .string "  - "
.STR91:    .string "[PARSER ERROR] Inline assembly block too large (max 8192 bytes)\n"
.STR92:    .string "End"
.STR93:    .string "Assembly"
.STR94:    .string "Byte"
.STR95:    .string "Short"
.STR96:    .string "Long"
.STR97:    .string "[PARSER WARNING] Unknown type '"
.STR98:    .string "', defaulting to 8 bytes"
.STR99:    .string "[PARSER ERROR] Expected type name at line "
.STR100:    .string " (got token type "
.STR101:    .string "[PARSER ERROR] Expected array size at line "
.STR102:    .string "[PARSER ERROR] Expected element type at line "
.STR103:    .string "[PARSER ERROR] Expected return type at line "
.STR104:    .string "[PARSER ERROR] Expected variant name at line "
.STR105:    .string "[PARSER ERROR] Expected field name in variant at line "
.STR106:    .string "[PARSER ERROR] Expected field type at line "
.STR107:    .string "[PARSER ERROR] Expected 'called' or type name after 'Type' at line "
.STR108:    .string "[PARSER ERROR] Expected function name string literal (type "
.STR109:    .string "), got type "
.STR110:    .string "[PARSER ERROR] Function name is NULL!"
.STR111:    .string "[PARSER ERROR] Expected parameter name at line "
.STR112:    .string "[PARSER ERROR] Expected parameter name after separator at line "
.STR113:    .string "Nothing"
.STR114:    .string "[PARSER ERROR] Unrecognized statement at line "
.STR115:    .string " (token type "
.STR116:    .string "[ERROR] lexer_next_token returned NULL!"
.STR117:    .string "[PARSER ERROR] First token is already EOF (input file is empty or unreadable)"
.STR118:    .string "[ERROR] current_token is NULL!"
.STR119:    .string "[ERROR] parser_parse_import returned NULL!"
.STR120:    .string "Use"
.STR121:    .string "[PARSER ERROR] Expected 'Process' after 'Export'"
.STR122:    .string "[ERROR] parser_parse_function returned NULL!"
.STR123:    .string "[PARSER ERROR] Expected string literal or identifier after Import, got token type "
.text


.globl token_can_be_identifier
token_can_be_identifier:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2
.L1:
    movq -8(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
    movq -8(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
    movq -8(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
    movq -8(%rbp), %rax
    pushq %rax
    movq $151, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
    movq -8(%rbp), %rax
    pushq %rax
    movq $152, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
    movq -8(%rbp), %rax
    pushq %rax
    movq $153, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
    movq -8(%rbp), %rax
    pushq %rax
    movq $154, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
    movq -8(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
    movq -8(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
    movq -8(%rbp), %rax
    pushq %rax
    movq $145, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
    movq -8(%rbp), %rax
    pushq %rax
    movq $159, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L112
.L111:
    movq -8(%rbp), %rax
    pushq %rax
    movq $160, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L122
.L121:
    movq -8(%rbp), %rax
    pushq %rax
    movq $155, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L132
.L131:
    movq -8(%rbp), %rax
    pushq %rax
    movq $132, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L142
.L141:
    movq -8(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L152
.L151:
    movq -8(%rbp), %rax
    pushq %rax
    movq $129, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L161
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L162
.L161:
    movq -8(%rbp), %rax
    pushq %rax
    movq $126, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L172
.L171:
    movq -8(%rbp), %rax
    pushq %rax
    movq $177, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L182
.L181:
    movq -8(%rbp), %rax
    pushq %rax
    movq $178, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L192
.L191:
    movq -8(%rbp), %rax
    pushq %rax
    movq $175, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L202
.L201:
    movq -8(%rbp), %rax
    pushq %rax
    movq $176, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L212
.L211:
    movq -8(%rbp), %rax
    pushq %rax
    movq $179, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L222
.L221:
    movq -8(%rbp), %rax
    pushq %rax
    movq $174, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L231
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L232
.L231:
    movq -8(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L242
.L241:
    movq -8(%rbp), %rax
    pushq %rax
    movq $180, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L251
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L252
.L251:
    movq -8(%rbp), %rax
    pushq %rax
    movq $181, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L262
.L261:
    movq -8(%rbp), %rax
    pushq %rax
    movq $182, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L272
.L271:
    movq -8(%rbp), %rax
    pushq %rax
    movq $39, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L282
.L281:
    movq -8(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L292
.L291:
    movq -8(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L302
.L301:
    movq -8(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L312
.L311:
    movq -8(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L322
.L321:
    movq -8(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L331
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L332
.L331:
    movq -8(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L341
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L342
.L341:
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L352
.L351:
    movq -8(%rbp), %rax
    pushq %rax
    movq $15, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L362
.L361:
    movq -8(%rbp), %rax
    pushq %rax
    movq $21, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L372
.L371:
    movq -8(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L382
.L381:
    movq -8(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L391
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L392
.L391:
    movq -8(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L402
.L401:
    movq -8(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L412
.L411:
    movq -8(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L422
.L421:
    movq -8(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L431
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L432
.L431:
    movq -8(%rbp), %rax
    pushq %rax
    movq $162, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L442
.L441:
    movq -8(%rbp), %rax
    pushq %rax
    movq $164, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L451
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L452
.L451:
    movq -8(%rbp), %rax
    pushq %rax
    movq $183, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L462
.L461:
    movq -8(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L471
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L472
.L471:
    movq -8(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L482
.L481:
    movq -8(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L491
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L492
.L491:
.L492:
.L482:
.L472:
.L462:
.L452:
.L442:
.L432:
.L422:
.L412:
.L402:
.L392:
.L382:
.L372:
.L362:
.L352:
.L342:
.L332:
.L322:
.L312:
.L302:
.L292:
.L282:
.L272:
.L262:
.L252:
.L242:
.L232:
.L222:
.L212:
.L202:
.L192:
.L182:
.L172:
.L162:
.L152:
.L142:
.L132:
.L122:
.L112:
.L102:
.L92:
.L82:
.L72:
.L62:
.L52:
.L42:
.L32:
.L22:
.L12:
.L2:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_expression
parser_parse_expression:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_logical_or
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_logical_or
parser_parse_logical_or:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_logical_and
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L501:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L502
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L511
    movq $31, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_logical_and
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $31, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L512
.L511:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L512:
    jmp .L501
.L502:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_logical_and
parser_parse_logical_and:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L521:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L522
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $30, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L532
.L531:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L532:
    jmp .L521
.L522:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_comparison_level
parser_parse_comparison_level:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_additive
parser_parse_additive:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_multiplicative
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L541:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L542
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L551
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_multiplicative
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L552
.L551:
    movq -40(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L561
    movq $17, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_multiplicative
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq $17, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L562
.L561:
    movq -40(%rbp), %rax
    pushq %rax
    movq $182, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq $182, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_multiplicative
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -64(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L572
.L571:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L572:
.L562:
.L552:
    jmp .L541
.L542:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_multiplicative
parser_parse_multiplicative:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L581:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L582
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
    movq $35, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L592
.L591:
    movq -40(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L601
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $36, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L602
.L601:
    movq -40(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L611
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $37, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L612
.L611:
    movq -40(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L621
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $42, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L622
.L621:
    movq -40(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $43, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L632
.L631:
    movq -40(%rbp), %rax
    pushq %rax
    movq $39, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L641
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $39, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L642
.L641:
    movq -40(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L651
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L652
.L651:
    movq -40(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L661
    movq -40(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $41, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L662
.L661:
    movq -40(%rbp), %rax
    pushq %rax
    movq $175, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L671
    movq $175, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -72(%rbp)
    movq $39, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -72(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L681
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $39, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L682
.L681:
    movq -72(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L691
    movq $31, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $40, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L692
.L691:
    movq $8, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L701
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L702
.L701:
.L702:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $41, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L712
.L711:
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L712:
.L692:
.L682:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $38, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L722
.L721:
.L722:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L672
.L671:
    movq -40(%rbp), %rax
    pushq %rax
    movq $176, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L731
    movq $176, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $177, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L741
    movq $177, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $42, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L742
.L741:
.L742:
    movq -120(%rbp), %rax
    pushq %rax
    movq $178, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    movq $178, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $43, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L752
.L751:
.L752:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L732
.L731:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L732:
.L672:
.L662:
.L652:
.L642:
.L632:
.L622:
.L612:
.L602:
.L592:
    jmp .L581
.L582:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_primary_with_postfix
parser_parse_primary_with_postfix:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -16(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L761
    movq $148, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L771
    movq $149, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L772
.L771:
.L772:
    movq -48(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L781
    movq $150, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L782
.L781:
.L782:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -56(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -64(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    leaq .STR2(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L762
.L761:
.L762:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L791
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq EXPR_VARIABLE(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L801
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -104(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq $4, %rax
    movq %rax, -120(%rbp)
    movq $8, %rax
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -144(%rbp)
.L811:    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L812
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L821
    movq $0, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L822
.L821:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -168(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L831
    movq -120(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -120(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L832
.L831:
.L832:
    movq -112(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -184(%rbp)
    movq -104(%rbp), %rax
    addq -184(%rbp), %rax
    movq %rax, -192(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -112(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L841
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L842
.L841:
.L842:
.L822:
    jmp .L811
.L812:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -112(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -216(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -216(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L802
.L801:
.L802:
    jmp .L792
.L791:
.L792:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L851
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L861:    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L862
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -232(%rbp)
    movq $0, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -240(%rbp)
    movq $0, %rax
    movq %rax, -248(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L872
.L871:
.L872:
    movq -240(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L881
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L892
.L891:
.L892:
    jmp .L882
.L881:
.L882:
    movq -248(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L901
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -264(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    addq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -112(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L902
.L901:
    movq $0, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L902:
    jmp .L861
.L862:
    movq -112(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call with_promote_to_call_or_lambda
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L852
.L851:
.L852:
    movq $1, %rax
    movq %rax, -272(%rbp)
.L911:    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L912
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L921
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq -304(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    leaq .STR3(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    jmp .L942
.L941:
.L942:
    jmp .L932
.L931:
.L932:
    movq $8, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -336(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L951
    movq -304(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L952
.L951:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L952:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq $0, %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq EXPR_VARIABLE(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L971
    leaq .STR4(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L972
.L971:
.L972:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -368(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -376(%rbp)
    movq $0, %rax
    movq %rax, -384(%rbp)
    movq $4, %rax
    movq %rax, -392(%rbp)
    movq $8, %rax
    movq %rax, -400(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq -400(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -416(%rbp)
.L981:    movq -416(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L982
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -424(%rbp)
    movq $0, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L991
    movq $0, %rax
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L992
.L991:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -440(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq -400(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -448(%rbp)
    movq -376(%rbp), %rax
    addq -448(%rbp), %rax
    movq %rax, -456(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -384(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -464(%rbp)
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -472(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1002
.L1001:
.L1002:
.L992:
    jmp .L981
.L982:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -480(%rbp)
    movq EXPR_QUALIFIED_CALL(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -368(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -336(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -376(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -384(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -480(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L962
.L961:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -488(%rbp)
    movq $0, %rax
    movq %rax, -496(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1011
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -512(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1021
    movq $40, %rax
    pushq %rax
    movq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -520(%rbp)
    movq $32, %rax
    pushq %rax
    movq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -528(%rbp)
    movq -528(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq $0, %rax
    movq %rax, -536(%rbp)
.L1041:    movq -536(%rbp), %rax
    pushq %rax
    movq -520(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1042
    movq -536(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -544(%rbp)
    movq -544(%rbp), %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -552(%rbp)
    movq -552(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq $8, %rax
    pushq %rax
    movq -552(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -560(%rbp)
    movq -504(%rbp), %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq $1, %rax
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -520(%rbp), %rax
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1062
.L1061:
.L1062:
    jmp .L1052
.L1051:
.L1052:
    movq -536(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1041
.L1042:
    jmp .L1032
.L1031:
.L1032:
    jmp .L1022
.L1021:
.L1022:
    jmp .L1012
.L1011:
.L1012:
    movq -496(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1072
.L1071:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -568(%rbp)
    movq $6, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -336(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -568(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1072:
.L962:
    jmp .L922
.L921:
.L922:
    movq -288(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1081
    movq $148, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -288(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -576(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq $1, %rax
    pushq %rax
    leaq -576(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1092
.L1091:
.L1092:
    movq -288(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq $1, %rax
    pushq %rax
    leaq -576(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1102
.L1101:
.L1102:
    movq -576(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq -288(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -584(%rbp)
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -592(%rbp)
    movq $16, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -584(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -592(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1112
.L1111:
    leaq .STR5(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -600(%rbp)
    movq -600(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L1112:
    jmp .L1082
.L1081:
.L1082:
    movq -288(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    movq -288(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    movq $0, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1132
.L1131:
.L1132:
    jmp .L1122
.L1121:
.L1122:
    jmp .L911
.L912:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -608(%rbp)
    movq $0, %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -616(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1141
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -624(%rbp)
    movq $0, %rax
    movq %rax, -632(%rbp)
    movq $4, %rax
    movq %rax, -640(%rbp)
    movq -640(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -624(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -656(%rbp)
    movq -656(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -624(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -632(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -664(%rbp)
.L1151:    movq -664(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1152
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -672(%rbp)
    movq $0, %rax
    pushq %rax
    movq -672(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -680(%rbp)
    movq $0, %rax
    movq %rax, -688(%rbp)
    movq -680(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1161
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -688(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1162
.L1161:
.L1162:
    movq -680(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1171
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -696(%rbp)
    movq -696(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1181
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -688(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1182
.L1181:
.L1182:
    jmp .L1172
.L1171:
.L1172:
    movq -688(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1191
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -704(%rbp)
    movq -632(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -712(%rbp)
    movq -704(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -624(%rbp), %rax
    addq -712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -632(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -632(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1192
.L1191:
    movq $0, %rax
    pushq %rax
    leaq -664(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1192:
    jmp .L1151
.L1152:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -720(%rbp)
    movq -720(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -728(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -736(%rbp)
    movq $0, %rax
    pushq %rax
    movq -728(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -744(%rbp)
    movq -744(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1211
    movq $8, %rax
    pushq %rax
    movq -728(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -752(%rbp)
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -760(%rbp)
    movq EXPR_QUALIFIED_CALL(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -752(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -736(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -624(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -632(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -760(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1212
.L1211:
    movq -632(%rbp), %rax
    pushq %rax
    movq -624(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call with_promote_to_call_or_lambda
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1212:
    jmp .L1202
.L1201:
    movq -632(%rbp), %rax
    pushq %rax
    movq -624(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call with_promote_to_call_or_lambda
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1202:
    jmp .L1142
.L1141:
.L1142:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_comparison
parser_parse_comparison:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $21, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    movq $21, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1231
    movq $29, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1232
.L1231:
.L1232:
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $22, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    movq $22, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1251
    movq $23, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1252
.L1251:
    movq $22, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1252:
    jmp .L1242
.L1241:
.L1242:
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1261
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1271
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1281
    movq $31, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $22, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1291
    movq $25, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1292
.L1291:
    movq $27, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1292:
    jmp .L1282
.L1281:
.L1282:
    movq -96(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
    movq $26, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1312
.L1311:
    movq $24, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1312:
    jmp .L1302
.L1301:
.L1302:
    jmp .L1272
.L1271:
.L1272:
    movq -80(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
    leaq .STR6(%rip), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1322
.L1321:
.L1322:
    jmp .L1262
.L1261:
.L1262:
    movq -48(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
    movq $25, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -96(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1351
    movq $31, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $22, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1361
    movq $24, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1362
.L1361:
    movq $26, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1362:
    jmp .L1352
.L1351:
.L1352:
    movq -96(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1371
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1381
    movq $27, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1382
.L1381:
    movq $25, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1382:
    jmp .L1372
.L1371:
.L1372:
    jmp .L1342
.L1341:
.L1342:
    movq -80(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1391
    leaq .STR7(%rip), %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1392
.L1391:
.L1392:
    jmp .L1332
.L1331:
.L1332:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1401
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1411
    movq $23, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1412
.L1411:
    movq $22, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1412:
    jmp .L1402
.L1401:
.L1402:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -128(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -136(%rbp)
    movq $0, %rax
    movq %rax, -144(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1421
    leaq .STR8(%rip), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1431
    movq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1432
.L1431:
.L1432:
    leaq .STR9(%rip), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1441
    movq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1442
.L1441:
.L1442:
    jmp .L1422
.L1421:
.L1422:
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1451
    movq -128(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_comparison
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1452
.L1451:
.L1452:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_comparison
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1222
.L1221:
.L1222:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1461
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1471
    leaq .STR10(%rip), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1481
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $22, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_comparison
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1482
.L1481:
.L1482:
    leaq .STR11(%rip), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1491
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1501
    movq $29, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $23, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_comparison
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1502
.L1501:
.L1502:
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1511
    leaq .STR12(%rip), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1521
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $22, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_comparison
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1522
.L1521:
.L1522:
    jmp .L1512
.L1511:
.L1512:
    jmp .L1492
.L1491:
.L1492:
    jmp .L1472
.L1471:
.L1472:
    jmp .L1462
.L1461:
.L1462:
    movq -32(%rbp), %rax
    pushq %rax
    movq $179, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1531
    movq $179, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    leaq .STR13(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -240(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1541
    movq $150, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    leaq .STR14(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1542
.L1541:
.L1542:
    movq -256(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1551
    movq $149, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1552
.L1551:
.L1552:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -264(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -272(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1532
.L1531:
.L1532:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_let_statement
parser_parse_let_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1561
    leaq .STR15(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1562
.L1561:
.L1562:
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1571
    leaq .STR16(%rip), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1572
.L1571:
.L1572:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -64(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1581
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1591
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1592
.L1591:
.L1592:
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1601
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1602
.L1601:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1602:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq $0, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1611
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -152(%rbp)
    movq $8, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1621
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1622
.L1621:
.L1622:
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1631
    movq -152(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1632
.L1631:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1632:
    jmp .L1612
.L1611:
.L1612:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1641
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -192(%rbp)
.L1651:    movq -192(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1652
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -184(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1661
    movq -192(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1662
.L1661:
.L1662:
    movq -184(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1671
    movq -192(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1672
.L1671:
.L1672:
    movq -184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1651
.L1652:
    jmp .L1642
.L1641:
.L1642:
    jmp .L1582
.L1581:
.L1582:
    movq $13, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1681
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1682
.L1681:
.L1682:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_create_let
    movq %rax, -208(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1691
    movq -88(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_set_let_type
    jmp .L1692
.L1691:
.L1692:
    movq -208(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_implicit_compound_assign
parser_parse_implicit_compound_assign:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -40(%rbp)
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call statement_create_compound_assign
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_set_statement
parser_parse_set_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $14, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $136, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1701
    movq $136, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $137, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1711
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $137, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1712
.L1711:
.L1712:
    movq -32(%rbp), %rax
    pushq %rax
    movq $138, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1721
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $138, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1722
.L1721:
.L1722:
    movq -32(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1731
    movq $2, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $35, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1732
.L1731:
.L1732:
    movq -32(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1741
    movq $2, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $141, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1742
.L1741:
.L1742:
    movq -32(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1751
    movq $3, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $36, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1752
.L1751:
.L1752:
    movq -32(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1761
    movq $3, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $142, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1762
.L1761:
.L1762:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1771
    movq -32(%rbp), %rax
    pushq %rax
    movq $137, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1781
    leaq .STR18(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR19(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1782
.L1781:
.L1782:
    jmp .L1772
.L1771:
.L1772:
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call statement_create_compound_assign
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1702
.L1701:
.L1702:
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_create_set
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_duplicate_parser
string_duplicate_parser:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1791
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1792
.L1791:
.L1792:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    addq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_copy
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_advance
parser_advance:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_eat
parser_eat:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1801
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -40(%rbp)
    jmp .L1802
.L1801:
    leaq .STR20(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR21(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR22(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L1802:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_call_statement
parser_parse_call_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $183, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1811
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1812
.L1811:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1812:
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1821
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq $8, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1831
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1832
.L1831:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1832:
    jmp .L1822
.L1821:
.L1822:
    movq $0, %rax
    movq %rax, -96(%rbp)
    movq $0, %rax
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1841
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -128(%rbp)
.L1851:    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1852
    movq -104(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1861
    movq -112(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -120(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1862
.L1861:
.L1862:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -136(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -144(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -104(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1871
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -168(%rbp)
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1881
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1882
.L1881:
.L1882:
    jmp .L1872
.L1871:
    movq -160(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1891
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1892
.L1891:
    movq $0, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1892:
.L1872:
    jmp .L1851
.L1852:
    jmp .L1842
.L1841:
.L1842:
    movq $0, %rax
    movq %rax, -184(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1901
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $25, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -104(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L1902
.L1901:
    movq -104(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1902:
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_peek_struct_field_after_comma
parser_peek_struct_field_after_comma:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $12, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $20, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    movq %rax, -56(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1911
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1921
    movq $1, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1922
.L1921:
.L1922:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1931
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1941
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1951
    movq $1, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1952
.L1951:
.L1952:
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L1942
.L1941:
.L1942:
    jmp .L1932
.L1931:
.L1932:
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L1912
.L1911:
.L1912:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_a_value_of_type
parser_parse_a_value_of_type:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1961
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1962
.L1961:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1962:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1971
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1972
.L1971:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1972:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1981
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -88(%rbp)
.L1991:    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1992
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2001
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2002
.L2001:
    movq -104(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2011
    movq -88(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $128, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2012
.L2011:
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2021
    movq $0, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2022
.L2021:
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2022:
.L2012:
.L2002:
    jmp .L1991
.L1992:
    jmp .L1982
.L1981:
.L1982:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    movq %rax, -128(%rbp)
    movq $0, %rax
    movq %rax, -136(%rbp)
    movq $0, %rax
    movq %rax, -144(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2031
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $128, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $128, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -152(%rbp)
.L2041:    movq -152(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2042
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $0, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -176(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2051
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2052
.L2051:
.L2052:
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    movq $0, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2062
.L2061:
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -192(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -200(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -208(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -200(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -128(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2071
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2072
.L2071:
    movq $0, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2072:
.L2062:
    jmp .L2041
.L2042:
    jmp .L2032
.L2031:
.L2032:
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -232(%rbp)
    movq $20, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -136(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -144(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -128(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -232(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_proc_expression
parser_parse_proc_expression:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $171, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2081
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2082
.L2081:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2082:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2091
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -32(%rbp), %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq $8, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2101
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2102
.L2101:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2102:
    jmp .L2092
.L2091:
.L2092:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2111
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -120(%rbp)
    movq $8, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2121
    movq -120(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2122
.L2121:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2122:
    jmp .L2112
.L2111:
.L2112:
    movq -32(%rbp), %rax
    movq %rax, -136(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2131
    leaq .STR23(%rip), %rax
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -152(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2132
.L2131:
.L2132:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -160(%rbp)
    movq $0, %rax
    movq %rax, -168(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2141
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -192(%rbp)
.L2151:    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2152
    movq -168(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2161
    movq -176(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -184(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2162
.L2161:
.L2162:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -200(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -208(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -168(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2171
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2181
    movq $0, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2182
.L2181:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2182:
    jmp .L2172
.L2171:
    movq $0, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2172:
    jmp .L2151
.L2152:
    jmp .L2142
.L2141:
.L2142:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2191
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -240(%rbp)
    movq $25, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -168(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -240(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2192
.L2191:
.L2192:
    movq -168(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret


.globl with_promote_to_call_or_lambda
with_promote_to_call_or_lambda:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2201
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -48(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2202
.L2201:
.L2202:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -56(%rbp)
    movq $24, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_a_list_literal
parser_parse_a_list_literal:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $174, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2211
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2212
.L2211:
.L2212:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2221
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2231
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2232
.L2231:
.L2232:
    jmp .L2222
.L2221:
.L2222:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2241
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -56(%rbp)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2242
.L2241:
.L2242:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2251
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2252
.L2251:
.L2252:
    movq $128, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq $16, %rax
    movq %rax, -96(%rbp)
    movq $1, %rax
    movq %rax, -104(%rbp)
.L2261:    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2262
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2271
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2272
.L2271:
.L2272:
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2281
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2282
.L2281:
.L2282:
    movq -120(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2291
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2292
.L2291:
.L2292:
    movq -120(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2301
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2302
.L2301:
.L2302:
    movq -120(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2311
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2312
.L2311:
.L2312:
    movq -120(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2321
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2322
.L2321:
.L2322:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2331
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2332
.L2331:
.L2332:
    movq -120(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2341
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2342
.L2341:
.L2342:
    movq -120(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2351
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2352
.L2351:
.L2352:
    movq -120(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2361
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2362
.L2361:
.L2362:
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2371
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2372
.L2371:
    movq -88(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2381
    movq -96(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2382
.L2381:
.L2382:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -144(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $0, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2391
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2401
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2402
.L2401:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2402:
    jmp .L2392
.L2391:
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2392:
.L2372:
    jmp .L2261
.L2262:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2411
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq $12, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq $16, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -224(%rbp)
    movq $20, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -232(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -240(%rbp)
    movq $0, %rax
    movq %rax, -248(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2421
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -256(%rbp)
    movq $8, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2431
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2441
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2451
    movq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2452
.L2451:
.L2452:
    jmp .L2442
.L2441:
.L2442:
    jmp .L2432
.L2431:
.L2432:
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L2422
.L2421:
.L2422:
    movq -208(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -216(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -224(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -232(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -248(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2461
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2462
.L2461:
.L2462:
    jmp .L2412
.L2411:
.L2412:
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -272(%rbp)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -88(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -272(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_a_dictionary_literal
parser_parse_a_dictionary_literal:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $174, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2472
.L2471:
.L2472:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2481
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2491
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2492
.L2491:
.L2492:
    jmp .L2482
.L2481:
.L2482:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -56(%rbp)
    movq $22, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2502
.L2501:
.L2502:
    movq -32(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2511
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2512
.L2511:
.L2512:
    movq $8, %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    movq %rax, -96(%rbp)
    movq $1, %rax
    movq %rax, -104(%rbp)
.L2521:    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2522
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2531
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2532
.L2531:
.L2532:
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2542
.L2541:
.L2542:
    movq -120(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2551
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2552
.L2551:
.L2552:
    movq -120(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2561
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2562
.L2561:
.L2562:
    movq -120(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2572
.L2571:
.L2572:
    movq -120(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2581
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2582
.L2581:
.L2582:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2591
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2592
.L2591:
.L2592:
    movq -120(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2601
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2602
.L2601:
.L2602:
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2611
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2612
.L2611:
    movq -96(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2621
    movq -64(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -72(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -72(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2622
.L2621:
.L2622:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -136(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2631
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2632
.L2631:
.L2632:
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -168(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -176(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -168(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2652
.L2651:
.L2652:
    jmp .L2642
.L2641:
    movq -192(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2662
.L2661:
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2662:
.L2642:
.L2612:
    jmp .L2521
.L2522:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2671
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -232(%rbp)
    movq $8, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -240(%rbp)
    movq $12, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -248(%rbp)
    movq $16, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq $20, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -264(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -272(%rbp)
    movq $0, %rax
    movq %rax, -280(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2681
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -288(%rbp)
    movq $8, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $160, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2691
    movq $1, %rax
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2692
.L2691:
.L2692:
    movq -288(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq -296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2711
    leaq .STR27(%rip), %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2721
    movq $1, %rax
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2722
.L2721:
.L2722:
    jmp .L2712
.L2711:
.L2712:
    jmp .L2702
.L2701:
.L2702:
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L2682
.L2681:
.L2682:
    movq -240(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -248(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -256(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -264(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2731
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -304(%rbp)
    movq $0, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2732
.L2731:
.L2732:
    jmp .L2672
.L2671:
.L2672:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -320(%rbp)
    movq $22, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -88(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -320(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_is_builtin_function_token
parser_is_builtin_function_token:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $54, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2741
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2742
.L2741:
    movq -8(%rbp), %rax
    pushq %rax
    movq $55, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2751
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2752
.L2751:
    movq -8(%rbp), %rax
    pushq %rax
    movq $57, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2761
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2762
.L2761:
    movq -8(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2771
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2772
.L2771:
    movq -8(%rbp), %rax
    pushq %rax
    movq $59, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2781
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2782
.L2781:
    movq -8(%rbp), %rax
    pushq %rax
    movq $60, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2791
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2792
.L2791:
    movq -8(%rbp), %rax
    pushq %rax
    movq $61, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2801
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2802
.L2801:
    movq -8(%rbp), %rax
    pushq %rax
    movq $62, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2811
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2812
.L2811:
    movq -8(%rbp), %rax
    pushq %rax
    movq $63, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2821
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2822
.L2821:
    movq -8(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2831
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2832
.L2831:
    movq -8(%rbp), %rax
    pushq %rax
    movq $65, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2841
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2842
.L2841:
    movq -8(%rbp), %rax
    pushq %rax
    movq $66, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2851
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2852
.L2851:
    movq -8(%rbp), %rax
    pushq %rax
    movq $67, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2861
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2862
.L2861:
    movq -8(%rbp), %rax
    pushq %rax
    movq $68, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2871
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2872
.L2871:
    movq -8(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2881
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2882
.L2881:
    movq -8(%rbp), %rax
    pushq %rax
    movq $70, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2891
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2892
.L2891:
    movq -8(%rbp), %rax
    pushq %rax
    movq $71, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2901
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2902
.L2901:
    movq -8(%rbp), %rax
    pushq %rax
    movq $72, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2911
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2912
.L2911:
    movq -8(%rbp), %rax
    pushq %rax
    movq $73, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2921
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2922
.L2921:
    movq -8(%rbp), %rax
    pushq %rax
    movq $74, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2931
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2932
.L2931:
    movq -8(%rbp), %rax
    pushq %rax
    movq $75, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2941
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2942
.L2941:
    movq -8(%rbp), %rax
    pushq %rax
    movq $76, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2951
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2952
.L2951:
    movq -8(%rbp), %rax
    pushq %rax
    movq $77, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2961
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2962
.L2961:
    movq -8(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2971
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2972
.L2971:
    movq -8(%rbp), %rax
    pushq %rax
    movq $79, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2981
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2982
.L2981:
    movq -8(%rbp), %rax
    pushq %rax
    movq $80, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2991
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2992
.L2991:
    movq -8(%rbp), %rax
    pushq %rax
    movq $81, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3001
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3002
.L3001:
    movq -8(%rbp), %rax
    pushq %rax
    movq $82, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3011
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3012
.L3011:
    movq -8(%rbp), %rax
    pushq %rax
    movq $83, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3021
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3022
.L3021:
    movq -8(%rbp), %rax
    pushq %rax
    movq $84, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3031
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3032
.L3031:
    movq -8(%rbp), %rax
    pushq %rax
    movq $85, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3041
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3042
.L3041:
    movq -8(%rbp), %rax
    pushq %rax
    movq $86, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3051
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3052
.L3051:
    movq -8(%rbp), %rax
    pushq %rax
    movq $87, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3061
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3062
.L3061:
    movq -8(%rbp), %rax
    pushq %rax
    movq $88, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3071
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3072
.L3071:
    movq -8(%rbp), %rax
    pushq %rax
    movq $89, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3081
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3082
.L3081:
    movq -8(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3091
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3092
.L3091:
    movq -8(%rbp), %rax
    pushq %rax
    movq $91, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3101
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3102
.L3101:
    movq -8(%rbp), %rax
    pushq %rax
    movq $92, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3111
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3112
.L3111:
    movq -8(%rbp), %rax
    pushq %rax
    movq $93, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3121
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3122
.L3121:
    movq -8(%rbp), %rax
    pushq %rax
    movq $94, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3131
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3132
.L3131:
    movq -8(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3141
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3142
.L3141:
    movq -8(%rbp), %rax
    pushq %rax
    movq $96, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3151
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3152
.L3151:
    movq -8(%rbp), %rax
    pushq %rax
    movq $97, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3161
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3162
.L3161:
    movq -8(%rbp), %rax
    pushq %rax
    movq $98, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3171
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3172
.L3171:
    movq -8(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3181
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3182
.L3181:
    movq -8(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3191
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3192
.L3191:
    movq -8(%rbp), %rax
    pushq %rax
    movq $101, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3201
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3202
.L3201:
    movq -8(%rbp), %rax
    pushq %rax
    movq $102, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3211
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3212
.L3211:
    movq -8(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3221
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3222
.L3221:
    movq -8(%rbp), %rax
    pushq %rax
    movq $104, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3231
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3232
.L3231:
    movq -8(%rbp), %rax
    pushq %rax
    movq $105, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3241
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3242
.L3241:
    movq -8(%rbp), %rax
    pushq %rax
    movq $106, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3251
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3252
.L3251:
    movq -8(%rbp), %rax
    pushq %rax
    movq $107, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3261
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3262
.L3261:
    movq -8(%rbp), %rax
    pushq %rax
    movq $108, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3271
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3272
.L3271:
    movq -8(%rbp), %rax
    pushq %rax
    movq $109, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3281
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3282
.L3281:
    movq -8(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3291
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3292
.L3291:
    movq -8(%rbp), %rax
    pushq %rax
    movq $115, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3301
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3302
.L3301:
    movq -8(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3311
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3312
.L3311:
    movq -8(%rbp), %rax
    pushq %rax
    movq $117, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3321
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3322
.L3321:
    movq -8(%rbp), %rax
    pushq %rax
    movq $118, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3331
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3332
.L3331:
    movq -8(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3341
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3342
.L3341:
    movq -8(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3351
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3352
.L3351:
    movq -8(%rbp), %rax
    pushq %rax
    movq $130, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3361
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3362
.L3361:
    movq -8(%rbp), %rax
    pushq %rax
    movq $131, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3371
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3372
.L3371:
.L3372:
.L3362:
.L3352:
.L3342:
.L3332:
.L3322:
.L3312:
.L3302:
.L3292:
.L3282:
.L3272:
.L3262:
.L3252:
.L3242:
.L3232:
.L3222:
.L3212:
.L3202:
.L3192:
.L3182:
.L3172:
.L3162:
.L3152:
.L3142:
.L3132:
.L3122:
.L3112:
.L3102:
.L3092:
.L3082:
.L3072:
.L3062:
.L3052:
.L3042:
.L3032:
.L3022:
.L3012:
.L3002:
.L2992:
.L2982:
.L2972:
.L2962:
.L2952:
.L2942:
.L2932:
.L2922:
.L2912:
.L2902:
.L2892:
.L2882:
.L2872:
.L2862:
.L2852:
.L2842:
.L2832:
.L2822:
.L2812:
.L2802:
.L2792:
.L2782:
.L2772:
.L2762:
.L2752:
.L2742:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_integer
expression_create_integer:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq EXPR_INTEGER(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_variable
expression_create_variable:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq EXPR_VARIABLE(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_binary_op
expression_create_binary_op:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq EXPR_BINARY_OP(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_comparison
expression_create_comparison:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq EXPR_COMPARISON(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_unary_op
expression_create_unary_op:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $32, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq $12, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_function_call
expression_create_function_call:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq EXPR_FUNCTION_CALL(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_string_literal_owned
expression_create_string_literal_owned:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq EXPR_STRING_LITERAL(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lambda_is_var_in_list
lambda_is_var_in_list:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
.L3381:    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3382
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3391
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3392
.L3391:
.L3392:
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3381
.L3382:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lambda_add_free_var
lambda_add_free_var:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
.L3401:    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3402
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3411
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3412
.L3411:
.L3412:
    movq -48(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3401
.L3402:
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3421
    movq $8, %rax
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3431
    movq -40(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3432
.L3431:
.L3432:
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
.L3441:    movq -88(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3442
    movq -88(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3441
.L3442:
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3451
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3452
.L3451:
.L3452:
    movq -80(%rbp), %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -72(%rbp), %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L3422
.L3421:
.L3422:
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lambda_collect_free_vars
lambda_collect_free_vars:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3461
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3462
.L3461:
.L3462:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3471
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call lambda_is_var_in_list
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3481
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call lambda_add_free_var
    jmp .L3482
.L3481:
.L3482:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3472
.L3471:
.L3472:
    movq -40(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3491
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3492
.L3491:
.L3492:
    movq -40(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3501
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    movq %rax, -96(%rbp)
.L3511:    movq -96(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3512
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq -96(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3511
.L3512:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3502
.L3501:
.L3502:
    movq -40(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3521
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3522
.L3521:
.L3522:
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3531
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -136(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3532
.L3531:
.L3532:
    movq -40(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3541
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq $0, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3551:    movq -96(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3552
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -104(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq -96(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3551
.L3552:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3542
.L3541:
.L3542:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_lambda
expression_create_lambda:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $32, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq EXPR_LAMBDA(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_lambda_multi
expression_create_lambda_multi:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $48, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq EXPR_LAMBDA(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_let
statement_create_let:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $32, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq STMT_LET(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_set_let_type
statement_set_let_type:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3561
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3562
.L3561:
.L3562:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3571
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3572
.L3571:
.L3572:
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_set
statement_create_set:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $24, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq STMT_SET(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_compound_assign
statement_create_compound_assign:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq STMT_COMPOUND_ASSIGN(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_for_range
statement_create_for_range:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq %r8, -40(%rbp)
    movq %r9, -48(%rbp)
    movq $56, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -64(%rbp)
    movq STMT_FOR(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $48, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_for_each
statement_create_for_each:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq $40, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -48(%rbp)
    movq STMT_FOR_EACH(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_return
statement_create_return:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $24, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq STMT_RETURN(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_print
statement_create_print:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $24, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq STMT_PRINT(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_expression
statement_create_expression:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $24, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq STMT_EXPRESSION(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_if
statement_create_if:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq %r8, -40(%rbp)
    movq $48, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -56(%rbp)
    movq STMT_IF(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_while
statement_create_while:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq STMT_WHILE(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_break
statement_create_break:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $8, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq STMT_BREAK(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_continue
statement_create_continue:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $8, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq STMT_CONTINUE(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_create
function_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $48, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_add_parameter
function_add_parameter:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
    movq $16, %rax
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -72(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_add_statement
function_add_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -32(%rbp)
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -64(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -64(%rbp), %rax
    addq -72(%rbp), %rax
    movq %rax, -80(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_create
program_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $64, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $48, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $56, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $60, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_function
program_add_function:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3581
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3591
    movq $128, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3592
.L3591:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3592:
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L3582
.L3581:
.L3582:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    addq -72(%rbp), %rax
    movq %rax, -80(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_global
program_add_global:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $60, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3601
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3611
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3612
.L3611:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3612:
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $60, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L3602
.L3601:
.L3602:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    addq -72(%rbp), %rax
    movq %rax, -80(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_type
program_add_type:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3621
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3631
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3632
.L3631:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3632:
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L3622
.L3621:
.L3622:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    addq -72(%rbp), %rax
    movq %rax, -80(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_import
program_add_import:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3641
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3651
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3652
.L3651:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3652:
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L3642
.L3641:
.L3642:
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    addq -72(%rbp), %rax
    movq %rax, -80(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_lookup_type_size
codegen_lookup_type_size:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3661
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3662
.L3661:
.L3662:
    leaq .STR28(%rip), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3671
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3672
.L3671:
.L3672:
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3681
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3682
.L3681:
.L3682:
    leaq .STR30(%rip), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3691
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3692
.L3691:
.L3692:
    leaq .STR31(%rip), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3701
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3702
.L3701:
.L3702:
    leaq .STR32(%rip), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3711
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3712
.L3711:
.L3712:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3721
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3722
.L3721:
.L3722:
    movq $24, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3731
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3732
.L3731:
.L3732:
    movq $0, %rax
    movq %rax, -48(%rbp)
.L3741:    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3742
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3751
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3761
    movq $40, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3762
.L3761:
.L3762:
    jmp .L3752
.L3751:
.L3752:
    movq -48(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3741
.L3742:
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_primary
parser_parse_primary:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3771
    leaq .STR33(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L3772
.L3771:
.L3772:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3781
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L3782
.L3781:
.L3782:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3791
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3801
    leaq .STR35(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3811
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -56(%rbp)
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3821
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3822
.L3821:
.L3822:
    movq -56(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_lookup_type_size
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3812
.L3811:
.L3812:
    jmp .L3802
.L3801:
.L3802:
    jmp .L3792
.L3791:
.L3792:
    movq -24(%rbp), %rax
    pushq %rax
    movq $155, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3831
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $155, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    movq %rax, -120(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $159, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3841
    movq $1, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3842
.L3841:
.L3842:
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3851
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3861
    movq $1, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3862
.L3861:
.L3862:
    jmp .L3852
.L3851:
.L3852:
    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3871
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_a_list_literal
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3872
.L3871:
.L3872:
    movq $0, %rax
    movq %rax, -128(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3881
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3882
.L3881:
.L3882:
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3891
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_a_dictionary_literal
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3892
.L3891:
.L3892:
    movq $0, %rax
    movq %rax, -136(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3901
    leaq .STR38(%rip), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3902
.L3901:
.L3902:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3911
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_a_value_of_type
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3912
.L3911:
.L3912:
    leaq .STR39(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3832
.L3831:
.L3832:
    movq -24(%rbp), %rax
    pushq %rax
    movq $171, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3921
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_proc_expression
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3922
.L3921:
.L3922:
    movq -24(%rbp), %rax
    pushq %rax
    movq $168, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3931
    movq $168, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -144(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -152(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -160(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -152(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    leaq .STR40(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3932
.L3931:
.L3932:
    movq -24(%rbp), %rax
    pushq %rax
    movq $170, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3941
    movq $170, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -168(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -176(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -184(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -176(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    leaq .STR41(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3942
.L3941:
.L3942:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3951
    movq -24(%rbp), %rax
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -208(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -216(%rbp)
    movq $0, %rax
    movq %rax, -224(%rbp)
    movq $0, %rax
    movq %rax, -232(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3961
    movq $2, %rax
    movq %rax, -256(%rbp)
    movq $8, %rax
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -280(%rbp)
.L3971:    movq -280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3972
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq $0, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3981
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -304(%rbp)
    jmp .L3982
.L3981:
.L3982:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -312(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3991
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3992
.L3991:
.L3992:
    movq -232(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -328(%rbp)
    movq -224(%rbp), %rax
    addq -328(%rbp), %rax
    movq %rax, -336(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -232(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq $0, %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4001
    movq $0, %rax
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4002
.L4001:
.L4002:
    jmp .L3971
.L3972:
    jmp .L3962
.L3961:
.L3962:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -360(%rbp)
    movq $32, %rax
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -376(%rbp)
    movq $8, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -224(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -232(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3952
.L3951:
.L3952:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4011
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -392(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -400(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4012
.L4011:
.L4012:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4021
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -408(%rbp)
    movq $0, %rax
    movq %rax, -416(%rbp)
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -424(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4031
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -432(%rbp)
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -440(%rbp)
    movq $0, %rax
    movq %rax, -448(%rbp)
.L4041:    movq -448(%rbp), %rax
    pushq %rax
    movq -432(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4042
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -448(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -440(%rbp), %rax
    addq -328(%rbp), %rax
    movq %rax, -456(%rbp)
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -464(%rbp)
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -472(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq -472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -480(%rbp)
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4051
    movq $1, %rax
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -432(%rbp), %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4052
.L4051:
    movq -448(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4052:
    jmp .L4041
.L4042:
    jmp .L4032
.L4031:
.L4032:
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -488(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4061
    movq $32, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq EXPR_TYPE_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -408(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4062
.L4061:
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_string_literal_owned
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4062:
    jmp .L4022
.L4021:
.L4022:
    movq -24(%rbp), %rax
    pushq %rax
    movq $157, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4071
    movq $157, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -496(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq $0, %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -512(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4081
    leaq .STR42(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -520(%rbp)
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4082
.L4081:
.L4082:
    movq $8, %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -528(%rbp)
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -536(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -544(%rbp)
    movq $32, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $10, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -536(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4072
.L4071:
.L4072:
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4091
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -552(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -552(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4092
.L4091:
.L4092:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4101
    movq $17, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -560(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -568(%rbp)
    movq -560(%rbp), %rax
    pushq %rax
    movq $17, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    movq %rax, -576(%rbp)
    movq -576(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4102
.L4101:
.L4102:
    movq -24(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4111
    movq $29, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -584(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq $29, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_create_unary_op
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4112
.L4111:
.L4112:
    movq -24(%rbp), %rax
    pushq %rax
    movq $151, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4121
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -592(%rbp)
    movq $151, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -600(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -600(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -608(%rbp)
    movq -608(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4131
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -616(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -624(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -624(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq -624(%rbp), %rax
    pushq %rax
    leaq .STR43(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4132
.L4131:
    leaq .STR44(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
.L4132:
    jmp .L4122
.L4121:
.L4122:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4141
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -632(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -640(%rbp)
    movq $0, %rax
    movq %rax, -648(%rbp)
    movq -640(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4151
    leaq .STR45(%rip), %rax
    pushq %rax
    movq -640(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -648(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4152
.L4151:
.L4152:
    movq -648(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4161
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -656(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -664(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4171
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -680(%rbp)
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -688(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -696(%rbp)
    movq $0, %rax
    movq %rax, -704(%rbp)
    movq $0, %rax
    movq %rax, -712(%rbp)
    movq -696(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4181
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -720(%rbp)
    movq -720(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -728(%rbp)
.L4191:    movq -728(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4192
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -736(%rbp)
    movq -736(%rbp), %rax
    pushq %rax
    movq -712(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -704(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -712(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -712(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -744(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -744(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -752(%rbp)
    movq -752(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4201
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4211
    movq $0, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4212
.L4211:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L4212:
    jmp .L4202
.L4201:
    movq $0, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4202:
    jmp .L4191
.L4192:
    jmp .L4182
.L4181:
.L4182:
    movq -712(%rbp), %rax
    pushq %rax
    movq -704(%rbp), %rax
    pushq %rax
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4172
.L4171:
.L4172:
    leaq .STR45(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4162
.L4161:
.L4162:
    jmp .L4142
.L4141:
.L4142:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4221
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -768(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -768(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -776(%rbp)
    movq $0, %rax
    movq %rax, -784(%rbp)
    movq -776(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4231
    leaq .STR46(%rip), %rax
    pushq %rax
    movq -776(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -784(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4232
.L4231:
.L4232:
    movq -784(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4241
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -792(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -792(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -800(%rbp)
    movq -800(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4251
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -808(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -816(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -824(%rbp)
    movq -824(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4261
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -832(%rbp)
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -840(%rbp)
    movq $24, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -848(%rbp)
    movq -808(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -848(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -832(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -848(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -840(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -848(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -848(%rbp), %rax
    pushq %rax
    leaq .STR47(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4262
.L4261:
.L4262:
    movq -808(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4252
.L4251:
.L4252:
    leaq .STR46(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4242
.L4241:
.L4242:
    jmp .L4222
.L4221:
.L4222:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4271
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -856(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -856(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -864(%rbp)
    movq $0, %rax
    movq %rax, -872(%rbp)
    movq -864(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4281
    leaq .STR48(%rip), %rax
    pushq %rax
    movq -864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -872(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4282
.L4281:
.L4282:
    movq -872(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4291
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -880(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -888(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -896(%rbp)
    movq $0, %rax
    movq %rax, -904(%rbp)
    movq -896(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4301
    leaq .STR49(%rip), %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -904(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4302
.L4301:
.L4302:
    movq -904(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4311
    movq -888(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -912(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -912(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -920(%rbp)
    movq -920(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4321
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -928(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -936(%rbp)
    movq -928(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -936(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq -936(%rbp), %rax
    pushq %rax
    leaq .STR50(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4322
.L4321:
.L4322:
    leaq .STR49(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4312
.L4311:
.L4312:
    leaq .STR48(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4292
.L4291:
.L4292:
    jmp .L4272
.L4271:
.L4272:
    movq -24(%rbp), %rax
    pushq %rax
    movq $175, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4331
    movq $175, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -944(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -944(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -952(%rbp)
    movq -952(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4341
    movq $29, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -960(%rbp)
    movq $0, %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -968(%rbp)
    movq -968(%rbp), %rax
    pushq %rax
    movq $41, %rax
    pushq %rax
    movq -960(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    movq %rax, -976(%rbp)
    movq -976(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4342
.L4341:
.L4342:
    jmp .L4332
.L4331:
.L4332:
    movq -24(%rbp), %rax
    pushq %rax
    movq $158, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4351
    movq $158, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4361
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -984(%rbp)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4362
.L4361:
.L4362:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -992(%rbp)
    movq -992(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1000(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4371
    leaq .STR52(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4372
.L4371:
.L4372:
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -1008(%rbp)
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1016(%rbp)
    movq $6, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1008(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1000(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1016(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4352
.L4351:
.L4352:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4381
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR39(%rip), %rax
    pushq %rax
    movq -992(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1024(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -992(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1032(%rbp)
    movq -1024(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4391
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1040(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1048(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4401
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1056(%rbp)
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1064(%rbp)
    movq -1064(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4411
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4421
    leaq .STR54(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4422
.L4421:
.L4422:
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1072(%rbp)
    movq $0, %rax
    movq %rax, -1080(%rbp)
    movq $4, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -1088(%rbp)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1096(%rbp)
.L4431:    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4432
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4441
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4451
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4452
.L4451:
.L4452:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -1104(%rbp)
    movq -1080(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4461
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4462
.L4461:
.L4462:
    movq -1080(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1072(%rbp), %rax
    addq -328(%rbp), %rax
    movq %rax, -1112(%rbp)
    movq -1104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4442
.L4441:
    movq $0, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4442:
    jmp .L4431
.L4432:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1120(%rbp)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1072(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1120(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4412
.L4411:
    leaq .STR55(%rip), %rax
    pushq %rax
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1128(%rbp)
    movq -1128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4471
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4481
    leaq .STR56(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4482
.L4481:
.L4482:
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1088(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4491:    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4492
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4501
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4511
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4512
.L4511:
.L4512:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1080(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4521
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4522
.L4521:
.L4522:
    movq -1080(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1072(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -1112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4502
.L4501:
    movq $0, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4502:
    jmp .L4491
.L4492:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1136(%rbp)
    movq $21, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1072(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1136(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4472
.L4471:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1144(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4531
    movq $24, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1152(%rbp)
.L4541:    movq -1152(%rbp), %rax
    pushq %rax
    movq -432(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4542
    movq -1152(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1160(%rbp)
    movq -1160(%rbp), %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1056(%rbp), %rax
    pushq %rax
    movq -472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4551
    movq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -432(%rbp), %rax
    pushq %rax
    leaq -1152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4552
.L4551:
.L4552:
    movq -1152(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4541
.L4542:
    jmp .L4532
.L4531:
.L4532:
    movq -1144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4561
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1168(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4571
    leaq .STR57(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4572
.L4571:
.L4572:
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1176(%rbp)
    movq $0, %rax
    movq %rax, -1184(%rbp)
    movq $0, %rax
    movq %rax, -1192(%rbp)
    movq $4, %rax
    movq %rax, -1200(%rbp)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1208(%rbp)
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1216(%rbp)
.L4581:    movq -1216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4582
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4591
    leaq .STR58(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4592
.L4591:
.L4592:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1224(%rbp)
    movq -1224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -1000(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1232(%rbp)
    movq -1192(%rbp), %rax
    pushq %rax
    movq -1200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4601
    movq -1200(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1240(%rbp)
    movq -1240(%rbp), %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1240(%rbp), %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4602
.L4601:
.L4602:
    movq -1192(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1248(%rbp)
    movq -1176(%rbp), %rax
    addq -1248(%rbp), %rax
    movq %rax, -1256(%rbp)
    movq -1184(%rbp), %rax
    addq -1248(%rbp), %rax
    movq %rax, -1264(%rbp)
    movq -1000(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1232(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4611
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4612
.L4611:
    movq $0, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4612:
    jmp .L4581
.L4582:
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1272(%rbp)
    movq $20, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1168(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1176(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1184(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1272(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4562
.L4561:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1280(%rbp)
    movq $97, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -1280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -1280(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1288(%rbp)
    movq -1288(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4562:
.L4472:
.L4412:
    jmp .L4402
.L4401:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1296(%rbp)
    movq $97, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -1296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -1296(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1304(%rbp)
    movq -1304(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4402:
    jmp .L4392
.L4391:
.L4392:
    movq -1032(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4621
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4631
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1056(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR59(%rip), %rax
    pushq %rax
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1312(%rbp)
    movq -1312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4641
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4651
    leaq .STR60(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4652
.L4651:
.L4652:
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4661
    leaq .STR61(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4662
.L4661:
.L4662:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1320(%rbp)
    movq -1320(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -1328(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4671
    leaq .STR62(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4672
.L4671:
.L4672:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1336(%rbp)
    movq -1336(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1344(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4681
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1088(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4691:    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4692
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4701
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4711
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4712
.L4711:
.L4712:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1080(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4721
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4722
.L4721:
.L4722:
    movq -1080(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1072(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -1112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4702
.L4701:
    movq $0, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4702:
    jmp .L4691
.L4692:
    movq -1080(%rbp), %rax
    pushq %rax
    movq -1328(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4731
    leaq .STR63(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -1328(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR64(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -1080(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR65(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4732
.L4731:
.L4732:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1352(%rbp)
    movq $18, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1072(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1328(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1344(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1352(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4682
.L4681:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1360(%rbp)
    movq $19, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1328(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1344(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1360(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4682:
    jmp .L4642
.L4641:
    movq -992(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1368(%rbp)
    movq -1368(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1376(%rbp)
    movq -1376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4642:
    jmp .L4632
.L4631:
    movq -992(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1384(%rbp)
    movq -1384(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1392(%rbp)
    movq -1392(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4632:
    jmp .L4622
.L4621:
.L4622:
    jmp .L4382
.L4381:
.L4382:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -1400(%rbp)
    movq -1400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4741
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1408(%rbp)
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1416(%rbp)
    movq -1416(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4751
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1424(%rbp)
    movq -1424(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4761
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1088(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4771:    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4772
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4781
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4791
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4792
.L4791:
.L4792:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1080(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4801
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4802
.L4801:
.L4802:
    movq -1080(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1072(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -1112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4782
.L4781:
    movq $0, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4782:
    jmp .L4771
.L4772:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1072(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1120(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4762
.L4761:
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -1288(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1288(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4762:
    jmp .L4752
.L4751:
.L4752:
    leaq .STR55(%rip), %rax
    pushq %rax
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1432(%rbp)
    movq -1432(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4811
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1424(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4821
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1088(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4831:    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4832
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4841
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4851
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4852
.L4851:
.L4852:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1080(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4861
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4862
.L4861:
.L4862:
    movq -1080(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1072(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -1112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1080(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4842
.L4841:
    movq $0, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4842:
    jmp .L4831
.L4832:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $21, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1072(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1136(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4822
.L4821:
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -1288(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1288(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4822:
    jmp .L4812
.L4811:
.L4812:
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1440(%rbp)
    movq -1440(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4871
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1424(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4881
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4891
    leaq .STR66(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4892
.L4891:
.L4892:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1448(%rbp)
    movq $0, %rax
    movq %rax, -1456(%rbp)
    movq $0, %rax
    movq %rax, -1464(%rbp)
    movq $4, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1472(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4901
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4902
.L4901:
.L4902:
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1480(%rbp)
    movq -1472(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1448(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1480(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4911:    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4912
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4921
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1488(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4931
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4932
.L4931:
.L4932:
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1496(%rbp)
    movq -1464(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4941
    movq -256(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1448(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -1456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4942
.L4941:
.L4942:
    movq -1464(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1448(%rbp), %rax
    addq -328(%rbp), %rax
    movq %rax, -1504(%rbp)
    movq -1456(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1496(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1464(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4922
.L4921:
    movq $0, %rax
    pushq %rax
    leaq -1096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4922:
    jmp .L4911
.L4912:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1512(%rbp)
    movq $22, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1448(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1456(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1464(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1512(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4882
.L4881:
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -1288(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1288(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4882:
    jmp .L4872
.L4871:
.L4872:
    movq $0, %rax
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4951
    jmp .L4952
.L4951:
.L4952:
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4961
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -432(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4971
    jmp .L4972
.L4971:
.L4972:
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -440(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4981
    jmp .L4982
.L4981:
.L4982:
    movq $0, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1520(%rbp)
.L4991:    movq -1520(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4992
    movq $0, %rax
    movq %rax, -1528(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    movq -432(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5001
    movq $1, %rax
    pushq %rax
    leaq -1528(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5002
.L5001:
.L5002:
    movq -1528(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5011
    movq $0, %rax
    pushq %rax
    leaq -1520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5012
.L5011:
.L5012:
    movq -1528(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5021
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -448(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -440(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1408(%rbp), %rax
    pushq %rax
    movq -472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -480(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5031
    movq $1, %rax
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5032
.L5031:
.L5032:
    movq -448(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5022
.L5021:
.L5022:
    jmp .L4991
.L4992:
    jmp .L4962
.L4961:
.L4962:
    movq $0, %rax
    movq %rax, -1536(%rbp)
    movq $0, %rax
    movq %rax, -1544(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5041
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5051
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1552(%rbp)
.L5061:    movq -1552(%rbp), %rax
    pushq %rax
    movq -432(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5062
    movq -1552(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -440(%rbp), %rax
    addq -1160(%rbp), %rax
    pushq %rax
    leaq -456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TYPEDEFINITION_KIND_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1560(%rbp)
    movq -1560(%rbp), %rax
    pushq %rax
    movq TYPE_KIND_VARIANT(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5071
    movq TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1568(%rbp)
    movq TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1576(%rbp)
    movq $0, %rax
    movq %rax, -1584(%rbp)
.L5081:    movq -1584(%rbp), %rax
    pushq %rax
    movq -1568(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5082
    movq -1584(%rbp), %rax
    pushq %rax
    movq VARIANT_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1592(%rbp)
    movq -1576(%rbp), %rax
    addq -1592(%rbp), %rax
    movq %rax, -1600(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1600(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1608(%rbp)
    movq -1408(%rbp), %rax
    pushq %rax
    movq -1608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5091
    movq $1, %rax
    pushq %rax
    leaq -1536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1616(%rbp)
    movq -1616(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -1544(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -432(%rbp), %rax
    pushq %rax
    leaq -1552(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1568(%rbp), %rax
    pushq %rax
    leaq -1584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5092
.L5091:
.L5092:
    movq -1584(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5081
.L5082:
    jmp .L5072
.L5071:
.L5072:
    movq -1552(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1552(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5061
.L5062:
    jmp .L5052
.L5051:
.L5052:
    jmp .L5042
.L5041:
.L5042:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1624(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1632(%rbp)
    movq -1632(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5101
    movq $0, %rax
    pushq %rax
    movq -1632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1640(%rbp)
    movq -1640(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5111
    movq -416(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5121
    movq $0, %rax
    pushq %rax
    leaq -1640(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5122
.L5121:
.L5122:
    jmp .L5112
.L5111:
.L5112:
    movq -1640(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5131
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1648(%rbp)
    movq -1648(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5141
    leaq .STR67(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5142
.L5141:
.L5142:
    movq $0, %rax
    pushq %rax
    movq -1648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1656(%rbp)
    movq -1656(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -1664(%rbp)
    movq -1664(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5151
    movq -1656(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5161
    leaq .STR67(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5162
.L5161:
.L5162:
    jmp .L5152
.L5151:
.L5152:
    movq $8, %rax
    pushq %rax
    movq -1648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1672(%rbp)
    movq -1656(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $40, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq EXPR_VARIANT_CONSTRUCTOR(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1672(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1680(%rbp)
    movq -1680(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5171
    movq $0, %rax
    pushq %rax
    movq -1680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1688(%rbp)
    movq -1688(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5181
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5191:    movq -1216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5192
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1696(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1704(%rbp)
    movq -1704(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5201
    leaq .STR68(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5202
.L5201:
.L5202:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    movq %rax, -1712(%rbp)
    movq -1192(%rbp), %rax
    pushq %rax
    movq -1200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5211
    movq -1200(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5212
.L5211:
.L5212:
    movq -1192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1712(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1720(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1728(%rbp)
    movq -1728(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5221
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5222
.L5221:
    movq $0, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5222:
    jmp .L5191
.L5192:
    movq -1184(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L5182
.L5181:
.L5182:
    jmp .L5172
.L5171:
.L5172:
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5132
.L5131:
.L5132:
    jmp .L5102
.L5101:
.L5102:
    movq -1536(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5231
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq EXPR_VARIANT_CONSTRUCTOR(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1544(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1680(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1680(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5241
    movq $0, %rax
    pushq %rax
    movq -1680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1688(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1688(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5251
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5261:    movq -1216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5262
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1696(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1704(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5271
    leaq .STR68(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5272
.L5271:
.L5272:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    pushq %rax
    leaq -1712(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1192(%rbp), %rax
    pushq %rax
    movq -1200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5281
    movq -1200(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5282
.L5281:
.L5282:
    movq -1192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1712(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1720(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1728(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5291
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5292
.L5291:
    movq $0, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5292:
    jmp .L5261
.L5262:
    movq -1184(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L5252
.L5251:
.L5252:
    jmp .L5242
.L5241:
.L5242:
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5232
.L5231:
.L5232:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1736(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1736(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1744(%rbp)
    movq -1408(%rbp), %rax
    movq %rax, -1752(%rbp)
    movq $0, %rax
    movq %rax, -1760(%rbp)
    movq $1, %rax
    movq %rax, -1768(%rbp)
    movq -1744(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5301
    movq $0, %rax
    pushq %rax
    leaq -1768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5302
.L5301:
.L5302:
    movq -1768(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5311
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5321
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1776(%rbp)
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1784(%rbp)
    movq $0, %rax
    movq %rax, -1792(%rbp)
.L5331:    movq -1792(%rbp), %rax
    pushq %rax
    movq -1776(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5332
    movq -1784(%rbp), %rax
    pushq %rax
    movq -1792(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1800(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1800(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1808(%rbp)
    movq TYPEDEFINITION_KIND_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -1808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1816(%rbp)
    movq -1816(%rbp), %rax
    pushq %rax
    movq TYPE_KIND_VARIANT(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5341
    movq TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -1808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1824(%rbp)
    movq TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -1808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1832(%rbp)
    movq $0, %rax
    movq %rax, -1840(%rbp)
.L5351:    movq -1840(%rbp), %rax
    pushq %rax
    movq -1824(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5352
    movq -1832(%rbp), %rax
    pushq %rax
    movq -1840(%rbp), %rax
    pushq %rax
    movq VARIANT_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1848(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1848(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1856(%rbp)
    movq -1752(%rbp), %rax
    pushq %rax
    movq -1856(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5361
    movq -1808(%rbp), %rax
    pushq %rax
    leaq -1760(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1824(%rbp), %rax
    pushq %rax
    leaq -1840(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1776(%rbp), %rax
    pushq %rax
    leaq -1792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5362
.L5361:
.L5362:
    movq -1840(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1840(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5351
.L5352:
    jmp .L5342
.L5341:
.L5342:
    movq -1792(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5331
.L5332:
    jmp .L5322
.L5321:
.L5322:
    jmp .L5312
.L5311:
.L5312:
    movq -1760(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5371
    movq $40, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq EXPR_VARIANT_CONSTRUCTOR(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq -1760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1864(%rbp)
    movq -1864(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1752(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5372
.L5371:
.L5372:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1872(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1872(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1880(%rbp)
    movq -1880(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5381
    movq -1408(%rbp), %rax
    movq %rax, -1888(%rbp)
    movq $0, %rax
    movq %rax, -1896(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5391
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1904(%rbp)
.L5401:    movq -1904(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5402
    movq $0, %rax
    movq %rax, -1912(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    movq -432(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5411
    movq $1, %rax
    pushq %rax
    leaq -1912(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5412
.L5411:
.L5412:
    movq -1912(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5421
    movq $0, %rax
    pushq %rax
    leaq -1904(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5422
.L5421:
.L5422:
    movq -1912(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5431
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -448(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -440(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1560(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1920(%rbp)
    movq -1560(%rbp), %rax
    pushq %rax
    movq TYPE_KIND_VARIANT(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5441
    movq $1, %rax
    pushq %rax
    leaq -1920(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5442
.L5441:
.L5442:
    movq -1920(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5451
    movq $24, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1568(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1576(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1928(%rbp)
    movq $1, %rax
    movq %rax, -1936(%rbp)
.L5461:    movq -1936(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5462
    movq $0, %rax
    movq %rax, -1944(%rbp)
    movq -1928(%rbp), %rax
    pushq %rax
    movq -1568(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5471
    movq $1, %rax
    pushq %rax
    leaq -1944(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5472
.L5471:
.L5472:
    movq -1944(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5481
    movq $0, %rax
    pushq %rax
    leaq -1936(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5482
.L5481:
.L5482:
    movq -1944(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5491
    movq -1928(%rbp), %rax
    pushq %rax
    movq VARIANT_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1592(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1576(%rbp), %rax
    addq -1592(%rbp), %rax
    pushq %rax
    leaq -1600(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1600(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1952(%rbp)
    movq -1888(%rbp), %rax
    pushq %rax
    movq -1952(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1960(%rbp)
    movq -1960(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5501
    movq -464(%rbp), %rax
    pushq %rax
    leaq -1896(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1936(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1904(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5502
.L5501:
.L5502:
    movq -1928(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1928(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5492
.L5491:
.L5492:
    jmp .L5461
.L5462:
    jmp .L5452
.L5451:
.L5452:
    movq -448(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5432
.L5431:
.L5432:
    jmp .L5401
.L5402:
    jmp .L5392
.L5391:
.L5392:
    movq -1896(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5511
    movq $40, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq EXPR_VARIANT_CONSTRUCTOR(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq -1896(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -1864(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1864(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1888(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1968(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1968(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1976(%rbp)
    movq -1976(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5521
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5531:    movq -1216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5532
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1696(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1704(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5541
    leaq .STR68(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5542
.L5541:
.L5542:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    pushq %rax
    leaq -1712(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1192(%rbp), %rax
    pushq %rax
    movq -1200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5551
    movq -1200(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5552
.L5551:
.L5552:
    movq -1192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1712(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1720(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1728(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5561
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5562
.L5561:
    movq $0, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5562:
    jmp .L5531
.L5532:
    movq -1184(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1192(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L5522
.L5521:
.L5522:
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5512
.L5511:
.L5512:
    jmp .L5382
.L5381:
.L5382:
    movq $0, %rax
    movq %rax, -1984(%rbp)
    movq -1984(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5571
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1992(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -2000(%rbp)
    movq $1, %rax
    movq %rax, -2008(%rbp)
.L5581:    movq -2008(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5582
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2016(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2024(%rbp)
    movq -2024(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5591
    movq $0, %rax
    pushq %rax
    leaq -2008(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5592
.L5591:
.L5592:
    movq -2024(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5601
    movq $0, %rax
    pushq %rax
    leaq -2008(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5602
.L5601:
.L5602:
    movq $0, %rax
    movq %rax, -2032(%rbp)
    movq -2024(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5611
    movq -2024(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5621
    movq $1, %rax
    pushq %rax
    leaq -2032(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5622
.L5621:
.L5622:
    jmp .L5612
.L5611:
.L5612:
    movq -2032(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5631
    movq -232(%rbp), %rax
    pushq %rax
    movq -2000(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5641
    movq -2000(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5651
    movq $4, %rax
    pushq %rax
    leaq -2000(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5652
.L5651:
    movq -2000(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -2000(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5652:
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -2000(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5642
.L5641:
.L5642:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -232(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -224(%rbp), %rax
    addq -328(%rbp), %rax
    pushq %rax
    leaq -336(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -232(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2040(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2048(%rbp)
    movq -2048(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5661
    movq $0, %rax
    pushq %rax
    leaq -2008(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5662
.L5661:
    movq -2048(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5671
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2056(%rbp)
    jmp .L5672
.L5671:
    leaq .STR69(%rip), %rax
    movq %rax, -2064(%rbp)
    movq -2064(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -2040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L5672:
.L5662:
    jmp .L5632
.L5631:
.L5632:
    jmp .L5581
.L5582:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2072(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5572
.L5571:
.L5572:
    movq -416(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5681
    movq $32, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq EXPR_TYPE_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5682
.L5681:
.L5682:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2080(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -2080(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2088(%rbp)
    movq -2088(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5691
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2096(%rbp)
    movq $8, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2104(%rbp)
    movq $12, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2112(%rbp)
    movq $16, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2120(%rbp)
    movq $20, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -2128(%rbp)
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -2136(%rbp)
    movq $0, %rax
    movq %rax, -2144(%rbp)
    movq -2136(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5701
    movq $0, %rax
    pushq %rax
    movq -2136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2152(%rbp)
    movq -2152(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5711
    movq $8, %rax
    pushq %rax
    movq -2136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2160(%rbp)
    movq -2160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5721
    movq $0, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -2168(%rbp)
    movq -2168(%rbp), %rax
    pushq %rax
    movq $65, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5731
    movq -2168(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5741
    movq $1, %rax
    pushq %rax
    leaq -2144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5742
.L5741:
.L5742:
    jmp .L5732
.L5731:
.L5732:
    jmp .L5722
.L5721:
.L5722:
    jmp .L5712
.L5711:
.L5712:
    movq -2136(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L5702
.L5701:
.L5702:
    movq -2104(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -2112(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -2120(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -2128(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -2096(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -2144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5751
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2176(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -2176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2184(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -2176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2192(%rbp)
    movq -2184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5752
.L5751:
.L5752:
    jmp .L5692
.L5691:
.L5692:
    movq -1408(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4742
.L4741:
.L4742:
    movq -24(%rbp), %rax
    pushq %rax
    movq $134, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5761
    movq $134, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2200(%rbp)
    movq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5762
.L5761:
.L5762:
    movq -24(%rbp), %rax
    pushq %rax
    movq $135, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5771
    movq $135, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    pushq %rax
    leaq -1992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5772
.L5771:
.L5772:
    movq -24(%rbp), %rax
    pushq %rax
    movq $133, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5781
    movq $133, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    pushq %rax
    leaq -2056(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2216(%rbp)
    movq -2216(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5791
    leaq .STR70(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -2208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5792
.L5791:
.L5792:
    movq $8, %rax
    pushq %rax
    movq -2208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    subq -392(%rbp), %rax
    movq %rax, -2224(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2232(%rbp)
    movq -2224(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5782
.L5781:
.L5782:
    movq -24(%rbp), %rax
    pushq %rax
    movq $162, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5801
    movq $162, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -2240(%rbp)
    movq $0, %rax
    movq %rax, -2248(%rbp)
    movq $4, %rax
    movq %rax, -2256(%rbp)
    movq -2256(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -2264(%rbp)
    movq -2264(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -2240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2272(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2280(%rbp)
    movq -2280(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5811
    leaq .STR71(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5812
.L5811:
.L5812:
    movq $8, %rax
    pushq %rax
    movq -2272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2288(%rbp)
    movq -2288(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -2296(%rbp)
    movq -2296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -2240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -2248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -2304(%rbp)
.L5821:    movq -2304(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5822
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2312(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1424(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5831
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2320(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2328(%rbp)
    movq -2328(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5841
    leaq .STR72(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5842
.L5841:
.L5842:
    movq $8, %rax
    pushq %rax
    movq -2320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2336(%rbp)
    movq -2336(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -2344(%rbp)
    movq -2248(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -2352(%rbp)
    movq -2344(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -2240(%rbp), %rax
    addq -2352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -2248(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -2248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5832
.L5831:
    movq $0, %rax
    pushq %rax
    leaq -2304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5832:
    jmp .L5821
.L5822:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2360(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2368(%rbp)
    movq -2368(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5851
    leaq .STR73(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5852
.L5851:
.L5852:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -2376(%rbp)
    movq -2376(%rbp), %rax
    pushq %rax
    movq -2248(%rbp), %rax
    pushq %rax
    movq -2240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_lambda_multi
    movq %rax, -2384(%rbp)
    movq -2248(%rbp), %rax
    pushq %rax
    movq -2240(%rbp), %rax
    pushq %rax
    movq -2376(%rbp), %rax
    pushq %rax
    movq -2384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq -2384(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5802
.L5801:
.L5802:
    leaq .STR74(%rip), %rax
    pushq %rax
    leaq -2064(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -2064(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_return_statement
parser_parse_return_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $7, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5861
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5862
.L5861:
.L5862:
    movq -32(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5871
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5872
.L5871:
.L5872:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5881
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5882
.L5881:
.L5882:
    movq -32(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5891
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5892
.L5891:
.L5892:
    movq -32(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5901
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5902
.L5901:
.L5902:
    movq -32(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5911
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5912
.L5911:
.L5912:
    movq -32(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5921
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5922
.L5921:
.L5922:
    movq -32(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5931
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5932
.L5931:
.L5932:
    movq -32(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5941
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5942
.L5941:
.L5942:
    movq -32(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5951
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5952
.L5951:
.L5952:
    movq -32(%rbp), %rax
    pushq %rax
    movq $113, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5961
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5962
.L5961:
.L5962:
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5971
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5972
.L5971:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5972:
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_return
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_break_statement
parser_parse_break_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call statement_create_break
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_continue_statement
parser_parse_continue_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $45, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call statement_create_continue
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_print_statement
parser_parse_print_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5981
    movq $172, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5982
.L5981:
    movq $47, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5982:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5991
    leaq .STR75(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5992
.L5991:
.L5992:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -64(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6001
    movq -64(%rbp), %rax
    movq %rax, -88(%rbp)
.L6011:    movq -80(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6012
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -96(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -104(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -112(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -104(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6011
.L6012:
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_print
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6002
.L6001:
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_print
    movq %rbp, %rsp
    popq %rbp
    ret
.L6002:
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_statement_block
parser_parse_statement_block:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $1, %rax
    movq %rax, -40(%rbp)
.L6021:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6022
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6031
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6032
.L6031:
.L6032:
    movq -56(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6041
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6042
.L6041:
.L6042:
    movq -56(%rbp), %rax
    pushq %rax
    movq $113, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6051
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6052
.L6051:
.L6052:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6061
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6062
.L6061:
.L6062:
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6071
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6081
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6082
.L6081:
.L6082:
    movq -56(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6091
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6092
.L6091:
.L6092:
    movq -56(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6101
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6102
.L6101:
.L6102:
    movq -56(%rbp), %rax
    pushq %rax
    movq $44, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6111
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_break_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6112
.L6111:
.L6112:
    movq -56(%rbp), %rax
    pushq %rax
    movq $45, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6121
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_continue_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6122
.L6121:
.L6122:
    movq -56(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6131
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6132
.L6131:
.L6132:
    movq -56(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6141
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6142
.L6141:
.L6142:
    movq -56(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6151
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6152
.L6151:
.L6152:
    movq -56(%rbp), %rax
    pushq %rax
    movq $180, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6161
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_loop_forever
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6162
.L6161:
.L6162:
    movq -56(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6171
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6172
.L6171:
.L6172:
    movq -56(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6181
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6182
.L6181:
.L6182:
    movq -56(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6191
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_for_range_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6192
.L6191:
.L6192:
    movq -56(%rbp), %rax
    pushq %rax
    movq $139, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6201
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6202
.L6201:
.L6202:
    movq -56(%rbp), %rax
    pushq %rax
    movq $140, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6211
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6212
.L6211:
.L6212:
    movq -56(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6221
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6222
.L6221:
.L6222:
    movq -56(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6231
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6232
.L6231:
.L6232:
    movq -56(%rbp), %rax
    pushq %rax
    movq $167, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6241
    movq $167, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -72(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -80(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -88(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -96(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -88(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    leaq .STR76(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6242
.L6241:
.L6242:
    movq -56(%rbp), %rax
    pushq %rax
    movq $169, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6251
    movq $169, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -112(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -120(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -128(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -136(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -120(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -128(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    leaq .STR77(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6252
.L6251:
.L6252:
    movq -56(%rbp), %rax
    pushq %rax
    movq $171, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6261
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6262
.L6261:
.L6262:
    movq -56(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6272
.L6271:
.L6272:
    movq -56(%rbp), %rax
    pushq %rax
    movq $183, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6281
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_call_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6282
.L6281:
.L6282:
    movq -56(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6291
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $0, %rax
    movq %rax, -168(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6301
    leaq .STR78(%rip), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6302
.L6301:
.L6302:
    movq -168(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6311
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -176(%rbp)
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -192(%rbp)
    movq $8, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    movq %rax, -208(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6321
    leaq .STR79(%rip), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6331
    movq $1, %rax
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6332
.L6331:
.L6332:
    jmp .L6322
.L6321:
.L6322:
    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6341
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L6342
.L6341:
.L6342:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -216(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -224(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -176(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    leaq .STR80(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6312
.L6311:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -240(%rbp)
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6351
    movq -248(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6361
    leaq .STR81(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR82(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    jmp .L6362
.L6361:
.L6362:
    jmp .L6352
.L6351:
.L6352:
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6312:
    jmp .L6292
.L6291:
.L6292:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6371
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6372
.L6371:
.L6372:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6381
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6382
.L6381:
.L6382:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6391
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6401
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6411
    movq $256, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6412
.L6411:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6412:
    movq $8, %rax
    movq %rax, -280(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6402
.L6401:
.L6402:
    movq $8, %rax
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -296(%rbp)
    movq -24(%rbp), %rax
    addq -296(%rbp), %rax
    movq %rax, -304(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    addq $1, %rax
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L6392
.L6391:
.L6392:
    jmp .L6072
.L6071:
.L6072:
    jmp .L6021
.L6022:
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_while_statement
parser_parse_while_statement:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -24(%rbp)
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -32(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -64(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call statement_create_while
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_loop_forever
parser_parse_loop_forever:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $180, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -72(%rbp)
    movq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $22, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_comparison
    movq %rax, -88(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call statement_create_while
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_for_range_statement
parser_parse_for_range_statement:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $143, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $145, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6421
    movq $145, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6431
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -80(%rbp)
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -88(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $38, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6441
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6442
.L6441:
.L6442:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -128(%rbp)
    movq $0, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -136(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $143, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -136(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    popq %r8
    popq %r9
    call statement_create_for_range
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6432
.L6431:
.L6432:
    movq $152, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -144(%rbp)
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -160(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -168(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $143, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -168(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call statement_create_for_each
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6422
.L6421:
.L6422:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -184(%rbp)
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -192(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq $0, %rax
    movq %rax, -216(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $38, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6451
    movq $38, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6452
.L6451:
    movq -208(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6461
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6471
    leaq .STR83(%rip), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6481
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6482
.L6481:
.L6482:
    jmp .L6472
.L6471:
.L6472:
    jmp .L6462
.L6461:
.L6462:
.L6452:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -152(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $143, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -168(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    popq %r8
    popq %r9
    call statement_create_for_range
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_if_statement
parser_parse_if_statement:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $18, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -24(%rbp)
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -32(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $1, %rax
    movq %rax, -80(%rbp)
.L6491:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6492
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6501
    movq $19, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6511
    movq $18, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -128(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -136(%rbp)
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -144(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -160(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -168(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    popq %r8
    call statement_create_if
    movq %rax, -176(%rbp)
    movq -72(%rbp), %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6521
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6522
.L6521:
.L6522:
    movq -184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6531
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq $32, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
.L6541:    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6542
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $32, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6541
.L6542:
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -208(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -208(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L6532
.L6531:
.L6532:
    jmp .L6512
.L6511:
.L6512:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6551
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -216(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -232(%rbp)
    movq $0, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -240(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6561
    movq -232(%rbp), %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -240(%rbp), %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6562
.L6561:
.L6562:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6571
    movq -64(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6581
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $32, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6591:    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6592
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $32, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6591
.L6592:
    movq -232(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -240(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L6582
.L6581:
.L6582:
    jmp .L6572
.L6571:
.L6572:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6552
.L6551:
.L6552:
    jmp .L6502
.L6501:
.L6502:
    movq -96(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6601
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6602
.L6601:
.L6602:
    jmp .L6491
.L6492:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -248(%rbp)
    movq $18, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -256(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    popq %r8
    call statement_create_if
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_match_statement
parser_parse_match_statement:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $112, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -16(%rbp)
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $4, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq $1, %rax
    movq %rax, -48(%rbp)
.L6611:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6612
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6621
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6622
.L6621:
.L6622:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6631
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $113, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6641
    movq $113, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq PATTERN_LITERAL(%rip), %rax  # Load global variable
    movq %rax, -88(%rbp)
    movq $0, %rax
    movq %rax, -96(%rbp)
    movq $0, %rax
    movq %rax, -104(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $161, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6651
    movq PATTERN_WILDCARD(%rip), %rax  # Load global variable
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $161, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L6652
.L6651:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6661
    movq $8, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -128(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -136(%rbp)
    movq $0, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6671
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6681
    leaq .STR84(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6682
.L6681:
.L6682:
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -168(%rbp)
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6691
    movq -176(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6701
    leaq .STR85(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6702
.L6701:
.L6702:
    jmp .L6692
.L6691:
.L6692:
    movq $8, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -192(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PATTERN_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -192(%rbp), %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6672
.L6671:
    movq -128(%rbp), %rax
    movq %rax, -200(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6711
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $0, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6721
    movq -232(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L6722
.L6721:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L6722:
    jmp .L6712
.L6711:
.L6712:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6731
    movq PATTERN_VARIANT(%rip), %rax  # Load global variable
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6732
.L6731:
    movq -256(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6741
    movq PATTERN_VARIANT(%rip), %rax  # Load global variable
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $4, %rax
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -272(%rbp)
.L6751:    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6752
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6761
    leaq .STR86(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6762
.L6761:
.L6762:
    movq $8, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -304(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -312(%rbp)
    movq $0, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6771
    leaq .STR87(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6772
.L6771:
.L6772:
    movq $8, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -336(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -112(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6781
    movq -264(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6782
.L6781:
.L6782:
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -344(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -112(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -352(%rbp)
    movq $0, %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6791
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L6792
.L6791:
    movq $0, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6792:
    jmp .L6751
.L6752:
    jmp .L6742
.L6741:
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6742:
.L6732:
.L6672:
    jmp .L6662
.L6661:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6662:
.L6652:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -376(%rbp)
    movq $0, %rax
    pushq %rax
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -384(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6801
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6802
.L6801:
.L6802:
    movq -40(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -392(%rbp)
    movq -32(%rbp), %rax
    addq -392(%rbp), %rax
    movq %rax, -400(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq WHEN_PATTERN_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq WHEN_PATTERN_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -104(%rbp), %rax
    pushq %rax
    movq WHEN_FIELD_BINDINGS(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq WHEN_FIELD_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -376(%rbp), %rax
    pushq %rax
    movq WHEN_BODY_STMTS(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -384(%rbp), %rax
    pushq %rax
    movq WHEN_BODY_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6642
.L6641:
    movq -64(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6811
    movq $19, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -416(%rbp)
    movq $0, %rax
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -424(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6821
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6822
.L6821:
.L6822:
    movq -40(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -432(%rbp)
    movq -32(%rbp), %rax
    addq -432(%rbp), %rax
    movq %rax, -440(%rbp)
    movq PATTERN_WILDCARD(%rip), %rax  # Load global variable
    pushq %rax
    movq WHEN_PATTERN_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq WHEN_PATTERN_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq WHEN_FIELD_BINDINGS(%rip), %rax  # Load global variable
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq WHEN_FIELD_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -416(%rbp), %rax
    pushq %rax
    movq WHEN_BODY_STMTS(%rip), %rax  # Load global variable
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -424(%rbp), %rax
    pushq %rax
    movq WHEN_BODY_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6812
.L6811:
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6831
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $112, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6832
.L6831:
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6832:
.L6812:
.L6642:
    jmp .L6632
.L6631:
.L6632:
    jmp .L6611
.L6612:
    movq $0, %rax
    movq %rax, -448(%rbp)
    movq $0, %rax
    movq %rax, -456(%rbp)
.L6841:    movq -456(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6842
    movq -456(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    addq -392(%rbp), %rax
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq WHEN_PATTERN_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -464(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6851
    movq $1, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6852
.L6851:
.L6852:
    movq -456(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6841
.L6842:
    movq -448(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6861
    movq $8, %rax
    movq %rax, -472(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -480(%rbp)
    movq $0, %rax
    movq %rax, -488(%rbp)
    movq $0, %rax
    movq %rax, -496(%rbp)
.L6871:    movq -496(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6872
    movq -496(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    addq -392(%rbp), %rax
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq WHEN_PATTERN_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -464(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6881
    movq WHEN_PATTERN_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq -472(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6891
    movq -472(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -472(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -480(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6892
.L6891:
.L6892:
    movq -504(%rbp), %rax
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -488(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6882
.L6881:
.L6882:
    movq -496(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6871
.L6872:
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6901
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -512(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6911
    movq $0, %rax
    pushq %rax
    leaq -488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6912
.L6911:
.L6912:
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6921
    movq $24, %rax
    pushq %rax
    movq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -520(%rbp)
    movq $16, %rax
    pushq %rax
    movq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -528(%rbp)
    movq $0, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -536(%rbp)
    movq $0, %rax
    movq %rax, -544(%rbp)
    movq $0, %rax
    movq %rax, -552(%rbp)
    movq $0, %rax
    movq %rax, -560(%rbp)
.L6931:    movq -560(%rbp), %rax
    pushq %rax
    movq -520(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6932
    movq -560(%rbp), %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer_at_index
    movq %rax, -568(%rbp)
    movq $8, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -576(%rbp)
    movq -576(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6941
    movq $24, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -584(%rbp)
    movq $16, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -592(%rbp)
    movq $0, %rax
    movq %rax, -600(%rbp)
.L6951:    movq -600(%rbp), %rax
    pushq %rax
    movq -584(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6952
    movq -600(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -608(%rbp)
    movq -592(%rbp), %rax
    addq -608(%rbp), %rax
    movq %rax, -616(%rbp)
    movq $0, %rax
    pushq %rax
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -624(%rbp)
    movq -536(%rbp), %rax
    pushq %rax
    movq -624(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6961
    movq -568(%rbp), %rax
    pushq %rax
    leaq -544(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -584(%rbp), %rax
    pushq %rax
    leaq -552(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -520(%rbp), %rax
    pushq %rax
    leaq -560(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -584(%rbp), %rax
    pushq %rax
    leaq -600(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6962
.L6961:
.L6962:
    movq -600(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -600(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6951
.L6952:
    jmp .L6942
.L6941:
.L6942:
    movq -560(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -560(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6931
.L6932:
    movq -544(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6971
    movq $16, %rax
    pushq %rax
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -592(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -632(%rbp)
    movq $0, %rax
    movq %rax, -640(%rbp)
    movq $0, %rax
    movq %rax, -648(%rbp)
.L6981:    movq -648(%rbp), %rax
    pushq %rax
    movq -552(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6982
    movq -648(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -592(%rbp), %rax
    addq -608(%rbp), %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -656(%rbp)
    movq $0, %rax
    movq %rax, -664(%rbp)
.L6991:    movq -664(%rbp), %rax
    pushq %rax
    movq -488(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6992
    movq -664(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7001
    movq $1, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -488(%rbp), %rax
    pushq %rax
    leaq -664(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7002
.L7001:
.L7002:
    movq -664(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -664(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6991
.L6992:
    movq -656(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7011
    movq -640(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7021
    leaq .STR88(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR89(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    leaq -640(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7022
.L7021:
.L7022:
    leaq .STR90(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    jmp .L7012
.L7011:
.L7012:
    movq -648(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -648(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6981
.L6982:
    jmp .L6972
.L6971:
.L6972:
    jmp .L6922
.L6921:
.L6922:
    jmp .L6902
.L6901:
.L6902:
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L6862
.L6861:
.L6862:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -680(%rbp)
    movq STMT_MATCH(%rip), %rax  # Load global variable
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_MATCH_EXPR(%rip), %rax  # Load global variable
    pushq %rax
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq STMT_MATCH_WHEN_CLAUSES(%rip), %rax  # Load global variable
    pushq %rax
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq STMT_MATCH_WHEN_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -680(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_inline_assembly_statement
parser_parse_inline_assembly_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $121, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -16(%rbp)
    movq $122, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $20, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    movq $32, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -56(%rbp)
    movq $16, %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_read_raw_assembly_until_end
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -88(%rbp)
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_read_raw_assembly_until_end
parser_read_raw_assembly_until_end:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $8192, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq $1, %rax
    movq %rax, -48(%rbp)
.L7031:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7032
    movq $20, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7041
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7042
.L7041:
    movq $69, %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7051
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_try_match_end_assembly
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7061
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7062
.L7061:
    movq -56(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -80(%rbp)
.L7062:
    jmp .L7052
.L7051:
    movq -56(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7052:
.L7042:
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    subq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7071
    leaq .STR91(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L7072
.L7071:
.L7072:
    jmp .L7031
.L7032:
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -88(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -88(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_try_match_end_assembly
parser_try_match_end_assembly:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    leaq .STR92(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call lexer_try_match_word
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7081
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7082
.L7081:
.L7082:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_whitespace
    movq %rax, -40(%rbp)
    leaq .STR93(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call lexer_try_match_word
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7091
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7092
.L7091:
.L7092:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_try_match_word
lexer_try_match_word:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
.L7101:    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7102
    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -40(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7111
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7112
.L7111:
.L7112:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7101
.L7102:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl calculate_type_size
calculate_type_size:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    leaq .STR28(%rip), %rax
    movq %rax, -24(%rbp)
    leaq .STR94(%rip), %rax
    movq %rax, -32(%rbp)
    leaq .STR95(%rip), %rax
    movq %rax, -40(%rbp)
    leaq .STR96(%rip), %rax
    movq %rax, -48(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7121
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7122
.L7121:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7131
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7132
.L7131:
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7141
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7142
.L7141:
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7151
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7152
.L7151:
.L7152:
.L7142:
.L7132:
.L7122:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7161
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $1, %rax
    movq %rax, -80(%rbp)
.L7171:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7172
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7181
    movq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7182
.L7181:
.L7182:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7191
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7192
.L7191:
.L7192:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7201
    movq $8, %rax
    movq %rax, -96(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -64(%rbp), %rax
    addq -104(%rbp), %rax
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7211
    movq $40, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7212
.L7211:
.L7212:
    movq -72(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7202
.L7201:
.L7202:
    jmp .L7171
.L7172:
    jmp .L7162
.L7161:
.L7162:
    leaq .STR97(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR98(%rip), %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_type_definition
parser_parse_type_definition:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq TypeDefinition_SIZE(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7221
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7231
    leaq .STR99(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7232
.L7231:
.L7232:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_NAME_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq TYPE_KIND_STRUCT(%rip), %rax  # Load global variable
    pushq %rax
    movq TYPEDEFINITION_KIND_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7241:    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7242
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7251
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7252
.L7251:
.L7252:
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7261
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7262
.L7261:
.L7262:
    movq -32(%rbp), %rax
    pushq %rax
    movq $151, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7271
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7272
.L7271:
.L7272:
    movq -32(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7281
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7282
.L7281:
.L7282:
    movq -32(%rbp), %rax
    pushq %rax
    movq $132, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7291
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7292
.L7291:
.L7292:
    movq -32(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7301
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7302
.L7301:
.L7302:
    movq -32(%rbp), %rax
    pushq %rax
    movq $155, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7311
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7312
.L7311:
.L7312:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7321
    leaq .STR58(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR100(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR19(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7322
.L7321:
.L7322:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -88(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -96(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7331
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7332
.L7331:
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7332:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7341
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -104(%rbp)
.L7351:    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7352
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7361
    movq -104(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7362
.L7361:
.L7362:
    movq -32(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7371
    movq -104(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7372
.L7371:
.L7372:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7351
.L7352:
    jmp .L7342
.L7341:
.L7342:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7381
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7382
.L7381:
.L7382:
    movq TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    addq $1, %rax
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -136(%rbp)
    movq $0, %rax
    movq %rax, -144(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7391
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7392
.L7391:
    movq -136(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7392:
    movq -144(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -120(%rbp), %rax
    subq $1, %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -160(%rbp)
    movq -144(%rbp), %rax
    addq -160(%rbp), %rax
    movq %rax, -168(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_NAME_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_OFFSET_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -64(%rbp), %rax
    addq -184(%rbp), %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7241
.L7242:
    movq -64(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7222
.L7221:
.L7222:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7401
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_NAME_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $21, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $126, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7411
    movq $126, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7421
    leaq .STR101(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7422
.L7421:
.L7422:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -192(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $128, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -200(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7431
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7432
.L7431:
.L7432:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7441
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7442
.L7441:
.L7442:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7451
    leaq .STR32(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7452
.L7451:
.L7452:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7461
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7462
.L7461:
.L7462:
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7471
    leaq .STR102(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7472
.L7471:
.L7472:
    movq TYPE_KIND_ARRAY(%rip), %rax  # Load global variable
    pushq %rax
    movq TYPEDEFINITION_KIND_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -200(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_ARRAY_ELEMENT_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -192(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_ARRAY_LENGTH_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_ARRAY_ELEMENT_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7412
.L7411:
    movq -32(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7481
    movq $124, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq TYPE_KIND_FUNCTION(%rip), %rax  # Load global variable
    pushq %rax
    movq TYPEDEFINITION_KIND_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $8, %rax
    pushq %rax
    movq TYPEDEFINITION_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7491
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7492
.L7491:
.L7492:
    movq -32(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7501
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7502
.L7501:
.L7502:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7511
    movq $2, %rax
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -232(%rbp)
.L7521:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7522
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7531
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7532
.L7531:
.L7532:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -240(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -216(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7541
    movq -216(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -216(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -256(%rbp), %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7542
.L7541:
.L7542:
    movq -248(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -264(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -224(%rbp), %rax
    addq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -248(%rbp), %rax
    addq $1, %rax
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7551
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7552
.L7551:
.L7552:
    movq -32(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7561
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7562
.L7561:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7562:
    jmp .L7521
.L7522:
    jmp .L7512
.L7511:
.L7512:
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7571
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7572
.L7571:
.L7572:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7581
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -280(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7582
.L7581:
.L7582:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7591
    leaq .STR32(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -280(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7592
.L7591:
.L7592:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7601
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -280(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7602
.L7601:
    leaq .STR103(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L7602:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7482
.L7481:
    movq TYPE_KIND_VARIANT(%rip), %rax  # Load global variable
    pushq %rax
    movq TYPEDEFINITION_KIND_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7611:    movq -32(%rbp), %rax
    pushq %rax
    movq $111, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7612
    movq $111, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7621
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7631
    leaq .STR104(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7632
.L7631:
.L7632:
    jmp .L7622
.L7621:
.L7622:
    movq TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    addq $1, %rax
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -312(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq VARIANT_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -304(%rbp), %rax
    subq $1, %rax
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq VARIANT_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -344(%rbp)
    movq -328(%rbp), %rax
    addq -344(%rbp), %rax
    movq %rax, -352(%rbp)
    movq -304(%rbp), %rax
    subq $1, %rax
    movq %rax, -360(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq VARIANT_NAME_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq VARIANT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq VARIANT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -360(%rbp), %rax
    pushq %rax
    movq VARIANT_TAG_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7641
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7651:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7652
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7661
    leaq .STR105(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7662
.L7661:
.L7662:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7671
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7681
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7691
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7701
    leaq .STR106(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7702
.L7701:
.L7702:
    jmp .L7692
.L7691:
.L7692:
    jmp .L7682
.L7681:
.L7682:
    jmp .L7672
.L7671:
.L7672:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq VARIANT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -376(%rbp)
    movq -376(%rbp), %rax
    addq $1, %rax
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq VARIANT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq VARIANT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq VARIANT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -384(%rbp), %rax
    subq $1, %rax
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -424(%rbp)
    movq -408(%rbp), %rax
    addq -424(%rbp), %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -88(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_NAME_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_OFFSET_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -184(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -160(%rbp), %rax
    addq -184(%rbp), %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7711
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7712
.L7711:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7712:
    jmp .L7651
.L7652:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7642
.L7641:
.L7642:
    movq -32(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7721
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7731:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7732
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7741
    leaq .STR105(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7742
.L7741:
.L7742:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7751
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7761
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7771
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7781
    leaq .STR106(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7782
.L7781:
.L7782:
    jmp .L7772
.L7771:
.L7772:
    jmp .L7762
.L7761:
.L7762:
    jmp .L7752
.L7751:
.L7752:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7791
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7792
.L7791:
.L7792:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7801
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7802
.L7801:
.L7802:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7811
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7812
.L7811:
.L7812:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7821
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7822
.L7821:
.L7822:
    movq VARIANT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -384(%rbp), %rax
    pushq %rax
    movq VARIANT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq VARIANT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -384(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -400(%rbp), %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    movq VARIANT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -384(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    addq -424(%rbp), %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -88(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_NAME_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_OFFSET_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -184(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -160(%rbp), %rax
    addq -184(%rbp), %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7831
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7832
.L7831:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7832:
    jmp .L7731
.L7732:
    jmp .L7722
.L7721:
.L7722:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7611
.L7612:
    movq $8, %rax
    pushq %rax
    movq TYPEDEFINITION_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -432(%rbp)
.L7841:    movq -432(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7842
    movq -432(%rbp), %rax
    pushq %rax
    movq VARIANT_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -344(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    addq -344(%rbp), %rax
    pushq %rax
    leaq -352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    movq %rax, -440(%rbp)
    movq VARIANT_FIELD_COUNT_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq VARIANT_FIELDS_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -448(%rbp)
.L7851:    movq -448(%rbp), %rax
    pushq %rax
    movq -376(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7852
    movq -448(%rbp), %rax
    pushq %rax
    movq TYPEFIELD_SIZE(%rip), %rax  # Load global variable
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -392(%rbp), %rax
    addq -160(%rbp), %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TYPEFIELD_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -440(%rbp), %rax
    addq -184(%rbp), %rax
    pushq %rax
    leaq -440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -448(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -448(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7851
.L7852:
    movq TYPEDEFINITION_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -456(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq -456(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7861
    movq -440(%rbp), %rax
    pushq %rax
    movq TYPEDEFINITION_SIZE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L7862
.L7861:
.L7862:
    movq -432(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7841
.L7842:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L7482:
.L7412:
    jmp .L7402
.L7401:
    leaq .STR107(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L7402:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_function
parser_parse_function:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7871
    leaq .STR108(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $10, %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR109(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR22(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7872
.L7871:
.L7872:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7881
    leaq .STR110(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7882
.L7881:
.L7882:
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -48(%rbp)
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_create
    movq %rax, -64(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7891
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7892
.L7891:
.L7892:
    movq -24(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7901
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7911
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7912
.L7911:
.L7912:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7921
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7922
.L7921:
.L7922:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7931
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7941
    leaq .STR111(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L7942
.L7941:
.L7942:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -96(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -104(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7951
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7952
.L7951:
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7952:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7961
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -112(%rbp)
.L7971:    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7972
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7981
    movq -112(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7982
.L7981:
.L7982:
    movq -24(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7991
    movq -112(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7992
.L7991:
.L7992:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7971
.L7972:
    jmp .L7962
.L7961:
.L7962:
    movq -104(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call function_add_parameter
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -128(%rbp)
    movq $0, %rax
    movq %rax, -136(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8001
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8002
.L8001:
.L8002:
    movq -128(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8011
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8012
.L8011:
.L8012:
.L8021:    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8022
    movq -128(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8031
    leaq .STR112(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L8032
.L8031:
.L8032:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -152(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8041
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8042
.L8041:
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8042:
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8051
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -224(%rbp)
.L8061:    movq -224(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8062
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -216(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8071
    movq -224(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8072
.L8071:
.L8072:
    movq -216(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8081
    movq -224(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8082
.L8081:
.L8082:
    movq -216(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8061
.L8062:
    jmp .L8052
.L8051:
.L8052:
    movq -104(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call function_add_parameter
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -128(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8091
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8092
.L8091:
.L8092:
    movq -128(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8101
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8102
.L8101:
.L8102:
    jmp .L8021
.L8022:
    jmp .L7932
.L7931:
.L7932:
    jmp .L7902
.L7901:
.L7902:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -232(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8111
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8112
.L8111:
.L8112:
    leaq .STR113(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -240(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8121
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8131
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8132
.L8131:
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8132:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8122
.L8121:
.L8122:
    movq -240(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8141
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -248(%rbp)
.L8151:    movq -248(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8152
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8161
    movq -248(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8162
.L8161:
.L8162:
    movq -24(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8171
    movq -248(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8172
.L8171:
.L8172:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8151
.L8152:
    jmp .L8142
.L8141:
.L8142:
    movq $1, %rax
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8181
    leaq .STR103(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L8182
.L8181:
.L8182:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -272(%rbp)
.L8191:    movq -272(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8192
    movq -272(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8201
    jmp .L8192
    jmp .L8202
.L8201:
.L8202:
    movq -272(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8211
    jmp .L8192
    jmp .L8212
.L8211:
.L8212:
    movq $0, %rax
    movq %rax, -280(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8221
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8222
.L8221:
.L8222:
    movq -272(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8231
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8232
.L8231:
.L8232:
    movq -272(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8241
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8242
.L8241:
.L8242:
    movq -272(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8251
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8252
.L8251:
.L8252:
    movq -272(%rbp), %rax
    pushq %rax
    movq $180, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8261
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_loop_forever
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8262
.L8261:
.L8262:
    movq -272(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8272
.L8271:
.L8272:
    movq -272(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8281
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8282
.L8281:
.L8282:
    movq -272(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8291
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8292
.L8291:
.L8292:
    movq -272(%rbp), %rax
    pushq %rax
    movq $171, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8301
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8302
.L8301:
.L8302:
    movq -272(%rbp), %rax
    pushq %rax
    movq $183, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8311
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_call_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8312
.L8311:
.L8312:
    movq -272(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8321
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8322
.L8321:
.L8322:
    movq -272(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8331
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_for_range_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8332
.L8331:
.L8332:
    movq -272(%rbp), %rax
    pushq %rax
    movq $139, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8341
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8342
.L8341:
.L8342:
    movq -272(%rbp), %rax
    pushq %rax
    movq $140, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8351
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8352
.L8351:
.L8352:
    movq -272(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8361
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8362
.L8361:
.L8362:
    movq -272(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8371
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8372
.L8371:
.L8372:
    movq -272(%rbp), %rax
    pushq %rax
    movq $167, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8381
    movq $167, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -296(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -304(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -312(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -320(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -304(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -312(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    leaq .STR76(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8382
.L8381:
.L8382:
    movq -272(%rbp), %rax
    pushq %rax
    movq $169, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8391
    movq $169, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -336(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -344(%rbp)
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -352(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -360(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -344(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -352(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    leaq .STR77(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8392
.L8391:
.L8392:
    movq -272(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8401
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -376(%rbp)
    movq $0, %rax
    movq %rax, -384(%rbp)
    movq -376(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8411
    leaq .STR78(%rip), %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8412
.L8411:
.L8412:
    movq -384(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8421
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -392(%rbp)
    movq $15, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -400(%rbp)
    movq $0, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -408(%rbp)
    movq $8, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -416(%rbp)
    movq $0, %rax
    movq %rax, -424(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8431
    leaq .STR79(%rip), %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8441
    movq $1, %rax
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8442
.L8441:
.L8442:
    jmp .L8432
.L8431:
.L8432:
    movq -424(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8451
    movq -408(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $125, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8452
.L8451:
.L8452:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -432(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -392(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    leaq .STR80(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -448(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8422
.L8421:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -456(%rbp)
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8422:
    jmp .L8402
.L8401:
.L8402:
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -464(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8461
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -472(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8462
.L8461:
.L8462:
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8471
    leaq .STR114(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq TOKEN_LINE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -480(%rbp)
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR115(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR19(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L8472
.L8471:
.L8472:
    movq -280(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_add_statement
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8191
.L8192:
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8481
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_add_statement
    jmp .L8482
.L8481:
.L8482:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_create
parser_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq SIZEOF_PARSER(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq PARSER_LEXER(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq PARSER_ARENA(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8491
    leaq .STR116(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L8492
.L8491:
.L8492:
    movq -32(%rbp), %rax
    pushq %rax
    movq PARSER_CURRENT_TOKEN(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_destroy
parser_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8501
    movq PARSER_CURRENT_TOKEN(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8511
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L8512
.L8511:
.L8512:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L8502
.L8501:
.L8502:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_program
parser_parse_program:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq SIZEOF_PROGRAM(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8521
    leaq .STR117(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L8522
.L8521:
.L8522:
    movq $0, %rax
    pushq %rax
    movq PROGRAM_IMPORTS(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_FUNCTIONS(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_GLOBAL_VARS(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_FUNCTION_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_IMPORT_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_GLOBAL_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_FUNCTION_CAPACITY(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_TYPE_CAPACITY(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_IMPORT_CAPACITY(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq PROGRAM_GLOBAL_CAPACITY(%rip), %rax  # Load global variable
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq PARSER_CURRENT_PROGRAM_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -40(%rbp)
.L8531:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8532
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8541
    leaq .STR118(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L8542
.L8541:
.L8542:
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8551
    movq $1, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8552
.L8551:
.L8552:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8561
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8562
.L8561:
.L8562:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8571
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $56, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8581
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8582
.L8581:
.L8582:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8591
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_import
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8601
    leaq .STR119(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L8602
.L8601:
.L8602:
    movq -80(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_import
    jmp .L8592
.L8591:
.L8592:
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8611
    movq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8612
.L8611:
.L8612:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8621
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -96(%rbp)
.L8631:    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8632
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -112(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8641
    leaq .STR120(%rip), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8642
.L8641:
.L8642:
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8651
    movq -112(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -136(%rbp)
.L8661:    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8662
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8671
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8672
.L8671:
    movq $0, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8672:
    jmp .L8661
.L8662:
    movq $0, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8652
.L8651:
    movq -112(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L8652:
    jmp .L8631
.L8632:
    jmp .L8622
.L8621:
.L8622:
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8681
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8682
.L8681:
.L8682:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8691
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_type_definition
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_type
    jmp .L8692
.L8691:
.L8692:
    movq $0, %rax
    movq %rax, -192(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $163, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8701
    movq $1, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8702
.L8701:
.L8702:
    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8711
    movq $163, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8721
    leaq .STR121(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L8722
.L8721:
.L8722:
    jmp .L8712
.L8711:
.L8712:
    movq $0, %rax
    movq %rax, -200(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $173, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8731
    movq $1, %rax
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $173, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8732
.L8731:
.L8732:
    movq $0, %rax
    movq %rax, -208(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8741
    movq $1, %rax
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8742
.L8741:
.L8742:
    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8751
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_function
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8761
    leaq .STR122(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L8762
.L8761:
.L8762:
    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8771
    movq $1, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L8772
.L8771:
.L8772:
    movq -216(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_function
    jmp .L8752
.L8751:
.L8752:
    movq $0, %rax
    movq %rax, -224(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8781
    movq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8782
.L8781:
.L8782:
    movq -224(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8791
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -232(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8801
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -248(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -256(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8811
    movq $13, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -272(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8821
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -304(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -312(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -304(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -312(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_global
    jmp .L8822
.L8821:
.L8822:
    jmp .L8812
.L8811:
.L8812:
    jmp .L8802
.L8801:
.L8802:
    jmp .L8792
.L8791:
.L8792:
    movq $0, %rax
    movq %rax, -320(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $164, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8831
    movq $1, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8832
.L8831:
.L8832:
    movq -320(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8841
    movq $164, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8851
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -352(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -368(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -376(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $21, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -392(%rbp)
    movq $0, %rax
    movq %rax, -400(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8861
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8862
.L8861:
    movq -392(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8871
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -424(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_string_literal_owned
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8872
.L8871:
    movq -392(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8881
    movq $17, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -432(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -440(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -448(%rbp)
    movq $0, %rax
    subq -448(%rbp), %rax
    movq %rax, -456(%rbp)
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8882
.L8881:
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -392(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L8882:
.L8872:
.L8862:
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -464(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -376(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -400(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -464(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_global
    jmp .L8852
.L8851:
.L8852:
    jmp .L8842
.L8841:
.L8842:
    movq $0, %rax
    movq %rax, -472(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8891
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8892
.L8891:
.L8892:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8901
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8902
.L8901:
.L8902:
    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8911
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8912
.L8911:
.L8912:
    movq -224(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8921
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8922
.L8921:
.L8922:
    movq -320(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8931
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8932
.L8931:
.L8932:
    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8941
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8942
.L8941:
.L8942:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8951
    movq $1, %rax
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8952
.L8951:
.L8952:
    movq -472(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8961
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L8962
.L8961:
.L8962:
    jmp .L8572
.L8571:
.L8572:
    jmp .L8531
.L8532:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_destroy
expression_destroy:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8971
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L8972
.L8971:
.L8972:
    movq EXPR_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_BINARY(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8981
    movq EXPR_BINARY_LEFT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq EXPR_BINARY_RIGHT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L8982
.L8981:
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_UNARY(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8991
    movq EXPR_UNARY_OPERAND(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L8992
.L8991:
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_CALL(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9001
    movq EXPR_CALL_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    jmp .L9002
.L9001:
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_FIELD_ACCESS(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9011
    movq EXPR_FIELD_OBJECT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq EXPR_FIELD_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    jmp .L9012
.L9011:
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_ARRAY_ACCESS(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9021
    movq EXPR_ARRAY_OBJECT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq EXPR_ARRAY_INDEX_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9022
.L9021:
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_IDENTIFIER(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9031
    movq EXPR_IDENTIFIER_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    jmp .L9032
.L9031:
    movq -16(%rbp), %rax
    pushq %rax
    movq EXPR_STRING_LITERAL(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9041
    movq EXPR_STRING_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    jmp .L9042
.L9041:
.L9042:
.L9032:
.L9022:
.L9012:
.L9002:
.L8992:
.L8982:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_destroy
statement_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9051
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9052
.L9051:
.L9052:
    movq STMT_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_LET(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9061
    movq STMT_LET_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq STMT_LET_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq STMT_LET_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L9062
.L9061:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_SET(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9071
    movq STMT_SET_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq STMT_SET_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9072
.L9071:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_IF(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9081
    movq STMT_IF_CONDITION(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9082
.L9081:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_WHILE(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9091
    movq STMT_WHILE_CONDITION(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9092
.L9091:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_FOR(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9101
    movq STMT_FOR_VAR(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq STMT_FOR_START(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq STMT_FOR_END(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9102
.L9101:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_FOR_EACH(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9111
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9112
.L9111:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_RETURN(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9121
    movq STMT_RETURN_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9122
.L9121:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_EXPRESSION(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9131
    movq STMT_EXPR_VALUE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L9132
.L9131:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_BREAK(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9141
    jmp .L9142
.L9141:
    movq -16(%rbp), %rax
    pushq %rax
    movq STMT_CONTINUE(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9151
    jmp .L9152
.L9151:
.L9152:
.L9142:
.L9132:
.L9122:
.L9112:
.L9102:
.L9092:
.L9082:
.L9072:
.L9062:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_destroy
function_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9161
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9162
.L9161:
.L9162:
    movq FUNCTION_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl type_destroy
type_destroy:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9171
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9172
.L9171:
.L9172:
    movq TYPE_KIND(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq TYPE_PRIMITIVE(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9181
    jmp .L9182
.L9181:
    movq -16(%rbp), %rax
    pushq %rax
    movq TYPE_STRUCT(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9191
    movq TYPE_STRUCT_NAME(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_destroy
    jmp .L9192
.L9191:
    movq -16(%rbp), %rax
    pushq %rax
    movq TYPE_ARRAY(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9201
    movq TYPE_ARRAY_ELEMENT_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L9202
.L9201:
    movq -16(%rbp), %rax
    pushq %rax
    movq TYPE_POINTER(%rip), %rax  # Load global variable
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9211
    movq TYPE_POINTER_TARGET_TYPE(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L9212
.L9211:
.L9212:
.L9202:
.L9192:
.L9182:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_destroy
program_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9221
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9222
.L9221:
.L9222:
    movq PROGRAM_FUNCTION_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq PROGRAM_FUNCTIONS(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9231
    movq $0, %rax
    movq %rax, -32(%rbp)
.L9241:    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9242
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -24(%rbp), %rax
    addq -48(%rbp), %rax
    movq %rax, -56(%rbp)
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9251
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call function_destroy
    jmp .L9252
.L9251:
.L9252:
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9241
.L9242:
    jmp .L9232
.L9231:
.L9232:
    movq PROGRAM_TYPE_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq PROGRAM_TYPES(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9261
    movq $0, %rax
    movq %rax, -88(%rbp)
.L9271:    movq -88(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9272
    movq $8, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -88(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    addq -48(%rbp), %rax
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9281
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L9282
.L9281:
.L9282:
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9271
.L9272:
    jmp .L9262
.L9261:
.L9262:
    movq PROGRAM_IMPORT_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -112(%rbp)
    movq PROGRAM_IMPORTS(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9291
    jmp .L9292
.L9291:
.L9292:
    movq PROGRAM_GLOBAL_COUNT(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -128(%rbp)
    movq PROGRAM_GLOBAL_VARS(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9301
    movq $0, %rax
    movq %rax, -144(%rbp)
.L9311:    movq -144(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9312
    movq $8, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -144(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -136(%rbp), %rax
    addq -48(%rbp), %rax
    movq %rax, -152(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9321
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_destroy
    jmp .L9322
.L9321:
.L9322:
    movq -144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9311
.L9312:
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L9302
.L9301:
.L9302:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_destroy
string_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9331
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L9332
.L9331:
.L9332:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl param_destroy
param_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9341
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9342
.L9341:
.L9342:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl field_destroy
field_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9351
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9352
.L9351:
.L9352:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl import_destroy
import_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9361
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9362
.L9361:
.L9362:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_destroy
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_import
parser_parse_import:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -16(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9371
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -80(%rbp)
.L9381:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9382
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9391
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9392
.L9391:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L9392:
    jmp .L9381
.L9382:
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -120(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -120(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9372
.L9371:
.L9372:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq $0, %rax
    movq %rax, -136(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9401
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9402
.L9401:
.L9402:
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9411
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9412
.L9411:
.L9412:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9421
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -152(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9431
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9432
.L9431:
.L9432:
    movq -168(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9441
.L9451:    movq -168(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9452
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9451
.L9452:
    movq -168(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9461
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9462
.L9461:
.L9462:
    jmp .L9442
.L9441:
.L9442:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9471
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -216(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -232(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -240(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9481
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9482
.L9481:
.L9482:
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -264(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -240(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -264(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9472
.L9471:
.L9472:
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -272(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9422
.L9421:
.L9422:
    movq -32(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9491
    leaq .STR123(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L9492
.L9491:
.L9492:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -280(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -288(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -304(%rbp)
    movq $0, %rax
    movq %rax, -312(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9501
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -320(%rbp)
    movq PARSER_CURRENT_TOKEN_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq TOKEN_TYPE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9511
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -352(%rbp)
    jmp .L9512
.L9511:
    movq -336(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9521
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -360(%rbp)
    jmp .L9522
.L9521:
    movq TOKEN_VALUE_OFFSET(%rip), %rax  # Load global variable
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -368(%rbp)
.L9522:
.L9512:
    jmp .L9502
.L9501:
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L9502:
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -376(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -312(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -376(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret

# Stack overflow panic handler
.stack_overflow_panic:
    # Print error message
    leaq .stack_overflow_msg(%rip), %rdi
    call print_string@PLT
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.section .rodata
.stack_overflow_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 83,116,97,99,107,32,111,118,101,114,102,108,111,119,32
    .byte 100,101,116,101,99,116,101,100
    .byte 10,0
.text


.null_pointer_error:
    # Print error message for null pointer
    leaq .null_pointer_msg(%rip), %rdi
    call print_string@PLT
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.bounds_error_negative:
    # Print error message for negative index
    leaq .bounds_error_negative_msg(%rip), %rdi
    call print_string@PLT
    # Print the negative index value
    movq %rbx, %rdi  # Index value
    call print_integer@PLT
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.bounds_error_overflow:
    # Save registers that will be clobbered
    pushq %rcx  # Save array size
    pushq %rbx  # Save index
    # Print error message for out-of-bounds index
    leaq .bounds_error_overflow_msg(%rip), %rdi
    call print_string@PLT
    # Print the index value
    popq %rdi  # Restore and use index
    pushq %rdi  # Save again for later
    call print_integer@PLT
    # Print size message
    leaq .bounds_error_size_msg(%rip), %rdi
    call print_string@PLT
    # Print the array size
    movq 8(%rsp), %rdi  # Get saved array size from stack
    call print_integer@PLT
    # Clean up stack
    addq $16, %rsp
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.section .rodata
.null_pointer_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 78,117,108,108,32,112,111,105,110,116,101,114,32
    .byte 100,101,114,101,102,101,114,101,110,99,101
    .byte 10,0

.bounds_error_negative_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 65,114,114,97,121,32,105,110,100,101,120,32
    .byte 105,115,32,110,101,103,97,116,105,118,101,58,32
    .byte 0

.bounds_error_overflow_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 65,114,114,97,121,32,105,110,100,101,120,32
    .byte 111,117,116,32,111,102,32,98,111,117,110,100,115,58,32
    .byte 0

.bounds_error_size_msg:
    .byte 32,40,97,114,114,97,121,32,115,105,122,101,32,105,115,32
    .byte 41,10,0


.section .note.GNU-stack
