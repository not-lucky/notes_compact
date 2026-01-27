# Solutions: Meeting Rooms

## 1. Meeting Rooms
**Problem Statement**:
Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `intervals = [[0,30],[5,10],[15,20]]`
    - Output: `false`
- **Example 2**:
    - Input: `intervals = [[7,10],[2,4]]`
    - Output: `true`
- **Edge Cases**:
    - Empty input: `true`.
    - Single meeting: `true`.
    - Meetings touching at the end (e.g., `[1,2]` and `[2,3]`): `true` (usually considered not overlapping).

**Optimal Python Solution**:
```python
def canAttendMeetings(intervals: list[list[int]]) -> bool:
    """
    Check for any overlaps in meetings by sorting by start time.
    """
    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    # Check if current meeting starts before previous one ends
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False

    return True
```

**Explanation**:
1.  **Sorting**: By sorting meetings by start time, any potential overlap must occur between consecutive meetings in the sorted list.
2.  **Overlap Check**: If `current_meeting.start < previous_meeting.end`, there's a conflict.
3.  **Correctness**: If the list is sorted and no adjacent meetings overlap, then no two meetings in the entire set can overlap.

**Complexity Analysis**:
- **Time Complexity**: `O(N log N)` for sorting.
- **Space Complexity**: `O(1)` additional space (excluding sort overhead).

---

## 2. Meeting Rooms II
**Problem Statement**:
Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `intervals = [[0,30],[5,10],[15,20]]`
    - Output: `2`
- **Example 2**:
    - Input: `intervals = [[7,10],[2,4]]`
    - Output: `1`

**Optimal Python Solution (Min-Heap)**:
```python
import heapq

def minMeetingRooms(intervals: list[list[int]]) -> int:
    """
    Find minimum rooms using a min-heap to track the earliest end time
    of meetings currently in progress.
    """
    if not intervals:
        return 0

    # Sort meetings by start time
    intervals.sort(key=lambda x: x[0])

    # Min-heap to store end times of meetings currently in rooms
    rooms = []

    # Add the end time of the first meeting
    heapq.heappush(rooms, intervals[0][1])

    for i in range(1, len(intervals)):
        # If the earliest ending meeting finishes BEFORE the current one starts
        if intervals[i][0] >= rooms[0]:
            # Reuse the room: remove the old end time
            heapq.heappop(rooms)

        # Add the current meeting's end time (either to the reused room
        # or as a new room)
        heapq.heappush(rooms, intervals[i][1])

    return len(rooms)
```

**Explanation**:
1.  **Greedy strategy**: We want to reuse rooms whenever possible. To maximize reuse, we should always check the room that becomes free **the soonest**.
2.  **Min-Heap**: A min-heap allows us to efficiently find the smallest end time (`rooms[0]`).
3.  **Process**:
    - Sort meetings by start time.
    - For each meeting, check if its start time is `>=` the earliest end time in the heap.
    - If yes, `heappop` to "free" that room.
    - `heappush` the new meeting's end time.
    - The final size of the heap is the number of rooms used simultaneously at the peak.

**Complexity Analysis**:
- **Time Complexity**: `O(N log N)` for sorting and `O(N log N)` for heap operations (each meeting pushed/popped once).
- **Space Complexity**: `O(N)` for the heap in the worst case where all meetings overlap.

---

## 3. Car Pooling
**Problem Statement**:
There is a car with `capacity` empty seats. The car only drives east. You are given the integer `capacity` and an array `trips` where `trips[i] = [numPassengers_i, from_i, to_i]`. Return `true` if it is possible to pick up and drop off all passengers for all the given trips.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `trips = [[2,1,5],[3,3,7]], capacity = 4`
    - Output: `false`
- **Example 2**:
    - Input: `trips = [[2,1,5],[3,3,7]], capacity = 5`
    - Output: `true`

**Optimal Python Solution (Difference Array / Bucket Sort)**:
```python
def carPooling(trips: list[list[int]], capacity: int) -> bool:
    """
    Check capacity at every point using a difference array/bucket sort approach.
    Since locations are within [0, 1000], we can use an array instead of sorting.
    """
    # Tracking changes at each milestone
    # We use 1001 because 'to' can be up to 1000
    milestones = [0] * 1001

    for passengers, start, end in trips:
        milestones[start] += passengers
        milestones[end] -= passengers

    current_passengers = 0
    for change in milestones:
        current_passengers += change
        if current_passengers > capacity:
            return False

    return True
```

**Explanation**:
1.  **Events logic**: At each `start` location, `capacity` decreases by `passengers`. At each `end` location, `capacity` increases by `passengers`.
2.  **Efficiency**: Since the locations are bounded (0 to 1000), we don't need to sort events. We can simply increment/decrement values in an array.
3.  **Prefix Sum**: Iterating through the array and keeping a running sum (`current_passengers`) tells us exactly how many people are in the car at any given point.

**Complexity Analysis**:
- **Time Complexity**: `O(N + K)`, where `N` is the number of trips and `K` is the number of locations (1000).
- **Space Complexity**: `O(K)` for the milestones array.

---

## 4. My Calendar I
**Problem Statement**:
Implement a `MyCalendar` class that can book events. An event is added if it does not cause a double booking (overlapping with an existing event). `book(start, end)` returns `true` if the event can be added.

**Optimal Python Solution (Binary Search Tree / Sorted List)**:
```python
from bisect import bisect_left

class MyCalendar:
    def __init__(self):
        self.calendar = []

    def book(self, start: int, end: int) -> bool:
        """
        Check for overlap and insert in O(log N) + O(N) for insertion.
        """
        # Find where this interval would be inserted
        idx = bisect_left(self.calendar, (start, end))

        # Check overlap with the NEXT interval
        if idx < len(self.calendar) and self.calendar[idx][0] < end:
            return False

        # Check overlap with the PREVIOUS interval
        if idx > 0 and start < self.calendar[idx-1][1]:
            return False

        self.calendar.insert(idx, (start, end))
        return True
```

**Explanation**:
1.  **Maintaining Order**: We keep the intervals sorted by their start times.
2.  **Efficient Lookup**: `bisect_left` finds the position where the interval *should* go.
3.  **Conflict check**:
    - Overlap with previous: `new.start < prev.end`
    - Overlap with next: `next.start < new.end`
4.  **Insert**: If no conflict, we insert it at the correct index.

**Complexity Analysis**:
- **Time Complexity**: `O(N)` per `book` call ( `O(log N)` search + `O(N)` insertion in a list). Using a balanced BST or `SortedList` would make it `O(log N)`.
- **Space Complexity**: `O(N)` to store the bookings.

---

## 5. My Calendar II
**Problem Statement**:
Implement a `MyCalendarTwo` class that can book events. An event is added if it does not cause a triple booking. A triple booking happens when three events have some non-empty intersection.

**Optimal Python Solution (Sweep Line / Segment Tree)**:
```python
from sortedcontainers import SortedDict

class MyCalendarTwo:
    def __init__(self):
        self.delta = SortedDict()

    def book(self, start: int, end: int) -> bool:
        """
        Check for triple booking using sweep-line.
        """
        self.delta[start] = self.delta.get(start, 0) + 1
        self.delta[end] = self.delta.get(end, 0) - 1

        active_bookings = 0
        for time in self.delta:
            active_bookings += self.delta[time]
            if active_bookings >= 3:
                # Rollback
                self.delta[start] -= 1
                self.delta[end] += 1
                return False

        return True
```

**Explanation**:
1.  **Sweep Line**: Similar to My Calendar III, we track the number of concurrent bookings.
2.  **Constraint**: We only allow the booking if the peak concurrency stays below 3.
3.  **Rollback**: If the booking causes `active_bookings` to reach 3, we undo the change to the `delta` map and return `False`.

**Complexity Analysis**:
- **Time Complexity**: `O(N)` per `book` call if using a map (to iterate through all events). `O(log N)` with a segment tree.
- **Space Complexity**: `O(N)` to store the events.

---

## 6. My Calendar III (Max Overlap)
**Problem Statement**:
Find the maximum number of concurrent bookings at any time.

**Optimal Python Solution (Sweep Line)**:
```python
from sortedcontainers import SortedDict

class MyCalendarThree:
    def __init__(self):
        # We need sorted keys for the sweep line
        self.delta = SortedDict()

    def book(self, start: int, end: int) -> int:
        """
        Use a sweep-line algorithm to find peak concurrency.
        """
        self.delta[start] = self.delta.get(start, 0) + 1
        self.delta[end] = self.delta.get(end, 0) - 1

        max_k = 0
        current_k = 0
        for time in self.delta:
            current_k += self.delta[time]
            max_k = max(max_k, current_k)

        return max_k
```

**Explanation**:
1.  **Sweep Line Algorithm**: This is the standard way to find the "peak" of overlapping intervals.
2.  **Events**: Each booking is two events: `+1` at `start` and `-1` at `end`.
3.  **Process**: We traverse all events in chronological order. The running sum of the `delta` values at any point `t` gives the number of active bookings at that time.
4.  **Goal**: The result is the maximum value of this running sum.

**Complexity Analysis**:
- **Time Complexity**: `O(N²)` if using a regular dictionary and sorting keys every time. `O(N log N)` or better if using a `SortedDict`.
- **Space Complexity**: `O(N)` to store the events.
