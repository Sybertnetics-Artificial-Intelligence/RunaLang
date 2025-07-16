#!/usr/bin/env python3
"""
Comprehensive fix for all dataclass field ordering issues in AST files.

This script identifies and fixes all fields without default values in dataclasses 
that inherit from classes with default values.
"""

import re
import os
from pathlib import Path

def fix_dataclass_fields_comprehensive(file_path):
    """Fix all dataclass field ordering issues in a Python file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # More comprehensive patterns to fix all remaining issues
    patterns_to_fix = [
        # Basic types
        (r'(\s+)(\w+): str\n', r'\1\2: str = ""\n'),
        (r'(\s+)(\w+): int\n', r'\1\2: int = 0\n'),
        (r'(\s+)(\w+): bool\n', r'\1\2: bool = False\n'),
        (r'(\s+)(\w+): float\n', r'\1\2: float = 0.0\n'),
        
        # Collection types
        (r'(\s+)(\w+): List\[(.*?)\]\n', r'\1\2: List[\3] = None\n'),
        (r'(\s+)(\w+): Dict\[(.*?)\]\n', r'\1\2: Dict[\3] = None\n'),
        (r'(\s+)(\w+): Tuple\[(.*?)\]\n', r'\1\2: Tuple[\3] = None\n'),
        (r'(\s+)(\w+): Set\[(.*?)\]\n', r'\1\2: Set[\3] = None\n'),
        (r'(\s+)(\w+): Any\n', r'\1\2: Any = None\n'),
        (r'(\s+)(\w+): Optional\[(.*?)\]\n', r'\1\2: Optional[\3] = None\n'),
        (r'(\s+)(\w+): Union\[(.*?)\]\n', r'\1\2: Union[\3] = None\n'),
        
        # Quoted type annotations
        (r"(\s+)(\w+): '(\w+)'\n", r"\1\2: '\3' = None\n"),
        (r"(\s+)(\w+): \"(\w+)\"\n", r'\1\2: "\3" = None\n'),
        
        # Language-specific AST node types
        (r'(\s+)(\w+): Py(\w+)\n', r'\1\2: Py\3 = None\n'),
        (r'(\s+)(\w+): TS(\w+)\n', r'\1\2: TS\3 = None\n'),
        (r'(\s+)(\w+): JS(\w+)\n', r'\1\2: JS\3 = None\n'),
        (r'(\s+)(\w+): Java(\w+)\n', r'\1\2: Java\3 = None\n'),
        (r'(\s+)(\w+): CSharp(\w+)\n', r'\1\2: CSharp\3 = None\n'),
        (r'(\s+)(\w+): Cpp(\w+)\n', r'\1\2: Cpp\3 = None\n'),
        (r'(\s+)(\w+): SQL(\w+)\n', r'\1\2: SQL\3 = None\n'),
        
        # Expression and Statement types
        (r'(\s+)(\w+): (\w+Expression)\n', r'\1\2: \3 = None\n'),
        (r'(\s+)(\w+): (\w+Statement)\n', r'\1\2: \3 = None\n'),
        (r'(\s+)(\w+): (\w+Node)\n', r'\1\2: \3 = None\n'),
        
        # Common field names that need fixing
        (r'(\s+)args: \'PyArguments\'\n', r'\1args: \'PyArguments\' = None\n'),
        (r'(\s+)module: Optional\[str\]\n', r'\1module: Optional[str] = None\n'),
        (r'(\s+)arg: Optional\[str\]\n', r'\1arg: Optional[str] = None\n'),
        
        # Fix remaining specific patterns
        (r'(\s+)(\w+): (\w+)Type\n', r'\1\2: \3Type = None\n'),
        (r'(\s+)(\w+): (\w+)Operator\n', r'\1\2: \3Operator = None\n'),
        (r'(\s+)(\w+): (\w+)Context\n', r'\1\2: \3Context = None\n'),
    ]
    
    original_content = content
    
    # Apply all patterns
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)
    
    # Additional pass to catch any remaining patterns like 'type: Optional[Expression]'
    # Fix patterns that might have been missed
    additional_patterns = [
        (r'(\s+)type: Optional\[(\w+Expression)\]\n', r'\1type: Optional[\2] = None\n'),
        (r'(\s+)(\w+): (\w+)\[(\w+)\]\n(?!\s*=)', r'\1\2: \3[\4] = None\n'),
    ]
    
    for pattern, replacement in additional_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Only write if there were changes
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Fixed dataclass fields in {file_path}")
        return True
    return False

def main():
    """Fix dataclass issues in all tier 1 language AST files."""
    runa_dir = Path("src/runa/languages/tier1")
    
    if not runa_dir.exists():
        print(f"Directory {runa_dir} not found. Make sure you're in the runa project root.")
        return
    
    ast_files = []
    for lang_dir in runa_dir.iterdir():
        if lang_dir.is_dir():
            # Try different naming patterns
            potential_names = [
                f"{lang_dir.name}_ast.py",  # Standard pattern
                "py_ast.py",  # Python
                "js_ast.py",  # JavaScript  
                "ts_ast.py",  # TypeScript
            ]
            for name in potential_names:
                ast_file = lang_dir / name
                if ast_file.exists():
                    ast_files.append(ast_file)
                    break
    
    print(f"Found {len(ast_files)} AST files to check:")
    for file_path in ast_files:
        print(f"  {file_path}")
    
    fixed_count = 0
    for file_path in ast_files:
        try:
            if fix_dataclass_fields_comprehensive(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
    
    print(f"\nFixed dataclass issues in {fixed_count} files.")

if __name__ == "__main__":
    main()