.section .rodata
.STR0:    .string "[LEXER ERROR] Unterminated string literal at line "
.STR1:    .string ", column "
.STR2:    .string "Unterminated string"
.STR3:    .string "[LEXER ERROR] Unexpected character '"
.STR4:    .string "' at line "
.STR5:    .string "Unexpected character"
.STR6:    .string "Process"
.STR7:    .string "called"
.STR8:    .string "returns"
.STR9:    .string "Integer"
.STR10:    .string "String"
.STR11:    .string "Character"
.STR12:    .string "Return"
.STR13:    .string "End"
.STR14:    .string "Let"
.STR15:    .string "be"
.STR16:    .string "Set"
.STR17:    .string "to"
.STR18:    .string "plus"
.STR19:    .string "minus"
.STR20:    .string "If"
.STR21:    .string "Otherwise"
.STR22:    .string "While"
.STR23:    .string "is"
.STR24:    .string "equal"
.STR25:    .string "less"
.STR26:    .string "greater"
.STR27:    .string "than"
.STR28:    .string "not"
.STR29:    .string "and"
.STR30:    .string "or"
.STR31:    .string "that"
.STR32:    .string "takes"
.STR33:    .string "as"
.STR34:    .string "multiplied"
.STR35:    .string "divided"
.STR36:    .string "modulo"
.STR37:    .string "by"
.STR38:    .string "Break"
.STR39:    .string "Continue"
.STR40:    .string "Print"
.STR41:    .string "Display"
.STR42:    .string "Type"
.STR43:    .string "Import"
.STR44:    .string "string_length"
.STR45:    .string "read_file"
.STR46:    .string "write_file"
.STR47:    .string "memory_get_byte"
.STR48:    .string "memory_set_byte"
.STR49:    .string "bit_and"
.STR50:    .string "bit_or"
.STR51:    .string "bit_xor"
.STR52:    .string "bit_shift_left"
.STR53:    .string "bit_shift_right"
.STR54:    .string "negative"
.STR55:    .string "true"
.STR56:    .string "false"
.STR57:    .string "gets"
.STR58:    .string "increased"
.STR59:    .string "decreased"
.STR60:    .string "increase"
.STR61:    .string "decrease"
.STR62:    .string "multiply"
.STR63:    .string "divide"
.STR64:    .string "For"
.STR65:    .string "from"
.STR66:    .string "each"
.STR67:    .string "at"
.STR68:    .string "index"
.STR69:    .string "key"
.STR70:    .string "length"
.STR71:    .string "in"
.STR72:    .string "where"
.STR73:    .string "an"
.STR74:    .string "a"
.STR75:    .string "containing"
.STR76:    .string ":"
.STR77:    .string "("
.STR78:    .string ")"
.STR79:    .string "."
.STR80:    .string ","
.STR81:    .string "|"
.STR82:    .string "{"
.STR83:    .string "}"

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
.globl TOKEN_LBRACKET_RESERVED
TOKEN_LBRACKET_RESERVED:    .quad 127
.globl TOKEN_RBRACKET_RESERVED
TOKEN_RBRACKET_RESERVED:    .quad 128
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

.text
print_string:
    pushq %rbp
    movq %rsp, %rbp

    # Calculate string len
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
    movq %rax, %rdx   # count = string len
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

    # Calculate string len
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
    movq %rax, %rdx   # count = string len
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
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
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
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
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
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
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
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
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
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
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
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
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
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_skip_comment
lexer_skip_comment:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
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
    movq %rax, -32(%rbp)
    movq $10, %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L92
.L91:
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L102
.L101:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
.L102:
.L92:
    jmp .L81
.L82:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
    jz .L111
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
    jmp .L112
.L111:
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
.L112:
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
.L121:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L122
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
    jz .L131
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L132
.L131:
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L142
.L141:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
.L142:
.L132:
    jmp .L121
.L122:
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
    jz .L151
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -96(%rbp)
    movq $1, %rax
    movq %rax, -104(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
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
    jmp .L152
.L151:
.L152:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
.L161:    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L162
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
    jz .L171
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L172
.L171:
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
    jz .L181
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
    jmp .L182
.L181:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
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
    movq %rax, -72(%rbp)
    jmp .L192
.L191:
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L192:
.L182:
.L172:
    jmp .L161
.L162:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -88(%rbp)
    movq $1, %rax
    movq %rax, -96(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
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
.L201:    movq -32(%rbp), %rax
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
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
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
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L212
.L211:
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
    jz .L221
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    jmp .L222
.L221:
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L222:
.L212:
    jmp .L201
.L202:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -72(%rbp)
    movq $1, %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
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
    jz .L231
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
    jmp .L232
.L231:
.L232:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
.L241:    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L242
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
    jz .L251
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L252
.L251:
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
    jz .L261
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_whitespace
    movq %rax, -56(%rbp)
    jmp .L262
.L261:
    movq $35, %rax
    movq %rax, -64(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_comment
    movq %rax, -72(%rbp)
    jmp .L272
.L271:
    movq $34, %rax
    movq %rax, -80(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_string_literal
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    movq $10, %rax  # Load compile-time constant TOKEN_STRING_LITERAL
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L292
.L291:
    leaq .STR0(%rip), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    call print_newline
    leaq .STR2(%rip), %rax
    movq %rax, -120(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq $129, %rax  # Load compile-time constant TOKEN_ERROR
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L292:
    jmp .L282
.L281:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_integer
    movq %rax, -144(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    movq $11, %rax  # Load compile-time constant TOKEN_INTEGER
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L302
.L301:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_alpha
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call determine_token_type
    movq %rax, -176(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L312
.L311:
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
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L322
.L321:
    leaq .STR3(%rip), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_char
    leaq .STR4(%rip), %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
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
    movq %rax, -224(%rbp)
    leaq .STR5(%rip), %rax
    movq %rax, -120(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq $129, %rax  # Load compile-time constant TOKEN_ERROR
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L322:
.L312:
.L302:
.L282:
.L272:
.L262:
.L252:
    jmp .L241
.L242:
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
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl determine_token_type
determine_token_type:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR6(%rip), %rax
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
    jz .L331
    movq $1, %rax  # Load compile-time constant TOKEN_PROCESS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L332
.L331:
.L332:
    leaq .STR7(%rip), %rax
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
    jz .L341
    movq $2, %rax  # Load compile-time constant TOKEN_CALLED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L342
.L341:
.L342:
    leaq .STR8(%rip), %rax
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
    jz .L351
    movq $3, %rax  # Load compile-time constant TOKEN_RETURNS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L352
.L351:
.L352:
    leaq .STR9(%rip), %rax
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
    jz .L361
    movq $4, %rax  # Load compile-time constant TOKEN_INTEGER_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L362
.L361:
.L362:
    leaq .STR10(%rip), %rax
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
    jz .L371
    movq $5, %rax  # Load compile-time constant TOKEN_STRING_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L372
.L371:
.L372:
    leaq .STR11(%rip), %rax
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
    jz .L381
    movq $6, %rax  # Load compile-time constant TOKEN_CHARACTER_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L382
.L381:
.L382:
    leaq .STR12(%rip), %rax
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
    jz .L391
    movq $7, %rax  # Load compile-time constant TOKEN_RETURN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L392
.L391:
.L392:
    leaq .STR13(%rip), %rax
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
    jz .L401
    movq $8, %rax  # Load compile-time constant TOKEN_END
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L402
.L401:
.L402:
    leaq .STR14(%rip), %rax
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
    jz .L411
    movq $12, %rax  # Load compile-time constant TOKEN_LET
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L412
.L411:
.L412:
    leaq .STR15(%rip), %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
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
    jz .L421
    movq $13, %rax  # Load compile-time constant TOKEN_BE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L422
.L421:
.L422:
    leaq .STR16(%rip), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
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
    jz .L431
    movq $14, %rax  # Load compile-time constant TOKEN_SET
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L432
.L431:
.L432:
    leaq .STR17(%rip), %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
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
    jz .L441
    movq $15, %rax  # Load compile-time constant TOKEN_TO
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L442
.L441:
.L442:
    leaq .STR18(%rip), %rax
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
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
    jz .L451
    movq $16, %rax  # Load compile-time constant TOKEN_PLUS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L452
.L451:
.L452:
    leaq .STR19(%rip), %rax
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
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
    jz .L461
    movq $17, %rax  # Load compile-time constant TOKEN_MINUS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L462
.L461:
.L462:
    leaq .STR20(%rip), %rax
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
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
    jz .L471
    movq $18, %rax  # Load compile-time constant TOKEN_IF
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L472
.L471:
.L472:
    leaq .STR21(%rip), %rax
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
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
    jz .L481
    movq $19, %rax  # Load compile-time constant TOKEN_OTHERWISE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L482
.L481:
.L482:
    leaq .STR22(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
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
    jz .L491
    movq $20, %rax  # Load compile-time constant TOKEN_WHILE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L492
.L491:
.L492:
    leaq .STR23(%rip), %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
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
    jz .L501
    movq $21, %rax  # Load compile-time constant TOKEN_IS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L502
.L501:
.L502:
    leaq .STR24(%rip), %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
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
    jz .L511
    movq $22, %rax  # Load compile-time constant TOKEN_EQUAL
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L512
.L511:
.L512:
    leaq .STR25(%rip), %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
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
    jz .L521
    movq $24, %rax  # Load compile-time constant TOKEN_LESS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L522
.L521:
.L522:
    leaq .STR26(%rip), %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
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
    jz .L531
    movq $25, %rax  # Load compile-time constant TOKEN_GREATER
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L532
.L531:
.L532:
    leaq .STR27(%rip), %rax
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
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
    jz .L541
    movq $28, %rax  # Load compile-time constant TOKEN_THAN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L542
.L541:
.L542:
    leaq .STR28(%rip), %rax
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
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
    jz .L551
    movq $29, %rax  # Load compile-time constant TOKEN_NOT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L552
.L551:
.L552:
    leaq .STR29(%rip), %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
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
    jz .L561
    movq $30, %rax  # Load compile-time constant TOKEN_AND
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L562
.L561:
.L562:
    leaq .STR30(%rip), %rax
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
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
    jz .L571
    movq $31, %rax  # Load compile-time constant TOKEN_OR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L572
.L571:
.L572:
    leaq .STR31(%rip), %rax
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
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
    jz .L581
    movq $32, %rax  # Load compile-time constant TOKEN_THAT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L582
.L581:
.L582:
    leaq .STR32(%rip), %rax
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
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
    jz .L591
    movq $33, %rax  # Load compile-time constant TOKEN_TAKES
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L592
.L591:
.L592:
    leaq .STR33(%rip), %rax
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
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
    jz .L601
    movq $34, %rax  # Load compile-time constant TOKEN_AS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L602
.L601:
.L602:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_remaining_keywords
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L611
    movq -248(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L612
.L611:
.L612:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_remaining_keywords
check_remaining_keywords:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR34(%rip), %rax
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
    jz .L621
    movq $35, %rax  # Load compile-time constant TOKEN_MULTIPLIED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L622
.L621:
.L622:
    leaq .STR35(%rip), %rax
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
    jz .L631
    movq $36, %rax  # Load compile-time constant TOKEN_DIVIDED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L632
.L631:
.L632:
    leaq .STR36(%rip), %rax
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
    jz .L641
    movq $37, %rax  # Load compile-time constant TOKEN_MODULO
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L642
.L641:
.L642:
    leaq .STR37(%rip), %rax
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
    jz .L651
    movq $38, %rax  # Load compile-time constant TOKEN_BY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L652
.L651:
.L652:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_builtin_functions
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L661
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L662
.L661:
.L662:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_builtin_functions
check_builtin_functions:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR38(%rip), %rax
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
    jz .L671
    movq $44, %rax  # Load compile-time constant TOKEN_BREAK
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L672
.L671:
.L672:
    leaq .STR39(%rip), %rax
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
    jz .L681
    movq $45, %rax  # Load compile-time constant TOKEN_CONTINUE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L682
.L681:
.L682:
    leaq .STR40(%rip), %rax
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
    jz .L691
    movq $47, %rax  # Load compile-time constant TOKEN_PRINT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L692
.L691:
.L692:
    leaq .STR41(%rip), %rax
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
    jz .L701
    movq $47, %rax  # Load compile-time constant TOKEN_PRINT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L702
.L701:
.L702:
    leaq .STR42(%rip), %rax
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
    jz .L711
    movq $50, %rax  # Load compile-time constant TOKEN_TYPE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L712
.L711:
.L712:
    leaq .STR43(%rip), %rax
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
    jz .L721
    movq $56, %rax  # Load compile-time constant TOKEN_IMPORT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L722
.L721:
.L722:
    leaq .STR44(%rip), %rax
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
    jz .L731
    movq $57, %rax  # Load compile-time constant TOKEN_STRING_LENGTH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L732
.L731:
.L732:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_more_builtins
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_more_builtins
check_more_builtins:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    leaq .STR45(%rip), %rax
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
    jz .L741
    movq $54, %rax  # Load compile-time constant TOKEN_READ_FILE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L742
.L741:
.L742:
    leaq .STR46(%rip), %rax
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
    jz .L751
    movq $55, %rax  # Load compile-time constant TOKEN_WRITE_FILE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L752
.L751:
.L752:
    leaq .STR47(%rip), %rax
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
    jz .L761
    movq $130, %rax  # Load compile-time constant TOKEN_MEMORY_GET_BYTE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L762
.L761:
.L762:
    leaq .STR48(%rip), %rax
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
    jz .L771
    movq $131, %rax  # Load compile-time constant TOKEN_MEMORY_SET_BYTE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L772
.L771:
.L772:
    leaq .STR49(%rip), %rax
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
    jz .L781
    movq $39, %rax  # Load compile-time constant TOKEN_BIT_AND
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L782
.L781:
.L782:
    leaq .STR50(%rip), %rax
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
    jz .L791
    movq $40, %rax  # Load compile-time constant TOKEN_BIT_OR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L792
.L791:
.L792:
    leaq .STR51(%rip), %rax
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
    jz .L801
    movq $41, %rax  # Load compile-time constant TOKEN_BIT_XOR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L802
.L801:
.L802:
    leaq .STR52(%rip), %rax
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
    jz .L811
    movq $42, %rax  # Load compile-time constant TOKEN_BIT_SHIFT_LEFT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L812
.L811:
.L812:
    leaq .STR53(%rip), %rax
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
    jz .L821
    movq $43, %rax  # Load compile-time constant TOKEN_BIT_SHIFT_RIGHT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L822
.L821:
.L822:
    leaq .STR54(%rip), %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
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
    jz .L831
    movq $133, %rax  # Load compile-time constant TOKEN_NEGATIVE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L832
.L831:
.L832:
    leaq .STR55(%rip), %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
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
    jz .L841
    movq $134, %rax  # Load compile-time constant TOKEN_TRUE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L842
.L841:
.L842:
    leaq .STR56(%rip), %rax
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
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
    jz .L851
    movq $135, %rax  # Load compile-time constant TOKEN_FALSE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L852
.L851:
.L852:
    leaq .STR57(%rip), %rax
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
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
    jz .L861
    movq $136, %rax  # Load compile-time constant TOKEN_GETS
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L862
.L861:
.L862:
    leaq .STR58(%rip), %rax
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
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
    jz .L871
    movq $137, %rax  # Load compile-time constant TOKEN_INCREASED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L872
.L871:
.L872:
    leaq .STR59(%rip), %rax
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
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
    jz .L881
    movq $138, %rax  # Load compile-time constant TOKEN_DECREASED
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L882
.L881:
.L882:
    leaq .STR60(%rip), %rax
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
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
    jz .L891
    movq $139, %rax  # Load compile-time constant TOKEN_INCREASE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L892
.L891:
.L892:
    leaq .STR61(%rip), %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
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
    jz .L901
    movq $140, %rax  # Load compile-time constant TOKEN_DECREASE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L902
.L901:
.L902:
    leaq .STR62(%rip), %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
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
    jz .L911
    movq $141, %rax  # Load compile-time constant TOKEN_MULTIPLY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L912
.L911:
.L912:
    leaq .STR63(%rip), %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
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
    jz .L921
    movq $142, %rax  # Load compile-time constant TOKEN_DIVIDE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L922
.L921:
.L922:
    leaq .STR64(%rip), %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
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
    jz .L931
    movq $143, %rax  # Load compile-time constant TOKEN_FOR
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L932
.L931:
.L932:
    leaq .STR65(%rip), %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
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
    jz .L941
    movq $144, %rax  # Load compile-time constant TOKEN_FROM
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L942
.L941:
.L942:
    leaq .STR66(%rip), %rax
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
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
    jz .L951
    movq $145, %rax  # Load compile-time constant TOKEN_EACH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L952
.L951:
.L952:
    leaq .STR67(%rip), %rax
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
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
    jz .L961
    movq $148, %rax  # Load compile-time constant TOKEN_AT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L962
.L961:
.L962:
    leaq .STR68(%rip), %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
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
    jz .L971
    movq $149, %rax  # Load compile-time constant TOKEN_INDEX
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L972
.L971:
.L972:
    leaq .STR69(%rip), %rax
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
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
    jz .L981
    movq $150, %rax  # Load compile-time constant TOKEN_KEY
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L982
.L981:
.L982:
    leaq .STR70(%rip), %rax
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
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
    jz .L991
    movq $151, %rax  # Load compile-time constant TOKEN_LENGTH
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L992
.L991:
.L992:
    leaq .STR71(%rip), %rax
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
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
    jz .L1001
    movq $152, %rax  # Load compile-time constant TOKEN_IN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1002
.L1001:
.L1002:
    leaq .STR72(%rip), %rax
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
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
    jz .L1011
    movq $153, %rax  # Load compile-time constant TOKEN_WHERE
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1012
.L1011:
.L1012:
    leaq .STR73(%rip), %rax
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
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
    jz .L1021
    movq $154, %rax  # Load compile-time constant TOKEN_AN
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1022
.L1021:
.L1022:
    leaq .STR74(%rip), %rax
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
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
    jz .L1031
    movq $155, %rax  # Load compile-time constant TOKEN_A
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1032
.L1031:
.L1032:
    leaq .STR75(%rip), %rax
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
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
    jz .L1041
    movq $156, %rax  # Load compile-time constant TOKEN_CONTAINING
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1042
.L1041:
.L1042:
    movq $53, %rax  # Load compile-time constant TOKEN_IDENTIFIER
    movq %rbp, %rsp
    popq %rbp
    ret
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
    movq $58, %rax
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR76(%rip), %rax
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
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
    jmp .L1052
.L1051:
.L1052:
    movq $40, %rax
    movq %rax, -72(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR77(%rip), %rax
    movq %rax, -88(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
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
    jmp .L1062
.L1061:
.L1062:
    movq $41, %rax
    movq %rax, -104(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR78(%rip), %rax
    movq %rax, -120(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
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
    jmp .L1072
.L1071:
.L1072:
    movq $46, %rax
    movq %rax, -136(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1081
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR79(%rip), %rax
    movq %rax, -152(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
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
    jmp .L1082
.L1081:
.L1082:
    movq $44, %rax
    movq %rax, -168(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR80(%rip), %rax
    movq %rax, -184(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -184(%rbp), %rax
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
    jmp .L1092
.L1091:
.L1092:
    movq $124, %rax
    movq %rax, -200(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR81(%rip), %rax
    movq %rax, -216(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -216(%rbp), %rax
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
    jmp .L1102
.L1101:
.L1102:
    movq $123, %rax
    movq %rax, -232(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR82(%rip), %rax
    movq %rax, -248(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -248(%rbp), %rax
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
    jmp .L1112
.L1111:
.L1112:
    movq $125, %rax
    movq %rax, -264(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR83(%rip), %rax
    movq %rax, -280(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
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
    jmp .L1122
.L1121:
.L1122:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
    jz .L1131
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
    jz .L1141
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L1142
.L1141:
.L1142:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L1132
.L1131:
.L1132:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
    popq %rdi
    call is_digit@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
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
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
