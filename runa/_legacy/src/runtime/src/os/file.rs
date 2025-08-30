//! File I/O operations for the Runa runtime.

use std::ffi::{c_char, c_void, CStr};
use std::fs::{File, OpenOptions};
use std::io::{Read, Write, Seek, SeekFrom};
use std::collections::HashMap;
use std::sync::{Mutex, LazyLock};
use crate::{runa_file_handle, os::{SeekWhence, FileInfo}};

// Global file handle registry
pub static FILE_HANDLES: LazyLock<Mutex<HashMap<usize, File>>> = LazyLock::new(|| Mutex::new(HashMap::new()));
static mut HANDLE_COUNTER: usize = 0;

/// Opens a file with the given path and mode
/// Returns a file handle or null on error
pub fn open(path: *const c_char, mode: *const c_char) -> runa_file_handle {
    if path.is_null() || mode.is_null() {
        return std::ptr::null_mut();
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return std::ptr::null_mut(),
    };

    let mode_str = match unsafe { CStr::from_ptr(mode).to_str() } {
        Ok(s) => s,
        Err(_) => return std::ptr::null_mut(),
    };

    let mut options = OpenOptions::new();
    
    // Parse mode string
    match mode_str {
        "r" | "read" => {
            options.read(true);
        }
        "w" | "write" => {
            options.write(true).create(true).truncate(true);
        }
        "a" | "append" => {
            options.write(true).create(true).append(true);
        }
        "r+" | "readwrite" => {
            options.read(true).write(true);
        }
        "w+" | "writeplus" => {
            options.read(true).write(true).create(true).truncate(true);
        }
        "a+" | "appendplus" => {
            options.read(true).write(true).create(true).append(true);
        }
        _ => {
            return std::ptr::null_mut();
        }
    }

    match options.open(path_str) {
        Ok(file) => {
            let handle_id = unsafe {
                HANDLE_COUNTER += 1;
                HANDLE_COUNTER
            };

            if let Ok(mut handles) = FILE_HANDLES.lock() {
                handles.insert(handle_id, file);
            }

            handle_id as runa_file_handle
        }
        Err(_) => std::ptr::null_mut(),
    }
}

/// Closes a file handle
/// Returns 0 on success, -1 on error
pub fn close(handle: runa_file_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let handle_id = handle as usize;
    if let Ok(mut handles) = FILE_HANDLES.lock() {
        if handles.remove(&handle_id).is_some() {
            return 0;
        }
    }

    -1
}

/// Reads data from a file
/// Returns number of bytes read, or -1 on error
pub fn read(handle: runa_file_handle, buffer: *mut c_void, size: usize) -> isize {
    if handle.is_null() || buffer.is_null() || size == 0 {
        return -1;
    }

    let handle_id = handle as usize;
    if let Ok(mut handles) = FILE_HANDLES.lock() {
        if let Some(file) = handles.get_mut(&handle_id) {
            let buffer_slice = unsafe {
                std::slice::from_raw_parts_mut(buffer as *mut u8, size)
            };

            match file.read(buffer_slice) {
                Ok(bytes_read) => bytes_read as isize,
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Writes data to a file
/// Returns number of bytes written, or -1 on error
pub fn write(handle: runa_file_handle, buffer: *const c_void, size: usize) -> isize {
    if handle.is_null() || buffer.is_null() || size == 0 {
        return -1;
    }

    let handle_id = handle as usize;
    if let Ok(mut handles) = FILE_HANDLES.lock() {
        if let Some(file) = handles.get_mut(&handle_id) {
            let buffer_slice = unsafe {
                std::slice::from_raw_parts(buffer as *const u8, size)
            };

            match file.write(buffer_slice) {
                Ok(bytes_written) => bytes_written as isize,
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Seeks to a position in a file
/// Returns the new position, or -1 on error
pub fn seek(handle: runa_file_handle, offset: i64, whence: SeekWhence) -> i64 {
    if handle.is_null() {
        return -1;
    }

    let handle_id = handle as usize;
    if let Ok(mut handles) = FILE_HANDLES.lock() {
        if let Some(file) = handles.get_mut(&handle_id) {
            let seek_from = match whence {
                SeekWhence::Start => SeekFrom::Start(offset as u64),
                SeekWhence::Current => SeekFrom::Current(offset),
                SeekWhence::End => SeekFrom::End(offset),
            };

            match file.seek(seek_from) {
                Ok(position) => position as i64,
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Gets information about a file
/// Returns file information structure
pub fn get_info(handle: runa_file_handle) -> FileInfo {
    if handle.is_null() {
        return FileInfo {
            size: 0,
            is_directory: false,
            is_file: false,
            is_readonly: false,
            created_time: 0,
            modified_time: 0,
            accessed_time: 0,
        };
    }

    let handle_id = handle as usize;
    if let Ok(handles) = FILE_HANDLES.lock() {
        if let Some(file) = handles.get(&handle_id) {
            if let Ok(metadata) = file.metadata() {
                return FileInfo {
                    size: metadata.len(),
                    is_directory: metadata.is_dir(),
                    is_file: metadata.is_file(),
                    is_readonly: metadata.permissions().readonly(),
                    created_time: metadata.created()
                        .map(|t| t.duration_since(std::time::UNIX_EPOCH).unwrap().as_secs())
                        .unwrap_or(0),
                    modified_time: metadata.modified()
                        .map(|t| t.duration_since(std::time::UNIX_EPOCH).unwrap().as_secs())
                        .unwrap_or(0),
                    accessed_time: metadata.accessed()
                        .map(|t| t.duration_since(std::time::UNIX_EPOCH).unwrap().as_secs())
                        .unwrap_or(0),
                };
            }
        }
    }

    FileInfo {
        size: 0,
        is_directory: false,
        is_file: false,
        is_readonly: false,
        created_time: 0,
        modified_time: 0,
        accessed_time: 0,
    }
}

/// Flushes any buffered data to disk
/// Returns 0 on success, -1 on error
pub fn flush(handle: runa_file_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let handle_id = handle as usize;
    if let Ok(mut handles) = FILE_HANDLES.lock() {
        if let Some(file) = handles.get_mut(&handle_id) {
            match file.flush() {
                Ok(_) => 0,
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Checks if a file exists
/// Returns 1 if exists, 0 if not, -1 on error
pub fn exists(path: *const c_char) -> i32 {
    if path.is_null() {
        return -1;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    match std::path::Path::new(path_str).exists() {
        true => 1,
        false => 0,
    }
}

/// Deletes a file
/// Returns 0 on success, -1 on error
pub fn delete(path: *const c_char) -> i32 {
    if path.is_null() {
        return -1;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    match std::fs::remove_file(path_str) {
        Ok(_) => 0,
        Err(_) => -1,
    }
}

/// Creates a directory
/// Returns 0 on success, -1 on error
pub fn create_directory(path: *const c_char) -> i32 {
    if path.is_null() {
        return -1;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    match std::fs::create_dir(path_str) {
        Ok(_) => 0,
        Err(_) => -1,
    }
}

/// Removes a directory
/// Returns 0 on success, -1 on error
pub fn remove_directory(path: *const c_char) -> i32 {
    if path.is_null() {
        return -1;
    }

    let path_str = match unsafe { CStr::from_ptr(path).to_str() } {
        Ok(s) => s,
        Err(_) => return -1,
    };

    match std::fs::remove_dir(path_str) {
        Ok(_) => 0,
        Err(_) => -1,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    use tempfile::NamedTempFile;

    #[test]
    fn test_file_operations() {
        // Create a temporary file for testing
        let temp_file = NamedTempFile::new().unwrap();
        let path = temp_file.path().to_str().unwrap();
        let path_cstr = std::ffi::CString::new(path).unwrap();
        let mode_cstr = std::ffi::CString::new("w").unwrap();

        // Test file opening
        let handle = open(path_cstr.as_ptr(), mode_cstr.as_ptr());
        assert!(!handle.is_null());

        // Test file writing
        let test_data = b"Hello, World!";
        let bytes_written = write(handle, test_data.as_ptr() as *const c_void, test_data.len());
        assert_eq!(bytes_written, test_data.len() as isize);

        // Test file closing
        let close_result = close(handle);
        assert_eq!(close_result, 0);

        // Test file reading
        let mode_read_cstr = std::ffi::CString::new("r").unwrap();
        let read_handle = open(path_cstr.as_ptr(), mode_read_cstr.as_ptr());
        assert!(!read_handle.is_null());

        let mut buffer = [0u8; 13];
        let bytes_read = read(read_handle, buffer.as_mut_ptr() as *mut c_void, buffer.len());
        assert_eq!(bytes_read, test_data.len() as isize);
        assert_eq!(&buffer, test_data);

        close(read_handle);

        // Test file existence
        assert_eq!(exists(path_cstr.as_ptr()), 1);
    }

    #[test]
    fn test_null_handles() {
        assert_eq!(close(std::ptr::null_mut()), -1);
        assert_eq!(read(std::ptr::null_mut(), std::ptr::null_mut(), 0), -1);
        assert_eq!(write(std::ptr::null_mut(), std::ptr::null(), 0), -1);
        assert_eq!(seek(std::ptr::null_mut(), 0, SeekWhence::Start), -1);
        assert_eq!(flush(std::ptr::null_mut()), -1);
    }
} 