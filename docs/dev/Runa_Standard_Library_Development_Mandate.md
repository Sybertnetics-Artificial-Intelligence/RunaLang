# Runa Standard Library Implementation: Core Development Mandate

## 1. Objective

Your primary mission is to implement the complete Runa Standard Library **in the Runa language itself**. This is not a prototyping exercise; it is the foundational implementation of a production-grade, AI-first programming language. The goal is to build a library that is robust, comprehensive, and intuitive, enabling Runa to become a practical, self-hostable language capable of complex application development. Writing the library in Runa is the critical first step to "dogfood" the language and drive the compiler to completion.

## 2. Guiding Philosophy & Core Reference

All development **must** be executed in strict accordance with the principles and structure laid out in the **[Runa Standard Library Manifesto](./Runa%20Standard%20Library%20Manifesto.md)**. This document is your single source of truth for the library's design, scope, and "AI-first" philosophy. Before implementing any module, review the relevant sections of the manifesto to ensure your code aligns with its vision.

## 3. The Uncompromising Standard: Production-Ready & Complete Runa Code

This is the most critical directive. Every line of Runa code you write must be **finished and production-ready**. The concept of "placeholder code" is antithetical to this project's goals.

**"Complete" means:**
-   **No Placeholders:** Under no circumstances should you write stub functions that do nothing or simply return a default value.
-   **No "TODO" or "FIXME":** Do not leave comments indicating incomplete work. If a function or class is in the file, it must be fully implemented.
-   **Full Functionality:** Every declared function must have a complete and correct implementation of its intended logic, written in Runa.
-   **Comprehensive Error Handling:** All functions must anticipate and gracefully handle invalid inputs, edge cases, and potential runtime errors using Runa's error handling mechanisms (e.g., raising exceptions).
-   **Rigorous Type Annotations:** All functions, methods, and variables must use precise Runa type annotations as defined in the language specification.
-   **Documentation Comments:** Every module, class, and function must have a clear, concise documentation comment explaining its purpose, parameters, and return value, following the Runa language specification for documentation.

You are building the standard library for a language intended to power next-generation AI systems. The quality, reliability, and completeness of your work must reflect that ambition. There is no "later" to fix things; the code must be correct and complete upon delivery.

## 4. Structure & Scope

The blueprint for the standard library is the file skeleton already created in `runa/src/runa/stdlib/`. You are to populate these files, ensuring they have a `.runa` extension. Do not deviate from this structure unless a compelling, manifesto-aligned reason exists.

## 5. Compiler-Driven Implementation Order

This is a "compiler-driven" development process. We will write the standard library in Runa, and then implement the compiler features necessary to make that Runa code work. This dogfooding process is essential for achieving self-hosting.

The recommended implementation order is:

1.  **Core Primitives & Builtins:**
    -   `stdlib/types`
    -   `stdlib/builtins`
2.  **Fundamental Data Structures:**
    -   `stdlib/collections` (list, dict, set first)
3.  **System Interaction:**
    -   `stdlib/io`
    -   `stdlib/os`
4.  **Core Utilities:**
    -   `stdlib/math`
    -   `stdlib/string`
    -   `stdlib/datetime`
5.  **Remaining Modules:** Proceed through the rest of the structure as logically as possible.

## 6. Final Deliverable

Your final output for each module will be a set of fully implemented Runa files (e.g., `list.runa`). When you claim a module (e.g., `stdlib.collections.list`) is complete, it means that `list.runa` contains a production-ready implementation of a list data structure, written entirely in Runa, as envisioned by the manifesto, with all features, error handling, and documentation in place. The successful parsing and semantic analysis of this file by our current compiler will be the first gate of acceptance, with full execution being the final goal. 