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
.STR0:    .string "PASS: If condition true"
.STR1:    .string "FAIL: If condition true"
.STR2:    .string "FAIL: If condition false"
.STR3:    .string "PASS: If condition false"
.STR4:    .string "PASS: Simple Otherwise If - first condition (got 100)"
.STR5:    .string "FAIL: Simple Otherwise If - first condition (expected 100)"
.STR6:    .string "PASS: Simple Otherwise If - second condition (got 200)"
.STR7:    .string "FAIL: Simple Otherwise If - second condition (expected 200)"
.STR8:    .string "PASS: Simple Otherwise If - default Otherwise (got 999)"
.STR9:    .string "FAIL: Simple Otherwise If - default Otherwise (expected 999)"
.STR10:    .string "PASS: Multi Otherwise If - condition 1"
.STR11:    .string "FAIL: Multi Otherwise If - condition 1"
.STR12:    .string "PASS: Multi Otherwise If - condition 3"
.STR13:    .string "FAIL: Multi Otherwise If - condition 3"
.STR14:    .string "PASS: Multi Otherwise If - condition 5"
.STR15:    .string "FAIL: Multi Otherwise If - condition 5"
.STR16:    .string "PASS: Multi Otherwise If - default Otherwise"
.STR17:    .string "FAIL: Multi Otherwise If - default Otherwise"
.STR18:    .string "PASS: Nested Otherwise If - (1,1)"
.STR19:    .string "FAIL: Nested Otherwise If - (1,1)"
.STR20:    .string "PASS: Nested Otherwise If - (1,2)"
.STR21:    .string "FAIL: Nested Otherwise If - (1,2)"
.STR22:    .string "PASS: Nested Otherwise If - (2,1)"
.STR23:    .string "FAIL: Nested Otherwise If - (2,1)"
.STR24:    .string "PASS: Nested Otherwise If - (2,2)"
.STR25:    .string "FAIL: Nested Otherwise If - (2,2)"
.STR26:    .string "PASS: Nested Otherwise If - (9,9) default"
.STR27:    .string "FAIL: Nested Otherwise If - (9,9) default"
.STR28:    .string "PASS: Complex conditions - less than 10"
.STR29:    .string "FAIL: Complex conditions - less than 10"
.STR30:    .string "PASS: Complex conditions - 10-19"
.STR31:    .string "FAIL: Complex conditions - 10-19"
.STR32:    .string "PASS: Complex conditions - 20-29"
.STR33:    .string "FAIL: Complex conditions - 20-29"
.STR34:    .string "PASS: Complex conditions - 30+"
.STR35:    .string "FAIL: Complex conditions - 30+"
.STR36:    .string "PASS: No Otherwise - condition 1"
.STR37:    .string "FAIL: No Otherwise - condition 1"
.STR38:    .string "PASS: No Otherwise - condition 2"
.STR39:    .string "FAIL: No Otherwise - condition 2"
.STR40:    .string "PASS: No Otherwise - fall through"
.STR41:    .string "FAIL: No Otherwise - fall through"
.STR42:    .string "PASS: While loop sum"
.STR43:    .string "FAIL: While loop sum"
.text


.globl test_simple_otherwise_if
test_simple_otherwise_if:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    movq $100, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2
.L1:
    movq -8(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $200, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L12
.L11:
    movq $999, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L12:
.L2:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_multi_otherwise_if
test_multi_otherwise_if:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    movq $10, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L22
.L21:
    movq -8(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $20, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L32
.L31:
    movq -8(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq $30, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L42
.L41:
    movq -8(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    movq $40, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L52
.L51:
    movq -8(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $50, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L62
.L61:
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L62:
.L52:
.L42:
.L32:
.L22:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_nested_otherwise_if
test_nested_otherwise_if:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    movq $11, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L82
.L81:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq $12, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L92
.L91:
    movq $10, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L92:
.L82:
    jmp .L72
.L71:
    movq -8(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq $21, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L112
.L111:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq $22, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L122
.L121:
    movq $20, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L122:
.L112:
    jmp .L102
.L101:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq $91, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L132
.L131:
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq $92, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L142
.L141:
    movq $99, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L142:
.L132:
.L102:
.L72:
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_complex_conditions
test_complex_conditions:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq $1, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L152
.L151:
    movq -8(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L161
    movq -8(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq $2, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L172
.L171:
    movq -8(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq $3, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L182
.L181:
    movq $4, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L182:
.L172:
    jmp .L162
.L161:
    movq $0, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L162:
.L152:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_no_otherwise
test_no_otherwise:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $99, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq $10, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L192
.L191:
    movq -8(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq $20, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L202
.L201:
    movq -8(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $30, %rax
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L212
.L211:
.L212:
.L202:
.L192:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $10, %rax
    movq %rax, -8(%rbp)
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L222
.L221:
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
.L222:
    movq -8(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L231
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L232
.L231:
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
.L232:
    movq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call test_simple_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L242
.L241:
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
.L242:
    movq $2, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call test_simple_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $200, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L251
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L252
.L251:
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
.L252:
    movq $99, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call test_simple_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $999, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L262
.L261:
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
.L262:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call test_multi_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L272
.L271:
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
.L272:
    movq $3, %rax
    pushq %rax
    popq %rdi
    call test_multi_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L282
.L281:
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
.L282:
    movq $5, %rax
    pushq %rax
    popq %rdi
    call test_multi_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L292
.L291:
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
.L292:
    movq $99, %rax
    pushq %rax
    popq %rdi
    call test_multi_otherwise_if
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
    jz .L301
    leaq .STR16(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L302
.L301:
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
.L302:
    movq $1, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call test_nested_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    leaq .STR18(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L312
.L311:
    leaq .STR19(%rip), %rax
    movq %rax, %rdi
    call print_string
.L312:
    movq $2, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call test_nested_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    leaq .STR20(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L322
.L321:
    leaq .STR21(%rip), %rax
    movq %rax, %rdi
    call print_string
.L322:
    movq $1, %rax
    pushq %rax
    movq $2, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call test_nested_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $21, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L331
    leaq .STR22(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L332
.L331:
    leaq .STR23(%rip), %rax
    movq %rax, %rdi
    call print_string
.L332:
    movq $2, %rax
    pushq %rax
    movq $2, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call test_nested_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $22, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L341
    leaq .STR24(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L342
.L341:
    leaq .STR25(%rip), %rax
    movq %rax, %rdi
    call print_string
.L342:
    movq $9, %rax
    pushq %rax
    movq $9, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call test_nested_otherwise_if
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
    leaq .STR26(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L352
.L351:
    leaq .STR27(%rip), %rax
    movq %rax, %rdi
    call print_string
.L352:
    movq $5, %rax
    pushq %rax
    popq %rdi
    call test_complex_conditions
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    leaq .STR28(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L362
.L361:
    leaq .STR29(%rip), %rax
    movq %rax, %rdi
    call print_string
.L362:
    movq $15, %rax
    pushq %rax
    popq %rdi
    call test_complex_conditions
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    leaq .STR30(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L372
.L371:
    leaq .STR31(%rip), %rax
    movq %rax, %rdi
    call print_string
.L372:
    movq $25, %rax
    pushq %rax
    popq %rdi
    call test_complex_conditions
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    leaq .STR32(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L382
.L381:
    leaq .STR33(%rip), %rax
    movq %rax, %rdi
    call print_string
.L382:
    movq $35, %rax
    pushq %rax
    popq %rdi
    call test_complex_conditions
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L391
    leaq .STR34(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L392
.L391:
    leaq .STR35(%rip), %rax
    movq %rax, %rdi
    call print_string
.L392:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call test_no_otherwise
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    leaq .STR36(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L402
.L401:
    leaq .STR37(%rip), %rax
    movq %rax, %rdi
    call print_string
.L402:
    movq $2, %rax
    pushq %rax
    popq %rdi
    call test_no_otherwise
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    leaq .STR38(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L412
.L411:
    leaq .STR39(%rip), %rax
    movq %rax, %rdi
    call print_string
.L412:
    movq $99, %rax
    pushq %rax
    popq %rdi
    call test_no_otherwise
    pushq %rax
    leaq -16(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -16(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    leaq .STR40(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L422
.L421:
    leaq .STR41(%rip), %rax
    movq %rax, %rdi
    call print_string
.L422:
    movq $0, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
.L431:    movq -32(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L432
    movq -40(%rbp), %rax
    addq -32(%rbp), %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L431
.L432:
    movq -40(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    leaq .STR42(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L442
.L441:
    leaq .STR43(%rip), %rax
    movq %rax, %rdi
    call print_string
.L442:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
