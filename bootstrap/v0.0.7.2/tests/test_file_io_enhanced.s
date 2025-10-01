.section .rodata
.STR0:
    .string "Testing Enhanced File I/O Operations\n"
.STR1:
    .string "\n=== Testing file_exists ==="
.STR2:
    .string "test_output.txt"
.STR3:
    .string "\nChecking if test_output.txt exists: "
.STR4:
    .string "exists\n"
.STR5:
    .string "does not exist\n"
.STR6:
    .string "\n=== Testing file_open for writing ==="
.STR7:
    .string "w"
.STR8:
    .string "\nError: Could not open file for writing\n"
.STR9:
    .string "\nOpened file for writing, handle: "
.STR10:
    .string "\n"
.STR11:
    .string "\n=== Testing file_write_line ==="
.STR12:
    .string "First line of text"
.STR13:
    .string "\nError writing line 1\n"
.STR14:
    .string "Second line of text"
.STR15:
    .string "\nError writing line 2\n"
.STR16:
    .string "Third line of text"
.STR17:
    .string "\nError writing line 3\n"
.STR18:
    .string "\nWrote 3 lines to file\n"
.STR19:
    .string "\n=== Testing file_close ==="
.STR20:
    .string "\nError closing file\n"
.STR21:
    .string "\nClosed file successfully\n"
.STR22:
    .string "\n=== Testing file_size ==="
.STR23:
    .string "\nFile size: "
.STR24:
    .string " bytes\n"
.STR25:
    .string "\n=== Testing file_open for reading ==="
.STR26:
    .string "r"
.STR27:
    .string "\nError: Could not open file for reading\n"
.STR28:
    .string "\nOpened file for reading\n"
.STR29:
    .string "\n=== Testing file_read_line ==="
.STR30:
    .string "\nLine 1: "
.STR31:
    .string "Line 2: "
.STR32:
    .string "\n=== Testing file_tell ==="
.STR33:
    .string "\nCurrent file position: "
.STR34:
    .string "\n=== Testing file_seek ==="
.STR35:
    .string "\nSeeked to beginning of file\n"
.STR36:
    .string "First line again: "
.STR37:
    .string "\n=== Testing file_eof ==="
.STR38:
    .string "Read: "
.STR39:
    .string "Reached end of file\n"
.STR40:
    .string "\n=== Testing file_open for append ==="
.STR41:
    .string "a"
.STR42:
    .string "\nError: Could not open file for append\n"
.STR43:
    .string "Fourth line appended"
.STR44:
    .string "\nAppended a line to the file\n"
.STR45:
    .string "\n=== Testing file_delete ==="
.STR46:
    .string "temp_test.txt"
.STR47:
    .string "Temporary file content"
.STR48:
    .string "\nCreated temp file, now deleting..."
.STR49:
    .string " deleted successfully\n"
.STR50:
    .string " failed to delete\n"
.STR51:
    .string "Verified: temp file no longer exists\n"
.STR52:
    .string "Error: temp file still exists\n"
.STR53:
    .string "\n=== All Enhanced File I/O Tests Complete ===\n"

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
    subq $96, %rsp
           
    leaq .STR0(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR1(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR2(%rip), %rax
    movq %rax, -24(%rbp)
    leaq .STR3(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_exists@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    leaq .STR4(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L2
.L1:
    leaq .STR5(%rip), %rax
    movq %rax, %rdi
    call print_string
.L2:
    leaq .STR6(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR7(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_open@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    leaq .STR8(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    leaq .STR9(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR11(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR12(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_write_line@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR13(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L22
.L21:
.L22:
    leaq .STR14(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_write_line@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    leaq .STR15(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L32
.L31:
.L32:
    leaq .STR16(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_write_line@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    leaq .STR17(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L42
.L41:
.L42:
    leaq .STR18(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR19(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_close@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    leaq .STR20(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L52
.L51:
.L52:
    leaq .STR21(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR22(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_size@PLT
    movq %rax, -48(%rbp)
    leaq .STR23(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -48(%rbp), %rax
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
    leaq .STR26(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_open@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    leaq .STR27(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
.L62:
    leaq .STR28(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR29(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_read_line@PLT
    movq %rax, -56(%rbp)
    leaq .STR30(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -56(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_read_line@PLT
    movq %rax, -64(%rbp)
    leaq .STR31(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -64(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR32(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_tell@PLT
    movq %rax, -72(%rbp)
    leaq .STR33(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, %rdi
    call print_string
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR34(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call runtime_file_seek@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    leaq .STR35(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L72
.L71:
.L72:
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_read_line@PLT
    movq %rax, -80(%rbp)
    leaq .STR36(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -80(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR37(%rip), %rax
    movq %rax, %rdi
    call print_string
.L81:
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_eof@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L82
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_read_line@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    leaq .STR38(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -88(%rbp), %rax
    movq %rax, %rdi
    call print_integer
    leaq .STR10(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L92
.L91:
.L92:
    jmp .L81
.L82:
    leaq .STR39(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_close@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR40(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_open@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    leaq .STR42(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
.L102:
    leaq .STR43(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_write_line@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR44(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_close@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR45(%rip), %rax
    movq %rax, %rdi
    call print_string
    leaq .STR46(%rip), %rax
    movq %rax, -96(%rbp)
    leaq .STR7(%rip), %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_open@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR47(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call runtime_file_write_line@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_close@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    leaq .STR48(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_delete@PLT
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    leaq .STR49(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L112
.L111:
    leaq .STR50(%rip), %rax
    movq %rax, %rdi
    call print_string
.L112:
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_file_exists@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    leaq .STR51(%rip), %rax
    movq %rax, %rdi
    call print_string
    jmp .L122
.L121:
    leaq .STR52(%rip), %rax
    movq %rax, %rdi
    call print_string
.L122:
    leaq .STR53(%rip), %rax
    movq %rax, %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack,"",@progbits
