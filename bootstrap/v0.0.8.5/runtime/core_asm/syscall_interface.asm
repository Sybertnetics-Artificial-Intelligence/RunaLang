; syscall_interface.asm - System Call Interface Assembly
; Ultra-fast syscall interface for maximum performance
; Part of the 1% Assembly portion of the runtime

section .data
    ; Syscall numbers (Linux x86-64)
    SYS_READ equ 0
    SYS_WRITE equ 1
    SYS_OPEN equ 2
    SYS_CLOSE equ 3
    SYS_MMAP equ 9
    SYS_MUNMAP equ 11
    SYS_EXIT equ 60

section .text
    global syscall_read
    global syscall_write
    global syscall_mmap
    global syscall_munmap

; Read from file descriptor
; Input: RDI = fd, RSI = buffer, RDX = count
; Output: RAX = bytes read
syscall_read:
    mov rax, SYS_READ
    syscall
    ret

; Write to file descriptor
; Input: RDI = fd, RSI = buffer, RDX = count
; Output: RAX = bytes written
syscall_write:
    mov rax, SYS_WRITE
    syscall
    ret

; Memory map
; Input: RDI = addr, RSI = length, RDX = prot, R10 = flags, R8 = fd, R9 = offset
; Output: RAX = mapped address
syscall_mmap:
    mov rax, SYS_MMAP
    syscall
    ret

; Memory unmap
; Input: RDI = addr, RSI = length
; Output: RAX = 0 on success, -1 on error
syscall_munmap:
    mov rax, SYS_MUNMAP
    syscall
    ret
