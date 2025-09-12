# Runa Type System Reference
*Comprehensive Guide to Runa's Advanced Type System*

**Last Updated**: 2025-08-15  
**Note**: This documentation reflects the current implementation with mathematical symbol enforcement.

## Overview

Runa's type system is designed to provide the safety and expressiveness of modern statically-typed languages while maintaining the natural, human-readable syntax that makes Runa unique. The type system supports gradual typing, powerful inference, generics, algebraic data types, and sophisticated constraint systems.

**Mathematical Symbol Enforcement**: The type system works with the compiler's mathematical symbol enforcement, where mathematical operators (`+`, `-`, `*`, `/`, `%`, `<`, `>`, `<=`, `>=`, `!=`) are restricted to mathematical contexts only. Type checking validates operator usage based on operand types and contexts.

Note: Operator Tokens and Concatenation
The bootstrap lexer/parser provide a dedicated concatenation operator token for strings using the phrase "joined with". Examples:

```runa
Let greeting be "Hello, " joined with user_name
Let path be base joined with "/" joined with filename
```

Use natural language for non-math operations; mathematical symbols are rejected outside numeric contexts.

## Core Principles

### 1. Gradual Typing
Runa allows mixing of typed and untyped code, enabling incremental adoption of typing:

```runa
Note: Untyped - types are inferred
Let user_name be "Alice"
Let age be 30

Note: Partially typed - some annotations for clarity
Let scores (List[Integer]) be list containing 85, 92, 78

Note: Fully typed - complete type annotations
Let calculate_average (Function[List[Integer], Float]) be lambda numbers:
    Return (sum of numbers) divided by (length of numbers)
```

### 2. Powerful Type Inference
The type checker can infer complex types without explicit annotations:

```runa
Note: Inferred as Dictionary[String, List[Integer]]
Let grade_book be dictionary with:
    "Alice" as list containing 85, 92, 78
    "Bob" as list containing 88, 85, 90
    "Charlie" as list containing 92, 88, 95

Note: Inferred as Function[String, Optional[Float]]
Process called "get_average_grade" that takes student_name:
    If grade_book contains key student_name:
        Let grades be grade_book[student_name]
        Return (sum of grades) divided by (length of grades)
    Otherwise:
        Return None
```

### 3. Natural Language Type Syntax
Type expressions follow Runa's natural language philosophy:

```runa
Note: Natural type expressions
Type UserId is Integer
Type UserRecord is Dictionary with name as String and age as Integer
Type Result is Success with data as Any OR Failure with error as String
Type OptionalUser is User OR None
```

## Basic Types

### Primitive Types

```runa
Type Integer                 Note: 64-bit signed integers: -9223372036854775808 to 9223372036854775807
Type Float                   Note: 64-bit IEEE 754 floating point numbers
Type String                  Note: UTF-8 encoded text strings
Type Boolean                 Note: true or false
Type Character               Note: Single Unicode character
Type Byte                    Note: 8-bit unsigned integer (0-255)
```

### Special Types

```runa
Type Any                     Note: Top type - can hold any value
Type Never                   Note: Bottom type - represents impossible values
Type Void                    Note: Unit type for functions that return nothing
Type None                    Note: Null type with single value None
```

### Collection Types

```runa
Type List[T]                 Note: Ordered, mutable collection of T
Type Array[T, N]             Note: Fixed-size array of T with N elements
Type Dictionary[K, V]        Note: Key-value mapping from K to V
Type Set[T]                  Note: Unordered collection of unique T values
Type Tuple[T1, T2, ..., Tn]  Note: Fixed-size ordered collection of specific types
Type Optional[T]             Note: Value of type T or None
```

## Type Declarations

### Variable Type Annotations

```runa
Note: Explicit type annotation
Let user_name (String) be "Alice"
Let user_age (Integer) be 30
Let user_scores (List[Integer]) be list containing 85, 92, 78

Note: Type inference (preferred when obvious)
Let user_name be "Alice"          Note: Inferred as String
Let user_age be 30                Note: Inferred as Integer
Let user_scores be list containing 85, 92, 78  Note: Inferred as List[Integer]
```

### Function Type Annotations

```runa
Note: Full function type annotation
Process called "calculate_grade" 
    that takes scores as List[Integer] and weights as List[Float] 
    returns Float:
    Note: Implementation
    Return weighted_average

Note: Parameter types with inferred return type
Process called "format_name" that takes first as String and last as String:
    Return first joined with " " joined with last  Note: Return type inferred as String

Note: Generic function with type parameters
Process called "find_maximum"[T: Comparable] 
    that takes items as List[T] 
    returns Optional[T]:
    If length of items is equal to 0:
        Return None
    
    Let max_item be items at index 0
    For each item in items:
        If item is greater than max_item:
            Set max_item to item
    Return max_item
```

## Custom Type Definitions

### Type Aliases

Type aliases create new names for existing types:

```runa
Note: Simple aliases for clarity
Type UserId is Integer
Type EmailAddress is String
Type PhoneNumber is String

Note: Complex type aliases
Type UserProfile is Dictionary with:
    id as UserId
    email as EmailAddress
    phone as Optional[PhoneNumber]
    preferences as Dictionary[String, Any]

Note: Function type aliases
Type ValidationFunction[T] is Function[T, Boolean]
Type TransformFunction[T, U] is Function[T, U]
```

### Record Types (Structs/Classes)

Record types define structured data with named fields:

```runa
Note: Basic record type
Type Person is Dictionary with:
    name as String
    age as Integer
    email as String

Note: Record with methods
Type BankAccount is Dictionary with:
    Public account_number as String
    Private balance as Float
    Private pin as String

    Process called "deposit" that takes amount as Float:
        If amount is greater than 0:
            Set self.balance to self.balance plus amount
            Return true
        Otherwise:
            Return false

    Process called "withdraw" that takes amount as Float returns Boolean:
        If amount is greater than 0 and amount is less than or equal to self.balance:
            Set self.balance to self.balance minus amount
            Return true
        Otherwise:
            Return false

    Process called "get_balance" returns Float:
        Return self.balance
```

### Algebraic Data Types (Sum Types/Variants)

ADTs define types that can be one of several distinct variants:

```runa
Note: Basic sum type
Type Shape is:
    | Circle with radius as Float
    | Rectangle with width as Float and height as Float
    | Triangle with base as Float and height as Float

Note: Result type for error handling
Type Result[T, E] is:
    | Success with value as T
    | Failure with error as E

Note: Option type (built-in as Optional[T])
Type Option[T] is:
    | Some with value as T
    | None

Note: Complex state machine
Type ConnectionState is:
    | Disconnected
    | Connecting with progress as Float
    | Connected with session_id as String and start_time as Integer
    | Error with code as Integer and message as String
```

### Enumeration Types

```runa
Note: String-based enums
Type Priority is "low" OR "medium" OR "high" OR "critical"
Type Status is "pending" OR "approved" OR "rejected" OR "cancelled"

Note: Integer-based enums
Type HttpStatus is 200 OR 404 OR 500 OR 503

Note: Complex enums with associated data
Type ApiResponse is:
    | Ok with data as Any and status as Integer
    | ClientError with message as String and code as Integer
    | ServerError with error as String and retry_after as Optional[Integer]
```

## Generic Types

### Generic Type Parameters

```runa
Note: Generic container
Type Container[T] is Dictionary with:
    value as T
    
    Process called "get" returns T:
        Return self.value
    
    Process called "set" that takes new_value as T:
        Set self.value to new_value

Note: Multiple type parameters
Type Pair[A, B] is Dictionary with:
    first as A
    second as B

Note: Generic with constraints
Type Comparable_Container[T: Comparable] is Dictionary with:
    items as List[T]
    
    Process called "find_max" returns Optional[T]:
        Return find_maximum with items as self.items
```

### Type Constraints

Type constraints limit which types can be used as generic parameters:

```runa
Note: Constraint interfaces
Type Comparable is Interface with:
    compare_to as Function[Self, Integer]  Note: Returns -1, 0, or 1

Type Addable is Interface with:
    add as Function[Self, Self]

Type Serializable is Interface with:
    to_json as Function[String]
    from_json as Function[String, Self]

Note: Using constraints
Process called "sort_items"[T: Comparable] that takes items as List[T] returns List[T]:
    Note: Can use comparison operations on T
    Return sorted_version_of items

Process called "sum_values"[T: Addable] that takes values as List[T] returns T:
    Let total be first item in values
    For each value in rest of values:
        Set total to total.add(value)
    Return total
```

### Generic Specialization

```runa
Note: Generic function
Process called "process_data"[T] that takes data as T returns String:
    Return "Processing: " joined with (data to string)

Note: Specialized version for specific type
Process called "process_data" that takes data as List[Integer] returns String:
    Let sum be sum of data
    Return "Processing list with sum: " joined with (sum to string)
```

## Union and Intersection Types

### Union Types (OR Types)

Union types represent values that can be one of several types:

```runa
Note: Basic union
Type StringOrNumber is String OR Integer

Note: Complex union
Type JsonValue is String OR Integer OR Float OR Boolean OR List[JsonValue] OR Dictionary[String, JsonValue] OR None

Note: Function with union parameter
Process called "format_value" that takes value as String OR Integer returns String:
    Match type of value:
        When String:
            Return value
        When Integer:
            Return value to string
```

### Intersection Types (AND Types)

Intersection types combine multiple type requirements:

```runa
Note: Interface intersection
Type Drawable is Interface with:
    draw as Function[None]

Type Movable is Interface with:
    move as Function[Float, Float, None]

Type GameObject is Drawable AND Movable

Note: Implementation must satisfy both interfaces
Type Player is Dictionary with conforms to GameObject:
    x as Float
    y as Float
    sprite as String
    
    Process called "draw":
        Display sprite at position (self.x, self.y)
    
    Process called "move" that takes dx as Float and dy as Float:
        Set self.x to self.x plus dx
        Set self.y to self.y plus dy
```

## Advanced Type Features

### Phantom Types

Phantom types provide compile-time type safety without runtime overhead:

```runa
Note: Define phantom type parameter
Type Length[Unit] is Float

Note: Unit types
Type Meters is Interface
Type Feet is Interface

Note: Constructor functions
Process called "meters" that takes value as Float returns Length[Meters]:
    Return value as Length[Meters]

Process called "feet" that takes value as Float returns Length[Feet]:
    Return value as Length[Feet]

Note: Type-safe operations
Process called "add_lengths"[Unit] 
    that takes a as Length[Unit] and b as Length[Unit] 
    returns Length[Unit]:
    Return (a plus b) as Length[Unit]

Note: Usage - prevents mixing units
Let distance1 be meters(5.0)
Let distance2 be meters(3.0)
Let total be add_lengths with a as distance1 and b as distance2  Note: OK

Note: This would be a compile error:
Note: Let mixed be add_lengths with a as meters(5.0) and b as feet(3.0)  Note: Error!
```

### Higher-Kinded Types

Runa supports higher-kinded types for advanced generic programming:

```runa
Note: Higher-kinded type parameter
Type Functor[F[_]] is Interface with:
    map as Function[F[A], Function[A, B], F[B]] for any A, B

Note: Container types implement Functor
Type List implements Functor[List]:
    Process called "map"[A, B] that takes items as List[A] and transform as Function[A, B] returns List[B]:
        Let result be list containing
        For each item in items:
            Add (transform with value as item) to result
        Return result

Type Optional implements Functor[Optional]:
    Process called "map"[A, B] that takes maybe_value as Optional[A] and transform as Function[A, B] returns Optional[B]:
        Match maybe_value:
            When Some with value as v:
                Return Some with value as (transform with value as v)
            When None:
                Return None
```

### Dependent Types (Limited Support)

Runa provides limited dependent typing for array bounds and constraints:

```runa
Note: Length-indexed arrays
Type Vector[N: Integer] is Array[Float, N]

Process called "dot_product"[N: Integer] 
    that takes a as Vector[N] and b as Vector[N] 
    returns Float:
    Let result be 0.0
    For i from 0 to N minus 1:
        Set result to result plus (a[i] multiplied by b[i])
    Return result

Note: Constraint-based dependent types
Type NonEmptyList[T] is List[T] where length is greater than 0

Process called "head"[T] that takes list as NonEmptyList[T] returns T:
    Return list at index 0  Note: Safe - guaranteed non-empty
```

## Type Inference and Checking

### Type Inference Algorithm

Runa uses a sophisticated type inference algorithm based on Hindley-Milner with extensions:

1. **Local Type Inference**: Variables get types from their initializers
2. **Bidirectional Checking**: Uses expected types to guide inference
3. **Constraint Generation**: Generates type equations from usage
4. **Unification**: Solves type equations to find most general types
5. **Generalization**: Introduces type variables where appropriate

```runa
Note: Step-by-step inference example
Let numbers be list containing 1, 2, 3
Note: 1. Literal 1, 2, 3 have type Integer
Note: 2. list containing T, T, T has type List[T]
Note: 3. Unify Integer with T gives T = Integer
Note: 4. numbers has type List[Integer]

Let doubled be Map over numbers using lambda x: x multiplied by 2
Note: 1. numbers has type List[Integer]
Note: 2. lambda x: x * 2 expects x: Integer, returns Integer
Note: 3. Map expects List[A], Function[A, B], returns List[B]
Note: 4. Unify A = Integer, B = Integer
Note: 5. doubled has type List[Integer]
```

### Type Error Messages

Runa provides detailed, helpful error messages:

```runa
Note: Example code with type error
Let name be "Alice"
Set name to 42  Note: Error!

Note: Error message:
Note: Type Error at line 2, column 5:
Note:   Cannot assign Integer value 42 to String variable 'name'
Note:   Expected: String
Note:   Actual: Integer
Note:   
Note:   Suggestion: Convert the value to string using 'to string'
Note:   Set name to (42 to string)
```

### Pattern Matching and Types

Pattern matching integrates deeply with the type system:

```runa
Type Result[T] is Success with value as T OR Failure with error as String

Process called "handle_result"[T] that takes result as Result[T] returns String:
    Match result:
        When Success with value as v:
            Note: v has type T here
            Return "Success: " joined with (v to string)
        When Failure with error as e:
            Note: e has type String here
            Return "Error: " joined with e
```

### Exhaustiveness Checking

The type checker ensures all cases are handled:

```runa
Type Color is Red OR Green OR Blue

Process called "color_name" that takes color as Color returns String:
    Match color:
        When Red:
            Return "red"
        When Green:
            Return "green"
        Note: Error: Missing case for Blue
```

## Type System Extensions

### Effect Types

Effect types track and control side effects at the type level, enabling precise reasoning about program behavior:

```runa
Note: Effect annotations for side effect tracking
Process called "read_file"[IO] that takes path as String returns String:
    Note: Can perform IO operations
    Let file be open_file with path as path
    Let contents be read_all from file
    close_file with file as file
    Return contents

Process called "pure_calculation"[Pure] that takes x as Integer returns Integer:
    Note: Cannot perform side effects - enforced by type system
    Return x multiplied by 2

Process called "log_message"[IO, Logging] that takes message as String returns None:
    Note: Can perform both IO and logging operations
    write_to_log with message as message
    Return None

Note: Effect composition
Process called "process_data"[IO, Pure] that takes data as List[Integer] returns List[Integer]:
    Note: Can perform IO and pure computations
    Let processed be map over data using pure_calculation
    write_to_file with filename as "output.txt" and content as processed
    Return processed

Note: Effect polymorphism
Process called "safe_operation"[E] that takes operation as Function[String, Integer, E] returns Integer:
    Note: Generic over effects - can work with any effect set
    Return operation with input as "test" and value as 42
```

#### Effect System Features

```runa
Note: Effect inference
Process called "auto_infer_effects" that takes x as Integer returns Integer:
    Let result be x multiplied by 2  Note: Pure effect inferred
    Display "Result:" with message result  Note: IO effect added
    Return result  Note: Final effect: [IO, Pure]

Note: Effect subtyping
Process called "subtype_example"[IO] that takes x as Integer returns Integer:
    Note: IO is a subtype of [IO, Pure], so this is valid
    Return pure_calculation with x as x

Note: Effect constraints
Process called "constrained_operation"[E: Pure] that takes x as Integer returns Integer:
    Note: E must be Pure or a subtype - no side effects allowed
    Return x multiplied by 2

Note: Effect handlers
Handle effects [IO, Logging] in process_data with:
    IO as handle_io_effects
    Logging as handle_logging_effects
    Default as handle_unknown_effects
```

### Refinement Types

Refinement types allow value-level constraints to be expressed in the type system:

```runa
Note: Basic refinement types
Type PositiveInteger is Integer where value is greater than 0
Type NonEmptyString is String where length is greater than 0
Type SortedList[T] is List[T] where is_sorted(value) is true
Type BoundedInteger is Integer where value is greater than or equal to 0 and value is less than or equal to 100

Note: Refinement type usage
Process called "safe_division" that takes numerator as Integer and denominator as PositiveInteger returns Float:
    Return numerator divided by denominator  Note: Type system ensures denominator > 0

Process called "process_non_empty" that takes items as NonEmptyString returns String:
    Return "Processing: " joined with items  Note: Type system ensures items is not empty

Note: Refinement type construction
Let positive_number be 42 as PositiveInteger  Note: Runtime check: 42 > 0
Let empty_string be "" as NonEmptyString     Note: Runtime error: length is 0

Note: Refinement type inference
Process called "create_positive" that takes x as Integer returns PositiveInteger:
    If x is greater than 0:
        Return x as PositiveInteger  Note: Type system knows x > 0 here
    Otherwise:
        Raise "Value must be positive"  Note: Cannot return PositiveInteger

Note: Complex refinements
Type ValidEmail is String where matches_email_pattern(value) is true
Type Age is Integer where value is greater than or equal to 0 and value is less than or equal to 150
Type Password is String where length is greater than or equal to 8 and contains_strong_pattern(value) is true

Note: Refinement type composition
Type ValidUser is Record with:
    name as NonEmptyString
    email as ValidEmail
    age as Age
    password as Password
```

#### Refinement Type System

```runa
Note: Refinement type subtyping
Type VeryPositiveInteger is PositiveInteger where value is greater than 10
Note: VeryPositiveInteger is a subtype of PositiveInteger

Note: Refinement type intersection
Type SmallPositiveInteger is PositiveInteger AND Integer where value is less than 100

Note: Refinement type union
Type ValidInput is PositiveInteger OR NonEmptyString

Note: Refinement type parameters
Type BoundedList[T, N] is List[T] where length equals N
Type Matrix[Rows, Cols] is List[List[Float]] where length equals Rows and all items satisfy length equals Cols

Note: Refinement type functions
Process called "validate_age" that takes age as Integer returns Age:
    If age is greater than or equal to 0 and age is less than or equal to 150:
        Return age as Age
    Otherwise:
        Raise "Invalid age: " joined with (age to string)

Process called "validate_email" that takes email as String returns ValidEmail:
    If matches_email_pattern with input as email:
        Return email as ValidEmail
    Otherwise:
        Raise "Invalid email format"
```

### Linear Types

Linear types ensure resources are used exactly once, preventing resource leaks and enabling precise resource management:

```runa
Note: Linear resource types
Type FileHandle[Linear] is resource
Type DatabaseConnection[Linear] is resource
Type Lock[Linear] is resource
Type MemoryBuffer[Linear] is resource

Note: Linear type usage
Process called "read_file_linear" that takes handle as FileHandle[Linear] returns String:
    Let contents be read_all from handle
    close_file with handle as handle  Note: handle is consumed here
    Return contents

Note: Linear type error (would not compile)
Process called "bad_usage" that takes handle as FileHandle[Linear] returns String:
    Let contents be read_all from handle
    Return contents  Note: Error: handle not consumed

Note: Linear type composition
Process called "process_file" that takes handle as FileHandle[Linear] returns String:
    Let contents be read_all from handle
    close_file with handle as handle  Note: Consume handle
    Return process_contents with input as contents

Note: Linear type borrowing
Process called "borrow_handle" that takes handle as FileHandle[Linear] returns String:
    Let contents be read_all from handle
    Return contents  Note: handle is borrowed, not consumed

Note: Linear type with effects
Process called "linear_io" that takes handle as FileHandle[Linear] returns String[IO, Linear]:
    Let contents be read_all from handle
    close_file with handle as handle
    Return contents
```

#### Linear Type System Features

```runa
Note: Linear type inference
Process called "auto_linear" that takes handle as FileHandle[Linear] returns String:
    Let contents be read_all from handle
    close_file with handle as handle  Note: Linear type automatically inferred
    Return contents

Note: Linear type polymorphism
Process called "linear_map"[T, U] that takes resource as T[Linear] and func as Function[T, U] returns U:
    Let result be func with input as resource
    consume with resource as resource  Note: Generic consumption
    Return result

Note: Linear type constraints
Process called "linear_constraint"[T: Linear] that takes resource as T returns None:
    consume with resource as resource  Note: T must be linear
    Return None

Note: Linear type with refinement
Type SafeFileHandle[Linear] is FileHandle[Linear] where is_open(value) is true
```

### Dependent Types (Advanced)

Dependent types allow types to depend on values, enabling precise specifications:

```runa
Note: Dependent type examples
Type Vector[N: Integer] is List[Float] where length equals N
Type Matrix[Rows: Integer, Cols: Integer] is List[Vector[Cols]] where length equals Rows

Note: Dependent type usage
Process called "vector_add" that takes v1 as Vector[N] and v2 as Vector[N] returns Vector[N]:
    Note: Type system ensures vectors have same length
    Return zip_with with list1 as v1 and list2 as v2 using add

Process called "matrix_multiply" that takes m1 as Matrix[M, N] and m2 as Matrix[N, P] returns Matrix[M, P]:
    Note: Type system ensures matrix dimensions are compatible
    Return matrix_multiply_impl with matrix1 as m1 and matrix2 as m2

Note: Dependent type construction
Let vec3 be list containing 1.0, 2.0, 3.0 as Vector[3]
Let mat2x3 be list containing vec3, vec3 as Matrix[2, 3]

Note: Dependent type inference
Process called "create_vector" that takes n as Integer returns Vector[n]:
    Let elements be generate_list with size as n using random_float
    Return elements as Vector[n]
```

## Best Practices

### 1. Type Annotation Guidelines

```runa
Note: Good: Annotate public interfaces
Export Process called "calculate_tax" 
    that takes income as Float and rate as Float 
    returns Float:
    Return income multiplied by rate

Note: Good: Let inference work for local variables
Process called "process_order" that takes order as Order:
    Let total be calculate_total with order as order  Note: Type inferred
    Let tax be calculate_tax with income as total and rate as 0.08  Note: Type inferred
    Return total plus tax

Note: Avoid: Over-annotation of obvious types
Let name (String) be "Alice"  Note: Type annotation unnecessary
Let count (Integer) be 0      Note: Type annotation unnecessary
```

### 2. Generic Type Design

```runa
Note: Good: Use meaningful type parameter names
Type Repository[Entity, Key] is Interface with:
    find_by_id as Function[Key, Optional[Entity]]
    save as Function[Entity, None]
    delete as Function[Key, Boolean]

Note: Good: Use constraints when needed
Process called "merge_sorted_lists"[T: Comparable] 
    that takes list1 as List[T] and list2 as List[T] 
    returns List[T]:
    Note: Implementation can use comparison on T
```

### 3. Error Handling with Types

```runa
Note: Good: Use Result types for recoverable errors
Type ParseResult[T] is Success with value as T OR ParseError with message as String

Process called "parse_json"[T] that takes json_string as String returns ParseResult[T]:
    Try:
        Let parsed be parse_json_string with input as json_string
        Return Success with value as parsed
    Catch parse_error:
        Return ParseError with message as parse_error.message

Note: Good: Use Optional for nullable values
Process called "find_user" that takes id as UserId returns Optional[User]:
    Note: Returns Some(user) if found, None if not found
```

### 4. Type Safety Patterns

```runa
Note: Good: Use newtype pattern for domain types
Type UserId is Integer
Type ProductId is Integer
Note: Prevents mixing different ID types

Note: Good: Use enums for finite state
Type OrderStatus is "pending" OR "processing" OR "shipped" OR "delivered" OR "cancelled"

Note: Good: Use ADTs for complex data
Type Payment is:
    | CreditCard with number as String and expiry as String
    | PayPal with email as String
    | BankTransfer with account as String and routing as String
```

## Type System Performance

### Compilation Performance

- **Incremental Checking**: Only re-check modified modules
- **Parallel Checking**: Type check independent modules in parallel
- **Caching**: Cache type information between compilations
- **Lazy Evaluation**: Defer expensive type computations when possible

### Runtime Performance

- **Type Erasure**: Most type information is erased at runtime
- **Monomorphization**: Generic functions are specialized for concrete types
- **Inline Optimization**: Type information enables aggressive inlining
- **Dead Code Elimination**: Unused type variants are eliminated

## Conclusion

Runa's type system provides a powerful foundation for safe, expressive programming while maintaining the language's natural syntax philosophy. The combination of gradual typing, sophisticated inference, and advanced features like ADTs and generics makes it suitable for both rapid prototyping and large-scale software development.

The type system serves as a bridge between human reasoning about program correctness and machine verification, enabling developers to express their intent clearly while receiving automated assistance in maintaining program invariants.