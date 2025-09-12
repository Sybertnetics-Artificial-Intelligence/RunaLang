# Markov Processes - Runa Standard Library

The `math/probability/markov` module provides comprehensive support for Markov processes, chains, and decision processes. This module enables modeling systems with the Markov property where future states depend only on the current state.

## Overview

Markov processes are fundamental to modeling systems where the future evolution depends only on the current state, not the entire history. This module provides tools for:

- **Discrete-time Markov chains** with finite and infinite state spaces
- **Continuous-time Markov processes** including birth-death processes
- **Hidden Markov Models** for systems with unobservable states
- **Markov Decision Processes** for optimal control and reinforcement learning
- **Absorbing Markov chains** for reliability and queuing analysis
- **Semi-Markov processes** with state-dependent holding times

## Key Features

### Markov Chain Analysis
- Transition probability matrices and generators
- Steady-state distribution computation
- Transient analysis and first-passage times
- Classification of states (recurrent, transient, periodic)
- Absorption probabilities and expected hitting times

### Hidden Markov Models
- Forward-backward algorithm for likelihood computation
- Viterbi algorithm for optimal state sequence decoding
- Baum-Welch algorithm for parameter estimation
- Multiple observation models (discrete, Gaussian, mixture)

### Markov Decision Processes
- Value iteration and policy iteration algorithms
- Q-learning and temporal difference methods
- Partially Observable MDPs (POMDPs)
- Multi-armed bandits and contextual bandits

### Advanced Features
- Markov chain Monte Carlo diagnostics
- Reversible jump MCMC for variable dimension problems
- Regime-switching models for time series
- Markov-modulated processes for risk modeling

## Quick Start

```runa
Use math/probability/markov

Note: Create a simple weather model
Let weather_states be ["Sunny", "Rainy", "Cloudy"]
Let transition_matrix be Matrix([
    [0.7, 0.2, 0.1],  Note: From Sunny
    [0.3, 0.4, 0.3],  Note: From Rainy  
    [0.4, 0.3, 0.3]   Note: From Cloudy
])

Note: Create Markov chain
Let weather_chain be MarkovChain::new(weather_states, transition_matrix)

Note: Compute steady-state distribution
Let steady_state be weather_chain.steady_state_distribution()
Print("Long-term weather probabilities: {steady_state}")

Note: Simulate weather sequence
Let initial_state be 0  Note: Start sunny
Let forecast be weather_chain.simulate(initial_state, 30)  Note: 30 days
Print("Weather forecast: {forecast}")

Note: Analyze first-passage times
Let rain_hitting_time be weather_chain.first_passage_time(0, 1)  Note: Sunny to Rainy
Print("Expected time to rain from sunny: {rain_hitting_time} days")
```

## Discrete-Time Markov Chains

### Basic Chain Operations

```runa
Note: Create absorption chain (gambler's ruin)
Let states be Range(0, 11)  Note: Money from $0 to $10
Let absorbing_chain be AbsorbingMarkovChain::new(states)
    .with_absorbing_states([0, 10])
    .with_transition_probability(|i, j| {
        If i == 0 Or i == 10:
            Return If i == j Then 1.0 Else 0.0
        Otherwise If j == i + 1:
            Return 0.6  Note: Win probability
        Otherwise If j == i - 1:
            Return 0.4  Note: Lose probability
        Otherwise:
            Return 0.0
    })

Note: Compute absorption probabilities
Let absorption_probs be absorbing_chain.absorption_probabilities(5)  Note: Start with $5
Print("Probability of winning from $5: {absorption_probs[10]}")
Print("Expected time to absorption: {absorbing_chain.expected_absorption_time(5)}")
```

### State Classification

```runa
Note: Analyze chain structure
Let chain_analysis be MarkovChainAnalyzer::new(transition_matrix)
Let classification be chain_analysis.classify_states()

For Each state, class_info In classification:
    Print("State {state}: {class_info.type}")
    If class_info.is_recurrent:
        Print("  Period: {class_info.period}")
        Print("  Return time: {class_info.expected_return_time}")

Note: Find communicating classes
Let comm_classes be chain_analysis.communicating_classes()
Print("Number of communicating classes: {comm_classes.length}")
```

## Continuous-Time Markov Processes

### Birth-Death Processes

```runa
Note: Model population dynamics
Let birth_rates be [0.0, 1.5, 2.0, 2.5, 2.0, 1.0, 0.0]  Note: Population-dependent births
Let death_rates be [0.0, 0.5, 1.0, 1.5, 2.5, 3.0, 4.0]  Note: Population-dependent deaths

Let population_process be BirthDeathProcess::new(birth_rates, death_rates)
    .with_carrying_capacity(6)

Note: Compute steady-state distribution
Let equilibrium be population_process.steady_state_distribution()
Print("Equilibrium population distribution: {equilibrium}")

Note: Simulate population trajectory
Let trajectory be population_process.simulate_path(3, 0.0, 100.0, 0.1)  Note: Start at 3, 100 time units
Print("Population over time: {trajectory}")

Note: Compute extinction probability
Let extinction_prob be population_process.extinction_probability(3)
Print("Extinction probability from size 3: {extinction_prob}")
```

### Queueing Systems

```runa
Note: M/M/1 queue analysis
Let arrival_rate be 2.0  Note: customers per hour
Let service_rate be 3.0  Note: customers per hour

Let queue_process be MM1Queue::new(arrival_rate, service_rate)

Note: Performance metrics
Let utilization be queue_process.utilization()
Let avg_customers be queue_process.average_customers()
Let avg_wait_time be queue_process.average_waiting_time()

Print("Queue utilization: {utilization}")
Print("Average customers in system: {avg_customers}")
Print("Average waiting time: {avg_wait_time} hours")

Note: Simulate queue over time
Let queue_simulation be queue_process.simulate_continuous(0, 8.0, 0.01)  Note: 8 hours
Let busy_periods be queue_simulation.analyze_busy_periods()
Print("Number of busy periods: {busy_periods.length}")
```

## Hidden Markov Models

### Discrete Observation HMM

```runa
Note: DNA sequence analysis example
Let states be ["A", "T", "G", "C"]  Note: Hidden nucleotide states
Let observations be ["Peak1", "Peak2", "Peak3", "Peak4"]  Note: Observed peaks

Let transition_probs be Matrix([
    [0.3, 0.2, 0.3, 0.2],  Note: From A
    [0.2, 0.3, 0.2, 0.3],  Note: From T
    [0.3, 0.2, 0.3, 0.2],  Note: From G
    [0.2, 0.3, 0.2, 0.3]   Note: From C
])

Let emission_probs be Matrix([
    [0.7, 0.1, 0.1, 0.1],  Note: A emits mostly Peak1
    [0.1, 0.7, 0.1, 0.1],  Note: T emits mostly Peak2
    [0.1, 0.1, 0.7, 0.1],  Note: G emits mostly Peak3
    [0.1, 0.1, 0.1, 0.7]   Note: C emits mostly Peak4
])

Let initial_probs be [0.25, 0.25, 0.25, 0.25]

Let hmm be DiscreteHMM::new(states, observations, transition_probs, emission_probs, initial_probs)

Note: Observe sequence and decode
Let observed_sequence be [0, 1, 2, 3, 0, 1, 2]  Note: Peak indices
Let likelihood be hmm.forward_probability(observed_sequence)
Print("Sequence likelihood: {likelihood}")

Note: Find most likely hidden sequence
Let decoded_states be hmm.viterbi_decode(observed_sequence)
Print("Most likely nucleotide sequence: {decoded_states}")
```

### Gaussian HMM

```runa
Note: Economic regime switching model
Let regime_states be ["Recession", "Expansion"]
Let regime_transitions be Matrix([
    [0.8, 0.2],  Note: Recession persistence
    [0.1, 0.9]   Note: Expansion persistence
])

Note: Different growth rates and volatilities per regime
Let regime_parameters be [
    GaussianParameters::new(-0.01, 0.05),  Note: Recession: negative growth, high volatility
    GaussianParameters::new(0.02, 0.02)    Note: Expansion: positive growth, low volatility
]

Let regime_hmm be GaussianHMM::new(regime_states, regime_transitions, regime_parameters)

Note: Fit model to historical data
Let returns_data be load_stock_returns("SPY")  Note: Load S&P 500 returns
Let fitted_hmm be regime_hmm.fit_baum_welch(returns_data, max_iterations: 100, tolerance: 1e-6)

Note: Decode economic regimes
Let regime_probabilities be fitted_hmm.posterior_probabilities(returns_data)
Let regime_sequence be fitted_hmm.viterbi_decode(returns_data)

Print("Fitted transition matrix: {fitted_hmm.transition_matrix}")
Print("Recession periods: {regime_sequence.filter(|r| r == 0)}")
```

## Markov Decision Processes

### Basic MDP Setup

```runa
Note: Grid world navigation problem
Let grid_size be (5, 5)
Let actions be ["North", "South", "East", "West"]
Let goal_state be (4, 4)
Let obstacle_states be [(2, 2), (3, 2)]

Let grid_mdp be GridWorldMDP::new(grid_size, actions)
    .with_goal_state(goal_state, reward: 10.0)
    .with_obstacle_states(obstacle_states, reward: -10.0)
    .with_step_cost(-0.1)
    .with_transition_noise(0.1)  Note: 10% chance of random movement

Note: Solve using value iteration
Let value_iteration_solver be ValueIteration::new()
    .with_discount_factor(0.9)
    .with_convergence_threshold(1e-6)
    .with_max_iterations(1000)

Let solution be value_iteration_solver.solve(grid_mdp)
Print("Converged in {solution.iterations} iterations")
Print("Optimal value at start (0,0): {solution.values[(0, 0)]}")

Note: Extract optimal policy
Let policy be solution.extract_policy()
For Each state In grid_mdp.states():
    If Not obstacle_states.contains(state):
        Let optimal_action be policy.get_action(state)
        Print("State {state}: take action {optimal_action}")
```

### Q-Learning Implementation

```runa
Note: Reinforcement learning approach
Let q_learner be QLearning::new(grid_mdp)
    .with_learning_rate(0.1)
    .with_discount_factor(0.9)
    .with_exploration_strategy(EpsilonGreedy::new(0.1))

Note: Train the agent
Let training_episodes be 1000
For episode In Range(training_episodes):
    Let state be grid_mdp.reset()
    Let episode_return be 0.0
    
    While Not grid_mdp.is_terminal(state):
        Let action be q_learner.select_action(state)
        Let (next_state, reward) be grid_mdp.step(state, action)
        
        q_learner.update(state, action, reward, next_state)
        
        state = next_state
        episode_return += reward
    
    If episode % 100 == 0:
        Print("Episode {episode}: Return = {episode_return}")

Note: Compare learned policy with optimal
Let learned_policy be q_learner.extract_policy()
Let policy_difference be PolicyComparator::compare(optimal_policy, learned_policy)
Print("Policy agreement: {policy_difference.agreement_percentage}%")
```

### Partially Observable MDPs

```runa
Note: Tiger problem - classic POMDP example
Let tiger_states be ["TigerLeft", "TigerRight"]
Let tiger_actions be ["Listen", "OpenLeft", "OpenRight"]
Let tiger_observations be ["HearLeft", "HearRight"]

Let tiger_pomdp be POMDP::new(tiger_states, tiger_actions, tiger_observations)
    .with_transition_function(|state, action| {
        Match action:
            "Listen" => Return state  Note: Listening doesn't change tiger position
            _ => Return tiger_states.sample_uniform()  Note: Tiger moves randomly after opening
    })
    .with_observation_function(|state, action| {
        Match action:
            "Listen" => Return If state == "TigerLeft" Then "HearLeft" Else "HearRight" With probability 0.85
            _ => Return tiger_observations.sample_uniform()
    })
    .with_reward_function(|state, action| {
        Match action:
            "Listen" => Return -1.0  Note: Cost of listening
            "OpenLeft" => Return If state == "TigerLeft" Then -100.0 Else 10.0
            "OpenRight" => Return If state == "TigerRight" Then -100.0 Else 10.0
    })

Note: Solve using point-based value iteration
Let pbvi_solver be PointBasedValueIteration::new()
    .with_belief_points(1000)
    .with_horizon(10)

Let pomdp_solution be pbvi_solver.solve(tiger_pomdp)
Print("POMDP value function has {pomdp_solution.alpha_vectors.length} alpha vectors")

Note: Test policy on belief states
Let initial_belief be UniformBelief::new(tiger_states)
Let policy_value be pomdp_solution.evaluate_belief(initial_belief)
Print("Expected value from uniform belief: {policy_value}")
```

## Performance Optimization

### Sparse Matrix Operations

```runa
Note: Large sparse Markov chains
Let sparse_chain be SparseMarkovChain::new()
    .with_dimension(10000)
    .with_sparsity_pattern(BandedPattern::new(bandwidth: 3))

Note: Efficient steady-state computation
Let sparse_solver be SparseEigenSolver::new()
    .with_method(ArpackMethod::new())
    .with_convergence_tolerance(1e-10)

Let steady_state be sparse_solver.find_steady_state(sparse_chain)
Print("Computed steady state for 10,000 state chain")
```

### Parallel Simulation

```runa
Note: Monte Carlo estimation with multiple trajectories
Let parallel_simulator be ParallelMarkovSimulator::new(weather_chain)
    .with_thread_count(8)
    .with_batch_size(1000)

Let trajectories be parallel_simulator.simulate_batch(
    initial_states: [0, 1, 2],
    trajectory_length: 365,
    num_trajectories: 100000
)

Let annual_rain_days be trajectories
    .parallel_map(|traj| traj.count(|state| state == 1))
    .collect_statistics()

Print("Average rainy days per year: {annual_rain_days.mean} ± {annual_rain_days.std_dev}")
```

## Advanced Applications

### Financial Modeling

```runa
Note: Credit rating transition analysis
Let credit_ratings be ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "Default"]
Let rating_transitions be load_rating_transition_matrix("credit_data.csv")

Let credit_chain be MarkovChain::new(credit_ratings, rating_transitions)

Note: Compute default probabilities over multiple years
Let initial_rating be "BBB"
Let initial_index be credit_ratings.index_of("BBB")
Let default_index be credit_ratings.index_of("Default")

For year In Range(1, 11):
    Let transition_power be rating_transitions.power(year)
    Let default_prob be transition_power[initial_index, default_index]
    Print("Year {year} default probability: {default_prob:.4f}")

Note: Simulate credit portfolio
Let portfolio_ratings be ["A", "BBB", "BB", "BBB", "A", "BB", "A"]
Let portfolio_defaults be credit_chain.simulate_portfolio_defaults(
    portfolio_ratings,
    time_horizon: 5,
    num_simulations: 10000
)

Print("Expected portfolio defaults in 5 years: {portfolio_defaults.mean}")
```

### Network Reliability

```runa
Note: System reliability with component failures
Let components be ["Server1", "Server2", "Network", "Database"]
Let system_states be generate_system_states(components)  Note: All possible component combinations

Let reliability_chain be ReliabilityMarkovChain::new(components)
    .with_failure_rates([0.01, 0.015, 0.005, 0.02])  Note: Per hour
    .with_repair_rates([0.1, 0.12, 0.2, 0.08])       Note: Per hour
    .with_system_function(|state| {
        Note: System works if at least one server AND network AND database work
        Let servers_up be state["Server1"] Or state["Server2"]
        Return servers_up And state["Network"] And state["Database"]
    })

Note: Compute system availability
Let availability be reliability_chain.steady_state_availability()
Print("System availability: {availability:.6f}")

Note: Find critical components
Let importance_measures be reliability_chain.compute_importance_measures()
For Each component, importance In importance_measures:
    Print("{component} importance: {importance:.4f}")
```

## Error Handling and Validation

### Matrix Validation

```runa
Note: Validate transition matrix properties
Process validate_transition_matrix(matrix as Matrix[Real]) returns ValidationResult:
    Let validator be MarkovChainValidator::new()
    
    Note: Check if rows sum to 1
    If Not validator.check_row_sums(matrix, tolerance: 1e-10):
        Return ValidationResult::error("Rows do not sum to 1")
    
    Note: Check for negative probabilities
    If Not validator.check_non_negative(matrix):
        Return ValidationResult::error("Contains negative probabilities")
    
    Note: Check for irreducibility if required
    If Not validator.check_irreducible(matrix):
        Return ValidationResult::warning("Chain is reducible")
    
    Return ValidationResult::success()

Let validation be validate_transition_matrix(transition_matrix)
Match validation:
    ValidationResult::Success => Print("Matrix is valid")
    ValidationResult::Warning(msg) => Print("Warning: {msg}")
    ValidationResult::Error(msg) => Panic("Invalid matrix: {msg}")
```

### Convergence Diagnostics

```runa
Note: MCMC convergence diagnostics for HMM fitting
Process diagnose_hmm_convergence(hmm_chains as List[HMMFitResult]) returns ConvergenceDiagnostics:
    Let diagnostics be MCMCDiagnostics::new()
    
    Note: Gelman-Rubin statistic
    Let r_hat be diagnostics.gelman_rubin_statistic(hmm_chains.map(|c| c.log_likelihood_trace))
    
    Note: Effective sample size
    Let eff_samples be diagnostics.effective_sample_size(hmm_chains[0].parameter_trace)
    
    Note: Geweke diagnostic
    Let geweke_scores be diagnostics.geweke_diagnostic(hmm_chains[0].parameter_trace)
    
    Return ConvergenceDiagnostics {
        r_hat: r_hat,
        effective_samples: eff_samples,
        geweke_scores: geweke_scores,
        converged: r_hat < 1.1 And eff_samples > 400
    }
```

## Best Practices

### Model Selection and Validation

```runa
Note: Compare different Markov models using information criteria
Process select_best_markov_model(data as List[Integer], max_states as Integer) returns ModelSelection:
    Let models be List::new()
    
    For num_states In Range(2, max_states + 1):
        Note: Fit HMM with different numbers of states
        Let hmm be DiscreteHMM::with_states(num_states)
        Let fitted_model be hmm.fit_em(data, max_iterations: 200)
        
        Note: Compute information criteria
        Let log_likelihood be fitted_model.log_likelihood(data)
        Let num_parameters be fitted_model.count_parameters()
        Let aic be -2.0 * log_likelihood + 2.0 * num_parameters
        Let bic be -2.0 * log_likelihood + num_parameters * Real::ln(data.length)
        
        models.push(ModelResult {
            num_states: num_states,
            model: fitted_model,
            aic: aic,
            bic: bic,
            log_likelihood: log_likelihood
        })
    
    Note: Select model with lowest BIC
    Let best_model be models.min_by(|m| m.bic)
    
    Return ModelSelection {
        best_model: best_model,
        all_models: models,
        selection_criterion: "BIC"
    }
```

### Computational Efficiency

```runa
Note: Efficient implementation for large-scale problems
Process optimize_large_markov_chain(chain as MarkovChain) returns OptimizedChain:
    Note: Use sparse representation for large chains
    If chain.dimension() > 1000:
        Let sparse_chain be chain.to_sparse()
            .with_compression(CSRFormat::new())
        
        Note: Use iterative methods for eigenvalue problems
        Let solver be IterativeEigenSolver::new()
            .with_method(LanczosMethod::new())
            .with_preconditioning(true)
        
        Return OptimizedChain::Sparse(sparse_chain, solver)
    Otherwise:
        Note: Use dense methods for smaller chains
        Let dense_solver be DenseEigenSolver::new()
            .with_method(QRMethod::new())
        
        Return OptimizedChain::Dense(chain, dense_solver)
```

### Memory Management

```runa
Note: Stream-based processing for very long simulations
Process simulate_long_trajectory(chain as MarkovChain, length as Integer) returns TrajectoryStream:
    Note: Use streaming to avoid memory issues
    Let stream be TrajectoryStream::new(chain)
        .with_buffer_size(10000)
        .with_checkpoint_interval(100000)
    
    Return stream.simulate_streaming(length)
        .with_statistics_collection(true)
        .with_periodic_summary(10000)
```

The Markov processes module provides a complete framework for modeling and analyzing systems with memory-less properties, from simple weather models to complex financial and biological systems. The combination of exact mathematical algorithms and efficient computational implementations makes it suitable for both theoretical analysis and practical applications.