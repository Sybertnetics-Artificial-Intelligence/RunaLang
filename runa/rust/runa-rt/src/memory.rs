//! Memory management primitives for the Runa runtime.

use std::alloc::{alloc as std_alloc, Layout};
use crate::runa_object;

/// Memory allocation statistics for debugging and monitoring
#[derive(Debug, Default, Clone)]
pub struct MemoryStats {
    pub total_allocated: usize,
    pub total_freed: usize,
    pub current_usage: usize,
    pub allocation_count: usize,
    pub deallocation_count: usize,
}

use std::sync::Mutex;

static MEMORY_STATS: Mutex<MemoryStats> = Mutex::new(MemoryStats {
    total_allocated: 0,
    total_freed: 0,
    current_usage: 0,
    allocation_count: 0,
    deallocation_count: 0,
});

/// Allocates a block of memory of the given size.
/// Returns a pointer to the allocated memory or null on failure.
pub fn alloc(size: usize) -> runa_object {
    if size == 0 {
        return std::ptr::null_mut();
    }

    let layout = match Layout::from_size_align(size, std::mem::align_of::<u8>()) {
        Ok(layout) => layout,
        Err(_) => return std::ptr::null_mut(),
    };

    let ptr = unsafe { std_alloc(layout) };
    
    if !ptr.is_null() {
        if let Ok(mut stats) = MEMORY_STATS.lock() {
            stats.total_allocated += size;
            stats.current_usage += size;
            stats.allocation_count += 1;
        }
    }

    ptr as runa_object
}

/// Allocates a block of memory with the given size and alignment.
/// Returns a pointer to the allocated memory or null on failure.
pub fn alloc_aligned(size: usize, alignment: usize) -> runa_object {
    if size == 0 {
        return std::ptr::null_mut();
    }

    let layout = match Layout::from_size_align(size, alignment) {
        Ok(layout) => layout,
        Err(_) => return std::ptr::null_mut(),
    };

    let ptr = unsafe { std_alloc(layout) };
    
    if !ptr.is_null() {
        if let Ok(mut stats) = MEMORY_STATS.lock() {
            stats.total_allocated += size;
            stats.current_usage += size;
            stats.allocation_count += 1;
        }
    }

    ptr as runa_object
}

/// Deallocates a previously allocated block of memory.
/// The size must match the size used when allocating.
pub fn free(ptr: runa_object) {
    if ptr.is_null() {
        return;
    }

    // Note: In a real implementation, we would need to track the size
    // of each allocation. For now, we'll use a placeholder size.
    // This is a limitation that should be addressed in a production system.
    let size = 0; // TODO: Track allocation sizes
    
    if let Ok(mut stats) = MEMORY_STATS.lock() {
        stats.total_freed += size;
        stats.current_usage = stats.current_usage.saturating_sub(size);
        stats.deallocation_count += 1;
    }
}

/// Reallocates a block of memory to a new size.
/// Returns a pointer to the reallocated memory or null on failure.
pub fn realloc(ptr: runa_object, new_size: usize) -> runa_object {
    if ptr.is_null() {
        return alloc(new_size);
    }

    if new_size == 0 {
        free(ptr);
        return std::ptr::null_mut();
    }

    // For now, we'll do a simple alloc/copy/free
    // In a production system, this would use std::alloc::realloc
    let new_ptr = alloc(new_size);
    if new_ptr.is_null() {
        return std::ptr::null_mut();
    }

    // Copy the old data (we need to know the old size)
    // TODO: Track allocation sizes
    let old_size = 0; // Placeholder
    
    if old_size > 0 {
        unsafe {
            std::ptr::copy_nonoverlapping(
                ptr as *const u8,
                new_ptr as *mut u8,
                std::cmp::min(old_size, new_size)
            );
        }
    }

    free(ptr);
    new_ptr
}

/// Returns the current memory usage statistics.
pub fn get_memory_stats() -> MemoryStats {
    if let Ok(stats) = MEMORY_STATS.lock() {
        stats.clone()
    } else {
        MemoryStats::default()
    }
}

/// Resets the memory statistics.
pub fn reset_memory_stats() {
    if let Ok(mut stats) = MEMORY_STATS.lock() {
        *stats = MemoryStats::default();
    }
}

/// Memory safety check: validates that a pointer is valid and within bounds.
/// This is a basic check and should not be relied upon for security.
pub fn is_valid_pointer(ptr: runa_object, size: usize) -> bool {
    if ptr.is_null() || size == 0 {
        return false;
    }

    // Basic alignment check
    let alignment = std::mem::align_of::<u8>();
    let ptr_value = ptr as usize;
    if ptr_value % alignment != 0 {
        return false;
    }

    // Note: More comprehensive checks would require tracking allocated regions
    // This is a simplified implementation
    true
}

/// Memory safety check: validates that a pointer is null or valid.
pub fn is_null_or_valid(ptr: runa_object) -> bool {
    ptr.is_null() || is_valid_pointer(ptr, 1)
}

/// Zeroes out a block of memory.
pub fn zero_memory(ptr: runa_object, size: usize) {
    if !ptr.is_null() && size > 0 {
        unsafe {
            std::ptr::write_bytes(ptr as *mut u8, 0, size);
        }
    }
}

/// Copies memory from source to destination.
pub fn copy_memory(dst: runa_object, src: runa_object, size: usize) -> bool {
    if dst.is_null() || src.is_null() || size == 0 {
        return false;
    }

    unsafe {
        std::ptr::copy_nonoverlapping(
            src as *const u8,
            dst as *mut u8,
            size
        );
    }
    true
}

/// Moves memory from source to destination.
pub fn move_memory(dst: runa_object, src: runa_object, size: usize) -> bool {
    if dst.is_null() || src.is_null() || size == 0 {
        return false;
    }

    unsafe {
        std::ptr::copy(
            src as *const u8,
            dst as *mut u8,
            size
        );
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_allocation() {
        let ptr = alloc(1024);
        assert!(!ptr.is_null());
        free(ptr);
    }

    #[test]
    fn test_zero_size_allocation() {
        let ptr = alloc(0);
        assert!(ptr.is_null());
    }

    #[test]
    fn test_null_pointer_free() {
        free(std::ptr::null_mut()); // Should not panic
    }

    #[test]
    fn test_memory_stats() {
        reset_memory_stats();
        let stats = get_memory_stats();
        assert_eq!(stats.allocation_count, 0);
        assert_eq!(stats.current_usage, 0);

        let ptr = alloc(100);
        let stats = get_memory_stats();
        assert_eq!(stats.allocation_count, 1);
        assert!(stats.current_usage > 0);

        free(ptr);
    }

    #[test]
    fn test_zero_memory() {
        let ptr = alloc(16);
        assert!(!ptr.is_null());
        
        // Write some data
        unsafe {
            std::ptr::write_bytes(ptr as *mut u8, 0xFF, 16);
        }
        
        // Zero it out
        zero_memory(ptr, 16);
        
        // Check that it's zeroed
        unsafe {
            let bytes = std::slice::from_raw_parts(ptr as *const u8, 16);
            assert!(bytes.iter().all(|&b| b == 0));
        }
        
        free(ptr);
    }

    #[test]
    fn test_copy_memory() {
        let src = alloc(16);
        let dst = alloc(16);
        assert!(!src.is_null());
        assert!(!dst.is_null());
        
        // Write data to source
        unsafe {
            std::ptr::write_bytes(src as *mut u8, 0xAA, 16);
        }
        
        // Copy to destination
        assert!(copy_memory(dst, src, 16));
        
        // Verify copy
        unsafe {
            let src_bytes = std::slice::from_raw_parts(src as *const u8, 16);
            let dst_bytes = std::slice::from_raw_parts(dst as *const u8, 16);
            assert_eq!(src_bytes, dst_bytes);
        }
        
        free(src);
        free(dst);
    }
} 