"""
Test Suite for Complete Runa Compilation Pipeline

This module tests the end-to-end compilation from Runa source code
to executable Python code. It demonstrates the TDD approach for
Phase 1.4 implementation.
"""

import unittest
import tempfile
import subprocess
import sys
from textwrap import dedent

from runa.compiler import compile_runa_to_python, compile_runa_to_ir, parse_runa_source

# Test helper functions that can be injected or assumed to exist for tests
def get_test_helpers() -> str:
    return dedent('''
        def calculate_interest(principal, rate, years=1):
            return principal * rate * years

        def calculate_total(*args, **kwargs):
            total = sum(v for v in args if isinstance(v, (int, float))) + \
                    sum(v for v in kwargs.values() if isinstance(v, (int, float)))
            return total

        def calculate_discount_amount(original_price, discount_rate):
            return original_price * discount_rate

        def format_currency(amount, symbol="$"):
            return f"{symbol}{amount:.2f}"
    ''')

class TestCompilationPipeline(unittest.TestCase):
    """Test the complete Runa→IR→Python compilation pipeline."""
    
    def test_simple_variable_assignment(self):
        """Test compilation of basic variable assignment."""
        runa_source = dedent('''
            Let user name be "Alice"
            Let user age be 25
            Display user name
            Display user age
        ''').strip()
        
        # Compile to Python
        python_code = compile_runa_to_python(runa_source)
        
        # Verify Python code was generated
        self.assertIn("user_name", python_code)
        self.assertIn("user_age", python_code)
        self.assertIn('= "Alice"', python_code)
        self.assertIn("= 25", python_code)
        self.assertIn("print(", python_code)
        
        # Test that generated Python code is executable
        self._test_python_execution(python_code, expected_output=["Alice", "25"])
    
    def test_arithmetic_operations(self):
        """Test compilation of arithmetic expressions."""
        runa_source = dedent('''
            Let price be 100
            Let tax rate be 0.08
            Let tax amount be price multiplied by tax rate
            Let total be price plus tax amount
            Display total
        ''').strip()
        
        python_code = compile_runa_to_python(runa_source)
        
        # Verify arithmetic operations are calculated correctly by execution.
        # Removed brittle assertIn checks.
        
        # Test execution - should print 108.0
        self._test_python_execution(python_code, expected_output=["108.0"])
    
    def test_conditional_logic(self):
        """Test compilation of if-else statements."""
        runa_source = dedent('''
            Let age be 25
            If age is greater than 18:
                Display "Adult"
            Otherwise:
                Display "Minor"
        ''').strip()
        
        python_code = compile_runa_to_python(runa_source)
        
        # Verify conditional structure by execution, not by exact string match.
        # Removed brittle assertIn checks.
        
        # Test execution
        self._test_python_execution(python_code, expected_output=["Adult"])
    
    def test_list_operations(self):
        """Test compilation of list creation and operations."""
        runa_source = dedent('''
            Let numbers be list containing 1, 2, 3, 4, 5
            Display numbers
        ''').strip()
        
        python_code = compile_runa_to_python(runa_source)
        
        # Verify list creation by execution.
        # Removed brittle assertIn check.
        
        # Test execution
        self._test_python_execution(python_code, expected_output=["[1, 2, 3, 4, 5]"])
    
    def test_function_calls(self):
        """Test compilation of function calls with named parameters."""
        runa_source = dedent('''
            Let result be Calculate Interest with principal as 1000 and rate as 0.05
            Display result
        ''').strip()
        
        python_code = compile_runa_to_python(runa_source)
        
        # Verify function call generation by execution.
        # Removed brittle assertIn check.
        
        # Test execution - should print 50.0 (1000 * 0.05 * 1)
        self._test_python_execution(python_code, expected_output=["50.0"])
    
    def test_complex_program(self):
        """Test compilation of a more complex Runa program."""
        runa_source = dedent('''
            Let customer name be "Bob Smith"
            Let order total be 150.00
            Let discount rate be 0.10
            
            Let discount amount be Calculate Discount Amount with:
                original price as order total
                discount rate as discount rate
            
            Let final price be order total minus discount amount
            
            Display customer name with message "Customer:"
            Display final price with message "Final price:"
            
            If final price is greater than 100:
                Display "Eligible for free shipping"
        ''').strip()
        
        python_code = compile_runa_to_python(runa_source)
        
        # Verify complex operations via execution.
        # The output check is a more robust test than string-matching the generated code.
        
        # Test execution
        expected_output = [
            "Customer: Bob Smith",
            "Final price: 135.0",  # 150 - (150 * 0.10)
            "Eligible for free shipping"
        ]
        self._test_python_execution(python_code, expected_output)
    
    def test_ir_generation(self):
        """Test intermediate representation generation."""
        runa_source = dedent('''
            Let x be 42
            Let y be x plus 8
            Display y
        ''').strip()
        
        ir_module = compile_runa_to_ir(runa_source)
        
        # Verify IR structure
        self.assertIsNotNone(ir_module)
        self.assertEqual(ir_module.name, "main")
        self.assertTrue(any(f.name == "main" for f in ir_module.functions), "Main function not found in IR")
        
        main_func = next((f for f in ir_module.functions if f.name == "main"), None)
        self.assertIsNotNone(main_func)
        self.assertEqual(main_func.name, "main")
        self.assertGreater(len(main_func.basic_blocks), 0)
        
        # Verify IR contains expected operations
        ir_str = str(ir_module)
        self.assertIn("assign", ir_str.lower())
        self.assertIn("add", ir_str.lower())
        self.assertIn("display", ir_str.lower())
    
    def test_compilation_error_handling(self):
        """Test that compilation errors are properly handled."""
        # Test with invalid syntax
        invalid_source = "Let x be"  # Incomplete statement
        
        with self.assertRaises(Exception):  # Should raise some parsing error
            compile_runa_to_python(invalid_source)
    
    def _test_python_execution(self, python_code: str, expected_output: list):
        """Helper method to test that generated Python code executes correctly."""
        # Create temporary file with generated Python code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, newline='') as f:
            # Inject helper functions into the test code
            helpers = get_test_helpers()
            
            # The generated code from compile_runa_to_python includes the header and main block.
            # We need to inject our Python test helpers before the generated code.
            # A simple concatenation is sufficient if compile_runa_to_python provides the full script.
            
            # Let's rebuild the python code structure to ensure correctness.
            # The generator already creates the full structure, so we just prepend helpers.
            
            final_code = f"{helpers}\n\n{python_code}"
            f.write(final_code)
            
            temp_file = f.name
        
        try:
            # Execute the generated Python code
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Check execution was successful
            self.assertEqual(result.returncode, 0, 
                           f"Generated Python code failed to execute: {result.stderr}")
            
            # Check output matches expected
            actual_lines = result.stdout.strip().split('\n')
            actual_lines = [line.strip() for line in actual_lines if line.strip()]
            
            self.assertEqual(len(actual_lines), len(expected_output),
                           f"Expected {len(expected_output)} lines, got {len(actual_lines)}: {actual_lines}")
            
            for expected, actual in zip(expected_output, actual_lines):
                self.assertEqual(actual, expected,
                               f"Expected '{expected}', got '{actual}'")
                
        finally:
            # Clean up temporary file
            import os
            try:
                os.unlink(temp_file)
            except FileNotFoundError:
                pass

class TestIRStructure(unittest.TestCase):
    """Test the structure and correctness of generated IR."""
    
    def test_ir_basic_structure(self):
        """Test that IR has correct basic structure."""
        runa_source = "Let x be 5"
        ir_module = compile_runa_to_ir(runa_source)
        
        # Check module structure
        self.assertEqual(ir_module.name, "main")
        self.assertTrue(any(f.name == "main" for f in ir_module.functions), "Main function not found in IR")
        
        # Check function structure
        main_func = next((f for f in ir_module.functions if f.name == "main"), None)
        self.assertIsNotNone(main_func)
        self.assertEqual(main_func.name, "main")
        self.assertEqual(len(main_func.parameters), 0)
        self.assertIn("entry", main_func.blocks)
        
        # Check basic block structure
        entry_block = main_func.blocks["entry"]
        self.assertGreater(len(entry_block.instructions), 0)
    
    def test_ir_variable_handling(self):
        """Test that IR correctly handles variable assignments."""
        runa_source = dedent('''
            Let username be "Alice"
            Set username to "Bob"
        ''').strip()
        
        ir_module = compile_runa_to_ir(runa_source)
        main_func = next((f for f in ir_module.functions if f.name == "main"), None)
        self.assertIsNotNone(main_func)
        
        # Verify that the IR contains assign instructions for the variable
        assign_count = 0
        for block in main_func.basic_blocks:
            for instr in block.instructions:
                if hasattr(instr, 'instruction_type') and instr.instruction_type.name == 'ASSIGN':
                    assign_count += 1
        self.assertGreaterEqual(assign_count, 1, "Expected at least one assignment instruction")

if __name__ == '__main__':
    unittest.main() 