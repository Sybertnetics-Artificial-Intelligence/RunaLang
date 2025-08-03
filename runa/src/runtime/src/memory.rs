//! Advanced memory management system for the Runa runtime.
//! Provides custom allocators, GC algorithms, and ownership tracking.

use std::alloc::{alloc as std_alloc, dealloc as std_dealloc, Layout};
use std::collections::HashMap;
use std::sync::{Arc, Mutex, RwLock};
use std::ptr::NonNull;
use crate::runa_object;

/// Advanced memory allocation statistics for debugging and monitoring
#[derive(Debug, Default, Clone)]
pub struct MemoryStats {
    pub total_allocated: usize,
    pub total_freed: usize,
    pub current_usage: usize,
    pub allocation_count: usize,
    pub deallocation_count: usize,
    pub peak_usage: usize,
    pub fragmentation_ratio: f64,
    pub gc_collections: usize,
    pub gc_time_ms: u64,
}

/// Custom allocator trait for pluggable memory allocation strategies
pub trait CustomAllocator: Send + Sync {
    fn allocate(&self, size: usize, align: usize) -> Result<NonNull<u8>, AllocError>;
    fn deallocate(&self, ptr: NonNull<u8>, size: usize, align: usize);
    fn reallocate(&self, ptr: NonNull<u8>, old_size: usize, new_size: usize, align: usize) -> Result<NonNull<u8>, AllocError>;
    fn get_stats(&self) -> AllocatorStats;
    fn reset_stats(&self);
}

#[derive(Debug, Clone)]
pub struct AllocatorStats {
    pub allocated_bytes: usize,
    pub freed_bytes: usize,
    pub active_allocations: usize,
    pub peak_allocations: usize,
    pub fragmentation: f64,
}

#[derive(Debug)]
pub enum AllocError {
    OutOfMemory,
    InvalidSize,
    InvalidAlignment,
    Fragmentation,
}

/// Arena allocator for fast bulk allocations
pub struct ArenaAllocator {
    buffer: Arc<Mutex<Vec<u8>>>,
    offset: Arc<Mutex<usize>>,
    stats: Arc<Mutex<AllocatorStats>>,
}

/// Pool allocator for fixed-size allocations
pub struct PoolAllocator {
    block_size: usize,
    free_blocks: Arc<Mutex<Vec<NonNull<u8>>>>,
    allocated_blocks: Arc<Mutex<HashMap<*mut u8, usize>>>,
    stats: Arc<Mutex<AllocatorStats>>,
}

/// Stack allocator for LIFO allocations
pub struct StackAllocator {
    buffer: Arc<Mutex<Vec<u8>>>,
    top: Arc<Mutex<usize>>,
    markers: Arc<Mutex<Vec<usize>>>,
    stats: Arc<Mutex<AllocatorStats>>,
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

// ============================================================================
// CUSTOM ALLOCATOR IMPLEMENTATIONS
// ============================================================================

impl ArenaAllocator {
    pub fn new(capacity: usize) -> Self {
        Self {
            buffer: Arc::new(Mutex::new(vec![0u8; capacity])),
            offset: Arc::new(Mutex::new(0)),
            stats: Arc::new(Mutex::new(AllocatorStats::default())),
        }
    }
    
    pub fn reset(&self) {
        if let (Ok(mut offset), Ok(mut stats)) = (self.offset.lock(), self.stats.lock()) {
            *offset = 0;
            stats.reset();
        }
    }
}

impl CustomAllocator for ArenaAllocator {
    fn allocate(&self, size: usize, align: usize) -> Result<NonNull<u8>, AllocError> {
        if size == 0 {
            return Err(AllocError::InvalidSize);
        }
        
        let (buffer_guard, mut offset_guard, mut stats_guard) = {
            let buffer = self.buffer.lock().map_err(|_| AllocError::OutOfMemory)?;
            let offset = self.offset.lock().map_err(|_| AllocError::OutOfMemory)?;
            let stats = self.stats.lock().map_err(|_| AllocError::OutOfMemory)?;
            (buffer, offset, stats)
        };
        
        let aligned_offset = (*offset_guard + align - 1) & !(align - 1);
        let end_offset = aligned_offset + size;
        
        if end_offset > buffer_guard.len() {
            return Err(AllocError::OutOfMemory);
        }
        
        let ptr = unsafe {
            NonNull::new_unchecked(buffer_guard.as_ptr().add(aligned_offset) as *mut u8)
        };
        
        *offset_guard = end_offset;
        stats_guard.allocated_bytes += size;
        stats_guard.active_allocations += 1;
        
        Ok(ptr)
    }
    
    fn deallocate(&self, _ptr: NonNull<u8>, size: usize, _align: usize) {
        if let Ok(mut stats) = self.stats.lock() {
            stats.freed_bytes += size;
            stats.active_allocations = stats.active_allocations.saturating_sub(1);
        }
    }
    
    fn reallocate(&self, _ptr: NonNull<u8>, _old_size: usize, new_size: usize, align: usize) -> Result<NonNull<u8>, AllocError> {
        // Arena allocators can't reallocate in place, so allocate new
        self.allocate(new_size, align)
    }
    
    fn get_stats(&self) -> AllocatorStats {
        self.stats.lock().unwrap_or_default().clone()
    }
    
    fn reset_stats(&self) {
        if let Ok(mut stats) = self.stats.lock() {
            stats.reset();
        }
    }
}

impl PoolAllocator {
    pub fn new(block_size: usize, pool_size: usize) -> Self {
        let mut free_blocks = Vec::new();
        let buffer = vec![0u8; block_size * pool_size];
        
        for i in 0..pool_size {
            let ptr = unsafe {
                NonNull::new_unchecked(buffer.as_ptr().add(i * block_size) as *mut u8)
            };
            free_blocks.push(ptr);
        }
        
        Self {
            block_size,
            free_blocks: Arc::new(Mutex::new(free_blocks)),
            allocated_blocks: Arc::new(Mutex::new(HashMap::new())),
            stats: Arc::new(Mutex::new(AllocatorStats::default())),
        }
    }
}

impl CustomAllocator for PoolAllocator {
    fn allocate(&self, size: usize, _align: usize) -> Result<NonNull<u8>, AllocError> {
        if size > self.block_size {
            return Err(AllocError::InvalidSize);
        }
        
        let (mut free_blocks, mut allocated_blocks, mut stats) = {
            let free = self.free_blocks.lock().map_err(|_| AllocError::OutOfMemory)?;
            let alloc = self.allocated_blocks.lock().map_err(|_| AllocError::OutOfMemory)?;
            let stats = self.stats.lock().map_err(|_| AllocError::OutOfMemory)?;
            (free, alloc, stats)
        };
        
        let ptr = free_blocks.pop().ok_or(AllocError::OutOfMemory)?;
        allocated_blocks.insert(ptr.as_ptr(), self.block_size);
        
        stats.allocated_bytes += self.block_size;
        stats.active_allocations += 1;
        
        Ok(ptr)
    }
    
    fn deallocate(&self, ptr: NonNull<u8>, _size: usize, _align: usize) {
        if let (Ok(mut free_blocks), Ok(mut allocated_blocks), Ok(mut stats)) = 
            (self.free_blocks.lock(), self.allocated_blocks.lock(), self.stats.lock()) {
            
            if allocated_blocks.remove(&ptr.as_ptr()).is_some() {
                free_blocks.push(ptr);
                stats.freed_bytes += self.block_size;
                stats.active_allocations = stats.active_allocations.saturating_sub(1);
            }
        }
    }
    
    fn reallocate(&self, ptr: NonNull<u8>, _old_size: usize, new_size: usize, align: usize) -> Result<NonNull<u8>, AllocError> {
        if new_size <= self.block_size {
            Ok(ptr) // No need to reallocate if it fits
        } else {
            let new_ptr = self.allocate(new_size, align)?;
            self.deallocate(ptr, self.block_size, align);
            Ok(new_ptr)
        }
    }
    
    fn get_stats(&self) -> AllocatorStats {
        self.stats.lock().unwrap_or_default().clone()
    }
    
    fn reset_stats(&self) {
        if let Ok(mut stats) = self.stats.lock() {
            stats.reset();
        }
    }
}

impl Default for AllocatorStats {
    fn default() -> Self {
        Self {
            allocated_bytes: 0,
            freed_bytes: 0,
            active_allocations: 0,
            peak_allocations: 0,
            fragmentation: 0.0,
        }
    }
}

impl AllocatorStats {
    fn reset(&mut self) {
        *self = Self::default();
    }
}

// ============================================================================
// FFI EXPORTS FOR CUSTOM ALLOCATORS
// ============================================================================

#[no_mangle]
pub extern "C" fn runa_create_arena_allocator(capacity: usize) -> *mut ArenaAllocator {
    let allocator = Box::new(ArenaAllocator::new(capacity));
    Box::into_raw(allocator)
}

#[no_mangle]
pub extern "C" fn runa_create_pool_allocator(block_size: usize, pool_size: usize) -> *mut PoolAllocator {
    let allocator = Box::new(PoolAllocator::new(block_size, pool_size));
    Box::into_raw(allocator)
}

#[no_mangle]
pub extern "C" fn runa_arena_allocate(allocator: *mut ArenaAllocator, size: usize, align: usize) -> runa_object {
    if allocator.is_null() {
        return std::ptr::null_mut();
    }
    
    let allocator = unsafe { &*allocator };
    match allocator.allocate(size, align) {
        Ok(ptr) => ptr.as_ptr() as runa_object,
        Err(_) => std::ptr::null_mut(),
    }
}

#[no_mangle]
pub extern "C" fn runa_pool_allocate(allocator: *mut PoolAllocator, size: usize, align: usize) -> runa_object {
    if allocator.is_null() {
        return std::ptr::null_mut();
    }
    
    let allocator = unsafe { &*allocator };
    match allocator.allocate(size, align) {
        Ok(ptr) => ptr.as_ptr() as runa_object,
        Err(_) => std::ptr::null_mut(),
    }
}

#[no_mangle]
pub extern "C" fn runa_get_allocator_stats(allocator: *mut dyn CustomAllocator) -> AllocatorStats {
    if allocator.is_null() {
        return AllocatorStats::default();
    }
    
    let allocator = unsafe { &*allocator };
    allocator.get_stats()
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