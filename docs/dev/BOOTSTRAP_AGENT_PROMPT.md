# RUNA COMPILER BOOTSTRAP - AGENT DIRECTIVE

## 🎯 YOUR MISSION: v0.1 MICRORUNA SELF-HOSTED COMPILER

You are implementing the **first self-hosted Runa compiler** written entirely in MicroRuna and compiled by the v0.0 Rust seed compiler. This is the critical bootstrap moment that achieves true language independence.

**Primary Objective:** Create `runac-v0.1` that successfully compiles its own source code.

---

## 📊 CURRENT STATUS

**Phase**: 🚀 **v0.1 MICRORUNA COMPILER DEVELOPMENT**
**Base Compiler**: v0.0 Rust Seed (✅ 100% COMPLETE - Production Ready)
**Target Directory**: `/runa/bootstrap/v0.1_microruna-compiler/` (to be created)
**Current Task**: Begin v0.1 foundation setup and project structure

### **v0.0 Completion Status**
✅ **FULLY COMPLETE AND VALIDATED:**
- Complete MicroRuna language support (variables, functions, structs, lists, control flow)
- Full type system with struct validation and field access
- Runtime library (strings, I/O, collections, file operations)
- Memory management with bounds checking and safety
- x86-64 assembly generation with System V ABI compliance
- Security audit completed - all placeholders eliminated
- **Ready for v0.1 bootstrap development**

---

## 📋 THE IMMUTABLE BOOTSTRAP PLAN

**Master Specification**: `/runa/docs/dev/Last_Effort_Compiler_Bootstrapping.md`
**Progress Tracker**: `/runa/docs/dev/Bootstrap_Progress.md`

### **v0.1 Development Strategy**
Following the **PHASE 0.1: MICRORUNA SELF-HOSTED COMPILER** section of the specification:

#### **Stage 1: Foundation Setup (2-3 days)**
- [ ] Create v0.1 project structure
- [ ] Define MicroRuna grammar for compiler implementation
- [ ] Implement skeleton files with minimal stubs
- [ ] Set up build pipeline using v0.0 compiler

#### **Stage 2: Core Translation (5-7 days)**
- [ ] Translate `lexer.rs` → `lexer.runa`
- [ ] Translate `parser.rs` → `parser.runa`
- [ ] Translate `typechecker.rs` → `typechecker.runa`
- [ ] Translate `codegen.rs` → `codegen.runa`

#### **Stage 3: Runtime Integration (3-4 days)**
- [ ] Implement `runtime.runa` with built-in functions
- [ ] Memory management and string operations
- [ ] Assembly integration and error handling

#### **Stage 4: Bootstrap Validation (2-3 days)**
- [ ] Self-compilation test: `runac-v0.1` compiles its own source
- [ ] Output validation and comparison testing
- [ ] Performance optimization and comprehensive testing

### **Success Criteria**
```bash
# The ultimate validation
./runac-v0.1 src/*.runa  # Compiles its own source successfully
```

---

## 🔧 TECHNICAL SPECIFICATIONS

### **MicroRuna Language Subset (v0.1)**
The compiler must support **exactly** these constructs:

**Core Types:**
```runa
Integer, String, Void, List
Type called "CustomType": field as Type End Type
```

**Variables and Functions:**
```runa
Let variable be value
Set variable to new_value

Process called "function_name" that takes param as Type returns Type:
    // implementation
End Process
```

**Control Flow:**
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

**Data Structures:**
```runa
// Struct operations
Let obj be a value of type TypeName with field1 as val1, field2 as val2
Set obj.field1 to new_value
Let val be obj.field2

// List operations
Let my_list be a list containing item1, item2, item3
Let element be my_list[index]
```

**Built-in Functions:**
- String: `length_of`, `char_at`, `substring`, `concat`, `to_string`
- I/O: `read_file`, `write_file`, `print`
- Lists: Basic creation and indexing

### **Translation Guidelines**

**From Rust to MicroRuna:**
- `Vec<T>` → `List` (with manual type tracking)
- `HashMap<K,V>` → `List` of key-value structs
- `match/enum` → `If/Otherwise` chains
- `Result<T,E>` → Return value error conventions
- `struct` → `Type called` definitions
- Methods → `Process called` functions

**Critical Requirements:**
1. **No Placeholders**: Complete implementation only
2. **Reference Compliance**: Match v0.0 behavior exactly
3. **Self-Hosting**: Must compile its own source
4. **Error Handling**: Comprehensive error messages
5. **Memory Safety**: Proper bounds checking

---

## 📁 PROJECT STRUCTURE

### **Target Directory Layout**
```
/runa/bootstrap/v0.1_microruna-compiler/
├── src/
│   ├── main.runa          # Entry point and CLI
│   ├── lexer.runa         # Tokenization
│   ├── parser.runa        # AST generation
│   ├── typechecker.runa   # Type validation
│   ├── codegen.runa       # Assembly generation
│   └── runtime.runa       # Built-in functions
├── tests/
│   ├── unit_tests.runa    # Component testing
│   └── integration_tests.runa # End-to-end testing
├── examples/
│   ├── hello_world.runa   # Basic test
│   └── arithmetic.runa    # Complex test
├── compile.sh             # Build script using v0.0
└── README.md              # Documentation
```

---

## 🚀 IMPLEMENTATION WORKFLOW

### **Reference Implementation**
Use `/runa/bootstrap/v0.0_rust-seed/src/` as your **reference implementation**:
- `lexer.rs` - Tokenization patterns and logic
- `parser.rs` - AST construction and grammar rules
- `typechecker.rs` - Type validation and inference
- `codegen.rs` - x86-64 assembly generation
- Test files - Expected behavior patterns

### **Development Process**
1. **Study Reference**: Understand v0.0 implementation thoroughly
2. **Plan Translation**: Map Rust patterns to MicroRuna equivalents
3. **Implement Incrementally**: Build and test each component
4. **Validate Continuously**: Compare against v0.0 behavior
5. **Integrate Systematically**: Ensure components work together
6. **Test Comprehensively**: Unit tests, integration tests, self-compilation

### **Build Pipeline**
```bash
# Compile v0.1 sources using v0.0
cd /runa/bootstrap/v0.0_rust-seed
./target/debug/runac ../v0.1_microruna-compiler/src/main.runa -o runac-v0.1

# Test self-compilation
./runac-v0.1 ../v0.1_microruna-compiler/src/*.runa -o runac-v0.1-gen2

# Validate outputs match
diff runac-v0.1 runac-v0.1-gen2  # Should be identical
```

---

## ⚠️ CRITICAL COMPLIANCE RULES

### **Mandatory Requirements**
1. **Complete Implementation Only**: No TODOs, placeholders, or incomplete logic
2. **Specification Compliance**: Follow Last_Effort_Compiler_Bootstrapping.md exactly
3. **Reference Behavior**: Match v0.0 compiler behavior precisely
4. **Self-Hosting Capable**: Must successfully compile its own source code
5. **Production Quality**: Comprehensive error handling and validation

### **Forbidden Actions**
- Creating placeholder implementations or stubs (except skeleton phase)
- Deviating from the specification without approval
- Adding features not required for self-hosting
- Using external dependencies beyond v0.0 compiler
- Implementing incomplete or "simplified" versions of algorithms

### **Success Validation**
The v0.1 compiler is only complete when:
- [ ] All MicroRuna constructs are supported
- [ ] Self-compilation test passes successfully
- [ ] Generated executable functions correctly
- [ ] Performance is acceptable (<60 seconds compilation)
- [ ] Comprehensive test suite passes

---

## 📚 DEVELOPMENT RESOURCES

**Documentation:**
- Master specification: `Last_Effort_Compiler_Bootstrapping.md`
- Progress tracking: `Bootstrap_Progress.md`
- Reference implementation: `/runa/bootstrap/v0.0_rust-seed/src/`

**Tools:**
- v0.0 compiler: `./target/debug/runac file.runa -o output`
- Standard assembly tools: `as`, `ld`
- Testing infrastructure from v0.0 project

**Validation:**
- Use v0.0 test cases as behavior benchmarks
- Reference v0.0 assembly output for correctness
- Continuous integration with self-compilation testing

---

Remember: This is the **crucial bootstrap moment**. Success here establishes true self-hosting and independence. Every component must be complete, correct, and production-ready. No shortcuts, no placeholders - only working, self-hosting code.