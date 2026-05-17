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
.globl EXPR_ARRAY_LITERAL_CONST
EXPR_ARRAY_LITERAL_CONST:    .quad 26
.globl EXPR_CONVERT
EXPR_CONVERT:    .quad 27
.globl EXPR_POSITION_OF
EXPR_POSITION_OF:    .quad 28
.globl EXPR_FLOAT_LITERAL
EXPR_FLOAT_LITERAL:    .quad 29
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
TypeDefinition_SIZE:    .quad 56
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
.globl TYPEDEFINITION_SOURCE_FILE_OFFSET
TYPEDEFINITION_SOURCE_FILE_OFFSET:    .quad 48
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
.globl FUNCTION_SOURCE_FILE_OFFSET
FUNCTION_SOURCE_FILE_OFFSET:    .quad 48
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

    # Convert integer to string (signed)
    movq %rdi, %rax  # integer value
    xorq %r8, %r8    # r8 = 0 (negative flag)
    testq %rax, %rax
    jns .pi_not_negative
    movq $1, %r8     # mark as negative
    negq %rax        # make positive for conversion
.pi_not_negative:
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
    # Prepend minus sign if negative
    testq %r8, %r8
    jz .pi_not_neg_print
    decq %rsi
    movb $45, (%rsi)  # '-' character
.pi_not_neg_print:

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
.STR28:    .string "[PARSER ERROR] Named arguments are not supported on this call form (expression type "
.STR29:    .string "Integer"
.STR30:    .string "Float"
.STR31:    .string "String"
.STR32:    .string "Boolean"
.STR33:    .string "Character"
.STR34:    .string "[PARSER ERROR] Null parser in parse_primary"
.STR35:    .string "[PARSER ERROR] Null current_token in parse_primary"
.STR36:    .string "Set"
.STR37:    .string "size_of"
.STR38:    .string "position"
.STR39:    .string "list"
.STR40:    .string "dictionary"
.STR41:    .string "value"
.STR42:    .string "a"
.STR43:    .string "memory_get_pointer"
.STR44:    .string "memory_get_byte"
.STR45:    .string "[PARSER ERROR] Expected function name after $ at line "
.STR46:    .string "string_length"
.STR47:    .string "length"
.STR48:    .string "External"
.STR49:    .string "substring"
.STR50:    .string "string_substring"
.STR51:    .string "string"
.STR52:    .string "representation"
.STR53:    .string "int_to_string"
.STR54:    .string "[PARSER ERROR] Expected field name after 'the' at line "
.STR55:    .string "[PARSER ERROR] Expected 'of' after field name at line "
.STR56:    .string "an"
.STR57:    .string "[PARSER ERROR] Expected 'containing' after 'a list' at line "
.STR58:    .string "set"
.STR59:    .string "[PARSER ERROR] Expected 'containing' after 'a set' at line "
.STR60:    .string "[PARSER ERROR] Expected 'with' after struct type name at line "
.STR61:    .string "[PARSER ERROR] Expected field name at line "
.STR62:    .string "Array"
.STR63:    .string "[PARSER ERROR] Expected 'of' after 'an Array' at line "
.STR64:    .string "[PARSER ERROR] Expected integer size after 'an Array of' at line "
.STR65:    .string "[PARSER ERROR] Expected type name after array size at line "
.STR66:    .string "[PARSER ERROR] Array size mismatch: declared "
.STR67:    .string " but got "
.STR68:    .string " elements"
.STR69:    .string "[PARSER ERROR] Expected ':' after 'dictionary with' at line "
.STR70:    .string "[PARSER ERROR] Expected variant name after 'as'"
.STR71:    .string "[PARSER ERROR] Expected field name after 'with'"
.STR72:    .string "[PARSER ERROR] Expected ',' or ')' in function arguments at line "
.STR73:    .string "[PARSER ERROR] Expected integer after 'negative' at line "
.STR74:    .string "[PARSER ERROR] Expected parameter name after 'lambda'"
.STR75:    .string "[PARSER ERROR] Expected parameter name after comma"
.STR76:    .string "[PARSER ERROR] Expected ':' after lambda parameters"
.STR77:    .string "[PARSER ERROR] Expected integer or identifier at line "
.STR78:    .string "[PARSER ERROR] Display/Print is a statement and should not use parentheses. Use 'Display expression' not 'Display(expression)' at line "
.STR79:    .string "memory_set_pointer"
.STR80:    .string "memory_set_byte"
.STR81:    .string "Add"
.STR82:    .string "end"
.STR83:    .string "list_append"
.STR84:    .string "[PARSER WARNING] Expression statement (type="
.STR85:    .string ") - may not have intended effect"
.STR86:    .string "step"
.STR87:    .string "[PARSER ERROR] Expected 'type' keyword after 'of'"
.STR88:    .string "[PARSER ERROR] Expected type name after 'of Type'"
.STR89:    .string "[PARSER ERROR] Expected field name in When pattern"
.STR90:    .string "[PARSER ERROR] Expected binding name after 'as'"
.STR91:    .string "[WARNING] Match on type '"
.STR92:    .string "' is not exhaustive. Missing variants:"
.STR93:    .string "  - "
.STR94:    .string "[PARSER ERROR] Inline assembly block too large (max 8192 bytes)\n"
.STR95:    .string "End"
.STR96:    .string "Assembly"
.STR97:    .string "Byte"
.STR98:    .string "Short"
.STR99:    .string "Long"
.STR100:    .string "[PARSER WARNING] Unknown type '"
.STR101:    .string "', defaulting to 8 bytes"
.STR102:    .string "[PARSER ERROR] Expected type name at line "
.STR103:    .string " (got token type "
.STR104:    .string "[PARSER ERROR] Expected array size at line "
.STR105:    .string "[PARSER ERROR] Expected element type at line "
.STR106:    .string "[PARSER ERROR] Expected return type at line "
.STR107:    .string "[PARSER ERROR] Expected variant name at line "
.STR108:    .string "[PARSER ERROR] Expected field name in variant at line "
.STR109:    .string "[PARSER ERROR] Expected field type at line "
.STR110:    .string "[PARSER ERROR] Expected 'called' or type name after 'Type' at line "
.STR111:    .string "[PARSER ERROR] Expected function name string literal (type "
.STR112:    .string "), got type "
.STR113:    .string "[PARSER ERROR] Function name is NULL!"
.STR114:    .string "[PARSER ERROR] Expected parameter name at line "
.STR115:    .string "[PARSER ERROR] Expected parameter name after separator at line "
.STR116:    .string "Nothing"
.STR117:    .string "[PARSER ERROR] Unrecognized statement at line "
.STR118:    .string " (token type "
.STR119:    .string "[ERROR] lexer_next_token returned NULL!"
.STR120:    .string "[ERROR] current_token is NULL!"
.STR121:    .string "[ERROR] parser_parse_import returned NULL!"
.STR122:    .string "Use"
.STR123:    .string "[PARSER ERROR] Expected 'Process' after 'Export'"
.STR124:    .string "[ERROR] parser_parse_function returned NULL!"
.STR125:    .string "[PARSER ERROR] Float literal in non-Float array literal"
.STR126:    .string "[PARSER ERROR] Cannot apply unary minus to a String literal"
.STR127:    .string "[PARSER ERROR] String literal in non-String array literal"
.STR128:    .string "[PARSER ERROR] Array literal element '"
.STR129:    .string "' is not a Constant of the declared array element type"
.STR130:    .string "[PARSER ERROR] Array literal element must be a literal of the declared element type or an identifier referencing such a Constant (got token type "
.STR131:    .string "[PARSER ERROR] Expected string literal or identifier after Import, got token type "
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $1, %rax  # Load constant EXPR_VARIABLE
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
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -232(%rbp)
    movq $0, %rax
    movq %rax, -240(%rbp)
    movq $0, %rax
    movq %rax, -248(%rbp)
.L861:    movq -248(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L862
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -248(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L861
.L862:
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -256(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -256(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call parser_handle_named_arg_capture
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq $0, %rax
    movq %rax, -272(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L872
.L871:
.L872:
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
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -232(%rbp), %rax
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
.L881:    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L882
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
    movq $0, %rax
    movq %rax, -296(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L892
.L891:
.L892:
    movq -288(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L901
    movq $0, %rax
    movq %rax, -304(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L911
    movq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L912
.L911:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L921
    movq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L922
.L921:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L932
.L931:
.L932:
.L922:
.L912:
    movq -304(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L942
.L941:
.L942:
    jmp .L902
.L901:
.L902:
    movq -296(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L951
    movq -112(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    movq -224(%rbp), %rax
    movq %rax, -320(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
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
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -136(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -320(%rbp), %rax
    movq %rax, -328(%rbp)
.L971:    movq -328(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L972
    movq $0, %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -328(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L971
.L972:
    jmp .L962
.L961:
.L962:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -336(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call parser_handle_named_arg_capture
    pushq %rax
    leaq -336(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -344(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L981
    movq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L982
.L981:
.L982:
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -336(%rbp), %rax
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
    movq -344(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -232(%rbp), %rax
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
    jmp .L952
.L951:
    movq $0, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L952:
    jmp .L881
.L882:
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L991
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L992
.L991:
.L992:
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
    movq -232(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq -232(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_attach_arg_names
    jmp .L1002
.L1001:
.L1002:
    jmp .L852
.L851:
.L852:
    movq $1, %rax
    movq %rax, -352(%rbp)
.L1011:    movq -352(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1012
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq $0, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1021
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
    movq %rax, -376(%rbp)
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq -384(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1041
    leaq .STR3(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
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
    jmp .L1042
.L1041:
.L1042:
    jmp .L1032
.L1031:
.L1032:
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -416(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq -384(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1052
.L1051:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1052:
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
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -440(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant EXPR_VARIABLE
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    leaq .STR4(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1072
.L1071:
.L1072:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -448(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -456(%rbp)
    movq $0, %rax
    movq %rax, -464(%rbp)
    movq $4, %rax
    movq %rax, -472(%rbp)
    movq $8, %rax
    movq %rax, -480(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq -480(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -456(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -496(%rbp)
.L1081:    movq -496(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1082
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
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq $0, %rax
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1092
.L1091:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -520(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    movq -480(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -528(%rbp)
    movq -456(%rbp), %rax
    addq -528(%rbp), %rax
    movq %rax, -536(%rbp)
    movq -520(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -464(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -544(%rbp)
    movq $0, %rax
    pushq %rax
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -552(%rbp)
    movq -552(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1102
.L1101:
.L1102:
.L1092:
    jmp .L1081
.L1082:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $48, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -560(%rbp)
    movq $25, %rax  # Load constant EXPR_QUALIFIED_CALL
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -448(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -416(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -456(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -464(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -560(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1062
.L1061:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -568(%rbp)
    movq $0, %rax
    movq %rax, -576(%rbp)
    movq -568(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -584(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -592(%rbp)
    movq -592(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    movq $40, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -600(%rbp)
    movq $32, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -608(%rbp)
    movq -608(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    movq $0, %rax
    movq %rax, -616(%rbp)
.L1141:    movq -616(%rbp), %rax
    pushq %rax
    movq -600(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1142
    movq -616(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -624(%rbp)
    movq -624(%rbp), %rax
    pushq %rax
    movq -608(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -632(%rbp)
    movq -632(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1151
    movq $8, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -640(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq -640(%rbp), %rax
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
    jz .L1161
    movq $1, %rax
    pushq %rax
    leaq -576(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -600(%rbp), %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1162
.L1161:
.L1162:
    jmp .L1152
.L1151:
.L1152:
    movq -616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1141
.L1142:
    jmp .L1132
.L1131:
.L1132:
    jmp .L1122
.L1121:
.L1122:
    jmp .L1112
.L1111:
.L1112:
    movq -576(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1171
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1172
.L1171:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -648(%rbp)
    movq $6, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -416(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -648(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1172:
.L1062:
    jmp .L1022
.L1021:
.L1022:
    movq -368(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1181
    movq $148, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -656(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1191
    movq $1, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1192
.L1191:
.L1192:
    movq -368(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    movq $1, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1202
.L1201:
.L1202:
    movq -656(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1211
    movq -368(%rbp), %rax
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
    movq %rax, -664(%rbp)
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -672(%rbp)
    movq $16, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -672(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -672(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -664(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -672(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -672(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1212
.L1211:
    leaq .STR5(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -680(%rbp)
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
.L1212:
    jmp .L1182
.L1181:
.L1182:
    movq -368(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    movq -368(%rbp), %rax
    pushq %rax
    movq $148, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1231
    movq $0, %rax
    pushq %rax
    leaq -352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1232
.L1231:
.L1232:
    jmp .L1222
.L1221:
.L1222:
    jmp .L1011
.L1012:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -688(%rbp)
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -696(%rbp)
    movq -696(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -704(%rbp)
    movq $0, %rax
    movq %rax, -712(%rbp)
    movq $4, %rax
    movq %rax, -720(%rbp)
    movq -720(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -728(%rbp)
    movq -728(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -728(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -736(%rbp)
    movq $0, %rax
    movq %rax, -744(%rbp)
    movq $0, %rax
    movq %rax, -752(%rbp)
.L1251:    movq -752(%rbp), %rax
    pushq %rax
    movq -720(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1252
    movq $0, %rax
    pushq %rax
    movq -752(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -752(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -752(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1251
.L1252:
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -760(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -768(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq -768(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call parser_handle_named_arg_capture
    pushq %rax
    leaq -768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -760(%rbp), %rax
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
    jz .L1261
    movq $1, %rax
    pushq %rax
    leaq -784(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -744(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1262
.L1261:
.L1262:
    movq -768(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -704(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -776(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -712(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -792(%rbp)
.L1271:    movq -792(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1272
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -800(%rbp)
    movq $0, %rax
    pushq %rax
    movq -800(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -808(%rbp)
    movq $0, %rax
    movq %rax, -816(%rbp)
    movq -808(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1281
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -816(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1282
.L1281:
.L1282:
    movq -808(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1291
    movq $0, %rax
    movq %rax, -824(%rbp)
    movq -784(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq $1, %rax
    pushq %rax
    leaq -824(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1302
.L1301:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -832(%rbp)
    movq -832(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
    movq $1, %rax
    pushq %rax
    leaq -824(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1312
.L1311:
.L1312:
.L1302:
    movq -824(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -816(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1322
.L1321:
.L1322:
    jmp .L1292
.L1291:
.L1292:
    movq -816(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
    movq -712(%rbp), %rax
    pushq %rax
    movq -720(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq -720(%rbp), %rax
    movq %rax, -840(%rbp)
    movq -720(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -720(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -720(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -728(%rbp), %rax
    pushq %rax
    movq -704(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -728(%rbp), %rax
    pushq %rax
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -736(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -840(%rbp), %rax
    movq %rax, -848(%rbp)
.L1351:    movq -848(%rbp), %rax
    pushq %rax
    movq -720(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1352
    movq $0, %rax
    pushq %rax
    movq -848(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -848(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -848(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1351
.L1352:
    jmp .L1342
.L1341:
.L1342:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -856(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq -856(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call parser_handle_named_arg_capture
    pushq %rax
    leaq -856(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -864(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -784(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -864(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1361
    movq $1, %rax
    pushq %rax
    leaq -784(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -744(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1362
.L1361:
.L1362:
    movq -712(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -872(%rbp)
    movq -856(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -704(%rbp), %rax
    addq -872(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -864(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -736(%rbp), %rax
    addq -872(%rbp), %rax
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
    jmp .L1332
.L1331:
    movq $0, %rax
    pushq %rax
    leaq -792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1332:
    jmp .L1271
.L1272:
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -744(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1371
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    leaq -736(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1372
.L1371:
.L1372:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -880(%rbp)
    movq -880(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1381
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -888(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -896(%rbp)
    movq $0, %rax
    pushq %rax
    movq -888(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -904(%rbp)
    movq -904(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1391
    movq $8, %rax
    pushq %rax
    movq -888(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -912(%rbp)
    movq $48, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -920(%rbp)
    movq $25, %rax  # Load constant EXPR_QUALIFIED_CALL
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -912(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -704(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -712(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -736(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -920(%rbp), %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1392
.L1391:
    movq -712(%rbp), %rax
    pushq %rax
    movq -704(%rbp), %rax
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
    movq -736(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1401
    movq -736(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_attach_arg_names
    jmp .L1402
.L1401:
.L1402:
.L1392:
    jmp .L1382
.L1381:
    movq -712(%rbp), %rax
    pushq %rax
    movq -704(%rbp), %rax
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
    movq -736(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1411
    movq -736(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_attach_arg_names
    jmp .L1412
.L1411:
.L1412:
.L1382:
    jmp .L1242
.L1241:
.L1242:
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
    jz .L1421
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
    jz .L1431
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
    jmp .L1432
.L1431:
.L1432:
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
    jz .L1441
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
    jz .L1451
    movq $23, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1452
.L1451:
    movq $22, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1452:
    jmp .L1442
.L1441:
.L1442:
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1461
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
    jz .L1471
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
    jz .L1481
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
    jz .L1491
    movq $25, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1492
.L1491:
    movq $27, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1492:
    jmp .L1482
.L1481:
.L1482:
    movq -96(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1501
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1511
    movq $26, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1512
.L1511:
    movq $24, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1512:
    jmp .L1502
.L1501:
.L1502:
    jmp .L1472
.L1471:
.L1472:
    movq -80(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1521
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
    jmp .L1522
.L1521:
.L1522:
    jmp .L1462
.L1461:
.L1462:
    movq -48(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1531
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
    jz .L1541
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
    jz .L1551
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
    jz .L1561
    movq $24, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1562
.L1561:
    movq $26, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1562:
    jmp .L1552
.L1551:
.L1552:
    movq -96(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1571
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1581
    movq $27, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1582
.L1581:
    movq $25, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1582:
    jmp .L1572
.L1571:
.L1572:
    jmp .L1542
.L1541:
.L1542:
    movq -80(%rbp), %rax
    pushq %rax
    movq $28, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1591
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
    jmp .L1592
.L1591:
.L1592:
    jmp .L1532
.L1531:
.L1532:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1601
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1611
    movq $23, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1612
.L1611:
    movq $22, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L1612:
    jmp .L1602
.L1601:
.L1602:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -128(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L1621
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
    jz .L1631
    movq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1632
.L1631:
.L1632:
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
    jz .L1641
    movq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1642
.L1641:
.L1642:
    jmp .L1622
.L1621:
.L1622:
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1651
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
    jmp .L1652
.L1651:
.L1652:
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
    jmp .L1422
.L1421:
.L1422:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1661
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
    jz .L1671
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
    jz .L1681
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
    jmp .L1682
.L1681:
.L1682:
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
    jz .L1691
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L1701
    movq $29, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L1702
.L1701:
.L1702:
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1711
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
    jz .L1721
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
    jmp .L1722
.L1721:
.L1722:
    jmp .L1712
.L1711:
.L1712:
    jmp .L1692
.L1691:
.L1692:
    jmp .L1672
.L1671:
.L1672:
    jmp .L1662
.L1661:
.L1662:
    movq -32(%rbp), %rax
    pushq %rax
    movq $179, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1731
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L1741
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
    jmp .L1742
.L1741:
.L1742:
    movq -256(%rbp), %rax
    pushq %rax
    movq $149, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1751
    movq $149, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1752
.L1751:
.L1752:
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
    jmp .L1732
.L1731:
.L1732:
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
    jz .L1761
    leaq .STR15(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1762
.L1761:
.L1762:
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
    jz .L1771
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
    jmp .L1772
.L1771:
.L1772:
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
    jz .L1781
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
    jz .L1791
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1792
.L1791:
.L1792:
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
    jz .L1801
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1802
.L1801:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L1802:
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
    jz .L1811
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
    jz .L1821
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1822
.L1821:
.L1822:
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
    jz .L1831
    movq -152(%rbp), %rax
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
    jmp .L1812
.L1811:
.L1812:
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
    jz .L1841
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -192(%rbp)
.L1851:    movq -192(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1852
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
    jz .L1861
    movq -192(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1862
.L1861:
.L1862:
    movq -184(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1871
    movq -192(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1872
.L1871:
.L1872:
    movq -184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L1851
.L1852:
    jmp .L1842
.L1841:
.L1842:
    jmp .L1782
.L1781:
.L1782:
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
    jz .L1881
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L1882
.L1881:
.L1882:
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
    jz .L1891
    movq -88(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_set_let_type
    jmp .L1892
.L1891:
.L1892:
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
    jz .L1901
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
    jz .L1911
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
    jmp .L1912
.L1911:
.L1912:
    movq -32(%rbp), %rax
    pushq %rax
    movq $138, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1921
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
    jmp .L1922
.L1921:
.L1922:
    movq -32(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1931
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
    jmp .L1932
.L1931:
.L1932:
    movq -32(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1941
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
    jmp .L1942
.L1941:
.L1942:
    movq -32(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1951
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
    jmp .L1952
.L1951:
.L1952:
    movq -32(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1961
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
    jmp .L1962
.L1961:
.L1962:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1971
    movq -32(%rbp), %rax
    pushq %rax
    movq $137, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1981
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
    jmp .L1982
.L1981:
.L1982:
    jmp .L1972
.L1971:
.L1972:
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
    jmp .L1902
.L1901:
.L1902:
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
    jz .L1991
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1992
.L1991:
.L1992:
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
    jz .L2001
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -40(%rbp)
    jmp .L2002
.L2001:
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
.L2002:
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
    jz .L2011
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2012
.L2011:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2012:
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
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2021
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -32(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
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
    call string_duplicate_parser
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
    jz .L2031
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2032
.L2031:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2032:
    jmp .L2022
.L2021:
.L2022:
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
    jz .L2041
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
    call string_duplicate_parser
    pushq %rax
    leaq -48(%rbp), %rbx
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
    jz .L2051
    movq -120(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2052
.L2051:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2052:
    jmp .L2042
.L2041:
.L2042:
    movq $0, %rax
    movq %rax, -136(%rbp)
    movq $0, %rax
    movq %rax, -144(%rbp)
    movq $0, %rax
    movq %rax, -152(%rbp)
    movq $0, %rax
    movq %rax, -160(%rbp)
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
    movq -104(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -184(%rbp)
.L2071:    movq -184(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2072
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -184(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2071
.L2072:
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -192(%rbp)
    movq $1, %rax
    movq %rax, -200(%rbp)
.L2081:    movq -200(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2082
    movq -160(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2091
    movq -168(%rbp), %rax
    movq %rax, -208(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -168(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -176(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -208(%rbp), %rax
    movq %rax, -216(%rbp)
.L2101:    movq -216(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2102
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -216(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2101
.L2102:
    jmp .L2092
.L2091:
.L2092:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -224(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call parser_handle_named_arg_capture
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -160(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -232(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2111
    movq $1, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2112
.L2111:
.L2112:
    movq -160(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
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
    call memory_get_integer@PLT
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2121
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
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2131
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2132
.L2131:
.L2132:
    jmp .L2122
.L2121:
    movq -256(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2141
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2142
.L2141:
    movq $0, %rax
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2142:
.L2122:
    jmp .L2081
.L2082:
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2062
.L2061:
.L2062:
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2151
    movq -144(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2161
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2162
.L2161:
.L2162:
    jmp .L2152
.L2151:
.L2152:
    movq $0, %rax
    movq %rax, -280(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2171
    movq $48, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $25, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -136(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -144(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L2172
.L2171:
    movq -160(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -144(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_attach_arg_names
.L2172:
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_peek_next_token_type
parser_peek_next_token_type:
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
    jz .L2181
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L2182
.L2181:
.L2182:
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
    jz .L2191
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
    jz .L2201
    movq $1, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2202
.L2201:
.L2202:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2211
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
    jz .L2221
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
    jz .L2231
    movq $1, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2232
.L2231:
.L2232:
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L2222
.L2221:
.L2222:
    jmp .L2212
.L2211:
.L2212:
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L2192
.L2191:
.L2192:
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
    jz .L2241
    movq $50, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2242
.L2241:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2242:
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
    jz .L2251
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2252
.L2251:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2252:
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
    jz .L2261
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -88(%rbp)
.L2271:    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2272
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
    jz .L2281
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
    jmp .L2282
.L2281:
    movq -104(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2291
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
    jmp .L2292
.L2291:
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2301
    movq $0, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2302
.L2301:
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2302:
.L2292:
.L2282:
    jmp .L2271
.L2272:
    jmp .L2262
.L2261:
.L2262:
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
    jz .L2311
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
.L2321:    movq -152(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2322
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
    jz .L2331
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2332
.L2331:
.L2332:
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2341
    movq $0, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2342
.L2341:
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
    jz .L2351
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2352
.L2351:
    movq $0, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2352:
.L2342:
    jmp .L2321
.L2322:
    jmp .L2312
.L2311:
.L2312:
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
    jz .L2361
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2362
.L2361:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2362:
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
    jz .L2371
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
    jz .L2381
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2382
.L2381:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
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
    jz .L2391
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
    jz .L2401
    movq -120(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2402
.L2401:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2402:
    jmp .L2392
.L2391:
.L2392:
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
    jz .L2411
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
    jmp .L2412
.L2411:
.L2412:
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
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq $0, %rax
    movq %rax, -184(%rbp)
    movq -104(%rbp), %rax
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
    movq $8, %rax
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -208(%rbp)
.L2431:    movq -208(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2432
    movq $0, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -208(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2431
.L2432:
    movq $8, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -216(%rbp)
    movq $1, %rax
    movq %rax, -224(%rbp)
    movq $0, %rax
    movq %rax, -232(%rbp)
.L2441:    movq -224(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2442
    movq -184(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2451
    movq -192(%rbp), %rax
    movq %rax, -240(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
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
    movq -200(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -240(%rbp), %rax
    movq %rax, -248(%rbp)
.L2461:    movq -248(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2462
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -248(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2461
.L2462:
    jmp .L2452
.L2451:
.L2452:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -256(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call parser_handle_named_arg_capture
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq $1, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2472
.L2471:
.L2472:
    movq -184(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -264(%rbp), %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -184(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
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
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2481
    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2491
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2492
.L2491:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
    movq $0, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2502
.L2501:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2502:
.L2492:
    jmp .L2482
.L2481:
    movq $0, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2482:
    jmp .L2441
.L2442:
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2422
.L2421:
.L2422:
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2511
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2521
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2522
.L2521:
.L2522:
    jmp .L2512
.L2511:
.L2512:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2531
    movq $48, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -304(%rbp)
    movq $25, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -184(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -168(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -304(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2532
.L2531:
.L2532:
    movq -184(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -312(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_attach_arg_names
    movq -312(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_parse_position_expression
parser_parse_position_expression:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    call parser_parse_expression
    movq %rax, -16(%rbp)
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
    movq %rax, -24(%rbp)
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq $28, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
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


.globl parser_parse_convert_expression
parser_parse_convert_expression:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $184, %rax
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
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2542
.L2541:
.L2542:
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
    movq $27, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -56(%rbp), %rax
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
    jz .L2551
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
    jmp .L2552
.L2551:
.L2552:
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
    jz .L2561
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2562
.L2561:
.L2562:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
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
    jz .L2581
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2582
.L2581:
.L2582:
    jmp .L2572
.L2571:
.L2572:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2591
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
    jmp .L2592
.L2591:
.L2592:
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
    jz .L2601
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2602
.L2601:
.L2602:
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
.L2611:    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2612
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
    jz .L2621
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2622
.L2621:
.L2622:
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2631
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2632
.L2631:
.L2632:
    movq -120(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2642
.L2641:
.L2642:
    movq -120(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2652
.L2651:
.L2652:
    movq -120(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2662
.L2661:
.L2662:
    movq -120(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2671
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2672
.L2671:
.L2672:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2681
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2682
.L2681:
.L2682:
    movq -120(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2691
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2692
.L2691:
.L2692:
    movq -120(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2702
.L2701:
.L2702:
    movq -120(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2711
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2712
.L2711:
.L2712:
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2721
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2722
.L2721:
    movq -88(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2731
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
    jmp .L2732
.L2731:
.L2732:
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
    jz .L2741
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
    jz .L2751
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2752
.L2751:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L2752:
    jmp .L2742
.L2741:
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2742:
.L2722:
    jmp .L2611
.L2612:
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
    jz .L2761
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
    jz .L2771
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
    jz .L2781
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2791
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
    jz .L2801
    movq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2802
.L2801:
.L2802:
    jmp .L2792
.L2791:
.L2792:
    jmp .L2782
.L2781:
.L2782:
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L2772
.L2771:
.L2772:
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
    jz .L2811
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
    jmp .L2812
.L2811:
.L2812:
    jmp .L2762
.L2761:
.L2762:
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
    jz .L2821
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2822
.L2821:
.L2822:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2831
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
    jz .L2841
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2842
.L2841:
.L2842:
    jmp .L2832
.L2831:
.L2832:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2851
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
    jmp .L2852
.L2851:
.L2852:
    movq -32(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2861
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L2862
.L2861:
.L2862:
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
.L2871:    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2872
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
    jz .L2881
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2882
.L2881:
.L2882:
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2891
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2892
.L2891:
.L2892:
    movq -120(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2901
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2902
.L2901:
.L2902:
    movq -120(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2911
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2912
.L2911:
.L2912:
    movq -120(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2921
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2922
.L2921:
.L2922:
    movq -120(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2931
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2932
.L2931:
.L2932:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2941
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2942
.L2941:
.L2942:
    movq -120(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2951
    movq $1, %rax
    pushq %rax
    leaq -128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2952
.L2951:
.L2952:
    movq -128(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2961
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2962
.L2961:
    movq -96(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2971
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
    jmp .L2972
.L2971:
.L2972:
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
    jz .L2981
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
    jmp .L2982
.L2981:
.L2982:
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
    jz .L2991
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
    jz .L3001
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3002
.L3001:
.L3002:
    jmp .L2992
.L2991:
    movq -192(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3011
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L3012
.L3011:
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L3012:
.L2992:
.L2962:
    jmp .L2871
.L2872:
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
    jz .L3021
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
    jz .L3031
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
    jz .L3041
    movq $1, %rax
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3042
.L3041:
.L3042:
    movq -288(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3051
    movq -296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3061
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
    jz .L3071
    movq $1, %rax
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3072
.L3071:
.L3072:
    jmp .L3062
.L3061:
.L3062:
    jmp .L3052
.L3051:
.L3052:
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L3032
.L3031:
.L3032:
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
    jz .L3081
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
    jmp .L3082
.L3081:
.L3082:
    jmp .L3022
.L3021:
.L3022:
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
    jz .L3091
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3092
.L3091:
    movq -8(%rbp), %rax
    pushq %rax
    movq $55, %rax
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
    movq $57, %rax
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
    movq $58, %rax
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
    movq $59, %rax
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
    movq $60, %rax
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
    movq $61, %rax
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
    movq $62, %rax
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
    movq $63, %rax
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
    movq $64, %rax
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
    movq $65, %rax
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
    movq $66, %rax
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
    movq $67, %rax
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
    movq $68, %rax
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
    movq $69, %rax
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
    movq $70, %rax
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
    movq $71, %rax
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
    movq $72, %rax
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
    movq $73, %rax
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
    movq $74, %rax
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
    movq $75, %rax
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
    movq $76, %rax
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
    movq $77, %rax
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
    movq $78, %rax
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
    movq $79, %rax
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
    movq $80, %rax
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
    movq $81, %rax
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
    movq $82, %rax
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
    movq $83, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $84, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3381
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3382
.L3381:
    movq -8(%rbp), %rax
    pushq %rax
    movq $85, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $86, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3401
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3402
.L3401:
    movq -8(%rbp), %rax
    pushq %rax
    movq $87, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3411
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3412
.L3411:
    movq -8(%rbp), %rax
    pushq %rax
    movq $88, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3421
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3422
.L3421:
    movq -8(%rbp), %rax
    pushq %rax
    movq $89, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3431
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3432
.L3431:
    movq -8(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3441
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3442
.L3441:
    movq -8(%rbp), %rax
    pushq %rax
    movq $91, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3451
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3452
.L3451:
    movq -8(%rbp), %rax
    pushq %rax
    movq $92, %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    movq $93, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3471
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3472
.L3471:
    movq -8(%rbp), %rax
    pushq %rax
    movq $94, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3481
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3482
.L3481:
    movq -8(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3491
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3492
.L3491:
    movq -8(%rbp), %rax
    pushq %rax
    movq $96, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3501
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3502
.L3501:
    movq -8(%rbp), %rax
    pushq %rax
    movq $97, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3511
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3512
.L3511:
    movq -8(%rbp), %rax
    pushq %rax
    movq $98, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3521
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3522
.L3521:
    movq -8(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3531
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3532
.L3531:
    movq -8(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3541
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3542
.L3541:
    movq -8(%rbp), %rax
    pushq %rax
    movq $101, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3551
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3552
.L3551:
    movq -8(%rbp), %rax
    pushq %rax
    movq $102, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3561
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3562
.L3561:
    movq -8(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3571
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3572
.L3571:
    movq -8(%rbp), %rax
    pushq %rax
    movq $104, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3581
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3582
.L3581:
    movq -8(%rbp), %rax
    pushq %rax
    movq $105, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3591
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3592
.L3591:
    movq -8(%rbp), %rax
    pushq %rax
    movq $106, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3601
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3602
.L3601:
    movq -8(%rbp), %rax
    pushq %rax
    movq $107, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3611
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3612
.L3611:
    movq -8(%rbp), %rax
    pushq %rax
    movq $108, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3621
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3622
.L3621:
    movq -8(%rbp), %rax
    pushq %rax
    movq $109, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3631
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3632
.L3631:
    movq -8(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3641
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3642
.L3641:
    movq -8(%rbp), %rax
    pushq %rax
    movq $115, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3651
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3652
.L3651:
    movq -8(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3661
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3662
.L3661:
    movq -8(%rbp), %rax
    pushq %rax
    movq $117, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3671
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3672
.L3671:
    movq -8(%rbp), %rax
    pushq %rax
    movq $118, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3681
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3682
.L3681:
    movq -8(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3691
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3692
.L3691:
    movq -8(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3701
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3702
.L3701:
    movq -8(%rbp), %rax
    pushq %rax
    movq $130, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3711
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3712
.L3711:
    movq -8(%rbp), %rax
    pushq %rax
    movq $131, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3721
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3722
.L3721:
.L3722:
.L3712:
.L3702:
.L3692:
.L3682:
.L3672:
.L3662:
.L3652:
.L3642:
.L3632:
.L3622:
.L3612:
.L3602:
.L3592:
.L3582:
.L3572:
.L3562:
.L3552:
.L3542:
.L3532:
.L3522:
.L3512:
.L3502:
.L3492:
.L3482:
.L3472:
.L3462:
.L3452:
.L3442:
.L3432:
.L3422:
.L3412:
.L3402:
.L3392:
.L3382:
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
    movq $0, %rax  # Load constant EXPR_INTEGER
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
    movq $1, %rax  # Load constant EXPR_VARIABLE
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
    movq $2, %rax  # Load constant EXPR_BINARY_OP
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
    movq $3, %rax  # Load constant EXPR_COMPARISON
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
    movq $40, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -40(%rbp)
    movq $4, %rax  # Load constant EXPR_FUNCTION_CALL
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
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl expression_attach_arg_names
expression_attach_arg_names:
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
    jz .L3731
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3732
.L3731:
.L3732:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3741
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3742
.L3741:
.L3742:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
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
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3751
    movq -16(%rbp), %rax
    pushq %rax
    movq $32, %rax
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
    jmp .L3752
.L3751:
.L3752:
    movq -24(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3761
    movq -16(%rbp), %rax
    pushq %rax
    movq $40, %rax
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
    jmp .L3762
.L3761:
.L3762:
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
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
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl parser_handle_named_arg_capture
parser_handle_named_arg_capture:
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
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3771
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3772
.L3771:
.L3772:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3781
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3782
.L3781:
.L3782:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3791
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3792
.L3791:
.L3792:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3801
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3802
.L3801:
.L3802:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
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
    movq $5, %rax  # Load constant EXPR_STRING_LITERAL
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
.L3811:    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3812
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
    jz .L3821
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3822
.L3821:
.L3822:
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3811
.L3812:
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
.L3831:    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3832
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
    jz .L3841
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3842
.L3841:
.L3842:
    movq -48(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3831
.L3832:
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3851
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
    jz .L3861
    movq -40(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3862
.L3861:
.L3862:
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
.L3871:    movq -88(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3872
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
    jmp .L3871
.L3872:
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3881
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3882
.L3881:
.L3882:
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
    jmp .L3852
.L3851:
.L3852:
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
    jz .L3891
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3892
.L3891:
.L3892:
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
    jz .L3901
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
    jz .L3911
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call lambda_add_free_var
    jmp .L3912
.L3911:
.L3912:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3902
.L3901:
.L3902:
    movq -40(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3921
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
    jmp .L3922
.L3921:
.L3922:
    movq -40(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3931
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
.L3941:    movq -96(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3942
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
    jmp .L3941
.L3942:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3932
.L3931:
.L3932:
    movq -40(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3951
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
    jmp .L3952
.L3951:
.L3952:
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3961
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
    jmp .L3962
.L3961:
.L3962:
    movq -40(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3971
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
.L3981:    movq -96(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3982
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
    jmp .L3981
.L3982:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3972
.L3971:
.L3972:
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
    movq $23, %rax  # Load constant EXPR_LAMBDA
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
    movq $23, %rax  # Load constant EXPR_LAMBDA
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
    movq $40, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -32(%rbp)
    movq $1, %rax  # Load constant STMT_LET
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
    movq $0, %rax
    pushq %rax
    movq $32, %rax
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
    jz .L3991
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3992
.L3991:
.L3992:
    movq -16(%rbp), %rax
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


.globl statement_set_let_constant
statement_set_let_constant:
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
    jz .L4011
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4012
.L4011:
.L4012:
    movq $1, %rax
    pushq %rax
    movq $32, %rax
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


.globl parser_parse_local_constant_statement
parser_parse_local_constant_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $164, %rax
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
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4021
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4022
.L4021:
.L4022:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4031
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L4032
.L4031:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L4032:
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call statement_create_let
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_set_let_constant
    movq -80(%rbp), %rax
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
    movq $2, %rax  # Load constant STMT_SET
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
    movq $17, %rax  # Load constant STMT_COMPOUND_ASSIGN
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
    movq $11, %rax  # Load constant STMT_FOR
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
    movq %r8, -40(%rbp)
    movq $48, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -56(%rbp)
    movq $12, %rax  # Load constant STMT_FOR_EACH
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
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -56(%rbp), %rax
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
    movq $3, %rax  # Load constant STMT_RETURN
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
    movq $4, %rax  # Load constant STMT_PRINT
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
    movq $7, %rax  # Load constant STMT_EXPRESSION
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
    movq $5, %rax  # Load constant STMT_IF
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
    movq $6, %rax  # Load constant STMT_WHILE
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
    movq $9, %rax  # Load constant STMT_BREAK
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
    movq $10, %rax  # Load constant STMT_CONTINUE
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
    movq $56, %rax
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
    movq $0, %rax
    pushq %rax
    movq $48, %rax
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


.globl function_set_source_file
function_set_source_file:
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
    jz .L4041
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4042
.L4041:
.L4042:
    movq -16(%rbp), %rax
    pushq %rax
    movq $48, %rax  # Load constant FUNCTION_SOURCE_FILE_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl function_get_source_file
function_get_source_file:
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
    jz .L4051
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4052
.L4051:
.L4052:
    movq $48, %rax  # Load constant FUNCTION_SOURCE_FILE_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rbp, %rsp
    popq %rbp
    ret


.globl type_definition_set_source_file
type_definition_set_source_file:
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
    jz .L4061
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4062
.L4061:
.L4062:
    movq -16(%rbp), %rax
    pushq %rax
    movq $48, %rax  # Load constant TYPEDEFINITION_SOURCE_FILE_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl type_definition_get_source_file
type_definition_get_source_file:
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
    jz .L4071
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4072
.L4071:
.L4072:
    movq $48, %rax  # Load constant TYPEDEFINITION_SOURCE_FILE_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
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
    jz .L4081
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4091
    movq $128, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4092
.L4091:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4092:
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
    jmp .L4082
.L4081:
.L4082:
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
    jz .L4101
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4111
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4112
.L4111:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4112:
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
    jmp .L4102
.L4101:
.L4102:
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
    jz .L4121
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4131
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4132
.L4131:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4132:
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
    jmp .L4122
.L4121:
.L4122:
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
    jz .L4141
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4151
    movq $4, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4152
.L4151:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4152:
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
    jmp .L4142
.L4141:
.L4142:
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
    jz .L4161
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4162
.L4161:
.L4162:
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
    jz .L4171
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4172
.L4171:
.L4172:
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
    jz .L4181
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4182
.L4181:
.L4182:
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
    jz .L4191
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4192
.L4191:
.L4192:
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
    jz .L4201
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4202
.L4201:
.L4202:
    leaq .STR33(%rip), %rax
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
    jz .L4211
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4212
.L4211:
.L4212:
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
    jz .L4221
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4222
.L4221:
.L4222:
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
    jz .L4231
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4232
.L4231:
.L4232:
    movq $0, %rax
    movq %rax, -48(%rbp)
.L4241:    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4242
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
    jz .L4251
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
    jz .L4261
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
    jmp .L4262
.L4261:
.L4262:
    jmp .L4252
.L4251:
.L4252:
    movq -48(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4241
.L4242:
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
    jz .L4271
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4272
.L4271:
.L4272:
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
    jz .L4281
    leaq .STR35(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4282
.L4281:
.L4282:
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
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4291
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4301
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4302
.L4301:
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4302:
    movq $14, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4292
.L4291:
.L4292:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4311
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
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
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4321
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
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
    jz .L4341
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4342
.L4341:
.L4342:
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -88(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_lookup_type_size
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4332
.L4331:
.L4332:
    leaq .STR38(%rip), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4351
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
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4361
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_position_expression
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4362
.L4361:
.L4362:
    leaq .STR38(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4352
.L4351:
.L4352:
    jmp .L4322
.L4321:
.L4322:
    jmp .L4312
.L4311:
.L4312:
    movq -24(%rbp), %rax
    pushq %rax
    movq $155, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4371
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
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
    movq %rax, -136(%rbp)
    movq $0, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -144(%rbp)
    movq $8, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq $0, %rax
    movq %rax, -160(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $159, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4381
    movq $1, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4382
.L4381:
.L4382:
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4391
    leaq .STR39(%rip), %rax
    pushq %rax
    movq -152(%rbp), %rax
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
    jz .L4401
    movq $1, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4402
.L4401:
.L4402:
    jmp .L4392
.L4391:
.L4392:
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4411
    movq -144(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_a_list_literal
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4412
.L4411:
.L4412:
    movq $0, %rax
    movq %rax, -168(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4421
    leaq .STR40(%rip), %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4422
.L4421:
.L4422:
    movq -168(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4431
    movq -144(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_a_dictionary_literal
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4432
.L4431:
.L4432:
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4441
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4442
.L4441:
.L4442:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4451
    movq -144(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_a_value_of_type
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4452
.L4451:
.L4452:
    leaq .STR42(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4372
.L4371:
.L4372:
    movq -24(%rbp), %rax
    pushq %rax
    movq $171, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4461
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_proc_expression
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4462
.L4461:
.L4462:
    movq -24(%rbp), %rax
    pushq %rax
    movq $184, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4471
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_convert_expression
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4472
.L4471:
.L4472:
    movq -24(%rbp), %rax
    pushq %rax
    movq $168, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4481
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
    movq %rax, -184(%rbp)
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
    movq %rax, -192(%rbp)
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
    movq %rax, -200(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    leaq .STR43(%rip), %rax
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
    jmp .L4482
.L4481:
.L4482:
    movq -24(%rbp), %rax
    pushq %rax
    movq $170, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4491
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
    movq %rax, -208(%rbp)
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
    movq %rax, -216(%rbp)
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
    movq %rax, -224(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -216(%rbp), %rax
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
    leaq .STR44(%rip), %rax
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
    jmp .L4492
.L4491:
.L4492:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4501
    movq -24(%rbp), %rax
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -248(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -256(%rbp)
    movq $0, %rax
    movq %rax, -264(%rbp)
    movq $0, %rax
    movq %rax, -272(%rbp)
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
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4511
    movq $2, %rax
    movq %rax, -296(%rbp)
    movq $8, %rax
    movq %rax, -304(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -320(%rbp)
.L4521:    movq -320(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4522
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
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
    call memory_get_integer@PLT
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4531
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -344(%rbp)
    jmp .L4532
.L4531:
.L4532:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -352(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4541
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4542
.L4541:
.L4542:
    movq -272(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -368(%rbp)
    movq -264(%rbp), %rax
    addq -368(%rbp), %rax
    movq %rax, -376(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq $0, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4551
    movq $0, %rax
    pushq %rax
    leaq -320(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4552
.L4551:
.L4552:
    jmp .L4521
.L4522:
    jmp .L4512
.L4511:
.L4512:
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -400(%rbp)
    movq $32, %rax
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -416(%rbp)
    movq $8, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -240(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -264(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4502
.L4501:
.L4502:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4561
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -424(%rbp)
    movq -424(%rbp), %rax
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
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4562
.L4561:
.L4562:
    movq -24(%rbp), %rax
    pushq %rax
    movq $186, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4571
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -448(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_float
    movq %rax, -456(%rbp)
    movq $186, %rax
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
    movq %rax, -464(%rbp)
    movq $29, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -456(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -464(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4572
.L4571:
.L4572:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4581
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
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
    popq %rdi
    call string_duplicate_parser
    movq %rax, -472(%rbp)
    movq $0, %rax
    movq %rax, -480(%rbp)
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4591
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -496(%rbp)
    movq $16, %rax  # Load constant PROGRAM_TYPES
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq $0, %rax
    movq %rax, -512(%rbp)
.L4601:    movq -512(%rbp), %rax
    pushq %rax
    movq -496(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4602
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -512(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -504(%rbp), %rax
    addq -368(%rbp), %rax
    movq %rax, -520(%rbp)
    movq $0, %rax
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -528(%rbp)
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -536(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -544(%rbp)
    movq -544(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4611
    movq $1, %rax
    pushq %rax
    leaq -480(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -496(%rbp), %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4612
.L4611:
    movq -512(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4612:
    jmp .L4601
.L4602:
    jmp .L4592
.L4591:
.L4592:
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -552(%rbp)
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4621
    movq $32, %rax
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $7, %rax  # Load constant EXPR_TYPE_NAME
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -472(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4622
.L4621:
    movq -472(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_string_literal_owned
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4622:
    jmp .L4582
.L4581:
.L4582:
    movq -24(%rbp), %rax
    pushq %rax
    movq $157, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4631
    movq $157, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -560(%rbp)
    movq $8, %rax
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
    movq -576(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4641
    leaq .STR45(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -584(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4642
.L4641:
.L4642:
    movq $8, %rax
    pushq %rax
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -592(%rbp)
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -600(%rbp)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -608(%rbp)
    movq $32, %rax
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $10, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -600(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4632
.L4631:
.L4632:
    movq -24(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4651
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
    movq %rax, -616(%rbp)
    movq $49, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -616(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4652
.L4651:
.L4652:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4661
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
    movq %rax, -624(%rbp)
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -632(%rbp)
    movq -624(%rbp), %rax
    pushq %rax
    movq $17, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    movq %rax, -640(%rbp)
    movq -640(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4662
.L4661:
.L4662:
    movq -24(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4671
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
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
    pushq %rax
    movq $29, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call expression_create_unary_op
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4672
.L4671:
.L4672:
    movq -24(%rbp), %rax
    pushq %rax
    movq $151, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4681
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -656(%rbp)
    movq $151, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -664(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -664(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4691
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
    movq %rax, -680(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -688(%rbp)
    movq -680(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    leaq .STR46(%rip), %rax
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
    jmp .L4692
.L4691:
    leaq .STR47(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
.L4692:
    jmp .L4682
.L4681:
.L4682:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4701
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -696(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -704(%rbp)
    movq $0, %rax
    movq %rax, -712(%rbp)
    movq -704(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4711
    leaq .STR48(%rip), %rax
    pushq %rax
    movq -704(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -712(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4712
.L4711:
.L4712:
    movq -712(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4721
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -720(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -728(%rbp)
    movq -728(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4731
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -736(%rbp)
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -744(%rbp)
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -752(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -752(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -760(%rbp)
    movq $0, %rax
    movq %rax, -768(%rbp)
    movq $0, %rax
    movq %rax, -776(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4741
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax
    movq %rax, -784(%rbp)
    movq -784(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -792(%rbp)
.L4751:    movq -792(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4752
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -800(%rbp)
    movq -800(%rbp), %rax
    pushq %rax
    movq -776(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -768(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -776(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -776(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -808(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -816(%rbp)
    movq -816(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4761
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_struct_field_after_comma
    movq %rax, -824(%rbp)
    movq -824(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4771
    movq $0, %rax
    pushq %rax
    leaq -792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4772
.L4771:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L4772:
    jmp .L4762
.L4761:
    movq $0, %rax
    pushq %rax
    leaq -792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L4762:
    jmp .L4751
.L4752:
    jmp .L4742
.L4741:
.L4742:
    movq -776(%rbp), %rax
    pushq %rax
    movq -768(%rbp), %rax
    pushq %rax
    movq -744(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4732
.L4731:
.L4732:
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
    jmp .L4722
.L4721:
.L4722:
    jmp .L4702
.L4701:
.L4702:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4781
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -832(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -832(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -840(%rbp)
    movq $0, %rax
    movq %rax, -848(%rbp)
    movq -840(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4791
    leaq .STR49(%rip), %rax
    pushq %rax
    movq -840(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -848(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4792
.L4791:
.L4792:
    movq -848(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4801
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -856(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -856(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -864(%rbp)
    movq -864(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4811
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
    movq %rax, -872(%rbp)
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -880(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -888(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4821
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
    movq %rax, -896(%rbp)
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
    movq %rax, -904(%rbp)
    movq $24, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -912(%rbp)
    movq -872(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -912(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -912(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -904(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -912(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -912(%rbp), %rax
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
    jmp .L4822
.L4821:
.L4822:
    movq -872(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4812
.L4811:
.L4812:
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
    jmp .L4802
.L4801:
.L4802:
    jmp .L4782
.L4781:
.L4782:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4831
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -920(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -920(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -928(%rbp)
    movq $0, %rax
    movq %rax, -936(%rbp)
    movq -928(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4841
    leaq .STR51(%rip), %rax
    pushq %rax
    movq -928(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -936(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4842
.L4841:
.L4842:
    movq -936(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4851
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -944(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -944(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -952(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -944(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -960(%rbp)
    movq $0, %rax
    movq %rax, -968(%rbp)
    movq -960(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4861
    leaq .STR52(%rip), %rax
    pushq %rax
    movq -960(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -968(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L4862
.L4861:
.L4862:
    movq -968(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4871
    movq -952(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -976(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -976(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -984(%rbp)
    movq -984(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4881
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
    movq %rax, -992(%rbp)
    movq $8, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -1000(%rbp)
    movq -992(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1000(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq -1000(%rbp), %rax
    pushq %rax
    leaq .STR53(%rip), %rax
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
    jmp .L4882
.L4881:
.L4882:
    leaq .STR52(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4872
.L4871:
.L4872:
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4852
.L4851:
.L4852:
    jmp .L4832
.L4831:
.L4832:
    movq -24(%rbp), %rax
    pushq %rax
    movq $175, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4891
    movq $175, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1008(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -1008(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1016(%rbp)
    movq -1016(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4901
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
    movq %rax, -1024(%rbp)
    movq $0, %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    movq %rax, -1032(%rbp)
    movq -1032(%rbp), %rax
    pushq %rax
    movq $41, %rax
    pushq %rax
    movq -1024(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_binary_op
    movq %rax, -1040(%rbp)
    movq -1040(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4902
.L4901:
.L4902:
    jmp .L4892
.L4891:
.L4892:
    movq -24(%rbp), %rax
    pushq %rax
    movq $158, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4911
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
    jz .L4921
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
    movq %rax, -1048(%rbp)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4922
.L4921:
.L4922:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1056(%rbp)
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1064(%rbp)
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
    jz .L4931
    leaq .STR55(%rip), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L4932
.L4931:
.L4932:
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
    movq %rax, -1072(%rbp)
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1080(%rbp)
    movq $6, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1080(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1072(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1080(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1064(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1080(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1080(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4912
.L4911:
.L4912:
    movq -24(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4941
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
    leaq .STR42(%rip), %rax
    pushq %rax
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1088(%rbp)
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1096(%rbp)
    movq -1088(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4951
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1112(%rbp)
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
    jz .L4961
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1120(%rbp)
    leaq .STR39(%rip), %rax
    pushq %rax
    movq -1120(%rbp), %rax
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
    jz .L4971
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
    jz .L4981
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L4982
.L4981:
.L4982:
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1136(%rbp)
    movq $0, %rax
    movq %rax, -1144(%rbp)
    movq $4, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -1152(%rbp)
    movq -1152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1160(%rbp)
.L4991:    movq -1160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4992
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
    jz .L5001
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
    jz .L5011
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5012
.L5011:
.L5012:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -1168(%rbp)
    movq -1144(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5021
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5022
.L5021:
.L5022:
    movq -1144(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1136(%rbp), %rax
    addq -368(%rbp), %rax
    movq %rax, -1176(%rbp)
    movq -1168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5002
.L5001:
    movq $0, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5002:
    jmp .L4991
.L4992:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1184(%rbp)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1136(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1184(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4972
.L4971:
    leaq .STR58(%rip), %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1192(%rbp)
    movq -1192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5031
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
    jz .L5041
    leaq .STR59(%rip), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5042
.L5041:
.L5042:
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5051:    movq -1160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5052
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
    jz .L5061
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
    jz .L5071
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5072
.L5071:
.L5072:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1144(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5081
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5082
.L5081:
.L5082:
    movq -1144(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1136(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -1176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5062
.L5061:
    movq $0, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5062:
    jmp .L5051
.L5052:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1200(%rbp)
    movq $21, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1136(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1200(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5032
.L5031:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1208(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5091
    movq $24, %rax
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -504(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1216(%rbp)
.L5101:    movq -1216(%rbp), %rax
    pushq %rax
    movq -496(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5102
    movq -1216(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1224(%rbp)
    movq -1224(%rbp), %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1120(%rbp), %rax
    pushq %rax
    movq -536(%rbp), %rax
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
    jz .L5111
    movq $1, %rax
    pushq %rax
    leaq -1208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -496(%rbp), %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5112
.L5111:
.L5112:
    movq -1216(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5101
.L5102:
    jmp .L5092
.L5091:
.L5092:
    movq -1208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5121
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1232(%rbp)
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
    jz .L5131
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5132
.L5131:
.L5132:
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1240(%rbp)
    movq $0, %rax
    movq %rax, -1248(%rbp)
    movq $0, %rax
    movq %rax, -1256(%rbp)
    movq $4, %rax
    movq %rax, -1264(%rbp)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1272(%rbp)
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1272(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1280(%rbp)
.L5141:    movq -1280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5142
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
    jz .L5151
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5152
.L5151:
.L5152:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1288(%rbp)
    movq -1288(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -1064(%rbp), %rbx
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
    movq %rax, -1296(%rbp)
    movq -1256(%rbp), %rax
    pushq %rax
    movq -1264(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5161
    movq -1264(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1304(%rbp)
    movq -1304(%rbp), %rax
    pushq %rax
    movq -1240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1304(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5162
.L5161:
.L5162:
    movq -1256(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1312(%rbp)
    movq -1240(%rbp), %rax
    addq -1312(%rbp), %rax
    movq %rax, -1320(%rbp)
    movq -1248(%rbp), %rax
    addq -1312(%rbp), %rax
    movq %rax, -1328(%rbp)
    movq -1064(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
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
    jz .L5171
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5172
.L5171:
    movq $0, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5172:
    jmp .L5141
.L5142:
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1336(%rbp)
    movq $20, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1232(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1240(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1248(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -1336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1336(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5122
.L5121:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1344(%rbp)
    movq $97, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -1344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -1344(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1352(%rbp)
    movq -1352(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5122:
.L5032:
.L4972:
    jmp .L4962
.L4961:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1360(%rbp)
    movq $97, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -1360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -1360(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1368(%rbp)
    movq -1368(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L4962:
    jmp .L4952
.L4951:
.L4952:
    movq -1096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5181
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
    jz .L5191
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR62(%rip), %rax
    pushq %rax
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1376(%rbp)
    movq -1376(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5201
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
    jz .L5211
    leaq .STR63(%rip), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5212
.L5211:
.L5212:
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
    jz .L5221
    leaq .STR64(%rip), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5222
.L5221:
.L5222:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1384(%rbp)
    movq -1384(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -1392(%rbp)
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
    jz .L5231
    leaq .STR65(%rip), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5232
.L5231:
.L5232:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1400(%rbp)
    movq -1400(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1408(%rbp)
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
    jz .L5241
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5251:    movq -1160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5252
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
    jz .L5261
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
    jz .L5271
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5272
.L5271:
.L5272:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1144(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5281
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5282
.L5281:
.L5282:
    movq -1144(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1136(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -1176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5262
.L5261:
    movq $0, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5262:
    jmp .L5251
.L5252:
    movq -1144(%rbp), %rax
    pushq %rax
    movq -1392(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5291
    leaq .STR66(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -1392(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR67(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -1144(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR68(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5292
.L5291:
.L5292:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1416(%rbp)
    movq $18, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1136(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1392(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5242
.L5241:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1424(%rbp)
    movq $19, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1392(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -1408(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1424(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5242:
    jmp .L5202
.L5201:
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1432(%rbp)
    movq -1432(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1440(%rbp)
    movq -1440(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5202:
    jmp .L5192
.L5191:
    movq -1056(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1448(%rbp)
    movq -1448(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    movq %rax, -1456(%rbp)
    movq -1456(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5192:
    jmp .L5182
.L5181:
.L5182:
    jmp .L4942
.L4941:
.L4942:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -1464(%rbp)
    movq -1464(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5301
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
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
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1472(%rbp)
    leaq .STR39(%rip), %rax
    pushq %rax
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1480(%rbp)
    movq -1480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5311
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
    movq %rax, -1488(%rbp)
    movq -1488(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5321
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5331:    movq -1160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5332
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
    jz .L5341
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
    jz .L5351
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5352
.L5351:
.L5352:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1144(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5361
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5362
.L5361:
.L5362:
    movq -1144(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1136(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -1176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5342
.L5341:
    movq $0, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5342:
    jmp .L5331
.L5332:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $17, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1136(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1184(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5322
.L5321:
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -1352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1352(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5322:
    jmp .L5312
.L5311:
.L5312:
    leaq .STR58(%rip), %rax
    pushq %rax
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1496(%rbp)
    movq -1496(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5371
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
    leaq -1488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1488(%rbp), %rax
    pushq %rax
    movq $156, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5381
    movq $156, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5391:    movq -1160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5392
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
    jz .L5401
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
    jz .L5411
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5412
.L5411:
.L5412:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -1168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1144(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5421
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5422
.L5421:
.L5422:
    movq -1144(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1136(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -1176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5402
.L5401:
    movq $0, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5402:
    jmp .L5391
.L5392:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $21, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1136(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1144(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1200(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5382
.L5381:
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -1352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1352(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5382:
    jmp .L5372
.L5371:
.L5372:
    leaq .STR40(%rip), %rax
    pushq %rax
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -1504(%rbp)
    movq -1504(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5431
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
    leaq -1488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1488(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5441
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
    jz .L5451
    leaq .STR69(%rip), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5452
.L5451:
.L5452:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -1512(%rbp)
    movq $0, %rax
    movq %rax, -1520(%rbp)
    movq $0, %rax
    movq %rax, -1528(%rbp)
    movq $4, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    movq %rax, -1536(%rbp)
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
    jz .L5461
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5462
.L5461:
.L5462:
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
    movq %rax, -1544(%rbp)
    movq -1536(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1544(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -1528(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5471:    movq -1160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5472
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
    jz .L5481
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
    movq %rax, -1552(%rbp)
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
    jz .L5491
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L5492
.L5491:
.L5492:
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
    movq %rax, -1560(%rbp)
    movq -1528(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5501
    movq -296(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -296(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -1520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5502
.L5501:
.L5502:
    movq -1528(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1512(%rbp), %rax
    addq -368(%rbp), %rax
    movq %rax, -1568(%rbp)
    movq -1520(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -1328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1552(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1568(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1560(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1328(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1528(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1528(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5482
.L5481:
    movq $0, %rax
    pushq %rax
    leaq -1160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5482:
    jmp .L5471
.L5472:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -1576(%rbp)
    movq $22, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -1576(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1512(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -1576(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1520(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -1576(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1528(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -1576(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1576(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5442
.L5441:
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -1352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1352(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L5442:
    jmp .L5432
.L5431:
.L5432:
    movq $0, %rax
    pushq %rax
    leaq -480(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5511
    jmp .L5512
.L5511:
.L5512:
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5521
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -496(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5531
    jmp .L5532
.L5531:
.L5532:
    movq $16, %rax  # Load constant PROGRAM_TYPES
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -504(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -504(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5541
    jmp .L5542
.L5541:
.L5542:
    movq $0, %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1584(%rbp)
.L5551:    movq -1584(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5552
    movq $0, %rax
    movq %rax, -1592(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq -496(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5561
    movq $1, %rax
    pushq %rax
    leaq -1592(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5562
.L5561:
.L5562:
    movq -1592(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5571
    movq $0, %rax
    pushq %rax
    leaq -1584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5572
.L5571:
.L5572:
    movq -1592(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5581
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -512(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -504(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -528(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1472(%rbp), %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -544(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -544(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5591
    movq $1, %rax
    pushq %rax
    leaq -480(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5592
.L5591:
.L5592:
    movq -512(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5582
.L5581:
.L5582:
    jmp .L5551
.L5552:
    jmp .L5522
.L5521:
.L5522:
    movq $0, %rax
    movq %rax, -1600(%rbp)
    movq $0, %rax
    movq %rax, -1608(%rbp)
    movq -480(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5601
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5611
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax  # Load constant PROGRAM_TYPES
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -504(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1616(%rbp)
.L5621:    movq -1616(%rbp), %rax
    pushq %rax
    movq -496(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5622
    movq -1616(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -504(%rbp), %rax
    addq -1224(%rbp), %rax
    pushq %rax
    leaq -520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -528(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax  # Load constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1624(%rbp)
    movq -1624(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant TYPE_KIND_VARIANT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5631
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1632(%rbp)
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1640(%rbp)
    movq $0, %rax
    movq %rax, -1648(%rbp)
.L5641:    movq -1648(%rbp), %rax
    pushq %rax
    movq -1632(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5642
    movq -1648(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1656(%rbp)
    movq -1640(%rbp), %rax
    addq -1656(%rbp), %rax
    movq %rax, -1664(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1664(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1672(%rbp)
    movq -1472(%rbp), %rax
    pushq %rax
    movq -1672(%rbp), %rax
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
    jz .L5651
    movq $1, %rax
    pushq %rax
    leaq -1600(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1680(%rbp)
    movq -1680(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -1608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -496(%rbp), %rax
    pushq %rax
    leaq -1616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1632(%rbp), %rax
    pushq %rax
    leaq -1648(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5652
.L5651:
.L5652:
    movq -1648(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1648(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5641
.L5642:
    jmp .L5632
.L5631:
.L5632:
    movq -1616(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1616(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5621
.L5622:
    jmp .L5612
.L5611:
.L5612:
    jmp .L5602
.L5601:
.L5602:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -1688(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1696(%rbp)
    movq -1696(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5661
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
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5671
    movq -480(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5681
    movq $0, %rax
    pushq %rax
    leaq -1704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5682
.L5681:
.L5682:
    jmp .L5672
.L5671:
.L5672:
    movq -1704(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5691
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
    movq %rax, -1712(%rbp)
    movq -1712(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5701
    leaq .STR70(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5702
.L5701:
.L5702:
    movq $0, %rax
    pushq %rax
    movq -1712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1720(%rbp)
    movq -1720(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -1728(%rbp)
    movq -1728(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5711
    movq -1720(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5721
    leaq .STR70(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5722
.L5721:
.L5722:
    jmp .L5712
.L5711:
.L5712:
    movq $8, %rax
    pushq %rax
    movq -1712(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -1736(%rbp)
    movq -1720(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $40, %rax
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $9, %rax  # Load constant EXPR_VARIANT_CONSTRUCTOR
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1736(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
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
    movq %rax, -1744(%rbp)
    movq -1744(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5731
    movq $0, %rax
    pushq %rax
    movq -1744(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1752(%rbp)
    movq -1752(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5741
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5751:    movq -1280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5752
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1760(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1768(%rbp)
    movq -1768(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5761
    leaq .STR71(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5762
.L5761:
.L5762:
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
    movq %rax, -1776(%rbp)
    movq -1256(%rbp), %rax
    pushq %rax
    movq -1264(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5771
    movq -1264(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5772
.L5771:
.L5772:
    movq -1256(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1776(%rbp), %rax
    pushq %rax
    movq -1312(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1784(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1784(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1792(%rbp)
    movq -1792(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5781
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5782
.L5781:
    movq $0, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5782:
    jmp .L5751
.L5752:
    movq -1248(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L5742
.L5741:
.L5742:
    jmp .L5732
.L5731:
.L5732:
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5692
.L5691:
.L5692:
    jmp .L5662
.L5661:
.L5662:
    movq -1600(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5791
    movq $40, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $9, %rax  # Load constant EXPR_VARIANT_CONSTRUCTOR
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
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
    leaq -1744(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1744(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5801
    movq $0, %rax
    pushq %rax
    movq -1744(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1752(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1752(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5811
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5821:    movq -1280(%rbp), %rax
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
    pushq %rax
    leaq -1760(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1768(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5831
    leaq .STR71(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L5832
.L5831:
.L5832:
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
    leaq -1776(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1256(%rbp), %rax
    pushq %rax
    movq -1264(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5841
    movq -1264(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5842
.L5841:
.L5842:
    movq -1256(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1776(%rbp), %rax
    pushq %rax
    movq -1312(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
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
    leaq -1784(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1784(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1792(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5851
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L5852
.L5851:
    movq $0, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L5852:
    jmp .L5821
.L5822:
    movq -1248(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L5812
.L5811:
.L5812:
    jmp .L5802
.L5801:
.L5802:
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5792
.L5791:
.L5792:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1800(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1800(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1808(%rbp)
    movq -1472(%rbp), %rax
    movq %rax, -1816(%rbp)
    movq $0, %rax
    movq %rax, -1824(%rbp)
    movq $1, %rax
    movq %rax, -1832(%rbp)
    movq -1808(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5861
    movq $0, %rax
    pushq %rax
    leaq -1832(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5862
.L5861:
.L5862:
    movq -1832(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5871
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5881
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1840(%rbp)
    movq $16, %rax  # Load constant PROGRAM_TYPES
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1848(%rbp)
    movq $0, %rax
    movq %rax, -1856(%rbp)
.L5891:    movq -1856(%rbp), %rax
    pushq %rax
    movq -1840(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5892
    movq -1848(%rbp), %rax
    pushq %rax
    movq -1856(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1864(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1872(%rbp)
    movq $8, %rax  # Load constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -1872(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1880(%rbp)
    movq -1880(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant TYPE_KIND_VARIANT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5901
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -1872(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1888(%rbp)
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -1872(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1896(%rbp)
    movq $0, %rax
    movq %rax, -1904(%rbp)
.L5911:    movq -1904(%rbp), %rax
    pushq %rax
    movq -1888(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5912
    movq -1896(%rbp), %rax
    pushq %rax
    movq -1904(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1912(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1912(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1920(%rbp)
    movq -1816(%rbp), %rax
    pushq %rax
    movq -1920(%rbp), %rax
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
    jz .L5921
    movq -1872(%rbp), %rax
    pushq %rax
    leaq -1824(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1888(%rbp), %rax
    pushq %rax
    leaq -1904(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1840(%rbp), %rax
    pushq %rax
    leaq -1856(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5922
.L5921:
.L5922:
    movq -1904(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1904(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5911
.L5912:
    jmp .L5902
.L5901:
.L5902:
    movq -1856(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1856(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5891
.L5892:
    jmp .L5882
.L5881:
.L5882:
    jmp .L5872
.L5871:
.L5872:
    movq -1824(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5931
    movq $40, %rax
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $9, %rax  # Load constant EXPR_VARIANT_CONSTRUCTOR
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq -1824(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1928(%rbp)
    movq -1928(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1816(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5932
.L5931:
.L5932:
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
    call memory_get_int32@PLT
    movq %rax, -1944(%rbp)
    movq -1944(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5941
    movq -1472(%rbp), %rax
    movq %rax, -1952(%rbp)
    movq $0, %rax
    movq %rax, -1960(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5951
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -496(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax  # Load constant PROGRAM_TYPES
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -504(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    movq %rax, -1968(%rbp)
.L5961:    movq -1968(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5962
    movq $0, %rax
    movq %rax, -1976(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq -496(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5971
    movq $1, %rax
    pushq %rax
    leaq -1976(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5972
.L5971:
.L5972:
    movq -1976(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5981
    movq $0, %rax
    pushq %rax
    leaq -1968(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5982
.L5981:
.L5982:
    movq -1976(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L5991
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -512(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -504(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -520(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -528(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1624(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1984(%rbp)
    movq -1624(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant TYPE_KIND_VARIANT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6001
    movq $1, %rax
    pushq %rax
    leaq -1984(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6002
.L6001:
.L6002:
    movq -1984(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6011
    movq $24, %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1632(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    movq -528(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1640(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -1992(%rbp)
    movq $1, %rax
    movq %rax, -2000(%rbp)
.L6021:    movq -2000(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6022
    movq $0, %rax
    movq %rax, -2008(%rbp)
    movq -1992(%rbp), %rax
    pushq %rax
    movq -1632(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6031
    movq $1, %rax
    pushq %rax
    leaq -2008(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6032
.L6031:
.L6032:
    movq -2008(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6041
    movq $0, %rax
    pushq %rax
    leaq -2000(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6042
.L6041:
.L6042:
    movq -2008(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6051
    movq -1992(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant VARIANT_SIZE
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1640(%rbp), %rax
    addq -1656(%rbp), %rax
    pushq %rax
    leaq -1664(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1664(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2016(%rbp)
    movq -1952(%rbp), %rax
    pushq %rax
    movq -2016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -2024(%rbp)
    movq -2024(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6061
    movq -528(%rbp), %rax
    pushq %rax
    leaq -1960(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -2000(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1968(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6062
.L6061:
.L6062:
    movq -1992(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1992(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6052
.L6051:
.L6052:
    jmp .L6021
.L6022:
    jmp .L6012
.L6011:
.L6012:
    movq -512(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L5992
.L5991:
.L5992:
    jmp .L5961
.L5962:
    jmp .L5952
.L5951:
.L5952:
    movq -1960(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6071
    movq $40, %rax
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $9, %rax  # Load constant EXPR_VARIANT_CONSTRUCTOR
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
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
    call memory_get_integer@PLT
    pushq %rax
    leaq -1928(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1928(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1952(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
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
    movq %rax, -2032(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2032(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2040(%rbp)
    movq -2040(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6081
    movq $114, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $4, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6091:    movq -1280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6092
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -1760(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1760(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1768(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6101
    leaq .STR71(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6102
.L6101:
.L6102:
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
    leaq -1776(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1256(%rbp), %rax
    pushq %rax
    movq -1264(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6111
    movq -1264(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -1248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6112
.L6111:
.L6112:
    movq -1256(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -1312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1776(%rbp), %rax
    pushq %rax
    movq -1312(%rbp), %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -1256(%rbp), %rbx
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
    leaq -1784(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -1784(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1792(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1792(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6121
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L6122
.L6121:
    movq $0, %rax
    pushq %rax
    leaq -1280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6122:
    jmp .L6091
.L6092:
    movq -1248(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L6082
.L6081:
.L6082:
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6072
.L6071:
.L6072:
    jmp .L5942
.L5941:
.L5942:
    movq $0, %rax
    movq %rax, -2048(%rbp)
    movq -2048(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6131
    movq $51, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2056(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -2064(%rbp)
    movq $1, %rax
    movq %rax, -2072(%rbp)
.L6141:    movq -2072(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6142
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2080(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2080(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2088(%rbp)
    movq -2088(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6151
    movq $0, %rax
    pushq %rax
    leaq -2072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6152
.L6151:
.L6152:
    movq -2088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6161
    movq $0, %rax
    pushq %rax
    leaq -2072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6162
.L6161:
.L6162:
    movq $0, %rax
    movq %rax, -2096(%rbp)
    movq -2088(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6171
    movq -2088(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6181
    movq $1, %rax
    pushq %rax
    leaq -2096(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6182
.L6181:
.L6182:
    jmp .L6172
.L6171:
.L6172:
    movq -2096(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6191
    movq -272(%rbp), %rax
    pushq %rax
    movq -2064(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6201
    movq -2064(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6211
    movq $4, %rax
    pushq %rax
    leaq -2064(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6212
.L6211:
    movq -2064(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -2064(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6212:
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -2064(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -360(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -360(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6202
.L6201:
.L6202:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    pushq %rax
    leaq -352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -272(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -264(%rbp), %rax
    addq -368(%rbp), %rax
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2112(%rbp)
    movq -2112(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6221
    movq $0, %rax
    pushq %rax
    leaq -2072(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6222
.L6221:
    movq -2112(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6231
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2120(%rbp)
    jmp .L6232
.L6231:
    leaq .STR72(%rip), %rax
    movq %rax, -2128(%rbp)
    movq -2128(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -2104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L6232:
.L6222:
    jmp .L6192
.L6191:
.L6192:
    jmp .L6141
.L6142:
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2136(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6132
.L6131:
.L6132:
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6241
    movq $32, %rax
    pushq %rax
    leaq -408(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $7, %rax  # Load constant EXPR_TYPE_NAME
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1472(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6242
.L6241:
.L6242:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2144(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -2144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2152(%rbp)
    movq -2152(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6251
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2160(%rbp)
    movq $8, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2168(%rbp)
    movq $12, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2176(%rbp)
    movq $16, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2184(%rbp)
    movq $20, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -2192(%rbp)
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rax, -2200(%rbp)
    movq $0, %rax
    movq %rax, -2208(%rbp)
    movq -2200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6261
    movq $0, %rax
    pushq %rax
    movq -2200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -2216(%rbp)
    movq -2216(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6271
    movq $8, %rax
    pushq %rax
    movq -2200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2224(%rbp)
    movq -2224(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6281
    movq $0, %rax
    pushq %rax
    movq -2224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -2232(%rbp)
    movq -2232(%rbp), %rax
    pushq %rax
    movq $65, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6291
    movq -2232(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6301
    movq $1, %rax
    pushq %rax
    leaq -2208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6302
.L6301:
.L6302:
    jmp .L6292
.L6291:
.L6292:
    jmp .L6282
.L6281:
.L6282:
    jmp .L6272
.L6271:
.L6272:
    movq -2200(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L6262
.L6261:
.L6262:
    movq -2168(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -2176(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -2184(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -2192(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -2160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -2208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6311
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2240(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -2240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2248(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -2240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2256(%rbp)
    movq -2248(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6312
.L6311:
.L6312:
    jmp .L6252
.L6251:
.L6252:
    movq -1472(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L5302
.L5301:
.L5302:
    movq -24(%rbp), %rax
    pushq %rax
    movq $134, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6321
    movq $134, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2264(%rbp)
    movq $1, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6322
.L6321:
.L6322:
    movq -24(%rbp), %rax
    pushq %rax
    movq $135, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6331
    movq $135, %rax
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
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6332
.L6331:
.L6332:
    movq -24(%rbp), %rax
    pushq %rax
    movq $133, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6341
    movq $133, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    pushq %rax
    leaq -2120(%rbp), %rbx
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
    call memory_get_integer@PLT
    movq %rax, -2280(%rbp)
    movq -2280(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6351
    leaq .STR73(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax
    pushq %rax
    movq -2272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6352
.L6351:
.L6352:
    movq $8, %rax
    pushq %rax
    movq -2272(%rbp), %rax
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
    popq %rdi
    call string_to_integer
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    subq -432(%rbp), %rax
    movq %rax, -2288(%rbp)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq %rax, -2296(%rbp)
    movq -2288(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -416(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -416(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6342
.L6341:
.L6342:
    movq -24(%rbp), %rax
    pushq %rax
    movq $162, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6361
    movq $162, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $0, %rax
    movq %rax, -2304(%rbp)
    movq $0, %rax
    movq %rax, -2312(%rbp)
    movq $4, %rax
    movq %rax, -2320(%rbp)
    movq -2320(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -2328(%rbp)
    movq -2328(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -2304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2336(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2344(%rbp)
    movq -2344(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6371
    leaq .STR74(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6372
.L6371:
.L6372:
    movq $8, %rax
    pushq %rax
    movq -2336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2352(%rbp)
    movq -2352(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -2360(%rbp)
    movq -2360(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -2304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    leaq -2312(%rbp), %rbx
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
    movq %rax, -2368(%rbp)
.L6381:    movq -2368(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6382
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2376(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -1488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1488(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6391
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
    movq %rax, -2384(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2392(%rbp)
    movq -2392(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6401
    leaq .STR75(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6402
.L6401:
.L6402:
    movq $8, %rax
    pushq %rax
    movq -2384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2400(%rbp)
    movq -2400(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -2408(%rbp)
    movq -2312(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -2416(%rbp)
    movq -2408(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -2304(%rbp), %rax
    addq -2416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -2312(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -2312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L6392
.L6391:
    movq $0, %rax
    pushq %rax
    leaq -2368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6392:
    jmp .L6381
.L6382:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -2424(%rbp)
    movq $0, %rax
    pushq %rax
    movq -2424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -2432(%rbp)
    movq -2432(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6411
    leaq .STR76(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L6412
.L6411:
.L6412:
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
    movq %rax, -2440(%rbp)
    movq -2440(%rbp), %rax
    pushq %rax
    movq -2312(%rbp), %rax
    pushq %rax
    movq -2304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_lambda_multi
    movq %rax, -2448(%rbp)
    movq -2312(%rbp), %rax
    pushq %rax
    movq -2304(%rbp), %rax
    pushq %rax
    movq -2440(%rbp), %rax
    pushq %rax
    movq -2448(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call lambda_collect_free_vars
    movq -2448(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6362
.L6361:
.L6362:
    leaq .STR77(%rip), %rax
    pushq %rax
    leaq -2128(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -2128(%rbp), %rax
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
    leaq -1048(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -1048(%rbp), %rax
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
    jz .L6421
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6422
.L6421:
.L6422:
    movq -32(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6431
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6432
.L6431:
.L6432:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6441
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6442
.L6441:
.L6442:
    movq -32(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6451
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6452
.L6451:
.L6452:
    movq -32(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6461
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6462
.L6461:
.L6462:
    movq -32(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6471
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6472
.L6471:
.L6472:
    movq -32(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6481
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6482
.L6481:
.L6482:
    movq -32(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6491
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6492
.L6491:
.L6492:
    movq -32(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6501
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6502
.L6501:
.L6502:
    movq -32(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6511
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6512
.L6511:
.L6512:
    movq -32(%rbp), %rax
    pushq %rax
    movq $113, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6521
    movq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6522
.L6521:
.L6522:
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
    jz .L6531
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6532
.L6531:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6532:
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
    jz .L6541
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
    jmp .L6542
.L6541:
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
.L6542:
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
    jz .L6551
    leaq .STR78(%rip), %rax
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
    jmp .L6552
.L6551:
.L6552:
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
    jz .L6561
    movq -64(%rbp), %rax
    movq %rax, -88(%rbp)
.L6571:    movq -80(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6572
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
    jmp .L6571
.L6572:
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_print
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L6562
.L6561:
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_print
    movq %rbp, %rsp
    popq %rbp
    ret
.L6562:
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
.L6581:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6582
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
    jz .L6591
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6592
.L6591:
.L6592:
    movq -56(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6601
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6602
.L6601:
.L6602:
    movq -56(%rbp), %rax
    pushq %rax
    movq $113, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6611
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6612
.L6611:
.L6612:
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
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6622
.L6621:
.L6622:
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6631
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
    jz .L6641
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6642
.L6641:
.L6642:
    movq -56(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6651
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_next_token_type
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6661
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6662
.L6661:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6662:
    jmp .L6652
.L6651:
.L6652:
    movq -56(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6671
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6672
.L6671:
.L6672:
    movq -56(%rbp), %rax
    pushq %rax
    movq $44, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6681
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_break_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6682
.L6681:
.L6682:
    movq -56(%rbp), %rax
    pushq %rax
    movq $45, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6691
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_continue_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6692
.L6691:
.L6692:
    movq -56(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6701
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6702
.L6701:
.L6702:
    movq -56(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6711
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6712
.L6711:
.L6712:
    movq -56(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6721
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6722
.L6721:
.L6722:
    movq -56(%rbp), %rax
    pushq %rax
    movq $180, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6731
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_loop_forever
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6732
.L6731:
.L6732:
    movq -56(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6741
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6742
.L6741:
.L6742:
    movq -56(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6751
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6752
.L6751:
.L6752:
    movq -56(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6761
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_for_range_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6762
.L6761:
.L6762:
    movq -56(%rbp), %rax
    pushq %rax
    movq $164, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6771
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_local_constant_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6772
.L6771:
.L6772:
    movq -56(%rbp), %rax
    pushq %rax
    movq $139, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6781
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
    jmp .L6782
.L6781:
.L6782:
    movq -56(%rbp), %rax
    pushq %rax
    movq $140, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6791
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
    jmp .L6792
.L6791:
.L6792:
    movq -56(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6801
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
    jmp .L6802
.L6801:
.L6802:
    movq -56(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6811
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
    jmp .L6812
.L6811:
.L6812:
    movq -56(%rbp), %rax
    pushq %rax
    movq $167, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6821
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
    movq %rax, -88(%rbp)
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
    movq %rax, -96(%rbp)
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
    movq %rax, -104(%rbp)
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
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -104(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    leaq .STR79(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6822
.L6821:
.L6822:
    movq -56(%rbp), %rax
    pushq %rax
    movq $169, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6831
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
    movq %rax, -128(%rbp)
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
    movq %rax, -136(%rbp)
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
    movq %rax, -144(%rbp)
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
    movq %rax, -152(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -136(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -144(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -152(%rbp), %rax
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
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6832
.L6831:
.L6832:
    movq -56(%rbp), %rax
    pushq %rax
    movq $171, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6841
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6842
.L6841:
.L6842:
    movq -56(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6851
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6852
.L6851:
.L6852:
    movq -56(%rbp), %rax
    pushq %rax
    movq $183, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6861
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_call_statement
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6862
.L6861:
.L6862:
    movq -56(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6871
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq $0, %rax
    movq %rax, -184(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6881
    leaq .STR81(%rip), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6882
.L6881:
.L6882:
    movq -184(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6891
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
    movq %rax, -192(%rbp)
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
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -208(%rbp)
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax
    movq %rax, -224(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6901
    leaq .STR82(%rip), %rax
    pushq %rax
    movq -216(%rbp), %rax
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
    jz .L6911
    movq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6912
.L6911:
.L6912:
    jmp .L6902
.L6901:
.L6902:
    movq -224(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6921
    movq -208(%rbp), %rax
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
    jmp .L6922
.L6921:
.L6922:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -232(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -240(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -192(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    leaq .STR83(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6892
.L6891:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -256(%rbp)
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6931
    movq -264(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6941
    leaq .STR84(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR85(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    jmp .L6942
.L6941:
.L6942:
    jmp .L6932
.L6931:
.L6932:
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6892:
    jmp .L6872
.L6871:
.L6872:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6951
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6952
.L6951:
.L6952:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6961
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6962
.L6961:
.L6962:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6971
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6981
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L6991
    movq $256, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L6992
.L6991:
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L6992:
    movq $8, %rax
    movq %rax, -296(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
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
    jmp .L6982
.L6981:
.L6982:
    movq $8, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -288(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -312(%rbp)
    movq -24(%rbp), %rax
    addq -312(%rbp), %rax
    movq %rax, -320(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -288(%rbp), %rax
    addq $1, %rax
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L6972
.L6971:
.L6972:
    jmp .L6632
.L6631:
.L6632:
    jmp .L6581
.L6582:
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L7001
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
    movq $0, %rax
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
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $34, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7011
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
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -96(%rbp)
    movq $8, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7012
.L7011:
.L7012:
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
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7021
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
    movq %rax, -128(%rbp)
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
    movq $0, %rax
    movq %rax, -160(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $38, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7031
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
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7032
.L7031:
.L7032:
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
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -176(%rbp)
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -184(%rbp)
    movq -168(%rbp), %rax
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
    movq -184(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
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
    jmp .L7022
.L7021:
.L7022:
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
    movq %rax, -192(%rbp)
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
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -216(%rbp)
    movq -200(%rbp), %rax
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
    movq -64(%rbp), %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    popq %r8
    call statement_create_for_each
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7002
.L7001:
.L7002:
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
    movq %rax, -232(%rbp)
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
    movq %rax, -240(%rbp)
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
    movq $0, %rax
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $38, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7041
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
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7042
.L7041:
    movq -256(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7051
    movq $8, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7061
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -272(%rbp), %rax
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
    jz .L7071
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
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7072
.L7071:
.L7072:
    jmp .L7062
.L7061:
.L7062:
    jmp .L7052
.L7051:
.L7052:
.L7042:
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
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
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
    movq -216(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
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
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
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
.L7081:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7082
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
    jz .L7091
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
    jz .L7101
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
    jz .L7111
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
    jmp .L7112
.L7111:
.L7112:
    movq -184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7121
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
.L7131:    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7132
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
    jmp .L7131
.L7132:
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
    jmp .L7122
.L7121:
.L7122:
    jmp .L7102
.L7101:
.L7102:
    movq -120(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7141
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
    jz .L7151
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
    jmp .L7152
.L7151:
.L7152:
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7161
    movq -64(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7171
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
.L7181:    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7182
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
    jmp .L7181
.L7182:
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
    jmp .L7172
.L7171:
.L7172:
    jmp .L7162
.L7161:
.L7162:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7142
.L7141:
.L7142:
    jmp .L7092
.L7091:
.L7092:
    movq -96(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
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
    jmp .L7081
.L7082:
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
.L7201:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7202
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
    jz .L7211
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7212
.L7211:
.L7212:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7221
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
    jz .L7231
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
    movq $0, %rax  # Load constant PATTERN_LITERAL
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
    jz .L7241
    movq $2, %rax  # Load constant PATTERN_WILDCARD
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
    jmp .L7242
.L7241:
    movq -80(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7251
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
    jz .L7261
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
    jz .L7271
    leaq .STR87(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L7272
.L7271:
.L7272:
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
    jz .L7281
    movq -176(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7291
    leaq .STR88(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L7292
.L7291:
.L7292:
    jmp .L7282
.L7281:
.L7282:
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
    movq $3, %rax  # Load constant PATTERN_TYPE
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -192(%rbp), %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7262
.L7261:
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
    jz .L7301
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
    jz .L7311
    movq -232(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7312
.L7311:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L7312:
    jmp .L7302
.L7301:
.L7302:
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
    jz .L7321
    movq $1, %rax  # Load constant PATTERN_VARIANT
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -200(%rbp), %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7322
.L7321:
    movq -256(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7331
    movq $1, %rax  # Load constant PATTERN_VARIANT
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
.L7341:    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7342
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
    jz .L7351
    leaq .STR89(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L7352
.L7351:
.L7352:
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
    jz .L7361
    leaq .STR90(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L7362
.L7361:
.L7362:
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
    jz .L7371
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
    jmp .L7372
.L7371:
.L7372:
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
    movq $0, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7382:
    jmp .L7341
.L7342:
    jmp .L7332
.L7331:
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_variable
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7332:
.L7322:
.L7262:
    jmp .L7252
.L7251:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_additive
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7252:
.L7242:
    movq $4, %rax
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -376(%rbp)
    movq $0, %rax
    movq %rax, -384(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq $0, %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -400(%rbp)
.L7391:    movq -400(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7392
    movq $31, %rax
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
    movq %rax, -408(%rbp)
    movq $0, %rax
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -416(%rbp)
    movq $0, %rax
    movq %rax, -424(%rbp)
    movq $0, %rax
    movq %rax, -432(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq $161, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7401
    movq $2, %rax
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $161, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7402
.L7401:
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -440(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7411
    movq $8, %rax
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -448(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -456(%rbp)
    movq -416(%rbp), %rax
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
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7421
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
    movq %rax, -480(%rbp)
    movq $0, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
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
    jz .L7431
    movq -488(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L7432
.L7431:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L7432:
    jmp .L7422
.L7421:
.L7422:
    movq $1, %rax
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -456(%rbp), %rax
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7412
.L7411:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -504(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -424(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -504(%rbp), %rax
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7412:
.L7402:
    movq -384(%rbp), %rax
    pushq %rax
    movq -368(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7441
    movq -368(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -368(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -368(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -376(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7442
.L7441:
.L7442:
    movq -384(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -512(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    addq -512(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -432(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    addq -512(%rbp), %rax
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
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7391
.L7392:
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
    movq %rax, -520(%rbp)
    movq -520(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -528(%rbp)
    movq $0, %rax
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -536(%rbp)
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    addq -384(%rbp), %rax
    movq %rax, -544(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -544(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7451
.L7461:    movq -24(%rbp), %rax
    pushq %rax
    movq -544(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7462
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7461
.L7462:
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
    jmp .L7452
.L7451:
.L7452:
    movq -40(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -552(%rbp)
    movq -32(%rbp), %rax
    addq -552(%rbp), %rax
    movq %rax, -560(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load constant WHEN_PATTERN_TYPE
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant WHEN_PATTERN_VALUE
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -104(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant WHEN_FIELD_BINDINGS
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load constant WHEN_FIELD_COUNT
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -528(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant WHEN_BODY_STMTS
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -536(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load constant WHEN_BODY_COUNT
    pushq %rax
    movq -560(%rbp), %rax
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
    movq $0, %rax
    movq %rax, -568(%rbp)
.L7471:    movq -568(%rbp), %rax
    pushq %rax
    movq -384(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7472
    movq -40(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -576(%rbp)
    movq -32(%rbp), %rax
    addq -576(%rbp), %rax
    movq %rax, -584(%rbp)
    movq -568(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -592(%rbp)
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    addq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -600(%rbp)
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    addq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -608(%rbp)
    movq -600(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load constant WHEN_PATTERN_TYPE
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant WHEN_PATTERN_VALUE
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant WHEN_FIELD_BINDINGS
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load constant WHEN_FIELD_COUNT
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -528(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant WHEN_BODY_STMTS
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -536(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load constant WHEN_BODY_COUNT
    pushq %rax
    movq -584(%rbp), %rax
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
    movq -568(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -568(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7471
.L7472:
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L7232
.L7231:
    movq -64(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7481
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
    movq %rax, -616(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_parse_statement_block
    movq %rax, -624(%rbp)
    movq $0, %rax
    pushq %rax
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -632(%rbp)
    movq -616(%rbp), %rax
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
    jz .L7491
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
    jmp .L7492
.L7491:
.L7492:
    movq -40(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -640(%rbp)
    movq -32(%rbp), %rax
    addq -640(%rbp), %rax
    movq %rax, -648(%rbp)
    movq $2, %rax  # Load constant PATTERN_WILDCARD
    pushq %rax
    movq $0, %rax  # Load constant WHEN_PATTERN_TYPE
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load constant WHEN_PATTERN_VALUE
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant WHEN_FIELD_BINDINGS
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load constant WHEN_FIELD_COUNT
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -624(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant WHEN_BODY_STMTS
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -632(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load constant WHEN_BODY_COUNT
    pushq %rax
    movq -648(%rbp), %rax
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
    jmp .L7482
.L7481:
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7501
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
    jmp .L7502
.L7501:
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L7502:
.L7482:
.L7232:
    jmp .L7222
.L7221:
.L7222:
    jmp .L7201
.L7202:
    movq $0, %rax
    movq %rax, -656(%rbp)
    movq $0, %rax
    movq %rax, -664(%rbp)
.L7511:    movq -664(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7512
    movq -664(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -552(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    addq -552(%rbp), %rax
    pushq %rax
    leaq -560(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax  # Load constant WHEN_PATTERN_TYPE
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7521
    movq $1, %rax
    pushq %rax
    leaq -656(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7522
.L7521:
.L7522:
    movq -664(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -664(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7511
.L7512:
    movq -656(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7531
    movq $8, %rax
    movq %rax, -680(%rbp)
    movq -680(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -688(%rbp)
    movq $0, %rax
    movq %rax, -696(%rbp)
    movq $0, %rax
    movq %rax, -704(%rbp)
.L7541:    movq -704(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7542
    movq -704(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -552(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    addq -552(%rbp), %rax
    pushq %rax
    leaq -560(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax  # Load constant WHEN_PATTERN_TYPE
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -672(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -672(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7551
    movq $8, %rax  # Load constant WHEN_PATTERN_VALUE
    pushq %rax
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -712(%rbp)
    movq -696(%rbp), %rax
    pushq %rax
    movq -680(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7561
    movq -680(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -680(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -680(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -688(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7562
.L7561:
.L7562:
    movq -712(%rbp), %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -696(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -696(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7552
.L7551:
.L7552:
    movq -704(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -704(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7541
.L7542:
    movq -696(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7571
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -720(%rbp)
    movq -720(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7581
    movq $0, %rax
    pushq %rax
    leaq -696(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7582
.L7581:
.L7582:
    movq -720(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7591
    movq $24, %rax
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -728(%rbp)
    movq $16, %rax
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -736(%rbp)
    movq $0, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -744(%rbp)
    movq $0, %rax
    movq %rax, -752(%rbp)
    movq $0, %rax
    movq %rax, -760(%rbp)
    movq $0, %rax
    movq %rax, -768(%rbp)
.L7601:    movq -768(%rbp), %rax
    pushq %rax
    movq -728(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7602
    movq -768(%rbp), %rax
    pushq %rax
    movq -736(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer_at_index
    movq %rax, -776(%rbp)
    movq $8, %rax
    pushq %rax
    movq -776(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -784(%rbp)
    movq -784(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7611
    movq $24, %rax
    pushq %rax
    movq -776(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -792(%rbp)
    movq $16, %rax
    pushq %rax
    movq -776(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -800(%rbp)
    movq $0, %rax
    movq %rax, -808(%rbp)
.L7621:    movq -808(%rbp), %rax
    pushq %rax
    movq -792(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7622
    movq -808(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -816(%rbp)
    movq -800(%rbp), %rax
    addq -816(%rbp), %rax
    movq %rax, -824(%rbp)
    movq $0, %rax
    pushq %rax
    movq -824(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -832(%rbp)
    movq -744(%rbp), %rax
    pushq %rax
    movq -832(%rbp), %rax
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
    jz .L7631
    movq -776(%rbp), %rax
    pushq %rax
    leaq -752(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -792(%rbp), %rax
    pushq %rax
    leaq -760(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -728(%rbp), %rax
    pushq %rax
    leaq -768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -792(%rbp), %rax
    pushq %rax
    leaq -808(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7632
.L7631:
.L7632:
    movq -808(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -808(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7621
.L7622:
    jmp .L7612
.L7611:
.L7612:
    movq -768(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7601
.L7602:
    movq -752(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7641
    movq $16, %rax
    pushq %rax
    movq -752(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -800(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -752(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -840(%rbp)
    movq $0, %rax
    movq %rax, -848(%rbp)
    movq $0, %rax
    movq %rax, -856(%rbp)
.L7651:    movq -856(%rbp), %rax
    pushq %rax
    movq -760(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7652
    movq -856(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -816(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -800(%rbp), %rax
    addq -816(%rbp), %rax
    pushq %rax
    leaq -824(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    movq -824(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -864(%rbp)
    movq $0, %rax
    movq %rax, -872(%rbp)
.L7661:    movq -872(%rbp), %rax
    pushq %rax
    movq -696(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7662
    movq -872(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -880(%rbp)
    movq -880(%rbp), %rax
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
    jz .L7671
    movq $1, %rax
    pushq %rax
    leaq -864(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -696(%rbp), %rax
    pushq %rax
    leaq -872(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7672
.L7671:
.L7672:
    movq -872(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -872(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7661
.L7662:
    movq -864(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7681
    movq -848(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7691
    leaq .STR91(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -840(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR92(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    leaq -848(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7692
.L7691:
.L7692:
    leaq .STR93(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    jmp .L7682
.L7681:
.L7682:
    movq -856(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -856(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7651
.L7652:
    jmp .L7642
.L7641:
.L7642:
    jmp .L7592
.L7591:
.L7592:
    jmp .L7572
.L7571:
.L7572:
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L7532
.L7531:
.L7532:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -888(%rbp)
    movq $8, %rax  # Load constant STMT_MATCH
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -888(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant STMT_MATCH_EXPR
    pushq %rax
    movq -888(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant STMT_MATCH_WHEN_CLAUSES
    pushq %rax
    movq -888(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load constant STMT_MATCH_WHEN_COUNT
    pushq %rax
    movq -888(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -888(%rbp), %rax
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
.L7701:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7702
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
    jz .L7711
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7712
.L7711:
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
    jz .L7721
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
    jz .L7731
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7732
.L7731:
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
.L7732:
    jmp .L7722
.L7721:
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
.L7722:
.L7712:
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    subq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7741
    leaq .STR94(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L7742
.L7741:
.L7742:
    jmp .L7701
.L7702:
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
    leaq .STR95(%rip), %rax
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
    jz .L7751
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
    jmp .L7752
.L7751:
.L7752:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_whitespace
    movq %rax, -40(%rbp)
    leaq .STR96(%rip), %rax
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
    jz .L7761
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
    jmp .L7762
.L7761:
.L7762:
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
.L7771:    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7772
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
    jz .L7781
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7782
.L7781:
.L7782:
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
    jmp .L7771
.L7772:
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
    leaq .STR29(%rip), %rax
    movq %rax, -24(%rbp)
    leaq .STR97(%rip), %rax
    movq %rax, -32(%rbp)
    leaq .STR98(%rip), %rax
    movq %rax, -40(%rbp)
    leaq .STR99(%rip), %rax
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
    jz .L7791
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7792
.L7791:
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
    jz .L7801
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7802
.L7801:
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
    jz .L7811
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7812
.L7811:
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
    jz .L7821
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L7822
.L7821:
.L7822:
.L7812:
.L7802:
.L7792:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7831
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
.L7841:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7842
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
    jz .L7851
    movq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7852
.L7851:
.L7852:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7861
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7862
.L7861:
.L7862:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7871
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
    jz .L7881
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
    jmp .L7882
.L7881:
.L7882:
    movq -72(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7872
.L7871:
.L7872:
    jmp .L7841
.L7842:
    jmp .L7832
.L7831:
.L7832:
    leaq .STR100(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR101(%rip), %rax
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
    movq $56, %rax  # Load constant TypeDefinition_SIZE
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L7891
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L7901
    leaq .STR102(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L7902
.L7901:
.L7902:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $0, %rax  # Load constant TYPEDEFINITION_NAME_OFFSET
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
    movq $0, %rax  # Load constant TYPE_KIND_STRUCT
    pushq %rax
    movq $8, %rax  # Load constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
.L7911:    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7912
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
    jz .L7921
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7922
.L7921:
.L7922:
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
    jz .L7931
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7932
.L7931:
.L7932:
    movq -32(%rbp), %rax
    pushq %rax
    movq $151, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7941
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7942
.L7941:
.L7942:
    movq -32(%rbp), %rax
    pushq %rax
    movq $150, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7951
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7952
.L7951:
.L7952:
    movq -32(%rbp), %rax
    pushq %rax
    movq $132, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7961
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7962
.L7961:
.L7962:
    movq -32(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7971
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7972
.L7971:
.L7972:
    movq -32(%rbp), %rax
    pushq %rax
    movq $155, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7981
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L7982
.L7981:
.L7982:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L7991
    leaq .STR61(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    leaq .STR103(%rip), %rax
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
    jmp .L7992
.L7991:
.L7992:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8001
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8002
.L8001:
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8002:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8011
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -104(%rbp)
.L8021:    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8022
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8031
    movq -104(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8032
.L8031:
.L8032:
    movq -32(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8041
    movq -104(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8042
.L8041:
.L8042:
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8021
.L8022:
    jmp .L8012
.L8011:
.L8012:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8051
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8052
.L8051:
.L8052:
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
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
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_STRUCT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
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
    jz .L8061
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8062
.L8061:
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
.L8062:
    movq -144(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_STRUCT_FIELDS_OFFSET
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
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -160(%rbp)
    movq -144(%rbp), %rax
    addq -160(%rbp), %rax
    movq %rax, -168(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
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
    movq $20, %rax  # Load constant TYPEFIELD_SIZE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L7911
.L7912:
    movq -64(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load constant TYPEDEFINITION_SIZE_OFFSET
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
    jmp .L7892
.L7891:
.L7892:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8071
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $0, %rax  # Load constant TYPEDEFINITION_NAME_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8081
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8091
    leaq .STR104(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8092
.L8091:
.L8092:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8101
    leaq .STR29(%rip), %rax
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
    jmp .L8102
.L8101:
.L8102:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8111
    leaq .STR31(%rip), %rax
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
    jmp .L8112
.L8111:
.L8112:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8121
    leaq .STR33(%rip), %rax
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
    jmp .L8122
.L8121:
.L8122:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8131
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jmp .L8132
.L8131:
.L8132:
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8141
    leaq .STR105(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8142
.L8141:
.L8142:
    movq $3, %rax  # Load constant TYPE_KIND_ARRAY
    pushq %rax
    movq $8, %rax  # Load constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -200(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_ARRAY_ELEMENT_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -192(%rbp), %rax
    pushq %rax
    movq $28, %rax  # Load constant TYPEDEFINITION_DATA_ARRAY_LENGTH_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_ARRAY_ELEMENT_SIZE_OFFSET
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
    movq $40, %rax  # Load constant TYPEDEFINITION_SIZE_OFFSET
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
    jmp .L8082
.L8081:
    movq -32(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8151
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
    movq $2, %rax  # Load constant TYPE_KIND_FUNCTION
    pushq %rax
    movq $8, %rax  # Load constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $32, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $8, %rax
    pushq %rax
    movq $40, %rax  # Load constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8161
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
    jmp .L8162
.L8161:
.L8162:
    movq -32(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8171
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8172
.L8171:
.L8172:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8181
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
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -232(%rbp)
.L8191:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8192
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8201
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
    jmp .L8202
.L8201:
.L8202:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
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
    jz .L8211
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
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_PARAM_TYPES_OFFSET
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
    jmp .L8212
.L8211:
.L8212:
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
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_PARAM_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8221
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8222
.L8221:
.L8222:
    movq -32(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8231
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8232
.L8231:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8232:
    jmp .L8191
.L8192:
    jmp .L8182
.L8181:
.L8182:
    movq $3, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8241
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L8242
.L8241:
.L8242:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8251
    leaq .STR31(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -280(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L8252
.L8251:
.L8252:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8261
    leaq .STR33(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -280(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L8262
.L8261:
.L8262:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8271
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $32, %rax  # Load constant TYPEDEFINITION_DATA_FUNCTION_RETURN_TYPE_OFFSET
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
    jmp .L8272
.L8271:
    leaq .STR106(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
.L8272:
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
    jmp .L8152
.L8151:
    movq $1, %rax  # Load constant TYPE_KIND_VARIANT
    pushq %rax
    movq $8, %rax  # Load constant TYPEDEFINITION_KIND_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
.L8281:    movq -32(%rbp), %rax
    pushq %rax
    movq $111, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8282
    movq $111, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8291
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8301
    leaq .STR107(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8302
.L8301:
.L8302:
    jmp .L8292
.L8291:
.L8292:
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
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
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -312(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant VARIANT_SIZE
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
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
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
    movq $32, %rax  # Load constant VARIANT_SIZE
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
    movq $0, %rax  # Load constant VARIANT_NAME_OFFSET
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -360(%rbp), %rax
    pushq %rax
    movq $20, %rax  # Load constant VARIANT_TAG_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8311
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
.L8321:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8322
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8331
    leaq .STR108(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8332
.L8331:
.L8332:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8341
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8351
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8361
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8371
    leaq .STR109(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8372
.L8371:
.L8372:
    jmp .L8362
.L8361:
.L8362:
    jmp .L8352
.L8351:
.L8352:
    jmp .L8342
.L8341:
.L8342:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $16, %rax  # Load constant VARIANT_FIELD_COUNT_OFFSET
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
    movq $16, %rax  # Load constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax  # Load constant VARIANT_FIELDS_OFFSET
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
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
    movq $8, %rax  # Load constant VARIANT_FIELDS_OFFSET
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
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
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
    movq $0, %rax  # Load constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
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
    movq $20, %rax  # Load constant TYPEFIELD_SIZE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8381
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8382
.L8381:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8382:
    jmp .L8321
.L8322:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L8312
.L8311:
.L8312:
    movq -32(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8391
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
.L8401:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8402
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8411
    leaq .STR108(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8412
.L8411:
.L8412:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8421
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8431
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8441
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8451
    leaq .STR109(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8452
.L8451:
.L8452:
    jmp .L8442
.L8441:
.L8442:
    jmp .L8432
.L8431:
.L8432:
    jmp .L8422
.L8421:
.L8422:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8461
    movq $4, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8462
.L8461:
.L8462:
    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8471
    movq $5, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8472
.L8471:
.L8472:
    movq -32(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8481
    movq $6, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8482
.L8481:
.L8482:
    movq -32(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8491
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8492
.L8491:
.L8492:
    movq $16, %rax  # Load constant VARIANT_FIELD_COUNT_OFFSET
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
    movq $16, %rax  # Load constant VARIANT_FIELD_COUNT_OFFSET
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax  # Load constant VARIANT_FIELDS_OFFSET
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
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
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
    movq $8, %rax  # Load constant VARIANT_FIELDS_OFFSET
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
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
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
    movq $0, %rax  # Load constant TYPEFIELD_NAME_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant TYPEFIELD_TYPE_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -160(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant TYPEFIELD_OFFSET_OFFSET
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
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
    movq $20, %rax  # Load constant TYPEFIELD_SIZE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8501
    movq $30, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8502
.L8501:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8502:
    jmp .L8401
.L8402:
    jmp .L8392
.L8391:
.L8392:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L8281
.L8282:
    movq $8, %rax
    pushq %rax
    movq $40, %rax  # Load constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $24, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANT_COUNT_OFFSET
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
    movq $16, %rax  # Load constant TYPEDEFINITION_DATA_VARIANT_VARIANTS_OFFSET
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
.L8511:    movq -432(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8512
    movq -432(%rbp), %rax
    pushq %rax
    movq $32, %rax  # Load constant VARIANT_SIZE
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
    movq $16, %rax  # Load constant VARIANT_FIELD_COUNT_OFFSET
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
    movq $8, %rax  # Load constant VARIANT_FIELDS_OFFSET
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
.L8521:    movq -448(%rbp), %rax
    pushq %rax
    movq -376(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8522
    movq -448(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load constant TYPEFIELD_SIZE
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
    movq $20, %rax  # Load constant TYPEFIELD_SIZE_OFFSET
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
    jmp .L8521
.L8522:
    movq $40, %rax  # Load constant TYPEDEFINITION_SIZE_OFFSET
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
    jz .L8531
    movq -440(%rbp), %rax
    pushq %rax
    movq $40, %rax  # Load constant TYPEDEFINITION_SIZE_OFFSET
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L8532
.L8531:
.L8532:
    movq -432(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8511
.L8512:
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
.L8152:
.L8082:
    jmp .L8072
.L8071:
    leaq .STR110(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
.L8072:
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8541
    leaq .STR111(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $10, %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR112(%rip), %rax
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
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8542
.L8541:
.L8542:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8551
    leaq .STR113(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit
    jmp .L8552
.L8551:
.L8552:
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
    leaq .STR29(%rip), %rax
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8561
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L8562
.L8561:
.L8562:
    movq -24(%rbp), %rax
    pushq %rax
    movq $33, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8571
    movq $33, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8581
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
    jmp .L8582
.L8581:
.L8582:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8591
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8592
.L8591:
.L8592:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8601
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8611
    leaq .STR114(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8612
.L8611:
.L8612:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8621
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8622
.L8621:
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8622:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8631
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -112(%rbp)
.L8641:    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8642
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8651
    movq -112(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8652
.L8651:
.L8652:
    movq -24(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8661
    movq -112(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8662
.L8661:
.L8662:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8641
.L8642:
    jmp .L8632
.L8631:
.L8632:
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8671
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8672
.L8671:
.L8672:
    movq -128(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8681
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8682
.L8681:
.L8682:
.L8691:    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8692
    movq -128(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8701
    leaq .STR115(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8702
.L8701:
.L8702:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8711
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8712
.L8711:
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8712:
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8721
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -224(%rbp)
.L8731:    movq -224(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8732
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8741
    movq -224(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8742
.L8741:
.L8742:
    movq -216(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8751
    movq -224(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -224(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8752
.L8751:
.L8752:
    movq -216(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8731
.L8732:
    jmp .L8722
.L8721:
.L8722:
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8761
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8762
.L8761:
.L8762:
    movq -128(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8771
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8772
.L8771:
.L8772:
    jmp .L8691
.L8692:
    jmp .L8602
.L8601:
.L8602:
    jmp .L8572
.L8571:
.L8572:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8781
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
    jmp .L8782
.L8781:
.L8782:
    leaq .STR116(%rip), %rax
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
    jz .L8791
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L8801
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8802
.L8801:
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -240(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8802:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8792
.L8791:
.L8792:
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8811
    movq $127, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -248(%rbp)
.L8821:    movq -248(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8822
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L8831
    movq -248(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8832
.L8831:
.L8832:
    movq -24(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8841
    movq -248(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8842
.L8841:
.L8842:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L8821
.L8822:
    jmp .L8812
.L8811:
.L8812:
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
    jz .L8851
    leaq .STR106(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
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
    jmp .L8852
.L8851:
.L8852:
    movq $9, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -272(%rbp)
.L8861:    movq -272(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8862
    movq -272(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8871
    jmp .L8862
    jmp .L8872
.L8871:
.L8872:
    movq -272(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8881
    jmp .L8862
    jmp .L8882
.L8881:
.L8882:
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
    jz .L8891
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_let_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8892
.L8891:
.L8892:
    movq -272(%rbp), %rax
    pushq %rax
    movq $14, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8901
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_peek_next_token_type
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $51, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8911
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8912
.L8911:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_set_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L8912:
    jmp .L8902
.L8901:
.L8902:
    movq -272(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8921
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_if_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8922
.L8921:
.L8922:
    movq -272(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8931
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_while_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8932
.L8931:
.L8932:
    movq -272(%rbp), %rax
    pushq %rax
    movq $180, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8941
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_loop_forever
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8942
.L8941:
.L8942:
    movq -272(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8951
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_match_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8952
.L8951:
.L8952:
    movq -272(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8961
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8962
.L8961:
.L8962:
    movq -272(%rbp), %rax
    pushq %rax
    movq $172, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8971
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_print_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8972
.L8971:
.L8972:
    movq -272(%rbp), %rax
    pushq %rax
    movq $171, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8981
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_primary
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8982
.L8981:
.L8982:
    movq -272(%rbp), %rax
    pushq %rax
    movq $183, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L8991
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_call_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L8992
.L8991:
.L8992:
    movq -272(%rbp), %rax
    pushq %rax
    movq $121, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9001
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_inline_assembly_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9002
.L9001:
.L9002:
    movq -272(%rbp), %rax
    pushq %rax
    movq $143, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9011
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_for_range_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9012
.L9011:
.L9012:
    movq -272(%rbp), %rax
    pushq %rax
    movq $164, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9021
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_local_constant_statement
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9022
.L9021:
.L9022:
    movq -272(%rbp), %rax
    pushq %rax
    movq $139, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9031
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
    jmp .L9032
.L9031:
.L9032:
    movq -272(%rbp), %rax
    pushq %rax
    movq $140, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9041
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
    jmp .L9042
.L9041:
.L9042:
    movq -272(%rbp), %rax
    pushq %rax
    movq $141, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9051
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
    jmp .L9052
.L9051:
.L9052:
    movq -272(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9061
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
    jmp .L9062
.L9061:
.L9062:
    movq -272(%rbp), %rax
    pushq %rax
    movq $167, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9071
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
    movq %rax, -312(%rbp)
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
    movq %rax, -320(%rbp)
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
    movq %rax, -328(%rbp)
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
    movq -320(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -328(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    leaq .STR79(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9072
.L9071:
.L9072:
    movq -272(%rbp), %rax
    pushq %rax
    movq $169, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9081
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
    movq %rax, -352(%rbp)
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
    movq %rax, -360(%rbp)
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
    movq %rax, -368(%rbp)
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
    movq %rax, -376(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -360(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -368(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $3, %rax
    pushq %rax
    movq -376(%rbp), %rax
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
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9082
.L9081:
.L9082:
    movq -272(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9091
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq $0, %rax
    movq %rax, -400(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9101
    leaq .STR81(%rip), %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -400(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9102
.L9101:
.L9102:
    movq -400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9111
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
    movq %rax, -408(%rbp)
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
    movq %rax, -416(%rbp)
    movq $0, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -424(%rbp)
    movq $8, %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -432(%rbp)
    movq $0, %rax
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9121
    leaq .STR82(%rip), %rax
    pushq %rax
    movq -432(%rbp), %rax
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
    jz .L9131
    movq $1, %rax
    pushq %rax
    leaq -440(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9132
.L9131:
.L9132:
    jmp .L9122
.L9121:
.L9122:
    movq -440(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9141
    movq -424(%rbp), %rax
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
    jmp .L9142
.L9141:
.L9142:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -448(%rbp)
    movq $16, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -456(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -408(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $2, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    leaq .STR83(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call expression_create_function_call
    movq %rax, -464(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9112
.L9111:
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
.L9112:
    jmp .L9092
.L9091:
.L9092:
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_is_builtin_function_token
    movq %rax, -480(%rbp)
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9151
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    movq %rax, -488(%rbp)
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_create_expression
    pushq %rax
    leaq -280(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9152
.L9151:
.L9152:
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9161
    leaq .STR117(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $16, %rax  # Load constant TOKEN_LINE_OFFSET
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR118(%rip), %rax
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
    jmp .L9162
.L9161:
.L9162:
    movq -280(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_add_statement
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L8861
.L8862:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L9171
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_return_statement
    movq %rax, -504(%rbp)
    movq -504(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_add_statement
    jmp .L9172
.L9171:
.L9172:
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
    movq $32, %rax  # Load constant SIZEOF_PARSER
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load constant PARSER_LEXER
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $24, %rax  # Load constant PARSER_ARENA
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
    jz .L9181
    leaq .STR119(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L9182
.L9181:
.L9182:
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN
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
    jz .L9191
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN
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
    jz .L9201
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_destroy
    jmp .L9202
.L9201:
.L9202:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L9192
.L9191:
.L9192:
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
    movq $64, %rax  # Load constant SIZEOF_PROGRAM
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq $32, %rax  # Load constant PROGRAM_IMPORTS
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax  # Load constant PROGRAM_TYPES
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $0, %rax  # Load constant PROGRAM_FUNCTIONS
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $48, %rax  # Load constant PROGRAM_GLOBAL_VARS
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load constant PROGRAM_FUNCTION_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax  # Load constant PROGRAM_IMPORT_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $56, %rax  # Load constant PROGRAM_GLOBAL_COUNT
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $12, %rax  # Load constant PROGRAM_FUNCTION_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $28, %rax  # Load constant PROGRAM_TYPE_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $44, %rax  # Load constant PROGRAM_IMPORT_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $60, %rax  # Load constant PROGRAM_GLOBAL_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant PARSER_CURRENT_PROGRAM_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    movq %rax, -24(%rbp)
.L9211:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9212
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
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
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9221
    leaq .STR120(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9222
.L9221:
.L9222:
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9231
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9232
.L9231:
.L9232:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9241
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9242
.L9241:
.L9242:
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9251
    movq $0, %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $56, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9261
    movq $1, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9262
.L9261:
.L9262:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_import
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9281
    leaq .STR121(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L9282
.L9281:
.L9282:
    movq -64(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_import
    jmp .L9272
.L9271:
.L9272:
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9291
    movq $1, %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9292
.L9291:
.L9292:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9301
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -80(%rbp)
.L9311:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9312
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -96(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9321
    leaq .STR122(%rip), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9322
.L9321:
.L9322:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9331
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    movq %rax, -120(%rbp)
.L9341:    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9342
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9351
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9352
.L9351:
    movq $0, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L9352:
    jmp .L9341
.L9342:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9332
.L9331:
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L9332:
    jmp .L9311
.L9312:
    jmp .L9302
.L9301:
.L9302:
    movq $0, %rax
    movq %rax, -160(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9361
    movq $1, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9362
.L9361:
.L9362:
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9371
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_type_definition
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_type
    jmp .L9372
.L9371:
.L9372:
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $163, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9381
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9382
.L9381:
.L9382:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9391
    movq $163, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9401
    leaq .STR123(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L9402
.L9401:
.L9402:
    jmp .L9392
.L9391:
.L9392:
    movq $0, %rax
    movq %rax, -184(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $173, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9411
    movq $1, %rax
    pushq %rax
    leaq -184(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $173, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L9412
.L9411:
.L9412:
    movq $0, %rax
    movq %rax, -192(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9421
    movq $1, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9422
.L9421:
.L9422:
    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9431
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_function
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9441
    leaq .STR124(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
    jz .L9451
    movq $1, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L9452
.L9451:
.L9452:
    movq -200(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_function
    jmp .L9432
.L9431:
.L9432:
    movq $0, %rax
    movq %rax, -208(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9461
    movq $1, %rax
    pushq %rax
    leaq -208(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9462
.L9461:
.L9462:
    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9471
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9481
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9491
    movq $13, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -256(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -264(%rbp)
    movq $0, %rax
    movq %rax, -272(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9501
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9502
.L9501:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_expression
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L9502:
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -296(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -272(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -296(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_global
    jmp .L9492
.L9491:
.L9492:
    jmp .L9482
.L9481:
.L9482:
    jmp .L9472
.L9471:
.L9472:
    movq $0, %rax
    movq %rax, -304(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $164, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9511
    movq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9512
.L9511:
.L9512:
    movq -304(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9521
    movq $164, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -312(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    call token_can_be_identifier
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9531
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -336(%rbp)
    movq -320(%rbp), %rax
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -352(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -360(%rbp)
    movq -352(%rbp), %rax
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -368(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -376(%rbp)
    movq $0, %rax
    movq %rax, -384(%rbp)
    movq $0, %rax
    movq %rax, -392(%rbp)
    movq -376(%rbp), %rax
    pushq %rax
    movq $126, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9541
    movq $1, %rax
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9542
.L9541:
.L9542:
    movq -376(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9551
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9561
    leaq .STR62(%rip), %rax
    pushq %rax
    movq -400(%rbp), %rax
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
    jz .L9571
    movq $1, %rax
    pushq %rax
    leaq -392(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9572
.L9571:
.L9572:
    jmp .L9562
.L9561:
.L9562:
    jmp .L9552
.L9551:
.L9552:
    movq -392(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9581
    movq -376(%rbp), %rax
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -408(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -416(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -424(%rbp)
    movq $0, %rax
    movq %rax, -432(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9591
    leaq .STR30(%rip), %rax
    pushq %rax
    movq -424(%rbp), %rax
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
    jz .L9601
    movq $1, %rax
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9602
.L9601:
.L9602:
    leaq .STR31(%rip), %rax
    pushq %rax
    movq -424(%rbp), %rax
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
    jz .L9611
    movq $2, %rax
    pushq %rax
    leaq -432(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9612
.L9611:
.L9612:
    jmp .L9592
.L9591:
.L9592:
    movq -416(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -440(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -448(%rbp)
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -456(%rbp)
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
    movq $21, %rax
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
    movq -456(%rbp), %rax
    movq %rax, -464(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9621
    movq $8, %rax
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9622
.L9621:
.L9622:
    movq -464(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -472(%rbp)
    movq $0, %rax
    movq %rax, -480(%rbp)
    movq $1, %rax
    movq %rax, -488(%rbp)
.L9631:    movq -488(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9632
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -496(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -504(%rbp)
    movq -504(%rbp), %rax
    pushq %rax
    movq $128, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9641
    movq $0, %rax
    pushq %rax
    leaq -488(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9642
.L9641:
    movq $0, %rax
    movq %rax, -512(%rbp)
    movq -504(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9651
    movq $17, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $1, %rax
    pushq %rax
    leaq -512(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9652
.L9651:
.L9652:
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -520(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -528(%rbp)
    movq $0, %rax
    movq %rax, -536(%rbp)
    movq -528(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9661
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -544(%rbp)
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -552(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9671
    movq -552(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_float
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9672
.L9671:
    movq -552(%rbp), %rax
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L9672:
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9662
.L9661:
    movq -528(%rbp), %rax
    pushq %rax
    movq $186, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9681
    movq -432(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9691
    leaq .STR125(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L9692
.L9691:
.L9692:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -560(%rbp)
    movq -560(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_float
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $186, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9682
.L9681:
    movq -528(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9701
    movq -512(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9711
    leaq .STR126(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L9712
.L9711:
.L9712:
    movq -432(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9721
    leaq .STR127(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L9722
.L9721:
.L9722:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -568(%rbp)
    movq -568(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9702
.L9701:
    movq -528(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9731
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -520(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -576(%rbp)
    movq $0, %rax
    movq %rax, -584(%rbp)
    movq $56, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -592(%rbp)
    movq $48, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -600(%rbp)
    movq $0, %rax
    movq %rax, -608(%rbp)
.L9741:    movq -608(%rbp), %rax
    pushq %rax
    movq -592(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9742
    movq -608(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -600(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -616(%rbp)
    movq -616(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9751
    movq $0, %rax
    pushq %rax
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -624(%rbp)
    movq -624(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9761
    movq -576(%rbp), %rax
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
    jz .L9771
    movq $16, %rax
    pushq %rax
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -632(%rbp)
    movq -632(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9781
    movq $0, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -640(%rbp)
    movq -640(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9791
    movq -432(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9801
    movq $8, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9802
.L9801:
.L9802:
    movq -432(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9811
    movq $8, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call integer_to_float
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9812
.L9811:
.L9812:
    jmp .L9792
.L9791:
.L9792:
    movq -640(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9821
    movq -432(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9831
    movq $8, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9832
.L9831:
.L9832:
    jmp .L9822
.L9821:
.L9822:
    movq -640(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9841
    movq -432(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9851
    movq $8, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    leaq -584(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9852
.L9851:
.L9852:
    jmp .L9842
.L9841:
.L9842:
    jmp .L9782
.L9781:
.L9782:
    movq -592(%rbp), %rax
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9772
.L9771:
.L9772:
    jmp .L9762
.L9761:
.L9762:
    jmp .L9752
.L9751:
.L9752:
    movq -608(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -608(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9741
.L9742:
    movq -584(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9861
    leaq .STR128(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -576(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR129(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    call print_newline
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L9862
.L9861:
.L9862:
    movq $53, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9732
.L9731:
    leaq .STR130(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -528(%rbp), %rax
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
.L9732:
.L9702:
.L9682:
.L9662:
    movq -512(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9871
    movq -432(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9881
    movq $0, %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    call float_to_integer
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    pushq %rax
    popq %rdi
    call integer_to_float
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9882
.L9881:
    movq $0, %rax
    subq -536(%rbp), %rax
    pushq %rax
    leaq -536(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L9882:
    jmp .L9872
.L9871:
.L9872:
    movq -480(%rbp), %rax
    pushq %rax
    movq -464(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9891
    movq -464(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -464(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -464(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -472(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    pushq %rax
    leaq -472(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9892
.L9891:
.L9892:
    movq -536(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -472(%rbp), %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -480(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -480(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -648(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -648(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -656(%rbp)
    movq -656(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9901
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9902
.L9901:
.L9902:
.L9642:
    jmp .L9631
.L9632:
    movq $128, %rax
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
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $26, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -472(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -480(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -432(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L9582
.L9581:
    movq -376(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9911
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -664(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -672(%rbp)
    movq -672(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9912
.L9911:
    movq -376(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9921
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    movq %rax, -680(%rbp)
    movq -680(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_string_literal_owned
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $10, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9922
.L9921:
    movq -376(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9931
    movq $17, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -688(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
    pushq %rax
    movq -688(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -696(%rbp)
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_to_integer
    movq %rax, -704(%rbp)
    movq $0, %rax
    subq -704(%rbp), %rax
    movq %rax, -712(%rbp)
    movq -712(%rbp), %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $11, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L9932
.L9931:
    movq $0, %rax
    pushq %rax
    popq %rdi
    call expression_create_integer
    pushq %rax
    leaq -384(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -376(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
.L9932:
.L9922:
.L9912:
.L9582:
    movq $24, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -720(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -360(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -384(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -720(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -720(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call program_add_global
    jmp .L9532
.L9531:
.L9532:
    jmp .L9522
.L9521:
.L9522:
    movq $0, %rax
    movq %rax, -728(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9941
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9942
.L9941:
.L9942:
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9951
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9952
.L9951:
.L9952:
    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9961
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9962
.L9961:
.L9962:
    movq -208(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9971
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9972
.L9971:
.L9972:
    movq -304(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9981
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9982
.L9981:
.L9982:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L9991
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L9992
.L9991:
.L9992:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10001
    movq $1, %rax
    pushq %rax
    leaq -728(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10002
.L10001:
.L10002:
    movq -728(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10011
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10012
.L10011:
.L10012:
    jmp .L9252
.L9251:
.L9252:
    jmp .L9211
.L9212:
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
    jz .L10021
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10022
.L10021:
.L10022:
    movq $0, %rax  # Load constant EXPR_TYPE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load constant EXPR_BINARY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10031
    movq $8, %rax  # Load constant EXPR_BINARY_LEFT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax  # Load constant EXPR_BINARY_RIGHT
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
    jmp .L10032
.L10031:
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load constant EXPR_UNARY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10041
    movq $8, %rax  # Load constant EXPR_UNARY_OPERAND
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
    jmp .L10042
.L10041:
    movq -16(%rbp), %rax
    pushq %rax
    movq $4, %rax  # Load constant EXPR_CALL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10051
    movq $8, %rax  # Load constant EXPR_CALL_NAME
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
    jmp .L10052
.L10051:
    movq -16(%rbp), %rax
    pushq %rax
    movq $6, %rax  # Load constant EXPR_FIELD_ACCESS
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10061
    movq $8, %rax  # Load constant EXPR_FIELD_OBJECT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $16, %rax  # Load constant EXPR_FIELD_NAME
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
    jmp .L10062
.L10061:
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load constant EXPR_ARRAY_ACCESS
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10071
    movq $8, %rax  # Load constant EXPR_ARRAY_OBJECT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $16, %rax  # Load constant EXPR_ARRAY_INDEX_OFFSET
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
    jmp .L10072
.L10071:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant EXPR_IDENTIFIER
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10081
    movq $8, %rax  # Load constant EXPR_IDENTIFIER_NAME
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
    jmp .L10082
.L10081:
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax  # Load constant EXPR_STRING_LITERAL
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10091
    movq $8, %rax  # Load constant EXPR_STRING_VALUE
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
    jmp .L10092
.L10091:
.L10092:
.L10082:
.L10072:
.L10062:
.L10052:
.L10042:
.L10032:
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
    jz .L10101
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10102
.L10101:
.L10102:
    movq $0, %rax  # Load constant STMT_TYPE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant STMT_LET
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10111
    movq $8, %rax  # Load constant STMT_LET_NAME
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax  # Load constant STMT_LET_VALUE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $24, %rax  # Load constant STMT_LET_TYPE
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
    jmp .L10112
.L10111:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load constant STMT_SET
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10121
    movq $8, %rax  # Load constant STMT_SET_NAME
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $16, %rax  # Load constant STMT_SET_VALUE
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
    jmp .L10122
.L10121:
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax  # Load constant STMT_IF
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10131
    movq $8, %rax  # Load constant STMT_IF_CONDITION
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
    jmp .L10132
.L10131:
    movq -16(%rbp), %rax
    pushq %rax
    movq $6, %rax  # Load constant STMT_WHILE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10141
    movq $8, %rax  # Load constant STMT_WHILE_CONDITION
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
    jmp .L10142
.L10141:
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load constant STMT_FOR
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10151
    movq $8, %rax  # Load constant STMT_FOR_VAR
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $16, %rax  # Load constant STMT_FOR_START
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $24, %rax  # Load constant STMT_FOR_END
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
    jmp .L10152
.L10151:
    movq -16(%rbp), %rax
    pushq %rax
    movq $12, %rax  # Load constant STMT_FOR_EACH
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10161
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
    jmp .L10162
.L10161:
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax  # Load constant STMT_RETURN
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10171
    movq $8, %rax  # Load constant STMT_RETURN_VALUE
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
    jmp .L10172
.L10171:
    movq -16(%rbp), %rax
    pushq %rax
    movq $7, %rax  # Load constant STMT_EXPRESSION
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10181
    movq $8, %rax  # Load constant STMT_EXPR_VALUE
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
    jmp .L10182
.L10181:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax  # Load constant STMT_BREAK
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10191
    jmp .L10192
.L10191:
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax  # Load constant STMT_CONTINUE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10201
    jmp .L10202
.L10201:
.L10202:
.L10192:
.L10182:
.L10172:
.L10162:
.L10152:
.L10142:
.L10132:
.L10122:
.L10112:
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
    jz .L10211
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10212
.L10211:
.L10212:
    movq $0, %rax  # Load constant FUNCTION_NAME
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
    jz .L10221
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10222
.L10221:
.L10222:
    movq $0, %rax  # Load constant TYPE_KIND
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load constant TYPE_PRIMITIVE
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10231
    jmp .L10232
.L10231:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax  # Load constant TYPE_STRUCT
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10241
    movq $8, %rax  # Load constant TYPE_STRUCT_NAME
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
    jmp .L10242
.L10241:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax  # Load constant TYPE_ARRAY
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10251
    movq $8, %rax  # Load constant TYPE_ARRAY_ELEMENT_TYPE
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
    jmp .L10252
.L10251:
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax  # Load constant TYPE_POINTER
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10261
    movq $8, %rax  # Load constant TYPE_POINTER_TARGET_TYPE
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
    jmp .L10262
.L10261:
.L10262:
.L10252:
.L10242:
.L10232:
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
    jz .L10271
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10272
.L10271:
.L10272:
    movq $8, %rax  # Load constant PROGRAM_FUNCTION_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax  # Load constant PROGRAM_FUNCTIONS
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
    jz .L10281
    movq $0, %rax
    movq %rax, -32(%rbp)
.L10291:    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10292
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
    jz .L10301
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call function_destroy
    jmp .L10302
.L10301:
.L10302:
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10291
.L10292:
    jmp .L10282
.L10281:
.L10282:
    movq $24, %rax  # Load constant PROGRAM_TYPE_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq $16, %rax  # Load constant PROGRAM_TYPES
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
    jz .L10311
    movq $0, %rax
    movq %rax, -88(%rbp)
.L10321:    movq -88(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10322
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
    jz .L10331
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call type_destroy
    jmp .L10332
.L10331:
.L10332:
    movq -88(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10321
.L10322:
    jmp .L10312
.L10311:
.L10312:
    movq $40, %rax  # Load constant PROGRAM_IMPORT_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -112(%rbp)
    movq $32, %rax  # Load constant PROGRAM_IMPORTS
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
    jz .L10341
    jmp .L10342
.L10341:
.L10342:
    movq $56, %rax  # Load constant PROGRAM_GLOBAL_COUNT
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -128(%rbp)
    movq $48, %rax  # Load constant PROGRAM_GLOBAL_VARS
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
    jz .L10351
    movq $0, %rax
    movq %rax, -144(%rbp)
.L10361:    movq -144(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10362
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
    jz .L10371
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call statement_destroy
    jmp .L10372
.L10371:
.L10372:
    movq -144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10361
.L10362:
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L10352
.L10351:
.L10352:
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
    jz .L10381
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L10382
.L10381:
.L10382:
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
    jz .L10391
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10392
.L10391:
.L10392:
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
    jz .L10401
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10402
.L10401:
.L10402:
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
    jz .L10411
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L10412
.L10411:
.L10412:
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L10421
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
.L10431:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10432
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L10441
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    jmp .L10442
.L10441:
    movq $0, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L10442:
    jmp .L10431
.L10432:
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
    jmp .L10422
.L10421:
.L10422:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jz .L10451
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10452
.L10451:
.L10452:
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
    jz .L10461
    movq $1, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10462
.L10461:
.L10462:
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10471
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L10481
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10482
.L10481:
.L10482:
    movq -168(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10491
.L10501:    movq -168(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10502
    movq $52, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
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
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jmp .L10501
.L10502:
    movq -168(%rbp), %rax
    pushq %rax
    movq $144, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10511
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L10512
.L10511:
.L10512:
    jmp .L10492
.L10491:
.L10492:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10521
    movq $144, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L10531
    movq $34, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_eat
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jmp .L10532
.L10531:
.L10532:
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
    jmp .L10522
.L10521:
.L10522:
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
    jmp .L10472
.L10471:
.L10472:
    movq -32(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10541
    leaq .STR131(%rip), %rax
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
    jmp .L10542
.L10541:
.L10542:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L10551
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_advance
    movq %rax, -320(%rbp)
    movq $8, %rax  # Load constant PARSER_CURRENT_TOKEN_OFFSET
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq $0, %rax  # Load constant TOKEN_TYPE_OFFSET
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
    jz .L10561
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jmp .L10562
.L10561:
    movq -336(%rbp), %rax
    pushq %rax
    movq $53, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L10571
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
    jmp .L10572
.L10571:
    movq $8, %rax  # Load constant TOKEN_VALUE_OFFSET
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
.L10572:
.L10562:
    jmp .L10552
.L10551:
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate_parser
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L10552:
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

.weak __module_init
__module_init:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Stack space for global initializers
    leave
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
