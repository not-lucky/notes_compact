# Interval Scheduling

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Interval scheduling tests:

1. **Greedy intuition**: Sorting by end time (not start time)
2. **Proof understanding**: Why earliest end time is optimal
3. **Pattern recognition**: Identifying interval selection problems
4. **Edge case handling**: Overlapping vs touching intervals

---

## Building Intuition

**The "Room for More" Principle**

Imagine you're scheduling meetings in a single conference room. You want to fit as many meetings as possible. The key insight:

_The earlier a meeting ends, the more time remains for future meetings._

This is why we sort by END time, not start time. Starting early doesn't help if the meeting runs long—what matters is when you're FREE again.

**Mental Model: The Greedy Host**

Think of yourself as a host who must accept/reject meeting requests one at a time. Your strategy:

```
Guest requests:  [9-10:30], [9:30-10], [10-11], [10:30-12]

Sort by end time: [9:30-10], [9-10:30], [10-11], [10:30-12]

Decision process:
1. [9:30-10]: Accept! (ends earliest, leaves most room)
2. [9-10:30]: Reject (conflicts with [9:30-10])
3. [10-11]: Accept! (starts after 10, ends at 11)
4. [10:30-12]: Reject (conflicts with [10-11])

Result: 2 meetings [9:30-10] and [10-11]
```

**Why NOT Sort by Start Time?**

```
Activities: [(0, 100), (1, 2), (3, 4)]

Sort by start:     [(0, 100), (1, 2), (3, 4)]
Greedy picks:      (0, 100) → 1 activity total 😞

Sort by end:       [(1, 2), (3, 4), (0, 100)]
Greedy picks:      (1, 2), then (3, 4) → 2 activities! 😊

The long-running (0, 100) activity "hogs" the room
if we pick it first!
```

**Why NOT Sort by Duration?**

```
Activities: [(0, 5), (4, 6), (5, 10)]
Durations:    5       2       5

Sort by duration: [(4, 6), (0, 5), (5, 10)]
Greedy picks: (4, 6) → blocks both (0, 5) and (5, 10)!
Result: 1 activity

Optimal: (0, 5), (5, 10) → 2 activities
```

---

## When NOT to Use Activity Selection

**1. When Activities Have Weights/Values**

If each activity has a different "profit" or value, greedy fails:

```
Activities: [(0, 5, value=10), (0, 3, value=7), (4, 6, value=8)]

Greedy (by end time): Picks (0, 3), then (4, 6) → value = 15
Optimal: Pick (0, 5) alone → value = 10? No wait...
Actually: (0, 3) + (4, 6) = 15, or (0, 5) alone = 10

In this case greedy works! But consider:
[(0, 10, value=100), (0, 3, value=7), (4, 6, value=8)]

Greedy: (0, 3) + (4, 6) = 15
Optimal: (0, 10) alone = 100 ← Greedy missed this!
```

Use **Weighted Interval Scheduling (DP)** for valued activities.

**2. When You Need Exactly K Activities**

If the goal is "select exactly K non-overlapping activities with max total value," that's a constrained optimization problem needing DP.

**3. When Activities Can Be Split**

If activities can start/pause/resume, the problem becomes entirely different (scheduling theory).

---

## Problem Statement

Given a set of activities with start and end times, select the **maximum number of non-overlapping activities**.

```
Input: activities = [(1,4), (3,5), (0,6), (5,7), (3,8), (5,9), (6,10), (8,11), (8,12), (2,13), (12,14)]
Output: 4 (e.g., activities [(1,4), (5,7), (8,11), (12,14)])
```

This is the classic **Activity Selection Problem**.

---

## The Core Insight

**Sort by end time, greedily pick earliest-ending non-overlapping activity.**

Why end time, not start time?

- Earliest end time leaves maximum room for future activities.
- Starting early doesn't help if the activity runs long.

```
Example showing why start time fails:

Activities: [(0, 10), (1, 2), (3, 4)]

Sort by start time: [(0, 10), (1, 2), (3, 4)]
Greedy picks (0, 10) → blocks (1, 2) and (3, 4) → only 1 activity

Sort by end time: [(1, 2), (3, 4), (0, 10)]
Greedy picks (1, 2), then (3, 4) → 2 activities ✓
```

---

## Solution

```python
def max_activities(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Select maximum number of non-overlapping activities.

    Args:
        activities: List of (start, end) tuples

    Returns:
        List of selected activities

    Time: O(n log n) for sorting
    Space: O(1) extra (excluding output)
    """
    if not activities:
        return []

    # Sort by end time
    activities = sorted(activities, key=lambda x: x[1])

    result = [activities[0]]
    last_end = activities[0][1]

    for start, end in activities[1:]:
        if start >= last_end:  # Non-overlapping
            result.append((start, end))
            last_end = end

    return result


def count_max_activities(activities: list[tuple[int, int]]) -> int:
    """Return count only (more space efficient)."""
    if not activities:
        return 0

    activities.sort(key=lambda x: x[1])

    count = 1
    last_end = activities[0][1]

    for start, end in activities[1:]:
        if start >= last_end:
            count += 1
            last_end = end

    return count
```

---

## Visual Trace

```
Activities: [(1,4), (3,5), (0,6), (5,7), (3,8), (5,9), (6,10), (8,11)]

Sorted by end time:
(1,4):  |---|
(3,5):    |--|
(0,6): |------|
(5,7):      |--|
(3,8):    |-----|
(5,9):      |----|
(6,10):       |----|
(8,11):         |---|

Greedy selection:
1. Pick (1,4):  |===|              last_end = 4
2. (3,5) starts at 3 < 4: SKIP
3. (0,6) starts at 0 < 4: SKIP
4. Pick (5,7):      |==|           last_end = 7
5. (3,8) starts at 3 < 7: SKIP
6. (5,9) starts at 5 < 7: SKIP
7. (6,10) starts at 6 < 7: SKIP
8. Pick (8,11):         |==|       last_end = 11

Result: [(1,4), (5,7), (8,11)] - 3 activities
```

---

## Proof of Correctness

### Greedy Stays Ahead Argument

**Claim**: The greedy algorithm selects as many activities as any optimal solution.

**Proof**:

1. Let $G = \{g_1, g_2, \dots, g_k\}$ be greedy's selection (sorted by end time)
2. Let $O = \{o_1, o_2, \dots, o_m\}$ be any optimal solution (sorted by end time)

**Lemma**: $end(g_i) \le end(o_i)$ for all $i \le \min(k, m)$

**By induction**:

- **Base (i=1)**: $g_1$ has the earliest end time by construction, so $end(g_1) \le end(o_1)$ ✓
- **Inductive step**: Assume $end(g_i) \le end(o_i)$
  - $o_{i+1}$ starts after $end(o_i) \ge end(g_i)$
  - So $o_{i+1}$ is a valid choice after $g_i$
  - Greedy picks the earliest-ending valid activity
  - Therefore $end(g_{i+1}) \le end(o_{i+1})$ ✓

**Conclusion**: Since greedy never falls behind, $k \ge m$. Since $O$ is optimal, $k \le m$. Therefore $k = m$.

---

## Non-overlapping Intervals (Related Problem)

**Problem**: Given intervals, find minimum number to remove for non-overlapping.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Minimum intervals to remove for non-overlapping result.

    Key insight: max_keep = activity selection answer
                 min_remove = total - max_keep

    Time: O(n log n)
    Space: O(1)
    """
    if not intervals:
        return 0

    # Sort by end time
    intervals.sort(key=lambda x: x[1])

    keep = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:  # Non-overlapping
            keep += 1
            last_end = end

    return len(intervals) - keep
```

---

## Minimum Number of Arrows to Burst Balloons

**Problem**: Points on x-axis as intervals. Find minimum arrows (vertical lines) to hit all balloons.

```python
def find_min_arrows(points: list[list[int]]) -> int:
    """
    Minimum arrows to burst all balloons.

    Key insight: Same as activity selection!
    Each "group" of overlapping balloons needs one arrow.

    Time: O(n log n)
    Space: O(1)
    """
    if not points:
        return 0

    # Sort by end point (right edge of balloon)
    points.sort(key=lambda x: x[1])

    arrows = 1
    arrow_pos = points[0][1]  # Shoot at end of first balloon

    for start, end in points[1:]:
        if start > arrow_pos:  # This balloon not hit by current arrow
            arrows += 1
            arrow_pos = end

    return arrows
```

---

## Weighted Interval Scheduling

When activities have values, greedy fails. Use DP instead.

```python
def weighted_interval_scheduling(intervals: list[tuple[int, int, int]]) -> int:
    """
    Max value of non-overlapping intervals.
    intervals: [(start, end, value), ...]

    Greedy fails! Use DP.

    Time: O(n log n)
    Space: O(n)
    """
    if not intervals:
        return 0

    n = len(intervals)
    # Sort by end time
    intervals = sorted(intervals, key=lambda x: x[1])

    # p[i] = last non-overlapping interval before i
    def find_last_non_overlapping(i):
        # Binary search for rightmost j where end[j] <= start[i]
        lo, hi = 0, i - 1
        last_valid = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if intervals[mid][1] <= intervals[i][0]:
                last_valid = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return last_valid

    # dp[i] = max value using intervals 0..i
    dp = [0] * n
    dp[0] = intervals[0][2]

    for i in range(1, n):
        # Option 1: don't include interval i
        exclude = dp[i - 1]

        # Option 2: include interval i
        p = find_last_non_overlapping(i)
        include = intervals[i][2]
        if p != -1:
            include += dp[p]

        dp[i] = max(exclude, include)

    return dp[n - 1]
```

---

## Maximum Meetings in One Room

```python
def max_meetings(start: list[int], end: list[int]) -> list[int]:
    """
    Return 1-indexed meeting numbers that can be held.

    Time: O(n log n)
    Space: O(n)
    """
    if not start:
        return []

    n = len(start)
    # Create meetings with original indices
    meetings = [(start[i], end[i], i + 1) for i in range(n)]

    # Sort by end time
    meetings.sort(key=lambda x: x[1])

    result = [meetings[0][2]]  # Original index of first meeting
    last_end = meetings[0][1]

    for s, e, idx in meetings[1:]:
        if s > last_end:  # Note: > not >= (some problems differ here)
            result.append(idx)
            last_end = e

    return result
```

---

## Complexity Analysis

| Operation                 | Time       | Space | Notes              |
| ------------------------- | ---------- | ----- | ------------------ |
| Activity Selection        | O(n log n) | O(1)  | Sorting dominates  |
| Non-overlapping Intervals | O(n log n) | O(1)  | Same algorithm     |
| Min Arrows                | O(n log n) | O(1)  | Same algorithm     |
| Weighted (DP)             | O(n log n) | O(n)  | DP + binary search |

---

## Edge Cases

- [ ] Empty input → return 0 or []
- [ ] Single activity → return 1 or [activity]
- [ ] All activities overlap → return 1
- [ ] No overlaps → return all activities
- [ ] Same end times → consistent tie-breaking
- [ ] Touching intervals (end = start) → clarify if overlapping

---

## Overlapping vs Touching

**Important clarification to ask in interviews**:

```
Intervals [1, 3] and [3, 5]:
- Overlapping interpretation: They conflict (share point 3)
- Non-overlapping interpretation: They don't conflict

Check condition:
- start >= last_end: non-overlapping (touching OK)
- start > last_end: touching counts as overlap
```

---

## Practice Problems

| #   | Problem                                       | Difficulty | Key Insight                  |
| --- | --------------------------------------------- | ---------- | ---------------------------- |
| 1   | Non-overlapping Intervals                     | Medium     | total - max_keep             |
| 2   | Minimum Number of Arrows to Burst Balloons    | Medium     | Same as activity selection   |
| 3   | Maximum Number of Events That Can Be Attended | Medium     | Heap for earliest deadline   |
| 4   | Maximum Profit in Job Scheduling              | Hard       | Weighted interval scheduling |
| 5   | Video Stitching                               | Medium     | Interval covering variant    |

---

## Interview Tips

1. **Clarify touching intervals**: Ask if [1,3] and [3,5] overlap
2. **Sort by end time**: This is the key insight
3. **Explain the proof**: "Earliest end leaves most room"
4. **Handle weights**: Know that weights need DP
5. **Trace an example**: Show the algorithm step by step

---

## Key Takeaways

1. Activity selection: sort by end time, greedy pick
2. "Earliest end" leaves maximum room for future activities
3. Non-overlapping intervals = total - max_activities
4. Weighted version requires DP with binary search
5. Clarify what "overlap" means (touching vs not)

---

## Next: [03-merge-intervals.md](./03-merge-intervals.md)

Learn to merge overlapping intervals - a different interval problem with different sorting.
