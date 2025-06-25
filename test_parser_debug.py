#!/usr/bin/env python3
"""
Debug test to check if parser can handle Display statements correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'runa', 'src'))

from runa.compiler.lexer import RunaLexer
from runa.compiler.parser import RunaParser

def test_display_parsing():
    """Test parsing of Display statements."""
    
    # Test simple display
    source1 = 'Display "Hello"'
    print(f"Testing: {source1}")
    
    lexer = RunaLexer()
    try:
        tokens1 = lexer.tokenize(source1)
        print("Tokens:", [f"{t.type.name}:{t.value}" for t in tokens1])
        
        parser = RunaParser()
        print("Starting parse...")
        program1 = parser.parse(tokens1)
        print("Parse completed successfully:", program1 is not None)
        if program1:
            print(f"Program has {len(program1.statements)} statements")
        print()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print()

if __name__ == "__main__":
    test_display_parsing() 