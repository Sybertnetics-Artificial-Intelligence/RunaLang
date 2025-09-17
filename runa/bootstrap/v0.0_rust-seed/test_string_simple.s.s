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
    movl %eax, %esi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl %eax, -4(%rbp)

    movl $0, %eax
    leave
    ret

    .size main, .-main

    .section .rodata
.LS0:
    .string "Hello, World!"
