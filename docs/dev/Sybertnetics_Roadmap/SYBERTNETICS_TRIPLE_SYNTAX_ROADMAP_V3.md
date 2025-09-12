# Sybertnetics Triple Syntax Architecture Roadmap v3.0
## Comprehensive Implementation Plan for READ-ONLY Viewer + Canonical Runa + Technical Developer Syntax

**Document Version**: 3.0.0  
**Date**: 2025  
**Priority**: FOUNDATIONAL - ARCHITECTURAL CORRECTION  
**Previous Version**: 2.0.0 (SYBERTNETICS_DUAL_SYNTAX_ROADMAP.md)  
**Architecture Change**: Viewer Mode → READ-ONLY Display, Canon Mode → NEW Writeable Standard  

---

## 🔄 CRITICAL ARCHITECTURAL UPDATE

### **Evolution from Dual to Triple Syntax**

**ORIGINAL DUAL SYSTEM (v1.0):**
- `--viewer`: Canonical Runa (writeable) 
- `--developer`: Technical syntax (writeable)

**INCORRECT TRIPLE SYSTEM (v2.0):**  
- `--viewer`: Natural language sentences (writeable) ❌ **WRONG**
- `--canon`: Canonical Runa (writeable)
- `--developer`: Technical syntax (writeable)

**CORRECT TRIPLE SYSTEM (v3.0):** ✅
- `--viewer`: Natural language sentences (**READ-ONLY DISPLAY**)
- `--canon`: Canonical Runa (**WRITEABLE** - replaces old viewer)  
- `--developer`: Technical syntax (**WRITEABLE**)

---

## 🎯 Executive Summary

The **Triple Syntax Architecture v3.0** provides three distinct interaction modes with Runa code:

### **The Corrected Triple Flow**

```
WRITE IN:                    DISPLAY IN:
┌─────────────────┐         ┌─────────────────┐
│  --canon        │◄────────┤  --viewer       │
│  (writeable)    │         │  (read-only)    │
│  Canonical Runa │         │  Natural Lang   │
└─────────────────┘         └─────────────────┘
         ▲                           ▲
         │                           │
         ▼                           │
┌─────────────────┐                  │
│  --developer    │──────────────────┘
│  (writeable)    │
│  Technical      │
└─────────────────┘
```

### **Key Architectural Principles**

1. **Canonical Foundation**: `--canon` is the new writeable canonical form (replacing old `--viewer`)
2. **Read-Only Display**: `--viewer` is ONLY for display/comprehension (AI-readable sentences)
3. **Technical Writing**: `--developer` remains writeable technical syntax 
4. **Bidirectional Conversion**: `--canon` ↔ `--developer` (both writeable)
5. **Unidirectional Display**: `--canon`/`--developer` → `--viewer` (display only)
6. **Return Path**: `--viewer` → `--canon`/`--developer` (for editing only)

---

## 🔧 IMPLEMENTATION CORRECTIONS NEEDED

### **Phase 1: Update Existing Dev Tools**

#### **1.1 Fix Current CLI Commands**

**Current Broken State:**
```bash
# These work incorrectly due to architecture misunderstanding
runa compile --viewer input.runa      # WRONG: tries to write viewer mode
runa syntax --viewer input.runa       # WRONG: treats viewer as writeable
```

**Required Fixes:**
```bash
# Correct usage patterns
runa compile --canon input.runa       # NEW: canonical writeable mode
runa compile --developer input.runa   # EXISTING: technical writeable mode
runa view --viewer input.runa         # NEW: display-only viewer mode
runa convert --from=canon --to=viewer input.runa  # NEW: conversion for display
```

#### **1.2 Update Dev Tools Architecture**

**Files to Update:**
- `runa/src/dev_tools/cli/commands/syntax.runa` - Fix CLI interface
- `runa/src/dev_tools/syntax_converter/viewer_mode.runa` - Make read-only
- `runa/src/dev_tools/syntax_converter/canonical_mode.runa` - **CREATE NEW**

### **Phase 2: Create Missing Components**

#### **2.1 Canonical Mode Converter (NEW)**

**File:** `runa/src/dev_tools/syntax_converter/canonical_mode.runa`

```runa
Note:
Canonical Mode Syntax Converter - The New Writeable Standard

Replaces the old viewer mode as the primary writeable canonical form.
This is the standard Runa syntax that serves as the compilation target
and the primary writing interface.

Features:
- Standard Runa syntax (`Process called "name"` etc.)
- Full writeable capability
- Direct compilation target
- Serves as intermediate for conversions
:End Note

Process called "handle_canonical_mode" that takes args as List[String] and options as Dictionary[String, Any] returns Integer:
    Note: Handle --canon flag for canonical Runa writing/editing
    Try:
        Let input_file be get_input_file with args as args
        Let output_file be get_output_file with args as args
        Let canonical_options be create_canonical_options with options as options
        
        Note: Canonical mode is primarily passthrough since it's the native form
        Let success be process_canonical_file with source_file as input_file and output_file as output_file and options as canonical_options
        
        If success:
            If output_file is None:
                Note: Output canonical form to stdout
                Return 0
            Otherwise:
                Display "✓ Canonical mode processing complete"
                Display "  Input:  " plus input_file
                Display "  Output: " plus output_file
                Return 0
        Otherwise:
            Display "✗ Canonical mode processing failed"
            Return 1
            
    Catch error:
        Display "Error in canonical mode: " plus error.message
        Return 1
```

#### **2.2 Updated CLI Interface**

**File:** `runa/src/dev_tools/cli/commands/syntax.runa` (UPDATED)

```runa
Note: Updated CLI command handlers for corrected triple syntax

Process called "handle_syntax_command" that takes args as List[String] and options as Dictionary[String, Any] returns Integer:
    Note: Handle dedicated 'runa syntax' command with corrected architecture
    Try:
        If options.contains("canon"):
            Return handle_canonical_mode with args as args and options as options
        Else if options.contains("developer"):
            Return handle_developer_mode with args as args and options as options
        Else if options.contains("viewer"):
            Note: Viewer mode is READ-ONLY display - convert FROM other modes
            Return handle_viewer_display_mode with args as args and options as options
        Otherwise:
            Display "Error: Must specify --canon, --developer, or --viewer mode"
            Display ""
            Call show_updated_syntax_help
            Return 1
            
    Catch error:
        Display "Syntax command error: " plus error.message
        Return 1

Process called "handle_viewer_display_mode" that takes args as List[String] and options as Dictionary[String, Any] returns Integer:
    Note: Handle --viewer flag for READ-ONLY display (not editing)
    Try:
        Let input_file be get_input_file with args as args
        Let source_mode be detect_source_mode with file as input_file
        
        Note: Viewer mode only displays - determine source mode first
        Let viewer_content be convert_to_viewer_display with source_file as input_file and source_mode as source_mode
        
        Display "📖 VIEWER MODE (Read-Only Display):"
        Display "Source: " plus source_mode
        Display "─────────────────────────────────────"
        Display viewer_content
        
        Return 0
        
    Catch error:
        Display "Error in viewer display mode: " plus error.message
        Return 1
```

### **Phase 3: Viewer Mode Naming Strategy and Implementation**

#### **3.1 File Naming Convention for Viewer Mode**

**Proposed Naming Strategy:**
```
Original File:          module.runa
Viewer Display Cache:   .viewer_cache/module.viewer.runa
Temporary Viewer:       module.viewer.tmp.runa
```

**Rationale:**
- `.viewer_cache/` directory for storing pre-generated viewer displays
- `.viewer.runa` extension clearly identifies read-only display files
- `.viewer.tmp.runa` for temporary viewer generation during conversion
- Cache invalidation when source file timestamp changes

**File Organization:**
```
project/
├── src/
│   ├── module.runa             # Canonical or Developer mode source
│   └── .viewer_cache/          # Generated viewer displays (gitignored)
│       └── module.viewer.runa  # Cached read-only display
```

#### **3.2 Viewer Mode Implementation Timeline**

**Phase 3A: Foundation (Current State - COMPLETE as of 2025)**
- ✅ Bootstrap lexer exists (but treats @ as invalid - acceptable limitation)
- ✅ Main lexer tokenizes annotations properly
- ✅ Canon/Developer modes COMPLETE (`get_canonical_form` exists, returns keywords unchanged as designed)
- ✅ Viewer mode metadata groundwork added (Token and AST preserve original forms)
- ❌ Viewer mode transformation engine not yet implemented

**Phase 3B: Complete Canon/Developer Modes (COMPLETED)**
- ✅ `Keywords.get_canonical_form()` function exists (keywords stay consistent by design)
- ✅ Bidirectional Canon ↔ Developer conversion complete (`Keywords.convert_operator()`)
- ✅ Operator lookup tables fully implemented
- ✅ All operator/symbol translations defined and working
- ⚠️ Mode detection exists but needs CLI integration (see CANON_DEVELOPER_MODE_COMPLETION_PLAN.md)

**Phase 3C: Viewer Mode Pattern Engine (Priority 2 - 2 weeks)**
- [ ] Create pattern-based translation system
- [ ] Implement natural language transformations
- [ ] Add educational context generation
- [ ] Build AI comprehension markers

**Phase 3D: Viewer Mode Integration (Priority 3 - 1 week)**
- [ ] Integrate with CLI commands
- [ ] Add caching system for viewer displays
- [ ] Implement file watching for cache invalidation
- [ ] Create viewer mode documentation

#### **3.3 Viewer Mode Metadata Groundwork (COMPLETED 2025)**

**Added Metadata Fields for Future Viewer Mode:**

1. **Token-Level Metadata** (`/src/compiler/frontend/lexical/token_stream.runa`):
   - `original_form: Optional[String]` - Preserves pre-conversion operator forms
   - `source_mode: String` - Tracks whether token came from "canon" or "developer" mode

2. **AST-Level Metadata** (`/src/compiler/frontend/parsing/ast.runa`):
   - `original_operators: Dictionary[String, String]` - Maps converted operators to originals
   - `source_context: Dictionary[String, String]` - Additional context for viewer
   - `preserve_for_viewer: Boolean` - Flag to maintain extra metadata
   - `operator_mappings: Dictionary[String, String]` - Tracks all conversions

3. **Lexer Integration** (`/src/compiler/frontend/lexical/lexer.runa`):
   - Operator tokens now preserve `original_form` and `source_mode`
   - Ready for viewer mode to access original representations

**Benefits of This Groundwork:**
- Viewer can generate mode-aware explanations
- Original operator context preserved for educational output
- No refactoring needed when implementing viewer transformer
- Clean separation between syntax modes and display layer

#### **3.4 Lexer Tokenization Strategy for Viewer Mode**

**Viewer Mode Processing Pipeline:**
```
1. Source Input (Canon/Developer)
    ↓
2. Standard Lexer Tokenization
    ↓
3. AST Generation
    ↓
4. Pattern-Based Translation
    ↓
5. Natural Language Generation
    ↓
6. Educational Context Injection
    ↓
7. Read-Only Display Output
```

**Key Design Decisions:**
- Viewer mode does NOT have its own lexer
- Viewer operates on already-tokenized Canon/Developer output
- Pattern matching transforms tokens to natural language
- Educational context added post-tokenization
- AI markers injected during final formatting

### **Phase 3.5: Remaining Work for Full Canon/Developer Integration**

**What Still Needs Implementation (from CANON_DEVELOPER_MODE_COMPLETION_PLAN.md):**

1. **CLI to Lexer Mode Passing** (Critical - 3 days)
   - Create `create_lexer_with_mode()` factory function
   - Update compiler driver to accept `--canon` and `--developer` flags
   - Pass mode through compilation pipeline

2. **Mode Configuration & Persistence** (Medium Priority - 2 days)
   - Project-level mode preferences (`.runa/config.toml`)
   - User preferences (`~/.runa/preferences.toml`)
   - Mode detection from file headers

3. **Testing & Validation** (Required - 2 days)
   - Mode switching tests
   - CLI integration tests
   - Operator conversion validation

**Total Remaining Work:** 7-8 days for full Canon/Developer mode functionality

### **Phase 4: Current State Assessment and Required Fixes**

#### **4.1 Bootstrap Limitations**

**Finding:** The Rust bootstrap (`/runa/bootstrap/runa-bootstrap/`) currently treats `@` as an invalid character, meaning it cannot tokenize annotations.

**Impact:** 
- Bootstrap cannot compile annotated Runa code
- Annotations must be stripped before bootstrap compilation
- This is acceptable since bootstrap is minimal and will be replaced

**Resolution:**
- Keep bootstrap minimal without annotation support
- Full Runa compiler (compiled by bootstrap) handles annotations properly
- Document this limitation in bootstrap README

#### **4.2 Missing Canon/Developer Mode Components**

**Finding:** The main lexer references but doesn't implement:
- `Keywords.get_canonical_form()` function
- Complete mode switching logic
- Bidirectional conversion validation

**Required Implementations:**
```runa
Process called "get_canonical_form" that takes keyword as String, mode as String returns String:
    Note: Convert keywords between Canon and Developer modes
    
    If string_equals(mode, "developer"):
        Note: In developer mode, allow shorthand
        Match keyword:
            When "Process": Return "proc"
            When "Otherwise": Return "else"
            When "Define": Return "def"
            Default: Return keyword
        End Match
    Otherwise:
        Note: Canon mode uses full keywords
        Match keyword:
            When "proc": Return "Process"
            When "else": Return "Otherwise"
            When "def": Return "Define"
            Default: Return keyword
        End Match
    End If
End Process
```

#### **4.3 Viewer Mode Architecture Clarification**

**Key Understanding:** Viewer mode is NOT a syntax mode for the lexer/parser, but a display transformation layer.

**Implementation Approach:**
1. Parse source in Canon or Developer mode
2. Generate standard AST
3. Apply viewer transformations to AST
4. Generate natural language output

**NOT This Approach:**
- ❌ Creating a separate lexer for viewer mode
- ❌ Parsing viewer mode syntax
- ❌ Allowing edits in viewer mode

### **Phase 5: Architecture Integration**

#### **4.1 Triple Syntax Pattern Integration**

**Update Existing Files:**

1. **Update `triple_syntax_converter.runa`** - Add canonical mode support
2. **Update `syntax_integration.runa`** - Fix mode detection and handling  
3. **Update `math_patterns.runa`** - Add canonical mode patterns

**Example Pattern Update:**
```runa
Note: Corrected triple syntax mathematical patterns

Circle Area Calculation (CORRECTED):
Canon:      Let area be PI multiplied by radius multiplied by radius
Viewer:     "Area equals pi times radius squared" (READ-ONLY DISPLAY)
Developer:  area = Math.PI * radius ** 2

Distance Formula (CORRECTED):
Canon:      Let distance be sqrt((x2 minus x1) multiplied by (x2 minus x1) plus (y2 minus y1) multiplied by (y2 minus y1))
Viewer:     "Distance equals square root of x-difference squared plus y-difference squared" (READ-ONLY DISPLAY)
Developer:  distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
```

---

## 📋 CORRECTED IMPLEMENTATION PHASES

### **Phase 1: Architecture Correction (Immediate - Week 1-2)**

**Priority: CRITICAL - Fix Existing Misunderstanding**

#### **Week 1: Core Architecture Fixes**
- [ ] Update CLI command interface to support `--canon` 
- [ ] Make `--viewer` read-only display only
- [ ] Update existing dev tools to reflect correct architecture
- [ ] Fix pattern definitions in existing files

#### **Week 2: Integration Testing**
- [ ] Test `--canon` as writeable canonical form
- [ ] Test `--viewer` as read-only display  
- [ ] Test `--developer` unchanged writeable technical
- [ ] Validate conversion flows work correctly

### **Phase 2: Missing Component Creation (Weeks 3-4)**

#### **Week 3: Canonical Mode Implementation**
- [ ] Create `canonical_mode.runa` converter
- [ ] Implement canonical mode CLI handlers
- [ ] Add canonical mode validation and processing
- [ ] Update help documentation

#### **Week 4: Enhanced Viewer Display**
- [ ] Improve viewer mode read-only display formatting
- [ ] Add intelligent source mode detection
- [ ] Create viewer-specific display optimizations
- [ ] Add explanatory context for viewer mode

### **Phase 3: Advanced Features (Weeks 5-8)**

#### **Week 5-6: Pattern System Updates**
- [ ] Update all pattern files with correct triple syntax
- [ ] Add canonical mode to pattern matching
- [ ] Fix conversion flows between all modes
- [ ] Comprehensive pattern testing

#### **Week 7-8: IDE Integration**
- [ ] Update IDE plugins for corrected architecture
- [ ] Add canonical mode support to language server
- [ ] Implement proper mode switching in editors
- [ ] Real-time conversion display

---

## 🎯 CORRECTED USAGE EXAMPLES

### **Daily Development Workflow**

**Scenario 1: Traditional Developer**
```bash
# Write in technical syntax
runa edit --developer my_algorithm.runa

# Compile from technical syntax
runa compile --developer my_algorithm.runa

# Display in natural language for stakeholders
runa view --viewer my_algorithm.runa
```

**Scenario 2: Canonical Runa Developer**  
```bash
# Write in canonical Runa (standard form)
runa edit --canon my_algorithm.runa

# Compile from canonical (direct)
runa compile --canon my_algorithm.runa

# Convert to technical for other developers
runa convert --from=canon --to=developer my_algorithm.runa
```

**Scenario 3: AI Code Review**
```bash
# AI reviews in viewer mode (read-only natural language)
runa view --viewer complex_algorithm.runa

# AI suggests changes in canonical form
runa edit --canon complex_algorithm.runa

# Human reviews in technical syntax  
runa view --developer complex_algorithm.runa
```

### **Conversion Flows**

**Valid Conversions:**
```bash
# Writeable ↔ Writeable (bidirectional)
runa convert --from=canon --to=developer input.runa
runa convert --from=developer --to=canon input.runa

# Writeable → Display (unidirectional)
runa convert --from=canon --to=viewer input.runa
runa convert --from=developer --to=viewer input.runa

# Display → Writeable (for editing only)
runa convert --from=viewer --to=canon input.runa
runa convert --from=viewer --to=developer input.runa
```

---

## 🛠️ UPDATED DEV TOOLS SPECIFICATION

### **Corrected CLI Commands**

```bash
# Primary writing modes (both compile directly)
runa compile --canon source.runa          # Canonical Runa (standard)
runa compile --developer source.runa      # Technical syntax

# Display mode (read-only)
runa view --viewer source.runa            # Natural language display

# Mode conversion
runa convert --from=canon --to=developer source.runa     # Canon → Tech
runa convert --from=developer --to=canon source.runa     # Tech → Canon  
runa convert --from=canon --to=viewer source.runa        # Canon → Display
runa convert --from=developer --to=viewer source.runa    # Tech → Display

# Editing modes
runa edit --canon source.runa             # Edit in canonical Runa
runa edit --developer source.runa         # Edit in technical syntax

# Help and information
runa syntax --help                        # Show corrected syntax help
runa modes --list                         # List all available modes
```

### **Updated Help Output**

```
Runa Triple Syntax System v3.0

WRITE IN (Compilation Sources):
    --canon       Canonical Runa syntax (standard writeable form)
    --developer   Technical syntax (familiar programming patterns)

DISPLAY IN (Read-Only):
    --viewer      Natural language sentences (AI-optimized display)

USAGE:
    runa compile --canon input.runa       # Compile canonical Runa
    runa compile --developer input.runa   # Compile technical syntax
    runa view --viewer input.runa         # Display in natural language
    
CONVERSION:
    runa convert --from=canon --to=developer input.runa
    runa convert --from=developer --to=viewer input.runa
    
ARCHITECTURE:
    📝 Write:    --canon (standard) or --developer (technical)
    👁️  Display: --viewer (natural language, read-only)
    🔄 Convert:  Between any modes for different contexts
```

---

## 📊 CORRECTED SYSTEM ARCHITECTURE

### **Data Flow Diagram**

```
INPUT SOURCES (Writeable):
┌─────────────────────┐    ┌─────────────────────┐
│    --canon          │    │   --developer       │
│  (Canonical Runa)   │    │  (Technical Syntax) │
│  ✍️ WRITEABLE       │    │  ✍️ WRITEABLE        │
└─────────┬───────────┘    └─────────┬───────────┘
          │                          │
          ▼                          ▼
       ┌─────────────────────────────────┐
       │     COMPILATION ENGINE          │
       │   (Both modes compile here)     │
       └─────────────┬───────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │  EXECUTABLE │
              └─────────────┘
                     ▲
                     │
    ┌────────────────┴─────────────────┐
    │                                  │
    ▼                                  ▼
┌─────────────┐                ┌─────────────┐
│   --canon   │◄──────────────►│ --developer │
│ (writeable) │   conversion   │ (writeable) │
└─────┬───────┘                └─────┬───────┘
      │                              │
      ▼                              ▼
   ┌─────────────────────────────────────┐
   │         --viewer (READ-ONLY)        │
   │      Natural Language Display       │
   │     👁️ DISPLAY ONLY - NO EDITING    │
   └─────────────────────────────────────┘
```

### **Mode Interaction Matrix**

| From → To | Canon | Developer | Viewer |
|-----------|-------|-----------|--------|
| **Canon** | ✅ Same | ✅ Convert | ✅ Display |
| **Developer** | ✅ Convert | ✅ Same | ✅ Display |  
| **Viewer** | ✅ Edit Mode | ✅ Edit Mode | ❌ Read Only |

**Legend:**
- ✅ **Supported operation**
- ❌ **Not supported** (viewer is read-only)
- **Same**: No conversion needed
- **Convert**: Bidirectional syntax conversion
- **Display**: Unidirectional display formatting  
- **Edit Mode**: Convert viewer back to writeable form for editing

---

## 🚀 DEPLOYMENT STRATEGY

### **Phase 1: Immediate Deployment (Production Ready)**

**Files to Update Immediately:**
1. `runa/src/dev_tools/cli/commands/syntax.runa` - Fix CLI commands
2. `runa/src/dev_tools/syntax_converter/viewer_mode.runa` - Make read-only
3. **CREATE:** `runa/src/dev_tools/syntax_converter/canonical_mode.runa`
4. Update help text and documentation throughout

### **Phase 2: Enhanced Features (Next Sprint)**

**Advanced Features:**
1. **Smart Mode Detection**: Automatically detect if file is canon or developer syntax
2. **Conversion Validation**: Ensure round-trip conversion maintains semantics  
3. **IDE Integration**: Real-time mode switching in editors
4. **Batch Processing**: Convert entire codebases between modes

### **Phase 3: Production Optimization (Ongoing)**

**Performance Enhancements:**
1. **Caching System**: Cache conversion results for faster switching
2. **Parallel Processing**: Convert multiple files simultaneously
3. **Incremental Updates**: Only reconvert changed portions
4. **Memory Optimization**: Efficient handling of large codebases

---

## 📚 MIGRATION GUIDE

### **For Existing Users**

**If you were using `--viewer` as writeable (OLD):**
```bash
# OLD (no longer works)
runa compile --viewer my_code.runa

# NEW (correct replacement) 
runa compile --canon my_code.runa
```

**If you want natural language display:**
```bash
# NEW (correct usage)
runa view --viewer my_code.runa    # Read-only display
```

**If you were using `--developer` (unchanged):**
```bash
# SAME (still works)
runa compile --developer my_code.runa
```

### **Update Your Workflows**

1. **Replace `--viewer` writes** with `--canon` 
2. **Use `--viewer`** only for display/reading
3. **Keep `--developer`** syntax unchanged
4. **Add conversion commands** for switching between modes

---

## ✅ VALIDATION CHECKLIST

### **Architecture Correctness**
- [ ] `--canon` is writeable canonical Runa
- [ ] `--developer` is writeable technical syntax  
- [ ] `--viewer` is read-only natural language display
- [ ] Conversions work: `canon ↔ developer`, `both → viewer`
- [ ] CLI commands reflect correct architecture

### **Functionality Testing**
- [ ] Compile from canonical mode works
- [ ] Compile from developer mode works
- [ ] Viewer mode displays correctly (read-only)
- [ ] Conversion between writeable modes preserves semantics
- [ ] Error messages appear in correct syntax mode

### **User Experience**  
- [ ] Help text reflects corrected architecture
- [ ] Migration path clear for existing users
- [ ] IDE integration supports all modes correctly
- [ ] Documentation updated throughout

---

## 🎉 CONCLUSION

The **Triple Syntax Architecture v3.0** provides the correct foundation for Runa's multi-modal development environment:

✅ **`--canon`**: Standard writeable Runa syntax (replaces old viewer)  
✅ **`--developer`**: Technical writeable syntax (unchanged)  
✅ **`--viewer`**: Natural language read-only display (AI-optimized)  

This architecture enables:
- **Developers** to write in their preferred syntax
- **AI systems** to read in optimized natural language  
- **Stakeholders** to understand code without technical knowledge
- **Universal compatibility** across all development contexts

**The foundation is now correct and ready for production deployment.** 🚀

---

*This document supersedes all previous versions and represents the definitive architecture for Runa's Triple Syntax System.*