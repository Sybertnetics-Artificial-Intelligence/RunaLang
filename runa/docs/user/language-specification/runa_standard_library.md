# Runa Standard Library Reference
*Comprehensive Guide to Runa's Built-in Functions and Modules*

**Last Updated**: 2025-08-15  
**Note**: This documentation reflects the current implementation with mathematical symbol enforcement.

## Overview

The Runa Standard Library provides a comprehensive set of built-in functions, types, and modules that enable rapid development while maintaining the language's natural syntax philosophy. The library is designed to be intuitive, with function names and operations that read like natural language.

Scope note (normative): Language rules (syntax, semantics, grammar, execution model) are defined in the language specification files (e.g., `runa_complete_specification.md`, `runa_formal_grammar.md`). This document is limited to library APIs and behavior. If conflicts arise, language specifications take precedence; this document should reference them rather than restate rules.

**Mathematical Symbol Note**: All examples use natural language operators (`plus`, `minus`, `multiplied by`, `divided by`) which are always valid. Mathematical symbols (`+`, `-`, `*`, `/`) are restricted to mathematical contexts only.

## Core Modules

### 1. Collections Module

#### List Operations

```runa
Note: List creation and manipulation
Let numbers be list containing 1, 2, 3, 4, 5
Let fruits be list containing "apple", "banana", "cherry"

Note: Basic operations
Let count be length of numbers              Note: Returns 5
Let first be numbers at index 0             Note: Returns 1
Let last be numbers at index -1             Note: Returns 5 (negative indexing)
Let slice be numbers from index 1 to 3      Note: Returns [2, 3]

Note: Modification operations
Add 6 to numbers                            Note: Appends to end: [1, 2, 3, 4, 5, 6]
Insert 0 into numbers at index 0            Note: Inserts at beginning: [0, 1, 2, 3, 4, 5, 6]
Remove item 3 from numbers                  Note: Removes first occurrence: [0, 1, 2, 4, 5, 6]
Remove item at index 0 from numbers         Note: Removes by index: [1, 2, 4, 5, 6]

Note: Functional operations
Let doubled be Map over numbers using lambda x: x multiplied by 2
Let evens be Filter numbers where lambda x: x modulo 2 equals 0
Let sum be Reduce numbers using lambda acc and x: acc plus x
Let sorted_numbers be Sort numbers                              Note: Ascending order
Let reverse_sorted be Sort numbers in descending order
```

#### Dictionary Operations

```runa
Note: Dictionary creation and access
Let user_data be dictionary with:
    "name" as "Alice"
    "age" as 30
    "city" as "New York"

Note: Access operations
Let name be user_data["name"]                Note: Direct access
Let age be user_data at key "age"           Note: Natural language access
Let has_email be user_data contains key "email"  Note: Returns false

Note: Modification operations
Set user_data["email"] to "alice@example.com"
Remove key "city" from user_data
Add key "phone" with value "555-1234" to user_data

Note: Iteration
For each key and value in user_data:
    Display key with message ": " with message value

Note: Dictionary comprehension
Let squared_numbers be dictionary with:
    For each num in list containing 1, 2, 3, 4, 5:
        num to string as key and num multiplied by num as value
```

#### Set Operations

```runa
Note: Set creation and operations
Let colors1 be set containing "red", "blue", "green"
Let colors2 be set containing "blue", "yellow", "red"

Note: Set operations
Let union be colors1 union colors2           Note: {"red", "blue", "green", "yellow"}
Let intersection be colors1 intersect colors2  Note: {"red", "blue"}
Let difference be colors1 minus colors2      Note: {"green"}
Let symmetric_diff be colors1 symmetric difference colors2  Note: {"green", "yellow"}

Note: Set membership and modification
Let has_red be colors1 contains "red"       Note: Returns true
Add "purple" to colors1
Remove "blue" from colors1
```

### 2. String Module

#### String Operations

```runa
Note: String creation and basic operations
Let greeting be "Hello, World!"
Let name be "Alice"
Let formatted_greeting be "Hello, " joined with name joined with "!"

Note: String properties
Let length be length of greeting             Note: Returns 13
Let is_empty be greeting is empty           Note: Returns false
Let upper_case be greeting converted to uppercase
Let lower_case be greeting converted to lowercase
Let title_case be greeting converted to title case

Note: String searching and testing
Let contains_world be greeting contains "World"     Note: Returns true
Let starts_with_hello be greeting starts with "Hello"  Note: Returns true
Let ends_with_exclamation be greeting ends with "!"    Note: Returns true
Let index_of_world be position of "World" in greeting  Note: Returns 7

Note: String manipulation
Let trimmed be trim whitespace from "  hello  "     Note: Returns "hello"
Let replaced be replace "World" with "Universe" in greeting
Let words be split greeting by " "                  Note: Returns ["Hello,", "World!"]
Let rejoined be join words with " "                 Note: Returns "Hello, World!"

Note: String formatting
Let formatted be format string "User {name} is {age} years old" with:
    name as "Alice"
    age as 30
Note: Returns "User Alice is 30 years old"
```

#### String Interpolation

```runa
Note: F-string style formatting
Let user_name be "Bob"
Let user_age be 25
Let message be f"User {user_name} is {user_age} years old"

Note: Advanced formatting
Let price be 123.456
Let formatted_price be f"Price: ${price:.2f}"      Note: Returns "Price: $123.46"
Let padded_number be f"{42:05d}"                    Note: Returns "00042"
```

### 3. Mathematical Module

#### Basic Arithmetic

```runa
Note: Basic operations (built-in operators)
Let sum be 10 plus 5                        Note: Addition: 15
Let difference be 10 minus 3                Note: Subtraction: 7
Let product be 4 multiplied by 6            Note: Multiplication: 24
Let quotient be 20 divided by 4             Note: Division: 5.0
Let remainder be 17 modulo 5                Note: Modulo: 2
Let power be 2 to the power of 8            Note: Exponentiation: 256

Note: Mathematical functions (natural language idioms)
Let absolute_value be absolute value of -10     Note: Returns 10
Let square_root be square root of 16            Note: Returns 4.0
Let ceiling be ceiling of 3.7                  Note: Returns 4
Let floor be floor of 3.7                      Note: Returns 3
Let rounded be round 3.6 to 0 decimal places   Note: Returns 4

Note: Helper functions for programmatic and AI use
Let result be pow with base as 2 and exponent as 8         Note: Returns 256
Let result be abs with x as -10                            Note: Returns 10
```

> In addition to natural language operators, the standard library provides helper processes for exponentiation (`pow`) and absolute value (`abs`), enabling programmatic and AI-generated code to perform these operations in a consistent way.

#### Advanced Mathematical Functions

```runa
Import module "math"

Note: Trigonometric functions
Let sine_value be math.sine of (math.PI divided by 2)      Note: Returns 1.0
Let cosine_value be math.cosine of 0                       Note: Returns 1.0
Let tangent_value be math.tangent of (math.PI divided by 4) Note: Returns 1.0

Note: Logarithmic functions
Let natural_log be math.natural logarithm of math.E        Note: Returns 1.0
Let log_base_10 be math.logarithm base 10 of 100          Note: Returns 2.0
Let log_base_2 be math.logarithm base 2 of 8              Note: Returns 3.0

Note: Constants
Let pi be math.PI                           Note: 3.141592653589793
Let e be math.E                             Note: 2.718281828459045
```

### 4. Input/Output Module

#### Console I/O

```runa
Note: Output operations
Display "Hello, World!"
Display user_name with message " is " with message user_age with message " years old"

Note: Input operations
Let user_input be input with prompt "Enter your name: "
Let number_input be input number with prompt "Enter a number: "
Let confirmed be input yes or no with prompt "Are you sure? "
```

#### File Operations

```runa
Import module "file"

Note: Reading files
Let content be read file "data.txt"
Let lines be read lines from file "data.txt"
Let binary_data be read binary file "image.jpg"

Note: Writing files
Write "Hello, World!" to file "output.txt"
Write lines to file "output.txt" with data as list containing "Line 1", "Line 2"
Append "New line" to file "output.txt"

Note: File information
Let file_exists be file "data.txt" exists
Let file_size be size of file "data.txt"
Let modification_time be modification time of file "data.txt"

Note: Directory operations
Let files_in_directory be list files in directory "data/"
Let subdirectories be list directories in directory "data/"
Create directory "new_folder"
Delete file "temporary.txt"
Delete directory "old_folder"
```

### 5. Time and Date Module

#### Date and Time Operations

```runa
Import module "datetime"

Note: Current time
Let now be current time
Let current_date be current date
Let current_timestamp be current timestamp

Note: Date creation
Let specific_date be create date with year 2023 and month 12 and day 25
Let specific_time be create time with hour 14 and minute 30 and second 0

Note: Date formatting
Let formatted_date be format date now as "YYYY-MM-DD"
Let formatted_time be format time now as "HH:MM:SS"
Let custom_format be format datetime now as "YYYY-MM-DD HH:MM:SS"

Note: Date arithmetic
Let tomorrow be now plus 1 day
Let next_week be now plus 7 days
Let last_month be now minus 1 month
Let difference be datetime1 minus datetime2  Note: Returns duration

Note: Date comparisons
Let is_after be date1 is after date2
Let is_before be date1 is before date2
Let is_same_day be date1 is same day as date2
```

### 6. Network Module

#### HTTP Operations

```runa
Import module "http"

Note: GET requests
Let response be http get from "https://api.example.com/users"
Let json_data be parse json from response.body

Note: POST requests
Let post_response be http post to "https://api.example.com/users" with data as:
    dictionary with:
        "name" as "Alice"
        "email" as "alice@example.com"

Note: Request with headers
Let response_with_auth be http get from "https://api.example.com/protected" with headers as:
    dictionary with:
        "Authorization" as "Bearer token123"
        "Content-Type" as "application/json"

Note: Error handling
Try:
    Let response be http get from "https://api.example.com/data"
    If response.status is equal to 200:
        Let data be parse json from response.body
        Display "Success: " with message data
    Otherwise:
        Display "HTTP Error: " with message response.status
Catch network_error:
    Display "Network error: " with message network_error.message
```

### 7. JSON Module

#### JSON Processing

```runa
Import module "json"

Note: Parsing JSON
Let json_string be '{"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]}'
Let parsed_data be parse json from json_string

Note: Creating JSON
Let user_data be dictionary with:
    "name" as "Bob"
    "age" as 25
    "active" as true
    "scores" as list containing 85, 92, 78

Let json_output be convert to json user_data
Let pretty_json be convert to pretty json user_data with indent 2

Note: JSON validation
Let is_valid be is valid json json_string
```

### 8. Regular Expressions Module

#### Pattern Matching

```runa
Import module "regex"

Note: Basic pattern matching
Let text be "The phone number is 555-1234"
Let phone_pattern be "\\d{3}-\\d{4}"
Let has_phone be text matches pattern phone_pattern

Note: Finding matches
Let all_matches be find all matches of phone_pattern in text
Let first_match be find first match of phone_pattern in text

Note: Replacing with patterns
Let censored be replace pattern phone_pattern with "XXX-XXXX" in text

Note: Extracting groups
Let email_pattern be "(\\w+)@(\\w+\\.\\w+)"
Let email_text be "Contact us at support@example.com"
Let groups be extract groups from email_text using email_pattern
Note: groups contains ["support", "example.com"]
```

### 9. Random Module

#### Random Number Generation

```runa
Import module "random"

Note: Basic random numbers
Let random_float be random number between 0.0 and 1.0
Let random_int be random integer between 1 and 100
Let random_choice be random item from list containing "red", "blue", "green"

Note: Random sampling
Let numbers be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Let sample be random sample of 3 items from numbers
Let shuffled be shuffle numbers

Note: Random with seed
Set random seed to 42
Let reproducible_random be random number between 0.0 and 1.0
```

### 10. Error Handling Module

#### Exception Types

```runa
Note: Built-in exception hierarchy
Type Error is Dictionary with:
    message as String
    stack_trace as List[String]

Type ValueError is Error      Note: Invalid values
Type TypeError is Error       Note: Type mismatches
Type IndexError is Error      Note: Invalid indices
Type KeyError is Error        Note: Missing dictionary keys
Type FileError is Error       Note: File operation errors
Type NetworkError is Error    Note: Network operation errors

Note: Custom exceptions
Type ValidationError is Error with:
    field_name as String
    invalid_value as Any

Note: Throwing exceptions
Process called "validate_age" that takes age as Integer:
    If age is less than 0:
        Throw ValueError with message "Age cannot be negative"
    If age is greater than 150:
        Throw ValueError with message "Age seems unrealistic"
    Return age
```

## Advanced Standard Library Features

### 1. Functional Programming Utilities

```runa
Import module "functional"

Note: Higher-order functions
Let numbers be list containing 1, 2, 3, 4, 5

Note: Map, Filter, Reduce
Let doubled be Map over numbers using lambda x: x multiplied by 2
Let evens be Filter numbers where lambda x: x modulo 2 equals 0
Let sum be Reduce numbers using lambda acc and x: acc plus x

Note: Function composition
Let add_one be lambda x: x plus 1
Let multiply_by_two be lambda x: x multiplied by 2
Let composed be compose add_one and multiply_by_two
Let result be composed with value as 5  Note: (5 + 1) * 2 = 12

Note: Partial application
Let add be lambda x and y: x plus y
Let add_five be partial add with x as 5
Let result be add_five with y as 3  Note: Returns 8

Note: Currying
Let curried_add be curry add
Let add_ten be curried_add with x as 10
Let result be add_ten with y as 5  Note: Returns 15
```

### 2. Concurrent Programming

```runa
Import module "concurrent"

Note: Thread-based concurrency
Let future1 be run in background: expensive_computation with data as data1
Let future2 be run in background: expensive_computation with data as data2

Let result1 be wait for future1
Let result2 be wait for future2

Note: Process pools
Let process_pool be create process pool with workers 4
Let futures be list containing
For each item in large_dataset:
    Add (submit to process_pool: process_item with item as item) to futures

Let results be list containing
For each future in futures:
    Add (wait for future) to results

Close process_pool
```

### 3. Data Validation

```runa
Import module "validation"

Note: Schema validation
Type UserSchema is Dictionary with:
    name as String where length is between 2 and 50
    age as Integer where value is between 0 and 120
    email as String where matches email pattern
    phone as Optional[String] where matches phone pattern

Process called "validate_user" that takes user_data as Dictionary returns UserSchema:
    Try:
        Return validate user_data against UserSchema
    Catch validation_error:
        Display "Validation failed: " with message validation_error.message
        Throw validation_error

Note: Custom validators
Process called "validate_positive" that takes value as Integer returns Integer:
    If value is less than or equal to 0:
        Throw ValidationError with message "Value must be positive"
    Return value
```

### 4. Configuration Management

```runa
Import module "config"

Note: Environment-based configuration
Let database_url be environment variable "DATABASE_URL" defaults to "sqlite:///app.db"
Let debug_mode be environment variable "DEBUG" as boolean defaults to false
Let port be environment variable "PORT" as integer defaults to 8000

Note: Configuration files
Let app_config be load config from file "app.toml"
Let database_config be app_config["database"]
Let server_config be app_config["server"]

Note: Dynamic configuration
When running in "development":
    Set log_level to "DEBUG"
    Set enable_hot_reload to true
When running in "production":
    Set log_level to "INFO"
    Set enable_hot_reload to false
```

### 5. Logging

```runa
Import module "logging"

Note: Basic logging
Log info message "Application started"
Log warning message "Configuration file not found, using defaults"
Log error message "Failed to connect to database"
Log debug message "Processing user request with ID: " joined with user_id

Note: Structured logging
Log info with data as dictionary with:
    "event" as "user_login"
    "user_id" as user_id
    "timestamp" as current timestamp
    "ip_address" as request.ip_address

Note: Custom loggers
Let app_logger be create logger "app"
Let db_logger be create logger "database"

app_logger.info with message "Application event"
db_logger.error with message "Database connection failed"
```

### 6. Testing Framework

```runa
Import module "testing"

Note: Unit tests
Test "addition works correctly":
    Let result be 2 plus 3
    Assert result equals 5

Test "list operations":
    Let numbers be list containing 1, 2, 3
    Add 4 to numbers
    Assert length of numbers equals 4
    Assert numbers contains 4

Note: Test fixtures
Define test fixture "sample_user":
    Return dictionary with:
        "name" as "Test User"
        "email" as "test@example.com"
        "age" as 25

Test "user validation" using fixture sample_user:
    Let validation_result be validate_user with user_data as sample_user
    Assert validation_result is not None

Note: Mocking
Test "external API call":
    Mock http_get to return fake_response
    Let result be fetch_user_data with id as 123
    Assert result["name"] equals "Mocked User"
    Verify http_get was called with url "https://api.example.com/users/123"
```

## AI-First Standard Library

The Runa standard library is engineered to be the premier toolkit for developing, orchestrating, and deploying advanced AI systems. It provides native abstractions for agents, skills, reasoning processes, and multi-agent coordination.

### Tier 0: Agent & Cognitive Primitives

#### Agent Core Module

```runa
Import module "agent"

Note: Create an agent with identity and capabilities
Let my_agent be Agent with:
    name as "DataProcessor"
    skills as list containing "data_analysis", "report_generation"
    goals as list containing "process_daily_data", "generate_insights"

Note: Register skills with the agent
Register skill "data_analysis" with agent my_agent:
    Process called "analyze_dataset" that takes data as DataFrame:
        Let statistics be calculate_statistics with data as data
        Let insights be extract_insights with statistics as statistics
        Return insights

Note: Create and manage tasks
Let task be Task with:
    name as "Process Quarterly Report"
    priority as "high"
    deadline as "2024-03-31"
    dependencies as list containing "data_collection", "validation"

Note: Set goals and track progress
Set goal "increase_accuracy" for agent my_agent with target 95.0
Let progress be get_progress for goal "increase_accuracy" of agent my_agent
```

#### Intention Management Module

```runa
Import module "intention"

Note: Create hierarchical task plans
Let plan be create_plan with:
    objective as "Deploy ML Model"
    tasks as list containing:
        Task with name as "Data Preparation" and duration as "2 days"
        Task with name as "Model Training" and duration as "1 week"
        Task with name as "Validation" and duration as "3 days"
        Task with name as "Deployment" and duration as "1 day"

Note: Execute plans with retry strategies
Execute plan with:
    plan as plan
    retry_strategy as "exponential_backoff"
    max_retries as 3
    on_failure as "notify_admin"

Note: Monitor intention progress
Let status be get_intention_status for plan
If status is "blocked":
    Let blockers be get_blockers for plan
    Display "Plan blocked by:" with message blockers
```

#### Memory Systems Module

```runa
Import module "memory"

Note: Episodic memory for storing experiences
Let episodic_memory be EpisodicMemory with capacity 10000
Store experience in episodic_memory with:
    event as "user_login"
    timestamp as current_time
    context as user_context
    outcome as "success"

Note: Semantic memory for knowledge
Let semantic_memory be SemanticMemory with embedding_model "text-embedding-ada-002"
Store knowledge in semantic_memory with:
    concept as "machine_learning"
    definition as "Subset of AI that enables systems to learn from data"
    relationships as list containing "artificial_intelligence", "data_science"

Note: Vector memory for similarity search
Let vector_memory be VectorMemory with dimensions 1536
Store vector in vector_memory with:
    id as "doc_123"
    vector as document_embedding
    metadata as document_metadata

Note: Memory policies and TTL
Set memory_policy for episodic_memory with:
    ttl as "30 days"
    priority as "high"
    compression as "lossy"
```

#### Reasoning Engine Module

```runa
Import module "reasoning"

Note: Create belief sets and world models
Let belief_set be BeliefSet with:
    facts as list containing:
        "All users require authentication"
        "Data must be encrypted in transit"
        "Backups run daily at 2 AM"
    confidence_scores as dictionary with:
        "All users require authentication" as 0.95
        "Data must be encrypted in transit" as 0.98
        "Backups run daily at 2 AM" as 0.90

Note: Forward chaining inference
Let conclusions be forward_chain with:
    beliefs as belief_set
    rules as inference_rules
    max_steps as 10

Note: Contradiction detection
Let contradictions be detect_contradictions in belief_set
For each contradiction in contradictions:
    Display "Contradiction detected:" with message contradiction
    Let resolution be suggest_resolution for contradiction
```

### Tier 1: Multi-Agent Systems & Communication

#### Agent Communication Module

```runa
Import module "comms"

Note: Create secure messaging channels
Let channel be create_channel with:
    name as "data_processing_team"
    participants as list containing agent1, agent2, agent3
    encryption as "AES-256"
    authentication as "JWT"

Note: Send and receive messages
Send message to channel with:
    sender as my_agent
    content as "Data processing complete"
    priority as "normal"
    ttl as "1 hour"

Note: Message routing and filtering
Let filtered_messages be filter_messages in channel with:
    sender as "DataProcessor"
    priority as "high"
    time_range as "last_24_hours"

Note: Mailbox management
Let mailbox be create_mailbox for agent my_agent
Let unread_count be get_unread_count for mailbox
If unread_count is greater than 10:
    Display "High message volume detected"
```

#### Protocol Management Module

```runa
Import module "protocols"

Note: Contract Net Protocol for task allocation
Let contract_net be ContractNet with:
    initiator as coordinator_agent
    task as "process_large_dataset"
    participants as available_agents
    deadline as "2 hours"

Note: Execute contract net
Let winner be execute_contract_net with contract_net as contract_net
Assign task to winner

Note: Delegation protocol
Let delegation be create_delegation with:
    delegator as manager_agent
    delegate as worker_agent
    task as "generate_report"
    authority_level as "full"
    constraints as task_constraints

Note: Negotiation protocol
Let negotiation be start_negotiation with:
    parties as list containing agent1, agent2
    topic as "resource_allocation"
    constraints as negotiation_constraints
    timeout as "30 minutes"

Let agreement be execute_negotiation with negotiation as negotiation
```

#### Trust Management Module

```runa
Import module "trust"

Note: Dynamic trust scoring
Let trust_score be calculate_trust_score for agent worker_agent with:
    history as interaction_history
    performance as recent_performance
    reliability as uptime_metrics
    security as security_incidents

Note: Anomaly detection
Let anomalies be detect_anomalies in agent_behavior with:
    baseline as normal_behavior_patterns
    sensitivity as 0.8
    time_window as "7 days"

Note: Reputation management
Let reputation be get_reputation for agent worker_agent
If reputation is less than 0.5:
    Display "Low reputation agent detected"
    Let actions be suggest_reputation_actions for worker_agent

Note: Trust-based decision making
Let decision be make_trust_decision with:
    agents as candidate_agents
    task as "sensitive_data_processing"
    required_trust as 0.8
```

### Tier 2: Knowledge, Data & Scientific Computing

#### Ontology Management Module

```runa
Import module "ontology"

Note: Create and manage knowledge representations
Let ontology be create_ontology with:
    name as "business_domain"
    concepts as business_concepts
    relationships as concept_relationships
    axioms as domain_axioms

Note: Align ontologies
Let alignment be align_ontologies with:
    source as source_ontology
    target as target_ontology
    method as "semantic_similarity"
    threshold as 0.7

Note: Query ontological knowledge
Let results be query_ontology with:
    ontology as ontology
    query as "What are the subtypes of Customer?"
    reasoning as "subsumption"
```

#### Context Management Module

```runa
Import module "context"

Note: Session-scoped memory management
Let context_window be create_context_window with:
    size as 4096
    strategy as "sliding_window"
    priority as "recent"

Note: Context propagation
Propagate context with:
    source as current_context
    target as child_process
    include as list containing "user_preferences", "session_data"
    exclude as list containing "sensitive_data"

Note: Constraint management
Let constraints be get_active_constraints in current_context
For each constraint in constraints:
    Let validity be validate_constraint with constraint as constraint
    If not validity:
        Display "Constraint violation:" with message constraint
```

#### Embedding and Vector Operations Module

```runa
Import module "embed"

Note: Generate embeddings
Let embedding be generate_embedding with:
    text as document_text
    model as "text-embedding-ada-002"
    normalize as true

Note: Similarity search
Let similar_docs be find_similar with:
    query_embedding as query_vector
    corpus_embeddings as document_vectors
    threshold as 0.8
    top_k as 10

Note: Embedding operations
Let combined_embedding be combine_embeddings with:
    embeddings as list containing emb1, emb2, emb3
    method as "weighted_average"
    weights as list containing 0.5, 0.3, 0.2
```

#### Advanced Data Structures Module

```runa
Import module "data"

Note: High-performance DataFrame
Let df be DataFrame with:
    data as raw_data
    columns as column_names
    index as row_indices
    dtypes as column_types

Note: DataFrame operations
Let filtered_df be filter df where column "age" is greater than 25
Let grouped_df be group df by column "department"
Let aggregated_df be aggregate grouped_df using:
    "salary" as "mean"
    "experience" as "max"

Note: Series operations
Let series be Series with data as time_series_data
Let moving_avg be calculate_moving_average for series with window 7

Note: Graph data structures
Let graph be Graph with:
    nodes as graph_nodes
    edges as graph_edges
    directed as true
    weighted as true

Note: Graph algorithms
Let shortest_path be find_shortest_path in graph from "A" to "Z"
Let communities be detect_communities in graph using "louvain"
```

#### Advanced Mathematics Module

```runa
Import module "statistics"

Note: Statistical analysis
Let stats be calculate_statistics with data as dataset:
    mean as true
    median as true
    std_dev as true
    percentiles as list containing 25, 50, 75

Note: Hypothesis testing
Let test_result be perform_t_test with:
    sample1 as group_a_data
    sample2 as group_b_data
    alpha as 0.05
    alternative as "two_sided"

Note: Machine learning metrics
Let metrics be calculate_metrics with:
    predictions as model_predictions
    actuals as true_values
    metrics as list containing "accuracy", "precision", "recall", "f1"

Note: Arbitrary-precision arithmetic
Let precise_result be calculate_precise with:
    expression as "2^1000"
    precision as 1000
    rounding as "nearest"
```

### Tier 3: Environment Interaction & Tooling

#### Environment Interface Module

```runa
Import module "env"

Note: Abstract sensor interface
Let sensor be create_sensor with:
    type as "temperature"
    location as "server_room"
    sampling_rate as "1 per minute"
    calibration as sensor_calibration

Note: Actuator interface
Let actuator be create_actuator with:
    type as "valve_control"
    location as "cooling_system"
    range as actuator_range
    safety_limits as safety_constraints

Note: Environment perception
Let perception be perceive_environment with:
    sensors as active_sensors
    fusion_method as "kalman_filter"
    confidence_threshold as 0.8

Note: Action execution
Let action_result be execute_action with:
    actuator as cooling_valve
    action as "open_50_percent"
    safety_check as true
    timeout as "30 seconds"
```

#### Simulation Environment Module

```runa
Import module "sim"

Note: Create sandboxed simulation
Let simulation be create_simulation with:
    environment as "data_center"
    agents as simulation_agents
    constraints as simulation_constraints
    duration as "24 hours"

Note: Run simulation
Let results be run_simulation with:
    simulation as simulation
    scenarios as test_scenarios
    metrics as performance_metrics
    logging as "detailed"

Note: Simulation analysis
Let analysis be analyze_simulation with:
    results as simulation_results
    baseline as expected_performance
    anomalies as true
    recommendations as true
```

#### Tool Registry Module

```runa
Import module "tools"

Note: Register external tools
Register tool "database_query" with:
    function as execute_sql_query
    parameters as sql_parameters
    permissions as "read_only"
    rate_limit as "100 per minute"

Note: Tool discovery and selection
Let available_tools be discover_tools in environment
Let selected_tool be select_tool with:
    task as "data_analysis"
    requirements as tool_requirements
    preferences as user_preferences

Note: Secure tool execution
Let result be execute_tool securely with:
    tool as selected_tool
    parameters as tool_parameters
    sandbox as "isolated"
    timeout as "5 minutes"
```

### Tier 4: Meta-Cognition & Strategy

#### Meta-Cognition Module

```runa
Import module "meta"

Note: Confidence estimation
Let confidence be estimate_confidence with:
    task as current_task
    experience as task_history
    complexity as task_complexity
    resources as available_resources

Note: Knowledge gap identification
Let gaps be identify_knowledge_gaps with:
    current_knowledge as knowledge_base
    required_knowledge as task_requirements
    priority as "high"

Note: Self-awareness assessment
Let limitations be assess_limitations with:
    capabilities as agent_capabilities
    task_requirements as current_requirements
    performance_history as recent_performance

Note: Learning needs analysis
Let learning_needs be analyze_learning_needs with:
    gaps as knowledge_gaps
    opportunities as learning_opportunities
    constraints as time_constraints
```

#### Strategy Management Module

```runa
Import module "strategy"

Note: Chain of Thought reasoning
Let reasoning_chain be chain_of_thought with:
    problem as current_problem
    steps as reasoning_steps
    validation as "logical_consistency"
    max_depth as 5

Note: Tree of Thoughts exploration
Let thought_tree be tree_of_thoughts with:
    root as initial_hypothesis
    branching_factor as 3
    max_depth as 4
    evaluation_metric as "solution_quality"

Note: Strategy selection
Let strategy be select_strategy with:
    problem as current_problem
    context as problem_context
    available_strategies as known_strategies
    constraints as resource_constraints

Note: Strategy execution and monitoring
Let execution_plan be execute_strategy with:
    strategy as selected_strategy
    monitoring as "continuous"
    adaptation as "dynamic"
    fallback as backup_strategy
```

### Tier 5: LLM Orchestration & Control

#### LLM Core Module

```runa
Import module "llm"

Note: Unified LLM interface
Let llm_client be create_llm_client with:
    model as "gpt-4"
    api_key as api_credentials
    configuration as model_config

Note: LLM invocation
Let response be invoke_llm with:
    client as llm_client
    prompt as user_prompt
    parameters as generation_parameters
    streaming as false

Note: Model management
Let available_models be list_available_models in llm_client
Let model_info be get_model_info for model "gpt-4"
```

#### LLM Router Module

```runa
Import module "llm.router"

Note: Intelligent model selection
Let selected_model be route_request with:
    request as user_request
    criteria as selection_criteria:
        cost as "minimize"
        latency as "under_2_seconds"
        quality as "high"
    available_models as model_pool

Note: Load balancing
Let balanced_model be select_balanced_model with:
    models as available_models
    current_load as model_loads
    strategy as "round_robin"
```

#### LLM Chain Module

```runa
Import module "llm.chain"

Note: Create reasoning chains
Let chain be create_chain with:
    steps as chain_steps:
        Step with name as "analyze" and model as "gpt-4"
        Step with name as "synthesize" and model as "claude-3"
        Step with name as "validate" and model as "gpt-4"
    dependencies as step_dependencies
    error_handling as "retry_with_fallback"

Note: Execute chain
Let chain_result be execute_chain with:
    chain as chain
    input as user_input
    monitoring as "step_by_step"
    timeout as "5 minutes"
```

#### LLM Agent Module

```runa
Import module "llm.agent"

Note: Central executive agent
Let executive_agent be create_executive_agent with:
    capabilities as agent_capabilities
    goals as system_goals
    constraints as operational_constraints

Note: Agent orchestration
Let orchestration_result be orchestrate_agents with:
    executive as executive_agent
    agents as subordinate_agents
    task as complex_task
    coordination as "hierarchical"
```

#### LLM Memory Module

```runa
Import module "llm.memory"

Note: Shared memory for LLM ensemble
Let shared_memory be create_shared_memory with:
    capacity as "10GB"
    access_pattern as "read_write"
    persistence as "temporary"

Note: Memory operations
Store in shared_memory with:
    key as "conversation_context"
    value as conversation_history
    ttl as "1 hour"

Let context be retrieve from shared_memory with key as "conversation_context"
```

#### LLM Tools Module

```runa
Import module "llm.tools"

Note: Function calling interface
Let tool_registry be create_tool_registry with:
    tools as available_tools
    descriptions as tool_descriptions
    schemas as tool_schemas

Note: Tool execution
Let tool_result be execute_tool_call with:
    registry as tool_registry
    call as function_call
    parameters as call_parameters
    validation as "strict"
```

#### LLM Evaluation Module

```runa
Import module "llm.evaluation"

Note: Model evaluation
Let evaluation_result be evaluate_model with:
    model as test_model
    dataset as evaluation_dataset
    metrics as evaluation_metrics:
        accuracy as true
        fluency as true
        coherence as true
        safety as true

Note: Human evaluation
Let human_score be human_evaluate with:
    responses as model_responses
    criteria as evaluation_criteria
    evaluators as human_evaluators
```

#### LLM Embedding Module

```runa
Import module "llm.embedding"

Note: Embedding generation
Let embeddings be generate_embeddings with:
    texts as document_texts
    model as "text-embedding-ada-002"
    batch_size as 100
    normalize as true

Note: Embedding operations
Let similarity be calculate_similarity between embedding1 and embedding2
Let cluster_assignments be cluster_embeddings with:
    embeddings as document_embeddings
    method as "kmeans"
    n_clusters as 5
```

### Tier 6: LLM Development & Training

#### Neural Network Module

```runa
Import module "nn"

Note: Layer definitions
Let dense_layer be DenseLayer with:
    input_size as 784
    output_size as 128
    activation as "relu"
    dropout as 0.2

Let conv_layer be ConvLayer with:
    in_channels as 3
    out_channels as 64
    kernel_size as 3
    stride as 1
    padding as "same"

Note: Attention mechanisms
Let attention_layer be AttentionLayer with:
    embed_dim as 512
    num_heads as 8
    dropout as 0.1
    bias as true

Note: Layer composition
Let model be Sequential with layers as list containing:
    dense_layer
    conv_layer
    attention_layer
```

#### Model Definition Module

```runa
Import module "model"

Note: High-level architecture definition
Let architecture be define_architecture with:
    input_shape as [224, 224, 3]
    output_shape as [1000]
    layers as layer_definitions:
        "conv1" as ConvLayer with filters 64 and kernel 7
        "pool1" as MaxPoolLayer with pool_size 2
        "conv2" as ConvLayer with filters 128 and kernel 3
        "pool2" as MaxPoolLayer with pool_size 2
        "flatten" as FlattenLayer
        "dense1" as DenseLayer with units 512
        "output" as DenseLayer with units 1000 and activation "softmax"
    connections as layer_connections

Note: Model configuration
Let config be ModelConfig with:
    architecture as architecture
    optimizer as "adam"
    learning_rate as 0.001
    loss_function as "categorical_crossentropy"
    metrics as list containing "accuracy", "precision", "recall"
```

#### Dataset Management Module

```runa
Import module "dataset"

Note: Dataset loading and preprocessing
Let dataset be load_dataset with:
    path as "data/training/"
    format as "image"
    preprocessing as preprocessing_pipeline:
        "resize" as ResizeTransform with size [224, 224]
        "normalize" as NormalizeTransform with mean [0.485, 0.456, 0.406] and std [0.229, 0.224, 0.225]
        "augment" as AugmentationTransform with:
            "rotation" as RandomRotation with max_angle 15
            "flip" as RandomHorizontalFlip with probability 0.5

Note: Data loading
Let dataloader be create_dataloader with:
    dataset as dataset
    batch_size as 32
    shuffle as true
    num_workers as 4
```

#### Tokenizer Module

```runa
Import module "tokenizer"

Note: BPE tokenizer
Let tokenizer be BPETokenizer with:
    vocab_size as 50000
    min_frequency as 2
    special_tokens as list containing "[PAD]", "[UNK]", "[CLS]", "[SEP]"

Note: Train tokenizer
Train tokenizer with:
    data as training_texts
    algorithm as "bpe"
    merge_operations as 10000

Note: Tokenization
Let tokens be tokenize with:
    tokenizer as tokenizer
    text as input_text
    add_special_tokens as true
    max_length as 512
    padding as "max_length"
    truncation as true

Note: Detokenization
Let text be detokenize with:
    tokenizer as tokenizer
    tokens as token_ids
    skip_special_tokens as true
```

#### Training Module

```runa
Import module "train"

Note: Training loop
Let training_result be train_model with:
    model as neural_network
    dataloader as training_dataloader
    optimizer as adam_optimizer
    loss_function as cross_entropy_loss
    epochs as 100
    validation_data as validation_dataloader
    callbacks as training_callbacks:
        "early_stopping" as EarlyStoppingCallback with patience 10
        "model_checkpoint" as ModelCheckpointCallback with save_best_only true
        "learning_rate_scheduler" as LRSchedulerCallback with scheduler cosine_annealing

Note: Training monitoring
Let metrics be get_training_metrics for training_result
Display "Final accuracy:" with message metrics["accuracy"]
```

#### Optimization Module

```runa
Import module "opt"

Note: Optimizer configuration
Let optimizer be AdamWOptimizer with:
    learning_rate as 0.001
    weight_decay as 0.01
    beta1 as 0.9
    beta2 as 0.999
    epsilon as 1e-8

Note: Learning rate schedulers
Let scheduler be CosineAnnealingScheduler with:
    optimizer as optimizer
    T_max as 100
    eta_min as 1e-6

Note: Gradient clipping
Let clipped_gradients be clip_gradients with:
    gradients as model_gradients
    max_norm as 1.0
    norm_type as 2
```

#### Metrics Module

```runa
Import module "metrics"

Note: Training metrics
Let training_metrics be calculate_training_metrics with:
    predictions as model_predictions
    targets as true_targets
    metrics as list containing:
        "accuracy" as AccuracyMetric
        "precision" as PrecisionMetric with average "weighted"
        "recall" as RecallMetric with average "weighted"
        "f1_score" as F1ScoreMetric with average "weighted"

Note: Custom metrics
Let custom_metric be CustomMetric with:
    name as "business_metric"
    function as business_metric_function
    higher_is_better as true
```

#### Distributed Training Module

```runa
Import module "distribute"

Note: Distributed training setup
Let distributed_config be DistributedConfig with:
    backend as "nccl"
    world_size as 4
    rank as 0
    init_method as "env://"

Note: Distributed data parallel
Let ddp_model be DistributedDataParallel with:
    model as neural_network
    device_ids as list containing 0, 1, 2, 3
    output_device as 0
    find_unused_parameters as false

Note: Synchronization
Synchronize model parameters across devices
```

#### Experiment Tracking Module

```runa
Import module "experiment"

Note: Experiment tracking
Let experiment be create_experiment with:
    name as "transformer_training"
    description as "Training transformer model for text classification"
    tags as list containing "nlp", "transformer", "classification"

Note: Log parameters
Log parameters for experiment with:
    "learning_rate" as 0.001
    "batch_size" as 32
    "epochs" as 100
    "model_size" as "base"

Note: Log metrics
Log metrics for experiment with:
    "train_loss" as current_loss
    "val_accuracy" as validation_accuracy
    "epoch" as current_epoch

Note: Save artifacts
Save artifact for experiment with:
    name as "model_checkpoint"
    path as model_path
    type as "model"
```

#### Model Compilation Module

```runa
Import module "compile"

Note: Model optimization
Let optimized_model be optimize_model with:
    model as trained_model
    optimization_level as "O2"
    target_device as "GPU"
    precision as "mixed"

Note: Model export
Let exported_model be export_model with:
    model as optimized_model
    format as "onnx"
    input_shape as [1, 3, 224, 224]
    output_shape as [1, 1000]
    dynamic_axes as dynamic_axis_config

Note: Quantization
Let quantized_model be quantize_model with:
    model as trained_model
    method as "int8"
    calibration_data as calibration_dataset
    target_device as "CPU"
```

### Tier 7: Security, Testing, and Developer Utilities

#### Security Module

```runa
Import module "security"

Note: Sandboxing
Let sandbox be create_sandbox with:
    permissions as sandbox_permissions:
        "file_read" as list containing "/data/input/"
        "file_write" as list containing "/data/output/"
        "network" as false
        "system" as false
    memory_limit as "512MB"
    cpu_limit as "2 cores"

Note: Permission management
Let permission_check be check_permissions for agent worker_agent with:
    resource as "sensitive_database"
    action as "read"
    context as current_context

Note: Capability guards
Let guarded_function be guard_function with:
    function as sensitive_operation
    capabilities as required_capabilities:
        "data_access" as "read_only"
        "network_access" as "none"
    validation as "strict"

Note: Prompt injection prevention
Let sanitized_prompt be sanitize_prompt with:
    prompt as user_input
    allowed_tokens as safe_token_set
    max_length as 1000
    validation as "content_filter"
```

#### Testing Framework Module

```runa
Import module "testing"

Note: Unit testing for agents
Test "agent_skill_execution":
    Let test_agent be create_test_agent with skills as list containing "test_skill"
    Let result be execute_skill "test_skill" with agent test_agent and input test_data
    Assert result is not None
    Assert result["status"] equals "success"

Note: Integration testing for multi-agent systems
Test "multi_agent_coordination":
    Let agent1 be create_test_agent with name "coordinator"
    Let agent2 be create_test_agent with name "worker"
    Let coordination_result be coordinate_agents with:
        coordinator as agent1
        workers as list containing agent2
        task as test_task
    Assert coordination_result["status"] equals "completed"

Note: Property-based testing
Test "data_processing_properties":
    For all data in generate_test_data():
        Let processed be process_data with data as data
        Assert length of processed is greater than 0
        Assert all items in processed satisfy validation_criteria

Note: Performance testing
Test "agent_response_time":
    Let start_time be current_time
    Let response be agent_response with agent test_agent and input test_input
    Let end_time be current_time
    Let response_time be end_time minus start_time
    Assert response_time is less than 1000  Note: milliseconds
```

#### Cryptographic Module

```runa
Import module "crypto"

Note: Hashing
Let hash_value be hash_data with:
    data as sensitive_data
    algorithm as "sha256"
    salt as random_salt

Note: Digital signatures
Let signature be sign_data with:
    data as document_data
    private_key as user_private_key
    algorithm as "rsa"
    padding as "pkcs1"

Note: Verification
Let is_valid be verify_signature with:
    data as document_data
    signature as document_signature
    public_key as user_public_key
    algorithm as "rsa"

Note: Encryption
Let encrypted_data be encrypt_data with:
    data as plaintext_data
    key as encryption_key
    algorithm as "aes-256-gcm"
    iv as random_iv

Note: Decryption
Let decrypted_data be decrypt_data with:
    data as encrypted_data
    key as encryption_key
    algorithm as "aes-256-gcm"
    iv as original_iv
```

#### Foreign Function Interface Module

```runa
Import module "interop"

Note: C library binding
Let c_library be load_library with:
    path as "libmath.so"
    functions as function_signatures:
        "add" as Function[Integer, Integer, Integer]
        "multiply" as Function[Integer, Integer, Integer]
        "sqrt" as Function[Float, Float]

Note: Call C functions
Let result be call_function with:
    library as c_library
    function as "add"
    arguments as list containing 5, 3

Note: Python interop
Let python_module be import_python_module with:
    module_name as "numpy"
    functions as list containing "array", "mean", "std"

Note: Call Python functions
Let numpy_array be call_python_function with:
    module as python_module
    function as "array"
    arguments as list containing [1, 2, 3, 4, 5]

Note: Rust interop
Let rust_library be load_rust_library with:
    path as "target/release/librust_math.rlib"
    functions as rust_function_signatures
```

## Performance and Memory Management

### 1. Memory-Efficient Operations

```runa
Import module "itertools"

Note: Lazy evaluation with generators
Process called "fibonacci_sequence":
    Let a be 0
    Let b be 1
    Loop forever:
        Yield a
        Let temp be a
        Set a to b
        Set b to temp plus b

Note: Using generators efficiently
Let first_ten_fibonacci be take 10 from fibonacci_sequence()

Note: Memory-efficient file processing
Process called "process_large_file" that takes filename:
    For each line in read lines lazily from file filename:
        Let processed_line be process_line with line as line
        Yield processed_line
```

### 2. Performance Utilities

```runa
Import module "performance"

Note: Timing operations
Let start_time be current time
expensive_operation()
Let end_time be current time
Let duration be end_time minus start_time
Display "Operation took " with message duration with message " seconds"

Note: Profiling
Profile "user_processing":
    For each user in users:
        process_user with user as user

Note: Caching
Let cached_function be cache expensive_function with max_size 100
Let result1 be cached_function with input as data  Note: Computed
Let result2 be cached_function with input as data  Note: Retrieved from cache
```

## Standard Library Organization

### Module Hierarchy

```
runa.std/
├── collections/          Note: List, Dict, Set operations
├── string/              Note: String manipulation
├── math/                Note: Mathematical functions
├── io/                  Note: Input/output operations
├── file/                Note: File system operations
├── datetime/            Note: Date and time utilities
├── network/             Note: Network operations
├── json/                Note: JSON processing
├── regex/               Note: Regular expressions
├── random/              Note: Random number generation
├── functional/          Note: Functional programming utilities
├── concurrent/          Note: Concurrency and parallelism
├── validation/          Note: Data validation
├── config/              Note: Configuration management
├── logging/             Note: Logging utilities
├── testing/             Note: Testing framework
├── performance/         Note: Performance utilities
├── system/              Note: System interaction
├── crypto/              Note: Cryptographic primitives
├── interop/             Note: Foreign function interface
└── security/            Note: Security and sandboxing

Note: AI-First Modules (Tier 0-7)
runa.ai/
├── agent/               Note: Agent core, skills, tasks, goals
├── intention/           Note: Goal management, task planning, retry strategies
├── memory/              Note: Episodic, semantic, vector memory systems
├── reasoning/           Note: Belief sets, inference engines, contradiction detection
├── comms/               Note: Agent-to-agent messaging and channels
├── protocols/           Note: Contract net, delegation, negotiation protocols
├── trust/               Note: Trust scoring, anomaly detection, reputation management
├── ontology/            Note: Knowledge representations and taxonomies
├── context/             Note: Session memory and constraint propagation
├── embed/               Note: Vector embedding generation and similarity search
├── data/                Note: High-performance DataFrame, Series, Graph structures
├── statistics/          Note: Advanced mathematical and statistical utilities
├── env/                 Note: Environment interfaces (sensors, actuators)
├── sim/                 Note: Sandboxed simulation environments
├── tools/               Note: External tool registry and secure execution
├── meta/                Note: Confidence estimation, knowledge gap identification
└── strategy/            Note: Chain of Thought, Tree of Thoughts, strategy selection

runa.llm/
├── core/                Note: Unified LLM interface and model management
├── router/              Note: Intelligent model selection and load balancing
├── chain/               Note: Multi-step reasoning chains (DAGs)
├── agent/               Note: Central executive agent for LLM orchestration
├── memory/              Note: Shared memory for LLM ensemble
├── tools/               Note: Function calling interface
├── evaluation/          Note: Model evaluation and human assessment
└── embedding/           Note: Embedding generation and operations

runa.train/
├── nn/                  Note: Neural network layers and attention mechanisms
├── model/               Note: High-level architecture definitions
├── dataset/             Note: Dataset loading and preprocessing
├── tokenizer/           Note: BPE and other tokenization methods
├── train/               Note: Training loops and monitoring
├── opt/                 Note: Optimizers and learning rate schedulers
├── metrics/             Note: Training metrics and custom evaluations
├── distribute/          Note: Distributed training and synchronization
├── experiment/          Note: Experiment tracking and artifact management
└── compile/             Note: Model optimization, export, and quantization
```

### Import Conventions

```runa
Note: Import entire module
Import module "math"
Let result be math.sine of angle

Note: Import specific functions
Import { sine, cosine, PI } from module "math"
Let result be sine of angle

Note: Import with alias
Import module "datetime" as "dt"
Let now be dt.current_time

Note: Conditional imports
When target_language is "Python":
    Import module "python_specific"
When target_language is "JavaScript":
    Import module "javascript_specific"
```

## Extension Points

### 1. Custom Collection Types

```runa
Note: Implementing custom collections
Type CircularBuffer[T] is Dictionary with:
    Private items as Array[T, capacity]
    Private head as Integer
    Private tail as Integer
    Private capacity as Integer
    
    Process called "add" that takes item as T:
        Set self.items[self.tail] to item
        Set self.tail to (self.tail plus 1) modulo self.capacity
        If self.tail is equal to self.head:
            Set self.head to (self.head plus 1) modulo self.capacity
```

### 2. Custom Validators

```runa
Note: Creating domain-specific validators
Process called "validate_credit_card" that takes card_number as String returns Boolean:
    Note: Luhn algorithm implementation
    Let digits be convert card_number to digit list
    Let checksum be calculate_luhn_checksum with digits as digits
    Return checksum modulo 10 equals 0
```

### 3. Plugin System

```runa
Note: Registering custom functionality
Register plugin "custom_math" with functions:
    "advanced_statistics" as calculate_advanced_stats
    "matrix_operations" as matrix_multiply

Note: Using registered plugins
Import plugin "custom_math"
Let stats be custom_math.advanced_statistics with data as dataset
```

## Best Practices

### 1. Error Handling
- Use Result types for operations that might fail
- Provide clear error messages with context
- Use appropriate exception types for different error categories

### 2. Performance
- Use lazy evaluation for large datasets
- Implement caching for expensive operations
- Consider memory usage in data structure choice

### 3. API Design
- Use natural language naming conventions
- Provide both verbose and concise API variants
- Include comprehensive documentation and examples

### 4. Testing
- Write unit tests for all public functions
- Use property-based testing for complex algorithms
- Provide test fixtures for common scenarios

This standard library provides a solid foundation for Runa development while maintaining the language's philosophy of natural, readable code that bridges human thinking and machine execution.

## Open Issues

1. Ensure all stdlib examples reference the canonical language spec for mode-scoped syntax.
2. Audit modules for any restated language rules; replace with links to spec sections.