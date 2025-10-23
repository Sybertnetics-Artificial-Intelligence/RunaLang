# Code Style Guide

This guide describes the recommended coding style for Runa programming language. Following these conventions makes your code more readable and maintainable.

## General Principles

1. **Clarity over cleverness** - Write code that's easy to understand
2. **Consistency** - Follow the same patterns throughout your codebase
3. **Natural language** - Prefer Canon mode for maximum readability
4. **Descriptive names** - Use meaningful identifiers that explain intent

## Syntax Mode

### Recommended: Canon Mode

Use **Canon Mode** (natural language) for all public code, libraries, and documentation:

```runa
# Recommended - Canon Mode
Let total price be base price multiplied by quantity
If total price is greater than 100:
    Display "Large order!"
```

### Developer Mode for Teams

If your team prefers symbolic operators, use **Developer Mode** consistently:

```runa
# Developer Mode - Also acceptable
Let total price be base price * quantity
If total price > 100:
    Display "Large order!"
```

### Never Mix Modes

**Don't do this:**
```runa
# WRONG - Mixed operators
Let result be x * y plus z
```

## Naming Conventions

### Identifiers

Use **spaced identifiers** (canonical form):

```runa
# Good - Spaced identifiers
Let user name be "Alice"
Let account balance be 1000
Let is active be true

# Avoid - camelCase/PascalCase (non-canonical)
Let userName be "Alice"
Let accountBalance be 1000
Let isActive be true
```

### Capitalization

Follow these capitalization rules:

```runa
# Variables and functions - lowercase
Let total count be 0
Process called "calculate total" that takes items:
    ...

# Types - PascalCase (each word capitalized)
Type called User:
    name as String
    age as Integer

# Constants - SCREAMING_SNAKE_CASE
Let MAX_RETRIES be 3
Let DEFAULT_TIMEOUT be 30
```

### Equivalence Rules

Remember that spaces and underscores are equivalent:

```runa
# These are THE SAME:
Let Calculate Total be 10
Let Calculate_Total be 10

# These are THE SAME:
Let user count be 5
Let user_count be 5

# These are DIFFERENT (case matters per word):
Let User Count be 10  # Different from user count
Let user Count be 20  # Different from both above
```

### Descriptive Names

Use descriptive names that explain purpose:

```runa
# Good - Clear intent
Let active user count be 0
Let monthly revenue total be 0
Process called "calculate shipping cost" that takes order:
    ...

# Bad - Unclear abbreviations
Let auc be 0
Let mrt be 0
Process called "calc_sc" that takes o:
    ...
```

### Avoid Single Letters

Except for loop counters, avoid single-letter names:

```runa
# Acceptable - Loop counter
For i in range from 0 to 10:
    Display i as text

# Bad - Unclear purpose
Let x be get data
Let y be process with x
Let z be y plus 10
```

## Indentation and Whitespace

### Indentation

Use **4 spaces** per indentation level (no tabs):

```runa
Process called "example":
    Let x be 10

    If x is greater than 5:
        Display "Greater"

        If x is greater than 8:
            Display "Much greater"
```

### Blank Lines

- One blank line between function definitions
- One blank line between logical sections within functions
- No blank line at the start or end of blocks

```runa
Process called "first function":
    Let x be 10
    Return x

Process called "second function":
    Let y be 20

    If y is greater than 10:
        Display "Large"

    Return y
```

### Line Length

Keep lines under **100 characters** when possible:

```runa
# Good - Readable length
Let message be "Hello, " joined with user name followed by "!"

# Too long - Break into multiple lines
Let very long message be "This is a very long string that exceeds the recommended line length and should be broken up"

# Better - Split across lines
Let very long message be "This is a very long string that " joined with
    "exceeds the recommended line length " joined with
    "and should be broken up"
```

## Comments and Documentation

### Single-Line Comments

Use `Note:` for single-line comments:

```runa
Note: Calculate the total price including tax
Let total be subtotal multiplied by 1.08
```

### Multi-Line Comments

Use multiple `Note:` lines for longer explanations:

```runa
Note: This function calculates shipping costs based on:
Note: - Order weight and destination
Note: - Current shipping rates
Note: - Any applicable discounts
Process called "calculate shipping" that takes order and destination:
    ...
```

### Documentation Comments

Document all public functions, types, and modules:

```runa
Note: Process called "validate email"
Note: Checks if the provided string is a valid email address
Note:
Note: Parameters:
Note:   email - The email address to validate
Note:
Note: Returns:
Note:   True if valid, False otherwise
Process called "validate email" that takes email:
    Note: Implementation here
    ...
```

### Inline Comments

Place inline comments on their own line above the code:

```runa
# Good
Note: Convert to uppercase for comparison
Let normalized be to uppercase with user input

# Avoid - Inline comments at end of line
Let normalized be to uppercase with user input  Note: Convert to uppercase
```

## Code Organization

### File Structure

Organize files in this order:

1. File-level documentation
2. Imports
3. Constants
4. Type definitions
5. Functions/Processes
6. Main code

```runa
Note: user_manager.runa
Note: Manages user accounts and authentication

Import "string_utils" as strings
Import "database" as db

Let MAX_USERNAME_LENGTH be 50
Let MIN_PASSWORD_LENGTH be 8

Type called User:
    id as Integer
    username as String
    email as String

Process called "create user" that takes username and email:
    ...

Process called "validate username" that takes username:
    ...
```

### Group Related Code

Group related functions together:

```runa
Note: === User Creation Functions ===

Process called "create user" that takes username and email:
    ...

Process called "validate new user" that takes username and email:
    ...

Note: === User Authentication Functions ===

Process called "authenticate user" that takes username and password:
    ...

Process called "hash password" that takes password:
    ...
```

## Control Flow

### If Statements

```runa
# Good - Clear structure
If condition:
    Do something

If condition:
    Do something
Otherwise:
    Do something else

# Multiple conditions
If first condition:
    Do first thing
Otherwise if second condition:
    Do second thing
Otherwise:
    Do default thing
```

### When Statements

Use `When` for value-based conditions:

```runa
When user role:
    Is "admin":
        Grant admin access
    Is "moderator":
        Grant moderator access
    Is "user":
        Grant basic access
    Otherwise:
        Deny access
```

### Loops

```runa
# For loop
For i in range from 0 to 10:
    Display i as text

# For each loop
For each item in items:
    Process item

# While loop
While condition is true:
    Do something
```

## Functions (Processes)

### Function Definitions

```runa
# Simple function
Process called "add" that takes x and y:
    Return x plus y

# Function with explicit types
Process called "calculate area" that takes width as Float and height as Float returns Float:
    Return width multiplied by height

# Function with multiple return values
Process called "get coordinates" returns tuple of Float and Float:
    Return pair of 10.5 and 20.3
```

### Function Calls

```runa
# Simple call
Let result be add with 5 and 3

# Named parameters (when available)
Let area be calculate area with width as 10 and height as 5

# Chaining (if applicable)
Let result be process data with input
    then transform
    then validate
```

## Types and Structures

### Type Definitions

```runa
# Simple type
Type called Point:
    x as Float
    y as Float

# Type with methods
Type called Rectangle:
    width as Float
    height as Float

    Method called "area" returns Float:
        Return width multiplied by height

    Method called "perimeter" returns Float:
        Return 2 multiplied by (width plus height)
```

### Type Instantiation

```runa
# Create instance
Let point be Point with:
    x as 10.0
    y as 20.0

# Access fields
Let x coordinate be point.x
Let y coordinate be point.y
```

## Collections

### Lists

```runa
# Create list
Let numbers be list containing 1, 2, 3, 4, 5

# Access elements
Let first be numbers at 0

# Iterate
For each number in numbers:
    Display number as text
```

### Maps

```runa
# Create map
Let user data be map with:
    "name" as "Alice"
    "age" as 30
    "email" as "alice@example.com"

# Access values
Let user name be user data at "name"
```

## Error Handling

### Try-Catch

```runa
Try:
    Let result be risky operation
    Display result
Catch error:
    Display "Error occurred: " joined with error message
Finally:
    Cleanup resources
```

### Result Types (when available)

```runa
Process called "divide" that takes x and y returns Result of Float:
    If y is equal to 0:
        Return error with "Division by zero"

    Return success with x divided by y
```

## Imports and Modules

### Import Statements

```runa
# Simple import
Import "standard_library.math" as math

# Selective import (when available)
Import from "collections" select List, Map, Set

# Relative imports
Import "../utils/string_utils" as strings
```

### Module Organization

Keep modules focused on a single responsibility:

```
myproject/
├── main.runa
├── models/
│   ├── user.runa
│   └── product.runa
├── services/
│   ├── auth.runa
│   └── database.runa
└── utils/
    ├── string_utils.runa
    └── validation.runa
```

## Best Practices

### DRY (Don't Repeat Yourself)

Extract repeated code into functions:

```runa
# Bad - Repetition
Let total 1 be price 1 multiplied by quantity 1 multiplied by 1.08
Let total 2 be price 2 multiplied by quantity 2 multiplied by 1.08
Let total 3 be price 3 multiplied by quantity 3 multiplied by 1.08

# Good - Reusable function
Process called "calculate total with tax" that takes price and quantity:
    Return price multiplied by quantity multiplied by 1.08

Let total 1 be calculate total with tax with price 1 and quantity 1
Let total 2 be calculate total with tax with price 2 and quantity 2
Let total 3 be calculate total with tax with price 3 and quantity 3
```

### Early Returns

Return early to reduce nesting:

```runa
# Bad - Deep nesting
Process called "process user" that takes user:
    If user is not null:
        If user.is_active:
            If user.age is greater than 18:
                Do processing
                Return success
    Return error

# Good - Early returns
Process called "process user" that takes user:
    If user is null:
        Return error

    If not user.is_active:
        Return error

    If user.age is less than or equal to 18:
        Return error

    Do processing
    Return success
```

### Avoid Magic Numbers

Use named constants:

```runa
# Bad - Magic number
If user.age is greater than 18:
    Grant access

# Good - Named constant
Let MINIMUM_AGE be 18

If user.age is greater than MINIMUM_AGE:
    Grant access
```

## Anti-Patterns to Avoid

### 1. God Functions

Don't create functions that do too much:

```runa
# Bad - Does everything
Process called "handle user" that takes user data:
    Validate user data
    Create user in database
    Send welcome email
    Log activity
    Update analytics
    Generate report
    ...

# Good - Separate concerns
Process called "create user" that takes user data:
    Return create in database with user data

Process called "onboard user" that takes user:
    send welcome email to user
    log user creation with user
```

### 2. Deep Nesting

Avoid deeply nested code:

```runa
# Bad - Hard to follow
If condition 1:
    If condition 2:
        If condition 3:
            If condition 4:
                Do something

# Good - Flatten with early returns or guards
If not condition 1:
    Return

If not condition 2:
    Return

If not condition 3:
    Return

If condition 4:
    Do something
```

### 3. Unclear Variable Names

```runa
# Bad
Let x be get data
Let temp be process with x
Let final be temp plus 10

# Good
Let user data be get data
Let processed data be process with user data
Let adjusted score be processed data plus 10
```

## Auto-Formatting

Use the Runa formatter to enforce style:

```bash
# Format a single file
runafmt myfile.runa

# Format all files in a directory
runafmt src/**/*.runa

# Format and convert to Canon mode
runafmt myfile.runa --mode canon

# Check without modifying
runafmt myfile.runa --check
```

## Linting

Use the Runa linter to catch style issues:

```bash
# Lint a file
runalint myfile.runa

# Strict mode (enforce all style rules)
runalint myfile.runa --strict

# Auto-fix simple issues
runalint myfile.runa --fix
```

## Example: Well-Styled Runa Code

```runa
Note: user_authentication.runa
Note: Handles user authentication and session management

Import "crypto" as crypto
Import "database" as db

Let MAX_LOGIN_ATTEMPTS be 3
Let SESSION_TIMEOUT be 3600

Type called User:
    id as Integer
    username as String
    password hash as String
    last login as Timestamp

Process called "authenticate user" that takes username and password returns Result of User:
    Note: Authenticate user with username and password

    If username is empty or password is empty:
        Return error with "Username and password required"

    Let user be db.find user by username with username
    If user is null:
        Return error with "User not found"

    Let password hash be crypto.hash password with password
    If password hash is not equal to user.password hash:
        Return error with "Invalid password"

    update last login for user
    Return success with user

Process called "create session" that takes user returns String:
    Note: Create a new session for the authenticated user

    Let session id be crypto.generate random string with 32
    Let expiry time be current time plus SESSION_TIMEOUT

    db.store session with:
        id as session id
        user id as user.id
        expires at as expiry time

    Return session id
```

## Related Pages

- [Syntax Modes](Syntax-Modes)
- [Quick Start Tutorial](Quick-Start-Tutorial)
- [Type System](Type-System)
- [Testing Guidelines](Testing-Guidelines)

---

**Questions about style?** Ask in [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions).
