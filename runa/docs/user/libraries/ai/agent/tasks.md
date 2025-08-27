# Agent Tasks Module

The Agent Tasks module provides comprehensive task and goal assignment, tracking, reporting, and error handling for agents in production-grade multi-agent systems.

## Overview

This module enables robust task orchestration with advanced workflow management, dependency resolution, resource optimization, fault tolerance, and real-time monitoring capabilities.

## Core Types

### AgentTask
```runa
Type called "AgentTask":
    id as String                     Note: Unique task identifier
    description as String            Note: Task description
    assigned_to as String           Note: Assigned agent ID
    status as String                Note: Current status
    progress as Number              Note: Completion progress (0-1)
    result as Any                   Note: Task result
    error as String                 Note: Error message if failed
    created_at as Number            Note: Creation timestamp
    updated_at as Number            Note: Last update timestamp
    priority as Number              Note: Task priority (1-10)
    complexity as Number            Note: Task complexity (0-1)
    estimated_duration as Number    Note: Estimated duration in seconds
    actual_duration as Number       Note: Actual execution time
    deadline as Number              Note: Task deadline
    dependencies as List[String]    Note: Dependent task IDs
    subtasks as List[String]        Note: Subtask IDs
    parent_task as String           Note: Parent task ID
    resource_requirements as Dictionary[String, Number] Note: Resource needs
    performance_metrics as Dictionary[String, Number] Note: Performance data
    retry_count as Number           Note: Current retry attempts
    max_retries as Number           Note: Maximum retry attempts
    retry_delay as Number           Note: Delay between retries
    tags as List[String]            Note: Task tags for organization
    metadata as Dictionary[String, Any] Note: Additional metadata
```

### TaskManager
```runa
Type called "TaskManager":
    tasks as Dictionary[String, AgentTask] Note: All managed tasks
    agent_tasks as Dictionary[String, List[String]] Note: Agent-to-task mapping
    task_queue as List[String]      Note: Pending task queue
    completed_tasks as Dictionary[String, AgentTask] Note: Completed tasks
    failed_tasks as Dictionary[String, AgentTask] Note: Failed tasks
    task_dependencies as Dictionary[String, List[String]] Note: Dependency graph
    resource_allocation as Dictionary[String, Dictionary[String, Number]] Note: Resource allocation
    performance_metrics as Dictionary[String, Dictionary[String, Number]] Note: Performance tracking
```

## Key Features

- **Advanced Task Orchestration**: Sophisticated workflow management and scheduling
- **Dependency Resolution**: Automatic dependency tracking and resolution
- **Resource Optimization**: Intelligent resource allocation and load balancing
- **Fault Tolerance**: Automatic recovery and retry strategies
- **Performance Monitoring**: Real-time performance analytics and optimization
- **Task Prioritization**: Priority-based scheduling with deadline management
- **Distributed Execution**: Multi-agent task coordination and synchronization
- **Advanced Error Handling**: Comprehensive error recovery and retry mechanisms

## API Reference

### create_task_manager
Creates a comprehensive task management system.
```runa
Process called "create_task_manager" returns TaskManager
```

### create_task
Creates a new task with specified parameters.
```runa
Process called "create_task" that takes description as String and complexity as Number returns AgentTask
```

### assign_task
Assigns a task to a specific agent with validation.
```runa
Process called "assign_task" that takes manager as TaskManager and task as AgentTask and agent_id as String returns TaskAssignmentResult
```

### execute_task
Executes a task with monitoring and error handling.
```runa
Process called "execute_task" that takes task as AgentTask and execution_context as ExecutionContext returns TaskResult
```

## Example Usage

```runa
Import "ai/agent/tasks" as Tasks

Let task_manager be Tasks.create_task_manager

Let analysis_task be Tasks.create_task with
    description as "Analyze quarterly sales data and generate insights"
    and complexity as 0.7

Set analysis_task.priority to 8
Set analysis_task.deadline to get_current_timestamp + 3600  Note: 1 hour deadline
Set analysis_task.resource_requirements["memory_mb"] to 512
Set analysis_task.resource_requirements["cpu_percent"] to 40

Let assignment_result be Tasks.assign_task with
    manager as task_manager
    and task as analysis_task  
    and agent_id as "data_analyst_1"

Let execution_result be Tasks.execute_task with
    task as analysis_task
    and execution_context as create_execution_context
```