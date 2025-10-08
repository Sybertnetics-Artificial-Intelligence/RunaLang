.section .data
.globl LEXER_POSITION
LEXER_POSITION:    .quad 0
.globl LEXER_CURRENT_CHAR
LEXER_CURRENT_CHAR:    .quad 0
.globl TOKEN_EOF
TOKEN_EOF:    .quad 0
.globl TOKEN_PROCESS
TOKEN_PROCESS:    .quad 1
.globl TOKEN_CALLED
TOKEN_CALLED:    .quad 2
.globl TOKEN_RETURNS
TOKEN_RETURNS:    .quad 3
.globl TOKEN_INTEGER_TYPE
TOKEN_INTEGER_TYPE:    .quad 4
.globl TOKEN_STRING_TYPE
TOKEN_STRING_TYPE:    .quad 5
.globl TOKEN_CHARACTER_TYPE
TOKEN_CHARACTER_TYPE:    .quad 6
.globl TOKEN_RETURN
TOKEN_RETURN:    .quad 7
.globl TOKEN_END
TOKEN_END:    .quad 8
.globl TOKEN_COLON
TOKEN_COLON:    .quad 9
.globl TOKEN_STRING_LITERAL
TOKEN_STRING_LITERAL:    .quad 10
.globl TOKEN_INTEGER
TOKEN_INTEGER:    .quad 11
.globl TOKEN_LET
TOKEN_LET:    .quad 12
.globl TOKEN_BE
TOKEN_BE:    .quad 13
.globl TOKEN_SET
TOKEN_SET:    .quad 14
.globl TOKEN_TO
TOKEN_TO:    .quad 15
.globl TOKEN_PLUS
TOKEN_PLUS:    .quad 16
.globl TOKEN_MINUS
TOKEN_MINUS:    .quad 17
.globl TOKEN_IF
TOKEN_IF:    .quad 18
.globl TOKEN_OTHERWISE
TOKEN_OTHERWISE:    .quad 19
.globl TOKEN_WHILE
TOKEN_WHILE:    .quad 20
.globl TOKEN_IS
TOKEN_IS:    .quad 21
.globl TOKEN_EQUAL
TOKEN_EQUAL:    .quad 22
.globl TOKEN_NOT_EQUAL
TOKEN_NOT_EQUAL:    .quad 23
.globl TOKEN_LESS
TOKEN_LESS:    .quad 24
.globl TOKEN_GREATER
TOKEN_GREATER:    .quad 25
.globl TOKEN_GREATER_EQUAL
TOKEN_GREATER_EQUAL:    .quad 26
.globl TOKEN_LESS_EQUAL
TOKEN_LESS_EQUAL:    .quad 27
.globl TOKEN_THAN
TOKEN_THAN:    .quad 28
.globl TOKEN_NOT
TOKEN_NOT:    .quad 29
.globl TOKEN_AND
TOKEN_AND:    .quad 30
.globl TOKEN_OR
TOKEN_OR:    .quad 31
.globl TOKEN_THAT
TOKEN_THAT:    .quad 32
.globl TOKEN_TAKES
TOKEN_TAKES:    .quad 33
.globl TOKEN_AS
TOKEN_AS:    .quad 34
.globl TOKEN_MULTIPLIED
TOKEN_MULTIPLIED:    .quad 35
.globl TOKEN_DIVIDED
TOKEN_DIVIDED:    .quad 36
.globl TOKEN_MODULO
TOKEN_MODULO:    .quad 37
.globl TOKEN_BY
TOKEN_BY:    .quad 38
.globl TOKEN_BIT_AND
TOKEN_BIT_AND:    .quad 39
.globl TOKEN_BIT_OR
TOKEN_BIT_OR:    .quad 40
.globl TOKEN_BIT_XOR
TOKEN_BIT_XOR:    .quad 41
.globl TOKEN_BIT_SHIFT_LEFT
TOKEN_BIT_SHIFT_LEFT:    .quad 42
.globl TOKEN_BIT_SHIFT_RIGHT
TOKEN_BIT_SHIFT_RIGHT:    .quad 43
.globl TOKEN_BREAK
TOKEN_BREAK:    .quad 44
.globl TOKEN_CONTINUE
TOKEN_CONTINUE:    .quad 45
.globl TOKEN_OTHERWISE_IF
TOKEN_OTHERWISE_IF:    .quad 46
.globl TOKEN_PRINT
TOKEN_PRINT:    .quad 47
.globl TOKEN_LPAREN
TOKEN_LPAREN:    .quad 48
.globl TOKEN_RPAREN
TOKEN_RPAREN:    .quad 49
.globl TOKEN_TYPE
TOKEN_TYPE:    .quad 50
.globl TOKEN_DOT
TOKEN_DOT:    .quad 51
.globl TOKEN_COMMA
TOKEN_COMMA:    .quad 52
.globl TOKEN_IDENTIFIER
TOKEN_IDENTIFIER:    .quad 53
.globl TOKEN_READ_FILE
TOKEN_READ_FILE:    .quad 54
.globl TOKEN_WRITE_FILE
TOKEN_WRITE_FILE:    .quad 55
.globl TOKEN_IMPORT
TOKEN_IMPORT:    .quad 56
.globl TOKEN_STRING_LENGTH
TOKEN_STRING_LENGTH:    .quad 57
.globl TOKEN_STRING_CHAR_AT
TOKEN_STRING_CHAR_AT:    .quad 58
.globl TOKEN_STRING_SUBSTRING
TOKEN_STRING_SUBSTRING:    .quad 59
.globl TOKEN_STRING_EQUALS
TOKEN_STRING_EQUALS:    .quad 60
.globl TOKEN_ASCII_VALUE_OF
TOKEN_ASCII_VALUE_OF:    .quad 61
.globl TOKEN_IS_DIGIT
TOKEN_IS_DIGIT:    .quad 62
.globl TOKEN_IS_ALPHA
TOKEN_IS_ALPHA:    .quad 63
.globl TOKEN_IS_WHITESPACE
TOKEN_IS_WHITESPACE:    .quad 64
.globl TOKEN_LIST_CREATE
TOKEN_LIST_CREATE:    .quad 65
.globl TOKEN_LIST_APPEND
TOKEN_LIST_APPEND:    .quad 66
.globl TOKEN_LIST_GET
TOKEN_LIST_GET:    .quad 67
.globl TOKEN_LIST_GET_INTEGER
TOKEN_LIST_GET_INTEGER:    .quad 68
.globl TOKEN_LIST_LENGTH
TOKEN_LIST_LENGTH:    .quad 69
.globl TOKEN_LIST_DESTROY
TOKEN_LIST_DESTROY:    .quad 70
.globl TOKEN_LIST_SET
TOKEN_LIST_SET:    .quad 71
.globl TOKEN_LIST_INSERT
TOKEN_LIST_INSERT:    .quad 72
.globl TOKEN_LIST_REMOVE
TOKEN_LIST_REMOVE:    .quad 73
.globl TOKEN_LIST_CLEAR
TOKEN_LIST_CLEAR:    .quad 74
.globl TOKEN_LIST_FIND
TOKEN_LIST_FIND:    .quad 75
.globl TOKEN_LIST_SORT
TOKEN_LIST_SORT:    .quad 76
.globl TOKEN_LIST_REVERSE
TOKEN_LIST_REVERSE:    .quad 77
.globl TOKEN_LIST_COPY
TOKEN_LIST_COPY:    .quad 78
.globl TOKEN_LIST_MERGE
TOKEN_LIST_MERGE:    .quad 79
.globl TOKEN_STRING_CONCAT
TOKEN_STRING_CONCAT:    .quad 80
.globl TOKEN_STRING_COMPARE
TOKEN_STRING_COMPARE:    .quad 81
.globl TOKEN_STRING_TO_INTEGER
TOKEN_STRING_TO_INTEGER:    .quad 82
.globl TOKEN_INTEGER_TO_STRING
TOKEN_INTEGER_TO_STRING:    .quad 83
.globl TOKEN_STRING_FIND
TOKEN_STRING_FIND:    .quad 84
.globl TOKEN_STRING_REPLACE
TOKEN_STRING_REPLACE:    .quad 85
.globl TOKEN_STRING_TRIM
TOKEN_STRING_TRIM:    .quad 86
.globl TOKEN_STRING_SPLIT
TOKEN_STRING_SPLIT:    .quad 87
.globl TOKEN_FILE_OPEN
TOKEN_FILE_OPEN:    .quad 88
.globl TOKEN_FILE_CLOSE
TOKEN_FILE_CLOSE:    .quad 89
.globl TOKEN_FILE_READ_LINE
TOKEN_FILE_READ_LINE:    .quad 90
.globl TOKEN_FILE_WRITE_LINE
TOKEN_FILE_WRITE_LINE:    .quad 91
.globl TOKEN_FILE_EXISTS
TOKEN_FILE_EXISTS:    .quad 92
.globl TOKEN_FILE_DELETE
TOKEN_FILE_DELETE:    .quad 93
.globl TOKEN_FILE_SIZE
TOKEN_FILE_SIZE:    .quad 94
.globl TOKEN_FILE_SEEK
TOKEN_FILE_SEEK:    .quad 95
.globl TOKEN_FILE_TELL
TOKEN_FILE_TELL:    .quad 96
.globl TOKEN_FILE_EOF
TOKEN_FILE_EOF:    .quad 97
.globl TOKEN_SIN
TOKEN_SIN:    .quad 98
.globl TOKEN_COS
TOKEN_COS:    .quad 99
.globl TOKEN_TAN
TOKEN_TAN:    .quad 100
.globl TOKEN_SQRT
TOKEN_SQRT:    .quad 101
.globl TOKEN_POW
TOKEN_POW:    .quad 102
.globl TOKEN_ABS
TOKEN_ABS:    .quad 103
.globl TOKEN_FLOOR
TOKEN_FLOOR:    .quad 104
.globl TOKEN_CEIL
TOKEN_CEIL:    .quad 105
.globl TOKEN_MIN
TOKEN_MIN:    .quad 106
.globl TOKEN_MAX
TOKEN_MAX:    .quad 107
.globl TOKEN_RANDOM
TOKEN_RANDOM:    .quad 108
.globl TOKEN_LOG
TOKEN_LOG:    .quad 109
.globl TOKEN_EXP
TOKEN_EXP:    .quad 110
.globl TOKEN_PIPE
TOKEN_PIPE:    .quad 111
.globl TOKEN_MATCH
TOKEN_MATCH:    .quad 112
.globl TOKEN_WHEN
TOKEN_WHEN:    .quad 113
.globl TOKEN_WITH
TOKEN_WITH:    .quad 114
.globl TOKEN_GET_COMMAND_LINE_ARGS
TOKEN_GET_COMMAND_LINE_ARGS:    .quad 115
.globl TOKEN_EXIT_WITH_CODE
TOKEN_EXIT_WITH_CODE:    .quad 116
.globl TOKEN_PANIC
TOKEN_PANIC:    .quad 117
.globl TOKEN_ASSERT
TOKEN_ASSERT:    .quad 118
.globl TOKEN_ALLOCATE
TOKEN_ALLOCATE:    .quad 119
.globl TOKEN_DEALLOCATE
TOKEN_DEALLOCATE:    .quad 120
.globl TOKEN_INLINE
TOKEN_INLINE:    .quad 121
.globl TOKEN_ASSEMBLY
TOKEN_ASSEMBLY:    .quad 122
.globl TOKEN_NOTE
TOKEN_NOTE:    .quad 123
.globl TOKEN_POINTER
TOKEN_POINTER:    .quad 124
.globl TOKEN_OF
TOKEN_OF:    .quad 125
.globl TOKEN_ARRAY
TOKEN_ARRAY:    .quad 126
.globl TOKEN_LBRACKET
TOKEN_LBRACKET:    .quad 127
.globl TOKEN_RBRACKET
TOKEN_RBRACKET:    .quad 128
.globl TOKEN_ERROR
TOKEN_ERROR:    .quad 129
.globl TOKEN_MEMORY_GET_BYTE
TOKEN_MEMORY_GET_BYTE:    .quad 130
.globl TOKEN_MEMORY_SET_BYTE
TOKEN_MEMORY_SET_BYTE:    .quad 131
.globl TOKEN_COUNT
TOKEN_COUNT:    .quad 132
.globl TOKEN_NEGATIVE
TOKEN_NEGATIVE:    .quad 133
.globl TOKEN_TRUE
TOKEN_TRUE:    .quad 134
.globl TOKEN_FALSE
TOKEN_FALSE:    .quad 135
.globl TOKEN_GETS
TOKEN_GETS:    .quad 136
.globl TOKEN_INCREASED
TOKEN_INCREASED:    .quad 137
.globl TOKEN_DECREASED
TOKEN_DECREASED:    .quad 138
.globl TOKEN_INCREASE
TOKEN_INCREASE:    .quad 139
.globl TOKEN_DECREASE
TOKEN_DECREASE:    .quad 140
.globl TOKEN_MULTIPLY
TOKEN_MULTIPLY:    .quad 141
.globl TOKEN_DIVIDE
TOKEN_DIVIDE:    .quad 142
.globl TOKEN_FOR
TOKEN_FOR:    .quad 143
.globl TOKEN_FROM
TOKEN_FROM:    .quad 144
.globl TOKEN_EACH
TOKEN_EACH:    .quad 145
.globl TOKEN_LBRACE
TOKEN_LBRACE:    .quad 146
.globl TOKEN_RBRACE
TOKEN_RBRACE:    .quad 147
.globl TOKEN_AT
TOKEN_AT:    .quad 148
.globl TOKEN_INDEX
TOKEN_INDEX:    .quad 149
.globl TOKEN_KEY
TOKEN_KEY:    .quad 150
.globl TOKEN_LENGTH
TOKEN_LENGTH:    .quad 151
.globl TOKEN_IN
TOKEN_IN:    .quad 152
.globl TOKEN_WHERE
TOKEN_WHERE:    .quad 153
.globl TOKEN_AN
TOKEN_AN:    .quad 154
.globl TOKEN_A
TOKEN_A:    .quad 155
.globl TOKEN_CONTAINING
TOKEN_CONTAINING:    .quad 156
.globl TOKEN_DOLLAR
TOKEN_DOLLAR:    .quad 157
.globl TOKEN_THE
TOKEN_THE:    .quad 158
.globl TOKEN_LIST
TOKEN_LIST:    .quad 159
.globl TOKEN_DICTIONARY
TOKEN_DICTIONARY:    .quad 160
.globl TOKEN_UNDERSCORE
TOKEN_UNDERSCORE:    .quad 161
.globl TOKEN_LAMBDA
TOKEN_LAMBDA:    .quad 162
.globl TOKEN_CHARACTER_LITERAL
TOKEN_CHARACTER_LITERAL:    .quad 163
.globl TOKEN_THROUGH
TOKEN_THROUGH:    .quad 164

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
.STR0:    .string "End"
.STR1:    .string "Note"
.STR2:    .string "[LEXER ERROR] Unterminated string literal at line "
.STR3:    .string ", column "
.STR4:    .string "Unterminated string"
.STR5:    .string "[LEXER ERROR] Invalid character literal at line "
.STR6:    .string "Invalid character literal"
.STR7:    .string "[LEXER ERROR] Unexpected character '"
.STR8:    .string "' at line "
.STR9:    .string "Unexpected character"
.STR10:    .string "Process"
.STR11:    .string "Print"
.STR12:    .string "called"
.STR13:    .string "containing"
.STR14:    .string "returns"
.STR15:    .string "Integer"
.STR16:    .string "If"
.STR17:    .string "Increase"
.STR18:    .string "Inline"
.STR19:    .string "Import"
.STR20:    .string "Assembly"
.STR21:    .string "String"
.STR22:    .string "Set"
.STR23:    .string "Character"
.STR24:    .string "Continue"
.STR25:    .string "Return"
.STR26:    .string "Let"
.STR27:    .string "be"
.STR28:    .string "by"
.STR29:    .string "bit_and"
.STR30:    .string "bit_or"
.STR31:    .string "bit_xor"
.STR32:    .string "bit_shift_left"
.STR33:    .string "bit_shift_right"
.STR34:    .string "to"
.STR35:    .string "takes"
.STR36:    .string "than"
.STR37:    .string "that"
.STR38:    .string "true"
.STR39:    .string "the"
.STR40:    .string "through"
.STR41:    .string "plus"
.STR42:    .string "minus"
.STR43:    .string "multiplied"
.STR44:    .string "modulo"
.STR45:    .string "is"
.STR46:    .string "in"
.STR47:    .string "index"
.STR48:    .string "increased"
.STR49:    .string "equal"
.STR50:    .string "each"
.STR51:    .string "less"
.STR52:    .string "length"
.STR53:    .string "lambda"
.STR54:    .string "greater"
.STR55:    .string "gets"
.STR56:    .string "not"
.STR57:    .string "negative"
.STR58:    .string "and"
.STR59:    .string "as"
.STR60:    .string "at"
.STR61:    .string "an"
.STR62:    .string "array"
.STR63:    .string "or"
.STR64:    .string "of"
.STR65:    .string "Otherwise"
.STR66:    .string "While"
.STR67:    .string "When"
.STR68:    .string "Type"
.STR69:    .string "Break"
.STR70:    .string "false"
.STR71:    .string "from"
.STR72:    .string "divided"
.STR73:    .string "decreased"
.STR74:    .string "Display"
.STR75:    .string "Decrease"
.STR76:    .string "Divide"
.STR77:    .string "Multiply"
.STR78:    .string "Match"
.STR79:    .string "For"
.STR80:    .string "where"
.STR81:    .string "with"
.STR82:    .string "key"
.STR83:    .string "string_length"
.STR84:    .string "read_file"
.STR85:    .string "write_file"
.STR86:    .string "memory_get_byte"
.STR87:    .string "memory_set_byte"
.STR88:    .string "-"
.STR89:    .string ":"
.STR90:    .string "("
.STR91:    .string ")"
.STR92:    .string "["
.STR93:    .string "]"
.STR94:    .string "."
.STR95:    .string ","
.STR96:    .string "|"
.STR97:    .string "$"
.STR98:    .string "_"
.STR99:    .string "{"
.STR100:    .string "}"
.text


.globl string_copy
string_copy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq $1, %rax
    movq %rax, -32(%rbp)
.L1:    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L12
.L11:
    movq -24(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L12:
    jmp .L1
.L2:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_copy_n
string_copy_n:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
.L21:    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L22
    movq -24(%rbp), %rax
    addq -40(%rbp), %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
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
    jmp .L21
.L22:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_set_char
string_set_char:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
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


.globl lexer_advance
lexer_advance:
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
    call memory_get_byte@PLT
    movq %rax, -16(%rbp)
    movq $10, %rax
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $12, %rax
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
    movq -40(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L32
.L31:
.L32:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    addq $1, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -56(%rbp), %rax
    pushq %rax
    leaq LEXER_POSITION(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
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
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -88(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq $0, %rax
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
    pushq %rax
    leaq LEXER_CURRENT_CHAR(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
    jmp .L42
.L41:
    movq -56(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -96(%rbp), %rax
    pushq %rax
    leaq LEXER_CURRENT_CHAR(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
.L42:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_skip_whitespace
lexer_skip_whitespace:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $1, %rax
    movq %rax, -16(%rbp)
.L51:    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L52
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L62
.L61:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_whitespace@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L72
.L71:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -40(%rbp)
.L72:
.L62:
    jmp .L51
.L52:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_skip_note_comment
lexer_skip_note_comment:
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
    call memory_get_byte@PLT
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L81:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L82
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq $9, %rax
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    jmp .L92
.L91:
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    jmp .L102
.L101:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L102:
.L92:
    jmp .L81
.L82:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $58, %rax
    movq %rax, -64(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L112
.L111:
.L112:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -72(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $10, %rax
    movq %rax, -80(%rbp)
    movq $13, %rax
    movq %rax, -88(%rbp)
    movq $32, %rax
    movq %rax, -32(%rbp)
    movq $9, %rax
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq $1, %rax
    movq %rax, -120(%rbp)
.L121:    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L122
    movq -16(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -128(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L132
.L131:
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -136(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L142
.L141:
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq $0, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L152
.L151:
    movq -16(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L161
    movq $0, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L162
.L161:
    movq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L162:
.L152:
    movq $0, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L142:
.L132:
    jmp .L121
.L122:
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -144(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L182
.L181:
.L182:
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -152(%rbp)
    jmp .L192
.L191:
.L192:
    movq $1, %rax
    movq %rax, -160(%rbp)
    movq $1, %rax
    movq %rax, -168(%rbp)
.L201:    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L202
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $0, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L212
.L211:
    movq $58, %rax
    movq %rax, -64(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -184(%rbp)
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -208(%rbp)
    movq $1, %rax
    movq %rax, -216(%rbp)
.L231:    movq -216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L232
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -224(%rbp)
    jmp .L242
.L241:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L251
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -232(%rbp)
    jmp .L252
.L251:
    movq -16(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -240(%rbp)
    jmp .L262
.L261:
    movq $0, %rax
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L262:
.L252:
.L242:
    jmp .L231
.L232:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -248(%rbp)
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -248(%rbp), %rax
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
    jz .L281
    movq $1, %rax
    movq %rax, -256(%rbp)
.L291:    movq -256(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L292
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -264(%rbp)
    jmp .L302
.L301:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -272(%rbp)
    jmp .L312
.L311:
    movq -16(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -280(%rbp)
    jmp .L322
.L321:
    movq $0, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L322:
.L312:
.L302:
    jmp .L291
.L292:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L331
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -288(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -288(%rbp), %rax
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
    jz .L341
    movq -168(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L352
.L351:
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L352:
    jmp .L342
.L341:
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L342:
    jmp .L332
.L331:
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L332:
    jmp .L282
.L281:
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L282:
    jmp .L272
.L271:
.L272:
    jmp .L222
.L221:
    movq -16(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -296(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -304(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -304(%rbp), %rax
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
    jz .L371
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    movq -168(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -312(%rbp)
    jmp .L382
.L381:
.L382:
    jmp .L372
.L371:
.L372:
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L362
.L361:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -320(%rbp)
.L362:
.L222:
.L212:
    jmp .L201
.L202:
    jmp .L172
.L171:
    movq $1, %rax
    movq %rax, -328(%rbp)
.L391:    movq -328(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L392
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    movq $0, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L402
.L401:
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    movq $0, %rax
    pushq %rax
    leaq -328(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L412
.L411:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -336(%rbp)
.L412:
.L402:
    jmp .L391
.L392:
.L172:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl token_create_owned
token_create_owned:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq $24, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -48(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl token_create
token_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq $24, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -48(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L422
.L421:
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
.L422:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_read_string_literal
lexer_read_string_literal:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -16(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq $1, %rax
    movq %rax, -40(%rbp)
.L431:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L432
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq $34, %rax
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L442
.L441:
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L451
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L452
.L451:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
.L452:
.L442:
    jmp .L431
.L432:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq $34, %rax
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    subq -32(%rbp), %rax
    movq %rax, -96(%rbp)
    movq $1, %rax
    movq %rax, -104(%rbp)
    movq -96(%rbp), %rax
    addq -104(%rbp), %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call string_copy_n
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -136(%rbp)
    movq -120(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L462
.L461:
.L462:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_read_character_literal
lexer_read_character_literal:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -16(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    movq $39, %rax
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L471
    movq $-1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L472
.L471:
.L472:
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    movq $-1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L482
.L481:
.L482:
    movq $92, %rax
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L491
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -64(%rbp)
    movq $110, %rax
    movq %rax, -72(%rbp)
    movq $116, %rax
    movq %rax, -80(%rbp)
    movq $114, %rax
    movq %rax, -88(%rbp)
    movq $48, %rax
    movq %rax, -96(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L501
    movq $10, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L502
.L501:
    movq -64(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L511
    movq $9, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L512
.L511:
    movq -64(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L521
    movq $13, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L522
.L521:
    movq -64(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq $0, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L532
.L531:
    movq -64(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L541
    movq $92, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L542
.L541:
    movq -64(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L551
    movq $39, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L552
.L551:
    movq $-1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L552:
.L542:
.L532:
.L522:
.L512:
.L502:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -104(%rbp)
    jmp .L492
.L491:
    movq -24(%rbp), %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -112(%rbp)
.L492:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L561
    movq $-1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L562
.L561:
.L562:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -128(%rbp)
    movq -48(%rbp), %rax
    addq $256, %rax
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_read_word
lexer_read_word:
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
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, -24(%rbp)
    movq $1, %rax
    movq %rax, -32(%rbp)
.L571:    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L572
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L581
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L582
.L581:
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_alnum_char
    movq %rax, -48(%rbp)
    movq $95, %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
    jmp .L592
.L591:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L601
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -72(%rbp)
    jmp .L602
.L601:
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L602:
.L592:
.L582:
    jmp .L571
.L572:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    subq -24(%rbp), %rax
    movq %rax, -88(%rbp)
    movq $1, %rax
    movq %rax, -96(%rbp)
    movq -88(%rbp), %rax
    addq -96(%rbp), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call string_copy_n
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq -112(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_read_integer
lexer_read_integer:
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
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, -24(%rbp)
    movq $1, %rax
    movq %rax, -32(%rbp)
.L611:    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L612
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L621
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L622
.L621:
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    jmp .L632
.L631:
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L632:
.L622:
    jmp .L611
.L612:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    subq -24(%rbp), %rax
    movq %rax, -72(%rbp)
    movq $1, %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call string_copy_n
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_create
lexer_create:
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
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
    leaq LEXER_POSITION(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $1, %rax
    pushq %rax
    movq $16, %rax
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
    call string_length@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -48(%rbp), %rax
    pushq %rax
    leaq LEXER_CURRENT_CHAR(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_destroy
lexer_destroy:
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
    jz .L641
    movq $0, %rax
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
    call deallocate@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L642
.L641:
.L642:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_next_token
lexer_next_token:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $1, %rax
    movq %rax, -16(%rbp)
.L651:    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L652
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L661
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L662
.L661:
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_whitespace@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L671
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_whitespace
    movq %rax, -56(%rbp)
    jmp .L672
.L671:
    movq $34, %rax
    movq %rax, -64(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L681
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_string_literal
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L691
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    movq $10, %rax  # Load compile-time constant TOKEN_STRING_LITERAL
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L692
.L691:
    leaq .STR2(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR3(%rip), %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    leaq .STR4(%rip), %rax
    movq %rax, -104(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq $129, %rax  # Load compile-time constant TOKEN_ERROR
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L692:
    jmp .L682
.L681:
    movq $39, %rax
    movq %rax, -120(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L701
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_character_literal
    movq %rax, -128(%rbp)
    movq $0, %rax
    subq $1, %rax
    movq %rax, -136(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq -128(%rbp), %rax
    subq $256, %rax
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, -152(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    movq $163, %rax  # Load compile-time constant TOKEN_CHARACTER_LITERAL
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L712
.L711:
    leaq .STR5(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR3(%rip), %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    leaq .STR6(%rip), %rax
    movq %rax, -104(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq $129, %rax  # Load compile-time constant TOKEN_ERROR
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L712:
    jmp .L702
.L701:
.L702:
    movq $45, %rax
    movq %rax, -200(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    addq $1, %rax
    movq %rax, -208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -232(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L731
    movq -208(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L741
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -256(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_integer
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    addq $2, %rax
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -288(%rbp)
    movq $45, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    movq %rax, -296(%rbp)
.L751:    movq -296(%rbp), %rax
    pushq %rax
    movq -272(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L752
    movq -296(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -296(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L751
.L752:
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant TOKEN_INTEGER
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L742
.L741:
.L742:
    jmp .L732
.L731:
.L732:
    jmp .L722
.L721:
.L722:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L761
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_integer
    movq %rax, -264(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant TOKEN_INTEGER
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L762
.L761:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_alpha
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L771
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -352(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L781
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    call determine_token_type
    movq %rax, -368(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    movq -368(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L782
.L781:
.L782:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_note_comment
    movq %rax, -384(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L772
.L771:
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call check_single_char_token
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L791
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L792
.L791:
    leaq .STR7(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_char
    leaq .STR8(%rip), %rax
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR3(%rip), %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -424(%rbp)
    leaq .STR9(%rip), %rax
    movq %rax, -104(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq $129, %rax  # Load compile-time constant TOKEN_ERROR
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L792:
.L772:
.L762:
.L682:
.L672:
.L662:
    jmp .L651
.L652:
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant TOKEN_EOF
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl determine_token_type
determine_token_type:
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
    call memory_get_byte@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $80, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L801
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_P
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L802
.L801:
    movq -16(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L811
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_c
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L812
.L811:
    movq -16(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L821
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_r
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L822
.L821:
    movq -16(%rbp), %rax
    pushq %rax
    movq $73, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L831
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_I
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L832
.L831:
    movq -16(%rbp), %rax
    pushq %rax
    movq $65, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L841
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_A
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L842
.L841:
    movq -16(%rbp), %rax
    pushq %rax
    movq $83, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L851
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_S
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L852
.L851:
    movq -16(%rbp), %rax
    pushq %rax
    movq $67, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L861
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_C
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L862
.L861:
    movq -16(%rbp), %rax
    pushq %rax
    movq $82, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_R
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L872
.L871:
    movq -16(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L881
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_E
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L882
.L881:
    movq -16(%rbp), %rax
    pushq %rax
    movq $76, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_L
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L892
.L891:
    movq -16(%rbp), %rax
    pushq %rax
    movq $98, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L901
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_b
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L902
.L901:
    movq -16(%rbp), %rax
    pushq %rax
    movq $115, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L911
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_s
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L912
.L911:
    movq -16(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L921
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_t
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L922
.L921:
    movq -16(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_p
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L932
.L931:
    movq -16(%rbp), %rax
    pushq %rax
    movq $109, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_m
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L942
.L941:
    movq -16(%rbp), %rax
    pushq %rax
    movq $105, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L951
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_i
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L952
.L951:
    movq -16(%rbp), %rax
    pushq %rax
    movq $101, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_e
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L962
.L961:
    movq -16(%rbp), %rax
    pushq %rax
    movq $108, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L971
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_l
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L972
.L971:
    movq -16(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L981
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_g
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L982
.L981:
    movq -16(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L991
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_n
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L992
.L991:
    movq -16(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_N
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1002
.L1001:
    movq -16(%rbp), %rax
    pushq %rax
    movq $97, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1011
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_a
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1012
.L1011:
    movq -16(%rbp), %rax
    pushq %rax
    movq $111, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1021
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_o
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1022
.L1021:
    movq -16(%rbp), %rax
    pushq %rax
    movq $79, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_O
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1032
.L1031:
    movq -16(%rbp), %rax
    pushq %rax
    movq $87, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1041
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_W
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1042
.L1041:
    movq -16(%rbp), %rax
    pushq %rax
    movq $84, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_T
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1052
.L1051:
    movq -16(%rbp), %rax
    pushq %rax
    movq $66, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_B
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1062
.L1061:
    movq -16(%rbp), %rax
    pushq %rax
    movq $102, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_f
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1072
.L1071:
    movq -16(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1081
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_d
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1082
.L1081:
    movq -16(%rbp), %rax
    pushq %rax
    movq $68, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_D
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1092
.L1091:
    movq -16(%rbp), %rax
    pushq %rax
    movq $77, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_M
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1102
.L1101:
    movq -16(%rbp), %rax
    pushq %rax
    movq $70, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_F
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1112
.L1111:
    movq -16(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_w
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1122
.L1121:
    movq -16(%rbp), %rax
    pushq %rax
    movq $107, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_k
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1132
.L1131:
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_builtin_functions
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_P
check_keywords_P:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR10(%rip), %rax
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
    jz .L1141
    movq $1, %rax  # Load compile-time constant TOKEN_PROCESS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1142
.L1141:
    leaq .STR11(%rip), %rax
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
    jz .L1151
    movq $47, %rax  # Load compile-time constant TOKEN_PRINT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1152
.L1151:
.L1152:
.L1142:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_c
check_keywords_c:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR12(%rip), %rax
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
    jz .L1161
    movq $2, %rax  # Load compile-time constant TOKEN_CALLED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1162
.L1161:
    leaq .STR13(%rip), %rax
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
    jz .L1171
    movq $156, %rax  # Load compile-time constant TOKEN_CONTAINING
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1172
.L1171:
.L1172:
.L1162:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_r
check_keywords_r:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR14(%rip), %rax
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
    jz .L1181
    movq $3, %rax  # Load compile-time constant TOKEN_RETURNS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1182
.L1181:
.L1182:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_I
check_keywords_I:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR15(%rip), %rax
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
    jz .L1191
    movq $4, %rax  # Load compile-time constant TOKEN_INTEGER_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1192
.L1191:
    leaq .STR16(%rip), %rax
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
    jz .L1201
    movq $18, %rax  # Load compile-time constant TOKEN_IF
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1202
.L1201:
    leaq .STR17(%rip), %rax
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
    jz .L1211
    movq $139, %rax  # Load compile-time constant TOKEN_INCREASE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1212
.L1211:
    leaq .STR18(%rip), %rax
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
    jz .L1221
    movq $121, %rax  # Load compile-time constant TOKEN_INLINE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1222
.L1221:
    leaq .STR19(%rip), %rax
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
    jz .L1231
    movq $56, %rax  # Load compile-time constant TOKEN_IMPORT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1232
.L1231:
.L1232:
.L1222:
.L1212:
.L1202:
.L1192:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_A
check_keywords_A:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR20(%rip), %rax
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
    jz .L1241
    movq $122, %rax  # Load compile-time constant TOKEN_ASSEMBLY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1242
.L1241:
.L1242:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_S
check_keywords_S:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR21(%rip), %rax
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
    jz .L1251
    movq $5, %rax  # Load compile-time constant TOKEN_STRING_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1252
.L1251:
    leaq .STR22(%rip), %rax
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
    jz .L1261
    movq $14, %rax  # Load compile-time constant TOKEN_SET
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1262
.L1261:
.L1262:
.L1252:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_C
check_keywords_C:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR23(%rip), %rax
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
    jz .L1271
    movq $6, %rax  # Load compile-time constant TOKEN_CHARACTER_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1272
.L1271:
    leaq .STR24(%rip), %rax
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
    jz .L1281
    movq $45, %rax  # Load compile-time constant TOKEN_CONTINUE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1282
.L1281:
.L1282:
.L1272:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_R
check_keywords_R:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR25(%rip), %rax
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
    jz .L1291
    movq $7, %rax  # Load compile-time constant TOKEN_RETURN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1292
.L1291:
.L1292:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_E
check_keywords_E:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR0(%rip), %rax
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
    jz .L1301
    movq $8, %rax  # Load compile-time constant TOKEN_END
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1302
.L1301:
.L1302:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_L
check_keywords_L:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR26(%rip), %rax
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
    jz .L1311
    movq $12, %rax  # Load compile-time constant TOKEN_LET
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1312
.L1311:
.L1312:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_b
check_keywords_b:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR27(%rip), %rax
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
    jz .L1321
    movq $13, %rax  # Load compile-time constant TOKEN_BE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1322
.L1321:
    leaq .STR28(%rip), %rax
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
    jz .L1331
    movq $38, %rax  # Load compile-time constant TOKEN_BY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1332
.L1331:
    leaq .STR29(%rip), %rax
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
    jz .L1341
    movq $39, %rax  # Load compile-time constant TOKEN_BIT_AND
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1342
.L1341:
    leaq .STR30(%rip), %rax
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
    jz .L1351
    movq $40, %rax  # Load compile-time constant TOKEN_BIT_OR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1352
.L1351:
    leaq .STR31(%rip), %rax
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
    jz .L1361
    movq $41, %rax  # Load compile-time constant TOKEN_BIT_XOR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1362
.L1361:
    leaq .STR32(%rip), %rax
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
    jz .L1371
    movq $42, %rax  # Load compile-time constant TOKEN_BIT_SHIFT_LEFT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1372
.L1371:
    leaq .STR33(%rip), %rax
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
    jz .L1381
    movq $43, %rax  # Load compile-time constant TOKEN_BIT_SHIFT_RIGHT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1382
.L1381:
.L1382:
.L1372:
.L1362:
.L1352:
.L1342:
.L1332:
.L1322:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_s
check_keywords_s:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_t
check_keywords_t:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR34(%rip), %rax
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
    jz .L1391
    movq $15, %rax  # Load compile-time constant TOKEN_TO
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1392
.L1391:
    leaq .STR35(%rip), %rax
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
    jz .L1401
    movq $33, %rax  # Load compile-time constant TOKEN_TAKES
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1402
.L1401:
    leaq .STR36(%rip), %rax
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
    jz .L1411
    movq $28, %rax  # Load compile-time constant TOKEN_THAN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1412
.L1411:
    leaq .STR37(%rip), %rax
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
    jz .L1421
    movq $32, %rax  # Load compile-time constant TOKEN_THAT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1422
.L1421:
    leaq .STR38(%rip), %rax
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
    jz .L1431
    movq $134, %rax  # Load compile-time constant TOKEN_TRUE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1432
.L1431:
    leaq .STR39(%rip), %rax
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
    jz .L1441
    movq $158, %rax  # Load compile-time constant TOKEN_THE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1442
.L1441:
    leaq .STR40(%rip), %rax
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
    jz .L1451
    movq $164, %rax  # Load compile-time constant TOKEN_THROUGH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1452
.L1451:
.L1452:
.L1442:
.L1432:
.L1422:
.L1412:
.L1402:
.L1392:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_p
check_keywords_p:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR41(%rip), %rax
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
    jz .L1461
    movq $16, %rax  # Load compile-time constant TOKEN_PLUS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1462
.L1461:
.L1462:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_m
check_keywords_m:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR42(%rip), %rax
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
    jz .L1471
    movq $17, %rax  # Load compile-time constant TOKEN_MINUS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1472
.L1471:
    leaq .STR43(%rip), %rax
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
    jz .L1481
    movq $35, %rax  # Load compile-time constant TOKEN_MULTIPLIED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1482
.L1481:
    leaq .STR44(%rip), %rax
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
    jz .L1491
    movq $37, %rax  # Load compile-time constant TOKEN_MODULO
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1492
.L1491:
.L1492:
.L1482:
.L1472:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_i
check_keywords_i:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR45(%rip), %rax
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
    jz .L1501
    movq $21, %rax  # Load compile-time constant TOKEN_IS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1502
.L1501:
    leaq .STR46(%rip), %rax
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
    jz .L1511
    movq $152, %rax  # Load compile-time constant TOKEN_IN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1512
.L1511:
    leaq .STR47(%rip), %rax
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
    jz .L1521
    movq $149, %rax  # Load compile-time constant TOKEN_INDEX
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1522
.L1521:
    leaq .STR48(%rip), %rax
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
    jz .L1531
    movq $137, %rax  # Load compile-time constant TOKEN_INCREASED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1532
.L1531:
.L1532:
.L1522:
.L1512:
.L1502:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_e
check_keywords_e:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR49(%rip), %rax
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
    jz .L1541
    movq $22, %rax  # Load compile-time constant TOKEN_EQUAL
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1542
.L1541:
    leaq .STR50(%rip), %rax
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
    jz .L1551
    movq $145, %rax  # Load compile-time constant TOKEN_EACH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1552
.L1551:
.L1552:
.L1542:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_l
check_keywords_l:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR51(%rip), %rax
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
    jz .L1561
    movq $24, %rax  # Load compile-time constant TOKEN_LESS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1562
.L1561:
    leaq .STR52(%rip), %rax
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
    jz .L1571
    movq $151, %rax  # Load compile-time constant TOKEN_LENGTH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1572
.L1571:
    leaq .STR53(%rip), %rax
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
    jz .L1581
    movq $162, %rax  # Load compile-time constant TOKEN_LAMBDA
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1582
.L1581:
.L1582:
.L1572:
.L1562:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_g
check_keywords_g:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR54(%rip), %rax
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
    jz .L1591
    movq $25, %rax  # Load compile-time constant TOKEN_GREATER
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1592
.L1591:
    leaq .STR55(%rip), %rax
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
    jz .L1601
    movq $136, %rax  # Load compile-time constant TOKEN_GETS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1602
.L1601:
.L1602:
.L1592:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_n
check_keywords_n:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR56(%rip), %rax
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
    jz .L1611
    movq $29, %rax  # Load compile-time constant TOKEN_NOT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1612
.L1611:
    leaq .STR57(%rip), %rax
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
    jz .L1621
    movq $133, %rax  # Load compile-time constant TOKEN_NEGATIVE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1622
.L1621:
.L1622:
.L1612:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_N
check_keywords_N:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR1(%rip), %rax
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
    jz .L1631
    movq $123, %rax  # Load compile-time constant TOKEN_NOTE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1632
.L1631:
.L1632:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_a
check_keywords_a:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR58(%rip), %rax
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
    jz .L1641
    movq $30, %rax  # Load compile-time constant TOKEN_AND
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1642
.L1641:
    leaq .STR59(%rip), %rax
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
    jz .L1651
    movq $34, %rax  # Load compile-time constant TOKEN_AS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1652
.L1651:
    leaq .STR60(%rip), %rax
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
    jz .L1661
    movq $148, %rax  # Load compile-time constant TOKEN_AT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1662
.L1661:
    leaq .STR61(%rip), %rax
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
    jz .L1671
    movq $154, %rax  # Load compile-time constant TOKEN_AN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1672
.L1671:
    leaq .STR62(%rip), %rax
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
    jz .L1681
    movq $126, %rax  # Load compile-time constant TOKEN_ARRAY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1682
.L1681:
.L1682:
.L1672:
.L1662:
.L1652:
.L1642:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_o
check_keywords_o:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR63(%rip), %rax
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
    jz .L1691
    movq $31, %rax  # Load compile-time constant TOKEN_OR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1692
.L1691:
    leaq .STR64(%rip), %rax
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
    jz .L1701
    movq $125, %rax  # Load compile-time constant TOKEN_OF
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1702
.L1701:
.L1702:
.L1692:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_O
check_keywords_O:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR65(%rip), %rax
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
    jz .L1711
    movq $19, %rax  # Load compile-time constant TOKEN_OTHERWISE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1712
.L1711:
.L1712:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_W
check_keywords_W:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR66(%rip), %rax
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
    jz .L1721
    movq $20, %rax  # Load compile-time constant TOKEN_WHILE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1722
.L1721:
    leaq .STR67(%rip), %rax
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
    jz .L1731
    movq $113, %rax  # Load compile-time constant TOKEN_WHEN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1732
.L1731:
.L1732:
.L1722:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_T
check_keywords_T:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR68(%rip), %rax
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
    jz .L1741
    movq $50, %rax  # Load compile-time constant TOKEN_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1742
.L1741:
.L1742:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_B
check_keywords_B:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR69(%rip), %rax
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
    jz .L1751
    movq $44, %rax  # Load compile-time constant TOKEN_BREAK
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1752
.L1751:
.L1752:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_f
check_keywords_f:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR70(%rip), %rax
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
    jz .L1761
    movq $135, %rax  # Load compile-time constant TOKEN_FALSE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1762
.L1761:
    leaq .STR71(%rip), %rax
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
    jz .L1771
    movq $144, %rax  # Load compile-time constant TOKEN_FROM
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1772
.L1771:
.L1772:
.L1762:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_d
check_keywords_d:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR72(%rip), %rax
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
    jz .L1781
    movq $36, %rax  # Load compile-time constant TOKEN_DIVIDED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1782
.L1781:
    leaq .STR73(%rip), %rax
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
    jz .L1791
    movq $138, %rax  # Load compile-time constant TOKEN_DECREASED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1792
.L1791:
.L1792:
.L1782:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_D
check_keywords_D:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR74(%rip), %rax
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
    jz .L1801
    movq $47, %rax  # Load compile-time constant TOKEN_PRINT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1802
.L1801:
    leaq .STR75(%rip), %rax
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
    jz .L1811
    movq $140, %rax  # Load compile-time constant TOKEN_DECREASE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1812
.L1811:
    leaq .STR76(%rip), %rax
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
    jz .L1821
    movq $142, %rax  # Load compile-time constant TOKEN_DIVIDE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1822
.L1821:
.L1822:
.L1812:
.L1802:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_M
check_keywords_M:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR77(%rip), %rax
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
    jz .L1831
    movq $141, %rax  # Load compile-time constant TOKEN_MULTIPLY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1832
.L1831:
    leaq .STR78(%rip), %rax
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
    jz .L1841
    movq $112, %rax  # Load compile-time constant TOKEN_MATCH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1842
.L1841:
.L1842:
.L1832:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_F
check_keywords_F:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR79(%rip), %rax
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
    jz .L1851
    movq $143, %rax  # Load compile-time constant TOKEN_FOR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1852
.L1851:
.L1852:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_w
check_keywords_w:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR80(%rip), %rax
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
    jz .L1861
    movq $153, %rax  # Load compile-time constant TOKEN_WHERE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1862
.L1861:
    leaq .STR81(%rip), %rax
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
    jz .L1871
    movq $114, %rax  # Load compile-time constant TOKEN_WITH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1872
.L1871:
.L1872:
.L1862:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_k
check_keywords_k:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR82(%rip), %rax
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
    jz .L1881
    movq $150, %rax  # Load compile-time constant TOKEN_KEY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1882
.L1881:
.L1882:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_builtin_functions
check_builtin_functions:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR69(%rip), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1891
    movq $44, %rax  # Load compile-time constant TOKEN_BREAK
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1892
.L1891:
.L1892:
    leaq .STR24(%rip), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1901
    movq $45, %rax  # Load compile-time constant TOKEN_CONTINUE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1902
.L1901:
.L1902:
    leaq .STR11(%rip), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1911
    movq $47, %rax  # Load compile-time constant TOKEN_PRINT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1912
.L1911:
.L1912:
    leaq .STR74(%rip), %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1921
    movq $47, %rax  # Load compile-time constant TOKEN_PRINT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1922
.L1921:
.L1922:
    leaq .STR68(%rip), %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1931
    movq $50, %rax  # Load compile-time constant TOKEN_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1932
.L1931:
.L1932:
    leaq .STR19(%rip), %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1941
    movq $56, %rax  # Load compile-time constant TOKEN_IMPORT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1942
.L1941:
.L1942:
    leaq .STR83(%rip), %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1951
    movq $57, %rax  # Load compile-time constant TOKEN_STRING_LENGTH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1952
.L1951:
.L1952:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_more_builtins
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_more_builtins
check_more_builtins:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR84(%rip), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1961
    movq $54, %rax  # Load compile-time constant TOKEN_READ_FILE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1962
.L1961:
.L1962:
    leaq .STR85(%rip), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1971
    movq $55, %rax  # Load compile-time constant TOKEN_WRITE_FILE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1972
.L1971:
.L1972:
    leaq .STR86(%rip), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1981
    movq $130, %rax  # Load compile-time constant TOKEN_MEMORY_GET_BYTE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1982
.L1981:
.L1982:
    leaq .STR87(%rip), %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1991
    movq $131, %rax  # Load compile-time constant TOKEN_MEMORY_SET_BYTE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1992
.L1991:
.L1992:
    leaq .STR32(%rip), %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2001
    movq $42, %rax  # Load compile-time constant TOKEN_BIT_SHIFT_LEFT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2002
.L2001:
.L2002:
    leaq .STR33(%rip), %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2011
    movq $43, %rax  # Load compile-time constant TOKEN_BIT_SHIFT_RIGHT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2012
.L2011:
.L2012:
    leaq .STR29(%rip), %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2021
    movq $39, %rax  # Load compile-time constant TOKEN_BIT_AND
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2022
.L2021:
.L2022:
    leaq .STR30(%rip), %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2031
    movq $40, %rax  # Load compile-time constant TOKEN_BIT_OR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2032
.L2031:
.L2032:
    leaq .STR31(%rip), %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2041
    movq $41, %rax  # Load compile-time constant TOKEN_BIT_XOR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2042
.L2041:
.L2042:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_single_char_token
check_single_char_token:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq $45, %rax
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2051
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR88(%rip), %rax
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    movq $17, %rax  # Load compile-time constant TOKEN_MINUS
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2052
.L2051:
    movq -16(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR89(%rip), %rax
    movq %rax, -80(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq $9, %rax  # Load compile-time constant TOKEN_COLON
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2062
.L2061:
    movq -16(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2071
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR90(%rip), %rax
    movq %rax, -104(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq $48, %rax  # Load compile-time constant TOKEN_LPAREN
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2072
.L2071:
    movq -16(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2081
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR91(%rip), %rax
    movq %rax, -128(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq $49, %rax  # Load compile-time constant TOKEN_RPAREN
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2082
.L2081:
    movq -16(%rbp), %rax
    pushq %rax
    movq $91, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2091
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR92(%rip), %rax
    movq %rax, -152(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    movq $127, %rax  # Load compile-time constant TOKEN_LBRACKET
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2092
.L2091:
    movq -16(%rbp), %rax
    pushq %rax
    movq $93, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2101
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR93(%rip), %rax
    movq %rax, -176(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    movq $128, %rax  # Load compile-time constant TOKEN_RBRACKET
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2102
.L2101:
    movq -16(%rbp), %rax
    pushq %rax
    movq $46, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2111
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR94(%rip), %rax
    movq %rax, -200(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    movq $51, %rax  # Load compile-time constant TOKEN_DOT
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2112
.L2111:
    movq -16(%rbp), %rax
    pushq %rax
    movq $44, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2121
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR95(%rip), %rax
    movq %rax, -224(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    movq $52, %rax  # Load compile-time constant TOKEN_COMMA
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2122
.L2121:
    movq -16(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2131
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR96(%rip), %rax
    movq %rax, -248(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    movq $111, %rax  # Load compile-time constant TOKEN_PIPE
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2132
.L2131:
    movq -16(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2141
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR97(%rip), %rax
    movq %rax, -272(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    movq $157, %rax  # Load compile-time constant TOKEN_DOLLAR
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2142
.L2141:
    movq -16(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2151
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR98(%rip), %rax
    movq %rax, -296(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    movq $161, %rax  # Load compile-time constant TOKEN_UNDERSCORE
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2152
.L2151:
    movq -16(%rbp), %rax
    pushq %rax
    movq $123, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2161
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR99(%rip), %rax
    movq %rax, -320(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    movq $146, %rax  # Load compile-time constant TOKEN_LBRACE
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2162
.L2161:
    movq -16(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2171
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR100(%rip), %rax
    movq %rax, -344(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    movq $147, %rax  # Load compile-time constant TOKEN_RBRACE
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2172
.L2171:
.L2172:
.L2162:
.L2152:
.L2142:
.L2132:
.L2122:
.L2112:
.L2102:
.L2092:
.L2082:
.L2072:
.L2062:
.L2052:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl token_destroy
token_destroy:
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
    jz .L2181
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
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2191
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2192
.L2191:
.L2192:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2182
.L2181:
.L2182:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_alnum_char
is_alnum_char:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_alpha
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2201
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2202
.L2201:
.L2202:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl print_char
print_char:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl print_newline
print_newline:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $10, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_char
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

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
