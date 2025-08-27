# DSL Support Module

## Overview

The DSL (Domain-Specific Language) Support module enables creation of custom domain-specific languages within Runa. It provides tools for defining new syntax, parsing domain-specific constructs, and integrating custom languages seamlessly with the Runa ecosystem. This module empowers developers to create expressive, domain-focused languages for specific problem domains.

## Key Features

- **Syntax Definition Framework**: Define custom syntax patterns and grammar rules
- **Parser Generation**: Automatic parser generation from grammar specifications  
- **Semantic Analysis**: Domain-specific type checking and validation
- **Code Translation**: Transform DSL code to native Runa code
- **Error Reporting**: Rich error messages with domain-specific context
- **IDE Integration**: Syntax highlighting and autocompletion for custom DSLs
- **Extensible Architecture**: Plugin system for custom language features
- **Performance Optimized**: Efficient parsing and compilation of DSL code

## Core Types

### DSLDefinition
```runa
Type called "DSLDefinition":
    name as String
    version as String
    description as String
    grammar as DSLGrammar
    semantics as DSLSemantics
    translator as DSLTranslator
    validator as DSLValidator
    metadata as Dictionary[String, Any]
```

Complete definition of a domain-specific language including grammar, semantics, and translation rules.

### DSLGrammar
```runa
Type called "DSLGrammar":
    productions as List[ProductionRule]
    terminals as List[Terminal]
    precedence_rules as List[PrecedenceRule]
    associativity_rules as List[AssociativityRule]
    metadata as Dictionary[String, Any]
```

Grammar specification for the DSL including syntax rules and operator precedence.

### ProductionRule
```runa
Type called "ProductionRule":
    name as String
    pattern as String
    action as Optional[String]
    precedence as Integer
    associativity as Associativity
    metadata as Dictionary[String, Any]
```

Individual grammar production rule mapping syntax patterns to actions.

## API Reference

### Core Functions

#### create_dsl
```runa
Process called "create_dsl" that takes definition as DSLDefinition returns DSL
```

Creates a new DSL instance from a definition, generating parser and translator components.

**Example:**
```runa
Note: Define a simple mathematical expression DSL
Let math_grammar be DSLGrammar with:
    productions as list containing:
        ProductionRule with:
            name as "expression"
            pattern as "term (('+' | '-') term)*"
            action as "create_binary_expression"
            precedence as 1
            associativity as LeftAssociative
            metadata as dictionary containing
        ProductionRule with:
            name as "term"
            pattern as "factor (('*' | '/') factor)*"
            action as "create_binary_expression"
            precedence as 2
            associativity as LeftAssociative
            metadata as dictionary containing
        ProductionRule with:
            name as "factor"
            pattern as "number | '(' expression ')'"
            action as "create_factor"
            precedence as 3
            associativity as LeftAssociative
            metadata as dictionary containing
    terminals as list containing:
        Terminal with name as "number" and pattern as "[0-9]+"
        Terminal with name as "+" and pattern as "\\+"
        Terminal with name as "-" and pattern as "-"
        Terminal with name as "*" and pattern as "\\*"
        Terminal with name as "/" and pattern as "/"
    precedence_rules as list containing
    associativity_rules as list containing
    metadata as dictionary containing

Let math_definition be DSLDefinition with:
    name as "MathDSL"
    version as "1.0.0"
    description as "Simple mathematical expression language"
    grammar as math_grammar
    semantics as create_math_semantics
    translator as create_math_translator
    validator as create_math_validator
    metadata as dictionary containing

Let math_dsl be create_dsl with definition as math_definition

Note: DSL is ready for parsing mathematical expressions
```

#### parse_dsl_code
```runa
Process called "parse_dsl_code" that takes dsl as DSL and code as String returns ParseResult
```

Parses DSL code using the defined grammar and returns an abstract syntax tree.

**Example:**
```runa
Note: Parse a mathematical expression
Let expression be "2 + 3 * (4 - 1)"
Let result be parse_dsl_code with dsl as math_dsl and code as expression

Match result:
    When ParseSuccess with ast as parsed_ast:
        Note: Successfully parsed expression
        Let evaluated be evaluate_ast with ast as parsed_ast
        Note: Result: 11
    When ParseError with error as parse_error:
        Note: Handle parsing errors
        Print "Parse error: " plus parse_error.message
```

#### translate_dsl_to_runa
```runa
Process called "translate_dsl_to_runa" that takes dsl as DSL and ast as DSLAst returns String
```

Translates parsed DSL code to equivalent Runa code.

**Example:**
```runa
Note: Translate mathematical expression to Runa
Let result be parse_dsl_code with dsl as math_dsl and code as "2 + 3 * 4"

Match result:
    When ParseSuccess with ast as ast:
        Let runa_code be translate_dsl_to_runa with dsl as math_dsl and ast as ast
        Note: Generated Runa code: "Let result be 2 plus (3 multiplied by 4)"
```

### Grammar Definition

#### define_production_rule
```runa
Process called "define_production_rule" that takes name as String and pattern as String and action as Optional[String] returns ProductionRule
```

Creates a new production rule for grammar definition.

**Example:**
```runa
Note: Define a production rule for if statements
Let if_rule be define_production_rule with:
    name as "if_statement"
    pattern as "'if' condition 'then' statement ('else' statement)?"
    action as "create_if_statement"

Note: Rule matches: if x > 0 then print("positive") else print("non-positive")
```

#### define_terminal
```runa
Process called "define_terminal" that takes name as String and pattern as String returns Terminal
```

Defines a terminal symbol (token) for the grammar.

**Example:**
```runa
Note: Define terminals for a simple query language
Let select_terminal be define_terminal with name as "SELECT" and pattern as "(?i)select"
Let from_terminal be define_terminal with name as "FROM" and pattern as "(?i)from"
Let where_terminal be define_terminal with name as "WHERE" and pattern as "(?i)where"
Let identifier_terminal be define_terminal with name as "IDENTIFIER" and pattern as "[a-zA-Z_][a-zA-Z0-9_]*"
```

## DSL Examples

### SQL-like Query Language
```runa
Note: Define a simplified SQL-like DSL
Let query_grammar be DSLGrammar with:
    productions as list containing:
        ProductionRule with:
            name as "query"
            pattern as "'SELECT' field_list 'FROM' table_name ('WHERE' condition)?"
            action as "create_query"
        ProductionRule with:
            name as "field_list"
            pattern as "field (',' field)*"
            action as "create_field_list"
        ProductionRule with:
            name as "field"
            pattern as "IDENTIFIER ('AS' IDENTIFIER)?"
            action as "create_field"
        ProductionRule with:
            name as "condition"
            pattern as "IDENTIFIER operator value"
            action as "create_condition"
    terminals as list containing:
        define_terminal with name as "SELECT" and pattern as "(?i)select"
        define_terminal with name as "FROM" and pattern as "(?i)from"
        define_terminal with name as "WHERE" and pattern as "(?i)where"
        define_terminal with name as "AS" and pattern as "(?i)as"
        define_terminal with name as "IDENTIFIER" and pattern as "[a-zA-Z_][a-zA-Z0-9_]*"
        define_terminal with name as "STRING" and pattern as "'[^']*'"
        define_terminal with name as "NUMBER" and pattern as "[0-9]+"

Let query_dsl be create_dsl with definition as DSLDefinition with:
    name as "SimpleSQL"
    grammar as query_grammar
    semantics as create_sql_semantics
    translator as create_sql_translator

Note: Parse and translate SQL queries
Let sql_query be "SELECT name, age FROM users WHERE age > 18"
Let parsed be parse_dsl_code with dsl as query_dsl and code as sql_query
```

### Configuration DSL
```runa
Note: Define a configuration DSL
Let config_grammar be DSLGrammar with:
    productions as list containing:
        ProductionRule with:
            name as "configuration"
            pattern as "section*"
            action as "create_configuration"
        ProductionRule with:
            name as "section"
            pattern as "'[' IDENTIFIER ']' setting*"
            action as "create_section"
        ProductionRule with:
            name as "setting"
            pattern as "IDENTIFIER '=' value"
            action as "create_setting"
        ProductionRule with:
            name as "value"
            pattern as "STRING | NUMBER | BOOLEAN | list"
            action as "create_value"
        ProductionRule with:
            name as "list"
            pattern as "'[' (value (',' value)*)? ']'"
            action as "create_list"
    terminals as list containing:
        define_terminal with name as "IDENTIFIER" and pattern as "[a-zA-Z_][a-zA-Z0-9_]*"
        define_terminal with name as "STRING" and pattern as "\"[^\"]*\""
        define_terminal with name as "NUMBER" and pattern as "[0-9]+(\\.[0-9]+)?"
        define_terminal with name as "BOOLEAN" and pattern as "true|false"

Let config_dsl be create_dsl with definition as DSLDefinition with:
    name as "ConfigDSL"
    grammar as config_grammar
    
Note: Parse configuration files
Let config_text be "[database]
host = \"localhost\"
port = 5432
enabled = true
replicas = [\"host1\", \"host2\", \"host3\"]

[logging]
level = \"INFO\"
file = \"/var/log/app.log\""

Let parsed_config be parse_dsl_code with dsl as config_dsl and code as config_text
```

### State Machine DSL
```runa
Note: Define a state machine DSL
Let state_machine_grammar be DSLGrammar with:
    productions as list containing:
        ProductionRule with:
            name as "state_machine"
            pattern as "'machine' IDENTIFIER '{' state* transition* '}'"
            action as "create_state_machine"
        ProductionRule with:
            name as "state"
            pattern as "'state' IDENTIFIER ('initial' | 'final')? '{' action* '}'"
            action as "create_state"
        ProductionRule with:
            name as "transition"
            pattern as "'on' event 'from' IDENTIFIER 'to' IDENTIFIER ('with' action)?"
            action as "create_transition"
        ProductionRule with:
            name as "action"
            pattern as "'action' IDENTIFIER '(' parameter_list? ')'"
            action as "create_action"
        ProductionRule with:
            name as "event"
            pattern as "IDENTIFIER"
            action as "create_event"

Let fsm_dsl be create_dsl with definition as DSLDefinition with:
    name as "StateMachineDSL"
    grammar as state_machine_grammar

Note: Define a simple state machine
Let fsm_code be "machine door_lock {
    state locked initial {
        action guard_active()
    }
    
    state unlocked {
        action guard_inactive()
    }
    
    on unlock from locked to unlocked with action log_unlock()
    on lock from unlocked to locked with action log_lock()
}"

Let fsm_ast be parse_dsl_code with dsl as fsm_dsl and code as fsm_code
```

## Idiomatic Usage

### Building Domain-Specific APIs
```runa
Note: Create a fluent API DSL for HTTP requests
Let http_dsl_grammar be DSLGrammar with:
    productions as list containing:
        ProductionRule with:
            name as "request"
            pattern as "method url header* body?"
            action as "create_http_request"
        ProductionRule with:
            name as "method"
            pattern as "'GET' | 'POST' | 'PUT' | 'DELETE'"
            action as "create_method"
        ProductionRule with:
            name as "url"
            pattern as "STRING"
            action as "create_url"
        ProductionRule with:
            name as "header"
            pattern as "'header' IDENTIFIER ':' STRING"
            action as "create_header"
        ProductionRule with:
            name as "body"
            pattern as "'body' STRING"
            action as "create_body"

Let http_dsl be create_dsl with definition as DSLDefinition with:
    name as "HttpDSL"
    grammar as http_dsl_grammar

Note: Use the DSL for HTTP requests
Let request_spec be "POST \"/api/users\"
header Content-Type: \"application/json\"
header Authorization: \"Bearer token123\"
body \"{\\\"name\\\": \\\"John\\\", \\\"email\\\": \\\"john@example.com\\\"}\""

Let request_ast be parse_dsl_code with dsl as http_dsl and code as request_spec
Let runa_code be translate_dsl_to_runa with dsl as http_dsl and ast as request_ast
```

### Creating Business Rule Languages
```runa
Note: Define a business rules DSL
Let rules_grammar be DSLGrammar with:
    productions as list containing:
        ProductionRule with:
            name as "rule_set"
            pattern as "rule*"
            action as "create_rule_set"
        ProductionRule with:
            name as "rule"
            pattern as "'rule' IDENTIFIER ':' condition 'then' action_list"
            action as "create_rule"
        ProductionRule with:
            name as "condition"
            pattern as "comparison ('and' | 'or' comparison)*"
            action as "create_condition"
        ProductionRule with:
            name as "comparison"
            pattern as "field operator value"
            action as "create_comparison"
        ProductionRule with:
            name as "action_list"
            pattern as "action (',' action)*"
            action as "create_action_list"

Let business_rules_dsl be create_dsl with definition as DSLDefinition with:
    name as "BusinessRulesDSL"
    grammar as rules_grammar

Note: Define business rules
Let rules_code be "rule discount_eligibility:
    customer.age >= 65 or customer.membership == \"premium\"
    then apply_discount(0.15), send_notification(\"discount_applied\")

rule shipping_free:
    order.total > 100 and customer.location == \"domestic\"
    then set_shipping_cost(0), add_benefit(\"free_shipping\")"

Let rules_ast be parse_dsl_code with dsl as business_rules_dsl and code as rules_code
```

## Comparative Notes

### vs. ANTLR
- **Runa**: Integrated with macro system and Runa ecosystem
- **ANTLR**: Standalone parser generator
- **Advantage**: Seamless integration and unified tooling

### vs. Lex/Yacc
- **Runa**: Modern declarative syntax with integrated semantics
- **Lex/Yacc**: Separate lexer and parser with C-style actions
- **Advantage**: Better maintainability and type safety

### vs. PEG Parsers
- **Runa**: Grammar-based with automatic error recovery
- **PEG**: Expression-based with backtracking
- **Advantage**: Better performance and error reporting

## Performance Considerations

### Parser Caching
```runa
Note: Parsed grammars are cached for reuse
Let dsl_config be DSLConfig with:
    enable_parser_caching as true
    cache_compiled_grammars as true
    max_cache_size as 1000

Note: Subsequent DSL creations reuse compiled parsers
```

### Incremental Parsing
```runa
Note: Support for incremental parsing of large DSL files
Let incremental_parser be create_incremental_parser with dsl as dsl
Let initial_result be parse_incrementally with parser as incremental_parser and code as initial_code
Let updated_result be update_parse with parser as incremental_parser and changes as code_changes

Note: Only re-parses changed sections
```

### Memory Management
```runa
Note: AST nodes are memory-managed efficiently
Let memory_config be ParserMemoryConfig with:
    enable_ast_pooling as true
    max_ast_nodes as 100000
    enable_garbage_collection as true

Let dsl be create_dsl with definition as dsl_definition and memory_config as memory_config
```

## Error Handling

### Syntax Errors
```runa
Note: Rich syntax error reporting with suggestions
Let result be parse_dsl_code with dsl as sql_dsl and code as "SELCT name FROM users"

Match result:
    When ParseError with error as err:
        Note: Error message: "Unexpected token 'SELCT' at line 1, column 1"
        Note: Suggestion: "Did you mean 'SELECT'?"
        Let suggestions be err.suggestions
        For each suggestion in suggestions:
            Print "Suggestion: " plus suggestion
```

### Semantic Errors
```runa
Note: Domain-specific semantic validation
Let validation_result be validate_dsl_semantics with dsl as dsl and ast as ast

Match validation_result:
    When ValidationError with errors as semantic_errors:
        For each error in semantic_errors:
            Print "Semantic error: " plus error.message plus " at " plus error.location
```

## Integration Examples

### With Macro System
```runa
Note: DSL that generates macros
Let macro_gen_dsl be create_dsl with definition as macro_generator_definition

Let dsl_code be "macro simple_getter for field {
    getter_name: get_{{field.name}}
    return_type: {{field.type}}
    body: return self.{{field.name}}
}"

Let generated_macro be parse_and_generate_macro with dsl as macro_gen_dsl and code as dsl_code
```

### With IDE Support
```runa
Note: Register DSL for IDE integration
Let ide_integration be register_dsl_with_ide with:
    dsl as config_dsl
    file_extensions as list containing ".config", ".cfg"
    syntax_highlighting as config_highlighting_rules
    autocompletion as config_completion_provider

Note: IDE now provides syntax highlighting and autocompletion
```

## Production Examples

### API Specification DSL
```runa
Note: Complete API specification language
Let api_spec_dsl be create_comprehensive_api_dsl

Let api_specification be "api UserService version 1.0 {
    base_url: \"/api/v1\"
    
    endpoint get_user {
        method: GET
        path: \"/users/{id}\"
        parameters: id as Integer
        returns: User
        auth: required
    }
    
    endpoint create_user {
        method: POST
        path: \"/users\"
        body: UserCreationRequest
        returns: User
        auth: required
        validation: validate_user_data
    }
    
    type User {
        id: Integer
        username: String
        email: String
        created_at: DateTime
    }
    
    type UserCreationRequest {
        username: String (required, min_length: 3)
        email: String (required, email_format)
        password: String (required, min_length: 8)
    }
}"

Let api_ast be parse_dsl_code with dsl as api_spec_dsl and code as api_specification
Let server_code be generate_server_implementation with ast as api_ast
Let client_code be generate_client_library with ast as api_ast
```

### Workflow Definition DSL
```runa
Note: Business workflow definition language
Let workflow_dsl be create_workflow_dsl

Let workflow_definition be "workflow order_processing {
    start -> validate_order
    
    step validate_order {
        action: validate_order_data
        on_success -> check_inventory
        on_failure -> send_error_notification
    }
    
    step check_inventory {
        action: verify_product_availability
        timeout: 30s
        on_success -> process_payment
        on_failure -> notify_backorder
    }
    
    step process_payment {
        action: charge_customer
        retry: 3 times with 5s delay
        on_success -> fulfill_order
        on_failure -> cancel_order
    }
    
    step fulfill_order {
        action: prepare_shipment
        on_success -> send_confirmation
    }
    
    end_steps: [send_confirmation, send_error_notification, cancel_order]
}"

Let workflow_ast be parse_dsl_code with dsl as workflow_dsl and code as workflow_definition
Let executable_workflow be compile_workflow with ast as workflow_ast
```

## Related Modules

- [**Macro System Core**](./system.md) - Core macro infrastructure
- [**Code Generation**](./code_generation.md) - Template-based code generation
- [**Syntax Extensions**](./syntax_extensions.md) - Custom syntax definitions
- [**Hygiene System**](./hygiene.md) - Variable scoping and hygiene
- [**Production System**](./production_system.md) - Enterprise-grade processing