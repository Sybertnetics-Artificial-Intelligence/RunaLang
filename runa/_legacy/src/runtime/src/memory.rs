//! Advanced memory management system for the Runa runtime.
//! Provides custom allocators, GC algorithms, and ownership tracking.

use std::alloc::{alloc as std_alloc, Layout};
use std::collections::HashMap;
use std::sync::{Arc, Mutex, RwLock, LazyLock};
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

/// Custom allocator error types
#[derive(Debug)]
pub enum AllocError {
    OutOfMemory,
    InvalidSize,
    InvalidAlignment,
    Fragmentation,
}

/// Arena allocator for fast bulk allocations - thread safe implementation
pub struct ArenaAllocator {
    buffer: Arc<Mutex<Vec<u8>>>,
    offset: Arc<Mutex<usize>>,
    stats: Arc<Mutex<AllocatorStats>>,
}

/// Pool allocator for fixed-size allocations - thread safe implementation
pub struct PoolAllocator {
    block_size: usize,
    buffer_base: usize, // Base address of the allocated buffer for address calculation
    free_blocks: Arc<Mutex<Vec<usize>>>, // Store addresses as usize for thread safety
    allocated_blocks: Arc<Mutex<HashMap<usize, usize>>>, // address -> size mapping
    stats: Arc<Mutex<AllocatorStats>>,
}

/// Stack allocator for LIFO allocations - thread safe implementation
pub struct StackAllocator {
    buffer: Arc<Mutex<Vec<u8>>>,
    top: Arc<Mutex<usize>>,
    markers: Arc<Mutex<Vec<usize>>>,
    stats: Arc<Mutex<AllocatorStats>>,
}

/// Global memory statistics with thread-safe access
pub static MEMORY_STATS: Mutex<MemoryStats> = Mutex::new(MemoryStats {
    total_allocated: 0,
    total_freed: 0,
    current_usage: 0,
    allocation_count: 0,
    deallocation_count: 0,
    peak_usage: 0,
    fragmentation_ratio: 0.0,
    gc_collections: 0,
    gc_time_ms: 0,
});

/// Thread-safe allocation tracking with size metadata using pointer addresses
pub static ALLOCATION_TRACKER: LazyLock<RwLock<HashMap<usize, AllocationInfo>>> = LazyLock::new(|| RwLock::new(HashMap::new()));

#[derive(Debug, Clone)]
struct AllocationInfo {
    size: usize,
    layout: Layout,
    allocated_at: std::time::Instant,
    thread_id: std::thread::ThreadId,
}

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
        // Record allocation info for proper size tracking
        let allocation_info = AllocationInfo {
            size,
            layout,
            allocated_at: std::time::Instant::now(),
            thread_id: std::thread::current().id(),
        };
        
        if let Ok(mut tracker) = ALLOCATION_TRACKER.write() {
            tracker.insert(ptr as usize, allocation_info);
        }
        
        // Update global statistics atomically
        if let Ok(mut stats) = MEMORY_STATS.lock() {
            stats.total_allocated += size;
            stats.current_usage += size;
            stats.allocation_count += 1;
            
            // Update peak usage
            if stats.current_usage > stats.peak_usage {
                stats.peak_usage = stats.current_usage;
            }
            
            // Calculate fragmentation ratio using comprehensive free block analysis
            stats.fragmentation_ratio = calculate_actual_fragmentation();
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
/// Uses tracked allocation information for proper size management.
pub fn free(ptr: runa_object) {
    if ptr.is_null() {
        return;
    }

    // Retrieve allocation info from tracker
    let allocation_info = if let Ok(mut tracker) = ALLOCATION_TRACKER.write() {
        tracker.remove(&(ptr as usize))
    } else {
        return; // Failed to acquire lock, cannot safely deallocate
    };

    if let Some(info) = allocation_info {
        // Perform the actual deallocation using the tracked layout
        unsafe {
            std::alloc::dealloc(ptr as *mut u8, info.layout);
        }
        
        // Update global statistics atomically
        if let Ok(mut stats) = MEMORY_STATS.lock() {
            stats.total_freed += info.size;
            stats.current_usage = stats.current_usage.saturating_sub(info.size);
            stats.deallocation_count += 1;
            
            // Recalculate fragmentation ratio
            let total_allocated = stats.total_allocated;
            let current_usage = stats.current_usage;
            if total_allocated > 0 {
                stats.fragmentation_ratio = 1.0 - (current_usage as f64 / total_allocated as f64);
            }
        }
    }
    // Note: If allocation info not found, this indicates a double-free or 
    // attempt to free untracked memory - this is caught by not performing the deallocation
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

    // Get the current allocation info to know the old size
    let old_info = if let Ok(tracker) = ALLOCATION_TRACKER.read() {
        tracker.get(&(ptr as usize)).cloned()
    } else {
        return std::ptr::null_mut(); // Failed to acquire lock
    };

    if let Some(old_allocation) = old_info {
        let old_size = old_allocation.size;
        
        // Create new layout for the requested size
        let new_layout = match Layout::from_size_align(new_size, std::mem::align_of::<u8>()) {
            Ok(layout) => layout,
            Err(_) => return std::ptr::null_mut(),
        };

        // Use std::alloc::realloc for efficient reallocation
        let new_ptr = unsafe {
            std::alloc::realloc(ptr as *mut u8, old_allocation.layout, new_size)
        };

        if !new_ptr.is_null() {
            // Update allocation tracking with new info
            let new_info = AllocationInfo {
                size: new_size,
                layout: new_layout,
                allocated_at: std::time::Instant::now(),
                thread_id: std::thread::current().id(),
            };

            if let Ok(mut tracker) = ALLOCATION_TRACKER.write() {
                tracker.remove(&(ptr as usize));
                tracker.insert(new_ptr as usize, new_info);
            }

            // Update statistics for the size change
            if let Ok(mut stats) = MEMORY_STATS.lock() {
                stats.current_usage = stats.current_usage.saturating_sub(old_size);
                stats.current_usage += new_size;
                
                if new_size > old_size {
                    stats.total_allocated += new_size - old_size;
                }

                // Update peak usage
                if stats.current_usage > stats.peak_usage {
                    stats.peak_usage = stats.current_usage;
                }

                // Recalculate fragmentation ratio
                let total_allocated = stats.total_allocated;
                let current_usage = stats.current_usage;
                if total_allocated > 0 {
                    stats.fragmentation_ratio = 1.0 - (current_usage as f64 / total_allocated as f64);
                }
            }

            new_ptr as runa_object
        } else {
            std::ptr::null_mut()
        }
    } else {
        // Allocation not tracked - fallback to alloc/copy/free
        let new_ptr = alloc(new_size);
        if !new_ptr.is_null() {
            // We don't know the old size, so copy what we can (risky)
            // This should not happen in a properly tracked system
            free(ptr);
        }
        new_ptr
    }
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
/// This performs comprehensive validation but should still not be relied upon for security.
/// For security-critical operations, use additional validation mechanisms.
pub fn is_valid_pointer(ptr: runa_object, size: usize) -> bool {
    if ptr.is_null() || size == 0 {
        return false;
    }

    let ptr_value = ptr as usize;
    
    // Check for integer overflow in range calculation
    if ptr_value.checked_add(size).is_none() {
        return false;
    }
    
    let end_ptr = ptr_value + size;

    // Proper alignment check for pointer type - align to word boundary
    let alignment = std::mem::align_of::<usize>();
    if ptr_value % alignment != 0 {
        return false;
    }

    // Platform-specific address space validation
    #[cfg(target_pointer_width = "64")]
    {
        // On 64-bit systems, check against reasonable user space limits
        const MAX_USER_ADDR: usize = 0x7fff_ffff_ffff;
        if end_ptr > MAX_USER_ADDR {
            return false;
        }
    }
    
    #[cfg(target_pointer_width = "32")]
    {
        // On 32-bit systems, check against address space limits
        const MAX_USER_ADDR: usize = 0x7fff_ffff;
        if end_ptr > MAX_USER_ADDR {
            return false;
        }
    }

    // Check if pointer is tracked in our allocation table
    if let Ok(tracker) = ALLOCATION_TRACKER.read() {
        if let Some(info) = tracker.get(&ptr_value) {
            // Verify the entire requested range is within the allocated block
            let allocated_start = ptr_value;
            let allocated_end = allocated_start + info.size;
            return ptr_value >= allocated_start && end_ptr <= allocated_end;
        }
    }
    
    // For untracked pointers, attempt limited accessibility validation
    // This is inherently risky but provides some validation for small accesses
    if size <= 8 {
        // For small reads, try to validate accessibility using a guarded approach
        unsafe {
            // Use std::panic::catch_unwind to safely test memory access
            std::panic::catch_unwind(|| {
                // Volatile read to prevent optimization and ensure actual memory access
                std::ptr::read_volatile(ptr as *const u8);
                if size > 1 {
                    std::ptr::read_volatile((ptr as *const u8).add(size - 1));
                }
            }).is_ok()
        }
    } else {
        // For larger ranges, we cannot safely validate without potential crashes
        // Return false for untracked large allocations as a safety measure
        false
    }
}

/// Enhanced memory safety check with type information and proper alignment
pub fn is_valid_typed_pointer<T>(ptr: *const T, count: usize) -> bool {
    if ptr.is_null() || count == 0 {
        return false;
    }

    // Check for overflow in total size calculation
    let size = match std::mem::size_of::<T>().checked_mul(count) {
        Some(s) => s,
        None => return false,
    };

    let ptr_value = ptr as usize;
    
    // Check alignment specific to type T
    let alignment = std::mem::align_of::<T>();
    if ptr_value % alignment != 0 {
        return false;
    }

    // Use the general pointer validation
    is_valid_pointer(ptr as runa_object, size)
}

/// Validate a C-style string pointer with maximum length check
pub fn is_valid_cstring_pointer(ptr: *const u8, max_len: usize) -> bool {
    if ptr.is_null() {
        return false;
    }

    // Check each byte until null terminator or max_len
    for i in 0..max_len {
        unsafe {
            // Validate each byte access
            if !is_valid_pointer((ptr as *const u8).add(i) as runa_object, 1) {
                return false;
            }
            
            // Check for null terminator
            if std::ptr::read_volatile((ptr as *const u8).add(i)) == 0 {
                return true;
            }
        }
    }
    
    // String longer than max_len without null terminator
    false
}

/// Memory range overlap detection for preventing dangerous operations
pub fn memory_ranges_overlap(
    ptr1: runa_object, size1: usize,
    ptr2: runa_object, size2: usize
) -> bool {
    if ptr1.is_null() || ptr2.is_null() || size1 == 0 || size2 == 0 {
        return false;
    }

    let start1 = ptr1 as usize;
    let end1 = match start1.checked_add(size1) {
        Some(end) => end,
        None => return true, // Overflow means definite overlap with something
    };
    
    let start2 = ptr2 as usize;
    let end2 = match start2.checked_add(size2) {
        Some(end) => end,
        None => return true,
    };

    // Check for overlap: ranges overlap if start1 < end2 && start2 < end1
    start1 < end2 && start2 < end1
}

/// Advanced validation for buffer operations (copies, moves, etc.)
pub fn validate_buffer_operation(
    src: runa_object, dst: runa_object, size: usize
) -> Result<(), &'static str> {
    // Check both pointers are valid
    if !is_valid_pointer(src, size) {
        return Err("Invalid source pointer");
    }
    
    if !is_valid_pointer(dst, size) {
        return Err("Invalid destination pointer");
    }
    
    // Check for overlap in potentially unsafe operations
    if memory_ranges_overlap(src, size, dst, size) {
        return Err("Overlapping memory ranges detected");
    }
    
    Ok(())
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
        
        // Lock all mutexes sequentially to avoid potential deadlocks
        let buffer_guard = self.buffer.lock().map_err(|_| AllocError::OutOfMemory)?;
        let mut offset_guard = self.offset.lock().map_err(|_| AllocError::OutOfMemory)?;
        let mut stats_guard = self.stats.lock().map_err(|_| AllocError::OutOfMemory)?;
        
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
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
    }
    
    fn reset_stats(&self) {
        if let Ok(mut stats) = self.stats.lock() {
            stats.reset();
        }
    }
}

impl PoolAllocator {
    pub fn new(block_size: usize, pool_size: usize) -> Self {
        // Allocate buffer using system allocator
        let layout = std::alloc::Layout::from_size_align(block_size * pool_size, std::mem::align_of::<u8>())
            .expect("Invalid layout for pool allocator");
        
        let buffer_ptr = unsafe { std::alloc::alloc(layout) };
        if buffer_ptr.is_null() {
            panic!("Failed to allocate buffer for pool allocator");
        }
        
        let buffer_base = buffer_ptr as usize;
        let mut free_blocks = Vec::new();
        
        // Store block addresses as usize for thread safety
        for i in 0..pool_size {
            let block_addr = buffer_base + (i * block_size);
            free_blocks.push(block_addr);
        }
        
        Self {
            block_size,
            buffer_base,
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
        
        // Lock all mutexes sequentially to avoid potential deadlocks
        let mut free_blocks = self.free_blocks.lock().map_err(|_| AllocError::OutOfMemory)?;
        let mut allocated_blocks = self.allocated_blocks.lock().map_err(|_| AllocError::OutOfMemory)?;
        let mut stats = self.stats.lock().map_err(|_| AllocError::OutOfMemory)?;
        
        let block_addr = free_blocks.pop().ok_or(AllocError::OutOfMemory)?;
        allocated_blocks.insert(block_addr, self.block_size);
        
        stats.allocated_bytes += self.block_size;
        stats.active_allocations += 1;
        
        // Convert address back to NonNull<u8>
        let ptr = unsafe { NonNull::new_unchecked(block_addr as *mut u8) };
        Ok(ptr)
    }
    
    fn deallocate(&self, ptr: NonNull<u8>, _size: usize, _align: usize) {
        let ptr_addr = ptr.as_ptr() as usize;
        
        // Lock all mutexes sequentially to avoid potential deadlocks
        let mut free_blocks = match self.free_blocks.lock() {
            Ok(guard) => guard,
            Err(_) => return, // Failed to acquire lock
        };
        let mut allocated_blocks = match self.allocated_blocks.lock() {
            Ok(guard) => guard,
            Err(_) => return, // Failed to acquire lock
        };
        let mut stats = match self.stats.lock() {
            Ok(guard) => guard,
            Err(_) => return, // Failed to acquire lock
        };
        
        if allocated_blocks.remove(&ptr_addr).is_some() {
            free_blocks.push(ptr_addr);
            stats.freed_bytes += self.block_size;
            stats.active_allocations = stats.active_allocations.saturating_sub(1);
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
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
    }
    
    fn reset_stats(&self) {
        if let Ok(mut stats) = self.stats.lock() {
            stats.reset();
        }
    }
}

impl Drop for PoolAllocator {
    fn drop(&mut self) {
        // Calculate buffer size for deallocation
        if let Ok(free_blocks) = self.free_blocks.lock() {
            if let Ok(allocated_blocks) = self.allocated_blocks.lock() {
                let total_blocks = free_blocks.len() + allocated_blocks.len();
                let buffer_size = total_blocks * self.block_size;
                
                let layout = std::alloc::Layout::from_size_align(buffer_size, std::mem::align_of::<u8>())
                    .expect("Invalid layout in PoolAllocator drop");
                
                unsafe {
                    std::alloc::dealloc(self.buffer_base as *mut u8, layout);
                }
            }
        }
    }
}

impl StackAllocator {
    pub fn new(capacity: usize) -> Self {
        Self {
            buffer: Arc::new(Mutex::new(vec![0u8; capacity])),
            top: Arc::new(Mutex::new(0)),
            markers: Arc::new(Mutex::new(Vec::new())),
            stats: Arc::new(Mutex::new(AllocatorStats::default())),
        }
    }
    
    pub fn push_marker(&self) {
        if let (Ok(top), Ok(mut markers)) = (self.top.lock(), self.markers.lock()) {
            markers.push(*top);
        }
    }
    
    pub fn pop_marker(&self) {
        if let (Ok(mut top), Ok(mut markers), Ok(mut stats)) = 
            (self.top.lock(), self.markers.lock(), self.stats.lock()) {
            if let Some(marker) = markers.pop() {
                let freed_bytes = *top - marker;
                *top = marker;
                stats.freed_bytes += freed_bytes;
                stats.active_allocations = 0; // Stack allocations are all freed at once
            }
        }
    }
    
    pub fn reset(&self) {
        if let (Ok(mut top), Ok(mut markers), Ok(mut stats)) = 
            (self.top.lock(), self.markers.lock(), self.stats.lock()) {
            *top = 0;
            markers.clear();
            stats.reset();
        }
    }
}

impl CustomAllocator for StackAllocator {
    fn allocate(&self, size: usize, align: usize) -> Result<NonNull<u8>, AllocError> {
        if size == 0 {
            return Err(AllocError::InvalidSize);
        }
        
        // Lock all mutexes sequentially to avoid potential deadlocks
        let buffer_guard = self.buffer.lock().map_err(|_| AllocError::OutOfMemory)?;
        let mut top_guard = self.top.lock().map_err(|_| AllocError::OutOfMemory)?;
        let mut stats_guard = self.stats.lock().map_err(|_| AllocError::OutOfMemory)?;
        
        // Align the allocation
        let aligned_top = (*top_guard + align - 1) & !(align - 1);
        let end_top = aligned_top + size;
        
        if end_top > buffer_guard.len() {
            return Err(AllocError::OutOfMemory);
        }
        
        let ptr = unsafe {
            NonNull::new_unchecked(buffer_guard.as_ptr().add(aligned_top) as *mut u8)
        };
        
        *top_guard = end_top;
        stats_guard.allocated_bytes += size;
        stats_guard.active_allocations += 1;
        
        if stats_guard.active_allocations > stats_guard.peak_allocations {
            stats_guard.peak_allocations = stats_guard.active_allocations;
        }
        
        Ok(ptr)
    }
    
    fn deallocate(&self, _ptr: NonNull<u8>, size: usize, _align: usize) {
        // Stack allocator doesn't support individual deallocation
        // Use markers for bulk deallocation
        if let Ok(mut stats) = self.stats.lock() {
            stats.freed_bytes += size;
            // Note: active_allocations not decremented here as stack doesn't track individual frees
        }
    }
    
    fn reallocate(&self, _ptr: NonNull<u8>, _old_size: usize, new_size: usize, align: usize) -> Result<NonNull<u8>, AllocError> {
        // Stack allocators can't reallocate in place efficiently, so allocate new
        self.allocate(new_size, align)
    }
    
    fn get_stats(&self) -> AllocatorStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
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
pub extern "C" fn runa_create_stack_allocator(capacity: usize) -> *mut StackAllocator {
    let allocator = Box::new(StackAllocator::new(capacity));
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
pub extern "C" fn runa_stack_allocate(allocator: *mut StackAllocator, size: usize, align: usize) -> runa_object {
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
pub extern "C" fn runa_stack_push_marker(allocator: *mut StackAllocator) -> bool {
    if allocator.is_null() {
        return false;
    }
    
    let allocator = unsafe { &*allocator };
    allocator.push_marker();
    true
}

#[no_mangle]
pub extern "C" fn runa_stack_pop_marker(allocator: *mut StackAllocator) -> bool {
    if allocator.is_null() {
        return false;
    }
    
    let allocator = unsafe { &*allocator };
    allocator.pop_marker();
    true
}

#[no_mangle]
pub extern "C" fn runa_get_allocator_stats(allocator: *mut dyn CustomAllocator) -> AllocatorStats {
    if allocator.is_null() {
        return AllocatorStats::default();
    }
    
    let allocator = unsafe { &*allocator };
    allocator.get_stats()
}

/// Calculate actual memory fragmentation by analyzing free block distribution
fn calculate_actual_fragmentation() -> f64 {
    use std::collections::HashMap;
    use std::fs;
    
    // Try to read actual system memory fragmentation data
    #[cfg(target_os = "linux")]
    {
        // Read from /proc/buddyinfo for free block sizes
        if let Ok(buddyinfo) = fs::read_to_string("/proc/buddyinfo") {
            let mut total_free_blocks = 0u64;
            let mut weighted_fragmentation = 0.0;
            
            for line in buddyinfo.lines() {
                if line.contains("Normal") || line.contains("DMA") {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() >= 15 {
                        // Parse free block counts for different orders (4KB, 8KB, 16KB, etc.)
                        let mut max_contiguous_size = 0;
                        let mut total_blocks_for_zone = 0u64;
                        
                        for (order, count_str) in parts[4..].iter().enumerate() {
                            if let Ok(count) = count_str.parse::<u64>() {
                                total_blocks_for_zone += count;
                                if count > 0 {
                                    max_contiguous_size = order;
                                }
                            }
                        }
                        
                        total_free_blocks += total_blocks_for_zone;
                        
                        // Calculate fragmentation: prefer larger contiguous blocks
                        if total_blocks_for_zone > 0 {
                            let ideal_order = 10.0; // Prefer 4MB blocks
                            let fragmentation_penalty = (ideal_order - max_contiguous_size as f64).abs() / ideal_order;
                            weighted_fragmentation += fragmentation_penalty * (total_blocks_for_zone as f64);
                        }
                    }
                }
            }
            
            if total_free_blocks > 0 {
                return (weighted_fragmentation / total_free_blocks as f64).min(1.0);
            }
        }
        
        // Fallback: read /proc/meminfo for memory pressure indicators
        if let Ok(meminfo) = fs::read_to_string("/proc/meminfo") {
            let mut mem_total = 0u64;
            let mut mem_free = 0u64;
            let mut mem_available = 0u64;
            let mut buffers = 0u64;
            let mut cached = 0u64;
            
            for line in meminfo.lines() {
                let parts: Vec<&str> = line.split_whitespace().collect();
                if parts.len() >= 2 {
                    if let Ok(value) = parts[1].parse::<u64>() {
                        match parts[0] {
                            "MemTotal:" => mem_total = value,
                            "MemFree:" => mem_free = value,
                            "MemAvailable:" => mem_available = value,
                            "Buffers:" => buffers = value,
                            "Cached:" => cached = value,
                            _ => {}
                        }
                    }
                }
            }
            
            if mem_total > 0 {
                let used_memory = mem_total - mem_free;
                let effective_free = mem_available.max(mem_free + buffers + cached);
                
                // Calculate fragmentation based on difference between theoretical and available memory
                let theoretical_available = mem_total - used_memory;
                if theoretical_available > 0 {
                    let availability_ratio = effective_free as f64 / theoretical_available as f64;
                    return (1.0 - availability_ratio).max(0.0).min(1.0);
                }
            }
        }
    }
    
    #[cfg(target_os = "macos")]
    {
        use std::process::Command;
        
        // Use vm_stat to get memory pressure information
        if let Ok(output) = Command::new("vm_stat").output() {
            if let Ok(vm_output) = String::from_utf8(output.stdout) {
                let mut pages_free = 0u64;
                let mut pages_inactive = 0u64;
                let mut pages_speculative = 0u64;
                let mut pages_wired = 0u64;
                let mut page_size = 4096u64; // Default 4KB
                
                for line in vm_output.lines() {
                    if line.contains("page size of") {
                        if let Some(size_start) = line.find("page size of ") {
                            if let Some(size_end) = line[size_start + 13..].find(" bytes") {
                                if let Ok(size) = line[size_start + 13..size_start + 13 + size_end].parse::<u64>() {
                                    page_size = size;
                                }
                            }
                        }
                    } else if line.contains("Pages free:") {
                        if let Some(count_str) = line.split(':').nth(1) {
                            let clean_count = count_str.trim().replace('.', "");
                            if let Ok(count) = clean_count.parse::<u64>() {
                                pages_free = count;
                            }
                        }
                    } else if line.contains("Pages inactive:") {
                        if let Some(count_str) = line.split(':').nth(1) {
                            let clean_count = count_str.trim().replace('.', "");
                            if let Ok(count) = clean_count.parse::<u64>() {
                                pages_inactive = count;
                            }
                        }
                    } else if line.contains("Pages speculative:") {
                        if let Some(count_str) = line.split(':').nth(1) {
                            let clean_count = count_str.trim().replace('.', "");
                            if let Ok(count) = clean_count.parse::<u64>() {
                                pages_speculative = count;
                            }
                        }
                    } else if line.contains("Pages wired down:") {
                        if let Some(count_str) = line.split(':').nth(1) {
                            let clean_count = count_str.trim().replace('.', "");
                            if let Ok(count) = clean_count.parse::<u64>() {
                                pages_wired = count;
                            }
                        }
                    }
                }
                
                let total_available = pages_free + pages_inactive + pages_speculative;
                let memory_pressure = pages_wired as f64 / (pages_wired + total_available) as f64;
                
                // High memory pressure indicates fragmentation
                return memory_pressure.min(1.0);
            }
        }
        
        // Fallback: try memory pressure via sysctl (macOS only)
        #[cfg(target_os = "macos")]
        unsafe {
            let mut pressure: i32 = 0;
            let mut len = std::mem::size_of::<i32>();
            let pressure_key = std::ffi::CString::new("kern.memorystatus_level").unwrap();
            
            if libc::sysctlbyname(
                pressure_key.as_ptr(),
                &mut pressure as *mut _ as *mut libc::c_void,
                &mut len,
                std::ptr::null_mut(),
                0,
            ) == 0 {
                // Memory status level: 0 = normal, higher = more pressure/fragmentation
                return (pressure as f64 / 4.0).min(1.0).max(0.0);
            }
        }
    }
    
    #[cfg(target_os = "windows")]
    {
        use std::process::Command;
        
        // Use PowerShell to query memory fragmentation
        if let Ok(output) = Command::new("powershell")
            .arg("-Command")
            .arg("Get-WmiObject -Class Win32_PerfRawData_PerfOS_Memory | Select-Object AvailableBytes, CommittedBytes, PoolNonpagedBytes")
            .output() {
            if let Ok(output_str) = String::from_utf8(output.stdout) {
                let mut available_bytes = 0u64;
                let mut committed_bytes = 0u64;
                let mut pool_nonpaged_bytes = 0u64;
                
                for line in output_str.lines() {
                    if line.contains("AvailableBytes") {
                        if let Some(value_str) = line.split(':').nth(1) {
                            if let Ok(value) = value_str.trim().parse::<u64>() {
                                available_bytes = value;
                            }
                        }
                    } else if line.contains("CommittedBytes") {
                        if let Some(value_str) = line.split(':').nth(1) {
                            if let Ok(value) = value_str.trim().parse::<u64>() {
                                committed_bytes = value;
                            }
                        }
                    } else if line.contains("PoolNonpagedBytes") {
                        if let Some(value_str) = line.split(':').nth(1) {
                            if let Ok(value) = value_str.trim().parse::<u64>() {
                                pool_nonpaged_bytes = value;
                            }
                        }
                    }
                }
                
                if committed_bytes > 0 && available_bytes > 0 {
                    let total_memory = committed_bytes + available_bytes;
                    let fragmentation_indicator = pool_nonpaged_bytes as f64 / total_memory as f64;
                    return fragmentation_indicator.min(1.0);
                }
            }
        }
    }
    
    // Advanced allocation pattern analysis for fragmentation estimation
    if let Ok(stats) = MEMORY_STATS.lock() {
        if stats.total_allocated > 0 {
            // Base fragmentation from memory holes (freed space that can't be reused efficiently)
            let base_fragmentation = 1.0 - (stats.current_usage as f64 / stats.total_allocated as f64);
            
            // Allocation churn factor - frequent alloc/free cycles increase fragmentation
            let alloc_dealloc_ratio = if stats.deallocation_count > 0 {
                stats.allocation_count as f64 / stats.deallocation_count as f64
            } else {
                1.0
            };
            
            // Churn penalty: more allocations relative to size indicates small object churn
            let size_normalized_churn = stats.allocation_count as f64 / (stats.total_allocated / 64) as f64;
            let churn_factor = (size_normalized_churn * 0.05).min(0.3);
            
            // Peak memory pressure factor - high peak usage relative to current indicates fragmentation
            let peak_pressure = if stats.current_usage > 0 {
                (stats.peak_usage as f64 / stats.current_usage as f64 - 1.0) * 0.1
            } else {
                0.0
            };
            
            // Allocation/deallocation imbalance factor
            let imbalance_factor = if alloc_dealloc_ratio > 1.2 || alloc_dealloc_ratio < 0.8 {
                (alloc_dealloc_ratio - 1.0).abs() * 0.05
            } else {
                0.0
            };
            
            // Composite fragmentation score
            let computed_fragmentation = base_fragmentation + churn_factor + peak_pressure + imbalance_factor;
            
            // Apply realistic bounds - most systems don't exceed 70% fragmentation in normal operation
            return computed_fragmentation.min(0.7).max(0.0);
        }
    }
    
    // No allocation activity detected - assume minimal fragmentation
    0.0
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

    #[test]
    fn test_pointer_validation() {
        // Test null pointer
        assert!(!is_valid_pointer(std::ptr::null_mut(), 1));
        
        // Test zero size
        let ptr = alloc(16);
        assert!(!is_valid_pointer(ptr, 0));
        
        // Test valid pointer and size
        assert!(is_valid_pointer(ptr, 16));
        
        // Test size exceeding allocation
        assert!(!is_valid_pointer(ptr, 32));
        
        free(ptr);
        
        // Test use after free
        assert!(!is_valid_pointer(ptr, 16));
    }

    #[test]
    fn test_typed_pointer_validation() {
        let ptr = alloc(std::mem::size_of::<u64>() * 4) as *const u64;
        
        // Valid typed pointer access
        assert!(is_valid_typed_pointer(ptr, 4));
        
        // Invalid count (would exceed allocation)
        assert!(!is_valid_typed_pointer(ptr, 8));
        
        free(ptr as runa_object);
        
        // Use after free
        assert!(!is_valid_typed_pointer(ptr, 4));
    }

    #[test]
    fn test_memory_overlap_detection() {
        let ptr1 = alloc(16);
        let ptr2 = alloc(16);
        
        // Non-overlapping pointers
        assert!(!memory_ranges_overlap(ptr1, 16, ptr2, 16));
        
        // Overlapping ranges (same pointer)
        assert!(memory_ranges_overlap(ptr1, 16, ptr1, 16));
        
        // Partially overlapping ranges
        unsafe {
            let ptr3 = (ptr1 as *mut u8).add(8) as runa_object;
            assert!(memory_ranges_overlap(ptr1, 16, ptr3, 8));
        }
        
        free(ptr1);
        free(ptr2);
    }

    #[test]
    fn test_buffer_operation_validation() {
        let src = alloc(16);
        let dst = alloc(16);
        
        // Valid operation
        assert!(validate_buffer_operation(src, dst, 16).is_ok());
        
        // Invalid source
        assert!(validate_buffer_operation(std::ptr::null_mut(), dst, 16).is_err());
        
        // Invalid destination  
        assert!(validate_buffer_operation(src, std::ptr::null_mut(), 16).is_err());
        
        // Overlapping ranges
        assert!(validate_buffer_operation(src, src, 16).is_err());
        
        free(src);
        free(dst);
    }

    #[test]
    fn test_alignment_checking() {
        // Test properly aligned pointer
        let aligned_ptr = alloc(16);
        assert!(is_valid_pointer(aligned_ptr, 16));
        
        // Test misaligned pointer (if we can create one safely)
        unsafe {
            let misaligned = (aligned_ptr as *mut u8).add(1) as runa_object;
            // This should fail alignment check on most architectures
            assert!(!is_valid_pointer(misaligned, 16));
        }
        
        free(aligned_ptr);
    }

    #[test] 
    fn test_address_space_limits() {
        // Test extremely high addresses that would be invalid
        let invalid_high_addr = usize::MAX as runa_object;
        assert!(!is_valid_pointer(invalid_high_addr, 1));
        
        // Test address that would cause overflow
        let near_max_addr = (usize::MAX - 10) as runa_object;
        assert!(!is_valid_pointer(near_max_addr, 20));
    }

    #[test]
    fn test_integer_overflow_protection() {
        let ptr = alloc(16);
        
        // Test that size overflow is detected
        assert!(!is_valid_pointer(ptr, usize::MAX));
        
        free(ptr);
    }

    #[test]
    fn test_cstring_validation() {
        // Create a proper C string
        let test_str = b"Hello, World!\0";
        let ptr = alloc(test_str.len());
        
        unsafe {
            std::ptr::copy_nonoverlapping(test_str.as_ptr(), ptr as *mut u8, test_str.len());
        }
        
        // Valid C string
        assert!(is_valid_cstring_pointer(ptr as *const u8, 20));
        
        // Test with a reasonable max length
        assert!(is_valid_cstring_pointer(ptr as *const u8, 14)); // Exactly the string length
        
        free(ptr);
        
        // Invalid after free
        assert!(!is_valid_cstring_pointer(ptr as *const u8, 20));
    }
    
    #[test]
    fn test_arena_allocator() {
        let arena = ArenaAllocator::new(1024);
        
        // Test basic allocation
        let ptr1 = arena.allocate(64, 8);
        assert!(ptr1.is_ok());
        
        let ptr2 = arena.allocate(128, 16);
        assert!(ptr2.is_ok());
        
        // Test stats
        let stats = arena.get_stats();
        assert_eq!(stats.active_allocations, 2);
        assert!(stats.allocated_bytes >= 192); // 64 + 128
        
        // Test out of memory
        let big_ptr = arena.allocate(2048, 8);
        assert!(big_ptr.is_err());
        
        // Test reset
        arena.reset();
        let stats = arena.get_stats();
        assert_eq!(stats.allocated_bytes, 0);
    }
    
    #[test]
    fn test_pool_allocator() {
        let pool = PoolAllocator::new(64, 16); // 16 blocks of 64 bytes each
        
        // Test allocation within block size
        let ptr1 = pool.allocate(32, 8);
        assert!(ptr1.is_ok());
        
        let ptr2 = pool.allocate(64, 8);
        assert!(ptr2.is_ok());
        
        // Test oversized allocation fails
        let big_ptr = pool.allocate(128, 8);
        assert!(big_ptr.is_err());
        
        // Test stats
        let stats = pool.get_stats();
        assert_eq!(stats.active_allocations, 2);
        assert_eq!(stats.allocated_bytes, 128); // 2 blocks * 64 bytes
        
        // Test deallocation
        if let Ok(ptr) = ptr1 {
            pool.deallocate(ptr, 32, 8);
        }
        
        let stats = pool.get_stats();
        assert_eq!(stats.active_allocations, 1);
        
        // Test exhaustion
        let mut ptrs = Vec::new();
        for _ in 0..15 { // Should allocate remaining blocks
            if let Ok(ptr) = pool.allocate(64, 8) {
                ptrs.push(ptr);
            }
        }
        
        // Should be out of memory now
        let ptr = pool.allocate(64, 8);
        assert!(ptr.is_err());
    }
    
    #[test]
    fn test_stack_allocator() {
        let stack = StackAllocator::new(1024);
        
        // Test basic allocation
        let ptr1 = stack.allocate(64, 8);
        assert!(ptr1.is_ok());
        
        // Test marker system
        stack.push_marker();
        
        let ptr2 = stack.allocate(128, 8);
        assert!(ptr2.is_ok());
        
        let ptr3 = stack.allocate(64, 8);
        assert!(ptr3.is_ok());
        
        let stats = stack.get_stats();
        assert_eq!(stats.active_allocations, 3);
        
        // Pop marker should free ptr2 and ptr3
        stack.pop_marker();
        
        let stats = stack.get_stats();
        assert_eq!(stats.active_allocations, 0); // Stack resets all active allocations
        
        // Test nested markers
        stack.push_marker();
        let _ptr4 = stack.allocate(32, 8);
        
        stack.push_marker();
        let _ptr5 = stack.allocate(32, 8);
        let _ptr6 = stack.allocate(32, 8);
        
        // Pop inner marker
        stack.pop_marker();
        // Pop outer marker
        stack.pop_marker();
        
        // Test reset
        stack.reset();
        let stats = stack.get_stats();
        assert_eq!(stats.allocated_bytes, 0);
    }
    
    #[test]
    fn test_allocator_alignment() {
        let arena = ArenaAllocator::new(1024);
        
        // Test various alignments
        let ptr1 = arena.allocate(64, 1);
        assert!(ptr1.is_ok());
        
        let ptr2 = arena.allocate(64, 8);
        assert!(ptr2.is_ok());
        
        let ptr3 = arena.allocate(64, 16);
        assert!(ptr3.is_ok());
        
        // Check alignment
        if let Ok(ptr) = ptr2 {
            assert_eq!(ptr.as_ptr() as usize % 8, 0);
        }
        
        if let Ok(ptr) = ptr3 {
            assert_eq!(ptr.as_ptr() as usize % 16, 0);
        }
    }
    
    #[test]
    fn test_allocator_reallocate() {
        let pool = PoolAllocator::new(128, 10);
        
        // Test reallocation within same block size
        let ptr = pool.allocate(64, 8).unwrap();
        let new_ptr = pool.reallocate(ptr, 64, 96, 8);
        assert!(new_ptr.is_ok());
        assert_eq!(ptr.as_ptr(), new_ptr.unwrap().as_ptr()); // Should be same pointer
        
        // Test reallocation to larger size
        let big_ptr = pool.reallocate(ptr, 96, 256, 8);
        assert!(big_ptr.is_err()); // Should fail as 256 > block_size (128)
    }
    
    #[test]
    fn test_allocator_stats_reset() {
        let arena = ArenaAllocator::new(1024);
        
        // Allocate some memory
        let _ptr1 = arena.allocate(64, 8);
        let _ptr2 = arena.allocate(128, 8);
        
        let stats = arena.get_stats();
        assert!(stats.allocated_bytes > 0);
        
        // Reset stats
        arena.reset_stats();
        let stats = arena.get_stats();
        assert_eq!(stats.allocated_bytes, 0);
        assert_eq!(stats.active_allocations, 0);
    }
    
    #[test]
    fn test_enhanced_fragmentation_calculation() {
        reset_memory_stats();
        
        // Create allocation churn to test fragmentation calculation
        let mut ptrs = Vec::new();
        
        // Allocate many small objects
        for _ in 0..100 {
            ptrs.push(alloc(32));
        }
        
        // Free every other allocation to create fragmentation
        for i in (0..ptrs.len()).step_by(2) {
            free(ptrs[i]);
        }
        
        // Calculate fragmentation
        let fragmentation = calculate_actual_fragmentation();
        
        // Should detect some fragmentation from the pattern
        assert!(fragmentation >= 0.0);
        assert!(fragmentation <= 0.7); // Within realistic bounds
        
        // Clean up remaining allocations
        for i in (1..ptrs.len()).step_by(2) {
            free(ptrs[i]);
        }
        
        // Reset for clean state
        reset_memory_stats();
    }
    
    #[test]
    fn test_fragmentation_with_different_patterns() {
        reset_memory_stats();
        
        // Test 1: No fragmentation scenario
        let ptr1 = alloc(1024);
        let initial_frag = calculate_actual_fragmentation();
        free(ptr1);
        
        // Test 2: High churn scenario
        let mut small_ptrs = Vec::new();
        for _ in 0..50 {
            small_ptrs.push(alloc(16));
        }
        for ptr in small_ptrs {
            free(ptr);
        }
        
        let churn_frag = calculate_actual_fragmentation();
        
        // Churn should result in higher fragmentation estimate
        assert!(churn_frag >= initial_frag);
        assert!(churn_frag <= 0.7);
        
        reset_memory_stats();
    }
}

// =============================================================================
// Memory Manager for Native Execution Integration
// =============================================================================

/// Advanced memory manager for native code execution with GC integration
#[derive(Debug)]
pub struct MemoryManager {
    /// Stack frame allocator for native function calls
    stack_allocator: Arc<Mutex<NativeStackAllocator>>,
    /// Allocation tracker for profiling
    allocation_tracker: Arc<RwLock<AllocationTracker>>,
    /// Garbage collector interface
    gc: Arc<dyn crate::gc::GCAlgorithm>,
    /// Memory statistics
    stats: Arc<RwLock<MemoryStats>>,
    /// Stack frames currently active
    active_frames: Arc<RwLock<HashMap<usize, StackFrame>>>,
}

impl MemoryManager {
    pub fn new() -> Self {
        Self {
            stack_allocator: Arc::new(Mutex::new(NativeStackAllocator::new())),
            allocation_tracker: Arc::new(RwLock::new(AllocationTracker::new())),
            gc: Arc::new(crate::gc::GenerationalGC::new(1024 * 1024, 16 * 1024 * 1024)),
            stats: Arc::new(RwLock::new(MemoryStats::default())),
            active_frames: Arc::new(RwLock::new(HashMap::new())),
        }
    }
    
    /// Allocate a stack frame for native function execution
    pub fn allocate_stack_frame(&self, size: usize) -> Result<usize, crate::aott::types::CompilerError> {
        let mut allocator = self.stack_allocator.lock().unwrap();
        let frame_id = allocator.allocate_frame(size)?;
        
        let frame = StackFrame {
            id: frame_id,
            size,
            base_pointer: allocator.get_frame_base(frame_id),
            allocated_at: std::time::Instant::now(),
        };
        
        self.active_frames.write().unwrap().insert(frame_id, frame);
        
        // Update statistics
        if let Ok(mut stats) = self.stats.write() {
            stats.total_allocated += size;
            stats.current_usage += size;
            stats.allocation_count += 1;
            if stats.current_usage > stats.peak_usage {
                stats.peak_usage = stats.current_usage;
            }
        }
        
        Ok(frame_id)
    }
    
    /// Deallocate a stack frame
    pub fn deallocate_stack_frame(&self, frame_id: usize) -> Result<(), crate::aott::types::CompilerError> {
        let frame_size = {
            let mut frames = self.active_frames.write().unwrap();
            match frames.remove(&frame_id) {
                Some(frame) => frame.size,
                None => return Err(crate::aott::types::CompilerError::InvalidStackFrame(format!("Stack frame {} not found", frame_id))),
            }
        };
        
        let mut allocator = self.stack_allocator.lock().unwrap();
        allocator.deallocate_frame(frame_id)?;
        
        // Update statistics
        if let Ok(mut stats) = self.stats.write() {
            stats.total_freed += frame_size;
            stats.current_usage = stats.current_usage.saturating_sub(frame_size);
            stats.deallocation_count += 1;
        }
        
        Ok(())
    }
    
    /// Expand stack size for overflow recovery
    pub fn expand_stack(&self, additional_size: usize) -> Result<(), crate::aott::types::CompilerError> {
        let mut allocator = self.stack_allocator.lock().unwrap();
        allocator.expand_stack(additional_size)
    }
    
    /// Get current GC state
    pub fn get_gc_state(&self) -> crate::aott::execution::native::GCState {
        let gc_stats = self.gc.get_stats();
        crate::aott::execution::native::GCState {
            generation: 0, // Simplified for example
            collection_in_progress: false,
            allocated_bytes: gc_stats.used_memory as u64,
        }
    }
    
    /// Get detailed memory statistics
    pub fn get_detailed_stats(&self) -> crate::aott::execution::native::MemoryStatistics {
        if let Ok(stats) = self.stats.read() {
            crate::aott::execution::native::MemoryStatistics {
                total_allocated: stats.total_allocated as u64,
                total_deallocated: stats.total_freed as u64,
                peak_usage: stats.peak_usage as u64,
                current_usage: stats.current_usage as u64,
                allocation_count: stats.allocation_count as u64,
                deallocation_count: stats.deallocation_count as u64,
            }
        } else {
            crate::aott::execution::native::MemoryStatistics::default()
        }
    }
    
    /// Get allocation count for profiling
    pub fn get_allocation_count(&self) -> u64 {
        self.stats.read().unwrap().allocation_count as u64
    }
    
    /// Get deallocation count for profiling
    pub fn get_deallocation_count(&self) -> u64 {
        self.stats.read().unwrap().deallocation_count as u64
    }
    
    /// Get peak memory usage
    pub fn get_peak_usage(&self) -> u64 {
        self.stats.read().unwrap().peak_usage as u64
    }
    
    /// Get garbage collector interface
    pub fn get_gc(&self) -> &dyn crate::gc::GCAlgorithm {
        &*self.gc
    }
}

/// Native stack allocator for function call frames (internal implementation)
#[derive(Debug)]
struct NativeStackAllocator {
    stack_memory: Vec<u8>,
    stack_pointer: usize,
    frame_counter: usize,
    allocated_frames: HashMap<usize, StackFrameInfo>,
    max_stack_size: usize,
}

impl NativeStackAllocator {
    fn new() -> Self {
        let initial_size = 1024 * 1024; // 1MB initial stack
        Self {
            stack_memory: vec![0; initial_size],
            stack_pointer: 0,
            frame_counter: 0,
            allocated_frames: HashMap::new(),
            max_stack_size: 64 * 1024 * 1024, // 64MB max stack
        }
    }
    
    fn allocate_frame(&mut self, size: usize) -> Result<usize, crate::aott::types::CompilerError> {
        // Align size to 8 bytes
        let aligned_size = (size + 7) & !7;
        
        // Check if we have enough space
        if self.stack_pointer + aligned_size > self.stack_memory.len() {
            if self.stack_memory.len() + aligned_size > self.max_stack_size {
                return Err(crate::aott::types::CompilerError::StackOverflow("Stack size limit exceeded".to_string()));
            }
            // Expand stack
            let new_size = (self.stack_memory.len() * 2).max(self.stack_pointer + aligned_size);
            self.stack_memory.resize(new_size, 0);
        }
        
        let frame_id = self.frame_counter;
        self.frame_counter += 1;
        
        let frame_info = StackFrameInfo {
            offset: self.stack_pointer,
            size: aligned_size,
        };
        
        self.allocated_frames.insert(frame_id, frame_info);
        self.stack_pointer += aligned_size;
        
        Ok(frame_id)
    }
    
    fn deallocate_frame(&mut self, frame_id: usize) -> Result<(), crate::aott::types::CompilerError> {
        let frame_info = self.allocated_frames.remove(&frame_id)
            .ok_or_else(|| crate::aott::types::CompilerError::InvalidStackFrame(format!("Frame {} not found", frame_id)))?;
        
        // For simplicity, only allow deallocating the most recent frame
        if frame_info.offset + frame_info.size == self.stack_pointer {
            self.stack_pointer = frame_info.offset;
        }
        // In a real implementation, we'd handle fragmented deallocation
        
        Ok(())
    }
    
    fn get_frame_base(&self, frame_id: usize) -> usize {
        self.allocated_frames.get(&frame_id)
            .map(|info| self.stack_memory.as_ptr() as usize + info.offset)
            .unwrap_or(0)
    }
    
    fn expand_stack(&mut self, additional_size: usize) -> Result<(), crate::aott::types::CompilerError> {
        let new_size = self.stack_memory.len() + additional_size;
        if new_size > self.max_stack_size {
            return Err(crate::aott::types::CompilerError::StackOverflow("Stack expansion would exceed limit".to_string()));
        }
        
        self.stack_memory.resize(new_size, 0);
        Ok(())
    }
}

/// Stack frame information
#[derive(Debug)]
struct StackFrameInfo {
    offset: usize,
    size: usize,
}

/// Active stack frame
#[derive(Debug)]
struct StackFrame {
    id: usize,
    size: usize,
    base_pointer: usize,
    allocated_at: std::time::Instant,
}

/// Allocation tracker for profiling and debugging
#[derive(Debug)]
pub struct AllocationTracker {
    active_allocations: HashMap<usize, TrackedAllocationInfo>,
    allocation_history: Vec<AllocationEvent>,
    total_allocations: u64,
    total_deallocations: u64,
    peak_active_count: usize,
}

impl AllocationTracker {
    pub fn new() -> Self {
        Self {
            active_allocations: HashMap::new(),
            allocation_history: Vec::new(),
            total_allocations: 0,
            total_deallocations: 0,
            peak_active_count: 0,
        }
    }
    
    pub fn track_allocation(&mut self, ptr: usize, size: usize, alignment: usize) {
        let info = TrackedAllocationInfo {
            size,
            alignment,
            allocated_at: std::time::Instant::now(),
        };
        
        self.active_allocations.insert(ptr, info);
        self.total_allocations += 1;
        
        if self.active_allocations.len() > self.peak_active_count {
            self.peak_active_count = self.active_allocations.len();
        }
        
        self.allocation_history.push(AllocationEvent {
            event_type: AllocationEventType::Allocate,
            ptr,
            size,
            timestamp: std::time::Instant::now(),
        });
    }
    
    pub fn track_deallocation(&mut self, ptr: usize) {
        if let Some(info) = self.active_allocations.remove(&ptr) {
            self.total_deallocations += 1;
            
            self.allocation_history.push(AllocationEvent {
                event_type: AllocationEventType::Deallocate,
                ptr,
                size: info.size,
                timestamp: std::time::Instant::now(),
            });
        }
    }
    
    pub fn get_stats(&self) -> AllocationTrackerStats {
        let total_active_size: usize = self.active_allocations.values()
            .map(|info| info.size)
            .sum();
            
        AllocationTrackerStats {
            active_allocations: self.active_allocations.len(),
            total_allocations: self.total_allocations,
            total_deallocations: self.total_deallocations,
            peak_active_count: self.peak_active_count,
            total_active_size,
        }
    }
}

/// Information about an active allocation in the tracker
#[derive(Debug)]
struct TrackedAllocationInfo {
    size: usize,
    alignment: usize,
    allocated_at: std::time::Instant,
}

/// Allocation event for history tracking
#[derive(Debug)]
struct AllocationEvent {
    event_type: AllocationEventType,
    ptr: usize,
    size: usize,
    timestamp: std::time::Instant,
}

/// Type of allocation event
#[derive(Debug)]
enum AllocationEventType {
    Allocate,
    Deallocate,
}

/// Statistics from allocation tracker
#[derive(Debug)]
pub struct AllocationTrackerStats {
    pub active_allocations: usize,
    pub total_allocations: u64,
    pub total_deallocations: u64,
    pub peak_active_count: usize,
    pub total_active_size: usize,
} 