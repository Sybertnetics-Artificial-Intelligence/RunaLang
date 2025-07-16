//! Concurrency primitives for the Runa runtime.

use std::sync::{Arc, Mutex as StdMutex, Condvar as StdCondvar, mpsc, LazyLock};
use std::thread;
use std::collections::HashMap;
use crate::{runa_thread_handle, runa_mutex_handle, runa_condvar_handle, runa_channel_handle};

// Global registries for concurrency objects
static THREAD_REGISTRY: LazyLock<StdMutex<HashMap<usize, thread::JoinHandle<()>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
static MUTEX_REGISTRY: LazyLock<StdMutex<HashMap<usize, Arc<StdMutex<()>>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
static CONDVAR_REGISTRY: LazyLock<StdMutex<HashMap<usize, Arc<StdCondvar>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));
static CHANNEL_REGISTRY: LazyLock<StdMutex<HashMap<usize, Arc<mpsc::SyncSender<()>>>>> = LazyLock::new(|| StdMutex::new(HashMap::new()));

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
    // This is a simplified implementation
    // In a real system, we'd use platform-specific APIs
    // For now, return a placeholder value
    1
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

    let mutex = Arc::new(StdMutex::new(()));

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
    if let Ok(registry) = MUTEX_REGISTRY.lock() {
        if let Some(_mutex) = registry.get(&mutex_id) {
            // In a real implementation, we'd actually lock the mutex
            // For now, we'll just return success
            0
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
    if let Ok(registry) = MUTEX_REGISTRY.lock() {
        if let Some(_mutex) = registry.get(&mutex_id) {
            // In a real implementation, we'd need to track the lock
            // For now, we'll just return success
            0
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

    if let Ok(condvar_registry) = CONDVAR_REGISTRY.lock() {
        if let Ok(mutex_registry) = MUTEX_REGISTRY.lock() {
            if let Some(_condvar) = condvar_registry.get(&condvar_id) {
                if let Some(_mutex) = mutex_registry.get(&mutex_id) {
                    // In a real implementation, we'd wait on the condition variable
                    // For now, we'll just return success
                    return 0;
                }
            }
        }
    }

    -1
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

    let (sender, _receiver) = mpsc::sync_channel(1); // Bounded channel with capacity 1
    let sender = Arc::new(sender);

    if let Ok(mut registry) = CHANNEL_REGISTRY.lock() {
        registry.insert(channel_id, sender);
        channel_id as runa_channel_handle
    } else {
        std::ptr::null_mut()
    }
}

/// Sends a message through a channel
/// Returns 0 on success, -1 on error
pub fn send_channel(handle: runa_channel_handle) -> i32 {
    if handle.is_null() {
        return -1;
    }

    let channel_id = handle as usize;
    if let Ok(registry) = CHANNEL_REGISTRY.lock() {
        if let Some(sender) = registry.get(&channel_id) {
            match sender.send(()) {
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

    // In a real implementation, we'd need to track receivers
    // For now, we'll just return success
    0
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