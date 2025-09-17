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
    movl $2, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    movl %eax, -4(%rbp)
    movl $10, %eax
    pushq %rax
    movl $3, %eax
    movl %eax, %ecx
    popq %rax
    subl %ecx, %eax
    movl %eax, -8(%rbp)
    movl -4(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl -8(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl -4(%rbp), %eax
    pushq %rax
    movl $3, %eax
    movl %eax, %ecx
    popq %rax
    cmpl %ecx, %eax
    sete %al
    movzbl %al, %eax
    testl %eax, %eax
    je .L_else_0
    movl $100, %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    jmp .L_end_0
.L_else_0:
    movl $200, %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
.L_end_0:

    movl $0, %eax
    leave
    ret

    .size main, .-main
