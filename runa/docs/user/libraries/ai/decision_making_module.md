# Decision Making Systems Module

## Overview

The Decision Making Systems module provides comprehensive automated decision-making capabilities for the Runa AI framework. This enterprise-grade decision infrastructure includes decision trees, multi-criteria analysis, probabilistic decision making, and utility-based reasoning with performance competitive with leading decision support systems.

## Quick Start

```runa
Import "ai.decision.core" as decision_core
Import "ai.decision.trees" as decision_trees

Note: Create a simple decision system
Let decision_config be dictionary with:
    "decision_model" as "utility_based",
    "uncertainty_handling" as "probabilistic",
    "criteria_weighting" as "analytical_hierarchy",
    "learning_enabled" as true

Let decision_system be decision_core.create_decision_system[decision_config]

Note: Define a decision problem
Let decision_problem be dictionary with:
    "problem_type" as "resource_allocation",
    "alternatives" as list containing:
        dictionary with: "id" as "option_a", "name" as "expand_cpu_cluster", "cost" as 50000, "performance_gain" as 0.3,
        dictionary with: "id" as "option_b", "name" as "upgrade_storage", "cost" as 30000, "performance_gain" as 0.2,
        dictionary with: "id" as "option_c", "name" as "optimize_algorithms", "cost" as 10000, "performance_gain" as 0.25
    "criteria" as list containing:
        dictionary with: "name" as "cost_effectiveness", "weight" as 0.4, "type" as "minimize",
        dictionary with: "name" as "performance_impact", "weight" as 0.4, "type" as "maximize",
        dictionary with: "name" as "implementation_speed", "weight" as 0.2, "type" as "maximize"
    "constraints" as dictionary with:
        "budget_limit" as 40000,
        "timeline_weeks" as 8

Note: Make a decision
Let decision_result be decision_core.make_decision[decision_system, decision_problem]
Display "Recommended decision: " with message decision_result["selected_alternative"]["name"]
Display "Confidence: " with message decision_result["confidence"]
```

## Architecture Components

### Decision Models
- **Utility Theory**: Multi-attribute utility functions and optimization
- **Decision Trees**: Hierarchical decision structures with probabilistic branches
- **Game Theory**: Strategic decision making in multi-agent environments
- **Fuzzy Logic**: Decision making under uncertainty and imprecision

### Multi-Criteria Analysis
- **MCDM Methods**: AHP, TOPSIS, ELECTRE, and PROMETHEE implementations
- **Criteria Weighting**: Weight elicitation and sensitivity analysis
- **Alternative Evaluation**: Comprehensive alternative assessment and ranking
- **Trade-off Analysis**: Pareto optimality and trade-off exploration

### Probabilistic Decision Making
- **Bayesian Decision Theory**: Bayesian inference and decision making
- **Decision Networks**: Influence diagrams and belief networks
- **Risk Analysis**: Risk assessment and uncertainty quantification
- **Sequential Decisions**: Dynamic programming and sequential optimization

### Learning and Adaptation
- **Reinforcement Learning**: Q-learning and policy gradient methods
- **Bandit Algorithms**: Multi-armed bandit and contextual bandits
- **Experience Replay**: Learning from historical decisions
- **Meta-Learning**: Learning decision strategies across domains

## API Reference

### Core Decision Functions

#### `create_decision_system[config]`
Creates a decision-making system with specified models and algorithms.

**Parameters:**
- `config` (Dictionary): Decision system configuration with models, algorithms, and learning parameters

**Returns:**
- `DecisionSystem`: Configured decision-making system instance

**Example:**
```runa
Let config be dictionary with:
    "decision_framework" as "hybrid_approach",
    "models" as dictionary with:
        "primary" as "multi_attribute_utility",
        "secondary" as "decision_tree",
        "uncertainty_model" as "bayesian_network"
    "learning_components" as dictionary with:
        "reinforcement_learning" as true,
        "experience_replay" as true,
        "meta_learning" as false
    "optimization" as dictionary with:
        "algorithm" as "genetic_algorithm",
        "population_size" as 100,
        "generations" as 50
    "evaluation_metrics" as list containing "decision_quality", "computation_time", "robustness"

Let decision_system be decision_core.create_decision_system[config]
```

#### `define_decision_problem[system, problem_definition]`
Defines a structured decision problem with alternatives, criteria, and constraints.

**Parameters:**
- `system` (DecisionSystem): Decision system instance
- `problem_definition` (Dictionary): Complete problem specification

**Returns:**
- `DecisionProblem`: Structured decision problem instance

**Example:**
```runa
Let problem_definition be dictionary with:
    "problem_id" as "infrastructure_investment",
    "problem_description" as "Selecting optimal infrastructure investments for AI workloads",
    "decision_maker" as "infrastructure_team",
    "stakeholders" as list containing "engineering", "finance", "operations",
    "alternatives" as list containing:
        dictionary with:
            "id" as "cloud_migration",
            "attributes" as dictionary with:
                "initial_cost" as 100000,
                "monthly_cost" as 15000,
                "scalability" as 0.9,
                "reliability" as 0.95,
                "implementation_time_weeks" as 12
        dictionary with:
            "id" as "on_premise_expansion",
            "attributes" as dictionary with:
                "initial_cost" as 200000,
                "monthly_cost" as 8000,
                "scalability" as 0.6,
                "reliability" as 0.85,
                "implementation_time_weeks" as 20
    "criteria" as list containing:
        dictionary with:
            "name" as "total_cost_of_ownership",
            "weight" as 0.35,
            "type" as "cost",
            "measurement_scale" as "ratio"
        dictionary with:
            "name" as "scalability_rating",
            "weight" as 0.25,
            "type" as "benefit",
            "measurement_scale" as "interval"
        dictionary with:
            "name" as "reliability_score",
            "weight" as 0.25,
            "type" as "benefit",
            "measurement_scale" as "interval"
        dictionary with:
            "name" as "implementation_speed",
            "weight" as 0.15,
            "type" as "benefit",
            "measurement_scale" as "ratio"
    "constraints" as dictionary with:
        "hard_constraints" as list containing:
            dictionary with: "criterion" as "initial_cost", "operator" as "less_than", "value" as 150000,
            dictionary with: "criterion" as "implementation_time_weeks", "operator" as "less_than", "value" as 16
        "soft_constraints" as list containing:
            dictionary with: "criterion" as "reliability_score", "operator" as "greater_than", "value" as 0.8, "penalty" as 0.1

Let decision_problem be decision_core.define_decision_problem[decision_system, problem_definition]
```

#### `make_decision[system, problem, decision_config]`
Makes a decision using the configured decision-making system and problem.

**Parameters:**
- `system` (DecisionSystem): Decision system instance
- `problem` (DecisionProblem): Defined decision problem
- `decision_config` (Dictionary): Decision-making configuration and parameters

**Returns:**
- `DecisionResult`: Comprehensive decision result with recommendations and analysis

**Example:**
```runa
Let decision_config be dictionary with:
    "analysis_depth" as "comprehensive",
    "sensitivity_analysis" as true,
    "robustness_testing" as true,
    "explanation_level" as "detailed",
    "confidence_calculation" as true,
    "alternative_ranking" as true

Let decision_result be decision_core.make_decision[decision_system, decision_problem, decision_config]

Display "Decision Analysis Results:"
Display "  Recommended alternative: " with message decision_result["recommendation"]["alternative_id"]
Display "  Utility score: " with message decision_result["recommendation"]["utility_score"]
Display "  Confidence level: " with message decision_result["confidence"]["overall_confidence"]

Display "Alternative Rankings:"
For each ranking in decision_result["alternative_rankings"]:
    Display "  " with message ranking["rank"] with message ". " with message ranking["alternative_id"]
    Display "     Score: " with message ranking["score"]
    Display "     Key strengths: " with message ranking["strengths"]

If decision_result["sensitivity_analysis"]["significant_changes"]:
    Display "Sensitivity Analysis: Decision is sensitive to weight changes"
    For each sensitivity in decision_result["sensitivity_analysis"]["critical_criteria"]:
        Display "  Critical criterion: " with message sensitivity["criterion_name"]
```

### Decision Tree Functions

#### `create_decision_tree[tree_definition, tree_config]`
Creates a decision tree for structured decision-making processes.

**Parameters:**
- `tree_definition` (Dictionary): Tree structure with nodes, branches, and conditions
- `tree_config` (Dictionary): Tree configuration and evaluation parameters

**Returns:**
- `DecisionTree`: Configured decision tree instance

**Example:**
```runa
Let tree_definition be dictionary with:
    "root_node" as dictionary with:
        "node_id" as "resource_allocation_root",
        "node_type" as "decision",
        "question" as "What is the current system utilization?",
        "branches" as list containing:
            dictionary with:
                "condition" as "utilization < 0.7",
                "child_node" as dictionary with:
                    "node_id" as "low_utilization",
                    "node_type" as "decision",
                    "question" as "Is there pending workload?",
                    "branches" as list containing:
                        dictionary with: "condition" as "pending_workload = true", "outcome" as "scale_up_gradually",
                        dictionary with: "condition" as "pending_workload = false", "outcome" as "maintain_current"
            dictionary with:
                "condition" as "utilization >= 0.7 AND utilization < 0.9",
                "outcome" as "monitor_closely"
            dictionary with:
                "condition" as "utilization >= 0.9",
                "child_node" as dictionary with:
                    "node_id" as "high_utilization",
                    "node_type" as "chance",
                    "question" as "Will additional resources be available?",
                    "probabilities" as dictionary with:
                        "resources_available" as 0.7,
                        "resources_limited" as 0.3
                    "outcomes" as dictionary with:
                        "resources_available" as "scale_up_immediately",
                        "resources_limited" as "optimize_current_workload"

Let tree_config be dictionary with:
    "evaluation_strategy" as "expected_value",
    "pruning_enabled" as true,
    "uncertainty_handling" as "probability_distributions",
    "sensitivity_analysis" as true

Let decision_tree be decision_trees.create_decision_tree[tree_definition, tree_config]
```

#### `evaluate_decision_tree[tree, input_variables]`
Evaluates a decision tree with specific input conditions.

**Parameters:**
- `tree` (DecisionTree): Decision tree instance
- `input_variables` (Dictionary): Input variables and their values

**Returns:**
- `TreeEvaluation`: Tree evaluation result with decision path and outcome

**Example:**
```runa
Let input_variables be dictionary with:
    "utilization" as 0.85,
    "pending_workload" as true,
    "available_budget" as 50000,
    "time_constraint_hours" as 2,
    "performance_target" as 0.95

Let tree_evaluation = decision_trees.evaluate_decision_tree[decision_tree, input_variables]

Display "Decision Tree Evaluation:"
Display "  Recommended action: " with message tree_evaluation["recommended_action"]
Display "  Decision path: " with message tree_evaluation["decision_path"]
Display "  Confidence: " with message tree_evaluation["confidence"]
Display "  Expected outcome value: " with message tree_evaluation["expected_value"]
```

### Multi-Criteria Decision Analysis Functions

#### `perform_mcdm_analysis[alternatives, criteria, method, config]`
Performs multi-criteria decision analysis using specified methods.

**Parameters:**
- `alternatives` (List[Dictionary]): Alternative options with attribute values
- `criteria` (List[Dictionary]): Decision criteria with weights and preferences
- `method` (String): MCDM method ("ahp", "topsis", "electre", "promethee")
- `config` (Dictionary): Method-specific configuration parameters

**Returns:**
- `MCDMResult`: MCDM analysis result with rankings and scores

**Example:**
```runa
Let alternatives be list containing:
    dictionary with:
        "id" as "solution_a",
        "attributes" as dictionary with: "cost" as 25000, "performance" as 0.8, "reliability" as 0.9, "ease_of_use" as 0.7,
    dictionary with:
        "id" as "solution_b", 
        "attributes" as dictionary with: "cost" as 35000, "performance" as 0.9, "reliability" as 0.8, "ease_of_use" as 0.9,
    dictionary with:
        "id" as "solution_c",
        "attributes" as dictionary with: "cost" as 20000, "performance" as 0.7, "reliability" as 0.85, "ease_of_use" as 0.8

Let criteria be list containing:
    dictionary with: "name" as "cost", "weight" as 0.3, "type" as "cost", "scale" as "ratio",
    dictionary with: "name" as "performance", "weight" as 0.4, "type" as "benefit", "scale" as "interval",
    dictionary with: "name" as "reliability", "weight" as 0.2, "type" as "benefit", "scale" as "interval",
    dictionary with: "name" as "ease_of_use", "weight" as 0.1, "type" as "benefit", "scale" as "interval"

Let mcdm_config be dictionary with:
    "normalization_method" as "vector_normalization",
    "distance_measure" as "euclidean",
    "fuzzy_numbers" as false,
    "sensitivity_analysis" as true

Let mcdm_result be mcdm_analysis.perform_mcdm_analysis[alternatives, criteria, "topsis", mcdm_config]

Display "MCDM Analysis Results (TOPSIS):"
For each i, ranking in mcdm_result["rankings"]:
    Display "  Rank " with message i plus 1 with message ": " with message ranking["alternative_id"]
    Display "    TOPSIS Score: " with message ranking["topsis_score"]
    Display "    Distance to Ideal: " with message ranking["distance_to_ideal"]
```

## Advanced Features

### Probabilistic and Bayesian Decision Making

Handle uncertainty and probabilistic reasoning in decisions:

```runa
Import "ai.decision.probabilistic" as prob_decision

Note: Create Bayesian decision network
Let bayesian_config be dictionary with:
    "network_structure" as "influence_diagram",
    "inference_algorithm" as "variable_elimination",
    "learning_enabled" as true,
    "evidence_integration" as true

Let bayesian_system be prob_decision.create_bayesian_decision_system[bayesian_config]

Note: Define probabilistic decision model
Let decision_network be dictionary with:
    "decision_nodes" as list containing:
        dictionary with: "name" as "investment_choice", "options" as list containing "aggressive", "moderate", "conservative"
    "chance_nodes" as list containing:
        dictionary with: "name" as "market_conditions", "states" as list containing "bull", "stable", "bear", "probabilities" as list containing 0.3, 0.4, 0.3,
        dictionary with: "name" as "technology_adoption", "states" as list containing "fast", "medium", "slow", "probabilities" as list containing 0.2, 0.6, 0.2
    "utility_nodes" as list containing:
        dictionary with: "name" as "financial_return", "utility_function" as "logarithmic_utility"
    "dependencies" as list containing:
        dictionary with: "parent" as "investment_choice", "child" as "financial_return",
        dictionary with: "parent" as "market_conditions", "child" as "financial_return",
        dictionary with: "parent" as "technology_adoption", "child" as "financial_return"

Let probabilistic_result be prob_decision.solve_decision_network[bayesian_system, decision_network]
```

### Game-Theoretic Decision Making

Handle strategic interactions and multi-agent decisions:

```runa
Import "ai.decision.game_theory" as game_theory

Note: Create game-theoretic decision system
Let game_config be dictionary with:
    "game_type" as "simultaneous_game",
    "solution_concept" as "nash_equilibrium",
    "player_rationality" as "bounded_rationality",
    "learning_dynamics" as "fictitious_play"

Let game_system be game_theory.create_game_system[game_config]

Note: Define strategic decision scenario
Let strategic_game be dictionary with:
    "players" as list containing "our_agent", "competitor_1", "competitor_2",
    "strategies" as dictionary with:
        "our_agent" as list containing "aggressive_pricing", "moderate_pricing", "premium_pricing",
        "competitor_1" as list containing "match_price", "undercut_price", "premium_strategy",
        "competitor_2" as list containing "cost_leadership", "differentiation", "niche_focus"
    "payoff_matrix" as game_payoff_matrix,
    "information_structure" as "complete_information"

Let game_result be game_theory.solve_game[game_system, strategic_game]
```

### Dynamic and Sequential Decision Making

Handle time-dependent and sequential decisions:

```runa
Import "ai.decision.dynamic" as dynamic_decision

Note: Create dynamic decision system
Let dynamic_config be dictionary with:
    "planning_horizon" as 12,
    "time_preference" as "exponential_discounting",
    "discount_rate" as 0.05,
    "state_space_approximation" as "function_approximation"

Let dynamic_system be dynamic_decision.create_dynamic_system[dynamic_config]

Note: Define sequential decision problem
Let sequential_problem be dictionary with:
    "state_variables" as list containing "inventory_level", "demand_forecast", "market_share",
    "action_space" as list containing "increase_production", "maintain_production", "decrease_production",
    "state_transitions" as transition_probabilities,
    "reward_function" as profit_function,
    "terminal_conditions" as termination_criteria

Let dynamic_result be dynamic_decision.solve_sequential_problem[dynamic_system, sequential_problem]
```

### Decision Explanation and Interpretability

Generate explanations for decision recommendations:

```runa
Import "ai.decision.explanation" as decision_explanation

Note: Create explanation system
Let explanation_config be dictionary with:
    "explanation_type" as "counterfactual",
    "detail_level" as "comprehensive",
    "target_audience" as "technical_stakeholders",
    "visualization_enabled" as true

Let explanation_system be decision_explanation.create_explanation_system[explanation_config]

Note: Generate decision explanation
Let explanation_request be dictionary with:
    "decision_result" as previous_decision_result,
    "explanation_questions" as list containing:
        "Why was this alternative selected?",
        "What would happen if we changed the criteria weights?",
        "Which factors were most influential?",
        "What are the risks of this decision?"

Let decision_explanation_result be decision_explanation.explain_decision[explanation_system, explanation_request]

Display "Decision Explanation:"
For each explanation in decision_explanation_result["explanations"]:
    Display "Q: " with message explanation["question"]
    Display "A: " with message explanation["answer"]
    Display "Supporting evidence: " with message explanation["evidence"]
```

## Performance Optimization

### Computational Efficiency and Scalability

Optimize decision-making performance for large problems:

```runa
Import "ai.decision.optimization" as decision_opt

Note: Configure performance optimization
Let optimization_config be dictionary with:
    "parallel_processing" as true,
    "approximation_algorithms" as true,
    "caching_enabled" as true,
    "incremental_computation" as true,
    "memory_optimization" as true

decision_opt.optimize_performance[decision_system, optimization_config]

Note: Configure scaling for large problems
Let scaling_config be dictionary with:
    "problem_decomposition" as true,
    "hierarchical_solving" as true,
    "distributed_computation" as true,
    "adaptive_precision" as true

decision_opt.enable_scaling[decision_system, scaling_config]
```

### Real-Time Decision Making

Enable real-time decision capabilities:

```runa
Import "ai.decision.realtime" as realtime_decision

Let realtime_config be dictionary with:
    "latency_target_ms" as 100,
    "anytime_algorithms" as true,
    "incremental_updates" as true,
    "precomputed_solutions" as true,
    "interrupt_handling" as true

Let realtime_system be realtime_decision.create_realtime_system[decision_system, realtime_config]
```

## Integration Examples

### Integration with Planning Systems

```runa
Import "ai.planning.core" as planning
Import "ai.decision.integration" as decision_integration

Let planner be planning.create_planner[planning_config]
decision_integration.connect_decision_planner[decision_system, planner]

Note: Use decision making for plan selection
Let plan_decision = decision_integration.decide_optimal_plan[decision_system, plan_alternatives]
```

### Integration with Learning Systems

```runa
Import "ai.learning.core" as learning
Import "ai.decision.integration" as decision_integration

Let learning_system be learning.create_learning_system[learning_config]
decision_integration.connect_decision_learner[decision_system, learning_system]

Note: Learn decision policies from experience
Let policy_learning_result = decision_integration.learn_decision_policy[decision_system, decision_experience]
```

## Best Practices

### Decision Model Design
1. **Problem Structuring**: Clearly define alternatives, criteria, and constraints
2. **Stakeholder Involvement**: Include relevant stakeholders in model development
3. **Sensitivity Analysis**: Test decision robustness to parameter changes
4. **Validation**: Validate models against historical decisions and outcomes

### Performance Guidelines
1. **Computational Efficiency**: Use appropriate algorithms for problem size
2. **Approximation Trade-offs**: Balance accuracy with computational requirements
3. **Incremental Updates**: Update decisions efficiently as conditions change
4. **Caching Strategies**: Cache frequently computed decision components

### Example: Production Decision Architecture

```runa
Process called "create_production_decision_architecture" that takes config as Dictionary returns Dictionary:
    Note: Create core decision components
    Let decision_system be decision_core.create_decision_system[config["core_config"]]
    Let bayesian_system be prob_decision.create_bayesian_decision_system[config["probabilistic_config"]]
    Let game_system be game_theory.create_game_system[config["strategic_config"]]
    Let dynamic_system be dynamic_decision.create_dynamic_system[config["dynamic_config"]]
    
    Note: Create integrated decision architecture
    Let integration_config be dictionary with:
        "decision_systems" as list containing decision_system, bayesian_system, game_system, dynamic_system,
        "orchestration_strategy" as "hybrid_approach",
        "conflict_resolution" as "weighted_voting",
        "explanation_enabled" as true,
        "learning_enabled" as true
    
    Let integrated_decision = decision_integration.create_integrated_system[integration_config]
    
    Note: Configure optimization and monitoring
    decision_opt.optimize_performance[integrated_decision, config["optimization_config"]]
    
    Return dictionary with:
        "decision_system" as integrated_decision,
        "capabilities" as list containing "multi_criteria", "probabilistic", "strategic", "dynamic", "explainable",
        "status" as "operational"

Let production_config be dictionary with:
    "core_config" as dictionary with:
        "decision_framework" as "hybrid_approach",
        "learning_enabled" as true
    "probabilistic_config" as dictionary with:
        "inference_algorithm" as "variable_elimination",
        "uncertainty_handling" as true
    "strategic_config" as dictionary with:
        "solution_concept" as "nash_equilibrium",
        "learning_dynamics" as "reinforcement_learning"
    "dynamic_config" as dictionary with:
        "planning_horizon" as 24,
        "state_space_approximation" as "neural_network"
    "optimization_config" as dictionary with:
        "parallel_processing" as true,
        "approximation_algorithms" as true

Let production_decision_architecture be create_production_decision_architecture[production_config]
```

## Troubleshooting

### Common Issues

**Poor Decision Quality**
- Review criteria weights and stakeholder preferences
- Validate alternative attribute measurements
- Check for missing or biased information

**Computational Performance Problems**
- Enable approximation algorithms for large problems
- Use problem decomposition techniques
- Implement parallel processing where applicable

**Inconsistent Results**
- Verify input data quality and consistency
- Check for conflicting constraints or criteria
- Review normalization and scaling methods

### Debugging Tools

```runa
Import "ai.decision.debug" as decision_debug

Note: Enable comprehensive debugging
decision_debug.enable_debug_mode[decision_system, dictionary with:
    "trace_decision_process" as true,
    "log_criteria_evaluations" as true,
    "monitor_computation_steps" as true,
    "capture_intermediate_results" as true
]

Let debug_report be decision_debug.generate_debug_report[decision_system]
```

This decision making systems module provides a comprehensive foundation for automated decision-making in Runa applications. The combination of multi-criteria analysis, probabilistic reasoning, game theory, and learning capabilities makes it suitable for complex decision scenarios across domains including resource allocation, strategic planning, investment decisions, and operational optimization.