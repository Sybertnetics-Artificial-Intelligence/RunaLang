    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

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
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %edx
    movl $1, %eax
    movl %eax, %ecx
    cmpl $0, %ecx
    jl .bounds_error_char_at_0
    cmpl %edx, %ecx
    jge .bounds_error_char_at_0
.safe_char_at_0:
    popq %rax
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rax
    movzbl (%rax), %eax
    jmp .char_at_end_0
.bounds_error_char_at_0:
    addq $16, %rsp
    movl $-1, %eax
.char_at_end_0:
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %edx
    movl $10, %eax
    movl %eax, %ecx
    cmpl $0, %ecx
    jl .bounds_error_char_at_1
    cmpl %edx, %ecx
    jge .bounds_error_char_at_1
.safe_char_at_1:
    popq %rax
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rax
    movzbl (%rax), %eax
    jmp .char_at_end_1
.bounds_error_char_at_1:
    addq $16, %rsp
    movl $-1, %eax
.char_at_end_1:
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq -24(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main

    .section .rodata
.LS0:
    .string "Hello"
