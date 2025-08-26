//! AOTT (All of The Time) Compilation System
//! 
//! Revolutionary hybrid compilation system with five execution tiers:
//! - T0: Lightning Interpreter - Zero-cost startup
//! - T1: Smart Bytecode - Fast bytecode execution  
//! - T2: Aggressive Native - Native compilation with LLVM
//! - T3: Heavily Optimized Native - Advanced native optimizations
//! - T4: Speculative - Speculative execution with guards
//!
//! This is the modularized version of the original monolithic aott.rs file.

pub mod compiler;
pub mod types;
pub mod execution;
pub mod compilation;
pub mod optimization;
pub mod analysis;
pub mod hot_swapping;

// Re-export the main compiler
pub use compiler::AoTTCompiler;

// Re-export commonly used types
pub use types::*;
pub use execution::{ExecutionEngine, ExecutionContext};

// Re-export compilation engines for compatibility
pub use compilation::{BytecodeCompiler, NativeCompiler, OptimizedNativeCompiler, SpeculativeCompiler};

// Module is now complete - all functionality moved to compiler.rs