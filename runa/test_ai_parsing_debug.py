#!/usr/bin/env python3
"""
Debug script to test AI construct parsing and identify hanging issues.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from runa.compiler.lexer import RunaLexer
from runa.compiler.parser import RunaParser

def test_simple_ai_parsing():
    """Test simple AI construct parsing to identify the issue."""
    print("Testing simple AI construct parsing...")
    
    # Test 1: Simple AI construct
    source1 = 'Ask coding_llm about "test"'
    print(f"Source 1: {source1}")
    
    try:
        lexer1 = RunaLexer(source1)
        tokens1 = lexer1.tokenize()
        print(f"Tokens 1: {[t.type.name for t in tokens1]}")
        
        parser1 = RunaParser(tokens1)
        program1 = parser1.parse()
        print(f"Program 1 parsed successfully: {program1 is not None}")
        
    except Exception as e:
        print(f"Error in test 1: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: More complex AI construct
    source2 = '''
Ask coding_llm about "How to implement quicksort in Python"
'''
    print(f"\nSource 2: {source2}")
    
    try:
        lexer2 = RunaLexer(source2)
        tokens2 = lexer2.tokenize()
        print(f"Tokens 2: {[t.type.name for t in tokens2]}")
        
        parser2 = RunaParser(tokens2)
        program2 = parser2.parse()
        print(f"Program 2 parsed successfully: {program2 is not None}")
        
    except Exception as e:
        print(f"Error in test 2: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_ai_parsing() 