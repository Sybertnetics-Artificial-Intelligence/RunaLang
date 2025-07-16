import unittest
import time
import threading
from runa.stdlib.concurrent import (
    ThreadPoolExecutor, Future, Lock, Event, Condition, Semaphore, Barrier,
    current_thread, active_count, enumerate_threads
)

class TestConcurrentModule(unittest.TestCase):
    def test_thread_pool_executor(self):
        """Test ThreadPoolExecutor basic functionality."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            future = executor.submit(lambda x: x * 2, 5)
            result = future.result()
            self.assertEqual(result, 10)

    def test_future_basic(self):
        """Test Future basic functionality."""
        future = Future()
        future.set_result(42)
        self.assertTrue(future.done())
        self.assertEqual(future.result(), 42)

    def test_future_exception(self):
        """Test Future with exception."""
        future = Future()
        future.set_exception(ValueError("test error"))
        self.assertTrue(future.done())
        with self.assertRaises(ValueError):
            future.result()

    def test_lock_basic(self):
        """Test Lock basic functionality."""
        lock = Lock()
        self.assertFalse(lock.locked())
        
        lock.acquire()
        self.assertTrue(lock.locked())
        
        lock.release()
        self.assertFalse(lock.locked())

    def test_lock_context_manager(self):
        """Test Lock as context manager."""
        lock = Lock()
        with lock:
            self.assertTrue(lock.locked())
        self.assertFalse(lock.locked())

    def test_event_basic(self):
        """Test Event basic functionality."""
        event = Event()
        self.assertFalse(event.is_set())
        
        event.set()
        self.assertTrue(event.is_set())
        
        event.clear()
        self.assertFalse(event.is_set())

    def test_event_wait(self):
        """Test Event wait functionality."""
        event = Event()
        result = []
        
        def set_event():
            time.sleep(0.1)
            event.set()
        
        thread = threading.Thread(target=set_event)
        thread.start()
        
        event.wait(timeout=1.0)
        self.assertTrue(event.is_set())
        thread.join()

    def test_condition_basic(self):
        """Test Condition basic functionality."""
        condition = Condition()
        lock = condition._lock
        
        with condition:
            self.assertTrue(lock.locked())

    def test_condition_wait_notify(self):
        """Test Condition wait and notify."""
        condition = Condition()
        result = []
        
        def worker():
            with condition:
                while not result:
                    condition.wait()
                result.append("notified")
        
        thread = threading.Thread(target=worker)
        thread.start()
        
        time.sleep(0.1)
        with condition:
            result.append("ready")
            condition.notify()
        
        thread.join()
        self.assertEqual(result, ["ready", "notified"])

    def test_semaphore_basic(self):
        """Test Semaphore basic functionality."""
        semaphore = Semaphore(2)
        self.assertEqual(semaphore._value, 2)
        
        semaphore.acquire()
        self.assertEqual(semaphore._value, 1)
        
        semaphore.release()
        self.assertEqual(semaphore._value, 2)

    def test_semaphore_context_manager(self):
        """Test Semaphore as context manager."""
        semaphore = Semaphore(1)
        with semaphore:
            self.assertEqual(semaphore._value, 0)
        self.assertEqual(semaphore._value, 1)

    def test_barrier_basic(self):
        """Test Barrier basic functionality."""
        barrier = Barrier(2)
        result = []
        
        def worker():
            barrier.wait()
            result.append("released")
        
        thread = threading.Thread(target=worker)
        thread.start()
        
        barrier.wait()
        thread.join()
        self.assertEqual(result, ["released"])

    def test_current_thread(self):
        """Test current_thread function."""
        thread_info = current_thread()
        self.assertIsInstance(thread_info, dict)
        self.assertIn('name', thread_info)
        self.assertIn('ident', thread_info)

    def test_active_count(self):
        """Test active_count function."""
        count = active_count()
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_enumerate_threads(self):
        """Test enumerate_threads function."""
        threads = enumerate_threads()
        self.assertIsInstance(threads, list)
        self.assertGreater(len(threads), 0)
        
        for thread_info in threads:
            self.assertIsInstance(thread_info, dict)
            self.assertIn('name', thread_info)
            self.assertIn('ident', thread_info)

    def test_thread_pool_map(self):
        """Test ThreadPoolExecutor map functionality."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda x: x * 2, [1, 2, 3, 4]))
            self.assertEqual(results, [2, 4, 6, 8])

    def test_future_callback(self):
        """Test Future callback functionality."""
        result = []
        
        def callback(future):
            result.append(future.result())
        
        future = Future()
        future.add_done_callback(callback)
        future.set_result("done")
        
        self.assertEqual(result, ["done"])

    def test_lock_timeout(self):
        """Test Lock with timeout."""
        lock = Lock()
        lock.acquire()
        
        # Try to acquire with timeout
        acquired = lock.acquire(timeout=0.1)
        self.assertFalse(acquired)
        
        lock.release()

    def test_semaphore_timeout(self):
        """Test Semaphore with timeout."""
        semaphore = Semaphore(1)
        semaphore.acquire()
        
        # Try to acquire with timeout
        acquired = semaphore.acquire(timeout=0.1)
        self.assertFalse(acquired)
        
        semaphore.release()

if __name__ == '__main__':
    unittest.main() 