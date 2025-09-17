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
    movl $1, %eax
    pushq %rax
    movl $0, %eax
    movl %eax, %ecx
    popq %rax
    cmpl %ecx, %eax
    setg %al
    movzbl %al, %eax
    testl %eax, %eax
    je .L_else_0
    jmp .L_end_0
.L_else_0:
.L_end_0:

    movl $0, %eax
    leave
    ret

    .size main, .-main
