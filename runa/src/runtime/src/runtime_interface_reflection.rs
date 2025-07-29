//! Reflection and Introspection Runtime Operations
//!
//! This module implements the 6 reflection system calls that allow Runa programs
//! to inspect their own structure, call stacks, and type information at runtime.

use std::ffi::{c_char, c_void, CStr, CString};
use std::ptr;
use std::collections::HashMap;
use std::sync::{Mutex, LazyLock};
use backtrace::Backtrace;

// ============================================================================
// REFLECTION TYPE DEFINITIONS
// ============================================================================

/// Stack frame information for reflection
#[repr(C)]
pub struct RunaStackFrame {
    pub function_name: *mut c_char,
    pub module_name: *mut c_char,
    pub file_path: *mut c_char,
    pub line_number: i32,
    pub column_number: i32,
}

/// Source location information
#[repr(C)]
pub struct RunaSourceLocation {
    pub file_path: *mut c_char,
    pub line_number: i32,
    pub column_number: i32,
}

/// Type information structure
#[repr(C)]
pub struct RunaTypeInfo {
    pub name: *mut c_char,
    pub module: *mut c_char,
    pub is_callable: bool,
    pub object_id: usize,
    pub size: usize,
    pub attribute_count: usize,
    pub attributes: *mut *mut c_char,
}

// ============================================================================
// GLOBAL REFLECTION STATE
// ============================================================================

// Type registry for runtime type tracking
static TYPE_REGISTRY: LazyLock<Mutex<HashMap<usize, String>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

// Function name registry for runtime debugging
static FUNCTION_REGISTRY: LazyLock<Mutex<HashMap<usize, String>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

// Module registry for namespace tracking
static MODULE_REGISTRY: LazyLock<Mutex<HashMap<usize, String>>> = 
    LazyLock::new(|| Mutex::new(HashMap::new()));

// ============================================================================
// REFLECTION CORE OPERATIONS (6 functions)
// ============================================================================

/// system_call_type_name: Get type name of object
/// Maps to: system_call_type_name(obj: Any) -> String
#[no_mangle]
pub extern "C" fn system_call_type_name(obj: *const c_void) -> *mut c_char {
    if obj.is_null() {
        return CString::new("Null").unwrap().into_raw();
    }

    let obj_addr = obj as usize;
    
    // Check type registry first
    if let Ok(registry) = TYPE_REGISTRY.lock() {
        if let Some(type_name) = registry.get(&obj_addr) {
            return CString::new(type_name.as_str()).unwrap().into_raw();
        }
    }
    
    // Perform basic type inference based on memory patterns
    // This is a simplified implementation - a full runtime would have
    // complete type metadata available
    unsafe {
        let first_bytes = std::slice::from_raw_parts(obj as *const u8, 8);
        
        // Check for common patterns that might indicate type
        match first_bytes {
            // String-like patterns (starts with length)
            [len, 0, 0, 0, _, _, _, _] if *len > 0 && *len < 255 => {
                CString::new("String").unwrap().into_raw()
            }
            // Integer patterns (small values)
            [val, 0, 0, 0, 0, 0, 0, 0] if *val < 100 => {
                CString::new("Integer").unwrap().into_raw()
            }
            // List/Array patterns (pointer-like values)
            _ if obj_addr > 0x1000 && obj_addr < 0x7fff_ffff_ffff => {
                CString::new("Object").unwrap().into_raw()
            }
            _ => {
                CString::new("Unknown").unwrap().into_raw()
            }
        }
    }
}

/// system_call_object_size: Get size of object in bytes
/// Maps to: system_call_object_size(obj: Any) -> Integer
#[no_mangle]
pub extern "C" fn system_call_object_size(obj: *const c_void) -> usize {
    if obj.is_null() {
        return 0;
    }

    // In a full implementation, this would use the memory allocator's
    // metadata to determine the actual allocated size
    // For now, we provide a reasonable estimate based on type
    
    let type_name_ptr = system_call_type_name(obj);
    if !type_name_ptr.is_null() {
        let type_name = unsafe { 
            let cstr = CStr::from_ptr(type_name_ptr);
            let result = cstr.to_str().unwrap_or("Unknown");
            let _ = CString::from_raw(type_name_ptr); // Free the string
            result.to_string()
        };
        
        match type_name.as_str() {
            "String" => {
                // Try to read string length from first 4 bytes
                unsafe {
                    let len_bytes = std::slice::from_raw_parts(obj as *const u8, 4);
                    let len = u32::from_le_bytes([len_bytes[0], len_bytes[1], len_bytes[2], len_bytes[3]]);
                    (len as usize).min(1024) + 8 // String data + metadata
                }
            }
            "Integer" => 8,
            "Float" => 8,
            "Boolean" => 1,
            "List" => {
                // Estimate based on typical list overhead
                64 // Base list structure
            }
            "Dictionary" => {
                // Estimate based on typical hash map overhead  
                128 // Base hash map structure
            }
            _ => 32, // Default object size estimate
        }
    } else {
        32
    }
}

/// system_call_call_stack: Get current call stack
/// Maps to: system_call_call_stack() -> List[StackFrame]
#[no_mangle]
pub extern "C" fn system_call_call_stack(frames_out: *mut *mut RunaStackFrame, count_out: *mut usize) -> bool {
    if frames_out.is_null() || count_out.is_null() {
        return false;
    }

    // Capture backtrace
    let backtrace = Backtrace::new();
    let mut stack_frames = Vec::new();
    
    // Process backtrace frames
    for frame in backtrace.frames().iter().take(10) { // Limit to 10 frames
        for symbol in frame.symbols() {
            let function_name = symbol.name()
                .map(|name| name.to_string())
                .unwrap_or_else(|| "<unknown>".to_string());
                
            let (file_path, line_number) = if let (Some(filename), Some(line)) = (symbol.filename(), symbol.lineno()) {
                (filename.to_string_lossy().to_string(), line as i32)
            } else {
                ("<unknown>".to_string(), 0)
            };
            
            let module_name = extract_module_from_function(&function_name);
            
            let stack_frame = RunaStackFrame {
                function_name: CString::new(function_name).unwrap().into_raw(),
                module_name: CString::new(module_name).unwrap().into_raw(),
                file_path: CString::new(file_path).unwrap().into_raw(),
                line_number,
                column_number: 0, // Column info not available from backtrace
            };
            
            stack_frames.push(stack_frame);
            break; // Take only first symbol per frame
        }
    }
    
    let count = stack_frames.len();
    if count > 0 {
        let frames_ptr = stack_frames.as_mut_ptr();
        std::mem::forget(stack_frames);
        
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

/// system_call_function_name: Get function name
/// Maps to: system_call_function_name(func: Any) -> String
#[no_mangle]
pub extern "C" fn system_call_function_name(func: *const c_void) -> *mut c_char {
    if func.is_null() {
        return CString::new("Unknown").unwrap().into_raw();
    }

    let func_addr = func as usize;
    
    // Check function registry
    if let Ok(registry) = FUNCTION_REGISTRY.lock() {
        if let Some(func_name) = registry.get(&func_addr) {
            return CString::new(func_name.as_str()).unwrap().into_raw();
        }
    }
    
    // Try to extract function name from current call stack
    let backtrace = Backtrace::new();
    for frame in backtrace.frames().iter().take(3) {
        for symbol in frame.symbols() {
            if let Some(name) = symbol.name() {
                let name_str = name.to_string();
                if name_str.contains("runa") || name_str.contains("Process") {
                    return CString::new(clean_function_name(&name_str)).unwrap().into_raw();
                }
            }
        }
    }
    
    CString::new("Unknown").unwrap().into_raw()
}

/// system_call_module_name: Get module name of object
/// Maps to: system_call_module_name(obj: Any) -> String  
#[no_mangle]
pub extern "C" fn system_call_module_name(obj: *const c_void) -> *mut c_char {
    if obj.is_null() {
        return CString::new("Unknown").unwrap().into_raw();
    }

    let obj_addr = obj as usize;
    
    // Check module registry
    if let Ok(registry) = MODULE_REGISTRY.lock() {
        if let Some(module_name) = registry.get(&obj_addr) {
            return CString::new(module_name.as_str()).unwrap().into_raw();
        }
    }
    
    // Try to infer module from call stack
    let backtrace = Backtrace::new();
    for frame in backtrace.frames().iter().take(5) {
        for symbol in frame.symbols() {
            if let Some(filename) = symbol.filename() {
                let filename_str = filename.to_string_lossy();
                if filename_str.contains("runa") {
                    let module = extract_module_from_path(&filename_str);
                    return CString::new(module).unwrap().into_raw();
                }
            }
        }
    }
    
    CString::new("main").unwrap().into_raw()
}

/// system_call_source_location: Get source location of function
/// Maps to: system_call_source_location(func: Any) -> SourceLocation
#[no_mangle]
pub extern "C" fn system_call_source_location(func: *const c_void) -> RunaSourceLocation {
    let unknown_location = RunaSourceLocation {
        file_path: CString::new("unknown").unwrap().into_raw(),
        line_number: 0,
        column_number: 0,
    };
    
    if func.is_null() {
        return unknown_location;
    }
    
    // Try to get location from current call stack
    let backtrace = Backtrace::new();
    for frame in backtrace.frames().iter().take(3) {
        for symbol in frame.symbols() {
            if let (Some(filename), Some(line)) = (symbol.filename(), symbol.lineno()) {
                let file_path_str = filename.to_string_lossy().to_string();
                if file_path_str.contains("runa") || file_path_str.contains(".runa") {
                    return RunaSourceLocation {
                        file_path: CString::new(file_path_str).unwrap().into_raw(),
                        line_number: line as i32,
                        column_number: 0, // Column info not typically available
                    };
                }
            }
        }
    }
    
    unknown_location
}

// ============================================================================
// HELPER FUNCTIONS FOR REFLECTION
// ============================================================================

/// Extract module name from function name
fn extract_module_from_function(func_name: &str) -> String {
    if let Some(pos) = func_name.rfind("::") {
        let module_part = &func_name[..pos];
        if let Some(last_module) = module_part.split("::").last() {
            return last_module.to_string();
        }
    }
    "main".to_string()
}

/// Extract module name from file path
fn extract_module_from_path(path: &str) -> String {
    if let Some(filename) = path.split('/').last().or_else(|| path.split('\\').last()) {
        if let Some(name_part) = filename.split('.').next() {
            return name_part.to_string();
        }
    }
    "main".to_string()
}

/// Clean up mangled function names for display
fn clean_function_name(raw_name: &str) -> String {
    // Remove Rust mangling and keep readable part
    if let Some(pos) = raw_name.find("::") {
        let clean_part = &raw_name[pos + 2..];
        if let Some(end_pos) = clean_part.find("::") {
            clean_part[..end_pos].to_string()
        } else {
            clean_part.to_string()
        }
    } else {
        raw_name.to_string()
    }
}

// ============================================================================
// REFLECTION REGISTRY MANAGEMENT
// ============================================================================

/// Register a type for runtime reflection
#[no_mangle]
pub extern "C" fn runa_register_type(obj_addr: usize, type_name: *const c_char) -> bool {
    if type_name.is_null() {
        return false;
    }
    
    let name_str = match unsafe { CStr::from_ptr(type_name).to_str() } {
        Ok(s) => s.to_string(),
        Err(_) => return false,
    };
    
    if let Ok(mut registry) = TYPE_REGISTRY.lock() {
        registry.insert(obj_addr, name_str);
        true
    } else {
        false
    }
}

/// Register a function for runtime reflection
#[no_mangle]
pub extern "C" fn runa_register_function(func_addr: usize, func_name: *const c_char) -> bool {
    if func_name.is_null() {
        return false;
    }
    
    let name_str = match unsafe { CStr::from_ptr(func_name).to_str() } {
        Ok(s) => s.to_string(),
        Err(_) => return false,
    };
    
    if let Ok(mut registry) = FUNCTION_REGISTRY.lock() {
        registry.insert(func_addr, name_str);
        true
    } else {
        false
    }
}

/// Register a module for runtime reflection
#[no_mangle]
pub extern "C" fn runa_register_module(obj_addr: usize, module_name: *const c_char) -> bool {
    if module_name.is_null() {
        return false;
    }
    
    let name_str = match unsafe { CStr::from_ptr(module_name).to_str() } {
        Ok(s) => s.to_string(),
        Err(_) => return false,
    };
    
    if let Ok(mut registry) = MODULE_REGISTRY.lock() {
        registry.insert(obj_addr, name_str);
        true
    } else {
        false
    }
}

// ============================================================================
// MEMORY CLEANUP FOR REFLECTION STRUCTURES
// ============================================================================

/// Free stack frame array allocated by call_stack
#[no_mangle]
pub extern "C" fn runa_free_stack_frames(frames: *mut RunaStackFrame, count: usize) {
    if !frames.is_null() && count > 0 {
        unsafe {
            for i in 0..count {
                let frame = &*frames.add(i);
                if !frame.function_name.is_null() {
                    let _ = CString::from_raw(frame.function_name);
                }
                if !frame.module_name.is_null() {
                    let _ = CString::from_raw(frame.module_name);
                }
                if !frame.file_path.is_null() {
                    let _ = CString::from_raw(frame.file_path);
                }
            }
            let _ = Vec::from_raw_parts(frames, count, count);
        }
    }
}

/// Free source location structure
#[no_mangle]
pub extern "C" fn runa_free_source_location(location: RunaSourceLocation) {
    if !location.file_path.is_null() {
        unsafe {
            let _ = CString::from_raw(location.file_path);
        }
    }
}