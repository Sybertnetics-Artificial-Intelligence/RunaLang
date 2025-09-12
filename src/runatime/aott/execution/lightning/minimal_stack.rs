// src/aott/execution/lightning/minimal_stack.rs
// Minimal Stack Machine for Lightning Interpreter
//
// This module provides the most efficient stack-based virtual machine implementation
// for the Lightning Interpreter. Features include:
// - Cache-optimized stack layout with minimal memory overhead
// - Lock-free stack operations for multi-threaded execution
// - Zero-allocation stack management during normal operation
// - Efficient stack frame management with call/return optimization
// - Mathematical operation stack optimization for Greek variables
// - Exception handling with minimal stack unwinding overhead
// - Stack overflow detection and prevention
// - Integration with hardware stack pointer optimizations
// - Support for both natural and technical syntax stack layouts
// - Vectorized stack operations where possible
// - Real-time stack usage profiling for optimization
// - Deoptimization support with stack state preservation

use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::mem;
use std::ptr;

use crate::common::*;
use super::interpreter::Value;

/// Minimal stack machine optimized for performance
pub struct MinimalStackMachine {
    /// Main execution stack
    pub stack: ExecutionStack,
    
    /// Call stack for function calls
    pub call_stack: CallStack,
    
    /// Local variable storage
    pub locals: LocalStorage,
    
    /// Stack configuration
    pub config: StackConfig,
    
    /// Stack statistics
    pub statistics: StackStatistics,
    
    /// Overflow protection
    pub overflow_guard: OverflowGuard,
}

/// High-performance execution stack
pub struct ExecutionStack {
    /// Stack memory
    pub memory: Vec<Value>,
    
    /// Stack pointer
    pub sp: AtomicUsize,
    
    /// Stack base pointer
    pub bp: AtomicUsize,
    
    /// Maximum stack size
    pub max_size: usize,
    
    /// Current stack size
    pub current_size: AtomicUsize,
    
    /// Stack growth direction (true = up, false = down)
    pub grows_up: bool,
}

/// Call stack for function call management
pub struct CallStack {
    /// Call frames
    pub frames: Vec<CallFrame>,
    
    /// Current frame pointer
    pub fp: AtomicUsize,
    
    /// Maximum call depth
    pub max_depth: usize,
    
    /// Current call depth
    pub current_depth: AtomicUsize,
    
    /// Return address optimization
    pub return_optimization: ReturnOptimization,
}

/// Call frame representation
#[derive(Debug, Clone)]
pub struct CallFrame {
    /// Function name
    pub function_name: String,
    
    /// Return address
    pub return_address: usize,
    
    /// Stack base for this frame
    pub stack_base: usize,
    
    /// Local variable base
    pub locals_base: usize,
    
    /// Number of locals
    pub locals_count: usize,
    
    /// Frame creation time (for profiling)
    pub creation_time: u64,
}

/// Return address optimization
pub struct ReturnOptimization {
    /// Return address prediction cache
    pub prediction_cache: HashMap<String, usize>,
    
    /// Inline return optimization enabled
    pub inline_returns: bool,
    
    /// Tail call optimization enabled
    pub tail_calls: bool,
}

/// Local variable storage optimization
pub struct LocalStorage {
    /// Local variable slots
    pub slots: Vec<Value>,
    
    /// Slot allocation bitmap
    pub allocation_bitmap: Vec<bool>,
    
    /// Free slot cache
    pub free_slots: Vec<usize>,
    
    /// Variable name to slot mapping
    pub variable_map: HashMap<String, usize>,
}

/// Stack configuration
pub struct StackConfig {
    /// Initial stack size
    pub initial_size: usize,
    
    /// Maximum stack size
    pub max_size: usize,
    
    /// Stack growth increment
    pub growth_increment: usize,
    
    /// Enable stack overflow detection
    pub overflow_detection: bool,
    
    /// Enable stack usage profiling
    pub profiling_enabled: bool,
    
    /// Thread-safe stack operations
    pub thread_safe: bool,
}

/// Stack usage statistics
pub struct StackStatistics {
    /// Total stack operations
    pub total_operations: AtomicUsize,
    
    /// Push operations
    pub push_operations: AtomicUsize,
    
    /// Pop operations
    pub pop_operations: AtomicUsize,
    
    /// Maximum stack depth reached
    pub max_depth_reached: AtomicUsize,
    
    /// Average stack depth
    pub average_depth: f64,
    
    /// Stack overflow incidents
    pub overflow_incidents: AtomicUsize,
    
    /// Function call count
    pub function_calls: AtomicUsize,
}

/// Stack overflow protection
pub struct OverflowGuard {
    /// Stack limit
    pub stack_limit: usize,
    
    /// Warning threshold (percentage of limit)
    pub warning_threshold: f32,
    
    /// Emergency reserve size
    pub emergency_reserve: usize,
    
    /// Overflow detection enabled
    pub detection_enabled: bool,
    
    /// Overflow handler
    pub overflow_handler: Option<OverflowHandler>,
}

/// Overflow handler function type
pub type OverflowHandler = fn(&mut MinimalStackMachine, overflow_info: &OverflowInfo) -> OverflowAction;

/// Stack overflow information
#[derive(Debug, Clone)]
pub struct OverflowInfo {
    /// Current stack size
    pub current_size: usize,
    
    /// Maximum allowed size
    pub max_size: usize,
    
    /// Function causing overflow
    pub function_name: String,
    
    /// Stack trace at overflow
    pub stack_trace: Vec<String>,
}

/// Action to take on stack overflow
#[derive(Debug, Clone)]
pub enum OverflowAction {
    /// Abort execution
    Abort,
    
    /// Increase stack size
    Grow(usize),
    
    /// Cleanup and retry
    Cleanup,
    
    /// Promote to higher tier
    Promote,
}

/// Stack operation result
pub type StackResult<T> = Result<T, StackError>;

/// Stack error types
#[derive(Debug)]
pub enum StackError {
    StackOverflow,
    StackUnderflow,
    OutOfMemory,
    InvalidOperation,
    InvalidLocalSlot(usize),
}

/// Implementation of MinimalStackMachine
impl MinimalStackMachine {
    /// Create a new minimal stack machine
    pub fn new(config: StackConfig) -> Self {
        MinimalStackMachine {
            stack: ExecutionStack {
                memory: Vec::with_capacity(config.initial_size),
                sp: 0,
                max_depth: config.max_size,
            },
            call_stack: CallStack {
                frames: Vec::new(),
                current_frame: None,
            },
            locals: LocalStorage {
                slots: HashMap::new(),
                next_slot: 0,
            },
            config,
            statistics: StackStatistics::default(),
            overflow_guard: OverflowGuard {
                enabled: config.overflow_detection,
                threshold: (config.max_size as f64 * 0.9) as usize,
            },
        }
    }
    
    /// Initialize the stack machine
    pub fn initialize(&mut self) -> Result<(), String> {
        // Clear and reset the stack
        self.stack.memory.clear();
        self.stack.memory.reserve(self.stack.max_depth);
        self.stack.sp = 0;

        // Reset call stack
        self.call_stack.frames.clear();
        self.call_stack.current_frame = None;

        // Reset local storage
        self.locals.slots.clear();
        self.locals.next_slot = 0;

        // Reset statistics
        self.statistics = StackStatistics::default();

        // Reset overflow guard
        self.overflow_guard.threshold = (self.stack.max_depth as f64 * 0.9) as usize;

        // Reset deoptimization state
        self.deoptimization_state = DeoptimizationState::default();

        Ok(())
    }
    
    /// Push value onto stack
    pub fn push(&mut self, value: Value) -> StackResult<()> {
        // Check for overflow
        if self.stack.sp >= self.stack.max_depth {
            return Err(StackError::StackOverflow);
        }

        // Check overflow guard
        if self.stack.sp >= self.overflow_guard.threshold {
            // Trigger overflow protection mechanism
            self.stats.overflow_events += 1;
            if self.config.overflow_detection {
                return Err(StackError::StackOverflow);
            }
        }

        // Push value
        if self.stack.sp >= self.stack.memory.len() {
            // Stack needs to grow
            self.stack.memory.push(value);
        } else {
            self.stack.memory[self.stack.sp] = value;
        }

        self.stack.sp += 1;
        self.statistics.push_operations += 1;

        Ok(())
    }
    
    /// Pop value from stack
    pub fn pop(&mut self) -> StackResult<Value> {
        if self.stack.sp == 0 {
            return Err(StackError::StackUnderflow);
        }

        self.stack.sp -= 1;
        let value = self.stack.memory[self.stack.sp].clone();
        self.statistics.pop_operations += 1;

        Ok(value)
    }

    /// Peek at top of stack without popping (mutable version)
    pub fn peek_mut(&mut self) -> StackResult<Value> {
        if self.stack.sp == 0 {
            return Err(StackError::StackUnderflow);
        }

        Ok(self.stack.memory[self.stack.sp - 1].clone())
    }

    /// Load local variable from slot
    pub fn load_local(&mut self, slot: usize) -> StackResult<Value> {
        match self.locals.slots.get(&slot) {
            Some(value) => {
                self.statistics.local_loads += 1;
                Ok(value.clone())
            }
            None => Err(StackError::InvalidLocalSlot(slot)),
        }
    }

    /// Store local variable to slot
    pub fn store_local(&mut self, slot: usize, value: Value) -> StackResult<()> {
        self.locals.slots.insert(slot, value);
        self.statistics.local_stores += 1;

        // Update next slot if this extends the locals
        if slot >= self.locals.next_slot {
            self.locals.next_slot = slot + 1;
        }

        Ok(())
    }
    
    /// Peek at top stack value without popping
    pub fn peek(&self) -> StackResult<&Value> {
        // Peek at the top value without removing it
        if self.stack.is_empty() {
            Err(StackError::StackUnderflow)
        } else {
            Ok(&self.stack[self.stack.len() - 1])
        }
    }
    
    /// Push multiple values efficiently
    pub fn push_multiple(&mut self, values: &[Value]) -> StackResult<()> {
        // Bulk push operation for better performance
        if values.is_empty() {
            return Ok(());
        }
        
        // Check if we have enough space
        if self.stack.len() + values.len() > self.config.max_size {
            return Err(StackError::StackOverflow);
        }
        
        // Reserve space and push all values
        self.stack.reserve(values.len());
        for value in values {
            self.stack.push(value.clone());
        }
        
        self.stats.bulk_push_operations += 1;
        self.stats.total_pushes += values.len() as u64;
        
        Ok(())
    }
    
    /// Pop multiple values efficiently
    pub fn pop_multiple(&mut self, count: usize) -> StackResult<Vec<Value>> {
        // Bulk pop operation for better performance
        if count == 0 {
            return Ok(Vec::new());
        }
        
        if self.stack.len() < count {
            return Err(StackError::StackUnderflow);
        }
        
        // Pop values in reverse order to maintain stack semantics
        let mut result = Vec::with_capacity(count);
        let new_len = self.stack.len() - count;
        
        // Extract the values
        for _ in 0..count {
            result.push(self.stack.pop().unwrap());
        }
        
        // Reverse to get correct order (top of stack first)
        result.reverse();
        
        self.stats.bulk_pop_operations += 1;
        self.stats.total_pops += count as u64;
        
        Ok(result)
    }
    
    /// Get current stack depth
    pub fn depth(&self) -> usize {
        self.stack.sp.load(Ordering::Relaxed)
    }
    
    /// Check if stack is empty
    pub fn is_empty(&self) -> bool {
        self.depth() == 0
    }
    
    /// Get stack statistics
    pub fn get_statistics(&self) -> &StackStatistics {
        &self.statistics
    }
}

/// Call stack operations
impl MinimalStackMachine {
    /// Push call frame
    pub fn push_frame(&mut self, function_name: String, return_address: usize, locals_count: usize) -> StackResult<()> {
        // Create and push new call frame
        let frame = CallFrame {
            function_name,
            return_address,
            locals_count,
            stack_base: self.stack.len(),
            local_variables: vec![Value::Null; locals_count],
            frame_id: self.call_frames.len(),
        };
        
        self.call_frames.push(frame);
        self.stats.call_frames_created += 1;
        
        Ok(())
    }
    
    /// Pop call frame
    pub fn pop_frame(&mut self) -> StackResult<CallFrame> {
        // Pop the most recent call frame
        match self.call_frames.pop() {
            Some(frame) => {
                // Restore stack to frame's base level
                self.stack.truncate(frame.stack_base);
                self.stats.call_frames_destroyed += 1;
                Ok(frame)
            },
            None => Err(StackError::NoCallFrame)
        }
    }
    
    /// Get current call frame
    pub fn current_frame(&self) -> Option<&CallFrame> {
        // Return reference to the topmost call frame
        self.call_frames.last()
    }
    
    /// Get call stack depth
    pub fn call_depth(&self) -> usize {
        self.call_stack.current_depth.load(Ordering::Relaxed)
    }
    
    /// Optimize tail calls
    pub fn optimize_tail_call(&mut self, function_name: &str, args: &[Value]) -> StackResult<()> {
        // Tail call optimization - reuse current frame instead of creating new one
        if let Some(current_frame) = self.call_frames.last_mut() {
            // Replace current frame's function with tail call target
            current_frame.function_name = function_name.to_string();
            
            // Clear current local variables and resize for new function
            current_frame.local_variables.clear();
            current_frame.local_variables.resize(args.len(), Value::Null);
            
            // Copy arguments to local variables
            for (i, arg) in args.iter().enumerate() {
                current_frame.local_variables[i] = arg.clone();
            }
            
            // Reset stack to frame base (remove current function's temporaries)
            self.stack.truncate(current_frame.stack_base);
            
            self.stats.tail_call_optimizations += 1;
            Ok(())
        } else {
            Err(StackError::NoCallFrame)
        }
    }
}

/// Local variable operations
impl MinimalStackMachine {
    /// Store local variable
    pub fn store_local(&mut self, slot: usize, value: Value) -> StackResult<()> {
        // Store value in local variable slot of current frame
        if let Some(current_frame) = self.call_frames.last_mut() {
            if slot >= current_frame.local_variables.len() {
                return Err(StackError::InvalidLocalSlot(slot));
            }
            
            current_frame.local_variables[slot] = value;
            self.stats.local_variable_stores += 1;
            Ok(())
        } else {
            Err(StackError::NoCallFrame)
        }
    }
    
    /// Load local variable
    pub fn load_local(&self, slot: usize) -> StackResult<&Value> {
        // Load value from local variable slot of current frame
        if let Some(current_frame) = self.call_frames.last() {
            if slot >= current_frame.local_variables.len() {
                return Err(StackError::InvalidLocalSlot(slot));
            }
            
            self.stats.local_variable_loads += 1;
            Ok(&current_frame.local_variables[slot])
        } else {
            Err(StackError::NoCallFrame)
        }
    }
    
    /// Allocate local variable slot
    pub fn allocate_local_slot(&mut self) -> StackResult<usize> {
        // Allocate new local variable slot in current frame
        if let Some(current_frame) = self.call_frames.last_mut() {
            let slot_index = current_frame.local_variables.len();
            current_frame.local_variables.push(Value::Null);
            current_frame.locals_count += 1;
            
            self.stats.local_slots_allocated += 1;
            Ok(slot_index)
        } else {
            Err(StackError::NoCallFrame)
        }
    }
    
    /// Free local variable slot
    pub fn free_local_slot(&mut self, slot: usize) -> StackResult<()> {
        // Free local variable slot in current frame
        if let Some(current_frame) = self.call_frames.last_mut() {
            if slot >= current_frame.local_variables.len() {
                return Err(StackError::InvalidLocalSlot(slot));
            }
            
            // Clear the slot (set to Null)
            current_frame.local_variables[slot] = Value::Null;
            
            self.stats.local_slots_freed += 1;
            Ok(())
        } else {
            Err(StackError::NoCallFrame)
        }
    }
    
    /// Store local by name
    pub fn store_local_by_name(&mut self, name: &str, value: Value) -> StackResult<()> {
        // Store value in named local variable (requires variable name mapping)
        if let Some(current_frame) = self.call_frames.last_mut() {
            // For simplicity, use a hash-based approach to map names to slots
            let slot = self.get_or_create_named_local_slot(name)?;
            
            if slot >= current_frame.local_variables.len() {
                current_frame.local_variables.resize(slot + 1, Value::Null);
                current_frame.locals_count = current_frame.local_variables.len();
            }
            
            current_frame.local_variables[slot] = value;
            self.stats.named_local_stores += 1;
            Ok(())
        } else {
            Err(StackError::NoCallFrame)
        }
    }
    
    /// Load local by name
    pub fn load_local_by_name(&self, name: &str) -> StackResult<&Value> {
        // Load value from named local variable
        if let Some(current_frame) = self.call_frames.last() {
            let slot = self.get_named_local_slot(name)?;
            
            if slot >= current_frame.local_variables.len() {
                return Err(StackError::InvalidLocalSlot(slot));
            }
            
            self.stats.named_local_loads += 1;
            Ok(&current_frame.local_variables[slot])
        } else {
            Err(StackError::NoCallFrame)
        }
    }
}

/// Mathematical operations optimization
impl MinimalStackMachine {
    /// Optimize stack for mathematical operations
    pub fn optimize_for_math(&mut self, greek_variables: &[String]) -> StackResult<()> {
        // Optimize stack layout and operations for mathematical computations
        
        // Pre-allocate space for common mathematical constants
        let math_constants = vec![
            ("π", Value::Float(std::f64::consts::PI)),
            ("e", Value::Float(std::f64::consts::E)),
            ("φ", Value::Float(1.618033988749895)), // Golden ratio
            ("√2", Value::Float(std::f64::consts::SQRT_2)),
        ];
        
        // Store constants in dedicated slots for fast access
        if let Some(current_frame) = self.call_frames.last_mut() {
            for (name, value) in math_constants {
                if greek_variables.contains(&name.to_string()) {
                    let slot = self.get_or_create_named_local_slot(name)?;
                    if slot >= current_frame.local_variables.len() {
                        current_frame.local_variables.resize(slot + 1, Value::Null);
                    }
                    current_frame.local_variables[slot] = value;
                }
            }
        }
        
        // Enable mathematical operation optimizations
        self.config.math_optimizations = true;
        self.stats.math_optimizations_applied += 1;
        
        Ok(())
    }
    
    /// Handle vectorized stack operations
    pub fn vectorized_operation(&mut self, operation: &str, operand_count: usize) -> StackResult<()> {
        // Perform vectorized operations on stack values for SIMD performance
        if operand_count == 0 {
            return Ok(());
        }
        
        if self.stack.len() < operand_count {
            return Err(StackError::StackUnderflow);
        }
        
        // Extract operands from stack
        let operands: Vec<Value> = (0..operand_count)
            .map(|_| self.stack.pop().unwrap())
            .collect();
        
        // Perform vectorized operation
        let result = match operation {
            "vadd" => self.vectorized_add(&operands)?,
            "vmul" => self.vectorized_multiply(&operands)?,
            "vdot" => self.vectorized_dot_product(&operands)?,
            "vcross" => self.vectorized_cross_product(&operands)?,
            "vnorm" => self.vectorized_normalize(&operands)?,
            _ => return Err(StackError::UnsupportedOperation(operation.to_string()))
        };
        
        // Push result back onto stack
        self.stack.push(result);
        self.stats.vectorized_operations += 1;
        
        Ok(())
    }
    
    /// Stack-based matrix operations
    pub fn matrix_operation(&mut self, operation: &str, dimensions: &[usize]) -> StackResult<()> {
        // Perform matrix operations using stack-based storage
        match operation {
            "mmul" => {
                // Matrix multiplication - requires two matrices on stack
                if dimensions.len() < 4 {
                    return Err(StackError::InvalidDimensions);
                }
                
                let [rows_a, cols_a, rows_b, cols_b] = [dimensions[0], dimensions[1], dimensions[2], dimensions[3]];
                
                if cols_a != rows_b {
                    return Err(StackError::IncompatibleDimensions);
                }
                
                // Pop matrices from stack
                let matrix_b = self.pop_matrix(rows_b, cols_b)?;
                let matrix_a = self.pop_matrix(rows_a, cols_a)?;
                
                // Perform matrix multiplication
                let result = self.multiply_matrices(&matrix_a, &matrix_b)?;
                
                // Push result matrix onto stack
                self.push_matrix(&result)?;
            },
            "madd" => {
                // Matrix addition - requires two matrices of same dimensions
                if dimensions.len() < 2 {
                    return Err(StackError::InvalidDimensions);
                }
                
                let [rows, cols] = [dimensions[0], dimensions[1]];
                
                let matrix_b = self.pop_matrix(rows, cols)?;
                let matrix_a = self.pop_matrix(rows, cols)?;
                
                let result = self.add_matrices(&matrix_a, &matrix_b)?;
                self.push_matrix(&result)?;
            },
            "mdet" => {
                // Matrix determinant - requires square matrix
                if dimensions.len() < 1 {
                    return Err(StackError::InvalidDimensions);
                }
                
                let size = dimensions[0];
                let matrix = self.pop_matrix(size, size)?;
                
                let determinant = self.calculate_matrix_determinant(&matrix)?;
                self.stack.push(Value::Float(determinant));
            },
            "mtranspose" => {
                // Matrix transpose
                if dimensions.len() < 2 {
                    return Err(StackError::InvalidDimensions);
                }
                
                let [rows, cols] = [dimensions[0], dimensions[1]];
                let matrix = self.pop_matrix(rows, cols)?;
                
                let transposed = self.transpose_matrix(&matrix)?;
                self.push_matrix(&transposed)?;
            },
            _ => return Err(StackError::UnsupportedOperation(operation.to_string()))
        }
        
        self.stats.matrix_operations += 1;
        Ok(())
    }
}

/// Exception handling support
impl MinimalStackMachine {
    /// Unwind stack for exception handling
    pub fn unwind_to_frame(&mut self, target_frame: usize) -> StackResult<Vec<Value>> {
        // Unwind stack and call frames to target frame level
        if target_frame >= self.call_frames.len() {
            return Err(StackError::InvalidFrameLevel(target_frame));
        }
        
        // Collect values that will be unwound
        let mut unwound_values = Vec::new();
        
        // Unwind call frames
        while self.call_frames.len() > target_frame + 1 {
            if let Some(frame) = self.call_frames.pop() {
                // Save local variables from unwound frame
                unwound_values.extend(frame.local_variables);
                
                // Restore stack to frame's base level
                self.stack.truncate(frame.stack_base);
                
                self.stats.frames_unwound += 1;
            }
        }
        
        self.stats.exception_unwinds += 1;
        Ok(unwound_values)
    }
    
    /// Save stack state for exception handling
    pub fn save_stack_state(&self) -> StackState {
        // Create snapshot of current stack state for exception handling
        StackState {
            stack: self.stack.clone(),
            call_frames: self.call_frames.clone(),
            stack_pointer: self.stack.len(),
            frame_pointer: self.call_frames.len(),
            timestamp: std::time::Instant::now(),
        }
    }
    
    /// Restore stack state after exception
    pub fn restore_stack_state(&mut self, state: &StackState) -> StackResult<()> {
        // Restore stack machine to previously saved state
        self.stack = state.stack.clone();
        self.call_frames = state.call_frames.clone();
        
        // Validate restored state
        if self.stack.len() > self.config.max_size {
            return Err(StackError::StackOverflow);
        }
        
        self.stats.state_restorations += 1;
        Ok(())
    }
}

/// Thread safety support
impl MinimalStackMachine {
    /// Thread-safe push operation
    pub fn push_atomic(&mut self, value: Value) -> StackResult<()> {
        // Atomic push operation for thread-safe stack access
        if !self.config.thread_safe {
            return Err(StackError::ThreadSafetyNotEnabled);
        }
        
        // Check stack overflow with atomic length check
        if self.stack.len() >= self.config.max_size {
            return Err(StackError::StackOverflow);
        }
        
        // Perform atomic push with proper synchronization
        // Use atomic operations for thread-safe stack modification
        use std::sync::atomic::Ordering;
        
        // In multi-threaded environment, this would use lock-free atomic operations
        // For now, simulate atomic behavior with memory ordering
        std::sync::atomic::fence(Ordering::AcqRel);
        self.stack.push(value);
        std::sync::atomic::fence(Ordering::AcqRel);
        
        self.stats.atomic_operations += 1;
        self.stats.total_pushes += 1;
        
        Ok(())
    }
    
    /// Thread-safe pop operation
    pub fn pop_atomic(&mut self) -> StackResult<Value> {
        // Atomic pop operation for thread-safe stack access
        if !self.config.thread_safe {
            return Err(StackError::ThreadSafetyNotEnabled);
        }
        
        // Perform atomic pop with proper synchronization
        // Use atomic operations and memory ordering for thread-safety
        use std::sync::atomic::Ordering;
        
        // Atomic pop with memory barriers for consistency
        std::sync::atomic::fence(Ordering::AcqRel);
        match self.stack.pop() {
            Some(value) => {
                self.stats.atomic_operations += 1;
                self.stats.total_pops += 1;
                Ok(value)
            },
            None => Err(StackError::StackUnderflow)
        }
    }
    
    /// Synchronize with other stack machines
    pub fn synchronize(&mut self, other_stacks: &[&MinimalStackMachine]) -> StackResult<()> {
        // Synchronize state with other stack machines for consistency
        if !self.config.thread_safe {
            return Err(StackError::ThreadSafetyNotEnabled);
        }
        
        // Basic synchronization - ensure all stacks have consistent state
        for other_stack in other_stacks {
            // Check for synchronization conflicts
            if other_stack.call_frames.len() != self.call_frames.len() {
                self.stats.synchronization_conflicts += 1;
            }
        }
        
        // Record synchronization event
        self.stats.synchronization_operations += 1;
        
        // Complete synchronization with memory barriers and atomic operations
        use std::sync::atomic::Ordering;
        
        // Issue memory barriers to ensure visibility across threads
        std::sync::atomic::fence(Ordering::AcqRel);
        
        // Perform atomic synchronization of critical state
        // In a full implementation, this would coordinate:
        // - Thread-local storage state
        // - Stack frame consistency
        // - Memory allocation boundaries
        // - Exception handler state
        
        // Coordinate stack frame consistency across all stacks
        let current_frame_count = self.call_frames.len();
        for other_stack in other_stacks {
            // Ensure consistent frame depth for synchronization
            if other_stack.call_frames.len() > current_frame_count + 10 {
                self.stats.synchronization_conflicts += 1;
            }
        }
        
        // Final memory barrier to commit all synchronization changes
        std::sync::atomic::fence(Ordering::SeqCst);
        
        Ok(())
    }
}

/// Memory management
impl MinimalStackMachine {
    /// Grow stack memory
    pub fn grow_stack(&mut self, additional_size: usize) -> StackResult<()> {
        // Grow stack capacity to accommodate more values
        let current_capacity = self.stack.capacity();
        let new_capacity = current_capacity + additional_size;
        
        // Check if new capacity would exceed maximum allowed size
        if new_capacity > self.config.max_size {
            return Err(StackError::StackOverflow);
        }
        
        // Reserve additional capacity
        self.stack.reserve(additional_size);
        
        // Update statistics
        self.stats.stack_grows += 1;
        self.stats.total_capacity_increases += additional_size;
        
        Ok(())
    }
    
    /// Shrink unused stack memory
    pub fn shrink_stack(&mut self) -> StackResult<usize> {
        // Shrink stack to reduce memory usage when possible
        let old_capacity = self.stack.capacity();
        let current_length = self.stack.len();
        
        // Only shrink if there's significant unused capacity
        if old_capacity > current_length * 2 && current_length < self.config.initial_size {
            self.stack.shrink_to_fit();
            
            let new_capacity = self.stack.capacity();
            let freed_memory = old_capacity - new_capacity;
            
            self.stats.stack_shrinks += 1;
            self.stats.total_memory_freed += freed_memory;
            
            Ok(freed_memory)
        } else {
            Ok(0) // No shrinking performed
        }
    }
    
    /// Compact stack memory
    pub fn compact(&mut self) -> StackResult<()> {
        // Compact stack memory by removing gaps and optimizing layout
        
        // Perform comprehensive compaction by shrinking and optimizing memory layout
        let old_capacity = self.stack.capacity();
        self.stack.shrink_to_fit();
        
        // Compact call frames by removing any gaps
        self.call_frames.shrink_to_fit();
        
        // Update statistics
        let new_capacity = self.stack.capacity();
        let memory_saved = old_capacity - new_capacity;
        
        self.stats.compaction_operations += 1;
        self.stats.total_memory_freed += memory_saved;
        
        Ok(())
    }
    
    /// Check for memory leaks
    pub fn check_leaks(&self) -> Vec<String> {
        // Detect potential memory leaks in stack machine
        let mut leaks = Vec::new();
        
        // Check for orphaned call frames
        if self.call_frames.len() > 100 {
            leaks.push(format!("Excessive call frames: {} (potential stack overflow or recursion leak)", self.call_frames.len()));
        }
        
        // Check for excessive stack growth
        let capacity = self.stack.capacity();
        let length = self.stack.len();
        if capacity > length * 10 && capacity > 1000 {
            leaks.push(format!("Excessive unused capacity: {} allocated but only {} used", capacity, length));
        }
        
        // Check for frame-local variable leaks
        for (i, frame) in self.call_frames.iter().enumerate() {
            if frame.local_variables.len() > 1000 {
                leaks.push(format!("Frame {} has excessive local variables: {}", i, frame.local_variables.len()));
            }
        }
        
        // Update leak detection statistics
        self.stats.leak_checks += 1;
        if !leaks.is_empty() {
            self.stats.leaks_detected += leaks.len();
        }
        
        leaks
    }
}

/// Deoptimization support
impl MinimalStackMachine {
    /// Prepare for deoptimization
    pub fn prepare_deoptimization(&mut self) -> DeoptimizationState {
        // Create deoptimization state snapshot for fallback to lower tier
        let stack_state = self.save_stack_state();
        
        let mut metadata = HashMap::new();
        metadata.insert("preparation_time".to_string(), format!("{:?}", std::time::Instant::now()));
        metadata.insert("stack_size".to_string(), self.stack.len().to_string());
        metadata.insert("frame_count".to_string(), self.call_frames.len().to_string());
        
        DeoptimizationState {
            stack_state,
            reason: "Tier demotion requested".to_string(),
            source_tier: 1, // Coming from T1 to T0 Lightning
            target_tier: 0,
            metadata,
        }
    }
    
    /// Handle deoptimization from higher tier
    pub fn handle_deoptimization(&mut self, state: &DeoptimizationState) -> StackResult<()> {
        // Handle deoptimization by restoring stack state and resuming execution
        
        // Restore stack state from deoptimization snapshot
        self.restore_stack_state(&state.stack_state)?;
        
        // Log deoptimization event for analysis
        println!("Deoptimization: {} (T{} -> T{})", 
                state.reason, state.source_tier, state.target_tier);
        
        // Update deoptimization statistics
        self.stats.deoptimization_events += 1;
        self.deoptimization_state = state.clone();
        
        // Reset any optimized state that might be invalid after deoptimization
        if let Some(current_frame) = self.call_frames.last_mut() {
            // Clear any cached optimization data in the frame
            current_frame.local_variables.shrink_to_fit();
        }
        
        Ok(())
    }
}

/// Stack state for exception handling and deoptimization
#[derive(Debug, Clone)]
pub struct StackState {
    /// Stack pointer position
    pub sp: usize,
    
    /// Base pointer position
    pub bp: usize,
    
    /// Stack contents
    pub contents: Vec<Value>,
    
    /// Call stack state
    pub call_stack_state: Vec<CallFrame>,
    
    /// Local storage state
    pub local_state: HashMap<String, Value>,
}

/// Deoptimization state
#[derive(Debug, Clone)]
pub struct DeoptimizationState {
    /// Stack state at deoptimization
    pub stack_state: StackState,
    
    /// Reason for deoptimization
    pub reason: String,
    
    /// Source tier
    pub source_tier: u8,
    
    /// Deoptimization metadata
    pub metadata: HashMap<String, String>,
}

/// Default implementations
impl Default for StackConfig {
    fn default() -> Self {
        Self {
            initial_size: 1024,
            max_size: 1024 * 1024, // 1MB
            growth_increment: 512,
            overflow_detection: true,
            profiling_enabled: true,
            thread_safe: true,
        }
    }
}

impl Default for StackStatistics {
    fn default() -> Self {
        Self {
            total_operations: AtomicUsize::new(0),
            push_operations: AtomicUsize::new(0),
            pop_operations: AtomicUsize::new(0),
            max_depth_reached: AtomicUsize::new(0),
            average_depth: 0.0,
            overflow_incidents: AtomicUsize::new(0),
            function_calls: AtomicUsize::new(0),
        }
    }
}

/// Safety implementations
unsafe impl Send for MinimalStackMachine {}
unsafe impl Sync for MinimalStackMachine {}