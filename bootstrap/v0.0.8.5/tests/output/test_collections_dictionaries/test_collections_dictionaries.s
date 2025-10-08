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
.STR0:    .string "FAIL: dict_size"
.STR1:    .string "FAIL: dict_get"
.STR2:    .string "FAIL: dict_has true"
.STR3:    .string "FAIL: dict_has false"
.STR4:    .string "FAIL: dict_set new"
.STR5:    .string "FAIL: dict_set update"
.STR6:    .string "FAIL: dict_remove"
.STR7:    .string "FAIL: dict_keys"
.STR8:    .string "FAIL: dict_values"
.STR9:    .string "FAIL: dictionary as variable"
.STR10:    .string "PASS: All dictionary tests"
.text
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    call dict_create
    pushq %rax  # Save dict pointer
    movq $1, %rax
    pushq %rax  # Save key
    movq $25, %rax
    pushq %rax  # Save value
    movq 16(%rsp), %rdi  # Load dict pointer
    movq 8(%rsp), %rsi   # Load key
    movq (%rsp), %rdx    # Load value
    call dict_set
    addq $16, %rsp  # Clean up key and value
    movq $2, %rax
    pushq %rax  # Save key
    movq $30, %rax
    pushq %rax  # Save value
    movq 16(%rsp), %rdi  # Load dict pointer
    movq 8(%rsp), %rsi   # Load key
    movq (%rsp), %rdx    # Load value
    call dict_set
    addq $16, %rsp  # Clean up key and value
    movq $3, %rax
    pushq %rax  # Save key
    movq $35, %rax
    pushq %rax  # Save value
    movq 16(%rsp), %rdi  # Load dict pointer
    movq 8(%rsp), %rsi   # Load key
    movq (%rsp), %rdx    # Load value
    call dict_set
    addq $16, %rsp  # Clean up key and value
    popq %rax  # Dict pointer as result
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call dict_size
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
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call dict_get
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $25, %rax
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
    movq $2, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call dict_has
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call dict_has
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
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
    call dict_create
    movq %rax, -48(%rbp)
    movq $100, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call dict_set
    movq $200, %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call dict_set
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call dict_size
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
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
    movq $999, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call dict_set
    movq $10, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call dict_get
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $999, %rax
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
    movq $10, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call dict_remove
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call dict_size
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
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
    call dict_create
    pushq %rax  # Save dict pointer
    movq $5, %rax
    pushq %rax  # Save key
    movq $50, %rax
    pushq %rax  # Save value
    movq 16(%rsp), %rdi  # Load dict pointer
    movq 8(%rsp), %rsi   # Load key
    movq (%rsp), %rdx    # Load value
    call dict_set
    addq $16, %rsp  # Clean up key and value
    movq $6, %rax
    pushq %rax  # Save key
    movq $60, %rax
    pushq %rax  # Save value
    movq 16(%rsp), %rdi  # Load dict pointer
    movq 8(%rsp), %rsi   # Load key
    movq (%rsp), %rdx    # Load value
    call dict_set
    addq $16, %rsp  # Clean up key and value
    popq %rax  # Dict pointer as result
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call dict_keys
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call list_length
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $2, %rax
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
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call dict_values
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call list_length
    movq %rax, -112(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $2, %rax
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
    movq $42, %rax
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
.L92:
    leaq .STR10(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
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
