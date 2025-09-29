#!/usr/bin/env python3
"""
Fix function call argument ordering in v0.0.7.3 generated assembly.
"""

import sys
import re

def fix_function_calls(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    result = []
    i = 0

    while i < len(lines):
        # Look for the pattern of 4 popq followed by a call
        if i + 4 < len(lines) and \
           'popq %rdi' in lines[i] and \
           'popq %rsi' in lines[i+1] and \
           'popq %rdx' in lines[i+2] and \
           'popq %r8' in lines[i+3] and \
           'call' in lines[i+4]:

            # We found a 4-argument function call
            # Now we need to find the 4 pushq instructions that precede it
            push_lines = []
            j = i - 1

            # Go backwards to find the 4 pushq instructions
            while j >= 0 and len(push_lines) < 4:
                if 'pushq' in lines[j]:
                    push_lines.insert(0, (j, lines[j]))
                j -= 1

            if len(push_lines) == 4:
                # We found all 4 pushq instructions
                # Mark them for reversal
                print(f"Found 4-arg call at line {i+5}: {lines[i+4].strip()}")

                # Remove the original push lines from result
                # (they were already added)
                for idx, _ in push_lines:
                    if idx < len(result):
                        result[idx] = None

                # Add them back in reverse order
                push_contents = [line for _, line in push_lines]
                first_push_idx = push_lines[0][0]

                # Inject reversed pushes at the position of the first push
                reversed_pushes = list(reversed(push_contents))

                # Find where to insert in result
                insert_pos = first_push_idx
                for k, reversed_push in enumerate(reversed_pushes):
                    if insert_pos + k < len(result):
                        result[insert_pos + k] = reversed_push

            # Add the popq and call instructions
            result.extend([lines[i], lines[i+1], lines[i+2], lines[i+3], lines[i+4]])
            i += 5

        elif i + 3 < len(lines) and \
             'popq %rdi' in lines[i] and \
             'popq %rsi' in lines[i+1] and \
             'popq %rdx' in lines[i+2] and \
             'call' in lines[i+3]:

            # 3-argument function call
            push_lines = []
            j = i - 1

            while j >= 0 and len(push_lines) < 3:
                if 'pushq' in lines[j]:
                    push_lines.insert(0, (j, lines[j]))
                j -= 1

            if len(push_lines) == 3:
                print(f"Found 3-arg call at line {i+4}: {lines[i+3].strip()}")

                for idx, _ in push_lines:
                    if idx < len(result):
                        result[idx] = None

                push_contents = [line for _, line in push_lines]
                first_push_idx = push_lines[0][0]
                reversed_pushes = list(reversed(push_contents))

                insert_pos = first_push_idx
                for k, reversed_push in enumerate(reversed_pushes):
                    if insert_pos + k < len(result):
                        result[insert_pos + k] = reversed_push

            result.extend([lines[i], lines[i+1], lines[i+2], lines[i+3]])
            i += 4

        else:
            result.append(lines[i])
            i += 1

    # Remove None entries and write back
    result = [line for line in result if line is not None]

    with open(filename, 'w') as f:
        f.writelines(result)

    print(f"Fixed {filename}")

# Fix all stage1 assembly files
for module in ['lexer', 'string_utils', 'parser', 'codegen', 'containers', 'hashtable', 'main']:
    fix_function_calls(f'stage1/{module}.s')