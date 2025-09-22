#!/bin/bash

# Run code generation tests for v0.1 using v0.0 compiler

echo "=== Running v0.1 Code Generation Tests ==="
echo

COMPILER="../v0.0/target/release/runac"
TESTS=(
    "test_codegen_simple"
    "test_codegen_arithmetic"
    "test_codegen_variables"
    "test_codegen_control_flow"
    "test_codegen_functions"
    "test_codegen_comparisons"
    "test_codegen_pointers"
    "test_codegen_globals"
    "test_codegen_unary"
)

PASSES=0
FAILURES=0

for test in "${TESTS[@]}"; do
    echo -n "Testing $test... "

    # Compile test
    if $COMPILER "tests/${test}.runa" -o "/tmp/${test}.s" --emit-asm-only 2>/dev/null; then
        # Assemble with NASM
        if nasm -f elf64 "/tmp/${test}.s" -o "/tmp/${test}.o" 2>/dev/null; then
            # Link
            if ld "/tmp/${test}.o" -o "/tmp/${test}" -lc -dynamic-linker /lib64/ld-linux-x86-64.so.2 2>/dev/null; then
                # Run test
                "/tmp/${test}" 2>/dev/null
                EXIT_CODE=$?

                if [ $EXIT_CODE -eq 0 ]; then
                    echo "PASS"
                    ((PASSES++))
                elif [ "$test" = "test_codegen_simple" ] && [ $EXIT_CODE -eq 42 ]; then
                    echo "PASS (exit code 42 expected)"
                    ((PASSES++))
                else
                    echo "FAIL (exit code: $EXIT_CODE)"
                    ((FAILURES++))
                fi
            else
                echo "FAIL (link error)"
                ((FAILURES++))
            fi
        else
            echo "FAIL (assembly error)"
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