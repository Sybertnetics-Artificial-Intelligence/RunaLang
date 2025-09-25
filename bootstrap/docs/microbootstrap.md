# 🛠 Micro Bootstrap Plan for Runa

## 🌱 Stage 0: Minimal C Seed Compiler (v0.0)

**Goal**: Smallest C program that can parse and compile a trivial Runa program into x86-64 assembly.

* Language subset: only `Process main … Return <int> End Process`
* Backend: emits raw `.s` file with `_start` calling Linux `exit()`
* Dependencies: `as`, `ld`
* Runtime: none (just syscalls)
* Lines of code: \~300–500 in C

👉 **Outcome**: Can compile:

```runa
Process called "main" returns Integer:
    Return 0
End Process
```

into a working ELF executable.

---

## 🔹 Stage 0.0.1: Variables + Arithmetic

**Goal**: Add integer literals, variables, and arithmetic.

* Parse `Let x be 42`
* Parse binary ops: `plus`, `minus`
* Generate assembly with registers and stack slots
* Implement return expressions (not just constants)

👉 **Outcome**:

```runa
Process called "main" returns Integer:
    Let x be 40
    Let y be 2
    Return x plus y
End Process
```

→ executable returns 42.

---

## 🔹 Stage 0.0.2: Conditionals + Loops

**Goal**: Add `If`, `Otherwise`, `While`.

* Emit labels + jumps
* Boolean operators: `is equal to`, `is less than`, etc.
* Stack-based variable model

👉 **Outcome**:

```runa
Process called "main" returns Integer:
    Let x be 0
    While x is less than 10:
        Set x to x plus 1
    End While
    Return x
End Process
```

→ returns 10.

---

## 🔹 Stage 0.0.3: Functions + Calls

**Goal**: Multi-function programs.

* Parse function definitions
* Handle parameters + return values
* System V ABI: pass args in `%rdi`, `%rsi`, etc.
* Support recursive calls

👉 **Outcome**:

```runa
Process called "factorial" that takes n as Integer returns Integer:
    If n is equal to 0:
        Return 1
    Otherwise:
        Return n multiplied by factorial(n minus 1)
    End If
End Process

Process called "main" returns Integer:
    Return factorial(5)
End Process
```

→ returns 120.

---

## 🔹 Stage 0.0.4: Strings + Print

**Goal**: Basic runtime functions.

* Add string literals → put in `.rodata`
* Add `print` syscall wrapper
* Minimal runtime in C/asm for I/O

👉 **Outcome**:

```runa
Process called "main" returns Integer:
    Print "Hello, Runa!"
    Return 0
End Process
```

→ prints to console.

---

## 🔹 Stage 0.0.5: Lists (Opaque Pointers)

**Goal**: Runtime-managed lists.

* Add `list_create`, `list_append`, `list_get`
* Implement in C runtime for now
* Compiler only needs to recognize built-in calls

👉 **Outcome**:

```runa
Process called "main" returns Integer:
    Let nums be list_create()
    list_append(nums, 1)
    list_append(nums, 2)
    Return list_get(nums, 1)
End Process
```

→ returns 2.

---

## 🔹 Stage 0.0.6: Types + Structs

**Goal**: User-defined types.

* Parse `Type called …`
* Lay out structs in memory
* Support field access via offsets

👉 **Outcome**:

```runa
Type called "Point":
    x as Integer
    y as Integer
End Type

Process called "main" returns Integer:
    Let p be a value of type Point with
        x as 10,
        y as 32
    Return p.x plus p.y
End Process
```

→ returns 42.

---

## 🔹 Stage 0.0.7: Self-Hosting Prep

**Goal**: Enough features to write the compiler in Runa itself.

* File I/O (`read_file`, `write_file`)
* Better string ops
* Dictionaries or Maps
* Basic module system (`Import "..." as ...`)

👉 **Outcome**: Runa can write its **own lexer and parser**.

---

## 🔹 Stage 0.0.7.5: First Self-Hosted Compiler

**Goal**: Runa compiler written in Runa, compiled by v0.0–0.7 seed.

* Compiler pipeline: Lexer → Parser → Codegen
* Still emits `.s` → `as/ld`
* C seed archived

👉 **Outcome**: Runa is **self-hosting**.

---

## 🔹 Stage 0.0.8: Inline Assembly

**Goal**: Cut out assembler dependency.

* Support:

```runa
Inline Assembly:
    mov $60, %rax
    xor %rdi, %rdi
    syscall
End Assembly
```

* Embed raw assembly into output
* Prepare for own object writer

---

## 🔹 Stage 0.0.9: Native Object Writer + Linker

**Goal**: No `as`/`ld`.

* Generate ELF directly
* Write custom linker
* Runa compiler produces standalone executables

👉 Now you’re fully independent of external toolchains.

---

# 🚀 Recap of Build Increments

1. v0.0 – Minimal C seed, returns int
2. v0.0.1 – Variables, arithmetic
3. v0.0.2 – Conditionals + loops
4. v0.0.3 – Functions + recursion
5. v0.0.4 – Strings + print
6. v0.0.5 – Lists
7. v0.0.6 – Structs + types
8. v0.0.7 – File I/O + modules
9. v0.0.7.5 – Self-host in Runa
10. v0.0.8 – Inline assembly
11. v0.0.9 – Native object writer/linker

---

# 🌱 Compiler Bootstrap Structure

## v0.0 — Minimal Skeleton

**Purpose:** Prove toolchain independence. Just parse a number, return it as `main`.

**Features in C seed compiler:**

* Lexer: integers only.
* Parser: single literal expression.
* Codegen: emit `mov $<int>, %rax ; ret`.
* Runtime: none.

**Runa subset supported:**

```runa
Process called "main" returns Integer:
    Return 42
End Process
```

**Directory layout:**

```
/runa/bootstrap/v0.0/
    lexer.c
    parser.c
    codegen_x86.c
    main.c
    Makefile
```

---

## v0.0.1 — Variables + Arithmetic

**Features in C seed compiler:**

* Lexer: identifiers, keywords (`Let`, `Set`), `plus`, `minus`.
* Parser: assignments + expressions.
* Codegen: variable stack slots, basic math ops.

**Runa subset supported:**

```runa
Process called "main" returns Integer:
    Let x be 10
    Set x to x plus 32
    Return x
End Process
```

---

## v0.0.2 — Conditionals + Loops

**Features in C seed compiler:**

* Lexer: `If`, `Otherwise`, `While`.
* Parser: conditionals, loop bodies.
* Codegen: labels + jumps.

**Runa subset supported:**

```runa
Process called "main" returns Integer:
    Let x be 0
    While x is less than 5:
        Set x to x plus 1
    End While

    If x is equal to 5:
        Return 123
    Otherwise:
        Return 0
    End If
End Process
```

---

## v0.0.3 — Functions + Recursion

**Features in C seed compiler:**

* Lexer: `Process`, `Return`.
* Parser: function definitions + calls.
* Codegen: function prologue/epilogue, call/ret.

**Runa subset supported:**

```runa
Process called "factorial" that takes n as Integer returns Integer:
    If n is equal to 0:
        Return 1
    Otherwise:
        Return n multiplied by factorial(n minus 1)
    End If
End Process

Process called "main" returns Integer:
    Return factorial(5)
End Process
```

---

## v0.0.4 — Strings + Printing

**Features in C seed compiler:**

* Lexer: string literals.
* Runtime: syscall wrapper for `print`.
* Codegen: string storage + calls to runtime.

**Runa subset supported:**

```runa
Process called "main" returns Integer:
    Let msg be "Hello, Runa!"
    print(msg)
    Return 0
End Process
```

---

## v0.0.5 — Lists (runtime-managed)

**Features in C seed compiler:**

* Built-in runtime: `list_create`, `list_append`, `list_get_integer`.
* Parser: `List` type.
* Codegen: opaque pointers + runtime calls.

**Runa subset supported:**

```runa
Process called "main" returns Integer:
    Let xs be list_create()
    list_append(xs, 10)
    list_append(xs, 20)
    Return list_get_integer(xs, 0) plus list_get_integer(xs, 1)
End Process
```

---

## v0.0.6 — Structs & Types

**Features in C seed compiler:**

* Lexer: `Type called ... End Type`.
* Parser: type definitions, field access.
* Codegen: structs as stack allocations + offsets.

**Runa subset supported:**

```runa
Type called "Point":
    x as Integer
    y as Integer
End Type

Process called "main" returns Integer:
    Let p be a value of type Point with
        x as 3,
        y as 4
    Return p.x plus p.y
End Process
```

---

## v0.0.7 — File I/O + Module System

**Features in C seed compiler:**

* Runtime: `read_file`, `write_file`.
* Lexer/Parser: `Import "file" as Name`.
* Codegen: multiple translation units.

**Runa subset supported:**

```runa
Import "lexer" as Lexer

Process called "main" returns Integer:
    Let src be read_file("input.runa")
    Let tokens be Lexer.tokenize(src)
    write_file("tokens.txt", "OK")
    Return 0
End Process
```

---

# 🚀 Handoff to Runa: v0.0.7.5 (First Self-Host)

At this stage, the C compiler (`v0.0.7`) can compile enough Runa to write a compiler in Runa itself.

**Runa features guaranteed by C seed:**

* Integers, booleans, strings.
* Variables, assignment, arithmetic.
* Conditionals (`If/Otherwise`), loops (`While`).
* Functions + recursion.
* Lists + structs.
* File I/O.
* Module system.

**Runa compiler in Runa (`v0.0.7.5`) will implement:**

* Lexer in Runa.
* Parser in Runa.
* Type checker in Runa.
* Codegen (x86-64) in Runa.
* Uses runtime built in C (for now).

Example:

```runa
Import "lexer" as Lexer
Import "parser" as Parser
Import "codegen" as CodeGen

Process called "main" that takes args as List[String] returns Integer:
    Let src be read_file("input.runa")
    Let tokens be Lexer.tokenize(src)
    Let ast be Parser.parse(tokens)
    Let asm be CodeGen.generate(ast)
    write_file("output.s", asm)
    Return 0
End Process
```

---

✅ So the **minimum Runa subset for v0.0.7.5** is exactly what’s in `v0.0.7`.
From there, future versions (v0.2+) add *For Each*, *Match*, IR, optimizations, etc.



Migration Plan: v0.0.7 (C) → v0.0.7.5 (Runa Self-Host)

  Based on my analysis of the v0.0.7 C compiler, here's the comprehensive migration plan:

  🏗️ Architecture Overview

  The v0.0.7 C compiler consists of 4 core modules + runtime:
  - main.c: Entry point and orchestration
  - lexer.c/h: Tokenization
  - parser.c/h: AST generation
  - codegen_x86.c/h: x86-64 assembly generation
  - Runtime: I/O and list operations

  🔄 Migration Strategy

  Components That Need DIRECT COPY (C → C)

  These components should remain in C and be copied/adapted to v0.0.7.5:

  1. Runtime Libraries (runtime/ directory):
    - runtime_io.c/h → Keep as C (File I/O operations)
    - runtime_list.c/h → Keep as C (List operations)
    - Rationale: Runtime functions need direct system calls and memory management. Runa at v0.0.7.5 isn't ready to replace these low-level operations.
  2. Build System:
    - Makefile logic → build.sh
    - Assembly/linking commands → Keep as shell scripts
    - Rationale: Build orchestration still needs external tools (as, ld)

  Components That Need TRANSLITERATION (C → Runa)

  These need to be rewritten in Runa following the language specification:

  1. Main Driver (src/main.runa)

  Current C structure:
  int main(int argc, char **argv) {
      char *source_code = read_file(input_filename);
      Lexer *lexer = lexer_create(source_code);
      Parser *parser = parser_create(lexer);
      Program *program = parser_parse_program(parser);
      CodeGenerator *codegen = codegen_create(output_filename);
      codegen_generate(codegen, program);
      // cleanup...
  }

  Runa equivalent:
  Process called "main" that takes args as List[String] returns Integer:
      Let input_filename be args.get(1)
      Let output_filename be args.get(2)
      Let source_code be read_file(input_filename)
      Let lexer be Lexer.create(source_code)
      Let parser be Parser.create(lexer)
      Let program be parser.parse_program()
      Let codegen be CodeGenerator.create(output_filename)
      codegen.generate(program)
      Return 0
  End Process

  2. Lexer Module (src/lexer.runa)

  Key Transliterations:
  - TokenType enum → Runa enum with same values
  - Token struct → Runa type
  - Lexer struct → Runa type
  - lexer_create(), lexer_next_token() → Runa processes

  Critical Details:
  - Keep exact same token types from lexer.h:4-49
  - Preserve tokenization logic for all v0.0.7 features
  - String handling will use Runa's built-in string type

  3. Parser Module (src/parser.runa)

  Key Transliterations:
  - All AST node types (Expression, Statement, etc.) → Runa types
  - parser_create(), parser_parse_program() → Runa processes
  - Recursive descent parsing logic → Equivalent Runa control flow

  Critical Details:
  - AST structure must remain identical for codegen compatibility
  - All expression types from parser.h:7-16 need direct equivalents
  - Statement types from parser.h:52-61 need preservation

  4. Code Generator (src/codegen.runa)

  Key Transliterations:
  - CodeGenerator struct → Runa type with file I/O
  - Variable tracking and stack management → Runa data structures
  - x86-64 assembly emission → String building and file writing

  Critical Details:
  - Must generate identical assembly output to v0.0.7
  - Preserve calling conventions and register usage
  - Keep string literal handling and label generation logic

  📋 Detailed Module Breakdown
Migration Plan: v0.0.7 (C) → v0.0.7.5 (Runa Self-Host)

  Based on my analysis of the v0.0.7 C compiler, here's the comprehensive migration plan:

  🏗️ Architecture Overview

  The v0.0.7 C compiler consists of 4 core modules + runtime:
  - main.c: Entry point and orchestration
  - lexer.c/h: Tokenization
  - parser.c/h: AST generation
  - codegen_x86.c/h: x86-64 assembly generation
  - Runtime: I/O and list operations

  🔄 Migration Strategy

  Components That Need DIRECT COPY (C → C)

  These components should remain in C and be copied/adapted to v0.0.7.5:

  1. Runtime Libraries (runtime/ directory):
    - runtime_io.c/h → Keep as C (File I/O operations)
    - runtime_list.c/h → Keep as C (List operations)
    - Rationale: Runtime functions need direct system calls and memory management. Runa at v0.0.7.5 isn't ready to replace these low-level operations.
  2. Build System:
    - Makefile logic → build.sh
    - Assembly/linking commands → Keep as shell scripts
    - Rationale: Build orchestration still needs external tools (as, ld)

  Components That Need TRANSLITERATION (C → Runa)

  These need to be rewritten in Runa following the language specification:

  1. Main Driver (src/main.runa)

  Current C structure:
  int main(int argc, char **argv) {
      char *source_code = read_file(input_filename);
      Lexer *lexer = lexer_create(source_code);
      Parser *parser = parser_create(lexer);
      Program *program = parser_parse_program(parser);
      CodeGenerator *codegen = codegen_create(output_filename);
      codegen_generate(codegen, program);
      // cleanup...
  }

  Runa equivalent:
  Process called "main" that takes args as List[String] returns Integer:
      Let input_filename be args.get(1)
      Let output_filename be args.get(2)
      Let source_code be read_file(input_filename)
      Let lexer be Lexer.create(source_code)
      Let parser be Parser.create(lexer)
      Let program be parser.parse_program()
      Let codegen be CodeGenerator.create(output_filename)
      codegen.generate(program)
      Return 0
  End Process

  2. Lexer Module (src/lexer.runa)

  Key Transliterations:
  - TokenType enum → Runa enum with same values
  - Token struct → Runa type
  - Lexer struct → Runa type
  - lexer_create(), lexer_next_token() → Runa processes

  Critical Details:
  - Keep exact same token types from lexer.h:4-49
  - Preserve tokenization logic for all v0.0.7 features
  - String handling will use Runa's built-in string type

  3. Parser Module (src/parser.runa)

  Key Transliterations:
  - All AST node types (Expression, Statement, etc.) → Runa types
  - parser_create(), parser_parse_program() → Runa processes
  - Recursive descent parsing logic → Equivalent Runa control flow

  Critical Details:
  - AST structure must remain identical for codegen compatibility
  - All expression types from parser.h:7-16 need direct equivalents
  - Statement types from parser.h:52-61 need preservation

  4. Code Generator (src/codegen.runa)

  Key Transliterations:
  - CodeGenerator struct → Runa type with file I/O
  - Variable tracking and stack management → Runa data structures
  - x86-64 assembly emission → String building and file writing

  Critical Details:
  - Must generate identical assembly output to v0.0.7
  - Preserve calling conventions and register usage
  - Keep string literal handling and label generation logic

  📋 Detailed Module Breakdown

  Files to Create in v0.0.7.5:

  v0.0.7.5/
  ├── src/
  │   ├── main.runa          # Main compiler driver [TRANSLITERATE]
  │   ├── lexer.runa         # Token scanner [TRANSLITERATE]
  │   ├── parser.runa        # AST builder [TRANSLITERATE]
  │   ├── codegen.runa       # x86-64 generator [TRANSLITERATE]
  │   └── types.runa         # Shared type definitions [NEW]
  ├── runtime/
  │   ├── runtime_io.c       # File I/O [DIRECT COPY]
  │   ├── runtime_io.h       # I/O headers [DIRECT COPY]
  │   ├── runtime_list.c     # List operations [DIRECT COPY]
  │   └── runtime_list.h     # List headers [DIRECT COPY]
  └── build.sh               # Build script [ADAPT FROM MAKEFILE]

  🎯 Implementation Priority

  1. Phase 1: Runtime setup (copy C runtime files)
  2. Phase 2: Core types (types.runa - AST definitions)
  3. Phase 3: Lexer (lexer.runa)
  4. Phase 4: Parser (parser.runa)
  5. Phase 5: Code generator (codegen.runa)
  6. Phase 6: Main driver (main.runa)
  7. Phase 7: Build system integration

  🔧 Key Technical Considerations

  Data Structure Translations:

  - C structs → Runa Type definitions
  - C arrays → Runa Lists
  - C pointers → Runa object references
  - C file handles → Use runtime functions via FFI

  Memory Management:

  - C manual malloc/free → Runa automatic memory management
  - Dynamic arrays → Runa Lists with automatic resizing
  - String handling → Runa built-in strings

  Function Calling:

  - C function pointers → Runa process references
  - C parameter passing → Runa parameter syntax
  - C return values → Runa Return statements

  🚨 Critical Success Factors

  1. AST Compatibility: The Runa parser must produce identical AST structure to ensure codegen works
  2. Token Compatibility: Lexer must recognize exact same tokens with same precedence
  3. Assembly Output: Generated assembly must be functionally equivalent to v0.0.7
  4. Runtime Integration: Runa code must correctly call C runtime functions
  5. Error Handling: Preserve error reporting and debugging information

  🎯 Success Criteria

  The v0.0.7.5 self-hosted compiler succeeds when:
  - It can compile the same Runa programs as v0.0.7
  - Generated executables behave identically
  - All v0.0.7 test cases pass
  - The v0.0.7.5 compiler can compile itself (true self-hosting)

  This plan maintains the proven architecture of v0.0.7 while transitioning the compiler logic to Runa, achieving true self-hosting while preserving all functionality.
  Files to Create in v0.0.7.5:

  v0.0.7.5/
  ├── src/
  │   ├── main.runa          # Main compiler driver [TRANSLITERATE]
  │   ├── lexer.runa         # Token scanner [TRANSLITERATE]
  │   ├── parser.runa        # AST builder [TRANSLITERATE]
  │   ├── codegen.runa       # x86-64 generator [TRANSLITERATE]
  │   └── types.runa         # Shared type definitions [NEW]
  ├── runtime/
  │   ├── runtime_io.c       # File I/O [DIRECT COPY]
  │   ├── runtime_io.h       # I/O headers [DIRECT COPY]
  │   ├── runtime_list.c     # List operations [DIRECT COPY]
  │   └── runtime_list.h     # List headers [DIRECT COPY]
  └── build.sh               # Build script [ADAPT FROM MAKEFILE]

  🎯 Implementation Priority

  1. Phase 1: Runtime setup (copy C runtime files)
  2. Phase 2: Core types (types.runa - AST definitions)
  3. Phase 3: Lexer (lexer.runa)
  4. Phase 4: Parser (parser.runa)
  5. Phase 5: Code generator (codegen.runa)
  6. Phase 6: Main driver (main.runa)
  7. Phase 7: Build system integration

  🔧 Key Technical Considerations

  Data Structure Translations:

  - C structs → Runa Type definitions
  - C arrays → Runa Lists
  - C pointers → Runa object references
  - C file handles → Use runtime functions via FFI

  Memory Management:

  - C manual malloc/free → Runa automatic memory management
  - Dynamic arrays → Runa Lists with automatic resizing
  - String handling → Runa built-in strings

  Function Calling:

  - C function pointers → Runa process references
  - C parameter passing → Runa parameter syntax
  - C return values → Runa Return statements

  🚨 Critical Success Factors

  1. AST Compatibility: The Runa parser must produce identical AST structure to ensure codegen works
  2. Token Compatibility: Lexer must recognize exact same tokens with same precedence
  3. Assembly Output: Generated assembly must be functionally equivalent to v0.0.7
  4. Runtime Integration: Runa code must correctly call C runtime functions
  5. Error Handling: Preserve error reporting and debugging information

  🎯 Success Criteria

  The v0.0.7.5 self-hosted compiler succeeds when:
  - It can compile the same Runa programs as v0.0.7
  - Generated executables behave identically
  - All v0.0.7 test cases pass
  - The v0.0.7.5 compiler can compile itself (true self-hosting)

  This plan maintains the proven architecture of v0.0.7 while transitioning the compiler logic to Runa, achieving true self-hosting while preserving all functionality.