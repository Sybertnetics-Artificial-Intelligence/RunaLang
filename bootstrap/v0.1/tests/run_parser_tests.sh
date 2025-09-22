#!/bin/bash

# Run parser tests for v0.1 using v0.0 compiler

COMPILER="../v0.0_rust-seed/target/release/runac"
TEST_DIR="tests"
FAILURES=0
PASSES=0

echo "=== Running v0.1 Parser Tests ==="
echo

# List of parser test files
TESTS=(
    "test_parser_functions"
    "test_parser_control_flow"
    "test_parser_expressions"
    "test_parser_variables"
    "test_parser_returns"
    "test_parser_edge_cases"
)

for test in "${TESTS[@]}"; do
    echo -n "Testing $test... "

    # Compile the test
    if $COMPILER "$TEST_DIR/${test}.runa" "/tmp/${test}.s" --emit-asm-only --no-dir-scan 2>/dev/null; then
        # Assemble and link
        if as "/tmp/${test}.s" -o "/tmp/${test}.o" 2>/dev/null && \
           ld "/tmp/${test}.o" -o "/tmp/${test}" 2>/dev/null; then
            # Run the test
            if "/tmp/${test}" 2>/dev/null; then
                echo "PASS"
                ((PASSES++))
            else
                EXIT_CODE=$?
                echo "FAIL (exit code: $EXIT_CODE)"
                ((FAILURES++))
            fi
        else
            echo "FAIL (link error)"
            ((FAILURES++))
        fi
    else
        echo "FAIL (compile error)"
        ((FAILURES++))
    fi
done

echo
echo "=== Test Results ==="
echo "PASSED: $PASSES"
echo "FAILED: $FAILURES"

if [ $FAILURES -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi