#!/usr/bin/env python3
"""
Comprehensive fix for SQL AST dataclass inheritance issues.

This script systematically finds ALL required fields in dataclass subclasses
and makes them optional with appropriate defaults.
"""

import re
from pathlib import Path

def fix_all_sql_dataclass_issues():
    """Fix ALL dataclass inheritance issues in SQL AST."""
    sql_ast_file = Path("src/runa/languages/tier1/sql/sql_ast.py")
    
    if not sql_ast_file.exists():
        print(f"File not found: {sql_ast_file}")
        return False
    
    # Read the file
    with open(sql_ast_file, 'r') as f:
        content = f.read()
    
    # Backup original file
    backup_file = sql_ast_file.with_suffix('.py.backup_comprehensive')
    with open(backup_file, 'w') as f:
        f.write(content)
    print(f"Backup created: {backup_file}")
    
    # Find all @dataclass classes that inherit from SQL base classes
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a dataclass that inherits from a SQL base class
        if line.strip() == "@dataclass" and i + 1 < len(lines):
            class_line = lines[i + 1]
            # Check if it inherits from a SQL class
            if re.match(r'^class \w+\(SQL\w+\):', class_line):
                # This is a SQL dataclass - scan its fields
                fixed_lines.append(line)  # @dataclass
                fixed_lines.append(class_line)  # class line
                
                i += 2
                # Skip docstring if present
                if i < len(lines) and lines[i].strip().startswith('"""'):
                    while i < len(lines) and not (lines[i].strip().endswith('"""') and len(lines[i].strip()) > 3):
                        fixed_lines.append(lines[i])
                        i += 1
                    if i < len(lines):  # Add the closing """
                        fixed_lines.append(lines[i])
                        i += 1
                
                # Now process field definitions
                while i < len(lines):
                    field_line = lines[i]
                    
                    # Stop when we hit a method or the end of the class
                    if (field_line.strip().startswith("def ") or 
                        field_line.strip().startswith("@") or
                        (field_line.strip() and not field_line.startswith("    ")) or
                        field_line.strip().startswith("class ")):
                        break
                    
                    # Check if this is a field definition without a default
                    field_match = re.match(r'^(\s+)(\w+):\s*([^=\n]+?)(\s*)$', field_line)
                    if field_match:
                        indent, field_name, field_type, trailing = field_match.groups()
                        field_type = field_type.strip()
                        
                        # Add appropriate default based on type
                        if field_type.startswith('List['):
                            default = " = field(default_factory=list)"
                        elif field_type.startswith('Dict['):
                            default = " = field(default_factory=dict)"
                        elif field_type.startswith('Set['):
                            default = " = field(default_factory=set)"
                        elif field_type.startswith('Optional[') or field_type.startswith('Union['):
                            default = " = None"
                        elif 'SQLIdentifier' in field_type or 'SQLExpression' in field_type or 'SQL' in field_type:
                            default = " = None"
                        elif field_type == 'str':
                            default = ' = ""'
                        elif field_type == 'int':
                            default = ' = 0'
                        elif field_type == 'float':
                            default = ' = 0.0'
                        elif field_type == 'bool':
                            default = ' = False'
                        elif "'SQL" in field_type:  # Forward references
                            default = " = None"
                        else:
                            # For unknown types, make them Optional
                            if not field_type.startswith('Optional['):
                                field_type = f"Optional[{field_type}]"
                            default = " = None"
                        
                        # Reconstruct the line with default
                        fixed_line = f"{indent}{field_name}: {field_type}{default}{trailing}"
                        fixed_lines.append(fixed_line)
                    else:
                        # Not a field definition, keep as-is
                        fixed_lines.append(field_line)
                    
                    i += 1
                
                # Don't increment i here since we stopped at a non-field line
                continue
        
        # Not a dataclass or not inheriting from SQL class
        fixed_lines.append(line)
        i += 1
    
    # Reconstruct content
    fixed_content = '\n'.join(fixed_lines)
    
    # Write the fixed content
    with open(sql_ast_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"Comprehensively fixed all dataclass issues in {sql_ast_file}")
    return True

if __name__ == "__main__":
    fix_all_sql_dataclass_issues()