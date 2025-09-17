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
    leaq .LS1(%rip), %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq 8(%rsp), %rdi
    call strlen@PLT
    movl %eax, %ecx
    movq (%rsp), %rdi
    call strlen@PLT
    movl %eax, %edx
    addl %ecx, %edx
    addl $1, %edx
    movslq %edx, %rdi
    call malloc@PLT
    movq %rax, %r10
    movq %r10, %rdi
    movq 8(%rsp), %rsi
    movslq %ecx, %rdx
    call memcpy@PLT
    movq %r10, %rdi
    movslq %ecx, %rcx
    addq %rcx, %rdi
    popq %rsi
    addq $8, %rsp
    pushq %rdi
    pushq %rsi
    movq %rsi, %rdi
    call strlen@PLT
    movslq %eax, %rdx
    popq %rsi
    popq %rdi
    call memcpy@PLT
    movq %r10, %rdi
    movslq %ecx, %rcx
    movslq %eax, %rax
    addq %rcx, %rax
    movb $0, (%r10,%rax,1)
    movq %r10, %rax
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
