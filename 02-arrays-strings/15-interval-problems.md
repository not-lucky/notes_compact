# Interval Problems

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Interval problems model real-world scheduling scenarios (e.g., calendar appointments, resource allocation, event planning). The core strategy is **sorting** (usually by start or end time), which transforms an overlapping $\Theta(n^2)$ pairwise comparison problem into a streamlined $\Theta(n \log n)$ linear pass. Most interval problems follow a common structure: sort first, then traverse once.

## Building Intuition & Mental Models

**Why does sorting unlock efficient interval algorithms?**

The key insight is that **sorted intervals reveal geometric structure**:

1. **Sort by Start = Merge Potential**: When sorted by start, consecutive intervals are most likely to overlap. Interval `[5, 10]` can only overlap with intervals starting at $\le 10$. Once we encounter a start time of `11`, no more overlaps are possible for the current interval.
2. **Sort by End = Greedy Selection**: When sorted by end time, the earliest-ending interval leaves maximum room for subsequent ones. This is why Activity Selection (or minimum removals to make non-overlapping) uses end-time sorting.
3. **Event-Based Counting**: Treating starts and ends as atomic events and processing them chronologically lets us count concurrent intervals in one pass.

**🧠 Mental Model: Merge Intervals (Painting a Fence)**
Imagine you are painting a long wooden fence, one segment at a time. Each segment is an interval. Sorting by start time means you walk along the fence from left to right. As you walk, if the next paint job overlaps with the wet paint of your current job, you simply extend your continuous wet block. If there's a dry gap, you step over it and start a brand new block of paint.

**🧠 Mental Model: Meeting Rooms (The Bouncer's Clicker)**
Think of a nightclub where people enter (`+1`) and leave (`-1`). A bouncer at the door logs the exact time of every entry and exit. Sort all these events chronologically. The bouncer walks through the log, clicking their tally counter up for entries and down for exits. The highest number the counter ever reaches is the maximum occupancy (rooms needed). If people leave and enter at the exact same minute, the bouncer processes the exits first so they don't incorrectly deny entry due to a full club!

**Why Sort by Start for Merging:**
```text
Unsorted: [[8, 10], [1, 3], [2, 6], [15, 18]]
Sorted:   [[1, 3], [2, 6], [8, 10], [15, 18]]

After sorting, we check consecutive pairs left-to-right:
[1, 3] and [2, 6]   -> 2 <= 3  -> overlap! Merge to [1, 6]
[1, 6] and [8, 10]  -> 8 > 6   -> gap! Start new interval [8, 10]
[8, 10] and [15, 18]-> 15 > 10 -> gap! Start new interval [15, 18]

Result: [[1, 6], [8, 10], [15, 18]]

Without sorting, we must compare all pairs: \Theta(n^2)
```

## Python Nuances & Complexity Reminders

When solving interval problems in Python, keep these facts in mind:
- **Dynamic Arrays:** Python lists (`list`) are dynamic arrays. Appending an interval using `.append()` takes **amortized $\Theta(1)$ time**.
- **Sorting:** `list.sort()` in Python uses Timsort (worst/average case $\Theta(n \log n)$, best case $\Theta(n)$). If sorting events represented as tuples `(time, delta)`, Python correctly sorts by time first, and breaks ties using the delta.
- **Avoid String Concatenation:** If building string representations of intervals, avoid `+=` in loops (which can be $O(n^2)$ time worst case). Accumulate parts in a list and use `"".join()`.
- **Recursion:** If you use recursion (e.g., Interval Trees), always factor the recursive call stack depth into your space complexity (often $\Theta(\log n)$ or $\Theta(n)$).

---

## Interval Basics

An interval is typically represented as `[start, end]` where `start <= end`.

```python
# Modern Python type hints
interval: list[int] = [1, 5]  # starts at 1, ends at 5

def overlaps(a: list[int], b: list[int]) -> bool:
    """Check if two intervals overlap (inclusive)."""
    return a[0] <= b[1] and b[0] <= a[1]

def merge_two(a: list[int], b: list[int]) -> list[int]:
    """Merge two overlapping intervals."""
    return [min(a[0], b[0]), max(a[1], b[1])]
```

---

## Template: Merge Intervals

### Problem Statement
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the inputs.

**Why it works:**
Sorting by start time ensures that overlapping intervals are adjacent. We only need to check the current interval against the *last* merged interval.

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge all overlapping intervals.

    Time Complexity: \Theta(n \log n) for sorting. The merge pass is \Theta(n).
    Space Complexity: \Theta(n) worst-case to store the result (or \Theta(\log n) for sort stack space).
    """
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    result: list[list[int]] = [intervals[0]]

    for i in range(1, len(intervals)):
        current = intervals[i]
        last_merged = result[-1]

        if current[0] <= last_merged[1]:  # Overlaps
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # Amortized \Theta(1) append to dynamic array
            result.append(current)

    return result
```

---

## Template: Insert Interval

### Problem Statement
You are given an array of non-overlapping `intervals` sorted in ascending order by start time. Insert `new_interval = [start, end]` such that the list remains sorted and non-overlapping.

**Why it works:**
Since the input is already sorted, we don't need to re-sort ($\Theta(n \log n)$). We can process it in three linear $\Theta(n)$ phases:
1. **Before**: Add all intervals ending before the new interval starts.
2. **Merge**: Combine overlapping intervals into the `new_interval`.
3. **After**: Add the remaining intervals.

```python
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """
    Insert new interval and merge if necessary.
    Input intervals are already sorted and non-overlapping.

    Time Complexity: \Theta(n) single pass.
    Space Complexity: \Theta(n) for output array.
    """
    result: list[list[int]] = []
    i = 0
    n = len(intervals)

    # 1. Add all intervals ending before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # 2. Merge all overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)

    # 3. Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

---

## Template: Meeting Rooms II (Minimum Rooms / Peak Overlap)

### Problem Statement
Given an array of meeting time intervals, return the minimum number of conference rooms required (equivalent to finding the maximum number of concurrent intervals).

**Why it works:**
The "Line Sweep" or "Event" method treats time as a series of distinct chronological events. By sorting events (start adds a room, end frees a room) and keeping a running sum, we map the "peaks" in activity.

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Find minimum number of meeting rooms required using Line Sweep.

    Time Complexity: \Theta(n \log n) to sort events.
    Space Complexity: \Theta(n) to store events array.
    """
    if not intervals:
        return 0

    # Event-based approach (Line Sweep)
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts, +1 room needed
        events.append((end, -1))    # Meeting ends, -1 room needed

    # Sort lexicographically.
    # Crucial Tie-Breaker: If times are equal, -1 comes before 1.
    # This means meetings ending exactly when another starts frees the room first!
    events.sort()

    rooms = 0
    max_rooms = 0

    for _, delta in events:
        rooms += delta
        max_rooms = max(max_rooms, rooms)

    return max_rooms
```

### Alternative: Min-Heap
Tracks the end times of *ongoing* meetings.
```python
import heapq

def min_meeting_rooms_heap(intervals: list[list[int]]) -> int:
    """
    Find minimum number of meeting rooms required using a Min-Heap.

    Time Complexity: \Theta(n \log n) to sort and manage heap operations.
    Space Complexity: \Theta(n) worst-case for the heap.
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap: list[int] = [intervals[0][1]]  # Min-heap of end times

    for i in range(1, len(intervals)):
        # If the earliest ending meeting finishes before/when current starts
        if intervals[i][0] >= heap[0]:
            heapq.heappop(heap)  # Free that room

        # Add the current meeting's end time
        heapq.heappush(heap, intervals[i][1])

    return len(heap)  # Heap size is peak concurrency
```

---

## Template: Non-Overlapping Intervals (Min Removals)

### Problem Statement
Given an array of intervals, return the minimum number of intervals to remove to make the rest non-overlapping.

**Why it works:**
This is a classic Greedy problem. To keep the *maximum* number of intervals, always pick the interval that **ends the earliest** among available non-overlapping ones. This guarantees the maximum possible room for future intervals. By maximizing what we keep, we mathematically minimize what we remove.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Greedy: Always keep the interval that ends earliest.

    Time Complexity: \Theta(n \log n) for sorting.
    Space Complexity: \Theta(\log n) for sorting in Python.
    """
    if not intervals:
        return 0

    # Sort by END time
    intervals.sort(key=lambda x: x[1])

    removed_count = 0
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            # Overlaps! Because we sorted by end time, the current
            # interval MUST end later than or equal to prev_end.
            # We "remove" the current one to preserve optimal space.
            removed_count += 1
        else:
            # Doesn't overlap. We keep it and advance our end tracker.
            prev_end = intervals[i][1]

    return removed_count
```

---

## Template: Interval Intersection (Two Pointers)

### Problem Statement
Given two lists of closed intervals `A` and `B`, where each list is internally sorted and disjoint. Return the intersection.

**Why it works:**
A two-pointer approach is perfect here. The intersecting boundary is always `[max(start1, start2), min(end1, end2)]`. We advance the pointer of the interval that ends earliest, as it cannot possibly overlap with any subsequent intervals in the other list.

```python
def interval_intersection(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """
    Find intersection of two disjoint, sorted interval lists.

    Time Complexity: \Theta(m + n)
    Space Complexity: \Theta(m + n) worst-case output array.
    """
    result: list[list[int]] = []
    i = j = 0

    while i < len(A) and j < len(B):
        # Calculate possible intersection bounds
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])

        # If valid intersection, record it
        if start <= end:
            result.append([start, end])

        # Move the pointer of the interval that finishes first
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return result
```

---

## Sorting Strategies Summary

| Sort By                 | Use Case                                       |
| ----------------------- | ---------------------------------------------- |
| **Start time**          | Merging, Insertion                             |
| **End time**            | Activity selection, Min removals               |
| **Start asc, end desc** | Covered intervals (keeps largest parent first) |
| **Events (start/end)**  | Counting concurrent (Line sweep)               |

---

## Edge Cases

```python
# Empty input
[] -> return [] or 0

# Single interval
[[1, 5]] -> no merge possible

# Adjacent intervals (touching bounds)
[[1, 2], [2, 3]] -> Depends on problem!
# "overlapping" usually implies < or <= depending on strictness.

# Completely contained (Russian Doll)
[[1, 10], [3, 5]] -> merge to [1, 10]

# All overlapping
[[1, 4], [2, 5], [3, 6]] -> [1, 6]
```

---

## Practice Problems

| Problem                     | Difficulty | Key Technique                   |
| --------------------------- | ---------- | ------------------------------- |
| Merge Intervals             | Medium     | Sort by start + merge           |
| Insert Interval             | Medium     | Three linear passes             |
| Meeting Rooms               | Easy       | Sort by start, check adjacencies|
| Meeting Rooms II            | Medium     | Events or Min-Heap              |
| Non-overlapping Intervals   | Medium     | Greedy by end time              |
| Interval List Intersections | Medium     | Two pointers                    |
| Remove Covered Intervals    | Medium     | Sort by start asc, end desc     |
| Employee Free Time          | Hard       | Flatten, merge all, find gaps   |

---

## Key Takeaways

1. **Sort first** - almost always necessary and drops time complexity to $\Theta(n \log n)$.
2. **Overlap check formula**: `a[0] <= b[1] and b[0] <= a[1]`
3. **Merge formula**: `[min(starts), max(ends)]`
4. **For minimum rooms / peak overlaps**: Treat time as events (`+1` and `-1`), sweep the timeline.
5. **For minimum removals**: Greedy strategy. Sort by **end time** and keep the earliest ending ones.
6. **Two pointers** for intersecting two sorted lists.

---

## Chapter Complete!

You've completed Chapter 02: Arrays & Strings. Key patterns learned:

- Two Pointers (same and opposite direction)
- Sliding Window (fixed and variable)
- Prefix Sum and Difference Array
- Kadane's Algorithm
- String Manipulation
- Pattern Matching
- Anagrams and Palindromes
- Matrix Traversal
- In-Place Modifications
- Interval Problems

Next chapter: [03-HashMaps & Sets](../03-hashmaps-sets/README.md)
