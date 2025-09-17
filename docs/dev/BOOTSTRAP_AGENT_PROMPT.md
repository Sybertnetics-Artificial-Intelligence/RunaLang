# RUNA COMPILER BOOTSTRAP - AGENT DIRECTIVE

## YOUR MISSION
You are building the **Runa compiler** from scratch under the **Last Effort Bootstrap Plan**.
The prior v0.1 bootstrap attempt has been **abandoned**.
Your immediate mission is to implement the **v0.0 Rust seed compiler** for the MicroRuna subset using standard Rust toolchain.

---

## CURRENT STATUS
**Phase**: v0.0 IMPLEMENTATION (Rust Seed)  
**Location**: `/runa/bootstrap/v0.0_rust-seed/`  
**Progress**: Starting from an empty directory  
**Next Task**: Implement lexer, parser, type checker, and code generator using Rust's LLVM backend for MicroRuna.

---

## THE IMMUTABLE PLAN
- **Spec**: `/runa/docs/dev/Last_Effort_Compiler_Bootstrapping.md`  
- **Progress Tracker**: `/runa/docs/dev/Bootstrap_Progress.md`  
- **Subset**: MicroRuna only (see spec).  

This plan is law:
- No extra features.
- Use standard Rust toolchain (LLVM backend acceptable for v0.0).
- No optimizations.
- No placeholders.  

---

## SYNTAX COMPLIANCE RULES

### Correct Examples
```runa
Note: Comments use "Note:" not //

Process called "add" that takes a as Integer, b as Integer returns Integer:
    Let result be a plus b
    Return result
End Process

If condition:
    Print "yes"
Otherwise:
    Print "no"
End If
```

### Forbidden
- `//` or `#` comments  
- `=` assignment (use `be` / `to`)  
- `+`, `-`, `*`, `/` (use `plus`, `minus`, `multiplied by`, `divided by`)  
- `==`, `<`, `>` (use natural-language forms)

---

## IMPLEMENTATION APPROACH: RUST-FIRST STRATEGY

**Build Rust capabilities first, then constrain MicroRuna to what actually works.**

### PHASE 1: Ultra-Minimal Proof of Concept
- Lexer for: identifiers, integers, `Let`, `be`, `Print`
- Parser for: `Let x be 42` and `Print x`
- Code generator that outputs working executable
- **Goal**: Get trivial programs compiling and running

### PHASE 2: Incremental Expansion
- Add arithmetic: `plus`, `minus`
- Add basic conditionals: `If`/`Otherwise`
- Add function definitions and calls
- **Each addition defines MicroRuna scope**

### PHASE 3: Self-Hosting Foundation
- Add strings, lists, file I/O
- Add while loops
- **Guided by**: "What do we need to write a lexer/parser in MicroRuna?"

### STEP 4: Test and Validate
- Create `test_micro.runa` using implemented features
- Compile → run → verify outputs
- Expand tests as capabilities grow  

---

## REPORTING FORMAT

Always report status as:
```
BOOTSTRAP STATUS:
Phase: v0.0 Rust Seed Implementation
Current Task: [WHAT YOU'RE DOING]
Next Task: [WHAT'S NEXT]
Blockers: [ANY ISSUES]
```

---

## START COMMAND
When ready to begin, state:
**"Previous bootstrap attempt abandoned. Beginning v0.0 Rust Seed implementation using standard Rust toolchain. The goal is a minimal compiler for the MicroRuna subset."**
