    .section .rodata
.LC0:
    .string "%d\n"

    .text
    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    leaq .LS0(%rip), %rax
    movl %eax, -4(%rbp)
    movl -4(%rbp), %eax
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
    .string "Hello, World!"
