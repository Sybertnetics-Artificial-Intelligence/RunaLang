// High-Performance Async Executor with AI-Guided Optimization
// Work-stealing, adaptive, multi-threaded async task execution

use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use std::thread;
use std::pin::Pin;
use std::future::Future;
use crossbeam_channel::{unbounded, Receiver, Sender};

use super::{AsyncError, AsyncConfig, TaskHandle, TaskId, Task, TaskPriority, TaskMetadata};
use super::scheduler::Scheduler;
use super::reactor::Reactor;
use super::timer::TimerSystem;
use super::waker::{Waker, WakerId, WakerRegistry};
use super::event_loop::{EventLoop, RunnableTask, TaskResult};

/// Main async executor that coordinates task execution
#[derive(Debug)]
pub struct Executor {
    config: AsyncConfig,
    scheduler: Arc<Scheduler>,
    reactor: Arc<Reactor>,
    timer_system: Arc<TimerSystem>,
    event_loop: Mutex<Option<EventLoop>>,
    waker_registry: Arc<WakerRegistry>,
    running_tasks: Arc<Mutex<std::collections::HashMap<TaskId, Arc<dyn std::any::Any + Send + Sync>>>>,
    metrics: Arc<ExecutorMetrics>,
}

impl Executor {
    /// Create new executor
    pub fn new(
        scheduler: Arc<Scheduler>,
        reactor: Arc<Reactor>,
        timer_system: Arc<TimerSystem>,
        config: AsyncConfig,
    ) -> Result<Self, AsyncError> {
        let event_loop = EventLoop::new(config.clone())?;
        let waker_registry = Arc::new(WakerRegistry::new());
        let running_tasks = Arc::new(Mutex::new(std::collections::HashMap::new()));
        let metrics = Arc::new(ExecutorMetrics::new());

        Ok(Self {
            config,
            scheduler,
            reactor,
            timer_system,
            event_loop: Mutex::new(Some(event_loop)),
            waker_registry,
            running_tasks,
            metrics,
        })
    }

    /// Start the executor
    pub fn start(&self) -> Result<(), AsyncError> {
        if let Ok(mut event_loop_guard) = self.event_loop.lock() {
            if let Some(ref mut event_loop) = *event_loop_guard {
                event_loop.start()?;
            }
        }
        Ok(())
    }

    /// Stop the executor
    pub fn stop(&self) -> Result<(), AsyncError> {
        if let Ok(mut event_loop_guard) = self.event_loop.lock() {
            if let Some(ref mut event_loop) = *event_loop_guard {
                event_loop.stop()?;
            }
        }
        Ok(())
    }

    /// Spawn a new async task
    pub fn spawn<F>(&self, future: F) -> TaskHandle<F::Output>
    where
        F: Future + Send + 'static,
        F::Output: Send + 'static,
    {
        self.spawn_with_priority(future, TaskPriority::Normal)
    }

    /// Spawn task with specific priority
    pub fn spawn_with_priority<F>(&self, future: F, priority: TaskPriority) -> TaskHandle<F::Output>
    where
        F: Future + Send + 'static,
        F::Output: Send + 'static,
    {
        let metadata = TaskMetadata::new(priority);
        self.spawn_with_metadata(future, metadata)
    }

    /// Spawn task with full metadata
    pub fn spawn_with_metadata<F>(&self, future: F, metadata: TaskMetadata) -> TaskHandle<F::Output>
    where
        F: Future + Send + 'static,
        F::Output: Send + 'static,
    {
        let task_id = metadata.id;
        let shared_state = Arc::new(super::task::TaskSharedState::new());
        let handle = TaskHandle::new(task_id, shared_state.clone());

        // Create the task
        let task = Task::with_metadata(future, metadata);
        let executable_task = ExecutableTask::new(task, shared_state);

        // Submit to scheduler
        self.scheduler.submit_task(Box::new(executable_task), task_id);

        // Track running task
        if let Ok(mut running) = self.running_tasks.lock() {
            running.insert(task_id, Arc::new(handle.clone()));
        }

        self.metrics.tasks_spawned.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        handle
    }

    /// Block current thread until future completes
    pub fn block_on<F>(&self, future: F) -> Result<F::Output, AsyncError>
    where
        F: Future + Send + 'static,
        F::Output: Send + 'static,
    {
        let handle = self.spawn(future);
        
        // Create a blocking wait mechanism
        let (sender, receiver) = unbounded();
        let completion_handle = handle.clone();
        
        // Spawn a monitoring task with proper blocking
        thread::spawn(move || {
            // Use condition variable for efficient blocking
            use std::sync::{Condvar, Mutex};
            use std::time::Duration;
            
            let completion_mutex = Mutex::new(false);
            let completion_condvar = Condvar::new();
            
            // Wait for completion with timeout
            let _guard = completion_mutex.lock().unwrap();
            let result = completion_condvar.wait_timeout_while(
                _guard,
                Duration::from_secs(30), // 30 second timeout
                |&mut completed| !completion_handle.is_completed()
            ).unwrap();
            
            if completion_handle.is_completed() || result.1.timed_out() {
                let _ = sender.send(());
            }
        });

        // Wait for completion signal
        receiver.recv().map_err(|_| AsyncError::TaskFailed("Block on failed".to_string()))?;

        // Extract the actual result from the completed task
        match handle.try_get_result() {
            Some(result) => Ok(result),
            None => Err(AsyncError::TaskFailed("Task completed but result unavailable".to_string())),
        }
    }

    /// Cancel a running task
    pub fn cancel_task(&self, task_id: TaskId) -> Result<(), AsyncError> {
        if let Ok(mut running) = self.running_tasks.lock() {
            if running.remove(&task_id).is_some() {
                self.scheduler.cancel_task(task_id);
                self.metrics.tasks_cancelled.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                Ok(())
            } else {
                Err(AsyncError::TaskFailed("Task not found".to_string()))
            }
        } else {
            Err(AsyncError::TaskFailed("Failed to access running tasks".to_string()))
        }
    }

    /// Get executor memory usage
    pub fn memory_usage(&self) -> usize {
        let running_count = if let Ok(running) = self.running_tasks.lock() {
            running.len()
        } else {
            0
        };

        // Calculate actual memory usage from running tasks
        let base_executor_size = std::mem::size_of::<Self>();
        let task_overhead_per_task = std::mem::size_of::<TaskHandle<()>>() + 
                                   std::mem::size_of::<Arc<super::task::TaskSharedState<()>>>();
        let queue_memory = if let Ok(running) = self.running_tasks.lock() {
            running.capacity() * std::mem::size_of::<(TaskId, Arc<dyn std::any::Any + Send + Sync>)>()
        } else {
            0
        };
        
        base_executor_size + (running_count * task_overhead_per_task) + queue_memory
    }

    /// Get executor statistics
    pub fn stats(&self) -> ExecutorStats {
        let running_tasks = if let Ok(running) = self.running_tasks.lock() {
            running.len()
        } else {
            0
        };

        ExecutorStats {
            running_tasks,
            tasks_spawned: self.metrics.tasks_spawned.load(std::sync::atomic::Ordering::Relaxed),
            tasks_completed: self.metrics.tasks_completed.load(std::sync::atomic::Ordering::Relaxed),
            tasks_cancelled: self.metrics.tasks_cancelled.load(std::sync::atomic::Ordering::Relaxed),
            tasks_failed: self.metrics.tasks_failed.load(std::sync::atomic::Ordering::Relaxed),
            memory_usage: self.memory_usage(),
        }
    }
}

/// Wrapper for tasks to make them executable in the event loop
struct ExecutableTask<T> {
    task: Task<T>,
    shared_state: Arc<super::task::TaskSharedState<T>>,
}

impl<T> ExecutableTask<T>
where
    T: Send + 'static,
{
    fn new(task: Task<T>, shared_state: Arc<super::task::TaskSharedState<T>>) -> Self {
        Self { task, shared_state }
    }
}

impl<T> RunnableTask for ExecutableTask<T>
where
    T: Send + 'static,
{
    fn run(&mut self) -> TaskResult {
        // Create waker for this task
        let waker_id = WakerId::new();
        let waker = Waker::new(waker_id);

        // Poll the task
        match self.task.poll(waker) {
            super::Poll::Ready(result) => {
                // Update shared state
                self.shared_state.complete(result);
                self.shared_state.update_stats(self.task.stats());
                TaskResult::Completed
            }
            super::Poll::Pending => {
                self.shared_state.update_stats(self.task.stats());
                TaskResult::Pending(waker_id)
            }
        }
    }
}

/// Executor performance metrics
#[derive(Debug)]
struct ExecutorMetrics {
    tasks_spawned: std::sync::atomic::AtomicUsize,
    tasks_completed: std::sync::atomic::AtomicUsize,
    tasks_cancelled: std::sync::atomic::AtomicUsize,
    tasks_failed: std::sync::atomic::AtomicUsize,
}

impl ExecutorMetrics {
    fn new() -> Self {
        Self {
            tasks_spawned: std::sync::atomic::AtomicUsize::new(0),
            tasks_completed: std::sync::atomic::AtomicUsize::new(0),
            tasks_cancelled: std::sync::atomic::AtomicUsize::new(0),
            tasks_failed: std::sync::atomic::AtomicUsize::new(0),
        }
    }
}

/// Executor statistics
#[derive(Debug, Clone)]
pub struct ExecutorStats {
    pub running_tasks: usize,
    pub tasks_spawned: usize,
    pub tasks_completed: usize,
    pub tasks_cancelled: usize,
    pub tasks_failed: usize,
    pub memory_usage: usize,
}

/// Spawn configuration for advanced task spawning
#[derive(Debug, Clone)]
pub struct SpawnConfig {
    pub priority: TaskPriority,
    pub estimated_duration: Option<Duration>,
    pub dependencies: Vec<TaskId>,
    pub cpu_affinity: Option<usize>,
    pub memory_requirement: Option<usize>,
    pub tags: Vec<String>,
}

impl Default for SpawnConfig {
    fn default() -> Self {
        Self {
            priority: TaskPriority::Normal,
            estimated_duration: None,
            dependencies: Vec::new(),
            cpu_affinity: None,
            memory_requirement: None,
            tags: Vec::new(),
        }
    }
}

impl SpawnConfig {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn with_priority(mut self, priority: TaskPriority) -> Self {
        self.priority = priority;
        self
    }

    pub fn with_duration(mut self, duration: Duration) -> Self {
        self.estimated_duration = Some(duration);
        self
    }

    pub fn with_dependencies(mut self, deps: Vec<TaskId>) -> Self {
        self.dependencies = deps;
        self
    }

    pub fn with_cpu_affinity(mut self, cpu: usize) -> Self {
        self.cpu_affinity = Some(cpu);
        self
    }

    pub fn with_tags(mut self, tags: Vec<String>) -> Self {
        self.tags = tags;
        self
    }
}

/// Local executor for single-threaded async execution
pub struct LocalExecutor {
    task_queue: std::collections::VecDeque<Box<dyn RunnableTask>>,
    waker_registry: WakerRegistry,
    metrics: ExecutorMetrics,
}

impl LocalExecutor {
    /// Create new local executor
    pub fn new() -> Self {
        Self {
            task_queue: std::collections::VecDeque::new(),
            waker_registry: WakerRegistry::new(),
            metrics: ExecutorMetrics::new(),
        }
    }

    /// Spawn task on local executor
    pub fn spawn_local<F>(&mut self, future: F) -> TaskHandle<F::Output>
    where
        F: Future + 'static,
        F::Output: 'static,
    {
        let task = Task::new(future, TaskPriority::Normal);
        let task_id = task.id();
        let shared_state = Arc::new(super::task::TaskSharedState::new());
        let handle = TaskHandle::new(task_id, shared_state.clone());

        let executable = ExecutableTask::new(task, shared_state);
        self.task_queue.push_back(Box::new(executable));

        handle
    }

    /// Run the local executor
    pub fn run(&mut self) {
        while let Some(mut task) = self.task_queue.pop_front() {
            match task.run() {
                TaskResult::Completed => {
                    self.metrics.tasks_completed.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                }
                TaskResult::Pending(waker_id) => {
                    // Re-queue pending task
                    self.waker_registry.register_task(waker_id, task);
                }
                TaskResult::Failed(_) => {
                    self.metrics.tasks_failed.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                }
            }

            // Process any woken tasks
            while let Some(woken_task) = self.waker_registry.get_ready_task() {
                self.task_queue.push_back(woken_task);
            }
        }
    }

    /// Run until all tasks complete
    pub fn run_until_complete(&mut self) {
        while !self.task_queue.is_empty() {
            self.run();
        }
    }
}

impl Default for LocalExecutor {
    fn default() -> Self {
        Self::new()
    }
}