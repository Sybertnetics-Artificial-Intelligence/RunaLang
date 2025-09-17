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
    movq %rax, %rdi
    call strlen@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %edx
    movl $0, %eax
    movl %eax, %ecx
    cmpl $0, %ecx
    jl .bounds_error_char_at_0
    cmpl %edx, %ecx
    jge .bounds_error_char_at_0
.safe_char_at_0:
    popq %rax
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rax
    movzbl (%rax), %eax
    jmp .char_at_end_0
.bounds_error_char_at_0:
    addq $16, %rsp
    movl $-1, %eax
.char_at_end_0:
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %edx
    movl $1, %eax
    movl %eax, %ecx
    cmpl $0, %ecx
    jl .bounds_error_char_at_1
    cmpl %edx, %ecx
    jge .bounds_error_char_at_1
.safe_char_at_1:
    popq %rax
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rax
    movzbl (%rax), %eax
    jmp .char_at_end_1
.bounds_error_char_at_1:
    addq $16, %rsp
    movl $-1, %eax
.char_at_end_1:
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movq -8(%rbp), %rax
    pushq %rax
    pushq %rax
    movq %rax, %rdi
    call strlen@PLT
    movl %eax, %r8d
    movl $0, %eax
    movl %eax, %ecx
    movl $2, %eax
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
    movl %edx, %r11d
    popq %rsi
    addq $8, %rsp
    movslq %ecx, %rcx
    addq %rcx, %rsi
    movq %r10, %rdi
    movslq %edx, %rdx
    call memcpy@PLT
    movslq %r11d, %r11
    movb $0, (%r10,%r11,1)
    movq %r10, %rax
    jmp .substring_end_2
.substring_bounds_error_2:
    addq $16, %rsp
    movq $0, %rax
.substring_end_2:
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
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
    .string "Hello"
