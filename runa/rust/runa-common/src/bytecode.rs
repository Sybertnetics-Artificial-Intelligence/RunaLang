//! Defines the bytecode instruction set and data structures for the Runa VM.

#[derive(Debug, Clone, PartialEq)]
pub struct Function {
    pub name: String,
    pub chunk: Chunk,
    pub arity: usize,
}

// Using u8 for opcodes is common as it's a single byte.
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum OpCode {
    // --- Constants ---
    /// Pushes a constant from the chunk's constant pool onto the stack.
    /// The operand is the 8-bit index of the constant.
    Constant,

    // --- Arithmetic ---
    Add,
    Subtract,
    Multiply,
    Divide,
    Negate,
    
    // --- String Operations ---
    Concat,

    // --- Logic ---
    Not,
    
    // --- Comparison ---
    Equal,
    NotEqual,
    Greater,
    GreaterEqual,
    Less,
    LessEqual,

    // --- Variables ---
    GetLocal,
    SetLocal,

    // --- Stack ---
    Pop,

    // --- Control Flow ---
    /// Jumps forward by a 16-bit offset if the top of stack is false.
    JumpIfFalse,
    /// Jumps forward by a 16-bit offset.
    Jump,
    /// Jumps backward by a 16-bit offset.
    Loop,

    /// The final instruction in a program.
    Return,

    // --- Functions ---
    /// Defines a function with the given name and parameter count.
    /// Operands: name index (8-bit), param count (8-bit)
    DefineFunction,
    /// Calls a function with the given argument count.
    /// Operand: argument count (8-bit)
    Call,
    /// Returns from the current function with the value on top of the stack.
    ReturnValue,
    
    // --- I/O Operations ---
    /// Prints the value on top of the stack
    Print,
    /// Reads a line from stdin and pushes it as a string
    ReadLine,
    /// Reads a number from stdin and pushes it as a number
    ReadNumber,
}

// We need a way to represent values in our language.
// For now, we'll just support numbers.
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Value {
    Number(f64),
    Boolean(bool),
    String(String),
    Function(Box<Function>),
    Nil,
}

impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Value::Number(n) => write!(f, "{}", n),
            Value::Boolean(b) => write!(f, "{}", b),
            Value::String(s) => write!(f, "{}", s),
            Value::Function(func) => write!(f, "<function {}>", func.name),
            Value::Nil => write!(f, "nil"),
        }
    }
}

/// A chunk represents a sequence of bytecode.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct Chunk {
    pub code: Vec<u8>,
    pub constants: Vec<Value>,
    // We can add line number information here later for better error reporting.
}

impl Chunk {
    pub fn new() -> Self {
        Self::default()
    }

    /// Appends a byte to the chunk. This could be an OpCode or an operand.
    pub fn write(&mut self, byte: u8) {
        self.code.push(byte);
    }
    
    /// Adds a constant value to the pool and returns its index.
    pub fn add_constant(&mut self, value: Value) -> u8 {
        self.constants.push(value);
        // Return the index of the constant we just added.
        // We are limited to 256 constants for now.
        if self.constants.len() > 256 {
            // This is a temporary measure. In a real compiler, we'd use a 16-bit operand for constants.
            panic!("Too many constants in one chunk.");
        }
        (self.constants.len() - 1) as u8
    }
} 