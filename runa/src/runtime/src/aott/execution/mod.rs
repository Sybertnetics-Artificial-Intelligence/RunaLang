//! Execution engines for all five AOTT compilation tiers
//! 
//! This module contains the execution engines for each tier:
//! - T0: Lightning Interpreter - Zero-cost startup interpreter
//! - T1: Bytecode Execution - Smart bytecode with optimizations  
//! - T2: Native Execution - Aggressive native compilation
//! - T3: Optimized Native - Heavily optimized native compilation
//! - T4: Speculative - Speculative execution with guards

pub mod interpreter;
pub mod bytecode;
pub mod native;
pub mod optimized_native;
pub mod speculative;

// Re-export the main execution engines
pub use interpreter::LightningInterpreter;
pub use bytecode::BytecodeExecutor;
pub use native::NativeExecutor;
pub use optimized_native::OptimizedNativeExecutor;
pub use speculative::SpeculativeExecutor;

use crate::aott::types::*;
use runa_common::bytecode::Value;
use std::sync::{Arc, RwLock};
use std::collections::HashMap;

/// Trait that all execution engines must implement
pub trait ExecutionEngine {
    /// Execute a function with the given arguments
    fn execute(&mut self, function_id: &FunctionId, args: Vec<Value>) -> CompilerResult<Value>;
    
    /// Check if this engine can handle the given function
    fn can_execute(&self, function_id: &FunctionId) -> bool;
    
    /// Get the tier level of this execution engine
    fn tier_level(&self) -> TierLevel;
    
    /// Collect profiling data from this execution
    fn collect_profile_data(&self) -> ExecutionProfile;
    
    /// Check if function should be promoted to next tier
    fn should_promote(&self, function_id: &FunctionId) -> bool;
}

/// Execution context shared across all tiers
#[derive(Debug)]
pub struct ExecutionContext {
    /// Function registry with metadata
    pub function_registry: Arc<RwLock<HashMap<FunctionId, FunctionMetadata>>>,
    /// Profiling data collector
    pub profiler: ContinuousProfiler,
    /// Variables environment
    pub variables: HashMap<String, Value>,
    /// Call stack for debugging
    pub call_stack: Vec<FunctionId>,
}

impl ExecutionContext {
    pub fn new() -> Self {
        Self {
            function_registry: Arc::new(RwLock::new(HashMap::new())),
            profiler: ContinuousProfiler::new(),
            variables: HashMap::new(),
            call_stack: Vec::new(),
        }
    }
    
    pub fn push_call(&mut self, function_id: FunctionId) {
        self.call_stack.push(function_id);
    }
    
    pub fn pop_call(&mut self) -> Option<FunctionId> {
        self.call_stack.pop()
    }
    
    pub fn current_function(&self) -> Option<&FunctionId> {
        self.call_stack.last()
    }
}

// =============================================================================
// Supporting Types for Execution Engines
// =============================================================================

/// Function metadata for tracking across tiers
#[derive(Debug, Clone)]
pub struct FunctionMetadata {
    pub id: FunctionId,
    pub tier: TierLevel,
    pub call_count: u64,
    pub execution_time: std::time::Duration,
    pub optimization_level: OptimizationComplexity,
    pub is_hot: bool,
    pub specializations: Vec<String>,
}

impl FunctionMetadata {
    pub fn new(id: FunctionId) -> Self {
        Self {
            id,
            tier: TierLevel::T0,
            call_count: 0,
            execution_time: std::time::Duration::default(),
            optimization_level: OptimizationComplexity::Low,
            is_hot: false,
            specializations: Vec::new(),
        }
    }
    
    pub fn increment_call_count(&mut self) {
        self.call_count += 1;
        if self.call_count > 1000 {
            self.is_hot = true;
        }
    }
    
    pub fn can_promote(&self) -> bool {
        self.tier.can_promote() && (self.is_hot || self.call_count > 100)
    }
}

/// Continuous profiler for tracking execution across tiers
#[derive(Debug)]
pub struct ContinuousProfiler {
    /// Function call frequency tracking
    pub call_counts: Arc<RwLock<HashMap<FunctionId, u64>>>,
    /// Execution time measurements per function
    pub execution_times: Arc<RwLock<HashMap<FunctionId, std::time::Duration>>>,
    /// Memory allocation patterns
    pub memory_patterns: Arc<RwLock<HashMap<FunctionId, MemoryProfile>>>,
    /// Branch prediction accuracy data
    pub branch_patterns: Arc<RwLock<HashMap<FunctionId, BranchProfile>>>,
    /// Type feedback for specialization decisions
    pub type_feedback: Arc<RwLock<HashMap<FunctionId, TypeProfile>>>,
    /// Runtime statistics aggregator
    pub stats_aggregator: StatisticsAggregator,
}

impl ContinuousProfiler {
    pub fn new() -> Self {
        ContinuousProfiler {
            call_counts: Arc::new(RwLock::new(HashMap::new())),
            execution_times: Arc::new(RwLock::new(HashMap::new())),
            memory_patterns: Arc::new(RwLock::new(HashMap::new())),
            branch_patterns: Arc::new(RwLock::new(HashMap::new())),
            type_feedback: Arc::new(RwLock::new(HashMap::new())),
            stats_aggregator: StatisticsAggregator::new(),
        }
    }
    
    pub fn record_tier0_execution(&mut self, function_id: FunctionId) {
        let mut counts = self.call_counts.write().unwrap();
        *counts.entry(function_id).or_insert(0) += 1;
    }
    
    pub fn record_tier1_execution(&mut self, function_id: FunctionId) {
        let mut counts = self.call_counts.write().unwrap();
        *counts.entry(function_id).or_insert(0) += 1;
    }
    
    pub fn record_tier2_execution(&mut self, function_id: FunctionId) {
        let mut counts = self.call_counts.write().unwrap();
        *counts.entry(function_id).or_insert(0) += 1;
    }
    
    pub fn record_tier3_execution(&mut self, function_id: FunctionId) {
        let mut counts = self.call_counts.write().unwrap();
        *counts.entry(function_id).or_insert(0) += 1;
    }
    
    pub fn record_tier4_execution(&mut self, function_id: FunctionId) {
        let mut counts = self.call_counts.write().unwrap();
        *counts.entry(function_id).or_insert(0) += 1;
    }
    
    pub fn get_call_count(&self, function_id: &FunctionId) -> u64 {
        self.call_counts.read().unwrap()
            .get(function_id).copied().unwrap_or(0)
    }
    
    pub fn should_promote_to_tier1(&self, function_id: &FunctionId) -> bool {
        self.get_call_count(function_id) > 10
    }
    
    pub fn should_promote_to_tier2(&self, function_id: &FunctionId) -> bool {
        self.get_call_count(function_id) > 100
    }
    
    pub fn should_promote_to_tier3(&self, function_id: &FunctionId) -> bool {
        self.get_call_count(function_id) > 1000
    }
    
    pub fn should_promote_to_tier4(&self, function_id: &FunctionId) -> bool {
        self.get_call_count(function_id) > 10000
    }
}

/// Memory profiling data
#[derive(Debug, Clone)]
pub struct MemoryProfile {
    pub allocations: u64,
    pub deallocations: u64,
    pub peak_usage: u64,
    pub average_allocation_size: f64,
}

impl MemoryProfile {
    pub fn new() -> Self {
        Self {
            allocations: 0,
            deallocations: 0,
            peak_usage: 0,
            average_allocation_size: 0.0,
        }
    }
}

/// Branch profiling data
#[derive(Debug, Clone)]
pub struct BranchProfile {
    pub total_branches: u64,
    pub taken_branches: u64,
    pub prediction_accuracy: f64,
}

impl BranchProfile {
    pub fn new() -> Self {
        Self {
            total_branches: 0,
            taken_branches: 0,
            prediction_accuracy: 0.0,
        }
    }
    
    pub fn record_branch(&mut self, taken: bool) {
        self.total_branches += 1;
        if taken {
            self.taken_branches += 1;
        }
        self.prediction_accuracy = self.taken_branches as f64 / self.total_branches as f64;
    }
}

/// Type profiling data for specialization
#[derive(Debug, Clone)]
pub struct TypeProfile {
    pub observed_types: HashMap<String, u64>,
    pub dominant_type: Option<String>,
    pub type_stability: f64,
}

impl TypeProfile {
    pub fn new() -> Self {
        Self {
            observed_types: HashMap::new(),
            dominant_type: None,
            type_stability: 0.0,
        }
    }
    
    pub fn record_type(&mut self, type_name: String) {
        *self.observed_types.entry(type_name.clone()).or_insert(0) += 1;
        self.update_dominant_type();
    }
    
    fn update_dominant_type(&mut self) {
        let total_observations: u64 = self.observed_types.values().sum();
        if let Some((dominant, count)) = self.observed_types.iter()
            .max_by_key(|(_, count)| *count) {
            self.dominant_type = Some(dominant.clone());
            self.type_stability = *count as f64 / total_observations as f64;
        }
    }
}

/// Statistics aggregator for performance metrics
#[derive(Debug)]
pub struct StatisticsAggregator {
    pub total_executions: u64,
    pub tier_distribution: HashMap<TierLevel, u64>,
    pub average_execution_time: std::time::Duration,
    pub promotion_events: u64,
}

impl StatisticsAggregator {
    pub fn new() -> Self {
        Self {
            total_executions: 0,
            tier_distribution: HashMap::new(),
            average_execution_time: std::time::Duration::default(),
            promotion_events: 0,
        }
    }
    
    pub fn record_execution(&mut self, tier: TierLevel, duration: std::time::Duration) {
        self.total_executions += 1;
        *self.tier_distribution.entry(tier).or_insert(0) += 1;
        
        // Update average execution time
        let total_time = self.average_execution_time.as_nanos() as u64 * (self.total_executions - 1)
            + duration.as_nanos() as u64;
        self.average_execution_time = std::time::Duration::from_nanos(total_time / self.total_executions);
    }
    
    pub fn record_promotion(&mut self) {
        self.promotion_events += 1;
    }
}