// Memory management utilities for the bootstrap compiler

use std::alloc::{GlobalAlloc, Layout, System};
use std::ptr::NonNull;

// Simple wrapper around system allocator for now
pub struct RunaAllocator;

unsafe impl GlobalAlloc for RunaAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        System.alloc(layout)
    }
    
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        System.dealloc(ptr, layout)
    }
}

// Memory pool for small allocations
pub struct MemoryPool {
    blocks: Vec<Vec<u8>>,
    block_size: usize,
    current_block: usize,
    current_offset: usize,
}

impl MemoryPool {
    pub fn new(block_size: usize) -> Self {
        Self {
            blocks: vec![vec![0; block_size]],
            block_size,
            current_block: 0,
            current_offset: 0,
        }
    }
    
    pub fn allocate(&mut self, size: usize, align: usize) -> Option<NonNull<u8>> {
        // Align current offset
        let aligned_offset = (self.current_offset + align - 1) & !(align - 1);
        
        // Check if allocation fits in current block
        if aligned_offset + size > self.block_size {
            // Need new block
            self.blocks.push(vec![0; self.block_size]);
            self.current_block += 1;
            self.current_offset = 0;
            let aligned_offset = (self.current_offset + align - 1) & !(align - 1);
            
            if aligned_offset + size > self.block_size {
                // Allocation too large for block size
                return None;
            }
        }
        
        let ptr = unsafe {
            self.blocks[self.current_block]
                .as_mut_ptr()
                .add(aligned_offset)
        };
        
        self.current_offset = aligned_offset + size;
        
        NonNull::new(ptr)
    }
    
    pub fn reset(&mut self) {
        self.current_block = 0;
        self.current_offset = 0;
    }
}

// Stack allocator for temporary allocations
pub struct StackAllocator {
    buffer: Vec<u8>,
    top: usize,
    markers: Vec<usize>,
}

impl StackAllocator {
    pub fn new(capacity: usize) -> Self {
        Self {
            buffer: vec![0; capacity],
            top: 0,
            markers: Vec::new(),
        }
    }
    
    pub fn push_marker(&mut self) {
        self.markers.push(self.top);
    }
    
    pub fn pop_to_marker(&mut self) -> bool {
        if let Some(marker) = self.markers.pop() {
            self.top = marker;
            true
        } else {
            false
        }
    }
    
    pub fn allocate(&mut self, size: usize, align: usize) -> Option<NonNull<u8>> {
        let aligned_top = (self.top + align - 1) & !(align - 1);
        
        if aligned_top + size > self.buffer.len() {
            return None;
        }
        
        let ptr = unsafe { self.buffer.as_mut_ptr().add(aligned_top) };
        self.top = aligned_top + size;
        
        NonNull::new(ptr)
    }
}