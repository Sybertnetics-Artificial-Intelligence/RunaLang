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
        // Instructions with constant pool references (16-bit operand)
        OpCode::Constant => constant_instruction(op_code, chunk, offset),
        OpCode::GetGlobal | OpCode::SetGlobal | OpCode::Class | OpCode::New |
        OpCode::GetProperty | OpCode::SetProperty | OpCode::Method | OpCode::Throw |
        OpCode::Catch => constant_instruction(op_code, chunk, offset),
        
        // Instructions with single byte operand
        OpCode::ConstantInt => byte_instruction(op_code, chunk, offset),
        OpCode::GetLocal | OpCode::SetLocal | OpCode::GetUpvalue | OpCode::SetUpvalue |
        OpCode::Call | OpCode::CreateList | OpCode::CreateDict | OpCode::CloseUpvalue => 
            byte_instruction(op_code, chunk, offset),
        
        // Jump instructions with 16-bit operand
        OpCode::JumpIfFalse | OpCode::JumpIfTrue | OpCode::Jump | OpCode::Loop => 
            jump_instruction(op_code, chunk, offset),
        
        // Specialized instructions
        OpCode::CallMethod => call_method_instruction(chunk, offset),
        OpCode::Closure => closure_instruction(chunk, offset),
        OpCode::CallNative => call_native_instruction(chunk, offset),
        OpCode::DefineFunction => define_function_instruction(chunk, offset, main_chunk),
        
        // All other instructions have no operands
        _ => simple_instruction(op_code, offset),
    }
}

/// Helper for instructions with no operands.
fn simple_instruction(op_code: OpCode, offset: usize) -> Result<usize, String> {
    println!("{:?}", op_code);
    Ok(offset + 1)
}

/// Helper for instructions with a single 8-bit (byte) operand.
fn byte_instruction(op_code: OpCode, chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 1 >= chunk.code.len() {
        return Err(format!("{:?} instruction missing operand", op_code));
    }
    let slot = chunk.code[offset + 1];
    println!("{:?} {}", op_code, slot);
    Ok(offset + 2)
}

/// Helper for instructions with a 16-bit operand that references the constant pool.
/// This is the "next-gen" version that resolves the constant's value for better debugging.
fn constant_instruction(op_code: OpCode, chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 2 >= chunk.code.len() {
        return Err(format!("{:?} instruction missing operands", op_code));
    }
    let constant_index = ((chunk.code[offset + 1] as u16) << 8) | (chunk.code[offset + 2] as u16);
    
    if constant_index as usize >= chunk.constants.len() {
        println!("{:?} {:4} <INVALID INDEX {}>", op_code, constant_index, constant_index);
        return Ok(offset + 3);
    }
    
    let constant_value = &chunk.constants[constant_index as usize];
    let value_str = match constant_value {
        Value::Function(f) => format!("<Function '{}', arity={}>", f.name, f.arity),
        Value::Float(n) => format!("<Float {}>", n),
        Value::Boolean(b) => format!("<Boolean {}>", b),
        Value::String(s) => format!("<String '{}'>", s),
        Value::Null => "<Null>".to_string(),
        Value::Integer(i) => format!("<Integer {}>", i),
        Value::List(l) => format!("<List with {} items>", l.len()),
        Value::Dictionary(d) => format!("<Dictionary with {} pairs>", d.len()),
        Value::Set(s) => format!("<Set with {} items>", s.len()),
        Value::Tuple(t) => format!("<Tuple with {} items>", t.len()),
        Value::Object(o) => format!("<Object of class {}>", o.class),
        Value::Class(c) => format!("<Class {}>", c.name),
        Value::Optional(opt) => format!("<Optional {}>", if opt.is_some() { "Some" } else { "None" }),
        Value::Result(res) => format!("<Result {}>", if res.is_ok() { "Ok" } else { "Err" }),
        Value::Process(p) => format!("<Process {}>", p),
        Value::Channel(c) => format!("<Channel {}>", c),
        Value::Reference(r) => format!("<Reference {}>", r),
        Value::WeakReference(w) => format!("<WeakReference {}>", w),
        Value::Error(e) => format!("<Error: {}>", e.message),
        Value::NativeFunction(_) => "<NativeFunction>".to_string(),
        Value::Number(n) => format!("{}", n),
        Value::Nil => "nil".to_string(),
    };
    
    println!("{:?} {:4} {}", op_code, constant_index, value_str);
    Ok(offset + 3)
}

/// Helper for jump instructions, showing the jump target.
fn jump_instruction(op_code: OpCode, chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 2 >= chunk.code.len() {
        return Err(format!("{:?} instruction missing operands", op_code));
    }
    let jump = ((chunk.code[offset + 1] as u16) << 8) | (chunk.code[offset + 2] as u16);
    let sign = if op_code == OpCode::Loop { -1 } else { 1 };
    let target = offset as isize + 3 + (sign * jump as isize);
    println!("{:?} {:4} -> {}", op_code, jump, target);
    Ok(offset + 3)
}

fn call_method_instruction(chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 3 >= chunk.code.len() {
        return Err("CallMethod instruction missing operands".to_string());
    }
    let arg_count = chunk.code[offset + 1];
    let method_name = ((chunk.code[offset + 2] as u16) << 8) | (chunk.code[offset + 3] as u16);
    println!("CallMethod {} {:4}", arg_count, method_name);
    Ok(offset + 4)
}

fn closure_instruction(chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 3 >= chunk.code.len() {
        return Err("Closure instruction missing operands".to_string());
    }
    let function_index = ((chunk.code[offset + 1] as u16) << 8) | (chunk.code[offset + 2] as u16);
    let upvalue_count = chunk.code[offset + 3];
    println!("Closure {:4} {:4}", function_index, upvalue_count);
    Ok(offset + 4)
}

fn call_native_instruction(chunk: &Chunk, offset: usize) -> Result<usize, String> {
    if offset + 3 >= chunk.code.len() {
        return Err("CallNative instruction missing operands".to_string());
    }
    let arg_count = chunk.code[offset + 1];
    let function_index = ((chunk.code[offset + 2] as u16) << 8) | (chunk.code[offset + 3] as u16);
    println!("CallNative {} {:4}", arg_count, function_index);
    Ok(offset + 4)
}

fn define_function_instruction(chunk: &Chunk, offset: usize, main_chunk: &Chunk) -> Result<usize, String> {
    if offset + 4 >= chunk.code.len() {
        return Err("DefineFunction instruction missing operands".to_string());
    }
    let name_index = ((chunk.code[offset + 1] as u16) << 8) | (chunk.code[offset + 2] as u16);
    let function_index = ((chunk.code[offset + 3] as u16) << 8) | (chunk.code[offset + 4] as u16);
    
    let name = main_chunk.constants.get(name_index as usize).map(|v| match v {
        Value::String(s) => s.clone(),
        _ => format!("<INVALID NAME TYPE>"),
    }).unwrap_or_else(|| format!("<INVALID NAME INDEX {}>", name_index));
    
    let function_info = main_chunk.constants.get(function_index as usize).map(|v| match v {
        Value::Function(f) => format!("arity={}", f.arity),
        _ => "<INVALID FUNCTION TYPE>".to_string(),
    }).unwrap_or_else(|| format!("<INVALID FUNCTION INDEX {}>", function_index));
    
    println!("DefineFunction     name_idx={} ('{}') function_idx={} ({})", 
             name_index, name, function_index, function_info);
    Ok(offset + 5)
} 