# ADT Implicit Variant Construction - Implementation Plan

## Current Status (v0.0.8.3)

### ✅ Implemented Features
1. **Type Definitions** - Variant types with multiple constructors
   ```runa
   Type Option is:
       | None
       | Some with value as Integer
   End Type
   ```

2. **Explicit Variant Construction** - Requires type prefix
   ```runa
   Let x be Option as None                    # Fieldless
   Let y be Option as Some with value as 42   # With field
   ```

3. **Pattern Matching** - Full support
   - Variant patterns with field extraction
   - Wildcard patterns (`_`)
   - Literal patterns (integers)
   - Type patterns (`of Type`)
   - Exhaustiveness checking

### ❌ Missing Feature: Implicit Variant Construction

**Current Behavior:**
```runa
Let y be None  # ERROR: Undefined variable 'None'
```

**Expected Behavior:**
```runa
Type Option is:
    | None
    | Some with value as Integer
End Type

Let y be None  # Should infer type as Option and create variant
```

**Test File:** `tests/unit/test_adt_explicit.runa` expects this to work but currently fails.

---

## Implementation Requirements

### 1. Variant Name Lookup in Parser

When parser encounters an identifier, it needs to:
1. Check if identifier matches a known variant name (not just type names)
2. If yes, determine which type it belongs to
3. Create EXPR_VARIANT_CONSTRUCTOR with inferred type

**Current Code Flow (parser.runa lines 2392-2432):**
- Only checks if identifier is a **type name**
- Does not check if identifier is a **variant name**

**Required Addition:**
```runa
Note: After type check, also check if this is a variant name
Let is_variant be 0
Let variant_type_name be 0
If is_type is equal to 0:
    Note: Not a type, check if it's a variant name
    Let vi be 0
    While vi is less than type_count:
        Let type_ptr be memory_get_pointer_at_index(types, vi)
        Let type_def_name be memory_get_pointer(type_ptr, 0)
        Let type_kind be memory_get_int32(type_ptr, 8)

        If type_kind is equal to 1:  Note: TYPE_KIND_VARIANT
            Let variant_count be memory_get_int32(type_ptr, 24)
            Let variants be memory_get_pointer(type_ptr, 16)

            Let vj be 0
            While vj is less than variant_count:
                Let variant_ptr be variants plus (vj multiplied by 32)
                Let vname be memory_get_pointer(variant_ptr, 0)

                If string_equals(vname, name) is equal to 1:
                    Set is_variant to 1
                    Set variant_type_name to type_def_name
                    Set vi to type_count  Note: Break outer
                    Set vj to variant_count  Note: Break inner
                End If
                Set vj to vj plus 1
            End While
        End If
        Set vi to vi plus 1
    End While
End If
```

### 2. Implicit Variant Construction

**After variant lookup succeeds:**
```runa
If is_variant is equal to 1:
    Note: Create implicit variant constructor
    Let expr be memory_allocate(40)
    memory_set_int32(expr, 0, EXPR_VARIANT_CONSTRUCTOR)
    memory_set_pointer(expr, 8, variant_type_name)    # Inferred type
    memory_set_pointer(expr, 16, name)                # Variant name
    memory_set_pointer(expr, 24, 0)                   # No fields (for now)
    memory_set_int32(expr, 32, 0)                     # Field count = 0

    parser_eat(parser, 53)  Note: TOKEN_IDENTIFIER
    Return expr
End If
```

### 3. Implicit Variants with Fields

**Challenge:** How to handle implicit variants with fields?
```runa
Let x be Some with value as 42  # Type must be inferred from 'Some'
```

**Solution:** Check for TOKEN_WITH after variant name
```runa
If is_variant is equal to 1:
    Let expr be memory_allocate(40)
    memory_set_int32(expr, 0, EXPR_VARIANT_CONSTRUCTOR)
    memory_set_pointer(expr, 8, variant_type_name)
    memory_set_pointer(expr, 16, name)

    parser_eat(parser, 53)

    Note: Check for 'with' keyword
    Let next_token be memory_get_pointer(parser, 8)
    If next_token is not equal to 0:
        Let next_type be memory_get_int32(next_token, 0)
        If next_type is equal to 114:  Note: TOKEN_WITH
            Note: Parse fields (same logic as explicit syntax)
            parser_eat(parser, 114)
            Note: ... field parsing code ...
        End If
    End If

    Return expr
End If
```

---

## Ambiguity Concerns

### Potential Conflicts

**Problem:** What if a variant name conflicts with a variable name?
```runa
Type Option is:
    | None
End Type

Let None be 42        # Variable named 'None'
Let x be None         # Is this the variant or the variable?
```

**Resolution Strategies:**

1. **Variant Priority** (Recommended)
   - Variant names always take precedence over variables
   - Variables cannot shadow variant names (parser error)
   - Simple, predictable, matches ML-family languages

2. **Context-Based**
   - If followed by `with`, it's a variant
   - Otherwise, check variant registry first, then variables
   - More complex, harder to reason about

3. **Explicit Opt-In**
   - Require explicit syntax unless disabled with pragma
   - Conservative but less convenient

**Recommended:** Use **Variant Priority** - it's simpler and matches user expectations.

---

## Implementation Steps

### Step 1: Add Variant Name Registry Lookup
**File:** `src/parser.runa` (~line 2432)
- After type name check fails
- Loop through all types looking for variant match
- Store matched type name

### Step 2: Create Implicit Variant Constructor
**File:** `src/parser.runa` (~line 2432)
- When variant found, create EXPR_VARIANT_CONSTRUCTOR
- Use inferred type name
- Handle optional 'with' for fields

### Step 3: Handle Shadowing Rules
**File:** `src/parser.runa` (variable declaration)
- When declaring variables, check if name conflicts with variant
- Emit error if variable would shadow variant name

### Step 4: Update Tests
**File:** `tests/unit/test_adt_explicit.runa`
- Should now pass with implicit syntax

### Step 5: Add Additional Tests
**New file:** `tests/unit/test_adt_implicit.runa`
```runa
Type Option is:
    | None
    | Some with value as Integer
End Type

Process called "main" returns Integer:
    Note: Implicit fieldless variant
    Let x be None

    Match x:
        When None:
            Display "Works!"
        When _:
            Display "FAIL"
            Return 1
    End Match

    Note: Implicit variant with field
    Let y be Some with value as 42

    Match y:
        When Some with value as v:
            If v is equal to 42:
                Display "Success"
            Otherwise:
                Display "FAIL"
                Return 1
            End If
        When _:
            Display "FAIL"
            Return 1
    End Match

    Return 0
End Process
```

---

## Edge Cases to Handle

1. **Multiple types with same variant name**
   ```runa
   Type A is: | None
   Type B is: | None

   Let x be None  # AMBIGUOUS - should error
   ```
   **Solution:** Emit parser error about ambiguous variant name

2. **Variant name same as built-in**
   ```runa
   Type X is: | Integer  # Conflicts with built-in type
   ```
   **Solution:** Probably should disallow this, emit error

3. **Case sensitivity**
   ```runa
   Type Option is: | none
   Let x be None  # Does this match?
   ```
   **Solution:** Runa is case-sensitive, these are different

---

## Testing Strategy

### Unit Tests Needed:
1. ✅ `test_adt_explicit.runa` - Should now pass
2. ➕ `test_adt_implicit.runa` - Basic implicit construction
3. ➕ `test_adt_implicit_with_fields.runa` - Implicit with fields
4. ➕ `test_adt_ambiguous.runa` - Ambiguity detection
5. ➕ `test_adt_shadowing.runa` - Variable/variant shadowing

### Integration Tests:
- Recursive ADTs with implicit construction
- Pattern matching on implicitly constructed variants
- Multiple variant types in same scope

---

## Estimated Effort

- **Variant lookup logic:** ~50 lines of Runa code
- **Implicit constructor creation:** ~30 lines
- **Field parsing reuse:** Reuse existing code
- **Shadowing detection:** ~20 lines
- **Testing:** 4-5 new test files

**Total:** ~2-3 hours of implementation + testing

---

## Open Questions

1. **Should we allow variant names to shadow variables?**
   - Recommendation: No, emit error

2. **What about type parameters/generics?**
   - Not relevant yet, generics not implemented

3. **Should implicit syntax be enabled by default?**
   - Recommendation: Yes, it's more ergonomic and matches OCaml/Rust/Haskell

---

## Summary

**What's Missing:**
- Parser doesn't check if identifier is a variant name
- No implicit variant construction path

**What's Needed:**
- Variant name lookup in parser (when identifier found)
- Implicit EXPR_VARIANT_CONSTRUCTOR creation
- Shadowing detection and error handling

**Breaking Changes:**
- None (only adds new syntax, doesn't remove anything)

**Benefits:**
- More ergonomic ADT usage
- Matches ML-family language conventions
- Makes pattern matching feel more natural
