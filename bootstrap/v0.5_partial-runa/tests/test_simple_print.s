	.text
	.file	"test_simple_print"
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	str_0@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.type	str_0,@object
	.section	.rodata,"a",@progbits
	.globl	str_0
	.p2align	3, 0x0
str_0:
	.quad	.str
	.size	str_0, 8

	.type	.str,@object
	.globl	.str
.str:
	.asciz	"Hello\\n"
	.size	.str, 8

	.section	".note.GNU-stack","",@progbits
