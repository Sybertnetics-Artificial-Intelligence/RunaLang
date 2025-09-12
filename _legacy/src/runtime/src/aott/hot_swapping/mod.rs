//! Hot swapping and runtime patching for AOTT
//! 
//! This module contains AOTT-specific runtime code modification capabilities.

pub mod patching;
pub mod guard_management;

// Re-export hot swapping components
pub use patching::RuntimePatcher;
pub use guard_management::GuardManager;

use crate::aott::types::*;