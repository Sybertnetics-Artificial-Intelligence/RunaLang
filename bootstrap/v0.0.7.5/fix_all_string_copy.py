#!/usr/bin/env python3
"""
Fix ALL string_copy_n calls in lexer.s
"""

with open('stage1/lexer.s', 'r') as f:
    lines = f.readlines()

# Find all string_copy_n calls
import re
for i, line in enumerate(lines):
    if 'call string_copy_n' in line:
        print(f"Found string_copy_n at line {i+1}")

        # Look back for the 4 popq instructions
        if i >= 4:
            if all('popq' in lines[i-j] for j in range(1, 5)):
                print(f"  Has 4 popq before it")

                # Look further back for the 4 pairs of movq/pushq
                push_start = None
                push_count = 0
                for j in range(i-4, -1, -1):
                    if 'pushq' in lines[j]:
                        push_count += 1
                        if push_count == 4:
                            # Found the 4th (earliest) push
                            # Go back to find its corresponding movq
                            if j > 0 and 'movq' in lines[j-1]:
                                push_start = j - 1
                            else:
                                push_start = j
                            break

                if push_start and push_count == 4:
                    print(f"  Found 4 pushq starting at line {push_start+1}")
                    # Extract the 8 lines (4 pairs of movq/pushq)
                    orig_lines = lines[push_start:push_start+8]

                    # Print what we found
                    print("  Original order:")
                    for ol in orig_lines:
                        if 'movq' in ol:
                            # Extract the source operand
                            match = re.search(r'movq (.*), %rax', ol)
                            if match:
                                print(f"    {match.group(1)}")

# Now fix them - there are 3 calls
# Based on manual inspection:
# 1. Line 1514 - uses -96, -24, -120, -112
# 2. Line 1686 - uses -88, -24, -120, -112
# 3. Line 1827 - uses -88, -24, -120, -112

# For all: the correct order should be length, start_pos, source, dest
# So: -112, -24, -120, -96/-88

fixes = [
    (1506, [  # Line 1514 call
        "    movq -112(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -24(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -120(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -96(%rbp), %rax\n",
        "    pushq %rax\n"
    ]),
    (1674, [  # Line 1686 call (already done but let's ensure)
        "    movq -112(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -24(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -120(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -88(%rbp), %rax\n",
        "    pushq %rax\n"
    ]),
    (1819, [  # Line 1827 call
        "    movq -112(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -24(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -120(%rbp), %rax\n",
        "    pushq %rax\n",
        "    movq -88(%rbp), %rax\n",
        "    pushq %rax\n"
    ])
]

for start_line, new_lines in fixes:
    # Replace the 8 lines
    for i, new_line in enumerate(new_lines):
        if start_line - 1 + i < len(lines):
            lines[start_line - 1 + i] = new_line
    print(f"Fixed call starting at line {start_line}")

with open('stage1/lexer.s', 'w') as f:
    f.writelines(lines)

print("Fixed all string_copy_n calls in lexer.s")