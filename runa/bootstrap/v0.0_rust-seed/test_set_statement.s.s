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
    movl $10, %eax
    movl %eax, -4(%rbp)
    movl -4(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $20, %eax
    movl %eax, -4(%rbp)
    movl -4(%rbp), %eax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl -4(%rbp), %eax
    pushq %rax
    movl $5, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
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
