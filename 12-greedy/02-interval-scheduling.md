# Interval Scheduling

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Interval scheduling tests your ability to:

1. **Greedy intuition**: Why sort by end time, not start time or duration
2. **Proof understanding**: Why earliest-end-time selection is optimal
3. **Pattern recognition**: Mapping problems to interval selection
4. **Edge case handling**: Overlapping vs touching intervals (`>` vs `>=`)

---

## Building Intuition

**The "Room for More" Principle**

Imagine you're scheduling meetings in a single conference room. You want to fit as many meetings as possible. The key insight:

_The earlier a meeting ends, the more time remains for future meetings._

This is why we sort by END time, not start time. Starting early doesn't help if the meeting runs long -- what matters is when the room is FREE again.

**Mental Model: The Greedy Host**

Think of yourself as a host accepting or rejecting meeting requests in order. Your strategy: always pick the request that ends earliest and doesn't conflict with what you already accepted.

```
Guest requests:  [9-10:30], [9:30-10], [10-11], [10:30-12]

Sort by end time: [9:30-10], [9-10:30], [10-11], [10:30-12]

Decision process:
1. [9:30-10]: Accept! (ends earliest, leaves most room)
2. [9-10:30]: Reject (conflicts with [9:30-10])
3. [10-11]: Accept! (starts at 10 = last_end, compatible)
4. [10:30-12]: Reject (conflicts with [10-11])

Result: 2 meetings [9:30-10] and [10-11]
```

### Sort by End Time vs Start Time vs Duration

**Why NOT sort by start time?**

A long-running activity that starts early "hogs" the room, blocking many short activities:

```
Activities: [(0, 100), (1, 2), (3, 4)]

Sort by start:     [(0, 100), (1, 2), (3, 4)]
Greedy picks:      (0, 100) → 1 activity total     ← WRONG

Sort by end:       [(1, 2), (3, 4), (0, 100)]
Greedy picks:      (1, 2), then (3, 4) → 2 activities  ← CORRECT
```

**Why NOT sort by duration?**

A short activity positioned in the middle blocks two compatible longer activities:

```
Activities: [(0, 5), (4, 6), (5, 10)]
Durations:    5       2       5

Sort by duration: [(4, 6), (0, 5), (5, 10)]
Greedy picks:     (4, 6) → overlaps both others → 1 activity  ← WRONG

Optimal:          (0, 5), (5, 10) → 2 activities               ← CORRECT
```

**Summary**: Sort by end time is the only correct greedy strategy. It directly optimizes for "leave the most room for future activities."

---

## Problem Statement

Given a set of activities with start and end times, select the **maximum number of non-overlapping activities**.

```
Input: activities = [(1,4), (3,5), (0,6), (5,7), (3,8), (5,9), (6,10), (8,11), (8,12), (2,13), (12,14)]
Output: 4 (e.g., activities [(1,4), (5,7), (8,11), (12,14)])
```

This is the classic **Activity Selection Problem**.

---

## Activity Selection Algorithm

```python
def max_activities(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Select maximum number of non-overlapping activities using greedy strategy.

    Strategy: Sort by end time, then greedily pick the earliest-ending
    compatible activity.

    Why it works: Finishing early leaves maximum room for future activities.

    Time:  O(n log n) for sorting
    Space: O(n) for sorted copy + output list
    """
    if not activities:
        return []

    # Sort by end time: earliest finish first
    activities = sorted(activities, key=lambda x: x[1])

    # Always pick the first activity (earliest ending)
    result = [activities[0]]
    last_end = activities[0][1]

    # Greedily pick next compatible activity
    for start, end in activities[1:]:
        if start >= last_end:  # Compatible: starts at or after last ended
            result.append((start, end))
            last_end = end

    return result


def count_max_activities(activities: list[tuple[int, int]]) -> int:
    """
    Return maximum count of non-overlapping activities.

    Same algorithm, but only tracks count (no output list needed).

    Time:  O(n log n)
    Space: O(n) for sorted copy
    """
    if not activities:
        return 0

    # Sort by end time
    activities = sorted(activities, key=lambda x: x[1])

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

After sorting by end time:

Timeline:  0  1  2  3  4  5  6  7  8  9  10  11
(1,4):        |-----------|
(3,5):              |--------|
(0,6):     |-------------------|
(5,7):                 |--------|
(3,8):              |--------------|
(5,9):                 |-----------|
(6,10):                   |-----------|
(8,11):                         |---------|

Greedy selection (>= means touching is OK):

Step  Interval  Check             Decision    last_end
 1    (1,4)     (first)           ACCEPT      4
 2    (3,5)     3 >= 4? NO        SKIP        4
 3    (0,6)     0 >= 4? NO        SKIP        4
 4    (5,7)     5 >= 4? YES       ACCEPT      7
 5    (3,8)     3 >= 7? NO        SKIP        7
 6    (5,9)     5 >= 7? NO        SKIP        7
 7    (6,10)    6 >= 7? NO        SKIP        7
 8    (8,11)    8 >= 7? YES       ACCEPT      11

Result: [(1,4), (5,7), (8,11)] → 3 activities
```

---

## Proof of Correctness (Greedy Stays Ahead)

**Claim**: The greedy algorithm selects as many activities as any optimal solution.

**Setup**:

1. Let $G = \{g_1, g_2, \dots, g_k\}$ be greedy's selection (sorted by end time)
2. Let $O = \{o_1, o_2, \dots, o_m\}$ be any optimal solution (sorted by end time)
3. We want to show $k \ge m$

**Lemma (Greedy Stays Ahead)**: For all $i \le \min(k, m)$: $\text{end}(g_i) \le \text{end}(o_i)$

_At every step, greedy's i-th activity ends no later than OPT's i-th activity._

**Proof by induction**:

- **Base case ($i = 1$)**: Greedy picks the activity with the globally earliest end time. Since $o_1$ is one possible choice, $\text{end}(g_1) \le \text{end}(o_1)$.

- **Inductive step**: Assume $\text{end}(g_i) \le \text{end}(o_i)$ for some $i$.
  - Since $O$ is a valid (non-overlapping) selection: $\text{start}(o_{i+1}) \ge \text{end}(o_i)$
  - By inductive hypothesis: $\text{end}(o_i) \ge \text{end}(g_i)$
  - Chaining: $\text{start}(o_{i+1}) \ge \text{end}(o_i) \ge \text{end}(g_i)$
  - So $o_{i+1}$ is compatible with $g_i$ (it starts after $g_i$ ends)
  - Greedy picks the earliest-ending activity compatible with $g_i$
  - Since $o_{i+1}$ is one such compatible activity: $\text{end}(g_{i+1}) \le \text{end}(o_{i+1})$

**Conclusion**: Suppose for contradiction that $k < m$ (greedy selects fewer). By the lemma, $\text{end}(g_k) \le \text{end}(o_k)$. Since $o_{k+1}$ exists in $O$ and $\text{start}(o_{k+1}) \ge \text{end}(o_k) \ge \text{end}(g_k)$, the activity $o_{k+1}$ is compatible with $g_k$. But greedy would have selected it (or something ending even earlier) -- contradiction with greedy stopping at $k$. Therefore $k \ge m$.

**Why this proof structure matters in interviews**: You don't need to recite this verbatim. The key point is: "greedy never falls behind optimal because at every step it ends at least as early, so it always has at least as much room for future picks."

---

## Overlapping vs Touching: The Critical Detail

**Always clarify this in interviews** -- the comparison operator determines correctness:

```
Intervals [1, 3] and [3, 5]:

If touching is OK (compatible):   start >= last_end  →  3 >= 3  →  compatible
If touching conflicts (overlap):  start >  last_end  →  3 >  3  →  conflict
```

**Physical interpretation:**
- `>=` (touching OK): Like meetings where one ends at 3:00 and another starts at 3:00 -- back-to-back is fine
- `>` (touching conflicts): Like meetings that need cleanup/setup time -- can't start exactly when the previous ends

**Problem-specific conventions:**

| Problem | Convention | Operator | Reasoning |
|---------|------------|----------|-----------|
| LeetCode 435 (Non-overlapping Intervals) | Touching OK | `>=` | [1,2] and [2,3] don't overlap |
| LeetCode 452 (Min Arrows) | Touching bursts | `>` | Arrow at x=2 bursts both [1,2] and [2,3] |
| Activity Selection (CLRS) | Touching OK | `>=` | Mathematical convention |

The difference is a single character (`>` vs `>=`), but using the wrong one changes the answer.

---

## When Greedy Activity Selection Fails

**1. When Activities Have Weights/Values**

If each activity has a different profit, maximizing count no longer maximizes value:

```
[(0, 10, value=100), (0, 3, value=7), (4, 6, value=8)]

Greedy (by end time): picks (0,3) + (4,6) = value 15
Optimal:              picks (0,10) alone  = value 100
```

Use **Weighted Interval Scheduling (DP)** instead -- see below.

**2. When You Need Exactly K Activities**

"Select exactly K non-overlapping activities with maximum total value" requires DP.

**3. Multiple Resources/Rooms**

If you have unlimited rooms and want to find the minimum number needed, the problem becomes Meeting Rooms II (sort by start time, use a min-heap). See [04-meeting-rooms.md](./04-meeting-rooms.md).

---

## Practice Problem 1: Non-overlapping Intervals (LeetCode 435)

**Problem**: Given intervals, find the minimum number to remove so the rest are non-overlapping.

**Key insight**: This is the activity selection problem in disguise.
- `max_keep` = max non-overlapping count (activity selection)
- `min_remove` = `total - max_keep`

**Why this works**: Instead of thinking "which intervals to remove," think "which intervals to keep." The maximum set of non-overlapping intervals is exactly what activity selection finds. Everything else gets removed.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Minimum intervals to remove to make remaining intervals non-overlapping.

    Reduction: min_remove = total - max_non_overlapping (activity selection).

    Touching convention: [1,3] and [3,5] do NOT overlap (touching is OK).

    Time:  O(n log n) for sorting
    Space: O(n) for sorted copy
    """
    if not intervals:
        return 0

    # Sort by end time: earliest finish first
    intervals = sorted(intervals, key=lambda x: x[1])

    # Count maximum non-overlapping intervals we can keep
    keep = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:  # Touching OK: [1,3] and [3,5] are compatible
            keep += 1
            last_end = end

    return len(intervals) - keep
```

**Trace**:

```
Input: [[1,2], [2,3], [3,4], [1,3]]

Sort by end: [[1,2], [2,3], [1,3], [3,4]]

Step  Interval  Check          Decision   last_end   keep
 1    [1,2]     (first)        KEEP       2          1
 2    [2,3]     2 >= 2? YES    KEEP       3          2
 3    [1,3]     1 >= 3? NO     REMOVE     3          2
 4    [3,4]     3 >= 3? YES    KEEP       4          3

keep = 3, total = 4
Answer: 4 - 3 = 1 removal
```

---

## Practice Problem 2: Minimum Arrows to Burst Balloons (LeetCode 452)

**Problem**: Balloons are intervals `[start, end]` on the x-axis. An arrow shot vertically at position x bursts all balloons where `start <= x <= end`. Find the minimum number of arrows to burst all balloons.

**Key insight**: Sort by end time, shoot at each balloon's right edge. This bursts the maximum number of overlapping balloons. Each time a balloon starts beyond the current arrow's position, we need a new arrow.

**Overlap convention**: Touching balloons (`start == prev_end`) share a point, so one arrow bursts both. Use strict `>` for "needs new arrow."

```python
def find_min_arrows(points: list[list[int]]) -> int:
    """
    Minimum arrows needed to burst all balloons.

    Strategy: Sort by end, shoot at each balloon's right edge.
    One arrow bursts all balloons that include that x-position.

    Touching: [1,3] and [3,5] share point 3, so one arrow bursts both.
    Use strict > for "needs new arrow."

    Time:  O(n log n) for sorting
    Space: O(n) for sorted copy
    """
    if not points:
        return 0

    # Sort by end point (right edge of balloon)
    points = sorted(points, key=lambda x: x[1])

    arrows = 1
    arrow_pos = points[0][1]  # Shoot at first balloon's right edge

    for start, end in points[1:]:
        if start > arrow_pos:  # Starts AFTER arrow -- needs new arrow
            arrows += 1
            arrow_pos = end

    return arrows
```

**Trace**:

```
Input: [[10,16], [2,8], [1,6], [7,12]]

Sort by end: [[1,6], [2,8], [7,12], [10,16]]

Step  Balloon   Arrow at  Check          Decision       arrow_pos
 1    [1,6]     6         (first)        SHOOT at 6     6
 2    [2,8]     6         2 > 6? NO      already burst  6
 3    [7,12]    6         7 > 6? YES     NEW ARROW→12   12
 4    [10,16]   12        10 > 12? NO    already burst  12

Answer: 2 arrows (at x=6 and x=12)
```

**Connection to Activity Selection**: The number of arrows equals the number of non-overlapping groups. This is exactly `count_max_activities` but with the touching convention flipped (`>` instead of `>=` because touching balloons share a point).

---

## Practice Problem 3: Maximum Length of Pair Chain (LeetCode 646)

**Problem**: Given pairs `[a, b]` where `a < b`, find the longest chain you can form. A pair `[c, d]` can follow pair `[a, b]` in the chain only if `b < c` (strictly).

**Key insight**: This is activity selection with strict inequality. A pair `[a, b]` is an interval -- we want the maximum number of non-overlapping pairs where the next pair starts strictly after the previous one ends.

```python
def find_longest_chain(pairs: list[list[int]]) -> int:
    """
    Longest chain of pairs where each pair starts strictly after the
    previous pair ends.

    This is activity selection with strict inequality (b < c, not b <= c).

    Time:  O(n log n) for sorting
    Space: O(n) for sorted copy
    """
    if not pairs:
        return 0

    # Sort by end time
    pairs = sorted(pairs, key=lambda x: x[1])

    count = 1
    last_end = pairs[0][1]

    for start, end in pairs[1:]:
        if start > last_end:  # Strict: next pair must start AFTER current ends
            count += 1
            last_end = end

    return count
```

**Trace**:

```
Input: [[1,2], [2,3], [3,4]]

Sort by end: [[1,2], [2,3], [3,4]]

Step  Pair    Check          Decision   last_end   count
 1    [1,2]   (first)        PICK       2          1
 2    [2,3]   2 > 2? NO      SKIP       2          1
 3    [3,4]   3 > 2? YES     PICK       4          2

Answer: 2 (chain: [1,2] → [3,4])
```

**Note**: This uses `>` (strict), not `>=`, because the problem requires `b < c` (the next pair must start strictly after the current pair ends). Compare to LC 435 which uses `>=`.

---

## Contrast: Weighted Interval Scheduling (LeetCode 1235)

When activities have values/weights (e.g., profit), greedy fails (maximizing count != maximizing value). This becomes **Maximum Profit in Job Scheduling** (LeetCode 1235), requiring Dynamic Programming.

**Recurrence**: For each interval `i` (sorted by end time):
- **Exclude**: best value from intervals `0..i-1` (skip interval `i`)
- **Include**: `profit[i]` + best value from intervals that end before `i` starts
- `dp[i] = max(exclude, include)`

Finding "latest interval that ends before `i` starts" uses binary search for $O(\log n)$.

```python
from bisect import bisect_right

def job_scheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    """
    LeetCode 1235: Maximum Profit in Job Scheduling.

    Why DP instead of greedy:
    - Greedy maximizes COUNT, not VALUE
    - A single high-value interval may beat multiple low-value ones

    Time:  O(n log n) -- sorting + binary search per interval
    Space: O(n) -- DP array + sorted copy
    """
    if not startTime:
        return 0

    n = len(startTime)
    # Zip into tuples and sort by end time
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])

    # Precompute end times for binary search
    ends = [job[1] for job in jobs]

    def find_last_compatible(i: int) -> int:
        """
        Find rightmost job j < i where end[j] <= start[i].
        Uses bisect_right on end times for O(log n) lookup.
        Returns -1 if no compatible job exists.
        """
        target = jobs[i][0]  # start time of job i
        # bisect_right finds insertion point for target in ends[0:i]
        # Subtract 1 to get the last index with end <= target
        return bisect_right(ends, target, 0, i) - 1

    dp = [0] * n
    dp[0] = jobs[0][2]  # Base case: profit of first job

    for i in range(1, n):
        exclude = dp[i - 1]

        p = find_last_compatible(i)
        include = jobs[i][2] + (dp[p] if p >= 0 else 0)

        dp[i] = max(exclude, include)

    return dp[n - 1]
```

**Trace**:

```
Input: startTime = [0, 0, 4], endTime = [3, 10, 6], profit = [7, 100, 8]

Zip & Sort by end: [(0, 3, 7), (4, 6, 8), (0, 10, 100)]
ends:              [3, 6, 10]

i=0: dp[0] = 7 (base case)

i=1: job (4,6,8)
     find_last_compatible(1): start=4, bisect_right([3,6], 4, 0, 1)=1, j=0
     exclude = dp[0] = 7
     include = 8 + dp[0] = 8 + 7 = 15
     dp[1] = max(7, 15) = 15

i=2: job (0,10,100)
     find_last_compatible(2): start=0, bisect_right([3,6,10], 0, 0, 2)=0, j=-1
     exclude = dp[1] = 15
     include = 100 + 0 = 100
     dp[2] = max(15, 100) = 100

Answer: 100 (just the high-value interval (0,10))

Compare to greedy by end time: would pick (0,3) + (4,6) = 15. Wrong!
```

### Reconstructing the Selected Jobs

To find WHICH jobs were selected (not just the max value), backtrack through the DP array:

```python
def job_scheduling_with_selection(
    startTime: list[int], endTime: list[int], profit: list[int]
) -> tuple[int, list[tuple[int, int, int]]]:
    """
    Returns (max_profit, selected_jobs) for weighted interval scheduling.
    """
    if not startTime:
        return 0, []

    n = len(startTime)
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
    ends = [job[1] for job in jobs]

    def find_last_compatible(i: int) -> int:
        target = jobs[i][0]
        return bisect_right(ends, target, 0, i) - 1

    dp = [0] * n
    dp[0] = jobs[0][2]

    for i in range(1, n):
        exclude = dp[i - 1]
        p = find_last_compatible(i)
        include = jobs[i][2] + (dp[p] if p >= 0 else 0)
        dp[i] = max(exclude, include)

    # Backtrack to find selected jobs
    selected = []
    i = n - 1
    while i >= 0:
        # If profit is the same without job i, we can skip it
        if i > 0 and dp[i] == dp[i - 1]:
            i -= 1
        else:
            # Otherwise, we must have included job i
            selected.append(jobs[i])
            i = find_last_compatible(i)

    # Return max profit and chronological jobs
    return dp[n - 1], selected[::-1]


# Example:
# startTime = [0, 0, 4], endTime = [3, 10, 6], profit = [7, 100, 8]
# Result: (100, [(0, 10, 100)])
```

**Why this works**: The backtrack compares `dp[i]` to `dp[i-1]`. If they are equal, it means job `i` wasn't strictly necessary for the maximum profit, so we can skip it. Otherwise, we must have included job `i`, so we add it to our selection and jump to the last compatible job before it.

---

## Complexity Summary

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Activity Selection | $O(n \log n)$ | $O(n)$ | Sorting dominates; $O(1)$ extra if sorted in place |
| Non-overlapping Intervals (LC 435) | $O(n \log n)$ | $O(1)$ | In-place sort, count only |
| Min Arrows (LC 452) | $O(n \log n)$ | $O(1)$ | In-place sort, count only |
| Pair Chain (LC 646) | $O(n \log n)$ | $O(1)$ | In-place sort, count only |
| Weighted (DP) | $O(n \log n)$ | $O(n)$ | DP array + binary search + sorted copy |

---

## Edge Cases

- [ ] Empty input -- return 0 or []
- [ ] Single activity -- always selected
- [ ] All activities overlap -- return 1 (any single activity)
- [ ] No overlaps -- return all activities
- [ ] Identical end times -- any tie-breaking order works (proof still holds)
- [ ] Touching intervals (`end == start`) -- clarify if overlapping or not (problem-dependent)
- [ ] Negative time values -- algorithm still works correctly
- [ ] Invalid intervals (`start > end`) -- validate based on problem constraints

---

## Interview Tips

1. **Clarify the overlap convention first**: Ask whether `[1,3]` and `[3,5]` are compatible. This determines `>=` vs `>`.

2. **State the key insight immediately**: "Sort by end time because finishing early leaves the maximum room for future activities."

3. **Know the proof sketch**: "Greedy stays ahead" -- at every step, greedy's i-th pick ends no later than optimal's i-th pick. So greedy always has at least as much room for future activities and can never select fewer.

4. **Recognize the DP trigger**: If activities have weights/values (maximize profit, not count), greedy fails. Use weighted interval scheduling with DP + binary search.

5. **Trace a small example**: Walk through 4-5 intervals step by step. Show the sort-by-start counterexample.

6. **Watch for reductions**:
   - "Minimum removals" = `total - max_keep` (LC 435)
   - "Minimum arrows" = count non-overlapping groups (LC 452)
   - "Longest chain" = activity selection with strict inequality (LC 646)

---

## Key Takeaways

1. **Core algorithm**: Sort by end time, greedily pick the earliest-ending compatible activity

2. **Why it works**: Finishing early maximizes remaining time for future activities. The "greedy stays ahead" proof shows greedy's i-th pick always ends no later than optimal's i-th pick.

3. **Counterexamples matter**:
   - Sort by start time fails: long activity hogs the room
   - Sort by duration fails: short activity in the middle blocks two compatible longer ones

4. **Three problem reductions**: LC 435 (min removals = total - max keep), LC 452 (arrows = non-overlapping groups with touching allowed), LC 646 (longest chain = activity selection with strict `>`)

5. **Weighted version**: When activities have values, use DP with binary search ($O(n \log n)$ time, $O(n)$ space)

6. **Critical detail**: `>` vs `>=` depends on the problem's overlap convention -- always clarify

---

## Next: [03-merge-intervals.md](./03-merge-intervals.md)

Learn to merge overlapping intervals -- a different interval problem where we sort by start time instead of end time.
