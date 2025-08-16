#!/usr/bin/env python3
"""
Runa Indentation Fixer v2
Improved version that fixes the specific patterns we've been seeing.
"""

import re
import sys
from pathlib import Path

def fix_runa_indentation(content: str) -> str:
    """Fix specific Runa indentation issues based on our manual fixing patterns."""
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
        
        # Fix broken statements on same line - pattern: "statement Let/Set/If/..."
        for keyword in ['Let ', 'Set ', 'If ', 'Return ', 'For ', 'While ']:
            if keyword in line and not line.strip().startswith(keyword.strip()):
                # Find where the new statement starts
                keyword_pos = line.find(' ' + keyword)
                if keyword_pos > 0:
                    # Split the line
                    first_part = line[:keyword_pos]
                    second_part = line[keyword_pos + 1:]  # Remove the space
                    
                    # Keep same indentation level for the second statement
                    indent = len(line) - len(line.lstrip())
                    
                    fixed_lines.append(first_part)
                    fixed_lines.append(' ' * indent + second_part)
                    i += 1
                    break
            elif ' ' + keyword in line and line.count(' ' + keyword) > 1:
                # Multiple instances of the same keyword
                parts = line.split(' ' + keyword)
                if len(parts) > 1:
                    indent = len(line) - len(line.lstrip())
                    fixed_lines.append(parts[0])
                    for part in parts[1:]:
                        fixed_lines.append(' ' * indent + keyword + part)
                    i += 1
                    break
        else:
            # Fix missing arithmetic operators in obvious cases
            # Pattern: word + word = word plus word (but be careful)
            fixed_line = line
            
            # Fix "Break Add" -> "Break\n    Add"
            if 'Break Add' in line:
                indent = len(line) - len(line.lstrip())
                parts = line.split('Break Add')
                fixed_line = parts[0] + 'Break'
                fixed_lines.append(fixed_line)
                fixed_lines.append(' ' * (indent + 4) + 'Add' + parts[1])
                i += 1
                continue
                
            # Fix missing "plus" operators in specific patterns
            # Pattern: "a b" where both are identifiers, should be "a plus b"
            words = fixed_line.split()
            if len(words) >= 5 and words[0] in ['Let', 'Set'] and words[2] in ['be', 'to']:
                # Look for missing operators in assignment
                expr_start = 3 if words[0] == 'Let' else 3
                expr_part = ' '.join(words[expr_start:])
                
                # Conservative fixes for obvious patterns
                if re.search(r'\b(\w+)\s+(\w+)\b', expr_part) and 'with' not in expr_part and 'as' not in expr_part:
                    # Look for specific missing operators
                    expr_part = re.sub(r'\b(\w+)\s+(\w+)\s+(\w+)\b', r'\1 plus \2 plus \3', expr_part)
                    expr_part = re.sub(r'\b(\w+)\s+-\s+(\w+)\b', r'\1 minus \2', expr_part)
                    fixed_line = ' '.join(words[:expr_start]) + ' ' + expr_part
            
            # Fix missing operators in specific contexts we've seen
            missing_ops_patterns = [
                (r'\bi\s+3\b', 'i plus 3'),  # Common pattern: i 3 -> i plus 3
                (r'\baa_observed\s+ab_observed\b', 'aa_observed plus ab_observed'),
                (r'\btotal_length\s+contig\.length\b', 'total_length plus contig.length'),
                (r'\bchi_square\s+Math\.pow\b', 'chi_square plus Math.pow'),
                (r'\bmean1\s+0\.001\b', 'mean1 plus 0.001'),
                (r'\bmean2\s+0\.001\b', 'mean2 plus 0.001'),
                (r'\bmean1\s+mean2\b', 'mean1 plus mean2'),
                (r'\bn\s+-\s+i\s+1\b', 'n minus i plus 1'),
                (r'\b(\w+)\s+fractional_day\b', r'\1 plus fractional_day'),
                (r'\b(\w+)\s+ra_temp\b', r'\1 plus ra_temp'),
                (r'\b(\w+)\s+l_temp\b', r'\1 minus l_temp'),
            ]
            
            for pattern, replacement in missing_ops_patterns:
                fixed_line = re.sub(pattern, replacement, fixed_line)
            
            # Fix Return statement field indentation
            if fixed_line.strip().startswith('Return') and 'with:' in fixed_line:
                fixed_lines.append(fixed_line)
                i += 1
                # Fix subsequent field lines
                while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('Process', 'Type', 'Note:', 'Import')):
                    field_line = lines[i]
                    if field_line.strip() and not field_line.startswith('        '):  # Not properly indented
                        base_indent = len(fixed_line) - len(fixed_line.lstrip())
                        field_content = field_line.strip()
                        fixed_lines.append(' ' * (base_indent + 4) + field_content)
                    else:
                        fixed_lines.append(field_line)
                    i += 1
                continue
                
            fixed_lines.append(fixed_line)
            i += 1
    
    return '\n'.join(fixed_lines)

def fix_file(file_path: Path) -> tuple[bool, str]:
    """Fix a single file and return (success, message)."""
    try:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        content = file_path.read_text(encoding='utf-8')
        backup_path.write_text(content, encoding='utf-8')
        
        fixed_content = fix_runa_indentation(content)
        
        if content != fixed_content:
            file_path.write_text(fixed_content, encoding='utf-8')
            return True, f"Fixed indentation issues in {file_path} (backup: {backup_path})"
        else:
            backup_path.unlink()  # Remove backup if no changes
            return True, f"No indentation issues found in {file_path}"
            
    except Exception as e:
        return False, f"Error processing {file_path}: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_indentation_v2.py <file_path>")
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