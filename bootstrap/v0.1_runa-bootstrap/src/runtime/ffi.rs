// Foreign Function Interface support for the bootstrap compiler

use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int, c_void};

// FFI function registry
pub struct FfiRegistry {
    // In a real implementation, this would contain function pointers
    // and type information for external functions
}

impl FfiRegistry {
    pub fn new() -> Self {
        Self {}
    }
    
    pub fn register_function(&mut self, _name: &str, _ptr: *const c_void) {
        // TODO: Implement function registration
    }
    
    pub fn call_function(&self, _name: &str, _args: &[*const c_void]) -> Result<*const c_void, String> {
        // TODO: Implement dynamic function calling
        Err("FFI not yet implemented".to_string())
    }
}

// Basic C string utilities
pub fn rust_string_to_c_string(s: &str) -> Result<CString, std::ffi::NulError> {
    CString::new(s)
}

pub unsafe fn c_string_to_rust_string(ptr: *const c_char) -> Result<String, std::str::Utf8Error> {
    let cstr = CStr::from_ptr(ptr);
    cstr.to_str().map(|s| s.to_string())
}

// Basic type marshaling
#[repr(C)]
pub struct FfiValue {
    pub tag: c_int,
    pub data: FfiData,
}

#[repr(C)]
pub union FfiData {
    pub int_val: i64,
    pub float_val: f64,
    pub ptr_val: *mut c_void,
    pub bool_val: bool,
}

impl FfiValue {
    pub fn from_int(value: i64) -> Self {
        Self {
            tag: 0,
            data: FfiData { int_val: value },
        }
    }
    
    pub fn from_float(value: f64) -> Self {
        Self {
            tag: 1,
            data: FfiData { float_val: value },
        }
    }
    
    pub fn from_ptr(value: *mut c_void) -> Self {
        Self {
            tag: 2,
            data: FfiData { ptr_val: value },
        }
    }
    
    pub fn from_bool(value: bool) -> Self {
        Self {
            tag: 3,
            data: FfiData { bool_val: value },
        }
    }
    
    pub unsafe fn as_int(&self) -> i64 {
        self.data.int_val
    }
    
    pub unsafe fn as_float(&self) -> f64 {
        self.data.float_val
    }
    
    pub unsafe fn as_ptr(&self) -> *mut c_void {
        self.data.ptr_val
    }
    
    pub unsafe fn as_bool(&self) -> bool {
        self.data.bool_val
    }
}