# Merge Intervals

> **Prerequisites:** [Interval Scheduling](./02-interval-scheduling.md)

## Interview Context

Merge intervals tests:

1. **Interval manipulation**: Core building block for many interval problems
2. **Sorting intuition**: Why sort by start time (not end time) for merging
3. **Edge case handling**: Adjacent, contained, and single intervals
4. **In-place vs new array**: Space optimization trade-offs

---

## Building Intuition

**The Timeline Visualization**

Imagine laying out all intervals on a number line. Overlapping intervals form "clusters." Our goal is to find these clusters and report their spans.

```
Input: [[1,3], [2,6], [8,10], [15,18]]

Timeline:
1   2   3   4   5   6   7   8   9  10  11 ... 15  16  17  18
|---+---|
    |---+---+---+---|
                        |---+---|
                                            |---+---+---|

Clusters: [1,6], [8,10], [15,18]
```

**Why Sort by START Time (Not End)?**

Sorting by start time guarantees a critical invariant:

> After sorting, every future interval starts at or after the current one.
> Therefore, any overlap must be with the **latest** cluster -- we never need to revisit earlier clusters.

This gives us a clean single-pass algorithm: scan left-to-right, and each new interval either **extends** the current cluster or **starts** a new one.

```
Sorted by start: [[1,3], [2,6], [8,10], [15,18]]

Scan:
- [1,3]:  Start first cluster → [1,3]
- [2,6]:  2 <= 3? Yes → extend cluster to [1,6]
- [8,10]: 8 <= 6? No  → close [1,6], start new cluster [8,10]
- [15,18]:15 <= 10? No → close [8,10], start new cluster [15,18]

Result: [1,6], [8,10], [15,18]
```

**Why End-Time Sort Breaks Merging**

```
Intervals: [[0,10], [1,2], [3,4]]

Sorted by end: [[1,2], [3,4], [0,10]]

Processing left-to-right:
- [1,2]: Start cluster [1,2]
- [3,4]: 3 > 2, no overlap → new cluster [3,4]
- [0,10]: 0 <= 4? Yes, merge with [3,4]... but [0,10] also overlaps [1,2]!

We'd need to LOOK BACK and re-merge earlier clusters, defeating the single-pass approach.
Correct answer: one merged cluster [0,10].
```

**Why start-sort avoids this**: With start-sort, `[0,10]` comes first. Then `[1,2]` and `[3,4]` both have `start <= 10`, so they merge into the existing cluster. No look-back needed.

**The "Extend or Close" Decision**

At each step, we make exactly one decision:

```python
if new_start <= current_end:
    # EXTEND: new interval overlaps or touches current cluster
    current_end = max(current_end, new_end)
else:
    # CLOSE: output current cluster, start new one
    output(current_cluster)
    current_cluster = new_interval
```

**Why `max(current_end, new_end)`?** Because the new interval might be fully contained inside the current cluster (e.g., `[1,10]` then `[2,3]`). Taking the max ensures we never shrink the cluster.

---

## Problem Statement

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

```
Input:  intervals = [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]

Explanation: [1,3] and [2,6] overlap, merge to [1,6]
```

---

## Solution

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals.

    Time:  O(n log n) — sorting dominates
    Space: O(n) for output array
    """
    if not intervals:
        return []

    # Sort by start time (creates a new list, avoiding input mutation)
    intervals = sorted(intervals, key=lambda x: x[0])

    merged = [intervals[0]]

    # Process all subsequent intervals
    for current_start, current_end in intervals[1:]:
        last_merged = merged[-1]

        if current_start <= last_merged[1]:
            # Overlaps or touches — extend the cluster's end (Union)
            last_merged[1] = max(last_merged[1], current_end)
        else:
            # No overlap — start a new cluster
            merged.append([current_start, current_end])

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
1. Initialize: merged = [[1,3]]

2. Process [2,6]:
   start=2 <= merged[-1][1]=3 (overlap!)
   → merged[-1][1] = max(3, 6) = 6
   → merged = [[1,6]]

3. Process [8,10]:
   start=8 > merged[-1][1]=6 (no overlap)
   → append [8,10]
   → merged = [[1,6], [8,10]]

4. Process [15,18]:
   start=15 > merged[-1][1]=10 (no overlap)
   → append [15,18]
   → merged = [[1,6], [8,10], [15,18]]

Output: [[1,6], [8,10], [15,18]]
```

**Contained interval trace** (common edge case):

```
Input: [[1,10], [2,3], [4,5]]

After sort: [[1,10], [2,3], [4,5]]

1. Initialize: merged = [[1,10]]

2. Process [2,3]:
   start=2 <= 10 (overlap)
   → max(10, 3) = 10 — end stays at 10 (contained!)
   → merged = [[1,10]]

3. Process [4,5]:
   start=4 <= 10 (overlap)
   → max(10, 5) = 10 — end stays at 10 (also contained)
   → merged = [[1,10]]

Output: [[1,10]]
```

---

## Overlap Detection

**General rule:** Two intervals `[a, b]` and `[c, d]` overlap (or touch) if and only if `a <= d AND c <= b`.

**Why this works:** For overlap, neither interval can be completely to the right of the other:
- If `b < c`: `[a,b]` ends before `[c,d]` starts -- no overlap
- If `d < a`: `[c,d]` ends before `[a,b]` starts -- no overlap
- Otherwise: they overlap (or touch at endpoints)

**After sorting by start** (`a <= c` guaranteed for intervals processed in order):
- The condition `a <= d` is automatically satisfied (since `a <= c` and `c <= d`)
- We only need to check: `c <= b` (next start <= current end)

```
Case 1: Partial overlap (c <= b, d > b)
[a----b]
   [c----d]    → merge to [a, max(b,d)] = [a, d]

Case 2: No overlap (c > b)
[a--b]
        [c--d]  → separate intervals

Case 3: Contained (c <= b, d <= b)
[a--------b]
   [c--d]      → merge to [a, max(b,d)] = [a, b]

All three cases handled by the same formula: [a, max(b,d)]
```

**Touching vs Overlapping:**
- Touching: `[1,2]` and `[2,3]` share only the endpoint 2
- Overlapping: `[1,3]` and `[2,4]` share a range `[2,3]`
- Whether touching counts as "overlap" depends on problem semantics (clarify with interviewer)

---

## When NOT to Use Standard Merge

**1. When Intervals Have Weights/Priorities**

If some intervals are "more important" and can override others:

```
Intervals: [(0, 10, 1), (2, 5, 2)]  # (start, end, priority)
Standard merge: [0, 10]
Weighted: [0, 2) = priority 1, [2, 5] = priority 2, (5, 10] = priority 1
```

This requires a sweep line with priority tracking.

**2. When You Need to Track Which Intervals Merged**

Standard merge loses the identity of merged intervals. If you need to know "which original intervals are in this merged cluster," maintain additional bookkeeping.

**3. When Intervals Represent Different Resources**

If intervals are for different resources (different meeting rooms, different people), you can't merge across resources.

**4. Overlap Detection vs Merge**

Sometimes you just need to check IF any overlap exists (Meeting Rooms I). Full merging is overkill:

```python
def has_overlap(intervals: list[list[int]]) -> bool:
    """
    Check if any intervals overlap (for Meeting Rooms I).

    Time:  O(n log n) for sorting
    Space: O(n) for sorted copy
    """
    intervals = sorted(intervals)  # Sort by start time
    for i in range(1, len(intervals)):
        # Strict < means touching intervals [1,2] and [2,3] do NOT conflict
        # Use <= if touching should count as overlap
        if intervals[i][0] < intervals[i - 1][1]:
            return True
    return False
```

Note: This uses strict `<` because in Meeting Rooms I, `[1,2]` and `[2,3]` do not conflict (one ends as the other starts). Use `<=` if touching intervals should count as overlapping.

---

## Sweep Line Algorithm (General Pattern)

The **sweep line algorithm** is a more general technique that encompasses merge intervals. It's useful when:
- You need to track overlapping counts (e.g., "maximum meetings at any time")
- Intervals have different weights or types
- You need to answer queries about specific time points

**The Pattern:**
1. Convert each interval `[start, end]` into two events: `(start, +1)` and `(end, -1)`
2. Sort all events by time (handle ties carefully based on problem semantics)
3. Sweep through events, maintaining a running count

```python
def max_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Find the maximum number of overlapping intervals at any time.
    This is the core of Meeting Rooms II.

    Time:  O(n log n) for sorting events
    Space: O(n) for events list
    """
    events = []

    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

    # Sort by time; if times equal, process ends (-1) before starts (+1)
    # so that [1,2] and [2,3] don't count as overlapping
    events = sorted(events, key=lambda x: (x[0], x[1]))

    max_rooms = 0
    current_rooms = 0

    for _, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)

    return max_rooms
```

**Tie-breaking intuition:**
- `(time, -1)` before `(time, 1)`: ending before starting -- touching intervals don't overlap
- `(time, 1)` before `(time, -1)`: starting before ending -- touching intervals DO overlap

---

## Practice Problem 1: Insert Interval (LC 57)

Insert a new interval into a sorted, non-overlapping list and merge if necessary. Since the input is already sorted, no re-sorting is needed -- we use a three-phase linear scan.

**Key idea:** Partition existing intervals into three groups:
1. **Before**: ends before the new interval starts (no overlap possible)
2. **Overlapping**: overlaps with the new interval (merge them all)
3. **After**: starts after the new interval ends (no overlap possible)

```python
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """
    Insert new_interval into sorted non-overlapping intervals, merging as needed.

    Time:  O(n) — single pass
    Space: O(n) for output
    """
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: Add all intervals that come completely before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: Merge all intervals that overlap with new_interval
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)

    # Phase 3: Add all remaining intervals that come completely after
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

**Visual trace:**

```
intervals = [[1,2], [3,5], [6,7], [8,10], [12,16]]
new_interval = [4,8]

Phase 1 — before [4,8]:
  [1,2]: end=2 < 4 → add to result. result = [[1,2]]
  [3,5]: end=5 >= 4 → stop

Phase 2 — overlapping with [4,8]:
  [3,5]: start=3 <= 8 → merge: new_interval[0] = min(4,3)=3, new_interval[1] = max(8,5)=8
  [6,7]: start=6 <= 8 → merge: new_interval[0] = min(3,6)=3, new_interval[1] = max(8,7)=8
  [8,10]: start=8 <= 8 → merge: new_interval[0] = min(3,8)=3, new_interval[1] = max(8,10)=10
  [12,16]: start=12 > 10 → stop (note: comparison is against updated new_interval[1]=10)
  Add [3,10] to result. result = [[1,2], [3,10]]

Phase 3 — after:
  Add [12,16]. result = [[1,2], [3,10], [12,16]]
```

---

## Practice Problem 2: Interval List Intersections (LC 986)

Find all pairwise intersections between two sorted, non-overlapping interval lists. Since both lists are already sorted, we use a two-pointer approach.

**Key insight:** Two intervals intersect if and only if `start <= end` where `start = max(a_start, b_start)` and `end = min(a_end, b_end)`. After recording the intersection, advance the pointer whose interval ends earlier -- the other interval might still intersect with the next one.

```python
def interval_intersection(
    first: list[list[int]],
    second: list[list[int]]
) -> list[list[int]]:
    """
    Find all intersections between two sorted, non-overlapping interval lists.

    Time:  O(n + m)
    Space: O(1) extra (excluding output)
    """
    result = []
    i = j = 0

    while i < len(first) and j < len(second):
        a_start, a_end = first[i]
        b_start, b_end = second[j]

        # Intersection = [later start, earlier end]
        start = max(a_start, b_start)
        end = min(a_end, b_end)

        if start <= end:
            result.append([start, end])

        # Advance the pointer whose interval ends first —
        # the other interval might still intersect with the next one
        if a_end < b_end:
            i += 1
        else:
            j += 1

    return result
```

**Why advance the earlier-ending pointer?** If `first[i]` ends before `second[j]`, then `first[i]` cannot possibly intersect with `second[j+1]` or beyond (since `second` is sorted and `second[j]` already extends past `first[i]`). But `second[j]` might still intersect with `first[i+1]`.

**Visual trace:**

```
first:  [[0,2], [5,10], [13,23], [24,25]]
second: [[1,5], [8,12], [15,24], [25,26]]

i=0, j=0: [0,2] ∩ [1,5]  → start=1, end=2 → [1,2] ✓   first ends earlier → i++
i=1, j=0: [5,10]∩ [1,5]  → start=5, end=5 → [5,5] ✓   second ends earlier → j++
i=1, j=1: [5,10]∩ [8,12] → start=8, end=10→ [8,10] ✓  first ends earlier → i++
i=2, j=1: [13,23]∩[8,12] → start=13,end=12→ empty      second ends earlier → j++
i=2, j=2: [13,23]∩[15,24]→ start=15,end=23→ [15,23] ✓  first ends earlier → i++
i=3, j=2: [24,25]∩[15,24]→ start=24,end=24→ [24,24] ✓  second ends earlier → j++
i=3, j=3: [24,25]∩[25,26]→ start=25,end=25→ [25,25] ✓  first ends earlier → i++
                                                      i=4, exit loop

Result: [[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]
```

Note: When both intervals end at the same point, advancing either pointer is correct. In the code above, `else: j += 1` handles both the `>` and `==` cases. This is safe because if both end at the same point, neither can intersect with anything beyond the other's next interval.

---

## Practice Problem 3: Remove Covered Intervals (LC 1288)

An interval `[a,b]` is **covered** by `[c,d]` if `c <= a` and `b <= d`. Remove all covered intervals and return the count of remaining ones.

```python
def remove_covered_intervals(intervals: list[list[int]]) -> int:
    """
    Return count of intervals that are NOT covered by another.

    Interval [a,b] is covered by [c,d] if c <= a and b <= d.

    Time:  O(n log n)
    Space: O(n) for sorted copy
    """
    # Sort by start ascending, then by end descending.
    # If two intervals share the same start, the longer one comes first.
    intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))

    if not intervals:
        return 0

    count = 1
    max_end = intervals[0][1]

    for _, end in intervals[1:]:
        if end > max_end:
            # Not covered by previous interval
            count += 1
            max_end = end
        # else: this interval's end <= max_end, meaning some earlier
        # interval (with <= start and >= end) covers it

    return count
```

**Why sort by `(start, -end)`?**

```
intervals = [[1,4], [1,2], [3,4]]
Correct answer: 1 (only [1,4] survives — it covers both [1,2] and [3,4])

Sort by (start, end):  [[1,2], [1,4], [3,4]]
- [1,2]: count=1, max_end=2
- [1,4]: 4 > 2, count=2, max_end=4   ← WRONG: [1,2] was counted as uncovered
- [3,4]: 4 <= 4, covered ✓
→ Returns 2 (incorrect!)

Sort by (start, -end): [[1,4], [1,2], [3,4]]
- [1,4]: count=1, max_end=4
- [1,2]: 2 <= 4, covered ✓
- [3,4]: 4 <= 4, covered ✓
→ Returns 1 (correct!)

The -end ensures longer intervals at same start come first,
so they can "cover" shorter ones that follow.
```

---

## LC 435 / LC 452 Variant: Removing/Bursting Intervals

**Problem 1 (LC 435)**: Given intervals, find the MINIMUM number of intervals to remove so all remaining intervals are non-overlapping.
**Problem 2 (LC 452)**: Find the minimum arrows to burst all balloons (balloons are intervals, an arrow at `x` bursts all balloons where `start <= x <= end`).

**Key insight**: This is the COMPLEMENT of activity selection! Instead of counting max non-overlapping, we count how many to remove or how many arrows we need.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    LC 435: Minimum intervals to remove to make non-overlapping.

    Greedy: Sort by end time, keep intervals that don't overlap.
    Answer = total - kept

    Time: O(n log n)
    Space: O(n) for sorted copy
    """
    if not intervals:
        return 0

    # Sort by end time
    intervals = sorted(intervals, key=lambda x: x[1])

    count = 1  # At least one interval can be kept
    end = intervals[0][1]

    for start, e in intervals[1:]:
        if start >= end:  # Use > if touching intervals are considered overlapping
            count += 1
            end = e

    return len(intervals) - count

def find_min_arrow_shots(points: list[list[int]]) -> int:
    """
    LC 452: Minimum number of arrows to burst balloons.
    """
    if not points:
        return 0

    points = sorted(points, key=lambda x: x[1])

    arrows = 1
    end = points[0][1]

    for start, e in points[1:]:
        if start > end:  # An arrow at `end` can burst balloons touching it
            arrows += 1
            end = e

    return arrows
```

**Example (Erase Overlap)**:
```
Input: [[1,2], [2,3], [3,4], [1,3]]
Sort by end: [[1,2], [2,3], [3,4], [1,3]]

Keep [1,2], end=2
[2,3]: 2 >= 2 ✓ Keep, end=3
[3,4]: 3 >= 3 ✓ Keep, end=4
[1,3]: 1 < 4 ✗ Remove

Kept: 3, Removed: 1
Answer: 1
```

**Why greedy works**: Same as activity selection - picking the earliest finishing interval leaves maximum room for others.

**Connection to other problems**:
- **LC 435 (Non-overlapping Intervals)**: Finding max intervals we can keep. We are finding intervals to *remove*, so `len(intervals) - kept`.
- **LC 452 (Minimum Number of Arrows to Burst Balloons)**: We want to find the minimum arrows (points) to intersect all intervals. The greedy strategy is almost identical: sort by end time, shoot an arrow at the end of the current interval. Any subsequent balloon starting *before or at* that point is also burst. The only difference is the condition uses `>` instead of `>=` because touching balloons can be burst by the same arrow.

---

## Employee Free Time

Find common free time gaps across all employees' schedules. Each employee's schedule is a sorted list of non-overlapping busy intervals.

**Approach:** Merge all busy intervals across employees, then find the gaps.

### Flatten and Merge (simpler, preferred in interviews)

```python
def employee_free_time(schedules: list[list[list[int]]]) -> list[list[int]]:
    """
    Find intervals where ALL employees are free.

    Time:  O(n log n) where n = total intervals across all employees
    Space: O(n) for the flattened list
    """
    # Flatten all employee schedules into one list
    all_busy = []
    for schedule in schedules:
        all_busy.extend(schedule)

    if not all_busy:
        return []

    # Sort by start time
    all_busy = sorted(all_busy, key=lambda x: x[0])

    # Find gaps between merged busy intervals
    free_times = []
    prev_end = all_busy[0][1]

    for start, end in all_busy[1:]:
        if start > prev_end:
            # Gap found: everyone is free from prev_end to start
            free_times.append([prev_end, start])
        # Extend the current merged busy interval
        prev_end = max(prev_end, end)

    return free_times
```

### Min-Heap (optimal for k sorted lists)

When each employee's schedule is already sorted, we can avoid the $O(n \log n)$ sort by using a min-heap to merge $k$ sorted lists in $O(n \log k)$.

```python
import heapq

def employee_free_time_heap(schedules: list[list[list[int]]]) -> list[list[int]]:
    """
    Find intervals where ALL employees are free.
    Uses a min-heap to merge k sorted interval lists.

    Time:  O(n log k) where n = total intervals, k = number of employees
    Space: O(k) for the heap
    """
    heap = []

    # Initialize heap with the first interval of each employee
    for emp_idx, schedule in enumerate(schedules):
        if schedule:
            start, end = schedule[0]
            heapq.heappush(heap, (start, end, emp_idx, 0))

    if not heap:
        return []

    free_times = []

    # Initialize prev_end with the earliest start time
    # (heap[0][0] is the start time of the earliest interval)
    prev_end = heap[0][0]

    while heap:
        start, end, emp_idx, int_idx = heapq.heappop(heap)

        if start > prev_end:
            # Gap: everyone is free from prev_end to start
            free_times.append([prev_end, start])

        prev_end = max(prev_end, end)

        # Push the next interval for this employee
        next_idx = int_idx + 1
        if next_idx < len(schedules[emp_idx]):
            next_start, next_end = schedules[emp_idx][next_idx]
            heapq.heappush(heap, (next_start, next_end, emp_idx, next_idx))

    return free_times
```

---

## Complexity Analysis

| Operation             | Time            | Space        | Notes                      |
| --------------------- | --------------- | ------------ | -------------------------- |
| Merge intervals       | $O(n \log n)$   | $O(n)$       | Sorting dominates          |
| Insert interval       | $O(n)$          | $O(n)$       | Single pass linear scan    |
| Interval intersection | $O(n + m)$      | $O(1)$ extra | Two pointers               |
| Remove covered        | $O(n \log n)$   | $O(n)$       | Sort by (start, -end)      |
| Erase overlapping     | $O(n \log n)$   | $O(n)$       | Sort by end                |
| Burst balloons        | $O(n \log n)$   | $O(n)$       | Sort by end                |
| Employee free time    | $O(n \log k)$   | $O(k)$       | Min-heap, k = employees    |
| Employee free (flat)  | $O(n \log n)$   | $O(n)$       | Flatten, sort, scan        |

---

## Edge Cases

| Case | Input | Output | Notes |
|------|-------|--------|-------|
| **Empty input** | `[]` | `[]` | Handle with early return |
| **Single interval** | `[[1,5]]` | `[[1,5]]` | Already merged |
| **No overlaps** | `[[1,2], [4,5], [7,8]]` | `[[1,2], [4,5], [7,8]]` | All intervals preserved |
| **All overlap** | `[[1,4], [2,5], [3,6]]` | `[[1,6]]` | Merges into one |
| **Adjacent (touching)** | `[[1,2], [2,3]]` | `[[1,3]]` | `<=` merges, `<` doesn't |
| **Contained interval** | `[[1,10], [2,3], [4,5]]` | `[[1,10]]` | `max(end)` handles this |
| **Duplicate intervals** | `[[1,3], [1,3], [1,3]]` | `[[1,3]]` | All merge together |
| **Unsorted input** | `[[8,10], [1,3], [2,6]]` | `[[1,6], [8,10]]` | Sorting handles this |
| **Negative endpoints** | `[[-5,-2], [-3,0]]` | `[[-5,0]]` | Works with negatives too |

---

## Adjacent vs Overlapping

**Important interview clarification:**

```
Intervals [1,2] and [2,3]:
- LeetCode "Merge Intervals": these overlap (share endpoint 2) → merge to [1,3]
- LeetCode "Meeting Rooms": these do NOT conflict (one ends as the other starts)

The difference in code is a single character:
- Merge touching:      if start <= last_end
- Don't merge touching: if start <  last_end

Always clarify with the interviewer which semantics they want.
```

---

## Sorting Comparison

| Problem            | Sort By         | Why                                        |
| ------------------ | --------------- | ------------------------------------------ |
| Merge intervals    | Start           | Process left-to-right, extend end          |
| Activity selection | End             | Pick earliest finish to maximize count     |
| Meeting rooms II   | Start (or both) | Process arrivals/departures chronologically|
| Remove covered     | (Start, -End)   | Longer interval first at same start        |
| Burst balloons     | End             | Shoot arrow at the end to burst max overlapping |

---

## Common Mistakes

1. **Forgetting `max()` when extending**: Writing `merged[-1][1] = current_end` instead of `merged[-1][1] = max(merged[-1][1], current_end)`. This breaks on contained intervals like `[1,10], [2,3]` where the new interval's end is smaller.

2. **Off-by-one on touching intervals**: Using `<` vs `<=` without thinking about whether touching intervals should merge. Always ask: "Do `[1,2]` and `[2,3]` overlap in this problem?"

3. **Sorting by end instead of start**: End-time sorting works for activity selection (maximize count) but breaks merging (requires look-back).

4. **Mutating input unexpectedly**: `intervals.sort()` modifies the input list. If the caller doesn't expect mutation, use `sorted()` to create a copy.

5. **Not handling the last cluster**: If you use the "close and output" pattern (instead of the `merged` list approach), remember to output the final cluster after the loop ends.

---

## Key Takeaways

1. **Sort by start, merge by max end** -- the core merge pattern. Different from activity selection (which sorts by end)
2. **Overlap check simplifies after sorting**: `next.start <= current.end` is the only comparison needed
3. **Always clarify adjacent intervals**: `<=` merges touching intervals, `<` keeps them separate. One character changes the semantics
4. **Insert interval**: three-phase approach (before, merge, after) avoids re-sorting and runs in $O(n)$
5. **Sweep line is a powerful generalization**: convert intervals to events, sort by time, sweep with running count for problems like "maximum meetings at any time"
6. **Draw the timeline**: visualizing intervals on a number line catches edge cases faster than reasoning abstractly

---

## Next: [04-meeting-rooms.md](./04-meeting-rooms.md)

Learn meeting rooms problems -- detecting conflicts and finding minimum rooms.
