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
.STR0:    .string "FAIL: set duplicate removal"
.STR1:    .string "FAIL: a set containing"
.STR2:    .string "FAIL: set_contains true"
.STR3:    .string "FAIL: set_contains false"
.STR4:    .string "FAIL: set_add"
.STR5:    .string "FAIL: set_remove"
.STR6:    .string "FAIL: set_union"
.STR7:    .string "FAIL: set_intersection"
.STR8:    .string "FAIL: set as variable"
.STR9:    .string "PASS: All set tests"
.text
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    call set_create
    pushq %rax  # Save set pointer
    movq $1, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $2, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $3, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $2, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $1, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    popq %rax  # Set pointer as result
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_size
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $3, %rax
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
    call set_create
    pushq %rax  # Save set pointer
    movq $10, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $20, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $30, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    popq %rax  # Set pointer as result
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_size
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    movq $20, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_contains
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR2(%rip), %rax
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
    movq $99, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_contains
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    leaq .STR3(%rip), %rax
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
    call set_create
    movq %rax, -56(%rbp)
    movq $5, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_add
    movq $10, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_add
    movq $5, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_add
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_size
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    leaq .STR4(%rip), %rax
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
    movq $5, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_remove
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_size
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    leaq .STR5(%rip), %rax
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
    call set_create
    pushq %rax  # Save set pointer
    movq $1, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $2, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $3, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    popq %rax  # Set pointer as result
    movq %rax, -80(%rbp)
    call set_create
    pushq %rax  # Save set pointer
    movq $3, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $4, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    movq $5, %rax
    pushq %rax  # Save element value
    movq 8(%rsp), %rdi  # Load set pointer
    movq (%rsp), %rsi   # Load element value
    call set_add
    popq %rax  # Clean up element value
    popq %rax  # Set pointer as result
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_union
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_size
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    leaq .STR6(%rip), %rax
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
    movq -88(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call set_intersection
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_size
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    leaq .STR7(%rip), %rax
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
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    leaq .STR8(%rip), %rax
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
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
