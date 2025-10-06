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
.globl STMT_FOR_EACH
STMT_FOR_EACH:    .quad 12
.globl STMT_INLINE_ASSEMBLY
STMT_INLINE_ASSEMBLY:    .quad 16
.globl STMT_COMPOUND_ASSIGN
STMT_COMPOUND_ASSIGN:    .quad 17
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
.STR0:    .string "[PARSER ERROR] Expected field name after '.' at line "
.STR1:    .string "[PARSER ERROR] Expected 'index' after 'at' at line "
.STR2:    .string "[PARSER ERROR] Expected 'than' after 'less' at line "
.STR3:    .string "[PARSER ERROR] Expected 'than' after 'greater' at line "
.STR4:    .string "[PARSER ERROR] Expected 'equal', 'less', or 'greater' after 'is' at line "
.STR5:    .string "[PARSER ERROR] NULL parser in parser_parse_let_statement"
.STR6:    .string "[PARSER ERROR] Expected identifier after Let at line "
.STR7:    .string "[PARSER ERROR] parser became NULL before expression parsing in Let"
.STR8:    .string "Parser error: Expected operation after gets (got token "
.STR9:    .string ")"
.STR10:    .string "[PARSER ERROR] Expected token type "
.STR11:    .string ", got "
.STR12:    .string " at line "
.STR13:    .string "[PARSER ERROR] Null parser in parse_primary"
.STR14:    .string "[PARSER ERROR] Null current_token in parse_primary"
.STR15:    .string "[PARSER ERROR] Expected function name after $ at line "
.STR16:    .string "[PARSER ERROR] Expected field name after 'the' at line "
.STR17:    .string "[PARSER ERROR] Expected 'of' after field name at line "
.STR18:    .string "a"
.STR19:    .string "an"
.STR20:    .string "list"
.STR21:    .string "[PARSER ERROR] Expected 'containing' after 'a list' at line "
.STR22:    .string "set"
.STR23:    .string "[PARSER ERROR] Expected 'containing' after 'a set' at line "
.STR24:    .string "[PARSER ERROR] Expected 'with' after struct type name at line "
.STR25:    .string "[PARSER ERROR] Expected field name at line "
.STR26:    .string "Array"
.STR27:    .string "[PARSER ERROR] Expected 'of' after 'an Array' at line "
.STR28:    .string "[PARSER ERROR] Expected integer size after 'an Array of' at line "
.STR29:    .string "[PARSER ERROR] Expected type name after array size at line "
.STR30:    .string "[PARSER ERROR] Array size mismatch: declared "
.STR31:    .string " but got "
.STR32:    .string " elements"
.STR33:    .string "dictionary"
.STR34:    .string "[PARSER ERROR] Expected ':' after 'dictionary with' at line "
.STR35:    .string "[PARSER ERROR] Expected 'as' in dictionary literal at line "
.STR36:    .string "[PARSER ERROR] Expected variant name after 'as'"
.STR37:    .string "[PARSER ERROR] Expected ',' or ')' in function arguments at line "
.STR38:    .string "[PARSER ERROR] Expected integer after 'negative' at line "
.STR39:    .string "[PARSER ERROR] Expected integer or identifier at line "
.STR40:    .string "[PARSER ERROR] Display/Print is a statement and should not use parentheses. Use 'Display expression' not 'Display(expression)' at line "
.STR41:    .string "[PARSER ERROR] Only function calls can be used as statements (expr_type="
.STR42:    .string ", expected "
.STR43:    .string ") at line "
.STR44:    .string "[PARSER ERROR] Invalid builtin function statement at line "
.STR45:    .string "[PARSER ERROR] Inline assembly block too large (max 8192 bytes)\n"
.STR46:    .string "End"
.STR47:    .string "Assembly"
.STR48:    .string "[PARSER ERROR] Expected variant name after 'When' at line "
.STR49:    .string "[PARSER ERROR] Expected field name in match case at line "
.STR50:    .string "[PARSER ERROR] Expected binding variable name at line "
.STR51:    .string "Integer"
.STR52:    .string "Byte"
.STR53:    .string "Short"
.STR54:    .string "Long"
.STR55:    .string "[PARSER WARNING] Unknown type '"
.STR56:    .string "', defaulting to 8 bytes"
.STR57:    .string "[PARSER ERROR] Expected type name at line "
.STR58:    .string " (got token type "
.STR59:    .string "[PARSER ERROR] Expected field type at line "
.STR60:    .string "[PARSER ERROR] Expected array size at line "
.STR61:    .string "String"
.STR62:    .string "Character"
.STR63:    .string "[PARSER ERROR] Expected element type at line "
.STR64:    .string "[PARSER ERROR] Expected parameter type at line "
.STR65:    .string "[PARSER ERROR] Expected return type at line "
.STR66:    .string "[PARSER ERROR] Expected variant name at line "
.STR67:    .string "[PARSER ERROR] Expected field name in variant at line "
.STR68:    .string "[PARSER ERROR] Expected 'called' or type name after 'Type' at line "
.STR69:    .string "[PARSER ERROR] Expected function name string literal (type "
.STR70:    .string "), got type "
.STR71:    .string "[PARSER ERROR] Function name is NULL!"
.STR72:    .string "[PARSER ERROR] Expected parameter name at line "
.STR73:    .string "[PARSER ERROR] Expected parameter name after comma at line "
.STR74:    .string "[PARSER ERROR] Only function calls can be used as statements (got expr_type="
.STR75:    .string "[PARSER ERROR] Unexpected token "
.STR76:    .string " in function body at line "
.STR77:    .string "[ERROR] lexer_next_token returned NULL!"
.STR78:    .string "[ERROR] First token is already EOF!"
.STR79:    .string "[ERROR] current_token is NULL!"
.STR80:    .string "[ERROR] parser_parse_import returned NULL!"
.STR81:    .string "[ERROR] parser_parse_function returned NULL!"
.STR82:    .string "[PARSER ERROR] Expected string literal after Import, got token type "
.STR83:    .string ", value: "
.STR84:    .string "[PARSER ERROR] Expected 'as' after filename, got token type "
.STR85:    .string "[PARSER ERROR] Expected module name after 'as', got token type "
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
    movq $132, %rax
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
    movq $124, %rax
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
    movq $129, %rax
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
    movq $126, %rax
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
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_logical_and
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L171:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L172
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
    jz .L181
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
    jmp .L182
.L181:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L182:
    jmp .L171
.L172:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_logical_and
parser_parse_logical_and:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_comparison_level
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L191:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L192
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
    jz .L201
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
    jmp .L202
.L201:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L202:
    jmp .L191
.L192:
    movq -16(%rbp), %rax
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
.L211:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L212
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
    jz .L221
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
    jmp .L222
.L221:
    movq -40(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L231
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
    jmp .L232
.L231:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L232:
.L222:
    jmp .L211
.L212:
    movq -16(%rbp), %rax
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
.L241:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L242
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
    jz .L251
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
    jmp .L252
.L251:
    movq -40(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
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
    jmp .L262
.L261:
    movq -40(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
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
    jmp .L272
.L271:
    movq -40(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L282
.L281:
    movq -40(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L292
.L291:
    movq -40(%rbp), %rax
    pushq %rax
    movq $39, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L302
.L301:
    movq -40(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L312
.L311:
    movq -40(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
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
    jmp .L322
.L321:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L322:
.L312:
.L302:
.L292:
.L282:
.L272:
.L262:
.L252:
    jmp .L241
.L242:
    movq -16(%rbp), %rax
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
    jz .L331
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
    jz .L341
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
.L351:    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L352
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
    jz .L361
    movq $0, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L362
.L361:
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
    jz .L371
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L372
.L371:
.L372:
.L362:
    jmp .L351
.L352:
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
    jmp .L342
.L341:
.L342:
    jmp .L332
.L331:
.L332:
    movq $1, %rax
    movq %rax, -168(%rbp)
.L381:    movq -168(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L382
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
    jz .L391
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
    jz .L401
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
    jmp .L402
.L401:
.L402:
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
    jmp .L392
.L391:
.L392:
    movq -184(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    movq $148, %rax
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
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -184(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    movq $149, %rax
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
    jmp .L422
.L421:
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L422:
    jmp .L412
.L411:
.L412:
    movq -184(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L431
    movq -184(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    movq $0, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L442
.L441:
.L442:
    jmp .L432
.L431:
.L432:
    jmp .L381
.L382:
    movq -16(%rbp), %rax
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
    jz .L451
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
    jz .L461
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
    jmp .L462
.L461:
.L462:
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
    jz .L471
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
    jz .L481
    movq $23, %rax
    movq %rax, -64(%rbp)
    jmp .L482
.L481:
    movq $22, %rax
    movq %rax, -64(%rbp)
.L482:
    jmp .L472
.L471:
.L472:
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L491
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
    jz .L501
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
    jz .L511
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
    jz .L521
    movq $25, %rax
    movq %rax, -64(%rbp)
    jmp .L522
.L521:
    movq $27, %rax
    movq %rax, -64(%rbp)
.L522:
    jmp .L512
.L511:
.L512:
    movq -112(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L541
    movq $26, %rax
    movq %rax, -64(%rbp)
    jmp .L542
.L541:
    movq $24, %rax
    movq %rax, -64(%rbp)
.L542:
    jmp .L532
.L531:
.L532:
    jmp .L502
.L501:
.L502:
    movq -96(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L551
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
    jmp .L552
.L551:
.L552:
    jmp .L492
.L491:
.L492:
    movq -48(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L561
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
    jz .L571
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
    jz .L581
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
    jz .L591
    movq $24, %rax
    movq %rax, -64(%rbp)
    jmp .L592
.L591:
    movq $26, %rax
    movq %rax, -64(%rbp)
.L592:
    jmp .L582
.L581:
.L582:
    movq -112(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L601
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L611
    movq $27, %rax
    movq %rax, -64(%rbp)
    jmp .L612
.L611:
    movq $25, %rax
    movq %rax, -64(%rbp)
.L612:
    jmp .L602
.L601:
.L602:
    jmp .L572
.L571:
.L572:
    movq -96(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L621
    leaq .STR3(%rip), %rax
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
    jmp .L622
.L621:
.L622:
    jmp .L562
.L561:
.L562:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    leaq .STR4(%rip), %rax
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
    jmp .L632
.L631:
.L632:
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
    jmp .L452
.L451:
.L452:
    movq -16(%rbp), %rax
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
    jz .L641
    leaq .STR5(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L642
.L641:
.L642:
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
    jz .L651
    leaq .STR6(%rip), %rax
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
    jmp .L652
.L651:
.L652:
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
    jz .L661
    leaq .STR7(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L662
.L661:
.L662:
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


.globl parser_parse_implicit_compound_assign
parser_parse_implicit_compound_assign:
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
    jz .L671
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
    jz .L681
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
    jmp .L682
.L681:
.L682:
    movq -32(%rbp), %rax
    pushq %rax
    movq $138, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L691
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
    jmp .L692
.L691:
.L692:
    movq -32(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L701
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
    jmp .L702
.L701:
.L702:
    movq -32(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
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
    jmp .L712
.L711:
.L712:
    movq -32(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
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
    jmp .L722
.L721:
.L722:
    movq -32(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L731
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
    jmp .L732
.L731:
.L732:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L741
    movq -32(%rbp), %rax
    pushq %rax
    movq $137, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    leaq .STR8(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L752
.L751:
.L752:
    jmp .L742
.L741:
.L742:
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
    jmp .L672
.L671:
.L672:
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
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_create_set
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
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
    jz .L761
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L762
.L761:
.L762:
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
    jz .L771
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -40(%rbp)
    jmp .L772
.L771:
    leaq .STR10(%rip), %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR11(%rip), %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR12(%rip), %rax
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
.L772:
    movq $0, %rax
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
    jz .L781
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L782
.L781:
    movq -8(%rbp), %rax
    pushq %rax
    movq $55, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $57, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $58, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $59, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $60, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $61, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $62, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $63, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $64, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $65, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $66, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $67, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $68, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $69, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $70, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $71, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $72, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $73, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $74, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $75, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $76, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $77, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $78, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $79, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $80, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $81, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $82, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $83, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $84, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $85, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $86, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $87, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $88, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $89, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $90, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $91, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $92, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $93, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $94, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1171
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1172
.L1171:
    movq -8(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1181
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1182
.L1181:
    movq -8(%rbp), %rax
    pushq %rax
    movq $96, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1191
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1192
.L1191:
    movq -8(%rbp), %rax
    pushq %rax
    movq $97, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1202
.L1201:
    movq -8(%rbp), %rax
    pushq %rax
    movq $98, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1211
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1212
.L1211:
    movq -8(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1222
.L1221:
    movq -8(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1231
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1232
.L1231:
    movq -8(%rbp), %rax
    pushq %rax
    movq $101, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1242
.L1241:
    movq -8(%rbp), %rax
    pushq %rax
    movq $102, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1251
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1252
.L1251:
    movq -8(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1261
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1262
.L1261:
    movq -8(%rbp), %rax
    pushq %rax
    movq $104, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1271
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1272
.L1271:
    movq -8(%rbp), %rax
    pushq %rax
    movq $105, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1281
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1282
.L1281:
    movq -8(%rbp), %rax
    pushq %rax
    movq $106, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1291
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1292
.L1291:
    movq -8(%rbp), %rax
    pushq %rax
    movq $107, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1302
.L1301:
    movq -8(%rbp), %rax
    pushq %rax
    movq $108, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1312
.L1311:
    movq -8(%rbp), %rax
    pushq %rax
    movq $109, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1322
.L1321:
    movq -8(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1332
.L1331:
    movq -8(%rbp), %rax
    pushq %rax
    movq $115, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1342
.L1341:
    movq -8(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1351
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1352
.L1351:
    movq -8(%rbp), %rax
    pushq %rax
    movq $117, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1361
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1362
.L1361:
    movq -8(%rbp), %rax
    pushq %rax
    movq $118, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1371
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1372
.L1371:
    movq -8(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1381
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1382
.L1381:
    movq -8(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1391
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1392
.L1391:
    movq -8(%rbp), %rax
    pushq %rax
    movq $130, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1401
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1402
.L1401:
    movq -8(%rbp), %rax
    pushq %rax
    movq $131, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1411
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1412
.L1411:
.L1412:
.L1402:
.L1392:
.L1382:
.L1372:
.L1362:
.L1352:
.L1342:
.L1332:
.L1322:
.L1312:
.L1302:
.L1292:
.L1282:
.L1272:
.L1262:
.L1252:
.L1242:
.L1232:
.L1222:
.L1212:
.L1202:
.L1192:
.L1182:
.L1172:
.L1162:
.L1152:
.L1142:
.L1132:
.L1122:
.L1112:
.L1102:
.L1092:
.L1082:
.L1072:
.L1062:
.L1052:
.L1042:
.L1032:
.L1022:
.L1012:
.L1002:
.L992:
.L982:
.L972:
.L962:
.L952:
.L942:
.L932:
.L922:
.L912:
.L902:
.L892:
.L882:
.L872:
.L862:
.L852:
.L842:
.L832:
.L822:
.L812:
.L802:
.L792:
.L782:
    movq $0, %rax
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


.globl expression_create_unary_op
expression_create_unary_op:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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


.globl statement_create_compound_assign
statement_create_compound_assign:
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
    movq $17, %rax  # Load compile-time constant STMT_COMPOUND_ASSIGN
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
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $11, %rax  # Load compile-time constant STMT_FOR
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
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    movq $12, %rax  # Load compile-time constant STMT_FOR_EACH
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
    jz .L1421
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1431
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1432
.L1431:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1432:
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
    jmp .L1422
.L1421:
.L1422:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -56(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -16(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
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
    jz .L1441
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1451
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1452
.L1451:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1452:
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
    jmp .L1442
.L1441:
.L1442:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -56(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -16(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
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
    jz .L1461
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1471
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1472
.L1471:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1472:
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
    jmp .L1462
.L1461:
.L1462:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -56(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -16(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
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
    jz .L1481
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1491
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1492
.L1491:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1492:
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
    jmp .L1482
.L1481:
.L1482:
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -56(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -16(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
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
    jz .L1501
    leaq .STR13(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1502
.L1501:
.L1502:
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
    jz .L1511
    leaq .STR14(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1512
.L1511:
.L1512:
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
    jz .L1521
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
    jz .L1531
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
.L1541:    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1542
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
    jz .L1551
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -144(%rbp)
    jmp .L1552
.L1551:
.L1552:
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
    jz .L1561
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
    jmp .L1562
.L1561:
.L1562:
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
    jz .L1571
    movq $0, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1572
.L1571:
.L1572:
    jmp .L1541
.L1542:
    jmp .L1532
.L1531:
.L1532:
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
    jmp .L1522
.L1521:
.L1522:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1581
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
    jmp .L1582
.L1581:
.L1582:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1591
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
    movq $16, %rax  # Load compile-time constant PARSER_CURRENT_PROGRAM_OFFSET
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
    jz .L1601
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
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
.L1611:    movq -304(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1612
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
    jz .L1621
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
    jmp .L1622
.L1621:
    movq -304(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1622:
    jmp .L1611
.L1612:
    jmp .L1602
.L1601:
.L1602:
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
    jz .L1631
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
    jmp .L1632
.L1631:
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_string_literal_owned
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1632:
    jmp .L1592
.L1591:
.L1592:
    movq -24(%rbp), %rax
    pushq %rax
    movq $157, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1641
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
    jz .L1651
    leaq .STR15(%rip), %rax
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
    jmp .L1652
.L1651:
.L1652:
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
    jmp .L1642
.L1641:
.L1642:
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1661
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
    jmp .L1662
.L1661:
.L1662:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1671
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
    movq -472(%rbp), %rax
    pushq %rax
    movq $17, %rax
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
    jmp .L1672
.L1671:
.L1672:
    movq -24(%rbp), %rax
    pushq %rax
    movq $158, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1681
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
    jz .L1691
    leaq .STR16(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1692
.L1691:
.L1692:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -512(%rbp)
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
    jz .L1701
    leaq .STR17(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1702
.L1701:
.L1702:
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
    movq %rax, -528(%rbp)
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -536(%rbp)
    movq $6, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -528(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -512(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -536(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1682
.L1681:
.L1682:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1711
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    leaq .STR18(%rip), %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -552(%rbp)
    leaq .STR19(%rip), %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -560(%rbp)
    movq -552(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1721
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -568(%rbp)
    movq $0, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -576(%rbp)
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
    jz .L1731
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -584(%rbp)
    leaq .STR20(%rip), %rax
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -592(%rbp)
    movq -592(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1741
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
    jz .L1751
    leaq .STR21(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1752
.L1751:
.L1752:
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -616(%rbp)
    movq $4, %rax
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
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -656(%rbp)
.L1761:    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1762
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
    jz .L1771
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
    jz .L1781
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1782
.L1781:
.L1782:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -664(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1791
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
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1792
.L1791:
.L1792:
    movq -616(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -608(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -688(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1772
.L1771:
    movq $0, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1772:
    jmp .L1761
.L1762:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -696(%rbp)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -696(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1742
.L1741:
    leaq .STR22(%rip), %rax
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -704(%rbp)
    movq -704(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1801
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
    jz .L1811
    leaq .STR23(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1812
.L1811:
.L1812:
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -616(%rbp)
    movq $4, %rax
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
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -656(%rbp)
.L1821:    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1822
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
    jz .L1831
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
    jz .L1841
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1842
.L1841:
.L1842:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -664(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1851
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
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1852
.L1851:
.L1852:
    movq -616(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -608(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -688(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1832
.L1831:
    movq $0, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1832:
    jmp .L1821
.L1822:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -808(%rbp)
    movq $21, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -808(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1802
.L1801:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq $0, %rax
    movq %rax, -824(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1861
    movq $24, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -288(%rbp)
    movq $16, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -848(%rbp)
.L1871:    movq -848(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1872
    movq -848(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -856(%rbp)
    movq -856(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq $0, %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq -344(%rbp), %rax
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
    jz .L1881
    movq $1, %rax
    movq %rax, -824(%rbp)
    movq -288(%rbp), %rax
    movq %rax, -848(%rbp)
    jmp .L1882
.L1881:
.L1882:
    movq -848(%rbp), %rax
    addq $1, %rax
    movq %rax, -848(%rbp)
    jmp .L1871
.L1872:
    jmp .L1862
.L1861:
.L1862:
    movq -824(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1891
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -904(%rbp)
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
    jz .L1901
    leaq .STR24(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1902
.L1901:
.L1902:
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -920(%rbp)
    movq $0, %rax
    movq %rax, -928(%rbp)
    movq $0, %rax
    movq %rax, -936(%rbp)
    movq $4, %rax
    movq %rax, -944(%rbp)
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -944(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -960(%rbp)
    movq -960(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -920(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -960(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -928(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -968(%rbp)
.L1911:    movq -968(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1912
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
    jz .L1921
    leaq .STR25(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1922
.L1921:
.L1922:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -984(%rbp)
    movq -984(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -512(%rbp)
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
    movq %rax, -1000(%rbp)
    movq -936(%rbp), %rax
    pushq %rax
    movq -944(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1931
    movq -944(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -944(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -944(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1008(%rbp)
    movq -1008(%rbp), %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -920(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1008(%rbp), %rax
    pushq %rax
    movq -928(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -928(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1932
.L1931:
.L1932:
    movq -936(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1016(%rbp)
    movq -920(%rbp), %rax
    addq -1016(%rbp), %rax
    movq %rax, -1024(%rbp)
    movq -928(%rbp), %rax
    addq -1016(%rbp), %rax
    movq %rax, -1032(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1024(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1000(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1032(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -936(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -936(%rbp), %rbx
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
    jz .L1941
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1942
.L1941:
    movq $0, %rax
    pushq %rax
    leaq -968(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1942:
    jmp .L1911
.L1912:
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1040(%rbp)
    movq $20, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -904(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -920(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -928(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -936(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -1040(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1040(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1892
.L1891:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1048(%rbp)
    movq $97, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1056(%rbp)
    movq -1056(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1892:
.L1802:
.L1742:
    jmp .L1732
.L1731:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1064(%rbp)
    movq $97, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1064(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -1064(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -1064(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1072(%rbp)
    movq -1072(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1732:
    jmp .L1722
.L1721:
.L1722:
    movq -560(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1951
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
    jz .L1961
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -584(%rbp)
    leaq .STR26(%rip), %rax
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1088(%rbp)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1971
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
    jz .L1981
    leaq .STR27(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1982
.L1981:
.L1982:
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
    jz .L1991
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1992
.L1991:
.L1992:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1112(%rbp)
    movq -1112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -1120(%rbp)
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
    jz .L2001
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2002
.L2001:
.L2002:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1136(%rbp)
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1144(%rbp)
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
    jz .L2011
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -616(%rbp)
    movq $4, %rax
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
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -656(%rbp)
.L2021:    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2022
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
    jz .L2031
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
    jz .L2041
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2042
.L2041:
.L2042:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -664(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2051
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
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2052
.L2051:
.L2052:
    movq -616(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -608(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -688(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2032
.L2031:
    movq $0, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2032:
    jmp .L2021
.L2022:
    movq -616(%rbp), %rax
    pushq %rax
    movq -1120(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR31(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR32(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2062
.L2061:
.L2062:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1240(%rbp)
    movq $18, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1120(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1144(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1240(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2012
.L2011:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1248(%rbp)
    movq $19, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1120(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1144(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1248(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L2012:
    jmp .L1972
.L1971:
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1256(%rbp)
    movq -1256(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1264(%rbp)
    movq -1264(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1972:
    jmp .L1962
.L1961:
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1272(%rbp)
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1280(%rbp)
    movq -1280(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1962:
    jmp .L1952
.L1951:
.L1952:
    jmp .L1712
.L1711:
.L1712:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -1288(%rbp)
    movq -1288(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2071
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
    movq %rax, -1304(%rbp)
    leaq .STR20(%rip), %rax
    pushq %rax
    movq -1304(%rbp), %rax
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
    jz .L2081
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
    movq %rax, -1320(%rbp)
    movq -1320(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2091
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -616(%rbp)
    movq $4, %rax
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
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -656(%rbp)
.L2101:    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2102
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
    jz .L2111
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
    jz .L2121
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2122
.L2121:
.L2122:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -664(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2131
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
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2132
.L2131:
.L2132:
    movq -616(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -608(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -688(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2112
.L2111:
    movq $0, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2112:
    jmp .L2101
.L2102:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -696(%rbp)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -696(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2092
.L2091:
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1056(%rbp)
    movq -1056(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L2092:
    jmp .L2082
.L2081:
.L2082:
    leaq .STR22(%rip), %rax
    pushq %rax
    movq -1304(%rbp), %rax
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
    jz .L2141
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
    movq %rax, -1320(%rbp)
    movq -1320(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2151
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -616(%rbp)
    movq $4, %rax
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
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -656(%rbp)
.L2161:    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2162
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
    jz .L2171
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
    jz .L2181
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2182
.L2181:
.L2182:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -664(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2191
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
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2192
.L2191:
.L2192:
    movq -616(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -608(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -688(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2172
.L2171:
    movq $0, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2172:
    jmp .L2161
.L2162:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -808(%rbp)
    movq $21, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -616(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -808(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2152
.L2151:
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1056(%rbp)
    movq -1056(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L2152:
    jmp .L2142
.L2141:
.L2142:
    leaq .STR33(%rip), %rax
    pushq %rax
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1552(%rbp)
    movq -1552(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2201
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
    movq %rax, -1320(%rbp)
    movq -1320(%rbp), %rax
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
    jz .L2221
    leaq .STR34(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2222
.L2221:
.L2222:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1576(%rbp)
    movq $0, %rax
    movq %rax, -1584(%rbp)
    movq $0, %rax
    movq %rax, -1592(%rbp)
    movq $4, %rax
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
    leaq -1576(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1624(%rbp)
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
    jz .L2231
    leaq .STR35(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2232
.L2231:
.L2232:
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
    movq %rax, -1640(%rbp)
    movq -1624(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1576(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1640(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1592(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -656(%rbp)
.L2241:    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2242
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
    jz .L2251
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
    movq %rax, -1656(%rbp)
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
    jz .L2261
    leaq .STR35(%rip), %rax
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
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L2262
.L2261:
.L2262:
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
    movq %rax, -1672(%rbp)
    movq -1592(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2271
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
    movq -1576(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1576(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -160(%rbp), %rax
    pushq %rax
    movq -1584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2272
.L2271:
.L2272:
    movq -1592(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -1576(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -1696(%rbp)
    movq -1584(%rbp), %rax
    addq -168(%rbp), %rax
    movq %rax, -1032(%rbp)
    movq -1656(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1672(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1032(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1592(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1592(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2252
.L2251:
    movq $0, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2252:
    jmp .L2241
.L2242:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1712(%rbp)
    movq $22, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1576(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1584(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1592(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1712(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2212
.L2211:
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1056(%rbp)
    movq -1056(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L2212:
    jmp .L2202
.L2201:
.L2202:
    movq $0, %rax
    movq %rax, -272(%rbp)
    movq $16, %rax  # Load compile-time constant PARSER_CURRENT_PROGRAM_OFFSET
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
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2281
    jmp .L2282
.L2281:
.L2282:
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2291
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2301
    jmp .L2302
.L2301:
.L2302:
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2311
    jmp .L2312
.L2311:
.L2312:
    movq $0, %rax
    movq %rax, -304(%rbp)
    movq $1, %rax
    movq %rax, -1768(%rbp)
.L2321:    movq -1768(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2322
    movq $0, %rax
    movq %rax, -1776(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2331
    movq $1, %rax
    movq %rax, -1776(%rbp)
    jmp .L2332
.L2331:
.L2332:
    movq -1776(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2341
    movq $0, %rax
    movq %rax, -1768(%rbp)
    jmp .L2342
.L2341:
.L2342:
    movq -1776(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2351
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
    movq -1304(%rbp), %rax
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
    jz .L2361
    movq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1768(%rbp)
    jmp .L2362
.L2361:
.L2362:
    movq -304(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2352
.L2351:
.L2352:
    jmp .L2321
.L2322:
    jmp .L2292
.L2291:
.L2292:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1856(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1864(%rbp)
    movq -1864(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2371
    movq $0, %rax
    pushq %rax
    movq -1864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1872(%rbp)
    movq -1872(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2381
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
    movq %rax, -1880(%rbp)
    movq -1880(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2391
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2392
.L2391:
.L2392:
    movq $0, %rax
    pushq %rax
    movq -1880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1888(%rbp)
    movq -1888(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2401
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2402
.L2401:
.L2402:
    movq $8, %rax
    pushq %rax
    movq -1880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1896(%rbp)
    movq $53, %rax
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
    movq -1304(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1896(%rbp), %rax
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
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1920(%rbp)
    movq -1920(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2411
    movq $0, %rax
    pushq %rax
    movq -1920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1928(%rbp)
    movq -1928(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2421
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2422
.L2421:
.L2422:
    jmp .L2412
.L2411:
.L2412:
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2382
.L2381:
.L2382:
    jmp .L2372
.L2371:
.L2372:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1936(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1936(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1944(%rbp)
    movq -1304(%rbp), %rax
    movq %rax, -1952(%rbp)
    movq $0, %rax
    movq %rax, -1960(%rbp)
    movq $1, %rax
    movq %rax, -1968(%rbp)
    movq -1944(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2431
    movq $0, %rax
    pushq %rax
    leaq -1968(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2432
.L2431:
.L2432:
    movq -1968(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2441
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2451
    movq $24, %rax  # Load compile-time constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1976(%rbp)
    movq $16, %rax  # Load compile-time constant PROGRAM_TYPES
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1984(%rbp)
    movq $0, %rax
    movq %rax, -1992(%rbp)
.L2461:    movq -1992(%rbp), %rax
    pushq %rax
    movq -1976(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2462
    movq -1984(%rbp), %rax
    pushq %rax
    movq -1992(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -2000(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2000(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2008(%rbp)
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -2008(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2016(%rbp)
    movq -2016(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant TYPE_KIND_VARIANT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -2008(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2024(%rbp)
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -2008(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2032(%rbp)
    movq $0, %rax
    movq %rax, -2040(%rbp)
.L2481:    movq -2040(%rbp), %rax
    pushq %rax
    movq -2024(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2482
    movq -2032(%rbp), %rax
    pushq %rax
    movq -2040(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -2048(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2048(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2056(%rbp)
    movq -1952(%rbp), %rax
    pushq %rax
    movq -2056(%rbp), %rax
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
    movq -2008(%rbp), %rax
    pushq %rax
    leaq -1960(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -2024(%rbp), %rax
    pushq %rax
    leaq -2040(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1976(%rbp), %rax
    pushq %rax
    leaq -1992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2492
.L2491:
.L2492:
    movq -2040(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -2040(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2481
.L2482:
    jmp .L2472
.L2471:
.L2472:
    movq -1992(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2461
.L2462:
    jmp .L2452
.L2451:
.L2452:
    jmp .L2442
.L2441:
.L2442:
    movq -1960(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
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
    movq -1960(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2080(%rbp)
    movq -2080(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1952(%rbp), %rax
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
    jmp .L2502
.L2501:
.L2502:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2088(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2088(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2096(%rbp)
    movq -2096(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2511
    movq -1304(%rbp), %rax
    movq %rax, -2104(%rbp)
    movq $0, %rax
    movq %rax, -2112(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2521
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
    movq %rax, -2144(%rbp)
.L2531:    movq -2144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2532
    movq $0, %rax
    movq %rax, -2152(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    movq $1, %rax
    movq %rax, -2152(%rbp)
    jmp .L2542
.L2541:
.L2542:
    movq -2152(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2551
    movq $0, %rax
    movq %rax, -2144(%rbp)
    jmp .L2552
.L2551:
.L2552:
    movq -2152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2561
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
    movq %rax, -2208(%rbp)
    movq $0, %rax
    movq %rax, -2216(%rbp)
    movq -2208(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant TYPE_KIND_VARIANT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
    movq $1, %rax
    movq %rax, -2216(%rbp)
    jmp .L2572
.L2571:
.L2572:
    movq -2216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2581
    movq $24, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2232(%rbp)
    movq $16, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2240(%rbp)
    movq $0, %rax
    movq %rax, -2248(%rbp)
    movq $1, %rax
    movq %rax, -2256(%rbp)
.L2591:    movq -2256(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2592
    movq $0, %rax
    movq %rax, -2264(%rbp)
    movq -2248(%rbp), %rax
    pushq %rax
    movq -2232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2601
    movq $1, %rax
    movq %rax, -2264(%rbp)
    jmp .L2602
.L2601:
.L2602:
    movq -2264(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2611
    movq $0, %rax
    movq %rax, -2256(%rbp)
    jmp .L2612
.L2611:
.L2612:
    movq -2264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2621
    movq -2248(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -2288(%rbp)
    movq -2240(%rbp), %rax
    addq -2288(%rbp), %rax
    movq %rax, -2296(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2304(%rbp)
    movq -2104(%rbp), %rax
    pushq %rax
    movq -2304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -2312(%rbp)
    movq -2312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2631
    movq -336(%rbp), %rax
    movq %rax, -2112(%rbp)
    movq $0, %rax
    movq %rax, -2256(%rbp)
    movq $0, %rax
    movq %rax, -2144(%rbp)
    jmp .L2632
.L2631:
.L2632:
    movq -2248(%rbp), %rax
    addq $1, %rax
    movq %rax, -2248(%rbp)
    jmp .L2622
.L2621:
.L2622:
    jmp .L2591
.L2592:
    jmp .L2582
.L2581:
.L2582:
    movq -304(%rbp), %rax
    addq $1, %rax
    movq %rax, -304(%rbp)
    jmp .L2562
.L2561:
.L2562:
    jmp .L2531
.L2532:
    jmp .L2522
.L2521:
.L2522:
    movq -2112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
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
    movq -2112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2080(%rbp)
    movq -2080(%rbp), %rax
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
    movq -2104(%rbp), %rax
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
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2384(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2392(%rbp)
    movq -2392(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2652
.L2651:
.L2652:
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2642
.L2641:
.L2642:
    jmp .L2512
.L2511:
.L2512:
    movq $0, %rax
    movq %rax, -2400(%rbp)
    movq -2400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2408(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $0, %rax
    movq %rax, -2432(%rbp)
    movq $1, %rax
    movq %rax, -2440(%rbp)
.L2671:    movq -2440(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2672
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2448(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2448(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2456(%rbp)
    movq -2456(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2681
    movq $0, %rax
    pushq %rax
    leaq -2440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2682
.L2681:
.L2682:
    movq -2456(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2691
    movq $0, %rax
    pushq %rax
    leaq -2440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2692
.L2691:
.L2692:
    movq $0, %rax
    movq %rax, -2464(%rbp)
    movq -2456(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq -2456(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2711
    movq $1, %rax
    pushq %rax
    leaq -2464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2712
.L2711:
.L2712:
    jmp .L2702
.L2701:
.L2702:
    movq -2464(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2721
    movq -72(%rbp), %rax
    pushq %rax
    movq -2432(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2731
    movq -2432(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2741
    movq $4, %rax
    pushq %rax
    leaq -2432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2742
.L2741:
.L2742:
    movq -2432(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2751
    movq -2432(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -2432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2752
.L2751:
.L2752:
    movq $8, %rax
    movq %rax, -104(%rbp)
    movq -2432(%rbp), %rax
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
    jmp .L2732
.L2731:
.L2732:
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
    movq %rax, -2520(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2528(%rbp)
    movq -2528(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2761
    movq $0, %rax
    pushq %rax
    leaq -2440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2762
.L2761:
    movq -2528(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2771
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2536(%rbp)
    jmp .L2772
.L2771:
    leaq .STR37(%rip), %rax
    movq %rax, -2544(%rbp)
    movq -2544(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -2520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L2772:
.L2762:
    jmp .L2722
.L2721:
.L2722:
    jmp .L2671
.L2672:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2560(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -1304(%rbp), %rax
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
    jmp .L2662
.L2661:
.L2662:
    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2781
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
    movq -1304(%rbp), %rax
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
    jmp .L2782
.L2781:
.L2782:
    movq -1304(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2072
.L2071:
.L2072:
    movq -24(%rbp), %rax
    pushq %rax
    movq $134, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2791
    movq $134, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2600(%rbp)
    movq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2792
.L2791:
.L2792:
    movq -24(%rbp), %rax
    pushq %rax
    movq $135, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2801
    movq $135, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2408(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2802
.L2801:
.L2802:
    movq -24(%rbp), %rax
    pushq %rax
    movq $133, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2811
    movq $133, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2536(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2640(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2640(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2648(%rbp)
    movq -2648(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2821
    leaq .STR38(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -2640(%rbp), %rax
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
    jmp .L2822
.L2821:
.L2822:
    movq $8, %rax
    pushq %rax
    movq -2640(%rbp), %rax
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
    movq %rax, -2680(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2688(%rbp)
    movq -2680(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2812
.L2811:
.L2812:
    leaq .STR39(%rip), %rax
    movq %rax, -2544(%rbp)
    movq -2544(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
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
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2831
    leaq .STR40(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2832
.L2831:
.L2832:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_print
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
.L2841:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2842
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
    jz .L2851
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2852
.L2851:
.L2852:
    movq -56(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2861
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2862
.L2861:
.L2862:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2871
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2872
.L2871:
.L2872:
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2881
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
    jz .L2891
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2892
.L2891:
.L2892:
    movq -56(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2901
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2902
.L2901:
.L2902:
    movq -56(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2911
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2912
.L2911:
.L2912:
    movq -56(%rbp), %rax
    pushq %rax
    movq $44, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2921
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_break_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2922
.L2921:
.L2922:
    movq -56(%rbp), %rax
    pushq %rax
    movq $45, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2931
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_continue_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2932
.L2931:
.L2932:
    movq -56(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2941
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2942
.L2941:
.L2942:
    movq -56(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2951
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2952
.L2951:
.L2952:
    movq -56(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2961
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2962
.L2961:
.L2962:
    movq -56(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2971
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2972
.L2971:
.L2972:
    movq -56(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2981
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2982
.L2981:
.L2982:
    movq -56(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2991
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_for_range_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2992
.L2991:
.L2992:
    movq -56(%rbp), %rax
    pushq %rax
    movq $139, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3001
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
    jmp .L3002
.L3001:
.L3002:
    movq -56(%rbp), %rax
    pushq %rax
    movq $140, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3011
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
    jmp .L3012
.L3011:
.L3012:
    movq -56(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3021
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
    jmp .L3022
.L3021:
.L3022:
    movq -56(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3031
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
    jmp .L3032
.L3031:
.L3032:
    movq -56(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3041
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
    jz .L3051
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3052
.L3051:
.L3052:
    movq -80(%rbp), %rax
    pushq %rax
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3061
    leaq .STR41(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR42(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR43(%rip), %rax
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
    jmp .L3062
.L3061:
.L3062:
    jmp .L3042
.L3041:
.L3042:
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
    jz .L3071
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
    jz .L3081
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3082
.L3081:
.L3082:
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant EXPR_BUILTIN_CALL
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3091
    leaq .STR44(%rip), %rax
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
    jmp .L3092
.L3091:
.L3092:
    jmp .L3072
.L3071:
.L3072:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3101
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3102
.L3101:
.L3102:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3111
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
    jz .L3121
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3131
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3132
.L3131:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3132:
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
    jmp .L3122
.L3121:
.L3122:
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
    jmp .L3112
.L3111:
.L3112:
    jmp .L2882
.L2881:
.L2882:
    jmp .L2841
.L2842:
    movq -24(%rbp), %rax
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


.globl parser_parse_for_range_statement
parser_parse_for_range_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    jz .L3141
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
    movq %rax, -64(%rbp)
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
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -80(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -88(%rbp)
    movq -72(%rbp), %rax
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
    movq -88(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call statement_create_for_each
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3142
.L3141:
.L3142:
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
    movq %rax, -136(%rbp)
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
    movq %rax, -144(%rbp)
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
    movq $0, %rax
    movq %rax, -168(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $38, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3151
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
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3152
.L3151:
.L3152:
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
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -80(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -88(%rbp)
    movq -72(%rbp), %rax
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
    movq -88(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
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
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
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
.L3161:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3162
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
    jz .L3171
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
    jz .L3181
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
    jz .L3191
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
    jmp .L3192
.L3191:
.L3192:
    movq -184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3201
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
.L3211:    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3212
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
    jmp .L3211
.L3212:
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
    jmp .L3202
.L3201:
.L3202:
    jmp .L3182
.L3181:
.L3182:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3221
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
    jz .L3231
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
    jmp .L3232
.L3231:
.L3232:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3241
    movq -64(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3251
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
.L3261:    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3262
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
    jmp .L3261
.L3262:
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
    jmp .L3252
.L3251:
.L3252:
    jmp .L3242
.L3241:
.L3242:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3222
.L3221:
.L3222:
    jmp .L3172
.L3171:
.L3172:
    movq -96(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3271
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3272
.L3271:
.L3272:
    jmp .L3161
.L3162:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -264(%rbp)
    movq $18, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -272(%rbp)
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


.globl parser_parse_inline_assembly_statement
parser_parse_inline_assembly_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    subq $2048, %rsp  # Pre-allocate generous stack space
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
.L3281:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3282
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
    jz .L3291
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3292
.L3291:
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
    jz .L3301
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
    jz .L3311
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3312
.L3311:
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
.L3312:
    jmp .L3302
.L3301:
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
.L3302:
.L3292:
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    subq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3321
    leaq .STR45(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L3322
.L3321:
.L3322:
    jmp .L3281
.L3282:
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
    movq %rax, -96(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_try_match_end_assembly
parser_try_match_end_assembly:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
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
    leaq .STR46(%rip), %rax
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
    jz .L3331
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
    jmp .L3332
.L3331:
.L3332:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_whitespace
    movq %rax, -40(%rbp)
    leaq .STR47(%rip), %rax
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
    jz .L3341
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
    jmp .L3342
.L3341:
.L3342:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_try_match_word
lexer_try_match_word:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
.L3351:    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3352
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
    jz .L3361
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3362
.L3361:
.L3362:
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
    jmp .L3351
.L3352:
    movq $1, %rax
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
.L3371:    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3372
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
    jz .L3381
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
    jz .L3391
    leaq .STR48(%rip), %rax
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
    jmp .L3392
.L3391:
.L3392:
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
    jz .L3401
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
.L3411:    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3412
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
    jz .L3421
    leaq .STR49(%rip), %rax
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
    jmp .L3422
.L3421:
.L3422:
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
    jz .L3431
    leaq .STR50(%rip), %rax
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
    jmp .L3432
.L3431:
.L3432:
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
    jz .L3441
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -352(%rbp)
    jmp .L3442
.L3441:
    movq $0, %rax
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3442:
    jmp .L3411
.L3412:
    jmp .L3402
.L3401:
.L3402:
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
    jmp .L3382
.L3381:
    movq $0, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3382:
    jmp .L3371
.L3372:
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


.globl calculate_type_size
calculate_type_size:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    leaq .STR51(%rip), %rax
    movq %rax, -24(%rbp)
    leaq .STR52(%rip), %rax
    movq %rax, -32(%rbp)
    leaq .STR53(%rip), %rax
    movq %rax, -40(%rbp)
    leaq .STR54(%rip), %rax
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
    jz .L3451
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3452
.L3451:
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
    jz .L3461
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3462
.L3461:
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
    jz .L3471
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3472
.L3471:
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
    jz .L3481
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3482
.L3481:
.L3482:
.L3472:
.L3462:
.L3452:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3491
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
.L3501:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3502
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
    jz .L3511
    movq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L3512
.L3511:
.L3512:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3521
    movq $0, %rax
    movq %rax, -80(%rbp)
    jmp .L3522
.L3521:
.L3522:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3531
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
    jz .L3541
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
    jmp .L3542
.L3541:
.L3542:
    movq -72(%rbp), %rax
    addq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L3532
.L3531:
.L3532:
    jmp .L3501
.L3502:
    jmp .L3492
.L3491:
.L3492:
    leaq .STR55(%rip), %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR56(%rip), %rax
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


.globl parser_parse_type_definition
parser_parse_type_definition:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
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
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3551
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
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3561
    leaq .STR57(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3562
.L3561:
.L3562:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEDEFINITION_NAME_OFFSET
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
    movq $0, %rax  # Load compile-time constant TYPE_KIND_STRUCT
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rax, -80(%rbp)
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
.L3571:    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3572
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3581
    leaq .STR25(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR58(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L3582
.L3581:
.L3582:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -120(%rbp)
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
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3591
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3601
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3611
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3621
    leaq .STR59(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3622
.L3621:
.L3622:
    jmp .L3612
.L3611:
.L3612:
    jmp .L3602
.L3601:
.L3602:
    jmp .L3592
.L3591:
.L3592:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -160(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3631
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3632
.L3631:
.L3632:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3641
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3642
.L3641:
.L3642:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3651
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3652
.L3651:
.L3652:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3661
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3662
.L3661:
.L3662:
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
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3671
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3672
.L3671:
.L3672:
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    addq $1, %rax
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -208(%rbp)
    movq $0, %rax
    movq %rax, -216(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3681
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3682
.L3681:
    movq -208(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3682:
    movq -216(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -192(%rbp), %rax
    subq $1, %rax
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -232(%rbp)
    movq -216(%rbp), %rax
    addq -232(%rbp), %rax
    movq %rax, -240(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load compile-time constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load compile-time constant TYPEFIELD_SIZE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -80(%rbp), %rax
    addq -256(%rbp), %rax
    movq %rax, -80(%rbp)
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
    jmp .L3571
.L3572:
    movq -80(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
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
    jmp .L3552
.L3551:
.L3552:
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
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3691
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEDEFINITION_NAME_OFFSET
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
    movq $126, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3701
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
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3711
    leaq .STR60(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3712
.L3711:
.L3712:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -368(%rbp)
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
    movq %rax, -376(%rbp)
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
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3721
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -376(%rbp)
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3722
.L3721:
.L3722:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3731
    leaq .STR61(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -376(%rbp)
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3732
.L3731:
.L3732:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3741
    leaq .STR62(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -376(%rbp)
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3742
.L3741:
.L3742:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3751
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -376(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3752
.L3751:
.L3752:
    movq -376(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3761
    leaq .STR63(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3762
.L3761:
.L3762:
    movq $3, %rax  # Load compile-time constant TYPE_KIND_ARRAY
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -376(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_ARRAY_ELEMENT_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -368(%rbp), %rax
    pushq %rax
    movq $28, %rax  # Load compile-time constant TYPEDEFINITION_DATA_ARRAY_LENGTH_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_ARRAY_ELEMENT_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -368(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -448(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
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
    jmp .L3702
.L3701:
    movq -32(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3771
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
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $8, %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
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
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3781
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
    jmp .L3782
.L3781:
.L3782:
    movq -32(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3791
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3792
.L3791:
.L3792:
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
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3801
    movq $2, %rax
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -504(%rbp)
.L3811:    movq -504(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3812
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3821
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
    jmp .L3822
.L3821:
.L3822:
    movq $0, %rax
    movq %rax, -512(%rbp)
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
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3831
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -512(%rbp)
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3832
.L3831:
.L3832:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3841
    leaq .STR61(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -512(%rbp)
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3842
.L3841:
.L3842:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3851
    leaq .STR62(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -512(%rbp)
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3852
.L3851:
.L3852:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3861
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -512(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3862
.L3861:
.L3862:
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3871
    leaq .STR64(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3872
.L3871:
.L3872:
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -584(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq -488(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3881
    movq -488(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -600(%rbp)
    movq -600(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -600(%rbp), %rax
    movq %rax, -496(%rbp)
    jmp .L3882
.L3881:
.L3882:
    movq -584(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -616(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -496(%rbp), %rax
    addq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -584(%rbp), %rax
    addq $1, %rax
    movq %rax, -624(%rbp)
    movq -624(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
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
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3891
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3892
.L3891:
.L3892:
    movq -32(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3901
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3902
.L3901:
    movq $0, %rax
    movq %rax, -504(%rbp)
.L3902:
    jmp .L3811
.L3812:
    jmp .L3802
.L3801:
.L3802:
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
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3911
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L3912
.L3911:
.L3912:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3921
    leaq .STR61(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L3922
.L3921:
.L3922:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3931
    leaq .STR62(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L3932
.L3931:
.L3932:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3941
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L3942
.L3941:
    leaq .STR65(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
.L3942:
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
    jmp .L3772
.L3771:
    movq $1, %rax  # Load compile-time constant TYPE_KIND_VARIANT
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
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
.L3951:    movq -32(%rbp), %rax
    pushq %rax
    movq $111, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3952
    movq $111, %rax
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
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3961
    leaq .STR66(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3962
.L3961:
.L3962:
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    addq $1, %rax
    movq %rax, -768(%rbp)
    movq -768(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -776(%rbp)
    movq -768(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -784(%rbp)
    movq -784(%rbp), %rax
    pushq %rax
    movq -776(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -792(%rbp)
    movq -792(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -768(%rbp), %rax
    subq $1, %rax
    movq %rax, -800(%rbp)
    movq -800(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -808(%rbp)
    movq -792(%rbp), %rax
    addq -808(%rbp), %rax
    movq %rax, -816(%rbp)
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -832(%rbp)
    movq -832(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant VARIANT_NAME_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -768(%rbp), %rax
    subq $1, %rax
    movq %rax, -840(%rbp)
    movq -840(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load compile-time constant VARIANT_TAG_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
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
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3971
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -232(%rbp)
    movq $1, %rax
    movq %rax, -504(%rbp)
.L3981:    movq -504(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3982
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
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3991
    leaq .STR67(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L3992
.L3991:
.L3992:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -120(%rbp)
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
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4001
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4011
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4021
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4031
    leaq .STR59(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
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
    call exit
    jmp .L4032
.L4031:
.L4032:
    jmp .L4022
.L4021:
.L4022:
    jmp .L4012
.L4011:
.L4012:
    jmp .L4002
.L4001:
.L4002:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -160(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4041
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4042
.L4041:
.L4042:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4051
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4052
.L4051:
.L4052:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4061
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4062
.L4061:
.L4062:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4071
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4072
.L4071:
.L4072:
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -960(%rbp)
    movq -960(%rbp), %rax
    addq $1, %rax
    movq %rax, -968(%rbp)
    movq -968(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -976(%rbp)
    movq -968(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -984(%rbp)
    movq -984(%rbp), %rax
    pushq %rax
    movq -976(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -992(%rbp)
    movq -992(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -968(%rbp), %rax
    subq $1, %rax
    movq %rax, -1000(%rbp)
    movq -1000(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1008(%rbp)
    movq -992(%rbp), %rax
    addq -1008(%rbp), %rax
    movq %rax, -240(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -232(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load compile-time constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call calculate_type_size
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load compile-time constant TYPEFIELD_SIZE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -232(%rbp), %rax
    addq -256(%rbp), %rax
    movq %rax, -232(%rbp)
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
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4081
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4082
.L4081:
    movq $0, %rax
    movq %rax, -504(%rbp)
.L4082:
    jmp .L3981
.L3982:
    jmp .L3972
.L3971:
.L3972:
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
    jmp .L3951
.L3952:
    movq $8, %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $24, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -760(%rbp)
    movq $16, %rax  # Load compile-time constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -776(%rbp)
    movq $0, %rax
    movq %rax, -1104(%rbp)
.L4091:    movq -1104(%rbp), %rax
    pushq %rax
    movq -760(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4092
    movq -1104(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load compile-time constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -808(%rbp)
    movq -776(%rbp), %rax
    addq -808(%rbp), %rax
    movq %rax, -816(%rbp)
    movq $8, %rax
    movq %rax, -1128(%rbp)
    movq $16, %rax  # Load compile-time constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -960(%rbp)
    movq $8, %rax  # Load compile-time constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -976(%rbp)
    movq $0, %rax
    movq %rax, -1152(%rbp)
.L4101:    movq -1152(%rbp), %rax
    pushq %rax
    movq -960(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4102
    movq -1152(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load compile-time constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -232(%rbp)
    movq -976(%rbp), %rax
    addq -232(%rbp), %rax
    movq %rax, -240(%rbp)
    movq $20, %rax  # Load compile-time constant TYPEFIELD_SIZE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq -1128(%rbp), %rax
    addq -256(%rbp), %rax
    movq %rax, -1128(%rbp)
    movq -1152(%rbp), %rax
    addq $1, %rax
    movq %rax, -1152(%rbp)
    jmp .L4101
.L4102:
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1200(%rbp)
    movq -1128(%rbp), %rax
    pushq %rax
    movq -1200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4111
    movq -1128(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load compile-time constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L4112
.L4111:
.L4112:
    movq -1104(%rbp), %rax
    addq $1, %rax
    movq %rax, -1104(%rbp)
    jmp .L4091
.L4092:
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
.L3772:
.L3702:
    jmp .L3692
.L3691:
    leaq .STR68(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax  # Load compile-time constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L3692:
    movq -16(%rbp), %rax
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
    jz .L4121
    leaq .STR69(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $10, %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR70(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR12(%rip), %rax
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
    jmp .L4122
.L4121:
.L4122:
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
    jz .L4131
    leaq .STR71(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4132
.L4131:
.L4132:
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
    leaq .STR51(%rip), %rax
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
    jz .L4141
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
    jz .L4151
    leaq .STR72(%rip), %rax
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
    jmp .L4152
.L4151:
.L4152:
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
    jz .L4161
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4171
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4181
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4191
    leaq .STR64(%rip), %rax
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
    jmp .L4192
.L4191:
.L4192:
    jmp .L4182
.L4181:
.L4182:
    jmp .L4172
.L4171:
.L4172:
    jmp .L4162
.L4161:
.L4162:
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
    jz .L4201
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4202
.L4201:
.L4202:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4211
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4212
.L4211:
.L4212:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4221
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
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
    jz .L4231
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4232
.L4231:
.L4232:
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
.L4241:    movq -184(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4242
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
    jz .L4251
    leaq .STR73(%rip), %rax
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
    jmp .L4252
.L4251:
.L4252:
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
    jz .L4261
    movq -248(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4271
    movq -248(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4281
    movq -248(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4291
    leaq .STR64(%rip), %rax
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
    jmp .L4292
.L4291:
.L4292:
    jmp .L4282
.L4281:
.L4282:
    jmp .L4272
.L4271:
.L4272:
    jmp .L4262
.L4261:
.L4262:
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
    jz .L4301
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4302
.L4301:
.L4302:
    movq -248(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4311
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4312
.L4311:
.L4312:
    movq -248(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4321
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4322
.L4321:
.L4322:
    movq -248(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4331
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4332
.L4331:
.L4332:
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
    jmp .L4241
.L4242:
    jmp .L4142
.L4141:
.L4142:
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
    jz .L4341
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L4342
.L4341:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4351
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L4352
.L4351:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4361
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L4362
.L4361:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4371
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L4372
.L4371:
.L4372:
.L4362:
.L4352:
.L4342:
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4381
    leaq .STR65(%rip), %rax
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
    jmp .L4382
.L4381:
.L4382:
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
.L4391:    movq -368(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4392
    movq -368(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4401
    jmp .L4392
    jmp .L4402
.L4401:
.L4402:
    movq -368(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4411
    jmp .L4392
    jmp .L4412
.L4411:
.L4412:
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
    jz .L4421
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4422
.L4421:
.L4422:
    movq -368(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4431
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4432
.L4431:
.L4432:
    movq -368(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4441
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4442
.L4441:
.L4442:
    movq -368(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4451
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4452
.L4451:
.L4452:
    movq -368(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4461
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4462
.L4461:
.L4462:
    movq -368(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4471
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4472
.L4471:
.L4472:
    movq -368(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4481
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4482
.L4481:
.L4482:
    movq -368(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4491
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_for_range_statement
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4492
.L4491:
.L4492:
    movq -368(%rbp), %rax
    pushq %rax
    movq $139, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4501
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4502
.L4501:
.L4502:
    movq -368(%rbp), %rax
    pushq %rax
    movq $140, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4511
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4512
.L4511:
.L4512:
    movq -368(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4521
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4522
.L4521:
.L4522:
    movq -368(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4531
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_implicit_compound_assign
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4532
.L4531:
.L4532:
    movq -368(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4541
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
    jz .L4551
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4552
.L4551:
    leaq .STR74(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR42(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $4, %rax  # Load compile-time constant EXPR_FUNCTION_CALL
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR43(%rip), %rax
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
.L4552:
    jmp .L4542
.L4541:
.L4542:
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
    jz .L4561
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
    jz .L4571
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4572
.L4571:
    leaq .STR44(%rip), %rax
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
.L4572:
    jmp .L4562
.L4561:
.L4562:
    movq -376(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4581
    leaq .STR75(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR76(%rip), %rax
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
    jmp .L4582
.L4581:
.L4582:
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
    jmp .L4391
.L4392:
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
    jz .L4591
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
    jmp .L4592
.L4591:
.L4592:
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
    jz .L4601
    leaq .STR77(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L4602
.L4601:
.L4602:
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
    jz .L4611
    leaq .STR78(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L4612
.L4611:
.L4612:
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
.L4621:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4622
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
    jz .L4631
    leaq .STR79(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4632
.L4631:
.L4632:
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
    jz .L4641
    movq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4642
.L4641:
.L4642:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4651
    movq $0, %rax
    movq %rax, -40(%rbp)
    jmp .L4652
.L4651:
.L4652:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4661
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
    jz .L4671
    movq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L4672
.L4671:
.L4672:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4681
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_import
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4691
    leaq .STR80(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4692
.L4691:
.L4692:
    movq -104(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_import
    jmp .L4682
.L4681:
.L4682:
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
    jz .L4701
    movq $1, %rax
    movq %rax, -112(%rbp)
    jmp .L4702
.L4701:
.L4702:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4711
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
    jmp .L4712
.L4711:
.L4712:
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
    jz .L4721
    movq $1, %rax
    movq %rax, -136(%rbp)
    jmp .L4722
.L4721:
.L4722:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4731
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
    jz .L4741
    leaq .STR81(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4742
.L4741:
.L4742:
    movq -152(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_function
    jmp .L4732
.L4731:
.L4732:
    movq $0, %rax
    movq %rax, -160(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4751
    movq $1, %rax
    movq %rax, -160(%rbp)
    jmp .L4752
.L4751:
.L4752:
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4761
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
    movq %rax, -176(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4771
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -192(%rbp)
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
    movq %rax, -200(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4781
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
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4791
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -248(%rbp)
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
    movq %rax, -256(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
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
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_global
    jmp .L4792
.L4791:
.L4792:
    jmp .L4782
.L4781:
.L4782:
    jmp .L4772
.L4771:
.L4772:
    jmp .L4762
.L4761:
.L4762:
    movq $0, %rax
    movq %rax, -264(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4801
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L4802
.L4801:
.L4802:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4811
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L4812
.L4811:
.L4812:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4821
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L4822
.L4821:
.L4822:
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4831
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L4832
.L4831:
.L4832:
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4841
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4842
.L4841:
.L4842:
    jmp .L4662
.L4661:
.L4662:
    jmp .L4621
.L4622:
    movq -16(%rbp), %rax
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
    jz .L4851
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4852
.L4851:
.L4852:
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
    jz .L4861
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
    jmp .L4862
.L4861:
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant EXPR_UNARY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4871
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
    jmp .L4872
.L4871:
    movq -16(%rbp), %rax
    pushq %rax
    movq $4, %rax  # Load compile-time constant EXPR_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4881
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
    jmp .L4882
.L4881:
    movq -16(%rbp), %rax
    pushq %rax
    movq $6, %rax  # Load compile-time constant EXPR_FIELD_ACCESS
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4891
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
    jmp .L4892
.L4891:
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant EXPR_ARRAY_ACCESS
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4901
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
    jmp .L4902
.L4901:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant EXPR_IDENTIFIER
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4911
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
    jmp .L4912
.L4911:
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax  # Load compile-time constant EXPR_STRING_LITERAL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4921
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
    jmp .L4922
.L4921:
.L4922:
.L4912:
.L4902:
.L4892:
.L4882:
.L4872:
.L4862:
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
    jz .L4931
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4932
.L4931:
.L4932:
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
    jz .L4941
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
    jmp .L4942
.L4941:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load compile-time constant STMT_SET
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4951
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
    jmp .L4952
.L4951:
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax  # Load compile-time constant STMT_IF
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4961
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
    jmp .L4962
.L4961:
    movq -16(%rbp), %rax
    pushq %rax
    movq $6, %rax  # Load compile-time constant STMT_WHILE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4971
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
    jmp .L4972
.L4971:
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant STMT_FOR
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4981
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
    jmp .L4982
.L4981:
    movq -16(%rbp), %rax
    pushq %rax
    movq $12, %rax  # Load compile-time constant STMT_FOR_EACH
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4991
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
    jmp .L4992
.L4991:
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax  # Load compile-time constant STMT_RETURN
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5001
    movq $8, %rax  # Load compile-time constant STMT_RETURN_VALUE
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
    jmp .L5002
.L5001:
    movq -16(%rbp), %rax
    pushq %rax
    movq $7, %rax  # Load compile-time constant STMT_EXPRESSION
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5011
    movq $8, %rax  # Load compile-time constant STMT_EXPR_VALUE
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
    jmp .L5012
.L5011:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax  # Load compile-time constant STMT_BREAK
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5021
    jmp .L5022
.L5021:
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax  # Load compile-time constant STMT_CONTINUE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5031
    jmp .L5032
.L5031:
.L5032:
.L5022:
.L5012:
.L5002:
.L4992:
.L4982:
.L4972:
.L4962:
.L4952:
.L4942:
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
    jz .L5041
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5042
.L5041:
.L5042:
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
    jz .L5051
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5052
.L5051:
.L5052:
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
    jz .L5061
    jmp .L5062
.L5061:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load compile-time constant TYPE_STRUCT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5071
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
    jmp .L5072
.L5071:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load compile-time constant TYPE_ARRAY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5081
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
    jmp .L5082
.L5081:
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax  # Load compile-time constant TYPE_POINTER
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5091
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
    jmp .L5092
.L5091:
.L5092:
.L5082:
.L5072:
.L5062:
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
    jz .L5101
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5102
.L5101:
.L5102:
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
    jz .L5111
    movq $0, %rax
    movq %rax, -32(%rbp)
.L5121:    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5122
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
    jz .L5131
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call function_destroy
    jmp .L5132
.L5131:
.L5132:
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5121
.L5122:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L5112
.L5111:
.L5112:
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
    jz .L5141
    movq $0, %rax
    movq %rax, -88(%rbp)
.L5151:    movq -88(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5152
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
    jz .L5161
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L5162
.L5161:
.L5162:
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5151
.L5152:
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L5142
.L5141:
.L5142:
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
    jz .L5171
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L5172
.L5171:
.L5172:
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
    jz .L5181
    movq $0, %rax
    movq %rax, -160(%rbp)
.L5191:    movq -160(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5192
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
    jz .L5201
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_destroy
    jmp .L5202
.L5201:
.L5202:
    movq -160(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5191
.L5192:
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L5182
.L5181:
.L5182:
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
    jz .L5211
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L5212
.L5211:
.L5212:
    movq $0, %rax
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
    jz .L5221
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5222
.L5221:
.L5222:
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
    jz .L5231
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5232
.L5231:
.L5232:
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
    jz .L5241
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5242
.L5241:
.L5242:
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
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
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
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5251
    leaq .STR82(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    leaq .STR83(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5252
.L5251:
.L5252:
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -48(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -56(%rbp)
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5261
    leaq .STR84(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    leaq .STR83(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5262
.L5261:
.L5262:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -88(%rbp)
    movq $8, %rax  # Load compile-time constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax  # Load compile-time constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5271
    leaq .STR85(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    leaq .STR83(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -112(%rbp), %rax
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
    movq $8, %rax  # Load compile-time constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -120(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -128(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -136(%rbp)
    movq -48(%rbp), %rax
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
    movq -136(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
