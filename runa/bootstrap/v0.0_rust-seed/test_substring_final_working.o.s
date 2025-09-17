    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    leaq .LS0(%rip), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    # Store string_ptr in its stack slot: -8(%rbp)
    movq %rax, -8(%rbp)
    movl $0, %eax
    # Store start_index in its stack slot: -16(%rbp)
    movl %eax, -16(%rbp)
    movl $5, %eax
    # Store substring_length in its stack slot: -24(%rbp)
    movl %eax, -24(%rbp)

    # --- Substring: Get total string length ---
    movq -8(%rbp), %rdi
    call strlen@PLT
    # Store total_length in its stack slot: -32(%rbp)
    movl %eax, -32(%rbp)

    # --- Substring: Bounds checking ---
    movl -16(%rbp), %eax
    cmpl $0, %eax
    jl .substring_bounds_error_0
    cmpl -32(%rbp), %eax
    jge .substring_bounds_error_0
    movl -24(%rbp), %eax
    cmpl $0, %eax
    jle .substring_bounds_error_0
    movl -16(%rbp), %eax
    addl -24(%rbp), %eax
    cmpl -32(%rbp), %eax
    jg .substring_bounds_error_0

.substring_safe_0:
    # --- Substring: Allocate memory ---
    movl -24(%rbp), %edi
    addl $1, %edi
    movslq %edi, %rdi
    call malloc@PLT
    # Store buffer_ptr in its stack slot: -40(%rbp)
    movq %rax, -40(%rbp)

    # --- Substring: Copy data ---
    movq -40(%rbp), %rdi
    movq -8(%rbp), %rsi
    movslq -16(%rbp), %rax
    addq %rax, %rsi
    movslq -24(%rbp), %rdx
    call memcpy@PLT

    # --- Substring: Add null terminator ---
    movq -40(%rbp), %rax
    movslq -24(%rbp), %rdx
    movb $0, (%rax,%rdx,1)

    # --- Substring: Return result ---
    movq -40(%rbp), %rax
    jmp .substring_end_0
.substring_bounds_error_0:
    movq $0, %rax
.substring_end_0:
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq -8(%rbp), %rax
    # Store string_ptr in its stack slot: -8(%rbp)
    movq %rax, -8(%rbp)
    movl $6, %eax
    # Store start_index in its stack slot: -16(%rbp)
    movl %eax, -16(%rbp)
    movl $5, %eax
    # Store substring_length in its stack slot: -24(%rbp)
    movl %eax, -24(%rbp)

    # --- Substring: Get total string length ---
    movq -8(%rbp), %rdi
    call strlen@PLT
    # Store total_length in its stack slot: -32(%rbp)
    movl %eax, -32(%rbp)

    # --- Substring: Bounds checking ---
    movl -16(%rbp), %eax
    cmpl $0, %eax
    jl .substring_bounds_error_1
    cmpl -32(%rbp), %eax
    jge .substring_bounds_error_1
    movl -24(%rbp), %eax
    cmpl $0, %eax
    jle .substring_bounds_error_1
    movl -16(%rbp), %eax
    addl -24(%rbp), %eax
    cmpl -32(%rbp), %eax
    jg .substring_bounds_error_1

.substring_safe_1:
    # --- Substring: Allocate memory ---
    movl -24(%rbp), %edi
    addl $1, %edi
    movslq %edi, %rdi
    call malloc@PLT
    # Store buffer_ptr in its stack slot: -40(%rbp)
    movq %rax, -40(%rbp)

    # --- Substring: Copy data ---
    movq -40(%rbp), %rdi
    movq -8(%rbp), %rsi
    movslq -16(%rbp), %rax
    addq %rax, %rsi
    movslq -24(%rbp), %rdx
    call memcpy@PLT

    # --- Substring: Add null terminator ---
    movq -40(%rbp), %rax
    movslq -24(%rbp), %rdx
    movb $0, (%rax,%rdx,1)

    # --- Substring: Return result ---
    movq -40(%rbp), %rax
    jmp .substring_end_1
.substring_bounds_error_1:
    movq $0, %rax
.substring_end_1:
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main

    .section .rodata
.LS0:
    .string "Hello World"
