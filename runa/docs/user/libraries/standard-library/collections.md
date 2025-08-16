# Runa Collections Module Guide

The Runa Collections module provides both fundamental and advanced data structures that deliver enterprise-grade performance with natural language syntax. This module includes essential collections for everyday programming as well as sophisticated structures for advanced algorithms.

## Table of Contents

### 🏗️ Core New Collections (Priority Access)
- [Priority Queue Operations](#priority-queue-operations-priority_queueruna) - Dictionary-based heap with min/max support and priority updates
- [Segment Tree Operations](#segment-tree-operations-segment_treeruna) - Range query data structure with lazy propagation and 2D support
- [Set Utilities](#set-utilities-setruna) - Comprehensive set operations with algebra and transformations
- [Ordered Dictionary Operations](#ordered-dictionary-operations-ordered_dictruna) - Dictionary with insertion order preservation and manipulation

### 📚 Basic Collections
- [Dictionary Operations](#dictionary-operations-dictruna) - Enhanced dictionary utilities with filtering and transformations
- [Deque Operations](#deque-operations-dequeruna) - Double-ended queue with efficient operations at both ends
- [Counter Operations](#counter-operations-counterruna) - Frequency counting and statistical analysis
- [Default Dictionary Operations](#default-dictionary-operations-default_dictruna) - Dictionary with automatic default value creation
- [Chain Map Operations](#chain-map-operations-chain_mapruna) - Hierarchical key lookup across multiple dictionaries
- [Bloom Filter Operations](#bloom-filter-operations-bloom_filterruna) - Probabilistic membership testing
- [Disjoint Set Operations](#disjoint-set-operations-disjoint_setruna) - Union-Find operations for connectivity

### 🚀 Advanced Collections
- [Trie Operations](#trie-operations-trieruna) - Prefix tree for efficient string operations
- [LRU Cache Operations](#lru-cache-operations-lru_cacheruna) - High-performance caching with O(1) operations
- [Suffix Array Operations](#suffix-array-operations-suffix_arrayruna) - Advanced string processing and pattern matching
- [Skip List Operations](#skip-list-operations-skip_listruna) - Probabilistic balanced tree with ordered operations
- [Frozen Set Operations](#frozen-set-operations-frozen_setruna) - Immutable set with hashable properties
- [Multiset Operations](#multiset-operations-multisetruna) - Bag data structure for frequency analysis
- [Graph Operations](#graph-operations-graphruna) - Comprehensive graph algorithms
- [Heap Operations](#heap-operations-heapruna) - Priority queue with min/max heap operations
- [Enhanced List Operations](#enhanced-list-operations-listruna) - Advanced list operations with statistical analysis

### 🔧 Integration & Performance
- [Integration Examples](#integration-examples) - Multi-structure data pipelines
- [Testing Your Code](#testing-your-code) - Test coverage and execution
- [Performance Characteristics](#performance-characteristics) - Time and space complexity analysis
- [Advanced Optimization Techniques](#advanced-optimization-techniques) - Memory and performance tuning

## Overview

The collections module consists of two categories of data structures:

### Basic Collections (Core Module)
- **dict.runa**: Enhanced dictionary operations with utilities, filtering, and transformations
- **deque.runa**: Double-ended queue with efficient operations at both ends
- **counter.runa**: Frequency counting and statistical analysis with advanced metrics
- **default_dict.runa**: Dictionary with automatic default value creation
- **chain_map.runa**: Hierarchical key lookup across multiple dictionaries
- **bloom_filter.runa**: Probabilistic membership testing with configurable false positive rates
- **disjoint_set.runa**: Union-Find operations for connectivity and graph algorithms

### Advanced Collections (Extended Module)
- **trie.runa**: Prefix tree for efficient string operations and autocompletion
- **lru_cache.runa**: Least Recently Used cache with O(1) operations and advanced eviction policies
- **segment_tree.runa**: Range query optimization for sum, min, max, and other operations
- **suffix_array.runa**: Advanced string processing and pattern matching algorithms
- **skip_list.runa**: Probabilistic balanced tree with ordered operations
- **frozen_set.runa**: Immutable set with hashable properties for dictionary keys and caching
- **multiset.runa**: Bag data structure for frequency analysis and statistical operations
- **graph.runa**: Comprehensive graph algorithms including pathfinding and analysis
- **heap.runa**: Priority queue with min/max heap operations and timestamp handling
- **list.runa**: Enhanced list operations with statistical analysis and functional programming support

## Basic Collections

### Dictionary Operations (`dict.runa`)

Enhanced dictionary utilities that extend beyond basic key-value operations with advanced querying, filtering, and transformation capabilities.

#### Core Dictionary Operations

```runa
Note: Create and manipulate dictionaries
Let user_data be from_pairs with list containing ("name", "Alice"), ("age", 25), ("city", "Boston")

Note: Safe operations with default values
Let name be get_safe with user_data and "name" and "Unknown"
Let country be get_safe with user_data and "country" and "USA"

Display "User: " with message name with message " from " with message country

Note: Batch updates
Let updates be dictionary with:
    "age" as 26
    "status" as "active"
    "last_login" as "2024-01-15"

Let user_data be set_multiple with user_data and updates

Note: Query operations
Let has_email be contains with user_data and "email"
Let total_keys be size with user_data
Display "Dictionary has " with message total_keys with message " keys"
```

#### Advanced Dictionary Operations

```runa
Note: Filtering and transformation
Let numeric_data be dictionary with:
    "score1" as 85
    "score2" as 92
    "score3" as 78
    "score4" as 96

Note: Filter by predicate
Process called "is_high_score" that takes score as Integer returns Boolean:
    Return score is greater than 90

Let high_scores be filter_values with numeric_data and is_high_score
Display "High scores: " with message high_scores

Note: Transform values
Process called "add_bonus" that takes score as Integer returns Integer:
    Return score plus 5

Let bonused_scores be map_values with numeric_data and add_bonus
Display "Scores with bonus: " with message bonused_scores

Note: Dictionary set operations
Let dict1 be dictionary with:
    "shared" as 1
    "unique1" as 2

Let dict2 be dictionary with:
    "shared" as 10
    "unique2" as 20

Let common_keys be intersection with dict1 and dict2
Let all_keys be union with dict1 and dict2
Let diff_keys be difference with dict1 and dict2

Display "Common keys: " with message common_keys
Display "All keys combined: " with message all_keys
Display "Keys only in dict1: " with message diff_keys
```

#### Group By and Aggregation

```runa
Note: Group data by category
Let transactions be list containing
    dictionary with: ("amount" as 100.0, "category" as "food"),
    dictionary with: ("amount" as 50.0, "category" as "transport"),
    dictionary with: ("amount" as 200.0, "category" as "food"),
    dictionary with: ("amount" as 75.0, "category" as "transport")

Process called "get_category" that takes transaction as Dictionary returns String:
    Return transaction at "category" as String

Let grouped be group_by with transactions and get_category
Display "Transactions by category: " with message grouped

Note: Count occurrences
Let categories be list containing "food", "transport", "food", "entertainment", "food"

Process called "identity" that takes item as String returns String:
    Return item

Let category_counts be count_by with categories and identity
Display "Category frequency: " with message category_counts
```

### Deque Operations (`deque.runa`)

Double-ended queue providing efficient insertion and removal at both ends, ideal for implementing queues, stacks, and sliding window algorithms.

#### Basic Deque Operations

```runa
Note: Create and manipulate deque
Let task_queue be create_deque()

Note: Add tasks to both ends
Let task_queue be add_to_back with task_queue and "Process payment"
Let task_queue be add_to_back with task_queue and "Send email"
Let task_queue be add_to_front with task_queue and "Critical: Security alert"

Display "Tasks in queue: " with message deque_length with task_queue

Note: Process tasks from both ends
Let (task_queue, urgent_task) be remove_from_front with task_queue
Display "Processing urgent: " with message urgent_task

Let (task_queue, regular_task) be remove_from_back with task_queue
Display "Processing regular: " with message regular_task

Note: Peek without removing
Let next_task be peek_front with task_queue
Display "Next task: " with message next_task
```

#### Sliding Window with Deque

```runa
Note: Implement sliding window for data analysis
Let sensor_readings be list containing 23.5, 24.1, 22.8, 25.2, 23.9, 26.1, 24.7, 23.3

Process called "sliding_window_average" that takes data as List[Float] and window_size as Integer returns List[Float]:
    Let window be create_deque()
    Let averages be list containing
    Let current_sum be 0.0
    
    For each reading in data:
        Note: Add new reading
        Let window be add_to_back with window and reading
        Let current_sum be current_sum plus reading
        
        Note: Remove old readings if window too large
        While deque_length with window is greater than window_size:
            Let (window, old_reading) be remove_from_front with window
            Let current_sum be current_sum minus old_reading
        
        Note: Calculate average if window is full
        If deque_length with window is equal to window_size:
            Let average be current_sum divided by window_size as Float
            Add average to averages
    
    Return averages

Let moving_averages be sliding_window_average with sensor_readings and 3
Display "3-period moving averages: " with message moving_averages
```

#### Bounded Deque with Capacity Management

```runa
Note: Create deque with maximum capacity
Let recent_events be create_deque_with_maxlen with 5

Note: Add events (automatically removes oldest when full)
Let events be list containing "Login", "View page", "Purchase", "Logout", "Login", "View page", "Download", "Logout"

For each event in events:
    Let recent_events be add_to_back with recent_events and event
    Display "Recent events (" with message deque_length with recent_events with message "): " with message recent_events

Note: Check if deque is at capacity
If deque_is_full with recent_events:
    Display "Event buffer is at maximum capacity"
```

### Counter Operations (`counter.runa`)

Frequency counting with advanced statistical analysis, similarity metrics, and mathematical operations.

#### Basic Frequency Counting

```runa
Note: Count word frequency in text
Let text_words be list containing "the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "the", "fox", "is", "quick"

Let word_counter be create_counter_from_list with text_words

Note: Get individual counts
Let the_count be get_count with word_counter and "the"
Let fox_count be get_count with word_counter and "fox"

Display "Word 'the' appears " with message the_count with message " times"
Display "Word 'fox' appears " with message fox_count with message " times"

Note: Get most common words
Let top_3_words be get_most_common with word_counter and 3
Display "Top 3 words: " with message top_3_words

Note: Get complete statistics
Let total_words be get_total_count with word_counter
Let unique_words be get_unique_elements_count with word_counter

Display "Total words: " with message total_words
Display "Unique words: " with message unique_words
```

#### Statistical Analysis

```runa
Note: Advanced statistical analysis of frequencies
Let stats be get_counter_statistics with word_counter

Display "Counter Statistics:"
Display "Mean frequency: " with message stats at "mean_count" as Float
Display "Median frequency: " with message stats at "median_count" as Float
Display "Standard deviation: " with message stats at "count_std_dev" as Float
Display "Entropy: " with message stats at "entropy" as Float
Display "Diversity index: " with message stats at "diversity_index" as Float

Note: Calculate information theoretic measures
Let entropy be calculate_entropy with word_counter
Let normalized_entropy be calculate_normalized_entropy with word_counter

Display "Information entropy: " with message entropy
Display "Normalized entropy: " with message normalized_entropy with message " (0=uniform, 1=maximum diversity)"
```

#### Counter Arithmetic and Similarity

```runa
Note: Mathematical operations on counters
Let document1_words be create_counter_from_list with list containing "machine", "learning", "data", "science", "machine", "learning"
Let document2_words be create_counter_from_list with list containing "deep", "learning", "neural", "networks", "learning", "data"

Note: Counter operations
Let combined_words be add_counters with document1_words and document2_words
Let unique_to_doc1 be subtract_counters with document1_words and document2_words
Let common_words be intersect_counters with document1_words and document2_words

Display "Combined word counts: " with message combined_words
Display "Words unique to document 1: " with message unique_to_doc1
Display "Common words: " with message common_words

Note: Similarity metrics
Let cosine_sim be calculate_cosine_similarity with document1_words and document2_words
Let jaccard_sim be calculate_jaccard_similarity with document1_words and document2_words

Display "Document similarity (cosine): " with message cosine_sim
Display "Document similarity (Jaccard): " with message jaccard_sim
```

### Default Dictionary Operations (`default_dict.runa`)

Dictionary that automatically creates default values for missing keys, essential for avoiding KeyError exceptions and implementing hierarchical data structures.

#### Basic Default Dictionary Usage

```runa
Note: Create default dictionaries with different types
Let student_grades be create_int_default_dict()
Let course_students be create_list_default_dict()
Let user_settings be create_string_default_dict()

Note: Automatic default value creation
Let math_grade be get_from_default_dict with student_grades and "Alice"
Note: Automatically creates 0 for missing student

Let student_grades be set_in_default_dict with student_grades and "Alice" and 95
Let student_grades be set_in_default_dict with student_grades and "Bob" and 87

Let history_students be get_from_default_dict with course_students and "History"
Note: Automatically creates empty list for missing course

Let history_students be append_to_list with course_students and "History" and "Alice"
Let history_students be append_to_list with course_students and "History" and "Charlie"

Display "Student grades: " with message student_grades
Display "History students: " with message get_from_default_dict with course_students and "History"
```

#### Advanced Factory Types and Nested Structures

```runa
Note: Create nested default dictionary for hierarchical data
Let user_activity be create_nested_default_dict with 2

Note: Automatic nested structure creation
Let alice_monday be get_nested_value with user_activity and list containing "Alice", "Monday"
Let alice_monday be set_nested_value with user_activity and list containing "Alice", "Monday" and dictionary with: ("login_count" as 3, "time_spent" as 120.5)

Let bob_tuesday be set_nested_value with user_activity and list containing "Bob", "Tuesday" and dictionary with: ("login_count" as 1, "time_spent" as 45.2)

Display "User activity data: " with message user_activity

Note: Custom factory for complex default values
Let project_tasks be create_default_dict_with_type with "dict"

Note: Automatically creates nested dictionaries
Let frontend_tasks be get_from_default_dict with project_tasks and "Frontend"
Let frontend_tasks be set_in_default_dict with frontend_tasks and "completed" and 5
Let frontend_tasks be set_in_default_dict with frontend_tasks and "pending" and 3

Let backend_tasks be get_from_default_dict with project_tasks and "Backend"
Let backend_tasks be set_in_default_dict with backend_tasks and "completed" and 8
Let backend_tasks be set_in_default_dict with backend_tasks and "pending" and 2

Display "Project tasks by team: " with message project_tasks
```

#### Counter Implementation with Default Dictionary

```runa
Note: Implement frequency counter using default dictionary
Process called "count_elements_with_default_dict" that takes elements as List[String] returns DefaultDict:
    Let counter be create_int_default_dict()
    
    For each element in elements:
        Let counter be increment_counter with counter and element
    
    Return counter

Let word_list be list containing "apple", "banana", "apple", "cherry", "banana", "apple"
Let word_counts be count_elements_with_default_dict with word_list

Display "Word frequencies: " with message word_counts

Note: Statistics and analysis
Let stats be get_default_dict_statistics with word_counts
Display "Counter statistics: " with message stats
```

### Chain Map Operations (`chain_map.runa`)

Hierarchical key lookup across multiple dictionaries, implementing the "chain of responsibility" pattern for configuration management and scope resolution.

#### Configuration Management with Chain Map

```runa
Note: Implement configuration hierarchy
Let system_defaults be dictionary with:
    "debug" as false
    "timeout" as 30
    "max_connections" as 100
    "log_level" as "INFO"

Let user_config be dictionary with:
    "debug" as true
    "timeout" as 60
    "custom_feature" as true

Let runtime_overrides be dictionary with:
    "log_level" as "DEBUG"
    "temp_setting" as "active"

Note: Create chain map with priority order (first has highest priority)
Let config_chain be create_chain_map_from_maps with list containing runtime_overrides, user_config, system_defaults

Note: Lookup values with automatic fallback
Let debug_mode be get_from_chain_map with config_chain and "debug"
Let timeout_value be get_from_chain_map with config_chain and "timeout"
Let log_level be get_from_chain_map with config_chain and "log_level"
Let max_connections be get_from_chain_map with config_chain and "max_connections"

Display "Effective configuration:"
Display "Debug mode: " with message debug_mode with message " (from user config)"
Display "Timeout: " with message timeout_value with message " (from user config)"
Display "Log level: " with message log_level with message " (from runtime overrides)"
Display "Max connections: " with message max_connections with message " (from system defaults)"
```

#### Scope Resolution in Programming Languages

```runa
Note: Simulate variable scope resolution
Let global_scope be dictionary with:
    "version" as "1.0"
    "debug" as false
    "max_users" as 1000

Let function_scope be dictionary with:
    "debug" as true
    "local_var" as "function_value"
    "temp_data" as list containing 1, 2, 3

Let block_scope be dictionary with:
    "temp_data" as list containing 4, 5, 6
    "loop_counter" as 10

Note: Create scope chain (innermost to outermost)
Let scope_chain be create_chain_map_from_maps with list containing block_scope, function_scope, global_scope

Note: Variable resolution follows scope hierarchy
Let debug_value be get_from_chain_map with scope_chain and "debug"
Let version_value be get_from_chain_map with scope_chain and "version"
Let temp_data_value be get_from_chain_map with scope_chain and "temp_data"

Display "Variable resolution:"
Display "debug = " with message debug_value with message " (resolved from function scope)"
Display "version = " with message version_value with message " (resolved from global scope)"
Display "temp_data = " with message temp_data_value with message " (resolved from block scope)"

Note: Check key existence across chain
Let has_local_var be contains_key_in_chain_map with scope_chain and "local_var"
Let has_undefined_var be contains_key_in_chain_map with scope_chain and "undefined_var"

Display "Has 'local_var': " with message has_local_var
Display "Has 'undefined_var': " with message has_undefined_var
```

#### Dynamic Configuration Updates

```runa
Note: Dynamic configuration management
Let base_config be dictionary with:
    "server_port" as 8080
    "database_url" as "localhost:5432"
    "cache_enabled" as true

Let environment_config be dictionary with:
    "server_port" as 3000
    "environment" as "development"

Let runtime_config be dictionary with:

Let config_stack be create_chain_map_from_maps with list containing runtime_config, environment_config, base_config

Note: Add runtime configuration dynamically
Let runtime_config be set with runtime_config and "maintenance_mode" and true
Let runtime_config be set with runtime_config and "cache_enabled" and false

Note: Update chain map with new runtime config
Let config_stack be update_chain_map with config_stack and 0 and runtime_config

Note: Query final configuration
Let final_port be get_from_chain_map with config_stack and "server_port"
let final_cache be get_from_chain_map with config_stack and "cache_enabled"
Let maintenance be get_from_chain_map with config_stack and "maintenance_mode"

Display "Final configuration:"
Display "Server port: " with message final_port with message " (from environment)"
Display "Cache enabled: " with message final_cache with message " (overridden at runtime)"
Display "Maintenance mode: " with message maintenance with message " (added at runtime)"

Note: Configuration analysis
Let total_keys be get_chain_map_size with config_stack
Let all_keys be get_all_keys_from_chain_map with config_stack

Display "Total configuration keys: " with message total_keys
Display "All available keys: " with message all_keys
```

## Core New Collections (Priority Access)

### Priority Queue Operations (`priority_queue.runa`)

Dictionary-based binary heap implementation supporting both min-heap and max-heap operations with O(log n) complexity for insertions and deletions, priority updates, and comprehensive queue management.

#### Key Features
- **Min/Max Heap Support**: Configure as min-heap or max-heap for different priority schemes
- **Priority Updates**: Modify element priorities in O(log n) time with automatic reheapification
- **Statistics Tracking**: Built-in performance monitoring with comparison and operation counts
- **Timestamp Tie-Breaking**: Consistent ordering for equal priorities using insertion timestamps
- **Bulk Operations**: Push/pop multiple elements efficiently with batch processing

#### Basic Usage

```runa
Import "collections/priority_queue" as pq

Note: Create priority queues for different use cases
Let min_pq be pq.create_min_priority_queue()
Let max_pq be pq.create_max_priority_queue()

Note: Push elements with priorities (lower priority = higher urgency for min-heap)
Set min_pq to pq.priority_queue_push with pq as min_pq and value as "urgent_task" and priority as 1.0
Set min_pq to pq.priority_queue_push with pq as min_pq and value as "normal_task" and priority as 5.0
Set min_pq to pq.priority_queue_push with pq as min_pq and value as "low_priority" and priority as 10.0

Note: Peek at highest priority element (doesn't remove)
Let peek_result be pq.priority_queue_peek with pq as min_pq
If peek_result["success"]:
    Display "Next task: " concatenated with peek_result["value"]
    Display "Priority: " concatenated with peek_result["priority"]

Note: Pop highest priority element (removes and returns)
Let pop_result be pq.priority_queue_pop with pq as min_pq
If pop_result["success"]:
    Let task_name be pop_result["value"]
    Set min_pq to pop_result["queue"]
    Display "Processing: " concatenated with task_name
```

#### Advanced Operations

```runa
Note: Update element priority dynamically
Let update_result be pq.priority_queue_update_priority with pq as min_pq and target_value as "normal_task" and new_priority as 0.5
If update_result["success"]:
    Set min_pq to update_result["queue"]
    Display "Updated priority from " concatenated with update_result["old_priority"] concatenated with " to " concatenated with update_result["new_priority"]

Note: Remove specific element by value
Let remove_result be pq.priority_queue_remove_value with pq as min_pq and target_value as "low_priority"
If remove_result["success"]:
    Set min_pq to remove_result["queue"]
    Display "Removed: " concatenated with remove_result["removed_value"]

Note: Get comprehensive statistics
Let stats be pq.priority_queue_statistics with pq as min_pq
Display "Queue size: " concatenated with stats["size"]
Display "Queue height: " concatenated with stats["height"]
Display "Valid heap: " concatenated with stats["is_valid"]
Display "Total comparisons: " concatenated with stats["comparisons_count"]
Display "Average priority: " concatenated with stats["average_priority"]

Note: Bulk operations for efficiency
Let tasks be list containing 
    dictionary with: value as "task1" and priority as 3.0,
    dictionary with: value as "task2" and priority as 1.0,
    dictionary with: value as "task3" and priority as 7.0

Set min_pq to pq.priority_queue_push_multiple with pq as min_pq and items as tasks

Note: Pop multiple elements at once
Let pop_multiple_result be pq.priority_queue_pop_multiple with pq as min_pq and count as 3
Let processed_tasks be pop_multiple_result["items"]
Set min_pq to pop_multiple_result["queue"]

For each task in processed_tasks:
    Display "Processed: " concatenated with task["value"] concatenated with " (priority: " concatenated with task["priority"] concatenated with ")"
```

#### AI Task Scheduling Example

```runa
Import "collections/priority_queue" as pq

Note: Create task scheduler for AI workloads
Let ai_task_queue be pq.create_min_priority_queue()

Note: Add AI tasks with different priorities
Set ai_task_queue to pq.priority_queue_push with pq as ai_task_queue and value as "model_training" and priority as 1.0
Set ai_task_queue to pq.priority_queue_push with pq as ai_task_queue and value as "data_preprocessing" and priority as 2.0
Set ai_task_queue to pq.priority_queue_push with pq as ai_task_queue and value as "model_evaluation" and priority as 3.0
Set ai_task_queue to pq.priority_queue_push with pq as ai_task_queue and value as "hyperparameter_tuning" and priority as 4.0

Note: Process tasks by priority
While not pq.priority_queue_is_empty with pq as ai_task_queue:
    Let task_result be pq.priority_queue_pop with pq as ai_task_queue
    If task_result["success"]:
        Let task_name be task_result["value"]
        Let task_priority be task_result["priority"]
        Set ai_task_queue to task_result["queue"]
        
        Display "Starting: " concatenated with task_name concatenated with " (priority: " concatenated with task_priority concatenated with ")"
        
        Note: Update queue statistics after each task
        Let current_stats be pq.priority_queue_statistics with pq as ai_task_queue
        Display "Remaining tasks: " concatenated with current_stats["size"]
```

### Segment Tree Operations (`segment_tree.runa`)

Range query data structure supporting sum, min, max, GCD, and LCM operations with lazy propagation for efficient range updates and 2D matrix support for advanced applications.

#### Key Features
- **Multiple Operations**: Sum, min, max, GCD, and LCM range queries with O(log n) complexity
- **Lazy Propagation**: Efficient range updates in O(log n) time with deferred computation
- **2D Support**: Matrix range queries and updates for spatial data analysis
- **Tree Validation**: Built-in structure validation and integrity checking
- **Performance Tracking**: Query and update statistics with memory usage estimation

#### Basic Usage

```runa
Import "collections/segment_tree" as seg_tree

Note: Create segment trees for different query types
Let sales_data be list containing 120.5, 180.3, 145.7, 220.1, 195.8, 167.4, 234.6, 201.3
Let sum_tree be seg_tree.create_sum_segment_tree with array as sales_data
Let min_tree be seg_tree.create_min_segment_tree with array as sales_data  
Let max_tree be seg_tree.create_max_segment_tree with array as sales_data

Note: Range queries for business analytics
Let q1_sum be seg_tree.query_range_sum with tree as sum_tree and start_index as 0 and end_index as 2
Display "Q1 Total Sales: $" concatenated with q1_sum["value"] concatenated with "K"

Let monthly_min be seg_tree.query_range_min with tree as min_tree and start_index as 0 and end_index as 7
Display "Lowest monthly sales: $" concatenated with monthly_min["value"] concatenated with "K"

Let monthly_max be seg_tree.query_range_max with tree as max_tree and start_index as 0 and end_index as 7  
Display "Highest monthly sales: $" concatenated with monthly_max["value"] concatenated with "K"

Note: Point updates with automatic tree rebalancing
Let update_result be seg_tree.update_point_in_segment_tree with tree as sum_tree and index as 1 and new_value as 195.5
Set sum_tree to update_result["tree"]
Display "Updated February sales, new tree ready"

Note: Range updates with lazy propagation
Let range_update be seg_tree.update_range_in_segment_tree with tree as sum_tree and range_start as 4 and range_end as 6 and update_value as 10.0
Set sum_tree to range_update["tree"]
Display "Applied 10K bonus to Q3 sales"
```

#### Advanced Operations

```runa
Note: Tree statistics and health monitoring
Let stats be seg_tree.get_segment_tree_statistics with tree as sum_tree
Display "Tree height: " concatenated with stats["tree_height"]
Display "Total nodes: " concatenated with stats["total_nodes"]
Display "Memory usage estimate: " concatenated with stats["memory_usage_estimate"] concatenated with " bytes"
Display "Query count: " concatenated with stats["query_count"]
Display "Update count: " concatenated with stats["update_count"]

Note: Validate tree structure integrity
Let validation be seg_tree.validate_segment_tree with tree as sum_tree
If validation["is_valid"]:
    Display "✅ Tree structure is valid"
Otherwise:
    Display "❌ Tree validation failed:"
    For each error in validation["errors"]:
        Display "  - " concatenated with error

Note: 2D segment tree for matrix operations
Let revenue_matrix be list containing 
    list containing 100.0, 150.0, 120.0,
    list containing 180.0, 200.0, 160.0,
    list containing 140.0, 190.0, 170.0

Let matrix_tree be seg_tree.create_2d_segment_tree with matrix as revenue_matrix and operation_type as "sum"

Note: Query submatrix sums (e.g., regional revenue)
Let region_sum be seg_tree.query_2d_segment_tree with tree_2d as matrix_tree and row_start as 0 and row_end as 1 and col_start as 1 and col_end as 2
Display "NE region revenue: $" concatenated with region_sum["value"] concatenated with "K"

Note: Update 2D point
Let update_2d_result be seg_tree.update_2d_point with tree_2d as matrix_tree and row as 1 and col as 1 and new_value as 250.0
Set matrix_tree to update_2d_result["tree"]
Display "Updated central office revenue"
```

#### Time Series Analysis Example

```runa
Import "collections/segment_tree" as seg_tree

Note: Analyze hourly server response times
Let response_times be list containing 45.2, 52.1, 38.7, 67.3, 44.9, 51.8, 42.3, 58.6, 47.1, 39.4, 53.2, 46.8

Note: Create trees for different metrics
Let avg_tree be seg_tree.create_sum_segment_tree with array as response_times
Let min_tree be seg_tree.create_min_segment_tree with array as response_times
Let max_tree be seg_tree.create_max_segment_tree with array as response_times

Note: Analyze peak hours (9 AM - 12 PM)
Let peak_sum be seg_tree.query_range_sum with tree as avg_tree and start_index as 9 and end_index as 11
Let peak_avg be peak_sum["value"] divided by 3.0
Let peak_min be seg_tree.query_range_min with tree as min_tree and start_index as 9 and end_index as 11
Let peak_max be seg_tree.query_range_max with tree as max_tree and start_index as 9 and end_index as 11

Display "Peak Hours Analysis:"
Display "  Average response time: " concatenated with peak_avg concatenated with "ms"
Display "  Best response time: " concatenated with peak_min["value"] concatenated with "ms"  
Display "  Worst response time: " concatenated with peak_max["value"] concatenated with "ms"

Note: Detect anomalies (response times > 60ms)
For i from 0 to 11:
    Let single_query be seg_tree.query_range_sum with tree as avg_tree and start_index as i and end_index as i
    If single_query["value"] is greater than 60.0:
        Display "⚠️  Anomaly detected at hour " concatenated with i concatenated with ": " concatenated with single_query["value"] concatenated with "ms"
```

### Set Utilities (`set.runa`)

Comprehensive set operations and algorithms with Dictionary-based return types, supporting complete set algebra, advanced transformations, statistical operations, and deep copy functionality for complex data structures.

#### Key Features
- **Complete Set Algebra**: Union, intersection, difference, symmetric difference with optimal algorithms
- **Advanced Transformations**: Map, filter, partition, powerset generation with functional programming patterns
- **Statistical Operations**: Min/max, sum, average, product calculations on numeric sets
- **Deep Copy Support**: Recursive copying of nested data structures and complex objects
- **Dictionary Returns**: All operations return Dictionary with success indicators instead of Optional types

#### Basic Usage

```runa
Import "collections/set" as set_utils

Note: Create and manipulate sets
Let employees be set_utils.from_list with elements as list containing "Alice", "Bob", "Charlie", "Diana"
Let managers be set_utils.from_list with elements as list containing "Bob", "Diana", "Eve", "Frank"
Let empty_set be set_utils.create_empty_set()

Note: Basic set operations
Set employees to set_utils.add with s as employees and value as "Grace"
Set employees to set_utils.remove with s as employees and value as "Charlie" 

Let has_alice be set_utils.contains with s as employees and value as "Alice"
Let employee_count be set_utils.size with s as employees

Display "Has Alice: " concatenated with has_alice
Display "Total employees: " concatenated with employee_count

Note: Set algebra operations
Let all_people be set_utils.union with s1 as employees and s2 as managers
Let employee_managers be set_utils.intersection with s1 as employees and s2 as managers  
Let non_manager_employees be set_utils.difference with s1 as employees and s2 as managers
Let exclusive_roles be set_utils.symmetric_difference with s1 as employees and s2 as managers

Display "All people: " concatenated with set_utils.to_list with s as all_people
Display "Employee-managers: " concatenated with set_utils.to_list with s as employee_managers
Display "Employees only: " concatenated with set_utils.to_list with s as non_manager_employees
Display "Exclusive roles: " concatenated with set_utils.to_list with s as exclusive_roles

Note: Set relationships
Let managers_subset be set_utils.is_subset with s1 as employee_managers and s2 as managers
Let disjoint_check be set_utils.is_disjoint with s1 as non_manager_employees and s2 as managers

Display "Employee-managers are subset of managers: " concatenated with managers_subset
Display "Non-managers disjoint from managers: " concatenated with disjoint_check
```

#### Advanced Operations

```runa
Note: Statistical operations on numeric sets  
Let scores be set_utils.from_list with elements as list containing 85, 92, 78, 96, 88, 91, 84

Let min_result be set_utils.min_element with s as scores
If min_result["found"]:
    Display "Minimum score: " concatenated with min_result["value"]

Let max_result be set_utils.max_element with s as scores  
If max_result["found"]:
    Display "Maximum score: " concatenated with max_result["value"]

Let total_score be set_utils.sum_elements with s as scores
Let average_score be set_utils.average_elements with s as scores
Let score_product be set_utils.product_elements with s as scores

Display "Total points: " concatenated with total_score
Display "Average score: " concatenated with average_score  
Display "Score product: " concatenated with score_product

Note: Set transformations with predicates
Let high_scores be set_utils.filter with s as scores and predicate as score_above_90
Let low_scores be set_utils.filter_not with s as scores and predicate as score_above_90

Note: Partition sets by criteria
Let (passing, failing) be set_utils.partition with s as scores and predicate as score_above_80

Display "High scores (>90): " concatenated with set_utils.to_list with s as high_scores
Display "Low scores (≤90): " concatenated with set_utils.to_list with s as low_scores
Display "Passing (>80): " concatenated with set_utils.to_list with s as passing
Display "Failing (≤80): " concatenated with set_utils.to_list with s as failing

Note: Advanced set generation
Let small_set be set_utils.from_list with elements as list containing "X", "Y"
Let powerset_result be set_utils.powerset with s as small_set
Display "Powerset: " concatenated with powerset_result["powerset"]

Note: Cartesian product
Let letters be set_utils.from_list with elements as list containing "A", "B"  
Let numbers be set_utils.from_list with elements as list containing 1, 2
Let cartesian be set_utils.cartesian_product with s1 as letters and s2 as numbers
Display "Cartesian product: " concatenated with cartesian["product"]
```

#### Data Analysis Example

```runa
Import "collections/set" as set_utils

Note: Analyze customer segments
Let premium_customers be set_utils.from_list with elements as list containing "C001", "C003", "C007", "C012", "C018"
Let active_customers be set_utils.from_list with elements as list containing "C001", "C002", "C005", "C007", "C009", "C015"
Let recent_customers be set_utils.from_list with elements as list containing "C002", "C008", "C012", "C015", "C020"

Note: Customer overlap analysis
Let premium_active be set_utils.intersection with s1 as premium_customers and s2 as active_customers
Let premium_recent be set_utils.intersection with s1 as premium_customers and s2 as recent_customers
Let active_recent be set_utils.intersection with s1 as active_customers and s2 as recent_customers

Let all_customers be set_utils.union with s1 as premium_customers and s2 as active_customers
Set all_customers to set_utils.union with s1 as all_customers and s2 as recent_customers

Display "Customer Analysis:"
Display "  Total unique customers: " concatenated with set_utils.size with s as all_customers
Display "  Premium + Active: " concatenated with set_utils.size with s as premium_active  
Display "  Premium + Recent: " concatenated with set_utils.size with s as premium_recent
Display "  Active + Recent: " concatenated with set_utils.size with s as active_recent

Note: Customer purchase amounts for statistical analysis
Let purchase_amounts be set_utils.from_list with elements as list containing 299.99, 89.50, 449.00, 125.75, 789.25, 199.99

Let stats_summary be dictionary with:
Set stats_summary["min"] to set_utils.min_element with s as purchase_amounts
Set stats_summary["max"] to set_utils.max_element with s as purchase_amounts  
Set stats_summary["total"] to set_utils.sum_elements with s as purchase_amounts
Set stats_summary["average"] to set_utils.average_elements with s as purchase_amounts

Display "Purchase Statistics:"
If stats_summary["min"]["found"]:
    Display "  Minimum purchase: $" concatenated with stats_summary["min"]["value"]
If stats_summary["max"]["found"]:
    Display "  Maximum purchase: $" concatenated with stats_summary["max"]["value"]
Display "  Total revenue: $" concatenated with stats_summary["total"]
Display "  Average purchase: $" concatenated with stats_summary["average"]
```

### Ordered Dictionary Operations (`ordered_dict.runa`)

Dictionary implementation that preserves insertion order with additional operations for order manipulation, bulk processing, advanced access patterns, and filtering/transformation capabilities.

#### Key Features
- **Insertion Order Preservation**: Keys maintain their insertion order across all operations  
- **Order Manipulation**: Move keys to front/end, reverse order, custom reordering
- **Bulk Operations**: Update from other dictionaries and ordered dictionaries with merge strategies
- **Advanced Access**: Pop first/last, get first/last keys and values, ordered iteration
- **Filtering and Transformation**: Map/filter keys and values with functional programming patterns

#### Basic Usage

```runa
Import "collections/ordered_dict" as od

Note: Create ordered dictionary with preserved insertion order
Let user_config be od.create_ordered_dict()

Note: Add elements in specific order (order preserved)
Set user_config to od.set with od as user_config and key as "database_host" and value as "localhost"
Set user_config to od.set with od as user_config and key as "database_port" and value as 5432
Set user_config to od.set with od as user_config and key as "database_name" and value as "app_db"
Set user_config to od.set with od as user_config and key as "max_connections" and value as 100
Set user_config to od.set with od as user_config and key as "timeout" and value as 30

Note: Access elements with order preservation
Let port be od.get with od as user_config and key as "database_port"
Let safe_timeout be od.get_safe with od as user_config and key as "connection_timeout" and default as 60

Display "Database port: " concatenated with port
Display "Timeout setting: " concatenated with safe_timeout

Note: Check order preservation
Let config_keys be od.keys with od as user_config  
Let config_values be od.values with od as user_config
Let config_items be od.items with od as user_config

Display "Configuration keys in order: " concatenated with config_keys
Display "Configuration values in order: " concatenated with config_values

Note: Iterate through ordered pairs
For each pair in config_items:
    Let key_name be pair[0]
    Let key_value be pair[1]
    Display "  " concatenated with key_name concatenated with " = " concatenated with key_value
```

#### Advanced Operations

```runa
Note: Order manipulation for priority configuration
Set user_config to od.move_to_front with od as user_config and key as "max_connections"
Display "Moved max_connections to front"

Set user_config to od.move_to_end with od as user_config and key as "database_host"  
Display "Moved database_host to end"

Note: Current order after manipulations
Let updated_keys be od.keys with od as user_config
Display "New key order: " concatenated with updated_keys

Note: Reverse entire configuration order
Set user_config to od.reverse with od as user_config
Let reversed_keys be od.keys with od as user_config  
Display "Reversed order: " concatenated with reversed_keys

Note: Advanced access operations
Let first_key be od.get_first_key with od as user_config
Let last_key be od.get_last_key with od as user_config
Let first_value be od.get_first_value with od as user_config
Let last_value be od.get_last_value with od as user_config

Display "First configuration: " concatenated with first_key concatenated with " = " concatenated with first_value
Display "Last configuration: " concatenated with last_key concatenated with " = " concatenated with last_value

Note: Pop operations (return tuple of updated dict and popped value)
Let (updated_config, last_popped) be od.pop_last with od as user_config
Display "Removed last item: " concatenated with last_popped

Let (final_config, first_popped) be od.pop_first with od as updated_config  
Display "Removed first item: " concatenated with first_popped
Set user_config to final_config

Note: Bulk operations and merging
Let additional_config be dictionary with:
    "cache_enabled" as true
    "log_level" as "INFO"
    "debug_mode" as false

Set user_config to od.update_from_dict with od as user_config and other as additional_config

Let other_ordered_config be od.create_ordered_dict()
Set other_ordered_config to od.set with od as other_ordered_config and key as "ssl_enabled" and value as true
Set other_ordered_config to od.set with od as other_ordered_config and key as "ssl_port" and value as 443

Set user_config to od.update with od as user_config and other as other_ordered_config
Display "Merged configurations, final key order: " concatenated with od.keys with od as user_config
```

#### Configuration Management Example

```runa
Import "collections/ordered_dict" as od

Note: Multi-environment configuration with order priority
Let production_config be od.create_ordered_dict()

Note: Add configurations in priority order (most critical first)
Set production_config to od.set with od as production_config and key as "security_key" and value as "***REDACTED***"
Set production_config to od.set with od as production_config and key as "database_url" and value as "prod-db.company.com"
Set production_config to od.set with od as production_config and key as "redis_cluster" and value as "prod-redis.company.com"
Set production_config to od.set with od as production_config and key as "api_rate_limit" and value as 1000
Set production_config to od.set with od as production_config and key as "log_retention_days" and value as 90
Set production_config to od.set with od as production_config and key as "backup_schedule" and value as "0 2 * * *"

Note: Apply configurations in order (critical settings first)
Let ordered_keys be od.keys with od as production_config
Display "Applying production configurations in priority order:"

For each config_key in ordered_keys:
    Let config_value be od.get with od as production_config and key as config_key
    Display "  ✓ Setting " concatenated with config_key concatenated with " = " concatenated with config_value
    
    Note: Simulate configuration application with order dependency
                    If config_key is equal to "security_key":
        Display "    → Security layer initialized"
                    Otherwise if config_key is equal to "database_url":
        Display "    → Database connection established"  
                    Otherwise if config_key is equal to "redis_cluster":
        Display "    → Cache layer connected"

Note: Environment-specific overrides
Let staging_overrides be dictionary with:
    "database_url" as "staging-db.company.com" 
    "api_rate_limit" as 500
    "log_retention_days" as 30

Note: Create staging config by copying and overriding
Let staging_config be od.copy with od as production_config
Set staging_config to od.update_from_dict with od as staging_config and other as staging_overrides

Display "\nStaging configuration differences:"
Let prod_keys be od.keys with od as production_config
For each key in prod_keys:
    Let prod_value be od.get with od as production_config and key as key
    Let staging_value be od.get with od as staging_config and key as key
    If prod_value is not equal to staging_value:
        Display "  " concatenated with key concatenated with ": " concatenated with prod_value concatenated with " → " concatenated with staging_value

Note: Configuration filtering and transformation
Let sensitive_keys be od.filter_keys with od as production_config and predicate as key_contains_sensitive_info
Let numeric_configs be od.filter_values with od as production_config and predicate as value_is_numeric

Display "\nFiltered configurations:"
Display "  Sensitive keys: " concatenated with od.keys with od as sensitive_keys
Display "  Numeric configs: " concatenated with od.keys with od as numeric_configs
```

## Advanced Collections

### Bloom Filter Operations (`bloom_filter.runa`)

### Probabilistic Membership Testing

```runa
Note: Create bloom filter for user tracking
Let user_filter be create_bloom_filter with 10000 and 0.01  Note: 10k users, 1% false positive rate

Note: Add users to the filter
Let user_filter be add_to_bloom_filter with user_filter and "user_12345"
Let user_filter be add_to_bloom_filter with user_filter and "user_67890"
Let user_filter be add_to_bloom_filter with user_filter and "user_abcdef"

Note: Test membership (guaranteed no false negatives)
Let is_member be contains_in_bloom_filter with user_filter and "user_12345"
If is_member is true:
    Display "User might be in the system (could be false positive)"

Let not_member be contains_in_bloom_filter with user_filter and "user_xyz"
If not_member is false:
    Display "User definitely not in the system (guaranteed true negative)"

Note: Monitor filter performance
Let stats be get_bloom_filter_stats with user_filter
Display "Filter utilization: " with message stats at "bit_utilization" as Float
Display "Current false positive rate: " with message stats at "current_false_positive_probability" as Float
Display "Elements added: " with message stats at "elements_count" as Integer
```

### Set Operations and Scaling

```runa
Note: Combine bloom filters for dataset union
Let filter_a be create_bloom_filter with 5000 and 0.01
Let filter_b be create_bloom_filter with 5000 and 0.01

Note: Add different data to each filter
For i from 0 to 1000:
    Let element_a be "dataset_a_" concatenated with i as String
    Let filter_a be add_to_bloom_filter with filter_a and element_a

For i from 500 to 1500:
    Let element_b be "dataset_b_" concatenated with i as String
    Let filter_b be add_to_bloom_filter with filter_b and element_b

Note: Union operation (elements from both sets)
Let combined_filter be union_bloom_filters with filter_a and filter_b

Let has_from_a be contains_in_bloom_filter with combined_filter and "dataset_a_100"
Let has_from_b be contains_in_bloom_filter with combined_filter and "dataset_b_1200"
Display "Contains from A: " with message has_from_a
Display "Contains from B: " with message has_from_b

Note: Scaling bloom filter for dynamic growth
Let scaling_filter be create_scaling_bloom_filter with 1000 and 0.01

For i from 0 to 2500:  Note: Exceeds initial capacity
    Let element be "dynamic_item_" concatenated with i as String
    Let scaling_filter be add_to_scaling_bloom_filter with scaling_filter and element

Display "Number of internal filters: " with message length of scaling_filter.filters
```

### Serialization and Persistence

```runa
Note: Export bloom filter for storage
Let binary_data be export_bloom_filter_binary with user_filter

Note: Save to persistent storage (using file I/O)
Process called "save_bloom_filter" that takes filter as BloomFilter and filename as String returns Boolean:
    Let export_data be export_bloom_filter_binary with filter
    
    Try:
        Let write_result be write_binary_file with filename and export_data
        Return true
    Catch error:
        Display "Failed to save bloom filter: " with message error
        Return false

Let save_success be save_bloom_filter with user_filter and "user_filter.bloom"

Note: Load and restore bloom filter
Process called "load_bloom_filter" that takes filename as String and false_positive_rate as Float returns Optional[BloomFilter]:
    Try:
        Let binary_data be read_binary_file with filename
        Let restored_filter be import_bloom_filter_binary with binary_data and false_positive_rate
        Return restored_filter
    Catch error:
        Display "Failed to load bloom filter: " with message error
        Return nothing

Let restored_filter be load_bloom_filter with "user_filter.bloom" and 0.01

If restored_filter is not nothing:
    Let filter be restored_filter as BloomFilter
    Display "Filter restored with " with message filter.elements_count with message " elements"
```

## Trie Operations (`trie.runa`)

### String Storage and Prefix Matching

```runa
Note: Create dictionary with word definitions
Let dictionary be create_trie

Let dictionary be insert_into_trie with dictionary and "algorithm" and "A set of rules for solving computational problems"
Let dictionary be insert_into_trie with dictionary and "algorithmic" and "Relating to or using algorithms"
Let dictionary be insert_into_trie with dictionary and "data" and "Information processed by computers"
Let dictionary be insert_into_trie with dictionary and "database" and "Organized collection of data"  
Let dictionary be insert_into_trie with dictionary and "structure" and "Organization of data elements"

Note: Fast prefix-based search
Let algo_words be get_words_with_prefix with dictionary and "algo"
Display "Words starting with 'algo': " with message algo_words
Note: Output: ["algorithm", "algorithmic"]

Let data_words be get_words_with_prefix with dictionary and "dat"
Display "Words starting with 'dat': " with message data_words
Note: Output: ["data", "database"]

Note: Autocompletion functionality
Let suggestions be get_autocomplete_suggestions with dictionary and "dat" and 5
Display "Autocompletion suggestions for 'dat': " with message suggestions

Note: Retrieve word definitions
Let definition be get_value_from_trie with dictionary and "algorithm"
If definition is not nothing:
    Display "Algorithm: " with message definition as String
```

### Frequency Analysis and Word Statistics

```runa
Note: Track search query frequency
Let search_trie be create_trie

Note: Simulate search queries (same words searched multiple times)
Let search_terms be list containing "python", "java", "python", "javascript", "python", "java", "rust", "go", "python"

For each term in search_terms:
    Let search_trie be insert_into_trie with search_trie and term and nothing

Note: Analyze search popularity
Let frequent_searches be get_most_frequent_words_with_prefix with search_trie and "" and 5

Display "Most popular search terms:"
For each search_data in frequent_searches:
    Let word be search_data at "word" as String
    Let frequency be search_data at "frequency" as Integer
    Display word with message " searched " with message frequency with message " times"

Note: Get individual word frequency
Let python_frequency be get_word_frequency with search_trie and "python"
Display "Python searched " with message python_frequency with message " times"

Note: Analyze trie structure efficiency
Let trie_stats be get_trie_statistics with search_trie
Display "Unique search terms: " with message trie_stats at "unique_words" as Integer
Display "Total searches: " with message trie_stats at "total_insertions" as Integer
Display "Memory efficiency: " with message trie_stats at "memory_efficiency" as Float
Display "Max depth: " with message trie_stats at "max_depth" as Integer
```

### Pattern Analysis and Common Prefixes

```runa
Note: Find common patterns in programming terms
Let programming_terms be create_trie
Let programming_terms be insert_into_trie with programming_terms and "programming" and nothing
Let programming_terms be insert_into_trie with programming_terms and "program" and nothing
Let programming_terms be insert_into_trie with programming_terms and "programmer" and nothing
Let programming_terms be insert_into_trie with programming_terms and "programming_language" and nothing

Note: Find longest common prefix
Let common_prefix be get_longest_common_prefix with programming_terms
Display "Common prefix for programming terms: '" with message common_prefix with message "'"

Note: Count terms with specific patterns
Let program_count be count_words_with_prefix with programming_terms and "program"
Display "Terms starting with 'program': " with message program_count

Note: Get all words sorted alphabetically
Let sorted_terms be get_all_words_sorted with programming_terms
Display "All programming terms (sorted): " with message sorted_terms
```

## LRU Cache Operations (`lru_cache.runa`)

### High-Performance Caching

```runa
Note: Create cache for API responses
Let api_cache be create_lru_cache with 1000  Note: 1000 item capacity

Note: Cache expensive API calls
Process called "get_user_data" that takes user_id as String returns Dictionary[String, Any]:
    Note: Check cache first
    Let cached_data be get_from_lru_cache with api_cache and user_id
    
    If cached_data is not nothing:
        Display "Cache hit for user: " with message user_id
        Return cached_data as Dictionary[String, Any]
    
    Note: Simulate expensive API call
    Let user_data be empty Dictionary[String, Any]
    Set user_data at "id" to user_id
    Set user_data at "name" to "User " concatenated with user_id
    Set user_data at "email" to user_id concatenated with "@example.com"
    Set user_data at "created_at" to current_timestamp
    
    Note: Cache the result
    Let api_cache be put_into_lru_cache with api_cache and user_id and user_data
    
    Display "Cache miss, fetched and stored user: " with message user_id
    Return user_data

Note: Use the cached function
Let user1 be get_user_data with "12345"
Let user2 be get_user_data with "12345"  Note: Cache hit
Let user3 be get_user_data with "67890"  Note: Cache miss

Note: Monitor cache performance
Let cache_stats be get_lru_cache_stats with api_cache
Display "Cache hit rate: " with message cache_stats at "hit_rate" as Float
Display "Cache utilization: " with message cache_stats at "utilization" as Float
Display "Total hits: " with message cache_stats at "hit_count" as Integer
Display "Total misses: " with message cache_stats at "miss_count" as Integer
```

### Advanced Caching Strategies

```runa
Note: Time-based cache with automatic expiration
Let session_cache be create_ttl_lru_cache with 500 and 1800.0  Note: 30 minute TTL

Note: Store user session data
Let session_data be empty Dictionary[String, Any]
Set session_data at "user_id" to 12345
Set session_data at "permissions" to list containing "read", "write", "admin"
Set session_data at "login_time" to current_timestamp
Set session_data at "last_activity" to current_timestamp

Let session_cache be put_into_ttl_lru_cache with session_cache and "session_abc123" and session_data

Note: Retrieve session (automatically checks expiration)
Let retrieved_session be get_from_ttl_lru_cache with session_cache and "session_abc123"

If retrieved_session is not nothing:
    Let session be retrieved_session as Dictionary[String, Any]
    Let user_id be session at "user_id" as Integer
    Display "Valid session for user: " with message user_id
Otherwise:
    Display "Session expired or not found"

Note: Clean expired sessions
Let session_cache be clean_expired_ttl_cache with session_cache

Note: Size-based cache for large objects
Let file_cache be create_size_lru_cache with 1073741824  Note: 1GB memory limit

Note: Cache files with size tracking
Process called "cache_large_file" that takes filename as String and file_data as String and size_bytes as Integer returns Boolean:
    Let file_cache be put_into_size_lru_cache with file_cache and filename and file_data and size_bytes
    Display "Cached file: " with message filename with message " (" with message size_bytes with message " bytes)"
    Return true

Let cache_success1 be cache_large_file with "dataset.csv" and "large,csv,data" and 52428800   Note: 50MB
Let cache_success2 be cache_large_file with "model.pkl" and "serialized,model,data" and 209715200  Note: 200MB
```

### Cache Analysis and Optimization

```runa
Note: Analyze cache usage patterns
Let usage_keys be get_keys_by_usage with api_cache
Display "Most recently used key: " with message first element of usage_keys

Let lru_key be get_lru_key with api_cache
Let mru_key be get_mru_key with api_cache
Display "Least recently used: " with message lru_key
Display "Most recently used: " with message mru_key

Note: Resize cache based on performance
Let current_stats be get_lru_cache_stats with api_cache
Let current_hit_rate be current_stats at "hit_rate" as Float

If current_hit_rate is less than 0.8:
    Display "Hit rate below 80%, increasing cache size"
    Let api_cache be resize_lru_cache with api_cache and api_cache.capacity times 2
    Display "Cache resized to: " with message api_cache.capacity
```

## Segment Tree Operations (`segment_tree.runa`)

### Range Query Optimization

```runa
Note: Analyze sales data with range queries
Let monthly_sales be list containing 120.5, 180.3, 145.7, 220.1, 195.8, 167.4, 234.6, 201.3, 189.7, 156.2, 198.5, 243.1

Note: Create segment tree for sum queries
Let sales_tree be create_segment_tree with monthly_sales and "sum"

Note: Query quarterly totals
Let q1_total be query_segment_tree with sales_tree and 0 and 2   Note: Jan-Mar
Let q2_total be query_segment_tree with sales_tree and 3 and 5   Note: Apr-Jun
Let q3_total be query_segment_tree with sales_tree and 6 and 8   Note: Jul-Sep
Let q4_total be query_segment_tree with sales_tree and 9 and 11  Note: Oct-Dec

Display "Q1 Sales Total: $" with message q1_total with message "K"
Display "Q2 Sales Total: $" with message q2_total with message "K"
Display "Q3 Sales Total: $" with message q3_total with message "K"
Display "Q4 Sales Total: $" with message q4_total with message "K"

Note: Update individual month and recalculate
Let sales_tree be update_point_in_segment_tree with sales_tree and 1 and 195.5  Note: Revised February
Let updated_q1_total be query_segment_tree with sales_tree and 0 and 2
Display "Updated Q1 Total: $" with message updated_q1_total with message "K"
```

### Statistical Analysis with Min/Max Queries

```runa
Note: Temperature monitoring with range statistics
Let daily_temperatures be list containing 72.5, 75.2, 68.9, 81.3, 77.8, 69.4, 83.1, 78.6, 76.3, 74.1, 79.2, 82.4, 71.8, 85.6

Let temp_min_tree be create_segment_tree with daily_temperatures and "min"
Let temp_max_tree be create_segment_tree with daily_temperatures and "max"

Note: Find temperature extremes for different periods
Let week1_min be query_segment_tree with temp_min_tree and 0 and 6
Let week1_max be query_segment_tree with temp_max_tree and 0 and 6

Let week2_min be query_segment_tree with temp_min_tree and 7 and 13
Let week2_max be query_segment_tree with temp_max_tree and 7 and 13

Display "Week 1 temperature range: " with message week1_min with message "°F - " with message week1_max with message "°F"
Display "Week 2 temperature range: " with message week2_min with message "°F - " with message week2_max with message "°F"

Note: Find hottest day
Let hottest_day_temp be query_segment_tree with temp_max_tree and 0 and 13
Display "Hottest temperature recorded: " with message hottest_day_temp with message "°F"

Note: Range updates for calibration adjustment
Let temp_min_tree be update_range_in_segment_tree with temp_min_tree and 0 and 6 and 1.5  Note: Add 1.5°F to first week
```

### Multi-Dimensional Range Queries

```runa
Note: Analyze profit data across regions and time
Let regional_profits be list containing
    list containing 150.0, 180.0, 220.0, 190.0,  Note: Region A quarterly profits
    list containing 200.0, 240.0, 180.0, 210.0,  Note: Region B quarterly profits  
    list containing 170.0, 195.0, 260.0, 230.0,  Note: Region C quarterly profits
    list containing 180.0, 220.0, 200.0, 250.0   Note: Region D quarterly profits

Let profit_2d_tree be create_2d_segment_tree with regional_profits and "sum"

Note: Query profit for specific region-time combinations
Let region_b_h1 be query_2d_segment_tree with profit_2d_tree and 1 and 1 and 0 and 1  Note: Region B, H1
Let all_regions_q3 be query_2d_segment_tree with profit_2d_tree and 0 and 3 and 2 and 2  Note: All regions, Q3

Display "Region B H1 profit: $" with message region_b_h1 with message "K"
Display "All regions Q3 profit: $" with message all_regions_q3 with message "K"

Note: Update specific data point
Let profit_2d_tree be update_2d_point with profit_2d_tree and 2 and 2 with 285.0  Note: Region C, Q3 revised

Let updated_all_q3 be query_2d_segment_tree with profit_2d_tree and 0 and 3 and 2 and 2
Display "Updated all regions Q3 profit: $" with message updated_all_q3 with message "K"
```

## Suffix Array Operations (`suffix_array.runa`)

### Pattern Matching and Text Search

```runa
Note: Analyze document text for patterns
Let document_text be "The quick brown fox jumps over the lazy dog. The fox is quick and the dog is lazy."
Let text_suffix_array be create_suffix_array with document_text

Note: Search for specific patterns
Let fox_matches be search_pattern_in_suffix_array with text_suffix_array and "fox"
Display "Pattern 'fox' found at positions: " with message fox_matches

Let the_matches be search_pattern_in_suffix_array with text_suffix_array and "the"
Display "Pattern 'the' found at positions: " with message the_matches

Note: Count pattern occurrences
Let lazy_count be count_pattern_occurrences with text_suffix_array and "lazy"
Display "Word 'lazy' appears " with message lazy_count with message " times"

Note: Find repeated content
Let repeated_info be find_longest_repeated_substring with text_suffix_array

If repeated_info at "length" as Integer is greater than 0:
    Let repeated_text be repeated_info at "substring" as String
    Let first_pos be repeated_info at "first_occurrence" as Integer
    Let second_pos be repeated_info at "second_occurrence" as Integer
    
    Display "Longest repeated substring: '" with message repeated_text with message "'"
    Display "Found at positions: " with message first_pos with message " and " with message second_pos
```

### Text Comparison and Analysis

```runa
Note: Compare two texts and find commonalities
Let text1 be "Machine learning algorithms process large datasets efficiently"
Let text2 be "Deep learning processes massive datasets using advanced algorithms"

Let common_info be find_longest_common_substring with text1 and text2

If common_info at "length" as Integer is greater than 0:
    Let common_text be common_info at "substring" as String
    Let pos1 be common_info at "position_in_text1" as Integer
    Let pos2 be common_info at "position_in_text2" as Integer
    
    Display "Longest common substring: '" with message common_text with message "'"
    Display "Position in text 1: " with message pos1
    Display "Position in text 2: " with message pos2

Note: Analyze text structure
Let analysis_stats be get_suffix_array_stats with text_suffix_array
Display "Text analysis results:"
Display "Text length: " with message analysis_stats at "text_length" as Integer with message " characters"
Display "Alphabet size: " with message analysis_stats at "alphabet_size" as Integer with message " unique characters"
Display "Average LCP: " with message analysis_stats at "average_lcp" as Float
```

### Advanced Text Processing

```runa
Note: Find all unique substrings
Let unique_substrings be find_all_unique_substrings with text_suffix_array
Display "Number of unique substrings: " with message length of unique_substrings

Note: Extract specific length substrings
Let three_char_substrings be get_substrings_of_length with text_suffix_array and 3
Display "All 3-character substrings found: " with message length of three_char_substrings

Note: Palindrome detection
Let palindromes be find_palindromic_substrings with text_suffix_array
Display "Palindromes found in text:"
For each palindrome_info in palindromes:
    Let palindrome_text be palindrome_info at "substring" as String
    Let start_pos be palindrome_info at "start_position" as Integer
    If length of palindrome_text is greater than 2:  Note: Only show meaningful palindromes
        Display "'" with message palindrome_text with message "' at position " with message start_pos
```

## Disjoint Set Operations (`disjoint_set.runa`)

### Network Connectivity Analysis

```runa
Note: Analyze computer network connectivity
Let network_nodes be create_disjoint_set with 12  Note: 12 network devices

Note: Establish network connections
Let connections be list containing
    list containing 0, 1,   Note: Router to Switch A
    list containing 1, 2,   Note: Switch A to Server 1
    list containing 1, 3,   Note: Switch A to Server 2
    list containing 4, 5,   Note: Switch B to Server 3
    list containing 5, 6,   Note: Server 3 to Server 4
    list containing 7, 8,   Note: Switch C to Server 5
    list containing 8, 9,   Note: Server 5 to Server 6
    list containing 10, 11  Note: Isolated segment

For each connection in connections:
    Let device1 be first element of connection
    Let device2 be second element of connection
    Let connection_result be union_sets with network_nodes and device1 and device2
    
    If connection_result is true:
        Display "Connected devices " with message device1 with message " and " with message device2

Note: Check connectivity between devices
Let devices_0_3_connected be are_connected with network_nodes and 0 and 3
Display "Device 0 and Device 3 connected: " with message devices_0_3_connected

Let devices_0_10_connected be are_connected with network_nodes and 0 and 10
Display "Device 0 and Device 10 connected: " with message devices_0_10_connected

Note: Analyze network segments
Let all_segments be get_all_sets with network_nodes
Display "Network has " with message length of all_segments with message " separate segments:"

For segment_index from 0 to length of all_segments minus 1:
    Let segment be all_segments at segment_index
    Display "Segment " with message segment_index plus 1 with message ": devices " with message segment
```

### Social Network Analysis

```runa
Note: Analyze friend groups in social network
Let social_network be create_disjoint_set with 15  Note: 15 users

Note: Process friendship connections
Let friendships be list containing
    list containing 0, 1, list containing 1, 2, list containing 2, 3,  Note: Friend group 1
    list containing 4, 5, list containing 5, 6,                       Note: Friend group 2
    list containing 7, 8, list containing 8, 9, list containing 9, 10, list containing 10, 11,  Note: Friend group 3
    list containing 12, 13                                             Note: Friend group 4

For each friendship in friendships:
    Let user1 be first element of friendship
    Let user2 be second element of friendship
    Let connection_result be union_sets with social_network and user1 and user2

Note: Analyze friend group sizes
Let group_representatives be get_set_representatives with social_network

Display "Friend group analysis:"
For each representative in group_representatives:
    Let group_size be get_set_size with social_network and representative
    Let group_members be get_set_members with social_network and representative
    Display "Group led by user " with message representative with message ": " with message group_size with message " members"
    Display "  Members: " with message group_members

Note: Check if users are friends (connected)
Let users_connected be are_connected with social_network and 2 and 10
Display "User 2 and User 10 are connected: " with message users_connected

Note: Network statistics
Let network_stats be get_disjoint_set_stats with social_network
Display "Social network statistics:"
Display "Total users: " with message network_stats at "total_elements" as Integer
Display "Number of friend groups: " with message network_stats at "num_sets" as Integer
Display "Connectivity ratio: " with message network_stats at "connectivity_ratio" as Float
Display "Largest group size: " with message network_stats at "largest_set_size" as Integer
```

### Graph Algorithm Applications

```runa
Note: Minimum spanning tree using Union-Find
Process called "find_minimum_spanning_tree" that takes edges as List[List[Any]] returns List[List[Any]]:
    Note: edges format: [[weight, node1, node2], ...]
    Let sorted_edges be sort edges by first element ascending
    Let node_count be 0
    
    Note: Find maximum node number to determine size
    For each edge in edges:
        Let node1 be edge at 1 as Integer
        Let node2 be edge at 2 as Integer
        If node1 is greater than node_count:
            Set node_count to node1
        If node2 is greater than node_count:
            Set node_count to node2
    
    Let mst_edges be empty List[List[Any]]
    Let disjoint_set be create_disjoint_set with node_count plus 1
    let edges_added be 0
    
    For each edge in sorted_edges:
        Let weight be edge at 0 as Float
        Let node1 be edge at 1 as Integer
        Let node2 be edge at 2 as Integer
        
        Note: If nodes not connected, add edge to MST
        If are_connected with disjoint_set and node1 and node2 is false:
            Let connection_result be union_sets with disjoint_set and node1 and node2
            Add edge to mst_edges
            Set edges_added to edges_added plus 1
            
            Note: MST complete when we have n-1 edges
            If edges_added is equal to node_count:
                Break
    
    Return mst_edges

Note: Example graph edges: [weight, node1, node2]
Let graph_edges be list containing
    list containing 4.0, 0, 1,
    list containing 2.0, 0, 2,
    list containing 6.0, 1, 2,
    list containing 3.0, 1, 3,
    list containing 5.0, 2, 3

Let mst be find_minimum_spanning_tree with graph_edges
Display "Minimum Spanning Tree edges:"
For each mst_edge in mst:
    Let weight be mst_edge at 0 as Float
    Let node1 be mst_edge at 1 as Integer
    Let node2 be mst_edge at 2 as Integer
    Display "Edge " with message node1 with message "-" with message node2 with message " (weight: " with message weight with message ")"
```

## Skip List Operations (`skip_list.runa`)

### Sorted Data Management

```runa
Note: Create leaderboard with skip list
Let leaderboard be create_skip_list with 16 and 0.5  Note: Max 16 levels, 50% probability

Note: Add player scores
Let leaderboard be insert_into_skip_list with leaderboard and 1450.0 and "Player_Alpha"
Let leaderboard be insert_into_skip_list with leaderboard and 1250.0 and "Player_Beta"
Let leaderboard be insert_into_skip_list with leaderboard and 1680.0 and "Player_Gamma"
Let leaderboard be insert_into_skip_list with leaderboard and 1120.0 and "Player_Delta"
Let leaderboard be insert_into_skip_list with leaderboard and 1520.0 and "Player_Echo"

Note: Query scores and rankings
Let player_1250 be search_skip_list with leaderboard and 1250.0
If player_1250 is not nothing:
    Display "Player with score 1250: " with message player_1250 as String

Note: Range queries for competitive brackets
Let elite_scores be get_keys_in_range with leaderboard and 1500.0 and 2000.0
Display "Elite players (1500+ scores): " with message elite_scores

Let competitive_scores be get_keys_in_range with leaderboard and 1200.0 and 1500.0
Display "Competitive players (1200-1500 scores): " with message competitive_scores

Note: Count players in different tiers
Let elite_count be count_nodes_in_range with leaderboard and 1500.0 and 2000.0
Let competitive_count be count_nodes_in_range with leaderboard and 1200.0 and 1500.0
Let casual_count be count_nodes_in_range with leaderboard and 0.0 and 1200.0

Display "Player distribution:"
Display "Elite tier (1500+): " with message elite_count with message " players"
Display "Competitive tier (1200-1500): " with message competitive_count with message " players"  
Display "Casual tier (<1200): " with message casual_count with message " players"
```

### Ranking and Positional Operations

```runa
Note: Analyze player rankings
Let target_score be 1450.0
Let player_rank be get_key_rank with leaderboard and target_score
Display "Score " with message target_score with message " is rank: " with message player_rank plus 1

Note: Get players by rank position
Let top_player_score be get_key_by_rank with leaderboard and 0
If top_player_score is not nothing:
    Display "Top player score: " with message top_player_score as Float

Let third_place_score be get_key_by_rank with leaderboard and 2
If third_place_score is not nothing:
    Display "Third place score: " with message third_place_score as Float

Note: Find neighboring scores
Let reference_score be 1400.0
Let predecessor_info be find_predecessor with leaderboard and reference_score
Let successor_info be find_successor with leaderboard and reference_score

If predecessor_info is not nothing:
    Let pred_score be predecessor_info at "key" as Float
    Let pred_player be predecessor_info at "value" as String
    Display "Score below " with message reference_score with message ": " with message pred_score with message " (" with message pred_player with message ")"

If successor_info is not nothing:
    Let succ_score be successor_info at "key" as Float
    Let succ_player be successor_info at "value" as String
    Display "Score above " with message reference_score with message ": " with message succ_score with message " (" with message succ_player with message ")"
```

### Skip List Performance Analysis

```runa
Note: Analyze skip list structure and performance
Let skip_stats be get_skip_list_stats with leaderboard
Display "Skip list performance metrics:"
Display "Total entries: " with message skip_stats at "size" as Integer
Display "Current max level: " with message skip_stats at "current_level" as Integer
Display "Theoretical max level: " with message skip_stats at "max_level" as Integer
Display "Probability factor: " with message skip_stats at "probability" as Float

Note: Level distribution analysis
Let level_distribution be skip_stats at "level_distribution" as List[Integer]
Display "Level distribution:"
For level_index from 0 to length of level_distribution minus 1:
    Let node_count be level_distribution at level_index
    If node_count is greater than 0:
        Display "Level " with message level_index with message ": " with message node_count with message " nodes"

Note: Bulk operations for performance testing
Let bulk_scores be empty List[Dictionary[String, Any]]
For i from 1000 to 1099:
    Let score_entry be empty Dictionary[String, Any]
    Set score_entry at "key" to i as Float
    Set score_entry at "value" to "Player_" concatenated with i as String
    Add score_entry to bulk_scores

Let bulk_leaderboard be create_skip_list with 16 and 0.5
Let bulk_leaderboard be bulk_insert_skip_list with bulk_leaderboard and bulk_scores

Display "Bulk inserted " with message length of bulk_scores with message " entries"
Display "Final leaderboard size: " with message bulk_leaderboard.size
```

## Frozen Set Operations (`frozen_set.runa`)

### Immutable Set with Hashable Properties

```runa
Note: Create immutable configuration sets
Let basic_permissions be create_frozen_set_from_list with list containing "read", "write", "execute"
Let admin_permissions be create_frozen_set_from_list with list containing "read", "write", "execute", "admin", "delete"
Let readonly_permissions be create_frozen_set_from_list with list containing "read"

Note: Use as dictionary keys (frozen sets are hashable)
Let permission_configs be dictionary with:
    frozen_set_hash with basic_permissions as "basic_user_config"
    frozen_set_hash with admin_permissions as "admin_user_config"  
    frozen_set_hash with readonly_permissions as "readonly_config"

Note: Set algebra operations
Let common_perms be frozen_set_intersection with basic_permissions and admin_permissions
Display "Common permissions: " with message frozen_set_to_list with common_perms

Let admin_only be frozen_set_difference with admin_permissions and basic_permissions
Display "Admin-only permissions: " with message frozen_set_to_list with admin_only

Note: Test relationships between permission sets
If frozen_set_is_subset with basic_permissions and admin_permissions:
    Display "Basic permissions are subset of admin permissions"

If frozen_set_is_superset with admin_permissions and readonly_permissions:
    Display "Admin permissions include all readonly permissions"
```

### Configuration Management with Frozen Sets

```runa
Note: Feature flag combinations that cannot be modified
Process called "create_feature_config" that takes enabled_features as List[String] returns Dictionary:
    Let feature_set be create_frozen_set_from_list with enabled_features
    
    Note: Validate incompatible feature combinations
    Let analytics_features be create_frozen_set_from_list with list containing "analytics", "reporting", "metrics"
    Let privacy_features be create_frozen_set_from_list with list containing "privacy_mode", "anonymous_tracking"
    
    Let has_analytics be not frozen_set_is_empty with frozen_set_intersection with feature_set and analytics_features
    Let has_privacy be not frozen_set_is_empty with frozen_set_intersection with feature_set and privacy_features
    
    If has_analytics and has_privacy:
        Display "Warning: Analytics and privacy features may conflict"
    
    Return dictionary with:
        features as feature_set
        config_hash as frozen_set_hash with feature_set
        analytics_enabled as has_analytics
        privacy_enabled as has_privacy

Let config1 be create_feature_config with list containing "analytics", "reporting", "user_tracking"
Let config2 be create_feature_config with list containing "privacy_mode", "minimal_data", "anonymous_tracking"

Note: Compare configurations
If frozen_set_equals with config1["features"] and config2["features"]:
    Display "Configurations are identical"
Otherwise:
    Let common_features be frozen_set_intersection with config1["features"] and config2["features"]
    Display "Common features: " with message frozen_set_size with common_features
```

## Multiset Operations (`multiset.runa`)

### Frequency Analysis and Statistical Operations

```runa
Note: Analyze customer purchase patterns
Let purchase_history be list containing "laptop", "mouse", "laptop", "keyboard", "mouse", "laptop", "monitor", "mouse"
Let purchase_counts be create_multiset_from_list with purchase_history

Note: Get frequency statistics
Let most_popular be multiset_most_common with purchase_counts and 3
Display "Top 3 purchased items:"
For each item_info in most_popular:
    Display item_info["element"] with message ": " with message item_info["count"] with message " purchases"

Let total_purchases be multiset_size with purchase_counts
Let unique_products be multiset_unique_count with purchase_counts
Display "Total purchases: " with message total_purchases
Display "Unique products: " with message unique_products

Note: Statistical analysis
Let stats be multiset_statistics with purchase_counts
Display "Purchase diversity (entropy): " with message stats["entropy"]
Display "Average purchase frequency: " with message stats["average_frequency"]

Note: Mode detection
Let mode_products be multiset_mode with purchase_counts
Display "Most frequently purchased: " with message mode_products
```

### Multiset Arithmetic for Data Analysis

```runa
Note: Compare sales data across quarters
Let q1_sales be create_multiset_from_list with list containing "widget", "gadget", "widget", "tool", "widget", "gadget"
Let q2_sales be create_multiset_from_list with list containing "widget", "tool", "tool", "gadget", "widget", "tool"

Note: Multiset operations
Let combined_sales be multiset_add_multisets with q1_sales and q2_sales
Display "Combined sales across quarters:"
Let combined_list be multiset_to_list with combined_sales
Display combined_list

Let sales_difference be multiset_difference with q2_sales and q1_sales
Display "Q2 vs Q1 sales difference:"
Let diff_elements be multiset_elements with sales_difference
For each product in diff_elements:
    Let diff_count be multiset_count with sales_difference and product
    If diff_count is greater than 0:
        Display product with message ": +" with message diff_count with message " more in Q2"

Note: Market share analysis
Let q1_freq_dist be multiset_frequency_distribution with q1_sales
Let q2_freq_dist be multiset_frequency_distribution with q2_sales

Display "Q1 market share:"
For each product in multiset_elements with q1_sales:
    Display product with message ": " with message q1_freq_dist[product] with message "%"

Display "Q2 market share:"
For each product in multiset_elements with q2_sales:
    Display product with message ": " with message q2_freq_dist[product] with message "%"
```

## Graph Operations (`graph.runa`)

### Network Analysis and Pathfinding

```runa
Note: Create social network graph
Let social_network be create_graph()
Let users be list containing "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"

Note: Add users as nodes
For each user in users:
    Set social_network to graph_add_node with social_network and user

Note: Add friendship connections
Let friendships be list containing
    list containing "Alice", "Bob", 5.0,      Note: Friendship strength
    list containing "Alice", "Charlie", 8.0,
    list containing "Bob", "Diana", 6.0,
    list containing "Charlie", "Diana", 7.0,
    list containing "Diana", "Eve", 9.0,
    list containing "Eve", "Frank", 4.0

For each friendship in friendships:
    Let user1 be friendship[0]
    Let user2 be friendship[1]
    Let strength be friendship[2]
    Set social_network to graph_add_edge with social_network and user1 and user2 and strength

Note: Network analysis
Display "Social network stats:"
Display "Users: " with message graph_node_count with social_network
Display "Friendships: " with message graph_edge_count with social_network

Note: Find paths between users
Let path_result be graph_dijkstra_shortest_path with social_network and "Alice" and "Frank"
If path_result["found"]:
    Display "Shortest friendship path from Alice to Frank:"
    Display "Path: " with message path_result["path"]
    Display "Total connection strength: " with message path_result["distance"]

Note: Community detection
Let communities be graph_find_connected_components with social_network
Display "Friend communities found: " with message length of communities
For i from 0 to length of communities minus 1:
    Display "Community " with message i plus 1 with message ": " with message communities[i]
```

### Advanced Graph Algorithms

```runa
Note: Transportation network optimization
Let transport_network be create_graph()
Let cities be list containing "NYC", "Boston", "Philadelphia", "Washington", "Baltimore"

For each city in cities:
    Set transport_network to graph_add_node with transport_network and city

Note: Add routes with travel times (in hours)
Let routes be list containing
    list containing "NYC", "Boston", 4.5,
    list containing "NYC", "Philadelphia", 2.0,
    list containing "NYC", "Washington", 5.0,
    list containing "Philadelphia", "Washington", 3.5,
    list containing "Washington", "Baltimore", 1.0,
    list containing "Boston", "Philadelphia", 6.0

For each route in routes:
    Set transport_network to graph_add_edge with transport_network and route[0] and route[1] and route[2]

Note: Find minimum spanning tree for infrastructure planning
Let mst_result be graph_minimum_spanning_tree with transport_network
Display "Minimum spanning tree for transport network:"
Display "Total cost: " with message mst_result["total_weight"]
Display "Essential routes:"
For each edge in mst_result["edges"]:
    Display edge["from"] with message " → " with message edge["to"] with message " (" with message edge["weight"] with message " hours)"

Note: Analyze centrality measures
Let centrality_results be graph_calculate_centrality with transport_network
Display "City importance analysis:"
For each city in cities:
    If city in centrality_results:
        Let centrality be centrality_results[city]
        Display city with message " centrality: " with message centrality

Note: Find all paths within distance threshold
Let nearby_cities be graph_find_nodes_within_distance with transport_network and "NYC" and 3.0
Display "Cities within 3 hours of NYC: " with message nearby_cities
```

## Heap Operations (`heap.runa`)

### Priority Queue Management

```runa
Note: Task scheduling with priorities
Let task_scheduler be create_heap()

Note: Add tasks with priorities (lower number = higher priority)
Let tasks be list containing
    list containing "Critical security patch", 1.0,
    list containing "Database backup", 5.0,
    list containing "Update documentation", 8.0,
    list containing "System monitoring", 3.0,
    list containing "User feedback review", 7.0

For each task_info in tasks:
    Let task_name be task_info[0]
    Let priority be task_info[1]
    Set task_scheduler to heap_push with task_scheduler and task_name and priority

Display "Task queue size: " with message heap_size with task_scheduler

Note: Process tasks in priority order
Display "Processing tasks by priority:"
While not heap_is_empty with task_scheduler:
    Let next_task_result be heap_peek with task_scheduler
    Display "Next task: " with message next_task_result["value"] with message " (priority: " with message next_task_result["priority"] with message ")"
    
    Let completed_task be heap_pop with task_scheduler
    Set task_scheduler to completed_task["heap"]
    Display "Completed: " with message completed_task["value"]

Note: Batch task processing
Let batch_tasks be list containing
    dictionary with: ("task" as "Email processing", "priority" as 4.0),
    dictionary with: ("task" as "Log rotation", "priority" as 6.0),
    dictionary with: ("task" as "Cache cleanup", "priority" as 9.0)

For each task_dict in batch_tasks:
    Set task_scheduler to heap_push with task_scheduler and task_dict["task"] and task_dict["priority"]

Let top_3_tasks be heap_peek_multiple with task_scheduler and 3
Display "Top 3 upcoming tasks:"
For each task_preview in top_3_tasks:
    Display task_preview["value"] with message " (priority: " with message task_preview["priority"] with message ")"
```

### Event Scheduling and Time Management

```runa
Note: Event scheduling with timestamps
Let event_scheduler be create_heap()

Note: Add events with timestamps (earlier times have higher priority)
Let current_time be get_current_timestamp()
Let events be list containing
    list containing "Daily standup", current_time plus 3600.0,    Note: 1 hour from now
    list containing "Code review", current_time plus 7200.0,     Note: 2 hours from now
    list containing "Team lunch", current_time plus 14400.0,     Note: 4 hours from now
    list containing "Sprint planning", current_time plus 1800.0,  Note: 30 minutes from now
    list containing "Client demo", current_time plus 10800.0     Note: 3 hours from now

For each event_info in events:
    Let event_name be event_info[0]
    Let event_time be event_info[1]
    Set event_scheduler to heap_push with event_scheduler and event_name and event_time

Note: Process upcoming events
Display "Upcoming events in chronological order:"
Let events_processed be 0
While not heap_is_empty with event_scheduler and events_processed is less than 3:
    Let next_event_result be heap_pop with event_scheduler
    Set event_scheduler to next_event_result["heap"]
    
    Let event_name be next_event_result["value"]
    Let event_time be next_event_result["priority"]
    Let time_until_event be event_time minus current_time
    
    Display event_name with message " in " with message time_until_event divided by 60.0 with message " minutes"
    Set events_processed to events_processed plus 1

Note: Heap statistics and performance
Let heap_stats be heap_statistics with event_scheduler
Display "Event scheduler statistics:"
Display "Remaining events: " with message heap_stats["size"]
Display "Heap depth: " with message heap_stats["depth"]
Display "Memory efficiency: " with message heap_stats["memory_efficiency"]
```

## Enhanced List Operations (`list.runa`)

### Statistical Analysis and Data Processing

```runa
Note: Analyze sales performance data
Let monthly_sales be list containing 120.5, 135.2, 98.7, 156.3, 142.8, 117.9, 164.1, 138.5, 129.3, 151.7, 133.2, 147.8

Note: Basic statistical measures
Let mean_result be mean with monthly_sales
Let median_result be median with monthly_sales
Let std_dev_result be standard_deviation with monthly_sales
Let variance_result be variance with monthly_sales

Display "Sales performance analysis:"
Display "Average monthly sales: $" with message mean_result["value"] with message "K"
Display "Median monthly sales: $" with message median_result["value"] with message "K"
Display "Standard deviation: $" with message std_dev_result["value"] with message "K"
Display "Variance: " with message variance_result["value"]

Note: Find outliers and trends
Let outliers_result be find_outliers with monthly_sales
If outliers_result["success"]:
    Display "Sales outliers detected:"
    For each outlier_info in outliers_result["outliers"]:
        Display "Month " with message outlier_info["index"] plus 1 with message ": $" with message outlier_info["value"] with message "K"

Note: Quartile analysis
Let quartiles_result be quartiles with monthly_sales
If quartiles_result["success"]:
    Display "Sales distribution quartiles:"
    Display "Q1 (25th percentile): $" with message quartiles_result["q1"] with message "K"
    Display "Q2 (50th percentile): $" with message quartiles_result["q2"] with message "K"  
    Display "Q3 (75th percentile): $" with message quartiles_result["q3"] with message "K"
    Display "Interquartile range: $" with message quartiles_result["iqr"] with message "K"
```

### Functional Programming Operations

```runa
Note: Data transformation pipeline
Let customer_scores be list containing 85, 92, 78, 96, 88, 73, 91, 84, 89, 95

Note: Filter high-performing customers
Let high_performers_result be filter with customer_scores and "is_high_score"
If high_performers_result["success"]:
    Display "High-performing customers (90+): " with message high_performers_result["result"]

Note: Transform scores with bonus points
Let bonus_scores_result be map with customer_scores and "add_bonus_points"
If bonus_scores_result["success"]:
    Display "Scores with bonus: " with message bonus_scores_result["result"]

Note: Reduce to total score
Let total_score_result be reduce with customer_scores and "sum_scores" and 0
If total_score_result["success"]:
    Display "Total customer scores: " with message total_score_result["result"]

Note: Partition customers by performance level
Let partition_result be partition with customer_scores and "is_above_average"
If partition_result["success"]:
    Display "Above average performers: " with message partition_result["true_items"]
    Display "Below average performers: " with message partition_result["false_items"]

Note: Group customers into performance tiers
Let grouped_result be group_by with customer_scores and "get_performance_tier"
If grouped_result["success"]:
    Display "Customer performance tiers:"
    For each tier in keys of grouped_result["result"]:
        Let tier_customers be grouped_result["result"][tier]
        Display tier with message ": " with message length of tier_customers with message " customers"
```

### Advanced List Processing

```runa
Note: Batch processing with chunking
Let transaction_data be list containing
For i from 1 to 50:
    Add i multiplied by 10.5 to transaction_data

Let chunk_result be chunk with transaction_data and 10
If chunk_result["success"]:
    Display "Processing " with message length of chunk_result["result"] with message " transaction batches"
    For batch_index from 0 to length of chunk_result["result"] minus 1:
        Let batch be chunk_result["result"][batch_index]
        Let batch_total_result be sum with batch
        If batch_total_result["success"]:
            Display "Batch " with message batch_index plus 1 with message " total: $" with message batch_total_result["result"]

Note: Sliding window analysis
Let time_series_data be list containing 23.1, 24.5, 22.8, 25.2, 23.9, 26.1, 24.7, 23.3, 25.8, 24.2
Let window_result be sliding_window with time_series_data and 3 and "average"

If window_result["success"]:
    Display "3-period moving averages:"
    For i from 0 to length of window_result["result"] minus 1:
        Display "Period " with message i plus 1 with message ": " with message window_result["result"][i]

Note: List flattening for nested data
Let nested_sales_data be list containing
    list containing 100.0, 120.0, 95.0,      Note: Q1 monthly sales
    list containing 135.0, 142.0, 118.0,     Note: Q2 monthly sales
    list containing 156.0, 163.0, 149.0      Note: Q3 monthly sales

Let flatten_result be flatten with nested_sales_data
If flatten_result["success"]:
    Let all_monthly_sales be flatten_result["result"]
    Display "All monthly sales flattened: " with message length of all_monthly_sales with message " months"
    
    Let annual_total_result be sum with all_monthly_sales
    If annual_total_result["success"]:
        Display "Annual sales total: $" with message annual_total_result["result"] with message "K"

Note: Frequency analysis with list
Let product_categories be list containing "electronics", "clothing", "books", "electronics", "home", "clothing", "electronics", "books", "electronics"
Let frequency_result be frequency_count with product_categories
If frequency_result["success"]:
    Display "Product category frequency:"
    For each category in keys of frequency_result["result"]:
        Display category with message ": " with message frequency_result["result"][category] with message " items"
```

## Skip List Operations (`skip_list.runa`)

### Probabilistic Balanced Tree with Ordered Operations

Skip lists provide O(log n) expected time complexity for search, insertion, and deletion while maintaining sorted order through probabilistic balancing.

#### Basic Skip List Operations

```runa
Note: Create and configure skip list
Let create_result be create_skip_list with max_level as 16 and probability as 0.5
Assert create_result["success"] equals true
Let skip_list be create_result["skip_list"]

Note: Insert key-value pairs
Let insert_result be skip_list_insert with skip_list as skip_list and key as 10.5 and value as "Product A"
Set skip_list to insert_result["skip_list"]
Let insert_result be skip_list_insert with skip_list as skip_list and key as 5.2 and value as "Product B"
Set skip_list to insert_result["skip_list"]
Let insert_result be skip_list_insert with skip_list as skip_list and key as 15.8 and value as "Product C"
Set skip_list to insert_result["skip_list"]

Note: Search operations
Let search_result be skip_list_search with skip_list as skip_list and key as 10.5
If search_result["found"]:
    Display "Found: " with message search_result["value"]

Note: Range queries
Let range_products be skip_list_get_range with skip_list as skip_list and min_key as 5.0 and max_key as 12.0
Display "Products in price range: " with message length of range_products
```

#### Advanced Skip List Operations

```runa
Note: Rank and order operations
Let rank be skip_list_get_rank with skip_list as skip_list and key as 10.5
Display "Product A rank: " with message rank

Let rank_result be skip_list_get_by_rank with skip_list as skip_list and rank as 1
If rank_result["found"]:
    Display "Second cheapest: " with message rank_result["value"]

Note: Predecessor and successor queries
Let predecessor be skip_list_find_predecessor with skip_list as skip_list and key as 12.0
If predecessor["found"]:
    Display "Product before $12.00: " with message predecessor["value"]

Let successor be skip_list_find_successor with skip_list as skip_list and key as 12.0
If successor["found"]:
    Display "Product after $12.00: " with message successor["value"]

Note: Bulk operations and statistics
Let bulk_pairs be list containing
Add dictionary with "key" as 20.0 and "value" as "Product D" to bulk_pairs
Add dictionary with "key" as 25.5 and "value" as "Product E" to bulk_pairs
Let bulk_result be skip_list_bulk_insert with skip_list as skip_list and pairs as bulk_pairs

Let stats be skip_list_statistics with skip_list as skip_list
Display "Skip list efficiency - Level distribution: " with message stats["level_distribution"]
Display "Total comparisons: " with message stats["comparisons_count"]
```

## Sparse Array Operations (`sparse_array.runa`)

### Memory-Efficient Multi-Dimensional Arrays

Sparse arrays store only non-zero elements, providing significant memory savings for arrays with many default values.

#### Basic Sparse Array Operations

```runa
Note: Create large sparse matrix for simulation data
Let dimensions be list containing 1000, 1000
Let create_result be create_sparse_array with dimensions as dimensions and default_value as 0.0
Let sparse_matrix be create_result["sparse_array"]

Display "Matrix size: " with message sparse_matrix["total_size"] with message " elements"
Display "Memory efficiency: " with message sparse_matrix["compression_ratio"] with message "%"

Note: Set sparse values for active simulation cells
Let set_result be sparse_array_set with sparse_array as sparse_matrix and indices as list containing 100, 200 and value as 42.5
Set sparse_matrix to set_result["sparse_array"]
Let set_result be sparse_array_set with sparse_array as sparse_matrix and indices as list containing 500, 750 and value as 17.3
Set sparse_matrix to set_result["sparse_array"]
Let set_result be sparse_array_set with sparse_array as sparse_matrix and indices as list containing 999, 999 and value as 99.9
Set sparse_matrix to set_result["sparse_array"]

Note: Efficient access and queries
Let get_result be sparse_array_get with sparse_array as sparse_matrix and indices as list containing 100, 200
Display "Active cell value: " with message get_result["value"]

Let get_result be sparse_array_get with sparse_array as sparse_matrix and indices as list containing 0, 0
Display "Empty cell value: " with message get_result["value"]
```

#### Matrix Operations and Analytics

```runa
Note: Matrix arithmetic operations
Let matrix_a be create_sparse_array with dimensions as list containing 100, 100 and default_value as 0
Set matrix_a to matrix_a["sparse_array"]
Let matrix_b be create_sparse_array with dimensions as list containing 100, 100 and default_value as 0
Set matrix_b to matrix_b["sparse_array"]

Note: Populate matrices with test data
Let set_result be sparse_array_set with sparse_array as matrix_a and indices as list containing 10, 10 and value as 5.0
Set matrix_a to set_result["sparse_array"]
Let set_result be sparse_array_set with sparse_array as matrix_b and indices as list containing 10, 10 and value as 3.0
Set matrix_b to set_result["sparse_array"]

Note: Add matrices
Let sum_result be sparse_array_add with sparse_array1 as matrix_a and sparse_array2 as matrix_b
Let matrix_sum be sum_result["sparse_array"]

Note: Scalar multiplication
Let scaled_result be sparse_array_multiply_scalar with sparse_array as matrix_a and scalar as 2.5
Let scaled_matrix be scaled_result["sparse_array"]

Note: Transpose operation for 2D matrices
Let transpose_result be sparse_array_transpose with sparse_array as matrix_a
Let matrix_t be transpose_result["sparse_array"]

Note: Row and column operations
Let row_result be sparse_array_get_row with sparse_array as matrix_a and row_index as 10
Display "Row 10 data: " with message row_result["row_data"]

Let stats be sparse_array_statistics with sparse_array as matrix_a
Display "Sparsity ratio: " with message stats["sparsity_ratio"] with message "%"
Display "Memory efficiency: " with message stats["memory_efficiency_percent"] with message "%"
```

## Suffix Array Operations (`suffix_array.runa`)

### Advanced String Processing and Pattern Matching

Suffix arrays enable efficient string algorithms with O(log n) pattern search and advanced text analysis capabilities.

#### Basic Suffix Array Operations

```runa
Note: Create suffix array for text analysis
Let document_text be "the quick brown fox jumps over the lazy dog"
Let create_result be create_suffix_array with text as document_text
Assert create_result["success"] equals true
Let suffix_array be create_result["suffix_array"]

Display "Text length: " with message suffix_array["text_length"]
Display "Alphabet size: " with message suffix_array["alphabet_size"]

Note: Pattern searching
Let pattern be "the"
Let search_result be search_pattern_in_suffix_array with suffix_array as suffix_array and pattern as pattern
Display "Pattern '" with message pattern with message "' found " with message search_result["count"] with message " times"
Display "Occurrences at positions: " with message search_result["occurrences"]

Note: Count pattern occurrences
Let quick_count be count_pattern_occurrences with suffix_array as suffix_array and pattern as "quick"
Let fox_count be count_pattern_occurrences with suffix_array as suffix_array and pattern as "fox"
Display "Word frequencies - quick: " with message quick_count with message ", fox: " with message fox_count
```

#### Advanced String Analysis

```runa
Note: Find repeated substrings
Let repeated_result be find_longest_repeated_substring with suffix_array as suffix_array
If repeated_result["success"]:
    Display "Longest repeated substring: '" with message repeated_result["substring"] with message "'"
    Display "First occurrence at: " with message repeated_result["first_occurrence"]
    Display "Second occurrence at: " with message repeated_result["second_occurrence"]

Note: Generate all unique substrings
Let unique_substrings be find_all_unique_substrings with suffix_array as suffix_array
Display "Total unique substrings: " with message length of unique_substrings

Note: Find substrings of specific length
Let three_char_substrings be get_substrings_of_length with suffix_array as suffix_array and target_length as 3
Display "Three-character substrings: " with message length of three_char_substrings

Note: Palindrome detection
Let palindromes be find_palindromic_substrings with suffix_array as suffix_array
Display "Palindromes found: " with message length of palindromes
For each palindrome in palindromes:
    Display "Palindrome: " with message palindrome["substring"] with message " at position " with message palindrome["start_position"]

Note: Bulk pattern search
Let search_patterns be list containing "the", "quick", "brown", "fox", "jumps"
Let bulk_result be suffix_array_bulk_search with suffix_array as suffix_array and patterns as search_patterns
For each pattern in search_patterns:
    Let pattern_result be bulk_result["pattern_results"][pattern]
    Display "Pattern '" with message pattern with message "': " with message pattern_result["count"] with message " occurrences"
```

#### String Comparison and Analysis

```runa
Note: Compare two texts for common substrings
Let text1 be "programming algorithms"
Let text2 be "algorithmic programming"
Let common_result be find_longest_common_substring with text1 as text1 and text2 as text2

If common_result["success"]:
    Display "Longest common substring: '" with message common_result["substring"] with message "'"
    Display "Length: " with message common_result["length"]
    Display "Position in text1: " with message common_result["position_in_text1"]
    Display "Position in text2: " with message common_result["position_in_text2"]

Note: Statistical analysis
Let stats be get_suffix_array_statistics with suffix_array as suffix_array
Display "Average LCP value: " with message stats["average_lcp"]
Display "Maximum LCP value: " with message stats["max_lcp"]
Display "Query count: " with message stats["query_count"]
```

## Tree Operations (`tree.runa`)

### Binary Search Trees and AVL Trees

Comprehensive tree data structures with both basic BST and self-balancing AVL implementations for efficient hierarchical data organization.

#### Binary Search Tree Operations

```runa
Note: Create and populate BST
Let bst be create_empty_bst()
Display "Created BST, type: " with message bst["tree_type"]

Note: Insert values to build tree structure
Let values be list containing 50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45
For each value in values:
    Let insert_result be bst_insert with tree as bst and value as value
    Set bst to insert_result["tree"]

Display "BST size: " with message bst["size"]

Note: Search operations
Let search_result be bst_search with tree as bst and value as 35
If search_result["found"]:
    Display "Found value: " with message search_result["node"]["value"]

Let search_result be bst_search with tree as bst and value as 55
If not search_result["found"]:
    Display "Value 55 not found in tree"

Note: Tree traversals
Let inorder_values be inorder_traversal with root as bst["root"]
Display "Inorder traversal (sorted): " with message inorder_values

Let preorder_values be preorder_traversal with root as bst["root"]
Display "Preorder traversal: " with message preorder_values

Let level_order_result be level_order_traversal with root as bst["root"]
Display "Level order traversal: " with message level_order_result
```

#### AVL Tree Self-Balancing Operations

```runa
Note: Create AVL tree for guaranteed balanced operations
Let avl_tree be create_empty_avl_tree()
Display "Created AVL tree, type: " with message avl_tree["tree_type"]

Note: Insert sequential values (would unbalance BST)
For i from 1 to 15:
    Let insert_result be avl_insert with tree as avl_tree and value as i
    Set avl_tree to insert_result["tree"]

Display "AVL tree size: " with message avl_tree["size"]

Note: Verify balance after insertions
Let is_balanced be is_tree_balanced with root as avl_tree["root"]
Display "Tree is balanced: " with message is_balanced

Note: Delete operations with rebalancing
Let delete_result be avl_delete with tree as avl_tree and value as 8
Set avl_tree to delete_result["tree"]
Display "Deleted value 8, tree still balanced: " with message is_tree_balanced with root as avl_tree["root"]

Note: Advanced tree analysis
Let tree_stats be tree_statistics with tree as avl_tree
Display "Tree depth: " with message tree_stats["depth"]
Display "Leaf nodes: " with message tree_stats["leaf_count"]
Display "Internal nodes: " with message tree_stats["internal_count"]
Display "Total operations - insertions: " with message tree_stats["insertions_count"]
Display "Total operations - deletions: " with message tree_stats["deletions_count"]
```

#### Tree Analysis and Utilities

```runa
Note: Create test tree for analysis
Let analysis_tree be create_empty_bst()
Let test_values be list containing 100, 50, 150, 25, 75, 125, 175
For each value in test_values:
    Let insert_result be bst_insert with tree as analysis_tree and value as value
    Set analysis_tree to insert_result["tree"]

Note: Find specific node types
Let leaf_nodes be get_leaf_nodes with root as analysis_tree["root"]
Display "Leaf node values: " with message leaf_nodes

Let internal_nodes be get_internal_nodes with root as analysis_tree["root"]
Display "Internal node values: " with message internal_nodes

Note: Path finding and tree relationships
Let path_to_75 be get_path_to_node with root as analysis_tree["root"] and target as 75
Display "Path to node 75: " with message path_to_75

Let lca_result be find_lowest_common_ancestor with root as analysis_tree["root"] and value1 as 25 and value2 as 75
If lca_result["found"]:
    Display "LCA of 25 and 75: " with message lca_result["ancestor"]

Note: Range queries and tree validation
Let range_values be tree_range_query with root as analysis_tree["root"] and min_value as 50 and max_value as 150
Display "Values in range [50, 150]: " with message range_values

Let validation_result be tree_validate_bst with root as analysis_tree["root"]
Display "Tree is valid BST: " with message validation_result["is_valid_bst"]

Note: Tree copying and transformation
Let copied_root be tree_copy with root as analysis_tree["root"]
Let mirrored_root be mirror_tree with root as analysis_tree["root"]
Let trees_identical be are_trees_identical with root1 as analysis_tree["root"] and root2 as copied_root
Display "Original and copy are identical: " with message trees_identical
```

## Trie Operations (`trie.runa`)

### Prefix Tree for Efficient String Operations

Tries (prefix trees) provide efficient string storage and retrieval with powerful prefix-based operations for autocompletion and string analysis.

#### Basic Trie Operations

```runa
Note: Create trie for word storage and retrieval
Let word_trie be create_trie()
Display "Created empty trie, size: " with message word_trie["size"]

Note: Insert words with associated values
Let insert_result be trie_insert with trie as word_trie and word as "apple" and value as "A red or green fruit"
Set word_trie to insert_result["trie"]
Let insert_result be trie_insert with trie as word_trie and word as "application" and value as "Software program"
Set word_trie to insert_result["trie"]
Let insert_result be trie_insert with trie as word_trie and word as "apply" and value as "To put into action"
Set word_trie to insert_result["trie"]
Let insert_result be trie_insert with trie as word_trie and word as "apartment" and value as "Living space"
Set word_trie to insert_result["trie"]
Let insert_result be trie_insert with trie as word_trie and word as "banana" and value as "Yellow fruit"
Set word_trie to insert_result["trie"]

Display "Trie size after insertions: " with message word_trie["size"]
Display "Total words inserted: " with message word_trie["total_words"]

Note: Word search operations
Let search_result be trie_search with trie as word_trie and word as "apple"
If search_result["found"]:
    Display "Definition of 'apple': " with message search_result["value"]
    Display "Word frequency: " with message search_result["frequency"]

Let search_result be trie_search with trie as word_trie and word as "orange"
If not search_result["found"]:
    Display "Word 'orange' not found in dictionary"
```

#### Prefix Operations and Autocompletion

```runa
Note: Prefix-based queries
Let prefix_check be trie_starts_with with trie as word_trie and prefix as "app"
If prefix_check["starts_with"]:
    Display "Words starting with 'app': " with message prefix_check["word_count"]

Note: Get all words with specific prefix
Let prefix_words be trie_get_words_with_prefix with trie as word_trie and prefix as "app"
Display "Words with prefix 'app':"
For each word in prefix_words["words"]:
    Display "  - " with message word

Note: Autocompletion suggestions
Let suggestions be trie_get_autocomplete_suggestions with trie as word_trie and partial_word as "ap" and max_suggestions as 3
Display "Autocomplete suggestions for 'ap':"
For each suggestion in suggestions:
    Display "  - " with message suggestion

Note: Count words with prefix
Let app_count be trie_count_words_with_prefix with trie as word_trie and prefix as "app"
Let ban_count be trie_count_words_with_prefix with trie as word_trie and prefix as "ban"
Display "Word counts - 'app': " with message app_count with message ", 'ban': " with message ban_count
```

#### Advanced Trie Operations

```runa
Note: Frequency analysis and word statistics
Let word_frequency be trie_get_word_frequency with trie as word_trie and word as "apple"
Display "Frequency of 'apple': " with message word_frequency

Let frequent_words be trie_get_most_frequent_words_with_prefix with trie as word_trie and prefix as "a" and limit as 3
Display "Most frequent words starting with 'a':"
For each word_data in frequent_words["words"]:
    Display "  - " with message word_data["word"] with message " (frequency: " with message word_data["frequency"] with message ")"

Note: Word length analysis
Let shortest_result be trie_get_shortest_word with trie as word_trie
If shortest_result["found"]:
    Display "Shortest word: '" with message shortest_result["word"] with message "' (length: " with message shortest_result["length"] with message ")"

Let longest_result be trie_get_longest_word with trie as word_trie
If longest_result["found"]:
    Display "Longest word: '" with message longest_result["word"] with message "' (length: " with message longest_result["length"] with message ")"

Note: Pattern matching and filtering
Let pattern_matches be trie_find_words_by_pattern with trie as word_trie and pattern as "a***e" and wildcard_char as "*"
Display "Words matching pattern 'a***e': " with message pattern_matches

Let five_letter_words be trie_get_words_by_length with trie as word_trie and target_length as 5
Display "Five-letter words: " with message five_letter_words

Note: Bulk operations
Let new_words be list containing
Add dictionary with "word" as "application" and "value" as "Updated definition" to new_words
Add dictionary with "word" as "approach" and "value" as "Method or way" to new_words
Add dictionary with "word" as "approve" and "value" as "To consent or agree" to new_words

Let bulk_result be trie_bulk_insert with trie as word_trie and words as new_words
Set word_trie to bulk_result["trie"]
Display "Bulk insert results - inserted: " with message bulk_result["inserted_count"]
```

#### Trie Analysis and Maintenance

```runa
Note: Trie statistics and performance analysis
Let trie_stats be trie_statistics with trie as word_trie
Display "Trie performance metrics:"
Display "  Unique words: " with message trie_stats["unique_words"]
Display "  Node count: " with message trie_stats["node_count"]
Display "  Max depth: " with message trie_stats["max_depth"]
Display "  Memory efficiency: " with message trie_stats["memory_efficiency_percent"] with message "%"
Display "  Alphabet size: " with message trie_stats["alphabet_size"]
Display "  Query count: " with message trie_stats["query_count"]

Note: Word deletion and cleanup
Let delete_result be trie_delete with trie as word_trie and word as "application"
If delete_result["was_deleted"]:
    Display "Deleted word 'application', value was: " with message delete_result["deleted_value"]
    Set word_trie to delete_result["trie"]

Note: Trie compression and optimization
Let compressed_trie be trie_compress with trie as word_trie
Display "Trie compressed successfully"

Note: Trie validation and integrity checking
Let validation_result be trie_validate with trie as word_trie
If validation_result["is_valid"]:
    Display "Trie structure is valid"
    Display "Node count verification: " with message validation_result["node_count"]
Otherwise:
    Display "Trie validation errors:"
    For each error in validation_result["errors"]:
        Display "  - " with message error

Note: Trie copying and merging
Let trie_copy be trie_copy with trie as word_trie
Let other_trie be create_trie()
Let merge_result be trie_merge with trie1 as word_trie and trie2 as other_trie
Display "Trie operations completed successfully"
```

## Integration Examples

### Multi-Structure Data Pipeline

```runa
Note: Create comprehensive data processing pipeline
Process called "process_user_activity_data" that takes activity_log as List[String] returns Dictionary[String, Any]:
    Let results be empty Dictionary[String, Any]
    
    Note: Use bloom filter for duplicate detection
    Let seen_users be create_bloom_filter with 10000 and 0.01
    
    Note: Use trie for activity pattern analysis
    Let activity_patterns be create_trie
    
    Note: Use LRU cache for frequently accessed data
    Let user_cache be create_lru_cache with 1000
    
    Note: Use skip list for activity scoring
    Let activity_scores be create_skip_list with 16 and 0.5
    
    Let unique_users be 0
    Let processed_activities be 0
    
    For each log_entry in activity_log:
        Note: Parse log entry (simplified)
        Let parts be split_string with log_entry and "|"
        Let user_id be parts at 0 as String
        Let activity_type be parts at 1 as String
        Let score be parse_float with parts at 2 as String
        
        Note: Check for duplicate users with bloom filter
        If contains_in_bloom_filter with seen_users and user_id is false:
            Let seen_users be add_to_bloom_filter with seen_users and user_id
            Set unique_users to unique_users plus 1
        
        Note: Track activity patterns with trie
        Let activity_patterns be insert_into_trie with activity_patterns and activity_type and nothing
        
        Note: Cache user data
        Let cached_user be get_from_lru_cache with user_cache and user_id
        If cached_user is nothing:
            Let user_data be empty Dictionary[String, Any]
            Set user_data at "total_score" to score
            Set user_data at "activity_count" to 1
            Let user_cache be put_into_lru_cache with user_cache and user_id and user_data
        Otherwise:
            Let user_data be cached_user as Dictionary[String, Any]
            Set user_data at "total_score" to user_data at "total_score" as Float plus score
            Set user_data at "activity_count" to user_data at "activity_count" as Integer plus 1
            Let user_cache be put_into_lru_cache with user_cache and user_id and user_data
        
        Note: Update activity leaderboard
        Let activity_scores be insert_into_skip_list with activity_scores and score and user_id
        
        Set processed_activities to processed_activities plus 1
    
    Note: Generate analysis report
    Set results at "unique_users" to unique_users
    Set results at "processed_activities" to processed_activities
    Set results at "top_activities" to get_most_frequent_words_with_prefix with activity_patterns and "" and 5
    Set results at "top_scores" to get_keys_in_range with activity_scores and 900.0 and 1000.0
    Set results at "cache_hit_rate" to get_lru_cache_stats with user_cache at "hit_rate" as Float
    
    Return results

Note: Example usage with sample data
Let sample_logs be list containing
    "user123|login|85.5",
    "user456|purchase|120.0",
    "user123|view_product|25.0",
    "user789|login|90.0",
    "user456|logout|10.0"

Let analysis_results be process_user_activity_data with sample_logs
Display "Data processing results:"
Display "Unique users: " with message analysis_results at "unique_users" as Integer
Display "Processed activities: " with message analysis_results at "processed_activities" as Integer
Display "Cache hit rate: " with message analysis_results at "cache_hit_rate" as Float
```

### Real-Time Analytics System

```runa
Note: Build real-time analytics with multiple data structures
Process called "real_time_analytics_system" that takes stream_data as List[Dictionary[String, Any]] returns Dictionary[String, Any]:
    Let analytics be empty Dictionary[String, Any]
    
    Note: Set up data structures for different analytics needs
    Let recent_visitors be create_bloom_filter with 50000 and 0.02    Note: Track unique visitors
    Let search_queries be create_trie                                 Note: Search analytics
    Let page_performance be create_segment_tree with list containing 0.0 and "sum"  Note: Performance metrics
    Let user_sessions be create_lru_cache with 10000                  Note: Session management
    Let trending_content be create_skip_list with 16 and 0.5         Note: Content ranking
    
    Let total_events be 0
    Let unique_visitor_count be 0
    
    For each event in stream_data:
        Let event_type be event at "type" as String
        Let user_id be event at "user_id" as String
        Let timestamp be event at "timestamp" as Float
        
        Note: Track unique visitors
        If contains_in_bloom_filter with recent_visitors and user_id is false:
            Let recent_visitors be add_to_bloom_filter with recent_visitors and user_id
            Set unique_visitor_count to unique_visitor_count plus 1
        
        Note: Process different event types
        If event_type is equal to "search":
            Let query be event at "query" as String
            Let search_queries be insert_into_trie with search_queries and query and nothing
        
        Else if event_type is equal to "page_view":
            Let page_id be event at "page_id" as String
            Let load_time be event at "load_time" as Float
            
            Note: Update performance metrics (would need proper segment tree with dynamic sizing)
            Note: This is simplified for demonstration
            
        Else if event_type is equal to "content_interaction":
            Let content_id be event at "content_id" as String
            Let engagement_score be event at "engagement_score" as Float
            
            Let trending_content be insert_into_skip_list with trending_content and engagement_score and content_id
        
        Note: Manage user sessions
        Let session_data be get_from_lru_cache with user_sessions and user_id
        If session_data is nothing:
            Let new_session be empty Dictionary[String, Any]
            Set new_session at "start_time" to timestamp
            Set new_session at "event_count" to 1
            Let user_sessions be put_into_lru_cache with user_sessions and user_id and new_session
        Otherwise:
            Let session be session_data as Dictionary[String, Any]
            Set session at "event_count" to session at "event_count" as Integer plus 1
            Set session at "last_activity" to timestamp
            Let user_sessions be put_into_lru_cache with user_sessions and user_id and session
        
        Set total_events to total_events plus 1
    
    Note: Generate real-time analytics report
    Set analytics at "total_events" to total_events
    Set analytics at "estimated_unique_visitors" to unique_visitor_count
    Set analytics at "top_searches" to get_most_frequent_words_with_prefix with search_queries and "" and 10
    Set analytics at "trending_content" to get_keys_in_range with trending_content and 80.0 and 100.0
    Set analytics at "active_sessions" to user_sessions.size
    Set analytics at "session_cache_hit_rate" to get_lru_cache_stats with user_sessions at "hit_rate" as Float
    
    Return analytics

Note: Simulate real-time data processing
Let sample_events be list containing
    empty Dictionary[String, Any], 
    empty Dictionary[String, Any],
    empty Dictionary[String, Any]

Set sample_events at 0 at "type" to "search"
Set sample_events at 0 at "user_id" to "user123"
Set sample_events at 0 at "query" to "machine learning"
Set sample_events at 0 at "timestamp" to current_timestamp

Set sample_events at 1 at "type" to "content_interaction"
Set sample_events at 1 at "user_id" to "user456"
Set sample_events at 1 at "content_id" to "article_789"
Set sample_events at 1 at "engagement_score" to 92.5
Set sample_events at 1 at "timestamp" to current_timestamp plus 10.0

Set sample_events at 2 at "type" to "search"
Set sample_events at 2 at "user_id" to "user123"
Set sample_events at 2 at "query" to "data structures"
Set sample_events at 2 at "timestamp" to current_timestamp plus 20.0

Let real_time_results be real_time_analytics_system with sample_events
Display "Real-time analytics:"
Display "Total events processed: " with message real_time_results at "total_events" as Integer
Display "Estimated unique visitors: " with message real_time_results at "estimated_unique_visitors" as Integer
Display "Active sessions: " with message real_time_results at "active_sessions" as Integer
```

## Testing Your Code

The collections module includes comprehensive test coverage for both basic and advanced collections. Run the test suite to verify functionality:

```bash
cd runa/
python -m pytest tests/unit/stdlib/test_collections.runa -v
```

### Basic Collections Test Coverage:
- **Dictionary utilities**: Core operations, filtering, transformations, and set operations
- **Deque operations**: Both ends insertion/removal, bounded deques, and capacity management  
- **Counter analysis**: Frequency counting, statistical measures, and similarity metrics
- **Default dictionary**: Automatic value creation, factory types, and nested structures
- **Chain map**: Configuration hierarchy, scope resolution, and dynamic updates
- **Bloom filter**: Probabilistic membership testing and false positive rate analysis
- **Disjoint set**: Union-find operations, connectivity analysis, and path compression

### Advanced Collections Test Coverage:
- **LRU cache**: Eviction policies, performance monitoring, and O(1) operations
- **Frozen set**: Immutability, hashability, set algebra operations, and configuration management
- **Multiset**: Frequency analysis, statistical operations, mode detection, and arithmetic
- **Graph algorithms**: Pathfinding (BFS, DFS, Dijkstra), MST, centrality, and connectivity analysis
- **Heap operations**: Priority queues, min/max operations, timestamp handling, and batch processing
- **Enhanced list**: Statistical analysis, functional programming, outlier detection, and data processing

### Integration Test Coverage:
- **Cross-collection integration**: Multi-structure data pipelines and real-time analytics
- **Performance characteristics**: Memory usage, time complexity verification, and scaling tests
- **Error handling**: Edge cases, input validation, and graceful failure recovery
- **Production scenarios**: Caching patterns, configuration management, and data analysis workflows

### Running Individual Test Suites:

```bash
# Test basic collections only
python -m pytest tests/unit/stdlib/test_collections.runa::test_dict_basic_operations -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_counter_from_list -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_deque_with_maxlen -v

# Test advanced collections
python -m pytest tests/unit/stdlib/test_collections.runa::test_lru_cache_basic_operations -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_frozen_set_algebra -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_multiset_statistics -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_graph_algorithms -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_heap_priority_ordering -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_list_statistical_operations -v

# Test integration scenarios
python -m pytest tests/unit/stdlib/test_collections.runa::test_collections_integration -v
python -m pytest tests/unit/stdlib/test_collections.runa::test_collections_performance -v

# Run all collections tests with coverage
python -m pytest tests/unit/stdlib/test_collections.runa --cov=src/runa/stdlib/collections -v
```

## Performance Characteristics

### Time Complexity Summary

#### Basic Collections
| Data Structure | Insert | Search | Delete | Update | Special Operations |
|---------------|--------|--------|--------|--------|-------------------|
| Dictionary    | O(1)*  | O(1)*  | O(1)*  | O(1)*  | Merge: O(n), Filter: O(n) |
| Deque        | O(1)   | O(n)   | O(1)   | O(n)   | Peek: O(1), Both ends: O(1) |
| Counter      | O(1)   | O(1)   | O(1)   | O(1)   | Most common: O(n log k) |
| DefaultDict  | O(1)*  | O(1)*  | O(1)*  | O(1)*  | Auto-create: O(1) |
| ChainMap     | O(1)   | O(m)   | O(1)   | O(1)   | Lookup chain: O(m) |
| Bloom Filter | O(k)   | O(k)   | N/A    | N/A    | Union: O(n), False positive rate |
| Disjoint Set | O(α(n))| O(α(n))| N/A    | N/A    | Union: O(α(n)), Path compression |

#### Advanced Collections  
| Data Structure | Insert | Search | Delete | Range Query | Special Operations |
|---------------|--------|--------|--------|-------------|-------------------|
| Trie         | O(m)   | O(m)   | O(m)   | O(m+k)      | Prefix: O(m+k) |
| LRU Cache    | O(1)   | O(1)   | O(1)   | N/A         | Eviction: O(1) |
| Segment Tree | O(log n)| O(log n)| O(log n)| O(log n)    | Update: O(log n) |
| Suffix Array | O(n log n)†| O(log n)| N/A    | O(log n + k)| Build: O(n log n) |
| Skip List   | O(log n)| O(log n)| O(log n)| O(log n + k)| Rank: O(log n) |
| Sparse Array | O(1)   | O(1)   | O(1)   | O(k)        | Matrix ops: O(k), Transpose: O(k) |
| Tree (BST)   | O(log n)| O(log n)| O(log n)| O(log n + k)| Traversal: O(n) |
| Tree (AVL)   | O(log n)| O(log n)| O(log n)| O(log n + k)| Balance: O(log n) |
| Frozen Set  | N/A    | O(1)   | N/A    | N/A         | Hash: O(n), Set ops: O(n) |
| Multiset    | O(1)   | O(1)   | O(1)   | N/A         | Most common: O(n log k) |
| Graph       | O(1)   | O(V+E) | O(1)   | O(V+E)      | Pathfinding: O(V²), MST: O(E log V) |
| Heap        | O(log n)| O(1)‡  | O(log n)| N/A         | Peek: O(1), Build: O(n) |
| Enhanced List| O(1)§  | O(n)   | O(n)   | O(n)        | Stats: O(n), Sort: O(n log n) |

*Average case for hash-based structures; **†Construction time**; **‡Peek only, full search is O(n)**; **§Append only, insert is O(n)**; k = number of hash functions/results; m = string length; n = number of elements; V = vertices; E = edges; α(n) = inverse Ackermann function

### Space Complexity

#### Basic Collections
- **Dictionary**: O(n) where n is number of key-value pairs
- **Deque**: O(n) where n is number of elements
- **Counter**: O(k) where k is number of unique elements
- **DefaultDict**: O(n) where n is number of stored key-value pairs
- **ChainMap**: O(n) where n is total keys across all maps (references only)
- **Bloom Filter**: O(m) where m is bit array size
- **Disjoint Set**: O(n) where n is number of elements

#### Advanced Collections  
- **Trie**: O(ALPHABET_SIZE × N × M) where N is nodes, M is max string length  
- **LRU Cache**: O(n) where n is capacity
- **Segment Tree**: O(4n) for array of size n
- **Suffix Array**: O(n) where n is text length
- **Skip List**: O(n) expected, O(n log n) worst case
- **Sparse Array**: O(k) where k is number of non-zero elements (significant memory savings when k << n)
- **Tree (BST/AVL)**: O(n) where n is number of nodes
- **Frozen Set**: O(n) where n is number of elements (immutable)
- **Multiset**: O(k) where k is number of unique elements
- **Graph**: O(V + E) where V is vertices, E is edges (adjacency list)
- **Heap**: O(n) where n is number of elements
- **Enhanced List**: O(n) where n is number of elements

## Advanced Optimization Techniques

### Memory-Efficient Operations

```runa
Note: Optimize memory usage across collections
Process called "optimize_collection_memory" that takes config as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let optimization_results be empty Dictionary[String, Any]
    
    Note: Use compact disjoint set for large networks
    Let compact_ds be create_compact_disjoint_set with 1000000
    Set optimization_results at "compact_disjoint_set_memory" to 1000000 times 8  Note: Approximate bytes
    
    Note: Configure bloom filter with optimal parameters
    Let expected_elements be config at "expected_elements" as Integer
    Let target_fpr be config at "target_false_positive_rate" as Float
    Let optimal_filter be create_bloom_filter with expected_elements and target_fpr
    
    Let filter_stats be get_bloom_filter_stats with optimal_filter
    Set optimization_results at "bloom_filter_efficiency" to filter_stats at "bit_utilization" as Float
    
    Note: Use TTL cache to prevent memory leaks  
    Let auto_cleanup_cache be create_ttl_lru_cache with 10000 and 3600.0  Note: 1 hour TTL
    Set optimization_results at "cache_auto_cleanup" to true
    
    Return optimization_results

Let memory_config be empty Dictionary[String, Any]
Set memory_config at "expected_elements" to 100000
Set memory_config at "target_false_positive_rate" to 0.001

Let memory_results be optimize_collection_memory with memory_config
Display "Memory optimization applied"
```

### Performance Monitoring and Tuning

```runa
Note: Monitor and tune collection performance
Process called "monitor_collection_performance" that takes collections as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let performance_report be empty Dictionary[String, Any]
    
    Note: Monitor cache performance
    If "cache" is in collections:
        Let cache be collections at "cache" as LRUCache
        Let cache_stats be get_lru_cache_stats with cache
        Let hit_rate be cache_stats at "hit_rate" as Float
        
        Set performance_report at "cache_hit_rate" to hit_rate
        
        If hit_rate is less than 0.8:
            Set performance_report at "cache_recommendation" to "Consider increasing cache size or adjusting TTL"
    
    Note: Monitor bloom filter efficiency
    If "bloom_filter" is in collections:
        Let filter be collections at "bloom_filter" as BloomFilter
        Let filter_stats be get_bloom_filter_stats with filter
        Let utilization be filter_stats at "bit_utilization" as Float
        
        Set performance_report at "bloom_filter_utilization" to utilization
        
        If utilization is greater than 0.7:
            Set performance_report at "bloom_filter_recommendation" to "Filter highly utilized, consider scaling or creating new filter"
    
    Note: Monitor skip list balance
    If "skip_list" is in collections:
        Let skip_list be collections at "skip_list" as SkipList
        Let skip_stats be get_skip_list_stats with skip_list
        Let max_level be skip_stats at "current_level" as Integer
        
        Set performance_report at "skip_list_max_level" to max_level
        
        If max_level is greater than 20:
            Set performance_report at "skip_list_recommendation" to "Consider adjusting probability factor for better balance"
    
    Return performance_report

Note: Example performance monitoring
Let test_collections be empty Dictionary[String, Any]
Set test_collections at "cache" to api_cache
Set test_collections at "bloom_filter" to user_filter
Set test_collections at "skip_list" to leaderboard

Let performance_results be monitor_collection_performance with test_collections
Display "Performance monitoring results:"
For each metric in keys of performance_results:
    Display metric with message ": " with message performance_results at metric
```

## Implementation Status

### ✅ Basic Collections (Completed & Tested)
All basic collections have been implemented with full Runa language compliance and comprehensive test coverage:

- **dict.runa**: 50+ utility functions for enhanced dictionary operations
- **deque.runa**: Complete double-ended queue with bounded capacity support  
- **counter.runa**: Advanced frequency analysis with 30+ statistical functions
- **default_dict.runa**: Automatic value creation with factory pattern support
- **chain_map.runa**: Hierarchical lookup with configuration management features  
- **bloom_filter.runa**: Probabilistic membership with scaling and serialization
- **disjoint_set.runa**: Union-find with path compression and connectivity analysis

### ✅ Advanced Collections (Completed & Tested)
All advanced collections have been implemented with production-ready functionality and comprehensive test coverage:

- **lru_cache.runa**: O(1) cache operations with advanced eviction policies and statistics
- **frozen_set.runa**: Immutable sets with hashable properties for dictionary keys and caching
- **multiset.runa**: Frequency analysis with statistical operations and set arithmetic
- **graph.runa**: 58+ graph algorithms including pathfinding, MST, and centrality analysis
- **heap.runa**: Priority queue with min/max operations and timestamp handling
- **list.runa**: Enhanced list operations with statistical analysis and functional programming

All collections pass comprehensive test suites with 29 individual test functions covering:
- Core functionality and edge cases
- Error handling and input validation  
- Performance characteristics verification
- Statistical analysis and metrics
- Integration patterns and real-world usage
- Cross-collection integration scenarios

### 🚧 Specialized Collections (In Development)
Specialized collections for niche algorithms and advanced scenarios:

- **trie.runa**: Prefix tree operations (documented, implementation in progress)
- **segment_tree.runa**: Range query optimization
- **suffix_array.runa**: Advanced string processing
- **skip_list.runa**: Probabilistic balanced operations

## Conclusion

The Runa Collections module provides both fundamental and advanced data structures with enterprise-grade performance and natural language syntax. The basic collections are production-ready and form a solid foundation for everyday programming tasks, while advanced collections enable sophisticated algorithms and data processing applications.

This comprehensive module demonstrates Runa's capability to deliver both accessible programming constructs and high-performance data structures, maintaining readability and maintainability throughout complex operations.