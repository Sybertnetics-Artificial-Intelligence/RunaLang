.section .rodata
.STR0:    .string "\n"
.STR1:    .string "Integer"
.STR2:    .string "Byte"
.STR3:    .string "Short"
.STR4:    .string "Long"
.STR5:    .string ".STR"
.STR6:    .string "    leaq "
.STR7:    .string "(%rip), %rbx  # Address of global variable"
.STR8:    .string "[CODEGEN ERROR] Unknown variable '"
.STR9:    .string "'"
.STR10:    .string "    leaq -"
.STR11:    .string "(%rbp), %rbx\n"
.STR12:    .string "[CODEGEN ERROR] Cannot determine type of object in field access"
.STR13:    .string "[CODEGEN ERROR] Unknown type '"
.STR14:    .string "[CODEGEN ERROR] Type '"
.STR15:    .string "' has no field '"
.STR16:    .string "    addq $"
.STR17:    .string ", %rbx"
.STR18:    .string "    movq -"
.STR19:    .string "(%rbp), %rbx  # Load array parameter pointer"
.STR20:    .string "    pushq %rbx"
.STR21:    .string "    popq %rbx"
.STR22:    .string "    imulq $8, %rax"
.STR23:    .string "    addq %rax, %rbx"
.STR24:    .string "[CODEGEN ERROR] Invalid lvalue expression type"
.STR25:    .string "    movq $"
.STR26:    .string ", %rax\n"
.STR27:    .string ", %rax  # Load compile-time constant "
.STR28:    .string "    movq "
.STR29:    .string "(%rip), %rax  # Load global variable\n"
.STR30:    .string "[CODEGEN ERROR] Undefined variable: "
.STR31:    .string "(%rip), %rax  # Load function address\n"
.STR32:    .string "(%rbp), %rax  # Load array address\n"
.STR33:    .string "(%rbp), %rax\n"
.STR34:    .string "[CODEGEN ERROR] Undefined variable in load: "
.STR35:    .string "[CODEGEN ERROR] Undefined variable in store: "
.STR36:    .string "    movq %rax, -"
.STR37:    .string "(%rbp)\n"
.STR38:    .string "[CODEGEN ERROR] Invalid string literal expression"
.STR39:    .string "    leaq .STR"
.STR40:    .string "(%rip), %rax\n"
.STR41:    .string "    pushq %rax"
.STR42:    .string "    addq %rbx, %rax"
.STR43:    .string "    subq %rax, %rbx"
.STR44:    .string "    movq %rbx, %rax"
.STR45:    .string "    imulq %rbx, %rax"
.STR46:    .string "    movq %rax, %rcx"
.STR47:    .string "    testq %rcx, %rcx"
.STR48:    .string "    jz .Ldiv_by_zero_"
.STR49:    .string "    cqto"
.STR50:    .string "    idivq %rcx"
.STR51:    .string "    jmp .Ldiv_done_"
.STR52:    .string ".Ldiv_by_zero_"
.STR53:    .string ":"
.STR54:    .string "    movq $0, %rax"
.STR55:    .string ".Ldiv_done_"
.STR56:    .string "    jz .Lmod_by_zero_"
.STR57:    .string "    movq %rdx, %rax"
.STR58:    .string "    jmp .Lmod_done_"
.STR59:    .string ".Lmod_by_zero_"
.STR60:    .string ".Lmod_done_"
.STR61:    .string "    andq %rbx, %rax"
.STR62:    .string "    orq %rbx, %rax"
.STR63:    .string "    xorq %rbx, %rax"
.STR64:    .string "    salq %cl, %rax"
.STR65:    .string "    sarq %cl, %rax"
.STR66:    .string "    cmpq %rax, %rbx"
.STR67:    .string "    sete %al"
.STR68:    .string "    setne %al"
.STR69:    .string "    setl %al"
.STR70:    .string "    setg %al"
.STR71:    .string "    setle %al"
.STR72:    .string "    setge %al"
.STR73:    .string "    movzbq %al, %rax"
.STR74:    .string "[CODEGEN ERROR] NULL argument expression pointer: "
.STR75:    .string "    pushq %rax\n"
.STR76:    .string "    popq %rdi\n"
.STR77:    .string "    popq %rsi\n"
.STR78:    .string "    popq %rdx\n"
.STR79:    .string "    popq %rcx\n"
.STR80:    .string "    popq %r8\n"
.STR81:    .string "    popq %r9\n"
.STR82:    .string "    call "
.STR83:    .string "allocate"
.STR84:    .string "deallocate"
.STR85:    .string "memory_allocate"
.STR86:    .string "memory_reallocate"
.STR87:    .string "string_length"
.STR88:    .string "string_char_at"
.STR89:    .string "string_equals"
.STR90:    .string "string_compare"
.STR91:    .string "string_find"
.STR92:    .string "string_substring"
.STR93:    .string "string_duplicate"
.STR94:    .string "string_concat"
.STR95:    .string "integer_to_string"
.STR96:    .string "ascii_value_of"
.STR97:    .string "is_digit"
.STR98:    .string "is_whitespace"
.STR99:    .string "file_open_buffered"
.STR100:    .string "file_write_buffered"
.STR101:    .string "file_close_buffered"
.STR102:    .string "memory_get_byte"
.STR103:    .string "memory_set_byte"
.STR104:    .string "memory_get_int32"
.STR105:    .string "memory_set_int32"
.STR106:    .string "memory_get_integer"
.STR107:    .string "memory_set_integer"
.STR108:    .string "memory_get_pointer"
.STR109:    .string "memory_set_pointer"
.STR110:    .string "memory_set_pointer_at_index"
.STR111:    .string "exit_with_code"
.STR112:    .string "read_file_internal"
.STR113:    .string "get_command_line_arg"
.STR114:    .string "@PLT"
.STR115:    .string "[CODEGEN ERROR] Unknown variable"
.STR116:    .string "    movq (%rax), %rax\n"
.STR117:    .string "    movq %rbx, %rax\n"
.STR118:    .string ""
.STR119:    .string "    # Unimplemented builtin type "
.STR120:    .string "    movq $0, %rax  # Placeholder return value\n"
.STR121:    .string "[CODEGEN ERROR] NULL expression pointer"
.STR122:    .string "unknown_builtin_"
.STR123:    .string "    movq $0, %rax\n"
.STR124:    .string "[CODEGEN ERROR] Unsupported expression type"
.STR125:    .string "    movq $0, -"
.STR126:    .string "(%rbp)  # Zero array element"
.STR127:    .string "String"
.STR128:    .string "List"
.STR129:    .string "    popq %rax"
.STR130:    .string "    movq %rax, (%rbx)"
.STR131:    .string "    movq %rbp, %rsp\n"
.STR132:    .string "    popq %rbp\n"
.STR133:    .string "    ret\n"
.STR134:    .string "    testq %rax, %rax"
.STR135:    .string "    jz .L"
.STR136:    .string "    jmp .L"
.STR137:    .string ".L"
.STR138:    .string "    movq %rax, %rdx"
.STR139:    .string "    cmpq %rdx, %rax"
.STR140:    .string "    jg .L"
.STR141:    .string "    addq $1, %rax"
.STR142:    .string "    addq %rdx, %rax"
.STR143:    .string "    movq %rax, %rdi\n"
.STR144:    .string "    call print_string\n"
.STR145:    .string "    call print_integer\n"
.STR146:    .string "    pushq %rax  # Save match expression value"
.STR147:    .string ".match_end_"
.STR148:    .string ".match_case_"
.STR149:    .string "_"
.STR150:    .string "    popq %rax  # Get match expression\n"
.STR151:    .string "    pushq %rax  # Keep on stack"
.STR152:    .string "    movq (%rax), %rdx  # Load variant tag"
.STR153:    .string "    cmpq $"
.STR154:    .string ", %rdx  # Check tag for "
.STR155:    .string "    jne "
.STR156:    .string "  # Jump to next case"
.STR157:    .string "  # No match, exit"
.STR158:    .string "    popq %rax  # Get variant pointer\n"
.STR159:    .string "(%rax), %rdx  # Load field "
.STR160:    .string "    movq %rdx, -"
.STR161:    .string "(%rbp, 0)  # Store "
.STR162:    .string " at stack offset"
.STR163:    .string "    jmp "
.STR164:    .string "    popq %rax  # Clean up match expression\n"
.STR165:    .string ".globl "
.STR166:    .string ":\n"
.STR167:    .string "    pushq %rbp"
.STR168:    .string "    movq %rsp, %rbp"
.STR169:    .string "%rdi"
.STR170:    .string "%rsi"
.STR171:    .string "%rdx"
.STR172:    .string "%rcx"
.STR173:    .string "%r8"
.STR174:    .string "%r9"
.STR175:    .string "main"
.STR176:    .string "    # Initialize command line arguments"
.STR177:    .string "    pushq %rdi  # Save argc"
.STR178:    .string "    pushq %rsi  # Save argv"
.STR179:    .string "    call runtime_set_command_line_args@PLT"
.STR180:    .string "    popq %rsi   # Restore argv"
.STR181:    .string "    popq %rdi   # Restore argc"
.STR182:    .string "    subq $2048, %rsp  # Pre-allocate generous stack space"
.STR183:    .string ", -"
.STR184:    .string "(%rbp)"
.STR185:    .string "    movq %rbp, %rsp"
.STR186:    .string "    popq %rbp"
.STR187:    .string "    ret"
.STR188:    .string "# Imports:"
.STR189:    .string "#   Import "
.STR190:    .string " as "
.STR191:    .string "[ERROR] codegen_generate: functions pointer is NULL"
.STR192:    .string ".section .rodata"
.STR193:    .string "    .string "
.STR194:    .string ".section .data"
.STR195:    .string "    .quad "
.STR196:    .string "    .quad 0  # Non-constant initializer defaults to 0"
.STR197:    .string ".section .bss"
.STR198:    .string "    .zero 8  # 8 bytes for Integer"
.STR199:    .string ".text"
.STR200:    .string "print_string:"
.STR201:    .string "    # Calculate string len"
.STR202:    .string "    movq %rdi, %rsi  # Save string pointer"
.STR203:    .string "    movq %rdi, %rcx  # Counter for strlen"
.STR204:    .string "    xorq %rax, %rax  # Length accumulator"
.STR205:    .string ".strlen_loop:"
.STR206:    .string "    cmpb $0, (%rcx)"
.STR207:    .string "    je .strlen_done"
.STR208:    .string "    incq %rcx"
.STR209:    .string "    incq %rax"
.STR210:    .string "    jmp .strlen_loop"
.STR211:    .string ".strlen_done:"
.STR212:    .string "    # Call write syscall (sys_write = 1)"
.STR213:    .string "    movq $1, %rdi     # fd = stdout"
.STR214:    .string "    movq %rsi, %rsi   # buf = string pointer (already in rsi)"
.STR215:    .string "    movq %rax, %rdx   # count = string len"
.STR216:    .string "    movq $1, %rax     # syscall number for write"
.STR217:    .string "    syscall"
.STR218:    .string "    # Print newline"
.STR219:    .string "    leaq .newline(%rip), %rsi  # newline string"
.STR220:    .string "    movq $1, %rdx     # count = 1"
.STR221:    .string "print_integer:"
.STR222:    .string "    subq $32, %rsp  # Space for string buffer (20 digits + null)"
.STR223:    .string "    # Convert integer to string"
.STR224:    .string "    movq %rdi, %rax  # integer value"
.STR225:    .string "    leaq -32(%rbp), %rsi  # buffer pointer"
.STR226:    .string "    addq $19, %rsi  # point to end of buffer (for reverse building)"
.STR227:    .string "    movb $0, (%rsi)  # null terminator"
.STR228:    .string "    decq %rsi"
.STR229:    .string "    # Handle zero case"
.STR230:    .string "    jnz .convert_loop"
.STR231:    .string "    movb $48, (%rsi)  # '0' character"
.STR232:    .string "    jmp .convert_done"
.STR233:    .string ".convert_loop:"
.STR234:    .string "    jz .convert_done"
.STR235:    .string "    movq $10, %rbx"
.STR236:    .string "    xorq %rdx, %rdx"
.STR237:    .string "    divq %rbx  # %rax = quotient, %rdx = remainder"
.STR238:    .string "    addq $48, %rdx  # convert remainder to ASCII"
.STR239:    .string "    movb %dl, (%rsi)  # store digit"
.STR240:    .string "    jmp .convert_loop"
.STR241:    .string ".convert_done:"
.STR242:    .string "    incq %rsi  # point to first character"
.STR243:    .string "    movq %rsi, %rcx  # Counter for strlen"
.STR244:    .string ".int_strlen_loop:"
.STR245:    .string "    je .int_strlen_done"
.STR246:    .string "    jmp .int_strlen_loop"
.STR247:    .string ".int_strlen_done:"
.STR248:    .string "    # %rsi already points to string"
.STR249:    .string ".newline:"
.STR250:    .string "    .byte 10  # newline character"
.STR251:    .string ".globl main"
.STR252:    .string ".section .note.GNU-stack"

.text
print_string:
    pushq %rbp
    movq %rsp, %rbp

    # Calculate string len
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
    movq %rax, %rdx   # count = string len
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

    # Calculate string len
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
    movq %rax, %rdx   # count = string len
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


.globl emit_line
emit_line:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_find_variable
codegen_find_variable:
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
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
.L1:    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2
    movq -40(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -56(%rbp)
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
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
    jz .L11
    movq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
.L12:
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -40(%rbp)
    jmp .L1
.L2:
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_calculate_type_size
codegen_calculate_type_size:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    leaq .STR1(%rip), %rax
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
    jz .L21
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L22
.L21:
.L22:
    leaq .STR2(%rip), %rax
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
    jz .L31
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L32
.L31:
.L32:
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
    jz .L41
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
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
    jz .L51
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L61
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
.L71:    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L72
    movq -40(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -8(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
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
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -40(%rbp)
    jmp .L71
.L72:
    jmp .L62
.L61:
.L62:
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_add_variable_with_type_and_param_flag
codegen_add_variable_with_type_and_param_flag:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq %rcx, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -48(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
    movq -48(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
.L101:    movq -88(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L102
    movq -88(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -120(%rbp)
    movq $32, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_copy
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -88(%rbp)
    jmp .L101
.L102:
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -80(%rbp), %rax
    movq %rax, -56(%rbp)
    jmp .L92
.L91:
.L92:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_calculate_type_size
    movq %rax, -152(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L111
    movq -144(%rbp), %rax
    pushq %rax
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_calculate_type_size
    movq %rax, -152(%rbp)
    jmp .L112
.L111:
.L112:
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -40(%rbp), %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -200(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -176(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L121
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L122
.L121:
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
.L122:
    movq -32(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -40(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -184(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_add_variable_with_type
codegen_add_variable_with_type:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call codegen_add_variable_with_type_and_param_flag
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_add_variable
codegen_add_variable:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    leaq .STR1(%rip), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_add_string_literal
codegen_add_string_literal:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L131
    movq -32(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
.L141:    movq -72(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L142
    movq -72(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -88(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -104(%rbp)
    movq $16, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_copy
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -72(%rbp)
    jmp .L141
.L142:
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -48(%rbp), %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -64(%rbp), %rax
    movq %rax, -40(%rbp)
    jmp .L132
.L131:
.L132:
    movq -24(%rbp), %rax
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -144(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR5(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -128(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_collect_strings_from_expression
codegen_collect_strings_from_expression:
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
    jz .L151
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L152
.L151:
.L152:
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
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L171
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
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
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L191
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L192
.L191:
.L192:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L201
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L202
.L201:
.L202:
    movq $0, %rax
    movq %rax, -56(%rbp)
.L211:    movq -56(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L212
    movq -56(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -64(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    movq -80(%rbp), %rax
    pushq %rax
    movq $65536, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L231
    movq -48(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
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
    jz .L241
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L242
.L241:
.L242:
    jmp .L232
.L231:
.L232:
    jmp .L222
.L221:
.L222:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -56(%rbp)
    jmp .L211
.L212:
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_string_literal
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L172
.L171:
.L172:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L251
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L252
.L251:
.L252:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L262
.L261:
.L262:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L271
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -128(%rbp)
    movq $0, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -136(%rbp)
    movq $8, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $16, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -152(%rbp)
    movq $0, %rax
    movq %rax, -56(%rbp)
.L281:    movq -56(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L282
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -56(%rbp)
    jmp .L281
.L282:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L272
.L271:
.L272:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L291
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L292
.L291:
.L292:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -208(%rbp)
    movq $8, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq $16, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -152(%rbp)
    movq $0, %rax
    movq %rax, -56(%rbp)
.L311:    movq -56(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L312
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -56(%rbp)
    jmp .L311
.L312:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L302
.L301:
.L302:
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -264(%rbp)
    movq $0, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -272(%rbp)
    movq $8, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq $16, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq $24, %rax
    pushq %rax
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -56(%rbp)
.L331:    movq -56(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L332
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -312(%rbp)
    movq -312(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -56(%rbp)
    jmp .L331
.L332:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L322
.L321:
.L322:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L341
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -336(%rbp)
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -344(%rbp)
    movq $8, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -352(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -352(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L342
.L341:
.L342:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_collect_strings_from_statement
codegen_collect_strings_from_statement:
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
    jz .L351
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L352
.L351:
.L352:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L361
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L362
.L361:
.L362:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L372
.L371:
.L372:
    movq -24(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L382
.L381:
.L382:
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L391
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L392
.L391:
.L392:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L401
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L402
.L401:
.L402:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L411
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L412
.L411:
.L412:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L421
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -80(%rbp)
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L422
.L421:
.L422:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L431
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -96(%rbp)
    movq $0, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $16, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -120(%rbp)
    movq $24, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq $32, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -136(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq -112(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
    movq $0, %rax
    movq %rax, -144(%rbp)
.L451:    movq -144(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L452
    movq -144(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -144(%rbp)
    jmp .L451
.L452:
    jmp .L442
.L441:
.L442:
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    movq $0, %rax
    movq %rax, -144(%rbp)
.L471:    movq -144(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L472
    movq -144(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -144(%rbp)
    jmp .L471
.L472:
    jmp .L462
.L461:
.L462:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L432
.L431:
.L432:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $16, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -232(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rax, -144(%rbp)
.L491:    movq -144(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L492
    movq -144(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -144(%rbp)
    jmp .L491
.L492:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L482
.L481:
.L482:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L501
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $8, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $16, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -232(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rax, -144(%rbp)
.L511:    movq -144(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L512
    movq -144(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -144(%rbp)
    jmp .L511
.L512:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L502
.L501:
.L502:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L521
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -336(%rbp)
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L522
.L521:
.L522:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L531
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -352(%rbp)
    movq $0, %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $8, %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -368(%rbp)
    movq $16, %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -376(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq $0, %rax
    movq %rax, -144(%rbp)
.L541:    movq -144(%rbp), %rax
    pushq %rax
    movq -368(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L542
    movq -144(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -392(%rbp)
    movq -376(%rbp), %rax
    pushq %rax
    movq -392(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -400(%rbp)
    movq $16, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -232(%rbp)
    movq $24, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $0, %rax
    movq %rax, -424(%rbp)
.L551:    movq -424(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L552
    movq -424(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq -424(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -424(%rbp)
    jmp .L551
.L552:
    movq -144(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -144(%rbp)
    jmp .L541
.L542:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L532
.L531:
.L532:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_get_expression_type
codegen_get_expression_type:
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
    jz .L561
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L562
.L561:
.L562:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L581
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L591
    movq $56, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq $48, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
.L601:    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L602
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -96(%rbp), %rax
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
    jz .L611
    movq $8, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L612
.L611:
.L612:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -72(%rbp)
    jmp .L601
.L602:
    jmp .L592
.L591:
.L592:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L582
.L581:
.L582:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -136(%rbp)
    movq $16, %rax
    pushq %rax
    movq -136(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L572
.L571:
.L572:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L621
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -152(%rbp)
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $8, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -168(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_get_expression_type
    movq %rax, -176(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L632
.L631:
.L632:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $32, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq $24, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    movq %rax, -208(%rbp)
    movq $0, %rax
    movq %rax, -216(%rbp)
.L641:    movq -216(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L642
    movq -216(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -232(%rbp)
    movq $0, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq -176(%rbp), %rax
    pushq %rax
    movq -240(%rbp), %rax
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
    jz .L651
    movq -232(%rbp), %rax
    movq %rax, -208(%rbp)
    movq -192(%rbp), %rax
    movq %rax, -216(%rbp)
    jmp .L652
.L651:
.L652:
    movq -216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -216(%rbp)
    jmp .L641
.L642:
    movq -208(%rbp), %rax
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
    movq $8, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L671
    movq -208(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -280(%rbp)
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -288(%rbp)
    movq $8, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -216(%rbp)
.L681:    movq -216(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L682
    movq -216(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -312(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq -312(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -320(%rbp)
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -328(%rbp), %rax
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
    jz .L691
    movq $8, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L692
.L691:
.L692:
    movq -216(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -216(%rbp)
    jmp .L681
.L682:
    jmp .L672
.L671:
.L672:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L622
.L621:
.L622:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_lvalue_address
codegen_generate_lvalue_address:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L701
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq $0, %rax
    movq %rax, -56(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L721
    movq $56, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq $48, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
.L731:    movq -88(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L732
    movq -88(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
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
    jz .L741
    movq $1, %rax
    movq %rax, -56(%rbp)
    movq -72(%rbp), %rax
    movq %rax, -88(%rbp)
    jmp .L742
.L741:
.L742:
    movq -88(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -88(%rbp)
    jmp .L731
.L732:
    jmp .L722
.L721:
.L722:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    movq $0, %rax
    pushq %rax
    leaq .STR6(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR7(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L752
.L751:
    leaq .STR8(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L752:
    jmp .L712
.L711:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -160(%rbp)
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR10(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR11(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L712:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L702
.L701:
.L702:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L761
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -176(%rbp)
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -184(%rbp)
    movq $8, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
    movq -184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_get_expression_type
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L771
    leaq .STR12(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L772
.L771:
.L772:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $32, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -216(%rbp)
    movq $24, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $0, %rax
    movq %rax, -232(%rbp)
    movq $0, %rax
    movq %rax, -240(%rbp)
.L781:    movq -240(%rbp), %rax
    pushq %rax
    movq -216(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L782
    movq -240(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -256(%rbp)
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
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
    jz .L791
    movq -256(%rbp), %rax
    movq %rax, -232(%rbp)
    movq -216(%rbp), %rax
    movq %rax, -240(%rbp)
    jmp .L792
.L791:
.L792:
    movq -240(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -240(%rbp)
    jmp .L781
.L782:
    movq -232(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L801
    leaq .STR13(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L802
.L801:
.L802:
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -296(%rbp)
    movq $8, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L811
    movq -232(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -312(%rbp)
    movq $0, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -320(%rbp)
    movq $8, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq $0, %rax
    movq %rax, -240(%rbp)
.L821:    movq -240(%rbp), %rax
    pushq %rax
    movq -320(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L822
    movq -240(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -296(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -352(%rbp)
    movq $0, %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq -360(%rbp), %rax
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
    jz .L831
    movq $16, %rax
    pushq %rax
    movq -352(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -296(%rbp)
    movq -320(%rbp), %rax
    movq %rax, -240(%rbp)
    jmp .L832
.L831:
.L832:
    movq -240(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -240(%rbp)
    jmp .L821
.L822:
    jmp .L812
.L811:
.L812:
    movq -296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L841
    leaq .STR14(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR15(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR9(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L842
.L841:
.L842:
    movq $0, %rax
    pushq %rax
    leaq .STR16(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -296(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR17(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L762
.L761:
.L762:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L851
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -392(%rbp)
    movq $0, %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -400(%rbp)
    movq $8, %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -408(%rbp)
    movq $0, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L861
    movq $8, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -424(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -160(%rbp)
    movq $24, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -464(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L881
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR18(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR19(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L882
.L881:
    movq -400(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
.L882:
    jmp .L872
.L871:
    movq -400(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
.L872:
    jmp .L862
.L861:
    movq -400(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
.L862:
    leaq .STR20(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -408(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR21(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR22(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR23(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L852
.L851:
.L852:
    leaq .STR24(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_integer_expr
codegen_generate_integer_expr:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR26(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_variable_expr
codegen_generate_variable_expr:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    movq $0, %rax
    movq %rax, -48(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L901
    movq $56, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -64(%rbp)
    movq $48, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
.L911:    movq -80(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L912
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
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
    jz .L921
    movq $1, %rax
    movq %rax, -48(%rbp)
    movq -104(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -64(%rbp), %rax
    movq %rax, -80(%rbp)
    jmp .L922
.L921:
.L922:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -80(%rbp)
    jmp .L911
.L912:
    jmp .L902
.L901:
.L902:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq $16, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L941
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -160(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L951
    movq $8, %rax
    pushq %rax
    movq -152(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -168(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR27(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L952
.L951:
.L952:
    jmp .L942
.L941:
.L942:
    movq $0, %rax
    pushq %rax
    leaq .STR28(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L932
.L931:
.L932:
    movq $0, %rax
    movq %rax, -176(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -184(%rbp)
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq $0, %rax
    movq %rax, -80(%rbp)
.L971:    movq -80(%rbp), %rax
    pushq %rax
    movq -184(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L972
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -216(%rbp)
    movq $0, %rax
    pushq %rax
    movq -216(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
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
    jz .L981
    movq $1, %rax
    movq %rax, -176(%rbp)
    movq -184(%rbp), %rax
    movq %rax, -80(%rbp)
    jmp .L982
.L981:
.L982:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -80(%rbp)
    jmp .L971
.L972:
    jmp .L962
.L961:
.L962:
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L991
    leaq .STR30(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L992
.L991:
.L992:
    movq $0, %rax
    pushq %rax
    leaq .STR6(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR31(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L892
.L891:
.L892:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -256(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -272(%rbp)
    movq $8, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -280(%rbp)
    movq $16, %rax
    pushq %rax
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq $0, %rax
    movq %rax, -296(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
    movq $32, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -312(%rbp)
    movq $24, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -320(%rbp)
    movq $0, %rax
    movq %rax, -328(%rbp)
.L1011:    movq -328(%rbp), %rax
    pushq %rax
    movq -312(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1012
    movq -328(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -336(%rbp)
    movq -336(%rbp), %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq $0, %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -352(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
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
    jz .L1021
    movq $8, %rax
    pushq %rax
    movq -344(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1031
    movq $1, %rax
    movq %rax, -296(%rbp)
    jmp .L1032
.L1031:
.L1032:
    movq -312(%rbp), %rax
    movq %rax, -328(%rbp)
    jmp .L1022
.L1021:
.L1022:
    movq -328(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -328(%rbp)
    jmp .L1011
.L1012:
    jmp .L1002
.L1001:
.L1002:
    movq -296(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1041
    movq $0, %rax
    pushq %rax
    leaq .STR10(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR32(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1042
.L1041:
    movq $0, %rax
    pushq %rax
    leaq .STR18(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR33(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L1042:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_emit_load_variable
codegen_emit_load_variable:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
    leaq .STR34(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1052
.L1051:
.L1052:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR18(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR33(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_emit_store_variable
codegen_emit_store_variable:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1061
    leaq .STR35(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1062
.L1061:
.L1062:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_integer_literal
codegen_generate_integer_literal:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR26(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_variable_handler
codegen_generate_variable_handler:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_variable_expr
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_string_literal
codegen_generate_string_literal:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1071
    leaq .STR38(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1072
.L1071:
.L1072:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L1081:    movq -64(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1082
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
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
    jz .L1091
    movq -64(%rbp), %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L1092
.L1091:
.L1092:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L1081
.L1082:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_string_literal
    movq %rax, -56(%rbp)
    jmp .L1102
.L1101:
.L1102:
    movq $0, %rax
    pushq %rax
    leaq .STR39(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR40(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_binary_op
codegen_generate_binary_op:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR21(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -48(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1111
    leaq .STR42(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1112
.L1111:
.L1112:
    movq -48(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    leaq .STR43(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR44(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1122
.L1121:
.L1122:
    movq -48(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1131
    leaq .STR45(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1132
.L1131:
.L1132:
    movq -48(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1141
    leaq .STR46(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR44(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR47(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR48(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR49(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR50(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR52(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -80(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR54(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR55(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -88(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L1142
.L1141:
.L1142:
    movq -48(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1151
    leaq .STR46(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR44(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR47(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR56(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR49(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR50(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR57(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR58(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR59(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -120(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR54(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR60(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -128(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L1152
.L1151:
.L1152:
    movq -48(%rbp), %rax
    pushq %rax
    movq $39, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1161
    leaq .STR61(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1162
.L1161:
.L1162:
    movq -48(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1171
    leaq .STR62(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1172
.L1171:
.L1172:
    movq -48(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1181
    leaq .STR63(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1182
.L1181:
.L1182:
    movq -48(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1191
    leaq .STR46(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR44(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR64(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1192
.L1191:
.L1192:
    movq -48(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1201
    leaq .STR46(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR44(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR65(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1202
.L1201:
.L1202:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_comparison
codegen_generate_comparison:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR21(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR66(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -48(%rbp), %rax
    pushq %rax
    movq $22, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1211
    leaq .STR67(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1212
.L1211:
.L1212:
    movq -48(%rbp), %rax
    pushq %rax
    movq $23, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    leaq .STR68(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1222
.L1221:
.L1222:
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1231
    leaq .STR69(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1232
.L1231:
.L1232:
    movq -48(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    leaq .STR70(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1242
.L1241:
.L1242:
    movq -48(%rbp), %rax
    pushq %rax
    movq $27, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1251
    leaq .STR71(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1252
.L1251:
.L1252:
    movq -48(%rbp), %rax
    pushq %rax
    movq $26, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1261
    leaq .STR72(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1262
.L1261:
.L1262:
    leaq .STR73(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_function_call
codegen_generate_function_call:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1271
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1272
.L1271:
.L1272:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -64(%rbp)
.L1281:    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1282
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1291
    leaq .STR74(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1292
.L1291:
.L1292:
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR75(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L1281
.L1282:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq $0, %rax
    pushq %rax
    leaq .STR76(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1302
.L1301:
.L1302:
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
    movq $0, %rax
    pushq %rax
    leaq .STR77(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1312
.L1311:
.L1312:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
    movq $0, %rax
    pushq %rax
    leaq .STR78(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1322
.L1321:
.L1322:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
    movq $0, %rax
    pushq %rax
    leaq .STR79(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1332
.L1331:
.L1332:
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq $0, %rax
    pushq %rax
    leaq .STR80(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1342
.L1341:
.L1342:
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1351
    movq $0, %rax
    pushq %rax
    leaq .STR81(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1352
.L1351:
.L1352:
    movq $0, %rax
    pushq %rax
    leaq .STR82(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rax, -96(%rbp)
    leaq .STR83(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1361
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1362
.L1361:
.L1362:
    leaq .STR84(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1371
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1372
.L1371:
.L1372:
    leaq .STR85(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1381
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1382
.L1381:
.L1382:
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1391
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1392
.L1391:
.L1392:
    leaq .STR87(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1401
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1402
.L1401:
.L1402:
    leaq .STR88(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1411
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1412
.L1411:
.L1412:
    leaq .STR89(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1421
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1422
.L1421:
.L1422:
    leaq .STR90(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1431
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1432
.L1431:
.L1432:
    leaq .STR91(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1441
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1442
.L1441:
.L1442:
    leaq .STR92(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1451
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1452
.L1451:
.L1452:
    leaq .STR93(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1461
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1462
.L1461:
.L1462:
    leaq .STR94(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1471
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1472
.L1471:
.L1472:
    leaq .STR95(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1481
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1482
.L1481:
.L1482:
    leaq .STR96(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1491
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1492
.L1491:
.L1492:
    leaq .STR97(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1501
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1502
.L1501:
.L1502:
    leaq .STR98(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1511
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1512
.L1511:
.L1512:
    leaq .STR99(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1521
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1522
.L1521:
.L1522:
    leaq .STR100(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1531
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1532
.L1531:
.L1532:
    leaq .STR101(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1541
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1542
.L1541:
.L1542:
    leaq .STR102(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1551
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1552
.L1551:
.L1552:
    leaq .STR103(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1561
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1562
.L1561:
.L1562:
    leaq .STR104(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1571
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1572
.L1571:
.L1572:
    leaq .STR105(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1581
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1582
.L1581:
.L1582:
    leaq .STR106(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1591
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1592
.L1591:
.L1592:
    leaq .STR107(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1601
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1602
.L1601:
.L1602:
    leaq .STR108(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1611
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1612
.L1611:
.L1612:
    leaq .STR109(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1621
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1622
.L1621:
.L1622:
    leaq .STR110(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1631
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1632
.L1631:
.L1632:
    leaq .STR111(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1641
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1642
.L1641:
.L1642:
    leaq .STR112(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1651
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1652
.L1651:
.L1652:
    leaq .STR113(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    jz .L1661
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1662
.L1661:
.L1662:
    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1671
    movq $0, %rax
    pushq %rax
    leaq .STR114(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1672
.L1671:
.L1672:
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_field_access
codegen_generate_field_access:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1681
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1691
    leaq .STR115(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1692
.L1691:
.L1692:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -88(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -88(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -96(%rbp)
    movq $8, %rax
    pushq %rax
    movq -96(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -104(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR18(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR33(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR116(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1682
.L1681:
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
    movq $0, %rax
    pushq %rax
    leaq .STR117(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR116(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L1682:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_builtin_call
codegen_generate_builtin_call:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq $8, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $16, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    leaq .STR118(%rip), %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -72(%rbp)
.L1701:    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1702
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR75(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -72(%rbp)
    jmp .L1701
.L1702:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1711
    movq $0, %rax
    pushq %rax
    leaq .STR76(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1712
.L1711:
.L1712:
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1721
    movq $0, %rax
    pushq %rax
    leaq .STR77(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1722
.L1721:
.L1722:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1731
    movq $0, %rax
    pushq %rax
    leaq .STR78(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1732
.L1731:
.L1732:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1741
    movq $0, %rax
    pushq %rax
    leaq .STR79(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1742
.L1741:
.L1742:
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1751
    movq $0, %rax
    pushq %rax
    leaq .STR80(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1752
.L1751:
.L1752:
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1761
    movq $0, %rax
    pushq %rax
    leaq .STR81(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1762
.L1761:
.L1762:
    movq $0, %rax
    pushq %rax
    leaq .STR119(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR120(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_expression
codegen_generate_expression:
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
    jz .L1771
    leaq .STR121(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1772
.L1771:
.L1772:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1781
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR26(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1782
.L1781:
.L1782:
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1791
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_variable_expr
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1792
.L1791:
.L1792:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1801
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_binary_op
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1802
.L1801:
.L1802:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1811
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_comparison
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1812
.L1811:
.L1812:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1821
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_function_call
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1822
.L1821:
.L1822:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1831
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_string_literal
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1832
.L1831:
.L1832:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1841
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_field_access
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1842
.L1841:
.L1842:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1851
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1852
.L1851:
.L1852:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1861
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -56(%rbp)
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -72(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -80(%rbp)
.L1871:    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1872
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -96(%rbp)
    movq -96(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR75(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -80(%rbp)
    jmp .L1871
.L1872:
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1881
    movq $0, %rax
    pushq %rax
    leaq .STR76(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1882
.L1881:
.L1882:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1891
    movq $0, %rax
    pushq %rax
    leaq .STR77(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1892
.L1891:
.L1892:
    movq -72(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1901
    movq $0, %rax
    pushq %rax
    leaq .STR78(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1902
.L1901:
.L1902:
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    movq %rax, -120(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $57, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1911
    leaq .STR87(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1912
.L1911:
.L1912:
    movq -112(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1921
    leaq .STR88(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1922
.L1921:
.L1922:
    movq -112(%rbp), %rax
    pushq %rax
    movq $59, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1931
    leaq .STR92(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1932
.L1931:
.L1932:
    movq -112(%rbp), %rax
    pushq %rax
    movq $60, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1941
    leaq .STR89(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1942
.L1941:
.L1942:
    movq -112(%rbp), %rax
    pushq %rax
    movq $61, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1951
    leaq .STR96(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1952
.L1951:
.L1952:
    movq -112(%rbp), %rax
    pushq %rax
    movq $62, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1961
    leaq .STR97(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1962
.L1961:
.L1962:
    movq -112(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1971
    leaq .STR98(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1972
.L1971:
.L1972:
    movq -112(%rbp), %rax
    pushq %rax
    movq $72, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1981
    leaq .STR91(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1982
.L1981:
.L1982:
    movq -112(%rbp), %rax
    pushq %rax
    movq $73, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1991
    leaq .STR90(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L1992
.L1991:
.L1992:
    movq -112(%rbp), %rax
    pushq %rax
    movq $74, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2001
    leaq .STR94(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2002
.L2001:
.L2002:
    movq -112(%rbp), %rax
    pushq %rax
    movq $75, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2011
    leaq .STR93(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2012
.L2011:
.L2012:
    movq -112(%rbp), %rax
    pushq %rax
    movq $76, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2021
    leaq .STR95(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2022
.L2021:
.L2022:
    movq -112(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2031
    leaq .STR83(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2032
.L2031:
.L2032:
    movq -112(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2041
    leaq .STR84(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2042
.L2041:
.L2042:
    movq -112(%rbp), %rax
    pushq %rax
    movq $130, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2051
    leaq .STR102(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2052
.L2051:
.L2052:
    movq -112(%rbp), %rax
    pushq %rax
    movq $131, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    leaq .STR103(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2062
.L2061:
.L2062:
    movq $0, %rax
    pushq %rax
    leaq .STR82(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2071
    movq $0, %rax
    pushq %rax
    leaq .STR122(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2072
.L2071:
    movq $0, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR114(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2072:
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L1862
.L1861:
.L1862:
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2081
    movq $0, %rax
    pushq %rax
    leaq .STR123(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2082
.L2081:
.L2082:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2091
    movq -16(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -256(%rbp)
    movq $0, %rax
    pushq %rax
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR6(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR40(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2092
.L2091:
.L2092:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2101
    movq $0, %rax
    pushq %rax
    leaq .STR123(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2102
.L2101:
.L2102:
    leaq .STR124(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_statement
codegen_generate_statement:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -32(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2111
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2121
    movq $0, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2131
    movq $8, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $32, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq $40, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    movq %rax, -96(%rbp)
    movq $0, %rax
    movq %rax, -104(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2141:    movq -112(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2142
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $0, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq -128(%rbp), %rax
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
    jz .L2151
    movq $1, %rax
    movq %rax, -96(%rbp)
    movq -120(%rbp), %rax
    movq %rax, -104(%rbp)
    movq -80(%rbp), %rax
    movq %rax, -112(%rbp)
    jmp .L2152
.L2151:
.L2152:
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -112(%rbp)
    jmp .L2141
.L2142:
    movq -96(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2161
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2162
.L2161:
.L2162:
    movq -64(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -168(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -184(%rbp)
    movq $8, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq $16, %rax
    pushq %rax
    movq -104(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2171
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2181:    movq -112(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2182
    movq $0, %rax
    pushq %rax
    leaq .STR125(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR126(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -112(%rbp)
    jmp .L2181
.L2182:
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L2172
.L2171:
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2191:    movq -112(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2192
    movq $0, %rax
    pushq %rax
    leaq .STR125(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -112(%rbp)
    jmp .L2191
.L2192:
.L2172:
    jmp .L2132
.L2131:
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2201
    movq -48(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -248(%rbp)
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq $0, %rax
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2211
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2212
.L2211:
.L2212:
    movq -256(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2221
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2222
.L2221:
.L2222:
    movq -256(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2231
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2232
.L2231:
.L2232:
    movq -256(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2241
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2242
.L2241:
.L2242:
    movq -256(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2251
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2252
.L2251:
.L2252:
    movq -256(%rbp), %rax
    pushq %rax
    movq $54, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2261
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2262
.L2261:
.L2262:
    movq -264(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2271
    leaq .STR127(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
    jmp .L2272
.L2271:
    movq $0, %rax
    movq %rax, -320(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2281
    movq $1, %rax
    movq %rax, -320(%rbp)
    jmp .L2282
.L2281:
.L2282:
    movq -256(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2291
    movq $1, %rax
    movq %rax, -320(%rbp)
    jmp .L2292
.L2291:
.L2292:
    movq -256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2301
    movq $1, %rax
    movq %rax, -320(%rbp)
    jmp .L2302
.L2301:
.L2302:
    movq -320(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2311
    leaq .STR128(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
    jmp .L2312
.L2311:
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_variable
.L2312:
.L2272:
    jmp .L2202
.L2201:
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_variable
.L2202:
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -168(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2132:
    jmp .L2122
.L2121:
.L2122:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2112
.L2111:
.L2112:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2321
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -376(%rbp)
    movq -376(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
    leaq .STR129(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR130(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2322
.L2321:
.L2322:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2331
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR131(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR132(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2332
.L2331:
.L2332:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2341
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    movq %rax, -408(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -408(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -416(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -424(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR134(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR135(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -440(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -448(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -456(%rbp)
    movq $0, %rax
    movq %rax, -464(%rbp)
.L2351:    movq -464(%rbp), %rax
    pushq %rax
    movq -456(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2352
    movq -464(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -472(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -464(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -464(%rbp)
    jmp .L2351
.L2352:
    movq $0, %rax
    pushq %rax
    leaq .STR136(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR137(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -488(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -496(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -488(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -512(%rbp)
    movq $0, %rax
    movq %rax, -520(%rbp)
.L2361:    movq -520(%rbp), %rax
    pushq %rax
    movq -512(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2362
    movq -520(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -504(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -528(%rbp)
    movq -528(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -520(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -520(%rbp)
    jmp .L2361
.L2362:
    movq -424(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR137(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -544(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -552(%rbp)
    movq -552(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -552(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2342
.L2341:
.L2342:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2371
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq $1000000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2381
    jmp .L2382
.L2381:
.L2382:
    movq -400(%rbp), %rax
    movq %rax, -408(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -408(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -576(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -584(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq -576(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_push_loop_context
    movq $0, %rax
    pushq %rax
    leaq .STR137(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -576(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, -592(%rbp)
    movq $0, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR134(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR135(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -440(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -616(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -624(%rbp)
    movq $0, %rax
    movq %rax, -632(%rbp)
.L2391:    movq -632(%rbp), %rax
    pushq %rax
    movq -624(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2392
    movq -632(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -616(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -640(%rbp)
    movq -640(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -632(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -632(%rbp)
    jmp .L2391
.L2392:
    movq $0, %rax
    pushq %rax
    leaq .STR136(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -576(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR137(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -656(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -664(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -664(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_pop_loop_context
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2372
.L2371:
.L2372:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2401
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    movq %rax, -408(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -408(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -576(%rbp)
    movq -408(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -584(%rbp)
    movq -584(%rbp), %rax
    pushq %rax
    movq -576(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_push_loop_context
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -704(%rbp)
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -712(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -720(%rbp)
    movq -720(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq -704(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_emit_store_variable
    movq $0, %rax
    pushq %rax
    leaq .STR137(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -576(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, -592(%rbp)
    movq $0, %rax
    pushq %rax
    movq -592(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -704(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_emit_load_variable
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -736(%rbp)
    movq -736(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR138(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR129(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR139(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR140(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -744(%rbp)
    movq -744(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -744(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -752(%rbp)
    movq $48, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -760(%rbp)
    movq $0, %rax
    movq %rax, -768(%rbp)
.L2411:    movq -768(%rbp), %rax
    pushq %rax
    movq -760(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2412
    movq -768(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -752(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -776(%rbp)
    movq -776(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -768(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    leaq -768(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2411
.L2412:
    movq -704(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_emit_load_variable
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -784(%rbp)
    movq -784(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2421
    leaq .STR141(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L2422
.L2421:
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -784(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR138(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR129(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR142(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
.L2422:
    movq -704(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_emit_store_variable
    movq $0, %rax
    pushq %rax
    leaq .STR136(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -576(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR137(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -656(%rbp)
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -664(%rbp)
    movq -664(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -664(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -592(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_pop_loop_context
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2402
.L2401:
.L2402:
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2431
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_current_loop_context
    movq %rax, -808(%rbp)
    movq -808(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2441
    movq $8, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -816(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR136(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -816(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2442
.L2441:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L2442:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2432
.L2431:
.L2432:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2451
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_current_loop_context
    movq %rax, -808(%rbp)
    movq -808(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2461
    movq $0, %rax
    pushq %rax
    movq -808(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -832(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR136(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -832(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2462
.L2461:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L2462:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2452
.L2451:
.L2452:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -840(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -848(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2481:    movq -112(%rbp), %rax
    pushq %rax
    movq -840(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2482
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -848(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -864(%rbp)
    movq -864(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_length@PLT
    movq %rax, -872(%rbp)
    movq -872(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -880(%rbp)
    movq $0, %rax
    movq %rax, -888(%rbp)
    movq $0, %rax
    movq %rax, -896(%rbp)
.L2491:    movq -888(%rbp), %rax
    pushq %rax
    movq -872(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2492
    movq -888(%rbp), %rax
    pushq %rax
    movq -864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -904(%rbp)
    movq -904(%rbp), %rax
    pushq %rax
    movq $92, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
    movq -888(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -872(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2511
    movq -888(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -864(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -912(%rbp)
    movq -912(%rbp), %rax
    pushq %rax
    movq $110, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2521
    movq -888(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -888(%rbp)
    jmp .L2522
.L2521:
    movq -912(%rbp), %rax
    pushq %rax
    movq $116, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2531
    movq $9, %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -888(%rbp)
    jmp .L2532
.L2531:
    movq -912(%rbp), %rax
    pushq %rax
    movq $92, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    movq $92, %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -888(%rbp)
    jmp .L2542
.L2541:
    movq -904(%rbp), %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -888(%rbp)
.L2542:
.L2532:
.L2522:
    jmp .L2512
.L2511:
    movq -904(%rbp), %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -888(%rbp)
.L2512:
    jmp .L2502
.L2501:
    movq -904(%rbp), %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq -896(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -896(%rbp)
    movq -888(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -888(%rbp)
.L2502:
    jmp .L2491
.L2492:
    movq $0, %rax
    pushq %rax
    movq -896(%rbp), %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -112(%rbp)
    jmp .L2481
.L2482:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2472
.L2471:
.L2472:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2551
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1016(%rbp)
    movq -1016(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    movq -1016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2561
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR144(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2562
.L2561:
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
    movq -1016(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -248(%rbp)
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -256(%rbp)
    movq $0, %rax
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2581
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2582
.L2581:
.L2582:
    movq -256(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2591
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2592
.L2591:
.L2592:
    movq -256(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2601
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2602
.L2601:
.L2602:
    movq -256(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2611
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2612
.L2611:
.L2612:
    movq -256(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2621
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2622
.L2621:
.L2622:
    movq -256(%rbp), %rax
    pushq %rax
    movq $54, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2631
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2632
.L2631:
.L2632:
    movq -264(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR144(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2642
.L2641:
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR145(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2642:
    jmp .L2572
.L2571:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    movq $8, %rax
    pushq %rax
    movq -1016(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2671
    leaq .STR127(%rip), %rax
    pushq %rax
    movq -64(%rbp), %rax
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
    jz .L2681
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR144(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2682
.L2681:
    leaq .STR128(%rip), %rax
    pushq %rax
    movq -64(%rbp), %rax
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
    jz .L2691
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR145(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2692
.L2691:
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR145(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2692:
.L2682:
    jmp .L2672
.L2671:
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR145(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2672:
    jmp .L2662
.L2661:
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR145(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2662:
    jmp .L2652
.L2651:
    movq $0, %rax
    pushq %rax
    leaq .STR143(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR145(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2652:
.L2572:
.L2562:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2552
.L2551:
.L2552:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1136(%rbp)
    movq -1136(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2702
.L2701:
.L2702:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2711
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2712
.L2711:
.L2712:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2721
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1144(%rbp)
    movq -1144(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR146(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    movq %rax, -1160(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1160(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR147(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -424(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1176(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1184(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2731:    movq -112(%rbp), %rax
    pushq %rax
    movq -1176(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2732
    movq -112(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1200(%rbp)
    movq -1184(%rbp), %rax
    pushq %rax
    movq -1200(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1208(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1216(%rbp)
    movq $8, %rax
    pushq %rax
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1224(%rbp)
    movq $16, %rax
    pushq %rax
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1232(%rbp)
    movq $24, %rax
    pushq %rax
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1240(%rbp)
    movq $32, %rax
    pushq %rax
    movq -1208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1248(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR149(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    movq -1160(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    leaq .STR148(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -1256(%rbp)
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1264(%rbp)
    movq -1264(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR149(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    movq -1160(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    pushq %rax
    leaq .STR148(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -1272(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1256(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR150(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR151(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR152(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR153(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR154(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1216(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq -1176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2741
    movq $0, %rax
    pushq %rax
    leaq .STR155(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1272(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR156(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2742
.L2741:
    movq $0, %rax
    pushq %rax
    leaq .STR155(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR157(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2742:
    movq -1224(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2751
    movq $0, %rax
    pushq %rax
    leaq .STR158(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR151(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rax, -1280(%rbp)
.L2761:    movq -1280(%rbp), %rax
    pushq %rax
    movq -1224(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2762
    movq -1280(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1288(%rbp)
    movq $8, %rax
    pushq %rax
    movq -1288(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1296(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR28(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1296(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR159(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1280(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1312(%rbp)
    movq -1312(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR160(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1312(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -1280(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1320(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR161(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1320(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR162(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1328(%rbp)
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1336(%rbp)
    movq -1328(%rbp), %rax
    pushq %rax
    movq -1336(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2771
    movq -1336(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1344(%rbp)
    movq -1344(%rbp), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -1344(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call reallocate
    movq %rax, -1360(%rbp)
    movq -1360(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L2772
.L2771:
.L2772:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -1328(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1376(%rbp)
    movq -1320(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq -1376(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1312(%rbp), %rax
    pushq %rax
    movq -1376(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq -1376(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1328(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1280(%rbp)
    jmp .L2761
.L2762:
    jmp .L2752
.L2751:
.L2752:
    movq $0, %rax
    movq %rax, -1392(%rbp)
.L2781:    movq -1392(%rbp), %rax
    pushq %rax
    movq -1240(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2782
    movq -1392(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1248(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1400(%rbp)
    movq -1400(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -1392(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1392(%rbp)
    jmp .L2781
.L2782:
    movq -1224(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2791
    movq $0, %rax
    movq %rax, -1280(%rbp)
.L2801:    movq -1280(%rbp), %rax
    pushq %rax
    movq -1224(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2802
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1328(%rbp)
    movq -1328(%rbp), %rax
    pushq %rax
    movq -1224(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    pushq %rax
    movq -1280(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1432(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -1432(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -704(%rbp)
    movq -1432(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1456(%rbp)
    movq -704(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1456(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1280(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -1280(%rbp)
    jmp .L2801
.L2802:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1328(%rbp)
    movq -1328(%rbp), %rax
    pushq %rax
    movq -1224(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L2792
.L2791:
.L2792:
    movq $0, %rax
    pushq %rax
    leaq .STR163(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -112(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -112(%rbp)
    jmp .L2731
.L2732:
    movq $0, %rax
    pushq %rax
    movq -424(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR164(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2722
.L2721:
.L2722:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_create
codegen_create:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $80, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -16(%rbp)
    movq $1, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call file_open_buffered@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2811
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2812
.L2811:
.L2812:
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq $256, %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $256, %rax
    pushq %rax
    movq $20, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $2048, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $2048, %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $48, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq $64, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax
    pushq %rax
    movq $68, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $16, %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $56, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2821
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2822
.L2821:
.L2822:
    movq -16(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_destroy
codegen_destroy:
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
    jz .L2831
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2841
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call file_close_fd
    jmp .L2842
.L2841:
.L2842:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    movq $17, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -32(%rbp)
    movq $18, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq $19, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $256, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $65536, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -64(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $16777216, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -80(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2851
    movq $0, %rax
    movq %rax, -96(%rbp)
.L2861:    movq -96(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2862
    movq -96(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $16, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2871
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2872
.L2871:
.L2872:
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2881
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2882
.L2881:
.L2882:
    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -96(%rbp)
    jmp .L2861
.L2862:
    jmp .L2852
.L2851:
.L2852:
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -24(%rbp)
    movq $41, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -32(%rbp)
    movq $42, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq $43, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $256, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $65536, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -64(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $16777216, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -72(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -200(%rbp)
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2891
    movq $0, %rax
    movq %rax, -96(%rbp)
.L2901:    movq -96(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2902
    movq -96(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -224(%rbp)
    movq -208(%rbp), %rax
    pushq %rax
    movq -224(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -232(%rbp)
    movq $0, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -240(%rbp)
    movq $8, %rax
    pushq %rax
    movq -232(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2911
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2912
.L2911:
.L2912:
    movq -248(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2921
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2922
.L2921:
.L2922:
    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -96(%rbp)
    jmp .L2901
.L2902:
    jmp .L2892
.L2891:
.L2892:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2931
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2932
.L2931:
.L2932:
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2941
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2942
.L2941:
.L2942:
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
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
    jz .L2951
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2952
.L2951:
.L2952:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L2832
.L2831:
.L2832:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_push_loop_context
codegen_push_loop_context:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq %rdx, -24(%rbp)
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq $68, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -40(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2961
    movq -40(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq $68, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $16, %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_reallocate@PLT
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L2962
.L2961:
.L2962:
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -24(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -32(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_pop_loop_context
codegen_pop_loop_context:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2971
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    pushq %rax
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L2972
.L2971:
.L2972:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_current_loop_context
codegen_current_loop_context:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2981
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2982
.L2981:
.L2982:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_function
codegen_generate_function:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq $0, %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR166(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR167(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR168(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $6, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -40(%rbp)
    leaq .STR169(%rip), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR170(%rip), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR171(%rip), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR172(%rip), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR173(%rip), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR174(%rip), %rax
    pushq %rax
    movq $40, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $6, %rax
    movq %rax, -48(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    leaq .STR175(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
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
    jz .L2991
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3001
    leaq .STR176(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR177(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR179(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR180(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR181(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3002
.L3001:
.L3002:
    jmp .L2992
.L2991:
.L2992:
    leaq .STR182(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $0, %rax
    movq %rax, -72(%rbp)
    movq $1, %rax
    movq %rax, -80(%rbp)
.L3011:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3012
    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3021
    movq $0, %rax
    movq %rax, -80(%rbp)
    jmp .L3022
.L3021:
.L3022:
    movq -72(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3031
    movq $0, %rax
    movq %rax, -80(%rbp)
    jmp .L3032
.L3031:
.L3032:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3041
    movq -72(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -120(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3051
    leaq .STR1(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L3052
.L3051:
.L3052:
    movq $1, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call codegen_add_variable_with_type_and_param_flag
    movq %rax, -136(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -160(%rbp)
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR28(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR183(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR37(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -72(%rbp)
    jmp .L3042
.L3041:
.L3042:
    jmp .L3011
.L3012:
    movq -48(%rbp), %rax
    movq %rax, -72(%rbp)
.L3061:    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3062
    movq -72(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq $1, %rax
    pushq %rax
    movq -120(%rbp), %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    call codegen_add_variable_with_type_and_param_flag
    movq %rax, -136(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -136(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -152(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -160(%rbp)
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    subq %rax, %rbx
    movq %rbx, %rax
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq $16, %rax
    pushq %rax
    movq -272(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -280(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR28(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR33(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -168(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR184(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -72(%rbp)
    jmp .L3061
.L3062:
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -296(%rbp)
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
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
    jz .L3071
    movq $0, %rax
    movq %rax, -312(%rbp)
.L3081:    movq -312(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3082
    movq -312(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3091
    movq -328(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    jmp .L3092
.L3091:
.L3092:
    movq -312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -312(%rbp)
    jmp .L3081
.L3082:
    jmp .L3072
.L3071:
.L3072:
    leaq .STR185(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR186(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR187(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate
codegen_generate:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq %rsi, -16(%rbp)
    movq -16(%rbp), %rax
    pushq %rax
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq $0, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -24(%rbp)
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3101
    jmp .L3102
.L3101:
.L3102:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3111
    movq $0, %rax
    movq %rax, -32(%rbp)
    jmp .L3112
.L3111:
.L3112:
    movq -32(%rbp), %rax
    pushq %rax
    movq $1000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3121
    movq $0, %rax
    movq %rax, -32(%rbp)
    jmp .L3122
.L3121:
.L3122:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3131
    movq $0, %rax
    pushq %rax
    leaq .STR188(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3141:    movq -64(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3142
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -72(%rbp)
    movq $0, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -80(%rbp)
    movq $8, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR189(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3141
.L3142:
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3132
.L3131:
.L3132:
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3151
    movq $0, %rax
    movq %rax, -104(%rbp)
    jmp .L3152
.L3151:
.L3152:
    movq -104(%rbp), %rax
    pushq %rax
    movq $10000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3161
    movq $0, %rax
    movq %rax, -104(%rbp)
    jmp .L3162
.L3161:
.L3162:
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3171
    leaq .STR191(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3172
.L3171:
.L3172:
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3181:    movq -64(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3182
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3191
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    movq $32, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -160(%rbp)
    movq $40, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -160(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3201
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3211
    movq $0, %rax
    movq %rax, -176(%rbp)
.L3221:    movq -176(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3222
    movq -176(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -184(%rbp)
    movq -184(%rbp), %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq $0, %rax
    movq %rax, -200(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3231
    movq -192(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3241
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3242
.L3241:
.L3242:
    jmp .L3232
.L3231:
.L3232:
    movq -176(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -176(%rbp)
    jmp .L3221
.L3222:
    jmp .L3212
.L3211:
.L3212:
    jmp .L3202
.L3201:
.L3202:
    jmp .L3192
.L3191:
.L3192:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3181
.L3182:
    movq $40, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -232(%rbp)
    movq $41, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -240(%rbp)
    movq $42, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -248(%rbp)
    movq $43, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -256(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $256, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -264(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq $65536, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $16777216, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -280(%rbp)
    movq -232(%rbp), %rax
    pushq %rax
    movq -264(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -272(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -280(%rbp), %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3251
    movq $0, %rax
    movq %rax, -288(%rbp)
    jmp .L3252
.L3251:
.L3252:
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_integer
    movq -288(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3261
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $32, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -304(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3271:    movq -64(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3272
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    addq %rbx, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -320(%rbp)
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR193(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $2, %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -336(%rbp)
    movq $34, %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -328(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3271
.L3272:
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3262
.L3261:
.L3262:
    movq $56, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -352(%rbp)
    movq $48, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq $0, %rax
    movq %rax, -368(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3281:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3282
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq $16, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3291
    movq $1, %rax
    movq %rax, -368(%rbp)
    movq -352(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L3292
.L3291:
.L3292:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3281
.L3282:
    movq -368(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3301
    leaq .STR194(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3311:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3312
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq $0, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -440(%rbp)
    movq $16, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3321
    movq $0, %rax
    pushq %rax
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -456(%rbp)
    movq -456(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3331
    movq $8, %rax
    pushq %rax
    movq -392(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -464(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR195(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3332
.L3331:
    movq $0, %rax
    pushq %rax
    leaq .STR196(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3332:
    jmp .L3322
.L3321:
.L3322:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3311
.L3312:
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3302
.L3301:
.L3302:
    movq $0, %rax
    movq %rax, -480(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3341:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3342
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq $16, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3351
    movq $1, %rax
    movq %rax, -480(%rbp)
    movq -352(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L3352
.L3351:
.L3352:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3341
.L3342:
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3361
    leaq .STR197(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3371:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3372
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -384(%rbp)
    movq $0, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -440(%rbp)
    movq $16, %rax
    pushq %rax
    movq -384(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -392(%rbp)
    movq -392(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3381
    movq $0, %rax
    pushq %rax
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR198(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3382
.L3381:
.L3382:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3371
.L3372:
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3362
.L3361:
.L3362:
    leaq .STR199(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR200(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR167(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR168(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR201(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR202(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR203(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR204(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR205(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR206(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR207(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR208(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR209(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR210(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR211(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR212(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR213(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR214(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR215(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR216(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR217(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR218(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR213(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR219(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR220(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR216(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR217(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR186(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR187(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR221(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR167(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR168(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR222(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR223(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR224(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR225(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR226(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR227(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR228(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR229(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR134(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR230(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR231(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR232(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR233(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR134(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR234(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR46(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR235(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR236(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR237(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR238(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR239(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR228(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR240(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR241(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR242(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR201(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR243(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR204(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR244(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR206(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR245(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR208(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR209(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR246(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR247(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR212(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR213(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR248(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR215(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR216(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR217(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR218(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR213(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR219(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR220(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR216(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR217(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR118(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR185(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR186(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR187(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR249(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR250(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR199(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3391:    movq -64(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3392
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3401
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    leaq .STR175(%rip), %rax
    pushq %rax
    movq -152(%rbp), %rax
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
    jz .L3411
    leaq .STR251(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3412
.L3411:
.L3412:
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -144(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_function
    jmp .L3402
.L3401:
.L3402:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3391
.L3392:
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L3421:    movq -64(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3422
    movq -64(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -144(%rbp)
    movq -144(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3431
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    leaq .STR175(%rip), %rax
    pushq %rax
    movq -152(%rbp), %rax
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
    jz .L3441
    movq $1, %rax
    movq %rax, -608(%rbp)
    movq -104(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L3442
.L3441:
.L3442:
    jmp .L3432
.L3431:
.L3432:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    addq %rbx, %rax
    movq %rax, -64(%rbp)
    jmp .L3421
.L3422:
    movq $0, %rax
    pushq %rax
    leaq .STR0(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR252(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    movq %rbp, %rsp
    popq %rbp
    ret

.section .note.GNU-stack
