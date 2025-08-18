# Runa Standard Library Progress

## Philosophy
- No __init__ files: Explicit over implicit. See rationale below.
- Modules are explicit, with clear boundaries and no hidden magic.
- All code is written in Runa, for self-hosting and clarity.

## No __init__ Files Rationale
1. Explicit over implicit - Init files create "hidden magic" that contradicts Runa's natural language philosophy
2. AI-first design - Hidden initialization makes code harder for AI agents to understand and generate
3. Self-hosting clarity - Clean module boundaries without hidden setup code
4. Deterministic behavior - No import-time side effects or ordering dependencies

## Implementation Plan
- Scaffold stdlib directory and modules (done)
- Implement core modules: collections, math, io, etc. (in progress)
- Document all design decisions and progress here

## Progress Log
- [x] Removed old stdlib, ai, llm, train directories
- [x] Scaffolded new stdlib directory structure (no __init__ files)
- [x] Created collections/list.runa with basic list operations
- [ ] Continue implementing core modules 