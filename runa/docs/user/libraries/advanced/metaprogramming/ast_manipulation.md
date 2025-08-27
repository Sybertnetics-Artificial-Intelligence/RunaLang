# AST Manipulation Module

The AST (Abstract Syntax Tree) Manipulation module provides comprehensive tools for creating, transforming, analyzing, and manipulating abstract syntax trees in Runa. This module forms the foundation for all metaprogramming operations and enables sophisticated code analysis and transformation.

## Table of Contents

- [Overview](#overview)
- [Core Types](#core-types)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Advanced Patterns](#advanced-patterns)
- [Performance Considerations](#performance-considerations)
- [Best Practices](#best-practices)

## Overview

The AST Manipulation module provides a complete toolkit for working with abstract syntax trees:

- **AST Construction**: Create AST nodes with proper structure and metadata
- **Tree Traversal**: Navigate AST structures with visitor patterns
- **Transformation**: Apply transformations to AST nodes and subtrees
- **Pattern Matching**: Match AST patterns for analysis and rewriting
- **Validation**: Ensure AST integrity and correctness
- **Diffing and Merging**: Compare and combine AST structures

### Key Features

- **Type-Safe AST Operations**: All operations maintain AST structure integrity
- **Immutable by Default**: Functional programming approach with immutable operations
- **Pattern Matching**: Sophisticated pattern matching for AST analysis
- **Position Tracking**: Complete source position information preservation
- **Annotation Support**: Rich metadata and annotation system
- **Performance Optimized**: Efficient operations for large AST structures

## Core Types

### ASTNode

The fundamental AST node type that represents any element in the syntax tree.

```runa
Type called "ASTNode":
    node_type as String          Note: Type of the node (e.g., "LetStatement", "BinaryOperation")
    value as Any                 Note: Node-specific value or data
    children as List[ASTNode]    Note: Child nodes in the tree
    position as Position         Note: Source position information
    annotations as List[Annotation]  Note: Metadata and annotations
    metadata as Dictionary[String, Any]  Note: Additional metadata
```

### Position

Source location information for debugging and error reporting.

```runa
Type called "Position":
    line as Integer              Note: Line number (1-based)
    column as Integer            Note: Column number (1-based)
    offset as Integer            Note: Character offset from start
    metadata as Dictionary[String, Any]  Note: Additional position metadata
```

### Annotation

Metadata attached to AST nodes for analysis and transformation.

```runa
Type called "Annotation":
    annotation_type as String    Note: Type of annotation
    value as Any                 Note: Annotation data
    metadata as Dictionary[String, Any]  Note: Additional annotation metadata
```

### ASTPattern

Pattern specification for matching AST structures.

```runa
Type called "ASTPattern":
    pattern_type as String       Note: Expected node type
    value as Any                 Note: Expected value (None for wildcard)
    children as List[ASTPattern] Note: Child patterns
    metadata as Dictionary[String, Any]  Note: Pattern metadata
```

### RewriteRule

Rule for transforming AST structures through pattern matching.

```runa
Type called "RewriteRule":
    rule_id as String            Note: Unique identifier for the rule
    pattern as ASTPattern        Note: Pattern to match
    replacement as ASTNode       Note: Replacement AST structure
    conditions as List[String]   Note: Additional conditions for application
    metadata as Dictionary[String, Any]  Note: Rule metadata
```

## API Reference

### Core AST Operations

#### create_ast_node

Creates a new AST node with specified properties.

```runa
Process called "create_ast_node" that takes 
    node_type as String 
    and value as Any 
    and children as List[ASTNode] 
    and position as Position 
    returns ASTNode
```

**Parameters:**
- `node_type`: The type identifier for the node
- `value`: The value associated with the node
- `children`: List of child nodes
- `position`: Source position information

**Returns:** A new ASTNode with the specified properties

**Example:**
```runa
Import "advanced/metaprogramming/ast_manipulation" as AST

Let pos be AST.Position with 
    line as 1 and column as 1 and offset as 0 and metadata as dictionary containing

Let literal_node be AST.create_ast_node with 
    node_type as "Literal" 
    and value as 42 
    and children as list containing 
    and position as pos
```

#### traverse_ast

Applies a visitor function to each node in the AST.

```runa
Process called "traverse_ast" that takes 
    node as ASTNode 
    and visitor as Function 
    returns None
```

**Parameters:**
- `node`: Root node to traverse from
- `visitor`: Function to apply to each node

**Example:**
```runa
Note: Count the number of literal nodes
Let literal_count be 0

Process called "count_literals" that takes node as AST.ASTNode returns None:
    If node.node_type is "Literal":
        Set literal_count to literal_count plus 1

AST.traverse_ast with node as my_ast and visitor as count_literals
Display "Found " plus literal_count plus " literal nodes"
```

#### transform_ast

Applies a transformation function to each node in the AST.

```runa
Process called "transform_ast" that takes 
    node as ASTNode 
    and transformer as Function 
    returns ASTNode
```

**Parameters:**
- `node`: Root node to transform
- `transformer`: Function that transforms each node

**Returns:** New AST with transformations applied

**Example:**
```runa
Note: Transform all string literals to uppercase
Process called "uppercase_strings" that takes node as AST.ASTNode returns AST.ASTNode:
    If node.node_type is "Literal" and node.value is String:
        Return AST.update_ast_node with 
            node as node 
            and value as node.value.to_uppercase()
    Return node

Let transformed_ast be AST.transform_ast with 
    node as original_ast 
    and transformer as uppercase_strings
```

### Pattern Matching and Rewriting

#### match_ast_pattern

Tests whether an AST node matches a specified pattern.

```runa
Process called "match_ast_pattern" that takes 
    node as ASTNode 
    and pattern as ASTPattern 
    returns Boolean
```

**Parameters:**
- `node`: AST node to test
- `pattern`: Pattern to match against

**Returns:** True if the node matches the pattern

**Example:**
```runa
Note: Create a pattern for binary addition
Let addition_pattern be AST.ASTPattern with 
    pattern_type as "BinaryOperation"
    and value as "plus"
    and children as list containing 
        AST.ASTPattern with pattern_type as "Literal" and value as None and children as list containing and metadata as dictionary containing,
        AST.ASTPattern with pattern_type as "Literal" and value as None and children as list containing and metadata as dictionary containing
    and metadata as dictionary containing

Note: Test if a node matches
Let matches be AST.match_ast_pattern with 
    node as my_node 
    and pattern as addition_pattern
```

#### rewrite_ast

Applies rewrite rules to transform an AST.

```runa
Process called "rewrite_ast" that takes 
    node as ASTNode 
    and rules as List[RewriteRule] 
    returns ASTNode
```

**Parameters:**
- `node`: AST node to rewrite
- `rules`: List of rewrite rules to apply

**Returns:** New AST with rules applied

**Example:**
```runa
Note: Create a rule to optimize addition by zero
Let zero_pattern be AST.ASTPattern with 
    pattern_type as "BinaryOperation"
    and value as "plus"
    and children as list containing 
        AST.ASTPattern with pattern_type as "Literal" and value as 0 and children as list containing and metadata as dictionary containing
    and metadata as dictionary containing

Let replacement be AST.create_ast_node with 
    node_type as "Literal" 
    and value as 0 
    and children as list containing 
    and position as create_default_position

Let optimization_rule be AST.RewriteRule with 
    rule_id as "eliminate_add_zero"
    and pattern as zero_pattern
    and replacement as replacement
    and conditions as list containing
    and metadata as dictionary containing

Let optimized_ast be AST.rewrite_ast with 
    node as my_ast 
    and rules as list containing optimization_rule
```

### Validation and Analysis

#### validate_ast

Validates the structural integrity of an AST.

```runa
Process called "validate_ast" that takes node as ASTNode returns Boolean
```

**Parameters:**
- `node`: AST node to validate

**Returns:** True if the AST is structurally valid

**Example:**
```runa
Let is_valid be AST.validate_ast with node as my_ast
If not is_valid:
    Display "AST validation failed"
```

#### diff_ast

Compares two AST structures and returns differences.

```runa
Process called "diff_ast" that takes 
    node1 as ASTNode 
    and node2 as ASTNode 
    returns ASTDiff
```

**Parameters:**
- `node1`: First AST to compare
- `node2`: Second AST to compare

**Returns:** ASTDiff containing all differences

**Example:**
```runa
Let differences be AST.diff_ast with node1 as original_ast and node2 as modified_ast
For each diff in differences.differences:
    Display "Difference: " plus diff.description
```

### Utility Functions

#### deep_copy_ast_node

Creates a deep copy of an AST node and all its children.

```runa
Process called "deep_copy_ast_node" that takes node as ASTNode returns ASTNode
```

**Example:**
```runa
Let ast_copy be AST.deep_copy_ast_node with node as original_ast
```

#### update_ast_node

Creates a new AST node with updated properties.

```runa
Process called "update_ast_node" that takes 
    node as ASTNode 
    and node_type as Optional[String] 
    and value as Optional[Any] 
    and children as Optional[List[ASTNode]] 
    and annotations as Optional[List[Annotation]] 
    and metadata as Optional[Dictionary[String, Any]] 
    returns ASTNode
```

**Example:**
```runa
Let updated_node be AST.update_ast_node with 
    node as original_node 
    and value as new_value 
    and metadata as new_metadata
```

## Usage Examples

### Basic AST Construction

```runa
Import "advanced/metaprogramming/ast_manipulation" as AST

Note: Create a simple let statement: Let x be 42
Let pos be AST.Position with line as 1 and column as 1 and offset as 0 and metadata as dictionary containing

Let literal_42 be AST.create_ast_node with 
    node_type as "Literal" 
    and value as 42 
    and children as list containing 
    and position as pos

Let let_statement be AST.create_ast_node with 
    node_type as "LetStatement" 
    and value as "x" 
    and children as list containing literal_42
    and position as pos

Display "Created AST for: Let x be 42"
```

### AST Transformation Pipeline

```runa
Note: Create a transformation pipeline
Process called "optimization_pipeline" that takes ast as AST.ASTNode returns AST.ASTNode:
    Note: Step 1: Constant folding
    Let folded be AST.transform_ast with node as ast and transformer as fold_constants
    
    Note: Step 2: Dead code elimination
    Let eliminated be AST.transform_ast with node as folded and transformer as eliminate_dead_code
    
    Note: Step 3: Common subexpression elimination
    Let optimized be AST.transform_ast with node as eliminated and transformer as eliminate_common_subexpressions
    
    Return optimized

Process called "fold_constants" that takes node as AST.ASTNode returns AST.ASTNode:
    If node.node_type is "BinaryOperation":
        If node.children[0].node_type is "Literal" and node.children[1].node_type is "Literal":
            Let left be node.children[0].value
            Let right be node.children[1].value
            If node.value is "plus":
                Return AST.create_ast_node with 
                    node_type as "Literal" 
                    and value as (left plus right) 
                    and children as list containing 
                    and position as node.position
            If node.value is "minus":
                Return AST.create_ast_node with 
                    node_type as "Literal" 
                    and value as (left minus right) 
                    and children as list containing 
                    and position as node.position
    Return node

Let optimized_ast be optimization_pipeline with ast as my_program_ast
```

### Pattern-Based Analysis

```runa
Note: Analyze function complexity
Process called "analyze_complexity" that takes ast as AST.ASTNode returns ComplexityReport:
    Let loop_count be 0
    Let condition_count be 0
    Let function_count be 0
    
    Process called "complexity_visitor" that takes node as AST.ASTNode returns None:
        If node.node_type is "ForEachStatement" or node.node_type is "WhileStatement":
            Set loop_count to loop_count plus 1
        If node.node_type is "IfStatement":
            Set condition_count to condition_count plus 1
        If node.node_type is "FunctionDefinition":
            Set function_count to function_count plus 1
    
    AST.traverse_ast with node as ast and visitor as complexity_visitor
    
    Let cyclomatic_complexity be 1 plus condition_count plus loop_count
    
    Return ComplexityReport with 
        loops as loop_count
        and conditions as condition_count
        and functions as function_count
        and cyclomatic_complexity as cyclomatic_complexity
        and metadata as dictionary containing

Let complexity be analyze_complexity with ast as my_code_ast
Display "Cyclomatic complexity: " plus complexity.cyclomatic_complexity
```

### AST Serialization and Comparison

```runa
Note: Serialize AST to JSON for storage
Process called "serialize_ast_to_json" that takes ast as AST.ASTNode returns String:
    Let json_obj be dictionary containing
    Set json_obj["node_type"] to ast.node_type
    Set json_obj["value"] to ast.value
    Set json_obj["position"] to serialize_position_to_json with position as ast.position
    Set json_obj["children"] to [serialize_ast_to_json with ast as child for each child in ast.children]
    Set json_obj["metadata"] to ast.metadata
    Return serialize_json with obj as json_obj

Note: Compare two versions of code
Let version1_ast be parse_code_to_ast with code as version1_code
Let version2_ast be parse_code_to_ast with code as version2_code
Let diff be AST.diff_ast with node1 as version1_ast and node2 as version2_ast

Display "Changes between versions:"
For each difference in diff.differences:
    Display "- " plus difference.description plus " at line " plus difference.node1.position.line
```

## Advanced Patterns

### Custom AST Visitors

```runa
Note: Create a sophisticated AST visitor for code metrics
Type called "CodeMetricsVisitor":
    metrics as CodeMetrics
    current_depth as Integer
    function_stack as List[String]
    
Type called "CodeMetrics":
    total_lines as Integer
    total_nodes as Integer
    max_depth as Integer
    function_count as Integer
    variable_count as Integer
    complexity_score as Float

Process called "create_metrics_visitor" returns CodeMetricsVisitor:
    Return CodeMetricsVisitor with 
        metrics as CodeMetrics with 
            total_lines as 0
            and total_nodes as 0
            and max_depth as 0
            and function_count as 0
            and variable_count as 0
            and complexity_score as 0.0
        and current_depth as 0
        and function_stack as list containing

Process called "visit_node" that takes visitor as CodeMetricsVisitor and node as AST.ASTNode returns None:
    Set visitor.metrics.total_nodes to visitor.metrics.total_nodes plus 1
    Set visitor.current_depth to visitor.current_depth plus 1
    
    If visitor.current_depth is greater than visitor.metrics.max_depth:
        Set visitor.metrics.max_depth to visitor.current_depth
    
    If node.node_type is "FunctionDefinition":
        Set visitor.metrics.function_count to visitor.metrics.function_count plus 1
        Add node.value to visitor.function_stack
        Set visitor.metrics.complexity_score to visitor.metrics.complexity_score plus calculate_function_complexity with node as node
    
    If node.node_type is "LetStatement":
        Set visitor.metrics.variable_count to visitor.metrics.variable_count plus 1
    
    Note: Visit children
    For each child in node.children:
        visit_node with visitor as visitor and node as child
    
    Set visitor.current_depth to visitor.current_depth minus 1
    
    If node.node_type is "FunctionDefinition":
        Remove last item from visitor.function_stack

Let metrics_visitor be create_metrics_visitor
visit_node with visitor as metrics_visitor and node as my_program_ast
Display "Code metrics: " plus metrics_visitor.metrics.total_nodes plus " nodes, " plus metrics_visitor.metrics.function_count plus " functions"
```

### AST-Based Code Generation

```runa
Note: Generate optimized code from AST
Process called "generate_optimized_code" that takes ast as AST.ASTNode returns String:
    Note: Apply optimizations first
    Let optimized_ast be optimization_pipeline with ast as ast
    
    Note: Generate code with proper formatting
    Return emit_formatted_code with ast as optimized_ast and indent_level as 0

Process called "emit_formatted_code" that takes ast as AST.ASTNode and indent_level as Integer returns String:
    Let indent be "    " multiplied by indent_level
    
    If ast.node_type is "Program":
        Let lines be list containing
        For each child in ast.children:
            Let child_code be emit_formatted_code with ast as child and indent_level as indent_level
            Add child_code to lines
        Return join with separator as "\n" and items as lines
    
    If ast.node_type is "LetStatement":
        Return indent plus "Let " plus ast.value plus " be " plus emit_formatted_code with ast as ast.children[0] and indent_level as 0
    
    If ast.node_type is "IfStatement":
        Let condition_code be emit_formatted_code with ast as ast.children[0] and indent_level as 0
        Let then_code be emit_formatted_code with ast as ast.children[1] and indent_level as (indent_level plus 1)
        Let result be indent plus "If " plus condition_code plus ":\n" plus then_code
        If length of ast.children is greater than 2:
            Let else_code be emit_formatted_code with ast as ast.children[2] and indent_level as (indent_level plus 1)
            Set result to result plus "\nOtherwise:\n" plus else_code
        Return result
    
    If ast.node_type is "Literal":
        Return to_string with value as ast.value
    
    If ast.node_type is "Identifier":
        Return ast.value
    
    Return "Note: Unsupported node type: " plus ast.node_type

Let generated_code be generate_optimized_code with ast as my_ast
Display "Generated code:"
Display generated_code
```

## Performance Considerations

### Memory Usage

- **Immutable Operations**: All AST operations create new nodes rather than modifying existing ones
- **Memory Pooling**: Consider using object pools for frequently created nodes
- **Lazy Evaluation**: Use lazy evaluation for expensive transformations

### Time Complexity

- **Traversal**: O(n) where n is the number of nodes
- **Transformation**: O(n) for most transformations
- **Pattern Matching**: O(k*n) where k is the complexity of the pattern
- **Deep Copy**: O(n) time and space

### Optimization Strategies

```runa
Note: Optimize AST operations for large trees
Process called "optimized_transform" that takes ast as AST.ASTNode and transformer as Function returns AST.ASTNode:
    Note: Use caching for repeated transformations
    Let cache be dictionary containing
    
    Process called "cached_transformer" that takes node as AST.ASTNode returns AST.ASTNode:
        Let node_key be compute_node_hash with node as node
        If node_key in cache:
            Return cache[node_key]
        
        Let result be transformer with node as node
        Set cache[node_key] to result
        Return result
    
    Return AST.transform_ast with node as ast and transformer as cached_transformer

Note: Use parallel processing for independent transformations
Process called "parallel_transform" that takes ast as AST.ASTNode and transformer as Function returns AST.ASTNode:
    If ast.children is empty:
        Return transformer with node as ast
    
    Note: Transform children in parallel
    Let child_futures be list containing
    For each child in ast.children:
        Add async_transform with ast as child and transformer as transformer to child_futures
    
    Let transformed_children be list containing
    For each future in child_futures:
        Add await future to transformed_children
    
    Let result be transformer with node as ast
    Return AST.update_ast_node with node as result and children as transformed_children
```

## Best Practices

### 1. Immutability

Always prefer immutable operations to maintain AST integrity:

```runa
Note: Good: Create new node
Let updated_node be AST.update_ast_node with node as original and value as new_value

Note: Avoid: Modifying node in place (not possible in Runa's design)
```

### 2. Position Preservation

Always preserve position information for debugging:

```runa
Process called "transform_with_position" that takes node as AST.ASTNode returns AST.ASTNode:
    Let transformed be apply_transformation with node as node
    Return AST.update_ast_node with 
        node as transformed 
        and position as node.position  Note: Preserve original position
```

### 3. Validation

Validate ASTs after complex transformations:

```runa
Let transformed_ast be complex_transformation with ast as original_ast
If not AST.validate_ast with node as transformed_ast:
    Raise AST.ASTValidationError with message as "Transformation produced invalid AST"
```

### 4. Error Handling

Implement robust error handling for AST operations:

```runa
Process called "safe_transform" that takes ast as AST.ASTNode and transformer as Function returns AST.ASTNode:
    Try:
        Let result be AST.transform_ast with node as ast and transformer as transformer
        If AST.validate_ast with node as result:
            Return result
        Else:
            Display "Warning: Transformation produced invalid AST, returning original"
            Return ast
    Catch error:
        Display "Error during transformation: " plus error.message
        Return ast
```

### 5. Performance Monitoring

Monitor performance for large AST operations:

```runa
Process called "monitored_transform" that takes ast as AST.ASTNode and transformer as Function returns AST.ASTNode:
    Let start_time be get_current_time
    Let node_count be count_nodes with ast as ast
    
    Let result be AST.transform_ast with node as ast and transformer as transformer
    
    Let end_time be get_current_time
    Let duration be end_time minus start_time
    
    Display "Transformed " plus node_count plus " nodes in " plus duration plus "ms"
    Return result
```

The AST Manipulation module provides the foundation for all metaprogramming operations in Runa. Its powerful yet simple API enables sophisticated code analysis and transformation while maintaining type safety and performance.