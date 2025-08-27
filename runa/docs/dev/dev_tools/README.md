## Developer Toolchain for Runa

Welcome to the documentation for the Runa Developer Toolchain. Runa is designed from the ground up to be an expressive, safe, and globally accessible programming language. A key part of this mission is providing a suite of powerful, integrated tools that make developing in Runa a productive and enjoyable experience.

This documentation is for developers building tools for Runa or those who want a deeper understanding of the compiler, formatter, linter, and translation pipeline.

> For a guide on how to *use* Runa and its features, please see the **[Runa User Documentation](../../user/README.md)**.

### Philosophy

The Runa toolchain is built on a few core principles that directly reflect the language's design goals:

1.  **Safety and Predictability**: Tooling should prevent errors, not introduce them. Automated changes, like formatting and code fixes, are designed to be safe, deterministic, and behavior-preserving.
2.  **Developer Ergonomics**: The developer experience is paramount. Tools are designed to be intuitive, provide clear feedback, and automate tedious tasks, freeing developers to focus on logic and creativity.
3.  **Global Accessibility (Localization-First)**: Runa is architected to not be gated by English proficiency. The toolchain's built-in localization and translation features are a core part of the development lifecycle, not an afterthought.
4.  **Dual Syntax Support**: Runa supports both a highly readable natural language syntax and a more conventional symbolic syntax. The toolchain provides seamless conversion between them, allowing developers to use the form they are most comfortable with.

---

### Structure of the Toolchain

The developer tools are located in `runa/src/dev_tools/` and are organized into several key components:

| Component | Description |
| :--- | :--- |
| **[CLI Toolkit](./cli/README.md)** | The command-line interface is the primary entry point for all developer tasks, from creating a new project to building, testing, and translating code. |
| **[Formatter](./formatting/README.md)** | A deterministic code formatter that automatically canonicalizes syntax, enforces style, and ensures consistency across a codebase. |
| **[Linter (`doctor`)](./linting/doctor.md)** | A static analysis tool that detects potential bugs, style issues, and semantic errors. It provides actionable feedback and can automatically apply safe fixes. |
| **[Syntax Converter](./syntax_converter/README.md)** | Tools to convert Runa code between its natural language form and its symbolic (`developer_mode`) form. |
| **[Localization Engine](./localization/README.md)** | The core engine that powers the translation of Runa's keywords and operators between different human languages. |
| **[Build Normalization](./build_normalization.md)** | An automated step in the build process that converts all source code into a canonical, language-agnostic form before compilation. |

---

### How the Tools Work Together

A typical workflow in Runa leverages multiple tools in the chain. For example, when you run `runa test`:

1.  The **CLI** parses your command.
2.  It discovers all test files, which may be written in different languages (e.g., Spanish or Japanese).
3.  The **Build Normalization** step is invoked. The **Localization Engine** reads each file, translates its keywords and operators into the canonical English form, and saves the result in a temporary build directory.
4.  The Runa compiler then compiles the normalized, canonical code.
5.  During this process, the compiler's semantic analysis may detect issues, like using `+` for string concatenation, and report an error.
6.  A developer could then run `runa doctor --fix` to have the **Linter** and **Formatter** automatically correct this and other issues in the original source file.

This integrated approach ensures consistency and correctness while allowing developers to write code in the language and style that is most natural to them.