//! Advanced Safety System for Runa
//! Making Runa safer than Rust while maintaining simplicity

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex, RwLock};
use std::time::{Duration, Instant};
use runa_common::bytecode::Value;

/// Ownership tracker that uses natural language patterns
#[derive(Debug, Clone)]
pub struct OwnershipTracker {
    pub owned_values: HashMap<String, OwnershipInfo>,
    pub borrowed_values: HashMap<String, BorrowInfo>,
    pub lifetime_dependencies: HashMap<String, Vec<String>>,
    pub access_patterns: HashMap<String, AccessPattern>,
}

#[derive(Debug, Clone)]
pub struct OwnershipInfo {
    pub owner: String,
    pub value_type: String,
    pub created_at: Instant,
    pub last_accessed: Instant,
    pub access_count: u64,
    pub can_be_moved: bool,
    pub is_unique: bool,
}

#[derive(Debug, Clone)]
pub struct BorrowInfo {
    pub borrower: String,
    pub original_owner: String,
    pub borrow_type: BorrowType,
    pub borrowed_at: Instant,
    pub expected_return: Option<Instant>,
    pub is_mutable: bool,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BorrowType {
    Shared,     // Multiple readers allowed
    Exclusive,  // Single writer, no readers
    Temporary,  // Short-term borrow for operation
    Transfer,   // Ownership transfer
}

#[derive(Debug, Clone)]
pub struct AccessPattern {
    pub reads: u64,
    pub writes: u64,
    pub concurrent_accesses: u64,
    pub last_race_condition: Option<Instant>,
    pub typical_lifetime: Duration,
}

/// Memory safety manager with automatic leak detection
pub struct MemorySafetyManager {
    pub active_allocations: Arc<Mutex<HashMap<usize, AllocationInfo>>>,
    pub freed_allocations: Arc<RwLock<HashSet<usize>>>,
    pub dangling_pointers: Arc<RwLock<Vec<DanglingPointer>>>,
    pub leak_detector: LeakDetector,
    pub bounds_checker: BoundsChecker,
}

#[derive(Debug, Clone)]
pub struct AllocationInfo {
    pub address: usize,
    pub size: usize,
    pub allocated_at: Instant,
    pub stack_trace: Vec<String>,
    pub allocation_type: AllocationType,
    pub expected_lifetime: Option<Duration>,
}

#[derive(Debug, Clone)]
pub enum AllocationType {
    Stack,
    Heap,
    Static,
    SharedReference,
}

#[derive(Debug, Clone)]
pub struct DanglingPointer {
    pub pointer_address: usize,
    pub original_target: usize,
    pub detected_at: Instant,
    pub last_valid_access: Instant,
}

/// Leak detector that tracks allocation patterns
pub struct LeakDetector {
    pub allocation_patterns: HashMap<String, AllocationPattern>,
    pub suspected_leaks: Vec<SuspectedLeak>,
    pub detection_threshold: Duration,
}

#[derive(Debug, Clone)]
pub struct AllocationPattern {
    pub function_name: String,
    pub typical_size: usize,
    pub typical_lifetime: Duration,
    pub allocation_count: u64,
    pub leak_count: u64,
}

#[derive(Debug, Clone)]
pub struct SuspectedLeak {
    pub allocation_info: AllocationInfo,
    pub suspicion_level: f32, // 0.0 - 1.0
    pub reasons: Vec<String>,
}

/// Bounds checker for array/string access
pub struct BoundsChecker {
    pub checked_accesses: u64,
    pub bounds_violations: Vec<BoundsViolation>,
    pub auto_fix_enabled: bool,
}

#[derive(Debug, Clone)]
pub struct BoundsViolation {
    pub array_name: String,
    pub attempted_index: isize,
    pub actual_size: usize,
    pub violation_type: BoundsViolationType,
    pub detected_at: Instant,
    pub stack_trace: Vec<String>,
}

#[derive(Debug, Clone)]
pub enum BoundsViolationType {
    NegativeIndex,
    IndexTooLarge,
    NullPointerAccess,
    UseAfterFree,
}

/// Null safety system
pub struct NullSafetyChecker {
    pub tracked_optionals: HashMap<String, OptionalTracker>,
    pub null_checks: u64,
    pub prevented_null_access: u64,
}

#[derive(Debug, Clone)]
pub struct OptionalTracker {
    pub variable_name: String,
    pub is_none: bool,
    pub last_check: Option<Instant>,
    pub access_attempts: u64,
}

/// Race condition detector for concurrent access
pub struct RaceConditionDetector {
    pub monitored_variables: HashMap<String, ConcurrencyTracker>,
    pub detected_races: Vec<RaceCondition>,
    pub thread_access_log: Vec<ThreadAccess>,
}

#[derive(Debug, Clone)]
pub struct ConcurrencyTracker {
    pub variable_name: String,
    pub current_readers: HashSet<String>, // thread IDs
    pub current_writer: Option<String>,
    pub lock_order: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct RaceCondition {
    pub variable_name: String,
    pub thread1: String,
    pub thread2: String,
    pub access_type1: AccessType,
    pub access_type2: AccessType,
    pub detected_at: Instant,
}

#[derive(Debug, Clone)]
pub enum AccessType {
    Read,
    Write,
    ReadWrite,
}

#[derive(Debug, Clone)]
pub struct ThreadAccess {
    pub thread_id: String,
    pub variable_name: String,
    pub access_type: AccessType,
    pub timestamp: Instant,
}

impl OwnershipTracker {
    pub fn new() -> Self {
        OwnershipTracker {
            owned_values: HashMap::new(),
            borrowed_values: HashMap::new(),
            lifetime_dependencies: HashMap::new(),
            access_patterns: HashMap::new(),
        }
    }

    /// Natural language ownership declaration: "Let user own the data"
    pub fn declare_ownership(&mut self, owner: &str, value_name: &str, value_type: &str) {
        let ownership_info = OwnershipInfo {
            owner: owner.to_string(),
            value_type: value_type.to_string(),
            created_at: Instant::now(),
            last_accessed: Instant::now(),
            access_count: 0,
            can_be_moved: true,
            is_unique: true,
        };

        self.owned_values.insert(value_name.to_string(), ownership_info);
        
        // Initialize access pattern
        self.access_patterns.insert(value_name.to_string(), AccessPattern {
            reads: 0,
            writes: 1, // Creation counts as write
            concurrent_accesses: 0,
            last_race_condition: None,
            typical_lifetime: Duration::from_secs(300), // 5 minutes default
        });
    }

    /// Natural language borrowing: "Let function borrow the data temporarily"
    pub fn borrow_value(&mut self, borrower: &str, value_name: &str, borrow_type: BorrowType, duration: Option<Duration>) -> Result<(), SafetyError> {
        if !self.owned_values.contains_key(value_name) {
            return Err(SafetyError::ValueNotOwned(value_name.to_string()));
        }

        let ownership_info = self.owned_values.get(value_name).unwrap();

        // Check if borrowing is allowed
        match borrow_type {
            BorrowType::Exclusive => {
                // Check no existing borrows
                if self.borrowed_values.values().any(|b| b.original_owner == ownership_info.owner) {
                    return Err(SafetyError::AlreadyBorrowed(value_name.to_string()));
                }
            }
            BorrowType::Shared => {
                // Check no exclusive borrows
                if self.borrowed_values.values().any(|b| 
                    b.original_owner == ownership_info.owner && b.borrow_type == BorrowType::Exclusive
                ) {
                    return Err(SafetyError::ExclusivelyBorrowed(value_name.to_string()));
                }
            }
            _ => {}
        }

        let borrow_info = BorrowInfo {
            borrower: borrower.to_string(),
            original_owner: ownership_info.owner.clone(),
            borrow_type,
            borrowed_at: Instant::now(),
            expected_return: duration.map(|d| Instant::now() + d),
            is_mutable: matches!(borrow_type, BorrowType::Exclusive),
        };

        self.borrowed_values.insert(value_name.to_string(), borrow_info);
        Ok(())
    }

    /// Return borrowed value
    pub fn return_value(&mut self, value_name: &str) -> Result<(), SafetyError> {
        if !self.borrowed_values.contains_key(value_name) {
            return Err(SafetyError::NotBorrowed(value_name.to_string()));
        }

        self.borrowed_values.remove(value_name);
        Ok(())
    }

    /// Check if access is safe
    pub fn check_access(&mut self, accessor: &str, value_name: &str, access_type: AccessType) -> Result<(), SafetyError> {
        // Update access pattern
        if let Some(pattern) = self.access_patterns.get_mut(value_name) {
            match access_type {
                AccessType::Read => pattern.reads += 1,
                AccessType::Write => pattern.writes += 1,
                AccessType::ReadWrite => {
                    pattern.reads += 1;
                    pattern.writes += 1;
                }
            }
        }

        // Check ownership
        if let Some(ownership) = self.owned_values.get_mut(value_name) {
            if ownership.owner != accessor {
                // Check if borrowing is allowed
                if let Some(borrow) = self.borrowed_values.get(value_name) {
                    if borrow.borrower != accessor {
                        return Err(SafetyError::AccessDenied(accessor.to_string(), value_name.to_string()));
                    }
                    
                    // Check borrow type compatibility
                    match (&access_type, &borrow.borrow_type) {
                        (AccessType::Write, BorrowType::Shared) => {
                            return Err(SafetyError::WriteToSharedBorrow(value_name.to_string()));
                        }
                        _ => {}
                    }
                } else {
                    return Err(SafetyError::AccessDenied(accessor.to_string(), value_name.to_string()));
                }
            }

            ownership.last_accessed = Instant::now();
            ownership.access_count += 1;
        }

        Ok(())
    }
}

impl MemorySafetyManager {
    pub fn new() -> Self {
        MemorySafetyManager {
            active_allocations: Arc::new(Mutex::new(HashMap::new())),
            freed_allocations: Arc::new(RwLock::new(HashSet::new())),
            dangling_pointers: Arc::new(RwLock::new(Vec::new())),
            leak_detector: LeakDetector::new(),
            bounds_checker: BoundsChecker::new(),
        }
    }

    /// Track new allocation with complete stack trace capture
    pub fn track_allocation(&self, address: usize, size: usize, allocation_type: AllocationType, function_name: &str) {
        let allocation_info = AllocationInfo {
            address,
            size,
            allocated_at: Instant::now(),
            stack_trace: capture_detailed_stack_trace(function_name),
            allocation_type: allocation_type.clone(),
            expected_lifetime: calculate_expected_lifetime(&allocation_type, size),
        };

        if let Ok(mut allocations) = self.active_allocations.lock() {
            allocations.insert(address, allocation_info);
        }
    }

    /// Track deallocation
    pub fn track_deallocation(&self, address: usize) -> Result<(), SafetyError> {
        let removed = if let Ok(mut allocations) = self.active_allocations.lock() {
            allocations.remove(&address)
        } else {
            return Err(SafetyError::LockPoisoned);
        };

        if removed.is_some() {
            if let Ok(mut freed) = self.freed_allocations.write() {
                freed.insert(address);
            }
            Ok(())
        } else {
            Err(SafetyError::DoubleFree(address))
        }
    }

    /// Check for dangling pointers
    pub fn check_pointer(&self, pointer: usize) -> Result<(), SafetyError> {
        if let Ok(freed) = self.freed_allocations.read() {
            if freed.contains(&pointer) {
                return Err(SafetyError::UseAfterFree(pointer));
            }
        }

        if let Ok(allocations) = self.active_allocations.lock() {
            if !allocations.contains_key(&pointer) {
                return Err(SafetyError::InvalidPointer(pointer));
            }
        }

        Ok(())
    }

    /// Run comprehensive leak detection with advanced heuristics
    pub fn detect_leaks(&mut self) -> Vec<SuspectedLeak> {
        let mut suspected_leaks = Vec::new();
        let now = Instant::now();

        if let Ok(allocations) = self.active_allocations.lock() {
            // Collect allocation statistics for analysis
            let total_allocations = allocations.len();
            let total_memory: usize = allocations.values().map(|a| a.size).sum();
            let average_size = if total_allocations > 0 { total_memory / total_allocations } else { 0 };
            
            for (_, allocation) in allocations.iter() {
                let age = now.duration_since(allocation.allocated_at);
                let mut reasons = Vec::new();
                let mut suspicion_level = 0.0f32;
                
                // Advanced leak detection heuristics
                let leak_analysis = analyze_allocation_for_leaks(allocation, age, total_memory, average_size);
                
                if leak_analysis.is_suspicious {
                    suspected_leaks.push(SuspectedLeak {
                        allocation_info: allocation.clone(),
                        suspicion_level: leak_analysis.suspicion_level,
                        reasons: leak_analysis.reasons,
                    });
                }
            }
        }

        // Sort by suspicion level (highest first)
        suspected_leaks.sort_by(|a, b| b.suspicion_level.partial_cmp(&a.suspicion_level).unwrap_or(std::cmp::Ordering::Equal));
        
        suspected_leaks
    }
}

impl BoundsChecker {
    pub fn new() -> Self {
        BoundsChecker {
            checked_accesses: 0,
            bounds_violations: Vec::new(),
            auto_fix_enabled: true,
        }
    }

    /// Check array bounds with automatic fixing
    pub fn check_array_access(&mut self, array_name: &str, index: isize, array_size: usize) -> Result<usize, SafetyError> {
        self.checked_accesses += 1;

        if index < 0 {
            let violation = BoundsViolation {
                array_name: array_name.to_string(),
                attempted_index: index,
                actual_size: array_size,
                violation_type: BoundsViolationType::NegativeIndex,
                detected_at: Instant::now(),
                stack_trace: vec![], // Would be populated with actual stack trace
            };
            self.bounds_violations.push(violation);

            if self.auto_fix_enabled {
                return Ok(0); // Clamp to start
            } else {
                return Err(SafetyError::NegativeIndex(index));
            }
        }

        if index as usize >= array_size {
            let violation = BoundsViolation {
                array_name: array_name.to_string(),
                attempted_index: index,
                actual_size: array_size,
                violation_type: BoundsViolationType::IndexTooLarge,
                detected_at: Instant::now(),
                stack_trace: vec![],
            };
            self.bounds_violations.push(violation);

            if self.auto_fix_enabled {
                return Ok(array_size.saturating_sub(1)); // Clamp to end
            } else {
                return Err(SafetyError::IndexOutOfBounds(index, array_size));
            }
        }

        Ok(index as usize)
    }
}

impl LeakDetector {
    pub fn new() -> Self {
        LeakDetector {
            allocation_patterns: HashMap::new(),
            suspected_leaks: Vec::new(),
            detection_threshold: Duration::from_secs(300), // 5 minutes
        }
    }
}

impl NullSafetyChecker {
    pub fn new() -> Self {
        NullSafetyChecker {
            tracked_optionals: HashMap::new(),
            null_checks: 0,
            prevented_null_access: 0,
        }
    }

    /// Check if optional value is safe to access
    pub fn check_optional_access(&mut self, var_name: &str) -> Result<(), SafetyError> {
        self.null_checks += 1;

        if let Some(tracker) = self.tracked_optionals.get_mut(var_name) {
            if tracker.is_none {
                self.prevented_null_access += 1;
                return Err(SafetyError::NullPointerAccess(var_name.to_string()));
            }
            tracker.access_attempts += 1;
            tracker.last_check = Some(Instant::now());
        }

        Ok(())
    }
}

// ============================================================================
// ADVANCED LEAK DETECTION FUNCTIONS
// ============================================================================

/// Comprehensive analysis result for leak detection
#[derive(Debug, Clone)]
struct LeakAnalysisResult {
    is_suspicious: bool,
    suspicion_level: f32,
    reasons: Vec<String>,
}

/// Capture detailed stack trace for allocation tracking
fn capture_detailed_stack_trace(function_name: &str) -> Vec<String> {
    let mut stack_trace = Vec::new();
    
    // Add the calling function
    stack_trace.push(function_name.to_string());
    
    // Capture actual stack trace using std::backtrace
    let backtrace = std::backtrace::Backtrace::new();
    
    // Process backtrace frames and extract meaningful function names
    for (i, frame) in backtrace.frames().iter().take(15).enumerate() { // Limit to 15 frames
        for symbol in frame.symbols() {
            if let Some(name) = symbol.name() {
                let name_str = name.to_string();
                
                // Filter out internal Rust symbols and keep relevant ones
                if is_relevant_stack_frame(&name_str) {
                    let cleaned_name = clean_symbol_name(&name_str);
                    if !cleaned_name.is_empty() && !stack_trace.contains(&cleaned_name) {
                        stack_trace.push(format!("{}:{}", cleaned_name, i));
                    }
                }
            }
        }
    }
    
    // If we couldn't get a good stack trace, provide basic information
    if stack_trace.len() == 1 {
        stack_trace.push("<stack trace unavailable>".to_string());
    }
    
    stack_trace
}

/// Calculate expected lifetime based on allocation type and size
fn calculate_expected_lifetime(allocation_type: &AllocationType, size: usize) -> Option<Duration> {
    match allocation_type {
        AllocationType::Stack => Some(Duration::from_secs(1)), // Stack allocations should be short-lived
        AllocationType::Heap => {
            // Heap allocations vary by size
            match size {
                0..=1024 => Some(Duration::from_secs(300)), // Small allocations: 5 minutes
                1025..=65536 => Some(Duration::from_secs(1800)), // Medium allocations: 30 minutes  
                65537..=1048576 => Some(Duration::from_secs(7200)), // Large allocations: 2 hours
                _ => Some(Duration::from_secs(14400)), // Very large allocations: 4 hours
            }
        }
        AllocationType::Global => None, // Global allocations can live indefinitely
        AllocationType::ThreadLocal => Some(Duration::from_secs(3600)), // Thread-local: 1 hour
    }
}

/// Advanced analysis of allocation for leak detection
fn analyze_allocation_for_leaks(
    allocation: &AllocationInfo,
    age: Duration,
    total_memory: usize,
    average_size: usize,
) -> LeakAnalysisResult {
    let mut reasons = Vec::new();
    let mut suspicion_level = 0.0f32;
    
    // Age-based analysis
    let age_suspicion = analyze_age_patterns(allocation, age, &mut reasons);
    suspicion_level += age_suspicion;
    
    // Size-based analysis
    let size_suspicion = analyze_size_patterns(allocation, average_size, total_memory, &mut reasons);
    suspicion_level += size_suspicion;
    
    // Stack trace analysis
    let stack_suspicion = analyze_stack_trace_patterns(&allocation.stack_trace, &mut reasons);
    suspicion_level += stack_suspicion;
    
    // Allocation type analysis
    let type_suspicion = analyze_allocation_type_patterns(allocation, age, &mut reasons);
    suspicion_level += type_suspicion;
    
    // Pattern-based analysis
    let pattern_suspicion = analyze_allocation_patterns(allocation, &mut reasons);
    suspicion_level += pattern_suspicion;
    
    // Normalize suspicion level (0.0 to 1.0)
    suspicion_level = suspicion_level.min(1.0);
    
    LeakAnalysisResult {
        is_suspicious: suspicion_level > 0.3, // Threshold for considering something suspicious
        suspicion_level,
        reasons,
    }
}

/// Analyze allocation age patterns for leaks
fn analyze_age_patterns(
    allocation: &AllocationInfo,
    age: Duration,
    reasons: &mut Vec<String>,
) -> f32 {
    let mut suspicion = 0.0f32;
    
    // Check against expected lifetime
    if let Some(expected_lifetime) = allocation.expected_lifetime {
        if age > expected_lifetime {
            let overage_ratio = age.as_secs_f32() / expected_lifetime.as_secs_f32();
            suspicion += (overage_ratio - 1.0).min(0.5); // Cap at 0.5
            reasons.push(format!("Exceeded expected lifetime by {:.1}x", overage_ratio));
        }
    } else {
        // No expected lifetime - use absolute age thresholds
        match age.as_secs() {
            3600..=7200 => {
                suspicion += 0.2;
                reasons.push("Long-lived allocation (1-2 hours)".to_string());
            }
            7201..=21600 => {
                suspicion += 0.4;
                reasons.push("Very long-lived allocation (2-6 hours)".to_string());
            }
            21601.. => {
                suspicion += 0.6;
                reasons.push("Extremely long-lived allocation (>6 hours)".to_string());
            }
            _ => {} // Not suspicious based on age
        }
    }
    
    suspicion
}

/// Analyze allocation size patterns for leaks
fn analyze_size_patterns(
    allocation: &AllocationInfo,
    average_size: usize,
    total_memory: usize,
    reasons: &mut Vec<String>,
) -> f32 {
    let mut suspicion = 0.0f32;
    
    // Large allocation analysis
    if allocation.size > 10 * 1024 * 1024 { // >10MB
        suspicion += 0.3;
        reasons.push(format!("Large allocation ({} MB)", allocation.size / (1024 * 1024)));
    } else if allocation.size > 1024 * 1024 { // >1MB
        suspicion += 0.1;
        reasons.push(format!("Medium-large allocation ({} KB)", allocation.size / 1024));
    }
    
    // Disproportionate size analysis
    if average_size > 0 && allocation.size > 100 * average_size {
        suspicion += 0.2;
        reasons.push(format!("Disproportionately large ({:.1}x average size)", allocation.size as f32 / average_size as f32));
    }
    
    // Memory usage analysis
    if total_memory > 0 {
        let memory_percentage = (allocation.size as f32 / total_memory as f32) * 100.0;
        if memory_percentage > 25.0 {
            suspicion += 0.25;
            reasons.push(format!("Consumes {:.1}% of total memory", memory_percentage));
        }
    }
    
    suspicion
}

/// Analyze stack trace patterns for potential leaks
fn analyze_stack_trace_patterns(
    stack_trace: &[String],
    reasons: &mut Vec<String>,
) -> f32 {
    let mut suspicion = 0.0f32;
    
    // Look for suspicious function patterns
    let suspicious_patterns = [
        ("malloc", 0.1, "Direct malloc usage"),
        ("alloc", 0.05, "Direct allocation"),
        ("new", 0.05, "New allocation"),
        ("clone", 0.1, "Object cloning"),
        ("copy", 0.05, "Data copying"),
        ("buffer", 0.1, "Buffer allocation"),
        ("cache", 0.15, "Cache-related allocation"),
        ("pool", 0.1, "Pool allocation"),
        ("string", 0.05, "String allocation"),
        ("vec", 0.05, "Vector allocation"),
    ];
    
    for frame in stack_trace {
        let frame_lower = frame.to_lowercase();
        for (pattern, score, description) in &suspicious_patterns {
            if frame_lower.contains(pattern) {
                suspicion += score;
                reasons.push(format!("Stack contains {}: {}", description, frame));
                break; // Only count once per frame
            }
        }
    }
    
    // Deep stack analysis
    if stack_trace.len() > 10 {
        suspicion += 0.1;
        reasons.push(format!("Deep call stack ({} frames)", stack_trace.len()));
    }
    
    suspicion.min(0.3) // Cap stack-based suspicion
}

/// Analyze allocation type patterns
fn analyze_allocation_type_patterns(
    allocation: &AllocationInfo,
    age: Duration,
    reasons: &mut Vec<String>,
) -> f32 {
    match allocation.allocation_type {
        AllocationType::Stack => {
            if age > Duration::from_secs(60) { // Stack allocations shouldn't live > 1 minute
                reasons.push("Stack allocation living too long".to_string());
                return 0.4;
            }
        }
        AllocationType::ThreadLocal => {
            if age > Duration::from_secs(7200) { // Thread-local shouldn't live > 2 hours
                reasons.push("Thread-local allocation living too long".to_string());
                return 0.3;
            }
        }
        AllocationType::Global => {
            // Global allocations are expected to be long-lived
            return 0.0;
        }
        AllocationType::Heap => {
            // Heap allocations are analyzed by other heuristics
        }
    }
    
    0.0
}

/// Analyze allocation patterns for anomalies
fn analyze_allocation_patterns(
    allocation: &AllocationInfo,
    reasons: &mut Vec<String>,
) -> f32 {
    let mut suspicion = 0.0f32;
    
    // Look for power-of-2 sizes that might indicate buffer allocations
    if allocation.size > 1024 && (allocation.size & (allocation.size - 1)) == 0 {
        suspicion += 0.05;
        reasons.push("Power-of-2 size (potential buffer)".to_string());
    }
    
    // Look for very round numbers that might indicate placeholder sizes
    if allocation.size % 1000 == 0 && allocation.size >= 10000 {
        suspicion += 0.1;
        reasons.push("Round number size (potential placeholder)".to_string());
    }
    
    // Address alignment analysis
    if allocation.address % 4096 == 0 { // Page-aligned
        suspicion += 0.05;
        reasons.push("Page-aligned allocation".to_string());
    }
    
    suspicion
}

/// Check if a stack frame is relevant for leak detection
fn is_relevant_stack_frame(name: &str) -> bool {
    // Filter out internal Rust and system symbols
    !name.contains("rust_begin_unwind") &&
    !name.contains("rust_panic") &&
    !name.contains("__pthread") &&
    !name.contains("_start") &&
    !name.contains("main") &&
    !name.contains("std::") &&
    !name.contains("core::") &&
    !name.contains("alloc::") &&
    name.len() < 200 // Avoid extremely long mangled names
}

/// Clean up symbol names for readability
fn clean_symbol_name(name: &str) -> String {
    // Remove Rust hash suffixes
    let cleaned = if let Some(pos) = name.find("::h") {
        &name[..pos]
    } else {
        name
    };
    
    // Extract the last meaningful part
    if let Some(pos) = cleaned.rfind("::") {
        cleaned[pos + 2..].to_string()
    } else {
        cleaned.to_string()
    }
}

/// Safety error types
#[derive(Debug, Clone)]
pub enum SafetyError {
    ValueNotOwned(String),
    AlreadyBorrowed(String),
    ExclusivelyBorrowed(String),
    NotBorrowed(String),
    AccessDenied(String, String),
    WriteToSharedBorrow(String),
    DoubleFree(usize),
    UseAfterFree(usize),
    InvalidPointer(usize),
    NegativeIndex(isize),
    IndexOutOfBounds(isize, usize),
    NullPointerAccess(String),
    RaceCondition(String, String, String),
    LockPoisoned,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ownership_tracker() {
        let mut tracker = OwnershipTracker::new();
        
        tracker.declare_ownership("alice", "data", "String");
        
        assert!(tracker.borrow_value("bob", "data", BorrowType::Shared, None).is_ok());
        assert!(tracker.check_access("bob", "data", AccessType::Read).is_ok());
        assert!(tracker.check_access("bob", "data", AccessType::Write).is_err());
        
        tracker.return_value("data").unwrap();
        
        assert!(tracker.borrow_value("bob", "data", BorrowType::Exclusive, None).is_ok());
        assert!(tracker.check_access("bob", "data", AccessType::Write).is_ok());
    }

    #[test]
    fn test_bounds_checker() {
        let mut checker = BoundsChecker::new();
        
        assert_eq!(checker.check_array_access("arr", 5, 10).unwrap(), 5);
        assert_eq!(checker.check_array_access("arr", -1, 10).unwrap(), 0); // Auto-fixed
        assert_eq!(checker.check_array_access("arr", 15, 10).unwrap(), 9); // Auto-fixed
        
        assert_eq!(checker.bounds_violations.len(), 2);
    }

    #[test]
    fn test_memory_safety_manager() {
        let manager = MemorySafetyManager::new();
        
        manager.track_allocation(0x1000, 256, AllocationType::Heap, "test_function");
        assert!(manager.check_pointer(0x1000).is_ok());
        
        manager.track_deallocation(0x1000).unwrap();
        assert!(matches!(manager.check_pointer(0x1000), Err(SafetyError::UseAfterFree(_))));
    }
}