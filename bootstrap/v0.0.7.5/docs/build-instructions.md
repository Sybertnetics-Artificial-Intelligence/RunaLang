# Build Instructions: Runa v0.0.7.5 Compiler

## **Overview**

This document describes how to build the v0.0.7.5 Runa compiler, which combines Runa source code for the compiler logic with C runtime libraries for system operations.

## **Prerequisites**

### **Required Tools**
- **GCC** 7.0 or later (C compiler for runtime libraries)
- **Make** (build system)
- **Runa v0.0.7.3** compiler (for bootstrapping v0.0.7.5)
- **GNU Assembler** (for linking generated assembly)
- **GNU Linker** (for creating final executable)

### **System Requirements**
- **Linux** x86-64 (primary target)
- **WSL** (Windows Subsystem for Linux) supported
- **macOS** x86-64 (experimental)

## **Directory Structure**

```
v0.0.7.5/
├── Makefile              # Main build script
├── build.sh             # Build automation script
├── docs/                # Documentation
├── src/                 # Runa compiler source
│   ├── main.runa        # Compiler entry point
│   ├── lexer.runa       # Tokenization
│   ├── parser.runa      # AST construction
│   ├── codegen.runa     # Code generation
│   ├── string_utils.runa # String utilities
│   ├── containers.runa  # Data structures
│   └── hashtable.runa   # Hash table implementation
├── runtime/             # C runtime libraries
│   ├── runtime_io.c/h   # File I/O operations
│   ├── runtime_list.c/h # List operations
│   ├── runtime_math.c/h # Mathematical functions
│   ├── runtime_string.c/h # String operations
│   └── runtime_system.c/h # System operations
├── tests/               # Test cases
└── build/               # Build artifacts
```

## **Build Process**

### **Phase 1: Runtime Library Compilation**

```bash
# Compile C runtime libraries
make runtime
```

This creates:
- `build/runtime_io.o`
- `build/runtime_list.o`
- `build/runtime_math.o`
- `build/runtime_string.o`
- `build/runtime_system.o`

### **Phase 2: Runa Compiler Compilation**

```bash
# Compile Runa source to assembly
make runa-compile
```

This process:
1. **Uses v0.0.7.3** to compile each `.runa` file to `.s` assembly
2. **Assembles** each `.s` file to `.o` object file
3. **Creates** object files in `build/` directory

Generated files:
- `build/main.o`
- `build/lexer.o`
- `build/parser.o`
- `build/codegen.o`
- `build/string_utils.o`
- `build/containers.o`
- `build/hashtable.o`

### **Phase 3: Linking**

```bash
# Link all object files
make link
```

This creates:
- `build/runac` - The v0.0.7.5 Runa compiler executable

### **Complete Build**

```bash
# Build everything
make all

# Or use build script
./build.sh
```

## **Makefile Targets**

### **Primary Targets**
- `make all` - Complete build process
- `make clean` - Remove build artifacts
- `make test` - Run test suite
- `make install` - Install compiler (optional)

### **Component Targets**
- `make runtime` - Compile C runtime libraries only
- `make runa-compile` - Compile Runa source only
- `make link` - Link final executable only

### **Development Targets**
- `make debug` - Build with debug symbols
- `make verbose` - Verbose build output
- `make check` - Static analysis and validation

## **Build Configuration**

### **Compiler Settings**

```makefile
# C compiler settings
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2

# Runa compiler settings
RUNAC_V0073 = ../v0.0.7.3/runac
RUNAC_FLAGS = --emit-asm-only

# Assembler settings
AS = as
ASFLAGS = --64

# Linker settings
LD = gcc
LDFLAGS = -o
```

### **Debug Build**

```bash
# Build with debug information
make debug

# Or set debug flags
CFLAGS="-g -O0 -DDEBUG" make all
```

### **Optimization Levels**

```bash
# Development build (faster compilation)
CFLAGS="-O0 -g" make all

# Production build (optimized)
CFLAGS="-O2 -DNDEBUG" make all

# Performance build (maximum optimization)
CFLAGS="-O3 -march=native" make all
```

## **Dependencies**

### **Build Dependencies**
The build process requires these dependencies in order:

1. **C runtime libraries** - No dependencies
2. **Runa utilities** - Depend on runtime libraries at link time
3. **Runa compiler core** - Depends on utilities
4. **Final linking** - Depends on all object files

### **Makefile Dependency Graph**

```makefile
# Runtime libraries (C)
runtime: runtime_io.o runtime_list.o runtime_math.o runtime_string.o runtime_system.o

# Runa utilities
string_utils.o: src/string_utils.runa
hashtable.o: src/hashtable.runa string_utils.o
containers.o: src/containers.runa hashtable.o

# Runa compiler core
lexer.o: src/lexer.runa string_utils.o containers.o
parser.o: src/parser.runa lexer.o containers.o hashtable.o
codegen.o: src/codegen.runa parser.o string_utils.o
main.o: src/main.runa lexer.o parser.o codegen.o

# Final executable
runac: main.o lexer.o parser.o codegen.o string_utils.o containers.o hashtable.o $(RUNTIME_OBJECTS)
```

## **Testing**

### **Unit Tests**

```bash
# Run component tests
make test-units
```

Tests individual components:
- String utilities functionality
- Hash table operations
- Container management
- Lexer tokenization
- Parser AST construction

### **Integration Tests**

```bash
# Run integration tests
make test-integration
```

Tests complete compilation pipeline:
- Simple program compilation
- Error handling
- Assembly output validation

### **Bootstrap Test**

```bash
# Self-compilation test
make test-bootstrap
```

Process:
1. **Compile v0.0.7.5** using v0.0.7.3
2. **Use v0.0.7.5** to compile itself
3. **Compare** both versions for identical output

## **Troubleshooting**

### **Common Build Issues**

#### **Missing v0.0.7.3 Compiler**
```
Error: ../v0.0.7.3/runac not found
```
**Solution**: Ensure v0.0.7.3 is built and path is correct in Makefile.

#### **Runtime Library Compilation Errors**
```
Error: undefined reference to runtime function
```
**Solution**: Check that all runtime `.o` files are built and linked.

#### **Assembly Generation Issues**
```
Error: invalid assembly syntax
```
**Solution**: Verify Runa syntax matches language specification exactly.

#### **Linking Errors**
```
Error: undefined symbol
```
**Solution**: Check function name consistency between Runa and C runtime.

### **Debug Build Issues**

```bash
# Verbose build for debugging
make clean
make VERBOSE=1 all

# Check intermediate files
ls -la build/
file build/*.o
```

### **Performance Issues**

```bash
# Profile build time
time make clean all

# Check optimization flags
make CFLAGS="-O2 -g" all
```

## **Installation**

### **System Installation**

```bash
# Install to /usr/local/bin
sudo make install

# Or specify prefix
make PREFIX=/opt/runa install
```

### **Development Installation**

```bash
# Create symlink in PATH
ln -s $(pwd)/build/runac ~/bin/runac

# Or add to PATH
export PATH="$(pwd)/build:$PATH"
```

## **Usage**

### **Basic Compilation**

```bash
# Compile Runa program
./build/runac input.runa output.s

# Assemble and link
as --64 output.s -o output.o
gcc output.o -o program
```

### **Complete Pipeline**

```bash
# Helper script for complete compilation
#!/bin/bash
PROGRAM=$1
./build/runac "$PROGRAM.runa" "$PROGRAM.s"
as --64 "$PROGRAM.s" -o "$PROGRAM.o"
gcc "$PROGRAM.o" -o "$PROGRAM"
```

## **Development Workflow**

### **Iterative Development**

```bash
# Fast development cycle
make clean-runa    # Clean only Runa objects
make runa-compile  # Recompile Runa source
make link         # Relink executable
```

### **Testing Changes**

```bash
# Test specific component
make test-lexer
make test-parser
make test-codegen

# Test complete pipeline
make test-integration
```

---

**This build system supports incremental compilation and efficient development workflow while maintaining the separation between Runa compiler logic and C runtime libraries.**