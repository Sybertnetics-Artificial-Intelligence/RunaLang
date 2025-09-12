// High-Performance Waker System for Async Task Coordination
// Optimized for minimal overhead and efficient task wakeup

use std::sync::{Arc, Mutex};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::collections::HashMap;
use super::event_loop::RunnableTask;

/// Unique identifier for wakers
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct WakerId(pub u64);

impl WakerId {
    pub fn new() -> Self {
        static COUNTER: AtomicU64 = AtomicU64::new(1);
        Self(COUNTER.fetch_add(1, Ordering::Relaxed))
    }
}

/// Waker for async task coordination
#[derive(Debug, Clone)]
pub struct Waker {
    id: WakerId,
    woken: Arc<AtomicBool>,
}

impl Waker {
    /// Create new waker with ID
    pub fn new(waker_id: WakerId) -> Self {
        Self {
            id: waker_id,
            woken: Arc::new(AtomicBool::new(false)),
        }
    }

    /// Wake the associated task
    pub fn wake(&self) {
        self.woken.store(true, Ordering::Release);
    }

    /// Wake the associated task by reference
    pub fn wake_by_ref(&self) {
        self.wake();
    }

    /// Check if the waker has been woken
    pub fn is_woken(&self) -> bool {
        self.woken.load(Ordering::Acquire)
    }

    /// Reset the waker state
    pub fn reset(&self) {
        self.woken.store(false, Ordering::Release);
    }

    /// Get the waker ID
    pub fn id(&self) -> WakerId {
        self.id
    }

    /// Clone the waker
    pub fn clone_waker(&self) -> Self {
        self.clone()
    }
}

/// Registry for managing waker-task relationships
#[derive(Debug)]
pub struct WakerRegistry {
    tasks: Mutex<HashMap<WakerId, Box<dyn RunnableTask>>>,
    ready_queue: Mutex<Vec<WakerId>>,
    woken_count: AtomicU64,
}

impl WakerRegistry {
    /// Create new waker registry
    pub fn new() -> Self {
        Self {
            tasks: Mutex::new(HashMap::new()),
            ready_queue: Mutex::new(Vec::new()),
            woken_count: AtomicU64::new(0),
        }
    }

    /// Register a task with a waker
    pub fn register_task(&self, waker_id: WakerId, task: Box<dyn RunnableTask>) {
        let mut tasks = self.tasks.lock().unwrap();
        tasks.insert(waker_id, task);
    }

    /// Unregister a task
    pub fn unregister_task(&self, waker_id: WakerId) -> Option<Box<dyn RunnableTask>> {
        let mut tasks = self.tasks.lock().unwrap();
        tasks.remove(&waker_id)
    }

    /// Wake a task by ID
    pub fn wake_task(&self, waker_id: WakerId) {
        let mut ready = self.ready_queue.lock().unwrap();
        ready.push(waker_id);
        self.woken_count.fetch_add(1, Ordering::Relaxed);
    }

    /// Get the next ready task
    pub fn get_ready_task(&self) -> Option<Box<dyn RunnableTask>> {
        let mut ready = self.ready_queue.lock().unwrap();
        if let Some(waker_id) = ready.pop() {
            let mut tasks = self.tasks.lock().unwrap();
            tasks.remove(&waker_id)
        } else {
            None
        }
    }

    /// Get all ready tasks
    pub fn get_all_ready_tasks(&self) -> Vec<Box<dyn RunnableTask>> {
        let mut ready = self.ready_queue.lock().unwrap();
        let mut tasks = self.tasks.lock().unwrap();
        let mut ready_tasks = Vec::new();

        for waker_id in ready.drain(..) {
            if let Some(task) = tasks.remove(&waker_id) {
                ready_tasks.push(task);
            }
        }

        ready_tasks
    }

    /// Check if any tasks are ready
    pub fn has_ready_tasks(&self) -> bool {
        let ready = self.ready_queue.lock().unwrap();
        !ready.is_empty()
    }

    /// Get the number of registered tasks
    pub fn task_count(&self) -> usize {
        let tasks = self.tasks.lock().unwrap();
        tasks.len()
    }

    /// Get the number of ready tasks
    pub fn ready_count(&self) -> usize {
        let ready = self.ready_queue.lock().unwrap();
        ready.len()
    }
}

impl Default for WakerRegistry {
    fn default() -> Self {
        Self::new()
    }
}

/// Waker factory for creating wakers with specific behavior
#[derive(Debug)]
pub struct WakerFactory {
    registry: Arc<WakerRegistry>,
}

impl WakerFactory {
    /// Create new waker factory
    pub fn new(registry: Arc<WakerRegistry>) -> Self {
        Self { registry }
    }

    /// Create a new waker
    pub fn create_waker(&self) -> (WakerId, Waker) {
        let waker_id = WakerId::new();
        let waker = Waker::new(waker_id);
        (waker_id, waker)
    }

    /// Create a waker that automatically registers with the registry
    pub fn create_registered_waker(&self, task: Box<dyn RunnableTask>) -> (WakerId, Waker) {
        let (waker_id, waker) = self.create_waker();
        self.registry.register_task(waker_id, task);
        (waker_id, waker)
    }

    /// Get reference to the registry
    pub fn registry(&self) -> &Arc<WakerRegistry> {
        &self.registry
    }
}

/// Collection of wakers for batch operations
#[derive(Debug)]
pub struct WakerCollection {
    wakers: Vec<Waker>,
}

impl WakerCollection {
    /// Create new waker collection
    pub fn new() -> Self {
        Self {
            wakers: Vec::new(),
        }
    }

    /// Add a waker to the collection
    pub fn add(&mut self, waker: Waker) {
        self.wakers.push(waker);
    }

    /// Wake all wakers in the collection
    pub fn wake_all(&self) {
        for waker in &self.wakers {
            waker.wake();
        }
    }

    /// Reset all wakers in the collection
    pub fn reset_all(&self) {
        for waker in &self.wakers {
            waker.reset();
        }
    }

    /// Check if any waker has been woken
    pub fn any_woken(&self) -> bool {
        self.wakers.iter().any(|w| w.is_woken())
    }

    /// Check if all wakers have been woken
    pub fn all_woken(&self) -> bool {
        self.wakers.iter().all(|w| w.is_woken())
    }

    /// Get the number of wakers
    pub fn len(&self) -> usize {
        self.wakers.len()
    }

    /// Check if the collection is empty
    pub fn is_empty(&self) -> bool {
        self.wakers.is_empty()
    }

    /// Clear all wakers
    pub fn clear(&mut self) {
        self.wakers.clear();
    }
}

impl Default for WakerCollection {
    fn default() -> Self {
        Self::new()
    }
}

/// Waker statistics for monitoring and debugging
#[derive(Debug, Clone)]
pub struct WakerStats {
    pub total_wakers: usize,
    pub active_wakers: usize,
    pub woken_wakers: usize,
    pub ready_tasks: usize,
}

impl WakerRegistry {
    /// Get waker statistics
    pub fn stats(&self) -> WakerStats {
        let tasks = self.tasks.lock().unwrap();
        let ready = self.ready_queue.lock().unwrap();

        WakerStats {
            total_wakers: tasks.len(),
            active_wakers: tasks.len(),
            woken_wakers: self.woken_count.load(Ordering::Relaxed) as usize,
            ready_tasks: ready.len(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use super::super::event_loop::{TaskResult};

    struct TestTask {
        id: u32,
    }

    impl RunnableTask for TestTask {
        fn run(&mut self) -> TaskResult {
            TaskResult::Completed
        }
    }

    #[test]
    fn test_waker_creation() {
        let waker_id = WakerId::new();
        let waker = Waker::new(waker_id);
        assert_eq!(waker.id(), waker_id);
        assert!(!waker.is_woken());
    }

    #[test]
    fn test_waker_wake() {
        let waker_id = WakerId::new();
        let waker = Waker::new(waker_id);
        
        assert!(!waker.is_woken());
        waker.wake();
        assert!(waker.is_woken());
        
        waker.reset();
        assert!(!waker.is_woken());
    }

    #[test]
    fn test_waker_registry() {
        let registry = WakerRegistry::new();
        let waker_id = WakerId::new();
        let task = Box::new(TestTask { id: 1 });

        registry.register_task(waker_id, task);
        assert_eq!(registry.task_count(), 1);

        registry.wake_task(waker_id);
        assert_eq!(registry.ready_count(), 1);

        let ready_task = registry.get_ready_task();
        assert!(ready_task.is_some());
        assert_eq!(registry.task_count(), 0);
        assert_eq!(registry.ready_count(), 0);
    }

    #[test]
    fn test_waker_collection() {
        let mut collection = WakerCollection::new();
        
        let waker1 = Waker::new(WakerId::new());
        let waker2 = Waker::new(WakerId::new());
        
        collection.add(waker1);
        collection.add(waker2);
        
        assert_eq!(collection.len(), 2);
        assert!(!collection.any_woken());
        
        collection.wake_all();
        assert!(collection.all_woken());
    }

    #[test]
    fn test_waker_factory() {
        let registry = Arc::new(WakerRegistry::new());
        let factory = WakerFactory::new(registry.clone());
        
        let (waker_id, waker) = factory.create_waker();
        assert_eq!(waker.id(), waker_id);
        
        let task = Box::new(TestTask { id: 1 });
        let (reg_waker_id, _reg_waker) = factory.create_registered_waker(task);
        assert_eq!(registry.task_count(), 1);
    }
}