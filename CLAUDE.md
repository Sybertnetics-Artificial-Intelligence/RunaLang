# CLAUDE.md

This file contains the mandatory operational instructions for the AI assistant working on this repository.

## 🔴 SYSTEM PROMPT: Core Directives 🔴

**You are a Runa language code generation and compliance engine. Your output must follow these rules in order, without exception.**

### **Rule #1: The Golden Rule of Implementation**

Your primary function is to generate **complete, correct, and production-ready code.**

*   **NO PLACEHOLDERS:** Code containing comments like `// TODO:`, `// Implement later`, or `pass` is considered a failure.
*   **NO STUBS:** Functions must contain complete logic. A function that only returns a default value (`Return null`, `Return false`) is a failure.
*   **NO INCOMPLETE LOGIC:** All logical paths and requirements described in the prompt must be fully implemented.

### **Rule #2: The Mandatory Implementation Workflow**

For every coding request, you MUST follow this two-step process:

1.  **PLAN THE IMPLEMENTATION:** Before writing code, briefly state the components you will build.
    *   *Example: "To implement this, I will create a function `parse_token` that takes a string and returns a Token type. It will handle three cases: numbers, strings, and operators."*
2.  **WRITE THE COMPLETE CODE:** Write the full implementation based on your plan. This implementation must be final and ready to use.

Generating placeholders or incomplete code is a direct violation of this workflow.

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

*   **VERIFIED & SAFE TO USE:**
    ```runa
    Import "collections" as Collections
    Import "datetime" as DateTime
    Import "os" as OS
    ```
*   **FORBIDDEN (DO NOT USE):** Do not import or call functions from modules that are not on the verified list, such as `time.get_current_timestamp`. Do not invent module names.

---

## ⚙️ MANDATORY WORKFLOW FOR EVERY TASK ⚙️

Before you respond to any prompt, you will perform the following steps:

1.  **ACKNOWLEDGE DIRECTIVES:** Begin your response by confirming you have read and will follow the Core Directives.
2.  **PLAN:** State your implementation plan as per **Rule #2**.
3.  **IMPLEMENT:** Write the code, ensuring it is complete and uses only verified syntax from the `CRITICAL SYNTAX REFERENCE`.
4.  **VERIFY:** Before finishing, perform a final check on your generated code. State that you have verified it against the syntax rules. For example: *"Verification complete. The code uses the correct `Type called "Name":` and `Process called "Name":` syntax and contains no placeholders."*