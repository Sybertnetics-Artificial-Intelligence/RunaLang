//! Minimal, robust disassembler for Runa bytecode.

use runa_common::bytecode::{Chunk, OpCode, Value};

pub fn disassemble_chunk(chunk: &Chunk, name: &str) {
    println!("--- Disassembly: {} ---", name);
    let mut offset = 0;
    let mut errors = 0;
    
    while offset < chunk.code.len() {
        match disassemble_instruction(chunk, offset, chunk) {
            Ok(new_offset) => {
                if new_offset <= offset {
                    println!("{:04} <STUCK AT OFFSET {}>", offset, offset);
                    break;
                }
                offset = new_offset;
            }
            Err(e) => {
                println!("{:04} <ERROR: {}>", offset, e);
                errors += 1;
                offset += 1; // Skip one byte and try to continue
                if errors > 10 {
                    println!("{:04} <TOO MANY ERRORS, STOPPING>", offset);
                    break;
                }
            }
        }
    }
    
    if errors > 0 {
        println!("--- Disassembly completed with {} errors ---", errors);
    }
}

fn disassemble_instruction(chunk: &Chunk, offset: usize, main_chunk: &Chunk) -> Result<usize, String> {
    print!("{:04} ", offset);
    
    if offset >= chunk.code.len() {
        return Err("Offset beyond chunk bounds".to_string());
    }
    
    let instruction = chunk.code[offset];
    
    // Try to convert to OpCode, handle unknown values gracefully
    let op_code = if instruction <= OpCode::ReadNumber as u8 {
        unsafe { std::mem::transmute(instruction) }
    } else {
        return Err(format!("Unknown opcode: 0x{:02x} ({})", instruction, instruction));
    };
    
    match op_code {
        OpCode::Constant => {
            if offset + 1 >= chunk.code.len() {
                return Err("Constant instruction missing operand".to_string());
            }
            let const_index = chunk.code[offset + 1] as usize;
            let value = chunk.constants.get(const_index);
            match value {
                Some(Value::Function(f)) => {
                    println!("Constant            {:4} <Function '{}', arity={}>", const_index, f.name, f.arity);
                }
                Some(Value::Number(n)) => {
                    println!("Constant            {:4} <Number {}>", const_index, n);
                }
                Some(Value::Boolean(b)) => {
                    println!("Constant            {:4} <Boolean {}>", const_index, b);
                }
                Some(Value::String(s)) => {
                    println!("Constant            {:4} <String '{}'>", const_index, s);
                }
                Some(Value::Nil) => {
                    println!("Constant            {:4} <Nil>", const_index);
                }
                None => {
                    println!("Constant            {:4} <INVALID INDEX {}>", const_index, const_index);
                }
            }
            Ok(offset + 2)
        }
        OpCode::Add => simple_instruction("Add", offset),
        OpCode::Subtract => simple_instruction("Subtract", offset),
        OpCode::Multiply => simple_instruction("Multiply", offset),
        OpCode::Divide => simple_instruction("Divide", offset),
        OpCode::Negate => simple_instruction("Negate", offset),
        OpCode::Not => simple_instruction("Not", offset),
        OpCode::Equal => simple_instruction("Equal", offset),
        OpCode::NotEqual => simple_instruction("NotEqual", offset),
        OpCode::Greater => simple_instruction("Greater", offset),
        OpCode::GreaterEqual => simple_instruction("GreaterEqual", offset),
        OpCode::Less => simple_instruction("Less", offset),
        OpCode::LessEqual => simple_instruction("LessEqual", offset),
        OpCode::GetLocal => byte_instruction("GetLocal", chunk, offset),
        OpCode::SetLocal => byte_instruction("SetLocal", chunk, offset),
        OpCode::Pop => simple_instruction("Pop", offset),
        OpCode::JumpIfFalse | OpCode::Jump | OpCode::Loop => jump_instruction(op_code, chunk, offset),
        OpCode::Return => simple_instruction("Return", offset),
        OpCode::DefineFunction => define_function_instruction(chunk, offset, main_chunk),
        OpCode::Call => byte_instruction("Call", chunk, offset),
        OpCode::ReturnValue => simple_instruction("ReturnValue", offset),
        OpCode::Concat => simple_instruction("Concat", offset),
        OpCode::Print => simple_instruction("Print", offset),
        OpCode::ReadLine => simple_instruction("ReadLine", offset),
        OpCode::ReadNumber => simple_instruction("ReadNumber", offset),
    }
}

fn simple_instruction(name: &str, offset: usize) -> Result<usize, String> {
    println!("{}", name);
    Ok(offset + 1)
}

fn byte_instruction(name: &str, chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 1 >= chunk.code.len() {
        return Err(format!("{} instruction missing operand", name));
    }
    let slot = chunk.code[offset + 1];
    println!("{:<16} {:4}", name, slot);
    Ok(offset + 2)
}

fn jump_instruction(op_code: OpCode, chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 2 >= chunk.code.len() {
        return Err(format!("{:?} instruction missing operands", op_code));
    }
    let jump = ((chunk.code[offset + 1] as u16) << 8) | (chunk.code[offset + 2] as u16);
    let sign = match op_code {
        OpCode::Loop => -1,
        _ => 1,
    };
    let jump_target = (offset as i16 + 3 + sign * jump as i16) as usize;
    println!("{:<16} {:4} -> {:04}", format!("{:?}", op_code), jump, jump_target);
    Ok(offset + 3)
}

fn define_function_instruction(chunk: &Chunk, offset: usize, main_chunk: &Chunk) -> Result<usize, String> {
    if offset + 2 >= chunk.code.len() {
        return Err("DefineFunction instruction missing operands".to_string());
    }
    let name_index = chunk.code[offset + 1] as usize;
    let param_count = chunk.code[offset + 2];
    let name = main_chunk.constants.get(name_index).map(|v| match v {
        Value::Function(f) => f.name.clone(),
        Value::Number(n) => format!("<Number {}>", n),
        Value::Boolean(b) => format!("<Boolean {}>", b),
        Value::String(s) => format!("<String '{}'>", s),
        Value::Nil => "<Nil>".to_string(),
    }).unwrap_or_else(|| format!("<INVALID INDEX {}>", name_index));
    println!("DefineFunction     name_idx={} ('{}') param_count={}", name_index, name, param_count);
    Ok(offset + 3)
} 