# Rust Bootstrap Roadmap for Runa

## Executive Summary

After discovering that our Assembly-based Genesis compiler locks us to x86-64 Linux only, we're pivoting to a Rust-based bootstrap strategy that provides immediate cross-platform support while maintaining our goal of eventual self-hosting.

## Why Rust Instead of Assembly?

### Assembly Approach Problems:
- **Platform Lock-in**: Each architecture needs complete rewrite (1000+ lines each)
- **No Windows/macOS**: Different syscall conventions per OS
- **Development Speed**: Assembly is 10x slower to write/debug
- **Limited Contributors**: Few developers know Assembly well
- **Years to Market**: Would delay Runa adoption significantly

### Rust Bootstrap Benefits:
- **Instant Cross-Platform**: Single codebase → all architectures
- **All Operating Systems**: Windows, macOS, Linux, BSD work immediately  
- **Fast Development**: Rust is high-level with great tooling
- **Community Accessible**: Many developers can contribute
- **Months to Market**: Production-ready much sooner

## Bootstrap Progression

### Runa 0.1: Rust Bootstrap Compiler
**Timeline**: Weeks 1-2  
**Language**: 100% Rust
**Output**: Native (via LLVM) + WASM

**Components**:
- Lexer (logos crate for speed)
- Parser (hand-written recursive descent)
- Type Checker (bidirectional type checking)
- IR Builder (SSA-based intermediate representation)
- LLVM Backend (native code generation)
- WASM Backend (direct WASM generation)

**Capabilities**:
- Full Runa syntax support
- Cross-compilation to any target
- Optimization via LLVM
- Fast compilation times

### Runa 0.2: Partial Self-Hosting
**Timeline**: Weeks 3-4  
**Language**: 60% Runa, 40% Rust
**Architecture**: Runa frontend, Rust backend

**Runa Components**:
- Lexer (ported from Rust)
- Parser (ported from Rust)
- Type System (ported from Rust)
- AST transformations
- Error reporting

**Rust Components** (temporary):
- LLVM interface (complex FFI)
- File I/O (until Runa stdlib ready)
- Memory management (bootstrap only)

### Runa 1.0: Full Self-Hosting
**Timeline**: Weeks 5-6  
**Language**: 100% Runa
**Achievement**: Runa compiles itself

**Complete Migration**:
- LLVM bindings in Runa (via FFI)
- Or initial native code generator
- Full standard library
- Complete toolchain in Runa

**Validation**:
```bash
# The critical test
./runa_0.2 compiler.runa -o runa_1.0
./runa_1.0 compiler.runa -o runa_1.0_v2
diff runa_1.0 runa_1.0_v2  # Must be identical!
```

### Runa 2.0: Beyond LLVM
**Timeline**: Month 2+  
**Language**: 100% Runa with custom backends
**Achievement**: No external dependencies

**Custom Backends**:
- Direct x86-64 machine code
- Direct ARM64 machine code
- Direct WASM generation
- Direct RISC-V support

**AOTT Integration**:
- Profile-guided optimization
- Multi-tier compilation
- Runtime specialization

## Implementation Plan

### Week 1: Rust Lexer & Parser
```rust
// bootstrap/runa-bootstrap/src/lexer.rs
pub fn tokenize(source: &str) -> Result<Vec<Token>, LexError> {
    // Use logos for fast lexing
    let lex = Token::lexer(source);
    lex.spanned()
       .map(|(tok, span)| ...)
       .collect()
}

// bootstrap/runa-bootstrap/src/parser.rs  
pub fn parse(tokens: Vec<Token>) -> Result<AST, ParseError> {
    // Recursive descent parser
    Parser::new(tokens).parse_program()
}
```

### Week 2: Type Checker & LLVM Backend
```rust
// bootstrap/runa-bootstrap/src/type_checker.rs
pub fn check(ast: AST) -> Result<TypedAST, TypeError> {
    // Bidirectional type checking with inference
    TypeChecker::new().check_program(ast)
}

// bootstrap/runa-bootstrap/src/llvm_backend.rs
pub fn compile(ast: TypedAST) -> Result<ObjectFile, CompileError> {
    // Generate LLVM IR and compile to native
    LLVMCodegen::new().generate(ast)
}
```

### Week 3: Begin Runa Frontend
```runa
Note: Port lexer from Rust to Runa
Process called "tokenize" that takes source as String returns List[Token]:
    Let tokens be empty_list()
    Let position be 0
    
    While position < length(source):
        Let token be next_token(source, position)
        tokens.append(token)
        position = token.end_position
    End While
    
    Return tokens
End Process
```

### Week 4: Runa-Rust Bridge
```runa
Note: FFI interface to call Rust backend from Runa frontend
External Process called "rust_compile_to_llvm" that takes ast as AST returns ByteArray

Process called "compile" that takes source as String returns ByteArray:
    Let tokens be tokenize(source)
    Let ast be parse(tokens)
    Let typed_ast be type_check(ast)
    
    Note: Call into Rust for LLVM compilation (temporary)
    Return rust_compile_to_llvm(typed_ast)
End Process
```

### Week 5-6: Complete Self-Hosting
- Port remaining Rust components to Runa
- Implement LLVM bindings in Runa
- Or write initial native code generator
- Validate self-compilation
- **Note**: The full compiler lives in `src/compiler/` with complete structure:
  - `frontend/` (lexer, parser, semantic analysis)
  - `middle/` (IR, optimizations, transformations)
  - `backend/` (code generation, LLVM/native)
  - `driver/` (compilation orchestration)
  - `services/` (LSP, tooling)

## File Structure

```
runa/
├── bootstrap/
│   ├── runa-bootstrap/          # Rust bootstrap (Runa 0.1)
│   │   ├── Cargo.toml
│   │   ├── src/
│   │   │   ├── main.rs
│   │   │   ├── lexer.rs
│   │   │   ├── parser.rs
│   │   │   ├── type_checker.rs
│   │   │   ├── ir_builder.rs
│   │   │   ├── llvm_backend.rs
│   │   │   └── wasm_backend.rs
│   │   └── tests/
│   │
│   ├── partial-runa/            # Partial self-hosting (Runa 0.2)
│   │   ├── lexer.runa          # Runa lexer
│   │   ├── parser.runa         # Runa parser
│   │   ├── type_checker.runa   # Runa type system
│   │   └── rust_bridge.runa    # FFI to Rust backend
│   │
│   └── self-hosted/             # Full self-hosting (Runa 1.0)
│       └── (uses src/compiler/) # Points to full compiler structure
```

## Success Criteria

### Runa 0.1
- [ ] Compiles test programs on x86-64, ARM64, WASM
- [ ] Passes all language feature tests
- [ ] Generates optimized code via LLVM
- [ ] Fast compilation (<1s for small programs)

### Runa 0.2  
- [ ] Runa frontend successfully parses all Runa code
- [ ] Type system implemented in Runa
- [ ] Can compile simple programs through Rust backend
- [ ] Maintains cross-platform support

### Runa 1.0
- [ ] Compiles itself successfully
- [ ] Generated compiler is byte-identical when self-compiling
- [ ] No Rust code remains in compiler
- [ ] Performance matches or exceeds Rust version

### Runa 2.0
- [ ] Direct machine code generation without LLVM
- [ ] AOTT system fully integrated
- [ ] Faster than all major compilers
- [ ] Zero external dependencies

## Advantages Over Assembly Bootstrap

| Aspect | Assembly Bootstrap | Rust Bootstrap |
|--------|-------------------|----------------|
| Development Time | 6-12 months | 6-8 weeks |
| Platform Support | x86-64 Linux only | All platforms immediately |
| Lines of Code | ~5000 (with ports) | ~2000 total |
| Contributors | Assembly experts only | Any Rust developer |
| Debugging | Extremely difficult | Standard tools work |
| Testing | Manual, platform-specific | Automated, cross-platform |
| Community Adoption | Limited | Immediate |

## Conclusion

The Rust bootstrap approach maintains our vision of a self-hosted Runa while being:
- **10x faster to implement**
- **Immediately cross-platform**
- **More maintainable**
- **Community-friendly**

This pivot from Assembly to Rust for bootstrapping is not a compromise—it's a strategic decision that gets Runa to market faster while achieving all our technical goals.

● Recommended Build Order for Partial-Runa Directory

  Based on dependencies and the compilation pipeline flow, here's the optimal build order:

  Phase 1: Foundation Layer (Week 1)

  1. core_libs.runa - FIRST
  - No dependencies on other partial-runa files
  - Provides basic data structures (Array, Dictionary, Stream, ByteArray)
  - Everything else needs these primitives

  2. diagnostic_system.runa - SECOND
  - Only depends on core_libs
  - Needed by all other components for error reporting
  - Must be ready before any parsing/analysis begins

  Phase 2: Frontend (Week 1-2)

  3. parser_frontend.runa - THIRD
  - Depends on core_libs and diagnostic_system
  - Produces AST needed by everything downstream
  - Lexer + Parser must work before any analysis

  Phase 3: Analysis (Week 2)

  4. semantic_analyzer.runa - FOURTH
  - Depends on parser_frontend for AST
  - Produces symbol table needed by type checker
  - Must complete before type checking

  5. type_system.runa - FIFTH
  - Depends on semantic_analyzer for symbols
  - Works closely with semantic analysis
  - Produces typed AST for IR generation

  Phase 4: Code Generation (Week 3)

  6. ir_builder.runa - SIXTH
  - Depends on typed AST from type_system
  - Transforms AST to IR
  - Must complete before backend interface

  7. codegen_interface.runa - SEVENTH
  - Depends on IR from ir_builder
  - Interfaces with Rust backend
  - Prepares for FFI bridge

  8. compiler_bridge.runa - EIGHTH
  - Depends on codegen_interface
  - FFI to Rust backend
  - Final connection to code generation

  Phase 5: Orchestration (Week 3-4)

  9. compiler_driver.runa - LAST
  - Depends on ALL other components
  - Orchestrates the entire pipeline
  - Must be built last

  Critical Path Dependencies:

  core_libs → diagnostic_system → parser_frontend → semantic_analyzer → type_system → ir_builder → codegen_interface → 
  compiler_bridge → compiler_driver

  Testing Strategy:

  After each component:
  1. Test with simple Runa programs
  2. Verify output/data structures are correct
  3. Ensure clean interface with next component
  4. Fix issues before moving to next
  **Tests go into the partial-runa/tests directory**

  Integration test points:
  - After parser_frontend: Can parse test programs
  - After type_system: Can analyze and type-check
  - After compiler_bridge: Can generate code via Rust
  - After compiler_driver: Full compilation works



  Adding More Runtime Functions

  To add more functions to the runtime, you need to work in two places:

  1. Runa Side (Function Declarations)

  Add external function declarations in your .runa files:
  External Process called "function_name" that takes param as Type returns 
  ReturnType

  Examples:
  External Process called "rust_string_concat" that takes left as String, right     
  as String returns String
  External Process called "rust_array_new" that takes element_size as Integer,      
  capacity as Integer returns Integer
  External Process called "rust_malloc" that takes size as Integer returns
  Integer

  2. Rust Side (Function Implementations)

  Add corresponding implementations in src/runtime.rs:
  #[no_mangle]
  pub extern "C" fn function_name(params) -> return_type {
      // Implementation
  }

  Key Points:
  - Function names must match exactly between Runa declaration and Rust
  implementation
  - Use #[no_mangle] to prevent name mangling
  - Use extern "C" for C ABI compatibility
  - Handle null pointers and error cases safely
  - String parameters come as *const c_char, return strings as *mut c_char

  Type Mapping Reference:

  - Runa String ↔ Rust *const c_char (input) or *mut c_char (output)
  - Runa Integer ↔ Rust i64
  - Runa Float ↔ Rust f64
  - Runa Boolean ↔ Rust bool

  The compiler now correctly handles the type conversions and parameter passing     
  for all these cases.