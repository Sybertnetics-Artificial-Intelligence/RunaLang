# Intelligent Debugging in Runa

## Overview

Runa's Intelligent Debugging system transforms the traditional debugging experience by integrating AI-powered analysis, error diagnosis, and fix suggestion capabilities directly into the language's development environment. This system helps developers identify, understand, and resolve issues more efficiently by combining static analysis, runtime insights, and machine learning.

## Core Features

### 1. AI-Assisted Error Diagnosis

Intelligently analyze errors and provide contextual explanations:

```runa
# Import the debugging module
import runa.debugging

# Initialize the intelligent debugger
Let debugger = IntelligentDebugger.create({
    "analysis_level": "comprehensive",   # Options: basic, standard, comprehensive
    "suggestion_mode": "interactive",    # Options: passive, interactive, aggressive
    "context_awareness": true,
    "language_model": "runa-debugging-assistant"
})

# Analyze runtime error with stack trace
Let diagnosis = debugger.diagnose_error(error_object, {
    "include_context": true,
    "max_suggestions": 3,
    "include_related_issues": true
})

# Display the diagnosis
Print("Root cause: " + diagnosis.root_cause)
Print("Error type: " + diagnosis.error_type)
Print("Explanation: " + diagnosis.explanation)

# Show suggestions
Print("Suggested fixes:")
For suggestion in diagnosis.suggestions:
    Print("- " + suggestion.description)
    Print("  Confidence: " + suggestion.confidence)
    Print("  Code: " + suggestion.code_snippet)
```

### 2. Semantic Breakpoints

Set intelligent breakpoints that trigger based on semantic conditions rather than just line numbers:

```runa
# Create a semantic breakpoint that triggers when a specific condition occurs
Let value_breakpoint = debugger.create_semantic_breakpoint({
    "type": "value_condition",
    "target": "user_data.balance",
    "condition": "< 0",
    "description": "Detect negative balance",
    "capture_context": true
})

# Create a pattern breakpoint that triggers when a specific code pattern executes
Let pattern_breakpoint = debugger.create_semantic_breakpoint({
    "type": "pattern_match",
    "pattern": "database.write() without validation",
    "capture_stack_trace": true,
    "notification": "alert"
})

# Create a performance breakpoint that triggers when execution is unexpectedly slow
Let performance_breakpoint = debugger.create_semantic_breakpoint({
    "type": "performance_anomaly",
    "target": "payment_processing()",
    "threshold": "200ms",
    "baseline": "historical_average"
})

# Create a state change breakpoint
Let state_breakpoint = debugger.create_semantic_breakpoint({
    "type": "state_change",
    "watch_object": "shopping_cart",
    "trigger_on": "item_count_decrease",
    "ignore_when": "checkout_in_progress"
})

# Activate all breakpoints
debugger.activate_breakpoints()
```

### 3. Smart Fix Suggestions

Receive intelligent fix suggestions for identified issues:

```runa
# Analyze code for issues
Let analysis_result = debugger.analyze_code("./src/payment_processor.runa", {
    "checks": ["security", "performance", "logic", "style"],
    "severity_threshold": "warning"
})

# Get fix suggestions for detected issues
Let fix_suggestions = debugger.generate_fixes(analysis_result.issues, {
    "max_suggestions_per_issue": 2,
    "include_explanations": true,
    "prefer_minimal_changes": true
})

# Apply a selected fix
If fix_suggestions.has_fixes():
    Let selected_fix = fix_suggestions.issues[0].suggestions[0]
    Let result = debugger.apply_fix(selected_fix, {
        "create_backup": true,
        "add_comment": true
    })
    
    If result.success:
        Print("Fix applied successfully to " + result.file_path)
    Else:
        Print("Failed to apply fix: " + result.error)
```

### 4. Execution Flow Visualization

Visualize program execution flow to better understand complex code paths:

```runa
# Start recording program execution
debugger.start_execution_recording({
    "max_depth": 10,
    "include_variables": true,
    "include_return_values": true
})

# Run the function to analyze
complex_process(input_data)

# Stop recording
Let execution_data = debugger.stop_execution_recording()

# Generate visualization
Let visualization = debugger.visualize_execution_flow(execution_data, {
    "format": "interactive",  # Options: text, graph, interactive
    "highlight_hotspots": true,
    "group_similar_calls": true,
    "max_nodes": 50
})

# Display or save the visualization
visualization.display()
visualization.save("./debug_output/execution_flow.html")
```

### 5. Time-Travel Debugging

Step backward and forward through program execution history:

```runa
# Enable time-travel debugging
debugger.enable_time_travel({
    "memory_limit": "2GB",
    "capture_interval": "instruction",  # Options: instruction, statement, function_call
    "auto_snapshot_frequency": 1000     # Create snapshots every 1000 instructions
})

# Execute program code that needs debugging
result = complex_calculation(data)

# Now navigate execution history
debugger.go_to_previous_state()  # Step back one state
debugger.go_to_state(state_id)   # Jump to specific state
debugger.go_to_next_state()      # Step forward one state

# Query variables at current history point
Let value_at_point = debugger.inspect_variable("result_sum")
Print("Value at this point: " + value_at_point)

# Find state where a condition was true
Let target_state = debugger.find_state_where({
    "condition": "validation_failed == true",
    "search_direction": "backward"
})

debugger.go_to_state(target_state.id)
```

### 6. Root Cause Analysis

Automatically trace issues back to their root causes:

```runa
# Run root cause analysis on an error
Let root_cause_analysis = debugger.analyze_root_cause(error_instance, {
    "max_depth": 10,
    "include_external_factors": true,
    "analyze_data_flow": true,
    "analyze_control_flow": true
})

# Display analysis results
Print("Root cause analysis:")
Print("Primary cause: " + root_cause_analysis.primary_cause)
Print("Confidence: " + root_cause_analysis.confidence)
Print("Causal chain:")

For step in root_cause_analysis.causal_chain:
    Print(step.sequence + ". " + step.description)
    Print("   Location: " + step.location)
    Print("   Relevance: " + step.relevance_score)

# Get recommended fix approach
Print("Recommended resolution approach:")
Print(root_cause_analysis.recommended_resolution)
```

### 7. Intelligent Log Analysis

Analyze application logs with AI to identify patterns and anomalies:

```runa
# Analyze logs for patterns and anomalies
Let log_analysis = debugger.analyze_logs("./logs/application.log", {
    "time_range": "last_24_hours",
    "detect_anomalies": true,
    "identify_patterns": true,
    "correlate_errors": true,
    "severity_threshold": "warning"
})

# Display log analysis results
Print("Log Analysis Results:")
Print("Total entries analyzed: " + log_analysis.total_entries)
Print("Anomalies detected: " + log_analysis.anomalies.count)
Print("Error patterns detected: " + log_analysis.patterns.count)

# Examine top anomalies
Print("\nTop Anomalies:")
For anomaly in log_analysis.anomalies.top(3):
    Print("- " + anomaly.description)
    Print("  Severity: " + anomaly.severity)
    Print("  First occurrence: " + anomaly.first_occurrence)
    Print("  Frequency: " + anomaly.frequency)
    Print("  Possible causes: " + anomaly.possible_causes.join(", "))

# Generate remediation plan
Let remediation_plan = log_analysis.generate_remediation_plan()
Print("\nRemediation Plan:")
For step in remediation_plan.steps:
    Print(step.order + ". " + step.description)
```

### 8. Collaborative Debugging

Share debugging sessions and collaborate with team members:

```runa
# Create a shareable debugging session
Let session = debugger.create_collaborative_session({
    "name": "Payment Processing Bug",
    "description": "Investigating timeout in payment gateway",
    "permission": "team_only",  # Options: public, team_only, private_with_links
    "expires_in": "24h"
})

# Add artifacts to the session
session.add_error_log(error_data)
session.add_execution_trace(execution_data)
session.add_code_snapshot("./src/payment_processor.runa")
session.add_note("The issue happens only with transactions > $10,000")

# Generate shareable link
Let share_link = session.generate_link()
Print("Collaborative debugging session created: " + share_link)

# Update session with findings
session.add_finding({
    "type": "root_cause",
    "description": "Timeout due to missing index in database query",
    "evidence": ["slow_query.log", "execution_trace_id:12345"],
    "proposed_fix": "Add index to transactions.amount column"
})

# Mark issues as resolved
session.mark_resolved({
    "resolution_type": "fix_applied",
    "fix_description": "Added missing index and optimized query",
    "fixed_by": "developer_id:8675309",
    "verified": true
})
```

## Advanced Features

### 1. Predictive Debugging

Anticipate potential issues before they cause problems:

```runa
# Run predictive analysis on codebase
Let prediction_results = debugger.run_predictive_analysis("./src/", {
    "prediction_types": ["errors", "performance_bottlenecks", "security_vulnerabilities"],
    "confidence_threshold": 0.7,
    "max_predictions": 20,
    "include_remediation": true
})

# Review predictions
Print("Predictive Analysis Results:")
Print("Total predictions: " + prediction_results.total)

For category in prediction_results.categories:
    Print("\n" + category.name + " (" + category.count + "):")
    For prediction in category.predictions:
        Print("- " + prediction.description)
        Print("  Location: " + prediction.location)
        Print("  Confidence: " + prediction.confidence)
        Print("  Potential impact: " + prediction.impact)
        Print("  Recommended action: " + prediction.recommendation)
```

### 2. Knowledge-Enhanced Debugging

Leverage domain knowledge and codebase-specific information:

```runa
# Create a knowledge-enhanced debugger
Let knowledge_debugger = IntelligentDebugger.create_with_knowledge({
    "knowledge_sources": [
        {"type": "code_repository", "path": "./src/"},
        {"type": "documentation", "path": "./docs/"},
        {"type": "error_database", "path": "./error_db.json"},
        {"type": "domain_model", "path": "./domain_model.kg"}
    ],
    "custom_rules": "./debugging_rules.yaml"
})

# Run knowledge-enhanced diagnosis
Let enhanced_diagnosis = knowledge_debugger.diagnose_with_knowledge(error_object, {
    "use_historical_context": true,
    "apply_domain_knowledge": true,
    "similarity_threshold": 0.8
})

# Review domain-specific insights
Print("Knowledge-Enhanced Diagnosis:")
Print("Error category: " + enhanced_diagnosis.domain_category)
Print("Similar past issues: " + enhanced_diagnosis.similar_issues.count)
Print("Domain-specific insights: ")
For insight in enhanced_diagnosis.domain_insights:
    Print("- " + insight)

# Get remediation based on domain knowledge
Let contextual_fix = enhanced_diagnosis.get_contextual_fix()
Print("Recommended fix based on domain knowledge: " + contextual_fix.description)
```

### 3. Multi-Language Debugging

Debug applications that use multiple programming languages:

```runa
# Create a multi-language debugger
Let multilang_debugger = IntelligentDebugger.create_multilanguage({
    "languages": [
        {"name": "runa", "version": "latest"},
        {"name": "python", "version": "3.9+"},
        {"name": "javascript", "version": "es2020+"},
        {"name": "c++", "version": "17+"}
    ],
    "translation_mode": "unified"  # Options: unified, native, hybrid
})

# Attach to multi-language project
multilang_debugger.attach_project("./project_root/", {
    "entry_point": "./src/main.runa",
    "include_external_dependencies": true
})

# Set cross-language breakpoint
Let cross_breakpoint = multilang_debugger.set_cross_language_breakpoint({
    "description": "Track data across language boundaries",
    "activation": {
        "runa": {"file": "api_handler.runa", "line": 42, "condition": "request.has_data()"},
        "python": {"file": "data_processor.py", "function": "process_data", "parameter": "input_data"}
    },
    "data_tracking": ["request.data", "input_data"]
})

# Start debugging
multilang_debugger.start()

# Get cross-language call stack when breakpoint hits
Let cross_stack = multilang_debugger.get_cross_language_stack()
Print("Cross-language call stack:")
For frame in cross_stack:
    Print(frame.language + ": " + frame.file + ":" + frame.line + " (" + frame.function + ")")

# Examine values across language boundaries
Let tracked_values = multilang_debugger.get_tracked_values()
For key in tracked_values.keys():
    Print(key + ": " + tracked_values[key])
```

### 4. Performance Profiling and Optimization

Identify and fix performance bottlenecks:

```runa
# Create a performance profiler
Let profiler = debugger.create_performance_profiler({
    "profiling_mode": "sampling",  # Options: sampling, instrumentation, hybrid
    "sampling_rate": 1000,         # Samples per second
    "track_memory": true,
    "track_io": true
})

# Start profiling
profiler.start()

# Execute code to profile
complex_operation()

# Stop profiling
Let profile_data = profiler.stop()

# Analyze performance data
Let perf_analysis = profiler.analyze(profile_data, {
    "focus_areas": ["cpu", "memory", "io"],
    "hotspot_threshold": 0.05,     # 5% of total time
    "generate_flame_graph": true
})

# Display performance analysis
Print("Performance Analysis:")
Print("Total execution time: " + perf_analysis.total_time + "ms")
Print("CPU hotspots:")
For hotspot in perf_analysis.cpu_hotspots:
    Print("- " + hotspot.function + ": " + hotspot.percentage + "% (" + hotspot.time + "ms)")
    Print("  File: " + hotspot.file + ":" + hotspot.line)
    Print("  Called: " + hotspot.call_count + " times")

# Get optimization suggestions
Let optimizations = profiler.suggest_optimizations(perf_analysis, {
    "max_suggestions": 5,
    "include_code_changes": true
})

For suggestion in optimizations:
    Print("\nOptimization suggestion: " + suggestion.description)
    Print("Estimated improvement: " + suggestion.estimated_improvement)
    Print("Confidence: " + suggestion.confidence)
    Print("Implementation:")
    Print(suggestion.implementation)
```

## Example: Comprehensive Debugging Workflow

```runa
Process called "debug_payment_system":
    # Step 1: Initialize the intelligent debugging system
    Print("Initializing intelligent debugging system...")
    import runa.debugging
    
    Let debugger = IntelligentDebugger.create({
        "analysis_level": "comprehensive",
        "context_awareness": true,
        "knowledge_sources": [
            {"type": "code_repository", "path": "./src/"},
            {"type": "documentation", "path": "./docs/"},
            {"type": "error_database", "path": "./error_db.json"}
        ]
    })
    
    # Step 2: Run the system with monitoring
    Print("Running payment system with debugging enabled...")
    debugger.enable_monitoring({
        "exception_tracking": true,
        "performance_tracking": true,
        "memory_tracking": true,
        "enable_time_travel": true
    })
    
    Let result = execute_with_monitoring("./src/payment_system.runa", {
        "arguments": ["--process", "daily_transactions.json"],
        "timeout": 300  # 5 minutes
    })
    
    # Step 3: Analyze execution results
    Print("Analyzing execution results...")
    If result.has_errors():
        # Error path - diagnose issues
        Print("Errors detected during execution. Diagnosing...")
        Let diagnosis = debugger.diagnose_error(result.error, {
            "include_context": true,
            "max_suggestions": 3
        })
        
        Print("Error diagnosis:")
        Print("- Type: " + diagnosis.error_type)
        Print("- Root cause: " + diagnosis.root_cause)
        Print("- Location: " + diagnosis.location)
        
        # Perform root cause analysis
        Let root_cause = debugger.analyze_root_cause(result.error)
        Print("\nRoot cause analysis:")
        Print("Primary cause: " + root_cause.primary_cause)
        Print("Causal chain:")
        For step in root_cause.causal_chain:
            Print("- " + step.description)
        
        # Get fix suggestions
        Print("\nSuggested fixes:")
        For suggestion in diagnosis.suggestions:
            Print("- " + suggestion.description)
            
        # Apply selected fix if confidence is high
        If diagnosis.suggestions[0].confidence > 0.85:
            Print("\nApplying high-confidence fix automatically...")
            Let fix_result = debugger.apply_fix(diagnosis.suggestions[0], {
                "create_backup": true,
                "add_comment": true
            })
            
            If fix_result.success:
                Print("Fix applied successfully!")
                Print("Running verification test...")
                Let verification = debugger.verify_fix(fix_result.file_path)
                Print("Verification result: " + (verification.success ? "Success" : "Failed"))
            Else:
                Print("Failed to apply fix: " + fix_result.error)
        Else:
            Print("\nNo high-confidence automatic fixes available.")
            Print("Please review suggested fixes manually.")
    Else:
        # Success path - performance analysis
        Print("Execution completed successfully. Analyzing performance...")
        Let perf_analysis = debugger.analyze_performance(result.performance_data, {
            "identify_bottlenecks": true,
            "suggest_optimizations": true
        })
        
        Print("Performance analysis:")
        Print("- Total execution time: " + perf_analysis.total_time + "ms")
        Print("- Memory peak: " + perf_analysis.memory_peak + "MB")
        
        # Check for performance bottlenecks
        If perf_analysis.bottlenecks.count > 0:
            Print("\nPerformance bottlenecks detected:")
            For bottleneck in perf_analysis.bottlenecks:
                Print("- " + bottleneck.description)
                Print("  Location: " + bottleneck.location)
                Print("  Impact: " + bottleneck.impact + "% of total time")
                
            # Get optimization suggestions
            Print("\nOptimization suggestions:")
            For optimization in perf_analysis.optimizations:
                Print("- " + optimization.description)
                Print("  Estimated improvement: " + optimization.estimated_improvement)
                Print("  Implementation complexity: " + optimization.complexity)
        Else:
            Print("\nNo significant performance bottlenecks detected.")
    
    # Step 4: Intelligent log analysis
    Print("\nAnalyzing application logs...")
    Let log_analysis = debugger.analyze_logs("./logs/payment_system.log", {
        "time_range": "execution_period",
        "detect_anomalies": true,
        "correlate_with_execution": true
    })
    
    Print("Log analysis results:")
    Print("- Entries analyzed: " + log_analysis.total_entries)
    Print("- Warning events: " + log_analysis.warning_count)
    Print("- Error events: " + log_analysis.error_count)
    
    If log_analysis.anomalies.count > 0:
        Print("\nLog anomalies detected:")
        For anomaly in log_analysis.anomalies:
            Print("- " + anomaly.description)
            Print("  First occurrence: " + anomaly.first_occurrence)
            Print("  Count: " + anomaly.count)
    
    # Step 5: Create a debugging report
    Print("\nGenerating comprehensive debugging report...")
    Let report = debugger.generate_report({
        "include_error_analysis": result.has_errors(),
        "include_performance_analysis": true,
        "include_log_analysis": true,
        "format": "html",
        "include_visualizations": true
    })
    
    report.save("./debug_output/payment_system_debug_report.html")
    Print("Debug report saved to: ./debug_output/payment_system_debug_report.html")
    
    # Step 6: Create collaborative session if issues found
    If result.has_errors() || perf_analysis.bottlenecks.count > 0:
        Print("\nCreating collaborative debugging session...")
        Let session = debugger.create_collaborative_session({
            "name": "Payment System Issues - " + current_date_time(),
            "description": result.has_errors() 
                ? "Error diagnosis and fixes" 
                : "Performance optimization opportunities",
            "permission": "team_only"
        })
        
        # Add artifacts to session
        session.add_report(report)
        session.add_execution_data(result)
        If result.has_errors():
            session.add_error_diagnosis(diagnosis)
        Else:
            session.add_performance_analysis(perf_analysis)
        
        Let share_link = session.generate_link()
        Print("Collaborative debugging session created: " + share_link)
    
    # Return debugging results
    Return {
        "success": !result.has_errors(),
        "error_diagnosed": result.has_errors() ? true : null,
        "performance_analyzed": true,
        "report_path": "./debug_output/payment_system_debug_report.html",
        "session_link": session ? session.link : null,
        "diagnosis": result.has_errors() ? diagnosis : null,
        "performance": perf_analysis
    }
```

## Integration with Other Components

### 1. Integration with Knowledge Graphs

Enhance debugging with knowledge graph capabilities:

```runa
# Import knowledge graph module
import runa.ai.knowledge_graph

# Create a knowledge graph enhanced debugger
Let kg_debugger = IntelligentDebugger.create_with_knowledge_graph({
    "knowledge_graph": {
        "source": "./project_knowledge_graph.kg",
        "embedding_model": "runa-code-embedding"
    },
    "reasoning_engine": "semantic",
    "query_language": "cypher"
})

# Diagnose errors with knowledge graph insights
Let kg_diagnosis = kg_debugger.diagnose_with_knowledge_graph(error_object, {
    "query_dependencies": true,
    "include_historical_patterns": true,
    "use_similar_cases": true
})

# Get contextual insights from knowledge graph
Print("Diagnosis enhanced with knowledge graph:")
Print("Classes involved: " + kg_diagnosis.related_entities.classes.join(", "))
Print("Dependencies: " + kg_diagnosis.related_entities.dependencies.join(", "))
Print("Similar past errors: " + kg_diagnosis.similar_cases.count)

# Query related knowledge
Let context = kg_debugger.query_knowledge_context({
    "error_type": error_object.type,
    "related_components": kg_diagnosis.related_entities.components,
    "depth": 2
})

Print("Knowledge context:")
For component in context.components:
    Print("- " + component.name)
    Print("  Purpose: " + component.purpose)
    Print("  Dependencies: " + component.dependencies.join(", "))
    Print("  Common issues: " + component.common_issues.join(", "))
```

### 2. Integration with LLMs

Leverage large language models for enhanced debugging:

```runa
# Import LLM module
import runa.ai.llm

# Create an LLM-enhanced debugger
Let llm_debugger = IntelligentDebugger.create_with_llm({
    "model": "runa-debugging-assistant",
    "temperature": 0.3,
    "max_tokens": 1000,
    "use_code_context": true
})

# Get natural language explanation of an error
Let explanation = llm_debugger.explain_error(error_object, {
    "detail_level": "detailed",  # Options: brief, standard, detailed
    "audience": "developer",     # Options: beginner, developer, expert
    "include_examples": true
})

Print("Error explanation:")
Print(explanation.summary)
Print("\nDetailed explanation:")
Print(explanation.detailed)

# Generate fixes using LLM
Let generated_fixes = llm_debugger.generate_fixes_with_llm(error_object, {
    "max_solutions": 3,
    "explain_solutions": true,
    "consider_best_practices": true
})

Print("LLM-generated fixes:")
For fix in generated_fixes:
    Print("\nSolution " + fix.id + ":")
    Print("Description: " + fix.description)
    Print("Code:")
    Print(fix.code)
    Print("Explanation: " + fix.explanation)
    Print("Pros: " + fix.pros.join(", "))
    Print("Cons: " + fix.cons.join(", "))
```

### 3. Integration with Semantic Indexing

Use semantic code search to enhance debugging:

```runa
# Import semantic indexing module
import runa.ai.semantic_indexing

# Create a semantically-enhanced debugger
Let semantic_debugger = IntelligentDebugger.create_with_semantic_index({
    "codebase_index": "./semantic_index/codebase.idx",
    "similarity_threshold": 0.75,
    "context_window": 5  # Lines of code above/below
})

# Find semantically similar code patterns
Let similar_patterns = semantic_debugger.find_similar_patterns(error_location, {
    "search_scope": "global",     # Options: function, file, module, global
    "max_results": 5,
    "include_comments": true
})

Print("Semantically similar code patterns:")
For pattern in similar_patterns:
    Print("\nSimilarity: " + pattern.similarity_score)
    Print("Location: " + pattern.file + ":" + pattern.line)
    Print("Code:")
    Print(pattern.code_snippet)
    If pattern.has_issues:
        Print("Known issues: " + pattern.issues.join(", "))
    If pattern.has_fixes:
        Print("Has established fix patterns: " + (pattern.has_fixes ? "Yes" : "No"))

# Find examples of correct implementations
Let correct_examples = semantic_debugger.find_correct_implementations({
    "function_intent": "validate_user_input",
    "max_examples": 3,
    "sort_by": "quality"
})

Print("\nExamples of correct implementations:")
For example in correct_examples:
    Print("\nQuality score: " + example.quality_score)
    Print("Location: " + example.file + ":" + example.line)
    Print("Code:")
    Print(example.code_snippet)
    Print("Key characteristics: " + example.key_features.join(", "))
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