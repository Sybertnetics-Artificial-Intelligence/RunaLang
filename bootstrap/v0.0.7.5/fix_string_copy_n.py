#!/usr/bin/env python3
"""
Fix the specific string_copy_n argument ordering bug in v0.0.7.3 generated assembly.

The bug: v0.0.7.3 pushes function arguments in order but pops them in reverse,
causing the arguments to be reversed.

For string_copy_n(dest, src, start, length):
- Currently: pushes dest,start,src,length → pops to rdi,rsi,rdx,r8 → gets length,src,start,dest
- Fixed: pushes length,src,start,dest → pops to rdi,rsi,rdx,r8 → gets dest,src,start,length
"""

import sys
import re

def fix_string_copy_n_calls(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    result = []
    i = 0

    while i < len(lines):
        # Look for string_copy_n calls
        if i + 8 < len(lines) and 'call string_copy_n' in lines[i + 8]:
            # We found a string_copy_n call
            # The pattern is 4 pushq, then 4 popq, then call
            # We need to reverse the order of the 4 pushq

            # Check if this matches our expected pattern
            if all('pushq' in lines[i+j] for j in range(4)) and \
               all('popq' in lines[i+4+j] for j in range(4)):
                # Reverse the push order
                push_lines = [lines[i+j] for j in range(4)]
                result.extend(reversed(push_lines))
                # Keep the pops and call as is
                result.extend(lines[i+4:i+9])
                i += 9
            else:
                result.append(lines[i])
                i += 1
        else:
            result.append(lines[i])
            i += 1

    # Write the fixed file
    with open(input_file, 'w') as f:
        f.writelines(result)

    print(f"Fixed {input_file}")

if __name__ == "__main__":
    # Fix string_copy_n in lexer.s specifically
    fix_string_copy_n_calls("stage1/lexer.s")