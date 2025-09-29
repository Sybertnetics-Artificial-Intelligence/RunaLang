#!/bin/bash
# Comprehensive fix for v0.0.7.3's incorrect calling convention
# v0.0.7.3 has TWO bugs:
# 1. Uses Windows x64 ABI (rcx for 4th arg) instead of System V (r8 for 4th arg)
# 2. Pushes arguments in wrong order (pushes forward, pops backward = reversed args)

for file in stage1/*.s; do
    if [ -f "$file" ]; then
        echo "Fixing ABI in $file"

        # Create a temporary file for processing
        tmp_file="${file}.tmp"
        cp "$file" "$tmp_file"

        # First fix: Replace popq %rcx with popq %r8 for 4th argument
        sed -i 's/popq %rcx$/popq %r8/g' "$tmp_file"

        # Fix function prologues to expect 4th parameter in r8 instead of rcx
        sed -i 's/movq %rcx, -32(%rbp)/movq %r8, -32(%rbp)/g' "$tmp_file"

        # Second fix: Reverse the order of pushq instructions before function calls
        # This is complex and needs careful handling
        python3 - "$tmp_file" "$file" << 'EOF'
import sys
import re

def fix_argument_order(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    result = []
    i = 0
    while i < len(lines):
        # Look for patterns of multiple pushq followed by multiple popq and a call
        if 'pushq' in lines[i]:
            # Collect all consecutive pushq instructions
            push_lines = []
            j = i
            while j < len(lines) and 'pushq' in lines[j]:
                push_lines.append(lines[j])
                j += 1

            # Check if this is followed by popq instructions
            if j < len(lines) and 'popq' in lines[j]:
                pop_lines = []
                k = j
                while k < len(lines) and 'popq' in lines[k]:
                    pop_lines.append(lines[k])
                    k += 1

                # Check if this is followed by a call instruction
                if k < len(lines) and 'call' in lines[k]:
                    # We found a function call pattern
                    # Check if it's a 4-argument call (4 pushq, 4 popq)
                    if len(push_lines) == 4 and len(pop_lines) == 4:
                        # Reverse the push order for 4-arg calls
                        result.extend(reversed(push_lines))
                    elif len(push_lines) == 3 and len(pop_lines) == 3:
                        # Reverse the push order for 3-arg calls
                        result.extend(reversed(push_lines))
                    elif len(push_lines) == 2 and len(pop_lines) == 2:
                        # Reverse the push order for 2-arg calls
                        result.extend(reversed(push_lines))
                    else:
                        # Keep original order for other patterns
                        result.extend(push_lines)

                    # Add the pop and call instructions
                    result.extend(pop_lines)
                    result.append(lines[k])
                    i = k + 1
                else:
                    # Not a function call pattern, keep original
                    result.append(lines[i])
                    i += 1
            else:
                # Not followed by popq, keep original
                result.append(lines[i])
                i += 1
        else:
            result.append(lines[i])
            i += 1

    with open(output_file, 'w') as f:
        f.writelines(result)

fix_argument_order(sys.argv[1], sys.argv[2])
EOF

        # Clean up temp file
        rm "$tmp_file"
    fi
done

echo "Comprehensive ABI fix complete"