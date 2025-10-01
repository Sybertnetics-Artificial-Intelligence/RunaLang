.section .rodata
.STR0:
    .string "Testing Math Operations\n"
.STR1:
    .string "\n=== Testing abs ==="
.STR2:
    .string "\nabs(-42): "
.STR3:
    .string "\nabs(42): "
.STR4:
    .string "\n\n=== Testing min and max ==="
.STR5:
    .string "\nmin(10, 20): "
.STR6:
    .string "\nmax(10, 20): "
.STR7:
    .string "\n\n=== Testing pow ==="
.STR8:
    .string "\npow(2, 8): "
.STR9:
    .string "\npow(3, 4): "
.STR10:
    .string "\npow(10, 3): "
.STR11:
    .string "\n\n=== Testing sqrt ==="
.STR12:
    .string "\nsqrt(144): "
.STR13:
    .string "\nsqrt(100): "
.STR14:
    .string "\nsqrt(25): "
.STR15:
    .string "\n\n=== Testing trigonometric functions ==="
.STR16:
    .string "\nsin(0 degrees): "
.STR17:
    .string "\nsin(90 degrees): "
.STR18:
    .string "\ncos(0 degrees): "
.STR19:
    .string "\ncos(90 degrees): "
.STR20:
    .string "\ntan(45 degrees): "
.STR21:
    .string "\n\n=== Testing random ==="
.STR22:
    .string "\nrandom(): "
.STR23:
    .string "\nrandom() again: "
.STR24:
    .string "\n\n=== Testing exp and log ==="
.STR25:
    .string "\nexp(0): "
.STR26:
    .string "\nexp(1): "
.STR27:
    .string "\nexp(2): "
.STR28:
    .string "\nlog(1): "
.STR29:
    .string "\nlog(10): "
.STR30:
    .string "\n\n=== Testing floor and ceil ==="
.STR31:
    .string "\nfloor(42): "
.STR32:
    .string "\nceil(42): "
.STR33:
    .string "\n\n=== All Math Tests Complete ===\n"

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
    .string "\n"

.text
.globl main

.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    subq $48, %rsp
           
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_abs@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $42, %rax
    pushq %rax
    popq %rdi
    call runtime_abs@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $20, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_min@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $20, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_max@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $8, %rax
    pushq %rax
    movq $2, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_pow@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $4, %rax
    pushq %rax
    movq $3, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_pow@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $3, %rax
    pushq %rax
    movq $10, %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_pow@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $144, %rax
    pushq %rax
    popq %rdi
    call runtime_sqrt@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $100, %rax
    pushq %rax
    popq %rdi
    call runtime_sqrt@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $25, %rax
    pushq %rax
    popq %rdi
    call runtime_sqrt@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR16(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    pushq %rax
    popq %rdi
    call runtime_sin@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $90, %rax
    pushq %rax
    popq %rdi
    call runtime_sin@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR18(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    pushq %rax
    popq %rdi
    call runtime_cos@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR19(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $90, %rax
    pushq %rax
    popq %rdi
    call runtime_cos@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR20(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $45, %rax
    pushq %rax
    popq %rdi
    call runtime_tan@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR21(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR22(%rip), %rax
    movq %rax, %rdi
    call print_string
    call runtime_random@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR23(%rip), %rax
    movq %rax, %rdi
    call print_string
    call runtime_random@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR24(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR25(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    pushq %rax
    popq %rdi
    call runtime_exp@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR26(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call runtime_exp@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR27(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $2, %rax
    pushq %rax
    popq %rdi
    call runtime_exp@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR28(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call runtime_log@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR29(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $10, %rax
    pushq %rax
    popq %rdi
    call runtime_log@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR30(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR31(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $42, %rax
    pushq %rax
    popq %rdi
    call runtime_floor@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR32(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $42, %rax
    pushq %rax
    popq %rdi
    call runtime_ceil@PLT
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR33(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack,"",@progbits
