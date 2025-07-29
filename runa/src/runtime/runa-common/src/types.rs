//! Defines the core types used in the Runa language for semantic analysis.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RunaType {
    Number,
    String,
    Boolean,
    Function, // Represents function types
    Nil, // Represents the absence of a value, e.g., an uninitialized variable
} 