# Runa Data & Configuration Format Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Table of Contents

1. [Philosophy: One Language for Everything](#philosophy-one-language-for-everything)
2. [Overview](#overview)
3. [Basic Data Structures](#basic-data-structures)
4. [Configuration Files](#configuration-files)
5. [Advanced Features](#advanced-features)
6. [File Naming Conventions](#file-naming-conventions)
7. [Comparison with Traditional Formats](#comparison-with-traditional-formats)
8. [Migration Guide](#migration-guide)
9. [Best Practices](#best-practices)
10. [Examples](#examples)

---

## Philosophy: One Language for Everything

**Runa replaces ALL traditional data/config formats:**
- ❌ JSON, YAML, TOML, XML
- ❌ .env files, .properties files
- ❌ Dockerfiles, docker-compose.yml
- ❌ package.json, requirements.txt, Cargo.toml
- ❌ CI/CD config (GitHub Actions, GitLab CI, Jenkins)
- ❌ Infrastructure as Code (Terraform HCL, CloudFormation)

**Why?**
1. **Cognitive Load Reduction** - One syntax to learn, not 10+
2. **Type Safety** - Config gets compile-time validation
3. **Executable Config** - Logic, validation, computed values built-in
4. **Tooling Unification** - One parser, LSP, formatter, linter
5. **AI-First** - AI agents master ONE language for all tasks

---

## Overview

### Runa Data Files Are Executable

Unlike static formats (JSON, YAML), Runa config files are **executable code** that produce data structures. This enables:

- **Computed values** - Calculate config based on environment
- **Validation** - Enforce constraints at load time
- **Imports** - Compose configs from multiple files
- **Type safety** - Catch errors before deployment
- **Logic** - Conditional configuration without templating

### Two Syntactic Modes

Runa supports both **Canonical** (natural language) and **Technical** (compact) syntax. Choose based on audience:

- **Canonical Mode** - For human-readable configs, documentation, tutorials
- **Technical Mode** - For machine-generated configs, performance-critical code

Both modes are **semantically equivalent** and can be mixed in the same file.

---

## Basic Data Structures

### Primitives

```runa
Note: Canonical Mode
Let name be "Alice"
Let age be 30
Let height be 1.75
Let is_active be true
Let nothing be null
```

```runa
Note: Technical Mode
name = "Alice"
age = 30
height = 1.75
is_active = true
nothing = null
```

### Lists

```runa
Note: Canonical Mode
Let fruits be a list containing "apple", "banana", "cherry"
Let numbers be a list of Integers, containing 1, 2, 3, 4, 5
```

```runa
Note: Technical Mode
fruits = ["apple", "banana", "cherry"]
numbers: List[Integer] = [1, 2, 3, 4, 5]
```

### Dictionaries

```runa
Note: Canonical Mode
Let user be a dictionary containing:
    "name" as "Alice",
    "age" as 30,
    "email" as "alice@example.com",
    "active" as true
End Dictionary
```

```runa
Note: Technical Mode
user = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "active": true
}
```

### Nested Structures

```runa
Note: Canonical Mode
Let config be a dictionary containing:
    "server" as a dictionary containing:
        "host" as "localhost",
        "port" as 8080,
        "ssl" as true
    End Dictionary,
    "database" as a dictionary containing:
        "host" as "db.example.com",
        "port" as 5432,
        "name" as "production"
    End Dictionary,
    "feature_flags" as a dictionary containing:
        "new_ui" as true,
        "beta_features" as false
    End Dictionary
End Dictionary
```

```runa
Note: Technical Mode (more compact)
config = {
    "server": {
        "host": "localhost",
        "port": 8080,
        "ssl": true
    },
    "database": {
        "host": "db.example.com",
        "port": 5432,
        "name": "production"
    },
    "feature_flags": {
        "new_ui": true,
        "beta_features": false
    }
}
```

---

## Configuration Files

### Simple Config File

**File:** `app_config.runa`

```runa
Note: Application configuration for MyApp
Note: This file replaces config.json / config.yaml

Type called "AppConfig":
    server_port as Integer
    database_url as String
    max_connections as Integer
    feature_flags as Dictionary[String, Boolean]
End Type

Process called "load_config" returns AppConfig:
    Note: Load and validate application configuration

    Return a value of type AppConfig with
        server_port as 8080,
        database_url as "postgresql://localhost/myapp",
        max_connections as 100,
        feature_flags as a dictionary containing:
            "debug_mode" as false,
            "experimental_features" as false
        End Dictionary
End Process

Note: Export the configuration
Let CONFIG be load_config()
```

**Usage in application code:**

```runa
Import "app_config.runa" as Config

Process called "start_application":
    Let port be Config.CONFIG.server_port
    Let db_url be Config.CONFIG.database_url

    Call connect_to_database(db_url)
    Call start_server_on_port(port)
End Process
```

### Environment-Based Configuration

**File:** `environment_config.runa`

```runa
Note: Configuration that adapts to environment (dev/staging/prod)

Type called "EnvironmentConfig":
    environment as String
    server_port as Integer
    database_url as String
    max_connections as Integer
    log_level as String
End Type

Process called "load_environment_config" that takes env as String returns EnvironmentConfig:
    Note: Load configuration based on environment variable

    Let port be match env:
        When "development": 3000
        When "staging": 8080
        When "production": 80
        Otherwise: 8080
    End Match

    Let db_url be match env:
        When "development": "postgresql://localhost/myapp_dev"
        When "staging": "postgresql://staging-db.example.com/myapp"
        When "production": "postgresql://prod-db.example.com/myapp"
        Otherwise: "postgresql://localhost/myapp"
    End Match

    Let max_conn be match env:
        When "development": 10
        When "staging": 50
        When "production": 500
        Otherwise: 10
    End Match

    Let log_level be match env:
        When "development": "DEBUG"
        When "staging": "INFO"
        When "production": "WARNING"
        Otherwise: "INFO"
    End Match

    Note: Validation - production requires secure settings
    If env is "production":
        If port is not 80 and port is not 443:
            Call panic("Production must use port 80 or 443")
        End If
    End If

    Return a value of type EnvironmentConfig with
        environment as env,
        server_port as port,
        database_url as db_url,
        max_connections as max_conn,
        log_level as log_level
End Process

Note: Load config from RUNA_ENV environment variable
Let CURRENT_ENV be get_environment_variable("RUNA_ENV") or default to "development"
Let CONFIG be load_environment_config(CURRENT_ENV)
```

### Secrets Management

**File:** `secrets.runa` (Replaces .env files)

```runa
Note: Application secrets (NEVER commit to version control)
Note: This file replaces .env / .secrets

Type called "Secrets":
    database_password as String
    api_key as String
    jwt_secret as String
    encryption_key as String
End Type

Process called "load_secrets" returns Secrets:
    Note: Load secrets from environment or secure vault

    Let db_password be get_environment_variable("DATABASE_PASSWORD")
    Let api_key be get_environment_variable("API_KEY")
    Let jwt_secret be get_environment_variable("JWT_SECRET")
    Let encryption_key be get_environment_variable("ENCRYPTION_KEY")

    Note: Validation - ensure all secrets are present
    If db_password is null or length of db_password < 8:
        Call panic("DATABASE_PASSWORD missing or too short")
    End If

    If api_key is null or length of api_key < 16:
        Call panic("API_KEY missing or invalid")
    End If

    Return a value of type Secrets with
        database_password as db_password,
        api_key as api_key,
        jwt_secret as jwt_secret,
        encryption_key as encryption_key
End Process

Let SECRETS be load_secrets()
```

---

## Advanced Features

### Computed Configuration

```runa
Note: Config with derived values

Type called "DeploymentConfig":
    environment as String
    base_url as String
    cdn_url as String
    api_url as String
    websocket_url as String
End Type

Process called "load_deployment_config" that takes env as String returns DeploymentConfig:
    Note: Compute URLs based on environment

    Let base_domain be match env:
        When "production": "myapp.com"
        When "staging": "staging.myapp.com"
        Otherwise: "localhost:3000"
    End Match

    Let protocol be if env is "production" or env is "staging" then "https" otherwise "http"

    Note: Derive all URLs from base configuration
    Let base_url be protocol + "://" + base_domain
    Let cdn_url be protocol + "://cdn." + base_domain
    Let api_url be protocol + "://api." + base_domain
    Let websocket_url be (if protocol is "https" then "wss" otherwise "ws") + "://" + base_domain + "/ws"

    Return a value of type DeploymentConfig with
        environment as env,
        base_url as base_url,
        cdn_url as cdn_url,
        api_url as api_url,
        websocket_url as websocket_url
End Process
```

### Validation and Constraints

```runa
Note: Config with built-in validation

Type called "DatabaseConfig":
    host as String
    port as Integer
    username as String
    database_name as String
    pool_size as Integer
    timeout_seconds as Integer
End Type

Process called "validate_database_config" that takes config as DatabaseConfig returns Boolean:
    Note: Validate database configuration constraints

    Note: Port must be in valid range
    If config.port < 1 or config.port > 65535:
        Call panic("Database port must be between 1 and 65535")
    End If

    Note: Pool size must be reasonable
    If config.pool_size < 1 or config.pool_size > 1000:
        Call panic("Database pool size must be between 1 and 1000")
    End If

    Note: Timeout must be positive
    If config.timeout_seconds < 1:
        Call panic("Database timeout must be at least 1 second")
    End If

    Note: Hostname must not be empty
    If length of config.host is 0:
        Call panic("Database host cannot be empty")
    End If

    Return true
End Process

Process called "load_database_config" returns DatabaseConfig:
    Let config be a value of type DatabaseConfig with
        host as "localhost",
        port as 5432,
        username as "app_user",
        database_name as "myapp_db",
        pool_size as 20,
        timeout_seconds as 30

    Note: Validate before returning
    Call validate_database_config(config)

    Return config
End Process

Let DB_CONFIG be load_database_config()
```

### Config Composition (Imports)

**File:** `base_config.runa`

```runa
Note: Base configuration shared across environments

Type called "BaseConfig":
    app_name as String
    app_version as String
    supported_languages as List[String]
End Type

Process called "load_base_config" returns BaseConfig:
    Return a value of type BaseConfig with
        app_name as "MyApplication",
        app_version as "1.0.0",
        supported_languages as a list containing "en", "es", "fr", "de"
End Process

Let BASE_CONFIG be load_base_config()
```

**File:** `production_config.runa`

```runa
Note: Production configuration that imports base config

Import "base_config.runa" as Base

Type called "ProductionConfig":
    base as BaseConfig
    server_port as Integer
    max_connections as Integer
End Type

Process called "load_production_config" returns ProductionConfig:
    Return a value of type ProductionConfig with
        base as Base.BASE_CONFIG,
        server_port as 443,
        max_connections as 1000
End Process

Let PROD_CONFIG be load_production_config()
```

### Dynamic Configuration

```runa
Note: Configuration that changes based on runtime conditions

Type called "FeatureFlags":
    new_dashboard as Boolean
    experimental_search as Boolean
    beta_api as Boolean
End Type

Process called "load_feature_flags" that takes user_tier as String returns FeatureFlags:
    Note: Enable features based on user tier

    Let enable_beta be user_tier is "ADMIN" or user_tier is "DEVELOPER"

    Return a value of type FeatureFlags with
        new_dashboard as true,  Note: Released to all users
        experimental_search as enable_beta,
        beta_api as enable_beta
End Process
```

---

## File Naming Conventions

### Configuration Files

- **Application config:** `app_config.runa`, `config.runa`
- **Environment-specific:** `dev_config.runa`, `staging_config.runa`, `prod_config.runa`
- **Secrets:** `secrets.runa`, `credentials.runa` (NEVER commit to version control)
- **Feature flags:** `features.runa`, `flags.runa`

### Data Files

- **Static data:** `data.runa`, `constants.runa`
- **Lookup tables:** `countries.runa`, `timezones.runa`
- **Seed data:** `seed_data.runa`, `initial_data.runa`

### Infrastructure Files

- **Deployment:** `deploy_config.runa`, `infrastructure.runa`
- **CI/CD:** `pipeline.runa`, `build.runa`
- **Docker:** `container_config.runa` (replaces Dockerfile)
- **Dependencies:** `dependencies.runa` (replaces package.json, requirements.txt)

---

## Comparison with Traditional Formats

### Runa vs JSON

**JSON (static, no logic):**
```json
{
  "server": {
    "port": 8080,
    "host": "localhost"
  },
  "database": {
    "url": "postgresql://localhost/myapp"
  }
}
```

**Runa (executable, validated, typed):**
```runa
Type called "Config":
    server_port as Integer
    server_host as String
    database_url as String
End Type

Process called "load_config" returns Config:
    Let config be a value of type Config with
        server_port as 8080,
        server_host as "localhost",
        database_url as "postgresql://localhost/myapp"

    Note: Validation not possible in JSON
    If config.server_port < 1024:
        Call panic("Port must be >= 1024 for non-root users")
    End If

    Return config
End Process

Let CONFIG be load_config()
```

### Runa vs YAML

**YAML (indentation-sensitive, no validation):**
```yaml
server:
  port: 8080
  host: localhost
  ssl:
    enabled: true
    cert_path: /etc/ssl/cert.pem
database:
  url: postgresql://localhost/myapp
  pool_size: 20
```

**Runa (explicit syntax, type-safe):**
```runa
Type called "SSLConfig":
    enabled as Boolean
    cert_path as String
End Type

Type called "ServerConfig":
    port as Integer
    host as String
    ssl as SSLConfig
End Type

Type called "DatabaseConfig":
    url as String
    pool_size as Integer
End Type

Type called "AppConfig":
    server as ServerConfig
    database as DatabaseConfig
End Type

Process called "load_config" returns AppConfig:
    Return a value of type AppConfig with
        server as a value of type ServerConfig with
            port as 8080,
            host as "localhost",
            ssl as a value of type SSLConfig with
                enabled as true,
                cert_path as "/etc/ssl/cert.pem"
        End,
        database as a value of type DatabaseConfig with
            url as "postgresql://localhost/myapp",
            pool_size as 20
End Process

Let CONFIG be load_config()
```

### Runa vs TOML

**TOML (limited nesting, no logic):**
```toml
[server]
port = 8080
host = "localhost"

[database]
url = "postgresql://localhost/myapp"
pool_size = 20

[feature_flags]
new_ui = true
beta = false
```

**Runa (better nesting, executable):**
```runa
config = {
    "server": {
        "port": 8080,
        "host": "localhost"
    },
    "database": {
        "url": "postgresql://localhost/myapp",
        "pool_size": 20
    },
    "feature_flags": {
        "new_ui": true,
        "beta": false
    }
}
```

### Runa vs .env Files

**.env (no structure, string-only):**
```
DATABASE_URL=postgresql://localhost/myapp
API_KEY=abc123xyz789
MAX_CONNECTIONS=100
DEBUG_MODE=true
```

**Runa (typed, validated):**
```runa
Type called "Environment":
    database_url as String
    api_key as String
    max_connections as Integer
    debug_mode as Boolean
End Type

Process called "load_environment" returns Environment:
    Let db_url be get_environment_variable("DATABASE_URL")
    Let api_key be get_environment_variable("API_KEY")
    Let max_conn be integer_from_string(get_environment_variable("MAX_CONNECTIONS"))
    Let debug_mode be boolean_from_string(get_environment_variable("DEBUG_MODE"))

    Note: Validation
    If length of api_key < 16:
        Call panic("API_KEY must be at least 16 characters")
    End If

    Return a value of type Environment with
        database_url as db_url,
        api_key as api_key,
        max_connections as max_conn,
        debug_mode as debug_mode
End Process

Let ENV be load_environment()
```

---

## Migration Guide

### From JSON to Runa

**Before (config.json):**
```json
{
  "name": "MyApp",
  "version": "1.0.0",
  "server": {
    "port": 8080,
    "host": "localhost"
  },
  "features": ["auth", "api", "websockets"]
}
```

**After (config.runa):**
```runa
config = {
    "name": "MyApp",
    "version": "1.0.0",
    "server": {
        "port": 8080,
        "host": "localhost"
    },
    "features": ["auth", "api", "websockets"]
}
```

**Or with types:**
```runa
Type called "Config":
    name as String
    version as String
    server_port as Integer
    server_host as String
    features as List[String]
End Type

Process called "load_config" returns Config:
    Return a value of type Config with
        name as "MyApp",
        version as "1.0.0",
        server_port as 8080,
        server_host as "localhost",
        features as a list containing "auth", "api", "websockets"
End Process

Let CONFIG be load_config()
```

### From YAML to Runa

**Before (docker-compose.yml):**
```yaml
version: '3.8'
services:
  web:
    image: myapp:latest
    ports:
      - "8080:80"
    environment:
      - NODE_ENV=production
  database:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=secret
```

**After (docker_compose.runa):**
```runa
Type called "Service":
    image as String
    ports as List[String]
    environment as List[String]
End Type

Type called "DockerCompose":
    version as String
    services as Dictionary[String, Service]
End Type

Process called "load_compose" returns DockerCompose:
    Return a value of type DockerCompose with
        version as "3.8",
        services as a dictionary containing:
            "web" as a value of type Service with
                image as "myapp:latest",
                ports as a list containing "8080:80",
                environment as a list containing "NODE_ENV=production"
            End,
            "database" as a value of type Service with
                image as "postgres:14",
                ports as an empty list,
                environment as a list containing "POSTGRES_PASSWORD=secret"
            End
        End Dictionary
End Process

Let COMPOSE_CONFIG be load_compose()
```

### From package.json to Runa

**Before (package.json):**
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^6.5.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  }
}
```

**After (dependencies.runa):**
```runa
Type called "Package":
    name as String
    version as String
    dependencies as Dictionary[String, String]
    dev_dependencies as Dictionary[String, String]
    scripts as Dictionary[String, String]
End Type

Process called "load_package" returns Package:
    Return a value of type Package with
        name as "my-app",
        version as "1.0.0",
        dependencies as a dictionary containing:
            "express" as "^4.18.0",
            "mongoose" as "^6.5.0"
        End Dictionary,
        dev_dependencies as a dictionary containing:
            "jest" as "^29.0.0"
        End Dictionary,
        scripts as a dictionary containing:
            "start" as "node index.js",
            "test" as "jest"
        End Dictionary
End Process

Let PACKAGE be load_package()
```

---

## Best Practices

### 1. Use Types for Complex Configs

```runa
Note: GOOD - Type-safe configuration
Type called "ServerConfig":
    host as String
    port as Integer
    ssl_enabled as Boolean
End Type

Let config be a value of type ServerConfig with
    host as "localhost",
    port as 8080,
    ssl_enabled as true
```

```runa
Note: AVOID - Untyped dictionary (loses type safety)
Let config be a dictionary containing:
    "host" as "localhost",
    "port" as 8080,
    "ssl_enabled" as true
End Dictionary
```

### 2. Validate Configuration at Load Time

```runa
Process called "load_config" returns AppConfig:
    Let config be a value of type AppConfig with
        server_port as 8080,
        max_connections as 100

    Note: GOOD - Validate before returning
    If config.server_port < 1024:
        Call panic("Server port must be >= 1024 for non-root")
    End If

    If config.max_connections < 1 or config.max_connections > 10000:
        Call panic("Max connections must be between 1 and 10000")
    End If

    Return config
End Process
```

### 3. Use Computed Values to Avoid Duplication

```runa
Note: GOOD - Compute related values
Process called "load_urls" that takes base_domain as String returns URLConfig:
    Let base_url be "https://" + base_domain

    Return a value of type URLConfig with
        base_url as base_url,
        api_url as base_url + "/api",
        cdn_url as "https://cdn." + base_domain,
        websocket_url as "wss://" + base_domain + "/ws"
End Process
```

```runa
Note: AVOID - Duplicate strings (error-prone)
Let urls be a value of type URLConfig with
    base_url as "https://example.com",
    api_url as "https://example.com/api",
    cdn_url as "https://cdn.example.com",
    websocket_url as "wss://example.com/ws"
```

### 4. Separate Secrets from Config

```runa
Note: GOOD - Secrets loaded from environment
Import "secrets.runa" as Secrets  Note: secrets.runa NOT in version control
Import "config.runa" as Config     Note: config.runa safe to commit

Let db_url be "postgresql://" + Config.DB_HOST + "/" + Config.DB_NAME
Let db_password be Secrets.DATABASE_PASSWORD
```

### 5. Use Environment-Based Loading

```runa
Note: GOOD - Single config file that adapts to environment
Process called "load_config" returns AppConfig:
    Let env be get_environment_variable("RUNA_ENV") or default to "development"

    Let port be match env:
        When "production": 443
        When "staging": 8080
        Otherwise: 3000
    End Match

    Return a value of type AppConfig with
        environment as env,
        server_port as port
End Process
```

```runa
Note: AVOID - Separate config files per environment (duplication)
Note: dev_config.runa, staging_config.runa, prod_config.runa
Note: (acceptable for large configs, but prefer single file with logic)
```

### 6. Document Your Config with Annotations

```runa
@Reasoning:
  Configuration for production deployment.
  Port 443 required for HTTPS.
  Max connections tuned for 100k concurrent users.
@End Reasoning

Type called "ProductionConfig":
    server_port as Integer  Note: Must be 443 for HTTPS
    max_connections as Integer  Note: Tuned for 100k users
    cache_size_mb as Integer  Note: 2GB cache for hot data
End Type

@Implementation:
  Load configuration and validate production requirements.
  Fails fast if production constraints violated.
@End Implementation

Process called "load_production_config" returns ProductionConfig:
    Let config be a value of type ProductionConfig with
        server_port as 443,
        max_connections as 500,
        cache_size_mb as 2048

    If config.server_port is not 443:
        Call panic("Production must use port 443 for HTTPS")
    End If

    Return config
End Process

Let PROD_CONFIG be load_production_config()
```

---

## Examples

### Complete Application Configuration

**File:** `app_config.runa`

```runa
Note: Complete application configuration example

@Reasoning:
  Central configuration file for MyApp.
  Supports multiple environments (dev/staging/prod).
  Validates all settings before application startup.
@End Reasoning

Note: ============================================
Note: TYPE DEFINITIONS
Note: ============================================

Type called "ServerConfig":
    host as String
    port as Integer
    ssl_enabled as Boolean
    max_request_size_mb as Integer
End Type

Type called "DatabaseConfig":
    host as String
    port as Integer
    database_name as String
    pool_size as Integer
    timeout_seconds as Integer
End Type

Type called "CacheConfig":
    enabled as Boolean
    ttl_seconds as Integer
    max_size_mb as Integer
End Type

Type called "LoggingConfig":
    level as String
    output_file as String
    max_file_size_mb as Integer
End Type

Type called "FeatureFlags":
    new_dashboard as Boolean
    experimental_search as Boolean
    beta_api as Boolean
End Type

Type called "AppConfig":
    environment as String
    server as ServerConfig
    database as DatabaseConfig
    cache as CacheConfig
    logging as LoggingConfig
    features as FeatureFlags
End Type

Note: ============================================
Note: VALIDATION FUNCTIONS
Note: ============================================

@Implementation:
  Validate server configuration constraints.
  Ensures port is in valid range and SSL enabled for production.
@End Implementation

Process called "validate_server_config" that takes config as ServerConfig, env as String returns Boolean:
    If config.port < 1 or config.port > 65535:
        Call panic("Server port must be between 1 and 65535")
    End If

    If env is "production" and not config.ssl_enabled:
        Call panic("Production environment requires SSL enabled")
    End If

    If config.max_request_size_mb < 1 or config.max_request_size_mb > 100:
        Call panic("Max request size must be between 1 and 100 MB")
    End If

    Return true
End Process

@Implementation:
  Validate database configuration constraints.
  Ensures pool size and timeouts are reasonable.
@End Implementation

Process called "validate_database_config" that takes config as DatabaseConfig returns Boolean:
    If config.port < 1 or config.port > 65535:
        Call panic("Database port must be between 1 and 65535")
    End If

    If config.pool_size < 1 or config.pool_size > 1000:
        Call panic("Database pool size must be between 1 and 1000")
    End If

    If config.timeout_seconds < 1 or config.timeout_seconds > 300:
        Call panic("Database timeout must be between 1 and 300 seconds")
    End If

    Return true
End Process

Note: ============================================
Note: CONFIGURATION LOADING
Note: ============================================

@Implementation:
  Load configuration based on environment.
  Computes environment-specific values and validates constraints.
@End Implementation

Process called "load_config" returns AppConfig:
    Note: Get environment from RUNA_ENV variable
    Let env be get_environment_variable("RUNA_ENV") or default to "development"

    Note: ============================================
    Note: Server Configuration (environment-specific)
    Note: ============================================

    Let server_port be match env:
        When "production": 443
        When "staging": 8080
        Otherwise: 3000
    End Match

    Let ssl_enabled be env is "production" or env is "staging"

    Let server_config be a value of type ServerConfig with
        host as "0.0.0.0",
        port as server_port,
        ssl_enabled as ssl_enabled,
        max_request_size_mb as 10

    Call validate_server_config(server_config, env)

    Note: ============================================
    Note: Database Configuration (environment-specific)
    Note: ============================================

    Let db_host be match env:
        When "production": "prod-db.example.com"
        When "staging": "staging-db.example.com"
        Otherwise: "localhost"
    End Match

    Let db_name be match env:
        When "production": "myapp_production"
        When "staging": "myapp_staging"
        Otherwise: "myapp_development"
    End Match

    Let db_pool_size be match env:
        When "production": 100
        When "staging": 20
        Otherwise: 5
    End Match

    Let db_config be a value of type DatabaseConfig with
        host as db_host,
        port as 5432,
        database_name as db_name,
        pool_size as db_pool_size,
        timeout_seconds as 30

    Call validate_database_config(db_config)

    Note: ============================================
    Note: Cache Configuration
    Note: ============================================

    Let cache_enabled be env is "production" or env is "staging"

    Let cache_config be a value of type CacheConfig with
        enabled as cache_enabled,
        ttl_seconds as 3600,
        max_size_mb as 512

    Note: ============================================
    Note: Logging Configuration
    Note: ============================================

    Let log_level be match env:
        When "production": "WARNING"
        When "staging": "INFO"
        Otherwise: "DEBUG"
    End Match

    Let log_file be "./logs/app_" + env + ".log"

    Let logging_config be a value of type LoggingConfig with
        level as log_level,
        output_file as log_file,
        max_file_size_mb as 100

    Note: ============================================
    Note: Feature Flags
    Note: ============================================

    Let features be a value of type FeatureFlags with
        new_dashboard as true,
        experimental_search as env is not "production",
        beta_api as env is "development"

    Note: ============================================
    Note: Assemble Final Configuration
    Note: ============================================

    Return a value of type AppConfig with
        environment as env,
        server as server_config,
        database as db_config,
        cache as cache_config,
        logging as logging_config,
        features as features
End Process

Note: Export global configuration
Let CONFIG be load_config()
```

**Usage in application:**

```runa
Import "app_config.runa" as Config

Process called "main":
    Note: Configuration is loaded and validated at import time
    Let cfg be Config.CONFIG

    Call display("Starting application in " + cfg.environment + " mode")
    Call display("Server: " + cfg.server.host + ":" + string_from(cfg.server.port))
    Call display("Database: " + cfg.database.host + "/" + cfg.database.database_name)

    Call start_application(cfg)
End Process
```

---

## Summary

**Runa replaces ALL configuration formats with:**
- ✅ Type-safe, validated configuration
- ✅ Executable logic (computed values, conditionals)
- ✅ One syntax to learn (Canonical or Technical mode)
- ✅ Import/composition for modular configs
- ✅ Built-in documentation via annotations
- ✅ Compile-time error checking

**Stop using:** JSON, YAML, TOML, XML, .env files, Dockerfiles, package.json, etc.

**Start using:** `.runa` files for EVERYTHING.

---

## See Also

- [Runa Syntax Modes](./runa_syntax_modes.md) - Canonical vs Technical syntax
- [Runa Collection Syntax](./runa_collection_syntax.md) - Lists and dictionaries
- [Runa Type System](./runa_type_system_reference.md) - Type definitions
- [Runa Annotation System](./runa_annotation_system.md) - Documentation annotations
- [Runa Standard Library](./runa_standard_library.md) - Built-in functionality

---

**End of Document**
