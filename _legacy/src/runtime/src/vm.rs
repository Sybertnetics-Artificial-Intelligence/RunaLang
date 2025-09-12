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
            upvalues: Vec::new(),
            is_native: false,
            native_fn: None,
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
                    (Value::Integer(a_val), Value::Integer(b_val)) => {
                        self.push(Value::Integer(a_val $op b_val));
                    }
                    (Value::Float(a_val), Value::Float(b_val)) => {
                        self.push(Value::Float(a_val $op b_val));
                    }
                    (Value::Integer(a_val), Value::Float(b_val)) => {
                        self.push(Value::Float(a_val as f64 $op b_val));
                    }
                    (Value::Float(a_val), Value::Integer(b_val)) => {
                        self.push(Value::Float(a_val $op b_val as f64));
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
                    (Value::Integer(a_val), Value::Integer(b_val)) => {
                        self.push(Value::Boolean(a_val $op b_val));
                    }
                    (Value::Float(a_val), Value::Float(b_val)) => {
                        self.push(Value::Boolean(a_val $op b_val));
                    }
                    (Value::Integer(a_val), Value::Float(b_val)) => {
                        self.push(Value::Boolean((a_val as f64) $op b_val));
                    }
                    (Value::Float(a_val), Value::Integer(b_val)) => {
                        self.push(Value::Boolean(a_val $op (b_val as f64)));
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
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val + b_val));
                        }
                        (Value::Float(a_val), Value::Float(b_val)) => {
                            self.push(Value::Float(a_val + b_val));
                        }
                        (Value::Integer(a_val), Value::Float(b_val)) => {
                            self.push(Value::Float(a_val as f64 + b_val));
                        }
                        (Value::Float(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Float(a_val + b_val as f64));
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
                OpCode::Modulo => binary_op_num!(%),
                OpCode::Power => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val.pow(b_val as u32)));
                        }
                        (Value::Float(a_val), Value::Float(b_val)) => {
                            self.push(Value::Float(a_val.powf(b_val)));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::Negate => {
                    let value = self.pop();
                    match value {
                        Value::Integer(n) => self.push(Value::Integer(-n)),
                        Value::Float(x) => self.push(Value::Float(-x)),
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                // Natural Language Arithmetic Operators
                OpCode::Plus => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val + b_val));
                        }
                        (Value::Float(a_val), Value::Float(b_val)) => {
                            self.push(Value::Float(a_val + b_val));
                        }
                        (Value::String(a_str), Value::String(b_str)) => {
                            self.push(Value::String(format!("{}{}", a_str, b_str)));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::Minus => binary_op_num!(-),
                OpCode::MultipliedBy => binary_op_num!(*),
                OpCode::DividedBy => binary_op_num!(/),
                OpCode::PowerOf => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val.pow(b_val as u32)));
                        }
                        (Value::Float(a_val), Value::Float(b_val)) => {
                            self.push(Value::Float(a_val.powf(b_val)));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::ModuloOp => binary_op_num!(%),
                // String Operations
                OpCode::Concat => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::String(a_str), Value::String(b_str)) => {
                            self.push(Value::String(format!("{}{}", a_str, b_str)));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::Substring => {
                    let end = self.pop();
                    let start = self.pop();
                    let string = self.pop();
                    match (string, start, end) {
                        (Value::String(s), Value::Integer(start_idx), Value::Integer(end_idx)) => {
                            if start_idx >= 0 && end_idx >= start_idx && end_idx <= s.len() as i64 {
                                let start = start_idx as usize;
                                let end = end_idx as usize;
                                self.push(Value::String(s[start..end].to_string()));
                            } else {
                                return InterpretResult::RuntimeError;
                            }
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::StringLength => {
                    let value = self.pop();
                    match value {
                        Value::String(s) => self.push(Value::Integer(s.len() as i64)),
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                // Logic Operations
                OpCode::Not => {
                    let value = self.pop();
                    match value {
                        Value::Boolean(b) => self.push(Value::Boolean(!b)),
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::And => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Boolean(a_val), Value::Boolean(b_val)) => {
                            self.push(Value::Boolean(a_val && b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::Or => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Boolean(a_val), Value::Boolean(b_val)) => {
                            self.push(Value::Boolean(a_val || b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                // Natural Language Logic Operators
                OpCode::LogicalAnd => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Boolean(a_val), Value::Boolean(b_val)) => {
                            self.push(Value::Boolean(a_val && b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::LogicalOr => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Boolean(a_val), Value::Boolean(b_val)) => {
                            self.push(Value::Boolean(a_val || b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::LogicalNot => {
                    let value = self.pop();
                    match value {
                        Value::Boolean(b) => self.push(Value::Boolean(!b)),
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                // Comparison Operations
                OpCode::Equal => binary_op_bool!(==),
                OpCode::NotEqual => binary_op_bool!(!=),
                OpCode::Greater => binary_op_bool!(>),
                OpCode::GreaterEqual => binary_op_bool!(>=),
                OpCode::Less => binary_op_bool!(<),
                OpCode::LessEqual => binary_op_bool!(<=),
                // Natural Language Comparison Operators
                OpCode::IsEqualTo => binary_op_bool!(==),
                OpCode::IsNotEqualTo => binary_op_bool!(!=),
                OpCode::IsGreaterThan => binary_op_bool!(>),
                OpCode::IsLessThan => binary_op_bool!(<),
                OpCode::IsGreaterThanOrEqualTo => binary_op_bool!(>=),
                OpCode::IsLessThanOrEqualTo => binary_op_bool!(<=),
                // Bitwise Operations
                OpCode::BitwiseAnd => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val & b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::BitwiseOr => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val | b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::BitwiseXor => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val ^ b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::BitwiseNot => {
                    let value = self.pop();
                    match value {
                        Value::Integer(n) => self.push(Value::Integer(!n)),
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::ShiftLeft => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val << b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::ShiftRight => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val >> b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                // Natural Language Bitwise Operators
                OpCode::BitwiseAndOp => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val & b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::BitwiseOrOp => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val | b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::BitwiseXorOp => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val ^ b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::BitwiseNotOp => {
                    let value = self.pop();
                    match value {
                        Value::Integer(n) => self.push(Value::Integer(!n)),
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::ShiftedLeftBy => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val << b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
                OpCode::ShiftedRightBy => {
                    let b = self.pop();
                    let a = self.pop();
                    match (a, b) {
                        (Value::Integer(a_val), Value::Integer(b_val)) => {
                            self.push(Value::Integer(a_val >> b_val));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                },
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
                OpCode::DefineFunction => {
                    let ip = self.current_frame().ip;
                    let name_index = self.current_chunk().code[ip] as usize;
                    let param_count = self.current_chunk().code[ip + 1] as usize;
                    self.current_frame_mut().ip += 2;
                    let name = match &self.current_chunk().constants[name_index] {
                        Value::String(s) => s.clone(),
                        _ => return InterpretResult::RuntimeError,
                    };
                    let function = Function {
                        name,
                        chunk: Chunk::new(),
                        arity: param_count,
                        upvalues: Vec::new(),
                        is_native: false,
                        native_fn: None,
                    };
                    self.push(Value::Function(Box::new(function)));
                }
                OpCode::Call => {
                    let ip = self.current_frame().ip;
                    let arg_count = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let function = self.peek(arg_count).clone();
                    match function {
                        Value::Function(func) => {
                            self.call_function(*func, arg_count);
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::Print => {
                    let value = self.pop();
                    println!("{}", value);
                }
                OpCode::ReadLine => {
                    let mut input = String::new();
                    std::io::stdin().read_line(&mut input).unwrap();
                    self.push(Value::String(input.trim().to_string()));
                }
                OpCode::ReadNumber => {
                    let mut input = String::new();
                    std::io::stdin().read_line(&mut input).unwrap();
                    match input.trim().parse::<f64>() {
                        Ok(n) => self.push(Value::Number(n)),
                        Err(_) => return InterpretResult::RuntimeError,
                    }
                }
                // --- Language Keywords ---
                OpCode::Display => {
                    let value = self.pop();
                    println!("{}", value);
                }
                OpCode::Length => {
                    let value = self.pop();
                    let length = match value {
                        Value::String(s) => s.len() as f64,
                        Value::List(items) => items.len() as f64,
                        Value::Dictionary(items) => items.len() as f64,
                        _ => return InterpretResult::RuntimeError,
                    };
                    self.push(Value::Number(length));
                }
                OpCode::GetItem => {
                    let index = self.pop();
                    let list = self.pop();
                    match (list, index) {
                        (Value::List(items), Value::Number(idx)) => {
                            let idx = idx as usize;
                            if idx < items.len() {
                                self.push(items[idx].clone());
                            } else {
                                return InterpretResult::RuntimeError;
                            }
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::SetItem => {
                    let value = self.pop();
                    let index = self.pop();
                    let list = self.pop();
                    match (list, index, value) {
                        (Value::List(mut items), Value::Number(idx), val) => {
                            let idx = idx as usize;
                            if idx < items.len() {
                                items[idx] = val;
                                self.push(Value::List(items));
                            } else {
                                return InterpretResult::RuntimeError;
                            }
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::GetDict => {
                    let key = self.pop();
                    let dict = self.pop();
                    match dict {
                        Value::Dictionary(items) => {
                            if let Some((_, value)) = items.iter().find(|(k, _)| k == &key) {
                                self.push(value.clone());
                            } else {
                                self.push(Value::Nil);
                            }
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::SetDict => {
                    let value = self.pop();
                    let key = self.pop();
                    let dict = self.pop();
                    match dict {
                        Value::Dictionary(mut items) => {
                            // Remove existing key if present
                            items.retain(|(k, _)| k != &key);
                            // Add new key-value pair
                            items.push((key, value));
                            self.push(Value::Dictionary(items));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::CreateList => {
                    let ip = self.current_frame().ip;
                    let item_count = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let mut items = Vec::new();
                    for _ in 0..item_count {
                        items.push(self.pop());
                    }
                    items.reverse(); // Restore original order
                    self.push(Value::List(items));
                }
                OpCode::CreateDict => {
                    let ip = self.current_frame().ip;
                    let pair_count = self.current_chunk().code[ip] as usize;
                    self.current_frame_mut().ip += 1;
                    let mut items = Vec::new();
                    for _ in 0..pair_count {
                        let value = self.pop();
                        let key = self.pop();
                        items.push((key, value));
                    }
                    items.reverse(); // Restore original order
                    self.push(Value::Dictionary(items));
                }
                OpCode::AddToList => {
                    let item = self.pop();
                    let list = self.pop();
                    match list {
                        Value::List(mut items) => {
                            items.push(item);
                            self.push(Value::List(items));
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::RemoveFromList => {
                    let item = self.pop();
                    let list = self.pop();
                    match list {
                        Value::List(mut items) => {
                            if let Some(pos) = items.iter().position(|x| x == &item) {
                                items.remove(pos);
                                self.push(Value::List(items));
                                self.push(Value::Boolean(true));
                            } else {
                                self.push(Value::List(items));
                                self.push(Value::Boolean(false));
                            }
                        }
                        _ => return InterpretResult::RuntimeError,
                    }
                }
                OpCode::Contains => {
                    let item = self.pop();
                    let collection = self.pop();
                    let contains = match collection {
                        Value::List(items) => items.contains(&item),
                        Value::String(s) => {
                            if let Value::String(substr) = item {
                                s.contains(&substr)
                            } else {
                                false
                            }
                        }
                        Value::Dictionary(items) => {
                            items.iter().any(|(k, _)| k == &item)
                        }
                        _ => false,
                    };
                    self.push(Value::Boolean(contains));
                }
                OpCode::ToString => {
                    let value = self.pop();
                    let string = match value {
                        Value::String(s) => s,
                        Value::Number(n) => n.to_string(),
                        Value::Boolean(b) => b.to_string(),
                        Value::List(_) => "[list]".to_string(),
                        Value::Dictionary(_) => "{dictionary}".to_string(),
                        Value::Function(func) => format!("<function {}>", func.name),
                        Value::Nil => "nil".to_string(),
                    };
                    self.push(Value::String(string));
                }
                OpCode::ToInteger => {
                    let value = self.pop();
                    let integer = match value {
                        Value::Number(n) => n as i64 as f64,
                        Value::String(s) => {
                            match s.parse::<f64>() {
                                Ok(n) => n,
                                Err(_) => return InterpretResult::RuntimeError,
                            }
                        }
                        Value::Boolean(b) => if b { 1.0 } else { 0.0 },
                        _ => return InterpretResult::RuntimeError,
                    };
                    self.push(Value::Number(integer));
                }
                OpCode::ToFloat => {
                    let value = self.pop();
                    let float = match value {
                        Value::Number(n) => n,
                        Value::String(s) => {
                            match s.parse::<f64>() {
                                Ok(n) => n,
                                Err(_) => return InterpretResult::RuntimeError,
                            }
                        }
                        Value::Boolean(b) => if b { 1.0 } else { 0.0 },
                        _ => return InterpretResult::RuntimeError,
                    };
                    self.push(Value::Number(float));
                }
                OpCode::ToBoolean => {
                    let value = self.pop();
                    let boolean = match value {
                        Value::Boolean(b) => b,
                        Value::Number(n) => n != 0.0,
                        Value::String(s) => !s.is_empty(),
                        Value::List(items) => !items.is_empty(),
                        Value::Dictionary(items) => !items.is_empty(),
                        Value::Function(_) => true,
                        Value::Nil => false,
                    };
                    self.push(Value::Boolean(boolean));
                }
                OpCode::TypeOf => {
                    let value = self.pop();
                    let type_name = match value {
                        Value::Number(_) => "Number",
                        Value::Boolean(_) => "Boolean",
                        Value::String(_) => "String",
                        Value::List(_) => "List",
                        Value::Dictionary(_) => "Dictionary",
                        Value::Function(_) => "Function",
                        Value::Nil => "Nil",
                    };
                    self.push(Value::String(type_name.to_string()));
                }
                OpCode::IsNone => {
                    let value = self.pop();
                    self.push(Value::Boolean(matches!(value, Value::Nil)));
                }
                OpCode::IsNotNone => {
                    let value = self.pop();
                    self.push(Value::Boolean(!matches!(value, Value::Nil)));
                }
                _ => {
                    eprintln!("Runtime error: Unknown opcode {:?} at instruction {}", op_code, self.current_frame().ip - 1);
                    self.runtime_error(&format!("Unknown opcode: {:?}", op_code));
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
    
    fn runtime_error(&mut self, message: &str) {
        eprintln!("Runtime error: {}", message);
        if !self.frames.is_empty() {
            eprintln!("At instruction {} in current function", self.current_frame().ip);
        }
    }
} 