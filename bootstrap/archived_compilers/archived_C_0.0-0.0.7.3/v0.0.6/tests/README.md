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
# v0.0.6 Test Suite

This directory contains comprehensive tests for the v0.0.6 Runa compiler.

## Test Files

### Core Functionality Tests
- `test_minimal_working.runa` - Basic compilation and print statement
- `test_print_integer_regression.runa` - Regression test for print integer fix
- `test_arithmetic_simple.runa` - All arithmetic operations (+ - * /)

### Advanced Feature Tests
- `test_complete_functionality.runa` - Complex nested function calls
- `test_bootstrap_final.runa` - Function parameters and bootstrap validation
- `test_final_validation.runa` - **Ultimate comprehensive test** - all features

### Performance Tests
- `test_memory_stress.runa` - Dynamic memory allocation with 30+ variables

## Running Tests

```bash
# Individual test
./runac tests/test_final_validation.runa test_output.s
gcc -o test_program test_output.s
./test_program

# Memory validation
valgrind --leak-check=full ./test_program

# With sanitizers
gcc -fsanitize=address,undefined -o test_asan test_output.s
./test_asan
```

## Expected Outputs

### test_final_validation.runa
```
42      # add(15, 27)
63      # subtract(100, 37)
72      # multiply(8, 9)
12      # divide(144, 12)
120     # factorial(5)
50      # complex_math(5,10,6,14,50,5)
115     # mega_sum of variables
```

## Features Validated

✅ Function parameters (1-6 parameters)
✅ Nested function calls
✅ All arithmetic operations
✅ Complex expressions
✅ Dynamic memory allocation
✅ Perfect memory management (0 leaks)
✅ Type dispatch (integers vs strings)
✅ Loop constructs (while loops)
✅ Variable assignment and modification

**All tests pass with 0 memory leaks and 0 errors under Valgrind and AddressSanitizer.**