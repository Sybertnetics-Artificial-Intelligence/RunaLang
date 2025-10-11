.section .data
.globl ARENA_BASE
ARENA_BASE:    .quad 0
.globl ARENA_USED
ARENA_USED:    .quad 8
.globl ARENA_CAPACITY
ARENA_CAPACITY:    .quad 16
.globl ARENA_STRUCT_SIZE
ARENA_STRUCT_SIZE:    .quad 24

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
.STR0:    .string "[ARENA ERROR] Arena capacity exceeded"
.STR1:    .string ""
.text


.globl arena_create
arena_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $24, %rax  # Load compile-time constant ARENA_STRUCT_SIZE
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax  # Load compile-time constant ARENA_BASE
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant ARENA_USED
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $16, %rax  # Load compile-time constant ARENA_CAPACITY
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_alloc
arena_alloc:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax  # Load compile-time constant ARENA_BASE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax  # Load compile-time constant ARENA_USED
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax  # Load compile-time constant ARENA_CAPACITY
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    movq %rax, %rcx
    popq %rax
    testq %rcx, %rcx
    jz .Lmod_by_zero_0
    cqto
    idivq %rcx
    movq %rdx, %rax
    jmp .Lmod_done_0
.Lmod_by_zero_0:
    movq $0, %rax
.Lmod_done_0:
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $8, %rax
    subq -48(%rbp), %rax
    movq %rax, -56(%rbp)
    movq -16(%rbp), %rax
    addq -56(%rbp), %rax
    movq %rax, -16(%rbp)
    jmp .L12
.L11:
.L12:
    movq -32(%rbp), %rax
    addq -16(%rbp), %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    leaq .STR0(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    movq -24(%rbp), %rax
    addq -32(%rbp), %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant ARENA_USED
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -80(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_get_used
arena_get_used:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $8, %rax  # Load compile-time constant ARENA_USED
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_get_capacity
arena_get_capacity:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $16, %rax  # Load compile-time constant ARENA_CAPACITY
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_reset
arena_reset:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $0, %rax
    pushq %rax
    movq $8, %rax  # Load compile-time constant ARENA_USED
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_destroy
arena_destroy:
    pushq %rbp
    movq %rsp, %rbp
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
    movq $0, %rax  # Load compile-time constant ARENA_BASE
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L42
.L41:
.L42:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_string_duplicate
arena_string_duplicate:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
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
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call arena_alloc
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
.L62:
    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_copy
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl arena_string_concat
arena_string_concat:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call arena_string_duplicate
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call arena_string_duplicate
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    addq -40(%rbp), %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    addq $1, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call arena_alloc
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
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
    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_copy
    movq -64(%rbp), %rax
    addq -32(%rbp), %rax
    movq %rax, -72(%rbp)
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_copy
    movq -64(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_length
string_length:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L101
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
.L102:
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
.L111:    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L112
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq $0, %rax
    movq %rax, -24(%rbp)
    jmp .L122
.L121:
    movq -16(%rbp), %rax
    addq $1, %rax
    movq %rax, -16(%rbp)
.L122:
    jmp .L111
.L112:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_char_at
string_char_at:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L131
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L132
.L131:
.L132:
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_equals
string_equals:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L141
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L152
.L151:
.L152:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L142
.L141:
.L142:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L161
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L162
.L161:
.L162:
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq $1, %rax
    movq %rax, -32(%rbp)
.L171:    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L172
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L182
.L181:
.L182:
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq $0, %rax
    movq %rax, -32(%rbp)
    jmp .L192
.L191:
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -24(%rbp)
.L192:
    jmp .L171
.L172:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_digit
is_digit:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $48, %rax
    movq %rax, -16(%rbp)
    movq $57, %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq -8(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L212
.L211:
.L212:
    jmp .L202
.L201:
.L202:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_alpha
is_alpha:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $65, %rax
    movq %rax, -16(%rbp)
    movq $90, %rax
    movq %rax, -24(%rbp)
    movq $97, %rax
    movq %rax, -32(%rbp)
    movq $122, %rax
    movq %rax, -40(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    movq -8(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L231
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L232
.L231:
.L232:
    jmp .L222
.L221:
.L222:
    movq -8(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    movq -8(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setle %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L251
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L252
.L251:
.L252:
    jmp .L242
.L241:
.L242:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_whitespace
is_whitespace:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $32, %rax
    movq %rax, -16(%rbp)
    movq $9, %rax
    movq %rax, -24(%rbp)
    movq $10, %rax
    movq %rax, -32(%rbp)
    movq $13, %rax
    movq %rax, -40(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L262
.L261:
    movq -8(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L272
.L271:
    movq -8(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L282
.L281:
    movq -8(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L292
.L291:
.L292:
.L282:
.L272:
.L262:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl integer_to_string
integer_to_string:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L301
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq $48, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L302
.L301:
.L302:
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    movq $1, %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    subq -8(%rbp), %rax
    movq %rax, -32(%rbp)
    jmp .L312
.L311:
.L312:
    movq $0, %rax
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    movq %rax, -64(%rbp)
.L321:    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L322
    movq -56(%rbp), %rax
    addq $1, %rax
    movq %rax, -56(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $10, %rax
    movq %rax, %rcx
    popq %rax
    testq %rcx, %rcx
    jz .Ldiv_by_zero_33
    cqto
    idivq %rcx
    jmp .Ldiv_done_33
.Ldiv_by_zero_33:
    movq $0, %rax
.Ldiv_done_33:
    movq %rax, -64(%rbp)
    jmp .L321
.L322:
    movq -56(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L341
    movq -88(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L342
.L341:
.L342:
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -16(%rbp)
    movq -56(%rbp), %rax
    movq %rax, -112(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
    movq -112(%rbp), %rax
    addq $1, %rax
    movq %rax, -112(%rbp)
    jmp .L352
.L351:
.L352:
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -32(%rbp), %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    subq $1, %rax
    movq %rax, -112(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    movq -112(%rbp), %rax
    addq $1, %rax
    movq %rax, -112(%rbp)
    jmp .L362
.L361:
.L362:
.L371:    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L372
    movq -64(%rbp), %rax
    pushq %rax
    movq $10, %rax
    movq %rax, %rcx
    popq %rax
    testq %rcx, %rcx
    jz .Ldiv_by_zero_38
    cqto
    idivq %rcx
    jmp .Ldiv_done_38
.Ldiv_by_zero_38:
    movq $0, %rax
.Ldiv_done_38:
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -160(%rbp)
    movq -64(%rbp), %rax
    subq -160(%rbp), %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    addq $48, %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -112(%rbp), %rax
    subq $1, %rax
    movq %rax, -112(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $10, %rax
    movq %rax, %rcx
    popq %rax
    testq %rcx, %rcx
    jz .Ldiv_by_zero_39
    cqto
    idivq %rcx
    jmp .Ldiv_done_39
.Ldiv_by_zero_39:
    movq $0, %rax
.Ldiv_done_39:
    movq %rax, -64(%rbp)
    jmp .L371
.L372:
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    movq $45, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    jmp .L402
.L401:
.L402:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl bit_not
bit_not:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    addq $1, %rax
    movq %rax, -16(%rbp)
    movq $0, %rax
    subq -16(%rbp), %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl system_write
system_write:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $1, %rax
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call system_call
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_to_integer
string_to_integer:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L411
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L412
.L411:
.L412:
    movq $0, %rax
    movq %rax, -16(%rbp)
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq $45, %rax
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    movq $1, %rax
    movq %rax, -32(%rbp)
    movq $1, %rax
    movq %rax, -24(%rbp)
    jmp .L422
.L421:
.L422:
    movq $1, %rax
    movq %rax, -72(%rbp)
.L431:    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L432
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    movq $0, %rax
    movq %rax, -72(%rbp)
    jmp .L442
.L441:
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L451
    movq -16(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -16(%rbp)
    movq $48, %rax
    movq %rax, -112(%rbp)
    movq -80(%rbp), %rax
    subq -112(%rbp), %rax
    movq %rax, -120(%rbp)
    movq -16(%rbp), %rax
    addq -120(%rbp), %rax
    movq %rax, -16(%rbp)
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -24(%rbp)
    jmp .L452
.L451:
    movq $0, %rax
    movq %rax, -72(%rbp)
.L452:
.L442:
    jmp .L431
.L432:
    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    movq $0, %rax
    subq -16(%rbp), %rax
    movq %rax, -16(%rbp)
    jmp .L462
.L461:
.L462:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl memory_reallocate
memory_reallocate:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L471
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L472
.L471:
.L472:
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_realloc
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_create_with_capacity
string_builder_create_with_capacity:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $24, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L482
.L481:
.L482:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L491
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L492
.L491:
.L492:
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -8(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_create
string_builder_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $256, %rax
    pushq %rax
    popq %rdi
    call string_builder_create_with_capacity
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_destroy
string_builder_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L501
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L502
.L501:
.L502:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_ensure_capacity
string_builder_ensure_capacity:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    addq -16(%rbp), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L511
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq $0, %rax
    movq %rax, -56(%rbp)
.L521:    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L522
    movq -48(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq $1, %rax
    movq %rax, -56(%rbp)
    jmp .L532
.L531:
    movq -48(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
.L532:
    jmp .L521
.L522:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call reallocate
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L541
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L542
.L541:
.L542:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L512
.L511:
.L512:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_append
string_builder_append:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L551
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L552
.L551:
.L552:
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L561
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L562
.L561:
.L562:
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_builder_ensure_capacity
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L572
.L571:
.L572:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_copy_string
    movq -48(%rbp), %rax
    addq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_append_char
string_builder_append_char:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L581
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L582
.L581:
.L582:
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_builder_ensure_capacity
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L592
.L591:
.L592:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_append_int
string_builder_append_int:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_builder_append
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_to_string
string_builder_to_string:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L601
    leaq .STR1(%rip), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L602
.L601:
.L602:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_pointer_to_string
    movq %rax, -24(%rbp)
    movq $1, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_get_string
string_builder_get_string:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L611
    leaq .STR1(%rip), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L612
.L611:
.L612:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_pointer_to_string
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_length
string_builder_length:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L621
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L622
.L621:
.L622:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_builder_clear
string_builder_clear:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L632
.L631:
.L632:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_tokenizer_create
string_tokenizer_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L641
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L642
.L641:
.L642:
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L651
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L652
.L651:
.L652:
    movq $32, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L661
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L662
.L661:
.L662:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L671
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L672
.L671:
.L672:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $1, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_tokenizer_next
string_tokenizer_next:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L681
    leaq .STR1(%rip), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L682
.L681:
.L682:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L691
    leaq .STR1(%rip), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L692
.L691:
.L692:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_pointer_to_string
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq $1, %rax
    movq %rax, -48(%rbp)
.L701:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L702
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq $0, %rax
    movq %rax, -48(%rbp)
    jmp .L712
.L711:
    movq -56(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_contains_char_value
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
    movq $0, %rax
    movq %rax, -48(%rbp)
    jmp .L722
.L721:
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
.L722:
.L712:
    jmp .L701
.L702:
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L731
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR1(%rip), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L732
.L731:
.L732:
    movq -40(%rbp), %rax
    movq %rax, -104(%rbp)
    movq $1, %rax
    movq %rax, -112(%rbp)
.L741:    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L742
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    movq $0, %rax
    movq %rax, -112(%rbp)
    jmp .L752
.L751:
    movq -56(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_contains_char_value
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L761
    movq $0, %rax
    movq %rax, -112(%rbp)
    jmp .L762
.L761:
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
.L762:
.L752:
    jmp .L741
.L742:
    movq -40(%rbp), %rax
    subq -104(%rbp), %rax
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_get_substring
    movq %rax, -168(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L771
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -40(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_pointer_offset
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L772
.L771:
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
.L772:
    movq -168(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_tokenizer_has_next
string_tokenizer_has_next:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L781
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L782
.L781:
.L782:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L791
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L792
.L791:
.L792:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_pointer_to_string
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
    movq $1, %rax
    movq %rax, -48(%rbp)
.L801:    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L802
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L811
    movq $0, %rax
    movq %rax, -48(%rbp)
    jmp .L812
.L811:
    movq -56(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_contains_char_value
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L821
    movq $0, %rax
    movq %rax, -48(%rbp)
    jmp .L822
.L821:
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
.L822:
.L812:
    jmp .L801
.L802:
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L831
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L832
.L831:
.L832:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_tokenizer_destroy
string_tokenizer_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L841
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L851
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L852
.L851:
.L852:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L842
.L841:
.L842:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_array_create
string_array_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq $24, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L861
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L862
.L861:
.L862:
    movq $8, %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L872
.L871:
.L872:
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -16(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -8(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_array_add
string_array_add:
    pushq %rbp
    movq %rsp, %rbp
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
    jz .L881
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L882
.L881:
.L882:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call reallocate
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L901
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L902
.L901:
.L902:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L892
.L891:
.L892:
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    movq %rax, -72(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_array_destroy
string_array_destroy:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L911
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
.L921:    movq -32(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L922
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -32(%rbp), %rax
    addq $1, %rax
    movq %rax, -32(%rbp)
    jmp .L921
.L922:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L912
.L911:
.L912:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_duplicate
string_duplicate:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    addq $1, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L932
.L931:
.L932:
    movq -8(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_copy_string_to_buffer
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_starts_with
string_starts_with:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L942
.L941:
.L942:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_substring@PLT
    movq %rax, -40(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    testq %rax, %rax
    jz .L951
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L952
.L951:
.L952:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_ends_with
string_ends_with:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L962
.L961:
.L962:
    movq -24(%rbp), %rax
    subq -32(%rbp), %rax
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_substring@PLT
    movq %rax, -48(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    testq %rax, %rax
    jz .L971
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L972
.L971:
.L972:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_contains
string_contains:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_find@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L981
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L982
.L981:
.L982:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_is_empty
string_is_empty:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L991
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L992
.L991:
.L992:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_is_whitespace
string_is_whitespace:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1002
.L1001:
.L1002:
    movq $0, %rax
    movq %rax, -24(%rbp)
.L1011:    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1012
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call ascii_value_of@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1021
    movq $1, %rax
    movq %rax, -48(%rbp)
    jmp .L1022
.L1021:
    movq -40(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq $1, %rax
    movq %rax, -48(%rbp)
    jmp .L1032
.L1031:
    movq -40(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1041
    movq $1, %rax
    movq %rax, -48(%rbp)
    jmp .L1042
.L1041:
    movq -40(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    movq $1, %rax
    movq %rax, -48(%rbp)
    jmp .L1052
.L1051:
.L1052:
.L1042:
.L1032:
.L1022:
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1062
.L1061:
.L1062:
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -24(%rbp)
    jmp .L1011
.L1012:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_is_numeric
string_is_numeric:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1072
.L1071:
.L1072:
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call ascii_value_of@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $45, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1081
    movq $1, %rax
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1091
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1092
.L1091:
.L1092:
    jmp .L1082
.L1081:
.L1082:
.L1101:    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1102
    movq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_digit@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1112
.L1111:
.L1112:
    movq -24(%rbp), %rax
    addq $1, %rax
    movq %rax, -24(%rbp)
    jmp .L1101
.L1102:
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_contains_char_value
string_contains_char_value:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
.L1121:    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1122
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call ascii_value_of@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1132
.L1131:
.L1132:
    movq -32(%rbp), %rax
    addq $1, %rax
    movq %rax, -32(%rbp)
    jmp .L1121
.L1122:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl string_util_split
string_util_split:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    call string_array_create
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1141
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1142
.L1141:
.L1142:
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_tokenizer_create
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1151
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_array_destroy
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1152
.L1151:
.L1152:
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_tokenizer_has_next
    movq %rax, -40(%rbp)
.L1161:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1162
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_tokenizer_next
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_array_add
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_tokenizer_has_next
    movq %rax, -40(%rbp)
    jmp .L1161
.L1162:
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_tokenizer_destroy
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl memory_copy_string
memory_copy_string:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq -8(%rbp), %rax
    addq -16(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq $1, %rax
    movq %rax, -56(%rbp)
.L1171:    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1172
    movq -48(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1181
    movq $0, %rax
    movq %rax, -56(%rbp)
    jmp .L1182
.L1181:
    movq -48(%rbp), %rax
    addq $1, %rax
    movq %rax, -48(%rbp)
.L1182:
    jmp .L1171
.L1172:
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl memory_copy_string_to_buffer
memory_copy_string_to_buffer:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    movq %rax, -32(%rbp)
    movq $1, %rax
    movq %rax, -40(%rbp)
.L1191:    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1192
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    movq $0, %rax
    movq %rax, -40(%rbp)
    jmp .L1202
.L1201:
    movq -32(%rbp), %rax
    addq $1, %rax
    movq %rax, -32(%rbp)
.L1202:
    jmp .L1191
.L1192:
    movq -32(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl memory_pointer_offset
memory_pointer_offset:
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


.globl memory_allocate
memory_allocate:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rbp, %rsp
    popq %rbp
    ret

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
