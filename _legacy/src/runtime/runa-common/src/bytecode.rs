//! Defines the bytecode instruction set and data structures for the Runa VM.

#[derive(Debug, Clone, PartialEq)]
pub struct Function {
    pub name: String,
    pub chunk: Chunk,
    pub arity: usize,
    pub upvalues: Vec<Upvalue>,
    pub is_native: bool,
    pub native_fn: Option<fn(&[Value]) -> Result<Value, String>>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Upvalue {
    pub index: usize,
    pub is_local: bool,
}

// Production-ready opcode set for Runa language
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum OpCode {
    // --- Constants ---
    /// Pushes a constant from the chunk's constant pool onto the stack.
    /// Operand: 16-bit constant index
    Constant,
    /// Pushes a constant integer (optimized for common values)
    /// Operand: 8-bit integer value
    ConstantInt,
    /// Pushes null value
    Null,
    /// Pushes true value
    True,
    /// Pushes false value
    False,

    // --- Arithmetic Operations ---
    Add,
    Subtract,
    Multiply,
    Divide,
    Modulo,
    Negate,
    Power,
    
    // --- Natural Language Arithmetic Operators ---
    /// Natural language: "plus"
    Plus,
    /// Natural language: "minus"
    Minus,
    /// Natural language: "multiplied by"
    MultipliedBy,
    /// Natural language: "divided by"
    DividedBy,
    /// Natural language: "power of"
    PowerOf,
    /// Natural language: "modulo"
    ModuloOp,
    
    // --- String Operations ---
    Concat,
    Substring,
    StringLength,
    
    // --- Logic Operations ---
    Not,
    And,
    Or,
    
    // --- Natural Language Logic Operators ---
    /// Natural language: "logical and"
    LogicalAnd,
    /// Natural language: "logical or"
    LogicalOr,
    /// Natural language: "logical not"
    LogicalNot,
    
    // --- Comparison Operations ---
    Equal,
    NotEqual,
    Greater,
    GreaterEqual,
    Less,
    LessEqual,

    // --- Natural Language Comparison Operators ---
    /// Natural language: "is equal to"
    IsEqualTo,
    /// Natural language: "is not equal to"
    IsNotEqualTo,
    /// Natural language: "is greater than"
    IsGreaterThan,
    /// Natural language: "is less than"
    IsLessThan,
    /// Natural language: "is greater than or equal to"
    IsGreaterThanOrEqualTo,
    /// Natural language: "is less than or equal to"
    IsLessThanOrEqualTo,
    
    // --- Bitwise Operations ---
    BitwiseAnd,
    BitwiseOr,
    BitwiseXor,
    BitwiseNot,
    ShiftLeft,
    ShiftRight,
    
    // --- Natural Language Bitwise Operators ---
    /// Natural language: "bitwise and"
    BitwiseAndOp,
    /// Natural language: "bitwise or"
    BitwiseOrOp,
    /// Natural language: "bitwise xor"
    BitwiseXorOp,
    /// Natural language: "bitwise not"
    BitwiseNotOp,
    /// Natural language: "shifted left by"
    ShiftedLeftBy,
    /// Natural language: "shifted right by"
    ShiftedRightBy,
    
    // --- Variable Operations ---
    /// Gets a local variable by index
    /// Operand: 8-bit local index
    GetLocal,
    /// Sets a local variable by index
    /// Operand: 8-bit local index
    SetLocal,
    /// Gets a global variable by name
    /// Operand: 16-bit name constant index
    GetGlobal,
    /// Sets a global variable by name
    /// Operand: 16-bit name constant index
    SetGlobal,
    /// Gets an upvalue by index
    /// Operand: 8-bit upvalue index
    GetUpvalue,
    /// Sets an upvalue by index
    /// Operand: 8-bit upvalue index
    SetUpvalue,

    // --- Stack Operations ---
    Pop,
    /// Duplicates the top value on the stack
    Dup,
    /// Swaps the top two values on the stack
    Swap,

    // --- Control Flow ---
    /// Jumps forward by 16-bit offset if the top of stack is false
    JumpIfFalse,
    /// Jumps forward by 16-bit offset if the top of stack is true
    JumpIfTrue,
    /// Unconditional jump forward by 16-bit offset
    Jump,
    /// Unconditional jump backward by 16-bit offset (for loops)
    Loop,
    /// Returns from the current function
    Return,
    /// Returns from the current function with the value on top of the stack
    ReturnValue,
    
    // --- Function Operations ---
    /// Calls a function with the given argument count
    /// Operand: 8-bit argument count
    Call,
    /// Calls a native function
    /// Operand: 16-bit native function index
    CallNative,
    /// Calls a method on an object
    /// Operand: 8-bit argument count, 16-bit method name constant index
    CallMethod,
    /// Creates a closure (function with captured variables)
    /// Operand: 16-bit function constant index, 8-bit upvalue count
    Closure,
    /// Closes upvalues that are no longer in scope
    /// Operand: 8-bit upvalue count
    CloseUpvalue,

    // --- Class and Object Operations ---
    /// Creates a new class
    /// Operand: 16-bit class name constant index
    Class,
    /// Creates a new instance of a class
    /// Operand: 16-bit class name constant index
    New,
    /// Gets a property from an object
    /// Operand: 16-bit property name constant index
    GetProperty,
    /// Sets a property on an object
    /// Operand: 16-bit property name constant index
    SetProperty,
    /// Defines a method on a class
    /// Operand: 16-bit method name constant index
    Method,

    // --- Collection Operations ---
    /// Creates a new list with the given number of items
    /// Operand: 8-bit item count
    CreateList,
    /// Creates a new dictionary with the given number of key-value pairs
    /// Operand: 8-bit pair count
    CreateDict,
    /// Gets an item from a list by index
    GetItem,
    /// Sets an item in a list by index
    SetItem,
    /// Gets a value from a dictionary by key
    GetDict,
    /// Sets a value in a dictionary by key
    SetDict,
    /// Adds an item to a list
    AddToList,
    /// Removes an item from a list
    RemoveFromList,
    /// Gets the length of a collection or string
    Length,
    /// Checks if a collection contains an item
    Contains,

    // --- Type Operations ---
    /// Converts a value to string
    ToString,
    /// Converts a value to integer
    ToInteger,
    /// Converts a value to float
    ToFloat,
    /// Converts a value to boolean
    ToBoolean,
    /// Gets the type of a value
    TypeOf,
    /// Checks if a value is null
    IsNull,
    /// Checks if a value is not null
    IsNotNull,

    // --- Language Keywords (Built-in Operations) ---
    /// Displays a value (language keyword)
    Display,
    /// Prints a value to console
    Print,
    /// Reads a line from stdin
    ReadLine,
    /// Reads a number from stdin
    ReadNumber,

    // --- Error Handling ---
    /// Throws an exception
    /// Operand: 16-bit exception type constant index
    Throw,
    /// Begins a try block
    Try,
    /// Begins a catch block
    /// Operand: 16-bit exception type constant index
    Catch,
    /// Begins a finally block
    Finally,

    // --- Concurrency ---
    /// Spawns a new process
    Spawn,
    /// Sends a message to a process
    Send,
    /// Receives a message from a process
    Receive,
    /// Yields control to another process
    Yield,

    // --- Memory Management ---
    /// Allocates memory for an object
    Allocate,
    /// Deallocates memory for an object
    Deallocate,
    /// Marks an object for garbage collection
    Mark,

    // --- Debugging and Profiling ---
    /// Sets a breakpoint (debug builds only)
    Breakpoint,
    /// Records a profiling event
    /// Operand: 16-bit event type constant index
    Profile,
    
    // --- Missing variants ---
    /// Defines a function
    DefineFunction,
    /// Checks if value is none/null
    IsNone,
    /// Checks if value is not none/null
    IsNotNone,
    /// Loads a constant by index (alias for Constant)
    LoadConstant,
    /// Loads a local variable
    LoadLocal,
    /// Stores a local variable
    StoreLocal,
}

// Production-ready value representation for Runa language
use std::fmt;

#[derive(Debug, Clone)]
pub enum Value {
    // Primitive types
    Integer(i64),
    Float(f64),
    Boolean(bool),
    String(String),
    Null,
    
    // Legacy aliases for compatibility
    Number(f64),  // Alias for numeric values (can represent both int and float)
    Nil,          // Alias for Null
    
    // Function types
    Function(Box<Function>),
    NativeFunction(fn(&[Value]) -> Result<Value, String>),
    
    // Collection types
    List(Vec<Value>),
    Dictionary(Vec<(Value, Value)>),
    Set(Vec<Value>),
    Tuple(Vec<Value>),
    
    // Object types
    Object(Box<Object>),
    Class(Box<Class>),
    
    // Special types
    Optional(Option<Box<Value>>),
    Result(Result<Box<Value>, Box<Value>>),
    
    // Process/Thread types
    Process(ProcessId),
    Channel(ChannelId),
    
    // Memory management
    Reference(ReferenceId),
    WeakReference(WeakReferenceId),
    
    // Error handling
    Error(RuntimeError),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Object {
    pub class: String,
    pub fields: Vec<(String, Value)>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Class {
    pub name: String,
    pub methods: Vec<(String, Function)>,
    pub fields: Vec<String>,
    pub superclass: Option<String>,
}

// Type aliases for process and memory management
pub type ProcessId = u64;
pub type ChannelId = u64;
pub type ReferenceId = u64;
pub type WeakReferenceId = u64;

#[derive(Debug, Clone, PartialEq)]
pub struct RuntimeError {
    pub message: String,
    pub error_type: String,
    pub line: Option<usize>,
    pub column: Option<usize>,
}

impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Value::Integer(n) => write!(f, "{}", n),
            Value::Float(x) => write!(f, "{}", x),
            Value::Boolean(b) => write!(f, "{}", b),
            Value::String(s) => write!(f, "{}", s),
            Value::Null => write!(f, "null"),
            Value::Number(n) => write!(f, "{}", n),
            Value::Nil => write!(f, "nil"),
            Value::Function(func) => write!(f, "<function {}>", func.name),
            Value::NativeFunction(_) => write!(f, "<native function>"),
            Value::List(items) => {
                write!(f, "[")?;
                for (i, item) in items.iter().enumerate() {
                    if i > 0 { write!(f, ", ")?; }
                    write!(f, "{}", item)?;
                }
                write!(f, "]")
            }
            Value::Dictionary(items) => {
                write!(f, "{{")?;
                for (i, (key, value)) in items.iter().enumerate() {
                    if i > 0 { write!(f, ", ")?; }
                    write!(f, "{}: {}", key, value)?;
                }
                write!(f, "}}")
            }
            Value::Set(items) => {
                write!(f, "{{")?;
                for (i, item) in items.iter().enumerate() {
                    if i > 0 { write!(f, ", ")?; }
                    write!(f, "{}", item)?;
                }
                write!(f, "}}")
            }
            Value::Tuple(items) => {
                write!(f, "(")?;
                for (i, item) in items.iter().enumerate() {
                    if i > 0 { write!(f, ", ")?; }
                    write!(f, "{}", item)?;
                }
                write!(f, ")")
            }
            Value::Object(obj) => write!(f, "<object {}>", obj.class),
            Value::Class(cls) => write!(f, "<class {}>", cls.name),
            Value::Optional(Some(val)) => write!(f, "Some({})", val),
            Value::Optional(None) => write!(f, "None"),
            Value::Result(Ok(val)) => write!(f, "Ok({})", val),
            Value::Result(Err(val)) => write!(f, "Err({})", val),
            Value::Process(id) => write!(f, "<process {}>", id),
            Value::Channel(id) => write!(f, "<channel {}>", id),
            Value::Reference(id) => write!(f, "<ref {}>", id),
            Value::WeakReference(id) => write!(f, "<weak_ref {}>", id),
            Value::Error(err) => write!(f, "Error: {}", err.message),
        }
    }
}

// Production-ready chunk structure with debugging information
#[derive(Debug, Clone, PartialEq)]
pub struct Chunk {
    pub code: Vec<u8>,
    pub constants: Vec<Value>,
    pub lines: Vec<usize>,  // Line number for each instruction
    pub source_map: Vec<SourceLocation>,  // Source location for each instruction
    pub instructions: Vec<OpCode>,
    pub bytecode: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct SourceLocation {
    pub file: String,
    pub line: usize,
    pub column: usize,
}

impl Chunk {
    pub fn new() -> Self {
        Chunk {
            code: Vec::new(),
            constants: Vec::new(),
            lines: Vec::new(),
            instructions: Vec::new(),
            source_map: Vec::new(),
            bytecode: Vec::new(),
        }
    }

    pub fn write(&mut self, byte: u8, line: usize) {
        self.code.push(byte);
        self.lines.push(line);
    }

    pub fn write_with_location(&mut self, byte: u8, line: usize, source_loc: SourceLocation) {
        self.code.push(byte);
        self.lines.push(line);
        self.source_map.push(source_loc);
    }
    
    pub fn add_constant(&mut self, value: Value) -> u16 {
        self.constants.push(value);
        (self.constants.len() - 1) as u16
    }

    pub fn write_constant(&mut self, value: Value, line: usize) -> u16 {
        let constant_index = self.add_constant(value);
        self.write(OpCode::Constant as u8, line);
        self.write((constant_index >> 8) as u8, line);
        self.write((constant_index & 0xFF) as u8, line);
        constant_index
    }

    pub fn write_constant_int(&mut self, value: i8, line: usize) {
        self.write(OpCode::ConstantInt as u8, line);
        self.write(value as u8, line);
    }

    pub fn write_short(&mut self, value: u16, line: usize) {
        self.write((value >> 8) as u8, line);
        self.write((value & 0xFF) as u8, line);
    }

    pub fn disassemble(&self, name: &str) {
        println!("== {} ==", name);
        
        let mut offset = 0;
        while offset < self.code.len() {
            offset = self.disassemble_instruction(offset);
        }
    }

    fn disassemble_instruction(&self, offset: usize) -> usize {
        print!("{:04} ", offset);
        
        if offset > 0 && self.lines[offset] == self.lines[offset - 1] {
            print!("   | ");
        } else {
            print!("{:4} ", self.lines[offset]);
        }

        let instruction = self.code[offset];
        match instruction {
            x if x == OpCode::Constant as u8 => {
                let constant_index = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("CONSTANT {:4} '{}'", constant_index, self.constants[constant_index as usize]);
                offset + 3
            }
            x if x == OpCode::ConstantInt as u8 => {
                let value = self.code[offset + 1] as i8;
                println!("CONSTANT_INT {}", value);
                offset + 2
            }
            x if x == OpCode::Null as u8 => {
                println!("NULL");
                offset + 1
            }
            x if x == OpCode::True as u8 => {
                println!("TRUE");
                offset + 1
            }
            x if x == OpCode::False as u8 => {
                println!("FALSE");
                offset + 1
            }
            x if x == OpCode::Add as u8 => {
                println!("ADD");
                offset + 1
            }
            x if x == OpCode::Subtract as u8 => {
                println!("SUBTRACT");
                offset + 1
            }
            x if x == OpCode::Multiply as u8 => {
                println!("MULTIPLY");
                offset + 1
            }
            x if x == OpCode::Divide as u8 => {
                println!("DIVIDE");
                offset + 1
            }
            x if x == OpCode::Negate as u8 => {
                println!("NEGATE");
                offset + 1
            }
            x if x == OpCode::Power as u8 => {
                println!("POWER");
                offset + 1
            }
            x if x == OpCode::Plus as u8 => {
                println!("PLUS");
                offset + 1
            }
            x if x == OpCode::Minus as u8 => {
                println!("MINUS");
                offset + 1
            }
            x if x == OpCode::MultipliedBy as u8 => {
                println!("MULTIPLIED_BY");
                offset + 1
            }
            x if x == OpCode::DividedBy as u8 => {
                println!("DIVIDED_BY");
                offset + 1
            }
            x if x == OpCode::PowerOf as u8 => {
                println!("POWER_OF");
                offset + 1
            }
            x if x == OpCode::ModuloOp as u8 => {
                println!("MODULO_OP");
                offset + 1
            }
            x if x == OpCode::Concat as u8 => {
                println!("CONCAT");
                offset + 1
            }
            x if x == OpCode::Substring as u8 => {
                println!("SUBSTRING");
                offset + 1
            }
            x if x == OpCode::StringLength as u8 => {
                println!("STRING_LENGTH");
                offset + 1
            }
            x if x == OpCode::Not as u8 => {
                println!("NOT");
                offset + 1
            }
            x if x == OpCode::And as u8 => {
                println!("AND");
                offset + 1
            }
            x if x == OpCode::Or as u8 => {
                println!("OR");
                offset + 1
            }
            x if x == OpCode::LogicalAnd as u8 => {
                println!("LOGICAL_AND");
                offset + 1
            }
            x if x == OpCode::LogicalOr as u8 => {
                println!("LOGICAL_OR");
                offset + 1
            }
            x if x == OpCode::LogicalNot as u8 => {
                println!("LOGICAL_NOT");
                offset + 1
            }
            x if x == OpCode::Equal as u8 => {
                println!("EQUAL");
                offset + 1
            }
            x if x == OpCode::NotEqual as u8 => {
                println!("NOT_EQUAL");
                offset + 1
            }
            x if x == OpCode::Greater as u8 => {
                println!("GREATER");
                offset + 1
            }
            x if x == OpCode::GreaterEqual as u8 => {
                println!("GREATER_EQUAL");
                offset + 1
            }
            x if x == OpCode::Less as u8 => {
                println!("LESS");
                offset + 1
            }
            x if x == OpCode::LessEqual as u8 => {
                println!("LESS_EQUAL");
                offset + 1
            }
            x if x == OpCode::IsEqualTo as u8 => {
                println!("IS_EQUAL_TO");
                offset + 1
            }
            x if x == OpCode::IsNotEqualTo as u8 => {
                println!("IS_NOT_EQUAL_TO");
                offset + 1
            }
            x if x == OpCode::IsGreaterThan as u8 => {
                println!("IS_GREATER_THAN");
                offset + 1
            }
            x if x == OpCode::IsLessThan as u8 => {
                println!("IS_LESS_THAN");
                offset + 1
            }
            x if x == OpCode::IsGreaterThanOrEqualTo as u8 => {
                println!("IS_GREATER_THAN_OR_EQUAL_TO");
                offset + 1
            }
            x if x == OpCode::IsLessThanOrEqualTo as u8 => {
                println!("IS_LESS_THAN_OR_EQUAL_TO");
                offset + 1
            }
            x if x == OpCode::BitwiseAnd as u8 => {
                println!("BITWISE_AND");
                offset + 1
            }
            x if x == OpCode::BitwiseOr as u8 => {
                println!("BITWISE_OR");
                offset + 1
            }
            x if x == OpCode::BitwiseXor as u8 => {
                println!("BITWISE_XOR");
                offset + 1
            }
            x if x == OpCode::BitwiseNot as u8 => {
                println!("BITWISE_NOT");
                offset + 1
            }
            x if x == OpCode::ShiftLeft as u8 => {
                println!("SHIFT_LEFT");
                offset + 1
            }
            x if x == OpCode::ShiftRight as u8 => {
                println!("SHIFT_RIGHT");
                offset + 1
            }
            x if x == OpCode::BitwiseAndOp as u8 => {
                println!("BITWISE_AND_OP");
                offset + 1
            }
            x if x == OpCode::BitwiseOrOp as u8 => {
                println!("BITWISE_OR_OP");
                offset + 1
            }
            x if x == OpCode::BitwiseXorOp as u8 => {
                println!("BITWISE_XOR_OP");
                offset + 1
            }
            x if x == OpCode::BitwiseNotOp as u8 => {
                println!("BITWISE_NOT_OP");
                offset + 1
            }
            x if x == OpCode::ShiftedLeftBy as u8 => {
                println!("SHIFTED_LEFT_BY");
                offset + 1
            }
            x if x == OpCode::ShiftedRightBy as u8 => {
                println!("SHIFTED_RIGHT_BY");
                offset + 1
            }
            x if x == OpCode::Pop as u8 => {
                println!("POP");
                offset + 1
            }
            x if x == OpCode::Dup as u8 => {
                println!("DUP");
                offset + 1
            }
            x if x == OpCode::Swap as u8 => {
                println!("SWAP");
                offset + 1
            }
            x if x == OpCode::JumpIfTrue as u8 => {
                let jump = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("JUMP_IF_TRUE {:4} -> {}", jump, offset + 3 + jump as usize);
                offset + 3
            }
            x if x == OpCode::Return as u8 => {
                println!("RETURN");
                offset + 1
            }
            x if x == OpCode::ReturnValue as u8 => {
                println!("RETURN_VALUE");
                offset + 1
            }
            x if x == OpCode::GetLocal as u8 => {
                let slot = self.code[offset + 1];
                println!("GET_LOCAL {}", slot);
                offset + 2
            }
            x if x == OpCode::SetLocal as u8 => {
                let slot = self.code[offset + 1];
                println!("SET_LOCAL {}", slot);
                offset + 2
            }
            x if x == OpCode::GetGlobal as u8 => {
                let name_index = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("GET_GLOBAL {:4} '{}'", name_index, self.constants[name_index as usize]);
                offset + 3
            }
            x if x == OpCode::SetGlobal as u8 => {
                let name_index = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("SET_GLOBAL {:4} '{}'", name_index, self.constants[name_index as usize]);
                offset + 3
            }
            x if x == OpCode::Call as u8 => {
                let arg_count = self.code[offset + 1];
                println!("CALL {}", arg_count);
                offset + 2
            }
            x if x == OpCode::Jump as u8 => {
                let jump = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("JUMP {:4} -> {}", jump, offset + 3 + jump as usize);
                offset + 3
            }
            x if x == OpCode::JumpIfFalse as u8 => {
                let jump = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("JUMP_IF_FALSE {:4} -> {}", jump, offset + 3 + jump as usize);
                offset + 3
            }
            x if x == OpCode::Loop as u8 => {
                let jump = (self.code[offset + 1] as u16) << 8 | self.code[offset + 2] as u16;
                println!("LOOP {:4} -> {}", jump, offset + 3 - jump as usize);
                offset + 3
            }
            x if x == OpCode::Display as u8 => {
                println!("DISPLAY");
                offset + 1
            }
            x if x == OpCode::Length as u8 => {
                println!("LENGTH");
                offset + 1
            }
            x if x == OpCode::CreateList as u8 => {
                let item_count = self.code[offset + 1];
                println!("CREATE_LIST {}", item_count);
                offset + 2
            }
            x if x == OpCode::CreateDict as u8 => {
                let pair_count = self.code[offset + 1];
                println!("CREATE_DICT {}", pair_count);
                offset + 2
            }
            x if x == OpCode::GetItem as u8 => {
                println!("GET_ITEM");
                offset + 1
            }
            x if x == OpCode::SetItem as u8 => {
                println!("SET_ITEM");
                offset + 1
            }
            x if x == OpCode::GetDict as u8 => {
                println!("GET_DICT");
                offset + 1
            }
            x if x == OpCode::SetDict as u8 => {
                println!("SET_DICT");
                offset + 1
            }
            x if x == OpCode::AddToList as u8 => {
                println!("ADD_TO_LIST");
                offset + 1
            }
            x if x == OpCode::RemoveFromList as u8 => {
                println!("REMOVE_FROM_LIST");
                offset + 1
            }
            x if x == OpCode::Contains as u8 => {
                println!("CONTAINS");
                offset + 1
            }
            x if x == OpCode::ToString as u8 => {
                println!("TO_STRING");
                offset + 1
            }
            x if x == OpCode::ToInteger as u8 => {
                println!("TO_INTEGER");
                offset + 1
            }
            x if x == OpCode::ToFloat as u8 => {
                println!("TO_FLOAT");
                offset + 1
            }
            x if x == OpCode::ToBoolean as u8 => {
                println!("TO_BOOLEAN");
                offset + 1
            }
            x if x == OpCode::TypeOf as u8 => {
                println!("TYPE_OF");
                offset + 1
            }
            x if x == OpCode::IsNull as u8 => {
                println!("IS_NULL");
                offset + 1
            }
            x if x == OpCode::IsNotNull as u8 => {
                println!("IS_NOT_NULL");
                offset + 1
            }
            _ => {
                println!("UNKNOWN_OPCODE {}", instruction);
                offset + 1
            }
        }
    }
}

// Custom trait implementations for Value to handle floating point numbers
impl PartialEq for Value {
    fn eq(&self, other: &Self) -> bool {
        use Value::*;
        match (self, other) {
            (Integer(a), Integer(b)) => a == b,
            (Float(a), Float(b)) => a.to_bits() == b.to_bits(), // Handle NaN correctly
            (Number(a), Number(b)) => a.to_bits() == b.to_bits(),
            (Boolean(a), Boolean(b)) => a == b,
            (String(a), String(b)) => a == b,
            (Null, Null) | (Nil, Nil) => true,
            (List(a), List(b)) => a == b,
            (Dictionary(a), Dictionary(b)) => a == b,
            (Set(a), Set(b)) => a == b,
            (Tuple(a), Tuple(b)) => a == b,
            _ => false, // Simplified for other complex types
        }
    }
}

impl Eq for Value {}

impl std::hash::Hash for Value {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        use Value::*;
        match self {
            Integer(i) => {
                0u8.hash(state);
                i.hash(state);
            }
            Float(f) => {
                1u8.hash(state);
                f.to_bits().hash(state); // Hash the bits representation
            }
            Number(f) => {
                2u8.hash(state);
                f.to_bits().hash(state);
            }
            Boolean(b) => {
                3u8.hash(state);
                b.hash(state);
            }
            String(s) => {
                4u8.hash(state);
                s.hash(state);
            }
            Null => 5u8.hash(state),
            Nil => 6u8.hash(state),
            List(v) => {
                7u8.hash(state);
                v.hash(state);
            }
            Dictionary(v) => {
                8u8.hash(state);
                v.hash(state);
            }
            Set(v) => {
                9u8.hash(state);
                v.hash(state);
            }
            Tuple(v) => {
                10u8.hash(state);
                v.hash(state);
            }
            _ => {
                // For complex types, hash a discriminant
                std::mem::discriminant(self).hash(state);
            }
        }
    }
} 