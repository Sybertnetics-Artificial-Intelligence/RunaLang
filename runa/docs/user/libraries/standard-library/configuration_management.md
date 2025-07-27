# Runa Configuration Management Ecosystem

## Overview

The Runa Configuration Management Ecosystem is a comprehensive, enterprise-grade solution for managing application configuration, secrets, environment variables, and configuration files. It provides a unified, secure, and scalable approach to configuration management that meets the demands of modern production environments.

## Key Features

### 🚀 **Core Configuration Management**
- **Unified Configuration Interface**: Single API for all configuration needs
- **Multi-Source Loading**: Environment variables, files, secrets, and runtime values
- **Hierarchical Merging**: Priority-based configuration source management
- **Type-Safe Access**: Automatic type conversion and validation
- **Schema-Based Validation**: Enforce configuration structure and constraints

### 🔒 **Enterprise Security**
- **Zero-Knowledge Encryption**: AES-256-GCM encryption for sensitive data
- **Fine-Grained Access Control**: Role-based permissions and temporary access
- **Comprehensive Audit Logging**: Full audit trail for compliance (SOC 2, FIPS 140-2)
- **Secret Lifecycle Management**: Automatic rotation, expiration, and versioning
- **Sensitive Value Detection**: Automatic identification and masking of secrets

### ⚡ **Advanced Features**
- **Configuration Interpolation**: Variable substitution with `${variable}` syntax
- **Dynamic Reloading**: Hot-swap configuration without restarts
- **Performance Optimization**: Intelligent caching and lazy loading
- **Multi-Environment Support**: Development, staging, production profiles
- **AI-Friendly Design**: Optimized for LLM-based agent systems

### 📊 **Production-Ready**
- **Thread-Safe Operations**: Designed for high-concurrency environments
- **Performance Monitoring**: Built-in metrics and performance tracking
- **Error Recovery**: Graceful error handling and fallback mechanisms
- **Compliance Support**: SOC 2, FIPS 140-2, Common Criteria compliance
- **Cloud Integration**: Support for AWS KMS, Azure Key Vault, Google Cloud KMS

## Quick Start Guide

### Basic Configuration Setup

```runa
Import "stdlib/config/config" as config

Note: Create a basic configuration
Let options be config.ConfigurationOptions with:
    profile as config.DEVELOPMENT
    enable_interpolation as true
    enable_validation as true
    enable_audit_logging as true

Let configuration be config.create_configuration with options as options

Note: Set configuration values
config.set_configuration_value with:
    configuration as configuration
    key as "app.name"
    value as "MyApplication"
    source as "default"

config.set_configuration_value with:
    configuration as configuration
    key as "app.port"
    value as "8080"
    source as "default"

Note: Get configuration values with type conversion
Let port_result be config.get_configuration_value with:
    configuration as configuration
    key as "app.port"
    default_value as 3000
    data_type as "integer"

Match port_result:
    When config.ConfigurationSuccess:
        Display "Application port: " plus port_result.value as String
    Otherwise:
        Display "Failed to get port configuration"
```

### Working with Secrets

```runa
Import "stdlib/config/secrets" as secrets

Note: Create a secret
Let secret_result be secrets.create_secret with:
    name as "database_password"
    value as "super_secure_password_123"
    secret_type as secrets.DATABASE_CREDENTIAL
    metadata as dictionary containing:
        "description" as "Production database password"
        "rotation_interval" as 2592000.0  Note: 30 days

Match secret_result:
    When secrets.SecretSuccess:
        Let secret_id be secret_result.value
        Display "Secret created with ID: " plus secret_id
        
        Note: Retrieve the secret
        Let retrieve_result be secrets.get_secret with:
            secret_id as secret_id
        
        Match retrieve_result:
            When secrets.SecretSuccess:
                Display "Retrieved secret value: " plus retrieve_result.value
            Otherwise:
                Display "Failed to retrieve secret"
    Otherwise:
        Display "Failed to create secret"
```

### Configuration with Interpolation

```runa
Note: Set up base configuration values
config.set_configuration_value with:
    configuration as configuration
    key as "database.host"
    value as "localhost"

config.set_configuration_value with:
    configuration as configuration
    key as "database.port"
    value as "5432"

config.set_configuration_value with:
    configuration as configuration
    key as "database.name"
    value as "myapp_db"

Note: Use interpolation for connection string
config.set_configuration_value with:
    configuration as configuration
    key as "database.connection_string"
    value as "postgresql://user@${database.host}:${database.port}/${database.name}"

Note: Retrieve interpolated value
Let connection_result be config.get_configuration_value with:
    configuration as configuration
    key as "database.connection_string"

Match connection_result:
    When config.ConfigurationSuccess:
        Note: Result will be: "postgresql://user@localhost:5432/myapp_db"
        Display "Connection string: " plus connection_result.value
```

## Architecture Overview

### Hub-and-Spoke Design

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Environment    │    │                  │    │   Config Files  │
│   Variables     │───▶│   Configuration  │◀───│   (JSON, YAML,  │
│                 │    │    Management    │    │    TOML, etc.)  │
└─────────────────┘    │      Core        │    └─────────────────┘
                       │                  │
┌─────────────────┐    │                  │    ┌─────────────────┐
│    Secrets      │───▶│                  │◀───│   Runtime       │
│  Management     │    │                  │    │   Overrides     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Application    │
                       │   Configuration  │
                       │                  │
                       └──────────────────┘
```

### Module Structure

```
stdlib/config/
├── config.runa          # Core configuration management
├── secrets.runa         # Secrets management and encryption
├── environment.runa     # Environment variable handling
└── loader.runa         # Configuration file loading
```

## Configuration Sources and Priority

Configuration values are loaded from multiple sources with a clear priority hierarchy:

1. **Runtime Overrides** (Priority: 999) - Values set programmatically
2. **Environment Variables** (Priority: 100) - OS environment variables with prefix filtering
3. **Local Configuration Files** (Priority: 50-80) - Application-specific config files
4. **User Configuration** (Priority: 30-40) - User-specific settings
5. **System Configuration** (Priority: 10-20) - System-wide defaults
6. **Schema Defaults** (Priority: 0) - Default values from configuration schema

### Example Priority Resolution

```runa
Note: Environment variable: MYAPP_DATABASE_HOST=prod-db.example.com
Note: Config file: database.host=localhost
Note: Runtime override: database.host=test-db.internal

Note: Result: test-db.internal (runtime override wins)
```

## Configuration Schema and Validation

Define and enforce configuration structure with comprehensive validation:

```runa
Let schema be config.ConfigurationSchema with:
    schema_version as "1.0"
    schema_id as "my_app_schema"
    required_keys as list containing:
        "app.name"
        "app.port"
        "database.host"
        "database.port"
    optional_keys as list containing:
        "app.debug"
        "app.max_connections"
        "cache.enabled"
    key_types as dictionary containing:
        "app.port" as "integer"
        "database.port" as "integer"
        "app.debug" as "boolean"
        "app.max_connections" as "integer"
        "cache.enabled" as "boolean"
    key_constraints as dictionary containing:
        "app.port" as dictionary containing:
            "min" as 1024
            "max" as 65535
        "app.max_connections" as dictionary containing:
            "min" as 1
            "max" as 10000
    default_values as dictionary containing:
        "app.debug" as false
        "app.max_connections" as 100
        "cache.enabled" as true
    sensitive_keys as list containing:
        "database.password_secret_id"
        "api.secret_key"

Note: Apply schema to configuration
Set configuration.schema to schema

Note: Validate configuration
Let validation_result be config.validate_configuration with:
    configuration as configuration
    schema as schema

If validation_result.valid:
    Display "Configuration is valid"
Else:
    Display "Validation errors: " plus validation_result.errors as String
```

## Secrets Management

### Secret Types and Lifecycle

The secrets management system supports various secret types with full lifecycle management:

```runa
Note: Available secret types
secrets.API_KEY              Note: API keys and tokens
secrets.PASSWORD             Note: User and service passwords  
secrets.DATABASE_CREDENTIAL  Note: Database connection credentials
secrets.PRIVATE_KEY          Note: Private keys and certificates
secrets.ENCRYPTION_KEY       Note: Encryption and signing keys
secrets.OAUTH_SECRET         Note: OAuth client secrets
secrets.WEBHOOK_SECRET       Note: Webhook signing secrets
secrets.CUSTOM               Note: Custom secret types
```

### Secret Rotation

Implement automatic secret rotation for enhanced security:

```runa
Note: Create secret with rotation policy
Let secret_result be secrets.create_secret with:
    name as "rotating_api_key"
    value as "initial_api_key_value"
    secret_type as secrets.API_KEY
    metadata as dictionary containing:
        "rotation_interval" as 86400.0  Note: Rotate every 24 hours
        "auto_rotate" as true

Note: Manual rotation
Let rotation_result be secrets.rotate_secret with:
    secret_id as secret_id
    new_value as "new_rotated_api_key_value"
    rotation_config as dictionary containing:
        "notify_on_rotation" as true

Note: Automatic rotation (generates new value)
Let auto_rotation_result be secrets.rotate_secret with:
    secret_id as secret_id
    new_value as None  Note: Auto-generate
    rotation_config as dictionary containing:
        "auto_generate" as true
```

### Access Control and Permissions

Implement fine-grained access control for secrets:

```runa
Note: Grant access to a secret
Let access_result be secrets.grant_secret_access with:
    secret_id as secret_id
    principal as "service_account_xyz"
    permissions as list containing "read", "metadata"
    conditions as dictionary containing:
        "ip_range" as "192.168.1.0/24"
        "time_restriction" as "business_hours"
    expires_at as get_current_timestamp plus 86400.0  Note: 24 hours

Note: Revoke access
Let revoke_result be secrets.revoke_secret_access with:
    access_id as access_result.value

Note: Check permissions
Let permission_check be secrets.check_secret_permission with:
    principal as "service_account_xyz"
    operation as "read"
    resource as secret_id

If permission_check.allowed:
    Display "Access granted"
Else:
    Display "Access denied: " plus permission_check.reason
```

## Multi-Environment Configuration

Manage configurations across different environments with environment-specific profiles:

```runa
Note: Development environment
Let dev_options be config.ConfigurationOptions with:
    profile as config.DEVELOPMENT
    auto_discover_files as true
    discovery_paths as list containing "./config/dev/"
    environment_prefix as "DEV_"
    enable_secrets_integration as false
    strict_mode as false
    enable_audit_logging as false

Note: Production environment  
Let prod_options be config.ConfigurationOptions with:
    profile as config.PRODUCTION
    auto_discover_files as true
    discovery_paths as list containing "/etc/myapp/", "./config/prod/"
    environment_prefix as "PROD_"
    enable_secrets_integration as true
    strict_mode as true
    enable_audit_logging as true
    performance_monitoring as true

Note: Create environment-specific configurations
Let dev_config be config.create_configuration with options as dev_options
Let prod_config be config.create_configuration with options as prod_options
```

## Configuration File Formats

The system supports multiple configuration file formats with automatic detection:

### JSON Configuration
```json
{
  "app": {
    "name": "MyApplication",
    "port": 8080,
    "debug": false
  },
  "database": {
    "host": "${DATABASE_HOST}",
    "port": 5432,
    "name": "myapp_${ENVIRONMENT}"
  }
}
```

### YAML Configuration
```yaml
app:
  name: MyApplication
  port: 8080
  debug: false

database:
  host: ${DATABASE_HOST}
  port: 5432
  name: myapp_${ENVIRONMENT}
```

### TOML Configuration
```toml
[app]
name = "MyApplication"
port = 8080
debug = false

[database]
host = "${DATABASE_HOST}"
port = 5432
name = "myapp_${ENVIRONMENT}"
```

## Advanced Features

### Configuration Interpolation

Support for variable substitution and expression evaluation:

```runa
Note: Basic variable substitution
"Database URL: ${database.host}:${database.port}"

Note: Environment variable access
"Home directory: ${env.HOME}"

Note: Nested interpolation
"Full endpoint: ${api.base_url}/${api.version}/users"

Note: Expression evaluation (future enhancement)
"Computed value: #{app.max_memory * 0.8}"
```

### Dynamic Configuration Reloading

Implement hot-swapping of configuration without application restart:

```runa
Note: Enable automatic reloading
Let reload_options be config.ConfigurationOptions with:
    enable_file_watching as true
    auto_reload_interval as 300.0  Note: Check every 5 minutes

Note: Manual reload
Let reload_result be config.reload_configuration with:
    configuration as configuration
    options as reload_options

Match reload_result:
    When config.ConfigurationSuccess:
        Display "Configuration reloaded successfully"
        Display "Changes detected: " plus reload_result.changes_count as String
    Otherwise:
        Display "Configuration reload failed"
```

### Performance Monitoring

Track configuration system performance and optimize for your workload:

```runa
Note: Get performance metrics
Let metadata be config.get_configuration_metadata with configuration as configuration

Display "Performance Metrics:"
Display "- Load count: " plus metadata["performance_metrics"]["load_count"] as String
Display "- Cache hits: " plus metadata["performance_metrics"]["cache_hits"] as String
Display "- Cache misses: " plus metadata["performance_metrics"]["cache_misses"] as String
Display "- Validation count: " plus metadata["performance_metrics"]["validation_count"] as String
```

## Security Best Practices

### 1. Sensitive Data Handling

```runa
Note: Automatic sensitive key detection
Let sensitive_keys be list containing:
    "password", "secret", "key", "token", "credential", "auth"

Note: Explicit marking
config.set_configuration_value with:
    configuration as configuration
    key as "api.secret_key"
    value as secret_id  Note: Reference to secret, not actual value
    metadata as dictionary containing:
        "sensitive" as true
        "secret_reference" as true
```

### 2. Encryption Configuration

```runa
Note: Configure encryption for secrets
Let encryption_config be secrets.EncryptionConfig with:
    algorithm as "AES-256-GCM"
    key_derivation as "PBKDF2"
    iterations as 100000
    salt_size as 32
    iv_size as 12
    compression_enabled as true
    encoding as "base64"
```

### 3. Audit and Compliance

```runa
Note: Enable comprehensive auditing
Let audit_options be config.ConfigurationOptions with:
    enable_audit_logging as true
    performance_monitoring as true
    strict_mode as true  Note: Enforce all validation rules

Note: Compliance-ready secret creation
Let compliance_secret be secrets.create_secret with:
    name as "compliance_key"
    value as "secret_value"
    secret_type as secrets.ENCRYPTION_KEY
    metadata as dictionary containing:
        "compliance_level" as "SOC2"
        "data_classification" as "highly_confidential"
        "retention_policy" as "365_days"
        "audit_required" as true
```

## Error Handling and Troubleshooting

### Common Configuration Result Types

```runa
Note: Handle configuration retrieval results
Let result be config.get_configuration_value with:
    configuration as configuration
    key as "some.key"

Match result:
    When config.ConfigurationSuccess:
        Display "Value: " plus result.value as String
        Display "Source: " plus result.source
    
    When config.ConfigurationMissing:
        Display "Key not found: " plus result.key
        Display "Searched sources: " plus result.searched_sources as String
    
    When config.ConfigurationInvalid:
        Display "Invalid value for key: " plus result.key
        Display "Error: " plus result.error_message
    
    When config.ConfigurationException:
        Display "Configuration error: " plus result.error_message
        Display "Error code: " plus result.error_code
```

### Common Secret Result Types

```runa
Note: Handle secret operation results
Let secret_result be secrets.get_secret with:
    secret_id as "some_secret_id"

Match secret_result:
    When secrets.SecretSuccess:
        Display "Secret value retrieved successfully"
    
    When secrets.SecretNotFound:
        Display "Secret not found: " plus secret_result.secret_id
    
    When secrets.SecretAccessDenied:
        Display "Access denied to secret: " plus secret_result.secret_id
        Display "Required permission: " plus secret_result.required_permission
    
    When secrets.SecretExpired:
        Display "Secret expired at: " plus secret_result.expired_at as String
    
    When secrets.SecretCorrupted:
        Display "Secret corrupted: " plus secret_result.error_details
    
    When secrets.SecretException:
        Display "Secret operation failed: " plus secret_result.error_message
```

### Debugging Configuration Issues

```runa
Note: Enable debug logging and verbose output
Let debug_options be config.ConfigurationOptions with:
    profile as config.DEVELOPMENT
    strict_mode as false  Note: More permissive for debugging
    enable_audit_logging as true
    performance_monitoring as true

Note: Inspect configuration sources
Let sources be config.get_configuration_sources with configuration as configuration
For each source in sources:
    Display "Source: " plus source.source_id
    Display "Type: " plus source.source_type  
    Display "Priority: " plus source.priority as String
    Display "Enabled: " plus source.enabled as String
    Display "Last loaded: " plus source.last_loaded as String

Note: Check configuration metadata
Let metadata be config.get_configuration_metadata with configuration as configuration
Display "Total values: " plus metadata["values_count"] as String
Display "Last reload: " plus metadata["last_reload"] as String
Display "Cache enabled: " plus metadata["cache_enabled"] as String
```

## Integration Examples

### Web Application Configuration

```runa
Note: Complete web application setup
Let web_app_config be config.create_configuration with options as config.ConfigurationOptions with:
    profile as config.PRODUCTION
    enable_secrets_integration as true
    enable_interpolation as true
    enable_validation as true

Note: Database configuration with secrets
Let db_password_secret be secrets.create_secret with:
    name as "webapp_db_password"
    value as "secure_db_password_123"
    secret_type as secrets.DATABASE_CREDENTIAL

config.set_configuration_value with:
    configuration as web_app_config
    key as "database.host"
    value as "db.production.company.com"

config.set_configuration_value with:
    configuration as web_app_config
    key as "database.password_secret_id"
    value as db_password_secret.value

config.set_configuration_value with:
    configuration as web_app_config
    key as "database.connection_url"
    value as "postgresql://user:${database.password_secret_id}@${database.host}/webapp"

Note: API configuration
config.set_configuration_value with:
    configuration as web_app_config
    key as "api.port"
    value as "8080"

config.set_configuration_value with:
    configuration as web_app_config
    key as "api.base_url"
    value as "https://api.mycompany.com"

config.set_configuration_value with:
    configuration as web_app_config
    key as "api.health_check_url"
    value as "${api.base_url}/health"
```

### Microservices Configuration

```runa
Note: Microservice configuration with service discovery
Let microservice_config be config.create_configuration with options as config.ConfigurationOptions with:
    profile as config.PRODUCTION
    environment_prefix as "SERVICE_"
    enable_secrets_integration as true
    enable_interpolation as true

Note: Service identity
config.set_configuration_value with:
    configuration as microservice_config
    key as "service.name"
    value as "user-service"

config.set_configuration_value with:
    configuration as microservice_config
    key as "service.version"
    value as "v1.2.3"

Note: Service discovery
config.set_configuration_value with:
    configuration as microservice_config
    key as "discovery.consul_host"
    value as "consul.service.consul"

config.set_configuration_value with:
    configuration as microservice_config
    key as "service.registry_url"
    value as "http://${discovery.consul_host}:8500/v1/agent/service/register"

Note: Inter-service communication
config.set_configuration_value with:
    configuration as microservice_config
    key as "dependencies.auth_service"
    value as "auth-service.internal"

config.set_configuration_value with:
    configuration as microservice_config
    key as "dependencies.user_db"
    value as "user-db.internal:5432"
```

## Migration Guide

### From Environment Variables Only

```runa
Note: Before - direct environment access
Let old_port be get_environment_variable with name as "PORT" and default as "3000"
Let old_db_host be get_environment_variable with name as "DB_HOST" and default as "localhost"

Note: After - unified configuration management
Let config be config.create_configuration with options as config.ConfigurationOptions with:
    environment_prefix as None  Note: Include all environment variables
    enable_interpolation as true

Let port_result be config.get_configuration_value with:
    configuration as config
    key as "port"
    default_value as 3000
    data_type as "integer"

Let db_host_result be config.get_configuration_value with:
    configuration as config
    key as "db.host"
    default_value as "localhost"
    data_type as "string"
```

### From Configuration Files Only

```runa
Note: Before - direct file parsing
Let config_data be load_json_file with path as "./config.json"
Let port be config_data["app"]["port"]
Let db_host be config_data["database"]["host"]

Note: After - managed configuration loading
Let config be config.create_configuration with options as config.ConfigurationOptions with:
    auto_discover_files as true
    discovery_paths as list containing "./", "./config/"
    enable_interpolation as true
    enable_validation as true

Note: Values automatically loaded from discovered files
Let port_result be config.get_configuration_value with:
    configuration as config
    key as "app.port"
    data_type as "integer"

Let db_host_result be config.get_configuration_value with:
    configuration as config
    key as "database.host"
```

## Performance Guidelines

### Optimization Strategies

1. **Enable Caching**
   ```runa
   Let optimized_options be config.ConfigurationOptions with:
       enable_caching as true
       max_cache_size as 1000
       cache_ttl as 3600.0  Note: 1 hour
   ```

2. **Batch Operations**
   ```runa
   Note: Retrieve multiple values efficiently
   Let keys be list containing "app.name", "app.port", "database.host"
   Let results be dictionary containing
   
   For each key in keys:
       Let result be config.get_configuration_value with:
           configuration as configuration
           key as key
       Set results[key] to result
   ```

3. **Minimize Interpolation Complexity**
   ```runa
   Note: Prefer simple interpolation
   "Good: ${database.host}:${database.port}"
   
   Note: Avoid deep nesting
   "Avoid: ${app.${environment}.${region}.host}"
   ```

### Memory Management

```runa
Note: Monitor configuration memory usage
Let metadata be config.get_configuration_metadata with configuration as configuration
Let cache_stats be metadata["performance_metrics"]

If cache_stats["cache_misses"] is greater than cache_stats["cache_hits"] times 2:
    Display "Consider increasing cache size or TTL"

If metadata["values_count"] is greater than 10000:
    Display "Consider splitting configuration into multiple instances"
```

## API Reference

### Configuration Module (config)

#### Core Types
- `Configuration` - Main configuration container
- `ConfigurationOptions` - Configuration creation options
- `ConfigurationSource` - Individual configuration source
- `ConfigurationValue` - Single configuration value with metadata
- `ConfigurationSchema` - Validation schema
- `ConfigurationResult[T]` - Result wrapper for configuration operations

#### Key Functions
- `create_configuration(options)` - Create new configuration instance
- `get_configuration_value(config, key, default, type)` - Retrieve configuration value
- `set_configuration_value(config, key, value, source, metadata)` - Set configuration value
- `validate_configuration(config, schema)` - Validate against schema
- `reload_configuration(config, options)` - Reload configuration from sources
- `get_configuration_metadata(config)` - Get configuration metadata

### Secrets Module (secrets)

#### Core Types
- `Secret` - Encrypted secret with metadata
- `SecretMetadata` - Secret metadata and lifecycle information
- `SecretStore` - Secret storage backend configuration
- `SecretAccess` - Access control grant
- `SecretResult[T]` - Result wrapper for secret operations

#### Key Functions
- `create_secret(name, value, type, metadata, store)` - Create new secret
- `get_secret(secret_id, store)` - Retrieve secret value
- `update_secret(secret_id, new_value, metadata, store)` - Update secret
- `delete_secret(secret_id, force, store)` - Delete secret
- `rotate_secret(secret_id, new_value, config, store)` - Rotate secret
- `grant_secret_access(secret_id, principal, permissions, conditions, expires_at, store)` - Grant access
- `revoke_secret_access(access_id, store)` - Revoke access

### Environment Module (environment)

#### Key Functions
- `get_environment_variable(name, default)` - Get single environment variable
- `get_all_environment_variables(prefix_filter, include_sensitive)` - Get all environment variables
- `set_environment_variable(name, value)` - Set environment variable
- `detect_environment_profile()` - Auto-detect environment (dev/staging/prod)

### Loader Module (loader)

#### Core Types
- `ConfigFormat` - Supported configuration file formats
- `LoaderOptions` - File loading options
- `LoadResult` - File loading result

#### Key Functions
- `load_configuration_file(path, format, options)` - Load configuration file
- `detect_config_format(path)` - Auto-detect file format
- `validate_config_file(path, schema)` - Validate configuration file

## Conclusion

The Runa Configuration Management Ecosystem provides a comprehensive, secure, and scalable solution for managing application configuration in production environments. With its unified API, enterprise security features, and performance optimizations, it meets the demands of modern distributed applications while maintaining simplicity for developers.

For additional support, examples, or advanced use cases, please refer to the test suites in `tests/unit/stdlib/test_config.runa`, `tests/unit/stdlib/test_secrets.runa`, and `tests/integration/test_configuration_ecosystem.runa`.