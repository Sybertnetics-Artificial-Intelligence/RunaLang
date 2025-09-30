# Runa v0.0.7.5 - Missing & Untested Features

**Status:** Analysis of current implementation gaps

---

## ❌ NOT IMPLEMENTED

### 1. **Negative Number Literals**
**Status:** NOT SUPPORTED

**Problem:**
```runa
Let x be -5  # Parser error - minus not recognized as unary operator
```

**Current behavior:**
- Lexer tokenizes `-` as TOKEN_MINUS (binary operator)
- Parser has NO unary minus handler in `parser_parse_primary`
- Cannot write negative literals directly

**Workaround:**
```runa
Let x be 0 minus 5  # Works, but verbose
```

**Impact:** Medium - annoying but workable

**Fix required in v0.0.8:**
1. Add unary operator parsing to `parser_parse_primary`
2. Check if `-` appears before primary expression
3. Generate unary negation expression
4. Codegen: `neg %rax` instruction

---

### 2. **Unary NOT Operator**
**Status:** NOT SUPPORTED

**Problem:**
```runa
Let x be Not true  # Parser error - Not not recognized as unary
```

**Current behavior:**
- TOKEN_NOT exists (29)
- NOT parsed in logical expressions
- NO unary NOT for boolean negation

**Workaround:**
```runa
# No good workaround for boolean negation
If x is equal to 0:  # Instead of: If Not x
```

**Impact:** Medium - reduces code readability

**Fix required in v0.0.8:**
1. Add unary NOT to `parser_parse_primary`
2. Parse `Not <expression>`
3. Codegen: Compare with 0, invert result

---

### 3. **Floating Point Numbers**
**Status:** NOT SUPPORTED AT ALL

**Problem:**
```runa
Let pi be 3.14  # No float literal support
```

**Current:**
- Only integers supported
- No float type
- No float arithmetic

**Impact:** HIGH - cannot do scientific computing, graphics, etc.

**Fix required:** v0.2.0+
- Too complex for v0.0.8
- Needs float lexer, parser, type system, codegen
- Requires x87 FPU or SSE instructions

---

### 4. **Arrays**
**Status:** NOT SUPPORTED

**Problem:**
```runa
Let numbers be Array with size 10  # No array type
Let x be numbers at 0               # No indexing
```

**Current:**
- Can only use pointers + manual offset math
- No array syntax
- No bounds checking

**Impact:** HIGH - fundamental data structure missing

**Fix required:** v0.3.0+
- Array type definition
- Array indexing syntax
- Bounds checking (optional)
- Array literals

---

### 5. **Structs / Types with Fields**
**Status:** PARTIALLY IMPLEMENTED

**Current:**
- Can define types: `Type called "Point":`
- **CANNOT** define fields yet
- **CANNOT** access fields

**Problem:**
```runa
Type called "Point":
    x as Integer    # NOT IMPLEMENTED
    y as Integer    # NOT IMPLEMENTED
End Type
```

**Impact:** CRITICAL for v1.0

**Fix required:** v0.4.0
- Field definitions in type parser
- Field access syntax (`point.x`)
- Memory layout calculation
- Constructor syntax

---

### 6. **Import/Module System**
**Status:** NOT FUNCTIONAL

**Current:**
- `Import` keyword exists
- Parser recognizes it
- **DOES NOTHING** - no module loading

**Problem:**
```runa
Import "string_utils"  # Parsed but ignored
```

**Impact:** CRITICAL for v1.0

**Fix required:** v0.5.0
- Module resolution (search paths)
- Separate compilation
- Symbol export/import
- Linking multiple `.o` files

---

### 7. **For Loops**
**Status:** PARTIAL - Only While loops work

**Current:**
```runa
# This works:
While x is less than 10:
    # ...
End While

# This is parsed but may not work correctly:
For i from 0 to 10:
    # ...
End For
```

**Impact:** Medium - While loops suffice, but For is cleaner

**Fix required:** v0.6.0
- Proper For loop codegen
- Range syntax
- Iterator patterns

---

### 8. **String Interpolation**
**Status:** NOT SUPPORTED

**Problem:**
```runa
Let name be "World"
Display "Hello, " plus name plus "!"  # Verbose
# Want: Display "Hello, {name}!"      # NOT SUPPORTED
```

**Impact:** Low - concatenation works

**Fix required:** v0.7.0+
- Nice-to-have, not critical

---

### 9. **Match/Pattern Matching**
**Status:** NOT IMPLEMENTED

**Current:**
- `Match` keyword exists
- NOT fully implemented in parser
- NO codegen

**Impact:** Medium - If/Otherwise suffices

**Fix required:** v0.8.0+

---

### 10. **Error Handling (Try/Catch)**
**Status:** NOT IMPLEMENTED

**Current:**
- `Try`, `Catch` keywords exist
- NOT implemented in parser
- NO runtime support

**Impact:** HIGH for production code

**Fix required:** v0.9.0+
- Exception mechanism design
- Stack unwinding
- Runtime support

---

### 11. **Comments in Code**
**Status:** ONLY `Note:` BLOCKS WORK

**Current:**
```runa
# This is NOT a comment       # Parser error
Note: This is a comment block  # WORKS
:End Note
```

**Problem:**
- No single-line comments
- Only multi-line Note blocks

**Impact:** Low - Note blocks work fine

**Fix required:** v0.0.8 (easy fix)
- Add `#` single-line comment lexer support

---

## ⚠️ IMPLEMENTED BUT UNTESTED

### 1. **Modulo Operator**
**Status:** IMPLEMENTED, NOT TESTED

**Parser:** ✅ Handles `x modulo by y`
**Codegen:** ✅ Generates `idivq` instruction for modulo

**Test needed:**
```runa
Let remainder be 17 modulo by 5  # Should return 2
```

**Add test:** `tests/unit/test_modulo.runa`

---

### 2. **Bitwise Operators**
**Status:** IMPLEMENTED, NOT TESTED

**Operators implemented:**
- `TOKEN_BIT_AND` (39) - Bitwise AND
- `TOKEN_BIT_OR` (40) - Bitwise OR
- `TOKEN_BIT_XOR` (41) - Bitwise XOR
- `TOKEN_BIT_SHIFT_LEFT` (42) - Left shift
- `TOKEN_BIT_SHIFT_RIGHT` (43) - Right shift

**Codegen:** ✅ All implemented

**Tests needed:**
```runa
Let x be 5 bitwise and 3      # Should return 1
Let y be 5 bitwise or 3       # Should return 7
Let z be 5 bitwise xor 3      # Should return 6
Let a be 5 shifted left by 1  # Should return 10
Let b be 10 shifted right by 1 # Should return 5
```

**Add test:** `tests/unit/test_bitwise.runa`

---

### 3. **Logical Operators (And, Or)**
**Status:** IMPLEMENTED, MINIMAL TESTING

**Operators:**
- `And` (TOKEN_AND)
- `Or` (TOKEN_OR)

**Parser:** ✅ Implemented
**Codegen:** ✅ Short-circuit evaluation

**More tests needed:** Complex boolean expressions

**Add test:** `tests/unit/test_logical_ops.runa`

---

### 4. **Comparison Operators**
**Status:** TESTED (basic), UNTESTED (edge cases)

**Implemented:**
- `is equal to` (==)
- `is not equal to` (!=)
- `is less than` (<)
- `is greater than` (>)
- `is less than or equal to` (<=)
- `is greater than or equal to` (>=)

**Edge cases NOT tested:**
- Comparing negative numbers
- Comparing very large numbers
- String comparisons (if supported?)

---

### 5. **String Operations**
**Status:** PARTIAL

**What works:**
- String literals
- `string_concat`
- `string_equals`
- `string_length`

**What's untested:**
- String escape sequences (`\n`, `\t`, `\"`)
- Empty strings
- Very long strings
- Unicode/UTF-8

**Add test:** `tests/unit/test_string_edge_cases.runa`

---

### 6. **Division by Zero**
**Status:** IMPLEMENTED (check), NOT TESTED

**Codegen shows:**
```asm
testq %rcx, %rcx
je .L_div_by_zero_X
```

**Question:** What happens at div_by_zero label?
- Does it crash gracefully?
- Does it return 0?
- Does it print error?

**Add test:** `tests/unit/test_division_by_zero.runa`

---

### 7. **Recursive Functions**
**Status:** SHOULD WORK, NOT TESTED

**Factorial test exists but doesn't test deep recursion**

**Tests needed:**
- Deep recursion (100+ calls)
- Mutual recursion (A calls B, B calls A)
- Stack overflow behavior

**Add test:** `tests/unit/test_deep_recursion.runa`

---

### 8. **Large Numbers**
**Status:** UNTESTED

**Questions:**
- What's the max integer?
- Does overflow wrap around?
- Are numbers signed or unsigned?

**Tests needed:**
```runa
Let big be 9223372036854775807  # Max int64
Let overflow be big plus 1       # What happens?
```

**Add test:** `tests/unit/test_large_numbers.runa`

---

## 🔧 OPTIMIZATION ISSUES

### 1. **No Constant Folding**
**Problem:**
```runa
Let x be 2 plus 3  # Generates: mov 2, mov 3, add
                    # Should be: mov 5
```

**Impact:** Slower code, larger binaries

**Fix:** v0.9.0 (MIR optimizer)

---

### 2. **No Dead Code Elimination**
**Problem:**
```runa
Let unused be 42  # Still allocated, still in codegen
```

**Impact:** Wasted stack space

**Fix:** v0.9.0 (MIR optimizer)

---

### 3. **No Register Allocation**
**Current:**
- Everything goes through stack
- No register reuse
- Spills everything

**Impact:** 10-50x slower than optimal

**Fix:** v1.2.0+ (proper register allocator)

---

### 4. **No Tail Call Optimization**
**Problem:**
```runa
Process called "factorial" takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    End If
    Return n times factorial(n minus 1)  # Could be tail call optimized
End Process
```

**Impact:** Deep recursion = stack overflow

**Fix:** v1.3.0+ (advanced optimization)

---

## 📋 Recommended Test Suite for v0.0.8

### Priority 1: Critical Missing Features
1. `test_negative_numbers.runa` - Unary minus
2. `test_unary_not.runa` - Boolean negation
3. `test_single_line_comments.runa` - `#` comments

### Priority 2: Untested Implemented Features
4. `test_modulo.runa` - Modulo operator
5. `test_bitwise.runa` - All bitwise operations
6. `test_logical_ops_complex.runa` - Complex boolean expressions
7. `test_division_by_zero.runa` - Error handling

### Priority 3: Edge Cases
8. `test_large_numbers.runa` - Integer overflow behavior
9. `test_deep_recursion.runa` - Stack limits
10. `test_string_edge_cases.runa` - Escapes, empty strings

---

## 🎯 Recommendation for v0.0.8

**Must fix:**
1. ✅ Negative numbers (critical for usability)
2. ✅ Unary NOT (critical for logic)
3. ✅ Single-line comments (developer QoL)

**Should add tests for:**
4. ✅ Modulo (already implemented)
5. ✅ Bitwise ops (already implemented)
6. ✅ Division by zero handling

**Defer to later:**
- Floats (v0.2.0)
- Arrays (v0.3.0)
- Structs (v0.4.0)
- Modules (v0.5.0)
- For loops (v0.6.0)
- Match (v0.8.0)
- Try/Catch (v0.9.0)

---

**Keep v0.0.8 focused:** Inline assembly + critical fixes + comprehensive testing
