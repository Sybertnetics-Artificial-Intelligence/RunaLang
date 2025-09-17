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
    movl $5, %eax
    movl %eax, -4(%rbp)

    movl $0, %eax
    leave
    ret

    .size main, .-main
