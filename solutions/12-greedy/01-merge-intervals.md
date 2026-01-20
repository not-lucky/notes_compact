# Merge Intervals

## Problem Statement

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Example:**
```
Input: intervals = [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]
Explanation: [1,3] and [2,6] overlap, merge into [1,6].
```

## Building Intuition

### Why This Works

Sorting by start time is the key insight that makes this problem tractable. Once sorted, intervals that could potentially merge are adjacent in the list. You never need to look back more than one interval because if interval A doesn't overlap with the last merged interval, no future interval will either (they all start even later).

Two intervals [a, b] and [c, d] overlap if and only if c <= b (assuming they're sorted by start, so a <= c). When they overlap, the merged interval is [a, max(b, d)] - start from the earlier interval, end at the later endpoint. This "extend the end if necessary" logic handles both partial overlap and complete containment.

The greedy choice is: always try to merge with the previous interval. This works because sorting ensures we process intervals in the order they "begin," and once an interval's end is finalized, no future interval can affect it (they start later).

### How to Discover This

Interval problems almost always start with sorting. Ask: "In what order would processing be easiest?" Sorting by start time groups overlapping intervals together. Then ask: "What's the simplest decision at each step?" Here, it's: "Does this interval overlap with the last one? If yes, merge. If no, start a new group."

### Pattern Recognition

This is the **Interval Processing** pattern. Recognize it when:
- You're dealing with ranges/intervals
- The problem involves overlap detection, scheduling, or partitioning
- Sorting would create useful structure

## When NOT to Use

- **When intervals have weights/priorities and you need optimal selection**: Use interval scheduling (greedy by end time) or DP.
- **When you can't modify the input and need sorted order**: You'd need O(n) extra space for a sorted copy.
- **When intervals are already non-overlapping**: No merging needed; just verify or count.
- **When the problem requires considering all pairs of intervals**: Sorting alone doesn't help; you might need O(n^2) comparisons.

## Approach

### Key Insight
1. Sort intervals by start time
2. Merge if current interval overlaps with previous
3. Two intervals [a,b] and [c,d] overlap if c <= b (when sorted by start)

## Implementation

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals.

    Time: O(n log n) - sorting
    Space: O(n) - output
    """
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for interval in intervals[1:]:
        # If overlaps with last merged
        if interval[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], interval[1])
        else:
            merged.append(interval)

    return merged


def merge_in_place(intervals: list[list[int]]) -> list[list[int]]:
    """
    In-place merging approach.
    """
    intervals.sort()

    i = 0
    while i < len(intervals) - 1:
        if intervals[i][1] >= intervals[i + 1][0]:
            intervals[i][1] = max(intervals[i][1], intervals[i + 1][1])
            intervals.pop(i + 1)
        else:
            i += 1

    return intervals
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n log n) | Dominated by sorting |
| Space | O(n) | Output array |

## Visual Walkthrough

```
intervals = [[1,3], [2,6], [8,10], [15,18]]

After sorting (already sorted):
[1,3], [2,6], [8,10], [15,18]

Step 1: merged = [[1,3]]
Step 2: [2,6] - 2 <= 3, overlap! merged = [[1,6]]
Step 3: [8,10] - 8 > 6, no overlap. merged = [[1,6], [8,10]]
Step 4: [15,18] - 15 > 10, no overlap. merged = [[1,6], [8,10], [15,18]]
```

## Edge Cases

1. **Empty input**: Return []
2. **Single interval**: Return as is
3. **No overlaps**: Return sorted intervals
4. **All overlap**: Single merged interval
5. **Nested intervals**: [1,10], [2,5] → [1,10]

## Variations

### Insert Interval
```python
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """
    Insert new interval into sorted non-overlapping intervals.

    Time: O(n)
    Space: O(n)
    """
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals before new
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

### Meeting Rooms II
```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Find minimum meeting rooms needed.

    Time: O(n log n)
    Space: O(n)
    """
    import heapq

    if not intervals:
        return 0

    intervals.sort()  # Sort by start time

    # Min heap of end times
    rooms = [intervals[0][1]]

    for start, end in intervals[1:]:
        if start >= rooms[0]:
            # Can reuse earliest ending room
            heapq.heappop(rooms)
        heapq.heappush(rooms, end)

    return len(rooms)


def min_meeting_rooms_sweep(intervals: list[list[int]]) -> int:
    """
    Line sweep approach.
    """
    events = []
    for start, end in intervals:
        events.append((start, 1))   # +1 for start
        events.append((end, -1))    # -1 for end

    events.sort()

    max_rooms = current = 0
    for _, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)

    return max_rooms
```

### Non-overlapping Intervals
```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Minimum intervals to remove for no overlap.

    Greedy: Keep interval with earliest end time.

    Time: O(n log n)
    Space: O(1)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])  # Sort by end time

    count = 0
    prev_end = float('-inf')

    for start, end in intervals:
        if start >= prev_end:
            # No overlap, keep this interval
            prev_end = end
        else:
            # Overlap, remove this interval
            count += 1

    return count
```

## Related Problems

- **Insert Interval** - Insert and merge
- **Meeting Rooms** - Can attend all meetings?
- **Meeting Rooms II** - Minimum rooms needed
- **Non-overlapping Intervals** - Minimum removals
- **Employee Free Time** - Merge across employees
