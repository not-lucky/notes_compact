# Synchronization Primitives

When multiple threads share mutable state, synchronization primitives are required to ensure thread safety and coordinate execution.

## 1. Locks (Mutex)

### `threading.Lock`
A non-reentrant lock. If the same thread tries to acquire it twice, it will hang (deadlock).
*   **Use Case**: Protecting simple shared variables or resources.

```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock: # Automatically acquires and releases
        counter += 1
```

### `threading.RLock` (Reentrant Lock)
Can be acquired multiple times by the same thread. It maintains an internal counter and must be released the same number of times it was acquired.
*   **Use Case**: Recursive functions or complex classes where multiple methods might need to acquire the same lock.

---

## 2. Semaphores

A Semaphore maintains an internal counter. `acquire()` decrements it; `release()` increments it. If the counter is zero, `acquire()` blocks.

*   **BoundedSemaphore**: A version that raises an error if `release()` is called too many times (exceeding the initial value).
*   **Use Case**: Throttling or limiting access to a resource (e.g., max 5 concurrent database connections).

```python
import threading

# Limit to 3 concurrent downloads
semaphore = threading.BoundedSemaphore(3)

def download_file():
    with semaphore:
        # Perform download
        pass
```

---

## 3. Events

A simple communication mechanism where one thread signals an event and other threads wait for it. It has an internal flag (`True`/`False`).

*   `set()`: Sets flag to True; wakes all waiting threads.
*   `clear()`: Sets flag to False.
*   `wait()`: Blocks until flag is True.

---

## 4. Condition Variables

Used when a thread needs to wait for a specific state change in a shared resource. It is always associated with a Lock.

*   `wait()`: Releases the lock and blocks until notified. When it wakes up, it re-acquires the lock.
*   `notify(n=1)`: Wakes up $n$ threads waiting on the condition.
*   `notify_all()`: Wakes up all waiting threads.

### The "While Loop" Rule
**Critical**: Always use `while` instead of `if` when waiting on a condition to handle **Spurious Wakeups**.

```python
with condition:
    while not resource_available():
        condition.wait()
    # consume resource
```

---

## 5. Barriers

A synchronization point where a fixed number of threads must all arrive before any are allowed to proceed.
*   **Use Case**: Map-Reduce style parallel processing where you need to wait for all "Map" tasks to finish before starting "Reduce".
