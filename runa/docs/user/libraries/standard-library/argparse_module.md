# ArgParse Module

The ArgParse module provides comprehensive command-line argument parsing and CLI utilities for Runa. It supports positional and optional arguments, subcommands, type conversion, validation, automatic help/usage generation, advanced error handling, and extensibility for interactive and AI-driven CLI scenarios.

## Overview

- **Positional and optional arguments** (types, defaults, required/optional)
- **Subcommands and command groups**
- **Type conversion and validation**
- **Automatic help/usage generation**
- **Error handling** (unknown args, missing required, type errors)
- **Config file/env var overrides**
- **Mutually exclusive groups, dependencies, argument file expansion, custom actions**
- **Extensible for AI/interactive CLI**

## Core Types

### ArgumentType
```runa
Type ArgumentType is:
    | STRING
    | INTEGER
    | FLOAT
    | BOOLEAN
    | FILE
    | DIRECTORY
    | CHOICE with choices as List[String]
    | CUSTOM with process as Process
```

### Argument
```runa
Type Argument is Dictionary with:
    name as String
    type as ArgumentType
    required as Boolean defaults to false
    default as Any
    help as String
    positional as Boolean defaults to false
    multiple as Boolean defaults to false
    choices as List[Any]
    env_var as Optional[String]
    config_key as Optional[String]
    mutually_exclusive_group as Optional[String]
    depends_on as List[String]
    action as Optional[Process]
    validator as Optional[Process]
    metavar as Optional[String]
    hidden as Boolean defaults to false
```

### Subcommand
```runa
Type Subcommand is Dictionary with:
    name as String
    help as String
    arguments as List[Argument]
    handler as Process
    subcommands as List[Subcommand]
    parent as Optional[Subcommand]
    hidden as Boolean defaults to false
```

### ArgParseResult
```runa
Type ArgParseResult is:
    | ParseSuccess with values as Dictionary[String, Any] and command as Optional[String]
    | ParseError with message as String and code as String
```

### ArgumentParser
```runa
Type ArgumentParser is Dictionary with:
    program_name as String
    description as String
    arguments as List[Argument]
    subcommands as List[Subcommand]
    options as ArgParseOptions
    version as Optional[String]
    epilog as Optional[String]
    usage as Optional[String]
    parent as Optional[ArgumentParser]
    metadata as Dictionary[String, Any]
```

## Basic Usage

### Creating a Parser
```runa
Let parser be create_parser with program_name as "myapp" and description as "Demo CLI"
```

### Adding Arguments
```runa
Let arg1 be Argument with:
    name as "input"
    type as STRING
    required as true
    help as "Input file path"
    positional as true

Let arg2 be Argument with:
    name as "--verbose"
    type as BOOLEAN
    default as false
    help as "Enable verbose output"

Let parser be add_argument with parser as parser and argument as arg1
Let parser be add_argument with parser as parser and argument as arg2
```

### Parsing Arguments
```runa
Let argv be list containing "data.txt", "--verbose"
Let result be parse_args with parser as parser and argv as argv

Match result:
    When ParseSuccess with values as args:
        Display "Input: " plus args["input"]
        Display "Verbose: " plus args["--verbose"]
    When ParseError with message as msg:
        Display "Error: " plus msg
```

### Automatic Help
```runa
Display generate_help with parser as parser
Display generate_usage with parser as parser
```

## Advanced Features

### Subcommands
```runa
Process called "handle_run" that takes args as Dictionary[String, Any] returns None:
    Display "Running with input: " plus args["input"]

Let run_cmd be Subcommand with:
    name as "run"
    help as "Run the main process"
    arguments as list containing Argument with:
        name as "input"
        type as STRING
        required as true
        help as "Input file"
        positional as true
    handler as handle_run
    subcommands as list containing
    parent as None
    hidden as false

Let parser be add_subcommand with parser as parser and subcommand as run_cmd
```

### Advanced Argument Parsing
```runa
Note: Parse arguments with complex options
Let options be ArgParseOptions with:
    allow_unknown as false
    strict_types as true
    auto_help as true
    ignore_case as false
    debug as false
    validate_dependencies as true
    expand_argument_files as true
    parse_environment_variables as true
    parse_config_files as true

Let parser be set_options with parser as parser and options as options
Let result be parse_args_with_options with parser as parser and argv as argv and options as options
```

### Nested Subcommands
```runa
Note: Create nested command structure: db -> migrate
Process called "handle_migrate" that takes args as Dictionary[String, Any] returns None:
    Display "Running database migration"

Let migrate_cmd be Subcommand with:
    name as "migrate"
    help as "Run database migrations"
    arguments as list containing
    handler as handle_migrate
    subcommands as list containing
    parent as None
    hidden as false

Let db_cmd be Subcommand with:
    name as "db"
    help as "Database operations"
    arguments as list containing
    handler as None
    subcommands as list containing migrate_cmd
    parent as None
    hidden as false

Let parser be add_subcommand with parser as parser and subcommand as db_cmd
```

### Plugin System
```runa
Note: Dynamic command registration for plugins
Process called "register_plugin_command" that takes parser as ArgumentParser and plugin_name as String returns ArgumentParser:
    Process called "handle_plugin" that takes args as Dictionary[String, Any] returns None:
        Display "Plugin " plus plugin_name plus " executed"
    
    Let plugin_cmd be Subcommand with:
        name as plugin_name
        help as "Plugin: " with message plugin_name
        arguments as list containing
        handler as handle_plugin
        subcommands as list containing
        parent as None
        hidden as false
    
    Return add_subcommand with parser as parser and subcommand as plugin_cmd

Let parser be register_plugin_command with parser as parser and plugin_name as "my-plugin"
```

### Type Conversion and Validation
```runa
Note: Basic type validation
Let arg be Argument with:
    name as "--count"
    type as INTEGER
    default as 1
    help as "Number of iterations"
    validator as Process called "validate_count" that takes value as Integer returns ValidationResult:
        If value is less than or equal to 0:
            Return ValidationError with message as "Count must be positive"
        If value is greater than 1000:
            Return ValidationError with message as "Count cannot exceed 1000"
        Return ValidationSuccess with value as value

Let parser be add_argument with parser as parser and argument as arg
```

### Advanced Validators
```runa
Note: File existence validator
Process called "file_exists_validator" that takes value as String returns ValidationResult:
    If file_exists with path as value:
        Return ValidationSuccess with value as value
    Otherwise:
        Return ValidationError with message as "File does not exist: " with message value

Note: Email validator
Process called "email_validator" that takes value as String returns ValidationResult:
    If value contains "@" and value contains ".":
        Return ValidationSuccess with value as value
    Otherwise:
        Return ValidationError with message as "Invalid email format"

Note: Range validator
Process called "range_validator" that takes min as Integer and max as Integer returns Process:
    Return Process called "validate_range" that takes value as Integer returns ValidationResult:
        If value is less than min:
            Return ValidationError with message as "Value must be at least " with message string from min
        If value is greater than max:
            Return ValidationError with message as "Value must be at most " with message string from max
        Return ValidationSuccess with value as value

Note: Using advanced validators
Let email_arg be Argument with:
    name as "--email"
    type as STRING
    validator as email_validator
    help as "Email address"

Let port_arg be Argument with:
    name as "--port"
    type as INTEGER
    validator as range_validator with min as 1 and max as 65535
    help as "Port number (1-65535)"

Let config_arg be Argument with:
    name as "--config"
    type as FILE
    validator as file_exists_validator
    help as "Configuration file"
```

### Mutually Exclusive Groups
```runa
Let arg_a be Argument with:
    name as "--foo"
    type as BOOLEAN
    mutually_exclusive_group as "group1"

Let arg_b be Argument with:
    name as "--bar"
    type as BOOLEAN
    mutually_exclusive_group as "group1"

Let parser be add_argument with parser as parser and argument as arg_a
Let parser be add_argument with parser as parser and argument as arg_b
```

### Argument Dependencies
```runa
Let arg_x be Argument with:
    name as "--x"
    type as STRING
    depends_on as list containing "--y"

Let parser be add_argument with parser as parser and argument as arg_x
```

### Argument File Expansion
```runa
Let argfile be Argument with:
    name as "--argfile"
    type as FILE
    action as Process called "expand_args" that takes value as String returns List[String]:
        Note: Read file and return list of arguments
        Return list containing

Let parser be add_argument with parser as parser and argument as argfile
```

### Config File and Env Var Overrides
```runa
Let arg_cfg be Argument with:
    name as "--config"
    type as FILE
    env_var as "MYAPP_CONFIG"
    config_key as "config_path"

Let parser be add_argument with parser as parser and argument as arg_cfg
```

## Error Handling

- Unknown arguments
- Missing required arguments
- Type conversion errors
- Mutually exclusive group violations
- Dependency violations
- Argument file errors
- Config/env var errors

## Usage Generation
```runa
Display generate_usage with parser as parser
```

## API Reference

- `create_parser(program_name: String, description: String) -> ArgumentParser`
- `add_argument(parser: ArgumentParser, argument: Argument) -> ArgumentParser`
- `add_subcommand(parser: ArgumentParser, subcommand: Subcommand) -> ArgumentParser`
- `set_version(parser: ArgumentParser, version: String) -> ArgumentParser`
- `set_epilog(parser: ArgumentParser, epilog: String) -> ArgumentParser`
- `set_usage(parser: ArgumentParser, usage: String) -> ArgumentParser`
- `set_options(parser: ArgumentParser, options: ArgParseOptions) -> ArgumentParser`
- `parse_args(parser: ArgumentParser, argv: List[String]) -> ArgParseResult`
- `generate_help(parser: ArgumentParser) -> String`
- `generate_usage(parser: ArgumentParser) -> String`

## Best Practices

- Use positional arguments for required inputs
- Use optional arguments for configuration and flags
- Validate argument values and handle errors gracefully
- Use subcommands for complex CLI tools
- Leverage config/env var overrides for flexible configuration
- Document all arguments and subcommands

This module provides all the functionality needed for robust, idiomatic, and AI-friendly command-line interfaces in Runa. 