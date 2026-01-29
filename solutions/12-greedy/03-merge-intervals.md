# Solutions: Merge Intervals

## 1. Merge Intervals

**Problem Statement**:
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `intervals = [[1,3],[2,6],[8,10],[15,18]]`
  - Output: `[[1,6],[8,10],[15,18]]`
  - Explanation: Since intervals `[1,3]` and `[2,6]` overlap, merge them into `[1,6]`.
- **Example 2**:
  - Input: `intervals = [[1,4],[4,5]]`
  - Output: `[[1,5]]`
  - Explanation: Intervals `[1,4]` and `[4,5]` are considered overlapping.
- **Edge Cases**:
  - Single interval: Return it.
  - Intervals are already merged: Return same.
  - Large overlaps (one interval containing many others).

**Optimal Python Solution**:

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals using sorting by start time.
    """
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        # If the list of merged intervals is empty or if the current
        # interval does not overlap with the previous, append it.
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # Otherwise, there is an overlap, so we merge the current
            # and previous intervals by updating the end time.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged
```

**Explanation**:

1.  **Sorting**: We sort intervals by their start times. This is crucial because it ensures that if two intervals overlap, they will be adjacent or near each other in the sorted list.
2.  **Linear Scan**: We maintain a list `merged`. For each interval:
    - If it's the first one or if its start time is greater than the end time of the last interval in `merged`, it doesn't overlap. We add it to `merged`.
    - Otherwise, it _must_ overlap (because `current.start <= previous.end` and we know `current.start >= previous.start` from sorting). We merge them by updating the end time of the last interval in `merged` to the maximum of the two end times.

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)`, where `N` is the number of intervals. Sorting takes `O(N log N)`, and the subsequent linear scan takes `O(N)`.
- **Space Complexity**: `O(N)` for the output list. The sorting itself might take `O(log N)` or `O(N)` space.

---

## 2. Insert Interval

**Problem Statement**:
You are given an array of non-overlapping intervals `intervals` sorted in ascending order by start time. You are also given a `newInterval`. Insert `newInterval` into `intervals` such that the result is still sorted and non-overlapping (merge if necessary).

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `intervals = [[1,3],[6,9]], newInterval = [2,5]`
  - Output: `[[1,5],[6,9]]`
- **Example 2**:
  - Input: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]`
  - Output: `[[1,2],[3,10],[12,16]]`
- **Edge Cases**:
  - `newInterval` goes at the very beginning or end.
  - `newInterval` covers all existing intervals.
  - Empty initial intervals.

**Optimal Python Solution**:

```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    """
    Insert and merge a new interval into a sorted list of non-overlapping intervals.
    """
    result = []
    i = 0
    n = len(intervals)

    # 1. Add all intervals ending before newInterval starts
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # 2. Merge all overlapping intervals with newInterval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)

    # 3. Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

**Explanation**:

1.  **Three-Step Process**:
    - **Before**: Iterate through `intervals` and add all that finish before `newInterval` starts.
    - **During (Merge)**: As long as the current interval starts before or at the `newInterval` end time, there's an overlap. We merge them by updating `newInterval`'s start and end.
    - **After**: Add the remaining intervals.
2.  **Efficiency**: This approach takes advantage of the fact that the input is already sorted and non-overlapping, allowing for an `O(N)` solution without re-sorting.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`, where `N` is the number of intervals. We traverse the list exactly once.
- **Space Complexity**: `O(N)` for the resulting list.

---

## 3. Interval List Intersections

**Problem Statement**:
You are given two lists of closed intervals, `firstList` and `secondList`, where each list is pairwise non-overlapping and in sorted order. Return the intersection of these two interval lists.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]`
  - Output: `[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]`
- **Edge Cases**:
  - One list is empty: Intersection is empty.
  - No actual intersections: Return empty.
  - Intersections are single points (e.g., [5,5]).

**Optimal Python Solution**:

```python
def intervalIntersection(firstList: list[list[int]], secondList: list[list[int]]) -> list[list[int]]:
    """
    Find intersection between two sorted, non-overlapping interval lists using two pointers.
    """
    i, j = 0, 0
    result = []

    while i < len(firstList) and j < len(secondList):
        # The intersection start is the max of starts
        start = max(firstList[i][0], secondList[j][0])
        # The intersection end is the min of ends
        end = min(firstList[i][1], secondList[j][1])

        # If start <= end, they overlap!
        if start <= end:
            result.append([start, end])

        # Move the pointer of the interval that ends first
        if firstList[i][1] < secondList[j][1]:
            i += 1
        else:
            j += 1

    return result
```

**Explanation**:

1.  **Intersection Logic**: Two intervals `[a, b]` and `[c, d]` overlap if `max(a, c) <= min(b, d)`. The overlap itself is `[max(a, c), min(b, d)]`.
2.  **Two Pointers**: We use pointers `i` and `j` for the two lists.
3.  **Pointer Movement**: We always advance the pointer of the interval that ends earlier. This is because the earlier-ending interval cannot possibly overlap with any future intervals in the other list.

**Complexity Analysis**:

- **Time Complexity**: `O(N + M)`, where `N` and `M` are the lengths of the two lists.
- **Space Complexity**: `O(1)` additional space (excluding output).

---

## 4. Remove Covered Intervals

**Problem Statement**:
Given a list of `intervals`, remove all intervals that are covered by another interval in the list. An interval `[a, b)` is covered by `[c, d)` if and only if `c <= a` and `b <= d`. Return the number of remaining intervals.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `intervals = [[1,4],[3,6],[2,8]]`
  - Output: `2` ( [3,6] is covered by [2,8] )
- **Example 2**:
  - Input: `intervals = [[1,4],[2,3]]`
  - Output: `1`

**Optimal Python Solution**:

```python
def removeCoveredIntervals(intervals: list[list[int]]) -> int:
    """
    Count intervals that are NOT covered by others.
    Strategy: Sort by start time asc, then by end time desc.
    """
    # Sort: start ASC, end DESC
    # End DESC ensures that if two intervals have the same start,
    # the longest one comes first and covers the shorter ones.
    intervals.sort(key=lambda x: (x[0], -x[1]))

    count = 0
    max_end = 0

    for _, end in intervals:
        # If the current interval's end is beyond the current max_end,
        # it is NOT covered by any previous interval.
        if end > max_end:
            count += 1
            max_end = end

    return count
```

**Explanation**:

1.  **Sorting Trick**: Sorting by start time ascending makes sense. But why end time descending? If we have `[1, 4]` and `[1, 2]`, sorting by `(1, -4), (1, -2)` gives `[1, 4], [1, 2]`. When we process `[1, 2]`, we see its end (2) is less than `max_end` (4), so it's covered.
2.  **Greedy Count**: Since we sorted by start time, any following interval starts at or after the current one. If its end is also within the `max_end` we've seen so far, it is completely covered. If its end is further, it's a new unique range we must keep.

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)` for sorting.
- **Space Complexity**: `O(1)` additional space.

---

## 5. Employee Free Time

**Problem Statement**:
We are given a list `schedule` of employees, which represents the working time for each employee. Each employee has a list of non-overlapping intervals, and these intervals are in sorted order. Return the list of finite intervals representing common, positive-length free time for all employees, also in sorted order.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `schedule = [[[1,2],[5,6]],[[1,3]],[[4,10]]]`
  - Output: `[[3,4]]`
- **Edge Cases**:
  - No gaps: Return empty.
  - Large number of employees.

**Optimal Python Solution**:

```python
def employeeFreeTime(schedule: list[list[list[int]]]) -> list[list[int]]:
    """
    Find common free time across all employees.
    Strategy: Flatten, Sort by start time, Merge, and find Gaps.
    """
    # 1. Flatten all employee schedules into one list
    all_intervals = []
    for emp in schedule:
        for interval in emp:
            all_intervals.append(interval)

    # 2. Sort by start time
    all_intervals.sort(key=lambda x: x[0])

    # 3. Merge overlapping intervals (standard merge)
    merged = []
    if not all_intervals: return []

    curr = all_intervals[0]
    for i in range(1, len(all_intervals)):
        nxt = all_intervals[i]
        if nxt[0] <= curr[1]:
            curr[1] = max(curr[1], nxt[1])
        else:
            merged.append(curr)
            curr = nxt
    merged.append(curr)

    # 4. Gaps between merged intervals are common free time
    free_time = []
    for i in range(1, len(merged)):
        # Gap is [previous.end, current.start]
        free_time.append([merged[i-1][1], merged[i][0]])

    return free_time
```

**Explanation**:

1.  **Flattening**: We treat all work intervals as one big pool.
2.  **Merging**: By merging all work intervals, we get blocks of time where _at least one_ person is working.
3.  **Gaps**: The space between these merged "busy" blocks represents time when _nobody_ is working.

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)`, where `N` is the total number of intervals across all employees (due to sorting).
- **Space Complexity**: `O(N)` for the intermediate merged intervals.
