# Macro Expansion Engine Module

## Overview

The Macro Expansion Engine provides the core infrastructure for pattern matching, template expansion, and code generation in Runa's macro system. This module handles the complete expansion pipeline from pattern recognition through optimized code generation.

## Key Features

- **Advanced Pattern Matching**: Sophisticated pattern recognition with constraint validation
- **Template Expansion**: Multiple expansion strategies including code and AST templates
- **Variable Binding**: Robust variable extraction, validation, and transformation
- **Optimization Pipeline**: Built-in optimization passes for performance and quality
- **Debug Support**: Comprehensive tracing and debugging capabilities
- **Performance Monitoring**: Real-time metrics and alert system
- **Conditional Expansion**: Support for conditional and branching template logic

## Core Components

### ExpansionEngine

The main orchestrator for all expansion operations.

```runa
Type called "ExpansionEngine":
    context as MacroContext
    pattern_matcher as PatternMatcher
    template_expander as TemplateExpander
    variable_binder as VariableBinder
    expansion_optimizer as ExpansionOptimizer
    debug_tracer as ExpansionDebugTracer
    performance_monitor as ExpansionPerformanceMonitor
    metadata as Dictionary[String, Any]
```

### Core Expansion Types

#### PatternMatcher
Handles pattern recognition and constraint validation:
```runa
Type called "PatternMatcher":
    matchers as Dictionary[String, PatternMatcherFunction]
    constraint_checkers as Dictionary[String, ConstraintCheckerFunction]
    variable_extractors as Dictionary[String, VariableExtractorFunction]
    metadata as Dictionary[String, Any]
```

#### TemplateExpander
Manages template expansion and code generation:
```runa
Type called "TemplateExpander":
    expanders as Dictionary[String, TemplateExpanderFunction]
    variable_substitutors as Dictionary[String, VariableSubstitutorFunction]
    conditional_processors as Dictionary[String, ConditionalProcessorFunction]
    metadata as Dictionary[String, Any]
```

## Main Functions

### Engine Creation and Management

#### create_expansion_engine
```runa
Process called "create_expansion_engine" that takes context as MacroContext returns ExpansionEngine:
    Note: Create a fully configured expansion engine
```

**Parameters:**
- `context` (MacroContext): The macro context containing configuration and registry

**Returns:** ExpansionEngine ready for macro expansion operations

**Example:**
```runa
Import "advanced/macros/expansion" as Expansion
Import "advanced/macros/system" as Macros

Note: Create macro context
Let macro_context be Macros.create_macro_context with config as None

Note: Create expansion engine
Let expansion_engine be Expansion.create_expansion_engine with context as macro_context

Display "Expansion engine created successfully"
Display "Pattern matchers available: " plus length of expansion_engine.pattern_matcher.matchers
Display "Template expanders available: " plus length of expansion_engine.template_expander.expanders
```

### Core Expansion Operations

#### expand_macro_with_engine
```runa
Process called "expand_macro_with_engine" that takes engine as ExpansionEngine and macro_name as String and input_tokens as List[Token] returns ExpansionResult:
    Note: Perform complete macro expansion with debugging and optimization
```

**Parameters:**
- `engine` (ExpansionEngine): The expansion engine to use
- `macro_name` (String): Name of the macro to expand
- `input_tokens` (List[Token]): Input tokens to process

**Returns:** ExpansionResult with success/failure and generated code

**Example:**
```runa
Note: Create input tokens for a debug print macro
Let input_tokens be list containing:
    Expansion.Token with:
        type as "identifier"
        value as "user_score"
        position as Expansion.Position with:
            line as 1
            column as 1
            offset as 0
            metadata as dictionary containing
        metadata as dictionary containing

Note: Expand the macro
Let expansion_result be Expansion.expand_macro_with_engine with 
    engine as expansion_engine 
    and macro_name as "debug_print" 
    and input_tokens as input_tokens

Match expansion_result:
    Case ExpansionSuccess with tokens and ast and performance_metrics:
        Display "Macro expansion successful!"
        Display "Generated " plus length of tokens plus " tokens"
        Display "Expansion time: " plus performance_metrics["expansion_time"] plus "s"
        
        Note: Display generated code
        For each token in tokens:
            Display "  " plus token.type plus ": " plus token.value
            
    Case ExpansionError with error and details:
        Display "Macro expansion failed: " plus error
        If "line" in details:
            Display "Error at line " plus details["line"]
            
    Case ExpansionWarning with warning and tokens and ast:
        Display "Macro expansion succeeded with warning: " plus warning
        Display "Generated " plus length of tokens plus " tokens"
```

### Pattern Matching

#### match_macro_pattern
```runa
Process called "match_macro_pattern" that takes engine as ExpansionEngine and pattern as MacroPattern and tokens as List[Token] returns MatchResult:
    Note: Match input tokens against a macro pattern with constraint validation
```

**Example:**
```runa
Note: Create a pattern for function calls
Let function_pattern be Macros.MacroPattern with:
    syntax as "$function_name($arguments)"
    tokens as list containing
    variables as list containing "function_name", "arguments"
    constraints as list containing:
        Macros.PatternConstraint with:
            constraint_type as "type"
            variable as "function_name"
            condition as "String"
            metadata as dictionary containing
    metadata as dictionary containing

Note: Test pattern matching
Let test_tokens be list containing:
    Expansion.Token with type as "identifier" and value as "print" and position as create_position(1, 1) and metadata as dictionary containing,
    Expansion.Token with type as "delimiter" and value as "(" and position as create_position(1, 6) and metadata as dictionary containing,
    Expansion.Token with type as "string" and value as "Hello World" and position as create_position(1, 7) and metadata as dictionary containing,
    Expansion.Token with type as "delimiter" and value as ")" and position as create_position(1, 20) and metadata as dictionary containing

Let match_result be Expansion.match_macro_pattern with 
    engine as expansion_engine 
    and pattern as function_pattern 
    and tokens as test_tokens

If match_result.matched:
    Display "Pattern matched successfully!"
    Display "Confidence: " plus match_result.confidence
    Display "Function name: " plus match_result.bindings["function_name"]
    Display "Consumed tokens: " plus match_result.consumed_tokens
Otherwise:
    Display "Pattern match failed"
```

### Template Expansion

#### expand_macro_template_with_engine
```runa
Process called "expand_macro_template_with_engine" that takes engine as ExpansionEngine and template as MacroTemplate and bindings as Dictionary[String, Any] returns List[Token]:
    Note: Expand a macro template with variable substitution
```

**Example:**
```runa
Note: Create a template for debug printing
Let debug_template be Macros.MacroTemplate with:
    template_code as "Display \"DEBUG: \" plus {{variable_name}}"
    ast_template as create_debug_ast_template()
    variable_mappings as dictionary containing "variable_name" as "expr"
    conditional_sections as list containing
    metadata as dictionary containing

Note: Create variable bindings
Let variable_bindings be dictionary containing:
    "variable_name" as "user_score"

Note: Expand the template
Let expanded_tokens be Expansion.expand_macro_template_with_engine with 
    engine as expansion_engine 
    and template as debug_template 
    and bindings as variable_bindings

Display "Template expansion completed"
Display "Generated " plus length of expanded_tokens plus " tokens:"
For each token in expanded_tokens:
    Display "  " plus token.type plus ": " plus token.value
```

### Variable Binding and Validation

#### validate_variable_bindings
```runa
Process called "validate_variable_bindings" that takes engine as ExpansionEngine and bindings as Dictionary[String, Any] and macro_def as MacroDefinition returns Optional[Dictionary[String, Any]]:
    Note: Validate and transform variable bindings according to macro definition
```

**Example:**
```runa
Note: Create a macro definition with validation rules
Let validation_macro be Macros.MacroDefinition with:
    name as "typed_debug"
    version as "1.0.0"
    macro_type as "function_like"
    pattern as create_typed_pattern()
    template as create_typed_template()
    hygiene_rules as list containing
    compilation_flags as dictionary containing
    metadata as dictionary containing

Note: Test variable bindings
Let raw_bindings be dictionary containing:
    "variable_name" as "score"
    "variable_type" as "Integer"
    "debug_level" as "info"

Let validated_bindings be Expansion.validate_variable_bindings with 
    engine as expansion_engine 
    and bindings as raw_bindings 
    and macro_def as validation_macro

If validated_bindings is not None:
    Display "Variable validation successful!"
    For each variable in validated_bindings:
        Display "  " plus variable plus " = " plus validated_bindings[variable]
Otherwise:
    Display "Variable validation failed"
```

## Pattern Matching System

### Built-in Pattern Matchers

The expansion engine includes several specialized pattern matchers:

#### Function Call Pattern Matcher
Recognizes function call syntax: `function_name(arguments)`

```runa
Note: Function call pattern matching example
Let function_tokens be create_function_call_tokens("calculate", ["x", "y", "z"])
Let function_pattern be create_function_call_pattern()

Let match_result be Expansion.function_call_pattern_matcher with 
    pattern as function_pattern 
    and tokens as function_tokens

If match_result.matched:
    Display "Function: " plus match_result.bindings["function_name"]
    Display "Arguments: " plus length of match_result.bindings["arguments"]
```

#### Variable Declaration Pattern Matcher
Recognizes Runa variable declarations: `Let variable_name be value`

```runa
Note: Variable declaration pattern matching
Let declaration_tokens be create_variable_declaration_tokens("result", "42")
Let declaration_pattern be create_variable_declaration_pattern()

Let match_result be Expansion.variable_declaration_pattern_matcher with 
    pattern as declaration_pattern 
    and tokens as declaration_tokens

If match_result.matched:
    Display "Variable: " plus match_result.bindings["variable_name"]
    Display "Value tokens: " plus length of match_result.bindings["value_tokens"]
```

#### Control Flow Pattern Matcher
Recognizes control flow statements: `If condition:`, `While condition:`, etc.

```runa
Note: Control flow pattern matching
Let control_tokens be create_control_flow_tokens("If", "x is greater than 10")
Let control_pattern be create_control_flow_pattern()

Let match_result be Expansion.control_flow_pattern_matcher with 
    pattern as control_pattern 
    and tokens as control_tokens

If match_result.matched:
    Display "Control type: " plus match_result.bindings["control_type"]
    Display "Condition tokens: " plus length of match_result.bindings["condition_tokens"]
```

### Pattern Constraints

The system supports various constraint types for pattern validation:

#### Type Constraints
Validate that variables match expected types:
```runa
Let type_constraint be Macros.PatternConstraint with:
    constraint_type as "type"
    variable as "user_input"
    condition as "String"
    metadata as dictionary containing

Note: Test type constraint
Let constraint_valid be Expansion.type_constraint_checker with 
    constraint as type_constraint 
    and value as "Hello World"

If constraint_valid:
    Display "Type constraint satisfied"
```

#### Range Constraints
Validate that numeric values fall within specified ranges:
```runa
Let range_constraint be Macros.PatternConstraint with:
    constraint_type as "range"
    variable as "score"
    condition as "0..100"
    metadata as dictionary containing

Note: Test range constraint
Let range_valid be Expansion.range_constraint_checker with 
    constraint as range_constraint 
    and value as 85

If range_valid:
    Display "Range constraint satisfied"
```

#### Format Constraints
Validate that values match regular expression patterns:
```runa
Let format_constraint be Macros.PatternConstraint with:
    constraint_type as "format"
    variable as "email"
    condition as "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    metadata as dictionary containing

Note: Test format constraint
Let format_valid be Expansion.format_constraint_checker with 
    constraint as format_constraint 
    and value as "user@example.com"

If format_valid:
    Display "Format constraint satisfied"
```

## Template Expansion System

### Expansion Strategies

#### Code Template Expansion
Expands templates using string substitution:
```runa
Let code_template be Macros.MacroTemplate with:
    template_code as "Let {{var_name}} be {{var_value}}"
    ast_template as create_empty_ast()
    variable_mappings as dictionary containing 
        "var_name" as "variable_name",
        "var_value" as "variable_value"
    conditional_sections as list containing
    metadata as dictionary containing

Let bindings be dictionary containing:
    "variable_name" as "result"
    "variable_value" as "42"

Let expanded_tokens be Expansion.code_template_expander with 
    template as code_template 
    and bindings as bindings

Display "Code template expansion result:"
For each token in expanded_tokens:
    Display "  " plus token.value
```

#### AST Template Expansion
Expands templates using abstract syntax tree manipulation:
```runa
Let ast_template be create_variable_declaration_ast("{{var_name}}", "{{var_value}}")

Let expanded_tokens be Expansion.ast_template_expander with 
    template as MacroTemplate with:
        template_code as ""
        ast_template as ast_template
        variable_mappings as dictionary containing
        conditional_sections as list containing
        metadata as dictionary containing
    and bindings as bindings

Display "AST template expansion result:"
For each token in expanded_tokens:
    Display "  " plus token.type plus ": " plus token.value
```

#### Hybrid Template Expansion
Combines code and AST expansion for maximum flexibility:
```runa
Let hybrid_tokens be Expansion.hybrid_template_expander with 
    template as code_template  Note: Template with both code and AST
    and bindings as bindings

Display "Hybrid template expansion result:"
Display "Generated " plus length of hybrid_tokens plus " tokens"
```

### Conditional Expansion

Templates can include conditional sections that are processed based on variable values:

```runa
Let conditional_template be Macros.MacroTemplate with:
    template_code as "Display \"Value: \" plus {{value}}"
    ast_template as create_display_ast()
    variable_mappings as dictionary containing "value" as "variable_value"
    conditional_sections as list containing:
        Macros.ConditionalSection with:
            condition as "debug_mode"
            template_code as "Display \"DEBUG: Processing {{value}}\""
            ast_template as create_debug_display_ast()
            metadata as dictionary containing
    metadata as dictionary containing

Let conditional_bindings be dictionary containing:
    "variable_value" as "test_data"
    "debug_mode" as true

Let conditional_result be Expansion.process_conditional_sections with 
    engine as expansion_engine 
    and template as conditional_template 
    and bindings as conditional_bindings 
    and base_tokens as list containing

Display "Conditional expansion result:"
For each token in conditional_result:
    Display "  " plus token.value
```

## Optimization System

### Built-in Optimizations

#### Constant Folding
Evaluates constant expressions at compile time:
```runa
Note: Example of constant folding optimization
Let unoptimized_expansion be ExpansionSuccess with:
    tokens as list containing:
        create_token("number", "5"),
        create_token("operator", "+"),
        create_token("number", "3"),
        create_token("operator", "*"),
        create_token("number", "2")
    ast as create_empty_ast()
    performance_metrics as dictionary containing

Let optimized_expansion be Expansion.constant_folding_optimizer with expansion as unoptimized_expansion

Match optimized_expansion:
    Case ExpansionSuccess with tokens and ast and performance_metrics:
        Display "Optimization result:"
        For each token in tokens:
            If token.metadata contains "folded" and token.metadata["folded"]:
                Display "  Folded: " plus token.value plus " (was: " plus token.metadata["original_expression"] plus ")"
            Otherwise:
                Display "  Token: " plus token.value
```

#### Complexity Analysis
Analyzes and reports on expansion complexity:
```runa
Let complexity_analysis be Expansion.analyze_expansion with 
    engine as expansion_engine 
    and expansion as optimized_expansion

Display "Expansion Analysis:"
Display "  Complexity: " plus complexity_analysis.complexity
Display "  Performance Impact: " plus complexity_analysis.performance_impact
Display "  Memory Usage: " plus complexity_analysis.memory_usage

If length of complexity_analysis.optimization_opportunities is greater than 0:
    Display "  Optimization Opportunities:"
    For each opportunity in complexity_analysis.optimization_opportunities:
        Display "    - " plus opportunity
```

## Debug and Performance Monitoring

### Debug Tracing

The expansion engine provides comprehensive debug tracing:

```runa
Note: Enable debug tracing
Set expansion_engine.debug_tracer.trace_level to "debug"

Note: Add a debug breakpoint
Let breakpoint_added be Expansion.add_debug_breakpoint with 
    engine as expansion_engine 
    and condition as "macro_name == 'debug_print'" 
    and action as "log_variables"

Note: Perform expansion with tracing
Let traced_result be Expansion.expand_macro_with_engine with 
    engine as expansion_engine 
    and macro_name as "debug_print" 
    and input_tokens as input_tokens

Note: Review trace output
Let trace_entries be Expansion.get_expansion_trace with engine as expansion_engine

Display "Debug Trace (" plus length of trace_entries plus " entries):"
For each entry in trace_entries:
    Display "  [" plus entry.level plus "] " plus entry.message plus " (" plus entry.timestamp plus ")"
    If "macro_name" in entry.data:
        Display "    Macro: " plus entry.data["macro_name"]
    If "expansion_time" in entry.data:
        Display "    Time: " plus entry.data["expansion_time"] plus "s"
```

### Performance Monitoring

Monitor expansion performance in real-time:

```runa
Note: Set performance thresholds
Expansion.set_performance_threshold with 
    engine as expansion_engine 
    and metric as "expansion_time" 
    and threshold as 0.1  Note: 100ms threshold

Expansion.set_performance_threshold with 
    engine as expansion_engine 
    and metric as "memory_usage" 
    and threshold as 1024.0  Note: 1KB threshold

Note: Check performance metrics after expansion
Let performance_metrics be Expansion.get_performance_metrics with engine as expansion_engine

Display "Performance Metrics:"
For each metric_name in performance_metrics:
    Let metric be performance_metrics[metric_name]
    Display "  " plus metric.name plus ": " plus metric.value plus " " plus metric.unit

Note: Check for performance alerts
Let performance_alerts be Expansion.get_performance_alerts with engine as expansion_engine

If length of performance_alerts is greater than 0:
    Display "Performance Alerts:"
    For each alert in performance_alerts:
        Display "  [" plus alert.severity plus "] " plus alert.metric plus 
                ": " plus alert.current_value plus " exceeds threshold " plus alert.threshold
```

## Advanced Usage Examples

### Custom Pattern Matcher
Creating a custom pattern matcher for domain-specific syntax:

```runa
Process called "create_database_query_pattern_matcher" that takes pattern as MacroPattern and tokens as List[Token] returns MatchResult:
    Try:
        Note: Match SQL-like query patterns: SELECT fields FROM table WHERE condition
        If length of tokens is less than 6:
            Return create_failed_match_result()
        
        Let select_token be tokens[0]
        Let fields_tokens be extract_until_keyword(tokens, 1, "FROM")
        Let from_index be find_keyword_index(tokens, "FROM")
        Let table_token be tokens[from_index plus 1]
        Let where_tokens be extract_after_keyword(tokens, "WHERE")
        
        If select_token.value equals "SELECT" and from_index is greater than 0:
            Return MatchResult with:
                matched as true
                bindings as dictionary containing:
                    "fields" as fields_tokens
                    "table" as table_token.value
                    "conditions" as where_tokens
                consumed_tokens as length of tokens
                remaining_tokens as list containing
                confidence as 0.95
                metadata as dictionary containing "pattern_type" as "database_query"
        Otherwise:
            Return create_failed_match_result()
            
    Catch error:
        Return create_failed_match_result()

Note: Register the custom pattern matcher
Set expansion_engine.pattern_matcher.matchers["database_query"] to create_database_query_pattern_matcher
```

### Custom Template Expander
Creating a custom template expander for specialized code generation:

```runa
Process called "create_rest_api_template_expander" that takes template as MacroTemplate and bindings as Dictionary[String, Any] returns List[Token]:
    Try:
        Note: Generate REST API endpoint code
        Let endpoint_name be bindings["endpoint_name"]
        Let method be bindings["method"]
        Let path be bindings["path"]
        
        Let generated_code be "Process called \"" plus endpoint_name plus "\" that takes request as HTTPRequest returns HTTPResponse:\n"
        Set generated_code to generated_code plus "    Note: " plus method plus " " plus path plus "\n"
        Set generated_code to generated_code plus "    Let response_data be handle_" plus endpoint_name plus " with request as request\n"
        Set generated_code to generated_code plus "    Return HTTPResponse with status as 200 and data as response_data"
        
        Let tokens be Expansion.tokenize_code with code as generated_code
        
        Return tokens
        
    Catch error:
        Return list containing Expansion.create_error_token with message as "REST API template expansion failed"

Note: Register the custom template expander
Set expansion_engine.template_expander.expanders["rest_api"] to create_rest_api_template_expander
```

### Integration with System Module
Combining expansion engine with the macro system:

```runa
Note: Create a complete macro with custom expansion
Let api_macro be Macros.MacroDefinition with:
    name as "rest_endpoint"
    version as "1.0.0"
    macro_type as "declarative"
    pattern as Macros.MacroPattern with:
        syntax as "rest_endpoint($method, $path, $handler)"
        tokens as list containing
        variables as list containing "method", "path", "handler"
        constraints as list containing
        metadata as dictionary containing
    template as Macros.MacroTemplate with:
        template_code as "rest_api"  Note: Uses our custom expander
        ast_template as create_empty_ast()
        variable_mappings as dictionary containing 
            "method" as "method",
            "path" as "path",
            "endpoint_name" as "handler"
        conditional_sections as list containing
        metadata as dictionary containing
    hygiene_rules as list containing
    compilation_flags as dictionary containing
    metadata as dictionary containing

Note: Register the macro
Let registration_success be Macros.register_macro with 
    context as macro_context 
    and macro_def as api_macro

Note: Use the macro with the expansion engine
Let api_tokens be list containing:
    create_token("string", "GET"),
    create_token("string", "/users"),
    create_token("identifier", "get_users")

Let api_expansion_result be Expansion.expand_macro_with_engine with 
    engine as expansion_engine 
    and macro_name as "rest_endpoint" 
    and input_tokens as api_tokens

Match api_expansion_result:
    Case ExpansionSuccess with tokens and ast and performance_metrics:
        Display "REST API macro expansion successful!"
        Display "Generated endpoint code:"
        For each token in tokens:
            If token.type equals "newline":
                Display ""
            Otherwise:
                Display token.value
```

## Best Practices

### Pattern Design
1. **Keep patterns specific**: Use constraints to ensure accurate matching
2. **Design for readability**: Choose pattern syntax that's intuitive
3. **Handle edge cases**: Include validation for malformed inputs
4. **Use appropriate matchers**: Choose the right built-in matcher or create custom ones

### Template Optimization
1. **Minimize complexity**: Keep templates simple and focused
2. **Use conditional sections**: Avoid generating unnecessary code
3. **Leverage AST templates**: Use AST expansion for complex code structures
4. **Cache frequently used templates**: Enable caching for performance

### Performance Tuning
1. **Monitor expansion times**: Set appropriate performance thresholds
2. **Enable optimization passes**: Use built-in optimizers
3. **Profile complex macros**: Use debug tracing to identify bottlenecks
4. **Limit recursion depth**: Prevent infinite expansion loops

### Error Handling
1. **Validate inputs**: Always check pattern matching results
2. **Provide meaningful errors**: Include context in error messages
3. **Use defensive programming**: Handle edge cases gracefully
4. **Enable debug tracing**: Use tracing for development and debugging

The macro expansion engine provides the foundation for sophisticated code generation and transformation capabilities in Runa, enabling developers to create powerful domain-specific languages and code generation tools.