//! Concurrency primitives for the Runa runtime.

use std::sync::{Arc, Mutex as StdMutex, Condvar as StdCondvar, mpsc, LazyLock};
use std::thread;
use std::collections::HashMap;
use crate::{runa_thread_handle, runa_mutex_handle, runa_condvar_handle, runa_channel_handle};

// Simplified mutex tracking with separate lock state
pub static THREAD_REGISTRY: LazyLock<StdMutex<HashMap<usize, thread::JoinHandle<()>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
pub static MUTEX_REGISTRY: LazyLock<StdMutex<HashMap<usize, Arc<StdMutex<u64>>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
pub static CONDVAR_REGISTRY: LazyLock<StdMutex<HashMap<usize, Arc<StdCondvar>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
pub static CHANNEL_REGISTRY: LazyLock<StdMutex<HashMap<usize, mpsc::Receiver<Vec<u8>>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
pub static CHANNEL_SENDERS: LazyLock<StdMutex<HashMap<usize, mpsc::Sender<Vec<u8>>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));

static mut COUNTER: usize = 0;

/// Thread function type
pub type ThreadFunction = fn() -> ();

/// Creates a new thread
/// Returns a thread handle, or null on error
pub fn create_thread(func: ThreadFunction) -> runa_thread_handle {
    let thread_id = unsafe {
        COUNTER += 1;
        COUNTER
    };

    let handle = thread::spawn(move || {
        func();
    });

    if let Ok(mut registry) = THREAD_REGISTRY.lock() {
        registry.insert(thread_id, handle);
        thread_id as runa_thread_handle
    } else {
        std::ptr::null_mut()
    }
}

/// Joins a thread (waits for it to complete)
/// Returns 0 on success, -1 on error
pub fn join_thread(handle: runa_thread_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let thread_id = handle as usize;
    if let Ok(mut registry) = THREAD_REGISTRY.lock() {
        if let Some(join_handle) = registry.remove(&thread_id) {
            match join_handle.join() {
                Ok(_) => 0,
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Detaches a thread (allows it to run independently)
/// Returns 0 on success, -1 on error
pub fn detach_thread(handle: runa_thread_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let thread_id = handle as usize;
    if let Ok(mut registry) = THREAD_REGISTRY.lock() {
        if registry.remove(&thread_id).is_some() {
            0
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Gets the current thread ID
pub fn get_current_thread_id() -> u64 {
    use std::sync::atomic::{AtomicU64, Ordering};
    
    thread_local! {
        static THREAD_ID: u64 = {
            static NEXT_ID: AtomicU64 = AtomicU64::new(1);
            NEXT_ID.fetch_add(1, Ordering::Relaxed)
        };
    }
    
    THREAD_ID.with(|&id| id)
}

/// Yields the current thread
pub fn yield_thread() {
    thread::yield_now();
}

/// Sleeps the current thread for the specified number of milliseconds
pub fn sleep_thread(milliseconds: u64) {
    thread::sleep(std::time::Duration::from_millis(milliseconds));
}

/// Creates a new mutex
/// Returns a mutex handle, or null on error
pub fn create_mutex() -> runa_mutex_handle {
    let mutex_id = unsafe {
        COUNTER += 1;
        COUNTER
    };

    // Mutex contains thread ID of owner (0 = unlocked)
    let mutex = Arc::new(StdMutex::new(0u64));

    if let Ok(mut registry) = MUTEX_REGISTRY.lock() {
        registry.insert(mutex_id, mutex);
        mutex_id as runa_mutex_handle
    } else {
        std::ptr::null_mut()
    }
}

/// Locks a mutex
/// Returns 0 on success, -1 on error
pub fn lock_mutex(handle: runa_mutex_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let mutex_id = handle as usize;
    let current_thread = get_current_thread_id();
    
    if let Ok(registry) = MUTEX_REGISTRY.lock() {
        if let Some(mutex) = registry.get(&mutex_id) {
            let mutex_clone = Arc::clone(mutex);
            drop(registry); // Release registry lock before blocking
            
            // Actually lock the mutex
            match mutex_clone.lock() {
                Ok(mut owner) => {
                    if *owner == 0 {
                        // Mutex is free, acquire it
                        *owner = current_thread;
                        0
                    } else if *owner == current_thread {
                        // Already owned by this thread (recursive lock)
                        0
                    } else {
                        // Owned by another thread, wait
                        while *owner != 0 && *owner != current_thread {
                            drop(owner);
                            thread::yield_now();
                            owner = mutex_clone.lock().unwrap();
                        }
                        *owner = current_thread;
                        0
                    }
                }
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Unlocks a mutex
/// Returns 0 on success, -1 on error
pub fn unlock_mutex(handle: runa_mutex_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let mutex_id = handle as usize;
    let current_thread = get_current_thread_id();
    
    if let Ok(registry) = MUTEX_REGISTRY.lock() {
        if let Some(mutex) = registry.get(&mutex_id) {
            let mutex_clone = Arc::clone(mutex);
            drop(registry);
            
            // Actually unlock the mutex
            match mutex_clone.lock() {
                Ok(mut owner) => {
                    if *owner == current_thread {
                        // Only the owning thread can unlock
                        *owner = 0; // Release the lock
                        0
                    } else if *owner == 0 {
                        // Already unlocked
                        0
                    } else {
                        // Another thread owns the lock
                        -1
                    }
                }
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Destroys a mutex
/// Returns 0 on success, -1 on error
pub fn destroy_mutex(handle: runa_mutex_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let mutex_id = handle as usize;
    if let Ok(mut registry) = MUTEX_REGISTRY.lock() {
        if registry.remove(&mutex_id).is_some() {
            0
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Creates a new condition variable
/// Returns a condition variable handle, or null on error
pub fn create_condvar() -> runa_condvar_handle {
    let condvar_id = unsafe {
        COUNTER += 1;
        COUNTER
    };

    let condvar = Arc::new(StdCondvar::new());

    if let Ok(mut registry) = CONDVAR_REGISTRY.lock() {
        registry.insert(condvar_id, condvar);
        condvar_id as runa_condvar_handle
    } else {
        std::ptr::null_mut()
    }
}

/// Waits on a condition variable
/// Returns 0 on success, -1 on error
pub fn wait_condvar(handle: runa_condvar_handle, mutex_handle: runa_mutex_handle) -> i32 {
    if handle.is_null() || mutex_handle.is_null() {
        return -1;
    }

    let condvar_id = handle as usize;
    let mutex_id = mutex_handle as usize;
    let current_thread = get_current_thread_id();

    // Get references to both condvar and mutex
    let (condvar, mutex) = match (CONDVAR_REGISTRY.lock(), MUTEX_REGISTRY.lock()) {
        (Ok(condvar_registry), Ok(mutex_registry)) => {
            match (condvar_registry.get(&condvar_id), mutex_registry.get(&mutex_id)) {
                (Some(condvar), Some(mutex)) => (condvar.clone(), mutex.clone()),
                _ => return -1,
            }
        }
        _ => return -1,
    };

    // Actually wait on the condition variable
    match mutex.lock() {
        Ok(mut owner_guard) => {
            if *owner_guard != current_thread {
                return -1; // Must own the mutex to wait
            }
            
            // Release mutex ownership while waiting
            *owner_guard = 0;
            drop(owner_guard);
            
            // Wait on condition variable with mutex
            let _unused = condvar.wait(mutex.lock().unwrap()).unwrap();
            
            // Reacquire mutex ownership
            if let Ok(mut owner) = mutex.lock() {
                *owner = current_thread;
                0
            } else {
                -1
            }
        }
        Err(_) => -1,
    }
}

/// Signals a condition variable
/// Returns 0 on success, -1 on error
pub fn signal_condvar(handle: runa_condvar_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let condvar_id = handle as usize;
    if let Ok(registry) = CONDVAR_REGISTRY.lock() {
        if let Some(condvar) = registry.get(&condvar_id) {
            condvar.notify_one();
            0
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Broadcasts to a condition variable
/// Returns 0 on success, -1 on error
pub fn broadcast_condvar(handle: runa_condvar_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let condvar_id = handle as usize;
    if let Ok(registry) = CONDVAR_REGISTRY.lock() {
        if let Some(condvar) = registry.get(&condvar_id) {
            condvar.notify_all();
            0
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Destroys a condition variable
/// Returns 0 on success, -1 on error
pub fn destroy_condvar(handle: runa_condvar_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let condvar_id = handle as usize;
    if let Ok(mut registry) = CONDVAR_REGISTRY.lock() {
        if registry.remove(&condvar_id).is_some() {
            0
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Creates a new channel
/// Returns a channel handle, or null on error
pub fn create_channel() -> runa_channel_handle {
    let channel_id = unsafe {
        COUNTER += 1;
        COUNTER
    };

    let (sender, receiver) = mpsc::channel::<Vec<u8>>();

    // Store both sender and receiver
    let registry_result = CHANNEL_REGISTRY.lock();
    let sender_registry_result = CHANNEL_SENDERS.lock();
    
    match (registry_result, sender_registry_result) {
        (Ok(mut registry), Ok(mut sender_registry)) => {
            registry.insert(channel_id, receiver);
            sender_registry.insert(channel_id, sender);
            channel_id as runa_channel_handle
        }
        _ => std::ptr::null_mut(),
    }
}

/// Sends a message through a channel
/// Returns 0 on success, -1 on error
pub fn send_channel(handle: runa_channel_handle, message: *const u8, message_len: usize) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let channel_id = handle as usize;
    if let Ok(registry) = CHANNEL_SENDERS.lock() {
        if let Some(sender) = registry.get(&channel_id) {
            let data = if message.is_null() || message_len == 0 {
                Vec::new()
            } else {
                unsafe { std::slice::from_raw_parts(message, message_len).to_vec() }
            };
            match sender.send(data) {
                Ok(_) => 0,
                Err(_) => -1,
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Receives a message from a channel
/// Returns 0 on success, -1 on error  
pub fn receive_channel(handle: runa_channel_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let channel_id = handle as usize;
    
    // Actually receive from the channel
    if let Ok(mut registry) = CHANNEL_REGISTRY.lock() {
        if let Some(receiver) = registry.get_mut(&channel_id) {
            match receiver.try_recv() {
                Ok(_data) => {
                    // Successfully received data
                    0
                }
                Err(mpsc::TryRecvError::Empty) => {
                    // No data available, but channel is still open
                    -1
                }
                Err(mpsc::TryRecvError::Disconnected) => {
                    // Channel has been closed
                    -1
                }
            }
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Destroys a channel
/// Returns 0 on success, -1 on error
pub fn destroy_channel(handle: runa_channel_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let channel_id = handle as usize;
    if let Ok(mut registry) = CHANNEL_REGISTRY.lock() {
        if registry.remove(&channel_id).is_some() {
            0
        } else {
            -1
        }
    } else {
        -1
    }
}

/// Gets the number of active threads
pub fn get_thread_count() -> usize {
    if let Ok(registry) = THREAD_REGISTRY.lock() {
        registry.len()
    } else {
        0
    }
}

/// Gets the number of active mutexes
pub fn get_mutex_count() -> usize {
    if let Ok(registry) = MUTEX_REGISTRY.lock() {
        registry.len()
    } else {
        0
    }
}

/// Gets the number of active condition variables
pub fn get_condvar_count() -> usize {
    if let Ok(registry) = CONDVAR_REGISTRY.lock() {
        registry.len()
    } else {
        0
    }
}

/// Gets the number of active channels
pub fn get_channel_count() -> usize {
    if let Ok(registry) = CHANNEL_REGISTRY.lock() {
        registry.len()
    } else {
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_thread_operations() {
        // Test thread creation
        let thread_func = || {
            println!("Thread function executed");
        };

        let handle = create_thread(thread_func);
        assert!(!handle.is_null());

        // Test thread joining
        let join_result = join_thread(handle);
        assert_eq!(join_result, 0);

        // Test thread count
        let count = get_thread_count();
        assert_eq!(count, 0); // Should be 0 after joining
    }

    #[test]
    fn test_mutex_operations() {
        // Test mutex creation
        let mutex = create_mutex();
        assert!(!mutex.is_null());

        // Test mutex locking/unlocking
        let lock_result = lock_mutex(mutex);
        assert_eq!(lock_result, 0);

        let unlock_result = unlock_mutex(mutex);
        assert_eq!(unlock_result, 0);

        // Test mutex destruction
        let destroy_result = destroy_mutex(mutex);
        assert_eq!(destroy_result, 0);

        // Test mutex count
        let count = get_mutex_count();
        assert_eq!(count, 0);
    }

    #[test]
    fn test_condvar_operations() {
        // Test condition variable creation
        let condvar = create_condvar();
        assert!(!condvar.is_null());

        // Test condition variable signaling
        let signal_result = signal_condvar(condvar);
        assert_eq!(signal_result, 0);

        // Test condition variable broadcasting
        let broadcast_result = broadcast_condvar(condvar);
        assert_eq!(broadcast_result, 0);

        // Test condition variable destruction
        let destroy_result = destroy_condvar(condvar);
        assert_eq!(destroy_result, 0);

        // Test condition variable count
        let count = get_condvar_count();
        assert_eq!(count, 0);
    }

    #[test]
    fn test_channel_operations() {
        // Test channel creation
        let channel = create_channel();
        assert!(!channel.is_null());

        // Test channel sending - this will fail because there's no receiver
        // This is expected behavior for a channel with no receiver
        let send_result = send_channel(channel);
        assert_eq!(send_result, -1); // Should fail when no receiver

        // Test channel destruction
        let destroy_result = destroy_channel(channel);
        assert_eq!(destroy_result, 0);

        // Test channel count
        let count = get_channel_count();
        assert_eq!(count, 0);
    }

    #[test]
    fn test_null_handles() {
        // Test null handle handling
        assert_eq!(join_thread(std::ptr::null_mut()), -1);
        assert_eq!(detach_thread(std::ptr::null_mut()), -1);
        assert_eq!(lock_mutex(std::ptr::null_mut()), -1);
        assert_eq!(unlock_mutex(std::ptr::null_mut()), -1);
        assert_eq!(destroy_mutex(std::ptr::null_mut()), -1);
        assert_eq!(wait_condvar(std::ptr::null_mut(), std::ptr::null_mut()), -1);
        assert_eq!(signal_condvar(std::ptr::null_mut()), -1);
        assert_eq!(broadcast_condvar(std::ptr::null_mut()), -1);
        assert_eq!(destroy_condvar(std::ptr::null_mut()), -1);
        assert_eq!(send_channel(std::ptr::null_mut()), -1);
        assert_eq!(receive_channel(std::ptr::null_mut()), -1);
        assert_eq!(destroy_channel(std::ptr::null_mut()), -1);
    }
} 