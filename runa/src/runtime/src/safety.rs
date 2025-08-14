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

#[derive(Debug, Clone, PartialEq)]
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

    /// Track new allocation
    pub fn track_allocation(&self, address: usize, size: usize, allocation_type: AllocationType, function_name: &str) {
        let allocation_info = AllocationInfo {
            address,
            size,
            allocated_at: Instant::now(),
            stack_trace: vec![function_name.to_string()], // Simplified stack trace
            allocation_type,
            expected_lifetime: None,
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

    /// Run leak detection
    pub fn detect_leaks(&mut self) -> Vec<SuspectedLeak> {
        let mut suspected_leaks = Vec::new();
        let now = Instant::now();

        if let Ok(allocations) = self.active_allocations.lock() {
            for (_, allocation) in allocations.iter() {
                let age = now.duration_since(allocation.allocated_at);
                
                // Simple heuristic: if allocation is older than 1 hour, it might be a leak
                if age > Duration::from_secs(3600) {
                    suspected_leaks.push(SuspectedLeak {
                        allocation_info: allocation.clone(),
                        suspicion_level: (age.as_secs() as f32 / 3600.0).min(1.0),
                        reasons: vec!["Long-lived allocation".to_string()],
                    });
                }
            }
        }

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