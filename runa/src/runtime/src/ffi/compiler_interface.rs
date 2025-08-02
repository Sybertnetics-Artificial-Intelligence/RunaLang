//! Compiler-Runtime FFI Interface
//!
//! This module provides the direct, in-memory communication between the Runa compiler
//! and the Runa runtime, eliminating the need for JSON serialization.

use crate::bytecode_generator::BytecodeGenerator;
use crate::vm::VirtualMachine;
use runa_common::bytecode::{Chunk, Value};
use std::ffi::{c_char, CStr, CString};
use std::ptr;

/// FFI-compatible LIR instruction structure
#[repr(C)]
pub struct FfiLirInstruction {
    pub opcode: u8,
    pub operand1: *const c_char,
    pub operand2: *const c_char,
    pub operand3: *const c_char,
    pub metadata: *const c_char,
}

/// FFI-compatible LIR basic block structure
#[repr(C)]
pub struct FfiLirBasicBlock {
    pub name: *const c_char,
    pub instructions: *const FfiLirInstruction,
    pub instruction_count: usize,
    pub successors: *const *const c_char,
    pub successor_count: usize,
}

/// FFI-compatible LIR function structure
#[repr(C)]
pub struct FfiLirFunction {
    pub name: *const c_char,
    pub basic_blocks: *const FfiLirBasicBlock,
    pub basic_block_count: usize,
    pub parameters: *const *const c_char,
    pub parameter_count: usize,
    pub return_type: *const c_char,
    pub upvalues: *const FfiUpvalue,
    pub upvalue_count: usize,
}

/// FFI-compatible upvalue structure
#[repr(C)]
pub struct FfiUpvalue {
    pub index: u32,
    pub is_local: bool,
}

/// FFI-compatible LIR module structure
#[repr(C)]
pub struct FfiLirModule {
    pub name: *const c_char,
    pub functions: *const FfiLirFunction,
    pub function_count: usize,
    pub globals: *const FfiGlobal,
    pub global_count: usize,
    pub constants: *const FfiConstant,
    pub constant_count: usize,
}

/// FFI-compatible global variable structure
#[repr(C)]
pub struct FfiGlobal {
    pub name: *const c_char,
    pub type_name: *const c_char,
    pub initial_value: *const c_char,
}

/// FFI-compatible constant structure
#[repr(C)]
pub struct FfiConstant {
    pub name: *const c_char,
    pub type_name: *const c_char,
    pub value: *const c_char,
}

/// FFI-compatible compilation result
#[repr(C)]
pub struct FfiCompilationResult {
    pub success: bool,
    pub bytecode: *mut Chunk,
    pub error_message: *const c_char,
}

/// Convert FFI string to Rust string safely
fn ffi_string_to_rust(ffi_str: *const c_char) -> Option<String> {
    if ffi_str.is_null() {
        return None;
    }
    
    unsafe {
        CStr::from_ptr(ffi_str)
            .to_str()
            .ok()
            .map(|s| s.to_string())
    }
}

/// Convert Rust string to FFI string
fn rust_string_to_ffi(rust_str: &str) -> *const c_char {
    match CString::new(rust_str) {
        Ok(c_string) => c_string.into_raw(),
        Err(_) => ptr::null(),
    }
}

/// Main FFI function: Translate LIR module to bytecode
#[no_mangle]
pub extern "C" fn runa_translate_lir_to_bytecode(
    lir_module: *const FfiLirModule,
) -> FfiCompilationResult {
    if lir_module.is_null() {
        return FfiCompilationResult {
            success: false,
            bytecode: ptr::null_mut(),
            error_message: rust_string_to_ffi("Null LIR module"),
        };
    }

    let module = unsafe { &*lir_module };
    
    // Convert FFI LIR to internal LIR format
    let internal_lir = match convert_ffi_lir_to_internal(module) {
        Ok(lir) => lir,
        Err(error) => {
            return FfiCompilationResult {
                success: false,
                bytecode: ptr::null_mut(),
                error_message: rust_string_to_ffi(&error),
            };
        }
    };

    // Generate bytecode using existing BytecodeGenerator
    let mut generator = BytecodeGenerator::new();
    match generator.translate_lir_module(&internal_lir) {
        Ok(chunk) => {
            let boxed_chunk = Box::new(chunk);
            FfiCompilationResult {
                success: true,
                bytecode: Box::into_raw(boxed_chunk),
                error_message: ptr::null(),
            }
        }
        Err(error) => {
            FfiCompilationResult {
                success: false,
                bytecode: ptr::null_mut(),
                error_message: rust_string_to_ffi(&error),
            }
        }
    }
}

/// Convert FFI LIR module to internal LIR format
fn convert_ffi_lir_to_internal(ffi_module: &FfiLirModule) -> Result<crate::bytecode_generator::LIRModule, String> {
    let name = ffi_string_to_rust(ffi_module.name)
        .ok_or("Invalid module name")?;
    
    let mut functions = Vec::new();
    let ffi_functions = unsafe {
        std::slice::from_raw_parts(ffi_module.functions, ffi_module.function_count)
    };
    
    for ffi_function in ffi_functions {
        let function = convert_ffi_function_to_internal(ffi_function)?;
        functions.push(function);
    }
    
    let mut globals = Vec::new();
    let ffi_globals = unsafe {
        std::slice::from_raw_parts(ffi_module.globals, ffi_module.global_count)
    };
    
    for ffi_global in ffi_globals {
        let name = ffi_string_to_rust(ffi_global.name)
            .ok_or("Invalid global name")?;
        let type_name = ffi_string_to_rust(ffi_global.type_name)
            .unwrap_or_else(|| "Any".to_string());
        let initial_value = ffi_string_to_rust(ffi_global.initial_value)
            .unwrap_or_else(|| "None".to_string());
        
        globals.push(crate::bytecode_generator::LIRGlobal {
            name,
            type_name,
            initial_value
        });
    }
    
    let mut constants = Vec::new();
    let ffi_constants = unsafe {
        std::slice::from_raw_parts(ffi_module.constants, ffi_module.constant_count)
    };
    
    for ffi_constant in ffi_constants {
        let name = ffi_string_to_rust(ffi_constant.name)
            .ok_or("Invalid constant name")?;
        let type_name = ffi_string_to_rust(ffi_constant.type_name)
            .unwrap_or_else(|| "Any".to_string());
        let value = ffi_string_to_rust(ffi_constant.value)
            .unwrap_or_else(|| "None".to_string());
        
        constants.push(crate::bytecode_generator::LIRConstant {
            name,
            type_name,
            value
        });
    }
    
    Ok(crate::bytecode_generator::LIRModule {
        name,
        functions,
        globals,
        constants,
    })
}

/// Convert FFI function to internal function format
fn convert_ffi_function_to_internal(ffi_function: &FfiLirFunction) -> Result<crate::bytecode_generator::LIRFunction, String> {
    let name = ffi_string_to_rust(ffi_function.name)
        .ok_or("Invalid function name")?;
    
    let mut basic_blocks = Vec::new();
    let ffi_blocks = unsafe {
        std::slice::from_raw_parts(ffi_function.basic_blocks, ffi_function.basic_block_count)
    };
    
    for ffi_block in ffi_blocks {
        let block = convert_ffi_basic_block_to_internal(ffi_block)?;
        basic_blocks.push(block);
    }
    
    let mut parameters = Vec::new();
    let ffi_parameters = unsafe {
        std::slice::from_raw_parts(ffi_function.parameters, ffi_function.parameter_count)
    };
    
    for (index, ffi_param) in ffi_parameters.iter().enumerate() {
        let name = ffi_string_to_rust(*ffi_param)
            .ok_or("Invalid parameter name")?;
        parameters.push(crate::bytecode_generator::LIRParameter {
            name,
            type_name: "Any".to_string(),
            index
        });
    }
    
    let return_type = ffi_string_to_rust(ffi_function.return_type)
        .unwrap_or_else(|| "Any".to_string());
    
    let mut upvalues = Vec::new();
    let ffi_upvalues = unsafe {
        std::slice::from_raw_parts(ffi_function.upvalues, ffi_function.upvalue_count)
    };
    
    for ffi_upvalue in ffi_upvalues {
        upvalues.push(crate::bytecode_generator::LIRUpvalue {
            index: ffi_upvalue.index as usize,
            is_local: ffi_upvalue.is_local
        });
    }
    
    Ok(crate::bytecode_generator::LIRFunction {
        name,
        basic_blocks,
        parameters,
        return_type,
        upvalues,
    })
}

/// Convert FFI basic block to internal basic block format
fn convert_ffi_basic_block_to_internal(ffi_block: &FfiLirBasicBlock) -> Result<crate::bytecode_generator::LIRBasicBlock, String> {
    let name = ffi_string_to_rust(ffi_block.name)
        .ok_or("Invalid block name")?;
    
    let mut instructions = Vec::new();
    let ffi_instructions = unsafe {
        std::slice::from_raw_parts(ffi_block.instructions, ffi_block.instruction_count)
    };
    
    for ffi_instruction in ffi_instructions {
        let instruction = convert_ffi_instruction_to_internal(ffi_instruction)?;
        instructions.push(instruction);
    }
    
    let mut successors = Vec::new();
    let ffi_successors = unsafe {
        std::slice::from_raw_parts(ffi_block.successors, ffi_block.successor_count)
    };
    
    for ffi_successor in ffi_successors {
        let successor = ffi_string_to_rust(*ffi_successor)
            .unwrap_or_else(|| "unknown".to_string());
        successors.push(successor);
    }
    
    Ok(crate::bytecode_generator::LIRBasicBlock {
        name,
        instructions,
        successors,
        predecessors: Vec::new(), // Predecessors are computed during analysis
    })
}

/// Convert FFI instruction to internal instruction format
fn convert_ffi_instruction_to_internal(ffi_instruction: &FfiLirInstruction) -> Result<crate::bytecode_generator::LIRInstruction, String> {
    let opcode = ffi_instruction.opcode;
    let operand1 = ffi_string_to_rust(ffi_instruction.operand1);
    let operand2 = ffi_string_to_rust(ffi_instruction.operand2);
    let operand3 = ffi_string_to_rust(ffi_instruction.operand3);
    
    match opcode {
        0 => Ok(crate::bytecode_generator::LIRInstruction::LIRNop),
        1 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let source = operand2.ok_or("Missing source operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRMove {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                source: crate::bytecode_generator::VirtualRegister { name: source }
            })
        }
        2 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let value = operand2.ok_or("Missing value operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRLoadConstant {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                value: value
            })
        }
        3 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let source = operand2.ok_or("Missing source operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRLoad {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                source: crate::bytecode_generator::MemoryAddress::LIRDirectAddress {
                    offset: 0
                }
            })
        }
        4 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let value = operand2.ok_or("Missing value operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRStore {
                destination: crate::bytecode_generator::MemoryAddress::LIRDirectAddress {
                    offset: 0
                },
                source: crate::bytecode_generator::VirtualRegister { name: value }
            })
        }
        5 => {
            let function = operand1.ok_or("Missing function operand")?;
            let args = operand2.map(|s| s.split(',').map(|s| s.trim().to_string()).collect()).unwrap_or_default();
            let result = operand3.map(|s| crate::bytecode_generator::VirtualRegister { name: s });
            Ok(crate::bytecode_generator::LIRInstruction::LIRCall {
                destination: result,
                function,
                arguments: args.into_iter().map(|s| crate::bytecode_generator::VirtualRegister { name: s }).collect()
            })
        }
        6 => {
            let condition = operand1.ok_or("Missing condition operand")?;
            let true_target = operand2.ok_or("Missing true target operand")?;
            let false_target = operand3.unwrap_or_default();
            Ok(crate::bytecode_generator::LIRInstruction::LIRBranch {
                condition: crate::bytecode_generator::VirtualRegister { name: condition },
                true_target,
                false_target
            })
        }
        7 => {
            let target = operand1.ok_or("Missing target operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRJump { target })
        }
        8 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let left = operand2.ok_or("Missing left operand")?;
            let right = operand3.ok_or("Missing right operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRBinaryOp {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                left: crate::bytecode_generator::VirtualRegister { name: left },
                right: crate::bytecode_generator::VirtualRegister { name: right },
                operator: "add".to_string()
            })
        }
        9 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let left = operand2.ok_or("Missing left operand")?;
            let right = operand3.ok_or("Missing right operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRBinaryOp {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                left: crate::bytecode_generator::VirtualRegister { name: left },
                right: crate::bytecode_generator::VirtualRegister { name: right },
                operator: "subtract".to_string()
            })
        }
        10 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let left = operand2.ok_or("Missing left operand")?;
            let right = operand3.ok_or("Missing right operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRBinaryOp {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                left: crate::bytecode_generator::VirtualRegister { name: left },
                right: crate::bytecode_generator::VirtualRegister { name: right },
                operator: "multiply".to_string()
            })
        }
        11 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let left = operand2.ok_or("Missing left operand")?;
            let right = operand3.ok_or("Missing right operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRBinaryOp {
                destination: crate::bytecode_generator::VirtualRegister { name: destination },
                left: crate::bytecode_generator::VirtualRegister { name: left },
                right: crate::bytecode_generator::VirtualRegister { name: right },
                operator: "divide".to_string()
            })
        }
        12 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let value = operand2.ok_or("Missing value operand")?;
            Ok(crate::bytecode_generator::LIRInstruction::LIRReturn {
                value: Some(crate::bytecode_generator::VirtualRegister { name: value })
            })
        }
        13 => {
            Ok(crate::bytecode_generator::LIRInstruction::LIRReturn { value: None })
        }
        14 => {
            let destination = operand1.ok_or("Missing destination operand")?;
            let intrinsic = operand2.ok_or("Missing intrinsic operand")?;
            let args = operand3.map(|s| s.split(',').map(|s| s.trim().to_string()).collect()).unwrap_or_default();
            Ok(crate::bytecode_generator::LIRInstruction::LIRIntrinsic {
                destination: Some(crate::bytecode_generator::VirtualRegister { name: destination }),
                intrinsic_name: intrinsic,
                arguments: args.into_iter().map(|s| crate::bytecode_generator::VirtualRegister { name: s }).collect()
            })
        }
        _ => Err(format!("Unknown opcode: {}", opcode))
    }
}

/// Execute bytecode in VM
#[no_mangle]
pub extern "C" fn runa_execute_bytecode(
    bytecode: *mut Chunk,
) -> FfiCompilationResult {
    if bytecode.is_null() {
        return FfiCompilationResult {
            success: false,
            bytecode: ptr::null_mut(),
            error_message: rust_string_to_ffi("Null bytecode"),
        };
    }

    let chunk = unsafe { &*bytecode };
    let mut vm = VirtualMachine::new();
    
    match vm.interpret(chunk) {
        Ok(_) => {
            FfiCompilationResult {
                success: true,
                bytecode: ptr::null_mut(),
                error_message: ptr::null(),
            }
        }
        Err(error) => {
            FfiCompilationResult {
                success: false,
                bytecode: ptr::null_mut(),
                error_message: rust_string_to_ffi(&error),
            }
        }
    }
}

/// Free FFI compilation result
#[no_mangle]
pub extern "C" fn runa_free_compilation_result(result: FfiCompilationResult) {
    if !result.bytecode.is_null() {
        unsafe {
            let _ = Box::from_raw(result.bytecode);
        }
    }
    
    if !result.error_message.is_null() {
        unsafe {
            let _ = CString::from_raw(result.error_message as *mut c_char);
        }
    }
} 