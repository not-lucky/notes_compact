# Interval Problems - Solutions

## Practice Problems

### 1. Merge Intervals
**Problem Statement**: Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Examples & Edge Cases**:
- Example: `[[1,3],[2,6],[8,10],[15,18]]` -> `[[1,6],[8,10],[15,18]]`
- Edge Case: Single interval.
- Edge Case: Intervals that are exactly adjacent (`[1,2], [2,3]` should merge to `[1,3]`).

**Optimal Python Solution**:
```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals: return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]
    for i in range(1, len(intervals)):
        # If current interval overlaps with the last merged interval
        if intervals[i][0] <= merged[-1][1]:
            # Update the end of the last merged interval
            merged[-1][1] = max(merged[-1][1], intervals[i][1])
        else:
            # No overlap, add current interval to results
            merged.append(intervals[i])

    return merged
```

**Explanation**:
We sort intervals by their start times. This ensures that any intervals that could potentially be merged are adjacent in our list. We then iterate through, either extending the current "running" interval or starting a new one if a gap is found.

**Complexity Analysis**:
- **Time Complexity**: O(n log n) due to sorting.
- **Space Complexity**: O(n) for the output list (or O(log n) for sorting in-place).

---

### 2. Insert Interval
**Problem Statement**: You are given an array of non-overlapping intervals `intervals` sorted by their start times. Insert a `newInterval` into the intervals such that the resulting intervals are still sorted and non-overlapping.

**Optimal Python Solution**:
```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    res = []
    i = 0
    n = len(intervals)

    # 1. Add all intervals that come before the new interval
    while i < n and intervals[i][1] < newInterval[0]:
        res.append(intervals[i])
        i += 1

    # 2. Merge overlapping intervals with the new interval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    res.append(newInterval)

    # 3. Add all intervals that come after the new interval
    while i < n:
        res.append(intervals[i])
        i += 1

    return res
```

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(n) for the result.

---

### 3. Meeting Rooms
**Problem Statement**: Given an array of meeting time intervals, determine if a person could attend all meetings.

**Optimal Python Solution**:
```python
def canAttendMeetings(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True
```

**Explanation**:
A person can attend all meetings if no two meetings overlap. After sorting by start time, we just check if any meeting starts before the previous one ends.

**Complexity Analysis**:
- **Time Complexity**: O(n log n).
- **Space Complexity**: O(1).

---

### 4. Meeting Rooms II
**Problem Statement**: Given an array of meeting time intervals, return the minimum number of conference rooms required.

**Optimal Python Solution**:
```python
def minMeetingRooms(intervals: list[list[int]]) -> int:
    if not intervals: return 0

    # Separate start and end times
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])

    res = 0
    count = 0
    s_ptr, e_ptr = 0, 0

    while s_ptr < len(intervals):
        if starts[s_ptr] < ends[e_ptr]:
            # A meeting starts before the earliest ending meeting finishes
            count += 1
            s_ptr += 1
        else:
            # A meeting ends, freeing up a room
            count -= 1
            e_ptr += 1
        res = max(res, count)

    return res
```

**Explanation**:
We treat starts and ends as independent events. We iterate through time; every start increases the room count, and every end decreases it. The maximum room count reached at any point is our answer.

**Complexity Analysis**:
- **Time Complexity**: O(n log n).
- **Space Complexity**: O(n).

---

### 5. Non-overlapping Intervals
**Problem Statement**: Given an array of intervals, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

**Optimal Python Solution**:
```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    if not intervals: return 0

    # Greedy approach: sort by end time
    # The interval that ends earliest leaves the most room for others
    intervals.sort(key=lambda x: x[1])

    count = 0
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            # Overlap found, remove this interval (greedy)
            count += 1
        else:
            # No overlap, update end time
            prev_end = intervals[i][1]

    return count
```

**Complexity Analysis**:
- **Time Complexity**: O(n log n).
- **Space Complexity**: O(1).

---

### 6. Interval List Intersections
**Problem Statement**: You are given two lists of closed intervals, `firstList` and `secondList`, where `firstList[i] = [starti, endi]` and `secondList[j] = [startj, endj]`. Each list of intervals is pairwise disjoint and in sorted order. Return the intersection of these two interval lists.

**Optimal Python Solution**:
```python
def intervalIntersection(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    res = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        # Find the overlap range
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])

        if start <= end:
            res.append([start, end])

        # Move the pointer of the interval that ends first
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return res
```

**Complexity Analysis**:
- **Time Complexity**: O(n + m).
- **Space Complexity**: O(n + m) for the result.

---

### 7. Remove Covered Intervals
**Problem Statement**: Given a list of intervals, remove all intervals that are covered by another interval in the list. Interval `[a,b]` is covered by interval `[c,d]` if and only if `c <= a` and `b <= d`. Return the number of remaining intervals.

**Optimal Python Solution**:
```python
def removeCoveredIntervals(intervals: list[list[int]]) -> int:
    # Sort by start (asc) and then by end (desc)
    # This ensures that for the same start, the larger interval comes first
    intervals.sort(key=lambda x: (x[0], -x[1]))

    res = 0
    prev_end = 0

    for _, end in intervals:
        if end > prev_end:
            # This interval is NOT covered by the previous ones
            res += 1
            prev_end = end

    return res
```

**Complexity Analysis**:
- **Time Complexity**: O(n log n).
- **Space Complexity**: O(1).

---

### 8. Employee Free Time
**Problem Statement**: Given a list of employee schedules, return the common free time for all employees.

**Optimal Python Solution**:
```python
def employeeFreeTime(schedule: list[list[list[int]]]) -> list[list[int]]:
    # 1. Flatten all working intervals
    ints = []
    for emp in schedule:
        for i in emp:
            ints.append(i)

    # 2. Sort by start time
    ints.sort(key=lambda x: x[0])

    # 3. Merge working intervals and find gaps
    res = []
    prev_end = ints[0][1]
    for i in range(1, len(ints)):
        curr_start, curr_end = ints[i]
        if curr_start > prev_end:
            # We found a gap between merged working intervals
            res.append([prev_end, curr_start])
        prev_end = max(prev_end, curr_end)

    return res
```

**Complexity Analysis**:
- **Time Complexity**: O(N log N) where N is the total number of intervals.
- **Space Complexity**: O(N).
