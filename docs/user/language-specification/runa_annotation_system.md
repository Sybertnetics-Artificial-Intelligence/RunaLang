# Runa Code Annotation System
*Structured Annotations for Direct AI Intent and Interaction*

**Last Updated**: 2025-09-08  
**Note**: This documentation reflects the current implementation with mathematical symbol enforcement.

## Overview

Runa’s annotation system encodes developer and architect intent for AI systems. Annotations are not comments; they are machine-parseable directives and context for AI agents and AI-powered tools. All AI engineers should use them, and developers building AI tools should prefer them to ad-hoc comments when intent must be consumed by machines.

**Mathematical Symbol Note**: All annotation examples use natural language operators (`plus`, `minus`, `is less than`) which are always valid. Mathematical symbols are restricted to mathematical contexts only.

### Implementation Conformance (Bootstrap Compiler)

The bootstrap parser currently recognizes and parses the following top-level annotation blocks:

- @Reasoning ... @End_Reasoning
- @Implementation ... @End_Implementation
- @Uncertainty ... @End_Uncertainty
- @Request_Clarification ... @End_Request_Clarification
- @KnowledgeReference ... @End_KnowledgeReference
- @TestCases ... @End_TestCases
- @Resource_Constraints ... @End_Resource_Constraints
- @Security_Scope ... @End_Security_Scope
- @Execution_Model ... @End_Execution_Model
- @Performance_Hints ... @End_Performance_Hints
- @Progress ... @End_Progress
- @Feedback ... @End_Feedback
- @Translation_Note ... @End_Translation_Note
- @Error_Handling ... @End_Error_Handling

Specified but not yet routed by the bootstrap parser as top-level blocks (reserved and recognized by the lexer, but not consumed as annotation blocks yet):

- @Task, @End_Task
- @Requirements, @End_Requirements
- @Verify, @End_Verify
- @Request, @End_Request
- @Context, @End_Context
- @Collaboration, @End_Collaboration
- @Iteration, @End_Iteration
- @Clarification, @End_Clarification

These remain part of the language specification and are supported in the annotation type system; parser routing will be enabled in a subsequent bootstrap update. Until then, keep these blocks in code for forward-compatibility, or place their content inside parsed blocks (e.g., within @Implementation) if immediate parsing is required.

## Core Concepts

### Annotation Categories and Intent

Runa provides several types of annotations that can be used individually or in combination:

- **Reasoning Annotations**: Convey the why behind decisions to guide AI synthesis and refactoring.
- **Context Annotations**: Describe environment, constraints, and assumptions for AI planning.
- **Verification Annotations**: Declare properties the AI must maintain/verify.
- **Resource/Security Annotations**: Bound what AI may do and under what budgets/capabilities.
- **Task/Requirements Annotations**: Specify formal objectives for AI agents to implement/check.

### Design Principles

1. **Semantic Preservation**: Annotations maintain meaning across different contexts and tools
2. **Tool Agnostic**: Annotations work with various development tools and AI systems
3. **Human Readable**: All annotations use natural language for clarity
4. **Machine Parseable**: Structured format enables automated processing
5. **Optional**: Annotations enhance code but are never required (strongly recommended for AI workflows)
### Usage Guidance (When and Why)

- Use annotations whenever AI agents must consume intent (architecture, constraints, goals, verification) rather than relying on prose.
- Prefer annotations to free-text comments for machine-facing guidance; use comments for human narration.
- Co-locate annotations with the code they govern; keep scopes minimal and precise.
- Treat annotations as normative inputs for AI tooling; conflicting comments yield to annotations.

### Lifecycle and Evaluation Phase

- Parsing: Annotations are parsed at compile-time and made available to tooling.
- Evaluation: Some annotations have compile-time effects (e.g., verification), others inform runtime systems (e.g., execution model) without overhead.
- Precedence: File-local overrides module-level; inner blocks override outer; explicit keys override defaults.

6. **Language Agnostic**: Annotation format works across all target programming languages

## Annotation Categories

### 1. Reasoning and Intent Annotations

#### @Reasoning Block
Documents the logical reasoning process and decision rationale behind code implementations.

What this is used for:
- Capture design rationale, trade-offs, and decision history for AI agents to respect during refactors and generation.
- Provide auditable context for reviewers and future maintainers.

How to use this:
- Place immediately above the implementation it governs.
- Write concise bullet points; prefer measurable criteria and constraints.
- Reference external sources with @KnowledgeReference when applicable.

Example (ideal structure):
```runa
@Reasoning:
    Goal: Reduce p95 latency below 50ms without increasing error rate
    Options considered: cache, batch, rewrite
    Decision: cache because hit-rate > 0.9, memory budget 256MB
    Risks: staleness; Mitigation: ttl=60s, background refresh
@End_Reasoning
```

or

```runa
@Reasoning:
    The quicksort algorithm is preferred over merge sort in this case because:
    1. We have a small dataset that fits in memory (< 10,000 items)
    2. The partial ordering of the data suggests good pivot selection
    3. The implementation is simpler and requires less additional memory
    4. Average case performance is O(n log n) which meets our requirements
@End_Reasoning
```

**Purpose**: Improves code maintainability by documenting the reasoning behind implementation decisions.

#### @Implementation Block
Provides detailed implementation notes and guidance.

What this is used for:
- Specify authoritative implementation structure, invariants, and algorithmic steps the AI should follow.
- Disambiguate between multiple viable implementations.

How to use this:
- Co-locate with the target process/type.
- Use imperative, stepwise instructions; include inputs/outputs and edge-case handling.

Example (ideal structure):
```runa
@Implementation:
    Process: "resize_image"
    Steps:
        1. Validate format ∈ {png,jpg}; Otherwise throw ValueError
        2. Compute scale preserving aspect ratio
        3. Apply bilinear filter; clamp to bounds
        4. Return new buffer with metadata updated
@End_Implementation
```

**Purpose**: Bridges the gap between high-level algorithmic thinking and concrete implementation details.

### 2. Uncertainty and Confidence Annotations

#### @Uncertainty Expression
Represents multiple possible choices with confidence levels.

What this is used for:
- Declare alternatives where multiple approaches are acceptable, with a confidence hint for selection.

How to use this:
- Limit to top 2–4 realistic options.
- Always include a numeric confidence and criteria for promotion/demotion.

Example (ideal structure):
```runa
Let hash_strategy be ?[SipHash, Murmur3] with confidence 0.7
```

**Purpose**: Allows developers to express uncertainty and make informed decisions about implementation choices.

### 3. Knowledge and Context Annotations

#### @KnowledgeReference Block
Links implementation to external knowledge sources.

What this is used for:
- Bind code decisions to vetted sources (papers, specs, standards) for traceability.

How to use this:
- Include stable identifiers (DOI, arXiv, version pins).
- Add a one-line "why relevant" note.

Example (ideal structure):
```runa
@KnowledgeReference:
    concept: "A* Search"
    reference_id: "doi:10.1145/321105.321114"
    version: "canonical"
    relevance: "Optimal pathfinding with admissible heuristics"
@End_KnowledgeReference
```

or

```runa
@KnowledgeReference:
    concept: "Transformer Architecture"
    reference_id: "arxiv:1706.03762"
    version: "as of 2023-10"
    relevant_sections: ["3.1 Scaled Dot-Product Attention", "3.2 Multi-Head Attention"]
    implementation_notes: "Using standard transformer but with modified positional encoding"
@End_KnowledgeReference
```

#### @Context Block
Provides situational context for implementation decisions.

What this is used for:
- Inform agents about deployment constraints, platforms, and business context impacting choices.

How to use this:
- Keep keys stable across a repository; prefer enums over free text.
- Scope narrowly (module or file) to avoid stale global context.

Example (ideal structure):
```runa
@Context:
    deployment_environment: "edge_device"
    latency_budget_ms: 50
    memory_limit_mb: 256
    reliability_target: "99.9%"
@End_Context
```

or

```runa
@Context:
    deployment_environment: "edge_device"
    performance_constraints: "sub_100ms_latency"
    memory_constraints: "max_512MB"
    user_base: "mobile_users"
    criticality: "high"
@End_Context
```

### 4. Task and Specification Annotations

#### @Task Block
Formal task specification for AI-assisted development.

What this is used for:
- Define objective, constraints, and acceptance for an autonomous or assisted task.

How to use this:
- Be testable: specify inputs/outputs and DONE criteria.
- Include priority and deadline only if actionable.

Example (ideal structure):
```runa
@Task:
    objective: "Implement LRU cache"
    inputs: ["capacity:Int", "loader:Function"]
    outputs: ["get/put interface", "eviction policy"]
    acceptance: ["O(1) ops", ">=95% hit-rate on Zipf(1.2)"]
@End_Task
```

or

```runa
@Task:
    objective: "Implement real-time face detection system"
    constraints: [
        "Must run on mobile devices",
        "Battery efficient",
        "Accuracy > 95%",
        "Latency < 50ms per frame"
    ]
    input_format: "Video stream (720p, 30fps)"
    output_format: "Bounding boxes with confidence scores"
    target_language: "Python"
    frameworks: ["OpenCV", "TensorFlow Lite"]
    priority: "Performance over accuracy"
    deadline: "2 weeks"
@End_Task
```

#### @Requirements Block
Detailed functional and non-functional requirements.

What this is used for:
- Contract for features and qualities; drives verification and tests.

How to use this:
- Separate functional vs non-functional; make each requirement verifiable.
- Cross-link to @Verify and @TestCases.

Example (ideal structure):
```runa
@Requirements:
    functional: ["persist user session", "rotate keys"]
    non_functional: ["p95<50ms", "error_rate<0.1%"]
    constraints: ["FIPS140-2", "EU-only data"]
@End_Requirements
```

or

```runa
@Requirements:
    functional: [
        "Detect faces in real-time video",
        "Handle multiple faces per frame",
        "Robust to lighting variations",
        "Work with different face orientations"
    ]
    non_functional: [
        "Response time < 50ms",
        "Memory usage < 100MB",
        "CPU usage < 30%",
        "Battery life impact < 5%"
    ]
    constraints: [
        "No internet connectivity required",
        "Must work offline",
        "Compatible with Android/iOS"
    ]
@End_Requirements
```

### 5. Verification and Quality Annotations

#### @Verify Block
Embedded verification conditions.

What this is used for:
- Assert invariants and postconditions that tooling must check.

How to use this:
- Write assertions using canonical operators; avoid side effects.
- Keep fast-running; move heavy checks to @TestCases.

Example (ideal structure):
```runa
@Verify:
    Assert cache_size is less than or equal to capacity
    Assert ttl is greater than 0
@End_Verify
```

or

```runa
@Verify:
    Assert result is not None
    Assert length of result is greater than 0
    Assert all items in result satisfy validation_criteria
    Assert response_time is less than 100 # milliseconds
    Assert memory_usage is less than 50_000_000 # bytes
@End_Verify

Process called "ProcessUserData" that takes user_input:
    # Implementation with automatic verification
    Let processed_data be transform_input with data as user_input
    Return processed_data
```

#### @TestCases Block
Comprehensive test specifications.

What this is used for:
- Define unit/integration/performance tests that CI can materialize.

How to use this:
- Provide names, inputs, expected outputs, and time/memory budgets where relevant.

Example (ideal structure):
```runa
@TestCases:
    unit_tests: [
        { "name": "hit", "input": ["k"], "prepare": "put(""k"",1)", "expected_output": 1 },
        { "name": "miss", "input": ["z"], "expected_output": null }
    ]
@End_TestCases
```

or

```runa
@TestCases:
    unit_tests: [
        {
            "name": "test_empty_input",
            "input": [],
            "expected_output": [],
            "expected_time": "< 1ms"
        },
        {
            "name": "test_large_dataset",
            "input": "generate_large_dataset(10000)",
            "expected_output": "sorted_dataset",
            "expected_time": "< 100ms"
        }
    ]
    integration_tests: [
        {
            "name": "test_end_to_end_workflow",
            "setup": "initialize_test_environment()",
            "steps": ["load_data", "process_data", "save_results"],
            "assertions": ["data_integrity", "performance_metrics"]
        }
    ]
    performance_tests: [
        {
            "metric": "throughput",
            "target": "> 1000 requests/second",
            "load_pattern": "gradual_increase"
        }
    ]
@End_TestCases
```

### 6. Resource and Security Annotations

#### @Resource_Constraints Block
Specifies computational and memory limitations.

What this is used for:
- Bound resource usage of an operation to protect SLAs and budgets.

How to use this:
- Prefer explicit units; set max iterations/timeouts; pair with @Execution_Model when needed.

Example (ideal structure):
```runa
@Resource_Constraints:
    memory_limit: "256MB"
    cpu_limit: "2 cores"
    execution_timeout: "30 seconds"
@End_Resource_Constraints
```
or

```runa
@Resource_Constraints:
    memory_limit: "256MB"
    cpu_limit: "2 cores"
    execution_timeout: "30 seconds"
    disk_space: "10MB"
    network_bandwidth: "1Mbps"
    optimize_for: "memory"  # or "speed", "battery", "accuracy"
    max_iterations: 10000
    cache_size: "64MB"
@End_Resource_Constraints
```

#### @Security_Scope Block
Defines security capabilities and restrictions.

What this is used for:
- Declare least-privilege capabilities and forbidden actions for code paths.

How to use this:
- List positive capabilities first, then forbidden; specify sandbox level and auditing.

Example (ideal structure):
```runa
@Security_Scope:
    capabilities: ["file.read", "crypto.hash"]
    forbidden: ["net.access"]
    sandbox_level: "strict"
    audit_logging: "detailed"
@End_Security_Scope
```

or

```runa
@Security_Scope:
    capabilities: [
        "file.read",
        "math.compute",
        "memory.local",
        "crypto.hash"
    ]
    forbidden: [
        "net.access",
        "file.write",
        "system.execute",
        "registry.modify"
    ]
    sandbox_level: "strict"
    data_access: "read_only"
    encryption_required: true
    audit_logging: "detailed"
    privilege_level: "user"
@End_Security_Scope
```

### 7. Execution and Performance Annotations

#### @Execution_Model Block
Specifies how code should be executed.

What this is used for:
- Communicate execution mode preferences to runtime/tooling (parallelism, scheduling) under AOTT.

How to use this:
- Choose one mode; specify concurrency and retry policy succinctly; avoid duplicating @Resource_Constraints.

Example (ideal structure):
```runa
@Execution_Model:
    mode: "batch"
    concurrency: "parallel"
    parallelism_level: 4
@End_Execution_Model
```

or

```runa
@Execution_Model:
    mode: "batch"  # or "streaming", "real_time", "interactive"
    concurrency: "parallel"  # or "sequential", "async"
    parallelism_level: 4
    scheduling: "round_robin"
    priority: "normal"  # or "high", "low", "critical"
    retry_policy: "exponential_backoff"
    error_recovery: "graceful_degradation"
    monitoring: "detailed"
@End_Execution_Model
```

#### @Performance_Hints Block
Optimization guidance for implementation.

What this is used for:
- Inform compilers/agents about safe optimizations and thresholds.

How to use this:
- Keep hints orthogonal to correctness; avoid mandatory semantics here (use @Implementation/@Requirements).

Example (ideal structure):
```runa
@Performance_Hints:
    cache_strategy: "aggressive"
    vectorization: "enabled"
    parallel_threshold: 1000
@End_Performance_Hints
```

or

```runa
@Performance_Hints:
    cache_strategy: "aggressive"  # or "conservative", "adaptive"
    vectorization: "enabled"
    memory_layout: "contiguous"
    parallel_threshold: 1000
    batch_size: 32
    prefetch_enabled: true
    compression: "enabled"
    hot_path_optimization: ["search", "sort", "filter"]
@End_Performance_Hints
```

### 8. Communication Flow Annotations

#### @Progress Block
Real-time progress reporting for development tracking.

What this is used for:
- Report status for agents and reviewers; enable dashboards and alerts.

How to use this:
- Update incrementally; keep blockers and confidence current; avoid marketing language.

Example (ideal structure):
```runa
@Progress:
    completion_percentage: 40
    current_milestone: "API complete"
    next_milestone: "Benchmarking"
    blockers: ["missing fixtures"]
@End_Progress
```

or

```runa
@Progress:
    completion_percentage: 75
    current_milestone: "Algorithm implementation completed"
    next_milestone: "Unit testing and optimization"
    estimated_time_remaining: "2 hours"
    blockers: []
    intermediate_results: {
        "tests_passing": 45,
        "code_coverage": "87%",
        "performance_baseline": "85ms average response time"
    }
    confidence_level: 0.9
@End_Progress
```

### 9. Translation and Target-Specific Annotations

#### @Translation_Note Block
Language-specific implementation guidance.

What this is used for:
- Capture target-language adaptations without changing core semantics.

How to use this:
- List supported targets and per-target notes; avoid prescribing global policy.

Example (ideal structure):
```runa
@Translation_Note:
    target_languages: ["Python", "Rust"]
    platform_specific: { "Python": "use asyncio" }
    performance_considerations: { "Rust": "prefer iterators over indexing" }
@End_Translation_Note
```

or

```runa
@Translation_Note:
    target_languages: ["Python", "JavaScript", "Java", "C++"]
    critical_feature: "Asynchronous processing"
    platform_specific: {
        "Python": "Use asyncio with proper event loop management",
        "JavaScript": "Use Promises with async/await syntax",
        "Java": "Use CompletableFuture with proper thread pool",
        "C++": "Use std::async with future objects"
    }
    performance_considerations: {
        "Python": "Consider using multiprocessing for CPU-bound tasks",
        "JavaScript": "Use Web Workers for heavy computations",
        "Java": "Optimize garbage collection settings",
        "C++": "Use move semantics for large objects"
    }
    compatibility_notes: {
        "Python": "Requires Python 3.8+ for proper asyncio support",
        "JavaScript": "Requires ES2017+ for async/await",
        "Java": "Requires Java 8+ for CompletableFuture",
        "C++": "Requires C++11+ for std::async"
    }
@End_Translation_Note
```

### 10. Error Handling and Recovery Annotations

#### @Error_Handling Block
Comprehensive error management strategy.

What this is used for:
- Define error models, recovery paths, and user impact explicitly.

How to use this:
- Enumerate expected errors with probabilities; state fallback behavior and notification policy.

Example (ideal structure):
```runa
@Error_Handling:
    expected_errors: [ { "type": "NetworkTimeout", "recovery": "retry" } ]
    fallback_behavior: "return_cached_result"
    user_notification: "user_friendly_messages"
@End_Error_Handling
```

or

```runa
@Error_Handling:
    strategy: "graceful_degradation"
    expected_errors: [
        {
            "type": "NetworkTimeout",
            "probability": 0.05,
            "recovery": "retry_with_exponential_backoff",
            "max_retries": 3
        },
        {
            "type": "InvalidInput",
            "probability": 0.1,
            "recovery": "sanitize_and_retry",
            "fallback": "use_default_values"
        }
    ]
    fallback_behavior: "return_cached_result"
    error_reporting: "detailed_logging"
    monitoring_alerts: "critical_errors_only"
    user_notification: "user_friendly_messages"
@End_Error_Handling
```

## Advanced Communication Patterns

### Multi-Agent Collaboration

### Iterative Refinement

#### @Iteration Block
Support for iterative development cycles.

What this is used for:
- Coordinate multi-step improvement loops with explicit success criteria.

How to use this:
- Link to previous feedback; keep cycle_number monotonic; update next plan based on measured outcomes.

Example (ideal structure):
```runa
@Iteration:
    cycle_number: 4
    previous_feedback: ["memory spike under load"]
    current_focus: "profile allocations"
    success_criteria: ["peak RSS < 200MB"]
    next_iteration_plan: "switch to arena allocator"
@End_Iteration
```

or

```runa
@Iteration:
    cycle_number: 3
    previous_feedback: [
        "Algorithm too slow for real-time requirements",
        "Memory usage exceeds constraints",
        "Edge cases not properly handled"
    ]
    current_focus: "Performance optimization while maintaining accuracy"
    success_criteria: [
        "Response time < 50ms",
        "Memory usage < 100MB",
        "Accuracy > 95%"
    ]
    next_iteration_plan: "Add comprehensive error handling and edge case coverage"
@End_Iteration
```

## Protocol Implementation Guidelines

### For Brain AI Systems

1. **Clear Intent Expression**: Use reasoning blocks to explain decision rationale
2. **Comprehensive Task Specification**: Provide complete requirements and constraints
3. **Uncertainty Acknowledgment**: Explicitly state confidence levels and alternatives
4. **Context Provision**: Include all relevant environmental and business context
5. **Verification Criteria**: Define clear success and failure conditions

### For Hat AI Systems

1. **Implementation Fidelity**: Preserve all semantic meaning from Brain annotations
2. **Progress Reporting**: Regular updates on implementation status and challenges
3. **Clarification Requests**: Proactive requests for missing information
4. **Alternative Suggestions**: Propose alternatives when constraints cannot be met
5. **Quality Assurance**: Include verification blocks in implementation

### For Translation Systems

1. **Annotation Preservation**: Maintain all annotations in target language comments
2. **Semantic Mapping**: Ensure target language idioms preserve original intent
3. **Performance Characteristics**: Adapt performance hints to target platform
4. **Error Handling**: Translate error handling patterns to target language conventions

## Example: Complete Communication Flow

```runa
# Brain -> Hat Communication
@Task:
    objective: "Implement user authentication system"
    constraints: ["Secure", "Fast", "User-friendly"]
    target_language: "Python"
    deadline: "3 days"
@End_Task

@Reasoning:
    Using JWT tokens for stateless authentication because:
    1. Scalable across multiple servers
    2. No server-side session storage required
    3. Industry standard with good library support
    4. Includes expiration and claims
@End_Reasoning

@Security_Scope:
    capabilities: ["crypto.hash", "crypto.jwt", "database.read", "database.write"]
    forbidden: ["file.system", "network.external"]
    encryption_required: true
    audit_logging: "enabled"
@End_Security_Scope

@Requirements:
    functional: [
        "User login with email/password",
        "Token generation and validation",
        "Password hashing with salt",
        "Token refresh mechanism"
    ]
    non_functional: [
        "Authentication time < 200ms",
        "Tokens expire in 1 hour",
        "Refresh tokens expire in 30 days",
        "Secure password storage"
    ]
@End_Requirements

# Implementation Example
@Implementation:
    Process called "authenticate_user" that takes email and password:
        @Verify:
            Assert email is not None
            Assert password is not None
            Assert email contains "@"
        @End_Verify
        
        Let user be find_user_by_email with email as email
        If user is None:
            Return AuthResult.failure with message "Invalid credentials"
        
        Let password_valid be verify_password with 
            password as password and 
            hash as user.password_hash
        
        If not password_valid:
            Return AuthResult.failure with message "Invalid credentials"
        
        Let token be generate_jwt_token with user_id as user.id
        Return AuthResult.success with token as token
@End_Implementation

@Progress:
    completion_percentage: 90
    current_milestone: "Core authentication implemented"
    next_milestone: "Token refresh mechanism"
    intermediate_results: {
        "unit_tests_passing": 12,
        "integration_tests_passing": 3,
        "performance_benchmark": "Average 150ms authentication time"
    }
@End_Progress


```

## Best Practices

### Annotation Density
- **High-Level Functions**: Rich annotations with reasoning and context
- **Utility Functions**: Minimal annotations focusing on verification
- **Critical Paths**: Comprehensive annotations including performance and security
- **Experimental Code**: Heavy use of uncertainty and progress annotations

### Consistency Guidelines
- Use consistent terminology across all annotations
- Maintain annotation style within project boundaries
- Follow semantic versioning for annotation schema evolution
- Document project-specific annotation conventions

### Performance Considerations
- Annotations are compile-time only and have no runtime overhead
- Use structured annotations for tool processing
- Keep free-text annotations concise but informative
- Balance annotation density with code readability

### Security and Privacy
- Never include sensitive data in annotations
- Use references rather than embedding confidential information
- Ensure annotations don't leak implementation details inappropriately
- Consider annotation visibility in shared codebases

## Tooling and Ecosystem

### Annotation Processors
- **Static Analysis**: Extract and validate annotation consistency
- **Documentation Generation**: Auto-generate docs from annotations
- **Code Quality Metrics**: Measure annotation coverage and quality
- **Translation Validation**: Verify annotation preservation across languages

### IDE Integration
- **Syntax Highlighting**: Special highlighting for annotation blocks
- **Auto-completion**: Suggest annotation templates and values
- **Validation**: Real-time checking of annotation syntax and semantics
- **Navigation**: Jump between related annotations and implementations

### AI Training Data
- **Corpus Generation**: Use annotated code for training AI models
- **Pattern Recognition**: Learn common annotation patterns
- **Quality Assessment**: Measure annotation effectiveness
- **Evolution Tracking**: Monitor annotation usage over time

This protocol represents a fundamental advancement in AI-assisted development, enabling enhanced code documentation, reasoning, and intelligent analysis while maintaining semantic fidelity and preserving human oversight capabilities.

## Open Issues

1. Finalize payload schemas and validation rules per annotation category with error codes.
2. Define precedence/merging rules across nested scopes with concrete examples.
3. Complete parser routing for reserved blocks and ensure round-trip in tooling.