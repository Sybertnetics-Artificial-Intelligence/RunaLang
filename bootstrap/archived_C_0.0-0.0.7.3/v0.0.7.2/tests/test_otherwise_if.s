.section .rodata
.STR0:
    .string "Testing Otherwise If (elif chains)\n"
.STR1:
    .string "x is 1\n"
.STR2:
    .string "x is 2\n"
.STR3:
    .string "x is 5 - CORRECT!\n"
.STR4:
    .string "x is something else\n"
.STR5:
    .string "Grade calculation for score: "
.STR6:
    .string "\n"
.STR7:
    .string "Grade: A\n"
.STR8:
    .string "Grade: B - CORRECT!\n"
.STR9:
    .string "Grade: D\n"
.STR10:
    .string "Grade: F\n"
.STR11:
    .string "Freezing\n"
.STR12:
    .string "Cold\n"
.STR13:
    .string "Warm - CORRECT!\n"
.STR14:
    .string "All elif tests completed\n"

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
    movq $5, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L2
.L1:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    leaq .STR2(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L12
.L11:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L22
.L21:
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
.L22:
.L12:
.L2:
    movq $85, %rax
    movq %rax, -32(%rbp)
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    movq $90, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    leaq .STR7(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L32
.L31:
    movq -32(%rbp), %rax
    pushq %rax
    movq $80, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L42
.L41:
    movq -32(%rbp), %rax
    pushq %rax
    movq $60, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L52
.L51:
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
.L52:
.L42:
.L32:
    movq $25, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L62
.L61:
    movq -40(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    leaq .STR12(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L72
.L71:
    movq -40(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L82
.L81:
.L82:
.L72:
.L62:
    leaq .STR14(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack,"",@progbits
