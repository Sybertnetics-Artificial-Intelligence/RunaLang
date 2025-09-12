# Mathematical Biology Module

## Overview

The mathematical biology module provides comprehensive tools for modeling biological systems using mathematical frameworks. This module implements mathematical models for population dynamics, epidemiological processes, evolutionary biology, ecological systems, genetic algorithms, and biochemical kinetics.

## Mathematical Foundation

### Population Dynamics Models

The module implements various population growth models:

**Exponential Growth Model:**
```
dN/dt = rN
```
Where N is population size, r is growth rate.

**Logistic Growth Model:**
```
dN/dt = rN(1 - N/K)
```
Where K is carrying capacity.

**Lotka-Volterra Predator-Prey Model:**
```
dx/dt = ax - bxy
dy/dt = cxy - dy
```
Where x is prey population, y is predator population.

### Epidemiological Models

**SIR Model:**
```
dS/dt = -βSI/N
dI/dt = βSI/N - γI  
dR/dt = γI
```
Where S, I, R are susceptible, infected, recovered populations.

**SEIR Model:**
Extends SIR with exposed compartment E.

### Evolutionary Biology

**Hardy-Weinberg Equilibrium:**
```
p² + 2pq + q² = 1
```
For allele frequencies p and q.

**Selection Models:**
```
Δp = sp(1-p)[p + q(1-h)]/(1 + sp[2p(1-h) + 2q])
```

## Core Data Structures

### Population Model
```runa
Type called "PopulationModel":
    species_count as Integer
    growth_rates as List[Float]
    carrying_capacities as List[Float]
    interaction_matrix as Matrix[Float]
    time_step as Float
    current_populations as List[Float]
```

### Epidemiological State
```runa
Type called "EpidemiologicalState":
    susceptible as Float
    exposed as Float
    infected as Float
    recovered as Float
    deceased as Float
    total_population as Float
    transmission_rate as Float
    incubation_rate as Float
    recovery_rate as Float
    mortality_rate as Float
```

### Genetic Population
```runa
Type called "GeneticPopulation":
    allele_frequencies as Dictionary[String, Float]
    genotype_frequencies as Dictionary[String, Float]
    fitness_values as Dictionary[String, Float]
    mutation_rates as Dictionary[String, Float]
    selection_coefficients as Dictionary[String, Float]
```

### Ecological Network
```runa
Type called "EcologicalNetwork":
    species_list as List[String]
    trophic_levels as Dictionary[String, Integer]
    interaction_strengths as Matrix[Float]
    energy_flows as Matrix[Float]
    biomass_distribution as Dictionary[String, Float]
```

## Basic Usage

### Population Dynamics

```runa
Import "runa/src/stdlib/math/applied/biology"

Process called "simulate_logistic_growth" that returns Void:
    Note: Create logistic growth model
    Let model be Biology.create_logistic_model(
        initial_population: 100.0,
        growth_rate: 0.1,
        carrying_capacity: 1000.0
    )
    
    Note: Simulate for 100 time steps
    Let time_series be Biology.simulate_population_dynamics(model, 100)
    
    Note: Display results
    For Each timepoint in time_series:
        Print("Time: " + timepoint.time + ", Population: " + timepoint.population)
```

### Epidemiological Modeling

```runa
Process called "model_epidemic_spread" that returns Void:
    Note: Create SEIR model
    Let epidemic_model be Biology.create_seir_model(
        total_population: 1000000.0,
        initial_infected: 100.0,
        transmission_rate: 0.3,
        incubation_rate: 1.0/5.2,  Note: 5.2 day incubation
        recovery_rate: 1.0/10.0    Note: 10 day recovery
    )
    
    Note: Simulate epidemic
    Let epidemic_data be Biology.simulate_epidemic(epidemic_model, 365)  Note: 1 year
    
    Note: Calculate key metrics
    Let peak_infections be Biology.find_peak_infections(epidemic_data)
    Let total_affected be Biology.calculate_total_affected(epidemic_data)
    
    Print("Peak infections: " + peak_infections.count + " on day " + peak_infections.day)
    Print("Total affected: " + total_affected)
```

### Genetic Analysis

```runa
Process called "analyze_population_genetics" that returns Void:
    Note: Create genetic population
    Let population be Biology.create_genetic_population()
    Biology.set_allele_frequency(population, "A", 0.6)
    Biology.set_allele_frequency(population, "a", 0.4)
    
    Note: Test Hardy-Weinberg equilibrium
    Let hw_expected be Biology.calculate_hardy_weinberg_frequencies(population)
    Let hw_test be Biology.test_hardy_weinberg_equilibrium(population, hw_expected)
    
    Print("Hardy-Weinberg test p-value: " + hw_test.p_value)
    
    Note: Simulate selection
    Biology.set_selection_coefficient(population, "AA", 1.0)
    Biology.set_selection_coefficient(population, "Aa", 0.95)
    Biology.set_selection_coefficient(population, "aa", 0.8)
    
    Let selection_results be Biology.simulate_selection(population, 50)  Note: 50 generations
    Print("Final allele A frequency: " + selection_results.final_frequencies["A"])
```

## Advanced Implementations

### Multi-Species Population Models

```runa
Process called "model_predator_prey_system" that returns Void:
    Note: Create Lotka-Volterra system
    Let system be Biology.create_lotka_volterra_system()
    
    Note: Set parameters for prey (rabbits)
    Biology.set_species_parameters(system, "prey", Dictionary[String, Float].from_pairs([
        ("growth_rate", 0.1),
        ("predation_rate", 0.075)
    ]))
    
    Note: Set parameters for predator (foxes)
    Biology.set_species_parameters(system, "predator", Dictionary[String, Float].from_pairs([
        ("efficiency", 0.1),
        ("death_rate", 0.05)
    ]))
    
    Note: Set initial conditions
    Biology.set_initial_population(system, "prey", 1000.0)
    Biology.set_initial_population(system, "predator", 50.0)
    
    Note: Simulate system
    Let dynamics be Biology.simulate_multi_species(system, 500)  Note: 500 time steps
    
    Note: Analyze stability
    Let stability_analysis be Biology.analyze_stability(dynamics)
    Print("System stability: " + stability_analysis.classification)
    Print("Oscillation period: " + stability_analysis.period)
```

### Spatial Epidemiology

```runa
Process called "model_spatial_epidemic" that returns Void:
    Note: Create spatial grid
    Let spatial_grid be Biology.create_spatial_grid(100, 100)  Note: 100x100 grid
    
    Note: Initialize population distribution
    Biology.distribute_population(spatial_grid, "uniform", 1000.0)
    
    Note: Set mobility parameters
    Let mobility_model be Biology.create_mobility_model(
        diffusion_rate: 0.1,
        long_distance_rate: 0.01
    )
    
    Note: Create spatial epidemic model
    Let spatial_epidemic be Biology.create_spatial_epidemic_model(
        grid: spatial_grid,
        mobility: mobility_model,
        transmission_rate: 0.3,
        recovery_rate: 0.1
    )
    
    Note: Introduce initial infection
    Biology.seed_infection(spatial_epidemic, 50, 50, 10.0)  Note: Center of grid
    
    Note: Simulate spread
    Let spatial_results be Biology.simulate_spatial_epidemic(spatial_epidemic, 200)
    
    Note: Analyze spatial patterns
    Let wave_speed be Biology.calculate_wave_speed(spatial_results)
    Let final_attack_rate be Biology.calculate_attack_rate(spatial_results)
    
    Print("Epidemic wave speed: " + wave_speed + " units/day")
    Print("Final attack rate: " + final_attack_rate)
```

### Phylogenetic Analysis

```runa
Process called "construct_phylogenetic_tree" that returns Void:
    Note: Load sequence data
    Let sequences be Biology.load_dna_sequences("data/species_sequences.fasta")
    
    Note: Calculate evolutionary distances
    Let distance_matrix be Biology.calculate_genetic_distances(sequences, "kimura_2p")
    
    Note: Construct tree using neighbor-joining
    Let phylo_tree be Biology.construct_neighbor_joining_tree(distance_matrix)
    
    Note: Bootstrap analysis for confidence
    Let bootstrap_support be Biology.bootstrap_analysis(sequences, phylo_tree, 1000)
    Biology.add_bootstrap_support(phylo_tree, bootstrap_support)
    
    Note: Root the tree
    Let rooted_tree be Biology.root_tree(phylo_tree, "outgroup_species")
    
    Note: Calculate evolutionary rates
    Let branch_rates be Biology.calculate_evolutionary_rates(rooted_tree, sequences)
    
    Note: Display tree statistics
    Print("Tree topology: " + Biology.describe_tree_topology(rooted_tree))
    Print("Mean evolutionary rate: " + Statistics.mean(branch_rates.values()))
```

### Biochemical Kinetics

```runa
Process called "model_enzyme_kinetics" that returns Void:
    Note: Create Michaelis-Menten model
    Let enzyme_model be Biology.create_michaelis_menten_model(
        vmax: 100.0,      Note: Maximum velocity
        km: 10.0,         Note: Michaelis constant
        ki: 5.0           Note: Inhibition constant
    )
    
    Note: Define substrate concentrations
    Let substrate_range be Mathematics.create_range(0.1, 100.0, 0.1)
    
    Note: Calculate reaction velocities
    Let velocities be List[Float].create()
    For Each substrate_conc in substrate_range:
        Let velocity be Biology.calculate_reaction_velocity(enzyme_model, substrate_conc)
        velocities.add(velocity)
    
    Note: Fit experimental data
    Let experimental_data be Biology.load_kinetic_data("enzyme_experiment.csv")
    Let fitted_parameters be Biology.fit_michaelis_menten(experimental_data)
    
    Print("Fitted Vmax: " + fitted_parameters.vmax)
    Print("Fitted Km: " + fitted_parameters.km)
    Print("R-squared: " + fitted_parameters.r_squared)
    
    Note: Simulate metabolic pathway
    Let pathway be Biology.create_metabolic_pathway([
        "glucose -> glucose-6-phosphate",
        "glucose-6-phosphate -> fructose-6-phosphate",
        "fructose-6-phosphate -> fructose-1,6-bisphosphate"
    ])
    
    Let pathway_dynamics be Biology.simulate_pathway_dynamics(pathway, 3600.0)  Note: 1 hour
    Biology.plot_metabolite_concentrations(pathway_dynamics)
```

### Evolutionary Game Theory

```runa
Process called "analyze_evolutionary_games" that returns Void:
    Note: Define Hawk-Dove game
    Let payoff_matrix be Biology.create_payoff_matrix(
        strategies: ["Hawk", "Dove"],
        payoffs: Matrix[Float].from_arrays([
            [0.5, 1.0],    Note: Hawk vs [Hawk, Dove]
            [0.0, 0.5]     Note: Dove vs [Hawk, Dove]
        ])
    )
    
    Note: Find evolutionarily stable strategy
    Let ess_analysis be Biology.find_evolutionarily_stable_strategy(payoff_matrix)
    Print("ESS frequencies: Hawk=" + ess_analysis.frequencies["Hawk"] + ", Dove=" + ess_analysis.frequencies["Dove"])
    
    Note: Simulate population dynamics
    Let game_population be Biology.create_game_population(1000, ["Hawk", "Dove"], [0.3, 0.7])
    
    Let evolution_results be Biology.simulate_evolutionary_game(
        population: game_population,
        payoff_matrix: payoff_matrix,
        generations: 100,
        mutation_rate: 0.01
    )
    
    Print("Final strategy distribution:")
    For Each strategy in evolution_results.final_frequencies.keys():
        Print("  " + strategy + ": " + evolution_results.final_frequencies[strategy])
```

## Error Handling and Validation

### Model Validation

```runa
Process called "validate_biological_model" that takes model as PopulationModel returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check parameter ranges
    If model.growth_rates.any(r => r < 0.0):
        validation.add_error("Negative growth rates not allowed")
    
    If model.carrying_capacities.any(k => k <= 0.0):
        validation.add_error("Carrying capacities must be positive")
    
    Note: Check matrix properties
    If not Biology.is_matrix_stable(model.interaction_matrix):
        validation.add_warning("Interaction matrix may lead to unstable dynamics")
    
    Note: Validate time step
    If model.time_step <= 0.0 or model.time_step > 1.0:
        validation.add_error("Time step must be between 0 and 1")
    
    Return validation
```

### Data Quality Checks

```runa
Process called "validate_genetic_data" that takes sequences as List[DNASequence] returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check sequence lengths
    Let lengths be sequences.map(seq => seq.length)
    If not lengths.all_equal():
        validation.add_error("All sequences must have equal length for analysis")
    
    Note: Validate nucleotides
    For Each sequence in sequences:
        For Each nucleotide in sequence.bases:
            If not nucleotide.is_valid_dna_base():
                validation.add_error("Invalid nucleotide found: " + nucleotide)
    
    Note: Check for sufficient variation
    Let variation_level be Biology.calculate_sequence_variation(sequences)
    If variation_level < 0.01:
        validation.add_warning("Low sequence variation may affect phylogenetic analysis")
    
    Return validation
```

## Performance Optimization

### Efficient Simulation Algorithms

```runa
Process called "optimize_population_simulation" that takes model as PopulationModel returns OptimizedModel:
    Note: Use adaptive time stepping for stiff systems
    Let optimized be OptimizedModel.create(model)
    
    Note: Detect stiffness
    Let jacobian be Biology.calculate_jacobian(model)
    Let eigenvalues be LinearAlgebra.calculate_eigenvalues(jacobian)
    Let stiffness_ratio be eigenvalues.max().real / eigenvalues.min().real
    
    If stiffness_ratio > 100.0:
        optimized.set_solver("implicit_euler")
        optimized.set_adaptive_stepping(true)
    Otherwise:
        optimized.set_solver("runge_kutta_4")
    
    Note: Optimize for sparse interactions
    If model.interaction_matrix.sparsity() > 0.8:
        optimized.enable_sparse_matrix_operations()
    
    Return optimized
```

### Parallel Processing

```runa
Process called "parallelize_genetic_analysis" that takes sequences as List[DNASequence] returns ParallelResults:
    Note: Distribute bootstrap calculations
    Let num_cores be System.get_cpu_count()
    Let bootstrap_batches be Biology.create_bootstrap_batches(1000, num_cores)
    
    Let parallel_results be List[BootstrapResult].create()
    Parallel.for_each(bootstrap_batches, batch => {
        Let batch_result be Biology.run_bootstrap_batch(sequences, batch)
        parallel_results.add_thread_safe(batch_result)
    })
    
    Let combined_results = Biology.combine_bootstrap_results(parallel_results)
    Return combined_results
```

## Related Documentation

- **[Mathematical Physics](physics.md)** - Physical modeling foundations
- **[Mathematical Economics](economics.md)** - Economic modeling applications  
- **[Operations Research](operations.md)** - Optimization methods
- **[Statistics Module](../statistics/README.md)** - Statistical analysis tools
- **[Linear Algebra Module](../core/linear_algebra.md)** - Matrix operations
- **[Differential Equations](../core/differential_equations.md)** - Equation solving
- **[Numerical Methods](../core/numerical.md)** - Computational algorithms
- **[Graph Theory](../discrete/graphs.md)** - Network analysis
- **[Probability Module](../probability/README.md)** - Stochastic modeling

## Further Reading

- Population Dynamics and Mathematical Biology
- Epidemiological Modeling Methods  
- Evolutionary Game Theory
- Phylogenetic Analysis Techniques
- Biochemical Systems Theory
- Mathematical Ecology
- Computational Biology Algorithms