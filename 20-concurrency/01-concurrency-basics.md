# Concurrency Basics

In Senior/Staff level interviews, concurrency isn't just about "using threads." It's about understanding the trade-offs between parallelism and concurrency, the limitations of the underlying runtime (like Python's GIL), and the costs of context switching.

## 1. Core Concepts

### Concurrency vs. Parallelism
*   **Concurrency**: Dealing with multiple tasks at once. It's about *structure*. Two tasks are concurrent if their start and end times overlap. On a single-core CPU, this is achieved via **Context Switching**.
*   **Parallelism**: Doing multiple tasks at once. It's about *execution*. It requires multi-core hardware where tasks literally run at the same physical time.

### Context Switching
The process of storing the state of a process or thread so that it can be restored and resume execution at a later point.
*   **Cost**: Saving/loading registers, program counter, and stack pointer. It also causes **CPU Cache Misses** and **TLB Flushes**, significantly impacting performance.
*   **Preemptive**: The OS scheduler decides when to switch (Threads).
*   **Cooperative**: The task itself yields control (Asyncio/Coroutines).

### Race Conditions
A race condition occurs when the behavior of a software system depends on the sequence or timing of uncontrollable events (like thread scheduling).
*   **Critical Section**: The part of the code that accesses shared resources and must not be concurrently executed by more than one thread.

---

## 2. The Python Global Interpreter Lock (GIL)

The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once.

### Why does it exist?
1.  **Memory Management**: CPython's memory management is not thread-safe. Without the GIL, reference counting would have race conditions, leading to memory leaks or crashes.
2.  **Simplicity**: It made integrating non-thread-safe C libraries easier.

### CPU-Bound vs. I/O-Bound

| Task Type | Behavior under GIL | Recommendation |
| :--- | :--- | :--- |
| **I/O-Bound** (Network, Disk) | Threads release the GIL while waiting for I/O. | Use `threading` or `asyncio`. |
| **CPU-Bound** (Matrix Mult, Hashing) | Threads fight for the GIL, often performing *worse* than single-threaded due to context switching overhead. | Use `multiprocessing` to bypass the GIL. |

### The "Check Interval"
Python threads don't hold the GIL forever. Every $N$ microseconds (or $N$ instructions in older versions), the thread is forced to release the GIL, giving other threads a chance to acquire it.

---

## 3. Liveness Hazards

*   **Deadlock**: Thread A waits for Thread B to release Lock 1, while Thread B waits for Thread A to release Lock 2.
*   **Livelock**: Threads keep changing their state in response to each other, but neither makes progress (like two people trying to pass each other in a hallway and stepping the same way repeatedly).
*   **Starvation**: A thread is perpetually denied access to resources because other threads are prioritized.
