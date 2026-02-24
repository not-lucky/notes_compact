# Chapter 07: Heaps & Priority Queues

## Why This Matters for Interviews

Heaps are **essential for efficiency-focused interview questions** at FANG+ companies because:

1. **Top-K problems**: Classic pattern that appears in nearly every interview loop
2. **Stream processing**: Handle real-time data with optimal complexity
3. **Scheduling problems**: Natural fit for priority-based task execution
4. **Merge patterns**: Efficiently combine sorted data sources
5. **Median finding**: Two-heap pattern is a FANG+ favorite

At FANG+ companies, heap problems test your ability to recognize when O(n log k) beats O(n log n).

**Interview frequency**: High. Heaps appear in 30-40% of technical interviews.

---

## Core Patterns to Master

| Pattern            | Frequency | Key Problems                       |
| ------------------ | --------- | ---------------------------------- |
| Top-K Elements     | Very High | Kth largest, K most frequent       |
| Merge K Sorted     | High      | Merge K lists, smallest range      |
| Two Heaps          | High      | Find median, sliding window median |
| Scheduling         | Medium    | Task scheduler, meeting rooms II   |
| K Closest/Smallest | High      | K closest points, K smallest pairs |

---

## Chapter Sections

| Section                                               | Topic               | Key Takeaway                        |
| ----------------------------------------------------- | ------------------- | ----------------------------------- |
| [01-heap-basics](./01-heap-basics.md)                 | Heap Fundamentals   | Heap property, heapify, push/pop    |
| [02-python-heapq](./02-python-heapq.md)               | Python heapq Module | Using Python's heap implementation  |
| [03-top-k-pattern](./03-top-k-pattern.md)             | Top-K Pattern       | Find K largest/smallest efficiently |
| [04-kth-largest-element](./04-kth-largest-element.md) | Kth Largest Element | Heap vs QuickSelect approaches      |
| [05-merge-k-sorted](./05-merge-k-sorted.md)           | Merge K Sorted      | Combine multiple sorted sources     |
| [06-median-stream](./06-median-stream.md)             | Median from Stream  | Two-heap pattern                    |
| [07-task-scheduler](./07-task-scheduler.md)           | Task Scheduling     | Priority queue with cooldown        |
| [08-k-closest-points](./08-k-closest-points.md)       | K Closest Points    | Distance-based heap problems        |

---

## Common Mistakes Interviewers Watch For

1. **Using max heap when min heap is needed**: Python's heapq is min heap only
2. **Forgetting to negate values for max heap**: Must negate when pushing/popping
3. **Wrong K vs N-K choice**: For K largest, use min heap of size K (not max heap of size N)
4. **Not handling duplicates**: Frequency counting with heap needs (freq, value) tuples
5. **Ignoring heap ordering**: Heap is not fully sorted, only root is guaranteed min/max
6. **Off-by-one errors**: K elements means heap size K, not K-1
7. **Modifying heap incorrectly**: Must use heappush/heappop, not direct list operations

---

## Time Targets

| Difficulty | Target Time | Examples                                            |
| ---------- | ----------- | --------------------------------------------------- |
| Easy       | 10-15 min   | Kth Largest in Array, Last Stone Weight             |
| Medium     | 15-25 min   | Top K Frequent, Task Scheduler, K Closest Points to Origin |
| Hard       | 25-40 min   | Merge K Sorted Lists, Find Median from Data Stream, Sliding Window Median |

---

## Pattern Recognition Guide

```
"Find K largest/smallest..."      → Min/Max heap of size K
"Find Kth largest/smallest..."    → Heap of size K, root is answer
"Merge K sorted..."               → Min heap with one element from each source
"Find median in stream..."        → Two heaps (max heap + min heap)
"Schedule tasks with cooldown..." → Max heap + queue for cooldown
"K closest to..."                 → Max heap of size K (for furthest eviction)
"Top K frequent..."               → Count first, then heap
"Smallest range covering..."      → Min heap tracking all lists
```

---

## Heap Property Reminder

```
Min Heap:                   Max Heap (simulated in Python):
     1                           -(-5) = 5
    / \                          /     \
   3   2                    -(-3)=3   -(-4)=4
  / \
 7   4

Parent ≤ Children           Parent ≥ Children
Root = minimum              Root = maximum
```

---

## Key Complexity Facts

| Operation          | Time       | Notes                                 |
| ------------------ | ---------- | ------------------------------------- |
| heappush           | O(log n)   | Bubble up to maintain heap property   |
| heappop            | O(log n)   | Remove root, bubble down              |
| heapify            | O(n)       | Build heap from list (NOT O(n log n)) |
| peek (heap[0])     | O(1)       | Access root without removal           |
| nlargest(k, list)  | O(n log k) | Uses heap internally                  |
| nsmallest(k, list) | O(n log k) | Uses heap internally                  |

### Why Use Heap Over Sorting?

| Approach        | Time         | When Better                  |
| --------------- | ------------ | ---------------------------- |
| Sort then slice | O(n log n)   | When K ≈ N                   |
| Heap of size K  | O(n log k)   | When K << N                  |
| QuickSelect     | O(n) average | When only Kth element needed |

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [02-arrays-strings](../02-arrays-strings/README.md)

Understanding Big-O and basic array operations is essential. Familiarity with complete binary trees helps but is not required.

---

## Next Steps

Start with [01-heap-basics.md](./01-heap-basics.md) to understand heap structure and operations. Then learn Python's heapq module before tackling the common patterns. The Top-K pattern is the foundation for most heap interview problems.
