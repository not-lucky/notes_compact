# Practice Problems - Interval Scheduling

## 1. Non-overlapping Intervals

### Problem Statement
Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

### Constraints
- `1 <= intervals.length <= 10^5`
- `intervals[i].length == 2`
- `-5 * 10^4 <= start_i < end_i <= 5 * 10^4`

### Example
**Input:** `intervals = [[1,2],[2,3],[3,4],[1,3]]`
**Output:** `1`
**Explanation:** `[1,3]` can be removed and the rest of the intervals are non-overlapping.

### Python Implementation
```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    if not intervals: return 0
    intervals.sort(key=lambda x: x[1])
    count = 1
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            count += 1
            end = intervals[i][1]
    return len(intervals) - count
```

## 2. Maximum Number of Events That Can Be Attended

### Problem Statement
You are given an array of `events` where `events[i] = [startDay_i, endDay_i]`. Every event `i` starts at `startDay_i` and ends at `endDay_i`.
You can attend an event `i` at any day `d` where `startDay_i <= d <= endDay_i`. You can only attend one event at any time `d`.
Return the maximum number of events you can attend.

### Constraints
- `1 <= events.length <= 10^5`
- `events[i].length == 2`
- `1 <= startDay_i <= endDay_i <= 10^5`

### Example
**Input:** `events = [[1,2],[2,3],[3,4]]`
**Output:** `3`
**Explanation:** You can attend all three events. One way is to attend the first event on day 1, the second on day 2, and the third on day 3.

### Python Implementation
```python
import heapq

def maxEvents(events: list[list[int]]) -> int:
    events.sort()
    n = len(events)
    min_heap = []
    res = 0
    i = 0
    day = events[0][0]

    while i < n or min_heap:
        # Add events starting on current day
        while i < n and events[i][0] == day:
            heapq.heappush(min_heap, events[i][1])
            i += 1

        # Remove events that already ended
        while min_heap and min_heap[0] < day:
            heapq.heappop(min_heap)

        # Attend the event ending earliest
        if min_heap:
            heapq.heappop(min_heap)
            res += 1
            day += 1
        elif i < n:
            day = events[i][0]

    return res
```

## 3. Maximum Profit in Job Scheduling

### Problem Statement
We have `n` jobs, where every job is scheduled to be done from `startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.
You're given the `startTime`, `endTime` and `profit` arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.
If you choose a job that ends at time `X` you will be able to start another job that starts at time `X`.

### Constraints
- `1 <= startTime.length == endTime.length == profit.length <= 5 * 10^4`
- `1 <= startTime[i] < endTime[i] <= 10^9`
- `1 <= profit[i] <= 10^4`

### Example
**Input:** `startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]`
**Output:** `120`
**Explanation:** The subset chosen is the first and fourth job. Profit = 50 + 70 = 120.

### Python Implementation
```python
import bisect

def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
    n = len(jobs)
    dp = [(0, 0)] # (end_time, max_profit)

    for s, e, p in jobs:
        # Find latest job that doesn't overlap with current job
        idx = bisect.bisect_right(dp, (s, float('inf'))) - 1
        current_profit = dp[idx][1] + p
        if current_profit > dp[-1][1]:
            dp.append((e, current_profit))

    return dp[-1][1]
```

## 4. Video Stitching

### Problem Statement
You are given a series of video clips from a sporting event that lasted `time` seconds. These video clips can be overlapping with each other and have varying lengths.
Each video clip `clips[i]` is an interval: it starts at `clips[i][0]` and ends at `clips[i][1]`.
We can cut these clips into smaller clips. For example, a clip `[0, 7]` can be cut into clips `[0, 5]`, `[1, 6]`, and `[3, 7]`.
Return the minimum number of clips needed so that we can cut the clips into a set of clips that covers the entire sporting event `[0, time]`. If the task is impossible, return -1.

### Constraints
- `1 <= clips.length <= 100`
- `0 <= clips[i][0] <= clips[i][1] <= 100`
- `1 <= time <= 100`

### Example
**Input:** `clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10`
**Output:** `3`
**Explanation:** We take clips [0,2], [8,10], [1,9]; a total of 3 clips.

### Python Implementation
```python
def videoStitching(clips: list[list[int]], time: int) -> int:
    # Sort clips by start time
    clips.sort()
    res = 0
    cur_end = 0
    next_end = 0
    i = 0

    while cur_end < time:
        while i < len(clips) and clips[i][0] <= cur_end:
            next_end = max(next_end, clips[i][1])
            i += 1

        if next_end == cur_end:
            return -1

        cur_end = next_end
        res += 1

    return res
```
