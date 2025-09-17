# Quantum States Module

## Overview

The quantum states module provides comprehensive tools for quantum state representation, manipulation, and analysis. This module implements both state vector and density matrix formalism, enabling full quantum mechanical calculations including pure and mixed states, entanglement measures, and quantum information processing operations.

## Mathematical Foundation

### Quantum State Vector
A quantum state |ψ⟩ is represented as a complex vector in a Hilbert space:
```
|ψ⟩ = Σᵢ αᵢ |i⟩
```
Where αᵢ are complex amplitudes and |i⟩ are basis states.

### Normalization Condition
For a valid quantum state:
```
⟨ψ|ψ⟩ = Σᵢ |αᵢ|² = 1
```

### Density Matrix Representation
Mixed states are represented by density matrices:
```
ρ = Σᵢ pᵢ |ψᵢ⟩⟨ψᵢ|
```
With properties:
- Trace(ρ) = 1
- ρ† = ρ (Hermitian)
- ρ ≥ 0 (positive semidefinite)

### Tensor Products
For multi-qubit systems:
```
|ψ⟩ = |ψ₁⟩ ⊗ |ψ₂⟩ ⊗ ... ⊗ |ψₙ⟩
```

### Entanglement Measures
**Von Neumann Entropy:**
```
S(ρ) = -Tr(ρ log₂ ρ)
```

**Concurrence (for 2-qubit states):**
```
C(ρ) = max(0, λ₁ - λ₂ - λ₃ - λ₄)
```

## Core Data Structures

### Quantum State
```runa
Type called "QuantumState":
    state_vector as List[Complex]
    num_qubits as Integer
    is_normalized as Boolean
    basis_labels as List[String]
```

### Density Matrix
```runa
Type called "DensityMatrix":
    matrix as List[List[Complex]]
    num_qubits as Integer
    trace as Float
    is_valid as Boolean
```

### Measurement Result
```runa
Type called "MeasurementResult":
    outcome as Integer
    probability as Float
    post_measurement_state as QuantumState
    measurement_basis as List[String]
```

### Entanglement Measures
```runa
Type called "EntanglementMeasures":
    entanglement_entropy as Float
    concurrence as Float
    negativity as Float
    schmidt_coefficients as List[Float]
```

## Basic Usage

### Creating Quantum States

```runa
Import "runa/src/stdlib/math/engine/quantum/states"

Process called "create_quantum_states" that returns Void:
    Note: Create |0⟩ state using zero_state function
    Let zero_state be States.zero_state(1)  Note: Single qubit |0⟩
    Print("Zero state created with " + zero_state.num_qubits + " qubits")
    
    Note: Create |1⟩ state using one_state function
    Let one_state be States.one_state(1)   Note: Single qubit |1⟩
    Print("One state: basis labels: " + one_state.basis_labels.toString())
    
    Note: Create superposition state |+⟩ = equal superposition
    Let plus_state be States.plus_state(1)
    Print("Plus state is normalized: " + plus_state.is_normalized)
    
    Note: Create computational basis state
    Let basis_state be States.computational_basis_state(2, 2)  Note: |10⟩ state
    Print("Computational basis state |10⟩ created")
    
    Note: Create random quantum state using Haar measure
    Let random_state be States.random_state(2, 12345)  Note: 2 qubits, seed=12345
    Print("Random state generated with seed")
```

### Multi-Qubit States and Bell States

```runa
Process called "multi_qubit_operations" that returns Void:
    Note: Create 2-qubit computational basis states
    Let state_00 be States.computational_basis_state(0, 2)  Note: |00⟩
    Let state_11 be States.computational_basis_state(3, 2)  Note: |11⟩
    
    Print("State |00⟩ has " + state_00.num_qubits + " qubits")
    Print("State |11⟩ basis labels: " + state_11.basis_labels.toString())
    
    Note: Create Bell states using bell_state function
    Let bell_phi_plus be States.bell_state(0)   Note: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    Let bell_phi_minus be States.bell_state(1)  Note: |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
    Let bell_psi_plus be States.bell_state(2)   Note: |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
    Let bell_psi_minus be States.bell_state(3)  Note: |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
    
    Print("Bell state |Φ⁺⟩ is normalized: " + bell_phi_plus.is_normalized)
    Print("Bell state |Φ⁻⟩ has dimension: " + bell_phi_minus.state_vector.length)
    
    Note: Create coherent state for continuous variables
    Let alpha_amplitude be MathOps.ComplexNumber
    Set alpha_amplitude.real_part to "1.5"
    Set alpha_amplitude.imaginary_part to "0.5"
    Let coherent_state be States.coherent_state(alpha_amplitude, 1)
    Print("Coherent state created with amplitude α = 1.5 + 0.5i")
```

### State Measurements

```runa
Process called "quantum_measurements" that returns Void:
    Note: Create superposition state
    Let superposition be States.create_plus_state(1)
    
    Note: Perform computational basis measurement
    Let measurement_result be States.measure_computational_basis(superposition)
    Print("Measurement outcome: " + measurement_result.outcome)
    Print("Measurement probability: " + measurement_result.probability)
    Print("Post-measurement state: " + States.state_to_string(measurement_result.post_measurement_state))
    
    Note: Perform multiple measurements for statistics
    Let num_measurements be 1000
    Let outcomes be List[Integer].create()
    
    For i in 0 to num_measurements - 1:
        Let fresh_state be States.create_plus_state(1)
        Let result be States.measure_computational_basis(fresh_state)
        outcomes.add(result.outcome)
    
    Let zero_count be outcomes.count(0)
    Let one_count be outcomes.count(1)
    
    Print("Statistics from " + num_measurements + " measurements:")
    Print("  |0⟩ outcomes: " + zero_count + " (" + (zero_count.to_float() / num_measurements * 100.0) + "%)")
    Print("  |1⟩ outcomes: " + one_count + " (" + (one_count.to_float() / num_measurements * 100.0) + "%)")
```

## Advanced Implementations

### Density Matrix Operations

```runa
Process called "density_matrix_operations" that returns Void:
    Note: Create mixed state: 50% |0⟩ + 50% |1⟩
    Let zero_state be States.create_zero_state(1)
    Let one_state be States.create_one_state(1)
    
    Let mixed_state be States.create_mixed_state([
        (zero_state, 0.5),
        (one_state, 0.5)
    ])
    
    Print("Mixed state density matrix:")
    States.print_density_matrix(mixed_state)
    
    Note: Calculate purity
    Let purity be States.calculate_purity(mixed_state)
    Print("Purity: " + purity)
    Print("Is pure state: " + (purity > 0.999))
    
    Note: Partial trace for multi-qubit systems
    Let two_qubit_state be States.create_bell_state("phi_plus")
    Let density_matrix_2q be States.state_to_density_matrix(two_qubit_state)
    
    Note: Trace out second qubit
    Let reduced_state_1 be States.partial_trace(density_matrix_2q, [1])  Note: Trace out qubit 1
    Print("Reduced density matrix (qubit 0):")
    States.print_density_matrix(reduced_state_1)
    
    Note: Calculate von Neumann entropy of reduced state
    Let entropy be States.calculate_von_neumann_entropy(reduced_state_1)
    Print("Von Neumann entropy of reduced state: " + entropy)
```

### Advanced Entanglement Analysis

```runa
Process called "advanced_entanglement_analysis" that returns Void:
    Note: Create various Bell states
    Let bell_states be Dictionary[String, QuantumState].from_pairs([
        ("phi_plus", States.create_bell_state("phi_plus")),
        ("phi_minus", States.create_bell_state("phi_minus")),
        ("psi_plus", States.create_bell_state("psi_plus")),
        ("psi_minus", States.create_bell_state("psi_minus"))
    ])
    
    Print("Entanglement analysis of Bell states:")
    For Each name in bell_states.keys():
        Let state be bell_states[name]
        Let measures be States.calculate_entanglement_measures(state)
        
        Print("Bell state |" + name + "⟩:")
        Print("  Concurrence: " + measures.concurrence)
        Print("  Entanglement of Formation: " + measures.entanglement_of_formation)
        Print("  Negativity: " + measures.negativity)
    
    Note: Create 3-qubit GHZ state: (|000⟩ + |111⟩)/√2
    Let ghz_amplitudes be List[Complex].create()
    For i in 0 to 7:  Note: 2³ = 8 basis states
        If i == 0 or i == 7:
            ghz_amplitudes.add(Complex.create(1.0/Mathematics.sqrt(2.0), 0.0))
        Otherwise:
            ghz_amplitudes.add(Complex.create(0.0, 0.0))
    
    Let ghz_state be States.create_state_from_amplitudes(ghz_amplitudes)
    
    Note: Analyze multipartite entanglement
    Let multipartite_measures be States.calculate_multipartite_entanglement(ghz_state)
    Print("GHZ state multipartite entanglement:")
    Print("  3-tangle: " + multipartite_measures.three_tangle)
    Print("  Global entanglement measure: " + multipartite_measures.global_entanglement)
```

### Quantum State Tomography

```runa
Process called "quantum_state_tomography" that returns Void:
    Note: Prepare unknown quantum state
    Let theta be Mathematics.pi / 3.0
    Let phi be Mathematics.pi / 4.0
    Let unknown_state_amplitudes be [
        Complex.create(Mathematics.cos(theta/2.0), 0.0),
        Complex.create(Mathematics.sin(theta/2.0) * Mathematics.cos(phi), Mathematics.sin(theta/2.0) * Mathematics.sin(phi))
    ]
    Let unknown_state be States.create_state_from_amplitudes(unknown_state_amplitudes)
    
    Print("Original state parameters:")
    Print("  θ = " + theta)
    Print("  φ = " + phi)
    
    Note: Perform tomographic measurements
    Let num_measurements be 10000
    
    Note: Pauli-X basis measurements
    Let x_outcomes be States.measure_in_basis(unknown_state, "pauli_x", num_measurements)
    
    Note: Pauli-Y basis measurements  
    Let y_outcomes be States.measure_in_basis(unknown_state, "pauli_y", num_measurements)
    
    Note: Pauli-Z basis measurements (computational basis)
    Let z_outcomes be States.measure_in_basis(unknown_state, "pauli_z", num_measurements)
    
    Note: Reconstruct density matrix from measurements
    Let reconstructed_density = States.reconstruct_density_matrix_from_measurements([
        ("pauli_x", x_outcomes),
        ("pauli_y", y_outcomes),  
        ("pauli_z", z_outcomes)
    ])
    
    Note: Compare with original state
    Let original_density be States.state_to_density_matrix(unknown_state)
    Let fidelity be States.calculate_state_fidelity(original_density, reconstructed_density)
    
    Print("State tomography results:")
    Print("  Fidelity between original and reconstructed: " + fidelity)
    
    Note: Extract Bloch sphere parameters from reconstructed state
    Let bloch_vector be States.extract_bloch_vector(reconstructed_density)
    Print("  Reconstructed Bloch vector: (" + bloch_vector.x + ", " + bloch_vector.y + ", " + bloch_vector.z + ")")
```

### Decoherence and Noise Modeling

```runa
Process called "model_decoherence" that returns Void:
    Note: Create initial pure state
    Let initial_state be States.create_plus_state(1)
    Let initial_density be States.state_to_density_matrix(initial_state)
    
    Print("Initial state purity: " + States.calculate_purity(initial_density))
    
    Note: Apply amplitude damping noise
    Let damping_rate be 0.1
    Let time_steps be [0.0, 1.0, 2.0, 5.0, 10.0]
    
    Print("Amplitude damping evolution:")
    For Each time in time_steps:
        Let noisy_state be States.apply_amplitude_damping(initial_density, damping_rate, time)
        Let purity be States.calculate_purity(noisy_state)
        Let excited_population be States.get_population(noisy_state, 1)  Note: |1⟩ population
        
        Print("  t=" + time + ": purity=" + purity + ", P(|1⟩)=" + excited_population)
    
    Note: Apply dephasing noise
    Let dephasing_rate be 0.05
    Print("Phase damping evolution:")
    For Each time in time_steps:
        Let dephased_state be States.apply_phase_damping(initial_density, dephasing_rate, time)
        Let coherence be States.get_off_diagonal_magnitude(dephased_state)
        
        Print("  t=" + time + ": coherence=" + coherence)
    
    Note: Apply depolarizing noise
    Let depolarizing_probability be 0.1
    Let depolarized_state be States.apply_depolarizing_noise(initial_density, depolarizing_probability)
    Print("After depolarizing noise (p=" + depolarizing_probability + "):")
    Print("  Purity: " + States.calculate_purity(depolarized_state))
```

### Quantum Process Tomography

```runa
Process called "quantum_process_tomography" that returns Void:
    Note: Unknown quantum process (let's say it's a rotation)
    Let rotation_angle be Mathematics.pi / 6.0
    
    Note: Define input states for process tomography
    Let input_states be [
        States.create_zero_state(1),
        States.create_one_state(1),
        States.create_plus_state(1),
        States.create_minus_state(1),
        States.create_plus_i_state(1),
        States.create_minus_i_state(1)
    ]
    
    Note: Apply unknown process and measure outputs
    Let process_data be List[Tuple[QuantumState, DensityMatrix]].create()
    
    For Each input_state in input_states:
        Note: Apply the unknown process (Y rotation)
        Let output_state be States.apply_rotation_y(input_state, rotation_angle)
        Let output_density be States.state_to_density_matrix(output_state)
        process_data.add((input_state, output_density))
    
    Note: Reconstruct process matrix (chi matrix)
    Let chi_matrix be States.reconstruct_process_matrix(process_data)
    
    Note: Analyze the reconstructed process
    Let process_fidelity be States.calculate_process_fidelity(chi_matrix, "rotation_y", rotation_angle)
    Print("Process tomography results:")
    Print("  Process fidelity: " + process_fidelity)
    
    Note: Extract process parameters
    Let estimated_angle be States.extract_rotation_angle_from_chi(chi_matrix, "y")
    Print("  Estimated rotation angle: " + estimated_angle)
    Print("  Error in angle estimation: " + Mathematics.abs(estimated_angle - rotation_angle))
```

## Error Handling and Validation

### State Validation

```runa
Process called "validate_quantum_state" that takes state as QuantumState returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check normalization
    Let norm_squared be States.calculate_norm_squared(state)
    If Mathematics.abs(norm_squared - 1.0) > 1e-10:
        validation.add_error("State is not normalized. Norm² = " + norm_squared)
    
    Note: Check amplitude validity
    For i in 0 to state.state_vector.length - 1:
        Let amplitude be state.state_vector[i]
        If not amplitude.is_finite():
            validation.add_error("Invalid amplitude at index " + i + ": " + amplitude.toString())
    
    Note: Check dimension consistency
    Let expected_dimension be Mathematics.power(2, state.num_qubits)
    If state.state_vector.length != expected_dimension:
        validation.add_error("Dimension mismatch: expected " + expected_dimension + ", got " + state.state_vector.length)
    
    Return validation
```

### Density Matrix Validation

```runa
Process called "validate_density_matrix" that takes rho as DensityMatrix returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check trace
    If Mathematics.abs(rho.trace - 1.0) > 1e-10:
        validation.add_error("Trace is not 1. Trace = " + rho.trace)
    
    Note: Check Hermiticity
    If not States.is_hermitian(rho):
        validation.add_error("Density matrix is not Hermitian")
    
    Note: Check positive semidefiniteness
    Let eigenvalues be States.calculate_eigenvalues(rho)
    For Each eigenvalue in eigenvalues:
        If eigenvalue.real < -1e-10:
            validation.add_error("Negative eigenvalue found: " + eigenvalue.real)
    
    Note: Check dimension consistency
    Let expected_dim be Mathematics.power(2, rho.num_qubits)
    If rho.matrix.length != expected_dim or rho.matrix[0].length != expected_dim:
        validation.add_error("Matrix dimension inconsistent with number of qubits")
    
    Return validation
```

## Performance Optimization

### Efficient State Operations

```runa
Process called "optimize_state_operations" that takes state as QuantumState returns OptimizedState:
    Let optimized be OptimizedState.create()
    
    Note: Use sparse representation for states with many zeros
    Let zero_threshold be 1e-12
    Let non_zero_count be 0
    For Each amplitude in state.state_vector:
        If amplitude.magnitude() > zero_threshold:
            non_zero_count = non_zero_count + 1
    
    Let sparsity be non_zero_count.to_float() / state.state_vector.length.to_float()
    If sparsity < 0.1:  Note: Less than 10% non-zero
        optimized.use_sparse_representation(true)
        optimized.set_zero_threshold(zero_threshold)
    
    Note: Optimize for specific state types
    If States.is_computational_basis_state(state):
        optimized.set_representation_type("computational_basis")
    Otherwise If States.is_product_state(state):
        optimized.set_representation_type("tensor_product")
        optimized.factorize_state(state)
    
    Return optimized
```

### Parallel State Processing

```runa
Process called "parallel_entanglement_analysis" that takes states as List[QuantumState] returns List[EntanglementMeasures]:
    Let results be List[EntanglementMeasures].create()
    
    Note: Process states in parallel
    Parallel.for_each(states, state => {
        Let measures be States.calculate_entanglement_measures(state)
        results.add_thread_safe(measures)
    })
    
    Return results
```

## Related Documentation

- **[Quantum Gates](gates.md)** - Quantum gate operations and transformations
- **[Quantum Circuits](circuits.md)** - Circuit construction and simulation
- **[Quantum Algorithms](algorithms.md)** - Implementation of quantum algorithms
- **[Linear Algebra Module](../../core/linear_algebra.md)** - Matrix operations and decompositions
- **[Complex Numbers](../../core/complex.md)** - Complex number arithmetic
- **[Probability Module](../../probability/README.md)** - Probability distributions and sampling
- **[Tensor Operations](../../tensors/README.md)** - Multi-dimensional array operations

## Further Reading

- Quantum Computation and Quantum Information (Nielsen & Chuang)
- Quantum Information Theory and Applications
- Entanglement Measures and Quantum Correlations
- Quantum State Tomography Methods
- Decoherence and Noise in Quantum Systems
- Multipartite Entanglement Theory
- Quantum Process Tomography
- Quantum Error Correction Fundamentals