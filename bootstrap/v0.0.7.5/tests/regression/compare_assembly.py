#!/usr/bin/env python3
# compare_assembly.py

import subprocess
import sys
import difflib

def compile_with_v0073(source, output):
    """Compile with v0.0.7.3"""
    result = subprocess.run([
        '../v0.0.7.3/runac', source, output
    ], capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def compile_with_v0075(source, output):
    """Compile with v0.0.7.5"""
    result = subprocess.run([
        './build/runac', source, output
    ], capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def compare_assembly(file1, file2):
    """Compare assembly files line by line"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Generate diff
    diff = list(difflib.unified_diff(lines1, lines2,
                                   fromfile='v0.0.7.3',
                                   tofile='v0.0.7.5'))

    return len(diff) == 0, diff

def test_program(source_file):
    """Test a single program against both compilers"""
    print(f"Testing {source_file}...")

    # Compile with both versions
    success_v0073, error_v0073 = compile_with_v0073(source_file, 'test_v0073.s')
    success_v0075, error_v0075 = compile_with_v0075(source_file, 'test_v0075.s')

    # Both should succeed or both should fail
    if success_v0073 != success_v0075:
        print(f"FAIL: Compilation results differ")
        print(f"v0.0.7.3: {'SUCCESS' if success_v0073 else 'FAIL'}")
        print(f"v0.0.7.5: {'SUCCESS' if success_v0075 else 'FAIL'}")
        return False

    # If both failed, check error messages
    if not success_v0073:
        if error_v0073.strip() != error_v0075.strip():
            print(f"FAIL: Error messages differ")
            print(f"v0.0.7.3: {error_v0073}")
            print(f"v0.0.7.5: {error_v0075}")
            return False
        print(f"PASS: Both failed with same error")
        return True

    # Compare assembly output
    identical, diff = compare_assembly('test_v0073.s', 'test_v0075.s')
    if not identical:
        print(f"FAIL: Assembly output differs")
        for line in diff:
            print(line.rstrip())
        return False

    print(f"PASS: Identical output")
    return True

# Test all programs in test suite
test_programs = [
    'tests/test_simple.runa',
    'tests/test_arithmetic.runa',
    'tests/test_functions.runa',
    'tests/test_conditions.runa',
    'tests/test_loops.runa',
]

all_passed = True
for program in test_programs:
    if not test_program(program):
        all_passed = False

sys.exit(0 if all_passed else 1)