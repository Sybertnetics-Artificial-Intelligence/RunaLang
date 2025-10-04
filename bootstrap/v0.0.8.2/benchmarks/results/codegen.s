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
.STR12:    .string "[CODEGEN ERROR] Unknown variable in field access"
.STR13:    .string "    movq -"
.STR14:    .string "(%rbp), %rbx  # Load struct pointer\n"
.STR15:    .string "    movq %rax, %rbx  # Use expression result as pointer\n"
.STR16:    .string "[CODEGEN ERROR] Cannot determine type of object in field access"
.STR17:    .string "[CODEGEN ERROR] Unknown type '"
.STR18:    .string "[CODEGEN ERROR] Type '"
.STR19:    .string "' has no field '"
.STR20:    .string "    addq $"
.STR21:    .string ", %rbx\n"
.STR22:    .string "(%rbp), %rbx  # Load array parameter pointer"
.STR23:    .string "    pushq %rbx"
.STR24:    .string "    popq %rbx"
.STR25:    .string "    imulq $8, %rax"
.STR26:    .string "    addq %rax, %rbx"
.STR27:    .string "[CODEGEN ERROR] Invalid lvalue expression type"
.STR28:    .string "    movq $"
.STR29:    .string ", %rax\n"
.STR30:    .string ", %rax  # Load compile-time constant "
.STR31:    .string "    movq "
.STR32:    .string "(%rip), %rax  # Load global variable\n"
.STR33:    .string "[CODEGEN ERROR] Undefined variable: "
.STR34:    .string "(%rip), %rax  # Load function address\n"
.STR35:    .string "(%rbp), %rax  # Load array address\n"
.STR36:    .string "(%rbp), %rax\n"
.STR37:    .string "[CODEGEN ERROR] Invalid string literal expression"
.STR38:    .string "    leaq .STR"
.STR39:    .string "(%rip), %rax\n"
.STR40:    .string "    addq -"
.STR41:    .string "    pushq %rax"
.STR42:    .string "    addq %rbx, %rax"
.STR43:    .string "    subq $"
.STR44:    .string "    subq -"
.STR45:    .string "    subq %rax, %rbx"
.STR46:    .string "    movq %rbx, %rax"
.STR47:    .string "    imulq %rbx, %rax"
.STR48:    .string "    movq %rax, %rcx"
.STR49:    .string "    popq %rax"
.STR50:    .string "    testq %rcx, %rcx"
.STR51:    .string "    jz .Ldiv_by_zero_"
.STR52:    .string "    cqto"
.STR53:    .string "    idivq %rcx"
.STR54:    .string "    jmp .Ldiv_done_"
.STR55:    .string ".Ldiv_by_zero_"
.STR56:    .string ":\n"
.STR57:    .string "    movq $0, %rax"
.STR58:    .string ".Ldiv_done_"
.STR59:    .string "    jz .Lmod_by_zero_"
.STR60:    .string "    movq %rdx, %rax"
.STR61:    .string "    jmp .Lmod_done_"
.STR62:    .string ".Lmod_by_zero_"
.STR63:    .string ".Lmod_done_"
.STR64:    .string "    andq $"
.STR65:    .string "    andq %rbx, %rax"
.STR66:    .string "    orq $"
.STR67:    .string "    orq %rbx, %rax"
.STR68:    .string "    xorq $"
.STR69:    .string "    xorq %rbx, %rax"
.STR70:    .string "    salq %cl, %rax"
.STR71:    .string "    sarq %cl, %rax"
.STR72:    .string "    testq %rax, %rax"
.STR73:    .string "    setz %al"
.STR74:    .string "    movzbq %al, %rax"
.STR75:    .string "    cmpq %rax, %rbx"
.STR76:    .string "    sete %al"
.STR77:    .string "    setne %al"
.STR78:    .string "    setl %al"
.STR79:    .string "    setg %al"
.STR80:    .string "    setle %al"
.STR81:    .string "    setge %al"
.STR82:    .string "[CODEGEN ERROR] NULL argument expression pointer: "
.STR83:    .string "    pushq %rax\n"
.STR84:    .string "    popq %rdi\n"
.STR85:    .string "    popq %rsi\n"
.STR86:    .string "    popq %rdx\n"
.STR87:    .string "    popq %rcx\n"
.STR88:    .string "    popq %r8\n"
.STR89:    .string "    popq %r9\n"
.STR90:    .string "    call "
.STR91:    .string "allocate"
.STR92:    .string "deallocate"
.STR93:    .string "memory_allocate"
.STR94:    .string "memory_reallocate"
.STR95:    .string "string_length"
.STR96:    .string "string_char_at"
.STR97:    .string "string_equals"
.STR98:    .string "string_compare"
.STR99:    .string "string_find"
.STR100:    .string "string_substring"
.STR101:    .string "string_duplicate"
.STR102:    .string "string_concat"
.STR103:    .string "integer_to_string"
.STR104:    .string "ascii_value_of"
.STR105:    .string "is_digit"
.STR106:    .string "is_whitespace"
.STR107:    .string "file_open_buffered"
.STR108:    .string "file_write_buffered"
.STR109:    .string "file_close_buffered"
.STR110:    .string "memory_get_byte"
.STR111:    .string "memory_set_byte"
.STR112:    .string "memory_get_int32"
.STR113:    .string "memory_set_int32"
.STR114:    .string "memory_get_integer"
.STR115:    .string "memory_set_integer"
.STR116:    .string "memory_get_pointer"
.STR117:    .string "memory_set_pointer"
.STR118:    .string "memory_set_pointer_at_index"
.STR119:    .string "exit_with_code"
.STR120:    .string "read_file_internal"
.STR121:    .string "get_command_line_arg"
.STR122:    .string "@PLT"
.STR123:    .string "    pushq %rdi\n"
.STR124:    .string "    pushq %rsi\n"
.STR125:    .string "    pushq %rdx\n"
.STR126:    .string "    pushq %rcx\n"
.STR127:    .string "    pushq %r8\n"
.STR128:    .string "    pushq %r9\n"
.STR129:    .string "    movq %rax, %r10  # Save function pointer\n"
.STR130:    .string "    call *%r10  # Indirect call through function pointer\n"
.STR131:    .string "[CODEGEN ERROR] Unknown variable"
.STR132:    .string "(%rax), %rax\n"
.STR133:    .string ""
.STR134:    .string "    # Unimplemented builtin type "
.STR135:    .string "    movq $0, %rax  # Placeholder return value\n"
.STR136:    .string "[CODEGEN ERROR] NULL expression pointer"
.STR137:    .string "unknown_builtin_"
.STR138:    .string "    movq $0, %rax\n"
.STR139:    .string "    pushq %rax  # Save index\n"
.STR140:    .string "    popq %rbx  # Load index\n"
.STR141:    .string "    imulq $8, %rbx  # Multiply index by 8\n"
.STR142:    .string "    addq %rbx, %rax  # Add offset to array pointer\n"
.STR143:    .string "    movq (%rax), %rax  # Load value from array\n"
.STR144:    .string ", %rdi\n"
.STR145:    .string "    call memory_allocate\n"
.STR146:    .string "    pushq %rax  # Save list pointer\n"
.STR147:    .string "    movq (%rsp), %rbx  # Load list pointer\n"
.STR148:    .string "    movq %rax, "
.STR149:    .string "(%rbx)\n"
.STR150:    .string "    popq %rax  # List pointer as result\n"
.STR151:    .string "    pushq %rax  # Save array pointer\n"
.STR152:    .string "    movq (%rsp), %rbx  # Load array pointer\n"
.STR153:    .string "    popq %rax  # Array pointer as result\n"
.STR154:    .string "[CODEGEN ERROR] Unknown struct type '"
.STR155:    .string "    call allocate@PLT\n"
.STR156:    .string "    pushq %rax  # Save struct pointer\n"
.STR157:    .string "[CODEGEN ERROR] Unknown field '"
.STR158:    .string "' in struct '"
.STR159:    .string "    movq (%rsp), %rbx  # Load struct pointer\n"
.STR160:    .string "(%rbx)  # Store field value\n"
.STR161:    .string "    popq %rax  # Struct pointer as result\n"
.STR162:    .string "[CODEGEN ERROR] Unsupported expression type"
.STR163:    .string "    movq $0, -"
.STR164:    .string "(%rbp)  # Zero array element"
.STR165:    .string "(%rbp)\n"
.STR166:    .string "String"
.STR167:    .string "List"
.STR168:    .string "    movq %rax, -"
.STR169:    .string "    movq %rax, (%rbx)"
.STR170:    .string "    movq (%rbx), %rcx"
.STR171:    .string "    addq %rax, %rcx"
.STR172:    .string "    subq %rax, %rcx"
.STR173:    .string "    imulq %rax, %rcx"
.STR174:    .string "    movq %rcx, %rax"
.STR175:    .string "    popq %rcx"
.STR176:    .string "    movq %rcx, (%rbx)"
.STR177:    .string ".L"
.STR178:    .string ":"
.STR179:    .string "    movq (%rsp), %rcx"
.STR180:    .string "    cmpq %rcx, %rax"
.STR181:    .string "    jg .L"
.STR182:    .string "    movq $1, %rax"
.STR183:    .string "    addq %rcx, %rax"
.STR184:    .string "    jmp .L"
.STR185:    .string "    movq %rbp, %rsp\n"
.STR186:    .string "    popq %rbp\n"
.STR187:    .string "    ret\n"
.STR188:    .string "    jz .L"
.STR189:    .string "    "
.STR190:    .string "    movq %rax, %rdi\n"
.STR191:    .string "    call print_string\n"
.STR192:    .string "    call print_integer\n"
.STR193:    .string "    pushq %rax  # Save match expression value"
.STR194:    .string ".match_end_"
.STR195:    .string ".match_case_"
.STR196:    .string "_"
.STR197:    .string "    popq %rax  # Get match expression\n"
.STR198:    .string "    pushq %rax  # Keep on stack"
.STR199:    .string "    movq (%rax), %rdx  # Load variant tag"
.STR200:    .string "    cmpq $"
.STR201:    .string ", %rdx  # Check tag for "
.STR202:    .string "    jne .match_case_"
.STR203:    .string "  # Jump to next case"
.STR204:    .string "    jne "
.STR205:    .string "  # No match, exit"
.STR206:    .string "    popq %rax  # Get variant pointer\n"
.STR207:    .string "(%rax), %rdx  # Load field "
.STR208:    .string "    movq %rdx, -"
.STR209:    .string "(%rbp, 0)  # Store "
.STR210:    .string " at stack offset"
.STR211:    .string "    jmp "
.STR212:    .string "    popq %rax  # Clean up match expression\n"
.STR213:    .string ".globl "
.STR214:    .string "    pushq %rbp"
.STR215:    .string "    movq %rsp, %rbp"
.STR216:    .string "%rdi"
.STR217:    .string "%rsi"
.STR218:    .string "%rdx"
.STR219:    .string "%rcx"
.STR220:    .string "%r8"
.STR221:    .string "%r9"
.STR222:    .string "main"
.STR223:    .string "    # Initialize command line arguments"
.STR224:    .string "    pushq %rdi  # Save argc"
.STR225:    .string "    pushq %rsi  # Save argv"
.STR226:    .string "    call runtime_set_command_line_args@PLT"
.STR227:    .string "    popq %rsi   # Restore argv"
.STR228:    .string "    popq %rdi   # Restore argc"
.STR229:    .string "    subq $2048, %rsp  # Pre-allocate generous stack space"
.STR230:    .string ", -"
.STR231:    .string "(%rbp)"
.STR232:    .string "    movq %rbp, %rsp"
.STR233:    .string "    popq %rbp"
.STR234:    .string "    ret"
.STR235:    .string "# Imports:"
.STR236:    .string "#   Import "
.STR237:    .string " as "
.STR238:    .string "[ERROR] codegen_generate: functions pointer is NULL"
.STR239:    .string ".section .rodata"
.STR240:    .string "    .string "
.STR241:    .string ".section .data"
.STR242:    .string "    .quad "
.STR243:    .string "    .quad 0  # Non-constant initializer defaults to 0"
.STR244:    .string ".section .bss"
.STR245:    .string "    .zero 8  # 8 bytes for Integer"
.STR246:    .string ".text"
.STR247:    .string "print_string:"
.STR248:    .string "    # Calculate string length"
.STR249:    .string "    movq %rdi, %rsi  # Save string pointer"
.STR250:    .string "    movq %rdi, %rcx  # Counter for strlen"
.STR251:    .string "    xorq %rax, %rax  # Length accumulator"
.STR252:    .string ".strlen_loop:"
.STR253:    .string "    cmpb $0, (%rcx)"
.STR254:    .string "    je .strlen_done"
.STR255:    .string "    incq %rcx"
.STR256:    .string "    incq %rax"
.STR257:    .string "    jmp .strlen_loop"
.STR258:    .string ".strlen_done:"
.STR259:    .string "    # Call write syscall (sys_write = 1)"
.STR260:    .string "    movq $1, %rdi     # fd = stdout"
.STR261:    .string "    movq %rsi, %rsi   # buf = string pointer (already in rsi)"
.STR262:    .string "    movq %rax, %rdx   # count = string length"
.STR263:    .string "    movq $1, %rax     # syscall number for write"
.STR264:    .string "    syscall"
.STR265:    .string "    # Print newline"
.STR266:    .string "    leaq .newline(%rip), %rsi  # newline string"
.STR267:    .string "    movq $1, %rdx     # count = 1"
.STR268:    .string "print_integer:"
.STR269:    .string "    subq $32, %rsp  # Space for string buffer (20 digits + null)"
.STR270:    .string "    # Convert integer to string"
.STR271:    .string "    movq %rdi, %rax  # integer value"
.STR272:    .string "    leaq -32(%rbp), %rsi  # buffer pointer"
.STR273:    .string "    addq $19, %rsi  # point to end of buffer (for reverse building)"
.STR274:    .string "    movb $0, (%rsi)  # null terminator"
.STR275:    .string "    decq %rsi"
.STR276:    .string "    # Handle zero case"
.STR277:    .string "    jnz .convert_loop"
.STR278:    .string "    movb $48, (%rsi)  # '0' character"
.STR279:    .string "    jmp .convert_done"
.STR280:    .string ".convert_loop:"
.STR281:    .string "    jz .convert_done"
.STR282:    .string "    movq $10, %rbx"
.STR283:    .string "    xorq %rdx, %rdx"
.STR284:    .string "    divq %rbx  # %rax = quotient, %rdx = remainder"
.STR285:    .string "    addq $48, %rdx  # convert remainder to ASCII"
.STR286:    .string "    movb %dl, (%rsi)  # store digit"
.STR287:    .string "    jmp .convert_loop"
.STR288:    .string ".convert_done:"
.STR289:    .string "    incq %rsi  # point to first character"
.STR290:    .string "    movq %rsi, %rcx  # Counter for strlen"
.STR291:    .string ".int_strlen_loop:"
.STR292:    .string "    je .int_strlen_done"
.STR293:    .string "    jmp .int_strlen_loop"
.STR294:    .string ".int_strlen_done:"
.STR295:    .string "    # %rsi already points to string"
.STR296:    .string ".newline:"
.STR297:    .string "    .byte 10  # newline character"
.STR298:    .string ".globl main"
.STR299:    .string ".section .note.GNU-stack"

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


.globl codegen_hash_string
codegen_hash_string:
    pushq %rbp
    movq %rsp, %rbp
    subq $2048, %rsp  # Pre-allocate generous stack space
    movq %rdi, -8(%rbp)
    movq -8(%rbp), %rax
    movq %rax, -16(%rbp)
    movq $5381, %rax
    movq %rax, -24(%rbp)
    movq $0, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -32(%rbp)
    movq $0, %rax
    movq %rax, -40(%rbp)
.L1:    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2
    movq -24(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -48(%rbp)
    movq -48(%rbp), %rax
    addq -24(%rbp), %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -24(%rbp), %rax
    addq -32(%rbp), %rax
    pushq %rax
    leaq -24(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -40(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -40(%rbp), %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    pushq %rax
    leaq -32(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L1
.L2:
    movq -24(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_compare_strings
codegen_compare_strings:
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
    call string_compare@PLT
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L11
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L12
.L11:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
.L12:
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
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -40(%rbp)
    movq $0, %rax
    movq %rax, -48(%rbp)
.L21:    movq -48(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L22
    movq -48(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -56(%rbp)
    movq -32(%rbp), %rax
    addq -56(%rbp), %rax
    movq %rax, -64(%rbp)
    movq $0, %rax
    pushq %rax
    movq -64(%rbp), %rax
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
    call memory_get_byte@PLT
    movq %rax, -80(%rbp)
    movq -80(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L31
    movq -16(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
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
    movq -48(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L42
.L41:
.L42:
    jmp .L32
.L31:
.L32:
    movq -48(%rbp), %rax
    addq $1, %rax
    movq %rax, -48(%rbp)
    jmp .L21
.L22:
    movq $-1, %rax
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
    jz .L51
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L52
.L51:
.L52:
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
    jz .L61
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L62
.L61:
.L62:
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
    jz .L71
    movq $2, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L72
.L71:
.L72:
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
    jz .L81
    movq $8, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L82
.L81:
.L82:
    movq -16(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L91
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
.L101:    movq -40(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L102
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
    jz .L111
    movq $40, %rax
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
    jmp .L112
.L111:
.L112:
    movq -40(%rbp), %rax
    addq $1, %rax
    movq %rax, -40(%rbp)
    jmp .L101
.L102:
    jmp .L92
.L91:
.L92:
    movq $8, %rax
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
    jz .L121
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
.L131:    movq -88(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L132
    movq -88(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -56(%rbp), %rax
    addq -96(%rbp), %rax
    movq %rax, -104(%rbp)
    movq -88(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -96(%rbp)
    movq -80(%rbp), %rax
    addq -96(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L131
.L132:
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
    jmp .L122
.L121:
.L122:
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
    jz .L141
    movq -144(%rbp), %rax
    pushq %rax
    leaq .STR1(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_calculate_type_size
    movq %rax, -152(%rbp)
    jmp .L142
.L141:
.L142:
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq -168(%rbp), %rax
    addq -152(%rbp), %rax
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
    addq -96(%rbp), %rax
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
    jz .L151
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
    jmp .L152
.L151:
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
.L152:
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
    addq $1, %rax
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
    jz .L161
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
.L171:    movq -72(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L172
    movq -72(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -40(%rbp), %rax
    addq -80(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -72(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -64(%rbp), %rax
    addq -80(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L171
.L172:
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
    jmp .L162
.L161:
.L162:
    movq -24(%rbp), %rax
    movq %rax, -128(%rbp)
    movq -128(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -80(%rbp)
    movq -40(%rbp), %rax
    addq -80(%rbp), %rax
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
    addq $1, %rax
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
    jz .L181
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L182
.L181:
.L182:
    movq -16(%rbp), %rax
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
    jz .L201
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
    jz .L211
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L212
.L211:
.L212:
    movq -48(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L221
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L222
.L221:
.L222:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
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
    movq $0, %rax
    movq %rax, -56(%rbp)
.L241:    movq -56(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L242
    movq -56(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -64(%rbp)
    movq -40(%rbp), %rax
    addq -64(%rbp), %rax
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
    jz .L251
    movq -80(%rbp), %rax
    pushq %rax
    movq $65536, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L261
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
    jz .L271
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L272
.L271:
.L272:
    jmp .L262
.L261:
.L262:
    jmp .L252
.L251:
.L252:
    movq -56(%rbp), %rax
    addq $1, %rax
    movq %rax, -56(%rbp)
    jmp .L241
.L242:
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
    jmp .L202
.L201:
.L202:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L281
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
    jmp .L282
.L281:
.L282:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
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
    jmp .L292
.L291:
.L292:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L301
    movq -16(%rbp), %rax
    addq $8, %rax
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
    addq $1, %rax
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
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L321
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
    jmp .L322
.L321:
.L322:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L331
    movq -16(%rbp), %rax
    addq $8, %rax
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
.L341:    movq -56(%rbp), %rax
    pushq %rax
    movq -152(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L342
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
    addq $1, %rax
    movq %rax, -56(%rbp)
    jmp .L341
.L342:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L332
.L331:
.L332:
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L351
    movq -16(%rbp), %rax
    addq $8, %rax
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
.L361:    movq -56(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L362
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
    addq $1, %rax
    movq %rax, -56(%rbp)
    jmp .L361
.L362:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L352
.L351:
.L352:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L371
    movq -16(%rbp), %rax
    addq $8, %rax
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
    jmp .L372
.L371:
.L372:
    movq -24(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L381
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -296(%rbp)
    movq $0, %rax
    movq %rax, -376(%rbp)
.L391:    movq -376(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L392
    movq -376(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -384(%rbp)
    movq -384(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
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
    call codegen_collect_strings_from_expression
    movq -376(%rbp), %rax
    addq $1, %rax
    movq %rax, -376(%rbp)
    jmp .L391
.L392:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L382
.L381:
.L382:
    movq $0, %rax
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
    jz .L401
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L402
.L401:
.L402:
    movq -16(%rbp), %rax
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
    jz .L421
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L422
.L421:
.L422:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L431
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L432
.L431:
.L432:
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L441
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
    jmp .L442
.L441:
.L442:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L451
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
    jmp .L452
.L451:
.L452:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L461
    movq -16(%rbp), %rax
    addq $8, %rax
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
    jmp .L462
.L461:
.L462:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L471
    movq -16(%rbp), %rax
    addq $8, %rax
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
    jmp .L472
.L471:
.L472:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L481
    movq -16(%rbp), %rax
    addq $8, %rax
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
    jz .L491
    movq $0, %rax
    movq %rax, -144(%rbp)
.L501:    movq -144(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L502
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
    addq $1, %rax
    movq %rax, -144(%rbp)
    jmp .L501
.L502:
    jmp .L492
.L491:
.L492:
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L511
    movq $0, %rax
    movq %rax, -144(%rbp)
.L521:    movq -144(%rbp), %rax
    pushq %rax
    movq -136(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L522
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
    addq $1, %rax
    movq %rax, -144(%rbp)
    jmp .L521
.L522:
    jmp .L512
.L511:
.L512:
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
    jz .L531
    movq -16(%rbp), %rax
    addq $8, %rax
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
.L541:    movq -144(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L542
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
    addq $1, %rax
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
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L551
    movq -16(%rbp), %rax
    addq $8, %rax
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
.L561:    movq -144(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L562
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
    addq $1, %rax
    movq %rax, -144(%rbp)
    jmp .L561
.L562:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L552
.L551:
.L552:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L571
    movq -16(%rbp), %rax
    addq $8, %rax
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
    jmp .L572
.L571:
.L572:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L581
    movq -16(%rbp), %rax
    addq $8, %rax
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
.L591:    movq -144(%rbp), %rax
    pushq %rax
    movq -368(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L592
    movq -144(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -392(%rbp)
    movq -376(%rbp), %rax
    addq -392(%rbp), %rax
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
.L601:    movq -424(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L602
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
    addq $1, %rax
    movq %rax, -424(%rbp)
    jmp .L601
.L602:
    movq -144(%rbp), %rax
    addq $1, %rax
    movq %rax, -144(%rbp)
    jmp .L591
.L592:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L582
.L581:
.L582:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L611
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $24, %rax
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
    movq %rax, -480(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq %rax, -488(%rbp)
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L612
.L611:
.L612:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L621
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -496(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -504(%rbp)
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -512(%rbp)
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $48, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -232(%rbp)
    movq -496(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq %rax, -480(%rbp)
    movq -504(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq %rax, -488(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L631
    movq -512(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_expression
    movq %rax, -552(%rbp)
    jmp .L632
.L631:
.L632:
    movq $0, %rax
    movq %rax, -144(%rbp)
.L641:    movq -144(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L642
    movq -144(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -224(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -568(%rbp)
    movq -568(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_collect_strings_from_statement
    movq %rax, -576(%rbp)
    movq -144(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -144(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L641
.L642:
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
    jz .L651
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L652
.L651:
.L652:
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
    jz .L661
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
    jz .L671
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
    jz .L681
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
.L691:    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L692
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
    jz .L701
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
    jmp .L702
.L701:
.L702:
    movq -72(%rbp), %rax
    addq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L691
.L692:
    jmp .L682
.L681:
.L682:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L672
.L671:
.L672:
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
    addq -128(%rbp), %rax
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
    jmp .L662
.L661:
.L662:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L711
    movq -16(%rbp), %rax
    addq $8, %rax
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
    jz .L721
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L722
.L721:
.L722:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -48(%rbp)
    movq $24, %rax
    pushq %rax
    movq -48(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -192(%rbp)
    movq $16, %rax
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
.L731:    movq -216(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L732
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
    jz .L741
    movq -232(%rbp), %rax
    movq %rax, -208(%rbp)
    movq -192(%rbp), %rax
    movq %rax, -216(%rbp)
    jmp .L742
.L741:
.L742:
    movq -216(%rbp), %rax
    addq $1, %rax
    movq %rax, -216(%rbp)
    jmp .L731
.L732:
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L751
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L752
.L751:
.L752:
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
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L761
    movq $24, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -280(%rbp)
    movq $16, %rax
    pushq %rax
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq $0, %rax
    movq %rax, -216(%rbp)
.L771:    movq -216(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L772
    movq -216(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -304(%rbp)
    movq -288(%rbp), %rax
    addq -304(%rbp), %rax
    movq %rax, -312(%rbp)
    movq $0, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -320(%rbp)
    movq -168(%rbp), %rax
    pushq %rax
    movq -320(%rbp), %rax
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
    jz .L781
    movq $8, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L782
.L781:
.L782:
    movq -216(%rbp), %rax
    addq $1, %rax
    movq %rax, -216(%rbp)
    jmp .L771
.L772:
    jmp .L762
.L761:
.L762:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L712
.L711:
.L712:
    movq -24(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L791
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L792
.L791:
.L792:
    movq $0, %rax
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
    jz .L801
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
    jz .L811
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
    jz .L821
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
.L831:    movq -88(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L832
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
    jz .L841
    movq $1, %rax
    movq %rax, -56(%rbp)
    movq -72(%rbp), %rax
    movq %rax, -88(%rbp)
    jmp .L842
.L841:
.L842:
    movq -88(%rbp), %rax
    addq $1, %rax
    movq %rax, -88(%rbp)
    jmp .L831
.L832:
    jmp .L822
.L821:
.L822:
    movq -56(%rbp), %rax
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
    jmp .L852
.L851:
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
.L852:
    jmp .L812
.L811:
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
    addq -152(%rbp), %rax
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
.L812:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L802
.L801:
.L802:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L861
    movq -16(%rbp), %rax
    addq $8, %rax
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
    movq $0, %rax
    pushq %rax
    movq -184(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L871
    movq $8, %rax
    pushq %rax
    movq -184(%rbp), %rax
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
    jz .L881
    leaq .STR12(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L882
.L881:
.L882:
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
    addq -152(%rbp), %rax
    movq %rax, -160(%rbp)
    movq $8, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -248(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR13(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -248(%rbp), %rax
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
    leaq .STR14(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L872
.L871:
    movq -184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR15(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L872:
    movq -184(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_get_expression_type
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L891
    leaq .STR16(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L892
.L891:
.L892:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $24, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -272(%rbp)
    movq $16, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq $0, %rax
    movq %rax, -288(%rbp)
    movq $0, %rax
    movq %rax, -296(%rbp)
.L901:    movq -296(%rbp), %rax
    pushq %rax
    movq -272(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L902
    movq -296(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -304(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -312(%rbp)
    movq $0, %rax
    pushq %rax
    movq -312(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -320(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq -320(%rbp), %rax
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
    jz .L911
    movq -312(%rbp), %rax
    movq %rax, -288(%rbp)
    movq -272(%rbp), %rax
    movq %rax, -296(%rbp)
    jmp .L912
.L911:
.L912:
    movq -296(%rbp), %rax
    addq $1, %rax
    movq %rax, -296(%rbp)
    jmp .L901
.L902:
    movq -288(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L921
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -256(%rbp), %rax
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
    jmp .L922
.L921:
.L922:
    movq $-1, %rax
    movq %rax, -352(%rbp)
    movq $8, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L931
    movq $24, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -368(%rbp)
    movq $16, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -376(%rbp)
    movq $0, %rax
    movq %rax, -296(%rbp)
.L941:    movq -296(%rbp), %rax
    pushq %rax
    movq -368(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L942
    movq -296(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -392(%rbp)
    movq -376(%rbp), %rax
    addq -392(%rbp), %rax
    movq %rax, -400(%rbp)
    movq $0, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -408(%rbp)
    movq -192(%rbp), %rax
    pushq %rax
    movq -408(%rbp), %rax
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
    jz .L951
    movq $16, %rax
    pushq %rax
    movq -400(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -352(%rbp)
    movq -368(%rbp), %rax
    movq %rax, -296(%rbp)
    jmp .L952
.L951:
.L952:
    movq -296(%rbp), %rax
    addq $1, %rax
    movq %rax, -296(%rbp)
    jmp .L941
.L942:
    jmp .L932
.L931:
.L932:
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L961
    leaq .STR18(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -256(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR19(%rip), %rax
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
    jmp .L962
.L961:
.L962:
    movq $0, %rax
    pushq %rax
    leaq .STR20(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -352(%rbp), %rax
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
    leaq .STR21(%rip), %rax
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
    jmp .L862
.L861:
.L862:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L971
    movq -16(%rbp), %rax
    addq $8, %rax
    movq %rax, -440(%rbp)
    movq $0, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -448(%rbp)
    movq $8, %rax
    pushq %rax
    movq -440(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -456(%rbp)
    movq $0, %rax
    pushq %rax
    movq -448(%rbp), %rax
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
    jz .L981
    movq $8, %rax
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
    jz .L991
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
    addq -152(%rbp), %rax
    movq %rax, -160(%rbp)
    movq $24, %rax
    pushq %rax
    movq -160(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -512(%rbp)
    movq -512(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1001
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
    leaq .STR13(%rip), %rax
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
    leaq .STR22(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1002
.L1001:
    movq -448(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
.L1002:
    jmp .L992
.L991:
    movq -448(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
.L992:
    jmp .L982
.L981:
    movq -448(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
.L982:
    leaq .STR23(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -456(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR25(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR26(%rip), %rax
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
    jmp .L972
.L971:
.L972:
    leaq .STR27(%rip), %rax
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
    jz .L1011
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
    jz .L1021
    movq $56, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
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
.L1031:    movq -80(%rbp), %rax
    pushq %rax
    movq -64(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1032
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
    jz .L1041
    movq $1, %rax
    movq %rax, -48(%rbp)
    movq -104(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -64(%rbp), %rax
    movq %rax, -80(%rbp)
    jmp .L1042
.L1041:
.L1042:
    movq -80(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    jmp .L1031
.L1032:
    jmp .L1022
.L1021:
.L1022:
    movq -48(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1051
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
    jz .L1061
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
    jz .L1071
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
    leaq .STR30(%rip), %rax
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
    jmp .L1072
.L1071:
.L1072:
    jmp .L1062
.L1061:
.L1062:
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
    leaq .STR32(%rip), %rax
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
    jmp .L1052
.L1051:
.L1052:
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
    jz .L1081
    movq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -192(%rbp)
    movq $0, %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_byte@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    movq %rax, -80(%rbp)
.L1091:    movq -80(%rbp), %rax
    pushq %rax
    movq -184(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1092
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -216(%rbp)
    movq -216(%rbp), %rax
    pushq %rax
    movq -192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -224(%rbp)
    movq $0, %rax
    pushq %rax
    movq -224(%rbp), %rax
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
    call memory_get_byte@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1101
    movq -32(%rbp), %rax
    pushq %rax
    movq -232(%rbp), %rax
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
    jz .L1111
    movq $1, %rax
    movq %rax, -176(%rbp)
    movq -184(%rbp), %rax
    movq %rax, -80(%rbp)
    jmp .L1112
.L1111:
.L1112:
    jmp .L1102
.L1101:
.L1102:
    movq -80(%rbp), %rax
    addq $1, %rax
    movq %rax, -80(%rbp)
    jmp .L1091
.L1092:
    jmp .L1082
.L1081:
.L1082:
    movq -176(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1121
    leaq .STR33(%rip), %rax
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
    jmp .L1122
.L1121:
.L1122:
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
    leaq .STR34(%rip), %rax
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
    jmp .L1012
.L1011:
.L1012:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -272(%rbp)
    movq -40(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -280(%rbp)
    movq -272(%rbp), %rax
    addq -280(%rbp), %rax
    movq %rax, -288(%rbp)
    movq $8, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -296(%rbp)
    movq $16, %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -304(%rbp)
    movq $0, %rax
    movq %rax, -312(%rbp)
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
    jz .L1131
    movq $24, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -328(%rbp)
    movq $16, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -336(%rbp)
    movq $0, %rax
    movq %rax, -344(%rbp)
.L1141:    movq -344(%rbp), %rax
    pushq %rax
    movq -328(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1142
    movq -344(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq -336(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq $0, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -368(%rbp)
    movq -304(%rbp), %rax
    pushq %rax
    movq -368(%rbp), %rax
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
    jz .L1151
    movq $8, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -376(%rbp)
    movq -376(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1161
    movq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L1162
.L1161:
.L1162:
    movq -328(%rbp), %rax
    movq %rax, -344(%rbp)
    jmp .L1152
.L1151:
.L1152:
    movq -344(%rbp), %rax
    addq $1, %rax
    movq %rax, -344(%rbp)
    jmp .L1141
.L1142:
    jmp .L1132
.L1131:
.L1132:
    movq -312(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1171
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
    movq -296(%rbp), %rax
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
    leaq .STR35(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1172
.L1171:
    movq $0, %rax
    pushq %rax
    leaq .STR13(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
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
.L1172:
    movq $0, %rax
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
    jz .L1181
    leaq .STR37(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1182
.L1181:
.L1182:
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
    movq $-1, %rax
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L1191:    movq -64(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1192
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
    jz .L1201
    movq -64(%rbp), %rax
    movq %rax, -56(%rbp)
    movq -40(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L1202
.L1201:
.L1202:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L1191
.L1192:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1211
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_string_literal
    movq %rax, -56(%rbp)
    jmp .L1212
.L1211:
.L1212:
    movq $0, %rax
    pushq %rax
    leaq .STR38(%rip), %rax
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
    leaq .STR39(%rip), %rax
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
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -56(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1221
    movq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L1222
.L1221:
.L1222:
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1231
    movq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L1232
.L1231:
.L1232:
    movq -64(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1241
    movq -32(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq -48(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1251
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1261
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR20(%rip), %rax
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
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1262
.L1261:
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    call codegen_find_variable
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1271
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -120(%rbp)
    movq -112(%rbp), %rax
    addq -120(%rbp), %rax
    movq %rax, -128(%rbp)
    movq $8, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -136(%rbp)
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
    pushq %rax
    movq -136(%rbp), %rax
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
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1272
.L1271:
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
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR42(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
.L1272:
.L1262:
    jmp .L1252
.L1251:
.L1252:
    movq -48(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1281
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1291
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR43(%rip), %rax
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
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1292
.L1291:
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
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
    call codegen_find_variable
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1301
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -120(%rbp)
    movq -112(%rbp), %rax
    addq -120(%rbp), %rax
    movq %rax, -128(%rbp)
    movq $8, %rax
    pushq %rax
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -136(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR44(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -136(%rbp), %rax
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
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1302
.L1301:
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
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR45(%rip), %rax
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
.L1302:
.L1292:
    jmp .L1282
.L1281:
.L1282:
    movq -48(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1311
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
    leaq .STR24(%rip), %rax
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
    jmp .L1312
.L1311:
.L1312:
    movq -48(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1321
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
    leaq .STR48(%rip), %rax
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
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR51(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR52(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR54(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR55(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR57(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR58(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -200(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L1322
.L1321:
.L1322:
    movq -48(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1331
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
    leaq .STR48(%rip), %rax
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
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR59(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR52(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR60(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR61(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR62(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR57(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR63(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -200(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L1332
.L1331:
.L1332:
    movq -48(%rbp), %rax
    pushq %rax
    movq $39, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1341
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1351
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR64(%rip), %rax
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
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1352
.L1351:
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
    leaq .STR24(%rip), %rax
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
.L1352:
    jmp .L1342
.L1341:
.L1342:
    movq -48(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1361
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1371
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR66(%rip), %rax
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
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1372
.L1371:
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
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR67(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
.L1372:
    jmp .L1362
.L1361:
.L1362:
    movq -48(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1381
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1391
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -88(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR68(%rip), %rax
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
    leaq .STR29(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1392
.L1391:
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
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR69(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
.L1392:
    jmp .L1382
.L1381:
.L1382:
    movq -48(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1401
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
    leaq .STR48(%rip), %rax
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
    leaq .STR70(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1402
.L1401:
.L1402:
    movq -48(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1411
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
    leaq .STR48(%rip), %rax
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
    leaq .STR71(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1412
.L1411:
.L1412:
    jmp .L1242
.L1241:
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
    leaq .STR24(%rip), %rax
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
    jz .L1421
    leaq .STR42(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1422
.L1421:
.L1422:
    movq -48(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1431
    leaq .STR45(%rip), %rax
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
    jmp .L1432
.L1431:
.L1432:
    movq -48(%rbp), %rax
    pushq %rax
    movq $35, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1441
    leaq .STR47(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1442
.L1441:
.L1442:
    movq -48(%rbp), %rax
    pushq %rax
    movq $36, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1451
    leaq .STR48(%rip), %rax
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
    leaq .STR50(%rip), %rax
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
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR51(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR52(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR54(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR55(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR57(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR58(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -200(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L1452
.L1451:
.L1452:
    movq -48(%rbp), %rax
    pushq %rax
    movq $37, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1461
    leaq .STR48(%rip), %rax
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
    leaq .STR50(%rip), %rax
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
    movq %rax, -200(%rbp)
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR59(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR52(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR60(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR61(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR62(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR57(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR63(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -200(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L1462
.L1461:
.L1462:
    movq -48(%rbp), %rax
    pushq %rax
    movq $39, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1471
    leaq .STR65(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1472
.L1471:
.L1472:
    movq -48(%rbp), %rax
    pushq %rax
    movq $40, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1481
    leaq .STR67(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1482
.L1481:
.L1482:
    movq -48(%rbp), %rax
    pushq %rax
    movq $41, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1491
    leaq .STR69(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1492
.L1491:
.L1492:
    movq -48(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1501
    leaq .STR48(%rip), %rax
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
    leaq .STR70(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1502
.L1501:
.L1502:
    movq -48(%rbp), %rax
    pushq %rax
    movq $43, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1511
    leaq .STR48(%rip), %rax
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
    leaq .STR71(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1512
.L1511:
.L1512:
    movq -48(%rbp), %rax
    pushq %rax
    movq $30, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1521
    leaq .STR65(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1522
.L1521:
.L1522:
    movq -48(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1531
    leaq .STR67(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1532
.L1531:
.L1532:
.L1242:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret


.globl codegen_generate_unary_op
codegen_generate_unary_op:
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
    call memory_get_integer@PLT
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
    call codegen_generate_expression
    movq -32(%rbp), %rax
    pushq %rax
    movq $29, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1541
    leaq .STR72(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR73(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR74(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1542
.L1541:
.L1542:
    movq $0, %rax
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
    leaq .STR24(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR75(%rip), %rax
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
    jz .L1551
    leaq .STR76(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1552
.L1551:
.L1552:
    movq -48(%rbp), %rax
    pushq %rax
    movq $23, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1561
    leaq .STR77(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1562
.L1561:
.L1562:
    movq -48(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1571
    leaq .STR78(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1572
.L1571:
.L1572:
    movq -48(%rbp), %rax
    pushq %rax
    movq $25, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1581
    leaq .STR79(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1582
.L1581:
.L1582:
    movq -48(%rbp), %rax
    pushq %rax
    movq $27, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1591
    leaq .STR80(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1592
.L1591:
.L1592:
    movq -48(%rbp), %rax
    pushq %rax
    movq $26, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1601
    leaq .STR81(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L1602
.L1601:
.L1602:
    leaq .STR74(%rip), %rax
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
    addq $8, %rax
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
    jz .L1611
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L1612
.L1611:
.L1612:
    movq -56(%rbp), %rax
    subq $1, %rax
    movq %rax, -64(%rbp)
.L1621:    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1622
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
    jz .L1631
    leaq .STR82(%rip), %rax
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
    jmp .L1632
.L1631:
.L1632:
    movq -80(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR83(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -64(%rbp), %rax
    subq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L1621
.L1622:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1641
    movq $0, %rax
    pushq %rax
    leaq .STR84(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1642
.L1641:
.L1642:
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1651
    movq $0, %rax
    pushq %rax
    leaq .STR85(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1652
.L1651:
.L1652:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1661
    movq $0, %rax
    pushq %rax
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1662
.L1661:
.L1662:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1671
    movq $0, %rax
    pushq %rax
    leaq .STR87(%rip), %rax
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
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1681
    movq $0, %rax
    pushq %rax
    leaq .STR88(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1682
.L1681:
.L1682:
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L1691
    movq $0, %rax
    pushq %rax
    leaq .STR89(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L1692
.L1691:
.L1692:
    movq $0, %rax
    pushq %rax
    leaq .STR90(%rip), %rax
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
    jz .L1701
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1702
.L1701:
.L1702:
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
    jz .L1711
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1712
.L1711:
.L1712:
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
    jz .L1721
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1722
.L1721:
.L1722:
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
    jz .L1731
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1732
.L1731:
.L1732:
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
    jz .L1741
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1742
.L1741:
.L1742:
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
    jz .L1751
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1752
.L1751:
.L1752:
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
    jz .L1761
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1762
.L1761:
.L1762:
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
    jz .L1771
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1772
.L1771:
.L1772:
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
    jz .L1781
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1782
.L1781:
.L1782:
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
    jz .L1791
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1792
.L1791:
.L1792:
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
    jz .L1801
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1802
.L1801:
.L1802:
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
    jz .L1811
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1812
.L1811:
.L1812:
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
    jz .L1821
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1822
.L1821:
.L1822:
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
    jz .L1831
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1832
.L1831:
.L1832:
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
    jz .L1841
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1842
.L1841:
.L1842:
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
    jz .L1851
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1852
.L1851:
.L1852:
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
    jz .L1861
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1862
.L1861:
.L1862:
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
    jz .L1871
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1872
.L1871:
.L1872:
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
    jz .L1881
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1882
.L1881:
.L1882:
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
    jz .L1891
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1892
.L1891:
.L1892:
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
    jz .L1901
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1902
.L1901:
.L1902:
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
    jz .L1911
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1912
.L1911:
.L1912:
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
    jz .L1921
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1922
.L1921:
.L1922:
    leaq .STR114(%rip), %rax
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
    jz .L1931
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1932
.L1931:
.L1932:
    leaq .STR115(%rip), %rax
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
    jz .L1941
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1942
.L1941:
.L1942:
    leaq .STR116(%rip), %rax
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
    jz .L1951
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1952
.L1951:
.L1952:
    leaq .STR117(%rip), %rax
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
    jz .L1961
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1962
.L1961:
.L1962:
    leaq .STR118(%rip), %rax
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
    jz .L1971
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1972
.L1971:
.L1972:
    leaq .STR119(%rip), %rax
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
    jz .L1981
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1982
.L1981:
.L1982:
    leaq .STR120(%rip), %rax
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
    jz .L1991
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L1992
.L1991:
.L1992:
    leaq .STR121(%rip), %rax
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
    jz .L2001
    movq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L2002
.L2001:
.L2002:
    movq -96(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2011
    movq $0, %rax
    pushq %rax
    leaq .STR122(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2012
.L2011:
.L2012:
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


.globl codegen_generate_indirect_call
codegen_generate_indirect_call:
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
    addq $8, %rax
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
    movq -56(%rbp), %rax
    subq $1, %rax
    movq %rax, -64(%rbp)
.L2021:    movq -64(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2022
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
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR83(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -64(%rbp), %rax
    subq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L2021
.L2022:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2031
    movq $0, %rax
    pushq %rax
    leaq .STR84(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2032
.L2031:
.L2032:
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2041
    movq $0, %rax
    pushq %rax
    leaq .STR85(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2042
.L2041:
.L2042:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2051
    movq $0, %rax
    pushq %rax
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2052
.L2051:
.L2052:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2061
    movq $0, %rax
    pushq %rax
    leaq .STR87(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2062
.L2061:
.L2062:
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2071
    movq $0, %rax
    pushq %rax
    leaq .STR88(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2072
.L2071:
.L2072:
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2081
    movq $0, %rax
    pushq %rax
    leaq .STR89(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2082
.L2081:
.L2082:
    movq $0, %rax
    pushq %rax
    leaq .STR123(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2091
    movq $0, %rax
    pushq %rax
    leaq .STR124(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2092
.L2091:
.L2092:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2101
    movq $0, %rax
    pushq %rax
    leaq .STR125(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2102
.L2101:
.L2102:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2111
    movq $0, %rax
    pushq %rax
    leaq .STR126(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2112
.L2111:
.L2112:
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2121
    movq $0, %rax
    pushq %rax
    leaq .STR127(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2122
.L2121:
.L2122:
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2131
    movq $0, %rax
    pushq %rax
    leaq .STR128(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2132
.L2131:
.L2132:
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR129(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2141
    movq $0, %rax
    pushq %rax
    leaq .STR89(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2142
.L2141:
.L2142:
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2151
    movq $0, %rax
    pushq %rax
    leaq .STR88(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2152
.L2151:
.L2152:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2161
    movq $0, %rax
    pushq %rax
    leaq .STR87(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2162
.L2161:
.L2162:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2171
    movq $0, %rax
    pushq %rax
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2172
.L2171:
.L2172:
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2181
    movq $0, %rax
    pushq %rax
    leaq .STR85(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2182
.L2181:
.L2182:
    movq $0, %rax
    pushq %rax
    leaq .STR84(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR130(%rip), %rax
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
    addq $8, %rax
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
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_get_expression_type
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2191
    leaq .STR16(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2192
.L2191:
.L2192:
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -64(%rbp)
    movq $24, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -72(%rbp)
    movq $16, %rax
    pushq %rax
    movq -64(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -80(%rbp)
    movq $0, %rax
    movq %rax, -88(%rbp)
    movq $0, %rax
    movq %rax, -96(%rbp)
.L2201:    movq -96(%rbp), %rax
    pushq %rax
    movq -72(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2202
    movq -96(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -104(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -112(%rbp)
    movq $0, %rax
    pushq %rax
    movq -112(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -120(%rbp)
    movq -56(%rbp), %rax
    pushq %rax
    movq -120(%rbp), %rax
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
    jz .L2211
    movq -112(%rbp), %rax
    movq %rax, -88(%rbp)
    movq -72(%rbp), %rax
    movq %rax, -96(%rbp)
    jmp .L2212
.L2211:
.L2212:
    movq -96(%rbp), %rax
    addq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L2201
.L2202:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2221
    leaq .STR17(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
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
    jmp .L2222
.L2221:
.L2222:
    movq $-1, %rax
    movq %rax, -152(%rbp)
    movq $8, %rax
    pushq %rax
    movq -88(%rbp), %rax
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
    jz .L2231
    movq $24, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -168(%rbp)
    movq $16, %rax
    pushq %rax
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq $0, %rax
    movq %rax, -184(%rbp)
.L2241:    movq -184(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2242
    movq -184(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -192(%rbp)
    movq -176(%rbp), %rax
    addq -192(%rbp), %rax
    movq %rax, -200(%rbp)
    movq $0, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -208(%rbp)
    movq -48(%rbp), %rax
    pushq %rax
    movq -208(%rbp), %rax
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
    jz .L2251
    movq $16, %rax
    pushq %rax
    movq -200(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -152(%rbp)
    movq -168(%rbp), %rax
    movq %rax, -184(%rbp)
    jmp .L2252
.L2251:
.L2252:
    movq -184(%rbp), %rax
    addq $1, %rax
    movq %rax, -184(%rbp)
    jmp .L2241
.L2242:
    jmp .L2232
.L2231:
.L2232:
    movq -152(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2261
    leaq .STR18(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR19(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -48(%rbp), %rax
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
    jmp .L2262
.L2261:
.L2262:
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -240(%rbp)
    movq -240(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2271
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -248(%rbp)
    movq -248(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_find_variable
    movq %rax, -256(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2281
    leaq .STR131(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2282
.L2281:
.L2282:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -264(%rbp)
    movq -256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq -264(%rbp), %rax
    addq -272(%rbp), %rax
    movq %rax, -280(%rbp)
    movq $8, %rax
    pushq %rax
    movq -280(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -288(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR13(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -288(%rbp), %rax
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
    leaq .STR31(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -152(%rbp), %rax
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
    leaq .STR132(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2272
.L2271:
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
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
    pushq %rax
    movq -152(%rbp), %rax
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
    leaq .STR132(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2272:
    movq $0, %rax
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
    addq $8, %rax
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
    leaq .STR133(%rip), %rax
    movq %rax, -64(%rbp)
    movq -56(%rbp), %rax
    subq $1, %rax
    movq %rax, -72(%rbp)
.L2291:    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2292
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
    leaq .STR83(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -72(%rbp), %rax
    subq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L2291
.L2292:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2301
    movq $0, %rax
    pushq %rax
    leaq .STR84(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2302
.L2301:
.L2302:
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2311
    movq $0, %rax
    pushq %rax
    leaq .STR85(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2312
.L2311:
.L2312:
    movq -56(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2321
    movq $0, %rax
    pushq %rax
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2322
.L2321:
.L2322:
    movq -56(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2331
    movq $0, %rax
    pushq %rax
    leaq .STR87(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2332
.L2331:
.L2332:
    movq -56(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2341
    movq $0, %rax
    pushq %rax
    leaq .STR88(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2342
.L2341:
.L2342:
    movq -56(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2351
    movq $0, %rax
    pushq %rax
    leaq .STR89(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2352
.L2351:
.L2352:
    movq $0, %rax
    pushq %rax
    leaq .STR134(%rip), %rax
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
    leaq .STR135(%rip), %rax
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
    jz .L2361
    leaq .STR136(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    jmp .L2362
.L2361:
.L2362:
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
    jz .L2371
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
    leaq .STR29(%rip), %rax
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
    jmp .L2372
.L2371:
.L2372:
    movq -24(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2381
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
    jmp .L2382
.L2381:
.L2382:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2391
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
    jmp .L2392
.L2391:
.L2392:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2401
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
    jmp .L2402
.L2401:
.L2402:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2411
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
    jmp .L2412
.L2411:
.L2412:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2421
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_indirect_call
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2422
.L2421:
.L2422:
    movq -24(%rbp), %rax
    pushq %rax
    movq $12, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2431
    movq -16(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_unary_op
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2432
.L2431:
.L2432:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2441
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
    jmp .L2442
.L2441:
.L2442:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2451
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
    jmp .L2452
.L2451:
.L2452:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2461
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
    jmp .L2462
.L2461:
.L2462:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2471
    movq -16(%rbp), %rax
    addq $8, %rax
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
    subq $1, %rax
    movq %rax, -80(%rbp)
.L2481:    movq -80(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2482
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
    leaq .STR83(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -80(%rbp), %rax
    subq $1, %rax
    movq %rax, -80(%rbp)
    jmp .L2481
.L2482:
    movq -72(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2491
    movq $0, %rax
    pushq %rax
    leaq .STR84(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2492
.L2491:
.L2492:
    movq -72(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2501
    movq $0, %rax
    pushq %rax
    leaq .STR85(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2502
.L2501:
.L2502:
    movq -72(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2511
    movq $0, %rax
    pushq %rax
    leaq .STR86(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L2512
.L2511:
.L2512:
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
    jz .L2521
    leaq .STR95(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2522
.L2521:
.L2522:
    movq -112(%rbp), %rax
    pushq %rax
    movq $58, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2531
    leaq .STR96(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2532
.L2531:
.L2532:
    movq -112(%rbp), %rax
    pushq %rax
    movq $59, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2541
    leaq .STR100(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2542
.L2541:
.L2542:
    movq -112(%rbp), %rax
    pushq %rax
    movq $60, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2551
    leaq .STR97(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2552
.L2551:
.L2552:
    movq -112(%rbp), %rax
    pushq %rax
    movq $61, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2561
    leaq .STR104(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2562
.L2561:
.L2562:
    movq -112(%rbp), %rax
    pushq %rax
    movq $62, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2571
    leaq .STR105(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2572
.L2571:
.L2572:
    movq -112(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2581
    leaq .STR106(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2582
.L2581:
.L2582:
    movq -112(%rbp), %rax
    pushq %rax
    movq $72, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2591
    leaq .STR99(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2592
.L2591:
.L2592:
    movq -112(%rbp), %rax
    pushq %rax
    movq $73, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2601
    leaq .STR98(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2602
.L2601:
.L2602:
    movq -112(%rbp), %rax
    pushq %rax
    movq $74, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2611
    leaq .STR102(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2612
.L2611:
.L2612:
    movq -112(%rbp), %rax
    pushq %rax
    movq $75, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2621
    leaq .STR101(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2622
.L2621:
.L2622:
    movq -112(%rbp), %rax
    pushq %rax
    movq $76, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2631
    leaq .STR103(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2632
.L2631:
.L2632:
    movq -112(%rbp), %rax
    pushq %rax
    movq $119, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2641
    leaq .STR91(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2642
.L2641:
.L2642:
    movq -112(%rbp), %rax
    pushq %rax
    movq $120, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2651
    leaq .STR92(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2652
.L2651:
.L2652:
    movq -112(%rbp), %rax
    pushq %rax
    movq $130, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2661
    leaq .STR110(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2662
.L2661:
.L2662:
    movq -112(%rbp), %rax
    pushq %rax
    movq $131, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2671
    leaq .STR111(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L2672
.L2671:
.L2672:
    movq $0, %rax
    pushq %rax
    leaq .STR90(%rip), %rax
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
    jz .L2681
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
    jmp .L2682
.L2681:
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
    leaq .STR122(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2682:
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
    jmp .L2472
.L2471:
.L2472:
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2691
    movq $0, %rax
    pushq %rax
    leaq .STR138(%rip), %rax
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
    jmp .L2692
.L2691:
.L2692:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2701
    movq -16(%rbp), %rax
    addq $8, %rax
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
    leaq .STR39(%rip), %rax
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
    jmp .L2702
.L2701:
.L2702:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2711
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -272(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -280(%rbp)
    movq -280(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR139(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -272(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR140(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR141(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR142(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
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
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2712
.L2711:
.L2712:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
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
    movq %rax, -288(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -296(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -304(%rbp)
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
    movq -304(%rbp), %rax
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
    leaq .STR144(%rip), %rax
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
    movq $0, %rax
    movq %rax, -80(%rbp)
.L2731:    movq -80(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2732
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR147(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR148(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
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
    leaq .STR149(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -80(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2731
.L2732:
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
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2722
.L2721:
.L2722:
    movq -24(%rbp), %rax
    pushq %rax
    movq $18, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2741
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -288(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -352(%rbp)
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
    movq -352(%rbp), %rax
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
    leaq .STR144(%rip), %rax
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
    movq %rax, -80(%rbp)
.L2751:    movq -80(%rbp), %rax
    pushq %rax
    movq -344(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2752
    movq -80(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -320(%rbp)
    movq -320(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -328(%rbp)
    movq -328(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
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
    leaq .STR148(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -320(%rbp), %rax
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
    leaq .STR149(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -80(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -80(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L2751
.L2752:
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
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2742
.L2741:
.L2742:
    movq -24(%rbp), %rax
    pushq %rax
    movq $19, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2761
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -344(%rbp)
    movq -344(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -352(%rbp)
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
    movq -352(%rbp), %rax
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
    leaq .STR144(%rip), %rax
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
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2762
.L2761:
.L2762:
    movq -24(%rbp), %rax
    pushq %rax
    movq $20, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2771
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -400(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -408(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -416(%rbp)
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -424(%rbp)
    movq $48, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -432(%rbp)
    movq $24, %rax
    pushq %rax
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -440(%rbp)
    movq $16, %rax
    pushq %rax
    movq -432(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -448(%rbp)
    movq $0, %rax
    movq %rax, -456(%rbp)
    movq $0, %rax
    movq %rax, -464(%rbp)
.L2781:    movq -464(%rbp), %rax
    pushq %rax
    movq -440(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2782
    movq -464(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -472(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -480(%rbp)
    movq $0, %rax
    pushq %rax
    movq -480(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -488(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq -488(%rbp), %rax
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
    jz .L2791
    movq -480(%rbp), %rax
    movq %rax, -456(%rbp)
    movq -440(%rbp), %rax
    movq %rax, -464(%rbp)
    jmp .L2792
.L2791:
.L2792:
    movq -464(%rbp), %rax
    addq $1, %rax
    movq %rax, -464(%rbp)
    jmp .L2781
.L2782:
    movq -456(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2801
    leaq .STR154(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -400(%rbp), %rax
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
    jmp .L2802
.L2801:
.L2802:
    movq $40, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -520(%rbp)
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
    movq -520(%rbp), %rax
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
    leaq .STR144(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
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
    leaq .STR156(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rax, -528(%rbp)
.L2811:    movq -528(%rbp), %rax
    pushq %rax
    movq -424(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2812
    movq -528(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -536(%rbp)
    movq -536(%rbp), %rax
    pushq %rax
    movq -408(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -544(%rbp)
    movq -536(%rbp), %rax
    pushq %rax
    movq -416(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -552(%rbp)
    movq $24, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -560(%rbp)
    movq $16, %rax
    pushq %rax
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -568(%rbp)
    movq $-1, %rax
    movq %rax, -576(%rbp)
    movq $0, %rax
    movq %rax, -584(%rbp)
.L2821:    movq -584(%rbp), %rax
    pushq %rax
    movq -560(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2822
    movq -584(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -592(%rbp)
    movq -568(%rbp), %rax
    addq -592(%rbp), %rax
    movq %rax, -600(%rbp)
    movq $0, %rax
    pushq %rax
    movq -600(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -608(%rbp)
    movq -544(%rbp), %rax
    pushq %rax
    movq -608(%rbp), %rax
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
    jz .L2831
    movq $16, %rax
    pushq %rax
    movq -600(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -576(%rbp)
    movq -560(%rbp), %rax
    movq %rax, -584(%rbp)
    jmp .L2832
.L2831:
.L2832:
    movq -584(%rbp), %rax
    addq $1, %rax
    movq %rax, -584(%rbp)
    jmp .L2821
.L2822:
    movq -576(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2841
    leaq .STR157(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -544(%rbp), %rax
    pushq %rax
    popq %rdi
    call print_string
    leaq .STR158(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq -400(%rbp), %rax
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
    jmp .L2842
.L2841:
.L2842:
    movq -552(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
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
    leaq .STR148(%rip), %rax
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
    leaq .STR160(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -528(%rbp), %rax
    addq $1, %rax
    movq %rax, -528(%rbp)
    jmp .L2811
.L2812:
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
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2772
.L2771:
.L2772:
    leaq .STR162(%rip), %rax
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
    jz .L2851
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
    jz .L2861
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
    jz .L2871
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
    movq $24, %rax
    pushq %rax
    movq -72(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -80(%rbp)
    movq $16, %rax
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
.L2881:    movq -112(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2882
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
    jz .L2891
    movq $1, %rax
    movq %rax, -96(%rbp)
    movq -120(%rbp), %rax
    movq %rax, -104(%rbp)
    movq -80(%rbp), %rax
    movq %rax, -112(%rbp)
    jmp .L2892
.L2891:
.L2892:
    movq -112(%rbp), %rax
    addq $1, %rax
    movq %rax, -112(%rbp)
    jmp .L2881
.L2882:
    movq -96(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2901
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
    movq $1, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2902
.L2901:
.L2902:
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
    addq $8, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
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
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2911
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2921:    movq -112(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2922
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
    movq -184(%rbp), %rax
    subq -112(%rbp), %rax
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
    leaq .STR164(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -112(%rbp), %rax
    addq $8, %rax
    movq %rax, -112(%rbp)
    jmp .L2921
.L2922:
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -224(%rbp)
    movq -224(%rbp), %rax
    addq -200(%rbp), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L2912
.L2911:
    movq $0, %rax
    movq %rax, -112(%rbp)
.L2931:    movq -112(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2932
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
    movq -184(%rbp), %rax
    subq -112(%rbp), %rax
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
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -112(%rbp), %rax
    addq $8, %rax
    movq %rax, -112(%rbp)
    jmp .L2931
.L2932:
.L2912:
    jmp .L2872
.L2871:
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2941
    movq -48(%rbp), %rax
    addq $8, %rax
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
    jz .L2951
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2952
.L2951:
.L2952:
    movq -256(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2961
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2962
.L2961:
.L2962:
    movq -256(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2971
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2972
.L2971:
.L2972:
    movq -256(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2981
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2982
.L2981:
.L2982:
    movq -256(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L2991
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L2992
.L2991:
.L2992:
    movq -256(%rbp), %rax
    pushq %rax
    movq $54, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3001
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3002
.L3001:
.L3002:
    movq -264(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3011
    leaq .STR166(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
    jmp .L3012
.L3011:
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
    jz .L3021
    movq $1, %rax
    movq %rax, -320(%rbp)
    jmp .L3022
.L3021:
.L3022:
    movq -256(%rbp), %rax
    pushq %rax
    movq $31, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3031
    movq $1, %rax
    movq %rax, -320(%rbp)
    jmp .L3032
.L3031:
.L3032:
    movq -256(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3041
    movq $1, %rax
    movq %rax, -320(%rbp)
    jmp .L3042
.L3041:
.L3042:
    movq -320(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3051
    leaq .STR167(%rip), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
    jmp .L3052
.L3051:
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_get_expression_type
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3061
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_variable
    jmp .L3062
.L3061:
    movq -352(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
.L3062:
.L3052:
.L3012:
    jmp .L2942
.L2941:
    movq -48(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_get_expression_type
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3071
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_variable
    jmp .L3072
.L3071:
    movq -352(%rbp), %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_add_variable_with_type
.L3072:
.L2942:
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
    addq $8, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -184(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR168(%rip), %rax
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
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L2872:
    jmp .L2862
.L2861:
.L2862:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L2852
.L2851:
.L2852:
    movq -24(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3081
    movq $16, %rax
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
    movq %rax, -400(%rbp)
    movq -400(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
    leaq .STR49(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR169(%rip), %rax
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
    jmp .L3082
.L3081:
.L3082:
    movq -24(%rbp), %rax
    pushq %rax
    movq $17, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3091
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -408(%rbp)
    movq -408(%rbp), %rax
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
    movq %rax, -416(%rbp)
    movq -416(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_lvalue_address
    leaq .STR170(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR49(%rip), %rax
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
    call memory_get_int32@PLT
    movq %rax, -424(%rbp)
    movq -424(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3101
    leaq .STR171(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3102
.L3101:
.L3102:
    movq -424(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3111
    leaq .STR172(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3112
.L3111:
.L3112:
    movq -424(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3121
    leaq .STR173(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3122
.L3121:
.L3122:
    movq -424(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3131
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR174(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR52(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR175(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR53(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR48(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3132
.L3131:
.L3132:
    leaq .STR176(%rip), %rax
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
    jmp .L3092
.L3091:
.L3092:
    movq -24(%rbp), %rax
    pushq %rax
    movq $11, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3141
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -440(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $1, %rax
    movq %rax, -448(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $2, %rax
    movq %rax, -456(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -464(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -472(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -480(%rbp)
    movq $32, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -488(%rbp)
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -496(%rbp)
    movq $48, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -504(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_add_variable
    movq -464(%rbp), %rax
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
    addq $8, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -528(%rbp)
    movq -472(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR168(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
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
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -480(%rbp), %rax
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
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR177(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -536(%rbp)
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -544(%rbp)
    movq -544(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR13(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
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
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR179(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR180(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR181(%rip), %rax
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
    movq $0, %rax
    movq %rax, -112(%rbp)
.L3151:    movq -112(%rbp), %rax
    pushq %rax
    movq -504(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3152
    movq -112(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -568(%rbp)
    movq -568(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -112(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -112(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3151
.L3152:
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3161
    movq -488(%rbp), %rax
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
    jmp .L3162
.L3161:
.L3162:
    movq -488(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3171
    leaq .STR182(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR41(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3172
.L3171:
.L3172:
    movq $0, %rax
    pushq %rax
    leaq .STR13(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
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
    leaq .STR36(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    leaq .STR175(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR183(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    pushq %rax
    leaq .STR168(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -528(%rbp), %rax
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
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -448(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR184(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -576(%rbp)
    movq -576(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -456(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR177(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -584(%rbp)
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -592(%rbp)
    movq -592(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR49(%rip), %rax
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
    jmp .L3142
.L3141:
.L3142:
    movq -24(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3181
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -600(%rbp)
    movq -600(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR185(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR186(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR187(%rip), %rax
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
    jmp .L3182
.L3181:
.L3182:
    movq -24(%rbp), %rax
    pushq %rax
    movq $5, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3191
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -440(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $1, %rax
    movq %rax, -624(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $2, %rax
    movq %rax, -632(%rbp)
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
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
    call codegen_generate_expression
    leaq .STR72(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -624(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR188(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
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
    movq %rax, -656(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -664(%rbp)
    movq $0, %rax
    movq %rax, -672(%rbp)
.L3201:    movq -672(%rbp), %rax
    pushq %rax
    movq -664(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3202
    movq -672(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -656(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -680(%rbp)
    movq -680(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -672(%rbp), %rax
    addq $1, %rax
    movq %rax, -672(%rbp)
    jmp .L3201
.L3202:
    movq $0, %rax
    pushq %rax
    leaq .STR184(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -632(%rbp), %rax
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
    movq -624(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR177(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -696(%rbp)
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -704(%rbp)
    movq -704(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -696(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -704(%rbp), %rax
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
    movq %rax, -712(%rbp)
    movq $40, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -720(%rbp)
    movq $0, %rax
    movq %rax, -728(%rbp)
.L3211:    movq -728(%rbp), %rax
    pushq %rax
    movq -720(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3212
    movq -728(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -712(%rbp), %rax
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
    call codegen_generate_statement
    movq -728(%rbp), %rax
    addq $1, %rax
    movq %rax, -728(%rbp)
    jmp .L3211
.L3212:
    movq -632(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR177(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -752(%rbp)
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -752(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -760(%rbp)
    movq -760(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -752(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -760(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3192
.L3191:
.L3192:
    movq -24(%rbp), %rax
    pushq %rax
    movq $6, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3221
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    pushq %rax
    movq $1000000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3231
    jmp .L3232
.L3231:
.L3232:
    movq -432(%rbp), %rax
    movq %rax, -440(%rbp)
    movq -432(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -440(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $1, %rax
    movq %rax, -784(%rbp)
    movq -440(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $2, %rax
    movq %rax, -792(%rbp)
    movq -792(%rbp), %rax
    pushq %rax
    movq -784(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call codegen_push_loop_context
    movq $0, %rax
    pushq %rax
    leaq .STR177(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -784(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    movq %rax, -536(%rbp)
    movq $0, %rax
    pushq %rax
    movq -536(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR178(%rip), %rax
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
    movq %rax, -640(%rbp)
    movq -640(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    leaq .STR72(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -792(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR188(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -648(%rbp)
    movq -648(%rbp), %rax
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
    movq %rax, -824(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -832(%rbp)
    movq $0, %rax
    movq %rax, -840(%rbp)
.L3241:    movq -840(%rbp), %rax
    pushq %rax
    movq -832(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3242
    movq -840(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -824(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -848(%rbp)
    movq -848(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -840(%rbp), %rax
    addq $1, %rax
    movq %rax, -840(%rbp)
    jmp .L3241
.L3242:
    movq $0, %rax
    pushq %rax
    leaq .STR184(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -784(%rbp), %rax
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
    movq -792(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR177(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -584(%rbp)
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -872(%rbp)
    movq -872(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq -584(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -872(%rbp), %rax
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
    jmp .L3222
.L3221:
.L3222:
    movq -24(%rbp), %rax
    pushq %rax
    movq $9, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3251
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_current_loop_context
    movq %rax, -880(%rbp)
    movq -880(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3261
    movq $8, %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -888(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR184(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -888(%rbp), %rax
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
    jmp .L3262
.L3261:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L3262:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3252
.L3251:
.L3252:
    movq -24(%rbp), %rax
    pushq %rax
    movq $10, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3271
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call codegen_current_loop_context
    movq %rax, -880(%rbp)
    movq -880(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3281
    movq $0, %rax
    pushq %rax
    movq -880(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -904(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR184(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -904(%rbp), %rax
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
    jmp .L3282
.L3281:
    movq $1, %rax
    pushq %rax
    popq %rdi
    call exit_with_code@PLT
.L3282:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3272
.L3271:
.L3272:
    movq -24(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3291
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -912(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -920(%rbp)
    movq $0, %rax
    movq %rax, -928(%rbp)
    movq $1, %rax
    movq %rax, -936(%rbp)
.L3301:    movq -928(%rbp), %rax
    pushq %rax
    movq -920(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3302
    movq -928(%rbp), %rax
    pushq %rax
    movq -912(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_char_at@PLT
    movq %rax, -944(%rbp)
    movq $10, %rax
    movq %rax, -952(%rbp)
    movq -936(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3311
    movq -944(%rbp), %rax
    pushq %rax
    movq -952(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3321
    movq $0, %rax
    pushq %rax
    leaq .STR189(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3322
.L3321:
.L3322:
    movq $0, %rax
    pushq %rax
    leaq -936(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3312
.L3311:
.L3312:
    movq $2, %rax
    movq %rax, -960(%rbp)
    movq -960(%rbp), %rax
    pushq %rax
    popq %rdi
    call memory_allocate@PLT
    movq %rax, -968(%rbp)
    movq -944(%rbp), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -968(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq $1, %rax
    pushq %rax
    movq -968(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_byte@PLT
    movq $0, %rax
    pushq %rax
    movq -968(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -968(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -944(%rbp), %rax
    pushq %rax
    movq -952(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3331
    movq $1, %rax
    pushq %rax
    leaq -936(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3332
.L3331:
.L3332:
    movq -928(%rbp), %rax
    addq $1, %rax
    pushq %rax
    leaq -928(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3301
.L3302:
    movq -936(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3341
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
    jmp .L3342
.L3341:
.L3342:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3292
.L3291:
.L3292:
    movq -24(%rbp), %rax
    pushq %rax
    movq $4, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3351
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -976(%rbp)
    movq -976(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    movq -976(%rbp), %rax
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
    jz .L3361
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR191(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3362
.L3361:
    movq -56(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3371
    movq -976(%rbp), %rax
    addq $8, %rax
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
    jz .L3381
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3382
.L3381:
.L3382:
    movq -256(%rbp), %rax
    pushq %rax
    movq $42, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3391
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3392
.L3391:
.L3392:
    movq -256(%rbp), %rax
    pushq %rax
    movq $48, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3401
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3402
.L3401:
.L3402:
    movq -256(%rbp), %rax
    pushq %rax
    movq $49, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3411
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3412
.L3411:
.L3412:
    movq -256(%rbp), %rax
    pushq %rax
    movq $52, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3421
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3422
.L3421:
.L3422:
    movq -256(%rbp), %rax
    pushq %rax
    movq $54, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3431
    movq $1, %rax
    movq %rax, -264(%rbp)
    jmp .L3432
.L3431:
.L3432:
    movq -264(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3441
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR191(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3442
.L3441:
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3442:
    jmp .L3372
.L3371:
    movq -56(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3451
    movq $8, %rax
    pushq %rax
    movq -976(%rbp), %rax
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
    jz .L3461
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
    addq $16, %rax
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
    jz .L3471
    leaq .STR166(%rip), %rax
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
    jz .L3481
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR191(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3482
.L3481:
    leaq .STR167(%rip), %rax
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
    jz .L3491
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3492
.L3491:
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3492:
.L3482:
    jmp .L3472
.L3471:
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3472:
    jmp .L3462
.L3461:
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3462:
    jmp .L3452
.L3451:
    movq $0, %rax
    pushq %rax
    leaq .STR190(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR192(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3452:
.L3372:
.L3362:
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3352
.L3351:
.L3352:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3501
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1096(%rbp)
    movq -1096(%rbp), %rax
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
    jmp .L3502
.L3501:
.L3502:
    movq -24(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3511
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3512
.L3511:
.L3512:
    movq -24(%rbp), %rax
    pushq %rax
    movq $7, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3521
    movq $8, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1104(%rbp)
    movq -1104(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_expression
    movq $0, %rax
    pushq %rax
    leaq .STR193(%rip), %rax
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
    movq %rax, -432(%rbp)
    movq -432(%rbp), %rax
    movq %rax, -1120(%rbp)
    movq -432(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $28, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1120(%rbp), %rax
    pushq %rax
    popq %rdi
    call integer_to_string@PLT
    pushq %rax
    leaq .STR194(%rip), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call string_concat@PLT
    movq %rax, -632(%rbp)
    movq $16, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1136(%rbp)
    movq $24, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1144(%rbp)
    movq $0, %rax
    movq %rax, -112(%rbp)
.L3531:    movq -112(%rbp), %rax
    pushq %rax
    movq -1136(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3532
    movq -112(%rbp), %rax
    pushq %rax
    movq $64, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1160(%rbp)
    movq -1144(%rbp), %rax
    addq -1160(%rbp), %rax
    movq %rax, -1168(%rbp)
    movq $0, %rax
    pushq %rax
    movq -1168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1176(%rbp)
    movq $8, %rax
    pushq %rax
    movq -1168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1184(%rbp)
    movq $16, %rax
    pushq %rax
    movq -1168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1192(%rbp)
    movq $24, %rax
    pushq %rax
    movq -1168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -504(%rbp)
    movq $32, %rax
    pushq %rax
    movq -1168(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -496(%rbp)
    movq -112(%rbp), %rax
    addq $1, %rax
    movq %rax, -1216(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR195(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1120(%rbp), %rax
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
    leaq .STR196(%rip), %rax
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
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR197(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR198(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR199(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR200(%rip), %rax
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
    leaq .STR201(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1176(%rbp), %rax
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
    movq -1136(%rbp), %rax
    subq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3541
    movq $0, %rax
    pushq %rax
    leaq .STR202(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1120(%rbp), %rax
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
    leaq .STR196(%rip), %rax
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
    leaq .STR203(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L3542
.L3541:
    movq $0, %rax
    pushq %rax
    leaq .STR204(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR205(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L3542:
    movq -1184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3551
    movq $0, %rax
    pushq %rax
    leaq .STR206(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR198(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    movq %rax, -1224(%rbp)
.L3561:    movq -1224(%rbp), %rax
    pushq %rax
    movq -1184(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3562
    movq -1224(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1232(%rbp)
    movq $8, %rax
    addq -1232(%rbp), %rax
    movq %rax, -1240(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR31(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1240(%rbp), %rax
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
    leaq .STR207(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1224(%rbp), %rax
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
    addq $8, %rax
    movq %rax, -1256(%rbp)
    movq -1256(%rbp), %rax
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
    leaq .STR208(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1256(%rbp), %rax
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
    movq -1224(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -1192(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1264(%rbp)
    movq $0, %rax
    pushq %rax
    leaq .STR209(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -1264(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR210(%rip), %rax
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
    movq %rax, -1272(%rbp)
    movq $24, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1280(%rbp)
    movq -1272(%rbp), %rax
    pushq %rax
    movq -1280(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3571
    movq -1280(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1288(%rbp)
    movq -1288(%rbp), %rax
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
    movq -1288(%rbp), %rax
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
    movq %rax, -1304(%rbp)
    movq -1304(%rbp), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    jmp .L3572
.L3571:
.L3572:
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -1272(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -1320(%rbp)
    movq -1264(%rbp), %rax
    pushq %rax
    popq %rdi
    call string_duplicate@PLT
    pushq %rax
    movq -1320(%rbp), %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1256(%rbp), %rax
    pushq %rax
    movq -1320(%rbp), %rax
    addq $8, %rax
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
    movq -1320(%rbp), %rax
    addq $16, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    movq -1272(%rbp), %rax
    addq $1, %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq -1224(%rbp), %rax
    addq $1, %rax
    movq %rax, -1224(%rbp)
    jmp .L3561
.L3562:
    jmp .L3552
.L3551:
.L3552:
    movq $0, %rax
    movq %rax, -1336(%rbp)
.L3581:    movq -1336(%rbp), %rax
    pushq %rax
    movq -504(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3582
    movq -1336(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    movq -496(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -1344(%rbp)
    movq -1344(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    movq -1336(%rbp), %rax
    addq $1, %rax
    movq %rax, -1336(%rbp)
    jmp .L3581
.L3582:
    movq -1184(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3591
    movq $0, %rax
    movq %rax, -1224(%rbp)
.L3601:    movq -1224(%rbp), %rax
    pushq %rax
    movq -1184(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3602
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1272(%rbp)
    movq -1272(%rbp), %rax
    subq -1184(%rbp), %rax
    addq -1224(%rbp), %rax
    movq %rax, -1376(%rbp)
    movq $8, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -176(%rbp)
    movq -1376(%rbp), %rax
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
    movq %rax, -464(%rbp)
    movq -1376(%rbp), %rax
    pushq %rax
    movq $24, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $16, %rax
    pushq %rax
    movq -176(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_integer@PLT
    movq %rax, -1400(%rbp)
    movq -464(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1400(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq -1224(%rbp), %rax
    addq $1, %rax
    movq %rax, -1224(%rbp)
    jmp .L3601
.L3602:
    movq $16, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -1272(%rbp)
    movq -1272(%rbp), %rax
    subq -1184(%rbp), %rax
    pushq %rax
    movq $12, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    jmp .L3592
.L3591:
.L3592:
    movq $0, %rax
    pushq %rax
    leaq .STR211(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    movq -632(%rbp), %rax
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
    addq $1, %rax
    movq %rax, -112(%rbp)
    jmp .L3531
.L3532:
    movq $0, %rax
    pushq %rax
    movq -632(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -32(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR212(%rip), %rax
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
    jmp .L3522
.L3521:
.L3522:
    movq $0, %rax
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
    jz .L3611
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3612
.L3611:
.L3612:
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
    movq $16, %rax
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
    movq $16, %rax
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
    movq $512, %rax
    pushq %rax
    movq $44, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $512, %rax
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
    movq $8, %rax
    pushq %rax
    movq $68, %rax
    pushq %rax
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    movq $8, %rax
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
    movq $0, %rax
    pushq %rax
    movq $72, %rax
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
    jz .L3621
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
    jmp .L3622
.L3621:
.L3622:
    movq -16(%rbp), %rax
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
    jz .L3631
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
    jz .L3641
    movq -16(%rbp), %rax
    pushq %rax
    popq %rdi
    call file_close_fd
    jmp .L3642
.L3641:
.L3642:
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
    addq -56(%rbp), %rax
    addq -64(%rbp), %rax
    addq -72(%rbp), %rax
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
    jz .L3651
    movq $0, %rax
    movq %rax, -96(%rbp)
.L3661:    movq -96(%rbp), %rax
    pushq %rax
    movq -80(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3662
    movq -96(%rbp), %rax
    pushq %rax
    movq $32, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -104(%rbp)
    movq -88(%rbp), %rax
    addq -104(%rbp), %rax
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
    jz .L3671
    movq -120(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3672
.L3671:
.L3672:
    movq -128(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3681
    movq -128(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3682
.L3681:
.L3682:
    movq -96(%rbp), %rax
    addq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L3661
.L3662:
    jmp .L3652
.L3651:
.L3652:
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
    addq -56(%rbp), %rax
    addq -64(%rbp), %rax
    addq -72(%rbp), %rax
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
    jz .L3691
    movq $0, %rax
    movq %rax, -96(%rbp)
.L3701:    movq -96(%rbp), %rax
    pushq %rax
    movq -200(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3702
    movq -96(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -224(%rbp)
    movq -208(%rbp), %rax
    addq -224(%rbp), %rax
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
    jz .L3711
    movq -240(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3712
.L3711:
.L3712:
    movq -248(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3721
    movq -248(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3722
.L3721:
.L3722:
    movq -96(%rbp), %rax
    addq $1, %rax
    movq %rax, -96(%rbp)
    jmp .L3701
.L3702:
    jmp .L3692
.L3691:
.L3692:
    movq -88(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3731
    movq -88(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3732
.L3731:
.L3732:
    movq -208(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3741
    movq -208(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3742
.L3741:
.L3742:
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
    jz .L3751
    movq -264(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3752
.L3751:
.L3752:
    movq $72, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -272(%rbp)
    movq -272(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3761
    movq -272(%rbp), %rax
    pushq %rax
    popq %rdi
    call hashtable_destroy
    jmp .L3762
.L3761:
.L3762:
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    jmp .L3632
.L3631:
.L3632:
    movq $0, %rax
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
    jz .L3771
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
    jmp .L3772
.L3771:
.L3772:
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
    addq $8, %rax
    pushq %rax
    movq -56(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_integer@PLT
    movq -32(%rbp), %rax
    addq $1, %rax
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
    jz .L3781
    movq -16(%rbp), %rax
    subq $1, %rax
    pushq %rax
    movq $64, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_int32@PLT
    jmp .L3782
.L3781:
.L3782:
    movq $0, %rax
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
    jz .L3791
    movq $56, %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    subq $1, %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -40(%rbp)
    movq -24(%rbp), %rax
    addq -40(%rbp), %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L3792
.L3791:
.L3792:
    movq $0, %rax
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
    leaq .STR213(%rip), %rax
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
    leaq .STR56(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
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
    movq $6, %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    popq %rdi
    call allocate@PLT
    movq %rax, -40(%rbp)
    leaq .STR216(%rip), %rax
    pushq %rax
    movq $0, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR217(%rip), %rax
    pushq %rax
    movq $8, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR218(%rip), %rax
    pushq %rax
    movq $16, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR219(%rip), %rax
    pushq %rax
    movq $24, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR220(%rip), %rax
    pushq %rax
    movq $32, %rax
    pushq %rax
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call memory_set_pointer@PLT
    leaq .STR221(%rip), %rax
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
    leaq .STR222(%rip), %rax
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
    jz .L3801
    movq -56(%rbp), %rax
    pushq %rax
    movq $2, %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3811
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
    jmp .L3812
.L3811:
.L3812:
    jmp .L3802
.L3801:
.L3802:
    leaq .STR229(%rip), %rax
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
.L3821:    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3822
    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3831
    movq $0, %rax
    movq %rax, -80(%rbp)
    jmp .L3832
.L3831:
.L3832:
    movq -72(%rbp), %rax
    pushq %rax
    movq -48(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setge %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3841
    movq $0, %rax
    movq %rax, -80(%rbp)
    jmp .L3842
.L3841:
.L3842:
    movq -80(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3851
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
    addq $8, %rax
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
    jz .L3861
    leaq .STR1(%rip), %rax
    movq %rax, -120(%rbp)
    jmp .L3862
.L3861:
.L3862:
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
    addq -152(%rbp), %rax
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
    leaq .STR31(%rip), %rax
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
    leaq .STR230(%rip), %rax
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
    leaq .STR165(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -72(%rbp), %rax
    addq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L3852
.L3851:
.L3852:
    jmp .L3821
.L3822:
    movq -48(%rbp), %rax
    movq %rax, -72(%rbp)
.L3871:    movq -72(%rbp), %rax
    pushq %rax
    movq -56(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3872
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
    addq $8, %rax
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
    addq -152(%rbp), %rax
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
    subq -48(%rbp), %rax
    movq %rax, -264(%rbp)
    movq -264(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    movq %rax, -272(%rbp)
    movq $16, %rax
    addq -272(%rbp), %rax
    movq %rax, -280(%rbp)
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
    leaq .STR168(%rip), %rax
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
    leaq .STR231(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq -72(%rbp), %rax
    addq $1, %rax
    movq %rax, -72(%rbp)
    jmp .L3871
.L3872:
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
    jz .L3881
    movq $0, %rax
    movq %rax, -312(%rbp)
.L3891:    movq -312(%rbp), %rax
    pushq %rax
    movq -296(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3892
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
    jz .L3901
    movq -328(%rbp), %rax
    pushq %rax
    movq -8(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call codegen_generate_statement
    jmp .L3902
.L3901:
.L3902:
    movq -312(%rbp), %rax
    addq $1, %rax
    movq %rax, -312(%rbp)
    jmp .L3891
.L3892:
    jmp .L3882
.L3881:
.L3882:
    movq $1, %rax
    movq %rax, -344(%rbp)
    movq -296(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3911
    movq -296(%rbp), %rax
    subq $1, %rax
    movq %rax, -352(%rbp)
    movq -352(%rbp), %rax
    pushq %rax
    movq $8, %rax
    popq %rbx
    imulq %rbx, %rax
    pushq %rax
    leaq -352(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    movq -352(%rbp), %rax
    pushq %rax
    movq -304(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -360(%rbp)
    movq -360(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setne %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3921
    movq $0, %rax
    pushq %rax
    movq -360(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_int32@PLT
    movq %rax, -368(%rbp)
    movq -368(%rbp), %rax
    pushq %rax
    movq $3, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3931
    movq $0, %rax
    pushq %rax
    leaq -344(%rbp), %rbx
    popq %rax
    movq %rax, (%rbx)
    jmp .L3932
.L3931:
.L3932:
    jmp .L3922
.L3921:
.L3922:
    jmp .L3912
.L3911:
.L3912:
    movq -344(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3941
    leaq .STR232(%rip), %rax
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
    leaq .STR234(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L3942
.L3941:
.L3942:
    movq -40(%rbp), %rax
    pushq %rax
    popq %rdi
    call deallocate@PLT
    movq $0, %rax
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
    jz .L3951
    jmp .L3952
.L3951:
.L3952:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3961
    movq $0, %rax
    movq %rax, -32(%rbp)
    jmp .L3962
.L3961:
.L3962:
    movq -32(%rbp), %rax
    pushq %rax
    movq $1000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3971
    movq $0, %rax
    movq %rax, -32(%rbp)
    jmp .L3972
.L3971:
.L3972:
    movq -32(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3981
    movq $0, %rax
    pushq %rax
    leaq .STR235(%rip), %rax
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
.L3991:    movq -64(%rbp), %rax
    pushq %rax
    movq -32(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L3992
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
    leaq .STR236(%rip), %rax
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
    leaq .STR237(%rip), %rax
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
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L3991
.L3992:
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
    jmp .L3982
.L3981:
.L3982:
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
    jz .L4001
    movq $0, %rax
    movq %rax, -104(%rbp)
    jmp .L4002
.L4001:
.L4002:
    movq -104(%rbp), %rax
    pushq %rax
    movq $10000, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4011
    movq $0, %rax
    movq %rax, -104(%rbp)
    jmp .L4012
.L4011:
.L4012:
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
    jz .L4021
    leaq .STR238(%rip), %rax
    pushq %rax
    popq %rdi
    call print_string
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4022
.L4021:
.L4022:
    movq $0, %rax
    movq %rax, -64(%rbp)
.L4031:    movq -64(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4032
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
    jz .L4041
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
    jz .L4051
    movq -168(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setg %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4061
    movq $0, %rax
    movq %rax, -176(%rbp)
.L4071:    movq -176(%rbp), %rax
    pushq %rax
    movq -168(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4072
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
    jz .L4081
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
    jz .L4091
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret
    jmp .L4092
.L4091:
.L4092:
    jmp .L4082
.L4081:
.L4082:
    movq -176(%rbp), %rax
    addq $1, %rax
    movq %rax, -176(%rbp)
    jmp .L4071
.L4072:
    jmp .L4062
.L4061:
.L4062:
    jmp .L4052
.L4051:
.L4052:
    jmp .L4042
.L4041:
.L4042:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4031
.L4032:
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
    addq -264(%rbp), %rax
    addq -272(%rbp), %rax
    addq -280(%rbp), %rax
    movq %rax, -288(%rbp)
    movq -288(%rbp), %rax
    pushq %rax
    movq $0, %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4101
    movq $0, %rax
    movq %rax, -288(%rbp)
    jmp .L4102
.L4101:
.L4102:
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
    jz .L4111
    leaq .STR239(%rip), %rax
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
.L4121:    movq -64(%rbp), %rax
    pushq %rax
    movq -288(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4122
    movq -64(%rbp), %rax
    pushq %rax
    movq $16, %rax
    popq %rbx
    imulq %rbx, %rax
    addq $8, %rax
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
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR240(%rip), %rax
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
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4121
.L4122:
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L4112
.L4111:
.L4112:
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
.L4131:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4132
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
    jz .L4141
    movq $1, %rax
    movq %rax, -368(%rbp)
    movq -352(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L4142
.L4141:
.L4142:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4131
.L4132:
    movq -368(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4151
    leaq .STR241(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rax, -64(%rbp)
.L4161:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4162
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
    jz .L4171
    movq $0, %rax
    pushq %rax
    leaq .STR213(%rip), %rax
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
    leaq .STR178(%rip), %rax
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
    jz .L4181
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
    leaq .STR242(%rip), %rax
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
    jmp .L4182
.L4181:
    movq $0, %rax
    pushq %rax
    leaq .STR243(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
.L4182:
    jmp .L4172
.L4171:
.L4172:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4161
.L4162:
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
    jmp .L4152
.L4151:
.L4152:
    movq $0, %rax
    movq %rax, -480(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L4191:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4192
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
    jz .L4201
    movq $1, %rax
    movq %rax, -480(%rbp)
    movq -352(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L4202
.L4201:
.L4202:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4191
.L4192:
    movq -480(%rbp), %rax
    pushq %rax
    movq $1, %rax
    popq %rbx
    cmpq %rax, %rbx
    sete %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4211
    leaq .STR244(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    movq $0, %rax
    movq %rax, -64(%rbp)
.L4221:    movq -64(%rbp), %rax
    pushq %rax
    movq -352(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4222
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
    jz .L4231
    movq $0, %rax
    pushq %rax
    leaq .STR213(%rip), %rax
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
    leaq .STR178(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    movq $0, %rax
    pushq %rax
    leaq .STR245(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    popq %rdx
    call file_write_buffered@PLT
    jmp .L4232
.L4231:
.L4232:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4221
.L4222:
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
    jmp .L4212
.L4211:
.L4212:
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
    leaq .STR133(%rip), %rax
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
    leaq .STR251(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR252(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR253(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR254(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR255(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR256(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR257(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR258(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR259(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR260(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR261(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR262(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR263(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR264(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR265(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR260(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR266(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR267(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR263(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR264(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
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
    leaq .STR234(%rip), %rax
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
    leaq .STR268(%rip), %rax
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
    leaq .STR269(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR270(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR271(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR272(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR273(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR274(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR275(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR276(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR72(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR277(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR278(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR279(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR280(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR72(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR281(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR48(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR282(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR283(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR284(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR285(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR286(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR275(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR287(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR288(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR289(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
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
    leaq .STR290(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR251(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR291(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR253(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR292(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR255(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR256(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR293(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR294(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR259(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR260(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR295(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR262(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR263(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR264(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR265(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR260(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR266(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR267(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR263(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR264(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR133(%rip), %rax
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
    leaq .STR233(%rip), %rax
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
    leaq .STR0(%rip), %rax
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
    leaq .STR296(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    leaq .STR297(%rip), %rax
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
    movq $0, %rax
    movq %rax, -64(%rbp)
.L4241:    movq -64(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4242
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
    jz .L4251
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    leaq .STR222(%rip), %rax
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
    jz .L4261
    leaq .STR298(%rip), %rax
    pushq %rax
    movq -24(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call emit_line
    jmp .L4262
.L4261:
.L4262:
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
    jmp .L4252
.L4251:
.L4252:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4241
.L4242:
    movq $0, %rax
    movq %rax, -608(%rbp)
    movq $0, %rax
    movq %rax, -64(%rbp)
.L4271:    movq -64(%rbp), %rax
    pushq %rax
    movq -104(%rbp), %rax
    popq %rbx
    cmpq %rax, %rbx
    setl %al
    movzbq %al, %rax
    testq %rax, %rax
    jz .L4272
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
    jz .L4281
    movq $0, %rax
    pushq %rax
    movq -144(%rbp), %rax
    pushq %rax
    popq %rdi
    popq %rsi
    call memory_get_pointer@PLT
    movq %rax, -152(%rbp)
    leaq .STR222(%rip), %rax
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
    jz .L4291
    movq $1, %rax
    movq %rax, -608(%rbp)
    movq -104(%rbp), %rax
    movq %rax, -64(%rbp)
    jmp .L4292
.L4291:
.L4292:
    jmp .L4282
.L4281:
.L4282:
    movq -64(%rbp), %rax
    addq $1, %rax
    movq %rax, -64(%rbp)
    jmp .L4271
.L4272:
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
    leaq .STR299(%rip), %rax
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

.section .note.GNU-stack
