# Enhanced Type System in Runa

Runa's enhanced type system provides flexible typing with powerful features that balance the benefits of static typing with the expressiveness of dynamic typing. This guide explains the type system features and how to effectively use them in your code.

## Introduction to Runa's Type System

Runa's type system is designed to be:
- **Optional**: Type annotations are not required but provide benefits when used
- **Inferential**: Types can often be inferred without explicit annotations
- **Gradual**: You can mix typed and untyped code as needed
- **Expressive**: Supports complex types including generics and algebraic data types
- **Natural**: Type syntax follows Runa's natural language philosophy

## Basic Types

Runa includes the following basic types:

```
Type Any                     # Any value
Type Integer                 # Whole numbers (e.g., 1, -5, 42)
Type Float                   # Floating-point numbers (e.g., 3.14, -0.5)
Type Boolean                 # Boolean values (true, false)
Type String                  # Text strings (e.g., "Hello")
Type None                    # The unit type, represented by None
```

## Collection Types

Runa provides parameterized collection types:

```
Type List[T]                 # List of elements of type T
Type Dictionary[K, V]        # Dictionary with keys of type K and values of type V
Type Set[T]                  # Set of elements of type T
Type Tuple[T1, T2, ...]      # Tuple with elements of specified types
```

## Function Types

Function types describe the inputs and outputs of functions:

```
Type Function[T1, T2, ..., R]  # Function taking arguments of types T1, T2, ... and returning type R
```

## Declaring Variables with Types

You can explicitly declare the type of a variable:

```
Let name be String "Alex"
Let age be Integer 28
Let is_active be Boolean true
Let points be Float 75.5
```

Runa can also infer types automatically:

```
Let name be "Alex"          # Inferred as String
Let age be 28               # Inferred as Integer
Let is_active be true       # Inferred as Boolean
Let points be 75.5          # Inferred as Float
```

## Type Definitions

You can define custom types using the `Type` keyword:

```
# Simple type alias
Type UserId is Integer

# Record type
Type Person is Dictionary with:
    name as String
    age as Integer
    email as String

# Create a value of the custom type
Let user be Person with:
    name as "Alice"
    age as 30
    email as "alice@example.com"
```

## Type Annotations for Functions

Function parameters and return types can be annotated:

```
Process called "calculate_discount" that takes price as Float and percentage as Float returns Float:
    Return price multiplied by (1 minus (percentage divided by 100))

# Call the function
Let discounted_price be calculate_discount with price as 100.0 and percentage as 20.0
```

Return types can be inferred in many cases:

```
Process called "increment" that takes value as Integer:  # Return type is inferred as Integer
    Return value plus 1
```

## Generic Types

Runa supports generic types for creating flexible, reusable code:

```
# Generic identity function
Process called "identity"[T] that takes value as T returns T:
    Return value

# Generic pair type
Type Pair[A, B] is Dictionary with:
    first as A
    second as B

# Create a pair
Let point be Pair[Integer, Integer] with:
    first as 10
    second as 20
```

## Type Constraints

You can specify constraints on generic types:

```
# Constrain to types that support comparison
Process called "max"[T: Comparable] that takes a as T and b as T returns T:
    If a is greater than b:
        Return a
    Otherwise:
        Return b

# Constrain to types that support addition
Process called "sum"[T: Addable] that takes list as List[T] returns T:
    Let result be first value in list
    For each item in rest of list:
        Set result to result plus item
    Return result
```

## Union Types

Union types represent values that could be one of several types:

```
Type Result is Integer OR String

Process called "safe_divide" that takes a as Integer and b as Integer returns Result:
    If b is equal to 0:
        Return "Cannot divide by zero"
    Otherwise:
        Return a divided by b

Let result be safe_divide with a as 10 and b as 2
Match type of result:
    When Integer:
        Display "Result:" with message result
    When String:
        Display "Error:" with message result
```

## Intersection Types

Intersection types combine multiple type requirements:

```
Type Serializable is Interface with:
    to_json as Function[String]

Type Validatable is Interface with:
    validate as Function[Boolean]

Type SerializableAndValidatable is Serializable AND Validatable

Process called "process_data" that takes data as SerializableAndValidatable:
    If data.validate():
        Return data.to_json()
    Otherwise:
        Return "Invalid data"
```

## Algebraic Data Types

Algebraic data types (ADTs) allow you to define composite types:

```
# Sum type (variant)
Type Shape is
    | Circle with radius as Float
    | Rectangle with width as Float and height as Float
    | Triangle with base as Float and height as Float

# Create shapes
Let circle be Shape.Circle with radius as 5.0
Let rectangle be Shape.Rectangle with width as 4.0 and height as 3.0

# Calculate area based on shape type
Process called "calculate_area" that takes shape as Shape returns Float:
    Match shape:
        When Circle with radius as r:
            Return 3.14159 multiplied by r multiplied by r
        When Rectangle with width as w and height as h:
            Return w multiplied by h
        When Triangle with base as b and height as h:
            Return 0.5 multiplied by b multiplied by h
```

## Type Inference

Runa's type inference system reduces the need for explicit annotations:

```
# Type is inferred as Dictionary[String, Integer]
Let scores be dictionary with:
    "Alice" as 95
    "Bob" as 87
    "Charlie" as 92

# Return type is inferred as the same type as 'value'
Process called "double" that takes value:
    Return value multiplied by 2

# Types are propagated through expressions
Let numbers be list containing 1, 2, 3
Let doubled be Map over numbers using double
# doubled is inferred as List[Integer]
```

## Structural Typing

Runa uses structural typing, which focuses on the shape of data rather than its nominal type:

```
# Any dictionary with a 'name' field of type String can be used here
Process called "greet" that takes person as Dictionary with name as String:
    Return "Hello, " followed by person["name"]

# Works with any dictionary containing a name field
Let user1 be dictionary with:
    "name" as "Alice"
    "age" as 30

Let user2 be dictionary with:
    "name" as "Bob"
    "email" as "bob@example.com"

Let greeting1 be greet with person as user1  # Works
Let greeting2 be greet with person as user2  # Also works
```

## Type Guards

Type guards help narrow down types in conditional branches:

```
Process called "process_value" that takes value as Any:
    If value is of type Integer:
        Return value multiplied by 2
    Otherwise if value is of type String:
        Return value followed by value
    Otherwise:
        Return "Unsupported type"
```

## Optional Types

Optional types represent values that might be absent:

```
Type Optional[T] is T OR None

Process called "find_user" that takes id as String returns Optional[User]:
    # Try to find user
    If user_exists with id as id:
        Return get_user with id as id
    Otherwise:
        Return None

Let user be find_user with id as "123"
If user is not None:
    Display "Found user:" with message user["name"]
Otherwise:
    Display "User not found"
```

## Interfaces and Protocols

Interfaces define expected behavior:

```
Type Shippable is Interface with:
    get_weight as Function[Float]
    get_dimensions as Function[Dictionary[String, Float]]

Type Package is Dictionary with:
    contents as String
    weight as Float
    width as Float
    height as Float
    depth as Float
    implements Shippable

# Implement the interface
Process called "get_weight" that takes self as Package returns Float:
    Return self["weight"]

Process called "get_dimensions" that takes self as Package returns Dictionary[String, Float]:
    Return dictionary with:
        "width" as self["width"]
        "height" as self["height"]
        "depth" as self["depth"]
```

## Type Assertions

You can assert the type of a value when needed:

```
# Assert that value is an Integer
Let age be 30 as Integer

# Dynamic assertion
Process called "process_data" that takes data as Any:
    Let user be data as Dictionary[String, Any]
    Let name be user["name"] as String
    Display name
```

## Recursive Types

Types can refer to themselves, enabling complex data structures:

```
Type TreeNode[T] is Dictionary with:
    value as T
    left as Optional[TreeNode[T]]
    right as Optional[TreeNode[T]]

# Create a binary tree
Let tree be TreeNode[Integer] with:
    value as 10
    left as TreeNode[Integer] with:
        value as 5
        left as None
        right as None
    right as TreeNode[Integer] with:
        value as 15
        left as None
        right as None
```

## Phantom Types

Phantom types provide type safety without runtime overhead:

```
# Define phantom types for units
Type Length is interface
Type Meters is Length
Type Feet is Length

Process called "meters"[T: Float] that takes value as T returns T as Meters:
    Return value

Process called "feet"[T: Float] that takes value as T returns T as Feet:
    Return value

Process called "add_lengths"[T: Length] that takes a as Float as T and b as Float as T returns Float as T:
    Return a plus b

# These work
Let total_meters be add_lengths with a as meters(5.0) and b as meters(10.0)  # 15.0 meters

# This would fail type checking
# Let mixed be add_lengths with a as meters(5.0) and b as feet(10.0)  # Type error!
```

## Type Classes and Ad Hoc Polymorphism

Type classes enable ad hoc polymorphism:

```
Type Showable is Interface with:
    show as Function[String]

Process called "show_default" that takes value as Any returns String:
    Match type of value:
        When Integer:
            Return value to string
        When String:
            Return value
        When Boolean:
            Return value to string
        When _:
            Return "{object}"
            
Process called "show" that takes value as Showable returns String:
    Return value.show()

Process called "show" that takes value as Any returns String:
    Return show_default with value as value
```

## Type Inference with Pattern Matching

Pattern matching works seamlessly with the type system:

```
Process called "describe_value" that takes value:
    Match value:
        When v of type Integer If v is greater than 0:
            Return "Positive integer:" followed by v to string
        When v of type Integer:
            Return "Non-positive integer:" followed by v to string
        When v of type String:
            Return "String of length" followed by length of v to string
        When v of type Boolean:
            Return "Boolean value:" followed by v to string
        When list containing first and rest:
            Return "List starting with" followed by first to string
        When _:
            Return "Unknown value type"
```

## Real-World Examples

### Type-Safe API Client

```
Type ApiResponse[T] is Dictionary with:
    status as Integer
    data as T
    errors as Optional[List[String]]

Type User is Dictionary with:
    id as String
    name as String
    email as String

Type Product is Dictionary with:
    id as String
    name as String
    price as Float

Async Process called "fetch_user" that takes id as String returns ApiResponse[User]:
    Let response be await http_get with url as "/api/users/" followed by id
    Return response as ApiResponse[User]

Async Process called "fetch_product" that takes id as String returns ApiResponse[Product]:
    Let response be await http_get with url as "/api/products/" followed by id
    Return response as ApiResponse[Product]
```

### State Management with Type Safety

```
Type AppState is Dictionary with:
    user as Optional[User]
    products as List[Product]
    cart as Dictionary[String, Integer]  # Product ID to quantity
    loading as Boolean
    error as Optional[String]

Type Action is
    | Login with user as User
    | Logout
    | AddToCart with product_id as String and quantity as Integer
    | RemoveFromCart with product_id as String
    | SetLoading with loading as Boolean
    | SetError with message as Optional[String]

Process called "reducer" that takes state as AppState and action as Action returns AppState:
    Match action:
        When Login with user as user:
            Return AppState with:
                user as user
                products as state["products"]
                cart as state["cart"]
                loading as false
                error as None
        
        When Logout:
            Return AppState with:
                user as None
                products as state["products"]
                cart as dictionary with  # Empty cart
                loading as false
                error as None
                
        When AddToCart with product_id as id and quantity as qty:
            Let new_cart be copy of state["cart"]
            
            If new_cart contains key id:
                Set new_cart[id] to new_cart[id] plus qty
            Otherwise:
                Set new_cart[id] to qty
                
            Return AppState with:
                user as state["user"]
                products as state["products"]
                cart as new_cart
                loading as state["loading"]
                error as state["error"]
                
        # Other actions...
```

## Type System Best Practices

1. **Start Simple**: Begin with minimal typing and add more as needed
2. **Use Type Inference**: Let Runa infer types when they're obvious
3. **Define Custom Types**: Create your own types for domain concepts
4. **Be Consistent**: Use similar typing approaches throughout your codebase
5. **Document Type Constraints**: Add comments explaining non-obvious type decisions
6. **Favor Composition**: Build complex types from simpler ones
7. **Use Union Types for Error Handling**: Return `Result OR Error` instead of throwing exceptions

## Common Pitfalls

1. **Overtyping**: Adding unnecessary type annotations everywhere
2. **Undertyping**: Not using types in complex functions where they would help
3. **Type Narrowing Issues**: Forgetting to narrow types after checks
4. **Forced Casting**: Overriding the type system with unsafe casts
5. **Ignoring Type Errors**: Working around type errors instead of fixing underlying issues

## Performance Considerations

- Runa's type system is primarily for static checking and has minimal runtime impact
- Most type information is erased at runtime after validation
- Generic types have no performance penalty compared to specific types
- Type assertions may have a small runtime cost

## Conclusion

Runa's enhanced type system provides a powerful yet flexible way to add safety to your code without sacrificing the natural syntax that makes Runa special. By understanding and utilizing these type features, you can create more robust, maintainable, and self-documenting programs.

## See Also

- [Pattern Matching](PatternMatching.md)
- [Functional Programming](FunctionalProgramming.md)
- [Error Handling](ErrorHandling.md) 