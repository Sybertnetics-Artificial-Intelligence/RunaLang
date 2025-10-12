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
.STR0:    .string "Test: If Branch Merge"
.STR1:    .string "  ✓ PASS - Took then branch, x = 50"
.STR2:    .string "  ✗ FAIL - Unexpected value"
.STR3:    .string "Test: Nested If Statements"
.STR4:    .string "  ✓ PASS - result = 100"
.STR5:    .string "  ✗ FAIL - result = "
.STR6:    .string "Test: Backward Propagation (range refinement from conditionals)"
.STR7:    .string "  ✓ PASS - Backward propagation worked, y = 90"
.STR8:    .string "  ✗ FAIL - y = "
.STR9:    .string "  ✗ FAIL - Should have entered if branch"
.STR10:    .string "Test: Loop Bound Analysis"
.STR11:    .string "  ✓ PASS - Loop analysis correct, sum = 15"
.STR12:    .string "  ✗ FAIL - sum = "
.STR13:    .string "===== Control Flow Test Suite ====="
.STR14:    .string ""
.STR15:    .string "===== Results ====="
.STR16:    .string "Passed: "
.STR17:    .string " / "
.STR18:    .string " - ALL TESTS PASSED!"
.STR19:    .string " - SOME TESTS FAILED"
.text


.globl test_if_branch_merge
test_if_branch_merge:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rax, -8(%rbp)
    movq $1, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    movq $50, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2
.L1:
    movq $200, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L2:
    movq -8(%rbp), %rax
    pushq %rax
    movq $50, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L12:
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_nested_if
test_nested_if:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rax, -8(%rbp)
    movq $1, %rax
    movq %rax, -16(%rbp)
    movq $10, %rax
    pushq %rax
.L21:
    movq -16(%rbp), %rax
    movq (%rsp), %rcx
    cmpq %rcx, %rax
    jg .L22
    movq -16(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq -8(%rbp), %rax
    addq -16(%rbp), %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L32
.L31:
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq -8(%rbp), %rax
    addq $10, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L42
.L41:
    movq -8(%rbp), %rax
    addq $20, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L42:
.L32:
    movq $1, %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rcx
    addq %rcx, %rax
    movq %rax, -16(%rbp)
    jmp .L21
.L22:
    popq %rax
    movq -8(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L52:
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_backward_propagation
test_backward_propagation:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $50, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $100, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq -8(%rbp), %rax
    addq $40, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L72:
    jmp .L62
.L61:
.L62:
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_loop_bound_analysis
test_loop_bound_analysis:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rax, -8(%rbp)
    movq $1, %rax
    movq %rax, -16(%rbp)
    movq $5, %rax
    pushq %rax
.L81:
    movq -16(%rbp), %rax
    movq (%rsp), %rcx
    cmpq %rcx, %rax
    jg .L82
    movq -8(%rbp), %rax
    addq -16(%rbp), %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq $1, %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rcx
    addq %rcx, %rax
    movq %rax, -16(%rbp)
    jmp .L81
.L82:
    popq %rax
    movq -8(%rbp), %rax
    pushq %rax
    movq $15, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L92:
    movq %rbp, %rsp
    popq %rbp
    ret
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rax, -8(%rbp)
    movq $4, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    call test_if_branch_merge
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    call test_nested_if
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    call test_backward_propagation
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    call test_loop_bound_analysis
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR16(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    leaq .STR18(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
    leaq .STR19(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L102:
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
