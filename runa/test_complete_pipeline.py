#!/usr/bin/env python3
"""
Complete Runa compiler pipeline test.

Tests the entire compilation and execution pipeline with various Runa programs.
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from runa.compiler import Compiler
from runa.runtime import get_runtime, reset_runtime
# NOTE: The VM is now implemented in Runa (vm.runa), not Python.
# This test must be ported to use the Runa toolchain for VM execution.
# import from runa.vm is no longer valid.
# from runa.vm import get_vm, reset_vm  # <-- REMOVE or port to Runa


def test_basic_compilation():
    """Test basic compilation and execution."""
    print("Testing basic compilation...")
    
    runa_code = """
Let message be "Hello, Runa World!"
Display message
Let x be 42
Let y be 8
Let result be x plus y
Display "Result:" with message result
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Basic compilation successful.")
        print(f"Output: {runtime.get_output()}")
        return True
    
    except Exception as e:
        print(f"Basic compilation failed: {e}")
        return False


def test_arithmetic_operations():
    """Test all arithmetic operations with Runa operators."""
    print("Testing arithmetic operations...")
    
    runa_code = """
Let a be 20
Let b be 4

Let sum be a plus b
Let difference be a minus b
Let product be a multiplied by b
Let quotient be a divided by b
Let remainder be a modulo b
Let power be a power of b

Display "Sum:" with message sum
Display "Difference:" with message difference
Display "Product:" with message product
Display "Quotient:" with message quotient
Display "Remainder:" with message remainder
Display "Power:" with message power
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
        print(f"Arithmetic operations failed: {e}")
        return False


def test_comparison_operations():
    """Test comparison operations with Runa operators."""
    print("Testing comparison operations...")
    
    runa_code = """
Let x be 15
Let y be 10

Let is_greater be x is greater than y
Let is_less be x is less than y
Let is_equal be x is equal to y
Let is_not_equal be x is not equal to y
Let is_greater_equal be x is greater than or equal to y
Let is_less_equal be x is less than or equal to y

Display "x is greater than y:" with message is_greater
Display "x is less than y:" with message is_less
Display "x is equal to y:" with message is_equal
Display "x is not equal to y:" with message is_not_equal
Display "x is greater than or equal to y:" with message is_greater_equal
Display "x is less than or equal to y:" with message is_less_equal
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
        print(f"Comparison operations failed: {e}")
        return False


def test_logical_operations():
    """Test logical operations with Runa operators."""
    print("Testing logical operations...")
    
    runa_code = """
Let a be true
Let b be false

Let and_result be a and b
Let or_result be a or b
Let not_a be not a
Let not_b be not b

Display "a and b:" with message and_result
Display "a or b:" with message or_result
Display "not a:" with message not_a
Display "not b:" with message not_b
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Logical operations successful.")
        print(f"Output: {runtime.get_output()}")
        return True
    
    except Exception as e:
        print(f"Logical operations failed: {e}")
        return False


def test_string_operations():
    """Test string operations with Runa operators."""
    print("Testing string operations...")
    
    runa_code = """
Let first be "Hello"
Let second be "World"
Let combined be first followed by " " followed by second

Display combined
Display "Length of combined:" with message length of combined

Let contains_hello be combined contains "Hello"
Display "Contains 'Hello':" with message contains_hello
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("String operations successful.")
        print(f"Output: {runtime.get_output()}")
        return True
    
    except Exception as e:
        print(f"String operations failed: {e}")
        return False


def test_list_operations():
    """Test list operations with Runa syntax."""
    print("Testing list operations...")
    
    runa_code = """
Let numbers be list containing 1, 2, 3, 4, 5
Let count be length of numbers

Display "List:" with message numbers
Display "Count:" with message count

Let first_number be numbers at index 0
Display "First number:" with message first_number

Let sum be sum of all numbers in numbers
Display "Sum of all numbers:" with message sum
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("List operations successful.")
        print(f"Output: {runtime.get_output()}")
        return True
    
    except Exception as e:
        print(f"List operations failed: {e}")
        return False


def test_builtin_functions():
    """Test built-in functions with Runa syntax."""
    print("Testing built-in functions...")
    
    runa_code = """
Let numbers be list containing 5, 2, 8, 1, 9, 3

Let min_val be minimum value of 5, 2, 8, 1, 9, 3
Let max_val be maximum value of 5, 2, 8, 1, 9, 3
Let abs_val be absolute value of -42
Let rounded be round number 3.14159 with 2

Display "Minimum:" with message min_val
Display "Maximum:" with message max_val
Display "Absolute value of -42:" with message abs_val
Display "Rounded 3.14159 to 2 places:" with message rounded
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("Built-in functions successful.")
        print(f"Output: {runtime.get_output()}")
        return True
    
    except Exception as e:
        print(f"Built-in functions failed: {e}")
        return False


def test_ai_functions():
    """Test AI-specific functions with Runa syntax."""
    print("Testing AI functions...")
    
    runa_code = """
Let thought be ai think with "What is the meaning of life?"
Display "AI thought:" with message thought

Let translation be ai translate with "Hello world" from "English" to "Spanish"
Display "Translation:" with message translation

Let analysis be ai analyze with "Sample data" as "sentiment"
Display "Analysis:" with message analysis
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        runtime = get_runtime()
        result = runtime.execute_bytecode(bytecode)
        
        print("AI functions successful.")
        print(f"Output: {runtime.get_output()}")
        return True
    
    except Exception as e:
        print(f"AI functions failed: {e}")
        return False


def test_performance_targets():
    """Test that compilation meets performance targets."""
    print("Testing performance targets...")
    
    runa_code = """
Let x be 1
Let y be 2
Let z be x plus y
Display z
"""
    
    try:
        start_time = time.time()
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        compilation_time = (time.time() - start_time) * 1000
        
        print(f"Compilation time: {compilation_time:.2f}ms")
        
        if compilation_time < 100:
            print("Performance target met (<100ms)")
            return True
        else:
            print(f"Performance target missed: {compilation_time:.2f}ms >= 100ms")
            return False
    
    except Exception as e:
        print(f"Performance test failed: {e}")
        return False


def test_memory_management():
    """Test memory management and garbage collection."""
    print("Testing memory management...")
    
    try:
        runtime = get_runtime()
        initial_stats = runtime.get_memory_stats()
        
        runa_code = """
Let large_list be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Display "Created large list"
"""
        
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        runtime.execute_bytecode(bytecode)
        
        final_stats = runtime.get_memory_stats()
        
        print(f"Initial memory usage: {initial_stats['used_memory']} bytes")
        print(f"Final memory usage: {final_stats['used_memory']} bytes")
        
        return True
    
    except Exception as e:
        print(f"Memory management test failed: {e}")
        return False


def test_vm_execution():
    """Test VM execution with JIT compilation."""
    print("Testing VM execution...")
    
    runa_code = """
Let counter be 0
Let limit be 1000

While counter is less than limit:
    Let counter be counter plus 1

Display "Counter reached:" with message counter
"""
    
    try:
        vm = get_vm()
        compiler = Compiler()
        bytecode = compiler.compile(runa_code)
        
        result = vm.execute(bytecode, "vm_test")
        
        stats = vm.get_stats()
        print(f"VM execution successful.")
        print(f"Instructions executed: {stats['total_instructions_executed']}")
        print(f"Execution time: {stats['total_execution_time']:.4f}s")
        
        return True
    
    except Exception as e:
        print(f"VM execution failed: {e}")
        return False


def test_error_handling():
    """Test error handling and recovery."""
    print("Testing error handling...")
    
    invalid_code = """
Let x be 10
Let y be 0
Let result be x divided by y
Display result
"""
    
    try:
        compiler = Compiler()
        bytecode = compiler.compile(invalid_code)
        
        runtime = get_runtime()
        runtime.execute_bytecode(bytecode)
        
        print("Error handling failed - should have caught division by zero")
        return False
    
    except Exception as e:
        if "Division by zero" in str(e):
            print("Error handling successful - caught division by zero")
            return True
        else:
            print(f"Unexpected error: {e}")
            return False


def main():
    """Run all complete pipeline tests."""
    print("Running complete Runa pipeline tests...")
    print("=" * 60)
    
    tests = [
        test_basic_compilation,
        test_arithmetic_operations,
        test_comparison_operations,
        test_logical_operations,
        test_string_operations,
        test_list_operations,
        test_builtin_functions,
        test_ai_functions,
        test_performance_targets,
        test_memory_management,
        test_vm_execution,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
        
        reset_runtime()
        reset_vm()
    
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All complete pipeline tests passed!")
        return 0
    else:
        print("Some tests failed.")
        return 1


if __name__ == "__main__":
    exit(main()) 