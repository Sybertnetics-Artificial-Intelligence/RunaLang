# Traceback Module

The Traceback module provides comprehensive utilities for working with stack traces, error reporting, debugging, and exception handling in Runa programs.

## Overview

The Traceback module offers a complete set of error handling and debugging functions with natural language syntax for basic operations and helper functions for advanced use cases.

## Basic Exception Handling

### Formatting and Printing Exceptions

```runa
Note: Basic exception handling uses natural language syntax
:End Note

Try:
    Let result be divide 10 by 0
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let trace be format exception with exc as e
    Call print exception with exc as e
    
    Call print with message as "Exception trace: " plus trace
```

### Stack Trace Operations

```runa
Let stack be extract stack trace
Let formatted_stack be format stack trace as stack
Call print stack trace as stack

Call print with message as "Stack depth: " plus length of stack
Call print with message as "Formatted stack: " plus formatted_stack
```

## Advanced Stack Analysis

### Stack Frame Operations

```runa
Let frames be extract stack frames
Let formatted_frames be format stack frames as frames
Call print stack frames as frames

Let current_frame be get current frame
Let caller_frame be get caller frame

Call print with message as "Current frame: " plus current_frame
Call print with message as "Caller frame: " plus caller_frame
```

### Frame Information

```runa
Let frame_info be get frame info of current_frame
Let formatted_frame be format frame as current_frame
Call print frame as current_frame

Call print with message as "Frame info: " plus frame_info
Call print with message as "Formatted frame: " plus formatted_frame
```

## Exception Analysis

### Exception Information Extraction

```runa
Try:
    Let result be access list at index 10 of empty_list
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let exc_info be extract exception info from e
    Let formatted_info be format exception info as exc_info
    Call print exception info as exc_info
    
    Let exc_type be get exception type of e
    Let exc_message be get exception message of e
    
    Call print with message as "Exception type: " plus exc_type
    Call print with message as "Exception message: " plus exc_message
```

### Exception Traceback

```runa
Try:
    Let result be call non_existent_function()
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let traceback be get exception traceback of e
    Let formatted_traceback be format exception traceback of e
    Call print exception traceback of e
    
    Call print with message as "Traceback lines: " plus length of traceback
    Call print with message as "Formatted traceback: " plus formatted_traceback
```

## Exception Cause Analysis

### Cause Chain Analysis

```runa
Try:
    Try:
        Let result be divide 10 by 0
        Assert false  Note: Should not reach here
    :End Note
    Catch Error as inner_e:
        Let wrapped_error be "Wrapped error: " plus inner_e
        Throw wrapped_error
    :End Note
:End Note
Catch Error as e:
    Let cause_chain be extract cause chain from e
    Let formatted_chain be format cause chain as cause_chain
    Call print cause chain as cause_chain
    
    Let root_cause be get root cause of e
    Let formatted_root be format root cause as root_cause
    Call print root cause as root_cause
    
    Call print with message as "Cause chain length: " plus length of cause_chain
    Call print with message as "Root cause: " plus formatted_root
```

## Stack Analysis

### Comprehensive Stack Analysis

```runa
Let stack be extract stack trace
Let analysis be analyze stack trace as stack
Let frames be extract stack frames
Let frame_analysis be analyze stack frames as frames

Call print with message as "Stack analysis: " plus analysis
Call print with message as "Frame analysis: " plus frame_analysis
```

### Stack Depth and Metrics

```runa
Let stack be extract stack trace
Let frames be extract stack frames

Let stack_depth be get stack depth of stack
Let frame_depth be get frame depth of frames

Call print with message as "Stack depth: " plus stack_depth
Call print with message as "Frame depth: " plus frame_depth
```

## Frame Searching and Filtering

### Finding Specific Frames

```runa
Let frames be extract stack frames

Let function_frame be find frame by function frames and "main"
Let file_frame be find frame by file frames and "main.runa"
Let line_frame be find frame by line frames and 42

If function_frame is not None:
    Call print with message as "Found function frame: " plus function_frame
If file_frame is not None:
    Call print with message as "Found file frame: " plus file_frame
If line_frame is not None:
    Call print with message as "Found line frame: " plus line_frame
```

### Filtering Frames

```runa
Let frames be extract stack frames

Let function_frames be filter frames by function frames and "process"
Let file_frames be filter frames by file frames and "*.runa"
Let line_range_frames be filter frames by line range frames and start_line as 10 and end_line as 50

Call print with message as "Function frames: " plus length of function_frames
Call print with message as "File frames: " plus length of file_frames
Call print with message as "Line range frames: " plus length of line_range_frames
```

## Frame Context and Variables

### Source Context

```runa
Let current_frame be get current frame
Let context be get frame context of current_frame with context_lines as 3
Let formatted_context be format frame context as context
Call print frame context as context

Call print with message as "Source context: " plus formatted_context
```

### Variable Inspection

```runa
Let current_frame be get current frame

Let variables be get frame variables of current_frame
Let formatted_variables be format frame variables as variables
Call print frame variables as variables

Let globals be get frame globals of current_frame
Let formatted_globals be format frame globals as globals
Call print frame globals as globals

Let arguments be get frame arguments of current_frame
Let formatted_arguments be format frame arguments as arguments
Call print frame arguments as arguments

Call print with message as "Local variables: " plus formatted_variables
Call print with message as "Global variables: " plus formatted_globals
Call print with message as "Function arguments: " plus formatted_arguments
```

## Call Chain Analysis

### Function Call Chains

```runa
Let frames be extract stack frames
Let call_chain be extract call chain from frames
Let formatted_chain be format call chain as call_chain
Call print call chain as call_chain

Call print with message as "Call chain: " plus formatted_chain
```

### Call Tree Analysis

```runa
Let frames be extract stack frames
Let call_tree be get call tree from frames
Let formatted_tree be format call tree as call_tree
Call print call tree as call_tree

Call print with message as "Call tree: " plus formatted_tree
```

## Performance Analysis

### Stack Performance

```runa
Let frames be extract stack frames
Let performance be analyze performance of frames
Let formatted_performance be format performance analysis as performance
Call print performance analysis as performance

Call print with message as "Performance analysis: " plus formatted_performance
```

### Cycle Detection

```runa
Let frames be extract stack frames
Let cycles be detect cycles in frames
Let formatted_cycles be format cycles as cycles
Call print cycles as cycles

Call print with message as "Detected cycles: " plus formatted_cycles
```

### Bottleneck Detection

```runa
Let frames be extract stack frames
Let bottlenecks be find bottlenecks in frames
Let formatted_bottlenecks be format bottlenecks as bottlenecks
Call print bottlenecks as bottlenecks

Call print with message as "Bottlenecks: " plus formatted_bottlenecks
```

## Memory and Execution Analysis

### Memory Usage

```runa
Let frames be extract stack frames
Let memory_usage be get memory usage of frames
Let formatted_memory be format memory usage as memory_usage
Call print memory usage as memory_usage

Call print with message as "Memory usage: " plus formatted_memory
```

### Execution Time

```runa
Let frames be extract stack frames
Let execution_time be get execution time of frames
Let formatted_time be format execution time as execution_time
Call print execution time as execution_time

Call print with message as "Execution time: " plus formatted_time
```

## Error Reporting

### Comprehensive Error Reports

```runa
Try:
    Let result be call problematic_function()
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let stack be extract stack trace
    Let error_report be create error report with exc as e and stack as stack
    Let formatted_report be format error report as error_report
    Call print error report as error_report
    
    Call print with message as "Error report: " plus formatted_report
```

### Saving and Loading Reports

```runa
Try:
    Let result be call another_problematic_function()
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let stack be extract stack trace
    Let error_report be create error report with exc as e and stack as stack
    
    If save error report error_report to "error_report.json":
        Call print with message as "Error report saved successfully"
        
        Let loaded_report be load error report from "error_report.json"
        Call print with message as "Loaded report: " plus loaded_report
```

### Report Comparison

```runa
Let report1 be load error report from "error_report1.json"
Let report2 be load error report from "error_report2.json"

Let comparison be compare error reports report1 and report2
Let formatted_comparison be format comparison as comparison
Call print comparison as comparison

Call print with message as "Report comparison: " plus formatted_comparison
```

### Error Statistics

```runa
Let reports be [load error report from "report1.json", load error report from "report2.json", load error report from "report3.json"]
Let statistics be get error statistics of reports
Let formatted_statistics be format error statistics as statistics
Call print error statistics as statistics

Call print with message as "Error statistics: " plus formatted_statistics
```

## Error Classification and Suggestions

### Error Classification

```runa
Try:
    Let result be call function_that_fails()
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let error_class be classify error e
    Let severity be get error severity of e
    Let category be get error category of e
    
    Call print with message as "Error class: " plus error_class
    Call print with message as "Severity: " plus severity
    Call print with message as "Category: " plus category
```

### Error Suggestions

```runa
Try:
    Let result be call function_with_issues()
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Let suggestions be get error suggestions for e
    Let formatted_suggestions be format error suggestions as suggestions
    Call print error suggestions as suggestions
    
    Call print with message as "Suggestions: " plus formatted_suggestions
```

## Debugging Support

### Debug Information

```runa
Let debug_info be get debug info
Let formatted_debug be format debug info as debug_info
Call print debug info as debug_info

Call print with message as "Debug info: " plus formatted_debug
```

### Debug Mode Management

```runa
Enable debug mode
Call print with message as "Debug enabled: " plus is debug enabled

Set debug level to "verbose"
Call print with message as "Debug level: " plus get debug level

Add debug point with name as "checkpoint1" and data as "Important data"
Add debug point with name as "checkpoint2" and data as dictionary with "key" as "value"

Let debug_points be get debug points
Let formatted_points be format debug points as debug_points
Call print debug points as debug_points

Clear debug points
Call print with message as "Debug points cleared"

Disable debug mode
Call print with message as "Debug disabled: " plus is debug enabled
```

## Logging Support

### Log Entry Management

```runa
Let log_entry be create log entry with level as "info" and message as "Application started" and data as dictionary with "version" as "1.0"
Add log entry log_entry

Let error_entry be create log entry with level as "error" and message as "Operation failed" and data as "Error details"
Add log entry error_entry

Let log_entries be get log entries
Let formatted_entries be format log entries as log_entries
Call print log entries as log_entries

Call print with message as "Log entries: " plus formatted_entries
```

### Log Persistence

```runa
If save log to "application.log":
    Call print with message as "Log saved successfully"
    
    Let loaded_entries be load log from "application.log"
    Call print with message as "Loaded entries: " plus length of loaded_entries
```

### Log Filtering and Search

```runa
Let all_entries be get log entries
Let error_entries be filter log entries all_entries and level as "error"
Let search_results be search log entries all_entries and pattern as "failed"

Call print with message as "Error entries: " plus length of error_entries
Call print with message as "Search results: " plus length of search_results
```

### Log Statistics

```runa
Let log_entries be get log entries
Let statistics be get log statistics of log_entries
Let formatted_statistics be format log statistics as statistics
Call print log statistics as statistics

Call print with message as "Log statistics: " plus formatted_statistics
```

## Helper Functions

### Advanced Usage

```runa
Note: For advanced/AI-generated code, use helper functions
:End Note

Let result be format with exc as exception and format_type as "detailed"
Let analysis be analyze with stack as traceback and analysis_type as "performance"
```

## Error Handling

### Robust Error Handling

```runa
Try:
    Let result be call potentially_failing_function()
    Note: Process result
    :End Note
Catch Error as e:
    Let error_report be create error report with exc as e and stack as extract stack trace
    Call print error report as error_report
    
    Let suggestions be get error suggestions for e
    Call print error suggestions as suggestions
    
    Add log entry create log entry with level as "error" and message as "Function failed" and data as e
```

## Performance Considerations

### Efficient Error Handling

```runa
Note: For production code, consider selective debugging
:End Note

If is debug enabled:
    Let frames be extract stack frames
    Let analysis be analyze stack frames as frames
    Call print with message as "Stack analysis: " plus analysis
Otherwise:
    Let basic_trace be format exception with exc as current_error
    Call print with message as "Error: " plus basic_trace
```

## API Reference

### Basic Exception Operations

- `format_exception(exc: Any) -> String`: Format exception to string
- `print_exception(exc: Any) -> None`: Print exception
- `extract_stack() -> List[String]`: Extract current stack trace
- `format_stack(stack: List[String]) -> String`: Format stack trace
- `print_stack(stack: List[String]) -> None`: Print stack trace

### Stack Frame Operations

- `extract_stack_frames() -> List[Dictionary[String, Any]]`: Extract stack frames
- `format_stack_frames(frames: List[Dictionary[String, Any]]) -> String`: Format stack frames
- `print_stack_frames(frames: List[Dictionary[String, Any]]) -> None`: Print stack frames
- `get_current_frame() -> Dictionary[String, Any]`: Get current frame
- `get_caller_frame() -> Dictionary[String, Any]`: Get caller frame
- `get_frame_info(frame: Dictionary[String, Any]) -> Dictionary[String, Any]`: Get detailed frame info
- `format_frame(frame: Dictionary[String, Any]) -> String`: Format single frame
- `print_frame(frame: Dictionary[String, Any]) -> None`: Print single frame

### Exception Analysis

- `extract_exception_info(exc: Any) -> Dictionary[String, Any]`: Extract exception information
- `format_exception_info(exc_info: Dictionary[String, Any]) -> String`: Format exception info
- `print_exception_info(exc_info: Dictionary[String, Any]) -> None`: Print exception info
- `get_exception_type(exc: Any) -> String`: Get exception type
- `get_exception_message(exc: Any) -> String`: Get exception message
- `get_exception_traceback(exc: Any) -> List[String]`: Get exception traceback
- `format_exception_traceback(exc: Any) -> String`: Format exception traceback
- `print_exception_traceback(exc: Any) -> None`: Print exception traceback

### Cause Chain Analysis

- `extract_cause_chain(exc: Any) -> List[Dictionary[String, Any]]`: Extract cause chain
- `format_cause_chain(cause_chain: List[Dictionary[String, Any]]) -> String`: Format cause chain
- `print_cause_chain(cause_chain: List[Dictionary[String, Any]]) -> None`: Print cause chain
- `get_root_cause(exc: Any) -> Dictionary[String, Any]`: Get root cause
- `format_root_cause(root_cause: Dictionary[String, Any]) -> String`: Format root cause
- `print_root_cause(root_cause: Dictionary[String, Any]) -> None`: Print root cause

### Stack Analysis

- `analyze_stack(stack: List[String]) -> Dictionary[String, Any]`: Analyze stack trace
- `analyze_stack_frames(frames: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`: Analyze stack frames
- `get_stack_depth(stack: List[String]) -> Integer`: Get stack depth
- `get_frame_depth(frames: List[Dictionary[String, Any]]) -> Integer`: Get frame depth

### Frame Searching and Filtering

- `find_frame_by_function(frames: List[Dictionary[String, Any]], function_name: String) -> Dictionary[String, Any]`: Find frame by function
- `find_frame_by_file(frames: List[Dictionary[String, Any]], file_name: String) -> Dictionary[String, Any]`: Find frame by file
- `find_frame_by_line(frames: List[Dictionary[String, Any]], line_number: Integer) -> Dictionary[String, Any]`: Find frame by line
- `filter_frames_by_function(frames: List[Dictionary[String, Any]], function_pattern: String) -> List[Dictionary[String, Any]]`: Filter frames by function
- `filter_frames_by_file(frames: List[Dictionary[String, Any]], file_pattern: String) -> List[Dictionary[String, Any]]`: Filter frames by file
- `filter_frames_by_line_range(frames: List[Dictionary[String, Any]], start_line: Integer, end_line: Integer) -> List[Dictionary[String, Any]]`: Filter frames by line range

### Frame Context and Variables

- `get_frame_context(frame: Dictionary[String, Any], context_lines: Integer) -> List[String]`: Get frame context
- `format_frame_context(context: List[String]) -> String`: Format frame context
- `print_frame_context(context: List[String]) -> None`: Print frame context
- `get_frame_variables(frame: Dictionary[String, Any]) -> Dictionary[String, Any]`: Get frame variables
- `format_frame_variables(variables: Dictionary[String, Any]) -> String`: Format frame variables
- `print_frame_variables(variables: Dictionary[String, Any]) -> None`: Print frame variables
- `get_frame_globals(frame: Dictionary[String, Any]) -> Dictionary[String, Any]`: Get frame globals
- `format_frame_globals(globals: Dictionary[String, Any]) -> String`: Format frame globals
- `print_frame_globals(globals: Dictionary[String, Any]) -> None`: Print frame globals
- `get_frame_arguments(frame: Dictionary[String, Any]) -> Dictionary[String, Any]`: Get frame arguments
- `format_frame_arguments(arguments: Dictionary[String, Any]) -> String`: Format frame arguments
- `print_frame_arguments(arguments: Dictionary[String, Any]) -> None`: Print frame arguments

### Call Chain Analysis

- `extract_call_chain(frames: List[Dictionary[String, Any]]) -> List[String]`: Extract call chain
- `format_call_chain(call_chain: List[String]) -> String`: Format call chain
- `print_call_chain(call_chain: List[String]) -> None`: Print call chain
- `get_call_tree(frames: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`: Get call tree
- `format_call_tree(call_tree: Dictionary[String, Any]) -> String`: Format call tree
- `print_call_tree(call_tree: Dictionary[String, Any]) -> None`: Print call tree

### Performance Analysis

- `analyze_performance(frames: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`: Analyze performance
- `format_performance_analysis(performance: Dictionary[String, Any]) -> String`: Format performance analysis
- `print_performance_analysis(performance: Dictionary[String, Any]) -> None`: Print performance analysis
- `detect_cycles(frames: List[Dictionary[String, Any]]) -> List[List[String]]`: Detect cycles
- `format_cycles(cycles: List[List[String]]) -> String`: Format cycles
- `print_cycles(cycles: List[List[String]]) -> None`: Print cycles
- `find_bottlenecks(frames: List[Dictionary[String, Any]]) -> List[Dictionary[String, Any]]`: Find bottlenecks
- `format_bottlenecks(bottlenecks: List[Dictionary[String, Any]]) -> String`: Format bottlenecks
- `print_bottlenecks(bottlenecks: List[Dictionary[String, Any]]) -> None`: Print bottlenecks

### Memory and Execution Analysis

- `get_memory_usage(frames: List[Dictionary[String, Any]]) -> Dictionary[String, Number]`: Get memory usage
- `format_memory_usage(memory: Dictionary[String, Number]) -> String`: Format memory usage
- `print_memory_usage(memory: Dictionary[String, Number]) -> None`: Print memory usage
- `get_execution_time(frames: List[Dictionary[String, Any]]) -> Dictionary[String, Number]`: Get execution time
- `format_execution_time(time: Dictionary[String, Number]) -> String`: Format execution time
- `print_execution_time(time: Dictionary[String, Number]) -> None`: Print execution time

### Error Reporting

- `create_error_report(exc: Any, stack: List[String]) -> Dictionary[String, Any]`: Create error report
- `format_error_report(report: Dictionary[String, Any]) -> String`: Format error report
- `print_error_report(report: Dictionary[String, Any]) -> None`: Print error report
- `save_error_report(report: Dictionary[String, Any], filename: String) -> Boolean`: Save error report
- `load_error_report(filename: String) -> Dictionary[String, Any]`: Load error report
- `compare_error_reports(report1: Dictionary[String, Any], report2: Dictionary[String, Any]) -> Dictionary[String, Any]`: Compare reports
- `format_comparison(comparison: Dictionary[String, Any]) -> String`: Format comparison
- `print_comparison(comparison: Dictionary[String, Any]) -> None`: Print comparison
- `get_error_statistics(reports: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`: Get error statistics
- `format_error_statistics(statistics: Dictionary[String, Any]) -> String`: Format error statistics
- `print_error_statistics(statistics: Dictionary[String, Any]) -> None`: Print error statistics

### Error Classification

- `classify_error(exc: Any) -> String`: Classify error
- `get_error_severity(exc: Any) -> String`: Get error severity
- `get_error_category(exc: Any) -> String`: Get error category
- `get_error_suggestions(exc: Any) -> List[String]`: Get error suggestions
- `format_error_suggestions(suggestions: List[String]) -> String`: Format error suggestions
- `print_error_suggestions(suggestions: List[String]) -> None`: Print error suggestions

### Debugging Support

- `get_debug_info() -> Dictionary[String, Any]`: Get debug info
- `format_debug_info(debug_info: Dictionary[String, Any]) -> String`: Format debug info
- `print_debug_info(debug_info: Dictionary[String, Any]) -> None`: Print debug info
- `set_debug_level(level: String) -> None`: Set debug level
- `get_debug_level() -> String`: Get debug level
- `enable_debug_mode() -> None`: Enable debug mode
- `disable_debug_mode() -> None`: Disable debug mode
- `is_debug_enabled() -> Boolean`: Check if debug enabled
- `add_debug_point(name: String, data: Any) -> None`: Add debug point
- `get_debug_points() -> List[Dictionary[String, Any]]`: Get debug points
- `clear_debug_points() -> None`: Clear debug points
- `format_debug_points(points: List[Dictionary[String, Any]]) -> String`: Format debug points
- `print_debug_points(points: List[Dictionary[String, Any]]) -> None`: Print debug points

### Logging Support

- `create_log_entry(level: String, message: String, data: Any) -> Dictionary[String, Any]`: Create log entry
- `add_log_entry(entry: Dictionary[String, Any]) -> None`: Add log entry
- `get_log_entries() -> List[Dictionary[String, Any]]`: Get log entries
- `clear_log_entries() -> None`: Clear log entries
- `format_log_entries(entries: List[Dictionary[String, Any]]) -> String`: Format log entries
- `print_log_entries(entries: List[Dictionary[String, Any]]) -> None`: Print log entries
- `save_log(filename: String) -> Boolean`: Save log
- `load_log(filename: String) -> List[Dictionary[String, Any]]`: Load log
- `filter_log_entries(entries: List[Dictionary[String, Any]], level: String) -> List[Dictionary[String, Any]]`: Filter log entries
- `search_log_entries(entries: List[Dictionary[String, Any]], pattern: String) -> List[Dictionary[String, Any]]`: Search log entries
- `get_log_statistics(entries: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`: Get log statistics
- `format_log_statistics(statistics: Dictionary[String, Any]) -> String`: Format log statistics
- `print_log_statistics(statistics: Dictionary[String, Any]) -> None`: Print log statistics

## Testing

The Traceback module includes comprehensive tests covering:

- Basic exception formatting and printing
- Stack trace extraction and analysis
- Stack frame operations and inspection
- Exception cause chain analysis
- Frame searching and filtering
- Variable and context inspection
- Call chain and tree analysis
- Performance and bottleneck detection
- Memory and execution analysis
- Error reporting and persistence
- Error classification and suggestions
- Debug mode management
- Logging operations
- Error handling scenarios
- Performance with large stack traces

## Examples

See the `examples/basic/traceback_operations.runa` file for complete working examples of all Traceback module features. 