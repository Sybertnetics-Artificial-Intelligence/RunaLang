//! Optimization engines for AOTT
//! 
//! This module contains optimization passes and tier promotion logic.

pub mod tier_promotion;
pub mod profiling;
pub mod inlining;
pub mod vectorization;
pub mod loop_optimization;
pub mod memory_layout;
pub mod speculative_opts;
pub mod deoptimization;

// Re-export optimization engines
pub use tier_promotion::TierPromoter;
pub use profiling::AdaptiveProfileOptimizer;
pub use inlining::AdvancedInliningOptimizer;
pub use vectorization::VectorizationOptimizer;
pub use loop_optimization::LoopOptimizationEngine;
pub use memory_layout::MemoryLayoutOptimizer;
pub use speculative_opts::SpeculativeOptimizer;
pub use deoptimization::LiveDeoptimizationEngine;

use crate::aott::types::*;