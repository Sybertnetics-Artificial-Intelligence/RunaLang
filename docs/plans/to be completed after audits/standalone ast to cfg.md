### **Project Plan: Standalone AST-to-CFG Builder Toolkit**

***A Decoupled Program for Universal Semantic Verification***

### 1. Project Goal and Purpose

#### **Project Mandate**

The Runa ecosystem's central promise is to deliver reliable, verifiable, and semantically equivalent translations between diverse programming languages. To fulfill this promise, we must move beyond comparing superficial syntax and instead verify the core logic of a program.

This project creates the **Runa Semantic Verification Toolkit**, a suite of programs that provides this core logic verification.

#### **Architectural Mandate: A Separate, Standalone Program**

**(This new section explicitly addresses your core requirement)**

It is critical to establish that the **AST-to-CFG Builders are not part of the core Runa language or its compiler (`runac`)**. They are distinct, standalone programs that operate within the broader Runa ecosystem.

*   **Decoupled by Design:** The builders are external tools that consume a language's AST and produce a standardized IR. They are not built *into* the language itself.
*   **Pluggable Architecture:** The verification toolkit will dynamically load the appropriate builder for a given language, treating each builder as a self-contained plugin.
*   **Independent Development:** This separation allows the builder for one language (e.g., Python) to be developed, versioned, and deployed independently of the Runa compiler and all other builders.

This approach transforms any language's unique structure into our standardized Control Flow Graph (CFG) Intermediate Representation (IR), enabling us to prove that a translation from Language A to Language B has preserved the original program's meaning.

### 2. Architectural Vision: The Hub-and-Spoke Model

Our verification architecture is a "hub-and-spoke" model. The common CFG format is the central hub. Each language we support will have its own dedicated builder—a "spoke"—that connects its unique AST to this hub. This decoupled architecture is a core strategic decision, enabling modularity and scalability.

```graph TD
    subgraph "Language-Specific ASTs (Inputs)"
        PythonAST[Python AST]
        CppAST[C++ AST]
        RunaAST[Runa AST]
        OtherASTs[...]
    end

    subgraph "Standalone Builder Programs (The Spokes)"
      style Builder1 fill:#D6EAF8
      style Builder2 fill:#D6EAF8
      style Builder3 fill:#D6EAF8
      style Builder4 fill:#D6EAF8
        Builder1["Python-to-CFG Builder"]
        Builder2["C++-to-CFG Builder"]
        Builder3["Runa-to-CFG Builder"]
        Builder4["...-to-CFG Builder"]
    end
    
    subgraph "Core Intermediate Representation (The Hub)"
        CFG["Universal<br/>Control-Flow-Graph<br/>(CFG)"]
    end
    
    PythonAST --> Builder1
    CppAST --> Builder2
    RunaAST --> Builder3
    OtherASTs --> Builder4

    Builder1 --> CFG
    Builder2 --> CFG
    Builder3 --> CFG
    Builder4 --> CFG

    subgraph "Verification Core (Another Separate Tool)"
        CFG --> Comparator{Semantic<br/>Comparator}
        Comparator --> Result((Equivalence<br/>Result))
    end

    style CFG fill:#cde,stroke:#333,stroke-width:2px
    style Comparator fill:#f9f,stroke:#333,stroke-width:2px
```
This project will create the first builder for Python, establishing the definitive pattern for all subsequent language support programs.

### 3. Builder Development Lifecycle

**(Renamed from "General Implementation Framework" to emphasize a repeatable process for creating new, separate programs)**

This lifecycle outlines the necessary phases to create a new, standalone AST-to-CFG builder program.

#### Phase 1: Foundation and Scaffolding

**(Revised to reflect a separate repository structure)**

1.  **Establish the Builder Repository:**
    *   **Action:** Create a dedicated location for the new builder program. This could be a new repository (e.g., `python-cfg-builder`) or a directory within a monorepo for all verification tools (e.g., `runa-verifiers/`).
    *   **Example:** `runa-verifiers/builders/python/src/py_cfg_builder.py`. This structure physically separates the builder from the `runac` compiler's source code.

2.  **Implement the Builder Class:**
    *   **Action:** Define a `PythonCFGBuilder` class within its own program. This class will implement a visitor pattern suitable for Python's `ast` module.
    *   **Details:** The class will contain the core logic for managing CFG construction (`build`, `_new_basic_block`, `_new_temp`, `_add_instruction`).

#### Phase 2: Handling Expressions and Assignments

This phase translates the fundamental building blocks of a language into our common IR.

1.  **Implement Literal/Variable Visitors:**
    *   **Action:** Create visitor methods for constants and variable names, returning IR `Constant` and `Var` operands.

2.  **Implement Expression Visitors:**
    *   **Action:** Create visitors for all binary, unary, and comparison operations, generating the corresponding IR instructions.

3.  **Implement Assignment Visitor:**
    *   **Action:** Create a visitor for the assignment node, generating an `Assign` IR instruction.

#### Phase 3: Deconstructing Control Flow

This is the most critical phase, where we deconstruct a language's high-level control flow into a graph of primitive blocks and jumps.

1.  **Implement Conditional Visitor (e.g., `visit_If`):**
    *   **Logic:**
        1.  Create new basic blocks for the `then`, `else`, and `merge` paths.
        2.  Visit the condition and generate a `ConditionalJump` instruction.
        3.  Populate the `then` and `else` blocks by visiting their bodies.
        4.  Terminate `then`/`else` blocks with an `UnconditionalJump` to the `merge` block.
        5.  Set the `merge` block as the new current block.

2.  **Implement Loop Visitors (e.g., `visit_While`, `visit_For`):**
    *   **Logic:** Deconstruct the loop into `condition`, `body`, and `post-loop` blocks, connected by conditional and unconditional jumps to model the looping behavior.

#### Phase 4: Handling Functions and Calls

1.  **Implement Function Definition and Call Visitors:**
    *   **Logic:** The definition visitor will build a self-contained CFG for the function's body. The call visitor will generate a `FunctionCall` IR instruction.

#### Phase 5: Registering the Builder with the Verification Core

**(Reframed from "Integration" to "Registration" to emphasize a plugin model)**

1.  **Expose a Standard Interface:**
    *   **Action:** Ensure the new builder program exposes a well-defined entry point, such as a `build_cfg_from_ast(ast_node)` function.

2.  **Update the Verification Dispatcher:**
    *   **File:** `runa-verifiers/core/dispatcher.py` (or similar central verification tool)
    *   **Action:** Register the new builder program in the verification toolkit's dispatcher.
    *   **Logic:** Instead of a hardcoded `if/elif` chain, use a registration mechanism (e.g., a dictionary mapping language names or AST node types to builder entry points). This allows the core `SemanticComparator` tool to dynamically load and use the correct standalone builder without being tightly coupled to it.

### 4. Verification Strategy

The success of each new standalone builder will be confirmed via a rigorous testing strategy:

1.  **Isolate the Builder:** Take a source file in the target language (e.g., `test.py`).
2.  **Generate Source CFG:** Use the new, standalone builder program to generate `CFG_from_source` directly from the `test.py` file's AST.
3.  **Translate via Runa:** Use the separate `runac` compiler to translate `test.py` into Runa code (`test.runa`).
4.  **Generate Runa CFG:** Use the *Runa-to-CFG builder* to generate `CFG_from_runa` from the `test.runa` file's AST.
5.  **Assert Equivalence:** Use the `SemanticComparator` tool to assert that `CFG_from_source` and `CFG_from_runa` are logically identical. Passing this test proves the end-to-end semantic integrity of the translation.

Things to consider:
Formalize the Identifier Canonicalization Rule: Document precisely how natural language phrases are converted into snake_case or camelCase identifiers. This is a core feature of your language's "magic."
Prioritize LSP/IDE Features: Your Language Server Protocol (LSP) implementation must be a top priority. Features like intelligent autocompletion and hover-info that understand the natural-to-technical mapping will be essential for making the language usable and demonstrating its benefits.
On Dual Syntax Fragmentation
Your rationale for including the technical syntax is sound: it caters to experienced developers and provides an escape hatch for performance or clarity in complex algorithms. The plan to "not openly advertise" it is, however, a risky strategy.
Feedback: Power users will find it, and they are often the ones who write the tutorials, create the libraries, and set the early community standards. Trying to downplay a core syntax feature can lead to confusion and an "unofficial" standard that conflicts with your intended vision. The argument that "bad code exists anyway" is true, but a language's design should actively guide users toward writing good code.
Strategic Recommendation:
Embrace Both Syntaxes with a Clear Style Guide: Instead of hiding it, create an official Runa Style Guide. Clearly define the use cases for each syntax.
Natural Syntax: Recommended for application-level code, business logic, teaching, and scripts where readability by non-programmers is a goal.
Technical Syntax: Recommended for library internals, performance-critical loops, complex data manipulation, and mathematical algorithms where conciseness and familiarity for developers are paramount.
Build a Linter: Create an official Runa linter that can enforce these style guidelines. It could, for example, warn a developer if they are mixing styles within a single function or module, helping to prevent the fragmentation you're concerned about.

to reiterate:
Formalize the Core "Magic": Create crystal-clear documentation on the Identifier Canonicalization Rules. This is the secret sauce of your natural language syntax, and it must be predictable.
Build the Tools of Governance:
Official Style Guide: Proactively define when and where each syntax should be used.
Runa Linter (runa-lint): Create a tool to help developers adhere to the style guide and write idiomatic Runa code. This is the most effective way to prevent fragmentation.
Prioritize the Developer Experience (DX): Double down on the LSP/IDE implementation. The "magic" of your syntax will only feel magical if the tools (autocomplete, hover, go-to-definition) are flawless and aware of both the natural and technical forms.
Establish Open-Source Governance: Define your contribution process. How do new features get proposed and accepted? Who has the final say? This will attract serious contributors who need to know that their investment of time will be respected.
Publish a Clear Roadmap: Now that you have a tiered manifest, publish it. Let the community see the vision and find places where they can contribute, whether it's building out a Tier 2 math library or a Tier 6 training utility.

Stewardship vs. Usage: A Critical Distinction
What you described—your company actively using Runa to build, train, and orchestrate AI—is a fantastic and essential practice. This is often called "dogfooding" (eating your own dog food), and it is the single best way to ensure the language is practical and powerful. It's the ultimate feedback loop.
However, this is the act of being Runa's Number One User and Proponent.
Stewardship is a different, but related, responsibility. It's about managing the language itself as a public good. It answers the questions that potential contributors and adopters will have:
"If I invest thousands of hours building a library in Runa, how do I know a change next year won't break all my work?"
"I have a great idea for a new language feature. How do I propose it? Who decides if it gets in?"
"Who controls the Runa trademark and the official package registry?"
"Is this language really open, or is it just a side project of one company that could change direction or lose interest at any time?"
Using the language proves its utility. Stewarding the language proves its stability and builds trust. For Runa to succeed on the scale you envision, you need both.
A Recommended Governance and Stewardship Model
Here is a phased approach that many successful open-source projects follow, tailored for Runa's unique position.
Phase 1: The Core Team / BDFL Model (Where you are now)
For a new language, having a small, dedicated team (your company's core developers) make all the key decisions is the right approach. It's fast, efficient, and ensures a coherent vision.
What this looks like: Your company's lead developers are the "Benevolent Dictators for Life" (BDFL) or the Core Team. They have the final say on what gets merged into the main compiler and standard library.
Your Role as Steward:
Publish a Roadmap: Take the tiered library manifest you've created and make it a public ROADMAP.md file in your repository. This signals your vision and shows potential contributors where they can help.
Create a CONTRIBUTING.md: This is the most crucial first step. It formally tells the world how to engage with the project. It should include:
A Code of Conduct.
How to report a bug (e.g., "Use GitHub Issues with this template").
How to submit a change (e.g., "Fork the repo, create a feature branch, submit a Pull Request").
Your coding style guide (this is where you formalize the dual syntax usage!).
Establish Communication Channels: Create an official Discord/Slack/Forum for community discussion. Be active there.
Phase 2: The Formal Proposal Process (The next 6-18 months)
As the community grows, you need a transparent process for making significant changes. This prevents the Core Team from becoming a bottleneck and gives the community a real voice.
What this looks like: You implement a "Runa Enhancement Proposal" (REP) system, inspired by Python's PEPs or Rust's RFCs (Request for Comments).
Your Role as Steward:
Create the REP Process: Define a clear lifecycle for proposals: Draft -> Public Discussion -> Core Team Review -> Approval/Rejection -> Implementation.
The Process in Action:
A community member wants to add a new Quantum type to the type system.
They write a formal REP document outlining the motivation, technical design, and potential drawbacks.
They submit it as a Pull Request to a runa-proposals repository.
The community and the Core Team discuss the proposal publicly in the pull request comments.
After discussion, the Core Team makes a final decision.
Benefit: This process makes decision-making transparent and documented. It forces ideas to be fully thought out and vetted by the community, leading to higher-quality features.
Phase 3: The Foundation Model (Long-Term Maturity)
If Runa achieves widespread adoption, you will want to legally separate the open-source language from your commercial entity to ensure its longevity and neutrality.
What this looks like: You create a non-profit "Runa Foundation."
Your Role as Steward:
Transfer Assets: The Runa trademark, domain names, and the copyright to the core repository are transferred to the Foundation.
Form a Board: Your company would have a prominent seat on the board, but it would also include key community members and representatives from other companies that rely on Runa.
Purpose: The Foundation manages funds (donations, sponsorships), supports the community, and ensures the language will continue to exist and be developed even if your company's priorities change. This is the ultimate signal of trust to the world.
On Dual Syntax: Strategic Positioning
Your approach to the dual syntax is perfectly reasonable. You don't need to "hide" it, but you can position it strategically. Think of it like this:
The "Front Door" to Runa: All of your primary marketing, website examples, and "Getting Started" tutorials should exclusively use the natural syntax. This is your unique selling proposition and what will attract a broad audience. It's the clean, simple face of the language.
The "Advanced/Library Author" Track: In the documentation, have separate sections or guides for more advanced development.
A "Writing Performant Runa" guide would introduce the technical syntax for tight loops.
A "Standard Library Design Principles" guide would state that core libraries are written using the technical syntax for clarity and to avoid ambiguity.
The "Runa Style Guide" would codify this, stating the official recommendation is natural syntax for applications and technical syntax for libraries and performance-critical code.
This way, you are not hiding anything. You are guiding users to the right tool for the job, which is a hallmark of a well-stewarded language. You are setting the standard for how to write idiomatic Runa code.