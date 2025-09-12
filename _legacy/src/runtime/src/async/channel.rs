// High-Performance Channel Implementation for Message Passing
// MPMC, MPSC, SPMC channels with backpressure and flow control

use std::sync::{Arc, Mutex, RwLock};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::collections::{VecDeque, HashMap};
use std::time::{Duration, Instant};
use std::pin::Pin;
use std::task::{Context, Poll, Waker};
use std::future::Future;

use super::{AsyncError};

/// Multi-producer, multi-consumer channel
pub struct Channel<T> {
    inner: Arc<ChannelInner<T>>,
}

impl<T> Channel<T> {
    /// Create a new unbounded channel
    pub fn unbounded() -> (Sender<T>, Receiver<T>) {
        let inner = Arc::new(ChannelInner::new(None));
        let sender = Sender { inner: inner.clone() };
        let receiver = Receiver { inner };
        (sender, receiver)
    }

    /// Create a new bounded channel with capacity
    pub fn bounded(capacity: usize) -> (Sender<T>, Receiver<T>) {
        let inner = Arc::new(ChannelInner::new(Some(capacity)));
        let sender = Sender { inner: inner.clone() };
        let receiver = Receiver { inner };
        (sender, receiver)
    }

    /// Create a broadcast channel (one-to-many)
    pub fn broadcast(capacity: usize) -> (BroadcastSender<T>, BroadcastReceiver<T>) 
    where
        T: Clone,
    {
        let inner = Arc::new(BroadcastInner::new(capacity));
        let sender = BroadcastSender { inner: inner.clone() };
        let receiver = BroadcastReceiver { inner, next_index: 0 };
        (sender, receiver)
    }

    /// Create a priority channel with message priorities
    pub fn priority() -> (PrioritySender<T>, PriorityReceiver<T>)
    where
        T: Ord,
    {
        let inner = Arc::new(PriorityChannelInner::new());
        let sender = PrioritySender { inner: inner.clone() };
        let receiver = PriorityReceiver { inner };
        (sender, receiver)
    }
}

/// Channel sender
#[derive(Debug)]
pub struct Sender<T> {
    inner: Arc<ChannelInner<T>>,
}

impl<T> Sender<T> {
    /// Send a message asynchronously
    pub fn send(&self, message: T) -> SendFuture<T> {
        SendFuture::new(self.inner.clone(), message)
    }

    /// Try to send a message immediately
    pub fn try_send(&self, message: T) -> Result<(), TrySendError<T>> {
        self.inner.try_send(message)
    }

    /// Check if channel is closed
    pub fn is_closed(&self) -> bool {
        self.inner.is_closed()
    }

    /// Get channel capacity
    pub fn capacity(&self) -> Option<usize> {
        self.inner.capacity()
    }

    /// Get number of messages in channel
    pub fn len(&self) -> usize {
        self.inner.len()
    }

    /// Check if channel is empty
    pub fn is_empty(&self) -> bool {
        self.inner.is_empty()
    }

    /// Close the channel
    pub fn close(&self) {
        self.inner.close();
    }
}

impl<T> Clone for Sender<T> {
    fn clone(&self) -> Self {
        self.inner.add_sender();
        Self { inner: self.inner.clone() }
    }
}

impl<T> Drop for Sender<T> {
    fn drop(&mut self) {
        self.inner.remove_sender();
    }
}

/// Channel receiver
#[derive(Debug)]
pub struct Receiver<T> {
    inner: Arc<ChannelInner<T>>,
}

impl<T> Receiver<T> {
    /// Receive a message asynchronously
    pub fn recv(&self) -> RecvFuture<T> {
        RecvFuture::new(self.inner.clone())
    }

    /// Try to receive a message immediately
    pub fn try_recv(&self) -> Result<T, TryRecvError> {
        self.inner.try_recv()
    }

    /// Check if channel is closed and empty
    pub fn is_closed(&self) -> bool {
        self.inner.is_closed() && self.inner.is_empty()
    }

    /// Get number of messages in channel
    pub fn len(&self) -> usize {
        self.inner.len()
    }

    /// Check if channel is empty
    pub fn is_empty(&self) -> bool {
        self.inner.is_empty()
    }

    /// Close the channel
    pub fn close(&self) {
        self.inner.close();
    }
}

impl<T> Clone for Receiver<T> {
    fn clone(&self) -> Self {
        self.inner.add_receiver();
        Self { inner: self.inner.clone() }
    }
}

impl<T> Drop for Receiver<T> {
    fn drop(&mut self) {
        self.inner.remove_receiver();
    }
}

/// Internal channel implementation
struct ChannelInner<T> {
    queue: Mutex<VecDeque<T>>,
    capacity: Option<usize>,
    send_wakers: Mutex<Vec<Waker>>,
    recv_wakers: Mutex<Vec<Waker>>,
    sender_count: AtomicUsize,
    receiver_count: AtomicUsize,
    closed: AtomicBool,
    metrics: ChannelMetrics,
}

impl<T> ChannelInner<T> {
    fn new(capacity: Option<usize>) -> Self {
        Self {
            queue: Mutex::new(VecDeque::new()),
            capacity,
            send_wakers: Mutex::new(Vec::new()),
            recv_wakers: Mutex::new(Vec::new()),
            sender_count: AtomicUsize::new(1),
            receiver_count: AtomicUsize::new(1),
            closed: AtomicBool::new(false),
            metrics: ChannelMetrics::new(),
        }
    }

    fn try_send(&self, message: T) -> Result<(), TrySendError<T>> {
        if self.closed.load(Ordering::Acquire) {
            return Err(TrySendError::Closed(message));
        }

        if let Ok(mut queue) = self.queue.lock() {
            // Check capacity
            if let Some(cap) = self.capacity {
                if queue.len() >= cap {
                    return Err(TrySendError::Full(message));
                }
            }

            queue.push_back(message);
            self.metrics.messages_sent.fetch_add(1, Ordering::Relaxed);
            
            // Wake a receiver
            if let Ok(mut wakers) = self.recv_wakers.lock() {
                if let Some(waker) = wakers.pop() {
                    waker.wake();
                }
            }

            Ok(())
        } else {
            Err(TrySendError::Closed(message))
        }
    }

    fn try_recv(&self) -> Result<T, TryRecvError> {
        if let Ok(mut queue) = self.queue.lock() {
            if let Some(message) = queue.pop_front() {
                self.metrics.messages_received.fetch_add(1, Ordering::Relaxed);
                
                // Wake a sender if there was backpressure
                if let Ok(mut wakers) = self.send_wakers.lock() {
                    if let Some(waker) = wakers.pop() {
                        waker.wake();
                    }
                }

                Ok(message)
            } else if self.closed.load(Ordering::Acquire) && self.sender_count.load(Ordering::Acquire) == 0 {
                Err(TryRecvError::Disconnected)
            } else {
                Err(TryRecvError::Empty)
            }
        } else {
            Err(TryRecvError::Disconnected)
        }
    }

    fn add_send_waker(&self, waker: Waker) {
        if let Ok(mut wakers) = self.send_wakers.lock() {
            wakers.push(waker);
        }
    }

    fn add_recv_waker(&self, waker: Waker) {
        if let Ok(mut wakers) = self.recv_wakers.lock() {
            wakers.push(waker);
        }
    }

    fn add_sender(&self) {
        self.sender_count.fetch_add(1, Ordering::Relaxed);
    }

    fn remove_sender(&self) {
        if self.sender_count.fetch_sub(1, Ordering::Relaxed) == 1 {
            // Last sender removed, wake all receivers
            if let Ok(mut wakers) = self.recv_wakers.lock() {
                for waker in wakers.drain(..) {
                    waker.wake();
                }
            }
        }
    }

    fn add_receiver(&self) {
        self.receiver_count.fetch_add(1, Ordering::Relaxed);
    }

    fn remove_receiver(&self) {
        if self.receiver_count.fetch_sub(1, Ordering::Relaxed) == 1 {
            // Last receiver removed, wake all senders
            if let Ok(mut wakers) = self.send_wakers.lock() {
                for waker in wakers.drain(..) {
                    waker.wake();
                }
            }
        }
    }

    fn is_closed(&self) -> bool {
        self.closed.load(Ordering::Acquire)
    }

    fn close(&self) {
        self.closed.store(true, Ordering::Release);
        
        // Wake all waiting tasks
        if let Ok(mut send_wakers) = self.send_wakers.lock() {
            for waker in send_wakers.drain(..) {
                waker.wake();
            }
        }
        
        if let Ok(mut recv_wakers) = self.recv_wakers.lock() {
            for waker in recv_wakers.drain(..) {
                waker.wake();
            }
        }
    }

    fn capacity(&self) -> Option<usize> {
        self.capacity
    }

    fn len(&self) -> usize {
        self.queue.lock().map(|q| q.len()).unwrap_or(0)
    }

    fn is_empty(&self) -> bool {
        self.queue.lock().map(|q| q.is_empty()).unwrap_or(true)
    }
}

/// Send future for async sending
pub struct SendFuture<T> {
    inner: Arc<ChannelInner<T>>,
    message: Option<T>,
}

impl<T> SendFuture<T> {
    fn new(inner: Arc<ChannelInner<T>>, message: T) -> Self {
        Self { inner, message: Some(message) }
    }
}

impl<T> Future for SendFuture<T> {
    type Output = Result<(), SendError<T>>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = unsafe { self.get_unchecked_mut() };
        if let Some(message) = this.message.take() {
            match this.inner.try_send(message) {
                Ok(()) => Poll::Ready(Ok(())),
                Err(TrySendError::Full(msg)) => {
                    this.message = Some(msg);
                    this.inner.add_send_waker(cx.waker().clone());
                    Poll::Pending
                }
                Err(TrySendError::Closed(msg)) => Poll::Ready(Err(SendError(msg))),
            }
        } else {
            // Future was polled after completion - this shouldn't happen
            panic!("SendFuture polled after completion")
        }
    }
}

/// Receive future for async receiving
pub struct RecvFuture<T> {
    inner: Arc<ChannelInner<T>>,
}

impl<T> RecvFuture<T> {
    fn new(inner: Arc<ChannelInner<T>>) -> Self {
        Self { inner }
    }
}

impl<T> Future for RecvFuture<T> {
    type Output = Result<T, RecvError>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        match self.inner.try_recv() {
            Ok(message) => Poll::Ready(Ok(message)),
            Err(TryRecvError::Empty) => {
                self.inner.add_recv_waker(cx.waker().clone());
                Poll::Pending
            }
            Err(TryRecvError::Disconnected) => Poll::Ready(Err(RecvError)),
        }
    }
}

/// Broadcast channel for one-to-many communication
pub struct BroadcastSender<T> {
    inner: Arc<BroadcastInner<T>>,
}

impl<T> BroadcastSender<T>
where
    T: Clone,
{
    /// Send message to all receivers
    pub fn send(&self, message: T) -> Result<usize, SendError<T>> {
        self.inner.send(message)
    }

    /// Get number of receivers
    pub fn receiver_count(&self) -> usize {
        self.inner.receiver_count()
    }

    /// Close the broadcast channel
    pub fn close(&self) {
        self.inner.close();
    }
}

/// Broadcast receiver
pub struct BroadcastReceiver<T> {
    inner: Arc<BroadcastInner<T>>,
    next_index: usize,
}

impl<T> BroadcastReceiver<T>
where
    T: Clone,
{
    /// Receive next message
    pub async fn recv(&mut self) -> Result<T, RecvError> {
        BroadcastRecvFuture::new(self.inner.clone(), &mut self.next_index).await
    }

    /// Try to receive message immediately
    pub fn try_recv(&mut self) -> Result<T, TryRecvError> {
        self.inner.try_recv(&mut self.next_index)
    }
}

impl<T> Clone for BroadcastReceiver<T> {
    fn clone(&self) -> Self {
        self.inner.add_receiver();
        Self {
            inner: self.inner.clone(),
            next_index: self.next_index,
        }
    }
}

/// Broadcast channel internal implementation
struct BroadcastInner<T> {
    messages: RwLock<VecDeque<(usize, T)>>, // (index, message)
    capacity: usize,
    next_index: AtomicUsize,
    receiver_count: AtomicUsize,
    closed: AtomicBool,
    wakers: Mutex<HashMap<usize, Vec<Waker>>>, // receiver_id -> wakers
}

impl<T> BroadcastInner<T>
where
    T: Clone,
{
    fn new(capacity: usize) -> Self {
        Self {
            messages: RwLock::new(VecDeque::new()),
            capacity,
            next_index: AtomicUsize::new(0),
            receiver_count: AtomicUsize::new(1),
            closed: AtomicBool::new(false),
            wakers: Mutex::new(HashMap::new()),
        }
    }

    fn send(&self, message: T) -> Result<usize, SendError<T>> {
        if self.closed.load(Ordering::Acquire) {
            return Err(SendError(message));
        }

        let index = self.next_index.fetch_add(1, Ordering::Relaxed);
        let receiver_count = self.receiver_count.load(Ordering::Relaxed);

        if let Ok(mut messages) = self.messages.write() {
            messages.push_back((index, message));
            
            // Remove old messages beyond capacity
            while messages.len() > self.capacity {
                messages.pop_front();
            }
        }

        // Wake all receivers
        if let Ok(mut wakers) = self.wakers.lock() {
            for waker_list in wakers.values_mut() {
                for waker in waker_list.drain(..) {
                    waker.wake();
                }
            }
        }

        Ok(receiver_count)
    }

    fn try_recv(&self, next_index: &mut usize) -> Result<T, TryRecvError> {
        if let Ok(messages) = self.messages.read() {
            // Find message with our index
            for (msg_index, message) in messages.iter() {
                if *msg_index >= *next_index {
                    *next_index = *msg_index + 1;
                    return Ok(message.clone());
                }
            }
        }

        if self.closed.load(Ordering::Acquire) {
            Err(TryRecvError::Disconnected)
        } else {
            Err(TryRecvError::Empty)
        }
    }

    fn add_receiver(&self) {
        self.receiver_count.fetch_add(1, Ordering::Relaxed);
    }

    fn receiver_count(&self) -> usize {
        self.receiver_count.load(Ordering::Relaxed)
    }

    fn close(&self) {
        self.closed.store(true, Ordering::Release);
        
        if let Ok(mut wakers) = self.wakers.lock() {
            for waker_list in wakers.values_mut() {
                for waker in waker_list.drain(..) {
                    waker.wake();
                }
            }
        }
    }
}

/// Broadcast receive future
struct BroadcastRecvFuture<'a, T> {
    inner: Arc<BroadcastInner<T>>,
    next_index: &'a mut usize,
}

impl<'a, T> BroadcastRecvFuture<'a, T>
where
    T: Clone,
{
    fn new(inner: Arc<BroadcastInner<T>>, next_index: &'a mut usize) -> Self {
        Self { inner, next_index }
    }
}

impl<'a, T> Future for BroadcastRecvFuture<'a, T>
where
    T: Clone,
{
    type Output = Result<T, RecvError>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = unsafe { self.get_unchecked_mut() };
        match this.inner.try_recv(this.next_index) {
            Ok(message) => Poll::Ready(Ok(message)),
            Err(TryRecvError::Empty) => {
                // Register waker for this receiver
                if let Ok(mut wakers) = this.inner.wakers.lock() {
                    let receiver_id = *this.next_index; // Use index as receiver ID
                    wakers.entry(receiver_id).or_insert_with(Vec::new).push(cx.waker().clone());
                }
                Poll::Pending
            }
            Err(TryRecvError::Disconnected) => Poll::Ready(Err(RecvError)),
        }
    }
}

/// Priority channel sender
pub struct PrioritySender<T> {
    inner: Arc<PriorityChannelInner<T>>,
}

impl<T> PrioritySender<T>
where
    T: Ord,
{
    /// Send message with priority
    pub async fn send(&self, message: T) -> Result<(), SendError<T>> {
        PrioritySendFuture::new(self.inner.clone(), message).await
    }

    /// Send high priority message
    pub async fn send_high_priority(&self, message: T) -> Result<(), SendError<T>> {
        PriorityMessage::High(message).send_to(self.inner.clone()).await
    }

    /// Send low priority message
    pub async fn send_low_priority(&self, message: T) -> Result<(), SendError<T>> {
        PriorityMessage::Low(message).send_to(self.inner.clone()).await
    }
}

/// Priority channel receiver
pub struct PriorityReceiver<T> {
    inner: Arc<PriorityChannelInner<T>>,
}

impl<T> PriorityReceiver<T>
where
    T: Ord,
{
    /// Receive highest priority message
    pub async fn recv(&self) -> Result<T, RecvError> {
        PriorityRecvFuture::new(self.inner.clone()).await
    }
}

/// Priority message wrapper
enum PriorityMessage<T> {
    High(T),
    Normal(T),
    Low(T),
}

impl<T> PriorityMessage<T> {
    async fn send_to(self, inner: Arc<PriorityChannelInner<T>>) -> Result<(), SendError<T>>
    where
        T: Ord,
    {
        match self {
            PriorityMessage::High(msg) => inner.send_priority(msg, Priority::High).await,
            PriorityMessage::Normal(msg) => inner.send_priority(msg, Priority::Normal).await,
            PriorityMessage::Low(msg) => inner.send_priority(msg, Priority::Low).await,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum Priority {
    High = 0,
    Normal = 1,
    Low = 2,
}

/// Priority channel internal implementation
struct PriorityChannelInner<T> {
    high_priority: Mutex<VecDeque<T>>,
    normal_priority: Mutex<VecDeque<T>>,
    low_priority: Mutex<VecDeque<T>>,
    wakers: Mutex<Vec<Waker>>,
    closed: AtomicBool,
}

impl<T> PriorityChannelInner<T>
where
    T: Ord,
{
    fn new() -> Self {
        Self {
            high_priority: Mutex::new(VecDeque::new()),
            normal_priority: Mutex::new(VecDeque::new()),
            low_priority: Mutex::new(VecDeque::new()),
            wakers: Mutex::new(Vec::new()),
            closed: AtomicBool::new(false),
        }
    }

    async fn send_priority(&self, message: T, priority: Priority) -> Result<(), SendError<T>> {
        if self.closed.load(Ordering::Acquire) {
            return Err(SendError(message));
        }

        let queue = match priority {
            Priority::High => &self.high_priority,
            Priority::Normal => &self.normal_priority,
            Priority::Low => &self.low_priority,
        };

        if let Ok(mut q) = queue.lock() {
            q.push_back(message);
            
            // Wake a receiver
            if let Ok(mut wakers) = self.wakers.lock() {
                if let Some(waker) = wakers.pop() {
                    waker.wake();
                }
            }
            
            Ok(())
        } else {
            Err(SendError(message))
        }
    }

    fn try_recv(&self) -> Result<T, TryRecvError> {
        // Try high priority first
        if let Ok(mut high) = self.high_priority.lock() {
            if let Some(message) = high.pop_front() {
                return Ok(message);
            }
        }

        // Then normal priority
        if let Ok(mut normal) = self.normal_priority.lock() {
            if let Some(message) = normal.pop_front() {
                return Ok(message);
            }
        }

        // Finally low priority
        if let Ok(mut low) = self.low_priority.lock() {
            if let Some(message) = low.pop_front() {
                return Ok(message);
            }
        }

        if self.closed.load(Ordering::Acquire) {
            Err(TryRecvError::Disconnected)
        } else {
            Err(TryRecvError::Empty)
        }
    }

    fn add_waker(&self, waker: Waker) {
        if let Ok(mut wakers) = self.wakers.lock() {
            wakers.push(waker);
        }
    }
}

/// Priority send future
struct PrioritySendFuture<T> {
    inner: Arc<PriorityChannelInner<T>>,
    message: Option<T>,
}

impl<T> PrioritySendFuture<T> {
    fn new(inner: Arc<PriorityChannelInner<T>>, message: T) -> Self {
        Self { inner, message: Some(message) }
    }
}

impl<T> Future for PrioritySendFuture<T>
where
    T: Ord,
{
    type Output = Result<(), SendError<T>>;

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {
        if let Some(message) = self.message.take() {
            // Priority channels are always ready to send (unbounded)
            match futures::executor::block_on(self.inner.send_priority(message, Priority::Normal)) {
                Ok(_) => Poll::Ready(Ok(())),
                Err(e) => Poll::Ready(Err(e))
            }
        } else {
            Poll::Ready(Ok(()))
        }
    }
}

/// Priority receive future
struct PriorityRecvFuture<T> {
    inner: Arc<PriorityChannelInner<T>>,
}

impl<T> PriorityRecvFuture<T> {
    fn new(inner: Arc<PriorityChannelInner<T>>) -> Self {
        Self { inner }
    }
}

impl<T> Future for PriorityRecvFuture<T>
where
    T: Ord,
{
    type Output = Result<T, RecvError>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        match self.inner.try_recv() {
            Ok(message) => Poll::Ready(Ok(message)),
            Err(TryRecvError::Empty) => {
                self.inner.add_waker(cx.waker().clone());
                Poll::Pending
            }
            Err(TryRecvError::Disconnected) => Poll::Ready(Err(RecvError)),
        }
    }
}

/// Channel metrics for monitoring
#[derive(Debug)]
struct ChannelMetrics {
    messages_sent: AtomicUsize,
    messages_received: AtomicUsize,
    peak_queue_size: AtomicUsize,
}

impl ChannelMetrics {
    fn new() -> Self {
        Self {
            messages_sent: AtomicUsize::new(0),
            messages_received: AtomicUsize::new(0),
            peak_queue_size: AtomicUsize::new(0),
        }
    }
}

/// Error types
#[derive(Debug)]
pub struct SendError<T>(pub T);

#[derive(Debug)]
pub struct RecvError;

#[derive(Debug)]
pub enum TrySendError<T> {
    Full(T),
    Closed(T),
}

#[derive(Debug)]
pub enum TryRecvError {
    Empty,
    Disconnected,
}

/// Utility functions
pub fn unbounded<T>() -> (Sender<T>, Receiver<T>) {
    Channel::unbounded()
}

pub fn bounded<T>(capacity: usize) -> (Sender<T>, Receiver<T>) {
    Channel::bounded(capacity)
}

pub fn broadcast<T>(capacity: usize) -> (BroadcastSender<T>, BroadcastReceiver<T>)
where
    T: Clone,
{
    Channel::broadcast(capacity)
}

pub fn priority<T>() -> (PrioritySender<T>, PriorityReceiver<T>)
where
    T: Ord,
{
    Channel::priority()
}

impl<T> std::fmt::Display for SendError<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "channel closed")
    }
}

impl<T: std::fmt::Debug> std::error::Error for SendError<T> {}

impl std::fmt::Display for RecvError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "channel disconnected")
    }
}

impl std::error::Error for RecvError {}