// Adaptive Concurrency System for Optimal Thread Pool Management
// AI-driven automatic thread count tuning based on workload patterns

use std::sync::{Arc, Mutex, RwLock};
use std::sync::atomic::{AtomicUsize, AtomicU32, AtomicBool, Ordering};
use std::collections::{HashMap, VecDeque};
use std::time::{Duration, Instant};
use std::thread;

use super::{AsyncError, TaskId, TaskPriority};

/// Adaptive concurrency controller that optimizes thread pool size
#[derive(Debug)]
pub struct AdaptiveConcurrencyController {
    config: ConcurrencyConfig,
    current_thread_count: AtomicUsize,
    target_thread_count: AtomicUsize,
    workload_analyzer: Arc<WorkloadAnalyzer>,
    performance_monitor: Arc<PerformanceMonitor>,
    thread_manager: Arc<Mutex<ThreadManager>>,
    tuning_algorithm: Arc<Mutex<TuningAlgorithm>>,
    running: AtomicBool,
    control_thread: Mutex<Option<thread::JoinHandle<()>>>,
}

impl AdaptiveConcurrencyController {
    /// Create new adaptive concurrency controller
    pub fn new(initial_thread_count: usize) -> Result<Self, AsyncError> {
        let config = ConcurrencyConfig::new(initial_thread_count);
        let workload_analyzer = Arc::new(WorkloadAnalyzer::new());
        let performance_monitor = Arc::new(PerformanceMonitor::new());
        let thread_manager = Arc::new(Mutex::new(ThreadManager::new()));
        let tuning_algorithm = Arc::new(Mutex::new(TuningAlgorithm::new()));

        Ok(Self {
            config: config.clone(),
            current_thread_count: AtomicUsize::new(initial_thread_count),
            target_thread_count: AtomicUsize::new(initial_thread_count),
            workload_analyzer,
            performance_monitor,
            thread_manager,
            tuning_algorithm,
            running: AtomicBool::new(false),
            control_thread: Mutex::new(None),
        })
    }

    /// Start the adaptive concurrency system
    pub fn start(&self) -> Result<(), AsyncError> {
        if self.running.load(Ordering::Acquire) {
            return Err(AsyncError::AlreadyRunning);
        }

        self.running.store(true, Ordering::Release);

        // Start monitoring and tuning thread
        let workload_analyzer = self.workload_analyzer.clone();
        let performance_monitor = self.performance_monitor.clone();
        let thread_manager = self.thread_manager.clone();
        let tuning_algorithm = self.tuning_algorithm.clone();
        let current_count = self.current_thread_count.clone();
        let target_count = self.target_thread_count.clone();
        let config = self.config.clone();
        let running = self.running.clone();

        let handle = thread::Builder::new()
            .name("runa-adaptive-concurrency".to_string())
            .spawn(move || {
                Self::control_loop(
                    workload_analyzer,
                    performance_monitor,
                    thread_manager,
                    tuning_algorithm,
                    current_count,
                    target_count,
                    config,
                    running,
                );
            })
            .map_err(|e| AsyncError::ThreadError(e.to_string()))?;

        if let Ok(mut thread_guard) = self.control_thread.lock() {
            *thread_guard = Some(handle);
        }

        Ok(())
    }

    /// Stop the adaptive concurrency system
    pub fn stop(&self) -> Result<(), AsyncError> {
        self.running.store(false, Ordering::Release);

        if let Ok(mut thread_guard) = self.control_thread.lock() {
            if let Some(handle) = thread_guard.take() {
                handle.join().map_err(|_| AsyncError::ThreadError("Failed to join control thread".to_string()))?;
            }
        }

        Ok(())
    }

    /// Report task submission for workload analysis
    pub fn report_task_submitted(&self, task_id: TaskId, priority: TaskPriority, estimated_duration: Duration) {
        self.workload_analyzer.record_task_submission(task_id, priority, estimated_duration);
    }

    /// Report task completion for performance monitoring
    pub fn report_task_completed(&self, task_id: TaskId, actual_duration: Duration, worker_id: usize) {
        self.workload_analyzer.record_task_completion(task_id, actual_duration, worker_id);
        self.performance_monitor.record_task_completion(actual_duration, worker_id);
    }

    /// Report worker thread utilization
    pub fn report_worker_utilization(&self, worker_id: usize, utilization: f32) {
        self.performance_monitor.record_worker_utilization(worker_id, utilization);
    }

    /// Get current optimal thread count
    pub fn current_thread_count(&self) -> usize {
        self.current_thread_count.load(Ordering::Relaxed)
    }

    /// Get target thread count (what system is trying to achieve)
    pub fn target_thread_count(&self) -> usize {
        self.target_thread_count.load(Ordering::Relaxed)
    }

    /// Get system performance metrics
    pub fn performance_metrics(&self) -> ConcurrencyMetrics {
        self.performance_monitor.get_metrics()
    }

    /// Force thread count adjustment (for testing or manual control)
    pub fn set_thread_count(&self, count: usize) -> Result<(), AsyncError> {
        let clamped_count = count.max(self.config.min_threads).min(self.config.max_threads);
        self.target_thread_count.store(clamped_count, Ordering::Release);
        Ok(())
    }

    fn control_loop(
        workload_analyzer: Arc<WorkloadAnalyzer>,
        performance_monitor: Arc<PerformanceMonitor>,
        thread_manager: Arc<Mutex<ThreadManager>>,
        tuning_algorithm: Arc<Mutex<TuningAlgorithm>>,
        current_count: Arc<AtomicUsize>,
        target_count: Arc<AtomicUsize>,
        config: ConcurrencyConfig,
        running: Arc<AtomicBool>,
    ) {
        let mut last_adjustment = Instant::now();
        let mut adjustment_cycle = 0;

        while running.load(Ordering::Acquire) {
            let cycle_start = Instant::now();

            // Analyze current workload and performance
            let workload_analysis = workload_analyzer.analyze_current_workload();
            let performance_analysis = performance_monitor.analyze_performance();

            // Determine optimal thread count using AI tuning algorithm
            if let Ok(mut tuning) = tuning_algorithm.lock() {
                let current_threads = current_count.load(Ordering::Relaxed);
                let recommendation = tuning.calculate_optimal_thread_count(
                    current_threads,
                    &workload_analysis,
                    &performance_analysis,
                );

                // Apply recommendation if significant change is needed
                if last_adjustment.elapsed() >= config.min_adjustment_interval {
                    let difference = if recommendation > current_threads {
                        recommendation - current_threads
                    } else {
                        current_threads - recommendation
                    };

                    // Only adjust if change is significant enough
                    if difference >= config.min_adjustment_threshold {
                        target_count.store(recommendation, Ordering::Release);
                        
                        // Gradually adjust thread count
                        if let Ok(mut manager) = thread_manager.lock() {
                            let adjusted_count = manager.adjust_thread_count(
                                current_threads,
                                recommendation,
                                &config,
                            );
                            current_count.store(adjusted_count, Ordering::Release);
                            last_adjustment = Instant::now();
                        }
                    }
                }

                // Update tuning algorithm with latest performance data
                tuning.update_performance_feedback(&performance_analysis);
            }

            adjustment_cycle += 1;

            // Periodic deep analysis and model retraining
            if adjustment_cycle % 100 == 0 {
                workload_analyzer.perform_deep_analysis();
                if let Ok(mut tuning) = tuning_algorithm.lock() {
                    tuning.retrain_model(&workload_analyzer.get_historical_data());
                }
            }

            // Sleep until next control cycle
            let cycle_duration = cycle_start.elapsed();
            if cycle_duration < config.control_interval {
                thread::sleep(config.control_interval - cycle_duration);
            }
        }
    }
}

/// Configuration for adaptive concurrency system
#[derive(Debug, Clone)]
pub struct ConcurrencyConfig {
    pub min_threads: usize,
    pub max_threads: usize,
    pub control_interval: Duration,
    pub min_adjustment_interval: Duration,
    pub min_adjustment_threshold: usize,
    pub target_cpu_utilization: f32,
    pub responsiveness_weight: f32,
    pub throughput_weight: f32,
}

impl ConcurrencyConfig {
    pub fn new(initial_thread_count: usize) -> Self {
        let cpu_count = num_cpus::get();
        
        Self {
            min_threads: 1,
            max_threads: (cpu_count * 4).max(8), // Allow up to 4x CPU cores
            control_interval: Duration::from_millis(500),
            min_adjustment_interval: Duration::from_secs(2),
            min_adjustment_threshold: 1,
            target_cpu_utilization: 0.8, // Target 80% CPU utilization
            responsiveness_weight: 0.6,  // 60% weight on responsiveness
            throughput_weight: 0.4,      // 40% weight on throughput
        }
    }
}

/// Workload analyzer for understanding task patterns
#[derive(Debug)]
pub struct WorkloadAnalyzer {
    recent_submissions: RwLock<VecDeque<TaskSubmission>>,
    recent_completions: RwLock<VecDeque<TaskCompletion>>,
    task_patterns: RwLock<HashMap<TaskPattern, usize>>,
    historical_data: RwLock<Vec<WorkloadSnapshot>>,
    current_queue_length: AtomicUsize,
    average_task_duration: AtomicU32, // Store as milliseconds in u32
}

impl WorkloadAnalyzer {
    pub fn new() -> Self {
        Self {
            recent_submissions: RwLock::new(VecDeque::new()),
            recent_completions: RwLock::new(VecDeque::new()),
            task_patterns: RwLock::new(HashMap::new()),
            historical_data: RwLock::new(Vec::new()),
            current_queue_length: AtomicUsize::new(0),
            average_task_duration: AtomicU32::new(100), // 100ms default
        }
    }

    pub fn record_task_submission(&self, task_id: TaskId, priority: TaskPriority, estimated_duration: Duration) {
        let submission = TaskSubmission {
            task_id,
            priority,
            estimated_duration,
            submitted_at: Instant::now(),
        };

        // Add to recent submissions
        if let Ok(mut submissions) = self.recent_submissions.write() {
            submissions.push_back(submission.clone());
            
            // Keep only last 1000 submissions
            while submissions.len() > 1000 {
                submissions.pop_front();
            }
        }

        // Update queue length
        self.current_queue_length.fetch_add(1, Ordering::Relaxed);

        // Update task patterns
        let pattern = TaskPattern::from_submission(&submission);
        if let Ok(mut patterns) = self.task_patterns.write() {
            *patterns.entry(pattern).or_insert(0) += 1;
        }
    }

    pub fn record_task_completion(&self, task_id: TaskId, actual_duration: Duration, worker_id: usize) {
        let completion = TaskCompletion {
            task_id,
            actual_duration,
            completed_at: Instant::now(),
            worker_id,
        };

        // Add to recent completions
        if let Ok(mut completions) = self.recent_completions.write() {
            completions.push_back(completion);
            
            // Keep only last 1000 completions
            while completions.len() > 1000 {
                completions.pop_front();
            }
        }

        // Update queue length
        self.current_queue_length.fetch_sub(1, Ordering::Relaxed);

        // Update average task duration
        let duration_ms = actual_duration.as_millis() as u32;
        let current_avg = self.average_task_duration.load(Ordering::Relaxed);
        let new_avg = (current_avg * 9 + duration_ms) / 10; // Exponential moving average
        self.average_task_duration.store(new_avg, Ordering::Relaxed);
    }

    pub fn analyze_current_workload(&self) -> WorkloadAnalysis {
        let queue_length = self.current_queue_length.load(Ordering::Relaxed);
        let avg_duration = Duration::from_millis(self.average_task_duration.load(Ordering::Relaxed) as u64);

        // Calculate submission rate (tasks per second)
        let submission_rate = if let Ok(submissions) = self.recent_submissions.read() {
            if submissions.len() < 2 {
                0.0
            } else {
                let time_span = submissions.back().unwrap().submitted_at - submissions.front().unwrap().submitted_at;
                if time_span.as_secs_f64() > 0.0 {
                    submissions.len() as f64 / time_span.as_secs_f64()
                } else {
                    0.0
                }
            }
        } else {
            0.0
        };

        // Calculate completion rate
        let completion_rate = if let Ok(completions) = self.recent_completions.read() {
            if completions.len() < 2 {
                0.0
            } else {
                let time_span = completions.back().unwrap().completed_at - completions.front().unwrap().completed_at;
                if time_span.as_secs_f64() > 0.0 {
                    completions.len() as f64 / time_span.as_secs_f64()
                } else {
                    0.0
                }
            }
        } else {
            0.0
        };

        // Determine workload characteristics
        let workload_type = self.classify_workload_type(submission_rate, avg_duration);
        let intensity = self.calculate_workload_intensity(queue_length, submission_rate, completion_rate);

        WorkloadAnalysis {
            queue_length,
            submission_rate,
            completion_rate,
            average_task_duration: avg_duration,
            workload_type,
            intensity,
            cpu_bound_ratio: self.estimate_cpu_bound_ratio(),
            io_bound_ratio: self.estimate_io_bound_ratio(),
        }
    }

    pub fn perform_deep_analysis(&self) {
        // Create workload snapshot for historical analysis
        let snapshot = WorkloadSnapshot {
            timestamp: Instant::now(),
            analysis: self.analyze_current_workload(),
        };

        if let Ok(mut historical) = self.historical_data.write() {
            historical.push(snapshot);
            
            // Keep only last 1000 snapshots (about 8 hours at 30-second intervals)
            while historical.len() > 1000 {
                historical.remove(0);
            }
        }
    }

    pub fn get_historical_data(&self) -> Vec<WorkloadSnapshot> {
        self.historical_data.read().unwrap_or_else(|_| {
            std::sync::RwLockReadGuard::leak(
                std::sync::RwLock::new(Vec::new()).read().unwrap()
            )
        }).clone()
    }

    fn classify_workload_type(&self, submission_rate: f64, avg_duration: Duration) -> WorkloadType {
        if submission_rate > 100.0 {
            WorkloadType::HighThroughput
        } else if avg_duration > Duration::from_millis(1000) {
            WorkloadType::LongRunning
        } else if submission_rate > 10.0 && avg_duration < Duration::from_millis(100) {
            WorkloadType::Burst
        } else {
            WorkloadType::Steady
        }
    }

    fn calculate_workload_intensity(&self, queue_length: usize, submission_rate: f64, completion_rate: f64) -> f32 {
        let queue_factor = (queue_length as f32 / 100.0).min(1.0); // Normalize to 0-1
        let rate_factor = if completion_rate > 0.0 {
            (submission_rate / completion_rate).min(2.0) as f32 / 2.0 // Normalize to 0-1
        } else {
            1.0
        };

        (queue_factor * 0.7 + rate_factor * 0.3).min(1.0)
    }

    fn estimate_cpu_bound_ratio(&self) -> f32 {
        // Estimate based on task duration patterns
        if let Ok(patterns) = self.task_patterns.read() {
            let total_patterns: usize = patterns.values().sum();
            if total_patterns > 0 {
                let cpu_intensive_count: usize = patterns.iter()
                    .filter(|(pattern, _)| pattern.is_cpu_intensive())
                    .map(|(_, count)| count)
                    .sum();
                cpu_intensive_count as f32 / total_patterns as f32
            } else {
                0.5 // Default assumption
            }
        } else {
            0.5
        }
    }

    fn estimate_io_bound_ratio(&self) -> f32 {
        // Analyze task patterns for I/O characteristics
        if let Ok(patterns) = self.task_patterns.read() {
            let total_patterns: usize = patterns.values().sum();
            if total_patterns > 0 {
                let io_intensive_count: usize = patterns.iter()
                    .filter(|(pattern, _)| pattern.is_io_intensive())
                    .map(|(_, count)| count)
                    .sum();
                
                // Base I/O ratio from patterns
                let pattern_io_ratio = io_intensive_count as f32 / total_patterns as f32;
                
                // Adjust based on recent completion times vs submission times
                let timing_adjustment = if let (Ok(submissions), Ok(completions)) = 
                    (self.recent_submissions.read(), self.recent_completions.read()) {
                    
                    if submissions.len() > 10 && completions.len() > 10 {
                        // Calculate average wait time (suggests I/O blocking)
                        let avg_submission_interval = self.calculate_avg_submission_interval(&submissions);
                        let avg_completion_time = self.calculate_avg_completion_time(&completions);
                        
                        // High completion time relative to submission suggests I/O bound
                        if avg_completion_time > avg_submission_interval * 2.0 {
                            0.3 // Boost I/O ratio
                        } else {
                            0.0 // No adjustment
                        }
                    } else {
                        0.0
                    }
                } else {
                    0.0
                };
                
                (pattern_io_ratio + timing_adjustment).min(1.0)
            } else {
                0.3 // Conservative default for I/O workloads
            }
        } else {
            0.3
        }
    }
    
    fn calculate_avg_submission_interval(&self, submissions: &std::collections::VecDeque<TaskSubmission>) -> f32 {
        if submissions.len() < 2 {
            return 100.0; // Default 100ms
        }
        
        let total_time = submissions.back().unwrap().submitted_at - submissions.front().unwrap().submitted_at;
        total_time.as_millis() as f32 / (submissions.len() - 1) as f32
    }
    
    fn calculate_avg_completion_time(&self, completions: &std::collections::VecDeque<TaskCompletion>) -> f32 {
        if completions.is_empty() {
            return 100.0; // Default 100ms
        }
        
        let total_duration: u128 = completions.iter()
            .map(|c| c.actual_duration.as_millis())
            .sum();
        
        total_duration as f32 / completions.len() as f32
    }
}

/// Performance monitor for system efficiency tracking
#[derive(Debug)]
pub struct PerformanceMonitor {
    worker_utilizations: RwLock<HashMap<usize, Vec<f32>>>,
    recent_task_durations: RwLock<VecDeque<Duration>>,
    system_metrics: RwLock<SystemMetrics>,
    performance_history: RwLock<Vec<PerformanceSnapshot>>,
}

impl PerformanceMonitor {
    pub fn new() -> Self {
        Self {
            worker_utilizations: RwLock::new(HashMap::new()),
            recent_task_durations: RwLock::new(VecDeque::new()),
            system_metrics: RwLock::new(SystemMetrics::new()),
            performance_history: RwLock::new(Vec::new()),
        }
    }

    pub fn record_worker_utilization(&self, worker_id: usize, utilization: f32) {
        if let Ok(mut utils) = self.worker_utilizations.write() {
            let worker_utils = utils.entry(worker_id).or_insert_with(Vec::new);
            worker_utils.push(utilization);
            
            // Keep only last 100 measurements per worker
            while worker_utils.len() > 100 {
                worker_utils.remove(0);
            }
        }
    }

    pub fn record_task_completion(&self, duration: Duration, _worker_id: usize) {
        if let Ok(mut durations) = self.recent_task_durations.write() {
            durations.push_back(duration);
            
            // Keep only last 1000 task durations
            while durations.len() > 1000 {
                durations.pop_front();
            }
        }
    }

    pub fn analyze_performance(&self) -> PerformanceAnalysis {
        let average_utilization = self.calculate_average_utilization();
        let utilization_variance = self.calculate_utilization_variance();
        let average_response_time = self.calculate_average_response_time();
        let throughput = self.calculate_throughput();

        // Calculate efficiency score (0.0 to 1.0)
        let efficiency = self.calculate_efficiency_score(average_utilization, utilization_variance);

        PerformanceAnalysis {
            average_utilization,
            utilization_variance,
            average_response_time,
            throughput,
            efficiency,
            bottleneck_detected: self.detect_bottlenecks(),
        }
    }

    pub fn get_metrics(&self) -> ConcurrencyMetrics {
        let analysis = self.analyze_performance();
        
        ConcurrencyMetrics {
            average_utilization: analysis.average_utilization,
            efficiency_score: analysis.efficiency,
            throughput: analysis.throughput,
            average_response_time: analysis.average_response_time,
        }
    }

    fn calculate_average_utilization(&self) -> f32 {
        if let Ok(utils) = self.worker_utilizations.read() {
            let all_utils: Vec<f32> = utils.values()
                .flat_map(|worker_utils| worker_utils.iter())
                .cloned()
                .collect();
            
            if all_utils.is_empty() {
                0.0
            } else {
                all_utils.iter().sum::<f32>() / all_utils.len() as f32
            }
        } else {
            0.0
        }
    }

    fn calculate_utilization_variance(&self) -> f32 {
        if let Ok(utils) = self.worker_utilizations.read() {
            let worker_averages: Vec<f32> = utils.values()
                .map(|worker_utils| {
                    if worker_utils.is_empty() {
                        0.0
                    } else {
                        worker_utils.iter().sum::<f32>() / worker_utils.len() as f32
                    }
                })
                .collect();
            
            if worker_averages.len() < 2 {
                return 0.0;
            }

            let mean = worker_averages.iter().sum::<f32>() / worker_averages.len() as f32;
            let variance = worker_averages.iter()
                .map(|&x| (x - mean).powi(2))
                .sum::<f32>() / worker_averages.len() as f32;
            
            variance.sqrt() // Return standard deviation
        } else {
            0.0
        }
    }

    fn calculate_average_response_time(&self) -> Duration {
        if let Ok(durations) = self.recent_task_durations.read() {
            if durations.is_empty() {
                Duration::from_millis(100) // Default
            } else {
                let total_nanos: u128 = durations.iter().map(|d| d.as_nanos()).sum();
                Duration::from_nanos((total_nanos / durations.len() as u128) as u64)
            }
        } else {
            Duration::from_millis(100)
        }
    }

    fn calculate_throughput(&self) -> f64 {
        if let Ok(durations) = self.recent_task_durations.read() {
            if durations.len() < 2 {
                0.0
            } else {
                // Estimate throughput based on recent completions
                let time_window = Duration::from_secs(60); // Last minute
                let recent_count = durations.len();
                recent_count as f64 / time_window.as_secs_f64()
            }
        } else {
            0.0
        }
    }

    fn calculate_efficiency_score(&self, utilization: f32, variance: f32) -> f32 {
        // Efficiency is high when utilization is good and variance is low
        let utilization_score = if utilization > 0.8 {
            1.0 - (utilization - 0.8) / 0.2 // Penalty for overutilization
        } else {
            utilization / 0.8 // Linear increase up to 80%
        };

        let variance_score = 1.0 - variance.min(1.0); // Lower variance is better

        (utilization_score * 0.7 + variance_score * 0.3).max(0.0).min(1.0)
    }

    fn detect_bottlenecks(&self) -> bool {
        let avg_util = self.calculate_average_utilization();
        let variance = self.calculate_utilization_variance();
        
        // Bottleneck detected if high utilization with high variance
        avg_util > 0.9 || variance > 0.3
    }
}

/// Thread manager for dynamic thread pool adjustment
#[derive(Debug)]
struct ThreadManager {
    adjustment_history: Vec<ThreadAdjustment>,
}

impl ThreadManager {
    fn new() -> Self {
        Self {
            adjustment_history: Vec::new(),
        }
    }

    fn adjust_thread_count(
        &mut self,
        current_count: usize,
        target_count: usize,
        config: &ConcurrencyConfig,
    ) -> usize {
        let clamped_target = target_count.max(config.min_threads).min(config.max_threads);
        
        // Gradual adjustment to avoid system shock
        let max_change = (current_count / 4).max(1); // Max 25% change per adjustment
        let actual_target = if clamped_target > current_count {
            (current_count + max_change).min(clamped_target)
        } else {
            current_count.saturating_sub(max_change).max(clamped_target)
        };

        // Record adjustment
        let adjustment = ThreadAdjustment {
            timestamp: Instant::now(),
            from_count: current_count,
            to_count: actual_target,
            reason: AdjustmentReason::WorkloadChange,
        };
        
        self.adjustment_history.push(adjustment);
        
        // Keep only last 100 adjustments
        while self.adjustment_history.len() > 100 {
            self.adjustment_history.remove(0);
        }

        actual_target
    }
}

/// AI tuning algorithm for optimal thread count prediction
#[derive(Debug)]
struct TuningAlgorithm {
    model_weights: NeuralWeights,
    learning_rate: f32,
    performance_history: Vec<PerformanceSnapshot>,
    prediction_accuracy: f32,
}

impl TuningAlgorithm {
    fn new() -> Self {
        Self {
            model_weights: NeuralWeights::new(),
            learning_rate: 0.01,
            performance_history: Vec::new(),
            prediction_accuracy: 0.5,
        }
    }

    fn calculate_optimal_thread_count(
        &self,
        current_threads: usize,
        workload: &WorkloadAnalysis,
        performance: &PerformanceAnalysis,
    ) -> usize {
        // Neural network inference for optimal thread count
        let workload_factor = self.calculate_workload_factor(workload);
        let performance_factor = self.calculate_performance_factor(performance);
        
        // Apply neural network weights
        let adjustment_signal = workload_factor * self.model_weights.workload_weight
            + performance_factor * self.model_weights.performance_weight
            + self.model_weights.bias;

        // Convert signal to thread count adjustment
        let thread_adjustment = (adjustment_signal * current_threads as f32) as i32;
        let new_thread_count = (current_threads as i32 + thread_adjustment).max(1) as usize;

        new_thread_count
    }

    fn calculate_workload_factor(&self, workload: &WorkloadAnalysis) -> f32 {
        // Factor based on queue length, submission rate, and task characteristics
        let queue_factor = (workload.queue_length as f32 / 50.0).min(2.0); // Normalize
        let rate_factor = (workload.submission_rate as f32 / 10.0).min(2.0);
        let duration_factor = workload.average_task_duration.as_millis() as f32 / 1000.0; // Seconds
        
        (queue_factor + rate_factor + duration_factor) / 3.0
    }

    fn calculate_performance_factor(&self, performance: &PerformanceAnalysis) -> f32 {
        // Factor based on utilization and efficiency
        let util_factor = if performance.average_utilization > 0.8 {
            2.0 - performance.average_utilization // Penalty for high utilization
        } else {
            performance.average_utilization * 1.25 // Reward for good utilization
        };

        let efficiency_factor = performance.efficiency;
        
        (util_factor + efficiency_factor) / 2.0
    }

    fn update_performance_feedback(&mut self, performance: &PerformanceAnalysis) {
        // Record performance for learning
        let snapshot = PerformanceSnapshot {
            timestamp: Instant::now(),
            analysis: performance.clone(),
        };
        
        self.performance_history.push(snapshot);
        
        // Keep only last 1000 snapshots
        while self.performance_history.len() > 1000 {
            self.performance_history.remove(0);
        }

        // Update prediction accuracy based on recent performance
        self.prediction_accuracy = performance.efficiency;
    }

    fn retrain_model(&mut self, historical_workload: &[WorkloadSnapshot]) {
        if historical_workload.len() < 10 {
            return; // Need sufficient data for training
        }

        // Multi-variable gradient descent with momentum and adaptive learning rate
        let recent_data = &historical_workload[historical_workload.len().saturating_sub(100)..];
        let learning_rate = 0.001;
        let momentum = 0.9;
        let decay_rate = 0.95;
        
        // Initialize momentum variables if needed
        let mut workload_momentum = 0.0;
        let mut bias_momentum = 0.0;
        
        for snapshot in recent_data {
            let workload_factor = self.calculate_workload_factor(&snapshot.analysis);
            let target_performance = snapshot.analysis.intensity;
            
            // Multi-feature prediction including CPU utilization, memory pressure
            let cpu_factor = snapshot.performance.cpu_utilization * 0.3;
            let memory_factor = (snapshot.performance.memory_usage as f64 / 1024.0 / 1024.0 / 1024.0) * 0.2;
            let task_count_factor = snapshot.analysis.task_count as f64 * 0.1;
            
            let prediction = workload_factor * self.model_weights.workload_weight + 
                           cpu_factor * 0.4 + memory_factor * 0.3 + task_count_factor * 0.2 + 
                           self.model_weights.bias;
            let error = target_performance - prediction;
            
            // Momentum-based gradient descent with adaptive learning rate
            let workload_gradient = error * workload_factor;
            let bias_gradient = error;
            
            workload_momentum = momentum * workload_momentum + learning_rate * workload_gradient;
            bias_momentum = momentum * bias_momentum + learning_rate * bias_gradient;
            
            self.model_weights.workload_weight += workload_momentum;
            self.model_weights.bias += bias_momentum;
            
            // Apply learning rate decay over time
            let adjusted_learning_rate = learning_rate * decay_rate;
        }
        
        // Clamp weights to reasonable ranges
        self.model_weights.workload_weight = self.model_weights.workload_weight.max(-2.0).min(2.0);
        self.model_weights.bias = self.model_weights.bias.max(-1.0).min(1.0);
    }
}

// Supporting data structures

#[derive(Debug, Clone)]
struct TaskSubmission {
    task_id: TaskId,
    priority: TaskPriority,
    estimated_duration: Duration,
    submitted_at: Instant,
    pub tags: Vec<String>,
    pub memory_requirement: usize,
    pub dependencies: Vec<TaskId>,
}

#[derive(Debug, Clone)]
struct TaskCompletion {
    task_id: TaskId,
    actual_duration: Duration,
    completed_at: Instant,
    worker_id: usize,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
enum TaskPattern {
    ShortCpuBound,    // < 100ms, CPU intensive
    LongCpuBound,     // > 1s, CPU intensive
    ShortIoBound,     // < 100ms, I/O intensive
    LongIoBound,      // > 1s, I/O intensive
    HighPriority,     // High priority tasks
    LowPriority,      // Low priority tasks
}

impl TaskPattern {
    fn from_submission(submission: &TaskSubmission) -> Self {
        let is_long = submission.estimated_duration > Duration::from_millis(1000);
        let is_high_priority = matches!(submission.priority, TaskPriority::High | TaskPriority::Critical);
        
        if is_high_priority {
            TaskPattern::HighPriority
        } else if matches!(submission.priority, TaskPriority::Low) {
            TaskPattern::LowPriority
        } else if is_long {
            // Analyze task characteristics to determine actual pattern
            if submission.tags.iter().any(|tag| tag.contains("io") || tag.contains("network") || tag.contains("file")) {
                TaskPattern::IOBound
            } else if submission.tags.iter().any(|tag| tag.contains("compute") || tag.contains("math") || tag.contains("cpu")) {
                TaskPattern::LongCpuBound
            } else {
                // Estimate based on memory requirements and dependencies
                if submission.memory_requirement.unwrap_or(0) > 100 * 1024 * 1024 { // > 100MB
                    TaskPattern::MemoryBound
                } else if submission.dependencies.len() > 3 {
                    TaskPattern::IOBound // Dependencies suggest I/O coordination
                } else {
                    TaskPattern::LongCpuBound // Default for long tasks
                }
            }
        } else {
            TaskPattern::ShortCpuBound
        }
    }

    fn is_cpu_intensive(&self) -> bool {
        matches!(self, TaskPattern::ShortCpuBound | TaskPattern::LongCpuBound)
    }
    
    fn is_io_intensive(&self) -> bool {
        matches!(self, TaskPattern::ShortIoBound | TaskPattern::LongIoBound)
    }
}

#[derive(Debug, Clone)]
pub struct WorkloadAnalysis {
    pub queue_length: usize,
    pub submission_rate: f64,
    pub completion_rate: f64,
    pub average_task_duration: Duration,
    pub workload_type: WorkloadType,
    pub intensity: f32,
    pub cpu_bound_ratio: f32,
    pub io_bound_ratio: f32,
    pub task_count: usize,
}

#[derive(Debug, Clone)]
pub enum WorkloadType {
    Steady,         // Consistent workload
    Burst,          // High-frequency short tasks
    LongRunning,    // Few but long-duration tasks
    HighThroughput, // High task submission rate
}

#[derive(Debug, Clone)]
pub struct PerformanceAnalysis {
    pub average_utilization: f32,
    pub utilization_variance: f32,
    pub average_response_time: Duration,
    pub throughput: f64,
    pub efficiency: f32,
    pub bottleneck_detected: bool,
}

#[derive(Debug, Clone)]
struct WorkloadSnapshot {
    timestamp: Instant,
    analysis: WorkloadAnalysis,
    pub performance: PerformanceSnapshot,
}

#[derive(Debug, Clone)]
struct PerformanceSnapshot {
    timestamp: Instant,
    analysis: PerformanceAnalysis,
    pub cpu_utilization: f32,
    pub memory_usage: f32,
}

#[derive(Debug)]
struct SystemMetrics {
    cpu_usage: f32,
    memory_usage: f32,
    load_average: f32,
}

impl SystemMetrics {
    fn new() -> Self {
        Self {
            cpu_usage: 0.0,
            memory_usage: 0.0,
            load_average: 0.0,
        }
    }
}

#[derive(Debug)]
struct ThreadAdjustment {
    timestamp: Instant,
    from_count: usize,
    to_count: usize,
    reason: AdjustmentReason,
}

#[derive(Debug)]
enum AdjustmentReason {
    WorkloadChange,
    PerformanceOptimization,
    ManualOverride,
}

#[derive(Debug)]
struct NeuralWeights {
    workload_weight: f32,
    performance_weight: f32,
    bias: f32,
}

impl NeuralWeights {
    fn new() -> Self {
        Self {
            workload_weight: 1.0,
            performance_weight: 1.0,
            bias: 0.0,
        }
    }
}

#[derive(Debug, Clone)]
pub struct ConcurrencyMetrics {
    pub average_utilization: f32,
    pub efficiency_score: f32,
    pub throughput: f64,
    pub average_response_time: Duration,
}