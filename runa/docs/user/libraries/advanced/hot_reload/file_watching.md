# Hot Reload File Watching Module

## Overview

The File Watching module provides comprehensive cross-platform file system monitoring for hot reload systems. It enables real-time detection of file changes using native OS APIs with intelligent fallbacks, advanced filtering, and performance optimization for AI development workflows.

## Key Features

- **Cross-Platform Monitoring**: Native file system APIs (inotify, FSEvents, ReadDirectoryChangesW) with polling fallbacks
- **Real-Time Change Detection**: Immediate notification of file system events (create, modify, delete, move)
- **Advanced Filtering**: Glob patterns, regex matching, and configurable ignore/include rules
- **Event Buffering & Debouncing**: Intelligent event aggregation to prevent excessive reloads
- **Recursive Directory Monitoring**: Watch entire directory trees with configurable depth limits
- **Performance Optimization**: Efficient monitoring for large codebases and AI model directories
- **Event Classification**: Detailed categorization of file system events for intelligent processing

## Core Types

### FileWatcherConfig

Configuration for file watching behavior.

```runa
Type called "FileWatcherConfig":
    watch_paths as List[String] defaults to list containing "."
    recursive as Boolean defaults to true
    max_depth as Integer defaults to 10
    poll_interval as Float defaults to 1.0
    buffer_size as Integer defaults to 1024
    debounce_delay as Float defaults to 0.1
    ignore_patterns as List[String] defaults to list containing "*.tmp", "*.log", ".git/*"
    include_patterns as List[String] defaults to list containing "*.runa"
    event_types as List[String] defaults to list containing "create", "modify", "delete"
    platform_specific as Dictionary[String, Any] defaults to empty dictionary
    metadata as Dictionary[String, Any] defaults to empty dictionary
```

### FileWatchEvent

Represents a detected file system change.

```runa
Type called "FileWatchEvent":
    file_path as String
    event_type as String
    timestamp as Float
    file_size as Integer
    checksum as String
    is_directory as Boolean
    old_path as Optional[String]
    metadata as Dictionary[String, Any]
```

### FileWatcher

Main file watching interface.

```runa
Type called "FileWatcher":
    config as FileWatcherConfig
    is_watching as Boolean
    pending_events as List[FileWatchEvent]
    platform_watcher as Optional[Any]
    event_buffer as List[FileWatchEvent]
    last_event_time as Float
    statistics as Dictionary[String, Integer]
    metadata as Dictionary[String, Any]
```

## Core Functions

### Watcher Creation

#### create_file_watcher

Creates a new file watcher with specified configuration.

```runa
Process called "create_file_watcher" that takes config as FileWatcherConfig returns FileWatcher:
    Let watcher be FileWatcher with:
        config as config
        is_watching as false
        pending_events as empty list
        platform_watcher as None
        event_buffer as empty list
        last_event_time as 0.0
        statistics as dictionary containing:
            "events_processed" as 0
            "files_watched" as 0
            "directories_watched" as 0
            "errors_encountered" as 0
        metadata as empty dictionary
        
    Note: Initialize platform-specific watcher
    Let platform_watcher be create_platform_watcher(config)
    Set watcher.platform_watcher to platform_watcher
    
    Return watcher
```

**Example Usage:**
```runa
Let config be FileWatcherConfig with:
    watch_paths as list containing "src/", "ai_models/"
    recursive as true
    include_patterns as list containing "*.runa", "*.py"
    ignore_patterns as list containing "*.tmp", "__pycache__/*"
    debounce_delay as 0.2

Let watcher be create_file_watcher with config as config
Display message "File watcher created for " plus (length of config.watch_paths) plus " paths"
```

#### start_watching

Begins file system monitoring.

```runa
Process called "start_watching" that takes watcher as FileWatcher returns Boolean:
    Try:
        If watcher.is_watching:
            Display message "File watcher is already running"
            Return true
            
        Note: Validate watch paths
        For each path in watcher.config.watch_paths:
            If not path_exists(path):
                Display message "Warning: Watch path does not exist: " plus path
                
        Note: Start platform-specific monitoring
        If watcher.platform_watcher is not None:
            Let platform_success be start_platform_watcher(watcher.platform_watcher, watcher.config)
            
            If platform_success:
                Set watcher.is_watching to true
                Set watcher.metadata["started_at"] to Common.get_current_timestamp()
                
                Display message "File watching started successfully"
                Display message "Monitoring " plus (length of watcher.config.watch_paths) plus " paths:"
                For each path in watcher.config.watch_paths:
                    Display message "  - " plus path
                    
                Return true
            Otherwise:
                Display message "Failed to start platform-specific file watcher"
                Return false
        Otherwise:
            Display message "No platform watcher available"
            Return false
            
    Catch error:
        Display message "Failed to start file watching: " plus error.message
        Return false
```

**Example Usage:**
```runa
Let watching_started be start_watching with watcher as watcher

If watching_started:
    Display message "✓ File watching active"
    Display message "Debounce delay: " plus watcher.config.debounce_delay plus "s"
    Display message "Include patterns: " plus (watcher.config.include_patterns joined with ", ")
Otherwise:
    Display message "✗ Failed to start file watching"
```

### Event Processing

#### get_pending_events

Retrieves and processes pending file system events.

```runa
Process called "get_pending_events" that takes watcher as FileWatcher returns List[FileWatchEvent]:
    If not watcher.is_watching:
        Return empty list
        
    Try:
        Note: Get raw events from platform watcher
        Let raw_events be get_platform_events(watcher.platform_watcher)
        
        Note: Process and filter events
        Let processed_events be empty list
        
        For each raw_event in raw_events:
            Let processed_event be process_raw_event(raw_event, watcher.config)
            
            If should_include_event(processed_event, watcher.config):
                Add processed_event to watcher.event_buffer
                
        Note: Apply debouncing
        Let current_time be Common.get_current_timestamp()
        Let debounced_events be apply_debouncing(watcher.event_buffer, current_time, watcher.config.debounce_delay)
        
        Note: Update statistics
        Set watcher.statistics["events_processed"] to watcher.statistics["events_processed"] plus length of debounced_events
        Set watcher.last_event_time to current_time
        
        Note: Clear processed events from buffer
        Set watcher.event_buffer to empty list
        
        Return debounced_events
        
    Catch error:
        Set watcher.statistics["errors_encountered"] to watcher.statistics["errors_encountered"] plus 1
        Display message "Error processing file events: " plus error.message
        Return empty list
```

**Example Usage:**
```runa
While watcher.is_watching:
    Let events be get_pending_events with watcher as watcher
    
    If length of events is greater than 0:
        Display message "Detected " plus (length of events) plus " file changes:"
        
        For each event in events:
            Let event_symbol be get_event_symbol(event.event_type)
            Display message "  " plus event_symbol plus " " plus event.file_path
            
            Match event.event_type:
                When "create":
                    Display message "    → New file created"
                When "modify":
                    Display message "    → File modified (size: " plus event.file_size plus " bytes)"
                When "delete":
                    Display message "    → File deleted"
                When "move":
                    If event.old_path is not None:
                        Display message "    → Moved from: " plus event.old_path
    
    Note: Sleep before next check
    Sleep for watcher.config.poll_interval seconds
```

#### process_file_change

Processes a single file change event with detailed analysis.

```runa
Process called "process_file_change" that takes watcher as FileWatcher and event as FileWatchEvent returns FileWatchEvent:
    Try:
        Note: Calculate file checksum for modification detection
        Let checksum be "unknown"
        If event.event_type is equal to "modify" and file_exists(event.file_path):
            Set checksum to calculate_file_checksum(event.file_path)
            
        Note: Enhance event with additional metadata
        Set event.checksum to checksum
        Set event.metadata["processing_time"] to Common.get_current_timestamp()
        Set event.metadata["watcher_id"] to get_watcher_id(watcher)
        
        Note: Classify file change importance
        Let importance be classify_file_importance(event.file_path, watcher.config)
        Set event.metadata["importance"] to importance
        
        Note: Add file type information
        Let file_extension be get_file_extension(event.file_path)
        Set event.metadata["file_type"] to file_extension
        
        Note: Track change frequency for this file
        Let change_frequency be track_file_change_frequency(event.file_path)
        Set event.metadata["change_frequency"] to change_frequency
        
        Return event
        
    Catch error:
        Set event.metadata["processing_error"] to error.message
        Return event
```

**Example Usage:**
```runa
For each raw_event in detected_events:
    Let processed_event be process_file_change with watcher as watcher and event as raw_event
    
    Display message "Processed file change:"
    Display message "  File: " plus processed_event.file_path
    Display message "  Type: " plus processed_event.event_type
    Display message "  Importance: " plus processed_event.metadata["importance"]
    Display message "  Checksum: " plus processed_event.checksum
    
    If processed_event.metadata["importance"] is equal to "high":
        Display message "  ⚠️  High-importance file change detected!"
```

### Advanced Filtering

#### configure_file_patterns

Configures advanced file filtering patterns.

```runa
Process called "configure_file_patterns" that takes watcher as FileWatcher and include_patterns as List[String] and ignore_patterns as List[String] returns Boolean:
    Try:
        Note: Validate pattern syntax
        For each pattern in include_patterns:
            If not is_valid_glob_pattern(pattern):
                Display message "Invalid include pattern: " plus pattern
                Return false
                
        For each pattern in ignore_patterns:
            If not is_valid_glob_pattern(pattern):
                Display message "Invalid ignore pattern: " plus pattern
                Return false
        
        Note: Update configuration
        Set watcher.config.include_patterns to include_patterns
        Set watcher.config.ignore_patterns to ignore_patterns
        
        Note: Compile patterns for performance
        Let compiled_includes be compile_glob_patterns(include_patterns)
        Let compiled_ignores be compile_glob_patterns(ignore_patterns)
        
        Set watcher.metadata["compiled_includes"] to compiled_includes
        Set watcher.metadata["compiled_ignores"] to compiled_ignores
        Set watcher.metadata["patterns_updated"] to Common.get_current_timestamp()
        
        Display message "File patterns updated:"
        Display message "  Include: " plus (include_patterns joined with ", ")
        Display message "  Ignore: " plus (ignore_patterns joined with ", ")
        
        Return true
        
    Catch error:
        Display message "Failed to configure file patterns: " plus error.message
        Return false
```

**Example Usage:**
```runa
Note: Configure patterns for AI development
Let ai_include_patterns be list containing:
    "*.runa"
    "*.py" 
    "*.json"
    "ai_models/*.pt"
    "ai_models/*.safetensors"
    "prompts/*.txt"
    "config/*.yaml"

Let ai_ignore_patterns be list containing:
    "*.tmp"
    "*.log"
    "__pycache__/*"
    ".git/*"
    "*.pyc"
    "checkpoints/temp_*"
    "logs/*"

Let pattern_success be configure_file_patterns with 
    watcher as watcher 
    and include_patterns as ai_include_patterns 
    and ignore_patterns as ai_ignore_patterns

If pattern_success:
    Display message "✓ AI development file patterns configured"
Otherwise:
    Display message "✗ Failed to configure file patterns"
```

### Performance Monitoring

#### get_watcher_statistics

Retrieves comprehensive file watcher performance statistics.

```runa
Process called "get_watcher_statistics" that takes watcher as FileWatcher returns Dictionary[String, Any]:
    Let stats be Dictionary[String, Any] containing
    
    Note: Basic statistics
    Set stats["is_watching"] to watcher.is_watching
    Set stats["events_processed"] to watcher.statistics["events_processed"]
    Set stats["errors_encountered"] to watcher.statistics["errors_encountered"]
    Set stats["watch_paths_count"] to length of watcher.config.watch_paths
    Set stats["include_patterns_count"] to length of watcher.config.include_patterns
    Set stats["ignore_patterns_count"] to length of watcher.config.ignore_patterns
    
    Note: Performance metrics
    If "started_at" in watcher.metadata:
        Let uptime be Common.get_current_timestamp() minus watcher.metadata["started_at"]
        Set stats["uptime_seconds"] to uptime
        
        If watcher.statistics["events_processed"] is greater than 0:
            Set stats["events_per_second"] to (watcher.statistics["events_processed"] as Float) divided by uptime
    
    Note: Configuration details
    Set stats["debounce_delay"] to watcher.config.debounce_delay
    Set stats["poll_interval"] to watcher.config.poll_interval
    Set stats["recursive_watching"] to watcher.config.recursive
    Set stats["max_depth"] to watcher.config.max_depth
    
    Note: Platform information
    Set stats["platform"] to get_current_platform()
    Set stats["platform_watcher_type"] to get_platform_watcher_type(watcher.platform_watcher)
    
    Return stats
```

**Example Usage:**
```runa
Let stats be get_watcher_statistics with watcher as watcher

Display message "File Watcher Statistics:"
Display message "  Status: " plus (if stats["is_watching"] then "Active" else "Inactive")
Display message "  Events processed: " plus stats["events_processed"]
Display message "  Errors: " plus stats["errors_encountered"]
Display message "  Watch paths: " plus stats["watch_paths_count"]

If "uptime_seconds" in stats:
    Display message "  Uptime: " plus stats["uptime_seconds"] plus " seconds"
    
If "events_per_second" in stats:
    Display message "  Event rate: " plus stats["events_per_second"] plus " events/sec"

Display message "  Platform: " plus stats["platform"]
Display message "  Watcher type: " plus stats["platform_watcher_type"]
```

## Platform-Specific Features

### Windows Integration

#### configure_windows_watcher

Configures Windows-specific file watching options.

```runa
Process called "configure_windows_watcher" that takes watcher as FileWatcher and buffer_size as Integer and watch_subtree as Boolean returns Boolean:
    If get_current_platform() is not equal to "windows":
        Display message "Windows-specific configuration only available on Windows platform"
        Return false
        
    Try:
        Let windows_config be dictionary containing:
            "buffer_size" as buffer_size
            "watch_subtree" as watch_subtree
            "notify_filters" as list containing "FILE_NAME", "DIR_NAME", "SIZE", "LAST_WRITE"
            "overlapped_io" as true
            
        Set watcher.config.platform_specific["windows"] to windows_config
        
        Display message "Windows file watcher configured:"
        Display message "  Buffer size: " plus buffer_size plus " bytes"
        Display message "  Watch subtree: " plus watch_subtree
        Display message "  Overlapped I/O: enabled"
        
        Return true
        
    Catch error:
        Display message "Failed to configure Windows watcher: " plus error.message
        Return false
```

### macOS Integration

#### configure_macos_watcher

Configures macOS FSEvents-specific options.

```runa
Process called "configure_macos_watcher" that takes watcher as FileWatcher and latency as Float and flags as List[String] returns Boolean:
    If get_current_platform() is not equal to "macos":
        Display message "macOS-specific configuration only available on macOS platform"
        Return false
        
    Try:
        Let macos_config be dictionary containing:
            "latency" as latency
            "flags" as flags
            "run_loop_mode" as "kCFRunLoopDefaultMode"
            "event_stream_flags" as list containing "kFSEventStreamCreateFlagUseCFTypes"
            
        Set watcher.config.platform_specific["macos"] to macos_config
        
        Display message "macOS file watcher configured:"
        Display message "  Latency: " plus latency plus " seconds"
        Display message "  Flags: " plus (flags joined with ", ")
        
        Return true
        
    Catch error:
        Display message "Failed to configure macOS watcher: " plus error.message
        Return false
```

### Linux Integration

#### configure_linux_watcher

Configures Linux inotify-specific options.

```runa
Process called "configure_linux_watcher" that takes watcher as FileWatcher and watch_mask as List[String] and buffer_size as Integer returns Boolean:
    If get_current_platform() is not equal to "linux":
        Display message "Linux-specific configuration only available on Linux platform"
        Return false
        
    Try:
        Let linux_config be dictionary containing:
            "watch_mask" as watch_mask
            "buffer_size" as buffer_size
            "event_types" as list containing "IN_CREATE", "IN_MODIFY", "IN_DELETE", "IN_MOVED_FROM", "IN_MOVED_TO"
            "recursive_support" as true
            
        Set watcher.config.platform_specific["linux"] to linux_config
        
        Display message "Linux file watcher configured:"
        Display message "  Watch mask: " plus (watch_mask joined with ", ")
        Display message "  Buffer size: " plus buffer_size plus " bytes"
        
        Return true
        
    Catch error:
        Display message "Failed to configure Linux watcher: " plus error.message
        Return false
```

## Complete Example: AI Model Development Workflow

```runa
Note: Complete example for AI model development with intelligent file watching

Import "advanced/hot_reload/file_watching" as FileWatch

Process called "setup_ai_model_file_watching":
    Note: Configure file watcher for AI development
    Let ai_config be FileWatcherConfig with:
        watch_paths as list containing:
            "ai_models/"
            "training_data/"
            "prompts/"
            "config/"
            "src/ai_agents/"
        recursive as true
        max_depth as 5
        poll_interval as 0.5
        debounce_delay as 0.3
        include_patterns as list containing:
            "*.runa"
            "*.py"
            "*.pt"           Note: PyTorch models
            "*.safetensors"  Note: SafeTensors format
            "*.json"
            "*.yaml"
            "*.txt"          Note: Prompt files
            "*.md"           Note: Documentation
        ignore_patterns as list containing:
            "*.tmp"
            "*.log"
            "__pycache__/*"
            ".git/*"
            "*.pyc"
            "checkpoints/temp_*"
            "logs/*"
            "wandb/*"        Note: Weights & Biases logs
            ".vscode/*"
        event_types as list containing "create", "modify", "delete", "move"
        metadata as dictionary containing:
            "purpose" as "ai_model_development"
            "auto_reload" as true
            "model_validation" as true
    
    Let watcher be FileWatch.create_file_watcher with config as ai_config
    
    Note: Configure platform-specific optimizations
    Let platform be get_current_platform()
    
    Match platform:
        When "windows":
            FileWatch.configure_windows_watcher with 
                watcher as watcher 
                and buffer_size as 8192 
                and watch_subtree as true
        When "macos":
            FileWatch.configure_macos_watcher with 
                watcher as watcher 
                and latency as 0.1 
                and flags as list containing "FileEvents", "WatchRoot"
        When "linux":
            FileWatch.configure_linux_watcher with 
                watcher as watcher 
                and watch_mask as list containing "IN_CREATE", "IN_MODIFY", "IN_DELETE"
                and buffer_size as 4096
    
    Return watcher

Process called "ai_model_development_loop":
    Let watcher be setup_ai_model_file_watching()
    
    Display message "🤖 Starting AI Model Development File Watching"
    Display message "Platform: " plus get_current_platform()
    
    Let watching_started be FileWatch.start_watching with watcher as watcher
    
    If not watching_started:
        Display message "❌ Failed to start file watching"
        Return
    
    Display message "✅ File watching active for AI development"
    
    Note: Main development loop
    Let iteration_count be 0
    
    While watcher.is_watching and iteration_count is less than 1000:  Note: Limit for demo
        Set iteration_count to iteration_count plus 1
        
        Let events be FileWatch.get_pending_events with watcher as watcher
        
        If length of events is greater than 0:
            Display message "\n📁 Detected " plus (length of events) plus " file changes (iteration " plus iteration_count plus "):"
            
            Let model_files_changed be empty list
            Let prompt_files_changed be empty list
            Let config_files_changed be empty list
            Let code_files_changed be empty list
            
            For each event in events:
                Let processed_event be FileWatch.process_file_change with watcher as watcher and event as event
                
                Let file_type be get_file_type_category(processed_event.file_path)
                Let importance be processed_event.metadata["importance"]
                
                Display message "  " plus get_event_symbol(processed_event.event_type) plus " " plus processed_event.file_path
                Display message "    Type: " plus file_type plus " | Importance: " plus importance
                
                Match file_type:
                    When "model":
                        Add processed_event.file_path to model_files_changed
                        Display message "    🧠 AI model file detected"
                    When "prompt":
                        Add processed_event.file_path to prompt_files_changed
                        Display message "    💬 Prompt template updated"
                    When "config":
                        Add processed_event.file_path to config_files_changed
                        Display message "    ⚙️  Configuration change"
                    When "code":
                        Add processed_event.file_path to code_files_changed
                        Display message "    🔧 Source code modified"
            
            Note: Handle different types of changes
            If length of model_files_changed is greater than 0:
                Display message "\n🔄 Model files changed - triggering validation:"
                For each model_file in model_files_changed:
                    Display message "  • Validating " plus model_file
                    validate_ai_model(model_file)
            
            If length of prompt_files_changed is greater than 0:
                Display message "\n💭 Prompt templates updated - reloading prompts:"
                For each prompt_file in prompt_files_changed:
                    Display message "  • Reloading " plus prompt_file
                    reload_prompt_template(prompt_file)
            
            If length of config_files_changed is greater than 0:
                Display message "\n⚙️  Configuration updated - applying changes:"
                For each config_file in config_files_changed:
                    Display message "  • Applying " plus config_file
                    apply_configuration_change(config_file)
            
            If length of code_files_changed is greater than 0:
                Display message "\n🔧 Source code changed - hot reloading:"
                For each code_file in code_files_changed:
                    Display message "  • Hot reloading " plus code_file
                    perform_hot_reload(code_file)
            
            Note: Display performance statistics every 10 iterations with changes
            If (iteration_count modulo 10) is equal to 0:
                Let stats be FileWatch.get_watcher_statistics with watcher as watcher
                Display message "\n📊 File Watcher Performance:"
                Display message "  Events processed: " plus stats["events_processed"]
                Display message "  Uptime: " plus stats["uptime_seconds"] plus "s"
                If "events_per_second" in stats:
                    Display message "  Event rate: " plus stats["events_per_second"] plus " events/sec"
        
        Note: Sleep before next check
        Sleep for watcher.config.poll_interval seconds
    
    Display message "\n🏁 AI model development watching completed"
    Display message "Total iterations: " plus iteration_count

Note: Helper functions for AI model development
Process called "validate_ai_model" that takes model_path as String:
    Display message "    ✓ Model validation completed for " plus model_path

Process called "reload_prompt_template" that takes prompt_path as String:
    Display message "    ✓ Prompt template reloaded: " plus prompt_path

Process called "apply_configuration_change" that takes config_path as String:
    Display message "    ✓ Configuration applied: " plus config_path

Process called "perform_hot_reload" that takes code_path as String:
    Display message "    ✓ Hot reload completed: " plus code_path

Process called "get_file_type_category" that takes file_path as String returns String:
    If file_path contains "models/" and (file_path ends with ".pt" or file_path ends with ".safetensors"):
        Return "model"
    Otherwise if file_path contains "prompts/":
        Return "prompt"
    Otherwise if file_path contains "config/":
        Return "config"
    Otherwise:
        Return "code"

Process called "get_event_symbol" that takes event_type as String returns String:
    Match event_type:
        When "create":
            Return "+"
        When "modify":
            Return "•"
        When "delete":
            Return "-"
        When "move":
            Return "→"
        Otherwise:
            Return "?"

Note: Start the AI model development file watching
ai_model_development_loop()
```

## Best Practices

### Performance Optimization

1. **Choose Appropriate Debounce Delays**: Shorter delays (0.1-0.2s) for active development, longer (0.5-1s) for production
2. **Optimize Include/Ignore Patterns**: Use specific patterns to reduce event volume
3. **Configure Platform-Specific Settings**: Tune buffer sizes and polling intervals for your platform
4. **Monitor Event Rates**: Track events/second to identify performance bottlenecks

### File Pattern Configuration

1. **Be Specific with Includes**: Target only files relevant to your development workflow
2. **Comprehensive Ignores**: Exclude temporary files, build artifacts, and version control directories
3. **Use Compiled Patterns**: Pre-compile regex patterns for performance in high-volume scenarios
4. **Regular Pattern Review**: Periodically review and optimize patterns based on usage

### Cross-Platform Considerations

1. **Test on Target Platforms**: Verify file watching behavior across Windows, macOS, and Linux
2. **Handle Platform Limitations**: Some platforms have limits on watched files/directories
3. **Graceful Fallbacks**: Ensure polling fallback works when native APIs fail
4. **Path Separators**: Use platform-appropriate path separators and normalization

### AI Development Workflow Integration

1. **Model File Monitoring**: Watch for changes in model weights, configurations, and training data
2. **Prompt Template Tracking**: Monitor prompt files for AI agent development
3. **Configuration Management**: Track changes in AI model configurations and hyperparameters
4. **Smart Filtering**: Filter out temporary training files and checkpoints that don't need hot reloading

The File Watching module provides the foundation for responsive AI development environments, enabling immediate feedback and rapid iteration cycles essential for modern AI-first development workflows.