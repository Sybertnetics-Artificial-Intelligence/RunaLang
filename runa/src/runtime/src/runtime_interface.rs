//! Native Rust Implementation of Runa's 25 Essential System Calls
//! 
//! This module provides the native runtime implementation that bridges Runa code
//! to actual system operations. These functions are called by the Runa standard
//! library through the bytecode execution engine.
//!
//! Architecture:
//! Runa stdlib → Bytecode → VM → Native Runtime (this module) → OS
//!
//! This is the critical layer that makes Runa programs actually work with real
//! files, processes, memory, and system resources.

use std::ffi::{c_char, c_void, CStr, CString};
use std::fs::{File, OpenOptions};
use std::io::{Read, Write, Seek, SeekFrom};
use std::process::{Command, Stdio};
use std::collections::HashMap;
use std::sync::{Mutex, LazyLock};
use std::time::{SystemTime, UNIX_EPOCH};
use std::env;
use std::ptr;

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

/// Bytes array structure - maps to Runa's Bytes (List[Integer])
#[repr(C)]
pub struct RunaBytes {
    pub data: *mut u8,
    pub length: usize,
}

// ============================================================================
// GLOBAL STATE MANAGEMENT
// ============================================================================

// File handle registry - thread-safe mapping of handles to files
static FILE_REGISTRY: LazyLock<Mutex<HashMap<i32, File>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

static mut NEXT_FILE_HANDLE: i32 = 1;

// Memory allocation tracking for debugging
static ALLOCATION_REGISTRY: LazyLock<Mutex<HashMap<usize, usize>>> = 
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
                *result_array = names_ptr;
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
// HELPER FUNCTIONS FOR MEMORY MANAGEMENT
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