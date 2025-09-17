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
    movl $5, %eax
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
    leaq .LS1(%rip), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    leaq .LS2(%rip), %rax
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
    # Store string_ptr in its stack slot: -8(%rbp)
    movq %rax, -8(%rbp)
    movl $0, %eax
    # Store start_index in its stack slot: -16(%rbp)
    movl %eax, -16(%rbp)
    movl $5, %eax
    # Store substring_length in its stack slot: -24(%rbp)
    movl %eax, -24(%rbp)

    # --- Substring: Get total string length ---
    movq -8(%rbp), %rdi
    call strlen@PLT
    # Store total_length in its stack slot: -32(%rbp)
    movl %eax, -32(%rbp)

    # --- Substring: Bounds checking ---
    movl -16(%rbp), %eax
    cmpl $0, %eax
    jl .substring_bounds_error_1
    cmpl -32(%rbp), %eax
    jge .substring_bounds_error_1
    movl -24(%rbp), %eax
    cmpl $0, %eax
    jle .substring_bounds_error_1
    movl -16(%rbp), %eax
    addl -24(%rbp), %eax
    cmpl -32(%rbp), %eax
    jg .substring_bounds_error_1

.substring_safe_1:
    # --- Substring: Allocate memory ---
    movl -24(%rbp), %edi
    addl $1, %edi
    movslq %edi, %rdi
    call malloc@PLT
    # Store buffer_ptr in its stack slot: -40(%rbp)
    movq %rax, -40(%rbp)

    # --- Substring: Copy data ---
    movq -40(%rbp), %rdi
    movq -8(%rbp), %rsi
    movslq -16(%rbp), %rax
    addq %rax, %rsi
    movslq -24(%rbp), %rdx
    call memcpy@PLT

    # --- Substring: Add null terminator ---
    movq -40(%rbp), %rax
    movslq -24(%rbp), %rdx
    movb $0, (%rax,%rdx,1)

    # --- Substring: Return result ---
    movq -40(%rbp), %rax
    jmp .substring_end_1
.substring_bounds_error_1:
    movq $0, %rax
.substring_end_1:
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    leaq .LS3(%rip), %rax
    # Store str2_ptr in its stack slot: -16(%rbp)
    movq %rax, -16(%rbp)
    leaq .LS4(%rip), %rax
    # Store str1_ptr in its stack slot: -8(%rbp)
    movq %rax, -8(%rbp)

    # --- Concat: Get length of str1 ---
    movq -8(%rbp), %rdi
    call strlen@PLT
    # Store len1 in its stack slot: -24(%rbp)
    movq %rax, -24(%rbp)

    # --- Concat: Get length of str2 ---
    movq -16(%rbp), %rdi
    call strlen@PLT
    # Store len2 in its stack slot: -32(%rbp)
    movq %rax, -32(%rbp)

    # --- Concat: Allocate new buffer ---
    movq -24(%rbp), %rax
    addq -32(%rbp), %rax
    # Store total_len in its stack slot: -40(%rbp)
    movq %rax, -40(%rbp)
    incq %rax
    movq %rax, %rdi
    call malloc@PLT
    # Store new_buffer_ptr in its stack slot: -48(%rbp)
    movq %rax, -48(%rbp)

    # --- Concat: Copy str1 ---
    movq -48(%rbp), %rdi
    movq -8(%rbp), %rsi
    movq -24(%rbp), %rdx
    call memcpy@PLT

    # --- Concat: Copy str2 ---
    movq -48(%rbp), %rdi
    addq -24(%rbp), %rdi
    movq -16(%rbp), %rsi
    movq -32(%rbp), %rdx
    call memcpy@PLT

    # --- Concat: Add null terminator ---
    movq -48(%rbp), %rax
    addq -40(%rbp), %rax
    movb $0, (%rax)

    # --- Concat: Set return value ---
    movq -48(%rbp), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $42, %eax
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
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    leaq .LS5(%rip), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $10, %eax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movl $10, %eax
    movl %eax, %ecx
    popq %rax
    cmpl %ecx, %eax
    sete %al
    movzbl %al, %eax
    testl %eax, %eax
    je .L_else_2
    leaq .LS6(%rip), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    jmp .L_end_2
.L_else_2:
.L_end_2:
    leaq .LS7(%rip), %rax
    movq %rax, %rsi
    leaq .LC1(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    movl $10, %eax
    pushq %rax
    popq %rax
    movl %eax, %edi
    call runa_function_test_func
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movl %eax, %esi
    leaq .LC0(%rip), %rdi
    movl $0, %eax
    call printf@PLT
    leaq .LS8(%rip), %rax
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
    .string "=== Phase 6: Basic Validation ==="
.LS1:
    .string "Test 1: Basic String Operations"
.LS2:
    .string "Hello World"
.LS3:
    .string " World"
.LS4:
    .string "Hello"
.LS5:
    .string "Test 2: Control Flow"
.LS6:
    .string "Control flow works"
.LS7:
    .string "Test 3: Function Integration"
.LS8:
    .string "=== Basic Validation Complete ==="
