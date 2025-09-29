#!/usr/bin/env python3
"""
Specifically fix the string_copy_n calls in lexer.s by reversing push order.
"""

# Read the file
with open('stage1/lexer.s', 'r') as f:
    lines = f.readlines()

# Find and fix each string_copy_n call
# We know they're at specific line numbers
fixes = [
    # First call around 1514
    (1506, 1513),
    # Second call around 1686
    (1674, 1681),
    # Third call around 1827
    (1819, 1826)
]

for start, end in fixes:
    # Extract the push lines (adjusting for 0-based indexing)
    push_lines = lines[start-1:end]

    # Only process if they're all pushq instructions
    if all('pushq' in line or 'movq' in line for line in push_lines):
        # Group into pairs (movq + pushq)
        pairs = []
        for i in range(0, len(push_lines), 2):
            if i+1 < len(push_lines):
                pairs.append((push_lines[i], push_lines[i+1]))

        # Reverse the pairs
        reversed_pairs = list(reversed(pairs))

        # Flatten back to lines
        reversed_lines = []
        for movq, pushq in reversed_pairs:
            reversed_lines.append(movq)
            reversed_lines.append(pushq)

        # Replace in the original
        for i, line in enumerate(reversed_lines):
            lines[start-1+i] = line

        print(f"Fixed string_copy_n call at lines {start}-{end}")

# Write the fixed file
with open('stage1/lexer.s', 'w') as f:
    f.writelines(lines)

print("Successfully fixed lexer.s")