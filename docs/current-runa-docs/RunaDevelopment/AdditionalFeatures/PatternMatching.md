# Pattern Matching in Runa

Pattern matching is a powerful feature in Runa that allows you to destructure data and branch based on its shape and content. This guide covers all aspects of pattern matching in Runa, from basic usage to advanced techniques.

## Introduction to Pattern Matching

Pattern matching provides an elegant way to:
- Extract values from complex data structures
- Branch code based on data shapes
- Handle different cases in a concise manner
- Make code more readable and maintainable

## Basic Pattern Matching Syntax

The basic syntax for pattern matching in Runa uses the `Match` and `When` keywords:

```
Match expression:
    When pattern1:
        # Code to execute if expression matches pattern1
    When pattern2:
        # Code to execute if expression matches pattern2
    When _:
        # Default case (wildcard pattern)
```

## Simple Value Matching

Match against literal values:

```
Let status_code be 404

Match status_code:
    When 200:
        Display "OK"
    When 404:
        Display "Not Found"
    When 500:
        Display "Server Error"
    When _:
        Display "Unknown Status Code:" with message status_code
```

## Destructuring Lists

Extract values from lists:

```
Let point be list containing 10, 20

Match point:
    When list containing x and y:
        Display "X coordinate:" with message x
        Display "Y coordinate:" with message y
    When list containing x:
        Display "One-dimensional point at:" with message x
    When _:
        Display "Not a valid point"
```

You can also match against specific values while extracting others:

```
Let data be list containing "temperature", 25, "Celsius"

Match data:
    When list containing "temperature" and value and unit:
        Display "Temperature is" with message value with message "degrees" with message unit
    When list containing "pressure" and value and unit:
        Display "Pressure is" with message value with message unit
    When _:
        Display "Unknown data format"
```

## Destructuring Dictionaries

Extract values from dictionaries:

```
Let user be dictionary with:
    "name" as "Alice"
    "role" as "admin"
    "age" as 32

Match user:
    When dictionary with "name" as name and "role" as "admin":
        Display "Administrator:" with message name
    When dictionary with "name" as name and "role" as "user":
        Display "Regular user:" with message name
    When dictionary with "name" as name:
        Display "Unknown role for user:" with message name
    When _:
        Display "Invalid user data"
```

## Nested Pattern Matching

You can match against nested structures:

```
Let employee be dictionary with:
    "name" as "Bob"
    "position" as "Developer"
    "address" as dictionary with:
        "city" as "Seattle"
        "state" as "WA"

Match employee:
    When dictionary with "name" as name and "address" as dictionary with "city" as "Seattle":
        Display "Seattle-based employee:" with message name
    When dictionary with "name" as name and "address" as dictionary with "city" as city:
        Display "Employee from" with message city with message ":" with message name
    When _:
        Display "Employee with incomplete data"
```

## Pattern Guards

You can add conditions to patterns using `If` clauses:

```
Let score be 85

Match score:
    When value If value is greater than or equal to 90:
        Display "Grade: A"
    When value If value is greater than or equal to 80:
        Display "Grade: B"
    When value If value is greater than or equal to 70:
        Display "Grade: C"
    When value If value is greater than or equal to 60:
        Display "Grade: D"
    When _:
        Display "Grade: F"
```

## Type Patterns

When used with Runa's enhanced type system, you can match against types:

```
Let data be "Hello, world!"

Match data:
    When value of type String:
        Display "Text:" with message value
    When value of type Integer:
        Display "Number:" with message value
    When value of type List:
        Display "List with" with message length of value with message "items"
    When _:
        Display "Unknown data type"
```

## Binding Multiple Variables

You can bind multiple variables in a pattern:

```
Let rectangle be dictionary with:
    "width" as 10
    "height" as 20

Match rectangle:
    When dictionary with "width" as w and "height" as h If w is equal to h:
        Display "Square with side" with message w
    When dictionary with "width" as w and "height" as h:
        Display "Rectangle" with message w with message "x" with message h
    When _:
        Display "Not a rectangle"
```

## Pattern Matching with OR Patterns

You can use the `OR` keyword to match multiple patterns:

```
Let day be "Saturday"

Match day:
    When "Saturday" OR "Sunday":
        Display "Weekend"
    When "Monday" OR "Tuesday" OR "Wednesday" OR "Thursday" OR "Friday":
        Display "Weekday"
    When _:
        Display "Invalid day"
```

## Advanced Pattern Matching Techniques

### Range Patterns

Match against ranges of values:

```
Let temperature be 22

Match temperature:
    When value If value is greater than or equal to 30:
        Display "Hot"
    When value If value is greater than or equal to 20 and value is less than 30:
        Display "Warm"
    When value If value is greater than or equal to 10 and value is less than 20:
        Display "Cool"
    When value If value is less than 10:
        Display "Cold"
```

### Record Patterns

Match against structured records:

```
Type Person is Dictionary with:
    name as String
    age as Integer

Let alice be dictionary with:
    "name" as "Alice"
    "age" as 30

Match alice:
    When Person with name as n and age as a If a is greater than 18:
        Display n with message "is an adult"
    When Person with name as n:
        Display n with message "is a minor"
    When _:
        Display "Not a valid person"
```

### List Pattern Variations

Match against list patterns with varying lengths:

```
Let numbers be list containing 1, 2, 3, 4, 5

Match numbers:
    When list containing first and second and rest:
        Display "First two elements:" with message first with message "and" with message second
        Display "Remaining elements:" with message rest
    When list containing first and rest:
        Display "First element:" with message first
        Display "Remaining elements:" with message rest
    When empty list:
        Display "Empty list"
```

## Pattern Matching with Functions

You can use pattern matching in function parameters:

```
Process called "process_data" that takes data:
    Match data:
        When list containing "user" and user_id:
            Return get_user_info with id as user_id
        When list containing "product" and product_id:
            Return get_product_info with id as product_id
        When _:
            Return "Invalid data format"
```

## Real-World Examples

### State Machine Implementation

```
Process called "process_event" that takes state and event:
    Match list containing state and event:
        When list containing "idle" and "start":
            Return "running"
        When list containing "running" and "pause":
            Return "paused"
        When list containing "paused" and "resume":
            Return "running"
        When list containing "running" and "complete":
            Return "completed"
        When list containing any_state and "reset":
            Return "idle"
        When _:
            Return state  # Unchanged
```

### JSON Processing

```
Process called "extract_important_data" that takes json_data:
    Match json_data:
        When dictionary with "user" as dictionary with "name" as name and "email" as email:
            Return dictionary with:
                "name" as name
                "contact" as email
        
        When dictionary with "company" as dictionary with "name" as company_name and "employees" as employees:
            Return dictionary with:
                "organization" as company_name
                "team_size" as length of employees
        
        When dictionary with "error" as message:
            Display "API Error:" with message message
            Return None
            
        When _:
            Display "Unexpected response format"
            Return None
```