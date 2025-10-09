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
.STR0:    .string "Testing function pointers...\n\n"
.STR1:    .string "Test 1: Store function pointer:\n"
.STR2:    .string "  Stored pointer to 'add' function\n"
.STR3:    .string "  add_ptr value (address): "
.STR4:    .string "\n\n"
.STR5:    .string "Test 2: Direct function pointer call:\n"
.STR6:    .string "  $add(5, 3) = "
.STR7:    .string "\n  Expected: 8\n\n"
.STR8:    .string "Test 3: Multiple function pointer calls:\n"
.STR9:    .string "  $subtract(10, 4) = "
.STR10:    .string "\n  $multiply(6, 7) = "
.STR11:    .string "\n  Expected: 6, 42\n\n"
.STR12:    .string "Test 4: Store multiple pointers:\n"
.STR13:    .string "  Stored subtract_ptr and multiply_ptr\n"
.STR14:    .string "  subtract_ptr: "
.STR15:    .string "\n  multiply_ptr: "
.STR16:    .string "Test 5: Function pointers with expressions:\n"
.STR17:    .string "  x=12, y=3\n"
.STR18:    .string "  $add(x,y)="
.STR19:    .string ", $subtract(x,y)="
.STR20:    .string ", $multiply(x,y)="
.STR21:    .string "\n  Expected: 15, 9, 36\n\n"
.STR22:    .string "Test 6: Nested calls:\n"
.STR23:    .string "  $add($multiply(2,3), $subtract(10,5)) = "
.STR24:    .string "\n  Expected: 11 (6 + 5)\n\n"
.STR25:    .string "All function pointer tests completed!\n"
.text


.globl add
add:
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


.globl subtract
subtract:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    subq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl multiply
multiply:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl apply_operation
apply_operation:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
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
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq add(%rip), %rax
    movq %rax, -8(%rbp)
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -8(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $3, %rax
    pushq %rax
    movq $5, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq add(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -16(%rbp)
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -16(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $4, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq subtract(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -24(%rbp)
    movq $7, %rax
    pushq %rax
    movq $6, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq multiply(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -32(%rbp)
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -24(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq subtract(%rip), %rax
    movq %rax, -40(%rbp)
    leaq multiply(%rip), %rax
    movq %rax, -48(%rbp)
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -40(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -48(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR16(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $12, %rax
    movq %rax, -56(%rbp)
    movq $3, %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq add(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -72(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq subtract(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -80(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq multiply(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -88(%rbp)
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR18(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -72(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR19(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -80(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR20(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -88(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR21(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR22(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $5, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq subtract(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    pushq %rax
    movq $3, %rax
    pushq %rax
    movq $2, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq multiply(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    pushq %rax
    popq %rdi
    popq %rsi
    pushq %rdi
    pushq %rsi
    leaq add(%rip), %rax
    movq %rax, %r10  # Save function pointer
    popq %rsi
    popq %rdi
    call *%r10  # Indirect call through function pointer
    movq %rax, -96(%rbp)
    leaq .STR23(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -96(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR24(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR25(%rip), %rax
    movq %rax, %rdi
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
