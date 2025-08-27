# Hot Reload Core Module

## Overview

The Hot Reload Core module provides comprehensive hot reloading capabilities for Runa development environments, enabling real-time code updates without losing application state. This module is designed for AI-first development workflows and supports enterprise-grade development productivity.

## Key Features

- **Real-time File Monitoring**: Cross-platform file system event detection with configurable polling
- **Intelligent Dependency Tracking**: Automatic dependency resolution with circular dependency detection  
- **State Preservation**: Module state serialization and restoration across reloads
- **Incremental Compilation**: Smart compilation with caching and optimization
- **Zero-Downtime Updates**: Hot-swapping modules without application restart
- **Error Recovery**: Comprehensive error handling with automatic rollback
- **Performance Monitoring**: Built-in profiling and bottleneck detection
- **AI/Agent Integration**: Optimized for AI-driven development workflows

## Core Types

### HotReloadConfig

Configuration for hot reload behavior.

```runa
Type called "HotReloadConfig":
    enabled as Boolean defaults to true
    watch_paths as List[String] defaults to list containing "."
    ignore_patterns as List[String] defaults to list containing "*.tmp", "*.log", ".git/*"
    poll_interval as Float defaults to 1.0
    max_file_size as Integer defaults to 10485760
    preserve_state as Boolean defaults to true
    incremental_compilation as Boolean defaults to true
    cache_enabled as Boolean defaults to true
    cache_size as Integer defaults to 100
    error_recovery as Boolean defaults to true
    performance_monitoring as Boolean defaults to true
    ai_mode as Boolean defaults to false
    metadata as Dictionary[String, Any] defaults to empty dictionary
```

### FileChangeEvent

Represents a file system change event.

```runa
Type called "FileChangeEvent":
    file_path as String
    change_type as String
    timestamp as Float
    file_size as Integer
    checksum as String
    metadata as Dictionary[String, Any]
```

### DependencyNode

Represents a module in the dependency graph.

```runa
Type called "DependencyNode":
    module_name as String
    file_path as String
    dependencies as List[String]
    dependents as List[String]
    last_modified as Float
    checksum as String
    compilation_state as String
    error_count as Integer
    metadata as Dictionary[String, Any]
```

### ModuleState

Stores the runtime state of a module for preservation.

```runa
Type called "ModuleState":
    module_name as String
    variables as Dictionary[String, Any]
    functions as Dictionary[String, Any]
    types as Dictionary[String, Any]
    imports as List[String]
    exports as List[String]
    metadata as Dictionary[String, Any]
```

### HotReloadContext

Main context for hot reload operations.

```runa
Type called "HotReloadContext":
    config as HotReloadConfig
    file_watcher as Optional[FileWatcher]
    dependency_graph as Dictionary[String, DependencyNode]
    module_states as Dictionary[String, ModuleState]
    compilation_cache as Dictionary[String, Any]
    error_log as List[String]
    performance_metrics as Dictionary[String, Float]
    is_reloading as Boolean
    reload_count as Integer
    metadata as Dictionary[String, Any]
```

## Core Functions

### Context Management

#### create_hot_reload_context

Creates a new hot reload context with default configuration.

```runa
Process called "create_hot_reload_context" returns HotReloadContext:
    Return HotReloadContext with:
        config as create_default_config()
        file_watcher as None
        dependency_graph as empty dictionary
        module_states as empty dictionary
        compilation_cache as empty dictionary
        error_log as empty list
        performance_metrics as empty dictionary
        is_reloading as false
        reload_count as 0
        metadata as empty dictionary
```

**Example Usage:**
```runa
Let context be create_hot_reload_context()
Display message "Hot reload context created successfully"
```

#### configure_hot_reload

Configures hot reload with custom settings.

```runa
Process called "configure_hot_reload" that takes context as HotReloadContext and config as HotReloadConfig returns Boolean:
    Try:
        Set context.config to config
        
        If config.enabled:
            Let watcher be create_file_watcher_with_config with config as config
            Set context.file_watcher to Some with value as watcher
            
        If config.cache_enabled:
            Let cache be create_compilation_cache with size as config.cache_size
            Set context.compilation_cache to cache
            
        Return true
        
    Catch error:
        Add error.message to context.error_log
        Return false
```

**Example Usage:**
```runa
Let custom_config be HotReloadConfig with:
    enabled as true
    watch_paths as list containing "src/", "tests/"
    ignore_patterns as list containing "*.tmp", "*.backup"
    poll_interval as 0.5
    ai_mode as true

Let success be configure_hot_reload with context as context and config as custom_config
If success:
    Display message "Hot reload configured with AI mode enabled"
Otherwise:
    Display message "Failed to configure hot reload"
```

### File Watching

#### start_file_watching

Initiates file system monitoring.

```runa
Process called "start_file_watching" that takes context as HotReloadContext returns Boolean:
    If context.file_watcher is None:
        Return false
        
    Let watcher be get_optional_value with optional as context.file_watcher
    
    For each path in context.config.watch_paths:
        Let watch_result be watcher.watch_directory with path as path
        If not watch_result:
            Add "Failed to watch path: " plus path to context.error_log
            Return false
    
    Let start_result be watcher.start_monitoring()
    Return start_result
```

**Example Usage:**
```runa
Let watching_started be start_file_watching with context as context
If watching_started:
    Display message "File watching started successfully"
    Display message "Monitoring paths: " plus context.config.watch_paths
Otherwise:
    Display message "Failed to start file watching"
```

#### process_file_changes

Processes detected file changes and triggers reloads.

```runa
Process called "process_file_changes" that takes context as HotReloadContext returns List[FileChangeEvent]:
    If context.file_watcher is None:
        Return empty list
        
    Let watcher be get_optional_value with optional as context.file_watcher
    Let changes be watcher.get_pending_changes()
    
    Let processed_changes be empty list
    
    For each change in changes:
        If should_process_change with context as context and change as change:
            Let processed_change be process_single_change with context as context and change as change
            Add processed_change to processed_changes
            
    Return processed_changes
```

**Example Usage:**
```runa
Let changes be process_file_changes with context as context
If length of changes is greater than 0:
    Display message "Processed " plus (length of changes) plus " file changes"
    For each change in changes:
        Display message "  - " plus change.file_path plus " (" plus change.change_type plus ")"
```

### Dependency Management

#### build_dependency_graph

Analyzes source files and builds dependency graph.

```runa
Process called "build_dependency_graph" that takes context as HotReloadContext and file_paths as List[String] returns Boolean:
    Try:
        Set context.dependency_graph to empty dictionary
        
        Note: First pass - create nodes for all files
        For each file_path in file_paths:
            Let module_name be extract_module_name with file_path as file_path
            Let node be create_dependency_node with file_path as file_path and module_name as module_name
            Set context.dependency_graph[module_name] to node
            
        Note: Second pass - analyze dependencies
        For each module_name in keys of context.dependency_graph:
            Let node be context.dependency_graph[module_name]
            Let dependencies be analyze_file_dependencies with file_path as node.file_path
            Set node.dependencies to dependencies
            
            Note: Update reverse dependencies
            For each dep in dependencies:
                If dep in context.dependency_graph:
                    Let dep_node be context.dependency_graph[dep]
                    Add module_name to dep_node.dependents
                    
        Return true
        
    Catch error:
        Add "Dependency graph build failed: " plus error.message to context.error_log
        Return false
```

**Example Usage:**
```runa
Let source_files be list containing "src/main.runa", "src/utils.runa", "src/config.runa"
Let graph_built be build_dependency_graph with context as context and file_paths as source_files

If graph_built:
    Display message "Dependency graph built with " plus (length of context.dependency_graph) plus " modules"
    
    Note: Display dependency information
    For each module_name in keys of context.dependency_graph:
        Let node be context.dependency_graph[module_name]
        Display message module_name plus " depends on: " plus node.dependencies
Otherwise:
    Display message "Failed to build dependency graph"
```

#### detect_circular_dependencies

Detects circular dependencies in the module graph.

```runa
Process called "detect_circular_dependencies" that takes context as HotReloadContext returns List[List[String]]:
    Let cycles be empty list
    Let visited be empty dictionary
    Let rec_stack be empty dictionary
    
    For each module_name in keys of context.dependency_graph:
        Set visited[module_name] to false
        Set rec_stack[module_name] to false
    
    For each module_name in keys of context.dependency_graph:
        If not visited[module_name]:
            Let cycle be find_cycle_from_node with 
                context as context 
                and node as module_name 
                and visited as visited 
                and rec_stack as rec_stack
            If cycle is not empty:
                Add cycle to cycles
                
    Return cycles
```

**Example Usage:**
```runa
Let circular_deps be detect_circular_dependencies with context as context
If length of circular_deps is greater than 0:
    Display message "WARNING: Circular dependencies detected!"
    For each cycle in circular_deps:
        Display message "  Cycle: " plus (cycle joined with " -> ")
Otherwise:
    Display message "No circular dependencies found"
```

### State Preservation

#### preserve_module_state

Captures the current state of a module before reload.

```runa
Process called "preserve_module_state" that takes context as HotReloadContext and module_name as String returns Boolean:
    Try:
        Let module_info be get_module_runtime_info with module_name as module_name
        
        Let state be ModuleState with:
            module_name as module_name
            variables as module_info.variables
            functions as module_info.functions
            types as module_info.types
            imports as module_info.imports
            exports as module_info.exports
            metadata as create_state_metadata with module_info as module_info
            
        Set context.module_states[module_name] to state
        Return true
        
    Catch error:
        Add "State preservation failed for " plus module_name plus ": " plus error.message to context.error_log
        Return false
```

**Example Usage:**
```runa
Let state_preserved be preserve_module_state with context as context and module_name as "utils"
If state_preserved:
    Display message "Module state preserved for 'utils'"
    Let state be context.module_states["utils"]
    Display message "  Variables: " plus (length of state.variables)
    Display message "  Functions: " plus (length of state.functions)
Otherwise:
    Display message "Failed to preserve state for 'utils'"
```

#### restore_module_state

Restores previously preserved module state after reload.

```runa
Process called "restore_module_state" that takes context as HotReloadContext and module_name as String returns Boolean:
    If module_name not in context.module_states:
        Return false
        
    Try:
        Let preserved_state be context.module_states[module_name]
        Let restore_result be restore_runtime_state with 
            module_name as module_name 
            and state as preserved_state
            
        If restore_result:
            Note: State successfully restored
            Return true
        Otherwise:
            Add "State restoration failed for " plus module_name to context.error_log
            Return false
            
    Catch error:
        Add "State restoration error for " plus module_name plus ": " plus error.message to context.error_log
        Return false
```

**Example Usage:**
```runa
Let state_restored be restore_module_state with context as context and module_name as "utils"
If state_restored:
    Display message "Module state restored for 'utils'"
Otherwise:
    Display message "Failed to restore state for 'utils'"
    Display message "Errors: " plus context.error_log
```

### Hot Reloading

#### perform_hot_reload

Performs a complete hot reload of modified modules.

```runa
Process called "perform_hot_reload" that takes context as HotReloadContext and changed_files as List[String] returns Boolean:
    If context.is_reloading:
        Return false  Note: Already in progress
        
    Set context.is_reloading to true
    
    Try:
        Note: Step 1 - Determine affected modules
        Let affected_modules be calculate_affected_modules with 
            context as context 
            and changed_files as changed_files
            
        Note: Step 2 - Preserve state if enabled
        If context.config.preserve_state:
            For each module_name in affected_modules:
                preserve_module_state with context as context and module_name as module_name
                
        Note: Step 3 - Perform incremental compilation
        Let compilation_success be perform_incremental_compilation with 
            context as context 
            and modules as affected_modules
            
        If compilation_success:
            Note: Step 4 - Reload modules
            Let reload_success be reload_affected_modules with 
                context as context 
                and modules as affected_modules
                
            If reload_success:
                Note: Step 5 - Restore state if enabled
                If context.config.preserve_state:
                    For each module_name in affected_modules:
                        restore_module_state with context as context and module_name as module_name
                        
                Set context.reload_count to context.reload_count plus 1
                Set context.is_reloading to false
                Return true
                
        Note: Reload failed - attempt rollback
        perform_rollback with context as context and modules as affected_modules
        Set context.is_reloading to false
        Return false
        
    Catch error:
        Add "Hot reload failed: " plus error.message to context.error_log
        Set context.is_reloading to false
        Return false
```

**Example Usage:**
```runa
Let changed_files be list containing "src/main.runa", "src/utils.runa"
Let reload_success be perform_hot_reload with context as context and changed_files as changed_files

If reload_success:
    Display message "Hot reload completed successfully!"
    Display message "Reload count: " plus context.reload_count
    Display message "Modules reloaded: " plus (length of changed_files)
Otherwise:
    Display message "Hot reload failed"
    Display message "Check error log for details:"
    For each error in context.error_log:
        Display message "  - " plus error
```

## Performance Monitoring

### get_performance_metrics

Retrieves hot reload performance statistics.

```runa
Process called "get_performance_metrics" that takes context as HotReloadContext returns Dictionary[String, Float]:
    Let metrics be Dictionary[String, Float] containing
    
    Note: Basic statistics
    Set metrics["reload_count"] to context.reload_count as Float
    Set metrics["error_count"] to (length of context.error_log) as Float
    Set metrics["module_count"] to (length of context.dependency_graph) as Float
    Set metrics["cache_size"] to (length of context.compilation_cache) as Float
    
    Note: Performance metrics if available
    For each key in keys of context.performance_metrics:
        Set metrics[key] to context.performance_metrics[key]
        
    Return metrics
```

**Example Usage:**
```runa
Let metrics be get_performance_metrics with context as context
Display message "Hot Reload Performance Metrics:"
Display message "  Total Reloads: " plus metrics["reload_count"]
Display message "  Error Count: " plus metrics["error_count"]
Display message "  Modules Tracked: " plus metrics["module_count"]
Display message "  Cache Entries: " plus metrics["cache_size"]

If "avg_reload_time" in metrics:
    Display message "  Average Reload Time: " plus metrics["avg_reload_time"] plus "ms"
If "compilation_time" in metrics:
    Display message "  Last Compilation Time: " plus metrics["compilation_time"] plus "ms"
```

## Complete Example: AI Development Workflow

```runa
Note: Complete example demonstrating AI-powered development with hot reload

Import "advanced/hot_reload/core" as HotReload

Process called "setup_ai_development_environment":
    Note: Create hot reload context for AI development
    Let context be HotReload.create_hot_reload_context()
    
    Note: Configure for AI mode with optimized settings
    Let ai_config be HotReloadConfig with:
        enabled as true
        watch_paths as list containing "src/", "ai_agents/", "prompts/"
        ignore_patterns as list containing "*.tmp", "*.log", ".git/*", "*.cache"
        poll_interval as 0.3  Note: Faster polling for AI responsiveness
        preserve_state as true
        incremental_compilation as true
        cache_enabled as true
        cache_size as 200  Note: Larger cache for AI workloads
        ai_mode as true
        performance_monitoring as true
        metadata as dictionary containing:
            "ai_optimization" as true
            "prompt_caching" as true
            "model_state_preservation" as true
    
    Let config_success be HotReload.configure_hot_reload with context as context and config as ai_config
    
    If config_success:
        Display message "AI development environment configured"
        
        Note: Start file watching
        Let watching_started be HotReload.start_file_watching with context as context
        
        If watching_started:
            Display message "File watching started for AI development"
            
            Note: Build dependency graph for source files
            Let source_files be discover_source_files with paths as ai_config.watch_paths
            Let graph_built be HotReload.build_dependency_graph with context as context and file_paths as source_files
            
            If graph_built:
                Display message "Dependency graph built with " plus (length of context.dependency_graph) plus " modules"
                
                Note: Check for circular dependencies
                Let circular_deps be HotReload.detect_circular_dependencies with context as context
                If length of circular_deps is greater than 0:
                    Display message "WARNING: Circular dependencies detected!"
                    For each cycle in circular_deps:
                        Display message "  Cycle: " plus (cycle joined with " -> ")
                
                Return context
            Otherwise:
                Display message "Failed to build dependency graph"
        Otherwise:
            Display message "Failed to start file watching"
    Otherwise:
        Display message "Failed to configure hot reload"
        
    Return None

Process called "ai_development_loop":
    Let context be setup_ai_development_environment()
    
    If context is not None:
        Display message "Starting AI development loop with hot reload..."
        
        Note: Main development loop
        While true:
            Note: Process file changes
            Let changes be HotReload.process_file_changes with context as context
            
            If length of changes is greater than 0:
                Display message "Detected " plus (length of changes) plus " file changes"
                
                Let changed_files be empty list
                For each change in changes:
                    Add change.file_path to changed_files
                    Display message "  - " plus change.file_path plus " (" plus change.change_type plus ")"
                
                Note: Perform hot reload
                Let reload_success be HotReload.perform_hot_reload with context as context and changed_files as changed_files
                
                If reload_success:
                    Display message "✓ Hot reload completed successfully"
                    
                    Note: Display performance metrics
                    Let metrics be HotReload.get_performance_metrics with context as context
                    Display message "  Reload #" plus metrics["reload_count"] plus " completed"
                    
                    If "avg_reload_time" in metrics:
                        Display message "  Average reload time: " plus metrics["avg_reload_time"] plus "ms"
                        
                Otherwise:
                    Display message "✗ Hot reload failed"
                    Display message "Errors:"
                    For each error in context.error_log:
                        Display message "  - " plus error
            
            Note: Sleep before next check
            Sleep for context.config.poll_interval seconds
    Otherwise:
        Display message "Failed to setup AI development environment"

Note: Start the AI development environment
ai_development_loop()
```

## Best Practices

### Performance Optimization

1. **Adjust Poll Interval**: Use shorter intervals (0.1-0.5s) for active development, longer (1-2s) for background monitoring
2. **Configure Cache Size**: Larger caches (200+) for complex projects, smaller (50-100) for simple modules
3. **Use Ignore Patterns**: Exclude temporary files, logs, and build artifacts to reduce noise
4. **Enable Incremental Compilation**: Always enable for faster reload times

### State Preservation

1. **Preserve Critical State**: Enable state preservation for long-running AI agents and data structures
2. **Handle State Conflicts**: Implement custom state merging for complex objects
3. **Monitor Memory Usage**: Large preserved states can impact performance

### Error Handling

1. **Enable Error Recovery**: Always enable automatic rollback for production environments
2. **Monitor Error Logs**: Regularly check context.error_log for issues
3. **Implement Fallbacks**: Have backup strategies when hot reload fails

### AI Development Integration

1. **Use AI Mode**: Enable ai_mode for optimized AI development workflows
2. **Monitor Dependencies**: AI agents often have complex dependency chains
3. **Cache Prompts and Models**: Preserve expensive AI model states across reloads

## Cross-Platform Considerations

- **Windows**: Uses ReadDirectoryChangesW API for native file monitoring
- **macOS**: Uses FSEvents for efficient file system monitoring  
- **Linux**: Uses inotify for real-time file change detection
- **Fallback**: Polling-based monitoring when native APIs unavailable

The Hot Reload Core module provides enterprise-grade hot reloading capabilities essential for productive Runa development, with special optimizations for AI-first development workflows.