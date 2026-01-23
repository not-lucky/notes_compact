# Chapter 07: Heaps & Priority Queues - Solutions

This directory contains Python implementations for practice problems in Chapter 07. Each solution includes type hints, complexity analysis, and `doctest` examples.

## Solutions

| File | Problems Covered |
|------|------------------|
| [01-heap-basics.md](./01-heap-basics.md) | Kth Largest (Stream), Last Stone Weight |
| [02-python-heapq.md](./02-python-heapq.md) | Practice problems for heapq module |
| [03-top-k-pattern.md](./03-top-k-pattern.md) | Top K Frequent, K Closest Points |
| [04-kth-largest-element.md](./04-kth-largest-element.md) | Kth Largest Element (Heap/QuickSelect) |
| [05-merge-k-sorted.md](./05-merge-k-sorted.md) | Merge K Sorted Lists/Arrays |
| [06-median-stream.md](./06-median-stream.md) | Find Median from Data Stream |
| [07-task-scheduler.md](./07-task-scheduler.md) | Task Scheduler (Greedy + Heap) |
| [08-k-closest-points.md](./08-k-closest-points.md) | K Closest Points to Origin |

## Best Practices
- **Use `heapq`**: Python's standard library for min heaps.
- **Max Heap**: Negate values to simulate max heap behavior.
- **Tuples**: Use `(priority, item)` for priority queues.
- **Complexity**: O(n log k) is typical for Top-K problems.
