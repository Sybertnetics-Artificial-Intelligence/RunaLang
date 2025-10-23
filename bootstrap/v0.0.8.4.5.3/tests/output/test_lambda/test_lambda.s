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
.text
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    jmp __skip_lambda_0

# Lambda function
__lambda_0:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    leave
    ret

__skip_lambda_0:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_0(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -8(%rbp)
    jmp __skip_lambda_1

# Lambda function
__lambda_1:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    addq $10, %rax
    leave
    ret

__skip_lambda_1:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_1(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -16(%rbp)
    jmp __skip_lambda_2

# Lambda function
__lambda_2:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq $42, %rax
    leave
    ret

__skip_lambda_2:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_2(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -24(%rbp)
    movq $4, %rax
    pushq %rax  # Save argument on stack
    movq -8(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
.L32:
    movq $5, %rax
    pushq %rax  # Save argument on stack
    movq -16(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $15, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L41
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
    movq $0, %rax
    pushq %rax  # Save argument on stack
    movq -24(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    movq $3, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
    jmp __skip_lambda_6

# Lambda function
__lambda_6:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq %rdx, -24(%rbp)  # Store parameter 2
    movq -16(%rbp), %rax
    addq -24(%rbp), %rax
    leave
    ret

__skip_lambda_6:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_6(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -56(%rbp)
    movq $3, %rax
    pushq %rax  # Save argument on stack
    movq $5, %rax
    pushq %rax  # Save argument on stack
    movq -56(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rdx  # Pop argument 2
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq $4, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
    jmp __skip_lambda_8

# Lambda function
__lambda_8:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq %rdx, -24(%rbp)  # Store parameter 2
    movq -16(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    leave
    ret

__skip_lambda_8:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_8(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -72(%rbp)
    movq $7, %rax
    pushq %rax  # Save argument on stack
    movq $6, %rax
    pushq %rax  # Save argument on stack
    movq -72(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rdx  # Pop argument 2
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq $5, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
.L92:
    jmp __skip_lambda_10

# Lambda function
__lambda_10:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq %rdx, -24(%rbp)  # Store parameter 2
    movq -16(%rbp), %rax
    subq -24(%rbp), %rax
    leave
    ret

__skip_lambda_10:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_10(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -88(%rbp)
    movq $10, %rax
    pushq %rax  # Save argument on stack
    movq $3, %rax
    pushq %rax  # Save argument on stack
    movq -88(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rdx  # Pop argument 2
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq $6, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L112
.L111:
.L112:
    movq $10, %rax
    movq %rax, -104(%rbp)
    jmp __skip_lambda_12

# Lambda function
__lambda_12:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_12:
    # Allocate environment for 1 captured variables
    movq $8, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -104(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_12(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -112(%rbp)
    movq $5, %rax
    pushq %rax  # Save argument on stack
    movq -112(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $15, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq $7, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L132
.L131:
.L132:
    movq $100, %rax
    movq %rax, -128(%rbp)
    jmp __skip_lambda_14

# Lambda function
__lambda_14:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_14:
    # Allocate environment for 1 captured variables
    movq $8, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -128(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_14(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -136(%rbp)
    movq $23, %rax
    pushq %rax  # Save argument on stack
    movq -136(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $123, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L151
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L152
.L151:
.L152:
    movq $3, %rax
    movq %rax, -152(%rbp)
    movq $4, %rax
    movq %rax, -160(%rbp)
    jmp __skip_lambda_16

# Lambda function
__lambda_16:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 8(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_16:
    # Allocate environment for 2 captured variables
    movq $16, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -152(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    movq -160(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 8(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_16(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -168(%rbp)
    movq $2, %rax
    pushq %rax  # Save argument on stack
    movq -168(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq $9, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L172
.L171:
.L172:
    movq $5, %rax
    movq %rax, -184(%rbp)
    movq $7, %rax
    movq %rax, -192(%rbp)
    jmp __skip_lambda_18

# Lambda function
__lambda_18:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 8(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    leave
    ret

__skip_lambda_18:
    # Allocate environment for 2 captured variables
    movq $16, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -184(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    movq -192(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 8(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_18(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -200(%rbp)
    movq $4, %rax
    pushq %rax  # Save argument on stack
    movq -200(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $13, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq $10, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L192
.L191:
.L192:
    movq $10, %rax
    movq %rax, -216(%rbp)
    jmp __skip_lambda_20

# Lambda function
__lambda_20:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_20:
    # Allocate environment for 1 captured variables
    movq $8, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -216(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_20(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -224(%rbp)
    movq $5, %rax
    pushq %rax  # Save argument on stack
    movq -224(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -232(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq $15, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L211
    movq $11, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L212
.L211:
.L212:
    movq $1000, %rax
    movq %rax, -240(%rbp)
    jmp __skip_lambda_22

# Lambda function
__lambda_22:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_22:
    # Allocate environment for 1 captured variables
    movq $8, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -240(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_22(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -248(%rbp)
    jmp __skip_lambda_23

# Lambda function
__lambda_23:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_23:
    # Allocate environment for 1 captured variables
    movq $8, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -240(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_23(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -256(%rbp)
    movq $23, %rax
    pushq %rax  # Save argument on stack
    movq -248(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -264(%rbp)
    movq $77, %rax
    pushq %rax  # Save argument on stack
    movq -256(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -272(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $1023, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    movq $12, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L242
.L241:
.L242:
    movq -272(%rbp), %rax
    pushq %rax
    movq $1077, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L251
    movq $13, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L252
.L251:
.L252:
    movq $2, %rax
    movq %rax, -280(%rbp)
    movq $10, %rax
    movq %rax, -288(%rbp)
    jmp __skip_lambda_26

# Lambda function
__lambda_26:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq %rdx, -24(%rbp)  # Store parameter 2
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 0(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    imulq %rbx, %rax
    addq -24(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rbx  # Load environment pointer
    movq 8(%rbx), %rax  # Load captured variable from environment
    popq %rbx
    addq %rbx, %rax
    leave
    ret

__skip_lambda_26:
    # Allocate environment for 2 captured variables
    movq $16, %rdi
    call allocate
    pushq %rax  # Save environment pointer
    movq -280(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 0(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    movq -288(%rbp), %rbx  # Load captured variable
    popq %rax  # Get environment pointer
    movq %rbx, 8(%rax)  # Store in environment
    pushq %rax  # Save environment pointer again
    popq %rcx  # Final environment pointer in %rcx
    # Allocate closure struct
    pushq %rcx  # Save environment pointer across call
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_26(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    popq %rcx  # Restore environment pointer
    movq %rcx, 8(%rax)  # Store environment pointer
    movq %rax, -296(%rbp)
    movq $5, %rax
    pushq %rax  # Save argument on stack
    movq $3, %rax
    pushq %rax  # Save argument on stack
    movq -296(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rdx  # Pop argument 2
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $23, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq $14, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L272
.L271:
.L272:
    jmp __skip_lambda_28

# Lambda function
__lambda_28:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp  # Allocate space for environment + parameters
    movq %rdi, -8(%rbp)  # Store environment pointer
    movq %rsi, -16(%rbp)  # Store parameter 1
    movq -16(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    leave
    ret

__skip_lambda_28:
    # Allocate closure struct
    movq $16, %rdi
    call allocate
    pushq %rax  # Save closure pointer
    leaq __lambda_28(%rip), %rbx  # Load function address
    popq %rax  # Restore closure pointer
    movq %rbx, 0(%rax)  # Store function_ptr
    movq $0, 8(%rax)  # NULL environment
    movq %rax, -312(%rbp)
    movq $21, %rax
    pushq %rax  # Save argument on stack
    movq -312(%rbp), %rax
    movq %rax, %r10  # Save closure pointer in r10
    movq 8(%r10), %rdi  # Load environment pointer (first param)
    popq %rsi  # Pop argument 1
    movq 0(%r10), %rbx  # Load function pointer from closure
    call *%rbx  # Invoke lambda
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq $15, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L292
.L291:
.L292:
    movq $0, %rax
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
