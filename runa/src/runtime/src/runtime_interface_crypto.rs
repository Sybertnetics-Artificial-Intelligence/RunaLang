//! Cryptography Runtime Operations
//!
//! This module implements the 3 cryptography system calls that provide
//! secure random number generation, cryptographic hashing, and entropy collection.
//! These are the core primitives that the Runa stdlib crypto modules build upon.

use std::ffi::{c_char, CStr, CString};
use std::ptr;
use rand::{RngCore, thread_rng};
use sha2::{Sha256, Sha512, Digest};
use sha1::Sha1;
use md5::Md5;

// ============================================================================
// CRYPTOGRAPHY TYPE DEFINITIONS
// ============================================================================

/// Bytes array structure for crypto operations
#[repr(C)]
pub struct RunaBytes {
    pub data: *mut u8,
    pub length: usize,
}

// ============================================================================
// CRYPTOGRAPHY CORE OPERATIONS (3 functions)
// ============================================================================

/// system_call_random_bytes: Generate cryptographically secure random bytes
/// Maps to: system_call_random_bytes(count: Integer) -> Bytes
#[no_mangle]
pub extern "C" fn system_call_random_bytes(count: usize) -> RunaBytes {
    if count == 0 || count > 1_048_576 { // Limit to 1MB for safety
        return RunaBytes {
            data: ptr::null_mut(),
            length: 0,
        };
    }

    let mut buffer = vec![0u8; count];
    
    // Use thread_rng() which is cryptographically secure
    // Removed panic handling to avoid unwind safety issues
    thread_rng().fill_bytes(&mut buffer);
    {
            let data_ptr = buffer.as_mut_ptr();
            std::mem::forget(buffer); // Prevent deallocation - caller must free
            
            RunaBytes {
                data: data_ptr,
                length: count,
            }
    }
}

/// system_call_crypto_hash: Compute cryptographic hash of data
/// Maps to: system_call_crypto_hash(data: Bytes, algorithm: String) -> Bytes
#[no_mangle]
pub extern "C" fn system_call_crypto_hash(
    data: *const u8,
    data_length: usize,
    algorithm: *const c_char,
) -> RunaBytes {
    let empty_result = RunaBytes {
        data: ptr::null_mut(),
        length: 0,
    };

    if data.is_null() || data_length == 0 || algorithm.is_null() {
        return empty_result;
    }

    let algorithm_str = match unsafe { CStr::from_ptr(algorithm).to_str() } {
        Ok(s) => s.to_lowercase(),
        Err(_) => return empty_result,
    };

    let data_slice = unsafe { std::slice::from_raw_parts(data, data_length) };

    match algorithm_str.as_str() {
        "md5" => {
            let mut hasher = Md5::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        "sha1" => {
            let mut hasher = Sha1::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        "sha256" => {
            let mut hasher = Sha256::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        "sha512" => {
            let mut hasher = Sha512::new();
            hasher.update(data_slice);
            let result = hasher.finalize();
            let mut hash_vec = result.to_vec();
            let data_ptr = hash_vec.as_mut_ptr();
            let length = hash_vec.len();
            std::mem::forget(hash_vec);
            
            RunaBytes {
                data: data_ptr,
                length,
            }
        }
        _ => empty_result, // Unsupported algorithm
    }
}

/// system_call_entropy_collect: Collect system entropy for random generation
/// Maps to: system_call_entropy_collect() -> Bytes
#[no_mangle]
pub extern "C" fn system_call_entropy_collect() -> RunaBytes {
    // Collect entropy from various system sources
    let mut entropy_sources = Vec::new();
    
    // High-resolution timestamp
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default();
    entropy_sources.extend_from_slice(&now.as_nanos().to_le_bytes());
    
    // Process ID
    entropy_sources.extend_from_slice(&std::process::id().to_le_bytes());
    
    // Thread ID (approximation) - use simple hash instead of unstable API
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    let mut hasher = DefaultHasher::new();
    std::thread::current().id().hash(&mut hasher);
    entropy_sources.extend_from_slice(&hasher.finish().to_le_bytes());
    
    // Memory address of stack variable (ASLR entropy)
    let stack_var = 0u64;
    let stack_addr = &stack_var as *const u64 as usize;
    entropy_sources.extend_from_slice(&stack_addr.to_le_bytes());
    
    // System-specific entropy
    #[cfg(unix)]
    {
        // Try to read from /dev/urandom if available
        if let Ok(mut file) = std::fs::File::open("/dev/urandom") {
            let mut random_bytes = [0u8; 32];
            if let Ok(_) = std::io::Read::read_exact(&mut file, &mut random_bytes) {
                entropy_sources.extend_from_slice(&random_bytes);
            }
        }
        
        // Add some process information
        entropy_sources.extend_from_slice(&std::process::id().to_le_bytes());
    }
    
    #[cfg(windows)]
    {
        // Use Windows-specific entropy sources
        use std::arch::x86_64::_rdtsc;
        
        // CPU timestamp counter (if available)
        unsafe {
            let tsc = _rdtsc();
            entropy_sources.extend_from_slice(&tsc.to_le_bytes());
        }
    }
    
    // Hash the collected entropy to produce uniform output
    let mut hasher = Sha256::new();
    hasher.update(&entropy_sources);
    let result = hasher.finalize();
    
    let mut entropy_vec = result.to_vec();
    let data_ptr = entropy_vec.as_mut_ptr();
    let length = entropy_vec.len();
    std::mem::forget(entropy_vec);
    
    RunaBytes {
        data: data_ptr,
        length,
    }
}

// ============================================================================
// ADDITIONAL CRYPTO SYSTEM CALLS (Extended Interface)
// ============================================================================

/// Get supported hash algorithms
#[no_mangle]
pub extern "C" fn system_call_crypto_algorithms(
    algorithms_out: *mut *const c_char,
    count_out: *mut usize,
) -> bool {
    if algorithms_out.is_null() || count_out.is_null() {
        return false;
    }

    let supported_algorithms = vec![
        "md5",
        "sha1", 
        "sha256",
        "sha512",
    ];
    
    let mut algorithm_ptrs = Vec::new();
    for algorithm in supported_algorithms {
        if let Ok(c_string) = CString::new(algorithm) {
            algorithm_ptrs.push(c_string.into_raw());
        }
    }
    
    let count = algorithm_ptrs.len();
    let algorithms_ptr = algorithm_ptrs.as_ptr();
    std::mem::forget(algorithm_ptrs);
    
    unsafe {
        *algorithms_out = algorithms_ptr as *const c_char;
        *count_out = count;
    }
    
    true
}

/// Secure memory comparison (constant-time)
#[no_mangle]
pub extern "C" fn system_call_crypto_secure_compare(
    data1: *const u8,
    data1_len: usize,
    data2: *const u8,
    data2_len: usize,
) -> bool {
    if data1.is_null() || data2.is_null() || data1_len != data2_len {
        return false;
    }
    
    let slice1 = unsafe { std::slice::from_raw_parts(data1, data1_len) };
    let slice2 = unsafe { std::slice::from_raw_parts(data2, data2_len) };
    
    // Constant-time comparison to prevent timing attacks
    let mut result = 0u8;
    for i in 0..data1_len {
        result |= slice1[i] ^ slice2[i];
    }
    
    result == 0
}

/// Secure memory wipe (overwrite with zeros)
#[no_mangle]
pub extern "C" fn system_call_crypto_secure_wipe(data: *mut u8, length: usize) -> bool {
    if data.is_null() || length == 0 {
        return false;
    }
    
    let data_slice = unsafe { std::slice::from_raw_parts_mut(data, length) };
    
    // Overwrite with zeros multiple times to ensure data is cleared
    for _ in 0..3 {
        for byte in data_slice.iter_mut() {
            *byte = 0;
        }
        
        // Memory fence to prevent compiler optimization
        std::sync::atomic::fence(std::sync::atomic::Ordering::SeqCst);
    }
    
    true
}

// ============================================================================
// CRYPTO HELPER FUNCTIONS
// ============================================================================

/// Validate hash algorithm name
#[allow(dead_code)]
fn is_supported_algorithm(algorithm: &str) -> bool {
    matches!(algorithm, "md5" | "sha1" | "sha256" | "sha512")
}

/// Get expected hash length for algorithm
#[allow(dead_code)]
fn get_hash_length(algorithm: &str) -> usize {
    match algorithm {
        "md5" => 16,
        "sha1" => 20,
        "sha256" => 32,
        "sha512" => 64,
        _ => 0,
    }
}

// ============================================================================
// MEMORY MANAGEMENT FOR CRYPTO OPERATIONS
// ============================================================================

/// Free bytes array allocated by crypto operations
#[no_mangle]
pub extern "C" fn runa_free_crypto_bytes(bytes: RunaBytes) {
    if !bytes.data.is_null() && bytes.length > 0 {
        unsafe {
            let _ = Vec::from_raw_parts(bytes.data, bytes.length, bytes.length);
        }
    }
}

/// Free algorithm names array
#[no_mangle]
pub extern "C" fn runa_free_crypto_algorithms(algorithms: *mut *mut c_char, count: usize) {
    if !algorithms.is_null() && count > 0 {
        unsafe {
            for i in 0..count {
                let str_ptr = *algorithms.add(i);
                if !str_ptr.is_null() {
                    let _ = CString::from_raw(str_ptr);
                }
            }
            let _ = Vec::from_raw_parts(algorithms, count, count);
        }
    }
}

// ============================================================================
// CRYPTO TESTING AND VALIDATION
// ============================================================================

/// Test crypto system functionality
#[no_mangle]
pub extern "C" fn test_crypto_system() -> bool {
    // Test random bytes generation
    let random_bytes = system_call_random_bytes(32);
    if random_bytes.data.is_null() || random_bytes.length != 32 {
        runa_free_crypto_bytes(random_bytes);
        return false;
    }
    runa_free_crypto_bytes(random_bytes);
    
    // Test hashing
    let test_data = b"Hello, World!";
    let algorithm = CString::new("sha256").unwrap();
    let hash_result = system_call_crypto_hash(
        test_data.as_ptr(),
        test_data.len(),
        algorithm.as_ptr(),
    );
    
    if hash_result.data.is_null() || hash_result.length != 32 {
        runa_free_crypto_bytes(hash_result);
        return false;
    }
    runa_free_crypto_bytes(hash_result);
    
    // Test entropy collection
    let entropy = system_call_entropy_collect();
    if entropy.data.is_null() || entropy.length == 0 {
        runa_free_crypto_bytes(entropy);
        return false;
    }
    runa_free_crypto_bytes(entropy);
    
    true
}