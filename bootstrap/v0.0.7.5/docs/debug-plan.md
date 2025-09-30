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
# Debug Plan for Transitional Compiler

## Objective
Debug and fix the transitional compiler (v0.0.7.5 compiled by v0.0.7.3 with 32-bit offsets) to achieve self-hosting.

## Current State
- v0.0.7.3 successfully compiles v0.0.7.5 source to assembly
- Assembly assembles and links successfully with complete runtime
- Debug output shows failure in parser_parse_program
- Parser fails immediately when trying to parse even "return 42"

## Phase 1 Results (COMPLETED)
- Added debug prints to main.runa
- Found failure point: parser_parse_program returns NULL
- Execution flow: main → lexer_create (OK) → parser_create (OK) → parser_parse_program (FAILS)

## Phase 2 Results (COMPLETED)
- Added detailed debug prints to parser
- Discovered root cause: v0.0.7.5 uses different syntax keywords
- Parser expects "Process" not "Function" and "End Process" not "End"
- With correct syntax, parsing succeeds but program hangs in codegen_create

## Phase 3 Results (COMPLETED)
- Found bug: file_open_fd called with string "w" instead of integer 1
- Fixed the parameter type mismatch

## Phase 4 Results (COMPLETED)
- Fixed file_open_fd call in codegen.runa (was passing string "w" instead of integer 1)
- Fixed lexer bug: LEXER_POSITION global not updated properly
- Fixed position tracking in lexer struct at offset 8
- Parser now correctly reads function names
- Stage 1 compiler successfully compiles test programs

## Phase 5 Results (COMPLETED)
- Stage 1 successfully parses all v0.0.7.5 source files
- Generates assembly output for all 7 modules
- Issue: Assembly output corrupted with debug strings
- Corruption pattern: "codegen_find_variable codegen_calculate_type_s" mixed into output
- Root cause: file_write_fd was called with only 2 parameters instead of 3
- **FIX APPLIED**: Added third parameter (0) to all file_write_fd calls in codegen.runa
- **RESULT**: Clean assembly output generated successfully!

## Phase 6 Results (PARTIAL SUCCESS)
- Successfully compiled all v0.0.7.5 modules with v0.0.7.3 (Stage 1)
- Clean assembly output without corruption
- Stage 2 assembled and linked successfully
- Issue: Stage 2 segfaults when trying to parse input (runtime ABI mismatch)
- **ACHIEVEMENT**: Assembly corruption fixed, clean code generation achieved

## Debug Plan

### Phase 1: Isolate Failure Point
**Goal:** Determine exactly where in the compilation pipeline the failure occurs.

**Actions:**
1. Add debug prints to `main.runa` in transitional source:
   - After command line argument parsing
   - After input file reading
   - After lexer creation
   - After parser creation
   - Before and after parsing
   - Before code generation
   - After code generation
   - Before file writing

**Success Criteria:** Know the exact function where failure occurs.

### Phase 2: Trace the Failure
**Goal:** Understand why the failure happens at that point.

**Actions:**
1. Once failure point is identified, add detailed prints:
   - All pointer values before dereferencing
   - All struct field accesses with offsets
   - String contents and lengths
   - Function arguments and return values
   - Memory allocation sizes

**Success Criteria:** Understand the root cause (null pointer, wrong offset, corrupted data, etc.).

### Phase 3: Compare with v0.0.7.3
**Goal:** Understand the behavioral difference between working v0.0.7.3 and broken transitional.

**Actions:**
1. Create identical test program
2. Run through v0.0.7.3 with same debug points
3. Compare:
   - Memory layouts
   - String handling
   - Struct offsets
   - Function call sequences

**Success Criteria:** Identify the specific mismatch causing the failure.

### Phase 4: Fix the Specific Bug
**Goal:** Make minimal targeted fix to transitional source.

**Actions based on bug type:**
- **Wrong offset:** Adjust the specific field offset in transitional source
- **String corruption:** Fix string handling functions or buffer sizes
- **Null pointer:** Fix initialization or allocation
- **Size mismatch:** Adjust memory allocation sizes

**Success Criteria:** Transitional compiler successfully compiles "return 42" program.

### Phase 5: Verify and Iterate
**Goal:** Ensure transitional compiler works for increasingly complex programs.

**Test sequence:**
1. `return 42` - simplest program
2. `print_string("Hello")` - basic string handling
3. `Let x be 5 + 3` - arithmetic and variables
4. Compile simple .runa file with multiple functions
5. Compile each v0.0.7.5 module

**Success Criteria:** Transitional compiler can compile all v0.0.7.5 source files.

### Phase 6: Achieve Self-Hosting
**Goal:** Use transitional compiler to bootstrap real v0.0.7.5.

**Actions:**
1. Use transitional compiler to compile real v0.0.7.5 source (with 64-bit offsets) → Stage 2
2. Use Stage 2 to compile v0.0.7.5 source → Stage 3
3. Verify Stage 3 binary matches Stage 2 (or produces identical output)

**Success Criteria:** Stage 3 successfully compiles test programs, proving self-hosting achieved.

## Deviation Policy
If ANY step fails or produces unexpected results, STOP immediately and report:
- Which phase/step failed
- What was expected vs what happened
- Any error messages or unexpected output

DO NOT attempt workarounds or skip steps.