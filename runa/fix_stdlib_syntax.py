#!/usr/bin/env python3
"""
Emergency Runa Standard Library Syntax Repair Script
Fixes the 384,000+ syntax errors across 602 files
"""

import os
import re
import glob
from pathlib import Path

def fix_file_syntax(file_path):
    """Fix syntax errors in a single Runa file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove "plus" tokens at start of lines
        content = re.sub(r'^\s*plus\s+', '    ', content, flags=re.MULTILINE)
        
        # Fix 2: Replace "minus" in descriptions with "-"
        content = re.sub(r'(\w+)\s+minus\s+(\w+)', r'\1 - \2', content)
        
        # Fix 3: Fix Type definitions
        content = re.sub(r'Type\s+(\w+)\s+is\s+Dictionary\s+with:', r'Type called "\1":', content)
        content = re.sub(r'Type\s+(\w+)\s+is\s+Enum\s+with\s+variants:', r'Type \1 is:', content)
        
        # Fix 4: Remove stray "plus" in middle of lines
        content = re.sub(r'\s+plus\s+', ' ', content)
        
        # Fix 5: Remove stray "minus" in middle of lines (but preserve mathematical minus)
        content = re.sub(r'(\w)\s+minus\s+(\w)', r'\1 - \2', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main repair function"""
    stdlib_path = "/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/src/stdlib"
    
    if not os.path.exists(stdlib_path):
        print(f"Stdlib path not found: {stdlib_path}")
        return
    
    # Find all .runa files
    runa_files = list(Path(stdlib_path).rglob("*.runa"))
    
    print(f"Found {len(runa_files)} .runa files to process")
    
    fixed_count = 0
    for i, file_path in enumerate(runa_files):
        if fix_file_syntax(file_path):
            fixed_count += 1
        
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1}/{len(runa_files)} files, fixed {fixed_count} files")
    
    print(f"Repair complete! Fixed {fixed_count}/{len(runa_files)} files")

if __name__ == "__main__":
    main()