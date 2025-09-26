#!/bin/bash

# Test Runner for v0.0.7.5 Bootstrap Compiler
# Runs all tests and reports results

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
COMPILER="../v0.0.7.3/runac"
TEST_DIR="."
BUILD_DIR="../build/tests"

# Create build directory for test outputs
mkdir -p "$BUILD_DIR"

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
COMPILE_ERRORS=0

# Function to run a single test
run_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .runa)

    echo -n "Testing $test_name... "
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Compile the test
    if $COMPILER "$test_file" "$BUILD_DIR/$test_name.s" 2>/dev/null; then
        # Assemble and link
        if gcc -o "$BUILD_DIR/$test_name" "$BUILD_DIR/$test_name.s" 2>/dev/null; then
            # Run the test
            if "$BUILD_DIR/$test_name" 2>/dev/null; then
                EXIT_CODE=$?
                if [ $EXIT_CODE -eq 0 ]; then
                    echo -e "${GREEN}PASSED${NC}"
                    PASSED_TESTS=$((PASSED_TESTS + 1))
                else
                    echo -e "${RED}FAILED${NC} (exit code: $EXIT_CODE)"
                    FAILED_TESTS=$((FAILED_TESTS + 1))
                fi
            else
                echo -e "${RED}RUNTIME ERROR${NC}"
                FAILED_TESTS=$((FAILED_TESTS + 1))
            fi
        else
            echo -e "${YELLOW}LINK ERROR${NC}"
            COMPILE_ERRORS=$((COMPILE_ERRORS + 1))
        fi
    else
        echo -e "${YELLOW}COMPILE ERROR${NC}"
        COMPILE_ERRORS=$((COMPILE_ERRORS + 1))
    fi
}

# Run unit tests
echo "=== Running Unit Tests ==="
for test_file in unit/*.runa; do
    if [ -f "$test_file" ]; then
        run_test "$test_file"
    fi
done

# Run integration tests
echo ""
echo "=== Running Integration Tests ==="
for test_file in integration/*.runa; do
    if [ -f "$test_file" ]; then
        run_test "$test_file"
    fi
done

# Run examples (just compile them)
echo ""
echo "=== Compiling Examples ==="
for example_file in examples/*.runa; do
    if [ -f "$example_file" ]; then
        example_name=$(basename "$example_file" .runa)
        echo -n "Compiling $example_name... "
        TOTAL_TESTS=$((TOTAL_TESTS + 1))

        if $COMPILER "$example_file" "$BUILD_DIR/$example_name.s" 2>/dev/null; then
            echo -e "${GREEN}OK${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "${YELLOW}COMPILE ERROR${NC}"
            COMPILE_ERRORS=$((COMPILE_ERRORS + 1))
        fi
    fi
done

# Print summary
echo ""
echo "========================================"
echo "Test Results Summary:"
echo "========================================"
echo -e "Total Tests:     $TOTAL_TESTS"
echo -e "Passed:          ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed:          ${RED}$FAILED_TESTS${NC}"
echo -e "Compile Errors:  ${YELLOW}$COMPILE_ERRORS${NC}"
echo "========================================"

# Exit with error if any tests failed
if [ $FAILED_TESTS -gt 0 ] || [ $COMPILE_ERRORS -gt 0 ]; then
    exit 1
fi

exit 0