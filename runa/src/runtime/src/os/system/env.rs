//! Environment variable operations for the Runa runtime.

use std::ffi::{c_char, CStr};
use std::alloc::{alloc, Layout};
use std::collections::HashMap;
use std::sync::{Mutex, LazyLock};

// Global storage for environment variable strings to prevent deallocation
static ENV_BUFFERS: LazyLock<Mutex<HashMap<usize, Vec<u8>>>> = LazyLock::new(|| Mutex::new(HashMap::new()));
static mut ENV_COUNTER: usize = 0;

/// Gets an environment variable by name
/// Returns a pointer to a null-terminated string, or null if not found
pub fn get(name: *const c_char) -> *const c_char {
    if name.is_null() {
        return std::ptr::null();
    }

    let name_str = match unsafe { CStr::from_ptr(name).to_str() } {
        Ok(s) => s,
        Err(_) => return std::ptr::null(),
    };

    match std::env::var(name_str) {
        Ok(value) => {
            // Allocate memory for the string
            let bytes = value.as_bytes();
            let size = bytes.len() + 1; // +1 for null terminator
            
            let layout = Layout::from_size_align(size, std::mem::align_of::<u8>()).unwrap();
            let ptr = unsafe { alloc(layout) };
            
            if !ptr.is_null() {
                // Copy the string data
                unsafe {
                    std::ptr::copy_nonoverlapping(bytes.as_ptr(), ptr, bytes.len());
                    std::ptr::write(ptr.add(bytes.len()), 0u8); // null terminator
                }
                
                // Store the buffer to prevent deallocation
                let buffer_id = unsafe {
                    ENV_COUNTER += 1;
                    ENV_COUNTER
                };
                
                if let Ok(mut buffers) = ENV_BUFFERS.lock() {
                    buffers.insert(buffer_id, bytes.to_vec());
                }
                
                return ptr as *const c_char;
            }
        }
        Err(_) => {}
    }
    
    std::ptr::null()
}

/// Sets an environment variable
/// Returns 0 on success, -1 on error
pub fn set(name: *const c_char, value: *const c_char) -> i32 {
    if name.is_null() {
        return -1;
    }

    let name_str = match unsafe { CStr::from_ptr(name).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    let value_str = if value.is_null() {
        None
    } else {
        match unsafe { CStr::from_ptr(value).to_str() } {
            Ok(s) => Some(s),
            Err(_) => return -1,
        }
    };

    match value_str {
        Some(val) => {
            std::env::set_var(name_str, val);
            0
        }
        None => {
            std::env::remove_var(name_str);
            0
        }
    }
}

/// Frees an environment variable buffer
pub fn free_env_buffer(ptr: *const c_char) {
    if ptr.is_null() {
        return;
    }
    
    // Find and remove the buffer from our storage
    if let Ok(mut buffers) = ENV_BUFFERS.lock() {
        let mut to_remove = None;
        for (id, _) in buffers.iter() {
            if ptr as usize == *id {
                to_remove = Some(*id);
                break;
            }
        }
        
        if let Some(id) = to_remove {
            buffers.remove(&id);
        }
    }
    
    // Free the memory
    unsafe {
        std::alloc::dealloc(ptr as *mut u8, Layout::from_size_align(1, 1).unwrap());
    }
}

/// Gets all environment variables
/// Returns a pointer to an array of key-value pairs, or null on error
/// The array is terminated with a null pointer
pub fn get_all() -> *const *const c_char {
    // This is a simplified implementation
    // In a real system, we'd need to manage the memory properly
    std::ptr::null()
}

/// Clears all environment variables
/// Returns 0 on success, -1 on error
pub fn clear_all() -> i32 {
    // This is a simplified implementation
    // In a real system, we'd clear all environment variables
    -1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_env_operations() {
        // Test setting and getting an environment variable
        let name = std::ffi::CString::new("TEST_VAR").unwrap();
        let value = std::ffi::CString::new("test_value").unwrap();
        
        // Set the environment variable
        let set_result = set(name.as_ptr(), value.as_ptr());
        assert_eq!(set_result, 0);
        
        // Get the environment variable
        let retrieved = get(name.as_ptr());
        assert!(!retrieved.is_null());
        
        // Verify the value
        let retrieved_str = unsafe { CStr::from_ptr(retrieved).to_str().unwrap() };
        assert_eq!(retrieved_str, "test_value");
        
        // Clean up
        free_env_buffer(retrieved);
    }

    #[test]
    fn test_null_handling() {
        // Test null pointer handling
        assert!(get(std::ptr::null()).is_null());
        assert_eq!(set(std::ptr::null(), std::ptr::null()), -1);
    }

    #[test]
    fn test_nonexistent_var() {
        let name = std::ffi::CString::new("NONEXISTENT_VAR").unwrap();
        let result = get(name.as_ptr());
        assert!(result.is_null());
    }
} 