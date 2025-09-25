#!/bin/bash

# Comprehensive test suite for v0.0.7 features
# Tests: Import statements, File I/O (read_file, write_file), Struct field offsets

echo "=== V0.0.7 Feature Verification Suite ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local expected_exit_code=$2
    local program_name=$3

    echo -n "Testing $test_name... "

    # Run the program and capture exit code
    ./$program_name > /tmp/test_output.txt 2>&1
    local exit_code=$?

    if [ $exit_code -eq $expected_exit_code ]; then
        echo -e "${GREEN}PASSED${NC} (exit code: $exit_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC} (expected: $expected_exit_code, got: $exit_code)"
        echo "Output:"
        cat /tmp/test_output.txt
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Clean up previous test files
rm -f test_*.s test_*_program test_output*.txt test_import_output.txt test_comprehensive_output.txt

echo "=== Test 1: Basic Import Parsing ==="
cat > test_import_basic.runa << 'EOF'
Import "lexer" as Lexer
Import "parser" as Parser

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 0
End Process
EOF

./runac test_import_basic.runa test_import_basic.s
if [ $? -eq 0 ]; then
    # Check if imports are in the assembly
    if grep -q "# Imports:" test_import_basic.s && \
       grep -q '#   Import "lexer" as Lexer' test_import_basic.s && \
       grep -q '#   Import "parser" as Parser' test_import_basic.s; then
        echo -e "${GREEN}PASSED${NC} - Imports correctly parsed and documented"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} - Imports not found in assembly"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

echo "=== Test 2: File Read (read_file) ==="
# Create test input file
echo "Test content for read_file" > test_read_input.txt

cat > test_read.runa << 'EOF'
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let content be read_file("test_read_input.txt")
    Print read_file("test_read_input.txt")
    Return 0
End Process
EOF

./runac test_read.runa test_read.s
gcc test_read.s runtime_io.o -o test_read_program 2>/dev/null
if [ $? -eq 0 ]; then
    output=$(./test_read_program 2>/dev/null)
    if [ "$output" = "Test content for read_file" ]; then
        echo -e "${GREEN}PASSED${NC} - read_file correctly reads file content"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} - Unexpected output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation/linking failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

echo "=== Test 3: File Write (write_file) ==="
cat > test_write.runa << 'EOF'
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let result be write_file("test_write_output.txt", "Successfully written by write_file!")
    Return result
End Process
EOF

./runac test_write.runa test_write.s
gcc test_write.s runtime_io.o -o test_write_program 2>/dev/null
if [ $? -eq 0 ]; then
    ./test_write_program
    if [ $? -eq 0 ] && [ -f "test_write_output.txt" ]; then
        content=$(cat test_write_output.txt)
        if [ "$content" = "Successfully written by write_file!" ]; then
            echo -e "${GREEN}PASSED${NC} - write_file correctly writes content"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAILED${NC} - Wrong content written: $content"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAILED${NC} - File not created or wrong exit code"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation/linking failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

echo "=== Test 4: Struct Field Offsets ==="
cat > test_struct_offsets.runa << 'EOF'
Type called "ThreeFields":
    first as Integer,
    second as Integer,
    third as Integer
End Type

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let obj be ThreeFields
    Set obj.first to 10
    Set obj.second to 20
    Set obj.third to 30

    Let sum be obj.first plus obj.second
    Let total be sum plus obj.third
    Return total
End Process
EOF

./runac test_struct_offsets.runa test_struct_offsets.s
gcc test_struct_offsets.s -o test_struct_offsets_program 2>/dev/null
if [ $? -eq 0 ]; then
    ./test_struct_offsets_program
    exit_code=$?
    if [ $exit_code -eq 60 ]; then
        # Check assembly for correct offsets (0, 8, 16)
        if grep -q "movq.*0(%r" test_struct_offsets.s && \
           grep -q "movq.*8(%r" test_struct_offsets.s && \
           grep -q "movq.*16(%r" test_struct_offsets.s; then
            echo -e "${GREEN}PASSED${NC} - Struct offsets correct (0, 8, 16) and values computed correctly (10+20+30=60)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAILED${NC} - Offsets incorrect in assembly"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAILED${NC} - Expected 60, got $exit_code"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

echo "=== Test 5: Combined Features ==="
# Create input file for combined test
echo "Input for combined test" > test_combined_input.txt

cat > test_combined.runa << 'EOF'
Import "utils" as Utils

Type called "FileInfo":
    size as Integer,
    status as Integer
End Type

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let info be FileInfo
    Set info.size to 25
    Set info.status to 17

    Let content be read_file("test_combined_input.txt")
    Let write_result be write_file("test_combined_output.txt", "Combined test output")

    Let result be info.size plus info.status
    Return result
End Process
EOF

./runac test_combined.runa test_combined.s
gcc test_combined.s runtime_io.o -o test_combined_program 2>/dev/null
if [ $? -eq 0 ]; then
    ./test_combined_program
    exit_code=$?
    if [ $exit_code -eq 42 ] && [ -f "test_combined_output.txt" ]; then
        content=$(cat test_combined_output.txt)
        if [ "$content" = "Combined test output" ] && \
           grep -q "# Imports:" test_combined.s && \
           grep -q '#   Import "utils" as Utils' test_combined.s; then
            echo -e "${GREEN}PASSED${NC} - All features work together"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAILED${NC} - Some feature didn't work correctly"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAILED${NC} - Wrong exit code or file not created"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation/linking failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

echo "=== Test 6: Multiple Imports ==="
cat > test_multi_import.runa << 'EOF'
Import "lexer" as Lexer
Import "parser" as Parser
Import "codegen" as CodeGen
Import "runtime" as Runtime

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 4
End Process
EOF

./runac test_multi_import.runa test_multi_import.s
if [ $? -eq 0 ]; then
    import_count=$(grep -c '#   Import' test_multi_import.s)
    if [ $import_count -eq 4 ]; then
        echo -e "${GREEN}PASSED${NC} - All 4 imports correctly parsed"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} - Expected 4 imports, found $import_count"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

echo "=== Test 7: read_file with non-existent file ==="
cat > test_read_error.runa << 'EOF'
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let content be read_file("this_file_does_not_exist.txt")
    If content is equal to 0:
        Return 99
    Otherwise:
        Return 1
    End If
End Process
EOF

./runac test_read_error.runa test_read_error.s
gcc test_read_error.s runtime_io.o -o test_read_error_program 2>/dev/null
if [ $? -eq 0 ]; then
    ./test_read_error_program 2>/dev/null
    exit_code=$?
    if [ $exit_code -eq 99 ]; then
        echo -e "${GREEN}PASSED${NC} - read_file returns NULL for non-existent file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} - Expected 99, got $exit_code"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC} - Compilation/linking failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Summary
echo "=== Test Summary ==="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All features verified successfully!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Please review the failures above.${NC}"
    exit 1
fi