// High-Precision Timer System for Async Runtime
// Provides delayed execution, intervals, and timeout functionality

use std::collections::BinaryHeap;
use std::cmp::{Ordering, Reverse};
use std::sync::{Arc, Mutex, RwLock};
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};
use std::thread;
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering as AtomicOrdering};
use crossbeam_channel::{bounded, unbounded, Receiver, Sender};

use super::{AsyncError, TaskId, TaskHandle};
use super::waker::{Waker, WakerId};

/// Unique identifier for timer entries
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct TimerId(pub u64);

impl TimerId {
    pub fn new() -> Self {
        static COUNTER: AtomicU64 = AtomicU64::new(1);
        Self(COUNTER.fetch_add(1, AtomicOrdering::Relaxed))
    }
}

/// Timer system for delayed execution and scheduling
#[derive(Debug)]
pub struct TimerSystem {
    timer_queue: Arc<Mutex<BinaryHeap<Reverse<TimerEntry>>>>,
    timer_thread: Mutex<Option<thread::JoinHandle<()>>>,
    waker_sender: Sender<TimerWakeup>,
    waker_receiver: Receiver<TimerWakeup>,
    running: AtomicBool,
    metrics: Arc<TimerMetrics>,
    config: TimerConfig,
    resolution: AtomicU64, // nanoseconds
    drift_compensator: Arc<DriftCompensator>,
}

impl TimerSystem {
    /// Create new timer system
    pub fn new(config: TimerConfig) -> Result<Self, AsyncError> {
        let (waker_sender, waker_receiver) = unbounded();
        let timer_queue = Arc::new(Mutex::new(BinaryHeap::new()));
        let metrics = Arc::new(TimerMetrics::new());
        let drift_compensator = Arc::new(DriftCompensator::new());
        let resolution = AtomicU64::new(config.resolution.as_nanos() as u64);

        Ok(Self {
            timer_queue,
            timer_thread: Mutex::new(None),
            waker_sender,
            waker_receiver,
            running: AtomicBool::new(false),
            metrics,
            config,
            resolution,
            drift_compensator,
        })
    }

    /// Start the timer system
    pub fn start(&self) -> Result<(), AsyncError> {
        if self.running.swap(true, AtomicOrdering::SeqCst) {
            return Err(AsyncError::TimerError("Timer system already running".to_string()));
        }

        let queue = self.timer_queue.clone();
        let sender = self.waker_sender.clone();
        let running = Arc::new(AtomicBool::new(true));
        let running_clone = running.clone();
        let metrics = self.metrics.clone();
        let resolution = self.resolution.load(AtomicOrdering::Relaxed);
        let drift_comp = self.drift_compensator.clone();

        let timer_thread = thread::Builder::new()
            .name("timer-system".to_string())
            .spawn(move || {
                let mut last_tick = Instant::now();
                
                while running_clone.load(AtomicOrdering::Relaxed) {
                    let now = Instant::now();
                    let mut expired_timers = Vec::new();

                    // Process expired timers
                    {
                        let mut heap = queue.lock().unwrap();
                        while let Some(Reverse(entry)) = heap.peek() {
                            if entry.deadline <= now {
                                let timer = heap.pop().unwrap().0;
                                expired_timers.push(timer);
                            } else {
                                break;
                            }
                        }
                    }

                    // Send wakeups for expired timers
                    for timer in expired_timers {
                        let wakeup = TimerWakeup {
                            timer_id: timer.id,
                            waker_id: timer.waker_id,
                            execution_time: now,
                            scheduled_time: timer.deadline,
                        };
                        
                        if sender.send(wakeup).is_ok() {
                            metrics.timers_fired.fetch_add(1, AtomicOrdering::Relaxed);
                        }

                        // Handle recurring timers
                        if let Some(interval) = timer.interval {
                            let next_deadline = timer.deadline + interval;
                            let recurring = TimerEntry {
                                id: timer.id,
                                deadline: next_deadline,
                                waker_id: timer.waker_id,
                                interval: timer.interval,
                                metadata: timer.metadata,
                            };
                            
                            queue.lock().unwrap().push(Reverse(recurring));
                        }
                    }

                    // Adaptive sleep with drift compensation
                    let elapsed = now.duration_since(last_tick);
                    let target_duration = Duration::from_nanos(resolution);
                    
                    drift_comp.record_timing(elapsed, target_duration);
                    let compensated_sleep = drift_comp.get_compensated_sleep(target_duration);
                    
                    if compensated_sleep > Duration::from_nanos(0) {
                        thread::sleep(compensated_sleep);
                    }
                    
                    last_tick = now;
                }
            })
            .map_err(|e| AsyncError::TimerError(format!("Failed to start timer thread: {}", e)))?;

        *self.timer_thread.lock().unwrap() = Some(timer_thread);
        Ok(())
    }

    /// Stop the timer system
    pub fn stop(&self) -> Result<(), AsyncError> {
        if !self.running.swap(false, AtomicOrdering::SeqCst) {
            return Ok(()); // Already stopped
        }

        if let Some(handle) = self.timer_thread.lock().unwrap().take() {
            handle.join().map_err(|_| AsyncError::TimerError("Failed to join timer thread".to_string()))?;
        }

        Ok(())
    }

    /// Schedule a one-shot timer
    pub fn schedule_once(&self, delay: Duration, waker_id: WakerId) -> Result<TimerId, AsyncError> {
        let timer_id = TimerId::new();
        let deadline = Instant::now() + delay;
        
        let entry = TimerEntry {
            id: timer_id,
            deadline,
            waker_id,
            interval: None,
            metadata: TimerMetadata::default(),
        };

        {
            let mut queue = self.timer_queue.lock().unwrap();
            queue.push(Reverse(entry));
        }

        self.metrics.timers_scheduled.fetch_add(1, AtomicOrdering::Relaxed);
        Ok(timer_id)
    }

    /// Schedule a recurring timer
    pub fn schedule_recurring(&self, interval: Duration, waker_id: WakerId) -> Result<TimerId, AsyncError> {
        let timer_id = TimerId::new();
        let deadline = Instant::now() + interval;
        
        let entry = TimerEntry {
            id: timer_id,
            deadline,
            waker_id,
            interval: Some(interval),
            metadata: TimerMetadata::default(),
        };

        {
            let mut queue = self.timer_queue.lock().unwrap();
            queue.push(Reverse(entry));
        }

        self.metrics.timers_scheduled.fetch_add(1, AtomicOrdering::Relaxed);
        Ok(timer_id)
    }

    /// Schedule timer with metadata
    pub fn schedule_with_metadata(
        &self,
        delay: Duration,
        waker_id: WakerId,
        metadata: TimerMetadata,
    ) -> Result<TimerId, AsyncError> {
        let timer_id = TimerId::new();
        let deadline = Instant::now() + delay;
        
        let entry = TimerEntry {
            id: timer_id,
            deadline,
            waker_id,
            interval: None,
            metadata,
        };

        {
            let mut queue = self.timer_queue.lock().unwrap();
            queue.push(Reverse(entry));
        }

        self.metrics.timers_scheduled.fetch_add(1, AtomicOrdering::Relaxed);
        Ok(timer_id)
    }

    /// Cancel a timer
    pub fn cancel_timer(&self, timer_id: TimerId) -> Result<(), AsyncError> {
        let mut queue = self.timer_queue.lock().unwrap();
        let mut temp_heap = BinaryHeap::new();
        let mut found = false;

        // Remove the timer from the heap
        while let Some(Reverse(entry)) = queue.pop() {
            if entry.id != timer_id {
                temp_heap.push(Reverse(entry));
            } else {
                found = true;
            }
        }

        // Restore the heap
        *queue = temp_heap;

        if found {
            self.metrics.timers_cancelled.fetch_add(1, AtomicOrdering::Relaxed);
            Ok(())
        } else {
            Err(AsyncError::TimerError("Timer not found".to_string()))
        }
    }

    /// Get the next timer wakeup
    pub fn get_next_wakeup(&self) -> Option<TimerWakeup> {
        self.waker_receiver.try_recv().ok()
    }

    /// Wait for the next timer wakeup (blocking)
    pub fn wait_for_wakeup(&self) -> Result<TimerWakeup, AsyncError> {
        self.waker_receiver.recv()
            .map_err(|_| AsyncError::TimerError("Timer wakeup channel closed".to_string()))
    }

    /// Get timer statistics
    pub fn stats(&self) -> TimerStats {
        let queue_size = self.timer_queue.lock().unwrap().len();
        
        TimerStats {
            active_timers: queue_size,
            timers_scheduled: self.metrics.timers_scheduled.load(AtomicOrdering::Relaxed),
            timers_fired: self.metrics.timers_fired.load(AtomicOrdering::Relaxed),
            timers_cancelled: self.metrics.timers_cancelled.load(AtomicOrdering::Relaxed),
            current_resolution_ns: self.resolution.load(AtomicOrdering::Relaxed),
            drift_compensation: self.drift_compensator.stats(),
        }
    }

    /// Adjust timer resolution for better performance or accuracy
    pub fn set_resolution(&self, resolution: Duration) {
        self.resolution.store(resolution.as_nanos() as u64, AtomicOrdering::Relaxed);
    }

    /// Get the next timer deadline
    pub fn next_deadline(&self) -> Option<Instant> {
        let queue = self.timer_queue.lock().unwrap();
        queue.peek().map(|Reverse(entry)| entry.deadline)
    }

    /// Sleep until a specific instant with drift compensation
    pub fn sleep_until(&self, deadline: Instant) -> TimerFuture {
        let waker_id = WakerId::new();
        let delay = deadline.saturating_duration_since(Instant::now());
        
        // Schedule the timer
        let timer_id = self.schedule_once(delay, waker_id).unwrap_or(TimerId::new());
        
        TimerFuture::new(timer_id, waker_id, deadline, self.waker_receiver.clone())
    }

    /// Sleep for a specific duration
    pub fn sleep(&self, duration: Duration) -> TimerFuture {
        let deadline = Instant::now() + duration;
        self.sleep_until(deadline)
    }
}

/// Timer entry in the priority queue
#[derive(Debug, Clone)]
struct TimerEntry {
    id: TimerId,
    deadline: Instant,
    waker_id: WakerId,
    interval: Option<Duration>,
    metadata: TimerMetadata,
}

impl PartialEq for TimerEntry {
    fn eq(&self, other: &Self) -> bool {
        self.deadline == other.deadline
    }
}

impl Eq for TimerEntry {}

impl PartialOrd for TimerEntry {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for TimerEntry {
    fn cmp(&self, other: &Self) -> Ordering {
        self.deadline.cmp(&other.deadline)
    }
}

/// Timer wakeup notification
#[derive(Debug, Clone)]
pub struct TimerWakeup {
    pub timer_id: TimerId,
    pub waker_id: WakerId,
    pub execution_time: Instant,
    pub scheduled_time: Instant,
}

impl TimerWakeup {
    /// Get the drift (difference between scheduled and actual execution time)
    pub fn drift(&self) -> Duration {
        if self.execution_time > self.scheduled_time {
            self.execution_time.duration_since(self.scheduled_time)
        } else {
            Duration::from_nanos(0)
        }
    }
}

/// Timer metadata for debugging and monitoring
#[derive(Debug, Clone)]
pub struct TimerMetadata {
    pub name: Option<String>,
    pub tags: Vec<String>,
    pub priority: TimerPriority,
    pub created_at: SystemTime,
}

impl Default for TimerMetadata {
    fn default() -> Self {
        Self {
            name: None,
            tags: Vec::new(),
            priority: TimerPriority::Normal,
            created_at: SystemTime::now(),
        }
    }
}

/// Timer priority for scheduling
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum TimerPriority {
    Low = 0,
    Normal = 1,
    High = 2,
    Critical = 3,
}

/// Timer system configuration
#[derive(Debug, Clone)]
pub struct TimerConfig {
    pub resolution: Duration,
    pub max_timers: usize,
    pub enable_drift_compensation: bool,
    pub enable_high_precision: bool,
}

impl Default for TimerConfig {
    fn default() -> Self {
        Self {
            resolution: Duration::from_millis(1),
            max_timers: 10_000,
            enable_drift_compensation: true,
            enable_high_precision: false,
        }
    }
}

/// Timer performance metrics
#[derive(Debug)]
struct TimerMetrics {
    timers_scheduled: AtomicUsize,
    timers_fired: AtomicUsize,
    timers_cancelled: AtomicUsize,
}

impl TimerMetrics {
    fn new() -> Self {
        Self {
            timers_scheduled: AtomicUsize::new(0),
            timers_fired: AtomicUsize::new(0),
            timers_cancelled: AtomicUsize::new(0),
        }
    }
}

/// Timer statistics
#[derive(Debug, Clone)]
pub struct TimerStats {
    pub active_timers: usize,
    pub timers_scheduled: usize,
    pub timers_fired: usize,
    pub timers_cancelled: usize,
    pub current_resolution_ns: u64,
    pub drift_compensation: DriftStats,
}

/// Drift compensation system
#[derive(Debug)]
struct DriftCompensator {
    accumulated_drift: Mutex<Duration>,
    drift_history: Mutex<std::collections::VecDeque<Duration>>,
    adjustment_factor: RwLock<f64>,
    stats: Mutex<DriftStats>,
}

impl DriftCompensator {
    fn new() -> Self {
        Self {
            accumulated_drift: Mutex::new(Duration::from_nanos(0)),
            drift_history: Mutex::new(std::collections::VecDeque::with_capacity(1000)),
            adjustment_factor: RwLock::new(1.0),
            stats: Mutex::new(DriftStats::default()),
        }
    }

    fn record_timing(&self, actual: Duration, expected: Duration) {
        let drift = if actual > expected {
            actual - expected
        } else {
            Duration::from_nanos(0)
        };

        {
            let mut accumulated = self.accumulated_drift.lock().unwrap();
            *accumulated += drift;
        }

        {
            let mut history = self.drift_history.lock().unwrap();
            history.push_back(drift);
            if history.len() > 1000 {
                history.pop_front();
            }
        }

        // Update statistics
        {
            let mut stats = self.stats.lock().unwrap();
            stats.total_measurements += 1;
            stats.total_drift += drift;
            if drift > stats.max_drift {
                stats.max_drift = drift;
            }
            stats.average_drift = stats.total_drift / stats.total_measurements as u32;
        }

        // Adjust compensation factor periodically
        if self.stats.lock().unwrap().total_measurements % 100 == 0 {
            self.update_adjustment_factor();
        }
    }

    fn update_adjustment_factor(&self) {
        let history = self.drift_history.lock().unwrap();
        if history.len() < 10 {
            return;
        }

        let recent_drift: Duration = history.iter().rev().take(10).sum();
        let average_recent = recent_drift / 10;

        let adjustment = if average_recent > Duration::from_micros(100) {
            0.95 // Compensate for consistently high drift
        } else if average_recent < Duration::from_micros(10) {
            1.05 // Less aggressive compensation
        } else {
            1.0 // No change
        };

        *self.adjustment_factor.write().unwrap() = adjustment;
    }

    fn get_compensated_sleep(&self, target: Duration) -> Duration {
        let factor = *self.adjustment_factor.read().unwrap();
        let compensated_nanos = (target.as_nanos() as f64 * factor) as u64;
        Duration::from_nanos(compensated_nanos.max(0))
    }

    fn stats(&self) -> DriftStats {
        self.stats.lock().unwrap().clone()
    }
}

/// Drift compensation statistics
#[derive(Debug, Clone)]
pub struct DriftStats {
    pub total_measurements: usize,
    pub total_drift: Duration,
    pub average_drift: Duration,
    pub max_drift: Duration,
}

impl Default for DriftStats {
    fn default() -> Self {
        Self {
            total_measurements: 0,
            total_drift: Duration::from_nanos(0),
            average_drift: Duration::from_nanos(0),
            max_drift: Duration::from_nanos(0),
        }
    }
}

/// Future for timer-based delays
pub struct TimerFuture {
    timer_id: TimerId,
    waker_id: WakerId,
    deadline: Instant,
    receiver: Receiver<TimerWakeup>,
    completed: bool,
}

impl TimerFuture {
    fn new(timer_id: TimerId, waker_id: WakerId, deadline: Instant, receiver: Receiver<TimerWakeup>) -> Self {
        Self {
            timer_id,
            waker_id,
            deadline,
            receiver,
            completed: false,
        }
    }
}

impl std::future::Future for TimerFuture {
    type Output = Result<(), AsyncError>;

    fn poll(mut self: std::pin::Pin<&mut Self>, cx: &mut std::task::Context<'_>) -> std::task::Poll<Self::Output> {
        if self.completed {
            return std::task::Poll::Ready(Ok(()));
        }

        // Check if we've reached the deadline
        if Instant::now() >= self.deadline {
            self.completed = true;
            return std::task::Poll::Ready(Ok(()));
        }

        // Check for timer wakeup
        while let Ok(wakeup) = self.receiver.try_recv() {
            if wakeup.timer_id == self.timer_id && wakeup.waker_id == self.waker_id {
                self.completed = true;
                return std::task::Poll::Ready(Ok(()));
            }
        }

        // Wake us when the timer fires
        cx.waker().wake_by_ref();
        std::task::Poll::Pending
    }
}

/// High-precision timer using platform-specific features
#[cfg(target_os = "linux")]
mod high_precision {
    use super::*;
    
    pub struct HighPrecisionTimer {
        timer_fd: i32,
    }
    
    impl HighPrecisionTimer {
        pub fn new() -> Result<Self, AsyncError> {
            // Use timerfd_create for high precision timing on Linux
            let timer_fd = unsafe {
                libc::timerfd_create(libc::CLOCK_MONOTONIC, libc::TFD_NONBLOCK | libc::TFD_CLOEXEC)
            };
            
            if timer_fd == -1 {
                return Err(AsyncError::TimerError("Failed to create timer fd".to_string()));
            }
            
            Ok(Self { timer_fd })
        }
        
        pub fn set_timer(&self, duration: Duration) -> Result<(), AsyncError> {
            let spec = libc::itimerspec {
                it_interval: libc::timespec { tv_sec: 0, tv_nsec: 0 },
                it_value: libc::timespec {
                    tv_sec: duration.as_secs() as i64,
                    tv_nsec: duration.subsec_nanos() as i64,
                },
            };
            
            let result = unsafe {
                libc::timerfd_settime(self.timer_fd, 0, &spec, std::ptr::null_mut())
            };
            
            if result == -1 {
                Err(AsyncError::TimerError("Failed to set timer".to_string()))
            } else {
                Ok(())
            }
        }
    }
    
    impl Drop for HighPrecisionTimer {
        fn drop(&mut self) {
            unsafe {
                libc::close(self.timer_fd);
            }
        }
    }
}

#[cfg(target_os = "windows")]
mod high_precision {
    use super::*;
    
    pub struct HighPrecisionTimer {
        handle: *mut std::ffi::c_void,
    }
    
    impl HighPrecisionTimer {
        pub fn new() -> Result<Self, AsyncError> {
            let handle = unsafe {
                winapi::um::synchapi::CreateWaitableTimerW(std::ptr::null_mut(), winapi::shared::minwindef::FALSE, std::ptr::null())
            };
            
            if handle.is_null() {
                return Err(AsyncError::TimerError("Failed to create Windows waitable timer".to_string()));
            }
            
            Ok(Self { handle: handle as *mut std::ffi::c_void })
        }
        
        pub fn set_timer(&self, duration: Duration) -> Result<(), AsyncError> {
            let nanoseconds = duration.as_nanos() as i64;
            let filetime_intervals = nanoseconds / 100;
            let due_time = -filetime_intervals;
            
            let result = unsafe {
                winapi::um::synchapi::SetWaitableTimer(
                    self.handle as winapi::um::winnt::HANDLE,
                    &due_time as *const i64 as *const winapi::shared::minwindef::LARGE_INTEGER,
                    0,
                    None,
                    std::ptr::null_mut(),
                    winapi::shared::minwindef::FALSE,
                )
            };
            
            if result == 0 {
                Err(AsyncError::TimerError("Failed to set Windows waitable timer".to_string()))
            } else {
                Ok(())
            }
        }
    }
}

#[cfg(target_os = "macos")]
mod high_precision {
    use super::*;
    use std::sync::{Arc, Mutex};
    use std::thread;
    use std::time::Instant;
    
    extern "C" {
        fn mach_timebase_info(info: *mut mach_timebase_info_data_t) -> i32;
        fn mach_absolute_time() -> u64;
    }
    
    #[repr(C)]
    struct mach_timebase_info_data_t {
        numer: u32,
        denom: u32,
    }
    
    pub struct HighPrecisionTimer {
        timebase: mach_timebase_info_data_t,
        start_time: Arc<Mutex<Option<Instant>>>,
        target_duration: Arc<Mutex<Option<Duration>>>,
    }
    
    impl HighPrecisionTimer {
        pub fn new() -> Result<Self, AsyncError> {
            let mut timebase = mach_timebase_info_data_t { numer: 0, denom: 0 };
            
            let result = unsafe { mach_timebase_info(&mut timebase) };
            if result != 0 {
                return Err(AsyncError::TimerError("Failed to get Mach timebase info".to_string()));
            }
            
            Ok(Self {
                timebase,
                start_time: Arc::new(Mutex::new(None)),
                target_duration: Arc::new(Mutex::new(None)),
            })
        }
        
        pub fn set_timer(&self, duration: Duration) -> Result<(), AsyncError> {
            let now = Instant::now();
            
            if let (Ok(mut start), Ok(mut target)) = (self.start_time.lock(), self.target_duration.lock()) {
                *start = Some(now);
                *target = Some(duration);
            }
            
            Ok(())
        }
        
        pub fn get_precise_time_ns(&self) -> u64 {
            let mach_time = unsafe { mach_absolute_time() };
            
            // Convert mach time to nanoseconds using timebase
            (mach_time * self.timebase.numer as u64) / self.timebase.denom as u64
        }
        
        pub fn wait_until_elapsed(&self) -> Result<bool, AsyncError> {
            if let (Ok(start_guard), Ok(target_guard)) = (self.start_time.lock(), self.target_duration.lock()) {
                if let (Some(start_time), Some(target_duration)) = (*start_guard, *target_guard) {
                    let elapsed = start_time.elapsed();
                    if elapsed >= target_duration {
                        return Ok(true);
                    }
                    
                    // Use high-precision Mach timing for remaining wait
                    let remaining = target_duration - elapsed;
                    let start_mach_time = self.get_precise_time_ns();
                    let target_ns = remaining.as_nanos() as u64;
                    
                    while (self.get_precise_time_ns() - start_mach_time) < target_ns {
                        thread::yield_now();
                    }
                    
                    return Ok(true);
                }
            }
            
            Ok(false)
        }
    }
}

/// Timer wheel implementation for very high throughput scenarios
pub struct TimerWheel {
    wheels: Vec<Vec<Vec<TimerEntry>>>,
    current_tick: AtomicUsize,
    tick_duration: Duration,
    running: AtomicBool,
}

impl TimerWheel {
    const WHEEL_SIZES: &'static [usize] = &[256, 64, 64, 64]; // 4 levels
    
    pub fn new(tick_duration: Duration) -> Self {
        let wheels = Self::WHEEL_SIZES.iter()
            .map(|&size| vec![Vec::new(); size])
            .collect();
        
        Self {
            wheels,
            current_tick: AtomicUsize::new(0),
            tick_duration,
            running: AtomicBool::new(false),
        }
    }
    
    /// Add timer to appropriate wheel level
    pub fn add_timer(&mut self, delay: Duration, timer: TimerEntry) {
        let ticks = (delay.as_nanos() / self.tick_duration.as_nanos()) as usize;
        let level = self.calculate_wheel_level(ticks);
        let slot = self.calculate_slot(ticks, level);
        
        self.wheels[level][slot].push(timer);
    }
    
    fn calculate_wheel_level(&self, ticks: usize) -> usize {
        if ticks < Self::WHEEL_SIZES[0] {
            0
        } else if ticks < Self::WHEEL_SIZES[0] * Self::WHEEL_SIZES[1] {
            1
        } else if ticks < Self::WHEEL_SIZES[0] * Self::WHEEL_SIZES[1] * Self::WHEEL_SIZES[2] {
            2
        } else {
            3
        }
    }
    
    fn calculate_slot(&self, ticks: usize, level: usize) -> usize {
        match level {
            0 => ticks % Self::WHEEL_SIZES[0],
            1 => (ticks / Self::WHEEL_SIZES[0]) % Self::WHEEL_SIZES[1],
            2 => (ticks / (Self::WHEEL_SIZES[0] * Self::WHEEL_SIZES[1])) % Self::WHEEL_SIZES[2],
            _ => (ticks / (Self::WHEEL_SIZES[0] * Self::WHEEL_SIZES[1] * Self::WHEEL_SIZES[2])) % Self::WHEEL_SIZES[3],
        }
    }
    
    /// Advance timer wheel and return expired timers
    pub fn tick(&mut self) -> Vec<TimerEntry> {
        let current = self.current_tick.fetch_add(1, AtomicOrdering::Relaxed);
        let slot = current % Self::WHEEL_SIZES[0];
        
        // Collect expired timers from current slot
        let mut expired = std::mem::take(&mut self.wheels[0][slot]);
        
        // Handle overflow to higher level wheels
        if slot == 0 && current > 0 {
            self.cascade_wheel(1, current / Self::WHEEL_SIZES[0]);
        }
        
        expired
    }
    
    fn cascade_wheel(&mut self, level: usize, tick: usize) {
        if level >= self.wheels.len() {
            return;
        }
        
        let slot = tick % Self::WHEEL_SIZES[level];
        let timers = std::mem::take(&mut self.wheels[level][slot]);
        
        // Redistribute timers to lower levels
        for timer in timers {
            let remaining_ticks = timer.deadline.saturating_duration_since(Instant::now()).as_nanos() / self.tick_duration.as_nanos();
            let new_level = self.calculate_wheel_level(remaining_ticks as usize);
            let new_slot = self.calculate_slot(remaining_ticks as usize, new_level);
            self.wheels[new_level][new_slot].push(timer);
        }
        
        // Continue cascading if needed
        if slot == 0 && level < self.wheels.len() - 1 {
            self.cascade_wheel(level + 1, tick / Self::WHEEL_SIZES[level]);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_timer_creation() {
        let config = TimerConfig::default();
        let timer_system = TimerSystem::new(config).unwrap();
        assert!(!timer_system.running.load(AtomicOrdering::Relaxed));
    }
    
    #[test]
    fn test_timer_scheduling() {
        let config = TimerConfig::default();
        let timer_system = TimerSystem::new(config).unwrap();
        timer_system.start().unwrap();
        
        let waker_id = WakerId::new();
        let timer_id = timer_system.schedule_once(Duration::from_millis(10), waker_id).unwrap();
        
        let stats = timer_system.stats();
        assert_eq!(stats.timers_scheduled, 1);
        assert_eq!(stats.active_timers, 1);
        
        timer_system.stop().unwrap();
    }
    
    #[test]
    fn test_timer_cancellation() {
        let config = TimerConfig::default();
        let timer_system = TimerSystem::new(config).unwrap();
        timer_system.start().unwrap();
        
        let waker_id = WakerId::new();
        let timer_id = timer_system.schedule_once(Duration::from_secs(10), waker_id).unwrap();
        
        assert!(timer_system.cancel_timer(timer_id).is_ok());
        
        let stats = timer_system.stats();
        assert_eq!(stats.timers_cancelled, 1);
        
        timer_system.stop().unwrap();
    }
    
    #[test]
    fn test_timer_wheel() {
        let mut wheel = TimerWheel::new(Duration::from_millis(1));
        
        let timer = TimerEntry {
            id: TimerId::new(),
            deadline: Instant::now() + Duration::from_millis(10),
            waker_id: WakerId::new(),
            interval: None,
            metadata: TimerMetadata::default(),
        };
        
        wheel.add_timer(Duration::from_millis(10), timer);
        
        // Advance time and check for expired timers
        for _ in 0..15 {
            let expired = wheel.tick();
            if !expired.is_empty() {
                assert_eq!(expired.len(), 1);
                break;
            }
        }
    }
    
    #[test]
    fn test_drift_compensation() {
        let compensator = DriftCompensator::new();
        
        // Test actual timing measurements with real sleep
        for _ in 0..5 {
            let target = Duration::from_millis(10);
            let start = std::time::Instant::now();
            std::thread::sleep(target);
            let actual = start.elapsed();
            
            compensator.record_timing(actual, target);
        }
        
        let stats = compensator.stats();
        assert!(stats.total_measurements > 0);
        
        // Test compensation actually works
        let target_sleep = Duration::from_millis(10);
        let compensated = compensator.get_compensated_sleep(target_sleep);
        
        // Compensated sleep should be adjusted based on measured drift
        assert!(compensated != target_sleep || stats.average_drift == Duration::ZERO);
    }
}