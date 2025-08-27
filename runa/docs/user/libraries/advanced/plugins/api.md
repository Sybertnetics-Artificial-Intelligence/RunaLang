# Plugin API Module

The Plugin API module provides the core interfaces, types, and functions for plugin development, registration, lifecycle management, and inter-plugin communication in the Runa Advanced Plugins Library.

## Overview

This module serves as the foundation for the entire plugin system, providing:

- **Core Plugin Types**: Plugin interface definitions and contracts
- **Registration System**: Plugin registration and unregistration
- **Lifecycle Management**: Plugin initialization, start, stop, and reload
- **Communication**: Message passing and event-driven communication
- **Service Discovery**: Service registration and discovery mechanisms
- **Multi-Language Support**: Bridges for Python, JavaScript, and other languages
- **AI Integration**: AI-assisted plugin generation and improvement

## Core Types

### Plugin Definition

```runa
Type called "Plugin":
    plugin_id as String              # Unique identifier
    name as String                   # Human-readable name
    version as String                # Semantic version
    author as String                 # Plugin author
    description as String            # Plugin description
    entry_point as Function          # Main entry function
    lifecycle as PluginLifecycle     # Lifecycle handlers
    metadata as Dictionary[String, Any]  # Additional metadata
```

### Plugin Lifecycle

```runa
Type called "PluginLifecycle":
    initialize as Function           # Called when plugin is loaded
    start as Function               # Called when plugin is activated
    stop as Function                # Called when plugin is deactivated
    reload as Optional[Function]     # Called when plugin is reloaded
    metadata as Dictionary[String, Any]
```

### Plugin Context

```runa
Type called "PluginContext":
    config as PluginConfig          # Plugin configuration
    state as Dictionary[String, Any] # Plugin state storage
    communication as PluginCommunication # Communication interface
    metadata as Dictionary[String, Any]  # Context metadata
```

## Core Functions

### Plugin Registration

#### `register_plugin(plugin: Plugin) -> Boolean`

Registers a plugin with the system.

```runa
Import "stdlib/advanced/plugins/api" as PluginAPI

Let my_plugin be PluginAPI.Plugin with:
    plugin_id as "com.example.calculator"
    name as "Calculator Plugin"
    version as "1.2.0"
    author as "Example Corp"
    description as "Basic calculator functionality"
    entry_point as calculator_entry_point
    lifecycle as PluginAPI.PluginLifecycle with:
        initialize as init_calculator
        start as start_calculator
        stop as stop_calculator
        reload as None
        metadata as dictionary containing
    metadata as dictionary containing

Let success be PluginAPI.register_plugin with plugin as my_plugin
If success:
    Display "Calculator plugin registered successfully"
```

#### `unregister_plugin(plugin_id: String) -> Boolean`

Unregisters a plugin from the system.

```runa
Let success be PluginAPI.unregister_plugin with plugin_id as "com.example.calculator"
If success:
    Display "Plugin unregistered successfully"
```

### Plugin Querying

#### `get_plugin(plugin_id: String) -> Optional[Plugin]`

Retrieves a specific plugin by ID.

```runa
Let plugin be PluginAPI.get_plugin with plugin_id as "com.example.calculator"
If plugin is not null:
    Display "Found plugin: " plus plugin.name
```

#### `list_plugins() -> List[Plugin]`

Returns all registered plugins.

```runa
Let all_plugins be PluginAPI.list_plugins()
For each plugin in all_plugins:
    Display "Plugin: " plus plugin.name plus " v" plus plugin.version
```

## Communication System

### Message Passing

#### `send_plugin_message(plugin_id: String, message: PluginMessage) -> Boolean`

Sends a message to a specific plugin.

```runa
Let message be PluginAPI.PluginMessage with:
    message_id as "calc-request-001"
    sender as "com.example.app"
    recipient as "com.example.calculator"
    payload as dictionary containing:
        "operation" as "add"
        "operands" as list containing 5, 3
    timestamp as get_current_timestamp()
    metadata as dictionary containing

Let sent be PluginAPI.send_plugin_message with:
    plugin_id as "com.example.calculator"
    message as message

If sent:
    Display "Message sent to calculator plugin"
```

#### `receive_plugin_message(plugin_id: String, handler: Function)`

Sets up message reception for a plugin.

```runa
Process called "handle_calculator_message" that takes message as PluginAPI.PluginMessage:
    Let operation be message.payload["operation"]
    Let operands be message.payload["operands"]
    
    Match operation:
        When "add":
            Let result be operands[0] plus operands[1]
            Display "Result: " plus result
        When "subtract":
            Let result be operands[0] minus operands[1]
            Display "Result: " plus result
        Otherwise:
            Display "Unknown operation: " plus operation

PluginAPI.receive_plugin_message with:
    plugin_id as "com.example.calculator"
    handler as handle_calculator_message
```

### Event-Driven Communication

#### `create_plugin_event_bus() -> PluginEventBus`

Creates an event bus for plugin communication.

```runa
Let event_bus be PluginAPI.create_plugin_event_bus()

Note: Subscribe to events
Let subscription be event_bus.subscribe with:
    plugin_id as "com.example.logger"
    event_type as "calculation-performed"
    handler as log_calculation_event

Note: Publish events
Let calc_event be PluginAPI.PluginEvent with:
    event_id as "calc-event-001"
    event_type as "calculation-performed"
    source_plugin as "com.example.calculator"
    timestamp as get_current_timestamp()
    data as dictionary containing:
        "operation" as "add"
        "result" as 8
    metadata as dictionary containing

event_bus.publish with event as calc_event
```

## Service Discovery

### Service Registry

#### `create_plugin_service_registry() -> PluginServiceRegistry`

Creates a service registry for plugin services.

```runa
Let service_registry be PluginAPI.create_plugin_service_registry()

Note: Register a calculation service
Let calc_service be PluginAPI.PluginService with:
    service_id as "basic-calculator"
    service_type as "calculator"
    plugin_id as "com.example.calculator"
    interface as create_calculator_interface()
    metadata as dictionary containing:
        "operations" as list containing "add", "subtract", "multiply", "divide"

Let registered be service_registry.register_service with:
    plugin_id as "com.example.calculator"
    service as calc_service

Note: Discover calculator services
Let calculators be service_registry.discover_services with 
    service_type as "calculator"

For each calc in calculators:
    Display "Found calculator service: " plus calc.service_id
```

## Extension APIs

### UI Extensions

```runa
Let plugin_api be PluginAPI.create_comprehensive_plugin_api()

Note: Show notification
plugin_api.ui.show_notification with:
    message as "Calculation completed!"
    type as PluginAPI.NotificationType.Success

Note: Create status bar item
Let status_item be plugin_api.ui.create_status_bar_item with 
    text as "Calculator Ready"

Note: Show input dialog
Let user_input be plugin_api.ui.show_input_box with 
    prompt as "Enter a number:"
```

### Editor Extensions

```runa
Note: Register editor command
plugin_api.editor.register_command with:
    command as "calculator.calculate"
    handler as perform_calculation

Note: Register key binding
plugin_api.editor.register_keybinding with:
    key as "Ctrl+Shift+C"
    command as "calculator.calculate"

Note: Set editor theme
Let calc_theme be PluginAPI.EditorTheme with:
    name as "Calculator Theme"
    colors as dictionary containing:
        "background" as "#1e1e1e"
        "foreground" as "#d4d4d4"
    syntax_highlighting as dictionary containing:
        "number" as "#b5cea8"
        "operator" as "#569cd6"
    metadata as dictionary containing

plugin_api.editor.set_theme with theme as calc_theme
```

### Workspace Extensions

```runa
Note: Open calculation file
Let calc_file be plugin_api.workspace.open_file with 
    path as "./calculations.txt"

Note: Save calculation results
Let saved be plugin_api.workspace.save_file with file as calc_file

Note: List workspace files
Let files be plugin_api.workspace.list_files with 
    directory as "./calculations"
```

## Multi-Language Support

### Python Plugin Integration

```runa
Note: Load Python plugin
Let python_calc be PluginAPI.load_python_plugin with 
    plugin_path as "./plugins/python-calculator"

Note: Execute Python calculation
Let py_result be PluginAPI.execute_foreign_plugin with:
    plugin as python_calc
    context as create_plugin_context(python_calc)
```

### JavaScript Plugin Integration

```runa
Note: Create JavaScript bridge
Let js_bridge be PluginAPI.create_language_bridge with:
    language as "javascript"
    runtime_command as "node"

Note: Create JavaScript plugin
Let js_calc be PluginAPI.ForeignPlugin with:
    language as "javascript"
    runtime_path as "/usr/bin/node"
    entry_point as "./plugins/js-calculator/main.js"
    bridge as js_bridge
    metadata as dictionary containing

Note: Execute JavaScript calculation
Let js_result be PluginAPI.execute_javascript_plugin with:
    plugin as js_calc
    method_name as "calculate"
    args as list containing "2 + 2"
```

## AI-Assisted Development

### Natural Language Plugin Generation

```runa
Note: Create AI plugin generator
Let generator be PluginAPI.PluginGenerator with:
    generate_from_description as ai_generate_plugin
    suggest_improvements as ai_suggest_improvements  
    auto_test_plugin as ai_test_plugin
    metadata as dictionary containing

Note: Generate plugin from description
Let generated_plugin be PluginAPI.generate_plugin_from_natural_language with:
    generator as generator
    description as "Create a plugin that performs advanced mathematical calculations including trigonometry, logarithms, and statistical functions"

Display "Generated plugin: " plus generated_plugin.name
Display "Plugin description: " plus generated_plugin.description
```

### Plugin Improvement Suggestions

```runa
Note: Get AI improvement suggestions
Let improvements be generator.suggest_improvements with plugin as my_plugin

For each improvement in improvements:
    Display "Improvement: " plus improvement.description
    Display "Impact: " plus improvement.impact
    
    If improvement.impact contains "high":
        Note: Apply high-impact improvements automatically
        Let improved_plugin be PluginAPI.apply_improvement_to_plugin with:
            plugin as my_plugin
            improvement as improvement
        Set my_plugin to improved_plugin
```

### Automated Plugin Testing

```runa
Note: Run automated tests on plugin
Let test_results be generator.auto_test_plugin with plugin as my_plugin

If test_results.has_failures:
    Display "Plugin tests failed:"
    For each failure in test_results.failures:
        Display "  - " plus failure.message
        
    Note: Get AI suggestions to fix failures
    Let fixes be generator.suggest_improvements with plugin as my_plugin
    For each fix in fixes:
        If fix.description contains "test":
            Let fixed_plugin be PluginAPI.apply_improvement_to_plugin with:
                plugin as my_plugin
                improvement as fix
            Set my_plugin to fixed_plugin
            Break
Else:
    Display "All plugin tests passed!"
```

## Advanced Features

### Plugin Validation

```runa
Note: Validate plugin metadata
Let is_valid be PluginAPI.validate_plugin_metadata with plugin as my_plugin
If not is_valid:
    Display "Plugin metadata is invalid"

Note: Check semantic versioning
Let version_valid be PluginAPI.is_valid_semver with version as "1.2.3"
If version_valid:
    Display "Version format is correct"
```

### Service Interface Validation

```runa
Note: Create service interface
Let calc_interface be PluginAPI.ServiceInterface with:
    methods as list containing:
        PluginAPI.MethodSignature with:
            name as "add"
            parameters as list containing:
                PluginAPI.ParameterSignature with:
                    name as "a"
                    parameter_type as "Number"
                    required as true
                    default_value as None
                    metadata as dictionary containing
                PluginAPI.ParameterSignature with:
                    name as "b"
                    parameter_type as "Number"
                    required as true
                    default_value as None
                    metadata as dictionary containing
            return_type as "Number"
            metadata as dictionary containing
    properties as list containing
    metadata as dictionary containing

Note: Validate the interface
Let interface_valid be PluginAPI.validate_service_interface with 
    interface as calc_interface
If interface_valid:
    Display "Service interface is valid"
```

## Error Handling

The API module defines several exception types for robust error handling:

```runa
Note: Handle plugin registration errors
Try:
    PluginAPI.register_plugin with plugin as duplicate_plugin
Catch error as PluginAPI.PluginRegistrationError:
    Display "Registration failed: " plus error.message
    
Note: Handle plugin not found errors
Try:
    PluginAPI.get_plugin with plugin_id as "nonexistent"
Catch error as PluginAPI.PluginNotFoundError:
    Display "Plugin not found: " plus error.message

Note: Handle service registration errors
Try:
    service_registry.register_service with plugin_id as "test" and service as invalid_service
Catch error as PluginAPI.ServiceRegistrationError:
    Display "Service registration failed: " plus error.message
```

## Best Practices

### Plugin Development

1. **Unique Plugin IDs**: Use reverse domain notation (e.g., "com.company.plugin-name")
2. **Semantic Versioning**: Follow semantic versioning for compatibility
3. **Graceful Lifecycle**: Implement proper initialization and cleanup
4. **Error Handling**: Handle errors gracefully and provide meaningful messages
5. **Resource Management**: Clean up resources in the stop lifecycle method

### Communication Patterns

1. **Event-Driven**: Use events for loose coupling between plugins
2. **Service Discovery**: Register services for other plugins to discover
3. **Message Validation**: Always validate incoming messages
4. **Async Operations**: Use appropriate async patterns for long-running operations
5. **Error Propagation**: Properly propagate and handle communication errors

### Performance Considerations

1. **Lazy Loading**: Load plugins only when needed
2. **Efficient Messaging**: Use appropriate message sizes and frequencies
3. **Resource Cleanup**: Properly clean up resources and event subscriptions
4. **Memory Management**: Monitor and manage memory usage
5. **Caching**: Cache frequently accessed data and services

The Plugin API module provides a comprehensive foundation for building robust, extensible plugin systems in Runa applications.