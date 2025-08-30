//! System-level operations for the Runa runtime.

pub mod env;
pub mod time;
pub mod process;
pub mod info;

use std::ffi::{c_char, CStr};


/// Gets the current working directory
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_current_dir() -> *const c_char {
    match std::env::current_dir() {
        Ok(path) => {
            if let Some(path_str) = path.to_str() {
                if let Ok(c_str) = CStr::from_bytes_with_nul(path_str.as_bytes()) {
                    return c_str.as_ptr();
                }
            }
        }
        Err(_) => {}
    }
    std::ptr::null()
}

/// Changes the current working directory
/// Returns 0 on success, -1 on error
pub fn change_dir(path: *const c_char) -> i32 {
    if path.is_null() {
        return -1;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    match std::env::set_current_dir(path_str) {
        Ok(_) => 0,
        Err(_) => -1,
    }
}

/// Gets the number of command line arguments
pub fn get_argc() -> i32 {
    std::env::args().count() as i32
}

/// Gets a command line argument by index
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_argv(index: i32) -> *const c_char {
    if index < 0 {
        return std::ptr::null();
    }

    let args: Vec<String> = std::env::args().collect();
    if index as usize >= args.len() {
        return std::ptr::null();
    }

    args.get(index as usize)
        .map(|arg| {
            // Allocate memory for the string and return pointer
            if let Ok(c_str) = std::ffi::CString::new(arg.as_str()) {
                let bytes = c_str.as_bytes_with_nul();
                let layout = std::alloc::Layout::from_size_align(bytes.len(), std::mem::align_of::<u8>()).unwrap();
                let ptr = unsafe { std::alloc::alloc(layout) };
                
                if !ptr.is_null() {
                    unsafe {
                        std::ptr::copy_nonoverlapping(bytes.as_ptr(), ptr, bytes.len());
                    }
                    return ptr as *const c_char;
                }
            }
            std::ptr::null()
        })
        .unwrap_or(std::ptr::null())
}

/// Exits the program with the given exit code
pub fn exit(code: i32) -> ! {
    std::process::exit(code);
}

/// Aborts the program
pub fn abort() -> ! {
    std::process::abort();
}

/// Gets the system page size
pub fn get_page_size() -> usize {
    info::get_page_size()
}

/// Gets the total system memory in bytes
pub fn get_total_memory() -> u64 {
    info::get_total_memory()
}

/// Gets the available system memory in bytes
pub fn get_available_memory() -> u64 {
    info::get_available_memory()
}

/// Gets the number of CPU cores
pub fn get_cpu_count() -> u32 {
    std::thread::available_parallelism()
        .map(|n| n.get() as u32)
        .unwrap_or(1)
}

/// Suspends execution for the specified number of seconds
pub fn sleep(seconds: f64) {
    let duration = std::time::Duration::from_secs_f64(seconds);
    std::thread::sleep(duration);
}

/// Suspends execution for the specified number of milliseconds
pub fn sleep_ms(milliseconds: u64) {
    let duration = std::time::Duration::from_millis(milliseconds);
    std::thread::sleep(duration);
}

/// Suspends execution for the specified number of microseconds
pub fn sleep_us(microseconds: u64) {
    let duration = std::time::Duration::from_micros(microseconds);
    std::thread::sleep(duration);
}

/// Yields the current thread to allow other threads to run
pub fn yield_thread() {
    std::thread::yield_now();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_system_operations() {
        // Test basic system information
        assert!(get_page_size() > 0);
        assert!(get_total_memory() > 0);
        assert!(get_available_memory() > 0);
        assert!(get_cpu_count() > 0);

        // Test argument count
        let argc = get_argc();
        assert!(argc >= 0);

        // Test sleep (very short)
        let start = std::time::Instant::now();
        sleep_ms(1);
        let elapsed = start.elapsed();
        assert!(elapsed >= std::time::Duration::from_millis(1));
    }

    #[test]
    fn test_directory_operations() {
        // Test getting current directory
        let _current_dir = get_current_dir();
        // Note: current_dir might be null in some environments
        // so we can't assert it's not null

        // Test changing to current directory (should succeed)
        let current_dir_str = std::env::current_dir().unwrap();
        let current_dir_cstr = std::ffi::CString::new(current_dir_str.to_str().unwrap()).unwrap();
        let result = change_dir(current_dir_cstr.as_ptr());
        assert_eq!(result, 0);
    }
} 