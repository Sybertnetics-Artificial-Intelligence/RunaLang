# Operations Research Module

## Overview

The operations research module provides comprehensive tools for optimization, decision analysis, queuing theory, inventory management, scheduling, network flows, and resource allocation. This module implements mathematical models and algorithms for solving complex operational problems in business, engineering, logistics, and management science.

## Mathematical Foundation

### Linear Programming

**Standard Form:**
```
minimize: c^T x
subject to: Ax = b, x ≥ 0
```

**Dual Problem:**
```
maximize: b^T y
subject to: A^T y ≤ c
```

**Duality Theorem:** Strong duality holds when both primal and dual are feasible.

### Integer Programming

**Binary Integer Programming:**
```
minimize: c^T x
subject to: Ax ≤ b, x ∈ {0,1}^n
```

**Mixed Integer Programming:**
```
minimize: c^T x + d^T y  
subject to: Ax + By ≤ b, x ∈ ℝ^n, y ∈ ℤ^m
```

### Queuing Theory

**M/M/1 Queue:**
- Arrival rate: λ
- Service rate: μ  
- Utilization: ρ = λ/μ < 1
- Average number in system: L = ρ/(1-ρ)
- Average waiting time: W = ρ/(μ(1-ρ))

**M/M/c Queue:**
- c servers
- Traffic intensity: ρ = λ/(cμ)

### Network Flows

**Max Flow Problem:**
```
maximize: Σ f(s,v) for v ∈ V
subject to: capacity and conservation constraints
```

**Min Cost Flow:**
```
minimize: Σ c(u,v) * f(u,v)
subject to: flow conservation and capacity constraints
```

## Core Data Structures

### Linear Program
```runa
Type called "LinearProgram":
    objective_coefficients as Vector[Float]
    constraint_matrix as Matrix[Float]
    constraint_bounds as Vector[Float]
    variable_bounds as List[Tuple[Float, Float]]
    optimization_sense as OptimizationSense
    solution_status as SolutionStatus
    optimal_value as Float
    optimal_solution as Vector[Float]
```

### Queue Model
```runa
Type called "QueueModel":
    arrival_process as ArrivalProcess
    service_process as ServiceProcess
    number_of_servers as Integer
    queue_capacity as Integer
    queue_discipline as QueueDiscipline
    performance_measures as QueuePerformance
    steady_state_probabilities as Vector[Float]
```

### Network Graph
```runa
Type called "NetworkGraph":
    nodes as List[NetworkNode]
    edges as List[NetworkEdge]
    node_properties as Dictionary[String, Dictionary[String, Float]]
    edge_properties as Dictionary[String, Dictionary[String, Float]]
    adjacency_matrix as Matrix[Float]
    incidence_matrix as Matrix[Float]
```

### Inventory System
```runa
Type called "InventorySystem":
    demand_pattern as DemandPattern
    lead_time as Float
    holding_cost as Float
    ordering_cost as Float
    shortage_cost as Float
    service_level as Float
    inventory_policy as InventoryPolicy
    safety_stock as Float
```

## Basic Usage

### Linear Programming

```runa
Import "runa/src/stdlib/math/applied/operations"

Process called "solve_production_planning" that returns Void:
    Note: Maximize profit: 3x₁ + 2x₂
    Note: Subject to: 2x₁ + x₂ ≤ 100, x₁ + 2x₂ ≤ 80, x₁,x₂ ≥ 0
    
    Let lp be Operations.create_linear_program()
    
    Note: Set objective function (maximize profit)
    Operations.set_objective(lp, [3.0, 2.0], OptimizationSense.Maximize)
    
    Note: Add constraints
    Operations.add_constraint(lp, [2.0, 1.0], ConstraintType.LessThanOrEqual, 100.0)
    Operations.add_constraint(lp, [1.0, 2.0], ConstraintType.LessThanOrEqual, 80.0)
    
    Note: Set variable bounds (non-negativity)
    Operations.set_variable_bounds(lp, 0, 0.0, Float.infinity())
    Operations.set_variable_bounds(lp, 1, 0.0, Float.infinity())
    
    Note: Solve using simplex method
    Let solution be Operations.solve_simplex(lp)
    
    If solution.status == SolutionStatus.Optimal:
        Print("Optimal solution found:")
        Print("  x₁ = " + solution.variables[0])
        Print("  x₂ = " + solution.variables[1])
        Print("  Maximum profit = " + solution.objective_value)
        
        Note: Perform sensitivity analysis
        Let sensitivity be Operations.perform_sensitivity_analysis(lp, solution)
        Print("Shadow prices: " + sensitivity.shadow_prices)
        Print("Reduced costs: " + sensitivity.reduced_costs)
```

### Queuing Analysis

```runa
Process called "analyze_service_system" that returns Void:
    Note: M/M/2 queue: Poisson arrivals, exponential service, 2 servers
    Let queue be Operations.create_mm2_queue(
        arrival_rate: 8.0,    Note: 8 customers per hour
        service_rate: 5.0     Note: 5 customers per hour per server
    )
    
    Note: Calculate performance measures
    Let performance be Operations.calculate_queue_performance(queue)
    
    Print("Queue Performance Measures:")
    Print("  Utilization (ρ): " + performance.utilization)
    Print("  Average number in system (L): " + performance.average_in_system)
    Print("  Average number in queue (Lq): " + performance.average_in_queue)
    Print("  Average waiting time (W): " + performance.average_waiting_time)
    Print("  Average time in queue (Wq): " + performance.average_queue_time)
    Print("  Probability of waiting: " + performance.probability_of_waiting)
    
    Note: Analyze different scenarios
    Let scenarios be [6.0, 8.0, 10.0, 12.0]  Note: Different arrival rates
    Print("Scenario Analysis:")
    For Each lambda in scenarios:
        Let scenario_queue be Operations.create_mm2_queue(lambda, 5.0)
        Let scenario_perf be Operations.calculate_queue_performance(scenario_queue)
        Print("  λ=" + lambda + ": W=" + scenario_perf.average_waiting_time)
```

### Network Flow Optimization

```runa
Process called "solve_transportation_problem" that returns Void:
    Note: 3 suppliers, 4 customers transportation problem
    Let suppliers be ["Factory1", "Factory2", "Factory3"]
    Let customers be ["Store1", "Store2", "Store3", "Store4"]
    
    Note: Supply capacities
    Let supply be Dictionary[String, Float].from_pairs([
        ("Factory1", 300.0),
        ("Factory2", 400.0), 
        ("Factory3", 500.0)
    ])
    
    Note: Demand requirements
    Let demand be Dictionary[String, Float].from_pairs([
        ("Store1", 250.0),
        ("Store2", 350.0),
        ("Store3", 400.0),
        ("Store4", 200.0)
    ])
    
    Note: Transportation costs (per unit)
    Let costs be Operations.create_cost_matrix(suppliers.length, customers.length)
    Operations.set_cost(costs, 0, 0, 8.0)   Note: Factory1 -> Store1
    Operations.set_cost(costs, 0, 1, 6.0)   Note: Factory1 -> Store2
    Note: ... set all costs
    
    Note: Create transportation network
    Let transport_network be Operations.create_transportation_network(
        suppliers: suppliers,
        customers: customers,
        supply: supply,
        demand: demand,
        costs: costs
    )
    
    Note: Solve using network simplex
    Let transport_solution be Operations.solve_transportation(transport_network)
    
    Print("Optimal transportation plan:")
    Print("  Total cost: " + transport_solution.total_cost)
    For Each route in transport_solution.routes:
        If route.flow > 0.0:
            Print("  " + route.from + " -> " + route.to + ": " + route.flow + " units")
```

## Advanced Implementations

### Integer Programming with Branch and Bound

```runa
Process called "solve_facility_location" that returns Void:
    Note: Binary facility location problem
    Note: Minimize: Σ fixed_costs[i] * y[i] + Σ transport_costs[i][j] * x[i][j]
    Note: Subject to: facility capacity and demand satisfaction constraints
    
    Let facilities be 5
    Let customers be 10
    
    Note: Fixed costs for opening facilities
    Let fixed_costs be [1000.0, 1200.0, 800.0, 1500.0, 900.0]
    
    Note: Transportation costs
    Let transport_costs be Operations.create_random_cost_matrix(facilities, customers, 10.0, 50.0)
    
    Note: Facility capacities
    Let capacities be [100.0, 150.0, 80.0, 200.0, 120.0]
    
    Note: Customer demands  
    Let demands be [15.0, 25.0, 10.0, 30.0, 20.0, 12.0, 18.0, 22.0, 16.0, 14.0]
    
    Note: Create mixed integer program
    Let mip be Operations.create_facility_location_mip(
        facilities: facilities,
        customers: customers,
        fixed_costs: fixed_costs,
        transport_costs: transport_costs,
        capacities: capacities,
        demands: demands
    )
    
    Note: Solve using branch and bound
    Let solution be Operations.solve_branch_and_bound(mip)
    
    Print("Optimal facility location solution:")
    Print("  Total cost: " + solution.objective_value)
    Print("  Facilities to open:")
    For i in 0 to facilities - 1:
        If solution.facility_decisions[i] > 0.5:  Note: Binary variable
            Print("    Facility " + (i+1) + " (cost: " + fixed_costs[i] + ")")
    
    Note: Display customer assignments
    Print("  Customer assignments:")
    For j in 0 to customers - 1:
        For i in 0 to facilities - 1:
            If solution.assignment_variables[i][j] > 0.01:
                Print("    Customer " + (j+1) + " <- Facility " + (i+1) + 
                      " (" + solution.assignment_variables[i][j] + " units)")
```

### Dynamic Programming

```runa
Process called "solve_inventory_optimization" that returns Void:
    Note: Multi-period inventory problem with stochastic demand
    Let periods be 12  Note: 12 months
    Let max_inventory be 1000.0
    Let holding_cost be 2.0  Note: Cost per unit per period
    Let ordering_cost be 50.0  Note: Fixed cost per order
    
    Note: Demand distribution for each period (seasonal)
    Let demand_means be [80.0, 85.0, 90.0, 95.0, 100.0, 110.0, 
                        120.0, 115.0, 105.0, 95.0, 85.0, 80.0]
    Let demand_std be 15.0
    
    Note: Create stochastic demand processes
    Let demand_distributions be List[ProbabilityDistribution].create()
    For Each mean_demand in demand_means:
        demand_distributions.add(Operations.create_normal_distribution(mean_demand, demand_std))
    
    Note: Set up dynamic programming problem
    Let dp_problem be Operations.create_stochastic_inventory_dp(
        periods: periods,
        max_inventory: max_inventory,
        holding_cost: holding_cost,
        ordering_cost: ordering_cost,
        demand_distributions: demand_distributions
    )
    
    Note: Solve using backward induction
    Let dp_solution be Operations.solve_stochastic_dp(dp_problem)
    
    Print("Optimal inventory policy:")
    For period in 0 to periods - 1:
        Let policy be dp_solution.policies[period]
        Print("Period " + (period + 1) + ":")
        Print("  Order up to level: " + policy.order_up_to_level)
        Print("  Expected cost: " + policy.expected_cost)
```

### Metaheuristic Optimization

```runa
Process called "solve_vehicle_routing_with_genetic_algorithm" that returns Void:
    Note: Vehicle Routing Problem with capacity constraints
    Let customers be 20
    Let vehicles be 3
    Let vehicle_capacity be 100.0
    
    Note: Generate random customer locations and demands
    Let customer_locations be Operations.generate_random_locations(customers, 50.0, 50.0)
    Let customer_demands be Operations.generate_random_demands(customers, 5.0, 25.0)
    
    Note: Calculate distance matrix
    Let distance_matrix be Operations.calculate_euclidean_distances(customer_locations)
    
    Note: Create VRP instance
    Let vrp_instance be Operations.create_vrp_instance(
        customers: customers,
        vehicles: vehicles,
        capacity: vehicle_capacity,
        distances: distance_matrix,
        demands: customer_demands
    )
    
    Note: Configure genetic algorithm
    Let ga_params be Operations.create_genetic_algorithm_parameters(
        population_size: 100,
        generations: 500,
        crossover_rate: 0.8,
        mutation_rate: 0.1,
        elite_size: 10
    )
    
    Note: Solve using genetic algorithm
    Let ga_solution be Operations.solve_vrp_genetic_algorithm(vrp_instance, ga_params)
    
    Print("Vehicle Routing Solution:")
    Print("  Total distance: " + ga_solution.total_distance)
    Print("  Number of vehicles used: " + ga_solution.routes.length)
    
    For i in 0 to ga_solution.routes.length - 1:
        Let route be ga_solution.routes[i]
        Print("  Vehicle " + (i+1) + " route:")
        Print("    Customers: " + route.customer_sequence)
        Print("    Total demand: " + route.total_demand)
        Print("    Route distance: " + route.total_distance)
```

### Simulation Optimization

```runa
Process called "optimize_manufacturing_system" that returns Void:
    Note: Discrete event simulation of manufacturing line
    Let workstations be 5
    Let simulation_time be 8760.0  Note: One year in hours
    
    Note: Decision variables: buffer sizes between stations
    Let buffer_sizes be [10, 15, 20, 12, 8]  Note: Initial values
    
    Note: Create simulation model
    Let manufacturing_model be Operations.create_manufacturing_simulation(
        workstations: workstations,
        buffer_sizes: buffer_sizes,
        processing_times: [2.0, 1.8, 2.2, 1.9, 2.1],  Note: Average processing times
        failure_rates: [0.01, 0.015, 0.008, 0.012, 0.01],  Note: Failures per hour
        repair_times: [30.0, 45.0, 25.0, 35.0, 40.0]  Note: Average repair times
    )
    
    Note: Use simulation-based optimization
    Let optimization_problem be Operations.create_simulation_optimization_problem(
        simulation_model: manufacturing_model,
        objective: "maximize_throughput",
        constraints: [
            Operations.create_constraint("total_buffer_cost", "<=", 50000.0),
            Operations.create_constraint("space_constraint", "<=", 1000.0)
        ]
    )
    
    Note: Solve using simulated annealing
    Let sa_params be Operations.create_simulated_annealing_parameters(
        initial_temperature: 1000.0,
        cooling_rate: 0.95,
        min_temperature: 1.0,
        iterations_per_temperature: 50
    )
    
    Let optimal_config be Operations.solve_simulation_optimization(
        problem: optimization_problem,
        method: "simulated_annealing",
        parameters: sa_params,
        replications: 10  Note: Number of simulation runs per evaluation
    )
    
    Print("Optimal manufacturing configuration:")
    Print("  Buffer sizes: " + optimal_config.buffer_sizes)
    Print("  Expected throughput: " + optimal_config.throughput + " units/hour")
    Print("  Total cost: " + optimal_config.total_cost)
    Print("  System utilization: " + optimal_config.utilization)
```

### Robust Optimization

```runa
Process called "solve_robust_portfolio_optimization" that returns Void:
    Note: Robust portfolio optimization under return uncertainty
    Let assets be 10
    Let risk_aversion be 3.0
    
    Note: Nominal expected returns
    Let nominal_returns be [0.08, 0.12, 0.10, 0.15, 0.09, 0.11, 0.07, 0.13, 0.14, 0.06]
    
    Note: Return uncertainty set (ellipsoidal)
    Let uncertainty_matrix be Operations.create_covariance_matrix(assets)
    Let uncertainty_level be 0.1  Note: 10% uncertainty level
    
    Note: Historical covariance matrix
    Let covariance_matrix be Operations.estimate_covariance_matrix("historical_returns.csv")
    
    Note: Create robust optimization problem
    Let robust_problem be Operations.create_robust_portfolio_problem(
        assets: assets,
        nominal_returns: nominal_returns,
        covariance_matrix: covariance_matrix,
        uncertainty_set: Operations.create_ellipsoidal_uncertainty(
            center: nominal_returns,
            shape_matrix: uncertainty_matrix,
            radius: uncertainty_level
        ),
        risk_aversion: risk_aversion
    )
    
    Note: Solve robust counterpart
    Let robust_solution be Operations.solve_robust_optimization(robust_problem)
    
    Print("Robust portfolio allocation:")
    For i in 0 to assets - 1:
        If robust_solution.weights[i] > 0.01:
            Print("  Asset " + (i+1) + ": " + (robust_solution.weights[i] * 100.0) + "%")
    
    Print("Expected return (worst case): " + robust_solution.worst_case_return)
    Print("Portfolio risk: " + robust_solution.portfolio_risk)
    
    Note: Compare with non-robust solution
    Let standard_solution be Operations.solve_mean_variance_optimization(
        returns: nominal_returns,
        covariance: covariance_matrix,
        risk_aversion: risk_aversion
    )
    
    Print("Comparison with non-robust portfolio:")
    Print("  Robust expected return: " + robust_solution.expected_return)
    Print("  Standard expected return: " + standard_solution.expected_return)
    Print("  Robust risk: " + robust_solution.portfolio_risk)
    Print("  Standard risk: " + standard_solution.portfolio_risk)
```

## Error Handling and Validation

### Model Validation

```runa
Process called "validate_optimization_model" that takes model as OptimizationModel returns ValidationResult:
    Let validation be ValidationResult.create()
    
    Note: Check problem feasibility
    If not Operations.check_feasibility(model):
        validation.add_error("Problem is infeasible")
        Return validation
    
    Note: Check for unbounded solutions
    If Operations.is_unbounded(model):
        validation.add_error("Problem is unbounded")
    
    Note: Validate constraint structure
    If model.constraint_matrix.rank() < model.constraint_matrix.rows:
        validation.add_warning("Redundant constraints detected")
    
    Note: Check numerical stability
    Let condition_number be Operations.calculate_condition_number(model.constraint_matrix)
    If condition_number > 1e12:
        validation.add_warning("Poor numerical conditioning (condition number: " + condition_number + ")")
    
    Note: Validate bounds
    For i in 0 to model.variable_bounds.length - 1:
        If model.variable_bounds[i].lower > model.variable_bounds[i].upper:
            validation.add_error("Invalid bounds for variable " + i)
    
    Return validation
```

### Solution Quality Assessment

```runa
Process called "assess_solution_quality" that takes solution as OptimizationSolution returns QualityAssessment:
    Let assessment be QualityAssessment.create()
    
    Note: Check optimality conditions
    If solution.method == "simplex":
        Let optimality_check be Operations.check_kkt_conditions(solution)
        assessment.kkt_satisfied = optimality_check.satisfied
        assessment.complementary_slackness = optimality_check.complementary_slackness
    
    Note: Assess numerical accuracy
    Let constraint_violations be Operations.calculate_constraint_violations(solution)
    assessment.max_constraint_violation = constraint_violations.max()
    assessment.constraint_feasibility = (assessment.max_constraint_violation < 1e-6)
    
    Note: Calculate solution statistics
    assessment.objective_value = solution.objective_value
    assessment.solve_time = solution.solve_time
    assessment.iterations = solution.iterations
    
    Note: Sensitivity analysis
    If solution.has_sensitivity_information():
        assessment.shadow_prices = solution.shadow_prices
        assessment.reduced_costs = solution.reduced_costs
        assessment.ranges = solution.sensitivity_ranges
    
    Return assessment
```

## Performance Optimization

### Specialized Solvers

```runa
Process called "select_optimal_solver" that takes problem as OptimizationProblem returns SolverConfiguration:
    Let config be SolverConfiguration.create()
    
    Note: Analyze problem structure
    If Operations.is_network_flow_problem(problem):
        config.set_solver("network_simplex")
        config.set_parameters(Dictionary[String, Any].from_pairs([
            ("pivot_rule", "first_improving"),
            ("scaling", true)
        ]))
    Otherwise If Operations.has_special_structure(problem, "transportation"):
        config.set_solver("transportation_simplex")
    Otherwise If Operations.is_integer_program(problem):
        If problem.variables.length < 1000:
            config.set_solver("branch_and_bound")
        Otherwise:
            config.set_solver("cutting_planes")
        config.set_parameters(Dictionary[String, Any].from_pairs([
            ("branching_strategy", "most_fractional"),
            ("cut_generation", true)
        ]))
    Otherwise:
        config.set_solver("dual_simplex")
    
    Note: Set numerical parameters based on problem scale
    If problem.constraint_matrix.rows > 10000:
        config.enable_sparse_matrix_operations()
        config.set_parameter("numerical_tolerance", 1e-8)
    
    Return config
```

### Parallel Processing

```runa
Process called "parallelize_optimization" that takes problems as List[OptimizationProblem] returns List[OptimizationSolution]:
    Let num_cores be System.get_cpu_count()
    Let solutions be List[OptimizationSolution].create()
    
    Note: Distribute problems across cores
    Parallel.for_each(problems, problem => {
        Let solver_config be Operations.select_optimal_solver(problem)
        Let solution be Operations.solve_with_config(problem, solver_config)
        solutions.add_thread_safe(solution)
    })
    
    Return solutions
```

## Related Documentation

- **[Mathematical Physics](physics.md)** - Physical optimization problems
- **[Mathematical Economics](economics.md)** - Economic optimization models
- **[Mathematical Biology](biology.md)** - Biological optimization applications
- **[Engineering Mathematics](engineering.md)** - Engineering optimization
- **[Optimization Module](../optimization/README.md)** - Core optimization algorithms
- **[Linear Algebra Module](../core/linear_algebra.md)** - Matrix computations
- **[Statistics Module](../statistics/README.md)** - Statistical optimization
- **[Probability Module](../probability/README.md)** - Stochastic optimization
- **[Graph Theory](../discrete/graphs.md)** - Network optimization
- **[Numerical Methods](../core/numerical.md)** - Computational algorithms

## Further Reading

- Linear and Nonlinear Programming (Luenberger & Ye)
- Introduction to Operations Research (Hillier & Lieberman)
- Network Flows (Ahuja, Magnanti & Orlin)
- Integer Programming (Wolsey)
- Stochastic Programming (Birge & Louveaux)
- Metaheuristics: From Design to Implementation
- Simulation Modeling and Analysis (Law)
- Robust Optimization (Ben-Tal, El Ghaoui & Nemirovski)