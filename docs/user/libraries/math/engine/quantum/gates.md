# Quantum Gates Module

## Overview

The quantum gates module provides comprehensive implementations of quantum gate operations for quantum computing simulations. This module includes standard single-qubit gates, two-qubit gates, multi-qubit gates, parameterized gates, and advanced gate operations including composition, decomposition, and optimization.

## Mathematical Foundation

### Quantum Gates as Unitary Matrices
Quantum gates are represented as unitary matrices U where U†U = I:
```
U† = U⁻¹
```

### Single-Qubit Gates
Single-qubit gates operate on the 2-dimensional Hilbert space with 2×2 matrices.

**Pauli Gates:**
```
X = |0⟩⟨1| + |1⟩⟨0| = [0 1; 1 0]
Y = -i|0⟩⟨1| + i|1⟩⟨0| = [0 -i; i 0]  
Z = |0⟩⟨0| - |1⟩⟨1| = [1 0; 0 -1]
```

**Hadamard Gate:**
```
H = (|0⟩⟨0| + |0⟩⟨1| + |1⟩⟨0| - |1⟩⟨1|)/√2 = [1 1; 1 -1]/√2
```

**Rotation Gates:**
```
R_x(θ) = e^(-iθX/2) = [cos(θ/2) -i·sin(θ/2); -i·sin(θ/2) cos(θ/2)]
R_y(θ) = e^(-iθY/2) = [cos(θ/2) -sin(θ/2); sin(θ/2) cos(θ/2)]
R_z(θ) = e^(-iθZ/2) = [e^(-iθ/2) 0; 0 e^(iθ/2)]
```

### Two-Qubit Gates
Two-qubit gates operate on the 4-dimensional Hilbert space with 4×4 matrices.

**CNOT Gate:**
```
CNOT = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ X = [1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0]
```

**Controlled-Z Gate:**
```
CZ = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ Z = [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 -1]
```

### Gate Composition
Sequential application: (A ∘ B)|ψ⟩ = A(B|ψ⟩)
Matrix form: U_total = U_n ... U_2 U_1

## Core Data Structures

### Quantum Gate
```runa
Type called "QuantumGate":
    name as String
    matrix as List[List[Complex]]
    num_qubits as Integer
    parameters as List[Float]
    is_unitary as Boolean
```

### Gate Sequence
```runa
Type called "GateSequence":
    gates as List[QuantumGate]
    target_qubits as List[List[Integer]]
    total_qubits as Integer
    depth as Integer
```

### Controlled Gate
```runa
Type called "ControlledGate":
    base_gate as QuantumGate
    control_qubits as List[Integer]
    target_qubits as List[Integer]
    control_state as Integer
```

### Parameterized Gate
```runa
Type called "ParameterizedGate":
    base_name as String
    parameter_names as List[String]
    parameter_values as Dictionary[String, Float]
    matrix_function as Function[List[Float], List[List[Complex]]]
```

## Basic Usage

### Creating Single-Qubit Gates

```runa
Import "runa/src/stdlib/math/engine/quantum/gates"

Process called "create_single_qubit_gates" that returns Void:
    Note: Create Pauli gates
    Let pauli_x be Gates.create_pauli_x_gate()
    Let pauli_y be Gates.create_pauli_y_gate()
    Let pauli_z be Gates.create_pauli_z_gate()
    
    Print("Pauli-X gate matrix:")
    Gates.print_gate_matrix(pauli_x)
    
    Note: Create Hadamard gate
    Let hadamard be Gates.create_hadamard_gate()
    Print("Hadamard gate matrix:")
    Gates.print_gate_matrix(hadamard)
    
    Note: Create rotation gates
    Let rotation_x be Gates.create_rotation_x_gate(Mathematics.pi / 4.0)  Note: π/4 rotation
    Let rotation_y be Gates.create_rotation_y_gate(Mathematics.pi / 3.0)  Note: π/3 rotation
    Let rotation_z be Gates.create_rotation_z_gate(Mathematics.pi / 2.0)  Note: π/2 rotation
    
    Print("R_x(π/4) gate matrix:")
    Gates.print_gate_matrix(rotation_x)
    
    Note: Verify unitarity
    Let is_unitary be Gates.verify_unitarity(hadamard)
    Print("Hadamard gate is unitary: " + is_unitary)
```

### Creating Two-Qubit Gates

```runa
Process called "create_two_qubit_gates" that returns Void:
    Note: Create CNOT gate
    Let cnot be Gates.create_cnot_gate()
    Print("CNOT gate matrix:")
    Gates.print_gate_matrix(cnot)
    
    Note: Create controlled-Z gate
    Let cz_gate be Gates.create_controlled_z_gate()
    Print("Controlled-Z gate matrix:")
    Gates.print_gate_matrix(cz_gate)
    
    Note: Create SWAP gate
    Let swap_gate be Gates.create_swap_gate()
    Print("SWAP gate matrix:")
    Gates.print_gate_matrix(swap_gate)
    
    Note: Create controlled rotation gates
    Let controlled_rx be Gates.create_controlled_rotation_x_gate(Mathematics.pi / 6.0)
    Print("Controlled R_x(π/6) gate matrix:")
    Gates.print_gate_matrix(controlled_rx)
    
    Note: Verify two-qubit gate properties
    Let cnot_eigenvalues be Gates.calculate_eigenvalues(cnot)
    Print("CNOT eigenvalues: " + cnot_eigenvalues.toString())
```

### Gate Composition and Sequences

```runa
Process called "compose_gate_sequences" that returns Void:
    Note: Create individual gates
    Let hadamard be Gates.create_hadamard_gate()
    Let pauli_x be Gates.create_pauli_x_gate()
    Let rotation_z be Gates.create_rotation_z_gate(Mathematics.pi / 4.0)
    
    Note: Compose gates sequentially: R_z(π/4) ∘ X ∘ H
    Let gate_sequence be Gates.create_gate_sequence([hadamard, pauli_x, rotation_z])
    
    Note: Calculate composed matrix
    Let composed_matrix be Gates.compose_gate_sequence(gate_sequence)
    Print("Composed gate matrix:")
    Gates.print_matrix(composed_matrix)
    
    Note: Verify composition is unitary
    Let is_composed_unitary be Gates.verify_matrix_unitarity(composed_matrix)
    Print("Composed gate is unitary: " + is_composed_unitary)
    
    Note: Calculate gate sequence depth
    Let sequence_depth be Gates.calculate_sequence_depth(gate_sequence)
    Print("Gate sequence depth: " + sequence_depth)
```

## Advanced Implementations

### Custom Controlled Gates

```runa
Process called "create_controlled_gates" that returns Void:
    Note: Create custom controlled gate
    Let base_gate be Gates.create_rotation_y_gate(Mathematics.pi / 3.0)
    
    Note: Create controlled version
    Let controlled_gate be Gates.create_controlled_gate(
        base_gate: base_gate,
        control_qubits: [0],
        target_qubits: [1],
        control_state: 1  Note: Control on |1⟩ state
    )
    
    Print("Controlled R_y(π/3) gate matrix:")
    Gates.print_gate_matrix(controlled_gate.to_gate())
    
    Note: Create doubly-controlled gate (Toffoli variant)
    Let toffoli_y be Gates.create_multi_controlled_gate(
        base_gate: base_gate,
        control_qubits: [0, 1],
        target_qubits: [2],
        control_state: 3  Note: Control on |11⟩ state
    )
    
    Print("Doubly-controlled R_y gate dimensions: " + 
          toffoli_y.matrix.length + "x" + toffoli_y.matrix[0].length)
    
    Note: Verify controlled gate properties
    Let control_verification be Gates.verify_controlled_gate_structure(controlled_gate)
    Print("Controlled gate structure valid: " + control_verification.is_valid)
```

### Parameterized Gate Operations

```runa
Process called "parameterized_gate_operations" that returns Void:
    Note: Create parameterized rotation gate family
    Let param_gate be Gates.create_parameterized_gate(
        name: "arbitrary_rotation",
        parameter_names: ["theta", "phi", "lambda"],
        matrix_generator: Gates.u3_gate_generator()
    )
    
    Note: Set specific parameters for U3 gate
    Gates.set_parameter_value(param_gate, "theta", Mathematics.pi / 2.0)
    Gates.set_parameter_value(param_gate, "phi", Mathematics.pi / 4.0)
    Gates.set_parameter_value(param_gate, "lambda", Mathematics.pi / 8.0)
    
    Note: Generate gate matrix with current parameters
    Let u3_matrix be Gates.generate_matrix_from_parameters(param_gate)
    Print("U3(π/2, π/4, π/8) gate matrix:")
    Gates.print_matrix(u3_matrix)
    
    Note: Calculate parameter derivatives for optimization
    Let theta_derivative be Gates.calculate_parameter_derivative(param_gate, "theta")
    Print("∂U/∂θ matrix norm: " + Gates.calculate_matrix_norm(theta_derivative))
    
    Note: Create parameter sweep
    Let theta_values be Mathematics.create_range(0.0, 2.0 * Mathematics.pi, 0.1)
    Let gate_family be Gates.create_parameter_sweep(param_gate, "theta", theta_values)
    
    Print("Created gate family with " + gate_family.gates.length + " parameter values")
```

### Gate Decomposition

```runa
Process called "gate_decomposition_analysis" that returns Void:
    Note: Create arbitrary single-qubit gate
    Let arbitrary_matrix be [
        [Complex.create(0.8, 0.2), Complex.create(0.5, -0.3)],
        [Complex.create(0.5, 0.3), Complex.create(0.8, -0.2)]
    ]
    Let arbitrary_gate be Gates.create_gate_from_matrix("arbitrary", arbitrary_matrix)
    
    Note: Decompose into elementary gates
    Let decomposition be Gates.decompose_single_qubit_gate(arbitrary_gate)
    
    Print("Single-qubit gate decomposition:")
    For i in 0 to decomposition.gates.length - 1:
        Let gate be decomposition.gates[i]
        Print("  Gate " + (i+1) + ": " + gate.name + 
              " with parameters " + gate.parameters.toString())
    
    Note: Verify decomposition accuracy
    Let reconstructed_matrix be Gates.compose_gate_matrices(decomposition.gates)
    Let fidelity be Gates.calculate_gate_fidelity(arbitrary_matrix, reconstructed_matrix)
    Print("Decomposition fidelity: " + fidelity)
    
    Note: Decompose two-qubit gate using CNOT + single-qubit gates
    Let arbitrary_2q_gate be Gates.create_random_two_qubit_gate()
    Let cnot_decomposition be Gates.decompose_two_qubit_gate_to_cnot_basis(arbitrary_2q_gate)
    
    Print("Two-qubit gate decomposition:")
    Print("  Number of CNOTs: " + cnot_decomposition.cnot_count)
    Print("  Total gate count: " + cnot_decomposition.total_gates)
    Print("  Circuit depth: " + cnot_decomposition.depth)
```

### Gate Optimization

```runa
Process called "optimize_gate_sequences" that returns Void:
    Note: Create inefficient gate sequence with redundancies
    Let redundant_sequence be [
        Gates.create_hadamard_gate(),
        Gates.create_pauli_z_gate(),
        Gates.create_hadamard_gate(),  Note: H Z H = X
        Gates.create_pauli_x_gate(),
        Gates.create_pauli_x_gate()    Note: X X = I (cancels)
    ]
    
    Print("Original sequence length: " + redundant_sequence.length)
    
    Note: Apply gate optimization
    Let optimized_sequence be Gates.optimize_gate_sequence(redundant_sequence)
    Print("Optimized sequence length: " + optimized_sequence.length)
    
    Note: Verify optimization preserves functionality
    Let original_unitary be Gates.compose_gate_matrices(redundant_sequence)
    Let optimized_unitary be Gates.compose_gate_matrices(optimized_sequence)
    Let optimization_fidelity be Gates.calculate_gate_fidelity(original_unitary, optimized_unitary)
    
    Print("Optimization fidelity: " + optimization_fidelity)
    
    Note: Apply circuit depth optimization
    Let depth_optimized be Gates.optimize_for_depth(redundant_sequence)
    Print("Depth-optimized sequence depth: " + Gates.calculate_sequence_depth(depth_optimized))
    
    Note: Apply gate count optimization
    Let count_optimized be Gates.optimize_for_gate_count(redundant_sequence)
    Print("Gate-count optimized sequence length: " + count_optimized.length)
```

### Advanced Gate Synthesis

```runa
Process called "synthesize_target_gates" that returns Void:
    Note: Define target unitary to synthesize
    Let target_angle be Mathematics.pi / 5.0  Note: Arbitrary angle
    Let target_matrix be [
        [Complex.create(Mathematics.cos(target_angle), 0.0), 
         Complex.create(-Mathematics.sin(target_angle), 0.0)],
        [Complex.create(Mathematics.sin(target_angle), 0.0), 
         Complex.create(Mathematics.cos(target_angle), 0.0)]
    ]
    
    Note: Synthesize using Solovay-Kitaev algorithm
    Let gate_set be Gates.create_universal_gate_set()  Note: {H, T, S}
    Let synthesis_result be Gates.solovay_kitaev_synthesis(
        target_matrix: target_matrix,
        gate_set: gate_set,
        precision: 1e-6
    )
    
    Print("Solovay-Kitaev synthesis results:")
    Print("  Gate count: " + synthesis_result.gate_count)
    Print("  Circuit depth: " + synthesis_result.depth)
    Print("  Approximation error: " + synthesis_result.error)
    
    Note: Alternative synthesis using CNOT + single-qubit gates
    Let cnot_synthesis be Gates.synthesize_with_cnot_basis(
        target_matrix: target_matrix,
        max_cnots: 3
    )
    
    Print("CNOT-based synthesis:")
    Print("  CNOT count: " + cnot_synthesis.cnot_count)
    Print("  Single-qubit gate count: " + cnot_synthesis.single_qubit_count)
    
    Note: Compare synthesis methods
    If synthesis_result.gate_count < cnot_synthesis.total_gates:
        Print("Solovay-Kitaev method more efficient for this target")
    Otherwise:
        Print("CNOT-based method more efficient for this target")
```

### Quantum Gate Tomography

```runa
Process called "perform_gate_tomography" that returns Void:
    Note: Unknown gate to be characterized
    Let unknown_gate be Gates.create_rotation_x_gate(Mathematics.pi / 7.0)  Note: Unknown to tomography
    
    Note: Define input states for process tomography
    Let input_states be [
        "|0⟩", "|1⟩", "|+⟩", "|-⟩", "|+i⟩", "|-i⟩"
    ]
    
    Note: Apply unknown gate to each input state and measure output
    Let tomography_data be Dictionary[String, Dictionary[String, Float]].create()
    
    For Each input_state in input_states:
        Let input_vector be Gates.state_string_to_vector(input_state)
        Let output_vector be Gates.apply_gate_to_vector(unknown_gate, input_vector)
        
        Note: Measure output in different bases
        Let measurements be Dictionary[String, Float].from_pairs([
            ("Z", Gates.measure_expectation_value(output_vector, Gates.pauli_z_gate())),
            ("X", Gates.measure_expectation_value(output_vector, Gates.pauli_x_gate())),
            ("Y", Gates.measure_expectation_value(output_vector, Gates.pauli_y_gate()))
        ])
        
        tomography_data.set(input_state, measurements)
    
    Note: Reconstruct gate matrix from tomography data
    Let reconstructed_matrix be Gates.reconstruct_gate_from_tomography(tomography_data)
    
    Note: Compare with true gate
    Let true_matrix be unknown_gate.matrix
    Let process_fidelity be Gates.calculate_process_fidelity(true_matrix, reconstructed_matrix)
    
    Print("Gate tomography results:")
    Print("  Process fidelity: " + process_fidelity)
    Print("  Diamond norm error: " + Gates.calculate_diamond_norm_distance(true_matrix, reconstructed_matrix))
    
    Note: Extract gate parameters from reconstructed matrix
    Let extracted_params be Gates.extract_rotation_parameters(reconstructed_matrix)
    Print("  Extracted rotation angle: " + extracted_params.angle)
    Print("  True rotation angle: " + (Mathematics.pi / 7.0))
    Print("  Parameter error: " + Mathematics.abs(extracted_params.angle - Mathematics.pi / 7.0))
```

## Error Handling and Validation

### Gate Matrix Validation

```runa
Process called "validate_quantum_gate" that takes gate as QuantumGate returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check matrix dimensions
    Let expected_dim be Mathematics.power(2, gate.num_qubits)
    If gate.matrix.length != expected_dim or gate.matrix[0].length != expected_dim:
        validation.add_error("Gate matrix dimensions incorrect for " + gate.num_qubits + " qubits")
    
    Note: Check unitarity
    If not Gates.verify_unitarity(gate):
        validation.add_error("Gate matrix is not unitary")
    
    Note: Check for NaN or infinite values
    For i in 0 to gate.matrix.length - 1:
        For j in 0 to gate.matrix[i].length - 1:
            Let element be gate.matrix[i][j]
            If not element.is_finite():
                validation.add_error("Matrix contains invalid values at (" + i + ", " + j + ")")
    
    Note: Check parameter consistency
    If gate.parameters.length > 0:
        For Each param in gate.parameters:
            If not param.is_finite():
                validation.add_error("Gate parameter contains invalid value: " + param)
    
    Return validation
```

### Gate Sequence Validation

```runa
Process called "validate_gate_sequence" that takes sequence as GateSequence returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check sequence consistency
    If sequence.gates.length != sequence.target_qubits.length:
        validation.add_error("Gate count doesn't match target qubit specifications")
    
    Note: Check qubit indices
    For i in 0 to sequence.target_qubits.length - 1:
        For Each qubit_index in sequence.target_qubits[i]:
            If qubit_index < 0 or qubit_index >= sequence.total_qubits:
                validation.add_error("Invalid qubit index: " + qubit_index)
    
    Note: Check individual gates
    For Each gate in sequence.gates:
        Let gate_validation be validate_quantum_gate(gate)
        If not gate_validation.is_valid():
            validation.add_errors(gate_validation.errors)
    
    Return validation
```

## Performance Optimization

### Efficient Matrix Operations

```runa
Process called "optimize_gate_operations" that takes gates as List[QuantumGate] returns OptimizedGateSet:
    Let optimized = OptimizedGateSet.create()
    
    Note: Use sparse matrices for gates with many zeros
    For Each gate in gates:
        Let sparsity = Gates.calculate_sparsity(gate.matrix)
        If sparsity > 0.7:  Note: More than 70% zeros
            optimized.add_sparse_gate(gate)
        Otherwise:
            optimized.add_dense_gate(gate)
    
    Note: Cache commonly used gates
    optimized.cache_common_gates([
        "hadamard", "pauli_x", "pauli_y", "pauli_z", "cnot"
    ])
    
    Note: Precompute gate powers for efficiency
    For Each gate in gates:
        If Gates.is_power_gate_beneficial(gate):
            optimized.precompute_powers(gate, [2, 4, 8])
    
    Return optimized
```

### Parallel Gate Synthesis

```runa
Process called "parallel_gate_synthesis" that takes targets as List[List[List[Complex]]] returns List[GateSequence]:
    Let results be List[GateSequence].create()
    
    Note: Synthesize gates in parallel
    Parallel.for_each(targets, target_matrix => {
        Let synthesis_result be Gates.solovay_kitaev_synthesis(
            target_matrix: target_matrix,
            gate_set: Gates.create_universal_gate_set(),
            precision: 1e-6
        )
        results.add_thread_safe(synthesis_result)
    })
    
    Return results
```

## Related Documentation

- **[Quantum States](states.md)** - Quantum state representation and operations
- **[Quantum Circuits](circuits.md)** - Circuit construction and simulation
- **[Quantum Algorithms](algorithms.md)** - Implementation of quantum algorithms
- **[Complex Numbers](../../core/complex.md)** - Complex number arithmetic
- **[Linear Algebra Module](../../core/linear_algebra.md)** - Matrix operations
- **[Trigonometry](../../core/trigonometry.md)** - Trigonometric functions
- **[Optimization Module](../../optimization/README.md)** - Gate optimization methods

## Further Reading

- Quantum Computation and Quantum Information (Nielsen & Chuang)
- Quantum Gate Synthesis and Optimization
- Solovay-Kitaev Theorem and Algorithm
- Universal Quantum Gate Sets
- Quantum Process Tomography
- Fault-Tolerant Quantum Gate Sets
- Quantum Compiling and Circuit Optimization
- Adiabatic Quantum Gates and Holonomic Quantum Computing