//! Time-related operations for the Runa runtime.

use std::time::{SystemTime, UNIX_EPOCH, Instant};
use std::alloc::{alloc, Layout};
use std::ffi::CString;
use chrono::{DateTime, NaiveDateTime, TimeZone, Utc};

#[cfg(unix)]
extern crate libc;

/// Gets the current time as seconds since Unix epoch
pub fn get_current_time() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs()
}

/// Gets the current time as milliseconds since Unix epoch
pub fn get_current_time_ms() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64
}

/// Gets the current time as microseconds since Unix epoch
pub fn get_current_time_us() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_micros() as u64
}

/// Gets the current time as nanoseconds since Unix epoch
pub fn get_current_time_ns() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos() as u64
}

/// Gets the monotonic time as nanoseconds since an arbitrary point
/// This is useful for measuring elapsed time
pub fn get_monotonic_time() -> u64 {
    // Use a static to store the start time
    static START_TIME: std::sync::OnceLock<Instant> = std::sync::OnceLock::new();
    
    let start = START_TIME.get_or_init(Instant::now);
    start.elapsed().as_nanos() as u64
}

/// Gets the monotonic time as milliseconds since an arbitrary point
pub fn get_monotonic_time_ms() -> u64 {
    static START_TIME: std::sync::OnceLock<Instant> = std::sync::OnceLock::new();
    
    let start = START_TIME.get_or_init(Instant::now);
    start.elapsed().as_millis() as u64
}

/// Gets the monotonic time as microseconds since an arbitrary point
pub fn get_monotonic_time_us() -> u64 {
    static START_TIME: std::sync::OnceLock<Instant> = std::sync::OnceLock::new();
    
    let start = START_TIME.get_or_init(Instant::now);
    start.elapsed().as_micros() as u64
}

/// Gets the monotonic time as seconds since an arbitrary point
pub fn get_monotonic_time_sec() -> f64 {
    static START_TIME: std::sync::OnceLock<Instant> = std::sync::OnceLock::new();
    
    let start = START_TIME.get_or_init(Instant::now);
    start.elapsed().as_secs_f64()
}

/// Converts a Unix timestamp to a human-readable string
/// Returns a pointer to a null-terminated string, or null on error
pub fn format_time(timestamp: u64) -> *const std::ffi::c_char {
    use std::alloc::{alloc, Layout};
    use std::ffi::CString;
    
    if let Some(datetime) = DateTime::from_timestamp(timestamp as i64, 0) {
        let formatted = datetime.naive_local().format("%Y-%m-%d %H:%M:%S").to_string();
        if let Ok(c_str) = CString::new(formatted) {
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
    
    std::ptr::null()
}

/// Parses a human-readable time string to a Unix timestamp
/// Returns the timestamp, or 0 on error
pub fn parse_time(time_str: *const std::ffi::c_char) -> u64 {
    if time_str.is_null() {
        return 0;
    }
    
    let c_str = unsafe { std::ffi::CStr::from_ptr(time_str) };
    if let Ok(s) = c_str.to_str() {
        // Try common formats
        let formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%f",
        ];
        
        for format in &formats {
            if let Ok(dt) = NaiveDateTime::parse_from_str(s, format) {
                return Utc.from_utc_datetime(&dt).timestamp() as u64;
            }
        }
    }
    
    0
}

/// Gets the current timezone offset in seconds
pub fn get_timezone_offset() -> i32 {
    #[cfg(unix)]
    {
        unsafe {
            let mut tv: libc::timeval = std::mem::zeroed();
            if libc::gettimeofday(&mut tv, std::ptr::null_mut()) == 0 {
                // Use localtime vs gmtime to calculate timezone offset
                let local_time = libc::localtime(&tv.tv_sec);
                let gm_time = libc::gmtime(&tv.tv_sec);
                if !local_time.is_null() && !gm_time.is_null() {
                    // Calculate the difference between local time and GMT
                    let local_seconds = (*local_time).tm_hour * 3600 + (*local_time).tm_min * 60 + (*local_time).tm_sec;
                    let gm_seconds = (*gm_time).tm_hour * 3600 + (*gm_time).tm_min * 60 + (*gm_time).tm_sec;
                    let mut offset = local_seconds - gm_seconds;
                    
                    // Handle day boundary crossings
                    if offset > 43200 { // More than 12 hours
                        offset -= 86400;
                    } else if offset < -43200 { // Less than -12 hours
                        offset += 86400;
                    }
                    
                    return offset;
                }
            }
        }
    }
    #[cfg(windows)]
    {
        extern "system" {
            fn GetTimeZoneInformation(lpTimeZoneInformation: *mut TIME_ZONE_INFORMATION) -> u32;
        }
        
        #[repr(C)]
        struct TIME_ZONE_INFORMATION {
            bias: i32,
            standard_name: [u16; 32],
            standard_date: SYSTEMTIME,
            standard_bias: i32,
            daylight_name: [u16; 32],
            daylight_date: SYSTEMTIME,
            daylight_bias: i32,
        }
        
        #[repr(C)]
        struct SYSTEMTIME {
            year: u16,
            month: u16,
            day_of_week: u16,
            day: u16,
            hour: u16,
            minute: u16,
            second: u16,
            milliseconds: u16,
        }
        
        let mut tz_info: TIME_ZONE_INFORMATION = unsafe { std::mem::zeroed() };
        let result = unsafe { GetTimeZoneInformation(&mut tz_info) };
        
        if result != 0xFFFFFFFF {
            return -(tz_info.bias * 60); // Convert minutes to seconds, negate for correct sign
        }
    }
    
    0 // UTC fallback
}

/// Gets the current timezone name
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_timezone_name() -> *const std::ffi::c_char {
    // Try environment variables first
    if let Ok(tz) = std::env::var("TZ") {
        if !tz.is_empty() {
            return allocate_string(&tz);
        }
    }
    
    #[cfg(target_os = "linux")]
    {
        // Try to read from /etc/timezone
        if let Ok(contents) = std::fs::read_to_string("/etc/timezone") {
            let tz = contents.trim();
            if !tz.is_empty() {
                return allocate_string(tz);
            }
        }
        
        // Fallback: parse /etc/localtime symlink
        if let Ok(link) = std::fs::read_link("/etc/localtime") {
            if let Some(tz_path) = link.to_str() {
                if let Some(tz_start) = tz_path.find("/zoneinfo/") {
                    let tz = &tz_path[tz_start + 10..];
                    if !tz.is_empty() {
                        return allocate_string(tz);
                    }
                }
            }
        }
    }
    
    #[cfg(target_os = "macos")]
    {
        // Try to read macOS timezone
        if let Ok(output) = std::process::Command::new("readlink")
            .arg("/etc/localtime")
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                let output_str = output_str.trim();
                if let Some(tz_start) = output_str.find("/zoneinfo/") {
                    let tz = &output_str[tz_start + 10..];
                    if !tz.is_empty() {
                        return allocate_string(tz);
                    }
                }
            }
        }
    }
    
    #[cfg(windows)]
    {
        // Try Windows time zone
        use std::process::Command;
        
        if let Ok(output) = Command::new("powershell")
            .args(&["-Command", "(Get-TimeZone).Id"])
            .output()
        {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                let tz = output_str.trim();
                if !tz.is_empty() {
                    return allocate_string(tz);
                }
            }
        }
    }
    
    // Fallback to UTC
    allocate_string("UTC")
}

/// Checks if daylight saving time is in effect
pub fn is_dst() -> bool {
    #[cfg(unix)]
    {
        
        unsafe {
            let now = libc::time(std::ptr::null_mut());
            let tm = libc::localtime(&now);
            if !tm.is_null() {
                return (*tm).tm_isdst > 0;
            }
        }
    }
    #[cfg(windows)]
    {
        extern "system" {
            fn GetTimeZoneInformation(lpTimeZoneInformation: *mut TIME_ZONE_INFORMATION) -> u32;
        }
        
        #[repr(C)]
        struct TIME_ZONE_INFORMATION {
            bias: i32,
            standard_name: [u16; 32],
            standard_date: SYSTEMTIME,
            standard_bias: i32,
            daylight_name: [u16; 32],
            daylight_date: SYSTEMTIME,
            daylight_bias: i32,
        }
        
        #[repr(C)]
        struct SYSTEMTIME {
            year: u16,
            month: u16,
            day_of_week: u16,
            day: u16,
            hour: u16,
            minute: u16,
            second: u16,
            milliseconds: u16,
        }
        
        let mut tz_info: TIME_ZONE_INFORMATION = unsafe { std::mem::zeroed() };
        let result = unsafe { GetTimeZoneInformation(&mut tz_info) };
        
        // TIME_ZONE_ID_DAYLIGHT = 2
        return result == 2;
    }
    
    false
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
    fn test_time_operations() {
        // Test current time functions
        let time1 = get_current_time();
        let time2 = get_current_time();
        assert!(time2 >= time1);
        
        let time_ms1 = get_current_time_ms();
        let time_ms2 = get_current_time_ms();
        assert!(time_ms2 >= time_ms1);
        
        let time_us1 = get_current_time_us();
        let time_us2 = get_current_time_us();
        assert!(time_us2 >= time_us1);
        
        let time_ns1 = get_current_time_ns();
        let time_ns2 = get_current_time_ns();
        assert!(time_ns2 >= time_ns1);
    }

    #[test]
    fn test_monotonic_time() {
        // Test monotonic time functions
        let mono1 = get_monotonic_time();
        std::thread::sleep(std::time::Duration::from_millis(1));
        let mono2 = get_monotonic_time();
        assert!(mono2 > mono1);
        
        let mono_ms1 = get_monotonic_time_ms();
        std::thread::sleep(std::time::Duration::from_millis(1));
        let mono_ms2 = get_monotonic_time_ms();
        assert!(mono_ms2 >= mono_ms1);
        
        let mono_us1 = get_monotonic_time_us();
        std::thread::sleep(std::time::Duration::from_millis(1));
        let mono_us2 = get_monotonic_time_us();
        assert!(mono_us2 > mono_us1);
        
        let mono_sec1 = get_monotonic_time_sec();
        std::thread::sleep(std::time::Duration::from_millis(1));
        let mono_sec2 = get_monotonic_time_sec();
        assert!(mono_sec2 > mono_sec1);
    }

    #[test]
    fn test_time_formatting() {
        // Test time formatting and parsing
        let timestamp = 1640995200; // 2022-01-01 00:00:00 UTC
        
        let formatted = format_time(timestamp);
        assert!(!formatted.is_null());
        
        let parsed = parse_time(formatted);
        assert_eq!(parsed, timestamp);
    }
} 