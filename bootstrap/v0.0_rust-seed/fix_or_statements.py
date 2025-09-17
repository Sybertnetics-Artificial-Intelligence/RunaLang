import re
import sys

with open(sys.argv[1], 'r') as f:
    content = f.read()

# Pattern to match If statements with Or
pattern = r'(\s+)If (.+?) Or (.+?):'

def replace_or(match):
    indent = match.group(1)
    cond1 = match.group(2)
    cond2 = match.group(3)
    
    return f"""{indent}Let should_process be 0
{indent}If {cond1}:
{indent}    Set should_process to 1
{indent}End If
{indent}If {cond2}:
{indent}    Set should_process to 1
{indent}End If
{indent}If should_process is equal to 1:"""

content = re.sub(pattern, replace_or, content)

# Fix the corresponding End If statements (we now have nested Ifs)
# This is tricky and might need manual adjustment

print(content)
