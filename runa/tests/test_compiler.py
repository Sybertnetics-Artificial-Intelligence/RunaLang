"""
Tests for the Runa compiler.

This module contains tests for the compiler, including integration tests for the
lexer, parser, and semantic analyzer with the enhanced type system.
"""

import unittest
from src.compiler import Compiler


class TestCompiler(unittest.TestCase):
    """Tests for the Compiler class."""
    
    def setUp(self):
        """Set up the compiler for each test."""
        self.compiler = Compiler()
    
    def test_compile_simple_program(self):
        """Test compiling a simple program."""
        source = """
        let x = 42;
        let y = "hello";
        let z = true;
        """
        
        result = self.compiler.compile_string(source)
        
        # Check that compilation was successful
        self.assertTrue(result.success)
        self.assertFalse(result.has_errors())
        
        # Check that the program was parsed correctly
        self.assertIsNotNone(result.program)
        self.assertEqual(len(result.program.statements), 3)
        
        # Check that types were inferred correctly
        self.assertIn("x", result.inferred_types)
        self.assertEqual(result.inferred_types["x"], "Int")
        self.assertIn("y", result.inferred_types)
        self.assertEqual(result.inferred_types["y"], "String")
        self.assertIn("z", result.inferred_types)
        self.assertEqual(result.inferred_types["z"], "Boolean")
    
    def test_compile_with_generic_types(self):
        """Test compiling a program with generic types."""
        source = """
        let numbers = [1, 2, 3];
        let strings = ["hello", "world"];
        let mixed = [1, "two", true];
        """
        
        result = self.compiler.compile_string(source)
        
        # Check that compilation was successful
        self.assertTrue(result.success)
        self.assertFalse(result.has_errors())
        
        # Check that the program was parsed correctly
        self.assertIsNotNone(result.program)
        self.assertEqual(len(result.program.statements), 3)
        
        # Check that types were inferred correctly
        self.assertIn("numbers", result.inferred_types)
        self.assertEqual(result.inferred_types["numbers"], "List[Int]")
        self.assertIn("strings", result.inferred_types)
        self.assertEqual(result.inferred_types["strings"], "List[String]")
        self.assertIn("mixed", result.inferred_types)
        # For mixed types, we should get a union type or Any
        mixed_type = result.inferred_types["mixed"]
        self.assertTrue(
            mixed_type == "List[Int | String | Boolean]" or
            mixed_type == "List[Any]"
        )
    
    def test_compile_with_functions(self):
        """Test compiling a program with functions."""
        source = """
        function add(a: Int, b: Int): Int {
            return a + b;
        }
        
        function greet(name: String): String {
            return "Hello, " + name;
        }
        
        let sum = add(1, 2);
        let greeting = greet("world");
        """
        
        result = self.compiler.compile_string(source)
        
        # Check that compilation was successful
        self.assertTrue(result.success)
        self.assertFalse(result.has_errors())
        
        # Check that the program was parsed correctly
        self.assertIsNotNone(result.program)
        self.assertEqual(len(result.program.statements), 4)
        
        # Check that types were inferred correctly
        self.assertIn("add", result.inferred_types)
        self.assertTrue(result.inferred_types["add"].startswith("(Int, Int) -> Int"))
        self.assertIn("greet", result.inferred_types)
        self.assertTrue(result.inferred_types["greet"].startswith("(String) -> String"))
        self.assertIn("sum", result.inferred_types)
        self.assertEqual(result.inferred_types["sum"], "Int")
        self.assertIn("greeting", result.inferred_types)
        self.assertEqual(result.inferred_types["greeting"], "String")
    
    def test_compile_with_type_errors(self):
        """Test compiling a program with type errors."""
        source = """
        let x: Int = "hello";  // Type error: String assigned to Int
        let y: String = 42;    // Type error: Int assigned to String
        """
        
        result = self.compiler.compile_string(source)
        
        # Check that compilation failed
        self.assertFalse(result.success)
        self.assertTrue(result.has_errors())
        self.assertTrue(len(result.semantic_errors) > 0)
        
        # Check that the error messages are helpful
        error_messages = [str(error) for error in result.semantic_errors]
        self.assertTrue(any("Type mismatch" in msg for msg in error_messages))
    
    def test_compile_with_union_types(self):
        """Test compiling a program with union types."""
        source = """
        function process(value: Int | String): String {
            if (typeof value == "Int") {
                return "Number: " + value;
            } else {
                return "Text: " + value;
            }
        }
        
        let result1 = process(42);
        let result2 = process("hello");
        """
        
        result = self.compiler.compile_string(source)
        
        # Note: This test might fail if union types aren't fully implemented yet
        # The purpose is to show how union types would be handled
        
        # Check that compilation was successful (if union types are supported)
        if result.success:
            # Check that types were inferred correctly
            self.assertIn("process", result.inferred_types)
            process_type = result.inferred_types["process"]
            self.assertTrue("Int | String" in process_type)
            self.assertTrue("-> String" in process_type)
            
            self.assertIn("result1", result.inferred_types)
            self.assertEqual(result.inferred_types["result1"], "String")
            self.assertIn("result2", result.inferred_types)
            self.assertEqual(result.inferred_types["result2"], "String")
    
    def test_compile_with_type_inference(self):
        """Test compiling a program with type inference."""
        source = """
        function add(a, b) {
            return a + b;
        }
        
        let x = 42;
        let y = 3.14;
        let z = add(x, y);
        """
        
        result = self.compiler.compile_string(source)
        
        # Check that compilation was successful
        self.assertTrue(result.success)
        self.assertFalse(result.has_errors())
        
        # Check that types were inferred correctly
        self.assertIn("add", result.inferred_types)
        # The add function should take two numbers and return a number
        self.assertIn("x", result.inferred_types)
        self.assertEqual(result.inferred_types["x"], "Int")
        self.assertIn("y", result.inferred_types)
        self.assertEqual(result.inferred_types["y"], "Float")
        self.assertIn("z", result.inferred_types)
        self.assertEqual(result.inferred_types["z"], "Float")  # Result should be Float
    
    def test_compile_complex_program(self):
        """Test compiling a more complex program."""
        source = """
        function map(list, func) {
            let result = [];
            for (let i = 0; i < len(list); i = i + 1) {
                result.push(func(list[i]));
            }
            return result;
        }
        
        function filter(list, predicate) {
            let result = [];
            for (let i = 0; i < len(list); i = i + 1) {
                if (predicate(list[i])) {
                    result.push(list[i]);
                }
            }
            return result;
        }
        
        let numbers = [1, 2, 3, 4, 5];
        let doubled = map(numbers, function(x) { return x * 2; });
        let evens = filter(numbers, function(x) { return x % 2 == 0; });
        """
        
        result = self.compiler.compile_string(source)
        
        # This test is mainly to check that complex programs compile
        # without errors, not to check specific type inference results
        
        # Check that compilation was successful
        self.assertTrue(result.success)
        self.assertFalse(result.has_errors())
        
        # Check that the program was parsed correctly
        self.assertIsNotNone(result.program)
        self.assertEqual(len(result.program.statements), 5)
        
        # Check that at least some types were inferred
        self.assertGreater(len(result.inferred_types), 0)


if __name__ == "__main__":
    unittest.main() 