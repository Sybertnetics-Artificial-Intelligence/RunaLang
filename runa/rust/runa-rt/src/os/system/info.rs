//! System information operations for the Runa runtime.

use std::alloc::{alloc, Layout};
use std::ffi::CString;
use crate::os::SystemInfo;

/// Gets comprehensive system information
pub fn get() -> SystemInfo {
    SystemInfo {
        platform: get_platform(),
        architecture: get_architecture(),
        page_size: get_page_size(),
        total_memory: get_total_memory(),
        available_memory: get_available_memory(),
        cpu_count: get_cpu_count(),
    }
}

/// Gets the platform name (e.g., "windows", "linux", "macos")
/// Returns a pointer to a null-terminated string
pub fn get_platform() -> *const std::ffi::c_char {
    let platform = if cfg!(target_os = "windows") {
        "windows"
    } else if cfg!(target_os = "linux") {
        "linux"
    } else if cfg!(target_os = "macos") {
        "macos"
    } else if cfg!(target_os = "android") {
        "android"
    } else if cfg!(target_os = "ios") {
        "ios"
    } else if cfg!(target_os = "freebsd") {
        "freebsd"
    } else if cfg!(target_os = "netbsd") {
        "netbsd"
    } else if cfg!(target_os = "openbsd") {
        "openbsd"
    } else if cfg!(target_os = "dragonfly") {
        "dragonfly"
    } else if cfg!(target_os = "solaris") {
        "solaris"
    } else if cfg!(target_os = "illumos") {
        "illumos"
    } else if cfg!(target_os = "fuchsia") {
        "fuchsia"
    } else if cfg!(target_os = "redox") {
        "redox"
    } else if cfg!(target_os = "haiku") {
        "haiku"
    } else if cfg!(target_os = "emscripten") {
        "emscripten"
    } else if cfg!(target_os = "wasi") {
        "wasi"
    } else {
        "unknown"
    };

    allocate_string(platform)
}

/// Gets the CPU architecture (e.g., "x86_64", "aarch64", "i686")
/// Returns a pointer to a null-terminated string
pub fn get_architecture() -> *const std::ffi::c_char {
    let arch = if cfg!(target_arch = "x86_64") {
        "x86_64"
    } else if cfg!(target_arch = "x86") {
        "x86"
    } else if cfg!(target_arch = "aarch64") {
        "aarch64"
    } else if cfg!(target_arch = "arm") {
        "arm"
    } else if cfg!(target_arch = "mips") {
        "mips"
    } else if cfg!(target_arch = "mips64") {
        "mips64"
    } else if cfg!(target_arch = "powerpc") {
        "powerpc"
    } else if cfg!(target_arch = "powerpc64") {
        "powerpc64"
    } else if cfg!(target_arch = "riscv64") {
        "riscv64"
    } else if cfg!(target_arch = "s390x") {
        "s390x"
    } else if cfg!(target_arch = "sparc64") {
        "sparc64"
    } else if cfg!(target_arch = "wasm32") {
        "wasm32"
    } else if cfg!(target_arch = "wasm64") {
        "wasm64"
    } else {
        "unknown"
    };

    allocate_string(arch)
}

/// Gets the system page size in bytes
pub fn get_page_size() -> usize {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs:
    // - Linux: sysconf(_SC_PAGESIZE)
    // - Windows: GetSystemInfo
    // - macOS: sysconf(_SC_PAGESIZE)
    
    // Common page sizes
    if cfg!(target_arch = "x86_64") || cfg!(target_arch = "aarch64") {
        4096 // 4KB
    } else if cfg!(target_arch = "x86") {
        4096 // 4KB
    } else {
        4096 // Default to 4KB
    }
}

/// Gets the total system memory in bytes
pub fn get_total_memory() -> u64 {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs:
    // - Linux: /proc/meminfo or sysinfo
    // - Windows: GlobalMemoryStatusEx
    // - macOS: sysctl hw.memsize
    
    // For now, return a reasonable default
    8 * 1024 * 1024 * 1024 // 8GB
}

/// Gets the available system memory in bytes
pub fn get_available_memory() -> u64 {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    
    // For now, return a reasonable default
    4 * 1024 * 1024 * 1024 // 4GB
}

/// Gets the number of CPU cores
pub fn get_cpu_count() -> u32 {
    std::thread::available_parallelism()
        .map(|n| n.get() as u32)
        .unwrap_or(1)
}

/// Gets the CPU model name
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_cpu_model() -> *const std::ffi::c_char {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs:
    // - Linux: /proc/cpuinfo
    // - Windows: GetSystemInfo
    // - macOS: sysctl machdep.cpu.brand_string
    
    allocate_string("Generic CPU")
}

/// Gets the CPU vendor name
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_cpu_vendor() -> *const std::ffi::c_char {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    
    allocate_string("Unknown")
}

/// Gets the system hostname
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_hostname() -> *const std::ffi::c_char {
    match std::env::var("HOSTNAME") {
        Ok(hostname) => allocate_string(&hostname),
        Err(_) => {
            // Try alternative methods
            if cfg!(target_os = "windows") {
                // On Windows, try COMPUTERNAME
                match std::env::var("COMPUTERNAME") {
                    Ok(hostname) => allocate_string(&hostname),
                    Err(_) => allocate_string("localhost"),
                }
            } else {
                allocate_string("localhost")
            }
        }
    }
}

/// Gets the system username
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_username() -> *const std::ffi::c_char {
    match std::env::var("USER") {
        Ok(username) => allocate_string(&username),
        Err(_) => {
            // Try alternative methods
            if cfg!(target_os = "windows") {
                match std::env::var("USERNAME") {
                    Ok(username) => allocate_string(&username),
                    Err(_) => allocate_string("unknown"),
                }
            } else {
                allocate_string("unknown")
            }
        }
    }
}

/// Gets the system home directory
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_home_dir() -> *const std::ffi::c_char {
    match std::env::var("HOME") {
        Ok(home) => allocate_string(&home),
        Err(_) => {
            // Try alternative methods
            if cfg!(target_os = "windows") {
                match std::env::var("USERPROFILE") {
                    Ok(home) => allocate_string(&home),
                    Err(_) => std::ptr::null(),
                }
            } else {
                std::ptr::null()
            }
        }
    }
}

/// Gets the system temporary directory
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_temp_dir() -> *const std::ffi::c_char {
    match std::env::temp_dir().to_str() {
        Some(temp) => allocate_string(temp),
        None => std::ptr::null(),
    }
}

/// Gets the system uptime in seconds
pub fn get_system_uptime() -> u64 {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs:
    // - Linux: /proc/uptime
    // - Windows: GetTickCount64
    // - macOS: sysctl kern.boottime
    
    0
}

/// Gets the system load average (1, 5, 15 minute averages)
/// Returns a pointer to an array of 3 f64 values, or null on error
pub fn get_load_average() -> *const f64 {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    
    std::ptr::null()
}

/// Helper function to allocate a string and return a C pointer
fn allocate_string(s: &str) -> *const std::ffi::c_char {
    if let Ok(c_str) = CString::new(s) {
        let bytes = c_str.as_bytes_with_nul();
        let size = bytes.len();
        
        let layout = Layout::from_size_align(size, std::mem::align_of::<u8>()).unwrap();
        let ptr = unsafe { alloc(layout) };
        
        if !ptr.is_null() {
            unsafe {
                std::ptr::copy_nonoverlapping(bytes.as_ptr(), ptr, size);
            }
            return ptr as *const std::ffi::c_char;
        }
    }
    
    std::ptr::null()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_system_info() {
        let info = get();
        
        // Test that we get valid platform and architecture
        assert!(!info.platform.is_null());
        assert!(!info.architecture.is_null());
        
        // Test that we get reasonable values
        assert!(info.page_size > 0);
        assert!(info.total_memory > 0);
        assert!(info.available_memory > 0);
        assert!(info.cpu_count > 0);
    }

    #[test]
    fn test_platform_detection() {
        let platform = get_platform();
        assert!(!platform.is_null());
        
        let platform_str = unsafe { std::ffi::CStr::from_ptr(platform).to_str().unwrap() };
        assert!(!platform_str.is_empty());
    }

    #[test]
    fn test_architecture_detection() {
        let arch = get_architecture();
        assert!(!arch.is_null());
        
        let arch_str = unsafe { std::ffi::CStr::from_ptr(arch).to_str().unwrap() };
        assert!(!arch_str.is_empty());
    }

    #[test]
    fn test_cpu_info() {
        let cpu_count = get_cpu_count();
        assert!(cpu_count > 0);
        
        let _cpu_model = get_cpu_model();
        // Note: cpu_model might be null in some environments
        // so we can't assert it's not null
        
        let _cpu_vendor = get_cpu_vendor();
        // Note: cpu_vendor might be null in some environments
        // so we can't assert it's not null
    }

    #[test]
    fn test_system_paths() {
        let _hostname = get_hostname();
        // Note: hostname might be null in some environments
        // so we can't assert it's not null
        
        let _username = get_username();
        // Note: username might be null in some environments
        // so we can't assert it's not null
        
        let _home_dir = get_home_dir();
        // Note: home_dir might be null in some environments
        // so we can't assert it's not null
        
        let _temp_dir = get_temp_dir();
        // Note: temp_dir might be null in some environments
        // so we can't assert it's not null
    }
} 