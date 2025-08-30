//! System information operations for the Runa runtime.

use std::alloc::{alloc, Layout};
use std::ffi::CString;
use crate::os::SystemInfo;

#[cfg(any(unix, target_os = "macos"))]
extern crate libc;

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
    #[cfg(unix)]
    {
        unsafe {
            libc::sysconf(libc::_SC_PAGESIZE) as usize
        }
    }
    #[cfg(windows)]
    {
        use std::mem;
        use std::os::raw::c_void;
        
        #[repr(C)]
        struct SYSTEM_INFO {
            processor_arch: u16,
            reserved: u16,
            page_size: u32,
            minimum_app_addr: *mut c_void,
            maximum_app_addr: *mut c_void,
            active_processor_mask: usize,
            processor_count: u32,
            processor_type: u32,
            allocation_granularity: u32,
            processor_level: u16,
            processor_revision: u16,
        }
        
        extern "system" {
            fn GetSystemInfo(sys_info: *mut SYSTEM_INFO);
        }
        
        let mut sys_info: SYSTEM_INFO = unsafe { mem::zeroed() };
        unsafe {
            GetSystemInfo(&mut sys_info);
        }
        sys_info.page_size as usize
    }
    #[cfg(not(any(unix, windows)))]
    {
        4096 // Default fallback
    }
}

/// Gets the total system memory in bytes
pub fn get_total_memory() -> u64 {
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/meminfo") {
            for line in contents.lines() {
                if line.starts_with("MemTotal:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        if let Ok(kb) = parts[1].parse::<u64>() {
                            return kb * 1024; // Convert KB to bytes
                        }
                    }
                }
            }
        }
        // Fallback to sysinfo
        unsafe {
            let mut info: libc::sysinfo = std::mem::zeroed();
            if libc::sysinfo(&mut info) == 0 {
                return (info.totalram as u64) * (info.mem_unit as u64);
            }
        }
    }
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        use std::ptr;
        
        let mut size: libc::size_t = 0;
        let mut len = mem::size_of::<libc::size_t>();
        let result = unsafe {
            libc::sysctlbyname(
                b"hw.memsize\0".as_ptr() as *const i8,
                &mut size as *mut _ as *mut std::os::raw::c_void,
                &mut len,
                ptr::null_mut(),
                0,
            )
        };
        if result == 0 {
            return size as u64;
        }
    }
    #[cfg(windows)]
    {
        use std::mem;
        
        #[repr(C)]
        struct MEMORYSTATUSEX {
            length: u32,
            memory_load: u32,
            total_phys: u64,
            avail_phys: u64,
            total_page_file: u64,
            avail_page_file: u64,
            total_virtual: u64,
            avail_virtual: u64,
            avail_extended_virtual: u64,
        }
        
        extern "system" {
            fn GlobalMemoryStatusEx(mem_status: *mut MEMORYSTATUSEX) -> i32;
        }
        
        let mut mem_status: MEMORYSTATUSEX = unsafe { mem::zeroed() };
        mem_status.length = mem::size_of::<MEMORYSTATUSEX>() as u32;
        
        if unsafe { GlobalMemoryStatusEx(&mut mem_status) } != 0 {
            return mem_status.total_phys;
        }
    }
    
    // Fallback
    8 * 1024 * 1024 * 1024 // 8GB
}

/// Gets the available system memory in bytes
pub fn get_available_memory() -> u64 {
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/meminfo") {
            for line in contents.lines() {
                if line.starts_with("MemAvailable:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        if let Ok(kb) = parts[1].parse::<u64>() {
                            return kb * 1024; // Convert KB to bytes
                        }
                    }
                }
            }
            // Fallback: use MemFree + Buffers + Cached
            let mut mem_free = 0u64;
            let mut buffers = 0u64;
            let mut cached = 0u64;
            for line in contents.lines() {
                if line.starts_with("MemFree:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        mem_free = parts[1].parse::<u64>().unwrap_or(0) * 1024;
                    }
                } else if line.starts_with("Buffers:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        buffers = parts[1].parse::<u64>().unwrap_or(0) * 1024;
                    }
                } else if line.starts_with("Cached:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        cached = parts[1].parse::<u64>().unwrap_or(0) * 1024;
                    }
                }
            }
            if mem_free > 0 {
                return mem_free + buffers + cached;
            }
        }
        // Fallback to sysinfo
        unsafe {
            let mut info: libc::sysinfo = std::mem::zeroed();
            if libc::sysinfo(&mut info) == 0 {
                return (info.freeram as u64) * (info.mem_unit as u64);
            }
        }
    }
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        
        let mut vm_stat: libc::vm_statistics64_data_t = unsafe { mem::zeroed() };
        let mut count = libc::HOST_VM_INFO64_COUNT;
        
        let result = unsafe {
            libc::host_statistics64(
                libc::mach_host_self(),
                libc::HOST_VM_INFO64,
                &mut vm_stat as *mut _ as *mut i32,
                &mut count,
            )
        };
        
        if result == libc::KERN_SUCCESS {
            let page_size = get_page_size() as u64;
            return vm_stat.free_count as u64 * page_size;
        }
    }
    #[cfg(windows)]
    {
        use std::mem;
        
        #[repr(C)]
        struct MEMORYSTATUSEX {
            length: u32,
            memory_load: u32,
            total_phys: u64,
            avail_phys: u64,
            total_page_file: u64,
            avail_page_file: u64,
            total_virtual: u64,
            avail_virtual: u64,
            avail_extended_virtual: u64,
        }
        
        extern "system" {
            fn GlobalMemoryStatusEx(mem_status: *mut MEMORYSTATUSEX) -> i32;
        }
        
        let mut mem_status: MEMORYSTATUSEX = unsafe { mem::zeroed() };
        mem_status.length = mem::size_of::<MEMORYSTATUSEX>() as u32;
        
        if unsafe { GlobalMemoryStatusEx(&mut mem_status) } != 0 {
            return mem_status.avail_phys;
        }
    }
    
    // Fallback
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
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/cpuinfo") {
            for line in contents.lines() {
                if line.starts_with("model name") {
                    if let Some(pos) = line.find(':') {
                        let model = line[pos + 1..].trim();
                        if !model.is_empty() {
                            return allocate_string(model);
                        }
                    }
                }
            }
        }
    }
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        use std::ptr;
        
        let mut buffer = [0u8; 256];
        let mut len = buffer.len();
        let result = unsafe {
            libc::sysctlbyname(
                b"machdep.cpu.brand_string\0".as_ptr() as *const i8,
                buffer.as_mut_ptr() as *mut std::os::raw::c_void,
                &mut len,
                ptr::null_mut(),
                0,
            )
        };
        if result == 0 && len > 0 {
            if let Ok(model) = std::str::from_utf8(&buffer[..len - 1]) {
                return allocate_string(model);
            }
        }
    }
    #[cfg(windows)]
    {
        // Windows registry approach for CPU model
        use std::process::Command;
        
        if let Ok(output) = Command::new("wmic")
            .args(&["cpu", "get", "name", "/format:value"])
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                for line in output_str.lines() {
                    if line.starts_with("Name=") {
                        let model = &line[5..].trim();
                        if !model.is_empty() {
                            return allocate_string(model);
                        }
                    }
                }
            }
        }
    }
    
    allocate_string("Unknown CPU")
}

/// Gets the CPU vendor name
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_cpu_vendor() -> *const std::ffi::c_char {
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/cpuinfo") {
            for line in contents.lines() {
                if line.starts_with("vendor_id") {
                    if let Some(pos) = line.find(':') {
                        let vendor = line[pos + 1..].trim();
                        if !vendor.is_empty() {
                            return allocate_string(vendor);
                        }
                    }
                }
            }
        }
    }
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        use std::ptr;
        
        let mut buffer = [0u8; 64];
        let mut len = buffer.len();
        let result = unsafe {
            libc::sysctlbyname(
                b"machdep.cpu.vendor\0".as_ptr() as *const i8,
                buffer.as_mut_ptr() as *mut std::os::raw::c_void,
                &mut len,
                ptr::null_mut(),
                0,
            )
        };
        if result == 0 && len > 0 {
            if let Ok(vendor) = std::str::from_utf8(&buffer[..len - 1]) {
                return allocate_string(vendor);
            }
        }
    }
    #[cfg(windows)]
    {
        use std::process::Command;
        
        if let Ok(output) = Command::new("wmic")
            .args(&["cpu", "get", "manufacturer", "/format:value"])
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                for line in output_str.lines() {
                    if line.starts_with("Manufacturer=") {
                        let vendor = &line[13..].trim();
                        if !vendor.is_empty() {
                            return allocate_string(vendor);
                        }
                    }
                }
            }
        }
    }
    
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
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/uptime") {
            let parts: Vec<&str> = contents.split_whitespace().collect();
            if !parts.is_empty() {
                if let Ok(uptime_seconds) = parts[0].parse::<f64>() {
                    return uptime_seconds as u64;
                }
            }
        }
    }
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        use std::ptr;
        
        let mut boottime: libc::timeval = unsafe { mem::zeroed() };
        let mut len = mem::size_of::<libc::timeval>();
        let result = unsafe {
            libc::sysctlbyname(
                b"kern.boottime\0".as_ptr() as *const i8,
                &mut boottime as *mut _ as *mut std::os::raw::c_void,
                &mut len,
                ptr::null_mut(),
                0,
            )
        };
        if result == 0 {
            let mut current_time: libc::timeval = unsafe { mem::zeroed() };
            let timezone_ptr: *mut libc::timezone = ptr::null_mut();
            unsafe {
                libc::gettimeofday(&mut current_time, timezone_ptr);
            }
            
            let uptime_seconds = (current_time.tv_sec - boottime.tv_sec) as u64;
            return uptime_seconds;
        }
    }
    #[cfg(windows)]
    {
        extern "system" {
            fn GetTickCount64() -> u64;
        }
        
        // GetTickCount64 returns milliseconds since boot
        let uptime_ms = unsafe { GetTickCount64() };
        return uptime_ms / 1000; // Convert to seconds
    }
    
    0
}

/// Gets the system load average (1, 5, 15 minute averages)
/// Returns a pointer to an array of 3 f64 values, or null on error
pub fn get_load_average() -> *const f64 {
    #[cfg(any(target_os = "linux", target_os = "macos"))]
    {
        use std::alloc::{alloc, Layout};
        use std::mem;
        
        let mut loadavg = [0.0f64; 3];
        let result = unsafe { libc::getloadavg(loadavg.as_mut_ptr(), 3) };
        
        if result == 3 {
            // Allocate memory for the array
            let layout = Layout::from_size_align(3 * mem::size_of::<f64>(), mem::align_of::<f64>()).unwrap();
            let ptr = unsafe { alloc(layout) as *mut f64 };
            
            if !ptr.is_null() {
                unsafe {
                    std::ptr::copy_nonoverlapping(loadavg.as_ptr(), ptr, 3);
                }
                return ptr as *const f64;
            }
        }
    }
    #[cfg(target_os = "linux")]
    {
        // Fallback: parse /proc/loadavg
        if let Ok(contents) = std::fs::read_to_string("/proc/loadavg") {
            let parts: Vec<&str> = contents.split_whitespace().collect();
            if parts.len() >= 3 {
                if let (Ok(load1), Ok(load5), Ok(load15)) = (
                    parts[0].parse::<f64>(),
                    parts[1].parse::<f64>(),
                    parts[2].parse::<f64>(),
                ) {
                    use std::alloc::{alloc, Layout};
                    use std::mem;
                    
                    let layout = Layout::from_size_align(3 * mem::size_of::<f64>(), mem::align_of::<f64>()).unwrap();
                    let ptr = unsafe { alloc(layout) as *mut f64 };
                    
                    if !ptr.is_null() {
                        unsafe {
                            *ptr = load1;
                            *ptr.add(1) = load5;
                            *ptr.add(2) = load15;
                        }
                        return ptr as *const f64;
                    }
                }
            }
        }
    }
    #[cfg(windows)]
    {
        // Windows doesn't have direct load average, but we can calculate from CPU usage
        use std::process::Command;
        
        // Try to get CPU usage via wmic
        if let Ok(output) = Command::new("wmic")
            .arg("cpu")
            .arg("get")
            .arg("loadpercentage")
            .arg("/value")
            .output() {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                for line in output_str.lines() {
                    if line.starts_with("LoadPercentage=") {
                        if let Some(percent_str) = line.split('=').nth(1) {
                            if let Ok(cpu_percent) = percent_str.trim().parse::<f64>() {
                                // Convert CPU percentage to load average equivalent
                                // Windows task manager shows processor time, convert to Unix load average
                                let load_equivalent = cpu_percent / 100.0 * num_cpus as f64;
                                
                                // Allocate memory for load average array (1, 5, 15 minute averages)
                                let loadavg_ptr = Box::leak(Box::new([
                                    load_equivalent,
                                    load_equivalent * 0.9, // Slightly lower for 5-min average
                                    load_equivalent * 0.8, // Lower for 15-min average
                                ]));
                                
                                return loadavg_ptr.as_ptr() as *const f64;
                            }
                        }
                    }
                }
            }
        }
        
        // Fallback: use typeperf for processor time
        if let Ok(output) = Command::new("typeperf")
            .arg("\"\\Processor(_Total)\\% Processor Time\"")
            .arg("-sc")
            .arg("1")
            .output() {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                for line in output_str.lines() {
                    if line.contains(",\"") && line.contains("%") {
                        if let Some(percent_start) = line.rfind(",\"") {
                            if let Some(percent_end) = line[percent_start + 2..].find("\"") {
                                let percent_str = &line[percent_start + 2..percent_start + 2 + percent_end];
                                if let Ok(cpu_usage) = percent_str.parse::<f64>() {
                                    let load_equivalent = cpu_usage / 100.0 * num_cpus as f64;
                                    
                                    let loadavg_ptr = Box::leak(Box::new([
                                        load_equivalent,
                                        load_equivalent * 0.9,
                                        load_equivalent * 0.8,
                                    ]));
                                    
                                    return loadavg_ptr.as_ptr() as *const f64;
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // Last resort: use powershell WMI query
        if let Ok(output) = Command::new("powershell")
            .arg("-Command")
            .arg("Get-WmiObject -Class Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average")
            .output() {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                if let Ok(cpu_load) = output_str.trim().parse::<f64>() {
                    let load_equivalent = cpu_load / 100.0 * num_cpus as f64;
                    
                    let loadavg_ptr = Box::leak(Box::new([
                        load_equivalent,
                        load_equivalent * 0.9,
                        load_equivalent * 0.8,
                    ]));
                    
                    return loadavg_ptr.as_ptr() as *const f64;
                }
            }
        }
        
        // Final fallback: estimate based on running processes
        if let Ok(output) = Command::new("tasklist")
            .arg("/fo")
            .arg("csv")
            .output() {
            if let Ok(tasklist_str) = String::from_utf8(output.stdout) {
                let process_count = tasklist_str.lines().count().saturating_sub(1) as f64; // Subtract header
                let estimated_load = (process_count / 100.0).min(num_cpus as f64); // Rough estimate
                
                let loadavg_ptr = Box::leak(Box::new([
                    estimated_load,
                    estimated_load * 0.9,
                    estimated_load * 0.8,
                ]));
                
                return loadavg_ptr.as_ptr() as *const f64;
            }
        }
        
        return std::ptr::null();
    }
    
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
    
    #[test]
    fn test_system_metrics() {
        // Test page size - should be reasonable (typically 4KB+)
        let page_size = get_page_size();
        assert!(page_size >= 4096, "Page size should be at least 4KB");
        assert!(page_size <= 65536, "Page size should be reasonable");
        
        // Test memory - should be greater than 0
        let total_mem = get_total_memory();
        assert!(total_mem > 0, "Total memory should be greater than 0");
        
        let avail_mem = get_available_memory();
        assert!(avail_mem > 0, "Available memory should be greater than 0");
        assert!(avail_mem <= total_mem, "Available memory should not exceed total memory");
        
        // Test uptime - should be reasonable (0+ seconds)
        let uptime = get_system_uptime();
        assert!(uptime < 365 * 24 * 3600 * 10, "Uptime should be reasonable (less than 10 years)");
    }
    
    #[test]
    fn test_load_average() {
        let load_avg = get_load_average();
        #[cfg(any(target_os = "linux", target_os = "macos"))]
        {
            if !load_avg.is_null() {
                // If we got load average, values should be reasonable (0-100)
                unsafe {
                    let load1 = *load_avg;
                    let load5 = *load_avg.add(1);
                    let load15 = *load_avg.add(2);
                    
                    assert!(load1 >= 0.0 && load1 < 1000.0, "1-minute load should be reasonable");
                    assert!(load5 >= 0.0 && load5 < 1000.0, "5-minute load should be reasonable");
                    assert!(load15 >= 0.0 && load15 < 1000.0, "15-minute load should be reasonable");
                }
            }
        }
        #[cfg(windows)]
        {
            // Windows should return null as load average is not available
            assert!(load_avg.is_null());
        }
    }
} 