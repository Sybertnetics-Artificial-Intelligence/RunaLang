"""
A simple test script for the Runa type system.

This script directly imports and tests the type system without relying on pytest.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

print("Python path:", sys.path)

try:
    print("Importing types module...")
    from src.semantic.types import (
        Type, TypeSystem, TypeCategory, FunctionType, UnionType, IntersectionType,
        TypeParameter, CustomType
    )
    print("Types module imported successfully")
    
    print("Importing inference module...")
    from src.semantic.inference import TypeInferenceEngine
    print("Inference module imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


def test_primitive_types():
    """Test primitive types."""
    print("\nRunning test_primitive_types...")
    type_system = TypeSystem()
    
    # Check that primitive types exist
    assert type_system.get_type("Int") is not None
    assert type_system.get_type("Float") is not None
    assert type_system.get_type("String") is not None
    assert type_system.get_type("Boolean") is not None
    assert type_system.get_type("Null") is not None
    assert type_system.get_type("Any") is not None
    
    # Check primitive type categories
    int_type = type_system.get_type("Int")
    assert int_type.category == TypeCategory.PRIMITIVE
    
    # Check is_primitive method
    assert int_type.is_primitive()
    
    print("Primitive types test passed!")


def test_assignability():
    """Test type assignability rules."""
    print("\nRunning test_assignability...")
    type_system = TypeSystem()
    
    # Test primitive type assignability
    assert type_system.is_assignable("Int", "Float")
    assert type_system.is_assignable("Null", "Int")
    assert type_system.is_assignable("Null", "Float")
    assert type_system.is_assignable("Null", "String")
    
    # Any type should be assignable to any other type
    assert type_system.is_assignable("Any", "Int")
    assert type_system.is_assignable("Int", "Any")
    
    # Test non-assignable types
    assert not type_system.is_assignable("String", "Int")
    assert not type_system.is_assignable("Boolean", "Float")
    
    print("Assignability test passed!")


def test_generic_types():
    """Test generic types."""
    print("\nRunning test_generic_types...")
    type_system = TypeSystem()
    
    # Check that generic types exist
    assert type_system.get_type("List[T]") is not None
    assert type_system.get_type("Dictionary[K, V]") is not None
    
    # Check specific instantiations
    assert type_system.get_type("List[Int]") is not None
    assert type_system.get_type("List[String]") is not None
    
    # Check generic type assignability
    assert not type_system.is_assignable("List[Int]", "List[String]")
    assert type_system.is_assignable("List[Int]", "List[Int]")
    
    # Test creating new generic instantiations
    list_of_booleans = Type("List", TypeCategory.COMPOSITE, [type_system.get_type("Boolean")])
    type_system.register_type(list_of_booleans)
    assert type_system.get_type("List[Boolean]") is not None
    
    print("Generic types test passed!")


def test_union_types():
    """Test union types."""
    print("\nRunning test_union_types...")
    type_system = TypeSystem()
    
    # Create a union type
    int_type = type_system.get_type("Int")
    string_type = type_system.get_type("String")
    union_type = UnionType([int_type, string_type])
    type_system.register_type(union_type)
    
    # Check that the union type exists
    assert type_system.get_type("Int | String") is not None
    
    # Test union type assignability
    assert type_system.is_assignable("Int", "Int | String")
    assert type_system.is_assignable("String", "Int | String")
    assert not type_system.is_assignable("Boolean", "Int | String")
    
    # Test union type creation through API
    assert type_system.create_union_type(["Int", "Boolean"]) is not None
    assert type_system.get_type("Int | Boolean") is not None
    
    print("Union types test passed!")


def test_function_types():
    """Test function types."""
    print("\nRunning test_function_types...")
    type_system = TypeSystem()
    
    # Create parameter and return types
    int_type = type_system.get_type("Int")
    string_type = type_system.get_type("String")
    
    # Create a function type
    function_type = FunctionType([int_type, string_type], int_type)
    type_system.register_type(function_type)
    
    # Check that the function type exists
    assert type_system.get_type("(Int, String) -> Int") is not None
    
    # Test function type creation through API
    assert type_system.create_function_type(["Int", "Boolean"], "String") is not None
    assert type_system.get_type("(Int, Boolean) -> String") is not None
    
    print("Function types test passed!")


def run_all_tests():
    """Run all tests."""
    print("\nRunning all tests...")
    test_primitive_types()
    test_assignability()
    test_generic_types()
    test_union_types()
    test_function_types()
    print("\nAll tests passed!")


if __name__ == "__main__":
    print("Starting test script...")
    run_all_tests() 