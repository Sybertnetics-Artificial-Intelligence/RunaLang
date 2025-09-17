    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl runa_function_test_char_at_only
    .type runa_function_test_char_at_only, @function
runa_function_test_char_at_only:
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
    movl %eax, %edx
    movl $1, %eax
    movl %eax, %ecx
    testl %ecx, %ecx
    js .done_char_at_0
    cmpl %edx, %ecx
    jl .safe_char_at_0
    movl $-1, %eax
    jmp .done_char_at_0
.safe_char_at_0:
    popq %rax
    addq %rcx, %rax
    movzbl (%rax), %eax
.done_char_at_0:
    addq $8, %rsp
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_test_char_at_only, .-runa_function_test_char_at_only

    .globl runa_function_test_to_string_only
    .type runa_function_test_to_string_only, @function
runa_function_test_to_string_only:
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

    # --- ToString: sprintf Call ---
    movq -16(%rbp), %rdi
    leaq .LC2(%rip), %rsi
    movl -8(%rbp), %edx
    movq $0, %rax
    call sprintf@PLT

    # --- ToString: Return buffer pointer ---
    movq -16(%rbp), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_test_to_string_only, .-runa_function_test_to_string_only

    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    call runa_function_test_char_at_only
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    call runa_function_test_to_string_only
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT

    movl $0, %eax
    leave
    ret

    .size main, .-main

    .section .rodata
.LS0:
    .string "hello"
