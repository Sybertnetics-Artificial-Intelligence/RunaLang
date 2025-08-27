# Syntax Extensions Module

## Overview

The Syntax Extensions module enables the creation of custom syntax constructs that extend the Runa language in powerful ways. It provides a framework for defining new operators, control structures, literals, and language constructs while maintaining full integration with the Runa parser, type system, and tooling ecosystem.

## Key Features

- **Custom Operators**: Define new infix, prefix, and postfix operators with custom precedence
- **Control Flow Extensions**: Create new control structures and loop constructs
- **Literal Extensions**: Add support for new literal types and formats
- **Syntax Sugar**: Define convenient syntax shortcuts for common patterns
- **Parser Integration**: Seamless integration with the Runa parser and AST
- **Type System Integration**: Full support for type checking and inference
- **IDE Support**: Automatic syntax highlighting and error reporting
- **Extensible Architecture**: Plugin system for complex syntax extensions

## Core Types

### SyntaxExtension
```runa
Type called "SyntaxExtension":
    extension_id as String
    extension_name as String
    extension_type as SyntaxExtensionType
    grammar_rules as List[GrammarRule]
    transformation_rules as List[TransformationRule]
    precedence_info as PrecedenceInfo
    type_rules as List[TypeRule]
    metadata as Dictionary[String, Any]
```

Complete definition of a syntax extension including grammar, transformations, and type information.

### SyntaxExtensionType
```runa
Type SyntaxExtensionType is:
    | OperatorExtension with operator_type as OperatorType
    | ControlFlowExtension with flow_type as String
    | LiteralExtension with literal_type as String
    | SyntaxSugarExtension with sugar_type as String
    | CompositeExtension with components as List[SyntaxExtensionType]
```

Different categories of syntax extensions supported by the system.

### GrammarRule
```runa
Type called "GrammarRule":
    rule_name as String
    pattern as String
    production as String
    precedence as Integer
    associativity as Associativity
    context_requirements as List[String]
    metadata as Dictionary[String, Any]
```

Grammar rule defining how the extension should be parsed.

## API Reference

### Core Functions

#### create_syntax_extension
```runa
Process called "create_syntax_extension" that takes definition as SyntaxExtensionDefinition returns SyntaxExtension
```

Creates a new syntax extension from a definition.

**Example:**
```runa
Note: Define a pipeline operator like in F# or Elixir
Let pipeline_definition be SyntaxExtensionDefinition with:
    extension_id as "pipeline_operator"
    extension_name as "Pipeline Operator"
    extension_type as OperatorExtension with:
        operator_type as InfixOperator
    grammar_rules as list containing:
        GrammarRule with:
            rule_name as "pipeline_expression"
            pattern as "expression '|>' expression"
            production as "apply_pipeline"
            precedence as 1
            associativity as LeftAssociative
            context_requirements as list containing
            metadata as dictionary containing
    transformation_rules as list containing:
        TransformationRule with:
            rule_name as "pipeline_transform"
            pattern as "{{left}} |> {{right}}"
            replacement as "{{right}} with input as {{left}}"
            metadata as dictionary containing
    metadata as dictionary containing

Let pipeline_extension be create_syntax_extension with definition as pipeline_definition

Note: Pipeline operator is now available for use
```

#### register_syntax_extension
```runa
Process called "register_syntax_extension" that takes extension as SyntaxExtension and parser as Parser returns Boolean
```

Registers a syntax extension with the Runa parser.

**Example:**
```runa
Let parser be get_global_runa_parser
Let registered be register_syntax_extension with:
    extension as pipeline_extension
    parser as parser

Note: Parser now recognizes the |> operator
Let code be "list containing 1, 2, 3 |> map with f |> filter with predicate |> reduce with combiner"
Let parsed_ast be parse_with_extensions with parser as parser and code as code
```

#### apply_syntax_transformations
```runa
Process called "apply_syntax_transformations" that takes ast as AST and extensions as List[SyntaxExtension] returns AST
```

Applies syntax extension transformations to an AST.

**Example:**
```runa
Note: Transform pipeline syntax to standard function calls
Let original_ast be parse_code with code as "data |> process |> validate"
Let transformed_ast be apply_syntax_transformations with:
    ast as original_ast
    extensions as list containing pipeline_extension

Note: Transformed AST represents: validate with input as (process with input as data)
```

### Operator Extensions

#### define_infix_operator
```runa
Process called "define_infix_operator" that takes symbol as String and precedence as Integer and associativity as Associativity and transformation as String returns SyntaxExtension
```

Defines a new infix operator.

**Example:**
```runa
Note: Define a composition operator (like in Haskell)
Let compose_operator be define_infix_operator with:
    symbol as "∘"
    precedence as 8
    associativity as RightAssociative
    transformation as "compose_functions({{left}}, {{right}})"

Let registered be register_syntax_extension with:
    extension as compose_operator
    parser as global_parser

Note: Now can write: f ∘ g ∘ h
Let composed_function be square ∘ increment ∘ double
```

#### define_prefix_operator
```runa
Process called "define_prefix_operator" that takes symbol as String and precedence as Integer and transformation as String returns SyntaxExtension
```

Defines a new prefix operator.

**Example:**
```runa
Note: Define a negation operator for predicates
Let not_operator be define_prefix_operator with:
    symbol as "¬"
    precedence as 10
    transformation as "negate_predicate({{operand}})"

Note: Usage: ¬is_valid instead of not is_valid
Let invalid_check be ¬is_valid_user
```

#### define_postfix_operator
```runa
Process called "define_postfix_operator" that takes symbol as String and precedence as Integer and transformation as String returns SyntaxExtension
```

Defines a new postfix operator.

**Example:**
```runa
Note: Define factorial operator
Let factorial_operator be define_postfix_operator with:
    symbol as "!"
    precedence as 12
    transformation as "factorial({{operand}})"

Note: Usage: 5! instead of factorial(5)
Let result be 5!  // Equivalent to factorial(5)
```

### Control Flow Extensions

#### define_control_structure
```runa
Process called "define_control_structure" that takes name as String and pattern as String and transformation as String returns SyntaxExtension
```

Defines a new control flow structure.

**Example:**
```runa
Note: Define a unless statement (opposite of if)
Let unless_structure be define_control_structure with:
    name as "unless"
    pattern as "'unless' condition statement"
    transformation as "if not ({{condition}}) then {{statement}}"

Note: Usage: unless user.is_admin: deny_access()
unless user.is_admin:
    deny_access
    log_unauthorized_attempt
```

#### define_loop_structure
```runa
Process called "define_loop_structure" that takes name as String and pattern as String and transformation as String returns SyntaxExtension
```

Defines a new loop construct.

**Example:**
```runa
Note: Define a repeat-until loop
Let repeat_until_loop be define_loop_structure with:
    name as "repeat_until"
    pattern as "'repeat' block 'until' condition"
    transformation as "do { {{block}} } while not ({{condition}})"

Note: Usage:
repeat:
    Let input be get_user_input
    process_input with input as input
until input equals "quit"
```

### Literal Extensions

#### define_literal_type
```runa
Process called "define_literal_type" that takes type_name as String and pattern as String and parser_function as String returns SyntaxExtension
```

Defines a new literal type with custom parsing.

**Example:**
```runa
Note: Define regex literals
Let regex_literal be define_literal_type with:
    type_name as "Regex"
    pattern as "r\"[^\"]*\""
    parser_function as "parse_regex_literal"

Note: Usage: r"\\d{3}-\\d{2}-\\d{4}" for SSN pattern
Let ssn_pattern be r"\\d{3}-\\d{2}-\\d{4}"
Let is_valid_ssn be ssn_pattern.matches with text as user_input
```

#### define_numeric_literal
```runa
Process called "define_numeric_literal" that takes format_name as String and pattern as String and converter as String returns SyntaxExtension
```

Defines a new numeric literal format.

**Example:**
```runa
Note: Define binary and hexadecimal literals
Let binary_literal be define_numeric_literal with:
    format_name as "binary"
    pattern as "0b[01]+"
    converter as "parse_binary"

Let hex_literal be define_numeric_literal with:
    format_name as "hexadecimal"
    pattern as "0x[0-9a-fA-F]+"
    converter as "parse_hex"

Note: Usage:
Let binary_value be 0b1010_1100  // 172 in decimal
Let hex_value be 0xFF_A0        // 65,440 in decimal
```

## Syntax Extension Examples

### Mathematical Notation
```runa
Note: Define mathematical notation extensions
Let summation_extension be define_control_structure with:
    name as "summation"
    pattern as "'Σ' '(' variable 'from' start 'to' end ')' expression"
    transformation as "sum_range({{start}}, {{end}}, lambda {{variable}}: {{expression}})"

Let product_extension be define_control_structure with:
    name as "product"
    pattern as "'Π' '(' variable 'from' start 'to' end ')' expression"
    transformation as "product_range({{start}}, {{end}}, lambda {{variable}}: {{expression}})"

Note: Usage:
Let sum_of_squares be Σ(i from 1 to 10) i * i
Let factorial_10 be Π(i from 1 to 10) i
```

### Query Syntax
```runa
Note: Define SQL-like query syntax for collections
Let query_extension be define_control_structure with:
    name as "query"
    pattern as "'from' variable 'in' collection ('where' condition)? ('select' projection)? ('orderby' ordering)?"
    transformation as "query_collection({{collection}}, {{variable}}, {{condition}}, {{projection}}, {{ordering}})"

Note: Usage:
Let adult_names be from user in users 
                   where user.age >= 18 
                   select user.name 
                   orderby user.name
```

### Pattern Matching Extensions
```runa
Note: Define advanced pattern matching syntax
Let pattern_extension be define_control_structure with:
    name as "pattern_match"
    pattern as "'match' expression 'with' '|' pattern_cases"
    transformation as "pattern_match_expression({{expression}}, {{pattern_cases}})"

Note: Usage:
Let result be match user_input with
    | r"\\d+" -> parse_number with text as user_input
    | r"[a-zA-Z]+" -> parse_word with text as user_input
    | _ -> InvalidInput
```

## Idiomatic Usage

### Building Domain-Specific Syntax
```runa
Note: Create syntax for state machine definitions
Let state_machine_syntax be create_composite_extension with:
    name as "state_machine_syntax"
    components as list containing:
        define_control_structure with:
            name as "state_definition"
            pattern as "'state' identifier '{' state_body '}'"
            transformation as "define_state({{identifier}}, {{state_body}})"
        define_control_structure with:
            name as "transition_definition"
            pattern as "state_id '->' state_id 'on' event"
            transformation as "define_transition({{state_id}}, {{target_id}}, {{event}})"
        define_operator with:
            symbol as "->"
            precedence as 3
            transformation as "transition_operator"

Note: Usage:
state idle {
    entry: initialize_system
    exit: cleanup_temporary_data
}

state processing {
    entry: start_processing
    action: process_current_item
    exit: finalize_processing
}

idle -> processing on start_event
processing -> idle on complete_event
```

### API Definition Syntax
```runa
Note: Create REST API definition syntax
Let api_syntax be create_composite_extension with:
    name as "api_definition_syntax"
    components as list containing:
        define_control_structure with:
            name as "endpoint_definition"
            pattern as "method path ('(' parameters ')')? ('returns' return_type)?"
            transformation as "define_endpoint"
        define_literal_type with:
            type_name as "HttpMethod"
            pattern as "GET|POST|PUT|DELETE|PATCH"
            parser_function as "parse_http_method"
        define_literal_type with:
            type_name as "Path"
            pattern as "\"/[^\"]*\""
            parser_function as "parse_api_path"

Note: Usage:
GET "/users" returns List[User]
POST "/users" (user_data as CreateUserRequest) returns User
PUT "/users/{id}" (id as Integer, update_data as UpdateUserRequest) returns User
DELETE "/users/{id}" (id as Integer) returns Boolean
```

### Configuration Syntax
```runa
Note: Define configuration file syntax
Let config_syntax be create_composite_extension with:
    name as "configuration_syntax"
    components as list containing:
        define_control_structure with:
            name as "section_definition"
            pattern as "'[' identifier ']' config_items"
            transformation as "create_config_section"
        define_operator with:
            symbol as "="
            precedence as 1
            transformation as "config_assignment"
        define_literal_type with:
            type_name as "ConfigValue"
            pattern as "\"[^\"]*\"|[0-9]+|true|false|\\[[^\\]]*\\]"
            parser_function as "parse_config_value"

Note: Usage:
[database]
host = "localhost"
port = 5432
pool_size = 10
ssl_enabled = true
replicas = ["server1", "server2", "server3"]

[logging]
level = "INFO"
file = "/var/log/app.log"
rotation = true
```

## Comparative Notes

### vs. Scala Operator Overloading
- **Runa**: Syntax extensions with parser integration
- **Scala**: Method-based operator overloading only
- **Advantage**: True syntax extension beyond just operators

### vs. Haskell Infix Operators
- **Runa**: Dynamic registration with precedence control
- **Haskell**: Fixed precedence for custom operators
- **Advantage**: More flexible precedence management

### vs. Nim Templates
- **Runa**: Type-safe syntax extensions with validation
- **Nim**: Template-based syntax transformation
- **Advantage**: Better type safety and error reporting

## Performance Considerations

### Parser Optimization
```runa
Note: Syntax extensions are compiled for performance
Let optimized_extensions be compile_syntax_extensions with:
    extensions as registered_extensions
    optimization_level as "aggressive"
    enable_caching as true

Note: Compiled extensions parse as fast as native syntax
```

### Extension Caching
```runa
Note: Cache parsed extension results
Let extension_cache be create_extension_cache with:
    max_entries as 10000
    cache_strategy as "LRU"
    enable_pattern_caching as true

Let cached_parser be create_parser_with_cache with:
    extensions as syntax_extensions
    cache as extension_cache
```

### Memory Management
```runa
Note: Efficient memory usage for extension ASTs
Let memory_config be ExtensionMemoryConfig with:
    enable_ast_pooling as true
    max_extension_nodes as 100000
    enable_lazy_evaluation as true

Let parser be create_extension_parser with:
    extensions as extensions
    memory_config as memory_config
```

## Error Handling

### Extension Conflicts
```runa
Note: Handle conflicts between syntax extensions
Let conflict_resolver be create_extension_conflict_resolver

Let resolution_result be resolve_extension_conflicts with:
    resolver as conflict_resolver
    extensions as conflicting_extensions

Match resolution_result:
    When ConflictResolved with resolved_extensions as resolved:
        Note: Conflicts automatically resolved
        Let parser be create_parser with extensions as resolved
    When ConflictUnresolvable with conflicts as unresolvable:
        Note: Manual resolution required
        For each conflict in unresolvable:
            Print "Conflict: " plus conflict.description
            Print "Suggestions: " plus conflict.resolution_suggestions
```

### Syntax Validation
```runa
Note: Validate syntax extensions before registration
Let validator be create_syntax_extension_validator

Let validation_result be validate_syntax_extension with:
    validator as validator
    extension as new_extension

Match validation_result:
    When ValidationSuccess:
        Let registered be register_syntax_extension with extension as new_extension
    When ValidationError with errors as validation_errors:
        For each error in validation_errors:
            Print "Validation error: " plus error.message
            Print "Location: " plus error.location
            Print "Suggestion: " plus error.suggestion
```

## Integration Examples

### With Macro System
```runa
Note: Syntax extensions that generate macros
Let macro_generating_extension be define_control_structure with:
    name as "auto_property"
    pattern as "'property' identifier ':' type_name"
    transformation as "generate_property_macro({{identifier}}, {{type_name}})"

Note: Usage generates getter/setter macros
property name: String
property age: Integer

Note: Expands to:
Note: private _name as String
Note: process get_name returns String: return _name
Note: process set_name that takes value as String: set _name to value
```

### With Type System
```runa
Note: Syntax extensions with custom type checking
Let typed_extension be create_typed_syntax_extension with:
    name as "safe_cast"
    pattern as "expression 'as?' type_name"
    type_checker as safe_cast_type_checker
    transformation as "safe_cast_expression"

Note: Usage with type safety
Let user be user_data as? User  // Returns Optional[User]
Match user:
    When Some with value as u:
        process_user with user as u
    When None:
        handle_invalid_user_data
```

### With IDE Support
```runa
Note: Register extensions for IDE integration
Let ide_support be register_extensions_with_ide with:
    extensions as all_syntax_extensions
    language_server as runa_language_server

Note: IDE now provides:
Note: - Syntax highlighting for extensions
Note: - Autocompletion for extension keywords
Note: - Error detection for extension syntax
Note: - Refactoring support for extensions
```

## Production Examples

### Enterprise DSL Framework
```runa
Note: Complete framework for enterprise DSLs
Let enterprise_dsl_framework be create_enterprise_dsl_framework with:
    supported_domains as list containing "business_rules", "workflows", "apis", "configurations"
    security_level as "enterprise"
    compliance_features as list containing "audit_trail", "access_control", "validation"
    integration_points as list containing "ide", "ci_cd", "monitoring"

Note: Register domain-specific extensions
Let business_rules_extensions be load_business_rules_extensions
Let workflow_extensions be load_workflow_extensions
Let api_extensions be load_api_extensions

Let framework_initialized be initialize_enterprise_framework with:
    framework as enterprise_dsl_framework
    extensions as list containing business_rules_extensions, workflow_extensions, api_extensions
```

### Multi-Language Syntax Bridge
```runa
Note: Bridge syntax from other languages
Let syntax_bridge be create_multi_language_syntax_bridge with:
    source_languages as list containing "python", "javascript", "rust", "go"
    enable_syntax_migration as true
    enable_gradual_adoption as true

Note: Import Python-style comprehensions
Let python_comprehensions be import_syntax_from_language with:
    bridge as syntax_bridge
    source_language as "python"
    syntax_features as list containing "list_comprehensions", "dict_comprehensions"

Note: Now can use: [x * 2 for x in range(10) if x % 2 == 0]
Let even_doubles be [x * 2 for x in range(10) if x % 2 == 0]
```

### Plugin Architecture for Extensions
```runa
Note: Plugin system for third-party syntax extensions
Let extension_plugin_system be create_extension_plugin_system with:
    security_sandbox as true
    plugin_verification as true
    hot_reload_support as true
    version_management as true

Let plugin_registry be create_plugin_registry with system as extension_plugin_system

Note: Load third-party extensions safely
Let loaded_plugins be load_extension_plugins with:
    registry as plugin_registry
    plugin_directory as "/plugins/syntax_extensions"
    security_policy as strict_security_policy

For each plugin in loaded_plugins:
    Let validated be validate_plugin_security with plugin as plugin
    If validated:
        Let registered be register_plugin_extensions with plugin as plugin
```

## Related Modules

- [**Macro System Core**](./system.md) - Core macro infrastructure
- [**DSL Support**](./dsl_support.md) - Domain-specific language creation
- [**Code Generation**](./code_generation.md) - Template-based code generation
- [**Hygiene System**](./hygiene.md) - Variable scoping and hygiene
- [**Production System**](./production_system.md) - Enterprise-grade processing