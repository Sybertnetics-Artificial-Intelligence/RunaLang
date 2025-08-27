# Agent Goals Module

The Agent Goals module provides comprehensive goal and intent management for agents, including goal creation, decomposition, retry strategies, monitoring, and adaptive execution.

## Overview

This production-grade module enables agents to pursue complex, hierarchical objectives with advanced planning, execution tracking, adaptive strategies, and comprehensive performance optimization.

## Core Types

### AgentGoal
```runa
Type called "AgentGoal":
    id as String                     Note: Unique goal identifier
    description as String            Note: Goal description
    status as String                Note: Current status
    subgoals as List[AgentGoal]     Note: Child goals
    retries as Integer              Note: Current retry count
    max_retries as Integer          Note: Maximum retry attempts
    progress as Number              Note: Completion progress (0-1)
    result as Any                   Note: Goal result
    error as String                 Note: Error message if failed
    priority as Integer             Note: Goal priority (1-10)
    deadline as Number              Note: Goal deadline timestamp
    created_at as Number            Note: Creation timestamp
    updated_at as Number            Note: Last update timestamp
    parent_goal as String           Note: Parent goal ID
    dependencies as List[String]    Note: Goal dependencies
    resource_requirements as Dictionary[String, Number] Note: Resource needs
    performance_metrics as Dictionary[String, Number] Note: Performance data
    execution_strategy as String    Note: Execution strategy type
    adaptive_parameters as Dictionary[String, Any] Note: Adaptive parameters
    audit_trail as List[Dictionary[String, Any]] Note: Execution history
```

### GoalManager
```runa
Type called "GoalManager":
    goals as Dictionary[String, AgentGoal] Note: All managed goals
    goal_hierarchy as Dictionary[String, List[String]] Note: Goal hierarchy
    execution_queue as List[String]  Note: Goal execution queue
    performance_metrics as Dictionary[String, Number] Note: Performance tracking
    resource_allocation as Dictionary[String, Dictionary[String, Number]] Note: Resource allocation
    conflict_resolution as Dictionary[String, String] Note: Conflict resolution strategies
    adaptive_strategies as Dictionary[String, Process] Note: Adaptive strategies
```

## Key Features

- **Hierarchical Goal Decomposition**: Break complex goals into manageable subgoals
- **Advanced Retry Strategies**: Exponential backoff and adaptive retry mechanisms
- **Real-Time Monitoring**: Live goal progress tracking and performance analytics
- **Adaptive Execution**: Dynamic strategy adjustment based on performance
- **Performance Optimization**: Continuous optimization and resource management
- **Conflict Resolution**: Automatic goal conflict detection and resolution
- **Advanced Reporting**: Comprehensive analytics and execution reports
- **Goal Persistence**: Reliable goal state persistence and recovery

## API Reference

### create_goal
Creates a basic goal with retry configuration.
```runa
Process called "create_goal" that takes description as String and max_retries as Integer returns AgentGoal
```

### create_goal_with_options
Creates a goal with comprehensive configuration options.
```runa
Process called "create_goal_with_options" that takes description as String and max_retries as Integer and priority as Integer and deadline as Number and dependencies as List[String] and resource_requirements as Dictionary[String, Number] returns AgentGoal
```

### execute_goal
Executes a goal with monitoring and adaptive strategies.
```runa
Process called "execute_goal" that takes goal as AgentGoal and execution_context as GoalExecutionContext returns GoalResult
```

### decompose_goal
Automatically decomposes complex goals into subgoals.
```runa
Process called "decompose_goal" that takes goal as AgentGoal and decomposition_strategy as String returns List[AgentGoal]
```

## Example Usage

```runa
Import "ai/agent/goals" as Goals

Let main_goal be Goals.create_goal_with_options with
    description as "Generate comprehensive quarterly business report"
    and max_retries as 3
    and priority as 1
    and deadline as (get_current_timestamp + 7200)  Note: 2 hour deadline
    and dependencies as list containing
    and resource_requirements as Dictionary with:
        "cpu_percent" as 60
        "memory_mb" as 512

Let subgoals be Goals.decompose_goal with
    goal as main_goal
    and decomposition_strategy as "capability_based"

For each subgoal in subgoals:
    Display "Subgoal: " + subgoal.description
    Display "  Priority: " + subgoal.priority
    Display "  Estimated duration: " + subgoal.resource_requirements["estimated_duration"]

Let execution_result be Goals.execute_goal with
    goal as main_goal
    and execution_context as create_goal_execution_context
```