# Interval Problems

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Interval problems model real-world scheduling scenarios. The key insight is that sorting (usually by start or end time) transforms O(n²) pairwise comparisons into O(n log n) sequential processing. Most interval problems follow a common structure: sort, then traverse once.

## Building Intuition

**Why does sorting unlock efficient interval algorithms?**

The key insight is **sorted intervals reveal structure**:

1. **Sort by Start = Merge Potential**: When sorted by start, consecutive intervals are most likely to overlap. Interval [5,10] can only overlap with intervals starting at ≤10. Once we pass start=11, no more overlap is possible.

2. **Sort by End = Greedy Selection**: When sorted by end time, the earliest-ending interval leaves maximum room for subsequent ones. This is why Activity Selection uses end-time sorting.

3. **Event-Based Counting**: Treating starts and ends as events and processing them chronologically lets us count concurrent intervals in one pass. This solves "maximum overlap" problems elegantly.

**Mental Model - Merge Intervals**: Imagine laying intervals as rods on a number line. Sorting by start arranges them left-to-right. Walk left to right, extending your current rod if the next one overlaps, or starting a new rod if there's a gap.

**Mental Model - Meeting Rooms**: Think of people entering (+1) and leaving (-1) a room. Sort all enter/leave events by time. Walk through events, tracking the current count. The peak count is the max occupancy = rooms needed.

**Why Sort by Start for Merging**:

```
Unsorted: [[8,10], [1,3], [2,6], [15,18]]
Sorted:   [[1,3], [2,6], [8,10], [15,18]]

After sorting, we check consecutive pairs:
[1,3] and [2,6]: 2 ≤ 3 → overlap! Merge to [1,6]
[1,6] and [8,10]: 8 > 6 → no overlap, start new
[8,10] and [15,18]: 15 > 10 → no overlap, start new

Result: [[1,6], [8,10], [15,18]]

No sorting = must compare all pairs O(n²)
```

**Why Sort by End for Minimum Removals**:

```
Goal: Keep maximum non-overlapping intervals
(equivalently: remove minimum)

Greedy insight: The interval that ends earliest leaves
most room for future intervals.

Intervals: [[1,3], [2,4], [3,5]]

Sorted by end:
[1,3] ← keep (ends earliest)
[2,4] ← overlaps with [1,3] (2 < 3), skip
[3,5] ← doesn't overlap with [1,3] (3 ≥ 3), keep

Keep 2, remove 1
```

## When NOT to Use Standard Interval Techniques

Interval problems have variations needing different approaches:

1. **Weighted Intervals**: If intervals have weights/values and you want maximum value non-overlapping subset, standard greedy doesn't work. Use DP with binary search.

2. **Interval Scheduling on Multiple Resources**: If you have k resources (rooms/machines) and want to maximize scheduling, this is more complex than single-resource greedy.

3. **Intervals with Dependencies**: If interval B must follow interval A, topological sort or constraint satisfaction comes into play.

4. **Modify Intervals Dynamically**: If intervals are added/removed frequently with queries, consider interval trees (balanced BST augmented for intervals).

5. **Circular Intervals**: If time wraps around (like daily schedules), need to handle the wrap-around case specially.

**Red Flags:**

- "Maximum value from non-overlapping intervals" → Weighted interval DP
- "Assign to k resources optimally" → Complex scheduling
- "Intervals added/removed + queries" → Interval tree
- "Daily repeating schedule" → Handle circular time

---

## Interview Context

Interval problems are extremely popular at FANG+ because they:

- Model real-world scheduling problems
- Test sorting and merging logic
- Have many subtle edge cases
- Appear in system design discussions

Key problems: Merge Intervals, Meeting Rooms, Insert Interval.

---

## Interval Basics

An interval is typically represented as `[start, end]` where start ≤ end.

```python
interval = [1, 5]  # starts at 1, ends at 5 (inclusive or exclusive)

# Overlap check
def overlaps(a: list[int], b: list[int]) -> bool:
    """Check if two intervals overlap."""
    return a[0] <= b[1] and b[0] <= a[1]

# Merge two overlapping intervals
def merge_two(a: list[int], b: list[int]) -> list[int]:
    """Merge two overlapping intervals."""
    return [min(a[0], b[0]), max(a[1], b[1])]
```

### Visual: Overlap Cases

```
Overlap:
|----A----|
     |----B----|

|----A----|
  |--B--|

     |----A----|
|----B----|

No Overlap:
|----A----|
              |----B----|
```

---

## Template: Merge Intervals

### Problem: Merge Intervals
**Problem Statement:** Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Why it works:**
Sorting by start time ensures that any potential overlapping intervals are adjacent in the list.
1. We sort the intervals.
2. We initialize our result with the first interval.
3. For each subsequent interval, if its start is less than or equal to the end of our last merged interval, they overlap. We update the end of the last merged interval.
4. If they don't overlap, we add the current interval as a new entry.
Sorting is the key that simplifies the complex pairwise comparison into a single O(n) pass.

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge all overlapping intervals.

    Time: O(n log n) for sorting
    Space: O(n) for output

    Example:
    [[1,3], [2,6], [8,10], [15,18]]
    → [[1,6], [8,10], [15,18]]
    """
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    result = [intervals[0]]

    for i in range(1, len(intervals)):
        current = intervals[i]
        last = result[-1]

        if current[0] <= last[1]:  # Overlaps
            last[1] = max(last[1], current[1])
        else:
            result.append(current)

    return result
```

---

## Template: Insert Interval

### Problem: Insert Interval
**Problem Statement:** You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `new_interval = [start, end]` that represents the start and end of another interval. Insert `new_interval` into `intervals` such that `intervals` is still sorted in ascending order by `start_i` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).

**Why it works:**
Since the input is already sorted, we can process it in three linear phases:
1. **Before**: Add all intervals that end before the new interval starts.
2. **Merge**: While intervals overlap with the new interval, update the new interval's boundaries (`min` of starts, `max` of ends).
3. **After**: Add the merged new interval and then all remaining original intervals.
This O(n) approach preserves the sorted property without needing to re-sort.

```python
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """
    Insert new interval and merge if necessary.
    Input intervals are already sorted and non-overlapping.

    Time: O(n)
    Space: O(n)

    Example:
    intervals = [[1,3], [6,9]], new = [2,5]
    → [[1,5], [6,9]]
    """
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals ending before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # Merge all overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)

    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

---

## Template: Meeting Rooms (Can Attend All)

```python
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    """
    Check if person can attend all meetings (no overlaps).

    Time: O(n log n)
    Space: O(1)

    Example:
    [[0,30], [5,10], [15,20]] → False
    [[7,10], [2,4]] → True
    """
    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False

    return True
```

---

## Template: Meeting Rooms II (Minimum Rooms)

### Problem: Meeting Rooms II
**Problem Statement:** Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.

**Why it works:**
The number of rooms needed is the maximum number of meetings occurring at the same time.
1. We treat starts and ends as separate "events" on a timeline.
2. A start event adds a room (`+1`), and an end event releases a room (`-1`).
3. By sorting all events chronologically and processing them, the maximum value reached by our running sum is our answer.
This effectively counts the number of overlapping intervals at every point in time.

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Find minimum number of meeting rooms required.

    Time: O(n log n)
    Space: O(n)

    Example:
    [[0,30], [5,10], [15,20]] → 2
    [[7,10], [2,4]] → 1
    """
    if not intervals:
        return 0

    # Event-based approach
    events = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

    events.sort()

    rooms = 0
    max_rooms = 0

    for _, delta in events:
        rooms += delta
        max_rooms = max(max_rooms, rooms)

    return max_rooms
```

### Alternative: Using Min-Heap

```python
import heapq

def min_meeting_rooms_heap(intervals: list[list[int]]) -> int:
    """
    Using min-heap to track end times.

    Heap contains end times of ongoing meetings.
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])

    # Min-heap of end times
    heap = [intervals[0][1]]

    for i in range(1, len(intervals)):
        # If current meeting starts after earliest ending meeting
        if intervals[i][0] >= heap[0]:
            heapq.heappop(heap)

        heapq.heappush(heap, intervals[i][1])

    return len(heap)
```

---

## Template: Interval Intersection

### Problem: Interval List Intersections
**Problem Statement:** You are given two lists of closed intervals, `firstList` and `secondList`, where `firstList[i] = [start_i, end_i]` and `secondList[j] = [start_j, end_j]`. Each list of intervals is pairwise disjoint and in sorted order. Return the intersection of these two interval lists.

**Why it works:**
We use a two-pointer approach to compare intervals from both lists.
1. An intersection exists if `max(start1, start2) <= min(end1, end2)`.
2. After finding an intersection (or lack thereof), we move the pointer pointing to the interval that ends earlier, because that interval cannot possibly overlap with any future intervals from the other list.
The linear scan is efficient because both lists are already sorted.

```python
def interval_intersection(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """
    Find intersection of two lists of intervals.
    Both lists are sorted and internally non-overlapping.

    Time: O(m + n)
    Space: O(min(m, n)) for output

    Example:
    A = [[0,2], [5,10]], B = [[1,5], [8,12]]
    → [[1,2], [5,5], [8,10]]
    """
    result = []
    i = j = 0

    while i < len(A) and j < len(B):
        # Find intersection
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])

        if start <= end:
            result.append([start, end])

        # Move pointer with smaller end
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return result
```

---

## Template: Remove Covered Intervals

```python
def remove_covered_intervals(intervals: list[list[int]]) -> int:
    """
    Remove intervals that are covered by another interval.
    Return count of remaining intervals.

    Interval [a,b] is covered by [c,d] if c <= a and b <= d.

    Time: O(n log n)
    Space: O(1)

    Example:
    [[1,4], [2,3], [3,6]] → 2
    Explanation: [2,3] is covered by [1,4], so we remove it.
    Remaining: [[1,4], [3,6]]
    """
    # Sort by start ascending, then by end descending
    intervals.sort(key=lambda x: (x[0], -x[1]))

    count = 0
    max_end = 0

    for _, end in intervals:
        if end > max_end:
            count += 1
            max_end = end

    return count
```

---

## Template: Non-Overlapping Intervals (Min Removals)

### Problem: Non-overlapping Intervals
**Problem Statement:** Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

**Why it works:**
To keep the maximum number of intervals, we should always pick the interval that ends the earliest among all available non-overlapping ones.
1. We sort by end time.
2. We keep the first interval.
3. For each subsequent interval, if it starts before our last kept interval ends, it overlaps. We must remove it.
4. If it doesn't overlap, we keep it and update our `prev_end`.
This greedy strategy ensures we leave as much room as possible for future intervals.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Minimum number of intervals to remove to make rest non-overlapping.

    Greedy: Always keep interval that ends earliest.

    Time: O(n log n)
    Space: O(1)

    Example:
    [[1,2], [2,3], [3,4], [1,3]] → 1 (remove [1,3])
    """
    if not intervals:
        return 0

    # Sort by end time
    intervals.sort(key=lambda x: x[1])

    count = 0
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            # Overlap: remove current (it ends later)
            count += 1
        else:
            prev_end = intervals[i][1]

    return count
```

---

## Template: Employee Free Time

```python
def employee_free_time(schedule: list[list[list[int]]]) -> list[list[int]]:
    """
    Find common free time among all employees.
    Each employee has list of working intervals.

    Time: O(n log n) where n = total intervals
    Space: O(n)

    Example:
    [[[1,2], [5,6]], [[1,3]], [[4,10]]]
    → [[3,4]] (free time between 3 and 4)
    """
    # Flatten all intervals
    all_intervals = []
    for employee in schedule:
        all_intervals.extend(employee)

    # Sort by start time
    all_intervals.sort(key=lambda x: x[0])

    result = []
    prev_end = all_intervals[0][1]

    for interval in all_intervals[1:]:
        if interval[0] > prev_end:
            result.append([prev_end, interval[0]])
        prev_end = max(prev_end, interval[1])

    return result
```

---

## Sorting Strategies

| Sort By             | Use Case                         |
| ------------------- | -------------------------------- |
| Start time          | Merging, insertion               |
| End time            | Activity selection, min removals |
| Start asc, end desc | Covered intervals                |
| Events (start/end)  | Counting concurrent              |

---

## Edge Cases

```python
# Empty input
[] → return [] or 0

# Single interval
[[1, 5]] → no merge possible

# Adjacent intervals (touching)
[[1, 2], [2, 3]] → depends on problem
  Some: merge to [1, 3]
  Some: keep separate

# Completely contained
[[1, 10], [3, 5]] → merge to [1, 10]

# All overlapping
[[1, 4], [2, 5], [3, 6]] → [1, 6]

# No overlapping
[[1, 2], [5, 6]] → same as input
```

---

## Practice Problems

| #   | Problem                     | Difficulty | Key Technique       |
| --- | --------------------------- | ---------- | ------------------- |
| 1   | Merge Intervals             | Medium     | Sort + merge        |
| 2   | Insert Interval             | Medium     | Three passes        |
| 3   | Meeting Rooms               | Easy       | Check overlaps      |
| 4   | Meeting Rooms II            | Medium     | Events or heap      |
| 5   | Non-overlapping Intervals   | Medium     | Greedy by end time  |
| 6   | Interval List Intersections | Medium     | Two pointers        |
| 7   | Remove Covered Intervals    | Medium     | Sort by start, -end |
| 8   | Employee Free Time          | Hard       | Merge all           |

---

## Key Takeaways

1. **Sort first** - almost always necessary
2. **Overlap check**: `a.start <= b.end and b.start <= a.end`
3. **Merge**: `[min(starts), max(ends)]`
4. **For min rooms**: count concurrent via events
5. **For min removals**: greedy by end time
6. **Two pointers** for intersecting sorted lists

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
