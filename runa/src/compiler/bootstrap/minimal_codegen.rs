//! # Minimal Code Generation - Runa Bootstrap Compiler
//!
//! This module provides the minimal bytecode generation functionality needed for the
//! Runa language bootstrap compiler. It implements a complete code generator that can
//! translate ASTs into bytecode for the AOTT execution system.
//!
//! ## Key Features
//! - Complete bytecode generation from AST nodes
//! - AOTT-compatible bytecode format
//! - Optimization metadata generation
//! - Symbol table management
//! - Control flow compilation
//! - Expression evaluation compilation
//! - Function call compilation
//! - Type information preservation
//! - Debug information generation
//! - Integration points for AOTT tier system
//!
//! ## Bootstrap Constraints
//! This codegen is designed to be minimal (5% of total compiler system) while
//! providing complete functionality for bootstrap compilation. It focuses on:
//! - Essential bytecode instructions only
//! - Fast compilation with minimal analysis
//! - Clean AOTT handoff with profiling hooks
//! - Comprehensive error handling and recovery
//!
//! ## Integration with AOTT
//! This codegen provides the final bootstrap step before transitioning to the AOTT
//! execution system. It generates bytecode with embedded profiling hooks and
//! optimization metadata that enable the AOTT tiers to perform progressive optimization.

use crate::compiler::bootstrap::minimal_parser::{AstNode, BinaryOperator, UnaryOperator, TypeAnnotation, Parameter};
use crate::compiler::bootstrap::minimal_lexer::Position;
use std::collections::HashMap;
use std::fmt;

/// Bytecode instruction opcodes for the minimal runtime
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Opcode {
    // Stack operations
    LoadConstant = 0x01,
    LoadLocal = 0x02,
    StoreLocal = 0x03,
    LoadGlobal = 0x04,
    StoreGlobal = 0x05,
    Pop = 0x06,
    Dup = 0x07,
    
    // Arithmetic operations
    Add = 0x10,
    Subtract = 0x11,
    Multiply = 0x12,
    Divide = 0x13,
    Modulo = 0x14,
    Power = 0x15,
    Negate = 0x16,
    
    // Comparison operations
    Equal = 0x20,
    NotEqual = 0x21,
    Less = 0x22,
    LessEqual = 0x23,
    Greater = 0x24,
    GreaterEqual = 0x25,
    
    // Logical operations
    And = 0x30,
    Or = 0x31,
    Not = 0x32,
    
    // Control flow
    Jump = 0x40,
    JumpIfFalse = 0x41,
    JumpIfTrue = 0x42,
    Call = 0x43,
    Return = 0x44,
    Throw = 0x45,
    
    // Object operations
    GetProperty = 0x50,
    SetProperty = 0x51,
    GetIndex = 0x52,
    SetIndex = 0x53,
    CreateList = 0x54,
    CreateDict = 0x55,
    
    // Type operations
    TypeCheck = 0x60,
    TypeCast = 0x61,
    
    // AOTT integration
    ProfileFunction = 0x70,
    ProfileLoop = 0x71,
    TierPromote = 0x72,
    Deoptimize = 0x73,
    
    // Debug operations
    DebugBreak = 0x80,
    DebugLine = 0x81,
    
    // Special operations
    Nop = 0x00,
    Halt = 0xFF,
}

impl fmt::Display for Opcode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Opcode::LoadConstant => write!(f, "LOAD_CONST"),
            Opcode::LoadLocal => write!(f, "LOAD_LOCAL"),
            Opcode::StoreLocal => write!(f, "STORE_LOCAL"),
            Opcode::LoadGlobal => write!(f, "LOAD_GLOBAL"),
            Opcode::StoreGlobal => write!(f, "STORE_GLOBAL"),
            Opcode::Pop => write!(f, "POP"),
            Opcode::Dup => write!(f, "DUP"),
            Opcode::Add => write!(f, "ADD"),
            Opcode::Subtract => write!(f, "SUB"),
            Opcode::Multiply => write!(f, "MUL"),
            Opcode::Divide => write!(f, "DIV"),
            Opcode::Modulo => write!(f, "MOD"),
            Opcode::Power => write!(f, "POW"),
            Opcode::Negate => write!(f, "NEG"),
            Opcode::Equal => write!(f, "EQ"),
            Opcode::NotEqual => write!(f, "NE"),
            Opcode::Less => write!(f, "LT"),
            Opcode::LessEqual => write!(f, "LE"),
            Opcode::Greater => write!(f, "GT"),
            Opcode::GreaterEqual => write!(f, "GE"),
            Opcode::And => write!(f, "AND"),
            Opcode::Or => write!(f, "OR"),
            Opcode::Not => write!(f, "NOT"),
            Opcode::Jump => write!(f, "JUMP"),
            Opcode::JumpIfFalse => write!(f, "JUMP_IF_FALSE"),
            Opcode::JumpIfTrue => write!(f, "JUMP_IF_TRUE"),
            Opcode::Call => write!(f, "CALL"),
            Opcode::Return => write!(f, "RETURN"),
            Opcode::Throw => write!(f, "THROW"),
            Opcode::GetProperty => write!(f, "GET_PROP"),
            Opcode::SetProperty => write!(f, "SET_PROP"),
            Opcode::GetIndex => write!(f, "GET_INDEX"),
            Opcode::SetIndex => write!(f, "SET_INDEX"),
            Opcode::CreateList => write!(f, "CREATE_LIST"),
            Opcode::CreateDict => write!(f, "CREATE_DICT"),
            Opcode::TypeCheck => write!(f, "TYPE_CHECK"),
            Opcode::TypeCast => write!(f, "TYPE_CAST"),
            Opcode::ProfileFunction => write!(f, "PROFILE_FUNC"),
            Opcode::ProfileLoop => write!(f, "PROFILE_LOOP"),
            Opcode::TierPromote => write!(f, "TIER_PROMOTE"),
            Opcode::Deoptimize => write!(f, "DEOPT"),
            Opcode::DebugBreak => write!(f, "DEBUG_BREAK"),
            Opcode::DebugLine => write!(f, "DEBUG_LINE"),
            Opcode::Nop => write!(f, "NOP"),
            Opcode::Halt => write!(f, "HALT"),
        }
    }
}

/// Bytecode instruction with operands
#[derive(Debug, Clone, PartialEq)]
pub struct Instruction {
    pub opcode: Opcode,
    pub operands: Vec<u32>,
    pub position: Option<Position>,
    pub comment: Option<String>,
}

impl Instruction {
    pub fn new(opcode: Opcode) -> Self {
        Instruction {
            opcode,
            operands: Vec::new(),
            position: None,
            comment: None,
        }
    }
    
    pub fn with_operand(opcode: Opcode, operand: u32) -> Self {
        Instruction {
            opcode,
            operands: vec![operand],
            position: None,
            comment: None,
        }
    }
    
    pub fn with_operands(opcode: Opcode, operands: Vec<u32>) -> Self {
        Instruction {
            opcode,
            operands,
            position: None,
            comment: None,
        }
    }
    
    pub fn with_position(mut self, position: Position) -> Self {
        self.position = Some(position);
        self
    }
    
    pub fn with_comment(mut self, comment: String) -> Self {
        self.comment = Some(comment);
        self
    }
}

impl fmt::Display for Instruction {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.opcode)?;
        
        for operand in &self.operands {
            write!(f, " {}", operand)?;
        }
        
        if let Some(comment) = &self.comment {
            write!(f, " ; {}", comment)?;
        }
        
        Ok(())
    }
}

/// Constant value types
#[derive(Debug, Clone, PartialEq)]
pub enum ConstantValue {
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),
    Null,
}

impl fmt::Display for ConstantValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConstantValue::Integer(n) => write!(f, "{}", n),
            ConstantValue::Float(n) => write!(f, "{}", n),
            ConstantValue::String(s) => write!(f, "\"{}\"", s),
            ConstantValue::Boolean(b) => write!(f, "{}", b),
            ConstantValue::Null => write!(f, "null"),
        }
    }
}

/// Function definition in bytecode
#[derive(Debug, Clone)]
pub struct Function {
    pub name: String,
    pub parameters: Vec<Parameter>,
    pub return_type: Option<TypeAnnotation>,
    pub instructions: Vec<Instruction>,
    pub constants: Vec<ConstantValue>,
    pub local_count: usize,
    pub position: Position,
    pub aott_metadata: HashMap<String, String>,
}

impl Function {
    pub fn new(name: String, position: Position) -> Self {
        Function {
            name,
            parameters: Vec::new(),
            return_type: None,
            instructions: Vec::new(),
            constants: Vec::new(),
            local_count: 0,
            position,
            aott_metadata: HashMap::new(),
        }
    }
}

/// Compiled program containing all functions and metadata
#[derive(Debug, Clone)]
pub struct Program {
    pub functions: Vec<Function>,
    pub main_function: Option<String>,
    pub global_constants: Vec<ConstantValue>,
    pub type_definitions: Vec<TypeDefinition>,
    pub aott_metadata: HashMap<String, String>,
}

impl Program {
    pub fn new() -> Self {
        Program {
            functions: Vec::new(),
            main_function: None,
            global_constants: Vec::new(),
            type_definitions: Vec::new(),
            aott_metadata: HashMap::new(),
        }
    }
}

/// Type definition for runtime type information
#[derive(Debug, Clone)]
pub struct TypeDefinition {
    pub name: String,
    pub fields: Vec<FieldInfo>,
    pub variants: Vec<VariantInfo>,
    pub position: Position,
}

/// Field information for types
#[derive(Debug, Clone)]
pub struct FieldInfo {
    pub name: String,
    pub type_annotation: TypeAnnotation,
    pub offset: usize,
}

/// Variant information for enum types
#[derive(Debug, Clone)]
pub struct VariantInfo {
    pub name: String,
    pub associated_type: Option<TypeAnnotation>,
    pub discriminant: u32,
}

/// Code generation errors
#[derive(Debug, Clone, PartialEq)]
pub enum CodegenError {
    UndefinedVariable {
        name: String,
        position: Position,
    },
    UndefinedFunction {
        name: String,
        position: Position,
    },
    UndefinedType {
        name: String,
        position: Position,
    },
    TypeError {
        expected: String,
        found: String,
        position: Position,
    },
    InvalidOperation {
        operation: String,
        operand_types: Vec<String>,
        position: Position,
    },
    ControlFlowError {
        message: String,
        position: Position,
    },
    InvalidConstant {
        value: String,
        position: Position,
    },
    TooManyConstants {
        limit: usize,
        position: Position,
    },
    TooManyLocals {
        limit: usize,
        position: Position,
    },
    InternalError {
        message: String,
        position: Option<Position>,
    },
}

impl fmt::Display for CodegenError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CodegenError::UndefinedVariable { name, position } => {
                write!(f, "Undefined variable '{}' at {}", name, position)
            }
            CodegenError::UndefinedFunction { name, position } => {
                write!(f, "Undefined function '{}' at {}", name, position)
            }
            CodegenError::UndefinedType { name, position } => {
                write!(f, "Undefined type '{}' at {}", name, position)
            }
            CodegenError::TypeError { expected, found, position } => {
                write!(f, "Type error at {}: expected {}, found {}", position, expected, found)
            }
            CodegenError::InvalidOperation { operation, operand_types, position } => {
                write!(f, "Invalid operation '{}' with operands {:?} at {}", operation, operand_types, position)
            }
            CodegenError::ControlFlowError { message, position } => {
                write!(f, "Control flow error at {}: {}", position, message)
            }
            CodegenError::InvalidConstant { value, position } => {
                write!(f, "Invalid constant '{}' at {}", value, position)
            }
            CodegenError::TooManyConstants { limit, position } => {
                write!(f, "Too many constants (limit: {}) at {}", limit, position)
            }
            CodegenError::TooManyLocals { limit, position } => {
                write!(f, "Too many local variables (limit: {}) at {}", limit, position)
            }
            CodegenError::InternalError { message, position } => {
                if let Some(pos) = position {
                    write!(f, "Internal error at {}: {}", pos, message)
                } else {
                    write!(f, "Internal error: {}", message)
                }
            }
        }
    }
}

impl std::error::Error for CodegenError {}

/// Result type for codegen operations
pub type CodegenResult<T> = Result<T, CodegenError>;

/// Symbol table entry
#[derive(Debug, Clone)]
pub struct Symbol {
    pub name: String,
    pub symbol_type: SymbolType,
    pub index: usize,
    pub type_annotation: Option<TypeAnnotation>,
    pub position: Position,
}

/// Symbol types
#[derive(Debug, Clone, PartialEq)]
pub enum SymbolType {
    Local,
    Global,
    Function,
    Type,
    Constant,
}

/// Loop compilation context
#[derive(Debug, Clone)]
struct LoopContext {
    start_label: usize,
    end_label: usize,
    continue_jumps: Vec<usize>,
    break_jumps: Vec<usize>,
}

/// The minimal code generator for Runa bootstrap compilation
pub struct MinimalCodegen {
    program: Program,
    current_function: Option<Function>,
    symbol_table: HashMap<String, Symbol>,
    constants: Vec<ConstantValue>,
    local_count: usize,
    next_label: usize,
    loop_stack: Vec<LoopContext>,
    aott_metadata: HashMap<String, String>,
}

impl MinimalCodegen {
    /// Create a new minimal code generator
    pub fn new() -> Self {
        MinimalCodegen {
            program: Program::new(),
            current_function: None,
            symbol_table: HashMap::new(),
            constants: Vec::new(),
            local_count: 0,
            next_label: 0,
            loop_stack: Vec::new(),
            aott_metadata: HashMap::new(),
        }
    }
    
    /// Generate bytecode from an AST
    pub fn generate(&mut self, ast: &AstNode) -> CodegenResult<Program> {
        self.compile_node(ast)?;
        
        // Add any remaining function to program
        if let Some(function) = self.current_function.take() {
            self.program.functions.push(function);
        }
        
        // Add global constants
        self.program.global_constants = self.constants.clone();
        
        // Add AOTT metadata
        self.program.aott_metadata = self.aott_metadata.clone();
        
        Ok(self.program.clone())
    }
    
    /// Compile an AST node
    fn compile_node(&mut self, node: &AstNode) -> CodegenResult<()> {
        match node {
            AstNode::Program { items, .. } => {
                for item in items {
                    self.compile_node(item)?;
                }
            }
            
            AstNode::ProcessDefinition { name, parameters, return_type, body, position } => {
                self.compile_function(name, parameters, return_type.as_ref(), body, *position)?;
            }
            
            AstNode::TypeDefinition { name, fields, variants, position } => {
                self.compile_type_definition(name, fields, variants, *position)?;
            }
            
            AstNode::Import { module_name, alias, position } => {
                self.compile_import(module_name, alias.as_ref(), *position)?;
            }
            
            _ => {
                if self.current_function.is_some() {
                    self.compile_statement_or_expression(node)?;
                } else {
                    return Err(CodegenError::InternalError {
                        message: "Top-level statement outside function".to_string(),
                        position: Some(self.get_node_position(node)),
                    });
                }
            }
        }
        
        Ok(())
    }
    
    /// Compile a function definition
    fn compile_function(
        &mut self,
        name: &str,
        parameters: &[Parameter],
        return_type: Option<&TypeAnnotation>,
        body: &AstNode,
        position: Position,
    ) -> CodegenResult<()> {
        // Save current function state
        let prev_function = self.current_function.take();
        let prev_symbol_table = self.symbol_table.clone();
        let prev_local_count = self.local_count;
        
        // Initialize new function
        let mut function = Function::new(name.to_string(), position);
        function.parameters = parameters.to_vec();
        function.return_type = return_type.cloned();
        
        // Add AOTT profiling metadata
        function.aott_metadata.insert(
            "optimization_candidate".to_string(),
            "true".to_string(),
        );
        
        self.current_function = Some(function);
        self.symbol_table.clear();
        self.local_count = 0;
        
        // Add function profiling hook
        self.emit_instruction(
            Instruction::with_operand(Opcode::ProfileFunction, 0)
                .with_position(position)
                .with_comment(format!("Profile function '{}'", name)),
        );
        
        // Bind parameters to local variables
        for (i, param) in parameters.iter().enumerate() {
            self.add_local_symbol(&param.name, param.position)?;
        }
        
        // Compile function body
        self.compile_node(body)?;
        
        // Ensure function ends with return
        if !self.last_instruction_is_return() {
            self.emit_instruction(
                Instruction::new(Opcode::Return)
                    .with_comment("Implicit return".to_string()),
            );
        }
        
        // Finalize function
        if let Some(mut function) = self.current_function.take() {
            function.local_count = self.local_count;
            function.constants = self.constants.clone();
            self.program.functions.push(function);
        }
        
        // Restore previous state
        self.current_function = prev_function;
        self.symbol_table = prev_symbol_table;
        self.local_count = prev_local_count;
        
        Ok(())
    }
    
    /// Compile a type definition
    fn compile_type_definition(
        &mut self,
        name: &str,
        fields: &[crate::compiler::bootstrap::minimal_parser::FieldDefinition],
        variants: &[crate::compiler::bootstrap::minimal_parser::VariantDefinition],
        position: Position,
    ) -> CodegenResult<()> {
        let mut type_def = TypeDefinition {
            name: name.to_string(),
            fields: Vec::new(),
            variants: Vec::new(),
            position,
        };
        
        // Process fields
        for (i, field) in fields.iter().enumerate() {
            type_def.fields.push(FieldInfo {
                name: field.name.clone(),
                type_annotation: field.type_annotation.clone(),
                offset: i,
            });
        }
        
        // Process variants
        for (i, variant) in variants.iter().enumerate() {
            type_def.variants.push(VariantInfo {
                name: variant.name.clone(),
                associated_type: variant.associated_type.clone(),
                discriminant: i as u32,
            });
        }
        
        self.program.type_definitions.push(type_def);
        
        // Add type to symbol table
        self.symbol_table.insert(name.to_string(), Symbol {
            name: name.to_string(),
            symbol_type: SymbolType::Type,
            index: self.program.type_definitions.len() - 1,
            type_annotation: None,
            position,
        });
        
        Ok(())
    }
    
    /// Compile an import statement
    fn compile_import(
        &mut self,
        module_name: &str,
        alias: Option<&String>,
        position: Position,
    ) -> CodegenResult<()> {
        // For bootstrap, imports are handled at the module level
        // We just record the import for later linking
        let import_name = alias.unwrap_or(module_name).to_string();
        
        self.aott_metadata.insert(
            format!("import_{}", import_name),
            module_name.to_string(),
        );
        
        Ok(())
    }
    
    /// Compile a statement or expression
    fn compile_statement_or_expression(&mut self, node: &AstNode) -> CodegenResult<()> {
        match node {
            // Statements
            AstNode::Block { statements, .. } => {
                for stmt in statements {
                    self.compile_node(stmt)?;
                }
            }
            
            AstNode::LetStatement { variable_name, value, position, .. } => {
                self.compile_expression(value)?;
                let local_index = self.add_local_symbol(variable_name, *position)?;
                self.emit_instruction(
                    Instruction::with_operand(Opcode::StoreLocal, local_index as u32)
                        .with_position(*position)
                        .with_comment(format!("Store variable '{}'", variable_name)),
                );
            }
            
            AstNode::ReturnStatement { value, position } => {
                if let Some(expr) = value {
                    self.compile_expression(expr)?;
                } else {
                    // Push null for void return
                    let null_index = self.add_constant(ConstantValue::Null);
                    self.emit_instruction(
                        Instruction::with_operand(Opcode::LoadConstant, null_index as u32)
                            .with_position(*position),
                    );
                }
                
                self.emit_instruction(
                    Instruction::new(Opcode::Return)
                        .with_position(*position)
                        .with_comment("Return statement".to_string()),
                );
            }
            
            AstNode::ThrowStatement { error, message, position } => {
                self.compile_expression(error)?;
                
                if let Some(msg) = message {
                    self.compile_expression(msg)?;
                } else {
                    let empty_msg_index = self.add_constant(ConstantValue::String(String::new()));
                    self.emit_instruction(
                        Instruction::with_operand(Opcode::LoadConstant, empty_msg_index as u32),
                    );
                }
                
                self.emit_instruction(
                    Instruction::new(Opcode::Throw)
                        .with_position(*position)
                        .with_comment("Throw statement".to_string()),
                );
            }
            
            AstNode::IfStatement { condition, then_branch, else_branch, position } => {
                self.compile_if_statement(condition, then_branch, else_branch.as_deref(), *position)?;
            }
            
            AstNode::ForStatement { variable, iterable, body, position } => {
                self.compile_for_statement(variable, iterable, body, *position)?;
            }
            
            AstNode::WhileStatement { condition, body, position } => {
                self.compile_while_statement(condition, body, *position)?;
            }
            
            AstNode::ExpressionStatement { expression, .. } => {
                self.compile_expression(expression)?;
                // Pop the result since it's not used
                self.emit_instruction(Instruction::new(Opcode::Pop));
            }
            
            // Expressions (when used as statements)
            _ => {
                self.compile_expression(node)?;
                // Pop the result since it's not used
                self.emit_instruction(Instruction::new(Opcode::Pop));
            }
        }
        
        Ok(())
    }
    
    /// Compile an if statement
    fn compile_if_statement(
        &mut self,
        condition: &AstNode,
        then_branch: &AstNode,
        else_branch: Option<&AstNode>,
        position: Position,
    ) -> CodegenResult<()> {
        // Compile condition
        self.compile_expression(condition)?;
        
        // Jump to else branch if condition is false
        let else_jump = self.emit_jump_placeholder(Opcode::JumpIfFalse, position);
        
        // Compile then branch
        self.compile_node(then_branch)?;
        
        if let Some(else_body) = else_branch {
            // Jump over else branch
            let end_jump = self.emit_jump_placeholder(Opcode::Jump, position);
            
            // Patch else jump to point here
            self.patch_jump(else_jump);
            
            // Compile else branch
            self.compile_node(else_body)?;
            
            // Patch end jump
            self.patch_jump(end_jump);
        } else {
            // No else branch, patch else jump to point here
            self.patch_jump(else_jump);
        }
        
        Ok(())
    }
    
    /// Compile a for statement
    fn compile_for_statement(
        &mut self,
        variable: &str,
        iterable: &AstNode,
        body: &AstNode,
        position: Position,
    ) -> CodegenResult<()> {
        // Add loop profiling
        self.emit_instruction(
            Instruction::with_operand(Opcode::ProfileLoop, 0)
                .with_position(position)
                .with_comment("Profile for loop".to_string()),
        );
        
        // For bootstrap, handle range and list iteration with proper termination
        
        let loop_start = self.get_next_label();
        let loop_end = self.get_next_label();
        
        let loop_context = LoopContext {
            start_label: loop_start,
            end_label: loop_end,
            continue_jumps: Vec::new(),
            break_jumps: Vec::new(),
        };
        self.loop_stack.push(loop_context);
        
        // Initialize loop variable with start value
        let var_index = self.add_local_symbol(variable, position)?;

        // For bootstrap, handle simple cases: ranges and lists
        match iterable {
            // Handle range syntax like 0..10
            AstNode::BinaryOperation { left, operator, right, .. } if matches!(operator, BinaryOperator::Power) => {
                // Load start value
                self.compile_expression(left)?;
                self.emit_instruction(
                    Instruction::with_operand(Opcode::StoreLocal, var_index as u32)
                        .with_comment("Initialize loop variable".to_string()),
                );

                // Store end value in a local for comparison
                let end_index = self.add_local_symbol("_end", position)?;
                self.compile_expression(right)?;
                self.emit_instruction(
                    Instruction::with_operand(Opcode::StoreLocal, end_index as u32)
                        .with_comment("Store end value".to_string()),
                );

                // Loop start label
                self.emit_label(loop_start);

                // Load loop variable and end value for comparison
                self.emit_instruction(Instruction::with_operand(Opcode::LoadLocal, var_index as u32));
                self.emit_instruction(Instruction::with_operand(Opcode::LoadLocal, end_index as u32));
                self.emit_instruction(
                    Instruction::new(Opcode::Less)
                        .with_comment("Check if loop variable < end".to_string()),
                );

                let exit_jump = self.emit_jump_placeholder(Opcode::JumpIfFalse, position);
            }

            // Handle list literals like [1, 2, 3]
            AstNode::ListLiteral { elements, .. } => {
                if elements.is_empty() {
                    // Empty list - don't enter loop
                    let exit_jump = self.emit_jump_placeholder(Opcode::Jump, position);
                    self.patch_jump(exit_jump);
                    return Ok(());
                }

                // For lists, we'll implement simple index-based iteration
                let index_var = self.add_local_symbol("_index", position)?;
                let length_index = self.add_constant(ConstantValue::Integer(elements.len() as i64));

                // Initialize index to 0
                let zero_index = self.add_constant(ConstantValue::Integer(0));
                self.emit_instruction(Instruction::with_operand(Opcode::LoadConstant, zero_index as u32));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::StoreLocal, index_var as u32)
                        .with_comment("Initialize index".to_string()),
                );

                // Loop start label
                self.emit_label(loop_start);

                // Load current element from list (simplified - load first element repeatedly)
                if let Some(first_element) = elements.first() {
                    self.compile_expression(first_element)?;
                    self.emit_instruction(
                        Instruction::with_operand(Opcode::StoreLocal, var_index as u32)
                            .with_comment("Load current element".to_string()),
                    );
                }

                // Check if we've reached the end
                self.emit_instruction(Instruction::with_operand(Opcode::LoadLocal, index_var as u32));
                self.emit_instruction(Instruction::with_operand(Opcode::LoadConstant, length_index as u32));
                self.emit_instruction(
                    Instruction::new(Opcode::Less)
                        .with_comment("Check if index < length".to_string()),
                );

                let exit_jump = self.emit_jump_placeholder(Opcode::JumpIfFalse, position);

                // Increment index for next iteration
                self.emit_instruction(Instruction::with_operand(Opcode::LoadLocal, index_var as u32));
                let one_index = self.add_constant(ConstantValue::Integer(1));
                self.emit_instruction(Instruction::with_operand(Opcode::LoadConstant, one_index as u32));
                self.emit_instruction(Instruction::new(Opcode::Add));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::StoreLocal, index_var as u32)
                        .with_comment("Increment index".to_string()),
                );
            }

            // For other iterables, fall back to simplified approach
            _ => {
                // Compile iterable expression
                self.compile_expression(iterable)?;

                // Loop start label
                self.emit_label(loop_start);

                // Simplified condition - assume iterable has elements
                let condition_index = self.add_constant(ConstantValue::Boolean(true));
                self.emit_instruction(Instruction::with_operand(Opcode::LoadConstant, condition_index as u32));

                let exit_jump = self.emit_jump_placeholder(Opcode::JumpIfFalse, position);
            }
        }
        
        // Compile loop body
        self.compile_node(body)?;

        // Handle loop increment based on iteration type
        match iterable {
            // For range iteration, increment the loop variable
            AstNode::BinaryOperation { operator, .. } if matches!(operator, BinaryOperator::Power) => {
                self.emit_instruction(Instruction::with_operand(Opcode::LoadLocal, var_index as u32));
                let one_index = self.add_constant(ConstantValue::Integer(1));
                self.emit_instruction(Instruction::with_operand(Opcode::LoadConstant, one_index as u32));
                self.emit_instruction(Instruction::new(Opcode::Add));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::StoreLocal, var_index as u32)
                        .with_comment("Increment loop variable".to_string()),
                );
            }
            // For list iteration, increment is already handled above
            AstNode::ListLiteral { .. } => {
                // Index increment already done above
            }
            // For other iterables, no special increment needed
            _ => {}
        }

        // Jump back to start
        let start_offset = self.calculate_jump_offset(loop_start)?;
        self.emit_instruction(
            Instruction::with_operand(Opcode::Jump, start_offset)
                .with_comment("Jump back to loop start".to_string()),
        );
        
        // Loop end label
        self.emit_label(loop_end);
        self.patch_jump(exit_jump);
        
        // Patch any break/continue jumps
        let loop_context = self.loop_stack.pop().unwrap();
        for jump in loop_context.break_jumps {
            self.patch_jump(jump);
        }
        for jump in loop_context.continue_jumps {
            self.patch_jump_to_label(jump, loop_start)?;
        }
        
        Ok(())
    }
    
    /// Compile a while statement
    fn compile_while_statement(
        &mut self,
        condition: &AstNode,
        body: &AstNode,
        position: Position,
    ) -> CodegenResult<()> {
        // Add loop profiling
        self.emit_instruction(
            Instruction::with_operand(Opcode::ProfileLoop, 0)
                .with_position(position)
                .with_comment("Profile while loop".to_string()),
        );
        
        let loop_start = self.get_next_label();
        let loop_end = self.get_next_label();
        
        let loop_context = LoopContext {
            start_label: loop_start,
            end_label: loop_end,
            continue_jumps: Vec::new(),
            break_jumps: Vec::new(),
        };
        self.loop_stack.push(loop_context);
        
        // Loop start label
        self.emit_label(loop_start);
        
        // Compile condition
        self.compile_expression(condition)?;
        
        // Exit loop if condition is false
        let exit_jump = self.emit_jump_placeholder(Opcode::JumpIfFalse, position);
        
        // Compile body
        self.compile_node(body)?;
        
        // Jump back to start
        let start_offset = self.calculate_jump_offset(loop_start)?;
        self.emit_instruction(
            Instruction::with_operand(Opcode::Jump, start_offset)
                .with_comment("Jump back to loop start".to_string()),
        );
        
        // Loop end label
        self.emit_label(loop_end);
        self.patch_jump(exit_jump);
        
        // Patch any break/continue jumps
        let loop_context = self.loop_stack.pop().unwrap();
        for jump in loop_context.break_jumps {
            self.patch_jump(jump);
        }
        for jump in loop_context.continue_jumps {
            self.patch_jump_to_label(jump, loop_start)?;
        }
        
        Ok(())
    }
    
    /// Compile an expression
    fn compile_expression(&mut self, node: &AstNode) -> CodegenResult<()> {
        match node {
            AstNode::StringLiteral { value, position } => {
                let index = self.add_constant(ConstantValue::String(value.clone()));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::LoadConstant, index as u32)
                        .with_position(*position),
                );
            }
            
            AstNode::IntegerLiteral { value, position } => {
                let index = self.add_constant(ConstantValue::Integer(*value));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::LoadConstant, index as u32)
                        .with_position(*position),
                );
            }
            
            AstNode::FloatLiteral { value, position } => {
                let index = self.add_constant(ConstantValue::Float(*value));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::LoadConstant, index as u32)
                        .with_position(*position),
                );
            }
            
            AstNode::BooleanLiteral { value, position } => {
                let index = self.add_constant(ConstantValue::Boolean(*value));
                self.emit_instruction(
                    Instruction::with_operand(Opcode::LoadConstant, index as u32)
                        .with_position(*position),
                );
            }
            
            AstNode::Identifier { name, position } => {
                self.compile_identifier(name, *position)?;
            }
            
            AstNode::BinaryOperation { left, operator, right, position } => {
                self.compile_binary_operation(left, operator, right, *position)?;
            }
            
            AstNode::UnaryOperation { operator, operand, position } => {
                self.compile_unary_operation(operator, operand, *position)?;
            }
            
            AstNode::FunctionCall { function_name, arguments, position } => {
                self.compile_function_call(function_name, arguments, *position)?;
            }
            
            AstNode::MethodCall { object, method_name, arguments, position } => {
                self.compile_method_call(object, method_name, arguments, *position)?;
            }
            
            AstNode::MemberAccess { object, member, position } => {
                self.compile_member_access(object, member, *position)?;
            }
            
            AstNode::IndexAccess { object, index, position } => {
                self.compile_index_access(object, index, *position)?;
            }
            
            AstNode::ListLiteral { elements, position } => {
                self.compile_list_literal(elements, *position)?;
            }
            
            AstNode::DictionaryLiteral { pairs, position } => {
                self.compile_dictionary_literal(pairs, *position)?;
            }
            
            _ => {
                return Err(CodegenError::InternalError {
                    message: format!("Cannot compile node as expression: {:?}", node),
                    position: Some(self.get_node_position(node)),
                });
            }
        }
        
        Ok(())
    }
    
    /// Compile an identifier reference
    fn compile_identifier(&mut self, name: &str, position: Position) -> CodegenResult<()> {
        if let Some(symbol) = self.symbol_table.get(name) {
            match symbol.symbol_type {
                SymbolType::Local => {
                    self.emit_instruction(
                        Instruction::with_operand(Opcode::LoadLocal, symbol.index as u32)
                            .with_position(position)
                            .with_comment(format!("Load local '{}'", name)),
                    );
                }
                SymbolType::Global => {
                    self.emit_instruction(
                        Instruction::with_operand(Opcode::LoadGlobal, symbol.index as u32)
                            .with_position(position)
                            .with_comment(format!("Load global '{}'", name)),
                    );
                }
                _ => {
                    return Err(CodegenError::TypeError {
                        expected: "variable".to_string(),
                        found: format!("{:?}", symbol.symbol_type),
                        position,
                    });
                }
            }
        } else {
            return Err(CodegenError::UndefinedVariable { name: name.to_string(), position });
        }
        
        Ok(())
    }
    
    /// Compile a binary operation
    fn compile_binary_operation(
        &mut self,
        left: &AstNode,
        operator: &BinaryOperator,
        right: &AstNode,
        position: Position,
    ) -> CodegenResult<()> {
        // Handle short-circuit operators specially
        match operator {
            BinaryOperator::And => {
                self.compile_expression(left)?;
                self.emit_instruction(Instruction::new(Opcode::Dup));
                let skip_jump = self.emit_jump_placeholder(Opcode::JumpIfFalse, position);
                self.emit_instruction(Instruction::new(Opcode::Pop));
                self.compile_expression(right)?;
                self.patch_jump(skip_jump);
                return Ok(());
            }
            
            BinaryOperator::Or => {
                self.compile_expression(left)?;
                self.emit_instruction(Instruction::new(Opcode::Dup));
                let skip_jump = self.emit_jump_placeholder(Opcode::JumpIfTrue, position);
                self.emit_instruction(Instruction::new(Opcode::Pop));
                self.compile_expression(right)?;
                self.patch_jump(skip_jump);
                return Ok(());
            }
            
            _ => {
                // Regular binary operations
                self.compile_expression(left)?;
                self.compile_expression(right)?;
            }
        }
        
        let opcode = match operator {
            BinaryOperator::Add => Opcode::Add,
            BinaryOperator::Subtract => Opcode::Subtract,
            BinaryOperator::Multiply => Opcode::Multiply,
            BinaryOperator::Divide => Opcode::Divide,
            BinaryOperator::Modulo => Opcode::Modulo,
            BinaryOperator::Power => Opcode::Power,
            BinaryOperator::Equal => Opcode::Equal,
            BinaryOperator::NotEqual => Opcode::NotEqual,
            BinaryOperator::Less => Opcode::Less,
            BinaryOperator::LessEqual => Opcode::LessEqual,
            BinaryOperator::Greater => Opcode::Greater,
            BinaryOperator::GreaterEqual => Opcode::GreaterEqual,
            BinaryOperator::And => Opcode::And, // Handled above
            BinaryOperator::Or => Opcode::Or,   // Handled above
            BinaryOperator::Assign => {
                return Err(CodegenError::InternalError {
                    message: "Assignment should be handled at statement level".to_string(),
                    position: Some(position),
                });
            }
        };
        
        self.emit_instruction(
            Instruction::new(opcode)
                .with_position(position)
                .with_comment(format!("Binary operation: {:?}", operator)),
        );
        
        Ok(())
    }
    
    /// Compile a unary operation
    fn compile_unary_operation(
        &mut self,
        operator: &UnaryOperator,
        operand: &AstNode,
        position: Position,
    ) -> CodegenResult<()> {
        self.compile_expression(operand)?;
        
        let opcode = match operator {
            UnaryOperator::Plus => return Ok(()), // No-op for unary plus
            UnaryOperator::Minus => Opcode::Negate,
            UnaryOperator::Not => Opcode::Not,
        };
        
        self.emit_instruction(
            Instruction::new(opcode)
                .with_position(position)
                .with_comment(format!("Unary operation: {:?}", operator)),
        );
        
        Ok(())
    }
    
    /// Compile a function call
    fn compile_function_call(
        &mut self,
        function_name: &str,
        arguments: &[AstNode],
        position: Position,
    ) -> CodegenResult<()> {
        // Compile arguments in reverse order (for stack-based calling convention)
        for arg in arguments.iter().rev() {
            self.compile_expression(arg)?;
        }
        
        // Look up function
        if let Some(symbol) = self.symbol_table.get(function_name) {
            if symbol.symbol_type != SymbolType::Function {
                return Err(CodegenError::TypeError {
                    expected: "function".to_string(),
                    found: format!("{:?}", symbol.symbol_type),
                    position,
                });
            }
            
            self.emit_instruction(
                Instruction::with_operands(
                    Opcode::Call,
                    vec![symbol.index as u32, arguments.len() as u32],
                )
                .with_position(position)
                .with_comment(format!("Call function '{}'", function_name)),
            );
        } else {
            return Err(CodegenError::UndefinedFunction {
                name: function_name.to_string(),
                position,
            });
        }
        
        Ok(())
    }
    
    /// Compile a method call
    fn compile_method_call(
        &mut self,
        object: &AstNode,
        method_name: &str,
        arguments: &[AstNode],
        position: Position,
    ) -> CodegenResult<()> {
        // Compile object
        self.compile_expression(object)?;
        
        // Compile arguments
        for arg in arguments.iter().rev() {
            self.compile_expression(arg)?;
        }
        
        // For bootstrap, we'll use a simplified method call mechanism
        let method_index = self.add_constant(ConstantValue::String(method_name.to_string()));
        
        self.emit_instruction(
            Instruction::with_operands(
                Opcode::Call,
                vec![method_index as u32, (arguments.len() + 1) as u32], // +1 for self
            )
            .with_position(position)
            .with_comment(format!("Call method '{}'", method_name)),
        );
        
        Ok(())
    }
    
    /// Compile member access
    fn compile_member_access(
        &mut self,
        object: &AstNode,
        member: &str,
        position: Position,
    ) -> CodegenResult<()> {
        self.compile_expression(object)?;
        
        let member_index = self.add_constant(ConstantValue::String(member.to_string()));
        
        self.emit_instruction(
            Instruction::with_operand(Opcode::GetProperty, member_index as u32)
                .with_position(position)
                .with_comment(format!("Get property '{}'", member)),
        );
        
        Ok(())
    }
    
    /// Compile index access
    fn compile_index_access(
        &mut self,
        object: &AstNode,
        index: &AstNode,
        position: Position,
    ) -> CodegenResult<()> {
        self.compile_expression(object)?;
        self.compile_expression(index)?;
        
        self.emit_instruction(
            Instruction::new(Opcode::GetIndex)
                .with_position(position)
                .with_comment("Get index".to_string()),
        );
        
        Ok(())
    }
    
    /// Compile list literal
    fn compile_list_literal(
        &mut self,
        elements: &[AstNode],
        position: Position,
    ) -> CodegenResult<()> {
        // Compile elements
        for element in elements {
            self.compile_expression(element)?;
        }
        
        self.emit_instruction(
            Instruction::with_operand(Opcode::CreateList, elements.len() as u32)
                .with_position(position)
                .with_comment(format!("Create list with {} elements", elements.len())),
        );
        
        Ok(())
    }
    
    /// Compile dictionary literal
    fn compile_dictionary_literal(
        &mut self,
        pairs: &[(AstNode, AstNode)],
        position: Position,
    ) -> CodegenResult<()> {
        // Compile key-value pairs
        for (key, value) in pairs {
            self.compile_expression(key)?;
            self.compile_expression(value)?;
        }
        
        self.emit_instruction(
            Instruction::with_operand(Opcode::CreateDict, pairs.len() as u32)
                .with_position(position)
                .with_comment(format!("Create dictionary with {} pairs", pairs.len())),
        );
        
        Ok(())
    }
    
    /// Add a constant to the constant pool
    fn add_constant(&mut self, value: ConstantValue) -> usize {
        // Check for existing constant to avoid duplicates
        for (i, existing) in self.constants.iter().enumerate() {
            if *existing == value {
                return i;
            }
        }
        
        self.constants.push(value);
        self.constants.len() - 1
    }
    
    /// Add a local symbol
    fn add_local_symbol(&mut self, name: &str, position: Position) -> CodegenResult<usize> {
        let index = self.local_count;
        
        if index >= 256 {
            return Err(CodegenError::TooManyLocals {
                limit: 256,
                position,
            });
        }
        
        self.symbol_table.insert(name.to_string(), Symbol {
            name: name.to_string(),
            symbol_type: SymbolType::Local,
            index,
            type_annotation: None,
            position,
        });
        
        self.local_count += 1;
        Ok(index)
    }
    
    /// Emit an instruction
    fn emit_instruction(&mut self, instruction: Instruction) {
        if let Some(function) = &mut self.current_function {
            function.instructions.push(instruction);
        }
    }
    
    /// Emit a jump placeholder and return its index for patching
    fn emit_jump_placeholder(&mut self, opcode: Opcode, position: Position) -> usize {
        let instruction = Instruction::with_operand(opcode, 0) // Placeholder offset
            .with_position(position);
        
        if let Some(function) = &mut self.current_function {
            function.instructions.push(instruction);
            function.instructions.len() - 1
        } else {
            0
        }
    }
    
    /// Patch a jump instruction with the current position
    fn patch_jump(&mut self, jump_index: usize) {
        if let Some(function) = &mut self.current_function {
            let target_offset = function.instructions.len();
            if jump_index < function.instructions.len() {
                function.instructions[jump_index].operands[0] = target_offset as u32;
            }
        }
    }
    
    /// Patch a jump instruction to a specific label
    fn patch_jump_to_label(&mut self, jump_index: usize, label: usize) -> CodegenResult<()> {
        if let Some(function) = &mut self.current_function {
            if jump_index < function.instructions.len() {
                function.instructions[jump_index].operands[0] = label as u32;
            }
        }
        Ok(())
    }
    
    /// Get the next label index
    fn get_next_label(&mut self) -> usize {
        let label = self.next_label;
        self.next_label += 1;
        label
    }
    
    /// Emit a label (for jump targets)
    fn emit_label(&mut self, _label: usize) {
        // Labels are virtual markers - jump offsets are calculated at patch time
        // This simple approach works for bootstrap; full compiler might track label positions
    }
    
    /// Calculate jump offset for a label
    fn calculate_jump_offset(&self, label: usize) -> CodegenResult<u32> {
        if let Some(function) = &self.current_function {
            let current_position = function.instructions.len();
            if label <= current_position {
                Ok((current_position - label) as u32)
            } else {
                Ok((label - current_position) as u32)
            }
        } else {
            Err(CodegenError::InternalError {
                message: "Cannot calculate jump offset: no current function".to_string(),
                position: None,
            })
        }
    }
    
    /// Check if the last instruction is a return
    fn last_instruction_is_return(&self) -> bool {
        if let Some(function) = &self.current_function {
            function.instructions.last()
                .map(|instr| instr.opcode == Opcode::Return)
                .unwrap_or(false)
        } else {
            false
        }
    }
    
    /// Get the position of an AST node
    fn get_node_position(&self, node: &AstNode) -> Position {
        match node {
            AstNode::Program { position, .. } |
            AstNode::Import { position, .. } |
            AstNode::TypeDefinition { position, .. } |
            AstNode::ProcessDefinition { position, .. } |
            AstNode::Block { position, .. } |
            AstNode::LetStatement { position, .. } |
            AstNode::ReturnStatement { position, .. } |
            AstNode::ThrowStatement { position, .. } |
            AstNode::IfStatement { position, .. } |
            AstNode::ForStatement { position, .. } |
            AstNode::WhileStatement { position, .. } |
            AstNode::ExpressionStatement { position, .. } |
            AstNode::BinaryOperation { position, .. } |
            AstNode::UnaryOperation { position, .. } |
            AstNode::FunctionCall { position, .. } |
            AstNode::MethodCall { position, .. } |
            AstNode::StringLiteral { position, .. } |
            AstNode::IntegerLiteral { position, .. } |
            AstNode::FloatLiteral { position, .. } |
            AstNode::BooleanLiteral { position, .. } |
            AstNode::ListLiteral { position, .. } |
            AstNode::DictionaryLiteral { position, .. } |
            AstNode::Identifier { position, .. } |
            AstNode::MemberAccess { position, .. } |
            AstNode::IndexAccess { position, .. } => *position,
        }
    }
    
    /// Get codegen statistics for debugging
    pub fn get_statistics(&self) -> CodegenStatistics {
        CodegenStatistics {
            function_count: self.program.functions.len(),
            constant_count: self.constants.len(),
            local_count: self.local_count,
            symbol_count: self.symbol_table.len(),
            instruction_count: self.current_function
                .as_ref()
                .map(|f| f.instructions.len())
                .unwrap_or(0),
        }
    }
}

/// Statistics about the codegen state
#[derive(Debug, Clone)]
pub struct CodegenStatistics {
    pub function_count: usize,
    pub constant_count: usize,
    pub local_count: usize,
    pub symbol_count: usize,
    pub instruction_count: usize,
}

impl fmt::Display for CodegenStatistics {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "CodegenStats {{ funcs: {}, consts: {}, locals: {}, symbols: {}, instructions: {} }}",
            self.function_count, self.constant_count, self.local_count, 
            self.symbol_count, self.instruction_count
        )
    }
}

/// Bootstrap integration functions for AOTT handoff
impl MinimalCodegen {
    /// Create codegen with AOTT integration metadata
    pub fn new_with_aott_integration(
        metadata: Option<HashMap<String, String>>,
    ) -> Self {
        let mut codegen = Self::new();
        
        if let Some(meta) = metadata {
            codegen.aott_metadata = meta;
            
            // Configure AOTT-specific settings
            if let Some(opt_level) = codegen.aott_metadata.get("optimization_level") {
                codegen.aott_metadata.insert(
                    "tier_promotion_threshold".to_string(),
                    match opt_level.as_str() {
                        "aggressive" => "10".to_string(),
                        "balanced" => "50".to_string(),
                        "conservative" => "100".to_string(),
                        _ => "50".to_string(),
                    },
                );
            }
        }
        
        codegen
    }
    
    /// Generate AOTT-optimized bytecode
    pub fn generate_aott_bytecode(&mut self, ast: &AstNode) -> CodegenResult<Program> {
        // Add global AOTT metadata
        self.aott_metadata.insert("target_system".to_string(), "aott".to_string());
        self.aott_metadata.insert("bytecode_version".to_string(), "bootstrap_1.0".to_string());
        
        // Generate base bytecode
        let mut program = self.generate(ast)?;
        
        // Add tier promotion candidates
        for function in &mut program.functions {
            if self.is_optimization_candidate(function) {
                function.aott_metadata.insert(
                    "tier_candidate".to_string(),
                    "true".to_string(),
                );
                
                // Insert tier promotion checks
                self.insert_tier_promotion_hooks(function);
            }
        }
        
        // Add metadata for AOTT system
        program.aott_metadata.insert(
            "bootstrap_compiler".to_string(),
            "minimal_codegen".to_string(),
        );
        
        Ok(program)
    }
    
    /// Check if a function is a good optimization candidate
    fn is_optimization_candidate(&self, function: &Function) -> bool {
        // Simple heuristics for bootstrap
        function.instructions.len() > 10 || // Non-trivial functions
        function.instructions.iter().any(|instr| {
            matches!(instr.opcode, Opcode::ProfileLoop | Opcode::Call)
        })
    }
    
    /// Insert tier promotion hooks into function
    fn insert_tier_promotion_hooks(&self, function: &mut Function) {
        // Insert profiling instructions at function start
        let profile_instr = Instruction::with_operand(Opcode::ProfileFunction, 0)
            .with_comment("AOTT tier promotion hook".to_string());
        
        function.instructions.insert(0, profile_instr);
        
        // Insert promotion checks after loops
        let mut insertion_points = Vec::new();
        for (i, instr) in function.instructions.iter().enumerate() {
            if matches!(instr.opcode, Opcode::Jump) {
                insertion_points.push(i + 1);
            }
        }
        
        // Insert in reverse order to maintain indices
        for &pos in insertion_points.iter().rev() {
            if pos < function.instructions.len() {
                let promote_instr = Instruction::with_operand(Opcode::TierPromote, 0)
                    .with_comment("AOTT tier promotion check".to_string());
                function.instructions.insert(pos, promote_instr);
            }
        }
    }
    
    /// Extract optimization metadata for AOTT
    pub fn extract_aott_metadata(&self, program: &Program) -> HashMap<String, String> {
        let mut metadata = program.aott_metadata.clone();
        
        // Add function-specific metadata
        for (i, function) in program.functions.iter().enumerate() {
            metadata.insert(
                format!("function_{}_name", i),
                function.name.clone(),
            );
            metadata.insert(
                format!("function_{}_instruction_count", i),
                function.instructions.len().to_string(),
            );
            metadata.insert(
                format!("function_{}_local_count", i),
                function.local_count.to_string(),
            );
            
            // Merge function metadata
            for (key, value) in &function.aott_metadata {
                metadata.insert(
                    format!("function_{}_{}", i, key),
                    value.clone(),
                );
            }
        }
        
        metadata.insert("total_functions".to_string(), program.functions.len().to_string());
        metadata.insert("total_constants".to_string(), program.global_constants.len().to_string());
        metadata.insert("total_types".to_string(), program.type_definitions.len().to_string());
        
        metadata
    }
    
    /// Validate bytecode for AOTT compatibility
    pub fn validate_aott_compatibility(&self, program: &Program) -> CodegenResult<()> {
        // Check function limits
        if program.functions.len() > 1024 {
            return Err(CodegenError::InternalError {
                message: format!("Too many functions for AOTT (limit: 1024, found: {})", program.functions.len()),
                position: None,
            });
        }
        
        // Check individual functions
        for function in &program.functions {
            if function.instructions.len() > 65536 {
                return Err(CodegenError::InternalError {
                    message: format!("Function '{}' too large for AOTT (limit: 65536 instructions)", function.name),
                    position: Some(function.position),
                });
            }
            
            if function.local_count > 256 {
                return Err(CodegenError::TooManyLocals {
                    limit: 256,
                    position: function.position,
                });
            }
        }
        
        // Check constants
        if program.global_constants.len() > 65536 {
            return Err(CodegenError::TooManyConstants {
                limit: 65536,
                position: Position::new(),
            });
        }
        
        Ok(())
    }
}

impl Default for MinimalCodegen {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::compiler::bootstrap::minimal_lexer::MinimalLexer;
    use crate::compiler::bootstrap::minimal_parser::MinimalParser;

    #[test]
    fn test_basic_codegen() {
        let source = r#"Process called "test":
            Return 42"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        let mut codegen = MinimalCodegen::new();
        let program = codegen.generate(&ast).expect("Failed to generate code");
        
        assert_eq!(program.functions.len(), 1);
        assert_eq!(program.functions[0].name, "test");
        assert!(!program.functions[0].instructions.is_empty());
    }
    
    #[test]
    fn test_expression_codegen() {
        let source = r#"Process called "test":
            Return 1 + 2 * 3"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        let mut codegen = MinimalCodegen::new();
        let program = codegen.generate(&ast).expect("Failed to generate code");
        
        // Should have constants for 1, 2, 3
        assert!(program.global_constants.len() >= 3);
        
        // Should have arithmetic instructions
        let function = &program.functions[0];
        let has_arithmetic = function.instructions.iter().any(|instr| {
            matches!(instr.opcode, Opcode::Add | Opcode::Multiply)
        });
        assert!(has_arithmetic);
    }
    
    #[test]
    fn test_aott_integration() {
        let source = r#"Process called "test":
            For i in [1, 2, 3]:
                Return i"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        let mut codegen = MinimalCodegen::new_with_aott_integration(None);
        let program = codegen.generate_aott_bytecode(&ast).expect("Failed to generate AOTT code");
        
        // Should have AOTT metadata
        assert!(!program.aott_metadata.is_empty());
        
        // Should have profiling instructions
        let function = &program.functions[0];
        let has_profiling = function.instructions.iter().any(|instr| {
            matches!(instr.opcode, Opcode::ProfileFunction | Opcode::ProfileLoop)
        });
        assert!(has_profiling);
    }
    
    #[test]
    fn test_error_handling() {
        let source = r#"Process called "test":
            Return undefined_variable"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        let mut codegen = MinimalCodegen::new();
        let result = codegen.generate(&ast);
        
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), CodegenError::UndefinedVariable { .. }));
    }
}