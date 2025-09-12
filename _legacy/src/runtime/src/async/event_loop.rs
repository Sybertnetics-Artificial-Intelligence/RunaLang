// Production-Ready Event Loop for Async Task Execution
// Simple, reliable, and efficient async runtime

use std::sync::{Arc, Mutex};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::collections::VecDeque;
use std::time::{Duration, Instant};
use std::thread;
use crossbeam_channel::{unbounded, Receiver, Sender};
use std::pin::Pin;
use std::task::{Context, Poll, Waker};
use std::future::Future;

use super::{AsyncError, AsyncConfig};
use super::waker::{WakerId, WakerRegistry};

/// Main event loop that drives async execution
#[derive(Debug)]
pub struct EventLoop {
    config: AsyncConfig,
    running: AtomicBool,
    threads: Vec<thread::JoinHandle<()>>,
    task_queue: Arc<TaskQueue>,
    waker_registry: Arc<WakerRegistry>,
    io_reactor: Arc<IoReactor>,
    metrics: Arc<EventLoopMetrics>,
    adaptive_controller: Arc<AdaptiveController>,
}

impl EventLoop {
    /// Create new event loop with configuration
    pub fn new(config: AsyncConfig) -> Result<Self, AsyncError> {
        let worker_count = config.worker_threads.unwrap_or_else(|| {
            std::thread::available_parallelism().map(|n| n.get()).unwrap_or(4)
        });

        let task_queue = Arc::new(TaskQueue::new(config.max_queued_tasks));
        let waker_registry = Arc::new(WakerRegistry::new());
        let io_reactor = Arc::new(IoReactor::new()?);
        let metrics = Arc::new(EventLoopMetrics::new());
        let adaptive_controller = Arc::new(AdaptiveController::new(config.adaptive_concurrency));

        Ok(Self {
            config,
            running: AtomicBool::new(false),
            threads: Vec::with_capacity(worker_count),
            task_queue,
            waker_registry,
            io_reactor,
            metrics,
            adaptive_controller,
        })
    }

    /// Start the event loop with worker threads
    pub fn start(&mut self) -> Result<(), AsyncError> {
        if self.running.load(Ordering::Acquire) {
            return Err(AsyncError::AlreadyRunning);
        }

        self.running.store(true, Ordering::Release);

        // Start IO reactor
        self.io_reactor.start()?;

        // Start worker threads
        let worker_count = self.config.worker_threads.unwrap_or(4);
        for thread_id in 0..worker_count {
            let task_queue = self.task_queue.clone();
            let waker_registry = self.waker_registry.clone();
            let io_reactor = self.io_reactor.clone();
            let metrics = self.metrics.clone();
            let adaptive_controller = self.adaptive_controller.clone();
            let running = self.running.clone();
            let config = self.config.clone();

            let handle = thread::Builder::new()
                .name(format!("runa-async-worker-{}", thread_id))
                .stack_size(config.thread_stack_size)
                .spawn(move || {
                    Self::worker_loop(
                        thread_id,
                        task_queue,
                        waker_registry,
                        io_reactor,
                        metrics,
                        adaptive_controller,
                        running,
                        config,
                    );
                })
                .map_err(|e| AsyncError::ThreadError(e.to_string()))?;

            self.threads.push(handle);
        }

        Ok(())
    }

    /// Stop the event loop gracefully
    pub fn stop(&mut self) -> Result<(), AsyncError> {
        self.running.store(false, Ordering::Release);

        // Stop IO reactor
        self.io_reactor.running.store(false, Ordering::Release);

        // Wait for all worker threads to finish
        while let Some(handle) = self.threads.pop() {
            handle.join().map_err(|_| AsyncError::ThreadError("Failed to join worker thread".to_string()))?;
        }

        Ok(())
    }

    /// Main worker thread loop - production-ready task execution
    fn worker_loop(
        thread_id: usize,
        task_queue: Arc<TaskQueue>,
        waker_registry: Arc<WakerRegistry>,
        io_reactor: Arc<IoReactor>,
        metrics: Arc<EventLoopMetrics>,
        adaptive_controller: Arc<AdaptiveController>,
        running: Arc<AtomicBool>,
        config: AsyncConfig,
    ) {
        let mut local_queue = VecDeque::new();
        let mut idle_start = None;
        let mut last_adaptation = Instant::now();

        while running.load(Ordering::Acquire) {
            let cycle_start = Instant::now();
            let mut tasks_processed = 0;

            // Process tasks from local queue first
            while let Some(task) = local_queue.pop_front() {
                if tasks_processed >= config.max_tasks_per_cycle {
                    local_queue.push_front(task);
                    break;
                }

                Self::execute_task(task, &waker_registry, &metrics);
                tasks_processed += 1;
            }

            // Try to steal work from global queue
            if let Some(stolen_tasks) = task_queue.steal_work(32) {
                local_queue.extend(stolen_tasks);
                idle_start = None;
            }

            // Poll IO reactor for ready events
            if let Ok(ready_wakers) = io_reactor.poll(config.poll_timeout) {
                for waker_id in ready_wakers {
                    waker_registry.wake_task(waker_id);
                }
            }

            // Check for newly woken tasks
            while let Some(task) = waker_registry.get_ready_task() {
                if local_queue.len() < 64 {
                    local_queue.push_back(task);
                } else {
                    task_queue.push(task);
                }
            }

            // Adaptive behavior adjustment
            if last_adaptation.elapsed() >= Duration::from_millis(100) {
                adaptive_controller.adjust_behavior(
                    thread_id,
                    tasks_processed,
                    cycle_start.elapsed(),
                    local_queue.len(),
                );
                last_adaptation = Instant::now();
            }

            // Track idle time for adaptive scheduling
            if tasks_processed == 0 {
                if idle_start.is_none() {
                    idle_start = Some(Instant::now());
                }
            } else {
                idle_start = None;
            }

            // Update metrics
            metrics.record_cycle(thread_id, tasks_processed, cycle_start.elapsed());

            // Yield if we're idle for too long
            if let Some(idle_time) = idle_start {
                if idle_time.elapsed() > Duration::from_millis(1) {
                    thread::yield_now();
                }
            }
        }
    }

    /// Execute a single task
    fn execute_task(
        mut task: Box<dyn RunnableTask>,
        waker_registry: &Arc<WakerRegistry>,
        metrics: &Arc<EventLoopMetrics>,
    ) {
        let start_time = Instant::now();
        
        match task.run() {
            TaskResult::Completed => {
                metrics.record_task_completion(start_time.elapsed());
            }
            TaskResult::Pending(waker_id) => {
                waker_registry.register_task(waker_id, task);
            }
            TaskResult::Failed(error) => {
                metrics.record_task_failure();
                eprintln!("Task failed: {}", error);
            }
        }
    }

    /// Add a task to the event loop
    pub fn spawn_task(&self, task: Box<dyn RunnableTask>) -> Result<(), AsyncError> {
        if !self.running.load(Ordering::Acquire) {
            return Err(AsyncError::NotRunning);
        }

        self.task_queue.push(task);
        Ok(())
    }

    /// Get current metrics
    pub fn metrics(&self) -> EventLoopStats {
        self.metrics.snapshot()
    }
}

/// Thread-safe task queue with work stealing
#[derive(Debug)]
pub struct TaskQueue {
    global_queue: Mutex<VecDeque<Box<dyn RunnableTask>>>,
    max_size: usize,
    queued_count: AtomicUsize,
}

impl TaskQueue {
    pub fn new(max_size: usize) -> Self {
        Self {
            global_queue: Mutex::new(VecDeque::new()),
            max_size,
            queued_count: AtomicUsize::new(0),
        }
    }

    pub fn push(&self, task: Box<dyn RunnableTask>) {
        if let Ok(mut queue) = self.global_queue.lock() {
            if queue.len() < self.max_size {
                queue.push_back(task);
                self.queued_count.fetch_add(1, Ordering::Relaxed);
            }
        }
    }

    pub fn steal_work(&self, max_tasks: usize) -> Option<Vec<Box<dyn RunnableTask>>> {
        if let Ok(mut queue) = self.global_queue.lock() {
            if queue.is_empty() {
                return None;
            }

            let steal_count = (queue.len() / 2).min(max_tasks);
            let mut stolen = Vec::with_capacity(steal_count);

            for _ in 0..steal_count {
                if let Some(task) = queue.pop_front() {
                    stolen.push(task);
                    self.queued_count.fetch_sub(1, Ordering::Relaxed);
                }
            }

            if stolen.is_empty() {
                None
            } else {
                Some(stolen)
            }
        } else {
            None
        }
    }

    pub fn len(&self) -> usize {
        self.queued_count.load(Ordering::Relaxed)
    }
}


/// IO reactor for handling async I/O operations
#[derive(Debug)]
pub struct IoReactor {
    running: AtomicBool,
    poll_thread: Option<thread::JoinHandle<()>>,
    event_sender: Sender<WakerId>,
    event_receiver: Receiver<WakerId>,
}

impl IoReactor {
    pub fn new() -> Result<Self, AsyncError> {
        let (event_sender, event_receiver) = unbounded();
        
        Ok(Self {
            running: AtomicBool::new(false),
            poll_thread: None,
            event_sender,
            event_receiver,
        })
    }

    pub fn start(&mut self) -> Result<(), AsyncError> {
        if self.running.load(Ordering::Acquire) {
            return Err(AsyncError::AlreadyRunning);
        }

        self.running.store(true, Ordering::Release);

        // Start IO polling thread
        let running = self.running.clone();
        let sender = self.event_sender.clone();
        let (fd_sender, fd_receiver) = unbounded::<(i32, WakerId)>();
        
        let handle = thread::spawn(move || {
            Self::io_poll_loop(running, sender, fd_receiver);
        });

        self.poll_thread = Some(handle);
        Ok(())
    }

    pub fn stop(&mut self) -> Result<(), AsyncError> {
        self.running.store(false, Ordering::Release);

        if let Some(handle) = self.poll_thread.take() {
            handle.join().map_err(|_| AsyncError::ThreadError("Failed to join IO thread".to_string()))?;
        }

        Ok(())
    }

    pub fn poll(&self, timeout: Duration) -> Result<Vec<WakerId>, AsyncError> {
        let mut wakers = Vec::new();
        let deadline = Instant::now() + timeout;

        while Instant::now() < deadline {
            match self.event_receiver.try_recv() {
                Ok(waker_id) => wakers.push(waker_id),
                Err(_) => break,
            }
        }

        Ok(wakers)
    }

    fn io_poll_loop(running: Arc<AtomicBool>, sender: Sender<WakerId>, fd_receiver: Receiver<(i32, WakerId)>) {
        let mut poll_fds = Vec::new();
        let mut waker_map = std::collections::HashMap::new();
        
        while running.load(Ordering::Acquire) {
            poll_fds.clear();
            
            #[cfg(unix)]
            {
                // Unix platforms: use poll() system call
                use std::os::unix::io::RawFd;
                
                // Collect file descriptors to poll
                for (fd, waker_id) in &waker_map {
                    poll_fds.push(libc::pollfd {
                        fd: *fd,
                        events: libc::POLLIN | libc::POLLOUT,
                        revents: 0,
                    });
                }
                
                if !poll_fds.is_empty() {
                    unsafe {
                        let result = libc::poll(
                            poll_fds.as_mut_ptr(),
                            poll_fds.len() as libc::nfds_t,
                            10, // 10ms timeout
                        );
                        
                        if result > 0 {
                            // Check which file descriptors are ready
                            for (i, poll_fd) in poll_fds.iter().enumerate() {
                                if poll_fd.revents != 0 {
                                    if let Some(waker_id) = waker_map.get(&poll_fd.fd) {
                                        let _ = sender.send(*waker_id);
                                    }
                                }
                            }
                        }
                    }
                } else {
                    // No file descriptors to poll, just wait a bit
                    thread::sleep(Duration::from_millis(10));
                }
            }
            
            #[cfg(windows)]
            {
                // Windows: use WaitForMultipleObjects
                use std::os::windows::io::RawHandle;
                
                if !waker_map.is_empty() {
                    let handles: Vec<RawHandle> = waker_map.keys().map(|&h| h as RawHandle).collect();
                    
                    unsafe {
                        let result = winapi::um::synchapi::WaitForMultipleObjects(
                            handles.len() as u32,
                            handles.as_ptr() as *const winapi::um::winnt::HANDLE,
                            0, // Don't wait for all
                            10, // 10ms timeout
                        );
                        
                        if result >= winapi::um::winbase::WAIT_OBJECT_0 &&
                           result < winapi::um::winbase::WAIT_OBJECT_0 + handles.len() as u32 {
                            let ready_index = (result - winapi::um::winbase::WAIT_OBJECT_0) as usize;
                            if let Some(waker_id) = waker_map.get(&(handles[ready_index] as i32)) {
                                let _ = sender.send(*waker_id);
                            }
                        }
                    }
                } else {
                    thread::sleep(Duration::from_millis(10));
                }
            }
            
            // Check for new file descriptor registrations
            while let Ok((fd, waker_id)) = fd_receiver.try_recv() {
                waker_map.insert(fd, waker_id);
            }
        }
    }
}

/// Adaptive controller for dynamic behavior adjustment
#[derive(Debug)]
pub struct AdaptiveController {
    enabled: bool,
    thread_stats: Mutex<std::collections::HashMap<usize, ThreadStats>>,
}

impl AdaptiveController {
    pub fn new(enabled: bool) -> Self {
        Self {
            enabled,
            thread_stats: Mutex::new(std::collections::HashMap::new()),
        }
    }

    pub fn adjust_behavior(
        &self,
        thread_id: usize,
        tasks_processed: usize,
        cycle_time: Duration,
        queue_length: usize,
    ) {
        if !self.enabled {
            return;
        }

        if let Ok(mut stats) = self.thread_stats.lock() {
            let thread_stats = stats.entry(thread_id).or_insert_with(ThreadStats::new);
            thread_stats.update(tasks_processed, cycle_time, queue_length);
        }
    }
}

/// Per-thread statistics for adaptive behavior
#[derive(Debug)]
struct ThreadStats {
    total_tasks: usize,
    total_time: Duration,
    avg_queue_length: f64,
    cycles: usize,
}

impl ThreadStats {
    fn new() -> Self {
        Self {
            total_tasks: 0,
            total_time: Duration::ZERO,
            avg_queue_length: 0.0,
            cycles: 0,
        }
    }

    fn update(&mut self, tasks: usize, time: Duration, queue_length: usize) {
        self.total_tasks += tasks;
        self.total_time += time;
        self.cycles += 1;
        
        // Exponential moving average for queue length
        let alpha = 0.1;
        self.avg_queue_length = alpha * queue_length as f64 + (1.0 - alpha) * self.avg_queue_length;
    }
}

/// Event loop performance metrics
#[derive(Debug)]
pub struct EventLoopMetrics {
    cycles_completed: AtomicUsize,
    tasks_completed: AtomicUsize,
    tasks_failed: AtomicUsize,
    total_cycle_time: std::sync::atomic::AtomicU64,
    total_task_time: std::sync::atomic::AtomicU64,
}

impl EventLoopMetrics {
    pub fn new() -> Self {
        Self {
            cycles_completed: AtomicUsize::new(0),
            tasks_completed: AtomicUsize::new(0),
            tasks_failed: AtomicUsize::new(0),
            total_cycle_time: std::sync::atomic::AtomicU64::new(0),
            total_task_time: std::sync::atomic::AtomicU64::new(0),
        }
    }

    pub fn record_cycle(&self, _thread_id: usize, tasks_processed: usize, cycle_time: Duration) {
        self.cycles_completed.fetch_add(1, Ordering::Relaxed);
        self.tasks_completed.fetch_add(tasks_processed, Ordering::Relaxed);
        self.total_cycle_time.fetch_add(cycle_time.as_nanos() as u64, Ordering::Relaxed);
    }

    pub fn record_task_completion(&self, task_time: Duration) {
        self.total_task_time.fetch_add(task_time.as_nanos() as u64, Ordering::Relaxed);
    }

    pub fn record_task_failure(&self) {
        self.tasks_failed.fetch_add(1, Ordering::Relaxed);
    }

    pub fn snapshot(&self) -> EventLoopStats {
        EventLoopStats {
            cycles_completed: self.cycles_completed.load(Ordering::Relaxed),
            tasks_completed: self.tasks_completed.load(Ordering::Relaxed),
            tasks_failed: self.tasks_failed.load(Ordering::Relaxed),
            average_cycle_time: Duration::from_nanos(
                self.total_cycle_time.load(Ordering::Relaxed) / 
                self.cycles_completed.load(Ordering::Relaxed).max(1) as u64
            ),
            average_task_time: Duration::from_nanos(
                self.total_task_time.load(Ordering::Relaxed) / 
                self.tasks_completed.load(Ordering::Relaxed).max(1) as u64
            ),
        }
    }
}

/// Event loop statistics snapshot
#[derive(Debug, Clone)]
pub struct EventLoopStats {
    pub cycles_completed: usize,
    pub tasks_completed: usize,
    pub tasks_failed: usize,
    pub average_cycle_time: Duration,
    pub average_task_time: Duration,
}



/// Result of task execution
pub enum TaskResult {
    Completed,
    Pending(WakerId),
    Failed(String),
}

/// Trait for runnable tasks in the event loop
pub trait RunnableTask: Send {
    fn run(&mut self) -> TaskResult;
}