#!/usr/bin/env python3
"""
Simple test for Runa compiler pipeline.

Tests basic compilation and execution of simple Runa programs.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from runa.compiler import Compiler
from runa.runtime import get_runtime
from runa.vm import get_vm


def test_simple_compilation():
    """Test simple Runa program compilation."""
    print("Testing simple Runa compilation...")
    
    runa_code = """
Let greeting be "Hello, Runa!"
Display greeting
Let x be 10
Let y be 5
Let sum be x plus y
Display "Sum is" with message sum
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        print(f"Compilation successful. Generated {len(bytecode)} instructions.")
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Execution successful.")
        print(f"Output: {runtime.get_output()}")
        
        return True
    
    except Exception as e:
        print(f"Test failed: {e}")
        return False


def test_arithmetic_operations():
    """Test arithmetic operations with Runa operators."""
    print("Testing arithmetic operations...")
    
    runa_code = """
Let a be 15
Let b be 3
Let sum be a plus b
Let difference be a minus b
Let product be a multiplied by b
Let quotient be a divided by b
Let remainder be a modulo b

Display "Sum:" with message sum
Display "Difference:" with message difference
Display "Product:" with message product
Display "Quotient:" with message quotient
Display "Remainder:" with message remainder
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Arithmetic operations successful.")
        print(f"Output: {runtime.get_output()}")
        
        return True
    
    except Exception as e:
        print(f"Arithmetic test failed: {e}")
        return False


def test_comparison_operations():
    """Test comparison operations with Runa operators."""
    print("Testing comparison operations...")
    
    runa_code = """
Let x be 10
Let y be 5

Let is_greater be x is greater than y
Let is_less be x is less than y
Let is_equal be x is equal to y
Let is_not_equal be x is not equal to y

Display "x is greater than y:" with message is_greater
Display "x is less than y:" with message is_less
Display "x is equal to y:" with message is_equal
Display "x is not equal to y:" with message is_not_equal
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Comparison operations successful.")
        print(f"Output: {runtime.get_output()}")
        
        return True
    
    except Exception as e:
        print(f"Comparison test failed: {e}")
        return False


def test_function_calls():
    """Test function calls with Runa syntax."""
    print("Testing function calls...")
    
    runa_code = """
Let message be "Hello from Runa!"
Display message

Let numbers be list containing 1, 2, 3, 4, 5
Let count be length of numbers
Display "List has" with message count followed by "elements"
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Function calls successful.")
        print(f"Output: {runtime.get_output()}")
        
        return True
    
    except Exception as e:
        print(f"Function call test failed: {e}")
        return False


def main():
    """Run all simple tests."""
    print("Running simple Runa tests...")
    print("=" * 50)
    
    tests = [
        test_simple_compilation,
        test_arithmetic_operations,
        test_comparison_operations,
        test_function_calls
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All simple tests passed!")
        return 0
    else:
        print("Some tests failed.")
        return 1


if __name__ == "__main__":
    exit(main()) 