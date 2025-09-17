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
    movl -4(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
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
