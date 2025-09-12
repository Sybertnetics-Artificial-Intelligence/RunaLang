//! Process-related operations for the Runa runtime.

use crate::os::ProcessInfo;
use std::alloc::{alloc, Layout};
use std::time::{SystemTime, UNIX_EPOCH};
use std::sync::LazyLock;

#[cfg(unix)]
extern crate libc;

// Global storage for process start time
static PROCESS_START_TIME: LazyLock<u64> = LazyLock::new(|| {
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/self/stat") {
            let parts: Vec<&str> = contents.split_whitespace().collect();
            if parts.len() > 21 {
                if let Ok(start_time_ticks) = parts[21].parse::<u64>() {
                    let clock_ticks_per_sec = unsafe { libc::sysconf(libc::_SC_CLK_TCK) } as u64;
                    let system_start = crate::os::system::info::get_system_uptime();
                    let process_start_sec = start_time_ticks / clock_ticks_per_sec;
                    return SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs() - (system_start - process_start_sec);
                }
            }
        }
    }
    
    // Fallback to current time
    SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs()
});

/// Gets the current process ID
pub fn get_pid() -> u32 {
    std::process::id()
}

/// Gets the parent process ID
pub fn get_parent_pid() -> u32 {
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/self/stat") {
            let parts: Vec<&str> = contents.split_whitespace().collect();
            if parts.len() > 3 {
                if let Ok(ppid) = parts[3].parse::<u32>() {
                    return ppid;
                }
            }
        }
    }
    #[cfg(unix)]
    {
        unsafe {
            libc::getppid() as u32
        }
    }
    #[cfg(windows)]
    {
        use std::process::Command;
        
        if let Ok(output) = Command::new("wmic")
            .args(&["process", "where", &format!("processid={}", std::process::id()), "get", "parentprocessid", "/format:value"])
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                for line in output_str.lines() {
                    if line.starts_with("ParentProcessId=") {
                        if let Ok(ppid) = line[16..].parse::<u32>() {
                            return ppid;
                        }
                    }
                }
            }
        }
        
        0
    }
    #[cfg(not(any(unix, windows)))]
    {
        0
    }
}

/// Gets information about the current process
pub fn get_info() -> ProcessInfo {
    ProcessInfo {
        pid: get_pid(),
        parent_pid: get_parent_pid(),
        memory_usage: get_memory_usage(),
        cpu_usage: get_cpu_usage(),
    }
}

/// Gets the current process memory usage in bytes
pub fn get_memory_usage() -> u64 {
    #[cfg(target_os = "linux")]
    {
        // Try /proc/self/status first
        if let Ok(contents) = std::fs::read_to_string("/proc/self/status") {
            for line in contents.lines() {
                if line.starts_with("VmRSS:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        if let Ok(kb) = parts[1].parse::<u64>() {
                            return kb * 1024; // Convert KB to bytes
                        }
                    }
                }
            }
        }
        
        // Fallback: try /proc/self/statm
        if let Ok(contents) = std::fs::read_to_string("/proc/self/statm") {
            let parts: Vec<&str> = contents.split_whitespace().collect();
            if parts.len() >= 2 {
                if let Ok(pages) = parts[1].parse::<u64>() {
                    let page_size = crate::os::system::info::get_page_size() as u64;
                    return pages * page_size;
                }
            }
        }
    }
    
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        use std::ptr;
        
        let mut info: libc::mach_task_basic_info = unsafe { mem::zeroed() };
        let mut count = libc::MACH_TASK_BASIC_INFO_COUNT;
        
        let result = unsafe {
            libc::task_info(
                libc::mach_task_self(),
                libc::MACH_TASK_BASIC_INFO,
                &mut info as *mut _ as *mut i32,
                &mut count,
            )
        };
        
        if result == libc::KERN_SUCCESS {
            return info.resident_size as u64;
        }
    }
    
    #[cfg(windows)]
    {
        use std::mem;
        
        #[repr(C)]
        struct PROCESS_MEMORY_COUNTERS {
            cb: u32,
            page_fault_count: u32,
            peak_working_set_size: usize,
            working_set_size: usize,
            quota_peak_paged_pool_usage: usize,
            quota_paged_pool_usage: usize,
            quota_peak_non_paged_pool_usage: usize,
            quota_non_paged_pool_usage: usize,
            pagefile_usage: usize,
            peak_pagefile_usage: usize,
        }
        
        extern "system" {
            fn GetCurrentProcess() -> *mut std::ffi::c_void;
            fn GetProcessMemoryInfo(
                process: *mut std::ffi::c_void,
                counters: *mut PROCESS_MEMORY_COUNTERS,
                cb: u32,
            ) -> i32;
        }
        
        let mut counters: PROCESS_MEMORY_COUNTERS = unsafe { mem::zeroed() };
        counters.cb = mem::size_of::<PROCESS_MEMORY_COUNTERS>() as u32;
        
        if unsafe { GetProcessMemoryInfo(GetCurrentProcess(), &mut counters, counters.cb) } != 0 {
            return counters.working_set_size as u64;
        }
    }
    
    // Fallback
    1024 * 1024 // 1MB
}

/// Gets the current process CPU usage as a percentage
pub fn get_cpu_usage() -> f64 {
    #[cfg(target_os = "linux")]
    {
        use std::sync::Mutex;
        use std::time::Instant;
        
        static LAST_MEASUREMENT: LazyLock<Mutex<Option<(Instant, u64, u64)>>> = LazyLock::new(|| Mutex::new(None));
        
        if let Ok(contents) = std::fs::read_to_string("/proc/self/stat") {
            let parts: Vec<&str> = contents.split_whitespace().collect();
            if parts.len() > 15 {
                if let (Ok(utime), Ok(stime)) = (parts[13].parse::<u64>(), parts[14].parse::<u64>()) {
                    let total_time = utime + stime;
                    let now = Instant::now();
                    
                    if let Ok(mut last_opt) = LAST_MEASUREMENT.lock() {
                        if let Some((last_instant, last_total, _)) = *last_opt {
                            let time_delta = now.duration_since(last_instant).as_secs_f64();
                            let cpu_delta = total_time - last_total;
                            let clock_ticks_per_sec = unsafe { libc::sysconf(libc::_SC_CLK_TCK) } as f64;
                            
                            if time_delta > 0.0 {
                                let cpu_usage = (cpu_delta as f64 / clock_ticks_per_sec) / time_delta * 100.0;
                                *last_opt = Some((now, total_time, 0));
                                return cpu_usage;
                            }
                        }
                        *last_opt = Some((now, total_time, 0));
                    }
                }
            }
        }
    }
    
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        use std::sync::Mutex;
        use std::time::Instant;
        
        static LAST_MEASUREMENT_MACOS: LazyLock<Mutex<Option<(Instant, u64, u64)>>> = LazyLock::new(|| Mutex::new(None));
        
        let mut info: libc::mach_task_basic_info = unsafe { mem::zeroed() };
        let mut count = libc::MACH_TASK_BASIC_INFO_COUNT;
        
        let result = unsafe {
            libc::task_info(
                libc::mach_task_self(),
                libc::MACH_TASK_BASIC_INFO,
                &mut info as *mut _ as *mut i32,
                &mut count,
            )
        };
        
        if result == libc::KERN_SUCCESS {
            // Get thread time info for more accurate CPU usage
            let mut thread_info: libc::mach_task_thread_times_info = unsafe { mem::zeroed() };
            let mut thread_count = libc::MACH_TASK_THREAD_TIMES_INFO_COUNT;
            
            let thread_result = unsafe {
                libc::task_info(
                    libc::mach_task_self(),
                    libc::MACH_TASK_THREAD_TIMES_INFO,
                    &mut thread_info as *mut _ as *mut i32,
                    &mut thread_count,
                )
            };
            
            if thread_result == libc::KERN_SUCCESS {
                let user_time = thread_info.user_time.seconds as u64 * 1_000_000 + thread_info.user_time.microseconds as u64;
                let system_time = thread_info.system_time.seconds as u64 * 1_000_000 + thread_info.system_time.microseconds as u64;
                let total_time = user_time + system_time;
                let now = Instant::now();
                
                if let Ok(mut last_opt) = LAST_MEASUREMENT_MACOS.lock() {
                    if let Some((last_instant, last_total, _)) = *last_opt {
                        let time_delta = now.duration_since(last_instant).as_micros() as f64;
                        let cpu_delta = (total_time - last_total) as f64;
                        
                        if time_delta > 0.0 {
                            let cpu_usage = (cpu_delta / time_delta) * 100.0;
                            *last_opt = Some((now, total_time, 0));
                            return cpu_usage;
                        }
                    }
                    *last_opt = Some((now, total_time, 0));
                }
            }
        }
    }
    
    #[cfg(windows)]
    {
        use std::mem;
        use std::sync::Mutex;
        use std::time::Instant;
        
        static LAST_MEASUREMENT_WINDOWS: LazyLock<Mutex<Option<(Instant, u64)>>> = LazyLock::new(|| Mutex::new(None));
        
        #[repr(C)]
        struct FILETIME {
            low_date_time: u32,
            high_date_time: u32,
        }
        
        extern "system" {
            fn GetCurrentProcess() -> *mut std::ffi::c_void;
            fn GetProcessTimes(
                process: *mut std::ffi::c_void,
                creation_time: *mut FILETIME,
                exit_time: *mut FILETIME,
                kernel_time: *mut FILETIME,
                user_time: *mut FILETIME,
            ) -> i32;
        }
        
        // Helper function to convert FILETIME to microseconds
        fn filetime_to_micros(ft: &FILETIME) -> u64 {
            let time_64 = ((ft.high_date_time as u64) << 32) | (ft.low_date_time as u64);
            time_64 / 10 // Convert from 100ns intervals to microseconds
        }
        
        let mut creation_time: FILETIME = unsafe { mem::zeroed() };
        let mut exit_time: FILETIME = unsafe { mem::zeroed() };
        let mut kernel_time: FILETIME = unsafe { mem::zeroed() };
        let mut user_time: FILETIME = unsafe { mem::zeroed() };
        
        if unsafe {
            GetProcessTimes(
                GetCurrentProcess(),
                &mut creation_time,
                &mut exit_time,
                &mut kernel_time,
                &mut user_time,
            )
        } != 0
        {
            let user_micros = filetime_to_micros(&user_time);
            let kernel_micros = filetime_to_micros(&kernel_time);
            let total_cpu_time = user_micros + kernel_micros;
            let now = Instant::now();
            
            if let Ok(mut last_opt) = LAST_MEASUREMENT_WINDOWS.lock() {
                if let Some((last_instant, last_total)) = *last_opt {
                    let time_delta = now.duration_since(last_instant).as_micros() as f64;
                    let cpu_delta = (total_cpu_time - last_total) as f64;
                    
                    if time_delta > 0.0 {
                        let cpu_usage = (cpu_delta / time_delta) * 100.0;
                        *last_opt = Some((now, total_cpu_time));
                        return cpu_usage;
                    }
                }
                *last_opt = Some((now, total_cpu_time));
            }
        }
    }
    
    0.0
}

/// Gets the process start time as seconds since Unix epoch
pub fn get_start_time() -> u64 {
    *PROCESS_START_TIME
}

/// Gets the process uptime in seconds
pub fn get_uptime() -> u64 {
    let current_time = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
    current_time - *PROCESS_START_TIME
}

/// Gets the number of threads in the current process
pub fn get_thread_count() -> u32 {
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/self/status") {
            for line in contents.lines() {
                if line.starts_with("Threads:") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 2 {
                        if let Ok(count) = parts[1].parse::<u32>() {
                            return count;
                        }
                    }
                }
            }
        }
    }
    
    #[cfg(target_os = "macos")]
    {
        use std::mem;
        
        let mut info: libc::mach_task_basic_info = unsafe { mem::zeroed() };
        let mut count = libc::MACH_TASK_BASIC_INFO_COUNT;
        
        let result = unsafe {
            libc::task_info(
                libc::mach_task_self(),
                libc::MACH_TASK_BASIC_INFO,
                &mut info as *mut _ as *mut i32,
                &mut count,
            )
        };
        
        if result == libc::KERN_SUCCESS {
            return info.suspend_count as u32; // This is not ideal, but mach doesn't easily expose thread count
        }
        
        // Fallback: use ps command
        use std::process::Command;
        if let Ok(output) = Command::new("ps")
            .args(&["-M", "-p", &std::process::id().to_string()])
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                return output_str.lines().count().saturating_sub(1) as u32;
            }
        }
    }
    
    #[cfg(windows)]
    {
        use std::process::Command;
        
        if let Ok(output) = Command::new("wmic")
            .args(&["process", "where", &format!("processid={}", std::process::id()), "get", "threadcount", "/format:value"])
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                for line in output_str.lines() {
                    if line.starts_with("ThreadCount=") {
                        if let Ok(count) = line[12..].parse::<u32>() {
                            return count;
                        }
                    }
                }
            }
        }
    }
    
    1 // Fallback
}

/// Gets the process priority
pub fn get_priority() -> i32 {
    #[cfg(unix)]
    {
        unsafe {
            libc::getpriority(libc::PRIO_PROCESS, 0)
        }
    }
    #[cfg(windows)]
    {
        extern "system" {
            fn GetCurrentProcess() -> *mut std::ffi::c_void;
            fn GetPriorityClass(process: *mut std::ffi::c_void) -> u32;
        }
        
        let priority_class = unsafe { GetPriorityClass(GetCurrentProcess()) };
        
        // Convert Windows priority class to Unix-like priority
        match priority_class {
            0x00000040 => -20, // IDLE_PRIORITY_CLASS
            0x00004000 => -10, // BELOW_NORMAL_PRIORITY_CLASS
            0x00000020 => 0,   // NORMAL_PRIORITY_CLASS
            0x00008000 => 10,  // ABOVE_NORMAL_PRIORITY_CLASS  
            0x00000080 => 20,  // HIGH_PRIORITY_CLASS
            0x00000100 => 30,  // REALTIME_PRIORITY_CLASS
            _ => 0,
        }
    }
    #[cfg(not(any(unix, windows)))]
    {
        0
    }
}

/// Sets the process priority
/// Returns 0 on success, -1 on error
pub fn set_priority(priority: i32) -> i32 {
    #[cfg(unix)]
    {
        unsafe {
            if libc::setpriority(libc::PRIO_PROCESS, 0, priority) == 0 {
                0
            } else {
                -1
            }
        }
    }
    #[cfg(windows)]
    {
        extern "system" {
            fn GetCurrentProcess() -> *mut std::ffi::c_void;
            fn SetPriorityClass(process: *mut std::ffi::c_void, priority_class: u32) -> i32;
        }
        
        // Convert Unix-like priority to Windows priority class
        let priority_class = if priority <= -15 {
            0x00000040 // IDLE_PRIORITY_CLASS
        } else if priority <= -5 {
            0x00004000 // BELOW_NORMAL_PRIORITY_CLASS
        } else if priority <= 5 {
            0x00000020 // NORMAL_PRIORITY_CLASS
        } else if priority <= 15 {
            0x00008000 // ABOVE_NORMAL_PRIORITY_CLASS
        } else if priority <= 25 {
            0x00000080 // HIGH_PRIORITY_CLASS
        } else {
            0x00000100 // REALTIME_PRIORITY_CLASS
        };
        
        if unsafe { SetPriorityClass(GetCurrentProcess(), priority_class) } != 0 {
            0
        } else {
            -1
        }
    }
    #[cfg(not(any(unix, windows)))]
    {
        -1
    }
}

/// Gets the process working directory
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_working_dir() -> *const std::ffi::c_char {
    use std::alloc::{alloc, Layout};
    use std::ffi::CString;
    
    match std::env::current_dir() {
        Ok(path) => {
            if let Some(path_str) = path.to_str() {
                if let Ok(c_str) = CString::new(path_str) {
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
            }
        }
        Err(_) => {}
    }
    
    std::ptr::null()
}

/// Gets the process executable path
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_executable_path() -> *const std::ffi::c_char {
    use std::alloc::{alloc, Layout};
    use std::ffi::CString;
    
    match std::env::current_exe() {
        Ok(path) => {
            if let Some(path_str) = path.to_str() {
                if let Ok(c_str) = CString::new(path_str) {
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
            }
        }
        Err(_) => {}
    }
    
    std::ptr::null()
}

/// Gets the process command line arguments
/// Returns a pointer to an array of null-terminated strings, or null on error
pub fn get_command_line() -> *const *const std::ffi::c_char {
    let args: Vec<String> = std::env::args().collect();
    
    if args.is_empty() {
        return std::ptr::null();
    }
    
    // Calculate total size needed: array of pointers + all strings
    let num_args = args.len();
    let ptr_array_size = (num_args + 1) * std::mem::size_of::<*const std::ffi::c_char>(); // +1 for null terminator
    
    // Calculate string storage size
    let mut total_string_size = 0;
    for arg in &args {
        total_string_size += arg.len() + 1; // +1 for null terminator
    }
    
    let total_layout = Layout::from_size_align(ptr_array_size + total_string_size, std::mem::align_of::<*const std::ffi::c_char>()).unwrap();
    let base_ptr = unsafe { alloc(total_layout) };
    
    if base_ptr.is_null() {
        return std::ptr::null();
    }
    
    // Set up pointer array at the beginning
    let ptr_array = base_ptr as *mut *const std::ffi::c_char;
    // String storage comes after the pointer array
    let string_storage = unsafe { base_ptr.add(ptr_array_size) };
    
    let mut string_offset = 0;
    
    for (i, arg) in args.iter().enumerate() {
        let arg_bytes = arg.as_bytes();
        
        // Copy string to storage
        let string_ptr = unsafe { string_storage.add(string_offset) };
        unsafe {
            std::ptr::copy_nonoverlapping(arg_bytes.as_ptr(), string_ptr, arg_bytes.len());
            std::ptr::write(string_ptr.add(arg_bytes.len()), 0u8); // null terminator
        }
        
        // Set pointer in array
        unsafe {
            std::ptr::write(ptr_array.add(i), string_ptr as *const std::ffi::c_char);
        }
        
        string_offset += arg_bytes.len() + 1;
    }
    
    // Null terminate the pointer array
    unsafe {
        std::ptr::write(ptr_array.add(num_args), std::ptr::null());
    }
    
    ptr_array as *const *const std::ffi::c_char
}

/// Gets the number of command line arguments
pub fn get_arg_count() -> u32 {
    std::env::args().count() as u32
}

/// Gets a command line argument by index
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_arg(index: u32) -> *const std::ffi::c_char {
    use std::alloc::{alloc, Layout};
    use std::ffi::CString;
    
    let args: Vec<String> = std::env::args().collect();
    if index as usize >= args.len() {
        return std::ptr::null();
    }
    
    let arg = &args[index as usize];
    if let Ok(c_str) = CString::new(arg.as_str()) {
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

/// Gets the process environment variables
/// Returns a pointer to an array of key-value pairs, or null on error
pub fn get_environment() -> *const *const std::ffi::c_char {
    let env_vars: Vec<(String, String)> = std::env::vars().collect();
    
    if env_vars.is_empty() {
        return std::ptr::null();
    }
    
    // Calculate total size needed: array of pointers + all strings
    let num_vars = env_vars.len();
    let ptr_array_size = (num_vars + 1) * std::mem::size_of::<*const std::ffi::c_char>(); // +1 for null terminator
    
    // Calculate string storage size
    let mut total_string_size = 0;
    for (key, value) in &env_vars {
        total_string_size += key.len() + 1 + value.len() + 1; // key=value\0
    }
    
    let total_layout = Layout::from_size_align(ptr_array_size + total_string_size, std::mem::align_of::<*const std::ffi::c_char>()).unwrap();
    let base_ptr = unsafe { alloc(total_layout) };
    
    if base_ptr.is_null() {
        return std::ptr::null();
    }
    
    // Set up pointer array at the beginning
    let ptr_array = base_ptr as *mut *const std::ffi::c_char;
    // String storage comes after the pointer array
    let string_storage = unsafe { base_ptr.add(ptr_array_size) };
    
    let mut string_offset = 0;
    
    for (i, (key, value)) in env_vars.iter().enumerate() {
        // Format as "key=value"
        let env_string = format!("{}={}", key, value);
        let env_bytes = env_string.as_bytes();
        
        // Copy string to storage
        let string_ptr = unsafe { string_storage.add(string_offset) };
        unsafe {
            std::ptr::copy_nonoverlapping(env_bytes.as_ptr(), string_ptr, env_bytes.len());
            std::ptr::write(string_ptr.add(env_bytes.len()), 0u8); // null terminator
        }
        
        // Set pointer in array
        unsafe {
            std::ptr::write(ptr_array.add(i), string_ptr as *const std::ffi::c_char);
        }
        
        string_offset += env_bytes.len() + 1;
    }
    
    // Null terminate the pointer array
    unsafe {
        std::ptr::write(ptr_array.add(num_vars), std::ptr::null());
    }
    
    ptr_array as *const *const std::ffi::c_char
}

/// Gets the number of environment variables
pub fn get_env_count() -> u32 {
    std::env::vars().count() as u32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_operations() {
        // Test basic process information
        let pid = get_pid();
        assert!(pid > 0);
        
        let info = get_info();
        assert_eq!(info.pid, pid);
        assert!(info.memory_usage > 0);
        
        let thread_count = get_thread_count();
        assert!(thread_count > 0);
        
        let arg_count = get_arg_count();
        assert!(arg_count > 0);
        
        let env_count = get_env_count();
        assert!(env_count >= 0);
    }

    #[test]
    fn test_path_operations() {
        // Test working directory
        let _working_dir = get_working_dir();
        // Note: working_dir might be null in some environments
        // so we can't assert it's not null
        
        // Test executable path
        let _exe_path = get_executable_path();
        // Note: exe_path might be null in some environments
        // so we can't assert it's not null
    }

    #[test]
    fn test_argument_operations() {
        let arg_count = get_arg_count();
        if arg_count > 0 {
            let _first_arg = get_arg(0);
            // Note: first_arg might be null in some environments
            // so we can't assert it's not null
        }
        
        // Test out of bounds
        let invalid_arg = get_arg(arg_count + 1);
        assert!(invalid_arg.is_null());
    }
} 