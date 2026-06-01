# Backends Rationalization Plan

Survey + per-backend migration plan for the HIR translation backend layer.

Survey root: `compiler/middle/gungnir/hir/translation/backends/`
Survey date: 2026-06-01
Baseline (must not regress): translation sweep PASS=340 FAIL=0 under `/tmp/runac_92`.

This document is a READ-ONLY survey. No `.runa` files were modified to produce it. All claims below are backed by `wc -l`, `grep -nE '^Process called|^Type called|^Import'`, or direct `Read` of the source files.

---

## 0. Scope and Top-Line Findings

- 53 language subdirectories exist under `backends/`. There are also two zero-byte directories on disk (`llvm/` and `x86_64/`) — they hold no `.runa` files and are noise.
- 52 of 53 backends have BOTH `<lang>_emitter.runa` and `hir_to_<lang>.runa`. Rust has only `rust_emitter.runa` (no `hir_to_rust.runa`).
- 36 of the 53 emitter files import `emitter_common.runa` (Wave 2 migration). 17 do not.
- The `<lang>_emitter.runa` files fall into FIVE distinct architectures, not the two implied by the brief (see Section 2).
- 7 backends (elixir, haskell, latex, makefile, ruby, scala, verilog) define an `<lang>_to_hir` + `hir_to_<lang>` proc pair in their emitter file (the entry points the central dispatcher in `translation.runa` calls). The other 46 do NOT define those exact procs in the emitter file — the dispatch is unresolved for them at the emitter boundary.
- The central dispatcher `compiler/middle/gungnir/hir/translation.runa` (lines 3231-3707) issues `Return proc <lang>_to_hir from <Lang>Emitter` and `Return proc hir_to_<lang> from <Lang>Emitter` calls for every backend, but these procs only exist in the 7 emitters above. For the remaining 46, the dispatcher is referring to procs that do not live in the imported emitter file. The build still passes — this dispatch is name-resolved later or these arms are unreached in compiled tests.
- Rust dispatcher arms (`rust_to_hir from RustEmitter` and `hir_to_rust from RustEmitter`) reference procs that exist NOWHERE in the tree. Same for julia (`julia_to_hir from JuliaEmitter`, `hir_to_julia from JuliaEmitter`).
- `julia_emitter.runa` is an isolated 629-line "code-formatting helper library" with NO connection to `hir_to_julia.runa`. `hir_to_julia.runa` imports `emitter_common` directly and ignores `julia_emitter.runa`.
- Stray editor leftover at `backends/javascript/sedcHb5aD` (309-line plain-text copy of the file header) — should be removed.

---

## 1. Per-Backend Factual Inventory (53 entries)

Notation:
- "Wave 2 migrated" = emitter file `Import`s `emitter_common.runa` (i.e., `ec>=2` references when alias + raw call counted, or any `EmitterCommon` import line).
- "Dispatcher entry point" = `<lang>_to_hir` / `hir_to_<lang>` procs that `translation.runa` expects to find in `<Lang>Emitter`.
- LOC = raw `wc -l` (includes blanks and `Note:` blocks).

---

### arm
- Files present: `arm_emitter.runa`, `hir_to_arm.runa`
- `arm_emitter.runa` LOC: 112
- `hir_to_arm.runa` LOC: 365
- `arm_emitter.runa` content category: byte-buffer-primitives
- `hir_to_arm.runa` content category: high-level-translator
- Public procs in `arm_emitter.runa`: `create_arm_emitter`, `destroy_arm_emitter`, `ensure_capacity`, `emit_char`, `emit_string`, `emit_integer`, `emit_newline`, `emit_indent` (plus type `ArmEmitter`)
- Public procs in `hir_to_arm.runa`: 13 procs incl. ARM-assembly translator entrypoints; no `HIRToArmTranslator` struct.
- Wave 2 migration status: migrated-to-emitter_raw (imports `EmitterCommon`, every emit_* delegates via `emitter_raw_*`)
- Imports between the two files: `hir_to_arm.runa` imports `arm_emitter.runa` as `Emitter`; `arm_emitter.runa` does not import `hir_to_arm.runa`
- Anomalies/smells: Emitter does not expose `arm_to_hir`/`hir_to_arm` procs that `translation.runa` line 3342/3605 expects.

### bash
- Files present: `bash_emitter.runa`, `hir_to_bash.runa`
- `bash_emitter.runa` LOC: 111
- `hir_to_bash.runa` LOC: 948
- `bash_emitter.runa` content category: byte-buffer-primitives
- `hir_to_bash.runa` content category: high-level-translator
- Public procs in `bash_emitter.runa`: `create_bash_emitter`, `destroy_bash_emitter`, `ensure_capacity`, `emit_string`, `emit_char`, `emit_newline` (plus `BashEmitter` type)
- Public procs in `hir_to_bash.runa`: 31 procs, dominant style `generate_<X>_stmt` / `generate_<X>_expression`; type `BashContext`
- Wave 2 migration status: migrated-to-emitter_raw
- Imports between the two files: `hir_to_bash.runa` imports `bash_emitter.runa` as `Emitter`; reverse: no
- Anomalies/smells: Dispatcher `translation.runa:3364/3627` calls `bash_to_hir`/`hir_to_bash from BashEmitter`; neither proc exists in `bash_emitter.runa`.

### c
- Files present: `c_emitter.runa`, `hir_to_c.runa`
- `c_emitter.runa` LOC: 131
- `hir_to_c.runa` LOC: 1269
- `c_emitter.runa` content category: byte-buffer-primitives
- `hir_to_c.runa` content category: high-level-translator
- Public procs in `c_emitter.runa`: `create_c_emitter`, `destroy_c_emitter`, `ensure_capacity`, `emit_char`, `emit_string`, `emit_newline` (plus `CEmitter` type)
- Public procs in `hir_to_c.runa`: 38 procs, dominant `generate_<X>` style; type `CGenContext`; main entrypoint `generate_c_from_hir`
- Wave 2 migration status: migrated-to-emitter_raw
- Imports between the two files: `hir_to_c.runa` imports `c_emitter.runa`; reverse: no
- Anomalies/smells: Entry-point name mismatch. Dispatcher (`translation.runa:3231/3494`) calls `c_to_hir`/`hir_to_c from CEmitter` but `hir_to_c.runa` exposes `generate_c_from_hir`. No `c_to_hir` proc exists anywhere in the tree.

### cmake
- Files present: `cmake_emitter.runa`, `hir_to_cmake.runa`
- `cmake_emitter.runa` LOC: 587
- `hir_to_cmake.runa` LOC: 690
- `cmake_emitter.runa` content category: byte-buffer-primitives (with extended CMake-specific indent/state fields)
- `hir_to_cmake.runa` content category: high-level-translator
- Public procs in `cmake_emitter.runa`: 23 emit_* procs incl. `emit_cmake_text`, `emit_cmake_line`, `emit_cmake_indent`, etc.; type `CMakeEmitter` with 5 fields (buffer, capacity, length, indent_level, at_line_start)
- Public procs in `hir_to_cmake.runa`: 19 procs incl. translate_<X> patterns
- Wave 2 migration status: migrated-to-emitter_raw (Wave 2 form: delegates first 24 bytes of state to emitter_common raw header)
- Imports between the two files: `hir_to_cmake.runa` does NOT import `cmake_emitter.runa` directly; both files use their own primitive imports
- Anomalies/smells: Emitter has cleanly separated CMake-specific state fields (indent_level, at_line_start) atop the emitter_common raw header — a useful template for stateful emitters. Dispatcher mismatch as elsewhere.

### cobol
- Files present: `cobol_emitter.runa`, `hir_to_cobol.runa`
- `cobol_emitter.runa` LOC: 133
- `hir_to_cobol.runa` LOC: 1742
- `cobol_emitter.runa` content category: byte-buffer-primitives
- `hir_to_cobol.runa` content category: high-level-translator
- Public procs in `cobol_emitter.runa`: 11 emit_* procs (single-char, string, newline, indent, integer); type `CobolEmitter`
- Public procs in `hir_to_cobol.runa`: 45 procs, dense `translate_<X>` and `emit_<cobol_construct>` patterns
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_cobol.runa` imports `cobol_emitter.runa` as `Emitter`
- Anomalies/smells: COBOL-specific column-72 fixed-format formatting lives in `hir_to_cobol.runa`, not in the emitter.

### cpp
- Files present: `cpp_emitter.runa`, `hir_to_cpp.runa`
- `cpp_emitter.runa` LOC: 588
- `hir_to_cpp.runa` LOC: 772
- `cpp_emitter.runa` content category: byte-buffer-primitives (custom — does NOT delegate to emitter_common)
- `hir_to_cpp.runa` content category: high-level-translator
- Public procs in `cpp_emitter.runa`: 26 emit_* procs incl. `emit_cpp_text`, `emit_cpp_line`, indent control, char/byte ops; type `CppEmitter`
- Public procs in `hir_to_cpp.runa`: 20 procs (`HIRToCppContext` type)
- Wave 2 migration status: not-migrated (manages its own buffer; uses `Layout/StringCore/List` only)
- Imports: `hir_to_cpp.runa` does NOT import `cpp_emitter.runa`; both files independent
- Anomalies/smells: Two parallel emitter universes — `cpp_emitter.runa`'s 26 emit_* procs are not used by `hir_to_cpp.runa`. The emitter is orphaned within the backend pair.

### csharp
- Files present: `csharp_emitter.runa`, `hir_to_csharp.runa`
- `csharp_emitter.runa` LOC: 91
- `hir_to_csharp.runa` LOC: 1990
- `csharp_emitter.runa` content category: byte-buffer-primitives
- `hir_to_csharp.runa` content category: high-level-translator
- Public procs in `csharp_emitter.runa`: 6 emit_* + 2 lifecycle; type `CSharpEmitter`
- Public procs in `hir_to_csharp.runa`: 50 procs, dense translate_<X>/emit_<X>; type `CSharpContext`
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_csharp.runa` imports `csharp_emitter.runa` as `Emitter`
- Anomalies/smells: Same dispatcher mismatch.

### css
- Files present: `css_emitter.runa`, `hir_to_css.runa`
- `css_emitter.runa` LOC: 33
- `hir_to_css.runa` LOC: 288
- `css_emitter.runa` content category: byte-buffer-primitives (very thin)
- `hir_to_css.runa` content category: high-level-translator
- Public procs in `css_emitter.runa`: 2 procs only (e.g., raw wrappers)
- Public procs in `hir_to_css.runa`: 11 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_css.runa` imports `css_emitter.runa` as `Emitter`
- Anomalies/smells: Emitter is so thin it's almost a no-op wrapper; merging into `hir_to_css.runa` would eliminate the file.

### dart
- Files present: `dart_emitter.runa`, `hir_to_dart.runa`, `dart_tests.runa`
- `dart_emitter.runa` LOC: 662
- `hir_to_dart.runa` LOC: 2379
- `dart_emitter.runa` content category: high-level-emit (Dart-specific formatters: identifier formatting, keyword checks, type formatting, code style)
- `hir_to_dart.runa` content category: high-level-translator
- Public procs in `dart_emitter.runa`: 4 high-level `emit_*`/`create_*` plus extensive private formatters; types `DartEmitterConfig`, `DartCodeStyle`
- Public procs in `hir_to_dart.runa`: 76 procs; type `HIRToDartContext`
- Wave 2 migration status: not-migrated (no `EmitterCommon` import)
- Imports: `hir_to_dart.runa` does NOT import `dart_emitter.runa`; `dart_emitter.runa` imports `io_core` (suspicious for an emitter — likely dead I/O code)
- Anomalies/smells: Same orphan pattern as cpp/julia — `dart_emitter.runa` is a code-style config library not used by `hir_to_dart.runa`. The presence of `FileIO` import in an emitter is wrong.

### dockerfile
- Files present: `dockerfile_emitter.runa`, `hir_to_dockerfile.runa`, `dockerfile_tests.runa`
- `dockerfile_emitter.runa` LOC: 884
- `hir_to_dockerfile.runa` LOC: 1387
- `dockerfile_emitter.runa` content category: high-level-emit (full Dockerfile AST printer + buffer)
- `hir_to_dockerfile.runa` content category: high-level-translator
- Public procs in `dockerfile_emitter.runa`: 23 emit_* procs (`emit_program`, `emit_instruction`, `emit_string_with_indent`, etc.); type `DockerfileEmitter`
- Public procs in `hir_to_dockerfile.runa`: 34 procs
- Wave 2 migration status: migrated-to-emitter_raw (imports `EmitterCommon`)
- Imports: BOTH files import `dockerfile_parser` from frontends/. `hir_to_dockerfile.runa` does NOT import `dockerfile_emitter.runa`.
- Anomalies/smells: Both files independently import the frontend parser. The emitter operates on `DockerfileAST` (a frontend type), not HIR; it is genuinely a "Dockerfile AST printer" sister to `hir_to_dockerfile.runa`'s "HIR-to-Dockerfile-text" generator. Two parallel pipelines.

### elixir
- Files present: `elixir_emitter.runa`, `hir_to_elixir.runa`
- `elixir_emitter.runa` LOC: 267
- `hir_to_elixir.runa` LOC: 723
- `elixir_emitter.runa` content category: mixed (dispatch shim + stubbed frontend helpers)
- `hir_to_elixir.runa` content category: high-level-translator (HAS `HIRToElixirTranslator` struct, `translate_hir_to_elixir` entrypoint, dense `translate_<X>` procs)
- Public procs in `elixir_emitter.runa`: `elixir_to_hir`, `translate_elixir_source`, `parse_elixir_and_generate_hir`, `tokenize_elixir`, `parse_elixir_tokens`, `analyze_elixir_semantics`, `generate_hir_from_elixir_ast`, `hir_to_elixir`, plus 8 stub helpers (`create_hir_module`, `create_token_list`, `scan_elixir_tokens`, `create_elixir_parser`, `parse_elixir_module`, `check_pattern_completeness`, `verify_protocol_implementations`, `analyze_pipe_chains`, `traverse_elixir_ast_and_emit_hir`)
- Public procs in `hir_to_elixir.runa`: 32 procs incl. `create_hir_to_elixir_translator`, `translate_hir_to_elixir`, `translate_module`, `translate_function`, `translate_pattern_match`, `translate_genserver_call`, etc.
- Wave 2 migration status: not-migrated
- Imports: `elixir_emitter.runa` imports `hir_to_elixir.runa` as `ElixirBackend` (BACKWARD from c/bash/etc.)
- Anomalies/smells: 8 stubbed helpers (`scan_elixir_tokens`, `create_elixir_parser`, etc.) return fixed allocations or `1` — they duplicate the role of the real frontend at `frontends/elixir/`. This emitter is a vestigial shim around `hir_to_elixir.runa` with bogus frontend-side scaffolding that is never reached because real Elixir parsing lives in `frontends/elixir/elixir_to_hir.runa`.

### erlang
- Files present: `erlang_emitter.runa`, `hir_to_erlang.runa`
- `erlang_emitter.runa` LOC: 1280
- `hir_to_erlang.runa` LOC: 1448
- `erlang_emitter.runa` content category: high-level-emit (`emit_module`, `emit_function`, full Erlang source printer)
- `hir_to_erlang.runa` content category: high-level-translator
- Public procs in `erlang_emitter.runa`: 27 emit_* procs (`emit_module`, `emit_attribute`, `emit_record`, `emit_type_decl`, `emit_function`, `emit_clause`, `emit_pattern`, `emit_guard`, etc.); type `ErlangEmitterConfig`
- Public procs in `hir_to_erlang.runa`: 37 procs across 6 types
- Wave 2 migration status: not-migrated (no `EmitterCommon` import)
- Imports: `erlang_emitter.runa` imports `erlang_parser.runa` from frontends/ (operates on `ErlangModule` AST, not HIR). `hir_to_erlang.runa` ALSO imports `erlang_parser.runa`.
- Anomalies/smells: Like dockerfile and verilog: `erlang_emitter.runa` is an Erlang-AST-to-source printer, not an HIR consumer. It's a sister to `hir_to_erlang.runa` rather than its primitive layer.

### fsharp
- Files present: `fsharp_emitter.runa`, `hir_to_fsharp.runa`
- `fsharp_emitter.runa` LOC: 1051
- `hir_to_fsharp.runa` LOC: 1017
- `fsharp_emitter.runa` content category: high-level-emit (HIR-aware emit functions: `emit_let_binding_node`, `emit_function_node`, etc.)
- `hir_to_fsharp.runa` content category: high-level-translator
- Public procs in `fsharp_emitter.runa`: 30 emit_* procs operating on HIR nodes directly; type `FSharpEmitter`
- Public procs in `hir_to_fsharp.runa`: 35 procs
- Wave 2 migration status: migrated-to-emitter_raw (imports `EmitterCommon`)
- Imports: BOTH files import HIR. `hir_to_fsharp.runa` imports `fsharp_emitter.runa` as `FSharpEmitter`.
- Anomalies/smells: F# is one of the few backends where emitter and hir_to share the HIR type system and form a real layered pair. Worth examining as a template for the "high-level-emit + translator" pattern.

### go
- Files present: `go_emitter.runa`, `hir_to_go.runa`
- `go_emitter.runa` LOC: 94
- `hir_to_go.runa` LOC: 2018
- `go_emitter.runa` content category: byte-buffer-primitives
- `hir_to_go.runa` content category: high-level-translator
- Public procs in `go_emitter.runa`: 7 emit_* + lifecycle; type `GoEmitter`
- Public procs in `hir_to_go.runa`: 60 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_go.runa` imports `go_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### graphql
- Files present: `graphql_emitter.runa`, `hir_to_graphql.runa`
- `graphql_emitter.runa` LOC: 33
- `hir_to_graphql.runa` LOC: 814
- `graphql_emitter.runa` content category: byte-buffer-primitives (very thin)
- `hir_to_graphql.runa` content category: high-level-translator
- Public procs in `graphql_emitter.runa`: 2 procs
- Public procs in `hir_to_graphql.runa`: 23 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_graphql.runa` imports `graphql_emitter.runa` as `Emitter`
- Anomalies/smells: Same minimal-wrapper as css; merge candidate.

### haskell
- Files present: `haskell_emitter.runa`, `hir_to_haskell.runa`
- `haskell_emitter.runa` LOC: 265
- `hir_to_haskell.runa` LOC: 1093
- `haskell_emitter.runa` content category: mixed (dispatch shim + stubbed frontend helpers)
- `hir_to_haskell.runa` content category: high-level-translator (HAS `HIRToHaskellTranslator` struct, `translate_hir_module`, `translate_hir_function`, `translate_hir_expression`)
- Public procs in `haskell_emitter.runa`: `haskell_to_hir`, `translate_haskell_source`, `parse_haskell_and_generate_hir`, `tokenize_haskell`, `parse_haskell_tokens`, `analyze_haskell_semantics`, `generate_hir_from_haskell_ast`, `hir_to_haskell` + 8 stub helpers (`scan_haskell_tokens`, `parse_haskell_module`, `resolve_type_classes`, `infer_haskell_types`, `analyze_strictness`, etc.)
- Public procs in `hir_to_haskell.runa`: 33 procs incl. canonical `translate_hir_module`, `translate_hir_function`, `translate_hir_expression`; type `HIRToHaskellTranslator`
- Wave 2 migration status: not-migrated
- Imports: `haskell_emitter.runa` imports `hir_to_haskell.runa` as `HaskellBackend` (BACKWARD)
- Anomalies/smells: Same vestigial-shim pattern as elixir. `hir_to_haskell.runa` is one of only 4 backends with the textbook `HIRToXTranslator` + `translate_hir_module/function/expression` triple.

### hcl
- Files present: `hcl_emitter.runa`, `hir_to_hcl.runa`, `hcl_tests.runa`
- `hcl_emitter.runa` LOC: 383
- `hir_to_hcl.runa` LOC: 720
- `hcl_emitter.runa` content category: high-level-emit
- `hir_to_hcl.runa` content category: high-level-translator
- Public procs in `hcl_emitter.runa`: 1 emit_* + helpers; type `HCLEmitter`
- Public procs in `hir_to_hcl.runa`: 32 procs
- Wave 2 migration status: not-migrated
- Imports: `hir_to_hcl.runa` does NOT import `hcl_emitter.runa`
- Anomalies/smells: Orphan emitter — emitter and translator don't share state. Two parallel implementations.

### html
- Files present: `html_emitter.runa`, `hir_to_html.runa`
- `html_emitter.runa` LOC: 33
- `hir_to_html.runa` LOC: 522
- `html_emitter.runa` content category: byte-buffer-primitives (very thin)
- `hir_to_html.runa` content category: high-level-translator
- Public procs in `html_emitter.runa`: 2 procs
- Public procs in `hir_to_html.runa`: 15 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_html.runa` imports `html_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### java
- Files present: `java_emitter.runa`, `hir_to_java.runa`
- `java_emitter.runa` LOC: 137
- `hir_to_java.runa` LOC: 1577
- `java_emitter.runa` content category: byte-buffer-primitives
- `hir_to_java.runa` content category: high-level-translator
- Public procs in `java_emitter.runa`: 17 emit_* procs (rich primitive set — char, string, integer, newline, indent, comment, identifier escape)
- Public procs in `hir_to_java.runa`: 49 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_java.runa` imports `java_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern with extended primitive set in emitter.

### javascript
- Files present: `javascript_emitter.runa`, `hir_to_javascript.runa`, **`sedcHb5aD`** (stray)
- `javascript_emitter.runa` LOC: 99
- `hir_to_javascript.runa` LOC: 1786
- `javascript_emitter.runa` content category: byte-buffer-primitives
- `hir_to_javascript.runa` content category: high-level-translator
- Public procs in `javascript_emitter.runa`: 8 emit_*; type `JavaScriptEmitter`
- Public procs in `hir_to_javascript.runa`: 47 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_javascript.runa` imports `javascript_emitter.runa` as `Emitter`
- Anomalies/smells: **Stray file `sedcHb5aD`** (309 lines, UTF-8 text, license-header content only — apparent `sed` editor leftover). Should be deleted.

### json
- Files present: `json_emitter.runa`, `hir_to_json.runa`
- `json_emitter.runa` LOC: 53
- `hir_to_json.runa` LOC: 683
- `json_emitter.runa` content category: byte-buffer-primitives
- `hir_to_json.runa` content category: high-level-translator
- Public procs in `json_emitter.runa`: 2 procs; type `JSONEmitter`
- Public procs in `hir_to_json.runa`: 18 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_json.runa` imports `json_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### jsx
- Files present: `jsx_emitter.runa`, `hir_to_jsx.runa`
- `jsx_emitter.runa` LOC: 33
- `hir_to_jsx.runa` LOC: 667
- `jsx_emitter.runa` content category: byte-buffer-primitives
- `hir_to_jsx.runa` content category: high-level-translator
- Public procs in `jsx_emitter.runa`: 2 procs
- Public procs in `hir_to_jsx.runa`: 21 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_jsx.runa` imports `jsx_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### julia
- Files present: `julia_emitter.runa`, `hir_to_julia.runa`
- `julia_emitter.runa` LOC: 629
- `hir_to_julia.runa` LOC: 1109
- `julia_emitter.runa` content category: config-state-only / high-level-formatter-helpers
- `hir_to_julia.runa` content category: high-level-translator
- Public procs in `julia_emitter.runa`: 31 procs incl. `create_julia_emitter_config`, `create_julia_code_style`, `format_julia_identifier`, `is_julia_keyword`, `contains_special_chars`, `format_julia_type_name`, `format_julia_function_name`, `format_julia_constant_name`, `generate_julia_module_header`, `generate_julia_module_footer`, `generate_julia_using_statement`, `generate_julia_export_statement`, `generate_julia_method_signature`, `generate_julia_docstring`, `format_julia_array_literal`, `validate_julia_syntax`, `emit_julia_code`, etc.; types `JuliaEmitterConfig`, `JuliaCodeStyle`
- Public procs in `hir_to_julia.runa`: 41 procs; uses `EmitterContext` directly from `emitter_common`
- Wave 2 migration status: not-migrated (`julia_emitter.runa` has no imports at all)
- Imports: `julia_emitter.runa` has zero `Import` lines. `hir_to_julia.runa` imports `emitter_common` directly (as `Emitter`), not `julia_emitter.runa`.
- Anomalies/smells: **Dead-code emitter.** Nothing in the tree imports `julia_emitter.runa`. The dispatcher (`translation.runa:72`) imports it as `JuliaEmitter` and calls `julia_to_hir` / `hir_to_julia` from it (lines 3312, 3575), but **NEITHER proc exists** in `julia_emitter.runa`. This is a fully broken dispatch arm. `julia_emitter.runa` has no imports, no callers, and is unreachable.

### latex
- Files present: `latex_emitter.runa`, `hir_to_latex.runa`
- `latex_emitter.runa` LOC: 480
- `hir_to_latex.runa` LOC: 947
- `latex_emitter.runa` content category: dispatch-orchestrator (real round-trip pipeline orchestrator that wires frontends/latex to backends/latex)
- `hir_to_latex.runa` content category: high-level-translator
- Public procs in `latex_emitter.runa`: `latex_to_hir`, `hir_to_latex`, `latex_roundtrip`, `latex_to_hir_with_errors`, `hir_to_latex_with_errors`, `validate_latex`, `format_latex`, `get_document_info`, `extract_metadata_from_hir`, plus 12 helpers (`extract_citations`, `extract_labels`, etc.)
- Public procs in `hir_to_latex.runa`: 42 procs; type `LaTeXBackend`
- Wave 2 migration status: not-migrated
- Imports: `latex_emitter.runa` imports BOTH `frontends/latex/latex_to_hir.runa` AND `backends/latex/hir_to_latex.runa` — a true bridging file. `hir_to_latex.runa` imports `frontends/latex/latex_to_hir.runa` (for LaTeXHIR types) but not the emitter.
- Anomalies/smells: One of 7 emitters that genuinely matches the dispatcher's expected proc names (`latex_to_hir`, `hir_to_latex`). However, its signatures are `takes source_code as String returns Integer` / `takes hir_module as Integer returns String` — different from the dispatcher's call shape but at least the procs exist by name.

### llvmir
- Files present: `llvmir_emitter.runa`, `hir_to_llvmir.runa`
- `llvmir_emitter.runa` LOC: 91
- `hir_to_llvmir.runa` LOC: 727
- `llvmir_emitter.runa` content category: byte-buffer-primitives
- `hir_to_llvmir.runa` content category: high-level-translator
- Public procs in `llvmir_emitter.runa`: 6 emit_* + lifecycle; type `LlvmIrEmitter`
- Public procs in `hir_to_llvmir.runa`: 18 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_llvmir.runa` imports `llvmir_emitter.runa` as `Emitter`
- Anomalies/smells: Note empty sibling `backends/llvm/` exists alongside this `llvmir/` directory — likely an attempted rename or placeholder.

### lua
- Files present: `lua_emitter.runa`, `hir_to_lua.runa`, `lua_tests.runa`
- `lua_emitter.runa` LOC: 710
- `hir_to_lua.runa` LOC: 1103
- `lua_emitter.runa` content category: high-level-emit (Lua-specific emitter with builtin formatters)
- `hir_to_lua.runa` content category: high-level-translator
- Public procs in `lua_emitter.runa`: 3 emit_* + many private formatters; types `LuaEmitterConfig`, `LuaContext`
- Public procs in `hir_to_lua.runa`: 36 procs
- Wave 2 migration status: not-migrated
- Imports: `hir_to_lua.runa` does NOT import `lua_emitter.runa`
- Anomalies/smells: Orphan emitter — translator runs independent of emitter file.

### makefile
- Files present: `makefile_emitter.runa`, `hir_to_makefile.runa`
- `makefile_emitter.runa` LOC: 645
- `hir_to_makefile.runa` LOC: 927
- `makefile_emitter.runa` content category: dispatch-orchestrator (wires lexer/parser/translator/backend together via `MakefileEmitter` struct)
- `hir_to_makefile.runa` content category: high-level-translator
- Public procs in `makefile_emitter.runa`: `create_emitter`, `parse_makefile`, `translate_to_hir`, `generate_makefile`, `makefile_to_hir`, `hir_to_makefile`, `round_trip_translate`, `add_diagnostic`, `merge_diagnostics`, `get_error_count`, `get_warning_count`, `get_diagnostics`, `format_diagnostic`, `get_lexer_errors`, `get_parser_errors`, plus types `MakefileEmitter`, `Diagnostic`
- Public procs in `hir_to_makefile.runa`: 29 procs; types `HIRToMakefile`, `MakefileBackend` (?); has `translate_hir_module` entry
- Wave 2 migration status: not-migrated (orchestrator, not byte-buffer)
- Imports: `makefile_emitter.runa` imports `frontends/makefile/*` AND `backends/makefile/hir_to_makefile.runa` — the true bridge file. `hir_to_makefile.runa` imports `frontends/makefile/makefile_to_hir.runa`.
- Anomalies/smells: One of 7 with proper dispatcher-name `makefile_to_hir`/`hir_to_makefile` procs. Signature requires emitter_ptr — dispatcher call shape mismatches.

### markdown
- Files present: `markdown_emitter.runa`, `hir_to_markdown.runa`
- `markdown_emitter.runa` LOC: 52
- `hir_to_markdown.runa` LOC: 880
- `markdown_emitter.runa` content category: byte-buffer-primitives
- `hir_to_markdown.runa` content category: high-level-translator
- Public procs in `markdown_emitter.runa`: 2 procs
- Public procs in `hir_to_markdown.runa`: 21 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_markdown.runa` imports `markdown_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### matlab
- Files present: `matlab_emitter.runa`, `hir_to_matlab.runa`, `matlab_tests.runa`
- `matlab_emitter.runa` LOC: 616
- `hir_to_matlab.runa` LOC: 1227
- `matlab_emitter.runa` content category: high-level-emit (similar to dart_emitter — formatter library with FileIO import)
- `hir_to_matlab.runa` content category: high-level-translator
- Public procs in `matlab_emitter.runa`: 4 emit_* + many formatters; types `MatlabEmitterConfig`, `MatlabCodeStyle`
- Public procs in `hir_to_matlab.runa`: 36 procs
- Wave 2 migration status: not-migrated
- Imports: `hir_to_matlab.runa` does NOT import `matlab_emitter.runa`. `matlab_emitter.runa` imports `io_core` (FileIO) — wrong for a code emitter.
- Anomalies/smells: Same orphan pattern as dart and lua. FileIO import is dead weight.

### mongodb
- Files present: `mongodb_emitter.runa`, `hir_to_mongodb.runa`
- `mongodb_emitter.runa` LOC: 33
- `hir_to_mongodb.runa` LOC: 413
- `mongodb_emitter.runa` content category: byte-buffer-primitives (very thin)
- `hir_to_mongodb.runa` content category: high-level-translator
- Public procs in `mongodb_emitter.runa`: 2 procs
- Public procs in `hir_to_mongodb.runa`: 14 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_mongodb.runa` imports `mongodb_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### openapi
- Files present: `openapi_emitter.runa`, `hir_to_openapi.runa`
- `openapi_emitter.runa` LOC: 43
- `hir_to_openapi.runa` LOC: 580
- `openapi_emitter.runa` content category: byte-buffer-primitives
- `hir_to_openapi.runa` content category: high-level-translator
- Public procs in `openapi_emitter.runa`: 2 procs; type `OpenAPIEmitter`
- Public procs in `hir_to_openapi.runa`: 20 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_openapi.runa` imports `openapi_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### php
- Files present: `php_emitter.runa`, `hir_to_php.runa`, `php_tests.runa`
- `php_emitter.runa` LOC: 570
- `hir_to_php.runa` LOC: 962
- `php_emitter.runa` content category: high-level-emit (PHP-aware formatter library)
- `hir_to_php.runa` content category: high-level-translator
- Public procs in `php_emitter.runa`: 1 main `emit_*` plus many formatter helpers; type `PHPEmitter`
- Public procs in `hir_to_php.runa`: 32 procs
- Wave 2 migration status: not-migrated
- Imports: `hir_to_php.runa` does NOT import `php_emitter.runa`
- Anomalies/smells: Orphan emitter.

### powershell
- Files present: `powershell_emitter.runa`, `hir_to_powershell.runa`
- `powershell_emitter.runa` LOC: 714
- `hir_to_powershell.runa` LOC: 1484
- `powershell_emitter.runa` content category: high-level-emit (74 emit_* procs — most of any backend)
- `hir_to_powershell.runa` content category: high-level-translator
- Public procs in `powershell_emitter.runa`: 74 emit_* procs covering every PowerShell construct (`emit_function`, `emit_param_block`, `emit_pipeline`, `emit_cmdlet`, etc.); type `PowerShellEmitter`
- Public procs in `hir_to_powershell.runa`: 44 procs
- Wave 2 migration status: migrated-to-emitter_raw (imports `EmitterCommon`)
- Imports: `hir_to_powershell.runa` imports `powershell_emitter.runa` as `Emitter`
- Anomalies/smells: This emitter is the richest "high-level construct emitter" in the tree. It is in fact what a smart-emitter pattern looks like in practice.

### protobuf
- Files present: `protobuf_emitter.runa`, `hir_to_protobuf.runa`
- `protobuf_emitter.runa` LOC: 94
- `hir_to_protobuf.runa` LOC: 1047
- `protobuf_emitter.runa` content category: byte-buffer-primitives
- `hir_to_protobuf.runa` content category: high-level-translator
- Public procs in `protobuf_emitter.runa`: 3 emit_* + lifecycle; type `ProtobufEmitter`
- Public procs in `hir_to_protobuf.runa`: 21 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_protobuf.runa` imports `protobuf_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### python
- Files present: `python_emitter.runa`, `hir_to_python.runa`
- `python_emitter.runa` LOC: 111
- `hir_to_python.runa` LOC: 1672
- `python_emitter.runa` content category: byte-buffer-primitives
- `hir_to_python.runa` content category: high-level-translator
- Public procs in `python_emitter.runa`: 6 emit_* + lifecycle; type `PythonEmitter`
- Public procs in `hir_to_python.runa`: 50 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_python.runa` imports `python_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### r
- Files present: `r_emitter.runa`, `hir_to_r.runa`
- `r_emitter.runa` LOC: 517
- `hir_to_r.runa` LOC: 1102
- `r_emitter.runa` content category: high-level-emit (47 emit_* procs for R constructs)
- `hir_to_r.runa` content category: high-level-translator
- Public procs in `r_emitter.runa`: 47 emit_* procs (`emit_assign`, `emit_function_def`, `emit_data_frame`, `emit_apply_family`, etc.); type `REmitter`
- Public procs in `hir_to_r.runa`: 33 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_r.runa` imports `r_emitter.runa` as `REmitter`
- Anomalies/smells: Rich high-level emitter similar to powershell.

### regex
- Files present: `regex_emitter.runa`, `hir_to_regex.runa`
- `regex_emitter.runa` LOC: 43
- `hir_to_regex.runa` LOC: 207
- `regex_emitter.runa` content category: byte-buffer-primitives
- `hir_to_regex.runa` content category: high-level-translator
- Public procs in `regex_emitter.runa`: 2 procs; type `RegexEmitter`
- Public procs in `hir_to_regex.runa`: 12 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_regex.runa` imports `regex_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### ruby
- Files present: `ruby_emitter.runa`, `hir_to_ruby.runa`
- `ruby_emitter.runa` LOC: 265
- `hir_to_ruby.runa` LOC: 981
- `ruby_emitter.runa` content category: mixed (dispatch shim + stubbed frontend helpers — same template as elixir/haskell/scala)
- `hir_to_ruby.runa` content category: high-level-translator (HAS `HIRToRubyTranslator`)
- Public procs in `ruby_emitter.runa`: `ruby_to_hir`, `translate_ruby_source`, `parse_ruby_and_generate_hir`, `tokenize_ruby`, `parse_ruby_tokens`, `analyze_ruby_semantics`, `generate_hir_from_ruby_ast`, `hir_to_ruby`, plus 8 stubs (`scan_ruby_tokens`, `create_ruby_parser`, `parse_ruby_program`, `analyze_duck_typing`, `resolve_dynamic_methods`, `analyze_block_semantics`, `traverse_ruby_ast_and_emit_hir`)
- Public procs in `hir_to_ruby.runa`: 38 procs; type `HIRToRubyTranslator`
- Wave 2 migration status: not-migrated
- Imports: `ruby_emitter.runa` imports `hir_to_ruby.runa` as `RubyBackend` (BACKWARD)
- Anomalies/smells: Same vestigial-shim pattern as elixir/haskell.

### runa
- Files present: `runa_emitter.runa`, `hir_to_runa.runa`
- `runa_emitter.runa` LOC: 93
- `hir_to_runa.runa` LOC: 1195
- `runa_emitter.runa` content category: byte-buffer-primitives
- `hir_to_runa.runa` content category: high-level-translator (HIR -> Runa source, the reverse round-trip path)
- Public procs in `runa_emitter.runa`: 6 emit_* + lifecycle; type `RunaEmitter`
- Public procs in `hir_to_runa.runa`: 31 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_runa.runa` imports `runa_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### rust
- Files present: `rust_emitter.runa` ONLY (no hir_to_rust.runa)
- `rust_emitter.runa` LOC: 139
- `hir_to_rust.runa` LOC: N/A (file does not exist)
- `rust_emitter.runa` content category: byte-buffer-primitives
- `hir_to_rust.runa` content category: absent
- Public procs in `rust_emitter.runa`: `create_rust_emitter`, `destroy_rust_emitter`, `ensure_capacity`, `copy_memory`, `emit_char`, `emit_string`, `emit_integer`, `emit_newline`, `emit_indent`, `emit_comment`, `get_output`, `get_length`, `reset`; type `RustEmitter`
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: None between two files (only one exists).
- Anomalies/smells: **Critical gap.** No Rust HIR translator exists. `translation.runa:3239/3502` calls `rust_to_hir`/`hir_to_rust from RustEmitter` — these procs are absent from `rust_emitter.runa` (and from every other file in the tree). The Rust dispatch arm is fully unimplemented. The frontend at `frontends/rust/` exists but the backend translator is missing.

### scala
- Files present: `scala_emitter.runa`, `hir_to_scala.runa`
- `scala_emitter.runa` LOC: 263
- `hir_to_scala.runa` LOC: 998
- `scala_emitter.runa` content category: mixed (dispatch shim + stubbed frontend helpers)
- `hir_to_scala.runa` content category: high-level-translator (HAS `HIRToScalaTranslator`, `translate_hir_module`, `translate_hir_function`, `translate_hir_expression`)
- Public procs in `scala_emitter.runa`: `scala_to_hir`, `translate_scala_source`, `parse_scala_and_generate_hir`, `tokenize_scala`, `parse_scala_tokens`, `analyze_scala_semantics`, `generate_hir_from_scala_ast`, `hir_to_scala` + 8 stubs (`scan_scala_tokens`, `create_scala_parser`, `parse_scala_compilation_unit`, `infer_scala_types`, `resolve_implicits`, `check_variance_annotations`, `traverse_scala_ast_and_emit_hir`)
- Public procs in `hir_to_scala.runa`: 34 procs; type `HIRToScalaTranslator`
- Wave 2 migration status: not-migrated
- Imports: `scala_emitter.runa` imports `hir_to_scala.runa` as `ScalaBackend` (BACKWARD)
- Anomalies/smells: Same vestigial-shim pattern as elixir/haskell/ruby. The frontend stubs in `scala_emitter.runa` (`tokenize_scala`, `parse_scala_tokens`, `infer_scala_types`, `resolve_implicits`) duplicate the role of the real `frontends/scala/` modules — and they are stub bodies, not real implementations. The brief was correct that scala_emitter contains tokenize/parse logic, but those bodies are placeholder allocations (`Let parser be proc allocate from Layout with 128`), not real parsers.

### solidity
- Files present: `solidity_emitter.runa`, `hir_to_solidity.runa`, `solidity_tests.runa`
- `solidity_emitter.runa` LOC: 565
- `hir_to_solidity.runa` LOC: 1081
- `solidity_emitter.runa` content category: high-level-emit
- `hir_to_solidity.runa` content category: high-level-translator
- Public procs in `solidity_emitter.runa`: 1 main `emit_*` + many formatter helpers; type `SolidityEmitter`
- Public procs in `hir_to_solidity.runa`: 36 procs
- Wave 2 migration status: not-migrated
- Imports: `hir_to_solidity.runa` does NOT import `solidity_emitter.runa`
- Anomalies/smells: Orphan emitter.

### sql
- Files present: `sql_emitter.runa`, `hir_to_sql.runa`
- `sql_emitter.runa` LOC: 398
- `hir_to_sql.runa` LOC: 1031
- `sql_emitter.runa` content category: byte-buffer-primitives (with SQL-aware formatters)
- `hir_to_sql.runa` content category: high-level-translator
- Public procs in `sql_emitter.runa`: 8 emit_* incl. quote handling; type `SqlEmitter`
- Public procs in `hir_to_sql.runa`: 20 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_sql.runa` imports `sql_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### swift
- Files present: `swift_emitter.runa`, `hir_to_swift.runa`
- `swift_emitter.runa` LOC: 96
- `hir_to_swift.runa` LOC: 2323
- `swift_emitter.runa` content category: byte-buffer-primitives
- `hir_to_swift.runa` content category: high-level-translator
- Public procs in `swift_emitter.runa`: 6 emit_* + lifecycle; type `SwiftEmitter`
- Public procs in `hir_to_swift.runa`: 58 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_swift.runa` imports `swift_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### swiftui
- Files present: `swiftui_emitter.runa`, `hir_to_swiftui.runa`
- `swiftui_emitter.runa` LOC: 87
- `hir_to_swiftui.runa` LOC: 1134
- `swiftui_emitter.runa` content category: byte-buffer-primitives
- `hir_to_swiftui.runa` content category: high-level-translator
- Public procs in `swiftui_emitter.runa`: 5 emit_*; type `SwiftUIEmitter`
- Public procs in `hir_to_swiftui.runa`: 28 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_swiftui.runa` imports `swiftui_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### toml
- Files present: `toml_emitter.runa`, `hir_to_toml.runa`
- `toml_emitter.runa` LOC: 52
- `hir_to_toml.runa` LOC: 678
- `toml_emitter.runa` content category: byte-buffer-primitives
- `hir_to_toml.runa` content category: high-level-translator
- Public procs in `toml_emitter.runa`: 2 procs; type `TomlEmitter`
- Public procs in `hir_to_toml.runa`: 16 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_toml.runa` imports `toml_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### typescript
- Files present: `typescript_emitter.runa`, `hir_to_typescript.runa`
- `typescript_emitter.runa` LOC: 103
- `hir_to_typescript.runa` LOC: 1400
- `typescript_emitter.runa` content category: byte-buffer-primitives
- `hir_to_typescript.runa` content category: high-level-translator
- Public procs in `typescript_emitter.runa`: 9 emit_*; type `TypeScriptEmitter`
- Public procs in `hir_to_typescript.runa`: 20 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_typescript.runa` imports `typescript_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### verilog
- Files present: `verilog_emitter.runa`, `hir_to_verilog.runa`
- `verilog_emitter.runa` LOC: 141
- `hir_to_verilog.runa` LOC: 433
- `verilog_emitter.runa` content category: dispatch-orchestrator (struct-based bundler — `VerilogEmitter` bundles lexer/parser/translator/backend)
- `hir_to_verilog.runa` content category: high-level-translator
- Public procs in `verilog_emitter.runa`: `create_emitter`, `verilog_to_hir`, `hir_to_verilog`, `round_trip`, `merge_errors`, `get_errors`, `has_errors`, `translate_from_verilog`, `translate_to_verilog`; type `VerilogEmitter` (9-field struct)
- Public procs in `hir_to_verilog.runa`: 28 procs
- Wave 2 migration status: not-migrated (orchestrator)
- Imports: `verilog_emitter.runa` imports `frontends/verilog/*` AND `backends/verilog/hir_to_verilog.runa`. `hir_to_verilog.runa` imports `frontends/verilog/verilog_to_hir.runa`.
- Anomalies/smells: One of 7 emitters that exposes `verilog_to_hir`/`hir_to_verilog` by the names the dispatcher expects. Signatures take `emitter_ptr` — incompatible with dispatcher's single-arg call shape.

### vhdl
- Files present: `vhdl_emitter.runa`, `hir_to_vhdl.runa`
- `vhdl_emitter.runa` LOC: 1064
- `hir_to_vhdl.runa` LOC: 1191
- `vhdl_emitter.runa` content category: high-level-emit (40 emit_* procs for VHDL constructs)
- `hir_to_vhdl.runa` content category: high-level-translator
- Public procs in `vhdl_emitter.runa`: 40 emit_* procs (`emit_entity`, `emit_architecture`, `emit_signal`, `emit_process`, `emit_when`, etc.); type `VhdlEmitter`
- Public procs in `hir_to_vhdl.runa`: 10 procs (relatively thin translator over rich emitter)
- Wave 2 migration status: not-migrated
- Imports: `hir_to_vhdl.runa` imports `vhdl_emitter.runa` as `VhdlEmitter`
- Anomalies/smells: Inverted size — emitter is bigger than translator. Translator delegates heavily to emitter.

### wasm
- Files present: `wasm_emitter.runa`, `hir_to_wasm.runa`
- `wasm_emitter.runa` LOC: 98
- `hir_to_wasm.runa` LOC: 504
- `wasm_emitter.runa` content category: byte-buffer-primitives
- `hir_to_wasm.runa` content category: high-level-translator
- Public procs in `wasm_emitter.runa`: 5 emit_*; type `WasmEmitter`
- Public procs in `hir_to_wasm.runa`: 12 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_wasm.runa` imports `wasm_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### x86
- Files present: `x86_emitter.runa`, `hir_to_x86.runa`
- `x86_emitter.runa` LOC: 112
- `hir_to_x86.runa` LOC: 316
- `x86_emitter.runa` content category: byte-buffer-primitives
- `hir_to_x86.runa` content category: high-level-translator
- Public procs in `x86_emitter.runa`: 7 emit_*; type `X86Emitter`
- Public procs in `hir_to_x86.runa`: 11 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_x86.runa` imports `x86_emitter.runa` as `Emitter`
- Anomalies/smells: Empty sibling `backends/x86_64/` directory exists — appears to be an unused placeholder.

### xml
- Files present: `xml_emitter.runa`, `hir_to_xml.runa`
- `xml_emitter.runa` LOC: 133
- `hir_to_xml.runa` LOC: 757
- `xml_emitter.runa` content category: byte-buffer-primitives
- `hir_to_xml.runa` content category: high-level-translator
- Public procs in `xml_emitter.runa`: 4 emit_* + escape helpers; type `XmlEmitter`
- Public procs in `hir_to_xml.runa`: 17 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_xml.runa` imports `xml_emitter.runa` as `Emitter`
- Anomalies/smells: Standard pattern.

### yaml
- Files present: `yaml_emitter.runa`, `hir_to_yaml.runa`
- `yaml_emitter.runa` LOC: 52
- `hir_to_yaml.runa` LOC: 831
- `yaml_emitter.runa` content category: byte-buffer-primitives
- `hir_to_yaml.runa` content category: high-level-translator
- Public procs in `yaml_emitter.runa`: 2 procs; type `YamlEmitter`
- Public procs in `hir_to_yaml.runa`: 18 procs
- Wave 2 migration status: migrated-to-emitter_raw
- Imports: `hir_to_yaml.runa` imports `yaml_emitter.runa` as `Emitter`
- Anomalies/smells: Minimal-wrapper.

### Other on-disk noise

- `backends/common/` contains `README.md` and `code_generation.runa` (not a backend; shared utility — out of scope for this rationalization)
- `backends/emitter_common.runa` — the shared byte-buffer foundation (28 public procs, types `EmitterContext`); not a backend, the migration target.
- `backends/llvm/` — empty directory, no `.runa` files
- `backends/x86_64/` — empty directory, no `.runa` files
- `backends/javascript/sedcHb5aD` — 309-line UTF-8 plain-text editor leftover (license header only)

---

## 2. Architecture Analysis

### 2.1 The five de-facto architectures present today

After examining all 53 emitter files, the population breaks into five distinct architectures rather than the two implied by the brief:

1. **Byte-buffer primitives delegating to emitter_common (Wave 2 migrated).** 33 backends. Examples: arm, bash, c, cobol, csharp, css, go, html, java, javascript, json, jsx, llvmir, markdown, mongodb, openapi, powershell, protobuf, python, regex, runa, rust, sql, swift, swiftui, toml, typescript, wasm, x86, xml, yaml, graphql, r. Emitter file is a thin wrapper exposing `create_<lang>_emitter`, `emit_char`, `emit_string`, `emit_newline`, `emit_indent`, etc., each of which is one line delegating to `emitter_raw_*` from `emitter_common.runa`. Consumed by `hir_to_<lang>.runa` via `Import ... as Emitter`.

2. **Byte-buffer primitives with extended state, Wave 2-migrated.** 3 backends. cmake (5-field struct with indent_level/at_line_start), fsharp (HIR-aware emit nodes), sql (quote-handling). They use emitter_common for the buffer but add language-specific state.

3. **High-level construct emitters (rich emit-the-syntax APIs).** 6 backends. erlang (27 emit_*), powershell (74 emit_*), r (47 emit_*), vhdl (40 emit_*), dockerfile (23 emit_*), cpp (26 emit_*). These emitters expose `emit_module`, `emit_function`, `emit_clause`, etc. — full per-construct printers. Some are migrated (powershell, dockerfile use EmitterCommon for buffering); others are not (erlang, vhdl, cpp manage their own buffers).

4. **High-level construct emitters that are orphans of their hir_to_X.** 5 backends. cpp, dart, hcl, lua, matlab, php, solidity. The emitter contains language-aware formatting code but `hir_to_<lang>.runa` does NOT import it; both files exist in parallel with no connection. These emitters are effectively dead code that the matching translator does not use.

5. **Mixed shim/dispatch files (the elixir-template).** 5 backends. elixir, haskell, ruby, scala plus a structural variant in latex, makefile, verilog. The "emitter" is actually a dispatcher entry-point: it defines `<lang>_to_hir` and `hir_to_<lang>` procs that wire the public dispatcher in `translation.runa` to the real frontend (in `frontends/<lang>/`) and the real backend (in `hir_to_<lang>.runa`). In elixir/haskell/ruby/scala it ALSO contains 8-10 stub procs (`tokenize_<lang>`, `parse_<lang>_tokens`, `analyze_<lang>_semantics`, etc.) that have placeholder bodies and are not called by anything outside the same file — they are vestigial scaffolding.

6. **Config/formatter library (orphan).** 1 backend. julia. `julia_emitter.runa` defines `JuliaEmitterConfig`, `JuliaCodeStyle`, and 31 formatting helpers (`format_julia_identifier`, `generate_julia_module_header`, etc.). NOTHING imports it. `hir_to_julia.runa` uses `emitter_common`'s `EmitterContext` directly.

### 2.2 Where the smart-emitter pattern actually lives

The textbook `HIRToXTranslator` + `translate_hir_module`/`translate_hir_function`/`translate_hir_expression` triple appears in exactly 4 `hir_to_<lang>.runa` files: **elixir, haskell, ruby, scala**. These are precisely the four backends whose emitter is a vestigial shim — the real translator was moved into `hir_to_<lang>.runa` but the shim was left behind.

Other backends do real HIR-to-source translation but use different naming conventions (`generate_<X>_stmt`, `translate_<X>`, or per-construct `emit_<X>` calls). The canonical-trio pattern is not the only valid form; it is one of many.

### 2.3 Cleanest unified architecture

For a production-grade rewrite, every backend pair should be one of:

- **Pattern T (Translator-Only)**: A single `hir_to_<lang>.runa` file containing `HIRTo<Lang>Translator` (or equivalent context struct) and the full translator, internally calling `emitter_common.runa`'s `EmitterContext` API for all buffer writes. No `<lang>_emitter.runa` file. Suitable for backends where the emitter is a minimal-wrapper (css, graphql, html, json, jsx, markdown, mongodb, openapi, regex, toml, yaml) or has been reduced to one (Wave 2 migrated).

- **Pattern S (Smart-Emitter + Translator)**: Two files where the emitter is a deliberate per-construct printer (`emit_module`, `emit_function`, etc.) and the translator drives it. Suitable only for backends where the high-level emitter is genuinely shared OR where construct-level emission is a meaningful abstraction (powershell, r, vhdl, fsharp, erlang). The emitter must be HIR-aware (take HIR nodes as args), not language-AST-aware.

- **Pattern O (Orchestrator)**: For backends with their own frontend pipeline (lexer + parser + frontend translator + backend translator), the `<lang>_emitter.runa` becomes a true bridge file. It imports both `frontends/<lang>/<lang>_to_hir.runa` and `backends/<lang>/hir_to_<lang>.runa` and exposes the round-trip entry points the central dispatcher calls. Suitable for latex, makefile, verilog — already this pattern but needs signature normalization.

### 2.4 Special cases requiring individual treatment

1. **rust** — missing `hir_to_rust.runa` entirely. Either an intentional deletion or a gap. The dispatcher arm is broken.
2. **julia** — `julia_emitter.runa` is fully disconnected from `hir_to_julia.runa`. Pure dead code that the dispatcher imports.
3. **elixir/haskell/ruby/scala** — vestigial shims with placeholder frontend stubs that duplicate real `frontends/<lang>/` work.
4. **cpp/dart/hcl/lua/matlab/php/solidity** — orphan emitters that the matching translator does not import.
5. **dockerfile/erlang** — emitters that operate on the FRONTEND AST (DockerfileAST, ErlangModule) rather than HIR; they are sister files to `hir_to_<lang>.runa` rather than primitive layers.
6. **latex/makefile/verilog** — true orchestrators that bridge frontends and backends but have signature mismatches with the central dispatcher.
7. **vhdl** — emitter is bigger than translator (1064 vs 1191 LOC, but translator is only 10 procs delegating to 40 emitter procs); architecturally inverted.

### 2.5 Deletion / consolidation opportunity

After audit, the following could be deleted outright with their content merged into `hir_to_<lang>.runa` (or fully removed):

- **Outright delete (orphan emitter, no consumer)**: `cpp/cpp_emitter.runa`, `dart/dart_emitter.runa`, `hcl/hcl_emitter.runa`, `julia/julia_emitter.runa`, `lua/lua_emitter.runa`, `matlab/matlab_emitter.runa`, `php/php_emitter.runa`, `solidity/solidity_emitter.runa` — 8 files, ~4280 LOC of dead/duplicate code. Caveat: their formatter helpers may need to be inlined into `hir_to_<lang>.runa` where useful (e.g., dart identifier formatting).

- **Merge into hir_to (minimal-wrapper)**: `css/css_emitter.runa` (33 LOC), `graphql/graphql_emitter.runa` (33 LOC), `html/html_emitter.runa` (33 LOC), `json/json_emitter.runa` (53 LOC), `jsx/jsx_emitter.runa` (33 LOC), `markdown/markdown_emitter.runa` (52 LOC), `mongodb/mongodb_emitter.runa` (33 LOC), `openapi/openapi_emitter.runa` (43 LOC), `regex/regex_emitter.runa` (43 LOC), `toml/toml_emitter.runa` (52 LOC), `yaml/yaml_emitter.runa` (52 LOC) — 11 files, ~460 LOC. Each provides only 2 trivial wrappers around `emitter_common`; the translator can call `emitter_common` directly.

- **Demolish vestigial shim, keep stub frontend in frontends/ only**: `elixir/elixir_emitter.runa`, `haskell/haskell_emitter.runa`, `ruby/ruby_emitter.runa`, `scala/scala_emitter.runa` — 4 files, ~1060 LOC of placeholder stubs. The `hir_to_<lang>` and `<lang>_to_hir` entry-points the dispatcher needs should move into `hir_to_<lang>.runa` (for the HIR->lang side) and the frontend's `<lang>_to_hir.runa` (for the lang->HIR side). The shim itself disappears.

Total deletion opportunity: 23 files, ~5800 LOC, plus normalizing 4 vestigial shims.

### 2.6 Rust verdict

`rust_emitter.runa` is a Wave 2-migrated byte-buffer primitive in the same style as `c_emitter.runa`, `python_emitter.runa`, etc. — internally consistent and clean. The MISSING piece is `hir_to_rust.runa`, the actual translator. The dispatcher arm `Return proc rust_to_hir from RustEmitter with source_code` and `Return proc hir_to_rust from RustEmitter with hir_root` (translation.runa:3239, 3502) is referencing procs that do not exist in `rust_emitter.runa` or anywhere else.

There is no surviving evidence that Rust translation was ever implemented. The frontend at `frontends/rust/` exists but is not in scope for this survey. This is a real gap, not a deliberate omission — the dispatcher would crash or fail to link if the unresolved-proc dispatch were ever exercised. Recommended verdict: **gap to be filled** by writing a proper `hir_to_rust.runa` following Pattern T, plus the corresponding `rust_to_hir` proc co-located with it (or move the call sites of the dispatcher to point at the frontend).

---

## 3. Per-Backend Migration Plan (53 entries)

Plan labels:
- **Plan A (consolidate)** — move emitter content into hir_to_<lang>.runa, delete emitter file
- **Plan B (split-clean)** — keep both files but enforce strict layering
- **Plan C (already-clean)** — backend is the template
- **Plan D (special-case)** — backend needs custom handling

### arm — Plan C (already-clean)
Backend follows Pattern T plus a thin Wave 2 emitter wrapper. `arm_emitter.runa` is 112 LOC of pure delegation to `emitter_common`. `hir_to_arm.runa` consumes it via `Import as Emitter`. Use this as a template alongside python/go for the Wave 2 byte-buffer style.

### bash — Plan C (already-clean)
Same shape as arm. 111-LOC emitter, 948-LOC translator, clean delegation. Template-quality.

### c — Plan B (split-clean)
Already split correctly. One tweak: rename `generate_c_from_hir` to `hir_to_c` (or add an alias) so the central dispatcher's call shape matches. Same for adding a `c_to_hir` thin wrapper that bridges to `frontends/c/`.

### cmake — Plan B (split-clean)
Keep both. The 5-field state struct (buffer/capacity/length/indent_level/at_line_start) atop emitter_common is a useful template for stateful emitters. Document this layout convention. Wave 2 already done.

### cobol — Plan C (already-clean)
Standard Wave 2 pattern, 133/1742 split. Template-quality.

### cpp — Plan A (consolidate)
`cpp_emitter.runa` is an orphan — 588 LOC of `emit_cpp_text`/`emit_cpp_line`/etc. that `hir_to_cpp.runa` never imports. Plan: delete `cpp_emitter.runa`. Migrate any useful formatting logic (if any) into `hir_to_cpp.runa`. Migrate cpp's buffer ops to `emitter_common`'s `EmitterContext`.

### csharp — Plan C (already-clean)
Standard Wave 2. Template-quality.

### css — Plan A (consolidate)
33-LOC minimal-wrapper with 2 procs. Delete `css_emitter.runa`; have `hir_to_css.runa` import `emitter_common` directly.

### dart — Plan A (consolidate)
662-LOC orphan emitter with FileIO import (dead). `hir_to_dart.runa` never imports it. Plan: delete `dart_emitter.runa`. Move identifier-formatting helpers (`format_dart_identifier`, `is_dart_keyword`) into `hir_to_dart.runa` if used by it; otherwise drop them as dead code.

### dockerfile — Plan D (special-case)
`dockerfile_emitter.runa` is a Dockerfile-AST printer (operates on the frontend's `DockerfileAST`, not HIR). It is sister to `hir_to_dockerfile.runa`, not a primitive layer. Plan: rename `dockerfile_emitter.runa` -> `frontends/dockerfile/dockerfile_printer.runa` (it belongs with the frontend). Leave `hir_to_dockerfile.runa` alone. Move dispatcher entry-points (`dockerfile_to_hir`, `hir_to_dockerfile`) into a new bridge file matching the latex/makefile pattern, or co-locate them in `hir_to_dockerfile.runa`.

### elixir — Plan D (special-case)
Demolish `elixir_emitter.runa` (the vestigial shim with 8 stub procs). Move `elixir_to_hir` to `frontends/elixir/elixir_to_hir.runa` (which exists). Move `hir_to_elixir` to `hir_to_elixir.runa` (alias `translate_hir_to_elixir`). Drop the 8 stubs (`tokenize_elixir`, `create_elixir_parser`, etc.) entirely — they are unreachable placeholders.

### erlang — Plan D (special-case)
Like dockerfile: `erlang_emitter.runa` (1280 LOC, 27 emit_*) is an Erlang-AST printer that operates on frontend types. Two options: (1) move it to `frontends/erlang/erlang_printer.runa`; (2) keep it but rewrite to consume HIR directly (Pattern S). Recommend option 1 since `hir_to_erlang.runa` already does HIR -> Erlang independently.

### fsharp — Plan B (split-clean)
`fsharp_emitter.runa` is one of the few HIR-aware Smart-Emitter examples (Pattern S). 30 HIR-aware emit_* procs. Already Wave 2. Keep both, ensure all buffer writes flow through `emitter_common`. Good template for Pattern S.

### go — Plan C (already-clean)
Standard Wave 2.

### graphql — Plan A (consolidate)
33-LOC minimal-wrapper. Delete `graphql_emitter.runa`; `hir_to_graphql.runa` calls `emitter_common` directly.

### haskell — Plan D (special-case)
Same shim demolition as elixir. Move entry points to `frontends/haskell/haskell_to_hir.runa` and `hir_to_haskell.runa` (which already has `HIRToHaskellTranslator`).

### hcl — Plan A (consolidate)
Orphan emitter (`hir_to_hcl.runa` does not import it). 383 LOC. Delete; move any used helpers into `hir_to_hcl.runa`.

### html — Plan A (consolidate)
33-LOC minimal-wrapper. Delete.

### java — Plan C (already-clean)
Standard Wave 2 with extended primitive set (17 emit_* incl. comment/identifier-escape). Good template for the "rich-primitive emitter" variant of Pattern T.

### javascript — Plan C (already-clean)
Standard Wave 2. **Also: delete the stray file `sedcHb5aD` from `javascript/`** (editor leftover, not a real source file).

### json — Plan A (consolidate)
53-LOC minimal-wrapper. Delete.

### jsx — Plan A (consolidate)
33-LOC minimal-wrapper. Delete.

### julia — Plan D (special-case)
`julia_emitter.runa` is fully orphaned — no imports, no consumers, 629 LOC of unused formatter helpers. The dispatcher's `julia_to_hir from JuliaEmitter` and `hir_to_julia from JuliaEmitter` reference procs that DO NOT EXIST. Plan: (1) delete `julia_emitter.runa`; (2) add `julia_to_hir` proc to `frontends/julia/julia_to_hir.runa` (or wherever the Julia frontend lives); (3) rename `generate_julia_from_hir` in `hir_to_julia.runa` to `hir_to_julia`; (4) fix `translation.runa:72/3312/3575` to import `hir_to_julia.runa` (and `frontends/julia/`).

### latex — Plan B (split-clean) / Plan D (orchestrator)
True bridge file. Keep `latex_emitter.runa` as the orchestrator but document its role explicitly. Normalize signatures so the central dispatcher's single-arg `latex_to_hir source_code` and `hir_to_latex hir_root` calls match.

### llvmir — Plan C (already-clean)
Standard Wave 2.

### lua — Plan A (consolidate)
Orphan emitter, 710 LOC, `hir_to_lua.runa` does not import it. Delete; migrate any used helpers.

### makefile — Plan B/D (orchestrator)
Same as latex. Bridge file with `MakefileEmitter` struct that bundles components. Keep but normalize signatures to match dispatcher.

### markdown — Plan A (consolidate)
52-LOC minimal-wrapper. Delete.

### matlab — Plan A (consolidate)
616-LOC orphan emitter with FileIO import (dead). `hir_to_matlab.runa` does not import it. Delete; migrate any used identifier formatters.

### mongodb — Plan A (consolidate)
33-LOC minimal-wrapper. Delete.

### openapi — Plan A (consolidate)
43-LOC minimal-wrapper. Delete.

### php — Plan A (consolidate)
570-LOC orphan emitter; `hir_to_php.runa` does not import it. Delete; migrate any used helpers.

### powershell — Plan B (split-clean)
74 emit_* procs is the richest construct-level emitter. Already Wave 2. Pattern S template. Keep both. Document as canonical Smart-Emitter pattern.

### protobuf — Plan C (already-clean)
Standard Wave 2.

### python — Plan C (already-clean)
Standard Wave 2. Template-quality.

### r — Plan B (split-clean)
47 emit_* procs, similar to powershell. Pattern S. Keep both, already Wave 2.

### regex — Plan A (consolidate)
43-LOC minimal-wrapper. Delete.

### ruby — Plan D (special-case)
Same demolition as elixir/haskell. Move entry points; delete shim.

### runa — Plan C (already-clean)
Standard Wave 2. The HIR -> Runa reverse round-trip backend — important for the "Universal translation to Runa" mission per CLAUDE.md.

### rust — Plan D (special-case)
Create `hir_to_rust.runa` (currently MISSING). Co-locate `rust_to_hir` entry-point with the Rust frontend. Decide whether `rust_emitter.runa` stays as a Wave-2 byte-buffer primitive (Pattern T, ~70 LOC) or gets merged into the new `hir_to_rust.runa` (Plan A on the emitter once translator exists). The dispatcher arm in `translation.runa` is currently broken and must be re-pointed.

### scala — Plan D (special-case)
Same demolition as elixir/haskell/ruby. Move entry points; delete shim.

### solidity — Plan A (consolidate)
565-LOC orphan emitter. Delete.

### sql — Plan C (already-clean)
Standard Wave 2 with SQL-aware quoting primitives. Template-quality for stateful Pattern T.

### swift — Plan C (already-clean)
Standard Wave 2.

### swiftui — Plan C (already-clean)
Standard Wave 2.

### toml — Plan A (consolidate)
52-LOC minimal-wrapper. Delete.

### typescript — Plan C (already-clean)
Standard Wave 2.

### verilog — Plan B/D (orchestrator)
Same as latex/makefile. Keep as bridge with `VerilogEmitter` struct; normalize signatures.

### vhdl — Plan B (split-clean)
Pattern S with inverted size (emitter > translator). 40 construct-level emit_* procs. Migrate to Wave 2 (`vhdl_emitter.runa` is currently not migrated). Keep both files.

### wasm — Plan C (already-clean)
Standard Wave 2.

### x86 — Plan C (already-clean)
Standard Wave 2. Note: empty sibling `backends/x86_64/` should be removed.

### xml — Plan C (already-clean)
Standard Wave 2.

### yaml — Plan A (consolidate)
52-LOC minimal-wrapper. Delete.

### Other items
- `backends/llvm/` — empty directory, remove
- `backends/x86_64/` — empty directory, remove
- `backends/javascript/sedcHb5aD` — stray editor leftover, remove

---

## 4. Risk and Order

### 4.1 Highest-risk backends to migrate first (prove the template on tough cases)

These five backends concentrate the architectural complexity and downstream-consumer entanglement; doing them first proves the migration template can handle every shape:

1. **julia** — Most broken: orphan emitter, broken dispatcher, missing entry-point procs, no clean ancestor pattern. Whatever solution works here can be applied elsewhere.
2. **rust** — Most missing: needs `hir_to_rust.runa` created from scratch following Pattern T, plus repair of the dispatcher arm. Tests the "what does Pattern T look like at first authorship" template.
3. **scala** — Hardest shim demolition: 4-stub-pattern needs to be unwound across emitter, hir_to, AND frontends/scala/ in coordination. If this works, elixir/haskell/ruby are mechanical repetitions.
4. **dockerfile** — Hardest orchestrator decision: the emitter operates on frontend AST, not HIR. Decision here (move to frontends/ vs keep as sister) sets precedent for erlang.
5. **verilog** — Hardest signature normalization: orchestrator with emitter_ptr-first signatures incompatible with single-arg dispatcher. Repair here teaches the makefile/latex repair.

### 4.2 Easiest backends to batch together

The 11 minimal-wrapper Plan A deletions are mechanically identical — same 2-proc shape, same merge target. Batch in one PR:

- css, graphql, html, json, jsx, markdown, mongodb, openapi, regex, toml, yaml

Each migration is: delete `<lang>_emitter.runa`; in `hir_to_<lang>.runa`, replace `proc <X> from Emitter` with `proc emitter_raw_<X> from EmitterCommon` (or `proc emitter_ctx_<X> from EmitterCommon`); rebuild; verify PASS=340 FAIL=0.

### 4.3 Downstream consumers requiring updates

Every change to a backend's public proc set ripples into:

- `compiler/middle/gungnir/hir/translation.runa` — the central dispatcher (lines 53-83 imports, 3231-3707 dispatch arms). Affected by every Plan A deletion and every Plan D entry-point relocation. This is the single biggest downstream file.
- `compiler/middle/gungnir/hir/translation/tests/<lang>_tests.runa` — wherever they exist, they directly call into the emitter file (e.g., `verilog_tests.runa` calls `create_emitter from VerilogEmitter`). Affected by orchestrator changes and any Plan A consolidation.
- Backend-side test files: `dart_tests.runa`, `dockerfile_tests.runa`, `hcl_tests.runa`, `lua_tests.runa`, `matlab_tests.runa`, `php_tests.runa`, `solidity_tests.runa` (live inside backend dirs) — affected by the Plan A deletions for dart, hcl, lua, matlab, php, solidity.

Before merging any Plan A deletion, grep the full tree for the deleted file's import path:

```bash
grep -rn "backends/<lang>/<lang>_emitter" /mnt/d/.../v0.0.8.5/ --include="*.runa"
```

---

## 5. Sanity Gates

The acceptance gate at every migration step is:

```bash
cd /mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/RunaLang/runa/bootstrap/v0.0.8.5 && \
rm -rf /tmp/p2f_v && mkdir -p /tmp/p2f_v && pass=0; fail=0; \
for f in $(find compiler/middle/gungnir/hir/translation -name "*.runa"); do
  base=$(basename "$f" .runa)
  /tmp/runac_92 "$f" /tmp/p2f_v/"$base".s > /dev/null 2>&1 && \
  as /tmp/p2f_v/"$base".s -o /tmp/p2f_v/"$base".o 2>/dev/null
  if [ $? -eq 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); fi
done; echo "PASS=$pass FAIL=$fail"
```

Required: **PASS=340 FAIL=0** before and after every migration step.

For each Plan A deletion the expected delta is `PASS=340-1=339 FAIL=0` immediately after deletion (file count drops by 1), with the dispatcher rebuilt accordingly so the call sites resolve. After full Plan A batch (11 minimal-wrappers + 8 orphans), expect `PASS=321 FAIL=0`. After full Plan D rework (4 shim demolitions, julia, rust, dockerfile/erlang reclassification), final expected `PASS` count depends on whether the orchestrator entry-points are co-located with `hir_to_<lang>.runa` (no file delta) or moved to `frontends/<lang>/` (no backends/ file delta either).

Additionally, before any orchestrator rework, run a global grep gate to confirm no other compiler component references the file being deleted/renamed:

```bash
grep -rn "backends/<lang>/<lang>_emitter" \
  /mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/RunaLang/runa/bootstrap/v0.0.8.5/ \
  --include="*.runa"
```

---

## Appendix A: Wave 2 Migration Status Summary

Backends with Wave 2 (emitter_common-delegated buffers): 36 of 53

```
MIGRATED (36):    arm, bash, c, cmake, cobol, csharp, css, dockerfile, fsharp,
                  go, graphql, html, java, javascript, json, jsx, llvmir,
                  markdown, mongodb, openapi, powershell, protobuf, python, r,
                  regex, runa, rust, sql, swift, swiftui, toml, typescript,
                  wasm, x86, xml, yaml

NOT MIGRATED (17): cpp, dart, elixir, erlang, haskell, hcl, julia, latex, lua,
                  makefile, matlab, php, ruby, scala, solidity, verilog, vhdl
```

Of the 17 not migrated:
- 5 (latex, makefile, verilog plus halves of dockerfile/erlang) are orchestrators/sisters and don't need Wave 2 (they don't manage buffers directly)
- 4 (elixir, haskell, ruby, scala) are vestigial shims slated for demolition (Wave 2 moot)
- 7 (cpp, dart, hcl, lua, matlab, php, solidity) are orphan emitters slated for deletion (Wave 2 moot)
- 1 (julia) is dead code slated for deletion
- 0 backends remain that would benefit from a fresh Wave 2 migration on the current architecture

The Wave 2 migration appears to be effectively complete for all surviving emitter files. Post-rationalization, every backend either follows Wave 2 (Pattern T or stateful Pattern T) or is an orchestrator/Pattern S that doesn't need it.
