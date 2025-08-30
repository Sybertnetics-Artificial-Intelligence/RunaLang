//! Analysis engines for AOTT
//! 
//! This module contains static analysis engines for optimization.

pub mod config;
pub mod dataflow;
pub mod escape_analysis;
pub mod call_graph;
pub mod symbolic_execution;
pub mod guard_analysis;
pub mod error_handling;

// Re-export analysis engines and configuration
pub use config::*;
pub use dataflow::DataFlowAnalysisEngine;
pub use escape_analysis::EscapeAnalysisOptimizer;
pub use call_graph::CallGraphAnalyzer;
pub use symbolic_execution::SymbolicExecutionEngine;
pub use guard_analysis::GuardAnalyzer;
pub use error_handling::{AnalysisErrorHandler, ErrorContext, ErrorHandlingConfig};

use crate::aott::types::*;