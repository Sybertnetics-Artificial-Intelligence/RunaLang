    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl runa_function_test_builtin
    .type runa_function_test_builtin, @function
runa_function_test_builtin:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl %edi, -4(%rbp)
    movq -4(%rbp), %rax
    movq %rax, %rdi
    movq $0, %rax
    call strlen@PLT
    movq %rax, -12(%rbp)
    movq -12(%rbp), %rax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_test_builtin, .-runa_function_test_builtin

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
    leaq .LS1(%rip), %rax
    pushq %rax
    popq %rax
    movl %eax, %edi
    call runa_function_test_builtin
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    leaq .LS2(%rip), %rax
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
    .string "Testing builtin in function context"
.LS1:
    .string "Hello"
.LS2:
    .string "Builtin context test complete"
