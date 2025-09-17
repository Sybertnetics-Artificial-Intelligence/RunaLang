# Formal Logic Systems

The Formal Logic Systems module provides comprehensive implementations of mathematical logic systems, from basic propositional logic to advanced higher-order logic and type theory. This module forms the foundation for rigorous mathematical reasoning and formal verification.

## Quick Start

```runa
Import "math/logic/formal" as Formal

Note: Create and work with propositional logic
Let prop_system be Formal.create_propositional_system()
Let formula be Formal.construct_propositional_formula("(P ∧ Q) → R", ["P", "Q", "R"])

Note: Check satisfiability and tautology
Let is_satisfiable be Formal.check_satisfiability(formula)
Let is_tautology be Formal.check_tautology(formula)

Display "Formula is satisfiable: " joined with is_satisfiable
Display "Formula is tautology: " joined with is_tautology

Note: Generate truth table
Let truth_table be Formal.generate_truth_table(formula)
Formal.display_truth_table(truth_table)
```

## Propositional Logic

### Basic Formula Construction

```runa
Import "math/logic/formal" as Logic

Note: Create propositional formulas with different connectives
Let conjunction be Logic.construct_conjunction(["P", "Q", "R"])
Let disjunction be Logic.construct_disjunction(["P", "Q", "R"])
Let implication be Logic.construct_implication("P", "Q")
Let biconditional be Logic.construct_biconditional("P", "Q")
Let negation be Logic.construct_negation("P")

Display "Conjunction: " joined with Logic.formula_to_string(conjunction)
Display "Disjunction: " joined with Logic.formula_to_string(disjunction)
Display "Implication: " joined with Logic.formula_to_string(implication)
```

### Formula Analysis and Transformation

```runa
Note: Analyze formula structure
Let complex_formula be Logic.parse_formula("((P → Q) ∧ (Q → R)) → (P → R)")
Let variables be Logic.extract_variables(complex_formula)
Let connectives be Logic.identify_connectives(complex_formula)
Let depth be Logic.calculate_formula_depth(complex_formula)

Display "Variables: " joined with Logic.variables_to_string(variables)
Display "Formula depth: " joined with depth

Note: Convert to normal forms
Let cnf_form be Logic.convert_to_cnf(complex_formula)
Let dnf_form be Logic.convert_to_dnf(complex_formula)
Let nnf_form be Logic.convert_to_nnf(complex_formula)

Display "CNF: " joined with Logic.formula_to_string(cnf_form)
Display "DNF: " joined with Logic.formula_to_string(dnf_form)
Display "NNF: " joined with Logic.formula_to_string(nnf_form)
```

### Semantic Analysis

```runa
Note: Truth table generation and analysis
Let formula_set be [
    Logic.parse_formula("P → Q"),
    Logic.parse_formula("¬P ∨ Q"),
    Logic.parse_formula("¬(P ∧ ¬Q)")
]

Note: Check semantic equivalence
Let equivalence_matrix be Logic.check_pairwise_equivalence(formula_set)
Logic.display_equivalence_matrix(equivalence_matrix)

Note: Find satisfying assignments
Let satisfying_assignments be Logic.find_all_satisfying_assignments(complex_formula)
For Each assignment in satisfying_assignments:
    Display "Satisfying assignment: " joined with Logic.assignment_to_string(assignment)
```

### Boolean Satisfiability (SAT)

```runa
Note: SAT solving with different algorithms
Let sat_formula be Logic.parse_formula("(P ∨ Q ∨ R) ∧ (¬P ∨ Q) ∧ (P ∨ ¬Q ∨ ¬R)")

Note: DPLL algorithm
Let dpll_result be Logic.solve_dpll(sat_formula)
If Logic.is_satisfiable_result(dpll_result):
    Let model be Logic.get_satisfying_model(dpll_result)
    Display "DPLL found model: " joined with Logic.model_to_string(model)

Note: Modern SAT solver
Let cdcl_result be Logic.solve_cdcl(sat_formula)
Let solution_time be Logic.get_solving_time(cdcl_result)
Display "CDCL solving time: " joined with solution_time joined with "ms"
```

## Predicate Logic (First-Order Logic)

### Predicate Formula Construction

```runa
Note: Create first-order logic formulas
Let predicate_system be Logic.create_first_order_system()

Note: Define predicates and terms
Let human_predicate be Logic.define_unary_predicate("Human", "x")
Let mortal_predicate be Logic.define_unary_predicate("Mortal", "x") 
Let loves_predicate be Logic.define_binary_predicate("Loves", "x", "y")

Note: Construct quantified formulas
Let universal_formula be Logic.construct_universal(
    "x", 
    Logic.construct_implication(
        Logic.apply_predicate(human_predicate, "x"),
        Logic.apply_predicate(mortal_predicate, "x")
    )
)

Let existential_formula be Logic.construct_existential(
    "y",
    Logic.apply_predicate(loves_predicate, "john", "y")
)

Display "Universal: " joined with Logic.formula_to_string(universal_formula)
Display "Existential: " joined with Logic.formula_to_string(existential_formula)
```

### Model Theory

```runa
Note: Create and work with models
Let domain be Logic.create_domain(["socrates", "plato", "aristotle", "mary"])
Let model be Logic.create_model(domain)

Note: Define predicate interpretations
Logic.set_predicate_extension(model, "Human", ["socrates", "plato", "aristotle"])
Logic.set_predicate_extension(model, "Mortal", ["socrates", "mary"])
Logic.set_predicate_extension(model, "Loves", [
    ["john", "mary"],
    ["mary", "john"],
    ["socrates", "plato"]
])

Note: Evaluate formulas in model
Let formula_value be Logic.evaluate_in_model(universal_formula, model)
Display "Formula truth value in model: " joined with formula_value

Note: Check model satisfaction
Let satisfies_theory be Logic.model_satisfies_theory(model, [universal_formula, existential_formula])
Display "Model satisfies theory: " joined with satisfies_theory
```

### Unification and Substitution

```runa
Note: Unification algorithm
Let term1 be Logic.parse_term("loves(john, f(x))")
Let term2 be Logic.parse_term("loves(y, f(mary))")

Let unification_result be Logic.unify(term1, term2)
If Logic.unification_successful(unification_result):
    Let mgu be Logic.get_most_general_unifier(unification_result)
    Display "Most general unifier: " joined with Logic.substitution_to_string(mgu)
    
    Note: Apply substitution
    Let substituted_term be Logic.apply_substitution(term1, mgu)
    Display "After substitution: " joined with Logic.term_to_string(substituted_term)
```

### Skolemization and Prenex Normal Form

```runa
Note: Convert to prenex normal form
Let complex_predicate_formula be Logic.parse_formula(
    "∀x(Human(x) → ∃y(Loves(x,y) ∧ ∀z(Human(z) → Loves(z,mother(z)))))"
)

Let prenex_form be Logic.convert_to_prenex_normal_form(complex_predicate_formula)
Display "Prenex form: " joined with Logic.formula_to_string(prenex_form)

Note: Skolemization
Let skolemized be Logic.skolemize(prenex_form)
Display "Skolemized: " joined with Logic.formula_to_string(skolemized)

Note: Convert to clause form
Let clause_set be Logic.convert_to_clause_form(skolemized)
Logic.display_clause_set(clause_set)
```

## Modal Logic

### Basic Modal Systems

```runa
Note: Create modal logic systems
Let modal_system_k be Logic.create_modal_system("K")   Note: Basic modal logic
Let modal_system_t be Logic.create_modal_system("T")   Note: Reflexive
Let modal_system_s4 be Logic.create_modal_system("S4") Note: Reflexive and transitive
Let modal_system_s5 be Logic.create_modal_system("S5") Note: Equivalence relation

Note: Construct modal formulas
Let necessary_p be Logic.construct_necessity("P")
Let possible_q be Logic.construct_possibility("Q")
Let modal_formula be Logic.construct_implication(necessary_p, possible_q)

Display "Modal formula: " joined with Logic.modal_formula_to_string(modal_formula)
```

### Kripke Semantics

```runa
Note: Create Kripke model
Let possible_worlds be ["w1", "w2", "w3", "w4"]
Let kripke_model be Logic.create_kripke_model(possible_worlds)

Note: Define accessibility relation
Logic.add_accessibility(kripke_model, "w1", "w2")
Logic.add_accessibility(kripke_model, "w1", "w3")
Logic.add_accessibility(kripke_model, "w2", "w3")
Logic.add_accessibility(kripke_model, "w3", "w4")

Note: Set valuation at worlds
Logic.set_world_valuation(kripke_model, "w1", "P", True)
Logic.set_world_valuation(kripke_model, "w2", "P", False)
Logic.set_world_valuation(kripke_model, "w3", "Q", True)
Logic.set_world_valuation(kripke_model, "w4", "Q", False)

Note: Evaluate modal formulas
Let necessity_evaluation be Logic.evaluate_modal_at_world(necessary_p, kripke_model, "w1")
Let possibility_evaluation be Logic.evaluate_modal_at_world(possible_q, kripke_model, "w1")

Display "□P at w1: " joined with necessity_evaluation
Display "◊Q at w1: " joined with possibility_evaluation
```

### Modal Axioms and Validity

```runa
Note: Check validity of modal axioms
Let axiom_k be Logic.parse_modal_formula("□(P → Q) → (□P → □Q)")
Let axiom_t be Logic.parse_modal_formula("□P → P")
Let axiom_4 be Logic.parse_modal_formula("□P → □□P")
Let axiom_5 be Logic.parse_modal_formula("◊P → □◊P")

Let validity_k be Logic.check_modal_validity(axiom_k, modal_system_k)
Let validity_t be Logic.check_modal_validity(axiom_t, modal_system_t)

Display "Axiom K valid in system K: " joined with validity_k
Display "Axiom T valid in system T: " joined with validity_t

Note: Model checking modal properties
Let modal_property be Logic.parse_modal_formula("□(P → ◊Q)")
Let model_check_result be Logic.modal_model_check(kripke_model, modal_property)
```

## Temporal Logic

### Linear Temporal Logic (LTL)

```runa
Note: Create temporal logic system
Let ltl_system be Logic.create_ltl_system()

Note: Define temporal operators
Let always_p be Logic.construct_globally("P")      Note: G P (always P)
Let eventually_q be Logic.construct_finally("Q")   Note: F Q (eventually Q)
Let next_r be Logic.construct_next("R")           Note: X R (next R)
Let until_formula be Logic.construct_until("P", "Q") Note: P U Q (P until Q)

Note: Complex temporal formula
Let temporal_property be Logic.parse_ltl_formula("G(P → F Q)")  Note: If P then eventually Q
Display "LTL formula: " joined with Logic.ltl_formula_to_string(temporal_property)

Note: Create temporal model
Let temporal_trace be Logic.create_infinite_trace([
    Logic.create_state(["P"]),
    Logic.create_state(["P", "Q"]),
    Logic.create_state(["Q"]),
    Logic.create_state([])
])

Let ltl_satisfaction be Logic.check_ltl_satisfaction(temporal_property, temporal_trace)
Display "LTL property holds: " joined with ltl_satisfaction
```

### Computation Tree Logic (CTL)

```runa
Note: Branching time logic
Let ctl_system be Logic.create_ctl_system()

Note: CTL path quantifiers and temporal operators
Let for_all_eventually be Logic.construct_af("P")    Note: AF P
Let exists_globally be Logic.construct_eg("Q")       Note: EG Q
Let for_all_until be Logic.construct_au("P", "Q")    Note: A[P U Q]
Let exists_next be Logic.construct_ex("R")           Note: EX R

Note: Create branching model (Kripke structure)
Let transition_system be Logic.create_transition_system()
Logic.add_state(transition_system, "s0", True, ["P"])
Logic.add_state(transition_system, "s1", False, ["Q"])
Logic.add_state(transition_system, "s2", False, ["P", "Q"])
Logic.add_transition(transition_system, "s0", "s1")
Logic.add_transition(transition_system, "s0", "s2")
Logic.add_transition(transition_system, "s1", "s2")

Let ctl_formula be Logic.parse_ctl_formula("AF(P ∧ Q)")
Let ctl_result be Logic.check_ctl_property(transition_system, ctl_formula)
```

### μ-Calculus

```runa
Note: Most expressive temporal logic
Let mu_calculus_system be Logic.create_mu_calculus_system()

Note: Fixed point operators
Let least_fixpoint be Logic.construct_mu("X", Logic.construct_or("P", Logic.construct_diamond("X")))
Let greatest_fixpoint be Logic.construct_nu("Y", Logic.construct_and("Q", Logic.construct_box("Y")))

Display "μ-calculus least fixpoint: " joined with Logic.mu_formula_to_string(least_fixpoint)
Display "μ-calculus greatest fixpoint: " joined with Logic.mu_formula_to_string(greatest_fixpoint)

Note: μ-calculus model checking
Let mu_property be Logic.parse_mu_formula("μX.(P ∨ ◊X)")
Let mu_evaluation be Logic.evaluate_mu_calculus(mu_property, transition_system)
```

## Higher-Order Logic

### Type Theory and Lambda Calculus

```runa
Note: Create higher-order logic system
Let hol_system be Logic.create_higher_order_system()

Note: Define types
Let nat_type be Logic.define_base_type("ℕ")
Let bool_type be Logic.define_base_type("𝔹")
Let function_type be Logic.define_function_type(nat_type, bool_type)
Let predicate_type be Logic.define_predicate_type(nat_type)

Note: Lambda abstractions
Let identity_function be Logic.construct_lambda("x", nat_type, "x")
Let constant_function be Logic.construct_lambda("x", nat_type, Logic.constant("42"))
Let predicate_lambda be Logic.construct_lambda("n", nat_type, 
    Logic.construct_equality(Logic.construct_modulo("n", "2"), "0"))

Display "Identity function: " joined with Logic.lambda_to_string(identity_function)
Display "Even number predicate: " joined with Logic.lambda_to_string(predicate_lambda)

Note: Function application and β-reduction
Let application be Logic.construct_application(identity_function, "5")
Let beta_reduced be Logic.beta_reduce(application)
Display "After β-reduction: " joined with Logic.term_to_string(beta_reduced)
```

### Polymorphic Types

```runa
Note: Polymorphic type system
Let type_variable_alpha be Logic.create_type_variable("α")
Let polymorphic_identity be Logic.construct_polymorphic_lambda(
    "α", 
    Logic.construct_lambda("x", type_variable_alpha, "x")
)

Let instantiated_nat be Logic.type_instantiate(polymorphic_identity, nat_type)
Let instantiated_bool be Logic.type_instantiate(polymorphic_identity, bool_type)

Note: Type checking
Let type_check_result be Logic.type_check(polymorphic_identity)
If Logic.is_well_typed(type_check_result):
    Let inferred_type be Logic.get_inferred_type(type_check_result)
    Display "Inferred type: " joined with Logic.type_to_string(inferred_type)
```

### Dependent Types

```runa
Note: Dependent type theory
Let dependent_system be Logic.create_dependent_type_system()

Note: Π-types (dependent function types)
Let vector_type be Logic.construct_pi_type(
    "n", nat_type,
    Logic.construct_vector_type(nat_type, "n")
)

Let head_function be Logic.construct_dependent_function(
    "n", nat_type,
    Logic.construct_lambda("v", Logic.construct_vector_type(nat_type, "n + 1"),
        Logic.construct_head("v"))
)

Note: Σ-types (dependent pair types)
Let sigma_type be Logic.construct_sigma_type(
    "n", nat_type,
    Logic.construct_vector_type(bool_type, "n")
)

Display "Dependent function type: " joined with Logic.dependent_type_to_string(vector_type)
```

## Intuitionistic Logic

### Constructive Logic Systems

```runa
Note: Create intuitionistic logic system
Let intuitionistic_system be Logic.create_intuitionistic_system()

Note: Intuitionistic formulas (no law of excluded middle)
Let formula_lem be Logic.parse_formula("P ∨ ¬P")  Note: Law of excluded middle
Let formula_pierce be Logic.parse_formula("((P → Q) → P) → P")  Note: Pierce's law
Let formula_double_neg be Logic.parse_formula("¬¬P → P")  Note: Double negation elimination

Let classical_validity_lem be Logic.check_classical_validity(formula_lem)
Let intuitionistic_validity_lem be Logic.check_intuitionistic_validity(formula_lem)

Display "LEM classically valid: " joined with classical_validity_lem
Display "LEM intuitionistically valid: " joined with intuitionistic_validity_lem

Note: Constructive proofs
Let constructive_proof_exists be Logic.construct_existence_proof(
    "n", nat_type,
    Logic.construct_and(
        Logic.construct_greater_than("n", "10"),
        Logic.construct_is_prime("n")
    ),
    "11"  Note: Witness
)
```

### Heyting Semantics

```runa
Note: Create Heyting algebra model
Let heyting_algebra be Logic.create_heyting_algebra()
Logic.define_heyting_elements(heyting_algebra, ["⊥", "a", "b", "⊤"])
Logic.define_heyting_order(heyting_algebra, [
    ["⊥", "a"], ["⊥", "b"], ["a", "⊤"], ["b", "⊤"]
])

Let intuitionistic_evaluation be Logic.evaluate_in_heyting_algebra(
    formula_double_neg,
    heyting_algebra
)

Display "Double negation in Heyting algebra: " joined with intuitionistic_evaluation
```

## Linear Logic

### Resource-Aware Logic

```runa
Note: Create linear logic system
Let linear_system be Logic.create_linear_logic_system()

Note: Linear logic connectives
Let multiplicative_conjunction be Logic.construct_multiplicative_and("A", "B")  Note: A ⊗ B
Let additive_conjunction be Logic.construct_additive_and("A", "B")              Note: A & B
Let linear_implication be Logic.construct_linear_implication("A", "B")          Note: A ⊸ B
Let exponential be Logic.construct_exponential("A")                            Note: !A

Note: Resource consumption example
Let resource_formula be Logic.parse_linear_formula("money ⊸ (food ⊗ change)")
Let available_resources be Logic.create_resource_context(["money"])
Let consumption_result be Logic.consume_resources(resource_formula, available_resources)

If Logic.consumption_successful(consumption_result):
    Let remaining_resources be Logic.get_remaining_resources(consumption_result)
    Display "Resources after consumption: " joined with Logic.resources_to_string(remaining_resources)
```

## Logical System Analysis

### Completeness and Consistency

```runa
Note: Analyze logical system properties
Let system_analysis be Logic.analyze_logical_system(modal_system_s4)

Let is_complete be Logic.is_complete_system(system_analysis)
Let is_consistent be Logic.is_consistent_system(system_analysis)
Let is_decidable be Logic.is_decidable_system(system_analysis)

Display "System S4 is complete: " joined with is_complete
Display "System S4 is consistent: " joined with is_consistent
Display "System S4 is decidable: " joined with is_decidable

Note: Gödel's incompleteness check
Let arithmetic_system be Logic.create_peano_arithmetic()
Let incompleteness_analysis be Logic.check_incompleteness(arithmetic_system)

If Logic.is_essentially_incomplete(incompleteness_analysis):
    Display "System is subject to Gödel's incompleteness theorems"
    Let godel_sentence be Logic.construct_godel_sentence(arithmetic_system)
    Display "Gödel sentence: " joined with Logic.formula_to_string(godel_sentence)
```

### Decidability and Complexity

```runa
Note: Analyze computational complexity
Let complexity_analysis be Logic.analyze_decision_complexity(first_order_logic)
Let complexity_class be Logic.get_complexity_class(complexity_analysis)

Display "First-order logic complexity: " joined with Logic.complexity_to_string(complexity_class)

Note: Specific fragment analysis
Let two_variable_logic be Logic.create_two_variable_fragment()
Let monadic_logic be Logic.create_monadic_fragment()

Let two_var_decidable be Logic.check_decidability(two_variable_logic)
Let monadic_decidable be Logic.check_decidability(monadic_logic)

Display "Two-variable logic decidable: " joined with two_var_decidable
Display "Monadic logic decidable: " joined with monadic_decidable
```

## Advanced Topics

### Non-Classical Logics

```runa
Note: Many-valued logics
Let three_valued_logic be Logic.create_three_valued_logic()  Note: Łukasiewicz logic
Let fuzzy_logic_system be Logic.create_fuzzy_logic_system()

Let lukasiewicz_evaluation be Logic.evaluate_three_valued("P → P", three_valued_logic)
Let fuzzy_evaluation be Logic.evaluate_fuzzy("P ∧ Q", fuzzy_logic_system, 
    Logic.create_fuzzy_assignment([["P", 0.7], ["Q", 0.3]]))

Display "Three-valued evaluation: " joined with lukasiewicz_evaluation
Display "Fuzzy evaluation: " joined with fuzzy_evaluation

Note: Paraconsistent logic
Let paraconsistent_system be Logic.create_paraconsistent_logic()
Let contradiction be Logic.parse_formula("P ∧ ¬P")
Let explosion be Logic.parse_formula("(P ∧ ¬P) → Q")

Let paraconsistent_validity be Logic.check_paraconsistent_validity(explosion, paraconsistent_system)
Display "Explosion principle in paraconsistent logic: " joined with paraconsistent_validity
```

### Algebraic Logic

```runa
Note: Boolean algebras and logical systems
Let boolean_algebra be Logic.create_boolean_algebra()
Logic.define_boolean_operations(boolean_algebra, ["∧", "∨", "¬", "→", "↔"])

Let cylindric_algebra be Logic.create_cylindric_algebra(3)  Note: 3 dimensions
Let relation_algebra be Logic.create_relation_algebra()

Note: Algebraic semantics
Let algebraic_model be Logic.create_algebraic_model(boolean_algebra)
Let algebraic_satisfaction be Logic.check_algebraic_satisfaction(
    complex_formula,
    algebraic_model
)
```

## Performance and Optimization

### Efficient Implementations

```runa
Note: Performance optimization strategies
Let optimized_formula be Logic.optimize_formula_representation(complex_formula)
Let sharing_analysis be Logic.analyze_subformula_sharing(optimized_formula)

Note: Caching and memoization
Logic.enable_evaluation_cache(True)
Logic.set_cache_size_limit(10000)

Let cached_evaluation be Logic.evaluate_with_cache(complex_formula, model)
Let cache_statistics be Logic.get_cache_statistics()

Display "Cache hit rate: " joined with Logic.get_cache_hit_rate(cache_statistics)

Note: Parallel evaluation
Let parallel_satisfiability be Logic.parallel_sat_check(formula_set, 4)  Note: 4 threads
```

### Memory Management

```runa
Note: Memory-efficient representations
Let compact_formula be Logic.create_compact_representation(large_formula)
Let memory_usage_before be Logic.get_memory_usage()
Logic.apply_garbage_collection()
Let memory_usage_after be Logic.get_memory_usage()

Display "Memory saved: " joined with (memory_usage_before - memory_usage_after) joined with " bytes"
```

## Error Handling and Validation

```runa
Import "core/error_handling" as ErrorHandling

Note: Handle parsing and evaluation errors
Let parsing_result be Logic.parse_formula_safe("∀x∃y(P(x,y) ∧")  Note: Malformed formula
If ErrorHandling.is_syntax_error(parsing_result):
    Let syntax_error be ErrorHandling.get_syntax_error(parsing_result)
    Display "Syntax error: " joined with ErrorHandling.get_error_message(syntax_error)
    Display "Error position: " joined with ErrorHandling.get_error_position(syntax_error)

Note: Handle evaluation timeout
Let timeout_result be Logic.evaluate_with_timeout(complex_formula, model, 5000)  Note: 5 second timeout
If ErrorHandling.is_timeout(timeout_result):
    Display "Evaluation timed out - formula may be too complex"
```

## Integration Examples

### With Automated Proving

```runa
Import "math/logic/proof" as Proof

Note: Use formal systems with theorem proving
Let theorem_to_prove be Logic.parse_formula("(P → Q) → (¬Q → ¬P)")  Note: Contrapositive
Let proof_attempt be Proof.prove_in_system(propositional_system, theorem_to_prove)

If Proof.proof_found(proof_attempt):
    Display "Theorem proved in propositional logic"
    Let proof_steps be Proof.get_proof_steps(proof_attempt)
    Proof.display_natural_deduction_proof(proof_steps)
```

### With Model Checking

```runa
Import "math/logic/verification" as Verification

Note: Use temporal logic for verification
Let safety_property be Logic.parse_ltl_formula("G(¬(critical1 ∧ critical2))")
Let system_model be Verification.create_concurrent_system_model(process_specifications)
Let verification_result be Verification.ltl_model_check(system_model, safety_property)
```

## Best Practices

### Formula Construction
- Build complex formulas incrementally from simpler components
- Use appropriate normal forms for specific applications
- Validate formula syntax before processing
- Consider performance implications of deeply nested formulas

### System Selection
- Choose propositional logic for boolean reasoning tasks
- Use first-order logic for mathematical reasoning
- Apply modal logic for reasoning about possibility and necessity
- Use temporal logic for system property specification

### Performance Considerations
- Enable caching for repeated evaluations
- Use compact representations for large formulas
- Consider parallel evaluation for independent subproblems
- Profile formula evaluation to identify bottlenecks

This module provides a comprehensive foundation for formal logic applications, supporting both theoretical investigation and practical reasoning tasks in computational mathematics and formal verification.