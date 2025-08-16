# Async Module

The Async module provides comprehensive asynchronous programming utilities for Runa, including async/await primitives, futures, tasks, event loop, scheduling, synchronization, agent-friendly concurrency patterns, and now robust context management protocols for both synchronous and asynchronous use.

## Overview

- Async/await primitives and scheduling
- Futures, tasks, and coroutines
- Event loop and scheduling
- Timeout, cancellation, and error propagation
- Synchronization primitives (locks, events, semaphores)
- Context manager protocol (sync and async)
- Async I/O and utilities
- AI/agent-friendly concurrency patterns

## Context Manager Protocol

Runa supports idiomatic context management for both synchronous and asynchronous resources via the following protocols:

```runa
Protocol ContextManager defines:
    Process called "enter_context" returns Any
    Process called "exit_context" returns None

Protocol AsyncContextManager defines:
    Async Process called "enter_async_context" returns Any
    Async Process called "exit_async_context" returns None
```

Any type implementing these protocols can be used with the `With` statement for resource management. For asynchronous context management, use an `Async:` block with `With` inside.

### Example: Synchronous Lock Context
```runa
Let lock be create_lock
With acquire lock with lock as lock_resource:
    Note: Critical section
    Display "Lock acquired!"
    Let released be release_lock with lock as lock_resource
```

### Example: Asynchronous Lock Context
```runa
Async:
    Let lock be create_lock
    With enter_async_context with lock as lock_resource:
        Note: Async critical section
        Display "Async lock acquired!"
        Let released be release_lock with lock as lock_resource
```

### Example: Using Helper Processes
```runa
With acquire_lock as lock:
    Display "Lock acquired via helper!"

Async:
    With acquire_lock_async as lock:
        Display "Async lock acquired via helper!"
```

## Supported Types

- **Lock**: Implements both ContextManager and AsyncContextManager
- **Semaphore**: Implements both ContextManager and AsyncContextManager
- **Event**: Implements both ContextManager and AsyncContextManager (wait/set idioms)

## API Reference (Context Management)

- `enter_context(lock: Lock) -> Lock`
- `exit_context(lock: Lock) -> None`
- `enter_async_context(lock: Lock) -> Lock`
- `exit_async_context(lock: Lock) -> None`
- `acquire_lock() -> Lock` (helper)
- `acquire_lock_async() -> Lock` (helper)
- `enter_context(semaphore: Semaphore) -> Semaphore`
- `exit_context(semaphore: Semaphore) -> None`
- `enter_async_context(semaphore: Semaphore) -> Semaphore`
- `exit_async_context(semaphore: Semaphore) -> None`
- `acquire_semaphore() -> Semaphore` (helper)
- `acquire_semaphore_async() -> Semaphore` (helper)
- `enter_context(event: Event) -> Event`
- `exit_context(event: Event) -> None`
- `enter_async_context(event: Event) -> Event`
- `exit_async_context(event: Event) -> None`
- `wait_for_event() -> Event` (helper)
- `wait_for_event_async() -> Event` (helper)

## Rationale and Extension Points

- The protocol is extensible: any user-defined type can implement `enter_context`/`exit_context` or their async variants.
- This design matches the ergonomics of Python's `with`/`async with` and Rust's RAII/context traits, but is fully idiomatic to Runa.
- For async context management, use `Async:` blocks with `With` inside, as `AsyncWith` is not yet a language keyword.
- All error handling is explicit: if a resource cannot be acquired or released, an exception is thrown.

## Best Practices

- Use context managers for all resource acquisition and release, especially for locks, semaphores, and events.
- Prefer helper processes for common patterns.
- Always handle exceptions in critical sections.
- For async code, always use `Async:` blocks.

## Full Example: Nested Contexts and Exception Handling
```runa
Let lock1 be create_lock
Let lock2 be create_lock
With acquire lock with lock1 as l1:
    With acquire lock with lock2 as l2:
        Try:
            Display "Both locks acquired"
        Catch exception as e:
            Display "Error: " plus e
        Finally:
            Display "Exiting critical section"
```

## See Also
- [Runa Language Specification: With Statement](../language-specification/runa_formal_grammar.md)
- [Async Programming Guide](../user/guides/ASYNC_PROGRAMMING.md)

## Core Types

### AsyncResult
```runa
Type AsyncResult is:
    | AsyncSuccess with value as Any
    | AsyncError with message as String and code as String
```

### Future
```runa
Type Future is Dictionary with:
    done as Boolean
    result as Optional[Any]
    exception as Optional[String]
    callbacks as List[Process]
    metadata as Dictionary[String, Any]
```

### Task
```runa
Type Task is Dictionary with:
    coroutine as Process
    future as Future
    cancelled as Boolean
    started as Boolean
    finished as Boolean
    result as Optional[Any]
    exception as Optional[String]
    metadata as Dictionary[String, Any]
```

### EventLoop
```runa
Type EventLoop is Dictionary with:
    running as Boolean
    tasks as List[Task]
    ready_queue as List[Task]
    scheduled as List[Tuple[Float, Task]]
    time as Float
    metadata as Dictionary[String, Any]
```

### Lock, Semaphore, Event
```runa
Type Lock is Dictionary with:
    locked as Boolean
    owner as Optional[Any]
    waiters as List[Task]
    metadata as Dictionary[String, Any]

Type Semaphore is Dictionary with:
    value as Integer
    max_value as Integer
    waiters as List[Task]
    metadata as Dictionary[String, Any]

Type Event is Dictionary with:
    is_set as Boolean
    waiters as List[Task]
    metadata as Dictionary[String, Any]
```

## Basic Usage

### Creating and Running Tasks
```runa
Let loop be create_event_loop
Process called "my_coroutine" returns Integer:
    Note: Simulate async work
    Return 42
Let task be create_task with coroutine as my_coroutine and loop as loop
Let result be run_until_complete with loop as loop and main_coroutine as my_coroutine
Display "Result: " plus result
```

### Async/Await Pattern
```runa
Note: Define an async coroutine
Async Process called "async_task" returns String:
    Display "Starting async task"
    sleep with seconds as 0.1
    Display "Task completed"
    Return "done"

Note: Run the async task
Let loop be create_event_loop
Let result be run_until_complete with loop as loop and main_coroutine as async_task
Display "Async result: " plus result
```

### Sleep Functionality
```runa
Note: Sleep in seconds
Async Process called "sleepy_task" returns String:
    Display "Before sleep"
    sleep with seconds as 1.0
    Display "After sleep"
    Return "slept"

Note: Sleep in milliseconds for precise timing
Async Process called "precise_task" returns String:
    Display "Before precise sleep"
    sleep_ms with milliseconds as 500.0
    Display "After precise sleep"
    Return "precise"
```

### Awaiting Futures
```runa
Let future be create_future
Let value be await_future with future as future
Display value
```

### Scheduling and Gathering
```runa
Let loop be create_event_loop
Let task1 be create_task with coroutine as my_coroutine and loop as loop
Let task2 be create_task with coroutine as my_coroutine and loop as loop
Let results be gather with tasks as list containing task1, task2
```

### Timeout and Cancellation
```runa
Let loop be create_event_loop
Let task be create_task with coroutine as my_coroutine and loop as loop
Let result be timeout with task as task and seconds as 5.0
Match result:
    When AsyncSuccess with value as val:
        Display "Completed: " plus val
    When AsyncError with message as msg:
        Display "Timeout: " plus msg
```

## Synchronization Primitives

### Locks
```runa
Let lock be create_lock
Let acquired be acquire_lock with lock as lock and task as task
If acquired:
    Note: Critical section
    Let released be release_lock with lock as lock
```

### Semaphores
```runa
Let sema be create_semaphore with value as 2
Let acquired be acquire_semaphore with semaphore as sema and task as task
If acquired:
    Note: Do work
    Let released be release_semaphore with semaphore as sema
```

### Events
```runa
Let event be create_event
Let set_event be set_event with event as event
Let cleared_event be clear_event with event as event
Let waited be wait_event with event as event and task as task
```

## Advanced Features

### Task Cancellation and Timeout
```runa
Note: Cancel a long-running task
Async Process called "long_task" returns String:
    sleep with seconds as 10.0
    Return "completed"

Let loop be create_event_loop
Let task be create_task with coroutine as long_task and loop as loop

Note: Cancel the task
Let cancelled_task be cancel_task with task as task
Display "Task cancelled: " plus cancelled_task["cancelled"]

Note: Use timeout for automatic cancellation
Let task2 be create_task with coroutine as long_task and loop as loop
Let result be timeout with task as task2 and seconds as 1.0
Match result:
    When AsyncError with code as "TIMEOUT":
        Display "Task timed out as expected"
    Otherwise:
        Display "Unexpected result"
```

### Concurrent Task Execution
```runa
Note: Define multiple async tasks
Async Process called "fetch_data" that takes url as String returns String:
    Display "Fetching: " plus url
    sleep with seconds as 0.5
    Return "data from " with message url

Async Process called "process_data" that takes data as String returns String:
    Display "Processing: " plus data
    sleep with seconds as 0.3
    Return "processed " with message data

Note: Run tasks concurrently
Let loop be create_event_loop
Let fetch_task1 be create_task with coroutine as (fetch_data with url as "api1.com") and loop as loop
Let fetch_task2 be create_task with coroutine as (fetch_data with url as "api2.com") and loop as loop
Let fetch_task3 be create_task with coroutine as (fetch_data with url as "api3.com") and loop as loop

Note: Wait for all tasks to complete
Let results be gather with tasks as list containing fetch_task1, fetch_task2, fetch_task3
Display "All data fetched: " plus length of results
```

### Wait Strategies
```runa
Note: Wait for first completion
Let loop be create_event_loop
Async Process called "fast_task" returns String:
    sleep with seconds as 0.1
    Return "fast"

Async Process called "slow_task" returns String:
    sleep with seconds as 1.0
    Return "slow"

Let fast be create_task with coroutine as fast_task and loop as loop
Let slow be create_task with coroutine as slow_task and loop as loop

Note: Return as soon as first task completes
Let completed be wait with tasks as list containing fast, slow and return_when as "FIRST_COMPLETED"
Display "First completed: " plus length of completed

Note: Wait for all to complete
Let all_completed be wait with tasks as list containing fast, slow and return_when as "ALL_COMPLETED"
Display "All completed: " plus length of all_completed
```

### Producer-Consumer Pattern
```runa
Note: Producer-consumer with async queues
Let shared_data be list containing

Async Process called "producer" returns None:
    For i from 1 to 5:
        Add "item" with message string from i to shared_data
        Display "Produced item " plus string from i
        sleep with seconds as 0.1

Async Process called "consumer" returns None:
    While length of shared_data is greater than 0:
        Let item be shared_data at index 0
        Remove shared_data at index 0
        Display "Consumed: " plus item
        sleep with seconds as 0.2

Let loop be create_event_loop
Let prod_task be create_task with coroutine as producer and loop as loop
Let cons_task be create_task with coroutine as consumer and loop as loop
Let results be gather with tasks as list containing prod_task, cons_task
```

### Error Handling and Propagation
```runa
Note: Handle errors in async tasks
Async Process called "failing_task" returns String:
    sleep with seconds as 0.1
    Throw "Something went wrong"
    Return "never reached"

Async Process called "error_handler" returns String:
    Try:
        Let task be create_task with coroutine as failing_task and loop as create_event_loop
        Let result be run_until_complete with loop as create_event_loop and main_coroutine as failing_task
        Return result
    Catch error:
        Display "Caught error: " plus error
        Return "error handled"

Let result be run_until_complete with loop as create_event_loop and main_coroutine as error_handler
Display "Final result: " plus result
```

### AI/Agent Concurrency Patterns
```runa
Note: Agent coordination pattern
Let agent_results be list containing

Async Process called "reasoning_agent" returns String:
    Display "Agent reasoning..."
    sleep with seconds as 0.3
    Add "reasoning complete" to agent_results
    Return "reasoning_done"

Async Process called "action_agent" returns String:
    Display "Agent acting..."
    sleep with seconds as 0.2
    Add "action complete" to agent_results
    Return "action_done"

Async Process called "memory_agent" returns String:
    Display "Agent remembering..."
    sleep with seconds as 0.1
    Add "memory updated" to agent_results
    Return "memory_done"

Note: Coordinate multiple AI agents
Let loop be create_event_loop
Let reasoning_task be create_task with coroutine as reasoning_agent and loop as loop
Let action_task be create_task with coroutine as action_agent and loop as loop
Let memory_task be create_task with coroutine as memory_agent and loop as loop

Let agent_coordination be gather with tasks as list containing reasoning_task, action_task, memory_task
Display "All agents completed: " plus length of agent_coordination
```

### Resource Management with Context Managers
```runa
Note: Advanced resource management
Async Process called "database_operation" returns String:
    Note: Use async context manager for database connection
    With acquire_lock_async as db_lock:
        Display "Database locked for operation"
        sleep with seconds as 0.1
        Display "Database operation complete"
    Return "database_result"

Note: Nested context management
Async Process called "complex_operation" returns String:
    With acquire_lock_async as resource1:
        With acquire_semaphore_async as resource2:
            Display "Both resources acquired"
            sleep with seconds as 0.1
            Return "complex_done"
```

## API Reference

### Core Event Loop and Tasks
- `create_event_loop() -> EventLoop`
- `run_until_complete(loop: EventLoop, main_coroutine: Process) -> Any`
- `create_task(coroutine: Process, loop: EventLoop) -> Task`
- `execute_task_step(loop: EventLoop, task: Task) -> None`

### Futures and Results  
- `create_future() -> Future`
- `await_future(future: Future) -> Any`
- `set_result(future: Future, value: Any) -> Future`
- `set_exception(future: Future, exception: String) -> Future`
- `add_done_callback(future: Future, callback: Process) -> Future`

### Task Management
- `cancel_task(task: Task) -> Task`
- `gather(tasks: List[Task]) -> List[Any]`
- `wait(tasks: List[Task], return_when: String) -> List[Task]`
- `timeout(task: Task, seconds: Float) -> AsyncResult`
- `shield(task: Task) -> Task`

### Sleep and Timing
- `sleep(seconds: Float) -> None` (Async)
- `sleep_ms(milliseconds: Float) -> None` (Async)

### Synchronization Primitives
- `create_lock() -> Lock`
- `acquire_lock(lock: Lock, task: Task) -> Boolean`
- `release_lock(lock: Lock) -> Boolean`
- `create_semaphore(value: Integer) -> Semaphore`
- `acquire_semaphore(semaphore: Semaphore, task: Task) -> Boolean`
- `release_semaphore(semaphore: Semaphore) -> Boolean`
- `create_event() -> Event`
- `set_event(event: Event) -> Event`
- `clear_event(event: Event) -> Event`
- `wait_event(event: Event, task: Task) -> Boolean`

### Context Management
- `enter_context(resource: Any) -> Any`
- `exit_context(resource: Any) -> None`
- `enter_async_context(resource: Any) -> Any` (Async)
- `exit_async_context(resource: Any) -> None` (Async)

### Context Manager Helpers
- `acquire_lock() -> Lock`
- `acquire_lock_async() -> Lock` (Async)
- `acquire_semaphore() -> Semaphore`
- `acquire_semaphore_async() -> Semaphore` (Async)
- `wait_for_event() -> Event`
- `wait_for_event_async() -> Event` (Async)

### Advanced Operations
- `run_in_executor(function: Process, args: List[Any]) -> Future`
- `current_time() -> Float`
- `create_async_options() -> AsyncOptions`

### Internal/System Functions
- `handle_await_target(loop: EventLoop, task: Task, await_target: Any) -> None`
- `resume_task(loop: EventLoop, task: Task, result: Any) -> None`
- `system_time_ms() -> Float`
- `system_delay(milliseconds: Float) -> None`
- `system_random() -> Integer`

This module provides all the functionality needed for robust, idiomatic, and AI-friendly asynchronous programming in Runa. 