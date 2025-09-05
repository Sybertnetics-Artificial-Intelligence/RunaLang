# Mathematical Economics Module

## Overview

The mathematical economics module provides comprehensive tools for modeling economic systems, market dynamics, game theory, auction mechanisms, optimization problems, and econometric analysis. This module implements advanced mathematical frameworks for understanding economic behavior, market equilibrium, strategic interactions, and policy analysis.

## Mathematical Foundation

### Utility Theory

**Utility Function:**
```
U(x₁, x₂, ..., xₙ) → ℝ
```
Subject to budget constraint: p₁x₁ + p₂x₂ + ... + pₙxₙ ≤ m

**Marginal Utility:**
```
MU_i = ∂U/∂x_i
```

**Elasticity of Substitution:**
```
σ = d(ln(x₁/x₂))/d(ln(MRS₁₂))
```

### Market Equilibrium

**Supply and Demand:**
```
Q^s = f(P, factors)
Q^d = g(P, factors)
Equilibrium: Q^s = Q^d
```

**Consumer and Producer Surplus:**
```
CS = ∫[P_equilibrium to P_max] D(P)dP
PS = ∫[P_min to P_equilibrium] S(P)dP
```

### Game Theory

**Nash Equilibrium:**
For strategy profiles s* = (s₁*, s₂*, ..., sₙ*):
```
u_i(s_i*, s_{-i}*) ≥ u_i(s_i, s_{-i}*) ∀s_i ∈ S_i, ∀i
```

**Mixed Strategy:**
```
σ_i ∈ Δ(S_i) where Σ_s σ_i(s) = 1
```

### Auction Theory

**Revenue Equivalence:**
Under certain conditions, all standard auction formats yield same expected revenue.

**Optimal Reserve Price:**
```
r* = c + (1-F(r*))/f(r*)
```

## Core Data Structures

### Market Structure
```runa
Type called "MarketStructure":
    demand_function as Function[Float, Float]
    supply_function as Function[Float, Float]
    market_type as MarketType
    participants as List[MarketAgent]
    equilibrium_price as Float
    equilibrium_quantity as Float
    consumer_surplus as Float
    producer_surplus as Float
    deadweight_loss as Float
```

### Game Structure
```runa
Type called "GameStructure":
    players as List[String]
    strategy_sets as Dictionary[String, List[String]]
    payoff_functions as Dictionary[String, PayoffFunction]
    information_structure as InformationStructure
    game_type as GameType
    solution_concepts as List[SolutionConcept]
```

### Auction Mechanism
```runa
Type called "AuctionMechanism":
    auction_type as AuctionType
    bidders as List[Bidder]
    valuation_distribution as ProbabilityDistribution
    reserve_price as Float
    allocation_rule as AllocationRule
    payment_rule as PaymentRule
    revenue_function as Function[List[Float], Float]
```

### Economic Agent
```runa
Type called "EconomicAgent":
    agent_id as String
    preferences as UtilityFunction
    endowments as Dictionary[String, Float]
    budget as Float
    strategy as Strategy
    beliefs as BeliefStructure
    rationality_type as RationalityType
```

## Basic Usage

### Market Analysis

```runa
Import "runa/src/stdlib/math/applied/economics"

Process called "analyze_market_equilibrium" that returns Void:
    Note: Define demand function: Q = 100 - 2P
    Let demand be Economics.create_linear_demand_function(100.0, -2.0)
    
    Note: Define supply function: Q = -20 + 3P
    Let supply be Economics.create_linear_supply_function(-20.0, 3.0)
    
    Note: Create market structure
    Let market be Economics.create_market_structure(demand, supply)
    
    Note: Find equilibrium
    Let equilibrium be Economics.find_market_equilibrium(market)
    Print("Equilibrium price: " + equilibrium.price)
    Print("Equilibrium quantity: " + equilibrium.quantity)
    
    Note: Calculate welfare measures
    Let welfare be Economics.calculate_market_welfare(market, equilibrium)
    Print("Consumer surplus: " + welfare.consumer_surplus)
    Print("Producer surplus: " + welfare.producer_surplus)
    Print("Total welfare: " + welfare.total_welfare)
```

### Game Theory Analysis

```runa
Process called "analyze_prisoners_dilemma" that returns Void:
    Note: Create 2x2 game structure
    Let game be Economics.create_matrix_game(2)
    
    Note: Define strategies
    Economics.set_strategies(game, "Player1", ["Cooperate", "Defect"])
    Economics.set_strategies(game, "Player2", ["Cooperate", "Defect"])
    
    Note: Set payoff matrix
    Economics.set_payoffs(game, "Player1", Matrix[Float].from_arrays([
        [3.0, 0.0],    Note: [Coop,Coop], [Coop,Defect]
        [5.0, 1.0]     Note: [Defect,Coop], [Defect,Defect]
    ]))
    
    Economics.set_payoffs(game, "Player2", Matrix[Float].from_arrays([
        [3.0, 5.0],    Note: [Coop,Coop], [Coop,Defect]  
        [0.0, 1.0]     Note: [Defect,Coop], [Defect,Defect]
    ]))
    
    Note: Find Nash equilibria
    Let equilibria be Economics.find_nash_equilibria(game)
    For Each equilibrium in equilibria:
        Print("Nash equilibrium: " + equilibrium.strategy_profile)
        Print("Expected payoffs: " + equilibrium.expected_payoffs)
```

### Auction Modeling

```runa
Process called "simulate_first_price_auction" that returns Void:
    Note: Create auction with 5 bidders
    Let auction be Economics.create_first_price_auction(5)
    
    Note: Set bidder valuations (private values)
    Let valuations be [10.0, 15.0, 12.0, 18.0, 8.0]
    Economics.set_bidder_valuations(auction, valuations)
    
    Note: Calculate optimal bidding strategies
    Let strategies be Economics.calculate_optimal_bids(auction)
    Print("Optimal bidding strategies:")
    For i in 0 to strategies.length - 1:
        Print("  Bidder " + (i+1) + ": bid " + strategies[i] + " (value " + valuations[i] + ")")
    
    Note: Simulate auction outcome
    Let outcome be Economics.simulate_auction_outcome(auction, strategies)
    Print("Winning bidder: " + outcome.winner)
    Print("Winning bid: " + outcome.winning_bid)
    Print("Seller revenue: " + outcome.revenue)
    Print("Winner's surplus: " + (outcome.winner_valuation - outcome.winning_bid))
```

## Advanced Implementations

### Dynamic Programming in Economics

```runa
Process called "solve_optimal_consumption" that returns Void:
    Note: Infinite horizon consumption problem
    Let time_horizon be 50
    Let discount_factor be 0.95
    Let interest_rate be 0.03
    
    Note: Utility function: U(c) = c^(1-σ)/(1-σ)
    Let risk_aversion be 2.0
    Let utility_function be Economics.create_crra_utility(risk_aversion)
    
    Note: Create dynamic programming problem
    Let consumption_problem be Economics.create_consumption_problem(
        utility: utility_function,
        discount_factor: discount_factor,
        interest_rate: interest_rate,
        initial_wealth: 100.0
    )
    
    Note: Solve using value function iteration
    Let value_function be Economics.solve_value_function_iteration(
        problem: consumption_problem,
        max_iterations: 1000,
        tolerance: 1e-6
    )
    
    Note: Extract optimal policy
    Let policy_function be Economics.extract_policy_function(value_function)
    
    Note: Simulate optimal consumption path
    Let consumption_path be Economics.simulate_consumption_path(
        policy: policy_function,
        initial_wealth: 100.0,
        periods: time_horizon
    )
    
    Print("Optimal consumption path:")
    For i in 0 to consumption_path.length - 1:
        Print("Period " + i + ": consume " + consumption_path[i])
```

### General Equilibrium Analysis

```runa
Process called "compute_general_equilibrium" that returns Void:
    Note: Create 2-good, 2-agent exchange economy
    Let economy be Economics.create_exchange_economy(
        goods: ["Good1", "Good2"],
        agents: ["Agent1", "Agent2"]
    )
    
    Note: Set agent preferences (Cobb-Douglas)
    Economics.set_utility_function(economy, "Agent1", 
        Economics.create_cobb_douglas_utility([0.6, 0.4]))
    Economics.set_utility_function(economy, "Agent2", 
        Economics.create_cobb_douglas_utility([0.3, 0.7]))
    
    Note: Set initial endowments
    Economics.set_endowments(economy, "Agent1", Dictionary[String, Float].from_pairs([
        ("Good1", 10.0),
        ("Good2", 5.0)
    ]))
    Economics.set_endowments(economy, "Agent2", Dictionary[String, Float].from_pairs([
        ("Good1", 5.0),
        ("Good2", 10.0)
    ]))
    
    Note: Find Walrasian equilibrium
    Let equilibrium be Economics.find_walrasian_equilibrium(economy)
    
    Print("Equilibrium prices:")
    For Each good in equilibrium.prices.keys():
        Print("  " + good + ": " + equilibrium.prices[good])
    
    Print("Equilibrium allocations:")
    For Each agent in equilibrium.allocations.keys():
        Print("  " + agent + ": " + equilibrium.allocations[agent])
    
    Note: Check Pareto efficiency
    Let efficiency_check be Economics.check_pareto_efficiency(equilibrium)
    Print("Pareto efficient: " + efficiency_check.is_efficient)
```

### Mechanism Design

```runa
Process called "design_optimal_auction" that returns Void:
    Note: Design auction for single item with two bidders
    Let num_bidders be 2
    Let valuation_distribution be Economics.create_uniform_distribution(0.0, 1.0)
    
    Note: Create mechanism design problem
    Let mechanism_problem be Economics.create_auction_design_problem(
        num_bidders: num_bidders,
        valuation_dist: valuation_distribution,
        reserve_constraint: true
    )
    
    Note: Find optimal mechanism (Myerson auction)
    Let optimal_mechanism be Economics.solve_optimal_auction(mechanism_problem)
    
    Print("Optimal reserve price: " + optimal_mechanism.reserve_price)
    Print("Expected revenue: " + optimal_mechanism.expected_revenue)
    
    Note: Compare with standard auctions
    Let first_price be Economics.analyze_first_price_auction(mechanism_problem)
    Let second_price be Economics.analyze_second_price_auction(mechanism_problem)
    
    Print("Revenue comparison:")
    Print("  Optimal mechanism: " + optimal_mechanism.expected_revenue)
    Print("  First-price auction: " + first_price.expected_revenue)
    Print("  Second-price auction: " + second_price.expected_revenue)
    
    Note: Revenue equivalence verification
    If Mathematics.abs(first_price.expected_revenue - second_price.expected_revenue) < 1e-6:
        Print("Revenue equivalence verified")
```

### Behavioral Economics

```runa
Process called "model_prospect_theory" that returns Void:
    Note: Implement Kahneman-Tversky prospect theory
    Let prospect_parameters be Economics.create_prospect_theory_parameters(
        loss_aversion: 2.25,
        risk_aversion_gains: 0.88,
        risk_aversion_losses: 0.88,
        probability_weighting_gains: 0.65,
        probability_weighting_losses: 0.69
    )
    
    Note: Define decision scenarios
    Let scenarios be List[DecisionScenario].from_array([
        Economics.create_scenario(
            name: "Insurance Decision",
            options: [
                Economics.create_lottery([(-1000.0, 0.01), (0.0, 0.99)]),  Note: No insurance
                Economics.create_lottery([(-10.0, 1.0)])  Note: Buy insurance
            ]
        ),
        Economics.create_scenario(
            name: "Investment Decision", 
            options: [
                Economics.create_lottery([(0.0, 1.0)]),  Note: Safe asset
                Economics.create_lottery([(1000.0, 0.5), (-500.0, 0.5)])  Note: Risky asset
            ]
        )
    ])
    
    Note: Calculate prospect values
    For Each scenario in scenarios:
        Print("Scenario: " + scenario.name)
        For i in 0 to scenario.options.length - 1:
            Let prospect_value be Economics.calculate_prospect_value(
                lottery: scenario.options[i],
                parameters: prospect_parameters
            )
            Print("  Option " + (i+1) + " prospect value: " + prospect_value)
        
        Let preferred_option be Economics.find_preferred_option(scenario, prospect_parameters)
        Print("  Preferred option: " + preferred_option)
```

### Industrial Organization

```runa
Process called "analyze_oligopoly_competition" that returns Void:
    Note: Cournot duopoly with linear demand
    Let market_demand be Economics.create_linear_demand(100.0, 1.0)  Note: P = 100 - Q
    Let marginal_costs be [10.0, 20.0]  Note: Different cost structures
    
    Note: Solve Cournot equilibrium
    Let cournot_equilibrium be Economics.solve_cournot_equilibrium(
        demand: market_demand,
        costs: marginal_costs
    )
    
    Print("Cournot equilibrium:")
    Print("  Firm 1 quantity: " + cournot_equilibrium.quantities[0])
    Print("  Firm 2 quantity: " + cournot_equilibrium.quantities[1])
    Print("  Market price: " + cournot_equilibrium.price)
    Print("  Firm profits: " + cournot_equilibrium.profits)
    
    Note: Compare with Bertrand competition
    Let bertrand_equilibrium be Economics.solve_bertrand_equilibrium(
        demand: market_demand,
        costs: marginal_costs
    )
    
    Print("Bertrand equilibrium:")
    Print("  Prices: " + bertrand_equilibrium.prices)
    Print("  Market shares: " + bertrand_equilibrium.market_shares)
    Print("  Profits: " + bertrand_equilibrium.profits)
    
    Note: Analyze merger effects
    Let merger_analysis be Economics.analyze_merger_effects(
        pre_merger_equilibrium: cournot_equilibrium,
        market_structure: "cournot"
    )
    Print("Merger analysis:")
    Print("  Price change: " + merger_analysis.price_change)
    Print("  Consumer welfare change: " + merger_analysis.welfare_change)
```

### Econometric Modeling

```runa
Process called "estimate_demand_function" that returns Void:
    Note: Load price and quantity data
    Let market_data be Economics.load_market_data("market_observations.csv")
    
    Note: Estimate linear demand: Q = α + βP + γY + ε
    Let demand_specification be Economics.create_demand_specification([
        "price",
        "income", 
        "population",
        "substitute_price"
    ])
    
    Note: Handle endogeneity using instrumental variables
    Let instruments be ["supply_cost_shifters", "weather_variables"]
    Let iv_estimation be Economics.estimate_instrumental_variables(
        specification: demand_specification,
        instruments: instruments,
        data: market_data
    )
    
    Print("Demand estimation results:")
    Print("  Price elasticity: " + iv_estimation.coefficients["price"])
    Print("  Income elasticity: " + iv_estimation.coefficients["income"])
    Print("  R-squared: " + iv_estimation.r_squared)
    Print("  F-statistic: " + iv_estimation.f_statistic)
    
    Note: Test for structural breaks
    Let stability_test be Economics.test_parameter_stability(iv_estimation, market_data)
    Print("Parameter stability test p-value: " + stability_test.p_value)
    
    Note: Forecast demand
    Let forecast_scenarios be Dictionary[String, Float].from_pairs([
        ("price", 15.0),
        ("income", 50000.0),
        ("population", 1000000.0),
        ("substitute_price", 12.0)
    ])
    
    Let demand_forecast be Economics.forecast_demand(iv_estimation, forecast_scenarios)
    Print("Forecasted demand: " + demand_forecast.point_estimate)
    Print("95% confidence interval: [" + demand_forecast.lower_bound + ", " + demand_forecast.upper_bound + "]")
```

## Error Handling and Validation

### Model Validation

```runa
Process called "validate_economic_model" that takes model as EconomicModel returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check utility function properties
    If model.has_utility_functions():
        For Each agent in model.agents:
            Let utility be model.get_utility_function(agent)
            If not Economics.is_monotone_increasing(utility):
                validation.add_warning("Non-monotone utility for agent: " + agent)
            
            If not Economics.is_quasi_concave(utility):
                validation.add_warning("Non-quasi-concave utility for agent: " + agent)
    
    Note: Check market structure validity
    If model.has_market_structure():
        Let demand be model.demand_function
        Let supply be model.supply_function
        
        If not Economics.has_negative_slope(demand):
            validation.add_error("Demand function must have negative slope")
        
        If not Economics.has_positive_slope(supply):
            validation.add_error("Supply function must have positive slope")
    
    Note: Check equilibrium existence
    If not Economics.equilibrium_exists(model):
        validation.add_error("No equilibrium exists for this model")
    
    Return validation
```

### Data Quality Checks

```runa
Process called "validate_auction_data" that takes bids as List[Bid] returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check bid validity
    For Each bid in bids:
        If bid.amount <= 0.0:
            validation.add_error("Negative or zero bids not allowed")
        
        If bid.bidder_id.is_empty():
            validation.add_error("Bidder ID cannot be empty")
    
    Note: Check for collusion patterns
    Let collusion_test be Economics.test_for_collusion(bids)
    If collusion_test.suspicious_patterns.length > 0:
        validation.add_warning("Potential collusion detected: " + collusion_test.description)
    
    Note: Validate reservation prices
    Let reservation_analysis be Economics.analyze_reservation_behavior(bids)
    If reservation_analysis.implausible_reservations.length > 0:
        validation.add_warning("Implausible reservation price patterns detected")
    
    Return validation
```

## Performance Optimization

### Efficient Equilibrium Computation

```runa
Process called "optimize_equilibrium_computation" that takes model as EconomicModel returns OptimizedModel:
    Let optimized be OptimizedModel.create(model)
    
    Note: Use sparse matrix methods for large games
    If model.is_large_game() and model.has_sparse_structure():
        optimized.enable_sparse_matrix_operations()
        optimized.set_solver("conjugate_gradient")
    
    Note: Parallelize agent computations
    If model.agents.length > System.get_cpu_count():
        optimized.enable_parallel_agent_computation()
    
    Note: Use specialized solvers for specific structures
    If model.is_potential_game():
        optimized.set_solver("potential_maximization")
    Otherwise If model.is_supermodular_game():
        optimized.set_solver("tarski_iteration")
    
    Return optimized
```

### Memory-Efficient Simulation

```runa
Process called "optimize_monte_carlo_simulation" that takes simulation_params as SimulationParameters returns OptimizedSimulation:
    Let optimized be OptimizedSimulation.create(simulation_params)
    
    Note: Use streaming algorithms for large simulations
    If simulation_params.num_simulations > 1000000:
        optimized.enable_streaming_computation()
        optimized.set_batch_size(10000)
    
    Note: Implement variance reduction techniques
    optimized.enable_antithetic_variates()
    optimized.enable_control_variates()
    
    Note: Use adaptive sampling
    If simulation_params.requires_precision():
        optimized.enable_adaptive_sampling()
        optimized.set_convergence_criterion("relative_error", 0.01)
    
    Return optimized
```

## Related Documentation

- **[Mathematical Physics](physics.md)** - Physical system modeling
- **[Mathematical Biology](biology.md)** - Population and evolutionary dynamics
- **[Operations Research](operations.md)** - Optimization and decision theory
- **[Statistics Module](../statistics/README.md)** - Statistical inference
- **[Probability Module](../probability/README.md)** - Stochastic modeling
- **[Optimization Module](../optimization/README.md)** - Mathematical optimization
- **[Linear Algebra Module](../core/linear_algebra.md)** - Matrix computations
- **[Game Theory Module](../discrete/games.md)** - Strategic interactions
- **[Financial Mathematics](../financial/README.md)** - Financial modeling

## Further Reading

- Microeconomic Theory (Mas-Colell, Whinston, Green)
- Game Theory (Fudenberg & Tirole)
- Mechanism Design Theory
- Industrial Organization Economics
- Behavioral Economics and Finance
- Econometric Methods
- Computational Economics
- Experimental Economics