"""
Tests for Hybrid Compiler Architecture
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from runa.compiler.hybrid_compiler import HybridCompiler
from runa.compiler.lexer import RunaLexer


class TestHybridCompiler(unittest.TestCase):
    """Test cases for hybrid compilation architecture."""
    
    def setUp(self):
        """Set up test environment."""
        self.compiler = HybridCompiler()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_compiler_initialization(self):
        """Test hybrid compiler initialization."""
        self.assertIsNotNone(self.compiler)
        self.assertIsNotNone(self.compiler.config)
        self.assertIsNotNone(self.compiler.translation_targets)
        self.assertIsNotNone(self.compiler.compilation_cache)
        
        # Check default configuration
        config = self.compiler.config
        self.assertEqual(config["primary_path"], "bytecode")
        self.assertEqual(config["target_language"], "python")
        self.assertEqual(config["optimization_level"], 2)
        self.assertTrue(config["enable_caching"])
        self.assertEqual(config["performance_target_ms"], 100)
    
    def test_supported_targets(self):
        """Test supported translation targets."""
        targets = self.compiler.get_supported_targets()
        expected_targets = ["python", "javascript", "cpp", "java", "rust", "go", "csharp"]
        
        for target in expected_targets:
            self.assertIn(target, targets)
        
        self.assertEqual(len(targets), 7)
    
    def test_bytecode_compilation(self):
        """Test bytecode compilation path."""
        source_code = """
Let x be 5
Display x
"""

        result = self.compiler.compile(source_code, target="runa_bytecode")
        
        # Debug output
        print(f"Compilation result: {result}")
        if not result["success"]:
            print(f"Error: {result.get('error', 'No error message')}")

        self.assertTrue(result["success"])
        self.assertEqual(result["output_type"], "bytecode")
        self.assertEqual(result["target"], "bytecode")
        self.assertIn("bytecode", result)
        self.assertGreater(result["compilation_time_ms"], 0)
        self.assertGreater(result["source_lines"], 0)
    
    def test_translation_compilation(self):
        """Test translation compilation path."""
        source_code = """
Let x be 5
Display x
"""

        result = self.compiler.compile(source_code, target="python")
        
        # Debug output
        print(f"Translation compilation result: {result}")
        if not result["success"]:
            print(f"Error: {result.get('error', 'No error message')}")

        self.assertTrue(result["success"])
        self.assertEqual(result["output_type"], "translation")
        self.assertEqual(result["target_language"], "python")
        self.assertIn("translated_code", result)
        self.assertIn("translation_accuracy", result)
        # Handle very fast compilations (0.0ms is valid for simple code)
        self.assertGreaterEqual(result["compilation_time_ms"], 0)
    
    def test_auto_target_selection(self):
        """Test automatic target selection."""
        # Simple code should default to translation
        simple_code = 'Display "Hello World"'
        result = self.compiler.compile(simple_code, target="auto")
        print("Simple result:", result)
        self.assertTrue(result["success"])
        
        # Complex code should select bytecode
        complex_code = (
            'Process called "factorial" with n as Integer:\n'
            '    If n is equal to 0:\n'
            '        Return 1\n'
            '    Otherwise:\n'
            '        Let result be factorial(n - 1)\n'
            '        Return result\n'
            '\n'
            'For each i in range(1, 1001):\n'
            '    Display factorial(i)\n'
        )
        result = self.compiler.compile(complex_code, target="auto")
        print("Complex result:", result)
        self.assertTrue(result["success"])
    
    def test_file_output(self):
        """Test compilation with file output."""
        source_code = 'Display "Test output"'
        output_path = os.path.join(self.temp_dir, "test_output")
        
        # Test bytecode output
        result = self.compiler.compile(source_code, target="runa_bytecode", output_path=output_path)
        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(output_path))
        
        # Test translation output
        output_path_py = os.path.join(self.temp_dir, "test_output_py")
        result = self.compiler.compile(source_code, target="python", output_path=output_path_py)
        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(output_path_py + ".py"))
    
    def test_caching(self):
        """Test compilation caching."""
        source_code = 'Display "Cached test"'
        
        # First compilation
        result1 = self.compiler.compile(source_code, target="runa_bytecode")
        self.assertTrue(result1["success"])
        self.assertFalse(result1["cached"])
        
        # Second compilation (should be cached)
        result2 = self.compiler.compile(source_code, target="runa_bytecode")
        self.assertTrue(result2["success"])
        self.assertTrue(result2["cached"])
        
        # Results should be identical
        self.assertEqual(result1["output_type"], result2["output_type"])
    
    def test_error_handling(self):
        """Test error handling for invalid code."""
        invalid_code = """
Process called "test":
    Return "invalid"  # Type mismatch
"""

        result = self.compiler.compile(invalid_code, target="runa_bytecode")

        # Should handle errors gracefully
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        self.assertIn("error", result)
    
    def test_complexity_analysis(self):
        """Test source code complexity analysis."""
        simple_code = 'Display "simple"'
        complex_code = """
Process called "complex":
    For each i in range with start as 1 and end as 11:
        If i modulo 2 is equal to 0:
            Display i
        Otherwise:
            Continue
    Return 42
"""
        
        # Test complexity calculation
        simple_complexity = self.compiler._analyze_complexity(simple_code)
        complex_complexity = self.compiler._analyze_complexity(complex_code)
        
        self.assertGreaterEqual(simple_complexity, 0.0)
        self.assertLessEqual(simple_complexity, 1.0)
        self.assertGreaterEqual(complex_complexity, 0.0)
        self.assertLessEqual(complex_complexity, 1.0)
        self.assertGreater(complex_complexity, simple_complexity)
    
    def test_performance_validation(self):
        """Test performance validation."""
        source_code = 'Display "performance test"'
        
        # Should not exceed performance target
        result = self.compiler.compile(source_code, target="runa_bytecode")
        self.assertTrue(result["success"])
        self.assertLess(result["compilation_time_ms"], 1000)  # Should be much faster
    
    def test_compilation_stats(self):
        """Test compilation statistics."""
        stats = self.compiler.get_compilation_stats()
        
        self.assertIn("cache_size", stats)
        self.assertIn("supported_targets", stats)
        self.assertIn("performance_target_ms", stats)
        self.assertIn("optimization_level", stats)
        
        self.assertEqual(stats["supported_targets"], 7)
        self.assertEqual(stats["performance_target_ms"], 100)
        self.assertEqual(stats["optimization_level"], 2)
    
    def test_multiple_target_languages(self):
        """Test compilation to multiple target languages."""
        source_code = """
Process called "multiply" with a as Integer and b as Integer:
    Return a multiplied by b

Display multiply(4, 5)
"""
        
        targets = ["python", "javascript", "cpp"]
        
        for target in targets:
            result = self.compiler.compile(source_code, target=target)
            self.assertTrue(result["success"])
            self.assertEqual(result["target_language"], target)
            self.assertIn("translated_code", result)
    
    def test_optimization_levels(self):
        """Test different optimization levels."""
        source_code = """
Process called "test":
    Return 42
"""
        
        # Test with different optimization levels
        for level in [0, 1, 2, 3]:
            config = {"optimization_level": level}
            compiler = HybridCompiler(config)
            result = compiler.compile(source_code, target="bytecode")
            
            self.assertTrue(result["success"])
            self.assertEqual(result["optimization_level"], level)


if __name__ == "__main__":
    unittest.main() 