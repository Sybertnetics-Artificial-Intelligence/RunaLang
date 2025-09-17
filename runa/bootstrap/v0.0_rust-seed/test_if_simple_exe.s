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
    movl $25, %eax
    movl %eax, -4(%rbp)
    movl -4(%rbp), %eax
    pushq %rax
    movl $20, %eax
    movl %eax, %ecx
    popq %rax
    cmpl %ecx, %eax
    setg %al
    movzbl %al, %eax
    testl %eax, %eax
    je .L_else_0
    movl $1, %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    jmp .L_end_0
.L_else_0:
    movl $0, %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
.L_end_0:

    movl $0, %eax
    leave
    ret

    .size main, .-main
