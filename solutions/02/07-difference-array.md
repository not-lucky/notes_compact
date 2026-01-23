# Difference Array

## Practice Problems

### 1. Range Addition
**Difficulty:** Medium
**Key Concept:** Basic difference array

```python
def get_modified_array(length: int, updates: list[list[int]]) -> list[int]:
    """
    Time: O(n + k)
    Space: O(n)
    """
    diff = [0] * (length + 1)
    for start, end, val in updates:
        diff[start] += val
        diff[end + 1] -= val

    res = [0] * length
    curr = 0
    for i in range(length):
        curr += diff[i]
        res[i] = curr
    return res
```

### 2. Car Pooling
**Difficulty:** Medium
**Key Concept:** Capacity check

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """
    Time: O(max(n, 1001))
    Space: O(1001)
    """
    diff = [0] * 1001
    for passengers, start, end in trips:
        diff[start] += passengers
        diff[end] -= passengers

    curr = 0
    for i in range(1001):
        curr += diff[i]
        if curr > capacity: return False
    return True
```

### 3. Corporate Flight Bookings
**Difficulty:** Medium
**Key Concept:** 1-indexed bookings

```python
def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:
    """
    Time: O(n + k)
    Space: O(n)
    """
    diff = [0] * (n + 2)
    for first, last, seats in bookings:
        diff[first] += seats
        diff[last + 1] -= seats

    res = []
    curr = 0
    for i in range(1, n + 1):
        curr += diff[i]
        res.append(curr)
    return res
```

### 4. Meeting Rooms II
**Difficulty:** Medium
**Key Concept:** Maximum concurrent

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Time: O(n log n)
    Space: O(n)
    """
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    events.sort()

    res = 0
    curr = 0
    for _, delta in events:
        curr += delta
        res = max(res, curr)
    return res
```

### 5. My Calendar III
**Difficulty:** Hard
**Key Concept:** Maximum overlapping events

```python
from bisect import insort

class MyCalendarThree:
    def __init__(self):
        self.diff = [] # list of (time, delta)

    def book(self, start: int, end: int) -> int:
        insort(self.diff, (start, 1))
        insort(self.diff, (end, -1))
        res = 0
        curr = 0
        for _, delta in self.diff:
            curr += delta
            res = max(res, curr)
        return res
```

### 6. Brightest Position on Street
**Difficulty:** Medium
**Key Concept:** Light intensity

```python
def brightest_position(lights: list[list[int]]) -> int:
    """
    Time: O(n log n)
    Space: O(n)
    """
    events = []
    for pos, r in lights:
        events.append((pos - r, 1))
        events.append((pos + r + 1, -1))
    events.sort()

    max_brightness = 0
    curr_brightness = 0
    res_pos = 0
    for pos, delta in events:
        curr_brightness += delta
        if curr_brightness > max_brightness:
            max_brightness = curr_brightness
            res_pos = pos
    return res_pos
```
