# LAST EFFORT COMPILER BOOTSTRAPPING: COMPLETE TECHNICAL SPECIFICATION

## EXECUTIVE SUMMARY

This document defines the exact, letter-by-letter implementation plan for bootstrapping the Runa programming language from its current state to complete independence from external toolchains. Every compiler version, every feature addition, every architectural decision is specified here in complete detail.

The bootstrap chain consists of five distinct compiler versions, each building upon the previous:
- **v0.1**: Rust-based bootstrap compiler with LLVM backend
- **v0.2**: First self-hosted Runa compiler with direct assembly generation
- **v0.3**: Enhanced Runa compiler with initial Syber-Core architecture
- **v0.4**: Full Syber-Core implementation with multi-platform support
- **v0.5**: Production-ready compiler with complete optimization pipeline

---

## PHASE 0: CURRENT STATE ASSESSMENT

### ⚠️ FRESH START - NO ASSUMPTIONS ⚠️
**Date**: 2025-09-14
**Starting Point**: VERIFY EVERYTHING FROM SCRATCH

#### v0.1 Bootstrap Compiler (Rust + LLVM)
**Location**: `/runa/bootstrap/v0.1_runa-bootstrap/`
**Language**: Rust
**Backend**: LLVM 17
**Status**: TO BE VERIFIED

**Verification Checklist**:
```runa
Note: MUST VERIFY each feature before marking complete:
- [ ] Integer literals and variables
- [ ] Basic arithmetic: plus, minus, multiplied by, divided by
- [ ] Comparisons: is greater than, is less than, is equal to
- [ ] If/Otherwise conditionals
- [ ] While loops
- [ ] Function definitions and calls
- [ ] Return statements
- [ ] Let variable declarations
- [ ] String literals (no operations)
```

**Missing Critical Features for Bootstrap**:
```runa
Note: Required for v0.2 compilation
- File I/O: ReadFile, WriteFile
- String operations: string_concat, string_length, string_char_at, string_substring
- Array/List support: Let arr be a list containing 1, 2, 3
- Dictionary support: Let dict be a dictionary containing "key" as "value"
- Type definitions: Type called "MyType"
- For Each loops: For Each item in collection
- Match expressions: Match value When pattern
- Character operations: is_digit, is_letter, to_uppercase, to_lowercase
- Escape sequences in strings: \"
- Module imports: Import "path/to/module" as ModuleName
```

#### Existing IR Infrastructure
**Location**: `/runa/src/compiler/middle/ir/`
**Status**: TO BE VERIFIED - Assume nothing works

```
hir/ - High-level Intermediate Representation
  hir_builder.runa - Skeleton
  hir_nodes.runa - Type definitions only
  hir_visitor.runa - Skeleton

mir/ - Mid-level Intermediate Representation
  mir_builder.runa - Skeleton
  mir_nodes.runa - Type definitions only
  mir_optimizer.runa - Skeleton
  mir_verifier.runa - Skeleton

lir/ - Low-level Intermediate Representation
  lir_builder.runa - Skeleton
  lir_nodes.runa - Type definitions only
  lir_optimizer.runa - Skeleton
```

---

## PHASE 1: v0.1 ENHANCEMENT (RUST + LLVM)

### Objective
Enhance v0.1 with the minimum features required to compile v0.2, which will be a basic Runa compiler written in Runa itself.

### Implementation Requirements

#### 1.1 File I/O Support
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/codegen.rs`

```rust
// Add to builtin functions
"ReadFile" => {
    // Implementation: Call LLVM intrinsics for file operations
    // 1. Open file using libc fopen
    // 2. Read entire contents into string
    // 3. Return as Runa string value
}

"WriteFile" => {
    // Implementation:
    // 1. Take string content and filepath
    // 2. Open/create file using libc fopen
    // 3. Write content
    // 4. Close file
}
```

**Runa Syntax Support**:
```runa
Let content be ReadFile("input.txt")
WriteFile "output data" to "output.txt"
```

#### 1.2 String Operations
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/codegen.rs`, `parser.rs`

```rust
// String concatenation
"string_concat" => {
    // Allocate new buffer = len(str1) + len(str2)
    // Copy str1, then str2
    // Return new string
}

// String length
"string_length" => {
    // Return length field from string structure
}

// Character access
"string_char_at" => {
    // Bounds check
    // Return character at index
}

// Substring
"string_substring" => {
    // Validate start/end indices
    // Allocate new buffer
    // Copy substring
}
```

**Runa Syntax**:
```runa
Let combined be string_concat(str1, str2)
Let len be string_length(text)
Let ch be string_char_at(text, 5)
Let sub be string_substring(text, 0, 10)
```

#### 1.3 Collection Types
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/types.rs`, `parser.rs`, `codegen.rs`

```rust
// Add to type system
enum Type {
    // Existing...
    List(Box<Type>),
    Array(Box<Type>, usize), // Fixed size
    Dictionary(Box<Type>, Box<Type>),
}
```

**List Operations**:
```runa
Let numbers be a list containing 1, 2, 3, 4, 5
Let first be numbers at index 0
Add 6 to end of numbers
Let size be length of numbers
```

**Dictionary Operations**:
```runa
Let config be a dictionary containing:
    "host" as "localhost",
    "port" as 8080,
    "debug" as true
End Dictionary

Let host be config at key "host"
Set config at key "timeout" to 30
```

#### 1.4 Type Definitions
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/parser.rs`, `types.rs`

```rust
// Support structured types
struct TypeDefinition {
    name: String,
    fields: Vec<(String, Type)>,
}

// Support enum types
struct EnumDefinition {
    name: String,
    variants: Vec<EnumVariant>,
}
```

**Runa Syntax**:
```runa
Type called "Token":
    token_type as String
    value as String
    line as Integer
    column as Integer
End Type

Type TokenType is:
    | Keyword
    | Identifier
    | Number
    | String
    | Symbol
End Type
```

#### 1.5 Control Flow Additions
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/parser.rs`, `codegen.rs`

**For Each Loops**:
```runa
For Each token in tokens:
    Process token
End For
```

**Match Expressions**:
```runa
Match token_type:
    When Keyword:
        Handle keyword
    When Identifier:
        Handle identifier
    Otherwise:
        Handle default
End Match
```

#### 1.6 Module System
**Files to Modify**: Create new `/runa/bootstrap/v0.1_runa-bootstrap/src/modules.rs`

```rust
struct Module {
    name: String,
    exports: HashMap<String, Symbol>,
    imports: Vec<Import>,
}
```

**Runa Syntax**:
```runa
Import "compiler/lexer" as Lexer
Import "compiler/parser" as Parser

Let tokens be Lexer.tokenize(source)
Let ast be Parser.parse(tokens)
```

#### 1.7 Character Operations
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/codegen.rs`

```rust
// Character classification
"is_digit" => { /* Check if char is 0-9 */ }
"is_letter" => { /* Check if char is a-z, A-Z */ }
"is_whitespace" => { /* Check if space, tab, newline */ }

// Character conversion
"to_uppercase" => { /* Convert a-z to A-Z */ }
"to_lowercase" => { /* Convert A-Z to a-z */ }
"char_to_string" => { /* Convert single char to string */ }
```

#### 1.8 Escape Sequences
**Files to Modify**: `/runa/bootstrap/v0.1_runa-bootstrap/src/lexer.rs`

```rust
// Handle escape sequences in string literals
fn parse_string_literal(input: &str) -> String {
    // Support: \n, \t, \r, \\, \"
}
```

### Cross-Compilation Support in v0.1

**Target Platforms via LLVM**:
- x86_64-linux-gnu (primary)
- x86_64-windows-msvc
- x86_64-apple-darwin
- aarch64-linux-gnu
- aarch64-apple-darwin
- wasm32-unknown-unknown

**Implementation**:
```rust
// Add target triple configuration
struct CompilerOptions {
    target_triple: String, // e.g., "x86_64-unknown-linux-gnu"
    optimization_level: OptLevel,
    output_type: OutputType, // Object, Assembly, LLVM-IR
}
```

### Testing Requirements

**Test Programs Required**:
```runa
Note: v0.1 must successfully compile these before proceeding
Note: ALL TESTS MUST BE RUN FROM SCRATCH

Note: test_file_io.runa
Process called "main" returns Integer:
    Let content be ReadFile("input.txt")
    WriteFile content to "output.txt"
    Return 0
End Process

Note: test_strings.runa
Process called "main" returns Integer:
    Let hello be "Hello"
    Let world be "World"
    Let message be string_concat(hello, world)
    Let len be string_length(message)
    Return len
End Process

Note: test_collections.runa
Process called "main" returns Integer:
    Let nums be a list containing 1, 2, 3
    For Each n in nums:
        Print n
    End For
    Return 0
End Process

Note: test_types.runa
Type called "Point":
    x as Integer
    y as Integer
End Type

Process called "main" returns Integer:
    Let p be a value of type Point with
        x as 10,
        y as 20
    Return p.x plus p.y
End Process
```

---

## PHASE 2: v0.2 SELF-HOSTED COMPILER (RUNA + ASSEMBLY)

### Objective
Write the first self-hosted Runa compiler in Runa itself, using v0.1 to compile it. This compiler generates x86-64 assembly directly without LLVM.

### Architecture

```
Source Code (.runa)
    ↓
Lexer (tokenize)
    ↓
Parser (build AST)
    ↓
Type Checker
    ↓
Assembly Generator (x86-64 only)
    ↓
Assembly File (.s)
    ↓
Assembler (as) → Object File (.o)
    ↓
Linker (ld) → Executable
```

### Implementation Files

#### 2.1 Main Compiler Driver
**File**: `/runa/bootstrap/v0.2_micro-runa/main.runa`

```runa
Import "lexer" as Lexer
Import "parser" as Parser
Import "type_checker" as TypeChecker
Import "codegen_x86" as CodeGen
Import "assembler" as Assembler

Process called "main" that takes args as List[String] returns Integer:
    If length of args is less than 2:
        Print "Usage: runac <input.runa> [-o output]"
        Return 1
    End If

    Let input_file be args at index 1
    Let output_file be get_output_filename(args)

    Let source be ReadFile(input_file)

    Note: Compilation pipeline
    Let tokens be Lexer.tokenize(source)
    Let ast be Parser.parse(tokens)
    Let typed_ast be TypeChecker.check(ast)
    Let assembly be CodeGen.generate(typed_ast)

    WriteFile assembly to output_file

    Note: Invoke system assembler
    Let object_file be string_concat(output_file, ".o")
    System("as " plus output_file plus " -o " plus object_file)

    Return 0
End Process
```

#### 2.2 Lexer Implementation
**File**: `/runa/bootstrap/v0.2_micro_runa/lexer.runa`

```runa
Type called "Token":
    token_type as TokenType
    value as String
    line as Integer
    column as Integer
End Type

Type TokenType is:
    | Keyword      Note: Process, Let, If, Return, etc.
    | Identifier   Note: Variable and function names
    | Integer      Note: Numeric literals
    | String       Note: String literals
    | Symbol       Note: (, ), :, etc.
    | Operator     Note: plus, minus, etc.
End Type

Process called "tokenize" that takes source as String returns List[Token]:
    Let tokens be a list containing nothing
    Let position be 0
    Let line be 1
    Let column be 1

    While position is less than string_length(source):
        Let ch be string_char_at(source, position)

        If is_whitespace(ch):
            If ch is equal to 10: Note: Newline
                Set line to line plus 1
                Set column to 1
            Otherwise:
                Set column to column plus 1
            End If
            Set position to position plus 1

        Otherwise If is_letter(ch):
            Let ident_result be read_identifier(source, position)
            Let identifier be get_first(ident_result)
            Let new_pos be get_second(ident_result)

            Let token_type be Keyword
            If is_keyword(identifier) is false:
                Set token_type to Identifier
            End If

            Let token be a value of type Token with
                token_type as token_type,
                value as identifier,
                line as line,
                column as column

            Add token to end of tokens
            Set column to column plus (new_pos minus position)
            Set position to new_pos

        Otherwise If is_digit(ch):
            Let num_result be read_number(source, position)
            Let number be get_first(num_result)
            Let new_pos be get_second(num_result)

            Let token be a value of type Token with
                token_type as Integer,
                value as number,
                line as line,
                column as column

            Add token to end of tokens
            Set column to column plus (new_pos minus position)
            Set position to new_pos

        Otherwise If ch is equal to 34: Note: Quote character
            Let str_result be read_string(source, position)
            Let string_val be get_first(str_result)
            Let new_pos be get_second(str_result)

            Let token be a value of type Token with
                token_type as String,
                value as string_val,
                line as line,
                column as column

            Add token to end of tokens
            Set column to column plus (new_pos minus position)
            Set position to new_pos

        Otherwise:
            Let symbol be char_to_string(ch)
            Let token be a value of type Token with
                token_type as Symbol,
                value as symbol,
                line as line,
                column as column

            Add token to end of tokens
            Set column to column plus 1
            Set position to position plus 1
        End If
    End While

    Return tokens
End Process
```

#### 2.3 Parser Implementation
**File**: `/runa/bootstrap/v0.2_micro-runa/parser.runa`

```runa
Type called "ASTNode":
    node_type as NodeType
    children as List[ASTNode]
    value as Optional[String]
    data_type as Optional[Type]
End Type

Type NodeType is:
    | Program
    | Function
    | Parameter
    | Statement
    | Expression
    | BinaryOp
    | UnaryOp
    | Literal
    | Identifier
    | FunctionCall
    | If
    | While
    | ForEach
    | Match
    | Return
    | Let
    | Set
    | TypeDef
End Type

Type called "Parser":
    tokens as List[Token]
    current as Integer
End Type

Process called "parse" that takes tokens as List[Token] returns ASTNode:
    Let parser be a value of type Parser with
        tokens as tokens,
        current as 0

    Return parse_program(parser)
End Process

Process called "parse_program" that takes parser as Parser returns ASTNode:
    Let program be a value of type ASTNode with
        node_type as Program,
        children as a list containing nothing,
        value as nothing,
        data_type as nothing

    While parser.current is less than length of parser.tokens:
        Let node be parse_top_level(parser)
        Add node to end of program.children
    End While

    Return program
End Process

Process called "parse_top_level" that takes parser as Parser returns ASTNode:
    Let token be current_token(parser)

    Match token.value:
        When "Process":
            Return parse_function(parser)
        When "Type":
            Return parse_type_definition(parser)
        When "Import":
            Return parse_import(parser)
        Otherwise:
            Error("Unexpected top-level token: " plus token.value)
    End Match
End Process

Process called "parse_function" that takes parser as Parser returns ASTNode:
    consume(parser, "Process")
    consume(parser, "called")

    Let name be consume_identifier(parser)

    Let parameters be a list containing nothing
    If current_token(parser).value is equal to "that":
        consume(parser, "that")
        consume(parser, "takes")
        Set parameters to parse_parameters(parser)
    End If

    Let return_type be nothing
    If current_token(parser).value is equal to "returns":
        consume(parser, "returns")
        Set return_type to parse_type(parser)
    End If

    consume(parser, ":")

    Let body be parse_block(parser, "End Process")

    Let function be a value of type ASTNode with
        node_type as Function,
        children as body,
        value as name,
        data_type as return_type

    Return function
End Process
```

#### 2.4 Type Checker
**File**: `/runa/bootstrap/v0.2_micro-runa/type_checker.runa`

```runa
Type called "TypeEnvironment":
    variables as Dictionary[String, Type]
    functions as Dictionary[String, FunctionType]
    types as Dictionary[String, TypeDefinition]
    parent as Optional[TypeEnvironment]
End Type

Process called "check" that takes ast as ASTNode returns ASTNode:
    Let env be create_global_environment()
    Return check_node(ast, env)
End Process

Process called "check_node" that takes node as ASTNode, env as TypeEnvironment returns ASTNode:
    Match node.node_type:
        When Program:
            For Each child in node.children:
                check_node(child, env)
            End For
            Return node

        When Function:
            Let func_env be create_function_environment(node, env)
            For Each stmt in node.children:
                check_node(stmt, func_env)
            End For
            Return node

        When Let:
            Let var_name be node.value
            Let init_expr be node.children at index 0
            Let expr_type be infer_type(init_expr, env)
            Set env.variables at key var_name to expr_type
            Set node.data_type to expr_type
            Return node

        When BinaryOp:
            Let left be check_node(node.children at index 0, env)
            Let right be check_node(node.children at index 1, env)

            If not types_compatible(left.data_type, right.data_type):
                Error("Type mismatch in binary operation")
            End If

            Set node.data_type to result_type(node.value, left.data_type)
            Return node

        Otherwise:
            Return node
    End Match
End Process
```

#### 2.5 x86-64 Assembly Generator
**File**: `/runa/bootstrap/v0.2_micro-runa/codegen_x86.runa`

```runa
Type called "CodeGenerator":
    output as String
    label_counter as Integer
    stack_offset as Integer
    variables as Dictionary[String, Integer] Note: Variable name to stack offset
End Type

Process called "generate" that takes ast as ASTNode returns String:
    Let gen be a value of type CodeGenerator with
        output as "",
        label_counter as 0,
        stack_offset as 0,
        variables as a dictionary containing nothing

    emit(gen, ".text")
    emit(gen, ".globl main")
    emit(gen, "")

    generate_node(gen, ast)

    Return gen.output
End Process

Process called "generate_node" that takes gen as CodeGenerator, node as ASTNode returns Nothing:
    Match node.node_type:
        When Program:
            For Each child in node.children:
                generate_node(gen, child)
            End For

        When Function:
            Let name be node.value
            emit(gen, name plus ":")

            Note: Function prologue
            emit(gen, "    push %rbp")
            emit(gen, "    mov %rsp, %rbp")

            Note: Allocate stack space for locals
            Let space be calculate_stack_space(node)
            If space is greater than 0:
                emit(gen, "    sub $" plus int_to_string(space) plus ", %rsp")
            End If

            Note: Generate function body
            For Each stmt in node.children:
                generate_statement(gen, stmt)
            End For

            Note: Function epilogue
            emit(gen, "    mov %rbp, %rsp")
            emit(gen, "    pop %rbp")
            emit(gen, "    ret")
            emit(gen, "")

        Otherwise:
            Error("Unexpected node type in code generation")
    End Match
End Process

Process called "generate_statement" that takes gen as CodeGenerator, stmt as ASTNode returns Nothing:
    Match stmt.node_type:
        When Let:
            Let var_name be stmt.value
            Let init_expr be stmt.children at index 0

            generate_expression(gen, init_expr)

            Note: Store result in variable
            Set gen.stack_offset to gen.stack_offset plus 8
            Set gen.variables at key var_name to gen.stack_offset
            emit(gen, "    mov %rax, -" plus int_to_string(gen.stack_offset) plus "(%rbp)")

        When Return:
            Let expr be stmt.children at index 0
            generate_expression(gen, expr)
            emit(gen, "    jmp .L_return_" plus current_function_name(gen))

        When If:
            Let condition be stmt.children at index 0
            Let then_block be stmt.children at index 1
            Let else_block be nothing
            If length of stmt.children is greater than 2:
                Set else_block to stmt.children at index 2
            End If

            Let else_label be gen_label(gen, "else")
            Let end_label be gen_label(gen, "endif")

            generate_expression(gen, condition)
            emit(gen, "    test %rax, %rax")
            emit(gen, "    jz " plus else_label)

            For Each s in then_block.children:
                generate_statement(gen, s)
            End For
            emit(gen, "    jmp " plus end_label)

            emit(gen, else_label plus ":")
            If else_block is not nothing:
                For Each s in else_block.children:
                    generate_statement(gen, s)
                End For
            End If

            emit(gen, end_label plus ":")

        Otherwise:
            generate_expression(gen, stmt)
    End Match
End Process

Process called "generate_expression" that takes gen as CodeGenerator, expr as ASTNode returns Nothing:
    Match expr.node_type:
        When Literal:
            If expr.data_type is Integer:
                emit(gen, "    mov $" plus expr.value plus ", %rax")
            Otherwise If expr.data_type is String:
                Let label be gen_string_literal(gen, expr.value)
                emit(gen, "    lea " plus label plus "(%rip), %rax")
            End If

        When Identifier:
            Let offset be gen.variables at key expr.value
            emit(gen, "    mov -" plus int_to_string(offset) plus "(%rbp), %rax")

        When BinaryOp:
            Let left be expr.children at index 0
            Let right be expr.children at index 1

            generate_expression(gen, left)
            emit(gen, "    push %rax")

            generate_expression(gen, right)
            emit(gen, "    mov %rax, %rbx")
            emit(gen, "    pop %rax")

            Match expr.value:
                When "plus":
                    emit(gen, "    add %rbx, %rax")
                When "minus":
                    emit(gen, "    sub %rbx, %rax")
                When "multiplied by":
                    emit(gen, "    imul %rbx, %rax")
                When "divided by":
                    emit(gen, "    xor %rdx, %rdx")
                    emit(gen, "    idiv %rbx")
                When "is greater than":
                    emit(gen, "    cmp %rbx, %rax")
                    emit(gen, "    setg %al")
                    emit(gen, "    movzx %al, %rax")
                When "is less than":
                    emit(gen, "    cmp %rbx, %rax")
                    emit(gen, "    setl %al")
                    emit(gen, "    movzx %al, %rax")
                When "is equal to":
                    emit(gen, "    cmp %rbx, %rax")
                    emit(gen, "    sete %al")
                    emit(gen, "    movzx %al, %rax")
            End Match

        When FunctionCall:
            Let func_name be expr.value
            Let args be expr.children

            Note: Pass arguments in registers (System V ABI)
            Note: rdi, rsi, rdx, rcx, r8, r9
            For Each i from 0 to length of args minus 1:
                generate_expression(gen, args at index i)
                Match i:
                    When 0: emit(gen, "    mov %rax, %rdi")
                    When 1: emit(gen, "    mov %rax, %rsi")
                    When 2: emit(gen, "    mov %rax, %rdx")
                    When 3: emit(gen, "    mov %rax, %rcx")
                    When 4: emit(gen, "    mov %rax, %r8")
                    When 5: emit(gen, "    mov %rax, %r9")
                    Otherwise:
                        Note: Stack arguments for 7+ parameters
                        emit(gen, "    push %rax")
                End Match
            End For

            emit(gen, "    call " plus func_name)

        Otherwise:
            Error("Unsupported expression type")
    End Match
End Process
```

### Platform Support in v0.2

**Primary Target**: x86_64-linux-gnu ONLY
- Direct assembly generation for x86-64
- ELF object file format
- System V ABI calling convention

**Why Only x86-64**:
- Simplest to implement correctly
- Most common development platform
- Well-documented instruction set
- Can test on standard Linux systems

**Cross-Compilation**: NOT SUPPORTED in v0.2
- This is intentional to keep v0.2 simple
- Cross-compilation added in v0.3

### Capabilities and Limitations

**What v0.2 CAN Compile**:
```runa
- All of v0.1's features
- Simple recursive functions
- Basic data structures
- File I/O programs
- String manipulation
- Mathematical computations
- Itself (self-hosting)
```

**What v0.2 CANNOT Do**:
```runa
- Optimization (straight code generation)
- Cross-compilation (x86-64 only)
- Advanced features (closures, coroutines, etc.)
- Debug information
- Proper error recovery
```

### Bootstrap Process

```bash
# Step 1: Use v0.1 to compile v0.2
cd /runa/bootstrap/v0.1_runa-bootstrap
./target/release/runac ../v0.2_micro-runa/main.runa -o ../v0.2_micro-runa/runac_v0.2.o

# Step 2: Link v0.2
gcc -no-pie ../v0.2_micro-runa/runac_v0.2.o -o ../v0.2_micro-runa/runac_v0.2

# Step 3: v0.2 compiles itself
cd ../v0.2_micro-runa
./runac_v0.2 main.runa -o runac_v0.2_self.s
as runac_v0.2_self.s -o runac_v0.2_self.o
gcc -no-pie runac_v0.2_self.o -o runac_v0.2_self

# Step 4: Verify self-hosting
diff runac_v0.2 runac_v0.2_self
# Should produce identical executables
```

---

## PHASE 2.5: v0.2.5 INLINE ASSEMBLY SUPPORT

### Objective
Add inline assembly support to the self-hosted v0.2 compiler to enable low-level operations needed for v0.3's Syber-Core implementation.

### Rationale
- **v0.3 Syber-Core needs low-level operations** for memory management, atomic operations, and system calls
- **Must be added after self-hosting** since it extends the language syntax
- **Required for bootstrap independence** from C runtime eventually

### Implementation

#### 2.5.1 Assembly Block Syntax
**File**: `/runa/bootstrap/v0.2_micro-runa/parser.runa` (enhancement)

Add new AST node type:
```runa
Type ASTNodeType is:
    | ... existing types ...
    | AssemblyBlock
End Type
```

Parse inline assembly:
```runa
Process called "parse_assembly_block" that takes parser as Parser returns ASTNode:
    consume(parser, "Inline Assembly")
    consume(parser, ":")

    Let instructions be a list containing nothing
    While not check_token(parser, "End"):
        Let line be consume_until_newline(parser)
        Add line to end of instructions
    End While

    consume(parser, "End")
    consume(parser, "Assembly")

    Return create_assembly_node(instructions)
End Process
```

#### 2.5.2 Code Generation
**File**: `/runa/bootstrap/v0.2_micro-runa/codegen_x86.runa` (enhancement)

```runa
Process called "generate_assembly_block" that takes gen as CodeGenerator, node as ASTNode returns Nothing:
    Note: Pass through assembly instructions directly
    For Each instruction in node.instructions:
        emit(gen, "    " plus instruction)
    End For
End Process
```

#### 2.5.3 Usage Examples

**System Call Example**:
```runa
Process called "syscall_write" that takes fd as Integer, buffer as String, length as Integer returns Integer:
    Inline Assembly:
        mov %rdi, %rax    Note: fd
        mov %rsi, %rbx    Note: buffer
        mov %rdx, %rcx    Note: length
        mov $1, %rax      Note: sys_write
        syscall
    End Assembly
    Note: Return value in %rax
End Process
```

**Atomic Operation Example**:
```runa
Process called "atomic_increment" that takes ptr as Integer returns Integer:
    Inline Assembly:
        lock incl (%rdi)
        mov (%rdi), %rax
    End Assembly
End Process
```

### Constraints and Limitations

**What v0.2.5 Assembly Blocks CAN do**:
- Direct CPU instructions
- System calls
- Atomic operations
- Memory barriers
- CPU feature detection (CPUID)

**What v0.2.5 Assembly Blocks CANNOT do**:
- Register constraints (fixed ABI)
- Inline variable substitution
- Cross-platform assembly (x86-64 only)
- Optimization hints

### Testing

Create test file `/runa/bootstrap/v0.2_micro-runa/test_assembly.runa`:
```runa
Process called "test_inline_asm" returns Integer:
    Let value be 41
    Inline Assembly:
        mov $41, %rax
        inc %rax
    End Assembly
    Note: Should return 42
End Process
```

---

## PHASE 3: v0.3 INITIAL SYBER-CORE (RUNA + MIR/LIR)

### Objective
Enhance v0.2 with the initial Syber-Core architecture, adding MIR/LIR layers and basic optimizations while maintaining self-hosting capability.

### Architecture Evolution

```
Source Code (.runa)
    ↓
Lexer (unchanged from v0.2)
    ↓
Parser (enhanced for new features)
    ↓
Type Checker (enhanced)
    ↓
HIR Builder (NEW)
    ↓
MIR Builder (NEW)
    ↓
MIR Optimizer (NEW - basic passes)
    ↓
LIR Builder (NEW)
    ↓
LIR Optimizer (NEW - register allocation)
    ↓
Assembly Generator (enhanced from v0.2)
    ↓
Object File Writer (NEW - native ELF generation)
```

### New Components

#### 3.1 HIR (High-level IR) Implementation
**File**: `/runa/bootstrap/v0.2_syber-core/hir/hir_builder.runa`

```runa
Import "../mir/mir_nodes" as MIR

Type called "HIRNode":
    node_id as String
    node_kind as HIRNodeKind
    data_type as Type
    source_location as SourceLocation
    metadata as Dictionary[String, String]
End Type

Type HIRNodeKind is:
    | Module as HIRModule
    | Function as HIRFunction
    | Block as HIRBlock
    | Statement as HIRStatement
    | Expression as HIRExpression
    | Pattern as HIRPattern
    | Type as HIRType
End Type

Type called "HIRModule":
    name as String
    imports as List[Import]
    exports as List[Export]
    functions as List[HIRFunction]
    types as List[TypeDefinition]
    constants as List[Constant]
End Type

Type called "HIRFunction":
    name as String
    parameters as List[Parameter]
    return_type as Type
    body as HIRBlock
    attributes as List[Attribute]
    is_generic as Boolean
    generic_params as List[GenericParameter]
End Type

Process called "build_hir" that takes ast as ASTNode returns HIRModule:
    Let builder be create_hir_builder()
    Return transform_ast_to_hir(builder, ast)
End Process

Process called "transform_ast_to_hir" that takes builder as HIRBuilder, ast as ASTNode returns HIRModule:
    Let module be a value of type HIRModule with
        name as get_module_name(ast),
        imports as a list containing nothing,
        exports as a list containing nothing,
        functions as a list containing nothing,
        types as a list containing nothing,
        constants as a list containing nothing

    For Each node in ast.children:
        Match node.node_type:
            When Function:
                Let hir_func be transform_function(builder, node)
                Add hir_func to end of module.functions

            When TypeDef:
                Let hir_type be transform_type_def(builder, node)
                Add hir_type to end of module.types

            When Import:
                Let import be transform_import(builder, node)
                Add import to end of module.imports

            When Constant:
                Let const be transform_constant(builder, node)
                Add const to end of module.constants
        End Match
    End For

    Return module
End Process
```

#### 3.2 MIR (Mid-level IR) Implementation
**File**: `/runa/bootstrap/v0.2_syber-core/mir/mir_builder.runa`

```runa
Type called "MIRProgram":
    modules as List[MIRModule]
    entry_point as String
    target_info as TargetInfo
End Type

Type called "MIRModule":
    name as String
    functions as List[MIRFunction]
    global_data as List[GlobalData]
    string_pool as StringPool
End Type

Type called "MIRFunction":
    name as String
    parameters as List[MIRValue]
    return_type as MIRType
    basic_blocks as List[BasicBlock]
    locals as List[LocalVariable]
    is_ssa as Boolean Note: Whether in SSA form
End Type

Type called "BasicBlock":
    id as String
    instructions as List[MIRInstruction]
    predecessors as List[String]
    successors as List[String]
    phi_nodes as List[PhiNode]
End Type

Type called "MIRInstruction":
    opcode as MIROpcode
    operands as List[MIROperand]
    result as Optional[MIRValue]
    metadata as InstructionMetadata
End Type

Type MIROpcode is:
    | Add | Sub | Mul | Div | Mod
    | And | Or | Xor | Not
    | Shl | Shr | Sar
    | Eq | Ne | Lt | Le | Gt | Ge
    | Load | Store
    | Call | Return
    | Branch | ConditionalBranch
    | Phi | Select
    | Alloca | GetElementPtr
    | Cast | Truncate | Extend
End Type

Process called "build_mir" that takes hir as HIRModule returns MIRProgram:
    Let builder be create_mir_builder()

    Let program be a value of type MIRProgram with
        modules as a list containing nothing,
        entry_point as "main",
        target_info as get_target_info()

    For Each hir_module in get_all_modules(hir):
        Let mir_module be transform_hir_module(builder, hir_module)
        Add mir_module to end of program.modules
    End For

    Note: Convert to SSA form
    For Each module in program.modules:
        For Each function in module.functions:
            convert_to_ssa(function)
        End For
    End For

    Return program
End Process

Process called "convert_to_ssa" that takes function as MIRFunction returns Nothing:
    Note: Step 1: Compute dominance frontiers
    Let dom_tree be compute_dominance_tree(function)
    Let dom_frontiers be compute_dominance_frontiers(function, dom_tree)

    Note: Step 2: Insert phi nodes
    For Each variable in function.locals:
        Let defs be find_definitions(function, variable)
        For Each def_block in defs:
            For Each frontier_block in dom_frontiers at key def_block:
                insert_phi_node(frontier_block, variable)
            End For
        End For
    End For

    Note: Step 3: Rename variables
    Let counter be a dictionary containing nothing
    rename_variables(function.basic_blocks at index 0, counter, dom_tree)

    Set function.is_ssa to true
End Process
```

#### 3.3 Basic MIR Optimizations
**File**: `/runa/bootstrap/v0.2_syber-core/mir/mir_optimizer.runa`

```runa
Type called "OptimizationPass":
    name as String
    level as OptimizationLevel Note: O0, O1, O2, O3
    transform as Process(MIRFunction) returns Boolean
End Type

Process called "optimize_mir" that takes program as MIRProgram, level as OptimizationLevel returns MIRProgram:
    Let passes be get_optimization_passes(level)

    Let changed be true
    While changed:
        Set changed to false

        For Each pass in passes:
            For Each module in program.modules:
                For Each function in module.functions:
                    If pass.transform(function):
                        Set changed to true
                    End If
                End For
            End For
        End For
    End While

    Return program
End Process

Process called "constant_folding" that takes function as MIRFunction returns Boolean:
    Let changed be false

    For Each block in function.basic_blocks:
        For Each inst in block.instructions:
            If is_arithmetic_op(inst.opcode):
                If all_operands_constant(inst.operands):
                    Let result be evaluate_constant_op(inst)
                    replace_instruction_with_constant(inst, result)
                    Set changed to true
                End If
            End If
        End For
    End For

    Return changed
End Process

Process called "dead_code_elimination" that takes function as MIRFunction returns Boolean:
    Let changed be false
    Let used_values be compute_used_values(function)

    For Each block in function.basic_blocks:
        Let new_instructions be a list containing nothing

        For Each inst in block.instructions:
            If inst.result is not nothing:
                If not (used_values contains inst.result):
                    Note: Dead instruction, skip it
                    Set changed to true
                    Continue
                End If
            End If

            Add inst to end of new_instructions
        End For

        Set block.instructions to new_instructions
    End For

    Return changed
End Process

Process called "common_subexpression_elimination" that takes function as MIRFunction returns Boolean:
    Let changed be false
    Let expressions be a dictionary containing nothing

    For Each block in function.basic_blocks:
        For Each inst in block.instructions:
            If is_pure_instruction(inst):
                Let key be hash_instruction(inst)

                If expressions contains key key:
                    Let existing be expressions at key key
                    replace_uses(inst.result, existing)
                    remove_instruction(inst)
                    Set changed to true
                Otherwise:
                    Set expressions at key key to inst.result
                End If
            End If
        End For
    End For

    Return changed
End Process
```

#### 3.4 LIR (Low-level IR) Implementation
**File**: `/runa/bootstrap/v0.2_syber-core/lir/lir_builder.runa`

```runa
Type called "LIRProgram":
    functions as List[LIRFunction]
    data_section as DataSection
    target as TargetMachine
End Type

Type called "LIRFunction":
    name as String
    instructions as List[LIRInstruction]
    frame_size as Integer
    spill_slots as List[SpillSlot]
    calling_convention as CallingConvention
End Type

Type called "LIRInstruction":
    opcode as LIROpcode
    operands as List[LIROperand]
    result as Optional[LIROperand]
    flags as InstructionFlags
End Type

Type LIROpcode is:
    | MOV | LEA
    | ADD | SUB | IMUL | IDIV
    | AND | OR | XOR | NOT
    | SHL | SHR | SAR
    | CMP | TEST
    | JMP | JE | JNE | JG | JGE | JL | JLE
    | CALL | RET
    | PUSH | POP
    | LOAD | STORE
End Type

Type called "LIROperand":
    kind as OperandKind
    value as Integer
    size as OperandSize
End Type

Type OperandKind is:
    | Register as RegisterId
    | Immediate as Integer
    | Memory as MemoryOperand
    | Label as String
End Type

Process called "build_lir" that takes mir as MIRProgram returns LIRProgram:
    Let builder be create_lir_builder()

    Let program be a value of type LIRProgram with
        functions as a list containing nothing,
        data_section as create_data_section(),
        target as get_target_machine()

    For Each mir_function in get_all_functions(mir):
        Let lir_function be lower_mir_function(builder, mir_function)
        Add lir_function to end of program.functions
    End For

    Return program
End Process

Process called "lower_mir_function" that takes builder as LIRBuilder, mir_func as MIRFunction returns LIRFunction:
    Let lir_func be a value of type LIRFunction with
        name as mir_func.name,
        instructions as a list containing nothing,
        frame_size as 0,
        spill_slots as a list containing nothing,
        calling_convention as SystemV_AMD64

    Note: Lower each basic block
    For Each block in mir_func.basic_blocks:
        lower_basic_block(builder, block, lir_func)
    End For

    Note: Perform register allocation
    allocate_registers(lir_func)

    Note: Calculate frame size
    Set lir_func.frame_size to calculate_frame_size(lir_func)

    Return lir_func
End Process
```

#### 3.5 Register Allocation
**File**: `/runa/bootstrap/v0.2_syber-core/lir/register_allocator.runa`

```runa
Type called "RegisterAllocator":
    available_registers as List[RegisterId]
    register_map as Dictionary[MIRValue, RegisterId]
    spill_map as Dictionary[MIRValue, SpillSlot]
    live_intervals as List[LiveInterval]
End Type

Type called "LiveInterval":
    value as MIRValue
    start as Integer
    end as Integer
    register as Optional[RegisterId]
    spilled as Boolean
End Type

Process called "allocate_registers" that takes function as LIRFunction returns Nothing:
    Let allocator be create_register_allocator()

    Note: Compute live intervals
    Let intervals be compute_live_intervals(function)

    Note: Sort intervals by start point
    sort_by_start(intervals)

    Note: Linear scan allocation
    For Each interval in intervals:
        If not try_allocate_register(allocator, interval):
            spill_interval(allocator, interval)
        End If
    End For

    Note: Rewrite instructions with allocated registers
    rewrite_with_allocation(function, allocator)
End Process

Process called "try_allocate_register" that takes allocator as RegisterAllocator, interval as LiveInterval returns Boolean:
    For Each reg in allocator.available_registers:
        If is_register_free(allocator, reg, interval):
            Set interval.register to reg
            mark_register_used(allocator, reg, interval)
            Return true
        End If
    End For

    Return false
End Process
```

#### 3.6 Native Object File Generation
**File**: `/runa/bootstrap/v0.2_syber-core/object_writer.runa`

```runa
Type called "ELFWriter":
    output as BinaryBuffer
    sections as List[Section]
    symbols as List[Symbol]
    relocations as List[Relocation]
End Type

Process called "write_object_file" that takes lir as LIRProgram, filename as String returns Nothing:
    Let writer be create_elf_writer()

    Note: Write ELF header
    write_elf_header(writer)

    Note: Generate code section
    Let code_section be generate_code_section(lir)
    Add code_section to end of writer.sections

    Note: Generate data section
    Let data_section be generate_data_section(lir)
    Add data_section to end of writer.sections

    Note: Generate symbol table
    generate_symbol_table(writer, lir)

    Note: Generate relocation entries
    generate_relocations(writer, lir)

    Note: Write section headers
    write_section_headers(writer)

    Note: Write to file
    WriteFile writer.output to filename
End Process
```

### Multi-Platform Support in v0.3

**Supported Targets**:
1. **x86_64-linux-gnu** (enhanced from v0.2)
2. **aarch64-linux-gnu** (NEW)
3. **x86_64-windows-pe** (NEW - experimental)

**Implementation Strategy**:
```runa
Type called "TargetMachine":
    arch as Architecture
    os as OperatingSystem
    abi as ABI
    pointer_size as Integer
    endianness as Endianness
    calling_convention as CallingConvention
End Type

Type Architecture is:
    | X86_64
    | AArch64
    | RISCV64
End Type

Process called "generate_target_code" that takes lir as LIRProgram, target as TargetMachine returns String:
    Match target.arch:
        When X86_64:
            Return generate_x86_64_assembly(lir, target)
        When AArch64:
            Return generate_aarch64_assembly(lir, target)
        Otherwise:
            Error("Unsupported architecture")
    End Match
End Process
```

### LLVM Dependency Status

**v0.3 is COMPLETELY INDEPENDENT of LLVM**
- No LLVM libraries linked
- No LLVM IR generation
- Direct assembly/machine code generation
- Native object file writing

**How Independence is Achieved**:
1. Assembly generation for each platform
2. Direct ELF/PE/Mach-O writing
3. System assembler/linker for final executable

---

## PHASE 4: v0.4 PRODUCTION SYBER-CORE

### Objective
Transform v0.3's basic Syber-Core into a production-quality optimizing compiler with advanced features.

### Major Enhancements

#### 4.1 Advanced Optimization Pipeline
**File**: `/runa/bootstrap/v0.4_moderate-runa/optimization_pipeline.runa`

```runa
Type called "OptimizationPipeline":
    passes as List[OptimizationPass]
    profiling_data as Optional[ProfileData]
    target_specific as Boolean
End Type

Process called "create_o3_pipeline" returns OptimizationPipeline:
    Let pipeline be a value of type OptimizationPipeline with
        passes as a list containing:
            create_pass("inline_small_functions", 100),
            create_pass("constant_propagation", 200),
            create_pass("dead_code_elimination", 300),
            create_pass("common_subexpression_elimination", 400),
            create_pass("loop_invariant_code_motion", 500),
            create_pass("loop_unrolling", 600),
            create_pass("vectorization", 700),
            create_pass("instruction_combining", 800),
            create_pass("global_value_numbering", 900),
            create_pass("partial_redundancy_elimination", 1000),
            create_pass("tail_call_optimization", 1100),
            create_pass("scalar_replacement_of_aggregates", 1200),
            create_pass("instruction_scheduling", 1300),
            create_pass("register_coalescing", 1400),
            create_pass("peephole_optimization", 1500)
        End List,
        profiling_data as nothing,
        target_specific as true

    Return pipeline
End Process
```

#### 4.2 Inlining Heuristics
```runa
Process called "should_inline" that takes caller as MIRFunction, callee as MIRFunction, call_site as CallSite returns Boolean:
    Note: Basic size threshold
    If instruction_count(callee) is greater than 50:
        Return false
    End If

    Note: Always inline tiny functions
    If instruction_count(callee) is less than 5:
        Return true
    End If

    Note: Hot path inlining
    If call_site.execution_count is greater than 1000:
        If instruction_count(callee) is less than 20:
            Return true
        End If
    End If

    Note: Recursive function check
    If is_recursive(callee):
        Return false
    End If

    Note: Cost-benefit analysis
    Let benefit be estimate_inlining_benefit(caller, callee, call_site)
    Let cost be estimate_inlining_cost(callee)

    Return benefit is greater than cost
End Process
```

#### 4.3 Loop Optimizations
```runa
Process called "optimize_loops" that takes function as MIRFunction returns Nothing:
    Let loops be detect_natural_loops(function)

    For Each loop in loops:
        Note: Loop-invariant code motion
        hoist_invariant_code(loop)

        Note: Loop strength reduction
        reduce_strength(loop)

        Note: Loop unrolling
        If should_unroll(loop):
            unroll_loop(loop)
        End If

        Note: Loop vectorization
        If can_vectorize(loop):
            vectorize_loop(loop)
        End If

        Note: Loop fusion
        try_fuse_adjacent_loops(loop, loops)
    End For
End Process
```

#### 4.4 Auto-Vectorization
```runa
Process called "vectorize_loop" that takes loop as Loop returns Nothing:
    Let vector_width be get_vector_width_for_target()

    Note: Check data dependencies
    If has_loop_carried_dependencies(loop):
        Return
    End If

    Note: Transform scalar operations to vector operations
    For Each inst in loop.body:
        If is_vectorizable(inst):
            Let vector_inst be create_vector_instruction(inst, vector_width)
            replace_instruction(inst, vector_inst)
        End If
    End For

    Note: Add loop peeling for alignment
    add_alignment_prologue(loop, vector_width)

    Note: Add remainder loop for non-multiple iterations
    add_remainder_epilogue(loop, vector_width)
End Process
```

### Complete Platform Support

**Tier 1 Platforms** (Fully Optimized):
- x86_64-linux-gnu
- x86_64-windows-msvc
- x86_64-apple-darwin
- aarch64-linux-gnu
- aarch64-apple-darwin

**Tier 2 Platforms** (Functional, Less Optimized):
- armv7-linux-gnueabihf
- riscv64-linux-gnu
- wasm32-unknown-unknown

**Cross-Compilation Matrix**:
```runa
Process called "configure_cross_compilation" that takes host as String, target as String returns CompilerConfig:
    Let config be default_config()

    Note: Configure for target architecture
    Set config.target to parse_target_triple(target)

    Note: Set up cross-toolchain paths
    Match target:
        When contains("windows"):
            Set config.linker to "x86_64-w64-mingw32-ld"
            Set config.archiver to "x86_64-w64-mingw32-ar"

        When contains("darwin"):
            Set config.linker to "x86_64-apple-darwin-ld"
            Set config.archiver to "x86_64-apple-darwin-ar"

        When contains("wasm"):
            Set config.linker to "wasm-ld"
            Set config.output_type to WebAssembly
    End Match

    Return config
End Process
```

### Advanced Language Features

#### 4.5 Generic Types
```runa
Type called "GenericFunction":
    type_parameters as List[TypeParameter]
    constraints as List[TypeConstraint]
    body as FunctionBody
    instantiations as Dictionary[List[Type], MIRFunction]
End Type

Process called "instantiate_generic" that takes generic as GenericFunction, type_args as List[Type] returns MIRFunction:
    Note: Check if already instantiated
    Let key be hash_type_list(type_args)
    If generic.instantiations contains key key:
        Return generic.instantiations at key key
    End If

    Note: Verify type constraints
    For Each constraint in generic.constraints:
        If not satisfies_constraint(type_args, constraint):
            Error("Type constraint violation")
        End If
    End For

    Note: Perform substitution
    Let specialized be substitute_types(generic.body, generic.type_parameters, type_args)

    Note: Generate specialized MIR
    Let mir_func be generate_mir_for_function(specialized)

    Note: Cache instantiation
    Set generic.instantiations at key key to mir_func

    Return mir_func
End Process
```

#### 4.6 Async/Await Support
```runa
Type called "AsyncFunction":
    state_machine as StateMachine
    yield_points as List[YieldPoint]
    continuation as Optional[Continuation]
End Type

Process called "transform_async_function" that takes function as MIRFunction returns AsyncFunction:
    Let async_func be a value of type AsyncFunction with
        state_machine as create_state_machine(),
        yield_points as a list containing nothing,
        continuation as nothing

    Note: Identify await points
    For Each block in function.basic_blocks:
        For Each inst in block.instructions:
            If is_await_call(inst):
                Let yield_point be create_yield_point(inst, block)
                Add yield_point to end of async_func.yield_points
            End If
        End For
    End For

    Note: Transform to state machine
    transform_to_state_machine(function, async_func)

    Return async_func
End Process
```

---

## PHASE 5: v0.5 FINAL PRODUCTION COMPILER

### Objective
The complete, production-ready Runa compiler with all features, optimizations, and platform support.

### Complete Feature Set

#### 5.1 Full Language Features
```runa
- All primitive types
- All collection types (List, Dictionary, Set, Array)
- All control flow (If, While, For, Match, Try)
- Pattern matching with guards
- Algebraic data types
- Generic types with constraints
- Async/await with cancellation
- Actors and message passing
- Modules and packages
- Traits and type classes
- Macros and compile-time execution
- Foreign function interface (FFI)
- Inline assembly
- SIMD intrinsics
```

#### 5.2 Complete Optimization Suite
```runa
- Interprocedural optimization
- Link-time optimization (LTO)
- Profile-guided optimization (PGO)
- Whole-program devirtualization
- Auto-parallelization
- GPU kernel generation
- Cache optimization
- Power optimization for mobile
- Size optimization mode
- Debug optimization mode
```

#### 5.3 Developer Tools
```runa
- Integrated debugger support
- Profiler integration
- Coverage instrumentation
- Sanitizer support (address, thread, undefined behavior)
- Static analysis
- Incremental compilation
- Parallel compilation
- Distributed compilation
- Language server protocol (LSP)
```

### Complete Platform Matrix

**Native Targets** (42 platforms):
```
x86_64: linux, windows, macos, freebsd, openbsd, netbsd
i686: linux, windows
aarch64: linux, macos, windows, android, ios
armv7: linux, android, ios
riscv64: linux
powerpc64: linux
mips64: linux
s390x: linux
wasm32: browser, node, wasi
```

**Compilation Targets**:
- Native executables
- Shared libraries (.so, .dll, .dylib)
- Static libraries (.a, .lib)
- WebAssembly modules
- CUDA kernels
- OpenCL kernels
- Vulkan compute shaders

### Syber-Core Architecture Completion

#### Final IR Pipeline
```
Source → Lexer → Parser → Type Checker →
HIR (with semantic analysis) →
MIR (with 30+ optimization passes) →
LIR (with register allocation) →
Machine Code Generation →
Object File → Linker → Executable
```

#### Performance Metrics
```runa
Type called "CompilerMetrics":
    lines_per_second as Integer       Note: > 100,000
    optimization_time as Float         Note: < 10% of total
    memory_usage as Integer            Note: < 1GB for 1M LOC
    binary_size as Integer             Note: < 10MB for compiler
    compilation_deterministic as Boolean Note: Always true
End Type
```

---

## DEPENDENCY LIBERATION TIMELINE

### LLVM Dependency Period
- **v0.1**: FULLY DEPENDENT on LLVM
  - Uses LLVM for all code generation
  - Requires LLVM 17+ installed
  - Links against LLVM libraries

### LLVM Liberation Process
- **v0.2**: LLVM-FREE
  - Generates assembly directly
  - Uses system assembler (as)
  - Uses system linker (ld/lld)

- **v0.3**: Partial toolchain independence
  - Writes ELF files directly
  - Still uses system linker

- **v0.4**: Near-complete independence
  - Implements basic linker
  - Can produce executables without external tools

- **v0.5**: COMPLETE INDEPENDENCE
  - Built-in assembler
  - Built-in linker
  - Direct executable generation
  - No external toolchain required

### How LLVM is Replaced

**LLVM Components** → **Syber-Core Replacements**:
```
LLVM IR → Runa MIR/LIR
LLVM Optimizer → Syber-Core Optimization Pipeline
LLVM CodeGen → Syber-Core Machine Code Generator
LLVM MC → Syber-Core Assembly/Object Writer
LLVM Linker → Syber-Core Linker
```

---

## BUILD REQUIREMENTS PER PHASE

### v0.1 Build Requirements
```bash
# Required
- Rust 1.70+
- LLVM 17+
- Cargo
- C compiler (for LLVM)

# Commands
cargo build --release
```

### v0.2 Build Requirements
```bash
# Required
- v0.1 compiler (to bootstrap)
- GNU as (assembler)
- GNU ld or lld (linker)
- libc headers

# Commands
v0.1/runac v0.2/main.runa -o v0.2/runac
```

### v0.3 Build Requirements
```bash
# Required
- v0.2 compiler
- System linker (ld/lld)
- No LLVM needed

# Commands
v0.2/runac v0.3/main.runa -o v0.3/runac
```

### v0.4 Build Requirements
```bash
# Required
- v0.3 compiler
- Optional: system linker for fallback

# Commands
v0.3/runac v0.4/main.runa -o v0.4/runac --no-external-linker
```

### v0.5 Build Requirements
```bash
# Required
- v0.4 compiler
- NOTHING ELSE

# Commands
v0.4/runac v0.5/main.runa -o v0.5/runac --fully-self-contained
```

---

## CRITICAL SUCCESS METRICS

### Per-Version Success Criteria

**v0.1 Success**:
- ✓ Compiles v0.2 source code
- ✓ All v0.2 language features work
- ✓ Produces working executables
- ✓ Test suite passes

**v0.2 Success**:
- ✓ Compiles itself (self-hosting)
- ✓ Generated assembly runs correctly
- ✓ No LLVM dependency
- ✓ Performance within 5x of v0.1

**v0.3 Success**:
- ✓ MIR/LIR pipeline works
- ✓ Basic optimizations functional
- ✓ Multi-platform support (2+ architectures)
- ✓ Performance within 2x of v0.1

**v0.4 Success**:
- ✓ Advanced optimizations work
- ✓ 5+ platform targets
- ✓ Performance matches v0.1
- ✓ Can build large programs (>100k LOC)

**v0.5 Success**:
- ✓ All Runa features implemented
- ✓ Performance EXCEEDS C/Rust
- ✓ Zero external dependencies
- ✓ Production ready

---

## IMPLEMENTATION CHECKPOINTS

### Checkpoint 1: v0.1 Feature Complete
```
□ Existing features verified from scratch
□ File I/O works
□ String operations work
□ Collections work
□ Type definitions work
□ Module system works
□ Can compile test_bootstrap.runa successfully
```

### Checkpoint 2: v0.2 Self-Hosting
```
□ v0.2 compiles with v0.1
□ v0.2 compiles itself
□ Assembly generation correct
□ No LLVM in v0.2 binary
```

### Checkpoint 3: v0.3 Syber-Core Operational
```
□ HIR → MIR → LIR pipeline works
□ Register allocation works
□ Basic optimizations measurable
□ ARM64 target works
```

### Checkpoint 4: v0.4 Production Features
```
□ Generics work
□ Async/await works
□ Advanced optimizations measurable
□ Cross-compilation works
□ Debug info generation works
```

### Checkpoint 5: v0.5 Complete
```
□ All language features work
□ All optimizations work
□ All platforms supported
□ Zero dependencies
□ Performance goals met
```

---

## RISK MITIGATION

### Technical Risks and Mitigations

**Risk**: Register allocation complexity
**Mitigation**: Start with simple linear scan, improve iteratively

**Risk**: Debugging self-hosted compiler
**Mitigation**: Extensive logging, intermediate dumps, comparison with v0.1

**Risk**: Platform-specific bugs
**Mitigation**: Start with x86-64 only, add platforms gradually

**Risk**: Optimization correctness
**Mitigation**: Extensive test suite, fuzzing, gradual enablement

**Risk**: Binary size explosion
**Mitigation**: Dead code elimination, LTO, size optimization mode

---

## TESTING STRATEGY

### Test Programs Required at Each Phase

**v0.1 Tests**:
```runa
- basic_arithmetic.runa
- string_operations.runa
- file_io.runa
- collections.runa
- type_definitions.runa
- control_flow.runa
- function_calls.runa
- module_imports.runa
```

**v0.2 Tests**:
```runa
- self_compile.runa (v0.2 compiling itself)
- lexer_test.runa
- parser_test.runa
- codegen_test.runa
- assembly_test.runa
```

**v0.3 Tests**:
```runa
- mir_tests.runa
- optimization_tests.runa
- register_allocation_tests.runa
- multi_platform_tests.runa
```

**v0.4 Tests**:
```runa
- generic_tests.runa
- async_tests.runa
- vectorization_tests.runa
- cross_compilation_tests.runa
```

**v0.5 Tests**:
```runa
- complete_language_tests.runa
- performance_benchmarks.runa
- stress_tests.runa
- compatibility_tests.runa
```

---

## CONCLUSION

This document represents the complete, detailed technical specification for bootstrapping the Runa programming language from its current embryonic state to a fully independent, production-ready compiler system.

The journey spans five compiler versions:
1. **v0.1**: Rust+LLVM bootstrap (enhancement phase)
2. **v0.2**: First self-hosted compiler (assembly backend)
3. **v0.3**: Initial Syber-Core architecture (MIR/LIR)
4. **v0.4**: Production Syber-Core (advanced optimizations)
5. **v0.5**: Complete production compiler (all features)

By following this specification exactly, Runa will achieve:
- Complete independence from external toolchains
- Performance exceeding existing systems languages
- Support for all modern platforms
- A proven self-hosting compiler architecture
- The foundation for Runa's ecosystem dominance

The path is clear. The specification is complete. Implementation begins now.

## END OF SPECIFICATION