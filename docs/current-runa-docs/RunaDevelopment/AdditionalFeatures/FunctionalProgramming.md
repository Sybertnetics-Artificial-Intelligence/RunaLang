# Functional Programming in Runa

Runa incorporates powerful functional programming features that enable concise, expressive, and composable code. This guide covers the functional programming capabilities of Runa and how to effectively use them in your programs.

## Introduction to Functional Programming in Runa

Functional programming in Runa emphasizes:
- Immutable data
- First-class functions
- Higher-order functions
- Function composition
- Pure functions
- Declarative style

These features help create code that is easier to reason about, test, and maintain.

## Lambda Expressions

Lambda expressions allow you to create anonymous functions inline:

```
# Basic lambda expression
Let double be Lambda x: x multiplied by 2

# Using the lambda
Let result be double with x as 5  # Result is 10
```

Lambda expressions can take multiple parameters:

```
Let add be Lambda a and b: a plus b
Let sum be add with a as 3 and b as 4  # Sum is 7
```

They can also capture variables from the surrounding scope:

```
Let factor be 3
Let multiply_by_factor be Lambda x: x multiplied by factor

Let result be multiply_by_factor with x as 7  # Result is 21
```

## Higher-Order Functions

Higher-order functions take functions as arguments or return functions as results.

### Map

The `Map` function applies a function to each element in a collection:

```
Let numbers be list containing 1, 2, 3, 4, 5
Let double be Lambda x: x multiplied by 2

Let doubled_numbers be Map over numbers using double
# doubled_numbers is [2, 4, 6, 8, 10]
```

### Filter

The `Filter` function selects elements from a collection based on a predicate:

```
Let numbers be list containing 1, 2, 3, 4, 5, 6
Let is_even be Lambda x: x modulo 2 is equal to 0

Let even_numbers be Filter over numbers using is_even
# even_numbers is [2, 4, 6]
```

### Reduce

The `Reduce` function combines elements of a collection into a single value:

```
Let numbers be list containing 1, 2, 3, 4, 5
Let add be Lambda a and b: a plus b

Let sum be Reduce over numbers using add with initial 0
# sum is 15
```

### All Three Together

These higher-order functions can be combined for powerful data transformations:

```
Let products be list containing
    dictionary with: "name" as "Apple", "price" as 1.20, "in_stock" as true
    dictionary with: "name" as "Banana", "price" as 0.50, "in_stock" as true
    dictionary with: "name" as "Cherry", "price" as 3.00, "in_stock" as false
    dictionary with: "name" as "Date", "price" as 2.50, "in_stock" as true

# Get names of in-stock products with price over $1
Let in_stock_filter be Lambda product: product["in_stock"] is equal to true
Let expensive_filter be Lambda product: product["price"] is greater than 1.0
Let get_name be Lambda product: product["name"]

Let available_expensive_products be Map over
    Filter over
        Filter over products using in_stock_filter
    using expensive_filter
using get_name

# available_expensive_products is ["Apple", "Date"]
```

## The Pipeline Operator

Runa provides the pipeline operator `|>` to make function composition more readable:

```
Let numbers be list containing 1, 2, 3, 4, 5, 6

Let result be numbers
    |> Filter using Lambda x: x modulo 2 is equal to 0
    |> Map using Lambda x: x multiplied by 3
    |> Reduce using Lambda a and b: a plus b with initial 0

# Result is 36 (sum of [6, 12, 18])
```

## Function Composition

Runa allows combining functions to create new functions:

```
Let add_one be Lambda x: x plus 1
Let multiply_by_two be Lambda x: x multiplied by 2

# Compose functions (applies from right to left)
Let add_then_multiply be compose multiply_by_two with add_one

Let result be add_then_multiply with x as 5
# Result is 12: (5 + 1) * 2
```

The `pipe` function composes functions in left-to-right order:

```
Let add_one be Lambda x: x plus 1
Let multiply_by_two be Lambda x: x multiplied by 2

# Pipe functions (applies from left to right)
Let multiply_then_add be pipe add_one with multiply_by_two

Let result be multiply_then_add with x as 5
# Result is 11: (5 * 2) + 1
```

## Partial Application

Partial application allows you to fix some arguments of a function, returning a new function:

```
Process called "greet" that takes greeting and name:
    Return greeting followed by ", " followed by name followed by "!"

# Partially apply the greeting
Let greet_with_hello be partial greet with greeting as "Hello"

# Use the partially applied function
Let message be greet_with_hello with name as "Alice"
# message is "Hello, Alice!"
```

## Currying

Currying transforms a function that takes multiple arguments into a sequence of functions that each take a single argument:

```
# Define a function that takes three arguments
Process called "calculate_volume" that takes length and width and height:
    Return length multiplied by width multiplied by height

# Curry the function
Let curried_volume be curry calculate_volume

# Call the curried function
Let length_5 be curried_volume with length as 5
Let length_5_width_10 be length_5 with width as 10
Let volume be length_5_width_10 with height as 3
# volume is 150
```

## Immutable Data Structures

Runa encourages the use of immutable data structures:

```
# Create an immutable list
Let numbers be immutable list containing 1, 2, 3, 4, 5

# Operations on immutable lists return new lists
Let with_added be numbers with 6 added      # Returns a new list [1, 2, 3, 4, 5, 6]
Let with_removed be numbers without 3       # Returns a new list [1, 2, 4, 5]
Let with_replaced be numbers with 2 replaced by 20  # Returns a new list [1, 20, 3, 4, 5]

# Original list remains unchanged
Display numbers  # Still [1, 2, 3, 4, 5]
```

## Pure Functions

Pure functions are a cornerstone of functional programming:

```
# Pure function - no side effects, same output for same input
Process called "add_pure" that takes a and b:
    Return a plus b

# Impure function - has side effects
Let counter be 0
Process called "increment_counter" that takes amount:
    Set counter to counter plus amount
    Return counter
```

## Recursion

Functional programming often uses recursion instead of loops:

```
# Calculate factorial using recursion
Process called "factorial" that takes n:
    If n is less than or equal to 1:
        Return 1
    Otherwise:
        Return n multiplied by factorial with n as n minus 1
        
Let result be factorial with n as 5  # Result is 120
```

Runa optimizes tail-recursive functions to prevent stack overflow:

```
# Tail-recursive factorial
Process called "factorial_tail" that takes n and accumulator:
    If n is less than or equal to 1:
        Return accumulator
    Otherwise:
        Return factorial_tail with n as n minus 1 and accumulator as n multiplied by accumulator

Let result be factorial_tail with n as 5 and accumulator as 1  # Result is 120
```

## Memoization

Runa provides built-in support for memoization to cache function results:

```
# Memoized Fibonacci function
Memoized Process called "fibonacci" that takes n:
    If n is less than or equal to 1:
        Return n
    Otherwise:
        Return fibonacci with n as n minus 1 plus fibonacci with n as n minus 2

# Now even large Fibonacci values compute quickly
Let result be fibonacci with n as 50
```

## Lazy Evaluation

Runa supports lazy evaluation for improved performance with large data sets:

```
# Create a lazy sequence from 1 to 1000000
Let numbers be lazy range from 1 to 1000000

# Operations on lazy sequences are only computed when needed
Let evens be numbers |> Filter using Lambda x: x modulo 2 is equal to 0
Let first_10_evens be evens |> take with count as 10

# first_10_evens is [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
# The full sequence is never generated
```

## Combining with Pattern Matching

Functional programming works well with pattern matching:

```
# Define a recursive function with pattern matching
Process called "sum_list" that takes list:
    Match list:
        When empty list:
            Return 0
        When list containing first and rest:
            Return first plus sum_list with list as rest
            
Let total be sum_list with list as list containing 1, 2, 3, 4, 5  # Result is 15
```

## Closures

Runa supports closures, allowing functions to capture their surrounding state:

```
Process called "create_counter" that takes initial_value:
    Let count be initial_value
    
    Return Process called "counter" that takes action:
        Match action:
            When "increment":
                Set count to count plus 1
                Return count
            When "decrement":
                Set count to count minus 1
                Return count
            When "get":
                Return count
            When _:
                Return "Unknown action"
                
Let my_counter be create_counter with initial_value as 0
Let value1 be my_counter with action as "increment"  # Returns 1
Let value2 be my_counter with action as "increment"  # Returns 2
Let value3 be my_counter with action as "get"        # Returns 2
```

## Real-World Examples

### Data Processing Pipeline

```
# Process a list of customer records
Let customers be get_customer_data()

Let premium_emails be customers
    |> Filter using Lambda c: c["subscription_level"] is equal to "premium" 
    |> Map using Lambda c: c["email"]
    |> Filter using Lambda email: email contains "@"
    
# Now send marketing emails to premium customers
For each email in premium_emails:
    send_marketing_email with recipient as email and template as "premium_offer"
```

### Functional Error Handling

```
# Define Result type for functional error handling
Type Result is Dictionary with:
    success as Boolean
    value as Any
    error as Any

# Functions return Result objects instead of throwing exceptions
Process called "divide" that takes a and b:
    If b is equal to 0:
        Return Result with:
            success as false
            value as None
            error as "Division by zero"
    Otherwise:
        Return Result with:
            success as true
            value as a divided by b
            error as None
            
# Map over Results
Process called "map_result" that takes result and function:
    If result["success"] is equal to true:
        Let new_value be function with value as result["value"]
        Return Result with:
            success as true
            value as new_value
            error as None
    Otherwise:
        Return result
        
# Chain Results
Process called "and_then" that takes result and function:
    If result["success"] is equal to true:
        Return function with value as result["value"]
    Otherwise:
        Return result
        
# Usage example
Let result be divide with a as 10 and b as 2
    |> and_then using Lambda value: divide with a as value and b as 2
    |> map_result using Lambda value: value multiplied by 10

If result["success"] is equal to true:
    Display "Result:" with message result["value"]
Otherwise:
    Display "Error:" with message result["error"]
```

### Functional State Management

```
# Immutable state updates
Type AppState is Dictionary with:
    user as Dictionary
    items as List
    settings as Dictionary

Process called "update_state" that takes state and action:
    Match action["type"]:
        When "ADD_ITEM":
            Return AppState with:
                user as state["user"]
                items as state["items"] with action["item"] added
                settings as state["settings"]
                
        When "REMOVE_ITEM":
            Return AppState with:
                user as state["user"]
                items as state["items"] without action["item"]
                settings as state["settings"]
                
        When "UPDATE_USER":
            Return AppState with:
                user as action["user"]
                items as state["items"]
                settings as state["settings"]
                
        When "TOGGLE_SETTING":
            Let updated_settings be state["settings"] with 
                action["key"] updated to not state["settings"][action["key"]]
                
            Return AppState with:
                user as state["user"]
                items as state["items"]
                settings as updated_settings
                
        When _:
            Return state
```

## Advanced Functional Concepts

### Functors, Applicatives, and Monads

For advanced functional programming, Runa supports these higher abstractions:

```
# Maybe monad
Type Maybe is Dictionary with:
    has_value as Boolean
    value as Any

Process called "just" that takes value:
    Return Maybe with:
        has_value as true
        value as value
        
Process called "nothing" that takes:
    Return Maybe with:
        has_value as false
        value as None
        
# Functor map operation
Process called "map_maybe" that takes maybe and function:
    If maybe["has_value"] is equal to true:
        Return just with value as function with value as maybe["value"]
    Otherwise:
        Return nothing with
        
# Monad bind operation
Process called "bind_maybe" that takes maybe and function:
    If maybe["has_value"] is equal to true:
        Return function with value as maybe["value"]
    Otherwise:
        Return nothing with
        
# Usage example
Process called "get_user_setting" that takes user_id and setting_name:
    Let user be find_user with id as user_id
    
    Return just with value as user
        |> bind_maybe using Lambda user: 
            If user["settings"] contains key setting_name:
                Return just with value as user["settings"][setting_name]
            Otherwise:
                Return nothing with
```

## Best Practices

1. **Prefer Immutability**: Use immutable data structures whenever possible
2. **Use Pure Functions**: Minimize side effects for easier testing and reasoning
3. **Compose Small Functions**: Build complex behavior from simple, reusable functions
4. **Consider Readability**: Use pipelines and composition for more readable code
5. **Handle Errors Functionally**: Use Result or Maybe types instead of exceptions

## Performance Considerations

- Immutable data structures may have performance overhead for large data sets
- Lazy evaluation can significantly improve performance for large computations
- Memoization helps with expensive recursive computations
- Tail recursion optimization prevents stack overflow in recursive functions

## Conclusion

Functional programming in Runa provides a powerful paradigm for building reliable, maintainable, and expressive code. By utilizing features like lambda expressions, higher-order functions, immutable data, and function composition, you can create elegant solutions to complex problems with less code and fewer bugs.

## See Also

- [Pattern Matching](PatternMatching.md)
- [Asynchronous Programming](AsyncProgramming.md)
- [Enhanced Type System](TypeSystem.md) 