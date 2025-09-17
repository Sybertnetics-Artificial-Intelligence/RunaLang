#!/bin/bash

echo "Building v0.1 MicroRuna Runtime Library..."

# Compile the runtime as an object file
gcc -c -o runtime.o runtime.c -Wall -Wextra

if [ $? -eq 0 ]; then
    echo "✓ Runtime compiled successfully to runtime.o"

    # Create a static library
    ar rcs libruna_runtime.a runtime.o

    if [ $? -eq 0 ]; then
        echo "✓ Static library libruna_runtime.a created"
        echo ""
        echo "Usage:"
        echo "To link with a MicroRuna program:"
        echo "  gcc program.s runtime.o -o program"
        echo "Or with the static library:"
        echo "  gcc program.s -L. -lruna_runtime -o program"
    else
        echo "✗ Failed to create static library"
        exit 1
    fi
else
    echo "✗ Runtime compilation failed"
    exit 1
fi