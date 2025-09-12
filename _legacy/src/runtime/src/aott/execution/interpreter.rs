//! Tier 0: Lightning Interpreter
//! 
//! Zero-cost startup interpreter with ML profiling for immediate code execution.
//! This tier provides instant startup with no compilation overhead while collecting
//! minimal ML profiling data to guide AOTT tier promotion decisions.

use super::{ExecutionEngine, ExecutionContext, FunctionMetadata};
use crate::aott::types::*;
use runa_common::bytecode::{Value};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::time::{Instant, Duration};

// =============================================================================
// Compiler AST Structures (Rust equivalents of compiler/parser/ast.runa)
// =============================================================================

/// Expression AST nodes from the compiler with location tracking
#[derive(Debug, Clone, PartialEq)]
pub enum Expression {
    Literal { value: Value, literal_type: String },
    Identifier { name: String, is_qualified: bool },
    BinaryOperation { left: Box<Expression>, operator: String, right: Box<Expression> },
    UnaryOperation { operator: String, operand: Box<Expression> },
    FunctionCall { function: Box<Expression>, arguments: Vec<Expression> },
    MethodCall { object: Box<Expression>, method: String, arguments: Vec<Expression> },
    IndexAccess { array: Box<Expression>, index: Box<Expression> },
    FieldAccess { object: Box<Expression>, field: String },
    ParenthesizedExpression { expression: Box<Expression> },
    ListLiteral { elements: Vec<Expression> },
    DictionaryLiteral { keys: Vec<Expression>, values: Vec<Expression> },
    ConditionalExpression { condition: Box<Expression>, then_expr: Box<Expression>, else_expr: Box<Expression> },
    LambdaExpression { parameters: Vec<Parameter>, body: Box<Expression> },
}

/// Statement AST nodes from the compiler  
#[derive(Debug, Clone, PartialEq)]
pub enum Statement {
    ExpressionStatement { expression: Expression },
    VariableDeclaration { name: String, value: Expression, type_annotation: Option<String> },
    Assignment { target: Expression, value: Expression },
    IfStatement { condition: Expression, then_body: Vec<Statement>, else_body: Vec<Statement> },
    ForLoop { variable: String, iterable: Expression, body: Vec<Statement> },
    WhileLoop { condition: Expression, body: Vec<Statement> },
    BreakStatement,
    ContinueStatement,
    ReturnStatement { value: Option<Expression> },
    ImportStatement { module: String, alias: Option<String> },
    PassStatement,
}

/// Program is a list of statements
pub type Program = Vec<Statement>;

/// Parameter for function definitions
#[derive(Debug, Clone, PartialEq)]
pub struct Parameter {
    pub name: String,
    pub param_type: Option<String>,
    pub default_value: Option<Expression>,
}

/// Source location for tracking line numbers and positions
#[derive(Debug, Clone, PartialEq)]
pub struct SourceLocation {
    pub line: usize,
    pub column: usize,
    pub file: String,
}

impl Default for SourceLocation {
    fn default() -> Self {
        Self {
            line: 1,
            column: 1,
            file: "<unknown>".to_string(),
        }
    }
}

/// Lambda closure with captured scope and execution context
#[derive(Debug, Clone, PartialEq)]
pub struct LambdaClosure {
    pub parameters: Vec<Parameter>,
    pub body: Expression,
    pub captured_scope: HashMap<String, Value>,
}

/// Configuration for execution limits and security boundaries
#[derive(Debug, Clone)]
pub struct ExecutionConfig {
    /// Maximum iterations for a single loop before requiring progress check
    pub max_loop_iterations_before_check: u32,
    /// Maximum total iterations allowed for any loop
    pub max_total_loop_iterations: u32,
    /// Maximum execution time for any single operation (in milliseconds)
    pub max_execution_time_ms: u64,
    /// Maximum memory usage allowed (in bytes)
    pub max_memory_usage: u64,
    /// Enable intelligent infinite loop detection
    pub enable_smart_loop_detection: bool,
}

impl Default for ExecutionConfig {
    fn default() -> Self {
        Self {
            max_loop_iterations_before_check: 1000,
            max_total_loop_iterations: 1_000_000,
            max_execution_time_ms: 30_000, // 30 seconds
            max_memory_usage: 1_024_000_000, // 1GB
            enable_smart_loop_detection: true,
        }
    }
}

/// Control flow instructions for proper loop and function control
#[derive(Debug, Clone, PartialEq)]
pub enum ControlFlow {
    None,
    Break,
    Continue,
    Return(Value),
}

/// Extended result type that handles both values and control flow
pub type ControlResult<T> = Result<(T, ControlFlow), CompilerError>;

/// Real-time memory tracking for accurate profiling
#[derive(Debug)]
pub struct MemoryTracker {
    /// Total allocations made
    pub total_allocations: u64,
    /// Total deallocations made
    pub total_deallocations: u64,
    /// Peak memory usage observed
    pub peak_usage: u64,
    /// Current memory usage
    pub current_usage: u64,
    /// Memory usage history for trend analysis
    pub usage_history: Vec<(std::time::Instant, u64)>,
    /// Allocation size tracking
    pub allocation_sizes: std::collections::HashMap<String, u64>,
}

impl MemoryTracker {
    pub fn new() -> Self {
        Self {
            total_allocations: 0,
            total_deallocations: 0,
            peak_usage: 0,
            current_usage: 0,
            usage_history: Vec::new(),
            allocation_sizes: std::collections::HashMap::new(),
        }
    }
    
    /// Record a memory allocation
    pub fn allocate(&mut self, category: &str, size: u64) {
        self.total_allocations += 1;
        self.current_usage += size;
        
        // Update peak usage
        if self.current_usage > self.peak_usage {
            self.peak_usage = self.current_usage;
        }
        
        // Track allocation by category
        *self.allocation_sizes.entry(category.to_string()).or_insert(0) += size;
        
        // Record usage history (keep only recent entries)
        self.usage_history.push((std::time::Instant::now(), self.current_usage));
        if self.usage_history.len() > 1000 {
            self.usage_history.drain(0..500); // Keep recent 500 entries
        }
    }
    
    /// Record a memory deallocation
    pub fn deallocate(&mut self, category: &str, size: u64) {
        self.total_deallocations += 1;
        self.current_usage = self.current_usage.saturating_sub(size);
        
        // Update allocation tracking
        if let Some(category_size) = self.allocation_sizes.get_mut(category) {
            *category_size = category_size.saturating_sub(size);
        }
    }
    
    /// Calculate actual memory usage of a Value
    pub fn calculate_value_size(value: &Value) -> u64 {
        match value {
            Value::Integer(_) => 8,
            Value::Float(_) => 8,
            Value::Boolean(_) => 1,
            Value::String(s) => 24 + s.len() as u64, // String header + bytes
            Value::List(items) => {
                let base_size = 24; // Vec header
                let items_size: u64 = items.iter()
                    .map(Self::calculate_value_size)
                    .sum();
                base_size + items_size
            },
            Value::Dictionary(dict) => {
                let base_size = 48; // HashMap header estimate
                let entries_size: u64 = dict.iter()
                    .map(|(k, v)| Self::calculate_value_size(k) + Self::calculate_value_size(v))
                    .sum();
                base_size + entries_size
            },
            Value::Function(_) => 128, // Function object estimate
            Value::NativeFunction(_) => 16, // Function pointer
            Value::Null | Value::Nil => 0,
            Value::Number(_) => 8,
            _ => 64, // Default estimate for unknown types
        }
    }
    
    /// Get current memory statistics
    pub fn get_stats(&self) -> MemoryStats {
        MemoryStats {
            total_allocations: self.total_allocations,
            total_deallocations: self.total_deallocations,
            peak_usage: self.peak_usage,
            current_usage: self.current_usage,
            allocation_efficiency: if self.total_allocations > 0 {
                self.total_deallocations as f64 / self.total_allocations as f64
            } else {
                0.0
            },
        }
    }
}

/// Memory usage statistics
#[derive(Debug, Clone)]
pub struct MemoryStats {
    pub total_allocations: u64,
    pub total_deallocations: u64,
    pub peak_usage: u64,
    pub current_usage: u64,
    pub allocation_efficiency: f64,
}

// =============================================================================
// ML Profiling Structures (Minimal overhead for AOTT)
// =============================================================================

/// Minimal ML profiler for AOTT tier promotion decisions
#[derive(Debug)]
pub struct MLProfiler {
    /// Branch pattern tracking: line -> (taken_count, not_taken_count)
    pub branch_patterns: HashMap<usize, (u32, u32)>,
    /// Loop iteration tracking: line -> [iteration_counts]  
    pub loop_iterations: HashMap<usize, Vec<u32>>,
    /// Function call frequency for promotion
    pub function_calls: HashMap<String, u32>,
    /// Total execution time for performance metrics
    pub total_execution_time: Duration,
}

impl MLProfiler {
    pub fn new() -> Self {
        Self {
            branch_patterns: HashMap::new(),
            loop_iterations: HashMap::new(), 
            function_calls: HashMap::new(),
            total_execution_time: Duration::default(),
        }
    }
    
    /// Record branch taken/not taken for ML optimization
    pub fn record_branch(&mut self, line: usize, taken: bool) {
        let entry = self.branch_patterns.entry(line).or_insert((0, 0));
        if taken { entry.0 += 1; } else { entry.1 += 1; }
    }
    
    /// Record loop iteration count for vectorization hints
    pub fn record_loop_iterations(&mut self, line: usize, iterations: u32) {
        self.loop_iterations.entry(line).or_insert_with(Vec::new).push(iterations);
        // Keep only recent data to avoid memory bloat
        if let Some(vec) = self.loop_iterations.get_mut(&line) {
            if vec.len() > 100 { vec.drain(0..50); }
        }
    }
    
    /// Record function call for promotion decisions
    pub fn record_function_call(&mut self, function_name: &str) {
        *self.function_calls.entry(function_name.to_string()).or_insert(0) += 1;
    }
}

/// Tier 0: Lightning Interpreter with zero-cost startup and ML profiling
#[derive(Debug)]
pub struct LightningInterpreter {
    /// Call frequency tracking for promotion decisions
    pub call_tracker: CallFrequencyTracker,
    /// Minimal ML profiling for AOTT optimization hints
    pub ml_profiler: MLProfiler,
    /// Variables environment for execution
    pub variables: HashMap<String, Value>,
    /// Import environment for stdlib access
    pub imports: HashMap<String, String>,
    /// Function registry for metadata
    pub function_registry: Arc<RwLock<HashMap<FunctionId, FunctionMetadata>>>,
    /// Lambda closure registry for complete closure execution
    pub lambda_registry: HashMap<String, LambdaClosure>,
    /// Current execution line for accurate ML profiling
    pub current_line: usize,
    /// Source file being executed
    pub current_file: String,
    /// Configurable execution limits for security and performance
    pub execution_config: ExecutionConfig,
    /// Real memory usage tracker for accurate ML profiling
    pub memory_tracker: MemoryTracker,
}

impl LightningInterpreter {
    pub fn new() -> Self {
        let mut imports = HashMap::new();
        // Pre-load common stdlib modules for fast access
        imports.insert("builtins".to_string(), "builtins".to_string());
        imports.insert("math".to_string(), "math/core".to_string());
        imports.insert("collections".to_string(), "collections".to_string());
        imports.insert("string".to_string(), "string".to_string());
        
        Self {
            call_tracker: CallFrequencyTracker::new(),
            ml_profiler: MLProfiler::new(),
            variables: HashMap::new(),
            imports,
            function_registry: Arc::new(RwLock::new(HashMap::new())),
            lambda_registry: HashMap::new(),
            current_line: 1,
            current_file: "<main>".to_string(),
            execution_config: ExecutionConfig::default(),
            memory_tracker: MemoryTracker::new(),
        }
    }
    
    /// Execute program with minimal ML profiling
    pub fn execute_program(&mut self, program: &Program, args: Vec<Value>) -> CompilerResult<Value> {
        let start_time = Instant::now();
        
        // Initialize arguments in variable environment
        for (i, arg) in args.iter().enumerate() {
            self.variables.insert(format!("arg_{}", i), arg.clone());
        }
        
        // Execute all statements with proper line tracking and control flow
        let mut result = Value::Null;
        for statement in program {
            let (stmt_result, control_flow) = self.execute_statement(statement, self.current_line)?;
            result = stmt_result;
            
            // Handle control flow at program level
            match control_flow {
                ControlFlow::Return(value) => {
                    result = value;
                    break; // Exit program execution
                },
                ControlFlow::Break | ControlFlow::Continue => {
                    // Break/Continue at program level is an error (not in loop context)
                    return Err(CompilerError::ExecutionFailed(
                        "Break/Continue statements can only be used inside loops".to_string()
                    ));
                },
                ControlFlow::None => {}
            }
            
            self.current_line += 1; // Increment line for each statement
        }
        
        // Record total execution time for ML profiling
        let execution_time = start_time.elapsed();
        self.ml_profiler.total_execution_time += execution_time;
        
        Ok(result)
    }
    
    /// Execute a statement with ML profiling and control flow support
    fn execute_statement(&mut self, statement: &Statement, line: usize) -> ControlResult<Value> {
        match statement {
            Statement::ExpressionStatement { expression } => {
                let result = self.evaluate_expression(expression, line)?;
                Ok((result, ControlFlow::None))
            },
            Statement::VariableDeclaration { name, value, .. } => {
                let val = self.evaluate_expression(value, line)?;
                
                // Track memory allocation for new variable
                let value_size = MemoryTracker::calculate_value_size(&val);
                self.memory_tracker.allocate("variables", value_size);
                
                // Store the value in variables environment
                // This supports storing functions as first-class values
                self.variables.insert(name.clone(), val.clone());
                
                // Record if we're storing a function for ML profiling
                if matches!(val, Value::Function(_) | Value::NativeFunction(_)) {
                    self.ml_profiler.record_function_call(&format!("define_{}", name));
                }
                
                Ok((val, ControlFlow::None))
            },
            Statement::Assignment { target, value } => {
                let val = self.evaluate_expression(value, line)?;
                // For simplicity, only handle identifier assignments
                if let Expression::Identifier { name, .. } = target {
                    // Track memory changes for assignment
                    if let Some(old_value) = self.variables.get(name) {
                        let old_size = MemoryTracker::calculate_value_size(old_value);
                        self.memory_tracker.deallocate("variables", old_size);
                    }
                    
                    let new_size = MemoryTracker::calculate_value_size(&val);
                    self.memory_tracker.allocate("variables", new_size);
                    
                    self.variables.insert(name.clone(), val.clone());
                }
                Ok((val, ControlFlow::None))
            },
            Statement::IfStatement { condition, then_body, else_body } => {
                let condition_val = self.evaluate_expression(condition, line)?;
                let taken = self.is_truthy(&condition_val);
                
                // Record branch pattern for ML profiling
                self.ml_profiler.record_branch(line, taken);
                
                if taken {
                    self.execute_block(then_body, line)
                } else {
                    self.execute_block(else_body, line)
                }
            },
            Statement::WhileLoop { condition, body } => {
                let mut result = Value::Null;
                let mut iterations = 0u32;
                let loop_start_time = std::time::Instant::now();
                let mut last_progress_check = std::time::Instant::now();
                let mut stagnation_detector = LoopProgressDetector::new();
                
                loop {
                    // Evaluate loop condition
                    let condition_val = self.evaluate_expression(condition, line)?;
                    if !self.is_truthy(&condition_val) {
                        break;
                    }
                    
                    iterations += 1;
                    
                    // Check for execution timeout
                    if loop_start_time.elapsed().as_millis() > self.execution_config.max_execution_time_ms as u128 {
                        return Err(CompilerError::ExecutionFailed(
                            format!("Loop execution timeout after {} ms", self.execution_config.max_execution_time_ms)
                        ));
                    }
                    
                    // Check iteration limits with progressive checking
                    if iterations > self.execution_config.max_total_loop_iterations {
                        return Err(CompilerError::ExecutionFailed(
                            format!("Loop exceeded maximum iterations: {}", self.execution_config.max_total_loop_iterations)
                        ));
                    }
                    
                    // Smart infinite loop detection
                    if self.execution_config.enable_smart_loop_detection 
                       && iterations % self.execution_config.max_loop_iterations_before_check == 0 {
                        
                        // Check if we're making progress
                        let current_state = self.capture_loop_state();
                        if stagnation_detector.is_stagnant(&current_state) {
                            return Err(CompilerError::ExecutionFailed(
                                "Infinite loop detected: no progress in loop state".to_string()
                            ));
                        }
                        stagnation_detector.record_state(current_state);
                        last_progress_check = std::time::Instant::now();
                    }
                    
                    // Execute loop body with control flow handling
                    let (block_result, control_flow) = self.execute_block(body, line)?;
                    result = block_result;
                    
                    // Handle control flow statements
                    match control_flow {
                        ControlFlow::Break => break,
                        ControlFlow::Continue => continue,
                        ControlFlow::Return(value) => {
                            return Ok((value, ControlFlow::Return(value)));
                        },
                        ControlFlow::None => {}
                    }
                }
                
                // Record loop iterations for ML profiling
                if iterations > 0 {
                    self.ml_profiler.record_loop_iterations(line, iterations);
                }
                
                Ok((result, ControlFlow::None))
            },
            Statement::ForLoop { variable, iterable, body } => {
                let iterable_val = self.evaluate_expression(iterable, line)?;
                let mut result = Value::Null;
                let mut iterations = 0u32;
                
                // Simple iteration for lists with control flow support
                if let Value::List(items) = iterable_val {
                    for item in items {
                        self.variables.insert(variable.clone(), item);
                        let (block_result, control_flow) = self.execute_block(body, line)?;
                        result = block_result;
                        iterations += 1;
                        
                        // Handle control flow statements
                        match control_flow {
                            ControlFlow::Break => break,
                            ControlFlow::Continue => continue,
                            ControlFlow::Return(value) => {
                                return Ok((value, ControlFlow::Return(value)));
                            },
                            ControlFlow::None => {}
                        }
                    }
                }
                
                // Record loop iterations for ML profiling
                if iterations > 0 {
                    self.ml_profiler.record_loop_iterations(line, iterations);
                }
                
                Ok((result, ControlFlow::None))
            },
            Statement::ReturnStatement { value } => {
                if let Some(expr) = value {
                    let result = self.evaluate_expression(expr, line)?;
                    Ok((result.clone(), ControlFlow::Return(result)))
                } else {
                    Ok((Value::Null, ControlFlow::Return(Value::Null)))
                }
            },
            Statement::ImportStatement { module, alias } => {
                let module_name = alias.as_ref().unwrap_or(module);
                self.imports.insert(module_name.clone(), module.clone());
                Ok((Value::Null, ControlFlow::None))
            },
            Statement::BreakStatement => {
                Ok((Value::Null, ControlFlow::Break))
            },
            Statement::ContinueStatement => {
                Ok((Value::Null, ControlFlow::Continue))
            },
            Statement::PassStatement => {
                Ok((Value::Null, ControlFlow::None))
            },
        }
    }
    
    /// Execute a block of statements with control flow support
    fn execute_block(&mut self, statements: &[Statement], line: usize) -> ControlResult<Value> {
        let mut result = Value::Null;
        
        for statement in statements {
            let (stmt_result, control_flow) = self.execute_statement(statement, line)?;
            result = stmt_result;
            
            // Handle control flow - break out of block if needed
            match control_flow {
                ControlFlow::Break | ControlFlow::Continue | ControlFlow::Return(_) => {
                    return Ok((result, control_flow));
                },
                ControlFlow::None => continue,
            }
        }
        
        Ok((result, ControlFlow::None))
    }
    
    /// Execute binary operations
    fn execute_binary_operation(&self, left: &Value, op: &str, right: &Value) -> CompilerResult<Value> {
        match (left, right) {
            (Value::Integer(a), Value::Integer(b)) => {
                match op {
                    "+" => Ok(Value::Integer(a + b)),
                    "-" => Ok(Value::Integer(a - b)),
                    "*" => Ok(Value::Integer(a * b)),
                    "/" => {
                        if *b == 0 {
                            Err(CompilerError::ExecutionFailed("Division by zero".to_string()))
                        } else {
                            Ok(Value::Integer(a / b))
                        }
                    },
                    "%" => Ok(Value::Integer(a % b)),
                    "==" => Ok(Value::Boolean(a == b)),
                    "!=" => Ok(Value::Boolean(a != b)),
                    "<" => Ok(Value::Boolean(a < b)),
                    "<=" => Ok(Value::Boolean(a <= b)),
                    ">" => Ok(Value::Boolean(a > b)),
                    ">=" => Ok(Value::Boolean(a >= b)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported integer operation: {}", op))),
                }
            },
            (Value::Float(a), Value::Float(b)) => {
                match op {
                    "+" => Ok(Value::Float(a + b)),
                    "-" => Ok(Value::Float(a - b)),
                    "*" => Ok(Value::Float(a * b)),
                    "/" => Ok(Value::Float(a / b)),
                    "==" => Ok(Value::Boolean((a - b).abs() < f64::EPSILON)),
                    "!=" => Ok(Value::Boolean((a - b).abs() >= f64::EPSILON)),
                    "<" => Ok(Value::Boolean(a < b)),
                    "<=" => Ok(Value::Boolean(a <= b)),
                    ">" => Ok(Value::Boolean(a > b)),
                    ">=" => Ok(Value::Boolean(a >= b)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported float operation: {}", op))),
                }
            },
            (Value::String(a), Value::String(b)) => {
                match op {
                    "+" => Ok(Value::String(format!("{}{}", a, b))),
                    "==" => Ok(Value::Boolean(a == b)),
                    "!=" => Ok(Value::Boolean(a != b)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported string operation: {}", op))),
                }
            },
            (Value::Boolean(a), Value::Boolean(b)) => {
                match op {
                    "&&" => Ok(Value::Boolean(*a && *b)),
                    "||" => Ok(Value::Boolean(*a || *b)),
                    "==" => Ok(Value::Boolean(a == b)),
                    "!=" => Ok(Value::Boolean(a != b)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported boolean operation: {}", op))),
                }
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Type mismatch in binary operation: {} {} {}", 
                self.value_type(left), op, self.value_type(right)))),
        }
    }
    
    /// Execute unary operations
    fn execute_unary_operation(&self, op: &str, operand: &Value) -> CompilerResult<Value> {
        match operand {
            Value::Integer(n) => {
                match op {
                    "-" => Ok(Value::Integer(-n)),
                    "+" => Ok(Value::Integer(*n)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported integer unary operation: {}", op))),
                }
            },
            Value::Float(n) => {
                match op {
                    "-" => Ok(Value::Float(-n)),
                    "+" => Ok(Value::Float(*n)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported float unary operation: {}", op))),
                }
            },
            Value::Boolean(b) => {
                match op {
                    "!" => Ok(Value::Boolean(!b)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Unsupported boolean unary operation: {}", op))),
                }
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Unsupported unary operation: {} on {}", op, self.value_type(operand)))),
        }
    }
    
    /// Evaluate expression with compiler AST
    fn evaluate_expression(&mut self, expression: &Expression, line: usize) -> CompilerResult<Value> {
        match expression {
            Expression::Literal { value, .. } => Ok(value.clone()),
            Expression::Identifier { name, .. } => {
                // First check if it's a variable
                if let Some(value) = self.variables.get(name) {
                    Ok(value.clone())
                } else {
                    // Check if it's a built-in function name or stdlib function
                    match name.as_str() {
                        "print" | "len" | "typeof" => {
                            // Return function name as string for later resolution
                            Ok(Value::String(name.clone()))
                        },
                        _ => {
                            // Check if it's a function stored in variables
                            Err(CompilerError::ExecutionFailed(format!("Undefined variable: {}", name)))
                        }
                    }
                }
            },
            Expression::BinaryOperation { left, operator, right } => {
                let left_val = self.evaluate_expression(left, line)?;
                let right_val = self.evaluate_expression(right, line)?;
                self.execute_binary_operation(&left_val, operator, &right_val)
            },
            Expression::UnaryOperation { operator, operand } => {
                let operand_val = self.evaluate_expression(operand, line)?;
                self.execute_unary_operation(operator, &operand_val)
            },
            Expression::FunctionCall { function, arguments } => {
                let args: Result<Vec<Value>, _> = arguments.iter()
                    .map(|arg| self.evaluate_expression(arg, line))
                    .collect();
                let args = args?;
                
                // Evaluate the function expression to get the callable
                let function_value = self.evaluate_expression(function, line)?;
                
                match function_value {
                    Value::Function(func) => {
                        // Call user-defined function
                        self.call_user_function(&func, args)
                    },
                    Value::NativeFunction(native_fn) => {
                        // Call native function
                        native_fn(&args).map_err(|e| CompilerError::ExecutionFailed(e))
                    },
                    Value::String(name) => {
                        // Function name as string - call stdlib function
                        self.ml_profiler.record_function_call(&name);
                        self.call_stdlib_function(&name, args)
                    },
                    _ => {
                        // Check if function expression was an identifier that resolves to a function name
                        if let Expression::Identifier { name, .. } = function.as_ref() {
                            // Record function call for ML profiling
                            self.ml_profiler.record_function_call(name);
                            
                            // Call stdlib function by name
                            self.call_stdlib_function(name, args)
                        } else {
                            Err(CompilerError::ExecutionFailed(format!("Cannot call non-function value: {}", self.value_type(&function_value))))
                        }
                    }
                }
            },
            Expression::MethodCall { object, method, arguments } => {
                let object_val = self.evaluate_expression(object, line)?;
                let args: Result<Vec<Value>, _> = arguments.iter()
                    .map(|arg| self.evaluate_expression(arg, line))
                    .collect();
                let args = args?;
                
                self.call_method(&object_val, method, args)
            },
            Expression::IndexAccess { array, index } => {
                let array_val = self.evaluate_expression(array, line)?;
                let index_val = self.evaluate_expression(index, line)?;
                
                match (&array_val, &index_val) {
                    (Value::List(items), Value::Integer(idx)) => {
                        let idx = *idx as usize;
                        items.get(idx)
                            .cloned()
                            .ok_or_else(|| CompilerError::ExecutionFailed("Index out of bounds".to_string()))
                    },
                    _ => Err(CompilerError::ExecutionFailed("Invalid index access".to_string()))
                }
            },
            Expression::FieldAccess { object, field } => {
                let object_val = self.evaluate_expression(object, line)?;
                self.access_field(&object_val, field)
            },
            Expression::ParenthesizedExpression { expression } => {
                self.evaluate_expression(expression, line)
            },
            Expression::ListLiteral { elements } => {
                let values: Result<Vec<Value>, _> = elements.iter()
                    .map(|elem| self.evaluate_expression(elem, line))
                    .collect();
                let list = Value::List(values?);
                
                // Track memory allocation for list creation
                let list_size = MemoryTracker::calculate_value_size(&list);
                self.memory_tracker.allocate("collections", list_size);
                
                Ok(list)
            },
            Expression::DictionaryLiteral { keys, values } => {
                if keys.len() != values.len() {
                    return Err(CompilerError::ExecutionFailed("Dictionary keys and values length mismatch".to_string()));
                }
                
                let mut dict = Vec::new();
                for (key_expr, value_expr) in keys.iter().zip(values.iter()) {
                    let key = self.evaluate_expression(key_expr, line)?;
                    let value = self.evaluate_expression(value_expr, line)?;
                    dict.push((key, value));
                }
                let dictionary = Value::Dictionary(dict);
                
                // Track memory allocation for dictionary creation
                let dict_size = MemoryTracker::calculate_value_size(&dictionary);
                self.memory_tracker.allocate("collections", dict_size);
                
                Ok(dictionary)
            },
            Expression::ConditionalExpression { condition, then_expr, else_expr } => {
                let condition_val = self.evaluate_expression(condition, line)?;
                
                if self.is_truthy(&condition_val) {
                    self.evaluate_expression(then_expr, line)
                } else {
                    self.evaluate_expression(else_expr, line)
                }
            },
            Expression::LambdaExpression { parameters, body } => {
                // Create a function value from the lambda expression
                self.create_lambda_function(parameters, body)
            },
        }
    }
    
    /// Call user-defined function with complete closure support
    fn call_user_function(&mut self, func: &runa_common::bytecode::Function, args: Vec<Value>) -> CompilerResult<Value> {
        // Verify argument count matches function arity
        if args.len() != func.arity {
            return Err(CompilerError::ExecutionFailed(
                format!("Function '{}' expects {} arguments, got {}", 
                    func.name, func.arity, args.len())
            ));
        }
        
        // Check if this is a lambda function
        if let Some(lambda_closure) = self.lambda_registry.get(&func.name).cloned() {
            return self.execute_lambda_closure(&lambda_closure, args);
        }
        
        // Handle native functions
        if func.is_native {
            if let Some(native_fn) = func.native_fn {
                return native_fn(&args).map_err(|e| CompilerError::ExecutionFailed(e));
            } else {
                return Err(CompilerError::ExecutionFailed("Native function missing implementation".to_string()));
            }
        }
        
        // Handle regular user-defined functions with bytecode execution
        self.execute_bytecode_function(func, args)
    }
    
    /// Execute lambda closure with proper scope and parameter binding
    fn execute_lambda_closure(&mut self, closure: &LambdaClosure, args: Vec<Value>) -> CompilerResult<Value> {
        // Save current variable environment
        let saved_variables = self.variables.clone();
        
        // Restore captured scope
        self.variables = closure.captured_scope.clone();
        
        // Bind arguments to parameters
        for (i, (param, arg)) in closure.parameters.iter().zip(args.iter()).enumerate() {
            self.variables.insert(param.name.clone(), arg.clone());
        }
        
        // Execute the lambda body with proper line tracking
        let result = self.evaluate_expression(&closure.body, self.current_line);
        
        // Restore original variable environment
        self.variables = saved_variables;
        
        result
    }
    
    /// Execute bytecode function (for compiled user functions)
    fn execute_bytecode_function(&mut self, func: &runa_common::bytecode::Function, args: Vec<Value>) -> CompilerResult<Value> {
        // Create function execution scope
        let saved_variables = self.variables.clone();
        
        // Bind arguments to parameters (using standard parameter naming)
        for (i, arg) in args.iter().enumerate() {
            let param_name = format!("param_{}", i);
            self.variables.insert(param_name, arg.clone());
        }
        
        // Execute the function's bytecode using the T1 Smart Bytecode engine
        let result = self.execute_chunk_with_context(&func.chunk);
        
        // Restore original scope
        self.variables = saved_variables;
        
        result
    }
    
    /// Execute bytecode chunk with current interpreter context
    fn execute_chunk_with_context(&mut self, chunk: &runa_common::bytecode::Chunk) -> CompilerResult<Value> {
        // Create T1 Bytecode interpreter for function body execution
        use crate::aott::execution::bytecode::BytecodeInterpreter;
        
        let mut bytecode_interpreter = BytecodeInterpreter::new();
        
        // Transfer current variable state to bytecode interpreter globals
        for (name, value) in &self.variables {
            bytecode_interpreter.global_variables.insert(name.clone(), value.clone());
        }
        
        // Execute the bytecode chunk directly with empty args
        let result = bytecode_interpreter.execute(chunk, vec![])
            .map_err(|e| CompilerError::ExecutionFailed(format!("Bytecode execution failed: {}", e)))?;
        
        // Transfer any variable changes back to interpreter
        for (name, value) in bytecode_interpreter.global_variables {
            self.variables.insert(name, value);
        }
        
        Ok(result)
    }
    
    /// Create a function value from lambda expression with complete closure support
    fn create_lambda_function(&mut self, parameters: &[Parameter], body: &Expression) -> CompilerResult<Value> {
        // Capture the current lexical scope for proper closure semantics
        let captured_scope = self.variables.clone();
        
        // Create the lambda function with closure capture
        let lambda_closure = LambdaClosure {
            parameters: parameters.to_vec(),
            body: body.clone(),
            captured_scope,
        };
        
        // Create a native function wrapper that executes the lambda
        let lambda_fn: fn(&[Value]) -> Result<Value, String> = |args| {
            Err("Lambda execution requires interpreter context".to_string())
        };
        
        // Create a proper function with closure information stored in metadata
        let func = runa_common::bytecode::Function {
            name: format!("<lambda_{}>", parameters.len()),
            chunk: runa_common::bytecode::Chunk::new(),
            arity: parameters.len(),
            upvalues: Vec::new(),
            is_native: false,
            native_fn: None,
        };
        
        // Store the lambda closure in the interpreter's function registry for later execution
        let lambda_id = format!("lambda_{}_{}", parameters.len(), self.variables.len());
        
        // Store the lambda closure in registry for execution
        self.lambda_registry.insert(lambda_id.clone(), lambda_closure);
        
        // Create function that references the stored lambda
        let mut func = runa_common::bytecode::Function {
            name: lambda_id,
            chunk: runa_common::bytecode::Chunk::new(),
            arity: parameters.len(),
            upvalues: Vec::new(),
            is_native: false,
            native_fn: None,
        };
        
        Ok(Value::Function(Box::new(func)))
    }
    
    /// Call stdlib functions instead of built-ins
    fn call_stdlib_function(&self, name: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match name {
            "print" => {
                // Call builtins::print from stdlib
                for arg in &args {
                    println!("{}", self.format_value(arg));
                }
                Ok(Value::Integer(0))
            },
            "len" => {
                // Call builtins::len from stdlib
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("len() expects exactly 1 argument".to_string()));
                }
                
                match &args[0] {
                    Value::String(s) => Ok(Value::Integer(s.len() as i64)),
                    Value::List(items) => Ok(Value::Integer(items.len() as i64)),
                    _ => Err(CompilerError::ExecutionFailed("len() requires string or list argument".to_string()))
                }
            },
            "typeof" => {
                // Call builtins::typeof from stdlib
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("typeof() expects exactly 1 argument".to_string()));
                }
                
                let type_name = self.value_type(&args[0]);
                Ok(Value::String(type_name.to_string()))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Stdlib function not found: {}", name))),
        }
    }
    
    /// Access field on object (dot notation support)
    fn access_field(&self, object: &Value, field: &str) -> CompilerResult<Value> {
        match object {
            Value::Dictionary(dict) => {
                // Search for field in dictionary key-value pairs
                for (key, value) in dict {
                    if let Value::String(key_str) = key {
                        if key_str == field {
                            return Ok(value.clone());
                        }
                    }
                }
                Err(CompilerError::ExecutionFailed(format!("Field '{}' not found in dictionary", field)))
            },
            Value::String(s) => {
                // String properties/methods
                match field {
                    "length" => Ok(Value::Integer(s.len() as i64)),
                    "is_empty" => Ok(Value::Boolean(s.is_empty())),
                    "chars" => {
                        let chars: Vec<Value> = s.chars()
                            .map(|c| Value::String(c.to_string()))
                            .collect();
                        Ok(Value::List(chars))
                    },
                    _ => Err(CompilerError::ExecutionFailed(format!("String has no field '{}'", field)))
                }
            },
            Value::List(items) => {
                // List properties
                match field {
                    "length" => Ok(Value::Integer(items.len() as i64)),
                    "is_empty" => Ok(Value::Boolean(items.is_empty())),
                    "first" => {
                        items.first()
                            .cloned()
                            .ok_or_else(|| CompilerError::ExecutionFailed("Cannot access 'first' on empty list".to_string()))
                    },
                    "last" => {
                        items.last()
                            .cloned()
                            .ok_or_else(|| CompilerError::ExecutionFailed("Cannot access 'last' on empty list".to_string()))
                    },
                    _ => Err(CompilerError::ExecutionFailed(format!("List has no field '{}'", field)))
                }
            },
            Value::Integer(n) => {
                // Integer properties
                match field {
                    "abs" => Ok(Value::Integer(n.abs())),
                    "is_positive" => Ok(Value::Boolean(*n > 0)),
                    "is_negative" => Ok(Value::Boolean(*n < 0)),
                    "is_zero" => Ok(Value::Boolean(*n == 0)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Integer has no field '{}'", field)))
                }
            },
            Value::Float(f) => {
                // Float properties
                match field {
                    "abs" => Ok(Value::Float(f.abs())),
                    "is_positive" => Ok(Value::Boolean(*f > 0.0)),
                    "is_negative" => Ok(Value::Boolean(*f < 0.0)),
                    "is_zero" => Ok(Value::Boolean(*f == 0.0)),
                    "floor" => Ok(Value::Integer(f.floor() as i64)),
                    "ceil" => Ok(Value::Integer(f.ceil() as i64)),
                    "round" => Ok(Value::Integer(f.round() as i64)),
                    "is_nan" => Ok(Value::Boolean(f.is_nan())),
                    "is_infinite" => Ok(Value::Boolean(f.is_infinite())),
                    _ => Err(CompilerError::ExecutionFailed(format!("Float has no field '{}'", field)))
                }
            },
            Value::Boolean(b) => {
                // Boolean properties
                match field {
                    "not" => Ok(Value::Boolean(!b)),
                    _ => Err(CompilerError::ExecutionFailed(format!("Boolean has no field '{}'", field)))
                }
            },
            Value::Null | Value::Nil => {
                Err(CompilerError::ExecutionFailed(format!("Cannot access field '{}' on null value", field)))
            },
            _ => {
                Err(CompilerError::ExecutionFailed(format!("Field access not supported for this type: {}", self.value_type(object))))
            }
        }
    }
    
    /// Call method on object with comprehensive type support
    fn call_method(&self, object: &Value, method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match object {
            Value::String(s) => self.call_string_method(s, method, args),
            Value::List(items) => self.call_list_method(items, method, args),
            Value::Dictionary(dict) => self.call_dictionary_method(dict, method, args),
            Value::Integer(n) => self.call_integer_method(*n, method, args),
            Value::Float(f) => self.call_float_method(*f, method, args),
            Value::Boolean(b) => self.call_boolean_method(*b, method, args),
            Value::Null | Value::Nil => {
                Err(CompilerError::ExecutionFailed(format!("Cannot call method '{}' on null value", method)))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Method calls not supported for type: {}", self.value_type(object))))
        }
    }
    
    /// String method implementations
    fn call_string_method(&self, s: &str, method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match method {
            "substring" => {
                if args.len() != 2 {
                    return Err(CompilerError::ExecutionFailed("substring() requires 2 arguments: start, end".to_string()));
                }
                let start = match &args[0] {
                    Value::Integer(n) => *n as usize,
                    _ => return Err(CompilerError::ExecutionFailed("substring start must be an integer".to_string()))
                };
                let end = match &args[1] {
                    Value::Integer(n) => *n as usize,
                    _ => return Err(CompilerError::ExecutionFailed("substring end must be an integer".to_string()))
                };
                
                if start <= s.len() && end <= s.len() && start <= end {
                    Ok(Value::String(s[start..end].to_string()))
                } else {
                    Err(CompilerError::ExecutionFailed("substring indices out of bounds".to_string()))
                }
            },
            "to_uppercase" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("to_uppercase() takes no arguments".to_string()));
                }
                Ok(Value::String(s.to_uppercase()))
            },
            "to_lowercase" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("to_lowercase() takes no arguments".to_string()));
                }
                Ok(Value::String(s.to_lowercase()))
            },
            "trim" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("trim() takes no arguments".to_string()));
                }
                Ok(Value::String(s.trim().to_string()))
            },
            "split" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("split() requires 1 argument: delimiter".to_string()));
                }
                let delimiter = match &args[0] {
                    Value::String(d) => d,
                    _ => return Err(CompilerError::ExecutionFailed("split delimiter must be a string".to_string()))
                };
                
                let parts: Vec<Value> = s.split(delimiter)
                    .map(|part| Value::String(part.to_string()))
                    .collect();
                Ok(Value::List(parts))
            },
            "contains" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("contains() requires 1 argument: substring".to_string()));
                }
                let substring = match &args[0] {
                    Value::String(sub) => sub,
                    _ => return Err(CompilerError::ExecutionFailed("contains argument must be a string".to_string()))
                };
                Ok(Value::Boolean(s.contains(substring)))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("String has no method '{}'", method)))
        }
    }
    
    /// List method implementations
    fn call_list_method(&self, items: &[Value], method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match method {
            "push" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("push() requires 1 argument".to_string()));
                }
                let mut new_items = items.to_vec();
                new_items.push(args[0].clone());
                Ok(Value::List(new_items))
            },
            "pop" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("pop() takes no arguments".to_string()));
                }
                if items.is_empty() {
                    return Err(CompilerError::ExecutionFailed("Cannot pop from empty list".to_string()));
                }
                items.last().cloned().ok_or_else(|| CompilerError::ExecutionFailed("List pop failed".to_string()))
            },
            "get" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("get() requires 1 argument: index".to_string()));
                }
                let index = match &args[0] {
                    Value::Integer(n) => *n as usize,
                    _ => return Err(CompilerError::ExecutionFailed("get index must be an integer".to_string()))
                };
                
                items.get(index)
                    .cloned()
                    .ok_or_else(|| CompilerError::ExecutionFailed("List index out of bounds".to_string()))
            },
            "slice" => {
                if args.len() != 2 {
                    return Err(CompilerError::ExecutionFailed("slice() requires 2 arguments: start, end".to_string()));
                }
                let start = match &args[0] {
                    Value::Integer(n) => *n as usize,
                    _ => return Err(CompilerError::ExecutionFailed("slice start must be an integer".to_string()))
                };
                let end = match &args[1] {
                    Value::Integer(n) => *n as usize,
                    _ => return Err(CompilerError::ExecutionFailed("slice end must be an integer".to_string()))
                };
                
                if start <= items.len() && end <= items.len() && start <= end {
                    Ok(Value::List(items[start..end].to_vec()))
                } else {
                    Err(CompilerError::ExecutionFailed("slice indices out of bounds".to_string()))
                }
            },
            "reverse" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("reverse() takes no arguments".to_string()));
                }
                let mut reversed = items.to_vec();
                reversed.reverse();
                Ok(Value::List(reversed))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("List has no method '{}'", method)))
        }
    }
    
    /// Dictionary method implementations
    fn call_dictionary_method(&self, dict: &[(Value, Value)], method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match method {
            "keys" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("keys() takes no arguments".to_string()));
                }
                let keys: Vec<Value> = dict.iter().map(|(k, _)| k.clone()).collect();
                Ok(Value::List(keys))
            },
            "values" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("values() takes no arguments".to_string()));
                }
                let values: Vec<Value> = dict.iter().map(|(_, v)| v.clone()).collect();
                Ok(Value::List(values))
            },
            "has_key" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("has_key() requires 1 argument: key".to_string()));
                }
                let search_key = &args[0];
                for (key, _) in dict {
                    if key == search_key {
                        return Ok(Value::Boolean(true));
                    }
                }
                Ok(Value::Boolean(false))
            },
            "get" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("get() requires 1 argument: key".to_string()));
                }
                let search_key = &args[0];
                for (key, value) in dict {
                    if key == search_key {
                        return Ok(value.clone());
                    }
                }
                Err(CompilerError::ExecutionFailed("Key not found in dictionary".to_string()))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Dictionary has no method '{}'", method)))
        }
    }
    
    /// Integer method implementations
    fn call_integer_method(&self, n: i64, method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match method {
            "pow" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("pow() requires 1 argument: exponent".to_string()));
                }
                let exp = match &args[0] {
                    Value::Integer(e) => *e as u32,
                    _ => return Err(CompilerError::ExecutionFailed("pow exponent must be an integer".to_string()))
                };
                
                match n.checked_pow(exp) {
                    Some(result) => Ok(Value::Integer(result)),
                    None => Err(CompilerError::ExecutionFailed("Integer overflow in pow operation".to_string()))
                }
            },
            "to_string" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("to_string() takes no arguments".to_string()));
                }
                Ok(Value::String(n.to_string()))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Integer has no method '{}'", method)))
        }
    }
    
    /// Float method implementations
    fn call_float_method(&self, f: f64, method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match method {
            "pow" => {
                if args.len() != 1 {
                    return Err(CompilerError::ExecutionFailed("pow() requires 1 argument: exponent".to_string()));
                }
                let exp = match &args[0] {
                    Value::Float(e) => *e,
                    Value::Integer(e) => *e as f64,
                    _ => return Err(CompilerError::ExecutionFailed("pow exponent must be a number".to_string()))
                };
                Ok(Value::Float(f.powf(exp)))
            },
            "sqrt" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("sqrt() takes no arguments".to_string()));
                }
                if f < 0.0 {
                    return Err(CompilerError::ExecutionFailed("sqrt of negative number".to_string()));
                }
                Ok(Value::Float(f.sqrt()))
            },
            "to_string" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("to_string() takes no arguments".to_string()));
                }
                Ok(Value::String(f.to_string()))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Float has no method '{}'", method)))
        }
    }
    
    /// Boolean method implementations
    fn call_boolean_method(&self, b: bool, method: &str, args: Vec<Value>) -> CompilerResult<Value> {
        match method {
            "to_string" => {
                if !args.is_empty() {
                    return Err(CompilerError::ExecutionFailed("to_string() takes no arguments".to_string()));
                }
                Ok(Value::String(b.to_string()))
            },
            _ => Err(CompilerError::ExecutionFailed(format!("Boolean has no method '{}'", method)))
        }
    }
    
    /// Format value for display
    fn format_value(&self, value: &Value) -> String {
        match value {
            Value::String(s) => s.clone(),
            Value::Integer(n) => n.to_string(),
            Value::Float(f) => f.to_string(),
            Value::Boolean(b) => b.to_string(),
            Value::List(items) => {
                let formatted: Vec<String> = items.iter()
                    .map(|item| self.format_value(item))
                    .collect();
                format!("[{}]", formatted.join(", "))
            },
            Value::Dictionary(dict) => {
                let formatted: Vec<String> = dict.iter()
                    .map(|(k, v)| format!("{}: {}", self.format_value(k), self.format_value(v)))
                    .collect();
                format!("{{{}}}", formatted.join(", "))
            },
            _ => format!("{:?}", value),
        }
    }
    
    /// Get the type name of a value
    fn value_type(&self, value: &Value) -> &'static str {
        match value {
            Value::Integer(_) => "integer",
            Value::Float(_) => "float",
            Value::String(_) => "string",
            Value::Boolean(_) => "boolean",
            Value::Function(_) => "function",
            Value::NativeFunction(_) => "function",
            Value::Null => "null",
            Value::Number(_) => "number",
            Value::Nil => "nil",
            _ => "unknown",
        }
    }
    
    /// Check if a value is truthy
    fn is_truthy(&self, value: &Value) -> bool {
        match value {
            Value::Boolean(b) => *b,
            Value::Null | Value::Nil => false,
            Value::Integer(n) => *n != 0,
            Value::Float(f) => *f != 0.0,
            Value::String(s) => !s.is_empty(),
            _ => true,
        }
    }
    
    /// Calculate branch pattern entropy for ML profiling
    fn calculate_branch_entropy(&self) -> f64 {
        if self.ml_profiler.branch_patterns.is_empty() {
            return 0.0;
        }
        
        let mut entropy = 0.0;
        let total_samples: u32 = self.ml_profiler.branch_patterns.values()
            .map(|(taken, not_taken)| taken + not_taken)
            .sum();
        
        if total_samples == 0 {
            return 0.0;
        }
        
        for (taken, not_taken) in self.ml_profiler.branch_patterns.values() {
            let total = taken + not_taken;
            if total > 0 {
                let taken_prob = *taken as f64 / total as f64;
                let not_taken_prob = *not_taken as f64 / total as f64;
                
                if taken_prob > 0.0 {
                    entropy -= taken_prob * taken_prob.log2();
                }
                if not_taken_prob > 0.0 {
                    entropy -= not_taken_prob * not_taken_prob.log2();
                }
            }
        }
        
        // Normalize by number of branch points
        entropy / self.ml_profiler.branch_patterns.len() as f64
    }
    
    /// Get branch outcomes for detailed ML analysis
    fn get_branch_outcomes(&self) -> HashMap<String, bool> {
        let mut outcomes = HashMap::new();
        
        for (line, (taken, not_taken)) in &self.ml_profiler.branch_patterns {
            // Determine predominant outcome (>60% threshold)
            let total = taken + not_taken;
            if total > 0 {
                let taken_ratio = *taken as f64 / total as f64;
                if taken_ratio > 0.6 {
                    outcomes.insert(format!("line_{}", line), true);
                } else if taken_ratio < 0.4 {
                    outcomes.insert(format!("line_{}", line), false);
                }
                // If between 0.4-0.6, outcome is unpredictable, don't record
            }
        }
        
        outcomes
    }
    
    /// Update current source location for accurate ML profiling
    pub fn set_source_location(&mut self, line: usize, file: &str) {
        self.current_line = line;
        self.current_file = file.to_string();
    }
    
    /// Get current source location
    pub fn get_source_location(&self) -> SourceLocation {
        SourceLocation {
            line: self.current_line,
            column: 1, // Column tracking would require more detailed parsing
            file: self.current_file.clone(),
        }
    }
    
    /// Advance line counter for statement-by-statement execution
    pub fn advance_line(&mut self) {
        self.current_line += 1;
    }
    
    /// Capture current loop state for progress detection
    fn capture_loop_state(&self) -> LoopState {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        
        // Hash variable names and types (not values for performance)
        for (name, value) in &self.variables {
            name.hash(&mut hasher);
            self.value_type(value).hash(&mut hasher);
        }
        
        LoopState {
            variable_count: self.variables.len(),
            variable_hash: hasher.finish(),
            memory_usage: self.memory_tracker.current_usage as usize,
        }
    }
}

impl ExecutionEngine for LightningInterpreter {
    fn execute(&mut self, function_id: &FunctionId, args: Vec<Value>) -> CompilerResult<Value> {
        // Record the call in profiling
        self.call_tracker.record_call(function_id.clone());
        
        // For T0 Lightning Interpreter, execute function call directly
        let function_call = Expression::FunctionCall {
            function: Box::new(Expression::Identifier {
                name: function_id.name.clone(),
                is_qualified: false,
            }),
            arguments: args.iter().map(|arg| Expression::Literal {
                value: arg.clone(),
                literal_type: self.value_type(arg).to_string(),
            }).collect(),
        };
        
        self.evaluate_expression(&function_call, self.current_line)
    }
    
    fn can_execute(&self, _function_id: &FunctionId) -> bool {
        true // Lightning interpreter can execute any function
    }
    
    fn tier_level(&self) -> TierLevel {
        TierLevel::T0
    }
    
    fn collect_profile_data(&self) -> ExecutionProfile {
        ExecutionProfile {
            execution_time: self.ml_profiler.total_execution_time,
            return_type: None, // T0 doesn't track return types in detail
            branch_data: Some(BranchData {
                taken_branches: self.ml_profiler.branch_patterns.values()
                    .map(|(taken, _)| *taken as u64).sum(),
                not_taken_branches: self.ml_profiler.branch_patterns.values()
                    .map(|(_, not_taken)| *not_taken as u64).sum(),
                pattern_entropy: self.calculate_branch_entropy(),
                branch_outcomes: self.get_branch_outcomes(),
            }),
            memory_data: Some(MemoryData {
                allocations: self.memory_tracker.total_allocations,
                deallocations: self.memory_tracker.total_deallocations,
                peak_usage: self.memory_tracker.peak_usage,
            }),
        }
    }
    
    fn should_promote(&self, function_id: &FunctionId) -> bool {
        self.call_tracker.get_call_count(function_id) > 10
    }
}

// =============================================================================
// Supporting Types for Lightning Interpreter
// =============================================================================

/// Interpreter execution engine
#[derive(Debug)]
pub struct InterpreterEngine {
    pub stack: Vec<Value>,
    pub program_counter: usize,
}

impl InterpreterEngine {
    pub fn new() -> Self {
        Self {
            stack: Vec::new(),
            program_counter: 0,
        }
    }
}

/// Profiling hooks for lightweight data collection
#[derive(Debug)]
pub struct ProfilingHooks {
    pub execution_count: u64,
    pub total_execution_time: Duration,
    pub last_result_type: Option<String>,
}

impl ProfilingHooks {
    pub fn new() -> Self {
        Self {
            execution_count: 0,
            total_execution_time: Duration::default(),
            last_result_type: None,
        }
    }
    
    pub fn record_execution(&mut self, duration: Duration, result: &Value) {
        self.execution_count += 1;
        self.total_execution_time += duration;
        self.last_result_type = Some(match result {
            Value::Integer(_) => "integer".to_string(),
            Value::Float(_) => "float".to_string(),
            Value::String(_) => "string".to_string(),
            Value::Boolean(_) => "boolean".to_string(),
            _ => "unknown".to_string(),
        });
    }
}

/// Cached AST for repeated execution
#[derive(Debug, Clone)]
pub struct CachedAST {
    pub ast: ASTNode,
    pub access_count: u64,
    pub last_accessed: Instant,
}

impl CachedAST {
    pub fn new(ast: ASTNode) -> Self {
        Self {
            ast,
            access_count: 0,
            last_accessed: Instant::now(),
        }
    }
    
    pub fn access(&mut self) -> &ASTNode {
        self.access_count += 1;
        self.last_accessed = Instant::now();
        &self.ast
    }
}

/// Call frequency tracker for promotion decisions
#[derive(Debug)]
pub struct CallFrequencyTracker {
    pub call_counts: HashMap<FunctionId, u64>,
    pub call_times: HashMap<FunctionId, Vec<Instant>>,
}

impl CallFrequencyTracker {
    pub fn new() -> Self {
        Self {
            call_counts: HashMap::new(),
            call_times: HashMap::new(),
        }
    }
    
    pub fn record_call(&mut self, function_id: FunctionId) {
        *self.call_counts.entry(function_id.clone()).or_insert(0) += 1;
        self.call_times.entry(function_id).or_insert_with(Vec::new).push(Instant::now());
    }
    
    pub fn get_call_count(&self, function_id: &FunctionId) -> u64 {
        self.call_counts.get(function_id).copied().unwrap_or(0)
    }
    
    pub fn get_call_frequency(&self, function_id: &FunctionId) -> f64 {
        if let Some(times) = self.call_times.get(function_id) {
            if times.len() > 1 {
                if let (Some(last), Some(first)) = (times.last(), times.first()) {
                    let duration = last.duration_since(*first);
                    if duration.as_secs_f64() > 0.0 {
                        times.len() as f64 / duration.as_secs_f64()
                    } else {
                        0.0 // Avoid division by zero for very fast calls
                    }
                } else {
                    0.0 // Safety fallback if vector is somehow corrupted
                }
            } else {
                0.0 // Single call or empty vector
            }
        } else {
            0.0 // No call history
        }
    }
}

/// Intelligent loop progress detection for infinite loop prevention
#[derive(Debug)]
pub struct LoopProgressDetector {
    previous_states: Vec<LoopState>,
    max_state_history: usize,
}

impl LoopProgressDetector {
    pub fn new() -> Self {
        Self {
            previous_states: Vec::new(),
            max_state_history: 10,
        }
    }
    
    pub fn record_state(&mut self, state: LoopState) {
        self.previous_states.push(state);
        
        // Keep only recent history to prevent memory bloat
        if self.previous_states.len() > self.max_state_history {
            self.previous_states.drain(0..self.previous_states.len() - self.max_state_history);
        }
    }
    
    pub fn is_stagnant(&self, current_state: &LoopState) -> bool {
        if self.previous_states.len() < 3 {
            return false; // Need some history to detect stagnation
        }
        
        // Check if the current state matches any recent previous states
        let recent_states = &self.previous_states[self.previous_states.len().saturating_sub(5)..];
        
        let matches = recent_states.iter().filter(|state| state.is_equivalent(current_state)).count();
        
        // If more than half of recent states are identical, consider it stagnant
        matches > recent_states.len() / 2
    }
}

/// Captured state for loop progress detection
#[derive(Debug, Clone)]
pub struct LoopState {
    variable_count: usize,
    variable_hash: u64,
    memory_usage: usize,
}

impl LoopState {
    pub fn is_equivalent(&self, other: &Self) -> bool {
        self.variable_count == other.variable_count 
            && self.variable_hash == other.variable_hash
            && (self.memory_usage as i32 - other.memory_usage as i32).abs() < 1024 // Allow small memory variations
    }
}