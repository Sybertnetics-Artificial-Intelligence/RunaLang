# Runa Syntax Converter

A core feature of Runa is its **dual syntax methodology**. Runa code can be written in a highly verbose, readable **natural language syntax** or a more compact, symbol-driven **technical syntax**. Neither is "better" than the other; they are simply different views of the same underlying code. The Syntax Converter is the tool that enables seamless translation between these two forms.

-   **Developer Mode Source**: `runa/src/dev_tools/syntax_converter/developer_mode.runa`
-   **Viewer Mode Source**: `runa/src/dev_tools/syntax_converter/viewer_mode.runa`

### Philosophy: Code for Humans

The dual syntax approach allows developers to write code in the way that is most comfortable and readable for them and their team. A developer working on complex algorithms might prefer the conciseness of technical syntax, while another developer writing business logic might prefer the expressiveness of natural language.

The Syntax Converter ensures that these preferences don't create friction. A developer can convert a module to their preferred syntax for editing, and then convert it back to a team-standard form before committing.

### How to Use

The converter is exposed via the `runa syntax` command.

```shell
# Convert a file to technical syntax (Developer Mode)
runa syntax --mode=dev my_file.runa

# Convert a file to natural language syntax (Viewer Mode)
runa syntax --mode=viewer my_file.runa
```
By default, the command prints the converted code to the console. You can use the `--output <file>` flag to write to a file or `--in-place` to modify the original file.

---

### Developer Mode (Natural → Technical)

Developer mode is designed for developers who prefer a more traditional, symbol-heavy programming style. It converts natural language operators and keywords into their more compact, technical equivalents.

**Example Conversion**

**Before (Natural Language Syntax):**
```runa
Process "calculate total" with items as List<Number> returns Number:
    Let total be 0
    For each item in items:
        Set total to total plus item
    Return total

Let prices be [10, 20, 30]
Let my_total be calculate total with items as prices
If my_total is greater than 50:
    Console.print("That's expensive!")

```

**After (`runa syntax --mode=dev`):**
```runa
fn "calculate_total"(items: List<Number>): Number {
    total = 0
    for item in items {
        total = total + item
    }
    return total
}

prices = [10, 20, 30]
my_total = calculate_total(prices)
if my_total > 50 {
    Display "That's expensive!"
}
```

### Viewer Mode (Technical → Natural)

Viewer mode does the exact opposite. It's designed to make dense, technical code more accessible and readable, especially for those less familiar with symbolic programming conventions. It translates symbols and terse keywords back into their natural language counterparts.

**Example Conversion**

**Before (Technical Syntax):**
```runa
fn "greet"(name: String): String {
    return "Hello, " + name
}

let result = greet("Runa")
Console.print(result)
```

**After (`runa syntax --mode=viewer`):**
```runa
Process "greet" with name as String returns String:
    Return "Hello, " joined with name

Let result be greet with name as "Runa"
Console.print(result)
```
*Note: The converter will also apply canonicalization rules. For example, it converted `+` to the canonical `joined with` for string concatenation during the viewer mode conversion.*


