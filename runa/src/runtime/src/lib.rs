#![allow(non_camel_case_types)]

pub mod vm;
pub mod memory;
pub mod os;
pub mod ffi;
pub mod concurrency;
pub mod gc;
pub mod ownership;

// NEW: Runtime Interface - The 25 Essential System Calls
pub mod runtime_interface;
pub mod runtime_interface_reflection;
pub mod runtime_interface_crypto;
pub mod runtime_exports;

use std::ffi::{c_char, c_void};

/// Represents a raw pointer to a Runa object.
pub type runa_object = *mut c_void;

/// Represents a file handle.
pub type runa_file_handle = *mut c_void;

/// Represents a thread handle.
pub type runa_thread_handle = *mut c_void;

/// Represents a mutex handle.
pub type runa_mutex_handle = *mut c_void;

/// Represents a condition variable handle.
pub type runa_condvar_handle = *mut c_void;

/// Represents a channel handle.
pub type runa_channel_handle = *mut c_void;

/// Error codes for runtime operations
#[repr(C)]
pub enum RunaError {
    Success = 0,
    OutOfMemory = 1,
    FileNotFound = 2,
    PermissionDenied = 3,
    InvalidArgument = 4,
    IoError = 5,
    ThreadError = 6,
    MutexError = 7,
    ChannelError = 8,
    UnknownError = 255,
}

/// Result type for runtime operations
#[repr(C)]
pub struct RunaResult {
    pub error: RunaError,
    pub value: u64, // Can hold pointer, integer, or other data
}

impl RunaResult {
    pub fn success(value: u64) -> Self {
        RunaResult {
            error: RunaError::Success,
            value,
        }
    }

    pub fn error(error: RunaError) -> Self {
        RunaResult {
            error,
            value: 0,
        }
    }
}

// Re-export the legacy functions for backward compatibility
// These will be deprecated in favor of the new modular system

/// Allocates a block of memory of a given size.
/// This is the most basic memory primitive.
#[no_mangle]
pub extern "C" fn _rt_alloc(size: usize) -> runa_object {
    memory::alloc(size)
}

/// Deallocates a previously allocated block of memory.
#[no_mangle]
pub extern "C" fn _rt_free(ptr: runa_object) {
    memory::free(ptr);
}



/// Opens a file with the given path and mode.
/// Returns a handle to the file, or a null pointer on error.
#[no_mangle]
pub extern "C" fn _rt_open_file(path: *const c_char, mode: *const c_char) -> runa_file_handle {
    os::file::open(path, mode)
}

#[cfg(test)]
mod tests {


    #[test]
    fn it_works() {
        // We can add tests for the runtime functions here later.
    }
}
