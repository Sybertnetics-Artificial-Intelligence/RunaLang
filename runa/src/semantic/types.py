"""
Type system for the Runa programming language.

This module defines the type system and provides utilities for type checking.
The type system supports primitive types, generics, unions, and user-defined types.
"""

from typing import Dict, Set, Optional, List, Tuple, Any, Union as PyUnion
from enum import Enum, auto


class TypeCategory(Enum):
    """Categories of types in the Runa type system."""
    
    PRIMITIVE = auto()  # Int, Float, String, Boolean, Null
    COMPOSITE = auto()  # List, Dictionary, etc.
    FUNCTION = auto()   # Function types
    UNION = auto()      # Union types (Int | String)
    INTERSECTION = auto() # Intersection types (Comparable & Printable)
    CUSTOM = auto()     # User-defined types
    TYPE_PARAMETER = auto()  # Type parameters for generics (T, K, V)


class TypeConstraint(Enum):
    """Constraints that can be applied to type parameters."""
    
    NONE = auto()  # No constraint
    COMPARABLE = auto()  # Type must be comparable
    NUMERIC = auto()  # Type must be numeric
    HASHABLE = auto()  # Type must be hashable
    PRINTABLE = auto()  # Type must be printable
    ITERABLE = auto()  # Type must be iterable
    CALLABLE = auto()  # Type must be callable


class Type:
    """
    Represents a type in the Runa type system.
    
    Attributes:
        name: The name of the type
        category: The category of the type
        subtypes: Child types for generic types (like List[Int])
        constraints: Constraints for type parameters
    """
    
    def __init__(
        self,
        name: str,
        category: TypeCategory,
        subtypes: Optional[List['Type']] = None,
        constraints: Optional[List[TypeConstraint]] = None
    ):
        """
        Initialize a new Type.
        
        Args:
            name: The name of the type
            category: The category of the type
            subtypes: Child types for generic types
            constraints: Constraints for type parameters
        """
        self.name = name
        self.category = category
        self.subtypes = subtypes or []
        self.constraints = constraints or []
        
        # Additional properties for function types
        self.parameter_types: List[Type] = []
        self.return_type: Optional[Type] = None
        
        # Properties for custom/user-defined types
        self.fields: Dict[str, Type] = {}
        self.methods: Dict[str, 'Type'] = {}
        self.parent_types: List['Type'] = []
    
    def __str__(self) -> str:
        """Return a string representation of the type."""
        if self.category == TypeCategory.FUNCTION:
            params = ", ".join(str(param) for param in self.parameter_types)
            return f"({params}) -> {self.return_type}"
            
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
    
    def is_primitive(self) -> bool:
        """Check if this is a primitive type."""
        return self.category == TypeCategory.PRIMITIVE
    
    def is_composite(self) -> bool:
        """Check if this is a composite type."""
        return self.category == TypeCategory.COMPOSITE
    
    def is_function(self) -> bool:
        """Check if this is a function type."""
        return self.category == TypeCategory.FUNCTION
    
    def is_union(self) -> bool:
        """Check if this is a union type."""
        return self.category == TypeCategory.UNION
    
    def is_intersection(self) -> bool:
        """Check if this is an intersection type."""
        return self.category == TypeCategory.INTERSECTION
    
    def is_generic(self) -> bool:
        """Check if this is a generic type."""
        return bool(self.subtypes) and any(
            subtype.category == TypeCategory.TYPE_PARAMETER 
            for subtype in self.subtypes
        )
    
    def is_custom(self) -> bool:
        """Check if this is a custom/user-defined type."""
        return self.category == TypeCategory.CUSTOM
    
    def is_type_parameter(self) -> bool:
        """Check if this is a type parameter."""
        return self.category == TypeCategory.TYPE_PARAMETER
    
    def has_constraint(self, constraint: TypeConstraint) -> bool:
        """Check if this type has a specific constraint."""
        return constraint in self.constraints


class FunctionType(Type):
    """
    Represents a function type in the Runa type system.
    
    Attributes:
        parameter_types: The types of the function parameters
        return_type: The return type of the function
    """
    
    def __init__(
        self,
        parameter_types: List[Type],
        return_type: Type
    ):
        """
        Initialize a new FunctionType.
        
        Args:
            parameter_types: The types of the function parameters
            return_type: The return type of the function
        """
        super().__init__("Function", TypeCategory.FUNCTION)
        self.parameter_types = parameter_types
        self.return_type = return_type
    
    def __str__(self) -> str:
        """Return a string representation of the function type."""
        params = ", ".join(str(param) for param in self.parameter_types)
        return f"({params}) -> {self.return_type}"
    
    def __eq__(self, other) -> bool:
        """Compare two function types for equality."""
        if not isinstance(other, FunctionType):
            return False
        
        # Check return type
        if self.return_type != other.return_type:
            return False
        
        # Check parameter types
        if len(self.parameter_types) != len(other.parameter_types):
            return False
        
        for i, param_type in enumerate(self.parameter_types):
            if param_type != other.parameter_types[i]:
                return False
        
        return True


class UnionType(Type):
    """
    Represents a union type in the Runa type system.
    
    A union type can be one of several types (e.g., Int | String).
    
    Attributes:
        types: The possible types in the union
    """
    
    def __init__(self, types: List[Type]):
        """
        Initialize a new UnionType.
        
        Args:
            types: The possible types in the union
        """
        super().__init__("Union", TypeCategory.UNION, types)
    
    def __str__(self) -> str:
        """Return a string representation of the union type."""
        return " | ".join(str(t) for t in self.subtypes)
    
    def __eq__(self, other) -> bool:
        """Compare two union types for equality."""
        if not isinstance(other, UnionType):
            return False
        
        # Check if both unions have the same set of types
        # (order doesn't matter for unions)
        return set(str(t) for t in self.subtypes) == set(str(t) for t in other.subtypes)


class IntersectionType(Type):
    """
    Represents an intersection type in the Runa type system.
    
    An intersection type must satisfy all of the component types
    (e.g., Comparable & Printable).
    
    Attributes:
        types: The component types in the intersection
    """
    
    def __init__(self, types: List[Type]):
        """
        Initialize a new IntersectionType.
        
        Args:
            types: The component types in the intersection
        """
        super().__init__("Intersection", TypeCategory.INTERSECTION, types)
    
    def __str__(self) -> str:
        """Return a string representation of the intersection type."""
        return " & ".join(str(t) for t in self.subtypes)
    
    def __eq__(self, other) -> bool:
        """Compare two intersection types for equality."""
        if not isinstance(other, IntersectionType):
            return False
        
        # Check if both intersections have the same set of types
        # (order doesn't matter for intersections)
        return set(str(t) for t in self.subtypes) == set(str(t) for t in other.subtypes)


class TypeParameter(Type):
    """
    Represents a type parameter in the Runa type system.
    
    Type parameters are used in generic types (e.g., T in List[T]).
    
    Attributes:
        name: The name of the type parameter
        constraints: Constraints that the type parameter must satisfy
    """
    
    def __init__(
        self,
        name: str,
        constraints: Optional[List[TypeConstraint]] = None
    ):
        """
        Initialize a new TypeParameter.
        
        Args:
            name: The name of the type parameter
            constraints: Constraints that the type parameter must satisfy
        """
        super().__init__(name, TypeCategory.TYPE_PARAMETER, constraints=constraints or [])
    
    def __str__(self) -> str:
        """Return a string representation of the type parameter."""
        if not self.constraints:
            return self.name
        
        constraints_str = " & ".join(str(c.name) for c in self.constraints)
        return f"{self.name}: {constraints_str}"


class CustomType(Type):
    """
    Represents a user-defined type in the Runa type system.
    
    Attributes:
        name: The name of the type
        fields: The fields of the type
        methods: The methods of the type
        parent_types: The parent types that this type inherits from
    """
    
    def __init__(
        self,
        name: str,
        fields: Optional[Dict[str, Type]] = None,
        methods: Optional[Dict[str, FunctionType]] = None,
        parent_types: Optional[List[Type]] = None
    ):
        """
        Initialize a new CustomType.
        
        Args:
            name: The name of the type
            fields: The fields of the type
            methods: The methods of the type
            parent_types: The parent types that this type inherits from
        """
        super().__init__(name, TypeCategory.CUSTOM)
        self.fields = fields or {}
        self.methods = methods or {}
        self.parent_types = parent_types or []
    
    def get_field_type(self, field_name: str) -> Optional[Type]:
        """
        Get the type of a field.
        
        Args:
            field_name: The name of the field
            
        Returns:
            The type of the field or None if the field doesn't exist
        """
        if field_name in self.fields:
            return self.fields[field_name]
        
        # Check parent types
        for parent in self.parent_types:
            if isinstance(parent, CustomType):
                field_type = parent.get_field_type(field_name)
                if field_type:
                    return field_type
        
        return None
    
    def get_method_type(self, method_name: str) -> Optional[FunctionType]:
        """
        Get the type of a method.
        
        Args:
            method_name: The name of the method
            
        Returns:
            The type of the method or None if the method doesn't exist
        """
        if method_name in self.methods:
            return self.methods[method_name]
        
        # Check parent types
        for parent in self.parent_types:
            if isinstance(parent, CustomType):
                method_type = parent.get_method_type(method_name)
                if method_type:
                    return method_type
        
        return None


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
        self.register_type(Type("Any", TypeCategory.PRIMITIVE))
        
        # Type parameters for generic types
        t_param = TypeParameter("T")
        k_param = TypeParameter("K")
        v_param = TypeParameter("V")
        
        # Composite types
        list_type = Type("List", TypeCategory.COMPOSITE, [t_param])
        dict_type = Type("Dictionary", TypeCategory.COMPOSITE, [k_param, v_param])
        self.register_type(list_type)
        self.register_type(dict_type)
        
        # Create specific instantiations of generic types
        int_list = Type("List", TypeCategory.COMPOSITE, [self.get_type("Int")])
        string_list = Type("List", TypeCategory.COMPOSITE, [self.get_type("String")])
        
        # Register common specialized types
        self.register_type(int_list)
        self.register_type(string_list)
        
        # Define assignability rules
        self.register_assignable("Int", "Float")  # Int can be assigned to Float
        self.register_assignable("Null", "Int")   # Null can be assigned to any type
        self.register_assignable("Null", "Float")
        self.register_assignable("Null", "String")
        self.register_assignable("Null", "Boolean")
        self.register_assignable("Null", "List")
        self.register_assignable("Null", "Dictionary")
        
        # Any type is assignable to any other type
        self.register_assignable("Any", "Int")
        self.register_assignable("Any", "Float")
        self.register_assignable("Any", "String")
        self.register_assignable("Any", "Boolean")
        self.register_assignable("Any", "List")
        self.register_assignable("Any", "Dictionary")
        
        # And any type is assignable to Any
        self.register_assignable("Int", "Any")
        self.register_assignable("Float", "Any")
        self.register_assignable("String", "Any")
        self.register_assignable("Boolean", "Any")
        self.register_assignable("List", "Any")
        self.register_assignable("Dictionary", "Any")
    
    def register_type(self, type_obj: Type) -> None:
        """
        Register a type in the type system.
        
        Args:
            type_obj: The type to register
        """
        type_name = str(type_obj)
        self.types[type_name] = type_obj
        
        # Initialize assignable types set (a type is always assignable to itself)
        if type_name not in self.assignable_types:
            self.assignable_types[type_name] = {type_name}
    
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
        # Check direct assignability
        if to_type in self.assignable_types and from_type in self.assignable_types[to_type]:
            return True
        
        # Parse type strings to handle generic types
        from_type_obj = self.parse_type_string(from_type)
        to_type_obj = self.parse_type_string(to_type)
        
        if not from_type_obj or not to_type_obj:
            return False
        
        # Check generic type compatibility
        if from_type_obj.name == to_type_obj.name and from_type_obj.category == to_type_obj.category:
            # Same type name and category, check subtypes
            if len(from_type_obj.subtypes) != len(to_type_obj.subtypes):
                return False
            
            # Check if all subtypes are assignable
            for i, from_subtype in enumerate(from_type_obj.subtypes):
                to_subtype = to_type_obj.subtypes[i]
                if not self.is_assignable(str(from_subtype), str(to_subtype)):
                    return False
            
            return True
        
        # Handle union types
        if from_type_obj.is_union():
            # A union is assignable to a type if all of its component types are assignable to that type
            return all(self.is_assignable(str(t), to_type) for t in from_type_obj.subtypes)
        
        if to_type_obj.is_union():
            # A type is assignable to a union if it's assignable to any of the union's component types
            return any(self.is_assignable(from_type, str(t)) for t in to_type_obj.subtypes)
        
        # Handle intersection types
        if to_type_obj.is_intersection():
            # A type is assignable to an intersection if it's assignable to all of the intersection's component types
            return all(self.is_assignable(from_type, str(t)) for t in to_type_obj.subtypes)
        
        # No other rules match
        return False
    
    def parse_type_string(self, type_str: str) -> Optional[Type]:
        """
        Parse a type string into a Type object.
        
        Args:
            type_str: The type string to parse
            
        Returns:
            The parsed Type object or None if parsing fails
        """
        # Check if the type is already registered
        if type_str in self.types:
            return self.types[type_str]
        
        # Check for union types
        if "|" in type_str:
            type_names = [name.strip() for name in type_str.split("|")]
            types = [self.get_type(name) for name in type_names]
            
            # Only create a union if all component types exist
            if all(types):
                return UnionType(types)
            
            return None
        
        # Check for intersection types
        if "&" in type_str:
            type_names = [name.strip() for name in type_str.split("&")]
            types = [self.get_type(name) for name in type_names]
            
            # Only create an intersection if all component types exist
            if all(types):
                return IntersectionType(types)
            
            return None
        
        # Check for generic types
        if "[" in type_str and "]" in type_str:
            # Extract base type and parameters
            base_name = type_str[:type_str.index("[")]
            params_str = type_str[type_str.index("[") + 1:type_str.rindex("]")]
            
            # Parse parameter types
            param_names = [name.strip() for name in params_str.split(",")]
            param_types = [self.get_type(name) for name in param_names]
            
            # Only create a generic type if the base type and all parameters exist
            base_type = self.get_type(base_name)
            if base_type and all(param_types):
                return Type(base_type.name, base_type.category, param_types)
            
            return None
        
        # No special parsing needed
        return None
    
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
        
        # Try to create a union type
        type1_obj = self.get_type(type1)
        type2_obj = self.get_type(type2)
        
        if type1_obj and type2_obj:
            union_type = UnionType([type1_obj, type2_obj])
            self.register_type(union_type)
            return str(union_type)
        
        # No common type
        return None
    
    def create_function_type(
        self,
        parameter_types: List[str],
        return_type: str
    ) -> Optional[FunctionType]:
        """
        Create a function type with the given parameter types and return type.
        
        Args:
            parameter_types: The types of the function parameters
            return_type: The return type of the function
            
        Returns:
            The created FunctionType or None if any of the types don't exist
        """
        param_types_obj = [self.get_type(param) for param in parameter_types]
        return_type_obj = self.get_type(return_type)
        
        # Only create a function type if all types exist
        if all(param_types_obj) and return_type_obj:
            function_type = FunctionType(param_types_obj, return_type_obj)
            self.register_type(function_type)
            return function_type
        
        return None
    
    def create_union_type(self, types: List[str]) -> Optional[UnionType]:
        """
        Create a union type with the given types.
        
        Args:
            types: The types in the union
            
        Returns:
            The created UnionType or None if any of the types don't exist
        """
        type_objs = [self.get_type(t) for t in types]
        
        # Only create a union type if all types exist
        if all(type_objs):
            union_type = UnionType(type_objs)
            self.register_type(union_type)
            return union_type
        
        return None
    
    def create_intersection_type(self, types: List[str]) -> Optional[IntersectionType]:
        """
        Create an intersection type with the given types.
        
        Args:
            types: The types in the intersection
            
        Returns:
            The created IntersectionType or None if any of the types don't exist
        """
        type_objs = [self.get_type(t) for t in types]
        
        # Only create an intersection type if all types exist
        if all(type_objs):
            intersection_type = IntersectionType(type_objs)
            self.register_type(intersection_type)
            return intersection_type
        
        return None
    
    def create_custom_type(
        self,
        name: str,
        fields: Dict[str, str],
        methods: Dict[str, Tuple[List[str], str]],
        parent_types: List[str] = None
    ) -> Optional[CustomType]:
        """
        Create a custom type with the given fields, methods, and parent types.
        
        Args:
            name: The name of the type
            fields: Dictionary mapping field names to type names
            methods: Dictionary mapping method names to (parameter types, return type) tuples
            parent_types: List of parent type names
            
        Returns:
            The created CustomType or None if any of the types don't exist
        """
        # Convert field types
        field_types = {}
        for field_name, type_name in fields.items():
            field_type = self.get_type(type_name)
            if not field_type:
                return None
            field_types[field_name] = field_type
        
        # Convert method types
        method_types = {}
        for method_name, (param_types, ret_type) in methods.items():
            function_type = self.create_function_type(param_types, ret_type)
            if not function_type:
                return None
            method_types[method_name] = function_type
        
        # Convert parent types
        parent_type_objs = []
        if parent_types:
            for parent_name in parent_types:
                parent_type = self.get_type(parent_name)
                if not parent_type:
                    return None
                parent_type_objs.append(parent_type)
        
        # Create and register the custom type
        custom_type = CustomType(name, field_types, method_types, parent_type_objs)
        self.register_type(custom_type)
        
        return custom_type 