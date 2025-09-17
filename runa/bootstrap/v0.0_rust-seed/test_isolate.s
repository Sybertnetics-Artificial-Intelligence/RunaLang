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

    .globl runa_function_test_concat_only
    .type runa_function_test_concat_only, @function
runa_function_test_concat_only:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    leaq .LS1(%rip), %rax
    movq %rax, -8(%rbp)
    leaq .LS2(%rip), %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    movq %rax, %rsi
    popq %rdi
    pushq %rdi
    pushq %rsi
    call strlen@PLT
    pushq %rax
    movq -8(%rsp), %rdi
    call strlen@PLT
    popq %rcx
    addq %rcx, %rax
    incq %rax
    movq %rax, %rdi
    call malloc@PLT
    popq %rsi
    popq %rdi
    pushq %rax
    movq %rax, %rdx
    call strcpy@PLT
    popq %rax
    pushq %rax
    movq %rax, %rdi
    call strcat@PLT
    popq %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_test_concat_only, .-runa_function_test_concat_only

    .globl runa_function_test_substring_only
    .type runa_function_test_substring_only, @function
runa_function_test_substring_only:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    leaq .LS3(%rip), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movl $0, %eax
    pushq %rax
    movl $5, %eax
    movl %eax, %edx
    popq %rsi
    popq %rdi
    incl %edx
    movl %edx, %edi
    call malloc@PLT
    pushq %rax
    popq %rax
    popq %rsi
    popq %rdi
    pushq %rax
    pushq %rsi
    pushq %rdi
    addq %rsi, %rdi
    movq %rax, %rsi
    movl %edx, %ecx
    decl %ecx
    call memcpy@PLT
    popq %rdi
    popq %rsi
    popq %rax
    movl %edx, %ecx
    decl %ecx
    addq %rcx, %rax
    movb $0, (%rax)
    subq %rcx, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    leave
    ret
    movl $0, %eax
    leave
    ret
    .size runa_function_test_substring_only, .-runa_function_test_substring_only

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
    call runa_function_test_concat_only
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    call runa_function_test_substring_only
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
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
.LS1:
    .string "hello"
.LS2:
    .string " world"
.LS3:
    .string "hello world"
