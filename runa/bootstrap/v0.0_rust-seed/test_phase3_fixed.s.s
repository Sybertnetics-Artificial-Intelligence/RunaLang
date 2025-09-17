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
    movl $0, %eax
    movl %eax, -4(%rbp)
.L_while_start_0:
    movl -4(%rbp), %eax
    pushq %rax
    movl $5, %eax
    movl %eax, %ecx
    popq %rax
    cmpl %ecx, %eax
    setl %al
    movzbl %al, %eax
    testl %eax, %eax
    je .L_while_end_0
    movl -4(%rbp), %eax
    pushq %rax
    movl $1, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    movl %eax, -4(%rbp)
    movl -4(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    jmp .L_while_start_0
.L_while_end_0:
    # List literal with 3 elements
    movl $3, %eax
    movl %eax, -8(%rbp)
    movl -8(%rbp), %eax
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
    movl %eax, -12(%rbp)
    movl -12(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main
