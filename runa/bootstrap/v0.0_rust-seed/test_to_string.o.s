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
    movl $42, %eax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movl %eax, %r11d
    movl $12, %edi
    call malloc@PLT
    movq %rax, %r10
    movq %r10, %rdi
    leaq .LC0(%rip), %rsi
    movl $0x00006425, %esi
    pushq %rsi
    movq %rsp, %rsi
    movl %r11d, %edx
    call sprintf@PLT
    addq $8, %rsp
    movq %r10, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main
