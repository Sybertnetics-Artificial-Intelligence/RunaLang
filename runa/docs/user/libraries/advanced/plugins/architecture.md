# Plugin Architecture Module

The Plugin Architecture module defines the architecture and design patterns for robust, extensible, and secure plugin systems in the Runa Advanced Plugins Library.

## Overview

This module provides the architectural foundation and design patterns necessary for building scalable plugin ecosystems. It defines extension points, dependency management, plugin isolation, and version compatibility strategies that enable complex applications to remain maintainable and secure.

### Key Features

- **Extension Point System**: Structured extension points with schema validation
- **Plugin System Architecture**: Modular system design with clear boundaries
- **Dependency Resolution**: Advanced dependency graph analysis and resolution
- **Plugin Isolation**: Security and resource isolation mechanisms
- **Version Management**: Compatibility checking and upgrade strategies
- **Plugin Marketplace**: Integration with plugin registries and repositories
- **Architecture Patterns**: Best practices and design patterns for plugin systems

## Core Types

### PluginSystem

The central architecture that coordinates all plugin operations:

```runa
Type called "PluginSystem":
    plugins as Dictionary[String, Plugin]                    # Registered plugins
    extension_points as Dictionary[String, ExtensionPoint]    # Available extension points
    dependencies as Dictionary[String, List[String]]         # Dependency relationships
    isolation_manager as PluginIsolationManager             # Isolation management
    version_manager as PluginVersionManager                 # Version management
    metadata as Dictionary[String, Any]                     # System metadata
```

### ExtensionPoint

Defines points where plugins can extend application functionality:

```runa
Type called "ExtensionPoint":
    extension_id as String                 # Unique extension point identifier
    name as String                        # Human-readable name
    description as String                 # Extension point description
    register as Function that takes extension as Any returns None
    unregister as Function that takes extension_id as String returns None
    metadata as Dictionary[String, Any]   # Extension point metadata
```

### ExtensionPointSchema

Advanced schema-based extension points with validation:

```runa
Type called "ExtensionPointSchema":
    extension_point_id as String              # Extension point identifier
    name as String                           # Extension point name
    description as String                    # Description of the extension point
    schema as JSONSchema                     # Validation schema
    required_attributes as List[String]      # Required extension attributes
    optional_attributes as List[String]      # Optional extension attributes
    child_elements as List[ExtensionElementSchema]  # Child element schemas
    metadata as Dictionary[String, Any]      # Additional metadata
```

## Key Functions

### Plugin System Management

#### create_plugin_system

Creates a new plugin system with all necessary components:

```runa
Process called "create_plugin_system" returns PluginSystem:
    Return PluginSystem with:
        plugins as dictionary containing
        extension_points as _extension_registry
        dependencies as _dependency_graph
        isolation_manager as create_plugin_isolation_manager()
        version_manager as create_plugin_version_manager()
        metadata as dictionary containing
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/architecture" as Architecture

Let plugin_system be Architecture.create_plugin_system()
Log message "Plugin system initialized"
Log message "Extension points: " plus length of plugin_system.extension_points
Log message "Isolation manager ready: " plus (plugin_system.isolation_manager is not None)
```

### Extension Point Management

#### create_extension_point_with_schema

Creates a schema-validated extension point:

```runa
Process called "create_extension_point_with_schema" that takes id as String and schema as ExtensionPointSchema returns ExtensionPoint:
    Let extension_point be ExtensionPoint with:
        extension_id as id
        name as schema.name
        description as schema.description
        register as function(extension):
            validate_extension_against_schema(extension, schema)
            register_validated_extension(id, extension)
        unregister as function(extension_id):
            unregister_extension_safely(id, extension_id)
        metadata as schema.metadata
    Set _extension_registry[id] to extension_point
    Return extension_point
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/architecture" as Architecture

Note: Define a schema for command extensions
Let command_schema be Architecture.ExtensionPointSchema with:
    extension_point_id as "ui.commands"
    name as "UI Commands"
    description as "Extension point for UI command contributions"
    required_attributes as list containing "id", "name", "handler"
    optional_attributes as list containing "icon", "tooltip", "shortcut"
    metadata as dictionary containing

Let command_extension_point be Architecture.create_extension_point_with_schema("ui.commands", command_schema)

Note: Register the extension point with the system
Let system be Architecture.create_plugin_system()
Architecture.register_extension_point(system, command_extension_point)
```

#### register_extension_point

Registers an extension point with the plugin system:

```runa
Process called "register_extension_point" that takes system as PluginSystem and extension_point as ExtensionPoint returns Boolean:
    If extension_point.extension_id in system.extension_points:
        Return false
    Set system.extension_points[extension_point.extension_id] to extension_point
    Return true
```

## Dependency Management

### DependencyResolver

Advanced dependency resolution with cycle detection:

```runa
Type called "DependencyResolver":
    resolve_dependencies as Function that takes plugins as List[Plugin] returns DependencyGraph
    check_circular_dependencies as Function that takes graph as DependencyGraph returns Boolean
    resolve_load_order as Function that takes graph as DependencyGraph returns List[String]
    metadata as Dictionary[String, Any]
```

### DependencyGraph

Represents plugin dependencies as a directed graph:

```runa
Type called "DependencyGraph":
    nodes as Dictionary[String, DependencyNode]    # Plugin nodes
    edges as Dictionary[String, List[String]]      # Dependency edges
    metadata as Dictionary[String, Any]            # Graph metadata
```

#### build_dependency_graph

Constructs a dependency graph from a list of plugins:

```runa
Process called "build_dependency_graph" that takes plugins as List[Plugin] returns DependencyGraph:
    Let graph be DependencyGraph with:
        nodes as dictionary containing
        edges as dictionary containing
        metadata as dictionary containing
    
    For each plugin in plugins:
        Let node be DependencyNode with:
            plugin_id as plugin.plugin_id
            dependencies as get_plugin_dependencies(plugin)
            dependents as list containing
            metadata as dictionary containing
        Set graph.nodes[plugin.plugin_id] to node
        Set graph.edges[plugin.plugin_id] to get_plugin_dependencies(plugin)
    
    Return graph
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/architecture" as Architecture

Let resolver be Architecture.create_dependency_resolver()
Let plugins be list containing plugin1, plugin2, plugin3

Note: Build dependency graph
Let dependency_graph be Architecture.build_dependency_graph(plugins)

Note: Check for circular dependencies
If resolver.check_circular_dependencies(dependency_graph):
    Log error message "Circular dependency detected!"
    Return false

Note: Get proper load order
Let load_order be resolver.resolve_load_order(dependency_graph)
Log message "Load order: " plus join_list(load_order, " -> ")
```

#### detect_cycles_in_graph

Detects circular dependencies in the plugin graph:

```runa
Process called "detect_cycles_in_graph" that takes graph as DependencyGraph returns Boolean:
    Let visited be dictionary containing
    Let rec_stack be dictionary containing
    
    For each node_id in keys of graph.nodes:
        Set visited[node_id] to false
        Set rec_stack[node_id] to false
    
    For each node_id in keys of graph.nodes:
        If not visited[node_id]:
            If has_cycle_from_node(graph, node_id, visited, rec_stack):
                Return true
    
    Return false
```

### Plugin Isolation

#### isolate_plugin

Isolates a plugin within the system for security and stability:

```runa
Process called "isolate_plugin" that takes system as PluginSystem and plugin_id as String returns Boolean:
    If plugin_id not in system.plugins:
        Return false
    Acquire _extension_locks[plugin_id]
    Set _isolation_state[plugin_id] to true
    Release _extension_locks[plugin_id]
    Return system.isolation_manager.isolate_plugin with plugin_id as plugin_id
```

**Usage Example:**
```runa
Let system be Architecture.create_plugin_system()

Note: Add a plugin to the system
Set system.plugins["untrusted-plugin"] to untrusted_plugin

Note: Isolate the plugin for security
If Architecture.isolate_plugin(system, "untrusted-plugin"):
    Log message "Plugin isolated successfully"
    
    Note: Plugin can still function but with restricted access
    Note: Release isolation when appropriate
    Architecture.release_plugin(system, "untrusted-plugin")
```

## Version Management

### PluginVersionManager

Manages plugin version compatibility and upgrades:

```runa
Type called "PluginVersionManager":
    check_compatibility as Function that takes plugin as Plugin returns Boolean
    upgrade_plugin as Function that takes plugin_id as String and new_version as String returns Boolean
    metadata as Dictionary[String, Any]
```

#### check_plugin_compatibility

Validates plugin compatibility with the current system:

```runa
Process called "check_plugin_compatibility" that takes system as PluginSystem and plugin as Plugin returns Boolean:
    Return system.version_manager.check_compatibility with plugin as plugin
```

#### is_compatible_version

Checks semantic version compatibility:

```runa
Process called "is_compatible_version" that takes version1 as String and version2 as String returns Boolean:
    Let v1_parts be split_string with string as version1 and delimiter as "."
    Let v2_parts be split_string with string as version2 and delimiter as "."
    If length of v1_parts is not equal to 3 or length of v2_parts is not equal to 3:
        Return false
    Let v1_major be parse_integer(v1_parts[0])
    Let v2_major be parse_integer(v2_parts[0])
    Return v1_major is equal to v2_major
```

**Usage Example:**
```runa
Let system be Architecture.create_plugin_system()

Note: Check if plugin is compatible before loading
If Architecture.check_plugin_compatibility(system, new_plugin):
    Log message "Plugin " plus new_plugin.name plus " is compatible"
    Note: Safe to load and use
Otherwise:
    Log error message "Plugin " plus new_plugin.name plus " is not compatible"
    Note: Need to upgrade plugin or system
```

## Plugin Marketplace Integration

### PluginMarketplace

Integrates with external plugin repositories:

```runa
Type called "PluginMarketplace":
    search_plugins as Function that takes query as String returns List[PluginInfo]
    install_plugin as Function that takes plugin_id as String returns Boolean
    update_plugin as Function that takes plugin_id as String returns Boolean
    uninstall_plugin as Function that takes plugin_id as String returns Boolean
    metadata as Dictionary[String, Any]
```

### PluginInfo

Represents plugin information from the marketplace:

```runa
Type called "PluginInfo":
    plugin_id as String              # Unique plugin identifier
    name as String                   # Plugin name
    description as String            # Plugin description
    version as String               # Current version
    author as String                # Plugin author
    rating as Float                 # User rating (0.0-5.0)
    download_count as Integer       # Number of downloads
    tags as List[String]            # Plugin tags
    metadata as Dictionary[String, Any]  # Additional metadata
```

#### search_marketplace_plugins

Searches for plugins in the marketplace:

```runa
Process called "search_marketplace_plugins" that takes query as String returns List[PluginInfo]:
    Note: Production implementation would query actual marketplace API
    Let results be list containing
    Return results
```

**Usage Example:**
```runa
Let marketplace be Architecture.create_plugin_marketplace()

Note: Search for data processing plugins
Let search_results be marketplace.search_plugins("data processing")
For each plugin_info in search_results:
    Log message "Found: " plus plugin_info.name plus " (" plus plugin_info.rating plus " stars)"
    
Note: Install a specific plugin
If marketplace.install_plugin("com.example.data-processor"):
    Log message "Plugin installed successfully"
```

## Advanced Architecture Patterns

### Plugin Containers

Containerized plugin execution for maximum isolation:

```runa
Type called "PluginContainer":
    container_id as String                        # Container identifier
    plugin_id as String                          # Associated plugin
    runtime_info as ContainerRuntimeInfo         # Runtime configuration
    security_context as SecurityContext          # Security settings
    resource_constraints as ResourceConstraints   # Resource limits
    metadata as Dictionary[String, Any]          # Container metadata
```

#### create_plugin_container

Creates a containerized environment for a plugin:

```runa
Process called "create_plugin_container" that takes plugin_id as String and config as ContainerConfig returns PluginContainer:
    Return PluginContainer with:
        container_id as generate_uuid()
        plugin_id as plugin_id
        runtime_info as ContainerRuntimeInfo with:
            image as config.image
            command as config.command
            environment as config.environment
            working_directory as config.working_directory
            metadata as dictionary containing
        security_context as SecurityContext with:
            user_id as config.user_id
            group_id as config.group_id
            capabilities as config.capabilities
            seccomp_profile as config.seccomp_profile
            selinux_context as config.selinux_context
            metadata as dictionary containing
        resource_constraints as ResourceConstraints with:
            cpu_limit as config.cpu_limit
            memory_limit as config.memory_limit
            disk_limit as config.disk_limit
            network_bandwidth as config.network_bandwidth
            file_descriptors as config.file_descriptors
            metadata as dictionary containing
        metadata as dictionary containing
```

## Best Practices

### 1. **Extension Point Design**
Design extension points with clear contracts:

```runa
Note: Good extension point design
Let ui_extension_schema be Architecture.ExtensionPointSchema with:
    extension_point_id as "ui.menu.items"
    name as "Menu Items"
    description as "Contributes menu items to the application UI"
    required_attributes as list containing:
        "id"           # Unique identifier
        "label"        # Display text
        "action"       # Function to execute
    optional_attributes as list containing:
        "icon"         # Menu item icon
        "shortcut"     # Keyboard shortcut
        "group"        # Menu group for organization
        "enabled"      # Enable/disable condition
    metadata as dictionary with:
        "version" as "1.0"
        "documentation" as "https://docs.example.com/ui-extensions"
```

### 2. **Dependency Management**
Organize plugins with clear dependency hierarchies:

```runa
Process called "validate_plugin_architecture" that takes plugins as List[Plugin] returns ArchitectureReport:
    Let resolver be Architecture.create_dependency_resolver()
    Let graph be Architecture.build_dependency_graph(plugins)
    
    Let report be ArchitectureReport with:
        has_cycles as resolver.check_circular_dependencies(graph)
        load_order as resolver.resolve_load_order(graph)
        max_depth as calculate_dependency_depth(graph)
        isolated_plugins as find_isolated_plugins(graph)
        recommendations as list containing
    
    Note: Add recommendations
    If report.max_depth is greater than 5:
        Add "Consider reducing dependency depth" to report.recommendations
    
    If length of report.isolated_plugins is greater than 0:
        Add "Consider connecting isolated plugins" to report.recommendations
    
    Return report
```

### 3. **Version Compatibility Strategy**
Implement semantic versioning with clear compatibility rules:

```runa
Process called "check_system_compatibility" that takes system as PluginSystem returns CompatibilityReport:
    Let report be CompatibilityReport with:
        compatible_plugins as list containing
        incompatible_plugins as list containing
        upgrade_required as list containing
        warnings as list containing
    
    For each plugin_id, plugin in system.plugins:
        If Architecture.check_plugin_compatibility(system, plugin):
            Add plugin to report.compatible_plugins
        Otherwise:
            Add plugin to report.incompatible_plugins
            Note: Check if upgrade is available
            Let latest_version be get_latest_version(plugin_id)
            If latest_version is not None and is_newer_version(latest_version, plugin.version):
                Add plugin to report.upgrade_required
    
    Return report
```

### 4. **Security Architecture**
Implement defense-in-depth for plugin security:

```runa
Process called "secure_plugin_architecture" that takes system as PluginSystem:
    Note: Apply security policies to all plugins
    For each plugin_id, plugin in system.plugins:
        Note: Isolate untrusted plugins
        If not is_trusted_plugin(plugin):
            Architecture.isolate_plugin(system, plugin_id)
        
        Note: Apply resource limits
        Let limits be calculate_safe_resource_limits(plugin)
        apply_resource_constraints(plugin_id, limits)
        
        Note: Audit plugin permissions
        audit_plugin_permissions(plugin_id)
```

## Integration Examples

### With Discovery and Loading

```runa
Import "stdlib/advanced/plugins/architecture" as Architecture
Import "stdlib/advanced/plugins/discovery" as Discovery
Import "stdlib/advanced/plugins/loading" as Loading

Note: Create a complete plugin system
Let system be Architecture.create_plugin_system()
Let discovery be Discovery.create_plugin_discovery()
Let loader = Loading.create_plugin_loader()

Note: Discover and validate architecture
Let discovered_plugins be Discovery.scan_plugins(discovery, "/plugins")
Let resolver be Architecture.create_dependency_resolver()
Let dependency_graph be Architecture.build_dependency_graph(discovered_plugins)

If not resolver.check_circular_dependencies(dependency_graph):
    Let load_order be resolver.resolve_load_order(dependency_graph)
    
    Note: Load plugins in proper order
    For each plugin_id in load_order:
        Let plugin_path be get_plugin_path(plugin_id)
        Let plugin be Loading.load_plugin(loader, plugin_path)
        
        Note: Add to system architecture
        Set system.plugins[plugin_id] to plugin
        
        Note: Apply isolation if needed
        If requires_isolation(plugin):
            Architecture.isolate_plugin(system, plugin_id)
```

### With Management and Sandboxing

```runa
Import "stdlib/advanced/plugins/architecture" as Architecture
Import "stdlib/advanced/plugins/management" as Management
Import "stdlib/advanced/plugins/sandboxing" as Sandboxing

Note: Create enterprise-grade plugin architecture
Let system be Architecture.create_plugin_system()
Let manager be Management.create_plugin_manager()
Let sandbox be Sandboxing.create_plugin_sandbox()

Note: Define security policies for different plugin types
Let untrusted_policy be create_restrictive_security_policy()
Let trusted_policy be create_permissive_security_policy()

For each plugin_id, plugin in system.plugins:
    Note: Apply appropriate security model
    If is_trusted_plugin(plugin):
        Sandboxing.enforce_policy(sandbox, plugin_id, trusted_policy)
    Otherwise:
        Architecture.isolate_plugin(system, plugin_id)
        Sandboxing.enforce_policy(sandbox, plugin_id, untrusted_policy)
    
    Note: Enable management control
    manager.enable_plugin(plugin_id)
```

## Comparative Notes

### Advantages over Other Plugin Architectures

**vs. Eclipse RCP:**
- Simpler extension point registration
- Better dependency resolution algorithms
- Modern containerization support
- AI-friendly architecture patterns

**vs. Visual Studio Code Extensions:**
- Type-safe extension contracts
- Advanced security isolation
- Built-in marketplace integration
- Performance monitoring capabilities

**vs. Firefox Add-ons:**
- Unified architecture across platforms
- Better resource management
- Structured dependency resolution
- Modern development tools

The Runa Plugin Architecture module provides a modern, secure, and scalable foundation for building complex plugin ecosystems with enterprise-grade reliability and maintainability.