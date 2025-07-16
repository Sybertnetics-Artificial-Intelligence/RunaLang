# Runa Standard Library: Primitives Module

## Overview

Primitive types (`Integer`, `Float`, `String`, `Boolean`, `None`) are built-in to the Runa language. This module documents the idiomatic way to check and retrieve types in Runa.

## Type Checking

Type checking is performed using the `is of type` operator:

```runa
Let x be 42
Assert x is of type Integer
```

## Type Retrieval

Type retrieval is performed using the `type of` expression:

```runa
Let t be type of x
Assert t is equal to "Integer"
```

## Testing

A comprehensive Runa-based test file for the primitives module is located at:

    runa/tests/stdlib/test_primitives.runa

This file exercises type checking and retrieval using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability. 