# LaTeX Mathematical Notation

The LaTeX module (`math/symbolic/latex`) provides comprehensive LaTeX mathematical notation export and formatting systems for symbolic expressions. This module enables conversion of symbolic mathematical expressions to properly formatted LaTeX code, document generation, and integration with mathematical typesetting systems.

## Overview

The LaTeX module offers extensive mathematical notation capabilities including:

- **Expression Formatting**: Convert symbolic expressions to LaTeX with proper mathematical formatting
- **Document Generation**: Create complete LaTeX documents for mathematical content
- **Symbol Mapping**: Comprehensive Unicode and mathematical symbol conversion
- **Equation Environments**: Generate appropriate LaTeX equation environments
- **Custom Formatting**: Configurable formatting options and style customization
- **Bidirectional Conversion**: Parse LaTeX expressions back to symbolic form
- **Integration Support**: Integration with mathematical publishing workflows

## Core Data Structures

### LaTeX Expression Representation

```runa
Type called "LaTeXExpression":
    latex_code as String                      # Generated LaTeX code
    expression_type as String                 # inline, display, align, etc.
    formatting_options as Dictionary[String, String]  # Formatting preferences
    required_packages as List[String]         # LaTeX packages needed
    custom_commands as Dictionary[String, String]     # User-defined commands
    display_mode as String                    # inline, block, equation
```

### LaTeX Document Structure

```runa
Type called "LaTeXDocument":
    document_class as String                  # article, book, amsart, etc.
    preamble as String                       # Document preamble
    document_body as String                  # Main document content
    required_packages as List[String]        # All required packages
    custom_definitions as Dictionary[String, String]  # Custom definitions
    bibliography as String                   # Bibliography section
```

## Basic Expression Conversion

### Simple Expression Formatting

```runa
Import "math/symbolic/latex" as LaTeX

Note: Convert basic expressions to LaTeX
Let simple_expr = "x^2 + 2*x + 1"
Let latex_simple = LaTeX.expression_to_latex(simple_expr)

Display "Expression: " joined with simple_expr
Display "LaTeX: " joined with latex_simple.latex_code

Note: Inline vs display mode
Let inline_math = LaTeX.expression_to_latex(simple_expr, Dictionary with: "mode": "inline")
Let display_math = LaTeX.expression_to_latex(simple_expr, Dictionary with: "mode": "display")

Display "Inline: $" joined with inline_math.latex_code joined with "$"
Display "Display: $$" joined with display_math.latex_code joined with "$$"

Note: Fractions and complex expressions
Let complex_expr = "(x^2 + 1)/(x - 1)"
Let latex_fraction = LaTeX.expression_to_latex(complex_expr, Dictionary with:
    "fraction_style": "displaystyle"
    "parentheses": "auto"
})

Display "Fraction LaTeX: " joined with latex_fraction.latex_code
```

### Mathematical Functions

```runa
Note: Trigonometric functions
Let trig_expr = "sin(x) + cos(y) + tan(z)"
Let latex_trig = LaTeX.expression_to_latex(trig_expr)
Display "Trig functions: " joined with latex_trig.latex_code

Note: Logarithms and exponentials
Let log_expr = "log(x) + ln(y) + exp(z)"
Let latex_log = LaTeX.expression_to_latex(log_expr, Dictionary with:
    "log_base": "explicit"  Note: Show base when specified
})
Display "Log/exp functions: " joined with latex_log.latex_code

Note: Special functions
Let special_expr = "Γ(x) + Β(a,b) + J_ν(z)"
Let latex_special = LaTeX.expression_to_latex(special_expr, Dictionary with:
    "unicode_symbols": "true"
    "function_names": "upright"
})
Display "Special functions: " joined with latex_special.latex_code
```

### Subscripts and Superscripts

```runa
Note: Complex subscripts and superscripts
Let subscript_expr = "x_{i,j}^{(k)} + a_n^{(m+1)}"
Let latex_subscript = LaTeX.expression_to_latex(subscript_expr, Dictionary with:
    "subscript_style": "text"
    "superscript_grouping": "auto"
})
Display "Subscripts/superscripts: " joined with latex_subscript.latex_code

Note: Multi-level indices
Let multilevel = "x_{i_1, i_2}^{j_1^{(k)}}"
Let latex_multilevel = LaTeX.expression_to_latex(multilevel, Dictionary with:
    "nested_indices": "clear"
    "index_spacing": "medium"
})
Display "Multi-level indices: " joined with latex_multilevel.latex_code
```

## Advanced Mathematical Notation

### Matrix and Vector Formatting

```runa
Note: Matrix representation
Let matrix_expr = "[[a, b], [c, d]]"
Let latex_matrix = LaTeX.matrix_to_latex(matrix_expr, Dictionary with:
    "matrix_type": "pmatrix"  Note: parentheses around matrix
    "alignment": "center"
})
Display "Matrix LaTeX: " joined with latex_matrix.latex_code

Note: Different matrix environments
Let matrix_types = ["matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix"]
For Each matrix_type in matrix_types:
    Let formatted_matrix = LaTeX.matrix_to_latex(matrix_expr, Dictionary with:
        "matrix_type": matrix_type
    })
    Display matrix_type joined with ": " joined with formatted_matrix.latex_code

Note: Vectors
Let vector_expr = "[x_1, x_2, x_3]"
Let latex_vector = LaTeX.vector_to_latex(vector_expr, Dictionary with:
    "vector_style": "column"
    "bracket_type": "pmatrix"
})
Display "Vector LaTeX: " joined with latex_vector.latex_code
```

### Calculus Notation

```runa
Note: Derivatives
Let derivative_expr = "d/dx[f(x)]"
Let latex_derivative = LaTeX.derivative_to_latex(derivative_expr, Dictionary with:
    "derivative_style": "leibniz"  Note: d/dx notation
})
Display "Derivative: " joined with latex_derivative.latex_code

Note: Partial derivatives
Let partial_expr = "∂²f/∂x∂y"
Let latex_partial = LaTeX.partial_derivative_to_latex(partial_expr, Dictionary with:
    "partial_style": "standard"
    "mixed_partials": "clear"
})
Display "Partial derivative: " joined with latex_partial.latex_code

Note: Integrals
Let integral_expr = "∫₀^∞ e^(-x²) dx"
Let latex_integral = LaTeX.integral_to_latex(integral_expr, Dictionary with:
    "integral_style": "displaystyle"
    "limits_placement": "traditional"
})
Display "Integral: " joined with latex_integral.latex_code

Note: Multiple integrals
Let multiple_integral = "∫∫∫_V f(x,y,z) dx dy dz"
Let latex_multiple = LaTeX.multiple_integral_to_latex(multiple_integral, Dictionary with:
    "integral_spacing": "medium"
    "limits_style": "below"
})
Display "Triple integral: " joined with latex_multiple.latex_code
```

### Summations and Products

```runa
Note: Summation notation
Let summation_expr = "∑_{i=1}^n x_i"
Let latex_summation = LaTeX.summation_to_latex(summation_expr, Dictionary with:
    "limits_placement": "above_below"
    "index_style": "italic"
})
Display "Summation: " joined with latex_summation.latex_code

Note: Product notation
Let product_expr = "∏_{i=1}^n (1 + x_i)"
Let latex_product = LaTeX.product_to_latex(product_expr, Dictionary with:
    "limits_placement": "above_below"
})
Display "Product: " joined with latex_product.latex_code

Note: Complex summations
Let complex_sum = "∑_{i,j=1}^{n,m} a_{ij} x_i y_j"
Let latex_complex_sum = LaTeX.summation_to_latex(complex_sum, Dictionary with:
    "multi_index": "compact"
    "limits_alignment": "center"
})
Display "Complex summation: " joined with latex_complex_sum.latex_code
```

## Equation Environments

### Single Equations

```runa
Note: Equation environment
Let equation_expr = "E = mc^2"
Let latex_equation = LaTeX.create_equation_environment(equation_expr, Dictionary with:
    "environment": "equation"
    "label": "eq:mass_energy"
    "numbering": "true"
})

Display "Equation environment:"
Display latex_equation.latex_code

Note: Equation without numbering
Let unnumbered_eq = LaTeX.create_equation_environment(equation_expr, Dictionary with:
    "environment": "equation*"
    "numbering": "false"
})
Display "Unnumbered equation: " joined with unnumbered_eq.latex_code
```

### Multi-line Equations

```runa
Note: Align environment
Let multiline_equations = [
    "f(x) = x^2 + 2x + 1",
    "     = (x + 1)^2",
    "     = (x + 1)(x + 1)"
]

Let latex_align = LaTeX.create_align_environment(multiline_equations, Dictionary with:
    "alignment_points": ["=", "=", "="]
    "equation_spacing": "normal"
    "numbering": "individual"
})

Display "Align environment:"
Display latex_align.latex_code

Note: Split environment
Let split_equation = LaTeX.create_split_environment(multiline_equations, Dictionary with:
    "main_label": "eq:factorization"
    "split_alignment": "left"
})
Display "Split environment: " joined with split_equation.latex_code
```

### System of Equations

```runa
Note: System of equations using cases
Let system = [
    "x + y = 5",
    "x - y = 1"
]

Let latex_system = LaTeX.create_system_environment(system, Dictionary with:
    "system_type": "cases"
    "left_delimiter": "{"
    "right_delimiter": ""
})

Display "System of equations:"
Display latex_system.latex_code

Note: Matrix form of system
Let matrix_system = LaTeX.system_to_matrix_form(system, ["x", "y"])
Display "Matrix form: " joined with matrix_system.latex_code
```

## Symbol Handling and Unicode

### Greek Letters

```runa
Note: Greek letter conversion
Let greek_expr = "α + β + γ + Δ + Σ + Ω"
Let latex_greek = LaTeX.expression_to_latex(greek_expr, Dictionary with:
    "greek_style": "italics"
    "capital_greek": "upright"
})
Display "Greek letters: " joined with latex_greek.latex_code

Note: Mathematical constants with Greek letters
Let constants_expr = "π ≈ 3.14159, e ≈ 2.71828, φ = (1+√5)/2"
Let latex_constants = LaTeX.expression_to_latex(constants_expr)
Display "Mathematical constants: " joined with latex_constants.latex_code
```

### Special Symbols

```runa
Note: Logical and set theory symbols
Let logic_expr = "∀x ∈ ℝ, ∃y ∈ ℕ : x ≤ y ∧ (P(x) ⟹ Q(y))"
Let latex_logic = LaTeX.expression_to_latex(logic_expr, Dictionary with:
    "symbol_font": "amsmath"
    "quantifier_spacing": "medium"
})
Display "Logic symbols: " joined with latex_logic.latex_code

Note: Arrows and relations
Let arrows_expr = "f: X → Y, x ↦ f(x), A ⊆ B ⟺ A ∩ B = A"
Let latex_arrows = LaTeX.expression_to_latex(arrows_expr, Dictionary with:
    "arrow_style": "long"
    "relation_spacing": "thick"
})
Display "Arrows and relations: " joined with latex_arrows.latex_code
```

### Custom Symbol Definitions

```runa
Note: Define custom LaTeX commands
Let custom_symbols = LaTeX.define_custom_symbols(Dictionary with:
    "R": "\\mathbb{R}"
    "C": "\\mathbb{C}"
    "Z": "\\mathbb{Z}"
    "N": "\\mathbb{N}"
    "Q": "\\mathbb{Q}"
})

Let expr_with_custom = "f: ℝ → ℂ is analytic"
Let latex_with_custom = LaTeX.expression_to_latex(expr_with_custom, Dictionary with:
    "custom_symbols": custom_symbols
    "use_custom_commands": "true"
})

Display "With custom symbols: " joined with latex_with_custom.latex_code
Display "Required commands: " joined with StringOps.join(latex_with_custom.custom_commands, ", ")
```

## Document Generation

### Complete LaTeX Documents

```runa
Note: Generate complete mathematical document
Let document_content = [
    "Let f(x) = x² + 2x + 1 be a quadratic function.",
    "We can factor this as f(x) = (x+1)².",
    "The derivative is f'(x) = 2x + 2 = 2(x+1)."
]

Let latex_document = LaTeX.create_mathematical_document(
    "Quadratic Functions",
    document_content,
    Dictionary with:
        "document_class": "amsart"
        "author": "Mathematical Analysis"
        "packages": ["amsmath", "amssymb", "amsthm"]
        "theorem_environments": "true"
)

Display "Complete LaTeX document:"
Display latex_document.latex_code
```

### Beamer Presentations

```runa
Note: Create presentation slides
Let slide_content = [
    Dictionary with:
        "title": "Taylor Series"
        "content": ["f(x) = ∑_{n=0}^∞ \\frac{f^{(n)}(a)}{n!}(x-a)^n"]
        "frame_options": ["fragile"],
    Dictionary with:
        "title": "Examples"
        "content": [
            "e^x = ∑_{n=0}^∞ \\frac{x^n}{n!}",
            "sin(x) = ∑_{n=0}^∞ \\frac{(-1)^n x^{2n+1}}{(2n+1)!}"
        ]
]

Let beamer_presentation = LaTeX.create_beamer_presentation(
    "Calculus Review",
    slide_content,
    Dictionary with:
        "theme": "Madrid"
        "color_theme": "whale"
        "math_packages": "true"
)

Display "Beamer presentation created with " joined with String(Length(slide_content)) joined with " slides"
```

### Article Templates

```runa
Note: Generate research article template
Let article_structure = Dictionary with:
    "title": "On the Convergence of Power Series"
    "authors": ["Dr. A. Mathematician", "Prof. B. Analyst"]
    "abstract": "This paper investigates convergence properties..."
    "keywords": ["power series", "convergence", "radius"]
    "sections": [
        Dictionary with: "title": "Introduction", "label": "sec:intro",
        Dictionary with: "title": "Main Results", "label": "sec:main",
        Dictionary with: "title": "Conclusions", "label": "sec:conclusions"
    ]

Let research_article = LaTeX.create_research_article_template(article_structure, Dictionary with:
    "journal_style": "ams"
    "bibliography_style": "amsalpha"
    "theorem_numbering": "section"
})

Display "Research article template generated"
Display "Required packages: " joined with StringOps.join(research_article.required_packages, ", ")
```

## Formatting Options and Customization

### Style Customization

```runa
Note: Create custom formatting style
Let custom_style = LaTeX.create_formatting_style(Dictionary with:
    "function_names": Dictionary with:
        "font": "mathrm"
        "spacing": "thin"
    ]
    "fractions": Dictionary with:
        "style": "displaystyle"
        "line_thickness": "medium"
    ]
    "matrices": Dictionary with:
        "bracket_type": "square"
        "row_spacing": "normal"
        "column_spacing": "medium"
    ]
    "integrals": Dictionary with:
        "symbol_size": "large"
        "limits_placement": "beside"
    ]
})

Let styled_expr = "∫₀¹ sin(πx)/x dx + [[1,2],[3,4]]"
Let custom_formatted = LaTeX.apply_custom_style(styled_expr, custom_style)
Display "Custom styled: " joined with custom_formatted.latex_code
```

### Package Management

```runa
Note: Manage LaTeX package dependencies
Let package_manager = LaTeX.create_package_manager()
LaTeX.add_required_package(package_manager, "amsmath", Dictionary with: "options": ["intlimits"])
LaTeX.add_required_package(package_manager, "tikz", Dictionary with: "libraries": ["matrix", "arrows"])

Let package_list = LaTeX.generate_package_list(package_manager)
Display "Package declarations:"
For Each package_line in package_list:
    Display "\\usepackage" joined with package_line

Note: Check package compatibility
Let compatibility_check = LaTeX.check_package_compatibility(package_manager)
If not compatibility_check.compatible:
    Display "Package conflicts detected:"
    For Each conflict in compatibility_check.conflicts:
        Display "  " joined with conflict.description
```

## Bidirectional Conversion

### LaTeX to Symbolic

```runa
Note: Parse LaTeX back to symbolic expressions
Let latex_input = "\\frac{x^2 + 1}{x - 1} + \\sin(\\alpha)"
Let parsed_expr = LaTeX.parse_latex_to_symbolic(latex_input)

Display "LaTeX input: " joined with latex_input
Display "Parsed symbolic: " joined with parsed_expr.symbolic_expression
Display "Parse tree: " joined with parsed_expr.parse_tree

Note: Handle complex LaTeX structures
Let complex_latex = "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} \\begin{pmatrix} x \\\\ y \\end{pmatrix}"
Let parsed_matrix = LaTeX.parse_matrix_expression(complex_latex)

Display "Matrix expression parsed:"
Display "Operation: " joined with parsed_matrix.operation_type
Display "Operands: " joined with StringOps.join(parsed_matrix.operands, " × ")
```

### Validation and Error Correction

```runa
Note: Validate LaTeX syntax
Let invalid_latex = "\\frac{x^2 + 1{x - 1}"  Note: Missing closing brace
Let validation_result = LaTeX.validate_latex_syntax(invalid_latex)

If not validation_result.valid:
    Display "LaTeX syntax errors found:"
    For Each error in validation_result.errors:
        Display "  Line " joined with String(error.line) joined with ": " joined with error.message
        Display "  Suggested fix: " joined with error.suggestion
        
    Let corrected_latex = LaTeX.auto_correct_syntax(invalid_latex)
    Display "Auto-corrected: " joined with corrected_latex.corrected_code
```

## Advanced Features

### TikZ Integration

```runa
Note: Generate TikZ diagrams
Let function_plot = LaTeX.create_tikz_plot(
    "sin(x)",
    Dictionary with:
        "x_range": "[-2*pi, 2*pi]"
        "y_range": "[-1.5, 1.5]"
        "samples": "100"
        "grid": "true"
        "axes_labels": Dictionary with: "x": "x", "y": "f(x)"
)

Display "TikZ plot code:"
Display function_plot.tikz_code

Note: Mathematical diagrams
Let commutative_diagram = LaTeX.create_commutative_diagram([
    Dictionary with: "objects": ["A", "B", "C", "D"], "arrows": [
        Dictionary with: "from": "A", "to": "B", "label": "f",
        Dictionary with: "from": "A", "to": "C", "label": "g",
        Dictionary with: "from": "B", "to": "D", "label": "h",
        Dictionary with: "from": "C", "to": "D", "label": "k"
    ]
])

Display "Commutative diagram: " joined with commutative_diagram.tikz_code
```

### Bibliography Integration

```runa
Note: Mathematical bibliography
Let bibliography_entries = [
    Dictionary with:
        "key": "rudin1976"
        "type": "book"
        "author": "Walter Rudin"
        "title": "Principles of Mathematical Analysis"
        "publisher": "McGraw-Hill"
        "year": "1976"
    ],
    Dictionary with:
        "key": "spivak1965"
        "type": "book"
        "author": "Michael Spivak"
        "title": "Calculus on Manifolds"
        "publisher": "W. A. Benjamin"
        "year": "1965"
]

Let bibliography = LaTeX.create_mathematical_bibliography(bibliography_entries, Dictionary with:
    "style": "amsalpha"
    "sort_order": "alphabetical"
})

Display "Bibliography generated with " joined with String(Length(bibliography_entries)) joined with " entries"

Note: Citation integration
Let text_with_citations = "As shown in \\cite{rudin1976}, the convergence of..."
Let citation_check = LaTeX.validate_citations(text_with_citations, bibliography_entries)
Display "Citations valid: " joined with String(citation_check.all_valid)
```

## Performance and Optimization

### Efficient LaTeX Generation

```runa
Note: Optimize LaTeX generation for large expressions
Let optimization_settings = Dictionary with:
    "cache_symbols": "true"
    "minimize_packages": "true"
    "compress_whitespace": "true"
    "reuse_definitions": "true"

LaTeX.configure_optimization(optimization_settings)

Note: Batch processing
Let expression_batch = [
    "x^2 + y^2 = r^2",
    "∫₀^∞ e^(-x²) dx = √π/2",
    "∑_{n=1}^∞ 1/n² = π²/6",
    "lim_{x→0} sin(x)/x = 1"
]

Let batch_result = LaTeX.batch_convert_expressions(expression_batch, Dictionary with:
    "shared_preamble": "true"
    "common_packages": "deduplicate"
})

Display "Batch converted " joined with String(Length(expression_batch)) joined with " expressions"
Display "Shared packages: " joined with StringOps.join(batch_result.common_packages, ", ")
```

## Error Handling

### LaTeX Generation Errors

```runa
Try:
    Let problematic_expr = "√(-1)"  Note: May need special handling
    Let latex_complex = LaTeX.expression_to_latex(problematic_expr, Dictionary with:
        "complex_numbers": "rectangular"
        "sqrt_style": "radical"
    })
    
    Display "Complex number LaTeX: " joined with latex_complex.latex_code
    
Catch Errors.LaTeXFormattingError as format_error:
    Display "LaTeX formatting error: " joined with format_error.message
    Display "Expression: " joined with format_error.problematic_expression
    Display "Suggested alternative: " joined with format_error.alternative_format

Catch Errors.UnicodeConversionError as unicode_error:
    Display "Unicode conversion error: " joined with unicode_error.message
    Display "Unsupported character: " joined with unicode_error.character
    Display "Suggested LaTeX command: " joined with unicode_error.latex_equivalent
```

### Package Dependency Issues

```runa
Note: Handle missing package dependencies
Let package_check = LaTeX.check_package_availability([
    "amsmath", "amssymb", "tikz", "pgfplots", "custom_package"
])

For Each package, available in package_check:
    If not available:
        Display "Package not available: " joined with package
        Let alternatives = LaTeX.suggest_package_alternatives(package)
        If Length(alternatives) > 0:
            Display "  Alternatives: " joined with StringOps.join(alternatives, ", ")
```

## Integration with Publishing Systems

### Journal Templates

```runa
Note: Adapt to specific journal requirements
Let journal_styles = LaTeX.get_available_journal_styles()
Display "Available journal styles: " joined with StringOps.join(journal_styles, ", ")

Let journal_document = LaTeX.create_journal_article(
    "Nature",
    Dictionary with:
        "title": "New Results in Mathematical Analysis"
        "authors": ["A. Researcher"]
        "content": "Mathematical content here..."
        "figures": []
        "tables": []
)

Display "Journal-specific formatting applied for Nature"
Display "Compliance check: " joined with String(journal_document.compliance_check.passes)
```

### Online Platform Integration

```runa
Note: Generate MathJax-compatible output
Let mathjax_output = LaTeX.convert_for_mathjax("E = mc^2", Dictionary with:
    "mathjax_version": "3.0"
    "delimiters": "dollar"
    "extensions": ["ams"]
})

Display "MathJax format: " joined with mathjax_output.formatted_expression

Note: Generate for online platforms
Let platform_formats = LaTeX.convert_for_platforms("∫₀^∞ e^(-x²) dx = √π/2", [
    "stackoverflow", "arxiv", "overleaf", "mathjax"
])

For Each platform, formatted_code in platform_formats:
    Display platform joined with ": " joined with formatted_code
```

## Related Documentation

- **[Symbolic Core](core.md)**: Expression representation for LaTeX conversion
- **[Mathematical Symbols](../symbols/README.md)**: Unicode symbol mappings
- **[Symbolic Functions](functions.md)**: Special functions in LaTeX notation
- **[Symbolic Series](series.md)**: Series representations in LaTeX format
- **[Document Generation](../../../tools/documentation.md)**: Broader documentation tools

The LaTeX module provides comprehensive mathematical notation formatting capabilities, enabling seamless conversion from symbolic expressions to publication-ready LaTeX code. Its extensive customization options, document generation features, and integration capabilities make it essential for mathematical publishing and documentation workflows.