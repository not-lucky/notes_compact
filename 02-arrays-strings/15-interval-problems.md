# Interval Problems

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

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
    [[1,4], [3,6], [2,8]] → 2 ([1,4] covered by [2,8]... wait no)
    Actually: [[1,4], [2,8]] remain, [3,6] is not covered
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

| Sort By | Use Case |
|---------|----------|
| Start time | Merging, insertion |
| End time | Activity selection, min removals |
| Start asc, end desc | Covered intervals |
| Events (start/end) | Counting concurrent |

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

| # | Problem | Difficulty | Key Technique |
|---|---------|------------|---------------|
| 1 | Merge Intervals | Medium | Sort + merge |
| 2 | Insert Interval | Medium | Three passes |
| 3 | Meeting Rooms | Easy | Check overlaps |
| 4 | Meeting Rooms II | Medium | Events or heap |
| 5 | Non-overlapping Intervals | Medium | Greedy by end time |
| 6 | Interval List Intersections | Medium | Two pointers |
| 7 | Remove Covered Intervals | Medium | Sort by start, -end |
| 8 | Employee Free Time | Hard | Merge all |

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
