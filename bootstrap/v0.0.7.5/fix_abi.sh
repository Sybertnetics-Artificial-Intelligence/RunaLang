#!/bin/bash
# Fix v0.0.7.3's incorrect calling convention
# v0.0.7.3 uses Windows x64 ABI (rcx for 4th arg) instead of System V (r8 for 4th arg)

for file in stage1/*.s; do
    if [ -f "$file" ]; then
        echo "Fixing ABI in $file"
        # Before any 4+ argument function call, replace rcx with r8
        # This fixes calls to functions with 4+ arguments
        sed -i 's/popq %rcx$/popq %r8/g' "$file"

        # Fix function prologues to expect 4th parameter in r8 instead of rcx
        # Look for the pattern where functions save their 4th parameter
        sed -i 's/movq %rcx, -32(%rbp)/movq %r8, -32(%rbp)/g' "$file"

        # Also need to fix the initial register saving in string_copy_n specifically
        # After the 3rd param (rdx), the 4th should come from r8 not rcx
        sed -i '/string_copy_n:/,/^[a-zA-Z_]/ {
            /movq %rdi, -8(%rbp)/,/movq %rcx, -32(%rbp)/ {
                s/movq %rcx, -32(%rbp)/movq %r8, -32(%rbp)/g
            }
        }' "$file"
    fi
done

echo "ABI fix complete"