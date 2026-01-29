# Solutions: Interval Scheduling

## 1. Non-overlapping Intervals

**Problem Statement**:
Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `intervals = [[1,2],[2,3],[3,4],[1,3]]`
  - Output: `1`
  - Explanation: `[1,3]` can be removed and the rest of the intervals are non-overlapping.
- **Example 2**:
  - Input: `intervals = [[1,2],[1,2],[1,2]]`
  - Output: `2`
  - Explanation: You need to remove two `[1,2]` to make the rest of the intervals non-overlapping.
- **Edge Cases**:
  - Empty intervals: 0.
  - Single interval: 0.
  - Intervals that touch at the end (e.g., [1,2] and [2,3]): These are considered non-overlapping in most interval scheduling problems.

**Optimal Python Solution**:

```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    """
    Find minimum removals to make intervals non-overlapping.
    Strategy: Use the Activity Selection algorithm to find the maximum
    number of non-overlapping intervals we can keep.
    Min Removals = Total Intervals - Max Kept Intervals.
    """
    if not intervals:
        return 0

    # Sort by end time: The key to Activity Selection
    intervals.sort(key=lambda x: x[1])

    # We can always keep at least one interval
    count_keep = 1
    last_end = intervals[0][1]

    for i in range(1, len(intervals)):
        start, end = intervals[i]
        # If the current interval starts after or at the previous end
        if start >= last_end:
            # Keep this interval
            count_keep += 1
            # Update the last end time
            last_end = end

    return len(intervals) - count_keep
```

**Explanation**:

1.  **Activity Selection Link**: This problem is a direct application of the "Activity Selection Problem." The goal is to maximize the number of non-overlapping intervals. Any interval not in this maximal set must be removed.
2.  **Greedy Choice**: We always pick the interval that ends the earliest. This leaves the maximum possible time for subsequent intervals to fit.
3.  **Sorting**: Sorting by end time ensures that we are always making the most "conservative" choice for the current step.

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)`, where `N` is the number of intervals. Sorting is the dominant operation.
- **Space Complexity**: `O(1)` (ignoring the space used for sorting) as we only use a few variables for tracking.

---

## 2. Minimum Number of Arrows to Burst Balloons

**Problem Statement**:
There are some spherical balloons taped onto a flat wall. For each balloon, you are given the horizontal range `[x_start, x_end]`. Arrows can be shot up vertically from different points along the x-axis. A balloon is burst by an arrow shot at `x` if `x_start <= x <= x_end`. Find the minimum number of arrows to burst all balloons.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `points = [[10,16],[2,8],[1,6],[7,12]]`
  - Output: `2`
- **Example 2**:
  - Input: `points = [[1,2],[3,4],[5,6],[7,8]]`
  - Output: `4`
- **Edge Cases**:
  - Overlapping endpoints: One arrow can hit both.
  - Balloons nested within each other.

**Optimal Python Solution**:

```python
def findMinArrowShots(points: list[list[int]]) -> int:
    """
    Minimize arrows by shooting at the earliest possible end coordinate.
    """
    if not points:
        return 0

    # Sort by end point
    points.sort(key=lambda x: x[1])

    arrows = 1
    # Current arrow position is the end of the first balloon
    arrow_pos = points[0][1]

    for i in range(1, len(points)):
        # If current balloon starts AFTER our current arrow position
        if points[i][0] > arrow_pos:
            # Need a new arrow
            arrows += 1
            # Update arrow to the end of this balloon
            arrow_pos = points[i][1]

    return arrows
```

**Explanation**:

1.  **Greedy Insight**: To hit a balloon and as many others as possible, the best place to shoot is at its _end_ point.
2.  **Activity Selection Mapping**: This is essentially selecting non-overlapping intervals, but with a slight twist: intervals that "touch" can be burst by the same arrow (so we check `start > arrow_pos` instead of `start >= arrow_pos`).

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)` for sorting the balloons.
- **Space Complexity**: `O(1)` for the arrow count and position tracking.

---

## 3. Maximum Number of Events That Can Be Attended

**Problem Statement**:
You are given an array of `events` where `events[i] = [startDay_i, endDay_i]`. Every day, you can attend at most one event `i` where `startDay_i <= d <= endDay_i`. Return the maximum number of events you can attend.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `events = [[1,2],[2,3],[3,4]]`
  - Output: `3`
- **Example 2**:
  - Input: `events = [[1,2],[2,3],[3,4],[1,2]]`
  - Output: `4`
- **Edge Cases**:
  - Many events starting on the same day.
  - Events with very long durations.

**Optimal Python Solution**:

```python
import heapq

def maxEvents(events: list[list[int]]) -> int:
    """
    Greedy strategy using a Min-Heap:
    On each day, attend the event that ends the earliest among all available events.
    """
    # Sort events by start day
    events.sort()

    total_events = len(events)
    min_heap = []
    event_idx = 0
    attended = 0

    # Determine the total timeframe
    max_day = max(e[1] for e in events)
    min_day = events[0][0]

    for day in range(min_day, max_day + 1):
        # 1. Add all events that start today to the heap
        while event_idx < total_events and events[event_idx][0] == day:
            heapq.heappush(min_heap, events[event_idx][1])
            event_idx += 1

        # 2. Remove events that have already ended
        while min_heap and min_heap[0] < day:
            heapq.heappop(min_heap)

        # 3. Attend the event that ends the earliest (greedy choice)
        if min_heap:
            heapq.heappop(min_heap)
            attended += 1

        # Optimization: If no more events to start and heap is empty, break
        if event_idx == total_events and not min_heap:
            break

    return attended
```

**Explanation**:

1.  **The Greedy Choice**: At any given day, if you have multiple events you _could_ attend, which one should you pick? You should pick the one that **ends the earliest**. This is because it is the most "urgent" and will become unavailable sooner than others.
2.  **Heap Usage**: We use a min-priority queue (heap) to keep track of the end days of all events that have already started but haven't ended yet.
3.  **Iteration**: We iterate day by day. On each day, we update our "available" events and pick the one with the smallest end day.

**Complexity Analysis**:

- **Time Complexity**: `O(D + N log N)`, where `D` is the range of days and `N` is the number of events. Sorting takes `N log N`. Each event is pushed and popped from the heap once (`N log N`).
- **Space Complexity**: `O(N)` for the heap in the worst case.

---

## 4. Maximum Profit in Job Scheduling (Weighted Interval Scheduling)

**Problem Statement**:
We have `n` jobs, where every job is scheduled to be done from `startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`. You're given the `startTime`, `endTime` and `profit` arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time ranges.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]`
  - Output: `120`
- **Example 2**:
  - Input: `startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]`
  - Output: `150`

**Optimal Python Solution**:

```python
import bisect

def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    """
    Weighted Interval Scheduling using DP + Binary Search.
    Greedy doesn't work here because profit varies!
    """
    # Combine and sort jobs by end time
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
    n = len(jobs)

    # dp[i] = max profit considering first i jobs
    # Store as (end_time, max_profit) to facilitate binary search
    dp = [(0, 0)]

    for s, e, p in jobs:
        # Find the latest job that doesn't overlap with current job
        # We look for the largest end_time <= current start_time
        idx = bisect.bisect_right(dp, (s, float('inf'))) - 1

        # Current profit if we include this job
        current_profit = dp[idx][1] + p

        # If including this job is better than the previous max profit
        if current_profit > dp[-1][1]:
            dp.append((e, current_profit))

    return dp[-1][1]
```

**Explanation**:

1.  **Why Greedy Fails**: Simple greedy (earliest end time) works for counts, but when values (profits) are added, a job that ends later might be so profitable that it's worth skipping multiple earlier jobs.
2.  **DP Approach**: We define `dp[i]` as the maximum profit achievable using a subset of the first `i` jobs (sorted by end time).
3.  **Recurrence**: For each job `j`, we have two choices:
    - **Exclude job `j`**: Profit is `dp[j-1]`.
    - **Include job `j`**: Profit is `profit[j]` + `dp[latest_non_overlapping_job]`.
4.  **Binary Search**: To efficiently find the `latest_non_overlapping_job`, we use binary search on the sorted end times.

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)`, where `N` is the number of jobs. Sorting takes `N log N`. For each job, we perform a binary search which takes `log N`.
- **Space Complexity**: `O(N)` to store the DP array.

---

## 5. Video Stitching

**Problem Statement**:
You are given a series of video clips from a sporting event that lasted `T` seconds. These video clips can be overlapping, have different durations, and are represented by `clips[i] = [start_i, end_i]`. Return the minimum number of clips needed so that we can cut the multi-second video into a continuous piece of video covering the entire interval `[0, T]`. If the task is impossible, return -1.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], T = 10`
  - Output: `3`
- **Example 2**:
  - Input: `clips = [[0,1],[1,2]], T = 5`
  - Output: `-1`

**Optimal Python Solution**:

```python
def videoStitching(clips: list[list[int]], T: int) -> int:
    """
    Greedy strategy for Interval Covering:
    At each step, among all clips that start within the current reachable range,
    pick the one that extends the reach the farthest.
    """
    # Sort by start time
    clips.sort()

    res = 0
    cur_end = 0
    farthest_reach = 0
    i = 0

    while cur_end < T:
        # Check all clips that start before or at the current end
        while i < len(clips) and clips[i][0] <= cur_end:
            farthest_reach = max(farthest_reach, clips[i][1])
            i += 1

        # If we didn't extend our reach, it's impossible
        if cur_end == farthest_reach:
            return -1

        # Move our "cur_end" to the farthest we found
        cur_end = farthest_reach
        res += 1

    return res
```

**Explanation**:

1.  **Interval Covering Pattern**: This is a classic "Interval Covering" problem. We want to cover `[0, T]` with the minimum number of segments.
2.  **Greedy Logic**:
    - Start at time 0.
    - Look at all clips that start at or before 0. Of these, which one should we pick? The one that ends the farthest!
    - After picking it, say it ends at `E`. Now look at all clips that start at or before `E`, and pick the one that ends the farthest.
    - Repeat until we reach `T`.
3.  **Why Greedy Works**: Picking the segment that extends the reach the farthest always provides more options for the next segment than any other choice.

**Complexity Analysis**:

- **Time Complexity**: `O(N log N)` for sorting the clips. The while loops traverse the clips list once, making that part `O(N)`.
- **Space Complexity**: `O(1)` extra space.
