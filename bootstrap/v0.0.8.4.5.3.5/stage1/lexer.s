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
.globl TOKEN_EXPORT
TOKEN_EXPORT:    .quad 163
.globl TOKEN_CONSTANT
TOKEN_CONSTANT:    .quad 164
.globl TOKEN_ANNOTATION_START
TOKEN_ANNOTATION_START:    .quad 165
.globl TOKEN_ANNOTATION_END
TOKEN_ANNOTATION_END:    .quad 166
.globl TOKEN_INTRINSIC_STORE
TOKEN_INTRINSIC_STORE:    .quad 167
.globl TOKEN_INTRINSIC_LOAD
TOKEN_INTRINSIC_LOAD:    .quad 168
.globl TOKEN_INTRINSIC_STORE8
TOKEN_INTRINSIC_STORE8:    .quad 169
.globl TOKEN_INTRINSIC_LOAD8
TOKEN_INTRINSIC_LOAD8:    .quad 170
.globl TOKEN_PROC
TOKEN_PROC:    .quad 171
.globl TOKEN_ALERT
TOKEN_ALERT:    .quad 172
.globl TOKEN_PRIVATE
TOKEN_PRIVATE:    .quad 173
.globl TOKEN_NOTHING
TOKEN_NOTHING:    .quad 174
.globl TOKEN_BITWISE
TOKEN_BITWISE:    .quad 175
.globl TOKEN_SHIFTED
TOKEN_SHIFTED:    .quad 176
.globl TOKEN_LEFT
TOKEN_LEFT:    .quad 177
.globl TOKEN_RIGHT
TOKEN_RIGHT:    .quad 178
.globl TOKEN_CONTAINS
TOKEN_CONTAINS:    .quad 179
.globl TOKEN_LOOP
TOKEN_LOOP:    .quad 180
.globl TOKEN_FOREVER
TOKEN_FOREVER:    .quad 181
.globl TOKEN_JOINED
TOKEN_JOINED:    .quad 182
.globl TOKEN_CALL
TOKEN_CALL:    .quad 183

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
.STR5:    .string "[LEXER ERROR] Unexpected character '"
.STR6:    .string "' at line "
.STR7:    .string "Unexpected character"
.STR8:    .string "joined"
.STR9:    .string "Process"
.STR10:    .string "Print"
.STR11:    .string "Private"
.STR12:    .string "called"
.STR13:    .string "containing"
.STR14:    .string "contains"
.STR15:    .string "returns"
.STR16:    .string "right"
.STR17:    .string "Integer"
.STR18:    .string "If"
.STR19:    .string "Increase"
.STR20:    .string "Inline"
.STR21:    .string "Import"
.STR22:    .string "Assembly"
.STR23:    .string "Alert"
.STR24:    .string "String"
.STR25:    .string "Set"
.STR26:    .string "Character"
.STR27:    .string "Continue"
.STR28:    .string "Constant"
.STR29:    .string "Call"
.STR30:    .string "Return"
.STR31:    .string "Export"
.STR32:    .string "Each"
.STR33:    .string "Let"
.STR34:    .string "Loop"
.STR35:    .string "be"
.STR36:    .string "by"
.STR37:    .string "bit_and"
.STR38:    .string "bit_or"
.STR39:    .string "bit_xor"
.STR40:    .string "bit_shift_left"
.STR41:    .string "bit_shift_right"
.STR42:    .string "bitwise"
.STR43:    .string "bitwise_and"
.STR44:    .string "bitwise_or"
.STR45:    .string "bitwise_xor"
.STR46:    .string "shifted"
.STR47:    .string "to"
.STR48:    .string "takes"
.STR49:    .string "than"
.STR50:    .string "that"
.STR51:    .string "true"
.STR52:    .string "the"
.STR53:    .string "plus"
.STR54:    .string "proc"
.STR55:    .string "minus"
.STR56:    .string "multiplied"
.STR57:    .string "modulo"
.STR58:    .string "is"
.STR59:    .string "in"
.STR60:    .string "index"
.STR61:    .string "increased"
.STR62:    .string "equal"
.STR63:    .string "each"
.STR64:    .string "less"
.STR65:    .string "length"
.STR66:    .string "lambda"
.STR67:    .string "left"
.STR68:    .string "list"
.STR69:    .string "greater"
.STR70:    .string "gets"
.STR71:    .string "not"
.STR72:    .string "negative"
.STR73:    .string "and"
.STR74:    .string "as"
.STR75:    .string "at"
.STR76:    .string "an"
.STR77:    .string "array"
.STR78:    .string "a"
.STR79:    .string "or"
.STR80:    .string "of"
.STR81:    .string "Otherwise"
.STR82:    .string "While"
.STR83:    .string "When"
.STR84:    .string "Type"
.STR85:    .string "Break"
.STR86:    .string "false"
.STR87:    .string "from"
.STR88:    .string "forever"
.STR89:    .string "divided"
.STR90:    .string "decreased"
.STR91:    .string "Display"
.STR92:    .string "Decrease"
.STR93:    .string "Divide"
.STR94:    .string "Multiply"
.STR95:    .string "Match"
.STR96:    .string "For"
.STR97:    .string "where"
.STR98:    .string "with"
.STR99:    .string "key"
.STR100:    .string "string_length"
.STR101:    .string "read_file"
.STR102:    .string "write_file"
.STR103:    .string "memory_get_byte"
.STR104:    .string "memory_set_byte"
.STR105:    .string "-"
.STR106:    .string ":"
.STR107:    .string "("
.STR108:    .string ")"
.STR109:    .string "["
.STR110:    .string "]"
.STR111:    .string "."
.STR112:    .string ","
.STR113:    .string "|"
.STR114:    .string "$"
.STR115:    .string "+"
.STR116:    .string "store8"
.STR117:    .string "__store8"
.STR118:    .string "store"
.STR119:    .string "__store"
.STR120:    .string "load8"
.STR121:    .string "__load8"
.STR122:    .string "load"
.STR123:    .string "__load"
.STR124:    .string "__"
.STR125:    .string "_"
.STR126:    .string "{"
.STR127:    .string "}"
.text


.globl string_copy
string_copy:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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


.globl lexer_skip_to_eol
lexer_skip_to_eol:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $1, %rax
    movq %rax, -16(%rbp)
.L81:    movq -16(%rbp), %rax
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
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
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
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L92
.L91:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
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
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L102
.L101:
    movq -24(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
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
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    jmp .L122
.L121:
.L122:
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L112
.L111:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
.L112:
.L102:
.L92:
    jmp .L81
.L82:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_skip_note_comment
lexer_skip_note_comment:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
.L131:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L132
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
    jz .L141
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    jmp .L142
.L141:
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -56(%rbp)
    jmp .L152
.L151:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L152:
.L142:
    jmp .L131
.L132:
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
    jz .L161
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L162
.L161:
.L162:
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
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $9, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -96(%rbp)
    movq $1, %rax
    movq %rax, -104(%rbp)
.L171:    movq -104(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L172
    movq -16(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
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
    movq %rax, -112(%rbp)
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
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    movq %rax, -120(%rbp)
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
    jmp .L192
.L191:
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq $0, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L202
.L201:
    movq -16(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $0, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L212
.L211:
    movq $1, %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L212:
.L202:
    movq $0, %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L192:
.L182:
    jmp .L171
.L172:
    movq -96(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
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
    jz .L231
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
    jmp .L232
.L231:
.L232:
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
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
    movq %rax, -136(%rbp)
    jmp .L242
.L241:
.L242:
    movq $1, %rax
    movq %rax, -144(%rbp)
    movq $1, %rax
    movq %rax, -152(%rbp)
.L251:    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L252
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
    jz .L261
    movq $0, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L262
.L261:
    movq $58, %rax
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -160(%rbp)
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -176(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -184(%rbp)
    movq $1, %rax
    movq %rax, -192(%rbp)
.L281:    movq -192(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L282
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
    jz .L291
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -200(%rbp)
    jmp .L292
.L291:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax
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
    movq %rax, -208(%rbp)
    jmp .L302
.L301:
    movq -16(%rbp), %rax
    pushq %rax
    movq $13, %rax
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
    movq %rax, -216(%rbp)
    jmp .L312
.L311:
    movq $0, %rax
    pushq %rax
    leaq -192(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L312:
.L302:
.L292:
    jmp .L281
.L282:
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
    jz .L321
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -224(%rbp)
    leaq .STR0(%rip), %rax
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
    jz .L331
    movq $1, %rax
    movq %rax, -232(%rbp)
.L341:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L342
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
    jz .L351
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -240(%rbp)
    jmp .L352
.L351:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -248(%rbp)
    jmp .L362
.L361:
    movq -16(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -256(%rbp)
    jmp .L372
.L371:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L372:
.L362:
.L352:
    jmp .L341
.L342:
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
    jz .L381
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -264(%rbp)
    leaq .STR1(%rip), %rax
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
    jz .L391
    movq -152(%rbp), %rax
    subq $1, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L402
.L401:
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L402:
    jmp .L392
.L391:
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L392:
    jmp .L382
.L381:
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L382:
    jmp .L332
.L331:
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
.L332:
    jmp .L322
.L321:
.L322:
    jmp .L272
.L271:
    movq -16(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -272(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -280(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -280(%rbp), %rax
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
    jz .L421
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
    jz .L431
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -288(%rbp)
    movq $1, %rax
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -304(%rbp)
.L441:    movq -296(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L442
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
    jz .L451
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -312(%rbp)
    jmp .L452
.L451:
    movq -16(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -320(%rbp)
    jmp .L462
.L461:
    movq -16(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L471
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -328(%rbp)
    jmp .L472
.L471:
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    movq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L482
.L481:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L491
    movq $1, %rax
    pushq %rax
    leaq -304(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L492
.L491:
    movq $0, %rax
    pushq %rax
    leaq -296(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L492:
.L482:
.L472:
.L462:
.L452:
    jmp .L441
.L442:
    movq -304(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L501
    movq -152(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -152(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L502
.L501:
.L502:
    jmp .L432
.L431:
.L432:
    jmp .L422
.L421:
.L422:
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L412
.L411:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -336(%rbp)
.L412:
.L272:
.L262:
    jmp .L251
.L252:
    jmp .L222
.L221:
    movq $1, %rax
    movq %rax, -344(%rbp)
.L511:    movq -344(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L512
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
    jz .L521
    movq $0, %rax
    pushq %rax
    leaq -344(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L522
.L521:
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq $0, %rax
    pushq %rax
    leaq -344(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L532
.L531:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -352(%rbp)
.L532:
.L522:
    jmp .L511
.L512:
.L222:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl token_create_owned
token_create_owned:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L541
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
    jmp .L542
.L541:
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
.L542:
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
.L551:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L552
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
    jz .L561
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L562
.L561:
    movq -48(%rbp), %rax
    pushq %rax
    movq $92, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -72(%rbp)
    jmp .L572
.L571:
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L581
    movq $0, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L582
.L581:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -80(%rbp)
.L582:
.L572:
.L562:
    jmp .L551
.L552:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $34, %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -48(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    subq -32(%rbp), %rax
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
    movq -32(%rbp), %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -128(%rbp)
    movq -112(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L592
.L591:
.L592:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_read_word
lexer_read_word:
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
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, -24(%rbp)
    movq $1, %rax
    movq %rax, -32(%rbp)
.L601:    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L602
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
    jz .L611
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L612
.L611:
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
    jz .L621
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -64(%rbp)
    jmp .L622
.L621:
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
    movq %rax, -72(%rbp)
    jmp .L632
.L631:
    movq $0, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L632:
.L622:
.L612:
    jmp .L601
.L602:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    subq -24(%rbp), %rax
    movq %rax, -80(%rbp)
    movq $1, %rax
    movq %rax, -88(%rbp)
    movq -80(%rbp), %rax
    addq -88(%rbp), %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call string_copy_n
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq -104(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_read_integer
lexer_read_integer:
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
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, -24(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L641
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    addq -56(%rbp), %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L651
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -80(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -88(%rbp)
    jmp .L652
.L651:
.L652:
    movq -72(%rbp), %rax
    pushq %rax
    movq $88, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L661
    movq $1, %rax
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -96(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -104(%rbp)
    jmp .L662
.L661:
.L662:
    jmp .L642
.L641:
.L642:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L671
    movq $0, %rax
    movq %rax, -112(%rbp)
    movq $1, %rax
    movq %rax, -120(%rbp)
.L681:    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L682
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -128(%rbp)
    movq $0, %rax
    subq $1, %rax
    movq %rax, -136(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L691
    movq -128(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L701
    movq -128(%rbp), %rax
    subq $48, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L702
.L701:
.L702:
    jmp .L692
.L691:
.L692:
    movq -128(%rbp), %rax
    pushq %rax
    movq $96, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq -128(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
    movq -128(%rbp), %rax
    subq $87, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L722
.L721:
.L722:
    jmp .L712
.L711:
.L712:
    movq -128(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L731
    movq -128(%rbp), %rax
    pushq %rax
    movq $71, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L741
    movq -128(%rbp), %rax
    subq $55, %rax
    pushq %rax
    leaq -136(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L742
.L741:
.L742:
    jmp .L732
.L731:
.L732:
    movq -136(%rbp), %rax
    pushq %rax
    movq $0, %rax
    subq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    movq -112(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    addq -136(%rbp), %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -144(%rbp)
    jmp .L752
.L751:
    movq $0, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L752:
    jmp .L681
.L682:
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L672
.L671:
.L672:
    movq $1, %rax
    movq %rax, -160(%rbp)
.L761:    movq -160(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L762
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L771
    movq $0, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L772
.L771:
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L781
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -184(%rbp)
    jmp .L782
.L781:
    movq $0, %rax
    pushq %rax
    leaq -160(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L782:
.L772:
    jmp .L761
.L762:
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $46, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L791
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    addq -16(%rbp), %rax
    addq $1, %rax
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L801
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -224(%rbp)
    movq $1, %rax
    movq %rax, -232(%rbp)
.L811:    movq -232(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L812
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L821
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L822
.L821:
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
    jz .L831
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -256(%rbp)
    jmp .L832
.L831:
    movq $0, %rax
    pushq %rax
    leaq -232(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L832:
.L822:
    jmp .L811
.L812:
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
    call memory_get_int32@PLT
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    movq %rax, -264(%rbp)
    movq -24(%rbp), %rax
    movq %rax, -272(%rbp)
.L841:    movq -272(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L842
    movq -40(%rbp), %rax
    addq -272(%rbp), %rax
    movq %rax, -280(%rbp)
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $46, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L851
    movq -272(%rbp), %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L852
.L851:
    movq -272(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -272(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L852:
    jmp .L841
.L842:
    movq -264(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L861
    movq -16(%rbp), %rax
    pushq %rax
    leaq -264(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L862
.L861:
.L862:
    movq -264(%rbp), %rax
    subq -24(%rbp), %rax
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    addq $1, %rax
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -312(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call string_copy_n
    movq $0, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_set_char
    movq -312(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_create
lexer_create:
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
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
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    leaq LEXER_POSITION(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $1, %rax
    pushq %rax
    movq $16, %rax
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
    call string_length@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -56(%rbp), %rax
    pushq %rax
    leaq LEXER_CURRENT_CHAR(%rip), %rbx  # Address of global variable    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
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


.globl lexer_destroy
lexer_destroy:
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
    jz .L871
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
    jmp .L872
.L871:
.L872:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl lexer_next_token
lexer_next_token:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    movq $1, %rax
    movq %rax, -16(%rbp)
.L881:    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L882
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
    jz .L891
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L892
.L891:
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
    jz .L901
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_whitespace
    movq %rax, -56(%rbp)
    jmp .L902
.L901:
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
    jz .L911
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
    jz .L921
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    movq TOKEN_STRING_LITERAL(%rip), %rax  # Load global variable
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
    jmp .L922
.L921:
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
    movq TOKEN_ERROR(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L922:
    jmp .L912
.L911:
    movq $45, %rax
    movq %rax, -112(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -120(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
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
    call string_length@PLT
    movq %rax, -136(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    movq -120(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L951
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -160(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_integer
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    addq $2, %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -192(%rbp)
    movq $45, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    movq %rax, -200(%rbp)
.L961:    movq -200(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L962
    movq -200(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -200(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -200(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L961
.L962:
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    movq TOKEN_INTEGER(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L952
.L951:
.L952:
    jmp .L942
.L941:
.L942:
    jmp .L932
.L931:
.L932:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L971
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_integer
    pushq %rax
    leaq -168(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    movq TOKEN_INTEGER(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L972
.L971:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_alpha
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L981
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -232(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    movq %rax, -240(%rbp)
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
    call determine_token_type
    movq %rax, -248(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create_owned
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L992
.L991:
.L992:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_note_comment
    movq %rax, -256(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L982
.L981:
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
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1002
.L1001:
    leaq .STR5(%rip), %rax
    pushq %rax
    leaq -88(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_char
    leaq .STR6(%rip), %rax
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR3(%rip), %rax
    pushq %rax
    leaq -96(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
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
    movq %rax, -272(%rbp)
    leaq .STR7(%rip), %rax
    pushq %rax
    leaq -104(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq TOKEN_ERROR(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L1002:
.L982:
.L972:
.L912:
.L902:
.L892:
    jmp .L881
.L882:
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
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
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq TOKEN_EOF(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl determine_token_type
determine_token_type:
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
    jz .L1011
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_P
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1012
.L1011:
    movq -16(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1021
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_c
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1022
.L1021:
    movq -16(%rbp), %rax
    pushq %rax
    movq $114, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_r
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1032
.L1031:
    movq -16(%rbp), %rax
    pushq %rax
    movq $73, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1041
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_I
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1042
.L1041:
    movq -16(%rbp), %rax
    pushq %rax
    movq $65, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_A
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1052
.L1051:
    movq -16(%rbp), %rax
    pushq %rax
    movq $83, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_S
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1062
.L1061:
    movq -16(%rbp), %rax
    pushq %rax
    movq $67, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_C
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1072
.L1071:
    movq -16(%rbp), %rax
    pushq %rax
    movq $82, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1081
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_R
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1082
.L1081:
    movq -16(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_E
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1092
.L1091:
    movq -16(%rbp), %rax
    pushq %rax
    movq $76, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_L
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1102
.L1101:
    movq -16(%rbp), %rax
    pushq %rax
    movq $98, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_b
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1112
.L1111:
    movq -16(%rbp), %rax
    pushq %rax
    movq $115, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_s
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1122
.L1121:
    movq -16(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_t
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1132
.L1131:
    movq -16(%rbp), %rax
    pushq %rax
    movq $112, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1141
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_p
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1142
.L1141:
    movq -16(%rbp), %rax
    pushq %rax
    movq $109, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1151
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_m
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1152
.L1151:
    movq -16(%rbp), %rax
    pushq %rax
    movq $105, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1161
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_i
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1162
.L1161:
    movq -16(%rbp), %rax
    pushq %rax
    movq $106, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1171
    leaq .STR8(%rip), %rax
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
    movq TOKEN_JOINED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1182
.L1181:
.L1182:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1172
.L1171:
    movq -16(%rbp), %rax
    pushq %rax
    movq $101, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1191
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_e
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1192
.L1191:
    movq -16(%rbp), %rax
    pushq %rax
    movq $108, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_l
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1202
.L1201:
    movq -16(%rbp), %rax
    pushq %rax
    movq $103, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1211
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_g
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1212
.L1211:
    movq -16(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_n
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1222
.L1221:
    movq -16(%rbp), %rax
    pushq %rax
    movq $78, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1231
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_N
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1232
.L1231:
    movq -16(%rbp), %rax
    pushq %rax
    movq $97, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_a
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1242
.L1241:
    movq -16(%rbp), %rax
    pushq %rax
    movq $111, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1251
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_o
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1252
.L1251:
    movq -16(%rbp), %rax
    pushq %rax
    movq $79, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1261
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_O
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1262
.L1261:
    movq -16(%rbp), %rax
    pushq %rax
    movq $87, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_W
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1272
.L1271:
    movq -16(%rbp), %rax
    pushq %rax
    movq $84, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1281
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_T
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1282
.L1281:
    movq -16(%rbp), %rax
    pushq %rax
    movq $66, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1291
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_B
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1292
.L1291:
    movq -16(%rbp), %rax
    pushq %rax
    movq $102, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_f
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1302
.L1301:
    movq -16(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_d
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1312
.L1311:
    movq -16(%rbp), %rax
    pushq %rax
    movq $68, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_D
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1322
.L1321:
    movq -16(%rbp), %rax
    pushq %rax
    movq $77, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_M
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1332
.L1331:
    movq -16(%rbp), %rax
    pushq %rax
    movq $70, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_F
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1342
.L1341:
    movq -16(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1351
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_w
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1352
.L1351:
    movq -16(%rbp), %rax
    pushq %rax
    movq $107, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1361
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call check_keywords_k
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1362
.L1361:
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR9(%rip), %rax
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
    movq TOKEN_PROCESS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1372
.L1371:
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
    jz .L1381
    movq TOKEN_PRINT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1382
.L1381:
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
    jz .L1391
    movq TOKEN_PRIVATE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1392
.L1391:
.L1392:
.L1382:
.L1372:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_c
check_keywords_c:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L1401
    movq TOKEN_CALLED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1402
.L1401:
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
    jz .L1411
    movq TOKEN_CONTAINING(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1412
.L1411:
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
    jz .L1421
    movq TOKEN_CONTAINS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1422
.L1421:
.L1422:
.L1412:
.L1402:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_r
check_keywords_r:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L1431
    movq TOKEN_RETURNS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1432
.L1431:
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
    jz .L1441
    movq TOKEN_RIGHT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1442
.L1441:
.L1442:
.L1432:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_I
check_keywords_I:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1451
    movq TOKEN_INTEGER_TYPE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1452
.L1451:
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
    jz .L1461
    movq TOKEN_IF(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1462
.L1461:
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
    jz .L1471
    movq TOKEN_INCREASE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1472
.L1471:
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
    jz .L1481
    movq TOKEN_INLINE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1482
.L1481:
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
    jz .L1491
    movq TOKEN_IMPORT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1492
.L1491:
.L1492:
.L1482:
.L1472:
.L1462:
.L1452:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_A
check_keywords_A:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1501
    movq TOKEN_ASSEMBLY(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1502
.L1501:
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
    jz .L1511
    movq TOKEN_ALERT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1512
.L1511:
.L1512:
.L1502:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_S
check_keywords_S:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1521
    movq TOKEN_STRING_TYPE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1522
.L1521:
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
    jz .L1531
    movq TOKEN_SET(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1532
.L1531:
.L1532:
.L1522:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_C
check_keywords_C:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L1541
    movq TOKEN_CHARACTER_TYPE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1542
.L1541:
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
    jz .L1551
    movq TOKEN_CONTINUE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1552
.L1551:
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
    jz .L1561
    movq TOKEN_CONSTANT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1562
.L1561:
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
    jz .L1571
    movq TOKEN_CALL(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1572
.L1571:
.L1572:
.L1562:
.L1552:
.L1542:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_R
check_keywords_R:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1581
    movq TOKEN_RETURN(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1582
.L1581:
.L1582:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_E
check_keywords_E:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L1591
    movq TOKEN_END(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1592
.L1591:
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
    jz .L1601
    movq TOKEN_EXPORT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1602
.L1601:
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
    jz .L1611
    movq TOKEN_EACH(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1612
.L1611:
.L1612:
.L1602:
.L1592:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_L
check_keywords_L:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1621
    movq TOKEN_LET(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1622
.L1621:
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
    jz .L1631
    movq TOKEN_LOOP(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1632
.L1631:
.L1632:
.L1622:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_b
check_keywords_b:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1641
    movq TOKEN_BE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1642
.L1641:
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
    jz .L1651
    movq TOKEN_BY(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1652
.L1651:
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
    jz .L1661
    movq TOKEN_BIT_AND(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1662
.L1661:
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
    jz .L1671
    movq TOKEN_BIT_OR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1672
.L1671:
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
    jz .L1681
    movq TOKEN_BIT_XOR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1682
.L1681:
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
    jz .L1691
    movq TOKEN_BIT_SHIFT_LEFT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1692
.L1691:
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
    jz .L1701
    movq TOKEN_BIT_SHIFT_RIGHT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1702
.L1701:
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
    jz .L1711
    movq TOKEN_BITWISE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1712
.L1711:
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
    jz .L1721
    movq TOKEN_BIT_AND(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1722
.L1721:
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
    jz .L1731
    movq TOKEN_BIT_OR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1732
.L1731:
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
    jz .L1741
    movq TOKEN_BIT_XOR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1742
.L1741:
.L1742:
.L1732:
.L1722:
.L1712:
.L1702:
.L1692:
.L1682:
.L1672:
.L1662:
.L1652:
.L1642:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_s
check_keywords_s:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1751
    movq TOKEN_SHIFTED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1752
.L1751:
.L1752:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_t
check_keywords_t:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1761
    movq TOKEN_TO(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1762
.L1761:
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
    jz .L1771
    movq TOKEN_TAKES(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1772
.L1771:
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
    jz .L1781
    movq TOKEN_THAN(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1782
.L1781:
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
    jz .L1791
    movq TOKEN_THAT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1792
.L1791:
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
    jz .L1801
    movq TOKEN_TRUE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1802
.L1801:
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
    jz .L1811
    movq TOKEN_THE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1812
.L1811:
.L1812:
.L1802:
.L1792:
.L1782:
.L1772:
.L1762:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_p
check_keywords_p:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1821
    movq TOKEN_PLUS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1822
.L1821:
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
    jz .L1831
    movq TOKEN_PROC(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1832
.L1831:
.L1832:
.L1822:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_m
check_keywords_m:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1841
    movq TOKEN_MINUS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1842
.L1841:
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
    jz .L1851
    movq TOKEN_MULTIPLIED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1852
.L1851:
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
    jz .L1861
    movq TOKEN_MODULO(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1862
.L1861:
.L1862:
.L1852:
.L1842:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_i
check_keywords_i:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L1871
    movq TOKEN_IS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1872
.L1871:
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
    jz .L1881
    movq TOKEN_IN(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1882
.L1881:
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
    jz .L1891
    movq TOKEN_INDEX(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1892
.L1891:
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
    jz .L1901
    movq TOKEN_INCREASED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1902
.L1901:
.L1902:
.L1892:
.L1882:
.L1872:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_e
check_keywords_e:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1911
    movq TOKEN_EQUAL(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1912
.L1911:
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
    jz .L1921
    movq TOKEN_EACH(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1922
.L1921:
.L1922:
.L1912:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_l
check_keywords_l:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L1931
    movq TOKEN_LESS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1932
.L1931:
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
    jz .L1941
    movq TOKEN_LENGTH(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1942
.L1941:
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
    jz .L1951
    movq TOKEN_LAMBDA(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1952
.L1951:
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
    jz .L1961
    movq TOKEN_LEFT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1962
.L1961:
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
    jz .L1971
    movq TOKEN_LIST(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1972
.L1971:
.L1972:
.L1962:
.L1952:
.L1942:
.L1932:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_g
check_keywords_g:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L1981
    movq TOKEN_GREATER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1982
.L1981:
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
    jz .L1991
    movq TOKEN_GETS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1992
.L1991:
.L1992:
.L1982:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_n
check_keywords_n:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L2001
    movq TOKEN_NOT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2002
.L2001:
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
    jz .L2011
    movq TOKEN_NEGATIVE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2012
.L2011:
.L2012:
.L2002:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_N
check_keywords_N:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L2021
    movq TOKEN_NOTE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2022
.L2021:
.L2022:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_a
check_keywords_a:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L2031
    movq TOKEN_AND(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2032
.L2031:
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
    jz .L2041
    movq TOKEN_AS(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2042
.L2041:
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
    jz .L2051
    movq TOKEN_AT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2052
.L2051:
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
    jz .L2061
    movq TOKEN_AN(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2062
.L2061:
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
    jz .L2071
    movq TOKEN_ARRAY(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2072
.L2071:
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
    jz .L2081
    movq TOKEN_A(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2082
.L2081:
.L2082:
.L2072:
.L2062:
.L2052:
.L2042:
.L2032:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_o
check_keywords_o:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L2091
    movq TOKEN_OR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2092
.L2091:
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
    jz .L2101
    movq TOKEN_OF(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2102
.L2101:
.L2102:
.L2092:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_O
check_keywords_O:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
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
    jz .L2111
    movq TOKEN_OTHERWISE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2112
.L2111:
.L2112:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_W
check_keywords_W:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L2121
    movq TOKEN_WHILE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2122
.L2121:
    leaq .STR83(%rip), %rax
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
    jz .L2131
    movq TOKEN_WHEN(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2132
.L2131:
.L2132:
.L2122:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_T
check_keywords_T:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR84(%rip), %rax
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
    jz .L2141
    movq TOKEN_TYPE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2142
.L2141:
.L2142:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_B
check_keywords_B:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR85(%rip), %rax
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
    jz .L2151
    movq TOKEN_BREAK(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2152
.L2151:
.L2152:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_f
check_keywords_f:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR86(%rip), %rax
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
    jz .L2161
    movq TOKEN_FALSE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2162
.L2161:
    leaq .STR87(%rip), %rax
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
    jz .L2171
    movq TOKEN_FROM(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2172
.L2171:
    leaq .STR88(%rip), %rax
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
    jz .L2181
    movq TOKEN_FOREVER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2182
.L2181:
.L2182:
.L2172:
.L2162:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_d
check_keywords_d:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR89(%rip), %rax
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
    jz .L2191
    movq TOKEN_DIVIDED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2192
.L2191:
    leaq .STR90(%rip), %rax
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
    jz .L2201
    movq TOKEN_DECREASED(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2202
.L2201:
.L2202:
.L2192:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_D
check_keywords_D:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR91(%rip), %rax
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
    jz .L2211
    movq TOKEN_PRINT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2212
.L2211:
    leaq .STR92(%rip), %rax
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
    jz .L2221
    movq TOKEN_DECREASE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2222
.L2221:
    leaq .STR93(%rip), %rax
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
    jz .L2231
    movq TOKEN_DIVIDE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2232
.L2231:
.L2232:
.L2222:
.L2212:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_M
check_keywords_M:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR94(%rip), %rax
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
    jz .L2241
    movq TOKEN_MULTIPLY(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2242
.L2241:
    leaq .STR95(%rip), %rax
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
    jz .L2251
    movq TOKEN_MATCH(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2252
.L2251:
.L2252:
.L2242:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_F
check_keywords_F:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR96(%rip), %rax
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
    movq TOKEN_FOR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2262
.L2261:
.L2262:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_w
check_keywords_w:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR97(%rip), %rax
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
    movq TOKEN_WHERE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2272
.L2271:
    leaq .STR98(%rip), %rax
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
    movq TOKEN_WITH(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2282
.L2281:
.L2282:
.L2272:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_keywords_k
check_keywords_k:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR99(%rip), %rax
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
    movq TOKEN_KEY(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2292
.L2291:
.L2292:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_builtin_functions
check_builtin_functions:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR85(%rip), %rax
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
    jz .L2301
    movq TOKEN_BREAK(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2302
.L2301:
.L2302:
    leaq .STR27(%rip), %rax
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
    jz .L2311
    movq TOKEN_CONTINUE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2312
.L2311:
.L2312:
    leaq .STR10(%rip), %rax
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
    jz .L2321
    movq TOKEN_PRINT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2322
.L2321:
.L2322:
    leaq .STR91(%rip), %rax
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
    jz .L2331
    movq TOKEN_PRINT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2332
.L2331:
.L2332:
    leaq .STR84(%rip), %rax
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
    jz .L2341
    movq TOKEN_TYPE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2342
.L2341:
.L2342:
    leaq .STR21(%rip), %rax
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
    jz .L2351
    movq TOKEN_IMPORT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2352
.L2351:
.L2352:
    leaq .STR100(%rip), %rax
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
    jz .L2361
    movq TOKEN_STRING_LENGTH(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2362
.L2361:
.L2362:
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
    movq %rdi, -8(%rbp)
    leaq .STR101(%rip), %rax
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
    jz .L2371
    movq TOKEN_READ_FILE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2372
.L2371:
.L2372:
    leaq .STR102(%rip), %rax
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
    jz .L2381
    movq TOKEN_WRITE_FILE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2382
.L2381:
.L2382:
    leaq .STR103(%rip), %rax
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
    jz .L2391
    movq TOKEN_MEMORY_GET_BYTE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2392
.L2391:
.L2392:
    leaq .STR104(%rip), %rax
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
    jz .L2401
    movq TOKEN_MEMORY_SET_BYTE(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2402
.L2401:
.L2402:
    leaq .STR40(%rip), %rax
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
    jz .L2411
    movq TOKEN_BIT_SHIFT_LEFT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2412
.L2411:
.L2412:
    leaq .STR41(%rip), %rax
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
    jz .L2421
    movq TOKEN_BIT_SHIFT_RIGHT(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2422
.L2421:
.L2422:
    leaq .STR37(%rip), %rax
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
    jz .L2431
    movq TOKEN_BIT_AND(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2432
.L2431:
.L2432:
    leaq .STR38(%rip), %rax
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
    jz .L2441
    movq TOKEN_BIT_OR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2442
.L2441:
.L2442:
    leaq .STR39(%rip), %rax
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
    jz .L2451
    movq TOKEN_BIT_XOR(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2452
.L2451:
.L2452:
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    movq %rbp, %rsp
    popq %rbp
    ret


.globl check_single_char_token
check_single_char_token:
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
    jz .L2461
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    movq %rax, -48(%rbp)
    leaq .STR105(%rip), %rax
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    movq TOKEN_MINUS(%rip), %rax  # Load global variable
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
    jmp .L2462
.L2461:
    movq -16(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR106(%rip), %rax
    movq %rax, -72(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    movq TOKEN_COLON(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2472
.L2471:
    movq -16(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2481
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR107(%rip), %rax
    movq %rax, -80(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq TOKEN_LPAREN(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2482
.L2481:
    movq -16(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2491
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR108(%rip), %rax
    movq %rax, -88(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    movq TOKEN_RPAREN(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2492
.L2491:
    movq -16(%rbp), %rax
    pushq %rax
    movq $91, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR109(%rip), %rax
    movq %rax, -96(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    movq TOKEN_LBRACKET(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2502
.L2501:
    movq -16(%rbp), %rax
    pushq %rax
    movq $93, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2511
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR110(%rip), %rax
    movq %rax, -104(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq TOKEN_RBRACKET(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2512
.L2511:
    movq -16(%rbp), %rax
    pushq %rax
    movq $46, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2521
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR111(%rip), %rax
    movq %rax, -112(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq TOKEN_DOT(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2522
.L2521:
    movq -16(%rbp), %rax
    pushq %rax
    movq $44, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2531
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR112(%rip), %rax
    movq %rax, -120(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq TOKEN_COMMA(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2532
.L2531:
    movq -16(%rbp), %rax
    pushq %rax
    movq $124, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR113(%rip), %rax
    movq %rax, -128(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    movq TOKEN_PIPE(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2542
.L2541:
    movq -16(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2551
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR114(%rip), %rax
    movq %rax, -136(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    movq TOKEN_DOLLAR(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2552
.L2551:
    movq -16(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2561
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR115(%rip), %rax
    movq %rax, -144(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    movq TOKEN_PLUS(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2562
.L2561:
    movq -16(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $95, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2581
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2591
    leaq .STR116(%rip), %rax
    pushq %rax
    movq -160(%rbp), %rax
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
    jz .L2601
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    leaq .STR117(%rip), %rax
    pushq %rax
    movq TOKEN_INTRINSIC_STORE8(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2602
.L2601:
.L2602:
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -160(%rbp), %rax
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
    jz .L2611
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    leaq .STR119(%rip), %rax
    pushq %rax
    movq TOKEN_INTRINSIC_STORE(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2612
.L2611:
.L2612:
    leaq .STR120(%rip), %rax
    pushq %rax
    movq -160(%rbp), %rax
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
    jz .L2621
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    leaq .STR121(%rip), %rax
    pushq %rax
    movq TOKEN_INTRINSIC_LOAD8(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2622
.L2621:
.L2622:
    leaq .STR122(%rip), %rax
    pushq %rax
    movq -160(%rbp), %rax
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
    jz .L2631
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    leaq .STR123(%rip), %rax
    pushq %rax
    movq TOKEN_INTRINSIC_LOAD(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2632
.L2631:
.L2632:
    jmp .L2592
.L2591:
.L2592:
    leaq .STR124(%rip), %rax
    movq %rax, -168(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    movq TOKEN_IDENTIFIER(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2582
.L2581:
.L2582:
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $96, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
    movq -152(%rbp), %rax
    pushq %rax
    movq $123, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2652
.L2651:
.L2652:
    jmp .L2642
.L2641:
.L2642:
    movq -152(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    movq -152(%rbp), %rax
    pushq %rax
    movq $91, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2671
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2672
.L2671:
.L2672:
    jmp .L2662
.L2661:
.L2662:
    movq -152(%rbp), %rax
    pushq %rax
    movq $47, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2681
    movq -152(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2691
    movq $1, %rax
    pushq %rax
    leaq -176(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2692
.L2691:
.L2692:
    jmp .L2682
.L2681:
.L2682:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2711
    movq -184(%rbp), %rax
    pushq %rax
    leaq .STR125(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -192(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    movq $53, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2712
.L2711:
.L2712:
    jmp .L2702
.L2701:
.L2702:
    leaq .STR125(%rip), %rax
    movq %rax, -200(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    movq TOKEN_UNDERSCORE(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2572
.L2571:
    movq -16(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2721
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -208(%rbp)
    movq $0, %rax
    movq %rax, -216(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2731
    movq $0, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -224(%rbp)
    movq $1, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -232(%rbp)
    movq $2, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -240(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2741
    movq -232(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2751
    movq -240(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2761
    movq $1, %rax
    pushq %rax
    leaq -216(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2762
.L2761:
.L2762:
    jmp .L2752
.L2751:
.L2752:
    jmp .L2742
.L2741:
.L2742:
    jmp .L2732
.L2731:
.L2732:
    movq -216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2771
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_to_eol
    movq %rax, -248(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2772
.L2771:
.L2772:
    movq $1, %rax
    movq %rax, -256(%rbp)
.L2781:    movq -256(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2782
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2791
    movq $0, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2792
.L2791:
    movq -264(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2801
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_read_word
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2811
    movq $0, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -280(%rbp)
    movq $1, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -288(%rbp)
    movq $2, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -296(%rbp)
    movq $3, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -304(%rbp)
    movq $0, %rax
    movq %rax, -312(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $69, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2821
    movq -288(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2831
    movq -296(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2841
    movq -304(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2851
    movq $1, %rax
    pushq %rax
    leaq -312(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
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
    movq -312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2861
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_skip_to_eol
    movq %rax, -320(%rbp)
    movq $0, %rax
    pushq %rax
    leaq -256(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2862
.L2861:
.L2862:
    jmp .L2812
.L2811:
.L2812:
    jmp .L2802
.L2801:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2802:
.L2792:
    jmp .L2781
.L2782:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_next_token
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2722
.L2721:
    movq -16(%rbp), %rax
    pushq %rax
    movq $123, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2871
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR126(%rip), %rax
    movq %rax, -328(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    movq TOKEN_LBRACE(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2872
.L2871:
    movq -16(%rbp), %rax
    pushq %rax
    movq $125, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2881
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_advance
    pushq %rax
    leaq -48(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR127(%rip), %rax
    movq %rax, -336(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    movq TOKEN_RBRACE(%rip), %rax  # Load global variable
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call token_create
    pushq %rax
    leaq -64(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2882
.L2881:
.L2882:
.L2872:
.L2722:
.L2572:
.L2562:
.L2552:
.L2542:
.L2532:
.L2522:
.L2512:
.L2502:
.L2492:
.L2482:
.L2472:
.L2462:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl token_destroy
token_destroy:
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
    jz .L2891
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
    jz .L2901
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2902
.L2901:
.L2902:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2892
.L2891:
.L2892:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_alnum_char
is_alnum_char:
    pushq %rbp
    movq %rsp, %rbp
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    jz .L2911
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2912
.L2911:
.L2912:
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
    subq $16384, %rsp  # Pre-allocate stack frame (16KB, fits all known function sizes)
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
