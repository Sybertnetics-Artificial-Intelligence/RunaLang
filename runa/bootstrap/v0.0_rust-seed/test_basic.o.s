    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl runa_function_double
    .type runa_function_double, @function
runa_function_double:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl %edi, -4(%rbp)
    movq -4(%rbp), %rax
    pushq %rax
    movq -4(%rbp), %rax
    movl %eax, %ecx
    popq %rax
    addl %ecx, %eax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_double, .-runa_function_double

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
    movl $42, %eax
    movq %rax, -12(%rbp)
    movq -12(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $5, %eax
    pushq %rax
    popq %rax
    movl %eax, %edi
    call runa_function_double
    movq %rax, -20(%rbp)
    movq -20(%rbp), %rax
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
    .string "Testing v0.0 compiler"
.LS1:
    .string "All basic tests passed"
