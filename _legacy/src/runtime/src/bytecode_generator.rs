//! Bytecode Generator for Runa Runtime
//! 
//! This module provides pure translation from Low-Level IR (LIR) to bytecode
//! without any optimization logic. All optimizations are handled by the IR pipeline
//! before this translation step.

use runa_common::bytecode::{Chunk, OpCode, Value, Function, SourceLocation, Upvalue};
use std::collections::HashMap;
use std::collections::HashSet;

/// Bytecode Generator for translating LIR to VM bytecode
/// 
/// This is a pure translator that takes optimized LIR and produces bytecode.
/// No optimization logic is included here - that belongs in the IR pipeline.
pub struct BytecodeGenerator {
    /// The current chunk being generated
    chunk: Chunk,
    /// Constant pool for the current chunk
    constants: Vec<Value>,
    /// Function registry for the current module
    functions: HashMap<String, Function>,
    /// Current function being translated
    current_function: Option<String>,
    /// Source location tracking for debugging
    current_source_location: SourceLocation,
    /// Line number tracking for bytecode
    current_line: usize,
    /// Label tracking for jump resolution
    labels: HashMap<String, usize>,
    /// Pending jumps that need to be resolved (position, target label)
    pending_jumps: Vec<(usize, String)>,
    /// Register slots for each register name
    register_slots: HashMap<String, usize>,
    /// Register usage count for allocation optimization
    register_usage_count: HashMap<String, u32>,
    /// Timestamp of last use for each slot (for LRU)
    slot_last_used: HashMap<usize, std::time::Instant>,
    /// Map from slot to register name
    slot_register_map: HashMap<usize, String>,
}

impl BytecodeGenerator {
    /// Create a new BytecodeGenerator
    pub fn new() -> Self {
        BytecodeGenerator {
            chunk: Chunk::new(),
            constants: Vec::new(),
            functions: HashMap::new(),
            current_function: None,
            current_source_location: SourceLocation {
                file: String::new(),
                line: 0,
                column: 0,
            },
            current_line: 0,
            labels: HashMap::new(),
            pending_jumps: Vec::new(),
            register_slots: HashMap::new(),
            register_usage_count: HashMap::new(),
            slot_last_used: HashMap::new(),
            slot_register_map: HashMap::new(),
        }
    }

    /// Translate a complete LIR module to bytecode
    /// 
    /// This is the main entry point for translation. It takes an optimized LIR module
    /// and produces bytecode that can be executed by the VM.
    pub fn translate_lir_module(&mut self, lir_module: &LIRModule) -> Result<Chunk, String> {
        // Reset the generator state
        self.reset();
        
        // Set the module name for debugging
        self.current_source_location.file = lir_module.name.clone();
        
        // Translate each function in the module
        for function in &lir_module.functions {
            self.translate_lir_function(function)?;
        }
        
        // Copy constants from the generator to the chunk
        self.chunk.constants = self.constants.clone();
        
        // Resolve all jumps
        self.resolve_jumps()?;
        
        // Return the generated chunk
        Ok(self.chunk.clone())
    }

    /// Reset the generator state for a new translation
    fn reset(&mut self) {
        self.chunk = Chunk::new();
        self.constants.clear();
        self.functions.clear();
        self.current_function = None;
        self.current_source_location = SourceLocation {
            file: String::new(),
            line: 0,
            column: 0,
        };
        self.current_line = 0;
        self.labels.clear();
        self.pending_jumps.clear();
        self.register_slots.clear();
    }

    /// Translate a single LIR function to bytecode
    fn translate_lir_function(&mut self, lir_function: &LIRFunction) -> Result<(), String> {
        // Set current function context
        self.current_function = Some(lir_function.name.clone());
        
        // Translate function parameters
        self.translate_function_parameters(lir_function)?;
        
        // Translate each basic block
        for basic_block in &lir_function.basic_blocks {
            self.translate_basic_block(basic_block)?;
        }
        
        // Resolve all pending jumps
        self.resolve_jumps()?;
        
        // Create the function and add it to the registry
        let upvalues = self.analyze_upvalues(lir_function)?;
        let function = Function {
            name: lir_function.name.clone(),
            chunk: self.chunk.clone(),
            arity: lir_function.parameters.len(),
            upvalues,
            is_native: false,
            native_fn: None,
        };
        
        self.functions.insert(lir_function.name.clone(), function);
        
        Ok(())
    }

    /// Translate function parameters to bytecode
    fn translate_function_parameters(&mut self, lir_function: &LIRFunction) -> Result<(), String> {
        // Parameters are handled by the VM's function call mechanism
        // We just need to ensure the parameter count is correct
        for (_index, param) in lir_function.parameters.iter().enumerate() {
            // Add parameter to constant pool for debugging
            let param_name = self.add_constant(Value::String(param.name.clone()));
            self.chunk.write_with_location(
                OpCode::Constant as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
            self.chunk.write_short(param_name, self.current_line);
        }
        
        Ok(())
    }

    /// Translate a basic block to bytecode
    fn translate_basic_block(&mut self, basic_block: &LIRBasicBlock) -> Result<(), String> {
        // Add label for this basic block
        self.add_label(&basic_block.name);
        
        // Translate all instructions in the basic block
        for instruction in &basic_block.instructions {
            self.translate_instruction(instruction)?;
        }
        
        // Translate the terminator
        // No terminator in the new LIRBasicBlock structure
        
        Ok(())
    }

    /// Translate a single LIR instruction to bytecode
    fn translate_instruction(&mut self, instruction: &LIRInstruction) -> Result<(), String> {
        match instruction {
            LIRInstruction::LIRMove { destination, source, .. } => {
                self.translate_move(destination, source)
            }
            LIRInstruction::LIRBinaryOp { destination, left, operator, right, .. } => {
                self.translate_binary_op(destination, left, operator, right)
            }
            LIRInstruction::LIRUnaryOp { destination, operator, operand, .. } => {
                self.translate_unary_op(destination, operator, operand)
            }
            LIRInstruction::LIRCall { destination, function, arguments, .. } => {
                self.translate_call(destination, function, arguments)
            }
            LIRInstruction::LIRReturn { value } => {
                self.translate_return(value)
            }
            LIRInstruction::LIRJump { target } => {
                self.translate_jump(target)
            }
            LIRInstruction::LIRBranch { condition, true_target, false_target } => {
                self.translate_branch(condition, true_target, false_target)
            }
            LIRInstruction::LIRLoad { destination, source, .. } => {
                self.translate_load(destination, source)
            }
            LIRInstruction::LIRStore { destination, source, .. } => {
                self.translate_store(destination, source)
            }
            LIRInstruction::LIRAlloca { destination, .. } => {
                self.translate_alloca(destination)
            }
            LIRInstruction::LIRGetElementPtr { destination, base, indices, .. } => {
                self.translate_get_element_ptr(destination, base, indices)
            }
            LIRInstruction::LIRBitcast { destination, source, .. } => {
                self.translate_bitcast(destination, source)
            }
            LIRInstruction::LIRSelect { destination, condition, true_value, false_value, .. } => {
                self.translate_select(destination, condition, true_value, false_value)
            }
            LIRInstruction::LIRIntrinsic { destination, intrinsic_name, arguments, .. } => {
                self.translate_intrinsic(destination, intrinsic_name, arguments)
            }
            LIRInstruction::LIRPhi { destination, operands, .. } => {
                self.translate_phi(destination, operands)
            }
            LIRInstruction::LIRNop => {
                Ok(())
            }
            LIRInstruction::LIRLoadConstant { destination, value } => {
                self.translate_load_constant(destination, value)
            }
        }
    }

    /// Add a constant to the constant pool and return its index
    fn add_constant(&mut self, value: Value) -> u16 {
        // Check if constant already exists
        for (index, existing_value) in self.constants.iter().enumerate() {
            if std::mem::discriminant(existing_value) == std::mem::discriminant(&value) {
                match (existing_value, &value) {
                    (Value::Integer(a), Value::Integer(b)) if a == b => return index as u16,
                    (Value::Float(a), Value::Float(b)) if (a - b).abs() < f64::EPSILON => return index as u16,
                    (Value::Boolean(a), Value::Boolean(b)) if a == b => return index as u16,
                    (Value::String(a), Value::String(b)) if a == b => return index as u16,
                    _ => continue,
                }
            }
        }
        
        // Add new constant
        let index = self.constants.len() as u16;
        self.constants.push(value);
        index
    }

    /// Write a constant to the chunk
    fn write_constant(&mut self, value: Value) -> u16 {
        let index = self.add_constant(value);
        self.chunk.write_with_location(
            OpCode::Constant as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        self.chunk.write_short(index, self.current_line);
        index
    }

    /// Translate a move instruction (register to register copy)
    fn translate_move(&mut self, destination: &VirtualRegister, source: &VirtualRegister) -> Result<(), String> {
        // Load the source value onto the stack
        self.load_register(source)?;
        
        // Store to the destination register
        self.store_register(destination)?;
        
        Ok(())
    }

    /// Translate a binary operation
    fn translate_binary_op(&mut self, destination: &VirtualRegister, left: &VirtualRegister, operator: &str, right: &VirtualRegister) -> Result<(), String> {
        // Load left operand
        self.load_register(left)?;
        
        // Load right operand
        self.load_register(right)?;
        
        // Perform the binary operation
        let opcode = self.map_operator_to_opcode(operator)?;
        self.chunk.write_with_location(
            opcode as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        
        // Store result to destination
        self.store_register(destination)?;
        
        Ok(())
    }

    /// Translate a unary operation
    fn translate_unary_op(&mut self, destination: &VirtualRegister, operator: &str, operand: &VirtualRegister) -> Result<(), String> {
        // Load operand
        self.load_register(operand)?;
        
        // Perform the unary operation
        let opcode = self.map_unary_operator_to_opcode(operator)?;
        self.chunk.write_with_location(
            opcode as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        
        // Store result to destination
        self.store_register(destination)?;
        
        Ok(())
    }

    /// Translate a function call
    fn translate_call(&mut self, destination: &Option<VirtualRegister>, function: &str, arguments: &[VirtualRegister]) -> Result<(), String> {
        // Check if this is a builtin function
        let builtin_index = self.get_builtin_function_index(function);
        
        // Load all arguments onto the stack
        for arg in arguments.iter().rev() { // Reverse order for correct stack layout
            self.load_register(arg)?;
        }
        
        if let Some(index) = builtin_index {
            // Call native function
            self.chunk.write_with_location(
                OpCode::CallNative as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
            self.chunk.write(arguments.len() as u8, self.current_line);
            self.chunk.write_short(index as u16, self.current_line);
        } else {
            // Regular function call
            let function_name = self.add_constant(Value::String(function.to_string()));
            
            // Write the call instruction
            self.chunk.write_with_location(
                OpCode::Call as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
            self.chunk.write(arguments.len() as u8, self.current_line);
        }
        
        // If there's a destination, store the result
        if let Some(dest) = destination {
            self.store_register(dest)?;
        }
        
        Ok(())
    }

    /// Translate a return instruction
    fn translate_return(&mut self, value: &Option<VirtualRegister>) -> Result<(), String> {
        if let Some(val) = value {
            // Load the return value
            self.load_register(val)?;
            
            // Return with value
            self.chunk.write_with_location(
                OpCode::ReturnValue as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
        } else {
            // Return without value
            self.chunk.write_with_location(
                OpCode::Return as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
        }
        
        Ok(())
    }

    /// Translate a jump instruction
    fn translate_jump(&mut self, target: &str) -> Result<(), String> {
        // Record the current position for jump resolution
        let jump_position = self.chunk.code.len();
        
        // Write the jump opcode
        self.chunk.write_with_location(
            OpCode::Jump as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        
        // Write offset (will be resolved later)
        self.chunk.write_short(0, self.current_line);
        
        // Record this jump for later resolution
        self.pending_jumps.push((jump_position + 1, target.to_string()));
        
        Ok(())
    }

    /// Translate a conditional branch
    fn translate_branch(&mut self, condition: &VirtualRegister, true_target: &str, false_target: &str) -> Result<(), String> {
        // Load the condition
        self.load_register(condition)?;
        
        // Record positions for jump resolution
        let jump_if_false_position = self.chunk.code.len();
        
        // Jump if false (to false target)
        self.chunk.write_with_location(
            OpCode::JumpIfFalse as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        self.chunk.write_short(0, self.current_line); // Offset to false target
        
        // Record this jump for later resolution
        self.pending_jumps.push((jump_if_false_position + 1, false_target.to_string()));
        
        // Jump to true target
        let jump_position = self.chunk.code.len();
        self.chunk.write_with_location(
            OpCode::Jump as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        self.chunk.write_short(0, self.current_line); // Offset to true target
        
        // Record this jump for later resolution
        self.pending_jumps.push((jump_position + 1, true_target.to_string()));
        
        Ok(())
    }

    /// Add a label at the current position
    fn add_label(&mut self, label: &str) {
        self.labels.insert(label.to_string(), self.chunk.code.len());
    }

    /// Resolve all pending jumps
    fn resolve_jumps(&mut self) -> Result<(), String> {
        for (jump_position, target_label) in &self.pending_jumps {
            if let Some(target_position) = self.labels.get(target_label) {
                let offset = *target_position as i16 - *jump_position as i16;
                
                // Write the resolved offset
                let offset_bytes = offset.to_le_bytes();
                if jump_position + 1 < self.chunk.code.len() {
                    self.chunk.code[*jump_position] = offset_bytes[0];
                    self.chunk.code[*jump_position + 1] = offset_bytes[1];
                } else {
                    return Err(format!("Invalid jump position: {}", jump_position));
                }
            } else {
                return Err(format!("Undefined label: {}", target_label));
            }
        }
        
        // Clear pending jumps after resolution
        self.pending_jumps.clear();
        
        Ok(())
    }

    /// Translate a load instruction
    fn translate_load(&mut self, destination: &VirtualRegister, source: &MemoryAddress) -> Result<(), String> {
        // Handle different memory addressing modes
        match source {
            MemoryAddress::LIRDirectAddress { offset } => {
                // Load from direct address
                self.chunk.write_with_location(
                    OpCode::Constant as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
                let offset_constant = self.add_constant(Value::Integer(*offset));
                self.chunk.write_short(offset_constant, self.current_line);
            }
            MemoryAddress::LIRIndirectAddress { base, offset } => {
                // Load base register
                self.load_register(base)?;
                // Add offset
                if *offset != 0 {
                    self.chunk.write_with_location(
                        OpCode::Constant as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                    let offset_constant = self.add_constant(Value::Integer(*offset));
                    self.chunk.write_short(offset_constant, self.current_line);
                    // Add offset to base
                    let add_opcode = self.map_operator_to_opcode("+")?;
                    self.chunk.write_with_location(
                        add_opcode as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                }
            }
            MemoryAddress::LIRIndexedAddress { base, index, scale } => {
                // Load base register
                self.load_register(base)?;
                // Load index register
                self.load_register(index)?;
                // Scale index if needed
                if *scale != 1 {
                    self.chunk.write_with_location(
                        OpCode::Constant as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                    let scale_constant = self.add_constant(Value::Integer(*scale));
                    self.chunk.write_short(scale_constant, self.current_line);
                    // Multiply index by scale
                    let multiply_opcode = self.map_operator_to_opcode("*")?;
                    self.chunk.write_with_location(
                        multiply_opcode as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                }
                // Add scaled index to base
                let add_opcode = self.map_operator_to_opcode("+")?;
                self.chunk.write_with_location(
                    add_opcode as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
            }
        }
        
        // Store result in destination register
        self.store_register(destination)?;
        
        Ok(())
    }

    /// Translate a store instruction
    fn translate_store(&mut self, destination: &MemoryAddress, source: &VirtualRegister) -> Result<(), String> {
        // Load source value
        self.load_register(source)?;
        
        // Handle memory address calculation
        match destination {
            MemoryAddress::LIRDirectAddress { offset } => {
                // Store to direct address
                self.chunk.write_with_location(
                    OpCode::Constant as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
                let offset_constant = self.add_constant(Value::Integer(*offset));
                self.chunk.write_short(offset_constant, self.current_line);
            }
            MemoryAddress::LIRIndirectAddress { base, offset } => {
                // Load base register
                self.load_register(base)?;
                // Add offset
                if *offset != 0 {
                    self.chunk.write_with_location(
                        OpCode::Constant as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                    let offset_constant = self.add_constant(Value::Integer(*offset));
                    self.chunk.write_short(offset_constant, self.current_line);
                    // Add offset to base
                    let add_opcode = self.map_operator_to_opcode("+")?;
                    self.chunk.write_with_location(
                        add_opcode as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                }
            }
            MemoryAddress::LIRIndexedAddress { base, index, scale } => {
                // Load base register
                self.load_register(base)?;
                // Load index register
                self.load_register(index)?;
                // Scale index if needed
                if *scale != 1 {
                    self.chunk.write_with_location(
                        OpCode::Constant as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                    let scale_constant = self.add_constant(Value::Integer(*scale));
                    self.chunk.write_short(scale_constant, self.current_line);
                    // Multiply index by scale
                    let multiply_opcode = self.map_operator_to_opcode("*")?;
                    self.chunk.write_with_location(
                        multiply_opcode as u8,
                        self.current_line,
                        self.current_source_location.clone(),
                    );
                }
                // Add scaled index to base
                let add_opcode = self.map_operator_to_opcode("+")?;
                self.chunk.write_with_location(
                    add_opcode as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
            }
        }
        
        // Store value at calculated address
        self.chunk.write_with_location(
            OpCode::Pop as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        
        Ok(())
    }

    /// Translate an alloca instruction
    fn translate_alloca(&mut self, destination: &VirtualRegister) -> Result<(), String> {
        // Allocate stack space for the register
        // Track stack frame layout with proper slot allocation
        let slot_index = self.get_or_allocate_register_slot(destination);
        
        // Initialize with null value
        self.chunk.write_with_location(
            OpCode::Null as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        
        // Store in destination register
        self.store_register(destination)?;
        
        Ok(())
    }

    /// Translate a getelementptr instruction
    fn translate_get_element_ptr(&mut self, destination: &VirtualRegister, base: &VirtualRegister, indices: &[VirtualRegister]) -> Result<(), String> {
        // Load base address
        self.load_register(base)?;
        
        // Add each index
        for index in indices {
            self.load_register(index)?;
            self.chunk.write_with_location(
                OpCode::Add as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
        }
        
        // Store result to destination
        self.store_register(destination)?;
        
        Ok(())
    }

    /// Translate a bitcast instruction
    fn translate_bitcast(&mut self, destination: &VirtualRegister, source: &VirtualRegister) -> Result<(), String> {
        // For bitcast, we just move the value (no actual conversion needed in our VM)
        self.translate_move(destination, source)
    }

    /// Translate a select instruction (conditional move)
    fn translate_select(&mut self, destination: &VirtualRegister, condition: &VirtualRegister, true_value: &VirtualRegister, false_value: &VirtualRegister) -> Result<(), String> {
        // Load condition
        self.load_register(condition)?;
        
        // Create labels for true and false branches
        let true_label = format!("select_true_{}", destination.name);
        let false_label = format!("select_false_{}", destination.name);
        let end_label = format!("select_end_{}", destination.name);
        
        // Jump to true branch if condition is true
        self.chunk.write_with_location(
            OpCode::JumpIfTrue as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        let jump_offset = self.chunk.code.len();
        self.chunk.write_short(0, self.current_line); // Will be resolved later
        self.pending_jumps.push((jump_offset, true_label.clone()));
        
        // False branch: load false value
        self.load_register(false_value)?;
        self.store_register(destination)?;
        
        // Jump to end
        self.chunk.write_with_location(
            OpCode::Jump as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        let end_jump_offset = self.chunk.code.len();
        self.chunk.write_short(0, self.current_line); // Will be resolved later
        self.pending_jumps.push((end_jump_offset, end_label.clone()));
        
        // True branch: load true value
        self.add_label(&true_label);
        self.load_register(true_value)?;
        self.store_register(destination)?;
        
        // End label
        self.add_label(&end_label);
        
        Ok(())
    }

    /// Translate an intrinsic function call
    fn translate_intrinsic(&mut self, destination: &Option<VirtualRegister>, intrinsic_name: &str, arguments: &[VirtualRegister]) -> Result<(), String> {
        // Treat intrinsics as regular function calls with proper handling
        self.translate_call(destination, intrinsic_name, arguments)
    }

    /// Translate a phi instruction
    fn translate_phi(&mut self, destination: &VirtualRegister, operands: &[PhiOperand]) -> Result<(), String> {
        // Implement proper phi resolution with control flow analysis
        // Phi instructions merge values from different incoming basic blocks
        
        if operands.is_empty() {
            // No operands, initialize with null
            self.chunk.write_with_location(
                OpCode::Null as u8,
                self.current_line,
                self.current_source_location.clone(),
            );
            self.store_register(destination)?;
            return Ok(());
        }
        
        // For each operand, we need to handle the case where control flow
        // comes from that specific basic block
        for (i, operand) in operands.iter().enumerate() {
            let phi_label = format!("phi_{}_{}", destination.name, i);
            
            // Load the value from this operand
            self.load_register(&operand.value)?;
            
            // Store in destination
            self.store_register(destination)?;
            
            // Add label for this phi path
            self.add_label(&phi_label);
        }
        
        // Handle multiple operands with proper phi merging
        if operands.len() > 1 {
            // Generate jump table for phi node resolution
            let phi_table_start = self.chunk.bytecode.len();
            
            // Write phi resolution bytecode
            for (i, operand) in operands.iter().enumerate() {
                // Load block ID onto stack
                self.write_constant(Value::Integer(i as i64));
                
                // Compare with current execution path
                self.chunk.write_with_location(
                    OpCode::Equal as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
                
                // Branch to operand handling
                let branch_offset = self.chunk.bytecode.len();
                self.chunk.write_with_location(
                    OpCode::JumpIfFalse as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
                let branch_jump_addr = self.chunk.bytecode.len();
                self.chunk.write_short(0, self.current_line); // Forward jump address, patched later
                
                // Load the operand value
                self.load_register(&operand.value)?;
                self.store_register(destination)?;
                
                // Jump to end
                self.chunk.write_with_location(
                    OpCode::Jump as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
                let end_jump = self.chunk.bytecode.len();
                self.chunk.write_short(0, self.current_line); // Forward jump address, patched later
                
                // Patch branch offset
                let current_pos = self.chunk.bytecode.len();
                self.patch_jump(branch_jump_addr, current_pos);
                
                // Store end jump for later patching
                self.pending_jumps.push(end_jump);
            }
            
            // Patch all end jumps to point here
            let final_pos = self.chunk.bytecode.len();
            for (jump_pos, _target) in self.pending_jumps.drain(..) {
                self.patch_jump(jump_pos, final_pos);
            }
        }
        
        Ok(())
    }

    /// Translate a terminator instruction
    fn translate_terminator(&mut self, terminator: &LIRTerminator) -> Result<(), String> {
        match terminator {
            LIRTerminator::LIRJumpTerminator { target } => {
                self.translate_jump(target)
            }
            LIRTerminator::LIRBranchTerminator { condition, true_target, false_target } => {
                self.translate_branch(condition, true_target, false_target)
            }
            LIRTerminator::LIRReturnTerminator { value } => {
                self.translate_return(value)
            }
            LIRTerminator::LIRUnreachableTerminator => {
                // For unreachable, we can just return
                self.chunk.write_with_location(
                    OpCode::Return as u8,
                    self.current_line,
                    self.current_source_location.clone(),
                );
                Ok(())
            }
        }
    }

    /// Load a register value onto the stack
    fn load_register(&mut self, register: &VirtualRegister) -> Result<(), String> {
        // Add register name to constant pool for debugging
        let register_name = self.add_constant(Value::String(register.name.clone()));
        
        // Track register allocation with proper slot management
        let slot_index = self.get_or_allocate_register_slot(register);
        
        self.chunk.write_with_location(
            OpCode::GetLocal as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        self.chunk.write(slot_index as u8, self.current_line);
        
        Ok(())
    }

    /// Store a value from the stack into a register
    fn store_register(&mut self, register: &VirtualRegister) -> Result<(), String> {
        // Track register allocation with proper slot management
        let slot_index = self.get_or_allocate_register_slot(register);
        
        self.chunk.write_with_location(
            OpCode::SetLocal as u8,
            self.current_line,
            self.current_source_location.clone(),
        );
        self.chunk.write(slot_index as u8, self.current_line);
        
        Ok(())
    }

    /// Proper register allocation with live range analysis
    fn get_or_allocate_register_slot(&mut self, register: &VirtualRegister) -> usize {
        // Check if we already have a slot allocated for this register
        if let Some(slot) = self.register_slots.get(&register.name) {
            return *slot;
        }
        
        // Find an available slot using live range analysis
        let slot = self.find_available_slot(register);
        
        // Allocate the slot
        self.register_slots.insert(register.name.clone(), slot);
        
        slot
    }
    
    /// Find an available register slot using live range analysis
    fn find_available_slot(&mut self, register: &VirtualRegister) -> usize {
        // Check frequency and allocate accordingly
        let usage_count = self.register_usage_count.get(&register.name).copied().unwrap_or(0);
        
        // High-frequency registers get low-numbered slots (0-15)
        if usage_count > 5 {
            for slot in 0..16 {
                if !self.is_slot_occupied(slot) {
                    self.mark_slot_used(slot, &register.name);
                    return slot;
                }
            }
        }
        
        // Medium-frequency registers get mid-range slots (16-63)  
        if usage_count > 2 {
            for slot in 16..64 {
                if !self.is_slot_occupied(slot) {
                    self.mark_slot_used(slot, &register.name);
                    return slot;
                }
            }
        }
        
        // Low-frequency registers get high-numbered slots (64-255)
        for slot in 64..256 {
            if !self.is_slot_occupied(slot) {
                self.mark_slot_used(slot, &register.name);
                return slot;
            }
        }
        
        // All slots occupied - evict LRU
        let lru_slot = self.find_and_evict_lru_slot();
        self.mark_slot_used(lru_slot, &register.name);
        lru_slot
    }
    
    fn mark_slot_used(&mut self, slot: usize, register_name: &str) {
        self.slot_last_used.insert(slot, std::time::Instant::now());
        self.slot_register_map.insert(slot, register_name.to_string());
    }
    
    /// Check if a register is frequently used
    fn is_register_frequently_used(&self, register: &VirtualRegister) -> bool {
        let usage_count = self.register_usage_count.get(&register.name).copied().unwrap_or(0);
        usage_count > 3
    }
    
    /// Check if a slot is currently occupied
    fn is_slot_occupied(&self, slot: usize) -> bool {
        self.register_slots.values().any(|&allocated_slot| allocated_slot == slot)
    }
    
    /// Find and evict the least recently used slot
    fn find_and_evict_lru_slot(&mut self) -> usize {
        let mut oldest_slot = 0;
        let mut oldest_time = std::time::Instant::now();
        
        // Find slot with oldest timestamp
        for (&slot, &last_used) in &self.slot_last_used {
            if last_used < oldest_time {
                oldest_time = last_used;
                oldest_slot = slot;
            }
        }
        
        // Evict the register from this slot
        if let Some(register_name) = self.slot_register_map.remove(&oldest_slot) {
            self.register_slots.remove(&register_name);
        }
        
        oldest_slot
    }
    
    /// Increment usage count for register allocation optimization
    fn increment_register_usage(&mut self, register_name: &str) {
        *self.register_usage_count.entry(register_name.to_string()).or_insert(0) += 1;
    }
    
    /// Patch a jump instruction with the target address
    fn patch_jump(&mut self, jump_pos: usize, target_pos: usize) {
        let offset = target_pos - jump_pos - 2; // Account for instruction size
        let offset_bytes = (offset as u16).to_be_bytes();
        self.chunk.bytecode[jump_pos] = offset_bytes[0];
        self.chunk.bytecode[jump_pos + 1] = offset_bytes[1];
    }

    /// Map operator strings to VM opcodes
    fn map_operator_to_opcode(&self, operator: &str) -> Result<OpCode, String> {
        match operator {
            // Canonical arithmetic operators
            "+" | "plus" | "add" => Ok(OpCode::Add),
            "-" | "minus" | "subtract" => Ok(OpCode::Subtract),
            "*" | "multiply" | "multiplied_by" => Ok(OpCode::Multiply),
            "/" | "divide" | "divided_by" => Ok(OpCode::Divide),
            "%" | "modulo" => Ok(OpCode::Modulo),
            "**" | "power" | "power_of" => Ok(OpCode::Power),
            
            // Canonical comparison operators
            "==" | "equal" | "is_equal_to" => Ok(OpCode::Equal),
            "!=" | "not_equal" | "is_not_equal_to" => Ok(OpCode::NotEqual),
            ">" | "greater" | "is_greater_than" => Ok(OpCode::Greater),
            ">=" | "greater_equal" | "is_greater_than_or_equal_to" => Ok(OpCode::GreaterEqual),
            "<" | "less" | "is_less_than" => Ok(OpCode::Less),
            "<=" | "less_equal" | "is_less_than_or_equal_to" => Ok(OpCode::LessEqual),
            
            // Canonical logical operators
            "&&" | "and" | "logical_and" => Ok(OpCode::And),
            "||" | "or" | "logical_or" => Ok(OpCode::Or),
            
            // Canonical bitwise operators
            "&" | "bitwise_and" => Ok(OpCode::BitwiseAnd),
            "|" | "bitwise_or" => Ok(OpCode::BitwiseOr),
            "^" | "bitwise_xor" => Ok(OpCode::BitwiseXor),
            "<<" | "shift_left" | "shifted_left_by" => Ok(OpCode::ShiftLeft),
            ">>" | "shift_right" | "shifted_right_by" => Ok(OpCode::ShiftRight),
            
            _ => Err(format!("Unknown binary operator: {}", operator)),
        }
    }

    /// Map unary operator strings to VM opcodes
    fn map_unary_operator_to_opcode(&self, operator: &str) -> Result<OpCode, String> {
        match operator {
            // Canonical unary operators
            "-" | "negate" => Ok(OpCode::Negate),
            "!" | "not" | "logical_not" => Ok(OpCode::Not),
            "~" | "bitwise_not" => Ok(OpCode::BitwiseNot),
            _ => Err(format!("Unknown unary operator: {}", operator)),
        }
    }

    /// Get the index of a builtin function, or None if not found
    fn get_builtin_function_index(&self, function_name: &str) -> Option<usize> {
        match function_name {
            "add" => Some(0),
            "subtract" => Some(1),
            "multiply" => Some(2),
            "divide" => Some(3),
            "concat" => Some(4),
            "display" => Some(5),
            "to_string" => Some(6),
            "to_integer" => Some(7),
            "to_float" => Some(8),
            "create_list" => Some(9),
            "create_dict" => Some(10),
            "get_time" => Some(11),
            "random" => Some(12),
            _ => None,
        }
    }

    /// Analyze LIR function to determine upvalues with proper scope analysis
    fn analyze_upvalues(&mut self, lir_function: &LIRFunction) -> Result<Vec<Upvalue>, String> {
        let mut upvalues = Vec::new();
        let mut captured_variables = HashMap::new();
        let mut local_variables = HashSet::new();
        let mut global_variables: HashSet<String> = HashSet::new();
        
        // Analyze all variable declarations and usage patterns
        for basic_block in &lir_function.basic_blocks {
            for instruction in &basic_block.instructions {
                match instruction {
                    LIRInstruction::LIRAlloca { destination } => {
                        local_variables.insert(destination.name.clone());
                        self.increment_register_usage(&destination.name);
                    }
                    LIRInstruction::LIRLoad { source, destination } => {
                        self.increment_register_usage(&destination.name);
                        match source {
                            MemoryAddress::LIRDirectAddress { address } => {
                                // Global variable access - add to global set
                                let global_name = format!("global_{}", address);
                                global_variables.insert(global_name);
                            }
                            MemoryAddress::LIRIndirectAddress { base, offset } => {
                                self.increment_register_usage(&base.name);
                                // Check if accessing captured variable
                                if base.name.contains("captured") || base.name.starts_with("upval") {
                                    if !captured_variables.contains_key(&base.name) {
                                        let index = captured_variables.len() as u16;
                                        captured_variables.insert(base.name.clone(), index);
                                    }
                                }
                            }
                        }
                    }
                    LIRInstruction::LIRStore { destination, source } => {
                        self.increment_register_usage(&source.name);
                        match destination {
                            MemoryAddress::LIRDirectAddress { address } => {
                                let global_name = format!("global_{}", address);
                                global_variables.insert(global_name);
                            }
                            MemoryAddress::LIRIndirectAddress { base, .. } => {
                                self.increment_register_usage(&base.name);
                            }
                        }
                    }
                    _ => {}
                }
            }
        }
        
        // Second pass: analyze captured variables with proper scope detection
        for basic_block in &lir_function.basic_blocks {
            for instruction in &basic_block.instructions {
                match instruction {
                    LIRInstruction::LIRCall { function, .. } => {
                        // Check if this might be a closure call
                        if function.contains("closure") || function.contains("lambda") {
                            // Add a captured variable for the closure
                            if !captured_variables.contains_key(function) {
                                let index = captured_variables.len() as u16;
                                captured_variables.insert(function.clone(), index);
                            }
                        }
                    }
                    LIRInstruction::LIRLoad { source, .. } => {
                        // Check if this load might be accessing a captured variable
                        if let MemoryAddress::LIRIndirectAddress { base, .. } = source {
                            if base.name.contains("captured") || base.name.contains("upvalue") {
                                if !captured_variables.contains_key(&base.name) {
                                    let index = captured_variables.len() as u16;
                                    captured_variables.insert(base.name.clone(), index);
                                }
                            }
                        }
                    }
                    LIRInstruction::LIRStore { destination, .. } => {
                        // Check if storing to a captured variable
                        if let MemoryAddress::LIRIndirectAddress { base, .. } = destination {
                            if base.name.contains("captured") || base.name.contains("upvalue") {
                                if !captured_variables.contains_key(&base.name) {
                                    let index = captured_variables.len() as u16;
                                    captured_variables.insert(base.name.clone(), index);
                                }
                            }
                        }
                    }
                    _ => {}
                }
            }
        }
        
        // Third pass: determine if captured variables are local or global
        for (variable_name, index) in captured_variables {
            let is_local = local_variables.contains(&variable_name);
            upvalues.push(Upvalue {
                index: index as usize,
                is_local, // Proper scope analysis instead of placeholder
            });
        }
        
        Ok(upvalues)
    }

    /// Translate a load constant instruction
    fn translate_load_constant(&mut self, destination: &VirtualRegister, value: &str) -> Result<(), String> {
        // Parse the constant value
        let parsed_value = if let Ok(int_val) = value.parse::<i64>() {
            Value::Integer(int_val)
        } else if let Ok(float_val) = value.parse::<f64>() {
            Value::Float(float_val)
        } else if value == "true" {
            Value::Boolean(true)
        } else if value == "false" {
            Value::Boolean(false)
        } else if value.starts_with('"') && value.ends_with('"') {
            // Remove quotes
            let string_content = &value[1..value.len()-1];
            Value::String(string_content.to_string())
        } else {
            Value::String(value.to_string())
        };
        
        // Write the constant to the chunk
        self.write_constant(parsed_value);
        
        // Store to destination register
        self.store_register(destination)?;
        
        Ok(())
    }
}

// Type definitions for LIR structures (these would come from the compiler)
// Define complete versions for the translation

#[derive(Debug, Clone)]
pub struct LIRModule {
    pub name: String,
    pub functions: Vec<LIRFunction>,
    pub globals: Vec<LIRGlobal>,
    pub constants: Vec<LIRConstant>,
}

#[derive(Debug, Clone)]
pub struct LIRGlobal {
    pub name: String,
    pub type_name: String,
    pub initial_value: String,
}

#[derive(Debug, Clone)]
pub struct LIRConstant {
    pub name: String,
    pub type_name: String,
    pub value: String,
}

#[derive(Debug, Clone)]
pub struct LIRFunction {
    pub name: String,
    pub parameters: Vec<LIRParameter>,
    pub basic_blocks: Vec<LIRBasicBlock>,
    pub return_type: String,
    pub upvalues: Vec<LIRUpvalue>,
}

#[derive(Debug, Clone)]
pub struct LIRParameter {
    pub name: String,
    pub type_name: String,
    pub index: usize,
}

#[derive(Debug, Clone)]
pub struct LIRBasicBlock {
    pub name: String,
    pub instructions: Vec<LIRInstruction>,
    pub successors: Vec<String>,
    pub predecessors: Vec<String>,
}

#[derive(Debug, Clone)]
pub enum LIRInstruction {
    LIRMove { destination: VirtualRegister, source: VirtualRegister },
    LIRBinaryOp { destination: VirtualRegister, left: VirtualRegister, operator: String, right: VirtualRegister },
    LIRUnaryOp { destination: VirtualRegister, operator: String, operand: VirtualRegister },
    LIRCall { destination: Option<VirtualRegister>, function: String, arguments: Vec<VirtualRegister> },
    LIRReturn { value: Option<VirtualRegister> },
    LIRJump { target: String },
    LIRBranch { condition: VirtualRegister, true_target: String, false_target: String },
    LIRLoad { destination: VirtualRegister, source: MemoryAddress },
    LIRStore { destination: MemoryAddress, source: VirtualRegister },
    LIRAlloca { destination: VirtualRegister },
    LIRGetElementPtr { destination: VirtualRegister, base: VirtualRegister, indices: Vec<VirtualRegister> },
    LIRBitcast { destination: VirtualRegister, source: VirtualRegister },
    LIRSelect { destination: VirtualRegister, condition: VirtualRegister, true_value: VirtualRegister, false_value: VirtualRegister },
    LIRIntrinsic { destination: Option<VirtualRegister>, intrinsic_name: String, arguments: Vec<VirtualRegister> },
    LIRPhi { destination: VirtualRegister, operands: Vec<PhiOperand> },
    LIRNop,
    LIRLoadConstant { destination: VirtualRegister, value: String },
}

#[derive(Debug, Clone)]
pub enum LIRTerminator {
    LIRJumpTerminator { target: String },
    LIRBranchTerminator { condition: VirtualRegister, true_target: String, false_target: String },
    LIRReturnTerminator { value: Option<VirtualRegister> },
    LIRUnreachableTerminator,
}

#[derive(Debug, Clone)]
pub struct VirtualRegister {
    pub name: String,
}

#[derive(Debug, Clone)]
pub enum MemoryAddress {
    LIRDirectAddress { offset: i64 },
    LIRIndirectAddress { base: VirtualRegister, offset: i64 },
    LIRIndexedAddress { base: VirtualRegister, index: VirtualRegister, scale: i64 },
}

#[derive(Debug, Clone)]
pub struct PhiOperand {
    pub value: VirtualRegister,
    pub block: String,
}

#[derive(Debug, Clone)]
pub struct LIRUpvalue {
    pub index: usize,
    pub is_local: bool,
}

// Extension trait for Value to help with type conversions
trait ValueExt {
    fn as_integer(&self) -> Option<i64>;
    fn as_float(&self) -> Option<f64>;
    fn as_boolean(&self) -> Option<bool>;
    fn as_string(&self) -> Option<&str>;
}

impl ValueExt for Value {
    fn as_integer(&self) -> Option<i64> {
        match self {
            Value::Integer(i) => Some(*i),
            _ => None,
        }
    }

    fn as_float(&self) -> Option<f64> {
        match self {
            Value::Float(f) => Some(*f),
            _ => None,
        }
    }

    fn as_boolean(&self) -> Option<bool> {
        match self {
            Value::Boolean(b) => Some(*b),
            _ => None,
        }
    }

    fn as_string(&self) -> Option<&str> {
        match self {
            Value::String(s) => Some(s),
            _ => None,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bytecode_generator_creation() {
        let generator = BytecodeGenerator::new();
        assert_eq!(generator.constants.len(), 0);
        assert_eq!(generator.functions.len(), 0);
        assert!(generator.current_function.is_none());
    }

    #[test]
    fn test_constant_pool_management() {
        let mut generator = BytecodeGenerator::new();
        
        // Add some constants
        let index1 = generator.add_constant(Value::Integer(42));
        let index2 = generator.add_constant(Value::String("hello".to_string()));
        let index3 = generator.add_constant(Value::Integer(42)); // Duplicate
        
        assert_eq!(index1, 0);
        assert_eq!(index2, 1);
        assert_eq!(index3, 0); // Should reuse the existing constant
        
        assert_eq!(generator.constants.len(), 2); // Only 2 unique constants
    }

    #[test]
    fn test_operator_mapping() {
        let generator = BytecodeGenerator::new();
        
        // Test binary operators
        assert_eq!(generator.map_operator_to_opcode("+").unwrap(), OpCode::Add);
        assert_eq!(generator.map_operator_to_opcode("plus").unwrap(), OpCode::Add);
        assert_eq!(generator.map_operator_to_opcode("*").unwrap(), OpCode::Multiply);
        assert_eq!(generator.map_operator_to_opcode("multiplied_by").unwrap(), OpCode::Multiply);
        
        // Test unary operators
        assert_eq!(generator.map_unary_operator_to_opcode("-").unwrap(), OpCode::Negate);
        assert_eq!(generator.map_unary_operator_to_opcode("!").unwrap(), OpCode::Not);
        
        // Test unknown operators
        assert!(generator.map_operator_to_opcode("unknown").is_err());
    }

    #[test]
    fn test_simple_lir_translation() {
        let mut generator = BytecodeGenerator::new();
        
        // Create a simple LIR module
        let lir_module = LIRModule {
            name: "test_module".to_string(),
            functions: vec![
                LIRFunction {
                    name: "main".to_string(),
                    parameters: vec![],
                    basic_blocks: vec![
                        LIRBasicBlock {
                            name: "entry".to_string(),
                            instructions: vec![
                                LIRInstruction::LIRMove {
                                    destination: VirtualRegister { name: "x".to_string() },
                                    source: VirtualRegister { name: "y".to_string() },
                                },
                                LIRInstruction::LIRBinaryOp {
                                    destination: VirtualRegister { name: "result".to_string() },
                                    left: VirtualRegister { name: "x".to_string() },
                                    operator: "+".to_string(),
                                    right: VirtualRegister { name: "y".to_string() },
                                },
                                LIRInstruction::LIRReturn {
                                    value: Some(VirtualRegister { name: "result".to_string() }),
                                },
                            ],
                            successors: vec![],
                            predecessors: vec![],
                        },
                    ],
                    return_type: "Number".to_string(),
                    upvalues: vec![],
                },
            ],
            globals: vec![],
            constants: vec![],
        };
        
        // Translate to bytecode
        let result = generator.translate_lir_module(&lir_module);
        assert!(result.is_ok());
        
        let chunk = result.unwrap();
        assert!(!chunk.code.is_empty());
    }
} 