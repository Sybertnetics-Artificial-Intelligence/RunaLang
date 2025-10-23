# Runa Domain-Specific Formats

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2024-10-18

---

## Table of Contents

1. [Data and Configuration Formats](#data-and-configuration-formats)
2. [Database Schema](#database-schema)
3. [Documentation Format](#documentation-format)
4. [API Specification](#api-specification)
5. [Protocol Definition](#protocol-definition)
6. [GraphQL Schema](#graphql-schema)
7. [Web Markup](#web-markup)
8. [Web Styling](#web-styling)

---

# Data and Configuration Formats

---

## Subtable of Contents

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

Runa supports both **Canon** (natural language) and **Developer** (compact) syntax. Choose based on audience:

- **Canon Mode** - For human-readable configs, documentation, tutorials
- **Developer Mode** - For machine-generated configs, performance-critical code

Both modes are **semantically equivalent** and can be mixed in the same file.

---

## Basic Data Structures

### Primitives

```runa
Note: Canon Mode
Let name be "Alice"
Let age be 30
Let height be 1.75
Let is_active be true
Let nothing be null
```

```runa
Note: Developer Mode
name = "Alice"
age = 30
height = 1.75
is_active = true
nothing = null
```

### Lists

```runa
Note: Canon Mode
Let fruits be a list containing "apple", "banana", "cherry"
Let numbers be a list of Integers, containing 1, 2, 3, 4, 5
```

```runa
Note: Developer Mode
fruits = ["apple", "banana", "cherry"]
numbers: List[Integer] = [1, 2, 3, 4, 5]
```

### Dictionaries

```runa
Note: Canon Mode
Let user be a dictionary containing:
    "name" as "Alice",
    "age" as 30,
    "email" as "alice@example.com",
    "active" as true
End Dictionary
```

```runa
Note: Developer Mode
user = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "active": true
}
```

### Nested Structures

```runa
Note: Canon Mode
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
Note: Developer Mode (more compact)
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
- ✅ One syntax to learn (Canon or Developer mode)
- ✅ Import/composition for modular configs
- ✅ Built-in documentation via annotations
- ✅ Compile-time error checking

**Stop using:** JSON, YAML, TOML, XML, .env files, Dockerfiles, package.json, etc.

**Start using:** `.runa` files for EVERYTHING.

---

## See Also

- [Runa Syntax Modes](./runa_syntax_modes.md) - Canon vs Developer syntax
- [Runa Type System](./runa_type_system.md) - Type definitions
- [Runa Annotation System](./runa_annotation_system.md) - Documentation annotations
- [Runa Standard Library](./runa_standard_library.md) - Built-in functionality

---

# Database Schema

## Subtable of Contents

1. [Overview](#overview-1)
2. [Basic Schema Definition](#basic-schema-definition)
3. [SQL DDL Comparison](#sql-ddl-comparison)
4. [Migrations](#migrations)
5. [ORM Model Comparison](#orm-model-comparison)
6. [Query Interface](#query-interface)
7. [Prisma Comparison](#prisma-comparison)
8. [Summary](#summary-1)

---

## Overview

**Runa replaces SQL DDL with executable `.runa` schema files.**

**Replaces:**
- ❌ SQL DDL (CREATE TABLE, ALTER TABLE, etc.)
- ❌ ORM models (Django, SQLAlchemy, ActiveRecord)
- ❌ Prisma schema
- ❌ Database migration files

---

## Basic Schema Definition

**File:** `schema.runa`

```runa
Note: Database schema definition
Note: Replaces SQL DDL, ORM models, Prisma schema

Import "runa/database" as DB

Type called "TableColumn":
    name as String
    type as String
    nullable as Boolean
    default_value as String
    primary_key as Boolean
    unique as Boolean
End Type

Type called "TableSchema":
    name as String
    columns as List[TableColumn]
    indexes as List[Index]
    foreign_keys as List[ForeignKey]
End Type

Process called "define_users_table" returns TableSchema:
    Return a value of type TableSchema with
        name as "users",
        columns as a list containing:
            col("id", "INTEGER", false, "", true, true),
            col("email", "VARCHAR(255)", false, "", false, true),
            col("password_hash", "VARCHAR(255)", false, "", false, false),
            col("created_at", "TIMESTAMP", false, "CURRENT_TIMESTAMP", false, false),
            col("updated_at", "TIMESTAMP", false, "CURRENT_TIMESTAMP", false, false)
        End,
        indexes as a list containing:
            index("idx_email", "email")
        End,
        foreign_keys as an empty list
End Process

Process called "col" that takes name as String, type as String, nullable as Boolean, default_val as String, pk as Boolean, unique as Boolean returns TableColumn:
    Return a value of type TableColumn with
        name as name,
        type as type,
        nullable as nullable,
        default_value as default_val,
        primary_key as pk,
        unique as unique
End Process

Process called "index" that takes name as String, column as String returns Index:
    Return DB.create_index(name, column)
End Process

Process called "main":
    Let users_table be define_users_table()
    Call DB.create_table(users_table)
    Call display("✓ Tables created")
End Process
```

---

## SQL DDL Comparison

**Before (schema.sql):**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_email ON users(email);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    published_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**After (schema.runa):**
```runa
Process called "define_schema":
    Let users be DB.table("users",
        DB.column("id", DB.INTEGER, primary_key(true)),
        DB.column("email", DB.VARCHAR(255), unique(true)),
        DB.column("password_hash", DB.VARCHAR(255)),
        DB.column("created_at", DB.TIMESTAMP, default("CURRENT_TIMESTAMP")),
        DB.index("email")
    )

    Let posts be DB.table("posts",
        DB.column("id", DB.INTEGER, primary_key(true)),
        DB.column("user_id", DB.INTEGER, not_null(true)),
        DB.column("title", DB.VARCHAR(255)),
        DB.column("content", DB.TEXT),
        DB.column("published_at", DB.TIMESTAMP, nullable(true)),
        DB.foreign_key("user_id", "users", "id", on_delete("CASCADE"))
    )

    Call DB.create_tables(a list containing users, posts)
End Process
```

---

## Migrations

**File:** `migrations/001_create_users.runa`

```runa
Note: Database migration
Note: Replaces SQL migration files

Import "runa/database/migration" as Migration

Process called "up":
    Note: Apply migration
    Call Migration.create_table("users",
        Migration.column("id", "INTEGER", primary_key(true)),
        Migration.column("email", "VARCHAR(255)", unique(true)),
        Migration.column("created_at", "TIMESTAMP", default("NOW()"))
    )

    Call display("✓ Migration applied: create users table")
End Process

Process called "down":
    Note: Rollback migration
    Call Migration.drop_table("users")

    Call display("✓ Migration rolled back: drop users table")
End Process
```

**File:** `migrations/002_add_user_profile.runa`

```runa
Process called "up":
    Note: Add column to existing table
    Call Migration.add_column("users", "bio", "TEXT", nullable(true))
    Call Migration.add_column("users", "avatar_url", "VARCHAR(255)", nullable(true))

    Call display("✓ Migration applied: add profile columns")
End Process

Process called "down":
    Call Migration.drop_column("users", "bio")
    Call Migration.drop_column("users", "avatar_url")

    Call display("✓ Migration rolled back: remove profile columns")
End Process
```

---

## ORM Model Comparison

**Before (Django ORM):**
```python
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(null=True)
```

**After (Runa ORM):**
```runa
Type called "User":
    id as Integer
    email as String
    password_hash as String
    created_at as Timestamp
End Type

Type called "Post":
    id as Integer
    user_id as Integer
    title as String
    content as String
    published_at as Timestamp
End Type

Process called "define_user_model" returns DB.Model:
    Return DB.model("User", "users",
        DB.field("id", DB.INTEGER, primary_key(true)),
        DB.field("email", DB.VARCHAR(255), unique(true)),
        DB.field("password_hash", DB.VARCHAR(255)),
        DB.field("created_at", DB.TIMESTAMP, auto_now_add(true))
    )
End Process

Process called "define_post_model" returns DB.Model:
    Return DB.model("Post", "posts",
        DB.field("id", DB.INTEGER, primary_key(true)),
        DB.field("user_id", DB.INTEGER, foreign_key("User", "id")),
        DB.field("title", DB.VARCHAR(255)),
        DB.field("content", DB.TEXT),
        DB.field("published_at", DB.TIMESTAMP, nullable(true))
    )
End Process
```

---

## Query Interface

```runa
Process called "query_users":
    Note: Find all users with .com email addresses
    Let users be DB.query("User")
        .where("email", "LIKE", "%.com")
        .order_by("created_at", "DESC")
        .limit(10)
        .execute()

    For Each user in users:
        Call display(user.email)
    End For
End Process

Process called "create_user" that takes email as String, password as String:
    Let user be DB.insert("User", a dictionary containing:
        "email" as email,
        "password_hash" as hash_password(password),
        "created_at" as DB.now()
    End Dictionary)

    Return user
End Process
```

---

## Prisma Comparison

**Before (schema.prisma):**
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id          Int       @id @default(autoincrement())
  title       String
  content     String?
  published   Boolean   @default(false)
  author      User      @relation(fields: [authorId], references: [id])
  authorId    Int
  publishedAt DateTime?
}
```

**After (schema.runa):**
```runa
Let User_model be DB.model("User", "users",
    DB.id_field(),
    DB.field("email", DB.STRING, unique(true)),
    DB.has_many("posts", "Post"),
    DB.timestamp("created_at", auto_now_add(true))
)

Let Post_model be DB.model("Post", "posts",
    DB.id_field(),
    DB.field("title", DB.STRING),
    DB.field("content", DB.STRING, nullable(true)),
    DB.field("published", DB.BOOLEAN, default(false)),
    DB.belongs_to("author", "User", foreign_key("author_id")),
    DB.timestamp("published_at", nullable(true))
)
```

---

## Summary

**Runa replaces SQL/ORM with:**
- ✅ Type-safe schema definitions
- ✅ Executable migrations
- ✅ Unified query interface
- ✅ Replaces SQL, Django ORM, Prisma, etc.

**Stop using:** SQL DDL, ORM models
**Start using:** `schema.runa`, `migrations/*.runa`

---

# Documentation Format

## Subtable of Contents

1. [Overview](#overview-2)
2. [Basic Documentation File](#basic-documentation-file)
3. [Markdown Comparison](#markdown-comparison)
4. [API Documentation](#api-documentation)
5. [CHANGELOG Generation](#changelog-generation)
6. [Interactive Documentation](#interactive-documentation)
7. [Documentation with Diagrams](#documentation-with-diagrams)
8. [Multi-Format Output](#multi-format-output)
9. [Documentation Testing](#documentation-testing)
10. [Static Site Generation](#static-site-generation)
11. [Summary](#summary-2)

---

## Overview

**Runa replaces Markdown and documentation formats with executable `.runa` documentation files.**

**Replaces:**
- ❌ Markdown (.md)
- ❌ reStructuredText (.rst)
- ❌ AsciiDoc
- ❌ LaTeX (for docs)
- ❌ Sphinx, MkDocs, Docusaurus configs

---

## Basic Documentation File

**File:** `README.runa`

```runa
Note: Project documentation in Runa
Note: Replaces README.md

Import "runa/docs" as Doc

Process called "generate_readme" returns Doc.Document:
    Return Doc.document(
        Doc.title("My Project"),
        Doc.subtitle("A revolutionary application"),

        Doc.section("Overview",
            Doc.paragraph("This is a project that demonstrates..."),
            Doc.paragraph("Key features include:")
        ),

        Doc.section("Installation",
            Doc.code_block("bash", "runa install my-project"),
            Doc.paragraph("Or from source:"),
            Doc.code_block("bash", "git clone https://github.com/user/my-project\ncd my-project\nruna build.runa")
        ),

        Doc.section("Usage",
            Doc.code_block("runa", "Import \"my-project\" as Project\n\nCall Project.run()"),
            Doc.paragraph("See examples/ directory for more.")
        ),

        Doc.section("License",
            Doc.paragraph("MIT License - see LICENSE file")
        )
    )
End Process

Process called "main":
    Let readme be generate_readme()
    Call Doc.render_to_markdown(readme, "README.md")
    Call Doc.render_to_html(readme, "docs/index.html")
    Call display("✓ Documentation generated")
End Process
```

**Output (README.md):**
```markdown
# My Project
## A revolutionary application

## Overview
This is a project that demonstrates...

Key features include:

## Installation
```bash
runa install my-project
```

Or from source:
```bash
git clone https://github.com/user/my-project
cd my-project
runa build.runa
```

## Usage
...
```

---

## Markdown Comparison

**Before (README.md):**
```markdown
# My Project

A revolutionary application.

## Installation

```bash
npm install my-project
```

## Usage

```javascript
const project = require('my-project');
project.run();
```
```

**After (README.runa):**
```runa
Let readme be Doc.document(
    Doc.h1("My Project"),
    Doc.p("A revolutionary application."),
    Doc.h2("Installation"),
    Doc.code("bash", "runa install my-project"),
    Doc.h2("Usage"),
    Doc.code("runa", "Import \"my-project\" as Project\nCall Project.run()")
)

Call Doc.render(readme, "README.md")
```

---

## API Documentation

**File:** `docs/api_reference.runa`

```runa
Note: API reference documentation

Process called "generate_api_docs" returns Doc.Document:
    Return Doc.document(
        Doc.title("API Reference"),

        Doc.section("Calculator Module",
            Doc.function_doc(
                "add",
                "Adds two numbers together",
                parameters(
                    param("a", "Integer", "First number"),
                    param("b", "Integer", "Second number")
                ),
                returns("Integer", "Sum of a and b"),
                example("add(2, 3)", "Returns 5")
            ),

            Doc.function_doc(
                "multiply",
                "Multiplies two numbers",
                parameters(
                    param("a", "Integer", "First number"),
                    param("b", "Integer", "Second number")
                ),
                returns("Integer", "Product of a and b"),
                example("multiply(4, 5)", "Returns 20")
            )
        )
    )
End Process
```

---

## CHANGELOG Generation

**File:** `CHANGELOG.runa`

```runa
Note: Changelog generation

Type called "ChangeEntry":
    version as String
    date as String
    type as String  Note: "added", "changed", "fixed", "removed"
    description as String
End Type

Process called "generate_changelog" returns Doc.Document:
    Let entries be a list containing:
        entry("1.2.0", "2025-10-08", "added", "New database migration system"),
        entry("1.2.0", "2025-10-08", "changed", "Improved error messages"),
        entry("1.1.0", "2025-09-15", "fixed", "Bug in user authentication"),
        entry("1.0.0", "2025-08-01", "added", "Initial release")

    Let changelog be Doc.document(
        Doc.title("Changelog"),
        Doc.paragraph("All notable changes to this project.")
    )

    Note: Group by version
    Let versions be group_by_version(entries)

    For Each version, version_entries in versions:
        Call Doc.add_section(changelog, "Version " + version,
            Doc.subsection("Added",
                filter_and_list(version_entries, "added")
            ),
            Doc.subsection("Changed",
                filter_and_list(version_entries, "changed")
            ),
            Doc.subsection("Fixed",
                filter_and_list(version_entries, "fixed")
            )
        )
    End For

    Return changelog
End Process

Process called "entry" that takes version as String, date as String, type as String, desc as String returns ChangeEntry:
    Return a value of type ChangeEntry with
        version as version,
        date as date,
        type as type,
        description as desc
End Process
```

---

## Interactive Documentation

```runa
Note: Documentation with executable examples

Process called "interactive_tutorial" returns Doc.Document:
    Return Doc.document(
        Doc.title("Interactive Tutorial"),

        Doc.section("Basic Arithmetic",
            Doc.paragraph("Let's learn addition:"),

            Doc.interactive_example(
                "add(2, 3)",
                run_example(add(2, 3))
            ),

            Doc.paragraph("Try different numbers:"),

            Doc.interactive_widget(arithmetic_calculator)
        )
    )
End Process

Process called "run_example" that takes result as Any returns String:
    Return "Result: " + string_from(result)
End Process

Process called "arithmetic_calculator" returns Doc.Widget:
    Note: Create interactive calculator widget
    Return Doc.widget("calculator",
        Doc.input_field("a", "integer"),
        Doc.input_field("b", "integer"),
        Doc.button("Add", on_add),
        Doc.button("Multiply", on_multiply),
        Doc.output_field("result")
    )
End Process
```

---

## Documentation with Diagrams

```runa
Process called "docs_with_diagrams" returns Doc.Document:
    Return Doc.document(
        Doc.title("System Architecture"),

        Doc.section("Overview",
            Doc.paragraph("The system consists of three main components:")
        ),

        Doc.diagram("sequence",
            diagram_node("Client", "Browser"),
            diagram_node("Server", "API"),
            diagram_node("Database", "PostgreSQL"),

            diagram_connection("Client", "Server", "HTTP Request"),
            diagram_connection("Server", "Database", "SQL Query"),
            diagram_connection("Database", "Server", "Result"),
            diagram_connection("Server", "Client", "HTTP Response")
        ),

        Doc.diagram("flowchart",
            flowchart_start("Start"),
            flowchart_decision("User logged in?"),
            flowchart_process("Show login form"),
            flowchart_process("Show dashboard"),
            flowchart_end("End")
        )
    )
End Process
```

---

## Multi-Format Output

```runa
Process called "generate_all_formats":
    Let doc be generate_api_docs()

    Note: Generate multiple output formats
    Call Doc.render_to_markdown(doc, "docs/api.md")
    Call Doc.render_to_html(doc, "docs/api.html")
    Call Doc.render_to_pdf(doc, "docs/api.pdf")
    Call Doc.render_to_latex(doc, "docs/api.tex")

    Call display("✓ Documentation generated in all formats")
End Process
```

---

## Documentation Testing

```runa
Process called "test_documentation_examples":
    Note: Extract and test all code examples from documentation
    Let doc be generate_readme()
    Let code_examples be Doc.extract_code_blocks(doc, "runa")

    For Each example in code_examples:
        Call display("Testing example: " + example.code)

        Let result be execute_code(example.code)

        If result.success:
            Call display("  ✓ Example works")
        Otherwise:
            Call display("  ✗ Example failed: " + result.error)
        End If
    End For
End Process
```

---

## Static Site Generation

**File:** `docs/site.runa`

```runa
Note: Static site configuration

Type called "SiteConfig":
    title as String
    pages as List[Page]
    theme as String
    navigation as List[NavItem]
End Type

Process called "define_site" returns SiteConfig:
    Return a value of type SiteConfig with
        title as "My Project Documentation",
        pages as a list containing:
            page("index", "Home", "docs/index.runa"),
            page("quickstart", "Quick Start", "docs/quickstart.runa"),
            page("api", "API Reference", "docs/api.runa"),
            page("examples", "Examples", "docs/examples.runa")
        End,
        theme as "modern",
        navigation as a list containing:
            nav_item("Documentation", "/"),
            nav_item("API", "/api"),
            nav_item("GitHub", "https://github.com/user/project")
        End
End Process

Process called "build_site":
    Let config be define_site()
    Call Doc.build_static_site(config, "dist/")
    Call display("✓ Static site built to dist/")
End Process
```

---

## Summary

**Runa replaces documentation formats with:**
- ✅ Executable documentation
- ✅ Multi-format output (Markdown, HTML, PDF)
- ✅ Interactive examples
- ✅ Automated API documentation
- ✅ Diagram generation
- ✅ Testable code examples

**Stop using:** Markdown, reStructuredText, MkDocs
**Start using:** `.runa` documentation files


---

# API Specification

## Subtable of Contents

1. [Overview](#overview-3)
2. [Basic API Specification](#basic-api-specification)
3. [OpenAPI/Swagger Comparison](#openapiswagger-comparison)
4. [Authentication Specification](#authentication-specification)
5. [Request/Response Examples](#requestresponse-examples)
6. [API Client Generation](#api-client-generation)
7. [Validation](#validation)
8. [Summary](#summary-3)

---

## Overview

**Runa replaces API specification formats with executable `.runa` files.**

**Replaces:**
- ❌ OpenAPI/Swagger (YAML/JSON)
- ❌ API Blueprint
- ❌ RAML
- ❌ Postman collections

---

## Basic API Specification

**File:** `api_spec.runa`

```runa
Note: API specification
Note: Replaces OpenAPI/Swagger

Import "runa/api" as API

Type called "Endpoint":
    path as String
    method as String
    description as String
    parameters as List[Parameter]
    request_body as Schema
    responses as Dictionary[Integer, Response]
End Type

Process called "define_api" returns API.Specification:
    Return API.spec("My API", "1.0.0",
        API.server("https://api.example.com"),

        API.endpoint("GET", "/users",
            API.description("Get all users"),
            API.query_param("page", "integer", optional(true)),
            API.query_param("limit", "integer", optional(true)),
            API.response(200, "Success", user_list_schema()),
            API.response(401, "Unauthorized", error_schema())
        ),

        API.endpoint("POST", "/users",
            API.description("Create a new user"),
            API.request_body(user_create_schema()),
            API.response(201, "Created", user_schema()),
            API.response(400, "Bad Request", error_schema())
        ),

        API.endpoint("GET", "/users/{id}",
            API.description("Get user by ID"),
            API.path_param("id", "integer"),
            API.response(200, "Success", user_schema()),
            API.response(404, "Not Found", error_schema())
        )
    )
End Process

Process called "user_schema" returns API.Schema:
    Return API.object_schema(
        API.field("id", "integer"),
        API.field("email", "string", format("email")),
        API.field("created_at", "string", format("date-time"))
    )
End Process

Process called "main":
    Let api_spec be define_api()
    Call API.generate_docs(api_spec, "api_docs.html")
    Call display("✓ API documentation generated")
End Process
```

---

## OpenAPI/Swagger Comparison

**Before (openapi.yaml):**
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /users:
    get:
      summary: Get all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Success
        '404':
          description: Not Found

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
```

**After (api_spec.runa):**
```runa
Let api be API.specification("My API", "1.0.0",
    endpoint("GET", "/users",
        query("page", INT, optional),
        query("limit", INT, optional),
        response(200, user_list_schema)
    ),

    endpoint("GET", "/users/{id}",
        path("id", INT, required),
        response(200, user_schema),
        response(404, error_schema)
    )
)

Let user_schema be object_schema(
    field("id", INT),
    field("email", STRING, format("email"))
)
```

---

## Authentication Specification

```runa
Process called "api_with_auth" returns API.Specification:
    Return API.spec("Secure API", "1.0.0",
        API.security_scheme("bearer", "JWT",
            API.bearer_format("JWT")
        ),

        API.endpoint("GET", "/protected",
            API.security("bearer"),
            API.response(200, "Success", data_schema()),
            API.response(401, "Unauthorized")
        )
    )
End Process
```

---

## Request/Response Examples

```runa
Process called "endpoint_with_examples" returns Endpoint:
    Return API.endpoint("POST", "/users",
        API.request_body(user_create_schema(),
            API.example("basic_user", a dictionary containing:
                "email" as "user@example.com",
                "password" as "securepassword123"
            End Dictionary)
        ),

        API.response(201, "Created", user_schema(),
            API.example("created_user", a dictionary containing:
                "id" as 1,
                "email" as "user@example.com",
                "created_at" as "2025-10-08T12:00:00Z"
            End Dictionary)
        )
    )
End Process
```

---

## API Client Generation

```runa
Process called "generate_client":
    Let api_spec be define_api()

    Note: Generate client library
    Call API.generate_client(api_spec, "typescript", "client/")
    Call API.generate_client(api_spec, "python", "client/")
    Call API.generate_client(api_spec, "go", "client/")

    Call display("✓ API clients generated")
End Process
```

---

## Validation

```runa
Process called "validate_request" that takes endpoint as String, data as Dictionary[String, Any] returns Boolean:
    Let api_spec be define_api()
    Let validation_result be API.validate(api_spec, endpoint, data)

    If validation_result.is_valid:
        Return true
    Otherwise:
        For Each error in validation_result.errors:
            Call display("Validation error: " + error.message)
        End For
        Return false
    End If
End Process
```

---

## Summary

**Runa replaces API specs with:**
- ✅ Type-safe endpoint definitions
- ✅ Executable specifications
- ✅ Automatic client generation
- ✅ Built-in validation

**Stop using:** OpenAPI YAML/JSON
**Start using:** `api_spec.runa`


---

# Protocol Definition

## Subtable of Contents

1. [Overview](#overview-4)
2. [Basic Protocol Definition](#basic-protocol-definition)
3. [Protobuf Comparison](#protobuf-comparison)
4. [Enumerations](#enumerations)
5. [Nested Messages](#nested-messages)
6. [Binary Serialization](#binary-serialization)
7. [Code Generation](#code-generation)
8. [Thrift Comparison](#thrift-comparison)
9. [Summary](#summary-4)

---

## Overview

**Runa replaces binary protocol definitions with executable `.runa` files.**

**Replaces:**
- ❌ Protocol Buffers (.proto)
- ❌ Apache Thrift (.thrift)
- ❌ Apache Avro schemas
- ❌ FlatBuffers schemas

---

## Basic Protocol Definition

**File:** `protocol.runa`

```runa
Note: Protocol definition
Note: Replaces Protocol Buffers .proto files

Import "runa/protocol" as Proto

Type called "Message":
    id as Integer
    name as String
    fields as List[Field]
End Type

Process called "define_protocol" returns Proto.Protocol:
    Return Proto.protocol("UserService", "1.0",
        Proto.message("User",
            Proto.field(1, "id", Proto.INT64, required(true)),
            Proto.field(2, "email", Proto.STRING, required(true)),
            Proto.field(3, "name", Proto.STRING, optional(true)),
            Proto.field(4, "created_at", Proto.TIMESTAMP, required(true))
        ),

        Proto.message("CreateUserRequest",
            Proto.field(1, "email", Proto.STRING, required(true)),
            Proto.field(2, "password", Proto.STRING, required(true))
        ),

        Proto.message("CreateUserResponse",
            Proto.field(1, "user", "User", required(true)),
            Proto.field(2, "success", Proto.BOOL, required(true))
        ),

        Proto.service("UserService",
            Proto.rpc("CreateUser", "CreateUserRequest", "CreateUserResponse"),
            Proto.rpc("GetUser", "GetUserRequest", "User"),
            Proto.rpc("ListUsers", "ListUsersRequest", "ListUsersResponse")
        )
    )
End Process

Let PROTOCOL be define_protocol()
```

---

## Protobuf Comparison

**Before (.proto):**
```protobuf
syntax = "proto3";

package userservice;

message User {
  int64 id = 1;
  string email = 2;
  string name = 3;
  int64 created_at = 4;
}

message CreateUserRequest {
  string email = 1;
  string password = 2;
}

message CreateUserResponse {
  User user = 1;
  bool success = 2;
}

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}
```

**After (protocol.runa):**
```runa
Note: Equivalent Runa protocol (shown above)
```

---

## Enumerations

```runa
Process called "protocol_with_enums" returns Proto.Protocol:
    Return Proto.protocol("MessageService", "1.0",
        Proto.enum("MessageStatus",
            Proto.enum_value("PENDING", 0),
            Proto.enum_value("SENT", 1),
            Proto.enum_value("DELIVERED", 2),
            Proto.enum_value("READ", 3)
        ),

        Proto.message("Message",
            Proto.field(1, "id", Proto.INT64),
            Proto.field(2, "content", Proto.STRING),
            Proto.field(3, "status", "MessageStatus")
        )
    )
End Process
```

---

## Nested Messages

```runa
Process called "protocol_with_nested" returns Proto.Protocol:
    Return Proto.protocol("AddressBook", "1.0",
        Proto.message("Person",
            Proto.field(1, "name", Proto.STRING),
            Proto.field(2, "id", Proto.INT32),
            Proto.field(3, "email", Proto.STRING),

            Proto.nested_message("PhoneNumber",
                Proto.field(1, "number", Proto.STRING),
                Proto.field(2, "type", "PhoneType")
            ),

            Proto.field(4, "phones", Proto.REPEATED, "PhoneNumber")
        ),

        Proto.enum("PhoneType",
            Proto.enum_value("MOBILE", 0),
            Proto.enum_value("HOME", 1),
            Proto.enum_value("WORK", 2)
        )
    )
End Process
```

---

## Binary Serialization

```runa
Process called "serialize_message" that takes user as User returns Bytes:
    Let proto be define_protocol()
    Let serialized be Proto.serialize(proto, "User", user)
    Return serialized
End Process

Process called "deserialize_message" that takes data as Bytes returns User:
    Let proto be define_protocol()
    Let user be Proto.deserialize(proto, "User", data)
    Return user
End Process
```

---

## Code Generation

```runa
Process called "generate_protocol_code":
    Let proto be define_protocol()

    Note: Generate code for multiple languages
    Call Proto.generate_code(proto, "rust", "generated/rust/")
    Call Proto.generate_code(proto, "go", "generated/go/")
    Call Proto.generate_code(proto, "python", "generated/python/")

    Call display("✓ Protocol code generated")
End Process
```

---

## Thrift Comparison

**Before (.thrift):**
```thrift
struct User {
  1: i64 id,
  2: string email,
  3: optional string name
}

service UserService {
  User getUser(1: i64 id),
  list<User> listUsers(),
  User createUser(1: string email, 2: string password)
}
```

**After (protocol.runa):**
```runa
Let protocol be Proto.protocol("UserService", "1.0",
    Proto.struct("User",
        Proto.field(1, "id", Proto.I64),
        Proto.field(2, "email", Proto.STRING),
        Proto.field(3, "name", Proto.STRING, optional(true))
    ),

    Proto.service("UserService",
        Proto.method("getUser",
            Proto.param(1, "id", Proto.I64),
            Proto.returns("User")
        ),
        Proto.method("listUsers",
            Proto.returns(Proto.list_of("User"))
        ),
        Proto.method("createUser",
            Proto.param(1, "email", Proto.STRING),
            Proto.param(2, "password", Proto.STRING),
            Proto.returns("User")
        )
    )
)
```

---

## Summary

**Runa replaces protocol definitions with:**
- ✅ Type-safe message definitions
- ✅ Binary serialization
- ✅ Multi-language code generation
- ✅ RPC service definitions

**Stop using:** .proto, .thrift files
**Start using:** `protocol.runa`


---

# GraphQL Schema

## Subtable of Contents

1. [Overview](#overview-5)
2. [Basic GraphQL Schema](#basic-graphql-schema)
3. [GraphQL SDL Comparison](#graphql-sdl-comparison)
4. [Resolvers](#resolvers)
5. [Subscriptions](#subscriptions)
6. [Input Types](#input-types)
7. [Directives](#directives)
8. [Summary](#summary-5)

---

## Overview

**Runa replaces GraphQL SDL with executable `.runa` schema files.**

**Replaces:**
- ❌ GraphQL SDL (.graphql files)
- ❌ Apollo Schema
- ❌ GraphQL Code Generator configs

---

## Basic GraphQL Schema

**File:** `graphql_schema.runa`

```runa
Note: GraphQL schema definition
Note: Replaces .graphql SDL files

Import "runa/graphql" as GQL

Process called "define_schema" returns GQL.Schema:
    Return GQL.schema(
        GQL.type("User",
            GQL.field("id", GQL.ID, non_null(true)),
            GQL.field("email", GQL.String, non_null(true)),
            GQL.field("posts", GQL.list_of("Post")),
            GQL.field("created_at", GQL.String)
        ),

        GQL.type("Post",
            GQL.field("id", GQL.ID, non_null(true)),
            GQL.field("title", GQL.String, non_null(true)),
            GQL.field("content", GQL.String),
            GQL.field("author", "User", non_null(true)),
            GQL.field("published_at", GQL.String)
        ),

        GQL.query(
            GQL.field("users", GQL.list_of("User")),
            GQL.field("user", "User",
                GQL.arg("id", GQL.ID, non_null(true))
            ),
            GQL.field("posts", GQL.list_of("Post"),
                GQL.arg("limit", GQL.Int),
                GQL.arg("offset", GQL.Int)
            )
        ),

        GQL.mutation(
            GQL.field("createUser", "User",
                GQL.arg("email", GQL.String, non_null(true)),
                GQL.arg("password", GQL.String, non_null(true))
            ),
            GQL.field("createPost", "Post",
                GQL.arg("title", GQL.String, non_null(true)),
                GQL.arg("content", GQL.String),
                GQL.arg("author_id", GQL.ID, non_null(true))
            )
        )
    )
End Process

Let SCHEMA be define_schema()
```

---

## GraphQL SDL Comparison

**Before (schema.graphql):**
```graphql
type User {
  id: ID!
  email: String!
  posts: [Post!]!
  created_at: String
}

type Post {
  id: ID!
  title: String!
  content: String
  author: User!
  published_at: String
}

type Query {
  users: [User!]!
  user(id: ID!): User
  posts(limit: Int, offset: Int): [Post!]!
}

type Mutation {
  createUser(email: String!, password: String!): User!
  createPost(title: String!, content: String, author_id: ID!): Post!
}
```

**After (graphql_schema.runa):**
```runa
Note: Equivalent Runa schema (shown above)
```

---

## Resolvers

```runa
Process called "define_resolvers" returns GQL.Resolvers:
    Return GQL.resolvers(
        GQL.query_resolver("users", resolve_all_users),
        GQL.query_resolver("user", resolve_user_by_id),
        GQL.mutation_resolver("createUser", create_user),
        GQL.field_resolver("User", "posts", resolve_user_posts)
    )
End Process

Process called "resolve_all_users" returns List[User]:
    Let users be DB.query("User").all()
    Return users
End Process

Process called "resolve_user_by_id" that takes id as Integer returns User:
    Let user be DB.query("User").where("id", id).first()
    Return user
End Process

Process called "resolve_user_posts" that takes user as User returns List[Post]:
    Let posts be DB.query("Post").where("author_id", user.id).all()
    Return posts
End Process

Process called "create_user" that takes email as String, password as String returns User:
    Let user be DB.insert("User", a dictionary containing:
        "email" as email,
        "password_hash" as hash_password(password)
    End Dictionary)
    Return user
End Process
```

---

## Subscriptions

```runa
Process called "schema_with_subscriptions" returns GQL.Schema:
    Return GQL.schema(
        Note: ... types and queries ...

        GQL.subscription(
            GQL.field("post_created", "Post"),
            GQL.field("user_updated", "User",
                GQL.arg("id", GQL.ID, non_null(true))
            )
        )
    )
End Process

Process called "define_subscription_resolvers" returns GQL.Resolvers:
    Return GQL.resolvers(
        GQL.subscription_resolver("post_created", subscribe_post_created),
        GQL.subscription_resolver("user_updated", subscribe_user_updated)
    )
End Process

Process called "subscribe_post_created" returns GQL.Subscription:
    Return GQL.pubsub_subscribe("POST_CREATED")
End Process
```

---

## Input Types

```runa
Process called "schema_with_inputs" returns GQL.Schema:
    Return GQL.schema(
        GQL.input_type("CreateUserInput",
            GQL.field("email", GQL.String, non_null(true)),
            GQL.field("password", GQL.String, non_null(true)),
            GQL.field("name", GQL.String)
        ),

        GQL.mutation(
            GQL.field("createUser", "User",
                GQL.arg("input", "CreateUserInput", non_null(true))
            )
        )
    )
End Process
```

---

## Directives

```runa
Process called "schema_with_directives" returns GQL.Schema:
    Return GQL.schema(
        GQL.directive("auth",
            GQL.arg("requires", GQL.String)
        ),

        GQL.type("User",
            GQL.field("id", GQL.ID),
            GQL.field("email", GQL.String,
                GQL.apply_directive("auth", "USER")
            ),
            GQL.field("admin_notes", GQL.String,
                GQL.apply_directive("auth", "ADMIN")
            )
        )
    )
End Process
```

---

## Summary

**Runa replaces GraphQL SDL with:**
- ✅ Type-safe schema definitions
- ✅ Integrated resolvers
- ✅ Executable specifications
- ✅ Built-in validation

**Stop using:** .graphql SDL files
**Start using:** `graphql_schema.runa`


---

# Web Markup

## Subtable of Contents

1. [Overview](#overview-6)
2. [Basic Web Page](#basic-web-page)
3. [HTML Comparison](#html-comparison)
4. [Dynamic Content](#dynamic-content)
5. [Forms](#forms)
6. [Component System](#component-system)
7. [JSX Comparison](#jsx-comparison)
8. [State Management](#state-management)
9. [Summary](#summary-6)

---

## Overview

**Runa replaces HTML with executable `.runa` markup files.**

**Replaces:**
- ❌ HTML
- ❌ JSX/TSX (React)
- ❌ Vue templates
- ❌ Svelte components

---

## Basic Web Page

**File:** `index.runa`

```runa
Note: Web page markup in Runa (Aether Framework)
Note: Replaces HTML

Import "runa/aether" as Web

Process called "render_page" returns Web.Element:
    Return Web.html(
        Web.head(
            Web.title("My Application"),
            Web.meta("charset", "UTF-8"),
            Web.link("stylesheet", "styles.runa")
        ),
        Web.body(
            Web.header(
                Web.h1("Welcome to My App")
            ),
            Web.main(
                Web.section(
                    Web.p("This is a paragraph"),
                    Web.button("Click Me", on_click)
                )
            ),
            Web.footer(
                Web.p("© 2025 My Company")
            )
        )
    )
End Process

Process called "on_click":
    Call Web.alert("Button clicked!")
End Process

Process called "main":
    Let page be render_page()
    Call Web.render(page, "root")
End Process
```

---

## HTML Comparison

**Before (index.html):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Application</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Welcome to My App</h1>
    </header>
    <main>
        <section>
            <p>This is a paragraph</p>
            <button onclick="handleClick()">Click Me</button>
        </section>
    </main>
    <footer>
        <p>© 2025 My Company</p>
    </footer>
</body>
</html>
```

**After (index.runa):**
```runa
Process called "render_page" returns Web.Element:
    Return Web.page(
        Web.header(Web.h1("Welcome to My App")),
        Web.main(
            Web.section(
                Web.p("This is a paragraph"),
                Web.button("Click Me", on_click)
            )
        ),
        Web.footer(Web.p("© 2025 My Company"))
    )
End Process
```

---

## Dynamic Content

```runa
Process called "render_user_list" that takes users as List[User] returns Web.Element:
    Let user_elements be an empty list

    For Each user in users:
        Let user_card be Web.div(
            Web.h3(user.name),
            Web.p("Email: " + user.email),
            Web.button("View Profile", view_profile(user.id))
        )
        Add user_card to user_elements
    End For

    Return Web.div(
        Web.h2("Users"),
        Web.div(user_elements)
    )
End Process
```

---

## Forms

```runa
Process called "render_login_form" returns Web.Element:
    Return Web.form(
        Web.input("text", "username", "Username"),
        Web.input("password", "password", "Password"),
        Web.button("Login", handle_login),
        on_submit(handle_login)
    )
End Process

Process called "handle_login":
    Let username be Web.get_value("username")
    Let password be Web.get_value("password")

    Call authenticate(username, password)
End Process
```

---

## Component System

```runa
Process called "Card" that takes title as String, content as String returns Web.Element:
    Return Web.div(
        Web.class("card"),
        Web.h3(title),
        Web.p(content)
    )
End Process

Process called "render_dashboard" returns Web.Element:
    Return Web.div(
        Card("Statistics", "100 users online"),
        Card("Activity", "50 new sign-ups today"),
        Card("Revenue", "$10,000 this month")
    )
End Process
```

---

## JSX Comparison

**Before (React JSX):**
```jsx
function UserProfile({ user }) {
  return (
    <div className="profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={() => editUser(user.id)}>Edit</button>
    </div>
  );
}
```

**After (Runa Aether):**
```runa
Process called "UserProfile" that takes user as User returns Web.Element:
    Return Web.div(
        Web.class("profile"),
        Web.h2(user.name),
        Web.p(user.email),
        Web.button("Edit", edit_user(user.id))
    )
End Process
```

---

## State Management

```runa
Type called "AppState":
    count as Integer
    user as User
    loading as Boolean
End Type

Process called "render_counter" that takes state as AppState returns Web.Element:
    Return Web.div(
        Web.h2("Count: " + string_from(state.count)),
        Web.button("Increment", increment),
        Web.button("Decrement", decrement)
    )
End Process

Process called "increment":
    Call Web.update_state(a dictionary containing:
        "count" as Web.get_state("count") + 1
    End Dictionary)
End Process
```

---

## Summary

**Runa replaces HTML/JSX with:**
- ✅ Type-safe markup
- ✅ Component functions
- ✅ Integrated state management
- ✅ No template strings

**Stop using:** HTML, JSX, Vue templates
**Start using:** Aether Framework (`.runa`)


---

# Web Styling

## Subtable of Contents

1. [Overview](#overview-7)
2. [Basic Styles](#basic-styles)
3. [CSS Comparison](#css-comparison)
4. [Computed Styles](#computed-styles)
5. [Responsive Design](#responsive-design)
6. [Component Styles](#component-styles)
7. [SCSS Comparison](#scss-comparison)
8. [Animations](#animations)
9. [Utility Functions](#utility-functions)
10. [Tailwind-Style Utilities](#tailwind-style-utilities)
11. [Summary](#summary-7)

---

## Overview

**Runa replaces CSS with executable `.runa` style files.**

**Replaces:**
- ❌ CSS
- ❌ SCSS/Sass
- ❌ Less
- ❌ Styled-components
- ❌ Tailwind CSS

---

## Basic Styles

**File:** `styles.runa`

```runa
Note: Web styling in Runa (Aether Framework)
Note: Replaces CSS/SCSS

Import "runa/aether/styles" as Style

Process called "define_styles" returns Style.Stylesheet:
    Return Style.stylesheet(
        Style.rule(".container", a dictionary containing:
            "max-width" as "1200px",
            "margin" as "0 auto",
            "padding" as "20px"
        End Dictionary),

        Style.rule(".button", a dictionary containing:
            "background-color" as "#007bff",
            "color" as "white",
            "padding" as "10px 20px",
            "border" as "none",
            "border-radius" as "4px",
            "cursor" as "pointer"
        End Dictionary),

        Style.rule(".button:hover", a dictionary containing:
            "background-color" as "#0056b3"
        End Dictionary)
    )
End Process

Let STYLES be define_styles()
```

---

## CSS Comparison

**Before (styles.css):**
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
```

**After (styles.runa):**
```runa
Let styles be Style.create(
    rule(".container", props("max-width", "1200px", "margin", "0 auto", "padding", "20px")),
    rule(".button", props(
        "background-color", "#007bff",
        "color", "white",
        "padding", "10px 20px",
        "border-radius", "4px"
    )),
    rule(".button:hover", props("background-color", "#0056b3"))
)
```

---

## Computed Styles

```runa
Process called "theme_colors" that takes theme as String returns Dictionary[String, String]:
    Return match theme:
        When "light":
            a dictionary containing:
                "primary" as "#007bff",
                "background" as "#ffffff",
                "text" as "#000000"
            End Dictionary
        When "dark":
            a dictionary containing:
                "primary" as "#0056b3",
                "background" as "#1a1a1a",
                "text" as "#ffffff"
            End Dictionary
        Otherwise:
            theme_colors("light")
    End Match
End Process

Process called "create_themed_styles" that takes theme as String returns Style.Stylesheet:
    Let colors be theme_colors(theme)

    Return Style.stylesheet(
        Style.rule("body", a dictionary containing:
            "background-color" as colors at key "background",
            "color" as colors at key "text"
        End Dictionary),

        Style.rule(".button-primary", a dictionary containing:
            "background-color" as colors at key "primary"
        End Dictionary)
    )
End Process
```

---

## Responsive Design

```runa
Process called "responsive_styles" returns Style.Stylesheet:
    Return Style.stylesheet(
        Style.rule(".grid", a dictionary containing:
            "display" as "grid",
            "grid-template-columns" as "repeat(3, 1fr)",
            "gap" as "20px"
        End Dictionary),

        Style.media_query("max-width: 768px",
            Style.rule(".grid", a dictionary containing:
                "grid-template-columns" as "repeat(2, 1fr)"
            End Dictionary)
        ),

        Style.media_query("max-width: 480px",
            Style.rule(".grid", a dictionary containing:
                "grid-template-columns" as "1fr"
            End Dictionary)
        )
    )
End Process
```

---

## Component Styles

```runa
Process called "Button" that takes text as String, variant as String returns Web.Element:
    Let button_styles be match variant:
        When "primary":
            props("background-color", "#007bff", "color", "white")
        When "secondary":
            props("background-color", "#6c757d", "color", "white")
        When "danger":
            props("background-color", "#dc3545", "color", "white")
        Otherwise:
            props("background-color", "#e0e0e0", "color", "#000000")
    End Match

    Return Web.button(text, Style.inline(button_styles))
End Process
```

---

## SCSS Comparison

**Before (styles.scss):**
```scss
$primary-color: #007bff;
$padding-small: 10px;
$padding-large: 20px;

.button {
  background-color: $primary-color;
  padding: $padding-small $padding-large;

  &:hover {
    background-color: darken($primary-color, 10%);
  }

  &.large {
    padding: $padding-large * 1.5;
  }
}
```

**After (styles.runa):**
```runa
Constant PRIMARY_COLOR as String is "#007bff"
Constant PADDING_SMALL as Integer is 10
Constant PADDING_LARGE as Integer is 20

Process called "button_styles" returns Style.Stylesheet:
    Return Style.stylesheet(
        rule(".button", props(
            "background-color", PRIMARY_COLOR,
            "padding", string_from(PADDING_SMALL) + "px " + string_from(PADDING_LARGE) + "px"
        )),

        rule(".button:hover", props(
            "background-color", darken(PRIMARY_COLOR, 10)
        )),

        rule(".button.large", props(
            "padding", string_from(PADDING_LARGE * 3 / 2) + "px"
        ))
    )
End Process

Process called "darken" that takes color as String, percent as Integer returns String:
    Note: Color manipulation function
    Return Style.adjust_color(color, "darken", percent)
End Process
```

---

## Animations

```runa
Process called "define_animations" returns Style.Stylesheet:
    Return Style.stylesheet(
        Style.keyframes("fade-in", a list containing:
            keyframe(0, props("opacity", "0")),
            keyframe(100, props("opacity", "1"))
        End),

        Style.rule(".fade-in", a dictionary containing:
            "animation" as "fade-in 0.3s ease-in"
        End Dictionary)
    )
End Process

Process called "keyframe" that takes percent as Integer, properties as Dictionary[String, String] returns Dictionary[String, Any]:
    Return a dictionary containing:
        "offset" as percent,
        "properties" as properties
    End Dictionary
End Process
```

---

## Utility Functions

```runa
Process called "props" that takes pairs as Variadic[String] returns Dictionary[String, String]:
    Let result be an empty dictionary

    Let i be 0
    While i < length of pairs:
        Let key be pairs at index i
        Let value be pairs at index (i + 1)
        Set result at key key to value
        Set i to i + 2
    End While

    Return result
End Process

Process called "spacing" that takes size as Integer returns String:
    Return string_from(size * 4) + "px"
End Process

Process called "color_with_alpha" that takes hex as String, alpha as Float returns String:
    Return Style.hex_to_rgba(hex, alpha)
End Process
```

---

## Tailwind-Style Utilities

```runa
Process called "utility_classes" returns Style.Stylesheet:
    Return Style.stylesheet(
        rule(".flex", props("display", "flex")),
        rule(".flex-col", props("flex-direction", "column")),
        rule(".justify-center", props("justify-content", "center")),
        rule(".items-center", props("align-items", "center")),
        rule(".gap-1", props("gap", spacing(1))),
        rule(".gap-2", props("gap", spacing(2))),
        rule(".gap-4", props("gap", spacing(4))),
        rule(".p-1", props("padding", spacing(1))),
        rule(".p-2", props("padding", spacing(2))),
        rule(".m-1", props("margin", spacing(1))),
        rule(".m-2", props("margin", spacing(2)))
    )
End Process
```

---

## Summary

**Runa replaces CSS/SCSS with:**
- ✅ Type-safe styling
- ✅ Computed values
- ✅ Theme support
- ✅ Component-scoped styles
- ✅ No preprocessors needed

**Stop using:** CSS, SCSS, Tailwind
**Start using:** Aether Styling (`.runa`)


---

**Document Version:** 1.0
**Last Updated:** 2024-10-18
**Status:** Canonical
