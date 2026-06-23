# Syntax Modes

Runa supports multiple syntax modes to accommodate different developer preferences and use cases while maintaining complete semantic equivalence.

## Overview

Runa implements a triple syntax architecture:

1. **Canon Mode** - Natural language operators (default)
2. **Developer Mode** - Symbolic operators (familiar to programmers)
3. **Viewer Mode** - Full natural language display (planned, read-only)

## Canon Mode (Default)

Canon mode uses natural language operators and is the recommended mode for Runa programming.

### Characteristics

- Natural language operators: `multiplied by`, `is equal to`, `plus`
- Standard Runa keywords: `Process`, `Type`, `If`, `Otherwise`
- Designed for clarity and AI comprehension
- Ideal for documentation and teaching
- Primary mode for examples and tutorials

### Example

```runa
Process called "calculate total price" that takes quantity and unit price:
    Let subtotal be quantity multiplied by unit price
    Let tax be subtotal multiplied by 0.08
    Let total be subtotal plus tax

    If total is greater than 100:
        Let discount be total multiplied by 0.1
        Let total be total minus discount

    Return total
```

### Canon Mode Operators

| Operation | Canon Mode | Example |
|-----------|------------|---------|
| Addition | `plus` | `x plus y` |
| Subtraction | `minus` | `x minus y` |
| Multiplication | `multiplied by` | `x multiplied by y` |
| Division | `divided by` | `x divided by y` |
| Modulo | `modulo` | `x modulo y` |
| Equality | `is equal to` | `x is equal to y` |
| Inequality | `is not equal to` | `x is not equal to y` |
| Greater than | `is greater than` | `x is greater than y` |
| Less than | `is less than` | `x is less than y` |
| Greater or equal | `is greater than or equal to` | `x is greater than or equal to y` |
| Less or equal | `is less than or equal to` | `x is less than or equal to y` |
| Logical AND | `and` | `x and y` |
| Logical OR | `or` | `x or y` |
| Logical NOT | `not` | `not x` |
| Bitwise AND | `bitwise and` | `x bitwise and y` |
| Bitwise OR | `bitwise or` | `x bitwise or y` |
| Bitwise XOR | `bitwise xor` | `x bitwise xor y` |
| Left shift | `shifted left by` | `x shifted left by y` |
| Right shift | `shifted right by` | `x shifted right by y` |

## Developer Mode

Developer mode uses symbolic operators familiar to programmers from C-style languages.

### Characteristics

- Symbolic operators: `*`, `==`, `+`
- Same keywords as Canon mode
- More compact representation
- Familiar to developers from other languages
- Useful for experienced programmers

### Example

```runa
Process called "calculate total price" that takes quantity and unit price:
    Let subtotal be quantity * unit price
    Let tax be subtotal * 0.08
    Let total be subtotal + tax

    If total > 100:
        Let discount be total * 0.1
        Let total be total - discount

    Return total
```

### Developer Mode Operators

| Operation | Developer Mode | Example |
|-----------|----------------|---------|
| Addition | `+` | `x + y` |
| Subtraction | `-` | `x - y` |
| Multiplication | `*` | `x * y` |
| Division | `/` | `x / y` |
| Modulo | `%` | `x % y` |
| Equality | `==` | `x == y` |
| Inequality | `!=` | `x != y` |
| Greater than | `>` | `x > y` |
| Less than | `<` | `x < y` |
| Greater or equal | `>=` | `x >= y` |
| Less or equal | `<=` | `x <= y` |
| Logical AND | `&&` | `x && y` |
| Logical OR | `\|\|` | `x \|\| y` |
| Logical NOT | `!` | `!x` |
| Bitwise AND | `&` | `x & y` |
| Bitwise OR | `\|` | `x \| y` |
| Bitwise XOR | `^` | `x ^ y` |
| Left shift | `<<` | `x << y` |
| Right shift | `>>` | `x >> y` |

## Viewer Mode (Planned)

Viewer mode will provide a read-only natural language representation for non-technical stakeholders.

### Characteristics (When Implemented)

- Full natural language sentences
- Educational context injection
- Read-only display format
- Pattern-based transformation from Canon/Developer modes
- No separate lexer/parser required

### Use Cases

- Documentation generation
- Code review by non-programmers
- AI system verification
- Educational materials

### Example (Planned)

```
Define a process named "calculate total price" that accepts quantity and unit price:
    First, calculate the subtotal by multiplying the quantity by the unit price.
    Next, calculate the tax by multiplying the subtotal by 0.08.
    Then, calculate the total by adding the subtotal and tax together.

    Check if the total is greater than 100:
        When true, calculate a discount of 10% of the total.
        Subtract the discount from the total.

    Finally, return the total value.
```

## Mode Consistency

### Keywords Remain Constant

All keywords are identical across Canon and Developer modes:

```runa
# Both modes use the same keywords:
Process, Type, If, Otherwise, When, For, While, Return, Let, etc.
```

### Only Operators Change

The difference between modes is **only** in operators, not keywords or structure:

```runa
# Canon Mode
If x is greater than y and y is less than z:
    Let result be x multiplied by 2

# Developer Mode
If x > y && y < z:
    Let result be x * 2
```

## Identifier Rules

Identifiers follow consistent rules across all modes.

### Canonical Form (Recommended)

Use spaced identifiers:
```runa
Let calculate area be 10
Let user name be "Alice"
Let process data be true
```

### Equivalence Rules

Spaces and underscores are equivalent separators, but case matters per-word:

```runa
# These are THE SAME:
Calculate Area ≡ Calculate_Area

# These are THE SAME:
Calculate area ≡ Calculate_area

# These are DIFFERENT:
Calculate Area ≠ Calculate area
# (Different case on "Area" vs "area")
```

### Non-Canonical Forms (Discouraged)

camelCase and PascalCase work but are discouraged:

```runa
# Works but not recommended:
Let calculateArea be 10  # camelCase
Let CalculateArea be 20  # PascalCase

# These are treated as atomic identifiers (no normalization)
calculateArea ≠ CalculateArea
```

## Switching Between Modes

### In Your Code

Specify the mode in your source file or via compiler flag:

```bash
# Compile Canon mode (default)
runac myfile.runa

# Compile Developer mode
runac myfile.runa --mode developer

# Convert between modes
runac myfile.runa --convert-to developer -o myfile_dev.runa
```

### Auto-Formatting

The Runa formatter can convert between modes:

```bash
# Format to Canon mode
runafmt myfile.runa --mode canon

# Format to Developer mode
runafmt myfile.runa --mode developer
```

## Best Practices

### For Libraries and Public Code

- **Use Canon mode** for maximum readability
- Include clear documentation
- Use descriptive spaced identifiers

### For Internal Projects

- **Choose one mode** and stick with it
- Configure your team's preferred mode in project settings
- Use auto-formatting to enforce consistency

### For Documentation

- **Always use Canon mode** in examples
- Show Developer mode equivalents when helpful
- Explain the concept, not just the syntax

## Mixing Modes (Don't Do This)

**Warning**: Do not mix operators from different modes in the same expression:

```runa
# WRONG - Mixing Canon and Developer operators
Let result be x * y plus z  # Confusing!

# CORRECT - Canon mode
Let result be x multiplied by y plus z

# CORRECT - Developer mode
Let result be x * y + z
```

The compiler will warn about mixed-mode expressions.

## Style Enforcement

### Linter

The Runa linter can enforce mode consistency:

```bash
# Check for mode consistency
runalint myfile.runa --strict-mode
```

### CI/CD Integration

Add mode checking to your CI pipeline:

```yaml
# .runalint.yml
mode: canon
strict: true
warn_non_canonical_identifiers: true
```

## Examples Side-by-Side

### Fibonacci Function

**Canon Mode:**
```runa
Process called "fibonacci" that takes n:
    If n is less than or equal to 1:
        Return n

    Return fibonacci with n minus 1 plus fibonacci with n minus 2
```

**Developer Mode:**
```runa
Process called "fibonacci" that takes n:
    If n <= 1:
        Return n

    Return fibonacci with n - 1 + fibonacci with n - 2
```

### Sorting Algorithm

**Canon Mode:**
```runa
Process called "bubble sort" that takes list:
    Let n be length of list

    For i in range from 0 to n minus 1:
        For j in range from 0 to n minus i minus 1:
            If list at j is greater than list at j plus 1:
                Let temp be list at j
                Set list at j to list at j plus 1
                Set list at j plus 1 to temp

    Return list
```

**Developer Mode:**
```runa
Process called "bubble sort" that takes list:
    Let n be length of list

    For i in range from 0 to n - 1:
        For j in range from 0 to n - i - 1:
            If list at j > list at j + 1:
                Let temp be list at j
                Set list at j to list at j + 1
                Set list at j + 1 to temp

    Return list
```

## Related Pages

- [Quick Start Tutorial](Quick-Start-Tutorial)
- [Code Style Guide](Code-Style-Guide)
- [Variables and Data Types](Variables-and-Data-Types)

---

**For more information**, see the [complete language specification](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/blob/main/docs/user/language-specification/runa_syntax_modes.md).
