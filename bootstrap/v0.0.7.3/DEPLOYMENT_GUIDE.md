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
# Runa v0.0.7.3 Deployment Guide

> **Exactly what your team needs to copy and use Runa.**

## 🎯 Answer: Minimum Required Files

**No, teams cannot use just the `runac` executable alone.** They need:

### Absolute Minimum (6 files)
```
runac                    # The compiler executable
runtime_io.o            # File I/O functions
runtime_string.o        # String operations
runtime_math.o          # Mathematical functions
runtime_list.o          # List operations
runtime_system.o        # System utilities
```

**Total size: ~330KB**

### Quick Test
```bash
# Copy these 6 files to any directory and test:
echo 'Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 42
End Process' > hello.runa

./runac hello.runa hello.s
gcc -o hello hello.s runtime_*.o -no-pie -lm
./hello; echo "Exit: $?"  # Should show: Exit: 42
```

## 📦 Deployment Options

### Option 1: Minimal Deployment (Production)
**Copy these files only:**
- `bin/runac`
- `runtime/*.o` (all 5 files)

**Pros:** Smallest footprint (~330KB)
**Cons:** No documentation, no examples
**Use case:** Production deployment, CI/CD systems

### Option 2: Developer Kit (Recommended)
**Copy these directories:**
- `bin/` (runac executable)
- `runtime/` (runtime objects)
- `docs/QUICK_REFERENCE.md` (syntax cheat sheet)

**Pros:** Has essential reference, still compact (~350KB)
**Cons:** Limited examples
**Use case:** Developer workstations

### Option 3: Complete Package (Learning)
**Copy entire `v0.0.7.3/` directory**

**Pros:** Complete documentation, 50+ examples, source code
**Cons:** Larger size (~2MB)
**Use case:** Learning, training, full development environment

## 🛠️ Build Commands for Each Option

### Option 1 (Minimal):
```bash
# Assuming runac and runtime_*.o are in current directory:
./runac program.runa program.s
gcc -o program program.s runtime_*.o -no-pie -lm
./program
```

### Option 2 (Developer Kit):
```bash
# With organized structure:
./bin/runac program.runa program.s
gcc -o program program.s runtime/*.o -no-pie -lm
./program
```

### Option 3 (Complete):
```bash
# Same as Option 2, plus access to:
# - docs/USER_GUIDE.md
# - docs/CAPABILITIES_REFERENCE.md
# - examples/*.runa
# - src/ (source code)
```

## 📋 File Breakdown

### The Compiler
- **`runac`** (265KB) - Main compiler executable
  - Converts `.runa` files to `.s` assembly files
  - Self-contained, no external dependencies
  - Works independently but needs runtime for linking

### Runtime Objects (Required for Linking)
- **`runtime_io.o`** (23KB) - File reading/writing functions
- **`runtime_string.o`** (15KB) - String manipulation (concat, find, etc.)
- **`runtime_math.o`** (14KB) - Mathematical functions (sin, cos, sqrt, etc.)
- **`runtime_list.o`** (19KB) - List operations and memory management
- **`runtime_system.o`** (14KB) - System utilities and program setup

**Why these are needed:** The compiler generates assembly that calls these runtime functions. Without them, linking fails with "undefined reference" errors.

## 🧪 Verification Scripts

### Test Minimal Deployment
```bash
#!/bin/bash
# test_minimal.sh - Verify minimal deployment works

# Ensure we have the required files
required_files=("runac" "runtime_io.o" "runtime_string.o" "runtime_math.o" "runtime_list.o" "runtime_system.o")
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

# Test basic compilation
echo 'Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 42
End Process' > test_minimal.runa

echo "🔨 Compiling..."
./runac test_minimal.runa test_minimal.s || exit 1

echo "🔗 Linking..."
gcc -o test_minimal test_minimal.s runtime_*.o -no-pie -lm || exit 1

echo "🚀 Running..."
./test_minimal
exit_code=$?

if [[ $exit_code -eq 42 ]]; then
    echo "✅ Minimal deployment works! Exit code: $exit_code"
    rm -f test_minimal test_minimal.s test_minimal.runa
    exit 0
else
    echo "❌ Test failed! Expected exit code 42, got: $exit_code"
    exit 1
fi
```

### Test All Features
```bash
#!/bin/bash
# test_comprehensive.sh - Test major language features

tests=(
    "Return 42|42|Basic return"
    "Let x be 10\n    Let y be 20\n    Return x plus y|30|Arithmetic"
    "If 5 is less than 10:\n        Return 1\n    Otherwise:\n        Return 0\n    End If|1|Conditionals"
)

for test_spec in "${tests[@]}"; do
    IFS='|' read -r code expected_exit description <<< "$test_spec"

    echo "Testing: $description"

    cat > test_feature.runa << EOF
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    $code
End Process
EOF

    ./runac test_feature.runa test_feature.s && \
    gcc -o test_feature test_feature.s runtime_*.o -no-pie -lm && \
    ./test_feature
    actual_exit=$?

    if [[ $actual_exit -eq $expected_exit ]]; then
        echo "✅ $description works (exit: $actual_exit)"
    else
        echo "❌ $description failed (expected: $expected_exit, got: $actual_exit)"
    fi

    rm -f test_feature test_feature.s test_feature.runa
    echo "---"
done
```

## 🚀 CI/CD Integration

### Docker Example
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y gcc

# Copy minimal Runa deployment
COPY runac /usr/local/bin/
COPY runtime_*.o /usr/local/lib/runa/

# Set up environment
ENV RUNA_RUNTIME_PATH=/usr/local/lib/runa
WORKDIR /workspace

# Usage: docker run -v $(pwd):/workspace runa-dev ./compile.sh program.runa
```

### Build Script for CI
```bash
#!/bin/bash
# ci_build.sh - Automated Runa build for CI systems

set -e

RUNA_FILE="$1"
OUTPUT="${2:-${RUNA_FILE%.runa}}"

if [[ ! -f "$RUNA_FILE" ]]; then
    echo "❌ File not found: $RUNA_FILE"
    exit 1
fi

echo "🔨 Compiling $RUNA_FILE..."
runac "$RUNA_FILE" "${OUTPUT}.s"

echo "🔗 Linking..."
gcc -o "$OUTPUT" "${OUTPUT}.s" ${RUNA_RUNTIME_PATH:-/usr/local/lib/runa}/*.o -no-pie -lm

echo "✅ Built: $OUTPUT"
```

## 📊 Size Comparison

| Deployment Option | Files | Total Size | Use Case |
|-------------------|-------|------------|----------|
| **Minimal** | 6 files | ~330KB | Production, CI/CD |
| **Developer Kit** | 8 files | ~350KB | Development workstations |
| **Complete Package** | ~70 files | ~2MB | Learning, training |

## 🎯 Recommendations by Team Size

### Solo Developer
- **Option 3 (Complete)** - You want all the documentation and examples

### Small Team (2-5 people)
- **Option 2 (Developer Kit)** - Shared quick reference, minimal size

### Large Team (5+ people)
- **Option 3 (Complete)** - Full docs help with onboarding
- Set up shared team standards from examples

### Production/CI Systems
- **Option 1 (Minimal)** - Smallest footprint, fastest deployment

---

## ✅ Final Answer

**Teams need at minimum:**
1. `runac` (compiler executable)
2. `runtime_*.o` (5 runtime object files)

**They cannot use just `runac` alone** - the runtime objects are required for linking any Runa program.

**Recommended approach:** Copy the entire organized `v0.0.7.3/` directory for the best development experience.