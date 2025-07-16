# Runa Language Server Protocol (LSP) Core API

The Runa Language Server Protocol provides comprehensive IDE integration and development tooling for the Runa programming language. This document covers the core LSP implementation and API.

## Overview

The Runa LSP server implements the Language Server Protocol specification, providing language intelligence features for any LSP-compatible editor or IDE. The server is written in Python and provides natural language syntax support.

## Server Configuration

### Installation

```bash
# Install the Runa LSP server
pip install runa-lsp

# Or install from source
git clone https://github.com/runa-lang/runa-lsp
cd runa-lsp
pip install -e .
```

### Basic Configuration

```json
{
  "runa-lsp": {
    "enabled": true,
    "command": ["runa-lsp"],
    "args": ["--log-level=info"],
    "env": {
      "RUNA_HOME": "/path/to/runa/installation"
    }
  }
}
```

### Advanced Configuration

```json
{
  "runa-lsp": {
    "enabled": true,
    "command": ["runa-lsp"],
    "args": [
      "--log-level=debug",
      "--memory-limit=512MB",
      "--timeout=30s",
      "--max-workers=4"
    ],
    "env": {
      "RUNA_HOME": "/path/to/runa/installation",
      "RUNA_CACHE_DIR": "/path/to/cache",
      "RUNA_LOG_LEVEL": "debug"
    },
    "settings": {
      "runa": {
        "targetLanguage": "python",
        "optimizationLevel": "O2",
        "enableTypeChecking": true,
        "enableLinting": true,
        "formatOnSave": true,
        "autoImport": true
      }
    }
  }
}
```

## Core LSP Features

### Text Document Synchronization

The Runa LSP server supports full text document synchronization:

```runa
# Example: Document change notification
Process called "handle_document_change" that takes uri as String and changes as List[TextDocumentContentChangeEvent]:
    For each change in changes:
        Let range be change.range
        Let text be change.text
        Update document with uri as uri and range as range and text as text
        Trigger reanalysis with document as uri
```

### Language Features

#### Completion

```runa
# Example: Code completion implementation
Process called "provide_completion" that takes position as Position and context as CompletionContext returns List[CompletionItem]:
    Let document be get_document with uri as context.uri
    Let tokens be tokenize_document with document as document
    Let suggestions be generate_completions with:
        tokens as tokens
        position as position
        context as context
    Return suggestions
```

#### Hover Information

```runa
# Example: Hover information provider
Process called "provide_hover" that takes position as Position returns Hover:
    Let document be get_document with uri as position.uri
    Let symbol be find_symbol_at_position with:
        document as document
        position as position
    If symbol is not None:
        Return Hover with:
            contents as symbol.documentation
            range as symbol.range
    Otherwise:
        Return None
```

#### Signature Help

```runa
# Example: Signature help provider
Process called "provide_signature_help" that takes position as Position returns SignatureHelp:
    Let document be get_document with uri as position.uri
    Let function_call be find_function_call_at_position with:
        document as document
        position as position
    If function_call is not None:
        Let signatures be get_function_signatures with function as function_call.name
        Return SignatureHelp with:
            signatures as signatures
            active_signature as function_call.active_signature
            active_parameter as function_call.active_parameter
    Otherwise:
        Return None
```

#### Definition and References

```runa
# Example: Definition provider
Process called "provide_definition" that takes position as Position returns List[Location]:
    Let document be get_document with uri as position.uri
    Let symbol be find_symbol_at_position with:
        document as document
        position as position
    If symbol is not None:
        Let definition be find_symbol_definition with symbol as symbol
        Return list containing Location with:
            uri as definition.uri
            range as definition.range
    Otherwise:
        Return empty list

# Example: References provider
Process called "provide_references" that takes position as Position and context as ReferenceContext returns List[Location]:
    Let document be get_document with uri as position.uri
    Let symbol be find_symbol_at_position with:
        document as document
        position as position
    If symbol is not None:
        Let references be find_symbol_references with:
            symbol as symbol
            include_declaration as context.include_declaration
        Return references
    Otherwise:
        Return empty list
```

#### Document Symbols

```runa
# Example: Document symbols provider
Process called "provide_document_symbols" that takes document as TextDocument returns List[SymbolInformation]:
    Let ast be parse_document with document as document
    Let symbols be extract_symbols from ast
    Return symbols
```

#### Workspace Symbols

```runa
# Example: Workspace symbols provider
Process called "provide_workspace_symbols" that takes query as String returns List[SymbolInformation]:
    Let workspace be get_workspace()
    Let symbols be search_workspace_symbols with:
        workspace as workspace
        query as query
    Return symbols
```

### Code Actions and Refactoring

#### Code Actions

```runa
# Example: Code actions provider
Process called "provide_code_actions" that takes range as Range and context as CodeActionContext returns List[CodeAction]:
    Let actions be empty list
    For each diagnostic in context.diagnostics:
        Let fix be generate_fix for diagnostic
        If fix is not None:
            Add fix to actions
    Return actions
```

#### Refactoring

```runa
# Example: Rename provider
Process called "provide_rename" that takes position as Position and new_name as String returns WorkspaceEdit:
    Let document be get_document with uri as position.uri
    Let symbol be find_symbol_at_position with:
        document as document
        position as position
    If symbol is not None:
        Let references be find_symbol_references with symbol as symbol
        Let changes be create_rename_changes with:
            references as references
            new_name as new_name
        Return WorkspaceEdit with changes as changes
    Otherwise:
        Return None
```

### Formatting and Linting

#### Document Formatting

```runa
# Example: Document formatter
Process called "format_document" that takes document as TextDocument and options as FormattingOptions returns List[TextEdit]:
    Let ast be parse_document with document as document
    Let formatted_ast be format_ast with:
        ast as ast
        options as options
    Let edits be generate_formatting_edits with:
        original as document
        formatted as formatted_ast
    Return edits
```

#### Range Formatting

```runa
# Example: Range formatter
Process called "format_range" that takes document as TextDocument and range as Range and options as FormattingOptions returns List[TextEdit]:
    Let ast be parse_document_range with:
        document as document
        range as range
    Let formatted_ast be format_ast with:
        ast as ast
        options as options
    Let edits be generate_formatting_edits with:
        original as document
        formatted as formatted_ast
        range as range
    Return edits
```

#### On-Type Formatting

```runa
# Example: On-type formatter
Process called "format_on_type" that takes document as TextDocument and position as Position and ch as String and options as FormattingOptions returns List[TextEdit]:
    If ch is equal to ":" or ch is equal to "}":
        Let range be create_range with:
            start as position
            end as position
        Return format_range with:
            document as document
            range as range
            options as options
    Otherwise:
        Return empty list
```

### Diagnostics and Linting

#### Diagnostics

```runa
# Example: Diagnostics provider
Process called "provide_diagnostics" that takes document as TextDocument returns List[Diagnostic]:
    Let ast be parse_document with document as document
    Let diagnostics be validate_ast with ast as ast
    Return diagnostics
```

#### Linting

```runa
# Example: Linting provider
Process called "provide_linting" that takes document as TextDocument returns List[Diagnostic]:
    Let ast be parse_document with document as document
    Let linting_rules be get_linting_rules()
    Let violations be apply_linting_rules with:
        ast as ast
        rules as linting_rules
    Return violations
```

## Runa-Specific Extensions

### Natural Language Completion

```runa
# Example: Natural language completion
Process called "provide_natural_completion" that takes position as Position and context as CompletionContext returns List[CompletionItem]:
    Let document be get_document with uri as context.uri
    Let natural_context be extract_natural_context with:
        document as document
        position as position
    Let suggestions be generate_natural_suggestions with:
        context as natural_context
        position as position
    Return suggestions
```

### AI-Assisted Features

```runa
# Example: AI-assisted code generation
Process called "provide_ai_completion" that takes position as Position and context as CompletionContext returns List[CompletionItem]:
    Let document be get_document with uri as context.uri
    Let code_context be extract_code_context with:
        document as document
        position as position
    Let ai_suggestions be generate_ai_suggestions with:
        context as code_context
        position as position
    Return ai_suggestions
```

### Multi-Language Support

```runa
# Example: Target language switching
Process called "switch_target_language" that takes target_language as String returns Boolean:
    Let config be get_workspace_config()
    Set config.target_language to target_language
    Save config with config as config
    Trigger reanalysis with workspace as get_workspace()
    Return true
```

## Performance and Optimization

### Caching

```runa
# Example: AST caching
Process called "get_cached_ast" that takes document as TextDocument returns Optional[AST]:
    Let cache_key be generate_cache_key with document as document
    Let cached_ast be get_from_cache with key as cache_key
    If cached_ast is not None and is_valid with ast as cached_ast:
        Return cached_ast
    Otherwise:
        Let new_ast be parse_document with document as document
        Store in cache with key as cache_key and value as new_ast
        Return new_ast
```

### Incremental Processing

```runa
# Example: Incremental parsing
Process called "incremental_parse" that takes document as TextDocument and changes as List[TextDocumentContentChangeEvent] returns AST:
    Let base_ast be get_cached_ast with document as document
    For each change in changes:
        Let base_ast be apply_change to base_ast with change as change
    Return base_ast
```

## Error Handling

### Graceful Degradation

```runa
# Example: Error handling in LSP
Process called "safe_lsp_operation" that takes operation as Function returns Result[Output, LSPError]:
    Try:
        Let result be operation()
        Return Success with value as result
    Catch parse_error as ParseError:
        Return Error with error as LSPError with:
            code as "PARSE_ERROR"
            message as parse_error.message
    Catch validation_error as ValidationError:
        Return Error with error as LSPError with:
            code as "VALIDATION_ERROR"
            message as validation_error.message
    Catch unexpected_error:
        Return Error with error as LSPError with:
            code as "UNEXPECTED_ERROR"
            message as "An unexpected error occurred"
```

### Logging and Diagnostics

```runa
# Example: LSP logging
Process called "log_lsp_event" that takes event as String and details as Dictionary:
    Let log_entry be create_log_entry with:
        timestamp as current_time
        event as event
        details as details
        level as "info"
    Write to log with entry as log_entry
```

## Testing

### Unit Tests

```runa
# Example: LSP unit test
Test "completion_provider":
    Let document be create_test_document with content as "Let x be 42"
    Let position be Position with line 0 and character 5
    Let completions be provide_completion with:
        position as position
        context as CompletionContext
    Assert length of completions is greater than 0
    Assert any item in completions satisfies item.label is equal to "be"
```

### Integration Tests

```runa
# Example: LSP integration test
Test "end_to_end_completion":
    Let server be start_lsp_server()
    Let client be create_lsp_client()
    Connect client to server
    Let document be open_document with client as client and uri as "test.runa"
    Let completions be request_completion with:
        client as client
        position as Position with line 0 and character 5
    Assert completions is not None
    Shutdown server
```

## Configuration Reference

### Server Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `runa.targetLanguage` | String | "python" | Default target language for compilation |
| `runa.optimizationLevel` | String | "O1" | Compiler optimization level |
| `runa.enableTypeChecking` | Boolean | true | Enable type checking |
| `runa.enableLinting` | Boolean | true | Enable linting |
| `runa.formatOnSave` | Boolean | false | Format document on save |
| `runa.autoImport` | Boolean | true | Auto-import missing modules |
| `runa.memoryLimit` | String | "256MB" | Memory limit for server |
| `runa.timeout` | String | "30s" | Operation timeout |
| `runa.maxWorkers` | Integer | 4 | Maximum worker threads |

### Client Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `runa-lsp.enabled` | Boolean | true | Enable Runa LSP |
| `runa-lsp.command` | Array | `["runa-lsp"]` | LSP server command |
| `runa-lsp.args` | Array | `[]` | LSP server arguments |
| `runa-lsp.env` | Object | `{}` | Environment variables |

## Troubleshooting

### Common Issues

1. **Server not starting**: Check Python installation and dependencies
2. **No completions**: Verify document syntax and server configuration
3. **Slow performance**: Adjust memory limits and worker count
4. **Type checking errors**: Check target language compatibility

### Debug Mode

Enable debug logging for troubleshooting:

```json
{
  "runa-lsp": {
    "args": ["--log-level=debug", "--verbose"]
  }
}
```

### Performance Profiling

Profile LSP performance:

```bash
# Enable performance profiling
runa-lsp --profile --profile-output=profile.json

# Analyze profile
python -m runa_lsp.profiler profile.json
```

## API Reference

### Core Classes

- `RunaLanguageServer` - Main LSP server implementation
- `DocumentManager` - Document synchronization and management
- `CompletionProvider` - Code completion implementation
- `DiagnosticProvider` - Error and warning reporting
- `FormattingProvider` - Code formatting implementation

### Key Methods

- `initialize()` - Initialize LSP server
- `shutdown()` - Graceful server shutdown
- `exit()` - Force server exit
- `textDocument/didOpen()` - Handle document open
- `textDocument/didChange()` - Handle document changes
- `textDocument/didClose()` - Handle document close
- `textDocument/completion()` - Provide completions
- `textDocument/hover()` - Provide hover information
- `textDocument/definition()` - Find definitions
- `textDocument/references()` - Find references
- `textDocument/formatting()` - Format documents
- `textDocument/rename()` - Rename symbols

This LSP implementation provides comprehensive language intelligence for Runa, enabling rich IDE features while maintaining the language's natural syntax philosophy. 