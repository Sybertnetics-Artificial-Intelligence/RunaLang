.section .rodata
.STR0:    .string "PASS: is equal to"
.STR1:    .string "FAIL: is equal to"
.STR2:    .string "PASS: is not equal to"
.STR3:    .string "FAIL: is not equal to"
.STR4:    .string "PASS: is less than"
.STR5:    .string "FAIL: is less than"
.STR6:    .string "PASS: is greater than"
.STR7:    .string "FAIL: is greater than"
.STR8:    .string "PASS: is less than or equal to"
.STR9:    .string "FAIL: is less than or equal to"
.STR10:    .string "PASS: is greater than or equal to"
.STR11:    .string "FAIL: is greater than or equal to"
.STR12:    .string "PASS: is not less than"
.STR13:    .string "FAIL: is not less than"
.STR14:    .string "PASS: is not greater than"
.STR15:    .string "FAIL: is not greater than"

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
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $5, %rax
    movq %rax, -8(%rbp)
    movq $10, %rax
    movq %rax, -16(%rbp)
    movq $5, %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L2
.L1:
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
.L2:
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L12
.L11:
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
.L12:
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L22
.L21:
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
.L22:
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L32
.L31:
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
.L32:
    movq -8(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L42
.L41:
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
.L42:
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L52
.L51:
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
.L52:
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L62
.L61:
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
.L62:
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L72
.L71:
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
.L72:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
