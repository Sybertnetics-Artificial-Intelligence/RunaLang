// High-Performance Task System with AI-Guided Scheduling
// Supports task priorities, dependencies, and adaptive scheduling

use std::sync::{Arc, Weak};
use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering};
use std::collections::{HashMap, VecDeque};
use std::time::{Duration, Instant};
use std::pin::Pin;
use std::future::Future;
use std::task::{Context, Poll, Waker};

use super::AsyncError;

/// Unique task identifier
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct TaskId(pub u64);

impl TaskId {
    pub fn new() -> Self {
        static COUNTER: AtomicU64 = AtomicU64::new(0);
        TaskId(COUNTER.fetch_add(1, Ordering::Relaxed))
    }
}

/// Task priority levels for scheduling
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum TaskPriority {
    Critical = 0,   // System-critical tasks
    High = 1,       // User-interactive tasks
    Normal = 2,     // Default priority
    Low = 3,        // Background tasks
    Idle = 4,       // Only when nothing else to do
}

impl Default for TaskPriority {
    fn default() -> Self {
        TaskPriority::Normal
    }
}

/// Task execution state
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TaskState {
    Created,
    Scheduled,
    Running,
    Waiting,
    Completed,
    Cancelled,
    Failed,
}

/// Task metadata for scheduling and optimization
#[derive(Debug, Clone)]
pub struct TaskMetadata {
    pub id: TaskId,
    pub priority: TaskPriority,
    pub created_at: Instant,
    pub estimated_duration: Option<Duration>,
    pub dependencies: Vec<TaskId>,
    pub tags: Vec<String>,
    pub cpu_affinity: Option<usize>,
    pub memory_requirement: Option<usize>,
}

impl TaskMetadata {
    pub fn new(priority: TaskPriority) -> Self {
        Self {
            id: TaskId::new(),
            priority,
            created_at: Instant::now(),
            estimated_duration: None,
            dependencies: Vec::new(),
            tags: Vec::new(),
            cpu_affinity: None,
            memory_requirement: None,
        }
    }

    pub fn with_duration(mut self, duration: Duration) -> Self {
        self.estimated_duration = Some(duration);
        self
    }

    pub fn with_dependencies(mut self, deps: Vec<TaskId>) -> Self {
        self.dependencies = deps;
        self
    }

    pub fn with_tags(mut self, tags: Vec<String>) -> Self {
        self.tags = tags;
        self
    }

    pub fn with_cpu_affinity(mut self, cpu: usize) -> Self {
        self.cpu_affinity = Some(cpu);
        self
    }
}

/// Main task structure
pub struct Task<T> {
    metadata: TaskMetadata,
    future: Pin<Box<dyn Future<Output = T> + Send>>,
    state: TaskState,
    waker: Option<Waker>,
    result: Option<Result<T, AsyncError>>,
    start_time: Option<Instant>,
    execution_time: Option<Duration>,
    wake_count: AtomicUsize,
}

impl<T> Task<T>
where
    T: Send + Clone + 'static,
{
    /// Create new task from future
    pub fn new<F>(future: F, priority: TaskPriority) -> Self
    where
        F: Future<Output = T> + Send + 'static,
    {
        Self {
            metadata: TaskMetadata::new(priority),
            future: Box::pin(future),
            state: TaskState::Created,
            waker: None,
            result: None,
            start_time: None,
            execution_time: None,
            wake_count: AtomicUsize::new(0),
        }
    }

    /// Create task with metadata
    pub fn with_metadata<F>(future: F, metadata: TaskMetadata) -> Self
    where
        F: Future<Output = T> + Send + 'static,
    {
        Self {
            metadata,
            future: Box::pin(future),
            state: TaskState::Created,
            waker: None,
            result: None,
            start_time: None,
            execution_time: None,
            wake_count: AtomicUsize::new(0),
        }
    }

    /// Get task ID
    pub fn id(&self) -> TaskId {
        self.metadata.id
    }

    /// Get task priority
    pub fn priority(&self) -> TaskPriority {
        self.metadata.priority
    }

    /// Get task state
    pub fn state(&self) -> TaskState {
        self.state
    }

    /// Get task metadata
    pub fn metadata(&self) -> &TaskMetadata {
        &self.metadata
    }

    /// Poll the task for completion
    pub fn poll(&mut self, cx: &mut Context<'_>) -> Poll<Result<T, AsyncError>> {
        if let Some(result) = self.result.take() {
            return Poll::Ready(result);
        }

        self.waker = Some(cx.waker().clone());
        
        match self.state {
            TaskState::Created | TaskState::Scheduled => {
                self.state = TaskState::Running;
                self.start_time = Some(Instant::now());
            }
            TaskState::Waiting => {
                self.state = TaskState::Running;
                self.wake_count.fetch_add(1, Ordering::Relaxed);
            }
            _ => {}
        }

        // Poll the underlying future
        match self.future.as_mut().poll(cx) {
            Poll::Ready(value) => {
                self.state = TaskState::Completed;
                if let Some(start_time) = self.start_time {
                    self.execution_time = Some(start_time.elapsed());
                }
                self.result = Some(Ok(value.clone()));
                Poll::Ready(Ok(value))
            }
            Poll::Pending => {
                self.state = TaskState::Waiting;
                Poll::Pending
            }
        }
    }

    /// Cancel the task
    pub fn cancel(&mut self) {
        if matches!(self.state, TaskState::Completed | TaskState::Failed | TaskState::Cancelled) {
            return;
        }

        self.state = TaskState::Cancelled;
        self.result = Some(Err(AsyncError::TaskFailed("Task was cancelled".to_string())));
    }

    /// Get execution statistics
    pub fn stats(&self) -> TaskStats {
        TaskStats {
            id: self.metadata.id,
            priority: self.metadata.priority,
            state: self.state,
            created_at: self.metadata.created_at,
            started_at: self.start_time,
            execution_time: self.execution_time,
            wake_count: self.wake_count.load(Ordering::Relaxed),
        }
    }
}

// Note: RunnableTask implementation removed to eliminate dependencies on custom waker system
// The Task<T> can still be used as a standard Future through its Future trait implementation

/// Task execution statistics
#[derive(Debug, Clone)]
pub struct TaskStats {
    pub id: TaskId,
    pub priority: TaskPriority,
    pub state: TaskState,
    pub created_at: Instant,
    pub started_at: Option<Instant>,
    pub execution_time: Option<Duration>,
    pub wake_count: usize,
}

/// Task handle for external control
pub struct TaskHandle<T> {
    task_id: TaskId,
    shared_state: Arc<TaskSharedState<T>>,
}

impl<T> TaskHandle<T> {
    pub fn new(task_id: TaskId, shared_state: Arc<TaskSharedState<T>>) -> Self {
        Self {
            task_id,
            shared_state,
        }
    }

    /// Get task ID
    pub fn id(&self) -> TaskId {
        self.task_id
    }

    /// Check if task is completed
    pub fn is_completed(&self) -> bool {
        self.shared_state.is_completed()
    }

    /// Cancel the task
    pub fn cancel(&self) {
        self.shared_state.cancel();
    }

    /// Wait for task completion
    pub async fn await_result(&self) -> Result<T, AsyncError>
    where
        T: Clone,
    {
        self.shared_state.await_result().await
    }

    /// Get task statistics
    pub fn stats(&self) -> Option<TaskStats> {
        self.shared_state.stats()
    }
}

impl<T> Clone for TaskHandle<T> {
    fn clone(&self) -> Self {
        Self {
            task_id: self.task_id,
            shared_state: self.shared_state.clone(),
        }
    }
}

/// Shared state between task and handle
pub struct TaskSharedState<T> {
    completed: std::sync::atomic::AtomicBool,
    cancelled: std::sync::atomic::AtomicBool,
    result: std::sync::Mutex<Option<Result<T, AsyncError>>>,
    stats: std::sync::Mutex<Option<TaskStats>>,
    completion_wakers: std::sync::Mutex<Vec<Waker>>,
}

impl<T> TaskSharedState<T> {
    pub fn new() -> Self {
        Self {
            completed: std::sync::atomic::AtomicBool::new(false),
            cancelled: std::sync::atomic::AtomicBool::new(false),
            result: std::sync::Mutex::new(None),
            stats: std::sync::Mutex::new(None),
            completion_wakers: std::sync::Mutex::new(Vec::new()),
        }
    }

    pub fn is_completed(&self) -> bool {
        self.completed.load(Ordering::Acquire)
    }

    pub fn cancel(&self) {
        self.cancelled.store(true, Ordering::Release);
        self.wake_completion_waiters();
    }

    pub fn complete(&self, result: Result<T, AsyncError>) {
        if let Ok(mut res) = self.result.lock() {
            *res = Some(result);
        }
        self.completed.store(true, Ordering::Release);
        self.wake_completion_waiters();
    }

    pub fn update_stats(&self, stats: TaskStats) {
        if let Ok(mut task_stats) = self.stats.lock() {
            *task_stats = Some(stats);
        }
    }

    pub fn stats(&self) -> Option<TaskStats> {
        self.stats.lock().ok()?.clone()
    }

    pub async fn await_result(&self) -> Result<T, AsyncError>
    where
        T: Clone,
    {
        if self.is_completed() {
            if let Ok(result) = self.result.lock() {
                if let Some(ref res) = *result {
                    return res.clone();
                }
            }
        }

        // Wait for completion
        CompletionFuture::new(self).await
    }

    fn wake_completion_waiters(&self) {
        if let Ok(mut wakers) = self.completion_wakers.lock() {
            for waker in wakers.drain(..) {
                waker.wake();
            }
        }
    }

    fn register_completion_waker(&self, waker: Waker) {
        if let Ok(mut wakers) = self.completion_wakers.lock() {
            wakers.push(waker);
        }
    }
}

/// Future for waiting on task completion
struct CompletionFuture<'a, T> {
    shared_state: &'a TaskSharedState<T>,
}

impl<'a, T> CompletionFuture<'a, T> {
    fn new(shared_state: &'a TaskSharedState<T>) -> Self {
        Self { shared_state }
    }
}

impl<'a, T> Future for CompletionFuture<'a, T>
where
    T: Clone,
{
    type Output = Result<T, AsyncError>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.shared_state.is_completed() {
            if let Ok(result) = self.shared_state.result.lock() {
                if let Some(ref res) = *result {
                    return Poll::Ready(res.clone());
                }
            }
        }

        // Register waker for completion notification
        self.shared_state.register_completion_waker(cx.waker().clone());
        Poll::Pending
    }
}

/// Task group for managing related tasks
pub struct TaskGroup {
    tasks: std::sync::Mutex<HashMap<TaskId, TaskHandle<()>>>,
    completed_count: AtomicUsize,
    total_count: AtomicUsize,
    waiting_wakers: std::sync::Mutex<Vec<Waker>>,
}

impl TaskGroup {
    pub fn new() -> Self {
        Self {
            tasks: std::sync::Mutex::new(HashMap::new()),
            completed_count: AtomicUsize::new(0),
            total_count: AtomicUsize::new(0),
            waiting_wakers: std::sync::Mutex::new(Vec::new()),
        }
    }

    pub fn add_task(&self, handle: TaskHandle<()>) {
        self.total_count.fetch_add(1, Ordering::Relaxed);
        
        if let Ok(mut tasks) = self.tasks.lock() {
            tasks.insert(handle.id(), handle);
        }
    }

    pub fn wait_all(&self) -> impl Future<Output = ()> + '_ {
        TaskGroupWaitFuture::new(self)
    }

    pub fn cancel_all(&self) {
        if let Ok(tasks) = self.tasks.lock() {
            for handle in tasks.values() {
                handle.cancel();
            }
        }
    }

    pub fn completion_ratio(&self) -> f32 {
        let total = self.total_count.load(Ordering::Relaxed);
        if total == 0 {
            return 1.0;
        }
        
        let completed = self.completed_count.load(Ordering::Relaxed);
        completed as f32 / total as f32
    }
    
    pub fn notify_completion(&self) {
        if let Ok(mut wakers) = self.waiting_wakers.lock() {
            for waker in wakers.drain(..) {
                waker.wake();
            }
        }
    }
}

/// Future for waiting on task group completion
struct TaskGroupWaitFuture<'a> {
    group: &'a TaskGroup,
}

impl<'a> TaskGroupWaitFuture<'a> {
    fn new(group: &'a TaskGroup) -> Self {
        Self { group }
    }
}

impl<'a> Future for TaskGroupWaitFuture<'a> {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let total = self.group.total_count.load(Ordering::Relaxed);
        
        // Actually check each task's completion status
        let mut completed = 0;
        if let Ok(tasks) = self.group.tasks.lock() {
            for handle in tasks.values() {
                if handle.is_completed() {
                    completed += 1;
                }
            }
        }
        
        // Update completion count atomically
        self.group.completed_count.store(completed, Ordering::Relaxed);

        if completed >= total {
            Poll::Ready(())
        } else {
            // Register waker for completion notification
            if let Ok(mut wakers) = self.group.waiting_wakers.lock() {
                wakers.push(cx.waker().clone());
            }
            Poll::Pending
        }
    }
}

