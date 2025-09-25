#!/bin/bash

# Build script for Runa v0.0.7.5 (written in Runa)
# This script compiles the Runa compiler using the v0.0.7 C compiler

set -e  # Exit on error

RUNA_V007="../v0.0.7/runac"
SRC_DIR="src"
RUNTIME_DIR="runtime"
BUILD_DIR="build"

echo "=== Building Runa v0.0.7.5 ==="
echo "Using v0.0.7 compiler: $RUNA_V007"

# Check if v0.0.7 compiler exists
if [ ! -f "$RUNA_V007" ]; then
    echo "Error: v0.0.7 compiler not found at $RUNA_V007"
    echo "Please build v0.0.7 first"
    exit 1
fi

# Create build directory
mkdir -p $BUILD_DIR

# Step 1: Compile runtime libraries
echo ""
echo "Step 1: Compiling runtime libraries..."
gcc -c $RUNTIME_DIR/runtime_io.c -o $BUILD_DIR/runtime_io.o
gcc -c $RUNTIME_DIR/runtime_memory.c -o $BUILD_DIR/runtime_memory.o
gcc -c $RUNTIME_DIR/runtime_stdio.c -o $BUILD_DIR/runtime_stdio.o

# Step 2: Compile Runa source files to assembly
echo ""
echo "Step 2: Compiling Runa source files..."

# Compile lexer.runa
echo "  Compiling lexer.runa..."
$RUNA_V007 $SRC_DIR/lexer.runa $BUILD_DIR/lexer.s

# Compile parser.runa
echo "  Compiling parser.runa..."
$RUNA_V007 $SRC_DIR/parser.runa $BUILD_DIR/parser.s

# Compile codegen.runa
echo "  Compiling codegen.runa..."
$RUNA_V007 $SRC_DIR/codegen.runa $BUILD_DIR/codegen.s

# Compile main.runa
echo "  Compiling main.runa..."
$RUNA_V007 $SRC_DIR/main.runa $BUILD_DIR/main.s

# Step 3: Assemble the generated assembly files
echo ""
echo "Step 3: Assembling generated code..."
as $BUILD_DIR/lexer.s -o $BUILD_DIR/lexer.o
as $BUILD_DIR/parser.s -o $BUILD_DIR/parser.o
as $BUILD_DIR/codegen.s -o $BUILD_DIR/codegen.o
as $BUILD_DIR/main.s -o $BUILD_DIR/main.o

# Step 4: Link everything together
echo ""
echo "Step 4: Linking..."
gcc -o runac_v075 \
    $BUILD_DIR/main.o \
    $BUILD_DIR/lexer.o \
    $BUILD_DIR/parser.o \
    $BUILD_DIR/codegen.o \
    $BUILD_DIR/runtime_io.o \
    $BUILD_DIR/runtime_memory.o \
    $BUILD_DIR/runtime_stdio.o \
    -no-pie

echo ""
echo "=== Build complete! ==="
echo "Runa v0.0.7.5 compiler created: runac_v075"
echo ""
echo "To test the compiler, run:"
echo "  ./runac_v075 test.runa test.s"