#!/usr/bin/env python3
"""
Test imports for Runa compiler components.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test all imports step by step."""
    print("Testing Runa compiler imports...")
    
    try:
        # Test lexer
        print("1. Testing lexer import...")
        from runa.compiler.lexer import RunaLexer, Token, TokenType
        print("   ✓ Lexer import successful")
        
        # Test parser
        print("2. Testing parser import...")
        from runa.compiler.parser import RunaParser, ASTNode, Program, Statement, Expression
        print("   ✓ Parser import successful")
        
        # Test semantic analyzer
        print("3. Testing semantic analyzer import...")
        from runa.compiler.semantic_analyzer import SemanticAnalyzer
        print("   ✓ Semantic analyzer import successful")
        
        # Test bytecode generator
        print("4. Testing bytecode generator import...")
        from runa.compiler.bytecode_generator import BytecodeGenerator
        print("   ✓ Bytecode generator import successful")
        
        # Test runtime
        print("5. Testing runtime import...")
        from runa.runtime import RunaRuntime
        print("   ✓ Runtime import successful")
        
        # Test VM
        print("6. Testing VM import...")
        from runa.vm import RunaVM
        print("   ✓ VM import successful")
        
        # Test compiler package
        print("7. Testing compiler package import...")
        from runa.compiler import Compiler
        print("   ✓ Compiler package import successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"   ✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 