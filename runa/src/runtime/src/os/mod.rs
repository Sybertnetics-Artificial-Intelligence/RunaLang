//! Operating system abstraction layer for the Runa runtime.

pub mod console;
pub mod file;
pub mod system;

use std::ffi::{c_char, c_void};
use crate::runa_file_handle;

/// File access modes
#[repr(C)]
pub enum FileMode {
    Read = 0,
    Write = 1,
    Append = 2,
    ReadWrite = 3,
}

/// File seek positions
#[repr(C)]
pub enum SeekWhence {
    Start = 0,
    Current = 1,
    End = 2,
}

/// File information structure
#[repr(C)]
pub struct FileInfo {
    pub size: u64,
    pub is_directory: bool,
    pub is_file: bool,
    pub is_readonly: bool,
    pub created_time: u64,
    pub modified_time: u64,
    pub accessed_time: u64,
}

/// System information structure
#[repr(C)]
pub struct SystemInfo {
    pub platform: *const c_char,
    pub architecture: *const c_char,
    pub page_size: usize,
    pub total_memory: u64,
    pub available_memory: u64,
    pub cpu_count: u32,
}

/// Process information structure
#[repr(C)]
pub struct ProcessInfo {
    pub pid: u32,
    pub parent_pid: u32,
    pub memory_usage: u64,
    pub cpu_usage: f64,
}

/// Environment variable operations
#[no_mangle]
pub extern "C" fn _rt_get_env(name: *const c_char) -> *const c_char {
    system::env::get(name)
}

#[no_mangle]
pub extern "C" fn _rt_set_env(name: *const c_char, value: *const c_char) -> i32 {
    system::env::set(name, value) as i32
}

/// System time operations
#[no_mangle]
pub extern "C" fn _rt_get_time() -> u64 {
    system::time::get_current_time()
}

#[no_mangle]
pub extern "C" fn _rt_get_monotonic_time() -> u64 {
    system::time::get_monotonic_time()
}

/// Process operations
#[no_mangle]
pub extern "C" fn _rt_get_pid() -> u32 {
    system::process::get_pid()
}

#[no_mangle]
pub extern "C" fn _rt_get_process_info() -> ProcessInfo {
    system::process::get_info()
}

/// System information
#[no_mangle]
pub extern "C" fn _rt_get_system_info() -> SystemInfo {
    system::info::get()
}

/// File operations (re-exported from file module)
#[no_mangle]
pub extern "C" fn _rt_close_file(handle: runa_file_handle) -> i32 {
    file::close(handle) as i32
}

#[no_mangle]
pub extern "C" fn _rt_read_file(handle: runa_file_handle, buffer: *mut c_void, size: usize) -> isize {
    file::read(handle, buffer, size)
}

#[no_mangle]
pub extern "C" fn _rt_write_file(handle: runa_file_handle, buffer: *const c_void, size: usize) -> isize {
    file::write(handle, buffer, size)
}

#[no_mangle]
pub extern "C" fn _rt_seek_file(handle: runa_file_handle, offset: i64, whence: SeekWhence) -> i64 {
    file::seek(handle, offset, whence)
}

#[no_mangle]
pub extern "C" fn _rt_get_file_info(handle: runa_file_handle) -> FileInfo {
    file::get_info(handle)
}

/// Console operations (re-exported from console module)
#[no_mangle]
pub extern "C" fn _rt_print(s: *const c_char) {
    console::print(s);
}

#[no_mangle]
pub extern "C" fn _rt_println(s: *const c_char) {
    console::println(s);
}

#[no_mangle]
pub extern "C" fn _rt_input(prompt: *const c_char) -> *const c_char {
    console::input(prompt)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_os_operations() {
        // Test that we can get basic system information
        let sys_info = _rt_get_system_info();
        assert!(!sys_info.platform.is_null());
        assert!(!sys_info.architecture.is_null());
        assert!(sys_info.page_size > 0);
        assert!(sys_info.cpu_count > 0);

        // Test that we can get process information
        let pid = _rt_get_pid();
        assert!(pid > 0);

        // Test that we can get time
        let time = _rt_get_time();
        assert!(time > 0);
    }
} 