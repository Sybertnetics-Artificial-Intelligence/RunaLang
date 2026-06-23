# Backend Common Utilities

## Purpose

This directory contains **universal code generation utilities** used by all backend translators in the translation layer.

These utilities eliminate ~400 lines of duplicated code across 51+ backend implementations.

## Files

### `code_generation.runa`

**Universal code generation context and helpers for HIR → Target Language backends.**

**Key Features:**
- Output buffering with efficient string concatenation
- Automatic indentation management (increase/decrease/emit)
- Line and column position tracking
- Error and warning collection
- Backend-specific metadata storage
- Common emission patterns (braces, brackets, separators, comments)

## Usage

### Basic Usage Pattern

```runa
Import "compiler/middle/gungnir/hir/translation/backends/common/code_generation.runa" as CodeGen

Process called "translate_to_python" that takes hir_module as Integer returns String:
    Note: Create generation context
    Let ctx be proc create_code_context from CodeGen

    Note: Generate code
    proc generate_module from ctx, hir_module

    Note: Get output
    Let code be proc get_output from CodeGen with ctx

    Note: Check for errors
    Let has_errors be proc has_errors from CodeGen with ctx
    If has_errors is equal to 1:
        Return ""
    End If

    Return code
End Process
```

### Indentation Example

```runa
Note: Generate a function with indented body
proc emit_line from CodeGen with ctx, "def my_function():"
proc increase_indent from CodeGen with ctx

proc emit_indented_line from CodeGen with ctx, "x = 10"
proc emit_indented_line from CodeGen with ctx, "return x"

proc decrease_indent from CodeGen with ctx
```

**Output:**
```python
def my_function():
    x = 10
    return x
```

### Block Generation Example

```runa
Note: Generate a brace-delimited block
proc emit_indented from CodeGen with ctx, "if (condition) "
proc begin_brace_block from CodeGen with ctx

proc emit_block_statement from CodeGen with ctx, "doSomething();"
proc emit_block_statement from CodeGen with ctx, "doSomethingElse();"

proc end_brace_block from CodeGen with ctx
```

**Output:**
```c
if (condition) {
    doSomething();
    doSomethingElse();
}
```

### Error Handling Example

```runa
Note: Add errors during generation
If invalid_node is equal to 1:
    proc add_generation_error from CodeGen with ctx, "Invalid HIR node encountered"
    Return ""
End If

Note: Add warnings
If deprecated_feature is equal to 1:
    proc add_generation_warning from CodeGen with ctx, "Deprecated feature usage"
End If

Note: Check for errors before returning
Let has_errors be proc has_errors from CodeGen with ctx
If has_errors is equal to 1:
    Let errors be proc get_errors from CodeGen with ctx
    Note: Report errors to user
    Return ""
End If
```

### List Generation Example

```runa
Note: Generate comma-separated list
proc emit from CodeGen with ctx, "["

Let count be proc size from List with items
Let index be 0
While index is less than count:
    Let item be proc get from List with items, index
    Let is_last be index is equal to count - 1

    proc emit from CodeGen with ctx, item
    proc emit_list_item from CodeGen with ctx, item, is_last

    Set index to index + 1
End While

proc emit from CodeGen with ctx, "]"
```

**Output:** `[item1, item2, item3]`

## API Reference

### Context Management

| Function | Description |
|----------|-------------|
| `create_code_context()` | Create new generation context with default settings |
| `create_code_context_with_indent(indent_string)` | Create context with custom indent (e.g., tabs) |
| `destroy_code_context(ctx)` | Clean up context (optional, memory managed) |

### Output Emission

| Function | Description |
|----------|-------------|
| `emit(ctx, text)` | Append text to output |
| `emit_line(ctx, text)` | Append text with newline |
| `emit_newline(ctx)` | Emit blank line |
| `get_output(ctx)` | Retrieve generated code |
| `get_output_length(ctx)` | Get output length in characters |
| `clear_output(ctx)` | Reset output buffer |

### Indentation

| Function | Description |
|----------|-------------|
| `emit_indent(ctx)` | Emit current indentation level |
| `increase_indent(ctx)` | Increase indent by 1 level |
| `decrease_indent(ctx)` | Decrease indent by 1 level |
| `set_indent_level(ctx, level)` | Set absolute indent level |
| `get_indent_level(ctx)` | Get current indent level |
| `set_indent_string(ctx, string)` | Set indent string (default: 4 spaces) |
| `get_indent_string(ctx)` | Get current indent string |

### Indented Helpers

| Function | Description |
|----------|-------------|
| `emit_indented(ctx, text)` | Emit indent then text (no newline) |
| `emit_indented_line(ctx, text)` | Emit indent, text, and newline |
| `begin_indented_block(ctx)` | Increase indent (alias for `increase_indent`) |
| `end_indented_block(ctx)` | Decrease indent (alias for `decrease_indent`) |

### Block Generation

| Function | Description |
|----------|-------------|
| `begin_block(ctx, opening)` | Emit opening line and increase indent |
| `end_block(ctx, closing)` | Decrease indent and emit closing line |
| `begin_brace_block(ctx)` | Begin `{` block |
| `end_brace_block(ctx)` | End `}` block |
| `emit_block_statement(ctx, stmt)` | Emit indented statement line |

### Convenience Emitters

| Function | Description |
|----------|-------------|
| `emit_space(ctx)` | Emit space |
| `emit_comma(ctx)` | Emit `,` |
| `emit_semicolon(ctx)` | Emit `;` |
| `emit_comma_separator(ctx)` | Emit `, ` |
| `emit_opening_brace(ctx)` | Emit `{` |
| `emit_closing_brace(ctx)` | Emit `}` |
| `emit_opening_bracket(ctx)` | Emit `[` |
| `emit_closing_bracket(ctx)` | Emit `]` |
| `emit_opening_paren(ctx)` | Emit `(` |
| `emit_closing_paren(ctx)` | Emit `)` |

### List Generation

| Function | Description |
|----------|-------------|
| `emit_list_item(ctx, item, is_last)` | Emit item with comma (unless last) |
| `emit_list_item_with_newline(ctx, item, is_last)` | Emit item on new line with comma |

### Error/Warning Management

| Function | Description |
|----------|-------------|
| `add_generation_error(ctx, message)` | Add error message |
| `add_generation_error_with_location(ctx, msg, line, col)` | Add error with location |
| `add_generation_warning(ctx, message)` | Add warning message |
| `add_generation_warning_with_location(ctx, msg, line, col)` | Add warning with location |
| `get_errors(ctx)` | Get error list |
| `get_warnings(ctx)` | Get warning list |
| `has_errors(ctx)` | Check if errors exist |
| `get_error_count(ctx)` | Count errors |
| `get_warning_count(ctx)` | Count warnings |

### Position Tracking

| Function | Description |
|----------|-------------|
| `get_current_line(ctx)` | Get current output line number |
| `get_current_column(ctx)` | Get current output column |

### Metadata

| Function | Description |
|----------|-------------|
| `set_metadata(ctx, metadata)` | Store backend-specific data |
| `get_metadata(ctx)` | Retrieve backend-specific data |

### Comments

| Function | Description |
|----------|-------------|
| `emit_line_comment(ctx, prefix, text)` | Emit line comment (e.g., `// text`) |
| `emit_block_comment_start(ctx, prefix)` | Start block comment |
| `emit_block_comment_line(ctx, text)` | Add line to block comment |
| `emit_block_comment_end(ctx, suffix)` | End block comment |

## Benefits

### Before (Without Common Utilities)

Each backend had ~10-15 lines of duplicated code:

```runa
Note: Every backend repeated this pattern
Type called "PythonBackend":
    output as String
    indent_level as Integer
End Type

Process called "emit" that takes backend as Integer, text as String returns Integer:
    Let current be proc read_string from Memory at backend with 0
    Let new_output be proc string_concat from StringCore with current, text
    proc write_string from Memory at backend with 0, new_output
    Return 1
End Process

Process called "increase_indent" that takes backend as Integer returns Integer:
    Let level be proc read_integer from Memory at backend with 8
    proc write_integer from Memory at backend with 8, level + 1
    Return 1
End Process

Note: ... repeated in 51 backends
```

**Total Duplication:** ~400-500 lines across all backends

### After (With Common Utilities)

Each backend now uses shared utilities:

```runa
Import "compiler/middle/gungnir/hir/translation/backends/common/code_generation.runa" as CodeGen

Process called "translate_to_python" that takes hir_module as Integer returns String:
    Let ctx be proc create_code_context from CodeGen
    proc generate_module from ctx, hir_module
    Return proc get_output from CodeGen with ctx
End Process
```

**Result:**
- **400+ lines eliminated**
- **Consistent API** across all backends
- **Easier maintenance** (fix once, fixes everywhere)
- **Better testing** (test common utilities once)

## Migration Guide

### Step 1: Add Import

```runa
Import "compiler/middle/gungnir/hir/translation/backends/common/code_generation.runa" as CodeGen
```

### Step 2: Replace Backend Type

**Before:**
```runa
Type called "MyBackend":
    output as String
    indent_level as Integer
End Type
```

**After:**
```runa
Note: Use CodeGenerationContext from CodeGen utilities
```

### Step 3: Replace Context Creation

**Before:**
```runa
Let backend be proc allocate from Memory with 16
proc write_string from Memory at backend with 0, ""
proc write_integer from Memory at backend with 8, 0
```

**After:**
```runa
Let ctx be proc create_code_context from CodeGen
```

### Step 4: Replace Emit Functions

**Before:**
```runa
Process called "emit" that takes backend as Integer, text as String returns Integer:
    Let current be proc read_string from Memory at backend with 0
    Let new_output be proc string_concat from StringCore with current, text
    proc write_string from Memory at backend with 0, new_output
    Return 1
End Process
```

**After:**
```runa
Note: Use proc emit from CodeGen with ctx, text
```

### Step 5: Replace Indentation

**Before:**
```runa
Process called "increase_indent" ...
Process called "decrease_indent" ...
Process called "emit_indent" ...
```

**After:**
```runa
Note: Use proc increase_indent from CodeGen with ctx
Note: Use proc decrease_indent from CodeGen with ctx
Note: Use proc emit_indent from CodeGen with ctx
```

## Complete Example

**Full backend using common utilities:**

```runa
Import "compiler/middle/gungnir/hir/translation/backends/common/code_generation.runa" as CodeGen
Import "compiler/middle/gungnir/hir/hir_nodes.runa" as HIR

Process called "translate_to_javascript" that takes hir_module as Integer returns String:
    Let ctx be proc create_code_context from CodeGen

    proc generate_javascript_module from ctx, hir_module

    If proc has_errors from CodeGen with ctx is equal to 1:
        Return ""
    End If

    Return proc get_output from CodeGen with ctx
End Process

Process called "generate_javascript_module" that takes ctx as Integer, module as Integer returns Integer:
    Let functions be proc get_module_functions from module
    Let count be proc size from List with functions
    Let index be 0

    While index is less than count:
        Let func be proc get from List with functions, index
        proc generate_javascript_function from ctx, func
        proc emit_newline from CodeGen with ctx
        Set index to index + 1
    End While

    Return 1
End Process

Process called "generate_javascript_function" that takes ctx as Integer, func as Integer returns Integer:
    Let func_name be proc get_function_name from func

    proc emit_indented from CodeGen with ctx, "function "
    proc emit from CodeGen with ctx, func_name
    proc emit from CodeGen with ctx, "() "
    proc begin_brace_block from CodeGen with ctx

    Note: Generate function body
    Let body be proc get_function_body from func
    proc generate_javascript_block from ctx, body

    proc end_brace_block from CodeGen with ctx

    Return 1
End Process
```

This approach is **clean, maintainable, and eliminates hundreds of lines of duplication**.
