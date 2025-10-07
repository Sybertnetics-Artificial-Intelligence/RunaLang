#!/bin/bash
# Phase 1 Lambda Parsing Test
# Validates that lambda expressions parse correctly and fail at codegen with expected error

set -e

COMPILER="../v0.0.8.4/stage1/runac"
TEST_FILE="unit/test_lambda_parse.runa"
OUTPUT_FILE="output/test_lambda_parse.s"

echo "=== Phase 1: Lambda Expression Parsing Test ==="
echo ""
echo "Test file: $TEST_FILE"
echo "Expected behavior:"
echo "  - Parser should accept 'lambda x: expression' syntax"
echo "  - Codegen should fail with: 'Lambda expressions not yet supported in codegen (Phase 2)'"
echo ""

# Run the compiler and capture output
echo "Running compiler..."
OUTPUT=$($COMPILER $TEST_FILE $OUTPUT_FILE 2>&1)
EXIT_CODE=$?

echo "Compiler output:"
echo "$OUTPUT"
echo ""

# Check if we got the expected error
if echo "$OUTPUT" | grep -q "Lambda expressions not yet supported in codegen (Phase 2)"; then
    echo "✓ SUCCESS: Parser accepted lambda syntax"
    echo "✓ SUCCESS: Codegen failed with expected error message"
    echo ""
    echo "Phase 1 test PASSED!"
    exit 0
else
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✗ FAIL: Compiler succeeded when it should have failed at codegen"
    else
        echo "✗ FAIL: Got unexpected error message"
        echo "Expected: 'Lambda expressions not yet supported in codegen (Phase 2)'"
        echo "Got: $OUTPUT"
    fi
    echo ""
    echo "Phase 1 test FAILED!"
    exit 1
fi
