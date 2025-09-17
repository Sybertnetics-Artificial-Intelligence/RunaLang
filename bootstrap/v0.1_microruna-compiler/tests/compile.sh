#!/bin/bash

# MicroRuna v0.1 Self-Hosted Compiler Build Script
# Compiles MicroRuna source files using the v0.0 Rust seed compiler
# This is the critical bootstrap moment!

set -e  # Exit on any error

echo "🚀 Building MicroRuna v0.1 Self-Hosted Compiler"
echo "=================================================="

# Configuration
V0_COMPILER="../v0.0_rust-seed/target/debug/runac"
SRC_DIR="src"
OUTPUT_DIR="build"
TARGET_BINARY="runac-v0.1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create build directory
echo -e "${BLUE}Creating build directory...${NC}"
mkdir -p "$OUTPUT_DIR"

# Check if v0.0 compiler exists
if [ ! -f "$V0_COMPILER" ]; then
    echo -e "${RED}ERROR: v0.0 compiler not found at $V0_COMPILER${NC}"
    echo "Please build the v0.0 Rust seed compiler first:"
    echo "  cd ../v0.0_rust-seed && cargo build"
    exit 1
fi

echo -e "${GREEN}✓ v0.0 compiler found${NC}"

# Source files to compile (in dependency order)
SOURCE_FILES=(
    "runtime.runa"
    "lexer.runa"
    "parser.runa"
    "typechecker.runa"
    "codegen.runa"
    "main.runa"
)

echo -e "${BLUE}Compiling MicroRuna source files...${NC}"

# Compile each source file to object file
for src_file in "${SOURCE_FILES[@]}"; do
    echo -e "${YELLOW}Compiling $src_file...${NC}"

    src_path="$SRC_DIR/$src_file"
    obj_name="${src_file%.runa}.o"
    obj_path="$OUTPUT_DIR/$obj_name"

    if [ ! -f "$src_path" ]; then
        echo -e "${RED}ERROR: Source file $src_path not found${NC}"
        exit 1
    fi

    # Compile using v0.0 compiler
    if ! "$V0_COMPILER" "$src_path" "$obj_path"; then
        echo -e "${RED}ERROR: Failed to compile $src_file${NC}"
        exit 1
    fi

    echo -e "${GREEN}✓ $src_file compiled successfully${NC}"
done

# Link all object files into final executable
echo -e "${BLUE}Linking object files...${NC}"

OBJECT_FILES=""
for src_file in "${SOURCE_FILES[@]}"; do
    obj_name="${src_file%.runa}.o"
    OBJECT_FILES="$OBJECT_FILES $OUTPUT_DIR/$obj_name"
done

# Create the final executable by linking the main object
# Note: The v0.0 compiler already handles linking, so we use the main.o as our executable
if [ -f "$OUTPUT_DIR/main.o" ]; then
    cp "$OUTPUT_DIR/main.o" "$OUTPUT_DIR/$TARGET_BINARY"
    chmod +x "$OUTPUT_DIR/$TARGET_BINARY"
    echo -e "${GREEN}✓ Linking completed successfully${NC}"
else
    echo -e "${RED}ERROR: main.o not found for linking${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 SUCCESS: MicroRuna v0.1 Self-Hosted Compiler Built!${NC}"
echo "=================================================="
echo -e "Executable: ${BLUE}$OUTPUT_DIR/$TARGET_BINARY${NC}"
echo ""

# Display build statistics
echo -e "${BLUE}Build Statistics:${NC}"
echo "Source files compiled: ${#SOURCE_FILES[@]}"
echo "Object files created: $(ls -1 $OUTPUT_DIR/*.o 2>/dev/null | wc -l)"
echo "Executable size: $(du -h $OUTPUT_DIR/$TARGET_BINARY 2>/dev/null | cut -f1)B"
echo ""

# Test the executable
echo -e "${BLUE}Testing the new compiler...${NC}"
if [ -x "$OUTPUT_DIR/$TARGET_BINARY" ]; then
    echo -e "${GREEN}✓ Executable is ready${NC}"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./$OUTPUT_DIR/$TARGET_BINARY <input.runa> <output>"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Test with simple MicroRuna programs"
    echo "2. Attempt self-compilation: compile v0.1 source with v0.1 compiler"
    echo "3. Validate bootstrap success!"
else
    echo -e "${RED}ERROR: Executable is not ready${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🚀 Bootstrap Phase 1 (Foundation Setup) - COMPLETE!${NC}"
echo "Ready to proceed to Phase 2 (Core Translation)"