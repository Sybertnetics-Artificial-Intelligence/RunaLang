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


.globl hash
hash:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1000, %rax
    movq %rax, %rcx
    popq %rax
    testq %rcx, %rcx
    jz .Lmod_by_zero_0
    cqto
    idivq %rcx
    movq %rdx, %rax
    jmp .Lmod_done_0
.Lmod_by_zero_0:
    movq $0, %rax
.Lmod_done_0:
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl ht_insert
ht_insert:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call hash
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -40(%rbp), %rax
    addq $8, %rax
    movq %rax, -48(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
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


.globl ht_lookup
ht_lookup:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call hash
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq -32(%rbp), %rax
    addq $8, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $1000, %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    movq %rax, -24(%rbp)
.L21:    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L22
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L21
.L22:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L31:    movq -24(%rbp), %rax
    pushq %rax
    movq $10000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L32
    movq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call ht_insert
    movq %rax, -48(%rbp)
    movq -24(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L31
.L32:
    movq $0, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $0, %rax
    movq %rax, -56(%rbp)
.L41:    movq -24(%rbp), %rax
    pushq %rax
    movq $10000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L42
    movq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call ht_lookup
    movq %rax, -40(%rbp)
    movq -56(%rbp), %rax
    addq -40(%rbp), %rax
    pushq %rax
    leaq -56(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L41
.L42:
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
