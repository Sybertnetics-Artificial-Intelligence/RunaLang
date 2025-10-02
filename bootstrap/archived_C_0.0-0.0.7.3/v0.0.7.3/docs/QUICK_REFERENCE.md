# Copyright 2025 Sybertnetics Artificial Intelligence Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Runa v0.0.7.3 Quick Reference Card

> **Keep this handy while coding!** Essential syntax and commands for daily Runa development.

## 🚀 Build Commands

```bash
# Basic build
./runac program.runa program.s
gcc -o program program.s runtime_*.o -no-pie -lm
./program

# One-liner
./runac program.runa program.s && gcc -o program program.s runtime_*.o -no-pie -lm && ./program; echo "Exit: $?"

# With debugging
gcc -g -o program program.s runtime_*.o -no-pie -lm
```

## 📝 Core Syntax

### Process Definition
```runa
Process called "name" takes param as Type returns Type:
    # body
    Return value
End Process
```

### Variables
```runa
Let variable be value        # Declare
Set variable to new_value    # Assign
```

### Types
```runa
Type called "Name":
    field1 as Integer,
    field2 as String
End Type
```

## 🔢 Operators

| Operation | Syntax | Example |
|-----------|--------|---------|
| **Arithmetic** | | |
| Add | `a plus b` | `5 plus 3` |
| Subtract | `a minus b` | `10 minus 4` |
| Multiply | `a multiplied by b` | `6 multiplied by 7` |
| Divide | `a divided by b` | `20 divided by 4` |
| Modulo | `a modulo b` | `10 modulo 3` |
| **Comparison** | | |
| Less | `a is less than b` | `5 is less than 10` |
| Greater | `a is greater than b` | `10 is greater than 5` |
| Equal | `a equals b` | `5 equals 5` |
| Not Equal | `a is not equal to b` | `5 is not equal to 10` |

## 🔀 Control Flow

### If Statement
```runa
If condition:
    # statements
Otherwise:
    # alternative
End If
```

### While Loop
```runa
While condition:
    # body
    # (update condition variables!)
End While
```

## 📚 Common Runtime Functions

### String Functions
```runa
string_length("hello")                    # → 5
string_char_at("hello", 1)               # → 'e'
string_substring("hello", 1, 3)          # → "ell"
string_concat("hello", " world")         # → "hello world"
string_equals("test", "test")            # → 1
string_to_integer("42")                  # → 42
integer_to_string(42)                    # → "42"
string_find("hello world", "world")      # → 6
```

### File Operations
```runa
runtime_file_exists("file.txt")          # → 1 if exists
runtime_read_file("file.txt")            # → file content
runtime_write_file("out.txt", "data")    # → 0 if success
runtime_file_size("file.txt")            # → size in bytes
```

### Math Functions
```runa
runtime_sqrt(16)                         # → 4
runtime_sin(1.57)                        # → ~1
runtime_cos(0)                           # → 1
runtime_log(2.718)                       # → ~1
```

## 🎯 Common Patterns

### Error Checking
```runa
If result equals -1:
    # Handle error
    Return 0
End If
```

### Loop with Counter
```runa
Let i be 0
While i is less than max:
    # body
    Set i to i plus 1
End While
```

### Max/Min Function
```runa
Process called "max" takes a as Integer, b as Integer returns Integer:
    If a is greater than b:
        Return a
    Otherwise:
        Return b
    End If
End Process
```

### String Processing
```runa
Let content be runtime_read_file("input.txt")
Let processed be string_replace(content, "old", "new")
Let result be runtime_write_file("output.txt", processed)
```

## 🐛 Debugging Tips

### Check Exit Codes
```bash
./program; echo "Exit code: $?"
```

### Simple Print Debugging
```runa
# Use return values to debug:
Return debug_value  # Check what value is being calculated
```

### File Debugging
```runa
# Write debug info to file:
Let debug_info be integer_to_string(my_variable)
Let result be runtime_write_file("debug.txt", debug_info)
```

## ⚠️ Common Mistakes

### Don't Forget End Statements
```runa
Process called "test":
    Return 0
End Process  # ← Required!

Type called "Point":
    x as Integer
End Type     # ← Required!
```

### Initialize Before Use
```runa
# Wrong:
Set x to 10

# Right:
Let x be 0
Set x to 10
```

### Math Library Linking
```bash
# Don't forget -lm flag:
gcc -o program program.s runtime_*.o -no-pie -lm
```

## 📖 Example Templates

### Basic Program
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let result be 42
    Return result
End Process
```

### With Custom Type
```runa
Type called "Point":
    x as Integer,
    y as Integer
End Type

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let p be Point
    Set p.x to 10
    Set p.y to 20
    Return p.x plus p.y
End Process
```

### File Processing
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let exists be runtime_file_exists("input.txt")
    If exists equals 0:
        Return 1  # File not found
    End If

    Let content be runtime_read_file("input.txt")
    Let length be string_length(content)

    Let output be string_concat("Length: ", integer_to_string(length))
    Let write_result be runtime_write_file("output.txt", output)

    Return write_result
End Process
```

---

**🎉 Happy Coding with Runa v0.0.7.3!**

*Print this reference and keep it nearby while developing!*