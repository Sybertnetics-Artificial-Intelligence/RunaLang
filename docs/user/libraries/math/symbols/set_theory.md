# Set Theory Symbols

The Set Theory module provides comprehensive support for set theory notation, including set operations, relations, cardinality symbols, and advanced set-theoretic concepts. This module is essential for mathematical logic, foundations of mathematics, and abstract algebra applications.

## Quick Start

```runa
Import "math/symbols/set_theory" as Sets

Note: Basic set theory symbols
Let element_of be Sets.get_membership_symbol("element_of")        Note: ∈
Let not_element be Sets.get_membership_symbol("not_element_of")   Note: ∉
Let union_symbol be Sets.get_operation_symbol("union")            Note: ∪
Let intersection_symbol be Sets.get_operation_symbol("intersection")  Note: ∩

Display "Membership: a " joined with element_of joined with " A, b " joined with not_element joined with " A"
Display "Operations: A " joined with union_symbol joined with " B, A " joined with intersection_symbol joined with " B"

Note: Create set expressions
Let set_expression be Sets.create_set_expression("A ∪ (B ∩ C)")
Let membership_statement be Sets.create_membership_statement("x", "ℝ")

Display "Set expression: " joined with set_expression
Display "Membership: " joined with membership_statement

Note: Standard number sets
Let natural_numbers be Sets.get_number_set("naturals")           Note: ℕ
Let real_numbers be Sets.get_number_set("reals")                 Note: ℝ
Let complex_numbers be Sets.get_number_set("complex")            Note: ℂ

Display "Number sets: " joined with natural_numbers joined with " ⊂ " joined with real_numbers joined with " ⊂ " joined with complex_numbers
```

## Basic Set Operations

### Membership and Inclusion

```runa
Import "math/symbols/set_theory" as SetSymbols

Note: Membership symbols
Let element_of be SetSymbols.get_element_of_symbol()             Note: ∈
Let not_element_of be SetSymbols.get_not_element_of_symbol()     Note: ∉
Let contains_symbol be SetSymbols.get_contains_symbol()          Note: ∋
Let not_contains be SetSymbols.get_not_contains_symbol()         Note: ∌

Display "Element relationships:"
Display "x " joined with element_of joined with " A means x is in A"
Display "x " joined not_element_of joined with " A means x is not in A"
Display "A " joined with contains_symbol joined with " x means A contains x"

Note: Subset and superset relations
Let subset_symbol be SetSymbols.get_subset_symbol()             Note: ⊆
Let proper_subset be SetSymbols.get_proper_subset_symbol()      Note: ⊂
Let superset_symbol be SetSymbols.get_superset_symbol()         Note: ⊇
Let proper_superset be SetSymbols.get_proper_superset_symbol()  Note: ⊃

Display "Subset relations:"
Display "A " joined with subset_symbol joined with " B (A is subset of B)"
Display "A " joined with proper_subset joined with " B (A is proper subset of B)"
Display "B " joined with superset_symbol joined with " A (B is superset of A)"
```

### Set Operations

```runa
Note: Basic set operations
Let union_symbol be SetSymbols.get_union_symbol()               Note: ∪
Let intersection_symbol be SetSymbols.get_intersection_symbol() Note: ∩
Let difference_symbol be SetSymbols.get_difference_symbol()     Note: ∖ or \
Let complement_symbol be SetSymbols.get_complement_symbol()     Note: ᶜ or '

Display "Basic operations:"
Display "Union: A " joined with union_symbol joined with " B"
Display "Intersection: A " joined with intersection_symbol joined with " B"
Display "Difference: A " joined with difference_symbol joined with " B"
Display "Complement: A" joined with complement_symbol

Note: Advanced set operations
Let symmetric_difference be SetSymbols.get_symmetric_difference_symbol()  Note: △ or ⊕
Let cartesian_product be SetSymbols.get_cartesian_product_symbol()        Note: ×
Let disjoint_union be SetSymbols.get_disjoint_union_symbol()              Note: ⊎

Display "Advanced operations:"
Display "Symmetric difference: A " joined with symmetric_difference joined with " B"
Display "Cartesian product: A " joined with cartesian_product joined with " B"
Display "Disjoint union: A " joined with disjoint_union joined with " B"
```

### Set Construction

```runa
Note: Set builder notation
Let set_builder_example be SetSymbols.format_set_builder(
    "x", "ℝ", "x² < 4"
)  Note: {x ∈ ℝ | x² < 4}

Let interval_notation be SetSymbols.format_interval("a", "b", "closed")  Note: [a,b]
Let open_interval be SetSymbols.format_interval("0", "1", "open")        Note: (0,1)
Let half_open_interval be SetSymbols.format_interval("0", "1", "half_open_right")  Note: (0,1]

Display "Set builder: " joined with set_builder_example
Display "Closed interval: " joined with interval_notation
Display "Open interval: " joined with open_interval
Display "Half-open interval: " joined with half_open_interval

Note: Special sets
Let empty_set be SetSymbols.get_empty_set_symbol()              Note: ∅
Let universal_set be SetSymbols.get_universal_set_symbol()      Note: U or 𝕌
Let power_set be SetSymbols.format_power_set("A")               Note: P(A) or 2^A

Display "Special sets:"
Display "Empty set: " joined with empty_set
Display "Universal set: " joined with universal_set
Display "Power set of A: " joined with power_set
```

## Number Sets and Algebraic Structures

### Standard Number Sets

```runa
Note: Common number sets
Let naturals be SetSymbols.get_natural_numbers()               Note: ℕ
Let integers be SetSymbols.get_integers()                      Note: ℤ
Let rationals be SetSymbols.get_rational_numbers()             Note: ℚ
Let reals be SetSymbols.get_real_numbers()                     Note: ℝ
Let complex_numbers be SetSymbols.get_complex_numbers()        Note: ℂ

Display "Number hierarchy:"
Display naturals joined with " ⊂ " joined with integers joined with " ⊂ " joined with rationals
Display rationals joined with " ⊂ " joined with reals joined with " ⊂ " joined with complex_numbers

Note: Number set variants
Let positive_naturals be SetSymbols.get_positive_naturals()    Note: ℕ₊ or ℕ*
Let nonzero_integers be SetSymbols.get_nonzero_integers()      Note: ℤ*
Let positive_reals be SetSymbols.get_positive_reals()          Note: ℝ₊
Let negative_reals be SetSymbols.get_negative_reals()          Note: ℝ₋

Display "Number set variants:"
Display "Positive naturals: " joined with positive_naturals
Display "Nonzero integers: " joined with nonzero_integers
Display "Positive reals: " joined with positive_reals
```

### Algebraic Structures

```runa
Note: Algebraic structure notation
Let field_notation be SetSymbols.format_field("F")             Note: (F, +, ·)
Let group_notation be SetSymbols.format_group("G", "∘")        Note: (G, ∘)
Let ring_notation be SetSymbols.format_ring("R")               Note: (R, +, ·)
Let vector_space be SetSymbols.format_vector_space("V", "F")   Note: V over F

Display "Algebraic structures:"
Display "Field: " joined with field_notation
Display "Group: " joined with group_notation  
Display "Ring: " joined with ring_notation
Display "Vector space: " joined with vector_space

Note: Structure operations
Let group_operation be SetSymbols.get_binary_operation_symbol() Note: ∘
Let identity_element be SetSymbols.format_identity_element("e") Note: e or 1
Let inverse_element be SetSymbols.format_inverse_element("a")   Note: a⁻¹

Display "Group elements:"
Display "Operation: a " joined with group_operation joined with " b"
Display "Identity: " joined with identity_element
Display "Inverse: " joined with inverse_element
```

## Cardinality and Infinity

### Cardinality Symbols

```runa
Note: Cardinality notation
Let cardinality_symbol be SetSymbols.get_cardinality_symbol()  Note: |·| or #
Let finite_cardinality be SetSymbols.format_cardinality("A")   Note: |A|
Let infinite_cardinality be SetSymbols.format_infinite_cardinality("ℵ₀")

Display "Cardinality notation:"
Display "Finite set: " joined with finite_cardinality
Display "Infinite set: " joined with infinite_cardinality

Note: Cardinality comparisons
Let equipotent_symbol be SetSymbols.get_equipotent_symbol()    Note: ≈ or ~
Let cardinality_less be SetSymbols.get_cardinality_less_symbol()   Note: ≺
Let cardinality_leq be SetSymbols.get_cardinality_leq_symbol()     Note: ≼

Display "Cardinality relations:"
Display "Equipotent: |A| " joined with equipotent_symbol joined with " |B|"
Display "Smaller: |A| " joined with cardinality_less joined with " |B|"
Display "At most: |A| " joined with cardinality_leq joined with " |B|"
```

### Infinite Cardinals

```runa
Note: Transfinite cardinals
Let aleph_null be SetSymbols.get_aleph_null()                  Note: ℵ₀
Let aleph_one be SetSymbols.get_aleph_one()                    Note: ℵ₁
Let aleph_alpha be SetSymbols.format_aleph("α")                Note: ℵₐ
Let continuum be SetSymbols.get_continuum_cardinality()        Note: 𝔠 or 2^ℵ₀

Display "Infinite cardinals:"
Display "Countable infinity: " joined with aleph_null
Display "First uncountable: " joined with aleph_one  
Display "General aleph: " joined with aleph_alpha
Display "Continuum: " joined with continuum

Note: Ordinal numbers
Let omega_symbol be SetSymbols.get_omega_symbol()              Note: ω
Let omega_one be SetSymbols.get_omega_one()                    Note: ω₁
Let epsilon_naught be SetSymbols.get_epsilon_naught()          Note: ε₀

Display "Ordinals:"
Display "First infinite ordinal: " joined with omega_symbol
Display "First uncountable ordinal: " joined with omega_one
Display "First epsilon number: " joined with epsilon_naught
```

## Logic and Quantifiers

### Quantifier Symbols

```runa
Note: Logical quantifiers in set theory
Let universal_quantifier be SetSymbols.get_universal_quantifier()    Note: ∀
Let existential_quantifier be SetSymbols.get_existential_quantifier() Note: ∃
Let unique_existence be SetSymbols.get_unique_existence_quantifier()   Note: ∃!

Display "Quantifiers:"
Display "Universal: " joined with universal_quantifier joined with "x ∈ A, P(x)"
Display "Existential: " joined with existential_quantifier joined with "x ∈ A, P(x)"
Display "Unique existence: " joined with unique_existence joined with "x ∈ A, P(x)"

Note: Restricted quantifiers
Let bounded_universal be SetSymbols.format_bounded_quantifier("∀", "x", "A", "P(x)")
Let bounded_existential be SetSymbols.format_bounded_quantifier("∃", "y", "B", "Q(y)")

Display "Bounded quantifiers:"
Display "Bounded universal: " joined with bounded_universal
Display "Bounded existential: " joined with bounded_existential
```

### Logical Connectives in Set Theory

```runa
Note: Logical operations
Let logical_and be SetSymbols.get_logical_and()               Note: ∧
Let logical_or be SetSymbols.get_logical_or()                 Note: ∨
Let logical_not be SetSymbols.get_logical_not()               Note: ¬
Let implication be SetSymbols.get_implication()               Note: →
Let equivalence be SetSymbols.get_equivalence()               Note: ↔

Display "Logical connectives:"
Display "And: P " joined with logical_and joined with " Q"
Display "Or: P " joined with logical_or joined with " Q"
Display "Not: " joined with logical_not joined with "P"
Display "Implies: P " joined with implication joined with " Q"
Display "Equivalent: P " joined with equivalence joined with " Q"
```

## Relations and Functions

### Relation Symbols

```runa
Note: Relation notation
Let relation_symbol be SetSymbols.get_relation_symbol()       Note: R or ~
Let equivalence_relation be SetSymbols.get_equivalence_relation() Note: ≡
Let congruence_relation be SetSymbols.get_congruence_relation()   Note: ≡
Let similarity_relation be SetSymbols.get_similarity_relation()   Note: ∼

Display "Relations:"
Display "General relation: aRb or a " joined with relation_symbol joined with " b"
Display "Equivalence: a " joined with equivalence_relation joined with " b"
Display "Congruence: a " joined with congruence_relation joined with " b (mod n)"
Display "Similarity: a " joined with similarity_relation joined with " b"

Note: Relation properties
Let reflexive_symbol be SetSymbols.format_reflexive_property("R")
Let symmetric_symbol be SetSymbols.format_symmetric_property("R")
Let transitive_symbol be SetSymbols.format_transitive_property("R")

Display "Relation properties:"
Display "Reflexive: " joined with reflexive_symbol
Display "Symmetric: " joined with symmetric_symbol
Display "Transitive: " joined with transitive_symbol
```

### Function Notation

```runa
Note: Function symbols
Let function_arrow be SetSymbols.get_function_arrow()         Note: →
Let partial_function be SetSymbols.get_partial_function_arrow() Note: ⇀
Let injection_arrow be SetSymbols.get_injection_arrow()       Note: ↣
Let surjection_arrow be SetSymbols.get_surjection_arrow()     Note: ↠
Let bijection_arrow be SetSymbols.get_bijection_arrow()       Note: ↔

Display "Function types:"
Display "Function: f: A " joined with function_arrow joined with " B"
Display "Partial: f: A " joined with partial_function joined with " B"
Display "Injection: f: A " joined with injection_arrow joined with " B"
Display "Surjection: f: A " joined with surjection_arrow joined with " B"
Display "Bijection: f: A " joined with bijection_arrow joined with " B"

Note: Function operations
Let composition_symbol be SetSymbols.get_composition_symbol() Note: ∘
Let restriction_symbol be SetSymbols.get_restriction_symbol() Note: ↾
Let inverse_function be SetSymbols.format_inverse_function("f") Note: f⁻¹

Display "Function operations:"
Display "Composition: (g " joined with composition_symbol joined with " f)(x)"
Display "Restriction: f " joined with restriction_symbol joined with " A"
Display "Inverse: " joined with inverse_function
```

## Topology and Analysis

### Topological Symbols

```runa
Note: Topology notation
Let interior_symbol be SetSymbols.get_interior_symbol()       Note: ° or int
Let closure_symbol be SetSymbols.get_closure_symbol()         Note: ̄ or cl
Let boundary_symbol be SetSymbols.get_boundary_symbol()       Note: ∂ or bd
Let complement_symbol be SetSymbols.get_topological_complement() Note: ᶜ

Display "Topological operations:"
Display "Interior: A" joined with interior_symbol
Display "Closure: A" joined with closure_symbol  
Display "Boundary: " joined with boundary_symbol joined with "A"
Display "Complement: A" joined with complement_symbol

Note: Neighborhood notation
Let neighborhood_symbol be SetSymbols.get_neighborhood_symbol()   Note: N or U
Let open_ball = SetSymbols.format_open_ball("x", "r")             Note: B(x,r)
Let closed_ball = SetSymbols.format_closed_ball("x", "r")         Note: B̄(x,r)

Display "Neighborhoods:"
Display "Neighborhood: " joined with neighborhood_symbol joined with "(x)"
Display "Open ball: " joined with open_ball
Display "Closed ball: " joined with closed_ball
```

### Convergence and Limits

```runa
Note: Convergence notation in set contexts
Let convergence_arrow be SetSymbols.get_convergence_arrow()   Note: →
Let limit_point_symbol be SetSymbols.get_limit_point_symbol() Note: '
Let accumulation_point be SetSymbols.get_accumulation_point() Note: ω

Display "Convergence notation:"
Display "Sequence convergence: xₙ " joined with convergence_arrow joined with " x"
Display "Limit points: A" joined with limit_point_symbol
Display "Accumulation point: " joined with accumulation_point joined with " ∈ A"

Note: Set limits
Let limsup_set be SetSymbols.format_limsup_set("Aₙ")         Note: lim sup Aₙ
Let liminf_set be SetSymbols.format_liminf_set("Aₙ")         Note: lim inf Aₙ

Display "Set limits:"
Display "Limit superior: " joined with limsup_set
Display "Limit inferior: " joined with liminf_set
```

## Advanced Set Theory

### Axiom Systems

```runa
Note: Axiomatic set theory symbols
Let axiom_of_choice be SetSymbols.get_axiom_of_choice_symbol() Note: AC
Let zfc_symbol be SetSymbols.get_zfc_symbol()                  Note: ZFC
Let continuum_hypothesis be SetSymbols.get_continuum_hypothesis() Note: CH

Display "Axiomatic systems:"
Display "Axiom of Choice: " joined with axiom_of_choice
Display "ZFC: " joined with zfc_symbol
Display "Continuum Hypothesis: " joined with continuum_hypothesis

Note: Independence results
Let independence_symbol be SetSymbols.get_independence_symbol() Note: ⊥
Let consistency_symbol be SetSymbols.get_consistency_symbol()   Note: Con

Display "Metalogical symbols:"
Display "Independence: CH " joined with independence_symbol joined with " ZFC"
Display "Consistency: " joined with consistency_symbol joined with "(ZFC)"
```

### Category Theory Interface

```runa
Note: Category-theoretic concepts in set theory
Let category_symbol be SetSymbols.get_category_symbol()       Note: Set
Let functor_arrow be SetSymbols.get_functor_arrow()           Note: ⟶
Let natural_transformation be SetSymbols.get_natural_transformation() Note: ⟹

Display "Category theory:"
Display "Category of sets: " joined with category_symbol
Display "Functor: F: C " joined with functor_arrow joined with " D"
Display "Natural transformation: α: F " joined with natural_transformation joined with " G"

Note: Topos theory
Let topos_symbol be SetSymbols.get_topos_symbol()             Note: ℰ
Let subobject_classifier be SetSymbols.get_subobject_classifier() Note: Ω

Display "Topos theory:"
Display "Topos: " joined with topos_symbol
Display "Subobject classifier: " joined with subobject_classifier
```

## Set Expression Validation

### Syntax Validation

```runa
Import "core/error_handling" as ErrorHandling

Note: Validate set-theoretic expressions
Let expressions_to_validate be [
    "A ∪ B ∩ C",                    Note: Valid (with precedence)
    "∀x ∈ A, P(x)",                 Note: Valid
    "{x ∈ ℝ | x² < 4}",             Note: Valid set builder
    "A ∪ ∩ B",                      Note: Invalid - malformed
    "∀x, P(x)",                     Note: Missing domain
    "{x | x² < 4}"                  Note: Missing domain specification
]

For Each expression in expressions_to_validate:
    Let validation_result be SetSymbols.validate_set_expression(expression)
    
    If ErrorHandling.is_valid(validation_result):
        Display expression joined with " ✓ Valid"
    Otherwise:
        Display expression joined with " ✗ Invalid"
        Let errors be ErrorHandling.get_validation_errors(validation_result)
        For Each error in errors:
            Display "  Error: " joined with ErrorHandling.error_message(error)
            Display "  Suggestion: " joined with SetSymbols.suggest_correction(error)
```

### Semantic Validation

```runa
Note: Check logical consistency
Let set_statements be [
    "A ⊂ B ∧ B ⊂ A",               Note: Should imply A = B
    "x ∈ ∅",                       Note: Always false
    "|A ∪ B| = |A| + |B|"          Note: Only true if A ∩ B = ∅
]

For Each statement in set_statements:
    Let semantic_check be SetSymbols.check_semantic_validity(statement)
    Let consistency_result be SetSymbols.analyze_logical_consistency(semantic_check)
    
    If SetSymbols.is_always_true(consistency_result):
        Display statement joined with " - Always true"
    Otherwise If SetSymbols.is_always_false(consistency_result):
        Display statement joined with " - Always false"
    Otherwise If SetSymbols.is_conditional(consistency_result):
        Let conditions be SetSymbols.get_truth_conditions(consistency_result)
        Display statement joined with " - True when: " joined with conditions
```

## Formatting and Display

### Mathematical Typesetting

```runa
Note: Format set theory expressions
Let complex_set_expression be "{x ∈ ℝ | ∃y ∈ ℕ: x = √y ∧ y > 100}"
Let formatted_expression be SetSymbols.format_for_display(complex_set_expression)

Display "Formatted expression: " joined with formatted_expression

Note: Multi-format output
Let latex_output be SetSymbols.convert_to_latex(complex_set_expression)
Let mathml_output be SetSymbols.convert_to_mathml(complex_set_expression)
Let ascii_output be SetSymbols.convert_to_ascii(complex_set_expression)

Display "LaTeX: " joined with latex_output
Display "MathML: " joined with mathml_output
Display "ASCII: " joined with ascii_output
```

### Accessibility Support

```runa
Note: Generate accessible descriptions
Let set_formula be "A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)"
Let screen_reader_text be SetSymbols.generate_screen_reader_text(set_formula)
Let speech_text be SetSymbols.generate_speech_text(set_formula)

Display "Screen reader: " joined with screen_reader_text
Display "Speech: " joined with speech_text

Note: Braille mathematical notation
Let braille_output be SetSymbols.convert_to_braille_math(set_formula)
Display "Braille: " joined with braille_output
```

## Integration Examples

### With Logic Systems

```runa
Import "math/logic/formal" as Logic

Note: Integrate with formal logic
Let set_theoretic_axiom be "∀x (x ∈ A ∪ B ↔ (x ∈ A ∨ x ∈ B))"
Let logical_formula be Logic.parse_formula(set_theoretic_axiom)
Let set_symbols = SetSymbols.extract_set_symbols(logical_formula)

Display "Set symbols in formula: " joined with SetSymbols.symbols_to_string(set_symbols)
```

### With Number Theory

```runa
Import "math/discrete/number_theory" as NumberTheory

Note: Use set notation with number theory
Let prime_set_notation be SetSymbols.format_set_builder(
    "p", NumberTheory.get_natural_numbers(), "is_prime(p)"
)
Display "Set of primes: " joined with prime_set_notation
```

## Performance and Optimization

### Symbol Lookup Optimization

```runa
Note: Optimize set symbol operations
SetSymbols.enable_symbol_caching(True)
SetSymbols.preload_common_set_symbols()

Let performance_test be SetSymbols.benchmark_symbol_operations(1000)
Let average_time be SetSymbols.get_average_operation_time(performance_test)

Display "Average symbol operation time: " joined with average_time joined with "μs"
```

### Expression Parsing Optimization

```runa
Note: Optimize complex expression parsing
Let complex_expressions be [
    "{x ∈ ℝ | ∀ε > 0, ∃δ > 0: |x - a| < δ → |f(x) - f(a)| < ε}",
    "⋃ᵢ₌₁^∞ (Aᵢ ∩ Bᵢᶜ)",
    "𝒫(A) ∩ {X ⊆ A | |X| = n}"
]

Let parsing_benchmark be SetSymbols.benchmark_expression_parsing(complex_expressions)
Let optimization_results be SetSymbols.apply_parsing_optimizations(parsing_benchmark)

Display "Parsing optimization speedup: " joined with 
    SetSymbols.get_speedup_factor(optimization_results) joined with "x"
```

## Best Practices

### Mathematical Rigor
- Use precise set-theoretic notation to avoid ambiguity
- Specify domains clearly in quantified statements
- Follow standard conventions for set notation
- Validate logical consistency of set-theoretic statements

### Symbol Selection
- Use internationally recognized set theory symbols
- Prefer standard Unicode mathematical symbols
- Consider context when choosing between notation variants
- Ensure symbols are accessible across platforms

### Educational Applications
- Provide clear explanations of set theory concepts
- Use progressive complexity in mathematical expressions
- Include visual representations where helpful
- Support multiple learning styles with varied notation

This module provides comprehensive set theory symbol support, enabling precise mathematical communication in foundations of mathematics, logic, and abstract algebra applications.