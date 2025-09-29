#!/bin/bash
# Fix the push order for string_copy_n calls in lexer.s

# For the call at line 1674-1686, we need to reverse the push order
# Original: pushes -88, -24, -120, -112 (word, start_pos, source, length)
# Fixed: pushes -112, -120, -24, -88 (length, source, start_pos, word)

# This will make it so when popped to rdi,rsi,rdx,r8, we get:
# rdi=word, rsi=source, rdx=start_pos, r8=length (correct!)

sed -i '1674,1681s/.*/    movq -112(%rbp), %rax\n    pushq %rax\n    movq -120(%rbp), %rax\n    pushq %rax\n    movq -24(%rbp), %rax\n    pushq %rax\n    movq -88(%rbp), %rax\n    pushq %rax/' stage1/lexer.s

# Fix the other string_copy_n calls similarly
# First call around line 1514
sed -i '1506,1513s/.*/    movq -112(%rbp), %rax\n    pushq %rax\n    movq -120(%rbp), %rax\n    pushq %rax\n    movq -24(%rbp), %rax\n    pushq %rax\n    movq -96(%rbp), %rax\n    pushq %rax/' stage1/lexer.s

# Third call around line 1827
sed -i '1819,1826s/.*/    movq -112(%rbp), %rax\n    pushq %rax\n    movq -120(%rbp), %rax\n    pushq %rax\n    movq -24(%rbp), %rax\n    pushq %rax\n    movq -88(%rbp), %rax\n    pushq %rax/' stage1/lexer.s

echo "Fixed push order for string_copy_n calls"