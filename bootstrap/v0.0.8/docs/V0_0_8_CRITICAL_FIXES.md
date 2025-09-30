# Runa v0.0.8 - Critical Fixes & Feature Additions

**Focus:** Fix critical bugs, add inline assembly, comprehensive testing

---

## 🚨 CRITICAL FIXES FOR v0.0.8

### 1. **Imports Don't Actually Work**
**Status:** BROKEN - CRITICAL BUG

**Current State:**
- ✅ Parser recognizes `Import "filename" as module`
- ✅ Creates import AST nodes
- ❌ **Codegen does nothing** - Line 1980: "Imports are handled at program level, no code generation needed"
- ❌ Imported files are **never loaded or compiled**

**This is a CRITICAL BUG** - imports are foundational!

**Problem:**
```runa
Import "string_utils" as StringUtils
# string_utils.runa is NEVER loaded!
# StringUtils functions DON'T EXIST!
```

**Fix required in v0.0.8:**
1. When parsing `Import "file" as Module`:
   - Load and parse `file.runa`
   - Compile it to intermediate form
   - Make its functions available under `Module.function_name`
2. Multi-file compilation support
3. Symbol resolution across modules
4. Proper linking

**This must work before v0.1.0 beta!**

---

### 2. **Negative Number Literals**
**Status:** NOT SUPPORTED

**Problem:**
```runa
Note: Canonical syntax
Let x be negative 5  # Parser error - "negative" keyword not recognized

Note: Developer/technical syntax
Let x be -5          # Parser error - unary minus not supported
```

**Workaround:**
```runa
Let x be 0 minus 5  # Verbose but works
```

**Fix required in v0.0.8:**
1. **Canonical:** Recognize `negative` keyword for negative literals
2. **Developer:** Recognize `-` as unary minus operator
3. Add unary negation to `parser_parse_primary`
4. Generate unary negation expression
5. Codegen: `negq %rax` instruction

---

### 3. **Boolean Negation with "is not"**
**Status:** PARTIALLY IMPLEMENTED

**Design:** Runa uses "is" for positive checks, "is not" for negation

**Should work:**
```runa
If x is not equal to 5:           # ✅ Works
If y is not greater than 10:      # ❓ May not work
If z is not less than 0:          # ❓ May not work
If a is not greater than or equal to b:  # ❓ May not work
```

**Fix required in v0.0.8:**
1. Ensure ALL "is not" variants parse correctly
2. Test "is not greater than", "is not less than", etc.
3. Proper codegen for inverted comparisons

**Note:** We do NOT use `Not x` - only "is not" in comparisons!

---

### 4. **Parentheses for Expression Grouping**
**Status:** NOT SUPPORTED - CRITICAL BUG

**Problem:**
```runa
Let x be (2 plus 3) multiplied by 4  # Parser error - parentheses not recognized!
Let y be 2 multiplied by (3 plus 4)  # Parser error!
```

**Current behavior:**
- Parentheses ONLY recognized for function calls
- Cannot override operator precedence
- Cannot group sub-expressions
- **Forces all complex math to be split into multiple lines**

**Workaround:**
```runa
Note: Must split into multiple lines - very verbose!
Let temp be 2 plus 3
Let x be temp multiplied by 4
```

**Why this is CRITICAL:**
- Can't write complex math on one line (your original complaint!)
- Can't override PEMDAS when needed
- Makes mathematical code extremely verbose
- Basic feature that every language has

**Fix required in v0.0.8:**
1. In `parser_parse_primary`, check for TOKEN_LPAREN (48)
2. If LPAREN found:
   - Eat LPAREN
   - Recursively call `parser_parse_expression()` to parse sub-expression
   - Eat RPAREN (49)
   - Return the sub-expression
3. This allows arbitrary nesting: `((2 plus 3) multiplied by (4 plus 5))`

**Example after fix:**
```runa
Note: Canonical syntax
Let result be (2 plus 3) multiplied by (4 minus 1)  # = 15
Let complex be ((10 plus 5) divided by 3) multiplied by 2  # = 10

Note: Developer syntax
Let result be (2 + 3) * (4 - 1)  # = 15
Let complex be ((10 + 5) / 3) * 2  # = 10
```

---

### 5. **Comment System**
**Status:** WORKING AS DESIGNED

**Runa has THREE comment types:**

```runa
Note: This is a single-line comment

Let x be 42 Note: This is an inline comment

Note: This is a
multi-line comment block
that spans multiple lines
and provides detailed documentation
:End Note
```

**We do NOT use `#` for comments** - that was my mistake!

**Status:** ✅ Working correctly, no fix needed

---

## ✨ NEW FEATURES FOR v0.0.8

### 1. **Inline Assembly**
**Status:** NEW FEATURE

See: [V0.0.8_INLINE_ASSEMBLY.md](milestones/V0.0.8_INLINE_ASSEMBLY.md)

```runa
proc syscall_exit(code: int) -> int:
    Inline Assembly:
        mov $60, %rax
        movq -8(%rbp), %rdi
        syscall
    End Assembly
    ret 0
End proc
```

---

## 🧪 COMPREHENSIVE TESTING FOR v0.0.8

### Priority 1: Test Already-Implemented Features

#### 1.1 **Modulo Operator**
```runa
# tests/unit/test_modulo.runa
Process called "main" returns Integer:
    Let x be 17 modulo by 5
    If x is equal to 2:
        Return 0  # Success
    End If
    Return 1  # Failure
End Process
```

#### 1.2 **Bitwise Operators**
```runa
# tests/unit/test_bitwise.runa
Process called "main" returns Integer:
    Let and_result be 5 bitwise and 3       # Should be 1
    Let or_result be 5 bitwise or 3         # Should be 7
    Let xor_result be 5 bitwise xor 3       # Should be 6
    Let shift_left be 5 shifted left by 1   # Should be 10
    Let shift_right be 10 shifted right by 1 # Should be 5

    If and_result is not equal to 1:
        Return 1
    End If
    If or_result is not equal to 7:
        Return 2
    End If
    Note: etc...
    Return 0
End Process
```

#### 1.3 **Logical Operators (And, Or)**
```runa
# tests/unit/test_logical.runa
Process called "main" returns Integer:
    Let a be 1
    Let b be 0

    If a is equal to 1 And b is equal to 0:
        # Should execute
    Otherwise:
        Return 1  # Failure
    End If

    If a is equal to 1 Or b is equal to 1:
        # Should execute
    Otherwise:
        Return 2  # Failure
    End If

    Return 0
End Process
```

#### 1.4 **Division by Zero**
```runa
# tests/unit/test_division_by_zero.runa
Process called "main" returns Integer:
    Let x be 10
    Let y be 0
    Let result be x divided by y
    Note: What happens here? Should not crash
    Return result
End Process
```

#### 1.5 **Large Numbers & Overflow**
```runa
# tests/unit/test_overflow.runa
Process called "main" returns Integer:
    Let max_int be 9223372036854775807  # Max int64
    Let overflow be max_int plus 1       # What happens?
    Display "Overflow: "
    Display overflow
    Return 0
End Process
```

#### 1.6 **Deep Recursion**
```runa
# tests/unit/test_deep_recursion.runa
Process called "countdown" takes n as Integer returns Integer:
    If n is less than or equal to 0:
        Return 0
    End If
    Return countdown(n minus 1)
End Process

Process called "main" returns Integer:
    Let result be countdown(1000)  # Test stack depth
    Return result
End Process
```

### Priority 2: Test New Features

#### 2.1 **Negative Numbers**
```runa
# tests/unit/test_negative.runa
Process called "main" returns Integer:
    Let x be minus 5
    Let y be 10
    Let result be x plus y
    If result is equal to 5:
        Return 0
    End If
    Return 1
End Process
```

#### 2.2 **"is not" Comparisons**
```runa
# tests/unit/test_is_not.runa
Process called "main" returns Integer:
    Let x be 5

    If x is not equal to 10:
        # Should execute
    Otherwise:
        Return 1
    End If

    If x is not greater than 10:
        # Should execute
    Otherwise:
        Return 2
    End If

    If x is not less than 1:
        # Should execute
    Otherwise:
        Return 3
    End If

    Return 0
End Process
```

#### 2.3 **Imports**
```runa
# tests/unit/math_utils.runa
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process

# tests/unit/test_import.runa
Import "math_utils" as Math

Process called "main" returns Integer:
    Let result be Math.add(5, 3)
    If result is equal to 8:
        Return 0
    End If
    Return 1
End Process
```

---

## 📋 REVISED ROADMAP

**Why arrays/structs/modules should be in v0.0.8, not spread out?**

You're right - these are **foundational features** that should be done **early and together**, not spread across multiple versions. Here's the corrected thinking:

### v0.0.8 - Core Language Complete
**All basic features working:**
- ✅ Inline assembly
- ✅ Imports (FIXED)
- ✅ Negative numbers
- ✅ "is not" comparisons
- ✅ Arrays
- ✅ Structs with fields
- ✅ For loops
- ✅ All operators tested

**Rationale:** Get the **core language complete** before optimizing or adding advanced features.

### v0.0.9 - Toolchain Independence
- Native object writer (.o files)
- Custom linker
- Pure Runa runtime (zero C)

### v0.1.0 - Beta Release
- Polished, documented, tested
- Ready for public use

### v0.2.0+ - Advanced Features
- Standard library expansion
- Optimization passes
- Error handling improvements
- Concurrency
- Advanced type system features

**Key insight:** Don't artificially spread basic features across versions. Get the **foundation solid first**, then build on it.

---

## 🎯 v0.0.8 Success Criteria

### Must Work:
1. ✅ Imports load and compile files
2. ✅ Negative number literals
3. ✅ All "is not" comparisons
4. ✅ Inline assembly syntax
5. ✅ Arrays with indexing
6. ✅ Structs with field access
7. ✅ For loops

### Must Pass Tests:
8. ✅ All operators (modulo, bitwise, logical)
9. ✅ Edge cases (division by zero, overflow, deep recursion)
10. ✅ Multi-file compilation (imports)
11. ✅ 50+ comprehensive test programs

### Must Document:
12. ✅ Complete language specification update
13. ✅ Import system documentation
14. ✅ Inline assembly guide
15. ✅ Testing results

---

**Bottom line:** v0.0.8 should complete the **core language**, not just add one feature. Get arrays, structs, and imports working NOW, not in v0.4-v0.5.
