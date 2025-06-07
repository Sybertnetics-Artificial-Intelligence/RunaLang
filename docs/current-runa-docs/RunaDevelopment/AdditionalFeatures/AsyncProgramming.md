# Asynchronous Programming in Runa

Asynchronous programming is a key feature in Runa that allows you to write non-blocking code for operations that might take time to complete, such as network requests, file I/O, or complex computations. This guide covers all aspects of asynchronous programming in Runa.

## Introduction to Asynchronous Programming

Asynchronous programming allows your code to:
- Continue execution while waiting for long-running operations
- Handle multiple operations concurrently
- Improve responsiveness in applications
- Efficiently utilize system resources

## Basic Asynchronous Syntax

Runa uses the keywords `Async` and `await` for asynchronous programming:

```
Async Process called "fetch_data" that takes url:
    Let response be await http_get with url as url
    Return response
```

## Defining Asynchronous Functions

To define an asynchronous function, prefix the `Process` keyword with `Async`:

```
Async Process called "download_file" that takes file_url and destination_path:
    Let content be await http_get with url as file_url
    await write_file with path as destination_path and content as content
    Return "File downloaded successfully"
```

## Using await

The `await` keyword is used to wait for the completion of an asynchronous operation:

```
Async Process called "process_user_data" that takes user_id:
    # Wait for the user data to be fetched
    Let user_data be await fetch_user with id as user_id
    
    # Wait for the analytics data to be processed
    Let analytics be await process_analytics with data as user_data
    
    Return analytics
```

## Error Handling in Asynchronous Code

Use `Try` and `Catch` blocks to handle errors in asynchronous code:

```
Async Process called "safe_fetch" that takes url:
    Try:
        Let response be await http_get with url as url
        Return response
    Catch error:
        Display "Error fetching data:" with message error
        Return None
```

## Concurrent Asynchronous Operations

### Running Tasks in Parallel

Use `parallel_await` to run multiple asynchronous operations concurrently:

```
Async Process called "fetch_multiple_resources" that takes urls:
    Let results be parallel_await for each url in urls:
        http_get with url as url
    
    Return results
```

### Waiting for the First Completed Task

Use `race_await` to wait for the first task to complete:

```
Async Process called "fetch_fastest_mirror" that takes mirror_urls:
    Let result be race_await for each url in mirror_urls:
        http_get with url as url
    
    Return result
```

## Timeouts

You can add timeouts to asynchronous operations:

```
Async Process called "fetch_with_timeout" that takes url and seconds:
    Try:
        Let response be await_with_timeout with:
            operation as http_get with url as url
            timeout_seconds as seconds
        Return response
    Catch timeout_error:
        Return "Operation timed out"
```

## Cancellation

You can cancel asynchronous operations:

```
Async Process called "cancellable_operation" that takes operation and cancel_token:
    Try:
        Let result be await_cancellable with:
            operation as operation
            token as cancel_token
        Return result
    Catch cancelled_error:
        Return "Operation was cancelled"
```

## Asynchronous Generators

Runa supports asynchronous generators that can yield values over time:

```
Async Generator Process called "stream_data" that takes source:
    Let connection be await connect with source as source
    
    While connection is open:
        Let data be await read_next with connection as connection
        If data is None:
            Break
        Yield data
        
    await close with connection as connection
```

Using an asynchronous generator:

```
Async Process called "process_stream" that takes data_source:
    Let total_processed be 0
    
    For each chunk in stream_data with source as data_source:
        await process_chunk with data as chunk
        Set total_processed to total_processed plus 1
        
    Return total_processed
```

## Asynchronous Context Managers

Define asynchronous resources that need setup and cleanup:

```
Async Context Manager Process called "database_connection" that takes connection_string:
    # Setup phase
    Let connection be await connect_to_db with connection_string as connection_string
    Yield connection
    # Cleanup phase (executed after the context block ends)
    await close_connection with connection as connection
```

Using an asynchronous context manager:

```
Async Process called "run_database_query" that takes query and connection_params:
    With database_connection with connection_string as connection_params as conn:
        Let results be await execute_query with:
            connection as conn
            query as query
        Return results
    # Connection is automatically closed after this block
```

## Real-World Examples

### Web API Client

```
Async Process called "fetch_user_profile" that takes user_id:
    Let base_url be "https://api.example.com/users"
    Let url be base_url followed by "/" followed by user_id
    
    Try:
        Let response be await http_get with url as url
        
        If response["status_code"] is equal to 200:
            Return response["body"]
        Otherwise:
            Display "Error:" with message response["status_code"] with message "-" with message response["body"]
            Return None
    Catch error:
        Display "Request failed:" with message error
        Return None
```

### Parallel Data Processing

```
Async Process called "analyze_documents" that takes document_urls:
    # Fetch all documents in parallel
    Let documents be parallel_await for each url in document_urls:
        http_get with url as url
    
    # Process each document in parallel
    Let results be parallel_await for each doc in documents:
        analyze_document with content as doc
    
    # Aggregate results
    Let summary be create_summary with results as results
    
    Return summary
```

### Asynchronous Event Processing

```
Async Process called "event_processor" that takes event_source:
    With event_connection with source as event_source as connection:
        While true:
            Let event be await connection.next_event()
            
            If event is None:
                Break
                
            Match event["type"]:
                When "message":
                    await process_message with data as event["data"]
                When "notification":
                    await send_notification with data as event["data"]
                When "error":
                    await log_error with data as event["data"]
                When _:
                    await log_unknown_event with data as event
```

## Advanced Topics

### Asynchronous Patterns

#### Pipeline Pattern

```
Async Process called "data_pipeline" that takes input_data:
    Let step1_result be await process_step_1 with data as input_data
    Let step2_result be await process_step_2 with data as step1_result
    Let step3_result be await process_step_3 with data as step2_result
    Return step3_result
```

#### Fan-out/Fan-in Pattern

```
Async Process called "distributed_processing" that takes input_chunks:
    # Fan out - distribute work
    Let tasks be list containing
    For each chunk in input_chunks:
        Add process_chunk with data as chunk to tasks
    
    # Execute all tasks in parallel
    Let results be await parallel_await with tasks as tasks
    
    # Fan in - aggregate results
    Let final_result be aggregate_results with results as results
    
    Return final_result
```

### Asynchronous State Management

```
Type AsyncState is Dictionary with:
    data as Any
    version as Integer
    last_updated as DateTime

Async Process called "update_state" that takes state and update_function:
    # Get exclusive access to state
    With async_lock with name as "state_lock":
        Let new_data be await update_function with data as state["data"]
        Let new_state be AsyncState with:
            data as new_data
            version as state["version"] plus 1
            last_updated as current_datetime()
        
        Return new_state
```

## Best Practices

1. **Use Async Appropriately**: Only make functions async when they perform I/O or call other async functions
2. **Always Await Async Results**: Never ignore awaitable results
3. **Proper Error Handling**: Always handle exceptions in async code
4. **Avoid Blocking Operations**: Don't perform CPU-intensive operations directly in async functions
5. **Consider Cancellation**: Design long-running operations to be cancellable
6. **Test Async Code Thoroughly**: Asynchronous code can have subtle timing issues

## Common Pitfalls

1. **Forgetting to Await**: Not using await on async function calls
2. **Blocking the Event Loop**: Performing CPU-intensive work without offloading
3. **Callback Hell**: Nesting too many async calls instead of using proper patterns
4. **Resource Management**: Not properly cleaning up resources (connections, file handles)
5. **Ignoring Exceptions**: Not handling errors in async code

## Performance Considerations

- Async operations have overhead; very fast operations may be faster when done synchronously
- Too many concurrent operations can overwhelm system resources
- Consider using worker pools for CPU-bound tasks
- Monitor memory usage in long-running async applications

## Debugging Asynchronous Code

1. **Logging**: Add detailed logging at different stages of async operations
2. **Tracing**: Use async context to trace request flows
3. **Timeouts**: Add timeouts to detect operations that take too long
4. **Structured Error Handling**: Use typed errors to distinguish between different failure modes

```
Async Process called "traceable_operation" that takes context and params:
    Let trace_id be context["trace_id"]
    log_event with message as "Starting operation" with trace_id as trace_id
    
    Try:
        Let result be await perform_operation with params as params
        log_event with message as "Completed operation" with trace_id as trace_id
        Return result
    Catch error:
        log_event with message as "Error in operation" with trace_id as trace_id with error as error
        Throw error
```

## Interoperability

### Working with External Asynchronous APIs

```
Async Process called "call_external_api" that takes api_function and params:
    # Convert external promise/future to Runa awaitable
    Let awaitable be convert_to_awaitable with promise as api_function(params)
    Return await awaitable
```

### Creating Awaitables from Callbacks

```
Process called "create_awaitable_from_callback" that takes callback_function and params:
    Return new awaitable that resolves when:
        callback_function with params as params and callback as (result, error):
            If error is not None:
                Reject with error
            Otherwise:
                Resolve with result
```

## Conclusion

Asynchronous programming in Runa provides powerful tools for handling concurrent operations without the complexity often associated with threading and callbacks. By understanding and applying these concepts, you can build responsive, efficient applications that handle multiple operations simultaneously while maintaining readable code.

## See Also

- [Error Handling](ErrorHandling.md)
- [Functional Programming](FunctionalProgramming.md)
- [Network Operations](NetworkOperations.md) 