# Runa Examples

This directory contains example programs demonstrating various Runa language features.

## Basic Examples

- [`hello_world.runa`](basic/hello_world.runa) - Your first Runa program
- [`variables.runa`](basic/variables.runa) - Variable declaration and types
- [`calculator.runa`](basic/calculator.runa) - Basic arithmetic operations
- [`conditions.runa`](basic/conditions.runa) - If statements and comparisons
- [`loops.runa`](basic/loops.runa) - All types of loops

## Intermediate Examples

- [`functions.runa`](intermediate/functions.runa) - Function definition and calling
- [`lists_and_data.runa`](intermediate/lists_and_data.runa) - Working with collections
- [`pattern_matching.runa`](intermediate/pattern_matching.runa) - Pattern matching examples
- [`error_handling.runa`](intermediate/error_handling.runa) - Try/catch/finally
- [`type_system.runa`](intermediate/type_system.runa) - Advanced type features

## Advanced Examples

- [`modules.runa`](advanced/modules.runa) - Module system and imports
- [`async_programming.runa`](advanced/async_programming.runa) - Async/await
- [`concurrency.runa`](advanced/concurrency.runa) - Concurrent programming
- [`memory_management.runa`](advanced/memory_management.runa) - Memory annotations

## Real-World Projects

- [`todo_app/`](projects/todo_app/) - Complete todo list application
- [`web_scraper/`](projects/web_scraper/) - Web scraping utility
- [`data_processor/`](projects/data_processor/) - Data analysis tool
- [`api_client/`](projects/api_client/) - REST API client
- [`calculator_gui/`](projects/calculator_gui/) - GUI calculator

## Running Examples

Each example can be compiled and run:

```bash
# Compile to Python
python -m runa.cli compile examples/basic/hello_world.runa -t python

# Run the generated code
python hello_world.py
```

## Learning Path

1. Start with **Basic Examples** to learn syntax
2. Move to **Intermediate Examples** for language features
3. Try **Advanced Examples** for complex concepts
4. Build your own projects using **Real-World Projects** as templates