#!/bin/bash
# Test runner for bootstrap unit tests
# Compiles, assembles, links, and runs all tests in tests/unit
# Output goes to tests/output

# Note: Not using set -e so tests continue after failures

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UNIT_DIR="$SCRIPT_DIR/unit"
OUTPUT_DIR="$SCRIPT_DIR/output"
RUNTIME_DIR="$PROJECT_DIR/runtime"
COMPILER="$PROJECT_DIR/build/runac"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Counters
TOTAL=0
PASSED=0
FAILED=0
SKIPPED=0

# Test results file
RESULTS_FILE="$OUTPUT_DIR/test_results.txt"
echo "Test Results - $(date)" > "$RESULTS_FILE"
echo "========================================" >> "$RESULTS_FILE"

# Helper files that are not standalone tests
HELPER_FILES=("test_imports_helper.runa")

# Function to check if file is a helper
is_helper() {
    local filename="$1"
    for helper in "${HELPER_FILES[@]}"; do
        if [[ "$filename" == "$helper" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to run a single test
run_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .runa)
    local test_output_dir="$OUTPUT_DIR/$test_name"

    TOTAL=$((TOTAL + 1))

    # Create test-specific output directory
    mkdir -p "$test_output_dir"

    echo -n "Testing $test_name... "

    # Step 1: Compile .runa to .s
    if ! "$COMPILER" "$test_file" "$test_output_dir/${test_name}.s" > "$test_output_dir/compile.log" 2>&1; then
        echo -e "${RED}FAILED${NC} (compilation)"
        echo "FAILED: $test_name (compilation error)" >> "$RESULTS_FILE"
        cat "$test_output_dir/compile.log" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        return 1
    fi

    # Step 2: Assemble .s to .o
    if ! as -o "$test_output_dir/${test_name}.o" "$test_output_dir/${test_name}.s" > "$test_output_dir/assemble.log" 2>&1; then
        echo -e "${RED}FAILED${NC} (assembly)"
        echo "FAILED: $test_name (assembly error)" >> "$RESULTS_FILE"
        cat "$test_output_dir/assemble.log" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        return 1
    fi

    # Step 3: Link with runtime (compile runtime.c directly to ensure set functions are included)
    if ! gcc -o "$test_output_dir/${test_name}" "$test_output_dir/${test_name}.o" "$RUNTIME_DIR/runtime.c" -no-pie -lm > "$test_output_dir/link.log" 2>&1; then
        echo -e "${RED}FAILED${NC} (linking)"
        echo "FAILED: $test_name (linking error)" >> "$RESULTS_FILE"
        cat "$test_output_dir/link.log" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        return 1
    fi

    # Step 4: Run the test
    if "$test_output_dir/${test_name}" > "$test_output_dir/output.txt" 2>&1; then
        local exit_code=$?
        echo -e "${GREEN}PASSED${NC}"
        echo "PASSED: $test_name" >> "$RESULTS_FILE"
        echo "Output:" >> "$RESULTS_FILE"
        cat "$test_output_dir/output.txt" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        PASSED=$((PASSED + 1))
        return 0
    else
        local exit_code=$?
        echo -e "${RED}FAILED${NC} (runtime, exit code: $exit_code)"
        echo "FAILED: $test_name (runtime error, exit code: $exit_code)" >> "$RESULTS_FILE"
        echo "Output:" >> "$RESULTS_FILE"
        cat "$test_output_dir/output.txt" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Main execution
echo "========================================="
echo "Running Unit Tests for bootstrap compiler"
echo "========================================="
echo ""

# Check if compiler exists
if [[ ! -f "$COMPILER" ]]; then
    echo -e "${RED}ERROR:${NC} Compiler not found at $COMPILER"
    echo "Please build stage2 first."
    exit 1
fi

# Run all tests
for test_file in "$UNIT_DIR"/*.runa; do
    test_filename=$(basename "$test_file")

    # Skip helper files
    if is_helper "$test_filename"; then
        echo -e "${YELLOW}SKIPPED${NC}: $test_filename (helper file)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    run_test "$test_file"
done

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "Total:   $TOTAL"
echo -e "Passed:  ${GREEN}$PASSED${NC}"
echo -e "Failed:  ${RED}$FAILED${NC}"
echo -e "Skipped: ${YELLOW}$SKIPPED${NC}"
echo ""

# Write summary to results file
echo "" >> "$RESULTS_FILE"
echo "========================================" >> "$RESULTS_FILE"
echo "Summary" >> "$RESULTS_FILE"
echo "========================================" >> "$RESULTS_FILE"
echo "Total:   $TOTAL" >> "$RESULTS_FILE"
echo "Passed:  $PASSED" >> "$RESULTS_FILE"
echo "Failed:  $FAILED" >> "$RESULTS_FILE"
echo "Skipped: $SKIPPED" >> "$RESULTS_FILE"

echo "Results written to: $RESULTS_FILE"
echo ""

# Exit with appropriate code
if [[ $FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi
