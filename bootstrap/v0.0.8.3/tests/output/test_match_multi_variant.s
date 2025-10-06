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
.STR0:    .string "FAIL: Matched 0 instead of 42"
.STR1:    .string "FAIL: Matched 100 instead of 42"
.STR2:    .string "FAIL: First matched Second pattern"
.STR3:    .string "FAIL: Second matched First pattern"
.STR4:    .string "FAIL: One matched Two"
.STR5:    .string "FAIL: One matched Three"
.STR6:    .string "FAIL: Two matched One"
.STR7:    .string "FAIL: Two matched Three"
.STR8:    .string "FAIL: Three matched One"
.STR9:    .string "FAIL: Three matched Two"
.text
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $42, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax  # Save match value
.match_0_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $0, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_0_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_0_end
.match_0_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $42, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_0_case_2  # Try next case
    popq %rax  # Matched, clean up stack
    jmp .match_0_end
.match_0_case_2:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $100, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_0_end  # No match
    popq %rax  # Matched, clean up stack
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_0_end
.match_0_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax  # Save match value
.match_1_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_1_case_1  # Try next case
    popq %rax  # Get match value pointer
    jmp .match_1_end
.match_1_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_1_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_1_end
.match_1_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $1, (%rax)  # Store variant tag
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax  # Save match value
.match_2_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_2_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_2_end
.match_2_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_2_end  # No match
    popq %rax  # Get match value pointer
    jmp .match_2_end
.match_2_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -32(%rbp)
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $1, (%rax)  # Store variant tag
    movq %rax, -40(%rbp)
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $2, (%rax)  # Store variant tag
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax  # Save match value
.match_3_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_3_case_1  # Try next case
    popq %rax  # Get match value pointer
    jmp .match_3_end
.match_3_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_3_case_2  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_3_end
.match_3_case_2:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $2, %ebx  # Compare with expected tag
    jne .match_3_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_3_end
.match_3_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq -40(%rbp), %rax
    pushq %rax  # Save match value
.match_4_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_4_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_4_end
.match_4_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_4_case_2  # Try next case
    popq %rax  # Get match value pointer
    jmp .match_4_end
.match_4_case_2:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $2, %ebx  # Compare with expected tag
    jne .match_4_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_4_end
.match_4_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq -48(%rbp), %rax
    pushq %rax  # Save match value
.match_5_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_5_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_5_end
.match_5_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_5_case_2  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_5_end
.match_5_case_2:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $2, %ebx  # Compare with expected tag
    jne .match_5_end  # No match
    popq %rax  # Get match value pointer
    jmp .match_5_end
.match_5_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
