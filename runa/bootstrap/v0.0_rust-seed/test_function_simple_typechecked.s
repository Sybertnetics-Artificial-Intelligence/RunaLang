    .section .rodata
.LC0:
    .string "%d\n"

    .text
    .globl runa_function_add_five
    .type runa_function_add_five, @function
runa_function_add_five:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl %edi, -4(%rbp)
    movl -4(%rbp), %eax
    pushq %rax
    movl $5, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    movl %eax, -8(%rbp)
    movl -8(%rbp), %eax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_add_five, .-runa_function_add_five

    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl $10, %eax
    pushq %rax
    popq %rax
    movl %eax, %edi
    call runa_function_add_five
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
