"""
Tests for the Runa type system.

This module contains tests for the type system, including primitive types,
generics, unions, and type inference.
"""

import unittest
from src.semantic.types import (
    Type, TypeSystem, TypeCategory, FunctionType, UnionType, IntersectionType,
    TypeParameter, CustomType
)
from src.semantic.inference import TypeInferenceEngine


class TestTypeSystem(unittest.TestCase):
    """Tests for the TypeSystem class."""
    
    def setUp(self):
        """Set up the type system for each test."""
        self.type_system = TypeSystem()
    
    def test_primitive_types(self):
        """Test primitive types."""
        # Check that primitive types exist
        self.assertIsNotNone(self.type_system.get_type("Int"))
        self.assertIsNotNone(self.type_system.get_type("Float"))
        self.assertIsNotNone(self.type_system.get_type("String"))
        self.assertIsNotNone(self.type_system.get_type("Boolean"))
        self.assertIsNotNone(self.type_system.get_type("Null"))
        self.assertIsNotNone(self.type_system.get_type("Any"))
        
        # Check primitive type categories
        int_type = self.type_system.get_type("Int")
        self.assertEqual(int_type.category, TypeCategory.PRIMITIVE)
        
        # Check is_primitive method
        self.assertTrue(int_type.is_primitive())
    
    def test_assignability(self):
        """Test type assignability rules."""
        # Test primitive type assignability
        self.assertTrue(self.type_system.is_assignable("Int", "Float"))
        self.assertTrue(self.type_system.is_assignable("Null", "Int"))
        self.assertTrue(self.type_system.is_assignable("Null", "Float"))
        self.assertTrue(self.type_system.is_assignable("Null", "String"))
        
        # Any type should be assignable to any other type
        self.assertTrue(self.type_system.is_assignable("Any", "Int"))
        self.assertTrue(self.type_system.is_assignable("Int", "Any"))
        
        # Test non-assignable types
        self.assertFalse(self.type_system.is_assignable("String", "Int"))
        self.assertFalse(self.type_system.is_assignable("Boolean", "Float"))
    
    def test_generic_types(self):
        """Test generic types."""
        # Check that generic types exist
        self.assertIsNotNone(self.type_system.get_type("List[T]"))
        self.assertIsNotNone(self.type_system.get_type("Dictionary[K, V]"))
        
        # Check specific instantiations
        self.assertIsNotNone(self.type_system.get_type("List[Int]"))
        self.assertIsNotNone(self.type_system.get_type("List[String]"))
        
        # Check generic type assignability
        self.assertFalse(self.type_system.is_assignable("List[Int]", "List[String]"))
        self.assertTrue(self.type_system.is_assignable("List[Int]", "List[Int]"))
        
        # Test creating new generic instantiations
        list_of_booleans = Type("List", TypeCategory.COMPOSITE, [self.type_system.get_type("Boolean")])
        self.type_system.register_type(list_of_booleans)
        self.assertIsNotNone(self.type_system.get_type("List[Boolean]"))
    
    def test_union_types(self):
        """Test union types."""
        # Create a union type
        int_type = self.type_system.get_type("Int")
        string_type = self.type_system.get_type("String")
        union_type = UnionType([int_type, string_type])
        self.type_system.register_type(union_type)
        
        # Check that the union type exists
        self.assertIsNotNone(self.type_system.get_type("Int | String"))
        
        # Test union type assignability
        self.assertTrue(self.type_system.is_assignable("Int", "Int | String"))
        self.assertTrue(self.type_system.is_assignable("String", "Int | String"))
        self.assertFalse(self.type_system.is_assignable("Boolean", "Int | String"))
        
        # Test union type creation through API
        self.assertIsNotNone(self.type_system.create_union_type(["Int", "Boolean"]))
        self.assertIsNotNone(self.type_system.get_type("Int | Boolean"))
    
    def test_intersection_types(self):
        """Test intersection types."""
        # Create custom types for interfaces
        comparable = CustomType("Comparable")
        printable = CustomType("Printable")
        self.type_system.register_type(comparable)
        self.type_system.register_type(printable)
        
        # Create an intersection type
        intersection_type = IntersectionType([comparable, printable])
        self.type_system.register_type(intersection_type)
        
        # Check that the intersection type exists
        self.assertIsNotNone(self.type_system.get_type("Comparable & Printable"))
        
        # Create a custom type that implements both interfaces
        comparable_printable = CustomType("ComparablePrintable", parent_types=[comparable, printable])
        self.type_system.register_type(comparable_printable)
        
        # Test intersection type assignability
        self.assertTrue(self.type_system.is_assignable("ComparablePrintable", "Comparable"))
        self.assertTrue(self.type_system.is_assignable("ComparablePrintable", "Printable"))
        self.assertTrue(self.type_system.is_assignable("ComparablePrintable", "Comparable & Printable"))
    
    def test_function_types(self):
        """Test function types."""
        # Create parameter and return types
        int_type = self.type_system.get_type("Int")
        string_type = self.type_system.get_type("String")
        
        # Create a function type
        function_type = FunctionType([int_type, string_type], int_type)
        self.type_system.register_type(function_type)
        
        # Check that the function type exists
        self.assertIsNotNone(self.type_system.get_type("(Int, String) -> Int"))
        
        # Test function type creation through API
        self.assertIsNotNone(self.type_system.create_function_type(["Int", "Boolean"], "String"))
        self.assertIsNotNone(self.type_system.get_type("(Int, Boolean) -> String"))
    
    def test_custom_types(self):
        """Test custom types."""
        # Create a custom type with fields and methods
        fields = {"name": self.type_system.get_type("String"), "age": self.type_system.get_type("Int")}
        methods = {}
        
        # Add a method to the custom type
        method_params = [self.type_system.get_type("String")]
        method_return = self.type_system.get_type("Boolean")
        methods["validate"] = FunctionType(method_params, method_return)
        
        # Create the custom type
        person_type = CustomType("Person", fields, methods)
        self.type_system.register_type(person_type)
        
        # Check that the custom type exists
        self.assertIsNotNone(self.type_system.get_type("Person"))
        
        # Test field and method access
        self.assertEqual(person_type.get_field_type("name"), self.type_system.get_type("String"))
        self.assertEqual(person_type.get_field_type("age"), self.type_system.get_type("Int"))
        self.assertIsNotNone(person_type.get_method_type("validate"))
        
        # Test custom type creation through API
        self.assertIsNotNone(self.type_system.create_custom_type(
            "Employee",
            {"name": "String", "salary": "Float"},
            {"get_bonus": (["Float"], "Float")},
            ["Person"]
        ))
        self.assertIsNotNone(self.type_system.get_type("Employee"))
        
        # Test inheritance
        employee_type = self.type_system.get_type("Employee")
        self.assertEqual(employee_type.get_field_type("name"), self.type_system.get_type("String"))
        self.assertEqual(employee_type.get_field_type("age"), self.type_system.get_type("Int"))
    
    def test_common_type(self):
        """Test finding common types."""
        # Test common type between primitives
        self.assertEqual(self.type_system.common_type("Int", "Int"), "Int")
        self.assertEqual(self.type_system.common_type("Int", "Float"), "Float")
        
        # Test common type with union types
        int_string_union = self.type_system.create_union_type(["Int", "String"])
        self.assertEqual(
            self.type_system.common_type("Int", "String"),
            "Int | String"
        )
        
        # Test common type with Any
        self.assertEqual(self.type_system.common_type("Int", "Any"), "Any")
        self.assertEqual(self.type_system.common_type("Any", "String"), "Any")
    
    def test_parse_type_string(self):
        """Test parsing type strings."""
        # Test parsing primitive types
        self.assertEqual(self.type_system.parse_type_string("Int"), self.type_system.get_type("Int"))
        
        # Test parsing generic types
        list_int_type = self.type_system.parse_type_string("List[Int]")
        self.assertEqual(list_int_type.name, "List")
        self.assertEqual(list_int_type.subtypes[0], self.type_system.get_type("Int"))
        
        # Test parsing union types
        int_string_union = self.type_system.create_union_type(["Int", "String"])
        union_type = self.type_system.parse_type_string("Int | String")
        self.assertEqual(str(union_type), "Int | String")


class TestTypeInference(unittest.TestCase):
    """Tests for the TypeInferenceEngine class."""
    
    def setUp(self):
        """Set up the type system and inference engine for each test."""
        self.type_system = TypeSystem()
        self.engine = TypeInferenceEngine(self.type_system)
    
    def test_infer_literal_types(self):
        """Test inferring types of literals."""
        from src.parser.ast import Literal
        
        # Create literal nodes
        int_literal = Literal("int", "42")
        float_literal = Literal("float", "3.14")
        string_literal = Literal("string", "hello")
        bool_literal = Literal("boolean", "true")
        null_literal = Literal("null", "null")
        
        # Create inference context
        from src.semantic.inference import InferenceContext
        context = InferenceContext(self.type_system)
        
        # Test literal type inference
        self.assertEqual(self.engine._infer_literal_type(int_literal, context), "Int")
        self.assertEqual(self.engine._infer_literal_type(float_literal, context), "Float")
        self.assertEqual(self.engine._infer_literal_type(string_literal, context), "String")
        self.assertEqual(self.engine._infer_literal_type(bool_literal, context), "Boolean")
        self.assertEqual(self.engine._infer_literal_type(null_literal, context), "Null")
    
    def test_constraint_solving(self):
        """Test solving type constraints."""
        from src.semantic.inference import InferenceContext
        
        # Create inference context with constraints
        context = InferenceContext(self.type_system)
        
        # Create type variables
        t1 = context.create_type_var()
        t2 = context.create_type_var()
        t3 = context.create_type_var()
        
        # Add constraints
        context.add_constraint(t1, "Int")
        context.add_constraint(t2, t1)
        context.add_constraint(t3, "String")
        context.add_constraint(t2, "Float")
        
        # Solve constraints
        self.engine._solve_constraints(context)
        
        # Check inferred types
        self.assertEqual(context.resolve_type_var(t1), "Int")
        self.assertEqual(context.resolve_type_var(t2), "Float")
        self.assertEqual(context.resolve_type_var(t3), "String")


if __name__ == "__main__":
    unittest.main() 