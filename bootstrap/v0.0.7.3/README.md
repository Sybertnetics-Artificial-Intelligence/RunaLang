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
# Runa v0.0.7.3 - Production Ready Compiler

> **Complete, stable Runa compiler ready for team development.**

## 🚀 Quick Start

```bash
# Create your first program
echo 'Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 42
End Process' > hello.runa

# Compile and run
./bin/runac hello.runa hello.s
gcc -o hello hello.s runtime/*.o -no-pie -lm
./hello; echo "Exit code: $?"  # Shows: Exit code: 42
```

## 📁 Directory Structure

```
v0.0.7.3/
├── README.md                 ← This file
├── Makefile                  ← Rebuild system (if needed)
├── bin/
│   └── runac                 ← The Runa compiler
├── runtime/
│   ├── runtime_io.o          ← File I/O functions
│   ├── runtime_string.o      ← String operations
│   ├── runtime_math.o        ← Mathematical functions
│   ├── runtime_list.o        ← List operations
│   └── runtime_system.o      ← System utilities
├── src/                      ← Source code (reference only)
│   ├── main.c                ← Compiler entry point
│   ├── lexer.c/.h            ← Tokenization
│   ├── parser.c/.h           ← Syntax analysis
│   ├── codegen_x86.c/.h      ← Code generation
│   └── runtime_*.c/.h        ← Runtime library source
├── examples/                 ← Working Runa programs
│   ├── test_simple.runa      ← Basic program
│   ├── test_arithmetic.runa  ← Math operations
│   ├── test_function.runa    ← Function definitions
│   └── ...                   ← 50+ examples
└── docs/                     ← Complete documentation
    ├── USER_GUIDE.md         ← Complete tutorial
    ├── CAPABILITIES_REFERENCE.md ← Feature reference
    └── QUICK_REFERENCE.md    ← Daily cheat sheet
```

## 💼 What Teams Need

### Minimum for Development
Your team only needs to copy these files:
- `bin/runac` - The compiler executable
- `runtime/*.o` - Runtime object files
- `docs/QUICK_REFERENCE.md` - Syntax reference

### Recommended for Full Development
Copy the entire `v0.0.7.3/` directory for:
- Complete documentation (`docs/`)
- Working examples (`examples/`)
- Source code reference (`src/`)

## 🛠️ Basic Commands

```bash
# Compile Runa to assembly
./bin/runac program.runa program.s

# Link and create executable
gcc -o program program.s runtime/*.o -no-pie -lm

# Run your program
./program
```

## 📚 Learning Resources

1. **Start here:** `docs/QUICK_REFERENCE.md`
2. **Complete tutorial:** `docs/USER_GUIDE.md`
3. **Feature reference:** `docs/CAPABILITIES_REFERENCE.md`
4. **Working examples:** `examples/` directory

## 🧪 Test Your Setup

```bash
# Test basic functionality
./bin/runac examples/test_simple.runa test.s
gcc -o test test.s runtime/*.o -no-pie -lm
./test; echo "Exit: $?"  # Should show: Exit: 42

# Test arithmetic
./bin/runac examples/test_arithmetic.runa math.s
gcc -o math math.s runtime/*.o -no-pie -lm
./math; echo "Exit: $?"  # Should show: Exit: 30
```

## 🎯 Language Capabilities

### ✅ Fully Working
- **Functions** - Parameters, return values, recursion
- **Variables** - Declaration, assignment, scoping
- **Arithmetic** - All basic math operations
- **Conditionals** - If/Otherwise statements with nesting
- **Loops** - While loops with complex conditions
- **Custom Types** - Struct definition and field access
- **String Operations** - 15+ string manipulation functions
- **File I/O** - Complete file reading/writing system
- **Math Library** - Trigonometry, logarithms, square root

### 🚧 Not Yet Available
- Arrays (use multiple variables)
- For loops (use While loops)
- Modules/imports (single file only)
- Exception handling (use return codes)

## 🔧 Rebuilding (Advanced)

Only needed if modifying the compiler itself:

```bash
make clean
make
```

Most teams will never need to rebuild - the provided `bin/runac` works for all normal development.

## 📞 Documentation

- **`docs/USER_GUIDE.md`** - Complete language tutorial with examples
- **`docs/CAPABILITIES_REFERENCE.md`** - What works, what doesn't, workarounds
- **`docs/QUICK_REFERENCE.md`** - Daily syntax cheat sheet

---

**✅ This compiler is stable, tested, and ready for production use.**

*Start building your Runa projects today! Your code will be forward-compatible with future versions.*