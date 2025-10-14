#!/bin/bash

# Build stage1 of v0.0.8.4.5.3 using v0.0.8.4.5.2
# This adds the world-class recursive import system

set -e  # Exit on error

echo "========================================"
echo "Building v0.0.8.4.5.3 - Recursive Imports"
echo "========================================"
echo ""

# Create build directory
mkdir -p build

echo "[1/8] Compiling string_utils.runa..."
../v0.0.8.4.5.2/build/runac src/string_utils.runa build/string_utils.s

echo "[2/8] Compiling hashtable.runa..."
../v0.0.8.4.5.2/build/runac src/hashtable.runa build/hashtable.s

echo "[3/8] Compiling containers.runa..."
../v0.0.8.4.5.2/build/runac src/containers.runa build/containers.s

echo "[4/8] Compiling lexer.runa..."
../v0.0.8.4.5.2/build/runac src/lexer.runa build/lexer.s

echo "[5/8] Compiling parser.runa..."
../v0.0.8.4.5.2/build/runac src/parser.runa build/parser.s

echo "[6/8] Compiling codegen.runa..."
../v0.0.8.4.5.2/build/runac src/codegen.runa build/codegen.s

echo "[7/8] Compiling main.runa (with recursive imports integrated)..."
../v0.0.8.4.5.2/build/runac src/main.runa build/main.s

echo ""
echo "========================================"
echo "Assembling and linking..."
echo "========================================"
echo ""

# Assemble all .s files
for src in string_utils hashtable containers lexer parser codegen main; do
    echo "Assembling $src.s..."
    as build/$src.s -o build/$src.o
done

# Link everything
echo "Linking runac..."
gcc build/string_utils.o build/hashtable.o build/containers.o build/lexer.o build/parser.o build/codegen.o build/main.o runtime/runtime.c -o build/runac -lm -no-pie

echo ""
echo "========================================"
echo "✓ Build complete!"
echo "========================================"
echo ""
echo "Binary: build/runac"
echo "Test with: ./build/runac tests/unit/test_basic_types.runa /tmp/test.s"
