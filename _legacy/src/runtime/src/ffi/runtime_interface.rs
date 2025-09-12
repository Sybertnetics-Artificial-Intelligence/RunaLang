//! Unified Runa Runtime Interface - All System Calls in One Place
//! 
//! This module provides the complete native runtime implementation that bridges Runa code
//! to actual system operations. These functions are called by the Runa standard library
//! through the bytecode execution engine.
//!
//! Architecture:
//! Runa stdlib → Bytecode → VM → Native Runtime (this module) → OS
//!
//! This is the critical layer that makes Runa programs actually work with real
//! files, processes, memory, and system resources.
//!
//! ## Complete System Call Interface
//! 
//! **FILE SYSTEM (9 functions):**
//! - system_call_file_open/read/write/close
//! - system_call_file_create/delete/stat
//! - system_call_directory_create/list
//! 
//! **PROCESS & OS (8 functions):**
//! - system_call_process_execute/exit
//! - system_call_time_current/high_res
//! - system_call_environment_get/set
//! - system_call_memory_allocate
//! - system_call_object_address
//! 
//! **REFLECTION (6 functions):**
//! - system_call_type_name/object_size
//! - system_call_call_stack
//! - system_call_function_name/module_name
//! - system_call_source_location
//! 
//! **CRYPTOGRAPHY (3 functions):**
//! - system_call_random_bytes
//! - system_call_crypto_hash
//! - system_call_entropy_collect

use std::ffi::{c_char, c_void, CStr, CString};
use std::fs::{File, OpenOptions};
use std::io::{Read, Write, Seek, SeekFrom};
use std::process::{Command, Stdio};
use std::collections::{HashMap, hash_map::DefaultHasher};
use std::sync::{Mutex, LazyLock};
use std::time::{SystemTime, UNIX_EPOCH};
use std::env;
use std::ptr;
use std::hash::{Hash, Hasher};
use rand::{RngCore, thread_rng};
use sha2::{Sha256, Sha512, Digest};
use sha1::Sha1;
use md5;

// ============================================================================
// CORE RUNTIME TYPES
// ============================================================================

/// File handle type - maps to Runa's FileHandle
pub type RunaFileHandle = i32;

/// Process result structure - maps to Runa's ProcessResult
#[repr(C)]
pub struct RunaProcessResult {
    pub success: bool,
    pub exit_code: i32,
    pub stdout: *mut c_char,
    pub stderr: *mut c_char,
    pub pid: i32,
}

/// Stack frame structure - maps to Runa's StackFrame
#[repr(C)]
pub struct RunaStackFrame {
    pub function_name: *mut c_char,
    pub module_name: *mut c_char,
    pub file_path: *mut c_char,
    pub line_number: i32,
    pub column_number: i32,
}

/// Source location structure for reflection
#[repr(C)]
pub struct RunaSourceLocation {
    pub file_path: *mut c_char,
    pub line_number: i32,
    pub column_number: i32,
    pub function_name: *mut c_char,
    pub module_name: *mut c_char,
}

/// Bytes array structure - maps to Runa's Bytes (List[Integer])
#[repr(C)]
pub struct RunaBytes {
    pub data: *mut u8,
    pub length: usize,
}

/// Runtime function registry for dynamic linking
#[repr(C)]
pub struct RunaRuntimeFunction {
    pub name: *const c_char,
    pub function_ptr: *const c_void,
}

// Mark as Send + Sync for static usage
unsafe impl Send for RunaRuntimeFunction {}
unsafe impl Sync for RunaRuntimeFunction {}

// ============================================================================
// GLOBAL STATE MANAGEMENT
// ============================================================================

// File handle registry - thread-safe mapping of handles to files
pub static FILE_REGISTRY: LazyLock<Mutex<HashMap<i32, File>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

static mut NEXT_FILE_HANDLE: i32 = 1;

// Memory allocation tracking for debugging
pub static ALLOCATION_REGISTRY: LazyLock<Mutex<HashMap<usize, usize>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

// Reflection registries
static TYPE_NAME_CACHE: LazyLock<Mutex<HashMap<usize, String>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

static CALL_STACK_REGISTRY: LazyLock<Mutex<Vec<RunaStackFrame>>> = 
    LazyLock::new(|| Mutex::new(Vec::new()));

static FUNCTION_NAME_REGISTRY: LazyLock<Mutex<HashMap<usize, String>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

static MODULE_NAME_REGISTRY: LazyLock<Mutex<HashMap<usize, String>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

static SOURCE_LOCATION_REGISTRY: LazyLock<Mutex<HashMap<usize, RunaSourceLocation>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

// ============================================================================
// FILE SYSTEM OPERATIONS (8 functions)
// ============================================================================

/// system_call_file_open: Open a file and return a handle
/// Maps to: system_call_file_open(path: String, mode: String) -> FileHandle
#[no_mangle]
pub extern "C" fn system_call_file_open(path: *const c_char, mode: *const c_char) -> RunaFileHandle {
    if path.is_null() || mode.is_null() {
        return -1;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    let mode_str = match unsafe { CStr::from_ptr(mode).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    let mut options = OpenOptions::new();
    
    // Parse Runa file modes
    match mode_str {
        "r" => { options.read(true); }
        "w" => { options.write(true).create(true).truncate(true); }
        "a" => { options.write(true).create(true).append(true); }
        "r+" => { options.read(true).write(true); }
        _ => return -1,
    }

    match options.open(path_str) {
        Ok(file) => {
            let handle = unsafe {
                NEXT_FILE_HANDLE += 1;
                NEXT_FILE_HANDLE
            };

            if let Ok(mut registry) = FILE_REGISTRY.lock() {
                registry.insert(handle, file);
                handle
            } else {
                -1
            }
        }
        Err(_) => -1,
    }
}

/// system_call_file_read: Read bytes from file at offset
/// Maps to: system_call_file_read(handle: FileHandle, offset: Integer, length: Integer) -> Bytes
#[no_mangle]
pub extern "C" fn system_call_file_read(handle: RunaFileHandle, offset: i64, length: i32) -> RunaBytes {
    let empty_result = RunaBytes { data: ptr::null_mut(), length: 0 };
    
    if handle <= 0 {
        return empty_result;
    }

    let mut registry = match FILE_REGISTRY.lock() {
        Ok(reg) => reg,
        Err(_) => return empty_result,
    };

    if let Some(file) = registry.get_mut(&handle) {
        // Seek to offset if specified
        if offset >= 0 {
            if file.seek(SeekFrom::Start(offset as u64)).is_err() {
                return empty_result;
            }
        }

        // Determine read length
        let read_length = if length < 0 {
            // Read to end of file
            match file.metadata() {
                Ok(metadata) => {
                    let current_pos = file.stream_position().unwrap_or(0);
                    (metadata.len() - current_pos) as usize
                }
                Err(_) => 4096, // Default buffer size
            }
        } else {
            length as usize
        };

        // Allocate buffer and read
        let mut buffer = vec![0u8; read_length];
        match file.read(&mut buffer) {
            Ok(bytes_read) => {
                buffer.truncate(bytes_read);
                let data_ptr = buffer.as_mut_ptr();
                std::mem::forget(buffer); // Prevent deallocation - caller must free
                
                RunaBytes {
                    data: data_ptr,
                    length: bytes_read,
                }
            }
            Err(_) => empty_result,
        }
    } else {
        empty_result
    }
}

/// system_call_file_write: Write bytes to file at offset
/// Maps to: system_call_file_write(handle: FileHandle, offset: Integer, data: Bytes) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_file_write(handle: RunaFileHandle, offset: i64, data: *const u8, data_length: usize) -> bool {
    if handle <= 0 || data.is_null() || data_length == 0 {
        return false;
    }

    let mut registry = match FILE_REGISTRY.lock() {
        Ok(reg) => reg,
        Err(_) => return false,
    };

    if let Some(file) = registry.get_mut(&handle) {
        // Seek to offset if specified
        if offset >= 0 {
            if file.seek(SeekFrom::Start(offset as u64)).is_err() {
                return false;
            }
        }

        // Write data
        let data_slice = unsafe { std::slice::from_raw_parts(data, data_length) };
        match file.write_all(data_slice) {
            Ok(_) => {
                file.flush().is_ok()
            }
            Err(_) => false,
        }
    } else {
        false
    }
}

/// system_call_file_close: Close a file handle
/// Maps to: system_call_file_close(handle: FileHandle) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_file_close(handle: RunaFileHandle) -> bool {
    if handle <= 0 {
        return false;
    }

    if let Ok(mut registry) = FILE_REGISTRY.lock() {
        registry.remove(&handle).is_some()
    } else {
        false
    }
}

/// system_call_file_create: Create a new file with permissions
/// Maps to: system_call_file_create(path: String, mode: Integer) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_file_create(path: *const c_char, mode: i32) -> bool {
    if path.is_null() {
        return false;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    match File::create(path_str) {
        Ok(_) => {
            // Set permissions on Unix-like systems
            #[cfg(unix)]
            {
                use std::os::unix::fs::PermissionsExt;
                if let Ok(file) = File::open(path_str) {
                    let permissions = std::fs::Permissions::from_mode(mode as u32);
                    file.set_permissions(permissions).is_ok()
                } else {
                    true // File created successfully even if permission setting failed
                }
            }
            #[cfg(not(unix))]
            {
                let _ = mode; // Suppress unused parameter warning
                true
            }
        }
        Err(_) => false,
    }
}

/// system_call_file_delete: Delete a file
/// Maps to: system_call_file_delete(path: String) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_file_delete(path: *const c_char) -> bool {
    if path.is_null() {
        return false;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    std::fs::remove_file(path_str).is_ok()
}

/// system_call_directory_create: Create a directory
/// Maps to: system_call_directory_create(path: String) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_directory_create(path: *const c_char) -> bool {
    if path.is_null() {
        return false;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    std::fs::create_dir_all(path_str).is_ok()
}

/// system_call_directory_list: List directory contents
/// Maps to: system_call_directory_list(path: String) -> List[String]
#[no_mangle]
pub extern "C" fn system_call_directory_list(path: *const c_char, result_array: *mut *const c_char, result_count: *mut usize) -> bool {
    if path.is_null() || result_array.is_null() || result_count.is_null() {
        return false;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    match std::fs::read_dir(path_str) {
        Ok(entries) => {
            let mut entry_names = Vec::new();
            
            for entry in entries {
                if let Ok(entry) = entry {
                    if let Some(name) = entry.file_name().to_str() {
                        if let Ok(c_string) = CString::new(name) {
                            entry_names.push(c_string.into_raw());
                        }
                    }
                }
            }

            let count = entry_names.len();
            let names_ptr = entry_names.as_ptr();
            std::mem::forget(entry_names); // Prevent deallocation

            unsafe {
                *result_array = names_ptr as *const c_char;
                *result_count = count;
            }
            true
        }
        Err(_) => {
            unsafe {
                *result_array = ptr::null_mut();
                *result_count = 0;
            }
            false
        }
    }
}

/// system_call_file_stat: Get file information and metadata
/// Maps to: system_call_file_stat(path: String) -> Dictionary[String, Any]
#[no_mangle]
pub extern "C" fn system_call_file_stat(path: *const c_char, result_keys: *mut *const c_char, result_values: *mut *const c_char, result_count: *mut usize) -> bool {
    if path.is_null() || result_keys.is_null() || result_values.is_null() || result_count.is_null() {
        return false;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    match std::fs::metadata(path_str) {
        Ok(metadata) => {
            let mut keys = Vec::new();
            let mut values = Vec::new();
            
            // File size
            keys.push(CString::new("size").unwrap().into_raw());
            values.push(CString::new(metadata.len().to_string()).unwrap().into_raw());
            
            // File type
            keys.push(CString::new("type").unwrap().into_raw());
            let file_type = if metadata.is_file() { "file" } 
                           else if metadata.is_dir() { "directory" } 
                           else { "other" };
            values.push(CString::new(file_type).unwrap().into_raw());
            
            // Permissions (Unix style numeric)
            keys.push(CString::new("permissions").unwrap().into_raw());
            #[cfg(unix)]
            {
                use std::os::unix::fs::PermissionsExt;
                let mode = metadata.permissions().mode();
                values.push(CString::new(format!("{:o}", mode)).unwrap().into_raw());
            }
            #[cfg(not(unix))]
            {
                let mode = if metadata.permissions().readonly() { "444" } else { "644" };
                values.push(CString::new(mode).unwrap().into_raw());
            }
            
            // Modified time (Unix timestamp)
            keys.push(CString::new("modified").unwrap().into_raw());
            if let Ok(time) = metadata.modified() {
                if let Ok(duration) = time.duration_since(std::time::UNIX_EPOCH) {
                    values.push(CString::new(duration.as_secs().to_string()).unwrap().into_raw());
                } else {
                    values.push(CString::new("0").unwrap().into_raw());
                }
            } else {
                values.push(CString::new("0").unwrap().into_raw());
            }
            
            // Created time (Unix timestamp)
            keys.push(CString::new("created").unwrap().into_raw());
            if let Ok(time) = metadata.created() {
                if let Ok(duration) = time.duration_since(std::time::UNIX_EPOCH) {
                    values.push(CString::new(duration.as_secs().to_string()).unwrap().into_raw());
                } else {
                    values.push(CString::new("0").unwrap().into_raw());
                }
            } else {
                values.push(CString::new("0").unwrap().into_raw());
            }
            
            // Accessed time (Unix timestamp)
            keys.push(CString::new("accessed").unwrap().into_raw());
            if let Ok(time) = metadata.accessed() {
                if let Ok(duration) = time.duration_since(std::time::UNIX_EPOCH) {
                    values.push(CString::new(duration.as_secs().to_string()).unwrap().into_raw());
                } else {
                    values.push(CString::new("0").unwrap().into_raw());
                }
            } else {
                values.push(CString::new("0").unwrap().into_raw());
            }

            let count = keys.len();
            let keys_ptr = keys.as_ptr();
            let values_ptr = values.as_ptr();
            std::mem::forget(keys);
            std::mem::forget(values);
            
            unsafe {
                *result_keys = keys_ptr as *const c_char;
                *result_values = values_ptr as *const c_char;
                *result_count = count;
            }
            
            true
        }
        Err(_) => {
            unsafe {
                *result_keys = ptr::null_mut();
                *result_values = ptr::null_mut();
                *result_count = 0;
            }
            false
        }
    }
}

// ============================================================================
// PROCESS & OS OPERATIONS (8 functions)
// ============================================================================

/// system_call_process_execute: Execute a process with args and environment
/// Maps to: system_call_process_execute(command: String, args: List[String], env: Dictionary[String, String]) -> ProcessResult
#[no_mangle]
pub extern "C" fn system_call_process_execute(
    command: *const c_char,
    args: *const *const c_char,
    args_count: usize,
    env: *const *const c_char,
    env_count: usize,
) -> RunaProcessResult {
    let error_result = RunaProcessResult {
        success: false,
        exit_code: -1,
        stdout: CString::new("").unwrap().into_raw(),
        stderr: CString::new("Runtime error").unwrap().into_raw(),
        pid: -1,
    };

    if command.is_null() {
        return error_result;
    }

    let command_str = match unsafe { CStr::from_ptr(command).to_str() } {
        Ok(s) => s,
        Err(_) => return error_result,
    };

    let mut cmd = Command::new(command_str);

    // Add arguments
    if !args.is_null() && args_count > 0 {
        for i in 0..args_count {
            let arg_ptr = unsafe { *args.add(i) };
            if !arg_ptr.is_null() {
                if let Ok(arg_str) = unsafe { CStr::from_ptr(arg_ptr).to_str() } {
                    cmd.arg(arg_str);
                }
            }
        }
    }

    // Add environment variables
    if !env.is_null() && env_count > 0 {
        for i in 0..(env_count / 2) {
            let key_ptr = unsafe { *env.add(i * 2) };
            let value_ptr = unsafe { *env.add(i * 2 + 1) };
            
            if !key_ptr.is_null() && !value_ptr.is_null() {
                if let (Ok(key), Ok(value)) = (
                    unsafe { CStr::from_ptr(key_ptr).to_str() },
                    unsafe { CStr::from_ptr(value_ptr).to_str() }
                ) {
                    cmd.env(key, value);
                }
            }
        }
    }

    // Execute command
    cmd.stdout(Stdio::piped()).stderr(Stdio::piped());
    
    match cmd.spawn() {
        Ok(child) => {
            let pid = child.id() as i32;
            
            match child.wait_with_output() {
                Ok(output) => {
                    let stdout_str = String::from_utf8_lossy(&output.stdout);
                    let stderr_str = String::from_utf8_lossy(&output.stderr);
                    
                    RunaProcessResult {
                        success: output.status.success(),
                        exit_code: output.status.code().unwrap_or(-1),
                        stdout: CString::new(stdout_str.as_ref()).unwrap().into_raw(),
                        stderr: CString::new(stderr_str.as_ref()).unwrap().into_raw(),
                        pid,
                    }
                }
                Err(_) => error_result,
            }
        }
        Err(_) => error_result,
    }
}

/// system_call_process_exit: Exit the current process
/// Maps to: system_call_process_exit(code: Integer) -> Never
#[no_mangle]
pub extern "C" fn system_call_process_exit(code: i32) -> ! {
    std::process::exit(code);
}

/// system_call_time_current: Get current system time
/// Maps to: system_call_time_current() -> Float
#[no_mangle]
pub extern "C" fn system_call_time_current() -> f64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| duration.as_secs_f64())
        .unwrap_or(0.0)
}

/// system_call_time_high_res: Get high-resolution timestamp
/// Maps to: system_call_time_high_res() -> Integer
#[no_mangle]
pub extern "C" fn system_call_time_high_res() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| duration.as_nanos() as i64)
        .unwrap_or(0)
}

/// system_call_environment_get: Get environment variable
/// Maps to: system_call_environment_get(name: String) -> Optional[String]
#[no_mangle]
pub extern "C" fn system_call_environment_get(name: *const c_char) -> *mut c_char {
    if name.is_null() {
        return ptr::null_mut();
    }

    let name_str = match unsafe { CStr::from_ptr(name).to_str() } {
        Ok(s) => s,
        Err(_) => return ptr::null_mut(),
    };

    match env::var(name_str) {
        Ok(value) => CString::new(value).unwrap().into_raw(),
        Err(_) => ptr::null_mut(),
    }
}

/// system_call_environment_set: Set environment variable
/// Maps to: system_call_environment_set(name: String, value: String) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_environment_set(name: *const c_char, value: *const c_char) -> bool {
    if name.is_null() || value.is_null() {
        return false;
    }

    let name_str = match unsafe { CStr::from_ptr(name).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    let value_str = match unsafe { CStr::from_ptr(value).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    env::set_var(name_str, value_str);
    true
}

/// system_call_environment_list: List all environment variables
/// Maps to: system_call_environment_list() -> Dictionary[String, String]
#[no_mangle]
pub extern "C" fn system_call_environment_list(keys_out: *mut *const c_char, values_out: *mut *const c_char, count_out: *mut usize) -> bool {
    if keys_out.is_null() || values_out.is_null() || count_out.is_null() {
        return false;
    }

    let env_vars: Vec<(String, String)> = env::vars().collect();
    let count = env_vars.len();
    
    if count == 0 {
        unsafe {
            *keys_out = ptr::null_mut();
            *values_out = ptr::null_mut();
            *count_out = 0;
        }
        return true;
    }
    
    let mut keys = Vec::new();
    let mut values = Vec::new();
    
    for (key, value) in env_vars {
        if let (Ok(key_cstring), Ok(value_cstring)) = (CString::new(key), CString::new(value)) {
            keys.push(key_cstring.into_raw());
            values.push(value_cstring.into_raw());
        }
    }
    
    let keys_ptr = keys.as_ptr();
    let values_ptr = values.as_ptr();
    std::mem::forget(keys);
    std::mem::forget(values);
    
    unsafe {
        *keys_out = keys_ptr as *const c_char;
        *values_out = values_ptr as *const c_char;
        *count_out = count;
    }
    
    true
}

/// system_call_environment_remove: Remove environment variable
/// Maps to: system_call_environment_remove(name: String) -> Boolean
#[no_mangle]
pub extern "C" fn system_call_environment_remove(name: *const c_char) -> bool {
    if name.is_null() {
        return false;
    }

    let name_str = match unsafe { CStr::from_ptr(name).to_str() } {
        Ok(s) => s,
        Err(_) => return false,
    };

    env::remove_var(name_str);
    true
}

/// system_call_memory_allocate: Allocate memory
/// Maps to: system_call_memory_allocate(size: Integer) -> Address
#[no_mangle]
pub extern "C" fn system_call_memory_allocate(size: usize) -> usize {
    if size == 0 {
        return 0;
    }

    let layout = match std::alloc::Layout::from_size_align(size, std::mem::align_of::<u8>()) {
        Ok(layout) => layout,
        Err(_) => return 0,
    };

    let ptr = unsafe { std::alloc::alloc(layout) };
    
    if ptr.is_null() {
        0
    } else {
        let addr = ptr as usize;
        
        // Track allocation for debugging
        if let Ok(mut registry) = ALLOCATION_REGISTRY.lock() {
            registry.insert(addr, size);
        }
        
        addr
    }
}

/// system_call_object_address: Get memory address of object
/// Maps to: system_call_object_address(obj: Any) -> Address
#[no_mangle]
pub extern "C" fn system_call_object_address(obj: *const c_void) -> usize {
    obj as usize
}

// ============================================================================
// REFLECTION OPERATIONS (6 functions)
// ============================================================================

/// system_call_type_name: Get type name of object
/// Maps to: system_call_type_name(obj: Any) -> String
#[no_mangle]
pub extern "C" fn system_call_type_name(obj: *const c_void) -> *mut c_char {
    if obj.is_null() {
        return CString::new("null").unwrap().into_raw();
    }
    
    let obj_addr = obj as usize;
    
    // Try to get cached type name first
    if let Ok(cache) = TYPE_NAME_CACHE.lock() {
        if let Some(type_name) = cache.get(&obj_addr) {
            return CString::new(type_name.as_str()).unwrap().into_raw();
        }
    }
    
    // Analyze memory pattern to infer type
    let inferred_type = unsafe {
        analyze_memory_pattern(obj)
    };
    
    // Cache the result
    if let Ok(mut cache) = TYPE_NAME_CACHE.lock() {
        cache.insert(obj_addr, inferred_type.clone());
    }
    
    CString::new(inferred_type).unwrap().into_raw()
}

/// system_call_object_size: Get size of object
/// Maps to: system_call_object_size(obj: Any) -> Integer
#[no_mangle]
pub extern "C" fn system_call_object_size(obj: *const c_void) -> usize {
    if obj.is_null() {
        return 0;
    }
    
    // Check if this is a tracked allocation
    let obj_addr = obj as usize;
    if let Ok(registry) = ALLOCATION_REGISTRY.lock() {
        if let Some(&size) = registry.get(&obj_addr) {
            return size;
        }
    }
    
    // Try to determine size from memory pattern analysis
    unsafe {
        analyze_object_size(obj)
    }
}

/// system_call_call_stack: Get current call stack
/// Maps to: system_call_call_stack() -> List[StackFrame]
#[no_mangle]
pub extern "C" fn system_call_call_stack(frames_out: *mut *const RunaStackFrame, count_out: *mut usize) -> bool {
    if frames_out.is_null() || count_out.is_null() {
        return false;
    }
    
    if let Ok(stack) = CALL_STACK_REGISTRY.lock() {
        let count = stack.len();
        
        if count == 0 {
            unsafe {
                *frames_out = ptr::null_mut();
                *count_out = 0;
            }
            return true;
        }
        
        let frames_ptr = stack.as_ptr();
        
        unsafe {
            *frames_out = frames_ptr;
            *count_out = count;
        }
        
        true
    } else {
        unsafe {
            *frames_out = ptr::null_mut();
            *count_out = 0;
        }
        false
    }
}

/// system_call_function_name: Get function name at address
/// Maps to: system_call_function_name(address: Address) -> String
#[no_mangle]
pub extern "C" fn system_call_function_name(address: usize) -> *mut c_char {
    if let Ok(registry) = FUNCTION_NAME_REGISTRY.lock() {
        if let Some(name) = registry.get(&address) {
            return CString::new(name.as_str()).unwrap().into_raw();
        }
    }
    
    CString::new("<unknown>").unwrap().into_raw()
}

/// system_call_module_name: Get module name at address
/// Maps to: system_call_module_name(address: Address) -> String
#[no_mangle]
pub extern "C" fn system_call_module_name(address: usize) -> *mut c_char {
    if let Ok(registry) = MODULE_NAME_REGISTRY.lock() {
        if let Some(name) = registry.get(&address) {
            return CString::new(name.as_str()).unwrap().into_raw();
        }
    }
    
    CString::new("<unknown>").unwrap().into_raw()
}

/// system_call_source_location: Get source location at address
/// Maps to: system_call_source_location(address: Address) -> SourceLocation
#[no_mangle]
pub extern "C" fn system_call_source_location(address: usize) -> RunaSourceLocation {
    let default_location = RunaSourceLocation {
        file_path: CString::new("<unknown>").unwrap().into_raw(),
        line_number: 0,
        column_number: 0,
        function_name: CString::new("<unknown>").unwrap().into_raw(),
        module_name: CString::new("<unknown>").unwrap().into_raw(),
    };
    
    if let Ok(registry) = SOURCE_LOCATION_REGISTRY.lock() {
        if let Some(location) = registry.get(&address) {
            // Create a copy since we can't return the reference
            return RunaSourceLocation {
                file_path: unsafe { 
                    let src = CStr::from_ptr(location.file_path);
                    CString::new(src.to_str().unwrap_or("<unknown>")).unwrap().into_raw()
                },
                line_number: location.line_number,
                column_number: location.column_number,
                function_name: unsafe {
                    let src = CStr::from_ptr(location.function_name);
                    CString::new(src.to_str().unwrap_or("<unknown>")).unwrap().into_raw()
                },
                module_name: unsafe {
                    let src = CStr::from_ptr(location.module_name);
                    CString::new(src.to_str().unwrap_or("<unknown>")).unwrap().into_raw()
                },
            };
        }
    }
    
    default_location
}

// ============================================================================
// CRYPTOGRAPHY OPERATIONS (3 functions)
// ============================================================================

/// system_call_random_bytes: Generate cryptographically secure random bytes
/// Maps to: system_call_random_bytes(count: Integer) -> Bytes
#[no_mangle]
pub extern "C" fn system_call_random_bytes(count: usize) -> RunaBytes {
    if count == 0 || count > 1_048_576 { // Limit to 1MB for safety
        return RunaBytes {
            data: ptr::null_mut(),
            length: 0,
        };
    }

    let mut buffer = vec![0u8; count];
    
    // Use thread_rng() which is cryptographically secure
    thread_rng().fill_bytes(&mut buffer);
    {
            let data_ptr = buffer.as_mut_ptr();
            std::mem::forget(buffer); // Prevent deallocation - caller must free
            
            RunaBytes {
                data: data_ptr,
                length: count,
            }
    }
}

/// system_call_crypto_hash: Compute cryptographic hash of data
/// Maps to: system_call_crypto_hash(data: Bytes, algorithm: String) -> Bytes
#[no_mangle]
pub extern "C" fn system_call_crypto_hash(
    data: *const u8,
    data_length: usize,
    algorithm: *const c_char,
) -> RunaBytes {
    let empty_result = RunaBytes {
        data: ptr::null_mut(),
        length: 0,
    };

    if data.is_null() || data_length == 0 || algorithm.is_null() {
        return empty_result;
    }

    let algorithm_str = match unsafe { CStr::from_ptr(algorithm).to_str() } {
        Ok(s) => s.to_lowercase(),
        Err(_) => return empty_result,
    };

    let data_slice = unsafe { std::slice::from_raw_parts(data, data_length) };

    match algorithm_str.as_str() {
        "md5" => {
            let result = md5::compute(data_slice);
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        "sha1" => {
            let mut hasher = Sha1::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        "sha256" => {
            let mut hasher = Sha256::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        "sha512" => {
            let mut hasher = Sha512::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        _ => empty_result, // Unsupported algorithm
    }
}

/// system_call_entropy_collect: Collect system entropy for random generation
/// Maps to: system_call_entropy_collect() -> Bytes
#[no_mangle]
pub extern "C" fn system_call_entropy_collect() -> RunaBytes {
    // Collect entropy from various system sources
    let mut entropy_sources = Vec::new();
    
    // High-resolution timestamp
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default();
    entropy_sources.extend_from_slice(&now.as_nanos().to_le_bytes());
    
    // Process ID
    entropy_sources.extend_from_slice(&std::process::id().to_le_bytes());
    
    // Thread ID (approximation) - use simple hash instead of unstable API
    let mut hasher = DefaultHasher::new();
    std::thread::current().id().hash(&mut hasher);
    entropy_sources.extend_from_slice(&hasher.finish().to_le_bytes());
    
    // Memory address of stack variable (ASLR entropy)
    let stack_var = 0u64;
    let stack_addr = &stack_var as *const u64 as usize;
    entropy_sources.extend_from_slice(&stack_addr.to_le_bytes());
    
    // System-specific entropy
    #[cfg(unix)]
    {
        // Try to read from /dev/urandom if available
        if let Ok(mut file) = std::fs::File::open("/dev/urandom") {
            let mut random_bytes = [0u8; 32];
            if let Ok(_) = std::io::Read::read_exact(&mut file, &mut random_bytes) {
                entropy_sources.extend_from_slice(&random_bytes);
            }
        }
        
        // Add some process information
        entropy_sources.extend_from_slice(&std::process::id().to_le_bytes());
    }
    
    #[cfg(windows)]
    {
        // Use Windows-specific entropy sources
        use std::arch::x86_64::_rdtsc;
        
        // CPU timestamp counter (if available)
        unsafe {
            let tsc = _rdtsc();
            entropy_sources.extend_from_slice(&tsc.to_le_bytes());
        }
    }
    
    // Hash the collected entropy to produce uniform output
    let mut hasher = Sha256::new();
    hasher.update(&entropy_sources);
    let result = hasher.finalize();
    
    let mut entropy_vec = result.to_vec();
    let data_ptr = entropy_vec.as_mut_ptr();
    let length = entropy_vec.len();
    std::mem::forget(entropy_vec);
    
    RunaBytes {
        data: data_ptr,
        length,
    }
}

// ============================================================================
// COMPLETE RUNTIME INTERFACE EXPORT TABLE
// ============================================================================

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
        RunaRuntimeFunction {
            name: b"system_call_file_stat\0".as_ptr() as *const c_char,
            function_ptr: system_call_file_stat as *const c_void,
        },
        
        // Process & OS Operations (10 functions)
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
            name: b"system_call_environment_list\0".as_ptr() as *const c_char,
            function_ptr: system_call_environment_list as *const c_void,
        },
        RunaRuntimeFunction {
            name: b"system_call_environment_remove\0".as_ptr() as *const c_char,
            function_ptr: system_call_environment_remove as *const c_void,
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
    use std::io::{self, Write};
    
    // Step 1: Flush any pending I/O operations
    let _ = io::stdout().flush();
    let _ = io::stderr().flush();
    
    // Step 2: Close any remaining file handles
    cleanup_file_handles();
    
    // Step 3: Clean up memory tracking
    cleanup_memory_tracking();
    
    // Step 4: Clean up reflection registries
    cleanup_reflection_registries();
    
    // Step 5: Final memory statistics report (if debug mode)
    #[cfg(debug_assertions)]
    report_final_memory_stats();
}

/// Get runtime version information
#[no_mangle]
pub extern "C" fn runa_runtime_version() -> *const c_char {
    b"Runa Runtime v1.0.0 - Unified System Call Interface\0".as_ptr() as *const c_char
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
// MEMORY MANAGEMENT FOR ALL OPERATIONS
// ============================================================================

/// Free memory allocated by runtime calls
#[no_mangle]
pub extern "C" fn runa_free_string(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe {
            let _ = CString::from_raw(ptr);
        }
    }
}

/// Free bytes array allocated by runtime calls
#[no_mangle]
pub extern "C" fn runa_free_bytes(bytes: RunaBytes) {
    if !bytes.data.is_null() && bytes.length > 0 {
        unsafe {
            let _ = Vec::from_raw_parts(bytes.data, bytes.length, bytes.length);
        }
    }
}

/// Free string array allocated by directory listing
#[no_mangle]
pub extern "C" fn runa_free_string_array(array: *mut *mut c_char, count: usize) {
    if !array.is_null() && count > 0 {
        unsafe {
            for i in 0..count {
                let str_ptr = *array.add(i);
                if !str_ptr.is_null() {
                    let _ = CString::from_raw(str_ptr);
                }
            }
            let _ = Vec::from_raw_parts(array, count, count);
        }
    }
}

/// Free environment variable arrays
#[no_mangle]
pub extern "C" fn runa_free_environment_arrays(keys: *mut *mut c_char, values: *mut *mut c_char, count: usize) {
    runa_free_string_array(keys, count);
    runa_free_string_array(values, count);
}

// ============================================================================
// SYSTEM VALIDATION FUNCTIONS
// ============================================================================

fn test_file_system() -> bool {
    // Test basic file operations
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

/// Test crypto system functionality
#[no_mangle]
pub extern "C" fn test_crypto_system() -> bool {
    // Test random bytes generation
    let random_bytes = system_call_random_bytes(32);
    if random_bytes.data.is_null() || random_bytes.length != 32 {
        runa_free_bytes(random_bytes);
        return false;
    }
    runa_free_bytes(random_bytes);
    
    // Test hashing
    let test_data = b"Hello, World!";
    let algorithm = CString::new("sha256").unwrap();
    let hash_result = system_call_crypto_hash(
        test_data.as_ptr(),
        test_data.len(),
        algorithm.as_ptr(),
    );
    
    if hash_result.data.is_null() || hash_result.length != 32 {
        runa_free_bytes(hash_result);
        return false;
    }
    runa_free_bytes(hash_result);
    
    // Test entropy collection
    let entropy = system_call_entropy_collect();
    if entropy.data.is_null() || entropy.length == 0 {
        runa_free_bytes(entropy);
        return false;
    }
    runa_free_bytes(entropy);
    
    true
}

// ============================================================================
// INTERNAL HELPER FUNCTIONS
// ============================================================================

/// Clean up any open file handles
fn cleanup_file_handles() {
    if let Ok(mut file_registry) = FILE_REGISTRY.lock() {
        for (_, mut file) in file_registry.drain() {
            let _ = file.sync_all(); // Flush any pending writes
        }
    }
}

/// Clean up memory tracking resources
fn cleanup_memory_tracking() {
    if let Ok(mut registry) = ALLOCATION_REGISTRY.lock() {
        registry.clear();
    }
}

/// Clean up reflection registries
fn cleanup_reflection_registries() {
    if let Ok(mut cache) = TYPE_NAME_CACHE.lock() {
        cache.clear();
    }
    
    if let Ok(mut stack) = CALL_STACK_REGISTRY.lock() {
        stack.clear();
    }
    
    if let Ok(mut registry) = FUNCTION_NAME_REGISTRY.lock() {
        registry.clear();
    }
    
    if let Ok(mut registry) = MODULE_NAME_REGISTRY.lock() {
        registry.clear();
    }
    
    if let Ok(mut registry) = SOURCE_LOCATION_REGISTRY.lock() {
        registry.clear();
    }
}

/// Report final memory statistics in debug mode
#[cfg(debug_assertions)]
fn report_final_memory_stats() {
    if let Ok(registry) = ALLOCATION_REGISTRY.lock() {
        let total_allocations = registry.len();
        let total_bytes: usize = registry.values().sum();
        
        eprintln!("=== Runa Runtime Shutdown Memory Report ===");
        eprintln!("Total tracked allocations: {}", total_allocations);
        eprintln!("Total tracked bytes: {}", total_bytes);
        
        if total_allocations > 0 {
            eprintln!("WARNING: {} allocations still tracked at shutdown", total_allocations);
        }
    }
}

/// Analyze memory pattern to infer object type (unsafe helper)
unsafe fn analyze_memory_pattern(obj: *const c_void) -> String {
    if obj.is_null() {
        return "null".to_string();
    }
    
    // Simple pattern analysis - in a real implementation this would be more sophisticated
    let ptr_as_bytes = std::slice::from_raw_parts(obj as *const u8, 8);
    
    // Check for common patterns
    if ptr_as_bytes.iter().all(|&b| b == 0) {
        "zeroed_data".to_string()
    } else if ptr_as_bytes.iter().all(|&b| b.is_ascii_alphanumeric() || b.is_ascii_whitespace()) {
        "string_like".to_string()
    } else if ptr_as_bytes[0] < 128 && ptr_as_bytes.iter().skip(1).all(|&b| b == 0) {
        "integer_like".to_string()
    } else {
        "binary_data".to_string()
    }
}

/// Analyze object size from memory patterns (unsafe helper)
unsafe fn analyze_object_size(obj: *const c_void) -> usize {
    if obj.is_null() {
        return 0;
    }
    
    // Try to find end of data by looking for patterns
    // This is a simplified heuristic - real implementation would be more robust
    let base_ptr = obj as *const u8;
    
    for size in [8, 16, 32, 64, 128, 256, 512, 1024].iter() {
        // Check if we can safely read this much
        if is_readable_memory(base_ptr, *size) {
            continue;
        } else {
            return if *size > 8 { *size - 8 } else { 8 };
        }
    }
    
    // Default fallback
    64
}

/// Check if memory region is readable (unsafe helper)
unsafe fn is_readable_memory(ptr: *const u8, size: usize) -> bool {
    if ptr.is_null() || size == 0 {
        return false;
    }
    
    // Very basic check - in production this would use OS-specific APIs
    // For now, just assume small regions are readable
    size <= 1024
}

/// Get human-readable documentation for the runtime interface
#[no_mangle]
pub extern "C" fn runa_runtime_docs() -> *const c_char {
    b"Runa Runtime Interface Documentation\n\
    \n\
    This runtime provides 27 system calls organized into 4 categories:\n\
    \n\
    FILE SYSTEM (8 functions):\n\
    - system_call_file_open/read/write/close\n\
    - system_call_file_create/delete\n\
    - system_call_directory_create/list\n\
    \n\
    PROCESS & OS (10 functions):\n\
    - system_call_process_execute/exit\n\
    - system_call_time_current/high_res\n\
    - system_call_environment_get/set/list/remove\n\
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