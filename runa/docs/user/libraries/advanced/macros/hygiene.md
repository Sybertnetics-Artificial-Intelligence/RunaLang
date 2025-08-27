# Hygiene System Module

## Overview

The Hygiene System module provides comprehensive variable hygiene and scoping management for Runa macros. It prevents variable capture, ensures proper name resolution, and maintains lexical scoping integrity during macro expansion. This system is essential for writing safe, predictable macros that don't interfere with surrounding code.

## Key Features

- **Automatic Variable Hygiene**: Prevents accidental variable capture and name conflicts
- **Lexical Scoping**: Maintains proper scope boundaries during macro expansion
- **Name Mangling**: Intelligent renaming of variables to avoid collisions
- **Scope Isolation**: Complete isolation of macro-generated code from surrounding context
- **Cross-Module Safety**: Ensures hygiene across module boundaries
- **Performance Optimized**: Efficient hygiene checking with minimal runtime overhead
- **Debugging Support**: Rich introspection and debugging capabilities for hygiene issues
- **AI-Friendly**: Clear semantic rules for AI agent interaction

## Core Types

### HygieneSystem
```runa
Type called "HygieneSystem":
    scope_manager as ScopeManager
    name_mangler as NameMangler
    capture_detector as CaptureDetector
    isolation_manager as IsolationManager
    hygiene_rules as List[HygieneRule]
    metadata as Dictionary[String, Any]
```

Main hygiene system coordinator managing all aspects of variable hygiene.

### ScopeManager
```runa
Type called "ScopeManager":
    scope_stack as List[Scope]
    scope_registry as Dictionary[String, Scope]
    current_scope as Optional[Scope]
    parent_scope_map as Dictionary[String, String]
    metadata as Dictionary[String, Any]
```

Manages scope creation, nesting, and resolution during macro expansion.

### HygieneRule
```runa
Type called "HygieneRule":
    rule_id as String
    rule_type as HygieneRuleType
    scope_pattern as String
    variable_pattern as String
    action as HygieneAction
    priority as Integer
    metadata as Dictionary[String, Any]
```

Individual hygiene rule defining how variables should be handled in specific contexts.

## API Reference

### Core Functions

#### create_hygiene_system
```runa
Process called "create_hygiene_system" that takes config as HygieneConfig returns HygieneSystem
```

Creates a new hygiene system with specified configuration.

**Example:**
```runa
Let hygiene_config be HygieneConfig with:
    enable_automatic_hygiene as true
    enable_name_mangling as true
    enable_scope_isolation as true
    enable_capture_detection as true
    mangle_prefix as "hygienic_"
    metadata as dictionary containing

Let hygiene_system be create_hygiene_system with config as hygiene_config

Note: Hygiene system is ready for macro processing
```

#### apply_hygiene
```runa
Process called "apply_hygiene" that takes system as HygieneSystem and macro_expansion as MacroExpansion returns HygienicExpansion
```

Applies hygiene rules to a macro expansion, ensuring variable safety.

**Example:**
```runa
Note: Define a macro that could cause variable capture
Let unsafe_macro_code be "
Let x be 10
Process called \"dangerous_macro\" that takes value as Integer returns Integer:
    Let x be value plus 1  // This could capture outer 'x'
    Return x
"

Note: Apply hygiene to prevent capture
Let expansion be MacroExpansion with:
    original_code as unsafe_macro_code
    variables as dictionary containing "value" as 5
    scope_context as current_scope
    metadata as dictionary containing

Let safe_expansion be apply_hygiene with:
    system as hygiene_system
    macro_expansion as expansion

Note: Result has hygienic variable names that don't conflict
```

#### check_hygiene_violations
```runa
Process called "check_hygiene_violations" that takes system as HygieneSystem and code as String and scope as Scope returns List[HygieneViolation]
```

Analyzes code for potential hygiene violations before macro expansion.

**Example:**
```runa
Let potentially_unsafe_code be "
Let user_id be 42
macro generate_user_query:
    Let user_id be get_current_user_id  // Potential capture
    Return \"SELECT * FROM users WHERE id = \" plus user_id
"

Let violations be check_hygiene_violations with:
    system as hygiene_system
    code as potentially_unsafe_code
    scope as current_scope

For each violation in violations:
    Print "Hygiene violation: " plus violation.description
    Print "Suggested fix: " plus violation.suggested_fix
```

### Scope Management

#### create_hygienic_scope
```runa
Process called "create_hygienic_scope" that takes system as HygieneSystem and parent as Optional[Scope] returns Scope
```

Creates a new hygienic scope with proper isolation from parent scopes.

**Example:**
```runa
Note: Create isolated scope for macro expansion
Let parent_scope be get_current_scope
Let macro_scope be create_hygienic_scope with:
    system as hygiene_system
    parent as parent_scope

Note: Variables in macro_scope won't interfere with parent_scope
```

#### enter_scope
```runa
Process called "enter_scope" that takes system as HygieneSystem and scope as Scope returns Boolean
```

Enters a scope, making it the current active scope for variable resolution.

**Example:**
```runa
Let scope_entered be enter_scope with system as hygiene_system and scope as macro_scope

Note: All variable declarations now go into macro_scope
Let hygienic_var be declare_variable with name as "temp_var" and value as 100

Let scope_exited be exit_scope with system as hygiene_system
Note: Back to parent scope
```

### Name Mangling

#### mangle_variable_name
```runa
Process called "mangle_variable_name" that takes system as HygieneSystem and original_name as String and scope_id as String returns String
```

Generates a hygienic name for a variable to prevent conflicts.

**Example:**
```runa
Let original_name be "counter"
Let current_scope_id be get_current_scope_id with system as hygiene_system

Let mangled_name be mangle_variable_name with:
    system as hygiene_system
    original_name as original_name
    scope_id as current_scope_id

Note: mangled_name might be "hygienic_counter_scope_123_var_456"
```

#### unmangle_variable_name
```runa
Process called "unmangle_variable_name" that takes system as HygieneSystem and mangled_name as String returns String
```

Extracts the original variable name from a mangled name.

**Example:**
```runa
Let original be unmangle_variable_name with:
    system as hygiene_system
    mangled_name as "hygienic_counter_scope_123_var_456"

Note: original is "counter"
```

## Hygiene Patterns

### Variable Capture Prevention
```runa
Note: Macro that safely uses local variables
macro safe_counter:
    Note: These variables are automatically made hygienic
    Let count be 0
    Let increment be 1
    
    Process called "increment_counter" returns Integer:
        Set count to count plus increment
        Return count

Note: Generated code uses mangled names to prevent capture
```

### Scope Isolation
```runa
Note: Macro with complete scope isolation
macro isolated_computation that takes input as Integer:
    Note: Create isolated scope for all variables
    Let isolated_scope be create_hygienic_scope with system as hygiene_system and parent as None
    Let scope_entered be enter_scope with system as hygiene_system and scope as isolated_scope
    
    Note: All variables are isolated from outer scope
    Let temp_result be input multiplied by 2
    Let temp_squared be temp_result multiplied by temp_result
    Let final_result be temp_squared plus 1
    
    Let scope_exited be exit_scope with system as hygiene_system
    Return final_result
```

### Cross-Module Hygiene
```runa
Note: Macro that works safely across module boundaries
macro cross_module_safe that imports module_a and module_b:
    Note: Ensure hygiene across module boundaries
    Let module_scope be create_cross_module_scope with:
        system as hygiene_system
        modules as list containing module_a, module_b
    
    Let scope_entered be enter_scope with system as hygiene_system and scope as module_scope
    
    Note: Use qualified names to prevent conflicts
    Let result_a be module_a.calculate_value
    Let result_b be module_b.calculate_value
    Let combined be result_a plus result_b
    
    Let scope_exited be exit_scope with system as hygiene_system
    Return combined
```

## Idiomatic Usage

### Building Hygienic Macros
```runa
Note: Template for creating hygienic macros
macro hygienic_template that takes parameters:
    Note: Step 1: Create isolated scope
    Let macro_scope be create_hygienic_scope with:
        system as global_hygiene_system
        parent as get_current_scope
    
    Let scope_entered be enter_scope with:
        system as global_hygiene_system
        scope as macro_scope
    
    Note: Step 2: Declare hygienic variables
    Let hygienic_vars be declare_hygienic_variables with:
        system as global_hygiene_system
        variables as list containing "temp", "result", "intermediate"
    
    Note: Step 3: Generate code using hygienic variables
    Let temp be initial_computation with parameters as parameters
    Let intermediate be process_temp with value as temp
    Let result be finalize_computation with value as intermediate
    
    Note: Step 4: Exit scope and return result
    Let scope_exited be exit_scope with system as global_hygiene_system
    Return result
```

### Advanced Hygiene Rules
```runa
Note: Define custom hygiene rules for domain-specific needs
Let custom_hygiene_rule be HygieneRule with:
    rule_id as "database_variable_hygiene"
    rule_type as VariableCapture
    scope_pattern as "database_macro_*"
    variable_pattern as "(connection|cursor|result)_.*"
    action as HygieneAction with:
        action_type as Qualify
        namespace as "db_hygienic"
    priority as 10
    metadata as dictionary containing:
        "description" as "Ensures database variables don't conflict"
        "domain" as "database_operations"

Let rule_added be add_hygiene_rule with:
    system as hygiene_system
    rule as custom_hygiene_rule

Note: Database macros now use qualified names automatically
```

### Hygiene Debugging
```runa
Note: Debug hygiene issues during development
Let hygiene_debugger be create_hygiene_debugger with system as hygiene_system

Let debug_session be start_hygiene_debug with:
    debugger as hygiene_debugger
    macro_code as potentially_problematic_macro
    input_scope as current_scope

Note: Step through hygiene application
Let step_result be step_hygiene_application with debugger as hygiene_debugger
While not step_result.is_complete:
    Print "Current step: " plus step_result.description
    Print "Variables: " plus step_result.variable_state
    Print "Scope: " plus step_result.scope_info
    
    Let step_result be step_hygiene_application with debugger as hygiene_debugger

Print "Final hygienic code: " plus step_result.final_code
```

## Comparative Notes

### vs. Lisp Hygiene
- **Runa**: Automatic hygiene with configurable rules
- **Lisp**: Manual gensym and explicit hygiene
- **Advantage**: Reduced boilerplate and better safety by default

### vs. Rust Hygiene
- **Runa**: Cross-module hygiene and dynamic scoping support
- **Rust**: Compile-time only hygiene
- **Advantage**: Better runtime flexibility and debugging

### vs. Scheme Syntax-Case
- **Runa**: Integrated with type system and module system
- **Scheme**: Syntax-focused hygiene
- **Advantage**: Broader scope safety and better tooling integration

## Performance Considerations

### Hygiene Caching
```runa
Note: Cache hygiene decisions for repeated patterns
Let hygiene_cache be create_hygiene_cache with:
    max_entries as 10000
    cache_strategy as "LRU"
    enable_pattern_matching as true

Let cached_system be create_hygiene_system with:
    config as hygiene_config
    cache as hygiene_cache

Note: Repeated hygiene operations are served from cache
```

### Lazy Hygiene Application
```runa
Note: Apply hygiene only when needed
Let lazy_hygiene_config be HygieneConfig with:
    enable_lazy_application as true
    defer_until_expansion as true
    batch_hygiene_operations as true

Let lazy_system be create_hygiene_system with config as lazy_hygiene_config

Note: Hygiene rules are applied only during actual macro expansion
```

### Memory Management
```runa
Note: Efficient memory usage for large codebases
Let memory_config be HygieneMemoryConfig with:
    enable_scope_pooling as true
    max_concurrent_scopes as 1000
    enable_garbage_collection as true
    gc_threshold as 500

Let memory_efficient_system be create_hygiene_system with:
    config as hygiene_config
    memory_config as memory_config
```

## Error Handling

### Hygiene Violation Detection
```runa
Note: Detect and report hygiene violations
Let violation_detector be create_violation_detector with system as hygiene_system

Let violations be detect_violations with:
    detector as violation_detector
    code as macro_code
    scope as current_scope

For each violation in violations:
    Match violation.severity:
        When "error":
            Note: Critical hygiene violation that must be fixed
            Print "ERROR: " plus violation.message
            Print "Location: " plus violation.location
            Print "Fix: " plus violation.suggested_fix
        When "warning":
            Note: Potential hygiene issue
            Print "WARNING: " plus violation.message
        When "info":
            Note: Informational hygiene note
            Print "INFO: " plus violation.message
```

### Automatic Hygiene Repair
```runa
Note: Automatically fix common hygiene issues
Let hygiene_repairer be create_hygiene_repairer with system as hygiene_system

Let repair_result be repair_hygiene_violations with:
    repairer as hygiene_repairer
    code as problematic_code
    violations as detected_violations

Match repair_result:
    When RepairSuccess with repaired_code as fixed_code:
        Print "Successfully repaired hygiene violations"
        Print "Repaired code: " plus fixed_code
    When RepairFailure with errors as repair_errors:
        Print "Unable to automatically repair hygiene violations"
        For each error in repair_errors:
            Print "Manual fix required: " plus error.description
```

## Integration Examples

### With Macro Expansion
```runa
Note: Integrate hygiene with macro expansion pipeline
Let expansion_pipeline be create_expansion_pipeline with:
    hygiene_system as hygiene_system
    enable_automatic_hygiene as true
    hygiene_checking_level as "strict"

Let macro_result be expand_macro_with_hygiene with:
    pipeline as expansion_pipeline
    macro_name as "complex_macro"
    input_tokens as input_tokens
    expansion_context as current_context

Note: Expansion includes automatic hygiene application
```

### With IDE Support
```runa
Note: Provide hygiene information to IDEs
Let ide_hygiene_provider be create_ide_hygiene_provider with system as hygiene_system

Let hygiene_info be get_hygiene_info_for_ide with:
    provider as ide_hygiene_provider
    code_position as cursor_position
    surrounding_code as editor_context

Note: IDE can show hygiene status and variable mappings
```

### With Static Analysis
```runa
Note: Integration with static analysis tools
Let static_analyzer be create_static_analyzer with hygiene_system as hygiene_system

Let analysis_result be analyze_hygiene_safety with:
    analyzer as static_analyzer
    codebase as project_codebase
    analysis_level as "comprehensive"

Note: Comprehensive hygiene analysis across entire codebase
```

## Production Examples

### Enterprise Macro Hygiene
```runa
Note: Configure hygiene for large-scale enterprise development
Let enterprise_hygiene_config be HygieneConfig with:
    enable_automatic_hygiene as true
    enable_cross_module_checking as true
    enable_third_party_hygiene as true
    hygiene_reporting_level as "detailed"
    enable_hygiene_metrics as true
    enable_continuous_monitoring as true
    compliance_mode as "strict"
    audit_trail_enabled as true

Let enterprise_system be create_hygiene_system with config as enterprise_hygiene_config

Note: Set up hygiene monitoring
Let hygiene_monitor be create_hygiene_monitor with:
    system as enterprise_system
    alert_thresholds as dictionary containing:
        "violation_rate" as 0.01
        "capture_incidents" as 0
        "scope_leaks" as 0
    reporting_interval as 3600  // 1 hour

Let monitoring_started be start_hygiene_monitoring with monitor as hygiene_monitor
```

### Multi-Language Hygiene
```runa
Note: Hygiene system for multi-language code generation
Let multilang_hygiene_system be create_multilanguage_hygiene_system with:
    target_languages as list containing "runa", "javascript", "python", "rust"
    language_specific_rules as dictionary containing:
        "javascript" as js_hygiene_rules
        "python" as python_hygiene_rules
        "rust" as rust_hygiene_rules
    cross_language_safety as true

Let multilang_expansion be expand_multilanguage_macro with:
    hygiene_system as multilang_hygiene_system
    macro_definition as cross_lang_macro
    target_language as "javascript"

Note: Generated JavaScript code follows JS naming conventions while maintaining hygiene
```

### Legacy Code Hygiene Migration
```runa
Note: Migrate legacy macros to hygienic versions
Let migration_tool be create_hygiene_migration_tool with:
    source_system as legacy_macro_system
    target_system as modern_hygiene_system
    migration_strategy as "gradual"
    compatibility_mode as true

Let migration_plan be analyze_migration_requirements with:
    tool as migration_tool
    legacy_codebase as old_macro_codebase

Let migration_result be execute_hygiene_migration with:
    tool as migration_tool
    plan as migration_plan
    validation_enabled as true

Note: Legacy macros are gradually converted to hygienic versions
```

## Related Modules

- [**Macro System Core**](./system.md) - Core macro infrastructure
- [**Macro Expansion**](./expansion.md) - Macro expansion pipeline
- [**Code Generation**](./code_generation.md) - Template-based code generation
- [**Syntax Extensions**](./syntax_extensions.md) - Custom syntax definitions
- [**Production System**](./production_system.md) - Enterprise-grade processing