#!/usr/bin/env python3
"""
Runa Indentation Fixer
Fixes the specific indentation issues we've been seeing in stdlib files.
"""

import re
import sys
from pathlib import Path

def fix_runa_indentation(content: str) -> str:
    """Fix common Runa indentation issues based on our manual fixing patterns."""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('Note:'):
            fixed_lines.append(line)
            i += 1
            continue
            
        # Fix broken line continuations (common pattern we've seen)
        if line.strip() and i + 1 < len(lines):
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            
            # Pattern: "Let x be something Let y be something" on one line
            if " Let " in line and not line.strip().startswith("Let"):
                parts = line.split(" Let ")
                if len(parts) > 1:
                    # Keep the indentation from the original line
                    indent = len(line) - len(line.lstrip())
                    fixed_lines.append(parts[0])
                    for part in parts[1:]:
                        fixed_lines.append(" " * indent + "Let " + part)
                    i += 1
                    continue
            
            # Pattern: Missing plus/minus/operators at line breaks
            missing_ops = [
                (r'(\w+)\s+(\w+)', r'\1 plus \2'),  # "a b" -> "a plus b"
                (r'(\w+)\s*-\s*(\w+)', r'\1 minus \2'),  # "a - b" -> "a minus b"  
            ]
            
        # Fix Return statement indentation
        if line.strip().startswith("Return") and "with:" in line:
            fixed_lines.append(line)
            # Next lines should be indented 4 more spaces
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("Process") and not lines[i].strip().startswith("Type") and not lines[i].strip().startswith("Note:"):
                next_line = lines[i]
                if next_line.strip() and not next_line.startswith("    "):
                    # This is a field that needs proper indentation
                    base_indent = len(line) - len(line.lstrip())
                    field_content = next_line.strip()
                    fixed_lines.append(" " * (base_indent + 4) + field_content)
                else:
                    fixed_lines.append(next_line)
                i += 1
            continue
            
        # Fix If statements followed by Return on same line
        if_return_pattern = r'^(\s*)(If .+):\s*(Return .+)$'
        match = re.match(if_return_pattern, line)
        if match:
            indent, if_part, return_part = match.groups()
            fixed_lines.append(f"{indent}{if_part}:")
            fixed_lines.append(f"{indent}    {return_part}")
            i += 1
            continue
            
        # Fix broken mathematical expressions with missing operators
        # Pattern: "a b" should be "a plus b" or similar
        if "be " in line and not any(op in line for op in ["plus", "minus", "multiplied", "divided"]):
            # Look for patterns like "Let x be a b c" which should have operators
            parts = line.split()
            if len(parts) > 4 and parts[0] == "Let" and parts[2] == "be":
                # Check if we have consecutive identifiers that need operators
                expression_part = " ".join(parts[3:])
                # This is a heuristic - if we have multiple words that aren't function calls, add 'plus'
                if re.search(r'\b\w+\s+\w+\b', expression_part) and "with" not in expression_part:
                    # Conservative fix - only fix obvious cases
                    pass
        
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

def fix_file(file_path: Path) -> tuple[bool, str]:
    """Fix a single file and return (success, message)."""
    try:
        content = file_path.read_text(encoding='utf-8')
        fixed_content = fix_runa_indentation(content)
        
        if content != fixed_content:
            file_path.write_text(fixed_content, encoding='utf-8')
            return True, f"Fixed indentation issues in {file_path}"
        else:
            return True, f"No indentation issues found in {file_path}"
            
    except Exception as e:
        return False, f"Error processing {file_path}: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_indentation.py <file_path>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    success, message = fix_file(file_path)
    print(message)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())