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
