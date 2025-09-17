#!/bin/bash
# Build script for MicroRuna v0.1 programs with runtime
# Usage: ./build_with_runtime.sh program.runa

if [ $# -ne 1 ]; then
    echo "Usage: $0 program.runa"
    exit 1
fi

SOURCE_FILE="$1"
BASE_NAME="${SOURCE_FILE%.runa}"
ASM_FILE="${BASE_NAME}.s"
EXEC_FILE="${BASE_NAME}_exe"

# Step 1: Compile MicroRuna to assembly using v0.0 compiler
echo "Compiling $SOURCE_FILE to assembly..."
../v0.0_rust-seed/target/debug/runac "$SOURCE_FILE" "$ASM_FILE"
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Step 2: Assemble runtime
echo "Assembling runtime..."
as runtime.s -o runtime.o
if [ $? -ne 0 ]; then
    echo "Runtime assembly failed!"
    exit 1
fi

# Step 3: Assemble generated code
echo "Assembling generated code..."
as "$ASM_FILE" -o "${BASE_NAME}.o"
if [ $? -ne 0 ]; then
    echo "Assembly failed!"
    exit 1
fi

# Step 4: Link with runtime
echo "Linking with runtime..."
ld runtime.o "${BASE_NAME}.o" -o "$EXEC_FILE"
if [ $? -ne 0 ]; then
    echo "Linking failed!"
    exit 1
fi

echo "Build successful: $EXEC_FILE"
echo "Run with: ./$EXEC_FILE"