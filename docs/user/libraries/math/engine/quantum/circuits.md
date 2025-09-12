# Quantum Circuits Module

## Overview

The quantum circuits module provides comprehensive tools for quantum circuit construction, simulation, and analysis. This module enables building complex quantum circuits, simulating their execution with various backends, optimizing circuit performance, and analyzing circuit properties including noise modeling and error simulation.

## Mathematical Foundation

### Quantum Circuit Model
A quantum circuit is a sequence of quantum gates applied to qubits:
```
U_total = U_n ∘ U_{n-1} ∘ ... ∘ U_2 ∘ U_1
```

Where each U_i represents a gate operation.

### State Evolution
The quantum state evolves under unitary operations:
```
|ψ_final⟩ = U_total |ψ_initial⟩
```

### Measurement Operations
Measurements collapse the quantum state probabilistically:
```
P(outcome = k) = |⟨k|ψ⟩|²
```

### Circuit Depth and Parallelism
Circuit depth is determined by the longest path of sequential gate dependencies.

### Noise Models
**Depolarizing Noise:**
```
ε_dep(ρ) = (1-p)ρ + p/d * I
```

**Amplitude Damping:**
```
ε_AD(ρ) = Σᵢ Aᵢ ρ Aᵢ†
```

**Phase Damping:**
```
ε_PD(ρ) = Σᵢ Bᵢ ρ Bᵢ†
```

## Core Data Structures

### Quantum Circuit
```runa
Type called "QuantumCircuit":
    num_qubits as Integer
    num_classical_bits as Integer
    gates as List[Dictionary[String, Any]]
    measurements as List[Dictionary[String, Integer]]
    parameters as Dictionary[String, Float]
    depth as Integer
```

### Circuit Instruction
```runa
Type called "CircuitInstruction":
    gate_name as String
    target_qubits as List[Integer]
    control_qubits as List[Integer]
    parameters as List[Float]
    classical_condition as Dictionary[String, Any]
```

### Simulation Result
```runa
Type called "SimulationResult":
    state_vector as List[Complex]
    measurement_counts as Dictionary[String, Integer]
    execution_time as Float
    memory_usage as Integer
    fidelity as Float
```

### Circuit Analysis
```runa
Type called "CircuitAnalysis":
    depth as Integer
    gate_count as Dictionary[String, Integer]
    two_qubit_gates as Integer
    complexity_measures as Dictionary[String, Float]
    entanglement_measures as List[Float]
```

## Basic Usage

### Creating Quantum Circuits

```runa
Import "runa/src/stdlib/math/engine/quantum/circuits"

Process called "create_basic_circuits" that returns Void:
    Note: Create a simple 2-qubit circuit
    Let circuit be Circuits.create_quantum_circuit(2, 2)
    
    Note: Add Hadamard gate to first qubit
    Set circuit to Circuits.add_gate(circuit, "hadamard", [0], [])
    
    Note: Add CNOT gate (control=0, target=1)
    Set circuit to Circuits.add_gate(circuit, "cnot", [0, 1], [])
    
    Note: Add measurements
    Set circuit to Circuits.add_measurement(circuit, [0, 1], [0, 1])
    
    Print("Created Bell state preparation circuit:")
    Print(Circuits.circuit_to_string(circuit))
    
    Note: Display circuit visualization
    Print("Circuit visualization:")
    Print(Circuits.visualize_circuit(circuit))
```

### Simulating Quantum Circuits

```runa
Process called "simulate_quantum_circuits" that returns Void:
    Note: Create Bell state circuit
    Let bell_circuit be Circuits.bell_state_circuit()
    
    Note: Add measurements to see the results
    Set bell_circuit to Circuits.add_measurement(bell_circuit, [0, 1], [0, 1])
    
    Note: Simulate with 1000 shots
    Let simulation_result be Circuits.simulate_circuit(bell_circuit, 1000)
    
    Print("Bell state simulation results:")
    Print("Execution time: " + simulation_result.execution_time + " seconds")
    Print("Memory usage: " + simulation_result.memory_usage + " bytes")
    Print("Fidelity: " + simulation_result.fidelity)
    
    Print("Measurement outcomes:")
    For Each outcome in simulation_result.measurement_counts.keys():
        Let count be simulation_result.measurement_counts.get(outcome)
        Let percentage be (count.to_float() / 1000.0) * 100.0
        Print("  |" + outcome + "⟩: " + count + " (" + percentage + "%)")
    
    Note: Get final state vector without measurement
    Let state_vector be Circuits.statevector_simulation(bell_circuit)
    Print("Final state vector amplitudes:")
    For i in 0 to state_vector.length - 1:
        Let amplitude be state_vector[i]
        Print("  |" + Integer.to_binary_string(i, 2) + "⟩: " + amplitude.toString())
```

### Circuit Composition

```runa
Process called "compose_quantum_circuits" that returns Void:
    Note: Create first part - state preparation
    Let preparation_circuit be Circuits.create_quantum_circuit(3, 0)
    Set preparation_circuit to Circuits.add_gate(preparation_circuit, "hadamard", [0], [])
    Set preparation_circuit to Circuits.add_gate(preparation_circuit, "hadamard", [1], [])
    Set preparation_circuit to Circuits.add_gate(preparation_circuit, "hadamard", [2], [])
    
    Note: Create second part - entangling operations
    Let entangling_circuit be Circuits.create_quantum_circuit(3, 0)
    Set entangling_circuit to Circuits.add_gate(entangling_circuit, "cnot", [0, 1], [])
    Set entangling_circuit to Circuits.add_gate(entangling_circuit, "cnot", [1, 2], [])
    
    Note: Compose circuits
    Let composed_circuit be Circuits.compose_circuits(preparation_circuit, entangling_circuit)
    
    Print("Composed circuit depth: " + composed_circuit.depth)
    Print("Composed circuit gate count: " + composed_circuit.gates.length)
    
    Note: Analyze the composed circuit
    Let complexity be Circuits.circuit_complexity(composed_circuit)
    Print("Circuit complexity analysis:")
    For Each measure in complexity.keys():
        Print("  " + measure + ": " + complexity.get(measure))
```

## Advanced Implementations

### Parameterized Quantum Circuits

```runa
Process called "create_parameterized_circuits" that returns Void:
    Note: Create variational quantum circuit
    Let vqe_circuit be Circuits.create_quantum_circuit(4, 0)
    
    Note: Layer 1 - Y rotations with parameters
    Let theta_1 be Mathematics.pi / 4.0
    Let theta_2 be Mathematics.pi / 6.0
    Let theta_3 be Mathematics.pi / 3.0
    Let theta_4 be Mathematics.pi / 8.0
    
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [0], [theta_1])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [1], [theta_2])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [2], [theta_3])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [3], [theta_4])
    
    Note: Entangling layer
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "cnot", [0, 1], [])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "cnot", [2, 3], [])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "cnot", [1, 2], [])
    
    Note: Layer 2 - More Y rotations
    Let phi_1 be Mathematics.pi / 5.0
    Let phi_2 be Mathematics.pi / 7.0
    Let phi_3 be Mathematics.pi / 9.0
    Let phi_4 be Mathematics.pi / 11.0
    
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [0], [phi_1])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [1], [phi_2])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [2], [phi_3])
    Set vqe_circuit to Circuits.add_gate(vqe_circuit, "rotation_y", [3], [phi_4])
    
    Note: Store parameters in circuit
    Circuits.set_circuit_parameter(vqe_circuit, "theta_1", theta_1)
    Circuits.set_circuit_parameter(vqe_circuit, "theta_2", theta_2)
    Circuits.set_circuit_parameter(vqe_circuit, "phi_1", phi_1)
    Circuits.set_circuit_parameter(vqe_circuit, "phi_2", phi_2)
    
    Print("Parameterized VQE circuit created:")
    Print("  Circuit depth: " + vqe_circuit.depth)
    Print("  Parameter count: " + vqe_circuit.parameters.size())
    
    Note: Simulate and analyze entanglement
    Let final_state be Circuits.statevector_simulation(vqe_circuit)
    Let entanglement_entropy be Circuits.calculate_entanglement_entropy(final_state, [0, 1])
    Print("  Entanglement entropy (qubits 0-1): " + entanglement_entropy)
```

### Quantum Algorithm Circuits

```runa
Process called "implement_quantum_algorithms" that returns Void:
    Note: Create quantum teleportation circuit
    Let teleportation_circuit be Circuits.quantum_teleportation_circuit()
    
    Print("Quantum teleportation circuit:")
    Print(Circuits.visualize_circuit(teleportation_circuit))
    
    Note: Create GHZ state circuit
    Let ghz_circuit be Circuits.ghz_state_circuit(5)  Note: 5-qubit GHZ state
    
    Note: Add measurements to analyze the GHZ state
    Set ghz_circuit to Circuits.add_measurement(ghz_circuit, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    
    Let ghz_result be Circuits.simulate_circuit(ghz_circuit, 2000)
    Print("5-qubit GHZ state measurement results:")
    For Each outcome in ghz_result.measurement_counts.keys():
        Let count be ghz_result.measurement_counts.get(outcome)
        Let probability be count.to_float() / 2000.0
        Print("  |" + outcome + "⟩: " + count + " (P = " + probability + ")")
    
    Note: Create quantum adder circuit
    Let adder_circuit be Circuits.quantum_adder_circuit(3)  Note: 3-bit adder
    Print("Quantum adder circuit complexity:")
    Let adder_complexity be Circuits.circuit_complexity(adder_circuit)
    For Each metric in adder_complexity.keys():
        Print("  " + metric + ": " + adder_complexity.get(metric))
```

### Circuit Optimization

```runa
Process called "optimize_quantum_circuits" that returns Void:
    Note: Create inefficient circuit with redundancies
    Let inefficient_circuit be Circuits.create_quantum_circuit(3, 0)
    
    Note: Add redundant gate sequence
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "hadamard", [0], [])
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "pauli_z", [0], [])
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "hadamard", [0], [])  Note: H·Z·H = X
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "pauli_x", [1], [])
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "pauli_x", [1], [])  Note: X·X = I
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "rotation_z", [2], [Mathematics.pi / 4.0])
    Set inefficient_circuit to Circuits.add_gate(inefficient_circuit, "rotation_z", [2], [Mathematics.pi / 4.0])  Note: Can merge
    
    Print("Original circuit:")
    Print("  Gate count: " + inefficient_circuit.gates.length)
    Print("  Circuit depth: " + Circuits.circuit_depth(inefficient_circuit))
    
    Note: Apply different optimization levels
    Let opt_level_1 be Circuits.optimize_circuit(inefficient_circuit, 1)
    Let opt_level_2 be Circuits.optimize_circuit(inefficient_circuit, 2)
    Let opt_level_3 be Circuits.optimize_circuit(inefficient_circuit, 3)
    
    Print("Optimization results:")
    Print("  Level 1 - Gate count: " + opt_level_1.gates.length + ", Depth: " + opt_level_1.depth)
    Print("  Level 2 - Gate count: " + opt_level_2.gates.length + ", Depth: " + opt_level_2.depth)
    Print("  Level 3 - Gate count: " + opt_level_3.gates.length + ", Depth: " + opt_level_3.depth)
    
    Note: Verify optimization preserves functionality
    Let original_unitary be Circuits.unitary_simulation(inefficient_circuit)
    Let optimized_unitary be Circuits.unitary_simulation(opt_level_3)
    Let fidelity be Circuits.calculate_unitary_fidelity(original_unitary, optimized_unitary)
    Print("  Optimization fidelity: " + fidelity)
```

### Noise Modeling and Error Analysis

```runa
Process called "analyze_noise_effects" that returns Void:
    Note: Create test circuit
    Let test_circuit be Circuits.bell_state_circuit()
    Set test_circuit to Circuits.add_measurement(test_circuit, [0, 1], [0, 1])
    
    Note: Simulate ideal case
    Let ideal_result be Circuits.simulate_circuit(test_circuit, 5000)
    
    Note: Add depolarizing noise
    Let noisy_circuit_1 be Circuits.add_depolarizing_noise(test_circuit, 0.01)  Note: 1% error rate
    Let noisy_result_1 be Circuits.simulate_circuit(noisy_circuit_1, 5000)
    
    Note: Add amplitude damping
    Let noisy_circuit_2 be Circuits.add_amplitude_damping(test_circuit, 0.05)  Note: 5% damping
    Let noisy_result_2 be Circuits.simulate_circuit(noisy_circuit_2, 5000)
    
    Note: Add phase damping
    Let noisy_circuit_3 be Circuits.add_phase_damping(test_circuit, 0.03)  Note: 3% phase damping
    Let noisy_result_3 be Circuits.simulate_circuit(noisy_circuit_3, 5000)
    
    Print("Noise analysis for Bell state:")
    Print("Ideal case fidelity: " + ideal_result.fidelity)
    Print("Depolarizing noise fidelity: " + noisy_result_1.fidelity)
    Print("Amplitude damping fidelity: " + noisy_result_2.fidelity)
    Print("Phase damping fidelity: " + noisy_result_3.fidelity)
    
    Note: Compare measurement distributions
    Print("Measurement outcome distributions:")
    Print("Ideal |00⟩ probability: " + (ideal_result.measurement_counts.get("00").to_float() / 5000.0))
    Print("Noisy |00⟩ probability (depol): " + (noisy_result_1.measurement_counts.get("00").to_float() / 5000.0))
    
    Note: Add readout error
    Let readout_error_matrix be [[0.95, 0.05], [0.02, 0.98]]  Note: 5% 0→1 error, 2% 1→0 error
    Let readout_noisy_circuit be Circuits.add_readout_error(test_circuit, readout_error_matrix)
    Let readout_result be Circuits.simulate_circuit(readout_noisy_circuit, 5000)
    Print("Readout error fidelity: " + readout_result.fidelity)
```

### Advanced Circuit Analysis

```runa
Process called "advanced_circuit_analysis" that returns Void:
    Note: Create complex quantum circuit
    Let complex_circuit be Circuits.create_quantum_circuit(6, 0)
    
    Note: Create entangled state preparation
    For i in 0 to 5:
        Set complex_circuit to Circuits.add_gate(complex_circuit, "hadamard", [i], [])
    
    Note: Add entangling gates
    For i in 0 to 4:
        Set complex_circuit to Circuits.add_gate(complex_circuit, "cnot", [i, i + 1], [])
    
    Note: Add rotation layer
    For i in 0 to 5:
        Let angle be (i + 1).to_float() * Mathematics.pi / 12.0
        Set complex_circuit to Circuits.add_gate(complex_circuit, "rotation_z", [i], [angle])
    
    Note: Comprehensive circuit analysis
    Let gate_counts be Circuits.gate_count(complex_circuit)
    Let circuit_depth be Circuits.circuit_depth(complex_circuit)
    Let two_qubit_count be Circuits.two_qubit_gate_count(complex_circuit)
    
    Print("Complex circuit analysis:")
    Print("  Total gates: " + complex_circuit.gates.length)
    Print("  Circuit depth: " + circuit_depth)
    Print("  Two-qubit gates: " + two_qubit_count)
    
    Print("Gate type distribution:")
    For Each gate_type in gate_counts.keys():
        Print("  " + gate_type + ": " + gate_counts.get(gate_type))
    
    Note: Analyze final state properties
    Let final_state be Circuits.statevector_simulation(complex_circuit)
    
    Note: Calculate various entanglement measures
    For i in 0 to 4:  Note: Bipartite entanglement for different cuts
        Let entropy be Circuits.calculate_entanglement_entropy(final_state, [i, i + 1])
        Print("Entanglement entropy (qubits " + i + "-" + (i+1) + "): " + entropy)
    
    Note: Convert to different representations
    Let density_matrix be Circuits.density_matrix_simulation(complex_circuit)
    Let unitary_matrix be Circuits.unitary_simulation(complex_circuit)
    
    Print("Circuit representations generated:")
    Print("  State vector dimension: " + final_state.length)
    Print("  Density matrix dimension: " + density_matrix.length + "x" + density_matrix[0].length)
    Print("  Unitary matrix dimension: " + unitary_matrix.length + "x" + unitary_matrix[0].length)
```

### Circuit Export and Visualization

```runa
Process called "export_and_visualize_circuits" that returns Void:
    Note: Create example circuit
    Let example_circuit be Circuits.create_quantum_circuit(3, 3)
    
    Note: Build quantum Fourier transform circuit
    Set example_circuit to Circuits.add_gate(example_circuit, "hadamard", [0], [])
    Set example_circuit to Circuits.add_gate(example_circuit, "rotation_z", [0], [Mathematics.pi / 2.0])
    Set example_circuit to Circuits.add_gate(example_circuit, "cnot", [0, 1], [])
    Set example_circuit to Circuits.add_gate(example_circuit, "hadamard", [1], [])
    Set example_circuit to Circuits.add_gate(example_circuit, "rotation_z", [1], [Mathematics.pi / 4.0])
    Set example_circuit to Circuits.add_gate(example_circuit, "cnot", [0, 2], [])
    Set example_circuit to Circuits.add_gate(example_circuit, "cnot", [1, 2], [])
    Set example_circuit to Circuits.add_gate(example_circuit, "hadamard", [2], [])
    
    Note: Add measurements
    Set example_circuit to Circuits.add_measurement(example_circuit, [0, 1, 2], [0, 1, 2])
    
    Print("Circuit string representation:")
    Print(Circuits.circuit_to_string(example_circuit))
    
    Print("Circuit ASCII visualization:")
    Print(Circuits.visualize_circuit(example_circuit))
    
    Note: Export to QASM format
    Let qasm_string be Circuits.circuit_to_qasm(example_circuit)
    Print("QASM representation:")
    Print(qasm_string)
    
    Note: Analyze circuit before and after optimization
    Print("Circuit analysis before optimization:")
    Let original_complexity be Circuits.circuit_complexity(example_circuit)
    For Each metric in original_complexity.keys():
        Print("  " + metric + ": " + original_complexity.get(metric))
    
    Let optimized_circuit be Circuits.optimize_circuit(example_circuit, 2)
    Print("Circuit analysis after optimization:")
    Let optimized_complexity be Circuits.circuit_complexity(optimized_circuit)
    For Each metric in optimized_complexity.keys():
        Print("  " + metric + ": " + optimized_complexity.get(metric))
```

## Error Handling and Validation

### Circuit Validation

```runa
Process called "validate_quantum_circuit" that takes circuit as QuantumCircuit returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check basic circuit properties
    If circuit.num_qubits <= 0:
        validation.add_error("Circuit must have at least one qubit")
    
    If circuit.num_classical_bits < 0:
        validation.add_error("Number of classical bits cannot be negative")
    
    Note: Validate gate instructions
    For Each gate_instruction in circuit.gates:
        Let gate_name be gate_instruction.get("gate_name")
        Let target_qubits be gate_instruction.get("target_qubits")
        
        Note: Check target qubits are within bounds
        For Each qubit_index in target_qubits:
            If qubit_index < 0 or qubit_index >= circuit.num_qubits:
                validation.add_error("Gate targets invalid qubit: " + qubit_index)
    
    Note: Validate measurements
    For Each measurement in circuit.measurements:
        Let qubit_index be measurement.get("qubit_index")
        Let classical_index be measurement.get("classical_index")
        
        If qubit_index < 0 or qubit_index >= circuit.num_qubits:
            validation.add_error("Measurement targets invalid qubit: " + qubit_index)
        
        If classical_index < 0 or classical_index >= circuit.num_classical_bits:
            validation.add_error("Measurement targets invalid classical bit: " + classical_index)
    
    Note: Check circuit consistency
    If circuit.gates.length == 0 and circuit.measurements.length == 0:
        validation.add_warning("Circuit contains no gates or measurements")
    
    Return validation
```

### Simulation Validation

```runa
Process called "validate_simulation_parameters" that takes circuit as QuantumCircuit, shots as Integer returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check shot count
    If shots <= 0:
        validation.add_error("Number of shots must be positive")
    
    If shots > 1000000:
        validation.add_warning("Large number of shots may cause memory issues")
    
    Note: Check circuit size for simulation feasibility
    Let state_dimension be Mathematics.power(2, circuit.num_qubits)
    If state_dimension > 1048576:  Note: 2^20 = ~1M dimensional state space
        validation.add_error("Circuit too large for classical simulation (>" + circuit.num_qubits + " qubits)")
    
    Note: Check for measurement compatibility
    If circuit.measurements.length == 0 and shots > 1:
        validation.add_warning("No measurements defined but multiple shots requested")
    
    Return validation
```

## Performance Optimization

### Simulation Optimization

```runa
Process called "optimize_circuit_simulation" that takes circuit as QuantumCircuit returns OptimizedSimulation:
    Let optimized be OptimizedSimulation.create()
    
    Note: Choose optimal simulation backend
    If circuit.num_qubits <= 25:
        optimized.set_backend("state_vector")
    Otherwise If circuit.num_qubits <= 30 and Circuits.is_sparse_circuit(circuit):
        optimized.set_backend("sparse_state_vector")
    Otherwise:
        optimized.set_backend("matrix_product_state")
    
    Note: Enable parallel gate application for large circuits
    If circuit.gates.length > 100:
        optimized.enable_parallel_gates()
    
    Note: Use gate caching for repeated patterns
    Let gate_pattern_analysis be Circuits.analyze_gate_patterns(circuit)
    If gate_pattern_analysis.has_repeated_patterns:
        optimized.enable_gate_caching()
    
    Return optimized
```

### Memory Management

```runa
Process called "manage_simulation_memory" that takes circuit as QuantumCircuit, shots as Integer returns MemoryStrategy:
    Let strategy be MemoryStrategy.create()
    
    Note: Calculate memory requirements
    Let state_vector_memory be Mathematics.power(2, circuit.num_qubits) * 16  Note: Complex128 = 16 bytes
    Let measurement_memory be shots * circuit.measurements.length * 4  Note: Integer = 4 bytes
    
    If state_vector_memory > 1073741824:  Note: 1GB
        strategy.use_streaming_simulation()
        strategy.set_chunk_size(1048576)  Note: 1M state components per chunk
    
    If measurement_memory > 104857600:  Note: 100MB
        strategy.use_result_streaming()
    
    strategy.set_garbage_collection_frequency(100)  Note: Every 100 gates
    
    Return strategy
```

## Related Documentation

- **[Quantum States](states.md)** - Quantum state representation and operations
- **[Quantum Gates](gates.md)** - Quantum gate operations and transformations  
- **[Quantum Algorithms](algorithms.md)** - Implementation of quantum algorithms
- **[Complex Numbers](../../core/complex.md)** - Complex number arithmetic
- **[Linear Algebra Module](../../core/linear_algebra.md)** - Matrix operations
- **[Probability Module](../../probability/README.md)** - Probability distributions and sampling
- **[Optimization Module](../../optimization/README.md)** - Circuit optimization methods

## Further Reading

- Quantum Computation and Quantum Information (Nielsen & Chuang)
- Quantum Circuit Simulation Methods
- Quantum Error Correction and Fault Tolerance
- Variational Quantum Algorithms
- Quantum Circuit Optimization Techniques
- NISQ Quantum Computing
- Quantum Noise and Decoherence Models
- Quantum Programming Languages and Compilers