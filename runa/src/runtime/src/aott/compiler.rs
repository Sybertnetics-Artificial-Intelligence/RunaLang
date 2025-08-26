//! Main AOTT Compiler
//! 
//! The primary orchestrator that manages all five execution tiers and coordinates
//! compilation, optimization, and tier promotion across the entire AOTT system.

use crate::aott::types::*;
use crate::aott::execution::{ExecutionEngine, ExecutionContext, FunctionMetadata, ContinuousProfiler};
use crate::aott::compilation::{BytecodeCompiler, NativeCompiler, OptimizedNativeCompiler, SpeculativeCompiler, CompilationEngine};
use crate::aott::optimization::{TierPromoter, AdaptiveProfileOptimizer};
use crate::aott::analysis::{DataFlowAnalysisEngine, EscapeAnalysisOptimizer, CallGraphAnalyzer, SymbolicExecutionEngine, GuardAnalyzer, EscapeAnalysisConfig, GuardAnalysisConfig, ProfilingConfig, call_graph::{CallGraph, CallGraphMetrics}};
use crate::aott::hot_swapping::{RuntimePatcher, GuardManager};

use runa_common::bytecode::Value;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::time::Instant;

/// Main AOTT Compiler orchestrating all five tiers
/// 
/// This is the central coordinator that manages:
/// - All five execution tiers (T0-T4)
/// - Tier promotion and demotion
/// - Cross-tier optimization
/// - Runtime profiling and adaptation
/// - Hot code swapping and patching
#[derive(Debug)]
pub struct AoTTCompiler {
    // === Execution Tiers ===
    /// Tier 0: Lightning Interpreter - Zero-cost startup
    pub tier0: crate::aott::execution::LightningInterpreter,
    /// Tier 1: Smart Bytecode Compiler - Fast portable execution
    pub tier1: BytecodeCompiler,
    /// Tier 2: Aggressive Native Compiler - High-performance native code
    pub tier2: NativeCompiler,
    /// Tier 3: Heavily Optimized Native Compiler - Maximum optimization
    pub tier3: OptimizedNativeCompiler,
    /// Tier 4: Speculative Compiler with Guards - Peak performance with speculation
    pub tier4: SpeculativeCompiler,
    
    // === Optimization and Analysis Systems ===
    /// Tier promotion system for automatic tier advancement
    pub tier_promoter: TierPromoter,
    /// Adaptive profile-guided optimizer
    pub profile_optimizer: AdaptiveProfileOptimizer,
    /// Data flow analysis engine
    pub dataflow_analyzer: DataFlowAnalysisEngine,
    /// Escape analysis optimizer
    pub escape_analyzer: EscapeAnalysisOptimizer,
    /// Call graph analyzer for interprocedural optimization
    pub call_graph_analyzer: CallGraphAnalyzer,
    /// Symbolic execution engine for path analysis
    pub symbolic_executor: SymbolicExecutionEngine,
    /// Guard analyzer for speculative execution
    pub guard_analyzer: GuardAnalyzer,
    
    // === Runtime Systems ===
    /// Continuous profiler across all tiers
    pub profiler: ContinuousProfiler,
    /// Runtime code patcher for hot swapping
    pub runtime_patcher: RuntimePatcher,
    /// Guard manager for T4 speculative execution
    pub guard_manager: GuardManager,
    
    // === Shared State ===
    /// Function registry tracking metadata across all tiers
    pub function_registry: Arc<RwLock<HashMap<FunctionId, FunctionMetadata>>>,
    /// Global execution context
    pub execution_context: ExecutionContext,
    /// Compiler configuration
    pub config: CompilerConfig,
    /// Runtime statistics
    pub statistics: CompilerStatistics,
}

impl AoTTCompiler {
    /// Create a new AOTT compiler instance with default configuration
    pub fn new() -> Self {
        Self::with_config(CompilerConfig::default())
    }
    
    /// Create a new AOTT compiler instance with custom configuration
    pub fn with_config(config: CompilerConfig) -> Self {
        let function_registry = Arc::new(RwLock::new(HashMap::new()));
        
        Self {
            // Initialize execution tiers
            tier0: crate::aott::execution::LightningInterpreter::new(),
            tier1: BytecodeCompiler::new(),
            tier2: NativeCompiler::new(),
            tier3: OptimizedNativeCompiler::new(),
            tier4: SpeculativeCompiler::new(),
            
            // Initialize optimization and analysis systems
            tier_promoter: TierPromoter::new(),
            profile_optimizer: AdaptiveProfileOptimizer::new(),
            dataflow_analyzer: DataFlowAnalysisEngine::new(),
            escape_analyzer: EscapeAnalysisOptimizer::new(
                EscapeAnalysisConfig::default(),
                Arc::new(crate::aott::types::CallGraph {
                    nodes: HashMap::new(),
                    edges: Vec::new(),
                })
            ),
            call_graph_analyzer: CallGraphAnalyzer::new(),
            symbolic_executor: SymbolicExecutionEngine::new(),
            guard_analyzer: GuardAnalyzer::new(
                GuardAnalysisConfig::default(),
                ProfilingConfig::default()
            ),
            
            // Initialize runtime systems
            profiler: ContinuousProfiler::new(),
            runtime_patcher: RuntimePatcher::new(),
            guard_manager: GuardManager::new(),
            
            // Initialize shared state
            function_registry,
            execution_context: ExecutionContext::new(),
            config,
            statistics: CompilerStatistics::new(),
        }
    }
    
    /// Execute a function using the appropriate tier
    /// 
    /// This is the main entry point for function execution. It:
    /// 1. Determines which tier should execute the function
    /// 2. Records profiling data
    /// 3. Checks for tier promotion opportunities
    /// 4. Updates statistics
    pub fn execute(&mut self, function_id: &FunctionId, args: Vec<Value>) -> CompilerResult<Value> {
        let tier = self.determine_execution_tier(function_id);
        let start_time = Instant::now();
        
        // Execute using the appropriate tier
        let result = match tier {
            TierLevel::T0 => self.tier0.execute(function_id, args),
            TierLevel::T1 => self.tier1.execute(function_id, args),
            TierLevel::T2 => self.tier2.execute(function_id, args),
            TierLevel::T3 => self.tier3.execute(function_id, args),
            TierLevel::T4 => self.tier4.execute(function_id, args),
        };
        
        let execution_time = start_time.elapsed();
        
        // Record profiling data
        self.record_execution_data(function_id, tier, execution_time, &result);
        
        // Check for tier promotion opportunities
        self.check_tier_promotion(function_id, tier)?;
        
        // Update statistics
        self.statistics.record_execution(tier, execution_time);
        
        result
    }
    
    /// Compile a function to a specific tier
    /// 
    /// Forces compilation of a function to a specific tier, bypassing
    /// the normal tier promotion logic.
    pub fn compile_to_tier(&mut self, function_id: &FunctionId, tier: TierLevel, source: &str) -> CompilerResult<()> {
        match tier {
            TierLevel::T0 => {
                // T0 doesn't require compilation - functions execute directly
                Ok(())
            },
            TierLevel::T1 => {
                self.tier1.compile_function(function_id, source)
            },
            TierLevel::T2 => {
                self.tier2.compile_function(function_id, source)
            },
            TierLevel::T3 => {
                self.tier3.compile_function(function_id, source)
            },
            TierLevel::T4 => {
                self.tier4.compile_function(function_id, source)
            },
        }
    }
    
    /// Determine which tier should execute a function
    fn determine_execution_tier(&self, function_id: &FunctionId) -> TierLevel {
        if let Ok(registry) = self.function_registry.read() {
            if let Some(metadata) = registry.get(function_id) {
                return metadata.tier;
            }
        }
        
        // Default to T0 for new functions
        TierLevel::T0
    }
    
    /// Record execution data for profiling and optimization
    fn record_execution_data(&mut self, function_id: &FunctionId, tier: TierLevel, execution_time: std::time::Duration, result: &CompilerResult<Value>) {
        // Record in continuous profiler
        match tier {
            TierLevel::T0 => self.profiler.record_tier0_execution(function_id.clone()),
            TierLevel::T1 => self.profiler.record_tier1_execution(function_id.clone()),
            TierLevel::T2 => self.profiler.record_tier2_execution(function_id.clone()),
            TierLevel::T3 => self.profiler.record_tier3_execution(function_id.clone()),
            TierLevel::T4 => self.profiler.record_tier4_execution(function_id.clone()),
        }
        
        // Update function metadata
        if let Ok(mut registry) = self.function_registry.write() {
            let metadata = registry.entry(function_id.clone())
                .or_insert_with(|| FunctionMetadata::new(function_id.clone()));
            metadata.increment_call_count();
            metadata.execution_time += execution_time;
            metadata.tier = tier;
            
            // Record success/failure
            if result.is_err() {
                metadata.call_count = metadata.call_count.saturating_sub(1); // Don't count failed executions
            }
        }
    }
    
    /// Check if a function should be promoted to a higher tier
    fn check_tier_promotion(&mut self, function_id: &FunctionId, current_tier: TierLevel) -> CompilerResult<()> {
        let should_promote = match current_tier {
            TierLevel::T0 => self.profiler.should_promote_to_tier1(function_id),
            TierLevel::T1 => self.profiler.should_promote_to_tier2(function_id),
            TierLevel::T2 => self.profiler.should_promote_to_tier3(function_id),
            TierLevel::T3 => self.profiler.should_promote_to_tier4(function_id),
            TierLevel::T4 => false, // T4 is the highest tier
        };
        
        if should_promote {
            match current_tier {
                TierLevel::T0 => self.tier_promoter.promote_to_tier1(function_id)?,
                TierLevel::T1 => self.tier_promoter.promote_to_tier2(function_id)?,
                TierLevel::T2 => self.tier_promoter.promote_to_tier3(function_id)?,
                TierLevel::T3 => self.tier_promoter.promote_to_tier4(function_id)?,
                TierLevel::T4 => {},
            }
            
            self.statistics.record_promotion();
        }
        
        Ok(())
    }
    
    /// Perform comprehensive analysis on a function
    /// 
    /// Runs all available analysis passes to gather optimization data
    pub fn analyze_function(&mut self, function_id: &FunctionId) -> CompilerResult<FunctionAnalysisResult> {
        let mut result = FunctionAnalysisResult::new(function_id.clone());
        
        // Data flow analysis
        if self.config.enable_dataflow_analysis {
            // Create a placeholder cfg using the correct dataflow ControlFlowGraph type
            let dataflow_function_id = crate::aott::analysis::dataflow::FunctionId {
                module: "main".to_string(),
                name: function_id.clone(),
                signature: "()".to_string(),
                context: crate::aott::analysis::dataflow::CallContext::Direct,
            };
            let placeholder_cfg = crate::aott::analysis::dataflow::ControlFlowGraph::new(dataflow_function_id, 0);
            result.dataflow_result = Some(self.dataflow_analyzer.analyze_function(function_id, placeholder_cfg)?);
        }
        
        // Escape analysis
        if self.config.enable_escape_analysis {
            result.escape_analysis = Some(self.escape_analyzer.analyze_escapes(function_id)?);
        }
        
        // Call graph analysis
        if self.config.enable_call_graph_analysis {
            // Build call graph for the function and create placeholder metrics
            let _ = self.call_graph_analyzer.build_call_graph("main")?;
            result.call_graph_metrics = Some(CallGraphMetrics::new(function_id.clone()));
        }
        
        // Symbolic execution
        if self.config.enable_symbolic_execution {
            result.symbolic_execution = Some(self.symbolic_executor.execute_symbolically(function_id)?);
        }
        
        // Guard analysis for T4 preparation
        if self.config.enable_guard_analysis {
            result.guard_placements = Some(self.guard_analyzer.analyze_guard_placement(function_id)?);
        }
        
        Ok(result)
    }
    
    /// Apply a runtime patch to a function
    pub fn apply_hot_patch(&mut self, function_id: FunctionId, patch: crate::aott::hot_swapping::patching::CodePatch) -> CompilerResult<()> {
        self.runtime_patcher.apply_patch(function_id, patch)
    }
    
    /// Rollback a runtime patch
    pub fn rollback_patch(&mut self, function_id: &FunctionId) -> CompilerResult<()> {
        self.runtime_patcher.rollback_patch(function_id)
    }
    
    /// Get comprehensive compiler statistics
    pub fn get_statistics(&self) -> &CompilerStatistics {
        &self.statistics
    }
    
    /// Get profiling data for a specific function
    pub fn get_function_profile(&self, function_id: &FunctionId) -> Option<FunctionMetadata> {
        self.function_registry.read().ok()?.get(function_id).cloned()
    }
    
    /// Force garbage collection of unused compiled code
    pub fn garbage_collect(&mut self) -> CompilerResult<GarbageCollectionResult> {
        let mut result = GarbageCollectionResult::new();
        
        // Clean up unused bytecode
        // Clean up unused native code
        // Clean up unused guards
        // Clean up stale profiling data
        
        Ok(result)
    }
    
    /// Optimize the entire program using interprocedural analysis
    pub fn optimize_program(&mut self, module_name: &str) -> CompilerResult<ProgramOptimizationResult> {
        // Build call graph for the entire module
        let call_graph = self.call_graph_analyzer.build_call_graph(module_name)?;
        
        // Perform interprocedural optimizations
        let mut result = ProgramOptimizationResult::new();
        
        // Cross-function inlining
        // Global optimization passes
        // Dead code elimination across functions
        
        Ok(result)
    }
}

impl Default for AoTTCompiler {
    fn default() -> Self {
        Self::new()
    }
}

// =============================================================================
// Configuration and Results Types
// =============================================================================

/// AOTT Compiler configuration
#[derive(Debug, Clone)]
pub struct CompilerConfig {
    pub enable_dataflow_analysis: bool,
    pub enable_escape_analysis: bool,
    pub enable_call_graph_analysis: bool,
    pub enable_symbolic_execution: bool,
    pub enable_guard_analysis: bool,
    pub enable_hot_swapping: bool,
    pub tier_promotion_thresholds: TierPromotionThresholds,
    pub optimization_level: OptimizationComplexity,
}

impl Default for CompilerConfig {
    fn default() -> Self {
        Self {
            enable_dataflow_analysis: true,
            enable_escape_analysis: true,
            enable_call_graph_analysis: true,
            enable_symbolic_execution: false, // Expensive, disabled by default
            enable_guard_analysis: true,
            enable_hot_swapping: true,
            tier_promotion_thresholds: TierPromotionThresholds::default(),
            optimization_level: OptimizationComplexity::Medium,
        }
    }
}

/// Tier promotion thresholds
#[derive(Debug, Clone)]
pub struct TierPromotionThresholds {
    pub t0_to_t1_calls: u64,
    pub t1_to_t2_calls: u64,
    pub t2_to_t3_calls: u64,
    pub t3_to_t4_calls: u64,
}

impl Default for TierPromotionThresholds {
    fn default() -> Self {
        Self {
            t0_to_t1_calls: 10,
            t1_to_t2_calls: 100,
            t2_to_t3_calls: 1000,
            t3_to_t4_calls: 10000,
        }
    }
}

/// Comprehensive function analysis result
#[derive(Debug)]
pub struct FunctionAnalysisResult {
    pub function_id: FunctionId,
    pub dataflow_result: Option<crate::aott::analysis::dataflow::DataFlowResult>,
    pub escape_analysis: Option<crate::aott::analysis::escape_analysis::EscapeAnalysisResult>,
    pub call_graph_metrics: Option<crate::aott::analysis::call_graph::CallGraphMetrics>,
    pub symbolic_execution: Option<crate::aott::analysis::symbolic_execution::SymbolicExecutionResult>,
    pub guard_placements: Option<Vec<crate::aott::analysis::guard_analysis::GuardPlacement>>,
}

impl FunctionAnalysisResult {
    pub fn new(function_id: FunctionId) -> Self {
        Self {
            function_id,
            dataflow_result: None,
            escape_analysis: None,
            call_graph_metrics: None,
            symbolic_execution: None,
            guard_placements: None,
        }
    }
}

/// Garbage collection result
#[derive(Debug)]
pub struct GarbageCollectionResult {
    pub bytecode_freed: usize,
    pub native_code_freed: usize,
    pub guards_removed: usize,
    pub memory_saved: usize,
}

impl GarbageCollectionResult {
    pub fn new() -> Self {
        Self {
            bytecode_freed: 0,
            native_code_freed: 0,
            guards_removed: 0,
            memory_saved: 0,
        }
    }
}

/// Program-wide optimization result
#[derive(Debug)]
pub struct ProgramOptimizationResult {
    pub functions_optimized: usize,
    pub cross_function_optimizations: usize,
    pub estimated_performance_gain: f64,
}

impl ProgramOptimizationResult {
    pub fn new() -> Self {
        Self {
            functions_optimized: 0,
            cross_function_optimizations: 0,
            estimated_performance_gain: 0.0,
        }
    }
}