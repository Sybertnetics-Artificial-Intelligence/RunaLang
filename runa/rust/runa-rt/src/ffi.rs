//! Foreign Function Interface for the Runa runtime.

use std::collections::HashMap;
use std::sync::{Mutex, LazyLock};
use crate::{runa_object, RunaResult, RunaError};

/// Function pointer type for FFI functions
pub type FfiFunction = fn(args: &[runa_object]) -> RunaResult;

/// Registry of FFI functions
static FFI_REGISTRY: LazyLock<Mutex<HashMap<String, FfiFunction>>> = LazyLock::new(|| Mutex::new(HashMap::new()));

/// Registers an FFI function
pub fn register_function(name: &str, func: FfiFunction) -> bool {
    if let Ok(mut registry) = FFI_REGISTRY.lock() {
        registry.insert(name.to_string(), func);
        true
    } else {
        false
    }
}

/// Unregisters an FFI function
pub fn unregister_function(name: &str) -> bool {
    if let Ok(mut registry) = FFI_REGISTRY.lock() {
        registry.remove(name).is_some()
    } else {
        false
    }
}

/// Calls an FFI function by name
pub fn call_function(name: &str, args: &[runa_object]) -> RunaResult {
    if let Ok(registry) = FFI_REGISTRY.lock() {
        if let Some(func) = registry.get(name) {
            func(args)
        } else {
            RunaResult::error(RunaError::UnknownError)
        }
    } else {
        RunaResult::error(RunaError::UnknownError)
    }
}

/// Checks if an FFI function is registered
pub fn is_function_registered(name: &str) -> bool {
    if let Ok(registry) = FFI_REGISTRY.lock() {
        registry.contains_key(name)
    } else {
        false
    }
}

/// Gets the number of registered FFI functions
pub fn get_function_count() -> usize {
    if let Ok(registry) = FFI_REGISTRY.lock() {
        registry.len()
    } else {
        0
    }
}

/// Gets a list of registered FFI function names
pub fn get_function_names() -> Vec<String> {
    if let Ok(registry) = FFI_REGISTRY.lock() {
        registry.keys().cloned().collect()
    } else {
        Vec::new()
    }
}

/// Built-in FFI functions

/// Print function - prints a string to stdout
fn ffi_print(args: &[runa_object]) -> RunaResult {
    if args.is_empty() {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just print a placeholder
    // In a real implementation, we'd convert the runa_object to a string
    println!("[FFI] Print called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// Input function - reads a string from stdin
fn ffi_input(args: &[runa_object]) -> RunaResult {
    // For now, we'll just return a placeholder
    // In a real implementation, we'd read from stdin and return a string
    println!("[FFI] Input called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// File open function
fn ffi_file_open(args: &[runa_object]) -> RunaResult {
    if args.len() < 2 {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd open the file and return a handle
    println!("[FFI] File open called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// File read function
fn ffi_file_read(args: &[runa_object]) -> RunaResult {
    if args.len() < 2 {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd read from the file
    println!("[FFI] File read called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// File write function
fn ffi_file_write(args: &[runa_object]) -> RunaResult {
    if args.len() < 2 {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd write to the file
    println!("[FFI] File write called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// File close function
fn ffi_file_close(args: &[runa_object]) -> RunaResult {
    if args.is_empty() {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd close the file
    println!("[FFI] File close called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// Memory allocation function
fn ffi_alloc(args: &[runa_object]) -> RunaResult {
    if args.is_empty() {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd allocate memory
    println!("[FFI] Alloc called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// Memory free function
fn ffi_free(args: &[runa_object]) -> RunaResult {
    if args.is_empty() {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd free memory
    println!("[FFI] Free called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// Time function - gets current time
fn ffi_time(args: &[runa_object]) -> RunaResult {
    // For now, we'll just return a placeholder
    // In a real implementation, we'd get the current time
    println!("[FFI] Time called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// Sleep function - suspends execution
fn ffi_sleep(args: &[runa_object]) -> RunaResult {
    if args.is_empty() {
        return RunaResult::error(RunaError::InvalidArgument);
    }
    
    // For now, we'll just return a placeholder
    // In a real implementation, we'd sleep for the specified time
    println!("[FFI] Sleep called with {} arguments", args.len());
    
    RunaResult::success(0)
}

/// Initialize the FFI system with built-in functions
pub fn initialize_ffi() {
    register_function("print", ffi_print);
    register_function("input", ffi_input);
    register_function("file_open", ffi_file_open);
    register_function("file_read", ffi_file_read);
    register_function("file_write", ffi_file_write);
    register_function("file_close", ffi_file_close);
    register_function("alloc", ffi_alloc);
    register_function("free", ffi_free);
    register_function("time", ffi_time);
    register_function("sleep", ffi_sleep);
}

/// Clean up the FFI system
pub fn cleanup_ffi() {
    if let Ok(mut registry) = FFI_REGISTRY.lock() {
        registry.clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ffi_registration() {
        // Test function registration
        let test_func = |args: &[runa_object]| {
            println!("Test function called with {} arguments", args.len());
            RunaResult::success(args.len() as u64)
        };
        
        assert!(register_function("test_func", test_func));
        assert!(is_function_registered("test_func"));
        
        // Test function calling
        let args = vec![std::ptr::null_mut(); 3];
        let result = call_function("test_func", &args);
        assert_eq!(result.error as i32, RunaError::Success as i32);
        assert_eq!(result.value, 3);
        
        // Test function unregistration
        assert!(unregister_function("test_func"));
        assert!(!is_function_registered("test_func"));
    }

    #[test]
    fn test_builtin_functions() {
        // Initialize FFI
        initialize_ffi();
        
        // Test that built-in functions are registered
        assert!(is_function_registered("print"));
        assert!(is_function_registered("input"));
        assert!(is_function_registered("file_open"));
        assert!(is_function_registered("alloc"));
        assert!(is_function_registered("time"));
        
        // Test function count
        let count = get_function_count();
        assert!(count >= 10); // At least our built-in functions
        
        // Test function names
        let names = get_function_names();
        assert!(names.contains(&"print".to_string()));
        assert!(names.contains(&"input".to_string()));
        
        // Clean up
        cleanup_ffi();
    }

    #[test]
    fn test_nonexistent_function() {
        let args = vec![std::ptr::null_mut()];
        let result = call_function("nonexistent", &args);
        assert_eq!(result.error as i32, RunaError::UnknownError as i32);
    }
} 