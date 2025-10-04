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
    movq $0, %rax
    subq -8(%rbp), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $-5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
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
    movq $-10, %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    subq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    movq $7, %rax
    movq %rax, -40(%rbp)
    movq $0, %rax
    subq -40(%rbp), %rax
    addq $3, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $-4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    movq $15, %rax
    movq %rax, -56(%rbp)
    movq $0, %rax
    subq -56(%rbp), %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -56(%rbp), %rax
    pushq %rax
    movq $-15, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $4, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
.L32:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
