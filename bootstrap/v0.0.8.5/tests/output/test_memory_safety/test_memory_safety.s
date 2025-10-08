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


.globl create_array
create_array:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $8, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    addq $8, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
.L1:    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2
    movq -40(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
    jmp .L1
.L2:
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_valid_operations
test_valid_operations:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $5, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -8(%rbp)
    movq $0, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -16(%rbp)
    movq $4, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    movq -24(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_bounds_validation
test_bounds_validation:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $3, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -8(%rbp)
    movq $0, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -16(%rbp)
    movq $1, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -24(%rbp)
    movq $2, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -32(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
.L32:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
    movq -32(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_variable_index
test_variable_index:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $10, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -8(%rbp)
    movq $5, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
.L62:
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_memory_lifecycle
test_memory_lifecycle:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $64, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -8(%rbp)
    movq $42, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
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
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_multiple_arrays
test_multiple_arrays:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $2, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -8(%rbp)
    movq $3, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -16(%rbp)
    movq $4, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -24(%rbp)
    movq $1, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -32(%rbp)
    movq $2, %rax
    pushq %rax  # Save index
    movq -16(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -40(%rbp)
    movq $3, %rax
    pushq %rax  # Save index
    movq -24(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -16(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    movq -40(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -16(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
.L92:
    movq -48(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -16(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
.L102:
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -16(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_edge_cases
test_edge_cases:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $1, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -8(%rbp)
    movq $0, %rax
    pushq %rax  # Save index
    movq -8(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L112
.L111:
.L112:
    movq -8(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $100, %rax
    pushq %rax
    popq %rdi
    call create_array
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax  # Save index
    movq -24(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -32(%rbp)
    movq $99, %rax
    pushq %rax  # Save index
    movq -24(%rbp), %rax
    popq %rbx  # Load index
    # Runtime bounds check: ensure index >= 0
    cmpq $0, %rbx
    jl .bounds_error_negative
    # Runtime bounds check: ensure index < size
    movq -8(%rax), %rcx  # Load array size from metadata
    cmpq %rcx, %rbx  # Compare index with size
    jge .bounds_error_overflow
    imulq $8, %rbx  # Multiply index by 8
    addq %rbx, %rax  # Add offset to array pointer
    movq (%rax), %rax  # Load value from array
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L122
.L121:
.L122:
    movq -40(%rbp), %rax
    pushq %rax
    movq $990, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L132
.L131:
.L132:
    movq -24(%rbp), %rax
    subq $8, %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
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
    movq $0, %rax
    movq %rax, -8(%rbp)
    call test_valid_operations
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq -8(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L142
.L141:
.L142:
    call test_bounds_validation
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq -8(%rbp), %rax
    addq $10, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L152
.L151:
.L152:
    call test_variable_index
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L161
    movq -8(%rbp), %rax
    addq $20, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L162
.L161:
.L162:
    call test_memory_lifecycle
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq -8(%rbp), %rax
    addq $30, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L172
.L171:
.L172:
    call test_multiple_arrays
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq -8(%rbp), %rax
    addq $40, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L182
.L181:
.L182:
    call test_edge_cases
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq -8(%rbp), %rax
    addq $50, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L192
.L191:
.L192:
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
