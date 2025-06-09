"""
Tests for control flow and pattern matching features.
"""

import unittest
from unittest.mock import patch
import io
import sys

from runa.src.lexer.lexer import Lexer
from runa.src.parser.parser import Parser
from runa.src.semantic.analyzer import SemanticAnalyzer
from runa.src.vm.bytecode import BytecodeGenerator
from runa.src.vm.vm import VirtualMachine


class TestControlFlow(unittest.TestCase):
    """Test cases for control flow constructs."""
    
    def setUp(self):
        """Set up the test environment."""
        self.vm = VirtualMachine()
    
    def _compile_and_run(self, source_code):
        """Compile and run the given source code."""
        # Parse the source code
        lexer = Lexer(source_code)
        parser = Parser(lexer)
        program = parser.parse()
        
        # Analyze the program
        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)
        
        # Generate bytecode
        generator = BytecodeGenerator("test_module")
        generator.generate(program)
        
        # Run the bytecode
        return self.vm.execute(generator.module)
    
    def test_if_statement(self):
        """Test if-otherwise statements."""
        source_code = """
        let x = 10
        let result = 0
        
        if x > 5:
            result = 1
        else if x > 0:
            result = 2
        else:
            result = 3
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, 1)
    
    def test_short_circuit_evaluation(self):
        """Test short-circuit evaluation of logical operators."""
        source_code = """
        let x = 10
        let y = 0
        
        # This should not cause a division by zero because of short-circuit
        let result = x < 5 && y > 0 && (x / y) > 2
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, False)
        
        source_code = """
        let x = 10
        let y = 0
        
        # This should not cause a division by zero because of short-circuit
        let result = x > 5 || y > 0 || (x / y) > 2
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, True)
    
    def test_pattern_matching_literal(self):
        """Test pattern matching with literals."""
        source_code = """
        let value = 42
        
        let result = match value:
            case 42:
                "The answer"
            case 7:
                "Lucky number"
            case _:
                "Something else"
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, "The answer")
    
    def test_pattern_matching_variable(self):
        """Test pattern matching with variable binding."""
        source_code = """
        let value = 42
        
        let result = match value:
            case x if x > 50:
                "Large number"
            case x if x > 0:
                "Positive number: " + x.to_string()
            case _:
                "Something else"
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, "Positive number: 42")
    
    def test_pattern_matching_list(self):
        """Test pattern matching with lists."""
        source_code = """
        let value = [1, 2, 3, 4, 5]
        
        let result = match value:
            case []:
                "Empty list"
            case [x]:
                "Single element: " + x.to_string()
            case [x, y]:
                "Two elements: " + x.to_string() + ", " + y.to_string()
            case [x, ...rest]:
                "First element: " + x.to_string() + ", rest: " + rest.to_string()
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, "First element: 1, rest: [2, 3, 4, 5]")
    
    def test_pattern_matching_dictionary(self):
        """Test pattern matching with dictionaries."""
        source_code = """
        let value = {
            "name": "Alice",
            "age": 30,
            "city": "Wonderland"
        }
        
        let result = match value:
            case {"name": "Bob"}:
                "It's Bob"
            case {"name": name, "age": age} if age > 20:
                "Adult: " + name
            case {"name": name}:
                "Person: " + name
            case _:
                "Unknown person"
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, "Adult: Alice")
    
    def test_pattern_matching_type(self):
        """Test pattern matching with types."""
        source_code = """
        let value = "Hello, world!"
        
        let result = match value:
            case x of Integer:
                "Integer: " + x.to_string()
            case x of String:
                "String with length: " + x.length().to_string()
            case x of List:
                "List with elements: " + x.length().to_string()
            case _:
                "Unknown type"
        
        return result
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, "String with length: 13")
    
    def test_closures(self):
        """Test closures with captured variables."""
        source_code = """
        let make_counter = (initial) => {
            let count = initial
            return (increment) => {
                count = count + increment
                return count
            }
        }
        
        let counter = make_counter(10)
        let result1 = counter(1)  # 11
        let result2 = counter(2)  # 13
        
        return result2
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, 13)
    
    def test_tail_call_optimization(self):
        """Test tail call optimization."""
        source_code = """
        let factorial = (n, acc) => {
            if n <= 1:
                return acc
            else:
                return factorial(n - 1, n * acc)  # Tail call
        }
        
        return factorial(5, 1)  # Should compute 5! = 120
        """
        
        result = self._compile_and_run(source_code)
        self.assertEqual(result.value, 120)


if __name__ == "__main__":
    unittest.main() 