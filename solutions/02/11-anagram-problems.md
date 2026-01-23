# Interval Problems

## Practice Problems

### 1. Merge Intervals
**Difficulty:** Medium
**Key Technique:** Sort + merge

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Time: O(n log n)
    Space: O(n)
    """
    if not intervals: return []
    intervals.sort()
    res = [intervals[0]]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= res[-1][1]:
            res[-1][1] = max(res[-1][1], intervals[i][1])
        else:
            res.append(intervals[i])
    return res
```

### 2. Insert Interval
**Difficulty:** Medium
**Key Technique:** Three passes

```python
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """
    Time: O(n)
    Space: O(n)
    """
    res = []
    i = 0
    n = len(intervals)
    while i < n and intervals[i][1] < new_interval[0]:
        res.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval = [min(new_interval[0], intervals[i][0]),
                        max(new_interval[1], intervals[i][1])]
        i += 1
    res.append(new_interval)
    res.extend(intervals[i:])
    return res
```

### 3. Meeting Rooms
**Difficulty:** Easy
**Key Technique:** Check overlaps

```python
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    """
    Time: O(n log n)
    Space: O(1)
    """
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True
```

### 4. Meeting Rooms II
**Difficulty:** Medium
**Key Technique:** Events or heap

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Time: O(n log n)
    Space: O(n)
    """
    if not intervals: return 0
    intervals.sort()
    heap = [intervals[0][1]]
    for i in range(1, len(intervals)):
        if intervals[i][0] >= heap[0]:
            heapq.heappop(heap)
        heapq.heappush(heap, intervals[i][1])
    return len(heap)
```

### 5. Non-overlapping Intervals
**Difficulty:** Medium
**Key Technique:** Greedy by end time

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Time: O(n log n)
    Space: O(1)
    """
    if not intervals: return 0
    intervals.sort(key=lambda x: x[1])
    cnt = 0
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            cnt += 1
        else:
            end = intervals[i][1]
    return cnt
```

### 6. Interval List Intersections
**Difficulty:** Medium
**Key Technique:** Two pointers

```python
def interval_intersection(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """
    Time: O(m + n)
    Space: O(m + n)
    """
    res = []
    i = j = 0
    while i < len(A) and j < len(B):
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])
        if start <= end:
            res.append([start, end])
        if A[i][1] < B[j][1]: i += 1
        else: j += 1
    return res
```

### 7. Remove Covered Intervals
**Difficulty:** Medium
**Key Technique:** Sort by start, -end

```python
def remove_covered_intervals(intervals: list[list[int]]) -> int:
    """
    Time: O(n log n)
    Space: O(1)
    """
    intervals.sort(key=lambda x: (x[0], -x[1]))
    cnt = 0
    max_end = 0
    for _, end in intervals:
        if end > max_end:
            cnt += 1
            max_end = end
    return cnt
```

### 8. Employee Free Time
**Difficulty:** Hard
**Key Technique:** Merge all

```python
# Definition for an Interval.
# class Interval:
#     def __init__(self, start: int = None, end: int = None):
#         self.start = start
#         self.end = end

def employeeFreeTime(schedule: list[list['Interval']]) -> list['Interval']:
    """
    Time: O(N log N) where N total intervals
    Space: O(N)
    """
    ints = []
    for s in schedule:
        for i in s:
            ints.append((i.start, i.end))
    ints.sort()

    res = []
    end = ints[0][1]
    for i in range(1, len(ints)):
        if ints[i][0] > end:
            res.append(Interval(end, ints[i][0]))
        end = max(end, ints[i][1])
    return res
```
