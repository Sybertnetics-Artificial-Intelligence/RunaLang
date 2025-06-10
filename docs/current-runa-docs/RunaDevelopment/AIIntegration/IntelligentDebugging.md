# Intelligent Debugging in Runa

## Overview

Runa's Intelligent Debugging system transforms the traditional debugging experience by integrating AI-powered analysis, error diagnosis, and fix suggestion capabilities directly into the language's development environment. This system helps developers identify, understand, and resolve issues more efficiently by combining static analysis, runtime insights, and machine learning.

## Core Features

### 1. AI-Assisted Error Diagnosis

Intelligently analyze errors and provide contextual explanations:

```
# Import the debugging module
Import module "runa.debugging"

# Initialize the intelligent debugger
Let debugger be IntelligentDebugger.create with dictionary with:
    "analysis_level" as "comprehensive"   # Options: basic, standard, comprehensive
    "suggestion_mode" as "interactive"    # Options: passive, interactive, aggressive
    "context_awareness" as true
    "language_model" as "runa-debugging-assistant"

# Analyze runtime error with stack trace
Let diagnosis be debugger.diagnose_error with error_object and dictionary with:
    "include_context" as true
    "max_suggestions" as 3
    "include_related_issues" as true

# Display the diagnosis
Display "Root cause:" with message diagnosis.root_cause
Display "Error type:" with message diagnosis.error_type
Display "Explanation:" with message diagnosis.explanation

# Show suggestions
Display "Suggested fixes:"
For each suggestion in diagnosis.suggestions:
    Display "-" with message suggestion.description
    Display "  Confidence:" with message suggestion.confidence
    Display "  Code:" with message suggestion.code_snippet
```

### 2. Semantic Breakpoints

Set intelligent breakpoints that trigger based on semantic conditions rather than just line numbers:

```
# Create a semantic breakpoint that triggers when a specific condition occurs
Let value_breakpoint be debugger.create_semantic_breakpoint with dictionary with:
    "type" as "value_condition"
    "target" as "user_data.balance"
    "condition" as "< 0"
    "description" as "Detect negative balance"
    "capture_context" as true

# Create a pattern breakpoint that triggers when a specific code pattern executes
Let pattern_breakpoint be debugger.create_semantic_breakpoint with dictionary with:
    "type" as "pattern_match"
    "pattern" as "database.write() without validation"
    "capture_stack_trace" as true
    "notification" as "alert"

# Create a performance breakpoint that triggers when execution is unexpectedly slow
Let performance_breakpoint be debugger.create_semantic_breakpoint with dictionary with:
    "type" as "performance_anomaly"
    "target" as "payment_processing()"
    "threshold" as "200ms"
    "baseline" as "historical_average"

# Create a state change breakpoint
Let state_breakpoint be debugger.create_semantic_breakpoint with dictionary with:
    "type" as "state_change"
    "watch_object" as "shopping_cart"
    "trigger_on" as "item_count_decrease"
    "ignore_when" as "checkout_in_progress"

# Activate all breakpoints
Call debugger.activate_breakpoints
```

### 3. Smart Fix Suggestions

Receive intelligent fix suggestions for identified issues:

```
# Analyze code for issues
Let analysis_result be debugger.analyze_code with "./src/payment_processor.runa" and dictionary with:
    "checks" as list containing "security", "performance", "logic", "style"
    "severity_threshold" as "warning"

# Get fix suggestions for detected issues
Let fix_suggestions be debugger.generate_fixes with analysis_result.issues and dictionary with:
    "max_suggestions_per_issue" as 2
    "include_explanations" as true
    "prefer_minimal_changes" as true

# Apply a selected fix
If fix_suggestions.has_fixes:
    Let selected_fix be fix_suggestions.issues[0].suggestions[0]
    Let result be debugger.apply_fix with selected_fix and dictionary with:
        "create_backup" as true
        "add_comment" as true
    
    If result.success is true:
        Display "Fix applied successfully to" with message result.file_path
    Otherwise:
        Display "Failed to apply fix:" with message result.error
```

### 4. Execution Flow Visualization

Visualize program execution flow to better understand complex code paths:

```
# Start recording program execution
Call debugger.start_execution_recording with dictionary with:
    "max_depth" as 10
    "include_variables" as true
    "include_return_values" as true

# Run the function to analyze
Call complex_process with input_data

# Stop recording
Let execution_data be debugger.stop_execution_recording

# Generate visualization
Let visualization be debugger.visualize_execution_flow with execution_data and dictionary with:
    "format" as "interactive"  # Options: text, graph, interactive
    "highlight_hotspots" as true
    "group_similar_calls" as true
    "max_nodes" as 50

# Display or save the visualization
Call visualization.display
Call visualization.save with "./debug_output/execution_flow.html"
```

### 5. Time-Travel Debugging

Step backward and forward through program execution history:

```
# Enable time-travel debugging
Call debugger.enable_time_travel with dictionary with:
    "memory_limit" as "2GB"
    "capture_interval" as "instruction"  # Options: instruction, statement, function_call
    "auto_snapshot_frequency" as 1000     # Create snapshots every 1000 instructions

# Execute program code that needs debugging
Let result be complex_calculation with data

# Now navigate execution history
Call debugger.go_to_previous_state  # Step back one state
Call debugger.go_to_state with state_id   # Jump to specific state
Call debugger.go_to_next_state      # Step forward one state

# Query variables at current history point
Let value_at_point be debugger.inspect_variable with "result_sum"
Display "Value at this point:" with message value_at_point

# Find state where a condition was true
Let target_state be debugger.find_state_where with dictionary with:
    "condition" as "validation_failed == true"
    "search_direction" as "backward"

Call debugger.go_to_state with target_state.id
```

### 6. Root Cause Analysis

Automatically trace issues back to their root causes:

```
# Run root cause analysis on an error
Let root_cause_analysis be debugger.analyze_root_cause with error_instance and dictionary with:
    "max_depth" as 10
    "include_external_factors" as true
    "analyze_data_flow" as true
    "analyze_control_flow" as true

# Display analysis results
Display "Root cause analysis:"
Display "Primary cause:" with message root_cause_analysis.primary_cause
Display "Confidence:" with message root_cause_analysis.confidence
Display "Causal chain:"

For step in root_cause_analysis.causal_chain:
    Display "-" with message step.sequence + ". " + step.description
    Display "   Location:" with message step.location
    Display "   Relevance:" with message step.relevance_score

# Get recommended fix approach
Display "Recommended resolution approach:"
Display "-" with message root_cause_analysis.recommended_resolution
```

### 7. Intelligent Log Analysis

Analyze application logs with AI to identify patterns and anomalies:

```
# Analyze logs for patterns and anomalies
Let log_analysis be debugger.analyze_logs with "./logs/application.log" and dictionary with:
    "time_range" as "last_24_hours"
    "detect_anomalies" as true
    "identify_patterns" as true
    "correlate_errors" as true
    "severity_threshold" as "warning"

# Display log analysis results
Display "Log Analysis Results:"
Display "Total entries analyzed:" with message log_analysis.total_entries
Display "Anomalies detected:" with message log_analysis.anomalies.count
Display "Error patterns detected:" with message log_analysis.patterns.count

# Examine top anomalies
Display "\nTop Anomalies:"
For each anomaly in log_analysis.anomalies.top(3):
    Display "-" with message anomaly.description
    Display "  Severity:" with message anomaly.severity
    Display "  First occurrence:" with message anomaly.first_occurrence
    Display "  Frequency:" with message anomaly.frequency
    Display "  Possible causes:" with message anomaly.possible_causes.join(", ")

# Generate remediation plan
Let remediation_plan be log_analysis.generate_remediation_plan
Display "\nRemediation Plan:"
For each step in remediation_plan.steps:
    Display "-" with message step.order + ". " + step.description
```

### 8. Collaborative Debugging

Share debugging sessions and collaborate with team members:

```
# Create a shareable debugging session
Let session be debugger.create_collaborative_session with dictionary with:
    "name" as "Payment Processing Bug"
    "description" as "Investigating timeout in payment gateway"
    "permission" as "team_only"  # Options: public, team_only, private_with_links
    "expires_in" as "24h"

# Add artifacts to the session
session.add_error_log(error_data)
session.add_execution_trace(execution_data)
session.add_code_snapshot("./src/payment_processor.runa")
session.add_note("The issue happens only with transactions > $10,000")

# Generate shareable link
Let share_link be session.generate_link
Display "Collaborative debugging session created:" with message share_link

# Update session with findings
session.add_finding with dictionary with:
    "type" as "root_cause"
    "description" as "Timeout due to missing index in database query"
    "evidence" as list containing "slow_query.log", "execution_trace_id:12345"
    "proposed_fix" as "Add index to transactions.amount column"

# Mark issues as resolved
session.mark_resolved with dictionary with:
    "resolution_type" as "fix_applied"
    "fix_description" as "Added missing index and optimized query"
    "fixed_by" as "developer_id:8675309"
    "verified" as true
```

## Advanced Features

### 1. Predictive Debugging

Anticipate potential issues before they cause problems:

```
# Run predictive analysis on codebase
Let prediction_results be debugger.run_predictive_analysis with "./src/" and dictionary with:
    "prediction_types" as list containing "errors", "performance_bottlenecks", "security_vulnerabilities"
    "confidence_threshold" as 0.7
    "max_predictions" as 20
    "include_remediation" as true

# Review predictions
Display "Predictive Analysis Results:"
Display "Total predictions:" with message prediction_results.total

For each category in prediction_results.categories:
    Display "\n" with message category.name + " (" + category.count + "):"
    For each prediction in category.predictions:
        Display "-" with message prediction.description
        Display "  Location:" with message prediction.location
        Display "  Confidence:" with message prediction.confidence
        Display "  Potential impact:" with message prediction.impact
        Display "  Recommended action:" with message prediction.recommendation
```

### 2. Knowledge-Enhanced Debugging

Leverage domain knowledge and codebase-specific information:

```
# Create a knowledge-enhanced debugger
Let knowledge_debugger be IntelligentDebugger.create_with_knowledge with dictionary with:
    "knowledge_sources" as list containing:
        dictionary with:
            "type" as "code_repository"
            "path" as "./src/"
        dictionary with:
            "type" as "documentation"
            "path" as "./docs/"
        dictionary with:
            "type" as "error_database"
            "path" as "./error_db.json"
        dictionary with:
            "type" as "domain_model"
            "path" as "./domain_model.kg"
    "custom_rules" as "./debugging_rules.yaml"

# Run knowledge-enhanced diagnosis
Let enhanced_diagnosis be knowledge_debugger.diagnose_with_knowledge with error_object and dictionary with:
    "use_historical_context" as true
    "apply_domain_knowledge" as true
    "similarity_threshold" as 0.8

# Review domain-specific insights
Display "Knowledge-Enhanced Diagnosis:"
Display "Error category:" with message enhanced_diagnosis.domain_category
Display "Similar past issues:" with message enhanced_diagnosis.similar_issues.count
Display "Domain-specific insights:"
For each insight in enhanced_diagnosis.domain_insights:
    Display "-" with message insight

# Get remediation based on domain knowledge
Let contextual_fix be enhanced_diagnosis.get_contextual_fix
Display "Recommended fix based on domain knowledge:" with message contextual_fix.description
```

### 3. Multi-Language Debugging

Debug applications that use multiple programming languages:

```
# Create a multi-language debugger
Let multilang_debugger be IntelligentDebugger.create_multilanguage with dictionary with:
    "languages" as list containing:
        dictionary with:
            "name" as "runa"
            "version" as "latest"
        dictionary with:
            "name" as "python"
            "version" as "3.9+"
        dictionary with:
            "name" as "javascript"
            "version" as "es2020+"
        dictionary with:
            "name" as "c++"
            "version" as "17+"
    "translation_mode" as "unified"  # Options: unified, native, hybrid

# Attach to multi-language project
multilang_debugger.attach_project("./project_root/", dictionary with:
    "entry_point" as "./src/main.runa"
    "include_external_dependencies" as true
)

# Set cross-language breakpoint
Let cross_breakpoint be multilang_debugger.set_cross_language_breakpoint with dictionary with:
    "description" as "Track data across language boundaries"
    "activation" as dictionary with:
        "runa" as dictionary with:
            "file" as "api_handler.runa"
            "line" as 42
            "condition" as "request.has_data()"
        "python" as dictionary with:
            "file" as "data_processor.py"
            "function" as "process_data"
            "parameter" as "input_data"
    "data_tracking" as list containing "request.data", "input_data"

# Start debugging
Call multilang_debugger.start

# Get cross-language call stack when breakpoint hits
Let cross_stack be multilang_debugger.get_cross_language_stack
Display "Cross-language call stack:"
For each frame in cross_stack:
    Display "-" with message frame.language + ": " + frame.file + ":" + frame.line + " (" + frame.function + ")"

# Examine values across language boundaries
Let tracked_values be multilang_debugger.get_tracked_values
For each key in tracked_values.keys:
    Display "-" with message key + ": " + tracked_values[key]
```

### 4. Performance Profiling and Optimization

Identify and fix performance bottlenecks:

```
# Create a performance profiler
Let profiler be debugger.create_performance_profiler with dictionary with:
    "profiling_mode" as "sampling"  # Options: sampling, instrumentation, hybrid
    "sampling_rate" as 1000,         # Samples per second
    "track_memory" as true,
    "track_io" as true

# Start profiling
Call profiler.start

# Execute code to profile
Call complex_operation

# Stop profiling
Let profile_data be profiler.stop

# Analyze performance data
Let perf_analysis be profiler.analyze with profile_data and dictionary with:
    "focus_areas" as list containing "cpu", "memory", "io"
    "hotspot_threshold" as 0.05,     # 5% of total time
    "generate_flame_graph" as true

# Display performance analysis
Display "Performance Analysis:"
Display "Total execution time:" with message perf_analysis.total_time + "ms"
Display "CPU hotspots:"
For each hotspot in perf_analysis.cpu_hotspots:
    Display "-" with message hotspot.function + ": " + hotspot.percentage + "% (" + hotspot.time + "ms)"
    Display "  File:" with message hotspot.file + ":" + hotspot.line
    Display "  Called:" with message hotspot.call_count + " times"

# Get optimization suggestions
Let optimizations be profiler.suggest_optimizations with perf_analysis and dictionary with:
    "max_suggestions" as 5
    "include_code_changes" as true

For each suggestion in optimizations:
    Display "\nOptimization suggestion:" with message suggestion.description
    Display "Estimated improvement:" with message suggestion.estimated_improvement
    Display "Confidence:" with message suggestion.confidence
    Display "Implementation:"
    Display "-" with message suggestion.implementation
```

## Example: Comprehensive Debugging Workflow

```
# Process called "debug_payment_system":
    # Step 1: Initialize the intelligent debugging system
    Display "Initializing intelligent debugging system..."
    Import module "runa.debugging"
    
    Let debugger be IntelligentDebugger.create with dictionary with:
        "analysis_level" as "comprehensive"
        "context_awareness" as true
        "knowledge_sources" as list containing:
            dictionary with:
                "type" as "code_repository"
                "path" as "./src/"
            dictionary with:
                "type" as "documentation"
                "path" as "./docs/"
            dictionary with:
                "type" as "error_database"
                "path" as "./error_db.json"
    
    # Step 2: Run the system with monitoring
    Display "Running payment system with debugging enabled..."
    Call debugger.enable_monitoring with dictionary with:
        "exception_tracking" as true
        "performance_tracking" as true
        "memory_tracking" as true
        "enable_time_travel" as true
    
    Let result be execute_with_monitoring with "./src/payment_system.runa" and dictionary with:
        "arguments" as list containing "--process", "daily_transactions.json"
        "timeout" as 300  # 5 minutes

    # Step 3: Analyze execution results
    Display "Analyzing execution results..."
    If result.has_errors:
        # Error path - diagnose issues
        Display "Errors detected during execution. Diagnosing..."
        Let diagnosis be debugger.diagnose_error with result.error and dictionary with:
            "include_context" as true
            "max_suggestions" as 3

        Display "Error diagnosis:"
        Display "- Type:" with message diagnosis.error_type
        Display "- Root cause:" with message diagnosis.root_cause
        Display "- Location:" with message diagnosis.location
        
        # Perform root cause analysis
        Let root_cause be debugger.analyze_root_cause with result.error
        Display "\nRoot cause analysis:"
        Display "Primary cause:" with message root_cause.primary_cause
        Display "Causal chain:"
        For each step in root_cause.causal_chain:
            Display "-" with message step.description
        
        # Get fix suggestions
        Display "\nSuggested fixes:"
        For each suggestion in diagnosis.suggestions:
            Display "-" with message suggestion.description
            
        # Apply selected fix if confidence is high
        If diagnosis.suggestions[0].confidence > 0.85:
            Display "\nApplying high-confidence fix automatically..."
            Let fix_result be debugger.apply_fix with diagnosis.suggestions[0] and dictionary with:
                "create_backup" as true
                "add_comment" as true
            
            If fix_result.success is true:
                Display "Fix applied successfully!"
                Display "Running verification test..."
                Let verification be debugger.verify_fix with fix_result.file_path
                Display "Verification result:" with message (verification.success ? "Success" : "Failed")
            Else:
                Display "Failed to apply fix:" with message fix_result.error
        Else:
            Display "\nNo high-confidence automatic fixes available."
            Display "Please review suggested fixes manually."
    Else:
        # Success path - performance analysis
        Display "Execution completed successfully. Analyzing performance..."
        Let perf_analysis be debugger.analyze_performance with result.performance_data and dictionary with:
            "identify_bottlenecks" as true
            "suggest_optimizations" as true

        Display "Performance analysis:"
        Display "- Total execution time:" with message perf_analysis.total_time + "ms"
        Display "- Memory peak:" with message perf_analysis.memory_peak + "MB"
        
        # Check for performance bottlenecks
        If perf_analysis.bottlenecks.count > 0:
            Display "\nPerformance bottlenecks detected:"
            For each bottleneck in perf_analysis.bottlenecks:
                Display "-" with message bottleneck.description
                Display "  Location:" with message bottleneck.location
                Display "  Impact:" with message bottleneck.impact + "% of total time"
                
            # Get optimization suggestions
            Display "\nOptimization suggestions:"
            For each optimization in perf_analysis.optimizations:
                Display "-" with message optimization.description
                Display "  Estimated improvement:" with message optimization.estimated_improvement
                Display "  Implementation complexity:" with message optimization.complexity
        Else:
            Display "\nNo significant performance bottlenecks detected."
    
    # Step 4: Intelligent log analysis
    Display "\nAnalyzing application logs..."
    Let log_analysis be debugger.analyze_logs with "./logs/payment_system.log" and dictionary with:
        "time_range" as "execution_period"
        "detect_anomalies" as true
        "correlate_with_execution" as true

    Display "Log analysis results:"
    Display "- Entries analyzed:" with message log_analysis.total_entries
    Display "- Warning events:" with message log_analysis.warning_count
    Display "- Error events:" with message log_analysis.error_count
    
    If log_analysis.anomalies.count > 0:
        Display "\nLog anomalies detected:"
        For each anomaly in log_analysis.anomalies:
            Display "-" with message anomaly.description
            Display "  First occurrence:" with message anomaly.first_occurrence
            Display "  Count:" with message anomaly.count
    
    # Step 5: Create a debugging report
    Display "\nGenerating comprehensive debugging report..."
    Let report be debugger.generate_report with dictionary with:
        "include_error_analysis" as result.has_errors
        "include_performance_analysis" as true
        "include_log_analysis" as true
        "format" as "html"
        "include_visualizations" as true

    Call report.save with "./debug_output/payment_system_debug_report.html"
    Display "Debug report saved to:" with message "./debug_output/payment_system_debug_report.html"
    
    # Step 6: Create collaborative session if issues found
    If result.has_errors || perf_analysis.bottlenecks.count > 0:
        Display "\nCreating collaborative debugging session..."
        Let session be debugger.create_collaborative_session with dictionary with:
            "name" as "Payment System Issues - " + current_date_time
            "description" as (result.has_errors ? "Error diagnosis and fixes" : "Performance optimization opportunities")
            "permission" as "team_only"

        # Add artifacts to session
        Call session.add_report with report
        Call session.add_execution_data with result
        If result.has_errors:
            Call session.add_error_diagnosis with diagnosis
        Else:
            Call session.add_performance_analysis with perf_analysis
        
        Let share_link be session.generate_link
        Display "Collaborative debugging session created:" with message share_link
    
    # Return debugging results
    Return dictionary with:
        "success" as !result.has_errors
        "error_diagnosed" as (result.has_errors ? true : null)
        "performance_analyzed" as true
        "report_path" as "./debug_output/payment_system_debug_report.html"
        "session_link" as (session ? session.link : null)
        "diagnosis" as (result.has_errors ? diagnosis : null)
        "performance" as perf_analysis
```

## Integration with Other Components

### 1. Integration with Knowledge Graphs

Enhance debugging with knowledge graph capabilities:

```
# Import knowledge graph module
Import module "runa.ai.knowledge_graph"

# Create a knowledge graph enhanced debugger
Let kg_debugger be IntelligentDebugger.create_with_knowledge_graph with dictionary with:
    "knowledge_graph" as dictionary with:
        "source" as "./project_knowledge_graph.kg"
        "embedding_model" as "runa-code-embedding"
    "reasoning_engine" as "semantic"
    "query_language" as "cypher"

# Diagnose errors with knowledge graph insights
Let kg_diagnosis be kg_debugger.diagnose_with_knowledge_graph with error_object and dictionary with:
    "query_dependencies" as true
    "include_historical_patterns" as true
    "use_similar_cases" as true

# Get contextual insights from knowledge graph
Display "Diagnosis enhanced with knowledge graph:"
Display "Classes involved:" with message kg_diagnosis.related_entities.classes.join(", ")
Display "Dependencies:" with message kg_diagnosis.related_entities.dependencies.join(", ")
Display "Similar past errors:" with message kg_diagnosis.similar_cases.count

# Query related knowledge
Let context be kg_debugger.query_knowledge_context with dictionary with:
    "error_type" as error_object.type
    "related_components" as kg_diagnosis.related_entities.components
    "depth" as 2

Display "Knowledge context:"
For each component in context.components:
    Display "-" with message component.name
    Display "  Purpose:" with message component.purpose
    Display "  Dependencies:" with message component.dependencies.join(", ")
    Display "  Common issues:" with message component.common_issues.join(", ")
```

### 2. Integration with LLMs

Leverage large language models for enhanced debugging:

```
# Import LLM module
Import module "runa.ai.llm"

# Create an LLM-enhanced debugger
Let llm_debugger be IntelligentDebugger.create_with_llm with dictionary with:
    "model" as "runa-debugging-assistant"
    "temperature" as 0.3
    "max_tokens" as 1000
    "use_code_context" as true

# Get natural language explanation of an error
Let explanation be llm_debugger.explain_error with error_object and dictionary with:
    "detail_level" as "detailed"  # Options: brief, standard, detailed
    "audience" as "developer"     # Options: beginner, developer, expert
    "include_examples" as true

Display "Error explanation:"
Display "-" with message explanation.summary
Display "\nDetailed explanation:"
Display "-" with message explanation.detailed

# Generate fixes using LLM
Let generated_fixes be llm_debugger.generate_fixes_with_llm with error_object and dictionary with:
    "max_solutions" as 3
    "explain_solutions" as true
    "consider_best_practices" as true

Display "LLM-generated fixes:"
For each fix in generated_fixes:
    Display "\nSolution" with message fix.id
    Display "Description:" with message fix.description
    Display "Code:"
    Display "-" with message fix.code
    Display "Explanation:" with message fix.explanation
    Display "Pros:" with message fix.pros.join(", ")
    Display "Cons:" with message fix.cons.join(", ")
```

### 3. Integration with Semantic Indexing

Use semantic code search to enhance debugging:

```
# Import semantic indexing module
Import module "runa.ai.semantic_indexing"

# Create a semantically-enhanced debugger
Let semantic_debugger be IntelligentDebugger.create_with_semantic_index with dictionary with:
    "codebase_index" as "./semantic_index/codebase.idx"
    "similarity_threshold" as 0.75
    "context_window" as 5  # Lines of code above/below

# Find semantically similar code patterns
Let similar_patterns be semantic_debugger.find_similar_patterns with error_location and dictionary with:
    "search_scope" as "global"     # Options: function, file, module, global
    "max_results" as 5
    "include_comments" as true

Display "Semantically similar code patterns:"
For each pattern in similar_patterns:
    Display "\nSimilarity:" with message pattern.similarity_score
    Display "Location:" with message pattern.file + ":" + pattern.line
    Display "Code:"
    Display "-" with message pattern.code_snippet
    If pattern.has_issues:
        Display "Known issues:" with message pattern.issues.join(", ")
    If pattern.has_fixes:
        Display "Has established fix patterns:" with message (pattern.has_fixes ? "Yes" : "No")

# Find examples of correct implementations
Let correct_examples be semantic_debugger.find_correct_implementations with dictionary with:
    "function_intent" as "validate_user_input"
    "max_examples" as 3
    "sort_by" as "quality"

Display "\nExamples of correct implementations:"
For each example in correct_examples:
    Display "\nQuality score:" with message example.quality_score
    Display "Location:" with message example.file + ":" + example.line
    Display "Code:"
    Display "-" with message example.code_snippet
    Display "Key characteristics:" with message example.key_features.join(", ")
```

## Best Practices

1. **Start with Intelligent Error Diagnosis**: When encountering an issue, begin with the `diagnose_error` function to get AI-powered insights into the root cause.

2. **Use Semantic Breakpoints Strategically**: Place semantic breakpoints at critical points in your code where state or logic complexities may lead to issues.

3. **Combine Execution Visualization with Time-Travel**: For complex bugs, use execution flow visualization together with time-travel debugging to understand exactly how the program state evolved.

4. **Leverage Knowledge-Enhanced Debugging**: For domain-specific applications, configure the debugger with relevant knowledge sources to get more targeted insights.

5. **Verify AI-Suggested Fixes**: Always review and test AI-generated fixes before applying them to production code, especially for critical systems.

6. **Use Collaborative Sessions for Team Debugging**: For complex issues, create collaborative sessions to share debugging context with team members.

7. **Balance Performance and Detail**: Adjust the debugging detail level based on your needs - more comprehensive analysis provides deeper insights but may impact performance.

8. **Maintain a Debugging Knowledge Base**: Save valuable debugging sessions and insights to build a growing knowledge base of common issues and solutions.

## References

- [Runa Intelligent Debugging API Reference](https://runa-lang.org/docs/api/debugging)
- [Debugging Best Practices Guide](https://runa-lang.org/docs/guides/debugging)
- [Advanced Debugging Techniques Documentation](https://runa-lang.org/docs/advanced/debugging-techniques)

For complete examples, see the [Debugging Examples](../../src/tests/examples/debugging_examples.runa) in the Runa codebase. 