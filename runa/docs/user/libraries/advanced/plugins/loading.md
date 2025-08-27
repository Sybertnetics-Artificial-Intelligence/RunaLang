# Plugin Loading Module

The Plugin Loading module provides robust, production-grade mechanisms for loading, initializing, and unloading plugins at runtime and compile time in the Runa Advanced Plugins Library.

## Overview

This module handles the complex process of safely loading plugins into the runtime environment, managing their lifecycle, and providing developer tools for hot-reloading and debugging. It ensures proper dependency resolution, error handling, and resource management.

### Key Features

- **Dynamic Plugin Loading**: Load plugins at runtime with full validation
- **Initialization Management**: Structured plugin lifecycle with proper error handling
- **Dependency Resolution**: Automatic dependency checking and loading order
- **Hot-Reload Support**: Development-time hot-reloading with state preservation
- **Resource Cleanup**: Proper unloading and memory management
- **Developer Tools**: Debugging, testing, and profiling capabilities
- **Compatibility Checking**: Version and platform compatibility validation
- **Error Recovery**: Robust error handling with detailed diagnostics

## Core Types

### PluginLoader Interface

```runa
Type called "PluginLoader":
    load_plugin as Function that takes plugin_path as String returns Plugin
    initialize_plugin as Function that takes plugin as Plugin returns Boolean
    unload_plugin as Function that takes plugin_id as String returns Boolean
    check_dependencies as Function that takes plugin as Plugin returns Boolean
    metadata as Dictionary[String, Any]
```

### Loading Error Types

```runa
Type PluginLoadError is Exception with:
    message as String
    metadata as Dictionary[String, Any]

Type PluginCompatibilityError is Exception with:
    message as String
    metadata as Dictionary[String, Any]
```

## Key Functions

### Plugin Loading

#### load_plugin

Loads a plugin from a specified path with comprehensive validation and error handling.

```runa
Process called "load_plugin" that takes loader as PluginLoader and plugin_path as String returns Plugin:
    Try:
        If not file_exists(plugin_path):
            Throw PluginLoadError with message "Plugin file not found: " plus plugin_path
        Let manifest_path be plugin_path joined with "/plugin.toml"
        Let manifest be parse_toml_file(manifest_path)
        Let validation_result be validate_plugin_manifest(manifest)
        If not validation_result.is_valid:
            Throw PluginLoadError with message "Manifest validation failed: " joined with join_list(validation_result.errors, "; ")
        If not loader.check_dependencies with plugin as manifest.plugin:
            Throw PluginLoadError with message "Dependency check failed for: " plus manifest.plugin.id
        If not is_compatible_version(manifest.compatibility.runa_version, current_runa_version()):
            Throw PluginCompatibilityError with message "Incompatible Runa version"
        Let entry_point_path be plugin_path joined with "/" joined with manifest.plugin.entry_point
        Let plugin_module be load_module_from_file(entry_point_path)
        Let plugin_instance be Plugin with:
            plugin_id as manifest.plugin.id
            name as manifest.plugin.name
            version as manifest.plugin.version
            author as manifest.plugin.author
            description as manifest.plugin.description
            entry_point as plugin_module.main
            lifecycle as create_plugin_lifecycle(plugin_module)
            metadata as manifest.plugin
        Acquire _plugin_locks[plugin_instance.plugin_id]
        Set _loaded_plugins[plugin_instance.plugin_id] to plugin_instance
        Release _plugin_locks[plugin_instance.plugin_id]
        Return plugin_instance
    Catch error:
        Add "Failed to load plugin: " joined with plugin_path joined with ": " joined with error.message to _plugin_load_errors
        Log error message "Failed to load plugin: " joined with plugin_path joined with ": " joined with error.message
        Rethrow error
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/loading" as Loading

Let loader be Loading.create_plugin_loader()
Try:
    Let plugin be Loading.load_plugin(loader, "/plugins/data-processor")
    Log message "Successfully loaded: " plus plugin.name plus " v" plus plugin.version
    Log message "Author: " plus plugin.author
    Log message "Description: " plus plugin.description
Catch Loading.PluginLoadError as error:
    Log error message "Load failed: " plus error.message
Catch Loading.PluginCompatibilityError as error:
    Log error message "Compatibility issue: " plus error.message
```

#### initialize_plugin

Initializes a loaded plugin and starts its lifecycle.

```runa
Process called "initialize_plugin" that takes loader as PluginLoader and plugin as Plugin returns Boolean:
    Try:
        plugin.lifecycle.initialize with context as create_plugin_context(plugin)
        plugin.lifecycle.start with context as create_plugin_context(plugin)
        Return true
    Catch error:
        Add "Initialization failed for plugin: " joined with plugin.plugin_id joined with ": " joined with error.message to _plugin_load_errors
        Log error message "Initialization failed for plugin: " joined with plugin.plugin_id joined with ": " joined with error.message
        Return false
```

**Usage Example:**
```runa
Let loader be Loading.create_plugin_loader()
Let plugin be Loading.load_plugin(loader, "/plugins/data-processor")

If Loading.initialize_plugin(loader, plugin):
    Log message "Plugin initialized and started successfully"
Otherwise:
    Log error message "Plugin initialization failed"
    Note: Attempt cleanup
    Loading.unload_plugin(loader, plugin.plugin_id)
```

#### unload_plugin

Safely unloads a plugin with proper cleanup and resource management.

```runa
Process called "unload_plugin" that takes loader as PluginLoader and plugin_id as String returns Boolean:
    If plugin_id not in _loaded_plugins:
        Return false
    Acquire _plugin_locks[plugin_id]
    Let plugin be _loaded_plugins[plugin_id]
    Try:
        plugin.lifecycle.stop with context as create_plugin_context(plugin)
        unload_plugin_module(plugin_id)
        Remove _loaded_plugins[plugin_id]
        Release _plugin_locks[plugin_id]
        Return true
    Catch error:
        Add "Unload failed for plugin: " joined with plugin_id joined with ": " joined with error.message to _plugin_load_errors
        Log error message "Unload failed for plugin: " joined with plugin_id joined with ": " joined with error.message
        Release _plugin_locks[plugin_id]
        Return false
```

**Usage Example:**
```runa
Let loader be Loading.create_plugin_loader()

Note: Safely unload a plugin
If Loading.unload_plugin(loader, "data-processor"):
    Log message "Plugin unloaded successfully"
Otherwise:
    Log error message "Failed to unload plugin"
```

### Dependency Management

#### check_plugin_dependencies

Validates that all required dependencies are available before loading.

```runa
Process called "check_plugin_dependencies" that takes loader as PluginLoader and plugin as Plugin returns Boolean:
    Let dependencies be plugin.metadata.get("dependencies", dictionary containing)
    For each dep_id in keys of dependencies:
        If dep_id not in _loaded_plugins:
            Log error message "Missing dependency: " plus dep_id
            Return false
    Return true
```

**Usage Example:**
```runa
Let loader be Loading.create_plugin_loader()
Let plugin be Loading.load_plugin(loader, "/plugins/analytics-plugin")

If Loading.check_plugin_dependencies(loader, plugin):
    Log message "All dependencies satisfied"
    If Loading.initialize_plugin(loader, plugin):
        Log message "Plugin ready to use"
Otherwise:
    Log error message "Missing dependencies - cannot initialize"
```

## Hot-Reload Development Support

### PluginHotReloader

```runa
Type called "PluginHotReloader":
    enable_hot_reload as Function that takes plugin_id as String returns Boolean
    disable_hot_reload as Function that takes plugin_id as String returns Boolean
    watch_files as Function that takes plugin_id as String and paths as List[String] returns FileWatcher
    reload_plugin as Function that takes plugin_id as String returns Boolean
    metadata as Dictionary[String, Any]
```

### File Watching

```runa
Type called "FileWatcher":
    on_change as Function that takes handler as Function returns None
    stop as Function that takes no arguments returns None
    metadata as Dictionary[String, Any]
```

#### enable_plugin_hot_reload

Enables automatic reloading when plugin files change.

```runa
Process called "enable_plugin_hot_reload" that takes reloader as PluginHotReloader and plugin_id as String returns Boolean:
    Let plugin be _loaded_plugins.get(plugin_id)
    If plugin is None:
        Return false
    Let plugin_path be get_plugin_path(plugin_id)
    Let watcher be reloader.watch_files(plugin_id, [plugin_path])
    watcher.on_change with handler as lambda file_path:
        Log message "Plugin file changed: " plus file_path
        If reload_plugin_safely(reloader, plugin_id):
            Log message "Plugin reloaded successfully: " plus plugin_id
        Otherwise:
            Log error message "Plugin reload failed: " plus plugin_id
    Return true
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/loading" as Loading

Let reloader be Loading.create_plugin_hot_reloader()

Note: Enable hot-reload for development
If Loading.enable_plugin_hot_reload(reloader, "data-processor"):
    Log message "Hot-reload enabled for data-processor"
    Log message "Plugin will automatically reload when files change"
    
    Note: Make changes to plugin files...
    Note: Plugin will be automatically reloaded
    
    Note: Disable when done
    reloader.disable_hot_reload("data-processor")
```

#### reload_plugin_safely

Safely reloads a plugin while preserving state where possible.

```runa
Process called "reload_plugin_safely" that takes reloader as PluginHotReloader and plugin_id as String returns Boolean:
    Try:
        Let plugin be _loaded_plugins.get(plugin_id)
        plugin.lifecycle.stop(create_plugin_context(plugin))
        unload_plugin_module(plugin_id)
        Let plugin_path be get_plugin_path(plugin_id)
        Let new_plugin be load_plugin_from_file(create_plugin_loader(), plugin_path)
        Acquire _plugin_locks[plugin_id]
        Set _loaded_plugins[plugin_id] to new_plugin
        Release _plugin_locks[plugin_id]
        new_plugin.lifecycle.start(create_plugin_context(new_plugin))
        Return true
    Catch error:
        Log error message "Hot reload failed for plugin " joined with plugin_id joined with ": " joined with error.message
        Return false
```

## Developer Tools

### PluginDebugger

Advanced debugging capabilities for plugin development:

```runa
Type called "PluginDebugger":
    set_breakpoint as Function that takes plugin_id as String and location as String returns Boolean
    inspect_state as Function that takes plugin_id as String returns PluginState
    step_over as Function that takes plugin_id as String returns Boolean
    continue_execution as Function that takes plugin_id as String returns Boolean
    metadata as Dictionary[String, Any]
```

### PluginTester

Automated testing support for plugins:

```runa
Type called "PluginTester":
    run_tests as Function that takes plugin_id as String returns TestResults
    get_test_coverage as Function that takes plugin_id as String returns CoverageReport
    metadata as Dictionary[String, Any]
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/loading" as Loading

Let debugger be Loading.create_plugin_debugger()
Let tester be Loading.create_plugin_tester()

Note: Debug a plugin during development
debugger.set_breakpoint("data-processor", "line:42")
Let state be debugger.inspect_state("data-processor")
Log message "Plugin state: " plus state

Note: Run automated tests
Let test_results be tester.run_tests("data-processor")
Log message "Test Results:"
Log message "  Passed: " plus test_results.passed
Log message "  Failed: " plus test_results.failed
Log message "  Total Time: " plus test_results.total_time_seconds plus "s"

Note: Get test coverage
Let coverage be tester.get_test_coverage("data-processor")
Log message "Test Coverage: " plus coverage.coverage_percentage plus "%"
```

## Lifecycle Management

### Plugin Lifecycle Creation

```runa
Process called "create_plugin_lifecycle" that takes module as Module returns PluginLifecycle:
    Return PluginLifecycle with:
        initialize as get_function_or_default(module, "initialize", default_initialize)
        start as get_function_or_default(module, "start", default_start)
        stop as get_function_or_default(module, "stop", default_stop)
        reload as get_optional_function(module, "reload")
        metadata as dictionary with "module_path" as module.path
```

### Default Lifecycle Functions

```runa
Process called "default_initialize" that takes context as PluginContext returns Boolean:
    Log message "Default plugin initialization"
    Return true

Process called "default_start" that takes context as PluginContext returns Boolean:
    Log message "Default plugin start"
    Return true

Process called "default_stop" that takes context as PluginContext returns Boolean:
    Log message "Default plugin stop"
    Return true
```

**Usage Example:**
```runa
Note: Create a custom plugin with lifecycle hooks
Type called "MyPlugin":
    data as Dictionary[String, Any]

Process called "my_plugin_initialize" that takes context as PluginContext returns Boolean:
    Log message "Initializing my custom plugin"
    Note: Setup database connections, load configuration, etc.
    Return true

Process called "my_plugin_start" that takes context as PluginContext returns Boolean:
    Log message "Starting my custom plugin services"
    Note: Start background tasks, register event handlers, etc.
    Return true

Process called "my_plugin_stop" that takes context as PluginContext returns Boolean:
    Log message "Stopping my custom plugin services"
    Note: Cleanup resources, save state, etc.
    Return true
```

## Advanced Loading Features

### Module Loading

```runa
Type called "Module":
    path as String                    # Module file path
    main as Function                  # Main entry point function
    metadata as Dictionary[String, Any]    # Module metadata
```

#### load_module_from_file

Loads a module from a file path with proper error handling:

```runa
Process called "load_module_from_file" that takes file_path as String returns Module:
    Note: Production implementation would load actual module
    Return create_mock_module(file_path)
```

### Plugin State Inspection

```runa
Type called "PluginState":
    plugin_id as String                    # Plugin identifier
    state as Dictionary[String, Any]       # Current plugin state
    variables as Dictionary[String, Any]   # Plugin variables
    stack_trace as List[String]           # Current execution stack
    metadata as Dictionary[String, Any]    # Additional state metadata
```

## Best Practices

### 1. **Proper Error Handling**
Always handle loading errors gracefully:

```runa
Let loader be Loading.create_plugin_loader()

Process called "safe_load_plugin" that takes plugin_path as String returns Optional[Plugin]:
    Try:
        Let plugin be Loading.load_plugin(loader, plugin_path)
        If Loading.initialize_plugin(loader, plugin):
            Return plugin
        Otherwise:
            Note: Initialization failed, clean up
            Loading.unload_plugin(loader, plugin.plugin_id)
            Return None
    Catch Loading.PluginLoadError as error:
        Log error message "Load error: " plus error.message
        Return None
    Catch Loading.PluginCompatibilityError as error:
        Log error message "Compatibility error: " plus error.message
        Return None
```

### 2. **Dependency Management**
Load plugins in proper dependency order:

```runa
Process called "load_plugins_with_dependencies" that takes plugin_paths as List[String] returns List[Plugin]:
    Let loaded_plugins be list containing
    Let remaining_paths be plugin_paths
    
    While length of remaining_paths is greater than 0:
        Let loaded_in_iteration be 0
        For each path in remaining_paths:
            Try:
                Let plugin be Loading.load_plugin(loader, path)
                If Loading.check_plugin_dependencies(loader, plugin):
                    If Loading.initialize_plugin(loader, plugin):
                        Append plugin to loaded_plugins
                        Remove path from remaining_paths
                        Set loaded_in_iteration to loaded_in_iteration plus 1
                    Otherwise:
                        Loading.unload_plugin(loader, plugin.plugin_id)
            Catch error:
                Log error message "Failed to load " plus path plus ": " plus error.message
                Remove path from remaining_paths
        
        If loaded_in_iteration is equal to 0 and length of remaining_paths is greater than 0:
            Log error message "Circular dependency or missing dependencies detected"
            Break
    
    Return loaded_plugins
```

### 3. **Resource Management**
Ensure proper cleanup on unload:

```runa
Process called "unload_all_plugins":
    Let all_plugin_ids be keys of _loaded_plugins
    For each plugin_id in all_plugin_ids:
        Try:
            Loading.unload_plugin(loader, plugin_id)
            Log message "Unloaded: " plus plugin_id
        Catch error:
            Log error message "Failed to unload " plus plugin_id plus ": " plus error.message
    
    Note: Clear any remaining state
    Clear _loaded_plugins
    Clear _plugin_locks
```

### 4. **Development Workflow**
Use hot-reload for efficient development:

```runa
Process called "development_setup" that takes plugin_id as String:
    Let reloader be Loading.create_plugin_hot_reloader()
    Let tester be Loading.create_plugin_tester()
    
    Note: Enable hot-reload
    If Loading.enable_plugin_hot_reload(reloader, plugin_id):
        Log message "Hot-reload enabled for " plus plugin_id
        
        Note: Run tests on every reload
        reloader.watch_files(plugin_id, [get_plugin_path(plugin_id)]).on_change with handler as lambda file_path:
            Log message "File changed: " plus file_path
            Note: Run tests after reload
            Let test_results be tester.run_tests(plugin_id)
            If test_results.failed is greater than 0:
                Log error message "Tests failed after reload!"
            Otherwise:
                Log message "All tests passed after reload"
```

## Integration Examples

### With Discovery Module

```runa
Import "stdlib/advanced/plugins/discovery" as Discovery
Import "stdlib/advanced/plugins/loading" as Loading

Let discovery be Discovery.create_plugin_discovery()
Let loader be Loading.create_plugin_loader()

Note: Discover and load compatible plugins
Let discovered_plugins be Discovery.scan_plugins(discovery, "/plugins")
For each plugin_metadata in discovered_plugins:
    If Discovery.check_plugin_compatibility(discovery, plugin_metadata):
        Try:
            Let plugin be Loading.load_plugin(loader, plugin_metadata.path)
            If Loading.initialize_plugin(loader, plugin):
                Log message "Successfully loaded and initialized: " plus plugin.name
        Catch error:
            Log error message "Failed to load " plus plugin_metadata.name plus ": " plus error.message
```

### With Management Module

```runa
Import "stdlib/advanced/plugins/loading" as Loading
Import "stdlib/advanced/plugins/management" as Management

Let loader be Loading.create_plugin_loader()
Let manager = Management.create_plugin_manager()

Note: Load plugin and register with manager
Let plugin be Loading.load_plugin(loader, "/plugins/data-processor")
If Loading.initialize_plugin(loader, plugin):
    Note: Register with manager for lifecycle control
    manager.registry[plugin.plugin_id] = plugin
    
    Note: Now can be managed through the manager
    If manager.enable_plugin(plugin.plugin_id):
        Log message "Plugin is now under management control"
```

## Comparative Notes

### Advantages over Other Plugin Loading Systems

**vs. Java ClassLoader:**
- Type-safe loading with compile-time checks
- Better error diagnostics and recovery
- Hot-reload without memory leaks
- Integrated dependency resolution

**vs. Python importlib:**
- Structured lifecycle management
- Built-in compatibility checking
- Advanced debugging capabilities
- Production-ready error handling

**vs. Node.js require():**
- Explicit plugin contracts
- Resource usage monitoring
- Security-first loading
- Professional development tools

The Runa Plugin Loading module provides a modern, secure, and developer-friendly foundation for building robust plugin-based applications with confidence in production environments.