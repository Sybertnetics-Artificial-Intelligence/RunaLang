//! Configuration system for AOTT analysis components
//! 
//! Provides comprehensive configuration management for all analysis phases

use std::time::Duration;

/// Comprehensive configuration for all AOTT analysis components
#[derive(Debug, Clone)]
pub struct AnalysisConfig {
    pub dataflow: DataFlowConfig,
    pub escape_analysis: EscapeAnalysisConfig,
    pub call_graph: CallGraphConfig,
    pub symbolic_execution: SymbolicExecutionConfig,
    pub guard_analysis: GuardAnalysisConfig,
    pub profiling: ProfilingConfig,
}

impl Default for AnalysisConfig {
    fn default() -> Self {
        Self {
            dataflow: DataFlowConfig::default(),
            escape_analysis: EscapeAnalysisConfig::default(),
            call_graph: CallGraphConfig::default(),
            symbolic_execution: SymbolicExecutionConfig::default(),
            guard_analysis: GuardAnalysisConfig::default(),
            profiling: ProfilingConfig::default(),
        }
    }
}

/// Data flow analysis configuration
#[derive(Debug, Clone)]
pub struct DataFlowConfig {
    pub max_iterations: usize,
    pub convergence_threshold: f64,
    pub enable_interprocedural: bool,
    pub precision_level: PrecisionLevel,
    pub optimization_level: OptimizationComplexity,
    pub constant_propagation_depth: usize,
    pub live_variable_precision: f64,
    pub reaching_definitions_cache_size: usize,
}

impl Default for DataFlowConfig {
    fn default() -> Self {
        Self {
            max_iterations: 1000,
            convergence_threshold: 1e-6,
            enable_interprocedural: true,
            precision_level: PrecisionLevel::High,
            optimization_level: OptimizationComplexity::Maximum,
            constant_propagation_depth: 10,
            live_variable_precision: 0.95,
            reaching_definitions_cache_size: 10000,
        }
    }
}

/// Escape analysis configuration
#[derive(Debug, Clone)]
pub struct EscapeAnalysisConfig {
    pub max_tracked_objects: usize,
    pub confidence_threshold: f64,
    pub heap_allocation_overhead: f64,
    pub stack_allocation_benefit: f64,
    pub max_analysis_depth: usize,
    pub similarity_threshold: f64,
    pub location_distance_threshold: usize,
    pub conservative_threshold: f64,
    pub optimization_aggressiveness: f64,
}

impl Default for EscapeAnalysisConfig {
    fn default() -> Self {
        Self {
            max_tracked_objects: 50000,
            confidence_threshold: 0.85,
            heap_allocation_overhead: 2.5,
            stack_allocation_benefit: 1.8,
            max_analysis_depth: 20,
            similarity_threshold: 0.90,
            location_distance_threshold: 500,
            conservative_threshold: 0.75,
            optimization_aggressiveness: 0.8,
        }
    }
}

/// Call graph analysis configuration
#[derive(Debug, Clone)]
pub struct CallGraphConfig {
    pub hot_path_threshold: u64,
    pub frequency_precision: f64,
    pub inlining_threshold: f64,
    pub recursion_depth_limit: usize,
    pub scc_detection_enabled: bool,
    pub cross_module_analysis: bool,
    pub devirtualization_confidence: f64,
    pub potential_scaling_factor: f64,
    pub bottleneck_detection_threshold: f64,
    pub profile_magic_number: Option<u32>,
    pub max_supported_profile_version: u32,
}

impl Default for CallGraphConfig {
    fn default() -> Self {
        Self {
            hot_path_threshold: 10000,
            frequency_precision: 0.01,
            inlining_threshold: 0.75,
            recursion_depth_limit: 50,
            scc_detection_enabled: true,
            cross_module_analysis: true,
            devirtualization_confidence: 0.85,
            potential_scaling_factor: 0.9,
            bottleneck_detection_threshold: 0.8,
            profile_magic_number: Some(0x50524F46), // "PROF" as default
            max_supported_profile_version: 1,
        }
    }
}

/// Symbolic execution configuration
#[derive(Debug, Clone)]
pub struct SymbolicExecutionConfig {
    pub max_path_depth: usize,
    pub max_symbolic_values: usize,
    pub constraint_solver_timeout: Duration,
    pub path_explosion_limit: usize,
    pub loop_unrolling_limit: usize,
    pub memory_model_precision: MemoryModelPrecision,
    pub bug_detection_sensitivity: f64,
    pub state_merging_threshold: usize,
    // Complexity weight parameters for symbolic expressions
    pub base_complexity_weight: f64,
    pub unary_op_complexity_weight: f64,
    pub binary_op_complexity_weight: f64,
    pub conditional_complexity_weight: f64,
    pub function_call_complexity_weight: f64,
    pub field_access_complexity_weight: f64,
    pub coverage_metrics_count: f64,
}

impl Default for SymbolicExecutionConfig {
    fn default() -> Self {
        Self {
            max_path_depth: 1000,
            max_symbolic_values: 10000,
            constraint_solver_timeout: Duration::from_secs(30),
            path_explosion_limit: 100000,
            loop_unrolling_limit: 10,
            memory_model_precision: MemoryModelPrecision::High,
            bug_detection_sensitivity: 0.90,
            state_merging_threshold: 50,
            // Default complexity weights for symbolic expressions
            base_complexity_weight: 1.0,
            unary_op_complexity_weight: 1.0,
            binary_op_complexity_weight: 1.0,
            conditional_complexity_weight: 1.0,
            function_call_complexity_weight: 1.0,
            field_access_complexity_weight: 1.0,
            coverage_metrics_count: 4.0,
        }
    }
}

/// Guard analysis configuration
#[derive(Debug, Clone)]
pub struct GuardAnalysisConfig {
    pub speculation_confidence_threshold: f64,
    pub branch_prediction_confidence: f64,
    pub type_speculation_confidence: f64,
    pub constant_speculation_confidence: f64,
    pub method_speculation_confidence: f64,
    pub deoptimization_cost_threshold: f64,
    pub guard_budget_per_function: usize,
    pub hot_path_execution_threshold: u64,
    pub type_stability_threshold: f64,
    pub branch_stability_threshold: f64,
    pub guard_placement_aggressiveness: f64,
    pub speculation_benefit_threshold: f64,
    pub failure_cost_tolerance: f64,
    pub epsilon_division_guard: f64,
    pub minimum_profile_data_size: usize,
    pub hot_path_significance_threshold: f64,
    pub total_program_execution_time: f64,
    pub location_encoding_factor: usize,
    pub propagation_benefit_divisor: f64,
    pub minimum_net_benefit_threshold: f64,
    pub max_confidence_threshold: f64,
}

impl Default for GuardAnalysisConfig {
    fn default() -> Self {
        Self {
            speculation_confidence_threshold: 0.85,
            branch_prediction_confidence: 0.88,
            type_speculation_confidence: 0.92,
            constant_speculation_confidence: 0.96,
            method_speculation_confidence: 0.80,
            deoptimization_cost_threshold: 0.15,
            guard_budget_per_function: 50,
            hot_path_execution_threshold: 1000,
            type_stability_threshold: 0.90,
            branch_stability_threshold: 0.85,
            guard_placement_aggressiveness: 0.75,
            speculation_benefit_threshold: 0.20,
            failure_cost_tolerance: 0.05,
            epsilon_division_guard: 1e-10,
            minimum_profile_data_size: 16,
            hot_path_significance_threshold: 0.05,
            total_program_execution_time: 1000.0,
            location_encoding_factor: 1000,
            propagation_benefit_divisor: 10.0,
            minimum_net_benefit_threshold: 0.15,
            max_confidence_threshold: 0.95,
        }
    }
}

/// Profiling integration configuration
#[derive(Debug, Clone)]
pub struct ProfilingConfig {
    pub enable_runtime_profiling: bool,
    pub profiling_sample_rate: f64,
    pub profile_data_retention: Duration,
    pub hot_method_threshold: u64,
    pub cold_method_threshold: u64,
    pub adaptive_threshold_adjustment: bool,
    pub profile_collection_overhead_limit: f64,
    pub statistical_confidence_level: f64,
}

impl Default for ProfilingConfig {
    fn default() -> Self {
        Self {
            enable_runtime_profiling: true,
            profiling_sample_rate: 0.1,
            profile_data_retention: Duration::from_hours(24),
            hot_method_threshold: 10000,
            cold_method_threshold: 10,
            adaptive_threshold_adjustment: true,
            profile_collection_overhead_limit: 0.02,
            statistical_confidence_level: 0.95,
        }
    }
}

/// Analysis precision levels
#[derive(Debug, Clone, PartialEq)]
pub enum PrecisionLevel {
    Low,     // Fast but less precise
    Medium,  // Balanced speed and precision
    High,    // Slow but very precise
    Maximum, // Exhaustive analysis
}

/// Optimization complexity levels
#[derive(Debug, Clone, PartialEq)]
pub enum OptimizationComplexity {
    Low,
    Medium,
    High,
    Maximum,
}

/// Memory model precision for symbolic execution
#[derive(Debug, Clone, PartialEq)]
pub enum MemoryModelPrecision {
    Basic,    // Simple pointer tracking
    Medium,   // Field-sensitive analysis
    High,     // Flow-sensitive, field-sensitive
    Precise,  // Full precision with aliasing
}

/// Performance metrics for configuration tuning
#[derive(Debug, Clone)]
pub struct PerformanceMetrics {
    pub analysis_time: Duration,
    pub memory_usage: usize,
    pub optimization_effectiveness: f64,
    pub compilation_speedup: f64,
    pub runtime_performance_gain: f64,
}

impl AnalysisConfig {
    /// Create a configuration optimized for development (fast analysis)
    pub fn development() -> Self {
        let mut config = Self::default();
        config.dataflow.max_iterations = 100;
        config.dataflow.precision_level = PrecisionLevel::Medium;
        config.escape_analysis.max_tracked_objects = 1000;
        config.symbolic_execution.max_path_depth = 100;
        config.guard_analysis.guard_budget_per_function = 10;
        config
    }

    /// Create a configuration optimized for production (comprehensive analysis)
    pub fn production() -> Self {
        let mut config = Self::default();
        config.dataflow.max_iterations = 10000;
        config.dataflow.precision_level = PrecisionLevel::Maximum;
        config.escape_analysis.max_tracked_objects = 100000;
        config.symbolic_execution.max_path_depth = 5000;
        config.guard_analysis.guard_budget_per_function = 200;
        config
    }

    /// Create a configuration optimized for debugging (maximum precision)
    pub fn debug() -> Self {
        let mut config = Self::production();
        config.dataflow.precision_level = PrecisionLevel::Maximum;
        config.symbolic_execution.memory_model_precision = MemoryModelPrecision::Precise;
        config.guard_analysis.speculation_confidence_threshold = 0.95;
        config
    }

    /// Adjust configuration based on performance metrics
    pub fn tune_from_metrics(&mut self, metrics: &PerformanceMetrics) {
        // Adaptive tuning based on performance feedback
        if metrics.analysis_time > Duration::from_secs(300) {
            // Analysis taking too long, reduce precision
            self.dataflow.max_iterations = (self.dataflow.max_iterations as f64 * 0.8) as usize;
            self.escape_analysis.max_tracked_objects = (self.escape_analysis.max_tracked_objects as f64 * 0.8) as usize;
        }

        if metrics.optimization_effectiveness < 0.5 {
            // Poor optimization results, increase precision
            self.guard_analysis.speculation_confidence_threshold *= 0.95;
            self.dataflow.precision_level = PrecisionLevel::High;
        }

        if metrics.compilation_speedup < 1.2 {
            // Compilation not getting faster, adjust guard budget
            self.guard_analysis.guard_budget_per_function = 
                (self.guard_analysis.guard_budget_per_function as f64 * 1.2) as usize;
        }
    }
}