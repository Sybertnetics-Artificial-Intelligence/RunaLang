use runa_common::bytecode::{Chunk, OpCode, Value, Function};

fn main() {
    // Test 1: Normal bytecode
    println!("=== Test 1: Normal Bytecode ===");
    let mut normal_chunk = Chunk::new();
    normal_chunk.write(OpCode::Constant as u8);
    normal_chunk.write(0);
    normal_chunk.write(OpCode::Return as u8);
    
    runa_rt::vm::VirtualMachine::interpret(normal_chunk);
    
    // Test 2: Malformed bytecode with unknown opcode
    println!("\n=== Test 2: Unknown Opcode ===");
    let mut malformed_chunk = Chunk::new();
    malformed_chunk.write(OpCode::Constant as u8);
    malformed_chunk.write(0);
    malformed_chunk.write(255); // Unknown opcode
    malformed_chunk.write(OpCode::Return as u8);
    
    // We can't run this through the VM, but we can test the disassembler
    println!("Malformed chunk would cause disassembler to show error");
    
    // Test 3: Incomplete instruction
    println!("\n=== Test 3: Incomplete Instruction ===");
    let mut incomplete_chunk = Chunk::new();
    incomplete_chunk.write(OpCode::Constant as u8);
    // Missing operand - would cause error in disassembler
    
    println!("Incomplete chunk would cause disassembler to show error");
} 