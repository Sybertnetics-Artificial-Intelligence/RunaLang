	.text
	.file	"test_minimal_runtime"
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	str_0@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movq	str_1@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movq	str_2@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movq	str_3@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movl	$42, %edi
	callq	rust_print_integer@PLT
	movq	str_4@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movq	str_5@GOTPCREL(%rip), %rdi
	movq	str_6@GOTPCREL(%rip), %rsi
	callq	rust_concat_strings@PLT
	movq	%rax, (%rsp)
	movq	str_7@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movq	(%rsp), %rdi
	callq	rust_print_string@PLT
	movq	str_4@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	movq	str_8@GOTPCREL(%rip), %rdi
	callq	rust_print_string@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.type	str_2,@object
	.section	.rodata,"a",@progbits
	.globl	str_2
	.p2align	3, 0x0
str_2:
	.quad	.str
	.size	str_2, 8

	.type	.str,@object
	.globl	.str
.str:
	.asciz	"SUCCESS\\n"
	.size	.str, 10

	.type	str_3,@object
	.globl	str_3
	.p2align	3, 0x0
str_3:
	.quad	.str.1
	.size	str_3, 8

	.type	.str.1,@object
	.globl	.str.1
	.p2align	4, 0x0
.str.1:
	.asciz	"Testing integer output: "
	.size	.str.1, 25

	.type	str_4,@object
	.globl	str_4
	.p2align	3, 0x0
str_4:
	.quad	.str.2
	.size	str_4, 8

	.type	.str.2,@object
	.globl	.str.2
.str.2:
	.asciz	"\\n"
	.size	.str.2, 3

	.type	str_1,@object
	.globl	str_1
	.p2align	3, 0x0
str_1:
	.quad	.str.3
	.size	str_1, 8

	.type	.str.3,@object
	.globl	.str.3
	.p2align	4, 0x0
.str.3:
	.asciz	"Testing basic output: "
	.size	.str.3, 23

	.type	str_6,@object
	.globl	str_6
	.p2align	3, 0x0
str_6:
	.quad	.str.4
	.size	str_6, 8

	.type	.str.4,@object
	.globl	.str.4
.str.4:
	.asciz	"Runa!"
	.size	.str.4, 6

	.type	str_8,@object
	.globl	str_8
	.p2align	3, 0x0
str_8:
	.quad	.str.5
	.size	str_8, 8

	.type	.str.5,@object
	.globl	.str.5
	.p2align	4, 0x0
.str.5:
	.asciz	"=== ALL TESTS PASSED ===\\n"
	.size	.str.5, 27

	.type	str_7,@object
	.globl	str_7
	.p2align	3, 0x0
str_7:
	.quad	.str.6
	.size	str_7, 8

	.type	.str.6,@object
	.globl	.str.6
	.p2align	4, 0x0
.str.6:
	.asciz	"Testing string concat: "
	.size	.str.6, 24

	.type	str_0,@object
	.globl	str_0
	.p2align	3, 0x0
str_0:
	.quad	.str.7
	.size	str_0, 8

	.type	.str.7,@object
	.globl	.str.7
	.p2align	4, 0x0
.str.7:
	.asciz	"=== MINIMAL RUNTIME TEST ===\\n"
	.size	.str.7, 31

	.type	str_5,@object
	.globl	str_5
	.p2align	3, 0x0
str_5:
	.quad	.str.8
	.size	str_5, 8

	.type	.str.8,@object
	.globl	.str.8
.str.8:
	.asciz	"Hello, "
	.size	.str.8, 8

	.section	".note.GNU-stack","",@progbits
