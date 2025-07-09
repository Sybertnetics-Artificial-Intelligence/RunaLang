#!/usr/bin/env python3
"""
Script to automatically fix dataclass field ordering issues in the Runa AST.

This script adds default values to all required fields in dataclasses that inherit
from ASTNode (which has default fields), fixing the "non-default argument follows
default argument" error.
"""

import re
import sys
from typing import Dict, List, Tuple

def fix_dataclass_fields(file_path: str) -> None:
    """Fix dataclass field ordering in the given file."""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Default values for common field types
    default_values = {
        'str': '""',
        'int': '0',
        'float': '0.0',
        'bool': 'False',
        'List[Expression]': 'field(default_factory=list)',
        'List[Statement]': 'field(default_factory=list)',
        'List[TypeExpression]': 'field(default_factory=list)',
        'List[Parameter]': 'field(default_factory=list)',
        'List[MatchCase]': 'field(default_factory=list)',
        'List[CatchClause]': 'field(default_factory=list)',
        'List[str]': 'field(default_factory=list)',
        'List[tuple[Expression, Expression]]': 'field(default_factory=list)',
        'List[Tuple[Expression, Expression]]': 'field(default_factory=list)',
        'List[Tuple[str, Expression]]': 'field(default_factory=list)',
        'List[tuple[str, Expression]]': 'field(default_factory=list)',
        'Expression': 'None',
        'Optional[Expression]': 'None',
        'TypeExpression': 'None',
        'Optional[TypeExpression]': 'None',
        'BinaryOperator': 'None',
        'Optional[BinaryOperator]': 'None',
        'UnaryOperator': 'None',
        'Pattern': 'None',
        'Statement': 'None',
        'Declaration': 'None',
    }
    
    # Find all dataclass definitions with inheritance from ASTNode hierarchy
    pattern = r'@dataclass\s*\nclass\s+(\w+)\((Expression|Statement|Declaration|TypeExpression|ASTNode)\):\s*\n(.*?)\n\s*def\s+'
    
    def fix_field(match):
        class_name = match.group(1)
        parent_class = match.group(2)
        class_body = match.group(3)
        
        print(f"Processing class {class_name} inheriting from {parent_class}")
        
        # Find field definitions
        field_pattern = r'^\s*(\w+):\s*([^=\n]+)$'
        lines = class_body.split('\n')
        fixed_lines = []
        
        for line in lines:
            field_match = re.match(field_pattern, line.strip())
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(2).strip()
                
                # Skip if field already has a default value
                if '=' in line:
                    fixed_lines.append(line)
                    continue
                
                # Add appropriate default value
                default_value = default_values.get(field_type)
                if not default_value:
                    # Handle more complex types
                    if field_type.startswith('List['):
                        default_value = 'field(default_factory=list)'
                    elif field_type.startswith('Optional[') or field_type.startswith('Union['):
                        default_value = 'None'
                    elif 'Expression' in field_type or 'Statement' in field_type or 'Declaration' in field_type:
                        default_value = 'None'
                        # Also make the type Optional if it isn't already
                        if not field_type.startswith('Optional['):
                            field_type = f'Optional[{field_type}]'
                    else:
                        # Default to None for unknown types and make them Optional
                        default_value = 'None'
                        if not field_type.startswith('Optional['):
                            field_type = f'Optional[{field_type}]'
                
                # Reconstruct the line with default value
                indent = len(line) - len(line.lstrip())
                fixed_line = ' ' * indent + f'{field_name}: {field_type} = {default_value}'
                fixed_lines.append(fixed_line)
                print(f"  Fixed field: {field_name}: {field_type} = {default_value}")
            else:
                fixed_lines.append(line)
        
        # Reconstruct the class
        fixed_body = '\n'.join(fixed_lines)
        return f'@dataclass\nclass {class_name}({parent_class}):\n{fixed_body}\n    def '
    
    # Apply the fixes
    original_content = content
    content = re.sub(pattern, fix_field, content, flags=re.MULTILINE | re.DOTALL)
    
    if content != original_content:
        print(f"Writing fixed content to {file_path}")
        with open(file_path, 'w') as f:
            f.write(content)
        print("Successfully fixed dataclass field ordering issues!")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    ast_file = "/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/src/runa/core/runa_ast.py"
    fix_dataclass_fields(ast_file)