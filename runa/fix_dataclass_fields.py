#!/usr/bin/env python3
"""
Fix dataclass field ordering issues in AST files.

This script identifies fields without default values in dataclasses that inherit from 
classes with default values, and fixes them by adding appropriate defaults.
"""

import re
import os
from pathlib import Path

def fix_dataclass_fields(file_path):
    """Fix dataclass field ordering issues in a Python file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to find dataclass fields without defaults that come after inheritance
    # This is a simplified approach - we'll add default values to required fields
    patterns_to_fix = [
        # Field definitions that need default values
        (r'(\s+)(\w+): str\n', r'\1\2: str = ""\n'),
        (r'(\s+)(\w+): int\n', r'\1\2: int = 0\n'),
        (r'(\s+)(\w+): bool\n', r'\1\2: bool = False\n'),
        (r'(\s+)(\w+): float\n', r'\1\2: float = 0.0\n'),
        (r'(\s+)(\w+): List\[(.*?)\]\n', r'\1\2: List[\3] = None\n'),
        (r'(\s+)(\w+): Dict\[(.*?)\]\n', r'\1\2: Dict[\3] = None\n'),
        (r'(\s+)(\w+): Any\n', r'\1\2: Any = None\n'),
        # Enum types
        (r'(\s+)(\w+): Py(\w+)\n', r'\1\2: Py\3 = None\n'),
        (r'(\s+)(\w+): TS(\w+)\n', r'\1\2: TS\3 = None\n'),
        (r'(\s+)(\w+): JS(\w+)\n', r'\1\2: JS\3 = None\n'),
        (r'(\s+)(\w+): Java(\w+)\n', r'\1\2: Java\3 = None\n'),
        (r'(\s+)(\w+): CSharp(\w+)\n', r'\1\2: CSharp\3 = None\n'),
        (r'(\s+)(\w+): Cpp(\w+)\n', r'\1\2: Cpp\3 = None\n'),
        (r'(\s+)(\w+): SQL(\w+)\n', r'\1\2: SQL\3 = None\n'),
        # Some specific field patterns
        (r'(\s+)id: str\n', r'\1id: str = ""\n'),
        (r'(\s+)name: str\n', r'\1name: str = ""\n'),
        (r'(\s+)operator: str\n', r'\1operator: str = ""\n'),
        (r'(\s+)op: (\w+)\n', r'\1op: \2 = None\n'),
        (r'(\s+)value: Any\n', r'\1value: Any = None\n'),
        (r'(\s+)left: (\w+Expression)\n', r'\1left: \2 = None\n'),
        (r'(\s+)right: (\w+Expression)\n', r'\1right: \2 = None\n'),
        (r'(\s+)operand: (\w+Expression)\n', r'\1operand: \2 = None\n'),
        (r'(\s+)test: (\w+Expression)\n', r'\1test: \2 = None\n'),
        (r'(\s+)body: List\[(\w+)\]\n', r'\1body: List[\2] = None\n'),
        (r'(\s+)orelse: List\[(\w+)\]\n', r'\1orelse: List[\2] = None\n'),
        (r'(\s+)(\w+): (\w+Expression)\n', r'\1\2: \3 = None\n'),
        (r'(\s+)(\w+): (\w+Statement)\n', r'\1\2: \3 = None\n'),
    ]
    
    original_content = content
    for pattern, replacement in patterns_to_fix:
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
            if fix_dataclass_fields(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
    
    print(f"\nFixed dataclass issues in {fixed_count} files.")

if __name__ == "__main__":
    main()