#!/usr/bin/env python3
"""
Test script to verify Runa toolchain integration with the hub-and-spoke system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_runa_toolchain_registration():
    """Test that the Runa toolchain can be registered and used."""
    print("Testing Runa toolchain registration...")
    
    try:
        # Import should trigger auto-registration
        from runa.languages.runa import runa_parser, runa_generator, RUNA_LANGUAGE_INFO
        from runa.core.pipeline import get_pipeline
        
        print(f"✓ Imported Runa toolchain components")
        print(f"  Language: {RUNA_LANGUAGE_INFO.name}")
        print(f"  Parser: {type(runa_parser).__name__}")
        print(f"  Generator: {type(runa_generator).__name__}")
        
        # Check pipeline registration
        pipeline = get_pipeline()
        print(f"✓ Pipeline retrieved: {type(pipeline).__name__}")
        
        # Verify Runa toolchain is registered
        if pipeline.runa_parser and pipeline.runa_generator:
            print("✓ Runa toolchain registered with pipeline")
        else:
            print("✗ Runa toolchain not properly registered")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Registration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_runa_parser():
    """Test basic Runa parser functionality."""
    print("\nTesting Runa parser...")
    
    try:
        from runa.languages.runa import runa_parser
        
        # Simple test code
        test_code = '''Let message be "Hello, World!"
Display message'''
        
        # Parse the code
        ast = runa_parser.parse(test_code, "test.runa")
        print(f"✓ Parsed test code successfully")
        print(f"  AST type: {type(ast).__name__}")
        print(f"  AST has {len(ast.statements)} statements")
        
        return True
        
    except Exception as e:
        print(f"✗ Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_runa_generator():
    """Test basic Runa generator functionality."""
    print("\nTesting Runa generator...")
    
    try:
        from runa.languages.runa import runa_parser, runa_generator
        
        # Simple test code
        test_code = '''Let x be 42
Display x'''
        
        # Parse then generate
        ast = runa_parser.parse(test_code, "test.runa")
        generated_code = runa_generator.generate(ast)
        
        print(f"✓ Generated code successfully")
        print(f"  Generated code length: {len(generated_code)} characters")
        print(f"  Generated code:\n{generated_code}")
        
        return True
        
    except Exception as e:
        print(f"✗ Generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_round_trip():
    """Test round-trip: parse -> generate -> parse."""
    print("\nTesting round-trip translation...")
    
    try:
        from runa.languages.runa import runa_parser, runa_generator
        from runa.core.verification import compare_asts
        
        # Test code
        original_code = '''Let greeting be "Hello, World!"
Let number be 42
Display greeting'''
        
        # Parse original
        ast1 = runa_parser.parse(original_code, "original.runa")
        
        # Generate code from AST
        generated_code = runa_generator.generate(ast1)
        
        # Parse generated code
        ast2 = runa_parser.parse(generated_code, "generated.runa")
        
        # Compare ASTs
        result = compare_asts(ast1, ast2)
        
        if result.is_identical:
            print("✓ Round-trip successful - ASTs are identical")
        else:
            print(f"⚠ Round-trip partial - {len(result.differences)} differences")
            for diff in result.differences[:3]:  # Show first 3 differences
                print(f"    {diff}")
        
        return True
        
    except Exception as e:
        print(f"✗ Round-trip test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=== Runa Toolchain Integration Test ===\n")
    
    tests = [
        test_runa_toolchain_registration,
        test_runa_parser,
        test_runa_generator,
        test_round_trip
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All tests passed! Runa toolchain is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())