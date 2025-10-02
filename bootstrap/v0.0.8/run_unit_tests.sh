#!/bin/bash
COMPILER=./stage2/runac
PASSED=0
FAILED=0
TOTAL=0

echo "Running v0.0.8 Unit Tests..."
echo "============================="

for test_file in tests/unit/test_*.runa; do
    TOTAL=1
    test_name=""
    output_asm="/tmp/.s"
    output_obj="/tmp/.o"
    output_bin="/tmp/"
    
    # Compile
    if  "" "" 2>/dev/null; then
        # Assemble
        if as --64 "" -o "" 2>/dev/null; then
            # Link
            if gcc "" stage2/runtime.o -lm -o "" 2>/dev/null; then
                echo "✓ "
                PASSED=1
            else
                echo "✗  (link failed)"
                FAILED=1
            fi
        else
            echo "✗  (assembly failed)"
            FAILED=1
        fi
    else
        echo "✗  (compilation failed)"
        FAILED=1
    fi
done

echo "============================="
echo "Total:  | Passed:  | Failed: "
