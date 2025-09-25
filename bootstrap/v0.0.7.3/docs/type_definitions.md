# Type Definition Syntax for v0.0.7.3

This document clarifies the type definition syntax used in the v0.0.7.3 bootstrap compiler.

## Consistency Rule

All type definitions should end with `End Type` for consistency with other block structures in Runa (like `Process ... End`, `If ... End If`, etc.).

## Type Definition Formats

### 1. Struct Types

Structs use the `Type called "Name":` syntax with fields listed inside:

```runa
Type called "Point":
    x as Integer,
    y as Integer
End Type
```

### 2. Variant Types (ADTs/Sum Types)

Variants use the `Type Name is` syntax with pipe-separated variants:

```runa
Type Shape is
    | Circle with radius as Float
    | Rectangle with width as Float and height as Float
End Type
```

**Note**: While current implementation doesn't require `End Type` for variants, it should be added for consistency.

### 3. Array Types

Fixed-size arrays use the `Type Name is` syntax:

```runa
Type IntArray is
    array[10] of Integer
End Type
```

The array definition specifies:
- Size in square brackets: `[10]`
- Element type after `of`: `Integer`

### 4. Function Pointer Types

Function pointer types use the `Type Name is Pointer to Process` syntax:

```runa
Type BinaryOp is Pointer to Process takes x as Integer and y as Integer returns Integer
End Type
```

**Note**: While not yet requiring `End Type`, it should be added for consistency.

## Implementation Status

As of v0.0.7.3:
- ✅ Structs require `End Type`
- ⚠️ Variants currently don't require `End Type` (should be fixed)
- ⚠️ Arrays being implemented with `End Type` requirement
- ⚠️ Function pointers currently don't require `End Type` (should be fixed)

## Future Consistency

All type definitions should follow the pattern:

```
Type <definition>
End Type
```

This maintains consistency with other Runa block structures and makes the language more predictable.