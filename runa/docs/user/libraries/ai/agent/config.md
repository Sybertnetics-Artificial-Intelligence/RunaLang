# Agent Configuration Module

The Agent Configuration module provides a secure, centralized configuration management system for the AI agent framework. This production-grade system enables loading configuration from files, environment variables, and remote sources with support for default values, validation, hot-reloading, and hierarchical overrides.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Configuration Structure](#configuration-structure)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Configuration Sources](#configuration-sources)
- [Security & Validation](#security--validation)
- [Hot-Reloading](#hot-reloading)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Configuration management is critical for production AI agent deployments. The Agent Configuration module provides a comprehensive solution that supports multiple configuration sources, environment-specific overrides, schema validation, and secure secret management. All configuration is type-safe and validated against schemas to prevent runtime errors.

### Design Principles

1. **Hierarchical Configuration**: Environment-specific overrides with fallback defaults
2. **Type Safety**: All configuration values are validated and typed
3. **Security First**: Secure handling of sensitive configuration data
4. **Hot-Reload**: Dynamic configuration updates without agent restart
5. **Centralized Access**: Single point of access for all configuration needs

## Key Features

### Configuration Management
- **Hierarchical Loading**: Multiple configuration sources with priority ordering
- **Environment Overrides**: Environment-specific configuration files
- **Default Values**: Comprehensive default configuration for all modules
- **Type Validation**: Schema validation and type checking for all values

### Security Features
- **Secret Management**: Secure handling of passwords, keys, and tokens
- **Encryption Support**: Encrypted configuration files and values
- **Access Control**: Permission-based configuration access
- **Audit Logging**: Track all configuration access and modifications

### Dynamic Features
- **Hot-Reloading**: Update configuration without system restart
- **Runtime Validation**: Continuous validation of configuration changes
- **Dependency Injection**: Automatic configuration injection into modules
- **Change Notifications**: Event-driven configuration change handling

## Configuration Structure

### AgentConfig Type

The main configuration structure containing all agent system settings.

```runa
Type called "AgentConfig":
    log_level as String                           Note: Logging level (debug, info, warn, error)
    persistence as Dictionary[String, String]     Note: File paths for persistence
    security as Dictionary[String, Any]           Note: Security settings
    resources as Dictionary[String, Number]       Note: Resource limits and thresholds
    network as Dictionary[String, Any]            Note: Network configuration
    skills as Dictionary[String, Any]             Note: Skill management settings
    tasks as Dictionary[String, Any]              Note: Task execution configuration
    coordination as Dictionary[String, Any]       Note: Multi-agent coordination
    swarm as Dictionary[String, Any]              Note: Swarm intelligence settings
    hierarchical as Dictionary[String, Any]       Note: Hierarchical management
```

### Default Configuration Values

```runa
Default Configuration Structure:
{
    "log_level": "info",
    "persistence": {
        "agent_registry": "./agent_registry.json",
        "skill_registry": "./skill_registry.json",
        "task_manager": "./task_manager.json"
    },
    "security": {
        "default_permissions": ["basic"],
        "sandbox_level": "medium",
        "audit_enabled": true
    },
    "resources": {
        "default_memory_limit_mb": 128,
        "default_cpu_limit_percent": 50,
        "default_network_limit_mbps": 10,
        "default_disk_limit_mb": 1024,
        "health_check_interval_seconds": 60.0
    },
    "network": {
        "default_timeout_seconds": 30,
        "max_retries": 3,
        "sync_message_polling_interval_seconds": 0.1
    },
    "swarm": {
        "default_bidding_strategy": "weighted_score",
        "leader_weights": {
            "performance": 0.4,
            "trust": 0.3,
            "load": 0.2,
            "capability": 0.1
        }
    }
}
```

## API Reference

### Core Configuration Functions

#### get_config

Retrieves the complete agent configuration with all defaults and overrides applied.

```runa
Process called "get_config" returns AgentConfig
```

**Returns:** Complete agent configuration structure

**Example:**
```runa
Import "ai/agent/config" as Config

Let config be Config.get_config

Display "Configuration loaded:"
Display "  Log level: " + config.log_level
Display "  Default memory limit: " + config.resources["default_memory_limit_mb"] + "MB"
Display "  Security level: " + config.security["sandbox_level"]
Display "  Swarm strategy: " + config.swarm["default_bidding_strategy"]
```

#### get_config_value

Retrieves a specific configuration value using dot notation with default fallback.

```runa
Process called "get_config_value" that takes key as String and default as Any returns Any
```

**Parameters:**
- `key`: Configuration key using dot notation (e.g., "resources.default_memory_limit_mb")
- `default`: Default value to return if key not found

**Returns:** Configuration value or default if not found

**Example:**
```runa
Let memory_limit be Config.get_config_value with 
    key as "resources.default_memory_limit_mb" 
    and default as 256

Let custom_setting be Config.get_config_value with
    key as "custom.experimental_feature"
    and default as false

Display "Memory limit: " + memory_limit + "MB"
Display "Experimental feature: " + custom_setting
```

### Configuration Management

#### load_config_from_file

Loads configuration from a specific file with validation.

```runa
Process called "load_config_from_file" that takes file_path as String returns Boolean
```

**Parameters:**
- `file_path`: Path to configuration file (JSON format)

**Returns:** True if successfully loaded, false if failed

#### save_config_to_file

Saves current configuration to file with backup.

```runa
Process called "save_config_to_file" that takes file_path as String returns Boolean
```

**Parameters:**
- `file_path`: Path where configuration should be saved

**Returns:** True if successfully saved, false if failed

#### merge_configs

Merges two configuration objects with intelligent override handling.

```runa
Process called "merge_configs" that takes base as Dictionary[String, Any] and overrides as Dictionary[String, Any] returns Dictionary[String, Any]
```

**Parameters:**
- `base`: Base configuration (usually defaults)
- `overrides`: Override configuration (environment-specific)

**Returns:** Merged configuration with overrides applied

## Usage Examples

### Basic Configuration Usage

```runa
Import "ai/agent/config" as Config
Import "ai/agent/core" as Agent

Process called "basic_config_usage_example" returns ConfigUsageExample:
    Note: Load default configuration
    Let config be Config.get_config
    
    Display "Agent Framework Configuration:"
    Display "================================"
    
    Note: Display key configuration sections
    Display "Logging:"
    Display "  Level: " + config.log_level
    
    Display "Security:"
    Display "  Default permissions: " + join_strings with strings as config.security["default_permissions"] and separator as ", "
    Display "  Sandbox level: " + config.security["sandbox_level"]
    Display "  Audit enabled: " + config.security["audit_enabled"]
    
    Display "Resources:"
    Display "  Memory limit: " + config.resources["default_memory_limit_mb"] + "MB"
    Display "  CPU limit: " + config.resources["default_cpu_limit_percent"] + "%"
    Display "  Network limit: " + config.resources["default_network_limit_mbps"] + "Mbps"
    Display "  Health check interval: " + config.resources["health_check_interval_seconds"] + "s"
    
    Display "Network:"
    Display "  Default timeout: " + config.network["default_timeout_seconds"] + "s"
    Display "  Max retries: " + config.network["max_retries"]
    Display "  Polling interval: " + config.network["sync_message_polling_interval_seconds"] + "s"
    
    Display "Swarm Intelligence:"
    Display "  Bidding strategy: " + config.swarm["default_bidding_strategy"]
    Display "  Leader weights:"
    For each weight_type and weight_value in config.swarm["leader_weights"]:
        Display "    " + weight_type + ": " + weight_value
    
    Note: Use configuration to create properly configured agent
    Let agent_identity be Agent.create_agent_identity_with_metadata with
        name as "ConfiguredAgent"
        and description as "Agent created with configuration system"
        and metadata as Dictionary with:
            "config_version" as "1.0"
            "environment" as Config.get_config_value with key as "environment" and default as "development"
    
    Note: Apply resource limits from configuration
    Set agent_identity.resource_limits["memory_mb"] to config.resources["default_memory_limit_mb"]
    Set agent_identity.resource_limits["cpu_percent"] to config.resources["default_cpu_limit_percent"]
    Set agent_identity.resource_limits["network_mbps"] to config.resources["default_network_limit_mbps"]
    
    Note: Apply security settings from configuration
    Set agent_identity.permissions to config.security["default_permissions"]
    
    Display "Agent Configuration Applied:"
    Display "  Memory limit: " + agent_identity.resource_limits["memory_mb"] + "MB"
    Display "  CPU limit: " + agent_identity.resource_limits["cpu_percent"] + "%"
    Display "  Permissions: " + join_strings with strings as agent_identity.permissions and separator as ", "
    
    Return ConfigUsageExample with:
        config as config
        agent as agent_identity
        configuration_applied as true
```

### Environment-Specific Configuration

```runa
Process called "environment_config_example" returns EnvironmentConfigExample:
    Note: Create environment-specific configurations
    Let development_config be Dictionary with:
        "log_level" as "debug"
        "security" as Dictionary with:
            "sandbox_level" as "low"
            "audit_enabled" as false
        "resources" as Dictionary with:
            "default_memory_limit_mb" as 256
            "health_check_interval_seconds" as 30.0
        "network" as Dictionary with:
            "default_timeout_seconds" as 60
            "max_retries" as 5
    
    Let production_config be Dictionary with:
        "log_level" as "warn"
        "security" as Dictionary with:
            "sandbox_level" as "high"
            "audit_enabled" as true
            "encryption_enabled" as true
        "resources" as Dictionary with:
            "default_memory_limit_mb" as 512
            "health_check_interval_seconds" as 10.0
        "network" as Dictionary with:
            "default_timeout_seconds" as 15
            "max_retries" as 2
        "monitoring" as Dictionary with:
            "metrics_enabled" as true
            "performance_tracking" as true
    
    Let testing_config be Dictionary with:
        "log_level" as "error"
        "security" as Dictionary with:
            "sandbox_level" as "maximum"
            "audit_enabled" as true
            "strict_validation" as true
        "resources" as Dictionary with:
            "default_memory_limit_mb" as 64
            "health_check_interval_seconds" as 5.0
        "network" as Dictionary with:
            "default_timeout_seconds" as 5
            "max_retries" as 1
    
    Note: Function to apply environment configuration
    Process called "apply_environment_config" that takes environment as String returns ConfigurationResult:
        Let base_config be Config.get_config
        Let environment_overrides be Dictionary with:
        
        Match environment:
            When "development":
                Set environment_overrides to development_config
            When "production":
                Set environment_overrides to production_config
            When "testing":
                Set environment_overrides to testing_config
            Otherwise:
                Display "Unknown environment: " + environment + ", using defaults"
                Set environment_overrides to dictionary containing
        
        Let merged_config be Config.merge_configs with
            base as base_config
            and overrides as environment_overrides
        
        Display "Environment Configuration Applied: " + environment
        Display "  Log level: " + merged_config.log_level
        Display "  Security level: " + merged_config.security["sandbox_level"]
        Display "  Memory limit: " + merged_config.resources["default_memory_limit_mb"] + "MB"
        Display "  Health check interval: " + merged_config.resources["health_check_interval_seconds"] + "s"
        Display "  Network timeout: " + merged_config.network["default_timeout_seconds"] + "s"
        
        Return ConfigurationResult with:
            environment as environment
            config as merged_config
            overrides_applied as length of environment_overrides
    
    Note: Test different environments
    Let dev_result be apply_environment_config with environment as "development"
    Let prod_result be apply_environment_config with environment as "production" 
    Let test_result be apply_environment_config with environment as "testing"
    
    Display "Environment Configuration Comparison:"
    Display "=========================================="
    Display "Development vs Production:"
    Display "  Log level: " + dev_result.config.log_level + " vs " + prod_result.config.log_level
    Display "  Memory: " + dev_result.config.resources["default_memory_limit_mb"] + "MB vs " + prod_result.config.resources["default_memory_limit_mb"] + "MB"
    Display "  Security: " + dev_result.config.security["sandbox_level"] + " vs " + prod_result.config.security["sandbox_level"]
    
    Return EnvironmentConfigExample with:
        development as dev_result
        production as prod_result
        testing as test_result
```

### Dynamic Configuration Updates

```runa
Process called "dynamic_config_example" returns DynamicConfigExample:
    Note: Initial configuration
    Let initial_config be Config.get_config
    Display "Initial Configuration:"
    Display "  Memory limit: " + initial_config.resources["default_memory_limit_mb"] + "MB"
    Display "  Timeout: " + initial_config.network["default_timeout_seconds"] + "s"
    
    Note: Create dynamic configuration updates
    Let runtime_updates be Dictionary with:
        "resources" as Dictionary with:
            "default_memory_limit_mb" as 1024  Note: Increase memory limit
            "health_check_interval_seconds" as 5.0  Note: More frequent health checks
        "network" as Dictionary with:
            "default_timeout_seconds" as 45  Note: Increase timeout
            "connection_pool_size" as 20  Note: Add new setting
        "performance" as Dictionary with:
            "optimization_enabled" as true  Note: New performance section
            "jit_compilation" as true
            "cache_size_mb" as 64
    
    Note: Apply updates using merge functionality
    Let updated_config be Config.merge_configs with
        base as initial_config
        and overrides as runtime_updates
    
    Display "Updated Configuration:"
    Display "  Memory limit: " + updated_config.resources["default_memory_limit_mb"] + "MB (was " + initial_config.resources["default_memory_limit_mb"] + "MB)"
    Display "  Timeout: " + updated_config.network["default_timeout_seconds"] + "s (was " + initial_config.network["default_timeout_seconds"] + "s)"
    Display "  New settings added: " + (updated_config.network contains "connection_pool_size")
    
    Note: Validate configuration changes
    Process called "validate_config_changes" that takes old_config as AgentConfig and new_config as AgentConfig returns ValidationResult:
        Let validation_result be ValidationResult with:
            valid as true
            warnings as list containing
            errors as list containing
            changes as list containing
        
        Note: Check for significant resource changes
        If new_config.resources["default_memory_limit_mb"] > old_config.resources["default_memory_limit_mb"] * 2:
            Add "Memory limit increased by more than 100%" to validation_result.warnings
        
        If new_config.network["default_timeout_seconds"] < 10:
            Add "Network timeout is very low - may cause failures" to validation_result.errors
            Set validation_result.valid to false
        
        Note: Track all changes
        If new_config.resources["default_memory_limit_mb"] is not equal to old_config.resources["default_memory_limit_mb"]:
            Add "Memory limit: " + old_config.resources["default_memory_limit_mb"] + " -> " + new_config.resources["default_memory_limit_mb"] to validation_result.changes
        
        If new_config.network["default_timeout_seconds"] is not equal to old_config.network["default_timeout_seconds"]:
            Add "Network timeout: " + old_config.network["default_timeout_seconds"] + " -> " + new_config.network["default_timeout_seconds"] to validation_result.changes
        
        Return validation_result
    
    Let validation_result be validate_config_changes with
        old_config as initial_config
        and new_config as updated_config
    
    Display "Configuration Validation Results:"
    Display "  Valid: " + validation_result.valid
    Display "  Changes: " + length of validation_result.changes
    For each change in validation_result.changes:
        Display "    " + change
    
    Display "  Warnings: " + length of validation_result.warnings
    For each warning in validation_result.warnings:
        Display "    WARNING: " + warning
    
    Display "  Errors: " + length of validation_result.errors
    For each error in validation_result.errors:
        Display "    ERROR: " + error
    
    Return DynamicConfigExample with:
        initial_config as initial_config
        updated_config as updated_config
        validation_result as validation_result
        update_successful as validation_result.valid
```

### Configuration-Driven Agent Creation

```runa
Process called "config_driven_agent_example" returns ConfigDrivenExample:
    Note: Create specialized configurations for different agent types
    Let data_processor_config be Dictionary with:
        "agent_type" as "data_processor"
        "resources" as Dictionary with:
            "memory_mb" as 512
            "cpu_percent" as 60
            "disk_mb" as 2048
        "capabilities" as list containing "data_analysis", "statistical_modeling", "report_generation"
        "security" as Dictionary with:
            "sandbox_level" as "medium"
            "permissions" as list containing "data_read", "data_write", "compute"
        "performance" as Dictionary with:
            "optimization_level" as "high"
            "parallel_processing" as true
            "cache_enabled" as true
    
    Let web_service_config be Dictionary with:
        "agent_type" as "web_service"
        "resources" as Dictionary with:
            "memory_mb" as 256
            "cpu_percent" as 30
            "network_mbps" as 50
        "capabilities" as list containing "http_handling", "json_processing", "rate_limiting"
        "security" as Dictionary with:
            "sandbox_level" as "high"
            "permissions" as list containing "network_access", "basic"
        "network" as Dictionary with:
            "max_connections" as 100
            "timeout_seconds" as 15
            "keep_alive" as true
    
    Let monitoring_config be Dictionary with:
        "agent_type" as "monitoring"
        "resources" as Dictionary with:
            "memory_mb" as 128
            "cpu_percent" as 10
            "network_mbps" as 5
        "capabilities" as list containing "health_monitoring", "metrics_collection", "alerting"
        "security" as Dictionary with:
            "sandbox_level" as "low"
            "permissions" as list containing "system_read", "basic"
        "monitoring" as Dictionary with:
            "collection_interval" as 5.0
            "retention_days" as 30
            "alert_thresholds" as Dictionary with:
                "cpu_percent" as 80
                "memory_percent" as 85
                "error_rate" as 0.05
    
    Note: Function to create agent from configuration
    Process called "create_agent_from_config" that takes agent_config as Dictionary[String, Any] returns ConfiguredAgent:
        Let base_config be Config.get_config
        Let merged_config be Config.merge_configs with
            base as base_config
            and overrides as agent_config
        
        Let agent_identity be Agent.create_agent_identity_with_metadata with
            name as agent_config["agent_type"] + "_agent"
            and description as "Agent configured for " + agent_config["agent_type"] + " workload"
            and metadata as agent_config
        
        Note: Apply configuration to agent identity
        If agent_config contains "resources":
            Set agent_identity.resource_limits["memory_mb"] to agent_config["resources"]["memory_mb"]
            If agent_config["resources"] contains "cpu_percent":
                Set agent_identity.resource_limits["cpu_percent"] to agent_config["resources"]["cpu_percent"]
            If agent_config["resources"] contains "network_mbps":
                Set agent_identity.resource_limits["network_mbps"] to agent_config["resources"]["network_mbps"]
        
        If agent_config contains "capabilities":
            Set agent_identity.capabilities to agent_config["capabilities"]
        
        If agent_config contains "security" and agent_config["security"] contains "permissions":
            Set agent_identity.permissions to agent_config["security"]["permissions"]
        
        Return ConfiguredAgent with:
            identity as agent_identity
            configuration as merged_config
            agent_type as agent_config["agent_type"]
    
    Note: Create different types of agents
    Let data_agent be create_agent_from_config with agent_config as data_processor_config
    Let web_agent be create_agent_from_config with agent_config as web_service_config  
    Let monitor_agent be create_agent_from_config with agent_config as monitoring_config
    
    Display "Configuration-Driven Agent Creation Results:"
    Display "================================================"
    
    Display "Data Processor Agent:"
    Display "  ID: " + data_agent.identity.id
    Display "  Memory: " + data_agent.identity.resource_limits["memory_mb"] + "MB"
    Display "  CPU: " + data_agent.identity.resource_limits["cpu_percent"] + "%"
    Display "  Capabilities: " + length of data_agent.identity.capabilities
    Display "  Permissions: " + join_strings with strings as data_agent.identity.permissions and separator as ", "
    
    Display "Web Service Agent:"
    Display "  ID: " + web_agent.identity.id
    Display "  Memory: " + web_agent.identity.resource_limits["memory_mb"] + "MB"
    Display "  Network: " + web_agent.identity.resource_limits["network_mbps"] + "Mbps"
    Display "  Capabilities: " + length of web_agent.identity.capabilities
    
    Display "Monitoring Agent:"  
    Display "  ID: " + monitor_agent.identity.id
    Display "  Memory: " + monitor_agent.identity.resource_limits["memory_mb"] + "MB"
    Display "  CPU: " + monitor_agent.identity.resource_limits["cpu_percent"] + "%"
    Display "  Capabilities: " + length of monitor_agent.identity.capabilities
    
    Return ConfigDrivenExample with:
        data_agent as data_agent
        web_agent as web_agent
        monitor_agent as monitor_agent
        agents_created as 3
```

## Configuration Sources

### File-Based Configuration

The system supports multiple configuration file formats and locations:

```runa
Configuration File Locations (in priority order):
1. ./agent_config.json (current directory)
2. ~/.runa/agent_config.json (user home)
3. /etc/runa/agent_config.json (system-wide)
4. Environment variable: RUNA_AGENT_CONFIG
```

**Example Configuration File:**
```json
{
    "log_level": "info",
    "environment": "production",
    "persistence": {
        "agent_registry": "/var/lib/runa/agent_registry.json",
        "skill_registry": "/var/lib/runa/skill_registry.json",
        "task_manager": "/var/lib/runa/task_manager.json"
    },
    "security": {
        "default_permissions": ["basic", "compute"],
        "sandbox_level": "high",
        "audit_enabled": true,
        "encryption_enabled": true
    },
    "resources": {
        "default_memory_limit_mb": 1024,
        "default_cpu_limit_percent": 75,
        "default_network_limit_mbps": 100,
        "health_check_interval_seconds": 30.0
    },
    "swarm": {
        "default_bidding_strategy": "capability_based",
        "leader_weights": {
            "performance": 0.5,
            "trust": 0.25,
            "load": 0.15,
            "capability": 0.1
        }
    }
}
```

### Environment Variables

```runa
Environment Variable Support:
- RUNA_LOG_LEVEL: Override log level
- RUNA_MEMORY_LIMIT: Override default memory limit
- RUNA_SECURITY_LEVEL: Override sandbox level
- RUNA_CONFIG_FILE: Specify config file location
- RUNA_ENVIRONMENT: Set environment (dev/prod/test)
```

### Remote Configuration

```runa
Process called "remote_config_example" returns RemoteConfigExample:
    Note: Load configuration from remote source
    Process called "load_remote_config" that takes config_url as String returns Dictionary[String, Any]:
        Let http_client be create_http_client
        Let response be http_client.get with url as config_url
        
        If response.status is equal to 200:
            Let remote_config be json_deserialize with json as response.body
            
            Note: Validate remote configuration
            Let validation_result be validate_configuration with config as remote_config
            
            If validation_result.valid:
                Display "Remote configuration loaded successfully"
                Return remote_config
            Otherwise:
                Display "Remote configuration validation failed"
                For each error in validation_result.errors:
                    Display "  ERROR: " + error
                Return dictionary containing
        
        Display "Failed to load remote configuration: HTTP " + response.status
        Return dictionary containing
    
    Let remote_config be load_remote_config with config_url as "https://config.example.com/agent-config.json"
    
    If length of remote_config is greater than 0:
        Let base_config be Config.get_config
        Let final_config be Config.merge_configs with
            base as base_config
            and overrides as remote_config
        
        Display "Remote configuration merged successfully"
    
    Return RemoteConfigExample with:
        remote_config as remote_config
        merge_successful as length of remote_config is greater than 0
```

## Security & Validation

### Configuration Validation

```runa
Process called "validate_configuration" that takes config as Dictionary[String, Any] returns ConfigValidationResult:
    Let validation_result be ConfigValidationResult with:
        valid as true
        errors as list containing
        warnings as list containing
        security_issues as list containing
    
    Note: Validate security settings
    If config contains "security":
        Let security_config be config["security"]
        
        If security_config contains "sandbox_level":
            Let valid_levels be list containing "low", "medium", "high", "maximum"
            If not valid_levels contains security_config["sandbox_level"]:
                Add "Invalid sandbox level: " + security_config["sandbox_level"] to validation_result.errors
                Set validation_result.valid to false
        
        If security_config contains "default_permissions":
            Let permissions be security_config["default_permissions"]
            Let valid_permissions be list containing "basic", "compute", "data_read", "data_write", "network_access", "admin"
            
            For each permission in permissions:
                If not valid_permissions contains permission:
                    Add "Invalid permission: " + permission to validation_result.errors
                    Set validation_result.valid to false
    
    Note: Validate resource settings
    If config contains "resources":
        Let resource_config be config["resources"]
        
        If resource_config contains "default_memory_limit_mb":
            Let memory_limit be resource_config["default_memory_limit_mb"]
            If memory_limit < 64:
                Add "Memory limit too low (minimum 64MB): " + memory_limit to validation_result.errors
                Set validation_result.valid to false
            Otherwise if memory_limit > 8192:
                Add "Memory limit very high: " + memory_limit + "MB" to validation_result.warnings
        
        If resource_config contains "default_cpu_limit_percent":
            Let cpu_limit be resource_config["default_cpu_limit_percent"]
            If cpu_limit < 1 or cpu_limit > 100:
                Add "CPU limit out of range (1-100): " + cpu_limit to validation_result.errors
                Set validation_result.valid to false
    
    Note: Security validations
    If config contains "security" and config["security"] contains "audit_enabled":
        If not config["security"]["audit_enabled"]:
            Add "Audit logging is disabled - may not meet compliance requirements" to validation_result.security_issues
    
    Return validation_result
```

### Secure Configuration Storage

```runa
Process called "secure_config_example" returns SecureConfigExample:
    Note: Create secure configuration with encryption
    Let sensitive_config be Dictionary with:
        "database" as Dictionary with:
            "password" as "encrypted:AES256:base64encodedencryptedpassword"
            "host" as "db.internal.company.com"
            "username" as "agent_service"
        "api_keys" as Dictionary with:
            "external_service" as "encrypted:AES256:base64encodedapikey"
            "monitoring_service" as "encrypted:AES256:base64encodedmonitoringkey"
        "certificates" as Dictionary with:
            "ssl_cert" as "encrypted:AES256:base64encodedcertificate"
            "ssl_key" as "encrypted:AES256:base64encodedprivatekey"
    
    Note: Function to decrypt configuration values
    Process called "decrypt_config_value" that takes encrypted_value as String returns String:
        If encrypted_value starts with "encrypted:":
            Let parts be split_string with text as encrypted_value and delimiter as ":"
            If length of parts is equal to 3:
                Let algorithm be parts[1]
                Let encrypted_data be parts[2]
                
                Match algorithm:
                    When "AES256":
                        Return decrypt_aes256 with data as encrypted_data and key as get_encryption_key
                    Otherwise:
                        Display "Unknown encryption algorithm: " + algorithm
                        Return ""
            
            Display "Invalid encrypted value format"
            Return ""
        
        Note: Return as-is if not encrypted
        Return encrypted_value
    
    Note: Process secure configuration
    Process called "process_secure_config" that takes config as Dictionary[String, Any] returns Dictionary[String, Any]:
        Let processed_config be config
        
        Note: Recursively decrypt encrypted values
        For each key and value in config:
            If type_of with value as value is equal to "String" and value starts with "encrypted:":
                Set processed_config[key] to decrypt_config_value with encrypted_value as value
            Otherwise if type_of with value as value is equal to "Dictionary":
                Set processed_config[key] to process_secure_config with config as value
        
        Return processed_config
    
    Let decrypted_config be process_secure_config with config as sensitive_config
    
    Display "Secure Configuration Processing:"
    Display "  Encrypted entries found: " + count_encrypted_values with config as sensitive_config
    Display "  Decryption successful: " + (length of decrypted_config is greater than 0)
    Display "  Database config processed: " + (decrypted_config contains "database")
    Display "  API keys processed: " + (decrypted_config contains "api_keys")
    
    Return SecureConfigExample with:
        original_config as sensitive_config
        decrypted_config as decrypted_config
        processing_successful as length of decrypted_config is greater than 0
```

## Hot-Reloading

### Configuration Change Detection

```runa
Process called "hot_reload_example" returns HotReloadExample:
    Note: Set up configuration monitoring
    Let config_monitor be create_config_monitor with
        config_file as "./agent_config.json"
        and check_interval as 5.0  Note: Check every 5 seconds
    
    Note: Register change handlers
    config_monitor.on_change as function(old_config, new_config):
        Display "Configuration change detected!"
        
        Let changes be detect_config_changes with
            old_config as old_config
            and new_config as new_config
        
        For each change in changes:
            Display "  " + change.path + ": " + change.old_value + " -> " + change.new_value
            
            Note: Handle specific types of changes
            Match change.category:
                When "security":
                    Display "    Security change detected - triggering security validation"
                    validate_security_config with config as new_config
                When "resources":
                    Display "    Resource change detected - updating agent limits"
                    update_agent_resource_limits with new_limits as change.new_value
                When "network":
                    Display "    Network change detected - updating connection settings"
                    update_network_settings with new_settings as change.new_value
        
        Note: Apply configuration updates
        apply_config_updates with new_config as new_config
        
        Display "Configuration hot-reload completed successfully"
    
    Note: Start monitoring
    config_monitor.start_monitoring
    
    Note: Simulate configuration changes
    Process called "simulate_config_changes" returns None:
        wait_seconds with duration as 2
        
        Note: Update memory limit
        Let updated_config be Config.get_config
        Set updated_config.resources["default_memory_limit_mb"] to 512
        save_config_to_file with config as updated_config and file_path as "./agent_config.json"
        Display "Simulated memory limit change to 512MB"
        
        wait_seconds with duration as 8
        
        Note: Update security level
        Set updated_config.security["sandbox_level"] to "high"
        save_config_to_file with config as updated_config and file_path as "./agent_config.json"
        Display "Simulated security level change to high"
        
        wait_seconds with duration as 8
        
        Note: Add new network setting
        Set updated_config.network["connection_timeout"] to 20
        save_config_to_file with config as updated_config and file_path as "./agent_config.json"
        Display "Simulated new network setting addition"
    
    simulate_config_changes
    
    Note: Monitor for 30 seconds
    wait_seconds with duration as 30
    
    config_monitor.stop_monitoring
    
    Return HotReloadExample with:
        monitor as config_monitor
        monitoring_duration as 30
        changes_detected as config_monitor.change_count
```

### Configuration Rollback

```runa
Process called "config_rollback_example" returns RollbackExample:
    Note: Create configuration backup system
    Let config_backup be create_config_backup_system with
        max_backups as 10
        and backup_interval as 60.0  Note: Backup every minute
    
    Note: Save initial configuration
    Let initial_config be Config.get_config
    config_backup.save_backup with
        config as initial_config
        and label as "initial_configuration"
    
    Note: Make problematic configuration changes
    Let problematic_config be Config.get_config
    Set problematic_config.resources["default_memory_limit_mb"] to 32  Note: Too low
    Set problematic_config.network["default_timeout_seconds"] to 1  Note: Too short
    Set problematic_config.security["sandbox_level"] to "invalid"  Note: Invalid value
    
    Note: Attempt to apply problematic configuration
    Let validation_result be validate_configuration with config as problematic_config
    
    If not validation_result.valid:
        Display "Configuration validation failed!"
        For each error in validation_result.errors:
            Display "  ERROR: " + error
        
        Display "Rolling back to previous configuration..."
        
        Note: Perform rollback
        Let rollback_result be config_backup.rollback_to_previous
        
        If rollback_result.success:
            Display "Rollback successful!"
            Display "  Restored to backup: " + rollback_result.backup_label
            Display "  Backup timestamp: " + rollback_result.backup_timestamp
            
            Let restored_config be Config.get_config
            Display "  Memory limit restored: " + restored_config.resources["default_memory_limit_mb"] + "MB"
            Display "  Security level restored: " + restored_config.security["sandbox_level"]
        Otherwise:
            Display "Rollback failed: " + rollback_result.error
    
    Note: List available backups
    Let available_backups be config_backup.list_backups
    
    Display "Configuration Backup History:"
    For each backup in available_backups:
        Display "  " + backup.label + " (" + backup.timestamp + ")"
        Display "    Valid: " + backup.validation_status
        Display "    Size: " + backup.size_bytes + " bytes"
    
    Return RollbackExample with:
        backup_system as config_backup
        initial_config as initial_config
        problematic_config as problematic_config
        rollback_successful as rollback_result.success
        available_backups as available_backups
```

## Best Practices

### Configuration Organization

1. **Hierarchical Structure**
```runa
Note: Organize configuration logically
Good Configuration Structure:
{
    "agent": {
        "identity": {
            "default_permissions": ["basic"],
            "signature_validation": true
        },
        "lifecycle": {
            "default_timeout": 300,
            "health_check_interval": 60
        }
    },
    "execution": {
        "skills": {
            "default_version": "1.0.0",
            "sandbox_level": "medium"
        },
        "tasks": {
            "max_concurrent": 5,
            "default_priority": 5
        }
    }
}
```

2. **Environment-Specific Values**
```runa
Note: Use environment-specific configurations
Process called "environment_aware_config" returns None:
    Let environment be Config.get_config_value with key as "environment" and default as "development"
    
    Match environment:
        When "development":
            apply_development_settings
        When "staging":
            apply_staging_settings
        When "production":
            apply_production_settings
            enable_enhanced_monitoring
            enable_audit_logging
```

3. **Secure Defaults**
```runa
Note: Always use secure defaults
Secure Configuration Defaults:
- sandbox_level: "high" (not "low")
- audit_enabled: true (not false)
- encryption_enabled: true (not false)  
- default_permissions: ["basic"] (not ["admin"])
```

### Performance Considerations

1. **Configuration Caching**
```runa
Process called "cached_config_access" returns None:
    Note: Cache frequently accessed configuration
    Let config_cache be create_config_cache with ttl as 300  Note: 5 minute TTL
    
    Process called "get_cached_config_value" that takes key as String returns Any:
        Let cached_value be config_cache.get with key as key
        If cached_value is not equal to "":
            Return cached_value
        
        Let fresh_value be Config.get_config_value with key as key and default as ""
        config_cache.set with key as key and value as fresh_value and ttl as 300
        Return fresh_value
```

2. **Lazy Loading**
```runa
Process called "lazy_config_loading" returns None:
    Note: Load configuration sections only when needed
    Let config_loader be create_lazy_config_loader
    
    Process called "get_section_when_needed" that takes section as String returns Any:
        If not config_loader.is_loaded with section as section:
            config_loader.load_section with section as section
        
        Return config_loader.get_section with section as section
```

### Validation & Testing

1. **Schema Validation**
```runa
Process called "schema_validation_example" returns None:
    Let config_schema be create_config_schema with:
        "log_level" as StringField with values as list containing "debug", "info", "warn", "error"
        and "resources" as ObjectField with:
            "default_memory_limit_mb" as IntegerField with min as 64 and max as 16384
            and "default_cpu_limit_percent" as IntegerField with min as 1 and max as 100
        and "security" as ObjectField with:
            "sandbox_level" as StringField with values as list containing "low", "medium", "high", "maximum"
            and "audit_enabled" as BooleanField
    
    Let config_to_validate be Config.get_config
    Let validation_result be config_schema.validate with config as config_to_validate
    
    If not validation_result.valid:
        Display "Configuration schema validation failed:"
        For each error in validation_result.errors:
            Display "  " + error.field + ": " + error.message
```

2. **Configuration Testing**
```runa
Process called "test_configuration" returns ConfigTestResult:
    Let test_configs be list containing
    
    Note: Test development configuration
    Let dev_config be load_test_config with environment as "development"
    Add create_config_test with config as dev_config and name as "development" to test_configs
    
    Note: Test production configuration
    Let prod_config be load_test_config with environment as "production"
    Add create_config_test with config as prod_config and name as "production" to test_configs
    
    Let all_tests_passed be true
    For each test in test_configs:
        Let test_result be run_config_test with test as test
        If not test_result.passed:
            Set all_tests_passed to false
            Display "Configuration test failed: " + test.name
            For each failure in test_result.failures:
                Display "  FAIL: " + failure
    
    Return ConfigTestResult with:
        all_passed as all_tests_passed
        test_count as length of test_configs
```

## Troubleshooting

### Common Configuration Issues

#### Issue: Configuration File Not Found

**Problem**: Agent fails to start with "Configuration file not found" error

**Solution**:
```runa
Process called "diagnose_config_file_issue" returns ConfigDiagnostic:
    Let diagnostic be ConfigDiagnostic with:
        file_exists as false
        file_readable as false
        file_valid as false
        recommendations as list containing
    
    Note: Check if file exists
    Let config_file_path be "./agent_config.json"
    Set diagnostic.file_exists to file_exists with path as config_file_path
    
    If not diagnostic.file_exists:
        Add "Create configuration file at: " + config_file_path to diagnostic.recommendations
        Add "Run: runa agent init-config to create default configuration" to diagnostic.recommendations
        Return diagnostic
    
    Note: Check if file is readable
    Try:
        Let file_content be read_file_sync with path as config_file_path
        Set diagnostic.file_readable to true
        
        Note: Check if file is valid JSON
        Try:
            Let parsed_config be json_deserialize with json as file_content
            Set diagnostic.file_valid to true
        Catch parse_error:
            Add "Fix JSON syntax errors in configuration file" to diagnostic.recommendations
            Add "Validation error: " + parse_error to diagnostic.recommendations
    Catch read_error:
        Add "Fix file permissions for configuration file" to diagnostic.recommendations
        Add "Error: " + read_error to diagnostic.recommendations
    
    Return diagnostic
```

#### Issue: Invalid Configuration Values

**Problem**: Configuration validation errors prevent agent startup

**Solution**:
```runa
Process called "fix_config_validation_errors" that takes config as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let fixed_config be config
    Let validation_result be validate_configuration with config as config
    
    If not validation_result.valid:
        Display "Fixing configuration validation errors..."
        
        For each error in validation_result.errors:
            Match error.field:
                When "security.sandbox_level":
                    Display "  Fixing invalid sandbox level"
                    Set fixed_config.security["sandbox_level"] to "medium"
                When "resources.default_memory_limit_mb":
                    Display "  Fixing invalid memory limit"
                    Set fixed_config.resources["default_memory_limit_mb"] to 256
                When "resources.default_cpu_limit_percent":
                    Display "  Fixing invalid CPU limit"
                    Set fixed_config.resources["default_cpu_limit_percent"] to 50
                Otherwise:
                    Display "  Unknown validation error: " + error.field
        
        Note: Re-validate fixed configuration
        Let revalidation_result be validate_configuration with config as fixed_config
        If revalidation_result.valid:
            Display "Configuration validation errors fixed successfully"
        Otherwise:
            Display "Some validation errors could not be automatically fixed"
    
    Return fixed_config
```

#### Issue: Configuration Hot-Reload Failures

**Problem**: Configuration changes not being applied during hot-reload

**Solution**:
```runa
Process called "diagnose_hot_reload_issues" returns HotReloadDiagnostic:
    Let diagnostic be HotReloadDiagnostic with:
        file_monitoring_active as false
        file_permissions_ok as false
        config_syntax_valid as false
        reload_handlers_registered as false
        recommendations as list containing
    
    Note: Check file monitoring
    Set diagnostic.file_monitoring_active to is_file_monitor_active
    If not diagnostic.file_monitoring_active:
        Add "Enable file monitoring for configuration hot-reload" to diagnostic.recommendations
    
    Note: Check file permissions
    Set diagnostic.file_permissions_ok to can_read_config_file
    If not diagnostic.file_permissions_ok:
        Add "Fix file permissions for configuration file" to diagnostic.recommendations
    
    Note: Check configuration syntax
    Try:
        Let current_config be load_config_from_file with file_path as "./agent_config.json"
        Set diagnostic.config_syntax_valid to true
    Catch error:
        Add "Fix configuration file syntax: " + error to diagnostic.recommendations
    
    Note: Check reload handlers
    Set diagnostic.reload_handlers_registered to are_reload_handlers_registered
    If not diagnostic.reload_handlers_registered:
        Add "Register configuration reload event handlers" to diagnostic.recommendations
    
    Return diagnostic
```

The Agent Configuration module provides a robust foundation for managing complex agent system configurations across different environments, ensuring security, performance, and reliability while maintaining flexibility and ease of use.