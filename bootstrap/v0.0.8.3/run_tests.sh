#!/bin/bash
passed=0
failed=0
for test in tests/unit/test_*.runa; do
    name=$(basename "$test" .runa)
    echo "Testing $name..."
    if ./build/runac "$test" "/tmp/${name}.s" > /dev/null 2>&1 && \
       as "/tmp/${name}.s" -o "/tmp/${name}.o" 2>/dev/null && \
       gcc "/tmp/${name}.o" runtime/runtime.o -o "/tmp/${name}" -no-pie -lm -Wl,--allow-multiple-definition 2>/dev/null && \
       timeout 5 "/tmp/${name}" > /dev/null 2>&1; then
        echo "✓ $name passed"
        ((passed++))
    else
        echo "✗ $name FAILED"
        ((failed++))
    fi
done
echo ""
echo "Results: $passed passed, $failed failed"
