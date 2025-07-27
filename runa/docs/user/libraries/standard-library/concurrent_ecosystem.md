#Runa Concurrent Programming Ecosystem

##Overview

The Runa Concurrent Programming Ecosystem provides a comprehensive, production-ready suite of concurrent programming primitives built on an actor-based message-passing model. This ecosystem enables developers to build scalable, thread-safe applications using natural language syntax that reads like English.

###Design Philosophy

- **Actor-Based Concurrency**: Message passing as the primary pattern for thread communication
- **Natural Language API**: Functions and operations that read like English descriptions
- **Unified Abstractions**: Hide complexity while preserving power and performance
- **Fail-Safe Defaults**: Explicit opt-in for advanced features with safe defaults
- **Seamless Integration**: All concurrent primitives work together cohesively

###Core Modules

The concurrent ecosystem consists of eight interconnected modules:

1. **[Atomic Operations](#atomic-operations)** (`stdlib/concurrent/atomic`) - Lock-free operations and memory ordering
2. **[Barriers](#barriers)** (`stdlib/concurrent/barriers`) - Thread synchronization points and coordination
3. **[Channels](#channels)** (`stdlib/concurrent/channels`) - Message passing and communication
4. **[Futures](#futures-and-promises)** (`stdlib/concurrent/futures`) - Asynchronous computation and promises
5. **[Locks](#locks-and-mutual-exclusion)** (`stdlib/concurrent/locks`) - Mutual exclusion and critical sections
6. **[Semaphores](#semaphores)** (`stdlib/concurrent/semaphores`) - Resource access control and coordination
7. **[Threads](#thread-management)** (`stdlib/concurrent/threads`) - Thread lifecycle and execution contexts
8. **[Unified Framework](#unified-concurrent-framework)** (`stdlib/concurrent/concurrent`) - Actor model and high-level abstractions

##Getting Started

###Basic Usage

```runa
Import "stdlib/concurrent/concurrent" as concurrent

Note: Create an actor for message processing
Let actor be concurrent.create_actor with behavior as "message_handler"

Note: Send a message to the actor
Let result be concurrent.send_message with:
    recipient as actor
    message as "Hello, Actor!"
    sender_id as None

Note: Create a work pool for parallel tasks
Let pool be concurrent.create_work_pool with:
    size as 4
    pool_type as None

Note: Submit tasks to the pool
Let task_result be concurrent.submit_task with:
    pool as pool
    function_name as "process_data"
    arguments as list containing data_item

Note: Create an async pipeline for data processing
Let pipeline be concurrent.create_async_pipeline
concurrent.add_pipeline_stage with:
    pipeline as pipeline
    stage_function as "validate_data"
    stage_config as None

concurrent.add_pipeline_stage with:
    pipeline as pipeline
    stage_function as "transform_data"
    stage_config as None

Note: Run the pipeline
Let pipeline_result be concurrent.run_async_pipeline with:
    pipeline as pipeline
    input_data as list containing item1, item2, item3
```

###Quick Start Examples

####Example 1: Producer-Consumer with Channels

```runa
Import "stdlib/concurrent/channels" as channels
Import "stdlib/concurrent/threads" as threads

Note: Create a channel for communication
Let message_channel be channels.create_channel with:
    capacity as 100
    overflow_strategy as None

Note: Producer thread function
Process called "producer_function" that takes channel as channels.Channel[String] returns None:
    For i from 1 to 10:
        Let message be "Message " plus i as String
        Let send_result be channels.send_to_channel with:
            channel as channel
            value as message
            timeout as None
        Display "Sent: " plus message
    
    Note: Close channel when done
    channels.close_channel with channel as channel
    Return None

Note: Consumer thread function  
Process called "consumer_function" that takes channel as channels.Channel[String] returns None:
    Let running be true
    While running:
        Let receive_result be channels.receive_from_channel with:
            channel as channel
            timeout as 1.0
        
        Match receive_result:
            When channels.ReceiveSuccess:
                Display "Received: " plus receive_result.value
            When channels.ReceiveClosed:
                Display "Channel closed, stopping consumer"
                Set running to false
            When channels.ReceiveTimeout:
                Display "Timeout waiting for message"
    
    Return None

Note: Create and start threads
Let producer_thread be threads.create_thread with:
    function_name as "producer_function"
    arguments as list containing message_channel
    thread_name as "Producer"

Let consumer_thread be threads.create_thread with:
    function_name as "consumer_function"
    arguments as list containing message_channel
    thread_name as "Consumer"

threads.start_thread with thread as producer_thread
threads.start_thread with thread as consumer_thread

Note: Wait for completion
Let producer_result be threads.join_thread with thread as producer_thread and timeout as None
Let consumer_result be threads.join_thread with thread as consumer_thread and timeout as None
```

####Example 2: Parallel Computation with Work Pool

```runa
Import "stdlib/concurrent/concurrent" as concurrent

Note:Define work function
Process called "compute_square" that takes number as Integer returns Integer:
    Return number times number

Note:Create work pool
Let computation_pool be concurrent.create_work_pool with:
    size as 4
    pool_type as "work_stealing"

Note:Submit parallel tasks
Let task_numbers be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

For each number in task_numbers:
    concurrent.submit_task with:
        pool as computation_pool
        function_name as "compute_square"
        arguments as list containing number

Note:Collect results
Let results be concurrent.collect_results with:
    pool as computation_pool
    max_results as length of task_numbers
    timeout as 10.0

Display "Computed squares: " plus results as String

Note:Shutdown pool
concurrent.shutdown_work_pool with:
    pool as computation_pool
    await_completion as true
    timeout_ms as 5000
```

####Example 3: Async Data Pipeline

```runa
Import "stdlib/concurrent/concurrent" as concurrent

Note:Define pipeline stages
Process called "validate_input" that takes data as String returns String:
    If length of data is less than 3:
        Throw "Input too short: " plus data
    Return data

Process called "transform_data" that takes data as String returns String:
    Return "PROCESSED_" plus data

Process called "save_result" that takes data as String returns String:
    Display "Saving: " plus data
    Return data

Note:Create and configure pipeline
Let data_pipeline be concurrent.create_async_pipeline

concurrent.add_pipeline_stage with:
    pipeline as data_pipeline
    stage_function as "validate_input"
    stage_config as None

concurrent.add_pipeline_stage with:
    pipeline as data_pipeline
    stage_function as "transform_data"
    stage_config as None

concurrent.add_pipeline_stage with:
    pipeline as data_pipeline
    stage_function as "save_result"
    stage_config as None

Note:Process data through pipeline
Let input_data be list containing "hello", "world", "runa", "concurrent"

Let pipeline_result be concurrent.run_async_pipeline with:
    pipeline as data_pipeline
    input_data as input_data

Match pipeline_result:
    When concurrent.ConcurrentSuccess:
        Display "Pipeline completed successfully: " plus pipeline_result.value as String
    When concurrent.ConcurrentException:
        Display "Pipeline failed: " plus pipeline_result.error_message
    When concurrent.ConcurrentTimeout:
        Display "Pipeline timed out after " plus pipeline_result.elapsed_time as String plus " seconds"
```

##Atomic Operations

###Overview

The atomic module provides lock-free programming primitives with memory ordering semantics for high-performance concurrent applications.

###Types

- **AtomicInteger**: Thread-safe integer with atomic operations
- **AtomicFloat**: Thread-safe floating-point with atomic operations  
- **AtomicBoolean**: Thread-safe boolean with atomic operations
- **AtomicReference[T]**: Thread-safe reference with atomic operations

###Memory Ordering

- **relaxed**: No ordering constraints, only atomicity guaranteed
- **acquire**: No reads/writes can be reordered before this operation
- **release**: No reads/writes can be reordered after this operation
- **acq_rel**: Both acquire and release semantics
- **seq_cst**: Sequential consistency (strongest ordering)

###Core Operations

```runa
Import "stdlib/concurrent/atomic" as atomic

Note:Create atomic integers
Let atomic_counter be atomic.create_atomic_integer with:
    initial_value as 0
    ordering as None

Note:Atomic increment
Let old_value be atomic.atomic_fetch_add with:
    atomic_int as atomic_counter
    value as 1
    ordering as None

Note:Compare and swap
Let cas_result be atomic.atomic_compare_and_swap with:
    atomic_int as atomic_counter
    expected as 1
    desired as 10
    ordering as None

Note:Load with specific ordering
Let current_value be atomic.atomic_load with:
    atomic_int as atomic_counter
    ordering as "acquire"

Note:Store with specific ordering
atomic.atomic_store with:
    atomic_int as atomic_counter
    value as 42
    ordering as "release"
```

###Advanced Usage: Lock-Free Data Structures

```runa
Note:Example: Lock-free counter with backoff
Process called "increment_with_backoff" that takes counter as atomic.AtomicInteger and amount as Integer returns Integer:
    Let max_attempts be 100
    Let attempt be 0
    
    While attempt is less than max_attempts:
        Let current be atomic.atomic_load with:
            atomic_int as counter
            ordering as "acquire"
        
        Let new_value be current plus amount
        
        Let cas_result be atomic.atomic_compare_and_swap with:
            atomic_int as counter
            expected as current
            desired as new_value
            ordering as "acq_rel"
        
        Match cas_result:
            When atomic.CASSuccess:
                Return cas_result.old_value
            When atomic.CASFailure:
               Note:Exponential backoff
                Let backoff_time be 2 to the power of (attempt modulo 10)
                atomic.cpu_relax_for_cycles with cycles as backoff_time
                Set attempt to attempt plus 1
    
    Throw "Failed to increment after maximum attempts"
```

##Barriers

###Overview

Barriers provide synchronization points where multiple threads wait for each other before proceeding, essential for parallel algorithms.

###Types

- **Barrier**: Basic synchronization barrier
- **CyclicBarrier**: Reusable barrier with optional barrier action
- **CountDownLatch**: One-time countdown synchronization
- **Phaser**: Advanced multi-phase synchronization

###Core Operations

```runa
Import "stdlib/concurrent/barriers" as barriers
Import "stdlib/concurrent/threads" as threads

Note:Create a barrier for 3 threads
Let sync_barrier be barriers.create_barrier with:
    parties as 3
    barrier_action as None

Note:Worker function that uses barrier
Process called "parallel_worker" that takes worker_id as Integer and barrier as barriers.Barrier returns None:
    Display "Worker " plus worker_id as String plus " starting work"
    
   Note:Simulate work
    threads.sleep_thread with duration_ms as (worker_id times 1000)
    
    Display "Worker " plus worker_id as String plus " finished work, waiting at barrier"
    
   Note:Wait for all workers at barrier
    Let barrier_result be barriers.await_barrier with:
        barrier as barrier
        timeout as None
    
    Match barrier_result:
        When barriers.BarrierSuccess:
            Display "Worker " plus worker_id as String plus " passed barrier"
        When barriers.BarrierBroken:
            Display "Worker " plus worker_id as String plus " barrier was broken"
        When barriers.BarrierTimeout:
            Display "Worker " plus worker_id as String plus " barrier timed out"
    
    Return None

Note:Create and start worker threads
Let worker_threads be list containing

For i from 1 to 3:
    Let worker_thread be threads.create_thread with:
        function_name as "parallel_worker"
        arguments as list containing i, sync_barrier
        thread_name as "Worker-" plus i as String
    
    Add worker_thread to worker_threads
    threads.start_thread with thread as worker_thread

Note:Wait for all workers to complete
For each thread in worker_threads:
    threads.join_thread with thread as thread and timeout as None
```

###Advanced Usage: Phased Computation

```runa
Note:Create phaser for multi-phase algorithm
Let computation_phaser be barriers.create_phaser with:
    initial_parties as 4
    max_phases as 3

Process called "phased_computation" that takes phase_id as Integer and phaser as barriers.Phaser returns None:
    For phase from 0 to 2:
        Display "Worker " plus phase_id as String plus " executing phase " plus phase as String
        
       Note:Simulate phase work
        threads.sleep_thread with duration_ms as 500
        
       Note:Advance to next phase
        Let advance_result be barriers.phaser_advance_and_await with:
            phaser as phaser
            timeout as 10.0
        
        Match advance_result:
            When barriers.PhaserAdvanced:
                Display "Worker " plus phase_id as String plus " advanced to phase " plus advance_result.new_phase as String
            When barriers.PhaserTerminated:
                Display "Worker " plus phase_id as String plus " phaser terminated"
                Return None
    
    Return None
```

##Channels

###Overview

Channels provide message passing communication between threads, supporting various patterns and buffering strategies.

###Types

- **Channel[T]**: General-purpose channel with configurable capacity
- **MPMCChannel[T]**: Multiple-producer, multiple-consumer channel
- **SPSCChannel[T]**: Single-producer, single-consumer high-performance channel
- **BroadcastChannel[T]**: One-to-many broadcast communication
- **PriorityChannel[T]**: Priority-based message ordering

###Core Operations

```runa
Import "stdlib/concurrent/channels" as channels

Note:Create buffered channel
Let message_channel be channels.create_channel with:
    capacity as 10
    overflow_strategy as "block"

Note:Send message (blocking)
Let send_result be channels.send_to_channel with:
    channel as message_channel
    value as "Hello, Channel!"
    timeout as None

Note:Receive message (blocking)
Let receive_result be channels.receive_from_channel with:
    channel as message_channel
    timeout as 5.0

Match receive_result:
    When channels.ReceiveSuccess:
        Display "Received: " plus receive_result.value
    When channels.ReceiveTimeout:
        Display "Receive timed out"
    When channels.ReceiveClosed:
        Display "Channel is closed"

Note:Non-blocking operations
Let try_send_result be channels.try_send_to_channel with:
    channel as message_channel
    value as "Non-blocking message"

Let try_receive_result be channels.try_receive_from_channel with:
    channel as message_channel
```

###Advanced Usage: Priority Channel

```runa
Note:Create priority channel
Let priority_channel be channels.create_priority_channel with:
    capacity as 100
    ordering as "max_heap"

Note:Send messages with priorities
channels.send_priority_message with:
    channel as priority_channel
    value as "Low priority"
    priority as 1
    timeout as None

channels.send_priority_message with:
    channel as priority_channel
    value as "High priority"
    priority as 10
    timeout as None

channels.send_priority_message with:
    channel as priority_channel
    value as "Medium priority"
    priority as 5
    timeout as None

Note:Receive in priority order (will get "High priority" first)
For i from 1 to 3:
    Let result be channels.receive_from_channel with:
        channel as priority_channel
        timeout as 1.0
    
    Match result:
        When channels.ReceiveSuccess:
            Display "Received: " plus result.value plus " (priority order)"
```

###Channel Patterns

####Fan-Out Pattern

```runa
Note:Distribute work to multiple workers
Process called "distribute_work" that takes work_items as List[String] and worker_count as Integer returns None:
    Let work_channel be channels.create_channel with:
        capacity as length of work_items
        overflow_strategy as "block"
    
   Note:Send all work items
    For each item in work_items:
        channels.send_to_channel with:
            channel as work_channel
            value as item
            timeout as None
    
   Note:Close channel to signal no more work
    channels.close_channel with channel as work_channel
    
   Note:Start workers
    Let worker_threads be list containing
    For i from 1 to worker_count:
        Let worker_thread be threads.create_thread with:
            function_name as "process_work_items"
            arguments as list containing work_channel
            thread_name as "Worker-" plus i as String
        
        Add worker_thread to worker_threads
        threads.start_thread with thread as worker_thread
    
   Note:Wait for workers to complete
    For each thread in worker_threads:
        threads.join_thread with thread as thread and timeout as None
    
    Return None

Process called "process_work_items" that takes work_channel as channels.Channel[String] returns None:
    Let running be true
    While running:
        Let result be channels.receive_from_channel with:
            channel as work_channel
            timeout as 1.0
        
        Match result:
            When channels.ReceiveSuccess:
                Display "Processing: " plus result.value
               Note:Simulate work
                threads.sleep_thread with duration_ms as 100
            When channels.ReceiveClosed:
                Display "No more work, worker stopping"
                Set running to false
            When channels.ReceiveTimeout:
                Continue
    
    Return None
```

##Futures and Promises

###Overview

Futures represent values that will be computed asynchronously, while promises allow setting those values from producer threads.

###Types

- **Future[T]**: Asynchronous computation result
- **Promise[T]**: Producer side of a future
- **CompletableFuture[T]**: Manually completable future
- **AsyncTask[T]**: Task wrapper for async execution

###Core Operations

```runa
Import "stdlib/concurrent/futures" as futures
Import "stdlib/concurrent/threads" as threads

Note:Create a promise-future pair
Let promise be futures.create_promise
Let future be futures.promise_get_future with promise as promise

Note:Producer function
Process called "async_computation" that takes promise as futures.Promise[Integer] returns None:
   Note:Simulate computation
    threads.sleep_thread with duration_ms as 2000
    
   Note:Complete the promise
    Let result be futures.promise_set_value with:
        promise as promise
        value as 42
    
    Return None

Note:Start async computation
Let computation_thread be threads.create_thread with:
    function_name as "async_computation"
    arguments as list containing promise
    thread_name as "AsyncComputation"

threads.start_thread with thread as computation_thread

Note:Wait for result
Let future_result be futures.future_get with:
    future as future
    timeout as 5.0

Match future_result:
    When futures.FutureSuccess:
        Display "Computation result: " plus future_result.value as String
    When futures.FutureTimeout:
        Display "Computation timed out"
    When futures.FutureException:
        Display "Computation failed: " plus future_result.error_message
```

###Future Combinators

```runa
Note:Create multiple futures
Let future1 be futures.create_completed_future with value as 10
Let future2 be futures.create_completed_future with value as 20
Let future3 be futures.create_completed_future with value as 30

Note:Combine multiple futures
Let combined_future be futures.combine_futures with:
    futures as list containing future1, future2, future3

Let combined_result be futures.future_get with:
    future as combined_future
    timeout as 1.0

Match combined_result:
    When futures.FutureSuccess:
        Display "Combined results: " plus combined_result.value as String

Note:Map operation on future
Let mapped_future be futures.future_map with:
    future as future1
    function_name as "double_value"

Note:Filter operation on future
Let filtered_future be futures.future_filter with:
    future as future1
    predicate_name as "is_positive"

Note:First completed future
Let any_future be futures.any_of_futures with:
    futures as list containing future1, future2, future3
```

###Async Task Management

```runa
Note:Create async task
Let async_task be futures.create_async_task with:
    function_name as "complex_computation"
    arguments as list containing 100, 200
    priority as 5

Note:Submit task to executor
Let submission_result be futures.submit_async_task with:
    task as async_task
    executor_context as None

Match submission_result:
    When futures.TaskSubmitted:
        Display "Task submitted with ID: " plus submission_result.task_id
    When futures.TaskRejected:
        Display "Task rejected: " plus submission_result.reason

Note:Await task completion
Let task_result be futures.await_async_task with:
    task as async_task
    timeout as 10.0
```

##Locks and Mutual Exclusion

###Overview

Locks provide mutual exclusion for protecting shared resources and critical sections.

###Types

- **Mutex**: Basic mutual exclusion lock
- **ReentrantMutex**: Reentrant mutual exclusion lock
- **ReadWriteLock**: Reader-writer lock for concurrent reads
- **ConditionVariable**: Condition-based thread coordination

###Core Operations

```runa
Import "stdlib/concurrent/locks" as locks
Import "stdlib/concurrent/threads" as threads

Note:Create mutex
Let shared_mutex be locks.create_mutex

Note:Critical section with mutex
Process called "critical_section_work" that takes mutex as locks.Mutex and worker_id as Integer returns None:
    Display "Worker " plus worker_id as String plus " requesting lock"
    
    Let lock_result be locks.mutex_lock with:
        mutex as mutex
        timeout as None
    
    Match lock_result:
        When locks.LockSuccess:
            Display "Worker " plus worker_id as String plus " acquired lock"
            
           Note:Critical section work
            threads.sleep_thread with duration_ms as 1000
            Display "Worker " plus worker_id as String plus " doing critical work"
            
           Note:Release lock
            locks.mutex_unlock with mutex as mutex
            Display "Worker " plus worker_id as String plus " released lock"
        
        When locks.LockTimeout:
            Display "Worker " plus worker_id as String plus " lock timed out"
        
        When locks.LockException:
            Display "Worker " plus worker_id as String plus " lock failed: " plus lock_result.error_message
    
    Return None

Note:Create multiple threads competing for lock
Let lock_threads be list containing
For i from 1 to 3:
    Let lock_thread be threads.create_thread with:
        function_name as "critical_section_work"
        arguments as list containing shared_mutex, i
        thread_name as "LockWorker-" plus i as String
    
    Add lock_thread to lock_threads
    threads.start_thread with thread as lock_thread

Note:Wait for all threads
For each thread in lock_threads:
    threads.join_thread with thread as thread and timeout as None
```

###Read-Write Lock Usage

```runa
Note:Create read-write lock
Let rw_lock be locks.create_read_write_lock

Note:Reader function
Process called "reader_function" that takes rw_lock as locks.ReadWriteLock and reader_id as Integer returns None:
    Display "Reader " plus reader_id as String plus " requesting read lock"
    
    Let read_lock_result be locks.read_lock with:
        rw_lock as rw_lock
        timeout as None
    
    Match read_lock_result:
        When locks.LockSuccess:
            Display "Reader " plus reader_id as String plus " acquired read lock"
            
           Note:Simulate reading
            threads.sleep_thread with duration_ms as 500
            Display "Reader " plus reader_id as String plus " finished reading"
            
            locks.read_unlock with rw_lock as rw_lock
            Display "Reader " plus reader_id as String plus " released read lock"
    
    Return None

Note:Writer function
Process called "writer_function" that takes rw_lock as locks.ReadWriteLock and writer_id as Integer returns None:
    Display "Writer " plus writer_id as String plus " requesting write lock"
    
    Let write_lock_result be locks.write_lock with:
        rw_lock as rw_lock
        timeout as None
    
    Match write_lock_result:
        When locks.LockSuccess:
            Display "Writer " plus writer_id as String plus " acquired write lock"
            
           Note:Simulate writing
            threads.sleep_thread with duration_ms as 1000
            Display "Writer " plus writer_id as String plus " finished writing"
            
            locks.write_unlock with rw_lock as rw_lock
            Display "Writer " plus writer_id as String plus " released write lock"
    
    Return None

Note:Start multiple readers and one writer
For i from 1 to 3:
    Let reader_thread be threads.create_thread with:
        function_name as "reader_function"
        arguments as list containing rw_lock, i
        thread_name as "Reader-" plus i as String
    threads.start_thread with thread as reader_thread

Let writer_thread be threads.create_thread with:
    function_name as "writer_function"
    arguments as list containing rw_lock, 1
    thread_name as "Writer-1"
threads.start_thread with thread as writer_thread
```

###Condition Variables

```runa
Note:Producer-consumer with condition variables
Let shared_data be dictionary containing "items" as list containing, "ready" as false
Let data_mutex be locks.create_mutex
Let data_condition be locks.create_condition_variable with mutex as data_mutex

Process called "producer_with_condition" that takes mutex as locks.Mutex and condition as locks.ConditionVariable and data as Dictionary[String, Any] returns None:
    For i from 1 to 5:
        locks.mutex_lock with mutex as mutex and timeout as None
        
        Add ("Item " plus i as String) to data["items"]
        Set data["ready"] to true
        
        Display "Produced item " plus i as String
        
       Note:Signal waiting consumers
        locks.condition_notify_all with condition as condition
        
        locks.mutex_unlock with mutex as mutex
        
        threads.sleep_thread with duration_ms as 500
    
    Return None

Process called "consumer_with_condition" that takes mutex as locks.Mutex and condition as locks.ConditionVariable and data as Dictionary[String, Any] and consumer_id as Integer returns None:
    Let items_consumed be 0
    
    While items_consumed is less than 3:
        locks.mutex_lock with mutex as mutex and timeout as None
        
       Note:Wait for items to be available
        While not data["ready"] or length of data["items"] is equal to 0:
            Let wait_result be locks.condition_wait with:
                condition as condition
                timeout as 5.0
            
            Match wait_result:
                When locks.ConditionTimeout:
                    Display "Consumer " plus consumer_id as String plus " timed out waiting"
                    locks.mutex_unlock with mutex as mutex
                    Return None
        
       Note:Consume an item
        If length of data["items"] is greater than 0:
            Let item be data["items"][0]
            Set data["items"] to data["items"][1:]
            Set items_consumed to items_consumed plus 1
            
            Display "Consumer " plus consumer_id as String plus " consumed: " plus item
            
            If length of data["items"] is equal to 0:
                Set data["ready"] to false
        
        locks.mutex_unlock with mutex as mutex
    
    Return None
```

##Semaphores

###Overview

Semaphores control access to resources by maintaining a count of available permits.

###Types

- **CountingSemaphore**: General-purpose counting semaphore
- **BinarySemaphore**: Mutex-like binary semaphore (0 or 1 permits)
- **FairSemaphore**: FIFO-ordered semaphore for fair access
- **TimedSemaphore**: Rate-limiting semaphore with time windows

###Core Operations

```runa
Import "stdlib/concurrent/semaphores" as semaphores
Import "stdlib/concurrent/threads" as threads

Note:Create counting semaphore for resource pool
Let resource_semaphore be semaphores.create_counting_semaphore with:
    initial_permits as 3
    max_permits as 5
    fairness_policy as "fair"

Note:Worker function that uses semaphore
Process called "resource_worker" that takes semaphore as semaphores.CountingSemaphore and worker_id as Integer returns None:
    Display "Worker " plus worker_id as String plus " requesting resource"
    
    Let acquire_result be semaphores.semaphore_acquire with:
        semaphore as semaphore
        permits as 1
        timeout as 5.0
    
    Match acquire_result:
        When semaphores.SemaphoreSuccess:
            Display "Worker " plus worker_id as String plus " acquired resource"
            
           Note:Use resource
            threads.sleep_thread with duration_ms as 2000
            Display "Worker " plus worker_id as String plus " finished using resource"
            
           Note:Release resource
            semaphores.semaphore_release with:
                semaphore as semaphore
                permits as 1
            
            Display "Worker " plus worker_id as String plus " released resource"
        
        When semaphores.SemaphoreTimeout:
            Display "Worker " plus worker_id as String plus " timed out waiting for resource"
        
        When semaphores.SemaphoreException:
            Display "Worker " plus worker_id as String plus " semaphore error: " plus acquire_result.error_message
    
    Return None

Note:Create multiple workers competing for resources
For i from 1 to 6:
    Let worker_thread be threads.create_thread with:
        function_name as "resource_worker"
        arguments as list containing resource_semaphore, i
        thread_name as "ResourceWorker-" plus i as String
    
    threads.start_thread with thread as worker_thread
```

###Rate Limiting with Timed Semaphore

```runa
Note:Create timed semaphore for rate limiting (10 permits per second)
Let rate_limiter be semaphores.create_timed_semaphore with:
    permits_per_window as 10
    time_window_ms as 1000
    max_permits as 10

Process called "rate_limited_operation" that takes semaphore as semaphores.TimedSemaphore and operation_id as Integer returns None:
    Let acquire_result be semaphores.timed_semaphore_acquire with:
        semaphore as semaphore
        permits as 1
        timeout as 2.0
    
    Match acquire_result:
        When semaphores.SemaphoreSuccess:
            Display "Operation " plus operation_id as String plus " executed (rate limited)"
           Note:Simulate operation
            threads.sleep_thread with duration_ms as 100
        
        When semaphores.SemaphoreTimeout:
            Display "Operation " plus operation_id as String plus " rate limited (timeout)"
    
    Return None

Note:Rapidly submit operations that will be rate limited
For i from 1 to 20:
    Let operation_thread be threads.create_thread with:
        function_name as "rate_limited_operation"
        arguments as list containing rate_limiter, i
        thread_name as "Operation-" plus i as String
    
    threads.start_thread with thread as operation_thread
    
   Note:Small delay between operations
    threads.sleep_thread with duration_ms as 50
```

##Thread Management

###Overview

The thread module provides comprehensive thread creation, management, and execution context control.

###Types

- **Thread**: Basic thread with lifecycle management
- **ThreadPool**: Fixed-size thread pool for task execution
- **WorkStealingPool**: Work-stealing thread pool for parallel computation
- **ScheduledThreadPool**: Thread pool with scheduling capabilities
- **ThreadLocal[T]**: Thread-local storage

###Core Operations

```runa
Import "stdlib/concurrent/threads" as threads

Note:Create and start a thread
Let my_thread be threads.create_thread with:
    function_name as "my_thread_function"
    arguments as list containing "argument1", 42
    thread_name as "MyWorkerThread"

Note:Set thread properties before starting
threads.set_thread_priority with:
    thread as my_thread
    priority as 7

threads.set_thread_daemon with:
    thread as my_thread
    daemon as false

Note:Start the thread
threads.start_thread with thread as my_thread

Note:Wait for completion
Let join_result be threads.join_thread with:
    thread as my_thread
    timeout as 10.0

Match join_result:
    When threads.ThreadSuccess:
        Display "Thread completed with result: " plus join_result.value as String
    When threads.ThreadTimeout:
        Display "Thread join timed out"
        threads.interrupt_thread with thread as my_thread
    When threads.ThreadException:
        Display "Thread failed: " plus join_result.error_message
```

###Thread Pools

```runa
Note:Create fixed thread pool
Let thread_pool be threads.create_fixed_thread_pool with pool_size as 4

Note:Submit tasks to pool
For i from 1 to 10:
    Let submission_result be threads.submit_to_thread_pool with:
        pool as thread_pool
        function_name as "parallel_task"
        arguments as list containing i
    
    Match submission_result:
        When threads.ExecutionSuccess:
            Display "Task " plus i as String plus " submitted successfully"
        When threads.ExecutionRejected:
            Display "Task " plus i as String plus " rejected: " plus submission_result.reason

Note:Shutdown pool gracefully
Let shutdown_success be threads.shutdown_thread_pool with:
    pool as thread_pool
    await_termination as true
    timeout_ms as 30000

If shutdown_success:
    Display "Thread pool shut down successfully"
Otherwise:
    Display "Thread pool shutdown timed out"
```

###Work-Stealing Pool

```runa
Note:Create work-stealing pool for parallel computation
Let work_stealing_pool be threads.create_work_stealing_pool with parallelism as None Note:Uses CPU count

Note:Submit parallel tasks
For i from 1 to 100:
    threads.submit_to_work_stealing_pool with:
        pool as work_stealing_pool
        function_name as "cpu_intensive_task"
        arguments as list containing i

Note:Shutdown work-stealing pool
threads.shutdown_work_stealing_pool with:
    pool as work_stealing_pool
    await_termination as true
    timeout_ms as 60000
```

###Thread-Local Storage

```runa
Note:Create thread-local storage
Let thread_local_counter be threads.create_thread_local with default_value as 0

Process called "increment_thread_local" that takes local_storage as threads.ThreadLocal[Integer] and worker_id as Integer returns None:
    For i from 1 to 5:
        Let current_value be threads.thread_local_get with thread_local as local_storage
        Let new_value be current_value plus 1
        
        threads.thread_local_set with:
            thread_local as local_storage
            value as new_value
        
        Display "Worker " plus worker_id as String plus " counter: " plus new_value as String
        
        threads.sleep_thread with duration_ms as 100
    
    Return None

Note:Create threads that use thread-local storage
For i from 1 to 3:
    Let tl_thread be threads.create_thread with:
        function_name as "increment_thread_local"
        arguments as list containing thread_local_counter, i
        thread_name as "TLWorker-" plus i as String
    
    threads.start_thread with thread as tl_thread
```

##Unified Concurrent Framework

###Overview

The unified concurrent framework integrates all concurrent primitives into a cohesive, actor-based system.

###Actor Model

```runa
Import "stdlib/concurrent/concurrent" as concurrent

Note:Create actor with specific behavior
Let message_processor be concurrent.create_actor with:
    behavior as "message_processor"
    initial_state as dictionary containing "processed_count" as 0

Note:Send messages to actor
For i from 1 to 5:
    Let send_result be concurrent.send_message with:
        recipient as message_processor
        message as "Process item " plus i as String
        sender_id as "MainThread"
    
    Match send_result:
        When concurrent.ConcurrentSuccess:
            Display "Message " plus i as String plus " sent successfully"

Note:Get actor statistics
Let actor_stats be concurrent.get_actor_statistics with actor as message_processor
Display "Actor processed " plus actor_stats["message_count"] as String plus " messages"

Note:Stop actor
concurrent.stop_actor with actor as message_processor
```

###Supervision Trees

```runa
Note:Create supervisor actor
Let supervisor be concurrent.create_actor with:
    behavior as "supervisor"
    initial_state as dictionary containing "supervised_count" as 0

Note:Create child actors
Let worker1 be concurrent.create_actor with:
    behavior as "worker"
    initial_state as dictionary containing "worker_id" as 1

Let worker2 be concurrent.create_actor with:
    behavior as "worker"
    initial_state as dictionary containing "worker_id" as 2

Note:Establish supervision relationships
concurrent.supervise_actor with:
    supervisor as supervisor
    child as worker1

concurrent.supervise_actor with:
    supervisor as supervisor
    child as worker2

Note:If supervisor stops, all children will be stopped automatically
concurrent.stop_actor with actor as supervisor
```

###Work Pools

```runa
Note:Create work pool for distributed processing
Let processing_pool be concurrent.create_work_pool with:
    size as 8
    pool_type as "work_stealing"

Note:Submit batch of tasks
Let task_data be list containing "task1", "task2", "task3", "task4", "task5"

For each task in task_data:
    concurrent.submit_task with:
        pool as processing_pool
        function_name as "process_task_data"
        arguments as list containing task

Note:Collect all results
Let all_results be concurrent.collect_results with:
    pool as processing_pool
    max_results as length of task_data
    timeout as 30.0

Display "Processed " plus length of all_results as String plus " tasks"

Note:Get pool statistics
Let pool_stats be concurrent.get_work_pool_statistics with pool as processing_pool
Display "Pool throughput: " plus pool_stats["throughput"] as String plus " tasks/second"

Note:Shutdown pool
concurrent.shutdown_work_pool with:
    pool as processing_pool
    await_completion as true
    timeout_ms as 10000
```

###Async Pipelines

```runa
Note:Create multi-stage processing pipeline
Let data_pipeline be concurrent.create_async_pipeline

Note:Add processing stages
concurrent.add_pipeline_stage with:
    pipeline as data_pipeline
    stage_function as "input_validation"
    stage_config as dictionary containing "strict_mode" as true

concurrent.add_pipeline_stage with:
    pipeline as data_pipeline
    stage_function as "data_transformation"
    stage_config as dictionary containing "output_format" as "json"

concurrent.add_pipeline_stage with:
    pipeline as data_pipeline
    stage_function as "output_storage"
    stage_config as dictionary containing "storage_type" as "database"

Note:Process data through pipeline
Let input_dataset be list containing "data1", "data2", "data3", "data4"

Let pipeline_result be concurrent.run_async_pipeline with:
    pipeline as data_pipeline
    input_data as input_dataset

Match pipeline_result:
    When concurrent.ConcurrentSuccess:
        Display "Pipeline processed " plus length of pipeline_result.value as String plus " items"
    When concurrent.ConcurrentException:
        Display "Pipeline failed: " plus pipeline_result.error_message
    When concurrent.ConcurrentTimeout:
        Display "Pipeline timed out after " plus pipeline_result.elapsed_time as String plus " seconds"

Note:Get pipeline statistics
Let pipeline_stats be concurrent.get_pipeline_statistics with pipeline as data_pipeline
Display "Pipeline error rate: " plus pipeline_stats["error_rate"] as String
```

##Best Practices

###General Guidelines

1. **Choose the Right Abstraction**:
   - Use **actors** for isolated, stateful components
   - Use **channels** for message passing between threads
   - Use **futures** for asynchronous computations
   - Use **locks** for protecting shared mutable state
   - Use **semaphores** for resource access control

2. **Avoid Common Pitfalls**:
   - Don't mix locking and message passing in the same code path
   - Always handle timeout cases in concurrent operations
   - Use appropriate buffer sizes for channels
   - Be careful with shared mutable state

3. **Performance Considerations**:
   - Prefer lock-free operations (atomics) for simple counters
   - Use work-stealing pools for CPU-intensive parallel tasks
   - Use fixed thread pools for I/O-bound tasks
   - Consider memory ordering requirements for atomic operations

###Error Handling

```runa
Note:Always handle all possible results
Let channel_result be channels.receive_from_channel with:
    channel as my_channel
    timeout as 5.0

Match channel_result:
    When channels.ReceiveSuccess:
       Note:Handle successful receive
        process_received_message with message as channel_result.value
    
    When channels.ReceiveTimeout:
       Note:Handle timeout - maybe retry or use default
        Display "No message received within timeout, using default"
        process_received_message with message as "default_message"
    
    When channels.ReceiveClosed:
       Note:Handle closed channel - clean shutdown
        Display "Channel closed, shutting down receiver"
        Return None
    
    When channels.ReceiveException:
       Note:Handle errors
        Display "Receive error: " plus channel_result.error_message
        Throw "Failed to receive message: " plus channel_result.error_message
```

###Resource Management

```runa
Note:Always clean up resources
Process called "managed_concurrent_operation" returns None:
    Let pool be None
    Let channel be None
    
    Try:
       Note:Create resources
        Set pool to concurrent.create_work_pool with:
            size as 4
            pool_type as "fixed"
        
        Set channel to channels.create_channel with:
            capacity as 100
            overflow_strategy as "block"
        
       Note:Use resources for concurrent work
        perform_concurrent_operations with pool as pool and channel as channel
    
    Finally:
       Note:Always clean up, even if exceptions occur
        If pool is not None:
            concurrent.shutdown_work_pool with:
                pool as pool
                await_completion as true
                timeout_ms as 5000
        
        If channel is not None:
            channels.close_channel with channel as channel
    
    Return None
```

###Testing Concurrent Code

```runa
Note:Example of testing concurrent behavior
Process called "test_concurrent_counter" returns None:
    Let atomic_counter be atomic.create_atomic_integer with:
        initial_value as 0
        ordering as None
    
    Let increment_count be 1000
    Let thread_count be 4
    Let expected_total be increment_count times thread_count
    
   Note:Create threads that increment counter
    Let increment_threads be list containing
    For i from 1 to thread_count:
        Let increment_thread be threads.create_thread with:
            function_name as "increment_counter_multiple_times"
            arguments as list containing atomic_counter, increment_count
            thread_name as "Incrementer-" plus i as String
        
        Add increment_thread to increment_threads
        threads.start_thread with thread as increment_thread
    
   Note:Wait for all threads to complete
    For each thread in increment_threads:
        threads.join_thread with thread as thread and timeout as 10.0
    
   Note:Verify final value
    Let final_value be atomic.atomic_load with:
        atomic_int as atomic_counter
        ordering as "acquire"
    
    If final_value is equal to expected_total:
        Display "Test passed: counter = " plus final_value as String
    Otherwise:
        Display "Test failed: expected " plus expected_total as String plus ", got " plus final_value as String
    
    Return None

Process called "increment_counter_multiple_times" that takes counter as atomic.AtomicInteger and count as Integer returns None:
    For i from 1 to count:
        atomic.atomic_fetch_add with:
            atomic_int as counter
            value as 1
            ordering as None
    
    Return None
```

##Performance Guidelines

###Choosing Thread Pool Types

- **Fixed Thread Pool**: Best for I/O-bound tasks with predictable load
- **Cached Thread Pool**: Good for short-lived tasks with variable load
- **Work-Stealing Pool**: Optimal for CPU-intensive, parallelizable tasks
- **Single Thread Executor**: Use for ordered task execution

###Memory Ordering Guidelines

- **relaxed**: Use for simple counters where ordering doesn't matter
- **acquire/release**: Use for synchronization and publishing data
- **seq_cst**: Use when you need the strongest guarantees (default)

###Channel Sizing

- **Unbuffered (capacity=0)**: Synchronous communication, strongest backpressure
- **Small buffer (1-10)**: Good for most producer-consumer scenarios
- **Large buffer (100+)**: Use when you need to decouple producer/consumer rates
- **Unbounded**: Avoid unless you have memory guarantees

##Integration Examples

###Web Server with Concurrent Request Handling

```runa
Import "stdlib/concurrent/concurrent" as concurrent
Import "stdlib/concurrent/channels" as channels

Note:Create request processing pipeline
Let request_pipeline be concurrent.create_async_pipeline

concurrent.add_pipeline_stage with:
    pipeline as request_pipeline
    stage_function as "parse_http_request"
    stage_config as None

concurrent.add_pipeline_stage with:
    pipeline as request_pipeline
    stage_function as "handle_business_logic"
    stage_config as None

concurrent.add_pipeline_stage with:
    pipeline as request_pipeline
    stage_function as "format_http_response"
    stage_config as None

Note:Create connection handler pool
Let connection_pool be concurrent.create_work_pool with:
    size as 10
    pool_type as "cached"

Note:Simulate handling multiple requests
Process called "handle_http_requests" that takes request_count as Integer returns None:
    Let requests be list containing
    
   Note:Generate mock requests
    For i from 1 to request_count:
        Add ("GET /api/data/" plus i as String) to requests
    
   Note:Process requests through pipeline
    Let pipeline_result be concurrent.run_async_pipeline with:
        pipeline as request_pipeline
        input_data as requests
    
    Match pipeline_result:
        When concurrent.ConcurrentSuccess:
            Display "Processed " plus length of pipeline_result.value as String plus " HTTP requests"
        When concurrent.ConcurrentException:
            Display "Request processing failed: " plus pipeline_result.error_message
    
    Return None

Note:Run web server simulation
handle_http_requests with request_count as 100
```

###Data Processing Pipeline

```runa
Note:Create data processing system with multiple stages
Process called "create_data_processing_system" returns None:
   Note:Create channels for each stage
    Let raw_data_channel be channels.create_channel with:
        capacity as 50
        overflow_strategy as "block"
    
    Let validated_data_channel be channels.create_channel with:
        capacity as 50
        overflow_strategy as "block"
    
    Let processed_data_channel be channels.create_channel with:
        capacity as 50
        overflow_strategy as "block"
    
   Note:Create actors for each processing stage
    Let validator_actor be concurrent.create_actor with:
        behavior as "data_validator"
        initial_state as dictionary containing:
            "input_channel" as raw_data_channel
            "output_channel" as validated_data_channel
    
    Let processor_actor be concurrent.create_actor with:
        behavior as "data_processor"
        initial_state as dictionary containing:
            "input_channel" as validated_data_channel
            "output_channel" as processed_data_channel
    
    Let storage_actor be concurrent.create_actor with:
        behavior as "data_storage"
        initial_state as dictionary containing:
            "input_channel" as processed_data_channel
    
   Note:Send data through the pipeline
    Let raw_data be list containing "data1", "data2", "data3", "invalid_data", "data5"
    
    For each data_item in raw_data:
        channels.send_to_channel with:
            channel as raw_data_channel
            value as data_item
            timeout as None
    
   Note:Close input channel to signal end of data
    channels.close_channel with channel as raw_data_channel
    
   Note:Allow time for processing
    threads.sleep_thread with duration_ms as 5000
    
   Note:Stop all actors
    concurrent.stop_actor with actor as validator_actor
    concurrent.stop_actor with actor as processor_actor
    concurrent.stop_actor with actor as storage_actor
    
    Return None
```

##Conclusion

The Runa Concurrent Programming Ecosystem provides a comprehensive, production-ready foundation for building scalable concurrent applications. By combining natural language syntax with powerful concurrent primitives, it enables developers to write maintainable, efficient concurrent code that scales from simple producer-consumer patterns to complex distributed systems.

The actor-based model ensures clean separation of concerns while the unified API makes it easy to combine different concurrent patterns as needed. Whether you're building web services, data processing pipelines, or real-time systems, this ecosystem provides the tools you need for robust concurrent programming.

For additional examples and advanced usage patterns, refer to the individual module documentation and the comprehensive test suite in `tests/unit/stdlib/test_concurrent.runa`.