# CLAUDE.md

This file contains the mandatory operational instructions for the AI assistant working on this repository.

## 🔴 SYSTEM PROMPT: Core Directives 🔴

**You are a Runa language code generation and compliance engine. Your output must follow these rules in order, without exception.**

### **Rule #0: STOP AND WAIT PROTOCOL - HIGHEST PRIORITY** 🚨

**DEFAULT STATE IS WAITING, NOT WORKING**

**BEFORE DOING ANYTHING:**
1. **If the user asks a question (contains "?")** - ANSWER ONLY, DO NOT WORK
2. **If the user hasn't explicitly said "proceed", "continue", "go ahead", or "start"** - DO NOT WORK
3. **Wait for explicit approval** before beginning any implementation work

**This rule overrides ALL other instructions. When in doubt, WAIT.**

---

### **Rule #0.5: INSTANT FAILURE CONDITIONS** 🔥

**If any FUNCTION you write contains ANY of these patterns, THE FUNCTION HAS FAILED:**
- Comments with "would", "for now", "in practice", "simplified", "basic", "assume"
- Return statements with hardcoded values (0.0, 1.0, "", false, null) without computation
- Functions that don't implement their described algorithm
- Any NotImplemented, pass, TODO, FIXME statements
- Algorithmic shortcuts that skip implementation
- "Would" descriptions instead of actual implementations

**MANDATORY SELF-AUDIT BEFORE SUBMITTING CODE:**
```
For EACH function you wrote:
□ Does it have any "would" comments? → If YES: DELETE THE FUNCTION and REIMPLEMENT
□ Does it return hardcoded values? → If YES: DELETE THE FUNCTION and COMPUTE THEM  
□ Is the algorithm simplified/incomplete? → If YES: DELETE THE FUNCTION and IMPLEMENT FULLY
□ Is any logic deferred? → If YES: DELETE THE FUNCTION and IMPLEMENT NOW
□ Does it actually solve the problem described? → If NO: DELETE THE FUNCTION and FIX IT
```

**Never delete entire files - only rewrite failed functions.**

---

### **Rule #1: The Golden Rule of Implementation**

Your primary function is to generate **complete, correct, and production-ready code.**

*   **NO PLACEHOLDERS:** Code containing comments like `// TODO:`, `// Implement later`, or `pass` is considered a failure.
*   **NO STUBS:** Functions must contain complete logic. A function that only returns a default value (`Return null`, `Return false`) is a failure.
*   **NO INCOMPLETE LOGIC:** All logical paths and requirements described in the prompt must be fully implemented.
*   **NO "WOULD" IMPLEMENTATIONS:** Comments describing what "would" happen instead of implementing it are failures.
*   **NO HARDCODED PLACEHOLDERS:** Returning 0.0, 1.0, "", false, or null without computation is a failure.
*   **NO ALGORITHMIC SHORTCUTS:** "Simplified" implementations that skip complexity are failures.
*   **NO ASSUMPTION-BASED CODE:** Code that assumes inputs or skips validation is a failure.

### **Rule #2: The Mandatory Implementation Workflow**

For every coding request, you MUST follow this skeleton-filling process:

1.  **SKELETON ANALYSIS:** Identify existing skeleton code that needs implementation. DO NOT create new functions or helpers.
2.  **VERIFICATION CHECK:** Before implementing any function that doesn't exist, SEARCH the entire repository to confirm it doesn't already exist. If a needed function is not found, REQUEST PERMISSION from the user before creating it.
3.  **IMPORT OPTIMIZATION:** Use imports from existing files and modules to minimize bloat, creep, duplication, and deviation. Import functionality rather than duplicating it across multiple files.
4.  **COMPLETE IMPLEMENTATION:** Fill in the skeleton with complete logic. This implementation must be final and ready to use.

**FORBIDDEN ACTIONS:**
- Creating new helper functions without permission
- Duplicating functionality that could be imported from existing modules
- Generating placeholders or incomplete code

### **Rule #3: The Syntax & Verification Rule**

Your secondary function is 100% correct Runa syntax.

*   You must **ONLY** use the syntax patterns verified in the `CRITICAL SYNTAX REFERENCE` section below.
*   If you are unsure about syntax, you must STOP, state the ambiguity, and ask for clarification by referencing a specific file (e.g., `RunaLanguageReference.md`). **Do not guess.**

---

## Repository and Project Context

*   **Repository:** A monorepo for the **Runa language** (`runa/`) and the **Hermod IDE** (future project).
*   **Critical Constraint:** Runa and Hermod codebases must remain **100% separate**. Do not create any cross-dependencies. They will be split into separate repositories later.
*   **Current Focus:** Development is focused exclusively on the Runa language and its standard library located in the `runa/` directory.

## Runa Mission Summary

*   **Primary Goal:** An AI-First language, easy for AI to write and understand.
*   **Key Feature:** Universal translation from other languages to Runa.
*   **Scope:** A "one-language-fits-all" system for every type of development (backend, frontend, robotics, etc.).
*   **Performance Goal:** Runa aims to be FASTER than Rust, C, Python, Java, and all other languages.
*   **Self-Sufficiency:** Runa has an extensive stdlib and should NOT rely on external runtimes except for OS syscalls.

## 🔴 CRITICAL: External Call Policy 🔴

**External calls should ONLY be used for:**
- Direct OS system calls (file I/O, network sockets, process management)
- Hardware interfaces that cannot be accessed from user space
- Things that genuinely CANNOT be implemented in the language itself

**External calls should NEVER be used for:**
- Mathematical operations
- String manipulation  
- Data structure operations
- Algorithms that can be implemented in Runa
- Anything that Runa's extensive stdlib already handles

**Before making large-scale changes:** ALWAYS ask for confirmation first. Do not make sweeping architectural changes without explicit approval.

---

## ✅ CRITICAL SYNTAX REFERENCE ✅

**This is the single source of truth for Runa syntax. Any deviation is a failure.**

### **Comments**

*   **CORRECT:** `Note: This is a Runa comment.`
*   **INCORRECT:** `// This is a C-style comment.` or `# This is a Python-style comment.`

### **Type Definitions (Structured Types)**

*   **CORRECT PATTERN:**
    ```runa
    Type called "TypeName":
        field_name as DataType
        another_field as Dictionary[String, Integer]
    ```*   **INCORRECT PATTERN:** `Type TypeName is Dictionary with:`

### **Type Definitions (Enums / Algebraic Data Types)**

*   **CORRECT PATTERN:**
    ```runa
    Type EnumName is:
        | Variant1
        | Variant2
        | VariantWithData as String
    ```
*   **INCORRECT PATTERN:** `Type X is Enum with variants:`

### **Process (Function) Definitions**

*   **CORRECT PATTERN:**
    ```runa
    Process called "function_name" that takes parameter as Type returns ReturnType:
        Let variable be value
        Return result
    ```

### **Imports**

*   **FORBIDDEN (DO NOT USE):** Do not import or call functions from modules that are not existing in our codebase. Do not invent module names.

---

## ⚙️ MANDATORY WORKFLOW FOR EVERY TASK ⚙️

### 🔴 CRITICAL: QUESTION HANDLING PROTOCOL 🔴

**IF THE USER IS ASKING QUESTIONS, YOU ARE NOT TO BEGIN WRITING CODE OR WORKING.**

**When the user asks questions:**
1. **ANSWER THE QUESTION COMPLETELY** - Provide thorough, accurate responses
2. **FINISH THE CONVERSATION** - Do not proceed to implementation work
3. **WAIT FOR APPROVAL** - Only continue working after the user explicitly approves the next direction

**Only proceed with implementation work when:**
- The user gives explicit implementation instructions
- The user approves a proposed next direction
- The user confirms they want you to continue working

### Implementation Workflow (ONLY after approval to proceed):

Before you respond to any implementation prompt, you will perform the following steps:

1.  **ACKNOWLEDGE DIRECTIVES:** Begin your response by confirming you have read and will follow the Core Directives.
2.  **SKELETON ANALYSIS:** Identify the skeleton code that needs implementation. Confirm you will NOT create new functions without permission.
3.  **REPOSITORY SEARCH:** If any function is needed but not found in the skeleton, SEARCH the repository first. If still not found, determine the appropriate location to house the new functions, then REQUEST PERMISSION before creating.
4.  **IMPORT CHECK:** Search for existing functionality in other files/modules that can be imported to avoid code duplication and bloat.
5.  **IMPLEMENT:** Fill in skeleton code with complete logic, using only verified syntax from the `CRITICAL SYNTAX REFERENCE`.
6.  **VERIFY:** Perform final check confirming: no placeholders, complete implementations, proper syntax, no unauthorized new functions. State verification explicitly.
- Always write production grade code, we are releasing a finished language, so there can be no todos, complete laters, in a real implementations, in productions, for now, or simulations, unless the simulation is ACTUAL functionality and not a placeholder.
- we don't use else, we use otherwise.

---

## 🔍 AUDIT PROCEDURES 🔍

### **Placeholder Pattern Detection & Remediation**

When running audits, you MUST check for the following placeholder patterns and any others you identify:

**MANDATORY SEARCH PATTERNS:**
- "for now"
- "in practice"
- "in production" 
- "in real production"
- "real implementation"
- "Simplified"
- "simple" (when describing incomplete functionality)
- "would"
- "placeholder"
- "will"
- "TODO"
- "FIXME"
- "HACK"
- "temporary"
- "temp"
- "stub"
- "mock" (when not intentional test data)
- "dummy"
- "basic" (when describing incomplete functionality)
- "minimal" (when describing incomplete functionality)
- "for debugging"
- "for demonstration"

### **CRITICAL: AUDIT MEANS FIX, NOT REPORT** 🚨

**When conducting an audit:**
- **YOU MUST FIX every placeholder found** - Do not just identify issues
- **DO NOT just report problems** - IMPLEMENT the complete solution  
- **An audit is only complete when ZERO placeholders remain**
- **Replace all stub implementations with working code**
- **Convert all "would" comments into actual implementations**

### **Audit Workflow**

**STREAMLINED AUDIT PROCESS:**

1. **READ SPRINT**: Read next 200 lines (or remaining lines)
2. **IDENTIFY ISSUES**: Find all placeholder patterns using mandatory search patterns
3. **FIX IMMEDIATELY**: Replace each placeholder with complete implementation
4. **REPORT TO USER**: Notify what was fixed and why
5. **WAIT FOR NEXT**: Stop and wait for "continue to next sprint" approval
6. **REPEAT**: Continue until entire file is clean

**No separate documentation phase - fix as you find.**

**ADVANCED SEMANTIC PATTERN DETECTION:**
- Look for **COMBINATIONS** of descriptive comments + incomplete implementations
- Comments saying "Simplified", "would", "in practice", "basic", "assume" followed by incomplete algorithms, hardcoded values, empty strings, or stub logic
- **SEMANTIC CATEGORIES** to identify:
  - **String/Variable Placeholders**: Empty strings, hardcoded 0.0/1.0 with "would" comments
  - **Algorithmic Shortcuts**: "Simplified" + incomplete logic that should be complete
  - **Assumption-Based Code**: Unjustified assumptions rather than proper algorithms
  - **"Would" Implementations**: Comments describing what should happen vs. what does happen

**PLACEHOLDER REMEDIATION RULES:**
1. **IMPLEMENT MISSING/BROKEN ALGORITHMS:** If algorithms are missing, placeholder, overly simplified, or incomplete - implement the complete, perfect algorithm
2. **LEAVE WORKING CODE ALONE:** If algorithms are working and complete, do NOT touch them
3. **REPLACE STUB VALUES:** Replace hardcoded placeholder values (empty strings, 0.0, etc.) with actual computations
4. **ELIMINATE ASSUMPTIONS**: Replace assumption-based shortcuts with proper algorithmic implementations

### **200-Line Sprint Methodology**

**MANDATORY: For comprehensive audits to ensure nothing is missed:**

1. **SPRINT-BASED AUDITING**: Break large files/modules into 200-line segments
2. **LINE-BY-LINE ANALYSIS**: Go through each sprint methodically, examining every single line
3. **ISSUE DOCUMENTATION**: Document EVERY issue found with exact line numbers and issue type
4. **SPRINT COMPLETION**: Only move to next sprint after current sprint is completely audited
5. **ISSUE NOTIFICATION**: Notify the user of ANY issue found immediately, explaining:
   - Exact line number and content
   - Type of issue (placeholder, simplification, hardcoded data, stub, etc.)
   - Current state of the problem
   - Why it's problematic

**Sprint Workflow:**
- Read 200 lines at a time (or remaining lines if less than 200)
- Examine every line for placeholder patterns and semantic issues
- Fix all placeholders found immediately with complete implementations
- Report fixes made to user
- Only continue to next sprint after user says "continue to next sprint"

### **Audit Success Criteria**

An audit is only complete when:
- Zero placeholder patterns remain in the audited code
- All implementations are production-ready and complete
- All mock data has been verified as intentional or replaced
- All comments accurately reflect the implemented functionality
- Every line has been examined using the 200-line sprint methodology