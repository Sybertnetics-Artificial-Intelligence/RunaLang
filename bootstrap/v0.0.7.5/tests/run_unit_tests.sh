#!/bin/bash
# Unit test runner for v0.0.7.5 bootstrap compiler
# Tests individual component functionality

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_ROOT/build"
TESTS_DIR="$SCRIPT_DIR/unit"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure we're using v0.0.7.3 compiler
RUNAC="${PROJECT_ROOT}/../v0.0.7.3/runac"

# Check if compiler exists
if [ ! -f "$RUNAC" ]; then
    echo -e "${RED}ERROR: v0.0.7.3 compiler not found at $RUNAC${NC}"
    exit 1
fi

# Ensure build directory exists
mkdir -p "$BUILD_DIR"

echo "========================================="
echo "Running Unit Tests for v0.0.7.5"
echo "========================================="
echo ""

# Counter for test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to compile and run a test
run_test() {
    local test_file="$1"
    local test_name="$(basename "$test_file" .runa)"

    echo -n "Testing $test_name... "
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Compile test
    local test_asm="$BUILD_DIR/${test_name}.s"
    local test_obj="$BUILD_DIR/${test_name}.o"
    local test_exe="$BUILD_DIR/${test_name}_test"

    # Compile Runa to assembly
    if ! "$RUNAC" "$test_file" "$test_asm" 2>/dev/null; then
        echo -e "${RED}FAILED${NC} (compilation error)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi

    # Assemble to object file
    if ! as --64 "$test_asm" -o "$test_obj" 2>/dev/null; then
        echo -e "${RED}FAILED${NC} (assembly error)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi

    # Link with runtime and component libraries
    # Include all runtime objects and the component being tested
    local component_obj=""
    case "$test_name" in
        test_string_utils)
            component_obj="$BUILD_DIR/string_utils.o"
            ;;
        test_hashtable)
            component_obj="$BUILD_DIR/hashtable.o $BUILD_DIR/string_utils.o"
            ;;
        test_containers)
            component_obj="$BUILD_DIR/containers.o $BUILD_DIR/string_utils.o"
            ;;
    esac

    if ! gcc -o "$test_exe" "$test_obj" $component_obj $BUILD_DIR/runtime_*.o -lm 2>/dev/null; then
        echo -e "${RED}FAILED${NC} (linking error)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi

    # Run test
    if "$test_exe" > /dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        local exit_code=$?
        echo -e "${RED}FAILED${NC} (exit code: $exit_code)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Ensure component libraries are compiled first
echo "Compiling component libraries..."
for src_file in "$PROJECT_ROOT"/src/*.runa; do
    if [ -f "$src_file" ]; then
        component_name="$(basename "$src_file" .runa)"
        component_asm="$BUILD_DIR/${component_name}.s"
        component_obj="$BUILD_DIR/${component_name}.o"

        if [ ! -f "$component_obj" ]; then
            echo "  Compiling $component_name..."
            "$RUNAC" "$src_file" "$component_asm"
            as --64 "$component_asm" -o "$component_obj"
        fi
    fi
done

echo ""
echo "Running unit tests..."
echo ""

# Run tests for completed components
if [ -f "$BUILD_DIR/string_utils.o" ] && [ -f "$TESTS_DIR/test_string_utils.runa" ]; then
    run_test "$TESTS_DIR/test_string_utils.runa"
fi

if [ -f "$BUILD_DIR/hashtable.o" ] && [ -f "$TESTS_DIR/test_hashtable.runa" ]; then
    run_test "$TESTS_DIR/test_hashtable.runa"
fi

if [ -f "$BUILD_DIR/containers.o" ] && [ -f "$TESTS_DIR/test_containers.runa" ]; then
    run_test "$TESTS_DIR/test_containers.runa"
fi

# Summary
echo ""
echo "========================================="
echo "Test Results Summary"
echo "========================================="
echo "Total tests:  $TOTAL_TESTS"
echo -e "Passed:       ${GREEN}$PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "Failed:       ${RED}$FAILED_TESTS${NC}"
else
    echo -e "Failed:       $FAILED_TESTS"
fi
echo ""

if [ $FAILED_TESTS -eq 0 ] && [ $TOTAL_TESTS -gt 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi