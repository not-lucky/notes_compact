# fn-2-knl.3 Implement Concurrency Module

## Description
Create a dedicated module for Concurrency and Parallelism, a critical differentiator for Senior roles. Focus on Python's `threading` vs `multiprocessing` and standard synchronization patterns.

## Scope
1.  **Foundations**:
    *   OS Basics: Context Switching, Scheduler, Race Conditions.
    *   Python Global Interpreter Lock (GIL): Impact on CPU-bound vs I/O-bound tasks.
2.  **Patterns & Sync Primitives**:
    *   **Locks (Mutex)**: `threading.Lock`, `RLock`.
    *   **Semaphores**: Limiting concurrent access (`threading.Semaphore`).
    *   **Events & Conditions**: Inter-thread communication.
    *   **Producer-Consumer**: using `queue.Queue` (thread-safe).
3.  **Classic Problems**:
    *   Design a Bounded Blocking Queue.
    *   Design a Rate Limiter (Token Bucket).
    *   Dining Philosophers (demonstrating deadlock avoidance).

## Definition of Done
- [ ] Directory `20-concurrency` created.
- [ ] `01-concurrency-basics.md` (Concepts + GIL).
- [ ] `02-synchronization-primitives.md` (Locks, Semaphores, Conditions).
- [ ] `03-producer-consumer.md` (Queue implementation).
- [ ] `04-common-concurrency-problems.md` (BlockingQueue, RateLimiter).
