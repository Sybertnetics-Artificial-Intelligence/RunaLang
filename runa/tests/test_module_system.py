"""
Tests for the Runa module system.

This module contains tests for the Runa module system, including imports,
exports, and namespaces.
"""

import os
import unittest
from pathlib import Path
import tempfile

from runa.src.compiler import Compiler
from runa.src.vm.vm import VirtualMachine, VMValueType


class TestModuleSystem(unittest.TestCase):
    """Tests for the Runa module system."""
    
    def setUp(self):
        """Set up the test environment."""
        self.vm = VirtualMachine()
        self.compiler = Compiler()
        
        # Create temporary directory for test modules
        self.temp_dir = tempfile.TemporaryDirectory()
        self.modules_dir = Path(self.temp_dir.name)
        
        # Add modules directory to search paths
        self.vm.module_search_paths.insert(0, str(self.modules_dir))
    
    def tearDown(self):
        """Clean up the test environment."""
        self.temp_dir.cleanup()
    
    def _create_module(self, name, source):
        """Create a module file with the given name and source."""
        module_path = self.modules_dir / f"{name}.runa"
        with open(module_path, "w") as f:
            f.write(source)
        return module_path
    
    def _compile_and_run(self, source):
        """Compile and run the given source code."""
        result = self.compiler.compile_string(source)
        self.assertTrue(result.success, f"Compilation failed: {result.error}")
        
        self.vm.load_module(result.module)
        return self.vm.execute_module(result.module.name)
    
    def test_basic_import(self):
        """Test basic module import."""
        # Create test module
        module_source = """
        Let message = "Hello from test_module"
        
        Process called "greet" that takes name:
            Return "Hello, " + name + "!"
        
        export { message, greet }
        """
        self._create_module("test_module", module_source)
        
        # Import the module
        main_source = """
        import test_module
        
        Let result = test_module.message + " - " + test_module.greet("World")
        Return result
        """
        
        result = self._compile_and_run(main_source)
        self.assertEqual(result.type, VMValueType.STRING)
        self.assertEqual(result.value, "Hello from test_module - Hello, World!")
    
    def test_import_specific_items(self):
        """Test importing specific items from a module."""
        # Create test module
        module_source = """
        Let message = "Hello from test_module"
        
        Process called "greet" that takes name:
            Return "Hello, " + name + "!"
        
        Let private_value = "This should not be imported"
        
        export { message, greet }
        """
        self._create_module("test_module", module_source)
        
        # Import specific items
        main_source = """
        import { message, greet } from test_module
        
        Let result = message + " - " + greet("World")
        Return result
        """
        
        result = self._compile_and_run(main_source)
        self.assertEqual(result.type, VMValueType.STRING)
        self.assertEqual(result.value, "Hello from test_module - Hello, World!")
    
    def test_nested_modules(self):
        """Test nested module imports."""
        # Create directory structure
        nested_dir = self.modules_dir / "nested"
        nested_dir.mkdir()
        
        # Create nested module
        nested_module_source = """
        Let message = "Hello from nested module"
        
        export { message }
        """
        with open(nested_dir / "module.runa", "w") as f:
            f.write(nested_module_source)
        
        # Import the nested module
        main_source = """
        import nested.module
        
        Return nested.module.message
        """
        
        result = self._compile_and_run(main_source)
        self.assertEqual(result.type, VMValueType.STRING)
        self.assertEqual(result.value, "Hello from nested module")
    
    def test_namespaces(self):
        """Test namespaces."""
        source = """
        # Create a namespace
        Let math_ns = runa.module.create_namespace("math")
        
        # Add functions to the namespace
        math_ns.add = Process that takes a, b:
            Return a + b
        
        math_ns.subtract = Process that takes a, b:
            Return a - b
        
        # Use the namespace
        Let result = math_ns.add(5, 3) + math_ns.subtract(10, 2)
        
        Return result
        """
        
        result = self._compile_and_run(source)
        self.assertEqual(result.type, VMValueType.INTEGER)
        self.assertEqual(result.value, 16)  # 5 + 3 + (10 - 2) = 16
    
    def test_module_resolution(self):
        """Test module path resolution."""
        # Create test module
        module_source = """
        Let message = "Module found!"
        
        export { message }
        """
        self._create_module("resolution_test", module_source)
        
        # Test resolving the module
        main_source = """
        Let path = runa.module.resolve_path("resolution_test")
        Let module = runa.module.load_module("resolution_test")
        
        Return module.message
        """
        
        result = self._compile_and_run(main_source)
        self.assertEqual(result.type, VMValueType.STRING)
        self.assertEqual(result.value, "Module found!")
    
    def test_circular_imports(self):
        """Test handling of circular imports."""
        # Create module A
        module_a_source = """
        import module_b
        
        Let message = "Module A"
        
        Process called "get_message" that takes:
            Return message + " imports " + module_b.message
        
        export { message, get_message }
        """
        self._create_module("module_a", module_a_source)
        
        # Create module B
        module_b_source = """
        import module_a
        
        Let message = "Module B"
        
        Process called "get_combined" that takes:
            Return module_a.message + " and " + message
        
        export { message, get_combined }
        """
        self._create_module("module_b", module_b_source)
        
        # Test circular imports
        main_source = """
        import module_a
        import module_b
        
        Let result = module_a.get_message() + " and " + module_b.get_combined()
        
        Return result
        """
        
        result = self._compile_and_run(main_source)
        self.assertEqual(result.type, VMValueType.STRING)
        self.assertEqual(result.value, "Module A imports Module B and Module A and Module B")
    
    def test_export_statement(self):
        """Test export statement."""
        # Create test module
        module_source = """
        Let internal_value = 42
        Let exported_value = 100
        
        Process called "get_value" that takes:
            Return exported_value
        
        Process called "set_value" that takes new_value:
            exported_value = new_value
            Return exported_value
        
        export { exported_value, get_value, set_value }
        """
        self._create_module("export_test", module_source)
        
        # Test using the exported values
        main_source = """
        import export_test
        
        Let original = export_test.exported_value
        Let from_getter = export_test.get_value()
        Let new_value = export_test.set_value(200)
        
        Return original + from_getter + new_value
        """
        
        result = self._compile_and_run(main_source)
        self.assertEqual(result.type, VMValueType.INTEGER)
        self.assertEqual(result.value, 400)  # 100 + 100 + 200 = 400


if __name__ == "__main__":
    unittest.main() 