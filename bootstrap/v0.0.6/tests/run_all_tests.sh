#!/bin/bash

# Copyright 2025 Sybertnetics Artificial Intelligence Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Comprehensive test runner for v0.0.6

set -e  # Exit on any error

echo "=== v0.0.6 Comprehensive Test Suite ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

passed=0
failed=0

run_test() {
    local test_file=$1
    local expected_output=$2
    local description=$3

    echo -n "Testing $description... "

    if ../runac "$test_file" "${test_file%.runa}.s" 2>/dev/null; then
        if gcc -o "${test_file%.runa}_program" "${test_file%.runa}.s" 2>/dev/null; then
            output=$(timeout 10 "./${test_file%.runa}_program" 2>/dev/null)
            if [ "$output" = "$expected_output" ]; then
                echo -e "${GREEN}PASS${NC}"
                ((passed++))
            else
                echo -e "${RED}FAIL${NC}"
                echo "  Expected: $expected_output"
                echo "  Got: $output"
                ((failed++))
            fi
            rm -f "${test_file%.runa}_program" "${test_file%.runa}.s"
        else
            echo -e "${RED}FAIL${NC} (assembly failed)"
            ((failed++))
        fi
    else
        echo -e "${RED}FAIL${NC} (compilation failed)"
        ((failed++))
    fi
}

run_memory_test() {
    local test_file=$1
    local description=$2

    echo -n "Memory testing $description... "

    if ../runac "$test_file" "${test_file%.runa}.s" 2>/dev/null; then
        if gcc -o "${test_file%.runa}_program" "${test_file%.runa}.s" 2>/dev/null; then
            if command -v valgrind >/dev/null 2>&1; then
                valgrind_output=$(valgrind --leak-check=full --error-exitcode=1 "./${test_file%.runa}_program" 2>&1 >/dev/null)
                if [ $? -eq 0 ] && echo "$valgrind_output" | grep -q "definitely lost: 0 bytes"; then
                    echo -e "${GREEN}PASS${NC} (no memory leaks)"
                    ((passed++))
                else
                    echo -e "${RED}FAIL${NC} (memory issues detected)"
                    ((failed++))
                fi
            else
                echo -e "${YELLOW}SKIP${NC} (valgrind not available)"
            fi
            rm -f "${test_file%.runa}_program" "${test_file%.runa}.s"
        else
            echo -e "${RED}FAIL${NC} (assembly failed)"
            ((failed++))
        fi
    else
        echo -e "${RED}FAIL${NC} (compilation failed)"
        ((failed++))
    fi
}

echo -e "${BLUE}=== Core Functionality Tests ===${NC}"
run_test "test_minimal_working.runa" "42" "basic compilation and print"
run_test "test_print_integer_regression.runa" $'42\n100\n142' "print integer regression"
run_test "test_arithmetic_simple.runa" $'40\n58\n42\n21' "arithmetic operations"

echo ""
echo -e "${BLUE}=== Advanced Feature Tests ===${NC}"
run_test "test_bootstrap_final.runa" $'30\n75\n48\n12\n250' "function parameters"
run_test "test_complete_functionality.runa" $'60\n78\n5500' "complex functionality"

echo ""
echo -e "${BLUE}=== Performance Tests ===${NC}"
run_test "test_memory_stress.runa" "85" "memory management (30+ vars)"

echo ""
echo -e "${BLUE}=== Ultimate Validation ===${NC}"
run_test "test_final_validation.runa" $'42\n63\n72\n12\n120\n50\n115' "final comprehensive test"

echo ""
echo -e "${BLUE}=== Memory Leak Tests ===${NC}"
run_memory_test "test_final_validation.runa" "comprehensive memory validation"
run_memory_test "test_memory_stress.runa" "stress test memory validation"

echo ""
echo -e "${BLUE}=== Test Results ===${NC}"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"

if [ $failed -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🏆 ALL TESTS PASSED! v0.0.6 is fully validated! 🏆${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Check output above.${NC}"
    exit 1
fi