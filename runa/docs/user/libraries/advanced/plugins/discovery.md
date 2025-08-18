# Plugin Discovery Module

The Plugin Discovery module provides comprehensive mechanisms for discovering, scanning, and validating plugins at runtime and compile time in the Runa Advanced Plugins Library.

## Overview

This module handles the automated discovery of plugins across file systems, registries, and remote repositories. It provides robust validation, compatibility checking, and metadata extraction capabilities essential for building reliable plugin ecosystems.

### Key Features

- **Automatic Plugin Scanning**: Discovers plugins from directories, manifests, and registries
- **Metadata Extraction**: Parses plugin.toml manifests and extracts comprehensive metadata
- **Compatibility Validation**: Checks Runa version compatibility and dependency requirements
- **Dynamic Discovery**: Runtime plugin discovery with hot-reloading support
- **Error Handling**: Robust error recovery and detailed diagnostics
- **Security Validation**: Verifies plugin integrity and security constraints

## Core Types

### PluginDiscovery Interface

```runa
Type called "PluginDiscovery":
    scan_plugins as Function that takes path as String returns List[Plugin]
    extract_metadata as Function that takes plugin_path as String returns PluginMetadata
    check_compatibility as Function that takes plugin as Plugin returns Boolean
    dynamic_discovery as Boolean
    metadata as Dictionary[String, Any]
```

### PluginMetadata

```runa
Type called "PluginMetadata":
    plugin_id as String                    # Unique plugin identifier
    name as String                         # Human-readable plugin name
    version as String                      # Semantic version
    author as String                       # Plugin author
    description as String                  # Plugin description
    entry_point as String                  # Main entry point file
    compatible_versions as List[String]     # Compatible Runa versions
    metadata as Dictionary[String, Any]     # Additional metadata
```

### Plugin Manifest Structure

```runa
Type called "PluginManifest":
    plugin as PluginInfo                   # Core plugin information
    compatibility as CompatibilityInfo     # Version and platform compatibility
    dependencies as Dictionary[String, String]  # Plugin dependencies
    capabilities as CapabilityInfo         # Required and provided capabilities
    configuration as ConfigurationInfo     # Configuration schema
    build as BuildInfo                     # Build and asset information
```

## Key Functions

### Plugin Scanning

#### scan_plugins

Scans a directory for plugins and returns a list of discovered, validated plugins.

```runa
Process called "scan_plugins" that takes discovery as PluginDiscovery and path as String returns List[Plugin]:
    Let plugin_files be list_plugin_files(path)
    Let plugins be list containing
    For each file in plugin_files:
        Try:
            Let metadata be discovery.extract_metadata with plugin_path as file
            If metadata.plugin_id in _discovered_plugins:
                Add "Duplicate plugin ID: " plus metadata.plugin_id to _discovery_errors
                Continue
            Set _discovered_plugins[metadata.plugin_id] to metadata
            If discovery.check_compatibility with plugin as metadata:
                Let plugin be load_plugin_from_metadata(metadata)
                Append plugin to plugins
            Else:
                Add "Incompatible plugin: " plus metadata.plugin_id to _discovery_errors
        Catch error:
            Add "Error loading plugin from " plus file plus ": " plus error.message to _discovery_errors
    Return plugins
```

**Usage Example:**
```runa
Import "stdlib/advanced/plugins/discovery" as Discovery

Let discovery be Discovery.create_plugin_discovery()
Let plugins be Discovery.scan_plugins(discovery, "/plugins")

For each plugin in plugins:
    Log message "Discovered plugin: " plus plugin.name plus " v" plus plugin.version
```

### Metadata Extraction

#### extract_plugin_metadata

Extracts and validates metadata from a plugin directory's manifest file.

```runa
Process called "extract_plugin_metadata" that takes discovery as PluginDiscovery and plugin_path as String returns PluginMetadata:
    Let manifest_path be plugin_path plus "/plugin.toml"
    Let manifest be parse_toml_file with path as manifest_path
    If not manifest:
        Throw PluginDiscoveryError with message "Missing or invalid manifest at " plus manifest_path
    Return PluginMetadata with:
        plugin_id as manifest.plugin.id
        name as manifest.plugin.name
        version as manifest.plugin.version
        author as manifest.plugin.author
        description as manifest.plugin.description
        entry_point as manifest.plugin.entry_point
        compatible_versions as manifest.compatibility.platform
        metadata as manifest.plugin
```

**Usage Example:**
```runa
Let discovery be Discovery.create_plugin_discovery()
Let metadata be Discovery.extract_plugin_metadata(discovery, "/plugins/my-plugin")

Log message "Plugin: " plus metadata.name
Log message "Version: " plus metadata.version
Log message "Author: " plus metadata.author
```

### Compatibility Checking

#### check_plugin_compatibility

Validates that a plugin is compatible with the current Runa version and environment.

```runa
Process called "check_plugin_compatibility" that takes discovery as PluginDiscovery and plugin as Plugin returns Boolean:
    If not is_valid_semver(plugin.version):
        Return false
    If not is_compatible_runa_version(plugin.compatible_versions):
        Return false
    Return true
```

**Usage Example:**
```runa
Let discovery be Discovery.create_plugin_discovery()
If Discovery.check_plugin_compatibility(discovery, plugin):
    Log message "Plugin is compatible"
Otherwise:
    Log error message "Plugin compatibility check failed"
```

## Plugin Manifest Format

The plugin.toml manifest file follows this structure:

```toml
[plugin]
id = "com.example.my-plugin"
name = "My Awesome Plugin"
version = "1.0.0"
author = "John Doe"
description = "An example plugin demonstrating the Runa plugin system"
license = "MIT"
repository = "https://github.com/example/my-plugin"
homepage = "https://example.com/my-plugin"
entry_point = "main.runa"

[compatibility]
runa_version = ">=1.0.0"
platform = ["linux", "windows", "macos"]
architecture = ["x86_64", "arm64"]

[dependencies]
"other-plugin" = "^2.0.0"
"utility-lib" = ">=1.5.0"

[capabilities]
requires = ["ui.commands", "file.system"]
provides = ["example.service", "data.processor"]

[configuration]
default_config = "config/default.toml"
schema = "config/schema.json"

[build]
build_script = "scripts/build.runa"
assets = ["assets/*", "templates/*"]
exclude = ["tests/*", "docs/*"]
```

## Validation and Error Handling

### Manifest Validation

```runa
Process called "validate_plugin_manifest" that takes manifest as PluginManifest returns ValidationResult:
    Let errors be list containing
    If manifest.plugin.id is empty:
        Add "Plugin ID is required" to errors
    If not is_valid_semver(manifest.plugin.version):
        Add "Invalid semantic version format" to errors
    If not is_compatible_runa_version(manifest.compatibility.runa_version):
        Add "Incompatible Runa version requirement" to errors
    For each dependency_name and version_spec in manifest.dependencies:
        If not is_valid_version_spec(version_spec):
            Add "Invalid version specification for dependency: " plus dependency_name to errors
    For each capability in manifest.capabilities.requires:
        If not is_known_capability(capability):
            Add "Unknown capability required: " plus capability to errors
    Return ValidationResult with:
        is_valid as (length of errors is equal to 0)
        errors as errors
```

### Error Types

```runa
Type PluginDiscoveryError is Exception with:
    message as String
    metadata as Dictionary[String, Any]
```

## Advanced Features

### Dynamic Discovery

Enable automatic discovery of newly added plugins without restarting the application:

```runa
Let discovery be Discovery.create_plugin_discovery()
Set discovery.dynamic_discovery to true

Note: Discovery will automatically detect new plugins
Let new_plugins be Discovery.scan_plugins(discovery, "/plugins")
```

### Version Compatibility

The discovery system supports semantic versioning with compatibility operators:

- `>=1.0.0` - Minimum version requirement
- `<=2.0.0` - Maximum version requirement  
- `=1.5.0` - Exact version requirement
- `^1.0.0` - Compatible within major version
- `~1.0.0` - Compatible within minor version

### Capability-Based Discovery

Filter plugins based on required capabilities:

```runa
Let discovery be Discovery.create_plugin_discovery()
Let plugins be Discovery.scan_plugins(discovery, "/plugins")

For each plugin in plugins:
    Let manifest be Discovery.extract_plugin_metadata(discovery, plugin.path)
    If "ui.commands" in manifest.capabilities.provides:
        Log message "Found UI plugin: " plus plugin.name
```

## Best Practices

### 1. **Validation First**
Always validate plugins before loading:

```runa
Let discovery be Discovery.create_plugin_discovery()
Let metadata be Discovery.extract_plugin_metadata(discovery, plugin_path)
Let validation_result be Discovery.validate_plugin_manifest(metadata.manifest)

If not validation_result.is_valid:
    For each error in validation_result.errors:
        Log error message "Validation error: " plus error
    Return false
```

### 2. **Error Recovery**
Handle discovery errors gracefully:

```runa
Try:
    Let plugins be Discovery.scan_plugins(discovery, "/plugins")
Catch Discovery.PluginDiscoveryError as error:
    Log error message "Discovery failed: " plus error.message
    Let plugins be list containing  # Continue with empty list
```

### 3. **Caching Results**
Cache discovery results for better performance:

```runa
Let _plugin_cache be Dictionary[String, PluginMetadata] containing

Process called "cached_scan_plugins" that takes path as String returns List[Plugin]:
    If path in _plugin_cache:
        Return _plugin_cache[path]
    
    Let plugins be Discovery.scan_plugins(discovery, path)
    Set _plugin_cache[path] to plugins
    Return plugins
```

### 4. **Security Validation**
Always verify plugin integrity:

```runa
Let discovery be Discovery.create_plugin_discovery()
Let metadata be Discovery.extract_plugin_metadata(discovery, plugin_path)

Note: Check for security issues
If metadata.capabilities.requires contains "system.admin":
    Log warning message "Plugin requests admin privileges: " plus metadata.name
    If not confirm_admin_access(metadata):
        Return false
```

## Integration Examples

### With Plugin Manager

```runa
Import "stdlib/advanced/plugins/discovery" as Discovery
Import "stdlib/advanced/plugins/management" as Management

Let discovery be Discovery.create_plugin_discovery()
Let manager be Management.create_plugin_manager()

Let plugins be Discovery.scan_plugins(discovery, "/plugins")
For each plugin in plugins:
    If manager.enable_plugin(plugin.plugin_id):
        Log message "Successfully loaded: " plus plugin.name
```

### With Plugin Loader

```runa
Import "stdlib/advanced/plugins/discovery" as Discovery
Import "stdlib/advanced/plugins/loading" as Loading

Let discovery be Discovery.create_plugin_discovery()
Let loader be Loading.create_plugin_loader()

Let metadata be Discovery.extract_plugin_metadata(discovery, "/plugins/example")
If Discovery.check_plugin_compatibility(discovery, metadata):
    Let plugin be Loading.load_plugin(loader, "/plugins/example")
    If Loading.initialize_plugin(loader, plugin):
        Log message "Plugin ready: " plus plugin.name
```

## Comparative Notes

### Advantages over Other Plugin Systems

**vs. Python's pkg_resources:**
- Type-safe metadata extraction
- Built-in compatibility validation
- Automatic error recovery
- AI-friendly discovery patterns

**vs. Node.js npm:**
- Unified manifest format
- Advanced dependency resolution
- Security-first validation
- Performance-optimized scanning

**vs. Java OSGi:**
- Simpler configuration
- Better error diagnostics  
- Hot-reload support
- Modern semantic versioning

The Runa Plugin Discovery module provides a modern, secure, and efficient foundation for building extensible applications with confident plugin management.