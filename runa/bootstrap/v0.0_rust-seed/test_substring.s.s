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
    leaq .LS0(%rip), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %r8d
    movl $0, %eax
    movl %eax, %ecx
    movl $5, %eax
    movl %eax, %edx
    cmpl $0, %ecx
    jl .substring_bounds_error_0
    cmpl %r8d, %ecx
    jge .substring_bounds_error_0
    cmpl $0, %edx
    jle .substring_bounds_error_0
    movl %ecx, %r9d
    addl %edx, %r9d
    cmpl %r8d, %r9d
    jg .substring_bounds_error_0
.substring_safe_0:
    movl %edx, %edi
    addl $1, %edi
    movslq %edi, %rdi
    call malloc@PLT
    movq %rax, %r10
    popq %rsi
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rsi
    movq %r10, %rdi
    movslq %edx, %rdx
    call memcpy@PLT
    movq %r10, %rax
    movslq %edx, %rdx
    movb $0, (%rax,%rdx,1)
    movq %r10, %rax
    jmp .substring_end_0
.substring_bounds_error_0:
    addq $16, %rsp
    movq $0, %rax
.substring_end_0:
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movl %eax, %esi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %r8d
    movl $7, %eax
    movl %eax, %ecx
    movl $5, %eax
    movl %eax, %edx
    cmpl $0, %ecx
    jl .substring_bounds_error_1
    cmpl %r8d, %ecx
    jge .substring_bounds_error_1
    cmpl $0, %edx
    jle .substring_bounds_error_1
    movl %ecx, %r9d
    addl %edx, %r9d
    cmpl %r8d, %r9d
    jg .substring_bounds_error_1
.substring_safe_1:
    movl %edx, %edi
    addl $1, %edi
    movslq %edi, %rdi
    call malloc@PLT
    movq %rax, %r10
    popq %rsi
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rsi
    movq %r10, %rdi
    movslq %edx, %rdx
    call memcpy@PLT
    movq %r10, %rax
    movslq %edx, %rdx
    movb $0, (%rax,%rdx,1)
    movq %r10, %rax
    jmp .substring_end_1
.substring_bounds_error_1:
    addq $16, %rsp
    movq $0, %rax
.substring_end_1:
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    movl %eax, %esi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq %rax, -40(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %r8d
    movl $1, %eax
    movl %eax, %ecx
    movl $4, %eax
    movl %eax, %edx
    cmpl $0, %ecx
    jl .substring_bounds_error_2
    cmpl %r8d, %ecx
    jge .substring_bounds_error_2
    cmpl $0, %edx
    jle .substring_bounds_error_2
    movl %ecx, %r9d
    addl %edx, %r9d
    cmpl %r8d, %r9d
    jg .substring_bounds_error_2
.substring_safe_2:
    movl %edx, %edi
    addl $1, %edi
    movslq %edi, %rdi
    call malloc@PLT
    movq %rax, %r10
    popq %rsi
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rsi
    movq %r10, %rdi
    movslq %edx, %rdx
    call memcpy@PLT
    movq %r10, %rax
    movslq %edx, %rdx
    movb $0, (%rax,%rdx,1)
    movq %r10, %rax
    jmp .substring_end_2
.substring_bounds_error_2:
    addq $16, %rsp
    movq $0, %rax
.substring_end_2:
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    movl %eax, %esi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq %rax, -56(%rbp)

    movl $0, %eax
    leave
    ret

    .size main, .-main

    .section .rodata
.LS0:
    .string "Hello, World!"
