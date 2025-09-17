# 🚀 MicroRuna v0.1 Self-Hosted Compiler

**The First Self-Hosted Runa Compiler - Written in MicroRuna**

This is the **critical bootstrap moment** that achieves true language independence for Runa. The v0.1 compiler is written entirely in MicroRuna and compiled by the v0.0 Rust seed compiler, creating the first self-hosted Runa compiler capable of compiling its own source code.

## 🎯 Mission Statement

**Primary Objective:** Create `runac-v0.1` that successfully compiles its own source code, establishing the foundation for all future Runa compiler development.

## 📊 Project Status

- **Phase:** v0.1 MicroRuna Self-Hosted Compiler Development
- **Base Compiler:** v0.0 Rust Seed (✅ 100% Complete)
- **Current Stage:** Stage 1 - Foundation Setup (✅ Complete)
- **Next Stage:** Stage 2 - Core Translation Implementation

## 🏗️ Project Structure

```
v0.1_microruna-compiler/
├── src/                     # Compiler source code (MicroRuna)
│   ├── main.runa           # Entry point and CLI handling
│   ├── lexer.runa          # Tokenization engine
│   ├── parser.runa         # AST generation
│   ├── typechecker.runa    # Type validation and inference
│   ├── codegen.runa        # x86-64 assembly generation
│   └── runtime.runa        # Built-in functions and system interface
├── tests/                   # Comprehensive test suite
│   ├── unit_tests.runa     # Component-level testing
│   └── integration_tests.runa # End-to-end compilation testing
├── examples/               # Example MicroRuna programs
│   ├── hello_world.runa    # Basic language demonstration
│   └── arithmetic.runa     # Complex mathematical operations
├── build/                  # Compilation artifacts (created by build)
├── compile.sh              # Build script using v0.0 compiler
└── README.md               # This documentation
```

## 🔧 Technical Specifications

### MicroRuna Language Subset (v0.1)

The v0.1 compiler supports exactly these MicroRuna constructs:

#### Core Types
- `Integer` - 64-bit signed integers
- `String` - UTF-8 text strings
- `Void` - Function return type for no value
- `List` - Dynamic arrays
- Custom types via `Type called "TypeName"`

#### Variables and Assignment
```runa
Let variable be value
Set variable to new_value
```

#### Functions
```runa
Process called "function_name" that takes param as Type returns Type:
    // implementation
End Process
```

#### Control Flow
```runa
If condition:
    // statements
Otherwise:
    // alternative
End If

While condition:
    // statements
End While
```

#### Data Structures
```runa
// Struct operations
Let obj be a value of type TypeName with field1 as val1, field2 as val2
Set obj.field1 to new_value
Let val be obj.field2

// List operations
Let my_list be a list containing item1, item2, item3
Let element be my_list[index]
```

#### Built-in Functions
- **String:** `length_of`, `char_at`, `substring`, `concat`, `to_string`
- **I/O:** `read_file`, `write_file`, `print_string`
- **Lists:** Basic creation and indexing
- **System:** Command execution and runtime utilities

## 🚀 Getting Started

### Prerequisites

- v0.0 Rust seed compiler (must be built first)
- GCC for assembly and linking
- Linux x86-64 environment

### Building the v0.1 Compiler

1. **Ensure v0.0 compiler is ready:**
   ```bash
   cd ../v0.0_rust-seed
   cargo build
   cd ../v0.1_microruna-compiler
   ```

2. **Build the v0.1 compiler:**
   ```bash
   chmod +x compile.sh
   ./compile.sh
   ```

3. **Verify successful build:**
   ```bash
   ls -la build/runac-v0.1
   ```

### Using the v0.1 Compiler

```bash
# Compile a MicroRuna program
./build/runac-v0.1 examples/hello_world.runa hello_world

# Run the compiled program
./hello_world
```

## 🧪 Testing

### Unit Tests
Test individual compiler components:
```bash
# Using v0.0 to compile and run unit tests
../v0.0_rust-seed/target/debug/runac tests/unit_tests.runa unit_tests
./unit_tests
```

### Integration Tests
Test complete compilation pipeline:
```bash
# Using v0.0 to compile and run integration tests
../v0.0_rust-seed/target/debug/runac tests/integration_tests.runa integration_tests
./integration_tests
```

### Self-Compilation Test (The Ultimate Validation)
```bash
# Attempt to compile v0.1 source with v0.1 compiler
./build/runac-v0.1 src/main.runa runac-v0.1-gen2

# If successful, compare outputs
diff build/runac-v0.1 runac-v0.1-gen2
```

## 📚 Examples

### Hello World
```runa
Let message be "Hello, World!"
call print_string(message)
```

### Function Definition
```runa
Process called "add" that takes a as Integer and b as Integer returns Integer:
    Return a plus b
End Process

Let result be call add(10, 20)
call print_string(to_string(result))
```

### Control Flow
```runa
Let x be 5
If x is greater than 3:
    call print_string("x is large")
Otherwise:
    call print_string("x is small")
End If
```

## 🔄 Development Workflow

### Stage 1: Foundation Setup ✅
- [x] Project structure creation
- [x] MicroRuna grammar definition
- [x] Skeleton file implementation
- [x] Build pipeline setup

### Stage 2: Core Translation 🔄
- [ ] Translate `lexer.rs` → `lexer.runa`
- [ ] Translate `parser.rs` → `parser.runa`
- [ ] Translate `typechecker.rs` → `typechecker.runa`
- [ ] Translate `codegen.rs` → `codegen.runa`

### Stage 3: Runtime Integration
- [ ] Implement `runtime.runa` with built-in functions
- [ ] Memory management and string operations
- [ ] Assembly integration and error handling

### Stage 4: Bootstrap Validation
- [ ] Self-compilation test
- [ ] Output validation and comparison testing
- [ ] Performance optimization

## 🎯 Success Criteria

The v0.1 compiler is complete when:

- [ ] All MicroRuna constructs are supported
- [ ] Self-compilation test passes: `./runac-v0.1 src/*.runa`
- [ ] Generated executable functions correctly
- [ ] Performance is acceptable (<60 seconds compilation)
- [ ] Comprehensive test suite passes

## 🛠️ Translation Guidelines

### From Rust to MicroRuna

| Rust Construct | MicroRuna Equivalent |
|----------------|---------------------|
| `Vec<T>` | `List` (with manual type tracking) |
| `HashMap<K,V>` | `List` of key-value structs |
| `match/enum` | `If/Otherwise` chains |
| `Result<T,E>` | Return value error conventions |
| `struct` | `Type called` definitions |
| Methods | `Process called` functions |

### Critical Requirements

1. **No Placeholders:** Complete implementation only
2. **Reference Compliance:** Match v0.0 behavior exactly
3. **Self-Hosting:** Must compile its own source
4. **Error Handling:** Comprehensive error messages
5. **Memory Safety:** Proper bounds checking

## 📖 Architecture Overview

### Compilation Pipeline

```
Source Code
    ↓
Lexer (Tokenization)
    ↓
Parser (AST Generation)
    ↓
TypeChecker (Validation)
    ↓
CodeGenerator (x86-64 Assembly)
    ↓
GCC (Assemble & Link)
    ↓
Executable
```

### Key Components

- **Lexer:** Converts source text into tokens
- **Parser:** Builds Abstract Syntax Tree (AST)
- **TypeChecker:** Validates types and semantics
- **CodeGenerator:** Produces x86-64 assembly
- **Runtime:** Provides built-in functions

## 🔗 Related Documentation

- **Master Specification:** `/runa/docs/dev/Last_Effort_Compiler_Bootstrapping.md`
- **Progress Tracking:** `/runa/docs/dev/Bootstrap_Progress.md`
- **Reference Implementation:** `/runa/bootstrap/v0.0_rust-seed/src/`

## ⚠️ Important Notes

### Compliance Rules

- **Complete Implementation Only:** No TODOs, placeholders, or incomplete logic
- **Specification Compliance:** Follow bootstrap specification exactly
- **Reference Behavior:** Match v0.0 compiler behavior precisely
- **Production Quality:** Comprehensive error handling and validation

### Forbidden Actions

- Creating placeholder implementations (except during skeleton phase)
- Deviating from specification without approval
- Adding features not required for self-hosting
- Using external dependencies beyond v0.0 compiler

## 🏆 Bootstrap Achievement

**This is the crucial bootstrap moment.** Success here establishes true self-hosting and independence. Every component must be complete, correct, and production-ready.

The ultimate validation:
```bash
./runac-v0.1 src/*.runa runac-v0.1-gen2  # Success = Bootstrap Complete!
```

## 🤝 Contributing

This is a critical bootstrap project. All changes must:

1. Maintain complete implementation (no placeholders)
2. Follow MicroRuna syntax exactly
3. Pass all tests before submission
4. Preserve self-compilation capability

---

**Remember:** This compiler will birth itself. Every line of code matters. No shortcuts, no placeholders - only working, self-hosting code that can compile its own source and establish true language independence.

🚀 **The future of Runa starts here!**