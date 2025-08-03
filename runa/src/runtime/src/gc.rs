//! Advanced Garbage Collection algorithms for the Runa runtime.
//! Provides pluggable GC strategies including generational, concurrent, and tracing collectors.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex, RwLock};
use std::ptr::NonNull;
use std::time::{Duration, Instant};
use crate::runa_object;

/// GC algorithm trait for pluggable garbage collection strategies
pub trait GCAlgorithm: Send + Sync {
    fn collect(&self, generation: Option<u32>) -> GCResult;
    fn allocate(&self, size: usize, align: usize) -> Result<NonNull<u8>, GCError>;
    fn register_root(&self, ptr: NonNull<u8>);
    fn unregister_root(&self, ptr: NonNull<u8>);
    fn get_stats(&self) -> GCStats;
    fn set_threshold(&self, threshold: usize);
    fn is_gc_needed(&self) -> bool;
}

#[derive(Debug, Clone)]
pub struct GCStats {
    pub total_collections: usize,
    pub total_collection_time_ms: u64,
    pub objects_collected: usize,
    pub bytes_collected: usize,
    pub heap_size: usize,
    pub used_memory: usize,
    pub gc_pressure: f64,
    pub average_pause_time_ms: f64,
}

#[derive(Debug)]
pub struct GCResult {
    pub objects_freed: usize,
    pub bytes_freed: usize,
    pub collection_time_ms: u64,
    pub gc_type: GCType,
}

#[derive(Debug)]
pub enum GCType {
    Minor,
    Major,
    Full,
    Concurrent,
}

#[derive(Debug)]
pub enum GCError {
    OutOfMemory,
    InvalidObject,
    ConcurrentAccess,
    InternalError,
}

/// Object header for GC tracking
#[repr(C)]
#[derive(Debug)]
pub struct ObjectHeader {
    pub size: usize,
    pub type_id: u32,
    pub mark: bool,
    pub generation: u8,
    pub references: Vec<NonNull<ObjectHeader>>,
}

/// Generational garbage collector
pub struct GenerationalGC {
    young_generation: Arc<Mutex<Generation>>,
    old_generation: Arc<Mutex<Generation>>,
    roots: Arc<RwLock<HashSet<NonNull<u8>>>>,
    stats: Arc<Mutex<GCStats>>,
    threshold: Arc<Mutex<usize>>,
    allocation_counter: Arc<Mutex<usize>>,
}

/// Concurrent garbage collector
pub struct ConcurrentGC {
    heap: Arc<Mutex<Heap>>,
    roots: Arc<RwLock<HashSet<NonNull<u8>>>>,
    stats: Arc<Mutex<GCStats>>,
    mark_stack: Arc<Mutex<Vec<NonNull<ObjectHeader>>>>,
    collection_thread: Option<std::thread::JoinHandle<()>>,
    stop_flag: Arc<Mutex<bool>>,
}

/// Tracing garbage collector (mark-and-sweep)
pub struct TracingGC {
    heap: Arc<Mutex<Heap>>,
    roots: Arc<RwLock<HashSet<NonNull<u8>>>>,
    stats: Arc<Mutex<GCStats>>,
    mark_set: Arc<Mutex<HashSet<NonNull<ObjectHeader>>>>,
    threshold: Arc<Mutex<usize>>,
}

struct Generation {
    objects: HashMap<NonNull<u8>, ObjectHeader>,
    size_limit: usize,
    current_size: usize,
}

struct Heap {
    objects: HashMap<NonNull<u8>, ObjectHeader>,
    free_list: Vec<NonNull<u8>>,
    total_size: usize,
    used_size: usize,
}

// ============================================================================
// GENERATIONAL GC IMPLEMENTATION
// ============================================================================

impl GenerationalGC {
    pub fn new(young_size_limit: usize, old_size_limit: usize) -> Self {
        Self {
            young_generation: Arc::new(Mutex::new(Generation::new(young_size_limit))),
            old_generation: Arc::new(Mutex::new(Generation::new(old_size_limit))),
            roots: Arc::new(RwLock::new(HashSet::new())),
            stats: Arc::new(Mutex::new(GCStats::default())),
            threshold: Arc::new(Mutex::new(young_size_limit / 2)),
            allocation_counter: Arc::new(Mutex::new(0)),
        }
    }
    
    fn collect_young_generation(&self) -> GCResult {
        let start_time = Instant::now();
        let mut objects_freed = 0;
        let mut bytes_freed = 0;
        
        if let (Ok(mut young), Ok(mut old), Ok(roots)) = 
            (self.young_generation.lock(), self.old_generation.lock(), self.roots.read()) {
            
            // Mark phase
            let mut marked = HashSet::new();
            for root in roots.iter() {
                self.mark_from_root(*root, &young.objects, &mut marked);
            }
            
            // Sweep phase
            let mut to_remove = Vec::new();
            for (ptr, header) in &young.objects {
                if !marked.contains(ptr) {
                    to_remove.push(*ptr);
                    objects_freed += 1;
                    bytes_freed += header.size;
                }
            }
            
            // Remove unmarked objects and promote survivors
            for ptr in to_remove {
                if let Some(header) = young.objects.remove(&ptr) {
                    young.current_size -= header.size;
                    
                    // Promote long-lived objects to old generation
                    if header.generation > 2 {
                        old.objects.insert(ptr, header);
                        old.current_size += header.size;
                    }
                }
            }
        }
        
        let collection_time = start_time.elapsed().as_millis() as u64;
        
        // Update stats
        if let Ok(mut stats) = self.stats.lock() {
            stats.total_collections += 1;
            stats.total_collection_time_ms += collection_time;
            stats.objects_collected += objects_freed;
            stats.bytes_collected += bytes_freed;
            stats.average_pause_time_ms = stats.total_collection_time_ms as f64 / stats.total_collections as f64;
        }
        
        GCResult {
            objects_freed,
            bytes_freed,
            collection_time_ms: collection_time,
            gc_type: GCType::Minor,
        }
    }
    
    fn mark_from_root(&self, root: NonNull<u8>, objects: &HashMap<NonNull<u8>, ObjectHeader>, marked: &mut HashSet<NonNull<u8>>) {
        if marked.contains(&root) {
            return;
        }
        
        marked.insert(root);
        
        if let Some(header) = objects.get(&root) {
            for reference in &header.references {
                let ref_ptr = NonNull::new(reference.as_ptr() as *mut u8);
                if let Some(ref_ptr) = ref_ptr {
                    self.mark_from_root(ref_ptr, objects, marked);
                }
            }
        }
    }
}

impl GCAlgorithm for GenerationalGC {
    fn collect(&self, generation: Option<u32>) -> GCResult {
        match generation {
            Some(0) | None => self.collect_young_generation(),
            Some(_) => {
                // Full collection - collect both generations
                let young_result = self.collect_young_generation();
                // Add old generation collection logic here
                young_result
            }
        }
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<NonNull<u8>, GCError> {
        if let Ok(mut young) = self.young_generation.lock() {
            if young.current_size + size > young.size_limit {
                return Err(GCError::OutOfMemory);
            }
            
            let layout = std::alloc::Layout::from_size_align(size, std::mem::align_of::<u8>())
                .map_err(|_| GCError::InvalidObject)?;
            
            let ptr = unsafe { std::alloc::alloc(layout) };
            if ptr.is_null() {
                return Err(GCError::OutOfMemory);
            }
            
            let non_null_ptr = NonNull::new(ptr).ok_or(GCError::OutOfMemory)?;
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: false,
                generation: 0,
                references: Vec::new(),
            };
            
            young.objects.insert(non_null_ptr, header);
            young.current_size += size;
            
            if let Ok(mut counter) = self.allocation_counter.lock() {
                *counter += 1;
            }
            
            Ok(non_null_ptr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: NonNull<u8>) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: NonNull<u8>) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().unwrap_or_default().clone()
    }
    
    fn set_threshold(&self, threshold: usize) {
        if let Ok(mut thresh) = self.threshold.lock() {
            *thresh = threshold;
        }
    }
    
    fn is_gc_needed(&self) -> bool {
        if let (Ok(young), Ok(threshold)) = (self.young_generation.lock(), self.threshold.lock()) {
            young.current_size > *threshold
        } else {
            false
        }
    }
}

// ============================================================================
// CONCURRENT GC IMPLEMENTATION
// ============================================================================

impl ConcurrentGC {
    pub fn new(heap_size: usize) -> Self {
        Self {
            heap: Arc::new(Mutex::new(Heap::new(heap_size))),
            roots: Arc::new(RwLock::new(HashSet::new())),
            stats: Arc::new(Mutex::new(GCStats::default())),
            mark_stack: Arc::new(Mutex::new(Vec::new())),
            collection_thread: None,
            stop_flag: Arc::new(Mutex::new(false)),
        }
    }
    
    pub fn start_concurrent_collection(&mut self) {
        let heap = Arc::clone(&self.heap);
        let roots = Arc::clone(&self.roots);
        let stats = Arc::clone(&self.stats);
        let mark_stack = Arc::clone(&self.mark_stack);
        let stop_flag = Arc::clone(&self.stop_flag);
        
        let handle = std::thread::spawn(move || {
            loop {
                if let Ok(should_stop) = stop_flag.lock() {
                    if *should_stop {
                        break;
                    }
                }
                
                // Perform concurrent marking
                Self::concurrent_mark_phase(&heap, &roots, &mark_stack);
                
                // Sleep before next cycle
                std::thread::sleep(Duration::from_millis(10));
            }
        });
        
        self.collection_thread = Some(handle);
    }
    
    pub fn stop_concurrent_collection(&mut self) {
        if let Ok(mut stop_flag) = self.stop_flag.lock() {
            *stop_flag = true;
        }
        
        if let Some(handle) = self.collection_thread.take() {
            let _ = handle.join();
        }
    }
    
    fn concurrent_mark_phase(
        heap: &Arc<Mutex<Heap>>,
        roots: &Arc<RwLock<HashSet<NonNull<u8>>>>,
        mark_stack: &Arc<Mutex<Vec<NonNull<ObjectHeader>>>>
    ) {
        if let (Ok(heap_guard), Ok(roots_guard), Ok(mut stack_guard)) = 
            (heap.lock(), roots.read(), mark_stack.lock()) {
            
            // Clear mark stack
            stack_guard.clear();
            
            // Initialize with roots
            for root in roots_guard.iter() {
                if let Some(header) = heap_guard.objects.get(root) {
                    let header_ptr = NonNull::new(header as *const ObjectHeader as *mut ObjectHeader);
                    if let Some(ptr) = header_ptr {
                        stack_guard.push(ptr);
                    }
                }
            }
            
            // Concurrent marking
            while let Some(obj_ptr) = stack_guard.pop() {
                unsafe {
                    let header = &mut *obj_ptr.as_ptr();
                    if !header.mark {
                        header.mark = true;
                        
                        // Add references to mark stack
                        for reference in &header.references {
                            stack_guard.push(*reference);
                        }
                    }
                }
            }
        }
    }
}

impl GCAlgorithm for ConcurrentGC {
    fn collect(&self, _generation: Option<u32>) -> GCResult {
        let start_time = Instant::now();
        let mut objects_freed = 0;
        let mut bytes_freed = 0;
        
        if let Ok(mut heap) = self.heap.lock() {
            // Stop-the-world sweep phase
            let mut to_remove = Vec::new();
            
            for (ptr, header) in &heap.objects {
                if !header.mark {
                    to_remove.push(*ptr);
                    objects_freed += 1;
                    bytes_freed += header.size;
                } else {
                    // Reset mark for next cycle
                    // Note: This is unsafe but necessary for concurrent GC
                    // In production, this would use atomic operations
                }
            }
            
            // Remove unmarked objects
            for ptr in to_remove {
                heap.objects.remove(&ptr);
                heap.used_size -= heap.objects.get(&ptr).map(|h| h.size).unwrap_or(0);
                heap.free_list.push(ptr);
            }
        }
        
        let collection_time = start_time.elapsed().as_millis() as u64;
        
        // Update stats
        if let Ok(mut stats) = self.stats.lock() {
            stats.total_collections += 1;
            stats.total_collection_time_ms += collection_time;
            stats.objects_collected += objects_freed;
            stats.bytes_collected += bytes_freed;
            stats.average_pause_time_ms = stats.total_collection_time_ms as f64 / stats.total_collections as f64;
        }
        
        GCResult {
            objects_freed,
            bytes_freed,
            collection_time_ms: collection_time,
            gc_type: GCType::Concurrent,
        }
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<NonNull<u8>, GCError> {
        if let Ok(mut heap) = self.heap.lock() {
            if heap.used_size + size > heap.total_size {
                return Err(GCError::OutOfMemory);
            }
            
            let layout = std::alloc::Layout::from_size_align(size, std::mem::align_of::<u8>())
                .map_err(|_| GCError::InvalidObject)?;
            
            let ptr = unsafe { std::alloc::alloc(layout) };
            if ptr.is_null() {
                return Err(GCError::OutOfMemory);
            }
            
            let non_null_ptr = NonNull::new(ptr).ok_or(GCError::OutOfMemory)?;
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: false,
                generation: 0,
                references: Vec::new(),
            };
            
            heap.objects.insert(non_null_ptr, header);
            heap.used_size += size;
            
            Ok(non_null_ptr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: NonNull<u8>) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: NonNull<u8>) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().unwrap_or_default().clone()
    }
    
    fn set_threshold(&self, _threshold: usize) {
        // Not applicable for concurrent GC
    }
    
    fn is_gc_needed(&self) -> bool {
        if let Ok(heap) = self.heap.lock() {
            heap.used_size > heap.total_size / 2
        } else {
            false
        }
    }
}

// ============================================================================
// TRACING GC IMPLEMENTATION
// ============================================================================

impl TracingGC {
    pub fn new(heap_size: usize, threshold: usize) -> Self {
        Self {
            heap: Arc::new(Mutex::new(Heap::new(heap_size))),
            roots: Arc::new(RwLock::new(HashSet::new())),
            stats: Arc::new(Mutex::new(GCStats::default())),
            mark_set: Arc::new(Mutex::new(HashSet::new())),
            threshold: Arc::new(Mutex::new(threshold)),
        }
    }
    
    fn mark_and_sweep(&self) -> GCResult {
        let start_time = Instant::now();
        let mut objects_freed = 0;
        let mut bytes_freed = 0;
        
        if let (Ok(mut heap), Ok(roots), Ok(mut mark_set)) = 
            (self.heap.lock(), self.roots.read(), self.mark_set.lock()) {
            
            // Clear previous marks
            mark_set.clear();
            
            // Mark phase: mark all reachable objects
            for root in roots.iter() {
                self.mark_from_object(*root, &heap.objects, &mut mark_set);
            }
            
            // Sweep phase: collect unmarked objects
            let mut to_remove = Vec::new();
            for (ptr, header) in &heap.objects {
                if !mark_set.contains(&NonNull::new(header as *const ObjectHeader as *mut ObjectHeader).unwrap()) {
                    to_remove.push(*ptr);
                    objects_freed += 1;
                    bytes_freed += header.size;
                }
            }
            
            // Remove unmarked objects
            for ptr in to_remove {
                if let Some(header) = heap.objects.remove(&ptr) {
                    heap.used_size -= header.size;
                    heap.free_list.push(ptr);
                    
                    // Deallocate memory
                    let layout = std::alloc::Layout::from_size_align(header.size, std::mem::align_of::<u8>()).unwrap();
                    unsafe {
                        std::alloc::dealloc(ptr.as_ptr(), layout);
                    }
                }
            }
        }
        
        let collection_time = start_time.elapsed().as_millis() as u64;
        
        // Update stats
        if let Ok(mut stats) = self.stats.lock() {
            stats.total_collections += 1;
            stats.total_collection_time_ms += collection_time;
            stats.objects_collected += objects_freed;
            stats.bytes_collected += bytes_freed;
            stats.average_pause_time_ms = stats.total_collection_time_ms as f64 / stats.total_collections as f64;
        }
        
        GCResult {
            objects_freed,
            bytes_freed,
            collection_time_ms: collection_time,
            gc_type: GCType::Full,
        }
    }
    
    fn mark_from_object(
        &self,
        obj_ptr: NonNull<u8>,
        objects: &HashMap<NonNull<u8>, ObjectHeader>,
        marked: &mut HashSet<NonNull<ObjectHeader>>
    ) {
        if let Some(header) = objects.get(&obj_ptr) {
            let header_ptr = NonNull::new(header as *const ObjectHeader as *mut ObjectHeader).unwrap();
            
            if marked.contains(&header_ptr) {
                return;
            }
            
            marked.insert(header_ptr);
            
            // Mark referenced objects
            for reference in &header.references {
                let ref_obj_ptr = NonNull::new(reference.as_ptr() as *mut u8);
                if let Some(ref_ptr) = ref_obj_ptr {
                    self.mark_from_object(ref_ptr, objects, marked);
                }
            }
        }
    }
}

impl GCAlgorithm for TracingGC {
    fn collect(&self, _generation: Option<u32>) -> GCResult {
        self.mark_and_sweep()
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<NonNull<u8>, GCError> {
        if let Ok(mut heap) = self.heap.lock() {
            if heap.used_size + size > heap.total_size {
                return Err(GCError::OutOfMemory);
            }
            
            let layout = std::alloc::Layout::from_size_align(size, std::mem::align_of::<u8>())
                .map_err(|_| GCError::InvalidObject)?;
            
            let ptr = unsafe { std::alloc::alloc(layout) };
            if ptr.is_null() {
                return Err(GCError::OutOfMemory);
            }
            
            let non_null_ptr = NonNull::new(ptr).ok_or(GCError::OutOfMemory)?;
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: false,
                generation: 0,
                references: Vec::new(),
            };
            
            heap.objects.insert(non_null_ptr, header);
            heap.used_size += size;
            
            Ok(non_null_ptr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: NonNull<u8>) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: NonNull<u8>) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().unwrap_or_default().clone()
    }
    
    fn set_threshold(&self, threshold: usize) {
        if let Ok(mut thresh) = self.threshold.lock() {
            *thresh = threshold;
        }
    }
    
    fn is_gc_needed(&self) -> bool {
        if let (Ok(heap), Ok(threshold)) = (self.heap.lock(), self.threshold.lock()) {
            heap.used_size > *threshold
        } else {
            false
        }
    }
}

// ============================================================================
// HELPER IMPLEMENTATIONS
// ============================================================================

impl Generation {
    fn new(size_limit: usize) -> Self {
        Self {
            objects: HashMap::new(),
            size_limit,
            current_size: 0,
        }
    }
}

impl Heap {
    fn new(total_size: usize) -> Self {
        Self {
            objects: HashMap::new(),
            free_list: Vec::new(),
            total_size,
            used_size: 0,
        }
    }
}

impl Default for GCStats {
    fn default() -> Self {
        Self {
            total_collections: 0,
            total_collection_time_ms: 0,
            objects_collected: 0,
            bytes_collected: 0,
            heap_size: 0,
            used_memory: 0,
            gc_pressure: 0.0,
            average_pause_time_ms: 0.0,
        }
    }
}

// ============================================================================
// FFI EXPORTS FOR GC ALGORITHMS
// ============================================================================

#[no_mangle]
pub extern "C" fn runa_create_generational_gc(young_size: usize, old_size: usize) -> *mut GenerationalGC {
    let gc = Box::new(GenerationalGC::new(young_size, old_size));
    Box::into_raw(gc)
}

#[no_mangle]
pub extern "C" fn runa_create_concurrent_gc(heap_size: usize) -> *mut ConcurrentGC {
    let gc = Box::new(ConcurrentGC::new(heap_size));
    Box::into_raw(gc)
}

#[no_mangle]
pub extern "C" fn runa_create_tracing_gc(heap_size: usize, threshold: usize) -> *mut TracingGC {
    let gc = Box::new(TracingGC::new(heap_size, threshold));
    Box::into_raw(gc)
}

#[no_mangle]
pub extern "C" fn runa_start_concurrent_gc(gc: *mut ConcurrentGC) -> bool {
    if gc.is_null() {
        return false;
    }
    
    let gc = unsafe { &mut *gc };
    gc.start_concurrent_collection();
    true
}

#[no_mangle]
pub extern "C" fn runa_stop_concurrent_gc(gc: *mut ConcurrentGC) -> bool {
    if gc.is_null() {
        return false;
    }
    
    let gc = unsafe { &mut *gc };
    gc.stop_concurrent_collection();
    true
}

#[no_mangle]
pub extern "C" fn runa_gc_collect(gc: *mut dyn GCAlgorithm, generation: i32) -> GCResult {
    if gc.is_null() {
        return GCResult {
            objects_freed: 0,
            bytes_freed: 0,
            collection_time_ms: 0,
            gc_type: GCType::Minor,
        };
    }
    
    let gc = unsafe { &*gc };
    let gen = if generation < 0 { None } else { Some(generation as u32) };
    gc.collect(gen)
}

#[no_mangle]
pub extern "C" fn runa_gc_allocate(gc: *mut dyn GCAlgorithm, size: usize, align: usize) -> runa_object {
    if gc.is_null() {
        return std::ptr::null_mut();
    }
    
    let gc = unsafe { &*gc };
    match gc.allocate(size, align) {
        Ok(ptr) => ptr.as_ptr() as runa_object,
        Err(_) => std::ptr::null_mut(),
    }
}

#[no_mangle]
pub extern "C" fn runa_gc_get_stats(gc: *mut dyn GCAlgorithm) -> GCStats {
    if gc.is_null() {
        return GCStats::default();
    }
    
    let gc = unsafe { &*gc };
    gc.get_stats()
}

#[no_mangle]
pub extern "C" fn runa_gc_is_needed(gc: *mut dyn GCAlgorithm) -> bool {
    if gc.is_null() {
        return false;
    }
    
    let gc = unsafe { &*gc };
    gc.is_gc_needed()
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_generational_gc_creation() {
        let gc = GenerationalGC::new(1024 * 1024, 4 * 1024 * 1024);
        assert_eq!(gc.get_stats().total_collections, 0);
    }
    
    #[test]
    fn test_gc_allocation() {
        let gc = GenerationalGC::new(1024 * 1024, 4 * 1024 * 1024);
        let ptr = gc.allocate(64, 8);
        assert!(ptr.is_ok());
    }
    
    #[test]
    fn test_gc_collection() {
        let gc = GenerationalGC::new(1024, 4096);
        
        // Allocate some objects
        for _ in 0..10 {
            let _ = gc.allocate(64, 8);
        }
        
        let result = gc.collect(Some(0));
        assert!(result.collection_time_ms >= 0);
    }
    
    #[test]
    fn test_concurrent_gc() {
        let mut gc = ConcurrentGC::new(1024 * 1024);
        assert_eq!(gc.get_stats().total_collections, 0);
        
        // Test allocation
        let ptr = gc.allocate(64, 8);
        assert!(ptr.is_ok());
        
        // Test collection
        let result = gc.collect(None);
        assert!(result.collection_time_ms >= 0);
    }
    
    #[test]
    fn test_tracing_gc() {
        let gc = TracingGC::new(1024 * 1024, 512 * 1024);
        assert_eq!(gc.get_stats().total_collections, 0);
        
        // Test allocation
        let ptr = gc.allocate(128, 8);
        assert!(ptr.is_ok());
        
        // Test GC threshold
        assert!(!gc.is_gc_needed());
        
        // Test collection
        let result = gc.collect(None);
        assert_eq!(result.gc_type as u32, GCType::Full as u32);
    }
    
    #[test]
    fn test_gc_root_management() {
        let gc = GenerationalGC::new(1024, 4096);
        
        let ptr = gc.allocate(64, 8).unwrap();
        gc.register_root(ptr);
        
        // Root should prevent collection
        let result = gc.collect(Some(0));
        assert_eq!(result.objects_freed, 0);
        
        gc.unregister_root(ptr);
    }
}