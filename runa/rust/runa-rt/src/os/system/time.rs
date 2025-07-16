//! Time-related operations for the Runa runtime.

use std::time::{SystemTime, UNIX_EPOCH, Instant};

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
    
    let datetime = chrono::DateTime::from_timestamp(timestamp as i64, 0).map(|dt| dt.naive_local());
    if let Some(dt) = datetime {
        let formatted = dt.format("%Y-%m-%d %H:%M:%S").to_string();
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
            if let Ok(dt) = chrono::NaiveDateTime::parse_from_str(s, format) {
                return dt.and_utc().timestamp() as u64;
            }
        }
    }
    
    0
}

/// Gets the current timezone offset in seconds
pub fn get_timezone_offset() -> i32 {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    0
}

/// Gets the current timezone name
/// Returns a pointer to a null-terminated string, or null on error
pub fn get_timezone_name() -> *const std::ffi::c_char {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    std::ptr::null()
}

/// Checks if daylight saving time is in effect
pub fn is_dst() -> bool {
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    false
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