# AI Reasoning Coordinator API Reference

The Reasoning Coordinator is the central orchestration engine for multi-model AI coordination. It manages the complete lifecycle from project analysis through execution and quality assurance.

## Overview

The reasoning coordinator implements sophisticated project decomposition, model assignment, and execution orchestration with built-in quality assurance and learning capabilities. It coordinates between a primary reasoning model and multiple specialized models to accomplish complex projects.

## Core Types

### ReasoningCoordinator

```runa
Type called "ReasoningCoordinator":
    coordinator_id as String
    reasoning_model as SpecializedModel
    specialized_models as Dictionary
    coordination_strategy as CoordinationType
    active_projects as Dictionary
    model_registry as Dictionary
    validation_engine as Dictionary
    learning_system as Dictionary
    coordinator_metadata as Dictionary
```

Primary coordination engine that manages all aspects of multi-model orchestration.

### ProjectState

```runa
Type called "ProjectState":
    project_id as String
    current_phase as ProjectPhase
    completed_phases as List[ProjectPhase]
    pending_phases as List[ProjectPhase]
    conversation_history as List[ConversationTurn]
    accumulated_context as Dictionary
    active_blockers as List[Dictionary]
    quality_assessments as Dictionary
    progress_metrics as Dictionary
    state_metadata as Dictionary
```

Comprehensive state tracking for coordinated projects with intelligent progress monitoring.

### ProjectPhase

```runa
Type called "ProjectPhase":
    phase_id as String
    phase_name as String
    phase_type as String
    required_models as List[String]
    input_requirements as Dictionary
    output_specifications as Dictionary
    validation_criteria as Dictionary
    dependencies as List[String]
    success_metrics as Dictionary
    phase_metadata as Dictionary
```

Structured representation of project phases with dependency tracking and validation criteria.

### SpecializedModel

```runa
Type called "SpecializedModel":
    model_id as String
    model_name as String
    model_type as String
    capabilities as List[String]
    input_formats as List[String]
    output_formats as List[String]
    quality_metrics as Dictionary
    performance_characteristics as Dictionary
    integration_endpoints as Dictionary
    model_metadata as Dictionary
```

Interface definition for specialized AI models with capability and performance specifications.

## Primary Functions

### create_reasoning_coordinator

Creates a new reasoning coordinator with comprehensive initialization.

```runa
Process called "create_reasoning_coordinator" that takes coordinator_config as Dictionary returns Dictionary
```

**Parameters:**
- `coordinator_config`: Configuration dictionary containing:
  - `reasoning_model_config`: Primary reasoning model configuration
  - `model_configs`: Dictionary of specialized model configurations
  - `project_type`: Type of projects this coordinator will handle
  - `complexity_level`: Expected complexity level ("low", "medium", "high")
  - `team_size`: Size of the coordination team

**Returns:** Dictionary containing:
- `reasoning_coordinator`: Initialized coordinator instance
- `phase_manager`: Phase management system
- `conversation_manager`: Conversation tracking system
- `quality_assurance`: Quality assurance engine
- `status`: Initialization status ("initialized" on success)
- `creation_timestamp`: Time of creation

**Example:**
```runa
Let coordinator_config be Dictionary with:
    "reasoning_model_config" as Dictionary with:
        "name" as "Odin-7B-Runa-Orchestrator"
        "capabilities" as list containing "analysis" and "planning" and "coordination"
    "model_configs" as Dictionary with:
        "code_model" as Dictionary with:
            "type" as "code_generation"
            "capabilities" as list containing "code_generation" and "refactoring"
            "specialization" as "Runa and Python Code Generation"
    "project_type" as "development"
    "complexity_level" as "medium"
    "team_size" as 3

Let result be create_reasoning_coordinator with coordinator_config as coordinator_config

If result["status"] is equal to "initialized":
    Display "Coordinator created successfully"
    Let coordinator be result["reasoning_coordinator"]
```

### initialize_coordinated_project

Initializes a new coordinated project with intelligent planning and decomposition.

```runa
Process called "initialize_coordinated_project" that takes project_request as String and reasoning_coordinator as ReasoningCoordinator and project_config as Dictionary returns Dictionary
```

**Parameters:**
- `project_request`: Natural language description of the project requirements
- `reasoning_coordinator`: Initialized reasoning coordinator instance
- `project_config`: Project-specific configuration including deadlines, priorities, and constraints

**Returns:** Dictionary containing:
- `initialization_status`: Status of initialization ("successful" on success)
- `project_state`: Complete project state with phases and assignments
- `project_analysis`: Detailed requirement analysis results
- `reasoning_plan`: Generated reasoning and execution plan
- `phase_decomposition`: Project breakdown into manageable phases
- `model_assignments`: Assignment of models to specific phases
- `project_validation`: Validation results for the initialized project
- `coordination_preparation`: Preparation for execution

**Example:**
```runa
Let project_request be "Create a REST API for user management with authentication, 
    role-based access control, and comprehensive documentation"

Let project_config be Dictionary with:
    "project_type" as "development"
    "priority" as "high"
    "deadline" as 86400.0  Note: 24 hours
    "quality_requirements" as Dictionary with:
        "accuracy_threshold" as 0.90
        "completeness_threshold" as 0.85

Let init_result be initialize_coordinated_project with
    project_request as project_request
    and reasoning_coordinator as coordinator
    and project_config as project_config

If init_result["initialization_status"] is equal to "successful":
    Let project_state be init_result["project_state"]
    Display "Project initialized: " with project_state["project_id"]
    Display "Total phases: " with length of init_result["phase_decomposition"]["phases"]
```

### execute_coordinated_project

Executes the complete coordination workflow with intelligent orchestration.

```runa
Process called "execute_coordinated_project" that takes project_state as ProjectState and reasoning_coordinator as ReasoningCoordinator returns Dictionary
```

**Parameters:**
- `project_state`: Initialized project state from `initialize_coordinated_project`
- `reasoning_coordinator`: Coordinator managing the execution

**Returns:** Dictionary containing:
- `coordination_status`: Overall coordination status ("completed" on success)
- `project_completed`: Boolean indicating if project was completed
- `total_iterations`: Number of coordination iterations executed
- `coordination_duration`: Total execution time in seconds
- `coordination_history`: Detailed history of all coordination iterations
- `final_project_state`: Final state of the project after coordination
- `completion_analysis`: Analysis of project completion and results

**Example:**
```runa
Let execution_result be execute_coordinated_project with
    project_state as project_state
    and reasoning_coordinator as coordinator

Display "Coordination completed in " with execution_result["total_iterations"] with " iterations"
Display "Total duration: " with execution_result["coordination_duration"] with " seconds"

If execution_result["project_completed"]:
    Display "🎉 Project completed successfully!"
    Let final_state be execution_result["final_project_state"]
    Display "Final quality score: " with final_state["quality_assessments"]["overall_quality"]
Otherwise:
    Display "Project coordination completed with partial results"
    Note: Check for blockers or quality issues
```

## Reasoning and Analysis Functions

### analyze_project_requirements

Performs comprehensive analysis of project requirements and complexity.

```runa
Process called "analyze_project_requirements" that takes project_request as String and reasoning_coordinator as Dictionary and project_config as Dictionary returns Dictionary
```

**Parameters:**
- `project_request`: Natural language project description
- `reasoning_coordinator`: Coordinator instance with reasoning capabilities
- `project_config`: Project configuration and constraints

**Returns:** Dictionary containing:
- `analysis_results`: Comprehensive requirement analysis including:
  - `project_scope`: Identified project scope and boundaries
  - `technical_requirements`: Technical specifications and dependencies
  - `business_requirements`: Business logic and user requirements
  - `constraints`: Project constraints and limitations
  - `stakeholders`: Identified stakeholders and their roles
  - `success_criteria`: Definition of project success
  - `risk_assessment`: Identified risks and mitigation strategies
  - `complexity_score`: Calculated complexity score (0.0-1.0)
- `validation_status`: Validation results for the analysis
- `confidence_score`: Confidence level in the analysis
- `recommendations`: Recommended approaches and considerations

**Example:**
```runa
Let analysis_result be analyze_project_requirements with
    project_request as "Build a microservices architecture with API gateway"
    and reasoning_coordinator as coordinator
    and project_config as config

Let analysis be analysis_result["analysis_results"]
Display "Project complexity: " with analysis["complexity_score"]
Display "Technical requirements: " with length of analysis["technical_requirements"]
Display "Identified risks: " with length of analysis["risk_assessment"]
```

### generate_reasoning_plan

Generates a comprehensive reasoning and execution plan based on project analysis.

```runa
Process called "generate_reasoning_plan" that takes project_analysis as Dictionary and reasoning_model as Dictionary returns Dictionary
```

**Parameters:**
- `project_analysis`: Results from `analyze_project_requirements`
- `reasoning_model`: Reasoning model configuration and capabilities

**Returns:** Dictionary containing:
- `reasoning_strategy`: Selected reasoning approach and methodology
- `reasoning_phases`: Structured breakdown of reasoning phases
- `plan_optimization`: Optimizations applied to the reasoning plan
- `resource_estimation`: Estimated resource requirements
- `estimated_duration`: Expected time for plan execution
- `quality_checkpoints`: Defined quality validation points

**Example:**
```runa
Let reasoning_plan be generate_reasoning_plan with
    project_analysis as analysis_result
    and reasoning_model as coordinator["reasoning_model"]

Display "Reasoning strategy: " with reasoning_plan["reasoning_strategy"]["strategy_type"]
Display "Estimated duration: " with reasoning_plan["estimated_duration"] with " seconds"
Display "Quality checkpoints: " with length of reasoning_plan["quality_checkpoints"]
```

### decompose_project_into_phases

Breaks down complex projects into manageable phases with dependency tracking.

```runa
Process called "decompose_project_into_phases" that takes reasoning_plan as Dictionary and project_analysis as Dictionary returns Dictionary
```

**Parameters:**
- `reasoning_plan`: Generated reasoning plan from `generate_reasoning_plan`
- `project_analysis`: Project requirements analysis

**Returns:** Dictionary containing:
- `phases`: List of project phases with complete specifications
- `dependencies`: Phase dependency graph
- `remaining_phases`: Phases remaining to be executed
- `total_phases`: Total number of phases

**Example:**
```runa
Let decomposition be decompose_project_into_phases with
    reasoning_plan as reasoning_plan
    and project_analysis as analysis_result

Display "Total phases: " with decomposition["total_phases"]
For each phase in decomposition["phases"]:
    Display "Phase: " with phase["phase_name"]
    Display "  Type: " with phase["phase_type"]
    Display "  Dependencies: " with length of phase["dependencies"]
```

## Model Coordination Functions

### assign_models_to_phases

Assigns optimal specialized models to project phases based on capability matching.

```runa
Process called "assign_models_to_phases" that takes phase_decomposition as Dictionary and specialized_models as Dictionary returns Dictionary
```

**Parameters:**
- `phase_decomposition`: Project phases from `decompose_project_into_phases`
- `specialized_models`: Available specialized models with capabilities

**Returns:** Dictionary mapping phase IDs to assigned model configurations

**Example:**
```runa
Let assignments be assign_models_to_phases with
    phase_decomposition as decomposition
    and specialized_models as coordinator["specialized_models"]

For each phase_id and model in assignments:
    Display "Phase " with phase_id with " assigned to " with model["model_name"]
    Display "  Model type: " with model["model_type"]
    Display "  Capabilities: " with length of model["capabilities"]
```

### coordinate_with_specialized_model

Establishes coordination with a specialized model for task execution.

```runa
Process called "coordinate_with_specialized_model" that takes specialized_model as SpecializedModel and project_state as ProjectState and reasoning_coordinator as ReasoningCoordinator returns Dictionary
```

**Parameters:**
- `specialized_model`: Model to coordinate with
- `project_state`: Current project state and context
- `reasoning_coordinator`: Coordinating reasoning system

**Returns:** Dictionary containing:
- `coordination_status`: Status of coordination setup ("prepared" on success)
- `model_coordination`: Coordination configuration and parameters
- `capability_analysis`: Analysis of model capabilities for the task
- `coordination_validation`: Validation of coordination setup

**Example:**
```runa
Let coordination_result be coordinate_with_specialized_model with
    specialized_model as assigned_model
    and project_state as current_state
    and reasoning_coordinator as coordinator

If coordination_result["coordination_status"] is equal to "prepared":
    Let coordination_data be coordination_result["model_coordination"]
    Display "Coordination established with " with assigned_model["model_name"]
    Display "Guidance parameters: " with coordination_data["guidance_parameters"]
```

### execute_specialized_task

Executes a specialized task using a coordinated model with progress tracking.

```runa
Process called "execute_specialized_task" that takes specialized_model as SpecializedModel and current_phase as ProjectPhase and accumulated_context as Dictionary and model_coordination as Dictionary returns Dictionary
```

**Parameters:**
- `specialized_model`: Model executing the task
- `current_phase`: Current project phase specifications
- `accumulated_context`: Context accumulated from previous phases
- `model_coordination`: Coordination configuration from `coordinate_with_specialized_model`

**Returns:** Dictionary containing:
- `execution_status`: Status of task execution ("completed" on success)
- `task_execution_id`: Unique identifier for this execution
- `execution_duration`: Time taken for task execution
- `intermediate_results`: Results from each iteration of execution
- `final_result`: Compiled final result of the task
- `execution_validation`: Validation of execution results
- `quality_assessment`: Quality metrics for the execution
- `model_performance_metrics`: Performance data for the model

**Example:**
```runa
Let task_result be execute_specialized_task with
    specialized_model as code_model
    and current_phase as current_phase
    and accumulated_context as project_context
    and model_coordination as coordination_data

If task_result["execution_status"] is equal to "completed":
    Display "Task completed in " with task_result["execution_duration"] with " seconds"
    Display "Quality score: " with task_result["quality_assessment"]["overall_quality"]
    Let final_output be task_result["final_result"]
```

## Quality Assurance Functions

### execute_reasoning_review

Performs comprehensive review and validation of task execution results.

```runa
Process called "execute_reasoning_review" that takes task_execution as Dictionary and current_phase as ProjectPhase and reasoning_model as SpecializedModel returns Dictionary
```

**Parameters:**
- `task_execution`: Results from `execute_specialized_task`
- `current_phase`: Current project phase specifications
- `reasoning_model`: Reasoning model performing the review

**Returns:** Dictionary containing:
- `review_status`: Status of the review process ("completed" on success)
- `reasoning_review`: Comprehensive review analysis including:
  - `result_analysis`: Analysis of task execution results
  - `quality_evaluation`: Quality assessment against success metrics
  - `completeness_assessment`: Evaluation of result completeness
  - `consistency_validation`: Consistency checks across results
  - `alignment_verification`: Verification of alignment with requirements
  - `improvement_opportunities`: Identified areas for improvement
  - `risk_evaluation`: Risk assessment of the results
- `review_confidence`: Confidence level in the review
- `next_steps`: Recommended next steps based on review

**Example:**
```runa
Let review_result be execute_reasoning_review with
    task_execution as task_result
    and current_phase as current_phase
    and reasoning_model as coordinator["reasoning_model"]

Let review be review_result["reasoning_review"]
Display "Quality evaluation: " with review["quality_evaluation"]["overall_score"]
Display "Completeness: " with review["completeness_assessment"]["completeness_percentage"]

If review["improvement_opportunities"]["has_improvements"]:
    Display "Improvement opportunities identified:"
    For each improvement in review["improvement_opportunities"]["opportunities"]:
        Display "  - " with improvement["description"]
```

### validate_project_initialization

Validates that project initialization was successful and complete.

```runa
Process called "validate_project_initialization" that takes project_state as Dictionary and reasoning_coordinator as Dictionary returns Dictionary
```

**Parameters:**
- `project_state`: Project state from `initialize_coordinated_project`
- `reasoning_coordinator`: Coordinator performing the validation

**Returns:** Dictionary containing:
- `initialization_valid`: Boolean indicating if initialization is valid
- `validation_errors`: List of validation errors if any
- `validation_warnings`: List of validation warnings
- `validation_score`: Overall validation score (0.0-1.0)

**Example:**
```runa
Let validation_result be validate_project_initialization with
    project_state as project_state
    and reasoning_coordinator as coordinator

If validation_result["initialization_valid"]:
    Display "✅ Project initialization validated successfully"
    Display "Validation score: " with validation_result["validation_score"]
Otherwise:
    Display "❌ Project initialization validation failed"
    For each error in validation_result["validation_errors"]:
        Display "Error: " with error
```

## Execution Management Functions

### execute_reasoning_evaluation

Evaluates current project phase and determines next steps.

```runa
Process called "execute_reasoning_evaluation" that takes current_phase as ProjectPhase and project_state as ProjectState and reasoning_model as SpecializedModel returns Dictionary
```

**Parameters:**
- `current_phase`: Current project phase to evaluate
- `project_state`: Complete project state and context
- `reasoning_model`: Reasoning model performing the evaluation

**Returns:** Dictionary containing:
- `evaluation_status`: Status of evaluation ("completed" on success)
- `reasoning_evaluation`: Comprehensive evaluation including:
  - `context_analysis`: Analysis of current context and state
  - `progress_assessment`: Assessment of project progress
  - `requirement_validation`: Validation against requirements
  - `readiness_evaluation`: Evaluation of readiness for execution
  - `phase_strategy`: Strategy for executing the current phase
  - `risk_assessment`: Risk analysis for the phase
  - `success_criteria`: Defined success criteria
  - `quality_expectations`: Expected quality outcomes
- `evaluation_confidence`: Confidence in the evaluation
- `evaluation_validation`: Validation of the evaluation itself

### generate_clarifying_questions

Generates clarifying questions when project requirements are unclear.

```runa
Process called "generate_clarifying_questions" that takes phase_evaluation as Dictionary and project_state as Dictionary and reasoning_coordinator as Dictionary returns Dictionary
```

**Parameters:**
- `phase_evaluation`: Results from `execute_reasoning_evaluation`
- `project_state`: Current project state
- `reasoning_coordinator`: Coordinator generating questions

**Returns:** Dictionary containing:
- `questions`: List of clarifying questions
- `question_count`: Number of questions generated
- `priority_level`: Priority level of clarification needs

### analyze_phase_dependencies

Analyzes dependencies between project phases.

```runa
Process called "analyze_phase_dependencies" that takes phase_decomposition as Dictionary and model_assignment as Dictionary returns Dictionary
```

**Parameters:**
- `phase_decomposition`: Project phases from decomposition
- `model_assignment`: Model assignments to phases

**Returns:** Dictionary containing:
- `dependency_graph`: Complete dependency graph
- `dependency_analysis`: Analysis of dependency relationships
- `total_dependencies`: Total number of dependencies

## Utility Functions

### generate_coordinated_project_id

Generates unique identifiers for coordinated projects.

```runa
Process called "generate_coordinated_project_id" that takes nothing returns String
```

**Returns:** Unique project identifier with "coord_project_" prefix

### generate_coordination_session_id

Generates unique identifiers for coordination sessions.

```runa
Process called "generate_coordination_session_id" that takes nothing returns String
```

**Returns:** Unique session identifier with "coord_session_" prefix

### determine_coordination_strategy

Determines optimal coordination strategy based on project characteristics.

```runa
Process called "determine_coordination_strategy" that takes coordinator_config as Dictionary returns String
```

**Parameters:**
- `coordinator_config`: Configuration including project type, complexity, and team size

**Returns:** Selected coordination strategy name

**Strategy Selection Rules:**
- `complexity_level` = "high" AND `team_size` > 5 → "hierarchical_coordination"
- `project_type` = "research" → "iterative_coordination"  
- `project_type` = "development" → "pipeline_coordination"
- `complexity_level` = "low" → "sequential_coordination"
- Default → "adaptive_coordination"

### calculate_model_compatibility

Calculates compatibility score between model capabilities and requirements.

```runa
Process called "calculate_model_compatibility" that takes model as Dictionary and required_capabilities as List[String] returns Number
```

**Parameters:**
- `model`: Model with capabilities list
- `required_capabilities`: Required capabilities for a task

**Returns:** Compatibility score (0.0-1.0) representing percentage of requirements met

### current_timestamp

Gets current timestamp for coordination tracking.

```runa
Process called "current_timestamp" that takes nothing returns Number
```

**Returns:** Current timestamp in seconds since epoch

## Advanced Functions

### monitor_situation_evolution

Monitors how project situations evolve during coordination.

```runa
Process called "monitor_situation_evolution" that takes situation_system as Dictionary and current_situation as Dictionary and monitoring_config as Dictionary returns Dictionary
```

### optimize_constraint_satisfaction

Optimizes solutions within project and resource constraints.

```runa
Process called "optimize_constraint_satisfaction" that takes constraint_system as Dictionary and optimization_problem as Dictionary and optimization_config as Dictionary returns Dictionary
```

### adapt_coordination_context

Adapts coordination approach based on changing project context.

```runa
Process called "adapt_coordination_context" that takes adaptation_system as Dictionary and context_changes as Dictionary and adaptation_config as Dictionary returns Dictionary
```

## Error Handling

### Common Error Patterns

#### Initialization Failures
```runa
If coordinator_result["status"] is not equal to "initialized":
    Display "Coordinator initialization failed"
    Let errors be coordinator_result["initialization_errors"]
    For each error in errors:
        Display "Error: " with error["type"] with " - " with error["message"]
```

#### Model Assignment Failures
```runa
If assignment_result is empty or length of assignment_result is equal to 0:
    Display "No suitable models found for project phases"
    Note: Check model capabilities and phase requirements
    suggest_model_additions_or_scope_adjustment[]
```

#### Quality Assurance Failures
```runa
If review_result["reasoning_review"]["quality_evaluation"]["meets_standards"] is equal to false:
    Display "Quality standards not met"
    Let improvements be review_result["reasoning_review"]["improvement_opportunities"]
    apply_improvement_recommendations with improvements as improvements
```

#### Coordination Execution Failures
```runa
If execution_result["coordination_status"] is not equal to "completed":
    Display "Coordination execution incomplete"
    Let final_state be execution_result["final_project_state"]
    
    If length of final_state["active_blockers"] is greater than 0:
        Display "Active blockers preventing completion:"
        For each blocker in final_state["active_blockers"]:
            Display "  - " with blocker["blocker_type"] with ": " with blocker["description"]
            attempt_blocker_resolution with blocker as blocker
```

## Performance Considerations

### Optimization Strategies

1. **Model Selection Optimization**: Choose models with optimal capability-to-performance ratios
2. **Phase Parallelization**: Execute independent phases in parallel when possible
3. **Context Management**: Efficiently manage accumulated context to prevent memory bloat
4. **Quality Checkpoint Frequency**: Balance quality assurance with execution speed
5. **Learning System Integration**: Leverage coordination learning for improved efficiency

### Memory Management

- **Context Compression**: Automatically compress older context data
- **Model State Caching**: Cache model states to reduce initialization overhead
- **Garbage Collection**: Regular cleanup of completed phase data
- **Resource Monitoring**: Continuous monitoring of memory and CPU usage

### Scalability Features

- **Horizontal Scaling**: Support for distributed model execution
- **Load Balancing**: Automatic load distribution across available models
- **Adaptive Resource Allocation**: Dynamic resource allocation based on demand
- **Performance Profiling**: Built-in profiling for coordination optimization

## Integration Examples

See the main [Coordination README](README.md) for comprehensive integration examples and usage patterns.

## Configuration Reference

See [`config.md`](config.md) for detailed configuration options and customization guides.