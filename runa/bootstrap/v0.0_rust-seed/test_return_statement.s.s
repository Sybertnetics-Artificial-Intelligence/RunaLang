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
    movl $42, %eax
    movl %eax, -4(%rbp)
    movl -4(%rbp), %eax
    leave
    ret

    movl $0, %eax
    leave
    ret

    .size main, .-main
