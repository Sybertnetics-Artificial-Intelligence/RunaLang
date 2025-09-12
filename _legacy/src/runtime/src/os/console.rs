//! Console I/O operations for the Runa runtime.

use std::ffi::{c_char, CStr};
use std::io::{self, Write, BufRead};
use std::sync::{Mutex, LazyLock};
use std::collections::HashMap;
use std::alloc::{alloc, Layout};

// Global storage for input buffers to prevent them from being deallocated
pub static INPUT_BUFFERS: LazyLock<Mutex<HashMap<usize, Vec<u8>>>> = LazyLock::new(|| Mutex::new(HashMap::new()));
static mut BUFFER_COUNTER: usize = 0;

/// Prints a string to stdout without a newline
pub fn print(s: *const c_char) {
    if s.is_null() {
        return;
    }

    let c_str = unsafe { CStr::from_ptr(s) };
    if let Ok(s_str) = c_str.to_str() {
        print!("{}", s_str);
        io::stdout().flush().ok();
    }
}

/// Prints a string to stdout with a newline
pub fn println(s: *const c_char) {
    if s.is_null() {
        println!();
        return;
    }

    let c_str = unsafe { CStr::from_ptr(s) };
    if let Ok(s_str) = c_str.to_str() {
        println!("{}", s_str);
    } else {
        println!("[invalid utf8]");
    }
}

/// Reads a line from stdin with an optional prompt
/// Returns a pointer to a null-terminated string
/// The caller is responsible for freeing the memory
pub fn input(prompt: *const c_char) -> *const c_char {
    // Print the prompt if provided
    if !prompt.is_null() {
        print(prompt);
    }

    // Read a line from stdin
    let mut input = String::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    
    if let Ok(_) = handle.read_line(&mut input) {
        // Remove trailing newline
        let trimmed = input.trim_end_matches('\n').trim_end_matches('\r');
        
        // Allocate memory for the string
        let bytes = trimmed.as_bytes();
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
                BUFFER_COUNTER += 1;
                BUFFER_COUNTER
            };
            
            if let Ok(mut buffers) = INPUT_BUFFERS.lock() {
                buffers.insert(buffer_id, bytes.to_vec());
            }
            
            return ptr as *const c_char;
        }
    }
    
    // Return empty string on error
    let layout = Layout::from_size_align(1, std::mem::align_of::<u8>()).unwrap();
    let ptr = unsafe { alloc(layout) };
    if !ptr.is_null() {
        unsafe {
            std::ptr::write(ptr, 0u8);
        }
    }
    ptr as *const c_char
}

/// Frees an input buffer
pub fn free_input_buffer(ptr: *const c_char) {
    if ptr.is_null() {
        return;
    }
    
    // Find and remove the buffer from our storage
    if let Ok(mut buffers) = INPUT_BUFFERS.lock() {
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

/// Prints an error message to stderr
pub fn eprint(s: *const c_char) {
    if s.is_null() {
        return;
    }

    let c_str = unsafe { CStr::from_ptr(s) };
    if let Ok(s_str) = c_str.to_str() {
        eprint!("{}", s_str);
        io::stderr().flush().ok();
    }
}

/// Prints an error message to stderr with a newline
pub fn eprintln(s: *const c_char) {
    if s.is_null() {
        eprintln!();
        return;
    }

    let c_str = unsafe { CStr::from_ptr(s) };
    if let Ok(s_str) = c_str.to_str() {
        eprintln!("{}", s_str);
    } else {
        eprintln!("[invalid utf8]");
    }
}

/// Checks if stdin is a terminal
pub fn is_tty() -> bool {
    atty::is(atty::Stream::Stdin)
}

/// Gets the terminal size (columns, rows)
pub fn get_terminal_size() -> Option<(u16, u16)> {
    term_size::dimensions().map(|(w, h)| (w as u16, h as u16))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_print_functions() {
        // Test print without newline
        let test_str = std::ffi::CString::new("Hello, World!").unwrap();
        print(test_str.as_ptr());
        
        // Test println with newline
        println(test_str.as_ptr());
        
        // Test null pointer handling
        print(std::ptr::null());
        println(std::ptr::null());
    }

    #[test]
    fn test_error_functions() {
        let test_str = std::ffi::CString::new("Error message").unwrap();
        eprint(test_str.as_ptr());
        eprintln(test_str.as_ptr());
    }

    #[test]
    fn test_terminal_functions() {
        // These functions should not panic
        let _ = is_tty();
        let _ = get_terminal_size();
    }
} 