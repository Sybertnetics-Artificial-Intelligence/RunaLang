    .section .rodata
.LC0:
    .string "%d\n"

    .text
    .globl runa_function_get_number
    .type runa_function_get_number, @function
runa_function_get_number:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl $42, %eax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_get_number, .-runa_function_get_number

    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    call runa_function_get_number
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
