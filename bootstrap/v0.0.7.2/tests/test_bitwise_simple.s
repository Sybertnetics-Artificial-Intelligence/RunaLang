.section .rodata
.STR0:
    .string "Simple Bitwise Test\n"
.STR1:
    .string "12 bit_and 10: "
.STR2:
    .string "\n"
.STR3:
    .string "12 bit_or 10: "
.STR4:
    .string "12 bit_xor 10: "
.STR5:
    .string "5 bit_shift_left by 2: "
.STR6:
    .string "20 bit_shift_right by 2: "

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
    subq $16, %rsp
           
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $12, %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    andq %rbx, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $12, %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    orq %rbx, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $12, %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    xorq %rbx, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $5, %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    movq %rax, %rcx
    movq %rbx, %rax
    salq %cl, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $20, %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    movq %rax, %rcx
    movq %rbx, %rax
    sarq %cl, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack,"",@progbits
