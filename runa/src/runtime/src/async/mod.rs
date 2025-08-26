// Runa Async Runtime System
// High-performance, AI-guided async runtime with adaptive concurrency

pub mod event_loop;
pub mod executor;
pub mod future;
pub mod task;
pub mod timer;
pub mod channel;
pub mod scheduler;
pub mod waker;
pub mod reactor;
pub mod adaptive_concurrency;

pub use event_loop::*;
pub use executor::*;
pub use future::*;
pub use task::*;
pub use timer::*;
pub use channel::*;
pub use scheduler::*;
pub use waker::*;
pub use reactor::*;
pub use adaptive_concurrency::*;

use std::time::Duration;
use std::sync::Arc;
use std::collections::VecDeque;

/// Async runtime configuration for optimal performance tuning
#[derive(Debug, Clone)]
pub struct AsyncConfig {
    /// Number of worker threads (auto-detected if None)
    pub worker_threads: Option<usize>,
    /// Event loop polling timeout
    pub poll_timeout: Duration,
    /// Maximum tasks per scheduling cycle
    pub max_tasks_per_cycle: usize,
    /// Enable AI-guided task scheduling
    pub ai_scheduling: bool,
    /// Enable adaptive concurrency
    pub adaptive_concurrency: bool,
    /// Thread stack size in bytes
    pub thread_stack_size: usize,
    /// Maximum number of queued tasks
    pub max_queued_tasks: usize,
}

impl Default for AsyncConfig {
    fn default() -> Self {
        Self {
            worker_threads: None, // Auto-detect based on CPU cores
            poll_timeout: Duration::from_millis(10),
            max_tasks_per_cycle: 1000,
            ai_scheduling: true,
            adaptive_concurrency: true,
            thread_stack_size: 2 * 1024 * 1024, // 2MB
            max_queued_tasks: 10000,
        }
    }
}

/// Main async runtime entry point
#[derive(Debug)]
pub struct AsyncRuntime {
    config: AsyncConfig,
    executor: Arc<Executor>,
    scheduler: Arc<Scheduler>,
    reactor: Arc<Reactor>,
    timer_system: Arc<TimerSystem>,
    adaptive_concurrency: Option<Arc<AdaptiveConcurrencyController>>,
    running: std::sync::atomic::AtomicBool,
}

impl AsyncRuntime {
    /// Create new async runtime with default configuration
    pub fn new() -> Result<Self, AsyncError> {
        Self::with_config(AsyncConfig::default())
    }

    /// Create new async runtime with custom configuration
    pub fn with_config(config: AsyncConfig) -> Result<Self, AsyncError> {
        let worker_count = config.worker_threads.unwrap_or_else(|| {
            std::thread::available_parallelism()
                .map(|n| n.get())
                .unwrap_or(4)
        });

        let reactor = Arc::new(Reactor::new()?);
        let timer_system = Arc::new(TimerSystem::new(TimerConfig::default())?);
        let scheduler = Arc::new(Scheduler::new(worker_count, config.ai_scheduling)?);
        let executor = Arc::new(Executor::new(
            scheduler.clone(),
            reactor.clone(),
            timer_system.clone(),
            config.clone(),
        )?);

        // Create adaptive concurrency controller if enabled
        let adaptive_concurrency = if config.adaptive_concurrency {
            Some(Arc::new(AdaptiveConcurrencyController::new(worker_count)?))
        } else {
            None
        };

        Ok(Self {
            config,
            executor,
            scheduler,
            reactor,
            timer_system,
            adaptive_concurrency,
            running: std::sync::atomic::AtomicBool::new(false),
        })
    }

    /// Start the async runtime
    pub fn start(&self) -> Result<(), AsyncError> {
        if self.running.load(std::sync::atomic::Ordering::Acquire) {
            return Err(AsyncError::AlreadyRunning);
        }

        self.running.store(true, std::sync::atomic::Ordering::Release);
        self.executor.start()?;
        self.scheduler.start()?;
        self.reactor.start()?;
        self.timer_system.start()?;

        // Start adaptive concurrency controller if enabled
        if let Some(ref adaptive) = self.adaptive_concurrency {
            adaptive.start()?;
        }

        Ok(())
    }

    /// Stop the async runtime gracefully
    pub fn stop(&self) -> Result<(), AsyncError> {
        self.running.store(false, std::sync::atomic::Ordering::Release);
        
        // Stop adaptive concurrency controller first
        if let Some(ref adaptive) = self.adaptive_concurrency {
            adaptive.stop()?;
        }
        
        self.timer_system.stop()?;
        self.reactor.stop()?;
        self.scheduler.stop()?;
        self.executor.stop()?;

        Ok(())
    }

    /// Spawn a new async task
    pub fn spawn<F>(&self, future: F) -> TaskHandle<F::Output>
    where
        F: Future + Send + 'static,
        F::Output: Send + 'static,
    {
        self.executor.spawn(future)
    }

    /// Block the current thread until the future completes
    pub fn block_on<F>(&self, future: F) -> Result<F::Output, AsyncError>
    where
        F: Future + Send + 'static,
        F::Output: Send + 'static,
    {
        self.executor.block_on(future)
    }

    /// Get runtime statistics
    pub fn stats(&self) -> AsyncStats {
        let concurrency_metrics = self.adaptive_concurrency
            .as_ref()
            .map(|ac| ac.performance_metrics())
            .unwrap_or_else(|| ConcurrencyMetrics {
                average_utilization: self.scheduler.cpu_utilization(),
                efficiency_score: 0.5,
                throughput: 0.0,
                average_response_time: self.scheduler.average_task_duration(),
            });

        AsyncStats {
            active_tasks: self.scheduler.active_task_count(),
            queued_tasks: self.scheduler.queued_task_count(),
            completed_tasks: self.scheduler.completed_task_count(),
            worker_threads: self.scheduler.worker_count(),
            cpu_utilization: self.scheduler.cpu_utilization(),
            memory_usage: self.executor.memory_usage(),
            average_task_duration: self.scheduler.average_task_duration(),
            adaptive_thread_count: self.adaptive_concurrency.as_ref().map(|ac| ac.current_thread_count()),
            target_thread_count: self.adaptive_concurrency.as_ref().map(|ac| ac.target_thread_count()),
            concurrency_efficiency: concurrency_metrics.efficiency_score,
        }
    }

    /// Get current adaptive concurrency metrics (if enabled)
    pub fn concurrency_metrics(&self) -> Option<ConcurrencyMetrics> {
        self.adaptive_concurrency.as_ref().map(|ac| ac.performance_metrics())
    }

    /// Manually adjust thread count (if adaptive concurrency is enabled)
    pub fn set_thread_count(&self, count: usize) -> Result<(), AsyncError> {
        if let Some(ref adaptive) = self.adaptive_concurrency {
            adaptive.set_thread_count(count)
        } else {
            Err(AsyncError::SchedulerError("Adaptive concurrency not enabled".to_string()))
        }
    }
}

/// Runtime statistics for monitoring and optimization
#[derive(Debug, Clone)]
pub struct AsyncStats {
    pub active_tasks: usize,
    pub queued_tasks: usize,
    pub completed_tasks: u64,
    pub worker_threads: usize,
    pub cpu_utilization: f32,
    pub memory_usage: usize,
    pub average_task_duration: Duration,
    pub adaptive_thread_count: Option<usize>,
    pub target_thread_count: Option<usize>,
    pub concurrency_efficiency: f32,
}

/// Async runtime error types
#[derive(Debug, thiserror::Error)]
pub enum AsyncError {
    #[error("Runtime is already running")]
    AlreadyRunning,
    #[error("Runtime is not running")]
    NotRunning,
    #[error("Task execution failed: {0}")]
    TaskFailed(String),
    #[error("Scheduler error: {0}")]
    SchedulerError(String),
    #[error("Reactor error: {0}")]
    ReactorError(String),
    #[error("Timer error: {0}")]
    TimerError(String),
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
    #[error("Threading error: {0}")]
    ThreadError(String),
}

// Use standard library Future and Poll
pub use std::future::Future;
pub use std::task::Poll;