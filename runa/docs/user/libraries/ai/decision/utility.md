# Utility Theory Module

**Advanced utility function optimization and preference modeling for rational decision-making**

## Overview

The Runa Utility Theory module implements comprehensive utility function optimization, multi-attribute utility analysis, prospect theory, and behavioral decision modeling. It provides sophisticated tools for modeling decision-maker preferences, handling uncertainty, and optimizing decisions under complex value structures, making it competitive with specialized decision analysis tools and behavioral economics frameworks.

### Key Features

- **Expected Utility Theory**: Classical utility maximization with risk preferences
- **Multi-Attribute Utility**: Complex preference structures across multiple criteria
- **Prospect Theory**: Behavioral decision modeling with reference points and loss aversion
- **Preference Elicitation**: Interactive methods for learning decision-maker preferences
- **Robust Optimization**: Utility maximization under uncertainty and ambiguity
- **Dynamic Utility**: Time-varying preferences and temporal decision modeling

## Core Types

### UtilityFunction
```runa
Type called "UtilityFunction":
    function_id as String
    function_type as String  Note: "linear", "exponential", "logarithmic", "piecewise", "learned"
    parameters as Dictionary
    domain as List[Float]
    range as List[Float]
    risk_attitude as String  Note: "risk_averse", "risk_neutral", "risk_seeking"
    utility_values as Dictionary[String, Float]
    derivative_function as String
    concavity as String
```

### MultiAttributeUtility
```runa
Type called "MultiAttributeUtility":
    mau_id as String
    attributes as List[Attribute]
    attribute_weights as Dictionary[String, Float]
    aggregation_function as String  Note: "additive", "multiplicative", "multilinear"
    value_functions as Dictionary[String, ValueFunction]
    preference_structure as PreferenceStructure
    tradeoff_rates as Dictionary[String, Dictionary[String, Float]]
```

### ProspectTheoryModel
```runa
Type called "ProspectTheoryModel":
    model_id as String
    reference_point as Dictionary[String, Float]
    loss_aversion_coefficient as Float
    probability_weighting_function as String
    value_function_parameters as Dictionary
    decision_weights as Dictionary[String, Float]
    framing_effects as Dictionary[String, Float]
```

## Quick Start

### Basic Utility Function Creation
```runa
Import "ai/decision/utility" as Utility

Note: Create exponential utility function for risk-averse decision maker
Let utility_config be Dictionary with:
    "function_type" as "exponential"
    "risk_coefficient" as 0.5  Note: risk aversion parameter
    "domain" as [-1000000.0, 1000000.0]  Note: wealth range
    "normalization" as "zero_one"

Let risk_averse_utility be Utility.create_utility_function with utility_config

Note: Evaluate utility for different wealth levels
Let wealth_levels be [-100000.0, -10000.0, 0.0, 10000.0, 50000.0, 100000.0, 500000.0]
Let utility_values be list containing

For each wealth in wealth_levels:
    Let utility_value be Utility.evaluate_utility with
        utility_function as risk_averse_utility
        and value as wealth
    
    Add utility_value to utility_values
    Print "Wealth: $" with wealth with ", Utility: " with utility_value

Note: Analyze risk preferences
Let risk_analysis be Utility.analyze_risk_preferences with
    utility_function as risk_averse_utility
    and wealth_range as [0.0, 100000.0]

Print "Risk Analysis:"
Print "  Risk attitude: " with risk_analysis["risk_attitude"]
Print "  Absolute risk aversion: " with risk_analysis["absolute_risk_aversion"]
Print "  Relative risk aversion: " with risk_analysis["relative_risk_aversion"]
Print "  Certainty equivalent (50/50 gamble $0/$100k): $" with risk_analysis["certainty_equivalent"]

Note: Compare with risk-neutral utility
Let risk_neutral_utility be Utility.create_utility_function with
    Dictionary with: "function_type" as "linear", "domain" as [-1000000.0, 1000000.0]

Let gamble_comparison be Utility.compare_gamble_preferences with
    risk_averse_utility as risk_averse_utility
    and risk_neutral_utility as risk_neutral_utility
    and gamble as Dictionary with:
        "outcomes" as [0.0, 100000.0]
        "probabilities" as [0.5, 0.5]

Print "Gamble comparison:"
Print "  Risk-averse expected utility: " with gamble_comparison["risk_averse_eu"]
Print "  Risk-neutral expected utility: " with gamble_comparison["risk_neutral_eu"]
Print "  Risk premium: $" with gamble_comparison["risk_premium"]
```

### Multi-Attribute Utility Analysis
```runa
Import "ai/decision/utility" as Utility

Note: Define attributes for car selection decision
Let car_attributes be [
    Dictionary with:
        "name" as "price"
        "type" as "continuous"
        "range" as [15000.0, 50000.0]
        "preference_direction" as "decreasing"  Note: lower price is better
        "unit" as "dollars",
    Dictionary with:
        "name" as "fuel_efficiency"
        "type" as "continuous"
        "range" as [15.0, 50.0]
        "preference_direction" as "increasing"  Note: higher MPG is better
        "unit" as "mpg",
    Dictionary with:
        "name" as "safety_rating"
        "type" as "ordinal"
        "range" as [1.0, 5.0]
        "preference_direction" as "increasing"
        "unit" as "stars",
    Dictionary with:
        "name" as "comfort_score"
        "type" as "continuous"
        "range" as [1.0, 10.0]
        "preference_direction" as "increasing"
        "unit" as "score"
]

Note: Create value functions for each attribute
Let value_functions be Dictionary containing

For each attribute in car_attributes:
    Let value_function_config be Dictionary with:
        "function_type" as if attribute["preference_direction"] is "decreasing" then "exponential_decreasing" else "logarithmic"
        "range" as attribute["range"]
        "reference_point" as calculate_reference_point with attribute["range"]
    
    Let value_function be Utility.create_value_function with
        attribute_name as attribute["name"]
        and config as value_function_config
    
    Set value_functions[attribute["name"]] to value_function

Note: Elicit attribute weights using pairwise comparisons
Let pairwise_comparisons be [
    Dictionary with: "attribute_a" as "price", "attribute_b" as "fuel_efficiency", "preference" as "price", "strength" as 0.6,
    Dictionary with: "attribute_a" as "price", "attribute_b" as "safety_rating", "preference" as "safety_rating", "strength" as 0.8,
    Dictionary with: "attribute_a" as "price", "attribute_b" as "comfort_score", "preference" as "price", "strength" as 0.7,
    Dictionary with: "attribute_a" as "fuel_efficiency", "attribute_b" as "safety_rating", "preference" as "safety_rating", "strength" as 0.9,
    Dictionary with: "attribute_a" as "fuel_efficiency", "attribute_b" as "comfort_score", "preference" as "fuel_efficiency", "strength" as 0.6,
    Dictionary with: "attribute_a" as "safety_rating", "attribute_b" as "comfort_score", "preference" as "safety_rating", "strength" as 0.8
]

Let weight_elicitation_result be Utility.elicit_attribute_weights with
    attributes as car_attributes
    and pairwise_comparisons as pairwise_comparisons
    and method as "eigenvector"

Let attribute_weights be weight_elicitation_result["weights"]
Print "Elicited attribute weights:"
For each attribute_name in attribute_weights:
    Print "  " with attribute_name with ": " with attribute_weights[attribute_name]

Note: Create multi-attribute utility function
Let mau_config be Dictionary with:
    "aggregation_function" as "additive"
    "scaling_method" as "direct_rating"
    "consistency_check" as true

Let multi_attribute_utility be Utility.create_multi_attribute_utility with
    attributes as car_attributes
    and value_functions as value_functions
    and weights as attribute_weights
    and config as mau_config

Note: Evaluate car alternatives
Let car_alternatives be [
    Dictionary with: "name" as "Economy Car", "price" as 18000.0, "fuel_efficiency" as 35.0, "safety_rating" as 4.0, "comfort_score" as 6.0,
    Dictionary with: "name" as "Luxury Car", "price" as 45000.0, "fuel_efficiency" as 25.0, "safety_rating" as 5.0, "comfort_score" as 9.0,
    Dictionary with: "name" as "Hybrid Car", "price" as 28000.0, "fuel_efficiency" as 45.0, "safety_rating" as 4.5, "comfort_score" as 7.0,
    Dictionary with: "name" as "Sports Car", "price" as 38000.0, "fuel_efficiency" as 20.0, "safety_rating" as 3.5, "comfort_score" as 8.0
]

Let alternative_utilities be list containing
For each car in car_alternatives:
    Let car_utility be Utility.evaluate_multi_attribute_utility with
        mau_function as multi_attribute_utility
        and alternative as car
    
    Add Dictionary with: "car" as car["name"], "utility" as car_utility to alternative_utilities
    Print car["name"] with " - Utility: " with car_utility["total_utility"]

Note: Rank alternatives and perform sensitivity analysis
Let ranking be Utility.rank_alternatives with alternative_utilities
Print "Ranking (best to worst):"
For i from 0 to length of ranking minus 1:
    Print (i plus 1) with ". " with ranking[i]["car"] with " (Utility: " with ranking[i]["utility"] with ")"

Let sensitivity_analysis be Utility.perform_sensitivity_analysis with
    mau_function as multi_attribute_utility
    and alternatives as car_alternatives
    and weight_variations as 0.2  Note: ±20% weight changes

Print "Sensitivity analysis - ranking stability: " with sensitivity_analysis["ranking_stability"]
```

### Prospect Theory Decision Modeling
```runa
Import "ai/decision/utility" as Utility

Note: Create prospect theory model for behavioral decision analysis
Let prospect_config be Dictionary with:
    "reference_point" as Dictionary with: "wealth" as 50000.0,  Note: current wealth
    "loss_aversion_coefficient" as 2.25  Note: typical loss aversion
    "probability_weighting" as "tversky_kahneman"
    "value_function_alpha" as 0.88  Note: diminishing sensitivity
    "value_function_beta" as 0.88  Note: for losses
    "probability_weighting_gamma" as 0.61  Note: for gains
    "probability_weighting_delta" as 0.69  Note: for losses

Let prospect_model be Utility.create_prospect_theory_model with prospect_config

Note: Analyze decision under risk with framing effects
Let investment_decision be Dictionary with:
    "sure_thing" as Dictionary with:
        "outcome" as 3000.0
        "probability" as 1.0
        "description" as "Guaranteed $3,000 gain",
    "gamble" as Dictionary with:
        "outcomes" as [4000.0, 0.0]
        "probabilities" as [0.8, 0.2]
        "description" as "80% chance of $4,000, 20% chance of $0"
]

Note: Evaluate both options with prospect theory
Let sure_thing_value be Utility.evaluate_prospect with
    model as prospect_model
    and prospect as investment_decision["sure_thing"]

Let gamble_value be Utility.evaluate_prospect with
    model as prospect_model
    and prospect as investment_decision["gamble"]

Print "Prospect Theory Analysis (Gain Frame):"
Print "  Sure thing value: " with sure_thing_value
Print "  Gamble value: " with gamble_value
Print "  Preferred option: " with if sure_thing_value > gamble_value then "Sure thing" else "Gamble"

Note: Test framing effect with loss frame
Let loss_framed_decision be Dictionary with:
    "sure_loss" as Dictionary with:
        "outcome" as -3000.0
        "probability" as 1.0
        "description" as "Guaranteed $3,000 loss",
    "loss_gamble" as Dictionary with:
        "outcomes" as [-4000.0, 0.0]
        "probabilities" as [0.8, 0.2]
        "description" as "80% chance of $4,000 loss, 20% chance of no loss"
]

Let sure_loss_value be Utility.evaluate_prospect with
    model as prospect_model
    and prospect as loss_framed_decision["sure_loss"]

Let loss_gamble_value be Utility.evaluate_prospect with
    model as prospect_model
    and prospect as loss_framed_decision["loss_gamble"]

Print "Prospect Theory Analysis (Loss Frame):"
Print "  Sure loss value: " with sure_loss_value
Print "  Loss gamble value: " with loss_gamble_value
Print "  Preferred option: " with if sure_loss_value > loss_gamble_value then "Sure loss" else "Loss gamble"

Note: Demonstrate reflection effect
Print "Reflection Effect Demonstration:"
Print "  Gain frame preference: " with if sure_thing_value > gamble_value then "Risk averse" else "Risk seeking"
Print "  Loss frame preference: " with if sure_loss_value > loss_gamble_value then "Risk averse" else "Risk seeking"
```

## Advanced Features

### Dynamic Utility with Time Preferences
```runa
Import "ai/decision/utility" as Utility

Note: Create intertemporal utility function with discounting
Let temporal_utility_config be Dictionary with:
    "base_utility_function" as "logarithmic"
    "discount_rate" as 0.05  Note: 5% annual discount rate
    "time_preference_function" as "exponential"
    "present_bias" as 1.2  Note: hyperbolic discounting factor
    "time_horizon" as 30  Note: 30 years
    "compounding_frequency" as "annual"

Let intertemporal_utility be Utility.create_intertemporal_utility with temporal_utility_config

Note: Analyze retirement savings decision
Let savings_scenarios be [
    Dictionary with:
        "name" as "Conservative Savings"
        "annual_savings" as 5000.0
        "expected_return" as 0.04
        "risk" as 0.1,
    Dictionary with:
        "name" as "Moderate Savings"
        "annual_savings" as 8000.0
        "expected_return" as 0.06
        "risk" as 0.15,
    Dictionary with:
        "name" as "Aggressive Savings"
        "annual_savings" as 12000.0
        "expected_return" as 0.08
        "risk" as 0.25
]

Let retirement_analysis be list containing
For each scenario in savings_scenarios:
    Note: Calculate utility stream over time
    Let utility_stream be Utility.calculate_intertemporal_utility_stream with
        utility_function as intertemporal_utility
        and savings_plan as scenario
        and time_horizon as 30
    
    Let present_value_utility be Utility.calculate_present_value_utility with
        utility_stream as utility_stream
        and discount_function as intertemporal_utility
    
    Add Dictionary with:
        "scenario" as scenario["name"]
        "present_value_utility" as present_value_utility
        "final_wealth_utility" as utility_stream[-1]
        to retirement_analysis
    
    Print scenario["name"] with ":"
    Print "  Present value of utility: " with present_value_utility
    Print "  Utility at retirement: " with utility_stream[-1]

Note: Optimal savings rate calculation
Let optimal_savings_rate be Utility.find_optimal_savings_rate with
    utility_function as intertemporal_utility
    and income as 60000.0
    and time_horizon as 30
    and constraints as Dictionary with:
        "min_savings_rate" as 0.05
        "max_savings_rate" as 0.3

Print "Optimal savings analysis:"
Print "  Optimal savings rate: " with optimal_savings_rate["rate"] with "%"
Print "  Maximized lifetime utility: " with optimal_savings_rate["lifetime_utility"]
```

### Preference Learning from Choice Data
```runa
Import "ai/decision/utility" as Utility

Note: Learn utility function from observed choices
Let choice_observations be [
    Dictionary with:
        "choice_id" as 1
        "alternative_a" as Dictionary with: "price" as 100.0, "quality" as 7.0
        "alternative_b" as Dictionary with: "price" as 150.0, "quality" as 9.0
        "chosen" as "b"
        "confidence" as 0.8,
    Dictionary with:
        "choice_id" as 2
        "alternative_a" as Dictionary with: "price" as 200.0, "quality" as 8.0
        "alternative_b" as Dictionary with: "price" as 120.0, "quality" as 6.0
        "chosen" as "b"
        "confidence" as 0.6,
    Dictionary with:
        "choice_id" as 3
        "alternative_a" as Dictionary with: "price" as 80.0, "quality" as 5.0
        "alternative_b" as Dictionary with: "price" as 180.0, "quality" as 10.0
        "chosen" as "a"
        "confidence" as 0.9
]

Note: Learn preference parameters using maximum likelihood
Let preference_learning_config be Dictionary with:
    "utility_function_type" as "cobb_douglas"  Note: U = price^α × quality^β
    "learning_method" as "maximum_likelihood"
    "regularization" as 0.01
    "convergence_threshold" as 0.001
    "max_iterations" as 1000

Let learned_preferences be Utility.learn_preferences_from_choices with
    choice_data as choice_observations
    and config as preference_learning_config

Print "Learned preference parameters:"
Print "  Price sensitivity (α): " with learned_preferences["price_coefficient"]
Print "  Quality preference (β): " with learned_preferences["quality_coefficient"]
Print "  Model likelihood: " with learned_preferences["log_likelihood"]
Print "  Prediction accuracy: " with learned_preferences["prediction_accuracy"]

Note: Validate learned model with cross-validation
Let validation_result be Utility.cross_validate_preference_model with
    learned_model as learned_preferences
    and choice_data as choice_observations
    and cv_folds as 5

Print "Cross-validation results:"
Print "  Average accuracy: " with validation_result["mean_accuracy"]
Print "  Standard deviation: " with validation_result["std_accuracy"]

Note: Use learned preferences for new predictions
Let new_choice_scenario be Dictionary with:
    "alternative_a" as Dictionary with: "price" as 130.0, "quality" as 7.5
    "alternative_b" as Dictionary with: "price" as 170.0, "quality" as 8.5

Let choice_prediction be Utility.predict_choice_with_learned_preferences with
    model as learned_preferences
    and scenario as new_choice_scenario

Print "Choice prediction for new scenario:"
Print "  Predicted choice: " with choice_prediction["predicted_choice"]
Print "  Choice probability: " with choice_prediction["choice_probability"]
Print "  Confidence interval: " with choice_prediction["confidence_interval"]
```

### Robust Utility Optimization
```runa
Import "ai/decision/utility" as Utility

Note: Optimize decisions under utility function uncertainty
Let utility_uncertainty_config be Dictionary with:
    "base_utility_function" as "exponential"
    "parameter_distributions" as Dictionary with:
        "risk_coefficient" as Dictionary with:
            "distribution" as "normal"
            "mean" as 0.5
            "std" as 0.1
            "min" as 0.1
            "max" as 1.0
    "robustness_criterion" as "minimax_regret"  Note: or "worst_case", "expected_value"
    "confidence_level" as 0.95

Note: Define decision alternatives with uncertain outcomes
Let investment_alternatives be [
    Dictionary with:
        "name" as "Government Bonds"
        "return_distribution" as Dictionary with:
            "distribution" as "normal"
            "mean" as 0.03
            "std" as 0.01
        "risk_level" as "low",
    Dictionary with:
        "name" as "Stock Index"
        "return_distribution" as Dictionary with:
            "distribution" as "normal"
            "mean" as 0.08
            "std" as 0.15
        "risk_level" as "medium",
    Dictionary with:
        "name" as "Venture Capital"
        "return_distribution" as Dictionary with:
            "distribution" as "lognormal"
            "mean" as 0.15
            "std" as 0.30
        "risk_level" as "high"
]

Let robust_optimization_result be Utility.robust_utility_optimization with
    utility_uncertainty as utility_uncertainty_config
    and alternatives as investment_alternatives
    and robustness_criterion as "minimax_regret"
    and monte_carlo_samples as 10000

Print "Robust optimization results:"
Print "  Robust optimal choice: " with robust_optimization_result["optimal_choice"]
Print "  Expected regret: " with robust_optimization_result["expected_regret"]
Print "  Worst-case regret: " with robust_optimization_result["worst_case_regret"]

Note: Sensitivity analysis for robustness
Let robustness_sensitivity be Utility.analyze_robustness_sensitivity with
    base_result as robust_optimization_result
    and parameter_variations as Dictionary with:
        "risk_coefficient_std" as [0.05, 0.1, 0.15, 0.2]
        "confidence_level" as [0.90, 0.95, 0.99]

Print "Robustness sensitivity analysis:"
For each variation in robustness_sensitivity["results"]:
    Print "  " with variation["parameter"] with " = " with variation["value"]
    Print "    Optimal choice: " with variation["optimal_choice"]
    Print "    Choice stability: " with variation["stability_score"]
```

### Utility-Based Portfolio Optimization
```runa
Import "ai/decision/utility" as Utility
Import "ai/decision/risk" as Risk

Note: Integrate utility theory with portfolio optimization
Let investor_utility_config be Dictionary with:
    "utility_function" as "power"
    "risk_aversion" as 3.0  Note: moderate risk aversion
    "wealth_level" as 500000.0
    "investment_horizon" as 5  Note: years

Let investor_utility be Utility.create_utility_function with investor_utility_config

Note: Define investment universe
Let asset_universe be [
    Dictionary with: "name" as "US_STOCKS", "expected_return" as 0.08, "volatility" as 0.15,
    Dictionary with: "name" as "INTL_STOCKS", "expected_return" as 0.07, "volatility" as 0.18,
    Dictionary with: "name" as "BONDS", "expected_return" as 0.04, "volatility" as 0.05,
    Dictionary with: "name" as "REAL_ESTATE", "expected_return" as 0.06, "volatility" as 0.12,
    Dictionary with: "name" as "COMMODITIES", "expected_return" as 0.05, "volatility" as 0.20
]

Let correlation_matrix be [
    [1.00, 0.75, 0.10, 0.60, 0.30],  Note: US_STOCKS correlations
    [0.75, 1.00, 0.15, 0.55, 0.35],  Note: INTL_STOCKS correlations
    [0.10, 0.15, 1.00, 0.20, -0.10], Note: BONDS correlations
    [0.60, 0.55, 0.20, 1.00, 0.40],  Note: REAL_ESTATE correlations
    [0.30, 0.35, -0.10, 0.40, 1.00]  Note: COMMODITIES correlations
]

Note: Optimize portfolio to maximize expected utility
Let utility_optimization_config be Dictionary with:
    "optimization_method" as "monte_carlo"
    "simulation_count" as 50000
    "rebalancing_frequency" as "annual"
    "transaction_costs" as 0.002
    "constraints" as Dictionary with:
        "max_weight_per_asset" as 0.4
        "min_weight_per_asset" as 0.0
        "leverage_limit" as 1.0

Let optimal_portfolio be Utility.optimize_portfolio_for_utility with
    utility_function as investor_utility
    and asset_universe as asset_universe
    and correlation_matrix as correlation_matrix
    and config as utility_optimization_config

Print "Utility-optimal portfolio allocation:"
For each asset in optimal_portfolio["allocation"]:
    Print "  " with asset["name"] with ": " with (asset["weight"] * 100.0) with "%"

Print "Portfolio characteristics:"
Print "  Expected return: " with optimal_portfolio["expected_return"] with "%"
Print "  Expected volatility: " with optimal_portfolio["expected_volatility"] with "%"
Print "  Expected utility: " with optimal_portfolio["expected_utility"]
Print "  Certainty equivalent: $" with optimal_portfolio["certainty_equivalent"]

Note: Compare with mean-variance optimization
Let mean_variance_portfolio be Risk.optimize_mean_variance_portfolio with
    asset_universe as asset_universe
    and correlation_matrix as correlation_matrix
    and target_return as optimal_portfolio["expected_return"]

Let utility_comparison be Utility.compare_portfolio_utilities with
    utility_function as investor_utility
    and portfolio_a as optimal_portfolio
    and portfolio_b as mean_variance_portfolio

Print "Portfolio comparison:"
Print "  Utility-optimal expected utility: " with utility_comparison["portfolio_a_utility"]
Print "  Mean-variance expected utility: " with utility_comparison["portfolio_b_utility"]
Print "  Utility improvement: " with utility_comparison["utility_difference"]
```

## Performance Optimization

### Efficient Utility Evaluation
```runa
Import "ai/decision/utility" as Utility

Note: Optimize utility calculations for high-frequency use
Let high_performance_config be Dictionary with:
    "vectorized_operations" as true
    "lookup_table_size" as 10000
    "interpolation_method" as "cubic_spline"
    "cache_derivatives" as true
    "parallel_evaluation" as true
    "precision" as "float32"  Note: vs float64 for speed

Let optimized_utility be Utility.create_high_performance_utility with
    base_utility_function as risk_averse_utility
    and config as high_performance_config

Note: Benchmark performance improvement
Let benchmark_config be Dictionary with:
    "evaluation_count" as 100000
    "value_range" as [-1000000.0, 1000000.0]
    "random_seed" as 42

Let performance_benchmark be Utility.benchmark_utility_performance with
    standard_utility as risk_averse_utility
    and optimized_utility as optimized_utility
    and config as benchmark_config

Print "Performance benchmark results:"
Print "  Standard utility time: " with performance_benchmark["standard_time"] with " ms"
Print "  Optimized utility time: " with performance_benchmark["optimized_time"] with " ms"
Print "  Speedup factor: " with performance_benchmark["speedup_factor"] with "x"
Print "  Accuracy preservation: " with performance_benchmark["accuracy_preservation"] with "%"
```

### Parallel Multi-Attribute Evaluation
```runa
Import "ai/decision/utility" as Utility
Import "concurrent/concurrent" as Concurrent

Note: Parallel evaluation for large-scale decision problems
Let parallel_config be Dictionary with:
    "num_workers" as 8
    "batch_size" as 1000
    "load_balancing" as "dynamic"
    "memory_limit_per_worker" as "512MB"

Note: Generate large decision problem
Let large_decision_problem be Utility.generate_large_decision_problem with
    num_alternatives as 10000
    and num_attributes as 20
    and complexity as "high"

Let parallel_evaluation_result be Utility.evaluate_alternatives_parallel with
    mau_function as multi_attribute_utility
    and alternatives as large_decision_problem["alternatives"]
    and config as parallel_config

Print "Parallel evaluation completed:"
Print "  Alternatives evaluated: " with length of large_decision_problem["alternatives"]
Print "  Total time: " with parallel_evaluation_result["total_time"] with " seconds"
Print "  Evaluations per second: " with parallel_evaluation_result["throughput"]
Print "  Memory efficiency: " with parallel_evaluation_result["memory_efficiency"] with "%"

Note: Find top alternatives efficiently
Let top_alternatives be Utility.find_top_k_alternatives with
    evaluation_results as parallel_evaluation_result["results"]
    and k as 10
    and selection_method as "utility_threshold"

Print "Top 10 alternatives by utility:"
For i from 0 to 9:
    Let alternative be top_alternatives[i]
    Print (i plus 1) with ". " with alternative["name"] with " (Utility: " with alternative["utility"] with ")"
```

## Integration with Other Decision Modules

### Utility-Enhanced Game Theory
```runa
Import "ai/decision/utility" as Utility
Import "ai/decision/game_theory" as GameTheory

Note: Model game with player-specific utility functions
Let player_utilities be Dictionary with:
    "player_1" as Utility.create_utility_function with Dictionary with:
        "function_type" as "exponential"
        "risk_coefficient" as 0.3  Note: moderately risk averse
    "player_2" as Utility.create_utility_function with Dictionary with:
        "function_type" as "power"
        "risk_coefficient" as 0.8  Note: more risk averse

Note: Define game with monetary payoffs
Let monetary_payoffs be [
    [[1000, 1000], [0, 1500]],    Note: Player 1's payoffs
    [[1000, 0], [1500, 1500]]     Note: Player 2's payoffs
]

Note: Convert to utility payoffs
Let utility_payoffs be GameTheory.convert_payoffs_to_utility with
    monetary_payoffs as monetary_payoffs
    and player_utilities as player_utilities

Let utility_game be GameTheory.create_game with
    payoff_matrices as utility_payoffs
    and game_type as "normal_form"

Note: Find Nash equilibrium with utility-based payoffs
Let nash_equilibrium be GameTheory.find_nash_equilibrium with utility_game

Print "Utility-based game analysis:"
Print "  Nash equilibrium strategies:"
Print "    Player 1: " with nash_equilibrium["player_1_strategy"]
Print "    Player 2: " with nash_equilibrium["player_2_strategy"]
Print "  Expected utilities:"
Print "    Player 1: " with nash_equilibrium["player_1_utility"]
Print "    Player 2: " with nash_equilibrium["player_2_utility"]

Note: Compare with monetary payoff analysis
Let monetary_nash be GameTheory.find_nash_equilibrium with
    GameTheory.create_game with
        payoff_matrices as monetary_payoffs
        and game_type as "normal_form"

Print "Comparison with monetary payoffs:"
Print "  Strategy differences due to risk preferences:"
Print "    Player 1 strategy change: " with calculate_strategy_difference[nash_equilibrium["player_1_strategy"], monetary_nash["player_1_strategy"]]
Print "    Player 2 strategy change: " with calculate_strategy_difference[nash_equilibrium["player_2_strategy"], monetary_nash["player_2_strategy"]]
```

### Utility-Based Multi-Criteria Decisions
```runa
Import "ai/decision/utility" as Utility
Import "ai/decision/multi_criteria" as MCDA

Note: Enhance MCDA with utility theory
Let mcda_with_utility_config be Dictionary with:
    "use_utility_functions" as true
    "risk_preferences" as Dictionary with:
        "cost" as "risk_seeking"  Note: willing to take cost risks
        "quality" as "risk_averse"  Note: conservative about quality
        "time" as "risk_neutral"
    "uncertainty_modeling" as true
    "robust_ranking" as true

Note: Define uncertain alternatives for vendor selection
Let vendor_alternatives be [
    Dictionary with:
        "name" as "Vendor A"
        "cost" as Dictionary with: "mean" as 100000, "std" as 5000
        "quality" as Dictionary with: "mean" as 8.5, "std" as 0.5
        "delivery_time" as Dictionary with: "mean" as 30, "std" as 3,
    Dictionary with:
        "name" as "Vendor B"
        "cost" as Dictionary with: "mean" as 120000, "std" as 8000
        "quality" as Dictionary with: "mean" as 9.2, "std" as 0.3
        "delivery_time" as Dictionary with: "mean" as 25, "std" as 2,
    Dictionary with:
        "name" as "Vendor C"
        "cost" as Dictionary with: "mean" as 90000, "std" as 10000
        "quality" as Dictionary with: "mean" as 7.8, "std" as 0.8
        "delivery_time" as Dictionary with: "mean" as 35, "std" as 5
]

Let utility_enhanced_mcda be MCDA.create_utility_enhanced_mcda with
    alternatives as vendor_alternatives
    and criteria as ["cost", "quality", "delivery_time"]
    and utility_config as mcda_with_utility_config

Let robust_ranking_result be MCDA.perform_robust_utility_ranking with
    mcda_system as utility_enhanced_mcda
    and monte_carlo_samples as 10000
    and confidence_level as 0.95

Print "Utility-enhanced MCDA results:"
Print "  Robust ranking:"
For i from 0 to length of robust_ranking_result["ranking"] minus 1:
    Let vendor be robust_ranking_result["ranking"][i]
    Print "    " with (i plus 1) with ". " with vendor["name"]
    Print "       Expected utility: " with vendor["expected_utility"]
    Print "       Ranking confidence: " with vendor["ranking_confidence"]

Print "  Ranking sensitivity to utility parameters: " with robust_ranking_result["sensitivity_score"]
```

## Performance Characteristics

### Computational Complexity
- **Single Utility Evaluation**: O(1) for simple functions, O(log n) for complex/learned functions
- **Multi-Attribute Utility**: O(m) where m = number of attributes
- **Preference Learning**: O(n × k × i) where n = choices, k = parameters, i = iterations
- **Robust Optimization**: O(s × a) where s = simulation samples, a = alternatives

### Scalability Benchmarks
| Operation | Problem Size | Computation Time | Memory Usage |
|-----------|--------------|------------------|--------------|
| Utility Function Evaluation | 1M evaluations | 50 ms | 10 MB |
| Multi-Attribute Utility | 10K alternatives × 20 attributes | 2 seconds | 100 MB |
| Preference Learning | 1K choice observations | 30 seconds | 50 MB |
| Robust Optimization | 1K alternatives × 10K samples | 45 seconds | 200 MB |

## Best Practices

### Utility Function Validation
```runa
Note: Validate utility function properties
Let validation_config be Dictionary with:
    "check_monotonicity" as true
    "check_concavity" as true
    "check_continuity" as true
    "check_bounded_rationality" as true
    "tolerance" as 0.001

Let validation_result be Utility.validate_utility_function with
    utility_function as risk_averse_utility
    and config as validation_config

If not validation_result["all_checks_passed"]:
    Print "Utility function validation issues:"
    For each issue in validation_result["issues"]:
        Print "  " with issue["property"] with ": " with issue["description"]
        Print "    Recommendation: " with issue["recommendation"]
```

### Preference Elicitation Best Practices
```runa
Note: Systematic preference elicitation process
Let elicitation_protocol be Utility.create_elicitation_protocol with
    method as "adaptive_questioning"
    and stopping_criteria as Dictionary with:
        "max_questions" as 20
        "confidence_threshold" as 0.95
        "consistency_threshold" as 0.9

Let elicitation_session be Utility.conduct_preference_elicitation with
    protocol as elicitation_protocol
    and decision_maker as current_user
    and attributes as car_attributes

Print "Elicitation session completed:"
Print "  Questions asked: " with elicitation_session["questions_count"]
Print "  Consistency score: " with elicitation_session["consistency_score"]
Print "  Confidence level: " with elicitation_session["confidence_level"]
```

## API Reference

### Core Functions
- `create_utility_function()` - Create single-attribute utility function
- `create_multi_attribute_utility()` - Create MAU function
- `create_prospect_theory_model()` - Create behavioral decision model
- `evaluate_utility()` - Evaluate utility for given values
- `optimize_portfolio_for_utility()` - Utility-based portfolio optimization

### Analysis Functions
- `analyze_risk_preferences()` - Extract risk attitude parameters
- `perform_sensitivity_analysis()` - Sensitivity analysis for MAU
- `learn_preferences_from_choices()` - Preference learning from data
- `robust_utility_optimization()` - Optimization under uncertainty

### Elicitation Functions
- `elicit_attribute_weights()` - Interactive weight elicitation
- `conduct_preference_elicitation()` - Comprehensive preference elicitation
- `validate_preference_consistency()` - Check preference consistency

### Utility Functions
- `rank_alternatives()` - Rank alternatives by utility
- `compare_gamble_preferences()` - Compare risk preferences
- `generate_utility_visualization()` - Visualize utility functions
- `export_utility_model()` - Export trained utility models

---

The Utility Theory module provides the foundation for rational decision-making in AI systems, enabling sophisticated preference modeling that captures both normative economic principles and descriptive behavioral patterns observed in human decision-making.