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
.STR0:    .string "Phase 1: Minimal Match Test"
.STR1:    .string "  ✓ Minimal match works"
.STR2:    .string "Phase 2: Literal Pattern Matching"
.STR3:    .string "  ✓ Exact match (5 = 5)"
.STR4:    .string "  ✗ FAIL: Matched 10 instead of 5"
.STR5:    .string "  ✗ FAIL: Matched wildcard instead of 5"
.STR6:    .string "  ✗ FAIL: Matched 5 for value 99"
.STR7:    .string "  ✗ FAIL: Matched 10 for value 99"
.STR8:    .string "  ✓ Wildcard catches non-matching value (99)"
.STR9:    .string "  ✗ FAIL: Matched 0 instead of 42"
.STR10:    .string "  ✓ Matched 42 correctly"
.STR11:    .string "  ✗ FAIL: Matched 100 instead of 42"
.STR12:    .string "Phase 3: Wildcard Pattern Tests"
.STR13:    .string "  ✗ FAIL: Matched 5 instead of wildcard"
.STR14:    .string "  ✗ FAIL: Matched 10 instead of wildcard"
.STR15:    .string "  ✓ Wildcard catches unmatched literal (100)"
.STR16:    .string "  ✓ Wildcard-only pattern catches everything"
.STR17:    .string "  ✓ Exact match (7) takes precedence over wildcard"
.STR18:    .string "  ✗ FAIL: Wildcard matched when exact match should"
.STR19:    .string "Phase 4: Basic Variant Pattern Matching"
.STR20:    .string "  ✓ Matched None variant"
.STR21:    .string "  ✗ FAIL: Matched Some when should be None"
.STR22:    .string "  ✗ FAIL: Matched None when should be Some"
.STR23:    .string "  ✓ Matched Some variant with data"
.STR24:    .string "Phase 5: Multi-Variant Pattern Matching"
.STR25:    .string "  ✓ First matched First"
.STR26:    .string "  ✗ FAIL: First matched Second pattern"
.STR27:    .string "  ✗ FAIL: Second matched First pattern"
.STR28:    .string "  ✓ Second matched Second"
.STR29:    .string "  ✓ One matched One (tag 0)"
.STR30:    .string "  ✗ FAIL: One matched Two"
.STR31:    .string "  ✗ FAIL: One matched Three"
.STR32:    .string "  ✗ FAIL: Two matched One"
.STR33:    .string "  ✓ Two matched Two (tag 1)"
.STR34:    .string "  ✗ FAIL: Two matched Three"
.STR35:    .string "  ✗ FAIL: Three matched One"
.STR36:    .string "  ✗ FAIL: Three matched Two"
.STR37:    .string "  ✓ Three matched Three (tag 2)"
.STR38:    .string "Phase 6: Type Pattern Matching"
.STR39:    .string "  ✓ Matched Integer type"
.STR40:    .string "  ✗ FAIL: Should have matched Integer"
.STR41:    .string "  ✗ FAIL: Should not match Integer for variant"
.STR42:    .string "  ✓ Correctly rejected Integer type for variant"
.STR43:    .string "  ✗ FAIL: Matched literal 50"
.STR44:    .string "  ✓ Matched Integer type in mixed pattern"
.STR45:    .string "  ✗ FAIL: Should have matched Integer type"
.STR46:    .string "Phase 7: Exhaustiveness Testing"
.STR47:    .string "  Test 7.1: Non-exhaustive Option (missing Some)"
.STR48:    .string "    ✓ Matched None (but Some is missing)"
.STR49:    .string "  Test 7.2: Exhaustive Option match (no warning expected)"
.STR50:    .string "    ✓ Matched None"
.STR51:    .string "    ✓ Some case covered (not executed)"
.STR52:    .string "  Test 7.3: Non-exhaustive Result (missing Error and Pending)"
.STR53:    .string "    ✓ Ok case covered (not executed)"
.STR54:    .string "All match statement tests passed successfully"
.text
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $5, %rax
    pushq %rax  # Save match value
.match_0_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $5, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_0_end  # No match
    popq %rax  # Matched, clean up stack
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_0_end
.match_0_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $5, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
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
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
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
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_1_end
.match_1_case_2:
    popq %rax  # Matched, clean up stack
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_1_end
.match_1_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $99, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax  # Save match value
.match_2_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $5, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_2_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_2_end
.match_2_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $10, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_2_case_2  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $4, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_2_end
.match_2_case_2:
    popq %rax  # Matched, clean up stack
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_2_end
.match_2_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $42, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax  # Save match value
.match_3_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $0, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_3_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $5, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_3_end
.match_3_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $42, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_3_case_2  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_3_end
.match_3_case_2:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $100, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_3_end  # No match
    popq %rax  # Matched, clean up stack
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $6, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_3_end
.match_3_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $100, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax  # Save match value
.match_4_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $5, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_4_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $7, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_4_end
.match_4_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $10, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_4_case_2  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_4_end
.match_4_case_2:
    popq %rax  # Matched, clean up stack
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_4_end
.match_4_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $42, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax  # Save match value
.match_5_case_0:
    popq %rax  # Matched, clean up stack
    leaq .STR16(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_5_end
.match_5_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $7, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax  # Save match value
.match_6_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $7, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_6_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_6_end
.match_6_case_1:
    popq %rax  # Matched, clean up stack
    leaq .STR18(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $9, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_6_end
.match_6_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR19(%rip), %rax
    movq %rax, %rdi
    call print_string
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax  # Save match value
.match_7_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_7_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR20(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_7_end
.match_7_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_7_end  # No match
    popq %rax  # Get match value pointer
    movq 8(%rax), %rbx  # Load field 0
    movq %rbx, -64(%rbp)  # Store in binding v
    leaq .STR21(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $10, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_7_end
.match_7_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $16, %rdi
    call allocate
    movl $1, (%rax)  # Store variant tag
    pushq %rax  # Save variant pointer
    movq $123, %rax
    movq (%rsp), %rbx  # Load variant pointer
    movq %rax, 8(%rbx)  # Store field 0
    popq %rax  # Restore variant pointer
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax  # Save match value
.match_8_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_8_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR22(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $11, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_8_end
.match_8_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_8_end  # No match
    popq %rax  # Get match value pointer
    movq 8(%rax), %rbx  # Load field 0
    movq %rbx, -64(%rbp)  # Store in binding v
    leaq .STR23(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_8_end
.match_8_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR24(%rip), %rax
    movq %rax, %rdi
    call print_string
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax  # Save match value
.match_9_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_9_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR25(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_9_end
.match_9_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_9_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR26(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $12, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_9_end
.match_9_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $1, (%rax)  # Store variant tag
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax  # Save match value
.match_10_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_10_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR27(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $13, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_10_end
.match_10_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_10_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR28(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_10_end
.match_10_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -104(%rbp)
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $1, (%rax)  # Store variant tag
    movq %rax, -112(%rbp)
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $2, (%rax)  # Store variant tag
    movq %rax, -120(%rbp)
    movq -104(%rbp), %rax
    pushq %rax  # Save match value
.match_11_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_11_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR29(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_11_end
.match_11_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_11_case_2  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR30(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $14, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_11_end
.match_11_case_2:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $2, %ebx  # Compare with expected tag
    jne .match_11_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR31(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $15, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_11_end
.match_11_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq -112(%rbp), %rax
    pushq %rax  # Save match value
.match_12_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_12_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR32(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $16, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_12_end
.match_12_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_12_case_2  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR33(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_12_end
.match_12_case_2:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $2, %ebx  # Compare with expected tag
    jne .match_12_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR34(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $17, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_12_end
.match_12_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq -120(%rbp), %rax
    pushq %rax  # Save match value
.match_13_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_13_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR35(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $18, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_13_end
.match_13_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_13_case_2  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR36(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $19, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_13_end
.match_13_case_2:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $2, %ebx  # Compare with expected tag
    jne .match_13_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR37(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_13_end
.match_13_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR38(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $42, %rax
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax  # Save match value
.match_14_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $4096, %rbx  # Pointer threshold
    cmpq %rbx, %rax  # Compare value with threshold
    jge .match_14_case_1  # Not Integer, try next case
    popq %rax  # Matched, clean up stack
    leaq .STR39(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_14_end
.match_14_case_1:
    popq %rax  # Matched, clean up stack
    leaq .STR40(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $20, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_14_end
.match_14_end:
    addq $8, %rsp  # Clean up match value if still on stack
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax  # Save match value
.match_15_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $4096, %rbx  # Pointer threshold
    cmpq %rbx, %rax  # Compare value with threshold
    jge .match_15_case_1  # Not Integer, try next case
    popq %rax  # Matched, clean up stack
    leaq .STR41(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $21, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_15_end
.match_15_case_1:
    popq %rax  # Matched, clean up stack
    leaq .STR42(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_15_end
.match_15_end:
    addq $8, %rsp  # Clean up match value if still on stack
    movq $100, %rax
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax  # Save match value
.match_16_case_0:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $50, %rax
    movq %rax, %rbx  # Pattern value to %rbx
    movq (%rsp), %rax  # Match value to %rax
    cmpq %rbx, %rax  # Compare
    jne .match_16_case_1  # Try next case
    popq %rax  # Matched, clean up stack
    leaq .STR43(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $22, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_16_end
.match_16_case_1:
    popq %rax  # Get match value
    pushq %rax  # Keep for next comparison
    movq $4096, %rbx  # Pointer threshold
    cmpq %rbx, %rax  # Compare value with threshold
    jge .match_16_case_2  # Not Integer, try next case
    popq %rax  # Matched, clean up stack
    leaq .STR44(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_16_end
.match_16_case_2:
    popq %rax  # Matched, clean up stack
    leaq .STR45(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $23, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .match_16_end
.match_16_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR46(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR47(%rip), %rax
    movq %rax, %rdi
    call print_string
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax  # Save match value
.match_17_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_17_end  # No match
    popq %rax  # Get match value pointer
    leaq .STR48(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_17_end
.match_17_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR49(%rip), %rax
    movq %rax, %rdi
    call print_string
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $0, (%rax)  # Store variant tag
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax  # Save match value
.match_18_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_18_case_1  # Try next case
    popq %rax  # Get match value pointer
    leaq .STR50(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_18_end
.match_18_case_1:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $1, %ebx  # Compare with expected tag
    jne .match_18_end  # No match
    popq %rax  # Get match value pointer
    movq 8(%rax), %rbx  # Load field 0
    movq %rbx, -64(%rbp)  # Store in binding v
    leaq .STR51(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_18_end
.match_18_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR52(%rip), %rax
    movq %rax, %rdi
    call print_string
    # Allocate variant
    movq $8, %rdi
    call allocate
    movl $2, (%rax)  # Store variant tag
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax  # Save match value
.match_19_case_0:
    movq (%rsp), %rax  # Get match value pointer
    movl (%rax), %ebx  # Load variant tag
    cmpl $0, %ebx  # Compare with expected tag
    jne .match_19_end  # No match
    popq %rax  # Get match value pointer
    movq 8(%rax), %rbx  # Load field 0
    movq %rbx, -64(%rbp)  # Store in binding v
    leaq .STR53(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .match_19_end
.match_19_end:
    addq $8, %rsp  # Clean up match value if still on stack
    leaq .STR54(%rip), %rax
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
