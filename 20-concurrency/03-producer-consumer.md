# Producer-Consumer Pattern

The Producer-Consumer pattern decouples the processes that produce data from the processes that consume it, using a shared buffer (Queue).

## 1. Why use it?
1.  **Load Balancing**: Handles bursts of traffic. Producers can work at their own pace.
2.  **Decoupling**: The producer doesn't need to know who the consumer is or how many there are.
3.  **Throttling**: Naturally limits the rate of production if the queue is bounded.

---

## 2. Implementation with `queue.Queue`

In Python, `queue.Queue` is inherently thread-safe and implements all the necessary locking logic internally.

```python
import threading
import queue
import time
import random

def producer(q, n):
    for i in range(n):
        item = f"item-{i}"
        q.put(item)
        print(f"Produced {item}")
        time.sleep(random.random())
    q.put(None) # Sentinel value to signal completion

def consumer(q):
    while True:
        item = q.get()
        if item is None: # Exit on sentinel
            break
        print(f"Consumed {item}")
        q.task_done()
        time.sleep(random.random() * 2)

q = queue.Queue(maxsize=10) # Bounded queue
t1 = threading.Thread(target=producer, args=(q, 5))
t2 = threading.Thread(target=consumer, args=(q,))

t1.start()
t2.start()

t1.join()
t2.join()
```

---

## 3. Core Queue Methods
*   `put(item, block=True, timeout=None)`: Add item. If queue is full, block until space is available.
*   `get(block=True, timeout=None)`: Remove item. If queue is empty, block until item is available.
*   `task_done()`: Used by consumers to indicate that a formerly enqueued task is complete.
*   `join()`: Blocks until all items in the queue have been gotten and processed (`task_done` called for every `put`).

---

## 4. Design Trade-offs: Throughput vs. Latency
*   **Small Buffer**: Low latency (items are processed quickly after production) but prone to producer blocking (lower throughput).
*   **Large Buffer**: High throughput (producers rarely block) but higher latency if consumers fall behind.
*   **Sentinel Pattern**: Use a special value (like `None`) to gracefully shut down consumer threads. For $N$ consumers, you need $N$ sentinels.
