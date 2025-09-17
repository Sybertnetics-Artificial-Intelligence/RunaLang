    .section .rodata
.LC0:
    .string "%d\n"
.LC1:
    .string "%s\n"

.LC2:
    .string "%d"

    .text
    .globl main
    .type main, @function
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    leaq .LS0(%rip), %rax
    movq %rax, -8(%rbp)
    leaq .LS1(%rip), %rax
    movq %rax, %rdi
    movq -8(%rbp), %rax
    movq %rax, %rsi
    call write_file_impl
    leaq .LS2(%rip), %rax
    movq %rax, %rdi
    call read_file_impl
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
# File I/O helper functions
read_file_impl:
    .type read_file_impl, @function
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp
    movq %rdi, -8(%rbp)
    movq %rdi, %rdi
    leaq .Lread_mode(%rip), %rsi
    call fopen@PLT
    movq %rax, -16(%rbp)
    testq %rax, %rax
    je .Lread_error
    movq %rax, %rdi
    movl $0, %esi
    movl $2, %edx
    call fseek@PLT
    movq -16(%rbp), %rdi
    call ftell@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rdi
    movl $0, %esi
    movl $0, %edx
    call fseek@PLT
    movq -24(%rbp), %rdi
    addq $1, %rdi
    call malloc@PLT
    movq %rax, -32(%rbp)
    movq %rax, %rdi
    movl $1, %esi
    movq -24(%rbp), %rdx
    movq -16(%rbp), %rcx
    call fread@PLT
    movq -32(%rbp), %rax
    movq -24(%rbp), %rdx
    movb $0, (%rax,%rdx,1)
    movq -16(%rbp), %rdi
    call fclose@PLT
    movq -32(%rbp), %rax
    leave
    ret
.Lread_error:
    movq $0, %rax
    leave
    ret

write_file_impl:
    .type write_file_impl, @function
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    leaq .Lwrite_mode(%rip), %rsi
    call fopen@PLT
    testq %rax, %rax
    je .Lwrite_error
    movq %rax, %rdi
    movq -16(%rbp), %rsi
    call fputs@PLT
    movq %rax, %rdi
    call fclose@PLT
    leave
    ret
.Lwrite_error:
    leave
    ret

    .section .rodata
.Lread_mode:
    .string "r"
.Lwrite_mode:
    .string "w"
    .text


    .section .rodata
.LS0:
    .string "Hello from Runa file I/O!"
.LS1:
    .string "test_output.txt"
.LS2:
    .string "test_output.txt"
