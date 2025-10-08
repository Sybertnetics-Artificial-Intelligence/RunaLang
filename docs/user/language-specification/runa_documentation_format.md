# Runa Documentation Format Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

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

**End of Document**
