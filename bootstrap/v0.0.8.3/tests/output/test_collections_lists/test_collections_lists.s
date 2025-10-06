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
.STR0:    .string "FAIL: list_length"
.STR1:    .string "FAIL: a list containing"
.STR2:    .string "FAIL: list_get"
.STR3:    .string "FAIL: list_set"
.STR4:    .string "FAIL: list_append"
.STR5:    .string "FAIL: list_insert"
.STR6:    .string "FAIL: list_remove"
.STR7:    .string "FAIL: list as variable"
.STR8:    .string "PASS: All list tests"
.text
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    call list_create
    pushq %rax  # Save list pointer
    movq $1, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    movq $2, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    movq $3, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    movq $4, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    movq $5, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    popq %rax  # List pointer as result
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call list_length
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    leaq .STR0(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2
.L1:
.L2:
    call list_create
    pushq %rax  # Save list pointer
    movq $10, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    movq $20, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    movq $30, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load list pointer
    movq (%rsp), %rsi   # Load element value
    call list_append
    popq %rax  # Clean up element value
    popq %rax  # List pointer as result
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq %rax, %rdi
    call list_length
    pushq %rax
    movq $0, %rax
    pushq %rax
.L11:
    movq (%rsp), %rax
    movq 8(%rsp), %rcx
    cmpq %rcx, %rax
    jge .L12
    movq 16(%rsp), %rdi
    movq (%rsp), %rsi
    call list_get
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    addq -40(%rbp), %rax
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq (%rsp), %rax
    addq $1, %rax
    movq %rax, (%rsp)
    jmp .L11
.L12:
    addq $24, %rsp
    movq -32(%rbp), %rax
    pushq %rax
    movq $60, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call list_get
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    leaq .STR2(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
.L32:
    movq $100, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call list_set
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call list_get
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    leaq .STR3(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
    call list_create
    movq %rax, -64(%rbp)
    movq $7, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call list_append
    movq $8, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call list_append
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call list_length
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    leaq .STR4(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
    movq $99, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call list_insert
    movq $1, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call list_get
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    leaq .STR5(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
.L62:
    movq $1, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call list_remove
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $99, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    leaq .STR6(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
    movq $42, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    leaq .STR7(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    leaq .STR8(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
