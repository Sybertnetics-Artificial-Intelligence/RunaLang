#!/usr/bin/env python3
"""
Minimal test script for Runa compiler
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_import():
    """Test basic import functionality."""
    print("Testing basic imports...")
    
    try:
        # Test individual module imports
        from src.runa.compiler.lexer import TokenType, Token
        print("✓ Lexer imports successful")
        
        from src.runa.compiler.parser import ASTNode, Program
        print("✓ Parser imports successful")
        
        from src.runa.compiler.semantic_analyzer import SemanticAnalyzer
        print("✓ Semantic analyzer imports successful")
        
        from src.runa.compiler.bytecode_generator import BytecodeGenerator
        print("✓ Bytecode generator imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_lexer_basic():
    """Test basic lexer functionality."""
    print("\nTesting basic lexer...")
    
    try:
        from src.runa.compiler.lexer import RunaLexer
        
        source = "Let x be 42"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        print(f"✓ Lexer: Generated {len(tokens)} tokens")
        return True
    except Exception as e:
        print(f"✗ Lexer failed: {e}")
        return False

def test_parser_basic():
    """Test basic parser functionality."""
    print("\nTesting basic parser...")
    
    try:
        from src.runa.compiler.lexer import RunaLexer
        from src.runa.compiler.parser import RunaParser
        
        source = "Let x be 42"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        parser = RunaParser(tokens)
        ast = parser.parse()
        
        print(f"✓ Parser: Generated AST with {len(ast.statements)} statements")
        return True
    except Exception as e:
        print(f"✗ Parser failed: {e}")
        return False

def main():
    """Run minimal tests."""
    print("Runa Compiler Minimal Test Suite")
    print("=" * 40)
    
    tests = [
        test_basic_import,
        test_lexer_basic,
        test_parser_basic,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 