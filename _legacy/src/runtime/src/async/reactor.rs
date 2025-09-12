// High-Performance IO Reactor for Async Operations
// Cross-platform IO event handling with epoll/kqueue/IOCP backends

use std::sync::{Arc, Mutex, RwLock};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use std::thread;
use std::io;
use crossbeam_channel::{unbounded, Receiver, Sender};

use super::{AsyncError, WakerId};

/// Cross-platform IO reactor for async operations
#[derive(Debug)]
pub struct Reactor {
    backend: Box<dyn ReactorBackend>,
    registrations: Arc<RwLock<HashMap<IoToken, IoRegistration>>>,
    waker_queue: Sender<WakerId>,
    waker_receiver: Receiver<WakerId>,
    running: AtomicBool,
    poll_thread: Mutex<Option<thread::JoinHandle<()>>>,
    metrics: Arc<ReactorMetrics>,
    next_token: AtomicUsize,
}

impl Reactor {
    /// Create new reactor with platform-optimized backend
    pub fn new() -> Result<Self, AsyncError> {
        let backend = Self::create_backend()?;
        let (waker_queue, waker_receiver) = unbounded();
        let registrations = Arc::new(RwLock::new(HashMap::new()));
        let metrics = Arc::new(ReactorMetrics::new());

        Ok(Self {
            backend,
            registrations,
            waker_queue,
            waker_receiver,
            running: AtomicBool::new(false),
            poll_thread: Mutex::new(None),
            metrics,
            next_token: AtomicUsize::new(1),
        })
    }

    /// Start the reactor
    pub fn start(&self) -> Result<(), AsyncError> {
        if self.running.load(Ordering::Acquire) {
            return Err(AsyncError::AlreadyRunning);
        }

        self.running.store(true, Ordering::Release);

        // Start polling thread
        let backend = self.backend.clone_backend();
        let registrations = self.registrations.clone();
        let waker_queue = self.waker_queue.clone();
        let running = self.running.clone();
        let metrics = self.metrics.clone();

        let handle = thread::Builder::new()
            .name("runa-async-reactor".to_string())
            .spawn(move || {
                Self::poll_loop(backend, registrations, waker_queue, running, metrics);
            })
            .map_err(|e| AsyncError::ThreadError(e.to_string()))?;

        if let Ok(mut thread_guard) = self.poll_thread.lock() {
            *thread_guard = Some(handle);
        }

        Ok(())
    }

    /// Stop the reactor
    pub fn stop(&self) -> Result<(), AsyncError> {
        self.running.store(false, Ordering::Release);

        // Wake up the polling thread
        self.backend.interrupt()?;

        if let Ok(mut thread_guard) = self.poll_thread.lock() {
            if let Some(handle) = thread_guard.take() {
                handle.join().map_err(|_| AsyncError::ThreadError("Failed to join reactor thread".to_string()))?;
            }
        }

        Ok(())
    }

    /// Register IO interest for a file descriptor
    pub fn register(&self, fd: RawFd, interest: IoInterest) -> Result<IoToken, AsyncError> {
        let token = IoToken(self.next_token.fetch_add(1, Ordering::Relaxed));
        
        // Register with backend
        self.backend.register(fd, token, interest)?;

        // Store registration
        let registration = IoRegistration {
            fd,
            token,
            interest,
            registered_at: Instant::now(),
        };

        if let Ok(mut registrations) = self.registrations.write() {
            registrations.insert(token, registration);
        }

        self.metrics.registrations.fetch_add(1, Ordering::Relaxed);
        Ok(token)
    }

    /// Unregister IO interest
    pub fn unregister(&self, token: IoToken) -> Result<(), AsyncError> {
        // Remove from backend
        self.backend.unregister(token)?;

        // Remove registration
        if let Ok(mut registrations) = self.registrations.write() {
            registrations.remove(&token);
        }

        self.metrics.unregistrations.fetch_add(1, Ordering::Relaxed);
        Ok(())
    }

    /// Poll for ready IO events
    pub fn poll(&self, timeout: Duration) -> Result<Vec<WakerId>, AsyncError> {
        let mut ready_wakers = Vec::new();
        let deadline = Instant::now() + timeout;

        while Instant::now() < deadline {
            match self.waker_receiver.try_recv() {
                Ok(waker_id) => ready_wakers.push(waker_id),
                Err(_) => break,
            }
        }

        Ok(ready_wakers)
    }

    /// Get reactor statistics
    pub fn stats(&self) -> ReactorStats {
        let active_registrations = if let Ok(registrations) = self.registrations.read() {
            registrations.len()
        } else {
            0
        };

        ReactorStats {
            active_registrations,
            registrations: self.metrics.registrations.load(Ordering::Relaxed),
            unregistrations: self.metrics.unregistrations.load(Ordering::Relaxed),
            events_processed: self.metrics.events_processed.load(Ordering::Relaxed),
            poll_cycles: self.metrics.poll_cycles.load(Ordering::Relaxed),
        }
    }

    fn create_backend() -> Result<Box<dyn ReactorBackend>, AsyncError> {
        #[cfg(target_os = "linux")]
        {
            Ok(Box::new(EpollBackend::new()?))
        }
        #[cfg(any(target_os = "macos", target_os = "freebsd", target_os = "openbsd"))]
        {
            Ok(Box::new(KqueueBackend::new()?))
        }
        #[cfg(target_os = "windows")]
        {
            Ok(Box::new(IocpBackend::new()?))
        }
        #[cfg(not(any(target_os = "linux", target_os = "macos", target_os = "freebsd", target_os = "openbsd", target_os = "windows")))]
        {
            Ok(Box::new(FallbackBackend::new()?))
        }
    }

    fn poll_loop(
        mut backend: Box<dyn ReactorBackend>,
        registrations: Arc<RwLock<HashMap<IoToken, IoRegistration>>>,
        waker_queue: Sender<WakerId>,
        running: Arc<AtomicBool>,
        metrics: Arc<ReactorMetrics>,
    ) {
        let mut events = Vec::with_capacity(1024);

        while running.load(Ordering::Acquire) {
            events.clear();

            // Poll for events
            match backend.poll(&mut events, Duration::from_millis(10)) {
                Ok(_) => {
                    metrics.poll_cycles.fetch_add(1, Ordering::Relaxed);
                    
                    for event in &events {
                        // Process IO event
                        if let Ok(registrations_guard) = registrations.read() {
                            if let Some(_registration) = registrations_guard.get(&event.token) {
                                // Create waker for this event
                                let waker_id = WakerId::new();
                                let _ = waker_queue.try_send(waker_id);
                                
                                metrics.events_processed.fetch_add(1, Ordering::Relaxed);
                            }
                        }
                    }
                }
                Err(_) => {
                    // Error in polling, back off briefly
                    thread::sleep(Duration::from_millis(1));
                }
            }
        }
    }
}

/// IO event token for identifying registrations
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct IoToken(usize);

/// IO interest flags
#[derive(Debug, Clone, Copy)]
pub struct IoInterest {
    pub readable: bool,
    pub writable: bool,
    pub edge_triggered: bool,
}

impl IoInterest {
    pub const READABLE: Self = Self { readable: true, writable: false, edge_triggered: false };
    pub const WRITABLE: Self = Self { readable: false, writable: true, edge_triggered: false };
    pub const READ_WRITE: Self = Self { readable: true, writable: true, edge_triggered: false };

    pub fn readable() -> Self {
        Self::READABLE
    }

    pub fn writable() -> Self {
        Self::WRITABLE
    }

    pub fn read_write() -> Self {
        Self::READ_WRITE
    }

    pub fn edge_triggered(mut self) -> Self {
        self.edge_triggered = true;
        self
    }
}

/// IO registration information
#[derive(Debug, Clone)]
struct IoRegistration {
    fd: RawFd,
    token: IoToken,
    interest: IoInterest,
    registered_at: Instant,
}

/// IO event from reactor backend
#[derive(Debug, Clone)]
pub struct IoEvent {
    pub token: IoToken,
    pub readable: bool,
    pub writable: bool,
    pub error: bool,
    pub hang_up: bool,
}

/// Platform-specific raw file descriptor
#[cfg(unix)]
pub type RawFd = std::os::unix::io::RawFd;
#[cfg(windows)]
pub type RawFd = std::os::windows::io::RawSocket;

/// Trait for platform-specific reactor backends
trait ReactorBackend: Send + Sync {
    fn register(&self, fd: RawFd, token: IoToken, interest: IoInterest) -> Result<(), AsyncError>;
    fn unregister(&self, token: IoToken) -> Result<(), AsyncError>;
    fn poll(&mut self, events: &mut Vec<IoEvent>, timeout: Duration) -> Result<usize, AsyncError>;
    fn interrupt(&self) -> Result<(), AsyncError>;
    fn clone_backend(&self) -> Box<dyn ReactorBackend>;
}

/// Linux epoll-based reactor backend
#[cfg(target_os = "linux")]
#[derive(Debug)]
struct EpollBackend {
    epoll_fd: RawFd,
    interrupt_fd: RawFd,
    registrations: Arc<RwLock<HashMap<IoToken, RawFd>>>,
}

#[cfg(target_os = "linux")]
impl EpollBackend {
    fn new() -> Result<Self, AsyncError> {
        use std::os::unix::io::AsRawFd;

        let epoll_fd = unsafe { libc::epoll_create1(libc::EPOLL_CLOEXEC) };
        if epoll_fd < 0 {
            return Err(AsyncError::ReactorError("Failed to create epoll".to_string()));
        }

        // Create eventfd for interrupting
        let interrupt_fd = unsafe { libc::eventfd(0, libc::EFD_CLOEXEC | libc::EFD_NONBLOCK) };
        if interrupt_fd < 0 {
            unsafe { libc::close(epoll_fd); }
            return Err(AsyncError::ReactorError("Failed to create interrupt fd".to_string()));
        }

        // Register interrupt fd
        let mut event = libc::epoll_event {
            events: libc::EPOLLIN as u32,
            u64: usize::MAX as u64, // Special token for interrupt
        };

        if unsafe { libc::epoll_ctl(epoll_fd, libc::EPOLL_CTL_ADD, interrupt_fd, &mut event) } < 0 {
            unsafe { 
                libc::close(epoll_fd);
                libc::close(interrupt_fd);
            }
            return Err(AsyncError::ReactorError("Failed to register interrupt fd".to_string()));
        }

        Ok(Self {
            epoll_fd,
            interrupt_fd,
            registrations: Arc::new(RwLock::new(HashMap::new())),
        })
    }
}

#[cfg(target_os = "linux")]
impl ReactorBackend for EpollBackend {
    fn register(&self, fd: RawFd, token: IoToken, interest: IoInterest) -> Result<(), AsyncError> {
        let mut events = 0u32;
        
        if interest.readable {
            events |= libc::EPOLLIN as u32;
        }
        if interest.writable {
            events |= libc::EPOLLOUT as u32;
        }
        if interest.edge_triggered {
            events |= libc::EPOLLET as u32;
        }

        let mut event = libc::epoll_event {
            events,
            u64: token.0 as u64,
        };

        if unsafe { libc::epoll_ctl(self.epoll_fd, libc::EPOLL_CTL_ADD, fd, &mut event) } < 0 {
            return Err(AsyncError::ReactorError("Failed to register fd with epoll".to_string()));
        }

        if let Ok(mut registrations) = self.registrations.write() {
            registrations.insert(token, fd);
        }

        Ok(())
    }

    fn unregister(&self, token: IoToken) -> Result<(), AsyncError> {
        if let Ok(mut registrations) = self.registrations.write() {
            if let Some(fd) = registrations.remove(&token) {
                if unsafe { libc::epoll_ctl(self.epoll_fd, libc::EPOLL_CTL_DEL, fd, std::ptr::null_mut()) } < 0 {
                    return Err(AsyncError::ReactorError("Failed to unregister fd from epoll".to_string()));
                }
            }
        }

        Ok(())
    }

    fn poll(&mut self, events: &mut Vec<IoEvent>, timeout: Duration) -> Result<usize, AsyncError> {
        const MAX_EVENTS: usize = 1024;
        let mut epoll_events = [libc::epoll_event { events: 0, u64: 0 }; MAX_EVENTS];
        
        let timeout_ms = timeout.as_millis().min(i32::MAX as u128) as i32;
        
        let num_events = unsafe {
            libc::epoll_wait(
                self.epoll_fd,
                epoll_events.as_mut_ptr(),
                MAX_EVENTS as i32,
                timeout_ms,
            )
        };

        if num_events < 0 {
            return Err(AsyncError::ReactorError("Epoll wait failed".to_string()));
        }

        for i in 0..num_events as usize {
            let event = &epoll_events[i];
            
            // Skip interrupt events
            if event.u64 == usize::MAX as u64 {
                continue;
            }

            let io_event = IoEvent {
                token: IoToken(event.u64 as usize),
                readable: (event.events & libc::EPOLLIN as u32) != 0,
                writable: (event.events & libc::EPOLLOUT as u32) != 0,
                error: (event.events & libc::EPOLLERR as u32) != 0,
                hang_up: (event.events & libc::EPOLLHUP as u32) != 0,
            };

            events.push(io_event);
        }

        Ok(num_events as usize)
    }

    fn interrupt(&self) -> Result<(), AsyncError> {
        let value: u64 = 1;
        if unsafe { libc::write(self.interrupt_fd, &value as *const u64 as *const libc::c_void, 8) } != 8 {
            return Err(AsyncError::ReactorError("Failed to interrupt reactor".to_string()));
        }
        Ok(())
    }

    fn clone_backend(&self) -> Box<dyn ReactorBackend> {
        // Clone the epoll file descriptor for shared access
        let cloned_epoll_fd = unsafe {
            libc::dup(self.epoll_fd)
        };
        
        if cloned_epoll_fd == -1 {
            // Fallback to creating new backend if dup fails
            Box::new(EpollBackend::new().unwrap())
        } else {
            Box::new(EpollBackend {
                epoll_fd: cloned_epoll_fd,
                events: Vec::with_capacity(1024),
                registered_fds: std::collections::HashMap::new(),
            })
        }
    }
}

#[cfg(target_os = "linux")]
impl Drop for EpollBackend {
    fn drop(&mut self) {
        unsafe {
            libc::close(self.epoll_fd);
            libc::close(self.interrupt_fd);
        }
    }
}

/// macOS/BSD kqueue-based reactor backend
#[cfg(any(target_os = "macos", target_os = "freebsd", target_os = "openbsd"))]
#[derive(Debug)]
struct KqueueBackend {
    kqueue_fd: RawFd,
}

#[cfg(any(target_os = "macos", target_os = "freebsd", target_os = "openbsd"))]
impl KqueueBackend {
    fn new() -> Result<Self, AsyncError> {
        let kqueue_fd = unsafe { libc::kqueue() };
        if kqueue_fd < 0 {
            return Err(AsyncError::ReactorError("Failed to create kqueue".to_string()));
        }

        Ok(Self { kqueue_fd })
    }
}

#[cfg(any(target_os = "macos", target_os = "freebsd", target_os = "openbsd"))]
impl ReactorBackend for KqueueBackend {
    fn register(&self, fd: RawFd, token: IoToken, interest: IoInterest) -> Result<(), AsyncError> {
        let mut changes = Vec::new();

        if interest.readable {
            let mut kevent = libc::kevent {
                ident: fd as usize,
                filter: libc::EVFILT_READ,
                flags: libc::EV_ADD | libc::EV_ENABLE,
                fflags: 0,
                data: 0,
                udata: token.0 as *mut libc::c_void,
            };
            changes.push(kevent);
        }

        if interest.writable {
            let mut kevent = libc::kevent {
                ident: fd as usize,
                filter: libc::EVFILT_WRITE,
                flags: libc::EV_ADD | libc::EV_ENABLE,
                fflags: 0,
                data: 0,
                udata: token.0 as *mut libc::c_void,
            };
            changes.push(kevent);
        }

        if unsafe {
            libc::kevent(
                self.kqueue_fd,
                changes.as_ptr(),
                changes.len() as i32,
                std::ptr::null_mut(),
                0,
                std::ptr::null(),
            )
        } < 0 {
            return Err(AsyncError::ReactorError("Failed to register with kqueue".to_string()));
        }

        Ok(())
    }

    fn unregister(&self, token: IoToken) -> Result<(), AsyncError> {
        // Find and remove the file descriptor associated with this token
        if let Some(fd) = self.token_to_fd.get(&token) {
            let fd = *fd;
            
            // Create kevent to delete the registration
            let mut kevent = libc::kevent {
                ident: fd as usize,
                filter: libc::EVFILT_READ,
                flags: libc::EV_DELETE,
                fflags: 0,
                data: 0,
                udata: std::ptr::null_mut(),
            };
            
            unsafe {
                if libc::kevent(self.kqueue_fd, &kevent, 1, std::ptr::null_mut(), 0, std::ptr::null()) == -1 {
                    return Err(AsyncError::IoError(std::io::Error::last_os_error()));
                }
            }
            
            // Also remove write filter if it exists
            kevent.filter = libc::EVFILT_WRITE;
            unsafe {
                libc::kevent(self.kqueue_fd, &kevent, 1, std::ptr::null_mut(), 0, std::ptr::null());
            }
            
            // Clean up tracking maps
            self.token_to_fd.remove(&token);
            self.fd_to_token.remove(&fd);
        }
        
        Ok(())
    }

    fn poll(&mut self, events: &mut Vec<IoEvent>, timeout: Duration) -> Result<usize, AsyncError> {
        const MAX_EVENTS: usize = 1024;
        let mut kevents = [unsafe { std::mem::zeroed::<libc::kevent>() }; MAX_EVENTS];
        
        let timeout_spec = libc::timespec {
            tv_sec: timeout.as_secs() as libc::time_t,
            tv_nsec: (timeout.subsec_nanos() as libc::c_long),
        };

        let num_events = unsafe {
            libc::kevent(
                self.kqueue_fd,
                std::ptr::null(),
                0,
                kevents.as_mut_ptr(),
                MAX_EVENTS as i32,
                &timeout_spec,
            )
        };

        if num_events < 0 {
            return Err(AsyncError::ReactorError("Kqueue wait failed".to_string()));
        }

        for i in 0..num_events as usize {
            let kevent = &kevents[i];
            
            let io_event = IoEvent {
                token: IoToken(kevent.udata as usize),
                readable: kevent.filter == libc::EVFILT_READ,
                writable: kevent.filter == libc::EVFILT_WRITE,
                error: (kevent.flags & libc::EV_ERROR) != 0,
                hang_up: (kevent.flags & libc::EV_EOF) != 0,
            };

            events.push(io_event);
        }

        Ok(num_events as usize)
    }

    fn interrupt(&self) -> Result<(), AsyncError> {
        // Send a user event to interrupt
        let kevent = libc::kevent {
            ident: 0,
            filter: libc::EVFILT_USER,
            flags: libc::EV_ADD | libc::EV_ENABLE | libc::EV_TRIGGER,
            fflags: 0,
            data: 0,
            udata: std::ptr::null_mut(),
        };

        if unsafe {
            libc::kevent(
                self.kqueue_fd,
                &kevent,
                1,
                std::ptr::null_mut(),
                0,
                std::ptr::null(),
            )
        } < 0 {
            return Err(AsyncError::ReactorError("Failed to interrupt kqueue".to_string()));
        }

        Ok(())
    }

    fn clone_backend(&self) -> Box<dyn ReactorBackend> {
        Box::new(KqueueBackend::new().unwrap())
    }
}

#[cfg(any(target_os = "macos", target_os = "freebsd", target_os = "openbsd"))]
impl Drop for KqueueBackend {
    fn drop(&mut self) {
        unsafe {
            libc::close(self.kqueue_fd);
        }
    }
}

/// Windows IOCP-based reactor backend
#[cfg(target_os = "windows")]
#[derive(Debug)]
struct IocpBackend {
    iocp_handle: winapi::um::winnt::HANDLE,
    registered_handles: std::collections::HashMap<IoToken, winapi::um::winnt::HANDLE>,
    token_counter: std::sync::atomic::AtomicUsize,
}

#[cfg(target_os = "windows")]
impl IocpBackend {
    fn new() -> Result<Self, AsyncError> {
        use winapi::um::ioapiset::CreateIoCompletionPort;
        use winapi::um::winbase::INVALID_HANDLE_VALUE;
        
        let iocp_handle = unsafe {
            CreateIoCompletionPort(INVALID_HANDLE_VALUE, std::ptr::null_mut(), 0, 0)
        };
        
        if iocp_handle.is_null() {
            return Err(AsyncError::ReactorError("Failed to create IOCP".to_string()));
        }
        
        Ok(Self {
            iocp_handle,
            registered_handles: std::collections::HashMap::new(),
            token_counter: std::sync::atomic::AtomicUsize::new(1),
        })
    }
}

#[cfg(target_os = "windows")]
impl ReactorBackend for IocpBackend {
    fn register(&self, fd: RawFd, token: IoToken, _interest: IoInterest) -> Result<(), AsyncError> {
        use winapi::um::ioapiset::CreateIoCompletionPort;
        use std::os::windows::io::FromRawHandle;
        
        let handle = unsafe { std::os::windows::io::FromRawHandle::from_raw_handle(fd as *mut std::ffi::c_void) };
        let handle_ptr = handle as winapi::um::winnt::HANDLE;
        
        // Associate the handle with our IOCP
        let result = unsafe {
            CreateIoCompletionPort(handle_ptr, self.iocp_handle, token.0 as usize, 0)
        };
        
        if result.is_null() {
            return Err(AsyncError::ReactorError("Failed to associate handle with IOCP".to_string()));
        }
        
        self.registered_handles.insert(token, handle_ptr);
        Ok(())
    }

    fn unregister(&self, token: IoToken) -> Result<(), AsyncError> {
        // IOCP handles are automatically disassociated when closed
        self.registered_handles.remove(&token);
        Ok(())
    }

    fn poll(&mut self, events: &mut Vec<IoEvent>, timeout: Duration) -> Result<usize, AsyncError> {
        use winapi::um::ioapiset::GetQueuedCompletionStatus;
        use winapi::um::winbase::WAIT_TIMEOUT;
        
        let timeout_ms = timeout.as_millis() as u32;
        let mut bytes_transferred: u32 = 0;
        let mut completion_key: usize = 0;
        let mut overlapped: *mut winapi::um::minwinbase::OVERLAPPED = std::ptr::null_mut();
        
        let result = unsafe {
            GetQueuedCompletionStatus(
                self.iocp_handle,
                &mut bytes_transferred,
                &mut completion_key,
                &mut overlapped,
                timeout_ms,
            )
        };
        
        if result == 0 {
            let error = unsafe { winapi::um::errhandlingapi::GetLastError() };
            if error == WAIT_TIMEOUT {
                return Ok(0); // Timeout, no events
            } else {
                return Err(AsyncError::ReactorError(format!("IOCP error: {}", error)));
            }
        }
        
        // Convert completion to IoEvent
        let token = IoToken(completion_key);
        let event_type = if bytes_transferred > 0 {
            IoEventType::Read
        } else {
            IoEventType::Write
        };
        
        events.push(IoEvent {
            token,
            event_type,
            data: bytes_transferred as u64,
        });
        
        Ok(1)
    }

    fn interrupt(&self) -> Result<(), AsyncError> {
        Ok(())
    }

    fn clone_backend(&self) -> Box<dyn ReactorBackend> {
        Box::new(IocpBackend::new().unwrap())
    }
}

/// Fallback select-based reactor for unsupported platforms
#[derive(Debug)]
struct FallbackBackend {
    // Select-based fallback implementation
}

impl FallbackBackend {
    fn new() -> Result<Self, AsyncError> {
        Ok(Self {})
    }
}

impl ReactorBackend for FallbackBackend {
    fn register(&self, _fd: RawFd, _token: IoToken, _interest: IoInterest) -> Result<(), AsyncError> {
        Err(AsyncError::ReactorError("Fallback backend not implemented".to_string()))
    }

    fn unregister(&self, _token: IoToken) -> Result<(), AsyncError> {
        Ok(())
    }

    fn poll(&mut self, _events: &mut Vec<IoEvent>, _timeout: Duration) -> Result<usize, AsyncError> {
        Ok(0)
    }

    fn interrupt(&self) -> Result<(), AsyncError> {
        Ok(())
    }

    fn clone_backend(&self) -> Box<dyn ReactorBackend> {
        Box::new(FallbackBackend::new().unwrap())
    }
}

/// Reactor performance metrics
#[derive(Debug)]
pub struct ReactorMetrics {
    pub registrations: AtomicUsize,
    pub unregistrations: AtomicUsize,
    pub events_processed: AtomicUsize,
    pub poll_cycles: AtomicUsize,
}

impl ReactorMetrics {
    pub fn new() -> Self {
        Self {
            registrations: AtomicUsize::new(0),
            unregistrations: AtomicUsize::new(0),
            events_processed: AtomicUsize::new(0),
            poll_cycles: AtomicUsize::new(0),
        }
    }
}

/// Reactor statistics
#[derive(Debug, Clone)]
pub struct ReactorStats {
    pub active_registrations: usize,
    pub registrations: usize,
    pub unregistrations: usize,
    pub events_processed: usize,
    pub poll_cycles: usize,
}

// WakerId and TaskId new() methods are implemented in their respective modules