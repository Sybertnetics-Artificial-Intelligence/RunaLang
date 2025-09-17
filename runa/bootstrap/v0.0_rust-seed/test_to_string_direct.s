    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movl $42, %eax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    # Store integer_value in its stack slot: -8(%rbp)
    movl %eax, -8(%rbp)

    # --- ToString: Allocate buffer ---
    movl $12, %edi
    call malloc@PLT
    # Store buffer_ptr in its stack slot: -16(%rbp)
    movq %rax, -16(%rbp)

    # --- ToString: Convert with sprintf ---
    movq -16(%rbp), %rdi
    leaq .LC2(%rip), %rsi
    movl -8(%rbp), %edx
    call sprintf@PLT

    # --- ToString: Return result ---
    movq -16(%rbp), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main
