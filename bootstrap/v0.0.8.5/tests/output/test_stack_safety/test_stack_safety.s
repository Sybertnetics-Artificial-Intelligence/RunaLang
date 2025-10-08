.text
print_string:
    pushq %rbp
    movq %rsp, %rbp

    # Calculate string length
    movq %rdi, %rsi  # Save string pointer
    movq %rdi, %rcx  # Counter for strlen
    xorq %rax, %rax  # Length accumulator
.strlen_loop:
    cmpb $0, (%rcx)
    je .strlen_done
    incq %rcx
    incq %rax
    jmp .strlen_loop
.strlen_done:

    # Call write syscall (sys_write = 1)
    movq $1, %rdi     # fd = stdout
    movq %rsi, %rsi   # buf = string pointer (already in rsi)
    movq %rax, %rdx   # count = string length
    movq $1, %rax     # syscall number for write
    syscall

    # Print newline
    movq $1, %rdi     # fd = stdout
    leaq .newline(%rip), %rsi  # newline string
    movq $1, %rdx     # count = 1
    movq $1, %rax     # syscall number for write
    syscall

    popq %rbp
    ret


print_integer:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp  # Space for string buffer (20 digits + null)

    # Convert integer to string
    movq %rdi, %rax  # integer value
    leaq -32(%rbp), %rsi  # buffer pointer
    addq $19, %rsi  # point to end of buffer (for reverse building)
    movb $0, (%rsi)  # null terminator
    decq %rsi

    # Handle zero case
    testq %rax, %rax
    jnz .convert_loop
    movb $48, (%rsi)  # '0' character
    jmp .convert_done

.convert_loop:
    testq %rax, %rax
    jz .convert_done
    movq %rax, %rcx
    movq $10, %rbx
    xorq %rdx, %rdx
    divq %rbx  # %rax = quotient, %rdx = remainder
    addq $48, %rdx  # convert remainder to ASCII
    movb %dl, (%rsi)  # store digit
    decq %rsi
    jmp .convert_loop

.convert_done:
    incq %rsi  # point to first character

    # Calculate string length
    movq %rsi, %rcx  # Counter for strlen
    xorq %rax, %rax  # Length accumulator
.int_strlen_loop:
    cmpb $0, (%rcx)
    je .int_strlen_done
    incq %rcx
    incq %rax
    jmp .int_strlen_loop
.int_strlen_done:

    # Call write syscall (sys_write = 1)
    movq $1, %rdi     # fd = stdout
    # %rsi already points to string
    movq %rax, %rdx   # count = string length
    movq $1, %rax     # syscall number for write
    syscall

    # Print newline
    movq $1, %rdi     # fd = stdout
    leaq .newline(%rip), %rsi  # newline string
    movq $1, %rdx     # count = 1
    movq $1, %rax     # syscall number for write
    syscall

    movq %rbp, %rsp
    popq %rbp
    ret


.section .rodata
.newline:
    .byte 10  # newline character
.STR0:    .string "=== STACK SAFETY TEST SUITE ===\n"
.STR1:    .string "\n"
.STR2:    .string "TEST 1: Direct Recursion (factorial)\n"
.STR3:    .string "factorial(5) = "
.STR4:    .string "\nTEST 2: Tail Recursion (factorial_tail)\n"
.STR5:    .string "factorial_tail(5, 1) = "
.STR6:    .string "\nTEST 3: Mutual Recursion (is_even/is_odd)\n"
.STR7:    .string "is_even(10) = "
.STR8:    .string "is_odd(10) = "
.STR9:    .string "\nTEST 4: Deep Recursion\n"
.STR10:    .string "deep_recursion(100) = "
.STR11:    .string "\nTEST 5: Non-Recursive Function\n"
.STR12:    .string "simple_add(10, 20) = "
.STR13:    .string "\nTEST 6: Indirect Recursion (3-way)\n"
.STR14:    .string "func_a(5) = "
.STR15:    .string "\nTEST 7: Fibonacci (Multiple Recursive Calls)\n"
.STR16:    .string "fibonacci(8) = "
.STR17:    .string "\nTEST 8: Nested Function Calls (Non-Recursive)\n"
.STR18:    .string "main_func(5) = "
.STR19:    .string "\nTEST 9: Conditional Recursion\n"
.STR20:    .string "conditional_recursion(10, 1) = "
.STR21:    .string "\nTEST 10: Ackermann Function\n"
.STR22:    .string "ackermann(2, 2) = "
.STR23:    .string "\n=== ALL TESTS COMPLETE ===\n"
.STR24:    .string "\nExpected Compiler Warnings:\n"
.STR25:    .string "- factorial: direct recursion\n"
.STR26:    .string "- factorial_tail: direct recursion (tail-recursive)\n"
.STR27:    .string "- is_even/is_odd: mutual recursion\n"
.STR28:    .string "- deep_recursion: direct recursion\n"
.STR29:    .string "- func_a/func_b/func_c: mutual recursion (3-way)\n"
.STR30:    .string "- fibonacci: direct recursion\n"
.STR31:    .string "- conditional_recursion: direct recursion\n"
.STR32:    .string "- ackermann: direct recursion\n"
.STR33:    .string "\nNO warnings expected for:\n"
.STR34:    .string "- simple_add\n"
.STR35:    .string "- helper_one/helper_two/main_func\n"
.text


.globl factorial
factorial:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2
.L1:
.L2:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call factorial
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl factorial_tail
factorial_tail:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call factorial_tail
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_even
is_even:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call is_odd
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_odd
is_odd:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
.L32:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call is_even
    movq %rbp, %rsp
    popq %rbp
    ret


.globl deep_recursion
deep_recursion:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call deep_recursion
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    addq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl simple_add
simple_add:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    addq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl func_a
func_a:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call func_b
    movq %rbp, %rsp
    popq %rbp
    ret


.globl func_b
func_b:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
.L62:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call func_c
    movq %rbp, %rsp
    popq %rbp
    ret


.globl func_c
func_c:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call func_a
    movq %rbp, %rsp
    popq %rbp
    ret


.globl fibonacci
fibonacci:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    movq -8(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    call fibonacci
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    subq $2, %rax
    pushq %rax
    popq %rdi
    call fibonacci
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    addq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl helper_one
helper_one:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl helper_two
helper_two:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call helper_one
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    addq $10, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl main_func
main_func:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call helper_two
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl conditional_recursion
conditional_recursion:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
.L92:
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call conditional_recursion
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
.L102:
    movq -8(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl ackermann
ackermann:
    pushq %rbp
    movq %rsp, %rbp
    # Stack overflow protection
    movq %rsp, %rax
    subq $16384, %rax  # Check if we have 16KB stack space
    cmpq $0x100000, %rax  # Compare against 1MB limit
    jb .stack_overflow_panic
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq -16(%rbp), %rax
    addq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L112
.L111:
.L112:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call ackermann
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L122
.L121:
.L122:
    movq -16(%rbp), %rax
    subq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call ackermann
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    subq $1, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call ackermann
    movq %rbp, %rsp
    popq %rbp
    ret
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    leaq .STR0(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR2(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $5, %rax
    pushq %rax
    popq %rdi
    call factorial
    movq %rax, -8(%rbp)
    leaq .STR3(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR4(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    movq $5, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call factorial_tail
    movq %rax, -16(%rbp)
    leaq .STR5(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR6(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $10, %rax
    pushq %rax
    popq %rdi
    call is_even
    movq %rax, -24(%rbp)
    movq $10, %rax
    pushq %rax
    popq %rdi
    call is_odd
    movq %rax, -32(%rbp)
    leaq .STR7(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR8(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $100, %rax
    pushq %rax
    popq %rdi
    call deep_recursion
    movq %rax, -40(%rbp)
    leaq .STR10(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR11(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $20, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call simple_add
    movq %rax, -48(%rbp)
    leaq .STR12(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR13(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $5, %rax
    pushq %rax
    popq %rdi
    call func_a
    movq %rax, -56(%rbp)
    leaq .STR14(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR15(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $8, %rax
    pushq %rax
    popq %rdi
    call fibonacci
    movq %rax, -64(%rbp)
    leaq .STR16(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $5, %rax
    pushq %rax
    popq %rdi
    call main_func
    movq %rax, -72(%rbp)
    leaq .STR18(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR19(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call conditional_recursion
    movq %rax, -80(%rbp)
    leaq .STR20(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR21(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $2, %rax
    pushq %rax
    movq $2, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call ackermann
    movq %rax, -88(%rbp)
    leaq .STR22(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR23(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR24(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR25(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR27(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR28(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR31(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR32(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR33(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR35(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

# Stack overflow panic handler
.stack_overflow_panic:
    # Print error message
    leaq .stack_overflow_msg(%rip), %rdi
    call print_string@PLT
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.section .rodata
.stack_overflow_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 83,116,97,99,107,32,111,118,101,114,102,108,111,119,32
    .byte 100,101,116,101,99,116,101,100
    .byte 10,0
.text


.null_pointer_error:
    # Print error message for null pointer
    leaq .null_pointer_msg(%rip), %rdi
    call print_string@PLT
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.bounds_error_negative:
    # Print error message for negative index
    leaq .bounds_error_negative_msg(%rip), %rdi
    call print_string@PLT
    # Print the negative index value
    movq %rbx, %rdi  # Index value
    call print_integer@PLT
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.bounds_error_overflow:
    # Save registers that will be clobbered
    pushq %rcx  # Save array size
    pushq %rbx  # Save index
    # Print error message for out-of-bounds index
    leaq .bounds_error_overflow_msg(%rip), %rdi
    call print_string@PLT
    # Print the index value
    popq %rdi  # Restore and use index
    pushq %rdi  # Save again for later
    call print_integer@PLT
    # Print size message
    leaq .bounds_error_size_msg(%rip), %rdi
    call print_string@PLT
    # Print the array size
    movq 8(%rsp), %rdi  # Get saved array size from stack
    call print_integer@PLT
    # Clean up stack
    addq $16, %rsp
    # Exit with error code
    movq $1, %rdi
    call exit_with_code@PLT

.section .rodata
.null_pointer_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 78,117,108,108,32,112,111,105,110,116,101,114,32
    .byte 100,101,114,101,102,101,114,101,110,99,101
    .byte 10,0

.bounds_error_negative_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 65,114,114,97,121,32,105,110,100,101,120,32
    .byte 105,115,32,110,101,103,97,116,105,118,101,58,32
    .byte 0

.bounds_error_overflow_msg:
    .byte 70,65,84,65,76,32,69,82,82,79,82,58,32
    .byte 65,114,114,97,121,32,105,110,100,101,120,32
    .byte 111,117,116,32,111,102,32,98,111,117,110,100,115,58,32
    .byte 0

.bounds_error_size_msg:
    .byte 32,40,97,114,114,97,121,32,115,105,122,101,32,105,115,32
    .byte 41,10,0


.section .note.GNU-stack
