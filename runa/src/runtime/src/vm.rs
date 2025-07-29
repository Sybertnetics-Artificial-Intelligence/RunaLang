//! The Runa Virtual Machine.

use runa_common::bytecode::{Chunk, OpCode, Value, Function};
use std::collections::HashMap;

// These constants will be used when implementing stack overflow protection
// and frame limit enforcement in future versions
#[allow(dead_code)]
const STACK_MAX: usize = 256;
#[allow(dead_code)]
const FRAMES_MAX: usize = 64;



#[derive(Debug)]
pub struct CallFrame {
    pub function: Function,
    pub ip: usize,
    pub slot: usize, // Stack slot where this frame's locals begin
}

pub struct VirtualMachine {
    frames: Vec<CallFrame>,
    stack: Vec<Value>,
    globals: HashMap<String, Value>,
}

pub enum InterpretResult {
    Ok,
    CompileError,
    RuntimeError,
}

impl VirtualMachine {
    pub fn new() -> Self {
        VirtualMachine {
            frames: Vec::new(),
            stack: Vec::new(),
            globals: HashMap::new(),
        }
    }

    pub fn interpret(chunk: Chunk) -> InterpretResult {
        let mut vm = VirtualMachine::new();
        let main_function = Function {
            name: "script".to_string(),
            chunk,
            arity: 0,
        };
        vm.call_function(main_function, 0);
        vm.run()
    }

    fn call_function(&mut self, function: Function, arg_count: usize) -> InterpretResult {
        if self.frames.len() >= 64 {
            println!("Stack overflow");
            return InterpretResult::RuntimeError;
        }
        
        let slot = if self.stack.len() >= arg_count { self.stack.len() - arg_count } else { 0 };
        let frame = CallFrame {
            function,
            ip: 0,
            slot,
        };
        self.frames.push(frame);
        InterpretResult::Ok
    }
    
    #[allow(dead_code)]
    fn call_function_by_name(&mut self, name: &str, arg_count: usize) -> InterpretResult {
        if let Some(function_value) = self.globals.get(name) {
            if let Value::Function(function) = function_value {
                return self.call_function(*function.clone(), arg_count);
            }
        }
        println!("Undefined function '{}'", name);
        InterpretResult::RuntimeError
    }

    fn current_frame(&self) -> &CallFrame {
        self.frames.last().expect("No call frame")
    }
    fn current_frame_mut(&mut self) -> &mut CallFrame {
        self.frames.last_mut().expect("No call frame")
    }
    fn current_chunk(&self) -> &Chunk {
        &self.current_frame().function.chunk
    }

    fn run(&mut self) -> InterpretResult {
        macro_rules! binary_op_num {
            ($op:tt) => {{
                let b = self.pop();
                let a = self.pop();
                match (a, b) {
                    (Value::Number(a_val), Value::Number(b_val)) => {
                        self.push(Value::Number(a_val $op b_val));
                    }
                    _ => return InterpretResult::RuntimeError,
                }
            }};
        }
        macro_rules! binary_op_bool {
            ($op:tt) => {{
                let b = self.pop();
                let a = self.pop();
                match (a, b) {
                    (Value::Number(a_val), Value::Number(b_val)) => {
                        self.push(Value::Boolean(a_val $op b_val));
                    }
                    _ => return InterpretResult::RuntimeError,
                }
            }};
        }
        loop {
            let ip = self.current_frame().ip;
            let instruction_byte = self.current_chunk().code[ip];
            self.current_frame_mut().ip += 1;
            let op_code: OpCode = unsafe { std::mem::transmute(instruction_byte) };
            match op_code {
                OpCode::Constant => {
                    let ip = self.current_frame().ip;
                    let const_index = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let constant = self.current_chunk().constants[const_index].clone();
                    self.push(constant);
                }
                OpCode::GetLocal => {
                    let ip = self.current_frame().ip;
                    let slot = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let idx = self.current_frame().slot + slot;
                    self.push(self.stack[idx].clone());
                }
                OpCode::SetLocal => {
                    let ip = self.current_frame().ip;
                    let slot = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let idx = self.current_frame().slot + slot;
                    self.stack[idx] = self.peek(0).clone();
                }
                OpCode::Pop => { self.pop(); }
                OpCode::Add => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Number(a_val), Value::Number(b_val)) => {
                            self.push(Value::Number(a_val + b_val));
                        }
                        (Value::String(a_str), Value::String(b_str)) => {
                            self.push(Value::String(format!("{}{}", a_str, b_str)));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::Subtract => binary_op_num!(-),
                OpCode::Multiply => binary_op_num!(*),
                OpCode::Divide => binary_op_num!(/),
                OpCode::Equal => binary_op_bool!(==),
                OpCode::NotEqual => binary_op_bool!(!=),
                OpCode::Greater => binary_op_bool!(>),
                OpCode::GreaterEqual => binary_op_bool!(>=),
                OpCode::Less => binary_op_bool!(<),
                OpCode::LessEqual => binary_op_bool!(<=),
                OpCode::Jump => {
                    let offset = self.read_short();
                    self.current_frame_mut().ip += offset;
                }
                OpCode::JumpIfFalse => {
                    let offset = self.read_short();
                    if self.peek(0) == Value::Boolean(false) {
                        self.current_frame_mut().ip += offset;
                    }
                }
                OpCode::Loop => {
                    let offset = self.read_short();
                    self.current_frame_mut().ip -= offset;
                }
                OpCode::Return => {
                    // No value to return, just pop the frame
                    let slot = self.current_frame().slot;
                    self.stack.truncate(slot);
                    self.frames.pop();
                    if self.frames.is_empty() {
                        self.print_stack_top();
                        return InterpretResult::Ok;
                    }
                }
                OpCode::ReturnValue => {
                    let result = self.pop();
                    let slot = self.current_frame().slot;
                    self.stack.truncate(slot);
                    self.push(result);
                    self.frames.pop();
                    if self.frames.is_empty() {
                        self.print_stack_top();
                        return InterpretResult::Ok;
                    }
                }
                OpCode::Call => {
                    let ip = self.current_frame().ip;
                    let arg_count = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    
                    // Get the function from the stack
                    let function_value = self.stack[self.stack.len() - arg_count - 1].clone();
                    
                    match function_value {
                        Value::Function(function) => {
                            // Remove the function and arguments from the stack
                            for _ in 0..arg_count + 1 {
                                self.pop();
                            }
                            
                            // Call the function
                            if let InterpretResult::RuntimeError = self.call_function(*function, arg_count) {
                                return InterpretResult::RuntimeError;
                            }
                        }
                        _ => {
                            println!("Can only call functions");
                            return InterpretResult::RuntimeError;
                        }
                    }
                }
                OpCode::DefineFunction => {
                    let ip = self.current_frame().ip;
                    let name_index = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let _param_count = self.current_chunk().code[self.current_frame().ip] as usize;
                    self.current_frame_mut().ip += 1;
                    
                    // The function is already on the stack from the Constant opcode
                    // We keep it there for the SetLocal instruction that follows
                    // Just store a copy in globals for debugging/fallback
                    if let Some(function_value) = self.stack.last() {
                        if let Value::Function(function) = function_value {
                            let function_name = format!("function_{}", name_index);
                            self.globals.insert(function_name, Value::Function(function.clone()));
                        }
                    }
                }
                OpCode::Concat => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::String(a_str), Value::String(b_str)) => {
                            self.push(Value::String(format!("{}{}", a_str, b_str)));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::Print => {
                    let value = self.pop();
                    println!("{}", value);
                }
                OpCode::ReadLine => {
                    use std::io::{self, Write};
                    io::stdout().flush().unwrap();
                    let mut input = String::new();
                    if io::stdin().read_line(&mut input).is_ok() {
                        // Remove trailing newline
                        input = input.trim_end_matches('\n').to_string();
                        self.push(Value::String(input));
                    } else {
                        self.push(Value::String("".to_string()));
                    }
                }
                OpCode::ReadNumber => {
                    use std::io::{self, Write};
                    io::stdout().flush().unwrap();
                    let mut input = String::new();
                    if io::stdin().read_line(&mut input).is_ok() {
                        if let Ok(num) = input.trim().parse::<f64>() {
                            self.push(Value::Number(num));
                        } else {
                            self.push(Value::Number(0.0));
                        }
                    } else {
                        self.push(Value::Number(0.0));
                    }
                }
                _ => {
                    println!("Unimplemented opcode: {:?}", op_code);
                    return InterpretResult::RuntimeError;
                }
            }
        }
    }

    fn read_short(&mut self) -> usize {
        let ip = self.current_frame().ip;
        let chunk = self.current_chunk();
        let high = chunk.code[ip] as usize;
        let low = chunk.code[ip + 1] as usize;
        self.current_frame_mut().ip += 2;
        (high << 8) | low
    }

    fn peek(&self, distance: usize) -> Value {
        self.stack[self.stack.len() - 1 - distance].clone()
    }

    fn push(&mut self, value: Value) {
        self.stack.push(value);
    }

    fn pop(&mut self) -> Value {
        self.stack.pop().expect("Stack underflow")
    }
    
    fn print_stack_top(&self) {
        if let Some(val) = self.stack.last() {
            println!("VM Result: {:?}", val);
        }
    }
} 