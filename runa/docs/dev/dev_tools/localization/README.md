# Runa Localization & Translation Engine

Runa is designed to be a globally accessible language, and the Localization Engine is the core component that makes this possible. It allows developers to write Runa code using keywords and operators from a variety of human languages, which are then translated into a single, canonical form that the compiler can understand.

This document explains how this translation process works, how to use the translation tools, and how it all integrates seamlessly into the development workflow.

-   **Engine Source**: `runa/src/dev_tools/syntax_converter/localization/engine.runa`
-   **Language Catalogs**: `runa/src/dev_tools/syntax_converter/localization/catalogs/`

### Philosophy: A Language-Agnostic Compiler

The core design principle of Runa's localization system is that **the compiler itself is language-agnostic**. The compiler is only designed to understand one single set of tokens—the canonical, English-based Runa syntax.

All translation is handled by the developer toolchain *before* compilation. This is achieved through the **Build Normalization Pipeline**, which automatically translates all source code into the canonical form as the first step of any `build`, `run`, or `test` command. This approach keeps the compiler simple and robust while providing a powerful, multi-lingual development experience.

---

### How Translation Works: Strict Token-Based Mapping

It is critical to understand that the Runa Localization Engine is **not** a natural language processing (NLP) or machine translation (MT) system. It does not understand the *semantic meaning* of your code, identifiers, or comments.

Instead, it performs a **strict, token-based mapping**. Here's how it works:

1.  **Protect Literals**: The engine first scans the source code and "protects" any string literals and comments, replacing them with a temporary, unique placeholder. This ensures that the content of your strings and comments is never accidentally translated.
2.  **Token Mapping**: It then compares the remaining code against a **language catalog**. It finds and replaces known keywords and operators from the source language with their equivalents in the target language. This is done using a longest-match-first algorithm to correctly handle multi-word operators (e.g., "is greater than").
3.  **Reconstruct Code**: Finally, it reconstructs the code, putting the original string literals and comments back in place of their placeholders.

**Example: Translating from Spanish to Canonical English**

Consider the following Runa code written in Spanish:
```runa
Proceso "sumar" con a como Número, b como Número devuelve Número:
    Devolver a más b
```

When this code is built, the normalization pipeline translates it to the following canonical form before compilation:
```runa
Process "sumar" with a as Number, b as Number returns Number:
    Return a plus b
```
Notice that only the keywords (`Proceso`, `con`, `como`, `devuelve`, `Devolver`, `más`) were translated. The identifiers (`sumar`, `a`, `b`) and types (`Número`) which have direct mappings were also translated based on the catalog. If `Número` was not in the catalog it would remain, same for the identifiers.

### Language Catalogs

The translation logic is driven by language catalogs. Each supported language has a catalog file that contains two key dictionaries:

-   `to_canonical`: Maps words and phrases from that language *to* the canonical English form.
-   `from_canonical`: Maps words and phrases *from* the canonical English form to that language.

These catalogs are essential for both translating code with the `runa translate` command and for the automatic build normalization process.

**Supported Languages**: `en` (English/Canonical), `hi` (Hindi), `ja` (Japanese), `es` (Spanish), `zh` (Mandarin Chinese), `ru` (Russian).

### Manual Translation with `runa translate`

While build-time normalization is automatic, you can also perform manual translations using the `runa translate` command. This is useful for converting a file to share with a colleague who speaks a different language, or for standardizing a project to a single language.

See the **[Commands Reference](./cli/commands.md#runa-translate)** for detailed usage and examples.

### Round-Trip Testing

To ensure the integrity of the language catalogs, the Runa test suite includes round-trip tests. These tests take a source file, translate it from canonical English to every other supported language, and then translate it back to English. The test then asserts that the final result is identical to the original. This guarantees that the translation process is reversible and does not corrupt the code.


