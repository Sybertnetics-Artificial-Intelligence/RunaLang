# Imports:#   Import compiler/frontend/primitives/platform/platform_selector.runa as Selector

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

    # Convert integer to string (signed)
    movq %rdi, %rax  # integer value
    xorq %r8, %r8    # r8 = 0 (negative flag)
    testq %rax, %rax
    jns .pi_not_negative
    movq $1, %r8     # mark as negative
    negq %rax        # make positive for conversion
.pi_not_negative:
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
    # Prepend minus sign if negative
    testq %r8, %r8
    jz .pi_not_neg_print
    decq %rsi
    movb $45, (%rsi)  # '-' character
.pi_not_neg_print:

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
.STR0:    .string "[MAIN ERROR] Could not open input file '"
.STR1:    .string "'"
.STR2:    .string "compiler/"
.STR3:    .string "linux_x86_64"
.STR4:    .string "linux_arm64"
.STR5:    .string "linux_arm32"
.STR6:    .string "mips32"
.STR7:    .string "mips64"
.STR8:    .string "darwin_x86_64"
.STR9:    .string "darwin_arm64"
.STR10:    .string "freebsd_x64"
.STR11:    .string "freebsd_arm64"
.STR12:    .string "netbsd_x64"
.STR13:    .string "netbsd_arm64"
.STR14:    .string "openbsd_x64"
.STR15:    .string "openbsd_arm64"
.STR16:    .string "windows_x86_64"
.STR17:    .string "windows_arm64"
.STR18:    .string "powerpc"
.STR19:    .string "riscv32"
.STR20:    .string "riscv64"
.STR21:    .string ""
.STR22:    .string "Usage: "
.STR23:    .string " <input.runa> <output.s> [--target <key>] [--verbose]"
.STR24:    .string "[ERROR] Missing trailing flag"
.STR25:    .string "--verbose"
.STR26:    .string "[ERROR] Unrecognized option: "
.STR27:    .string "[ERROR] Missing --target flag"
.STR28:    .string "--target"
.STR29:    .string "[ERROR] --target requires a platform key argument"
.STR30:    .string "[ERROR] Unknown --target platform key: "
.STR31:    .string "[ERROR] Missing trailing flag after --target value"
.STR32:    .string "[ERROR] Could not detect host platform - uname failed or the host os/arch is not a supported Runa target. Pass --target <key> explicitly."
.STR33:    .string "[ERROR] Failed to read source file"
.STR34:    .string "[ERROR] Failed to create arena allocator"
.STR35:    .string "[ERROR] main: Parsing failed - program is NULL"
.STR36:    .string "[PHASE_TIMING_US] lex="
.STR37:    .string " parse="
.STR38:    .string " imports="
.STR39:    .string " codegen="
.STR40:    .string " total="
.STR41:    .string "Successfully compiled '"
.STR42:    .string "' to '"
.text


.globl read_file_internal
read_file_internal:
    pushq %rbp
    movq %rsp, %rbp
    subq $1064, %rsp  # Per-function frame size
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call runtime_read_file
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1
    movq -8(%rbp), %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -24(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2
.L1:
.L2:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl extract_base_dir
extract_base_dir:
    pushq %rbp
    movq %rsp, %rbp
    subq $1064, %rsp  # Per-function frame size
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    leaq .STR2(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_find@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L21
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    movq -16(%rbp), %rax
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
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_substring@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl is_known_platform_key
is_known_platform_key:
    pushq %rbp
    movq %rsp, %rbp
    subq $1048, %rsp  # Per-function frame size
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
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
    leaq .STR3(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L51
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
    leaq .STR4(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
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
    leaq .STR5(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L71
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
    leaq .STR6(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L81
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    leaq .STR7(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L92
.L91:
.L92:
    leaq .STR8(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L101
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L102
.L101:
.L102:
    leaq .STR9(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L112
.L111:
.L112:
    leaq .STR10(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L122
.L121:
.L122:
    leaq .STR11(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L132
.L131:
.L132:
    leaq .STR12(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L141
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L142
.L141:
.L142:
    leaq .STR13(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
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
    leaq .STR14(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L161
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L162
.L161:
.L162:
    leaq .STR15(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L172
.L171:
.L172:
    leaq .STR16(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L181
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L182
.L181:
.L182:
    leaq .STR17(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L192
.L191:
.L192:
    leaq .STR18(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L202
.L201:
.L202:
    leaq .STR19(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
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
    leaq .STR20(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L222
.L221:
.L222:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl detect_host_platform_key
detect_host_platform_key:
    pushq %rbp
    movq %rsp, %rbp
    subq $1080, %rsp  # Per-function frame size
    movq $512, %rax
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
    jz .L231
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L232
.L231:
.L232:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call syscall_uname
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L241
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L242
.L241:
.L242:
    movq -8(%rbp), %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    addq $260, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call get_platform_key@PLT
    movq %rax, -40(%rbp)
    leaq .STR21(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    testq %rax, %rax
    jz .L251
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L252
.L251:
.L252:
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.globl main


.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    # Initialize command line arguments
    pushq %rdi  # Save argc
    pushq %rsi  # Save argv
    call runtime_set_command_line_args@PLT
    popq %rsi   # Restore argv
    popq %rdi   # Restore argc
    subq $1464, %rsp  # Per-function frame size
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    call __module_init  # Initialize runtime-initialized globals
    movq $0, %rax
    movq %rax, -24(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
    movq -8(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq -8(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
    movq -8(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq $0, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    leaq .STR22(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -40(%rbp)
    leaq .STR23(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -48(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L292
.L291:
.L292:
    jmp .L282
.L281:
.L282:
    jmp .L272
.L271:
.L272:
    jmp .L262
.L261:
.L262:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -56(%rbp)
    movq $2, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $0, %rax
    movq %rax, -80(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq $1, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L302
.L301:
.L302:
    movq -8(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L311
    movq $1, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L312
.L311:
.L312:
    movq -8(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    movq $3, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L331
    leaq .STR24(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L332
.L331:
.L332:
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L341
    movq -88(%rbp), %rax
    pushq %rax
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L342
.L341:
.L342:
    movq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L322
.L321:
.L322:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
    movq $3, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -104(%rbp)
    movq $4, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    leaq .STR27(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L362
.L361:
.L362:
    leaq .STR28(%rip), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    movq -104(%rbp), %rax
    pushq %rax
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L372
.L371:
.L372:
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    leaq .STR29(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L382
.L381:
.L382:
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call is_known_platform_key
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L391
    movq -112(%rbp), %rax
    pushq %rax
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L392
.L391:
.L392:
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -112(%rbp), %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -8(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    movq $5, %rax
    pushq %rax
    popq %rdi
    call get_command_line_arg@PLT
    movq %rax, -136(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    leaq .STR31(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L412
.L411:
.L412:
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_equals@PLT
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    movq -136(%rbp), %rax
    pushq %rax
    leaq .STR26(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L422
.L421:
.L422:
    movq $1, %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L402
.L401:
.L402:
    jmp .L352
.L351:
    call detect_host_platform_key
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L431
    leaq .STR32(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L432
.L431:
.L432:
    movq -152(%rbp), %rax
    pushq %rax
    leaq -72(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
.L352:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call read_file_internal@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    leaq .STR33(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L442
.L441:
.L442:
    movq $65536, %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call arena_create
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L451
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L452
.L451:
.L452:
    call get_time_us
    movq %rax, -184(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call lexer_create
    movq %rax, -192(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call parser_create
    movq %rax, -200(%rbp)
    call get_time_us
    movq %rax, -208(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_parse_program
    movq %rax, -216(%rbp)
    call get_time_us
    movq %rax, -224(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    leaq .STR35(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_destroy
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_destroy
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call arena_destroy
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L462
.L461:
.L462:
    movq $8, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -232(%rbp)
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L471
    movq $0, %rax
    movq %rax, -248(%rbp)
.L481:    movq -248(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L482
    movq -248(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -256(%rbp)
    movq $0, %rax
    pushq %rax
    movq -240(%rbp), %rax
    addq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L491
    movq -56(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call function_set_source_file
    jmp .L492
.L491:
.L492:
    movq -248(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -248(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L481
.L482:
    jmp .L472
.L471:
.L472:
    movq $24, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -272(%rbp)
    movq $16, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L501
    movq $0, %rax
    movq %rax, -288(%rbp)
.L511:    movq -288(%rbp), %rax
    pushq %rax
    movq -272(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L512
    movq -288(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L521
    movq -56(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call type_definition_set_source_file
    jmp .L522
.L521:
.L522:
    movq -288(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -288(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L511
.L512:
    jmp .L502
.L501:
.L502:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call extract_base_dir
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_import_base_dir
    jmp .L532
.L531:
.L532:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call extract_directory
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L541
    movq -312(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L551
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -328(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq -328(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L561
    movq -336(%rbp), %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call string_substring@PLT
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_import_source_dir
    jmp .L562
.L561:
.L562:
    jmp .L552
.L551:
.L552:
    jmp .L542
.L541:
.L542:
    call get_time_us
    movq %rax, -352(%rbp)
    movq $56, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq $64, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $1, %rax
    pushq %rax
    movq $68, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_target_platform_key
    movq -176(%rbp), %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call process_imports_recursive
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call program_destroy
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_destroy
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_destroy
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call arena_destroy
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L572
.L571:
.L572:
    call get_time_us
    movq %rax, -376(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_create
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L581
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call arena_destroy
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call program_destroy
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_destroy
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_destroy
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L582
.L581:
.L582:
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call set_codegen_target_platform_key
    movq -216(%rbp), %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate
    call get_time_us
    movq %rax, -392(%rbp)
    movq $0, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    call file_close_buffered@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    leaq .STR36(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -208(%rbp), %rax
    subq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR37(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -224(%rbp), %rax
    subq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR38(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -376(%rbp), %rax
    subq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR39(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -392(%rbp), %rax
    subq -376(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR40(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -392(%rbp), %rax
    subq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    leaq .STR21(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    jmp .L592
.L591:
.L592:
    movq -56(%rbp), %rax
    pushq %rax
    leaq .STR41(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -408(%rbp)
    leaq .STR42(%rip), %rax
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -416(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -424(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -432(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_destroy
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    call program_destroy
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call parser_destroy
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call lexer_destroy
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    call arena_destroy
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret

.weak __module_init
__module_init:
    pushq %rbp
    movq %rsp, %rbp
    subq $2056, %rsp  # Stack space for global initializer expression spills
    leave
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
