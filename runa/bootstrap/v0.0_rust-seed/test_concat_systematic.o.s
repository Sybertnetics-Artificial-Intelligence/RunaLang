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
    leaq .LS1(%rip), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    # Store str2_ptr in its stack slot: -16(%rbp)
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    # Store str1_ptr in its stack slot: -8(%rbp)
    movq %rax, -8(%rbp)

    # --- Concat: Get length of str1 ---
    movq -8(%rbp), %rdi
    call strlen@PLT
    # Store len1 in its stack slot: -24(%rbp)
    movq %rax, -24(%rbp)

    # --- Concat: Get length of str2 ---
    movq -16(%rbp), %rdi
    call strlen@PLT
    # Store len2 in its stack slot: -32(%rbp)
    movq %rax, -32(%rbp)

    # --- Concat: Allocate new buffer ---
    movq -24(%rbp), %rax
    addq -32(%rbp), %rax
    # Store total_len in its stack slot: -40(%rbp)
    movq %rax, -40(%rbp)
    incq %rax
    movq %rax, %rdi
    call malloc@PLT
    # Store new_buffer_ptr in its stack slot: -48(%rbp)
    movq %rax, -48(%rbp)

    # --- Concat: Copy str1 ---
    movq -48(%rbp), %rdi
    movq -8(%rbp), %rsi
    movq -24(%rbp), %rdx
    call memcpy@PLT

    # --- Concat: Copy str2 ---
    movq -48(%rbp), %rdi
    addq -24(%rbp), %rdi
    movq -16(%rbp), %rsi
    movq -32(%rbp), %rdx
    call memcpy@PLT

    # --- Concat: Add null terminator ---
    movq -48(%rbp), %rax
    addq -40(%rbp), %rax
    movb $0, (%rax)

    # --- Concat: Set return value ---
    movq -48(%rbp), %rax
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
    .string "Hello"
.LS1:
    .string " World"
