//! Advanced ownership tracking system for the Runa runtime.
//! Provides borrowing validation, ownership transfer, and memory safety analysis.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex, RwLock};
use std::ptr::NonNull;
use std::time::{Duration, Instant};
use crate::runa_object;

/// Ownership state of a memory object
#[derive(Debug, Clone, PartialEq)]
pub enum OwnershipState {
    Owned,
    Borrowed,
    MutableBorrowed,
    Moved,
    Freed,
}

/// Borrow type for tracking borrow relationships
#[derive(Debug, Clone, PartialEq)]
pub enum BorrowType {
    Immutable,
    Mutable,
}

/// Ownership information for a memory object
#[derive(Debug, Clone)]
pub struct OwnershipInfo {
    pub ptr: NonNull<u8>,
    pub state: OwnershipState,
    pub owner: Option<String>,
    pub borrows: Vec<BorrowInfo>,
    pub creation_time: Instant,
    pub last_access: Instant,
    pub size: usize,
    pub type_id: String,
    pub metadata: HashMap<String, String>,
}

/// Borrow information
#[derive(Debug, Clone)]
pub struct BorrowInfo {
    pub borrower: String,
    pub borrow_type: BorrowType,
    pub start_time: Instant,
    pub end_time: Option<Instant>,
    pub access_count: usize,
    pub metadata: HashMap<String, String>,
}

/// Ownership validation error
#[derive(Debug)]
pub enum OwnershipError {
    AlreadyBorrowed,
    MutableBorrowConflict,
    UseAfterMove,
    UseAfterFree,
    InvalidOwner,
    BorrowNotFound,
    ValidationFailed,
}

/// Ownership tracking statistics
#[derive(Debug, Default, Clone)]
pub struct OwnershipStats {
    pub total_objects: usize,
    pub owned_objects: usize,
    pub borrowed_objects: usize,
    pub moved_objects: usize,
    pub freed_objects: usize,
    pub borrow_violations: usize,
    pub ownership_violations: usize,
    pub validation_time_ms: u64,
}

/// Advanced ownership tracker
pub struct OwnershipTracker {
    objects: Arc<RwLock<HashMap<NonNull<u8>, OwnershipInfo>>>,
    borrowers: Arc<RwLock<HashMap<String, HashSet<NonNull<u8>>>>>,
    owners: Arc<RwLock<HashMap<String, HashSet<NonNull<u8>>>>>,
    stats: Arc<Mutex<OwnershipStats>>,
    validation_enabled: Arc<Mutex<bool>>,
    strict_mode: Arc<Mutex<bool>>,
}

impl OwnershipTracker {
    pub fn new() -> Self {
        Self {
            objects: Arc::new(RwLock::new(HashMap::new())),
            borrowers: Arc::new(RwLock::new(HashMap::new())),
            owners: Arc::new(RwLock::new(HashMap::new())),
            stats: Arc::new(Mutex::new(OwnershipStats::default())),
            validation_enabled: Arc::new(Mutex::new(true)),
            strict_mode: Arc::new(Mutex::new(false)),
        }
    }
    
    /// Register a new object with initial owner
    pub fn register_object(
        &self,
        ptr: NonNull<u8>,
        owner: String,
        size: usize,
        type_id: String
    ) -> Result<(), OwnershipError> {
        let now = Instant::now();
        
        let ownership_info = OwnershipInfo {
            ptr,
            state: OwnershipState::Owned,
            owner: Some(owner.clone()),
            borrows: Vec::new(),
            creation_time: now,
            last_access: now,
            size,
            type_id,
            metadata: HashMap::new(),
        };
        
        if let (Ok(mut objects), Ok(mut owners), Ok(mut stats)) = 
            (self.objects.write(), self.owners.write(), self.stats.lock()) {
            
            objects.insert(ptr, ownership_info);
            owners.entry(owner).or_insert_with(HashSet::new).insert(ptr);
            
            stats.total_objects += 1;
            stats.owned_objects += 1;
            
            Ok(())
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Create an immutable borrow
    pub fn borrow_immutable(
        &self,
        ptr: NonNull<u8>,
        borrower: String
    ) -> Result<(), OwnershipError> {
        let start_time = Instant::now();
        
        if let Ok(validation_enabled) = self.validation_enabled.lock() {
            if *validation_enabled {
                self.validate_borrow(ptr, BorrowType::Immutable)?;
            }
        }
        
        if let (Ok(mut objects), Ok(mut borrowers), Ok(mut stats)) = 
            (self.objects.write(), self.borrowers.write(), self.stats.lock()) {
            
            if let Some(obj_info) = objects.get_mut(&ptr) {
                // Check for mutable borrow conflicts
                if obj_info.borrows.iter().any(|b| b.borrow_type == BorrowType::Mutable && b.end_time.is_none()) {
                    return Err(OwnershipError::MutableBorrowConflict);
                }
                
                let borrow_info = BorrowInfo {
                    borrower: borrower.clone(),
                    borrow_type: BorrowType::Immutable,
                    start_time,
                    end_time: None,
                    access_count: 0,
                    metadata: HashMap::new(),
                };
                
                obj_info.borrows.push(borrow_info);
                obj_info.state = OwnershipState::Borrowed;
                obj_info.last_access = start_time;
                
                borrowers.entry(borrower).or_insert_with(HashSet::new).insert(ptr);
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Create a mutable borrow
    pub fn borrow_mutable(
        &self,
        ptr: NonNull<u8>,
        borrower: String
    ) -> Result<(), OwnershipError> {
        let start_time = Instant::now();
        
        if let Ok(validation_enabled) = self.validation_enabled.lock() {
            if *validation_enabled {
                self.validate_borrow(ptr, BorrowType::Mutable)?;
            }
        }
        
        if let (Ok(mut objects), Ok(mut borrowers), Ok(mut stats)) = 
            (self.objects.write(), self.borrowers.write(), self.stats.lock()) {
            
            if let Some(obj_info) = objects.get_mut(&ptr) {
                // Check for any active borrows
                if obj_info.borrows.iter().any(|b| b.end_time.is_none()) {
                    return Err(OwnershipError::AlreadyBorrowed);
                }
                
                let borrow_info = BorrowInfo {
                    borrower: borrower.clone(),
                    borrow_type: BorrowType::Mutable,
                    start_time,
                    end_time: None,
                    access_count: 0,
                    metadata: HashMap::new(),
                };
                
                obj_info.borrows.push(borrow_info);
                obj_info.state = OwnershipState::MutableBorrowed;
                obj_info.last_access = start_time;
                
                borrowers.entry(borrower).or_insert_with(HashSet::new).insert(ptr);
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// End a borrow
    pub fn end_borrow(
        &self,
        ptr: NonNull<u8>,
        borrower: String
    ) -> Result<(), OwnershipError> {
        let end_time = Instant::now();
        
        if let (Ok(mut objects), Ok(mut borrowers)) = 
            (self.objects.write(), self.borrowers.write()) {
            
            if let Some(obj_info) = objects.get_mut(&ptr) {
                // Find and end the borrow
                let mut found = false;
                for borrow in &mut obj_info.borrows {
                    if borrow.borrower == borrower && borrow.end_time.is_none() {
                        borrow.end_time = Some(end_time);
                        found = true;
                        break;
                    }
                }
                
                if !found {
                    return Err(OwnershipError::BorrowNotFound);
                }
                
                // Update state if no active borrows remain
                if obj_info.borrows.iter().all(|b| b.end_time.is_some()) {
                    obj_info.state = OwnershipState::Owned;
                }
                
                obj_info.last_access = end_time;
                
                // Remove from borrowers
                if let Some(borrowed_objects) = borrowers.get_mut(&borrower) {
                    borrowed_objects.remove(&ptr);
                    if borrowed_objects.is_empty() {
                        borrowers.remove(&borrower);
                    }
                }
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Transfer ownership
    pub fn transfer_ownership(
        &self,
        ptr: NonNull<u8>,
        new_owner: String
    ) -> Result<(), OwnershipError> {
        if let (Ok(mut objects), Ok(mut owners)) = 
            (self.objects.write(), self.owners.write()) {
            
            if let Some(obj_info) = objects.get_mut(&ptr) {
                // Check if object can be moved
                if obj_info.state != OwnershipState::Owned {
                    return Err(OwnershipError::AlreadyBorrowed);
                }
                
                // Remove from old owner
                if let Some(old_owner) = &obj_info.owner {
                    if let Some(owned_objects) = owners.get_mut(old_owner) {
                        owned_objects.remove(&ptr);
                        if owned_objects.is_empty() {
                            owners.remove(old_owner);
                        }
                    }
                }
                
                // Add to new owner
                obj_info.owner = Some(new_owner.clone());
                obj_info.last_access = Instant::now();
                owners.entry(new_owner).or_insert_with(HashSet::new).insert(ptr);
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Mark object as moved
    pub fn mark_moved(&self, ptr: NonNull<u8>) -> Result<(), OwnershipError> {
        if let (Ok(mut objects), Ok(mut stats)) = 
            (self.objects.write(), self.stats.lock()) {
            
            if let Some(obj_info) = objects.get_mut(&ptr) {
                obj_info.state = OwnershipState::Moved;
                obj_info.last_access = Instant::now();
                
                stats.moved_objects += 1;
                stats.owned_objects = stats.owned_objects.saturating_sub(1);
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Mark object as freed
    pub fn mark_freed(&self, ptr: NonNull<u8>) -> Result<(), OwnershipError> {
        if let (Ok(mut objects), Ok(mut owners), Ok(mut borrowers), Ok(mut stats)) = 
            (self.objects.write(), self.owners.write(), self.borrowers.write(), self.stats.lock()) {
            
            if let Some(obj_info) = objects.get_mut(&ptr) {
                obj_info.state = OwnershipState::Freed;
                obj_info.last_access = Instant::now();
                
                // Remove from owners and borrowers
                if let Some(owner) = &obj_info.owner {
                    if let Some(owned_objects) = owners.get_mut(owner) {
                        owned_objects.remove(&ptr);
                        if owned_objects.is_empty() {
                            owners.remove(owner);
                        }
                    }
                }
                
                for borrow in &obj_info.borrows {
                    if let Some(borrowed_objects) = borrowers.get_mut(&borrow.borrower) {
                        borrowed_objects.remove(&ptr);
                        if borrowed_objects.is_empty() {
                            borrowers.remove(&borrow.borrower);
                        }
                    }
                }
                
                stats.freed_objects += 1;
                stats.owned_objects = stats.owned_objects.saturating_sub(1);
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Validate a borrow operation
    fn validate_borrow(&self, ptr: NonNull<u8>, borrow_type: BorrowType) -> Result<(), OwnershipError> {
        if let Ok(objects) = self.objects.read() {
            if let Some(obj_info) = objects.get(&ptr) {
                match obj_info.state {
                    OwnershipState::Moved => return Err(OwnershipError::UseAfterMove),
                    OwnershipState::Freed => return Err(OwnershipError::UseAfterFree),
                    _ => {}
                }
                
                // Check for borrow conflicts
                match borrow_type {
                    BorrowType::Immutable => {
                        if obj_info.borrows.iter().any(|b| b.borrow_type == BorrowType::Mutable && b.end_time.is_none()) {
                            return Err(OwnershipError::MutableBorrowConflict);
                        }
                    },
                    BorrowType::Mutable => {
                        if obj_info.borrows.iter().any(|b| b.end_time.is_none()) {
                            return Err(OwnershipError::AlreadyBorrowed);
                        }
                    }
                }
                
                Ok(())
            } else {
                Err(OwnershipError::InvalidOwner)
            }
        } else {
            Err(OwnershipError::ValidationFailed)
        }
    }
    
    /// Get ownership information for an object
    pub fn get_ownership_info(&self, ptr: NonNull<u8>) -> Option<OwnershipInfo> {
        if let Ok(objects) = self.objects.read() {
            objects.get(&ptr).cloned()
        } else {
            None
        }
    }
    
    /// Get all objects owned by a specific owner
    pub fn get_owned_objects(&self, owner: &str) -> Vec<NonNull<u8>> {
        if let Ok(owners) = self.owners.read() {
            owners.get(owner).map(|set| set.iter().copied().collect()).unwrap_or_default()
        } else {
            Vec::new()
        }
    }
    
    /// Get all objects borrowed by a specific borrower
    pub fn get_borrowed_objects(&self, borrower: &str) -> Vec<NonNull<u8>> {
        if let Ok(borrowers) = self.borrowers.read() {
            borrowers.get(borrower).map(|set| set.iter().copied().collect()).unwrap_or_default()
        } else {
            Vec::new()
        }
    }
    
    /// Get ownership statistics
    pub fn get_stats(&self) -> OwnershipStats {
        self.stats.lock().map(|stats| stats.clone()).unwrap_or_default()
    }
    
    /// Enable or disable ownership validation
    pub fn set_validation_enabled(&self, enabled: bool) {
        if let Ok(mut validation_enabled) = self.validation_enabled.lock() {
            *validation_enabled = enabled;
        }
    }
    
    /// Enable or disable strict mode
    pub fn set_strict_mode(&self, strict: bool) {
        if let Ok(mut strict_mode) = self.strict_mode.lock() {
            *strict_mode = strict;
        }
    }
    
    /// Perform comprehensive ownership validation
    pub fn validate_all(&self) -> Result<Vec<String>, Vec<String>> {
        let start_time = Instant::now();
        let mut warnings = Vec::new();
        let mut errors = Vec::new();
        
        if let Ok(objects) = self.objects.read() {
            for (ptr, obj_info) in objects.iter() {
                // Check for use after move/free
                match obj_info.state {
                    OwnershipState::Moved => {
                        if obj_info.last_access > obj_info.creation_time + Duration::from_secs(1) {
                            warnings.push(format!("Object at {:?} accessed after move", ptr));
                        }
                    },
                    OwnershipState::Freed => {
                        if obj_info.last_access > obj_info.creation_time + Duration::from_secs(1) {
                            errors.push(format!("Object at {:?} accessed after free", ptr));
                        }
                    },
                    _ => {}
                }
                
                // Check for borrow conflicts
                let active_borrows: Vec<&BorrowInfo> = obj_info.borrows.iter().filter(|b| b.end_time.is_none()).collect();
                if active_borrows.len() > 1 {
                    let has_mutable = active_borrows.iter().any(|b| b.borrow_type == BorrowType::Mutable);
                    if has_mutable {
                        errors.push(format!("Object at {:?} has conflicting borrows", ptr));
                    }
                }
                
                // Check for long-lived borrows
                for borrow in &obj_info.borrows {
                    if borrow.end_time.is_none() && borrow.start_time.elapsed() > Duration::from_secs(60) {
                        warnings.push(format!("Long-lived borrow by {} on object at {:?}", borrow.borrower, ptr));
                    }
                }
            }
        }
        
        // Update stats
        if let Ok(mut stats) = self.stats.lock() {
            stats.validation_time_ms = start_time.elapsed().as_millis() as u64;
            stats.borrow_violations += errors.len();
        }
        
        if errors.is_empty() {
            Ok(warnings)
        } else {
            Err(errors)
        }
    }
    
    /// Clean up expired objects and borrows
    pub fn cleanup_expired(&self) {
        let cutoff_time = Instant::now() - Duration::from_secs(3600); // 1 hour
        
        if let (Ok(mut objects), Ok(mut owners), Ok(mut borrowers)) = 
            (self.objects.write(), self.owners.write(), self.borrowers.write()) {
            
            let mut to_remove = Vec::new();
            
            for (ptr, obj_info) in objects.iter_mut() {
                // Remove expired borrows
                obj_info.borrows.retain(|b| {
                    if let Some(end_time) = b.end_time {
                        end_time > cutoff_time
                    } else {
                        b.start_time > cutoff_time
                    }
                });
                
                // Mark old objects for removal if they're freed
                if obj_info.state == OwnershipState::Freed && obj_info.last_access < cutoff_time {
                    to_remove.push(*ptr);
                }
            }
            
            // Remove expired objects
            for ptr in to_remove {
                if let Some(obj_info) = objects.remove(&ptr) {
                    if let Some(owner) = &obj_info.owner {
                        if let Some(owned_objects) = owners.get_mut(owner) {
                            owned_objects.remove(&ptr);
                            if owned_objects.is_empty() {
                                owners.remove(owner);
                            }
                        }
                    }
                    
                    for borrow in &obj_info.borrows {
                        if let Some(borrowed_objects) = borrowers.get_mut(&borrow.borrower) {
                            borrowed_objects.remove(&ptr);
                            if borrowed_objects.is_empty() {
                                borrowers.remove(&borrow.borrower);
                            }
                        }
                    }
                }
            }
        }
    }
}

impl Default for OwnershipTracker {
    fn default() -> Self {
        Self::new()
    }
}

// ============================================================================
// FFI EXPORTS FOR OWNERSHIP TRACKING
// ============================================================================

#[no_mangle]
pub extern "C" fn runa_create_ownership_tracker() -> *mut OwnershipTracker {
    let tracker = Box::new(OwnershipTracker::new());
    Box::into_raw(tracker)
}

#[no_mangle]
pub extern "C" fn runa_register_object(
    tracker: *mut OwnershipTracker,
    ptr: runa_object,
    owner: *const libc::c_char,
    size: usize,
    type_id: *const libc::c_char
) -> bool {
    if tracker.is_null() || ptr.is_null() || owner.is_null() || type_id.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    let non_null_ptr = match NonNull::new(ptr) {
        Some(ptr) => ptr,
        None => return false,
    };
    
    let owner_str = unsafe {
        std::ffi::CStr::from_ptr(owner).to_string_lossy().to_string()
    };
    
    let type_id_str = unsafe {
        std::ffi::CStr::from_ptr(type_id).to_string_lossy().to_string()
    };
    
    let u8_ptr = NonNull::new(non_null_ptr.as_ptr() as *mut u8);
    if let Some(ptr) = u8_ptr {
        tracker.register_object(ptr, owner_str, size, type_id_str).is_ok()
    } else {
        false
    }
}

#[no_mangle]
pub extern "C" fn runa_borrow_immutable(
    tracker: *mut OwnershipTracker,
    ptr: runa_object,
    borrower: *const libc::c_char
) -> bool {
    if tracker.is_null() || ptr.is_null() || borrower.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    let non_null_ptr = match NonNull::new(ptr) {
        Some(ptr) => ptr,
        None => return false,
    };
    
    let borrower_str = unsafe {
        std::ffi::CStr::from_ptr(borrower).to_string_lossy().to_string()
    };
    
    let u8_ptr = NonNull::new(non_null_ptr.as_ptr() as *mut u8);
    if let Some(ptr) = u8_ptr {
        tracker.borrow_immutable(ptr, borrower_str).is_ok()
    } else {
        false
    }
}

#[no_mangle]
pub extern "C" fn runa_borrow_mutable(
    tracker: *mut OwnershipTracker,
    ptr: runa_object,
    borrower: *const libc::c_char
) -> bool {
    if tracker.is_null() || ptr.is_null() || borrower.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    let non_null_ptr = match NonNull::new(ptr) {
        Some(ptr) => ptr,
        None => return false,
    };
    
    let borrower_str = unsafe {
        std::ffi::CStr::from_ptr(borrower).to_string_lossy().to_string()
    };
    
    let u8_ptr = NonNull::new(non_null_ptr.as_ptr() as *mut u8);
    if let Some(ptr) = u8_ptr {
        tracker.borrow_mutable(ptr, borrower_str).is_ok()
    } else {
        false
    }
}

#[no_mangle]
pub extern "C" fn runa_end_borrow(
    tracker: *mut OwnershipTracker,
    ptr: runa_object,
    borrower: *const libc::c_char
) -> bool {
    if tracker.is_null() || ptr.is_null() || borrower.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    let non_null_ptr = match NonNull::new(ptr) {
        Some(ptr) => ptr,
        None => return false,
    };
    
    let borrower_str = unsafe {
        std::ffi::CStr::from_ptr(borrower).to_string_lossy().to_string()
    };
    
    let u8_ptr = NonNull::new(non_null_ptr.as_ptr() as *mut u8);
    if let Some(ptr) = u8_ptr {
        tracker.end_borrow(ptr, borrower_str).is_ok()
    } else {
        false
    }
}

#[no_mangle]
pub extern "C" fn runa_mark_moved(tracker: *mut OwnershipTracker, ptr: runa_object) -> bool {
    if tracker.is_null() || ptr.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    let non_null_ptr = match NonNull::new(ptr) {
        Some(ptr) => ptr,
        None => return false,
    };
    
    let u8_ptr = NonNull::new(non_null_ptr.as_ptr() as *mut u8);
    if let Some(ptr) = u8_ptr {
        tracker.mark_moved(ptr).is_ok()
    } else {
        false
    }
}

#[no_mangle]
pub extern "C" fn runa_mark_freed(tracker: *mut OwnershipTracker, ptr: runa_object) -> bool {
    if tracker.is_null() || ptr.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    let non_null_ptr = match NonNull::new(ptr) {
        Some(ptr) => ptr,
        None => return false,
    };
    
    let u8_ptr = NonNull::new(non_null_ptr.as_ptr() as *mut u8);
    if let Some(ptr) = u8_ptr {
        tracker.mark_freed(ptr).is_ok()
    } else {
        false
    }
}

#[no_mangle]
pub extern "C" fn runa_get_ownership_stats(tracker: *mut OwnershipTracker) -> OwnershipStats {
    if tracker.is_null() {
        return OwnershipStats::default();
    }
    
    let tracker = unsafe { &*tracker };
    tracker.get_stats()
}

#[no_mangle]
pub extern "C" fn runa_validate_ownership(tracker: *mut OwnershipTracker) -> bool {
    if tracker.is_null() {
        return false;
    }
    
    let tracker = unsafe { &*tracker };
    tracker.validate_all().is_ok()
}

#[no_mangle]
pub extern "C" fn runa_cleanup_ownership(tracker: *mut OwnershipTracker) {
    if tracker.is_null() {
        return;
    }
    
    let tracker = unsafe { &*tracker };
    tracker.cleanup_expired();
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::ptr;

    #[test]
    fn test_ownership_registration() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        let result = tracker.register_object(
            ptr,
            "test_owner".to_string(),
            64,
            "TestType".to_string()
        );
        
        assert!(result.is_ok());
        
        let info = tracker.get_ownership_info(ptr);
        assert!(info.is_some());
        
        let info = info.unwrap();
        assert_eq!(info.state, OwnershipState::Owned);
        assert_eq!(info.owner, Some("test_owner".to_string()));
        assert_eq!(info.size, 64);
        assert_eq!(info.type_id, "TestType");
    }
    
    #[test]
    fn test_immutable_borrowing() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        tracker.register_object(ptr, "owner".to_string(), 64, "TestType".to_string()).unwrap();
        
        // Multiple immutable borrows should work
        assert!(tracker.borrow_immutable(ptr, "borrower1".to_string()).is_ok());
        assert!(tracker.borrow_immutable(ptr, "borrower2".to_string()).is_ok());
        
        let info = tracker.get_ownership_info(ptr).unwrap();
        assert_eq!(info.state, OwnershipState::Borrowed);
        assert_eq!(info.borrows.len(), 2);
    }
    
    #[test]
    fn test_mutable_borrow_conflicts() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        tracker.register_object(ptr, "owner".to_string(), 64, "TestType".to_string()).unwrap();
        
        // Mutable borrow should work first
        assert!(tracker.borrow_mutable(ptr, "borrower1".to_string()).is_ok());
        
        // Second mutable borrow should fail
        assert!(tracker.borrow_mutable(ptr, "borrower2".to_string()).is_err());
        
        // Immutable borrow should also fail
        assert!(tracker.borrow_immutable(ptr, "borrower3".to_string()).is_err());
    }
    
    #[test]
    fn test_ownership_transfer() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        tracker.register_object(ptr, "owner1".to_string(), 64, "TestType".to_string()).unwrap();
        
        assert!(tracker.transfer_ownership(ptr, "owner2".to_string()).is_ok());
        
        let info = tracker.get_ownership_info(ptr).unwrap();
        assert_eq!(info.owner, Some("owner2".to_string()));
        
        let owned_by_1 = tracker.get_owned_objects("owner1");
        let owned_by_2 = tracker.get_owned_objects("owner2");
        
        assert!(owned_by_1.is_empty());
        assert_eq!(owned_by_2.len(), 1);
        assert_eq!(owned_by_2[0], ptr);
    }
    
    #[test]
    fn test_use_after_move() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        tracker.register_object(ptr, "owner".to_string(), 64, "TestType".to_string()).unwrap();
        tracker.mark_moved(ptr).unwrap();
        
        // Borrowing after move should fail
        assert!(tracker.borrow_immutable(ptr, "borrower".to_string()).is_err());
        assert!(tracker.borrow_mutable(ptr, "borrower".to_string()).is_err());
    }
    
    #[test]
    fn test_use_after_free() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        tracker.register_object(ptr, "owner".to_string(), 64, "TestType".to_string()).unwrap();
        tracker.mark_freed(ptr).unwrap();
        
        // Borrowing after free should fail
        assert!(tracker.borrow_immutable(ptr, "borrower".to_string()).is_err());
        assert!(tracker.borrow_mutable(ptr, "borrower".to_string()).is_err());
    }
    
    #[test]
    fn test_validation() {
        let tracker = OwnershipTracker::new();
        let ptr = NonNull::new(ptr::null_mut::<u8>().wrapping_add(0x1000)).unwrap();
        
        tracker.register_object(ptr, "owner".to_string(), 64, "TestType".to_string()).unwrap();
        
        // Validation should pass for clean state
        let result = tracker.validate_all();
        assert!(result.is_ok());
        
        // Create a conflict
        tracker.borrow_mutable(ptr, "borrower1".to_string()).unwrap();
        tracker.set_validation_enabled(false);
        tracker.borrow_immutable(ptr, "borrower2".to_string()).unwrap();
        
        // Validation should detect the conflict
        let result = tracker.validate_all();
        assert!(result.is_err());
    }
}