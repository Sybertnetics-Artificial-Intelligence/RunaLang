# Runa VS Code / Cursor Extension Source

This is the canonical, version-controlled source for the Runa syntax highlighting
extension. It lives in the Runa repo so the grammar is preserved across machine
reinstalls and tracked alongside language evolution.

## Files

- `syntaxes/runa.tmLanguage.json` — TextMate grammar used by VS Code, Cursor, and any
  other editor that consumes TextMate `.tmLanguage.json` grammars. This is the
  static-rule highlighter that runs instantly on file open.
- `language-configuration.json` — bracket pairs, comments, auto-indent rules.
- `package.json` — extension manifest (publisher, version, language id, grammar
  registration).

## Relationship to the LSP semantic tokenizer

There are TWO highlighting layers in Runa tooling:

1. **TextMate grammar (this directory)** — instant rule-based coloring. Runs in the
   editor itself. No LSP server needed.
2. **LSP semantic tokens** at `bootstrap/v0.0.8.5/compiler/services/ide_integration/syntax_highlighting.runa` —
   richer, semantics-aware tokens computed by the LSP server. Overrides TextMate
   grammar where the editor enables semantic-token highlighting.

Both should classify Runa source consistently. If you change one, also update the
other.

## Deployment

The installed extension copies live at (on this dev machine):

- `~/.vscode/extensions/sybertnetics.runa-language-support-v2-2.0.3/`
- `~/.cursor/extensions/sybertnetics.runa-language-support-v2-2.0.3/`

To deploy a change from this source-of-truth into the installed extensions, copy the
relevant file across. (Future improvement: a build/install script that publishes from
this directory to the installed locations.)

After updating an installed extension's files, **reload the editor window** for the
change to take effect (Ctrl+Shift+P → "Developer: Reload Window").

## Notable rules and what they protect

- `comment.line.note.single.runa` — single-line `Note: ...` comments
- `comment.block.note.runa` — multi-line `Note: ... :End Note` blocks; body is a
  single comment scope, internal patterns disabled (so apostrophes etc. don't break
  highlighting)
- `comment.block.annotation.runa` — annotation blocks (`@Reasoning: ... @End Reasoning`
  and similar). Same protection as Note: blocks. **Added 2026-05-18** to fix the
  apostrophe-breaks-everything bug reported by the CEO.
- `comment.line.annotation.runa` — single-line annotation form
  (`@Reasoning: short text`).

## Annotation names recognized

The grammar's annotation rules currently recognize these names (matched
case-insensitively):

`Reasoning`, `Implementation`, `Performance_Hints`, `Security_Scope`, `TestCases`,
`Verification`, `Pre_Conditions`, `Post_Conditions`, `Invariants`, `Examples`, `Notes`,
`References`.

If a new annotation type is added to the language spec (`docs/user/language-specification/runa_annotation_system.md`),
add it to BOTH `comment.block.annotation.runa` and `comment.line.annotation.runa`
patterns in `syntaxes/runa.tmLanguage.json`, AND to the LSP semantic tokenizer.
