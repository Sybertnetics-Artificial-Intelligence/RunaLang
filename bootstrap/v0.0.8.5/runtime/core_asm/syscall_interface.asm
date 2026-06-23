; ============================================================================
; syscall_interface.asm — STUB
; ============================================================================
; This file is a stub. The canonical syscall interface for Runa lives in
; pure Runa using the language's `Inline Assembly:` feature:
;
;   compiler/frontend/primitives/assembly/syscall.runa       — platform router
;   compiler/frontend/primitives/platform/<plat>/syscall.runa — per-platform impl
;
; The Linux x86-64 implementation is in
; compiler/frontend/primitives/platform/linux_x86_64/syscall.runa
; (2400+ lines, 467 process definitions). It provides syscall_0..syscall_6
; generic dispatchers plus named wrappers (syscall_read, syscall_write,
; syscall_mmap, syscall_munmap, syscall_open, syscall_close, syscall_stat,
; syscall_fstat, syscall_lseek, syscall_brk, syscall_exit, syscall_pipe,
; syscall_dup, syscall_dup2, syscall_fork, syscall_execve, syscall_wait4,
; syscall_kill, syscall_getpid, syscall_clone, syscall_futex,
; syscall_clock_gettime, syscall_nanosleep, syscall_socket, syscall_bind,
; syscall_listen, syscall_accept, syscall_connect, syscall_send, syscall_recv,
; syscall_select, syscall_poll, syscall_epoll_create1, syscall_epoll_ctl,
; syscall_epoll_wait, syscall_getrandom, and many more) plus full constant
; tables (SYS_*, O_*, PROT_*, MAP_*, SEEK_*, STDIN_FILENO, etc.).
;
; This file exists only because core_asm/ is the documented home for
; ultra-low-level hot paths. As of v0.0.8.5 the syscall interface does not
; need a separate external assembly file — Runa's inline assembly is
; sufficient. If future hot paths benefit from a tight, hand-tuned external
; assembly entry point (e.g. a custom fast-path mmap allocator), they belong
; here. Until then this is a placeholder for that future.

section .text

; ============================================================================
; End of syscall_interface.asm (stub — see header)
; ============================================================================
