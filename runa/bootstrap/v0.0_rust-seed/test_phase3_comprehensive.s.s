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
    movl $0, %eax
    movq %rax, -8(%rbp)
.L_while_start_0:
    movq -8(%rbp), %rax
    pushq %rax
    movl $5, %eax
    movl %eax, %ecx
    popq %rax
    cmpl %ecx, %eax
    setl %al
    movzbl %al, %eax
    testl %eax, %eax
    je .L_while_end_0
    movq -8(%rbp), %rax
    pushq %rax
    movl $1, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    jmp .L_while_start_0
.L_while_end_0:
    # List literal with 3 elements
    movl $3, %eax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $10, %eax
    pushq %rax
    movl $5, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main
