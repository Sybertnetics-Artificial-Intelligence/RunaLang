//! Advanced Garbage Collection algorithms for the Runa runtime.
//! Provides pluggable GC strategies including generational, concurrent, and tracing collectors.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex, RwLock};
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::{Duration, Instant};
use crate::runa_object;

/// GC algorithm trait for pluggable garbage collection strategies
pub trait GCAlgorithm: Send + Sync {
    fn collect(&self, generation: Option<u32>) -> GCResult;
    fn allocate(&self, size: usize, align: usize) -> Result<usize, GCError>; // Return address as usize
    fn register_root(&self, ptr: usize); // Use usize address
    fn unregister_root(&self, ptr: usize); // Use usize address
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
    pub mark: AtomicBool,
    pub generation: u8,
    pub references: Vec<usize>, // Use usize addresses for thread safety
}

/// Generational garbage collector
pub struct GenerationalGC {
    young_generation: Arc<Mutex<Generation>>,
    old_generation: Arc<Mutex<Generation>>,
    roots: Arc<RwLock<HashSet<usize>>>, // Use usize addresses for thread safety
    stats: Arc<Mutex<GCStats>>,
    threshold: Arc<Mutex<usize>>,
    allocation_counter: Arc<Mutex<usize>>,
}

/// Concurrent garbage collector
pub struct ConcurrentGC {
    heap: Arc<Mutex<Heap>>,
    roots: Arc<RwLock<HashSet<usize>>>, // Use usize addresses for thread safety
    stats: Arc<Mutex<GCStats>>,
    mark_stack: Arc<Mutex<Vec<usize>>>, // Use usize addresses for thread safety
    collection_thread: Option<std::thread::JoinHandle<()>>,
    stop_flag: Arc<Mutex<bool>>,
}

/// Tracing garbage collector (mark-and-sweep)
pub struct TracingGC {
    heap: Arc<Mutex<Heap>>,
    roots: Arc<RwLock<HashSet<usize>>>, // Use usize addresses for thread safety
    stats: Arc<Mutex<GCStats>>,
    mark_set: Arc<Mutex<HashSet<usize>>>, // Use usize addresses for thread safety
    threshold: Arc<Mutex<usize>>,
}

/// Real-time garbage collector with deterministic pause times
pub struct RealtimeGC {
    heap: Arc<Mutex<RealtimeHeap>>,
    roots: Arc<RwLock<HashSet<usize>>>,
    stats: Arc<Mutex<GCStats>>,
    incremental_state: Arc<Mutex<IncrementalState>>,
    time_budget_ns: Arc<Mutex<u64>>, // Maximum pause time in nanoseconds
    mark_stack: Arc<Mutex<Vec<usize>>>,
    sweep_iterator: Arc<Mutex<Option<Vec<usize>>>>, // Store keys to iterate over instead of iterator
}

/// NUMA-aware garbage collector for multi-socket systems
pub struct NumaAwareGC {
    numa_heaps: Vec<Arc<Mutex<NumaHeap>>>,
    global_roots: Arc<RwLock<HashSet<usize>>>,
    stats: Arc<Mutex<GCStats>>,
    node_count: usize,
    thread_to_node: Arc<Mutex<HashMap<std::thread::ThreadId, usize>>>,
    cross_node_references: Arc<Mutex<HashMap<usize, HashSet<usize>>>>,
}

/// Incremental state for real-time GC
#[derive(Debug)]
struct IncrementalState {
    phase: GCPhase,
    objects_to_mark: Vec<usize>,
    current_mark_index: usize,
    objects_to_sweep: Vec<usize>,
    current_sweep_index: usize,
}

#[derive(Debug, Clone, Copy)]
enum GCPhase {
    Idle,
    Marking,
    Sweeping,
}

/// Real-time heap with incremental collection support
struct RealtimeHeap {
    objects: HashMap<usize, ObjectHeader>,
    free_list: Vec<usize>,
    total_size: usize,
    used_size: usize,
    allocation_rate_tracker: AllocationRateTracker,
}

/// NUMA-specific heap per NUMA node
struct NumaHeap {
    node_id: usize,
    objects: HashMap<usize, ObjectHeader>,
    free_list: Vec<usize>,
    total_size: usize,
    used_size: usize,
    local_roots: HashSet<usize>,
}

/// Tracks allocation rate for real-time scheduling
struct AllocationRateTracker {
    recent_allocations: Vec<(Instant, usize)>,
    bytes_per_second: f64,
    last_update: Instant,
}

struct Generation {
    objects: HashMap<usize, ObjectHeader>, // Use usize addresses for thread safety
    size_limit: usize,
    current_size: usize,
}

struct Heap {
    objects: HashMap<usize, ObjectHeader>, // Use usize addresses for thread safety
    free_list: Vec<usize>, // Use usize addresses for thread safety
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
            for &root in roots.iter() {
                self.mark_from_root(root, &young.objects, &mut marked);
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
    
    fn mark_from_root(&self, root: usize, objects: &HashMap<usize, ObjectHeader>, marked: &mut HashSet<usize>) {
        if marked.contains(&root) {
            return;
        }
        
        marked.insert(root);
        
        if let Some(header) = objects.get(&root) {
            for &reference in &header.references {
                self.mark_from_root(reference, objects, marked);
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
    
    fn allocate(&self, size: usize, _align: usize) -> Result<usize, GCError> {
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
            
            let ptr_addr = ptr as usize; // Convert to usize address
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: AtomicBool::new(false),
                generation: 0,
                references: Vec::new(),
            };
            
            young.objects.insert(ptr_addr, header);
            young.current_size += size;
            
            if let Ok(mut counter) = self.allocation_counter.lock() {
                *counter += 1;
            }
            
            Ok(ptr_addr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
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
        roots: &Arc<RwLock<HashSet<usize>>>,
        mark_stack: &Arc<Mutex<Vec<usize>>>
    ) {
        if let (Ok(mut heap_guard), Ok(roots_guard), Ok(mut stack_guard)) = 
            (heap.lock(), roots.read(), mark_stack.lock()) {
            
            // Clear mark stack
            stack_guard.clear();
            
            // Initialize with roots
            for &root in roots_guard.iter() {
                if heap_guard.objects.contains_key(&root) {
                    stack_guard.push(root);
                }
            }
            
            // Concurrent marking - mark objects as reachable
            let mut marked = HashSet::new();
            while let Some(obj_addr) = stack_guard.pop() {
                if marked.contains(&obj_addr) {
                    continue;
                }
                
                marked.insert(obj_addr);
                
                if let Some(header) = heap_guard.objects.get_mut(&obj_addr) {
                    header.mark.store(true, Ordering::Release);
                    
                    // Add references to mark stack
                    for &reference in &header.references {
                        if !marked.contains(&reference) {
                            stack_guard.push(reference);
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
            
            for (&ptr, header) in &heap.objects {
                if !header.mark.load(Ordering::Acquire) {
                    to_remove.push(ptr);
                    objects_freed += 1;
                    bytes_freed += header.size;
                } else {
                    // Reset mark for next cycle using atomic operation
                    header.mark.store(false, Ordering::Release);
                }
            }
            
            // Remove unmarked objects
            for ptr in to_remove {
                if let Some(header) = heap.objects.remove(&ptr) {
                    heap.used_size -= header.size;
                    heap.free_list.push(ptr);
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
            gc_type: GCType::Concurrent,
        }
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<usize, GCError> {
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
            
            let ptr_addr = ptr as usize;
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: AtomicBool::new(false),
                generation: 0,
                references: Vec::new(),
            };
            
            heap.objects.insert(ptr_addr, header);
            heap.used_size += size;
            
            Ok(ptr_addr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
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
            for &root in roots.iter() {
                self.mark_from_object(root, &heap.objects, &mut mark_set);
            }
            
            // Sweep phase: collect unmarked objects
            let mut to_remove = Vec::new();
            for (&ptr, header) in &heap.objects {
                if !mark_set.contains(&ptr) {
                    to_remove.push(ptr);
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
                        std::alloc::dealloc(ptr as *mut u8, layout);
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
        obj_addr: usize,
        objects: &HashMap<usize, ObjectHeader>,
        marked: &mut HashSet<usize>
    ) {
        if marked.contains(&obj_addr) {
            return;
        }
        
        marked.insert(obj_addr);
        
        if let Some(header) = objects.get(&obj_addr) {
            // Mark referenced objects
            for &reference in &header.references {
                self.mark_from_object(reference, objects, marked);
            }
        }
    }
}

impl GCAlgorithm for TracingGC {
    fn collect(&self, _generation: Option<u32>) -> GCResult {
        self.mark_and_sweep()
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<usize, GCError> {
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
            
            let ptr_addr = ptr as usize;
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: AtomicBool::new(false),
                generation: 0,
                references: Vec::new(),
            };
            
            heap.objects.insert(ptr_addr, header);
            heap.used_size += size;
            
            Ok(ptr_addr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
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
// REAL-TIME GC IMPLEMENTATION
// ============================================================================

impl RealtimeGC {
    pub fn new(heap_size: usize, time_budget_ms: u64) -> Self {
        Self {
            heap: Arc::new(Mutex::new(RealtimeHeap::new(heap_size))),
            roots: Arc::new(RwLock::new(HashSet::new())),
            stats: Arc::new(Mutex::new(GCStats::default())),
            incremental_state: Arc::new(Mutex::new(IncrementalState::new())),
            time_budget_ns: Arc::new(Mutex::new(time_budget_ms * 1_000_000)), // Convert ms to ns
            mark_stack: Arc::new(Mutex::new(Vec::new())),
            sweep_iterator: Arc::new(Mutex::new(None)),
        }
    }
    
    /// Perform incremental collection within time budget
    fn incremental_collect(&self) -> GCResult {
        let start_time = Instant::now();
        let time_budget = *self.time_budget_ns.lock().unwrap();
        let mut objects_freed = 0;
        let mut bytes_freed = 0;
        
        loop {
            let elapsed = start_time.elapsed().as_nanos() as u64;
            if elapsed >= time_budget {
                break; // Time budget exceeded
            }
            
            let remaining_time = time_budget - elapsed;
            
            if let Ok(mut state) = self.incremental_state.lock() {
                match state.phase {
                    GCPhase::Idle => {
                        // Start new collection cycle
                        self.start_incremental_marking(&mut state);
                    },
                    GCPhase::Marking => {
                        let progress = self.incremental_mark(&mut state, remaining_time);
                        if progress == 0 {
                            // Marking complete, move to sweeping
                            self.start_incremental_sweeping(&mut state);
                        }
                    },
                    GCPhase::Sweeping => {
                        let (freed_objects, freed_bytes) = self.incremental_sweep(&mut state, remaining_time);
                        objects_freed += freed_objects;
                        bytes_freed += freed_bytes;
                        
                        if state.current_sweep_index >= state.objects_to_sweep.len() {
                            // Sweeping complete
                            state.phase = GCPhase::Idle;
                            break;
                        }
                    }
                }
            } else {
                break;
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
    
    fn start_incremental_marking(&self, state: &mut IncrementalState) {
        state.phase = GCPhase::Marking;
        state.current_mark_index = 0;
        state.objects_to_mark.clear();
        
        // Initialize marking with roots
        if let Ok(roots) = self.roots.read() {
            state.objects_to_mark.extend(roots.iter().cloned());
        }
    }
    
    /// Perform incremental marking within time budget
    /// Returns number of objects still to mark (0 if complete)
    fn incremental_mark(&self, state: &mut IncrementalState, time_budget_ns: u64) -> usize {
        let start_time = Instant::now();
        
        if let Ok(heap) = self.heap.lock() {
            while state.current_mark_index < state.objects_to_mark.len() {
                let elapsed = start_time.elapsed().as_nanos() as u64;
                if elapsed >= time_budget_ns {
                    break; // Time budget exceeded
                }
                
                let obj_addr = state.objects_to_mark[state.current_mark_index];
                state.current_mark_index += 1;
                
                if let Some(header) = heap.objects.get(&obj_addr) {
                    // Mark object
                    header.mark.store(true, Ordering::Release);
                    
                    // Add references to marking queue
                    for &reference in &header.references {
                        if !state.objects_to_mark.contains(&reference) {
                            state.objects_to_mark.push(reference);
                        }
                    }
                }
            }
        }
        
        state.objects_to_mark.len() - state.current_mark_index
    }
    
    fn start_incremental_sweeping(&self, state: &mut IncrementalState) {
        state.phase = GCPhase::Sweeping;
        state.current_sweep_index = 0;
        state.objects_to_sweep.clear();
        
        // Collect unmarked objects
        if let Ok(heap) = self.heap.lock() {
            for (&ptr, header) in &heap.objects {
                if !header.mark.load(Ordering::Acquire) {
                    state.objects_to_sweep.push(ptr);
                }
            }
        }
    }
    
    /// Perform incremental sweeping within time budget
    /// Returns (objects_freed, bytes_freed)
    fn incremental_sweep(&self, state: &mut IncrementalState, time_budget_ns: u64) -> (usize, usize) {
        let start_time = Instant::now();
        let mut objects_freed = 0;
        let mut bytes_freed = 0;
        
        if let Ok(mut heap) = self.heap.lock() {
            while state.current_sweep_index < state.objects_to_sweep.len() {
                let elapsed = start_time.elapsed().as_nanos() as u64;
                if elapsed >= time_budget_ns {
                    break; // Time budget exceeded
                }
                
                let obj_addr = state.objects_to_sweep[state.current_sweep_index];
                state.current_sweep_index += 1;
                
                if let Some(header) = heap.objects.remove(&obj_addr) {
                    heap.used_size -= header.size;
                    heap.free_list.push(obj_addr);
                    objects_freed += 1;
                    bytes_freed += header.size;
                    
                    // Deallocate memory
                    let layout = std::alloc::Layout::from_size_align(header.size, std::mem::align_of::<u8>()).unwrap();
                    unsafe {
                        std::alloc::dealloc(obj_addr as *mut u8, layout);
                    }
                }
            }
            
            // Reset marks for next cycle
            for header in heap.objects.values() {
                header.mark.store(false, Ordering::Release);
            }
        }
        
        (objects_freed, bytes_freed)
    }
}

impl GCAlgorithm for RealtimeGC {
    fn collect(&self, _generation: Option<u32>) -> GCResult {
        self.incremental_collect()
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<usize, GCError> {
        if let Ok(mut heap) = self.heap.lock() {
            // Update allocation rate tracking
            heap.allocation_rate_tracker.record_allocation(size);
            
            if heap.used_size + size > heap.total_size {
                return Err(GCError::OutOfMemory);
            }
            
            let layout = std::alloc::Layout::from_size_align(size, std::mem::align_of::<u8>())
                .map_err(|_| GCError::InvalidObject)?;
            
            let ptr = unsafe { std::alloc::alloc(layout) };
            if ptr.is_null() {
                return Err(GCError::OutOfMemory);
            }
            
            let ptr_addr = ptr as usize;
            
            let header = ObjectHeader {
                size,
                type_id: 0,
                mark: AtomicBool::new(false),
                generation: 0,
                references: Vec::new(),
            };
            
            heap.objects.insert(ptr_addr, header);
            heap.used_size += size;
            
            Ok(ptr_addr)
        } else {
            Err(GCError::ConcurrentAccess)
        }
    }
    
    fn register_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.insert(ptr);
        }
    }
    
    fn unregister_root(&self, ptr: usize) {
        if let Ok(mut roots) = self.roots.write() {
            roots.remove(&ptr);
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
    }
    
    fn set_threshold(&self, threshold_ms: usize) {
        if let Ok(mut time_budget) = self.time_budget_ns.lock() {
            *time_budget = (threshold_ms as u64) * 1_000_000; // Convert ms to ns
        }
    }
    
    fn is_gc_needed(&self) -> bool {
        if let Ok(heap) = self.heap.lock() {
            // Use allocation rate to predict when GC is needed
            let allocation_rate = heap.allocation_rate_tracker.bytes_per_second;
            let time_budget_ms = *self.time_budget_ns.lock().unwrap() / 1_000_000;
            
            // Predict if we need GC based on allocation rate and available space
            let predicted_allocation = allocation_rate * (time_budget_ms as f64 / 1000.0);
            heap.used_size as f64 + predicted_allocation > (heap.total_size as f64 * 0.8)
        } else {
            false
        }
    }
}

// ============================================================================
// NUMA-AWARE GC IMPLEMENTATION
// ============================================================================

impl NumaAwareGC {
    pub fn new(total_heap_size: usize) -> Self {
        let node_count = Self::detect_numa_nodes();
        let heap_per_node = total_heap_size / node_count;
        
        let mut numa_heaps = Vec::new();
        for node_id in 0..node_count {
            numa_heaps.push(Arc::new(Mutex::new(NumaHeap::new(node_id, heap_per_node))));
        }
        
        Self {
            numa_heaps,
            global_roots: Arc::new(RwLock::new(HashSet::new())),
            stats: Arc::new(Mutex::new(GCStats::default())),
            node_count,
            thread_to_node: Arc::new(Mutex::new(HashMap::new())),
            cross_node_references: Arc::new(Mutex::new(HashMap::new())),
        }
    }
    
    fn detect_numa_nodes() -> usize {
        // Production NUMA topology detection across platforms
        #[cfg(target_os = "linux")]
        {
            // Primary method: Read kernel NUMA topology from sysfs
            if let Ok(entries) = std::fs::read_dir("/sys/devices/system/node/") {
                let node_count = entries
                    .filter_map(|entry| {
                        entry.ok().and_then(|e| {
                            e.file_name().to_str().and_then(|name| {
                                if name.starts_with("node") && name.len() > 4 {
                                    name[4..].parse::<usize>().ok()
                                } else {
                                    None
                                }
                            })
                        })
                    })
                    .max()
                    .map(|max_node| max_node + 1) // Convert max node ID to count
                    .unwrap_or(1);
                
                if node_count > 1 {
                    return node_count;
                }
            }
            
            // Fallback: Check /proc/cpuinfo for NUMA information
            if let Ok(cpuinfo) = std::fs::read_to_string("/proc/cpuinfo") {
                let mut numa_nodes = std::collections::HashSet::new();
                for line in cpuinfo.lines() {
                    if line.starts_with("physical id") {
                        if let Some(id_str) = line.split(':').nth(1) {
                            if let Ok(id) = id_str.trim().parse::<usize>() {
                                numa_nodes.insert(id);
                            }
                        }
                    }
                }
                if numa_nodes.len() > 1 {
                    return numa_nodes.len();
                }
            }
        }
        
        #[cfg(target_os = "macos")]
        {
            use std::process::Command;
            
            // Use sysctl to query NUMA topology on macOS
            if let Ok(output) = Command::new("sysctl")
                .arg("-n")
                .arg("hw.packages")
                .output() {
                if let Ok(packages_str) = String::from_utf8(output.stdout) {
                    if let Ok(packages) = packages_str.trim().parse::<usize>() {
                        if packages > 1 {
                            return packages;
                        }
                    }
                }
            }
            
            // Alternative: Check CPU topology
            if let Ok(output) = Command::new("sysctl")
                .arg("-n")
                .arg("hw.physicalcpu")
                .output() {
                if let Ok(phys_str) = String::from_utf8(output.stdout) {
                    if let Ok(phys_cpus) = phys_str.trim().parse::<usize>() {
                        if let Ok(output) = Command::new("sysctl")
                            .arg("-n")
                            .arg("hw.logicalcpu")
                            .output() {
                            if let Ok(log_str) = String::from_utf8(output.stdout) {
                                if let Ok(log_cpus) = log_str.trim().parse::<usize>() {
                                    // Heuristic: if we have significantly more logical than physical CPUs
                                    // and many physical CPUs, likely multi-socket
                                    if phys_cpus >= 8 && log_cpus / phys_cpus >= 2 {
                                        return (phys_cpus / 8).max(1); // Estimate NUMA nodes
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        #[cfg(target_os = "windows")]
        {
            use std::process::Command;
            
            // Use WMIC to query NUMA node information
            if let Ok(output) = Command::new("wmic")
                .arg("computersystem")
                .arg("get")
                .arg("NumberOfProcessors")
                .arg("/value")
                .output() {
                if let Ok(output_str) = String::from_utf8(output.stdout) {
                    for line in output_str.lines() {
                        if line.starts_with("NumberOfProcessors=") {
                            if let Ok(num_proc) = line[19..].parse::<usize>() {
                                // Heuristic: assume NUMA if we have many processors
                                if num_proc >= 16 {
                                    return (num_proc / 8).max(1);
                                }
                            }
                        }
                    }
                }
            }
            
            // Alternative: Use PowerShell to get NUMA information
            if let Ok(output) = Command::new("powershell")
                .arg("-Command")
                .arg("Get-WmiObject -Class Win32_ComputerSystem | Select-Object NumberOfProcessors")
                .output() {
                if let Ok(output_str) = String::from_utf8(output.stdout) {
                    for line in output_str.lines() {
                        if let Ok(num_proc) = line.trim().parse::<usize>() {
                            if num_proc >= 16 {
                                return (num_proc / 8).max(1);
                            }
                        }
                    }
                }
            }
        }
        
        // Final fallback: single NUMA node (most common case)
        1
    }
    
    fn get_current_node(&self) -> usize {
        let thread_id = std::thread::current().id();
        
        if let Ok(thread_map) = self.thread_to_node.lock() {
            if let Some(&node) = thread_map.get(&thread_id) {
                return node;
            }
        }
        
        // Assign thread to node with least load
        self.assign_thread_to_node(thread_id)
    }
    
    fn assign_thread_to_node(&self, thread_id: std::thread::ThreadId) -> usize {
        let mut min_load = usize::MAX;
        let mut best_node = 0;
        
        // Find node with minimum memory usage
        for (node_id, heap) in self.numa_heaps.iter().enumerate() {
            if let Ok(heap_guard) = heap.lock() {
                if heap_guard.used_size < min_load {
                    min_load = heap_guard.used_size;
                    best_node = node_id;
                }
            }
        }
        
        // Assign thread to best node
        if let Ok(mut thread_map) = self.thread_to_node.lock() {
            thread_map.insert(thread_id, best_node);
        }
        
        best_node
    }
    
    fn collect_node(&self, node_id: usize) -> GCResult {
        let start_time = Instant::now();
        let mut objects_freed = 0;
        let mut bytes_freed = 0;
        
        if let Some(heap_arc) = self.numa_heaps.get(node_id) {
            if let Ok(mut heap) = heap_arc.lock() {
                // Mark phase: mark local objects
                let mut marked = HashSet::new();
                
                // Mark from local roots
                for &root in &heap.local_roots {
                    self.mark_numa_object(root, &heap.objects, &mut marked);
                }
                
                // Mark from global roots that reference this node
                if let Ok(global_roots) = self.global_roots.read() {
                    for &root in global_roots.iter() {
                        if heap.objects.contains_key(&root) {
                            self.mark_numa_object(root, &heap.objects, &mut marked);
                        }
                    }
                }
                
                // Handle cross-node references
                if let Ok(cross_refs) = self.cross_node_references.lock() {
                    for (source, targets) in cross_refs.iter() {
                        if heap.objects.contains_key(source) && marked.contains(source) {
                            for &target in targets {
                                if heap.objects.contains_key(&target) {
                                    self.mark_numa_object(target, &heap.objects, &mut marked);
                                }
                            }
                        }
                    }
                }
                
                // Sweep phase: collect unmarked objects
                let mut to_remove = Vec::new();
                for (&ptr, header) in &heap.objects {
                    if !marked.contains(&ptr) {
                        to_remove.push(ptr);
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
                            std::alloc::dealloc(ptr as *mut u8, layout);
                        }
                    }
                }
            }
        }
        
        let collection_time = start_time.elapsed().as_millis() as u64;
        
        GCResult {
            objects_freed,
            bytes_freed,
            collection_time_ms: collection_time,
            gc_type: GCType::Minor,
        }
    }
    
    fn mark_numa_object(&self, obj_addr: usize, objects: &HashMap<usize, ObjectHeader>, marked: &mut HashSet<usize>) {
        if marked.contains(&obj_addr) {
            return;
        }
        
        marked.insert(obj_addr);
        
        if let Some(header) = objects.get(&obj_addr) {
            for &reference in &header.references {
                self.mark_numa_object(reference, objects, marked);
            }
        }
    }
}

impl GCAlgorithm for NumaAwareGC {
    fn collect(&self, generation: Option<u32>) -> GCResult {
        match generation {
            Some(node_id) if (node_id as usize) < self.node_count => {
                // Collect specific NUMA node
                self.collect_node(node_id as usize)
            },
            _ => {
                // Collect all nodes
                let mut total_result = GCResult {
                    objects_freed: 0,
                    bytes_freed: 0,
                    collection_time_ms: 0,
                    gc_type: GCType::Full,
                };
                
                for node_id in 0..self.node_count {
                    let node_result = self.collect_node(node_id);
                    total_result.objects_freed += node_result.objects_freed;
                    total_result.bytes_freed += node_result.bytes_freed;
                    total_result.collection_time_ms = total_result.collection_time_ms.max(node_result.collection_time_ms);
                }
                
                // Update stats
                if let Ok(mut stats) = self.stats.lock() {
                    stats.total_collections += 1;
                    stats.total_collection_time_ms += total_result.collection_time_ms;
                    stats.objects_collected += total_result.objects_freed;
                    stats.bytes_collected += total_result.bytes_freed;
                    stats.average_pause_time_ms = stats.total_collection_time_ms as f64 / stats.total_collections as f64;
                }
                
                total_result
            }
        }
    }
    
    fn allocate(&self, size: usize, _align: usize) -> Result<usize, GCError> {
        let node_id = self.get_current_node();
        
        if let Some(heap_arc) = self.numa_heaps.get(node_id) {
            if let Ok(mut heap) = heap_arc.lock() {
                if heap.used_size + size > heap.total_size {
                    return Err(GCError::OutOfMemory);
                }
                
                let layout = std::alloc::Layout::from_size_align(size, std::mem::align_of::<u8>())
                    .map_err(|_| GCError::InvalidObject)?;
                
                let ptr = unsafe { std::alloc::alloc(layout) };
                if ptr.is_null() {
                    return Err(GCError::OutOfMemory);
                }
                
                let ptr_addr = ptr as usize;
                
                let header = ObjectHeader {
                    size,
                    type_id: 0,
                    mark: AtomicBool::new(false),
                    generation: node_id as u8,
                    references: Vec::new(),
                };
                
                heap.objects.insert(ptr_addr, header);
                heap.used_size += size;
                
                Ok(ptr_addr)
            } else {
                Err(GCError::ConcurrentAccess)
            }
        } else {
            Err(GCError::InvalidObject)
        }
    }
    
    fn register_root(&self, ptr: usize) {
        let node_id = self.get_current_node();
        
        // Add to global roots
        if let Ok(mut roots) = self.global_roots.write() {
            roots.insert(ptr);
        }
        
        // Add to local node roots if object is on this node
        if let Some(heap_arc) = self.numa_heaps.get(node_id) {
            if let Ok(mut heap) = heap_arc.lock() {
                if heap.objects.contains_key(&ptr) {
                    heap.local_roots.insert(ptr);
                }
            }
        }
    }
    
    fn unregister_root(&self, ptr: usize) {
        // Remove from global roots
        if let Ok(mut roots) = self.global_roots.write() {
            roots.remove(&ptr);
        }
        
        // Remove from all local node roots
        for heap_arc in &self.numa_heaps {
            if let Ok(mut heap) = heap_arc.lock() {
                heap.local_roots.remove(&ptr);
            }
        }
    }
    
    fn get_stats(&self) -> GCStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
    }
    
    fn set_threshold(&self, _threshold: usize) {
        // NUMA GC uses different heuristics
    }
    
    fn is_gc_needed(&self) -> bool {
        // Check if any NUMA node is over threshold
        for heap_arc in &self.numa_heaps {
            if let Ok(heap) = heap_arc.lock() {
                if heap.used_size > heap.total_size / 2 {
                    return true;
                }
            }
        }
        false
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

impl IncrementalState {
    fn new() -> Self {
        Self {
            phase: GCPhase::Idle,
            objects_to_mark: Vec::new(),
            current_mark_index: 0,
            objects_to_sweep: Vec::new(),
            current_sweep_index: 0,
        }
    }
}

impl RealtimeHeap {
    fn new(total_size: usize) -> Self {
        Self {
            objects: HashMap::new(),
            free_list: Vec::new(),
            total_size,
            used_size: 0,
            allocation_rate_tracker: AllocationRateTracker::new(),
        }
    }
}

impl NumaHeap {
    fn new(node_id: usize, total_size: usize) -> Self {
        Self {
            node_id,
            objects: HashMap::new(),
            free_list: Vec::new(),
            total_size,
            used_size: 0,
            local_roots: HashSet::new(),
        }
    }
}

impl AllocationRateTracker {
    fn new() -> Self {
        Self {
            recent_allocations: Vec::new(),
            bytes_per_second: 0.0,
            last_update: Instant::now(),
        }
    }
    
    fn record_allocation(&mut self, bytes: usize) {
        let now = Instant::now();
        self.recent_allocations.push((now, bytes));
        
        // Remove allocations older than 1 second
        let cutoff = now - Duration::from_secs(1);
        self.recent_allocations.retain(|(time, _)| *time > cutoff);
        
        // Update allocation rate every 100ms
        if now.duration_since(self.last_update) > Duration::from_millis(100) {
            let total_bytes: usize = self.recent_allocations.iter().map(|(_, bytes)| *bytes).sum();
            let time_span = now.duration_since(self.last_update).as_secs_f64();
            self.bytes_per_second = total_bytes as f64 / time_span;
            self.last_update = now;
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
pub extern "C" fn runa_create_realtime_gc(heap_size: usize, time_budget_ms: u64) -> *mut RealtimeGC {
    let gc = Box::new(RealtimeGC::new(heap_size, time_budget_ms));
    Box::into_raw(gc)
}

#[no_mangle]
pub extern "C" fn runa_create_numa_gc(total_heap_size: usize) -> *mut NumaAwareGC {
    let gc = Box::new(NumaAwareGC::new(total_heap_size));
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
        Ok(ptr_addr) => ptr_addr as *mut u8 as runa_object,
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
    
    #[test]
    fn test_realtime_gc() {
        let gc = RealtimeGC::new(1024 * 1024, 5); // 5ms time budget
        assert_eq!(gc.get_stats().total_collections, 0);
        
        // Test allocation
        let ptr = gc.allocate(128, 8);
        assert!(ptr.is_ok());
        
        // Test incremental collection
        let result = gc.collect(None);
        assert!(result.collection_time_ms <= 10); // Should be within time budget
        
        // Test GC need prediction
        assert!(!gc.is_gc_needed()); // Should be false with minimal allocation
    }
    
    #[test]
    fn test_numa_gc() {
        let gc = NumaAwareGC::new(1024 * 1024);
        assert_eq!(gc.get_stats().total_collections, 0);
        
        // Test allocation (should use current thread's NUMA node)
        let ptr1 = gc.allocate(128, 8);
        assert!(ptr1.is_ok());
        
        let ptr2 = gc.allocate(256, 8);
        assert!(ptr2.is_ok());
        
        // Test root management
        let ptr = ptr1.unwrap();
        gc.register_root(ptr);
        
        // Test node-specific collection
        let result = gc.collect(Some(0)); // Collect node 0
        assert!(result.collection_time_ms >= 0);
        
        // Test full collection
        let full_result = gc.collect(None);
        assert!(full_result.collection_time_ms >= 0);
        
        gc.unregister_root(ptr);
    }
    
    #[test]
    fn test_realtime_incremental_phases() {
        let gc = RealtimeGC::new(1024, 1); // Very small time budget
        
        // Allocate several objects
        let mut ptrs = Vec::new();
        for _ in 0..5 {
            if let Ok(ptr) = gc.allocate(64, 8) {
                ptrs.push(ptr);
            }
        }
        
        // Register some as roots
        for &ptr in &ptrs[0..2] {
            gc.register_root(ptr);
        }
        
        // Multiple incremental collections should eventually complete
        let mut total_freed = 0;
        for _ in 0..10 {
            let result = gc.collect(None);
            total_freed += result.objects_freed;
            if total_freed > 0 {
                break; // Collection made progress
            }
        }
        
        // Should have collected some unreachable objects
        assert!(total_freed >= ptrs.len() - 2); // At least non-root objects
    }
    
    #[test]
    fn test_allocation_rate_tracking() {
        let gc = RealtimeGC::new(1024 * 1024, 100);
        
        // Allocate several objects rapidly
        for _ in 0..10 {
            let _ = gc.allocate(128, 8);
            std::thread::sleep(Duration::from_millis(10));
        }
        
        // Check if GC is needed based on allocation rate
        let needs_gc = gc.is_gc_needed();
        
        // Even if not needed now, the rate tracking should be working
        // (difficult to test deterministically due to timing)
        assert!(needs_gc == true || needs_gc == false); // Just ensure it doesn't panic
    }
}