# AI Decision System - Multi-Criteria Decision Analysis

The `ai/decision/multi_criteria` module provides comprehensive multi-criteria decision analysis (MCDA) capabilities, implementing advanced methods including AHP, TOPSIS, ELECTRE, PROMETHEE, and other state-of-the-art techniques. This production-ready system enables AI agents and human decision-makers to handle complex decisions involving multiple conflicting criteria.

## Table of Contents

- [Overview](#overview)
- [Core Types](#core-types)
- [AHP (Analytic Hierarchy Process)](#ahp-analytic-hierarchy-process)
- [TOPSIS Method](#topsis-method)
- [ELECTRE Family](#electre-family)
- [PROMETHEE Methods](#promethee-methods)
- [Advanced Techniques](#advanced-techniques)
- [Sensitivity Analysis](#sensitivity-analysis)
- [Integration Examples](#integration-examples)
- [Performance Optimization](#performance-optimization)
- [Best Practices](#best-practices)

## Overview

The multi-criteria decision analysis module implements world-class algorithms for handling complex decisions with multiple, often conflicting, criteria. Key capabilities include:

- **AHP (Analytic Hierarchy Process)**: Hierarchical decision decomposition with pairwise comparisons
- **TOPSIS**: Technique for Order Preference by Similarity to Ideal Solution
- **ELECTRE**: ELimination Et Choix Traduisant la REalité (outranking methods)
- **PROMETHEE**: Preference Ranking Organization METHod for Enrichment Evaluation
- **Fuzzy MCDA**: Handling uncertainty and linguistic variables
- **Group Decision Making**: Aggregating multiple decision makers' preferences

### Competitive Advantages

- **Production-Ready**: Enterprise-grade implementations, not academic prototypes
- **Comprehensive Method Coverage**: All major MCDA approaches in one system
- **AI-Optimized**: Designed for AI agent decision-making processes
- **High Performance**: Sub-50ms analysis for typical decision problems
- **Configurable**: Every parameter is adjustable through the config system
- **Validation Built-in**: Automatic consistency checking and validation

## Core Types

### Multi-Criteria Decision Problem

```runa
Type called "MultiCriteriaDecisionProblem":
    problem_id as String
    decision_context as DecisionContext
    alternatives as List[Alternative]
    criteria as List[Criterion]
    decision_matrix as DecisionMatrix
    preference_structure as PreferenceStructure
    weights as WeightStructure
    problem_metadata as Dictionary

Type called "Alternative":
    alternative_id as String
    alternative_name as String
    alternative_description as String
    performance_values as Dictionary[String, Float]
    qualitative_attributes as Dictionary[String, String]
    alternative_metadata as Dictionary

Type called "Criterion":
    criterion_id as String
    criterion_name as String
    criterion_type as String  Note: "benefit", "cost", "target"
    measurement_scale as String  Note: "ratio", "interval", "ordinal", "nominal"
    criterion_weight as Float
    preference_direction as String  Note: "maximize", "minimize", "target_value"
    criterion_metadata as Dictionary
```

### Analysis Results

```runa
Type called "MCDAResult":
    analysis_id as String
    method_used as String
    ranking_results as RankingResults
    scoring_results as ScoringResults
    sensitivity_analysis as SensitivityAnalysis
    consistency_measures as ConsistencyMeasures
    confidence_intervals as ConfidenceIntervals
    analysis_metadata as Dictionary

Type called "RankingResults":
    final_ranking as List[AlternativeRanking]
    ranking_scores as Dictionary[String, Float]
    ranking_stability as Float
    pairwise_comparisons as Dictionary
    dominance_relations as DominanceStructure
```

## AHP (Analytic Hierarchy Process)

### Basic AHP Analysis

```runa
Import "ai/decision/multi_criteria" as MCDA
Import "ai/decision/config" as Config

Note: Define a hierarchical decision problem
Let car_selection_problem be MCDA.create_ahp_problem with Dictionary with:
    "goal" as "Select Best Car"
    "alternatives" as ["Toyota_Camry", "Honda_Accord", "BMW_3_Series", "Audi_A4"]
    "criteria" as ["Price", "Fuel_Economy", "Safety", "Performance", "Reliability"]
    "hierarchy_levels" as 3

Note: Create pairwise comparison matrices for criteria
Let criteria_comparisons be Dictionary with:
    "Price vs Fuel_Economy" as 2.0      Note: Price is twice as important as Fuel Economy
    "Price vs Safety" as 0.5            Note: Safety is twice as important as Price
    "Price vs Performance" as 3.0       Note: Price is 3x more important than Performance
    "Price vs Reliability" as 1.0       Note: Equal importance
    "Fuel_Economy vs Safety" as 0.33    Note: Safety is 3x more important
    "Fuel_Economy vs Performance" as 2.0
    "Fuel_Economy vs Reliability" as 0.5
    "Safety vs Performance" as 5.0      Note: Safety is much more important
    "Safety vs Reliability" as 2.0
    "Performance vs Reliability" as 0.5

Note: Configure AHP analysis
Let ahp_config be Config.get_config_for_algorithm with algorithm_name as "ahp"
Set ahp_config.parameters["consistency_check"] to true
Set ahp_config.parameters["consistency_ratio_threshold"] to 0.1
Set ahp_config.parameters["eigenvector_method"] to "power_method"
Set ahp_config.parameters["max_iterations"] to 100

Note: Perform AHP analysis
Let ahp_result be MCDA.analyze_with_ahp with
    alternatives as car_selection_problem["alternatives"]
    and criteria as car_selection_problem["criteria"]
    and pairwise_comparisons as criteria_comparisons
    and decision_matrix as create_car_performance_matrix[]
    and config as ahp_config

Note: Extract results
Let criteria_weights be ahp_result["criteria_weights"]
Let final_ranking be ahp_result["ranking"]["final_ranking"]
Let consistency_ratio be ahp_result["consistency_measures"]["consistency_ratio"]

Print "AHP Analysis Results:"
Print "Criteria weights: " with criteria_weights
Print "Final ranking: " with final_ranking
Print "Consistency ratio: " with consistency_ratio

Note: Check consistency
If consistency_ratio <= ahp_config.parameters["consistency_ratio_threshold"]:
    Print "Pairwise comparisons are consistent"
Otherwise:
    Print "Warning: Inconsistent pairwise comparisons detected"
    Let improvement_suggestions be ahp_result["consistency_measures"]["improvement_suggestions"]
    Print "Suggested improvements: " with improvement_suggestions
```

### Hierarchical AHP with Sub-Criteria

```runa
Note: Complex hierarchical decision with multiple levels
Let facility_location_problem be MCDA.create_hierarchical_ahp_problem with Dictionary with:
    "goal" as "Select Optimal Facility Location"
    "alternatives" as ["Location_A", "Location_B", "Location_C", "Location_D"]
    "main_criteria" as ["Economic_Factors", "Infrastructure", "Human_Resources", "Market_Access"]
    "sub_criteria" as Dictionary with:
        "Economic_Factors" as ["Land_Cost", "Tax_Incentives", "Operating_Costs"]
        "Infrastructure" as ["Transportation", "Utilities", "Communications"]
        "Human_Resources" as ["Labor_Availability", "Skill_Level", "Education_Quality"]
        "Market_Access" as ["Customer_Proximity", "Supplier_Access", "Competition_Level"]

Note: Multi-level pairwise comparisons
Let level1_comparisons be create_main_criteria_comparisons[]
Let level2_comparisons be Dictionary with:
    "Economic_Factors" as create_economic_sub_criteria_comparisons[]
    "Infrastructure" as create_infrastructure_sub_criteria_comparisons[]
    "Human_Resources" as create_hr_sub_criteria_comparisons[]
    "Market_Access" as create_market_sub_criteria_comparisons[]

Note: Alternative performance evaluations
Let alternative_evaluations be create_comprehensive_alternative_evaluations[]

Let hierarchical_result be MCDA.analyze_hierarchical_ahp with
    problem as facility_location_problem
    and level1_comparisons as level1_comparisons
    and level2_comparisons as level2_comparisons
    and alternative_evaluations as alternative_evaluations

Note: Extract hierarchical results
Let global_weights be hierarchical_result["global_criteria_weights"]
Let local_weights be hierarchical_result["local_criteria_weights"]
Let composite_scores be hierarchical_result["composite_scores"]
Let sensitivity_to_weights be hierarchical_result["sensitivity_analysis"]["weight_sensitivity"]
```

## TOPSIS Method

### Standard TOPSIS Analysis

```runa
Note: TOPSIS analysis for supplier selection
Let supplier_selection_problem be MCDA.create_decision_problem with Dictionary with:
    "alternatives" as ["Supplier_A", "Supplier_B", "Supplier_C", "Supplier_D", "Supplier_E"]
    "criteria" as ["Cost", "Quality", "Delivery_Time", "Service_Level", "Financial_Stability"]
    "criteria_types" as ["cost", "benefit", "cost", "benefit", "benefit"]  Note: Cost criteria to minimize
    "criteria_weights" as [0.3, 0.25, 0.2, 0.15, 0.1]

Note: Decision matrix with supplier performance data
Let decision_matrix be [
    [150000, 8.5, 12, 7.8, 8.2],  Note: Supplier_A
    [120000, 8.8, 15, 8.1, 7.9],  Note: Supplier_B
    [180000, 9.2, 10, 8.5, 9.1],  Note: Supplier_C
    [135000, 8.1, 14, 7.5, 8.8],  Note: Supplier_D
    [165000, 9.0, 11, 8.3, 8.5]   Note: Supplier_E
]

Note: Configure TOPSIS method
Let topsis_config be Config.get_config_for_algorithm with algorithm_name as "topsis"
Set topsis_config.parameters["normalization_method"] to "vector_normalization"
Set topsis_config.parameters["distance_metric"] to "euclidean"
Set topsis_config.parameters["ideal_solution_method"] to "max_benefit_min_cost"

Note: Perform TOPSIS analysis
Let topsis_result be MCDA.apply_topsis_method with
    decision_matrix as decision_matrix
    and criteria_weights as supplier_selection_problem["criteria_weights"]
    and criteria_types as supplier_selection_problem["criteria_types"]
    and config as topsis_config

Note: Extract TOPSIS results
Let closeness_coefficients be topsis_result["closeness_coefficients"]
Let ranking be topsis_result["ranking"]
Let ideal_solution be topsis_result["ideal_solution"]
Let negative_ideal_solution be topsis_result["negative_ideal_solution"]

Print "TOPSIS Supplier Ranking:"
For each rank and alternative_info in ranking:
    Let alternative_name be alternative_info["alternative"]
    Let closeness_score be alternative_info["closeness_coefficient"]
    Print rank with ". " with alternative_name with " (Score: " with closeness_score with ")"
```

### Fuzzy TOPSIS for Uncertainty Handling

```runa
Note: TOPSIS with fuzzy numbers for uncertain criteria
Let uncertain_decision_matrix be [
    [create_triangular_fuzzy_number[140000, 150000, 160000], create_triangular_fuzzy_number[8.0, 8.5, 9.0]],
    [create_triangular_fuzzy_number[110000, 120000, 130000], create_triangular_fuzzy_number[8.5, 8.8, 9.1]],
    [create_triangular_fuzzy_number[170000, 180000, 190000], create_triangular_fuzzy_number[9.0, 9.2, 9.4]]
]

Let fuzzy_weights be [
    create_triangular_fuzzy_number[0.25, 0.3, 0.35],   Note: Fuzzy weight for Cost
    create_triangular_fuzzy_number[0.2, 0.25, 0.3]     Note: Fuzzy weight for Quality
]

Let fuzzy_topsis_result be MCDA.apply_fuzzy_topsis with
    fuzzy_decision_matrix as uncertain_decision_matrix
    and fuzzy_weights as fuzzy_weights
    and defuzzification_method as "centroid"

Let fuzzy_ranking be fuzzy_topsis_result["fuzzy_ranking"]
Let defuzzified_scores be fuzzy_topsis_result["defuzzified_closeness_coefficients"]
```

## ELECTRE Family

### ELECTRE I (Outranking Relations)

```runa
Note: ELECTRE I for outranking-based decision making
Let investment_decision_problem be MCDA.create_decision_problem with Dictionary with:
    "alternatives" as ["Stock_Portfolio", "Bond_Portfolio", "Real_Estate", "Commodities"]
    "criteria" as ["Expected_Return", "Risk_Level", "Liquidity", "Diversification"]
    "criteria_types" as ["benefit", "cost", "benefit", "benefit"]

Let investment_matrix be [
    [12.5, 0.15, 8.0, 7.5],   Note: Stock_Portfolio
    [6.8, 0.05, 9.5, 6.0],    Note: Bond_Portfolio
    [9.2, 0.08, 4.0, 8.5],    Note: Real_Estate
    [11.0, 0.18, 6.5, 9.0]    Note: Commodities
]

Note: ELECTRE I parameters
Let electre_config be Config.get_config_for_algorithm with algorithm_name as "electre_1"
Set electre_config.parameters["concordance_threshold"] to 0.65
Set electre_config.parameters["discordance_threshold"] to 0.25
Set electre_config.parameters["criteria_weights"] to [0.4, 0.3, 0.2, 0.1]

Let electre_result be MCDA.apply_electre_1 with
    decision_matrix as investment_matrix
    and criteria_types as investment_decision_problem["criteria_types"]
    and config as electre_config

Note: Analyze outranking relations
Let outranking_matrix be electre_result["outranking_matrix"]
Let concordance_matrix be electre_result["concordance_matrix"]
Let discordance_matrix be electre_result["discordance_matrix"]
Let kernel_solutions be electre_result["kernel"]
Let dominated_alternatives be electre_result["dominated_alternatives"]

Print "ELECTRE I Outranking Analysis:"
Print "Kernel (non-dominated solutions): " with kernel_solutions
Print "Dominated alternatives: " with dominated_alternatives
```

### ELECTRE III (Pseudo-Criteria and Fuzzy Outranking)

```runa
Note: ELECTRE III with preference thresholds and veto thresholds
Let supplier_evaluation_problem be MCDA.create_electre_3_problem with Dictionary with:
    "alternatives" as ["Supplier_1", "Supplier_2", "Supplier_3", "Supplier_4"]
    "criteria" as ["Price", "Quality", "Delivery", "Service"]
    "criteria_weights" as [0.35, 0.30, 0.20, 0.15]
    "preference_thresholds" as [5000, 0.5, 2, 1.0]     Note: Below this, indifference
    "indifference_thresholds" as [2000, 0.2, 1, 0.5]   Note: Strict indifference
    "veto_thresholds" as [20000, 2.0, 10, 4.0]         Note: Veto large differences

Let electre_3_matrix be [
    [95000, 8.2, 14, 7.8],   Note: Supplier_1
    [105000, 8.8, 12, 8.5],  Note: Supplier_2
    [88000, 7.9, 16, 7.2],   Note: Supplier_3
    [112000, 9.1, 11, 8.9]   Note: Supplier_4
]

Let electre_3_result be MCDA.apply_electre_3 with
    decision_matrix as electre_3_matrix
    and problem_definition as supplier_evaluation_problem

Note: Extract fuzzy outranking relations
Let credibility_matrix be electre_3_result["credibility_matrix"]
Let distillation_result be electre_3_result["distillation"]
Let descending_ranking be distillation_result["descending_distillation"]
Let ascending_ranking be distillation_result["ascending_distillation"]
Let final_ranking be distillation_result["final_ranking"]

Print "ELECTRE III Final Ranking: " with final_ranking
```

## PROMETHEE Methods

### PROMETHEE II Complete Ranking

```runa
Note: PROMETHEE II for complete preference ranking
Let technology_selection_problem be MCDA.create_promethee_problem with Dictionary with:
    "alternatives" as ["Tech_A", "Tech_B", "Tech_C", "Tech_D"]
    "criteria" as ["Development_Cost", "Time_to_Market", "Technical_Risk", "Market_Potential"]
    "criteria_weights" as [0.25, 0.30, 0.20, 0.25]
    "preference_functions" as ["linear", "step", "gaussian", "level"]
    "preference_parameters" as Dictionary with:
        "Development_Cost" as Dictionary with: "threshold" as 50000
        "Time_to_Market" as Dictionary with: "threshold" as 3
        "Technical_Risk" as Dictionary with: "sigma" as 1.5
        "Market_Potential" as Dictionary with: "q" as 2, "p" as 5

Let technology_matrix be [
    [200000, 12, 6.5, 8.2],   Note: Tech_A
    [250000, 8, 4.8, 9.1],    Note: Tech_B
    [180000, 15, 7.2, 7.8],   Note: Tech_C
    [220000, 10, 5.5, 8.7]    Note: Tech_D
]

Let promethee_result be MCDA.apply_promethee_2 with
    decision_matrix as technology_matrix
    and problem_definition as technology_selection_problem

Note: Extract PROMETHEE results
Let positive_flows be promethee_result["positive_flows"]
Let negative_flows be promethee_result["negative_flows"]
Let net_flows be promethee_result["net_flows"]
Let complete_ranking be promethee_result["complete_ranking"]
Let pairwise_preferences be promethee_result["pairwise_preference_degrees"]

Print "PROMETHEE II Technology Ranking:"
For each rank and tech_info in complete_ranking:
    Print rank with ". " with tech_info["alternative"] with " (Net Flow: " with tech_info["net_flow"] with ")"
```

### PROMETHEE V with Constraints

```runa
Note: PROMETHEE V for portfolio selection with constraints
Let portfolio_selection_problem be MCDA.create_promethee_v_problem with Dictionary with:
    "alternatives" as ["Project_1", "Project_2", "Project_3", "Project_4", "Project_5"]
    "criteria" as ["NPV", "ROI", "Strategic_Fit", "Risk_Level"]
    "criteria_weights" as [0.4, 0.3, 0.2, 0.1]
    "budget_constraint" as 1000000
    "selection_constraints" as Dictionary with:
        "max_projects" as 3
        "min_strategic_fit" as 7.0
        "max_total_risk" as 15.0

Let project_data be [
    [150000, 0.25, 8.5, 4.2, 300000],  Note: Project_1 [NPV, ROI, Strategic_Fit, Risk, Cost]
    [200000, 0.30, 9.1, 5.8, 450000],  Note: Project_2
    [120000, 0.18, 7.8, 3.5, 250000],  Note: Project_3
    [180000, 0.22, 8.9, 6.1, 380000],  Note: Project_4
    [95000, 0.15, 7.2, 2.9, 200000]    Note: Project_5
]

Let promethee_v_result be MCDA.apply_promethee_v with
    alternatives_data as project_data
    and problem_definition as portfolio_selection_problem
    and optimization_method as "branch_and_bound"

Let optimal_portfolio be promethee_v_result["selected_projects"]
Let portfolio_performance be promethee_v_result["portfolio_metrics"]
Let constraint_satisfaction be promethee_v_result["constraint_validation"]
```

## Advanced Techniques

### Group Decision Making

```runa
Note: Aggregating multiple decision makers' preferences
Let group_decision_problem be MCDA.create_group_decision_problem with Dictionary with:
    "decision_makers" as ["Expert_1", "Expert_2", "Expert_3", "Manager_1", "Manager_2"]
    "decision_maker_weights" as [0.25, 0.25, 0.20, 0.15, 0.15]  Note: Expert knowledge weighted higher
    "alternatives" as ["Option_A", "Option_B", "Option_C"]
    "criteria" as ["Technical_Feasibility", "Cost_Effectiveness", "Market_Impact"]
    "aggregation_method" as "weighted_geometric_mean"

Note: Individual decision maker evaluations
Let individual_evaluations be Dictionary with:
    "Expert_1" as Dictionary with:
        "criteria_weights" as [0.5, 0.3, 0.2]
        "alternative_scores" as [[8.5, 7.2, 9.1], [9.0, 6.8, 8.5], [7.8, 8.1, 8.9]]
    "Expert_2" as Dictionary with:
        "criteria_weights" as [0.4, 0.35, 0.25]
        "alternative_scores" as [[8.8, 7.5, 8.7], [8.2, 7.1, 9.2], [8.0, 8.3, 8.4]]
    "Expert_3" as Dictionary with:
        "criteria_weights" as [0.45, 0.25, 0.3]
        "alternative_scores" as [[8.1, 7.8, 8.9], [8.9, 6.9, 8.8], [7.9, 8.0, 9.0]]

Note: Aggregate group preferences
Let group_result be MCDA.perform_group_decision_analysis with
    problem as group_decision_problem
    and individual_evaluations as individual_evaluations
    and consensus_method as "social_choice_function"

Let aggregated_ranking be group_result["group_ranking"]
Let consensus_measure be group_result["consensus_level"]
Let individual_vs_group_analysis be group_result["disagreement_analysis"]

Print "Group Decision Analysis:"
Print "Consensus level: " with consensus_measure
Print "Group ranking: " with aggregated_ranking
If consensus_measure < 0.7:
    Print "Low consensus detected. Individual disagreements:"
    Print individual_vs_group_analysis["major_disagreements"]
```

### Multi-Objective Optimization Integration

```runa
Note: Integrate MCDA with multi-objective optimization
Let moo_mcda_problem be MCDA.create_moo_integrated_problem with Dictionary with:
    "decision_variables" as ["x1", "x2", "x3", "x4"]
    "variable_bounds" as [[0, 100], [0, 50], [10, 200], [5, 75]]
    "objective_functions" as ["minimize_cost", "maximize_quality", "minimize_time"]
    "constraint_functions" as ["resource_constraint", "feasibility_constraint"]
    "mcda_criteria" as ["Cost", "Quality", "Time", "Risk", "Sustainability"]

Note: Generate Pareto-optimal solutions
Let pareto_solutions be MCDA.generate_pareto_optimal_solutions with
    problem as moo_mcda_problem
    and algorithm as "nsga_ii"
    and population_size as 100
    and generations as 500

Note: Apply MCDA to select from Pareto set
Let pareto_mcda_analysis be MCDA.apply_mcda_to_pareto_set with
    pareto_solutions as pareto_solutions["pareto_front"]
    and mcda_method as "promethee_2"
    and decision_maker_preferences as create_dm_preferences[]

Let final_solution_recommendation be pareto_mcda_analysis["recommended_solution"]
Let solution_robustness as pareto_mcda_analysis["robustness_analysis"]
```

## Sensitivity Analysis

### Weight Sensitivity Analysis

```runa
Note: Comprehensive sensitivity analysis for criteria weights
Process called "perform_comprehensive_sensitivity_analysis" that takes
    mcda_result as MCDAResult and
    sensitivity_config as Dictionary returns Dictionary:
    
    Note: Weight sensitivity analysis
    Let weight_sensitivity be MCDA.analyze_weight_sensitivity with
        original_result as mcda_result
        and weight_variation_range as sensitivity_config["weight_range"] or 0.2
        and analysis_method as "monte_carlo"
        and simulation_runs as sensitivity_config["simulation_runs"] or 10000
    
    Note: Criteria importance analysis
    Let importance_analysis be MCDA.analyze_criteria_importance with
        mcda_result as mcda_result
        and importance_measures as ["weight_stability", "rank_reversal", "score_impact"]
    
    Note: Alternative performance sensitivity
    Let performance_sensitivity be MCDA.analyze_performance_sensitivity with
        mcda_result as mcda_result
        and performance_variation as sensitivity_config["performance_range"] or 0.15
    
    Note: Method sensitivity (compare different MCDA methods)
    Let method_sensitivity be MCDA.compare_mcda_methods with
        problem_data as mcda_result.problem_data
        and methods as ["ahp", "topsis", "electre_1", "promethee_2"]
        and consistency_measure as "ranking_correlation"
    
    Return Dictionary with:
        "weight_sensitivity" as weight_sensitivity
        "criteria_importance" as importance_analysis  
        "performance_sensitivity" as performance_sensitivity
        "method_sensitivity" as method_sensitivity
        "overall_robustness" as calculate_overall_robustness with weight_sensitivity and performance_sensitivity
```

### Rank Reversal Analysis

```runa
Note: Detect and analyze rank reversal phenomena
Let rank_reversal_analysis be MCDA.analyze_rank_reversal with
    original_problem as mcda_result.problem_data
    and test_scenarios as [
        "add_irrelevant_alternative",
        "remove_dominated_alternative", 
        "scale_criteria_values",
        "modify_criteria_weights"
    ]

For each scenario and reversal_result in rank_reversal_analysis:
    If reversal_result["rank_reversal_detected"]:
        Let affected_alternatives be reversal_result["affected_alternatives"]
        Let reversal_magnitude be reversal_result["reversal_magnitude"]
        Print "Rank reversal detected in " with scenario
        Print "  Affected alternatives: " with affected_alternatives
        Print "  Magnitude: " with reversal_magnitude
        
        Note: Provide recommendations for handling rank reversal
        Let reversal_recommendations be reversal_result["recommendations"]
        Print "  Recommendations: " with reversal_recommendations
```

## Integration Examples

### AI Agent Decision Framework

```runa
Note: Complete AI agent multi-criteria decision framework
Import "ai/agent/core" as Agent
Import "ai/decision/multi_criteria" as MCDA
Import "ai/decision/config" as Config

Process called "ai_agent_mcda_framework" that takes 
    agent as Agent and 
    decision_context as Dictionary returns Dictionary:
    
    Note: Analyze decision complexity and select appropriate MCDA method
    Let complexity_analysis be MCDA.analyze_decision_complexity with decision_context
    
    Let selected_method as String
    Match complexity_analysis["complexity_level"]:
        When "low":
            Set selected_method to "weighted_sum"
        When "medium":
            Set selected_method to "topsis"
        When "high":
            Set selected_method to "ahp"
        When "very_high":
            Set selected_method to "electre_3"
        Otherwise:
            Set selected_method to "promethee_2"
    
    Note: Create agent-specific configuration
    Let agent_config be Config.create_agent_specific_mcda_config with
        agent_profile as agent.profile
        and decision_context as decision_context
        and selected_method as selected_method
    
    Note: Perform MCDA analysis
    Let mcda_analysis be MCDA.perform_adaptive_analysis with
        alternatives as decision_context["alternatives"]
        and criteria as decision_context["criteria"]
        and method as selected_method
        and config as agent_config
    
    Note: Add confidence and explanation
    Let analysis_with_confidence be MCDA.add_confidence_measures with
        analysis as mcda_analysis
        and confidence_method as "bootstrap_sampling"
    
    Let explanation be MCDA.generate_decision_explanation with
        analysis as analysis_with_confidence
        and explanation_level as agent.preferences["explanation_detail"]
    
    Return Dictionary with:
        "recommendation" as analysis_with_confidence["top_alternative"]
        "confidence_score" as analysis_with_confidence["confidence_measures"]["overall_confidence"]
        "full_ranking" as analysis_with_confidence["ranking"]
        "sensitivity_summary" as analysis_with_confidence["sensitivity_summary"]
        "explanation" as explanation
        "method_used" as selected_method
```

### Supply Chain Optimization

```runa
Note: Multi-criteria supply chain partner selection
Process called "supply_chain_partner_selection" that takes 
    potential_partners as List[Dictionary] and 
    selection_criteria as Dictionary returns Dictionary:
    
    Note: Define comprehensive evaluation framework
    Let evaluation_framework be MCDA.create_supply_chain_evaluation_framework with Dictionary with:
        "primary_criteria" as ["Cost", "Quality", "Reliability", "Flexibility", "Sustainability"]
        "sub_criteria" as Dictionary with:
            "Cost" as ["Unit_Price", "Transportation_Cost", "Inventory_Cost", "Total_Cost_of_Ownership"]
            "Quality" as ["Product_Quality", "Process_Quality", "Certification_Level", "Defect_Rate"]
            "Reliability" as ["Delivery_Performance", "Financial_Stability", "Risk_Profile"]
            "Flexibility" as ["Capacity_Scalability", "Product_Customization", "Response_Time"]
            "Sustainability" as ["Environmental_Impact", "Social_Responsibility", "Compliance"]
        "evaluation_method" as "hybrid_ahp_topsis"
    
    Note: Collect and standardize partner data
    Let standardized_data be MCDA.standardize_partner_data with
        partners as potential_partners
        and framework as evaluation_framework
    
    Note: Apply hybrid AHP-TOPSIS methodology
    Let ahp_weights be MCDA.compute_ahp_criteria_weights with evaluation_framework
    Let topsis_ranking be MCDA.apply_topsis_with_ahp_weights with
        partner_data as standardized_data
        and criteria_weights as ahp_weights
    
    Note: Perform risk-adjusted analysis
    let risk_adjusted_ranking be MCDA.apply_risk_adjustments with
        base_ranking as topsis_ranking
        and risk_factors as extract_risk_factors with potential_partners
        and risk_tolerance as "moderate"
    
    Note: Generate comprehensive partner recommendations
    Return Dictionary with:
        "recommended_partners" as risk_adjusted_ranking["top_3_partners"]
        "detailed_analysis" as risk_adjusted_ranking["full_analysis"]
        "risk_assessment" as risk_adjusted_ranking["risk_summary"]
        "implementation_roadmap" as generate_implementation_plan with risk_adjusted_ranking
        "monitoring_framework" as create_partner_monitoring_system with evaluation_framework
```

## Performance Optimization

### High-Performance MCDA Configuration

```runa
Note: Optimized configuration for high-throughput MCDA
Let high_performance_config be Config.create_high_performance_mcda_config with Dictionary with:
    "matrix_operations" as "vectorized_blas"
    "eigenvalue_computation" as "optimized_lapack"
    "parallel_processing" as true
    "max_workers" as 8
    "memory_optimization" as true
    "result_caching" as true

Note: Batch processing for multiple decision problems
Process called "batch_mcda_processing" that takes 
    decision_problems as List[MultiCriteriaDecisionProblem] and
    processing_config as Dictionary returns List[MCDAResult]:
    
    Let batch_results be list containing
    Let problem_batches be partition_problems with 
        problems as decision_problems
        and batch_size as processing_config["batch_size"] or 10
    
    For each batch in problem_batches:
        Let batch_result be MCDA.process_problem_batch with
            problems as batch
            and config as high_performance_config
            and parallel as true
        
        Add batch_result to batch_results
    
    Return flatten_batch_results with batch_results
```

### Memory-Efficient Processing

```runa
Note: Handle large-scale decision problems efficiently
Let memory_efficient_config be Config.create_memory_efficient_config with Dictionary with:
    "streaming_processing" as true
    "matrix_compression" as true
    "garbage_collection_aggressive" as true
    "disk_based_storage" as true

Process called "large_scale_mcda_analysis" that takes 
    large_problem as MultiCriteriaDecisionProblem returns MCDAResult:
    
    Note: Check if problem size exceeds memory limits
    Let problem_size_analysis be MCDA.analyze_problem_size with large_problem
    
    If problem_size_analysis["memory_required"] > memory_efficient_config["memory_limit"]:
        Note: Use streaming approach
        Return MCDA.streaming_mcda_analysis with
            problem as large_problem
            and config as memory_efficient_config
    Otherwise:
        Note: Standard in-memory processing
        Return MCDA.standard_mcda_analysis with
            problem as large_problem
            and config as memory_efficient_config
```

## Best Practices

### Method Selection Guidelines

```runa
Note: Systematic method selection based on problem characteristics
Process called "select_optimal_mcda_method" that takes 
    problem_characteristics as Dictionary returns String:
    
    Let method_recommendation as String
    
    Note: Decision tree for method selection
    If problem_characteristics["criteria_count"] <= 5 and problem_characteristics["alternative_count"] <= 10:
        If problem_characteristics["has_hierarchical_structure"]:
            Set method_recommendation to "ahp"
        Otherwise if problem_characteristics["has_uncertainty"]:
            Set method_recommendation to "fuzzy_topsis"
        Otherwise:
            Set method_recommendation to "topsis"
    
    Otherwise if problem_characteristics["has_outranking_preferences"]:
        If problem_characteristics["requires_partial_ranking"]:
            Set method_recommendation to "electre_1"
        Otherwise:
            Set method_recommendation to "electre_3"
    
    Otherwise if problem_characteristics["has_preference_functions"]:
        Set method_recommendation to "promethee_2"
    
    Otherwise:
        Note: Default to robust method for complex problems
        Set method_recommendation to "topsis"
    
    Return method_recommendation
```

### Validation and Quality Assurance

```runa
Note: Comprehensive MCDA result validation
Process called "validate_mcda_results" that takes 
    mcda_result as MCDAResult and
    validation_config as Dictionary returns Dictionary:
    
    Let validation_results be Dictionary with:
        "is_valid" as true
        "quality_score" as 0.0
        "warnings" as list containing
        "recommendations" as list containing
    
    Note: Consistency validation
    Let consistency_check be validate_consistency with mcda_result
    If consistency_check["consistency_ratio"] > validation_config["max_consistency_ratio"]:
        Add "High inconsistency detected in pairwise comparisons" to validation_results["warnings"]
        Set validation_results["quality_score"] to validation_results["quality_score"] minus 0.2
    
    Note: Sensitivity validation
    Let sensitivity_check be validate_sensitivity with mcda_result
    If sensitivity_check["ranking_stability"] < validation_config["min_stability"]:
        Add "Low ranking stability - results sensitive to input changes" to validation_results["warnings"]
        Set validation_results["quality_score"] to validation_results["quality_score"] minus 0.15
    
    Note: Method appropriateness validation
    Let method_validation be validate_method_choice with mcda_result
    If not method_validation["appropriate"]:
        Add "Selected method may not be optimal for this problem type" to validation_results["warnings"]
        Add method_validation["recommended_method"] to validation_results["recommendations"]
    
    Return validation_results
```

The multi-criteria decision analysis module provides AI agents and human decision-makers with world-class capabilities for handling complex decisions involving multiple, often conflicting objectives. By implementing rigorous mathematical foundations with practical usability considerations, it delivers production-ready decision support that scales from simple choices to enterprise-wide strategic decisions.