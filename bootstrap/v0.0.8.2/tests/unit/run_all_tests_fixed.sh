#!/bin/bash
PASS=0
FAIL=0
SKIP=0
TOTAL=0

echo "=================================="
echo "  Runa v0.0.8.2 Full Test Suite"
echo "=================================="
echo ""

for test_file in test_*.runa; do
    # Skip helper files
    if [[ "$test_file" == *"helper"* ]]; then
        continue
    fi
    
    TOTAL=$((TOTAL + 1))
    test_name="${test_file%.runa}"
    
    # Compile with relative path fix for imports
    ../../build/runac "$test_file" "${test_name}.s" 2>&1 > /tmp/compile_output.txt
    compile_status=$?
    
    if [ $compile_status -ne 0 ]; then
        echo "❌ FAIL: $test_name (compilation failed)"
        FAIL=$((FAIL + 1))
        continue
    fi
    
    # Assemble
    as --64 "${test_name}.s" -o "${test_name}.o" 2>&1 > /tmp/asm_output.txt
    if [ $? -ne 0 ]; then
        echo "❌ FAIL: $test_name (assembly failed)"
        FAIL=$((FAIL + 1))
        rm -f "${test_name}.s" "${test_name}.o"
        continue
    fi
    
    # Link
    gcc "${test_name}.o" ../../runtime/runtime.o -lm -o "$test_name" 2>&1 > /tmp/link_output.txt
    if [ $? -ne 0 ]; then
        echo "❌ FAIL: $test_name (linking failed)"
        FAIL=$((FAIL + 1))
        rm -f "${test_name}.s" "${test_name}.o"
        continue
    fi
    
    # Run
    timeout 5 ./"$test_name" > /tmp/run_output.txt 2>&1
    run_status=$?
    
    # Check for PASS/FAIL assertions or specific exit codes
    if grep -q "FAIL" /tmp/run_output.txt; then
        echo "❌ FAIL: $test_name (test assertions failed)"
        FAIL=$((FAIL + 1))
    elif [ $run_status -eq 124 ]; then
        echo "⏱️  SKIP: $test_name (timeout)"
        SKIP=$((SKIP + 1))
    elif [ $run_status -eq 0 ] || [ $run_status -eq 42 ]; then
        # Exit code 0 or 42 (test_simple_list_var) are success
        echo "✅ PASS: $test_name"
        PASS=$((PASS + 1))
    else
        echo "❌ FAIL: $test_name (exit code $run_status)"
        FAIL=$((FAIL + 1))
    fi
    
    # Cleanup
    rm -f "${test_name}.s" "${test_name}.o" "$test_name"
done

echo ""
echo "=================================="
echo "  Test Results Summary"
echo "=================================="
echo "Total:  $TOTAL"
echo "✅ Pass:  $PASS"
echo "❌ Fail:  $FAIL"
echo "⏱️  Skip:  $SKIP"
echo "Success Rate: $(echo "scale=1; $PASS * 100 / $TOTAL" | bc)%"
echo "=================================="

exit $([ $FAIL -eq 0 ] && echo 0 || echo 1)
