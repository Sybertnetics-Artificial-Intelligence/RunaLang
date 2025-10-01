.section .rodata
.STR0:    .string "[PARSER ERROR] Expected field name after '.' at line "
.STR1:    .string "[PARSER ERROR] Expected 'than' after 'less' at line "
.STR2:    .string "[PARSER ERROR] Expected 'than' after 'greater' at line "
.STR3:    .string "[PARSER ERROR] Expected 'equal', 'less', or 'greater' after 'is' at line "
.STR4:    .string "[PARSER ERROR] NULL parser in parser_parse_let_statement"
.STR5:    .string "[PARSER ERROR] Expected identifier after Let at line "
.STR6:    .string "[PARSER ERROR] parser became NULL before expression parsing in Let"
.STR7:    .string "[PARSER ERROR] Expected token type "
.STR8:    .string ", got "
.STR9:    .string " at line "
.STR10:    .string "[PARSER ERROR] Null parser in parse_primary"
.STR11:    .string "[PARSER ERROR] Null current_token in parse_primary"
.STR12:    .string "[PARSER ERROR] Expected function name after $ at line "
.STR13:    .string "[PARSER ERROR] Expected ',' or ')' in function arguments at line "
.STR14:    .string "[PARSER ERROR] Expected integer after 'negative' at line "
.STR15:    .string "[PARSER ERROR] Expected integer or identifier at line "
.STR16:    .string "[PARSER ERROR] Only function calls can be used as statements (expr_type="
.STR17:    .string ", expected "
.STR18:    .string ") at line "
.STR19:    .string "[PARSER ERROR] Invalid builtin function statement at line "
.STR20:    .string "[PARSER ERROR] Inline assembly not yet implemented in v0.0.7.6\n"
.STR21:    .string "[PARSER ERROR] Expected variant name after 'When' at line "
.STR22:    .string "[PARSER ERROR] Expected field name in match case at line "
.STR23:    .string "[PARSER ERROR] Expected binding variable name at line "
.STR24:    .string "Integer"
.STR25:    .string "Byte"
.STR26:    .string "Short"
.STR27:    .string "Long"
.STR28:    .string "[PARSER WARNING] Unknown type '"
.STR29:    .string "', defaulting to 8 bytes"
.STR30:    .string "[PARSER ERROR] Expected type name at line "
.STR31:    .string "[PARSER ERROR] Expected field name at line "
.STR32:    .string " (got token type "
.STR33:    .string ")"
.STR34:    .string "[PARSER ERROR] Expected field type at line "
.STR35:    .string "[PARSER ERROR] Expected array size at line "
.STR36:    .string "String"
.STR37:    .string "Character"
.STR38:    .string "[PARSER ERROR] Expected element type at line "
.STR39:    .string "[PARSER ERROR] Expected array or variant declaration after colon at line "
.STR40:    .string "[PARSER ERROR] Expected parameter type at line "
.STR41:    .string "[PARSER ERROR] Expected return type at line "
.STR42:    .string "[PARSER ERROR] Expected variant name at line "
.STR43:    .string "[PARSER ERROR] Expected field name in variant at line "
.STR44:    .string "[PARSER ERROR] Expected 'called' or type name after 'Type' at line "
.STR45:    .string "[PARSER ERROR] Expected function name string literal (type "
.STR46:    .string "), got type "
.STR47:    .string "[PARSER ERROR] Function name is NULL!"
.STR48:    .string "[PARSER ERROR] Expected parameter name at line "
.STR49:    .string "[PARSER ERROR] Expected parameter name after comma at line "
.STR50:    .string "[PARSER ERROR] Only function calls can be used as statements (got expr_type="
.STR51:    .string "[PARSER ERROR] Unexpected token in function body at line "
.STR52:    .string "[ERROR] lexer_next_token returned NULL!"
.STR53:    .string "[ERROR] First token is already EOF!"
.STR54:    .string "[ERROR] current_token is NULL!"
.STR55:    .string "[ERROR] parser_parse_function returned NULL!"

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
.globl STMT_IMPORT
STMT_IMPORT:    .quad 8
.globl STMT_BREAK
STMT_BREAK:    .quad 9
.globl STMT_CONTINUE
STMT_CONTINUE:    .quad 10
.globl STMT_FOR
STMT_FOR:    .quad 11
.globl STMT_INLINE_ASSEMBLY
STMT_INLINE_ASSEMBLY:    .quad 16
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
.globl EXPRESSION_TYPE_OFFSET
EXPRESSION_TYPE_OFFSET:    .quad 0
.globl SIZEOF_PARSER
SIZEOF_PARSER:    .quad 24
.globl SIZEOF_PROGRAM
SIZEOF_PROGRAM:    .quad 64
.globl PARSER_LEXER
PARSER_LEXER:    .quad 0
.globl PARSER_CURRENT_TOKEN
PARSER_CURRENT_TOKEN:    .quad 8
.globl PARSER_CURRENT_PROGRAM_OFFSET
PARSER_CURRENT_PROGRAM_OFFSET:    .quad 16
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
.text


.globl token_can_be_identifier
token_can_be_identifier:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
.L2:
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
.L12:
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
.L22:
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
.L32:
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
.L42:
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
.L52:
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
.L62:
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
.L72:
    movq -8(%rbp), %rax
    pushq %rax
    movq $155, %rax
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
.L82:
    movq -8(%rbp), %rax
    pushq %rax
    movq $156, %rax
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
.L92:
    movq -8(%rbp), %rax
    pushq %rax
    movq $144, %rax
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
.L102:
    movq -8(%rbp), %rax
    pushq %rax
    movq $145, %rax
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
.L112:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_expression
parser_parse_expression:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_comparison_level
parser_parse_comparison_level:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_additive
parser_parse_additive:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_multiplicative
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L121:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L122
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
    jz .L131
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
    jmp .L132
.L131:
    movq -40(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L142
.L141:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L142:
.L132:
    jmp .L121
.L122:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_multiplicative
parser_parse_multiplicative:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary_with_postfix
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L151:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L152
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
    jz .L161
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
    jmp .L162
.L161:
    movq -40(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L172
.L171:
    movq -40(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L182
.L181:
    movq -40(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
    movq $42, %rax
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
    jmp .L192
.L191:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L192:
.L182:
.L172:
.L162:
    jmp .L151
.L152:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_primary_with_postfix
parser_parse_primary_with_postfix:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
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
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant EXPR_VARIABLE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq $4, %rax
    movq %rax, -72(%rbp)
    movq $8, %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -96(%rbp)
.L221:    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L222
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L231
    movq $0, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L232
.L231:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -120(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -128(%rbp)
    movq -56(%rbp), %rax
    addq -128(%rbp), %rax
    movq %rax, -136(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -64(%rbp), %rax
    addq $1, %rax
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
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L242
.L241:
.L242:
.L232:
    jmp .L221
.L222:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -64(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -160(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -160(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L212
.L211:
.L212:
    jmp .L202
.L201:
.L202:
    movq $1, %rax
    movq %rax, -168(%rbp)
.L251:    movq -168(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L252
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
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
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
    movq %rax, -192(%rbp)
    movq $0, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    leaq .STR0(%rip), %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L272
.L271:
.L272:
    movq $8, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -232(%rbp)
    movq $53, %rax
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
    movq %rax, -240(%rbp)
    movq $10, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -232(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -240(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L262
.L261:
    movq -184(%rbp), %rax
    pushq %rax
    movq $127, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    movq $127, %rax
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
    movq %rax, -248(%rbp)
    movq $49, %rax
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
    movq %rax, -256(%rbp)
    movq $16, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -248(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -256(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L282
.L281:
    movq $0, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L282:
.L262:
    jmp .L251
.L252:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_comparison
parser_parse_comparison:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L291
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
    jz .L301
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
    jmp .L302
.L301:
.L302:
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
    jz .L311
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
    jz .L321
    movq $23, %rax
    movq %rax, -64(%rbp)
    jmp .L322
.L321:
    movq $22, %rax
    movq %rax, -64(%rbp)
.L322:
    jmp .L312
.L311:
.L312:
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L331
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
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L341
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
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
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
    jz .L361
    movq $25, %rax
    movq %rax, -64(%rbp)
    jmp .L362
.L361:
    movq $27, %rax
    movq %rax, -64(%rbp)
.L362:
    jmp .L352
.L351:
.L352:
    movq -112(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    movq $26, %rax
    movq %rax, -64(%rbp)
    jmp .L382
.L381:
    movq $24, %rax
    movq %rax, -64(%rbp)
.L382:
    jmp .L372
.L371:
.L372:
    jmp .L342
.L341:
.L342:
    movq -96(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L391
    leaq .STR1(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -88(%rbp), %rax
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
    jmp .L392
.L391:
.L392:
    jmp .L332
.L331:
.L332:
    movq -48(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
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
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
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
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
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
    jz .L431
    movq $24, %rax
    movq %rax, -64(%rbp)
    jmp .L432
.L431:
    movq $26, %rax
    movq %rax, -64(%rbp)
.L432:
    jmp .L422
.L421:
.L422:
    movq -112(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L451
    movq $27, %rax
    movq %rax, -64(%rbp)
    jmp .L452
.L451:
    movq $25, %rax
    movq %rax, -64(%rbp)
.L452:
    jmp .L442
.L441:
.L442:
    jmp .L412
.L411:
.L412:
    movq -96(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    leaq .STR2(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -88(%rbp), %rax
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
    jmp .L462
.L461:
.L462:
    jmp .L402
.L401:
.L402:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L471
    leaq .STR3(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
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
    jmp .L472
.L471:
.L472:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
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
    jmp .L292
.L291:
.L292:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_let_statement
parser_parse_let_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    leaq .STR4(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L482
.L481:
.L482:
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
    jz .L491
    leaq .STR5(%rip), %rax
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
    jmp .L492
.L491:
.L492:
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
    jz .L501
    leaq .STR6(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L502
.L501:
.L502:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_create_let
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_set_statement
parser_parse_set_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_create_set
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_duplicate_parser
string_duplicate_parser:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L511
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L512
.L511:
.L512:
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_advance
parser_advance:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_eat
parser_eat:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L521
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -40(%rbp)
    jmp .L522
.L521:
    leaq .STR7(%rip), %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR8(%rip), %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR9(%rip), %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
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
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L522:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_is_builtin_function_token
parser_is_builtin_function_token:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $54, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L532
.L531:
.L532:
    movq -8(%rbp), %rax
    pushq %rax
    movq $55, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L541
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L542
.L541:
.L542:
    movq -8(%rbp), %rax
    pushq %rax
    movq $57, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L551
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L552
.L551:
.L552:
    movq -8(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L561
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L562
.L561:
.L562:
    movq -8(%rbp), %rax
    pushq %rax
    movq $59, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L572
.L571:
.L572:
    movq -8(%rbp), %rax
    pushq %rax
    movq $60, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L581
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L582
.L581:
.L582:
    movq -8(%rbp), %rax
    pushq %rax
    movq $61, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L592
.L591:
.L592:
    movq -8(%rbp), %rax
    pushq %rax
    movq $62, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L601
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L602
.L601:
.L602:
    movq -8(%rbp), %rax
    pushq %rax
    movq $63, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L611
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L612
.L611:
.L612:
    movq -8(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L621
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L622
.L621:
.L622:
    movq -8(%rbp), %rax
    pushq %rax
    movq $65, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L632
.L631:
.L632:
    movq -8(%rbp), %rax
    pushq %rax
    movq $66, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L641
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L642
.L641:
.L642:
    movq -8(%rbp), %rax
    pushq %rax
    movq $67, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L651
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L652
.L651:
.L652:
    movq -8(%rbp), %rax
    pushq %rax
    movq $68, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L661
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L662
.L661:
.L662:
    movq -8(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L671
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L672
.L671:
.L672:
    movq -8(%rbp), %rax
    pushq %rax
    movq $70, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L681
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L682
.L681:
.L682:
    movq -8(%rbp), %rax
    pushq %rax
    movq $71, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L691
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L692
.L691:
.L692:
    movq -8(%rbp), %rax
    pushq %rax
    movq $72, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L701
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L702
.L701:
.L702:
    movq -8(%rbp), %rax
    pushq %rax
    movq $73, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L712
.L711:
.L712:
    movq -8(%rbp), %rax
    pushq %rax
    movq $74, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L722
.L721:
.L722:
    movq -8(%rbp), %rax
    pushq %rax
    movq $75, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L731
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L732
.L731:
.L732:
    movq -8(%rbp), %rax
    pushq %rax
    movq $76, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L741
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L742
.L741:
.L742:
    movq -8(%rbp), %rax
    pushq %rax
    movq $77, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L752
.L751:
.L752:
    movq -8(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L761
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L762
.L761:
.L762:
    movq -8(%rbp), %rax
    pushq %rax
    movq $79, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L771
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L772
.L771:
.L772:
    movq -8(%rbp), %rax
    pushq %rax
    movq $80, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L781
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L782
.L781:
.L782:
    movq -8(%rbp), %rax
    pushq %rax
    movq $81, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L791
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L792
.L791:
.L792:
    movq -8(%rbp), %rax
    pushq %rax
    movq $82, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L801
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L802
.L801:
.L802:
    movq -8(%rbp), %rax
    pushq %rax
    movq $83, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L811
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L812
.L811:
.L812:
    movq -8(%rbp), %rax
    pushq %rax
    movq $84, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L821
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L822
.L821:
.L822:
    movq -8(%rbp), %rax
    pushq %rax
    movq $85, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L831
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L832
.L831:
.L832:
    movq -8(%rbp), %rax
    pushq %rax
    movq $86, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L841
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L842
.L841:
.L842:
    movq -8(%rbp), %rax
    pushq %rax
    movq $87, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L851
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L852
.L851:
.L852:
    movq -8(%rbp), %rax
    pushq %rax
    movq $88, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L861
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L862
.L861:
.L862:
    movq -8(%rbp), %rax
    pushq %rax
    movq $89, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L872
.L871:
.L872:
    movq -8(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L881
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L882
.L881:
.L882:
    movq -8(%rbp), %rax
    pushq %rax
    movq $91, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L892
.L891:
.L892:
    movq -8(%rbp), %rax
    pushq %rax
    movq $92, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L901
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L902
.L901:
.L902:
    movq -8(%rbp), %rax
    pushq %rax
    movq $93, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L911
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L912
.L911:
.L912:
    movq -8(%rbp), %rax
    pushq %rax
    movq $94, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L921
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L922
.L921:
.L922:
    movq -8(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L932
.L931:
.L932:
    movq -8(%rbp), %rax
    pushq %rax
    movq $96, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L942
.L941:
.L942:
    movq -8(%rbp), %rax
    pushq %rax
    movq $97, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L951
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L952
.L951:
.L952:
    movq -8(%rbp), %rax
    pushq %rax
    movq $98, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L962
.L961:
.L962:
    movq -8(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L971
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L972
.L971:
.L972:
    movq -8(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L981
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L982
.L981:
.L982:
    movq -8(%rbp), %rax
    pushq %rax
    movq $101, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L991
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L992
.L991:
.L992:
    movq -8(%rbp), %rax
    pushq %rax
    movq $102, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1002
.L1001:
.L1002:
    movq -8(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1011
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1012
.L1011:
.L1012:
    movq -8(%rbp), %rax
    pushq %rax
    movq $104, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1021
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1022
.L1021:
.L1022:
    movq -8(%rbp), %rax
    pushq %rax
    movq $105, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1032
.L1031:
.L1032:
    movq -8(%rbp), %rax
    pushq %rax
    movq $106, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1041
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1042
.L1041:
.L1042:
    movq -8(%rbp), %rax
    pushq %rax
    movq $107, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1052
.L1051:
.L1052:
    movq -8(%rbp), %rax
    pushq %rax
    movq $108, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1062
.L1061:
.L1062:
    movq -8(%rbp), %rax
    pushq %rax
    movq $109, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1072
.L1071:
.L1072:
    movq -8(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1081
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1082
.L1081:
.L1082:
    movq -8(%rbp), %rax
    pushq %rax
    movq $115, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1092
.L1091:
.L1092:
    movq -8(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1102
.L1101:
.L1102:
    movq -8(%rbp), %rax
    pushq %rax
    movq $117, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1112
.L1111:
.L1112:
    movq -8(%rbp), %rax
    pushq %rax
    movq $118, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1122
.L1121:
.L1122:
    movq -8(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1132
.L1131:
.L1132:
    movq -8(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1141
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1142
.L1141:
.L1142:
    movq -8(%rbp), %rax
    pushq %rax
    movq $130, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1151
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1152
.L1151:
.L1152:
    movq -8(%rbp), %rax
    pushq %rax
    movq $131, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1161
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1162
.L1161:
.L1162:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_integer
expression_create_integer:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax  # Load compile-time constant EXPR_INTEGER
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_variable
expression_create_variable:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $1, %rax  # Load compile-time constant EXPR_VARIABLE
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_binary_op
expression_create_binary_op:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $2, %rax  # Load compile-time constant EXPR_BINARY_OP
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_comparison
expression_create_comparison:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $3, %rax  # Load compile-time constant EXPR_COMPARISON
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_function_call
expression_create_function_call:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_create_string_literal_owned
expression_create_string_literal_owned:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $5, %rax  # Load compile-time constant EXPR_STRING_LITERAL
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_let
statement_create_let:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $24, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq $1, %rax  # Load compile-time constant STMT_LET
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_set
statement_create_set:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $24, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq $2, %rax  # Load compile-time constant STMT_SET
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_return
statement_create_return:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $24, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $3, %rax  # Load compile-time constant STMT_RETURN
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_print
statement_create_print:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $24, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $4, %rax  # Load compile-time constant STMT_PRINT
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_expression
statement_create_expression:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $24, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $7, %rax  # Load compile-time constant STMT_EXPRESSION
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_if
statement_create_if:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $5, %rax  # Load compile-time constant STMT_IF
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_while
statement_create_while:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $6, %rax  # Load compile-time constant STMT_WHILE
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_break
statement_create_break:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $8, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $9, %rax  # Load compile-time constant STMT_BREAK
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_create_continue
statement_create_continue:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $8, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq $10, %rax  # Load compile-time constant STMT_CONTINUE
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_create
function_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_add_parameter
function_add_parameter:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    call memory_set_integer@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_add_statement
function_add_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_create
program_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_function
program_add_function:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L1171
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1181
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1182
.L1181:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1182:
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
    jmp .L1172
.L1171:
.L1172:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer_at_index@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_global
program_add_global:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L1191
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1202
.L1201:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1202:
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
    jmp .L1192
.L1191:
.L1192:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer_at_index@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_type
program_add_type:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L1211
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1222
.L1221:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1222:
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
    jmp .L1212
.L1211:
.L1212:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer_at_index@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_add_import
program_add_import:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L1231
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1242
.L1241:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1242:
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
    jmp .L1232
.L1231:
.L1232:
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer_at_index@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_primary
parser_parse_primary:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1251
    leaq .STR10(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1252
.L1251:
.L1252:
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
    jz .L1261
    leaq .STR11(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1262
.L1261:
.L1262:
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
    call parser_is_builtin_function_token
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1271
    movq -24(%rbp), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -48(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1281
    movq $2, %rax
    movq %rax, -96(%rbp)
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -120(%rbp)
.L1291:    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1292
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
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -144(%rbp)
    jmp .L1302
.L1301:
.L1302:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -152(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
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
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1312
.L1311:
.L1312:
    movq -72(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -64(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -176(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -72(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
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
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
    movq $0, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1322
.L1321:
.L1322:
    jmp .L1291
.L1292:
    jmp .L1282
.L1281:
.L1282:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -200(%rbp)
    movq $32, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -216(%rbp)
    movq $8, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -72(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1272
.L1271:
.L1272:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -232(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -240(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1332
.L1331:
.L1332:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -264(%rbp)
    movq $0, %rax
    movq %rax, -272(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1351
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -288(%rbp)
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -304(%rbp)
.L1361:    movq -304(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1362
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -296(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -328(%rbp)
    movq $0, %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -336(%rbp)
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1371
    movq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -288(%rbp), %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1372
.L1371:
    movq -304(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1372:
    jmp .L1361
.L1362:
    jmp .L1352
.L1351:
.L1352:
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -360(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1381
    movq $32, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -216(%rbp)
    movq $7, %rax  # Load compile-time constant EXPR_TYPE_NAME
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1382
.L1381:
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_string_literal_owned
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1382:
    jmp .L1342
.L1341:
.L1342:
    movq -24(%rbp), %rax
    pushq %rax
    movq $157, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1391
    movq $157, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -392(%rbp)
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
    movq -408(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1401
    leaq .STR12(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1402
.L1401:
.L1402:
    movq $8, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -424(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -432(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -440(%rbp)
    movq $32, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -216(%rbp)
    movq $10, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -432(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1392
.L1391:
.L1392:
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1411
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
    movq %rax, -464(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -464(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1412
.L1411:
.L1412:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1421
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
    movq %rax, -472(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -480(%rbp)
    movq $17, %rax
    pushq %rax
    movq -472(%rbp), %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1422
.L1421:
.L1422:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1431
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -512(%rbp)
    movq $0, %rax
    movq %rax, -272(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1441
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -288(%rbp)
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -304(%rbp)
    movq $1, %rax
    movq %rax, -560(%rbp)
.L1451:    movq -560(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1452
    movq $0, %rax
    movq %rax, -568(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1461
    movq $1, %rax
    movq %rax, -568(%rbp)
    jmp .L1462
.L1461:
.L1462:
    movq -568(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1471
    movq $0, %rax
    movq %rax, -560(%rbp)
    jmp .L1472
.L1471:
.L1472:
    movq -568(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1481
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -296(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -328(%rbp)
    movq $0, %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -336(%rbp)
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1491
    movq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -560(%rbp)
    jmp .L1492
.L1491:
.L1492:
    movq -304(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1482
.L1481:
.L1482:
    jmp .L1451
.L1452:
    jmp .L1442
.L1441:
.L1442:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -648(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -656(%rbp)
    movq $0, %rax
    pushq %rax
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -664(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1501
    movq -512(%rbp), %rax
    movq %rax, -672(%rbp)
    movq $0, %rax
    movq %rax, -680(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1511
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -288(%rbp)
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -304(%rbp)
    movq $1, %rax
    movq %rax, -712(%rbp)
.L1521:    movq -712(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1522
    movq $0, %rax
    movq %rax, -720(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1531
    movq $1, %rax
    movq %rax, -720(%rbp)
    jmp .L1532
.L1531:
.L1532:
    movq -720(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1541
    movq $0, %rax
    movq %rax, -712(%rbp)
    jmp .L1542
.L1541:
.L1542:
    movq -720(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1551
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -296(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -328(%rbp)
    movq $0, %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -336(%rbp)
    movq $8, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -776(%rbp)
    movq $0, %rax
    movq %rax, -784(%rbp)
    movq -776(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant TYPE_KIND_VARIANT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1561
    movq $1, %rax
    movq %rax, -784(%rbp)
    jmp .L1562
.L1561:
.L1562:
    movq -784(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1571
    movq $24, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -800(%rbp)
    movq $16, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -808(%rbp)
    movq $0, %rax
    movq %rax, -816(%rbp)
    movq $1, %rax
    movq %rax, -824(%rbp)
.L1581:    movq -824(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1582
    movq $0, %rax
    movq %rax, -832(%rbp)
    movq -816(%rbp), %rax
    pushq %rax
    movq -800(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1591
    movq $1, %rax
    movq %rax, -832(%rbp)
    jmp .L1592
.L1591:
.L1592:
    movq -832(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1601
    movq $0, %rax
    movq %rax, -824(%rbp)
    jmp .L1602
.L1601:
.L1602:
    movq -832(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1611
    movq -816(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -856(%rbp)
    movq -808(%rbp), %rax
    addq -856(%rbp), %rax
    movq %rax, -864(%rbp)
    movq $0, %rax
    pushq %rax
    movq -864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -872(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq -872(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -880(%rbp)
    movq -880(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1621
    movq -336(%rbp), %rax
    movq %rax, -680(%rbp)
    movq $0, %rax
    movq %rax, -824(%rbp)
    movq $0, %rax
    movq %rax, -712(%rbp)
    jmp .L1622
.L1621:
.L1622:
    movq -816(%rbp), %rax
    addq $1, %rax
    movq %rax, -816(%rbp)
    jmp .L1612
.L1611:
.L1612:
    jmp .L1581
.L1582:
    jmp .L1572
.L1571:
.L1572:
    movq -304(%rbp), %rax
    addq $1, %rax
    movq %rax, -304(%rbp)
    jmp .L1552
.L1551:
.L1552:
    jmp .L1521
.L1522:
    jmp .L1512
.L1511:
.L1512:
    movq -680(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1631
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $40, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -216(%rbp)
    movq $9, %rax  # Load compile-time constant EXPR_VARIANT_CONSTRUCTOR
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -944(%rbp)
    movq -944(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -672(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1632
.L1631:
.L1632:
    jmp .L1502
.L1501:
.L1502:
    movq $0, %rax
    movq %rax, -952(%rbp)
    movq -952(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1641
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -960(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $0, %rax
    movq %rax, -984(%rbp)
    movq $1, %rax
    movq %rax, -992(%rbp)
.L1651:    movq -992(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
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
    movq %rax, -1000(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1000(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1008(%rbp)
    movq -1008(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1661
    movq $0, %rax
    pushq %rax
    leaq -992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1662
.L1661:
.L1662:
    movq -1008(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1671
    movq $0, %rax
    pushq %rax
    leaq -992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1672
.L1671:
.L1672:
    movq $0, %rax
    movq %rax, -1016(%rbp)
    movq -1008(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1681
    movq -1008(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1691
    movq $1, %rax
    pushq %rax
    leaq -1016(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1692
.L1691:
.L1692:
    jmp .L1682
.L1681:
.L1682:
    movq -1016(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1701
    movq -72(%rbp), %rax
    pushq %rax
    movq -984(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1711
    movq -984(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1721
    movq $4, %rax
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1722
.L1721:
.L1722:
    movq -984(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1731
    movq -984(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1732
.L1731:
.L1732:
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -984(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1712
.L1711:
.L1712:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -152(%rbp)
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -64(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -176(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -72(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1072(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1080(%rbp)
    movq -1080(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1741
    movq $0, %rax
    pushq %rax
    leaq -992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1742
.L1741:
.L1742:
    movq -1080(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1751
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1088(%rbp)
    jmp .L1752
.L1751:
.L1752:
    movq -1080(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1761
    movq -1080(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1771
    leaq .STR13(%rip), %rax
    movq %rax, -1096(%rbp)
    movq -1096(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -1072(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1104(%rbp)
    movq -1104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1772
.L1771:
.L1772:
    jmp .L1762
.L1761:
.L1762:
    jmp .L1702
.L1701:
.L1702:
    jmp .L1651
.L1652:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1112(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1642
.L1641:
.L1642:
    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1781
    movq $32, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -216(%rbp)
    movq $7, %rax  # Load compile-time constant EXPR_TYPE_NAME
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -512(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1782
.L1781:
.L1782:
    movq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1432
.L1431:
.L1432:
    movq -24(%rbp), %rax
    pushq %rax
    movq $134, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1791
    movq $134, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1152(%rbp)
    movq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1792
.L1791:
.L1792:
    movq -24(%rbp), %rax
    pushq %rax
    movq $135, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1801
    movq $135, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -960(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1802
.L1801:
.L1802:
    movq -24(%rbp), %rax
    pushq %rax
    movq $133, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1811
    movq $133, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1088(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1192(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1200(%rbp)
    movq -1200(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1821
    leaq .STR14(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -1192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1822
.L1821:
.L1822:
    movq $8, %rax
    pushq %rax
    movq -1192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -232(%rbp)
    movq $0, %rax
    subq -232(%rbp), %rax
    movq %rax, -1232(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1240(%rbp)
    movq -1232(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1812
.L1811:
.L1812:
    leaq .STR15(%rip), %rax
    movq %rax, -1096(%rbp)
    movq -1096(%rbp), %rax
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
    movq %rax, -1104(%rbp)
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_return_statement
parser_parse_return_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $7, %rax
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
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_return
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_break_statement
parser_parse_break_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_continue_statement
parser_parse_continue_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_print_statement
parser_parse_print_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $47, %rax
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
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_print
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_statement_block
parser_parse_statement_block:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
.L1831:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1832
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
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1841
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1842
.L1841:
.L1842:
    movq -56(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1851
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1852
.L1851:
.L1852:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1861
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1862
.L1861:
.L1862:
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1871
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
    jz .L1881
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1882
.L1881:
.L1882:
    movq -56(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1891
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1892
.L1891:
.L1892:
    movq -56(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1901
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1902
.L1901:
.L1902:
    movq -56(%rbp), %rax
    pushq %rax
    movq $44, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1911
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_break_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1912
.L1911:
.L1912:
    movq -56(%rbp), %rax
    pushq %rax
    movq $45, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1921
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_continue_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1922
.L1921:
.L1922:
    movq -56(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1931
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1932
.L1931:
.L1932:
    movq -56(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1941
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1942
.L1941:
.L1942:
    movq -56(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1951
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1952
.L1951:
.L1952:
    movq -56(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1961
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1962
.L1961:
.L1962:
    movq -56(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1971
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1972
.L1971:
.L1972:
    movq -56(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1981
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
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
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1991
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1992
.L1991:
.L1992:
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2001
    leaq .STR16(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR18(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2002
.L2001:
.L2002:
    jmp .L1982
.L1981:
.L1982:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2011
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
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
    movq $8, %rax  # Load compile-time constant EXPR_BUILTIN_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2021
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2022
.L2021:
.L2022:
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant EXPR_BUILTIN_CALL
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2031
    leaq .STR19(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2032
.L2031:
.L2032:
    jmp .L2012
.L2011:
.L2012:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2041
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2042
.L2041:
.L2042:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2051
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2071
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2072
.L2071:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2072:
    movq $8, %rax
    movq %rax, -152(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
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
    jmp .L2062
.L2061:
.L2062:
    movq $8, %rax
    movq %rax, -152(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -176(%rbp)
    movq -24(%rbp), %rax
    addq -176(%rbp), %rax
    movq %rax, -184(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -144(%rbp), %rax
    addq $1, %rax
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L2052
.L2051:
.L2052:
    jmp .L1872
.L1871:
.L1872:
    jmp .L1831
.L1832:
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_while_statement
parser_parse_while_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    call parser_parse_comparison
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_if_statement
parser_parse_if_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    call parser_parse_comparison
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
.L2081:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2082
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
    jz .L2091
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
    jz .L2101
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
    call parser_parse_comparison
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
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2111
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
    jmp .L2112
.L2111:
.L2112:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2121
    movq -64(%rbp), %rax
    movq %rax, -184(%rbp)
    movq -72(%rbp), %rax
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    addq $1, %rax
    movq %rax, -200(%rbp)
    movq $8, %rax
    movq %rax, -208(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -224(%rbp)
.L2131:    movq -224(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2132
    movq -224(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -232(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -240(%rbp)
    movq -184(%rbp), %rax
    addq -232(%rbp), %rax
    movq %rax, -248(%rbp)
    movq -64(%rbp), %rax
    addq -240(%rbp), %rax
    movq %rax, -256(%rbp)
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -224(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2131
.L2132:
    movq -192(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq -64(%rbp), %rax
    addq -272(%rbp), %rax
    movq %rax, -280(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -200(%rbp), %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2122
.L2121:
.L2122:
    jmp .L2102
.L2101:
.L2102:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2141
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -288(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -304(%rbp)
    movq $0, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -312(%rbp)
    movq -296(%rbp), %rax
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
    jz .L2151
    movq -304(%rbp), %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2152
.L2151:
.L2152:
    movq -64(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2161
    movq -304(%rbp), %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2162
.L2161:
.L2162:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2142
.L2141:
.L2142:
    jmp .L2092
.L2091:
.L2092:
    movq -96(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2171
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2172
.L2171:
.L2172:
    jmp .L2081
.L2082:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -320(%rbp)
    movq $18, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -328(%rbp)
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_inline_assembly_statement
parser_parse_inline_assembly_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR20(%rip), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_match_statement
parser_parse_match_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $112, %rax
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
    movq $32, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -48(%rbp)
    movq $8, %rax  # Load compile-time constant STMT_MATCH
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $1, %rax
    movq %rax, -56(%rbp)
.L2181:    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2182
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
    movq $113, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2191
    movq $113, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -80(%rbp)
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
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2201
    leaq .STR21(%rip), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -88(%rbp), %rax
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
    jmp .L2202
.L2201:
.L2202:
    movq $8, %rax
    pushq %rax
    movq -88(%rbp), %rax
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
    movq %rax, -136(%rbp)
    movq $0, %rax
    movq %rax, -144(%rbp)
    movq $0, %rax
    movq %rax, -152(%rbp)
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
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2211
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -176(%rbp)
    movq $10, %rax
    movq %rax, -184(%rbp)
    movq $8, %rax
    movq %rax, -192(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -208(%rbp)
.L2221:    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2222
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
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2231
    leaq .STR22(%rip), %rax
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2232
.L2231:
.L2232:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -248(%rbp)
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -256(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq $0, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2241
    leaq .STR23(%rip), %rax
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2242
.L2241:
.L2242:
    movq $8, %rax
    pushq %rax
    movq -264(%rbp), %rax
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
    movq -152(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -312(%rbp)
    movq -144(%rbp), %rax
    addq -312(%rbp), %rax
    movq %rax, -320(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -152(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -328(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -336(%rbp)
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2251
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -352(%rbp)
    jmp .L2252
.L2251:
    movq $0, %rax
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2252:
    jmp .L2221
.L2222:
    jmp .L2212
.L2211:
.L2212:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -360(%rbp)
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
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -392(%rbp)
    movq $113, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -400(%rbp)
    movq $24, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    addq $1, %rax
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $32, %rax
    movq %rax, -424(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq -424(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -432(%rbp)
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -448(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -408(%rbp), %rax
    pushq %rax
    movq -424(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -456(%rbp)
    movq -448(%rbp), %rax
    addq -456(%rbp), %rax
    movq %rax, -464(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -144(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -152(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -376(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L2192
.L2191:
    movq $0, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2192:
    jmp .L2181
.L2182:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -472(%rbp)
    movq $112, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -480(%rbp)
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl calculate_type_size
calculate_type_size:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    leaq .STR24(%rip), %rax
    movq %rax, -24(%rbp)
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
    jz .L2261
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2262
.L2261:
.L2262:
    leaq .STR25(%rip), %rax
    movq %rax, -32(%rbp)
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
    jz .L2271
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2272
.L2271:
.L2272:
    leaq .STR26(%rip), %rax
    movq %rax, -40(%rbp)
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
    jz .L2281
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2282
.L2281:
.L2282:
    leaq .STR27(%rip), %rax
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
    jz .L2291
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2292
.L2291:
.L2292:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2301
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
.L2311:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2312
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
    jz .L2321
    movq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L2322
.L2321:
.L2322:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2331
    movq $0, %rax
    movq %rax, -80(%rbp)
    jmp .L2332
.L2331:
.L2332:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2341
    movq $8, %rax
    movq %rax, -112(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -120(%rbp)
    movq -64(%rbp), %rax
    addq -120(%rbp), %rax
    movq %rax, -128(%rbp)
    movq $0, %rax
    pushq %rax
    movq -128(%rbp), %rax
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
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2351
    movq $40, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2352
.L2351:
.L2352:
    movq -72(%rbp), %rax
    addq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L2342
.L2341:
.L2342:
    jmp .L2311
.L2312:
    jmp .L2302
.L2301:
.L2302:
    leaq .STR28(%rip), %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR29(%rip), %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_type_definition
parser_parse_type_definition:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq $8, %rax
    movq %rax, -24(%rbp)
    movq $16, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq $8, %rax
    movq %rax, -48(%rbp)
    movq $16, %rax
    movq %rax, -56(%rbp)
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax  # Load compile-time constant TypeDefinition_SIZE
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -64(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2361
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2371
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2372
.L2371:
.L2372:
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEDEFINITION_NAME_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rax, -128(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
.L2381:    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2382
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2391
    leaq .STR31(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR32(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR33(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2392
.L2391:
.L2392:
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -168(%rbp)
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
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2401
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2411
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2421
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2431
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2432
.L2431:
.L2432:
    jmp .L2422
.L2421:
.L2422:
    jmp .L2412
.L2411:
.L2412:
    jmp .L2402
.L2401:
.L2402:
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -208(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2441
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2442
.L2441:
.L2442:
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2451
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2452
.L2451:
.L2452:
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2461
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2462
.L2461:
.L2462:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2472
.L2471:
.L2472:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
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
    jz .L2481
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2482
.L2481:
.L2482:
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    addq $1, %rax
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -256(%rbp)
    movq $0, %rax
    movq %rax, -264(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2491
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2492
.L2491:
    movq -256(%rbp), %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2492:
    movq -264(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -240(%rbp), %rax
    subq $1, %rax
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -280(%rbp)
    movq -264(%rbp), %rax
    addq -280(%rbp), %rax
    movq %rax, -288(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -208(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -128(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
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
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load compile-time constant TYPEFIELD_SIZE_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -128(%rbp), %rax
    addq -304(%rbp), %rax
    movq %rax, -128(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    jmp .L2381
.L2382:
    movq -128(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2362
.L2361:
.L2362:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEDEFINITION_NAME_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
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
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $126, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2521
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
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2531
    leaq .STR35(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2532
.L2531:
.L2532:
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -432(%rbp)
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
    movq %rax, -440(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    leaq .STR24(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -440(%rbp)
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2542
.L2541:
.L2542:
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2551
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -440(%rbp)
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2552
.L2551:
.L2552:
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2561
    leaq .STR37(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -440(%rbp)
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2562
.L2561:
.L2562:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -440(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2572
.L2571:
.L2572:
    movq -440(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2581
    leaq .STR38(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2582
.L2581:
.L2582:
    movq $3, %rax  # Load compile-time constant TYPE_KIND_ARRAY
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -440(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_ARRAY_ELEMENT_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -432(%rbp), %rax
    pushq %rax
    movq $28, %rax  # Load compile-time constant TYPEDEFINITION_DATA_ARRAY_LENGTH_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_ARRAY_ELEMENT_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -432(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -512(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    jmp .L2522
.L2521:
    leaq .STR39(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L2522:
    jmp .L2512
.L2511:
.L2512:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2591
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
    movq $2, %rax  # Load compile-time constant TYPE_KIND_FUNCTION
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $8, %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2601
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
    jmp .L2602
.L2601:
.L2602:
    movq -80(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2611
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2612
.L2611:
.L2612:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2621
    movq $2, %rax
    movq %rax, -576(%rbp)
    movq -576(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -584(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -592(%rbp)
.L2631:    movq -592(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2632
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
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
    jmp .L2642
.L2641:
.L2642:
    movq $0, %rax
    movq %rax, -600(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    leaq .STR24(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -600(%rbp)
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2652
.L2651:
.L2652:
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -600(%rbp)
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2662
.L2661:
.L2662:
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2671
    leaq .STR37(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -600(%rbp)
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2672
.L2671:
.L2672:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2681
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -600(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2682
.L2681:
.L2682:
    movq -600(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2691
    leaq .STR40(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2692
.L2691:
.L2692:
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq -576(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq -576(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -576(%rbp)
    movq -576(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -688(%rbp)
    movq -688(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -688(%rbp), %rax
    movq %rax, -584(%rbp)
    jmp .L2702
.L2701:
.L2702:
    movq -672(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -704(%rbp)
    movq -600(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -584(%rbp), %rax
    addq -704(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -672(%rbp), %rax
    addq $1, %rax
    movq %rax, -712(%rbp)
    movq -712(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
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
    jz .L2711
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2712
.L2711:
.L2712:
    movq -80(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2721
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2722
.L2721:
    movq $0, %rax
    movq %rax, -592(%rbp)
.L2722:
    jmp .L2631
.L2632:
    jmp .L2622
.L2621:
.L2622:
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2731
    leaq .STR24(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    jmp .L2732
.L2731:
.L2732:
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2741
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    jmp .L2742
.L2741:
.L2742:
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2751
    leaq .STR37(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    jmp .L2752
.L2751:
.L2752:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2761
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
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
    jmp .L2762
.L2761:
    leaq .STR41(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L2762:
    jmp .L2592
.L2591:
    movq $1, %rax  # Load compile-time constant TYPE_KIND_VARIANT
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
.L2771:    movq -80(%rbp), %rax
    pushq %rax
    movq $111, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2772
    movq $111, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2781
    leaq .STR42(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2782
.L2781:
.L2782:
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -848(%rbp)
    movq -848(%rbp), %rax
    addq $1, %rax
    movq %rax, -856(%rbp)
    movq -856(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -864(%rbp)
    movq -856(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -872(%rbp)
    movq -872(%rbp), %rax
    pushq %rax
    movq -864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -880(%rbp)
    movq -880(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -856(%rbp), %rax
    subq $1, %rax
    movq %rax, -888(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -880(%rbp), %rax
    addq -896(%rbp), %rax
    movq %rax, -904(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -920(%rbp)
    movq -920(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant VARIANT_NAME_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -856(%rbp), %rax
    subq $1, %rax
    movq %rax, -928(%rbp)
    movq -928(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load compile-time constant VARIANT_TAG_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2791
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -280(%rbp)
    movq $1, %rax
    movq %rax, -592(%rbp)
.L2801:    movq -592(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2802
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2811
    leaq .STR43(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2812
.L2811:
.L2812:
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -168(%rbp)
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
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2821
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2831
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2841
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2851
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2852
.L2851:
.L2852:
    jmp .L2842
.L2841:
.L2842:
    jmp .L2832
.L2831:
.L2832:
    jmp .L2822
.L2821:
.L2822:
    movq -48(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -208(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2861
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2862
.L2861:
.L2862:
    movq -80(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2871
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2872
.L2871:
.L2872:
    movq -80(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2881
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2882
.L2881:
.L2882:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2891
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2892
.L2891:
.L2892:
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1048(%rbp)
    movq -1048(%rbp), %rax
    addq $1, %rax
    movq %rax, -1056(%rbp)
    movq -1056(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1064(%rbp)
    movq -1056(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1072(%rbp)
    movq -1072(%rbp), %rax
    pushq %rax
    movq -1064(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -1080(%rbp)
    movq -1080(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1056(%rbp), %rax
    subq $1, %rax
    movq %rax, -1088(%rbp)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1096(%rbp)
    movq -1080(%rbp), %rax
    addq -1096(%rbp), %rax
    movq %rax, -288(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -208(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -280(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
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
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load compile-time constant TYPEFIELD_SIZE_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -280(%rbp), %rax
    addq -304(%rbp), %rax
    movq %rax, -280(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2901
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2902
.L2901:
    movq $0, %rax
    movq %rax, -592(%rbp)
.L2902:
    jmp .L2801
.L2802:
    jmp .L2792
.L2791:
.L2792:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    jmp .L2771
.L2772:
    movq $8, %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -848(%rbp)
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -864(%rbp)
    movq $0, %rax
    movq %rax, -1192(%rbp)
.L2911:    movq -1192(%rbp), %rax
    pushq %rax
    movq -848(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2912
    movq -1192(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -864(%rbp), %rax
    addq -896(%rbp), %rax
    movq %rax, -904(%rbp)
    movq $8, %rax
    movq %rax, -1216(%rbp)
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1048(%rbp)
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -904(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1064(%rbp)
    movq $0, %rax
    movq %rax, -1240(%rbp)
.L2921:    movq -1240(%rbp), %rax
    pushq %rax
    movq -1048(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2922
    movq -1240(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -280(%rbp)
    movq -1064(%rbp), %rax
    addq -280(%rbp), %rax
    movq %rax, -288(%rbp)
    movq $20, %rax  # Load compile-time constant TYPEFIELD_SIZE_OFFSET
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -304(%rbp)
    movq -1216(%rbp), %rax
    addq -304(%rbp), %rax
    movq %rax, -1216(%rbp)
    movq -1240(%rbp), %rax
    addq $1, %rax
    movq %rax, -1240(%rbp)
    jmp .L2921
.L2922:
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1288(%rbp)
    movq -1216(%rbp), %rax
    pushq %rax
    movq -1288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2931
    movq -1216(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L2932
.L2931:
.L2932:
    movq -1192(%rbp), %rax
    addq $1, %rax
    movq %rax, -1192(%rbp)
    jmp .L2911
.L2912:
.L2592:
    jmp .L2502
.L2501:
    leaq .STR44(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L2502:
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_function
parser_parse_function:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
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
    jz .L2941
    leaq .STR45(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $10, %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR46(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
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
    jmp .L2942
.L2941:
.L2942:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
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
    jz .L2951
    leaq .STR47(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2952
.L2951:
.L2952:
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
    leaq .STR24(%rip), %rax
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
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2961
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2971
    leaq .STR48(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
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
    jmp .L2972
.L2971:
.L2972:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -128(%rbp)
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
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2981
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2991
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3001
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3011
    leaq .STR40(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
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
    jmp .L3012
.L3011:
.L3012:
    jmp .L3002
.L3001:
.L3002:
    jmp .L2992
.L2991:
.L2992:
    jmp .L2982
.L2981:
.L2982:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -168(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3021
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3022
.L3021:
.L3022:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3031
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3032
.L3031:
.L3032:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3041
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3042
.L3041:
.L3042:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3051
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3052
.L3051:
.L3052:
    movq -168(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call function_add_parameter
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -184(%rbp)
.L3061:    movq -184(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3062
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3071
    leaq .STR49(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L3072
.L3071:
.L3072:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -128(%rbp)
    movq -200(%rbp), %rax
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
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
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
    jz .L3081
    movq -248(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3091
    movq -248(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3101
    movq -248(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3111
    leaq .STR40(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L3112
.L3111:
.L3112:
    jmp .L3102
.L3101:
.L3102:
    jmp .L3092
.L3091:
.L3092:
    jmp .L3082
.L3081:
.L3082:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -168(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3121
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3122
.L3121:
.L3122:
    movq -248(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3131
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3132
.L3131:
.L3132:
    movq -248(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3141
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3142
.L3141:
.L3142:
    movq -248(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3151
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3152
.L3151:
.L3152:
    movq -168(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call function_add_parameter
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -184(%rbp)
    jmp .L3061
.L3062:
    jmp .L2962
.L2961:
.L2962:
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -312(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3161
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L3162
.L3161:
.L3162:
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3171
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3181
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L3182
.L3181:
.L3182:
    jmp .L3172
.L3171:
.L3172:
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3191
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3201
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L3202
.L3201:
.L3202:
    jmp .L3192
.L3191:
.L3192:
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3211
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3221
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L3222
.L3221:
.L3222:
    jmp .L3212
.L3211:
.L3212:
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3231
    leaq .STR41(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
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
    jmp .L3232
.L3231:
.L3232:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -368(%rbp)
.L3241:    movq -368(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3242
    movq -368(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3251
    jmp .L3242
    jmp .L3252
.L3251:
.L3252:
    movq -368(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3261
    jmp .L3242
    jmp .L3262
.L3261:
.L3262:
    movq $0, %rax
    movq %rax, -376(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3272
.L3271:
.L3272:
    movq -368(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3281
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3282
.L3281:
.L3282:
    movq -368(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3291
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3292
.L3291:
.L3292:
    movq -368(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3301
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3302
.L3301:
.L3302:
    movq -368(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3311
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3312
.L3311:
.L3312:
    movq -368(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3321
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3322
.L3321:
.L3322:
    movq -368(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3331
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3332
.L3331:
.L3332:
    movq -368(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3341
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -384(%rbp)
    movq $0, %rax  # Load compile-time constant EXPRESSION_TYPE_OFFSET
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3351
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3352
.L3351:
    leaq .STR50(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR18(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L3352:
    jmp .L3342
.L3341:
.L3342:
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3361
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -384(%rbp)
    movq $0, %rax  # Load compile-time constant EXPRESSION_TYPE_OFFSET
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant EXPR_BUILTIN_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3371
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3372
.L3371:
    leaq .STR19(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L3372:
    jmp .L3362
.L3361:
.L3362:
    movq -376(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3381
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -440(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L3382
.L3381:
.L3382:
    movq -376(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_add_statement
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -368(%rbp)
    jmp .L3241
.L3242:
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3391
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    movq %rax, -480(%rbp)
    movq -480(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_add_statement
    jmp .L3392
.L3391:
.L3392:
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_create
parser_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $24, %rax  # Load compile-time constant SIZEOF_PARSER
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant PARSER_LEXER
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3401
    leaq .STR52(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L3402
.L3401:
.L3402:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_destroy
parser_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_program
parser_parse_program:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $64, %rax  # Load compile-time constant SIZEOF_PROGRAM
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
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
    jz .L3411
    leaq .STR53(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L3412
.L3411:
.L3412:
    movq $0, %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant PROGRAM_IMPORTS
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant PROGRAM_FUNCTIONS
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $48, %rax  # Load compile-time constant PROGRAM_GLOBAL_VARS
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant PROGRAM_FUNCTION_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant PROGRAM_IMPORT_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $56, %rax  # Load compile-time constant PROGRAM_GLOBAL_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $12, %rax  # Load compile-time constant PROGRAM_FUNCTION_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $28, %rax  # Load compile-time constant PROGRAM_TYPE_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $44, %rax  # Load compile-time constant PROGRAM_IMPORT_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $60, %rax  # Load compile-time constant PROGRAM_GLOBAL_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -40(%rbp)
.L3421:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3422
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
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
    jz .L3431
    leaq .STR54(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3432
.L3431:
.L3432:
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
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
    jz .L3441
    movq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L3442
.L3441:
.L3442:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3451
    movq $0, %rax
    movq %rax, -40(%rbp)
    jmp .L3452
.L3451:
.L3452:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3461
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $56, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3471
    movq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L3472
.L3471:
.L3472:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3481
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_import
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_import
    jmp .L3482
.L3481:
.L3482:
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3491
    movq $1, %rax
    movq %rax, -112(%rbp)
    jmp .L3492
.L3491:
.L3492:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3501
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_type_definition
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_type
    jmp .L3502
.L3501:
.L3502:
    movq $0, %rax
    movq %rax, -136(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3511
    movq $1, %rax
    movq %rax, -136(%rbp)
    jmp .L3512
.L3511:
.L3512:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3521
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_function
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3531
    leaq .STR55(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3532
.L3531:
.L3532:
    movq -152(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_function
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    jmp .L3522
.L3521:
.L3522:
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3541
    movq $1, %rax
    movq %rax, -176(%rbp)
    jmp .L3542
.L3541:
.L3542:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3551
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3561
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -208(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3571
    movq $13, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -232(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3581
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -264(%rbp)
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
    movq %rax, -272(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR24(%rip), %rax
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
    movq -264(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_global
    jmp .L3582
.L3581:
.L3582:
    jmp .L3572
.L3571:
.L3572:
    jmp .L3562
.L3561:
.L3562:
    jmp .L3552
.L3551:
.L3552:
    movq $0, %rax
    movq %rax, -280(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3591
    movq $1, %rax
    movq %rax, -280(%rbp)
    jmp .L3592
.L3591:
.L3592:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3601
    movq $1, %rax
    movq %rax, -280(%rbp)
    jmp .L3602
.L3601:
.L3602:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3611
    movq $1, %rax
    movq %rax, -280(%rbp)
    jmp .L3612
.L3611:
.L3612:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3621
    movq $1, %rax
    movq %rax, -280(%rbp)
    jmp .L3622
.L3621:
.L3622:
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3631
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3632
.L3631:
.L3632:
    jmp .L3462
.L3461:
.L3462:
    jmp .L3421
.L3422:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_destroy
expression_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3641
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3642
.L3641:
.L3642:
    movq $0, %rax  # Load compile-time constant EXPR_TYPE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load compile-time constant EXPR_BINARY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3651
    movq $8, %rax  # Load compile-time constant EXPR_BINARY_LEFT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax  # Load compile-time constant EXPR_BINARY_RIGHT
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
    jmp .L3652
.L3651:
.L3652:
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant EXPR_UNARY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3661
    movq $8, %rax  # Load compile-time constant EXPR_UNARY_OPERAND
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
    jmp .L3662
.L3661:
.L3662:
    movq -16(%rbp), %rax
    pushq %rax
    movq $4, %rax  # Load compile-time constant EXPR_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3671
    movq $8, %rax  # Load compile-time constant EXPR_CALL_NAME
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
    jmp .L3672
.L3671:
.L3672:
    movq -16(%rbp), %rax
    pushq %rax
    movq $6, %rax  # Load compile-time constant EXPR_FIELD_ACCESS
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3681
    movq $8, %rax  # Load compile-time constant EXPR_FIELD_OBJECT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $16, %rax  # Load compile-time constant EXPR_FIELD_NAME
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
    jmp .L3682
.L3681:
.L3682:
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant EXPR_ARRAY_ACCESS
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3691
    movq $8, %rax  # Load compile-time constant EXPR_ARRAY_OBJECT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $16, %rax  # Load compile-time constant EXPR_ARRAY_INDEX_OFFSET
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
    jmp .L3692
.L3691:
.L3692:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant EXPR_IDENTIFIER
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3701
    movq $8, %rax  # Load compile-time constant EXPR_IDENTIFIER_NAME
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
    jmp .L3702
.L3701:
.L3702:
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax  # Load compile-time constant EXPR_STRING_LITERAL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3711
    movq $8, %rax  # Load compile-time constant EXPR_STRING_VALUE
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
    jmp .L3712
.L3711:
.L3712:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl statement_destroy
statement_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3721
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3722
.L3721:
.L3722:
    movq $0, %rax  # Load compile-time constant STMT_TYPE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant STMT_LET
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3731
    movq $8, %rax  # Load compile-time constant STMT_LET_NAME
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax  # Load compile-time constant STMT_LET_VALUE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $24, %rax  # Load compile-time constant STMT_LET_TYPE
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
    jmp .L3732
.L3731:
.L3732:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load compile-time constant STMT_SET
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3741
    movq $8, %rax  # Load compile-time constant STMT_SET_NAME
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $16, %rax  # Load compile-time constant STMT_SET_VALUE
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
    jmp .L3742
.L3741:
.L3742:
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax  # Load compile-time constant STMT_IF
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3751
    movq $8, %rax  # Load compile-time constant STMT_IF_CONDITION
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
    jmp .L3752
.L3751:
.L3752:
    movq -16(%rbp), %rax
    pushq %rax
    movq $6, %rax  # Load compile-time constant STMT_WHILE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3761
    movq $8, %rax  # Load compile-time constant STMT_WHILE_CONDITION
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
    jmp .L3762
.L3761:
.L3762:
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant STMT_FOR
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3771
    movq $8, %rax  # Load compile-time constant STMT_FOR_VAR
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $16, %rax  # Load compile-time constant STMT_FOR_START
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $24, %rax  # Load compile-time constant STMT_FOR_END
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
    jmp .L3772
.L3771:
.L3772:
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax  # Load compile-time constant STMT_RETURN
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3781
    movq $8, %rax  # Load compile-time constant STMT_RETURN_VALUE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L3782
.L3781:
.L3782:
    movq -16(%rbp), %rax
    pushq %rax
    movq $7, %rax  # Load compile-time constant STMT_EXPRESSION
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3791
    movq $8, %rax  # Load compile-time constant STMT_EXPR_VALUE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_destroy
    jmp .L3792
.L3791:
.L3792:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax  # Load compile-time constant STMT_BREAK
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3801
    jmp .L3802
.L3801:
.L3802:
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax  # Load compile-time constant STMT_CONTINUE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3811
    jmp .L3812
.L3811:
.L3812:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_destroy
function_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3821
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3822
.L3821:
.L3822:
    movq $0, %rax  # Load compile-time constant FUNCTION_NAME
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl type_destroy
type_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3831
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3832
.L3831:
.L3832:
    movq $0, %rax  # Load compile-time constant TYPE_KIND
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPE_PRIMITIVE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3841
    jmp .L3842
.L3841:
.L3842:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant TYPE_STRUCT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3851
    movq $8, %rax  # Load compile-time constant TYPE_STRUCT_NAME
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
    jmp .L3852
.L3851:
.L3852:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load compile-time constant TYPE_ARRAY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3861
    movq $8, %rax  # Load compile-time constant TYPE_ARRAY_ELEMENT_TYPE
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
    jmp .L3862
.L3861:
.L3862:
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax  # Load compile-time constant TYPE_POINTER
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3871
    movq $8, %rax  # Load compile-time constant TYPE_POINTER_TARGET_TYPE
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
    jmp .L3872
.L3871:
.L3872:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl program_destroy
program_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3881
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3882
.L3881:
.L3882:
    movq $8, %rax  # Load compile-time constant PROGRAM_FUNCTION_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant PROGRAM_FUNCTIONS
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
    jz .L3891
    movq $0, %rax
    movq %rax, -32(%rbp)
.L3901:    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3902
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
    jz .L3911
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call function_destroy
    jmp .L3912
.L3911:
.L3912:
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3901
.L3902:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3892
.L3891:
.L3892:
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
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
    jz .L3921
    movq $0, %rax
    movq %rax, -88(%rbp)
.L3931:    movq -88(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3932
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -80(%rbp), %rax
    addq -48(%rbp), %rax
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
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
    jz .L3941
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L3942
.L3941:
.L3942:
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3931
.L3932:
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3922
.L3921:
.L3922:
    movq $40, %rax  # Load compile-time constant PROGRAM_IMPORT_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -128(%rbp)
    movq $32, %rax  # Load compile-time constant PROGRAM_IMPORTS
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
    jz .L3951
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3952
.L3951:
.L3952:
    movq $56, %rax  # Load compile-time constant PROGRAM_GLOBAL_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -144(%rbp)
    movq $48, %rax  # Load compile-time constant PROGRAM_GLOBAL_VARS
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3961
    movq $0, %rax
    movq %rax, -160(%rbp)
.L3971:    movq -160(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3972
    movq $8, %rax
    movq %rax, -40(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -152(%rbp), %rax
    addq -48(%rbp), %rax
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3981
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_destroy
    jmp .L3982
.L3981:
.L3982:
    movq -160(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3971
.L3972:
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3962
.L3961:
.L3962:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_destroy
string_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3991
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3992
.L3991:
.L3992:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl param_destroy
param_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4001
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4002
.L4001:
.L4002:
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl field_destroy
field_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4011
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4012
.L4011:
.L4012:
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl import_destroy
import_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4021
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4022
.L4021:
.L4022:
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_import
parser_parse_import:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
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
    jz .L4031
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4032
.L4031:
.L4032:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
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
    movq $10, %rax
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
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4041
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4042
.L4041:
.L4042:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -56(%rbp)
    movq $53, %rax
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
    movq %rax, -64(%rbp)
    movq -32(%rbp), %rax
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
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
