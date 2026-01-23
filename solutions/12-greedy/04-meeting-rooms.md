# Practice Problems - Meeting Rooms

## 1. Meeting Rooms

### Problem Statement
Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings.

### Constraints
- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i < end_i <= 10^6`

### Example
**Input:** `intervals = [[0,30],[5,10],[15,20]]`
**Output:** `false`

### Python Implementation
```python
def canAttendMeetings(intervals: list[list[int]]) -> bool:
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True
```

## 2. Meeting Rooms II

### Problem Statement
Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, find the minimum number of conference rooms required.

### Constraints
- `1 <= intervals.length <= 10^4`
- `0 <= start_i < end_i <= 10^6`

### Example
**Input:** `intervals = [[0,30],[5,10],[15,20]]`
**Output:** `2`

### Python Implementation
```python
import heapq

def minMeetingRooms(intervals: list[list[int]]) -> int:
    if not intervals: return 0
    intervals.sort()
    rooms = []
    heapq.heappush(rooms, intervals[0][1])
    for i in range(1, len(intervals)):
        if intervals[i][0] >= rooms[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, intervals[i][1])
    return len(rooms)
```

## 3. Car Pooling

### Problem Statement
There is a car with `capacity` empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).
You are given the integer `capacity` and an array `trips` where `trips[i] = [numPassengers_i, from_i, to_i]` indicates that the `i-th` trip has `numPassengers_i` passengers and the locations to pick them up and drop them off are `from_i` and `to_i` respectively. The locations are given as the number of kilometers due east from the car's initial location.
Return `true` if it is possible to pick up and drop off all passengers for all the given trips, or `false` otherwise.

### Constraints
- `1 <= trips.length <= 1000`
- `trips[i].length == 3`
- `1 <= numPassengers_i <= 100`
- `0 <= from_i < to_i <= 1000`
- `1 <= capacity <= 10^5`

### Example
**Input:** `trips = [[2,1,5],[3,3,7]], capacity = 4`
**Output:** `false`

### Python Implementation
```python
def carPooling(trips: list[list[int]], capacity: int) -> bool:
    diff = [0] * 1001
    for n, f, t in trips:
        diff[f] += n
        diff[t] -= n
    cur = 0
    for d in diff:
        cur += d
        if cur > capacity:
            return False
    return True
```

## 4. My Calendar I

### Problem Statement
You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a double booking.
A double booking happens when two events have some non-empty intersection (i.e., some moment is common to both events).
Implement the `MyCalendar` class:
- `MyCalendar()` Initializes the calendar object.
- `boolean book(int start, int end)` Returns `true` if the event can be added to the calendar successfully without causing a double booking. Otherwise, return `false` and do not add the event to the calendar.

### Constraints
- `0 <= start < end <= 10^9`
- At most `1000` calls will be made to `book`.

### Example
**Input:** `["MyCalendar", "book", "book", "book"]`, `[[], [10, 20], [15, 25], [20, 30]]`
**Output:** `[null, true, false, true]`

### Python Implementation
```python
class MyCalendar:
    def __init__(self):
        self.calendar = []

    def book(self, start: int, end: int) -> bool:
        for s, e in self.calendar:
            if start < e and s < end:
                return False
        self.calendar.append((start, end))
        return True
```

## 5. My Calendar II

### Problem Statement
Implement a `MyCalendarTwo` class to store your events. A new event can be added if adding the event will not cause a triple booking.
A triple booking happens when three events have some non-empty intersection (i.e., some moment is common to all three events).
Implement the `MyCalendarTwo` class:
- `MyCalendarTwo()` Initializes the calendar object.
- `boolean book(int start, int end)` Returns `true` if the event can be added to the calendar successfully without causing a triple booking. Otherwise, return `false` and do not add the event to the calendar.

### Constraints
- `0 <= start < end <= 10^9`
- At most `1000` calls will be made to `book`.

### Example
**Input:** `["MyCalendarTwo", "book", "book", "book", "book", "book", "book"]`, `[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]`
**Output:** `[null, true, true, true, false, true, true]`

### Python Implementation
```python
class MyCalendarTwo:
    def __init__(self):
        self.calendar = []
        self.overlaps = []

    def book(self, start: int, end: int) -> bool:
        for s, e in self.overlaps:
            if start < e and s < end:
                return False
        for s, e in self.calendar:
            if start < e and s < end:
                self.overlaps.append((max(start, s), min(end, e)))
        self.calendar.append((start, end))
        return True
```

## 6. My Calendar III

### Problem Statement
Implement a `MyCalendarThree` class to store your events. A new event can always be added.
Implement the `MyCalendarThree` class:
- `MyCalendarThree()` Initializes the object.
- `int book(int start, int end)` Returns an integer `k` representing the largest integer such that there exists a `k-booking` in the calendar.
A `k-booking` happens when `k` events have some non-empty intersection.

### Constraints
- `0 <= start < end <= 10^9`
- At most `400` calls will be made to `book`.

### Example
**Input:** `["MyCalendarThree", "book", "book", "book", "book", "book", "book"]`, `[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]`
**Output:** `[null, 1, 1, 2, 3, 3, 3]`

### Python Implementation
```python
from bisect import bisect_left, insort

class MyCalendarThree:
    def __init__(self):
        self.times = []
        self.diff = []

    def book(self, start: int, end: int) -> int:
        idx1 = bisect_left(self.times, start)
        if idx1 < len(self.times) and self.times[idx1] == start:
            self.diff[idx1] += 1
        else:
            self.times.insert(idx1, start)
            self.diff.insert(idx1, 1)

        idx2 = bisect_left(self.times, end)
        if idx2 < len(self.times) and self.times[idx2] == end:
            self.diff[idx2] -= 1
        else:
            self.times.insert(idx2, end)
            self.diff.insert(idx2, -1)

        res = cur = 0
        for d in self.diff:
            cur += d
            res = max(res, cur)
        return res
```
