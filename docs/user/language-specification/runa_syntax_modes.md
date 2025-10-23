# Runa Syntax Modes Specification

## Overview

Runa supports multiple syntax modes to accommodate different developer preferences and use cases. The language maintains consistency in keywords across modes while allowing flexibility in operator representation.

## Syntax Modes

### Canon Mode (Default)
Canon mode uses natural language operators and is the default mode for Runa. It prioritizes readability and clarity.

**Characteristics:**
- Natural language operators: `multiplied by`, `is equal to`, `plus`
- Standard Runa keywords: `Process`, `Type`, `Public`, `Private`
- Designed for clarity and educational purposes
- Ideal for AI comprehension and generation

### Developer Mode
Developer mode uses symbolic operators familiar to programmers from other languages while maintaining Runa's keyword consistency.

**Characteristics:**
- Symbolic operators: `*`, `==`, `+`
- Same keywords as Canon mode: `Process`, `Type`, `Public`, `Private`
- Designed for developers familiar with C-style syntax
- More compact representation

### Viewer Mode (Future - Read-Only)
Viewer mode will provide a natural language representation for display purposes only. This mode is read-only and designed for non-technical stakeholders and AI systems that need to verify code behavior.

**Characteristics:**
- Full natural language sentences
- Educational context injection
- Read-only display format
- Pattern-based transformation from Canon/Developer modes

## Mode Consistency

### Keywords Remain Constant
All keywords remain the same across Canon and Developer modes:

| Keyword | Canon Mode | Developer Mode |
|---------|------------|----------------|
| Process | Process | Process |
| Type | Type | Type |
| Public | Public | Public |
| Private | Private | Private |
| If | If | If |
| Otherwise | Otherwise | Otherwise |
| For | For | For |
| While | While | While |
| Return | Return | Return |

### Identifier Rules Across Modes

Identifiers follow consistent normalization rules across all syntax modes:

#### Canonical vs Non-Canonical Forms

1. **Canonical Forms** (Normalized):
   - Identifiers with spaces or underscores as separators
   - `calculate_area` ≡ `calculate area` (treated as same identifier)
   - This is the idiomatic "Runa Way"

2. **Non-Canonical Forms** (Not Normalized):
   - camelCase: `calculateArea`
   - PascalCase: `CalculateArea`
   - These remain distinct, atomic identifiers
   - Supported for interoperability but discouraged

3. **Case Sensitivity**: Always enforced
   - `calculate` ≠ `Calculate` ≠ `CALCULATE`
   - Applies to both canonical and non-canonical forms

#### Style Enforcement Strategy

Runa actively promotes canonical spaced forms through:

- **Documentation**: All examples use `calculate area` style
- **Linter Warnings**: Flags non-canonical forms
- **Auto-Formatting**: Converts `snake_case` to spaced form
- **No Compiler Errors**: All forms compile successfully

**Idiomatic Examples (Recommended):**
```runa
Note: Canonical spaced form - THE RUNA WAY
Let result be calculate area(5.0)
Let user data be fetch user data()
Set shopping cart total to 0.0
```

**Supported but Discouraged:**
```runa
Note: These work but trigger linter warnings
Let result be calculateArea(5.0)    Note: Warning: Non-idiomatic camelCase
Let data be getUserData()           Note: Warning: Non-idiomatic camelCase
```

### Operators Change Between Modes
Only operators change between Canon and Developer modes:

| Operation | Canon Mode | Developer Mode |
|-----------|------------|----------------|
| Addition | `plus` | `+` |
| Subtraction | `minus` | `-` |
| Multiplication | `multiplied by` | `*` |
| Division | `divided by` | `/` |
| Modulo | `modulo by` | `%` |
| Power | `to the power of` | `**` |
| Equality | `is equal to` | `==` |
| Inequality | `is not equal to` | `!=` |
| Greater than | `is greater than` | `>` |
| Less than | `is less than` | `<` |
| Greater or equal | `is greater than or equal to` | `>=` |
| Less or equal | `is less than or equal to` | `<=` |
| Logical AND | `And` | `&&` |
| Logical OR | `Or` | `||` |
| Logical NOT | `Not` | `!` |
| Bitwise AND | `bitwise and` | `&` |
| Bitwise OR | `bitwise or` | `|` |
| Bitwise XOR | `bitwise xor` | `^` |
| Bitwise NOT | `bitwise not` | `~` |
| Left shift | `shifted left by` | `<<` |
| Right shift | `shifted right by` | `>>` |
| Assignment | `Let ___ be` | `=` |
| Reassignment | `Set ___ to` | `=` |
| Add-assign | `gets increased by` | `+=` |
| Sub-assign | `gets decreased by` | `-=` |
| Mul-assign | `gets multiplied by` | `*=` |
| Div-assign | `gets divided by` | `/=` |
| String concat | `joined with` | `++` |
| Membership | `contains` | `in` |

### Collection Literals Change Between Modes

| Collection Type | Canon Mode | Developer Mode |
|-----------------|------------|----------------|
| List creation | `a list containing 1, 2, 3` | `[1, 2, 3]` |
| Dictionary creation | `a dictionary containing: "key" as value End Dictionary` | `{"key": value}` |
| Array type | `Array of 3 Floats` | `Array[Float, 3]` |
| Index access | `list at index 0` | `list[0]` |
| Length operation | `length of list` | `list.length()` |
| Dictionary access | `dict at key "name"` | `dict["name"]` |
| Dictionary keys | `all keys in dict` | `dict.keys()` |
| List append | `Add item to end of list` | `list.append(item)` |
| List insert | `Insert item at index 0 in list` | `list.insert(0, item)` |

## Examples

### Canon Mode Example
```runa
Process called "calculate_area" that takes width as Float, height as Float returns Float:
    Let area be width multiplied by height

    If area is greater than 100.0:
        Display "Large area: " joined with area
    Otherwise:
        Display "Small area: " joined with area
    End If

    Return area
End Process

Process called "process_data":
    Let numbers be a list containing 1, 2, 3, 4, 5
    Let user be a dictionary containing:
        "name" as "Alice",
        "age" as 30
    End Dictionary

    Let first_num be numbers at index 0
    Let user_name be user at key "name"
    Let size be length of numbers

    Add 6 to end of numbers
    Set user at key "email" to "alice@example.com"
End Process
```

### Developer Mode Example
```runa
Process called "calculate_area" that takes width as Float, height as Float returns Float:
    Let area be width * height

    If area > 100.0:
        Display "Large area: " ++ area
    Otherwise:
        Display "Small area: " ++ area
    End If

    Return area
End Process

Process called "process_data":
    Let numbers = [1, 2, 3, 4, 5]
    Let user = {
        "name": "Alice",
        "age": 30
    }

    Let first_num = numbers[0]
    Let user_name = user["name"]
    Let size = numbers.length()

    numbers.append(6)
    user["email"] = "alice@example.com"
End Process
```

Note that in both examples, keywords like `Process`, `Let`, `If`, `Otherwise`, `Display`, and `Return` remain identical.

## Mode Selection

### Compiler Flags
```bash
# Canon mode (default)
runac source.runa

# Explicit Canon mode
runac --mode=canon source.runa

# Developer mode
runac --mode=developer source.runa
```

### File-Level Pragma (Future)
```runa
@pragma syntax_mode developer

Process called "main":
    Display "Using developer mode operators"
End Process
```

## Implementation Details

### Lexer Behavior
The lexer maintains the syntax mode in its state and uses it to:
1. Keep keywords unchanged regardless of mode
2. Convert operators between representations during tokenization
3. Preserve mode consistency throughout the compilation unit

### AST Representation
The Abstract Syntax Tree uses a canonical internal representation regardless of the input mode. This ensures consistent semantic analysis and code generation.

### Conversion Functions
The compiler provides bidirectional conversion functions:
- `Keywords.convert_operator(operator, target_mode)` - Converts operators between modes
- `Keywords.get_canonical_form(keyword, mode)` - Returns keywords unchanged
- `Keywords.is_operator(text)` - Checks if text is an operator in any mode

## Design Rationale

### Why Keywords Don't Change
- **Clarity**: Keywords like `Public` and `Private` are already clear to all audiences
- **Simplicity**: Reduces cognitive overhead by maintaining one set of keywords
- **Consistency**: Easier to learn and teach with consistent keywords
- **Less Bugs**: Fewer conversion points mean fewer potential errors

### Why Operators Change
- **Familiarity**: Developers can use familiar symbols from other languages
- **Compactness**: Symbolic operators are more concise for complex expressions
- **Readability**: Natural language operators improve readability for non-programmers
- **Flexibility**: Accommodates different preferences and use cases

## Future Considerations

### Viewer Mode Implementation
Viewer mode will be implemented as a post-processing transformation layer that:
1. Parses source in Canon or Developer mode
2. Generates standard AST
3. Applies pattern-based transformations
4. Produces natural language output with educational context

### Mixed Mode Support
Future versions may support mixing modes within a file using block-level pragmas:
```runa
@begin_developer_mode
Let result be (a * b) + (c / d)
@end_developer_mode
```

## Conclusion

Runa's syntax modes provide flexibility while maintaining consistency. By keeping keywords constant and only varying operators, the language achieves a balance between readability, familiarity, and simplicity. This design supports Runa's goal of being accessible to both AI systems and human developers while maintaining a clean, consistent architecture.