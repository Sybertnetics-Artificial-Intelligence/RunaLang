# Runa Example Projects

This directory contains example projects written in Runa to demonstrate language features and real-world usage patterns.

## TodoApp.runa

A complete command-line Todo application that showcases most of Runa's advanced features:

### Features Demonstrated:

- **Enhanced Type System**
  - Custom types (TodoId, Priority, Status)
  - Union types (OR)
  - Optional types
  - Generic types (Result[T])
  - Structured types (Dictionary with fields)

- **Functional Programming**
  - Pure functions for data operations
  - Higher-order functions (Map, Filter)
  - Lambda expressions
  - Pipeline operator (|>)

- **Pattern Matching**
  - Destructuring lists and dictionaries
  - Pattern guards
  - Wildcard patterns (_)
  - Complex nested patterns

- **Asynchronous Programming**
  - Async/await syntax
  - File operations
  - Error handling in async code

### Running the Example:

```bash
# Run the Todo application
runa run --advanced TodoApp.runa

# Example usage:
# > add Buy groceries [priority:high] [tags:shopping,food]
# > add Read documentation [priority:medium] [tags:work,study]
# > list all
# > list high
# > list tag:shopping
# > complete <id>
# > list completed
```

## More Examples

Additional examples demonstrating specific Runa features will be added here, including:

- Web API Client
- Data Analysis Tool
- Simple Game
- Neural Network Definition

Stay tuned for these upcoming examples! 