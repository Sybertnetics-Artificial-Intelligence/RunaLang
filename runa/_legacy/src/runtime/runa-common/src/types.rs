//! Defines the core types used in the Runa language for semantic analysis.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RunaType {
    // Primitive types
    Integer,
    Float, 
    Number, // Legacy alias for numeric values
    String,
    Boolean,
    Null,
    Nil, // Legacy alias for Null
    Any, // Dynamic type for untyped values
    
    // Function types
    Function {
        params: Vec<RunaType>,
        return_type: Box<RunaType>,
    },
    
    // Collection types  
    List(Box<RunaType>), // Represents list types with element type
    Dictionary {
        key: Box<RunaType>,
        value: Box<RunaType>, 
    }, // Represents dictionary types with key and value types
    
    // Object types
    Class(String),
    Object(String),
} 