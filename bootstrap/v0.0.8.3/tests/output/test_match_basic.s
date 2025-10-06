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
    movq -8(%rbp), %rax
    pushq %rax  # Save match value
.match_0_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $5, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_0_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    jmp .match_0_end
.match_0_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $10, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_0_case_2  # Try next case
    popq %rax  # Matched, clean up stack
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_0_end
.match_0_case_2:
    popq %rax  # Matched, clean up stack
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_0_end
.match_0_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $99, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax  # Save match value
.match_1_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $5, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_1_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_1_end
.match_1_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $10, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_1_case_2  # Try next case
    popq %rax  # Matched, clean up stack
    movq $4, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_1_end
.match_1_case_2:
    popq %rax  # Matched, clean up stack
    jmp .match_1_end
.match_1_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
