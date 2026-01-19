# Merge Intervals

> **Prerequisites:** [Interval Scheduling](./02-interval-scheduling.md)

## Interview Context

Merge intervals tests:
1. **Interval manipulation**: Core skill for many problems
2. **Sorting intuition**: Why sort by start time here
3. **Edge case handling**: Adjacent intervals, single intervals
4. **In-place vs new array**: Space optimization

---

## Problem Statement

Given an array of intervals, merge all overlapping intervals.

```
Input:  intervals = [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]

Explanation: [1,3] and [2,6] overlap, merge to [1,6]
```

---

## The Core Insight

**Sort by start time, then merge overlapping intervals linearly.**

After sorting by start time:
- If current interval overlaps with previous, extend the previous
- If no overlap, start a new merged interval

```
Why sort by start time (not end time)?

When processing left to right after start-sort:
- We know all following intervals start after (or at) current
- If they overlap, they must start before current ends
- Easy to check: next.start <= current.end → overlap

End time sort doesn't give us this property:
- An early-ending interval could start much later
- Would need to compare both start and end
```

---

## Solution

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals.

    Time: O(n log n) for sorting
    Space: O(n) for output (O(1) extra if in-place sort)
    """
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last = merged[-1]

        if start <= last[1]:  # Overlapping
            # Extend the last interval
            last[1] = max(last[1], end)
        else:
            # No overlap, add new interval
            merged.append([start, end])

    return merged
```

---

## Visual Trace

```
Input: [[1,3], [2,6], [8,10], [15,18]]

After sort by start: [[1,3], [2,6], [8,10], [15,18]]

Timeline:
[1,3]:    |---|
[2,6]:     |-----|
[8,10]:              |--|
[15,18]:                    |---|

Step-by-step:
1. merged = [[1,3]]
2. [2,6]: start=2 <= merged[-1][1]=3, overlap!
   → merged[-1][1] = max(3, 6) = 6
   → merged = [[1,6]]
3. [8,10]: start=8 > merged[-1][1]=6, no overlap
   → merged = [[1,6], [8,10]]
4. [15,18]: start=15 > merged[-1][1]=10, no overlap
   → merged = [[1,6], [8,10], [15,18]]

Output: [[1,6], [8,10], [15,18]]
```

---

## Overlap Detection

```
Two intervals [a, b] and [c, d] overlap if and only if:
    a <= d AND c <= b

When sorted by start (a <= c guaranteed):
    Overlap iff c <= b (next.start <= current.end)

Visual:
Case 1: Overlap (c <= b)
[a----b]
   [c----d]    → merge to [a, max(b,d)]

Case 2: No overlap (c > b)
[a--b]
        [c--d]  → separate intervals

Case 3: Contained (c <= b and d <= b)
[a--------b]
   [c--d]      → merge to [a, b] (b already covers)
```

---

## Insert Interval (Related Problem)

Insert a new interval into sorted non-overlapping intervals.

```python
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """
    Insert interval and merge if necessary.

    Time: O(n)
    Space: O(n) for output
    """
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals that come before new interval
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals with new
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

---

## Interval List Intersections

Find intersections between two sorted interval lists.

```python
def interval_intersection(
    first: list[list[int]],
    second: list[list[int]]
) -> list[list[int]]:
    """
    Find all intersections between two interval lists.

    Time: O(n + m)
    Space: O(1) extra
    """
    result = []
    i = j = 0

    while i < len(first) and j < len(second):
        a_start, a_end = first[i]
        b_start, b_end = second[j]

        # Check for intersection
        start = max(a_start, b_start)
        end = min(a_end, b_end)

        if start <= end:  # Valid intersection
            result.append([start, end])

        # Move pointer with earlier end
        if a_end < b_end:
            i += 1
        else:
            j += 1

    return result
```

### Visual Example

```
first:  [[0,2], [5,10], [13,23], [24,25]]
second: [[1,5], [8,12], [15,24], [25,26]]

Intersection finding:
[0,2] ∩ [1,5] = [1,2] ✓
      [1,5] ∩ [5,10] = [5,5] ✓
[5,10] ∩ [8,12] = [8,10] ✓
[13,23] ∩ [15,24] = [15,23] ✓
[24,25] ∩ [15,24] = [24,24] ✓
[24,25] ∩ [25,26] = [25,25] ✓

Result: [[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]
```

---

## Remove Covered Intervals

Remove intervals that are covered by another interval.

```python
def remove_covered_intervals(intervals: list[list[int]]) -> int:
    """
    Return count of intervals that are NOT covered by another.

    Interval [a,b] is covered by [c,d] if c <= a and b <= d.

    Time: O(n log n)
    Space: O(1)
    """
    # Sort by start asc, then by end desc
    # This way, if same start, longer interval comes first
    intervals.sort(key=lambda x: (x[0], -x[1]))

    count = 0
    max_end = 0

    for start, end in intervals:
        if end > max_end:
            # Not covered by previous
            count += 1
            max_end = end
        # else: covered by some previous interval

    return count
```

### Why Sort by (start, -end)?

```
intervals = [[1,4], [1,2], [3,4]]

Sort by (start, end): [[1,2], [1,4], [3,4]]
- Process [1,2]: count=1, max_end=2
- Process [1,4]: 4 > 2, count=2, max_end=4
- Process [3,4]: 4 <= 4, covered? But [3,4] not covered by [1,2]!
  Problem: We updated max_end to 4 from [1,4], hiding that [1,2] can't cover [3,4]

Sort by (start, -end): [[1,4], [1,2], [3,4]]
- Process [1,4]: count=1, max_end=4
- Process [1,2]: 2 <= 4, covered ✓ (by [1,4])
- Process [3,4]: 4 <= 4, covered ✓ (by [1,4])

The -end ensures longer intervals at same start come first,
so they can "cover" shorter ones.
```

---

## Employee Free Time

Find common free time across all employees.

```python
def employee_free_time(schedules: list[list[list[int]]]) -> list[list[int]]:
    """
    Find intervals where all employees are free.

    Time: O(n log n) where n = total intervals
    Space: O(n)
    """
    # Flatten all schedules
    all_intervals = []
    for schedule in schedules:
        all_intervals.extend(schedule)

    # Sort by start time
    all_intervals.sort(key=lambda x: x[0])

    # Merge intervals to find busy times
    merged = [all_intervals[0]]
    for start, end in all_intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    # Gaps between merged intervals = free time
    free = []
    for i in range(1, len(merged)):
        free.append([merged[i-1][1], merged[i][0]])

    return free
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Merge intervals | O(n log n) | O(n) | Sorting dominates |
| Insert interval | O(n) | O(n) | Already sorted |
| Interval intersection | O(n + m) | O(1) | Two pointers |
| Remove covered | O(n log n) | O(1) | Special sort |
| Employee free time | O(n log n) | O(n) | Flatten + merge |

---

## Edge Cases

- [ ] Empty input → return []
- [ ] Single interval → return [interval]
- [ ] No overlaps → return all intervals
- [ ] All overlap → return single merged interval
- [ ] Adjacent intervals [1,2], [2,3] → merge or not? (clarify!)
- [ ] Intervals in any order → sorting handles this

---

## Adjacent vs Overlapping

**Important interview clarification**:

```
Intervals [1,2] and [2,3]:
- Some problems: these overlap (share point 2)
- Some problems: these don't overlap (touching but separate)

Merge code difference:
- Merge touching: if start <= last[1]
- Don't merge touching: if start < last[1]

Always clarify with interviewer!
```

---

## Sorting Comparison

| Problem | Sort By | Why |
|---------|---------|-----|
| Merge intervals | Start | Process left to right, extend end |
| Activity selection | End | Pick earliest finish |
| Meeting rooms II | Start (or both) | Process in order |
| Remove covered | (Start, -End) | Longer first at same start |

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Merge Intervals | Medium | Sort by start, extend end |
| 2 | Insert Interval | Medium | Three phases: before, merge, after |
| 3 | Interval List Intersections | Medium | Two pointers |
| 4 | Remove Covered Intervals | Medium | Sort by (start, -end) |
| 5 | Employee Free Time | Hard | Merge all, find gaps |

---

## Interview Tips

1. **Sort by start time**: Different from activity selection
2. **Clarify overlap definition**: Adjacent intervals?
3. **Use max for merging**: `new_end = max(current_end, next_end)`
4. **Draw the timeline**: Visual helps catch edge cases
5. **Consider insert variant**: No re-sorting needed if already sorted

---

## Key Takeaways

1. Merge intervals: sort by start, extend by max end
2. Different from activity selection (which sorts by end)
3. Overlap check after sorting: `next.start <= current.end`
4. Insert interval: three-phase approach (before, merge, after)
5. Always clarify if adjacent intervals should merge

---

## Next: [04-meeting-rooms.md](./04-meeting-rooms.md)

Learn meeting rooms problems - detecting conflicts and finding minimum rooms.
