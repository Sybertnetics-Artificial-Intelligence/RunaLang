# Text Module

The `text` module provides advanced text processing and formatting utilities for the Runa programming language. It includes text wrapping, formatting, analysis, and manipulation capabilities.

## Overview

The text module is designed to handle complex text processing tasks with a simple, intuitive API. It provides both high-level formatting functions and detailed text analysis capabilities.

## Classes

### TextWrapper

A class for wrapping and filling text with various formatting options.

```runa
let wrapper = TextWrapper(width: 40, initial_indent: "  ")
let wrapped_text = wrapper.wrap("This is a long text that should be wrapped to multiple lines.")
let filled_text = wrapper.fill("This is a long text that should be filled to a specific width.")
```

#### Constructor Parameters

- `width` (int, default: 70): Maximum line width
- `initial_indent` (str, default: ""): String to prepend to the first line
- `subsequent_indent` (str, default: ""): String to prepend to subsequent lines
- `expand_tabs` (bool, default: true): Whether to expand tabs to spaces
- `replace_whitespace` (bool, default: true): Whether to replace whitespace characters
- `fix_sentence_endings` (bool, default: false): Whether to fix sentence endings
- `break_long_words` (bool, default: true): Whether to break long words
- `break_on_hyphens` (bool, default: true): Whether to break on hyphens
- `tabsize` (int, default: 8): Tab size for tab expansion
- `drop_whitespace` (bool, default: true): Whether to drop whitespace

#### Methods

- `wrap(text: str) -> list`: Wrap text into a list of lines
- `fill(text: str) -> str`: Fill text into a single string

## Text Formatting Functions

### dedent(text: str) -> str

Remove common leading whitespace from every line in text.

```runa
let text = """
    This text has
    common indentation
    that should be removed.
"""
let result = dedent(text)
```

### indent(text: str, prefix: str, predicate: Optional[Callable] = None) -> str

Add prefix to the beginning of selected lines in text.

```runa
let text = "line1\nline2\nline3"
let result = indent(text, "  ")
```

### fill(text: str, width: int = 70, **kwargs) -> str

Fill a single paragraph of text.

```runa
let text = "This is a long text that should be filled to a specific width."
let result = fill(text, width: 20)
```

### shorten(text: str, width: int, **kwargs) -> str

Collapse and truncate text to fit in the given width.

```runa
let text = "This is a very long text that should be shortened."
let result = shorten(text, width: 30)
```

### wrap(text: str, width: int = 70, **kwargs) -> list

Wrap a single paragraph of text.

```runa
let text = "This is a long text that should be wrapped to multiple lines."
let result = wrap(text, width: 20)
```

## Text Utility Functions

### get_text_width(text: str) -> int

Get the display width of text (handles wide characters).

```runa
let width = get_text_width("Hello, 世界!")
```

### justify(text: str, width: int, justify_type: str = 'left') -> str

Justify text to a given width.

```runa
let text = "Hello world"
let left_justified = justify(text, 20, 'left')
let right_justified = justify(text, 20, 'right')
let centered = justify(text, 20, 'center')
let full_justified = justify(text, 20, 'justify')
```

### center(text: str, width: int, fillchar: str = ' ') -> str

Center text in a field of given width.

```runa
let result = center("Hello", 10)
```

### ljust(text: str, width: int, fillchar: str = ' ') -> str

Left-justify text in a field of given width.

```runa
let result = ljust("Hello", 10)
```

### rjust(text: str, width: int, fillchar: str = ' ') -> str

Right-justify text in a field of given width.

```runa
let result = rjust("Hello", 10)
```

## Text Analysis Functions

### word_count(text: str) -> int

Count the number of words in text.

```runa
let count = word_count("Hello world! This is a test.")
```

### char_count(text: str, include_spaces: bool = true) -> int

Count the number of characters in text.

```runa
let total_chars = char_count("Hello world")
let no_spaces = char_count("Hello world", include_spaces: false)
```

### line_count(text: str) -> int

Count the number of lines in text.

```runa
let lines = line_count("line1\nline2\nline3")
```

### sentence_count(text: str) -> int

Count the number of sentences in text.

```runa
let sentences = sentence_count("Hello. How are you? I'm fine!")
```

### paragraph_count(text: str) -> int

Count the number of paragraphs in text.

```runa
let paragraphs = paragraph_count("Para 1.\n\nPara 2.\n\nPara 3.")
```

### readability_score(text: str) -> float

Calculate a simple readability score (Flesch Reading Ease).

```runa
let score = readability_score("Hello world. This is simple.")
```

### text_statistics(text: str) -> dict

Get comprehensive text statistics.

```runa
let stats = text_statistics("Hello world. This is a test.")
// Returns: {
//   'characters': 25,
//   'characters_no_spaces': 20,
//   'words': 5,
//   'lines': 1,
//   'sentences': 2,
//   'paragraphs': 1,
//   'readability_score': 85.2,
//   'average_word_length': 4.0,
//   'average_sentence_length': 2.5
// }
```

## Examples

### Basic Text Wrapping

```runa
let wrapper = TextWrapper(width: 30)
let text = "This is a very long text that needs to be wrapped to multiple lines for better readability."
let wrapped = wrapper.wrap(text)
```

### Text Analysis

```runa
let document = """
This is a sample document. It contains multiple sentences.
The readability score will be calculated based on the complexity
of the text and the average sentence length.
"""

let stats = text_statistics(document)
let word_count = stats['words']
let readability = stats['readability_score']
```

### Text Formatting

```runa
let code_block = """
def hello():
    print("Hello, world!")
    return True
"""

let formatted = indent(dedent(code_block), "  ")
```

## Error Handling

The text module functions handle edge cases gracefully:

- Empty strings return appropriate default values
- Invalid parameters raise `ValueError`
- Unicode text is handled correctly
- Whitespace-only text is processed appropriately

## Performance Notes

- Text analysis functions are optimized for typical document sizes
- Large text processing may benefit from chunking
- Memory usage scales linearly with input size
- Readability calculations use efficient algorithms

## See Also

- [String Module](string_module.md) - Basic string operations
- [Collections Module](collections_module.md) - Text data structures
- [IO Module](io_module.md) - File text processing 

# Testing

A comprehensive Runa-based test file for the text module is located at:

    runa/tests/stdlib/test_text.runa

This file exercises the main features and edge cases of the text module using idiomatic Runa assertions and error handling. All standard library modules will have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability. 