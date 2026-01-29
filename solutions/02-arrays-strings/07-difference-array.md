# Difference Array - Solutions

## Practice Problems

### 1. Range Addition

**Problem Statement**: You are given an integer `length` and an array `updates` where `updates[i] = [startIdxi, endIdxi, inci]`. You have an array of size `length` initialized with all 0's. For each update, you should add `inci` to all elements from `startIdxi` to `endIdxi` inclusive. Return the final array after all updates.

**Examples & Edge Cases**:

- Example: `length = 5, updates = [[1,3,2],[2,4,3],[0,2,-2]]` -> `[-2,0,3,5,3]`
- Edge Case: Empty updates.
- Edge Case: Updates that cover the entire array.

**Optimal Python Solution**:

```python
def getModifiedArray(length: int, updates: list[list[int]]) -> list[int]:
    # diff array of size length + 1 to handle endIdx + 1
    diff = [0] * (length + 1)

    for start, end, val in updates:
        diff[start] += val
        if end + 1 < length:
            diff[end + 1] -= val

    # Reconstruct the original array using prefix sum
    for i in range(1, length):
        diff[i] += diff[i - 1]

    # Return only the first 'length' elements
    return diff[:length]
```

**Explanation**:
Instead of updating every index in the range $[start, end]$, we mark the $start$ with the increment and the $end+1$ with the negative increment. This creates a "step" that, when integrated (via prefix sum), applies the increment only within the specified range.

**Complexity Analysis**:

- **Time Complexity**: O(n + k), where n is `length` and k is the number of `updates`.
- **Space Complexity**: O(n) to store the result/difference array.

---

### 2. Car Pooling

**Problem Statement**: There is a car with `capacity` empty seats. The vehicle only drives east. You are given the integer `capacity` and an array `trips` where `trips[i] = [numPassengersi, fromi, toi]`. Return `true` if it is possible to pick up and drop off all passengers for all the given trips, or `false` otherwise.

**Optimal Python Solution**:

```python
def carPooling(trips: list[list[int]], capacity: int) -> bool:
    # Use a fixed size array if locations are within a known range [0, 1000]
    # Otherwise, use a sorted map/dictionary of events
    stops = [0] * 1001

    for passengers, start, end in trips:
        stops[start] += passengers
        stops[end] -= passengers

    curr_passengers = 0
    for change in stops:
        curr_passengers += change
        if curr_passengers > capacity:
            return False

    return True
```

**Explanation**:
We treat each trip as a range update on the car's occupancy. At the `start` location, we increase the passenger count. At the `end` location, the passengers get off, so we decrease the count. By calculating the prefix sum across all locations, we get the exact occupancy at any given point.

**Complexity Analysis**:

- **Time Complexity**: O(max(n, 1001)), where n is number of trips.
- **Space Complexity**: O(1001) = O(1).

---

### 3. Corporate Flight Bookings

**Problem Statement**: There are `n` flights labeled from 1 to `n`. You are given an array of flight bookings `bookings`, where `bookings[i] = [firsti, lasti, seatsi]` represents a booking for flights `firsti` through `lasti` inclusive with `seatsi` seats reserved for each flight. Return an array `answer` of length `n`, where `answer[i]` is the total number of seats reserved for flight `i`.

**Optimal Python Solution**:

```python
def corpFlightBookings(bookings: list[list[int]], n: int) -> list[int]:
    diff = [0] * (n + 1)

    for first, last, seats in bookings:
        # Bookings are 1-indexed
        diff[first - 1] += seats
        if last < n:
            diff[last] -= seats

    # Prefix sum to get actual seats
    for i in range(1, n):
        diff[i] += diff[i - 1]

    return diff[:n]
```

**Explanation**:
This is a direct application of the difference array on a 1-indexed array. We map 1..n to 0..n-1 for convenience and apply the range updates.

**Complexity Analysis**:

- **Time Complexity**: O(n + k).
- **Space Complexity**: O(n).

---

### 4. Meeting Rooms II

**Problem Statement**: Given an array of meeting time intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of conference rooms required.

**Optimal Python Solution**:

```python
def minMeetingRooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0

    # Since time can be large, we use sorted events instead of a fixed array
    events = []
    for start, end in intervals:
        events.append((start, 1))  # Room becomes occupied
        events.append((end, -1))   # Room becomes free

    # Sort by time. If times are equal, process end (-1) before start (1)
    # depending on whether meetings can share the same end/start time.
    # Usually, if one ends at 10 and another starts at 10, they need different rooms
    # or the same room. Check problem constraints. Assuming they can't share:
    events.sort()

    max_rooms = 0
    curr_rooms = 0
    for time, delta in events:
        curr_rooms += delta
        max_rooms = max(max_rooms, curr_rooms)

    return max_rooms
```

**Explanation**:
Minimum rooms is equivalent to the maximum number of concurrent meetings. We mark the start of a meeting as `+1` room and the end as `-1` room. Sorting these events and calculating the running sum gives us the number of rooms in use at any point in time.

**Complexity Analysis**:

- **Time Complexity**: O(n log n) due to sorting.
- **Space Complexity**: O(n) to store the events.

---

### 5. My Calendar III

**Problem Statement**: A k-booking happens when `k` events have some non-empty intersection. Find the maximum `k` such that there exists a k-booking.

**Optimal Python Solution**:

```python
from bisect import insort

class MyCalendarThree:
    def __init__(self):
        # We use a sorted list of events (SortedDict equivalent in pure Python)
        self.events = [] # List of (time, delta)

    def book(self, startTime: int, endTime: int) -> int:
        # Standard range update: start +1, end -1
        # In an interview, using a SortedDict (like from sortedcontainers) is better
        # Here we manually maintain order for demonstration
        insort(self.events, (startTime, 1))
        insort(self.events, (endTime, -1))

        max_k = 0
        curr_k = 0
        for time, delta in self.events:
            curr_k += delta
            max_k = max(max_k, curr_k)

        return max_k
```

**Explanation**:
This is a dynamic version of the "maximum concurrent events" problem. Every time a new booking is added, we perform a range update and recalculate the maximum overlap.

**Complexity Analysis**:

- **Time Complexity**: O(n) per `book` call (due to `insort` and the loop). Total O(n²) for n calls.
- **Space Complexity**: O(n).

---

### 6. Brightest Position on Street

**Problem Statement**: A street is represented as a number line. You are given a 2D integer array `lights` where `lights[i] = [positioni, rangei]` indicates that there is a street lamp at `positioni` that lights up the area from `[positioni - rangei, positioni + rangei]` inclusive. Return the brightest position on the street. If there are multiple, return the smallest one.

**Optimal Python Solution**:

```python
def brightestPosition(lights: list[list[int]]) -> int:
    events = []
    for pos, r in lights:
        events.append((pos - r, 1))
        events.append((pos + r + 1, -1))

    # Sort events. Smaller position first.
    # For same position, +1 comes before -1 because the range is inclusive.
    events.sort()

    max_brightness = 0
    curr_brightness = 0
    best_pos = 0

    for pos, delta in events:
        curr_brightness += delta
        if curr_brightness > max_brightness:
            max_brightness = curr_brightness
            best_pos = pos

    return best_pos
```

**Explanation**:
Each light illuminates a range `[start, end]`. We convert this into range updates `(start, +1)` and `(end + 1, -1)`. The brightest position is where the prefix sum of these updates is maximized.

**Complexity Analysis**:

- **Time Complexity**: O(n log n).
- **Space Complexity**: O(n).
