# Practice Problems - Merge Intervals

## 1. Merge Intervals

### Problem Statement
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

### Constraints
- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

### Example
**Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`
**Output:** `[[1,6],[8,10],[15,18]]`
**Explanation:** Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

### Python Implementation
```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals: return []
    intervals.sort(key=lambda x: x[0])
    res = [intervals[0]]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= res[-1][1]:
            res[-1][1] = max(res[-1][1], intervals[i][1])
        else:
            res.append(intervals[i])
    return res
```

## 2. Insert Interval

### Problem Statement
You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` represented in ascending order by `start_i`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.

Insert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `start_i` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).

### Constraints
- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^5`
- `intervals` is sorted by `start_i` in ascending order.
- `newInterval.length == 2`
- `0 <= start <= end <= 10^5`

### Example
**Input:** `intervals = [[1,3],[6,9]], newInterval = [2,5]`
**Output:** `[[1,5],[6,9]]`

### Python Implementation
```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    res = []
    i = 0
    n = len(intervals)
    # Add intervals before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        res.append(intervals[i])
        i += 1
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    res.append(newInterval)
    # Add remaining intervals
    while i < n:
        res.append(intervals[i])
        i += 1
    return res
```

## 3. Interval List Intersections

### Problem Statement
You are given two lists of closed intervals, `firstList` and `secondList`, where `firstList[i] = [start_i, end_i]` and `secondList[j] = [start_j, end_j]`. Each list of intervals is pairwise disjoint and in sorted order.

Return the intersection of these two interval lists.

### Constraints
- `0 <= firstList.length, secondList.length <= 1000`
- `firstList[i].length == secondList[j].length == 2`
- `0 <= start_i < end_i <= 10^9`
- `0 <= start_j < end_j <= 10^9`

### Example
**Input:** `firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]`
**Output:** `[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]`

### Python Implementation
```python
def intervalIntersection(firstList: list[list[int]], secondList: list[list[int]]) -> list[list[int]]:
    res = []
    i = j = 0
    while i < len(firstList) and j < len(secondList):
        start = max(firstList[i][0], secondList[j][0])
        end = min(firstList[i][1], secondList[j][1])
        if start <= end:
            res.append([start, end])
        if firstList[i][1] < secondList[j][1]:
            i += 1
        else:
            j += 1
    return res
```

## 4. Remove Covered Intervals

### Problem Statement
Given an array `intervals` where `intervals[i] = [l_i, r_i]`, remove all intervals that are covered by another interval in the list.
An interval `[a, b]` is covered by an interval `[c, d]` if and only if `c <= a` and `b <= d`.
Return the number of remaining intervals.

### Constraints
- `1 <= intervals.length <= 1000`
- `intervals[i].length == 2`
- `0 <= l_i <= r_i <= 10^5`
- All the intervals are unique.

### Example
**Input:** `intervals = [[1,4],[3,6],[2,8]]`
**Output:** `2`
**Explanation:** Interval [3,6] is covered by [2,8], so it is removed.

### Python Implementation
```python
def removeCoveredIntervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: (x[0], -x[1]))
    res = 0
    max_end = 0
    for _, end in intervals:
        if end > max_end:
            res += 1
            max_end = end
    return res
```

## 5. Employee Free Time

### Problem Statement
We are given a list `schedule` of employees, which represents the working time for each employee.
Each employee has a list of non-overlapping `Intervals`, and these intervals are in sorted order.
Return the list of finite intervals representing common, positive-length free time for all employees, also in sorted order.

### Constraints
- `schedule` and `schedule[i]` are lists with lengths in range `[1, 50]`.
- `0 <= start < end <= 10^8`.

### Example
**Input:** `schedule = [[[1,2],[5,6]],[[1,3]],[[4,10]]]`
**Output:** `[[3,4]]`
**Explanation:** There are a total of three employees, and all common free time would be [-inf, 1], [3, 4], [10, inf].
We discard any intervals that contain inf as they aren't finite.

### Python Implementation
```python
def employeeFreeTime(schedule: list[list[list[int]]]) -> list[list[int]]:
    intervals = []
    for s in schedule:
        for i in s:
            intervals.append(i)
    intervals.sort()

    res = []
    merged_end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] > merged_end:
            res.append([merged_end, intervals[i][0]])
        merged_end = max(merged_end, intervals[i][1])
    return res
```
