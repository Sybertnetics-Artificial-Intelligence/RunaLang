//! C-Compatible Export Interface for the 25 Essential Runa Runtime System Calls
//!
//! This module provides the final C-compatible FFI layer that exposes all 25 
//! essential system calls defined in the Runa runtime interface specification.
//!
//! These functions are designed to be called directly from Runa bytecode
//! via the virtual machine's FFI mechanism.
//!
//! Architecture Flow:
//! Runa Source → Runa Compiler → Bytecode → VM → These Functions → OS

// Re-export specific runtime interface functions to avoid conflicts
pub use crate::runtime_interface::{
    system_call_file_open, system_call_file_read, system_call_file_write, system_call_file_close,
    system_call_file_create, system_call_file_delete, system_call_directory_create, system_call_directory_list,
    system_call_process_execute, system_call_process_exit, system_call_time_current, system_call_time_high_res,
    system_call_environment_get, system_call_environment_set, system_call_memory_allocate, system_call_object_address,
    RunaProcessResult, RunaFileHandle, RunaBytes as InterfaceBytes
};

pub use crate::runtime_interface_reflection::{
    system_call_type_name, system_call_object_size, system_call_call_stack,
    system_call_function_name, system_call_module_name, system_call_source_location,
    RunaStackFrame as ReflectionStackFrame, RunaSourceLocation
};

pub use crate::runtime_interface_crypto::{
    system_call_random_bytes, system_call_crypto_hash, system_call_entropy_collect,
    RunaBytes as CryptoBytes, test_crypto_system
};

use std::ffi::{c_char, c_void, CString};

// ============================================================================
// COMPLETE RUNTIME INTERFACE EXPORT TABLE
// ============================================================================

/// Runtime function registry for dynamic linking
#[repr(C)]
pub struct RunaRuntimeFunction {
    pub name: *const c_char,
    pub function_ptr: *const c_void,
}

// Mark as Send + Sync for static usage
unsafe impl Send for RunaRuntimeFunction {}
unsafe impl Sync for RunaRuntimeFunction {}

/// Get the complete runtime function table
/// This allows the VM to dynamically link to runtime functions
#[no_mangle]
pub extern "C" fn runa_get_runtime_functions(count_out: *mut usize) -> *const RunaRuntimeFunction {
    static RUNTIME_FUNCTIONS: &[RunaRuntimeFunction] = &[
        // File System Operations (8 functions)
        RunaRuntimeFunction {
            name: b"system_call_file_open\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_open as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_file_read\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_read as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_file_write\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_write as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_file_close\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_close as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_file_create\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_create as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_file_delete\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_delete as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_directory_create\0".as_ptr() as *const c_char,
            function_ptr: system_call_directory_create as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_directory_list\0".as_ptr() as *const c_char,
            function_ptr: system_call_directory_list as *const c_void,
        },
        
        // Process & OS Operations (8 functions)
        RunaRuntimeFunction {
            name: b"system_call_process_execute\0".as_ptr() as *const c_char,
            function_ptr: system_call_process_execute as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_process_exit\0".as_ptr() as *const c_char,
            function_ptr: system_call_process_exit as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_time_current\0".as_ptr() as *const c_char,
            function_ptr: system_call_time_current as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_time_high_res\0".as_ptr() as *const c_char,
            function_ptr: system_call_time_high_res as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_environment_get\0".as_ptr() as *const c_char,
            function_ptr: system_call_environment_get as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_environment_set\0".as_ptr() as *const c_char,
            function_ptr: system_call_environment_set as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_memory_allocate\0".as_ptr() as *const c_char,
            function_ptr: system_call_memory_allocate as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_object_address\0".as_ptr() as *const c_char,
            function_ptr: system_call_object_address as *const c_void,
        },
        
        // Reflection Operations (6 functions)
        RunaRuntimeFunction {
            name: b"system_call_type_name\0".as_ptr() as *const c_char,
            function_ptr: system_call_type_name as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_object_size\0".as_ptr() as *const c_char,
            function_ptr: system_call_object_size as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_call_stack\0".as_ptr() as *const c_char,
            function_ptr: system_call_call_stack as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_function_name\0".as_ptr() as *const c_char,
            function_ptr: system_call_function_name as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_module_name\0".as_ptr() as *const c_char,
            function_ptr: system_call_module_name as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_source_location\0".as_ptr() as *const c_char,
            function_ptr: system_call_source_location as *const c_void,
        },
        
        // Cryptography Operations (3 functions)
        RunaRuntimeFunction {
            name: b"system_call_random_bytes\0".as_ptr() as *const c_char,
            function_ptr: system_call_random_bytes as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_crypto_hash\0".as_ptr() as *const c_char,
            function_ptr: system_call_crypto_hash as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_entropy_collect\0".as_ptr() as *const c_char,
            function_ptr: system_call_entropy_collect as *const c_void,
        },
    ];
    
    if !count_out.is_null() {
        unsafe {
            *count_out = RUNTIME_FUNCTIONS.len();
        }
    }
    
    RUNTIME_FUNCTIONS.as_ptr()
}

// ============================================================================
// RUNTIME INITIALIZATION AND VALIDATION
// ============================================================================

/// Initialize the Runa runtime system
/// Must be called before any other runtime functions
#[no_mangle]
pub extern "C" fn runa_runtime_init() -> bool {
    // Initialize any global state needed by the runtime
    // This is a good place to set up logging, security contexts, etc.
    
    // Test that all critical systems are working
    let test_results = [
        test_file_system(),
        test_process_system(),
        test_memory_system(),
        test_reflection_system(),
        test_crypto_system(),
    ];
    
    // Return true only if all systems pass their tests
    test_results.iter().all(|&result| result)
}

/// Shutdown the Runa runtime system
/// Should be called when the program exits
#[no_mangle]
pub extern "C" fn runa_runtime_shutdown() {
    // Clean up any global state
    // This is important for proper resource cleanup
    
    // Note: In a full implementation, this would:
    // - Close any remaining file handles
    // - Clean up thread pools
    // - Free any cached data
    // - Flush any pending I/O operations
}

/// Get runtime version information
#[no_mangle]
pub extern "C" fn runa_runtime_version() -> *const c_char {
    b"Runa Runtime v1.0.0 - 25 Essential System Calls\0".as_ptr() as *const c_char
}

/// Get runtime capabilities flags
#[no_mangle]
pub extern "C" fn runa_runtime_capabilities() -> u64 {
    const FILE_SYSTEM_SUPPORT: u64 = 1 << 0;
    const PROCESS_SUPPORT: u64 = 1 << 1;
    const MEMORY_SUPPORT: u64 = 1 << 2;
    const REFLECTION_SUPPORT: u64 = 1 << 3;
    const CRYPTO_SUPPORT: u64 = 1 << 4;
    const CROSS_PLATFORM: u64 = 1 << 5;
    const THREAD_SAFE: u64 = 1 << 6;
    
    FILE_SYSTEM_SUPPORT 
        | PROCESS_SUPPORT 
        | MEMORY_SUPPORT 
        | REFLECTION_SUPPORT 
        | CRYPTO_SUPPORT 
        | CROSS_PLATFORM 
        | THREAD_SAFE
}

// ============================================================================
// SYSTEM VALIDATION FUNCTIONS
// ============================================================================

fn test_file_system() -> bool {
    // Test basic file operations
    use std::ffi::CString;
    
    let test_path = CString::new("/tmp/runa_test_file").unwrap();
    let write_mode = CString::new("w").unwrap();
    
    let handle = system_call_file_open(test_path.as_ptr(), write_mode.as_ptr());
    if handle < 0 {
        return false;
    }
    
    let test_data = b"test";
    let write_success = system_call_file_write(
        handle, 
        0, 
        test_data.as_ptr(), 
        test_data.len()
    );
    
    let close_success = system_call_file_close(handle);
    
    // Clean up
    let _ = system_call_file_delete(test_path.as_ptr());
    
    write_success && close_success
}

fn test_process_system() -> bool {
    // Test basic process operations
    use std::ffi::CString;
    
    let command = CString::new("echo").unwrap();
    let arg = CString::new("test").unwrap();
    let args = [arg.as_ptr()];
    
    let result = system_call_process_execute(
        command.as_ptr(),
        args.as_ptr(),
        1,
        std::ptr::null(),
        0,
    );
    
    // Clean up allocated strings
    if !result.stdout.is_null() {
        unsafe { let _ = CString::from_raw(result.stdout); }
    }
    if !result.stderr.is_null() {
        unsafe { let _ = CString::from_raw(result.stderr); }
    }
    
    result.success
}

fn test_memory_system() -> bool {
    // Test memory allocation
    let addr = system_call_memory_allocate(1024);
    if addr == 0 {
        return false;
    }
    
    // Test object address
    let test_obj = 42u64;
    let obj_addr = system_call_object_address(&test_obj as *const u64 as *const c_void);
    
    obj_addr != 0
}

fn test_reflection_system() -> bool {
    // Test reflection operations
    let test_obj = "test";
    let type_name_ptr = system_call_type_name(test_obj.as_ptr() as *const c_void);
    
    if type_name_ptr.is_null() {
        return false;
    }
    
    // Clean up
    unsafe { let _ = CString::from_raw(type_name_ptr); }
    
    let size = system_call_object_size(test_obj.as_ptr() as *const c_void);
    size > 0
}

// Note: test_crypto_system() is implemented in runtime_interface_crypto.rs

// ============================================================================
// DOCUMENTATION AND DEBUGGING
// ============================================================================

/// Get human-readable documentation for the runtime interface
#[no_mangle]
pub extern "C" fn runa_runtime_docs() -> *const c_char {
    b"Runa Runtime Interface Documentation\n\
    \n\
    This runtime provides 25 essential system calls organized into 4 categories:\n\
    \n\
    FILE SYSTEM (8 functions):\n\
    - system_call_file_open/read/write/close\n\
    - system_call_file_create/delete\n\
    - system_call_directory_create/list\n\
    \n\
    PROCESS & OS (8 functions):\n\
    - system_call_process_execute/exit\n\
    - system_call_time_current/high_res\n\
    - system_call_environment_get/set\n\
    - system_call_memory_allocate\n\
    - system_call_object_address\n\
    \n\
    REFLECTION (6 functions):\n\
    - system_call_type_name/object_size\n\
    - system_call_call_stack\n\
    - system_call_function_name/module_name\n\
    - system_call_source_location\n\
    \n\
    CRYPTOGRAPHY (3 functions):\n\
    - system_call_random_bytes\n\
    - system_call_crypto_hash\n\
    - system_call_entropy_collect\n\
    \n\
    All functions are thread-safe and cross-platform.\0"
        .as_ptr() as *const c_char
}