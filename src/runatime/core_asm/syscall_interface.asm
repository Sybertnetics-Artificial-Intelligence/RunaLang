; syscall_interface.asm
; Core syscall interface for Runa runtime
; Provides low-level syscall access for all platforms

section .text

; Linux x86_64 syscall interface
%ifdef LINUX_X64

global runa_syscall0
global runa_syscall1
global runa_syscall2
global runa_syscall3
global runa_syscall6
global runa_read_memory
global runa_allocate_memory
global runa_free_memory
global runa_read_byte
global runa_write_byte

; syscall with 0 arguments
runa_syscall0:
    mov rax, rdi        ; syscall number
    syscall
    ret

; syscall with 1 argument
runa_syscall1:
    mov rax, rdi        ; syscall number
    mov rdi, rsi        ; arg1
    syscall
    ret

; syscall with 2 arguments
runa_syscall2:
    mov rax, rdi        ; syscall number
    mov rdi, rsi        ; arg1
    mov rsi, rdx        ; arg2
    syscall
    ret

; syscall with 3 arguments
runa_syscall3:
    mov rax, rdi        ; syscall number
    mov rdi, rsi        ; arg1
    mov rsi, rdx        ; arg2
    mov rdx, rcx        ; arg3
    syscall
    ret

; syscall with 6 arguments
runa_syscall6:
    mov rax, rdi        ; syscall number
    mov rdi, rsi        ; arg1
    mov rsi, rdx        ; arg2
    mov rdx, rcx        ; arg3
    mov r10, r8         ; arg4 (r10, not rcx!)
    mov r8, r9          ; arg5
    mov r9, [rsp+8]     ; arg6 from stack
    syscall
    ret

; Read memory at address into buffer
runa_read_memory:
    mov rcx, rdx        ; size to counter
    xor rax, rax        ; clear return
.copy_loop:
    test rcx, rcx
    jz .done
    mov al, [rdi]       ; read byte
    mov [rsi], al       ; write to buffer
    inc rdi
    inc rsi
    dec rcx
    jmp .copy_loop
.done:
    mov rax, rdx        ; return size
    ret

; Allocate memory using mmap
; Input: rdi = size
; Output: rax = pointer to allocated memory (or -1 on error)
runa_allocate_memory:
    mov rsi, rdi        ; size to allocate
    xor rdi, rdi        ; addr = NULL
    mov rdx, 0x3        ; prot = PROT_READ | PROT_WRITE
    mov r10, 0x22       ; flags = MAP_PRIVATE | MAP_ANONYMOUS
    mov r8, -1          ; fd = -1
    xor r9, r9          ; offset = 0
    mov rax, 9          ; mmap syscall number
    syscall
    ret

; Free memory using munmap
; Input: rdi = pointer, rsi = size
; Output: rax = 0 on success, -1 on error
runa_free_memory:
    mov rax, 11         ; munmap syscall number
    syscall
    ret

; Read a byte from memory
; Input: rdi = address, rsi = offset
; Output: rax = byte value
runa_read_byte:
    add rdi, rsi        ; add offset to base address
    movzx rax, byte [rdi] ; read byte and zero-extend
    ret

; Write a byte to memory
; Input: rdi = address, rsi = offset, rdx = value
; Output: none
runa_write_byte:
    add rdi, rsi        ; add offset to base address
    mov [rdi], dl       ; write low byte of rdx
    ret

%endif ; LINUX_X64

; Linux ARM64 syscall interface
%ifdef LINUX_ARM64

global runa_syscall0
global runa_syscall1
global runa_syscall2
global runa_syscall3
global runa_syscall6
global runa_read_memory

; ARM64 uses different syntax - this is placeholder
; Actual ARM64 assembly would use svc instruction

%endif ; LINUX_ARM64

; macOS/Darwin x86_64 syscall interface
%ifdef DARWIN_X64

global _runa_syscall0
global _runa_syscall1
global _runa_syscall2
global _runa_syscall3
global _runa_syscall6
global _runa_read_memory

; macOS syscalls use different convention
; syscall number in rax with 0x2000000 offset for 64-bit

_runa_syscall0:
    mov rax, rdi
    or rax, 0x2000000   ; BSD syscall flag
    syscall
    ret

_runa_syscall1:
    mov rax, rdi
    or rax, 0x2000000
    mov rdi, rsi
    syscall
    ret

_runa_syscall2:
    mov rax, rdi
    or rax, 0x2000000
    mov rdi, rsi
    mov rsi, rdx
    syscall
    ret

_runa_syscall3:
    mov rax, rdi
    or rax, 0x2000000
    mov rdi, rsi
    mov rsi, rdx
    mov rdx, rcx
    syscall
    ret

_runa_syscall6:
    mov rax, rdi
    or rax, 0x2000000
    mov rdi, rsi
    mov rsi, rdx
    mov rdx, rcx
    mov r10, r8
    mov r8, r9
    mov r9, [rsp+8]
    syscall
    ret

_runa_read_memory:
    ; Same as Linux version
    mov rcx, rdx
    xor rax, rax
.copy_loop:
    test rcx, rcx
    jz .done
    mov al, [rdi]
    mov [rsi], al
    inc rdi
    inc rsi
    dec rcx
    jmp .copy_loop
.done:
    mov rax, rdx
    ret

%endif ; DARWIN_X64