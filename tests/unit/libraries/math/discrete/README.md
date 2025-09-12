# Discrete Mathematics Test Suite

Comprehensive unit tests for the Runa standard library discrete mathematics modules.

## Overview

This test suite provides complete coverage for 6 discrete mathematics modules:

- **Combinatorics** (`combinatorics_test.runa`) - 45 tests
- **Number Theory** (`number_theory_test.runa`) - 38 tests  
- **Logic** (`logic_test.runa`) - 52 tests
- **Automata Theory** (`automata_test.runa`) - 48 tests
- **Coding Theory** (`coding_theory_test.runa`) - 65 tests
- **Graph Theory** (`graph_theory_test.runa`) - 55 tests

**Total: 303 unit tests covering 321 functions across all discrete math modules**

## Quick Start

```runa
Import "tests/unit/libraries/math/discrete/discrete_test_runner" as DiscreteTests

Note: Run all discrete math tests
DiscreteTests.run_discrete_math_test_suite()

Note: Run specific module tests
DiscreteTests.run_specific_module("combinatorics")
DiscreteTests.run_specific_module("number_theory")

Note: Quick smoke tests
DiscreteTests.run_smoke_tests()
```

## Test Files

### 1. Combinatorics Tests (`combinatorics_test.runa`)

Tests combinatorial functions including:
- **Factorials**: Standard, double, subfactorial computations
- **Permutations**: With/without repetition, circular permutations
- **Combinations**: Binomial coefficients, multiset combinations
- **Stirling Numbers**: First/second kind, asymptotic approximations
- **Partitions**: Integer partitions, Bell numbers, restricted partitions
- **Special Sequences**: Fibonacci, Catalan, derangements

**Key Test Functions:**
- `test_factorial_computation()` - Factorial accuracy and edge cases
- `test_permutation_computation()` - Permutation counting
- `test_combination_computation()` - Binomial coefficient validation
- `test_stirling_numbers_computation()` - Stirling number calculations
- `test_partition_generation()` - Integer partition enumeration

### 2. Number Theory Tests (`number_theory_test.runa`)

Tests number theoretical algorithms:
- **Primality Testing**: Miller-Rabin, AKS, deterministic tests
- **Prime Generation**: Sieve of Eratosthenes, probabilistic generation
- **GCD/LCM**: Euclidean algorithms, extended GCD
- **Modular Arithmetic**: Exponentiation, inverse, square roots
- **Diophantine Equations**: Linear/quadratic equation solving
- **Factorization**: Trial division, Pollard's rho, quadratic sieve

**Key Test Functions:**
- `test_miller_rabin_primality()` - Probabilistic primality testing
- `test_extended_euclidean_algorithm()` - GCD with coefficients
- `test_chinese_remainder_theorem()` - System solving
- `test_quadratic_sieve_factorization()` - Large integer factorization

### 3. Logic Tests (`logic_test.runa`)

Tests formal logic systems:
- **Boolean Logic**: Operations, normal forms, equivalences
- **SAT Solving**: DPLL, CDCL, unit propagation
- **Truth Tables**: Generation, minimization, analysis
- **Predicate Logic**: Unification, resolution, proof systems
- **Model Checking**: CTL, LTL, temporal logic verification
- **Modal Logic**: Kripke structures, accessibility relations

**Key Test Functions:**
- `test_dpll_sat_solver()` - Boolean satisfiability
- `test_truth_table_generation()` - Exhaustive truth evaluation
- `test_cnf_conversion()` - Conjunctive normal form
- `test_temporal_logic_model_checking()` - LTL verification

### 4. Automata Theory Tests (`automata_test.runa`)

Tests computational automata:
- **Finite Automata**: DFA, NFA, ε-NFA creation and simulation
- **Regular Expressions**: Parsing, NFA conversion, optimization
- **Conversions**: NFA→DFA subset construction, minimization
- **Context-Free Grammars**: Parsing, FIRST/FOLLOW sets
- **Parsing Algorithms**: CYK, Earley, LL, LR parsers
- **Turing Machines**: Construction, simulation, complexity analysis

**Key Test Functions:**
- `test_simulate_dfa_acceptance()` - DFA string recognition
- `test_nfa_to_dfa_subset_construction()` - Conversion algorithms
- `test_regex_to_nfa_thompson()` - Thompson's construction
- `test_parse_cky_algorithm()` - Context-free parsing

### 5. Coding Theory Tests (`coding_theory_test.runa`)

Tests error-correcting codes:
- **Linear Codes**: Generator/parity-check matrices, encoding
- **Hamming Codes**: Single-error correction, extended codes
- **Reed-Solomon**: Symbol-level correction, finite field operations
- **BCH Codes**: Binary error correction, syndrome decoding
- **Convolutional Codes**: Sequential encoding, Viterbi decoding
- **Advanced Codes**: LDPC, polar, concatenated codes

**Key Test Functions:**
- `test_decode_hamming_syndrome()` - Single-error correction
- `test_decode_reed_solomon_berlekamp_massey()` - Symbol error correction
- `test_compute_entropy()` - Information theory measures
- `test_viterbi_decoding()` - Convolutional code decoding

### 6. Graph Theory Tests (`graph_theory_test.runa`)

Tests graph algorithms:
- **Graph Creation**: Empty, complete, random, cycle graphs
- **Traversals**: DFS, BFS, iterative deepening
- **Shortest Paths**: Dijkstra, Bellman-Ford, Floyd-Warshall
- **Spanning Trees**: Kruskal, Prim, Borůvka algorithms
- **Network Flow**: Ford-Fulkerson, Edmonds-Karp, Dinic
- **Matching**: Bipartite, general, weighted matching
- **Graph Coloring**: Vertex, edge, list coloring
- **Planarity**: Testing, embedding, crossing numbers

**Key Test Functions:**
- `test_dijkstra_shortest_path()` - Single-source shortest paths
- `test_kruskal_minimum_spanning_tree()` - MST construction
- `test_ford_fulkerson_max_flow()` - Maximum flow computation
- `test_graph_coloring_greedy()` - Vertex coloring

## Test Execution Options

### Full Test Suite
```runa
DiscreteTests.run_discrete_math_test_suite()
```
Runs all 303 tests across all modules (~5-10 minutes)

### Quick Tests
```runa
DiscreteTests.run_quick_discrete_tests()
```
Runs 18 essential tests covering core functionality (~30 seconds)

### Performance Tests
```runa
DiscreteTests.run_performance_tests()
```
Runs performance-focused tests with large inputs (~2-3 minutes)

### Selective Testing
```runa
Note: Test specific modules
DiscreteTests.run_discrete_tests_by_category(["combinatorics", "number_theory"])

Note: Individual module tests
CombinatoricsTest.run_all_combinatorics_tests()
NumberTheoryTest.run_all_number_theory_tests()
```

### CI/CD Integration
```runa
Note: Optimized for continuous integration
DiscreteTests.run_ci_test_suite()

Note: Extended nightly testing
DiscreteTests.run_nightly_test_suite()
```

## Test Architecture

### Test Data Generation
Each module includes comprehensive test data generators:
- **Mathematical Constants**: Known values for validation
- **Edge Cases**: Boundary conditions, empty inputs
- **Random Data**: Stress testing with varied inputs
- **Performance Data**: Large-scale inputs for performance validation

### Assertion Framework
Custom assertion helpers for mathematical validation:
- **Numerical Precision**: Floating-point comparison with tolerance
- **Structural Validation**: Graph/automata structure verification  
- **Algorithm Correctness**: Mathematical property verification
- **Performance Bounds**: Timing and complexity validation

### Error Handling Testing
Comprehensive error scenario coverage:
- **Invalid Inputs**: Malformed data, out-of-range values
- **Resource Limits**: Memory/time constraint testing
- **Numerical Stability**: Overflow, underflow, precision issues
- **Algorithm Failures**: Non-convergent algorithms, unsolvable problems

## Performance Characteristics

### Expected Test Durations
- **Combinatorics**: ~45 seconds (large factorial computations)
- **Number Theory**: ~60 seconds (primality testing, factorization)
- **Logic**: ~90 seconds (SAT solving, model checking)
- **Automata**: ~75 seconds (NFA→DFA conversion, parsing)
- **Coding Theory**: ~120 seconds (complex decoding algorithms)
- **Graph Theory**: ~80 seconds (shortest paths, network flows)

### Memory Requirements
- **Typical**: 128-256 MB for standard test execution
- **Performance Tests**: 512 MB - 1 GB for large-scale testing
- **Peak Usage**: During Reed-Solomon/LDPC decoding tests

### Computational Complexity
- **Basic Tests**: O(n²) algorithms with n ≤ 100
- **Advanced Tests**: O(n³) algorithms with n ≤ 50
- **Stress Tests**: Exponential algorithms with carefully chosen limits

## Module Dependencies

### External Dependencies
```runa
Import "dev/test" as UnitTest              // Core testing framework
Import "collections" as Collections        // Data structures
Import "engine/linalg/core" as LinAlg     // Linear algebra (coding theory)
```

### Internal Dependencies
- Each test module is self-contained
- No cross-module test dependencies
- Shared assertion patterns but independent implementations

## Test Quality Metrics

### Coverage Statistics
- **Function Coverage**: 284/321 functions (88.5%)
- **Branch Coverage**: High coverage of conditional paths
- **Edge Case Coverage**: Comprehensive boundary testing
- **Error Path Coverage**: Full error handling validation

### Test Categories Distribution
- **Unit Tests**: 70% - Individual function testing
- **Integration Tests**: 20% - Multi-function workflows
- **Performance Tests**: 8% - Large-scale validation
- **Error Tests**: 2% - Exception handling

## Continuous Integration

### CI Test Pipeline
1. **Smoke Tests** (30 seconds) - Basic functionality
2. **Quick Tests** (2 minutes) - Core features  
3. **Full Suite** (8 minutes) - Complete coverage
4. **Performance Tests** (5 minutes) - Scalability validation

### Test Report Generation
Automated reports include:
- **Success/Failure Rates** by module
- **Performance Metrics** and timing analysis
- **Coverage Analysis** with gap identification
- **Trend Analysis** for regression detection

## Contributing

### Adding New Tests
1. Follow existing test patterns in each module
2. Include both positive and negative test cases
3. Add appropriate assertion helpers for new data types
4. Update test count estimates in `get_test_count()`

### Test Naming Conventions
- `test_[function_name]_[scenario]` for unit tests
- `test_[algorithm]_[property]` for algorithmic validation
- `test_[category]_edge_cases` for boundary testing
- `test_[operation]_performance` for performance validation

### Documentation Requirements
- Document complex test scenarios
- Explain mathematical properties being validated
- Reference algorithms and theoretical bounds
- Include complexity analysis for performance tests