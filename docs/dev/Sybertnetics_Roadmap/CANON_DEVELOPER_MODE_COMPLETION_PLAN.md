# Canon/Developer Mode Switching - Implementation Completion Plan

**Document Version**: 1.0.0  
**Date**: 2025  
**Priority**: HIGH - Required for Triple Syntax Architecture  
**Status**: Partially Implemented  

---

## 📊 Current State Assessment

### ✅ **Already Complete:**
1. **Operator Conversion Infrastructure**
   - `Keywords.convert_operator()` - Converts operators between modes
   - `create_operator_lookup_tables()` - Bidirectional mapping tables
   - Full operator mappings defined (Canon ↔ Developer)

2. **Dev Tools CLI Structure**
   - `/src/dev_tools/cli/commands/syntax.runa` - CLI handlers
   - `/src/dev_tools/syntax_converter/canonical_mode.runa` - Canon mode processor
   - `/src/dev_tools/syntax_converter/developer_mode.runa` - Developer mode processor
   - `detect_source_file_mode()` - Basic mode detection

3. **Lexer Foundation**
   - `LexerState.syntax_mode` field exists
   - Lexer references conversion functions correctly
   - Math symbols have conversion support

### ⚠️ **Incomplete Components:**
1. **Mode Switching Logic** - No runtime mode switching
2. **Lexer Mode Integration** - No CLI → Lexer mode passing
3. **Mode Persistence** - No project/user preferences

---

## 🎯 Implementation Plan

### **Phase 1: Complete Lexer Mode Integration** (2 days)

#### 1.1 Create Lexer Factory with Mode Support
**File:** `/src/compiler/frontend/lexical/lexer_factory.runa`

```runa
Process called "create_lexer_with_mode" that takes source as String, mode as String returns LexerState:
    @Implementation
        Factory function to create a lexer with specified syntax mode.
        Validates mode and initializes lexer with proper configuration.
    @End Implementation
    
    Note: Validate syntax mode
    If Not validate_syntax_mode(mode):
        Throw LexerError with message as "Invalid syntax mode: " concatenated with mode
    End If
    
    Note: Create base lexer
    Let lexer be create_lexer(source)
    
    Note: Set syntax mode
    Set lexer.syntax_mode to mode
    
    Note: Initialize mode-specific settings
    If string_equals(mode, "developer"):
        configure_developer_mode(lexer)
    Otherwise:
        configure_canon_mode(lexer)
    End If
    
    Return lexer
End Process

Process called "validate_syntax_mode" that takes mode as String returns Boolean:
    Return string_equals(mode, "canon") Or string_equals(mode, "developer")
End Process
```

#### 1.2 Update Lexer Initialization
**File:** `/src/compiler/frontend/lexical/lexer.runa` (UPDATE)

Add mode parameter to existing `create_lexer` function:
```runa
Process called "create_lexer" that takes source as String, mode as Optional[String] returns LexerState:
    Let actual_mode be mode or "canon"  Note: Default to canon mode
    
    Let lexer be LexerState with
        source as source,
        syntax_mode as actual_mode,
        ... existing fields ...
    End LexerState
    
    Return lexer
End Process
```

---

### **Phase 2: CLI to Compiler Mode Passing** (3 days)

#### 2.1 Update Compiler Driver Interface
**File:** `/src/compiler/driver/compiler_driver.runa` (UPDATE)

```runa
Type called "CompilationOptions":
    ... existing fields ...
    syntax_mode as String  Note: "canon" or "developer"
End Type

Process called "compile_with_options" that takes source_file as String, options as CompilationOptions returns CompilationResult:
    Note: Read source file
    Let source be read_file(source_file)
    
    Note: Create lexer with specified mode
    Let lexer be create_lexer_with_mode(source, options.syntax_mode)
    
    Note: Continue with compilation pipeline
    Let tokens be tokenize(lexer)
    ... rest of compilation ...
End Process
```

#### 2.2 Update CLI Main Entry Point
**File:** `/src/compiler/main.runa` (UPDATE)

```runa
Process called "parse_command_line_args" that takes args as List[String] returns CompilationOptions:
    Let options be default_compilation_options()
    
    For arg in args:
        Match arg:
            When "--canon":
                Set options.syntax_mode to "canon"
            When "--developer":
                Set options.syntax_mode to "developer"
            ... other arguments ...
        End Match
    End For
    
    Return options
End Process
```

---

### **Phase 3: Mode Configuration & Persistence** (2 days)

#### 3.1 Create Configuration Manager
**File:** `/src/compiler/config/mode_config.runa` (NEW)

```runa
Note:
Mode Configuration Manager

Handles syntax mode preferences at multiple levels:
- Command line (highest priority)
- Project configuration (.runa/config.toml)
- User preferences (~/.runa/preferences.toml)
- System defaults (lowest priority)
:End Note

Type called "ModeConfiguration":
    default_mode as String
    project_mode as Optional[String]
    user_preference as Optional[String]
    cli_override as Optional[String]
End Type

Process called "determine_syntax_mode" that takes cli_args as List[String] returns String:
    @Implementation
        Determine syntax mode using priority hierarchy:
        1. CLI argument (--canon or --developer)
        2. Project configuration
        3. User preferences
        4. System default (canon)
    @End Implementation
    
    Let config be load_mode_configuration()
    
    Note: Check CLI override first
    If config.cli_override is not None:
        Return config.cli_override
    End If
    
    Note: Check project configuration
    If config.project_mode is not None:
        Return config.project_mode
    End If
    
    Note: Check user preferences
    If config.user_preference is not None:
        Return config.user_preference
    End If
    
    Note: Fall back to system default
    Return config.default_mode
End Process

Process called "save_project_mode_preference" that takes mode as String returns Boolean:
    Note: Save mode preference to project configuration
    Let config_path be ".runa/config.toml"
    Let config be load_or_create_config(config_path)
    
    Set config.syntax_mode to mode
    
    Return save_config(config_path, config)
End Process
```

#### 3.2 Project Configuration File Format
**File:** `.runa/config.toml` (EXAMPLE)

```toml
# Runa Project Configuration

[syntax]
# Default syntax mode for this project
# Options: "canon" or "developer"
default_mode = "canon"

[compilation]
# Other compilation options...
```

---

### **Phase 4: Mode Detection Enhancement** (1 day)

#### 4.1 Improve File Mode Detection
**File:** `/src/dev_tools/cli/commands/syntax.runa` (UPDATE)

```runa
Process called "detect_source_file_mode" that takes file_path as String returns String:
    @Implementation
        Enhanced detection using multiple heuristics:
        - File header comments
        - Syntax patterns
        - Operator usage
    @End Implementation
    
    Try:
        Let content be read_file(file_path)
        
        Note: Check for explicit mode declaration in header
        Let header_mode be detect_mode_from_header(content)
        If header_mode is not None:
            Return header_mode
        End If
        
        Note: Score-based detection
        Let canon_score be calculate_canon_score(content)
        Let developer_score be calculate_developer_score(content)
        
        If canon_score > developer_score:
            Return "canon"
        Otherwise If developer_score > canon_score:
            Return "developer"
        Otherwise:
            Return "canon"  Note: Default to canon when uncertain
        End If
        
    Catch error:
        Return "canon"  Note: Default on error
End Process

Process called "detect_mode_from_header" that takes content as String returns Optional[String]:
    Note: Look for mode declaration in file header comments
    If content starts with "Note: Mode: canon":
        Return "canon"
    Otherwise If content starts with "Note: Mode: developer":
        Return "developer"
    Otherwise:
        Return None
    End If
End Process

Process called "calculate_canon_score" that takes content as String returns Integer:
    Let score be 0
    
    Note: Canon mode indicators
    If content contains "Process called": Add 10 to score
    If content contains "Let ": Add 5 to score
    If content contains "Type called": Add 5 to score
    If content contains " plus ": Add 3 to score
    If content contains " minus ": Add 3 to score
    If content contains "is equal to": Add 3 to score
    
    Return score
End Process

Process called "calculate_developer_score" that takes content as String returns Integer:
    Let score be 0
    
    Note: Developer mode indicators
    If content contains "proc ": Add 10 to score
    If content contains "func ": Add 10 to score
    If content contains "==": Add 5 to score
    If content contains "!=": Add 5 to score
    If content contains "++": Add 3 to score
    If content contains "+=": Add 3 to score
    
    Return score
End Process
```

---

### **Phase 5: Testing & Validation** (2 days)

#### 5.1 Mode Switching Tests
**File:** `/tests/compiler/frontend/lexical/test_mode_switching.runa`

```runa
Process called "test_lexer_mode_creation":
    Note: Test creating lexer with different modes
    
    Let canon_lexer be create_lexer_with_mode("Let x be 5", "canon")
    Assert canon_lexer.syntax_mode equals "canon"
    
    Let dev_lexer be create_lexer_with_mode("let x = 5", "developer")
    Assert dev_lexer.syntax_mode equals "developer"
    
    Note: Test invalid mode
    Try:
        Let bad_lexer be create_lexer_with_mode("test", "invalid")
        Assert False with message as "Should have thrown error for invalid mode"
    Catch error:
        Assert True
    End Try
End Process

Process called "test_operator_conversion_in_lexer":
    Note: Test that operators are converted based on mode
    
    Let canon_source be "x plus y"
    Let canon_lexer be create_lexer_with_mode(canon_source, "canon")
    Let canon_tokens be tokenize(canon_lexer)
    Assert canon_tokens contains token with value "plus"
    
    Let dev_source be "x + y"
    Let dev_lexer be create_lexer_with_mode(dev_source, "developer")
    Let dev_tokens be tokenize(dev_lexer)
    Assert dev_tokens contains token with value "+"
End Process
```

#### 5.2 CLI Integration Tests
**File:** `/tests/cli/test_mode_cli_integration.runa`

```runa
Process called "test_cli_mode_passing":
    Note: Test that CLI flags properly pass mode to compiler
    
    Let result be run_compiler(["--canon", "test.runa"])
    Assert result.mode_used equals "canon"
    
    Let result be run_compiler(["--developer", "test.runa"])
    Assert result.mode_used equals "developer"
    
    Let result be run_compiler(["test.runa"])  Note: No mode flag
    Assert result.mode_used equals "canon"  Note: Default
End Process
```

---

## 📅 Timeline Summary

| Phase | Description | Duration | Dependencies |
|-------|-------------|----------|--------------|
| **Phase 1** | Complete Lexer Mode Integration | 2 days | None |
| **Phase 2** | CLI to Compiler Mode Passing | 3 days | Phase 1 |
| **Phase 3** | Mode Configuration & Persistence | 2 days | Phase 2 |
| **Phase 4** | Mode Detection Enhancement | 1 day | None (parallel) |
| **Phase 5** | Testing & Validation | 2 days | Phases 1-4 |

**Total Estimated Time:** 8-10 working days

---

## 🚀 Implementation Priority

1. **CRITICAL** - Phase 1 & 2: Core mode switching functionality
2. **HIGH** - Phase 4: Better mode detection
3. **MEDIUM** - Phase 3: Configuration persistence
4. **REQUIRED** - Phase 5: Testing before release

---

## ✅ Success Criteria

- [ ] Lexer accepts and respects syntax mode parameter
- [ ] CLI flags `--canon` and `--developer` work correctly
- [ ] Mode is properly passed through entire compilation pipeline
- [ ] Operators are converted based on active mode
- [ ] File mode detection is accurate >90% of the time
- [ ] Project preferences are saved and loaded
- [ ] All tests pass for both modes
- [ ] Documentation is updated with mode usage

---

## 📝 Notes

- Keywords remain consistent across modes (no "proc" shortcuts per user requirement)
- Only operators and symbols change between modes
- Default mode is always "canon" when not specified
- Viewer mode is handled separately as a display-only transformation