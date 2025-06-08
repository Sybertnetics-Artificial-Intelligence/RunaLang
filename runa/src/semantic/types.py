"""
Type system for the Runa programming language.

This module defines the type system and provides utilities for type checking.
"""

from typing import Dict, Set, Optional, List
from enum import Enum, auto


class TypeCategory(Enum):
    """Categories of types in the Runa type system."""
    
    PRIMITIVE = auto()  # Int, Float, String, Boolean, Null
    COMPOSITE = auto()  # List, Dictionary, etc.
    FUNCTION = auto()   # Function types
    CUSTOM = auto()     # User-defined types


class Type:
    """
    Represents a type in the Runa type system.
    
    Attributes:
        name: The name of the type
        category: The category of the type
        subtypes: Child types for generic types (like List[Int])
    """
    
    def __init__(
        self,
        name: str,
        category: TypeCategory,
        subtypes: Optional[List['Type']] = None
    ):
        """
        Initialize a new Type.
        
        Args:
            name: The name of the type
            category: The category of the type
            subtypes: Child types for generic types
        """
        self.name = name
        self.category = category
        self.subtypes = subtypes or []
    
    def __str__(self) -> str:
        """Return a string representation of the type."""
        if not self.subtypes:
            return self.name
        
        subtypes_str = ", ".join(str(subtype) for subtype in self.subtypes)
        return f"{self.name}[{subtypes_str}]"
    
    def __eq__(self, other) -> bool:
        """Compare two types for equality."""
        if not isinstance(other, Type):
            return False
        
        # Check name and category
        if self.name != other.name or self.category != other.category:
            return False
        
        # Check subtypes
        if len(self.subtypes) != len(other.subtypes):
            return False
        
        for i, subtype in enumerate(self.subtypes):
            if subtype != other.subtypes[i]:
                return False
        
        return True


class TypeSystem:
    """
    Type system for the Runa programming language.
    
    This class manages the type hierarchy and provides type checking utilities.
    
    Attributes:
        types: Dictionary of registered types
        assignable_types: Sets of types that are assignable to each type
    """
    
    def __init__(self):
        """Initialize a new TypeSystem with built-in types."""
        self.types: Dict[str, Type] = {}
        self.assignable_types: Dict[str, Set[str]] = {}
        
        # Register built-in types
        self._register_built_in_types()
    
    def _register_built_in_types(self) -> None:
        """Register built-in types in the type system."""
        # Primitive types
        self.register_type(Type("Int", TypeCategory.PRIMITIVE))
        self.register_type(Type("Float", TypeCategory.PRIMITIVE))
        self.register_type(Type("String", TypeCategory.PRIMITIVE))
        self.register_type(Type("Boolean", TypeCategory.PRIMITIVE))
        self.register_type(Type("Null", TypeCategory.PRIMITIVE))
        
        # Composite types
        self.register_type(Type("List", TypeCategory.COMPOSITE))
        self.register_type(Type("Dictionary", TypeCategory.COMPOSITE))
        
        # Define assignability rules
        self.register_assignable("Int", "Float")  # Int can be assigned to Float
        self.register_assignable("Null", "Int")   # Null can be assigned to any type
        self.register_assignable("Null", "Float")
        self.register_assignable("Null", "String")
        self.register_assignable("Null", "Boolean")
        self.register_assignable("Null", "List")
        self.register_assignable("Null", "Dictionary")
    
    def register_type(self, type_obj: Type) -> None:
        """
        Register a type in the type system.
        
        Args:
            type_obj: The type to register
        """
        self.types[type_obj.name] = type_obj
        
        # Initialize assignable types set (a type is always assignable to itself)
        if type_obj.name not in self.assignable_types:
            self.assignable_types[type_obj.name] = {type_obj.name}
    
    def register_assignable(self, from_type: str, to_type: str) -> None:
        """
        Register that from_type can be assigned to to_type.
        
        Args:
            from_type: The source type
            to_type: The target type
        """
        if to_type not in self.assignable_types:
            self.assignable_types[to_type] = {to_type}
        
        self.assignable_types[to_type].add(from_type)
    
    def get_type(self, name: str) -> Optional[Type]:
        """
        Get a type by name.
        
        Args:
            name: The name of the type
            
        Returns:
            The Type object or None if not found
        """
        return self.types.get(name)
    
    def is_assignable(self, from_type: str, to_type: str) -> bool:
        """
        Check if from_type can be assigned to to_type.
        
        Args:
            from_type: The source type
            to_type: The target type
            
        Returns:
            True if assignable, False otherwise
        """
        if to_type not in self.assignable_types:
            return False
        
        return from_type in self.assignable_types[to_type]
    
    def common_type(self, type1: str, type2: str) -> Optional[str]:
        """
        Find the common type that both type1 and type2 can be assigned to.
        
        Args:
            type1: The first type
            type2: The second type
            
        Returns:
            The common type or None if there isn't one
        """
        # If they're the same type, that's the common type
        if type1 == type2:
            return type1
        
        # If one can be assigned to the other, the other is the common type
        if self.is_assignable(type1, type2):
            return type2
        
        if self.is_assignable(type2, type1):
            return type1
        
        # Special case for numeric types
        if {type1, type2} == {"Int", "Float"}:
            return "Float"
        
        # No common type
        return None 