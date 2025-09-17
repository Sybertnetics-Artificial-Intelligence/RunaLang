    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl runa_function_test_func
    .type runa_function_test_func, @function
runa_function_test_func:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl %edi, -4(%rbp)
    movq -4(%rbp), %rax
    pushq %rax
    movl $10, %eax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    movq %rax, -12(%rbp)
    movq -12(%rbp), %rax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_test_func, .-runa_function_test_func

    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    leaq .LS0(%rip), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $5, %eax
    pushq %rax
    popq %rax
    movl %eax, %edi
    call runa_function_test_func
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    leaq .LS1(%rip), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main

    .section .rodata
.LS0:
    .string "Testing context fix"
.LS1:
    .string "Context test complete"
