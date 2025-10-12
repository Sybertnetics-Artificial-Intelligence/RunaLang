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
.STR0:    .string "Test: Simple Function Call Range Propagation"
.STR1:    .string "  ✓ PASS - Function returned 42"
.STR2:    .string "  ✗ FAIL - x = "
.STR3:    .string "Test: Chained Function Calls"
.STR4:    .string "  ✓ PASS - Chained calls work, result = 142"
.STR5:    .string "  ✗ FAIL - result = "
.STR6:    .string "Test: Recursion Handled Safely"
.STR7:    .string "  ✓ PASS - Recursion works correctly, 5! = 120"
.STR8:    .string "Test: Call Graph Bottom-Up Analysis"
.STR9:    .string "  ✓ PASS - Bottom-up analysis correct"
.STR10:    .string "  ✗ FAIL"
.STR11:    .string "===== Inter-Procedural Analysis Test Suite ====="
.STR12:    .string ""
.STR13:    .string "===== Results ====="
.STR14:    .string "Passed: "
.STR15:    .string " / "
.STR16:    .string " - ALL TESTS PASSED!"
.STR17:    .string " - SOME TESTS FAILED"
.text


.globl get_small_number
get_small_number:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $42, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl get_medium_number
get_medium_number:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $100, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl add_two_small_numbers
add_two_small_numbers:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    addq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl factorial
factorial:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
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
    movq -8(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call factorial
    popq %rbx
    imulq %rbx, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_simple_function_call
test_simple_function_call:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    call get_small_number
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $42, %rax
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
.L12:
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_chained_function_calls
test_chained_function_calls:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    call get_small_number
    movq %rax, -8(%rbp)
    call get_medium_number
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call add_two_small_numbers
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L22:
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_recursion_safety
test_recursion_safety:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $5, %rax
    pushq %rax
    popq %rdi
    call factorial
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
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
.L32:
    movq %rbp, %rsp
    popq %rbp
    ret


.globl test_call_graph_bottom_up
test_call_graph_bottom_up:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    call get_small_number
    movq %rax, -8(%rbp)
    call get_medium_number
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call add_two_small_numbers
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $142, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L42:
    movq %rbp, %rsp
    popq %rbp
    ret
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rax, -8(%rbp)
    movq $4, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    call test_simple_function_call
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    call test_chained_function_calls
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    call test_recursion_safety
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    call test_call_graph_bottom_up
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -8(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR15(%rip), %rax
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
    jz .L51
    leaq .STR16(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L52:
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
