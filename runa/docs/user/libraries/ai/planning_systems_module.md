# Planning Systems Module

## Overview

The Planning Systems module provides comprehensive automated planning capabilities for the Runa AI framework. This enterprise-grade planning infrastructure includes hierarchical planning, temporal scheduling, multi-agent coordination, and contingency planning with performance competitive with leading AI planning platforms.

## Quick Start

```runa
Import "ai.planning.hierarchical" as hierarchical_planning
Import "ai.planning.temporal" as temporal_planning

Note: Create a simple hierarchical planner
Let planner_config be dictionary with:
    "decomposition_strategy" as "top_down",
    "planning_algorithm" as "htn_planner",
    "domain_model" as "methods_and_operators",
    "optimization_objective" as "minimize_makespan"

Let planner be hierarchical_planning.create_hierarchical_planner[planner_config]

Note: Define a planning problem
Let problem be dictionary with:
    "initial_state" as dictionary with:
        "robot_location" as "kitchen",
        "coffee_status" as "empty",
        "user_waiting" as true
    "goal_state" as dictionary with:
        "coffee_status" as "served",
        "user_satisfaction" as "high"
    "available_actions" as list containing "move", "pick_up", "brew_coffee", "serve"

Note: Generate a plan
Let plan_result be hierarchical_planning.generate_plan[planner, problem]
Display "Generated plan with " with message plan_result["plan_length"] with message " steps"
```

## Architecture Components

### Hierarchical Planning
- **HTN Planning**: Hierarchical Task Network decomposition and refinement
- **Goal Decomposition**: Abstract goal breakdown into achievable subgoals
- **Method Selection**: Intelligent method selection for task decomposition
- **Plan Refinement**: Iterative plan improvement and optimization

### Temporal Planning
- **Temporal Constraints**: Time-aware planning with deadlines and durations
- **Resource Scheduling**: Resource allocation and capacity planning
- **Timeline Management**: Concurrent action execution and synchronization
- **Temporal Optimization**: Makespan and resource utilization optimization

### Multi-Agent Planning
- **Distributed Planning**: Coordinated planning across multiple agents
- **Task Allocation**: Optimal task distribution among team members
- **Coalition Formation**: Dynamic team formation for collaborative planning
- **Negotiation Protocols**: Conflict resolution and consensus building

### Contingency Planning
- **Failure Recovery**: Robust planning under uncertainty and failures
- **Adaptive Replanning**: Dynamic plan adaptation to changing conditions
- **Risk Assessment**: Probabilistic risk analysis and mitigation
- **Plan Monitoring**: Real-time plan execution monitoring and control

## API Reference

### Hierarchical Planning Functions

#### `create_hierarchical_planner[config]`
Creates a hierarchical task network planner with specified configuration.

**Parameters:**
- `config` (Dictionary): Planner configuration with algorithms, domain models, and optimization settings

**Returns:**
- `HierarchicalPlanner`: Configured hierarchical planner instance

**Example:**
```runa
Let config be dictionary with:
    "decomposition_strategy" as "mixed_initiative",
    "planning_algorithm" as "shop2",
    "domain_model" as "htn_domain",
    "search_strategy" as "depth_first",
    "optimization_objective" as "minimize_cost",
    "max_search_depth" as 20

Let htn_planner be hierarchical_planning.create_hierarchical_planner[config]
```

#### `define_planning_domain[planner, domain_definition]`
Defines the planning domain with methods, operators, and constraints.

**Parameters:**
- `planner` (HierarchicalPlanner): Target planner instance
- `domain_definition` (Dictionary): Domain specification with methods and operators

**Returns:**
- `Boolean`: Success status of domain definition

**Example:**
```runa
Let domain_definition be dictionary with:
    "methods" as dictionary with:
        "make_coffee" as dictionary with:
            "preconditions" as list containing "robot_in_kitchen", "coffee_beans_available",
            "decomposition" as list containing "grind_beans", "brew_coffee", "serve_coffee"
        "clean_kitchen" as dictionary with:
            "preconditions" as list containing "kitchen_dirty",
            "decomposition" as list containing "wash_dishes", "wipe_counters", "sweep_floor"
    "operators" as dictionary with:
        "grind_beans" as dictionary with:
            "preconditions" as list containing "beans_available", "grinder_ready",
            "effects" as list containing "beans_ground", "grinder_used",
            "duration" as 30
        "brew_coffee" as dictionary with:
            "preconditions" as list containing "beans_ground", "water_available",
            "effects" as list containing "coffee_brewed",
            "duration" as 180

Let domain_result be hierarchical_planning.define_planning_domain[htn_planner, domain_definition]
```

#### `generate_plan[planner, problem]`
Generates a hierarchical plan for the specified planning problem.

**Parameters:**
- `planner` (HierarchicalPlanner): Planner instance to use
- `problem` (Dictionary): Planning problem with initial state, goals, and constraints

**Returns:**
- `PlanResult`: Generated plan with actions, timeline, and metadata

**Example:**
```runa
Let problem be dictionary with:
    "initial_state" as dictionary with:
        "robot_location" as "living_room",
        "battery_level" as 0.8,
        "task_queue" as list containing "make_coffee", "clean_kitchen"
    "goal_state" as dictionary with:
        "all_tasks_completed" as true,
        "user_satisfaction" as "high"
    "constraints" as dictionary with:
        "max_execution_time" as 3600,
        "resource_limits" as dictionary with: "energy_budget" as 0.6

Let plan_result be hierarchical_planning.generate_plan[htn_planner, problem]

If plan_result["success"]:
    Display "Plan generated successfully:"
    For each action in plan_result["plan"]:
        Display "  " with message action["name"] with message " (duration: " with message action["duration"] with message "s)"
```

### Temporal Planning Functions

#### `create_temporal_planner[config]`
Creates a temporal planner with scheduling and resource management capabilities.

**Parameters:**
- `config` (Dictionary): Temporal planner configuration with algorithms and constraints

**Returns:**
- `TemporalPlanner`: Configured temporal planner instance

**Example:**
```runa
Let config be dictionary with:
    "scheduling_algorithm" as "critical_path_method",
    "resource_allocation" as "earliest_start_time",
    "temporal_network" as "simple_temporal_network",
    "optimization_objective" as "minimize_makespan",
    "uncertainty_handling" as "robust_scheduling"

Let temporal_planner be temporal_planning.create_temporal_planner[config]
```

#### `schedule_activities[planner, activities, resources, constraints]`
Schedules activities with temporal and resource constraints.

**Parameters:**
- `planner` (TemporalPlanner): Temporal planner instance
- `activities` (List[Dictionary]): Activities to schedule with durations and dependencies
- `resources` (Dictionary): Available resources and capacities
- `constraints` (Dictionary): Temporal and resource constraints

**Returns:**
- `ScheduleResult`: Optimized schedule with resource allocations

**Example:**
```runa
Let activities be list containing:
    dictionary with:
        "id" as "task_a",
        "duration" as 120,
        "resource_requirements" as dictionary with: "cpu" as 2, "memory" as 4,
        "dependencies" as list containing:
    dictionary with:
        "id" as "task_b", 
        "duration" as 180,
        "resource_requirements" as dictionary with: "cpu" as 1, "memory" as 2,
        "dependencies" as list containing "task_a"

Let resources be dictionary with:
    "cpu" as dictionary with: "capacity" as 4, "renewable" as true,
    "memory" as dictionary with: "capacity" as 8, "renewable" as true

Let constraints be dictionary with:
    "deadline" as 600,
    "resource_conflicts" as false,
    "precedence_constraints" as true

Let schedule_result be temporal_planning.schedule_activities[temporal_planner, activities, resources, constraints]
```

### Multi-Agent Planning Functions

#### `create_multiagent_planner[agents, coordination_config]`
Creates a multi-agent planner for coordinated team planning.

**Parameters:**
- `agents` (List[Agent]): Agent team members with capabilities
- `coordination_config` (Dictionary): Coordination protocols and mechanisms

**Returns:**
- `MultiAgentPlanner`: Configured multi-agent planner instance

**Example:**
```runa
Let coordination_config be dictionary with:
    "coordination_protocol" as "distributed_consensus",
    "task_allocation_method" as "auction_based",
    "communication_strategy" as "message_passing",
    "conflict_resolution" as "negotiation",
    "load_balancing" as true

Let multiagent_planner be multiagent_planning.create_multiagent_planner[agent_team, coordination_config]
```

#### `allocate_tasks[planner, tasks, allocation_strategy]`
Allocates tasks optimally among team members.

**Parameters:**
- `planner` (MultiAgentPlanner): Multi-agent planner instance
- `tasks` (List[Dictionary]): Tasks to be allocated with requirements
- `allocation_strategy` (String): Allocation method ("auction", "capability_based", "load_balanced")

**Returns:**
- `TaskAllocation`: Optimal task assignment with justification

**Example:**
```runa
Let tasks be list containing:
    dictionary with:
        "task_id" as "data_collection",
        "requirements" as list containing "sensor_access", "data_processing",
        "priority" as "high",
        "deadline" as 300
    dictionary with:
        "task_id" as "analysis",
        "requirements" as list containing "computation", "model_inference",
        "priority" as "medium",
        "deadline" as 600

Let allocation_result be multiagent_planning.allocate_tasks[multiagent_planner, tasks, "capability_based"]

For each assignment in allocation_result["assignments"]:
    Display assignment["agent_id"] with message " assigned to " with message assignment["task_id"]
    Display "  Justification: " with message assignment["justification"]
```

## Advanced Features

### Contingency Planning and Adaptation

Handle uncertainty and dynamic environments:

```runa
Import "ai.planning.contingency" as contingency_planning

Note: Create contingency planner
Let contingency_config be dictionary with:
    "uncertainty_model" as "probabilistic",
    "replanning_triggers" as list containing "plan_failure", "goal_change", "environment_change",
    "adaptation_strategy" as "incremental_replanning",
    "risk_tolerance" as 0.2

Let contingency_planner be contingency_planning.create_contingency_planner[contingency_config]

Note: Generate robust plans with alternatives
Let robust_plan_result be contingency_planning.generate_robust_plan[contingency_planner, problem, dictionary with:
    "failure_scenarios" as list containing "resource_unavailable", "action_failure", "time_constraint_violation",
    "alternative_strategies" as 3,
    "confidence_threshold" as 0.8
]
```

### Plan Execution and Monitoring

Execute plans with real-time monitoring:

```runa
Import "ai.planning.execution" as plan_execution

Note: Create plan executor
Let execution_config be dictionary with:
    "execution_strategy" as "event_driven",
    "monitoring_frequency_ms" as 1000,
    "failure_detection" as true,
    "replanning_enabled" as true,
    "state_estimation" as "particle_filter"

Let plan_executor be plan_execution.create_plan_executor[execution_config]

Note: Execute plan with monitoring
Let execution_result be plan_execution.execute_plan[plan_executor, generated_plan, dictionary with:
    "real_time_monitoring" as true,
    "adaptation_enabled" as true,
    "progress_reporting" as true
]
```

### Optimization and Meta-Planning

Optimize planning performance and strategies:

```runa
Import "ai.planning.optimization" as planning_optimization

Note: Configure planning optimization
Let optimization_config be dictionary with:
    "search_optimization" as true,
    "heuristic_learning" as true,
    "plan_caching" as true,
    "parallel_search" as true,
    "meta_reasoning" as true

planning_optimization.optimize_planner[htn_planner, optimization_config]

Note: Learn from planning experience
Let learning_config be dictionary with:
    "experience_collection" as true,
    "pattern_recognition" as true,
    "strategy_adaptation" as true,
    "performance_prediction" as true

planning_optimization.enable_learning[htn_planner, learning_config]
```

## Performance Optimization

### Scalability Features

Handle large-scale planning problems:

```runa
Import "ai.planning.scalability" as planning_scale

Note: Configure distributed planning
Let distributed_config be dictionary with:
    "distributed_search" as true,
    "node_count" as 4,
    "load_balancing" as "dynamic",
    "communication_optimization" as true,
    "result_merging" as "best_first"

Let distributed_planner be planning_scale.create_distributed_planner[base_planner, distributed_config]
```

### Memory and Computation Optimization

Optimize resource usage for planning:

```runa
Import "ai.planning.performance" as planning_perf

Let performance_config be dictionary with:
    "memory_management" as "garbage_collection",
    "search_pruning" as true,
    "state_space_reduction" as true,
    "incremental_planning" as true,
    "result_caching" as true

planning_perf.optimize_performance[planner, performance_config]
```

## Integration Examples

### Integration with Agent Systems

```runa
Import "ai.agent.core" as agent_core
Import "ai.planning.integration" as planning_integration

Let planning_agent be agent_core.create_deliberative_agent[agent_config]
planning_integration.connect_planner_to_agent[htn_planner, planning_agent]

Note: Use planning for agent decision making
Let decision_result be planning_integration.plan_agent_actions[planning_agent, current_situation]
```

### Integration with Knowledge Systems

```runa
Import "ai.knowledge.core" as knowledge
Import "ai.planning.integration" as planning_integration

Let knowledge_base be knowledge.create_knowledge_base[kb_config]
planning_integration.connect_knowledge_base[htn_planner, knowledge_base]

Note: Use knowledge for domain modeling
Let domain_knowledge = planning_integration.extract_planning_domain[knowledge_base, domain_query]
```

## Best Practices

### Planning Domain Design
1. **Modular Decomposition**: Design hierarchical methods with clear abstractions
2. **Efficient Operators**: Create atomic operators with minimal preconditions
3. **Constraint Modeling**: Model temporal and resource constraints accurately
4. **Domain Knowledge**: Leverage domain expertise for method design

### Performance Guidelines
1. **Search Optimization**: Use appropriate search strategies and heuristics
2. **State Representation**: Design efficient state representations
3. **Pruning Strategies**: Implement effective search space pruning
4. **Incremental Planning**: Use incremental approaches for dynamic environments

### Example: Production Planning System

```runa
Process called "create_production_planning_system" that takes config as Dictionary returns Dictionary:
    Note: Create core planning components
    Let hierarchical_planner be hierarchical_planning.create_hierarchical_planner[config["hierarchical_config"]]
    Let temporal_planner be temporal_planning.create_temporal_planner[config["temporal_config"]]
    Let multiagent_planner be multiagent_planning.create_multiagent_planner[config["agents"], config["coordination_config"]]
    Let contingency_planner be contingency_planning.create_contingency_planner[config["contingency_config"]]
    
    Note: Create integrated planning system
    Let integrated_config be dictionary with:
        "planners" as list containing hierarchical_planner, temporal_planner, multiagent_planner, contingency_planner,
        "orchestration_strategy" as "hierarchical_coordination",
        "plan_integration" as "merge_and_optimize",
        "conflict_resolution" as "priority_based",
        "performance_monitoring" as true
    
    Let planning_system = planning_integration.create_integrated_system[integrated_config]
    
    Note: Configure optimization and monitoring
    planning_optimization.optimize_system[planning_system, config["optimization_config"]]
    
    Return dictionary with:
        "system" as planning_system,
        "capabilities" as list containing "hierarchical", "temporal", "multiagent", "contingency",
        "status" as "operational"

Let production_config be dictionary with:
    "hierarchical_config" as dictionary with:
        "decomposition_strategy" as "mixed_initiative",
        "optimization_objective" as "minimize_cost_and_time"
    "temporal_config" as dictionary with:
        "scheduling_algorithm" as "constraint_satisfaction",
        "resource_optimization" as true
    "agents" as agent_team,
    "coordination_config" as dictionary with:
        "coordination_protocol" as "contract_net",
        "load_balancing" as true
    "contingency_config" as dictionary with:
        "uncertainty_handling" as "robust_planning",
        "replanning_enabled" as true
    "optimization_config" as dictionary with:
        "parallel_processing" as true,
        "caching_enabled" as true,
        "learning_enabled" as true

Let production_planning_system be create_production_planning_system[production_config]
```

## Troubleshooting

### Common Issues

**Plan Generation Failures**
- Check domain definition completeness
- Verify goal reachability from initial state
- Review constraint consistency

**Performance Bottlenecks**
- Optimize search strategies and heuristics
- Implement state space pruning
- Use incremental planning approaches

**Resource Conflicts**
- Review resource capacity definitions
- Check temporal constraint consistency
- Implement conflict resolution strategies

### Debugging Tools

```runa
Import "ai.planning.debug" as planning_debug

Note: Enable comprehensive debugging
planning_debug.enable_debug_mode[planning_system, dictionary with:
    "trace_search" as true,
    "log_decomposition_steps" as true,
    "monitor_resource_usage" as true,
    "capture_plan_states" as true
]

Let debug_report be planning_debug.generate_debug_report[planning_system]
```

This planning systems module provides a comprehensive foundation for automated planning in Runa applications. The combination of hierarchical decomposition, temporal scheduling, multi-agent coordination, and contingency planning makes it suitable for complex real-world planning problems across various domains including robotics, manufacturing, logistics, and resource management.