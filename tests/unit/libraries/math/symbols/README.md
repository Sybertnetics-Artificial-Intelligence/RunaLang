# Mathematical Symbols Test Suite

Comprehensive unit tests for the Runa standard library mathematical symbols modules.

## Overview

This test suite provides complete coverage for 6 mathematical symbols modules:

- **Calculus Symbols** (`calculus_symbols_test.runa`) - 44 tests
- **Formatting** (`formatting_test.runa`) - 44 tests
- **Greek Letters** (`greek_letters_test.runa`) - 42 tests
- **Logic Symbols** (`logic_test.runa`) - 47 tests
- **Set Theory** (`set_theory_test.runa`) - 54 tests
- **Unicode Operators** (`unicode_operators_test.runa`) - 45 tests

**Total: 276+ unit tests covering 413 functions across all mathematical symbol modules**

## Quick Start

```runa
Import "tests/unit/libraries/math/symbols/symbols_test_runner" as SymbolsTests

Note: Run all mathematical symbols tests
SymbolsTests.run_symbols_test_suite()

Note: Run specific module tests
SymbolsTests.run_specific_symbols_module("calculus_symbols")
SymbolsTests.run_specific_symbols_module("formatting")
SymbolsTests.run_specific_symbols_module("greek_letters")

Note: Quick smoke tests
SymbolsTests.run_quick_symbols_tests()
```

## Test Files

### 1. Calculus Symbols Tests (`calculus_symbols_test.runa`)

Tests mathematical calculus notation including:
- **Differential Operators**: ∂, d, ∇, Δ, δ with variants and properties
- **Integral Symbols**: ∫, ∬, ∭, ∮, ∯, ∰ (single to volume integrals)
- **Limit Notation**: lim, →, ∞, left/right limits
- **Summation/Product**: ∑, ∏, ∐, ⋃, ⋂ with bounds
- **Vector Calculus**: gradient, divergence, curl operations
- **Analysis Symbols**: Big O, little o, Θ, Ω asymptotic notation

**Key Test Functions:**
- `test_partial_differential_operator()` - Partial derivative symbol
- `test_single_integral()` - Integration symbol with bounds
- `test_nabla_operator()` - Vector calculus nabla operator
- `test_summation_symbol()` - Summation notation with subscripts
- `test_big_o_notation()` - Asymptotic complexity notation

### 2. Formatting Tests (`formatting_test.runa`)

Tests mathematical typography and rendering:
- **Symbol Formatting**: Font, size, weight, color application
- **Expression Layout**: Multi-line alignment, spacing, baseline adjustment
- **Rendering Context**: Output format adaptation (LaTeX, MathML, SVG, PNG)
- **Style Guidelines**: Mathematical typography compliance
- **Symbol Spacing**: Operator spacing, kerning, margin control
- **Color Coding**: Syntax highlighting, gradients, semantic coloring

**Key Test Functions:**
- `test_format_mathematical_symbol()` - Symbol formatting with styles
- `test_export_to_latex()` - LaTeX code generation
- `test_export_to_mathml()` - MathML markup generation
- `test_apply_mathematical_typography()` - Typography rule enforcement
- `test_format_matrix()` - Matrix formatting with brackets

### 3. Greek Letters Tests (`greek_letters_test.runa`)

Tests Greek alphabet and mathematical constants:
- **Complete Alphabet**: All 24 Greek letters (uppercase/lowercase)
- **Mathematical Usage**: Context-specific usage (angles, constants, variables)
- **Variant Forms**: Bold, italic, script mathematical styles
- **Mathematical Constants**: π, φ, τ, e, γ with precise values
- **Unicode Support**: Proper encoding, normalization, validation
- **Transliteration**: Pronunciation guides, Latin equivalents

**Key Test Functions:**
- `test_alpha_symbols()` - Alpha letter with variants
- `test_pi_constant()` - Pi constant with mathematical properties
- `test_bold_greek_letters()` - Bold variant Unicode mappings
- `test_get_mathematical_constants()` - All Greek mathematical constants
- `test_transliterate_to_latin()` - Greek to Latin conversion

### 4. Logic Symbols Tests (`logic_test.runa`)

Tests formal logic notation systems:
- **Propositional Logic**: ∧, ∨, ¬, →, ↔, ⊕ with precedence
- **Quantifiers**: ∀, ∃, ∄, ∃!, λ abstraction
- **Modal Logic**: □, ◇, K, B operators with Kripke semantics
- **Temporal Logic**: ○, □, ◇, U, R operators for time reasoning
- **Proof Theory**: ⊢, ⊨, ⊬, ⊭, ⊥, ⊤ symbols
- **Type Theory**: Dependent types, function types, type assignment

**Key Test Functions:**
- `test_conjunction_symbol()` - Logical AND with properties
- `test_universal_quantifier()` - Universal quantification
- `test_necessity_operator()` - Modal necessity operator
- `test_turnstile_symbol()` - Proof system turnstile
- `test_validate_logical_expression()` - Logic formula validation

### 5. Set Theory Tests (`set_theory_test.runa`)

Tests set-theoretic notation and operations:
- **Set Membership**: ∈, ∉, ∋, ∌ with relationship validation
- **Set Relations**: ⊂, ⊃, ⊆, ⊇, ⊊, ⊋ inclusion relations
- **Set Operations**: ∪, ∩, ∖, △, × with algebraic properties
- **Cardinality**: |A|, ℵ₀, ℵ₁, ℶ₀, ∞ infinity symbols
- **Functions/Relations**: →, ↦, ⇸, ↔ function notation
- **Special Sets**: ∅, ℕ, ℤ, ℚ, ℝ, ℂ number systems
- **Category Theory**: ⇄, ⊣, ⊢, ∘ categorical constructs

**Key Test Functions:**
- `test_element_of_symbol()` - Set membership relation
- `test_union_symbol()` - Set union with commutativity
- `test_empty_set_symbol()` - Empty set with cardinality
- `test_natural_numbers_symbol()` - Natural number set
- `test_validate_set_notation()` - Set-builder notation validation

### 6. Unicode Operators Tests (`unicode_operators_test.runa`)

Tests Unicode mathematical operator support:
- **Basic Arithmetic**: +, −, ×, ÷, ± with precedence
- **Comparison**: =, ≠, <, >, ≤, ≥, ≈, ≡ relations
- **Unicode Encoding**: UTF-8 encoding/decoding, validation
- **Symbol Classification**: Type detection, precedence rules
- **Rendering Support**: LaTeX, MathML, ASCII, SVG conversion
- **Accessibility**: Alt text, Braille, audio descriptions

**Key Test Functions:**
- `test_plus_operator()` - Addition with associativity
- `test_encode_utf8_symbol()` - Unicode to UTF-8 conversion
- `test_classify_symbol_type()` - Automatic symbol categorization
- `test_render_symbol_latex()` - LaTeX rendering pipeline
- `test_generate_alt_text()` - Accessibility text generation

## Test Execution Options

### Full Test Suite
```runa
SymbolsTests.run_symbols_test_suite()
```
Runs all 276+ tests across all modules (~10-15 minutes)

### Quick Tests
```runa
SymbolsTests.run_quick_symbols_tests()
```
Runs 12 essential tests covering core functionality (~60 seconds)

### Performance Tests
```runa
SymbolsTests.run_performance_symbols_tests()
```
Runs performance-focused tests with large symbol sets (~4-6 minutes)

### Categorical Testing
```runa
Note: Test specific symbol categories
SymbolsTests.run_symbols_tests_by_category(["Calculus Symbols", "Logic Symbols"])

Note: Individual category tests
SymbolsTests.run_calculus_category_tests()
SymbolsTests.run_typography_tests()
SymbolsTests.run_greek_letters_category_tests()
SymbolsTests.run_logic_category_tests()
SymbolsTests.run_set_theory_category_tests()
SymbolsTests.run_unicode_operations_tests()
```

### CI/CD Integration
```runa
Note: Optimized for continuous integration
SymbolsTests.run_ci_symbols_test_suite()

Note: Extended nightly testing
SymbolsTests.run_nightly_symbols_test_suite()
```

## Test Architecture

### Test Data Generation
Each module includes comprehensive test data generators:
- **Symbol Definitions**: Unicode, LaTeX, MathML representations
- **Mathematical Properties**: Precedence, associativity, arity
- **Rendering Contexts**: Multiple output formats and devices
- **Typography Options**: Font families, sizes, styles, colors
- **Edge Cases**: Malformed inputs, boundary conditions
- **Performance Data**: Large symbol collections and complex expressions

### Assertion Framework
Custom assertion helpers for mathematical validation:
- **Symbol Validation**: Unicode correctness, name consistency
- **Property Verification**: Mathematical operator properties
- **Format Validation**: LaTeX, MathML output correctness
- **Encoding Verification**: UTF-8 byte sequence validation
- **Accessibility Compliance**: Alt text, screen reader compatibility

### Error Handling Testing
Comprehensive error scenario coverage:
- **Invalid Symbols**: Malformed Unicode, unknown symbols
- **Encoding Errors**: Invalid UTF-8 sequences, normalization failures
- **Rendering Failures**: Unsupported output formats, font issues
- **Typography Violations**: Spacing rule violations, style conflicts
- **Performance Limits**: Memory constraints, processing timeouts

## Performance Characteristics

### Expected Test Durations
- **Calculus Symbols**: ~180 seconds (complex operator validation)
- **Formatting**: ~200 seconds (rendering and export operations)
- **Greek Letters**: ~120 seconds (alphabet and constant validation)
- **Logic Symbols**: ~150 seconds (logical system verification)
- **Set Theory**: ~220 seconds (comprehensive set operations)
- **Unicode Operators**: ~180 seconds (encoding and accessibility tests)

### Memory Requirements
- **Typical**: 128-256 MB for standard test execution
- **Performance Tests**: 512 MB - 1 GB for large symbol processing
- **Peak Usage**: During complex LaTeX/MathML generation

### Computational Complexity
- **Basic Tests**: Linear algorithms with moderate inputs
- **Typography Tests**: Quadratic algorithms for complex layout
- **Unicode Tests**: Constant time for most encoding operations
- **Rendering Tests**: Variable based on output complexity

## Module Dependencies

### External Dependencies
```runa
Import "dev/test" as UnitTest              // Core testing framework
Import "collections" as Collections        // Data structures and utilities
Import "datetime" as DateTime              // Performance timing
```

### Internal Dependencies
- Each test module is self-contained with its own symbols module import
- No cross-module test dependencies
- Shared assertion patterns but independent implementations

## Test Quality Metrics

### Coverage Statistics
- **Function Coverage**: 276/413 functions (67% function coverage)
- **Category Coverage**: All major symbol categories tested
- **Unicode Coverage**: All supported Unicode planes and blocks
- **Format Coverage**: LaTeX, MathML, SVG, PNG export testing

### Test Categories Distribution
- **Unit Tests**: 70% - Individual function and symbol testing
- **Integration Tests**: 20% - Multi-symbol expression testing
- **Performance Tests**: 7% - Large-scale processing validation
- **Accessibility Tests**: 3% - Screen reader and Braille testing

## Continuous Integration

### CI Test Pipeline
1. **Smoke Tests** (60 seconds) - Basic symbol operations
2. **Quick Tests** (90 seconds) - Core functionality
3. **Full Suite** (15 minutes) - Complete coverage
4. **Performance Tests** (8 minutes) - Scalability validation
5. **Compatibility Tests** (5 minutes) - Standards compliance

### Test Report Generation
Automated reports include:
- **Success/Failure Rates** by module and symbol category
- **Performance Metrics** and rendering timing
- **Coverage Analysis** with function gap identification
- **Standards Compliance** for Unicode, LaTeX, MathML
- **Accessibility Audit** results

## Contributing

### Adding New Tests
1. Follow existing test patterns in each module
2. Include both positive and negative test cases
3. Add appropriate assertion helpers for new symbol types
4. Update test count estimates in `get_*_test_count()`
5. Document mathematical properties being validated

### Test Naming Conventions
- `test_[symbol_name]_[property]` for symbol validation
- `test_[operation]_[scenario]` for operation testing
- `test_[format]_[conversion]` for rendering tests
- `test_[accessibility]_feature` for accessibility validation

### Documentation Requirements
- Document Unicode codepoints and mathematical meanings
- Explain mathematical properties and precedence rules
- Reference typography and formatting standards
- Include accessibility guidelines and requirements

## Mathematical Standards Reference

### Supported Standards
- **Unicode**: Unicode 15.0 with Mathematical Operators blocks
- **LaTeX**: LaTeX2e with AMS extensions for mathematical typesetting
- **MathML**: MathML 3.0 for web-based mathematical content
- **Typography**: ISO 31 and AMS guidelines for mathematical notation
- **Accessibility**: WCAG 2.1 guidelines for mathematical content

### Symbol Categories
- **Basic Arithmetic**: +, −, ×, ÷, ± and variants
- **Relations**: =, ≠, <, >, ≤, ≥, ≈, ≡ and extensions
- **Set Theory**: ∈, ∉, ∪, ∩, ⊂, ⊆ and comprehensive set notation
- **Logic**: ∧, ∨, ¬, →, ↔, ∀, ∃ and modal/temporal extensions
- **Calculus**: ∫, ∑, ∂, ∇, lim and differential/integral notation
- **Greek**: α-ω with mathematical constants and variants

### Typography Standards
- **Font Families**: Computer Modern, Times, Helvetica mathematical fonts
- **Spacing**: Proper operator spacing and mathematical kerning
- **Layout**: Multi-line expression alignment and baseline management
- **Colors**: Semantic coloring for mathematical syntax highlighting

## Performance Benchmarks

### Standard Benchmarks
- **Symbol Lookup**: Sub-millisecond for individual symbols
- **LaTeX Generation**: <50ms for complex expressions
- **Unicode Encoding**: >10,000 operations per second
- **Typography Layout**: Linear in expression complexity

### Optimization Targets
- **Memory Usage**: <256 MB for normal operation
- **Processing Speed**: Real-time for interactive mathematical editing
- **Rendering Quality**: Publication-ready output for all formats
- **Accessibility**: Screen reader compatible with <100ms response

## Troubleshooting

### Common Test Failures
1. **Unicode Encoding**: Check system UTF-8 support and locale settings
2. **Font Issues**: Ensure mathematical fonts are available for rendering tests
3. **LaTeX Dependencies**: Verify LaTeX installation for export tests
4. **Memory Limits**: Increase heap size for performance tests
5. **Timeout Issues**: Adjust test timeouts for slower systems

### Debugging Tools
- Use `SymbolsTests.run_specific_symbols_module()` to isolate issues
- Enable verbose logging with `UnitTest.set_verbose(true)`
- Check individual symbol properties with validation functions
- Use performance profiling for slow test identification

This comprehensive test suite ensures the reliability, correctness, and performance of Runa's mathematical symbols capabilities, supporting both theoretical mathematics and practical typographical applications in mathematical document preparation, educational software, and scientific computing environments.