# RUNA COMPILER BOOTSTRAP - AGENT DIRECTIVE

## YOUR MISSION
You are building the Runa programming language compiler through a precise 5-phase bootstrap process. This is a critical, multi-month effort to create a completely self-hosted, LLVM-independent compiler system.

## CURRENT STATUS
**Phase**: v0.2 IMPLEMENTATION (Runa + Assembly)
**Location**: `/runa/bootstrap/v0.2_self-hosted/`
**Progress**: v0.1 COMPLETE - Ready to implement v0.2
**Next Task**: Create v0.2 project structure and begin Runa compiler in Runa

## THE IMMUTABLE PLAN
**Your Bible**: `/runa/docs/dev/Last_Effort_Compiler_Bootstrapping.md`
**Progress Tracker**: `/runa/docs/dev/Bootstrap_Progress.md`
**Language Spec**: `/runa/docs/user/language-specification/`
**Syntax Reference**: See Section "MANDATORY LANGUAGE COMPLIANCE" below

This specification document is THE LAW. You will:
1. Follow it to the letter - no deviations
2. Implement features in the EXACT order specified
3. Complete ALL checkpoints before moving to next phase
4. Update progress tracker after EVERY task
5. Use ONLY verified Runa syntax patterns
6. NEVER create duplicate functions or unnecessary helpers

## THE BOOTSTRAP CHAIN

```
v0.1 (Rust+LLVM) → v0.2 (Runa+Assembly) → v0.3 (Runa+MIR/LIR) → v0.4 (Production) → v0.5 (Complete)
     ✅ COMPLETE        ↑ WE ARE HERE
```

### v0.2 REQUIREMENTS (Current Phase)

**STEP 1: PROJECT SETUP**
- [ ] Create v0.2 directory structure
- [ ] Write minimal Runa compiler skeleton in Runa
- [ ] Set up compilation pipeline using v0.1

**STEP 2: CORE COMPILER STRUCTURE**
- [ ] Lexer implementation in Runa
- [ ] Parser implementation in Runa
- [ ] AST definitions
- [ ] Symbol table management

**STEP 3: ASSEMBLY GENERATION**
- [ ] x86-64 instruction emitter
- [ ] Register allocator (simple)
- [ ] Stack management
- [ ] Function call conventions

**STEP 4: FEATURE IMPLEMENTATION**
- [ ] Arithmetic code generation
- [ ] Control flow generation
- [ ] String handling
- [ ] File I/O syscalls

**STEP 5: SELF-HOSTING TEST**
- [ ] Compile v0.2 with itself
- [ ] Verify generated assembly
- [ ] Bootstrap validation

**v0.1 Status**: ✅ ALL FEATURES COMPLETE - Ready to compile v0.2!

## YOUR WORKING RULES

### 1. BEFORE STARTING ANY TASK
- Read the relevant section in Last_Effort_Compiler_Bootstrapping.md
- Verify it's the NEXT required task for current phase
- State: "Implementing [FEATURE] per spec Section X.X"

### 2. MANDATORY LANGUAGE COMPLIANCE
**You MUST use ONLY these verified Runa syntax patterns:**

#### Correct Syntax Examples:
```runa
Note: Comments use "Note:" not // or #

Process called "function_name" that takes param as Type returns ReturnType:
    Let variable be value
    Set variable to new_value
    Return result
End Process

Let list be a list containing 1, 2, 3
Let dict be a dictionary containing:
    "key" as "value"
End Dictionary

If condition:
    statements
Otherwise:
    statements
End If

For Each item in collection:
    statements
End For

While condition:
    statements
End While
```

#### FORBIDDEN Syntax:
- `//` or `#` comments → Use `Note:`
- `else` → Use `Otherwise`
- `=` for assignment → Use `be` or `to`
- `+` `-` `*` `/` → Use `plus`, `minus`, `multiplied by`, `divided by`
- `>` `<` `==` → Use `is greater than`, `is less than`, `is equal to`

### 3. ANTI-BLOAT REQUIREMENTS

#### BEFORE Creating ANY New Function:
1. **SEARCH FIRST**: Use grep/find to search ENTIRE repository
2. **VERIFY ABSENCE**: Confirm function doesn't exist anywhere
3. **CHECK IMPORTS**: Look for similar functionality in other modules
4. **REQUEST PERMISSION**: Ask user before creating new helper functions

#### Import Protocol:
```runa
Note: ALWAYS import existing functionality
Import "compiler/utils/string_helpers" as StringHelpers
Let result be StringHelpers.concat(str1, str2)

Note: NEVER duplicate existing functions
```

#### Example Search Before Implementation:
```bash
# Before implementing string_concat
grep -r "string_concat" /runa/
grep -r "concat" /runa/src/
find /runa -name "*.runa" -exec grep -l "concatenate" {} \;

# If found, IMPORT it. If not found, REQUEST permission to create.
```

### 4. IMPLEMENTATION REQUIREMENTS
- NO placeholders, TODOs, or stub implementations
- Every function must be COMPLETE and WORKING
- Follow existing code patterns in v0.1 codebase
- Test with provided test cases in the spec
- NO HELPER FUNCTIONS without explicit permission

### 5. AFTER COMPLETING ANY TASK
- Run the test case from the spec
- Update Bootstrap_Progress.md checkpoints
- Report: "Completed [FEATURE]. X/8 features done."
- Identify the next required task

## CRITICAL CONSTRAINTS

### WHAT YOU MUST DO
✓ Implement ONLY features listed in current phase
✓ Use existing LLVM infrastructure in v0.1
✓ Maintain backward compatibility
✓ Write complete, production-ready code
✓ Test everything before marking complete

### WHAT YOU MUST NOT DO
✗ Skip ahead to future phases
✗ Add features not in the specification
✗ Change the architecture without approval
✗ Leave any TODOs or placeholders
✗ Claim completion without testing

## NEXT IMMEDIATE TASK

**CREATE v0.2 PROJECT STRUCTURE**
Location: `/runa/bootstrap/v0.2_self-hosted/`
Action: Set up v0.2 directory and begin writing Runa compiler in Runa

Setup process:
1. Create v0.2 directory structure
2. Write main compiler entry point in Runa
3. Begin with lexer implementation
4. Test compilation with v0.1

Example project setup:
```bash
# Create v0.2 structure
mkdir -p /runa/bootstrap/v0.2_self-hosted/{src,tests}

# Write main.runa
echo 'Process called "main" returns Integer:
    Note: v0.2 Runa Compiler Entry Point
    Return 0
End Process' > main.runa

# Compile with v0.1
../v0.1_runa-bootstrap/target/release/runac main.runa -o main.o
gcc -no-pie main.o -o runac_v02
./runac_v02
echo $?  # Should be 0
```

This marks the transition from v0.1 (Rust+LLVM) to v0.2 (Runa+Assembly).

## SUCCESS METRICS

You are successful when:
1. v0.2 compiler written entirely in Runa (no Rust code)
2. v0.2 generates x86-64 assembly (no LLVM dependency)
3. v0.2 can compile itself (self-hosting achieved)
4. Bootstrap_Progress.md shows all v0.2 checkpoints complete
5. LLVM liberation achieved - no external dependencies except OS syscalls

## REPORTING FORMAT

Always report status as:
```
BOOTSTRAP STATUS:
Phase: v0.2 Self-Hosted Implementation
Current Task: [WHAT YOU'RE WORKING ON]
Completed: X/5 phases
Next Task: [WHAT'S NEXT]
Blockers: [ANY ISSUES]
v0.1 Status: ✅ COMPLETE
```

## COMMON VIOLATIONS TO AVOID

### ❌ BLOAT VIOLATIONS:
- Creating `string_utils.runa` when string functions already exist elsewhere
- Writing `helper_function()` without searching for existing implementations
- Duplicating code instead of importing from existing modules
- Adding 10 helper functions when 1 import would suffice

### ❌ SYNTAX VIOLATIONS:
```runa
Note: WRONG
// This is a comment     ← NO!
x = 5                    ← NO!
if x > 10:               ← NO!
else:                    ← NO!
result = a + b           ← NO!
let x as 5               ← NO!

Note: CORRECT
Note: This is a comment  ← YES!
Note: This a 
comment block
:End Note                ← YES!
Let x be 5               ← YES!
If x is greater than 10: ← YES!
Otherwise:               ← YES!
Let result be a plus b   ← YES!
```

### ❌ IMPLEMENTATION VIOLATIONS:
- Leaving TODO comments
- Returning hardcoded 0 or "" as placeholders
- Writing "This would..." instead of implementing
- Skipping error handling with "assume valid input"
- Creating stub functions that don't work

## REMEMBER

- The specification is LAW - follow it exactly
- Complete means COMPLETE - no shortcuts
- Test everything - no assumptions
- Update progress - every single task
- Stay in current phase - no jumping ahead
- SEARCH before creating - minimize bloat
- IMPORT before duplicating - reuse existing code
- Use PROPER Runa syntax - no C/Python/Rust patterns

## START COMMAND

When ready to begin work, you will say:
"Bootstrap Protocol Engaged. v0.1 verified complete. Beginning v0.2 self-hosted implementation phase. Creating Runa compiler written in Runa that generates assembly."

Then proceed with v0.2 project setup and implementation per specification.

---

*This is your mission. The specification is your guide. The bootstrap chain is your path. Execute precisely.*