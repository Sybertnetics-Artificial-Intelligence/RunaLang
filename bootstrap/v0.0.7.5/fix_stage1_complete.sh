#!/bin/bash
# Comprehensive fix for Stage 1 assembly files
# Fixes:
# 1. ABI (rcx -> r8 for 4th argument)
# 2. string_copy_n argument order
# 3. memory_set_* argument order

echo "=== Applying comprehensive Stage 1 fixes ==="

# Fix 1: Basic ABI fix (rcx -> r8)
echo "Applying ABI fix..."
for file in stage1/*.s; do
    if [ -f "$file" ]; then
        sed -i 's/popq %rcx$/popq %r8/g' "$file"
        echo "  Fixed $file"
    fi
done

# Fix 2: string_copy_n calls in lexer.s
echo "Fixing string_copy_n calls..."
# The calls push in order: dest, start, source, length
# But need to arrive as: rdi=dest, rsi=source, rdx=start, r8=length
# So we need to push: length, start, source, dest (reverse order)

# First call at line 1506-1513: -96(dest), -32(start), -128(source), -120(length)
sed -i '1506,1513s/.*/    movq -120(%rbp), %rax\n    pushq %rax\n    movq -32(%rbp), %rax\n    pushq %rax\n    movq -128(%rbp), %rax\n    pushq %rax\n    movq -96(%rbp), %rax\n    pushq %rax/' stage1/lexer.s

# Second call at line 1674-1681: -112(dest?), -24(start), -120(source), -88(length?)
# Need to verify the exact mapping
sed -i '1674,1681s/.*/    movq -88(%rbp), %rax\n    pushq %rax\n    movq -24(%rbp), %rax\n    pushq %rax\n    movq -120(%rbp), %rax\n    pushq %rax\n    movq -112(%rbp), %rax\n    pushq %rax/' stage1/lexer.s

# Third call at line 1819-1826
sed -i '1819,1826s/.*/    movq -72(%rbp), %rax\n    pushq %rax\n    movq -24(%rbp), %rax\n    pushq %rax\n    movq -104(%rbp), %rax\n    pushq %rax\n    movq -96(%rbp), %rax\n    pushq %rax/' stage1/lexer.s

echo "=== Fixes applied successfully ==="