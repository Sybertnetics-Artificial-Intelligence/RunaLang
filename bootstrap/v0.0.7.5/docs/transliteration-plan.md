# Complete Line-for-Line Transliteration Plan: v0.0.7.3 → v0.0.7.5

## **Executive Summary**

This document outlines the comprehensive plan for transliterating the entire v0.0.7.3 C compiler codebase to Runa v0.0.7.5. This is **NOT** a reimplementation or stub creation - this is a complete, line-for-line translation that preserves every algorithm, edge case, and behavior from the original C implementation.

## **Codebase Analysis**

### **Scope Summary**
- **Total C code to transliterate**: 6,384 lines
- **Core compiler pipeline**: 4,481 lines (lexer, parser, codegen, main)
- **Support utilities**: 1,903 lines (string_utils, containers, hashtable)
- **Runtime libraries**: 2,375 lines (remain as C, copied to runtime/)
- **144 token types** requiring exact preservation
- **Complex AST structures** requiring faithful translation

### **File Breakdown**
```
TRANSLITERATE TO RUNA:
├── Core Compiler (4,481 LOC)
│   ├── main.c (64 LOC) → src/main.runa
│   ├── lexer.c (457 LOC) → src/lexer.runa
│   ├── parser.c (2,000 LOC) → src/parser.runa
│   └── codegen_x86.c (1,960 LOC) → src/codegen.runa
├── Utilities (1,903 LOC)
│   ├── string_utils.c (769 LOC) → src/string_utils.runa
│   ├── containers.c (766 LOC) → src/containers.runa
│   └── hashtable.c (368 LOC) → src/hashtable.runa

COPY TO RUNTIME (remain C):
├── runtime_io.c/h → runtime/
├── runtime_list.c/h → runtime/
├── runtime_math.c/h → runtime/
├── runtime_string.c/h → runtime/
└── runtime_system.c/h → runtime/
```

## **Phase 1: Infrastructure Setup**

### **1.1 Directory Structure**
```
v0.0.7.5/
├── docs/           (this documentation)
├── src/            (Runa compiler source)
├── runtime/        (C runtime libraries)
├── tests/          (test cases)
├── build/          (build artifacts)
├── Makefile        (build system)
└── build.sh        (build script)
```

### **1.2 Runtime Library Setup**
- **Copy** all `runtime_*.c/h` files to `runtime/` directory
- **No changes** to runtime - remains pure C for performance
- **Link** runtime libraries with compiled Runa code

### **1.3 Build System Configuration**
- **Update Makefile** for mixed C/Runa compilation
- **Configure linking** between Runa compiler and C runtime
- **Test basic compilation pipeline**

## **Phase 2: Utility Layer Transliteration (1,903 LOC)**

**Dependency Order: Foundation First, No Shortcuts**

### **2.1 String Utilities (769 LOC)**
**File**: `string_utils.c` → `src/string_utils.runa`

**Key Components**:
- **StringBuilder**: Dynamic string building with capacity management
- **String manipulation**: Format, join, split operations
- **Memory management**: Proper allocation/deallocation patterns
- **Edge cases**: Null handling, empty strings, buffer overflows

**Critical Requirements**:
- **Every function** must work identically to C version
- **Memory safety** through proper allocate/deallocate
- **Performance** must match C implementation
- **No shortcuts** in buffer management logic

### **2.2 Hash Table (368 LOC)**
**File**: `hashtable.c` → `src/hashtable.runa`

**Key Components**:
- **Hash function**: Exact same algorithm as C version
- **Collision handling**: Chain-based resolution
- **Dynamic resizing**: Growth/shrink logic preservation
- **Key/value management**: String and generic value support

**Critical Requirements**:
- **Hash distribution** must be identical
- **Collision resolution** behavior preserved
- **Resize triggers** and growth factors exact
- **Memory layout** compatible with expected usage

### **2.3 Containers (766 LOC)**
**File**: `containers.c` → `src/containers.runa`

**Key Components**:
- **Dynamic arrays**: Automatic resizing, capacity management
- **Generic collections**: Type-agnostic container operations
- **Iterator support**: Traversal and modification patterns
- **Bulk operations**: Insert, delete, search algorithms

**Critical Requirements**:
- **Capacity growth** algorithm identical
- **Index bounds** checking preserved
- **Iterator semantics** maintained
- **Bulk operation** efficiency preserved

## **Phase 3: Core Compiler Transliteration (4,481 LOC)**

**Pipeline Order: Lexer → Parser → Codegen → Main**

### **3.1 Lexer (457 LOC)**
**File**: `lexer.c` → `src/lexer.runa`

**Key Components**:
- **144 token types** with exact recognition patterns
- **Keyword tables**: All Runa language keywords
- **Number parsing**: Integer literal handling
- **String parsing**: Escape sequence processing
- **Position tracking**: Line/column information
- **Error handling**: Lexical error reporting

**Critical Requirements**:
- **Token stream** must be byte-identical to C version
- **Keyword recognition** patterns preserved exactly
- **Number parsing** edge cases (overflow, malformed)
- **String escape** sequences handled identically
- **Error messages** must match C version exactly

### **3.2 Parser (2,000 LOC)**
**File**: `parser.c` → `src/parser.runa`

**Key Components**:
- **AST node types**: All expression/statement structures
- **Recursive descent**: Parsing algorithm preservation
- **Precedence handling**: Operator precedence tables
- **Type checking**: Basic semantic validation
- **Error recovery**: Parser error handling
- **Memory management**: AST construction/destruction

**Critical Requirements**:
- **AST structure** must be identical for codegen compatibility
- **Parsing precedence** rules preserved exactly
- **Error recovery** behavior maintained
- **Type checking** logic replicated precisely
- **Memory patterns** for AST nodes preserved

### **3.3 Code Generator (1,960 LOC)**
**File**: `codegen_x86.c` → `src/codegen.runa`

**Key Components**:
- **x86-64 assembly**: Complete instruction set usage
- **Register allocation**: Temporary and preserved registers
- **Stack management**: Frame setup, local variables
- **Function calls**: Calling convention compliance
- **Control flow**: Jumps, labels, conditionals
- **Memory operations**: Load/store patterns

**Critical Requirements**:
- **Assembly output** must be byte-identical to C version
- **Register usage** patterns preserved
- **Stack frame** layout identical
- **Jump targets** and labels consistent
- **Optimization** patterns maintained

### **3.4 Main Compiler (64 LOC)**
**File**: `main.c` → `src/main.runa`

**Key Components**:
- **CLI argument** parsing
- **File I/O** coordination
- **Pipeline orchestration**: lexer → parser → codegen
- **Error handling**: Top-level error reporting
- **Resource cleanup**: Memory management

**Critical Requirements**:
- **CLI interface** identical to C version
- **Error messages** match exactly
- **Exit codes** preserved
- **Resource cleanup** behavior maintained

## **Phase 4: Build System Integration**

### **4.1 Makefile Updates**
- **Add Runa compilation** targets
- **Link C runtime** libraries
- **Dependency management** for mixed compilation
- **Test targets** for validation

### **4.2 Linking Strategy**
- **Runtime functions** callable from Runa
- **Memory model** compatibility between C and Runa
- **ABI compliance** for function calls

### **4.3 Build Validation**
- **Compile v0.0.7.5** compiler successfully
- **Test basic compilation** of simple programs
- **Verify runtime** integration works

## **Phase 5: Testing & Validation**

### **5.1 Unit Testing**
- **Component tests** for each transliterated module
- **Function-level** behavior verification
- **Edge case** coverage matching C version
- **Memory leak** detection

### **5.2 Integration Testing**
- **Pipeline tests** for full compilation flow
- **Regression tests** against v0.0.7.3 output
- **Assembly comparison** for identical output
- **Performance benchmarks** vs C version

### **5.3 Bootstrap Testing**
- **Self-compilation**: v0.0.7.5 compiling itself
- **Output verification**: Identical assembly generation
- **Iterative bootstrap** for stability verification

## **Critical Success Criteria**

### **Functional Requirements**
- ✅ **Every function works** - no placeholders or stubs
- ✅ **Identical behavior** - same algorithms, edge cases, errors
- ✅ **Compatible output** - assembly must be byte-identical
- ✅ **Memory safety** - proper allocation/deallocation
- ✅ **Performance** - no significant slowdown vs C

### **Quality Requirements**
- ✅ **Complete implementation** - every line translated
- ✅ **Error handling** - all error paths preserved
- ✅ **Edge cases** - boundary conditions maintained
- ✅ **Documentation** - code behavior documented

### **Integration Requirements**
- ✅ **Bootstrap capability** - self-compilation works
- ✅ **Runtime integration** - C libraries linked properly
- ✅ **Build system** - clean compilation process
- ✅ **Testing** - comprehensive validation suite

## **Timeline Estimation**

### **Detailed Breakdown**
- **Phase 1** (Infrastructure): 2 hours
- **Phase 2** (Utilities): 3-4 days (1,903 LOC)
  - String utilities: 1.5 days
  - Hash table: 0.5 days
  - Containers: 1-2 days
- **Phase 3** (Core Compiler): 7-10 days (4,481 LOC)
  - Lexer: 1-2 days
  - Parser: 4-5 days
  - Codegen: 3-4 days
  - Main: 0.5 days
- **Phase 4** (Build Integration): 1-2 days
- **Phase 5** (Testing): 2-3 days

**Total Estimated Time**: 14-19 days

### **Risk Factors**
- **Complex AST structures** may require additional debugging
- **Assembly generation** edge cases may be tricky
- **Memory management** patterns may need iteration
- **Runtime integration** may have linking challenges

## **Success Metrics**

1. **Functional Completion**: 100% of functions implemented and working
2. **Output Compatibility**: Assembly output byte-identical to v0.0.7.3
3. **Bootstrap Success**: v0.0.7.5 successfully compiles itself
4. **Test Coverage**: All existing tests pass with new compiler
5. **Performance**: <20% slowdown compared to C version

## **Documentation Deliverables**

This plan will be supplemented with:
- **transliteration-progress.md** - Daily progress tracking
- **api-mapping.md** - C to Runa function mappings
- **build-instructions.md** - Compilation and build process
- **testing-strategy.md** - Validation and testing approach
- **troubleshooting.md** - Common issues and solutions

---

**This is not a rewrite or reimplementation. This is a complete, faithful, line-for-line transliteration preserving every detail of the original C compiler.**