    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl runa_function_add_numbers
    .type runa_function_add_numbers, @function
runa_function_add_numbers:
    pushq %rbp
    movq %rsp, %rbp
    subq $128, %rsp
    movl %edi, -8(%rbp)
    movl %esi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_add_numbers, .-runa_function_add_numbers

    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl $5, %eax
    pushq %rax
    movl $7, %eax
    pushq %rax
    popq %rax
    movq %rax, %rsi
    popq %rax
    movq %rax, %rdi
    call runa_function_add_numbers
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main
