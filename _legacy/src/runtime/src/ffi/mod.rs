//! Foreign Function Interface (FFI) Module
//!
//! This module contains all external interfaces for the Runa runtime:
//! - Runtime Interface: System calls for OS operations (files, processes, memory, etc.)
//! - Compiler Interface: Bridge between compiler and runtime for LIR->bytecode translation
//!
//! These are the only two legitimate FFI boundaries in the Runa runtime system.

pub mod runtime_interface;
pub mod compiler_interface;

// Re-export key types and functions for easy access
pub use runtime_interface::{
    // Core system calls
    system_call_file_open, system_call_file_read, system_call_file_write, system_call_file_close,
    system_call_file_create, system_call_file_delete,
    system_call_directory_create, system_call_directory_list,
    system_call_process_execute, system_call_process_exit,
    system_call_time_current, system_call_time_high_res,
    system_call_environment_get, system_call_environment_set,
    system_call_environment_list, system_call_environment_remove,
    system_call_memory_allocate, system_call_object_address,
    
    // Reflection system calls
    system_call_type_name, system_call_object_size, system_call_call_stack,
    system_call_function_name, system_call_module_name, system_call_source_location,
    
    // Cryptographic system calls
    system_call_random_bytes, system_call_crypto_hash, system_call_entropy_collect,
    
    // Runtime management
    runa_runtime_init, runa_runtime_shutdown,
    runa_get_runtime_functions, runa_runtime_version, runa_runtime_capabilities,
    
    // Memory management
    runa_free_string, runa_free_bytes, runa_free_string_array, runa_free_environment_arrays,
    
    // Core types
    RunaFileHandle, RunaProcessResult, RunaStackFrame, RunaSourceLocation, RunaBytes, RunaRuntimeFunction,
};

pub use compiler_interface::{
    // Compiler-runtime bridge
    runa_translate_lir_to_bytecode, runa_execute_bytecode, runa_free_compilation_result,
    
    // FFI structures for compiler communication
    FfiLirInstruction, FfiLirBasicBlock, FfiLirFunction, FfiLirModule,
    FfiGlobal, FfiConstant, FfiUpvalue, FfiCompilationResult,
};

/// Clean up all FFI resources
pub fn cleanup_ffi() {
    runtime_interface::cleanup_file_handles();
    runtime_interface::cleanup_memory_tracking();
    runtime_interface::cleanup_reflection_registries();
}